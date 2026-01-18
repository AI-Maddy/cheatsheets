================================================================================
Embedded Linux: Root Filesystem - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 1 Ch5, Module 3 Ch5)
:Target: Embedded Linux Systems (BusyBox, systemd, Buildroot, Yocto)
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Essential Root Filesystem Commands:**

.. code-block:: bash

   # Create basic rootfs structure
   mkdir -p rootfs/{bin,sbin,lib,usr/{bin,sbin,lib},etc,proc,sys,dev,home,tmp,var,mnt,root}
   
   # Install BusyBox
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- install CONFIG_PREFIX=/path/to/rootfs
   
   # Copy libraries
   cp -a /path/to/toolchain/arm-linux-gnueabihf/libc/lib/* rootfs/lib/
   
   # Create essential device nodes
   sudo mknod -m 666 rootfs/dev/null c 1 3
   sudo mknod -m 666 rootfs/dev/console c 5 1
   sudo mknod -m 666 rootfs/dev/ttyO0 c 252 0
   
   # Pack rootfs as tar
   tar -czf rootfs.tar.gz -C rootfs .

**Filesystem Hierarchy Standard (FHS) Structure:**

.. code-block:: text

   /
   ├── bin/          # Essential user binaries (ls, cp, sh)
   ├── sbin/         # System binaries (init, mount)
   ├── lib/          # Shared libraries (libc.so.6)
   ├── usr/          # Secondary hierarchy
   │   ├── bin/      # Non-essential user binaries
   │   ├── sbin/     # Non-essential system binaries
   │   └── lib/      # Non-essential libraries
   ├── etc/          # Configuration files
   │   ├── inittab   # Init configuration
   │   ├── fstab     # Filesystem mount table
   │   ├── passwd    # User database
   │   └── init.d/   # Init scripts
   ├── dev/          # Device nodes
   ├── proc/         # Process information (virtual)
   ├── sys/          # System information (virtual)
   ├── tmp/          # Temporary files
   ├── var/          # Variable data (logs)
   ├── home/         # User home directories
   ├── root/         # Root user home
   └── mnt/          # Mount points

**Minimal Rootfs Size:**

.. code-block:: text

   Ultra minimal (static BusyBox + glibc):     ~5 MB
   Minimal with modules:                       ~15 MB
   Basic embedded system:                      ~30 MB
   Full-featured embedded:                     ~100 MB
   Desktop-like:                               ~500 MB+

================================================================================
1. Root Filesystem Fundamentals
================================================================================

1.1 What is a Root Filesystem?
-------------------------------

**Definition:**

.. code-block:: text

   Root filesystem (rootfs) is the filesystem hierarchy that:
   - Contains all files needed to boot and run the system
   - Mounted at / (root directory)
   - Provides environment for kernel and applications
   - Includes binaries, libraries, configuration files, device nodes
   
   Components:
   ✓ User-space applications and utilities
   ✓ Shared libraries (libc, libm, etc.)
   ✓ Configuration files (/etc/*)
   ✓ Device nodes (/dev/*)
   ✓ Mount points for special filesystems (/proc, /sys)
   ✓ Init system (first user-space process)

**Rootfs Types:**

.. code-block:: text

   Read-Write:
   - SD/eMMC with ext4
   - NFS (development)
   - JFFS2/UBIFS on flash
   Use case: Development, logging, user data
   
   Read-Only:
   - SquashFS
   - Compressed initramfs
   - Read-only ext4
   Use case: Production, security, reliability
   
   Hybrid:
   - Read-only root + read-write /data overlay
   Use case: Atomic updates, fail-safe operation

**Boot Process:**

.. code-block:: text

   1. Bootloader (U-Boot) loads kernel + device tree
   2. Kernel initializes hardware, drivers
   3. Kernel mounts root filesystem (from bootargs: root=/dev/mmcblk0p2)
   4. Kernel starts /sbin/init (PID 1)
   5. Init system brings up user-space services
   6. User login/application startup

1.2 Filesystem Hierarchy Standard (FHS)
----------------------------------------

**/bin - Essential User Binaries:**

.. code-block:: bash

   /bin/sh         # Shell (required by many scripts)
   /bin/ls         # List directory
   /bin/cp, mv     # File operations
   /bin/cat, echo  # Text utilities
   /bin/ps         # Process status
   /bin/mount      # Mount filesystems
   
   # Symlinked by BusyBox:
   ls -> /bin/busybox
   cp -> /bin/busybox

**/sbin - System Binaries:**

.. code-block:: bash

   /sbin/init      # Init process (PID 1)
   /sbin/getty     # Terminal login
   /sbin/ifconfig  # Network configuration
   /sbin/mount     # Mount command
   /sbin/modprobe  # Module loader
   /sbin/halt      # System shutdown

**/lib - Shared Libraries:**

.. code-block:: bash

   /lib/libc.so.6           # C library (glibc)
   /lib/libm.so.6           # Math library
   /lib/libpthread.so.0     # Threading
   /lib/ld-linux.so.3       # Dynamic linker
   /lib/modules/6.1.75/     # Kernel modules
   
   # Library dependencies (ldd)
   $ ldd /bin/busybox
   	libc.so.6 => /lib/libc.so.6
   	/lib/ld-linux.so.3

**/etc - Configuration Files:**

.. code-block:: bash

   /etc/inittab       # Init configuration
   /etc/fstab         # Filesystem mount table
   /etc/passwd        # User accounts
   /etc/group         # User groups
   /etc/shadow        # Encrypted passwords
   /etc/hostname      # System hostname
   /etc/hosts         # Static host lookup
   /etc/resolv.conf   # DNS configuration
   /etc/network/interfaces  # Network interfaces (Debian)
   /etc/init.d/       # Init scripts

**/dev - Device Nodes:**

.. code-block:: bash

   /dev/console       # System console
   /dev/null          # Null device (discard output)
   /dev/zero          # Zero device (infinite zeros)
   /dev/random        # Random number generator
   /dev/ttyO0         # Serial port (OMAP/TI)
   /dev/ttyS0         # Serial port (standard)
   /dev/mmcblk0       # SD/eMMC card
   /dev/mmcblk0p1     # SD/eMMC partition 1
   /dev/sda1          # SCSI/SATA/USB disk partition 1
   /dev/mtd0          # MTD (flash) device
   /dev/input/event0  # Input device (touchscreen, keyboard)

**/proc and /sys - Virtual Filesystems:**

.. code-block:: bash

   # /proc - Process and kernel information
   /proc/cpuinfo      # CPU information
   /proc/meminfo      # Memory statistics
   /proc/cmdline      # Kernel command line
   /proc/1/           # Process 1 (init) information
   /proc/mounts       # Currently mounted filesystems
   
   # /sys - Device and driver information
   /sys/class/net/eth0/  # Network device
   /sys/class/gpio/      # GPIO control
   /sys/devices/         # Device hierarchy
   /sys/bus/platform/    # Platform devices

**/var - Variable Data:**

.. code-block:: bash

   /var/log/          # Log files
   /var/run/          # Runtime data (PIDs)
   /var/tmp/          # Persistent temp files
   /var/cache/        # Application cache

**/usr - Secondary Hierarchy:**

.. code-block:: bash

   /usr/bin/          # Non-essential user binaries
   /usr/sbin/         # Non-essential system binaries
   /usr/lib/          # Non-essential libraries
   /usr/share/        # Architecture-independent data

1.3 Essential Files
--------------------

**/etc/inittab (BusyBox init):**

.. code-block:: text

   # /etc/inittab - init configuration
   
   # Syntax: <id>::<action>:<process>
   
   # Startup the system
   ::sysinit:/etc/init.d/rcS
   
   # Start an "askfirst" shell on the console
   ::askfirst:-/bin/sh
   
   # Start a getty on ttyO0
   ttyO0::respawn:/sbin/getty -L ttyO0 115200 vt100
   
   # Restart init on TERM signal
   ::restart:/sbin/init
   
   # Actions on shutdown
   ::shutdown:/bin/umount -a -r
   ::shutdown:/sbin/swapoff -a
   
   # Actions:
   #   sysinit   - Run once at startup
   #   respawn   - Restart if process dies
   #   askfirst  - Ask for confirmation before starting
   #   once      - Run once when runlevel entered
   #   wait      - Run and wait for completion
   #   restart   - Run when init restarts
   #   shutdown  - Run during shutdown

**/etc/fstab - Filesystem Table:**

.. code-block:: text

   # <device>       <mount point>  <type>  <options>        <dump> <pass>
   
   proc             /proc          proc    defaults         0      0
   sysfs            /sys           sysfs   defaults         0      0
   devpts           /dev/pts       devpts  mode=0620,gid=5  0      0
   tmpfs            /tmp           tmpfs   defaults         0      0
   tmpfs            /run           tmpfs   defaults         0      0
   /dev/mmcblk0p1   /boot          vfat    defaults         0      2
   /dev/mmcblk0p2   /              ext4    defaults         0      1
   /dev/mmcblk0p3   /data          ext4    defaults         0      2
   
   # Options:
   #   defaults   - rw,suid,dev,exec,auto,nouser,async
   #   noatime    - Don't update access time (faster, less writes)
   #   ro         - Read-only
   #   rw         - Read-write

**/etc/passwd - User Database:**

.. code-block:: text

   # username:password:UID:GID:comment:home:shell
   
   root:x:0:0:root:/root:/bin/sh
   daemon:x:1:1:daemon:/usr/sbin:/bin/false
   bin:x:2:2:bin:/bin:/bin/false
   nobody:x:99:99:Nobody:/:/bin/false
   user:x:1000:1000:Default User:/home/user:/bin/sh
   
   # x in password field means password in /etc/shadow

**/etc/group - Group Database:**

.. code-block:: text

   # groupname:password:GID:members
   
   root:x:0:
   daemon:x:1:
   bin:x:2:
   tty:x:5:
   disk:x:6:
   lp:x:7:
   dialout:x:20:
   sudo:x:27:user
   video:x:44:user
   audio:x:29:user
   users:x:100:

**/etc/shadow - Encrypted Passwords:**

.. code-block:: text

   # username:encrypted:lastchg:min:max:warn:inactive:expire:reserved
   
   root:$6$xyz...:18000:0:99999:7:::
   user:$6$abc...:18000:0:99999:7:::
   
   # Generate password:
   # openssl passwd -6 -salt xyz mypassword

**/etc/hostname:**

.. code-block:: text

   myboard

**/etc/hosts:**

.. code-block:: text

   127.0.0.1       localhost
   127.0.1.1       myboard
   
   192.168.1.10    server
   192.168.1.20    camera

**/etc/resolv.conf - DNS:**

.. code-block:: text

   nameserver 8.8.8.8
   nameserver 8.8.4.4
   search localdomain

================================================================================
2. BusyBox - The Swiss Army Knife
================================================================================

2.1 BusyBox Overview
--------------------

**What is BusyBox?**

.. code-block:: text

   BusyBox combines 300+ common Unix utilities into single executable:
   - Shell (ash/hush)
   - Coreutils (ls, cp, mv, cat, grep, etc.)
   - Init system
   - Network tools (ifconfig, ping, wget, etc.)
   - File system utilities (mount, tar, etc.)
   
   Benefits:
   ✓ Small size (~1-2 MB vs 30+ MB for separate utilities)
   ✓ Single binary reduces flash/RAM usage
   ✓ Sufficient for most embedded systems
   ✓ Compatible with shell scripts
   
   Trade-offs:
   ✗ Simplified options (not all GNU features)
   ✗ Single binary (can't easily replace individual tools)

**BusyBox Symlinks:**

.. code-block:: bash

   # BusyBox installs as:
   /bin/busybox
   
   # With symlinks:
   /bin/ls -> /bin/busybox
   /bin/cp -> /bin/busybox
   /bin/cat -> /bin/busybox
   # (BusyBox determines behavior from argv[0])
   
   # Manual execution:
   /bin/busybox ls -la
   /bin/busybox cat file.txt

2.2 Building BusyBox
--------------------

**Download and Configure:**

.. code-block:: bash

   # Download BusyBox
   wget https://busybox.net/downloads/busybox-1.36.1.tar.bz2
   tar xf busybox-1.36.1.tar.bz2
   cd busybox-1.36.1
   
   # Default configuration (most features enabled)
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
   
   # Menuconfig (customize)
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
   
   # Minimal configuration
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- allnoconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
   # Enable essentials: sh, ls, cp, mount, init

**Key Configuration Options:**

.. code-block:: text

   Settings
   -> Build Options
      [*] Build static binary (no shared libs)  # Self-contained
      [ ] Build shared libbusybox               # Smaller with glibc
      [*] Cross compiling
   
   Settings
   -> Installation Options
      [*] Don't use /usr
      (/bin) BusyBox installation prefix  # Install to /bin
   
   Shells
   -> Choose your default shell (ash)
      [*] ash (Advanced Bourne Shell)  # Lightweight shell
   
   Coreutils
   -> [*] ls, cp, mv, rm, cat, mkdir, touch, chmod, chown, etc.
   
   Init Utilities
   -> [*] init
      [*] Support reading an inittab file
   
   Networking Utilities
   -> [*] ifconfig, route, ping, wget, telnet
   
   Linux System Utilities
   -> [*] mount, umount, dmesg

**Build and Install:**

.. code-block:: bash

   # Build BusyBox
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   
   # Install to rootfs
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- CONFIG_PREFIX=/path/to/rootfs install
   
   # Results in:
   # /path/to/rootfs/bin/busybox
   # /path/to/rootfs/bin/ls -> busybox
   # /path/to/rootfs/bin/cp -> busybox
   # ... (hundreds of symlinks)
   
   # Verify installation
   ls -l /path/to/rootfs/bin/
   # lrwxrwxrwx 1 user user 7 Jan 18 busybox -> busybox
   # lrwxrwxrwx 1 user user 7 Jan 18 cat -> busybox
   # lrwxrwxrwx 1 user user 7 Jan 18 ls -> busybox

**Static vs Dynamic BusyBox:**

.. code-block:: bash

   # Static build (larger, no library dependencies)
   make menuconfig
   # Settings -> Build Options -> [*] Build static binary
   make -j$(nproc)
   file busybox
   # busybox: ELF 32-bit LSB executable, ARM, statically linked
   
   # Dynamic build (smaller, requires libraries)
   # Settings -> Build Options -> [ ] Build static binary
   make -j$(nproc)
   file busybox
   # busybox: ELF 32-bit LSB executable, ARM, dynamically linked
   ldd busybox
   # libc.so.6 => /lib/libc.so.6
   # /lib/ld-linux.so.3

2.3 BusyBox Applets
-------------------

**Essential Applets:**

.. code-block:: bash

   # File operations
   ls, cp, mv, rm, mkdir, rmdir, touch, cat, more, less, head, tail
   chmod, chown, chgrp, ln, find, grep, sed, awk, cut, sort, uniq
   
   # System utilities
   mount, umount, df, du, ps, top, kill, killall, free, uptime, dmesg
   
   # Shell
   ash, sh, echo, test, [, [[, expr
   
   # Init
   init, getty, login
   
   # Networking
   ifconfig, route, ping, wget, telnet, ftpget, ftpput, nc, traceroute
   
   # Archiving
   tar, gzip, gunzip, bzip2, bunzip2, unzip, cpio
   
   # Text editing
   vi, sed
   
   # Process management
   pidof, pgrep, pkill, renice

**List Available Applets:**

.. code-block:: bash

   # List all compiled applets
   busybox --list
   # [
   # [[
   # acpid
   # addgroup
   # adduser
   # ...
   
   # Count applets
   busybox --list | wc -l
   # 385

================================================================================
3. Creating Root Filesystem
================================================================================

3.1 Manual Rootfs Creation
---------------------------

**Step 1: Create Directory Structure:**

.. code-block:: bash

   # Set rootfs path
   export ROOTFS=/path/to/rootfs
   
   # Create FHS directories
   mkdir -p $ROOTFS/{bin,sbin,lib,usr/{bin,sbin,lib},etc,proc,sys,dev,home,tmp,var,mnt,root,boot}
   
   # Create /var subdirectories
   mkdir -p $ROOTFS/var/{log,run,lock,cache}
   
   # Create /etc subdirectories
   mkdir -p $ROOTFS/etc/{init.d,network,sysconfig}
   
   # Create device directories
   mkdir -p $ROOTFS/dev/{pts,shm}
   
   # Set permissions
   chmod 1777 $ROOTFS/tmp  # Sticky bit
   chmod 0755 $ROOTFS/root
   chmod 0755 $ROOTFS/etc

**Step 2: Install BusyBox:**

.. code-block:: bash

   # Build and install BusyBox (as shown in section 2.2)
   cd busybox-1.36.1
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- CONFIG_PREFIX=$ROOTFS install

**Step 3: Copy Libraries:**

.. code-block:: bash

   # Find toolchain sysroot
   arm-linux-gnueabihf-gcc -print-sysroot
   # /path/to/toolchain/arm-linux-gnueabihf/libc
   
   # Copy runtime libraries
   export SYSROOT=$(arm-linux-gnueabihf-gcc -print-sysroot)
   
   cp -a $SYSROOT/lib/* $ROOTFS/lib/
   cp -a $SYSROOT/usr/lib/* $ROOTFS/usr/lib/
   
   # Or copy only required libraries
   cp $SYSROOT/lib/ld-linux.so.3 $ROOTFS/lib/
   cp $SYSROOT/lib/libc.so.6 $ROOTFS/lib/
   cp $SYSROOT/lib/libm.so.6 $ROOTFS/lib/
   cp $SYSROOT/lib/libpthread.so.0 $ROOTFS/lib/
   
   # Strip libraries to reduce size
   arm-linux-gnueabihf-strip $ROOTFS/lib/*.so*

**Step 4: Create Device Nodes:**

.. code-block:: bash

   # Create essential device nodes (requires root)
   sudo mknod -m 666 $ROOTFS/dev/null c 1 3
   sudo mknod -m 666 $ROOTFS/dev/zero c 1 5
   sudo mknod -m 666 $ROOTFS/dev/random c 1 8
   sudo mknod -m 666 $ROOTFS/dev/urandom c 1 9
   sudo mknod -m 666 $ROOTFS/dev/console c 5 1
   sudo mknod -m 666 $ROOTFS/dev/tty c 5 0
   
   # Serial ports
   sudo mknod -m 666 $ROOTFS/dev/ttyO0 c 252 0  # OMAP UART
   sudo mknod -m 666 $ROOTFS/dev/ttyS0 c 4 64   # Standard serial
   
   # SD/MMC (if not using udev/mdev)
   sudo mknod -m 660 $ROOTFS/dev/mmcblk0 b 179 0
   sudo mknod -m 660 $ROOTFS/dev/mmcblk0p1 b 179 1
   sudo mknod -m 660 $ROOTFS/dev/mmcblk0p2 b 179 2
   
   # Alternative: Use mdev/udev to create devices dynamically

**Step 5: Create Configuration Files:**

.. code-block:: bash

   # /etc/inittab
   cat > $ROOTFS/etc/inittab << 'EOF'
   ::sysinit:/etc/init.d/rcS
   ::askfirst:-/bin/sh
   ttyO0::respawn:/sbin/getty -L ttyO0 115200 vt100
   ::shutdown:/bin/umount -a -r
   EOF
   
   # /etc/init.d/rcS
   mkdir -p $ROOTFS/etc/init.d
   cat > $ROOTFS/etc/init.d/rcS << 'EOF'
   #!/bin/sh
   
   # Mount proc, sys, devpts
   mount -t proc none /proc
   mount -t sysfs none /sys
   mount -t devpts none /dev/pts
   
   # Mount all filesystems in /etc/fstab
   mount -a
   
   # Configure network
   ifconfig lo 127.0.0.1
   
   # Start mdev for dynamic device creation
   echo /sbin/mdev > /proc/sys/kernel/hotplug
   mdev -s
   
   # Set hostname
   hostname -F /etc/hostname
   
   echo "System initialization complete"
   EOF
   chmod +x $ROOTFS/etc/init.d/rcS
   
   # /etc/fstab
   cat > $ROOTFS/etc/fstab << 'EOF'
   proc    /proc   proc    defaults    0   0
   sysfs   /sys    sysfs   defaults    0   0
   devpts  /dev/pts devpts mode=0620,gid=5 0 0
   tmpfs   /tmp    tmpfs   defaults    0   0
   EOF
   
   # /etc/passwd
   cat > $ROOTFS/etc/passwd << 'EOF'
   root:x:0:0:root:/root:/bin/sh
   nobody:x:99:99:Nobody:/:/bin/false
   EOF
   
   # /etc/group
   cat > $ROOTFS/etc/group << 'EOF'
   root:x:0:
   users:x:100:
   EOF
   
   # /etc/hostname
   echo "myboard" > $ROOTFS/etc/hostname
   
   # /etc/hosts
   cat > $ROOTFS/etc/hosts << 'EOF'
   127.0.0.1   localhost
   127.0.1.1   myboard
   EOF

**Step 6: Package Rootfs:**

.. code-block:: bash

   # Create tarball
   cd $ROOTFS
   tar -czf ../rootfs.tar.gz .
   
   # Or create ext4 image
   dd if=/dev/zero of=rootfs.ext4 bs=1M count=512
   mkfs.ext4 rootfs.ext4
   sudo mount -o loop rootfs.ext4 /mnt
   sudo cp -a $ROOTFS/* /mnt/
   sudo umount /mnt

3.2 Buildroot-Generated Rootfs
-------------------------------

**Using Buildroot:**

.. code-block:: bash

   # Download Buildroot
   wget https://buildroot.org/downloads/buildroot-2024.02.tar.gz
   tar xf buildroot-2024.02.tar.gz
   cd buildroot-2024.02
   
   # Configure for target (e.g., BeagleBone Black)
   make beaglebone_defconfig
   
   # Customize
   make menuconfig
   # Target options
   #   -> Target Architecture: ARM (little endian)
   #   -> Target Architecture Variant: cortex-A8
   # Toolchain
   #   -> Custom toolchain or Buildroot toolchain
   # System configuration
   #   -> /dev management: Dynamic using devtmpfs + mdev
   #   -> Root password: set password
   # Filesystem images
   #   -> [*] tar the root filesystem
   #   -> [*] ext2/3/4 root filesystem
   
   # Build
   make -j$(nproc)
   # Output: output/images/rootfs.tar
   #         output/images/rootfs.ext4

**Buildroot Output:**

.. code-block:: bash

   # Rootfs location
   ls output/images/
   # rootfs.tar
   # rootfs.ext4
   # zImage
   # am335x-boneblack.dtb
   
   # Extract and examine
   mkdir rootfs
   tar -xf output/images/rootfs.tar -C rootfs/
   ls rootfs/
   # bin  boot  dev  etc  lib  media  mnt  opt  proc  root  run  sbin  sys  tmp  usr  var

3.3 Yocto-Generated Rootfs
---------------------------

**Yocto Build:**

.. code-block:: bash

   # Setup Yocto (see Yocto Build System cheatsheet)
   # After build:
   ls tmp/deploy/images/beaglebone/
   # core-image-minimal-beaglebone.tar.bz2
   # core-image-minimal-beaglebone.ext4
   
   # Extract
   mkdir rootfs
   tar -xf core-image-minimal-beaglebone.tar.bz2 -C rootfs/

================================================================================
4. Init Systems
================================================================================

4.1 BusyBox Init
----------------

**Inittab Format:**

.. code-block:: text

   # Syntax: <id>::<action>:<process>
   
   # <id>: Terminal (tty1, ttyO0) or empty for system-wide
   # <action>: sysinit, respawn, askfirst, once, wait, restart, shutdown, ctrlaltdel
   # <process>: Command to execute

**Common Inittab:**

.. code-block:: text

   # System initialization
   ::sysinit:/etc/init.d/rcS
   
   # Start shells
   ::askfirst:-/bin/sh
   ttyO0::respawn:/sbin/getty -L ttyO0 115200 vt100
   tty1::respawn:/sbin/getty -L tty1 115200 vt100
   
   # Logging
   ::respawn:/sbin/syslogd -n
   ::respawn:/sbin/klogd -n
   
   # Stuff to do before rebooting
   ::shutdown:/etc/init.d/rcK
   ::shutdown:/bin/umount -a -r
   ::restart:/sbin/init
   
   # Ctrl-Alt-Del
   ::ctrlaltdel:/sbin/reboot

**Init Scripts:**

.. code-block:: bash

   # /etc/init.d/rcS - Startup script
   #!/bin/sh
   
   # Mount virtual filesystems
   mount -t proc proc /proc
   mount -t sysfs sysfs /sys
   mount -t devtmpfs devtmpfs /dev
   
   # Run init scripts
   for script in /etc/init.d/S*; do
       [ -x "$script" ] && $script start
   done
   
   # Set hostname
   hostname -F /etc/hostname 2>/dev/null
   
   # Configure network
   ifconfig lo 127.0.0.1 up
   
   # Start mdev
   echo /sbin/mdev > /proc/sys/kernel/hotplug
   mdev -s

**Service Scripts:**

.. code-block:: bash

   # /etc/init.d/S40network
   #!/bin/sh
   
   case "$1" in
       start)
           echo "Starting network..."
           ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up
           route add default gw 192.168.1.1
           ;;
       stop)
           echo "Stopping network..."
           ifconfig eth0 down
           ;;
       restart)
           $0 stop
           $0 start
           ;;
       *)
           echo "Usage: $0 {start|stop|restart}"
           exit 1
   esac

4.2 systemd (Advanced Embedded)
--------------------------------

**systemd on Embedded:**

.. code-block:: text

   Pros:
   ✓ Fast parallel service startup
   ✓ Dependency management
   ✓ Advanced logging (journald)
   ✓ Socket/D-Bus activation
   ✓ Modern, actively developed
   
   Cons:
   ✗ Larger footprint (~10 MB vs ~200 KB for BusyBox init)
   ✗ More dependencies
   ✗ Higher memory usage
   ✗ Complexity overhead
   
   Use case: Full-featured embedded Linux (automotive IVI, industrial HMI)

**Basic systemd Service:**

.. code-block:: ini

   # /etc/systemd/system/myapp.service
   [Unit]
   Description=My Application
   After=network.target
   
   [Service]
   Type=simple
   ExecStart=/usr/bin/myapp
   Restart=on-failure
   RestartSec=5s
   
   [Install]
   WantedBy=multi-user.target

**systemd Commands:**

.. code-block:: bash

   # Enable/start service
   systemctl enable myapp
   systemctl start myapp
   
   # Status
   systemctl status myapp
   
   # Logs
   journalctl -u myapp -f

================================================================================
5. Device Management
================================================================================

5.1 Static Device Nodes
------------------------

**Manual Creation:**

.. code-block:: bash

   # Syntax: mknod <name> <type> <major> <minor>
   # type: c (character), b (block)
   
   # Character devices
   sudo mknod /dev/null c 1 3
   sudo mknod /dev/console c 5 1
   sudo mknod /dev/ttyO0 c 252 0
   
   # Block devices
   sudo mknod /dev/mmcblk0 b 179 0
   sudo mknod /dev/mmcblk0p1 b 179 1
   
   # Find major/minor numbers
   ls -l /dev/
   # crw-rw-rw- 1 root root 1, 3 Jan 18 null
   #             major^ ^minor

5.2 Dynamic Device Management (mdev)
-------------------------------------

**BusyBox mdev:**

.. code-block:: bash

   # Enable mdev hotplugging
   echo /sbin/mdev > /proc/sys/kernel/hotplug
   
   # Populate /dev
   mdev -s
   
   # mdev.conf for custom rules
   # /etc/mdev.conf
   # Syntax: <device regex> <uid>:<gid> <permissions> [=path] [@|$|*<command>]
   
   # GPIO
   gpiochip[0-9]*  root:root 660
   
   # Input devices
   event[0-9]*     root:root 660 =input/
   
   # Network
   net/.*          root:root 660 @/etc/mdev/net.sh
   
   # Storage (auto-mount)
   sd[a-z][0-9]*   0:6 660 @/etc/mdev/storage-add.sh
   sd[a-z]         0:6 660 $/etc/mdev/storage-remove.sh

**mdev Mount Script:**

.. code-block:: bash

   # /etc/mdev/storage-add.sh
   #!/bin/sh
   # Auto-mount USB storage
   
   MOUNT_POINT="/mnt/$MDEV"
   
   mkdir -p "$MOUNT_POINT"
   mount -t auto "/dev/$MDEV" "$MOUNT_POINT"

5.3 udev (Full-featured)
-------------------------

**udev on Embedded:**

.. code-block:: bash

   # Larger but more powerful than mdev
   # Usually part of systemd
   
   # udev rule example
   # /etc/udev/rules.d/99-gpio.rules
   SUBSYSTEM=="gpio", KERNEL=="gpiochip*", MODE="0660", GROUP="gpio"
   
   # Auto-mount USB
   # /etc/udev/rules.d/99-usb-mount.rules
   ACTION=="add", KERNEL=="sd[a-z][0-9]", RUN+="/usr/local/bin/usb-mount.sh"

================================================================================
6. Networking Configuration
================================================================================

6.1 Network Interface Configuration
------------------------------------

**ifconfig Method:**

.. code-block:: bash

   # Configure IP address
   ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up
   
   # Add default route
   route add default gw 192.168.1.1
   
   # Configure DNS
   echo "nameserver 8.8.8.8" > /etc/resolv.conf
   
   # DHCP client
   udhcpc -i eth0  # BusyBox DHCP client

**ip Command (modern):**

.. code-block:: bash

   # Set IP address
   ip addr add 192.168.1.100/24 dev eth0
   ip link set eth0 up
   
   # Add default route
   ip route add default via 192.168.1.1
   
   # Show configuration
   ip addr show
   ip route show

**/etc/network/interfaces (Debian-style):**

.. code-block:: text

   # Loopback
   auto lo
   iface lo inet loopback
   
   # Static IP
   auto eth0
   iface eth0 inet static
       address 192.168.1.100
       netmask 255.255.255.0
       gateway 192.168.1.1
       dns-nameservers 8.8.8.8 8.8.4.4
   
   # DHCP
   auto eth0
   iface eth0 inet dhcp
   
   # WiFi (with wpa_supplicant)
   auto wlan0
   iface wlan0 inet dhcp
       wpa-conf /etc/wpa_supplicant.conf

**Startup Script:**

.. code-block:: bash

   # /etc/init.d/S40network
   #!/bin/sh
   
   case "$1" in
       start)
           echo "Configuring network..."
           ifconfig lo 127.0.0.1 up
           ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up
           route add default gw 192.168.1.1
           ;;
       stop)
           ifconfig eth0 down
           ;;
       restart)
           $0 stop
           sleep 1
           $0 start
           ;;
       *)
           echo "Usage: $0 {start|stop|restart}"
           exit 1
   esac

6.2 WiFi Configuration
-----------------------

**wpa_supplicant:**

.. code-block:: bash

   # /etc/wpa_supplicant.conf
   ctrl_interface=/var/run/wpa_supplicant
   update_config=1
   
   network={
       ssid="MyWiFi"
       psk="password123"
       key_mgmt=WPA-PSK
   }
   
   # Start wpa_supplicant
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
   
   # Get IP via DHCP
   udhcpc -i wlan0

**Generate PSK:**

.. code-block:: bash

   # Generate encrypted PSK
   wpa_passphrase "MyWiFi" "password123"
   # network={
   #     ssid="MyWiFi"
   #     #psk="password123"
   #     psk=59e0d07fa4c7741797a4e394f38a5c321e3bed51d54ad5fcbd3f84bc7415d73d
   # }

================================================================================
7. Storage and Filesystem Types
================================================================================

7.1 Filesystem Types for Embedded
----------------------------------

**ext4 (SD/eMMC):**

.. code-block:: text

   Pros:
   ✓ Journaling (crash recovery)
   ✓ Large file support
   ✓ Good performance
   ✓ Well-supported
   
   Cons:
   ✗ Not optimal for flash wear leveling
   ✗ Larger overhead than simpler filesystems
   
   Use case: SD card, eMMC, USB storage
   
   Mount options:
   - noatime: Don't update access time (reduce writes)
   - data=writeback: Faster, less safe
   - data=journal: Safer, slower

**SquashFS (Read-Only):**

.. code-block:: text

   Pros:
   ✓ High compression (60-70%)
   ✓ Read-only = no corruption
   ✓ Fast read access
   ✓ Low RAM usage
   
   Cons:
   ✗ Cannot modify
   ✗ Must rebuild for changes
   
   Use case: Production root filesystem, /usr partition

**UBIFS (NAND Flash):**

.. code-block:: text

   Pros:
   ✓ Flash-friendly (wear leveling)
   ✓ Compression
   ✓ Fast mount time
   
   Cons:
   ✗ Complex setup
   ✗ Requires UBI layer
   
   Use case: Raw NAND flash storage

**JFFS2 (NOR Flash):**

.. code-block:: text

   Pros:
   ✓ Designed for NOR flash
   ✓ Wear leveling
   ✓ Compression
   
   Cons:
   ✗ Slow mount time (scans entire flash)
   ✗ Not recommended for NAND
   
   Use case: Small NOR flash

**tmpfs (RAM):**

.. code-block:: text

   Pros:
   ✓ Very fast (RAM speed)
   ✓ No flash wear
   
   Cons:
   ✗ Data lost on reboot
   ✗ Uses RAM
   
   Use case: /tmp, /var/run, /var/lock

**Comparison:**

.. code-block:: text

   Filesystem  Storage      Read-Write  Flash-Aware  Compression  Use Case
   =========================================================================
   ext4        SD/eMMC/HDD  RW          No           No           General purpose
   SquashFS    Any          RO          No           Yes          Production rootfs
   UBIFS       NAND Flash   RW          Yes          Yes          NAND storage
   JFFS2       NOR Flash    RW          Yes          Yes          NOR storage
   tmpfs       RAM          RW          N/A          No           Temporary files
   NFS         Network      RW          N/A          No           Development

7.2 Creating Filesystems
-------------------------

**ext4:**

.. code-block:: bash

   # Create ext4 image
   dd if=/dev/zero of=rootfs.ext4 bs=1M count=512
   mkfs.ext4 -L rootfs rootfs.ext4
   
   # Mount and populate
   sudo mount -o loop rootfs.ext4 /mnt
   sudo cp -a rootfs/* /mnt/
   sudo umount /mnt
   
   # Or create on SD card partition
   sudo mkfs.ext4 -L rootfs /dev/mmcblk0p2
   sudo mount /dev/mmcblk0p2 /mnt
   sudo cp -a rootfs/* /mnt/
   sudo umount /mnt

**SquashFS:**

.. code-block:: bash

   # Create squashfs from directory
   mksquashfs rootfs/ rootfs.squashfs -comp xz -b 256K
   
   # -comp: Compression (gzip, lzma, lzo, xz, zstd)
   # -b: Block size (larger = better compression, slower)
   
   # Mount (read-only)
   sudo mount -t squashfs rootfs.squashfs /mnt
   
   # Hybrid: SquashFS root + tmpfs overlay
   mount -t squashfs rootfs.squashfs /mnt/lower
   mount -t tmpfs tmpfs /mnt/upper
   mount -t overlay overlay -o lowerdir=/mnt/lower,upperdir=/mnt/upper,workdir=/mnt/work /mnt/merged

**UBIFS:**

.. code-block:: bash

   # Create UBIFS image
   mkfs.ubifs -r rootfs/ -m 2048 -e 126976 -c 1024 -o rootfs.ubifs
   # -r: Root directory
   # -m: Minimum I/O size (NAND page size)
   # -e: Logical erase block size
   # -c: Maximum LEB count
   
   # Create UBI volume
   ubinize -o ubi.img -m 2048 -p 128KiB ubinize.cfg
   
   # ubinize.cfg:
   [ubifs]
   mode=ubi
   image=rootfs.ubifs
   vol_id=0
   vol_size=50MiB
   vol_type=dynamic
   vol_name=rootfs
   vol_flags=autoresize

**initramfs (Built into kernel):**

.. code-block:: bash

   # Create cpio archive
   cd rootfs
   find . | cpio -o -H newc | gzip > ../initramfs.cpio.gz
   
   # Configure kernel to include initramfs
   make menuconfig
   # General setup
   #   -> [*] Initial RAM filesystem and RAM disk
   #      -> Initramfs source file(s): /path/to/initramfs.cpio.gz
   
   # Rebuild kernel (initramfs embedded)
   make zImage

================================================================================
8. Optimizing Root Filesystem
================================================================================

8.1 Size Reduction Techniques
------------------------------

**Strip Binaries and Libraries:**

.. code-block:: bash

   # Strip all executables
   find rootfs/ -type f -executable -exec arm-linux-gnueabihf-strip {} \;
   
   # Strip libraries
   find rootfs/lib rootfs/usr/lib -name "*.so*" -exec arm-linux-gnueabihf-strip {} \;
   
   # Size comparison:
   # Before: libc.so.6 = 1.8 MB
   # After:  libc.so.6 = 1.2 MB (33% reduction)

**Remove Unnecessary Files:**

.. code-block:: bash

   # Remove documentation
   rm -rf rootfs/usr/share/{man,doc,info}
   
   # Remove headers (not needed at runtime)
   rm -rf rootfs/usr/include
   
   # Remove static libraries (keep only .so)
   find rootfs/ -name "*.a" -delete
   
   # Remove locale files (keep only needed locales)
   rm -rf rootfs/usr/share/locale/*
   # Or keep English only:
   find rootfs/usr/share/locale -mindepth 1 -maxdepth 1 ! -name 'en*' -exec rm -rf {} \;

**Use musl libc (smaller alternative to glibc):**

.. code-block:: bash

   # musl libc is significantly smaller
   # glibc: ~2 MB
   # musl:  ~600 KB
   
   # Build toolchain with musl
   # (Crosstool-NG, Buildroot support musl)

**Compress with UPX (for executables):**

.. code-block:: bash

   # UPX compresses executables (50-70% reduction)
   upx --best rootfs/bin/busybox
   # Original:   1.2 MB
   # Compressed: 450 KB

**Minimal BusyBox Configuration:**

.. code-block:: bash

   # Disable unnecessary applets
   make menuconfig
   # Disable: vi, awk, sed (if not needed)
   # Keep: sh, ls, cp, mount, init, ifconfig
   
   # Result: BusyBox ~200 KB vs 1.2 MB full-featured

8.2 Minimal Rootfs Example
---------------------------

**Ultra-Minimal Rootfs (5 MB):**

.. code-block:: text

   Structure:
   /bin/busybox (static)           800 KB
   /lib/libc.so.6                  1.2 MB
   /lib/libm.so.6                  500 KB
   /lib/ld-linux.so.3              150 KB
   /etc/{inittab,fstab,passwd}     5 KB
   /dev/{console,null,ttyO0}       -
   /proc, /sys, /tmp (empty)       -
   
   Total: ~5 MB

**Script to Create Minimal Rootfs:**

.. code-block:: bash

   #!/bin/bash
   
   ROOTFS=minimal-rootfs
   BUSYBOX=/path/to/busybox  # Static busybox binary
   SYSROOT=$(arm-linux-gnueabihf-gcc -print-sysroot)
   
   # Create structure
   mkdir -p $ROOTFS/{bin,lib,etc,proc,sys,dev,tmp}
   
   # Install static BusyBox
   cp $BUSYBOX $ROOTFS/bin/busybox
   chmod +x $ROOTFS/bin/busybox
   
   # Create symlinks
   for applet in sh init mount umount ls cat echo; do
       ln -s busybox $ROOTFS/bin/$applet
   done
   
   # Copy minimal libraries (if BusyBox is dynamic)
   # cp $SYSROOT/lib/{libc.so.6,libm.so.6,ld-linux.so.3} $ROOTFS/lib/
   
   # Create device nodes
   sudo mknod -m 666 $ROOTFS/dev/null c 1 3
   sudo mknod -m 666 $ROOTFS/dev/console c 5 1
   
   # Create inittab
   cat > $ROOTFS/etc/inittab << 'EOF'
   ::sysinit:/bin/mount -t proc proc /proc
   ::sysinit:/bin/mount -t sysfs sysfs /sys
   ::askfirst:-/bin/sh
   ::shutdown:/bin/umount -a -r
   EOF
   
   # Package
   tar -czf minimal-rootfs.tar.gz -C $ROOTFS .
   
   echo "Minimal rootfs created: $(du -sh $ROOTFS)"

================================================================================
9. Troubleshooting Root Filesystem
================================================================================

9.1 Common Boot Issues
----------------------

**Kernel panic: VFS: Unable to mount root fs:**

.. code-block:: text

   Causes:
   - Wrong root= parameter
   - Missing filesystem driver in kernel
   - Corrupted filesystem
   - Device not ready (SD card needs rootwait)
   
   Solutions:
   1. Check bootargs: root=/dev/mmcblk0p2 rootwait
   2. Enable filesystem in kernel: CONFIG_EXT4_FS=y
   3. Add rootdelay=5 to bootargs
   4. Try different root device (/dev/mmcblk0p2, /dev/sda1)
   
   Debug:
   # Add to bootargs:
   earlyprintk debug

**Kernel panic: No init found:**

.. code-block:: text

   Causes:
   - Missing /sbin/init
   - Wrong init binary (wrong architecture)
   - Missing library dependencies
   
   Solutions:
   1. Verify /sbin/init exists and is executable
   2. Check architecture: file rootfs/sbin/init
   3. Check dependencies: ldd rootfs/sbin/init
   4. Try init=/bin/sh to get emergency shell

**Kernel panic: Attempted to kill init:**

.. code-block:: text

   Causes:
   - Init process crashed
   - Missing libraries
   - Corrupted binary
   
   Solutions:
   1. Boot with init=/bin/sh
   2. Check /sbin/init manually
   3. Review init logs

**Failing to start getty/shell:**

.. code-block:: text

   Causes:
   - Wrong console device in inittab
   - Missing /dev/console or /dev/ttyO0
   
   Solutions:
   1. Check inittab console line matches kernel console= parameter
   2. Create device nodes
   3. Use mdev/udev for dynamic device creation

9.2 Debugging Techniques
-------------------------

**Emergency Shell:**

.. code-block:: bash

   # Boot with emergency shell
   # In U-Boot bootargs:
   setenv bootargs 'console=ttyO0,115200 root=/dev/mmcblk0p2 init=/bin/sh'
   
   # Once in shell:
   mount -t proc proc /proc
   mount -t sysfs sysfs /sys
   
   # Check filesystem
   ls /
   ls /bin
   
   # Test init
   /sbin/init

**Check Library Dependencies:**

.. code-block:: bash

   # On host (cross-compiled binary)
   arm-linux-gnueabihf-readelf -d rootfs/bin/busybox | grep NEEDED
   # 0x00000001 (NEEDED)     Shared library: [libc.so.6]
   
   # Check if libraries exist in rootfs
   ls -l rootfs/lib/libc.so.6

**Verify File System:**

.. code-block:: bash

   # Check ext4 filesystem
   e2fsck -f rootfs.ext4
   
   # Check mounted filesystem
   mount -o loop rootfs.ext4 /mnt
   ls -la /mnt

**Enable Kernel Debug Messages:**

.. code-block:: bash

   # Bootargs
   setenv bootargs 'console=ttyO0,115200 root=/dev/mmcblk0p2 earlyprintk debug loglevel=8'
   
   # Shows detailed kernel messages during boot

================================================================================
10. Exam-Style Questions
================================================================================

**Q1:** What are the essential directories in a root filesystem?

**A:** /bin (binaries), /sbin (system binaries), /lib (libraries), /etc
(configuration), /dev (devices), /proc (virtual), /sys (virtual), /tmp, /var.

**Q2:** What is BusyBox and why is it used in embedded systems?

**A:** BusyBox combines 300+ Unix utilities into single executable (~1-2 MB),
reducing flash/RAM usage. Ideal for embedded systems with limited resources.

**Q3:** How do you create a basic inittab for BusyBox init?

**A:**
.. code-block:: text

   ::sysinit:/etc/init.d/rcS
   ::askfirst:-/bin/sh
   ttyO0::respawn:/sbin/getty -L ttyO0 115200 vt100
   ::shutdown:/bin/umount -a -r

**Q4:** What is the difference between static and dynamic device nodes?

**A:** Static: Created manually with mknod, fixed. Dynamic: Created by
mdev/udev based on hardware detection, flexible, automatic.

**Q5:** What filesystem is best for read-only root on embedded Linux?

**A:** SquashFS - high compression, fast read access, prevents corruption.

**Q6:** How do you create ext4 filesystem image from directory?

**A:**
.. code-block:: bash

   dd if=/dev/zero of=rootfs.ext4 bs=1M count=512
   mkfs.ext4 rootfs.ext4
   sudo mount -o loop rootfs.ext4 /mnt
   sudo cp -a rootfs/* /mnt/
   sudo umount /mnt

**Q7:** What is the purpose of /etc/fstab?

**A:** Defines filesystems to mount at boot (device, mount point, type,
options). Used by "mount -a" command.

**Q8:** How to configure static IP address at boot?

**A:** In /etc/init.d/rcS or service script:
`ifconfig eth0 192.168.1.100 netmask 255.255.255.0 up`
`route add default gw 192.168.1.1`

**Q9:** What causes "Kernel panic: No init found"?

**A:** Missing /sbin/init, wrong architecture binary, or missing library
dependencies. Fix: Verify init exists, check with ldd, try init=/bin/sh.

**Q10:** How to reduce root filesystem size?

**A:** Strip binaries/libraries, remove documentation, use static BusyBox,
minimal BusyBox config, compress with UPX, use musl instead of glibc.

================================================================================
11. Key Takeaways
================================================================================

.. code-block:: text

   Essential Structure (FHS):
   ==========================
   /bin, /sbin, /lib - Binaries and libraries
   /etc - Configuration (inittab, fstab, passwd)
   /dev - Device nodes
   /proc, /sys - Virtual filesystems (kernel interface)
   /tmp, /var - Temporary and variable data
   
   BusyBox:
   ========
   - 300+ utilities in ~1-2 MB
   - Static or dynamic linking
   - Sufficient for most embedded systems
   
   Creating Rootfs:
   ================
   1. Create directory structure
   2. Install BusyBox
   3. Copy libraries (from toolchain sysroot)
   4. Create device nodes (or use mdev/udev)
   5. Create config files (inittab, fstab, passwd)
   6. Package (tar/ext4/squashfs)
   
   Init Systems:
   =============
   BusyBox init: Lightweight, inittab-based
   systemd: Advanced, parallel startup, larger footprint
   
   Filesystem Types:
   =================
   ext4:     SD/eMMC, read-write
   SquashFS: Read-only, compressed
   UBIFS:    NAND flash, wear-leveling
   tmpfs:    RAM-based, temporary
   NFS:      Network, development
   
   Size Optimization:
   ==================
   - Strip binaries: arm-linux-gnueabihf-strip
   - Remove docs: /usr/share/{man,doc}
   - Static BusyBox: No library dependencies
   - Minimal config: Only needed applets
   Result: 5-15 MB minimal rootfs
   
   Common Issues:
   ==============
   - "Unable to mount root fs": Check root= parameter, enable filesystem driver
   - "No init found": Verify /sbin/init exists, check dependencies
   - No console: Create /dev/console, match inittab with bootargs console=
   
   Device Management:
   ==================
   Static:  mknod /dev/null c 1 3
   Dynamic: mdev -s (BusyBox) or udev (full-featured)

================================================================================
END OF CHEATSHEET
================================================================================