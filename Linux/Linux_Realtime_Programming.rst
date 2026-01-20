================================================================================
Linux Real-Time Programming and POSIX.1b
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Embedded Linux System Design and Development (2006)
:Focus: POSIX.1b real-time extensions, scheduling, latency, RTAI

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. Real-Time Systems Overview
================================================================================

1.1 What is Real-Time?
--------------------------------------------------------------------------------

**Definition:** A system where correctness depends not only on functional
accuracy but also on the **time** at which results are produced.

**POSIX 1003.1b Definition:** The ability of an operating system to provide
a required level of service in a **bounded response time**.

**Example:**

- **Functional correctness:** MPEG decoder produces valid frames
- **Real-time correctness:** Decoder produces frames at exactly 30 FPS

1.2 Hard vs Soft Real-Time
--------------------------------------------------------------------------------

+-------------------------+---------------------------+---------------------------+
| Aspect                  | Hard Real-Time            | Soft Real-Time            |
+=========================+===========================+===========================+
| **Deadline**            | **Must** be met every time| Should be met most times  |
+-------------------------+---------------------------+---------------------------+
| **Consequence**         | Catastrophic failure,     | Degraded performance,     |
|                         | loss of life              | user annoyance            |
+-------------------------+---------------------------+---------------------------+
| **Response Time**       | Guaranteed worst-case     | Average-case bounded      |
+-------------------------+---------------------------+---------------------------+
| **Determinism**         | 100% deterministic        | Statistically deterministic|
+-------------------------+---------------------------+---------------------------+
| **Examples**            | - Aircraft control        | - Video playback          |
|                         | - Nuclear reactor         | - VoIP calls              |
|                         | - Medical devices         | - Gaming                  |
|                         | - Industrial safety       | - Audio processing        |
+-------------------------+---------------------------+---------------------------+
| **Linux Support**       | RTLinux, RTAI, Xenomai    | Mainline (PREEMPT_RT)     |
|                         | (separate kernel modules) | kernel                    |
+-------------------------+---------------------------+---------------------------+

1.3 RTOS Characteristics
--------------------------------------------------------------------------------

**Essential Features:**

1. **Multitasking/Multithreading:** Support concurrent execution
2. **Priority-based:** Critical tasks have higher priorities
3. **Priority Inheritance:** Prevent priority inversion
4. **Preemption:** Higher priority preempts lower immediately
5. **Bounded Interrupt Latency:** Predictable interrupt response
6. **Bounded Scheduler Latency:** Deterministic task scheduling
7. **Deterministic IPC:** Constant-time message passing
8. **Deterministic Memory:** Fixed-time allocation/deallocation

================================================================================
2. Linux Real-Time Evolution
================================================================================

2.1 Mainline Linux Issues (Pre-RT)
--------------------------------------------------------------------------------

**Problems with General-Purpose Linux:**

1. **High Interrupt Latency**
   - Long interrupt-disabled sections
   - Unpredictable interrupt handling

2. **High Scheduler Latency**
   - Non-preemptive kernel (2.4)
   - Scheduling only at safe points

3. **Non-Deterministic Services**
   - IPC mechanisms (variable time)
   - Memory allocation (unpredictable)
   - System calls (unbounded duration)

4. **Virtual Memory**
   - Page faults cause delays
   - Swapping to disk

2.2 Real-Time Solutions
--------------------------------------------------------------------------------

**Evolution Timeline:**

::

   2000: RTLinux/RTAI (hard real-time, dual-kernel)
   2001: Low-latency patches (Ingo Molnar, Andrew Morton)
   2002: O(1) scheduler (2.4.20 - Ingo Molnar)
   2004: Kernel preemption (2.6.0 - Robert Love, MontaVista)
   2005: PREEMPT_RT patches (Ingo Molnar, Thomas Gleixner)
   2011: Many RT features merged into mainline
   2015+: Ongoing PREEMPT_RT integration

**Soft Real-Time Approach (Mainline Kernel):**

- Reduce latencies (don't eliminate)
- Add preemption points
- Priority-based scheduling
- POSIX.1b real-time extensions

**Hard Real-Time Approach (RTLinux/RTAI):**

- Dual-kernel architecture
- Linux runs as lowest-priority task under RT kernel
- Direct hardware access for RT tasks
- Microsecond-level determinism

================================================================================
3. Latency Types and Reduction
================================================================================

3.1 System Latencies
--------------------------------------------------------------------------------

**Latency Flow (Interrupt to Task Execution):**

::

   Hardware Interrupt
        ↓ (Interrupt Latency)
   ISR Execution
        ↓ (Wakeup Latency)
   Task Made Runnable (added to run queue)
        ↓ (Scheduler Latency)
   Scheduler Selects Task
        ↓ (Context Switch)
   Task Executes
   
   Total Response Time = Interrupt Latency +
                        Wakeup Latency +
                        Scheduler Latency +
                        Context Switch Time

**Breakdown:**

1. **Interrupt Latency:** HW interrupt → ISR starts
2. **Wakeup Latency:** wake_up() called → task runnable
3. **Scheduler Latency:** Task runnable → starts executing
4. **Context Switch:** Old task → New task (save/restore)

3.2 Interrupt Latency
--------------------------------------------------------------------------------

**Causes of High Interrupt Latency:**

.. code-block:: c

   /* Cause 1: Disabling interrupts */
   local_irq_save(flags);
   /* Critical section - ALL interrupts disabled */
   local_irq_restore(flags);
   
   /* Cause 2: Spinlocks that disable IRQs */
   spin_lock_irqsave(&lock, flags);
   /* Critical section */
   spin_unlock_irqrestore(&lock, flags);
   
   /* Cause 3: Long ISR execution */
   irqreturn_t my_isr(int irq, void *dev_id)
   {
       /* Long processing here delays other interrupts */
       return IRQ_HANDLED;
   }

**Solutions:**

.. code-block:: c

   /* Solution 1: Use spinlock without IRQ disable when possible */
   spin_lock(&lock);
   /* Critical section */
   spin_unlock(&lock);
   
   /* Solution 2: Defer work to bottom half */
   irqreturn_t my_isr(int irq, void *dev_id)
   {
       /* Minimal work: acknowledge interrupt, schedule work */
       schedule_work(&my_work);
       return IRQ_HANDLED;
   }
   
   /* Solution 3: Use threaded IRQs (modern approach) */
   request_threaded_irq(irq, hard_handler, thread_handler,
                        IRQF_ONESHOT, "mydev", dev);

**Measurement:**

.. code-block:: c

   /* Use cyclictest to measure interrupt latency */
   sudo cyclictest -p 99 -t5 -n

3.3 Scheduler Latency
--------------------------------------------------------------------------------

**Pre-Preemption Kernel (Linux 2.4):**

::

   Low Priority Task (in kernel mode - system call)
   |-------------------------------------------|
   T0                                         T2
                      ↑
                     T1 (High priority task becomes runnable)
   
   Scheduler Latency = T2 - T1 (can be 10-100ms!)

**Problems:**

- Kernel not preemptible during system calls
- Scheduling only at safe points (return from syscall/interrupt)
- Long system calls cause unbounded latencies

**With Kernel Preemption (Linux 2.6+):**

::

   Low Priority Task (in kernel mode)
   |-----|   Critical   |-----|
   T0   T1'  Section    T1  T2
              (spinlock)
                ↑
               T1 (High priority task runnable)
   
   Scheduler Latency = T1' - T1 (reduced to microseconds)

**Preemption Implementation:**

.. code-block:: c

   /* Each task has preempt_count */
   struct thread_info {
       int preempt_count;  /* 0 = preemptible, >0 = not */
       /* ... */
   };
   
   /* Spinlocks increment/decrement preempt_count */
   #define spin_lock(lock) \
       do { \
           preempt_disable(); \
           _spin_lock(lock); \
       } while (0)
   
   #define spin_unlock(lock) \
       do { \
           _spin_unlock(lock); \
           preempt_enable(); \  /* May trigger schedule() */
       } while (0)
   
   /* Return from interrupt checks if reschedule needed */
   asmlinkage void ret_from_exception(void)
   {
       if (need_resched() && preempt_count() == 0)
           schedule();
       /* ... */
   }

**Low-Latency Patches:**

.. code-block:: c

   /* Add explicit schedule points in long kernel code */
   
   /* Before: Long loop, no preemption */
   for (i = 0; i < huge_number; i++) {
       process_item(i);
   }
   
   /* After: Explicit reschedule points */
   for (i = 0; i < huge_number; i++) {
       process_item(i);
       
       if (need_resched()) {
           cond_resched();  /* Check and schedule if needed */
       }
   }

3.4 Scheduler Duration - O(1) Scheduler
--------------------------------------------------------------------------------

**Problem with O(n) Scheduler (2.4):**

.. code-block:: c

   /* Goodness loop: O(n) - scan all tasks */
   for_each_task(p) {
       if (can_schedule(p)) {
           weight = goodness(p, prev, this_cpu);
           if (weight > max_weight) {
               max_weight = weight;
               next = p;
           }
       }
   }

**O(1) Scheduler Solution (2.6):**

::

   Active Array             Expired Array
   [Priority 0]  → Task A   [Priority 0]  → (empty)
   [Priority 1]  → (empty)  [Priority 1]  → Task C
   ...                      ...
   [Priority 99] → Task B   [Priority 99] → (empty)
   
   Bitmap: 10000...001 (indicates non-empty queues)
   
   Next task = find_first_bit(bitmap) → O(1)
   When active empty → swap(active, expired) → O(1)

.. code-block:: c

   /* O(1) scheduler structure */
   struct prio_array {
       int nr_active;
       unsigned long bitmap[5];  /* 5 * 32 = 160 bits for 140 priorities */
       struct list_head queue[MAX_PRIO];  /* Per-priority queue */
   };
   
   struct runqueue {
       struct prio_array *active;
       struct prio_array *expired;
       /* ... */
   };
   
   /* O(1) next task selection */
   static inline task_t *next_task(struct runqueue *rq)
   {
       struct prio_array *array = rq->active;
       int idx;
       
       idx = sched_find_first_bit(array->bitmap);  /* O(1) */
       return list_entry(array->queue[idx].next, task_t, run_list);
   }

================================================================================
4. POSIX.1b Real-Time Extensions
================================================================================

4.1 Overview
--------------------------------------------------------------------------------

**IEEE 1003.1b (POSIX.1b) Standard Features:**

1. **Scheduling:**
   - Fixed-priority scheduling
   - Real-time scheduling classes (SCHED_FIFO, SCHED_RR)

2. **Synchronization:**
   - POSIX semaphores
   - POSIX mutexes with priority inheritance

3. **IPC:**
   - POSIX message queues
   - POSIX shared memory

4. **Timers and Clocks:**
   - High-resolution clocks
   - POSIX timers

5. **Signals:**
   - Real-time signals (queued, ordered)

6. **Memory:**
   - Memory locking (prevent paging)

7. **I/O:**
   - Asynchronous I/O (AIO)

**Compilation:**

.. code-block:: bash

   # Link with librt
   gcc program.c -o program -lrt -lpthread

4.2 Real-Time Scheduling
--------------------------------------------------------------------------------

**Scheduling Classes:**

+-------------------------+---------------------------+---------------------------+
| Class                   | Priority Range            | Behavior                  |
+=========================+===========================+===========================+
| SCHED_OTHER             | Nice: -20 to +19          | Time-sharing (default)    |
|                         | (not real-time)           | Non-deterministic         |
+-------------------------+---------------------------+---------------------------+
| SCHED_FIFO              | 1 to 99                   | First-In-First-Out        |
|                         | (user-space view)         | No time slicing           |
|                         |                           | Runs until:               |
|                         |                           | - Blocks                  |
|                         |                           | - Yields                  |
|                         |                           | - Higher priority ready   |
+-------------------------+---------------------------+---------------------------+
| SCHED_RR                | 1 to 99                   | Round-Robin (time-sliced) |
|                         |                           | Same as FIFO but with     |
|                         |                           | time quantum              |
+-------------------------+---------------------------+---------------------------+

**Priority Mapping:**

::

   User-Space (Application View)       Kernel-Space (Internal)
   
   SCHED_FIFO/RR:  99 (highest)        → Kernel Priority: 0
                   50                  →                   49
                   1  (lowest RT)      →                   98
   
   SCHED_OTHER:    0                   → Kernel Priority: 99-139
                                         (based on nice value)

**Setting Scheduling Policy:**

.. code-block:: c

   #include <sched.h>
   
   /* Get priority limits */
   int min_prio = sched_get_priority_min(SCHED_FIFO);  /* Returns 1 */
   int max_prio = sched_get_priority_max(SCHED_FIFO);  /* Returns 99 */
   
   /* Set scheduling policy and priority */
   struct sched_param param;
   param.sched_priority = 50;
   
   if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
       perror("sched_setscheduler");
       /* Requires CAP_SYS_NICE capability or root */
   }
   
   /* Get current policy */
   int policy = sched_getscheduler(0);
   switch (policy) {
   case SCHED_OTHER:
       printf("SCHED_OTHER\n");
       break;
   case SCHED_FIFO:
       printf("SCHED_FIFO\n");
       break;
   case SCHED_RR:
       printf("SCHED_RR\n");
       break;
   }
   
   /* Get current priority */
   struct sched_param current_param;
   sched_getparam(0, &current_param);
   printf("Priority: %d\n", current_param.sched_priority);

**Thread Scheduling:**

.. code-block:: c

   #include <pthread.h>
   
   void *rt_thread(void *arg)
   {
       printf("Real-time thread running\n");
       /* Time-critical work */
       return NULL;
   }
   
   int main()
   {
       pthread_t thread;
       pthread_attr_t attr;
       struct sched_param param;
       
       /* Initialize thread attributes */
       pthread_attr_init(&attr);
       
       /* Set scheduling policy */
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       
       /* Set priority */
       param.sched_priority = 80;
       pthread_attr_setschedparam(&attr, &param);
       
       /* Use explicit scheduling (not inherited) */
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       /* Create real-time thread */
       pthread_create(&thread, &attr, rt_thread, NULL);
       
       pthread_join(thread, NULL);
       pthread_attr_destroy(&attr);
       
       return 0;
   }

**Yielding CPU:**

.. code-block:: c

   /* SCHED_FIFO thread voluntarily yields */
   sched_yield();  /* Let same-priority tasks run */

**Get Time Quantum (SCHED_RR):**

.. code-block:: c

   struct timespec ts;
   
   if (sched_rr_get_interval(0, &ts) == 0) {
       printf("Time quantum: %ld.%09ld seconds\n",
              ts.tv_sec, ts.tv_nsec);
   }

4.3 Memory Locking
--------------------------------------------------------------------------------

**Why Lock Memory?**

- Prevent page faults (unpredictable delays)
- Keep code and data in RAM
- Essential for real-time performance

**Memory Lock Functions:**

.. code-block:: c

   #include <sys/mman.h>
   
   /* Lock all current and future memory */
   if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
       perror("mlockall");
       /* Requires CAP_IPC_LOCK or root */
   }
   
   /* MCL_CURRENT: Lock all currently mapped pages */
   /* MCL_FUTURE:  Lock all future mappings */
   
   /* Unlock all memory */
   munlockall();
   
   /* Lock specific region */
   void *addr = malloc(SIZE);
   mlock(addr, SIZE);
   
   /* Unlock specific region */
   munlock(addr, SIZE);
   free(addr);

**Pre-Fault Stack:**

.. code-block:: c

   #define STACK_PREFAULT_SIZE (8 * 1024)  /* 8KB */
   
   void prefault_stack(void)
   {
       unsigned char dummy[STACK_PREFAULT_SIZE];
       
       /* Touch each page to fault it in */
       memset(dummy, 0, STACK_PREFAULT_SIZE);
   }
   
   int main()
   {
       /* Lock memory */
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       /* Pre-fault stack */
       prefault_stack();
       
       /* Now ready for real-time work */
       /* ... */
   }

4.4 POSIX Clocks and Timers
--------------------------------------------------------------------------------

**Clock Types:**

.. code-block:: c

   #include <time.h>
   
   /* Available clocks */
   CLOCK_REALTIME         /* System-wide wall-clock time */
   CLOCK_MONOTONIC        /* Monotonic time (not affected by time adjustments) */
   CLOCK_PROCESS_CPUTIME_ID  /* Per-process CPU time */
   CLOCK_THREAD_CPUTIME_ID   /* Per-thread CPU time */

**Get Clock Resolution:**

.. code-block:: c

   struct timespec res;
   
   clock_getres(CLOCK_MONOTONIC, &res);
   printf("Resolution: %ld ns\n", res.tv_nsec);

**Get Current Time:**

.. code-block:: c

   struct timespec now;
   
   clock_gettime(CLOCK_MONOTONIC, &now);
   printf("Time: %ld.%09ld\n", now.tv_sec, now.tv_nsec);

**POSIX Timers:**

.. code-block:: c

   #include <signal.h>
   #include <time.h>
   
   void timer_handler(int sig, siginfo_t *si, void *uc)
   {
       printf("Timer expired\n");
   }
   
   int main()
   {
       timer_t timerid;
       struct sigevent sev;
       struct itimerspec its;
       struct sigaction sa;
       
       /* Setup signal handler */
       sa.sa_flags = SA_SIGINFO;
       sa.sa_sigaction = timer_handler;
       sigemptyset(&sa.sa_mask);
       sigaction(SIGRTMIN, &sa, NULL);
       
       /* Create timer */
       sev.sigev_notify = SIGEV_SIGNAL;
       sev.sigev_signo = SIGRTMIN;
       sev.sigev_value.sival_ptr = &timerid;
       timer_create(CLOCK_MONOTONIC, &sev, &timerid);
       
       /* Start timer: 1 second initial, then every 500ms */
       its.it_value.tv_sec = 1;
       its.it_value.tv_nsec = 0;
       its.it_interval.tv_sec = 0;
       its.it_interval.tv_nsec = 500000000;  /* 500ms */
       
       timer_settime(timerid, 0, &its, NULL);
       
       /* Wait for timers */
       while (1) pause();
       
       return 0;
   }

**Thread-based Timers:**

.. code-block:: c

   void *timer_thread(void *arg)
   {
       printf("Timer expired in thread\n");
       return NULL;
   }
   
   struct sigevent sev;
   timer_t timerid;
   
   sev.sigev_notify = SIGEV_THREAD;
   sev.sigev_notify_function = timer_thread;
   sev.sigev_notify_attributes = NULL;
   
   timer_create(CLOCK_MONOTONIC, &sev, &timerid);

4.5 POSIX Message Queues
--------------------------------------------------------------------------------

**Features:**

- Priority-based message delivery
- Non-blocking and timed operations
- Deterministic message passing

**Create/Open Message Queue:**

.. code-block:: c

   #include <mqueue.h>
   #include <fcntl.h>
   
   mqd_t mq;
   struct mq_attr attr;
   
   /* Set queue attributes */
   attr.mq_flags = 0;
   attr.mq_maxmsg = 10;           /* Max messages in queue */
   attr.mq_msgsize = 256;         /* Max message size */
   attr.mq_curmsgs = 0;
   
   /* Create message queue */
   mq = mq_open("/my_queue", O_CREAT | O_RDWR, 0644, &attr);
   if (mq == (mqd_t)-1) {
       perror("mq_open");
       exit(1);
   }

**Send Message:**

.. code-block:: c

   char msg[] = "High priority message";
   unsigned int prio = 10;  /* Higher number = higher priority */
   
   if (mq_send(mq, msg, strlen(msg) + 1, prio) == -1) {
       perror("mq_send");
   }
   
   /* Timed send */
   struct timespec timeout;
   clock_gettime(CLOCK_REALTIME, &timeout);
   timeout.tv_sec += 5;  /* 5 second timeout */
   
   if (mq_timedsend(mq, msg, strlen(msg) + 1, prio, &timeout) == -1) {
       if (errno == ETIMEDOUT)
           printf("Send timeout\n");
   }

**Receive Message:**

.. code-block:: c

   char buffer[256];
   unsigned int prio;
   ssize_t bytes;
   
   /* Blocking receive */
   bytes = mq_receive(mq, buffer, sizeof(buffer), &prio);
   if (bytes >= 0) {
       printf("Received: %s (priority %u)\n", buffer, prio);
   }
   
   /* Timed receive */
   struct timespec timeout;
   clock_gettime(CLOCK_REALTIME, &timeout);
   timeout.tv_sec += 5;
   
   bytes = mq_timedreceive(mq, buffer, sizeof(buffer), &prio, &timeout);

**Notification:**

.. code-block:: c

   /* Get notified when message arrives */
   
   void notification_handler(union sigval sv)
   {
       mqd_t mq = *((mqd_t *)sv.sival_ptr);
       char buffer[256];
       unsigned int prio;
       
       /* Read message */
       mq_receive(mq, buffer, sizeof(buffer), &prio);
       printf("Notified: %s\n", buffer);
       
       /* Re-register for next notification */
       struct sigevent sev;
       sev.sigev_notify = SIGEV_THREAD;
       sev.sigev_notify_function = notification_handler;
       sev.sigev_value.sival_ptr = &mq;
       mq_notify(mq, &sev);
   }
   
   /* Register notification */
   struct sigevent sev;
   sev.sigev_notify = SIGEV_THREAD;
   sev.sigev_notify_function = notification_handler;
   sev.sigev_value.sival_ptr = &mq;
   
   mq_notify(mq, &sev);

**Cleanup:**

.. code-block:: c

   mq_close(mq);
   mq_unlink("/my_queue");  /* Remove queue */

4.6 Real-Time Signals
--------------------------------------------------------------------------------

**Features:**

- Guaranteed delivery (queued, not merged)
- Ordered delivery (by priority)
- Can carry data (sigval)

**Signal Range:**

.. code-block:: c

   /* Real-time signals: SIGRTMIN to SIGRTMAX */
   /* Typically: 34 to 64 (32 signals) */
   
   int first_rt = SIGRTMIN;
   int last_rt = SIGRTMAX;

**Sending Real-Time Signals:**

.. code-block:: c

   #include <signal.h>
   
   /* Send with value */
   union sigval value;
   value.sival_int = 42;
   
   sigqueue(pid, SIGRTMIN, value);
   
   /* Or use pointer */
   value.sival_ptr = &some_data;
   sigqueue(pid, SIGRTMIN+1, value);

**Receiving:**

.. code-block:: c

   void rt_signal_handler(int sig, siginfo_t *info, void *context)
   {
       printf("Signal %d received\n", sig);
       printf("Value: %d\n", info->si_value.sival_int);
       printf("Sender PID: %d\n", info->si_pid);
   }
   
   int main()
   {
       struct sigaction sa;
       
       sa.sa_flags = SA_SIGINFO;
       sa.sa_sigaction = rt_signal_handler;
       sigemptyset(&sa.sa_mask);
       
       /* Register handler for real-time signals */
       for (int i = SIGRTMIN; i <= SIGRTMAX; i++) {
           sigaction(i, &sa, NULL);
       }
       
       while (1) pause();
       
       return 0;
   }

4.7 POSIX Semaphores
--------------------------------------------------------------------------------

**Named Semaphores (Inter-Process):**

.. code-block:: c

   #include <semaphore.h>
   #include <fcntl.h>
   
   /* Create/open semaphore */
   sem_t *sem = sem_open("/my_sem", O_CREAT, 0644, 1);  /* Initial value 1 */
   
   /* Wait (decrement) */
   sem_wait(sem);
   
   /* Try wait (non-blocking) */
   if (sem_trywait(sem) == 0) {
       /* Got semaphore */
   }
   
   /* Timed wait */
   struct timespec ts;
   clock_gettime(CLOCK_REALTIME, &ts);
   ts.tv_sec += 5;
   if (sem_timedwait(sem, &ts) == 0) {
       /* Got semaphore within timeout */
   }
   
   /* Post (increment) */
   sem_post(sem);
   
   /* Cleanup */
   sem_close(sem);
   sem_unlink("/my_sem");

**Unnamed Semaphores (Thread/Shared Memory):**

.. code-block:: c

   sem_t sem;
   
   /* Initialize for threads */
   sem_init(&sem, 0, 1);  /* 0 = shared between threads, 1 = initial value */
   
   /* Initialize for processes (in shared memory) */
   sem_init(&sem, 1, 1);  /* 1 = shared between processes */
   
   /* Use same wait/post as above */
   sem_wait(&sem);
   sem_post(&sem);
   
   /* Destroy */
   sem_destroy(&sem);

4.8 POSIX Shared Memory
--------------------------------------------------------------------------------

.. code-block:: c

   #include <sys/mman.h>
   #include <fcntl.h>
   
   #define SHM_SIZE 4096
   
   /* Create shared memory */
   int fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0644);
   ftruncate(fd, SHM_SIZE);
   
   /* Map to address space */
   void *ptr = mmap(NULL, SHM_SIZE, PROT_READ | PROT_WRITE,
                    MAP_SHARED, fd, 0);
   
   /* Use shared memory */
   strcpy(ptr, "Shared data");
   
   /* Synchronize with msync */
   msync(ptr, SHM_SIZE, MS_SYNC);
   
   /* Cleanup */
   munmap(ptr, SHM_SIZE);
   close(fd);
   shm_unlink("/my_shm");

================================================================================
5. Priority Inversion and Solutions
================================================================================

5.1 Priority Inversion Problem
--------------------------------------------------------------------------------

**Scenario:**

::

   Task H (High Priority: 90)
   Task M (Medium Priority: 50)
   Task L (Low Priority: 10)
   
   Timeline:
   T0: Task L locks mutex
   T1: Task L running (holding mutex)
   T2: Task H becomes ready, preempts L
   T3: Task H tries to lock same mutex → BLOCKS
   T4: Task M becomes ready, preempts L (!)
   T5: Task M runs (while H waits for L to finish!)
   
   Result: High priority task waits for medium priority task

5.2 Priority Inheritance
--------------------------------------------------------------------------------

**Solution:** Low priority task inherits high priority temporarily

.. code-block:: c

   pthread_mutexattr_t attr;
   pthread_mutex_t mutex;
   
   /* Set priority inheritance protocol */
   pthread_mutexattr_init(&attr);
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
   
   /* Create mutex with priority inheritance */
   pthread_mutex_init(&mutex, &attr);
   
   /* Now when H blocks on mutex held by L:
    * L temporarily inherits H's priority
    * M cannot preempt L
    * L finishes quickly and releases mutex
    * L returns to original priority
    * H acquires mutex and continues
    */
   
   pthread_mutexattr_destroy(&attr);

**Priority Ceiling:**

.. code-block:: c

   pthread_mutexattr_t attr;
   pthread_mutex_t mutex;
   
   /* Set priority ceiling */
   pthread_mutexattr_init(&attr);
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_PROTECT);
   pthread_mutexattr_setprioceiling(&attr, 99);  /* Ceiling priority */
   
   pthread_mutex_init(&mutex, &attr);
   
   /* Task holding mutex runs at ceiling priority (99) */
   
   pthread_mutexattr_destroy(&attr);

================================================================================
6. Asynchronous I/O (AIO)
================================================================================

6.1 POSIX AIO
--------------------------------------------------------------------------------

.. code-block:: c

   #include <aio.h>
   
   /* Setup AIO control block */
   struct aiocb cb;
   memset(&cb, 0, sizeof(cb));
   
   cb.aio_fildes = fd;
   cb.aio_buf = buffer;
   cb.aio_nbytes = size;
   cb.aio_offset = 0;
   cb.aio_sigevent.sigev_notify = SIGEV_SIGNAL;
   cb.aio_sigevent.sigev_signo = SIGRTMIN;
   
   /* Start asynchronous read */
   aio_read(&cb);
   
   /* Continue doing other work */
   /* ... */
   
   /* Wait for completion */
   while (aio_error(&cb) == EINPROGRESS) {
       /* Do other work */
   }
   
   /* Get result */
   ssize_t bytes = aio_return(&cb);

**Multiple Operations:**

.. code-block:: c

   struct aiocb *list[10];
   
   /* Start multiple I/O operations */
   for (int i = 0; i < 10; i++) {
       aio_read(list[i]);
   }
   
   /* Wait for all */
   aio_suspend(list, 10, NULL);
   
   /* Or wait for any */
   while (aio_suspend(list, 10, &timeout) == 0) {
       /* Check which completed */
       for (int i = 0; i < 10; i++) {
           if (aio_error(list[i]) != EINPROGRESS) {
               /* This one completed */
               aio_return(list[i]);
           }
       }
   }

================================================================================
7. Practical Real-Time Programming
================================================================================

7.1 Complete Real-Time Application Template
--------------------------------------------------------------------------------

.. code-block:: c

   #define _GNU_SOURCE
   #include <stdio.h>
   #include <stdlib.h>
   #include <string.h>
   #include <pthread.h>
   #include <sched.h>
   #include <sys/mman.h>
   #include <unistd.h>
   
   #define STACK_PREFAULT (8 * 1024)
   
   void *rt_task(void *arg)
   {
       int task_id = *(int *)arg;
       struct timespec next, now, interval;
       
       /* Set interval: 10ms */
       interval.tv_sec = 0;
       interval.tv_nsec = 10000000;
       
       /* Get current time */
       clock_gettime(CLOCK_MONOTONIC, &now);
       next = now;
       
       while (1) {
           /* Do time-critical work */
           printf("Task %d: Processing\n", task_id);
           
           /* Calculate next activation time */
           next.tv_nsec += interval.tv_nsec;
           if (next.tv_nsec >= 1000000000) {
               next.tv_nsec -= 1000000000;
               next.tv_sec++;
           }
           
           /* Sleep until next period */
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
       }
       
       return NULL;
   }
   
   int main(int argc, char *argv[])
   {
       pthread_t thread;
       pthread_attr_t attr;
       struct sched_param param;
       int task_id = 1;
       
       /* Lock memory to prevent paging */
       if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
           perror("mlockall failed");
           return 1;
       }
       
       /* Pre-fault stack */
       unsigned char dummy[STACK_PREFAULT];
       memset(dummy, 0, STACK_PREFAULT);
       
       /* Initialize thread attributes */
       pthread_attr_init(&attr);
       
       /* Set scheduling policy to FIFO */
       pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
       
       /* Set priority */
       param.sched_priority = 80;
       pthread_attr_setschedparam(&attr, &param);
       
       /* Use explicit scheduling */
       pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
       
       /* Set stack size */
       pthread_attr_setstacksize(&attr, PTHREAD_STACK_MIN + 64 * 1024);
       
       /* Create real-time thread */
       if (pthread_create(&thread, &attr, rt_task, &task_id) != 0) {
           perror("pthread_create");
           return 1;
       }
       
       /* Wait for thread */
       pthread_join(thread, NULL);
       
       pthread_attr_destroy(&attr);
       
       return 0;
   }
   
   /* Compile: gcc -o rtapp rtapp.c -lrt -lpthread */
   /* Run: sudo ./rtapp */

7.2 Latency Measurement
--------------------------------------------------------------------------------

**Using cyclictest:**

.. code-block:: bash

   # Install rt-tests
   sudo apt-get install rt-tests
   
   # Run cyclictest
   sudo cyclictest -p 99 -t5 -n
   
   # Options:
   # -p 99: Priority 99
   # -t5: 5 threads
   # -n: Use clock_nanosleep
   
   # Output shows min/avg/max latency

**Custom Latency Measurement:**

.. code-block:: c

   struct timespec t1, t2, diff;
   
   clock_gettime(CLOCK_MONOTONIC, &t1);
   
   /* Time-critical operation */
   
   clock_gettime(CLOCK_MONOTONIC, &t2);
   
   /* Calculate difference */
   diff.tv_sec = t2.tv_sec - t1.tv_sec;
   diff.tv_nsec = t2.tv_nsec - t1.tv_nsec;
   if (diff.tv_nsec < 0) {
       diff.tv_sec--;
       diff.tv_nsec += 1000000000;
   }
   
   printf("Latency: %ld.%09ld seconds\n", diff.tv_sec, diff.tv_nsec);

================================================================================
8. Best Practices
================================================================================

**1. Memory Management:**

- Use ``mlockall()`` to prevent paging
- Pre-fault stack and heap
- Avoid dynamic allocation in RT path
- Use memory pools if allocation needed

**2. Scheduling:**

- Use SCHED_FIFO for hard real-time
- Set appropriate priorities (leave headroom)
- Don't make entire program RT (only time-critical parts)

**3. Synchronization:**

- Use priority inheritance mutexes
- Minimize critical section duration
- Avoid blocking operations in RT tasks

**4. I/O:**

- Use AIO for disk I/O
- Use O_DIRECT to bypass page cache
- Preallocate files to avoid allocation delays

**5. Signal Handling:**

- Block signals in RT threads
- Use dedicated signal handler thread
- Use real-time signals for priority

**6. Debugging:**

- Use ftrace for kernel latency tracing
- Use cyclictest for latency measurement
- Profile with perf

**7. System Configuration:**

- Disable CPU frequency scaling
- Isolate RT CPUs (isolcpus kernel parameter)
- Disable unnecessary services
- Use PREEMPT_RT kernel for best results

================================================================================
End of Linux Real-Time Programming Cheatsheet
================================================================================
