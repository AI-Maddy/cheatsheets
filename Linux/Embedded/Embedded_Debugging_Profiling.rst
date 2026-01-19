================================================================================
Embedded Linux: Debugging & Profiling - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch11)
:Target: GDB, Profiling Tools, Trace Tools
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**GDB Cross-Debugging:**

.. code-block:: bash

   # On target (gdbserver)
   gdbserver :1234 ./myapp
   
   # On host (cross-gdb)
   arm-linux-gnueabi-gdb ./myapp
   (gdb) target remote 192.168.1.10:1234
   (gdb) break main
   (gdb) continue

**Core Dumps:**

.. code-block:: bash

   # Enable core dumps
   ulimit -c unlimited
   echo "/tmp/core.%e.%p" > /proc/sys/kernel/core_pattern
   
   # Analyze
   arm-linux-gnueabi-gdb ./myapp core.myapp.1234

**strace:**

.. code-block:: bash

   # Trace system calls
   strace ./myapp
   strace -p 1234                    # Attach to running
   strace -e open,read,write ./myapp # Specific syscalls
   strace -c ./myapp                 # Summary
   strace -tt -T ./myapp             # Timestamps + duration

**perf:**

.. code-block:: bash

   # Profile CPU
   perf record -g ./myapp
   perf report
   
   # System-wide
   perf top
   perf stat ./myapp
   
   # Events
   perf list
   perf record -e cpu-cycles,cache-misses ./myapp

**ftrace:**

.. code-block:: bash

   # Enable function tracing
   cd /sys/kernel/debug/tracing
   echo function > current_tracer
   echo 1 > tracing_on
   cat trace

================================================================================
1. GDB Debugging
================================================================================

1.1 GDB Basics
--------------

**Core Commands:**

.. code-block:: bash

   # Start GDB
   gdb ./myapp
   gdb ./myapp core
   
   # Run
   (gdb) run
   (gdb) run arg1 arg2
   (gdb) start              # Run and break at main
   
   # Breakpoints
   (gdb) break main
   (gdb) break file.c:123
   (gdb) break function
   (gdb) info breakpoints
   (gdb) delete 1           # Delete breakpoint 1
   (gdb) disable 1
   (gdb) enable 1
   
   # Execution control
   (gdb) continue           # Resume
   (gdb) next               # Step over
   (gdb) step               # Step into
   (gdb) finish             # Step out
   (gdb) until 123          # Run until line
   
   # Variables
   (gdb) print var
   (gdb) print/x var        # Hex
   (gdb) print *ptr
   (gdb) display var        # Auto-print
   (gdb) set var = 10
   
   # Stack
   (gdb) backtrace
   (gdb) bt full            # With locals
   (gdb) frame 2            # Switch frame
   (gdb) info locals
   (gdb) info args
   
   # Watchpoints
   (gdb) watch var          # Break on write
   (gdb) rwatch var         # Break on read
   (gdb) awatch var         # Break on access

1.2 Cross-Debugging with gdbserver
-----------------------------------

**Setup:**

.. code-block:: bash

   # On target: Start gdbserver
   gdbserver :1234 ./myapp
   gdbserver :1234 --attach 1234  # Attach to running
   gdbserver /dev/ttyS0 ./myapp   # Serial connection
   
   # On host: Setup environment
   source /path/to/sdk/environment-setup-*
   
   # Start cross-GDB
   arm-linux-gnueabi-gdb ./myapp
   
   # Connect
   (gdb) target remote 192.168.1.10:1234
   (gdb) target remote /dev/ttyUSB0
   
   # Set sysroot (for libraries)
   (gdb) set sysroot /path/to/sysroot
   
   # Debug
   (gdb) break main
   (gdb) continue

**GDB Commands File:**

.. code-block:: bash

   # Create .gdbinit or commands file
   cat > debug.gdb << 'EOF'
   target remote 192.168.1.10:1234
   set sysroot /opt/sysroot
   break main
   continue
   EOF
   
   # Run GDB with commands
   arm-linux-gnueabi-gdb -x debug.gdb ./myapp

1.3 Core Dump Analysis
-----------------------

**Enable Core Dumps:**

.. code-block:: bash

   # Set unlimited core size
   ulimit -c unlimited
   
   # Set core pattern
   echo "/tmp/core.%e.%p.%t" > /proc/sys/kernel/core_pattern
   # %e = executable name
   # %p = PID
   # %t = timestamp
   
   # Permanent (in /etc/security/limits.conf)
   * soft core unlimited
   * hard core unlimited
   
   # Or in systemd service
   [Service]
   LimitCORE=infinity

**Analyze Core Dump:**

.. code-block:: bash

   # Load core dump
   arm-linux-gnueabi-gdb ./myapp core.myapp.1234
   
   # Analyze
   (gdb) backtrace
   (gdb) info threads
   (gdb) thread 2           # Switch thread
   (gdb) frame 3
   (gdb) print var
   (gdb) info registers

================================================================================
2. System Call Tracing
================================================================================

2.1 strace
----------

**Basic Usage:**

.. code-block:: bash

   # Trace all system calls
   strace ./myapp
   
   # Attach to running process
   strace -p 1234
   
   # Trace specific syscalls
   strace -e open,read,write,close ./myapp
   strace -e trace=file ./myapp
   strace -e trace=network ./myapp
   strace -e trace=process ./myapp
   strace -e trace=signal ./myapp
   
   # Summary statistics
   strace -c ./myapp
   
   # Timestamps
   strace -t ./myapp        # Time of day
   strace -tt ./myapp       # Microseconds
   strace -ttt ./myapp      # Unix timestamp
   strace -T ./myapp        # Time spent in syscall
   
   # Output to file
   strace -o trace.txt ./myapp
   
   # Follow forks
   strace -f ./myapp
   
   # String length
   strace -s 128 ./myapp    # Show 128 chars (default 32)

**Common Patterns:**

.. code-block:: bash

   # Find what files app opens
   strace -e open,openat ./myapp 2>&1 | grep -v ENOENT
   
   # Network debugging
   strace -e trace=network -s 1024 ./myapp
   
   # Performance analysis
   strace -c -S calls ./myapp    # Sort by calls
   strace -c -S time ./myapp     # Sort by time
   
   # Attach to all threads
   strace -f -p 1234

2.2 ltrace
----------

**Library Call Tracing:**

.. code-block:: bash

   # Trace library calls
   ltrace ./myapp
   
   # Attach to process
   ltrace -p 1234
   
   # Specific functions
   ltrace -e malloc,free ./myapp
   ltrace -e @libc.so.6 ./myapp
   
   # Summary
   ltrace -c ./myapp
   
   # Combined with syscalls
   ltrace -S ./myapp
   
   # Timestamps
   ltrace -t ./myapp
   ltrace -tt ./myapp

================================================================================
3. Performance Profiling
================================================================================

3.1 perf
--------

**perf Installation:**

.. code-block:: bash

   # Kernel config
   CONFIG_PERF_EVENTS=y
   CONFIG_HW_PERF_EVENTS=y
   CONFIG_DEBUG_INFO=y
   
   # Build perf
   cd linux/tools/perf
   make
   make install

**perf Commands:**

.. code-block:: bash

   # List events
   perf list
   perf list hw
   perf list sw
   perf list cache
   
   # Record samples
   perf record ./myapp
   perf record -g ./myapp               # Call graph
   perf record -F 99 ./myapp            # 99 Hz sampling
   perf record -e cpu-cycles ./myapp
   perf record -e cache-misses ./myapp
   
   # System-wide
   perf record -a sleep 10              # Record all CPUs
   perf record -C 0 sleep 10            # CPU 0 only
   
   # Analyze
   perf report
   perf report --stdio
   perf report -g graph                 # Call graph
   
   # Real-time top
   perf top
   perf top -g
   
   # Statistics
   perf stat ./myapp
   perf stat -d ./myapp                 # Detailed
   perf stat -r 10 ./myapp              # 10 runs

**Advanced perf:**

.. code-block:: bash

   # Flame graphs
   perf record -g ./myapp
   perf script > out.perf
   ./FlameGraph/stackcollapse-perf.pl out.perf > out.folded
   ./FlameGraph/flamegraph.pl out.folded > flamegraph.svg
   
   # Differential profiling
   perf record -o before.data ./myapp
   # Make changes
   perf record -o after.data ./myapp
   perf diff before.data after.data
   
   # Annotate
   perf annotate function_name

3.2 gprof
---------

**GNU Profiler:**

.. code-block:: bash

   # Compile with profiling
   gcc -pg -o myapp myapp.c
   
   # Run (generates gmon.out)
   ./myapp
   
   # Analyze
   gprof myapp gmon.out
   gprof myapp gmon.out > analysis.txt
   
   # Call graph
   gprof -q myapp gmon.out
   
   # Flat profile
   gprof -p myapp gmon.out

3.3 valgrind
------------

**Memory Profiling:**

.. code-block:: bash

   # Memory leak detection
   valgrind --leak-check=full ./myapp
   valgrind --leak-check=full --show-reachable=yes ./myapp
   
   # Track origins
   valgrind --track-origins=yes ./myapp
   
   # Callgrind (call profiling)
   valgrind --tool=callgrind ./myapp
   callgrind_annotate callgrind.out.<pid>
   
   # Cachegrind (cache profiling)
   valgrind --tool=cachegrind ./myapp
   cg_annotate cachegrind.out.<pid>
   
   # Massif (heap profiling)
   valgrind --tool=massif ./myapp
   ms_print massif.out.<pid>

================================================================================
4. Kernel Tracing
================================================================================

4.1 ftrace
----------

**Function Tracer:**

.. code-block:: bash

   # ftrace location
   cd /sys/kernel/debug/tracing
   
   # List tracers
   cat available_tracers
   
   # Function tracer
   echo function > current_tracer
   echo 1 > tracing_on
   cat trace
   echo 0 > tracing_on
   
   # Function graph
   echo function_graph > current_tracer
   echo 1 > tracing_on
   cat trace
   
   # Filter functions
   echo "kfree*" > set_ftrace_filter
   echo "!kfree_skb" >> set_ftrace_filter  # Exclude
   cat set_ftrace_filter
   
   # Trace specific PID
   echo 1234 > set_ftrace_pid
   
   # Clear trace
   echo > trace

**Events:**

.. code-block:: bash

   # List events
   cat available_events
   ls events/
   
   # Enable event
   echo 1 > events/sched/sched_switch/enable
   echo 1 > events/irq/enable               # All IRQ events
   
   # Disable all
   echo 0 > events/enable
   
   # View trace
   cat trace
   cat trace_pipe  # Continuous

**trace-cmd:**

.. code-block:: bash

   # Easier ftrace interface
   trace-cmd record -p function_graph ./myapp
   trace-cmd record -e sched ./myapp
   trace-cmd report
   
   # Live tracing
   trace-cmd record -e all
   trace-cmd show

4.2 Dynamic Tracing
-------------------

**kprobes:**

.. code-block:: bash

   # Enable kprobe on function
   echo 'p:myprobe do_sys_open filename=+0(%si):string' > /sys/kernel/debug/tracing/kprobe_events
   echo 1 > /sys/kernel/debug/tracing/events/kprobes/myprobe/enable
   
   # View
   cat /sys/kernel/debug/tracing/trace
   
   # Disable
   echo 0 > /sys/kernel/debug/tracing/events/kprobes/myprobe/enable
   echo '-:myprobe' > /sys/kernel/debug/tracing/kprobe_events

**uprobes:**

.. code-block:: bash

   # Trace user-space function
   echo 'p:/usr/bin/myapp:0x1234' > /sys/kernel/debug/tracing/uprobe_events
   echo 1 > /sys/kernel/debug/tracing/events/uprobes/enable
   cat /sys/kernel/debug/tracing/trace

================================================================================
5. Specialized Tools
================================================================================

5.1 OProfile
------------

**System-Wide Profiler:**

.. code-block:: bash

   # Start profiling
   operf ./myapp
   operf -g ./myapp  # Call graph
   
   # System-wide
   operf -s
   
   # Report
   opreport
   opreport -l               # Per-symbol
   opreport --callgraph
   
   # Annotate
   opannotate --source ./myapp

5.2 LTTng
---------

**Low-Overhead Tracing:**

.. code-block:: bash

   # Create session
   lttng create my-session
   
   # Enable events
   lttng enable-event -k --all           # Kernel
   lttng enable-event -u --all           # User space
   lttng enable-event -k sched_switch
   
   # Start tracing
   lttng start
   
   # Run application
   ./myapp
   
   # Stop and destroy
   lttng stop
   lttng view
   lttng destroy
   
   # Analyze with babeltrace
   babeltrace ~/lttng-traces/my-session-*

5.3 SystemTap
-------------

**Scriptable Tracing:**

.. code-block:: bash

   # Simple script
   stap -e 'probe syscall.open { printf("%s: %s\n", execname(), filename) }'
   
   # Script file
   cat > trace.stp << 'EOF'
   probe kernel.function("do_sys_open") {
       printf("%s opened %s\n", execname(), kernel_string($filename))
   }
   EOF
   
   stap trace.stp
   
   # Function count
   stap -e 'global calls; probe kernel.function("*@net/socket.c") { calls[probefunc()]++ } probe end { foreach (f in calls-) printf("%s: %d\n", f, calls[f]) }'

================================================================================
6. Debugging Best Practices
================================================================================

6.1 Compilation Flags
----------------------

.. code-block:: bash

   # Debug build
   CFLAGS="-g -O0"                      # Full debug, no optimization
   CFLAGS="-g -Og"                      # Debug + some optimization
   CFLAGS="-g3"                         # Maximum debug info
   
   # Sanitizers
   CFLAGS="-fsanitize=address"          # Address sanitizer (ASan)
   CFLAGS="-fsanitize=thread"           # Thread sanitizer (TSan)
   CFLAGS="-fsanitize=undefined"        # UBSan
   CFLAGS="-fstack-protector-all"       # Stack protection

6.2 Logging
-----------

.. code-block:: c

   // Kernel debug
   #define pr_debug(fmt, ...) \
       printk(KERN_DEBUG pr_fmt(fmt), ##__VA_ARGS__)
   
   // Dynamic debug
   #define DEBUG
   pr_debug("Variable x = %d\n", x);
   
   // User space
   #define LOG(level, fmt, ...) \
       fprintf(stderr, "[%s] " fmt "\n", level, ##__VA_ARGS__)
   
   LOG("ERROR", "Failed to open %s", filename);

================================================================================
7. Key Takeaways
================================================================================

.. code-block:: text

   GDB:
   ====
   gdbserver :1234 ./myapp
   arm-linux-gdb ./myapp
   (gdb) target remote 192.168.1.10:1234
   (gdb) break main; continue
   
   strace:
   =======
   strace -e open,read,write ./myapp
   strace -tt -T -p 1234
   strace -c ./myapp
   
   perf:
   =====
   perf record -g ./myapp
   perf report
   perf top
   perf stat ./myapp
   
   ftrace:
   =======
   echo function > /sys/kernel/debug/tracing/current_tracer
   echo 1 > /sys/kernel/debug/tracing/tracing_on
   cat /sys/kernel/debug/tracing/trace
   
   Core Dumps:
   ===========
   ulimit -c unlimited
   arm-linux-gdb ./myapp core.<pid>

================================================================================
END OF CHEATSHEET
================================================================================
