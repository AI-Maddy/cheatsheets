**cheatsheet** for **Linux bottom half** (deferred work / soft-interrupt) mechanisms as of early 2026.

Bottom halves allow interrupt handlers (top-half) to defer non-urgent/time-consuming work → executed later when system is less busy.

### Core Concepts

**Interrupt Context vs Process Context:**

- **Top-half (hard IRQ)**: Executes immediately, atomic, no sleeping, minimal latency needed
- **Bottom-half (soft IRQ/deferred)**: Executes asynchronously, can have priorities, may sleep (except softirq/tasklet)
- **Atomic Context**: Cannot sleep, allocate memory, call blocking functions, take mutexes
- **Process Context**: Can perform blocking operations, allocate memory, access user memory safely

**Why defer work?**

- Top-half handlers must be short to reduce interrupt latency
- Long operations block other interrupts on that CPU
- Bottom-halves allow flexible scheduling based on system load
- Improves system responsiveness and throughput

### Quick Comparison Table

| Mechanism          | Context              | Can Sleep? | Concurrency (same instance)      | Allocation     | Latency / Priority     | Main Users / Notes                              | Recommended When?                              | Modern Status (2025–2026)                  |
|--------------------|----------------------|------------|----------------------------------|----------------|------------------------|-------------------------------------------------|------------------------------------------------|--------------------------------------------|
| **Softirq**        | Interrupt            | ✗ No       | Multiple CPUs OK                 | Static         | Very low (highest)     | NET_TX/RX, Block, Timer, RCU, SCHED            | Very high-frequency, performance-critical      | Still core, but discouraged for new code   |
| **Tasklet**        | Interrupt            | ✗ No       | Single CPU only (serialized)     | Dynamic        | Low                    | Most drivers, SCSI, old networking              | Fast, non-sleeping work, simpler than softirq  | **Being phased out** (workqueue BH replacement) |
| **Workqueue**      | Process (kworker)    | ✓ Yes      | Multiple CPUs OK                 | Dynamic        | Medium–High            | Almost everything that can sleep                | Need to sleep, allocate memory, call fs/...    | **Preferred** for almost all new deferred work |
| **Threaded IRQ**   | Process (irq thread) | ✓ Yes      | Per-IRQ thread                   | Dynamic        | Medium                 | Modern drivers (especially slow bottom halves)  | Replace top-half + bottom-half combo           | Strongly recommended for new drivers       |
| **Old BH** (deprecated) | Interrupt       | ✗ No       | Global lock (very old)           | Static         | —                      | Pre-2.5 kernels                                 | Never (removed long ago)                       | Dead since ~2.5 era                        |

### When to Choose Which (Decision Flow – 2025/2026 style)

```
Your interrupt handler needs to defer work?

├── Must be **extremely fast** & high-frequency? (networking hot-path, timers, RCU)
│   └── → **Softirq**  (but think twice – new softirqs are very rarely accepted)
│
├── Can **not** sleep, no memory allocation, no fs calls, etc.?
│   ├── Want simplest API + automatic serialization?
│   │   └── → **Tasklet**  (still works, but prefer workqueue BH in new code)
│   └── Want maximum performance + per-CPU execution?
│       └── → **Softirq** (very rare for new code)
│
└── Can sleep / allocate memory / call blocking functions / take mutexes?
    ├── Want automatic per-IRQ threading (modern best practice)?
    │   └── → **Threaded IRQ**  (request_threaded_irq())
    └── Want flexible queuing, priorities, system-wide worker pools?
        └── → **Workqueue**  (queue_work* / schedule_work* / delayed_work / system_wq / dedicated wq)

    Bonus modern option (2024+) → **Workqueue in BH context**  
    (special workqueues that run in interrupt context → replacement for tasklets)
```

### Quick Code Snippets (most common patterns 2025/2026)

```c
// 1. Modern default choice: Workqueue (process context)
DECLARE_WORK(my_work, my_work_func, NULL);
schedule_work(&my_work);                    // or queue_work(my_wq, &my_work)

// 2. Threaded IRQ (very popular in new drivers)
request_threaded_irq(irq, quick_handler, thread_fn, IRQF_ONESHOT, "mydev", dev);

// 3. Tasklet (still ok, but not recommended for new code)
DECLARE_TASKLET(my_tasklet, my_tasklet_func, (unsigned long)dev);
tasklet_schedule(&my_tasklet);

// 4. Softirq (only when you really need it – very rare nowadays)
open_softirq(MY_SOFTIRQ, my_softirq_handler);   // static, compile-time
raise_softirq(MY_SOFTIRQ);
```

### Monitoring (very useful commands)

```bash
cat /proc/softirqs          # shows softirq statistics per CPU + type
cat /proc/interrupts        # classic interrupt counters
watch -n1 grep -i tasklet /proc/softirqs   # see if tasklets are still busy
ps aux | grep kworker       # see workqueue threads activity
```

### Detailed Mechanism Breakdown

**Softirq (Software Interrupt)**

- Registered statically at compile time via ``open_softirq()``
- Only 32 softirq types available (limited slots)
- Runs in interrupt context (atomic, no sleep)
- Can execute on multiple CPUs simultaneously
- Raised via ``raise_softirq()`` or ``raise_softirq_irqoff()``
- Protected by per-CPU disabling, not per-instance locking
- Used for: networking (NET_TX/RX), block I/O, timers, RCU, scheduling
- **Key limitation**: New softirqs are almost never accepted upstream (limited slots)

```c
// Define at compile time
static DECLARE_TASKLET(my_softirq_func, NULL);

// In module init
open_softirq(MY_SOFTIRQ, my_softirq_handler);

// In interrupt handler
raise_softirq(MY_SOFTIRQ);
```

**Tasklet (Dynamic Softirq-like)**

- Lightweight, softirq-like but dynamically allocated
- Single CPU execution (per-tasklet serialization)
- Runs in interrupt context (no sleep, atomic)
- Can use ``tasklet_disable()`` to prevent execution
- Useful for simple, fast bottom-halves
- **Status**: Being phased out in favor of workqueue in BH context

```c
// Define and initialize
DECLARE_TASKLET(my_tasklet, tasklet_func, (unsigned long)dev);
// or dynamically:
tasklet_init(&my_tasklet, tasklet_func, (unsigned long)dev);

// Schedule for later execution
tasklet_schedule(&my_tasklet);

// Disable/enable
tasklet_disable(&my_tasklet);
tasklet_enable(&my_tasklet);
```

**Workqueue (Process-Context Deferred Work)**

- Executed by ``kworker`` kernel threads (process context)
- Can sleep, allocate memory, call blocking functions
- Supports priorities and custom/shared queues
- ``schedule_work()`` → uses default system queue
- ``queue_work()`` → custom workqueue
- Delayed variants: ``schedule_delayed_work()``
- Per-CPU variant: ``queue_work_on()``
- Flush functions: ``flush_work()``, ``flush_workqueue()``
- **Recommended for**: Most new deferred work

```c
// Simple work struct
struct work_struct work;
DECLARE_WORK(my_work, work_func);

// Schedule on default queue
schedule_work(&my_work);

// Or use custom workqueue
struct workqueue_struct *wq = create_workqueue("my_wq");
queue_work(wq, &my_work);

// Delayed work
DECLARE_DELAYED_WORK(delayed, work_func);
queue_delayed_work(wq, &delayed, msecs_to_jiffies(100));

// Cleanup
flush_work(&my_work);
flush_workqueue(wq);
destroy_workqueue(wq);
```

**Threaded IRQ (Interrupt Thread)**

- Handler split into top-half (primary) and bottom-half (thread function)
- Bottom-half runs in a dedicated per-IRQ kernel thread
- Process context → can sleep, block, allocate memory
- Automatic serialization per IRQ
- ``IRQF_ONESHOT``: Disables IRQ during thread execution (for level-triggered)
- ``IRQF_TRIGGER_*``: Specify trigger type
- **Modern best practice** for many drivers

```c
// Top-half runs in interrupt context (must be fast!)
static irqreturn_t irq_handler(int irq, void *dev_id) {
    struct my_device *dev = dev_id;
    
    // Minimal work here
    if (!(read_status(dev) & STATUS_READY))
        return IRQ_NONE;
    
    // Disable IRQ and return to wake thread
    return IRQ_WAKE_THREAD;
}

// Bottom-half runs in kernel thread (can sleep!)
static irqreturn_t irq_thread_fn(int irq, void *dev_id) {
    struct my_device *dev = dev_id;
    
    // Safe to sleep, allocate memory, etc.
    mutex_lock(&dev->lock);
    process_data(dev);
    mutex_unlock(&dev->lock);
    
    return IRQ_HANDLED;
}

// Registration
request_threaded_irq(irq, irq_handler, irq_thread_fn, 
                     IRQF_ONESHOT, "my_device", dev);

// Cleanup
free_irq(irq, dev);
```

### Workqueue in Bottom-Half Context (Modern Tasklet Replacement)

Since kernel 5.17, workqueues can execute in BH context (like tasklets):

```c
// Create a BH workqueue (replaces tasklets)
struct workqueue_struct *bh_wq = create_workqueue("bh_work");

// Queue work that runs in BH context
queue_work(bh_wq, &work);

// Or use pre-allocated queues
struct work_struct work;
INIT_WORK(&work, work_func);
queue_work(system_bh_wq, &work);  // New in recent kernels
```

### Concurrency and Locking

| Mechanism | Serialization | Locking Notes |
|-----------|---------------|---------------|
| **Softirq** | Per-CPU disabled (no multicore on same softirq type) | No per-instance locking; shared data needs spinlock or atomic ops |
| **Tasklet** | Single CPU only (automatic serialization) | Multiple tasklets of same type can run on different CPUs; shared data needs spinlock |
| **Workqueue** | Depends on queue (default: shared) | Multiple workers can run in parallel; needs mutex or spinlock for shared data |
| **Threaded IRQ** | Per-IRQ thread (automatic per-thread) | Per-instance serialization; can use mutexes safely |

### Memory Allocation and Sleeping

| Mechanism | Can Sleep? | Can Allocate Memory (GFP_KERNEL)? | Can Take Mutex? |
|-----------|------------|-----------------------------------|-----------------|
| **Softirq** | ✗ No | ✗ No (GFP_ATOMIC only) | ✗ No |
| **Tasklet** | ✗ No | ✗ No (GFP_ATOMIC only) | ✗ No |
| **Workqueue** | ✓ Yes | ✓ Yes (GFP_KERNEL OK) | ✓ Yes |
| **Threaded IRQ** | ✓ Yes | ✓ Yes (GFP_KERNEL OK) | ✓ Yes |

### Common Performance Patterns

**High-frequency, low-latency path (networking):**
```c
// Use softirq or tasklet
tasklet_schedule(&net_tasklet);
```

**Device driver with blocking I/O:**
```c
// Use threaded IRQ or workqueue
request_threaded_irq(irq, quick_check, blocking_work, IRQF_ONESHOT, "dev", dev);
```

**Periodic maintenance work:**
```c
// Use delayed workqueue
queue_delayed_work(my_wq, &cleanup_work, HZ);  // Every 1 second
```

### Monitoring and Debugging Commands

```bash
# View softirq statistics
cat /proc/softirqs

# View IRQ statistics
cat /proc/interrupts

# View tasklet activity
grep -i tasklet /proc/softirqs

# Monitor workqueue threads
ps aux | grep kworker

# Real-time monitoring
watch -n 0.5 'cat /proc/softirqs'

# Trace softirq execution (ftrace)
echo 1 > /sys/kernel/debug/tracing/events/irq/softirq_entry/enable
cat /sys/kernel/debug/tracing/trace_pipe

# Check workqueue activity
cat /proc/pressure/io

# Top-level interrupt status
watch -n 1 'head -20 /proc/interrupts'
```

### Priority and Timing Characteristics

| Mechanism | Relative Latency | Jitter | Load Aware? | CPU Affinity? |
|-----------|------------------|--------|------------|---------------|
| **Softirq** | Lowest (atomic) | Low | Yes (disabled softirqs) | Per-CPU bound |
| **Tasklet** | Low (atomic) | Low | Yes (per-CPU) | Can be pinned |
| **Workqueue** | Higher (threaded) | Medium | Yes (kworker threads) | Flexible (can use queue_work_on) |
| **Threaded IRQ** | Medium-High | Medium | Moderate (single thread per IRQ) | Per-IRQ bound initially |

### Summary – Current Recommendation (early 2026)

- **New code → prefer workqueue** or **threaded IRQ**
  - Workqueue: For flexible, scalable deferred work
  - Threaded IRQ: For interrupt handlers with blocking bottom-half
  
- **Need atomic context + very fast → softirq** (very rare for new code)
  - Only if profiling shows necessity
  - New softirqs almost never accepted upstream
  
- **Still need tasklet → ok for maintenance**, but plan migration to:
  - **Workqueue in BH context** (newer replacement)
  - **Threaded IRQ** (if tied to specific interrupt)
  
- **Old BH / task queue → dead code**, remove when you see it
  - Pre-2.5 kernel mechanism, long deprecated

### Quick Reference: Which Mechanism When?

| Requirement | Best Choice | Fallback |
|-------------|-------------|----------|
| Blocking I/O needed | Threaded IRQ | Workqueue |
| Memory allocation needed | Workqueue | Threaded IRQ |
| Sub-millisecond latency | Softirq | Tasklet |
| Simple, non-blocking | Tasklet | Softirq |
| Flexible scheduling | Workqueue | Threaded IRQ |
| Per-CPU optimization | Softirq | Workqueue on_cpu |
| Maintenance code | Tasklet | Workqueue BH |

### Real-World Examples

**Network Driver (RX packets):**
```c
// Fast path: decide in IRQ, defer actual processing
irqreturn_t net_isr(int irq, void *dev) {
    if (rx_ready(dev)) {
        tasklet_schedule(&dev->rx_tasklet);  // or queue_work()
        return IRQ_HANDLED;
    }
    return IRQ_NONE;
}

void rx_tasklet_func(unsigned long dev_ptr) {
    struct net_device *dev = (void *)dev_ptr;
    while (rx_ready(dev))
        process_rx_packet(dev);
}
```

**Character Device (buffered I/O):**
```c
// Threaded IRQ allows sleeping in bottom-half
irqreturn_t uart_isr(int irq, void *data) {
    struct uart_port *port = data;
    if (!(read_isr(port) & RX_READY))
        return IRQ_NONE;
    return IRQ_WAKE_THREAD;  // Wake thread handler
}

irqreturn_t uart_thread_fn(int irq, void *data) {
    struct uart_port *port = data;
    
    // Safe to call blocking functions
    mutex_lock(&port->lock);
    copy_to_user(port->buf, port->rx_data, count);
    mutex_unlock(&port->lock);
    wake_up(&port->waitq);
    
    return IRQ_HANDLED;
}
```

**Maintenance Task (with flexibility):**
```c
// Workqueue allows flexible scheduling
static void cleanup_work_func(struct work_struct *work) {
    struct my_driver *drv = container_of(work, struct my_driver, cleanup);
    
    // Safe to sleep, allocate, etc.
    kmalloc(4096, GFP_KERNEL);
    synchronize_rcu();
    
    // Reschedule if needed
    queue_delayed_work(drv->wq, &drv->cleanup, HZ * 60);  // Every minute
}
```

### Additional Resources

- **Kernel Documentation**: `Documentation/timers/softirq.rst`
- **Driver Development**: `Documentation/driver-api/basics.rst`
- **Interrupt Handling**: `Documentation/core-api/irq/` 
- **Workqueue API**: `include/linux/workqueue.h`

Happy deferring! 🚀