===================================
Linux Real-time Scheduling Guide
===================================

:Author: Embedded Linux Documentation
:Date: January 2026
:Version: 1.0
:Focus: Real-time scheduling policies, priorities, and CPU affinity

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Scheduling Commands
------------------------------

.. code-block:: bash

   # Set SCHED_FIFO priority
   chrt -f 80 ./my_app
   
   # Set SCHED_RR priority
   chrt -r 50 ./my_app
   
   # Set SCHED_DEADLINE
   chrt -d --sched-runtime 10000000 --sched-deadline 20000000 --sched-period 30000000 ./my_app
   
   # Change existing process
   chrt -f -p 90 1234
   
   # View process scheduling
   chrt -p 1234
   ps -eLo pid,tid,class,rtprio,pri,psr,comm
   
   # Set CPU affinity
   taskset -c 2,3 ./my_app
   taskset -p 0x0C 1234  # CPUs 2-3 (binary: 1100)
   
   # Set niceness (non-RT)
   nice -n -10 ./my_app
   renice -n -5 -p 1234

Quick RT Application Template
------------------------------

.. code-block:: c

   #include <pthread.h>
   #include <sched.h>
   #include <sys/mman.h>
   #include <stdio.h>
   #include <string.h>
   
   #define RT_PRIORITY 80
   #define STACK_SIZE 8192
   
   void *rt_thread(void *arg) {
       struct timespec ts;
       
       while (1) {
           // Real-time work here
           
           // Sleep with RT-safe function
           ts.tv_sec = 0;
           ts.tv_nsec = 1000000;  // 1ms
           clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, NULL);
       }
       return NULL;
   }
   
   int main() {
       pthread_t thread;
       pthread_attr_t attr;
       struct sched_param param;
       
       // Lock memory
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       // Pre-fault stack
       unsigned char dummy[STACK_SIZE];
       memset(dummy, 0, STACK_SIZE);
       
       // Configure thread attributes
       pthread_attr_init(&attr);
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       param.sched_priority = RT_PRIORITY;
       pthread_attr_setschedparam(&attr, &param);
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       // Create RT thread
       pthread_create(&thread, &attr, rt_thread, NULL);
       
       pthread_join(thread, NULL);
       return 0;
   }
   
   // Compile: gcc -o rt_app rt_app.c -pthread -lrt
   // Run: sudo chrt -f 80 ./rt_app

Scheduling Policies
===================

Overview
--------

.. code-block:: text

   Linux Scheduling Policies:
   
   Real-time (deterministic):
   1. SCHED_FIFO    - First-In-First-Out
   2. SCHED_RR      - Round-Robin
   3. SCHED_DEADLINE - Earliest Deadline First (EDF)
   
   Non-real-time (time-sharing):
   4. SCHED_OTHER   - Default CFS (Completely Fair Scheduler)
   5. SCHED_BATCH   - Batch processing
   6. SCHED_IDLE    - Very low priority
   
   Priority Range:
   - RT policies: 1-99 (higher = more important)
   - Non-RT: Nice values -20 to +19 (lower = more important)

SCHED_FIFO (First-In-First-Out)
--------------------------------

.. code-block:: text

   Characteristics:
   - Strict priority-based
   - Higher priority always preempts lower
   - No time slicing within same priority
   - Runs until blocks, yields, or preempted
   - Most common for real-time tasks
   
   Use Cases:
   - Critical real-time tasks
   - Fixed priority systems
   - Tasks with known execution patterns
   
   Behavior:
   Priority 99 task:  [========================================]
   Priority 80 task:                                           [====]
   Priority 50 task:                                                [==]
   
   Higher priority runs exclusively until done/blocked

SCHED_RR (Round-Robin)
-----------------------

.. code-block:: text

   Characteristics:
   - Similar to SCHED_FIFO
   - Adds time slicing for same priority
   - Default timeslice: 100ms
   - Good for multiple RT tasks at same priority
   
   Use Cases:
   - Multiple RT tasks of equal importance
   - Preventing CPU monopolization
   
   Behavior at same priority:
   Task A (RR 80): [===]     [===]     [===]
   Task B (RR 80):     [===]     [===]     [===]
   Task C (RR 80):         [===]     [===]

SCHED_DEADLINE (EDF)
--------------------

.. code-block:: text

   Characteristics:
   - Deadline-based scheduling
   - Earliest deadline runs first
   - Admission control (prevents overload)
   - Most advanced RT policy
   - Requires: runtime, deadline, period
   
   Parameters:
   - Runtime: Max execution time per period
   - Deadline: When task must complete
   - Period: How often task runs
   
   Use Cases:
   - Periodic real-time tasks
   - Mixed criticality systems
   - Deadline-driven applications
   
   Example:
   Task needs 10ms every 50ms with 30ms deadline
   Runtime=10ms, Deadline=30ms, Period=50ms

SCHED_OTHER (CFS)
-----------------

.. code-block:: text

   Characteristics:
   - Default scheduler
   - Completely Fair Scheduler (CFS)
   - Time-sharing, not real-time
   - Priority via nice values (-20 to +19)
   - Good for general workloads
   
   Use Cases:
   - Normal applications
   - Background tasks
   - Interactive desktop
   
   Priority: Lower nice value = higher priority
   nice -20: Highest priority
   nice   0: Default
   nice +19: Lowest priority

SCHED_BATCH
-----------

.. code-block:: text

   Characteristics:
   - Optimized for throughput
   - Less preemption
   - Good for CPU-intensive batch jobs
   - Won't preempt SCHED_OTHER
   
   Use Cases:
   - Batch processing
   - Scientific computing
   - Background compilation

SCHED_IDLE
----------

.. code-block:: text

   Characteristics:
   - Lowest possible priority
   - Only runs when nothing else wants CPU
   - Good for background maintenance
   
   Use Cases:
   - Indexing
   - Log processing
   - System maintenance

Setting Scheduling Policy
==========================

Using chrt Command
------------------

.. code-block:: bash

   # SCHED_FIFO with priority 80
   chrt -f 80 ./my_app
   
   # SCHED_RR with priority 60
   chrt -r 60 ./my_app
   
   # SCHED_OTHER (normal)
   chrt -o 0 ./my_app
   
   # SCHED_BATCH
   chrt -b 0 ./my_app
   
   # SCHED_IDLE
   chrt -i 0 ./my_app
   
   # SCHED_DEADLINE
   # runtime=10ms, deadline=30ms, period=50ms (all in nanoseconds)
   chrt -d --sched-runtime 10000000 \
            --sched-deadline 30000000 \
            --sched-period 50000000 ./my_app
   
   # Change running process
   chrt -f -p 90 1234
   
   # Query process scheduling
   chrt -p 1234
   # Output: pid 1234's current scheduling policy: SCHED_FIFO
   #         pid 1234's current scheduling priority: 90

Using C API
-----------

.. code-block:: c

   #include <sched.h>
   #include <stdio.h>
   #include <unistd.h>
   
   // Set SCHED_FIFO
   int set_fifo_priority(int priority) {
       struct sched_param param;
       param.sched_priority = priority;
       
       if (sched_setscheduler(0, SCHED_FIFO, &param) != 0) {
           perror("sched_setscheduler");
           return -1;
       }
       return 0;
   }
   
   // Set SCHED_RR
   int set_rr_priority(int priority) {
       struct sched_param param;
       param.sched_priority = priority;
       
       if (sched_setscheduler(0, SCHED_RR, &param) != 0) {
           perror("sched_setscheduler");
           return -1;
       }
       return 0;
   }
   
   // Get current policy
   void print_scheduling_info() {
       int policy = sched_getscheduler(0);
       struct sched_param param;
       sched_getparam(0, &param);
       
       printf("Policy: ");
       switch (policy) {
           case SCHED_FIFO:     printf("SCHED_FIFO\n"); break;
           case SCHED_RR:       printf("SCHED_RR\n"); break;
           case SCHED_OTHER:    printf("SCHED_OTHER\n"); break;
           case SCHED_BATCH:    printf("SCHED_BATCH\n"); break;
           case SCHED_IDLE:     printf("SCHED_IDLE\n"); break;
           case SCHED_DEADLINE: printf("SCHED_DEADLINE\n"); break;
           default:             printf("Unknown\n");
       }
       printf("Priority: %d\n", param.sched_priority);
   }

pthread Real-time Threads
-------------------------

.. code-block:: c

   #include <pthread.h>
   #include <sched.h>
   
   void *thread_function(void *arg) {
       // Thread work
       return NULL;
   }
   
   int create_rt_thread(pthread_t *thread, int priority) {
       pthread_attr_t attr;
       struct sched_param param;
       
       // Initialize attributes
       pthread_attr_init(&attr);
       
       // Set scheduling policy
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       
       // Set priority
       param.sched_priority = priority;
       pthread_attr_setschedparam(&attr, &param);
       
       // Use explicit scheduling (don't inherit)
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       // Create thread
       int ret = pthread_create(thread, &attr, thread_function, NULL);
       
       pthread_attr_destroy(&attr);
       return ret;
   }

SCHED_DEADLINE Configuration
-----------------------------

.. code-block:: c

   #include <sched.h>
   #include <sys/syscall.h>
   #include <unistd.h>
   
   #ifndef SCHED_DEADLINE
   #define SCHED_DEADLINE 6
   #endif
   
   struct sched_attr {
       uint32_t size;
       uint32_t sched_policy;
       uint64_t sched_flags;
       int32_t  sched_nice;
       uint32_t sched_priority;
       uint64_t sched_runtime;
       uint64_t sched_deadline;
       uint64_t sched_period;
   };
   
   int sched_setattr(pid_t pid, const struct sched_attr *attr, unsigned int flags) {
       return syscall(SYS_sched_setattr, pid, attr, flags);
   }
   
   int set_deadline_scheduling(uint64_t runtime_ns, uint64_t deadline_ns, uint64_t period_ns) {
       struct sched_attr attr = {0};
       attr.size = sizeof(attr);
       attr.sched_policy = SCHED_DEADLINE;
       attr.sched_runtime = runtime_ns;
       attr.sched_deadline = deadline_ns;
       attr.sched_period = period_ns;
       
       if (sched_setattr(0, &attr, 0) != 0) {
           perror("sched_setattr");
           return -1;
       }
       return 0;
   }
   
   // Example: 10ms runtime every 50ms with 30ms deadline
   // set_deadline_scheduling(10000000, 30000000, 50000000);

CPU Affinity
============

Overview
--------

.. code-block:: text

   CPU Affinity:
   - Binds task to specific CPU(s)
   - Improves cache locality
   - Essential for real-time on multi-core
   - Prevents migration overhead
   
   Use Cases:
   - RT tasks on isolated CPUs
   - Cache-sensitive workloads
   - NUMA optimization
   - Avoiding interference

Setting Affinity with taskset
------------------------------

.. code-block:: bash

   # Run on CPU 2
   taskset -c 2 ./my_app
   
   # Run on CPUs 2 and 3
   taskset -c 2,3 ./my_app
   
   # Run on CPUs 0-3
   taskset -c 0-3 ./my_app
   
   # Using CPU mask (hexadecimal)
   taskset 0x1 ./my_app    # CPU 0 (binary: 0001)
   taskset 0x3 ./my_app    # CPUs 0-1 (binary: 0011)
   taskset 0xC ./my_app    # CPUs 2-3 (binary: 1100)
   taskset 0xF ./my_app    # CPUs 0-3 (binary: 1111)
   
   # Change running process affinity
   taskset -p 0x4 1234     # Move PID 1234 to CPU 2
   
   # Query process affinity
   taskset -p 1234
   # Output: pid 1234's current affinity mask: c  (CPUs 2-3)

Setting Affinity in C
----------------------

.. code-block:: c

   #define _GNU_SOURCE
   #include <sched.h>
   #include <stdio.h>
   #include <unistd.h>
   
   // Set affinity to CPU 2
   void set_cpu_affinity(int cpu) {
       cpu_set_t cpuset;
       CPU_ZERO(&cpuset);
       CPU_SET(cpu, &cpuset);
       
       if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
           perror("sched_setaffinity");
       }
   }
   
   // Set affinity to multiple CPUs
   void set_multi_cpu_affinity(int *cpus, int num_cpus) {
       cpu_set_t cpuset;
       CPU_ZERO(&cpuset);
       
       for (int i = 0; i < num_cpus; i++) {
           CPU_SET(cpus[i], &cpuset);
       }
       
       if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
           perror("sched_setaffinity");
       }
   }
   
   // Get current affinity
   void print_affinity() {
       cpu_set_t cpuset;
       CPU_ZERO(&cpuset);
       
       if (sched_getaffinity(0, sizeof(cpuset), &cpuset) == 0) {
           printf("Affinity:");
           for (int i = 0; i < CPU_SETSIZE; i++) {
               if (CPU_ISSET(i, &cpuset)) {
                   printf(" %d", i);
               }
           }
           printf("\n");
       }
   }
   
   // Example usage
   int main() {
       // Run on CPUs 2 and 3
       int cpus[] = {2, 3};
       set_multi_cpu_affinity(cpus, 2);
       
       print_affinity();
       
       // Your code here
       
       return 0;
   }

pthread Affinity
----------------

.. code-block:: c

   #define _GNU_SOURCE
   #include <pthread.h>
   #include <stdio.h>
   
   void *thread_function(void *arg) {
       // Thread work
       return NULL;
   }
   
   int create_affinity_thread(pthread_t *thread, int cpu) {
       pthread_attr_t attr;
       cpu_set_t cpuset;
       
       pthread_attr_init(&attr);
       
       CPU_ZERO(&cpuset);
       CPU_SET(cpu, &cpuset);
       
       pthread_attr_setaffinity_np(&attr, sizeof(cpuset), &cpuset);
       
       int ret = pthread_create(thread, &attr, thread_function, NULL);
       
       pthread_attr_destroy(&attr);
       return ret;
   }
   
   // Set affinity of existing thread
   void set_thread_affinity(pthread_t thread, int cpu) {
       cpu_set_t cpuset;
       CPU_ZERO(&cpuset);
       CPU_SET(cpu, &cpuset);
       
       pthread_setaffinity_np(thread, sizeof(cpuset), &cpuset);
   }

Priority Management
===================

Priority Levels
---------------

.. code-block:: text

   Recommended Priority Assignment:
   
   99: Critical interrupt threads (if needed)
   90-98: High-priority RT tasks
   80-89: Medium-priority RT tasks
   70-79: Low-priority RT tasks
   50-69: Background RT tasks
   1-49: Reserve for future use
   
   Guidelines:
   - Don't use priority 99 unless absolutely necessary
   - Leave gaps for future tasks
   - Group related tasks at similar priorities
   - Test priority assignments under load

Priority Inheritance
--------------------

.. code-block:: c

   #include <pthread.h>
   
   // Create mutex with priority inheritance
   pthread_mutex_t mutex;
   pthread_mutexattr_t attr;
   
   void init_pi_mutex() {
       pthread_mutexattr_init(&attr);
       
       // Enable priority inheritance
       pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
       
       // Or priority ceiling
       // pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_PROTECT);
       // pthread_mutexattr_setprioceiling(&attr, 90);
       
       pthread_mutex_init(&mutex, &attr);
   }
   
   // Use mutex normally
   void critical_section() {
       pthread_mutex_lock(&mutex);
       // Critical code
       pthread_mutex_unlock(&mutex);
   }

Checking Process Priorities
----------------------------

.. code-block:: bash

   # View all processes with scheduling info
   ps -eLo pid,tid,class,rtprio,pri,psr,comm
   
   # Column explanation:
   # pid: Process ID
   # tid: Thread ID
   # class: Scheduling class (FF=FIFO, RR=Round-Robin, TS=Time-Sharing)
   # rtprio: Real-time priority (1-99, or - for non-RT)
   # pri: Kernel's internal priority
   # psr: Processor (CPU) number
   # comm: Command name
   
   # Filter RT processes only
   ps -eLo pid,tid,class,rtprio,pri,psr,comm | grep -E "FF|RR"
   
   # View specific process
   ps -L -p 1234 -o pid,tid,class,rtprio,pri,psr,comm
   
   # Top with scheduling info
   top -H -p 1234

Monitoring and Debugging
=========================

Scheduler Statistics
--------------------

.. code-block:: bash

   # View scheduler debug info
   cat /proc/sched_debug
   
   # Per-CPU runqueues
   cat /proc/sched_debug | grep -A 20 "cpu#"
   
   # RT bandwidth (throttling)
   cat /proc/sys/kernel/sched_rt_period_us
   cat /proc/sys/kernel/sched_rt_runtime_us
   
   # Disable RT throttling (use carefully!)
   echo -1 > /proc/sys/kernel/sched_rt_runtime_us

Context Switches
----------------

.. code-block:: bash

   # Count context switches
   grep ctxt /proc/stat
   
   # Per-process context switches
   grep voluntary_ctxt_switches /proc/1234/status
   grep nonvoluntary_ctxt_switches /proc/1234/status
   
   # Monitor context switches
   vmstat 1
   # cs column shows context switches per second

RT Bandwidth Limit
-------------------

.. code-block:: bash

   # Default: RT tasks can use 950ms out of every 1000ms
   cat /proc/sys/kernel/sched_rt_period_us
   # 1000000 (1 second)
   
   cat /proc/sys/kernel/sched_rt_runtime_us
   # 950000 (0.95 seconds)
   
   # This prevents RT tasks from starving system
   # Remaining 50ms for SCHED_OTHER tasks
   
   # Disable limit (allow 100% RT usage)
   echo -1 > /proc/sys/kernel/sched_rt_runtime_us
   
   # WARNING: System may become unresponsive if RT task runs away

ftrace for Scheduling
---------------------

.. code-block:: bash

   # Enable scheduler tracing
   echo 1 > /sys/kernel/debug/tracing/events/sched/enable
   
   # Trace specific events
   echo 1 > /sys/kernel/debug/tracing/events/sched/sched_switch/enable
   echo 1 > /sys/kernel/debug/tracing/events/sched/sched_wakeup/enable
   
   # Start tracing
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # View trace
   cat /sys/kernel/debug/tracing/trace
   
   # Stop tracing
   echo 0 > /sys/kernel/debug/tracing/tracing_on
   
   # Clear trace
   echo > /sys/kernel/debug/tracing/trace

Complete RT Application Example
================================

.. code-block:: c

   #define _GNU_SOURCE
   #include <stdio.h>
   #include <stdlib.h>
   #include <pthread.h>
   #include <sched.h>
   #include <sys/mman.h>
   #include <unistd.h>
   #include <time.h>
   #include <string.h>
   #include <errno.h>
   
   #define RT_PRIORITY 80
   #define RT_CPU 2
   #define STACK_SIZE 8192
   #define NSEC_PER_SEC 1000000000ULL
   
   void *rt_thread_func(void *arg) {
       struct timespec ts, next;
       unsigned long count = 0;
       
       // Get initial time
       clock_gettime(CLOCK_MONOTONIC, &next);
       
       while (1) {
           // Do real-time work
           count++;
           
           // Sleep until next period (1ms)
           next.tv_nsec += 1000000;
           if (next.tv_nsec >= NSEC_PER_SEC) {
               next.tv_nsec -= NSEC_PER_SEC;
               next.tv_sec++;
           }
           
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
           
           if (count % 1000 == 0) {
               printf("RT thread: %lu iterations\n", count);
           }
       }
       
       return NULL;
   }
   
   int main(int argc, char *argv[]) {
       pthread_t thread;
       pthread_attr_t attr;
       struct sched_param param;
       cpu_set_t cpuset;
       int ret;
       
       printf("Real-time Application Starting...\n");
       
       // Lock memory
       if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
           perror("mlockall");
           return 1;
       }
       printf("Memory locked\n");
       
       // Pre-fault stack
       unsigned char dummy[STACK_SIZE];
       memset(dummy, 0, STACK_SIZE);
       
       // Set CPU affinity
       CPU_ZERO(&cpuset);
       CPU_SET(RT_CPU, &cpuset);
       if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
           perror("sched_setaffinity");
           return 1;
       }
       printf("CPU affinity set to CPU %d\n", RT_CPU);
       
       // Set real-time priority for main thread
       param.sched_priority = RT_PRIORITY;
       if (sched_setscheduler(0, SCHED_FIFO, &param) != 0) {
           perror("sched_setscheduler");
           printf("Note: Run with sudo or set RT limits in /etc/security/limits.conf\n");
           return 1;
       }
       printf("Main thread priority set to SCHED_FIFO %d\n", RT_PRIORITY);
       
       // Initialize thread attributes
       pthread_attr_init(&attr);
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       param.sched_priority = RT_PRIORITY;
       pthread_attr_setschedparam(&attr, &param);
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       // Set thread CPU affinity
       pthread_attr_setaffinity_np(&attr, sizeof(cpuset), &cpuset);
       
       // Create real-time thread
       ret = pthread_create(&thread, &attr, rt_thread_func, NULL);
       if (ret != 0) {
           fprintf(stderr, "pthread_create: %s\n", strerror(ret));
           return 1;
       }
       printf("RT thread created\n");
       
       pthread_attr_destroy(&attr);
       
       // Wait for thread
       pthread_join(thread, NULL);
       
       return 0;
   }
   
   /*
    * Compile:
    * gcc -o rt_app rt_app.c -pthread -lrt -O2
    *
    * Run:
    * sudo ./rt_app
    *
    * Or with chrt:
    * sudo chrt -f 80 ./rt_app
    */

Best Practices
==============

1. **Use appropriate policy** - FIFO for most RT tasks
2. **Set realistic priorities** - don't abuse priority 99
3. **Lock memory** - prevent page faults
4. **Set CPU affinity** - reduce cache misses and migration
5. **Use priority inheritance** - prevent priority inversion
6. **Avoid system calls** in critical paths
7. **Pre-allocate resources** - no malloc in RT context
8. **Use RT-safe sleep** - clock_nanosleep, not sleep/usleep
9. **Test under load** - verify behavior with stress
10. **Monitor continuously** - check for latency spikes

Common Pitfalls
===============

1. **All tasks at priority 99** - defeats scheduling
2. **No CPU affinity** - unpredictable cache behavior
3. **Using sleep/usleep** - not RT-safe
4. **No memory locking** - page faults cause latency
5. **Forgetting PI mutexes** - priority inversion
6. **RT throttling active** - limits RT CPU usage
7. **No resource limits** - can't set RT priority

Quick Reference
===============

.. code-block:: bash

   # Set scheduling policy
   chrt -f 80 ./app          # SCHED_FIFO
   chrt -r 60 ./app          # SCHED_RR
   chrt -d ... ./app         # SCHED_DEADLINE
   
   # Change running process
   chrt -f -p 90 1234
   
   # CPU affinity
   taskset -c 2,3 ./app      # CPUs 2-3
   taskset -p 0xC 1234       # Change running process
   
   # View scheduling
   ps -eLo pid,class,rtprio,pri,psr,comm
   chrt -p 1234
   taskset -p 1234
   
   # Set niceness (non-RT)
   nice -n -10 ./app
   renice -n -5 -p 1234

See Also
========

- Linux_Realtime_PREEMPT_RT.rst
- Linux_Latency_Analysis.rst
- Linux_Realtime_Best_Practices.rst

References
==========

- man 1 chrt
- man 1 taskset
- man 2 sched_setscheduler
- man 2 sched_setaffinity
- man 3 pthread_setschedparam
- man 7 sched
