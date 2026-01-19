================================================================================
Embedded Linux: Real-Time Programming - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch12)
:Target: PREEMPT_RT, Real-Time Scheduling, Latency Analysis
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**PREEMPT_RT Kernel:**

.. code-block:: bash

   # Kernel config
   CONFIG_PREEMPT_RT=y
   CONFIG_HIGH_RES_TIMERS=y
   CONFIG_NO_HZ_FULL=y
   CONFIG_RCU_NOCB_CPU=y
   
   # Kernel parameters
   isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3

**Real-Time Scheduling:**

.. code-block:: bash

   # Set RT priority
   chrt -f -p 80 <pid>                # SCHED_FIFO, priority 80
   chrt -r -p 80 <pid>                # SCHED_RR
   chrt -f 80 ./myapp                 # Start with RT priority
   
   # View scheduling policy
   chrt -p <pid>
   ps -eo pid,cls,rtprio,cmd

**Latency Testing:**

.. code-block:: bash

   # cyclictest (primary tool)
   cyclictest -p 80 -t4 -n -i 1000 -l 100000
   
   # Options:
   # -p: RT priority
   # -t: Number of threads
   # -n: Use clock_nanosleep
   # -i: Interval (microseconds)
   # -l: Loops
   # -m: Lock memory
   # -a: CPU affinity

**Interrupt Latency:**

.. code-block:: bash

   # hwlatdetect
   hwlatdetect --duration=60
   
   # /proc/sys/kernel/hung_task_timeout_secs
   echo 0 > /proc/sys/kernel/hung_task_timeout_secs

================================================================================
1. Real-Time Basics
================================================================================

1.1 Real-Time Concepts
-----------------------

**Definitions:**

.. code-block:: text

   Hard Real-Time:
   - Deadlines must NEVER be missed
   - Missing deadline = system failure
   - Examples: airbag control, industrial safety
   
   Firm Real-Time:
   - Occasional deadline misses tolerated
   - Result useless if late
   - Examples: video streaming, telecom
   
   Soft Real-Time:
   - Deadline misses degrade quality
   - Late results still useful
   - Examples: audio playback, user interfaces
   
   Determinism:
   - Predictable, bounded response times
   - Low latency variance (jitter)
   - Reproducible behavior

**Latency Types:**

.. code-block:: text

   Interrupt Latency:
   - Time from hardware interrupt to ISR
   - Hardware + kernel interrupt handling
   
   Scheduling Latency:
   - Time from wakeup to thread execution
   - Affected by priority, preemption
   
   End-to-End Latency:
   - Total time from event to response
   - Interrupt + scheduling + processing

1.2 Standard Linux Limitations
-------------------------------

**Non-RT Limitations:**

.. code-block:: text

   Problems:
   ✗ Long non-preemptible sections
   ✗ Interrupt handlers block other tasks
   ✗ Spinlocks disable preemption
   ✗ Priority inversion
   ✗ Unpredictable latencies
   
   Mitigations (CONFIG_PREEMPT):
   ✓ Voluntary preemption points
   ✓ Lower latency vs throughput
   ✓ Still not deterministic
   
   Use Cases:
   - Desktop Linux
   - Server workloads
   - Soft real-time (audio, video)

================================================================================
2. PREEMPT_RT Patch
================================================================================

2.1 PREEMPT_RT Features
------------------------

**Key Improvements:**

.. code-block:: text

   1. Fully Preemptible Kernel
      - Most kernel code can be preempted
      - Critical sections minimized
   
   2. Interrupt Threading
      - IRQ handlers run as threads
      - Prioritized like other tasks
      - Can be preempted
   
   3. Priority Inheritance
      - Prevents priority inversion
      - Mutex supports PI protocol
   
   4. High-Resolution Timers
      - Microsecond precision
      - Better timer accuracy
   
   5. Lockless Algorithms
      - Reduced lock contention
      - RCU, per-CPU variables

**PREEMPT_RT vs Standard:**

.. code-block:: text

   Feature                Standard    PREEMPT_RT
   =============================================
   Preemption model       Voluntary   Fully preemptible
   IRQ handling           In-context  Threaded
   Spinlocks              Disable PM  RT mutex
   Priority inheritance   No          Yes
   Typical worst latency  100-500 µs  10-50 µs
   Throughput             Higher      Lower

2.2 Building PREEMPT_RT Kernel
-------------------------------

**Kernel Configuration:**

.. code-block:: bash

   # Core RT config
   CONFIG_PREEMPT_RT=y
   CONFIG_PREEMPT_RT_FULL=y
   CONFIG_HIGH_RES_TIMERS=y
   CONFIG_NO_HZ_FULL=y
   CONFIG_NO_HZ=y
   CONFIG_HZ_1000=y
   
   # CPU isolation
   CONFIG_RCU_NOCB_CPU=y
   CONFIG_IRQ_FORCED_THREADING=y
   
   # Disable conflicting options
   # CONFIG_CPU_FREQ is not set
   # CONFIG_CPU_IDLE is not set
   # CONFIG_ACPI_PROCESSOR is not set

**Download and Patch:**

.. code-block:: bash

   # Get kernel
   wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.tar.xz
   tar xf linux-5.10.tar.xz
   cd linux-5.10
   
   # Get RT patch
   wget https://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/patch-5.10-rt.patch.xz
   xzcat ../patch-5.10-rt.patch.xz | patch -p1
   
   # Configure
   make menuconfig
   # General Setup -> Preemption Model -> Fully Preemptible Kernel (RT)
   
   # Build
   make -j$(nproc)
   make modules_install
   make install

2.3 Runtime Configuration
--------------------------

**Kernel Command Line:**

.. code-block:: bash

   # CPU isolation
   isolcpus=2,3              # Isolate CPUs 2-3
   nohz_full=2,3             # Tickless for CPUs 2-3
   rcu_nocbs=2,3             # Offload RCU callbacks
   
   # IRQ affinity
   irqaffinity=0,1           # Pin IRQs to CPUs 0-1
   
   # High-res timers
   highres=on
   nohz=on
   
   # Disable
   intel_pstate=disable      # Disable CPU freq scaling
   nosoftlockup              # Disable softlockup detector

**Runtime Tuning:**

.. code-block:: bash

   # IRQ threading (force all IRQs threaded)
   echo 1 > /proc/sys/kernel/threadirqs
   
   # Move IRQs away from RT CPUs
   for i in /proc/irq/*/smp_affinity; do
       echo 3 > $i  # CPUs 0-1 only (0x3 = 0b0011)
   done
   
   # Check threaded IRQs
   ps aux | grep "\[irq/"

================================================================================
3. Real-Time Scheduling
================================================================================

3.1 Scheduling Policies
------------------------

**RT Policies:**

.. code-block:: c

   // SCHED_FIFO (First-In-First-Out)
   struct sched_param param;
   param.sched_priority = 80;
   sched_setscheduler(0, SCHED_FIFO, &param);
   
   // SCHED_RR (Round-Robin)
   param.sched_priority = 80;
   sched_setscheduler(0, SCHED_RR, &param);
   
   // Priority range: 1-99 (99 = highest)

**chrt Tool:**

.. code-block:: bash

   # Set SCHED_FIFO
   chrt -f -p 80 <pid>
   chrt -f 80 ./myapp
   
   # Set SCHED_RR
   chrt -r -p 80 <pid>
   
   # Set time slice (RR only)
   chrt -r -p 80 <pid> -t 10000  # 10ms
   
   # View policy
   chrt -p <pid>
   
   # View all RT tasks
   ps -eo pid,cls,rtprio,cmd | grep -E 'FF|RR'

3.2 Priority Inversion
-----------------------

**Problem:**

.. code-block:: text

   Scenario:
   Task H (high priority) waits for lock held by Task L (low priority)
   Task M (medium priority) preempts Task L
   Result: Task H indirectly waits for Task M (priority inversion)

**Solutions:**

.. code-block:: c

   // Priority inheritance mutexes
   pthread_mutexattr_t attr;
   pthread_mutex_t mutex;
   
   pthread_mutexattr_init(&attr);
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
   pthread_mutex_init(&mutex, &attr);
   
   // Priority ceiling
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_PROTECT);
   pthread_mutexattr_setprioceiling(&attr, 99);
   pthread_mutex_init(&mutex, &attr);

3.3 CPU Affinity
-----------------

**Bind to CPUs:**

.. code-block:: c

   // CPU affinity (isolate RT task)
   cpu_set_t cpuset;
   CPU_ZERO(&cpuset);
   CPU_SET(2, &cpuset);  // Use CPU 2
   CPU_SET(3, &cpuset);  // Use CPU 3
   
   pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);

**Command Line:**

.. code-block:: bash

   # taskset
   taskset -c 2,3 ./rt-app
   taskset -p -c 2 <pid>
   
   # View affinity
   taskset -p <pid>
   cat /proc/<pid>/status | grep Cpus_allowed

================================================================================
4. Memory Management
================================================================================

4.1 Memory Locking
-------------------

**Lock Memory:**

.. code-block:: c

   #include <sys/mman.h>
   
   // Lock all current and future pages
   mlockall(MCL_CURRENT | MCL_FUTURE);
   
   // Prefault stack
   unsigned char dummy[MAX_STACK_SIZE];
   memset(dummy, 0, MAX_STACK_SIZE);
   
   // Unlock
   munlockall();

**Command Line:**

.. code-block:: bash

   # Check locked memory
   cat /proc/<pid>/status | grep VmLck
   
   # Increase limit
   ulimit -l unlimited
   
   # /etc/security/limits.conf
   @realtime  -  memlock  unlimited

4.2 Memory Allocation
----------------------

**RT-Safe Allocation:**

.. code-block:: c

   // Pre-allocate all memory at startup
   void *pool = malloc(POOL_SIZE);
   mlockall(MCL_CURRENT | MCL_FUTURE);
   
   // Use custom allocator (no syscalls)
   // OR use static allocation
   static char buffer[BUFFER_SIZE];
   
   // AVOID in RT path:
   // - malloc/free (page faults)
   // - dynamic allocation
   // - file I/O

================================================================================
5. Latency Measurement
================================================================================

5.1 cyclictest
--------------

**Basic Test:**

.. code-block:: bash

   # Simple test
   cyclictest -p 80 -t1 -n -l 100000
   
   # Comprehensive test
   cyclictest \
       -p 80 \              # RT priority 80
       -t4 \                # 4 threads (one per CPU)
       -a 0,1,2,3 \         # CPU affinity
       -n \                 # Use clock_nanosleep
       -i 1000 \            # 1000 µs interval
       -l 1000000 \         # 1M loops
       -m \                 # Lock memory
       -q \                 # Quiet (summary only)
       -h 100 \             # Histogram with 100 µs buckets
       -b 1000              # Trace if latency > 1000 µs

**Stress Testing:**

.. code-block:: bash

   # Run with system load
   stress-ng --cpu 4 --io 2 --vm 2 --vm-bytes 128M &
   cyclictest -p 80 -t4 -n -i 1000 -l 100000 -q
   
   # Dedicated CPU
   taskset -c 2 cyclictest -p 80 -t1 -n -i 1000 -l 100000 -q

**Interpret Results:**

.. code-block:: text

   Output:
   T: 0 ( 1234) P:80 I:1000 C: 100000 Min:   2 Act:   4 Avg:   3 Max:  15
   
   Min: Best-case latency
   Avg: Average latency
   Max: Worst-case latency (most important for RT)
   
   Acceptable RT latency:
   - Excellent: Max < 100 µs
   - Good:      Max < 200 µs
   - Fair:      Max < 500 µs
   - Poor:      Max > 1000 µs

5.2 hwlatdetect
---------------

**Hardware Latency:**

.. code-block:: bash

   # Test for SMI latency
   hwlatdetect --duration=60 --threshold=10
   
   # Continuous monitoring
   hwlatdetect --duration=3600 --window=1000000 --width=500000
   
   # Check results
   # High latencies often due to:
   # - SMI (System Management Interrupts)
   # - Firmware/BIOS issues
   # - Hardware defects

5.3 Latency Histogram
---------------------

**Generate Histogram:**

.. code-block:: bash

   # cyclictest with histogram
   cyclictest -p 80 -t1 -n -i 1000 -l 100000 -h 200 -q > histogram.txt
   
   # Plot with gnuplot
   gnuplot << 'EOF'
   set terminal png
   set output "latency.png"
   set xlabel "Latency (us)"
   set ylabel "Count"
   plot "histogram.txt" using 1:2 with lines
   EOF

================================================================================
6. RT Application Programming
================================================================================

6.1 RT Thread Template
-----------------------

.. code-block:: c

   #include <pthread.h>
   #include <sched.h>
   #include <sys/mman.h>
   #include <time.h>
   
   #define RT_PRIORITY 80
   #define NSEC_PER_SEC 1000000000
   
   void *rt_thread(void *arg) {
       struct sched_param param;
       cpu_set_t cpuset;
       struct timespec next;
       
       // Set RT priority
       param.sched_priority = RT_PRIORITY;
       pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
       
       // Set CPU affinity
       CPU_ZERO(&cpuset);
       CPU_SET(2, &cpuset);
       pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);
       
       // Lock memory
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       // Initialize periodic timer
       clock_gettime(CLOCK_MONOTONIC, &next);
       
       while (1) {
           // Do RT work
           
           // Sleep until next period
           next.tv_nsec += 1000000; // 1ms
           while (next.tv_nsec >= NSEC_PER_SEC) {
               next.tv_nsec -= NSEC_PER_SEC;
               next.tv_sec++;
           }
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
       }
       
       return NULL;
   }
   
   int main() {
       pthread_t thread;
       
       // Pre-allocate memory
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       // Create RT thread
       pthread_create(&thread, NULL, rt_thread, NULL);
       pthread_join(thread, NULL);
       
       return 0;
   }

6.2 RT Best Practices
----------------------

**Do's:**

.. code-block:: text

   ✓ Lock all memory (mlockall)
   ✓ Pre-allocate all resources
   ✓ Use SCHED_FIFO or SCHED_RR
   ✓ Set CPU affinity
   ✓ Use clock_nanosleep (absolute time)
   ✓ Minimize critical section length
   ✓ Use priority inheritance mutexes
   ✓ Test under maximum load
   ✓ Monitor worst-case latency

**Don'ts:**

.. code-block:: text

   ✗ No dynamic allocation in RT path
   ✗ No file I/O, network I/O
   ✗ No printf/syslog
   ✗ No blocking system calls
   ✗ No page faults
   ✗ No unbounded loops
   ✗ No sleep/usleep (use clock_nanosleep)
   ✗ No regular mutexes (use PI mutexes)

================================================================================
7. Key Takeaways
================================================================================

.. code-block:: text

   PREEMPT_RT Kernel:
   ==================
   CONFIG_PREEMPT_RT=y
   CONFIG_HIGH_RES_TIMERS=y
   isolcpus=2,3 nohz_full=2,3
   
   RT Scheduling:
   ==============
   chrt -f 80 ./rt-app
   chrt -p 80 <pid>
   mlockall(MCL_CURRENT | MCL_FUTURE)
   CPU affinity to isolated CPUs
   
   Latency Testing:
   ================
   cyclictest -p 80 -t4 -n -i 1000 -l 100000 -q
   hwlatdetect --duration=60
   
   RT Programming:
   ===============
   - SCHED_FIFO priority
   - mlockall() memory
   - clock_nanosleep() for timing
   - No malloc/free in RT path
   - Priority inheritance mutexes
   - Pre-allocate all resources
   
   Target Latency:
   ===============
   Excellent: < 100 µs
   Good:      < 200 µs
   Acceptable: < 500 µs

================================================================================
END OF CHEATSHEET
================================================================================
