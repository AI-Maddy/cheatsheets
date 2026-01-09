**Linux Process / Thread / Scheduling Cheatsheet** (updated for modern kernels ~2025–2026, mainly focusing on **CFS**, real-time policies, and practical commands).

⭐ 🎓 1. Key Concepts — Process vs Thread in Linux

| Concept              | Process                                      | Thread (in a process)                              | Kernel Representation       |
|----------------------|----------------------------------------------|-----------------------------------------------------|-----------------------------|
| PID                  | Unique                                       | Shares PID with other threads (thread group leader) | task_struct                 |
| Creation             | ``fork()`` / ``vfork()`` / ``posix_spawn()``       | ``pthread_create()`` → ``clone(CLONE_THREAD …)``        | All are tasks               |
| Virtual memory       | Separate                                     | Shared                                              | —                           |
| File descriptors     | Shared (after fork dup)                      | Shared                                              | —                           |
| Scheduler entity     | Scheduled independently                      | Scheduled independently                             | Each thread = separate task |
| Nice value           | Per-thread since kernel ~2.6.23 (NPTL)       | Per-thread (not shared!)                            | —                           |
| Real-time policy     | Per-thread                                   | Per-thread                                          | —                           |

⭐ **Important**: Linux scheduler works on **tasks** — both single-threaded processes and individual threads are scheduled the same way.

📌 2. Process / Thread States (as seen in ``ps``, ``/proc/pid/stat``)

| State | Letter (ps) | Meaning                                 | Runnable? |
|-------|-------------|-----------------------------------------|-----------|
| R     | R           | Running or runnable (on run-queue)      | Yes       |
| S     | S           | Interruptible sleep (wait, sleep, poll) | No        |
| D     | D           | Uninterruptible sleep (usually I/O)     | No        |
| T     | T           | Stopped (SIGSTOP / ptrace)              | No        |
| t     | t           | Tracing stop                            | No        |
| Z     | Z           | Zombie (terminated, waiting for wait()) | No        |
| X     | X           | Dead (should never be visible)          | —         |

📌 3. Scheduling Policies (sched(7))

| Policy          | Class          | Priority range | Time-sharing? | Preemption          | Typical use case                     | Command to set               |
|-----------------|----------------|----------------|---------------|----------------------|--------------------------------------|------------------------------|
| **SCHED_OTHER** | CFS (default)  | 0 (static)     | Yes           | Preemptive           | Normal user processes                | ``nice``, ``renice``             |
| **SCHED_BATCH** | Batch          | 0              | Yes (less preemption) | Less aggressive      | Batch / HPC jobs                     | ``chrt -b``                    |
| **SCHED_IDLE**  | Idle           | 0              | Very low prio  | Only when nothing else | Extremely low priority tasks         | ``chrt -i``                    |
| **SCHED_FIFO**  | Realtime       | 1–99           | No            | Preemptive, no slice | Low-latency audio, control systems   | ``chrt -f``                    |
| **SCHED_RR**    | Realtime       | 1–99           | Round-robin    | Time-sliced per prio | Soft real-time                       | ``chrt -r``                    |
| **SCHED_DEADLINE** | EDF / CBS   | Runtime/Deadline/Period | No      | Earliest deadline first | Hard real-time (since ~3.14)         | ``chrt --sched-deadline``      |

**Quick rules**:
- Realtime policies (FIFO/RR) **always** beat CFS/Batch/Idle
- Within same realtime priority → FIFO = FCFS, RR = round-robin
- CFS tries to be **fair** (vruntime-based)

📚 4. Most Useful Commands — Quick Reference

| Goal                                      | Command Example                                      | Notes / Requirements                     |
|-------------------------------------------|------------------------------------------------------|------------------------------------------|
| List all processes + threads              | ``ps -eLf``  or  ``top -H``                              | ``-H`` = thread view in top/htop           |
| Show threads of PID 1234                  | ``ps -T -p 1234``  or  ``ps -eLo pid,tid,psr,comm``      | TID = thread ID                          |
| Show scheduling policy + priority         | ``chrt -p 1234``                                       | Works on process or thread TID           |
| Set FIFO priority 50 (all threads)        | ``chrt -f -a 50 1234``                                 | Needs ``CAP_SYS_NICE`` or root             |
| Set RR priority 30 & launch               | ``chrt -r 30 ./myapp``                                 | —                                        |
| Make process nice +10 (lower priority)    | ``renice +10 -p 1234``  or  ``nice -n 10 ./myapp``       | No root needed for + nice                |
| Make very high priority (CFS)             | ``renice -20 -p 1234``                                 | Needs root / CAP_SYS_NICE                |
| Change policy & priority (running proc)   | ``chrt -r --pid 40 5678``                              | —                                        |
| Show max realtime priority                | ``chrt -m``                                            | Usually 99                               |
| Pin process to cores 0,3,4                | ``taskset -cp 0,3-4 1234``                             | Or ``taskset -c 0,3-4 ./myapp``            |
| Show CPU affinity                         | ``taskset -cp 1234``                                   | —                                        |
| See nice & dynamic priority               | ``ps -o pid,comm,pri,ni,rtprio,policy``                | ``pri`` = dynamic, ``rtprio`` = realtime prio|
| Change all threads of a process nice      | ``ps -T -o tid= -p 1234 \| xargs -I{} renice 15 {}``   | Because nice is per-thread               |

📌 5. Quick One-liners (copy-paste friendly)

.. code-block:: bash

================================================================================
Monitor threads sorted by CPU
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



top -H

================================================================================
⚙️ Give PID 4242 very low priority (CFS)
================================================================================

renice +19 -p 4242

================================================================================
🚗 Give realtime FIFO priority 70 to existing daemon (careful!)
================================================================================

sudo chrt -f -a 70 4242

================================================================================
⚙️ Launch ffmpeg with RR priority 50 on cores 2-5 only
================================================================================

taskset -c 2-5 chrt -r 50 ffmpeg -i input.mp4 output.mp4

================================================================================
Show realtime attributes of all chromium threads
================================================================================

ps -eLo pid,tid,psr,rtprio,policy,comm | grep -i chrome

================================================================================
Reset to normal scheduling
================================================================================

sudo chrt -o -p 0 12345

📌 6. Quick Rules of Thumb (2025–2026)

- Want better **responsiveness** for desktop/game/audio → use ``SCHED_RR`` 20–50
- Want lower **background** impact → ``nice +15`` … ``+19`` or ``SCHED_IDLE``
- Need **hard guarantees** → ``SCHED_DEADLINE`` (runtime ≤ deadline ≤ period)
- Never set realtime priority **99** unless you know what you're doing (watchdog, migration threads live there)
- ``nice``/``renice`` **only** meaningfully affect ``SCHED_OTHER``/``SCHED_BATCH``/``SCHED_IDLE``

🟢 🟢 Good luck tuning!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
