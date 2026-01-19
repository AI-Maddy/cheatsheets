===================================
Linux Latency Analysis Guide
===================================

:Author: Embedded Linux Documentation
:Date: January 2026
:Version: 1.0
:Focus: Measuring, analyzing, and minimizing system latency

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Latency Tools
-----------------------

.. code-block:: bash

   # cyclictest - Primary latency measurement tool
   sudo cyclictest -t 4 -p 80 -n -m -l 100000
   
   # hwlatdetect - Hardware latency detection
   sudo hwlatdetect --duration=60
   
   # ftrace - Kernel function tracing
   sudo trace-cmd record -p function_graph -g do_IRQ
   sudo trace-cmd report
   
   # perf - Performance analysis
   sudo perf record -a -g sleep 10
   sudo perf report
   
   # Check latency sources
   cat /proc/interrupts
   cat /proc/softirqs
   vmstat 1

Quick Latency Test
-------------------

.. code-block:: bash

   #!/bin/bash
   # Quick latency benchmark
   
   echo "Starting latency test..."
   
   # Run cyclictest for 1 minute
   sudo cyclictest -t $(nproc) -p 95 -n -m -l 60000 -q
   
   # Check for hardware latencies
   sudo hwlatdetect --duration=60 --threshold=10
   
   # Check interrupt distribution
   cat /proc/interrupts | head -20

Understanding Latency
=====================

Types of Latency
----------------

.. code-block:: text

   1. Interrupt Latency:
      - Time from interrupt to handler execution
      - Typically 1-10 μs on modern systems
      - Critical for real-time response
   
   2. Scheduling Latency:
      - Time from wakeup to actual execution
      - Depends on scheduler and priority
      - RT kernel: 10-50 μs typical
   
   3. Dispatch Latency:
      - Time to switch context to RT task
      - Includes interrupt + scheduling latency
      - Total: 20-100 μs (RT kernel)
   
   4. Hardware Latency:
      - SMI (System Management Interrupt)
      - Power management transitions
      - Can be 100+ μs, very problematic
   
   5. Application Latency:
      - End-to-end response time
      - Includes all above + processing time
      - Varies widely by application

Latency Budget
--------------

.. code-block:: text

   Example 1ms latency budget:
   
   Hardware/SMI:           50 μs (5%)
   Interrupt handling:     100 μs (10%)
   Context switch:         50 μs (5%)
   Kernel overhead:        100 μs (10%)
   Application processing: 700 μs (70%)
   -------------------------------
   Total:                  1000 μs (100%)
   
   Goal: Keep overhead <30% of budget

cyclictest - Latency Measurement
=================================

Basic Usage
-----------

.. code-block:: bash

   # Install rt-tests
   sudo apt install rt-tests
   
   # Basic test (1 thread, priority 80, 10000 iterations)
   sudo cyclictest -t 1 -p 80 -n -l 10000
   
   # Output explanation:
   # T: 0 ( 1234) P:80 I:1000 C: 10000 Min:   5 Act:   8 Avg:  10 Max:  45
   # T:0       - Thread 0
   # (1234)    - Thread PID
   # P:80      - Priority
   # I:1000    - Interval (μs)
   # C:10000   - Count (iterations)
   # Min:5     - Minimum latency (μs)
   # Act:8     - Actual latency (μs)
   # Avg:10    - Average latency (μs)
   # Max:45    - Maximum latency (μs) - MOST IMPORTANT!

Advanced Options
----------------

.. code-block:: bash

   # Multiple threads (one per CPU)
   sudo cyclictest -t $(nproc) -p 80 -n -m -l 100000
   
   # Options explained:
   # -t N      : Number of threads
   # -p N      : Real-time priority (1-99)
   # -n        : Use clock_nanosleep (more accurate)
   # -m        : Lock memory (mlockall)
   # -l N      : Number of loops/iterations
   # -a N      : CPU affinity (comma-separated)
   # -i N      : Interval (default 1000μs)
   # -h N      : Histogram buckets
   # -q        : Quiet mode (summary only)
   # -D N      : Duration in seconds
   
   # With CPU affinity
   sudo cyclictest -t 4 -a 0,1,2,3 -p 80 -n -m -l 100000
   
   # With histogram
   sudo cyclictest -t 4 -p 80 -n -m -l 100000 -h 200 -q
   
   # Long duration test (1 hour)
   sudo cyclictest -t 4 -p 80 -n -m -D 3600

Interpreting Results
--------------------

.. code-block:: text

   Good RT System:
   - Max latency: <100 μs (excellent)
   - Max latency: <200 μs (good)
   - Max latency: <500 μs (acceptable)
   - Max latency: >1000 μs (poor, investigate)
   
   What to look for:
   1. Consistent low max latency across all threads
   2. No outliers (occasional huge spikes)
   3. Histogram shows tight distribution
   4. Results stable over long duration
   
   Example output analysis:
   T: 0 ( 1234) P:80 I:1000 C:100000 Min:  4 Act:  7 Avg:  8 Max:  35
   T: 1 ( 1235) P:80 I:1000 C:100000 Min:  4 Act:  8 Avg:  8 Max:  38
   T: 2 ( 1236) P:80 I:1000 C:100000 Min:  5 Act:  9 Avg:  9 Max: 452  ← Problem!
   T: 3 ( 1237) P:80 I:1000 C:100000 Min:  4 Act:  7 Avg:  8 Max:  36
   
   Thread 2 has outlier (452 μs) - investigate CPU 2

Stress Testing
--------------

.. code-block:: bash

   # Test with system under load
   # Terminal 1: Start stress
   stress-ng --cpu $(nproc) --io 4 --vm 2 --vm-bytes 128M --timeout 300s
   
   # Terminal 2: Run cyclictest
   sudo cyclictest -t $(nproc) -p 95 -n -m -l 100000
   
   # Or combined
   sudo cyclictest -t 4 -p 95 -n -m -l 100000 & \
   stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 64M --timeout 60s
   
   # Disk I/O stress
   sudo cyclictest -t 4 -p 95 -n -m -l 100000 & \
   dd if=/dev/zero of=/tmp/testfile bs=1M count=10000

Histogram Analysis
------------------

.. code-block:: bash

   # Generate histogram
   sudo cyclictest -t 4 -p 80 -n -m -l 100000 -h 100 -q > latency.hist
   
   # Plot histogram (requires gnuplot)
   gnuplot <<EOF
   set terminal png size 800,600
   set output 'latency.png'
   set title 'Latency Histogram'
   set xlabel 'Latency (μs)'
   set ylabel 'Count'
   plot 'latency.hist' using 1:2 with lines title 'Thread 0'
   EOF

Hardware Latency Detection
===========================

hwlatdetect
-----------

.. code-block:: bash

   # Install
   sudo apt install rt-tests
   
   # Basic detection (60 seconds)
   sudo hwlatdetect --duration=60
   
   # With threshold (report only >10μs)
   sudo hwlatdetect --duration=60 --threshold=10
   
   # Specific CPU
   sudo hwlatdetect --duration=60 --cpu=2
   
   # Output interpretation:
   # hwlatdetect:  test duration 60 seconds
   #    detector: tracer
   #    parameters:
   #         Latency threshold: 10us
   #         Sample window:     1000000us
   #         Sample width:      500000us
   #    Max Latency: 142us  ← SMI or hardware issue!
   #    Samples: 120
   #    Samples exceeding threshold: 3

SMI Latency
-----------

.. code-block:: bash

   # SMI (System Management Interrupt) causes non-maskable latency
   # Common sources:
   # - BIOS/UEFI updates
   # - Thermal management
   # - Fan control
   # - Battery management
   
   # Check SMI count
   sudo cat /sys/firmware/acpi/interrupts/sci
   
   # Disable SMI in BIOS (if possible):
   # - Disable C-states beyond C1
   # - Disable P-states (CPU frequency scaling)
   # - Disable thermal management
   # - Update BIOS to latest version
   
   # Kernel command line to reduce SMI:
   # idle=poll processor.max_cstate=0 intel_pstate=disable

ftrace - Function Tracing
==========================

Basic Function Tracing
-----------------------

.. code-block:: bash

   # Enable function tracer
   echo function > /sys/kernel/debug/tracing/current_tracer
   
   # Start tracing
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # Stop tracing
   echo 0 > /sys/kernel/debug/tracing/tracing_on
   
   # View trace
   cat /sys/kernel/debug/tracing/trace | head -50
   
   # Clear trace
   echo > /sys/kernel/debug/tracing/trace

Function Graph Tracer
---------------------

.. code-block:: bash

   # Shows function call hierarchy with timing
   echo function_graph > /sys/kernel/debug/tracing/current_tracer
   
   # Trace specific function
   echo do_IRQ > /sys/kernel/debug/tracing/set_graph_function
   
   # Set depth limit
   echo 5 > /sys/kernel/debug/tracing/max_graph_depth
   
   # Start tracing
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   
   # Generate activity
   sleep 1
   
   # Stop and view
   echo 0 > /sys/kernel/debug/tracing/tracing_on
   cat /sys/kernel/debug/tracing/trace

Latency Tracers
---------------

.. code-block:: bash

   # Interrupt off tracer (irqsoff)
   echo irqsoff > /sys/kernel/debug/tracing/current_tracer
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   sleep 10
   echo 0 > /sys/kernel/debug/tracing/tracing_on
   cat /sys/kernel/debug/tracing/trace
   
   # Preemption off tracer (preemptoff)
   echo preemptoff > /sys/kernel/debug/tracing/current_tracer
   
   # Combined (preemptirqsoff)
   echo preemptirqsoff > /sys/kernel/debug/tracing/current_tracer
   
   # Wake-up latency tracer
   echo wakeup > /sys/kernel/debug/tracing/current_tracer
   echo wakeup_rt > /sys/kernel/debug/tracing/current_tracer  # RT tasks only

trace-cmd
---------

.. code-block:: bash

   # Install
   sudo apt install trace-cmd
   
   # Record function trace
   sudo trace-cmd record -p function -l do_IRQ
   
   # Record scheduler events
   sudo trace-cmd record -e sched_switch -e sched_wakeup
   
   # Record with filtering
   sudo trace-cmd record -e 'sched:*' -f 'prev_comm == "myapp"'
   
   # Record all events for 10 seconds
   sudo trace-cmd record -e all sleep 10
   
   # View trace
   sudo trace-cmd report
   
   # Generate flamegraph
   sudo trace-cmd record -p function_graph -g schedule
   sudo trace-cmd report | flamegraph.pl > flamegraph.svg

Event Tracing
-------------

.. code-block:: bash

   # List available events
   cat /sys/kernel/debug/tracing/available_events
   
   # Enable specific event
   echo 1 > /sys/kernel/debug/tracing/events/sched/sched_switch/enable
   echo 1 > /sys/kernel/debug/tracing/events/irq/irq_handler_entry/enable
   
   # Enable all scheduler events
   echo 1 > /sys/kernel/debug/tracing/events/sched/enable
   
   # Filter events
   echo 'irq == 16' > /sys/kernel/debug/tracing/events/irq/irq_handler_entry/filter

perf - Performance Analysis
============================

Basic Usage
-----------

.. code-block:: bash

   # Install
   sudo apt install linux-tools-generic
   
   # Record system-wide for 10 seconds
   sudo perf record -a -g sleep 10
   
   # Record specific process
   sudo perf record -p 1234 -g
   
   # Record with high frequency
   sudo perf record -a -F 1000 -g sleep 10
   
   # View report
   sudo perf report
   
   # Interactive TUI
   sudo perf report --tui

Latency Analysis with perf
---------------------------

.. code-block:: bash

   # Scheduler latency
   sudo perf sched record sleep 10
   sudo perf sched latency
   
   # Show per-task latency
   sudo perf sched latency --sort max
   
   # Timechart visualization
   sudo perf sched timechart
   
   # Lock contention
   sudo perf lock record sleep 10
   sudo perf lock report

Context Switches
----------------

.. code-block:: bash

   # Count context switches
   sudo perf stat -e context-switches -a sleep 10
   
   # Detailed context switch analysis
   sudo perf record -e sched:sched_switch -a sleep 10
   sudo perf report

Cache Misses
------------

.. code-block:: bash

   # CPU cache statistics
   sudo perf stat -e cache-misses,cache-references -a sleep 10
   
   # L1, L2, L3 cache events
   sudo perf stat -e L1-dcache-load-misses,L1-dcache-loads \
                   -e LLC-load-misses,LLC-loads -a sleep 10

Interrupt Analysis
==================

Viewing Interrupts
------------------

.. code-block:: bash

   # Current interrupt counts
   cat /proc/interrupts
   
   # Example output:
   #            CPU0       CPU1       CPU2       CPU3
   #   0:         24          0          0          0  IO-APIC   2-edge      timer
   #   8:          0          0          0          1  IO-APIC   8-edge      rtc0
   #  16:      12345      23456      34567      45678  IO-APIC  16-fasteoi   ehci_hcd
   
   # Monitor interrupt rate
   watch -n 1 cat /proc/interrupts
   
   # Soft IRQs
   cat /proc/softirqs

IRQ Affinity
------------

.. code-block:: bash

   # View IRQ affinity
   cat /proc/irq/16/smp_affinity
   # Output: ff (all CPUs)
   
   # Set IRQ to CPU 0 only
   echo 1 > /proc/irq/16/smp_affinity
   
   # Set to CPUs 0-1 (binary: 0011)
   echo 3 > /proc/irq/16/smp_affinity
   
   # Set to CPUs 2-3 (binary: 1100)
   echo c > /proc/irq/16/smp_affinity
   
   # Move all IRQs away from CPU 2-3 (RT CPUs)
   for irq in /proc/irq/*/smp_affinity; do
       echo 3 > $irq  # CPUs 0-1
   done

IRQ Threading
-------------

.. code-block:: bash

   # Check if IRQ is threaded
   ps aux | grep "\[irq/"
   
   # Example output:
   # root        12  ...  [irq/16-ehci_hcd]
   
   # Force IRQ to be threaded
   echo 1 > /proc/irq/16/threaded
   
   # Set IRQ thread priority
   chrt -f -p 90 $(pgrep "irq/16")
   
   # View IRQ thread priorities
   ps -eLo pid,class,rtprio,cmd | grep "\[irq/"

Latency Reduction Techniques
=============================

Kernel Configuration
--------------------

.. code-block:: bash

   # Essential kernel config for low latency:
   CONFIG_PREEMPT_RT=y               # PREEMPT_RT patch
   CONFIG_NO_HZ_FULL=y               # Tickless kernel
   CONFIG_HIGH_RES_TIMERS=y          # High-resolution timers
   CONFIG_HZ_1000=y                  # 1000Hz timer
   CONFIG_RCU_BOOST=y                # RCU priority boosting
   
   # Disable for lower latency:
   # CONFIG_CPU_FREQ is not set      # CPU frequency scaling
   # CONFIG_CPU_IDLE is not set      # CPU idle states

Kernel Command Line
-------------------

.. code-block:: bash

   # /etc/default/grub - GRUB_CMDLINE_LINUX
   
   # CPU isolation
   isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3
   
   # Disable CPU idle
   idle=poll
   # or limit C-states
   processor.max_cstate=1 intel_idle.max_cstate=0
   
   # Disable CPU frequency scaling
   intel_pstate=disable
   
   # Disable watchdog
   nowatchdog
   
   # Disable auditing
   audit=0
   
   # Complete example:
   GRUB_CMDLINE_LINUX="isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3 idle=poll intel_pstate=disable nowatchdog audit=0"

System Tuning
-------------

.. code-block:: bash

   # Disable CPU frequency scaling
   for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
       echo performance > $cpu
   done
   
   # Disable CPU idle (C-states)
   for cpu in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
       echo 1 > $cpu
   done
   
   # Disable swap
   swapoff -a
   
   # Disable transparent huge pages
   echo never > /sys/kernel/mm/transparent_hugepage/enabled
   
   # Set I/O scheduler to deadline (lower latency)
   echo deadline > /sys/block/sda/queue/scheduler

Application Best Practices
---------------------------

.. code-block:: c

   // 1. Lock memory
   mlockall(MCL_CURRENT | MCL_FUTURE);
   
   // 2. Pre-fault stack
   unsigned char dummy[STACK_SIZE];
   memset(dummy, 0, STACK_SIZE);
   
   // 3. Set CPU affinity
   cpu_set_t cpuset;
   CPU_ZERO(&cpuset);
   CPU_SET(2, &cpuset);
   sched_setaffinity(0, sizeof(cpuset), &cpuset);
   
   // 4. Set RT priority
   struct sched_param param;
   param.sched_priority = 80;
   sched_setscheduler(0, SCHED_FIFO, &param);
   
   // 5. Use RT-safe sleep
   struct timespec ts = {0, 1000000};  // 1ms
   clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, NULL);
   
   // 6. Pre-allocate resources
   // NO malloc/free in RT path!
   
   // 7. Minimize system calls
   // Direct register access where possible

Latency Debugging Checklist
============================

.. code-block:: bash

   #!/bin/bash
   # Latency debugging script
   
   echo "=== System Latency Analysis ==="
   
   echo -e "\n1. Kernel Version:"
   uname -a
   
   echo -e "\n2. PREEMPT_RT Status:"
   uname -v | grep PREEMPT_RT && echo "RT kernel" || echo "Non-RT kernel"
   
   echo -e "\n3. CPU Frequency Scaling:"
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "Disabled"
   
   echo -e "\n4. CPU Idle States:"
   cat /sys/devices/system/cpu/cpu0/cpuidle/state*/disable 2>/dev/null || echo "Unknown"
   
   echo -e "\n5. Isolated CPUs:"
   cat /sys/devices/system/cpu/isolated
   
   echo -e "\n6. High-Resolution Timers:"
   cat /proc/timer_list | grep -i "hres_active" | head -1
   
   echo -e "\n7. RT Processes:"
   ps -eLo pid,class,rtprio,cmd | grep -E "FF|RR" | head -10
   
   echo -e "\n8. Recent Max Latency (cyclictest):"
   timeout 30 cyclictest -t 1 -p 80 -n -q | grep "Max:"
   
   echo -e "\n9. Hardware Latency:"
   timeout 30 hwlatdetect --threshold=10 2>/dev/null | grep "Max Latency"
   
   echo -e "\n10. Top Interrupt Sources:"
   cat /proc/interrupts | head -20

Best Practices
==============

1. **Measure first** - establish baseline with cyclictest
2. **Identify sources** - use ftrace and perf to find bottlenecks
3. **Isolate CPUs** - dedicate cores for RT workload
4. **Disable power mgmt** - consistent performance over power saving
5. **Test under stress** - verify latency with system load
6. **Monitor continuously** - production latency monitoring
7. **Document changes** - track what affects latency
8. **Set realistic goals** - <100μs excellent, <1ms often sufficient

Common Pitfalls
===============

1. **SMI latencies** - check hwlatdetect, update BIOS
2. **CPU frequency scaling** - causes variable latency
3. **C-states** - deep sleep causes wakeup latency
4. **Unbalanced IRQs** - all on one CPU
5. **Page faults** - not locking memory
6. **Thermal throttling** - CPU slows down under heat
7. **NUMA effects** - memory access latency varies

Quick Reference
===============

.. code-block:: bash

   # Primary latency test
   sudo cyclictest -t 4 -p 80 -n -m -l 100000
   
   # Hardware latency
   sudo hwlatdetect --duration=60
   
   # Trace latency
   sudo trace-cmd record -e irq -e sched
   
   # Performance analysis
   sudo perf sched latency
   
   # Check configuration
   uname -a | grep PREEMPT_RT
   cat /proc/sys/kernel/sched_rt_runtime_us

See Also
========

- Linux_Realtime_PREEMPT_RT.rst
- Linux_Realtime_Scheduling.rst
- Linux_Realtime_Best_Practices.rst

References
==========

- man cyclictest
- man trace-cmd
- man perf
- https://rt.wiki.kernel.org/
- https://www.kernel.org/doc/html/latest/trace/ftrace.html
