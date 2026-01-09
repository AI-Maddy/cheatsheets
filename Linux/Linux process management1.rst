**cheatsheet** for **Linux process/thread management and scheduling** from a **kernel programming** perspective (based mainly on modern kernels ~6.1–6.12 era, early 2025+).

📌 1. Core Data Structures

⭐ | Structure              | Main Location              | Represents                          | Key Fields (most important for scheduling) |
|-----------------------|----------------------------|-------------------------------------|--------------------------------------------|
| ``struct task_struct``  | ``include/linux/sched.h``    | **One thread** (kernel uses “task”) | ``state``, ``exit_state``, ``pid``, ``tgid``, ``flags``, ``ptrace``, ``on_cpu``, ``cpu``, ``prio``, ``static_prio``, ``normal_prio``, ``rt_priority``, ``policy``, ``se`` (sched_entity), ``rt``, ``dl``, ``sched_class``, ``tasks``, ``ptrace_entry``, ``real_parent``, ``parent``, ``children``, ``sibling``, ``group_leader``, ``mm``, ``active_mm``, ``files``, ``cred``, ``fs``, ``files``, ``thread`` (arch-specific), ``fpu``, ``stack`` |
| ``struct sched_entity`` | ``kernel/sched/sched.h``     | Fair scheduling unit (CFS/EEVDF)    | ``load``, ``run_node`` (RB tree), ``group_node``, ``on_rq``, ``exec_start``, ``sum_exec_runtime``, ``vruntime``, ``prev_sum_exec_runtime``, ``nr_migrations``, ``avg`` (load tracking) |
| ``struct cfs_rq``       | ``kernel/sched/sched.h``     | Per-CPU run-queue for CFS tasks     | ``tasks``, ``balance_iterator``, ``min_vruntime``, ``tasks_timeline`` (**red-black tree**), ``nr_running``, ``load``, ``exec_clock``, ``tg`` pointer |
| ``struct rt_rq``        | ``kernel/sched/sched.h``     | Per-CPU run-queue for RT tasks      | Array of queues per priority [0..99]       |
| ``struct sched_class``  | ``kernel/sched/sched.h``     | Scheduling policy plugin            | ``next``, ``enqueue_task``, ``dequeue_task``, ``yield_task``, ``check_preempt_curr``, ``pick_task``, ``put_prev_task``, ``task_tick``, ``task_fork``, ``task_woken``, … |

🐧 2. Process vs Thread in Kernel

- Kernel does **not** distinguish process/thread — **everything is a task** (``task_struct``)
- **Thread group** = tasks that share the same ``tgid`` (thread-group ID = main thread's PID)
- ``getpid()`` → returns ``tgid``
- ``gettid()`` → returns ``pid``
- Main thread: ``task->group_leader == task``
- Kernel thread: ``task->mm == NULL``, ``task->flags & PF_KTHREAD``

Common flags (task_struct->flags):

| Flag               | Meaning                                      |
|--------------------|----------------------------------------------|
| ``PF_EXITING``       | Task is exiting                              |
| ``PF_EXITKILL``      | Killed by fatal signal                       |
| ``PF_KTHREAD``       | Kernel thread                                |
| ``PF_NO_SETAFFINITY``| Cannot change CPU affinity                   |
| ``PF_MEMPOLICY``     | Uses custom memory policy                    |
⭐ | ``PF_SCHED_JD``      | In deadline/jitter scheduling critical section (newer kernels) |

⚙️ 3. Scheduling Classes (priority order)

Highest → Lowest

⭐ | Class         | Policy values             | Module          | Key characteristics                          |
|---------------|---------------------------|-----------------|----------------------------------------------|
| ``stop_sched_class`` | —                       | —               | Migration / stop CPU (highest)               |
| ``dl_sched_class``   | ``SCHED_DEADLINE``        | ``sched/deadline.c`` | EDF + CBS ( Earliest Deadline First )      |
| ``rt_sched_class``   | ``SCHED_FIFO``, ``SCHED_RR``| ``sched/rt.c``    | Fixed priority 1–99                          |
| ``fair_sched_class`` | ``SCHED_NORMAL``, ``SCHED_BATCH``, ``SCHED_IDLE`` | ``sched/fair.c`` | **EEVDF** (since ~6.6) / was CFS             |
| ``idle_sched_class`` | —                       | —               | ``swapper`` / idle loop (lowest)               |

⭐ 📚 4. Important Scheduling Functions (kernel/sched/)

| Function                        | Purpose / When called                               | Common location          |
|---------------------------------|-----------------------------------------------------|--------------------------|
| ``schedule()``                    | Main entry point — pick & switch task               | ``kernel/sched/core.c``    |
| ``pick_next_task()``              | Iterates sched_classes → calls class->pick_task()   | ``core.c``                 |
| ``pick_task_fair()``              | Picks leftmost entity in RB-tree (EEVDF/CFS)        | ``fair.c``                 |
| ``enqueue_task_*()``              | Add task to run-queue                               | per-class                |
| ``dequeue_task_*()``              | Remove task from run-queue                          | per-class                |
| ``check_preempt_curr()``          | Wakeup path: maybe preempt current?                 | per-class                |
| ``try_to_wake_up()``              | Most common wakeup path                             | ``core.c``                 |
| ``ttwu_queue()`` / ``ttwu_do_activate()`` | Enqueue awakened task                        | ``core.c``                 |
| ``sched_tick()``                  | Timer tick → account time, check preemption         | ``core.c`` → class->task_tick() |
| ``update_curr()``                 | Update vruntime / exec time of current task         | ``fair.c``                 |
| ``yield_task()``                  | ``sched_yield()`` syscall                             | per-class                |
| ``set_task_cpu()``                | Change task → CPU affinity (migration)              | ``core.c``                 |

📖 5. vruntime & EEVDF / CFS Basics (very short version)

- ``vruntime`` ≈ virtual runtime accumulated (weighted by nice value)
- EEVDF (Earliest Eligible Virtual Deadline First) — default since kernel ~6.6
  - Leftmost task in red-black tree (``cfs_rq->tasks_timeline``) wins
⭐   - Key = ``vruntime`` (smaller = more eligible)
  - ``sched_slice()`` → ideal runtime per period (~4–20 ms)
  - ``calc_delta_fair()`` → weight-adjusted time
- Nice → weight mapping: ``-20`` = 88761, ``0`` = 1024, ``+19`` = 15

📚 6. Quick Reference: Common Kernel Operations

.. code-block:: c

// Current task
current                  // macro → current_thread_info()->task
current->pid
current->tgid
current->comm            // task name (16 chars)

// Iterate all processes
struct task_struct *p;
for_each_process(p) { ... }               // kernel/sched/signal.h

// Safe dereference (use RCU or rcu_read_lock())
rcu_read_lock();
p = pid_task(find_vpid(pid), PIDTYPE_PID);
rcu_read_unlock();

// Change scheduling class / parameters
sched_setscheduler(pid, policy, &param);  // from kernel
sched_setattr()                           // modern interface

// Kernel thread creation
kthread_run(my_func, data, "mykthread/%d", idx);

🐛 7. Quick Debugging Tips (ftrace / bpf)

.. code-block:: bash

================================================================================
🐛 Most useful tracepoints
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



trace-cmd record -e sched:sched_switch -e sched:sched_wakeup -e sched:sched_migrate_task
trace-cmd report

================================================================================
🐛 or ftrace directly
================================================================================

echo 'sched:*' > /sys/kernel/tracing/set_event
cat /sys/kernel/tracing/trace_pipe

================================================================================
EEVDF/CFS internals
================================================================================

perf sched record
perf sched latency

🟢 🟢 Good luck with your kernel module / scheduler tinkering!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
