=========================================
Linux CPU Scheduling Internals
=========================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Focus: CPU scheduler internals and algorithms

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Scheduler Overview
------------------

.. code-block:: text

   Linux Scheduler Classes (priority order):
   
   1. Stop (highest priority)
      - CPU stop tasks
      - Priority: -1
   
   2. Deadline (SCHED_DEADLINE)
      - Real-time deadline scheduling
      - EDF (Earliest Deadline First)
      - Priority: 0
   
   3. Real-Time (SCHED_FIFO, SCHED_RR)
      - Fixed-priority real-time
      - Priority: 1-99
   
   4. Fair (SCHED_NORMAL, SCHED_BATCH)
      - CFS (Completely Fair Scheduler)
      - Priority: 100-139 (nice -20 to +19)
   
   5. Idle (SCHED_IDLE)
      - Idle tasks
      - Priority: 140

Essential Scheduler APIs
------------------------

.. code-block:: c

   // Set scheduling policy
   sched_setscheduler(pid, policy, &param);
   
   // Set priority
   setpriority(PRIO_PROCESS, pid, nice_value);
   
   // Yield CPU
   schedule();
   cond_resched();  // Conditional reschedule
   
   // Sleep
   schedule_timeout(timeout);
   msleep(msecs);
   msleep_interruptible(msecs);

Scheduler Core
==============

Runqueue Structure
------------------

.. code-block:: c

   // Per-CPU runqueue
   struct rq {
       raw_spinlock_t lock;
       unsigned int nr_running;          // Number of runnable tasks
       u64 clock;                        // Runqueue clock
       u64 clock_task;                   // Task clock
       
       struct cfs_rq cfs;                // CFS runqueue
       struct rt_rq rt;                  // RT runqueue
       struct dl_rq dl;                  // Deadline runqueue
       
       struct task_struct *curr;         // Currently running task
       struct task_struct *idle;         // Idle task
       struct task_struct *stop;         // Stop task
       
       unsigned long nr_uninterruptible; // Uninterruptible tasks
       
       u64 nr_switches;                  // Context switches
       u64 nr_migrations;                // Task migrations
       
       int cpu;                          // CPU number
       int online;                       // CPU online status
       
       struct sched_domain *sd;          // Scheduling domain
       
       #ifdef CONFIG_SMP
       struct root_domain *rd;           // Root domain
       unsigned long cpu_capacity;       // CPU capacity
       unsigned char idle_balance;       // Idle balancing flag
       #endif
   };

Scheduling Entity
-----------------

.. code-block:: c

   // CFS scheduling entity
   struct sched_entity {
       struct load_weight load;          // Task weight
       struct rb_node run_node;          // Red-black tree node
       struct list_head group_node;
       unsigned int on_rq;               // On runqueue flag
       
       u64 exec_start;                   // Execution start time
       u64 sum_exec_runtime;             // Total execution time
       u64 vruntime;                     // Virtual runtime (CFS)
       u64 prev_sum_exec_runtime;
       
       u64 nr_migrations;
       
       #ifdef CONFIG_FAIR_GROUP_SCHED
       struct sched_entity *parent;
       struct cfs_rq *cfs_rq;            // CFS runqueue on
       struct cfs_rq *my_q;              // CFS runqueue I own
       #endif
   };
   
   // Real-time scheduling entity
   struct sched_rt_entity {
       struct list_head run_list;
       unsigned long timeout;
       unsigned long watchdog_stamp;
       unsigned int time_slice;          // RR time slice
       unsigned short on_rq;
       unsigned short on_list;
       
       struct sched_rt_entity *parent;
       struct rt_rq *rt_rq;
       struct rt_rq *my_q;
   };
   
   // Deadline scheduling entity
   struct sched_dl_entity {
       struct rb_node rb_node;
       u64 dl_runtime;                   // Maximum runtime
       u64 dl_deadline;                  // Relative deadline
       u64 dl_period;                    // Separation of two instances
       u64 dl_bw;                        // Utilization
       
       s64 runtime;                      // Remaining runtime
       u64 deadline;                     // Absolute deadline
       
       unsigned int flags;
       int dl_throttled;
       int dl_yielded;
       int dl_non_contending;
       int dl_overrun;
   };

CFS (Completely Fair Scheduler)
================================

CFS Concept
-----------

.. code-block:: text

   CFS Virtual Runtime:
   
   - Each task accumulates "virtual runtime" (vruntime)
   - vruntime increases slower for high-priority tasks
   - vruntime increases faster for low-priority tasks
   - Scheduler always picks task with smallest vruntime
   
   vruntime calculation:
   vruntime += (actual_runtime * NICE_0_LOAD) / weight
   
   Weight based on nice value:
   nice -20: weight = 88761 (highest priority)
   nice   0: weight =  1024 (normal)
   nice +19: weight =    15 (lowest priority)

CFS Runqueue
------------

.. code-block:: c

   // CFS runqueue
   struct cfs_rq {
       struct load_weight load;
       unsigned int nr_running;          // Number of tasks
       unsigned int h_nr_running;        // Hierarchical nr_running
       
       u64 exec_clock;
       u64 min_vruntime;                 // Minimum vruntime
       
       struct rb_root_cached tasks_timeline;  // Red-black tree
       
       struct sched_entity *curr;        // Currently running
       struct sched_entity *next;        // Next to run
       struct sched_entity *last;        // Last ran
       struct sched_entity *skip;        // Skip for balancing
   };

CFS Scheduling Algorithm
-------------------------

.. code-block:: c

   // Pick next task (simplified)
   static struct task_struct *pick_next_task_fair(struct rq *rq) {
       struct cfs_rq *cfs_rq = &rq->cfs;
       struct sched_entity *se;
       
       if (!cfs_rq->nr_running)
           return NULL;
       
       // Get leftmost (minimum vruntime) task
       se = __pick_first_entity(cfs_rq);
       set_next_entity(cfs_rq, se);
       
       return task_of(se);
   }
   
   // Update virtual runtime
   static void update_curr(struct cfs_rq *cfs_rq) {
       struct sched_entity *curr = cfs_rq->curr;
       u64 now = rq_clock_task(rq_of(cfs_rq));
       u64 delta_exec;
       
       if (!curr)
           return;
       
       delta_exec = now - curr->exec_start;
       curr->exec_start = now;
       
       curr->sum_exec_runtime += delta_exec;
       
       // Update vruntime
       curr->vruntime += calc_delta_fair(delta_exec, curr);
       update_min_vruntime(cfs_rq);
   }
   
   // Enqueue task
   static void enqueue_task_fair(struct rq *rq, struct task_struct *p, int flags) {
       struct cfs_rq *cfs_rq;
       struct sched_entity *se = &p->se;
       
       for_each_sched_entity(se) {
           cfs_rq = cfs_rq_of(se);
           enqueue_entity(cfs_rq, se, flags);
           cfs_rq->h_nr_running++;
           cfs_rq->idle_h_nr_running += idle_h_nr_running;
           flags = ENQUEUE_WAKEUP;
       }
   }
   
   // Dequeue task
   static void dequeue_task_fair(struct rq *rq, struct task_struct *p, int flags) {
       struct cfs_rq *cfs_rq;
       struct sched_entity *se = &p->se;
       
       for_each_sched_entity(se) {
           cfs_rq = cfs_rq_of(se);
           dequeue_entity(cfs_rq, se, flags);
           cfs_rq->h_nr_running--;
           flags |= DEQUEUE_SLEEP;
       }
   }

Real-Time Scheduling
====================

RT Runqueue
-----------

.. code-block:: c

   // Real-time runqueue
   struct rt_rq {
       struct rt_prio_array active;      // Priority queues
       unsigned int rt_nr_running;       // Number of RT tasks
       unsigned int rr_nr_running;       // Number of RR tasks
       
       struct {
           int curr;                     // Highest priority with task
           int next;                     // Next highest
       } highest_prio;
       
       u64 rt_runtime;                   // Runtime allocated
       u64 rt_time;                      // Time consumed
       int rt_throttled;                 // Throttled flag
       u64 rt_period;                    // Period
       
       struct rq *rq;
   };
   
   // Priority array (one list per priority)
   struct rt_prio_array {
       DECLARE_BITMAP(bitmap, MAX_RT_PRIO+1);  // Bitmap of active priorities
       struct list_head queue[MAX_RT_PRIO];     // Task lists
   };

RT Scheduling
-------------

.. code-block:: c

   // Pick next RT task
   static struct task_struct *pick_next_task_rt(struct rq *rq) {
       struct rt_rq *rt_rq = &rq->rt;
       struct rt_prio_array *array = &rt_rq->active;
       struct sched_rt_entity *rt_se;
       int idx;
       
       if (!rt_rq->rt_nr_running)
           return NULL;
       
       // Find highest priority with runnable task
       idx = sched_find_first_bit(array->bitmap);
       rt_se = list_entry(array->queue[idx].next,
                         struct sched_rt_entity, run_list);
       
       return rt_task_of(rt_se);
   }
   
   // SCHED_FIFO: Runs until blocks or yields
   // SCHED_RR: Round-robin with time slice
   static void task_tick_rt(struct rq *rq, struct task_struct *p, int queued) {
       struct sched_rt_entity *rt_se = &p->rt;
       
       update_curr_rt(rq);
       
       // Check for RR time slice expiration
       if (p->policy != SCHED_RR)
           return;
       
       if (--p->rt.time_slice)
           return;
       
       // Time slice expired, requeue
       p->rt.time_slice = sched_rr_timeslice;
       
       // Move to end of priority queue
       requeue_task_rt(rq, p, 0);
       resched_curr(rq);
   }

Deadline Scheduling
===================

Deadline Runqueue
-----------------

.. code-block:: c

   // Deadline runqueue
   struct dl_rq {
       struct rb_root_cached root;       // Red-black tree (by deadline)
       unsigned int dl_nr_running;       // Number of tasks
       
       struct {
           u64 curr;                     // Current task deadline
           u64 next;                     // Next task deadline
       } earliest_dl;
       
       u64 running_bw;                   // Total bandwidth
       u64 this_bw;                      // This CPU bandwidth
       u64 extra_bw;                     // Extra bandwidth
       
       u64 bw_ratio;
   };

Deadline Algorithm (EDF)
------------------------

.. code-block:: c

   // Earliest Deadline First
   static struct task_struct *pick_next_task_dl(struct rq *rq) {
       struct dl_rq *dl_rq = &rq->dl;
       struct sched_dl_entity *dl_se;
       struct rb_node *left;
       
       if (!dl_rq->dl_nr_running)
           return NULL;
       
       // Get task with earliest deadline (leftmost in tree)
       left = rb_first_cached(&dl_rq->root);
       if (!left)
           return NULL;
       
       dl_se = rb_entry(left, struct sched_dl_entity, rb_node);
       return dl_task_of(dl_se);
   }
   
   // Update deadline runtime
   static void update_curr_dl(struct rq *rq) {
       struct task_struct *curr = rq->curr;
       struct sched_dl_entity *dl_se = &curr->dl;
       u64 delta_exec;
       
       delta_exec = rq_clock_task(rq) - curr->se.exec_start;
       
       dl_se->runtime -= delta_exec;
       if (dl_se->runtime <= 0) {
           // Budget exhausted
           dl_se->dl_throttled = 1;
           __dequeue_task_dl(rq, curr, 0);
           
           // Replenish at next period
           replenish_dl_entity(dl_se);
           enqueue_task_dl(rq, curr, ENQUEUE_REPLENISH);
       }
   }

Context Switching
=================

Schedule Function
-----------------

.. code-block:: c

   // Main scheduler function
   asmlinkage __visible void __sched schedule(void) {
       struct task_struct *tsk = current;
       
       sched_submit_work(tsk);
       do {
           preempt_disable();
           __schedule(false);
           sched_preempt_enable_no_resched();
       } while (need_resched());
       sched_update_worker(tsk);
   }
   
   // Core scheduling
   static void __sched notrace __schedule(bool preempt) {
       struct task_struct *prev, *next;
       unsigned long *switch_count;
       struct rq *rq;
       int cpu;
       
       cpu = smp_processor_id();
       rq = cpu_rq(cpu);
       prev = rq->curr;
       
       // Pick next task
       next = pick_next_task(rq, prev);
       
       if (likely(prev != next)) {
           rq->nr_switches++;
           rq->curr = next;
           ++*switch_count;
           
           // Context switch
           rq = context_switch(rq, prev, next);
           cpu = cpu_of(rq);
       }
   }

Context Switch Implementation
------------------------------

.. code-block:: c

   // Switch context
   static __always_inline struct rq *
   context_switch(struct rq *rq, struct task_struct *prev,
                  struct task_struct *next) {
       struct mm_struct *mm, *oldmm;
       
       prepare_task_switch(rq, prev, next);
       
       mm = next->mm;
       oldmm = prev->active_mm;
       
       // Switch memory context
       if (!mm) {
           // Kernel thread
           next->active_mm = oldmm;
           mmgrab(oldmm);
           enter_lazy_tlb(oldmm, next);
       } else {
           // User thread
           switch_mm_irqs_off(oldmm, mm, next);
       }
       
       // Switch CPU context (registers, stack)
       switch_to(prev, next, prev);
       
       barrier();
       return finish_task_switch(prev);
   }

Load Balancing
==============

Scheduling Domains
------------------

.. code-block:: c

   struct sched_domain {
       struct sched_domain *parent;      // Parent domain
       struct sched_domain *child;       // Child domain
       struct sched_group *groups;       // Groups in domain
       
       unsigned long min_interval;       // Min balance interval
       unsigned long max_interval;       // Max balance interval
       unsigned int busy_factor;
       unsigned int imbalance_pct;       // Imbalance percentage
       unsigned int cache_nice_tries;
       unsigned int busy_idx;
       unsigned int idle_idx;
       unsigned int flags;               // Domain flags
       int level;
       
       char *name;
   };

Load Balancing
--------------

.. code-block:: c

   // Periodic load balance
   static void rebalance_domains(struct rq *rq, enum cpu_idle_type idle) {
       int continue_balancing = 1;
       int cpu = rq->cpu;
       unsigned long interval;
       struct sched_domain *sd;
       
       rcu_read_lock();
       for_each_domain(cpu, sd) {
           if (!(sd->flags & SD_LOAD_BALANCE))
               continue;
           
           interval = get_sd_balance_interval(sd, idle != CPU_IDLE);
           
           if (time_after_eq(jiffies, sd->last_balance + interval)) {
               if (load_balance(cpu, rq, sd, idle, &continue_balancing)) {
                   // Moved tasks
                   idle = CPU_NOT_IDLE;
               }
               sd->last_balance = jiffies;
           }
       }
       rcu_read_unlock();
   }

CPU Affinity
============

Affinity Masks
--------------

.. code-block:: c

   // Set CPU affinity
   long sched_setaffinity(pid_t pid, const struct cpumask *in_mask) {
       struct task_struct *p;
       int retval;
       
       p = find_process_by_pid(pid);
       if (!p)
           return -ESRCH;
       
       retval = set_cpus_allowed_ptr(p, in_mask);
       put_task_struct(p);
       
       return retval;
   }
   
   // Migration
   int set_cpus_allowed_ptr(struct task_struct *p, const struct cpumask *new_mask) {
       struct rq *rq;
       unsigned long flags;
       int ret = 0;
       
       rq = task_rq_lock(p, &flags);
       
       if (cpumask_equal(&p->cpus_allowed, new_mask))
           goto out;
       
       if (!cpumask_intersects(new_mask, cpu_active_mask)) {
           ret = -EINVAL;
           goto out;
       }
       
       do_set_cpus_allowed(p, new_mask);
       
       if (task_running(rq, p) || p->state == TASK_WAKING) {
           // Migrate running task
           migration_cpu_stop(p);
       } else if (task_on_rq_queued(p)) {
           // Migrate queued task
           set_task_cpu(p, cpumask_any_and(cpu_active_mask, new_mask));
       }
       
   out:
       task_rq_unlock(rq, p, &flags);
       return ret;
   }

Best Practices
==============

1. **Understand scheduler classes** and when to use each
2. **Minimize latency** for real-time tasks
3. **Use CPU affinity** carefully (let scheduler balance)
4. **Avoid busy-waiting** (use sleep/wait mechanisms)
5. **Profile scheduler behavior** (/proc/schedstat, perf)
6. **Consider NUMA** topology for large systems
7. **Use cgroups** for resource management
8. **Test under load** (stress testing)
9. **Monitor context switches** (high count = performance issue)
10. **Balance priority** (don't abuse nice/RT priorities)

Common Pitfalls
===============

1. **Priority inversion** - low-priority holds lock needed by high-priority
2. **CPU starvation** - tasks not getting CPU time
3. **Excessive migrations** - tasks moving between CPUs
4. **Wrong scheduler class** - using RT when not needed
5. **Cache thrashing** - poor CPU affinity
6. **Load imbalance** - uneven distribution across CPUs

Quick Reference
===============

.. code-block:: c

   // Scheduling
   schedule();
   cond_resched();
   yield();
   
   // Sleep
   msleep(msecs);
   msleep_interruptible(msecs);
   schedule_timeout(timeout);
   schedule_timeout_interruptible(timeout);
   
   // Scheduler info
   sched_setscheduler(pid, policy, &param);
   sched_getscheduler(pid);
   sched_setaffinity(pid, mask);
   sched_getaffinity(pid, mask);

See Also
========

- Linux_Kernel_Architecture.rst
- Linux_Process_Management.rst
- Linux_Realtime_Scheduling.rst

References
==========

- kernel/sched/ in Linux source
- Documentation/scheduler/ in Linux source
- https://www.kernel.org/doc/html/latest/scheduler/
