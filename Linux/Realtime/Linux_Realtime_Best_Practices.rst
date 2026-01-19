===================================
Linux Real-time Best Practices
===================================

:Author: Embedded Linux Documentation
:Date: January 2026
:Version: 1.0
:Focus: Best practices, patterns, and guidelines for real-time Linux development

.. contents:: Table of Contents
   :depth: 3

TL;DR - Essential Best Practices
=================================

Critical Do's and Don'ts
------------------------

.. code-block:: text

   DO:
   ✓ Lock memory with mlockall()
   ✓ Pre-allocate all resources
   ✓ Use PREEMPT_RT kernel
   ✓ Set appropriate RT priority (70-90 range)
   ✓ Isolate CPUs for RT tasks
   ✓ Use clock_nanosleep() for timing
   ✓ Minimize critical sections
   ✓ Test under load with cyclictest
   ✓ Use priority inheritance mutexes
   ✓ Profile and measure latency
   
   DON'T:
   ✗ Use malloc/free in RT path
   ✗ Use sleep/usleep (use clock_nanosleep)
   ✗ Leave memory unlocked (page faults!)
   ✗ Use non-RT locking primitives
   ✗ Perform I/O in RT critical path
   ✗ Use printf/logging in RT path
   ✗ Run all tasks at priority 99
   ✗ Ignore latency testing
   ✗ Use floating point without setup
   ✗ Make blocking system calls

Quick RT Application Checklist
-------------------------------

.. code-block:: c

   // Complete RT application template
   #define _GNU_SOURCE
   #include <stdio.h>
   #include <pthread.h>
   #include <sched.h>
   #include <sys/mman.h>
   #include <string.h>
   #include <time.h>
   
   #define RT_PRIORITY 80
   #define RT_CPU 2
   #define STACK_SIZE 8192
   
   // Pre-allocated buffers (no malloc in RT path!)
   static char buffer[4096];
   
   void *rt_task(void *arg) {
       struct timespec next;
       clock_gettime(CLOCK_MONOTONIC, &next);
       
       while (1) {
           // Critical RT work here
           
           // Deterministic sleep
           next.tv_nsec += 1000000;  // 1ms
           while (next.tv_nsec >= 1000000000) {
               next.tv_nsec -= 1000000000;
               next.tv_sec++;
           }
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
       }
       return NULL;
   }
   
   int main() {
       cpu_set_t cpuset;
       struct sched_param param;
       pthread_t thread;
       unsigned char dummy[STACK_SIZE];
       
       // 1. Lock memory
       if (mlockall(MCL_CURRENT | MCL_FUTURE)) {
           perror("mlockall");
           return 1;
       }
       
       // 2. Pre-fault stack
       memset(dummy, 0, STACK_SIZE);
       
       // 3. Set CPU affinity
       CPU_ZERO(&cpuset);
       CPU_SET(RT_CPU, &cpuset);
       sched_setaffinity(0, sizeof(cpuset), &cpuset);
       
       // 4. Set RT priority
       param.sched_priority = RT_PRIORITY;
       sched_setscheduler(0, SCHED_FIFO, &param);
       
       // 5. Create RT thread
       pthread_create(&thread, NULL, rt_task, NULL);
       pthread_join(thread, NULL);
       
       return 0;
   }

Memory Management
=================

Memory Locking
--------------

.. code-block:: c

   #include <sys/mman.h>
   
   // Lock all current and future pages
   int lock_memory(void) {
       // MCL_CURRENT: Lock all currently mapped pages
       // MCL_FUTURE:  Lock all future mapped pages
       if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
           perror("mlockall failed");
           return -1;
       }
       return 0;
   }
   
   // Check if locking is supported
   #include <unistd.h>
   
   long max_locked = sysconf(_SC_MEMLOCK);
   if (max_locked == -1) {
       printf("Memory locking not supported\n");
   } else {
       printf("Max locked memory: %ld bytes\n", max_locked);
   }
   
   // Unlock when done (cleanup)
   munlockall();

Stack Pre-faulting
------------------

.. code-block:: c

   // Pre-fault stack to avoid page faults
   #define STACK_SIZE 8192
   
   void prefault_stack(void) {
       unsigned char dummy[STACK_SIZE];
       
       // Touch every page (4KB typically)
       memset(dummy, 0, STACK_SIZE);
       
       // Ensure compiler doesn't optimize away
       __asm__ __volatile__("" : : "r" (dummy) : "memory");
   }
   
   // Alternative: Touch pages explicitly
   void prefault_stack_explicit(void) {
       volatile char stack[STACK_SIZE];
       for (int i = 0; i < STACK_SIZE; i += sysconf(_SC_PAGESIZE)) {
           stack[i] = 0;
       }
   }

Memory Allocation Strategies
-----------------------------

.. code-block:: c

   // Strategy 1: Static allocation (best for RT)
   static char buffer[4096];
   static struct my_data data_pool[MAX_ITEMS];
   
   // Strategy 2: Pre-allocated pools
   typedef struct {
       void *pool;
       size_t item_size;
       size_t num_items;
       unsigned long used_bitmap;
   } memory_pool_t;
   
   memory_pool_t *create_pool(size_t item_size, size_t num_items) {
       memory_pool_t *pool = malloc(sizeof(memory_pool_t));
       pool->pool = malloc(item_size * num_items);
       pool->item_size = item_size;
       pool->num_items = num_items;
       pool->used_bitmap = 0;
       
       // Pre-fault the pool
       memset(pool->pool, 0, item_size * num_items);
       
       return pool;
   }
   
   void *pool_alloc(memory_pool_t *pool) {
       for (size_t i = 0; i < pool->num_items; i++) {
           if (!(pool->used_bitmap & (1UL << i))) {
               pool->used_bitmap |= (1UL << i);
               return (char *)pool->pool + (i * pool->item_size);
           }
       }
       return NULL;  // Pool exhausted
   }
   
   void pool_free(memory_pool_t *pool, void *ptr) {
       size_t offset = (char *)ptr - (char *)pool->pool;
       size_t index = offset / pool->item_size;
       pool->used_bitmap &= ~(1UL << index);
   }
   
   // Strategy 3: Ring buffers (lock-free)
   typedef struct {
       void *buffer;
       size_t size;
       size_t head;
       size_t tail;
   } ring_buffer_t;

Avoid Dynamic Allocation
-------------------------

.. code-block:: c

   // BAD: Dynamic allocation in RT path
   void *rt_task_bad(void *arg) {
       while (1) {
           char *buf = malloc(1024);  // WRONG! Non-deterministic
           process_data(buf);
           free(buf);  // WRONG! Non-deterministic
       }
   }
   
   // GOOD: Static/pre-allocated
   static char static_buffer[1024];
   
   void *rt_task_good(void *arg) {
       while (1) {
           process_data(static_buffer);  // Deterministic
       }
   }
   
   // GOOD: Pre-allocated pool
   memory_pool_t *pool;
   
   void init_rt_task(void) {
       pool = create_pool(1024, 10);  // Pre-allocate during init
   }
   
   void *rt_task_pool(void *arg) {
       while (1) {
           void *buf = pool_alloc(pool);  // Fast, deterministic
           if (buf) {
               process_data(buf);
               pool_free(pool, buf);
           }
       }
   }

Timing and Synchronization
===========================

RT-Safe Sleeping
----------------

.. code-block:: c

   #include <time.h>
   
   // BAD: Non-RT sleep functions
   sleep(1);           // WRONG! Not RT-safe
   usleep(1000);       // WRONG! Not RT-safe
   nanosleep(...);     // OK, but relative timing
   
   // GOOD: clock_nanosleep with absolute time
   void rt_sleep_relative(unsigned long nsec) {
       struct timespec ts;
       ts.tv_sec = nsec / 1000000000UL;
       ts.tv_nsec = nsec % 1000000000UL;
       clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, NULL);
   }
   
   // BEST: Absolute timing (no drift)
   void rt_periodic_task(unsigned long period_ns) {
       struct timespec next;
       
       // Get initial time
       clock_gettime(CLOCK_MONOTONIC, &next);
       
       while (1) {
           // Do work
           process_periodic_task();
           
           // Calculate next wakeup (absolute)
           next.tv_nsec += period_ns;
           while (next.tv_nsec >= 1000000000UL) {
               next.tv_nsec -= 1000000000UL;
               next.tv_sec++;
           }
           
           // Sleep until absolute time
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
       }
   }

High-Resolution Timers
----------------------

.. code-block:: c

   #include <time.h>
   #include <signal.h>
   
   // Create high-resolution timer
   timer_t create_rt_timer(void (*handler)(int, siginfo_t *, void *)) {
       timer_t timerid;
       struct sigevent sev;
       struct sigaction sa;
       
       // Setup signal handler
       sa.sa_flags = SA_SIGINFO;
       sa.sa_sigaction = handler;
       sigemptyset(&sa.sa_mask);
       sigaction(SIGRTMIN, &sa, NULL);
       
       // Create timer
       sev.sigev_notify = SIGEV_SIGNAL;
       sev.sigev_signo = SIGRTMIN;
       sev.sigev_value.sival_ptr = &timerid;
       timer_create(CLOCK_MONOTONIC, &sev, &timerid);
       
       return timerid;
   }
   
   // Start timer (periodic)
   void start_periodic_timer(timer_t timerid, unsigned long period_ns) {
       struct itimerspec its;
       
       its.it_value.tv_sec = period_ns / 1000000000UL;
       its.it_value.tv_nsec = period_ns % 1000000000UL;
       its.it_interval.tv_sec = its.it_value.tv_sec;
       its.it_interval.tv_nsec = its.it_value.tv_nsec;
       
       timer_settime(timerid, 0, &its, NULL);
   }

Priority Inheritance Mutexes
-----------------------------

.. code-block:: c

   #include <pthread.h>
   
   // Create mutex with priority inheritance
   pthread_mutex_t mutex;
   pthread_mutexattr_t attr;
   
   void init_pi_mutex(void) {
       pthread_mutexattr_init(&attr);
       
       // Enable priority inheritance
       pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
       
       // Set robust attribute (optional, for fault tolerance)
       pthread_mutexattr_setrobust(&attr, PTHREAD_MUTEX_ROBUST);
       
       pthread_mutex_init(&mutex, &attr);
   }
   
   // Alternative: Priority ceiling protocol
   void init_pc_mutex(int ceiling_priority) {
       pthread_mutexattr_init(&attr);
       pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_PROTECT);
       pthread_mutexattr_setprioceiling(&attr, ceiling_priority);
       pthread_mutex_init(&mutex, &attr);
   }
   
   // Usage (same as normal mutex)
   void critical_section(void) {
       pthread_mutex_lock(&mutex);
       // Protected code
       pthread_mutex_unlock(&mutex);
   }

Lock-Free Data Structures
--------------------------

.. code-block:: c

   #include <stdatomic.h>
   
   // Lock-free ring buffer (single producer, single consumer)
   typedef struct {
       void **buffer;
       atomic_size_t head;
       atomic_size_t tail;
       size_t size;
   } lockfree_ring_t;
   
   lockfree_ring_t *create_lockfree_ring(size_t size) {
       lockfree_ring_t *ring = malloc(sizeof(lockfree_ring_t));
       ring->buffer = malloc(sizeof(void *) * size);
       atomic_init(&ring->head, 0);
       atomic_init(&ring->tail, 0);
       ring->size = size;
       return ring;
   }
   
   int ring_push(lockfree_ring_t *ring, void *item) {
       size_t head = atomic_load_explicit(&ring->head, memory_order_relaxed);
       size_t next_head = (head + 1) % ring->size;
       size_t tail = atomic_load_explicit(&ring->tail, memory_order_acquire);
       
       if (next_head == tail) {
           return -1;  // Full
       }
       
       ring->buffer[head] = item;
       atomic_store_explicit(&ring->head, next_head, memory_order_release);
       return 0;
   }
   
   void *ring_pop(lockfree_ring_t *ring) {
       size_t tail = atomic_load_explicit(&ring->tail, memory_order_relaxed);
       size_t head = atomic_load_explicit(&ring->head, memory_order_acquire);
       
       if (tail == head) {
           return NULL;  // Empty
       }
       
       void *item = ring->buffer[tail];
       size_t next_tail = (tail + 1) % ring->size;
       atomic_store_explicit(&ring->tail, next_tail, memory_order_release);
       return item;
   }

Thread Management
=================

Creating RT Threads
-------------------

.. code-block:: c

   #include <pthread.h>
   #include <sched.h>
   
   pthread_t create_rt_thread(void *(*start_routine)(void *), 
                              void *arg,
                              int priority, 
                              int cpu) {
       pthread_t thread;
       pthread_attr_t attr;
       struct sched_param param;
       cpu_set_t cpuset;
       
       // Initialize attributes
       pthread_attr_init(&attr);
       
       // Set stack size
       pthread_attr_setstacksize(&attr, PTHREAD_STACK_MIN + 65536);
       
       // Set scheduling policy and priority
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       param.sched_priority = priority;
       pthread_attr_setschedparam(&attr, &param);
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       // Set CPU affinity
       CPU_ZERO(&cpuset);
       CPU_SET(cpu, &cpuset);
       pthread_attr_setaffinity_np(&attr, sizeof(cpuset), &cpuset);
       
       // Create thread
       if (pthread_create(&thread, &attr, start_routine, arg) != 0) {
           perror("pthread_create");
           pthread_attr_destroy(&attr);
           return 0;
       }
       
       pthread_attr_destroy(&attr);
       return thread;
   }

Thread Naming (for debugging)
------------------------------

.. code-block:: c

   #include <pthread.h>
   
   // Set thread name (max 16 chars including null)
   void set_thread_name(const char *name) {
       pthread_setname_np(pthread_self(), name);
   }
   
   // Get thread name
   void print_thread_name(pthread_t thread) {
       char name[16];
       pthread_getname_np(thread, name, sizeof(name));
       printf("Thread name: %s\n", name);
   }

I/O and System Calls
====================

Minimize I/O in RT Path
------------------------

.. code-block:: c

   // BAD: I/O in RT critical path
   void *rt_task_bad(void *arg) {
       while (1) {
           int value = read_sensor();  // RT critical
           printf("Sensor: %d\n", value);  // WRONG! Blocking I/O
           write_actuator(value);  // RT critical
       }
   }
   
   // GOOD: Defer non-critical I/O
   lockfree_ring_t *log_ring;
   
   void *rt_task_good(void *arg) {
       while (1) {
           int value = read_sensor();
           
           // Store for logging (lock-free)
           int *log_entry = pool_alloc(log_pool);
           *log_entry = value;
           ring_push(log_ring, log_entry);
           
           write_actuator(value);
       }
   }
   
   // Separate low-priority logging thread
   void *logging_thread(void *arg) {
       while (1) {
           int *log_entry = ring_pop(log_ring);
           if (log_entry) {
               printf("Sensor: %d\n", *log_entry);  // Non-RT, OK
               pool_free(log_pool, log_entry);
           } else {
               usleep(10000);  // 10ms, non-RT thread
           }
       }
   }

O_DIRECT for Deterministic I/O
-------------------------------

.. code-block:: c

   #include <fcntl.h>
   
   // Open file with O_DIRECT (bypass page cache)
   int fd = open("/dev/sda1", O_RDWR | O_DIRECT | O_SYNC);
   
   // Buffer must be aligned
   void *buffer;
   posix_memalign(&buffer, 512, 4096);  // 512-byte alignment
   
   // Direct I/O (more deterministic)
   ssize_t bytes = read(fd, buffer, 4096);
   
   // Note: Still has latency, avoid in RT critical path

RT-Safe Logging
---------------

.. code-block:: c

   // Use lock-free ring buffer for logging
   typedef struct {
       char message[256];
       struct timespec timestamp;
   } log_entry_t;
   
   lockfree_ring_t *log_queue;
   
   // RT-safe log function (producer)
   void rt_log(const char *msg) {
       log_entry_t *entry = pool_alloc(log_pool);
       if (entry) {
           strncpy(entry->message, msg, 255);
           clock_gettime(CLOCK_MONOTONIC, &entry->timestamp);
           ring_push(log_queue, entry);
       }
   }
   
   // Low-priority logging thread (consumer)
   void *log_thread(void *arg) {
       while (1) {
           log_entry_t *entry = ring_pop(log_queue);
           if (entry) {
               printf("[%ld.%09ld] %s\n", 
                      entry->timestamp.tv_sec,
                      entry->timestamp.tv_nsec,
                      entry->message);
               pool_free(log_pool, entry);
           } else {
               usleep(1000);
           }
       }
   }

Error Handling
==============

RT-Safe Error Handling
-----------------------

.. code-block:: c

   // BAD: Complex error handling in RT path
   int rt_function_bad(void) {
       if (error_condition) {
           log_error("Error occurred");  // Blocking!
           cleanup_resources();  // May allocate!
           return -1;
       }
   }
   
   // GOOD: Deferred error handling
   atomic_int error_flag = 0;
   
   int rt_function_good(void) {
       if (error_condition) {
           atomic_store(&error_flag, ERROR_CODE);
           return -1;  // Quick return
       }
   }
   
   // Monitor thread (low priority)
   void *monitor_thread(void *arg) {
       while (1) {
           int error = atomic_exchange(&error_flag, 0);
           if (error) {
               handle_error(error);  // Complex handling OK here
           }
           sleep(1);
       }
   }

Assertions and Debugging
-------------------------

.. code-block:: c

   // Compile-time assertion (no runtime cost)
   #define STATIC_ASSERT(cond, msg) \
       typedef char static_assertion_##msg[(cond) ? 1 : -1]
   
   STATIC_ASSERT(sizeof(int) == 4, int_must_be_4_bytes);
   
   // Runtime assertion (disable in production)
   #ifdef DEBUG_RT
   #define RT_ASSERT(cond) \
       do { \
           if (!(cond)) { \
               atomic_store(&error_flag, __LINE__); \
           } \
       } while(0)
   #else
   #define RT_ASSERT(cond) ((void)0)
   #endif

Testing and Validation
=======================

Latency Testing
---------------

.. code-block:: bash

   #!/bin/bash
   # Comprehensive latency test
   
   echo "Starting RT validation..."
   
   # 1. Basic latency test
   echo "1. Cyclictest (5 minutes)..."
   sudo cyclictest -t $(nproc) -p 95 -n -m -l 300000 -q
   
   # 2. Stress test
   echo "2. Stress test (2 minutes)..."
   sudo cyclictest -t 4 -p 95 -n -m -l 120000 & \
   stress-ng --cpu 8 --io 4 --vm 2 --timeout 120s
   
   # 3. Hardware latency
   echo "3. Hardware latency detection..."
   sudo hwlatdetect --duration=60 --threshold=10
   
   # 4. Interrupt distribution
   echo "4. Checking interrupt distribution..."
   cat /proc/interrupts | head -20
   
   echo "Validation complete"

Unit Testing RT Code
--------------------

.. code-block:: c

   #include <assert.h>
   #include <time.h>
   
   // Test timing accuracy
   void test_timing_accuracy(void) {
       struct timespec start, end, sleep_time;
       long long diff_ns;
       
       sleep_time.tv_sec = 0;
       sleep_time.tv_nsec = 1000000;  // 1ms
       
       for (int i = 0; i < 100; i++) {
           clock_gettime(CLOCK_MONOTONIC, &start);
           clock_nanosleep(CLOCK_MONOTONIC, 0, &sleep_time, NULL);
           clock_gettime(CLOCK_MONOTONIC, &end);
           
           diff_ns = (end.tv_sec - start.tv_sec) * 1000000000LL +
                     (end.tv_nsec - start.tv_nsec);
           
           // Verify within 100μs of target
           assert(diff_ns >= 1000000 && diff_ns <= 1100000);
       }
   }
   
   // Test memory locking
   void test_memory_locked(void) {
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       // Check if memory is locked
       FILE *fp = fopen("/proc/self/status", "r");
       char line[256];
       int vm_lock = 0;
       
       while (fgets(line, sizeof(line), fp)) {
           if (sscanf(line, "VmLck: %d", &vm_lock) == 1) {
               break;
           }
       }
       fclose(fp);
       
       assert(vm_lock > 0);  // Should have locked pages
   }

Profiling RT Applications
--------------------------

.. code-block:: bash

   # Profile with minimal overhead
   sudo perf record -e cycles -c 100000 ./rt_app
   sudo perf report
   
   # Trace scheduling latency
   sudo trace-cmd record -e sched:sched_wakeup -e sched:sched_switch ./rt_app
   sudo trace-cmd report
   
   # Check for page faults (should be zero in RT path)
   sudo perf stat -e page-faults ./rt_app

Common Design Patterns
======================

Producer-Consumer Pattern
--------------------------

.. code-block:: c

   // RT producer + Non-RT consumer
   lockfree_ring_t *data_queue;
   
   // RT producer (high priority)
   void *producer_rt(void *arg) {
       while (1) {
           sensor_data_t *data = pool_alloc(data_pool);
           read_sensor(data);
           ring_push(data_queue, data);
           
           // Periodic timing
           clock_nanosleep(...);
       }
   }
   
   // Non-RT consumer (low priority)
   void *consumer_non_rt(void *arg) {
       while (1) {
           sensor_data_t *data = ring_pop(data_queue);
           if (data) {
               process_data(data);  // Can do I/O, malloc, etc.
               pool_free(data_pool, data);
           } else {
               usleep(1000);
           }
       }
   }

State Machine Pattern
----------------------

.. code-block:: c

   typedef enum {
       STATE_IDLE,
       STATE_RUNNING,
       STATE_ERROR
   } rt_state_t;
   
   typedef struct {
       rt_state_t current_state;
       void (*state_handlers[3])(void);
   } state_machine_t;
   
   void handle_idle(void);
   void handle_running(void);
   void handle_error(void);
   
   state_machine_t sm = {
       .current_state = STATE_IDLE,
       .state_handlers = {
           [STATE_IDLE] = handle_idle,
           [STATE_RUNNING] = handle_running,
           [STATE_ERROR] = handle_error
       }
   };
   
   // RT task executes state machine
   void *rt_state_machine(void *arg) {
       while (1) {
           sm.state_handlers[sm.current_state]();
           clock_nanosleep(...);
       }
   }

System Configuration Checklist
===============================

.. code-block:: bash

   #!/bin/bash
   # RT system configuration script
   
   echo "Configuring system for real-time..."
   
   # 1. CPU isolation
   # Edit /etc/default/grub:
   # GRUB_CMDLINE_LINUX="isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3"
   
   # 2. Disable CPU frequency scaling
   for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
       echo performance > $cpu
   done
   
   # 3. Disable CPU idle
   for cpu in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
       echo 1 > $cpu 2>/dev/null
   done
   
   # 4. Set I/O scheduler
   echo deadline > /sys/block/sda/queue/scheduler
   
   # 5. Disable swap
   swapoff -a
   
   # 6. Set RT limits
   cat >> /etc/security/limits.conf <<EOF
   @realtime   -   rtprio     99
   @realtime   -   memlock    unlimited
   @realtime   -   nice       -20
   EOF
   
   # 7. Disable RT throttling
   echo -1 > /proc/sys/kernel/sched_rt_runtime_us
   
   # 8. Move IRQs to non-RT CPUs
   for irq in /proc/irq/*/smp_affinity; do
       echo 3 > $irq 2>/dev/null  # CPUs 0-1
   done
   
   echo "Configuration complete. Reboot required for some changes."

Best Practices Summary
======================

1. **Memory Management**
   - Always mlockall()
   - Pre-fault stack
   - No malloc/free in RT path
   - Use memory pools or static allocation

2. **Timing**
   - Use clock_nanosleep() with TIMER_ABSTIME
   - CLOCK_MONOTONIC for relative timing
   - Avoid sleep/usleep
   - Use high-resolution timers

3. **Synchronization**
   - Priority inheritance mutexes
   - Minimize critical sections
   - Consider lock-free structures
   - Avoid complex locking

4. **Scheduling**
   - SCHED_FIFO for most RT tasks
   - Priority range 70-90 typical
   - Isolate CPUs for RT
   - Set CPU affinity

5. **I/O**
   - Minimize I/O in RT path
   - Defer logging to low-priority thread
   - Use lock-free queues for communication
   - Consider O_DIRECT for critical I/O

6. **Testing**
   - Test with cyclictest under load
   - Check hardware latency (hwlatdetect)
   - Profile with minimal overhead
   - Continuous monitoring in production

7. **Configuration**
   - PREEMPT_RT kernel
   - Disable CPU frequency scaling
   - Disable deep C-states
   - Isolate CPUs
   - Move IRQs away from RT CPUs

Quick Reference
===============

.. code-block:: c

   // Complete RT application structure
   
   // 1. Initialization
   mlockall(MCL_CURRENT | MCL_FUTURE);
   prefault_stack();
   set_cpu_affinity(RT_CPU);
   set_rt_priority(RT_PRIORITY);
   
   // 2. RT loop
   clock_gettime(CLOCK_MONOTONIC, &next);
   while (1) {
       // Critical work
       
       // Absolute sleep
       next.tv_nsec += PERIOD_NS;
       normalize_timespec(&next);
       clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
   }

See Also
========

- Linux_Realtime_PREEMPT_RT.rst
- Linux_Realtime_Scheduling.rst
- Linux_Latency_Analysis.rst

References
==========

- https://rt.wiki.kernel.org/
- https://www.kernel.org/doc/html/latest/scheduler/sched-rt-group.html
- man 7 sched
- man 2 mlockall
- man 2 clock_nanosleep
