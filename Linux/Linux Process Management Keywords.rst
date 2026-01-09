
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **keywords and concepts** specifically relevant to **process/task management** when doing **embedded Linux kernel programming** (e.g. on resource-constrained systems like ARM Cortex-A/M/R, RISC-V, MIPS, small SoCs, real-time patches, custom board support, minimal configurations).

⭐ Each keyword includes a short one-line description from an embedded kernel developer's perspective.

1. **task_struct**  
   Core per-thread/process structure — keep it lean in embedded by disabling unneeded features.

2. **sched_entity**  
⭐    EEVDF/CFS scheduling unit; critical for understanding fair scheduling on low-power CPUs.

3. **rt_task / rt_priority**  
⭐    Real-time (SCHED_FIFO/SCHED_RR) tasks — heavily used in embedded for latency-critical threads.

4. **SCHED_DEADLINE**  
⭐    EDF scheduling class — increasingly important for hard real-time on embedded multicore.

5. **PREEMPT_RT**  
   Real-time patch — turns Linux into soft/hard RT; changes many process management primitives.

6. **CONFIG_PREEMPT** / **CONFIG_PREEMPT_VOLUNTARY**  
   Kernel preemption model — choose carefully for latency vs. throughput on embedded.

7. **TIF_NEED_RESCHED**  
   Thread info flag that triggers rescheduling — often polled in embedded fast paths.

8. **need_resched()**  
   Fast check if the current task should yield — heavily used in tight embedded loops.

9. **schedule()**  
   Main scheduler entry point — understand its call sites in interrupt/ softirq/ syscall paths.

10. **try_to_wake_up() / wake_up_process()**  
   Most common wakeup paths — latency killers if misused on embedded systems.

11. **sched_yield()**  
   Voluntary yield — often 🔴 🔴 avoided in RT/embedded code due to poor determinism.

12. **kthread_run / kthread_create**  
   Preferred way to create kernel threads in embedded drivers/modules.

13. **PF_KTHREAD**  
   Flag identifying kernel threads — many embedded drivers run work in kthreads.

14. **current**  
   Macro for the currently executing task — 🔴 🔴 avoid overuse in hot paths (cache miss risk).

15. **for_each_process()**  
   Global task list traversal — very slow on systems with many tasks; 🔴 🔴 avoid in embedded.

16. **signal_pending() / signal_pending_state()**  
   Fast check for pending signals — crucial in interruptible sleeps on embedded.

17. **wait_event_interruptible() / wait_event()**  
   Common wait macros — prefer interruptible variants in embedded to handle signals.

18. **completion**  
   Lightweight synchronization primitive — widely used instead of semaphores in drivers.

19. **wait_queue_head_t / wake_up()**  
   Wait queue mechanism — backbone of most blocking in embedded drivers.

20. **TASK_INTERRUPTIBLE / TASK_UNINTERRUPTIBLE**  
   Sleep states — choose UNINTERRUPTIBLE carefully (can hang system on embedded).

21. **set_current_state()**  
   Sets task state before schedule() — must be paired correctly to 🔴 🔴 avoid races.

22. **sched_setscheduler() / sched_setattr()**  
   Change scheduling policy/priority from kernel — used for RT threads in drivers.

23. **nice / static_prio / normal_prio**  
   Priority levels — embedded often runs everything at default nice 0 or RT.

24. **rt_mutex**  
⭐    Priority-inheritance aware mutex — essential when using PREEMPT_RT.

25. **raw_spinlock_t**  
   Lowest-level lock (no preemption disabling in !RT) — used heavily in RT kernels.

26. **local_bh_disable() / local_irq_disable()**  
   Old-style preemption/IRQ disabling — still used in some embedded drivers.

27. **migrate_disable() / migrate_enable()**  
   Modern way to pin task to CPU (replaces get_cpu/put_cpu in many cases).

28. **cpumask_t / cpumask_var_t**  
⭐    CPU affinity masks — critical for pinning tasks on heterogeneous embedded SoCs.

29. **sched_setaffinity()**  
⭐    Set CPU affinity — used to bind latency-critical threads to specific cores.

30. **idle task / swapper**  
   Per-CPU idle loop — often customized in embedded for power management (cpuidle).

31. **stop_machine**  
   All-CPU stopper mechanism — used sparingly in embedded (long latency).

32. **per_cpu() / this_cpu_ptr()**  
   Per-CPU variables — heavily used for lockless counters/queues in embedded.

33. **rcu_read_lock() / rcu_dereference()**  
   Read-copy-update — preferred concurrency in modern embedded kernels.

34. **workqueue / delayed_work / system_wq**  
   Deferred work execution — default choice over kernel threads in many drivers.

35. **tasklet** (legacy)  
   Softirq-like bottom half — still seen in old embedded drivers, but workqueues preferred.

36. **high-priority workqueue (WQ_HIGHPRI)**  
⭐    Used for time-critical deferred work in embedded systems.

37. **CONFIG_NO_HZ_IDLE / CONFIG_NO_HZ_FULL**  
⭐    Tickless idle — important for power savings and latency on battery-powered embedded.

38. **CONFIG_HZ**  
   Timer tick frequency — often lowered (100/250) in embedded to reduce overhead.

39. **CONFIG_RCU_NOCB_CPU**  
   Offload RCU callbacks to no-CB kthreads — helps latency on RT embedded kernels.

40. **CONFIG_SCHED_AUTOGROUP**  
   Usually disabled in embedded — interferes with RT predictability.

⭐ These keywords cover the majority of what you will encounter when writing, debugging or optimizing **process/task management code** in embedded Linux kernels (drivers, custom schedulers, real-time extensions, power management hooks, etc.). Focus especially on RT-related terms if targeting deterministic latency.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
