================================================================================
Linux Kernel Debug, Trace, Profile Tools & Methodologies (Early 2026)
================================================================================

**Comprehensive cheatsheet for kernel debugging, tracing, and profiling tools**

*as of early 2026, kernel ~6.12+ era – focusing on relevant & actively used technologies*

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

Debugging Fundamentals
================================================================================

Three Core Activities
~~~~~~~~~~~~~~~~~~~~~

🎯 **Profiling** 
   Measuring resource usage (CPU, memory, I/O) to find bottlenecks

📊 **Tracing** 
   Recording all events/calls to understand behavior sequence

🔍 **Debugging** 
   Stepping through code, inspecting state at runtime

Performance Analysis Checklist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✓ Is the system responsive? (latency vs throughput trade-off)
✓ Which process/thread is slow? (userspace or kernel?)
✓ What resource is bottleneck? (CPU, memory, disk I/O, network)
✓ How much overhead do tools add? (measurement bias)
✓ Can I reproduce the issue? (race conditions are hard)

Sampling vs Instrumentation Trade-off
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------+----------+-------------------+----------------------------------+
| **Approach**             | Overhead | Accuracy          | Best For                         |
+==========================+==========+===================+==================================+
| Sampling                 | 🟢 Low   | Good (statistical)| CPU profiles, sustained issues   |
| (Periodic snapshots)     |          |                   |                                  |
+--------------------------+----------+-------------------+----------------------------------+
| Instrumentation          | 🔴 High  | Exact             | Rare/specific events, counting   |
| (Every event)            |          |                   |                                  |
+--------------------------+----------+-------------------+----------------------------------+
| Hybrid                   | 🟡 Med   | Very good         | bpftrace, perf with filters      |
| (Smart sampling + instr.)| – Medium |                   |                                  |
+--------------------------+----------+-------------------+----------------------------------+

Essential Tools Reference
================================================================================

⭐ ftrace (Built-in Kernel Tracer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Location:** ``/sys/kernel/tracing/`` (or ``/sys/kernel/debug/tracing/`` on older kernels)

**Key Features:**

✅ Function-level tracing with ``function`` tracer
✅ Call graph visualization with ``function_graph`` tracer  
✅ Tracepoints (stable ABI)
✅ Low overhead when inactive
✅ Ring buffer (circular, never fills)

**Essential Commands:**

.. code-block:: bash

   # List available tracers
   cat /sys/kernel/tracing/available_tracers

   # Enable function tracer
   echo function > /sys/kernel/tracing/current_tracer

   # Function graph tracer (shows call tree with timings)
   echo function_graph > /sys/kernel/tracing/current_tracer

   # View current trace
   cat /sys/kernel/tracing/trace

   # Disable tracer
   echo nop > /sys/kernel/tracing/current_tracer

**Powerful Filtering:**

.. code-block:: bash

   # Trace specific functions (glob patterns OK)
   echo 'vfs*' > /sys/kernel/tracing/set_ftrace_filter

   # Exclude functions
   echo '!vfs_read' > /sys/kernel/tracing/set_ftrace_notrace

   # Trace specific PID
   echo 'p:my_event do_syscall_trace_enter' > /sys/kernel/tracing/kprobe_events
   echo 'filter: common_pid == 1234' > /sys/kernel/tracing/events/tracepoints/my_event/filter


⭐⭐ perf (Performance Events – Best General-Purpose)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What:** Userspace tool + kernel subsystem (``perf_events``) for profiling

**Install:** Usually pre-installed or ``apt install linux-tools``

**Key Strengths:**

✨ CPU profiling & flame graphs
✨ Hardware Performance Counters (PMU)
✨ Syscall tracing
✨ Lock contention analysis
✨ Memory profiling
✨ Always available (no special packages)

**Most Used Commands:**

.. code-block:: bash

   # Record CPU profile (99 Hz sampling, with call stacks)
   perf record -F 99 -g -- sleep 30

   # View profile interactively
   perf report

   # Live profiling (like top)
   perf top -F 99 -g

   # System-wide profiling (all processes)
   perf record -a -F 99 sleep 30

   # Hardware counters (cycles, instructions, cache-misses)
   perf stat -ddd ./myapp

   # Specific event profiling
   perf record -e cache-misses -g -- sleep 10

   # Trace syscalls
   perf trace -e open,read,write -- ./myapp

   # Measure context switches
   perf stat -e context-switches ./myapp

   # Lock contention analysis
   perf lock record -- ./myapp
   perf lock report


⭐⭐⭐ bpftrace (eBPF One-Liners – Best for Quick Custom Queries)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What:** Modern ad-hoc kernel tracing without C code (DTrace-like syntax)

**Install:** ``apt install bpftrace`` (requires kernel 4.18+, LLVM)

**Key Strengths:**

⚡ **Fastest way to prototype custom queries**
⚡ Concise awk/DTrace-like syntax
⚡ Runs directly in kernel (extremely low overhead)
⚡ Built-in histograms, aggregations, maps
⚡ One-liner style (Ctrl+C to stop)

**Quick Reference Examples:**

.. code-block:: bash

   # System call count by process
   bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

   # Block I/O latency histogram (in microseconds)
   bpftrace -e 'tracepoint:block:block_rq_issue { @start[tid] = nsecs; }
                tracepoint:block:block_rq_complete /@start[tid]/ { 
                  @usecs = hist((nsecs - @start[tid]) / 1000); 
                  delete(@start[tid]); 
                }'

   # CPU profile (kernel stacks)
   bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'

   # Trace open() syscalls with file paths
   bpftrace -e 'tracepoint:syscalls:sys_enter_open* { printf("%s(%s)\n", comm, str(args[0])); }'

   # Find slow malloc() calls
   bpftrace -e 'uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc { @time[tid] = nsecs; }
                uretprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc /@time[tid]/ {
                  @lat = hist(nsecs - @time[tid]);
                  delete(@time[tid]);
                }'

   # Count page faults by process
   bpftrace -e 'software:page-faults { @[comm] = count(); }'


🟢 bcc (BPF Compiler Collection – Reusable Tools)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What:** Python + C framework for building eBPF tools and production agents

**Install:** ``apt install bpfcc-tools``

**Pre-built Tools Available:**

=========  ============================================================
Tool       What It Does
=========  ============================================================
biolatency I/O latency distribution (histograms)
offcputime Why threads not running (off-CPU flame graphs)
profile    CPU hot spots (flame graphs)
memleak    Memory allocation leak detection
vfscount   File system read/write frequency
runqlat    Scheduler runqueue latency distribution
tcpconnect TCP connection tracking
tcpdrop    Network packet loss tracking
=========  ============================================================

**Quick Usage:**

.. code-block:: bash

   # Block device I/O latency analysis
   biolatency

   # Off-CPU time flame graph (why not running)
   offcputime -f -p `pgrep myprocess` 10 > offcpu.stacks
   cat offcpu.stacks | flamegraph.pl > offcpu.svg

   # Memory leak detection
   memleak -p `pgrep myprocess`

   # Runqueue latency (scheduler delays)
   runqlat


🔵 trace-cmd & KernelShark (ftrace GUI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What:** Graphical frontend to ftrace (excellent for exploration)

**Install:** ``apt install trace-cmd kernelshark``

**Usage:**

.. code-block:: bash

   # Record trace with multiple events
   trace-cmd record -e sched:sched_switch -e block:* -e irq:* -- sleep 10

   # Generate HTML report
   trace-cmd report

   # Launch interactive GUI
   kernelshark trace.dat


📊 dmesg / journalctl (System Logs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Watch kernel logs in real-time:**

.. code-block:: bash

   # Real-time kernel logs
   dmesg -W

   # Filter by subsystem
   dmesg | grep -i block
   dmesg | grep -i memory

   # Follow journal
   journalctl -f

   # Errors only
   journalctl PRIORITY=err

Tool Deep Dives & Examples
================================================================================

ftrace (Function Tracer – Always Built-in)

Core Methodologies (Problem Solving)
================================================================================

🎓 USE Method (Utilization / Saturation / Errors)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Systematic approach to identify system bottleneck:

1. **Utilization**: What % of resource is in use?
   
   .. code-block:: bash
   
      top                           # CPU utilization
      iostat -x 1                   # Disk utilization
      free -h                       # Memory utilization

2. **Saturation**: How much queuing/waiting?
   
   .. code-block:: bash
   
      vmstat 1 10                   # runqueue size
      iostat -x 1 | grep '%'        # I/O queue saturation
      cat /proc/pressure/cpu        # CPU pressure

3. **Errors**: Count of errors?
   
   .. code-block:: bash
   
      dmesg | tail                  # System errors
      cat /proc/pressure/io         # I/O pressure stall
      cat /proc/pressure/memory     # Memory pressure


📈 Flame Graphs (Best Visualization for Call Stacks)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why:** Width = CPU time, Height = call depth. Easy to spot hot spots.

**Generate from perf:**

.. code-block:: bash

   # Record profile
   perf record -F 99 -g -- sleep 30

   # Convert to flame graph
   perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg

   # View in browser
   python3 -m http.server 8000
   # Then open http://localhost:8000/flame.svg

**Generate from bpftrace:**

.. code-block:: bash

   # Record CPU profile
   bpftrace -e 'profile:hz:99 { @[kstack] = count(); }' > stacks.txt

   # Convert to flame graph
   cat stacks.txt | stackcollapse-bpftrace.pl | flamegraph.pl > flame.svg


🔄 Off-CPU Analysis (Why Threads Not Running)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Application slow but CPU usage low → threads blocked

**Solution:** Measure off-CPU time (where threads waiting)

.. code-block:: bash

   # Using bcc tool
   offcputime -f -p `pgrep myprocess` 10 > offcpu.stacks
   cat offcpu.stacks | flamegraph.pl > offcpu.svg

   # Using bpftrace (scheduler switches)
   bpftrace -e 'tracepoint:sched:sched_switch { @[stack] = count(); }'


📉 Latency Distribution Analysis (Not Just Averages!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Average latency looks good but p99 is terrible

**Solution:** Measure distribution (percentiles, histograms)

.. code-block:: bash

   # Block I/O latency distribution
   bpftrace -e 'tracepoint:block:block_rq_issue { @start[args[0]] = nsecs; }
                tracepoint:block:block_rq_complete /@start[args[0]]/ {
                  @latency[comm] = hist((nsecs - @start[args[0]]) / 1000);
                  delete(@start[args[0]]);
                }'

   # Syscall latency by type
   perf record -e syscalls:sys_enter -a -- sleep 10
   perf script | perf stat


🔒 Lock Contention Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Find mutex/spinlock bottlenecks:**

.. code-block:: bash

   # Using perf
   perf record -e contention:lock_acquire -g -- sleep 10
   perf report

   # Using bpftrace
   bpftrace -e 'kprobe:__mutex_lock_slowpath { @[stack] = count(); }'

   # Using bcc
   /usr/share/bcc/tools/lockstat


⚙️ Memory Profiling
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Memory allocation frequency
   bpftrace -e 'uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc { @[ustack] = count(); }'

   # Detect memory leaks
   memleak -p `pgrep myprocess`

   # Page fault rate
   bpftrace -e 'software:page-faults { @[comm] = count(); }'


🌐 Network Performance Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # TCP connection tracking
   tcpconnect -t

   # Network packet loss
   tcpdrop -t

   # Socket statistics
   ss -s

   # Network packet distribution
   bpftrace -e 'tracepoint:net:net_dev_xmit { @[args[0]] = count(); }'


Quick Wins (Most Powerful One-Liners)
================================================================================

💡 CPU Profiling & Flame Graphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Classic CPU flame graph (perf)
   perf record -F 99 -g -- sleep 30
   perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg

   # 2. Kernel hot spots (bpftrace)
   bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'

   # 3. Live profiling (like top)
   perf top -F 99 -g --sort comm,dso,sym


💡 I/O & Storage Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 4. Block device I/O latency
   biolatency

   # 5. File system reads/writes
   vfscount

   # 6. Disk I/O statistics
   iostat -x 1


💡 Off-CPU & Scheduling
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 7. Off-CPU time flame graph
   offcputime -f -p `pgrep myprocess` 10 > offcpu.stacks

   # 8. Scheduler runqueue latency
   runqlat

   # 9. Context switch analysis
   perf record -e sched:sched_switch -g -- sleep 10


💡 Tracing & Events
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 10. List all available events
   perf list tracepoint:*

   # 11. Syscall count by process
   bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

   # 12. Function call count (ftrace)
   echo function > /sys/kernel/tracing/current_tracer
   echo 'vfs*' > /sys/kernel/tracing/set_ftrace_filter
   echo 1 > /sys/kernel/tracing/tracing_on; sleep 5; echo 0 > /sys/kernel/tracing/tracing_on
   cat /sys/kernel/tracing/trace


Real-World Debugging Scenarios
================================================================================

🔴 Scenario 1: High CPU but Application Slow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checklist:**

.. code-block:: bash

   # Step 1: Which process?
   top -b -n1 | head -15

   # Step 2: CPU profile
   perf record -F 99 -g -- sleep 30
   perf report              # Look for hot functions

   # Step 3: Detailed annotation
   perf annotate my_hot_function

   # Step 4: Context switches? Lock contention?
   perf record -e sched:sched_switch -g -- sleep 10


🔴 Scenario 2: Application Stalled (Not Responding)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checklist:**

.. code-block:: bash

   # Step 1: Is it running?
   ps aux | grep myapp

   # Step 2: Why not running? (Off-CPU)
   offcputime -p `pgrep myapp` 10

   # Step 3: System load?
   vmstat 1 5

   # Step 4: Blocked on I/O?
   lsof -p `pgrep myapp`

   # Step 5: Lock contention?
   perf lock record -p `pgrep myapp`


🔴 Scenario 3: High Memory Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checklist:**

.. code-block:: bash

   # Step 1: Memory stats
   free -h
   cat /proc/meminfo

   # Step 2: Memory leaks?
   memleak -p `pgrep myapp`

   # Step 3: Memory pressure
   cat /proc/pressure/memory

   # Step 4: Page fault rate
   perf stat -e page-faults -p `pgrep myapp`


🔴 Scenario 4: Slow I/O
~~~~~~~~~~~~~~~~~~~~~~~

**Checklist:**

.. code-block:: bash

   # Step 1: I/O stats
   iostat -x 1 5

   # Step 2: I/O latency
   biolatency

   # Step 3: Detailed block layer trace
   trace-cmd record -e block:* -- sleep 10
   trace-cmd report

   # Step 4: Process-specific I/O
   lsof -p `pgrep myapp`


Installation & Setup
================================================================================

📦 Most Linux Distros (Debian/Ubuntu)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Essential tools
   sudo apt install -y \
       linux-tools-generic \
       linux-tools-`uname -r` \
       trace-cmd \
       kernelshark \
       bpftrace \
       bpfcc-tools

   # FlameGraph (required for flame graphs)
   git clone https://github.com/brendangregg/FlameGraph.git
   export PATH="$PATH:$PWD/FlameGraph"


✅ Verify Kernel Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check if CONFIG_FTRACE enabled
   zcat /proc/config.gz | grep CONFIG_FTRACE

   # Check perf_events
   zcat /proc/config.gz | grep CONFIG_PERF_EVENTS

   # Check eBPF support
   zcat /proc/config.gz | grep CONFIG_BPF


Best Practices & Decision Tree
================================================================================

**Starting Point (Order of Preference):**

1. **🥇 Start with perf** — Safe, powerful, always available

   .. code-block:: bash

      perf record -F 99 -g -- sleep 30
      perf report


2. **🥈 Need custom insight fast?** → **bpftrace** one-liner

   .. code-block:: bash

      bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'


3. **🥉 Building production tools?** → **bcc** (reusable Python/C)


4. **Flame graphs needed?** → **perf + FlameGraph**


5. **Full-system detailed trace?** → **trace-cmd / KernelShark**


6. **Deep function flow?** → **ftrace function_graph**


**Decision Tree – Choose Tool:**

.. code-block:: text

   Need to debug/trace/profile?

   ├── Quick function graph?
   │   └── → ftrace function_graph
   │
   ├── CPU profiling, flame graphs, PMU?
   │   └── → perf (default best choice!)
   │
   ├── Custom histogram/aggregation/one-liner?
   │   ├── Fast experiment? → bpftrace
   │   └── Reusable tool? → bcc
   │
   └── Full-system trace?
       └── → trace-cmd / KernelShark / LTTng


Key Takeaways
================================================================================

✨ **Measurement over Guessing**
   Always measure before optimizing. Measurement bias is real.

✨ **Flame Graphs Rule**
   Best visualization for stack traces. Almost always reveals bottlenecks.

✨ **Prefer Stable APIs**
   Tracepoints > Kfuncs > Kprobes (prefer stable over unstable)

✨ **Histograms > Averages**
   Distribution matters more than mean. Use p99, not average.

✨ **Simple First**
   perf → bpftrace → bcc → custom. Start simple.

✨ **Know Your Overhead**
   Sampling < Instrumentation. Watch for measurement bias.

✨ **Off-CPU Analysis Often Wins**
   When CPU low but slow, threads are blocked. Check off-CPU time.


================================================================================

**Happy kernel hunting!** ⚡🐧

*References: Brendan Gregg's performance analysis resources (https://www.brendangregg.com) – the gold standard for Linux performance profiling.*