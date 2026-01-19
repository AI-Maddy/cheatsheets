================================================================================
Embedded Linux: Init Systems & Services - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch6)
:Target: Init Systems, Service Management
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Init System Comparison:**

.. code-block:: text

   BusyBox init:
   ✓ Simple, lightweight (<100KB)
   ✓ Single /etc/inittab file
   ✗ No dependency management
   ✗ Sequential startup
   Use: Simple embedded systems
   
   SysV init:
   ✓ Traditional Unix init
   ✓ Runlevels (/etc/rc*.d/)
   ✗ Shell scripts (slow)
   ✗ No parallel startup
   Use: Legacy compatibility
   
   systemd:
   ✓ Parallel startup, fast boot
   ✓ Dependency management
   ✓ Socket activation
   ✗ Complex, large (>10MB)
   ✗ Requires D-Bus
   Use: Modern systems, complex services

**BusyBox init Configuration:**

.. code-block:: bash

   # /etc/inittab
   ::sysinit:/etc/init.d/rcS
   ::respawn:/sbin/getty 115200 console
   ::restart:/sbin/init
   ::ctrlaltdel:/sbin/reboot
   ::shutdown:/bin/umount -a -r
   
   # /etc/init.d/rcS
   #!/bin/sh
   /bin/mount -t proc proc /proc
   /bin/mount -t sysfs sysfs /sys
   /bin/mount -t devtmpfs devtmpfs /dev
   /etc/init.d/networking start
   
   # Service management
   /etc/init.d/networking start
   /etc/init.d/networking stop
   /etc/init.d/networking restart

**systemd Service:**

.. code-block:: ini

   # /etc/systemd/system/myapp.service
   [Unit]
   Description=My Application
   After=network.target
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/myapp
   Restart=on-failure
   User=myapp
   
   [Install]
   WantedBy=multi-user.target
   
   # Management
   systemctl start myapp
   systemctl enable myapp
   systemctl status myapp
   systemctl restart myapp
   journalctl -u myapp -f

================================================================================
1. Init System Overview
================================================================================

1.1 Init Process Role
----------------------

**Responsibilities:**

.. code-block:: text

   1. First User Space Process (PID 1)
      - Started by kernel after boot
      - Parent of all processes
      - Never terminates (kernel panic if it does)
   
   2. System Initialization
      - Mount filesystems
      - Start essential services
      - Configure networking
      - Initialize devices
   
   3. Service Management
      - Start/stop daemons
      - Monitor service health
      - Restart failed services
   
   4. Process Supervision
      - Reap orphaned processes
      - Handle zombie processes
      - Manage process tree
   
   5. Shutdown/Reboot
      - Graceful service shutdown
      - Unmount filesystems
      - Sync disks
      - System halt/reboot

**Init System Selection:**

.. code-block:: bash

   # Kernel parameter
   init=/sbin/init           # Default
   init=/bin/sh              # Emergency shell
   init=/lib/systemd/systemd # systemd
   
   # Check current init
   ps -p 1
   ls -l /sbin/init

1.2 Init System Comparison
---------------------------

**Feature Matrix:**

.. code-block:: text

   Feature              BusyBox  SysV   systemd
   =====================================|=======
   Size                 <100KB   ~1MB   >10MB
   Boot Speed           Slow     Slow   Fast
   Parallel Startup     No       No     Yes
   Dependency Mgmt      No       Manual Yes
   Socket Activation    No       No     Yes
   Resource Limits      No       No     Yes
   Logging              syslog   syslog journal
   Configuration        inittab  rcN.d  units
   Complexity           Simple   Medium Complex
   D-Bus Required       No       No     Yes

================================================================================
2. BusyBox Init
================================================================================

2.1 BusyBox Init Configuration
-------------------------------

**/etc/inittab Structure:**

.. code-block:: text

   Format: <id>::<action>:<process>
   
   id: Terminal (tty1, ttyS0, or empty)
   action: When to run
   process: Command to execute

**Actions:**

.. code-block:: bash

   sysinit    # Run once at startup (before respawn)
   respawn    # Restart if process terminates
   askfirst   # Prompt before running (rescue mode)
   wait       # Run once, wait for completion
   once       # Run once, don't wait
   restart    # Run when init receives SIGHUP
   ctrlaltdel # Run on Ctrl+Alt+Del
   shutdown   # Run during shutdown

**Example /etc/inittab:**

.. code-block:: bash

   # System initialization
   ::sysinit:/etc/init.d/rcS
   
   # Console getty
   ::respawn:/sbin/getty 115200 console
   tty1::respawn:/sbin/getty 38400 tty1
   
   # Serial console
   ttyS0::respawn:/sbin/getty -L ttyS0 115200 vt100
   
   # Shell on ttyS1 (ask before starting)
   ttyS1::askfirst:/bin/sh
   
   # Init restart
   ::restart:/sbin/init
   
   # Ctrl+Alt+Del
   ::ctrlaltdel:/sbin/reboot
   
   # Shutdown
   ::shutdown:/bin/umount -a -r
   ::shutdown:/sbin/swapoff -a

2.2 Startup Scripts
-------------------

**/etc/init.d/rcS (Main Startup):**

.. code-block:: bash

   #!/bin/sh
   
   # Mount virtual filesystems
   /bin/mount -t proc proc /proc
   /bin/mount -t sysfs sysfs /sys
   /bin/mount -t devtmpfs devtmpfs /dev
   /bin/mkdir -p /dev/pts /dev/shm
   /bin/mount -t devpts devpts /dev/pts
   /bin/mount -t tmpfs tmpfs /dev/shm
   
   # Hostname
   /bin/hostname -F /etc/hostname
   
   # Kernel modules
   /sbin/modprobe -a -b /etc/modules
   
   # Run init scripts
   for i in /etc/init.d/S??*; do
       [ -x "$i" ] || continue
       case "$i" in
           *.sh) . "$i" ;;
           *) "$i" start ;;
       esac
   done

**Service Script Template:**

.. code-block:: bash

   #!/bin/sh
   # /etc/init.d/S50myapp
   
   DAEMON=/usr/bin/myapp
   PIDFILE=/var/run/myapp.pid
   
   start() {
       echo "Starting myapp..."
       start-stop-daemon -S -q -p $PIDFILE -x $DAEMON -- --daemon
   }
   
   stop() {
       echo "Stopping myapp..."
       start-stop-daemon -K -q -p $PIDFILE
   }
   
   restart() {
       stop
       sleep 1
       start
   }
   
   case "$1" in
       start)
           start
           ;;
       stop)
           stop
           ;;
       restart|reload)
           restart
           ;;
       *)
           echo "Usage: $0 {start|stop|restart}"
           exit 1
   esac
   
   exit 0

**Numbering Convention:**

.. code-block:: text

   S01-S09: Critical system services
   S10-S19: Basic system services (syslog, udev)
   S20-S39: Networking
   S40-S49: Application services
   S50-S99: User services
   
   K prefix: Shutdown scripts (run in reverse)

2.3 BusyBox Init Management
----------------------------

**Init Control:**

.. code-block:: bash

   # Reload configuration
   kill -HUP 1
   init -q
   
   # Shutdown
   halt
   poweroff
   reboot
   
   # Service management
   /etc/init.d/networking start
   /etc/init.d/networking stop
   /etc/init.d/networking restart
   
   # Enable/disable service
   chmod +x /etc/init.d/S50myapp    # Enable
   chmod -x /etc/init.d/S50myapp    # Disable
   mv /etc/init.d/S50myapp /etc/init.d/K50myapp  # Disable

================================================================================
3. systemd
================================================================================

3.1 systemd Architecture
-------------------------

**Components:**

.. code-block:: text

   systemd (PID 1):
   - Service manager
   - Process supervisor
   - System state manager
   
   systemctl:
   - Control systemd
   - Manage services
   - System operations
   
   journald:
   - Logging daemon
   - Binary logs
   - Centralized logging
   
   udevd:
   - Device manager
   - Hotplug handling
   - Device node creation
   
   networkd:
   - Network configuration
   - DHCP client
   - Link management
   
   logind:
   - Session management
   - User login
   - Seat management

**Unit Types:**

.. code-block:: text

   .service   - Daemons and processes
   .socket    - IPC/network sockets
   .device    - Device units (udev)
   .mount     - Mount points
   .automount - Automount points
   .swap      - Swap files/devices
   .target    - Group of units (runlevel)
   .path      - Path-based activation
   .timer     - Timer-based activation
   .slice     - Resource management

3.2 Service Units
-----------------

**Service File Structure:**

.. code-block:: ini

   # /etc/systemd/system/myapp.service
   
   [Unit]
   Description=My Application Service
   Documentation=man:myapp(8) https://example.com
   Requires=network.target
   After=network.target syslog.target
   Before=nginx.service
   
   [Service]
   Type=simple
   User=myapp
   Group=myapp
   WorkingDirectory=/var/lib/myapp
   ExecStartPre=/usr/bin/myapp-setup
   ExecStart=/usr/bin/myapp --config /etc/myapp/config.conf
   ExecReload=/bin/kill -HUP $MAINPID
   ExecStop=/usr/bin/myapp-cleanup
   Restart=on-failure
   RestartSec=10
   
   # Resource limits
   MemoryLimit=512M
   CPUQuota=50%
   
   # Security
   PrivateTmp=yes
   NoNewPrivileges=yes
   ProtectSystem=full
   ProtectHome=yes
   
   [Install]
   WantedBy=multi-user.target
   Alias=app.service

**Service Types:**

.. code-block:: ini

   Type=simple      # Default, process is main
   Type=forking     # Daemon forks, parent exits
   Type=oneshot     # Short-lived process
   Type=notify      # Sends readiness notification
   Type=dbus        # Acquires D-Bus name
   Type=idle        # Delayed until all jobs complete

**Restart Policies:**

.. code-block:: ini

   Restart=no               # Never restart
   Restart=always           # Always restart
   Restart=on-success       # Restart on clean exit
   Restart=on-failure       # Restart on error
   Restart=on-abnormal      # Restart on signal/timeout
   Restart=on-abort         # Restart on unclean signal
   Restart=on-watchdog      # Restart on watchdog timeout

3.3 systemctl Commands
-----------------------

**Service Management:**

.. code-block:: bash

   # Start/stop/restart service
   systemctl start myapp
   systemctl stop myapp
   systemctl restart myapp
   systemctl reload myapp
   systemctl reload-or-restart myapp
   
   # Enable/disable (start at boot)
   systemctl enable myapp
   systemctl disable myapp
   systemctl is-enabled myapp
   
   # Status
   systemctl status myapp
   systemctl is-active myapp
   systemctl is-failed myapp
   
   # List units
   systemctl list-units
   systemctl list-units --type=service
   systemctl list-units --state=failed
   systemctl list-unit-files
   
   # Dependencies
   systemctl list-dependencies myapp
   systemctl show myapp

**System Management:**

.. code-block:: bash

   # System state
   systemctl reboot
   systemctl poweroff
   systemctl suspend
   systemctl hibernate
   
   # Default target (runlevel)
   systemctl get-default
   systemctl set-default multi-user.target
   systemctl isolate rescue.target
   
   # Daemon reload (after config changes)
   systemctl daemon-reload

3.4 Targets (Runlevels)
-----------------------

**Target Comparison:**

.. code-block:: text

   systemd Target        SysV Runlevel  Description
   ===============================================================
   poweroff.target       0              Shutdown
   rescue.target         1, S           Single-user mode
   multi-user.target     2, 3, 4        Multi-user, no GUI
   graphical.target      5              Multi-user with GUI
   reboot.target         6              Reboot
   emergency.target      -              Emergency shell

**Target Operations:**

.. code-block:: bash

   # Switch to target
   systemctl isolate multi-user.target
   systemctl isolate graphical.target
   
   # Set default target
   systemctl set-default multi-user.target
   systemctl get-default
   
   # List targets
   systemctl list-units --type=target

3.5 Journal (Logging)
---------------------

**journalctl Commands:**

.. code-block:: bash

   # View all logs
   journalctl
   journalctl -n 50              # Last 50 entries
   journalctl -f                 # Follow (tail -f)
   
   # Filter by unit
   journalctl -u myapp
   journalctl -u myapp -f
   journalctl -u myapp --since today
   journalctl -u myapp --since "2024-01-01"
   journalctl -u myapp --since "1 hour ago"
   
   # Filter by priority
   journalctl -p err             # Error and above
   journalctl -p warning         # Warning and above
   
   # Boot logs
   journalctl -b                 # Current boot
   journalctl -b -1              # Previous boot
   journalctl --list-boots
   
   # Kernel messages
   journalctl -k
   
   # Output formats
   journalctl -o json
   journalctl -o json-pretty
   journalctl -o verbose
   
   # Disk usage
   journalctl --disk-usage
   journalctl --vacuum-time=2weeks
   journalctl --vacuum-size=100M

**Journal Configuration:**

.. code-block:: ini

   # /etc/systemd/journald.conf
   [Journal]
   Storage=persistent         # Store on disk
   SystemMaxUse=100M         # Max disk usage
   RuntimeMaxUse=50M         # Max RAM usage
   MaxRetentionSec=1month    # Keep 1 month
   ForwardToSyslog=yes       # Forward to syslog

================================================================================
4. Service Examples
================================================================================

4.1 Network Service (systemd)
------------------------------

.. code-block:: ini

   # /etc/systemd/system/network-config.service
   [Unit]
   Description=Network Configuration
   Wants=network-pre.target
   Before=network.target
   
   [Service]
   Type=oneshot
   RemainAfterExit=yes
   ExecStart=/usr/sbin/ip addr add 192.168.1.10/24 dev eth0
   ExecStart=/usr/sbin/ip link set eth0 up
   ExecStart=/usr/sbin/ip route add default via 192.168.1.1
   ExecStop=/usr/sbin/ip link set eth0 down
   
   [Install]
   WantedBy=multi-user.target

4.2 Application with Watchdog
------------------------------

.. code-block:: ini

   # /etc/systemd/system/monitored-app.service
   [Unit]
   Description=Monitored Application
   After=network.target
   
   [Service]
   Type=notify
   ExecStart=/usr/bin/monitored-app
   WatchdogSec=30
   Restart=on-failure
   RestartSec=5s
   StartLimitBurst=5
   StartLimitIntervalSec=300
   
   [Install]
   WantedBy=multi-user.target

**Application Code (Watchdog):**

.. code-block:: c

   #include <systemd/sd-daemon.h>
   
   int main() {
       // Notify systemd: ready
       sd_notify(0, "READY=1");
       
       while (1) {
           // Do work...
           
           // Send watchdog keepalive
           sd_notify(0, "WATCHDOG=1");
           
           sleep(10);
       }
   }

4.3 Timer-Based Service
-----------------------

.. code-block:: ini

   # /etc/systemd/system/backup.timer
   [Unit]
   Description=Backup Timer
   
   [Timer]
   OnBootSec=15min
   OnUnitActiveSec=1d
   Unit=backup.service
   
   [Install]
   WantedBy=timers.target
   
   # /etc/systemd/system/backup.service
   [Unit]
   Description=Backup Service
   
   [Service]
   Type=oneshot
   ExecStart=/usr/bin/backup-script

**Timer Management:**

.. code-block:: bash

   systemctl start backup.timer
   systemctl enable backup.timer
   systemctl list-timers

================================================================================
5. Boot Optimization
================================================================================

5.1 Boot Analysis
-----------------

**systemd Boot Analysis:**

.. code-block:: bash

   # Boot time breakdown
   systemd-analyze
   systemd-analyze blame
   systemd-analyze critical-chain
   
   # Generate boot chart
   systemd-analyze plot > boot.svg
   
   # Service timing
   systemd-analyze time

**BusyBox Boot Profiling:**

.. code-block:: bash

   # Add to kernel command line
   initcall_debug printk.time=y
   
   # In rcS script
   #!/bin/sh
   exec 2>/tmp/boot.log
   set -x
   
   # Analyze with grep/awk
   grep "S[0-9]" /tmp/boot.log

5.2 Optimization Strategies
----------------------------

**Parallel Startup (systemd):**

.. code-block:: ini

   # Services start in parallel by default
   # Control dependencies carefully
   [Unit]
   After=network.target
   Wants=network.target  # Weak dependency

**Socket Activation:**

.. code-block:: ini

   # Start service on-demand
   # /etc/systemd/system/myapp.socket
   [Socket]
   ListenStream=/run/myapp.sock
   
   [Install]
   WantedBy=sockets.target

**Reduce Services:**

.. code-block:: bash

   # Disable unnecessary services
   systemctl disable bluetooth
   systemctl mask bluetooth
   
   # BusyBox: Remove from init.d or chmod -x

**Filesystem Options:**

.. code-block:: bash

   # /etc/fstab - faster mounts
   /dev/mmcblk0p1 / ext4 noatime,nodiratime,data=writeback 0 1

================================================================================
6. Key Takeaways
================================================================================

.. code-block:: text

   BusyBox Init:
   =============
   /etc/inittab:
   ::sysinit:/etc/init.d/rcS
   ::respawn:/sbin/getty 115200 console
   
   Service: /etc/init.d/S50myapp
   start-stop-daemon -S -q -x /usr/bin/myapp
   
   systemd:
   ========
   Service: /etc/systemd/system/myapp.service
   [Service]
   ExecStart=/usr/bin/myapp
   Restart=on-failure
   
   Management:
   systemctl start myapp
   systemctl enable myapp
   journalctl -u myapp -f
   
   Boot Optimization:
   ==================
   systemd-analyze blame
   Socket activation
   Parallel startup
   Disable unnecessary services
   
   Selection Guide:
   ================
   Simple embedded: BusyBox init
   Complex system: systemd
   Legacy compat: SysV init

================================================================================
END OF CHEATSHEET
================================================================================
