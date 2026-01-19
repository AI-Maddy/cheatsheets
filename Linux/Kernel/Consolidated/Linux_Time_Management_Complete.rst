================================================================================
Linux Time Management - Comprehensive Cheatsheet
================================================================================

:Author: Linux Kernel Documentation Team
:Date: January 17, 2026
:Version: 1.0
:Target Audience: Kernel developers, real-time systems engineers, embedded developers
:Scope: Jiffies, timers, hrtimers, clocksource, clockevents, timekeeping, POSIX clocks

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**Time Concepts**:

+------------------+----------------------------+----------------------------------+
| **Concept**      | **Resolution**             | **Purpose**                      |
+==================+============================+==================================+
| jiffies          | 1-10 ms (HZ dependent)     | Low-resolution timing, legacy    |
+------------------+----------------------------+----------------------------------+
| hrtimer          | Nanosecond (hardware       | High-resolution timers           |
|                  | dependent)                 |                                  |
+------------------+----------------------------+----------------------------------+
| clocksource      | Hardware-specific          | Time measurement (TSC, HPET)     |
+------------------+----------------------------+----------------------------------+
| clockevent       | Programmable               | Timer interrupts (APIC, HPET)    |
+------------------+----------------------------+----------------------------------+

**Common Timer Operations**:

.. code-block:: c

    // Low-resolution timer (jiffies-based)
    struct timer_list my_timer;
    timer_setup(&my_timer, callback, 0);
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(1000));  // Fire in 1s
    del_timer(&my_timer);
    
    // High-resolution timer (nanosecond precision)
    struct hrtimer my_hrtimer;
    hrtimer_init(&my_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
    my_hrtimer.function = hrtimer_callback;
    hrtimer_start(&my_hrtimer, ms_to_ktime(100), HRTIMER_MODE_REL);  // 100ms
    hrtimer_cancel(&my_hrtimer);
    
    // Delays
    mdelay(10);           // Busy-wait for 10 ms (blocks CPU!)
    msleep(1000);         // Sleep for 1 second (scheduler-based)
    usleep_range(100, 200); // Sleep 100-200 microseconds
    ndelay(500);          // Nanosecond busy-wait

**HZ Configuration**:

.. code-block:: bash

    # Check current HZ
    grep 'CONFIG_HZ=' /boot/config-$(uname -r)
    
    # Common values:
    # CONFIG_HZ=100   (10 ms tick, server)
    # CONFIG_HZ=250   (4 ms tick, balanced)
    # CONFIG_HZ=1000  (1 ms tick, desktop/low-latency)

**Clock Types**:

.. code-block:: c

    CLOCK_REALTIME:      // Wall-clock time (can jump, NTP adjusted)
    CLOCK_MONOTONIC:     // Monotonic time (never goes backwards)
    CLOCK_BOOTTIME:      // Like MONOTONIC, includes suspend time
    CLOCK_PROCESS_CPUTIME_ID:  // Per-process CPU time
    CLOCK_THREAD_CPUTIME_ID:   // Per-thread CPU time

**Reading Time**:

.. code-block:: c

    // Kernel space
    ktime_t now = ktime_get();              // Monotonic time (ktime_t)
    u64 ns = ktime_get_ns();                // Monotonic time (nanoseconds)
    struct timespec64 ts = ktime_get_ts64();  // Monotonic timespec
    unsigned long jiff = jiffies;           // Jiffy count
    
    // User space
    clock_gettime(CLOCK_MONOTONIC, &ts);    // POSIX clock
    gettimeofday(&tv, NULL);                // Legacy (CLOCK_REALTIME)

**Time Conversion**:

.. code-block:: c

    // jiffies ↔ milliseconds
    unsigned long jiff = msecs_to_jiffies(1000);  // 1000 ms → jiffies
    unsigned int ms = jiffies_to_msecs(jiff);
    
    // ktime ↔ timespec
    ktime_t kt = timespec64_to_ktime(ts);
    struct timespec64 ts = ktime_to_timespec64(kt);
    
    // ktime ↔ nanoseconds
    ktime_t kt = ns_to_ktime(1000000);    // 1 ms
    u64 ns = ktime_to_ns(kt);

**Clocksource Selection**:

.. code-block:: bash

    # List available clocksources
    cat /sys/devices/system/clocksource/clocksource0/available_clocksource
    # Output: tsc hpet acpi_pm
    
    # Check current clocksource
    cat /sys/devices/system/clocksource/clocksource0/current_clocksource
    # Output: tsc
    
    # Change clocksource
    echo hpet > /sys/devices/system/clocksource/clocksource0/current_clocksource

================================================================================
Section 1: Jiffies and Low-Resolution Timing
================================================================================

1.1 Jiffies Concept
================================================================================

**What are Jiffies?**

Jiffies are the fundamental unit of time in the Linux kernel:
- Global counter incremented at every timer interrupt
- Frequency determined by ``HZ`` (configured at kernel compile time)
- 32-bit or 64-bit depending on architecture

**jiffies Variable**:

.. code-block:: c

    // Kernel definition
    extern unsigned long volatile jiffies;
    extern u64 jiffies_64;
    
    // On 32-bit systems: jiffies wraps around every ~49.7 days (HZ=100)
    // On 64-bit systems: jiffies_64 wraps around every 584 million years

**HZ Values**:

+-------+-------------+------------------+-----------------------------+
| HZ    | Tick Period | Use Case         | Notes                       |
+=======+=============+==================+=============================+
| 100   | 10 ms       | Servers          | Lower overhead, more battery|
+-------+-------------+------------------+-----------------------------+
| 250   | 4 ms        | Balanced         | Default on many distros     |
+-------+-------------+------------------+-----------------------------+
| 1000  | 1 ms        | Desktop/gaming   | Better responsiveness       |
+-------+-------------+------------------+-----------------------------+

**Reading Jiffies**:

.. code-block:: c

    unsigned long now = jiffies;
    
    // On 32-bit, read jiffies_64 safely
    u64 now64 = get_jiffies_64();

1.2 Jiffy Arithmetic and Wraparound
================================================================================

**Wraparound Problem**:

.. code-block:: c

    // WRONG: Direct comparison fails on wraparound
    unsigned long start = jiffies;
    // ... some time passes ...
    if (jiffies > start + timeout) {  // WRONG! Fails when jiffies wraps
        // Timeout
    }
    
    // CORRECT: Use time_after macros
    unsigned long start = jiffies;
    unsigned long timeout = msecs_to_jiffies(1000);
    
    if (time_after(jiffies, start + timeout)) {
        // Timeout occurred
    }

**Time Comparison Macros**:

.. code-block:: c

    time_after(a, b)         // True if a is after b
    time_before(a, b)        // True if a is before b
    time_after_eq(a, b)      // True if a >= b
    time_before_eq(a, b)     // True if a <= b
    
    // For jiffies_64
    time_after64(a, b)
    time_before64(a, b)

**Why They Work**:

.. code-block:: c

    #define time_after(a, b) \
        (typecheck(unsigned long, a) && \
         typecheck(unsigned long, b) && \
         ((long)((b) - (a)) < 0))
    
    // Signed comparison handles wraparound:
    // Before wrap: (long)(end - start) = positive
    // After wrap:  (long)(end - start) = negative (due to overflow)

1.3 Jiffy Conversion
================================================================================

**Convert to/from Jiffies**:

.. code-block:: c

    // Milliseconds ↔ Jiffies
    unsigned long j = msecs_to_jiffies(1000);  // 1000 ms → jiffies
    unsigned int ms = jiffies_to_msecs(j);
    
    // Microseconds ↔ Jiffies
    unsigned long j = usecs_to_jiffies(500000);  // 500 ms
    unsigned int us = jiffies_to_usecs(j);
    
    // Nanoseconds ↔ Jiffies
    unsigned long j = nsecs_to_jiffies64(1000000000);  // 1 second
    u64 ns = jiffies64_to_nsecs(j);
    
    // Timespec ↔ Jiffies
    unsigned long j = timespec64_to_jiffies(&ts);
    struct timespec64 ts = ns_to_timespec64(jiffies_to_nsecs(j));

**Precision Loss**:

.. code-block:: c

    // Example: HZ=100 (10 ms tick)
    unsigned long j = msecs_to_jiffies(15);  // 15 ms
    // Result: 2 jiffies (20 ms) - rounded up
    
    unsigned int ms = jiffies_to_msecs(j);
    // Result: 20 ms (not original 15 ms!)

1.4 Legacy Timer API (Low-Resolution)
================================================================================

**struct timer_list**:

.. code-block:: c

    struct timer_list {
        struct hlist_node       entry;
        unsigned long           expires;   // Expiration time (jiffies)
        void (*function)(struct timer_list *);
        u32                     flags;
    };

**Timer Lifecycle**:

.. code-block:: c

    // 1. Define timer
    static struct timer_list my_timer;
    
    // 2. Callback function
    static void my_timer_callback(struct timer_list *t)
    {
        pr_info("Timer expired!\n");
        
        // Optionally re-arm for periodic timer
        mod_timer(t, jiffies + msecs_to_jiffies(1000));
    }
    
    // 3. Initialize timer
    timer_setup(&my_timer, my_timer_callback, 0);
    
    // 4. Start timer
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(5000));  // Fire in 5s
    
    // 5. Cancel timer (if needed)
    del_timer(&my_timer);       // Non-blocking
    // or
    del_timer_sync(&my_timer);  // Wait for callback to finish

**Timer Functions**:

.. code-block:: c

    void timer_setup(struct timer_list *timer,
                     void (*callback)(struct timer_list *),
                     unsigned int flags);
    
    int mod_timer(struct timer_list *timer, unsigned long expires);
    // Returns: 0 if timer was inactive, 1 if timer was active
    
    int del_timer(struct timer_list *timer);
    // Returns: 0 if timer was inactive, 1 if timer was active (deactivated)
    
    int del_timer_sync(struct timer_list *timer);
    // Like del_timer but waits for callback to finish (cannot call from callback!)
    
    int timer_pending(const struct timer_list *timer);
    // Returns: 1 if timer is pending, 0 otherwise

**Periodic Timer Example**:

.. code-block:: c

    static struct timer_list periodic_timer;
    
    static void periodic_callback(struct timer_list *t)
    {
        pr_info("Periodic task executed at %lu jiffies\n", jiffies);
        
        // Re-arm timer for next interval (1 second)
        mod_timer(t, jiffies + HZ);
    }
    
    static int __init my_module_init(void)
    {
        timer_setup(&periodic_timer, periodic_callback, 0);
        mod_timer(&periodic_timer, jiffies + HZ);  // Start immediately
        return 0;
    }
    
    static void __exit my_module_exit(void)
    {
        del_timer_sync(&periodic_timer);
    }

================================================================================
Section 2: High-Resolution Timers (hrtimers)
================================================================================

2.1 hrtimer Overview
================================================================================

**Why hrtimers?**

Legacy timers (timer_list) have jiffy resolution (1-10 ms). hrtimers provide:
- Nanosecond precision (hardware-dependent)
- Separate from jiffy tick
- Uses clockevent hardware
- Better for real-time and multimedia

**ktime_t Type**:

.. code-block:: c

    // Opaque type representing nanoseconds (64-bit)
    typedef s64 ktime_t;
    
    // Constructors
    ktime_t kt = ms_to_ktime(100);      // 100 milliseconds
    ktime_t kt = us_to_ktime(500);      // 500 microseconds
    ktime_t kt = ns_to_ktime(1000000);  // 1 million nanoseconds (1 ms)
    
    // Conversions
    s64 ns = ktime_to_ns(kt);
    s64 us = ktime_to_us(kt);
    s64 ms = ktime_to_ms(kt);

2.2 hrtimer API
================================================================================

**struct hrtimer**:

.. code-block:: c

    struct hrtimer {
        struct timerqueue_node  node;
        ktime_t                 _softexpires;
        enum hrtimer_restart (*function)(struct hrtimer *);
        struct hrtimer_clock_base *base;
        u8                      state;
        u8                      is_rel;
        u8                      is_soft;
    };

**Clock Bases**:

.. code-block:: c

    CLOCK_REALTIME:      // System wall-clock time (can jump)
    CLOCK_MONOTONIC:     // Monotonic time (never goes backwards)
    CLOCK_BOOTTIME:      // Monotonic + suspend time
    CLOCK_TAI:           // International Atomic Time

**Timer Modes**:

.. code-block:: c

    HRTIMER_MODE_ABS:    // Absolute time (expire at specific ktime)
    HRTIMER_MODE_REL:    // Relative time (expire after duration)
    HRTIMER_MODE_SOFT:   // Execute in softirq context (less precise, lower overhead)
    HRTIMER_MODE_HARD:   // Execute in hardirq context (precise, higher overhead)

**hrtimer Lifecycle**:

.. code-block:: c

    static struct hrtimer my_hrtimer;
    
    // Callback function
    static enum hrtimer_restart my_hrtimer_callback(struct hrtimer *timer)
    {
        pr_info("hrtimer expired at %lld ns\n", ktime_to_ns(ktime_get()));
        
        // Return HRTIMER_NORESTART (one-shot)
        // or HRTIMER_RESTART (periodic)
        return HRTIMER_NORESTART;
    }
    
    // Initialize
    hrtimer_init(&my_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
    my_hrtimer.function = my_hrtimer_callback;
    
    // Start timer (100 ms from now)
    hrtimer_start(&my_hrtimer, ms_to_ktime(100), HRTIMER_MODE_REL);
    
    // Cancel timer
    hrtimer_cancel(&my_hrtimer);

**hrtimer Functions**:

.. code-block:: c

    void hrtimer_init(struct hrtimer *timer, clockid_t which_clock,
                      enum hrtimer_mode mode);
    
    void hrtimer_start(struct hrtimer *timer, ktime_t tim,
                       const enum hrtimer_mode mode);
    
    int hrtimer_cancel(struct hrtimer *timer);
    // Returns: 0 if timer was inactive, 1 if timer was active
    
    int hrtimer_try_to_cancel(struct hrtimer *timer);
    // Like cancel but doesn't wait for callback
    // Returns: -1 if callback running, 0 if inactive, 1 if cancelled
    
    int hrtimer_active(const struct hrtimer *timer);
    // Returns: 1 if timer is pending, 0 otherwise

2.3 Periodic hrtimer Example
================================================================================

.. code-block:: c

    static struct hrtimer periodic_hr_timer;
    static ktime_t interval;
    
    static enum hrtimer_restart periodic_hr_callback(struct hrtimer *timer)
    {
        ktime_t now = ktime_get();
        
        pr_info("Periodic hrtimer at %lld ns\n", ktime_to_ns(now));
        
        // Forward timer by interval
        hrtimer_forward(timer, now, interval);
        
        return HRTIMER_RESTART;  // Keep firing
    }
    
    static int __init my_module_init(void)
    {
        interval = ms_to_ktime(10);  // 10 ms period
        
        hrtimer_init(&periodic_hr_timer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
        periodic_hr_timer.function = periodic_hr_callback;
        
        hrtimer_start(&periodic_hr_timer, interval, HRTIMER_MODE_REL);
        return 0;
    }
    
    static void __exit my_module_exit(void)
    {
        hrtimer_cancel(&periodic_hr_timer);
    }

2.4 hrtimer vs timer_list
================================================================================

+-------------------+---------------------------+---------------------------+
| **Feature**       | **timer_list**            | **hrtimer**               |
+===================+===========================+===========================+
| Resolution        | Jiffy (1-10 ms)           | Nanosecond (hardware)     |
+-------------------+---------------------------+---------------------------+
| Overhead          | Lower                     | Higher                    |
+-------------------+---------------------------+---------------------------+
| Use case          | Low-precision timers      | Real-time, multimedia     |
+-------------------+---------------------------+---------------------------+
| Clock source      | Tied to HZ tick           | Hardware clockevent       |
+-------------------+---------------------------+---------------------------+
| Wakeup from idle  | No (tick-based)           | Yes (can wake CPU)        |
+-------------------+---------------------------+---------------------------+

**When to Use Each**:
- **timer_list**: Timeout checks, periodic tasks (second-scale), less critical timing
- **hrtimer**: Precise delays, real-time deadlines, multimedia (audio/video), profiling

================================================================================
Section 3: Delays and Sleeps
================================================================================

3.1 Busy-Wait Delays
================================================================================

**mdelay / udelay / ndelay**:

.. code-block:: c

    void mdelay(unsigned long msecs);  // Busy-wait milliseconds
    void udelay(unsigned long usecs);  // Busy-wait microseconds
    void ndelay(unsigned long nsecs);  // Busy-wait nanoseconds
    
    // Example
    pr_info("Before delay\n");
    mdelay(10);  // CPU spins for 10 ms (blocks everything!)
    pr_info("After delay\n");

**Characteristics**:
- Blocks CPU (cannot schedule other tasks)
- Accurate (not affected by scheduler)
- Use ONLY when absolutely necessary (atomic context, very short delays <1ms)

**When to Use**:
✓ Atomic context (cannot sleep)
✓ Hardware delays (device initialization)
✓ Very short delays (<1 ms)

❌ **Never use for long delays** (wastes CPU, hurts performance)

3.2 Scheduler-Based Sleeps
================================================================================

**msleep / usleep_range**:

.. code-block:: c

    void msleep(unsigned int msecs);           // Sleep milliseconds (can be interrupted)
    void msleep_interruptible(unsigned int msecs);  // Returns early if signal received
    void usleep_range(unsigned long min, unsigned long max);  // Sleep microseconds

    // Examples
    msleep(1000);             // Sleep 1 second
    usleep_range(100, 200);   // Sleep 100-200 microseconds

**Characteristics**:
- Process sleeps (scheduler can run other tasks)
- Cannot be called from atomic context
- Less precise than busy-wait (scheduler granularity)

**usleep_range Precision**:

.. code-block:: c

    // Preferred for sub-jiffy sleeps
    usleep_range(100, 150);  // 100-150 μs
    
    // Kernel can batch wakeups in range [min, max]
    // Improves power efficiency (fewer wakeups)

3.3 Schedule Timeouts
================================================================================

**schedule_timeout**:

.. code-block:: c

    long schedule_timeout(long timeout);  // Sleep for timeout jiffies
    // Returns: 0 if timeout elapsed, remaining jiffies if interrupted
    
    long schedule_timeout_interruptible(long timeout);
    long schedule_timeout_uninterruptible(long timeout);
    long schedule_timeout_killable(long timeout);

**Example**:

.. code-block:: c

    // Sleep for 5 seconds
    set_current_state(TASK_INTERRUPTIBLE);
    schedule_timeout(HZ * 5);
    
    // Or use wrapper
    schedule_timeout_interruptible(HZ * 5);

3.4 Delay Selection Guide
================================================================================

.. code-block:: text

    Choose delay mechanism:
    
    Can sleep (process context)?
    ├── No (atomic context, spinlock held, IRQ handler)
    │   └── Use: mdelay(), udelay(), ndelay()
    │       ⚠️  Keep delays very short (<1 ms)
    │
    └── Yes (can sleep)
        ├── Delay > 10 ms?
        │   └── Use: msleep(), msleep_interruptible()
        │
        └── Delay < 10 ms?
            └── Use: usleep_range(min, max)

================================================================================
Section 4: Clocksources and Timekeeping
================================================================================

4.1 Clocksource Abstraction
================================================================================

**What is a Clocksource?**

A clocksource provides monotonically increasing cycle counts:
- Hardware counter (TSC, HPET, ACPI PM timer)
- Read to get current time
- Kernel converts cycles → nanoseconds

**struct clocksource**:

.. code-block:: c

    struct clocksource {
        u64 (*read)(struct clocksource *cs);   // Read counter
        u64 mask;                               // Counter mask
        u32 mult;                               // Multiplier for conversion
        u32 shift;                              // Shift for conversion
        u64 max_idle_ns;                        // Max idle before wrap
        const char *name;                       // "tsc", "hpet", etc.
        int rating;                             // Quality rating
        // ... more fields ...
    };

**Common Clocksources (x86)**:

+-------------------+-----------+-------------+-------------------------------+
| **Name**          | **Rating**| **Accuracy**| **Notes**                     |
+===================+===========+=============+===============================+
| TSC (rdtsc)       | 300       | Nanosecond  | CPU Time Stamp Counter (fast) |
+-------------------+-----------+-------------+-------------------------------+
| HPET              | 250       | Nanosecond  | High Precision Event Timer    |
+-------------------+-----------+-------------+-------------------------------+
| ACPI PM Timer     | 200       | ~280 ns     | Slow (I/O read), reliable     |
+-------------------+-----------+-------------+-------------------------------+
| jiffies           | 1         | 1-10 ms     | Fallback only                 |
+-------------------+-----------+-------------+-------------------------------+

**Selecting Clocksource**:

.. code-block:: bash

    # View available clocksources
    cat /sys/devices/system/clocksource/clocksource0/available_clocksource
    # Output: tsc hpet acpi_pm
    
    # Current clocksource
    cat /sys/devices/system/clocksource/clocksource0/current_clocksource
    # Output: tsc
    
    # Override clocksource (runtime)
    echo hpet > /sys/devices/system/clocksource/clocksource0/current_clocksource
    
    # Or at boot
    # Kernel command line: clocksource=hpet

4.2 TSC (Time Stamp Counter)
================================================================================

**Reading TSC**:

.. code-block:: c

    // x86 assembly: rdtsc instruction
    static inline u64 rdtsc(void)
    {
        u32 low, high;
        asm volatile("rdtsc" : "=a" (low), "=d" (high));
        return ((u64)high << 32) | low;
    }
    
    // Kernel helper
    u64 cycles = rdtsc_ordered();

**TSC Characteristics**:
- Very fast (single CPU instruction)
- Per-CPU counter (can drift between CPUs)
- Modern CPUs: invariant TSC (constant rate, synchronized)

**TSC Issues**:
- **Frequency changes**: Old CPUs change TSC rate with CPU frequency
- **Non-synchronized**: Multi-socket systems may have different TSC values
- **VM issues**: Can be unstable in virtual machines

**TSC Stability Check**:

.. code-block:: bash

    # Check if TSC is stable
    dmesg | grep -i tsc
    # Good: "tsc: Marking TSC unstable due to check_tsc_sync_source failed"
    # Bad:  "tsc: Detected 2.4 GHz processor"

4.3 ktime_get Family
================================================================================

**Reading Current Time**:

.. code-block:: c

    // Monotonic time (never goes backwards)
    ktime_t now = ktime_get();              // ktime_t (nanoseconds)
    u64 ns = ktime_get_ns();                // u64 nanoseconds
    struct timespec64 ts = ktime_get_ts64();
    
    // Real time (wall clock, can jump)
    ktime_t rt = ktime_get_real();
    u64 rt_ns = ktime_get_real_ns();
    
    // Boot time (monotonic + suspend time)
    ktime_t boot = ktime_get_boottime();
    u64 boot_ns = ktime_get_boottime_ns();
    
    // Coarse (cached, faster, less precise)
    ktime_t coarse = ktime_get_coarse();    // ~jiffy precision
    struct timespec64 coarse_ts = ktime_get_coarse_ts64();

**Performance Comparison**:

+----------------------+---------------+-------------------------------------+
| **Function**         | **Latency**   | **Use Case**                        |
+======================+===============+=====================================+
| ktime_get()          | ~50 ns        | Accurate timestamps                 |
+----------------------+---------------+-------------------------------------+
| ktime_get_coarse()   | ~10 ns        | Frequent reads, lower precision OK  |
+----------------------+---------------+-------------------------------------+
| ktime_get_real()     | ~50 ns        | Wall-clock time (user-facing)       |
+----------------------+---------------+-------------------------------------+
| rdtsc()              | ~5 ns         | Ultra-fast, CPU cycles (not time)   |
+----------------------+---------------+-------------------------------------+

4.4 Timekeeping and NTP
================================================================================

**System Time Adjustment**:

The kernel maintains system time and adjusts it via:
- NTP (Network Time Protocol) daemon
- PPS (Pulse Per Second) signals
- Manual adjustments (settimeofday, clock_settime)

**Timekeeping Flow**:

.. code-block:: text

    Hardware Clocksource (TSC, HPET)
            ↓
    Read counter value
            ↓
    Convert to nanoseconds (mult/shift)
            ↓
    Apply NTP adjustments (frequency correction)
            ↓
    Update xtime (CLOCK_REALTIME)
    Update monotonic_time (CLOCK_MONOTONIC)

**NTP Tuning**:

.. code-block:: bash

    # Check NTP status
    timedatectl status
    
    # View timekeeping statistics
    cat /proc/timer_list | grep -i "offset\|mult\|shift"

================================================================================
Section 5: Clockevents and Timer Interrupts
================================================================================

5.1 Clockevent Concept
================================================================================

**What are Clockevents?**

Clockevents are programmable timer hardware that generate interrupts:
- Schedule timer interrupts at specific times
- Support periodic or one-shot modes
- Used for scheduling tick, hrtimer expiration, NOHZ idle

**struct clock_event_device**:

.. code-block:: c

    struct clock_event_device {
        void (*event_handler)(struct clock_event_device *);
        int (*set_next_event)(unsigned long evt, struct clock_event_device *);
        int (*set_state_oneshot)(struct clock_event_device *);
        int (*set_state_periodic)(struct clock_event_device *);
        int (*set_state_shutdown)(struct clock_event_device *);
        
        u64         min_delta_ns;     // Minimum delta nanoseconds
        u64         max_delta_ns;     // Maximum delta nanoseconds
        unsigned long   mult;
        u32         shift;
        unsigned int    rating;
        const char  *name;            // "lapic", "hpet", etc.
        // ... more fields ...
    };

**Common Clockevent Devices (x86)**:

+-------------------+-----------+------------------+-----------------------------+
| **Name**          | **Rating**| **Mode**         | **Notes**                   |
+===================+===========+==================+=============================+
| Local APIC Timer  | 100-110   | Periodic/oneshot | Per-CPU, integrated         |
+-------------------+-----------+------------------+-----------------------------+
| HPET              | 100       | Periodic/oneshot | Global, high precision      |
+-------------------+-----------+------------------+-----------------------------+
| PIT (i8254)       | 50        | Periodic only    | Legacy, slow                |
+-------------------+-----------+------------------+-----------------------------+

5.2 Clockevent Modes
================================================================================

**Periodic Mode**:

.. code-block:: c

    // Timer fires at fixed intervals
    // Used for: Regular scheduling tick (HZ times per second)
    
    static int apic_set_state_periodic(struct clock_event_device *evt)
    {
        // Program APIC to fire every (1/HZ) seconds
        lapic_timer_set_periodic();
        return 0;
    }

**One-Shot Mode**:

.. code-block:: c

    // Timer fires once at programmed time
    // Used for: hrtimers, tickless idle, dynamic tick
    
    static int apic_set_next_event(unsigned long delta,
                                    struct clock_event_device *evt)
    {
        // Program APIC to fire after 'delta' cycles
        lapic_timer_set_oneshot(delta);
        return 0;
    }

**Shutdown Mode**:

.. code-block:: c

    // Timer disabled
    // Used for: CPU offline, deep idle states
    
    static int apic_set_state_shutdown(struct clock_event_device *evt)
    {
        lapic_timer_disable();
        return 0;
    }

5.3 Tick Device and Event Handler
================================================================================

**Tick Device**:

Each CPU has a tick device that generates periodic/one-shot timer interrupts:

.. code-block:: c

    struct tick_device {
        struct clock_event_device *evtdev;  // Underlying hardware
        enum tick_device_mode mode;         // TICKDEV_MODE_PERIODIC or ONESHOT
    };

**Event Handler Flow**:

.. code-block:: text

    Hardware Timer Interrupt
            ↓
    clock_event_device->event_handler()
            ↓
    tick_handle_periodic() [Periodic mode]
    or
    tick_sched_timer() [One-shot/NOHZ mode]
            ↓
    update_process_times()
    ├── account_process_tick()    (CPU time accounting)
    ├── run_local_timers()        (Expire timer_list timers)
    ├── rcu_check_callbacks()     (RCU processing)
    ├── scheduler_tick()          (Process scheduling)
    └── run_posix_cpu_timers()    (POSIX timers)

**Tick Handler Code**:

.. code-block:: c

    // Periodic tick handler
    static void tick_handle_periodic(struct clock_event_device *dev)
    {
        ktime_t next;
        
        tick_periodic(cpu);  // Do tick work
        
        if (dev->state != CLOCK_EVT_STATE_ONESHOT)
            return;
        
        // Reprogram for next tick
        for (;;) {
            next = ktime_add(dev->next_event, tick_period);
            if (!clockevents_program_event(dev, next, false))
                return;
            tick_periodic(cpu);
        }
    }

5.4 Viewing Clockevent Devices
================================================================================

.. code-block:: bash

    # List all clock event devices
    cat /proc/timer_list
    
    # Example output (per-CPU):
    # Tick Device: mode:     1  # 0=periodic, 1=oneshot
    # Per CPU device: 0
    # Clock Event Device: lapic
    #  max_delta_ns:   807385544844
    #  min_delta_ns:   1000
    #  mult:           43980466
    #  shift:          32
    #  mode:           3  # CLOCK_EVT_STATE_ONESHOT
    #  next_event:     12854837500000 nsecs
    #  set_next_event: lapic_next_event
    #  event_handler:  hrtimer_interrupt

================================================================================
Section 6: Tickless Kernels (NO_HZ)
================================================================================

6.1 NO_HZ Overview
================================================================================

**Traditional Tick Behavior**:

.. code-block:: text

    CPU busy:   [task] [task] [task] [task] [task]
                   ↑      ↑      ↑      ↑      ↑
    Timer tick:    T      T      T      T      T  (every 1/HZ seconds)
    
    CPU idle:   [idle] [idle] [idle] [idle] [idle]
                   ↑      ↑      ↑      ↑      ↑
    Timer tick:    T      T      T      T      T  (wakes CPU for no reason!)

**Problem**: Periodic tick wakes idle CPUs, wastes power, prevents deep C-states.

**NO_HZ Solution**: Stop tick when CPU is idle or running single task.

**NO_HZ Variants**:

+---------------------+-------------------------+----------------------------------+
| **Config**          | **Behavior**            | **Use Case**                     |
+=====================+=========================+==================================+
| CONFIG_HZ_PERIODIC  | Always tick             | Servers, legacy                  |
+---------------------+-------------------------+----------------------------------+
| CONFIG_NO_HZ_IDLE   | Stop tick when idle     | Desktops, laptops (power saving) |
+---------------------+-------------------------+----------------------------------+
| CONFIG_NO_HZ_FULL   | Stop tick when 1 task   | Real-time, HPC (low latency)     |
+---------------------+-------------------------+----------------------------------+

6.2 NO_HZ_IDLE (Dynamic Ticks)
================================================================================

**Behavior**:

When CPU goes idle:
1. Determine next timer expiration
2. Program clockevent in one-shot mode
3. Enter idle state (C-state)
4. Wake up at next timer or interrupt

.. code-block:: c

    // Simplified idle loop
    void cpu_idle_loop(void)
    {
        while (1) {
            while (!need_resched()) {
                // Stop tick if possible
                tick_nohz_idle_enter();
                
                // Enter idle state
                cpuidle_idle_call();
                
                // Restart tick
                tick_nohz_idle_exit();
            }
            schedule();
        }
    }

**Benefits**:
- Reduces power consumption (fewer wakeups, deeper C-states)
- Extends laptop battery life
- Improves virtualization (fewer vmexits)

**Checking NO_HZ_IDLE**:

.. code-block:: bash

    # Check kernel config
    grep CONFIG_NO_HZ_IDLE /boot/config-$(uname -r)
    # CONFIG_NO_HZ_IDLE=y
    
    # View idle statistics
    cat /proc/timer_list | grep -A5 "idle"
    # idle_waketime  : 4295059100 nsecs
    # idle_sleeptime : 58392840000 nsecs

6.3 NO_HZ_FULL (Tickless Single-Task)
================================================================================

**Concept**:

Stop tick when only 1 task running on CPU:
- Real-time task with no interruptions
- Eliminate scheduling latency from tick
- Used in HPC, real-time audio/video, low-latency trading

**Kernel Configuration**:

.. code-block:: bash

    # Kernel config
    CONFIG_NO_HZ_FULL=y
    
    # Isolate CPUs at boot (e.g., CPUs 2-7)
    nohz_full=2-7 isolcpus=2-7 rcu_nocbs=2-7
    
    # nohz_full: CPUs eligible for full tickless
    # isolcpus: Exclude from load balancing
    # rcu_nocbs: RCU callbacks offloaded to housekeeping CPUs

**Runtime Check**:

.. code-block:: bash

    # Check isolated CPUs
    cat /sys/devices/system/cpu/nohz_full
    # 2-7
    
    # Check if CPU is tickless
    cat /proc/timer_list | grep "tick stopped"
    # .nohz_mode                  : 2  # NOHZ_MODE_INACTIVE (0), LOWRES (1), HIGHRES (2)
    # nohz next event = 18446744073709551615 ns  # Max value = tick stopped

**Application Usage**:

.. code-block:: c

    // Pin real-time task to isolated CPU
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(2, &cpuset);  // CPU 2 isolated
    sched_setaffinity(0, sizeof(cpuset), &cpuset);
    
    // Set real-time priority
    struct sched_param param;
    param.sched_priority = 99;
    sched_setscheduler(0, SCHED_FIFO, &param);
    
    // Now runs without tick interruptions!

**Limitations**:
- Requires careful tuning (RCU, timers, workqueues)
- Not all tasks benefit (CPU-bound computation)
- Housekeeping CPU still handles system tasks

6.4 Tick Skew and Compensation
================================================================================

**Tick Skew Problem**:

When tick stops and restarts, time accounting must compensate:

.. code-block:: c

    // Example: CPU idle for 10 seconds
    // Old jiffies: 100,000
    // Resume from idle: jiffies should be 100,000 + (10s * HZ) = 101,000
    
    // Kernel compensates during tick_nohz_idle_exit():
    void tick_nohz_idle_exit(void)
    {
        ktime_t now = ktime_get();
        ktime_t idle_time = ktime_sub(now, ts->idle_entrytime);
        
        // Update statistics
        update_ts_time_stats(cpu, ts, now, idle_time);
        
        // Restart tick
        tick_nohz_restart(ts, now);
    }

**Accounting**:

.. code-block:: bash

    # View per-CPU idle time
    cat /proc/stat
    # cpu0 123456 789 234567 98765432 ...
    #      ^user  ^sys      ^idle (jiffies)

================================================================================
Section 7: POSIX Clocks and Timers (User Space)
================================================================================

7.1 POSIX Clock Types
================================================================================

**clock_gettime() Clocks**:

.. code-block:: c

    #include <time.h>
    
    struct timespec ts;
    
    // Wall-clock time (affected by NTP, settimeofday)
    clock_gettime(CLOCK_REALTIME, &ts);
    
    // Monotonic time (never goes backwards)
    clock_gettime(CLOCK_MONOTONIC, &ts);
    
    // Monotonic time including suspend
    clock_gettime(CLOCK_BOOTTIME, &ts);
    
    // Process CPU time
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    
    // Thread CPU time
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);

**Clock Comparison**:

+----------------------------+-----------------+-------------------+
| **Clock**                  | **NTP Adjusted**| **Suspend**       |
+============================+=================+===================+
| CLOCK_REALTIME             | Yes             | Stopped           |
+----------------------------+-----------------+-------------------+
| CLOCK_MONOTONIC            | No              | Stopped           |
+----------------------------+-----------------+-------------------+
| CLOCK_BOOTTIME             | No              | Continues         |
+----------------------------+-----------------+-------------------+
| CLOCK_PROCESS_CPUTIME_ID   | No              | N/A               |
+----------------------------+-----------------+-------------------+

7.2 POSIX Timers
================================================================================

**timer_create() API**:

.. code-block:: c

    #include <signal.h>
    #include <time.h>
    
    timer_t timerid;
    struct sigevent sev;
    struct itimerspec its;
    
    // Create timer
    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGRTMIN;
    sev.sigev_value.sival_ptr = &timerid;
    
    if (timer_create(CLOCK_MONOTONIC, &sev, &timerid) == -1) {
        perror("timer_create");
        exit(1);
    }
    
    // Set timer (1 second initial, 500 ms periodic)
    its.it_value.tv_sec = 1;
    its.it_value.tv_nsec = 0;
    its.it_interval.tv_sec = 0;
    its.it_interval.tv_nsec = 500000000;  // 500 ms
    
    if (timer_settime(timerid, 0, &its, NULL) == -1) {
        perror("timer_settime");
        exit(1);
    }
    
    // Wait for signals...
    
    // Delete timer
    timer_delete(timerid);

**Timer Notification Methods**:

.. code-block:: c

    // 1. Signal notification
    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGRTMIN;
    
    // 2. Thread notification
    sev.sigev_notify = SIGEV_THREAD;
    sev.sigev_notify_function = timer_thread_func;
    sev.sigev_notify_attributes = NULL;
    
    // 3. No notification
    sev.sigev_notify = SIGEV_NONE;
    // Must poll with timer_gettime()

7.3 timerfd (Linux-Specific)
================================================================================

**timerfd_create() API**:

.. code-block:: c

    #include <sys/timerfd.h>
    #include <poll.h>
    
    // Create timer file descriptor
    int tfd = timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK);
    if (tfd == -1) {
        perror("timerfd_create");
        exit(1);
    }
    
    // Set timer (500 ms initial, 100 ms periodic)
    struct itimerspec its;
    its.it_value.tv_sec = 0;
    its.it_value.tv_nsec = 500000000;
    its.it_interval.tv_sec = 0;
    its.it_interval.tv_nsec = 100000000;
    
    if (timerfd_settime(tfd, 0, &its, NULL) == -1) {
        perror("timerfd_settime");
        exit(1);
    }
    
    // Wait for timer with poll/epoll
    struct pollfd pfd;
    pfd.fd = tfd;
    pfd.events = POLLIN;
    
    while (1) {
        int ret = poll(&pfd, 1, -1);
        if (ret > 0 && pfd.revents & POLLIN) {
            uint64_t expirations;
            read(tfd, &expirations, sizeof(expirations));
            printf("Timer expired %llu times\n", expirations);
        }
    }
    
    close(tfd);

**Benefits of timerfd**:
- Integrates with poll/epoll event loops
- No signals required
- Multiple timers per process
- File descriptor can be passed between processes

================================================================================
Section 8: Exam Question (18 Points)
================================================================================

**Question**: Design and implement a kernel module that demonstrates time management concepts.

**Part A (6 points)**: Implement a module with:
1. A low-resolution timer (timer_list) that fires every 5 seconds
2. A high-resolution timer (hrtimer) that fires every 100 milliseconds
3. Proper initialization and cleanup

**Part B (4 points)**: In the timer callbacks:
1. Print current time using jiffies, ktime_get(), and ktime_get_real()
2. Demonstrate jiffies wraparound safety with time_after() macro
3. Calculate elapsed time since module load

**Part C (4 points)**: Add module parameters to:
1. Configure timer intervals dynamically
2. Switch between CLOCK_MONOTONIC and CLOCK_REALTIME for hrtimer
3. Enable/disable periodic mode for hrtimer

**Part D (4 points)**: Implement performance measurement:
1. Measure hrtimer callback execution time
2. Calculate jitter (difference between expected and actual fire time)
3. Export statistics via /proc or sysfs

**Answer**:

.. code-block:: c

    #include <linux/module.h>
    #include <linux/kernel.h>
    #include <linux/timer.h>
    #include <linux/hrtimer.h>
    #include <linux/ktime.h>
    #include <linux/proc_fs.h>
    #include <linux/seq_file.h>
    
    // Module parameters
    static unsigned int lowres_interval_ms = 5000;  // 5 seconds
    module_param(lowres_interval_ms, uint, 0644);
    
    static unsigned int hires_interval_ms = 100;    // 100 ms
    module_param(hires_interval_ms, uint, 0644);
    
    static int use_realtime = 0;  // 0=MONOTONIC, 1=REALTIME
    module_param(use_realtime, int, 0644);
    
    static int hrtimer_periodic = 1;  // 1=periodic, 0=one-shot
    module_param(hrtimer_periodic, int, 0644);
    
    // Timers
    static struct timer_list lowres_timer;
    static struct hrtimer hires_timer;
    
    // Statistics
    static ktime_t module_start_time;
    static u64 hrtimer_count = 0;
    static u64 lowres_count = 0;
    static u64 total_jitter_ns = 0;
    static u64 max_jitter_ns = 0;
    static ktime_t expected_fire_time;
    
    // Part A & B: Low-resolution timer callback
    static void lowres_timer_callback(struct timer_list *t)
    {
        unsigned long now_jiffies = jiffies;
        ktime_t now_ktime = ktime_get();
        ktime_t now_real = ktime_get_real();
        ktime_t elapsed = ktime_sub(now_ktime, module_start_time);
        
        pr_info("=== Low-Res Timer Fired ===\n");
        pr_info("  jiffies:         %lu\n", now_jiffies);
        pr_info("  ktime_get:       %lld ns\n", ktime_to_ns(now_ktime));
        pr_info("  ktime_get_real:  %lld ns\n", ktime_to_ns(now_real));
        pr_info("  Elapsed:         %lld ms\n", ktime_to_ms(elapsed));
        pr_info("  Fires:           %llu\n", ++lowres_count);
        
        // Demonstrate time_after for wraparound safety
        unsigned long future = now_jiffies + msecs_to_jiffies(1000);
        if (time_after(future, now_jiffies)) {
            pr_info("  time_after check: OK (future > now)\n");
        }
        
        // Re-arm timer
        mod_timer(&lowres_timer, jiffies + msecs_to_jiffies(lowres_interval_ms));
    }
    
    // Part A, B, D: High-resolution timer callback
    static enum hrtimer_restart hires_timer_callback(struct hrtimer *timer)
    {
        ktime_t now = ktime_get();
        ktime_t callback_start = now;
        ktime_t elapsed = ktime_sub(now, module_start_time);
        
        // Part D: Calculate jitter
        s64 jitter_ns = 0;
        if (hrtimer_count > 0) {
            jitter_ns = ktime_to_ns(ktime_sub(now, expected_fire_time));
            jitter_ns = (jitter_ns < 0) ? -jitter_ns : jitter_ns;  // Absolute value
            total_jitter_ns += jitter_ns;
            if (jitter_ns > max_jitter_ns)
                max_jitter_ns = jitter_ns;
        }
        
        pr_info("=== High-Res Timer Fired ===\n");
        pr_info("  ktime:    %lld ns\n", ktime_to_ns(now));
        pr_info("  Elapsed:  %lld ms\n", ktime_to_ms(elapsed));
        pr_info("  Fires:    %llu\n", ++hrtimer_count);
        pr_info("  Jitter:   %lld ns\n", jitter_ns);
        
        // Part D: Measure callback execution time
        ktime_t callback_end = ktime_get();
        s64 exec_time_ns = ktime_to_ns(ktime_sub(callback_end, callback_start));
        pr_info("  Exec time: %lld ns\n", exec_time_ns);
        
        // Part C: Periodic or one-shot
        if (hrtimer_periodic) {
            ktime_t interval = ms_to_ktime(hires_interval_ms);
            expected_fire_time = ktime_add(now, interval);
            hrtimer_forward(timer, now, interval);
            return HRTIMER_RESTART;
        } else {
            return HRTIMER_NORESTART;
        }
    }
    
    // Part D: /proc statistics
    static int stats_show(struct seq_file *m, void *v)
    {
        u64 avg_jitter = 0;
        if (hrtimer_count > 1)
            avg_jitter = total_jitter_ns / (hrtimer_count - 1);
        
        seq_printf(m, "Module Statistics\n");
        seq_printf(m, "=================\n");
        seq_printf(m, "Uptime:           %lld ms\n",
                   ktime_to_ms(ktime_sub(ktime_get(), module_start_time)));
        seq_printf(m, "Low-res fires:    %llu\n", lowres_count);
        seq_printf(m, "High-res fires:   %llu\n", hrtimer_count);
        seq_printf(m, "Avg jitter:       %llu ns\n", avg_jitter);
        seq_printf(m, "Max jitter:       %llu ns\n", max_jitter_ns);
        seq_printf(m, "HZ:               %d\n", HZ);
        seq_printf(m, "Current jiffies:  %lu\n", jiffies);
        
        return 0;
    }
    
    static int stats_open(struct inode *inode, struct file *file)
    {
        return single_open(file, stats_show, NULL);
    }
    
    static const struct proc_ops stats_ops = {
        .proc_open    = stats_open,
        .proc_read    = seq_read,
        .proc_lseek   = seq_lseek,
        .proc_release = single_release,
    };
    
    static int __init timer_module_init(void)
    {
        clockid_t clock_id = use_realtime ? CLOCK_REALTIME : CLOCK_MONOTONIC;
        
        pr_info("Timer module loaded\n");
        pr_info("  Low-res interval: %u ms\n", lowres_interval_ms);
        pr_info("  High-res interval: %u ms\n", hires_interval_ms);
        pr_info("  Clock: %s\n", use_realtime ? "REALTIME" : "MONOTONIC");
        pr_info("  HZ: %d\n", HZ);
        
        module_start_time = ktime_get();
        
        // Part A: Initialize low-resolution timer
        timer_setup(&lowres_timer, lowres_timer_callback, 0);
        mod_timer(&lowres_timer, jiffies + msecs_to_jiffies(lowres_interval_ms));
        
        // Part A & C: Initialize high-resolution timer
        hrtimer_init(&hires_timer, clock_id, HRTIMER_MODE_REL);
        hires_timer.function = hires_timer_callback;
        expected_fire_time = ktime_add(ktime_get(), ms_to_ktime(hires_interval_ms));
        hrtimer_start(&hires_timer, ms_to_ktime(hires_interval_ms), HRTIMER_MODE_REL);
        
        // Part D: Create /proc entry
        proc_create("timer_stats", 0444, NULL, &stats_ops);
        
        return 0;
    }
    
    static void __exit timer_module_exit(void)
    {
        // Part A: Cleanup timers
        del_timer_sync(&lowres_timer);
        hrtimer_cancel(&hires_timer);
        
        // Part D: Remove /proc entry
        remove_proc_entry("timer_stats", NULL);
        
        pr_info("Timer module unloaded\n");
        pr_info("  Total low-res fires:  %llu\n", lowres_count);
        pr_info("  Total high-res fires: %llu\n", hrtimer_count);
    }
    
    module_init(timer_module_init);
    module_exit(timer_module_exit);
    
    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Kernel Developer");
    MODULE_DESCRIPTION("Timer Management Demonstration");

**Testing**:

.. code-block:: bash

    # Compile and load module
    make
    sudo insmod timer_module.ko
    
    # Watch dmesg for timer fires
    sudo dmesg -w
    
    # View statistics
    cat /proc/timer_stats
    
    # Change parameters at runtime
    echo 2000 | sudo tee /sys/module/timer_module/parameters/lowres_interval_ms
    echo 50 | sudo tee /sys/module/timer_module/parameters/hires_interval_ms
    echo 1 | sudo tee /sys/module/timer_module/parameters/use_realtime
    
    # Unload
    sudo rmmod timer_module

**Expected Output**:

.. code-block:: text

    $ cat /proc/timer_stats
    Module Statistics
    =================
    Uptime:           45230 ms
    Low-res fires:    9
    High-res fires:   452
    Avg jitter:       1247 ns
    Max jitter:       5832 ns
    HZ:               250
    Current jiffies:  4295078945

================================================================================
Section 9: Best Practices & Key Takeaways
================================================================================

================================================================================
Section 9: Best Practices & Key Takeaways
================================================================================

**Timer Selection**:
✓ Use **timer_list** for low-resolution timeouts (>10 ms, less critical)
✓ Use **hrtimer** for precise timing (<10 ms, real-time, multimedia)
✓ Prefer **msleep()** for delays in process context (can sleep)
✓ Use **mdelay()** only in atomic context and keep delays <1 ms

**Time Reading**:
✓ Use **ktime_get()** for monotonic time (never goes backwards)
✓ Use **ktime_get_real()** for wall-clock time (user-facing timestamps)
✓ Use **ktime_get_coarse()** for frequent reads with lower precision requirements
✓ Never directly compare jiffies (use **time_after** macros to handle wraparound)

**Clocksource**:
✓ Prefer **TSC** if stable (modern CPUs usually OK)
✓ Use **HPET** for compatibility across systems
✓ Check `/sys/devices/system/clocksource/` for available/current clocksource
✓ Boot parameter `clocksource=hpet` if TSC unstable

**Performance**:
✓ Coarse clocks (ktime_get_coarse) for hot paths
✓ Batch timer expiration (use usleep_range instead of fixed usleep)
✓ Avoid busy-wait delays (mdelay) in non-critical code
✓ Periodic timers: use hrtimer_forward for drift-free operation

**Real-Time Systems**:
✓ Use hrtimers with CLOCK_MONOTONIC
✓ Avoid jitter: hrtimer_forward prevents drift accumulation
✓ NO_HZ_FULL for tickless operation on isolated CPUs
✓ CPU affinity for timer callbacks (avoid migration)

**Tickless Configuration**:
✓ CONFIG_NO_HZ_IDLE for power saving (laptops, desktops)
✓ CONFIG_NO_HZ_FULL for real-time (HPC, low-latency applications)
✓ Isolate CPUs: `nohz_full=2-7 isolcpus=2-7 rcu_nocbs=2-7`
✓ Pin real-time tasks to isolated CPUs with sched_setaffinity

**Common Pitfalls**:
❌ Direct jiffy comparison (use time_after macros)
❌ Long mdelay() calls (blocks CPU, use msleep instead)
❌ Ignoring jiffy wraparound (49 days on 32-bit systems)
❌ Using timer_list for <1 ms precision (use hrtimer)
❌ Sleeping in atomic context (spinlock, IRQ handler)
❌ Assuming CLOCK_REALTIME is monotonic (can jump backward)
❌ Forgetting del_timer_sync in module exit (callback may still run)
❌ Using hrtimer_cancel from callback (use return HRTIMER_NORESTART)

**POSIX Clocks (User Space)**:
✓ CLOCK_MONOTONIC for elapsed time measurement (intervals, timeouts)
✓ CLOCK_REALTIME for wall-clock timestamps (logs, user-facing times)
✓ CLOCK_BOOTTIME for timers that should fire after suspend
✓ timerfd for event-loop integration (poll/epoll)

**Debugging Time Issues**:
✓ Check `/proc/timer_list` for detailed timer state
✓ Check `/sys/devices/system/clocksource/` for clocksource selection
✓ Use `trace-cmd` to trace timer events (timer_start, timer_expire)
✓ Monitor jitter with perf or ftrace
✓ Check `cat /proc/interrupts | grep timer` for timer interrupt count

**Power Efficiency**:
✓ Use NO_HZ_IDLE to reduce idle wakeups
✓ Batch timers (use usleep_range instead of precise usleep)
✓ Align timers to reduce wakeups (round_jiffies, hrtimer timer slack)
✓ Prefer deferred work when exact timing not critical

**Key Takeaways**:

**Core Concepts**:
✓ **jiffies**: Global counter incremented every timer tick (HZ times/second)
  - Resolution: 1-10 ms depending on HZ (100, 250, 1000)
  - Wraparound: 32-bit wraps every ~49 days, use time_after macros
  - Conversion: msecs_to_jiffies(), jiffies_to_msecs()

✓ **timer_list**: Low-resolution timers based on jiffies
  - API: timer_setup(), mod_timer(), del_timer_sync()
  - Use for: Timeouts, periodic tasks (>10 ms)
  - Overhead: Low (processed at tick interrupt)

✓ **hrtimer**: High-resolution timers with nanosecond precision
  - API: hrtimer_init(), hrtimer_start(), hrtimer_cancel()
  - Use for: Precise timing, real-time, multimedia (<10 ms)
  - Periodic: Use hrtimer_forward() to avoid drift

✓ **ktime_t**: Nanosecond time representation (64-bit signed)
  - Construction: ms_to_ktime(), us_to_ktime(), ns_to_ktime()
  - Reading: ktime_get() (monotonic), ktime_get_real() (wall-clock)
  - Conversion: ktime_to_ns(), ktime_to_us(), ktime_to_ms()

**Hardware Abstractions**:
✓ **Clocksource**: Hardware providing monotonic time measurement
  - Examples: TSC (CPU counter), HPET, ACPI PM timer
  - Rating: Higher is better (TSC=300, HPET=250)
  - Selection: /sys/devices/system/clocksource/

✓ **Clockevent**: Programmable hardware for timer interrupts
  - Examples: Local APIC, HPET, PIT
  - Modes: Periodic (fixed interval), One-shot (single event), Shutdown
  - Used by: Scheduling tick, hrtimer, NO_HZ

**Advanced Features**:
✓ **NO_HZ_IDLE**: Stop tick when CPU idle
  - Benefits: Power saving, deeper C-states, better battery life
  - Automatic: Kernel handles tick stop/restart transparently

✓ **NO_HZ_FULL**: Stop tick when single task running
  - Benefits: Eliminate scheduling jitter, ultra-low latency
  - Configuration: nohz_full=2-7 isolcpus=2-7 rcu_nocbs=2-7
  - Use case: Real-time, HPC, low-latency trading

✓ **POSIX Clocks**: User-space time interfaces
  - CLOCK_MONOTONIC: Never goes backward (elapsed time)
  - CLOCK_REALTIME: Wall-clock (can jump, NTP adjusted)
  - CLOCK_BOOTTIME: Monotonic + suspend time
  - API: clock_gettime(), timer_create(), timerfd_create()

**Decision Trees**:

**Timer Selection**:
```
Need precise timing (<1 ms)?
├── Yes → Use hrtimer
│   └── Periodic? Use hrtimer_forward()
└── No → Use timer_list
    └── Periodic? mod_timer() in callback
```

**Delay Selection**:
```
Can sleep (process context)?
├── No (atomic context) → Use mdelay/udelay (keep <1 ms!)
└── Yes
    ├── Delay > 10 ms? → Use msleep()
    └── Delay < 10 ms? → Use usleep_range(min, max)
```

**Clock Selection**:
```
Purpose?
├── Elapsed time / timeouts → CLOCK_MONOTONIC (ktime_get)
├── User timestamps / logs → CLOCK_REALTIME (ktime_get_real)
├── Timers across suspend → CLOCK_BOOTTIME (ktime_get_boottime)
└── Hot path / frequent reads → ktime_get_coarse()
```

**Historical Evolution**:
1. **Linux 2.4**: Only jiffies and timer_list (HZ=100)
2. **Linux 2.6.16** (2006): hrtimers introduced for nanosecond precision
3. **Linux 2.6.21** (2007): NO_HZ_IDLE (dynticks) for power saving
4. **Linux 3.10** (2013): NO_HZ_FULL for real-time workloads
5. **Linux 4.8** (2016): timerfd improvements, better slack handling
6. **Modern kernels**: TSC as default clocksource on stable CPUs

**Real-World Use Cases**:

**Multimedia (Audio/Video)**:
- Use hrtimer with CLOCK_MONOTONIC for frame/sample timing
- hrtimer_forward for drift-free periodic callbacks
- NO_HZ_FULL for isolated playback threads

**Networking**:
- timer_list for TCP retransmission timeouts (second-scale)
- hrtimer for precise packet pacing (sub-millisecond)
- NO_HZ_IDLE to reduce wakeups on idle servers

**Embedded/Real-Time**:
- CONFIG_HZ=1000 for better responsiveness
- hrtimer for control loops (PID controllers, motor control)
- NO_HZ_FULL on isolated CPUs for deterministic latency

**Power Management**:
- NO_HZ_IDLE to allow deeper C-states
- usleep_range to batch wakeups
- round_jiffies to align timer expiration

**Common Misconceptions**:
❌ "HZ=1000 is always better" → Higher HZ = more overhead, not always needed
❌ "ktime_get never fails" → Can be expensive on some architectures
❌ "timer_list is deprecated" → Still perfectly valid for low-res timers
❌ "NO_HZ_FULL eliminates all interrupts" → Only eliminates tick, not other IRQs
❌ "CLOCK_REALTIME is safe for timeouts" → Can jump backward (NTP), use MONOTONIC

**Performance Tips**:
✓ Cache ktime_get() results if called multiple times in same function
✓ Use ktime_get_coarse() for logs, statistics (10x faster than ktime_get)
✓ Batch timer expiration (round_jiffies for low-priority timers)
✓ Pin hrtimer callbacks to specific CPUs to avoid cache misses
✓ Use timer slack (hrtimer_set_expires_range) to batch wakeups

**References**:
- Documentation/timers/timers-howto.rst
- Documentation/timers/hrtimers.rst
- Documentation/timers/no_hz.rst
- Documentation/timers/timekeeping.rst
- "Professional Linux Kernel Architecture" - Wolfgang Mauerer, Chapter 15
- "Linux Kernel Development" (3rd Edition) - Robert Love, Chapter 11
- https://www.kernel.org/doc/html/latest/core-api/timekeeping.html

================================================================================
End of Document
================================================================================


