================================================================================
Linux Interrupts & Concurrency - Comprehensive Reference
================================================================================

**Professional Linux Kernel Architecture - Chapters 5, 14, 17**

**Last Updated:** January 2026

**Author:** Comprehensive consolidation from kernel sources

================================================================================

TL;DR - Quick Reference
================================================================================

**Interrupt Handling - The Modern Way (2026)**

::

    New drivers → Use threaded IRQ (request_threaded_irq)
    Legacy code → Tasklets OK, but migrate to workqueue BH
    Performance-critical → Softirq (rare, only core subsystems)
    
    Top-half: Fast check (< 100µs), return IRQ_WAKE_THREAD
    Bottom-half: Real work in kernel thread (can sleep, allocate)

**Key Decision Matrix**

.. list-table:: **Which Deferred Work Mechanism?**
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Mechanism
     - Can Sleep?
     - Context
     - Latency
     - 2026 Status
   * - **Softirq**
     - ✗ No
     - Interrupt
     - Lowest
     - Core only, avoid new
   * - **Tasklet**
     - ✗ No
     - Interrupt
     - Low
     - Legacy, migrate away
   * - **Workqueue**
     - ✓ Yes
     - Process
     - Medium
     - **Preferred**
   * - **Threaded IRQ**
     - ✓ Yes
     - Process
     - Medium
     - **Best for drivers**

**Critical Interrupt Constraints**

::

    In interrupt context (top-half):
    ✗ Cannot sleep
    ✗ Cannot call schedule()
    ✗ Cannot use mutex (use spinlock)
    ✗ Cannot allocate memory (except GFP_ATOMIC)
    ✗ Cannot access user space
    ✓ Must be FAST (< 100 microseconds)

**Locking Primitives Quick Reference**

.. list-table:: **Synchronization Mechanisms**
   :header-rows: 1
   :widths: 15 15 15 20 35

   * - Primitive
     - Can Sleep?
     - IRQ Safe?
     - Use Case
     - API
   * - **Spinlock**
     - ✗ No
     - ✓ Yes
     - Short critical sections
     - spin_lock/unlock
   * - **Mutex**
     - ✓ Yes
     - ✗ No
     - Long critical sections
     - mutex_lock/unlock
   * - **RCU**
     - Readers: No
     - ✓ Yes
     - Read-mostly data
     - rcu_read_lock/unlock
   * - **Seqlock**
     - Readers: No
     - ✓ Yes
     - Readers retry on conflict
     - read_seqbegin/retry
   * - **Completion**
     - ✓ Yes
     - ✗ No
     - Wait for event
     - wait_for_completion

**Most Common Patterns (2026)**

.. code-block:: c

   // Pattern 1: Threaded IRQ (BEST PRACTICE)
   static irqreturn_t quick_check(int irq, void *dev) {
       if (!device_ready(dev))
           return IRQ_NONE;
       return IRQ_WAKE_THREAD;  // Wake bottom-half thread
   }
   
   static irqreturn_t process_data(int irq, void *dev) {
       mutex_lock(&dev->lock);
       // Can sleep, allocate, block here
       mutex_unlock(&dev->lock);
       return IRQ_HANDLED;
   }
   
   request_threaded_irq(irq, quick_check, process_data,
                        IRQF_ONESHOT, "mydev", dev);

   // Pattern 2: Simple IRQ + Workqueue
   static irqreturn_t fast_isr(int irq, void *dev) {
       schedule_work(&dev->work);
       return IRQ_HANDLED;
   }
   
   static void work_func(struct work_struct *work) {
       struct mydev *dev = container_of(work, struct mydev, work);
       // Process in workqueue thread
   }

**Key Monitoring Commands**

::

    cat /proc/interrupts          # IRQ statistics per CPU
    cat /proc/softirqs            # Softirq statistics
    ps aux | grep "irq/"          # Threaded IRQ threads
    ps aux | grep kworker         # Workqueue threads
    perf record -e irq:*          # Profile interrupts

**Critical Architecture Points**

::

    Hardware IRQ → CPU → APIC/GIC → Generic IRQ layer
                                  → Driver handler (top-half)
                                  → Bottom-half (deferred work)
    
    IRQ Numbers:
    - x86: 0-255 (vector-based)
    - ARM GIC: SGI (0-15), PPI (16-31), SPI (32-1019)
    
    Affinity: /proc/irq/N/smp_affinity (CPU binding)

================================================================================

1. Interrupt Fundamentals
================================================================================

1.1 What is an Interrupt?
--------------------------

An **interrupt** is a hardware signal that temporarily stops CPU execution to handle an event. The CPU saves its state, executes an **interrupt handler** (ISR), then resumes normal execution.

**Types of Interrupts:**

1. **External Hardware IRQs** - From devices (keyboard, network card, timer)
2. **Software Interrupts** - Triggered by CPU instructions (int 0x80, syscalls)
3. **Inter-Processor Interrupts (IPI)** - CPU-to-CPU communication in SMP
4. **Non-Maskable Interrupts (NMI)** - Critical events (hardware errors, watchdog)
5. **Exceptions** - CPU-generated (page fault, divide by zero, invalid opcode)

**Hardware Interrupt Flow:**

::

    Device Event → IRQ Line → Interrupt Controller (APIC/GIC)
                → CPU Core → Vector Lookup → Handler Execution
                → Return from Interrupt (IRET/ERET)

1.2 Interrupt Controllers
--------------------------

**x86/x64: APIC (Advanced Programmable Interrupt Controller)**

.. code-block:: text

    Legacy PIC (8259) → replaced by APIC
    
    LAPIC (Local APIC) - One per CPU core
    ├── Receives local interrupts (timer, thermal, performance)
    ├── Receives IPIs from other CPUs
    └── Delivers interrupts as vectors (0-255)
    
    I/O APIC - Handles external device interrupts
    ├── Routes IRQs to specific CPUs
    └── Supports level/edge triggering

**ARM: GIC (Generic Interrupt Controller)**

.. code-block:: text

    GIC Distributor (global component)
    ├── SPIs (Shared Peripheral Interrupts): 32-1019
    ├── Handles prioritization, masking, routing
    └── Routes to GIC Redistributor
    
    GIC Redistributor (per-CPU component)
    ├── PPIs (Private Peripheral Interrupts): 16-31
    ├── SGIs (Software Generated Interrupts): 0-15
    └── Delivers to CPU core

**Device Tree Example (ARM GIC):**

.. code-block:: dts

    intc: interrupt-controller@f1001000 {
        compatible = "arm,gic-400";
        #interrupt-cells = <3>;
        interrupt-controller;
        reg = <0xf1001000 0x1000>,  /* Distributor */
              <0xf1002000 0x2000>;  /* CPU interface */
    };
    
    uart@12340000 {
        compatible = "vendor,uart";
        reg = <0x12340000 0x1000>;
        interrupts = <GIC_SPI 45 IRQ_TYPE_LEVEL_HIGH>;
        /* Shared peripheral IRQ 45, level-triggered */
    };

1.3 Interrupt Context Constraints
----------------------------------

**What You CANNOT Do in Interrupt Context:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Action
     - Reason
   * - **Sleep or schedule()**
     - No process context, scheduler cannot be called
   * - **Use mutex**
     - Mutex can sleep while waiting
   * - **Allocate memory (GFP_KERNEL)**
     - May sleep if memory is low
   * - **Access user space**
     - May page fault, causing sleep
   * - **Call blocking functions**
     - Includes I/O operations, msleep(), wait_event()
   * - **Take too long (> 100µs)**
     - Delays other interrupts, degrades system responsiveness

**What You CAN Do:**

.. code-block:: text

    ✓ Read/write device registers
    ✓ Use spinlocks (spin_lock, spin_lock_irqsave)
    ✓ Allocate memory with GFP_ATOMIC (risky, limited)
    ✓ Schedule bottom-halves (tasklet, workqueue, threaded IRQ)
    ✓ Access kernel memory
    ✓ Use atomic operations (atomic_t, test_and_set_bit)

1.4 Interrupt Processing Timeline
----------------------------------

.. code-block:: text

    t=0µs:     Hardware event (packet arrival, key press)
               ↓
    t=0.1µs:   Interrupt signal to CPU APIC/GIC
               ↓
    t=0.5µs:   CPU finishes current instruction
               ├── Saves registers, flags, return address
               ├── Switches to interrupt stack
               └── Disables preemption
               ↓
    t=1µs:     Kernel interrupt entry (arch-specific asm)
               └── Calls generic_handle_irq()
               ↓
    t=2µs:     IRQ descriptor lookup
               └── Calls registered handler(s)
               ↓
    t=3-100µs: **Top-half handler executes** (MUST BE FAST!)
               ├── Check if our interrupt
               ├── Read device status
               ├── Ack interrupt at device
               └── Schedule bottom-half if needed
               ↓
    t=100µs:   Return from interrupt
               ├── Restore context
               ├── Re-enable interrupts
               └── Resume interrupted code
               ↓
    Later:     **Bottom-half executes** (asynchronously)
               └── Softirq/tasklet: soon (microseconds)
               └── Workqueue: when scheduled (milliseconds)
               └── Threaded IRQ: when thread runs

1.5 IRQ Flags and Return Values
--------------------------------

**Common request_irq() Flags:**

.. code-block:: c

    IRQF_SHARED       // Multiple handlers can share this IRQ
    IRQF_TRIGGER_RISING   // Edge-triggered, rising edge
    IRQF_TRIGGER_FALLING  // Edge-triggered, falling edge
    IRQF_TRIGGER_HIGH     // Level-triggered, active high
    IRQF_TRIGGER_LOW      // Level-triggered, active low
    IRQF_ONESHOT      // Keep IRQ disabled during thread execution
    IRQF_NO_SUSPEND   // IRQ active during system suspend
    IRQF_PERCPU       // Per-CPU interrupt (no migration)

**Handler Return Values:**

.. code-block:: c

    IRQ_NONE         // Not our interrupt (shared IRQ scenario)
    IRQ_HANDLED      // We handled the interrupt
    IRQ_WAKE_THREAD  // Wake threaded handler (threaded IRQ only)

**Example:**

.. code-block:: c

    static irqreturn_t my_handler(int irq, void *dev_id) {
        struct my_device *dev = dev_id;
        u32 status = readl(dev->regs + STATUS);
        
        if (!(status & MY_IRQ_FLAG))
            return IRQ_NONE;  // Not ours (shared IRQ)
        
        // Clear interrupt at device
        writel(status, dev->regs + STATUS);
        
        // Schedule bottom-half
        tasklet_schedule(&dev->tasklet);
        
        return IRQ_HANDLED;
    }

================================================================================

2. Bottom-Half Mechanisms (Deferred Work)
================================================================================

2.1 Why Bottom-Halves?
-----------------------

Interrupt handlers must execute quickly (< 100µs). Bottom-halves defer time-consuming work to run later in a safer context.

**Top-Half vs Bottom-Half:**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Top-Half (IRQ Handler)
     - Bottom-Half
   * - **Context**
     - Interrupt context
     - Varies (softirq, process)
   * - **Can sleep?**
     - ✗ No
     - Depends on mechanism
   * - **When runs?**
     - Immediately when IRQ fires
     - Deferred, asynchronous
   * - **Duration**
     - < 100µs (MUST be fast)
     - Can take milliseconds
   * - **Work done**
     - Minimal: check, ack, schedule BH
     - Actual data processing

2.2 Softirq - Core Kernel Only
-------------------------------

**Characteristics:**

- Runs in interrupt context (cannot sleep)
- Highest priority deferred work
- Fixed set of 32 slots (only 10 used)
- Same softirq can run on multiple CPUs simultaneously
- **Use only for core subsystems** - new softirqs almost never accepted

**Predefined Softirqs:**

.. code-block:: c

    HI_SOFTIRQ          = 0,  // High-priority tasklets
    TIMER_SOFTIRQ       = 1,  // Timer bottom-halves
    NET_TX_SOFTIRQ      = 2,  // Network transmit
    NET_RX_SOFTIRQ      = 3,  // Network receive
    BLOCK_SOFTIRQ       = 4,  // Block devices
    IRQ_POLL_SOFTIRQ    = 5,  // IO completion polling
    TASKLET_SOFTIRQ     = 6,  // Regular tasklets
    SCHED_SOFTIRQ       = 7,  // Scheduler
    HRTIMER_SOFTIRQ     = 8,  // High-resolution timers
    RCU_SOFTIRQ         = 9,  // RCU callbacks

**API (rarely used in drivers):**

.. code-block:: c

    // Register softirq (kernel internal use only)
    open_softirq(NET_RX_SOFTIRQ, net_rx_action);
    
    // Raise softirq
    raise_softirq(NET_RX_SOFTIRQ);

**Monitoring:**

.. code-block:: bash

    cat /proc/softirqs
    #           CPU0       CPU1       CPU2       CPU3
    # HI:          0          0          0          0
    # TIMER:  123456     123500     123480     123520
    # NET_TX:  45000      45100      44950      45050
    # NET_RX: 890000     891000     889500     890500

2.3 Tasklet - Legacy But Common
--------------------------------

**Characteristics:**

- Runs in softirq context (cannot sleep)
- Dynamically allocated
- **Automatic serialization** - same tasklet runs on only ONE CPU at a time
- Different tasklets can run in parallel on different CPUs
- **Status: Legacy, being replaced by workqueue BH**

**API:**

.. code-block:: c

    // Declare tasklet
    void tasklet_func(unsigned long data);
    DECLARE_TASKLET(my_tasklet, tasklet_func, (unsigned long)dev);
    
    // Or dynamic allocation
    struct tasklet_struct *t = kmalloc(sizeof(*t), GFP_KERNEL);
    tasklet_init(t, tasklet_func, (unsigned long)dev);
    
    // Schedule tasklet (from IRQ handler)
    tasklet_schedule(&my_tasklet);
    
    // High-priority tasklet
    tasklet_hi_schedule(&my_tasklet);
    
    // Disable/enable tasklet
    tasklet_disable(&my_tasklet);  // Wait for completion
    tasklet_enable(&my_tasklet);
    
    // Cleanup
    tasklet_kill(&my_tasklet);

**Example:**

.. code-block:: c

    struct my_device {
        struct tasklet_struct rx_tasklet;
        void __iomem *regs;
    };
    
    static void rx_tasklet_func(unsigned long dev_ptr) {
        struct my_device *dev = (void *)dev_ptr;
        
        // Process received data (cannot sleep!)
        while (readl(dev->regs + STATUS) & RX_READY) {
            u32 data = readl(dev->regs + RX_DATA);
            process_packet(dev, data);
        }
    }
    
    static irqreturn_t irq_handler(int irq, void *dev_id) {
        struct my_device *dev = dev_id;
        
        if (readl(dev->regs + STATUS) & RX_READY) {
            tasklet_schedule(&dev->rx_tasklet);
            return IRQ_HANDLED;
        }
        return IRQ_NONE;
    }
    
    // Init
    tasklet_init(&dev->rx_tasklet, rx_tasklet_func, (unsigned long)dev);
    request_irq(dev->irq, irq_handler, 0, "mydev", dev);

2.4 Workqueue - Modern Preferred Choice
----------------------------------------

**Characteristics:**

- Runs in **process context** (can sleep!)
- Can allocate memory with GFP_KERNEL
- Can take mutexes, call blocking functions
- Multiple work items can run in parallel
- **2026 Best Practice** for most deferred work

**Types of Workqueues:**

.. code-block:: c

    system_wq              // Shared, general purpose
    system_highpri_wq      // High priority
    system_long_wq         // Long-running work
    system_unbound_wq      // Not bound to specific CPU
    system_bh_wq           // BH context (new, tasklet replacement)

**API:**

.. code-block:: c

    // Declare work
    static void work_func(struct work_struct *work);
    DECLARE_WORK(my_work, work_func);
    
    // Or embedded in structure
    struct my_device {
        struct work_struct process_work;
    };
    
    INIT_WORK(&dev->process_work, work_func);
    
    // Schedule work (on system_wq)
    schedule_work(&my_work);
    
    // Schedule on specific queue
    queue_work(system_highpri_wq, &my_work);
    
    // Delayed work
    DECLARE_DELAYED_WORK(delayed, work_func);
    schedule_delayed_work(&delayed, msecs_to_jiffies(100));
    
    // Cleanup
    cancel_work_sync(&my_work);       // Wait for completion
    flush_work(&my_work);
    flush_workqueue(my_wq);

**Example:**

.. code-block:: c

    struct my_device {
        struct work_struct data_work;
        struct mutex lock;
        void *buffer;
    };
    
    static void data_work_func(struct work_struct *work) {
        struct my_device *dev = container_of(work, 
                                    struct my_device, data_work);
        
        // Process context - can sleep, allocate, block!
        mutex_lock(&dev->lock);
        
        // Safe to allocate memory
        void *data = kmalloc(4096, GFP_KERNEL);
        
        // Safe to call blocking functions
        msleep(10);
        copy_to_user(dev->buffer, data, 4096);
        
        mutex_unlock(&dev->lock);
        kfree(data);
    }
    
    static irqreturn_t irq_handler(int irq, void *dev_id) {
        struct my_device *dev = dev_id;
        schedule_work(&dev->data_work);
        return IRQ_HANDLED;
    }

**Custom Workqueue:**

.. code-block:: c

    // Create custom workqueue
    struct workqueue_struct *wq;
    wq = create_workqueue("my_work");        // Bound to CPUs
    wq = create_singlethread_workqueue("my");  // Single thread
    wq = alloc_workqueue("my", WQ_HIGHPRI, 0); // With flags
    
    // Queue work
    queue_work(wq, &my_work);
    queue_delayed_work(wq, &delayed, HZ);
    
    // Cleanup
    destroy_workqueue(wq);

2.5 Threaded IRQ - Best Practice for Drivers
---------------------------------------------

**Characteristics:**

- Split handler into top-half and bottom-half
- Bottom-half runs in dedicated per-IRQ kernel thread
- Process context → can sleep, allocate, block
- **2026 Strongly Recommended** for most new drivers
- Automatic serialization per IRQ

**API:**

.. code-block:: c

    int request_threaded_irq(unsigned int irq,
                             irq_handler_t handler,      // Top-half
                             irq_handler_t thread_fn,    // Bottom-half
                             unsigned long flags,
                             const char *name,
                             void *dev);

**Flags:**

.. code-block:: c

    IRQF_ONESHOT     // Keep IRQ disabled during thread (level-triggered)
    IRQF_SHARED      // Shared IRQ line
    IRQF_TRIGGER_*   // Trigger type

**Complete Example:**

.. code-block:: c

    struct uart_port {
        int irq;
        void __iomem *regs;
        struct mutex lock;
        char rx_buffer[4096];
    };
    
    // Top-half: Quick check in interrupt context
    static irqreturn_t uart_irq_quick(int irq, void *dev_id) {
        struct uart_port *port = dev_id;
        u32 status = readl(port->regs + UART_STATUS);
        
        if (!(status & UART_RX_READY))
            return IRQ_NONE;  // Not our interrupt
        
        // Clear interrupt flag
        writel(UART_IRQ_CLR, port->regs + UART_CTRL);
        
        return IRQ_WAKE_THREAD;  // Wake bottom-half thread
    }
    
    // Bottom-half: Real work in process context
    static irqreturn_t uart_irq_thread(int irq, void *dev_id) {
        struct uart_port *port = dev_id;
        
        // Process context - can sleep, allocate, use mutex!
        mutex_lock(&port->lock);
        
        // Read data from device
        while (readl(port->regs + UART_STATUS) & UART_RX_READY) {
            char c = readl(port->regs + UART_RX_DATA);
            port->rx_buffer[port->rx_head++] = c;
        }
        
        // Safe to copy to user space
        copy_to_user(port->user_buffer, port->rx_buffer, port->rx_head);
        
        // Safe to wake up waiting processes
        wake_up_interruptible(&port->wait_queue);
        
        mutex_unlock(&port->lock);
        
        return IRQ_HANDLED;
    }
    
    // Registration
    ret = request_threaded_irq(port->irq,
                               uart_irq_quick,     // Top-half
                               uart_irq_thread,    // Bottom-half
                               IRQF_ONESHOT,       // Level-triggered safety
                               "uart",
                               port);
    
    // Cleanup
    free_irq(port->irq, port);

**Monitoring Threaded IRQs:**

.. code-block:: bash

    # View IRQ threads
    ps aux | grep "irq/"
    # irq/45-eth0     # Threaded IRQ for IRQ 45
    # irq/46-uart     # Threaded IRQ for IRQ 46

2.6 Comparison and Decision Matrix
-----------------------------------

.. list-table:: **Bottom-Half Mechanisms Detailed Comparison**
   :header-rows: 1
   :widths: 15 12 12 12 12 12 12 13

   * - Mechanism
     - Context
     - Sleep?
     - Mutex?
     - Concurrency
     - Latency
     - 2026 Status
   * - **Softirq**
     - Interrupt
     - ✗ No
     - ✗ No
     - Multi-CPU OK
     - Lowest
     - Core only
   * - **Tasklet**
     - Interrupt
     - ✗ No
     - ✗ No
     - Serialized
     - Low
     - **Migrate away**
   * - **Workqueue**
     - Process
     - ✓ Yes
     - ✓ Yes
     - Parallel OK
     - Medium
     - **Preferred**
   * - **Threaded IRQ**
     - Process
     - ✓ Yes
     - ✓ Yes
     - Per-IRQ thread
     - Medium
     - **Best for drivers**
   * - **Workqueue BH**
     - Interrupt
     - ✗ No
     - ✗ No
     - Parallel OK
     - Low
     - Tasklet replacement

**Decision Tree (2026):**

.. code-block:: text

    Need to defer work from IRQ?
    │
    ├── Can sleep / allocate / block?
    │   ├── Yes → Tied to specific IRQ?
    │   │   ├── Yes → **Threaded IRQ** (request_threaded_irq)
    │   │   └── No → **Workqueue** (schedule_work)
    │   │
    │   └── No (atomic context required)
    │       ├── Performance-critical core subsystem?
    │       │   └── Yes → **Softirq** (rare, core only)
    │       │
    │       └── Need simple serialization?
    │           ├── Legacy code → **Tasklet** (plan migration)
    │           └── Modern code → **Workqueue BH** (system_bh_wq)

================================================================================
3. Synchronization Primitives & Locking
================================================================================

3.1 Why Synchronization?
-------------------------

Multiple execution contexts (IRQs, softirqs, kernel threads, user processes) can access shared data simultaneously on SMP systems. Synchronization prevents race conditions and data corruption.

**Critical Section:** Code that accesses shared data and must not be interrupted.

3.2 Spinlocks - For Short Critical Sections
--------------------------------------------

**Characteristics:**

- Busy-wait lock (CPU spins in loop while waiting)
- **Cannot sleep** while holding spinlock
- Use for very short critical sections (microseconds)
- IRQ-safe variants available
- **Disables preemption** automatically

**Types:**

.. code-block:: c

    spinlock_t           // Basic spinlock
    rwlock_t             // Read-write spinlock
    raw_spinlock_t       // Non-RT spinlock (RT kernel)

**API:**

.. code-block:: c

    // Declaration
    DEFINE_SPINLOCK(my_lock);
    
    // Or dynamic
    spinlock_t lock;
    spin_lock_init(&lock);
    
    // Basic locking
    spin_lock(&lock);
    /* Critical section */
    spin_unlock(&lock);
    
    // IRQ-safe locking (disables IRQs on local CPU)
    unsigned long flags;
    spin_lock_irqsave(&lock, flags);
    /* Critical section */
    spin_unlock_irqrestore(&lock, flags);
    
    // Bottom-half safe (disables softirqs/tasklets)
    spin_lock_bh(&lock);
    /* Critical section */
    spin_unlock_bh(&lock);
    
    // Try to acquire (non-blocking)
    if (spin_trylock(&lock)) {
        /* Got lock */
        spin_unlock(&lock);
    }

**When to Use Which Variant:**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Variant
     - Use When
     - Disables
   * - **spin_lock**
     - Process context only
     - Preemption
   * - **spin_lock_irqsave**
     - IRQ + process context
     - Preemption + local IRQs
   * - **spin_lock_bh**
     - BH + process context
     - Preemption + softirqs/tasklets
   * - **spin_lock_irq**
     - Know IRQs already disabled
     - Preemption + local IRQs

**Example:**

.. code-block:: c

    struct shared_data {
        spinlock_t lock;
        int counter;
        struct list_head list;
    };
    
    // From process context
    void update_counter(struct shared_data *data) {
        unsigned long flags;
        spin_lock_irqsave(&data->lock, flags);
        data->counter++;
        spin_unlock_irqrestore(&data->lock, flags);
    }
    
    // From IRQ handler
    static irqreturn_t irq_handler(int irq, void *dev_id) {
        struct shared_data *data = dev_id;
        
        spin_lock(&data->lock);  // IRQ context, already disabled
        data->counter--;
        spin_unlock(&data->lock);
        
        return IRQ_HANDLED;
    }

**Read-Write Spinlock:**

.. code-block:: c

    DEFINE_RWLOCK(my_rwlock);
    
    // Reader (multiple readers can hold simultaneously)
    read_lock(&my_rwlock);
    /* Read shared data */
    read_unlock(&my_rwlock);
    
    // Writer (exclusive access)
    write_lock(&my_rwlock);
    /* Modify shared data */
    write_unlock(&my_rwlock);
    
    // IRQ-safe variants
    read_lock_irqsave(&my_rwlock, flags);
    write_lock_irqsave(&my_rwlock, flags);

3.3 Mutexes - For Longer Critical Sections
-------------------------------------------

**Characteristics:**

- Sleep lock (blocks waiting thread, schedules others)
- **Can sleep** while holding mutex
- Use for longer critical sections (milliseconds)
- **Cannot use in IRQ context**
- More efficient than spinlock for longer waits

**API:**

.. code-block:: c

    // Declaration
    DEFINE_MUTEX(my_mutex);
    
    // Or dynamic
    struct mutex lock;
    mutex_init(&lock);
    
    // Lock (sleeps if unavailable)
    mutex_lock(&lock);
    /* Critical section - can sleep, allocate, etc. */
    mutex_unlock(&lock);
    
    // Interruptible (can be interrupted by signals)
    if (mutex_lock_interruptible(&lock))
        return -ERESTARTSYS;  // Signal received
    mutex_unlock(&lock);
    
    // Try to acquire (non-blocking)
    if (mutex_trylock(&lock)) {
        /* Got lock */
        mutex_unlock(&lock);
    }
    
    // Check if locked
    if (mutex_is_locked(&lock))
        /* Someone holds it */

**Example:**

.. code-block:: c

    struct device_data {
        struct mutex lock;
        void *buffer;
        size_t size;
    };
    
    ssize_t device_read(struct file *file, char __user *buf,
                        size_t count, loff_t *ppos) {
        struct device_data *dev = file->private_data;
        
        if (mutex_lock_interruptible(&dev->lock))
            return -ERESTARTSYS;
        
        // Can call blocking functions safely
        if (copy_to_user(buf, dev->buffer, count)) {
            mutex_unlock(&dev->lock);
            return -EFAULT;
        }
        
        mutex_unlock(&dev->lock);
        return count;
    }

**Mutex vs Spinlock:**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Spinlock
     - Mutex
   * - **Wait type**
     - Busy-wait (CPU spins)
     - Sleep (blocks thread)
   * - **Can sleep in CS?**
     - ✗ No
     - ✓ Yes
   * - **IRQ context?**
     - ✓ Yes (with _irqsave)
     - ✗ No
   * - **Critical section**
     - Very short (µs)
     - Longer OK (ms)
   * - **Overhead**
     - Low (no scheduling)
     - Higher (context switch)
   * - **Best for**
     - Quick data access
     - I/O operations

3.4 RCU (Read-Copy-Update) - Read-Mostly Data
----------------------------------------------

**Characteristics:**

- Optimized for read-heavy workloads
- Readers have **zero overhead** (no locks!)
- Writers make copy, update atomically
- Wait for readers to finish before freeing old data
- Used extensively in kernel (networking, VFS)

**API:**

.. code-block:: c

    // Reader side
    rcu_read_lock();
    ptr = rcu_dereference(global_ptr);
    if (ptr)
        use_data(ptr);
    rcu_read_unlock();
    
    // Writer side (update pointer)
    new = kmalloc(sizeof(*new), GFP_KERNEL);
    *new = new_data;
    
    old = global_ptr;
    rcu_assign_pointer(global_ptr, new);  // Atomic update
    
    synchronize_rcu();  // Wait for all readers
    kfree(old);         // Now safe to free
    
    // Or use call_rcu for async free
    call_rcu(&old->rcu_head, free_callback);

**Example:**

.. code-block:: c

    struct config {
        int value;
        struct rcu_head rcu;
    };
    
    static struct config __rcu *global_config;
    
    // Reader (very fast, no locking!)
    int read_config(void) {
        struct config *cfg;
        int ret;
        
        rcu_read_lock();
        cfg = rcu_dereference(global_config);
        ret = cfg ? cfg->value : -1;
        rcu_read_unlock();
        
        return ret;
    }
    
    // Writer
    void update_config(int new_value) {
        struct config *new_cfg, *old_cfg;
        
        new_cfg = kmalloc(sizeof(*new_cfg), GFP_KERNEL);
        new_cfg->value = new_value;
        
        old_cfg = global_config;
        rcu_assign_pointer(global_config, new_cfg);
        
        synchronize_rcu();  // Wait for readers
        kfree(old_cfg);
    }

3.5 Seqlock - Readers Retry on Conflict
----------------------------------------

**Characteristics:**

- Readers can execute without blocking
- Writers get exclusive access
- Readers retry if data changed during read
- Good for small, frequently read data

**API:**

.. code-block:: c

    DEFINE_SEQLOCK(my_seqlock);
    
    // Reader
    unsigned seq;
    do {
        seq = read_seqbegin(&my_seqlock);
        /* Read data */
        value = shared_data;
    } while (read_seqretry(&my_seqlock, seq));
    
    // Writer
    write_seqlock(&my_seqlock);
    /* Update data */
    shared_data = new_value;
    write_sequnlock(&my_seqlock);
    
    // IRQ-safe
    write_seqlock_irqsave(&my_seqlock, flags);
    write_sequnlock_irqrestore(&my_seqlock, flags);

**Example:**

.. code-block:: c

    struct stats {
        seqlock_t lock;
        u64 packets;
        u64 bytes;
    };
    
    // Reader (fast, lock-free)
    void read_stats(struct stats *s, u64 *pkts, u64 *bytes) {
        unsigned seq;
        
        do {
            seq = read_seqbegin(&s->lock);
            *pkts = s->packets;
            *bytes = s->bytes;
        } while (read_seqretry(&s->lock, seq));
    }
    
    // Writer
    void update_stats(struct stats *s, u64 pkt_delta, u64 byte_delta) {
        write_seqlock(&s->lock);
        s->packets += pkt_delta;
        s->bytes += byte_delta;
        write_sequnlock(&s->lock);
    }

3.6 Atomic Operations
----------------------

**Characteristics:**

- Single instruction, indivisible
- No locks needed
- Very fast
- Limited operations

**API:**

.. code-block:: c

    atomic_t counter = ATOMIC_INIT(0);
    
    atomic_read(&counter);           // Read value
    atomic_set(&counter, 10);        // Set value
    atomic_inc(&counter);            // Increment
    atomic_dec(&counter);            // Decrement
    atomic_add(5, &counter);         // Add
    atomic_sub(3, &counter);         // Subtract
    
    // Test and return
    atomic_inc_and_test(&counter);   // Returns true if result is 0
    atomic_dec_and_test(&counter);   // Returns true if result is 0
    atomic_add_return(5, &counter);  // Returns new value
    
    // Compare and swap
    atomic_cmpxchg(&counter, old, new);  // Set new if equals old

**Bit Operations:**

.. code-block:: c

    unsigned long flags = 0;
    
    set_bit(0, &flags);              // Set bit 0
    clear_bit(1, &flags);            // Clear bit 1
    test_bit(2, &flags);             // Test bit 2
    test_and_set_bit(3, &flags);     // Test and set atomically
    test_and_clear_bit(4, &flags);   // Test and clear atomically

3.7 Lockdep - Lock Debugging
-----------------------------

**Characteristics:**

- Runtime lock validator (CONFIG_PROVE_LOCKING)
- Detects deadlocks, lock inversions
- Tracks lock ordering
- No runtime overhead when disabled

**Common Issues Detected:**

1. **Circular dependency** (A→B, B→A)
2. **IRQ inversion** (process takes lock, IRQ waits for it)
3. **Lock held too long**
4. **Incorrect nesting**

**Lockdep Annotations:**

.. code-block:: c

    // Inform lockdep about lock ordering
    mutex_lock_nested(&lock2, SINGLE_DEPTH_NESTING);
    
    // Disable lockdep check (rare)
    lockdep_off();
    /* Code */
    lockdep_on();

**Debugging:**

.. code-block:: bash

    # Enable lockdep
    echo 1 > /proc/sys/kernel/lock_stat
    
    # View lock statistics
    cat /proc/lock_stat

================================================================================

4. Comprehensive Exam Questions
================================================================================

Question 1: Threaded IRQ Design and Implementation (14 points)
---------------------------------------------------------------

You are developing a Linux driver for a high-speed UART device that receives data at 1 Mbps. The device generates an interrupt when the RX FIFO reaches 64 bytes.

**Part A (6 points):** Implement both the top-half and bottom-half handlers using the threaded IRQ mechanism. The bottom-half must copy data to user space and wake up waiting processes.

**Part B (4 points):** Explain why you chose ``IRQF_ONESHOT`` flag (or why not). What could happen if this flag is omitted for a level-triggered interrupt?

**Part C (4 points):** The system shows high interrupt latency. Describe three optimization techniques you would apply and their trade-offs.

**Answer:**

**Part A:**

.. code-block:: c

    struct uart_device {
        void __iomem *regs;
        int irq;
        struct mutex lock;
        wait_queue_head_t rx_wait;
        char rx_buffer[4096];
        size_t rx_count;
    };
    
    // Top-half: Quick check and acknowledgment
    static irqreturn_t uart_irq_handler(int irq, void *dev_id) {
        struct uart_device *uart = dev_id;
        u32 status = readl(uart->regs + UART_ISR);
        
        // Check if RX interrupt
        if (!(status & UART_ISR_RX))
            return IRQ_NONE;
        
        // Acknowledge interrupt at device level
        writel(UART_ISR_RX, uart->regs + UART_ISR);
        
        // Wake thread handler
        return IRQ_WAKE_THREAD;
    }
    
    // Bottom-half: Process data in thread context
    static irqreturn_t uart_irq_thread(int irq, void *dev_id) {
        struct uart_device *uart = dev_id;
        
        mutex_lock(&uart->lock);
        
        // Read FIFO (64 bytes available)
        while (readl(uart->regs + UART_LSR) & UART_LSR_DR) {
            if (uart->rx_count < sizeof(uart->rx_buffer)) {
                uart->rx_buffer[uart->rx_count++] = 
                    readl(uart->regs + UART_RBR);
            }
        }
        
        // Wake up waiting readers
        wake_up_interruptible(&uart->rx_wait);
        
        mutex_unlock(&uart->lock);
        
        return IRQ_HANDLED;
    }
    
    // Registration
    ret = request_threaded_irq(uart->irq,
                               uart_irq_handler,
                               uart_irq_thread,
                               IRQF_ONESHOT | IRQF_TRIGGER_HIGH,
                               "uart-device",
                               uart);

**Part B:**

``IRQF_ONESHOT`` is **essential** for level-triggered interrupts. It keeps the IRQ line disabled until the thread handler completes.

**Without IRQF_ONESHOT:**

1. Top-half acknowledges interrupt and returns
2. IRQ line is re-enabled immediately
3. If device still asserts IRQ (level-triggered), interrupt fires again
4. Results in IRQ storm - continuous interrupts before data is processed
5. System becomes unresponsive

**With IRQF_ONESHOT:**

1. Top-half runs, IRQ stays disabled
2. Thread handler processes data
3. IRQ re-enabled only after thread completes
4. Prevents interrupt storm

**Part C: Optimization Techniques:**

**1. IRQ Affinity to Isolated CPU:**

.. code-block:: bash

    # Isolate CPU 3 from scheduler
    isolcpus=3
    
    # Bind IRQ to CPU 3
    echo 8 > /proc/irq/45/smp_affinity  # 0x8 = CPU 3

*Trade-off:* Reduces interference but loses CPU for general work.

**2. Increase FIFO Threshold:**

.. code-block:: c

    // Trigger interrupt at 128 bytes instead of 64
    writel(UART_FCR_TRIGGER_128, uart->regs + UART_FCR);

*Trade-off:* Fewer interrupts but higher latency per character.

**3. Real-Time Thread Priority:**

.. code-block:: c

    // In probe function after request_threaded_irq
    struct task_struct *irq_thread;
    irq_thread = find_task_by_irq(uart->irq);
    sched_set_fifo(irq_thread);  // RT FIFO priority

*Trade-off:* Better latency but may starve other processes.

================================================================================

Question 2: Bottom-Half Mechanism Selection (12 points)
--------------------------------------------------------

You are implementing three different subsystems. For each scenario, select the most appropriate bottom-half mechanism and justify your choice.

**Scenario A:** Network packet processing - receives 10,000 packets/second, each packet requires 50µs of processing (checksum, parsing headers). Processing cannot sleep.

**Scenario B:** USB mass storage driver - receives completion interrupt for disk I/O. Must allocate bounce buffers, copy data to user space, and wake up blocked processes.

**Scenario C:** GPIO button driver - detects button press, must debounce (wait 20ms), then notify user space via sysfs attribute change.

**Answer:**

**Scenario A: Use NAPI + Softirq (NET_RX_SOFTIRQ)**

.. code-block:: c

    // Network drivers use NAPI framework (built on softirq)
    static irqreturn_t eth_irq_handler(int irq, void *dev_id) {
        struct net_device *ndev = dev_id;
        
        // Disable device interrupts
        eth_disable_irq(ndev);
        
        // Schedule NAPI poll (uses NET_RX_SOFTIRQ)
        napi_schedule(&ndev->napi);
        
        return IRQ_HANDLED;
    }
    
    static int eth_poll(struct napi_struct *napi, int budget) {
        int processed = 0;
        
        while (processed < budget && eth_has_rx(ndev)) {
            process_packet(ndev);
            processed++;
        }
        
        if (processed < budget) {
            napi_complete(napi);
            eth_enable_irq(ndev);  // Re-enable interrupts
        }
        
        return processed;
    }

**Justification:**

- **Softirq** provides lowest latency for high-frequency events
- **NAPI** batches processing (poll multiple packets per softirq)
- Cannot sleep → softirq/tasklet appropriate
- Network RX is **core subsystem** - softirq acceptable here
- Reduces interrupt overhead from 10,000/s to ~100/s

**Scenario B: Use Threaded IRQ**

.. code-block:: c

    static irqreturn_t usb_completion_handler(int irq, void *data) {
        struct usb_hcd *hcd = data;
        
        if (!usb_hcd_has_completed(hcd))
            return IRQ_NONE;
        
        return IRQ_WAKE_THREAD;
    }
    
    static irqreturn_t usb_completion_thread(int irq, void *data) {
        struct usb_hcd *hcd = data;
        struct urb *urb;
        
        // Process context - can sleep, allocate, copy to user
        urb = usb_hcd_get_completed(hcd);
        
        // Allocate bounce buffer
        void *bounce = kmalloc(urb->transfer_buffer_length, GFP_KERNEL);
        
        // Copy to user space
        copy_to_user(urb->transfer_buffer, bounce, urb->actual_length);
        
        // Wake blocked processes
        wake_up(&hcd->wait_queue);
        
        kfree(bounce);
        return IRQ_HANDLED;
    }

**Justification:**

- Must **sleep** (kmalloc, copy_to_user, wake_up)
- Mutex required for URB queue access
- **Threaded IRQ** provides process context automatically
- Per-IRQ thread - natural fit for USB controller
- Simpler than workqueue (automatic serialization)

**Scenario C: Use Delayed Workqueue**

.. code-block:: c

    struct button_dev {
        struct delayed_work debounce_work;
        struct gpio_desc *gpio;
        int last_state;
    };
    
    static void debounce_work_func(struct work_struct *work) {
        struct button_dev *btn = container_of(work,
                               struct button_dev, debounce_work.work);
        
        int state = gpiod_get_value(btn->gpio);
        
        if (state != btn->last_state) {
            btn->last_state = state;
            sysfs_notify(&btn->dev->kobj, NULL, "state");
        }
    }
    
    static irqreturn_t button_irq_handler(int irq, void *data) {
        struct button_dev *btn = data;
        
        // Schedule work after 20ms (debounce delay)
        schedule_delayed_work(&btn->debounce_work,
                            msecs_to_jiffies(20));
        
        return IRQ_HANDLED;
    }

**Justification:**

- Needs **delay** (20ms debounce) - cannot use softirq/tasklet
- **Delayed workqueue** provides built-in timer
- Can sleep for sysfs_notify()
- Low frequency (button presses) - no performance concern
- Simpler than hrtimer + separate work

================================================================================

Question 3: Spinlock vs Mutex Scenario Analysis (10 points)
------------------------------------------------------------

Given the following code with a **bug**:

.. code-block:: c

    struct device_stats {
        spinlock_t lock;
        unsigned long rx_packets;
        unsigned long tx_packets;
        void *log_buffer;
    };
    
    static irqreturn_t device_irq(int irq, void *data) {
        struct device_stats *stats = data;
        
        spin_lock(&stats->lock);
        stats->rx_packets++;
        
        // Allocate space for logging
        if (!stats->log_buffer) {
            stats->log_buffer = kmalloc(4096, GFP_KERNEL);
        }
        
        spin_unlock(&stats->lock);
        return IRQ_HANDLED;
    }
    
    void print_stats(struct device_stats *stats) {
        unsigned long flags;
        
        spin_lock_irqsave(&stats->lock, flags);
        printk("RX: %lu, TX: %lu\n", stats->rx_packets, stats->tx_packets);
        spin_unlock_irqrestore(&stats->lock, flags);
    }

**Part A (5 points):** Identify **all** bugs and explain why each is problematic.

**Part B (5 points):** Provide a corrected version using appropriate locking mechanisms.

**Answer:**

**Part A: Bugs Identified:**

**Bug 1:** ``kmalloc(GFP_KERNEL)`` while holding spinlock

- **Problem:** GFP_KERNEL can sleep if memory is low
- **Result:** "BUG: sleeping function called from invalid context"
- **Impact:** System deadlock or panic

**Bug 2:** ``spin_lock()`` in IRQ handler without ``_irqsave``

- **Problem:** If ``print_stats()`` holds lock, IRQ fires on same CPU → deadlock
- **Result:** IRQ handler spins forever waiting for lock it won't get
- **Impact:** System hang

**Bug 3:** Unnecessary allocation in IRQ path

- **Problem:** Memory allocation is slow operation (even with GFP_ATOMIC)
- **Impact:** Violates "fast IRQ handler" principle

**Part B: Corrected Version:**

.. code-block:: c

    struct device_stats {
        spinlock_t lock;
        unsigned long rx_packets;
        unsigned long tx_packets;
        void *log_buffer;  // Pre-allocated in probe()
    };
    
    // Fix 1: Pre-allocate buffer during device initialization
    int device_probe(struct platform_device *pdev) {
        struct device_stats *stats;
        
        stats = devm_kzalloc(&pdev->dev, sizeof(*stats), GFP_KERNEL);
        spin_lock_init(&stats->lock);
        
        // Pre-allocate log buffer
        stats->log_buffer = devm_kzalloc(&pdev->dev, 4096, GFP_KERNEL);
        if (!stats->log_buffer)
            return -ENOMEM;
        
        // Register IRQ, etc.
        return 0;
    }
    
    // Fix 2: Use spin_lock() in IRQ (already in IRQ context)
    static irqreturn_t device_irq(int irq, void *data) {
        struct device_stats *stats = data;
        
        spin_lock(&stats->lock);  // OK: already in IRQ context
        stats->rx_packets++;
        spin_unlock(&stats->lock);
        
        return IRQ_HANDLED;
    }
    
    // Fix 3: Keep spin_lock_irqsave in process context
    void print_stats(struct device_stats *stats) {
        unsigned long flags, rx, tx;
        
        spin_lock_irqsave(&stats->lock, flags);
        rx = stats->rx_packets;
        tx = stats->tx_packets;
        spin_unlock_irqrestore(&stats->lock, flags);
        
        // Print outside lock (slow operation)
        printk("RX: %lu, TX: %lu\n", rx, tx);
    }

**Alternative: Atomic Counters (Better Solution):**

.. code-block:: c

    struct device_stats {
        atomic_long_t rx_packets;
        atomic_long_t tx_packets;
        void *log_buffer;
    };
    
    static irqreturn_t device_irq(int irq, void *data) {
        struct device_stats *stats = data;
        
        atomic_long_inc(&stats->rx_packets);  // No lock needed!
        
        return IRQ_HANDLED;
    }
    
    void print_stats(struct device_stats *stats) {
        unsigned long rx = atomic_long_read(&stats->rx_packets);
        unsigned long tx = atomic_long_read(&stats->tx_packets);
        
        printk("RX: %lu, TX: %lu\n", rx, tx);
    }

================================================================================

Question 4: RCU Read-Mostly Optimization (12 points)
-----------------------------------------------------

You have a global configuration structure that is read frequently (10,000 times/second) but updated rarely (once per minute). Current implementation uses mutex:

.. code-block:: c

    struct config {
        int threshold;
        int timeout_ms;
        bool enabled;
    };
    
    static struct config *global_config;
    static DEFINE_MUTEX(config_lock);
    
    // Reader (called frequently from softirq)
    int check_threshold(int value) {
        int ret;
        
        mutex_lock(&config_lock);  // BUG: can't sleep in softirq!
        ret = value > global_config->threshold;
        mutex_unlock(&config_lock);
        
        return ret;
    }
    
    // Writer (called from sysfs store)
    void update_config(int threshold, int timeout, bool enabled) {
        mutex_lock(&config_lock);
        global_config->threshold = threshold;
        global_config->timeout_ms = timeout;
        global_config->enabled = enabled;
        mutex_unlock(&config_lock);
    }

**Part A (7 points):** Convert this to RCU-protected access. Show both reader and writer implementations.

**Part B (5 points):** Explain the performance benefit and memory overhead trade-off.

**Answer:**

**Part A: RCU Implementation:**

.. code-block:: c

    struct config {
        int threshold;
        int timeout_ms;
        bool enabled;
        struct rcu_head rcu;
    };
    
    static struct config __rcu *global_config;
    
    // Initialization (in module_init)
    static int __init config_init(void) {
        struct config *cfg;
        
        cfg = kzalloc(sizeof(*cfg), GFP_KERNEL);
        cfg->threshold = 100;
        cfg->timeout_ms = 1000;
        cfg->enabled = true;
        
        rcu_assign_pointer(global_config, cfg);
        return 0;
    }
    
    // Reader (softirq-safe, lock-free!)
    int check_threshold(int value) {
        struct config *cfg;
        int ret;
        
        rcu_read_lock();  // Very fast, no atomic ops
        cfg = rcu_dereference(global_config);
        ret = cfg && value > cfg->threshold;
        rcu_read_unlock();
        
        return ret;
    }
    
    // Free callback for RCU
    static void config_free_rcu(struct rcu_head *rcu) {
        struct config *cfg = container_of(rcu, struct config, rcu);
        kfree(cfg);
    }
    
    // Writer (allocate new, swap pointer, free old after grace period)
    void update_config(int threshold, int timeout, bool enabled) {
        struct config *new_cfg, *old_cfg;
        
        // Allocate new configuration
        new_cfg = kzalloc(sizeof(*new_cfg), GFP_KERNEL);
        if (!new_cfg)
            return;
        
        new_cfg->threshold = threshold;
        new_cfg->timeout_ms = timeout;
        new_cfg->enabled = enabled;
        
        // Atomic pointer update
        old_cfg = rcu_dereference_protected(global_config,
                                          lockdep_is_held(&config_lock));
        rcu_assign_pointer(global_config, new_cfg);
        
        // Free old config after grace period (when all readers done)
        if (old_cfg)
            call_rcu(&old_cfg->rcu, config_free_rcu);
    }

**Part B: Performance Analysis:**

**Performance Benefit:**

1. **Reader Performance:**
   - **Before (mutex):** ~50-100 CPU cycles (lock/unlock + cache ping-pong)
   - **After (RCU):** ~5-10 CPU cycles (memory barrier only)
   - **10x-20x faster** for read path
   - 10,000 reads/sec × 90 cycles saved = **900,000 cycles/sec saved**

2. **Scalability:**
   - Mutex: Serializes all readers → cache line bouncing
   - RCU: Readers run in parallel, no cache conflicts
   - Scales linearly with CPU count

3. **No Lock Contention:**
   - Readers never block each other or writer
   - Critical for softirq context (can't sleep)

**Memory Overhead:**

1. **Extra Memory:**
   - Old config exists until grace period ends
   - Typically 2 copies during update (old + new)
   - For small struct (12 bytes + rcu_head), negligible

2. **Grace Period Wait:**
   - ``call_rcu()`` defers free (asynchronous)
   - Multiple rapid updates can accumulate old copies
   - Can use ``synchronize_rcu()`` if memory-constrained (blocks writer)

**Trade-off Summary:**

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Aspect
     - Mutex
     - RCU
   * - **Read overhead**
     - High (50-100 cycles)
     - Very low (5-10 cycles)
   * - **Scalability**
     - Poor (serialized)
     - Excellent (parallel)
   * - **Write overhead**
     - Low (update in place)
     - Higher (allocate + free)
   * - **Memory**
     - Single copy
     - 2 copies during update
   * - **Complexity**
     - Simple
     - Moderate (grace periods)

**Conclusion:** RCU is ideal for this 10,000:1 read:write ratio.

================================================================================

Question 5: Interrupt Latency Debugging (10 points)
----------------------------------------------------

A real-time audio application is experiencing audio glitches (buffer underruns). You suspect high interrupt latency for the audio DMA completion IRQ (IRQ 67).

**Part A (6 points):** Describe the step-by-step methodology to measure and identify the source of latency.

**Part B (4 points):** The investigation reveals IRQ 67 waits an average of 2ms for IRQ 45 (network) to complete. Propose a solution.

**Answer:**

**Part A: Latency Measurement Methodology:**

**Step 1: Verify IRQ Statistics**

.. code-block:: bash

    # Check if IRQ 67 is firing
    watch -n 0.1 'cat /proc/interrupts | grep " 67:"'
    
    # Look for:
    # - IRQ firing regularly (every ~10ms for audio)
    # - Balanced across CPUs (or bound correctly)
    # - No excessive count (IRQ storm)

**Step 2: Measure Interrupt Latency with cyclictest**

.. code-block:: bash

    # Install rt-tests package
    sudo apt-get install rt-tests
    
    # Run cyclictest (measures IRQ response time)
    sudo cyclictest -m -n -p 95 -h 200 -l 100000
    
    # Options:
    # -m: lock memory
    # -n: use clock_nanosleep
    # -p 95: RT priority 95
    # -h 200: histogram with 200µs max
    # -l 100000: 100k iterations
    
    # Expected output shows latency histogram:
    # T: 0 ( 1234) P:95 I:1000 C: 100000 Min:   5 Act:   8 Avg:  10 Max:  2050

**Step 3: Trace Interrupt Handling with ftrace**

.. code-block:: bash

    cd /sys/kernel/debug/tracing
    
    # Enable IRQ tracing
    echo 1 > events/irq/irq_handler_entry/enable
    echo 1 > events/irq/irq_handler_exit/enable
    
    # Enable function graph tracer
    echo function_graph > current_tracer
    
    # Set filter for our IRQ
    echo 67 > events/irq/irq_handler_entry/filter
    
    # Record trace
    echo 1 > tracing_on
    sleep 5
    echo 0 > tracing_on
    
    # Analyze trace
    cat trace | grep "irq 67" -A 10

**Step 4: Check IRQ Affinity and Isolation**

.. code-block:: bash

    # Check which CPUs handle IRQ 67
    cat /proc/irq/67/smp_affinity_list
    
    # Check if CPUs are isolated
    cat /proc/cmdline | grep isolcpus
    
    # Check for IRQ affinity conflicts
    for i in /proc/irq/*/smp_affinity_list; do
        echo "$i: $(cat $i)"
    done

**Step 5: Profile with perf**

.. code-block:: bash

    # Record IRQ events
    sudo perf record -e irq:irq_handler_entry -e irq:irq_handler_exit \\
                     -a -g sleep 10
    
    # Analyze
    sudo perf report
    
    # Look for:
    # - Long IRQ handler execution times
    # - IRQs blocked by other handlers
    # - Softirq processing delays

**Step 6: Check for IRQ Storms**

.. code-block:: bash

    # Monitor IRQ rate
    watch -n 0.1 'cat /proc/interrupts | head -20'
    
    # If any IRQ shows 100k+ increments per second → storm

**Part B: Solution for IRQ Priority Inversion**

**Problem Analysis:**

- IRQ 67 (audio) disabled while IRQ 45 (network) handler runs
- Network handler takes 2ms (too long!)
- Audio requires < 500µs latency for 48kHz/128-sample buffer

**Solution 1: Move Network to Threaded IRQ**

.. code-block:: c

    // Network driver modification
    // Before: request_irq(irq, net_handler, 0, "eth0", dev);
    
    // After: Use threaded IRQ
    static irqreturn_t net_quick_check(int irq, void *data) {
        struct net_device *ndev = data;
        
        // Just check and ack (< 10µs)
        if (!(readl(ndev->regs + STATUS) & RX_READY))
            return IRQ_NONE;
        
        writel(STATUS_ACK, ndev->regs + STATUS);
        return IRQ_WAKE_THREAD;
    }
    
    static irqreturn_t net_process_packets(int irq, void *data) {
        struct net_device *ndev = data;
        
        // Process packets in thread (can take 2ms)
        while (has_packets(ndev))
            process_packet(ndev);
        
        return IRQ_HANDLED;
    }
    
    request_threaded_irq(ndev->irq, net_quick_check, net_process_packets,
                        IRQF_ONESHOT, "eth0", ndev);

**Solution 2: IRQ Affinity Isolation**

.. code-block:: bash

    # Isolate CPU 3 for audio (kernel command line)
    isolcpus=3 nohz_full=3 rcu_nocbs=3
    
    # Bind audio IRQ to isolated CPU 3
    echo 3 > /proc/irq/67/smp_affinity_list
    
    # Bind network IRQs to CPUs 0-2
    echo 0-2 > /proc/irq/45/smp_affinity_list
    
    # Bind audio process to CPU 3
    taskset -c 3 audio_application

**Solution 3: IRQ Threading (Kernel Parameter)**

.. code-block:: bash

    # Force all IRQs to threaded mode (except marked IRQF_NO_THREAD)
    threadirqs
    
    # Then set audio IRQ thread to real-time priority
    ps aux | grep "irq/67"  # Find PID
    chrt -f -p 90 <PID>     # Set SCHED_FIFO priority 90

**Expected Results:**

- Network top-half: < 50µs (doesn't block audio)
- Audio IRQ latency: < 100µs (acceptable)
- Audio glitches eliminated

================================================================================

5. Debugging and Monitoring
================================================================================

5.1 Essential Monitoring Commands
----------------------------------

**View Interrupt Statistics:**

.. code-block:: bash

    # Per-CPU interrupt counts
    cat /proc/interrupts
    #            CPU0       CPU1       CPU2       CPU3
    #   0:        100        110        105        108   IO-APIC-edge      timer
    #  45:      50000      50100      49980      50020   PCI-MSI-edge      eth0
    #  67:       1000       1005        998       1002   PCI-MSI-edge      snd_hda
    
    # Watch in real-time
    watch -n 1 'cat /proc/interrupts | head -20'
    
    # Find IRQ number for device
    grep eth0 /proc/interrupts

**View Softirq Statistics:**

.. code-block:: bash

    cat /proc/softirqs
    #                CPU0       CPU1       CPU2       CPU3
    #      HI:          0          0          0          0
    #   TIMER:     123456     123500     123480     123520
    #  NET_TX:      45000      45100      44950      45050
    #  NET_RX:     890000     891000     889500     890500
    # TASKLET:       5000       5010       4998       5002

**Check IRQ Affinity:**

.. code-block:: bash

    # View affinity mask (hex)
    cat /proc/irq/45/smp_affinity
    # Output: f (binary 1111 = all 4 CPUs)
    
    # View affinity list (human-readable)
    cat /proc/irq/45/smp_affinity_list
    # Output: 0-3
    
    # Set affinity to CPU 2 only
    echo 2 > /proc/irq/45/smp_affinity_list
    
    # Set affinity to CPUs 0 and 2
    echo 0,2 > /proc/irq/45/smp_affinity_list

**Monitor Threaded IRQs:**

.. code-block:: bash

    # List all IRQ threads
    ps aux | grep "irq/"
    # root     123  ... [irq/45-eth0]
    # root     456  ... [irq/67-snd_hda]
    
    # Check thread priority
    chrt -p 123
    # pid 123's current scheduling policy: SCHED_FIFO
    # pid 123's current scheduling priority: 50
    
    # Monitor thread CPU usage
    top -H -p 123

**Monitor Workqueues:**

.. code-block:: bash

    # List kworker threads
    ps aux | grep kworker
    # root     789  ... [kworker/0:1]
    # root     790  ... [kworker/1:2]
    
    # Monitor workqueue activity
    cat /proc/pressure/io

5.2 Ftrace - Interrupt Tracing
-------------------------------

.. code-block:: bash

    cd /sys/kernel/debug/tracing
    
    # Enable IRQ events
    echo 1 > events/irq/irq_handler_entry/enable
    echo 1 > events/irq/irq_handler_exit/enable
    echo 1 > events/irq/softirq_entry/enable
    echo 1 > events/irq/softirq_exit/enable
    
    # Start tracing
    echo 1 > tracing_on
    sleep 5
    echo 0 > tracing_on
    
    # View trace
    cat trace
    
    # Example output:
    #   irq/67-snd-123   [002] d... 1234.567890: irq_handler_entry: irq=67 name=snd_hda
    #   irq/67-snd-123   [002] d... 1234.567920: irq_handler_exit: irq=67 ret=handled
    
    # Cleanup
    echo 0 > events/irq/irq_handler_entry/enable
    echo 0 > events/irq/softirq_entry/enable

**Function Graph Tracer (Detailed IRQ Path):**

.. code-block:: bash

    # Set function graph tracer
    echo function_graph > current_tracer
    
    # Set filter for specific IRQ
    echo do_IRQ > set_ftrace_filter
    
    # Record and view
    echo 1 > tracing_on
    sleep 2
    echo 0 > tracing_on
    cat trace | less

5.3 Perf - Performance Analysis
--------------------------------

.. code-block:: bash

    # Record IRQ events for 10 seconds
    sudo perf record -e irq:irq_handler_entry -e irq:irq_handler_exit \\
                     -a -g sleep 10
    
    # Analyze report
    sudo perf report
    
    # Record all events including softirqs
    sudo perf record -e 'irq:*' -a -g sleep 10
    
    # Live monitoring
    sudo perf top -e irq:irq_handler_entry
    
    # Measure IRQ latency
    sudo perf probe --add 'irq_handler_entry'
    sudo perf probe --add 'irq_handler_exit'
    sudo perf record -e probe:irq_handler_entry -e probe:irq_handler_exit -a
    sudo perf script

5.4 Common Issues and Solutions
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Issue
     - Symptoms
     - Solution
   * - **IRQ Storm**
     - IRQ count rapidly increasing, 100% CPU
     - Check device status, disable IRQ, fix handler to return IRQ_NONE
   * - **High Latency**
     - Audio glitches, missed deadlines
     - Use threaded IRQ, IRQ affinity, RT priority
   * - **Handler Not Called**
     - Device not responding
     - Check /proc/interrupts, verify IRQ number, check dmesg
   * - **Sleeping in Atomic**
     - BUG: sleeping function
     - Use threaded IRQ or workqueue for blocking ops
   * - **Deadlock**
     - System hang
     - Check lockdep, use spin_lock_irqsave correctly
   * - **Shared IRQ Conflict**
     - Spurious interrupts
     - Return IRQ_NONE if not your interrupt

5.5 Lockdep Debugging
----------------------

.. code-block:: bash

    # Enable lockdep (kernel config)
    CONFIG_PROVE_LOCKING=y
    CONFIG_LOCK_STAT=y
    
    # Runtime enable
    echo 1 > /proc/sys/kernel/lock_stat
    
    # View lock statistics
    cat /proc/lock_stat
    
    # Example deadlock in dmesg:
    # ======================================================
    # WARNING: possible circular locking dependency detected
    # ======================================================
    # swapper/0/1 is trying to acquire lock:
    # (&dev->lock){+.+.}, at: device_handler+0x20/0x40
    # but task is already holding lock:
    # (&port->lock){+.+.}, at: port_handler+0x15/0x35

================================================================================

6. Quick Reference Checklist
================================================================================

**Before Writing an Interrupt Handler:**

.. code-block:: text

    ☐ Device is properly initialized (clocks, resets, power)
    ☐ IRQ number obtained (platform_get_irq or DT parsing)
    ☐ Chosen appropriate mechanism:
      ☐ Simple + fast → request_irq + tasklet/workqueue
      ☐ Blocking work → request_threaded_irq (preferred 2026)
      ☐ Network → NAPI framework
    ☐ Top-half is FAST (< 100µs target)
    ☐ No sleeping functions in top-half
    ☐ No GFP_KERNEL allocations in top-half
    ☐ Return IRQ_NONE if not your interrupt (shared IRQ)
    ☐ Properly clear interrupt at device level
    ☐ Use appropriate IRQ flags:
      ☐ IRQF_SHARED if sharing IRQ line
      ☐ IRQF_ONESHOT for level-triggered interrupts
      ☐ IRQF_TRIGGER_* matching hardware

**Locking Checklist:**

.. code-block:: text

    ☐ Identified all shared data
    ☐ Chosen appropriate lock:
      ☐ Spinlock for short CS, IRQ context
      ☐ Mutex for longer CS, process context only
      ☐ RCU for read-mostly data
      ☐ Atomic ops for simple counters
    ☐ Used spin_lock_irqsave when locking from both IRQ and process
    ☐ Kept critical sections SHORT
    ☐ No nested locks (or documented lock ordering)
    ☐ Tested with lockdep enabled (CONFIG_PROVE_LOCKING)

**Performance Tuning Checklist:**

.. code-block:: text

    ☐ Measured baseline latency (cyclictest, perf)
    ☐ Checked IRQ affinity (/proc/irq/N/smp_affinity_list)
    ☐ Considered CPU isolation for real-time IRQs
    ☐ Verified no IRQ storms (watch /proc/interrupts)
    ☐ Profiled IRQ handler duration (ftrace, perf)
    ☐ Minimized work in top-half
    ☐ Used threaded IRQ for blocking operations
    ☐ Tested under load (stress-ng, network traffic)

================================================================================

7. Key Takeaways
================================================================================

**Modern Best Practices (2026):**

1. **Prefer Threaded IRQs for New Drivers**

   - Use ``request_threaded_irq()`` by default
   - Top-half: < 100µs, just check and ack
   - Bottom-half: can sleep, allocate, block
   - Automatic per-IRQ serialization

2. **Avoid Tasklets in New Code**

   - Legacy mechanism, being phased out
   - Migrate to workqueue BH (``system_bh_wq``)
   - Or use threaded IRQ

3. **Never Add New Softirqs**

   - Only 32 slots, 10 already used
   - For core kernel subsystems only
   - Upstream maintainers reject new softirqs

4. **Use Workqueues for Flexible Deferred Work**

   - ``schedule_work()`` for general use
   - ``schedule_delayed_work()`` for timed work
   - ``queue_work()`` on custom queues for isolation

5. **Lock Correctly**

   - IRQ context → spinlock only
   - Process context (can sleep) → mutex preferred
   - IRQ + process → ``spin_lock_irqsave``
   - Read-mostly → RCU (10x-20x faster reads)

6. **Measure Before Optimizing**

   - Use ``cyclictest`` for latency
   - Use ``perf`` for profiling
   - Use ``ftrace`` for detailed tracing
   - Monitor ``/proc/interrupts`` and ``/proc/softirqs``

7. **Think About Real-Time**

   - IRQ affinity (bind to specific CPUs)
   - CPU isolation (``isolcpus`` kernel parameter)
   - RT thread priorities (``chrt``)
   - Threaded IRQs (``threadirqs`` kernel parameter)

**Common Mistakes to Avoid:**

.. code-block:: text

    ✗ Sleeping in IRQ context (use threaded IRQ)
    ✗ GFP_KERNEL allocation in spinlock (use GFP_ATOMIC or pre-allocate)
    ✗ Long IRQ handlers (> 100µs) (defer to bottom-half)
    ✗ spin_lock() when sharing with IRQ (use spin_lock_irqsave)
    ✗ Mutex in IRQ context (use spinlock or threaded IRQ)
    ✗ Not returning IRQ_NONE for shared IRQs (causes IRQ storm)
    ✗ Forgetting IRQF_ONESHOT for level-triggered (causes IRQ storm)

**Architecture Highlights:**

.. code-block:: text

    Hardware Event → Interrupt Controller (APIC/GIC)
                  → CPU Core (vector lookup)
                  → Generic IRQ Layer (descriptor, action chain)
                  → Driver Handler (top-half, FAST)
                  → Bottom-Half Scheduling
                  → Deferred Execution (softirq/tasklet/workqueue/thread)

**Quick Command Reference:**

.. code-block:: bash

    # Monitor interrupts
    cat /proc/interrupts
    cat /proc/softirqs
    
    # IRQ affinity
    cat /proc/irq/N/smp_affinity_list
    echo 0-2 > /proc/irq/N/smp_affinity_list
    
    # Threaded IRQs
    ps aux | grep "irq/"
    chrt -p <PID>
    
    # Trace with ftrace
    cd /sys/kernel/debug/tracing
    echo 1 > events/irq/irq_handler_entry/enable
    cat trace
    
    # Profile with perf
    perf record -e irq:* -a -g sleep 10
    perf report
    
    # Measure latency
    cyclictest -m -n -p 95 -l 100000

**Final Wisdom:**

    "In interrupt context, be fast. For everything else, there's threaded IRQ."
    
    "Lock only what you must, and for as briefly as possible."
    
    "RCU: Read fast, write rarely, sleep safely."

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================
