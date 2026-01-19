===================================
Linux PREEMPT_RT Real-time Patch
===================================

:Author: Embedded Linux Documentation
:Date: January 2026
:Version: 1.0
:Focus: PREEMPT_RT real-time patch for Linux kernel

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Commands
------------------

.. code-block:: bash

   # Check if kernel is real-time
   uname -a | grep PREEMPT_RT
   
   # Check preemption model
   zcat /proc/config.gz | grep PREEMPT
   
   # Set real-time priority
   chrt -f 80 ./my_rt_app
   chrt -r 50 ./my_rt_app
   
   # Check thread priorities
   ps -eLo pid,tid,class,rtprio,pri,psr,comm | grep my_rt_app
   
   # Isolate CPUs for real-time
   # Add to kernel command line: isolcpus=2,3
   
   # Check latency
   cyclictest -t 4 -p 80 -n -m -l 10000

Quick PREEMPT_RT Installation
------------------------------

.. code-block:: bash

   #!/bin/bash
   # Build and install PREEMPT_RT kernel
   
   KERNEL_VERSION="6.1.70"
   RT_PATCH_VERSION="6.1.70-rt20"
   
   # Download kernel and RT patch
   wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KERNEL_VERSION}.tar.xz
   wget https://cdn.kernel.org/pub/linux/kernel/projects/rt/6.1/patch-${RT_PATCH_VERSION}.patch.xz
   
   # Extract and patch
   tar xf linux-${KERNEL_VERSION}.tar.xz
   cd linux-${KERNEL_VERSION}
   xzcat ../patch-${RT_PATCH_VERSION}.patch.xz | patch -p1
   
   # Configure for PREEMPT_RT
   make oldconfig
   # Select: Fully Preemptible Kernel (RT)
   
   # Build
   make -j$(nproc) deb-pkg LOCALVERSION=-rt
   
   # Install
   sudo dpkg -i ../linux-image-*.deb
   sudo dpkg -i ../linux-headers-*.deb
   
   # Reboot
   sudo reboot

What is PREEMPT_RT?
===================

Overview
--------

.. code-block:: text

   PREEMPT_RT is a set of patches to the Linux kernel that:
   
   1. Makes the kernel fully preemptible
   2. Converts spinlocks to RT mutexes
   3. Provides deterministic latencies
   4. Enables hard real-time capabilities
   
   Use Cases:
   - Industrial automation
   - Robotics control
   - Audio/video processing
   - Telecommunications
   - Medical devices
   - Automotive systems (ADAS, engine control)
   
   NOT suitable for:
   - Hard real-time safety-critical systems (use RTOS)
   - Ultra-low latency (<10μs consistently)
   - Systems requiring formal verification

Preemption Models
-----------------

.. code-block:: text

   CONFIG_PREEMPT_NONE:
   - No forced preemption
   - Server workloads
   - Best throughput
   
   CONFIG_PREEMPT_VOLUNTARY:
   - Explicit preemption points
   - Desktop systems
   - Balanced latency/throughput
   
   CONFIG_PREEMPT:
   - Preemptible kernel (standard)
   - Low-latency desktop
   - Good for multimedia
   
   CONFIG_PREEMPT_RT (PREEMPT_RT patch):
   - Fully preemptible kernel
   - Hard real-time capable
   - Lowest latency
   - Some throughput cost

Key Features
------------

.. code-block:: text

   1. Threaded Interrupts:
      - Most interrupt handlers run as threads
      - Can be preempted and scheduled
      - Allows prioritization
   
   2. Priority Inheritance:
      - Prevents priority inversion
      - Mutex holders inherit priority
      - Automatic boost/deboost
   
   3. High-Resolution Timers:
      - Nanosecond precision
      - Hardware timer support
      - Reliable timing
   
   4. Spinlock to RT Mutex Conversion:
      - Most spinlocks become sleeping locks
      - Reduces non-preemptible sections
      - Better worst-case latency
   
   5. Reduced Latency Paths:
      - Shorter critical sections
      - Preemptible RCU
      - Predictable behavior

Installation
============

Downloading RT Patch
--------------------

.. code-block:: bash

   # Find matching kernel and RT patch
   # https://cdn.kernel.org/pub/linux/kernel/projects/rt/
   
   KERNEL_VERSION="6.1.70"
   RT_PATCH="patch-6.1.70-rt20.patch.xz"
   
   # Download kernel source
   wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KERNEL_VERSION}.tar.xz
   
   # Download RT patch
   wget https://cdn.kernel.org/pub/linux/kernel/projects/rt/6.1/${RT_PATCH}
   
   # Verify checksums (recommended)
   wget https://cdn.kernel.org/pub/linux/kernel/v6.x/sha256sums.asc
   sha256sum -c sha256sums.asc --ignore-missing

Applying the Patch
------------------

.. code-block:: bash

   # Extract kernel
   tar xf linux-${KERNEL_VERSION}.tar.xz
   cd linux-${KERNEL_VERSION}
   
   # Apply RT patch
   xzcat ../patch-6.1.70-rt20.patch.xz | patch -p1
   
   # Verify patch applied
   grep PREEMPT_RT Makefile
   # Should see: EXTRAVERSION = -rt20

Kernel Configuration
--------------------

.. code-block:: bash

   # Start with current config
   cp /boot/config-$(uname -r) .config
   make oldconfig
   
   # Or use menuconfig
   make menuconfig
   
   # Required RT settings:
   # General setup -->
   #   [*] Fully Preemptible Kernel (RT)
   #   [*] High Resolution Timer Support
   #
   # Processor type and features -->
   #   Timer frequency (1000 HZ)
   #
   # Power management and ACPI options -->
   #   CPU Frequency scaling -->
   #     [ ] CPU Frequency scaling (disable for determinism)
   #
   # Kernel hacking -->
   #   [ ] Debug preemptible kernel (optional, for development)

Important Config Options
------------------------

.. code-block:: bash

   # Check/set these in .config:
   
   # PREEMPT_RT model
   CONFIG_PREEMPT_RT=y
   CONFIG_PREEMPT_RT_FULL=y
   
   # High-resolution timers
   CONFIG_HIGH_RES_TIMERS=y
   CONFIG_NO_HZ_FULL=y
   
   # Timer frequency (1000Hz recommended for RT)
   CONFIG_HZ_1000=y
   CONFIG_HZ=1000
   
   # Disable CPU frequency scaling (for determinism)
   # CONFIG_CPU_FREQ is not set
   
   # Enable threaded IRQs
   CONFIG_IRQ_FORCED_THREADING=y
   
   # RCU configuration
   CONFIG_PREEMPT_RCU=y
   CONFIG_RCU_BOOST=y
   
   # Disable group scheduling (optional, for better RT behavior)
   # CONFIG_FAIR_GROUP_SCHED is not set

Building the Kernel
-------------------

.. code-block:: bash

   # Build Debian packages (Debian/Ubuntu)
   make -j$(nproc) deb-pkg LOCALVERSION=-rt
   
   # Or traditional build (all distros)
   make -j$(nproc)
   sudo make modules_install
   sudo make install
   
   # Update bootloader
   sudo update-grub  # Debian/Ubuntu
   sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL/Fedora

Installing Built Packages
-------------------------

.. code-block:: bash

   # Install Debian packages
   cd ..
   sudo dpkg -i linux-image-*-rt_*.deb
   sudo dpkg -i linux-headers-*-rt_*.deb
   
   # Reboot into new kernel
   sudo reboot
   
   # After reboot, verify
   uname -a
   # Should show: ... PREEMPT_RT ...

Verification
------------

.. code-block:: bash

   # Check kernel version
   uname -r
   # Example: 6.1.70-rt20
   
   # Verify RT patch
   uname -v | grep PREEMPT_RT
   
   # Check config
   zcat /proc/config.gz | grep PREEMPT_RT
   # Should show: CONFIG_PREEMPT_RT=y
   
   # Check threaded interrupts
   ps aux | grep "\[irq/"
   # Should see threaded IRQ handlers

System Configuration
====================

Kernel Command Line
-------------------

.. code-block:: bash

   # /etc/default/grub
   # Add to GRUB_CMDLINE_LINUX:
   
   # Isolate CPUs for real-time (CPUs 2-3 for RT only)
   isolcpus=2,3
   
   # Disable CPU idle (prevent C-states)
   idle=poll
   # Or limit C-states
   processor.max_cstate=1
   
   # Disable CPU frequency scaling
   intel_pstate=disable
   
   # Disable watchdog
   nowatchdog
   
   # Example full command line:
   GRUB_CMDLINE_LINUX="isolcpus=2,3 idle=poll intel_pstate=disable nowatchdog"
   
   # Update grub
   sudo update-grub
   sudo reboot

CPU Isolation
-------------

.. code-block:: bash

   # Isolate CPUs 2-3 for real-time workload
   # Add to kernel command line:
   isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3
   
   # Verify isolation
   cat /sys/devices/system/cpu/isolated
   
   # Move IRQ handling away from isolated CPUs
   # /etc/rc.local or systemd service:
   for i in /proc/irq/*/smp_affinity; do
       echo 3 > $i  # CPUs 0-1 (binary: 0011)
   done
   
   # Set CPU affinity for RT task
   taskset -c 2,3 ./my_rt_app

IRQ Threading
-------------

.. code-block:: bash

   # Check threaded IRQs
   ps -eLo pid,class,rtprio,cmd | grep "\[irq/"
   
   # Example output:
   #   12 FF      50 [irq/9-acpi]
   #   18 FF      50 [irq/16-ehci_hcd:usb1]
   
   # Force specific IRQ to be threaded
   echo 1 > /proc/irq/16/threaded
   
   # Set IRQ thread priority
   chrt -f -p 90 $(pgrep "irq/16")
   
   # Disable IRQ threading for specific IRQ (if needed)
   echo 0 > /proc/irq/16/threaded

Priority Configuration
======================

Real-time Scheduling Policies
------------------------------

.. code-block:: c

   // SCHED_FIFO: First-In-First-Out real-time scheduling
   // Higher priority always preempts lower
   // No time slicing at same priority
   
   // SCHED_RR: Round-Robin real-time scheduling
   // Time slicing among same priority tasks
   
   // SCHED_DEADLINE: Earliest Deadline First (EDF)
   // Deadline-based scheduling (most powerful)
   
   // Priority range: 1-99 (higher number = higher priority)

Setting Process Priority
-------------------------

.. code-block:: bash

   # SCHED_FIFO with priority 80
   chrt -f 80 ./my_rt_app
   
   # SCHED_RR with priority 50
   chrt -r 50 ./my_rt_app
   
   # Change running process priority
   chrt -f -p 90 1234
   
   # Check process priority
   chrt -p 1234
   
   # View all RT processes
   ps -eLo pid,tid,class,rtprio,pri,psr,comm | grep -E "FF|RR"
   # class: FF=FIFO, RR=Round-Robin
   # rtprio: Real-time priority (1-99)

Setting Thread Priority (C code)
---------------------------------

.. code-block:: c

   #include <pthread.h>
   #include <sched.h>
   #include <stdio.h>
   
   void set_rt_priority(pthread_t thread, int policy, int priority) {
       struct sched_param param;
       param.sched_priority = priority;
       
       if (pthread_setschedparam(thread, policy, &param) != 0) {
           perror("pthread_setschedparam");
       }
   }
   
   int main() {
       pthread_t thread = pthread_self();
       
       // Set to SCHED_FIFO with priority 80
       set_rt_priority(thread, SCHED_FIFO, 80);
       
       // Lock memory to prevent paging
       mlockall(MCL_CURRENT | MCL_FUTURE);
       
       // Your real-time code here
       
       return 0;
   }

Memory Locking
--------------

.. code-block:: c

   #include <sys/mman.h>
   
   // Lock all current and future pages
   if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
       perror("mlockall");
       return -1;
   }
   
   // Pre-fault stack
   unsigned char dummy[MAX_STACK_SIZE];
   memset(dummy, 0, MAX_STACK_SIZE);
   
   // Unlock when done
   munlockall();

Resource Limits
---------------

.. code-block:: bash

   # Allow non-root to set RT priority
   # /etc/security/limits.conf
   
   @realtime   -   rtprio     99
   @realtime   -   memlock    unlimited
   @realtime   -   nice       -20
   
   # Or for specific user
   myuser      -   rtprio     80
   myuser      -   memlock    102400
   
   # Apply limits
   # User must logout and login again
   
   # Check current limits
   ulimit -a

Testing and Validation
======================

Latency Testing with cyclictest
--------------------------------

.. code-block:: bash

   # Install rt-tests
   sudo apt install rt-tests
   
   # Basic latency test (4 threads, priority 80)
   sudo cyclictest -t 4 -p 80 -n -m
   
   # Extended test (10 minutes)
   sudo cyclictest -t 4 -p 80 -n -m -l 600000
   
   # With histogram
   sudo cyclictest -t 4 -p 80 -n -m -l 10000 -h 100 -q
   
   # Full stress test
   sudo cyclictest -t 4 -p 80 -n -m -l 1000000 -a 2,3,4,5 -h 100
   
   # Options:
   # -t N: number of threads
   # -p N: priority
   # -n: use clock_nanosleep
   # -m: lock memory
   # -l N: number of loops
   # -a N: CPU affinity
   # -h N: histogram buckets
   # -q: quiet mode
   
   # Interpret results:
   # Max latency should be <100μs for good RT system
   # <50μs is excellent

Stress Testing
--------------

.. code-block:: bash

   # Run cyclictest with stress load
   sudo apt install stress-ng
   
   # Terminal 1: Start stress
   stress-ng --cpu 4 --io 2 --vm 2 --vm-bytes 128M
   
   # Terminal 2: Run cyclictest
   sudo cyclictest -t 4 -p 80 -n -m -l 100000
   
   # Or combined
   sudo cyclictest -t 4 -p 80 -n -m -l 100000 & \
   stress-ng --cpu 4 --io 2 --vm 2 --vm-bytes 128M --timeout 60s

hwlatdetect
-----------

.. code-block:: bash

   # Detect hardware-induced latencies
   sudo hwlatdetect --duration=60
   
   # With threshold
   sudo hwlatdetect --duration=60 --threshold=10
   
   # Check for SMI (System Management Interrupt) latencies

Monitoring Tools
----------------

.. code-block:: bash

   # ftrace for latency analysis
   sudo trace-cmd record -e sched_wakeup -e sched_switch ./my_rt_app
   sudo trace-cmd report
   
   # perf for performance analysis
   sudo perf record -a -g ./my_rt_app
   sudo perf report
   
   # Check scheduler statistics
   cat /proc/sched_debug

Common Issues and Solutions
===========================

High Latencies
--------------

.. code-block:: bash

   # 1. Check for non-RT tasks using CPU
   ps -eLo pid,class,rtprio,cmd | grep -v FF
   
   # 2. Disable CPU frequency scaling
   for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
       echo performance > $cpu
   done
   
   # 3. Disable power management
   # Add to kernel command line: idle=poll processor.max_cstate=0
   
   # 4. Move IRQs away from RT CPUs
   for i in /proc/irq/*/smp_affinity; do
       echo 3 > $i  # Use CPUs 0-1 only
   done
   
   # 5. Check for SMI latencies
   sudo hwlatdetect --duration=60

Priority Inversion
------------------

.. code-block:: text

   PREEMPT_RT handles priority inversion automatically through:
   
   1. Priority Inheritance (PI):
      - Mutex owner inherits highest waiter priority
      - Automatic boost and deboost
   
   2. Use RT mutexes:
      - pthread_mutex with PTHREAD_PRIO_INHERIT
      - Kernel mutexes have PI built-in
   
   Example:
   pthread_mutexattr_t attr;
   pthread_mutexattr_init(&attr);
   pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
   pthread_mutex_init(&mutex, &attr);

Memory Allocation in RT Context
--------------------------------

.. code-block:: c

   // NEVER allocate memory in RT path
   // Pre-allocate everything
   
   // Bad:
   void rt_task() {
       char *buf = malloc(1024);  // WRONG! Non-deterministic
       // ...
       free(buf);
   }
   
   // Good:
   char static_buf[1024];  // Pre-allocated
   
   void rt_task() {
       // Use static_buf directly
   }
   
   // For dynamic needs, use memory pools
   // Pre-allocate pool at initialization

Best Practices
==============

1. **Lock memory** with mlockall() to prevent paging
2. **Pre-allocate resources** - no malloc/free in RT path
3. **Use appropriate priority** - not all tasks need priority 99
4. **Isolate RT CPUs** - dedicate cores for RT workload
5. **Avoid system calls** in critical paths
6. **Use RT-safe APIs** - clock_nanosleep, not sleep/usleep
7. **Minimize critical sections** - keep locks short
8. **Test under load** - stress test with cyclictest
9. **Monitor latencies** - continuous monitoring in production
10. **Profile and optimize** - use ftrace/perf to find bottlenecks

Common Pitfalls
===============

1. **Using non-RT sleep** - sleep/usleep are not RT-safe
2. **Memory allocation** in RT path causes latencies
3. **No memory locking** - page faults destroy determinism
4. **Wrong priority** - all tasks at 99 defeats scheduling
5. **Ignoring CPU isolation** - general tasks interfere
6. **CPU frequency scaling** enabled - variable performance
7. **Not testing** - latency spikes in production

Quick Reference
===============

.. code-block:: bash

   # Check RT kernel
   uname -a | grep PREEMPT_RT
   
   # Set RT priority
   chrt -f 80 ./app
   
   # Check RT processes
   ps -eLo pid,class,rtprio,cmd | grep -E "FF|RR"
   
   # Test latency
   sudo cyclictest -t 4 -p 80 -n -m -l 10000
   
   # Isolate CPUs
   # Kernel cmdline: isolcpus=2,3 nohz_full=2,3
   
   # Lock memory (in code)
   mlockall(MCL_CURRENT | MCL_FUTURE)

See Also
========

- Linux_Realtime_Scheduling.rst
- Linux_Latency_Analysis.rst
- Linux_Realtime_Best_Practices.rst

References
==========

- https://wiki.linuxfoundation.org/realtime/start
- https://rt.wiki.kernel.org/
- man 1 chrt
- man 2 sched_setscheduler
- man 3 pthread_setschedparam
