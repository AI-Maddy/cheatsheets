
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



🐧 Linux Kernel Process/Task Management Cheatsheet (Kernel ~6.x Perspective)

⭐ This cheatsheet covers **task management infrastructure**, **key syscalls internals** (fork/clone/exec/exit), and **scheduling code** details. Kernel views everything as a **task** (``task_struct``); processes/threads are user-space distinctions. Focus on x86_64/ARM64 common paths. Source paths: ``kernel/fork.c``, ``kernel/exit.c``, ``kernel/sched/core.c``, etc.

#### 1. Task Management Infrastructure

- **Core Data Structures** (expanded from prev):
⭐   | Structure            | Header/File                  | Purpose/Key Role                                                                 |
  |----------------------|------------------------------|----------------------------------------------------------------------------------|
  | ``struct task_struct`` | ``include/linux/sched.h``      | Represents a task (process/thread). ~1-2KB, allocated via slab.                  |
  | ``struct thread_struct``| Arch-specific (e.g., ``arch/x86/include/asm/processor.h``) | CPU registers/state (e.g., sp, pc, fpu).                                         |
  | ``struct thread_info`` | Arch-specific (e.g., ``arch/x86/include/asm/thread_info.h``) | Low-level flags (e.g., TIF_NEED_RESCHED). Often embedded in stack.                |
  | ``struct mm_struct``   | ``include/linux/mm_types.h``   | Memory management (VMAs, page tables). Shared among threads.                     |
  | ``struct signal_struct``| ``include/linux/signal.h``    | Pending signals, handlers. Shared in thread group.                               |
  | ``struct rq``          | ``kernel/sched/sched.h``       | Per-CPU runqueue. Holds cfs_rq, rt_rq, dl_rq, etc.                               |

⭐ - **Key Lists/Queues**:
  - Global task list: ``init_task.tasks`` (doubly-linked via ``task_struct->tasks``).
  - Per-CPU runqueues: ``per_cpu(runqueues, cpu)`` → ``struct rq *rq = this_rq();``.
  - Thread group: ``task->thread_group`` (circular list).
  - Children/siblings: ``task->children``, ``task->sibling`` (linked via ``list_head``).
  - PID hash: ``pid_hash`` table for fast lookup (``find_task_by_vpid()``).

- **Task States** (``task_struct->state``):
  | State                | Value    | Meaning                                      |
  |----------------------|----------|----------------------------------------------|
  | ``TASK_RUNNING``       | 0        | Runnable or running.                         |
  | ``TASK_INTERRUPTIBLE`` | 1        | Sleeping, wakeable by signals.               |
  | ``TASK_UNINTERRUPTIBLE``| 2       | Deep sleep, ignores signals.                 |
  | ``__TASK_STOPPED``     | 4        | Stopped (e.g., ptrace).                      |
  | ``__TASK_TRACED``      | 8        | Being traced.                                |
  | ``EXIT_ZOMBIE``        | 16 (exit_state) | Exited, waiting for parent reap.        |
  | ``EXIT_DEAD``          | 32 (exit_state) | Reaped, final cleanup.                  |

- **Access Macros**:
  - ``current``: Gets current task (per-CPU var or thread_info).
  - ``for_each_process(tsk)``: Iterate all tasks.
  - ``for_each_thread(p, t)``: Iterate threads in group.
  - ``task_rq_lock(tsk)``: Lock task's runqueue.

#### 2. Process Creation: fork/vfork/clone Internals

- **Syscalls Entry**:
  - User: ``fork()`` → syscall → ``sys_clone`` (unified; flags distinguish fork/vfork/clone).
  - Flags: ``CLONE_VM`` (share mm), ``CLONE_VFORK`` (parent waits), ``CLONE_THREAD`` (share tgid/signals).

- **Core Flow** (``kernel/fork.c``):
  1. ``copy_process()``: Main worker. Allocates new ``task_struct`` via ``dup_task_struct(current)``.
     - Copies most fields from parent (shallow copy).
     - Handles COW: ``dup_mm()`` → if !CLONE_VM, full copy; else share ``mm_struct``.
     - Copies: files (``dup_fd()``), signals (``copy_signal()``), creds (``copy_creds()``), etc.
     - Arch-specific: ``copy_thread()`` (setup stack, regs; child returns 0).
     - Sets PID: ``alloc_pid()``.
     - If thread: Join thread group, share signal_struct.
  2. ``wake_up_new_task(child)``: Enqueue on parent's CPU rq (or balance).
  3. vfork: Parent sleeps via ``completion`` until child calls ``exec`` or ``exit``.
  4. Return: Parent gets child's PID; child gets 0.

⭐ - **Key Functions**:
  | Function              | Role                                         |
  |-----------------------|----------------------------------------------|
  | ``dup_task_struct()``   | Slab alloc + memcpy parent task_struct.      |
  | ``copy_files()``        | Dup file table (or share if CLONE_FILES).    |
  | ``copy_mm()``           | Dup or share VM (COW pages).                 |
  | ``sched_fork()``        | Init sched params (prio, vruntime inherit).  |
  | ``wake_up_new_task()``  | Enqueue + possible preempt.                  |

- **Kernel Thread Creation** (not syscall):
  - ``kthread_create()`` → ``copy_process(PF_KTHREAD)`` with ``mm=NULL``.
  - ``kthread_run(fn, data, name)``: Create + wake.

#### 3. Exec: do_execve Internals

- **Syscall**: ``execve(path, argv, envp)`` → ``sys_execve`` → ``do_execve()``.
- **Core Flow** (``fs/exec.c``):
  1. ``bprm_init()``: Setup ``binprm`` (binary parameter struct).
  2. ``search_binary_handler()``: Find loader (ELF, script, etc.) via ``binfmt`` list.
     - ELF: ``load_elf_binary()`` → parse headers, setup new mm.
  3. ``exec_binprm()``: Load binary into memory.
  4. Replace old mm: ``exec_mmap(new_mm)`` → release old mm, switch to new.
  5. Setup stack: argv/envp pushed; set regs (e.g., rip to entry point).
  6. Signals/files/creds updated (e.g., close-on-exec).
  7. vfork complete: Wake parent if CLONE_VFORK.

⭐ - **Key Changes**:
  - New ``mm_struct``; old VM discarded (no COW).
  - PID/tgid unchanged; comm updated to binary name.
  - Threads: Only calling thread survives; others zombied? No—exec affects whole process (kills other threads implicitly via mm change).

- **Functions**:
  | Function                 | Role                                         |
  |--------------------------|----------------------------------------------|
  | ``do_execveat_common()``   | Common path (handles fd/path).               |
  | ``bprm_execve()``          | Core exec logic.                             |
  | ``start_thread(regs, pc, sp)`` | Arch: Set entry point.                    |

#### 4. Exit: do_exit/wait Internals

- **Syscall**: ``exit(code)`` → ``sys_exit`` → ``do_exit(code)``.
- **Core Flow** (``kernel/exit.c``):
  1. ``exit_signals()``: Set PF_EXITING, deliver signals.
  2. ``exit_mm()``: Release mm (if last thread).
  3. Close resources: files, fs, semaphores.
  4. ``exit_notify()``: Zombie state, notify parent (SIGCHLD).
     - Reparent orphans to init/subreaper.
  5. ``schedule()``: Never returns; task dequeued.
  6. Final: ``release_task()`` by reaper (frees task_struct).

- **Wait** (``sys_wait4``):
  - ``do_wait()``: Sleep until child exits (wait_queue).
  - Reap zombie: Copy exit info, ``release_task()``.

- **Group Exit**: ``do_group_exit()`` for threads.
- **Functions**:
  | Function              | Role                                         |
  |-----------------------|----------------------------------------------|
  | ``do_exit()``           | Main exit path.                              |
  | ``exit_thread()``       | Arch-specific cleanup.                       |
  | ``__exit_files()``      | Close files.                                 |
  | ``release_task()``      | Free resources post-reap.                    |

#### 5. Scheduling Code Internals

- **Main Entry**: ``schedule()`` (``kernel/sched/core.c``).
  - Called when: Tick, wakeup, block, yield, preempt.
- **Core Flow**:
  1. ``put_prev_task(rq, prev)``: Account time for current.
  2. ``pick_next_task(rq, prev)``: Loop sched_classes high-to-low.
     - If RT/DL: Pick highest prio.
     - Fair: ``pick_next_entity(cfs_rq)`` → leftmost in RB-tree (min vruntime).
     - Idle: ``idle_sched_class`` if nothing else.
  3. If same task: Return.
  4. ``context_switch(rq, prev, next)``:
     - ``prepare_task_switch()``: Hooks (e.g., perf).
     - ``finish_task_switch()``: Arch ``switch_to(prev, next)`` (save/restore regs, mm_cr3 if needed).
     - Lazy MM: If same mm, skip full switch (threads).

- **Preemption**:
  - Need resched: Set ``TIF_NEED_RESCHED`` (e.g., via ``preempt_schedule_irq()``).
  - User preemption: Ret to user checks flag → ``schedule()``.
  - Kernel preemption: If ``PREEMPT=y``, voluntary points.

- **Tick Handling**: ``scheduler_tick()`` → ``task_tick_fair()`` → ``update_curr()``, check resched.
- **Load Balancing**: ``run_rebalance_domains()`` (softirq) → ``rebalance_domains()``.
⭐ - **Key Sched Functions** (expanded):
  | Function                   | Role / Details                               |
  |----------------------------|----------------------------------------------|
  | ``__schedule()``             | Core schedule (with rq lock).                |
  | ``context_switch()``         | Switch tasks (mm_switch if diff mm).         |
  | ``update_rq_clock()``        | Sync rq clock.                               |
  | ``resched_curr()``           | Set need_resched on current.                 |
  | ``idle_task()``              | Per-CPU idle task (swapper/0).               |

- **EEVDF Notes**: ``entity_eligible(se)`` → vruntime < deadline; slice based on lag.

For code diving: Use ``cscope`` or ``git grep`` in kernel tree. Debug with ``ftrace`` (e.g., ``trace-cmd record -e sched:*``).

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
