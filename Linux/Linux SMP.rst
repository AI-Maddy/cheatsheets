**SMP (Symmetric Multi-Processing)** aspects in the Linux kernel, with special emphasis on how **processes/tasks**, **interrupts**, and **caches** interact in a multi-core / multi-socket environment (modern kernels ~6.1–6.12 era, 2025–2026 perspective).

⭐ 🎓 SMP – Process / Task Management Keywords & Concepts

⭐ | Concept / Keyword              | One-line SMP-relevant description                                                                 | Typical SMP impact / gotcha |
|-------------------------------|---------------------------------------------------------------------------------------------------|------------------------------|
| ``this_cpu_ptr()`` / ``per_cpu()`` | Access per-CPU variable safely — almost always the right choice in SMP code                       | 🔴 🔴 Avoid global variables for counters/queues |
| ``smp_processor_id()``           | Returns logical CPU id of current processor                                                       | Very fast, but disable preemption when storing result |
| ``get_cpu()`` / ``put_cpu()``      | Disable preemption + return current cpu; old style (mostly replaced by migrate_disable)           | Still seen in drivers; use migrate_* in new code |
⭐ | ``migrate_disable()`` / ``migrate_enable()`` | Prevent task migration during critical section (replaces get_cpu/put_cpu in many cases) | Essential for per-CPU data access without locks |
⭐ | ``cpumask_t`` / ``cpumask_var_t``  | CPU affinity mask — controls on which CPUs a task may run                                         | Used for pinning latency-critical threads |
| ``sched_setaffinity()``          | Kernel function to set task → CPU affinity                                                        | Common in embedded/SMP drivers for core isolation |
| ``sched_domain``                 | Hierarchy of scheduling domains (MC → DIE → NODE → SYSTEM)                                       | Defines load-balancing scope |
| ``sd_llc`` / ``sd_numa``           | LLC (last-level cache) and NUMA domains — influence task placement                                | Task prefers same LLC / NUMA node |
| ``idle_balance``                 | When idle CPU pulls tasks from busy siblings                                                      | Can cause cache line bouncing if over-aggressive |
| ``nohz_full`` / ``rcu_nocb``       | Full nohz + RCU offloading — used for low-jitter isolated cores                                   | Popular in HPC, networking, audio, trading |

⭐ 🎓 SMP – Interrupt Handling Keywords & Concepts

⭐ | Concept / Keyword              | SMP-relevant description                                                                          | Typical SMP impact / gotcha |
|-------------------------------|---------------------------------------------------------------------------------------------------|------------------------------|
| ``irq_desc``                     | Descriptor for each interrupt line — contains action list and affinity                            | Per-IRQ affinity mask |
| ``irq_set_affinity_hint()``      | Driver suggests preferred CPU(s) for IRQ                                                          | Hint only — kernel may ignore |
| ``irq_set_affinity_and_hint()``  | Stronger affinity request (newer kernels)                                                         | Preferred in modern drivers |
| ``IRQF_NO_THREAD``               | Interrupt runs in hardirq context (no thread)                                                     | Low latency, but must be short |
| ``IRQF_ONESHOT``                 | Threaded IRQ — primary handler + threaded bottom half                                            | Thread can sleep, better for complex work |
| ``irqbalance`` daemon            | Userspace daemon that redistributes IRQs across CPUs                                              | Usually disabled in low-latency setups |
| ``smp_affinity`` / ``/proc/irq/*/smp_affinity`` | Bitmask of CPUs allowed to handle this IRQ                                      | Tune for cache locality / balance |
| ``Affinity mask`` (hex)          | Example: ``1`` = CPU0 only, ``f`` = first 4 CPUs, ``ffffffff`` = all 32 CPUs                           | Write to ``/proc/irq/N/smp_affinity`` |
| ``percpu_irq`` / ``irq_percpu()``  | Interrupt delivered only to one specific CPU (e.g. timer, local APIC)                             | No cross-CPU IPI overhead |
| ``IPI`` (Inter-Processor Interrupt) | Mechanism to send interrupt from one CPU to another (resched, call function, etc.)          | Expensive — minimize in hot paths |
| ``call_function_single`` / ``smp_call_function_single()`` | Execute function on specific remote CPU (synchronous or async) | Used for TLB shootdown, cache flush, etc. |

⭐ 🎓 SMP – Cache & Memory Keywords & Concepts

⭐ | Concept / Keyword              | SMP-relevant description                                                                          | Typical SMP impact / gotcha |
|-------------------------------|---------------------------------------------------------------------------------------------------|------------------------------|
| ``cacheline_aligned`` / ``__cacheline_aligned__`` | Align variable/structure to cache line size (usually 64 bytes)                             | Prevents false sharing |
| ``____cacheline_internodealigned__`` | Align to node boundary (NUMA systems, larger than cache line)                                | Rare — used in some sched structures |
| ``smp_mb()`` / ``smp_wmb()`` / ``smp_rmb()`` | Full / write / read memory barriers with SMP ordering semantics                             | Required for lockless algorithms |
| ``smp_store_mb()``               | Store + full memory barrier                                                                       | Common pattern: write → barrier → read |
| ``ACCESS_ONCE()`` / ``{READ,WRITE}_ONCE()`` | Prevent compiler from reordering / tearing single-word accesses                             | Use for lockless single-variable access |
| ``cmpxchg()`` / ``xchg()``         | Compare-and-swap / exchange — building block of atomic ops                                        | Heavily used in per-CPU counters |
| ``this_cpu_add()`` / ``this_cpu_inc()`` | Lockless per-CPU atomic increment/add (no cross-core traffic)                               | Extremely fast for per-CPU stats |
| ``per_cpu_sum()`` / ``per_cpu_ptr()`` aggregation | Collect/sum values across all CPUs                                                               | Common pattern in /proc stats |
| ``false sharing``                | Multiple CPUs writing different variables in same cache line → ping-pong                      | Classic SMP performance killer |
| ``cache invalidation`` / ``clflush`` / ``clwb`` | Explicit cache line flush / write-back (used in drivers, DMA coherency)                     | Expensive — 🔴 🔴 avoid in hot paths |
| ``coherent DMA`` vs ``streaming DMA`` | Coherent = CPU/device see same view without flush; streaming = explicit dma_sync_*         | Streaming usually much faster on SMP |
| ``MESI / MOESI`` protocol        | Cache coherence protocol (Modified, Exclusive, Shared, Invalid)                                  | Understanding helps debug bouncing |

🐛 Quick SMP Tuning & Debugging Patterns (2025–2026)

.. code-block:: bash

================================================================================
Pin IRQ 44 to cores 4-7
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



echo 000000f0 > /proc/irq/44/smp_affinity

================================================================================
See which CPU handles IRQ
================================================================================

cat /proc/interrupts | grep eth0

================================================================================
Isolate CPUs (nohz_full + rcu_nocb)
================================================================================

isolcpus=4-7 nohz_full=4-7 rcu_nocb=4-7

================================================================================
Watch cache misses & false sharing
================================================================================

perf stat -e cache-misses,cache-references ./myapp
perf record -e mem_load_uops_retired.l3_miss,cpu_clk_unhalted.thread ./myapp

================================================================================
Per-CPU stats (very useful)
================================================================================

mpstat -P ALL 1
pidstat -w -I 1   # context switches + migrations

⚡ Most Common SMP-related Performance Killers (embedded & server)

1. False sharing on global counters/flags
2. Excessive IPIs (from too fine-grained load balancing or too many timers)
3. Over-using coherent DMA mappings for high-bandwidth data
⭐ 4. Running latency-critical threads on busy/shared cores
5. Not using per-CPU data structures when possible
6. Too aggressive irqbalance on real-time/low-jitter workloads

Use this cheatsheet when writing drivers, optimizing scheduler behavior, debugging cache-line contention, or tuning interrupt affinity on multi-core ARM/x86/RISC-V SoCs.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
