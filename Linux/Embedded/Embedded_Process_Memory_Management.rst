================================================================================
Embedded Linux: Process & Memory Management - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch9-10)
:Target: Process Scheduling, Memory Management, cgroups
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Process Management:**

.. code-block:: bash

   # Process info
   ps aux
   top
   htop
   pidof myapp
   pgrep -l myapp
   
   # Process control
   nice -n 10 myapp           # Start with priority
   renice -n -5 -p 1234       # Change priority
   ionice -c2 -n0 myapp       # I/O priority
   taskset -c 0,1 myapp       # CPU affinity
   
   # Kill processes
   kill -TERM 1234
   killall myapp
   pkill myapp

**Scheduling Policies:**

.. code-block:: bash

   # View policy
   chrt -p 1234
   
   # Set real-time policy
   chrt -f -p 50 1234         # SCHED_FIFO, priority 50
   chrt -r -p 50 1234         # SCHED_RR
   
   # Set normal policy
   chrt -o -p 0 1234          # SCHED_OTHER
   chrt -b -p 0 1234          # SCHED_BATCH
   chrt -i -p 0 1234          # SCHED_IDLE

**Memory Commands:**

.. code-block:: bash

   # Memory info
   free -h
   cat /proc/meminfo
   cat /proc/buddyinfo
   slabtop
   
   # Process memory
   cat /proc/1234/status
   cat /proc/1234/maps
   pmap 1234
   
   # Clear caches
   sync
   echo 3 > /proc/sys/vm/drop_caches

**cgroups:**

.. code-block:: bash

   # Create cgroup (v2)
   mkdir /sys/fs/cgroup/mygroup
   
   # Set limits
   echo "100M" > /sys/fs/cgroup/mygroup/memory.max
   echo "50000" > /sys/fs/cgroup/mygroup/cpu.max
   
   # Add process
   echo 1234 > /sys/fs/cgroup/mygroup/cgroup.procs
   
   # systemd cgroup
   systemctl set-property myapp.service MemoryLimit=100M
   systemctl set-property myapp.service CPUQuota=50%

================================================================================
1. Process Management
================================================================================

1.1 Process Basics
-------------------

**Process States:**

.. code-block:: text

   R  Running or runnable
   S  Interruptible sleep (waiting for event)
   D  Uninterruptible sleep (I/O)
   T  Stopped (SIGSTOP or debugger)
   Z  Zombie (terminated, parent not reaped)
   X  Dead

**Process Hierarchy:**

.. code-block:: bash

   # Process tree
   pstree
   pstree -p              # With PIDs
   ps axjf                # Forest view
   
   # Parent-child relationship
   ps -o pid,ppid,cmd
   
   # Orphaned processes adopted by init (PID 1)

**Process Information:**

.. code-block:: bash

   # List processes
   ps aux                 # All processes
   ps -eLf                # With threads
   ps -o pid,comm,state,nice,rtprio
   
   # Process details
   cat /proc/1234/status
   cat /proc/1234/cmdline
   cat /proc/1234/environ
   cat /proc/1234/limits
   
   # Find processes
   pidof myapp
   pgrep myapp
   pgrep -u username

1.2 Process Control
--------------------

**Process Signals:**

.. code-block:: bash

   # Signal list
   kill -l
   
   # Common signals
   SIGTERM (15)  # Graceful termination (default)
   SIGKILL (9)   # Force kill (cannot be caught)
   SIGHUP (1)    # Hangup (reload config)
   SIGINT (2)    # Interrupt (Ctrl+C)
   SIGQUIT (3)   # Quit (Ctrl+\)
   SIGSTOP (19)  # Pause
   SIGCONT (18)  # Resume
   
   # Send signals
   kill -TERM 1234
   kill -9 1234
   killall myapp
   pkill -TERM myapp
   pkill -9 -u username

**Process Priority:**

.. code-block:: bash

   # Nice values: -20 (highest) to 19 (lowest)
   # Default: 0
   
   # Start with nice value
   nice -n 10 myapp
   nice -n -5 myapp       # Requires root
   
   # Change priority
   renice -n 5 -p 1234
   renice -n -10 -p 1234  # Requires root
   
   # View priority
   ps -o pid,ni,cmd
   top  # Press 'r' to renice

================================================================================
2. CPU Scheduling
================================================================================

2.1 Scheduling Policies
------------------------

**Policy Types:**

.. code-block:: text

   Normal (Time-Sharing):
   ----------------------
   SCHED_OTHER (0):  Default, CFS scheduler
   SCHED_BATCH (3):  CPU-intensive batch jobs
   SCHED_IDLE (5):   Very low priority
   
   Real-Time:
   ----------
   SCHED_FIFO (1):   First-in-first-out, no time slicing
   SCHED_RR (2):     Round-robin with time quantum
   
   Priority ranges:
   - RT: 1-99 (higher = higher priority)
   - Normal: Uses nice values

**chrt Command:**

.. code-block:: bash

   # View scheduling policy
   chrt -p 1234
   chrt -p $$             # Current shell
   
   # Set SCHED_FIFO (real-time)
   chrt -f -p 50 1234     # Priority 50
   chrt -f 50 myapp       # Start with RT priority
   
   # Set SCHED_RR
   chrt -r -p 50 1234
   
   # Set SCHED_OTHER
   chrt -o -p 0 1234
   
   # Set SCHED_BATCH
   chrt -b -p 0 1234
   
   # Set SCHED_IDLE
   chrt -i -p 0 1234
   
   # View all processes with policy
   ps -eo pid,cls,rtprio,ni,cmd

2.2 CPU Affinity
-----------------

**CPU Binding:**

.. code-block:: bash

   # Set CPU affinity (taskset)
   taskset -c 0 myapp              # CPU 0 only
   taskset -c 0,1 myapp            # CPU 0 and 1
   taskset -c 0-3 myapp            # CPU 0-3
   
   # Set for running process
   taskset -p -c 0,1 1234
   
   # View affinity
   taskset -p 1234
   
   # View in /proc
   cat /proc/1234/status | grep Cpus_allowed

**CPU Isolation:**

.. code-block:: bash

   # Kernel command line (isolate CPU 2-3)
   isolcpus=2,3
   
   # Use isolated CPUs for dedicated tasks
   taskset -c 2 critical-app

================================================================================
3. Memory Management
================================================================================

3.1 Virtual Memory Basics
--------------------------

**Memory Layout:**

.. code-block:: text

   High Address
   +------------------+
   | Kernel Space     | 1GB (3G/1G split typical)
   +------------------+
   | Stack            | Grows down
   |       ↓          |
   |                  |
   |       ↑          |
   | Heap             | Grows up
   +------------------+
   | BSS (uninitialized)
   +------------------+
   | Data (initialized)
   +------------------+
   | Text (code)      | Read-only
   +------------------+
   Low Address

**Memory Information:**

.. code-block:: bash

   # System memory
   free -h
   cat /proc/meminfo
   
   # Process memory
   cat /proc/1234/status | grep -i vm
   cat /proc/1234/status | grep -i rss
   cat /proc/1234/smaps
   pmap 1234
   
   # Memory map
   cat /proc/1234/maps
   
   # Page size
   getconf PAGE_SIZE

**Memory Metrics:**

.. code-block:: text

   VSZ (Virtual Size):  Total virtual memory
   RSS (Resident Set):  Physical memory used
   PSS (Proportional):  Shared memory divided
   USS (Unique Set):    Private memory only
   
   Shared Memory:       Memory mapped by multiple processes
   Anonymous:           Not backed by files (heap, stack)
   File-backed:         Backed by files (mmap, executables)

3.2 OOM Killer
--------------

**Out-of-Memory Management:**

.. code-block:: bash

   # OOM score (higher = more likely to be killed)
   cat /proc/1234/oom_score
   
   # OOM adjustment (-1000 to 1000)
   echo -500 > /proc/1234/oom_score_adj  # Less likely
   echo 500 > /proc/1234/oom_score_adj   # More likely
   echo -1000 > /proc/1234/oom_score_adj # Disable OOM kill
   
   # View OOM kills in logs
   dmesg | grep -i oom
   journalctl -k | grep -i oom

**OOM Configuration:**

.. code-block:: bash

   # Kernel parameters
   vm.panic_on_oom = 0          # Don't panic on OOM
   vm.oom_kill_allocating_task = 0  # Kill task with lowest score
   vm.overcommit_memory = 0     # Heuristic overcommit
   
   # Set via sysctl
   sysctl -w vm.overcommit_memory=2
   
   # /etc/sysctl.conf
   vm.overcommit_memory = 2
   vm.overcommit_ratio = 80

3.3 Memory Tuning
-----------------

**Cache Management:**

.. code-block:: bash

   # View caches
   cat /proc/meminfo | grep -i cache
   cat /proc/slabinfo
   slabtop
   
   # Drop caches (free memory)
   sync
   echo 1 > /proc/sys/vm/drop_caches  # Page cache
   echo 2 > /proc/sys/vm/drop_caches  # Dentries/inodes
   echo 3 > /proc/sys/vm/drop_caches  # All

**Swappiness:**

.. code-block:: bash

   # View swappiness (0-100)
   cat /proc/sys/vm/swappiness
   
   # Set swappiness
   echo 10 > /proc/sys/vm/swappiness
   
   # Permanent (/etc/sysctl.conf)
   vm.swappiness = 10
   
   # Disable swap
   swapoff -a
   
   # Re-enable swap
   swapon -a

**Huge Pages:**

.. code-block:: bash

   # View huge pages
   cat /proc/meminfo | grep -i huge
   
   # Configure huge pages
   echo 128 > /proc/sys/vm/nr_hugepages
   
   # Mount hugetlbfs
   mount -t hugetlbfs none /mnt/huge

================================================================================
4. cgroups (Control Groups)
================================================================================

4.1 cgroups v1 vs v2
--------------------

**Version Comparison:**

.. code-block:: text

   cgroups v1:
   - Multiple hierarchies
   - Per-controller mountpoints
   - Complex, flexible
   
   cgroups v2:
   - Single unified hierarchy
   - Simpler interface
   - Better integrated with systemd

**Check cgroups Version:**

.. code-block:: bash

   # Check mount
   mount | grep cgroup
   
   # v1: /sys/fs/cgroup/<controller>
   # v2: /sys/fs/cgroup (unified)
   
   # Kernel support
   cat /proc/filesystems | grep cgroup

4.2 cgroups v2 Usage
--------------------

**cgroup Structure:**

.. code-block:: bash

   # Create cgroup
   mkdir /sys/fs/cgroup/mygroup
   
   # View controllers
   cat /sys/fs/cgroup/cgroup.controllers
   
   # Enable controllers
   echo "+cpu +memory +io" > /sys/fs/cgroup/cgroup.subtree_control
   
   # Add process to cgroup
   echo 1234 > /sys/fs/cgroup/mygroup/cgroup.procs
   
   # View processes
   cat /sys/fs/cgroup/mygroup/cgroup.procs

**Memory Limits:**

.. code-block:: bash

   # Set memory limit
   echo "100M" > /sys/fs/cgroup/mygroup/memory.max
   echo "50M" > /sys/fs/cgroup/mygroup/memory.high  # Soft limit
   
   # View usage
   cat /sys/fs/cgroup/mygroup/memory.current
   cat /sys/fs/cgroup/mygroup/memory.stat

**CPU Limits:**

.. code-block:: bash

   # CPU quota (100000 = 100% of 1 CPU)
   echo "50000 100000" > /sys/fs/cgroup/mygroup/cpu.max  # 50%
   
   # CPU weight (100-10000, default 100)
   echo "200" > /sys/fs/cgroup/mygroup/cpu.weight
   
   # View usage
   cat /sys/fs/cgroup/mygroup/cpu.stat

**I/O Limits:**

.. code-block:: bash

   # I/O weight (1-10000, default 100)
   echo "8:0 weight=200" > /sys/fs/cgroup/mygroup/io.weight
   
   # I/O max (bytes/sec or iops/sec)
   echo "8:0 rbps=1048576 wbps=1048576" > /sys/fs/cgroup/mygroup/io.max
   
   # View I/O stats
   cat /sys/fs/cgroup/mygroup/io.stat

4.3 systemd and cgroups
------------------------

**Service Resource Limits:**

.. code-block:: ini

   # /etc/systemd/system/myapp.service
   [Service]
   MemoryLimit=100M
   MemoryHigh=50M
   CPUQuota=50%
   CPUWeight=200
   IOWeight=200
   TasksMax=50
   
   # Alternative: MemoryMax, MemoryAccounting

**Runtime Configuration:**

.. code-block:: bash

   # Set limits at runtime
   systemctl set-property myapp.service MemoryLimit=100M
   systemctl set-property myapp.service CPUQuota=50%
   
   # View cgroup
   systemctl status myapp
   cat /proc/$(pidof myapp)/cgroup
   
   # View resource usage
   systemd-cgtop

**Slice Hierarchy:**

.. code-block:: text

   -.slice (root)
   ├─ system.slice
   │  ├─ system-serial\x2dgetty.slice
   │  └─ myapp.service
   ├─ user.slice
   │  └─ user-1000.slice
   └─ machine.slice

================================================================================
5. Process Monitoring
================================================================================

5.1 Monitoring Tools
--------------------

**top:**

.. code-block:: bash

   # Basic top
   top
   
   # Shortcuts in top:
   # 1 - Show all CPUs
   # H - Show threads
   # k - Kill process
   # r - Renice
   # M - Sort by memory
   # P - Sort by CPU
   # c - Show command line
   # f - Select fields

**htop:**

.. code-block:: bash

   # Enhanced top
   htop
   
   # Features:
   # - Color-coded
   # - Mouse support
   # - Tree view (F5)
   # - Search (F3)
   # - Filter (F4)
   # - Kill (F9)

**atop:**

.. code-block:: bash

   # Advanced monitoring
   atop
   atop -r /var/log/atop/atop_20260118  # Historical
   
   # Shortcuts:
   # m - Memory
   # d - Disk
   # n - Network
   # g - Generic

5.2 Process Accounting
-----------------------

**psacct/acct:**

.. code-block:: bash

   # Install and enable
   apt-get install acct
   systemctl enable acct
   systemctl start acct
   
   # View accounting
   sa                     # Summary
   ac                     # Connect time
   lastcomm               # Last commands
   dump-acct /var/log/account/pacct

================================================================================
6. Key Takeaways
================================================================================

.. code-block:: text

   Process Management:
   ===================
   ps aux
   top / htop
   nice -n 10 myapp
   renice -n 5 -p 1234
   taskset -c 0,1 myapp
   
   Scheduling:
   ===========
   chrt -f -p 50 1234     # RT FIFO
   chrt -r -p 50 1234     # RT RR
   chrt -o -p 0 1234      # Normal
   
   Memory:
   =======
   free -h
   pmap 1234
   cat /proc/1234/status
   echo 3 > /proc/sys/vm/drop_caches
   
   cgroups v2:
   ===========
   mkdir /sys/fs/cgroup/mygroup
   echo "100M" > /sys/fs/cgroup/mygroup/memory.max
   echo "50000 100000" > /sys/fs/cgroup/mygroup/cpu.max
   echo 1234 > /sys/fs/cgroup/mygroup/cgroup.procs
   
   systemd cgroups:
   ================
   systemctl set-property myapp.service MemoryLimit=100M
   systemctl set-property myapp.service CPUQuota=50%
   systemd-cgtop

================================================================================
END OF CHEATSHEET
================================================================================
