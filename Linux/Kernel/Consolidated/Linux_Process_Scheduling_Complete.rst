====================================================================
Linux Process Management & Scheduling — Complete Guide
====================================================================

**Comprehensive coverage of Linux process/thread management, scheduling policies, SMP, real-time scheduling, CPU affinity, load balancing, and namespaces.**

**Current as of:** Linux 6.12–6.16 (January 2026)  
**Architecture focus:** x86_64, ARM64 (SMP multicore systems)

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**Linux Process Management** handles task creation, scheduling, CPU affinity, priority, and inter-process coordination across multiple CPUs.

**Key Concepts:**

.. code-block:: text

   Component              Purpose                          Main Files
   ─────────────────────  ───────────────────────────────  ─────────────────────────
   task_struct            Per-process/thread descriptor    include/linux/sched.h
   CFS Scheduler          Fair scheduling (default)        kernel/sched/fair.c
   RT Scheduler           Real-time FIFO/RR                kernel/sched/rt.c
   Deadline Scheduler     EDF (Earliest Deadline First)    kernel/sched/deadline.c
   SMP Load Balancer      Cross-CPU task migration         kernel/sched/fair.c
   CPU Affinity           Pin tasks to specific CPUs       kernel/sched/core.c
   Namespaces             Process isolation (containers)   kernel/pid_namespace.c
   Cgroups                Resource limits (CPU, memory)    kernel/cgroup/

**Process vs Thread:**

.. code-block:: text

   Aspect              Process                          Thread
   ──────────────────  ───────────────────────────────  ───────────────────────────
   Creation            fork(), vfork(), clone()         pthread_create() → clone(CLONE_THREAD)
   PID                 Unique                           Shares PID (thread group)
   TID                 Same as PID                      Unique thread ID
   Virtual Memory      Separate                         Shared with other threads
   File Descriptors    Separate (unless dup'd)          Shared
   Scheduler Entity    Independent task_struct          Independent task_struct
   Scheduling          Per-process                      Per-thread

**Scheduling Policies:**

.. code-block:: text

   Policy              Class      Priority    Preemption     Use Case
   ──────────────────  ─────────  ──────────  ─────────────  ────────────────────────
   SCHED_OTHER (CFS)   Normal     Nice -20–19 Time-sliced   General workloads
   SCHED_BATCH         Normal     0           Less frequent  Background jobs
   SCHED_IDLE          Normal     0           Very low       Lowest priority
   SCHED_FIFO          Real-time  1–99        FCFS           Low-latency, no slice
   SCHED_RR            Real-time  1–99        Round-robin    Soft real-time
   SCHED_DEADLINE      Real-time  EDF params  EDF algorithm  Hard real-time

**Quick Commands:**

.. code-block:: bash

   # View all threads
   ps -eLf
   top -H
   
   # Set scheduling policy
   chrt -f 50 ./myapp           # SCHED_FIFO, priority 50
   chrt -r 30 -p 1234           # SCHED_RR, priority 30
   
   # Change nice value (SCHED_OTHER)
   nice -n 10 ./myapp           # Start with nice +10
   renice -20 -p 1234           # Change to nice -20 (highest)
   
   # CPU affinity
   taskset -c 0,2-4 ./myapp     # Run on CPUs 0,2,3,4
   taskset -cp 0-3 1234         # Pin PID 1234 to CPUs 0-3
   
   # View scheduling info
   chrt -p 1234                 # Show policy & priority
   ps -o pid,tid,class,rtprio,ni,comm -p 1234

================================================================================
1. Process & Thread Fundamentals
================================================================================

**1.1 task_struct — The Process Descriptor**
----------------------------------------------

Every process and thread in Linux is represented by a ``struct task_struct``.

**Key Fields:**

.. code-block:: c

   struct task_struct {
       // Identification
       pid_t pid;                        // Process ID
       pid_t tgid;                       // Thread Group ID (main PID)
       struct task_struct *parent;       // Parent process
       struct list_head children;        // Child processes
       
       // Scheduling
       int prio;                         // Dynamic priority
       int static_prio;                  // Static priority (nice value)
       int normal_prio;                  // Normal priority
       unsigned int rt_priority;         // Real-time priority (0–99)
       unsigned int policy;              // Scheduling policy
       struct sched_entity se;           // CFS scheduling entity
       struct sched_rt_entity rt;        // RT scheduling entity
       struct sched_dl_entity dl;        // Deadline scheduling entity
       
       // CPU affinity
       cpumask_t cpus_mask;              // Allowed CPUs
       int nr_cpus_allowed;              // Number of allowed CPUs
       int on_cpu;                       // Currently running on CPU
       
       // State
       long state;                       // TASK_RUNNING, TASK_INTERRUPTIBLE, etc.
       int exit_state;                   // EXIT_ZOMBIE, EXIT_DEAD
       unsigned int flags;               // PF_KTHREAD, PF_EXITING, etc.
       
       // Memory
       struct mm_struct *mm;             // Virtual memory (NULL for kernel threads)
       
       // Synchronization
       spinlock_t pi_lock;               // Priority inheritance lock
       struct mutex_waiter *blocked_on;  // Mutex waiting on
       
       // Signal handling
       struct signal_struct *signal;     // Signal handlers
       sigset_t blocked;                 // Blocked signals
       struct sigpending pending;        // Pending signals
       
       // Statistics
       u64 utime;                        // User CPU time
       u64 stime;                        // System CPU time
       unsigned long nvcsw;              // Voluntary context switches
       unsigned long nivcsw;             // Involuntary context switches
   };

**1.2 Process States**
-----------------------

.. code-block:: text

   State               Symbol  Meaning                              Runnable?
   ──────────────────  ──────  ───────────────────────────────────  ─────────
   TASK_RUNNING        R       On run queue or running              Yes
   TASK_INTERRUPTIBLE  S       Sleeping (can be woken by signal)    No
   TASK_UNINTERRUPTIBLE D      Sleeping (cannot be interrupted)     No
   __TASK_STOPPED      T       Stopped (SIGSTOP, ptrace)            No
   __TASK_TRACED       t       Traced by debugger                   No
   EXIT_ZOMBIE         Z       Terminated, waiting for wait()       No
   EXIT_DEAD           X       Dead (never visible in ps)           No

**View states:**

.. code-block:: bash

   ps aux | head
   # R = running, S = sleeping, D = disk wait, Z = zombie, T = stopped

**1.3 Process Creation**
-------------------------

.. code-block:: text

   System Call  Copies  Shares Memory  Shares FDs  Use Case
   ───────────  ──────  ─────────────  ──────────  ────────────────────────
   fork()       Yes     No             Dup'd       Classic process creation
   vfork()      No      Shared         Shared      Exec immediately (deprecated)
   clone()      Config  Configurable   Config      Flexible (used by pthread)
   
**Example: fork():**

.. code-block:: c

   pid_t pid = fork();
   
   if (pid < 0) {
       // Fork failed
       perror("fork");
       return -1;
   } else if (pid == 0) {
       // Child process
       printf("Child PID: %d\n", getpid());
       execl("/bin/ls", "ls", "-l", NULL);
   } else {
       // Parent process
       printf("Parent, child PID: %d\n", pid);
       wait(NULL);  // Wait for child to exit
   }

**Example: pthread_create() (maps to clone()):**

.. code-block:: c

   #include <pthread.h>
   
   void *thread_func(void *arg) {
       printf("Thread TID: %ld\n", (long)syscall(SYS_gettid));
       return NULL;
   }
   
   int main() {
       pthread_t thread;
       pthread_create(&thread, NULL, thread_func, NULL);
       pthread_join(thread, NULL);
       return 0;
   }

**Behind the scenes:**

.. code-block:: c

   // pthread_create() calls:
   clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | 
         CLONE_THREAD | CLONE_SYSVSEM, ...);
   
   // CLONE_VM     = Share virtual memory
   // CLONE_THREAD = Share PID (thread group)
   // CLONE_FILES  = Share file descriptor table

================================================================================
2. CFS Scheduler (Completely Fair Scheduler)
================================================================================

**2.1 Overview**
-----------------

**CFS** (default since 2.6.23) aims to provide **fair CPU time** to all tasks.

**Key Concepts:**

- **vruntime (virtual runtime):** Tracks CPU time used by task (weighted by priority)
- **Red-black tree:** Stores tasks sorted by vruntime
- **Scheduler tick:** Updates vruntime, checks preemption (~1000 Hz)
- **Preemption:** Task is preempted if another task has much lower vruntime

**Algorithm:**

.. code-block:: text

   1. Pick task with lowest vruntime from red-black tree
   2. Run task for timeslice (~6 ms / nr_running tasks)
   3. Update vruntime += runtime * weight_factor
   4. Re-insert task into tree
   5. Repeat

**2.2 Nice Values & Priority**
-------------------------------

.. code-block:: text

   Nice Value  Static Priority  Weight Factor  CPU Share (2 tasks)
   ──────────  ───────────────  ─────────────  ───────────────────
   -20         100              88761          ~95% vs nice 0
   -10         110              9548           ~90% vs nice 0
   0           120              1024           50% (baseline)
   +10         130              110            ~10% vs nice 0
   +19         139              15             ~1% vs nice 0

**Formula:**

.. code-block:: text

   vruntime += runtime * (1024 / weight)
   
   Lower nice → higher weight → slower vruntime growth → more CPU

**Set nice value:**

.. code-block:: bash

   # Start with nice +10
   nice -n 10 ./myapp
   
   # Change running process to nice -20 (requires root)
   sudo renice -20 -p 1234
   
   # View nice values
   ps -o pid,ni,comm

**2.3 CFS Tuning Knobs**
-------------------------

.. code-block:: bash

   # Minimum preemption granularity (default: 0.75 ms)
   cat /proc/sys/kernel/sched_min_granularity_ns
   # 750000
   
   # Target latency (default: 6 ms)
   cat /proc/sys/kernel/sched_latency_ns
   # 6000000
   
   # Wakeup granularity (default: 1 ms)
   cat /proc/sys/kernel/sched_wakeup_granularity_ns
   # 1000000

**Tuning examples:**

.. code-block:: bash

   # Reduce latency for interactive workloads
   echo 3000000 | sudo tee /proc/sys/kernel/sched_latency_ns
   
   # Increase throughput for batch workloads
   echo 24000000 | sudo tee /proc/sys/kernel/sched_latency_ns

================================================================================
3. Real-Time Scheduling (SCHED_FIFO / SCHED_RR)
================================================================================

**3.1 Overview**
-----------------

**Real-time policies** always preempt CFS tasks and run until:
- Task blocks (I/O, sleep, mutex)
- Task yields (sched_yield)
- Higher-priority RT task becomes runnable
- (SCHED_RR only) Timeslice expires

**Priority Range:** 1–99 (higher = more important)

.. code-block:: text

   Policy        Preemption               Timeslice
   ────────────  ───────────────────────  ─────────────────────
   SCHED_FIFO    First-In-First-Out       No timeslice (runs until blocks)
   SCHED_RR      Round-robin              Default 100 ms per task

**3.2 Setting Real-Time Priority**
-----------------------------------

.. code-block:: bash

   # Set SCHED_FIFO priority 50
   chrt -f 50 ./myapp
   
   # Set SCHED_RR priority 30
   chrt -r 30 ./myapp
   
   # Change running process to FIFO 80
   sudo chrt -f -p 80 1234
   
   # View RT priority
   chrt -p 1234
   # pid 1234's current scheduling policy: SCHED_FIFO
   # pid 1234's current scheduling priority: 80

**3.3 Kernel API**
-------------------

.. code-block:: c

   #include <linux/sched.h>
   
   // Change scheduling policy from kernel
   struct sched_param param = { .sched_priority = 50 };
   sched_setscheduler(current, SCHED_FIFO, &param);
   
   // Restore to CFS
   param.sched_priority = 0;
   sched_setscheduler(current, SCHED_OTHER, &param);

**Example: RT kernel thread:**

.. code-block:: c

   static int my_rt_thread(void *data) {
       struct sched_param param = { .sched_priority = 80 };
       sched_setscheduler(current, SCHED_FIFO, &param);
       
       while (!kthread_should_stop()) {
           // Critical real-time work
           msleep(10);
       }
       return 0;
   }
   
   struct task_struct *task = kthread_run(my_rt_thread, NULL, "my_rt");

**3.4 RT Throttling**
----------------------

To prevent RT tasks from starving system, kernel throttles RT CPU usage.

.. code-block:: bash

   # RT tasks can use max 95% of CPU time (per CPU)
   cat /proc/sys/kernel/sched_rt_runtime_us
   # 950000  (950 ms out of 1000 ms)
   
   cat /proc/sys/kernel/sched_rt_period_us
   # 1000000  (1 second period)

**Disable throttling (dangerous!):**

.. code-block:: bash

   echo -1 | sudo tee /proc/sys/kernel/sched_rt_runtime_us

================================================================================
4. SCHED_DEADLINE (EDF Scheduler)
================================================================================

**4.1 Overview**
-----------------

**SCHED_DEADLINE** implements **Earliest Deadline First (EDF)** scheduling.

**Parameters:**
- **Runtime:** Maximum execution time per period
- **Deadline:** Relative deadline
- **Period:** Task period

**Example:** Camera frame processing
- Period = 33 ms (30 FPS)
- Runtime = 10 ms (max processing time)
- Deadline = 33 ms (must finish before next frame)

**4.2 Setting SCHED_DEADLINE**
-------------------------------

.. code-block:: bash

   # Runtime: 10 ms, Deadline: 30 ms, Period: 30 ms
   chrt --sched-deadline \
        --sched-runtime  10000000 \
        --sched-deadline 30000000 \
        --sched-period   30000000 \
        0 ./myapp

**4.3 Kernel API**
-------------------

.. code-block:: c

   #include <linux/sched.h>
   
   struct sched_attr attr = {
       .size = sizeof(attr),
       .sched_policy = SCHED_DEADLINE,
       .sched_runtime  = 10 * 1000000ULL,  // 10 ms
       .sched_deadline = 30 * 1000000ULL,  // 30 ms
       .sched_period   = 30 * 1000000ULL,  // 30 ms
   };
   
   sched_setattr(0, &attr, 0);  // 0 = current task

**4.4 Admission Control**
--------------------------

Kernel ensures total utilization ≤ 1.0:

.. code-block:: text

   Sum(runtime_i / period_i) ≤ 1.0

If admission fails, sched_setattr() returns -EBUSY.

================================================================================
5. SMP & CPU Affinity
================================================================================

**5.1 CPU Affinity Overview**
-------------------------------

**CPU affinity** restricts which CPUs a task can run on.

**Benefits:**
- Improved cache locality (L1/L2/L3 cache warmth)
- Predictable latency (avoid migration overhead)
- NUMA optimization (keep task on same NUMA node)

**Costs:**
- Load imbalance (some CPUs idle while others busy)
- Reduced scheduler flexibility

**5.2 Setting Affinity**
-------------------------

.. code-block:: bash

   # Pin to CPU 2
   taskset -c 2 ./myapp
   
   # Pin to CPUs 0,2,3
   taskset -c 0,2-3 ./myapp
   
   # Change running process
   taskset -cp 4-7 1234
   
   # View affinity (hex mask)
   taskset -p 1234
   # pid 1234's current affinity mask: f0  (CPUs 4-7)

**5.3 Kernel API**
-------------------

.. code-block:: c

   #include <linux/sched.h>
   #include <linux/cpumask.h>
   
   // Set affinity to CPUs 0,2
   cpumask_t mask;
   cpumask_clear(&mask);
   cpumask_set_cpu(0, &mask);
   cpumask_set_cpu(2, &mask);
   
   set_cpus_allowed_ptr(current, &mask);
   
   // Get current affinity
   cpumask_t *allowed = &current->cpus_mask;

**5.4 Per-CPU Variables**
--------------------------

For SMP-safe access to per-CPU data:

.. code-block:: c

   #include <linux/percpu.h>
   
   // Declare per-CPU variable
   DEFINE_PER_CPU(unsigned long, my_counter);
   
   // Access on current CPU (preemption disabled)
   unsigned long *counter = this_cpu_ptr(&my_counter);
   (*counter)++;
   
   // Atomic increment on current CPU
   this_cpu_inc(my_counter);
   
   // Sum across all CPUs
   unsigned long total = 0;
   int cpu;
   for_each_possible_cpu(cpu) {
       total += per_cpu(my_counter, cpu);
   }

**5.5 Interrupt Affinity**
---------------------------

.. code-block:: bash

   # View IRQ affinity
   cat /proc/irq/44/smp_affinity
   # ffffffff  (all CPUs)
   
   # Pin IRQ 44 to CPUs 4-7
   echo f0 | sudo tee /proc/irq/44/smp_affinity
   
   # Check which CPU handles IRQ
   watch -n 1 'cat /proc/interrupts | grep eth0'

**Kernel API:**

.. code-block:: c

   #include <linux/interrupt.h>
   
   // Set IRQ affinity hint
   irq_set_affinity_hint(irq, cpumask_of(2));  // CPU 2

================================================================================
6. Load Balancing & Scheduling Domains
================================================================================

**6.1 Scheduling Domains**
---------------------------

Linux organizes CPUs into hierarchical **scheduling domains**:

.. code-block:: text

   Level        Domain Type        Scope                    Example (2-socket × 8-core)
   ───────────  ─────────────────  ───────────────────────  ──────────────────────────
   1 (lowest)   SMT (siblings)     Hyperthreads             CPU 0,16 (same core)
   2            MC (multi-core)    Cores sharing L3 cache   CPU 0-7 (socket 0)
   3            DIE                Cores on same die        CPU 0-7 (socket 0)
   4 (highest)  NUMA               All CPUs in NUMA node    CPU 0-15 (node 0)

**6.2 Load Balancing Algorithm**
----------------------------------

.. code-block:: text

   Trigger                  Action
   ───────────────────────  ──────────────────────────────────────────────
   Tick (every ~4 ms)       Check domain-specific balance interval
   CPU becomes idle         Pull tasks from busiest sibling
   Task wakeup              Try to place on cache-warm CPU
   exec()                   Select least-loaded CPU

**6.3 Tuning Load Balancing**
------------------------------

.. code-block:: bash

   # Disable load balancing for isolated CPUs
   isolcpus=4-7
   
   # View scheduling domains
   cat /proc/sys/kernel/sched_domain/cpu0/domain*/name
   # MC
   # NUMA

**6.4 NUMA Balancing**
-----------------------

.. code-block:: bash

   # Enable automatic NUMA balancing
   echo 1 | sudo tee /proc/sys/kernel/numa_balancing
   
   # View NUMA stats
   numastat -c myapp

**Bind task to NUMA node:**

.. code-block:: bash

   numactl --cpunodebind=0 --membind=0 ./myapp

================================================================================
7. Kernel Threads & Work Queues
================================================================================

**7.1 Creating Kernel Threads**
--------------------------------

.. code-block:: c

   #include <linux/kthread.h>
   
   static int my_thread_fn(void *data) {
       while (!kthread_should_stop()) {
           // Do work
           printk("Thread running on CPU %d\n", smp_processor_id());
           msleep(1000);
       }
       return 0;
   }
   
   static int __init my_init(void) {
       struct task_struct *task;
       
       task = kthread_run(my_thread_fn, NULL, "my_kthread");
       if (IS_ERR(task)) {
           return PTR_ERR(task);
       }
       
       // Store task pointer to stop later
       return 0;
   }
   
   static void __exit my_exit(void) {
       if (task)
           kthread_stop(task);
   }

**7.2 Work Queues**
--------------------

For deferring work to process context (can sleep).

.. code-block:: c

   #include <linux/workqueue.h>
   
   static void my_work_handler(struct work_struct *work) {
       printk("Work running on CPU %d\n", smp_processor_id());
   }
   
   static DECLARE_WORK(my_work, my_work_handler);
   
   // Schedule work
   schedule_work(&my_work);  // Uses system_wq
   
   // Create dedicated workqueue
   struct workqueue_struct *my_wq = create_singlethread_workqueue("my_wq");
   queue_work(my_wq, &my_work);
   
   // Cleanup
   flush_workqueue(my_wq);
   destroy_workqueue(my_wq);

**7.3 Tasklets (softirq context)**
-----------------------------------

.. code-block:: c

   #include <linux/interrupt.h>
   
   static void my_tasklet_fn(unsigned long data) {
       // Cannot sleep! (softirq context)
       printk("Tasklet running\n");
   }
   
   static DECLARE_TASKLET(my_tasklet, my_tasklet_fn, 0);
   
   // Schedule tasklet (from IRQ handler)
   tasklet_schedule(&my_tasklet);

================================================================================
8. Synchronization Primitives
================================================================================

**8.1 Spinlocks**
------------------

.. code-block:: c

   #include <linux/spinlock.h>
   
   static DEFINE_SPINLOCK(my_lock);
   
   // Lock (disables preemption on local CPU)
   spin_lock(&my_lock);
   // Critical section
   spin_unlock(&my_lock);
   
   // Lock + disable interrupts
   unsigned long flags;
   spin_lock_irqsave(&my_lock, flags);
   // Critical section
   spin_unlock_irqrestore(&my_lock, flags);

**8.2 Mutexes**
----------------

.. code-block:: c

   #include <linux/mutex.h>
   
   static DEFINE_MUTEX(my_mutex);
   
   // Lock (can sleep)
   mutex_lock(&my_mutex);
   // Critical section (may sleep, call schedule())
   mutex_unlock(&my_mutex);
   
   // Trylock
   if (mutex_trylock(&my_mutex)) {
       // Got lock
       mutex_unlock(&my_mutex);
   }

**8.3 Completions**
--------------------

.. code-block:: c

   #include <linux/completion.h>
   
   static DECLARE_COMPLETION(my_completion);
   
   // Thread A: Wait for event
   wait_for_completion(&my_completion);
   
   // Thread B: Signal event
   complete(&my_completion);

**8.4 Wait Queues**
--------------------

.. code-block:: c

   #include <linux/wait.h>
   
   static DECLARE_WAIT_QUEUE_HEAD(my_wq);
   static int condition = 0;
   
   // Wait for condition
   wait_event_interruptible(my_wq, condition != 0);
   
   // Wake up waiters
   condition = 1;
   wake_up_interruptible(&my_wq);

================================================================================
9. Namespaces & Containers
================================================================================

**9.1 Namespace Types**
------------------------

.. code-block:: text

   Namespace  Isolates                    Flag
   ─────────  ──────────────────────────  ──────────────
   PID        Process IDs                 CLONE_NEWPID
   NET        Network stack, interfaces   CLONE_NEWNET
   MNT        Mount points                CLONE_NEWNS
   UTS        Hostname, domain name       CLONE_NEWUTS
   IPC        IPC objects (SysV, POSIX)   CLONE_NEWIPC
   USER       User/group IDs              CLONE_NEWUSER
   CGROUP     Cgroup hierarchy            CLONE_NEWCGROUP
   TIME       System clocks               CLONE_NEWTIME

**9.2 Creating Namespaces**
----------------------------

.. code-block:: c

   // Create process in new PID namespace
   clone(child_fn, stack, CLONE_NEWPID | SIGCHLD, NULL);
   
   // Inside child:
   // - getpid() returns 1 (init process in new namespace)
   // - Cannot see parent's processes

**9.3 Entering Namespaces (setns)**
------------------------------------

.. code-block:: bash

   # View namespaces
   ls -l /proc/self/ns/
   # pid -> pid:[4026531836]
   # net -> net:[4026531905]
   
   # Enter PID namespace of process 1234
   nsenter -t 1234 -p /bin/bash

**9.4 Unshare (create new namespace for current process)**
------------------------------------------------------------

.. code-block:: bash

   # Create new network namespace
   unshare --net /bin/bash
   
   # Now isolated network stack
   ip addr show
   # Only loopback visible

================================================================================
10. Cgroups v2 — CPU Control
================================================================================

**10.1 CPU Controller**
------------------------

.. code-block:: bash

   # Create cgroup
   mkdir /sys/fs/cgroup/my_container
   
   # Set CPU weight (default 100, range 1-10000)
   echo 200 > /sys/fs/cgroup/my_container/cpu.weight
   # 2× more CPU than default
   
   # Set CPU quota (100 ms per 1000 ms = 10% CPU)
   echo "100000 1000000" > /sys/fs/cgroup/my_container/cpu.max
   
   # Move process into cgroup
   echo 1234 > /sys/fs/cgroup/my_container/cgroup.procs

**10.2 CPU Stats**
-------------------

.. code-block:: bash

   cat /sys/fs/cgroup/my_container/cpu.stat
   # usage_usec 123456789
   # user_usec 100000000
   # system_usec 23456789
   # nr_periods 1000
   # nr_throttled 50
   # throttled_usec 5000000

**10.3 RT Bandwidth**
----------------------

.. code-block:: bash

   # Limit RT tasks to 50% of CPU (500 ms per second)
   echo 500000 > /sys/fs/cgroup/my_container/cpu.rt_runtime_us

================================================================================
11. Debugging & Profiling
================================================================================

**11.1 Process Information**
-----------------------------

.. code-block:: bash

   # View all processes
   ps aux
   ps -eLf  # Include threads
   
   # Custom columns
   ps -o pid,tid,class,rtprio,ni,psr,comm
   # psr = CPU currently running on
   
   # Process tree
   pstree -p 1234
   
   # Thread view
   ps -T -p 1234

**11.2 Scheduling Statistics**
-------------------------------

.. code-block:: bash

   # Per-process scheduling info
   cat /proc/1234/sched
   # se.sum_exec_runtime      : 123456.789
   # se.vruntime              : 234567.890
   # nr_switches              : 10000
   # nr_voluntary_switches    : 5000
   # nr_involuntary_switches  : 5000
   
   # System-wide stats
   cat /proc/schedstat

**11.3 CPU Usage (top/htop)**
------------------------------

.. code-block:: bash

   # Interactive monitoring
   top -H  # Thread view
   htop    # Better UI
   
   # Sort by CPU
   top -o %CPU
   
   # Per-CPU view (press '1' in top)
   top
   # Shows individual CPU usage

**11.4 Tracing**
-----------------

.. code-block:: bash

   # Trace scheduler events
   trace-cmd record -e sched  # Ctrl+C to stop
   trace-cmd report
   
   # Trace specific process
   trace-cmd record -e sched -P 1234
   
   # Function graph (shows call stack)
   trace-cmd record -p function_graph -F schedule
   
   # Perf scheduler analysis
   perf sched record  # Ctrl+C to stop
   perf sched latency  # Show scheduling latencies
   perf sched map      # Visual timeline

**11.5 Context Switch Monitoring**
-----------------------------------

.. code-block:: bash

   # System-wide context switches
   vmstat 1
   # cs column = context switches per second
   
   # Per-process context switches
   cat /proc/1234/status | grep ctxt
   # voluntary_ctxt_switches:    5000
   # nonvoluntary_ctxt_switches: 1000

================================================================================
12. Exam Preparation — 5 Questions
================================================================================

**Question 1: CFS Scheduler (12 points)**

Two tasks run on single-CPU system:
- Task A: nice 0, vruntime = 100 ms
- Task B: nice +10, vruntime = 50 ms

a) Which task will CFS schedule next? Why? (4 pts)
b) If Task B runs for 10 ms, what is its new vruntime? (4 pts)
c) How would nice -10 for Task A affect scheduling? (4 pts)

**Answer:**

a) **CFS schedules Task B**
   - CFS always picks task with **lowest vruntime**
   - Task B: vruntime = 50 ms
   - Task A: vruntime = 100 ms
   - 50 < 100 → Task B runs next

b) **Task B new vruntime:**

.. code-block:: text

   Nice +10 → weight ≈ 110 (from weight table)
   Nice 0   → weight = 1024
   
   vruntime += runtime * (1024 / weight)
             = 10 ms * (1024 / 110)
             = 10 * 9.31
             ≈ 93 ms
   
   New vruntime = 50 + 93 = 143 ms

c) **Nice -10 for Task A:**

.. code-block:: text

   Nice -10 → weight ≈ 9548
   
   vruntime increment for 10 ms runtime:
   = 10 * (1024 / 9548)
   = 10 * 0.107
   ≈ 1 ms
   
   Effect:
   - Task A gets ~9× more CPU time than Task B
   - Task A vruntime grows 9× slower
   - Scheduler heavily favors Task A

---

**Question 2: Real-Time Priority Inversion (14 points)**

System has 3 tasks:
- Task H: SCHED_FIFO priority 90 (high)
- Task M: SCHED_FIFO priority 50 (medium)
- Task L: SCHED_FIFO priority 10 (low)

Scenario:
1. Task L acquires mutex
2. Task H blocks on same mutex
3. Task M becomes runnable

a) What is priority inversion? (4 pts)
b) Which task runs in step 3? Why is this a problem? (5 pts)
c) How does priority inheritance solve this? (5 pts)

**Answer:**

a) **Priority inversion:**
   - High-priority task blocked by low-priority task
   - Violates real-time priority semantics
   - Can cause unbounded delays (medium-priority tasks run)

b) **Task M runs in step 3:**

.. code-block:: text

   Current state:
   - Task H: blocked on mutex (not runnable)
   - Task L: owns mutex, runnable, priority 10
   - Task M: runnable, priority 50
   
   Scheduler picks Task M (highest runnable priority)
   
   Problem:
   - Task H (prio 90) indirectly blocked by Task M (prio 50)
   - Task M has lower priority than Task H!
   - Unbounded delay if Task M runs for long time
   - Classic priority inversion problem

c) **Priority inheritance:**

.. code-block:: text

   Solution:
   1. When Task H blocks on mutex owned by Task L:
      → Boost Task L priority to 90 (inherit from Task H)
   
   2. Now Task L runs (priority 90 > Task M priority 50)
   
   3. Task L finishes critical section, releases mutex
      → Task L priority restored to 10
      → Task H acquires mutex, runs
   
   Result:
   - Task M cannot delay Task H
   - Bounded priority inversion (only critical section length)

**Linux implementation:**

.. code-block:: c

   // Use rt_mutex (has priority inheritance)
   #include <linux/rtmutex.h>
   
   static DEFINE_RT_MUTEX(my_mutex);
   
   rt_mutex_lock(&my_mutex);
   // Critical section
   rt_mutex_unlock(&my_mutex);

---

**Question 3: CPU Affinity & Cache (12 points)**

System: 4-core CPU, each core has private 32 KB L1 cache, shared 8 MB L3 cache.

Task processes 1 MB data array repeatedly. Without affinity, scheduler migrates task between CPUs frequently.

a) What cache problem occurs due to migration? (4 pts)
b) How does CPU affinity improve performance? (4 pts)
c) When would affinity hurt performance? (4 pts)

**Answer:**

a) **Cache problem (cold cache on migration):**

.. code-block:: text

   Scenario:
   1. Task runs on CPU 0
      → Loads 1 MB data into L1/L3 cache (warm cache)
   
   2. Scheduler migrates task to CPU 1
      → CPU 1 L1 cache is cold (doesn't have data)
      → Must fetch from L3 or RAM
   
   3. Task accesses data
      → L1 cache misses (cold)
      → ~100 ns L3 hit or ~100 ns RAM hit
   
   Cost:
   - 1 MB / 64 bytes = ~16,000 cache lines
   - 16,000 × 100 ns = 1.6 ms cache warming overhead
   - Repeated on every migration!

b) **Affinity improves performance:**

.. code-block:: bash

   taskset -c 2 ./myapp  # Pin to CPU 2

.. code-block:: text

   Benefits:
   1. Cache stays warm (no migration)
      - L1 cache hit rate: ~95%
      - Access latency: ~4 cycles (~1 ns)
   
   2. TLB stays warm
      - Fewer TLB misses (page table walks expensive)
   
   3. Predictable performance
      - No migration jitter
   
   Speedup:
   - Typical: 2-5× for cache-intensive workloads
   - Extreme: 10× for tiny hot loops that fit in L1

c) **When affinity hurts:**

.. code-block:: text

   Scenario 1: Load imbalance
   - Pin task to CPU 2
   - CPUs 0,1,3 idle, CPU 2 100% busy
   - Wasted CPU capacity
   
   Scenario 2: Shared resources
   - 2 tasks pinned to same CPU
   - Other CPUs idle
   - Better: Let scheduler balance
   
   Scenario 3: Large working set
   - Data >> cache size (e.g., 100 MB)
   - Cache always cold anyway
   - Affinity provides no benefit
   
   Recommendation:
   - Use affinity for latency-critical tasks with small working set
   - Let scheduler handle throughput workloads

---

**Question 4: SCHED_DEADLINE Admission (10 points)**

System has 4 CPUs. Three SCHED_DEADLINE tasks:
- Task A: runtime 20 ms, period 100 ms
- Task B: runtime 30 ms, period 100 ms
- Task C: runtime 40 ms, period 200 ms

a) Calculate total CPU utilization. (5 pts)
b) Will kernel admit Task C? (5 pts)

**Answer:**

a) **CPU utilization:**

.. code-block:: text

   U = Sum(runtime_i / period_i)
   
   U_A = 20 / 100 = 0.20 (20%)
   U_B = 30 / 100 = 0.30 (30%)
   U_C = 40 / 200 = 0.20 (20%)
   
   U_total = 0.20 + 0.30 + 0.20 = 0.70 (70%)

b) **Admission decision:**

.. code-block:: text

   System capacity = 4 CPUs = 4.0
   Required utilization = 0.70
   
   0.70 < 4.0 → ✓ Admission succeeds
   
   Explanation:
   - 70% utilization across 4 CPUs
   - Average 0.175 per CPU (well below 100%)
   - EDF can schedule this workload
   
   Note:
   - If total was > 4.0, admission would fail (EBUSY)
   - Kernel guarantees schedulability if admitted

---

**Question 5: SMP Synchronization (12 points)**

Driver maintains global counter, incremented in interrupt handler (can occur on any CPU).

a) Why is ``counter++`` not SMP-safe? (4 pts)
b) Compare spinlock vs atomic_t for this use case. (8 pts)

**Answer:**

a) **Not SMP-safe:**

.. code-block:: text

   counter++ compiles to:
   1. LOAD  counter → register
   2. ADD   register, 1
   3. STORE register → counter
   
   Race condition (2 CPUs):
   
   CPU 0                    CPU 1                    counter
   ─────────────────────    ─────────────────────    ───────
   LOAD counter (50)                                 50
                            LOAD counter (50)        50
   ADD 1 (51)                                        50
                            ADD 1 (51)               50
   STORE 51                                          51
                            STORE 51                 51
   
   Result: counter = 51 (should be 52!)
   Lost update problem

b) **spinlock vs atomic_t:**

.. code-block:: c

   // Method 1: Spinlock
   static DEFINE_SPINLOCK(counter_lock);
   static unsigned long counter = 0;
   
   // In IRQ handler
   spin_lock(&counter_lock);
   counter++;
   spin_unlock(&counter_lock);
   
   // Method 2: atomic_t
   static atomic_t counter = ATOMIC_INIT(0);
   
   // In IRQ handler
   atomic_inc(&counter);

**Comparison:**

.. code-block:: text

   Aspect          Spinlock                 atomic_t
   ──────────────  ───────────────────────  ──────────────────────────
   Correctness     ✓ Correct                ✓ Correct
   Performance     Slower (lock overhead)   Faster (lockless)
   Scalability     Poor (cache bouncing)    Excellent (LOCK INC)
   Flexibility     Can protect multiple     Single counter only
                   variables
   Code size       More verbose             Concise
   
   Benchmark (4 CPUs, 1M increments):
   - Spinlock:  ~500 ms (cache line ping-pong)
   - atomic_t:  ~50 ms (10× faster)
   
   Recommendation: Use atomic_t for simple counters

**Read value:**

.. code-block:: c

   // Spinlock
   spin_lock(&counter_lock);
   unsigned long val = counter;
   spin_unlock(&counter_lock);
   
   // atomic_t
   unsigned long val = atomic_read(&counter);  // Lockless read

================================================================================
13. Completion Checklist
================================================================================

□ Understand task_struct and process states (R, S, D, Z)
□ Know difference between fork(), vfork(), clone()
□ Understand CFS vruntime and nice values
□ Set real-time priority with chrt (SCHED_FIFO, SCHED_RR)
□ Use SCHED_DEADLINE for hard real-time tasks
□ Pin tasks to CPUs with taskset (CPU affinity)
□ Create kernel threads with kthread_run
□ Use work queues for deferring work to process context
□ Understand spinlocks vs mutexes (when to use each)
□ Use completions and wait queues for synchronization
□ Isolate processes with namespaces (PID, NET, MNT, etc.)
□ Limit CPU usage with cgroups v2 (cpu.weight, cpu.max)
□ Debug scheduling with /proc/<pid>/sched and perf sched
□ Avoid priority inversion with rt_mutex (priority inheritance)
□ Use atomic_t for lockless counters
□ Understand false sharing and cache line alignment

================================================================================
14. Key Takeaways
================================================================================

1. **task_struct** represents both processes and threads (all are tasks)

2. **CFS** provides fair scheduling via vruntime (weighted by nice value)

3. **Real-time tasks** (SCHED_FIFO/RR) always preempt CFS tasks

4. **SCHED_DEADLINE** uses EDF for hard real-time guarantees

5. **CPU affinity** improves cache locality but can cause load imbalance

6. **Per-CPU variables** avoid locking (``this_cpu_ptr``, ``this_cpu_inc``)

7. **Spinlocks** for short critical sections (cannot sleep)

8. **Mutexes** for longer critical sections (can sleep)

9. **Namespaces** provide process isolation (containers)

10. **Cgroups** limit CPU/memory usage per container

11. **Priority inheritance** (rt_mutex) solves priority inversion

12. **Atomic operations** (atomic_t) faster than spinlocks for counters

13. **Load balancing** migrates tasks across CPUs for fairness

14. **Kernel threads** run in process context (can sleep)

15. **Work queues** defer work from interrupt to process context

16. **Scheduling domains** optimize load balancing for cache/NUMA

================================================================================
References & Further Reading
================================================================================

**Books:**
- Professional Linux Kernel Architecture (Wolfgang Mauerer)
- Linux Kernel Development (Robert Love)
- Understanding the Linux Kernel (Bovet & Cesati)

**Kernel Documentation:**
- Documentation/scheduler/sched-design-CFS.rst
- Documentation/scheduler/sched-rt-group.rst
- Documentation/scheduler/sched-deadline.rst
- Documentation/admin-guide/cgroup-v2.rst

**Source Code:**
- kernel/sched/core.c (scheduler core)
- kernel/sched/fair.c (CFS)
- kernel/sched/rt.c (real-time)
- kernel/sched/deadline.c (EDF)

**Tools:**
- chrt, taskset, nice, renice
- top, htop, ps, pstree
- perf sched, trace-cmd
- /proc/schedstat, /proc/<pid>/sched

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Kernel Version:** Linux 6.12–6.16

================================================================================
