================================================================================
Linux Kernel Debug, Tracing & Security - Comprehensive Cheatsheet
================================================================================

:Author: Linux Kernel Documentation Team
:Date: January 17, 2026
:Version: 1.0
:Target Audience: Kernel developers, embedded engineers, security auditors
:Scope: ftrace, perf, eBPF/bpftrace, KGDB/JTAG, kernel auditing, secure boot

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**Essential Debug Commands**:

.. code-block:: bash

    # ftrace: Quick function tracing
    cd /sys/kernel/tracing
    echo function_graph > current_tracer
    echo 'vfs_*' > set_ftrace_filter
    cat trace
    
    # perf: CPU profiling
    perf record -F 99 -g -- sleep 30
    perf report
    
    # bpftrace: One-liner syscall trace
    bpftrace -e 'tracepoint:syscalls:sys_enter_openat { 
        printf("%s: %s\n", comm, str(args->filename)); 
    }'
    
    # KGDB: Remote kernel debugging
    # Boot with: kgdbwait kgdboc=ttyS0,115200
    (gdb) target remote /dev/ttyS0
    (gdb) break do_sys_open
    (gdb) continue

**Tool Selection Decision Tree**:

+---------------------------+---------------------+------------------+--------------+
| **Use Case**              | **Tool**            | **Overhead**     | **Accuracy** |
+===========================+=====================+==================+==============+
| Function call graph       | ftrace function_graph| 5-10x           | Exact        |
+---------------------------+---------------------+------------------+--------------+
| CPU hot spots             | perf top            | 2-5x             | Statistical  |
+---------------------------+---------------------+------------------+--------------+
| Custom kernel tracing     | bpftrace            | 1-2x             | Exact        |
+---------------------------+---------------------+------------------+--------------+
| Syscall tracing           | strace              | 100-1000x        | Exact        |
+---------------------------+---------------------+------------------+--------------+
| Kernel breakpoints        | KGDB/JTAG           | N/A (stopped)    | Exact        |
+---------------------------+---------------------+------------------+--------------+
| Security auditing         | auditd              | <1%              | Exact        |
+---------------------------+---------------------+------------------+--------------+

**ftrace Quick Start**:

.. code-block:: bash

    # Enable function tracer
    echo function > /sys/kernel/tracing/current_tracer
    
    # Trace specific functions (glob patterns)
    echo 'sys_*' > set_ftrace_filter          # All syscalls
    echo 'vfs_read' >> set_ftrace_filter      # Append
    echo '!vfs_write' >> set_ftrace_filter    # Exclude
    
    # Trace specific PID
    echo $PID > set_ftrace_pid
    
    # View trace
    cat trace                                  # One-time
    cat trace_pipe                             # Continuous
    
    # Clear trace
    echo > trace

**perf Event Categories**:

.. code-block:: text

    Hardware Events:     cpu-cycles, instructions, cache-misses, branch-misses
    Software Events:     context-switches, page-faults, cpu-migrations
    Tracepoints:         syscalls:sys_enter_*, sched:sched_switch, block:*
    Hardware Cache:      L1-dcache-loads, L1-icache-load-misses, LLC-loads
    Kprobes:             probe:do_sys_open (dynamic)

**eBPF Program Types**:

.. code-block:: text

    BPF_PROG_TYPE_KPROBE:        Kernel function entry/exit
    BPF_PROG_TYPE_TRACEPOINT:    Static tracepoints (stable ABI)
    BPF_PROG_TYPE_PERF_EVENT:    Performance counter overflow
    BPF_PROG_TYPE_XDP:           High-performance packet filtering
    BPF_PROG_TYPE_SOCKET_FILTER: Socket-level packet filtering

**KGDB vs JTAG**:

+------------------+------------------------+---------------------------+
| **Feature**      | **KGDB (Software)**    | **JTAG (Hardware)**       |
+==================+========================+===========================+
| Hardware needed  | Serial/USB             | JTAG probe ($50-$2000)    |
+------------------+------------------------+---------------------------+
| Early boot debug | ❌ No                  | ✅ Yes                    |
+------------------+------------------------+---------------------------+
| Panic recovery   | Limited                | Excellent                 |
+------------------+------------------------+---------------------------+
| Breakpoints      | SW (limited)           | HW (unlimited)            |
+------------------+------------------------+---------------------------+
| Setup complexity | Easy                   | Medium                    |
+------------------+------------------------+---------------------------+

**Audit System Quick Commands**:

.. code-block:: bash

    # Check audit status
    auditctl -s
    
    # Monitor file access
    auditctl -w /etc/passwd -p rwxa -k passwd_changes
    
    # Monitor syscall
    auditctl -a always,exit -F arch=b64 -S open -S openat -k file_open
    
    # Search audit logs
    ausearch -k passwd_changes
    ausearch -ts today -m SYSCALL
    
    # Generate report
    aureport --summary

**Secure Boot Chain**:

.. code-block:: text

    UEFI Firmware (PK + KEK) 
        → Bootloader (MOK database)
            → Kernel (kernel lockdown)
                → Modules (module signing)
                    → IMA (integrity measurement)

================================================================================
Section 1: ftrace - Function Tracer
================================================================================

1.1 Overview
================================================================================

**What is ftrace?**

ftrace is the kernel's built-in tracing framework for analyzing kernel behavior:
- Function-level tracing (which functions called, when, duration)
- Latency analysis (irq-off, preempt-off, wakeup latency)
- Event tracing (stable tracepoints for syscalls, scheduler, block I/O)
- Dynamic tracing (kprobes for any kernel function)

**Key Properties**:
- Always compiled into kernel (no special packages)
- Ring buffer (never fills disk, circular buffer)
- Low overhead when disabled (static branches)
- Can trace both kernel and user context

**ftrace Interface**:

.. code-block:: bash

    # Modern location (kernel 4.1+)
    /sys/kernel/tracing/
    
    # Legacy location (still works via symlink)
    /sys/kernel/debug/tracing/

**Available Tracers**:

+---------------------+-------------------------------------------------------+
| **Tracer**          | **Purpose**                                           |
+=====================+=======================================================+
| function            | Trace all kernel function calls                       |
+---------------------+-------------------------------------------------------+
| function_graph      | Call graph with entry/exit times                      |
+---------------------+-------------------------------------------------------+
| irqsoff             | Find longest IRQ-disabled section                     |
+---------------------+-------------------------------------------------------+
| preemptoff          | Find longest preemption-disabled section              |
+---------------------+-------------------------------------------------------+
| wakeup              | Measure wakeup latency for highest priority task      |
+---------------------+-------------------------------------------------------+
| wakeup_rt           | Same, but only RT tasks                               |
+---------------------+-------------------------------------------------------+
| blk                 | Block I/O tracing                                     |
+---------------------+-------------------------------------------------------+
| nop                 | Disable function tracing (use events only)            |
+---------------------+-------------------------------------------------------+

1.2 Function Tracing
================================================================================

**Basic Function Tracer**:

.. code-block:: bash

    cd /sys/kernel/tracing
    
    # Enable function tracer
    echo function > current_tracer
    
    # Optional: Filter functions (reduces overhead)
    echo 'do_sys_open*' > set_ftrace_filter
    
    # Trigger action (e.g., run command that calls open())
    cat /etc/hostname
    
    # View trace
    head -50 trace

**Output Format**:

.. code-block:: text

    # tracer: function
    #
    # entries-in-buffer/entries-written: 142/142   #P:4
    #
    #                              _-----=> irqs-off
    #                             / _----=> need-resched
    #                            | / _---=> hardirq/softirq
    #                            || / _--=> preempt-depth
    #                            ||| /     delay
    #           TASK-PID   CPU#  ||||    TIMESTAMP  FUNCTION
    #              | |       |   ||||       |         |
               bash-1234  [001] .... 12345.678901: do_sys_open <-sys_open
               bash-1234  [001] .... 12345.678902: getname <-do_sys_open
               bash-1234  [001] .... 12345.678903: kmem_cache_alloc <-getname

**Explanation**:
- **irqs-off**: ``d`` = IRQs disabled, ``.`` = enabled
- **need-resched**: ``N`` = need resched, ``.`` = no
- **hardirq/softirq**: ``H`` = hardirq, ``s`` = softirq, ``.`` = none
- **preempt-depth**: Preemption nesting level

**Function Graph Tracer**:

.. code-block:: bash

    echo function_graph > current_tracer
    echo do_sys_open > set_graph_function
    cat trace

**Output**:

.. code-block:: text

     1)               |  do_sys_open() {
     1)               |    getname() {
     1)   0.876 us    |      kmem_cache_alloc();
     1)   1.234 us    |      strncpy_from_user();
     1)   3.456 us    |    }
     1)               |    get_unused_fd_flags() {
     1)   0.654 us    |      __alloc_fd();
     1)   1.123 us    |    }
     1)               |    do_filp_open() {
     1)               |      path_openat() {
     1)  42.123 us    |        link_path_walk();
     1)  56.789 us    |      }
     1)  60.234 us    |    }
     1)  67.890 us    |  }

**Key**: Duration in microseconds (us), nested function calls indented.

1.3 Event Tracing
================================================================================

**List Available Events**:

.. code-block:: bash

    # All events
    ls events/
    
    # Syscall events
    ls events/syscalls/
    
    # Scheduler events
    ls events/sched/

**Enable Event Tracing**:

.. code-block:: bash

    # Enable all syscall entry events
    echo 1 > events/syscalls/sys_enter_open/enable
    echo 1 > events/syscalls/sys_enter_openat/enable
    
    # Or enable entire category
    echo 1 > events/syscalls/enable
    
    # Disable function tracer (use events only)
    echo nop > current_tracer
    
    # View events
    cat trace_pipe

**Output**:

.. code-block:: text

               bash-1234  [001] .... 12345.678: sys_enter_openat: dfd: ffffff9c, filename: 7ffc1234abcd, flags: 80000, mode: 0

**Event Filtering**:

.. code-block:: bash

    # Filter by filename argument (requires string match)
    echo 'filename ~ "*/passwd"' > events/syscalls/sys_enter_openat/filter
    
    # Filter by PID
    echo 'common_pid == 1234' > events/syscalls/sys_enter_openat/filter
    
    # Complex filter
    echo 'flags & 64 && dfd == -100' > events/syscalls/sys_enter_openat/filter
    
    # Clear filter
    echo 0 > events/syscalls/sys_enter_openat/filter

1.4 Latency Tracers
================================================================================

**IRQ Latency** (irqsoff):

.. code-block:: bash

    # Find longest IRQ-disabled section
    echo 0 > tracing_max_latency      # Reset
    echo irqsoff > current_tracer
    
    # Trigger workload
    ./run_test
    
    # Check maximum latency found
    cat tracing_max_latency
    # Output: 234 (microseconds)
    
    # See trace of longest section
    cat trace

**Preemption Latency** (preemptoff):

.. code-block:: bash

    echo 0 > tracing_max_latency
    echo preemptoff > current_tracer
    # Run workload
    cat tracing_max_latency

**Wakeup Latency**:

.. code-block:: bash

    # Measure time from wakeup to scheduled
    echo wakeup_rt > current_tracer
    
    # Trigger RT task wakeup
    chrt -f 99 ./rt_test
    
    cat tracing_max_latency

1.5 Dynamic Tracing (kprobes)
================================================================================

**Add Kprobe**:

.. code-block:: bash

    # Trace kernel function entry
    echo 'p:my_open do_sys_open' > kprobe_events
    
    # Trace with arguments (requires BTF or debug info)
    echo 'p:my_open do_sys_open dfd=%di filename=%si' > kprobe_events
    
    # Trace function return
    echo 'r:my_open_ret do_sys_open ret=%ax' > kprobe_events
    
    # Enable kprobe event
    echo 1 > events/kprobes/my_open/enable
    
    # View
    cat trace_pipe

**Remove Kprobe**:

.. code-block:: bash

    echo '-:my_open' > kprobe_events

**Kprobe with Stacktrace**:

.. code-block:: bash

    # Enable stacktrace on event trigger
    echo 'stacktrace' > events/kprobes/my_open/trigger
    echo 1 > events/kprobes/my_open/enable

1.6 trace-cmd (User-Friendly Frontend)
================================================================================

**Installation**:

.. code-block:: bash

    apt install trace-cmd kernelshark

**Record Trace**:

.. code-block:: bash

    # Record all scheduler events
    trace-cmd record -e 'sched:*'
    
    # Record function graph for specific function
    trace-cmd record -p function_graph -g do_sys_open
    
    # Record with plugin
    trace-cmd record -p function -l 'vfs_*' -- ls /tmp
    
    # System-wide for 10 seconds
    trace-cmd record -e all sleep 10

**View Trace**:

.. code-block:: bash

    # Text report
    trace-cmd report
    
    # GUI viewer
    kernelshark trace.dat

**List Available Events**:

.. code-block:: bash

    trace-cmd list -e

================================================================================
Section 2: perf - Performance Analysis Tool
================================================================================

2.1 Overview
================================================================================

**What is perf?**

perf is the Linux profiling tool with a performance counter subsystem:
- CPU profiling (sampling at fixed frequency)
- Hardware counter access (PMU - Performance Monitoring Unit)
- Software event counting (context switches, page faults)
- Tracepoint recording (syscalls, block I/O, scheduler)
- Flamegraph generation

**Installation**:

.. code-block:: bash

    # Ubuntu/Debian
    apt install linux-tools-generic linux-tools-$(uname -r)
    
    # Check version
    perf --version

**Common Workflow**:

.. code-block:: text

    perf list → perf record → perf report → perf annotate
       ↓            ↓             ↓              ↓
    Find events  Record data   Analyze       See assembly

2.2 CPU Profiling
================================================================================

**Basic CPU Profile**:

.. code-block:: bash

    # Sample at 99 Hz with call graph
    perf record -F 99 -g -- ./myapp
    
    # System-wide profiling (requires root)
    perf record -F 99 -g -a -- sleep 30
    
    # Exclude kernel samples (userspace only)
    perf record -F 99 -g --exclude-kernel -- ./myapp

**View Results**:

.. code-block:: bash

    # TUI (text user interface)
    perf report
    
    # Navigate: arrow keys, Enter to expand, q to quit
    # Press 'a' to annotate function (see assembly)
    # Press 'g' to show call graph

**Report Output Example**:

.. code-block:: text

    Samples: 10K of event 'cpu-clock', Event count (approx.): 2500000000
    Overhead  Command  Shared Object      Symbol
      45.67%  myapp    myapp              [.] hot_function
      23.45%  myapp    libc.so.6          [.] __memcpy_sse2
      12.34%  myapp    [kernel.kallsyms]  [k] copy_user_generic_unrolled
       8.90%  myapp    myapp              [.] warm_function

**Explanation**:
- **Overhead**: % of samples in this function
- **[.]**: Userspace function
- **[k]**: Kernel function

**Top-like Live View**:

.. code-block:: bash

    # Live profiling (updates in real-time)
    perf top -F 99 -g
    
    # Filter by process
    perf top -p $(pgrep myapp)
    
    # Kernel only
    perf top -U

2.3 Hardware Performance Counters
================================================================================

**List Available Events**:

.. code-block:: bash

    # All events
    perf list
    
    # Hardware events only
    perf list hardware
    
    # Cache events
    perf list cache
    
    # Tracepoints
    perf list tracepoint

**Common Hardware Events**:

+---------------------------+--------------------------------------------------+
| **Event**                 | **Description**                                  |
+===========================+==================================================+
| cpu-cycles                | CPU cycles (accounts for frequency scaling)      |
+---------------------------+--------------------------------------------------+
| instructions              | Retired instructions                             |
+---------------------------+--------------------------------------------------+
| cache-misses              | Last-level cache misses                          |
+---------------------------+--------------------------------------------------+
| branch-misses             | Mispredicted branches                            |
+---------------------------+--------------------------------------------------+
| L1-dcache-load-misses     | L1 data cache load misses                        |
+---------------------------+--------------------------------------------------+
| LLC-loads                 | Last-level cache loads                           |
+---------------------------+--------------------------------------------------+
| dTLB-load-misses          | Data TLB load misses                             |
+---------------------------+--------------------------------------------------+

**Performance Statistics**:

.. code-block:: bash

    # Basic stats
    perf stat ./myapp
    
    # Output:
    #  Performance counter stats for './myapp':
    #
    #       1234.567890      task-clock (msec)         #    0.999 CPUs utilized
    #               123      context-switches          #    0.100 K/sec
    #                12      cpu-migrations            #    0.010 K/sec
    #             1,234      page-faults               #    1.000 K/sec
    #     3,123,456,789      cycles                    #    2.530 GHz
    #     2,345,678,901      instructions              #    0.75  insn per cycle
    #       234,567,890      branches                  #  190.000 M/sec
    #        12,345,678      branch-misses             #    5.26% of all branches

**Custom Event Selection**:

.. code-block:: bash

    # Specific events
    perf stat -e cycles,instructions,cache-misses ./myapp
    
    # Multiple runs with statistics
    perf stat -r 10 ./myapp
    
    # Interval statistics (print every 1000ms)
    perf stat -I 1000 -e cycles,instructions

**IPC (Instructions Per Cycle)**:

.. code-block:: bash

    perf stat -e cycles,instructions ./myapp
    
    # Good IPC: >2.0 (vectorized code)
    # Average: 0.5-1.5
    # Poor: <0.5 (cache misses, branch mispredicts)

2.4 Event Tracing
================================================================================

**Syscall Tracing**:

.. code-block:: bash

    # Trace all syscalls
    perf trace ./myapp
    
    # Trace specific syscalls
    perf trace -e open,read,write ./myapp
    
    # Summary statistics
    perf trace -s ./myapp

**Output**:

.. code-block:: text

    0.123 ( 0.045 ms): ls/12345 openat(dfd: CWD, filename: ".", flags: CLOEXEC|DIRECTORY|NONBLOCK) = 3
    0.234 ( 0.012 ms): ls/12345 fstat(fd: 3, statbuf: 0x7ffc12345678) = 0
    0.345 ( 0.089 ms): ls/12345 getdents64(fd: 3, dirent: 0x555512345000, count: 32768) = 584

**Record Tracepoint Events**:

.. code-block:: bash

    # Record scheduler events
    perf record -e sched:sched_switch -e sched:sched_wakeup -a -- sleep 10
    
    # Record block I/O
    perf record -e block:block_rq_issue -e block:block_rq_complete -a
    
    # Record syscalls
    perf record -e 'syscalls:sys_enter_*' ./myapp

**View Recorded Events**:

.. code-block:: bash

    perf script
    
    # Output:
    #     myapp 12345 [001] 123456.789: syscalls:sys_enter_openat: dfd: 0xffffff9c, filename: 0x7ffc..., flags: 0x80000

2.5 Advanced Profiling
================================================================================

**Off-CPU Profiling** (where time is spent waiting):

.. code-block:: bash

    # Record scheduler events with stacktraces
    perf record -e sched:sched_switch -e sched:sched_stat_sleep \
                -e sched:sched_stat_blocked -g -a -- sleep 30
    
    # Analyze with flamegraph
    perf script | stackcollapse-perf.pl | flamegraph.pl > offcpu.svg

**Lock Contention**:

.. code-block:: bash

    # Record lock events
    perf lock record -- ./myapp
    
    # Report contended locks
    perf lock report
    
    # Output shows:
    #  - Lock address
    #  - Total wait time
    #  - Max wait time
    #  - Number of contentions

**Cache Analysis**:

.. code-block:: bash

    # Record cache misses with sample IP
    perf record -e cache-misses -g -- ./myapp
    
    # See which functions have most cache misses
    perf report
    
    # Annotate to see exact instructions
    perf annotate

**Memory Access Profiling** (requires Intel PEBS or AMD IBS):

.. code-block:: bash

    # Sample memory loads
    perf mem record ./myapp
    
    # Report memory accesses
    perf mem report

2.6 Flamegraphs
================================================================================

**Installation**:

.. code-block:: bash

    git clone https://github.com/brendangregg/FlameGraph.git
    export PATH=$PATH:$PWD/FlameGraph

**Generate Flamegraph**:

.. code-block:: bash

    # Record with call graph
    perf record -F 99 -g -- ./myapp
    
    # Convert to flamegraph
    perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
    
    # View in browser
    firefox flame.svg

**Kernel Flamegraph**:

.. code-block:: bash

    # System-wide kernel profiling
    perf record -F 99 -g -a -- sleep 30
    perf script | stackcollapse-perf.pl | flamegraph.pl --color=java > kernel_flame.svg

**Differential Flamegraph**:

.. code-block:: bash

    # Before optimization
    perf record -F 99 -g -o perf.before.data -- ./myapp
    
    # After optimization
    perf record -F 99 -g -o perf.after.data -- ./myapp
    
    # Generate diff
    perf script -i perf.before.data | stackcollapse-perf.pl > before.folded
    perf script -i perf.after.data | stackcollapse-perf.pl > after.folded
    difffolded.pl before.folded after.folded | flamegraph.pl > diff.svg

2.7 Perf Tips and Tricks
================================================================================

**Reduce Data File Size**:

.. code-block:: bash

    # Compress during record
    perf record --compression-level=9 -F 99 -g -- ./myapp
    
    # Filter by function
    perf record -F 99 -g -e cpu-clock --filter 'ip >= 0x400000 && ip < 0x500000'

**Inject Build IDs** (for symbol resolution later):

.. code-block:: bash

    perf record -F 99 -g -- ./myapp
    perf buildid-cache --add ./myapp
    perf inject -b -i perf.data -o perf.data.build-id

**Record with Context**:

.. code-block:: bash

    # Include CPU, TID, time
    perf record -F 99 -g -e cycles:u --sample-cpu

**Per-Thread Profiling**:

.. code-block:: bash

    # Profile specific thread
    perf record -F 99 -g -t 12345

**Watch Specific Event Count**:

.. code-block:: bash

    # Count events without sampling
    perf stat -e cycles,instructions -d -d -d ./myapp
    # -d: detailed counters (cache, TLB)
    # -d -d: very detailed
    # -d -d -d: very very detailed

================================================================================
Section 3: eBPF and bpftrace
================================================================================

3.1 eBPF Overview
================================================================================

**What is eBPF?**

Extended Berkeley Packet Filter - in-kernel VM for safe, efficient programs:
- Bytecode verified before loading (safety guarantee)
- JIT compilation to native code (performance)
- Access to kernel data structures (visibility)
- Maps for data storage and user communication
- No kernel module compilation needed

**Key Components**:

+------------------+-------------------------------------------------------+
| **Component**    | **Purpose**                                           |
+==================+=======================================================+
| Verifier         | Ensures program safety (no loops, bounded execution)  |
+------------------+-------------------------------------------------------+
| JIT Compiler     | Converts bytecode to x86/ARM native code              |
+------------------+-------------------------------------------------------+
| Maps             | Key-value storage (hash, array, ring buffer)          |
+------------------+-------------------------------------------------------+
| Helpers          | Kernel functions callable from eBPF                   |
+------------------+-------------------------------------------------------+
| Program Types    | kprobe, tracepoint, XDP, tc, cgroup, etc.             |
+------------------+-------------------------------------------------------+

**eBPF Program Flow**:

.. code-block:: text

    User Space                  Kernel Space
    ┌─────────────┐            ┌──────────────────┐
    │ BPF Program │ ─ load ──> │ Verifier         │
    │ (C code)    │            │  - Check safety  │
    └─────────────┘            │  - No infinite   │
           │                   │    loops         │
           │ compile           │  - Bounded mem   │
           ↓                   └────────┬─────────┘
    ┌─────────────┐                    │ verified
    │ Bytecode    │                    ↓
    └─────────────┘            ┌──────────────────┐
           │                   │ JIT Compiler     │
           └─────────────────> │  - Native code   │
                               └────────┬─────────┘
                                        │
                                        ↓
                                ┌──────────────────┐
                                │ Attach to hook   │
                                │  - kprobe        │
                                │  - tracepoint    │
                                │  - XDP           │
                                └────────┬─────────┘
                                        │ events
                                        ↓
                                ┌──────────────────┐
                                │ Update eBPF Maps │
                                └────────┬─────────┘
                                        │
                   ┌────────────────────┘
                   ↓
    ┌─────────────────────────┐
    │ User reads from maps    │
    └─────────────────────────┘

3.2 bpftrace - High-Level eBPF Tool
================================================================================

**Installation**:

.. code-block:: bash

    apt install bpftrace
    
    # Check version (needs 0.9+ for best features)
    bpftrace --version

**bpftrace Syntax**:

.. code-block:: text

    probe_type:probe_name [/filter/] { actions }
    
    Examples:
    kprobe:do_sys_open { @opens = count(); }
    tracepoint:syscalls:sys_enter_openat { printf("%s\n", str(args->filename)); }
    interval:s:1 { print(@opens); clear(@opens); }

**One-Liner Examples**:

.. code-block:: bash

    # Count syscalls by process
    bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'
    
    # Trace file opens with filename
    bpftrace -e 'tracepoint:syscalls:sys_enter_openat { 
        printf("%s: %s\n", comm, str(args->filename)); 
    }'
    
    # Histogram of read sizes
    bpftrace -e 'tracepoint:syscalls:sys_exit_read /args->ret > 0/ { 
        @bytes = hist(args->ret); 
    }'
    
    # Count kernel function calls
    bpftrace -e 'kprobe:vfs_* { @[probe] = count(); }'
    
    # Trace slow syscalls (>10ms)
    bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @start[tid] = nsecs; }
                 tracepoint:raw_syscalls:sys_exit /@start[tid]/ {
                   $dur = (nsecs - @start[tid]) / 1000000;
                   if ($dur > 10) {
                     printf("%s: %d ms\n", comm, $dur);
                   }
                   delete(@start[tid]);
                 }'

**Probe Types**:

+----------------------+--------------------------------------------------+
| **Probe**            | **Description**                                  |
+======================+==================================================+
| kprobe:func          | Kernel function entry                            |
+----------------------+--------------------------------------------------+
| kretprobe:func       | Kernel function return                           |
+----------------------+--------------------------------------------------+
| tracepoint:cat:name  | Static tracepoint (stable ABI)                   |
+----------------------+--------------------------------------------------+
| uprobe:path:func     | Userspace function entry                         |
+----------------------+--------------------------------------------------+
| uretprobe:path:func  | Userspace function return                        |
+----------------------+--------------------------------------------------+
| profile:hz:99        | Timer-based sampling at 99 Hz                    |
+----------------------+--------------------------------------------------+
| interval:s:1         | Timed output every 1 second                      |
+----------------------+--------------------------------------------------+
| BEGIN                | Program start                                    |
+----------------------+--------------------------------------------------+
| END                  | Program termination (Ctrl-C)                     |
+----------------------+--------------------------------------------------+

3.3 bpftrace Built-in Variables and Functions
================================================================================

**Built-in Variables**:

.. code-block:: c

    pid       // Process ID
    tid       // Thread ID
    uid       // User ID
    comm      // Process name (char[16])
    nsecs     // Nanoseconds timestamp
    cpu       // CPU ID
    probe     // Full probe name
    args      // Probe arguments (tracepoint)
    retval    // Return value (kretprobe, uretprobe)
    arg0-argN // Function arguments (kprobe, uprobe)

**Functions**:

.. code-block:: c

    // String operations
    str(char *ptr)              // Convert pointer to string
    printf("fmt", ...)          // Print formatted output
    
    // Kernel access
    kstack()                    // Kernel stack trace
    ustack()                    // User stack trace
    ksym(addr)                  // Kernel symbol name
    usym(addr)                  // User symbol name
    
    // Aggregations (stored in maps)
    count()                     // Count events
    sum(value)                  // Sum values
    avg(value)                  // Average
    min(value)                  // Minimum
    max(value)                  // Maximum
    hist(value)                 // Power-of-2 histogram
    lhist(value, min, max, step) // Linear histogram
    
    // Time
    nsecs                       // Current timestamp (ns)
    elapsed                     // Time since program start (ns)
    
    // Control
    exit()                      // Terminate program
    print(@map)                 // Print map contents
    clear(@map)                 // Clear map
    delete(@map[key])           // Delete map entry

3.4 bpftrace Scripts (Multi-Line Programs)
================================================================================

**CPU Profiling Script** (profile.bt):

.. code-block:: c

    #!/usr/bin/env bpftrace
    
    BEGIN
    {
        printf("Profiling CPU... Hit Ctrl-C to end.\n");
    }
    
    profile:hz:99
    {
        @[kstack()] = count();
    }
    
    END
    {
        printf("\nTop 10 kernel stacks:\n");
        print(@, 10);
        clear(@);
    }

**Run**:

.. code-block:: bash

    chmod +x profile.bt
    ./profile.bt

**File Open Tracer** (opensnoop.bt):

.. code-block:: c

    #!/usr/bin/env bpftrace
    
    BEGIN
    {
        printf("%-10s %-6s %-16s %s\n", "TIME", "PID", "COMM", "FILE");
    }
    
    tracepoint:syscalls:sys_enter_openat
    {
        printf("%-10u %-6d %-16s %s\n",
               elapsed / 1000000,  // ms
               pid,
               comm,
               str(args->filename));
    }

**Slow Syscall Tracer** (slowsyscalls.bt):

.. code-block:: c

    #!/usr/bin/env bpftrace
    
    tracepoint:raw_syscalls:sys_enter
    {
        @start[tid] = nsecs;
    }
    
    tracepoint:raw_syscalls:sys_exit
    /@start[tid]/
    {
        $duration_ms = (nsecs - @start[tid]) / 1000000;
        
        if ($duration_ms > 10) {
            time("%H:%M:%S ");
            printf("%s (pid %d): %d ms\n",
                   comm, pid, $duration_ms);
        }
        
        delete(@start[tid]);
    }
    
    END
    {
        clear(@start);
    }

**Memory Allocation Tracking** (mallocsnoop.bt):

.. code-block:: c

    #!/usr/bin/env bpftrace
    
    uprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc
    {
        @alloc_size[tid] = arg0;  // Size argument
    }
    
    uretprobe:/lib/x86_64-linux-gnu/libc.so.6:malloc
    /@alloc_size[tid]/
    {
        printf("%s pid %d malloc(%d) = %p\n",
               comm, pid, @alloc_size[tid], retval);
        
        @total_alloc = sum(@alloc_size[tid]);
        delete(@alloc_size[tid]);
    }
    
    uprobe:/lib/x86_64-linux-gnu/libc.so.6:free
    {
        printf("%s pid %d free(%p)\n", comm, pid, arg0);
    }
    
    END
    {
        printf("\nTotal allocated: %d bytes\n", @total_alloc);
        clear(@alloc_size);
        clear(@total_alloc);
    }

3.5 BCC (BPF Compiler Collection)
================================================================================

**Overview**:

BCC provides Python/Lua frontends for writing eBPF programs:
- More powerful than bpftrace (full programming language)
- Reusable tools (execsnoop, biosnoop, tcplife, etc.)
- Production-ready monitoring agents

**Installation**:

.. code-block:: bash

    apt install bpfcc-tools python3-bpfcc
    
    # Tools installed in /usr/share/bcc/tools/
    ls /usr/share/bcc/tools/

**Common BCC Tools**:

.. code-block:: bash

    # Trace process execution
    execsnoop
    
    # Trace file opens
    opensnoop
    
    # Trace block I/O
    biosnoop
    biolatency          # I/O latency histogram
    
    # Trace TCP connections
    tcpconnect
    tcplife
    
    # CPU profiling
    profile
    
    # Off-CPU profiling
    offcputime
    
    # Memory leaks
    memleak -p $(pgrep myapp)
    
    # Count kernel/user function calls
    funccount 'vfs_*'

**BCC Python Example** (trace_openat.py):

.. code-block:: python

    #!/usr/bin/env python3
    from bcc import BPF
    
    # eBPF program (C code)
    prog = """
    #include <uapi/linux/ptrace.h>
    
    struct data_t {
        u32 pid;
        char comm[16];
        char filename[256];
    };
    
    BPF_PERF_OUTPUT(events);
    
    TRACEPOINT_PROBE(syscalls, sys_enter_openat)
    {
        struct data_t data = {};
        
        data.pid = bpf_get_current_pid_tgid() >> 32;
        bpf_get_current_comm(&data.comm, sizeof(data.comm));
        bpf_probe_read_user_str(&data.filename, sizeof(data.filename),
                                (void *)args->filename);
        
        events.perf_submit(args, &data, sizeof(data));
        return 0;
    }
    """
    
    # Load BPF program
    b = BPF(text=prog)
    
    # Define event handler
    def print_event(cpu, data, size):
        event = b["events"].event(data)
        print(f"{event.pid:<6} {event.comm.decode():<16} {event.filename.decode()}")
    
    # Print header
    print(f"{'PID':<6} {'COMM':<16} FILENAME")
    
    # Open perf buffer
    b["events"].open_perf_buffer(print_event)
    
    # Poll for events
    try:
        while True:
            b.perf_buffer_poll()
    except KeyboardInterrupt:
        pass

**Run**:

.. code-block:: bash

    chmod +x trace_openat.py
    sudo ./trace_openat.py

3.6 eBPF Maps
================================================================================

**Map Types**:

+------------------------+--------------------------------------------------+
| **Map Type**           | **Use Case**                                     |
+========================+==================================================+
| BPF_MAP_TYPE_HASH      | General key-value storage                        |
+------------------------+--------------------------------------------------+
| BPF_MAP_TYPE_ARRAY     | Fixed-size array, fast access                    |
+------------------------+--------------------------------------------------+
| BPF_MAP_TYPE_PERCPU_*  | Per-CPU data (no locking needed)                 |
+------------------------+--------------------------------------------------+
| BPF_MAP_TYPE_LRU_HASH  | Hash with automatic eviction (bounded size)      |
+------------------------+--------------------------------------------------+
| BPF_MAP_TYPE_RINGBUF   | Lock-free ring buffer (kernel 5.8+)             |
+------------------------+--------------------------------------------------+
| BPF_MAP_TYPE_STACK_TRACE| Store stack traces                               |
+------------------------+--------------------------------------------------+

**BCC Map Example**:

.. code-block:: python

    prog = """
    BPF_HASH(counts, u64, u64);  // Map: pid -> count
    
    int trace_open(struct pt_regs *ctx)
    {
        u64 pid = bpf_get_current_pid_tgid() >> 32;
        u64 *val, zero = 0;
        
        val = counts.lookup_or_try_init(&pid, &zero);
        if (val) {
            (*val)++;
        }
        
        return 0;
    }
    """
    
    b = BPF(text=prog)
    b.attach_kprobe(event="do_sys_open", fn_name="trace_open")
    
    # Read map
    for k, v in b["counts"].items():
        print(f"PID {k.value}: {v.value} opens")

================================================================================
Section 4: KGDB and JTAG Kernel Debugging
================================================================================

4.1 Overview
================================================================================

**Two Approaches to Kernel Debugging**:

1. **KGDB** (Software debugger):
   - GDB stub built into kernel
   - Connects via serial/USB
   - Simple setup, no extra hardware
   - Works after kernel boots

2. **JTAG** (Hardware debugger):
   - External hardware probe
   - Can debug bootloader + early kernel
   - Hardware breakpoints (unlimited)
   - More reliable on panics

**When to Use Each**:

.. code-block:: text

    Need to debug...
    ├── Early boot / bootloader → JTAG
    ├── Kernel panic (hard hang) → JTAG (more reliable)
    ├── Normal driver development → KGDB (simpler)
    ├── QEMU/virtual machine → Built-in gdbstub (easiest)
    └── Production system → ftrace/perf/eBPF (no debugger)

4.2 KGDB Setup
================================================================================

**Kernel Configuration**:

.. code-block:: bash

    CONFIG_KGDB=y
    CONFIG_KGDB_SERIAL_CONSOLE=y
    CONFIG_DEBUG_INFO=y              # DWARF debug symbols
    CONFIG_FRAME_POINTER=y            # Better backtraces
    CONFIG_GDB_SCRIPTS=y              # Helper scripts (lx-*)
    CONFIG_MAGIC_SYSRQ=y              # For triggering KGDB

**Boot with KGDB Enabled**:

.. code-block:: bash

    # Wait for debugger at boot
    kgdbwait kgdboc=ttyS0,115200
    
    # Or for USB serial
    kgdboc=ttyUSB0,115200
    
    # Disable KASLR (for stable addresses)
    nokaslr

**Trigger KGDB After Boot**:

.. code-block:: bash

    # From running system
    echo g > /proc/sysrq-trigger
    
    # Or Alt+SysRq+G (on console)

**Connect GDB from Host**:

.. code-block:: bash

    # Terminal 1: Watch kernel output (optional)
    screen /dev/ttyUSB0 115200
    
    # Terminal 2: Start GDB
    gdb ./vmlinux
    
    (gdb) set serial baud 115200
    (gdb) target remote /dev/ttyUSB0
    
    # Kernel is now halted, waiting for commands

4.3 JTAG Setup
================================================================================

**Hardware Needed**:

- JTAG probe: ST-Link ($15), J-Link EDU ($60), or OpenOCD-compatible
- Target board with JTAG/SWD header
- Jumper wires (GND, SWDIO, SWCLK, optionally RESET)

**OpenOCD Installation**:

.. code-block:: bash

    apt install openocd gdb-multiarch
    
    # Verify probe detected
    lsusb | grep -i stlink

**OpenOCD Configuration**:

.. code-block:: bash

    # Start OpenOCD (connects to hardware)
    openocd -f interface/stlink.cfg -f target/stm32h7x.cfg
    
    # Output should show:
    # Info : Listening on port 3333 for gdb connections

**Connect GDB**:

.. code-block:: bash

    # Use appropriate GDB for architecture
    gdb-multiarch ./vmlinux
    # or: arm-linux-gnueabihf-gdb ./vmlinux
    
    (gdb) target remote :3333
    (gdb) monitor reset halt
    (gdb) hbreak start_kernel
    (gdb) continue

4.4 Essential GDB Commands
================================================================================

**Breakpoints**:

.. code-block:: bash

    # Software breakpoint (KGDB, limited number)
    break do_sys_open
    break fs/open.c:1234
    
    # Hardware breakpoint (JTAG, unlimited)
    hbreak do_sys_open
    hbreak *0x80000000        # Address
    
    # Conditional breakpoint
    break do_sys_open if fd > 10
    
    # Temporary breakpoint (auto-delete after hit)
    tbreak start_kernel
    
    # List/delete breakpoints
    info breakpoints
    delete 1                  # Delete breakpoint #1
    clear do_sys_open         # Clear all at function

**Stepping**:

.. code-block:: bash

    step        # Step into (source level)
    next        # Step over (source level)
    stepi       # Step instruction (assembly level)
    nexti       # Next instruction
    finish      # Run until function returns
    continue    # Resume execution
    until 123   # Run until line 123

**Examining Data**:

.. code-block:: bash

    # Print variable
    print current->pid
    print task->comm
    
    # Print in hex/binary/decimal
    print/x address
    print/t flags
    print/d count
    
    # Dereference pointer
    print *ptr
    
    # Print structure
    print *current
    
    # Print array
    print argv[0]@10          # 10 elements starting at argv[0]
    
    # Examine memory
    x/10x 0x80000000          # 10 hex words
    x/10i $pc                 # 10 instructions at PC
    x/s 0x12345678            # String

**Backtraces**:

.. code-block:: bash

    backtrace               # Full backtrace
    bt                      # Short form
    bt full                 # Include local variables
    frame 3                 # Switch to frame #3
    up                      # Move up stack frame
    down                    # Move down stack frame
    info frame              # Current frame info
    info locals             # Local variables
    info args               # Function arguments

**Registers**:

.. code-block:: bash

    info registers          # All registers
    info all-registers      # Including FPU/vector
    print/x $pc             # Program counter
    print/x $sp             # Stack pointer
    set $rax = 0            # Modify register

**Threads/Tasks**:

.. code-block:: bash

    info threads            # List all kernel threads
    thread 5                # Switch to thread #5
    thread apply all bt     # Backtrace of all threads

4.5 Kernel-Specific GDB Commands (lx-*)
================================================================================

**Available with CONFIG_GDB_SCRIPTS=y**:

.. code-block:: bash

    (gdb) lx-symbols                # Load module symbols dynamically
    (gdb) lx-dmesg                  # Print kernel log buffer
    (gdb) lx-ps                     # List processes
    (gdb) lx-tasks                  # List tasks with more detail
    (gdb) lx-iomem                  # I/O memory regions
    (gdb) lx-ioports                # I/O port ranges
    (gdb) lx-mounts                 # Show mount points
    (gdb) lx-device-list-bus usb    # List USB devices
    (gdb) lx-fdtdump                # Dump device tree (ARM)

**Example Session**:

.. code-block:: bash

    (gdb) target remote /dev/ttyUSB0
    (gdb) lx-symbols
    loading vmlinux
    scanning for modules in /path/to/build
    (gdb) lx-dmesg | tail -20
    [    1.234567] random: fast init done
    [    2.345678] EXT4-fs (mmcblk0p2): mounted filesystem
    
    (gdb) lx-ps
    0xffff888012345678  1 init
    0xffff888023456789  2 kthreadd
    
    (gdb) break do_sys_open
    (gdb) continue

4.6 Debugging Kernel Panics
================================================================================

**With kdump (Crash Dumps)**:

.. code-block:: bash

    # Reserve crash kernel memory (boot parameter)
    crashkernel=256M
    
    # Load crash kernel
    kexec -p /boot/vmlinuz --initrd=/boot/initrd.img \
          --append="root=/dev/sda1 single irqpoll maxcpus=1"
    
    # After panic, analyze with crash utility
    crash /usr/lib/debug/vmlinux /var/crash/vmcore
    
    crash> bt                       # Backtrace of panicking CPU
    crash> log                      # Kernel log
    crash> ps                       # Process list at crash time
    crash> vm                       # Virtual memory info
    crash> files                    # Open files

**With KGDB (If System Responds)**:

.. code-block:: bash

    # Configure to enter KGDB on panic
    echo 1 > /proc/sys/kernel/panic_on_oops
    
    # Boot parameter
    kgdboc=ttyS0,115200 kgdbwait
    
    # On panic, KGDB activates automatically
    # Connect GDB and investigate

**With JTAG (Most Reliable)**:

.. code-block:: bash

    # System hangs, no response
    # JTAG probe can still halt CPU
    
    (gdb) monitor halt
    (gdb) bt                        # See where it hung
    (gdb) info threads              # Check all CPUs
    (gdb) thread apply all bt       # Backtraces from all CPUs

4.7 Common Debugging Scenarios
================================================================================

**Scenario 1: Driver Not Loading**:

.. code-block:: bash

    (gdb) break driver_probe_device
    (gdb) continue
    # Trigger module load
    
    (gdb) bt
    (gdb) print *dev
    (gdb) print *drv

**Scenario 2: Kernel Hang**:

.. code-block:: bash

    # Enter KGDB
    echo g > /proc/sysrq-trigger
    
    (gdb) target remote /dev/ttyUSB0
    (gdb) info threads              # Check what each CPU is doing
    (gdb) thread apply all bt
    
    # Look for spinlock loops, infinite loops

**Scenario 3: Memory Corruption**:

.. code-block:: bash

    # Enable KASAN (kernel address sanitizer)
    CONFIG_KASAN=y
    
    # Or use KGDB to watch memory
    (gdb) watch *(int*)0x12345678
    (gdb) continue
    # Stops when memory location changes

**Scenario 4: Race Condition**:

.. code-block:: bash

    # Set breakpoint in suspected code
    (gdb) break suspicious_function
    (gdb) commands
    > silent
    > printf "Called from CPU %d\n", smp_processor_id()
    > continue
    > end
    
    (gdb) continue
    # Watch for pattern indicating race

**Scenario 5: System Call Debugging**:

.. code-block:: bash

    (gdb) break do_sys_open
    (gdb) commands
    > printf "open: %s\n", filename
    > continue
    > end
    
    # Or conditional breakpoint
    (gdb) break do_sys_open if strcmp(filename, "/etc/passwd") == 0

4.8 Tips and Tricks
================================================================================

**Load Module Symbols Dynamically**:

.. code-block:: bash

    (gdb) lx-symbols
    # Automatically loads symbols for all loaded modules

**Set Breakpoint Before Module Load**:

.. code-block:: bash

    # Use pending breakpoint
    (gdb) break my_module_init
    Make breakpoint pending on future shared library load? (y or [n]) y
    
    # Load module
    (gdb) continue
    # Breakpoint hits when module loads

**Debug Kernel Threads**:

.. code-block:: bash

    (gdb) lx-ps | grep kworker
    (gdb) thread find "kworker/0:1"
    (gdb) thread <number>
    (gdb) bt

**Examine Data Structures**:

.. code-block:: bash

    # Cast and dereference
    (gdb) print *(struct task_struct *)0xffff888012345678
    
    # Follow linked list
    (gdb) print ((struct list_head *)0x...)->next
    
    # With helper
    (gdb) lx-list-check 0x... task_struct tasks

**Call Kernel Functions** (Dangerous!):

.. code-block:: bash

    # Can call non-sleeping functions
    (gdb) call printk("Debug message\n")
    (gdb) call dump_stack()
    
    # Check result
    (gdb) print $

================================================================================
Section 5: Kernel Security and Auditing
================================================================================

5.1 Linux Audit System
================================================================================

**Overview**:

The Linux Audit system provides:
- System call auditing (who did what, when)
- File access monitoring
- Security event logging
- Compliance reporting (PCI-DSS, HIPAA, etc.)

**Components**:

+------------------+------------------------------------------------------+
| **Component**    | **Purpose**                                          |
+==================+======================================================+
| auditd           | Audit daemon (collects and logs events)             |
+------------------+------------------------------------------------------+
| auditctl         | Configure audit rules                                |
+------------------+------------------------------------------------------+
| ausearch         | Search audit logs                                    |
+------------------+------------------------------------------------------+
| aureport         | Generate audit reports                               |
+------------------+------------------------------------------------------+
| audispd          | Audit event dispatcher (plugins)                     |
+------------------+------------------------------------------------------+

**Installation**:

.. code-block:: bash

    apt install auditd audispd-plugins
    systemctl enable auditd
    systemctl start auditd

5.2 Audit Rules
================================================================================

**Check Audit Status**:

.. code-block:: bash

    auditctl -s
    
    # Output:
    # enabled 1
    # failure 1
    # pid 1234
    # rate_limit 0
    # backlog_limit 8192
    # lost 0
    # backlog 0

**File/Directory Watches**:

.. code-block:: bash

    # Monitor file for all accesses (read, write, execute, attribute change)
    auditctl -w /etc/passwd -p rwxa -k passwd_changes
    
    # Monitor directory recursively
    auditctl -w /etc -p wa -k etc_changes
    
    # Monitor only writes
    auditctl -w /var/log -p w -k log_changes

**Parameters**:
- ``-w``: Watch path
- ``-p``: Permissions (r=read, w=write, x=execute, a=attribute)
- ``-k``: Key (tag for searching)

**System Call Auditing**:

.. code-block:: bash

    # Audit all open/openat syscalls
    auditctl -a always,exit -F arch=b64 -S open -S openat -k file_open
    
    # Audit unlink (file deletion)
    auditctl -a always,exit -F arch=b64 -S unlink -S unlinkat -k file_delete
    
    # Audit execve (program execution)
    auditctl -a always,exit -F arch=b64 -S execve -k exec
    
    # Audit with filter (only specific UID)
    auditctl -a always,exit -F arch=b64 -S openat -F uid=1000 -k user1000_opens

**Rule Fields**:
- ``-a``: Append rule (always=log all, exit=log on syscall exit)
- ``-F``: Filter (arch, syscall, uid, gid, pid, etc.)
- ``-S``: System call name/number

**Pre-configured Rules** (Best Practice):

.. code-block:: bash

    # Load rules from file
    auditctl -R /etc/audit/rules.d/audit.rules
    
    # Example rules file:
    cat <<EOF > /etc/audit/rules.d/audit.rules
    # Delete all rules
    -D
    
    # Buffer size
    -b 8192
    
    # Failure mode (0=silent, 1=printk, 2=panic)
    -f 1
    
    # Monitor authentication
    -w /etc/shadow -p wa -k shadow_changes
    -w /etc/sudoers -p wa -k sudo_changes
    
    # Monitor system calls
    -a always,exit -F arch=b64 -S mount -S umount2 -k mount_changes
    -a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -k perm_changes
    
    # Monitor privileged commands
    -a always,exit -F path=/usr/bin/sudo -F perm=x -k sudo_exec
    -a always,exit -F path=/usr/bin/su -F perm=x -k su_exec
    
    # Make rules immutable (reboot to change)
    -e 2
    EOF

**List Current Rules**:

.. code-block:: bash

    auditctl -l

5.3 Searching Audit Logs
================================================================================

**ausearch - Search Logs**:

.. code-block:: bash

    # Search by key
    ausearch -k passwd_changes
    
    # Search by time
    ausearch -ts today
    ausearch -ts this-week
    ausearch -ts 10:00
    ausearch -ts 01/17/2026 10:00:00
    
    # Search by event type
    ausearch -m SYSCALL
    ausearch -m USER_LOGIN
    ausearch -m USER_AUTH
    
    # Search by UID
    ausearch -ua 1000
    
    # Search by syscall
    ausearch -sc openat
    
    # Combine filters
    ausearch -ts today -k file_open -i
    # -i: Interpret fields (convert UIDs to usernames, etc.)

**Output Format**:

.. code-block:: text

    type=SYSCALL msg=audit(1705491234.567:12345): arch=c000003e syscall=257 \
      success=yes exit=3 a0=ffffff9c a1=7ffc12345678 a2=80000 a3=0 items=1 \
      ppid=1234 pid=5678 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 \
      fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=pts0 ses=3 comm="cat" \
      exe="/usr/bin/cat" key="file_open"
    
    type=PATH msg=audit(1705491234.567:12345): item=0 name="/etc/passwd" \
      inode=12345 dev=08:01 mode=0100644 ouid=0 ogid=0 rdev=00:00 \
      nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0

**Interpretation**:
- **arch=c000003e**: x86_64 architecture
- **syscall=257**: openat (syscall number)
- **success=yes**: Syscall succeeded
- **auid=1000**: Audit UID (login UID, doesn't change with su/sudo)
- **uid=1000**: Current UID
- **comm="cat"**: Command name
- **key="file_open"**: Audit rule key

5.4 Audit Reports
================================================================================

**aureport - Generate Reports**:

.. code-block:: bash

    # Summary report
    aureport --summary
    
    # Authentication report
    aureport --auth
    
    # Failed events
    aureport --failed
    
    # File access report
    aureport -f
    
    # Executable report
    aureport -x
    
    # User report
    aureport -u
    
    # Time range
    aureport --start 01/17/2026 00:00:00 --end 01/17/2026 23:59:59

**Example Summary Output**:

.. code-block:: text

    Summary Report
    ======================
    Range of time in logs: 01/17/2026 00:00:01 - 01/17/2026 23:59:59
    Selected time for report: 01/17/2026 00:00:01 - 01/17/2026 23:59:59
    Number of changes in configuration: 5
    Number of changes to accounts, groups, or roles: 3
    Number of logins: 42
    Number of failed logins: 7
    Number of authentications: 156
    Number of failed authentications: 12
    Number of users: 8
    Number of terminals: 15
    Number of host names: 3
    Number of executables: 234
    Number of files: 567
    Number of AVC's: 0
    Number of MAC events: 0
    Number of failed syscalls: 23
    Number of anomaly events: 0
    Number of responses to anomaly events: 0
    Number of crypto events: 45
    Number of keys: 12
    Number of process IDs: 1234
    Number of events: 5678

5.5 Secure Boot and Kernel Lockdown
================================================================================

**Secure Boot Chain**:

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ UEFI Firmware                           │
    │ - Platform Key (PK)                     │
    │ - Key Exchange Key (KEK)                │
    │ - Signature Database (db)               │
    │ - Forbidden Signatures (dbx)            │
    └────────────┬────────────────────────────┘
                 │ verifies
                 ↓
    ┌─────────────────────────────────────────┐
    │ Bootloader (GRUB/shim)                  │
    │ - Signed with Microsoft key (db)        │
    │ - Or signed with MOK (Machine Owner Key)│
    └────────────┬────────────────────────────┘
                 │ verifies
                 ↓
    ┌─────────────────────────────────────────┐
    │ Linux Kernel                            │
    │ - Signed with distro key or MOK         │
    │ - CONFIG_MODULE_SIG=y                   │
    │ - Lockdown mode (integrity/confidentiality)│
    └────────────┬────────────────────────────┘
                 │ verifies
                 ↓
    ┌─────────────────────────────────────────┐
    │ Kernel Modules                          │
    │ - Signature checked                     │
    │ - Trusted keyring                       │
    └────────────┬────────────────────────────┘
                 │ measures
                 ↓
    ┌─────────────────────────────────────────┐
    │ IMA (Integrity Measurement Architecture)│
    │ - TPM PCR values                        │
    │ - Runtime integrity checking            │
    └─────────────────────────────────────────┘

**Check Secure Boot Status**:

.. code-block:: bash

    # UEFI Secure Boot
    dmesg | grep -i "secure boot"
    mokutil --sb-state
    
    # Kernel lockdown mode
    cat /sys/kernel/security/lockdown
    # Output: none [integrity] confidentiality

**Lockdown Modes**:

+-----------------+-------------------------------------------------------+
| **Mode**        | **Restrictions**                                      |
+=================+=======================================================+
| none            | No restrictions                                       |
+-----------------+-------------------------------------------------------+
| integrity       | Block modification of running kernel:                 |
|                 | - No /dev/mem, /dev/kmem access                       |
|                 | - No kexec of unsigned kernels                        |
|                 | - No hibernation                                      |
|                 | - No module loading without signature                 |
+-----------------+-------------------------------------------------------+
| confidentiality | All integrity restrictions plus:                      |
|                 | - No kernel module parameters writable                |
|                 | - No ACPI custom tables                               |
|                 | - No perf CPU events                                  |
|                 | - No BPF write to kernel memory                       |
+-----------------+-------------------------------------------------------+

**Enable Lockdown**:

.. code-block:: bash

    # Boot parameter
    lockdown=integrity
    # or
    lockdown=confidentiality

**Module Signing**:

.. code-block:: bash

    # Check if module is signed
    modinfo -F sig_id mymodule
    
    # Sign module manually
    /lib/modules/$(uname -r)/build/scripts/sign-file \
        sha256 \
        /path/to/signing_key.pem \
        /path/to/signing_key.x509 \
        mymodule.ko
    
    # Verify signature
    modinfo mymodule.ko | grep sig

**Trusted Keyrings**:

.. code-block:: bash

    # View trusted keys
    keyctl list %:.builtin_trusted_keys
    keyctl list %:.platform
    
    # Add MOK (Machine Owner Key) for custom modules
    mokutil --import my-signing-key.der
    # Reboot and enroll key in MOK manager

5.6 Kernel Hardening
================================================================================

**Key Security Features**:

.. code-block:: bash

    # KASLR (Kernel Address Space Layout Randomization)
    CONFIG_RANDOMIZE_BASE=y
    # Boot: kaslr (enabled by default on most distros)
    
    # KPTI (Kernel Page Table Isolation) - Meltdown mitigation
    CONFIG_PAGE_TABLE_ISOLATION=y
    # Boot: pti=on (default if vulnerable CPU)
    
    # SMEP/SMAP (Supervisor Mode Execution/Access Prevention)
    # Automatically enabled if CPU supports
    dmesg | grep -i "smep\|smap"
    
    # Stack Canaries
    CONFIG_STACKPROTECTOR=y
    CONFIG_STACKPROTECTOR_STRONG=y
    
    # Hardened usercopy
    CONFIG_HARDENED_USERCOPY=y
    
    # FORTIFY_SOURCE
    CONFIG_FORTIFY_SOURCE=y

**Runtime Protections**:

.. code-block:: bash

    # Restrict dmesg to root
    kernel.dmesg_restrict = 1
    
    # Restrict access to kernel pointers
    kernel.kptr_restrict = 2
    
    # Disable module loading
    kernel.modules_disabled = 1
    
    # Restrict BPF to CAP_SYS_ADMIN (not CAP_BPF)
    kernel.unprivileged_bpf_disabled = 1
    
    # Restrict perf events
    kernel.perf_event_paranoid = 3
    
    # Restrict ptrace
    kernel.yama.ptrace_scope = 1

**Apply sysctl Settings**:

.. code-block:: bash

    # Add to /etc/sysctl.d/99-security.conf
    cat <<EOF > /etc/sysctl.d/99-security.conf
    kernel.dmesg_restrict = 1
    kernel.kptr_restrict = 2
    kernel.unprivileged_bpf_disabled = 1
    kernel.perf_event_paranoid = 3
    kernel.yama.ptrace_scope = 1
    EOF
    
    # Apply immediately
    sysctl -p /etc/sysctl.d/99-security.conf

**SELinux/AppArmor**:

.. code-block:: bash

    # SELinux status
    sestatus
    getenforce
    
    # Set to enforcing
    setenforce 1
    
    # AppArmor status
    aa-status
    
    # Set profile to enforce
    aa-enforce /etc/apparmor.d/usr.bin.myapp

================================================================================
Section 6: Exam Question
================================================================================

**Question (18 points): Comprehensive Debug & Security Analysis**

You are debugging a production embedded Linux system (automotive gateway) experiencing:
1. Intermittent high latency (>100ms) on CAN message forwarding
2. Suspected security issue: unauthorized file access to /etc/can_config
3. System occasionally panics with "NULL pointer dereference" in custom driver

**Requirements**:

**Part A (6 points): Performance Analysis**

Using ftrace, perf, and bpftrace, identify the latency source:

1. Design an ftrace configuration to trace the CAN message path
   - Which tracer (function, function_graph, irqsoff)?
   - What filter functions?
   - How to minimize overhead?

2. Write a bpftrace script to measure latency from CAN RX interrupt to userspace delivery
   - Trace both kernel (interrupt) and userspace (socketcan)
   - Calculate and histogram latency distribution
   - Filter for CAN ID 0x123 only

3. Use perf to identify CPU bottlenecks
   - What events to record?
   - How to generate flamegraph?

**Part B (6 points): Security Auditing**

Configure comprehensive auditing:

1. Create audit rules to:
   - Monitor all accesses to /etc/can_config
   - Track all CAN-related syscalls (socket, bind, send, recv with AF_CAN)
   - Log all executions of /usr/bin/can_gateway_ctrl

2. Write ausearch commands to:
   - Find who accessed /etc/can_config today
   - List all failed CAN socket operations
   - Generate report of all CAN gateway control executions

3. Configure audit alerts:
   - Real-time alert on unauthorized /etc/can_config write
   - Use audispd plugin to send syslog

**Part C (4 points): Crash Analysis**

The panic message shows:

.. code-block:: text

    BUG: unable to handle kernel NULL pointer dereference at 0000000000000018
    IP: [<ffffffffa0123456>] can_gateway_forward+0x42/0x120 [can_gw]
    Call Trace:
    [<ffffffff81234567>] can_receive+0x89/0xc0
    [<ffffffff81345678>] __netif_receive_skb_core+0x456/0x890

Configure KGDB to debug:

1. What kernel config options needed?
2. What boot parameters?
3. How to set conditional breakpoint in can_gateway_forward when skb is NULL?
4. How to examine the sk_buff structure when breakpoint hits?

**Part D (2 points): Security Hardening**

Recommend kernel security configurations and runtime settings for this embedded system.

--------------------------------------------------------------------------------
**Answer:**
--------------------------------------------------------------------------------

**Part A: Performance Analysis (6 points)**

**1. ftrace Configuration** (2 points):

.. code-block:: bash

    cd /sys/kernel/tracing
    
    # Use irqsoff tracer to find longest IRQ-disabled sections
    echo 0 > tracing_max_latency        # Reset
    echo irqsoff > current_tracer
    
    # Filter for CAN-related functions
    echo 'can_*' > set_ftrace_filter
    echo 'netif_rx*' >> set_ftrace_filter
    echo '__netif_receive_skb*' >> set_ftrace_filter
    
    # Trigger workload
    # ... CAN traffic ...
    
    # Check maximum latency
    cat tracing_max_latency
    # Expected output: 150 (microseconds) - indicates >100ms elsewhere
    
    # View trace of longest section
    cat trace

**Why this config**:
- ``irqsoff``: Detects IRQ-disabled sections (can cause latency)
- Filter: Reduces overhead by only tracing CAN path
- Alternative: ``wakeup_rt`` if CAN handler is RT task

**2. bpftrace Latency Script** (2 points):

.. code-block:: c

    #!/usr/bin/env bpftrace
    
    BEGIN
    {
        printf("Tracing CAN latency for ID 0x123... Ctrl-C to end\n");
    }
    
    // Trace CAN RX interrupt (hardware IRQ)
    kprobe:can_rx_interrupt
    {
        @rx_start[tid] = nsecs;
    }
    
    // Trace userspace socketcan read (syscall exit)
    tracepoint:syscalls:sys_exit_recvfrom
    /@rx_start[tid] && args->ret > 0/
    {
        // Read CAN frame from user buffer (requires ptr)
        $can_id = *(uint32_t *)(args->buf);
        
        // Filter for CAN ID 0x123
        if (($can_id & 0x1FFFFFFF) == 0x123) {
            $latency_us = (nsecs - @rx_start[tid]) / 1000;
            
            @latency_hist = hist($latency_us);
            @latency_max = max($latency_us);
            @count++;
            
            // Alert on high latency
            if ($latency_us > 100000) {  // >100ms
                time("%H:%M:%S ");
                printf("HIGH LATENCY: CAN 0x123: %d us (pid %d)\n",
                       $latency_us, pid);
            }
        }
        
        delete(@rx_start[tid]);
    }
    
    END
    {
        printf("\n=== CAN ID 0x123 Latency Analysis ===\n");
        printf("Frames received: %d\n", @count);
        printf("Max latency: %d us\n", @latency_max);
        printf("\nLatency distribution (microseconds):\n");
        print(@latency_hist);
        
        clear(@rx_start);
        clear(@latency_hist);
        clear(@latency_max);
        clear(@count);
    }

**Key Points**:
- Measures from hardware interrupt to userspace read
- Histogram shows distribution (helps identify if latency is consistent or spiky)
- Real-time alerts for violations

**3. perf CPU Bottleneck Analysis** (2 points):

.. code-block:: bash

    # Record CPU profile with call graph
    perf record -F 99 -g -a -- sleep 60
    
    # Also record cache misses (may cause latency)
    perf record -e cpu-clock,cache-misses,context-switches -g -a -- sleep 60
    
    # Generate flamegraph
    perf script | stackcollapse-perf.pl | flamegraph.pl > can_flame.svg
    
    # View in browser - look for wide blocks in CAN path
    firefox can_flame.svg
    
    # Alternative: Interactive TUI
    perf report
    # Look for hot functions in can_gateway_forward

**Expected findings**:
- Flamegraph shows if CAN path is CPU-bound
- Cache misses indicate memory bottleneck
- Context switches indicate scheduling issues

**Part B: Security Auditing (6 points)**

**1. Audit Rules** (3 points):

.. code-block:: bash

    # Create /etc/audit/rules.d/can_gateway.rules
    cat <<EOF > /etc/audit/rules.d/can_gateway.rules
    # Monitor /etc/can_config access
    -w /etc/can_config -p rwxa -k can_config_access
    
    # Track CAN socket syscalls (AF_CAN = 29)
    # socket(AF_CAN, SOCK_RAW, CAN_RAW)
    -a always,exit -F arch=b64 -S socket -F a0=29 -k can_socket_create
    
    # bind on CAN socket
    -a always,exit -F arch=b64 -S bind -k can_socket_bind
    
    # sendto/recvfrom on CAN
    -a always,exit -F arch=b64 -S sendto -k can_send
    -a always,exit -F arch=b64 -S recvfrom -k can_recv
    
    # Track CAN gateway control tool execution
    -a always,exit -F path=/usr/bin/can_gateway_ctrl -F perm=x -k can_gw_exec
    
    # Track failures
    -a always,exit -F arch=b64 -S socket -F a0=29 -F success=0 -k can_socket_fail
    EOF
    
    # Load rules
    auditctl -R /etc/audit/rules.d/can_gateway.rules
    
    # Verify
    auditctl -l | grep can

**2. ausearch Commands** (2 points):

.. code-block:: bash

    # Who accessed /etc/can_config today?
    ausearch -ts today -k can_config_access -i
    
    # Output shows:
    # type=SYSCALL ... auid=user1 uid=user1 comm="vi" exe="/usr/bin/vi" key="can_config_access"
    # type=PATH ... name="/etc/can_config" inode=12345 ouid=root ogid=root
    
    # Failed CAN socket operations
    ausearch -k can_socket_fail -i
    
    # Or all CAN syscalls with failures
    ausearch -k can_socket_create,can_socket_bind -x -if --success no
    
    # CAN gateway control executions with report
    aureport -x --start today | grep can_gateway_ctrl
    
    # Detailed view
    ausearch -k can_gw_exec -i --format csv > can_gw_audit.csv

**3. Real-time Alerts** (1 point):

.. code-block:: bash

    # Install audisp plugin
    apt install audispd-plugins
    
    # Configure /etc/audit/plugins.d/syslog.conf
    cat <<EOF > /etc/audit/plugins.d/syslog.conf
    active = yes
    direction = out
    path = builtin_syslog
    type = builtin
    args = LOG_INFO LOG_LOCAL6
    format = string
    EOF
    
    # Add rule with action
    auditctl -w /etc/can_config -p wa -k can_config_write
    
    # Configure rsyslog to alert (/etc/rsyslog.d/50-audit.conf)
    cat <<EOF > /etc/rsyslog.d/50-audit.conf
    # Forward audit alerts to monitoring system
    :msg, contains, "can_config_write" @@monitoring.example.com:514
    
    # Or send email (requires mail setup)
    :msg, contains, "can_config_write" ^/usr/local/bin/send_security_alert.sh
    EOF
    
    # Restart services
    systemctl restart auditd
    systemctl restart rsyslog

**Part C: Crash Analysis with KGDB (4 points)**

**1. Kernel Config** (1 point):

.. code-block:: bash

    CONFIG_KGDB=y
    CONFIG_KGDB_SERIAL_CONSOLE=y
    CONFIG_DEBUG_INFO=y              # DWARF symbols (required!)
    CONFIG_FRAME_POINTER=y            # Better backtraces
    CONFIG_GDB_SCRIPTS=y              # lx-* commands
    CONFIG_CAN=y
    CONFIG_CAN_GW=m                   # Build as module for symbol loading

**2. Boot Parameters** (1 point):

.. code-block:: bash

    # Boot command line
    console=ttyS0,115200 kgdboc=ttyS0,115200 kgdbwait nokaslr
    
    # Explanation:
    # kgdboc=ttyS0,115200  - KGDB over serial console
    # kgdbwait             - Wait for debugger at boot
    # nokaslr              - Disable KASLR for stable addresses

**3. Conditional Breakpoint** (1 point):

.. code-block:: bash

    # On host machine
    gdb ./vmlinux
    
    (gdb) set serial baud 115200
    (gdb) target remote /dev/ttyUSB0
    
    # Load module symbols
    (gdb) lx-symbols
    # Scans /lib/modules/... and loads can_gw.ko symbols
    
    # Set conditional breakpoint
    (gdb) break can_gateway_forward if skb == 0
    # Or check skb->data is NULL
    (gdb) break can_gateway_forward if skb && skb->data == 0
    
    # Continue
    (gdb) continue
    
    # When breakpoint hits...

**4. Examine sk_buff** (1 point):

.. code-block:: bash

    # Breakpoint hit at can_gateway_forward
    (gdb) print *skb
    # Output shows entire sk_buff structure
    
    # Key fields to check
    (gdb) print skb->data
    (gdb) print skb->len
    (gdb) print skb->head
    (gdb) print skb->end
    (gdb) print skb->protocol
    (gdb) print/x *(struct can_frame *)skb->data
    
    # Backtrace to see call chain
    (gdb) bt
    #0  can_gateway_forward (skb=0x..., data=0x...) at net/can/gw.c:123
    #1  can_receive (skb=0x...) at net/can/af_can.c:456
    #2  __netif_receive_skb_core (...) at net/core/dev.c:789
    
    # Check who allocated skb
    (gdb) print skb->alloc_cpu
    
    # Examine CAN frame payload
    (gdb) x/16xb skb->data
    # Shows: 0x12 0x34 0x00 0x00 ... (CAN ID, flags, data)
    
    # Check reference count (use-after-free?)
    (gdb) print skb->users.refs.counter

**Root Cause Analysis**:

Likely issues:
- skb allocation failure → NULL check missing
- Race condition → freed before use
- DMA issue → data pointer invalid

**Fix**:

.. code-block:: c

    int can_gateway_forward(struct sk_buff *skb, void *data)
    {
        struct can_frame *cf;
        
        // ADD: NULL check
        if (!skb || !skb->data) {
            pr_err("can_gw: NULL skb or data\n");
            return -EINVAL;
        }
        
        cf = (struct can_frame *)skb->data;
        
        // Existing code...
    }

**Part D: Security Hardening (2 points)**

**Kernel Configuration**:

.. code-block:: bash

    # Core security
    CONFIG_SECURITY=y
    CONFIG_SECURITYFS=y
    
    # Stack protection
    CONFIG_STACKPROTECTOR=y
    CONFIG_STACKPROTECTOR_STRONG=y
    
    # Hardened memory
    CONFIG_HARDENED_USERCOPY=y
    CONFIG_FORTIFY_SOURCE=y
    CONFIG_PAGE_TABLE_ISOLATION=y     # KPTI
    CONFIG_RANDOMIZE_BASE=y           # KASLR
    
    # Module signing (automotive requirement)
    CONFIG_MODULE_SIG=y
    CONFIG_MODULE_SIG_FORCE=y         # Reject unsigned modules
    CONFIG_MODULE_SIG_ALL=y
    CONFIG_MODULE_SIG_SHA256=y
    
    # Lockdown
    CONFIG_SECURITY_LOCKDOWN_LSM=y
    CONFIG_LOCK_DOWN_KERNEL_FORCE_INTEGRITY=y
    
    # Audit
    CONFIG_AUDIT=y
    CONFIG_AUDITSYSCALL=y

**Runtime sysctl** (/etc/sysctl.d/99-automotive-hardening.conf):

.. code-block:: bash

    # Restrict kernel info exposure
    kernel.dmesg_restrict = 1
    kernel.kptr_restrict = 2
    
    # Disable module loading after boot (safety-critical)
    kernel.modules_disabled = 1
    
    # Restrict BPF (only allow signed BPF programs)
    kernel.unprivileged_bpf_disabled = 1
    
    # Disable kexec (prevent kernel replacement)
    kernel.kexec_load_disabled = 1
    
    # Network hardening
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.tcp_syncookies = 1

**Boot Parameters**:

.. code-block:: bash

    # Secure boot chain
    lockdown=integrity         # Or =confidentiality for stricter
    module.sig_enforce=1       # Enforce module signatures
    
    # Performance vs security trade-off
    mitigations=auto           # Enable CPU vulnerability mitigations
    # For safety-critical: mitigations=on (even if slower)

**Additional Measures**:

1. **SELinux/AppArmor**: Confine CAN gateway process
2. **Network namespaces**: Isolate CAN interface
3. **Capabilities**: Drop all except CAP_NET_RAW for CAN socket
4. **systemd hardening**: ReadOnlyPaths=/etc (protect config)

================================================================================
Section 7: Best Practices
================================================================================

7.1 Debugging Workflow
================================================================================

**Systematic Approach**:

.. code-block:: text

    1. Reproduce issue reliably
       ├── Minimal test case
       ├── Known trigger
       └── Consistent environment
    
    2. Gather information
       ├── dmesg/journalctl
       ├── /proc/interrupts, /proc/slabinfo
       └── System metrics (CPU, memory, I/O)
    
    3. Form hypothesis
       ├── What subsystem?
       ├── Timing issue? Resource leak?
       └── Race condition?
    
    4. Choose appropriate tool
       ├── Quick insight → bpftrace
       ├── Function flow → ftrace function_graph
       ├── CPU profiling → perf
       ├── Breakpoint debugging → KGDB
       └── Production system → ftrace/eBPF (low overhead)
    
    5. Collect data
       ├── Minimize overhead
       ├── Filter aggressively
       └── Record enough context
    
    6. Analyze
       ├── Look for patterns
       ├── Compare good vs bad runs
       └── Correlate with system events
    
    7. Verify fix
       ├── Reproduce original issue
       ├── Apply fix
       └── Confirm issue resolved

**Tool Selection Matrix**:

+---------------------------+---------------------+---------------------+
| **Scenario**              | **First Choice**    | **Alternative**     |
+===========================+=====================+=====================+
| High CPU usage            | perf top            | bpftrace profile    |
+---------------------------+---------------------+---------------------+
| Slow syscall              | strace -T           | bpftrace            |
+---------------------------+---------------------+---------------------+
| Kernel function latency   | ftrace function_graph| bpftrace kprobe    |
+---------------------------+---------------------+---------------------+
| Memory leak               | /proc/slabinfo      | memleak (BCC)       |
+---------------------------+---------------------+---------------------+
| Deadlock                  | crash (from kdump)  | KGDB backtrace      |
+---------------------------+---------------------+---------------------+
| Race condition            | KASAN/lockdep       | KGDB watchpoint     |
+---------------------------+---------------------+---------------------+
| Interrupt latency         | ftrace irqsoff      | cyclictest          |
+---------------------------+---------------------+---------------------+

7.2 Performance Profiling
================================================================================

**DO**:
✅ Start with low overhead tools (perf, ftrace)
✅ Use sampling for long-running analysis
✅ Filter early (specific functions, PIDs, time ranges)
✅ Generate flamegraphs for visualization
✅ Compare baseline vs problematic runs
✅ Record hardware counters (IPC, cache misses)
✅ Check for obvious bottlenecks first (CPU, I/O wait)

**DON'T**:
❌ Use strace in production (100-1000x overhead)
❌ Trace all kernel functions (use filters!)
❌ Ignore flamegraph methodology (Brendan Gregg's guide)
❌ Profile optimized builds without debug symbols
❌ Assume first hot function is root cause (may be symptom)
❌ Change multiple things before re-measuring

7.3 Security Auditing
================================================================================

**Audit Rule Design**:

✅ **Monitor high-value targets**:
   - Authentication files (/etc/shadow, /etc/sudoers)
   - Configuration files
   - Privileged executables (sudo, su)

✅ **Use specific filters**:
   - Filter by UID for user-specific auditing
   - Use syscall filters (not just file watches)
   - Tag with meaningful keys

✅ **Performance considerations**:
   - Don't audit high-frequency events globally
   - Use auditctl -b to increase buffer if events lost
   - Consider ausearch overhead on large logs

❌ **Avoid**:
   - Auditing every syscall (massive overhead)
   - No key tags (impossible to search)
   - Forgetting to backup/rotate audit logs

**Compliance Mapping**:

+------------------+------------------------------------------------------+
| **Standard**     | **Audit Requirements**                               |
+==================+======================================================+
| PCI-DSS 10.2     | Track all access to cardholder data                  |
+------------------+------------------------------------------------------+
| HIPAA            | Audit access to ePHI                                 |
+------------------+------------------------------------------------------+
| NIST 800-53 AU-2 | Audit security-relevant events                       |
+------------------+------------------------------------------------------+
| ISO 27001 A.12.4 | Logging and monitoring                               |
+------------------+------------------------------------------------------+

7.4 KGDB/JTAG Debugging
================================================================================

**When to Use KGDB**:
✅ Driver development (stable kernel)
✅ Reproducible bugs
✅ Kernel module debugging
✅ Available serial/USB port

**When to Use JTAG**:
✅ Early boot issues
✅ Bootloader debugging
✅ Hard lockups/panics
✅ No console output
✅ Flash programming needed

**Common Pitfalls**:

❌ **Forgetting nokaslr**: Addresses change every boot
❌ **No debug symbols**: CONFIG_DEBUG_INFO=y required
❌ **Optimized builds**: Stepping behaves unpredictably
❌ **Calling sleeping functions**: Deadlocks in KGDB context
❌ **Not using lx-symbols**: Module symbols not loaded

**Efficiency Tips**:

✅ Use conditional breakpoints (avoid manual filtering)
✅ Use commands to automate actions
✅ Prepare scripts for common tasks
✅ Keep vmlinux matching running kernel

7.5 Security Hardening
================================================================================

**Defense in Depth**:

.. code-block:: text

    Layer 1: Boot Security
    ├── UEFI Secure Boot
    ├── Signed bootloader
    └── Kernel lockdown
    
    Layer 2: Kernel Hardening
    ├── KASLR, KPTI
    ├── Stack canaries
    ├── Hardened usercopy
    └── Module signing
    
    Layer 3: Access Control
    ├── SELinux/AppArmor
    ├── Capabilities
    └── Namespaces
    
    Layer 4: Runtime Monitoring
    ├── Audit system
    ├── IMA/EVM
    └── Security event logging
    
    Layer 5: Incident Response
    ├── Log aggregation
    ├── SIEM integration
    └── Forensic readiness

**Embedded Systems Specific**:

✅ **Enable**:
   - Module signature enforcement
   - Kernel lockdown (integrity mode minimum)
   - Disable unnecessary syscalls (seccomp)
   - Read-only root filesystem

✅ **Disable**:
   - /dev/mem, /dev/kmem
   - Kernel module loading after boot
   - kexec (unless needed for updates)
   - User namespaces (if not using containers)

================================================================================
Section 8: Key Takeaways
================================================================================

**Debugging Tools**:
✓ **ftrace**: Built-in, low overhead, function/latency tracing, stable API (tracepoints)
✓ **perf**: CPU profiling, hardware counters, flamegraphs, syscall tracing
✓ **eBPF/bpftrace**: Programmable tracing, kernel+user, custom logic, production-safe
✓ **KGDB**: Breakpoint debugging, source-level, post-boot kernel
✓ **JTAG**: Hardware debugger, early boot, unlimited breakpoints, most reliable

**Tool Selection**:
✓ Quick insight → bpftrace one-liner
✓ CPU profiling → perf record/report/flamegraph
✓ Function call flow → ftrace function_graph
✓ Latency analysis → ftrace irqsoff/wakeup
✓ Breakpoint debugging → KGDB (or JTAG for early boot)
✓ Production monitoring → eBPF (lowest overhead)

**Security Architecture**:
✓ **Audit system**: Who did what, when (compliance, forensics)
✓ **Secure boot**: Verify boot chain integrity (UEFI → bootloader → kernel → modules)
✓ **Kernel lockdown**: Prevent runtime kernel modification
✓ **Module signing**: Only load trusted code
✓ **Hardening**: KASLR, KPTI, stack canaries, fortify source
✓ **LSM**: SELinux/AppArmor for mandatory access control

**Best Practices**:
✓ Always filter/limit scope to reduce overhead
✓ Use stable APIs (tracepoints) over unstable (kprobes)
✓ Start with low-overhead tools, escalate if needed
✓ Collect context (timestamps, PIDs, stacks) for correlation
✓ Flamegraphs for CPU profiling visualization
✓ Defense in depth for security (multiple layers)
✓ Audit security-relevant events with meaningful keys
✓ Test debug infrastructure before you need it

**Common Patterns**:
✓ High latency → ftrace irqsoff + perf + bpftrace latency histogram
✓ CPU hotspot → perf record + flamegraph
✓ Memory leak → /proc/slabinfo + BCC memleak
✓ Kernel panic → kdump + crash utility (or JTAG/KGDB)
✓ Security incident → audit logs + ausearch + aureport
✓ Driver bug → KGDB + breakpoints + structure examination

**Modern Trends (2026)**:
✓ eBPF everywhere: networking, tracing, security, observability
✓ BTF (BPF Type Format): portable eBPF programs across kernel versions
✓ Confidential computing: kernel lockdown confidentiality mode
✓ Runtime integrity: IMA + EVM for file/executable verification
✓ Continuous auditing: Real-time security event streaming to SIEM
✓ Supply chain security: SBOM + signed artifacts

================================================================================
References
================================================================================

**ftrace**:
- Documentation/trace/ftrace.rst
- trace-cmd: https://trace-cmd.org
- KernelShark: https://kernelshark.org

**perf**:
- https://perf.wiki.kernel.org
- Brendan Gregg's site: https://www.brendangregg.com/perf.html
- FlameGraph: https://github.com/brendangregg/FlameGraph

**eBPF/bpftrace**:
- https://ebpf.io
- bpftrace: https://github.com/iovisor/bpftrace
- BCC: https://github.com/iovisor/bcc
- Cilium (eBPF networking): https://cilium.io

**KGDB/JTAG**:
- Documentation/dev-tools/kgdb.rst
- OpenOCD: https://openocd.org
- GDB manual: https://sourceware.org/gdb/documentation

**Audit**:
- Documentation/admin-guide/audit.rst
- aureport man pages
- Red Hat Audit Guide

**Security**:
- kernel.org/doc/html/latest/admin-guide/LSM/
- Kernel Self Protection Project: https://kernsec.org/wiki/index.php/Kernel_Self_Protection_Project

**Books**:
- "BPF Performance Tools" - Brendan Gregg
- "Systems Performance" - Brendan Gregg
- "Linux Kernel Debugging" - Christophe Blaess
- "Professional Linux Kernel Architecture" - Wolfgang Mauerer

================================================================================
End of Document
================================================================================

