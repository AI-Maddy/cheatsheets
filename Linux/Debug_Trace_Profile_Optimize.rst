======================================================
Linux Embedded Systems - Debug, Trace, Profile, Optimize
======================================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Experience: Multi-platform embedded debugging and optimization

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========

Comprehensive guide to debugging, tracing, profiling, and optimizing embedded Linux systems, covering JTAG debugging, kernel tracing, performance analysis, power profiling, boot time optimization, and memory optimization based on real project experience.

Hardware Debugging
==================

JTAG/SWD Debugging
------------------

**OpenOCD Configuration:**

.. code-block:: bash

   # openocd.cfg for i.MX 93
   source [find interface/jlink.cfg]
   
   # Target configuration
   adapter speed 10000
   
   transport select swd
   
   # Cortex-A55 cores
   set _CHIPNAME imx93
   set _ENDIAN little
   set _CPUTAPID 0x6ba02477
   
   # Create SWD target
   swd newdap $_CHIPNAME cpu -irlen 4 -ircapture 0x1 -irmask 0xf \
       -expected-id $_CPUTAPID
   
   dap create $_CHIPNAME.dap -chain-position $_CHIPNAME.cpu
   
   # Cortex-A55 core 0
   set _TARGETNAME $_CHIPNAME.a55.0
   target create $_TARGETNAME cortex_a -dap $_CHIPNAME.dap \
       -coreid 0 -dbgbase 0x90410000
   
   # Cortex-A55 core 1
   set _TARGETNAME $_CHIPNAME.a55.1
   target create $_TARGETNAME cortex_a -dap $_CHIPNAME.dap \
       -coreid 1 -dbgbase 0x90510000
   
   # Cortex-M33
   set _TARGETNAME $_CHIPNAME.m33
   target create $_TARGETNAME cortex_m -dap $_CHIPNAME.dap \
       -ap-num 2 -coreid 2
   
   # Reset configuration
   $_CHIPNAME.a55.0 configure -event reset-assert-pre {
       adapter assert srst
   }

**OpenOCD Usage:**

.. code-block:: bash

   # Start OpenOCD
   openocd -f openocd.cfg
   
   # In another terminal, connect with telnet
   telnet localhost 4444
   
   # OpenOCD commands
   > targets  # List all targets
   > halt     # Halt CPU
   > reg      # Display registers
   > mdw 0x80000000 256  # Memory dump (256 words)
   > mww 0x80000000 0x12345678  # Memory write
   
   # Load and run U-Boot
   > load_image u-boot-spl.bin 0x2020_0000
   > resume 0x2020_0000
   
   # Set breakpoint
   > bp 0x80100000 4 hw
   
   # Single step
   > step

**GDB with OpenOCD:**

.. code-block:: bash

   # Connect GDB to OpenOCD
   arm-linux-gnueabihf-gdb vmlinux
   
   (gdb) target extended-remote localhost:3333
   (gdb) monitor reset halt
   (gdb) load
   (gdb) continue
   
   # Debug kernel
   (gdb) b start_kernel
   (gdb) c
   (gdb) bt  # Backtrace
   (gdb) info threads
   (gdb) thread 2
   (gdb) frame 0
   
   # Examine memory
   (gdb) x/32x 0x80000000
   
   # Watch variable
   (gdb) watch my_variable
   
   # Python scripts for kernel debugging
   (gdb) source scripts/gdb/vmlinux-gdb.py
   (gdb) lx-dmesg
   (gdb) lx-lsmod

**Early Boot Debugging:**

.. code-block:: bash

   # Kernel command line for early debug
   earlyprintk=serial,ttyS0,115200 earlycon=uart8250,mmio32,0x30860000
   
   # Enable early printk in kernel config
   CONFIG_EARLY_PRINTK=y
   CONFIG_DEBUG_LL=y
   CONFIG_DEBUG_LL_UART_8250=y

Kernel Debugging
================

KGDB (Kernel GDB)
-----------------

**Kernel Configuration:**

.. code-block:: bash

   CONFIG_KGDB=y
   CONFIG_KGDB_SERIAL_CONSOLE=y
   CONFIG_KGDB_KDB=y
   CONFIG_DEBUG_INFO=y
   CONFIG_DEBUG_INFO_DWARF4=y
   CONFIG_FRAME_POINTER=y

**Boot with KGDB:**

.. code-block:: bash

   # Kernel command line
   kgdboc=ttyS0,115200 kgdbwait
   
   # On host (debugger)
   arm-linux-gnueabihf-gdb vmlinux
   (gdb) target remote /dev/ttyUSB0
   (gdb) set remote interrupt-sequence Ctrl-C
   
   # Continue kernel boot
   (gdb) c
   
   # Break in (Ctrl-C on serial console)
   # Or trigger from kernel: kgdb_breakpoint();

**KDB Commands:**

.. code-block:: bash

   # Enter KDB with SysRq
   echo g > /proc/sysrq-trigger
   
   # KDB commands
   kdb> help
   kdb> ps          # Process list
   kdb> bt          # Backtrace
   kdb> md 0xc0000000 100  # Memory dump
   kdb> mm 0xc0000000 0x12345678  # Memory modify
   kdb> lsmod       # List modules
   kdb> dmesg       # Kernel log
   kdb> go          # Continue

Dynamic Debug
-------------

**Enable Dynamic Debug:**

.. code-block:: bash

   CONFIG_DYNAMIC_DEBUG=y
   
   # Enable debug for specific file
   echo "file drivers/video/vpfe.c +p" > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific function
   echo "func vpfe_probe +p" > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug by module
   echo "module flexcan +p" > /sys/kernel/debug/dynamic_debug/control
   
   # Query current settings
   cat /sys/kernel/debug/dynamic_debug/control
   
   # In code:
   pr_debug("Debug message: value=%d\n", value);
   dev_dbg(&pdev->dev, "Device probe\n");

Kernel Tracing
==============

Ftrace
------

**Function Tracer:**

.. code-block:: bash

   # Enable ftrace
   CONFIG_FTRACE=y
   CONFIG_FUNCTION_TRACER=y
   CONFIG_FUNCTION_GRAPH_TRACER=y
   CONFIG_STACK_TRACER=y
   
   cd /sys/kernel/debug/tracing
   
   # List available tracers
   cat available_tracers
   # function function_graph blk wakeup ...
   
   # Enable function tracer
   echo function > current_tracer
   
   # Filter specific function
   echo "vpfe_*" > set_ftrace_filter
   echo "!vpfe_interrupt" >> set_ftrace_filter  # Exclude
   
   # Enable tracing
   echo 1 > tracing_on
   
   # View trace
   cat trace | less
   
   # Disable tracing
   echo 0 > tracing_on
   
   # Function graph tracer
   echo function_graph > current_tracer
   echo vpfe_probe > set_graph_function
   echo 1 > tracing_on
   cat trace

**Trace Events:**

.. code-block:: bash

   # List available events
   cat available_events | grep sched
   
   # Enable specific event
   echo 1 > events/sched/sched_switch/enable
   echo 1 > events/irq/irq_handler_entry/enable
   
   # Enable all events in subsystem
   echo 1 > events/net/enable
   
   # Filter events
   echo 'pid == 1234' > events/sched/sched_switch/filter
   
   # View trace
   cat trace_pipe  # Continuous output

**Custom Trace Points:**

.. code-block:: c

   // Add trace point in driver
   #include <trace/events/my_driver.h>
   
   // In my_driver.h
   TRACE_EVENT(vpfe_frame_captured,
       TP_PROTO(int frame_num, unsigned long timestamp),
       TP_ARGS(frame_num, timestamp),
       TP_STRUCT__entry(
           __field(int, frame_num)
           __field(unsigned long, timestamp)
       ),
       TP_fast_assign(
           __entry->frame_num = frame_num;
           __entry->timestamp = timestamp;
       ),
       TP_printk("frame=%d timestamp=%lu",
                 __entry->frame_num, __entry->timestamp)
   );
   
   // In driver code
   trace_vpfe_frame_captured(frame_number, jiffies);

Perf
----

**System-Wide Profiling:**

.. code-block:: bash

   # Record system activity
   perf record -a -g sleep 10
   
   # View report
   perf report
   
   # Record specific process
   perf record -p 1234 -g
   
   # Record with specific events
   perf record -e cycles,instructions,cache-misses -a
   
   # CPU profiling
   perf record -e cpu-clock -a -g -- sleep 30
   
   # Function profiling
   perf record -e block:block_rq_issue -a -g
   
   # Annotate source
   perf annotate

**Perf Stat:**

.. code-block:: bash

   # Performance counters
   perf stat ./my_application
   
   # Specific events
   perf stat -e cycles,instructions,cache-references,cache-misses ./app
   
   # System-wide
   perf stat -a sleep 10
   
   # Example output:
   #  Performance counter stats for 'system wide':
   #      10001.234567      task-clock (msec)
   #             1,234      context-switches
   #                45      cpu-migrations
   #           123,456      page-faults
   #     1,234,567,890      cycles
   #       987,654,321      instructions        # 0.80  insn per cycle
   #        12,345,678      cache-references
   #         1,234,567      cache-misses        # 10% of all cache refs

**Flame Graphs:**

.. code-block:: bash

   # Record with call graph
   perf record -F 99 -a -g -- sleep 60
   
   # Generate flame graph
   perf script | ./FlameGraph/stackcollapse-perf.pl | \
       ./FlameGraph/flamegraph.pl > flamegraph.svg

Memory Debugging
================

KASAN (Kernel Address Sanitizer)
---------------------------------

**Enable KASAN:**

.. code-block:: bash

   CONFIG_KASAN=y
   CONFIG_KASAN_INLINE=y
   CONFIG_SLUB_DEBUG=y
   
   # Kernel will detect:
   # - Out-of-bounds accesses
   # - Use-after-free
   # - Use-after-scope
   # - Double-free

**KASAN Output:**

.. code-block:: text

   BUG: KASAN: slab-out-of-bounds in my_driver_probe+0x123/0x456
   Write of size 4 at addr ffff888012345678 by task insmod/1234
   
   CPU: 0 PID: 1234 Comm: insmod Not tainted 5.15.0
   Call Trace:
    dump_stack+0x12/0x34
    kasan_report+0x56/0x78
    my_driver_probe+0x123/0x456

Memory Leak Detection
----------------------

**Kmemleak:**

.. code-block:: bash

   CONFIG_DEBUG_KMEMLEAK=y
   
   # Trigger scan
   echo scan > /sys/kernel/debug/kmemleak
   
   # View leaks
   cat /sys/kernel/debug/kmemleak
   
   # Clear
   echo clear > /sys/kernel/debug/kmemleak

**Valgrind for Userspace:**

.. code-block:: bash

   # Memory leak check
   valgrind --leak-check=full --show-leak-kinds=all ./my_app
   
   # Callgrind profiling
   valgrind --tool=callgrind ./my_app
   kcachegrind callgrind.out.12345

SLUB Debug
----------

.. code-block:: bash

   CONFIG_SLUB_DEBUG=y
   CONFIG_SLUB_DEBUG_ON=y
   
   # Boot parameter
   slub_debug=FZP
   # F = Consistency checks
   # Z = Red zoning
   # P = Poisoning
   
   # Per-cache debug
   slub_debug=F,kmalloc-512

Power Profiling
===============

PowerTOP
--------

.. code-block:: bash

   # Install powertop
   powertop --auto-tune
   
   # Interactive mode
   powertop
   
   # Generate HTML report
   powertop --html=power_report.html
   
   # Example output shows:
   # - CPU package power
   # - Wake-ups per second
   # - Top power consumers
   # - Device power states

Power Measurement
-----------------

**Project Example: DaVinci Hibernation (<8mW):**

.. code-block:: c

   // Measure power states
   #include <linux/pm.h>
   #include <linux/pm_runtime.h>
   
   static void measure_power_state(void)
   {
       unsigned long active_time, sleep_time;
       
       active_time = ktime_to_us(ktime_get()) - last_active;
       sleep_time = total_time - active_time;
       
       pr_info("Active: %lu us (%lu%%)\n", active_time,
               active_time * 100 / total_time);
       pr_info("Sleep: %lu us (%lu%%)\n", sleep_time,
               sleep_time * 100 / total_time);
   }

**Kernel Power States:**

.. code-block:: bash

   # Check C-states
   cat /sys/devices/system/cpu/cpu0/cpuidle/state*/name
   cat /sys/devices/system/cpu/cpu0/cpuidle/state*/power
   cat /sys/devices/system/cpu/cpu0/cpuidle/state*/time
   
   # Check P-states (frequency)
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
   
   # Runtime PM statistics
   cat /sys/devices/platform/*/power/runtime_status
   cat /sys/devices/platform/*/power/runtime_suspended_time

Boot Time Optimization
=======================

Measurement Tools
-----------------

**Bootchart:**

.. code-block:: bash

   # Kernel command line
   initcall_debug printk.time=y
   
   # Install bootchart
   apt-get install bootchart2 pybootchartgui
   
   # Add to init
   /sbin/bootchartd start
   
   # Generate chart
   pybootchartgui -f svg /var/log/bootchart.tgz

**systemd-analyze:**

.. code-block:: bash

   # Overall boot time
   systemd-analyze
   # Startup finished in 2.156s (kernel) + 5.432s (userspace) = 7.588s
   
   # Service breakdown
   systemd-analyze blame
   
   # Critical chain
   systemd-analyze critical-chain
   
   # Plot SVG
   systemd-analyze plot > boot.svg
   
   # Verify
   systemd-analyze verify myservice.service

**Kernel Boot Time Analysis:**

.. code-block:: bash

   # Enable initcall debug
   CONFIG_PRINTK_TIME=y
   CONFIG_INITCALL_DEBUG=y
   
   # Kernel command line
   initcall_debug
   
   # Parse dmesg
   dmesg | grep "initcall" | awk '{print $7, $4}' | sort -n -k2
   
   # Example output:
   # initcall_0x80123456 returned 0 after 1234 usecs
   # initcall_0x80abcdef returned 0 after 5678 usecs

Optimization Techniques
-----------------------

**1. Parallel Initialization:**

.. code-block:: c

   // Mark driver for async probing
   static struct platform_driver my_driver = {
       .probe = my_probe,
       .driver = {
           .name = "my-device",
           .probe_type = PROBE_PREFER_ASYNCHRONOUS,
       },
   };

**2. Deferred Initialization:**

.. code-block:: c

   // Use late_initcall for non-critical drivers
   late_initcall(my_driver_init);
   
   // Or defer to userspace
   static int __init my_driver_init(void)
   {
       if (fast_boot)
           return -EPROBE_DEFER;
       
       return real_init();
   }

**3. Reduce initramfs Size:**

.. code-block:: bash

   # Use compressed initramfs
   CONFIG_INITRAMFS_COMPRESSION_XZ=y
   
   # Minimal busybox config
   CONFIG_FEATURE_INSTALLER=n
   
   # Strip binaries
   strip --strip-all busybox

**Project Results (from experience):**

.. list-table:: Boot Time Optimization Results
   :header-rows: 1
   :widths: 30 20 20 30
   
   * - Platform
     - Before
     - After
     - Key Optimizations
   * - i.MX 93
     - 6.2s
     - 1.8s
     - Async probe, initramfs, parallel init
   * - TI DaVinci
     - 8.5s
     - 5.8s
     - Built-in drivers, U-Boot opt
   * - Intel Atom
     - 12.1s
     - 9.2s
     - UEFI tuning, systemd optimization

Memory Optimization
===================

Kernel Memory Analysis
----------------------

**SLUB Statistics:**

.. code-block:: bash

   # View memory usage by cache
   cat /proc/slabinfo
   
   # Top memory consumers
   sort -k3 -n -r /proc/slabinfo | head -20

**Page Allocation Tracking:**

.. code-block:: bash

   CONFIG_PAGE_OWNER=y
   
   # Boot parameter
   page_owner=on
   
   # Analyze allocations
   cat /sys/kernel/debug/page_owner > page_owner.txt
   
   # Parse with script
   ./scripts/page_owner_sort.py page_owner.txt

**Memory Fragmentation:**

.. code-block:: bash

   # Check fragmentation
   cat /proc/buddyinfo
   
   # Compact memory
   echo 1 > /proc/sys/vm/compact_memory

Reducing Memory Footprint
--------------------------

**1. Kernel Configuration:**

.. code-block:: bash

   # Minimize kernel
   CONFIG_CC_OPTIMIZE_FOR_SIZE=y
   CONFIG_SLOB=y  # Simple allocator
   CONFIG_KERNEL_XZ=y  # Best compression
   
   # Remove debugging
   # CONFIG_DEBUG_KERNEL is not set
   # CONFIG_KALLSYMS is not set

**2. Application Optimization:**

.. code-block:: bash

   # Strip binaries
   strip --strip-all executable
   
   # Use shared libraries
   # Use musl instead of glibc (smaller)
   
   # Optimize compiler flags
   CFLAGS="-Os -ffunction-sections -fdata-sections"
   LDFLAGS="-Wl,--gc-sections"

**3. Memory Profiling:**

.. code-block:: bash

   # pmap for process memory
   pmap -x 1234
   
   # smem for system overview
   smem -r
   
   # /proc filesystem
   cat /proc/meminfo
   cat /proc/$PID/smaps
   cat /proc/$PID/status

Real-Time Performance
=====================

Latency Measurement
-------------------

**Cyclictest:**

.. code-block:: bash

   # Install rt-tests
   apt-get install rt-tests
   
   # Run cyclictest
   cyclictest -p 80 -t5 -n -i 10000 -l 10000
   
   # With histogram
   cyclictest -p 80 -t5 -n -i 10000 -l 10000 -h 100 -q
   
   # Example output:
   # T: 0 ( 1234) P:80 I:10000 C: 10000 Min:   8 Act:  12 Avg:  11 Max:  156

**Preempt-RT Kernel:**

.. code-block:: bash

   # Apply RT patches
   CONFIG_PREEMPT_RT=y
   CONFIG_HIGH_RES_TIMERS=y
   CONFIG_NO_HZ_FULL=y
   
   # Kernel command line
   isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3
   
   # Set RT priority
   chrt -f 80 ./my_rt_app

**IRQ Latency:**

.. code-block:: bash

   # hwlatdetect
   hwlatdetect --duration=60
   
   # Example output:
   # Max latency: 23 usec
   # Samples: 60000
   # CPU: 0

Trace-based Analysis
--------------------

**Latency Tracer:**

.. code-block:: bash

   cd /sys/kernel/debug/tracing
   
   # Enable latency tracer
   echo 0 > tracing_on
   echo wakeup_rt > current_tracer
   echo 1 > tracing_on
   
   # Generate load
   stress-ng --cpu 4 --timeout 60s
   
   # View worst case
   cat trace

Performance Tuning
==================

CPU Performance
---------------

**CPU Frequency Scaling:**

.. code-block:: bash

   # Set performance governor
   echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
   
   # Set specific frequency
   echo 1700000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed
   
   # Disable CPU idle
   for cpu in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
       echo 1 > $cpu
   done

**IRQ Affinity:**

.. code-block:: bash

   # Pin IRQ to specific CPU
   echo 2 > /proc/irq/45/smp_affinity  # CPU 1
   echo 4 > /proc/irq/46/smp_affinity  # CPU 2
   
   # Use irqbalance
   irqbalance --oneshot

I/O Performance
---------------

**Block Device:**

.. code-block:: bash

   # Check I/O scheduler
   cat /sys/block/sda/queue/scheduler
   
   # Set scheduler
   echo deadline > /sys/block/sda/queue/scheduler
   
   # Tune read-ahead
   blockdev --setra 8192 /dev/sda
   
   # iostat
   iostat -x 1

**Network:**

.. code-block:: bash

   # Ethtool optimization
   ethtool -G eth0 rx 4096 tx 4096
   ethtool -K eth0 gro on gso on tso on
   
   # TCP tuning
   sysctl -w net.core.rmem_max=16777216
   sysctl -w net.core.wmem_max=16777216
   sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
   sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"

Advanced Debugging Tools
========================

Kernel Oops Analysis
--------------------

.. code-block:: bash

   # Decode oops
   ./scripts/decode_stacktrace.sh vmlinux < oops.txt
   
   # addr2line
   addr2line -e vmlinux 0xc0123456
   
   # objdump
   objdump -dS vmlinux | less

Core Dumps
----------

.. code-block:: bash

   # Enable core dumps
   ulimit -c unlimited
   echo "/tmp/core-%e-%p-%t" > /proc/sys/kernel/core_pattern
   
   # Debug core dump
   gdb ./application core.12345
   (gdb) bt
   (gdb) frame 3
   (gdb) print variable

System Tap
----------

.. code-block:: bash

   # Install systemtap
   apt-get install systemtap systemtap-sdt-dev
   
   # Example: trace syscalls
   stap -e 'probe syscall.* { printf("%s\n", name) }'
   
   # Function tracing
   stap -e 'probe kernel.function("vpfe_probe") { 
       printf("Called from: %s\n", backtrace())
   }'

Best Practices
==============

General Guidelines
------------------

1. **Start with Measurement**
   - Always measure before optimizing
   - Use appropriate tools for each domain
   - Establish baseline metrics

2. **Systematic Approach**
   - Identify bottlenecks
   - Fix biggest issue first
   - Verify each change

3. **Documentation**
   - Document findings
   - Record optimization results
   - Maintain test procedures

4. **Regression Testing**
   - Automated testing
   - Performance benchmarks
   - Memory leak checks

Embedded-Specific Tips
-----------------------

1. **Boot Time**
   - Parallel initialization
   - Lazy loading
   - Minimal root filesystem

2. **Memory**
   - Shared libraries
   - Stripped binaries
   - Appropriate page sizes

3. **Power**
   - Runtime PM
   - CPU idle states
   - Clock gating

4. **Real-Time**
   - Kernel preemption
   - IRQ threading
   - CPU isolation

Tools Summary
=============

.. list-table:: Debug/Profile Tools Matrix
   :header-rows: 1
   :widths: 25 25 25 25
   
   * - Category
     - Tool
     - Use Case
     - Overhead
   * - Hardware Debug
     - OpenOCD/JTAG
     - Early boot, crashes
     - None (external)
   * - Kernel Debug
     - KGDB/KDB
     - Kernel debugging
     - High
   * - Tracing
     - ftrace
     - Function tracing
     - Low-Medium
   * - Profiling
     - perf
     - Performance analysis
     - Low
   * - Memory
     - KASAN
     - Memory errors
     - High
   * - Memory
     - Kmemleak
     - Memory leaks
     - Medium
   * - Power
     - PowerTOP
     - Power analysis
     - Low
   * - Boot
     - bootchart
     - Boot analysis
     - Low
   * - Real-Time
     - cyclictest
     - Latency measurement
     - Medium

References
==========

- Linux Kernel Debugging Guide
- ftrace Documentation
- perf Tutorial
- Embedded Linux Performance
- Real-Time Linux
- Kernel Profiling with perf

