
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for Linux Interrupt Handling** (kernel ~6.12 / early 2026 era)

### 0. Interrupt Fundamentals

**What is an Interrupt?**
An asynchronous signal that temporarily suspends normal program execution and transfers control to an interrupt handler. Used for event-driven hardware communication (I/O, timers, etc.).

**Hardware Interrupt Types:**

- **External Interrupts** (Hardware IRQs): From I/O devices via IRQ lines (PIC) or MSI/MSI-X (modern)
- **Software Interrupts** (Exceptions): CPU generates internally (div-by-zero, page fault, syscall)
- **Interprocessor Interrupts (IPI)**: CPU-to-CPU signaling for SMP systems
- **NMI (Non-Maskable Interrupt)**: Highest priority, cannot be disabled (watchdog, crash dump)

**Interrupt Controller Architecture:**

- **x86/x64**: APIC (Advanced PIC) + IO-APIC + LAPIC (Local APIC) per CPU
- **ARM**: GIC (Generic Interrupt Controller) with redistributor per CPU
- **RISC-V**: PLIC (Platform-Level Interrupt Controller)
- **Legacy**: 8259 PIC (rarely used now)

⭐ **Critical Constraints in Interrupt Context:**

- No sleeping (no ``mutex_lock()``, ``msleep()``, I/O wait, user memory copy)
- Limited stack (8 KB typical on x86-64, IRQ stack separate)
- Cannot call blocking functions or schedule()
- Must be fast (other interrupts delayed while handler runs)
- Preemption disabled on that CPU
- Use atomic operations for shared data

### 1. Basic Flow of Interrupt Handling (Detailed)

```
Hardware event (GPIO, timer, network packet, etc.)
    ↓
IRQ Signal Delivery:
├── PCI/PCIe MSI/MSI-X → Direct to LAPIC (modern, preferred)
├── Legacy IRQ line → IO-APIC → LAPIC
└── IPI → Direct to target LAPIC(s)
    ↓
CPU Interrupt Delivery:
├── Check IF (Interrupt Flag) in EFLAGS/PSTATE
├── If enabled and priority sufficient → enter interrupt mode
└── Save context (return address, flags, registers) to stack
    ↓
Vector Lookup (0–255 on x86):
├── Entry point in IDT (Interrupt Descriptor Table)
└── May trigger IOAPIC EOI / ACK hardware
    ↓
CPU Enters Privileged Mode (if not already):
├── Load kernel stack
├── Disable lower-priority interrupts (on some archs)
└── Prevent preemption on this CPU
    ↓
arch-specific asm entry point (e.g., ``common_interrupt`` on x86):
└── Save registers, switch to kernel stack
    ↓
generic_handle_irq() [arch-agnostic]
    ├── Look up irq_desc via irq_to_desc()
    └── Call handle_irq_event()
    ↓
irqaction chain traversal:
├── Usually first handler only (dedicated IRQ line)
└── Or multiple handlers (shared IRQ on legacy systems)
    ↓
Top-half Handler executes (irqaction.handler):
├── **Must be atomic** (no sleep, no blocking)
├── Ack/disable device IRQ if needed
├── Read minimal status/data
├── Decide if bottom-half needed
└── Return IRQ_HANDLED, IRQ_WAKE_THREAD, or IRQ_NONE
    ↓
Bottom-half execution (if deferred):
├── Softirq: Raised immediately, runs when CPU does softirq processing
├── Tasklet: Scheduled in softirq queue, runs when processing
├── Workqueue: Enqueued to kworker thread, runs when scheduled
└── Threaded IRQ: Wakes dedicated irq thread, runs in process context
    ↓
Return from Interrupt (IRET/RFE):
├── Restore context from stack
├── Restore IF flag (re-enable interrupts if appropriate)
├── Return to interrupted code
└── Kernel checks if reschedule needed (preemption)
```

### 2. Top-half vs Bottom-half (Comprehensive Comparison)

| Aspect                  | Top-half (Primary IRQ handler)          | Bottom-half (Deferred)                     |
|-------------------------|------------------------------------------|--------------------------------------------|
| Execution context       | **Interrupt context** (atomic)           | Interrupt or Process context               |
| Can sleep?              | **Never**                                | Depends (softirq/tasklet → no, workqueue → yes) |
| Can allocate memory?    | **No** (GFP_ATOMIC only, risky)          | Yes (in workqueue/threaded IRQ)            |
| Preemptible?            | **No** (preemption disabled)             | Softirq/tasklet → no, workqueue → yes      |
| Reentrant on same CPU?  | Usually not (depends on IRQ flags)       | Softirq → yes (different types), tasklet → no |
| Latency                 | **Must be very fast** (<1ms typical)     | Can be slower (ms to seconds)               |
| Typical work            | Ack IRQ, read status, disable device IRQ if needed, schedule bottom-half | Process data, copy to user, kick state machines, call fs/block/net code |
| Stack constraints       | Limited (8KB on x86-64)                  | Full kernel stack available                |
| Example operations      | ``readl(mmio_reg)``, ``spin_lock()``, set flag | ``mutex_lock()``, ``kmalloc(GFP_KERNEL)``, ``copy_to_user()`` |

### 3. Interrupt Handling Flags and Properties

**IRQ Line Attributes (stored in irq_desc):**

- **IRQ_LEVEL_TRIGGER**: Level-triggered (signal stays active until serviced)
- **IRQ_EDGE_TRIGGER**: Edge-triggered (signal pulse, must not miss it)
- **IRQF_TRIGGER_HIGH/LOW/RISING/FALLING**: Specify trigger type
- **IRQF_ONESHOT**: Keep IRQ disabled during threaded handler execution (level-triggered safety)
- **IRQF_SHARED**: Multiple handlers on same IRQ line (legacy PCI, rare now)
- **IRQF_NO_SUSPEND**: Handler must run during suspend (watchdog, power button)
- **IRQF_NO_THREAD**: Cannot be converted to threaded IRQ

**Return Values from Top-half Handler:**

- **IRQ_HANDLED**: Handler dealt with interrupt (consume it)
- **IRQ_NONE**: Not our interrupt (share line scenario)
- **IRQ_WAKE_THREAD**: (Threaded IRQ only) Activate bottom-half thread
- **IRQ_RETVAL(x)**: Macro to return IRQ_HANDLED iff x != 0

### 4. Main Bottom-Half Mechanisms – Modern Recommendation (2025–2026)

| Mechanism              | Context               | Can sleep / Alloc mem | Concurrency (same instance) | Priority / Latency | Allocation    | Modern status & 🟢 🟢 Best Practice (2025+)                  |
|------------------------|-----------------------|-----------------------|------------------------------|--------------------|---------------|--------------------------------------------------------|
| **Softirq**            | Interrupt             | ✗                     | Multiple per CPU OK          | Highest            | Static (32)   | **Only for core subsystems** (NET_RX/TX, RCU, TIMER, BLOCK, SCHED, HRTIMER) – **🔴 🔴 avoid new ones** |
| **Tasklet**            | Interrupt             | ✗                     | **Serialized** (1 CPU only)  | High               | Dynamic       | **Legacy** – being replaced by **workqueue BH** or threaded IRQ |
| **Workqueue (system/unbound)** | Process (kworker threads) | ✓                     | Multiple CPUs OK             | Medium             | Dynamic       | **Most common choice for new code** – flexible & safe |
| **Workqueue BH context** | Interrupt (special)   | ✗                     | Serialized                   | High               | Dynamic       | **Modern tasklet replacement** (queue_work_on/system_bh_wq) |
| **Threaded IRQ**       | Process (dedicated IRQ thread) | ✓                     | Per-IRQ thread               | Medium             | Dynamic       | **Strongly preferred** for **new drivers** (request_threaded_irq) |
| **Timer / hrtimer**    | Softirq context       | ✗                     | —                            | High / Very high   | Dynamic       | For time-based deferred work                           |

**Decision Tree – What to use in 2026?**

```
Need to defer work from IRQ handler?

⭐ ├── **Extremely performance/latency critical** (high-freq, core subsys)?
│   └── → **Softirq** (very rare for new code – upstream hates new ones)
│
├── **Cannot sleep, no memory allocation, no blocking calls**?
│   ├── Simple & want automatic serialization → **Tasklet** (still ok, but legacy)
│   └── Want modern replacement → **Workqueue in BH context**
│
└── **Can sleep / allocate / call blocking functions / take mutex**?
    ├── Want simplest & most modern → **Threaded IRQ** (request_threaded_irq)
    └── Want flexible queuing, priorities, delayed execution → **Workqueue** (system_wq / delayed_work / create_workqueue)

Bottom line 2025–2026:
New drivers → **Threaded IRQ** or **Workqueue**
Maintenance/old code → Tasklet → plan migration to workqueue BH
Only very special cases → new softirq
```

### 5. Detailed API Reference

**request_irq() – Simple Handler Registration (Legacy)**

```c
int request_irq(unsigned int irq, irq_handler_t handler,
                unsigned long flags, const char *name, void *dev);
```

- Simple but all work in interrupt context
- Returns 0 on success, error code otherwise
- Call ``free_irq(irq, dev)`` to cleanup
- Example: ``request_irq(platform_irq, my_handler, IRQF_SHARED, "mydev", dev)``

**request_threaded_irq() – Modern 🟢 🟢 Best Practice**

```c
int request_threaded_irq(unsigned int irq,
                         irq_handler_t handler,
                         irq_handler_t thread_fn,
                         unsigned long flags,
                         const char *name,
                         void *dev);
```

- ``handler``: Quick top-half (can return ``IRQ_WAKE_THREAD``)
- ``thread_fn``: Bottom-half runs in dedicated kernel thread (can sleep)
- ``IRQF_ONESHOT``: Keep IRQ disabled during thread execution (level-triggered safety)
- Returns 0 on success, error code otherwise
- Call ``free_irq(irq, dev)`` to cleanup
- Example: ``request_threaded_irq(irq, quick_check, process_data, IRQF_ONESHOT, "uart", dev)``

**Shared IRQ Registration**

```c
// For multiple handlers on same IRQ (legacy PCI, rare)
int request_irq(irq, handler1, IRQF_SHARED, "dev1", dev1);
int request_irq(irq, handler2, IRQF_SHARED, "dev2", dev2);  // Same IRQ

// Each handler MUST return IRQ_NONE if not its interrupt
// Kernel tries all handlers until one returns IRQ_HANDLED
```

**Disabling/Enabling IRQs from Driver**

```c
// At IRQ controller level (entire IRQ line)
disable_irq(irq);      // Also waits for in-flight handlers (blocking)
enable_irq(irq);       // Re-enable

disable_irq_nosync(irq);  // 🔴 🔴 Don't wait (use in interrupt context)

// Disable all IRQs (entire system – 🔴 🔴 AVOID!)
local_irq_save(flags);
⭐ // ... critical section ...
local_irq_restore(flags);

// Disable IRQ on local CPU
local_irq_disable();
local_irq_enable();
```

**Setting IRQ Affinity (CPU binding)**

```c
// From userspace
echo "0x1" > /proc/irq/NNN/smp_affinity        # Bind IRQ NNN to CPU 0
cat /proc/irq/NNN/smp_affinity_list            # View affinity

// From kernel
irq_set_affinity(irq, cpumask);
```

### 6. Quick Code Patterns (most used in modern kernels)

```c
// 1. Modern 🟢 🟢 best practice – Threaded IRQ (STRONGLY PREFERRED)
static irqreturn_t my_irq_top(int irq, void *dev_id) {
🔧     struct my_device *dev = dev_id;
    
    // Very quick: check if our interrupt, ack hardware
    if (!(readl(dev->reg_status) & DEVICE_READY))
⚙️         return IRQ_NONE;  // Not our interrupt (shared line scenario)
    
    // Clear interrupt flag on device
🔧     writel(DEVICE_IRQ_CLR, dev->reg_ctrl);
    
    // Return to wake thread handler
    return IRQ_WAKE_THREAD;
}

static irqreturn_t my_irq_thread(int irq, void *dev_id) {
🔧     struct my_device *dev = dev_id;
    
    // All the real work here – can sleep, allocate, call blocking functions
    mutex_lock(&dev->lock);
    process_device_data(dev);
    copy_to_user(dev->user_buf, dev->kernel_buf, count);
    mutex_unlock(&dev->lock);
    
    // Re-enable device IRQ if needed
🔧     writel(DEVICE_IRQ_EN, dev->reg_ctrl);
    
    return IRQ_HANDLED;
}

// Registration
request_threaded_irq(dev->irq, my_irq_top, my_irq_thread,
                     IRQF_ONESHOT, "my-device", dev);
// Cleanup
free_irq(dev->irq, dev);

// 2. Classic + still common – request_irq + workqueue
static irqreturn_t my_fast_handler(int irq, void *dev) {
🔧     struct my_device *d = dev;
    
    if (!device_has_data(d))
        return IRQ_NONE;
    
    // Schedule deferred work (runs in workqueue thread later)
    schedule_work(&d->work);
    return IRQ_HANDLED;
}

static void my_work_func(struct work_struct *work) {
    struct my_device *d = container_of(work, struct my_device, work);
    // Process data (can sleep)
    process_data(d);
}

// In driver init:
INIT_WORK(&dev->work, my_work_func);
request_irq(dev->irq, my_fast_handler, 0, "my-device", dev);

// In driver exit:
free_irq(dev->irq, dev);
flush_work(&dev->work);

// 3. Tasklet (legacy but still everywhere – 🔴 🔴 avoid for new code)
static void my_tasklet_func(unsigned long dev_ptr) {
    struct my_device *dev = (void *)dev_ptr;
    // Cannot sleep, but can access device data
    process_data_fast(dev);
}

DECLARE_TASKLET(my_tasklet, my_tasklet_func, (unsigned long)dev);

static irqreturn_t my_handler(int irq, void *dev_id) {
    tasklet_schedule(&my_tasklet);
    return IRQ_HANDLED;
}

// 4. Disable IRQ in handler (for level-triggered or slow ACK)
static irqreturn_t slow_ack_handler(int irq, void *dev_id) {
🔧     struct my_device *dev = dev_id;
    
    if (!device_has_data(dev))
        return IRQ_NONE;
    
    // Disable IRQ at controller (will be re-enabled later)
    disable_irq_nosync(irq);
    
    // Schedule work that will eventually re-enable
    queue_work(dev->wq, &dev->enable_work);
    
    return IRQ_HANDLED;
}

static void enable_work_func(struct work_struct *work) {
🔧     struct my_device *dev = container_of(work, struct my_device, enable_work);
    
    // Process data (can sleep)
    process_data(dev);
    
    // Re-enable IRQ
    enable_irq(dev->irq);
}
```

### 7. Performance Optimization Techniques

**IRQ Affinity Tuning:**

```bash
# Bind high-frequency IRQs to specific CPUs
echo "0x01" > /proc/irq/45/smp_affinity    # IRQ 45 → CPU 0 only

# Spread interrupts across CPUs for balance
echo "0xFF" > /proc/irq/45/smp_affinity    # IRQ 45 → All CPUs
```

**Measuring IRQ Latency:**

```bash
# Install trace-cmd (ftrace frontend)
sudo trace-cmd record -e irq -e sched

# Check hardirq time in /proc/softirqs (HI column)
cat /proc/softirqs
```

**Reducing IRQ Overhead:**

1. Use **MSI/MSI-X** over legacy IRQs (no IRQ sharing overhead)
2. Bind IRQs to **isolated CPUs** (CPU isolation in kernel command line)
3. Use **NAPI** for networking (batch packet processing)
4. Consider **polling** for latency-sensitive devices
5. Profile with **perf**: ``perf record -e irq:irq_handler_entry/exit``

### 8. Useful Monitoring and Debugging Commands

```bash
# View interrupt statistics per CPU
cat /proc/interrupts

# Example output (first few lines):
#            CPU0       CPU1       CPU2       CPU3
#   0:        100        110        105        108   IO-APIC-edge      timer
#   1:         50         48         45         47   IO-APIC-edge      i8042
#   8:          1          0          0          0   IO-APIC-edge      rtc0
#  45:       5000       5010       4998       5002   PCI-MSI-edge      eth0

# View softirq statistics (per CPU)
cat /proc/softirqs

# Example: NET_RX → tasklet, SCHED → scheduler, RCU_SOFTIRQ → RCU
# Higher numbers = more activity

# Monitor in real-time (watch for tasklet usage)
watch -n 1 'cat /proc/softirqs | head -20'

# List all IRQs with descriptions
cat /proc/interrupts | awk '{print $1, $(NF-1), $NF}'

# Check IRQ affinity
cat /proc/irq/*/smp_affinity

# View threaded IRQ threads
ps aux | grep irq/
ps aux | grep "irq/45-"              # Specific IRQ thread

# Check workqueue threads
ps aux | grep kworker

# System-wide softirq delay
mpstat -P ALL 1                      # %soft shows softirq CPU usage

# Real-time IRQ tracing (ftrace)
echo 1 > /sys/kernel/debug/tracing/events/irq/irq_handler_entry/enable
cat /sys/kernel/debug/tracing/trace_pipe | head -30

# Measure IRQ latency
cyclictest -m -n -h 200 -l 100000

# Find which CPUs handle which interrupts
for i in /proc/irq/*/; 🟢 🟢 do
    echo "IRQ $i:"
    cat "$i/smp_affinity_list"
done

# Check for IRQ storms (same IRQ firing repeatedly)
watch -n 0.1 'cat /proc/interrupts | grep NNN'

# Profile interrupt handlers
perf record -e irq:irq_handler_entry -e irq:irq_handler_exit -a sleep 10
perf report

# Get IRQ name by number
cat /proc/interrupts | grep "NNN:"
```

### 9. Interrupt Controller Architecture (ARM GIC Example)

**GIC (Generic Interrupt Controller) Layout:**

```
Peripheral Devices
    ↓
Interrupt Signal
    ↓
GIC Distributor (handles prioritization, masking, routing)
    ├── Shared peripheral interrupts (SPIs) 32–1019
    └── Private peripheral interrupts (PPIs) 16–31
    ↓
GIC Redistributor (per-CPU component)
    ├── Handles SGIs (0–15)
    ├── Handles PPIs (16–31)
    └── Routes to Local Interrupt Controller
    ↓
CPU Local Interrupt Controller
    ├── Pending queue
    ├── Priority arbiter
    └── → IRQ signal to CPU
```

**GIC Device Tree Entry:**

```dts
intc: interrupt-controller@f1001000 {
    compatible = "arm,gic-400";
    #interrupt-cells = <3>;
    interrupt-controller;
    reg = <0xf1001000 0x1000>,    /* Distributor */
          <0xf1002000 0x2000>;    /* CPU interface (GICC) */
    
    /* Interrupt specifier: (type, hwirq, flags) */
    /* type: 0=SPI (shared), 1=PPI (private) */
    /* flags: 1=edge, 4=level */
};
```

### 10. Interrupt Processing Flow (Detailed Timeline)

```
t=0ms: Hardware event (e.g., packet arrives)
       ↓
t=0.1µs: Interrupt signal to CPU's APIC/GIC
         ↓
t=0.5µs: CPU finishes current instruction, enters interrupt mode
         ├── Saves context (registers, flags, return address)
         ├── Switches to interrupt stack
         └── Disables preemption
         ↓
t=1µs: Kernel's interrupt entry code (arch asm)
       ├── Saves remaining context
       └── Calls generic_handle_irq()
       ↓
t=2µs: IRQ descriptor lookup and handler chain traversal
       ├── Finds irqaction linked list
       └── Calls first/only handler
       ↓
t=3µs–100µs: Top-half handler runs (MUST be fast!)
       ├── Reads device status
       ├── Acks interrupt at device
       └── Returns (possibly schedules bottom-half)
       ↓
t=100µs: Return from interrupt
         ├── Restores context
         ├── Re-enables interrupts (if appropriate)
         └── Returns to interrupted code
         ↓
t=100µs–∞: Bottom-half executes (asynchronously)
          ├── Softirq: When kernel does softirq processing (soon)
          ├── Tasklet: Similar timing to softirq
          ├── Workqueue: When kworker thread scheduled (ms range possible)
          └── Threaded IRQ: When kernel thread gets CPU time
```

### 11. Common Interrupt Issues and Debugging

| Issue | Symptoms | Debugging Steps |
|-------|----------|-----------------|
| **High IRQ latency** | System sluggish, audio pops | perf, cyclictest, isolcpus, check affinity |
| **IRQ storm** | One interrupt fires repeatedly, CPU at 100% | cat /proc/interrupts (rapidly increase), dmesg for error messages |
| **Handler not called** | Device not responding | Check /proc/interrupts, verify IRQ number, check dmesg for "no irqhandler" |
| **Shared IRQ conflict** | Both handlers called, one spurious | Return IRQ_NONE if not your interrupt, use IRQF_SHARED |
| **Threaded IRQ not running** | Data not processed | Check ps for irq thread, ensure IRQF_ONESHOT for level-triggered, check thread priority |
| **Memory allocation in IRQ** | Kernel crash/panic | Allocate in setup, not in handler; use GFP_ATOMIC if necessary (risky) |
| **Lock contention** | Spinlock held during sleep | 🔴 🔴 Don't sleep in top-half, use threaded IRQ or workqueue for blocking ops |

### 12. Architecture-Specific Considerations

**x86/x64 (APIC/IO-APIC):**
- Vector-based (256 possible interrupts)
- MSI/MSI-X for PCI devices
- LAPIC per CPU for local interrupts
⭐ - EOI (End-of-Interrupt) handling critical for level-triggered

**ARM (GIC):**
- SPIs (0–1019) shared, PPIs (0–15) private per CPU
- SGIs (0–15) CPU-to-CPU
- MMIO-based, separate distributor and redistributor (GICv3/v4)
- No EOI required (hardware handles it)

**RISC-V (PLIC):**
- Platform-wide interrupt controller
- Simple level-based, no vector table
- Limited interrupt sources typical (32–1024)

### 13. Modern Trends (2025–2026)

**What's Fading:**
- Tasklets (moving to workqueue BH context)
- New softirq implementations (limited slots, hard to accept upstream)
- Shared IRQs on legacy PCI (MSI/MSI-X now standard)

**What's Growing:**
- Threaded IRQ (safest, most flexible)
- Workqueue-based deferred work (can sleep, allocate)
- Workqueue in BH context (tasklet replacement)
- Interrupt affinity tuning and isolation
- Real-time kernel (RT_PREEMPT) adoption

**Kernel Command-Line Parameters (Tuning):**

```bash
# Isolate CPUs from general scheduling (for real-time/latency-sensitive)
isolcpus=2,3

# Reduce softirq processing jitter (limit softirq execution time)
default_sched_domain=1

# Disable IRQ affinity auto-tuning
irqaffinity=0

# NR_CPUS at build time (some arch-specific)
```

**Summary – Current Recommendation (early 2026)

- **New drivers → Threaded IRQ** (request_threaded_irq) or **Workqueue**
  - Safest, can sleep, most maintainable
  - Strongly preferred by upstream maintainers
  
⭐ - **Performance-critical paths** → Softirq (rarely, profiling required)
  - Only for core subsystems (NET, RCU, TIMER, BLOCK)
  - New softirqs almost never accepted
  
- **Legacy code** → Tasklet still ok but plan migration to:
  - **Workqueue in BH context** (modern tasklet replacement)
  - **Threaded IRQ** (if tied to specific interrupt)
  
- **Tuning** → Affinity, isolation, real-time kernel (RT_PREEMPT)

**Quick Motto 2026:**  
"**Thread it or queue it** – 🔴 🔴 avoid tasklets & new softirqs whenever possible."

Happy interrupt debugging! ⚡

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
