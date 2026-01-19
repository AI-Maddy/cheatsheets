================================================================================
Embedded Linux: Master Index & Quick Reference
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Complete Embedded Linux Development Guide
:Coverage: All 15 Cheatsheets
:Version: 1.0

================================================================================
Quick Navigation
================================================================================

**Available Cheatsheets:**

1. Toolchains & Cross-Compilation
2. Bootloaders (U-Boot)
3. Kernel Configuration & Building
4. Root Filesystem
5. Yocto Build System
6. BSP Layer Development
7. Application Development
8. Storage & Filesystems
9. Device Drivers
10. Init Systems & Services
11. Process & Memory Management
12. Debugging & Profiling
13. Real-Time Programming
14. Security & Hardening
15. Master Index & Reference (this document)

================================================================================
Essential Commands Quick Reference
================================================================================

**Cross-Compilation:**

.. code-block:: bash

   export CROSS_COMPILE=arm-linux-gnueabihf-
   export CC=${CROSS_COMPILE}gcc
   export ARCH=arm
   source /opt/poky/environment-setup-*

**U-Boot:**

.. code-block:: bash

   # Build
   make <board>_defconfig
   make CROSS_COMPILE=arm-linux-gnueabihf-
   
   # Commands
   printenv; setenv; saveenv
   tftp ${loadaddr} zImage
   bootz ${loadaddr} - ${fdt_addr}
   nand erase.chip; nand write ${loadaddr} 0 ${filesize}

**Kernel:**

.. code-block:: bash

   # Configure
   make ARCH=arm menuconfig
   make ARCH=arm savedefconfig
   
   # Build
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- dtbs
   
   # Modules
   make ARCH=arm modules
   make ARCH=arm INSTALL_MOD_PATH=/path/to/rootfs modules_install

**Yocto/BitBake:**

.. code-block:: bash

   # Setup
   source oe-init-build-env
   bitbake <image-name>
   
   # Tasks
   bitbake -c fetch <recipe>
   bitbake -c compile <recipe>
   bitbake -c clean <recipe>
   bitbake -c devshell <recipe>
   
   # SDK
   bitbake -c populate_sdk <image>

**Root Filesystem:**

.. code-block:: bash

   # BusyBox
   make defconfig
   make menuconfig
   make install
   
   # Create rootfs
   mkdir -p rootfs/{bin,sbin,etc,proc,sys,dev,lib,usr,tmp,var}
   cp -a busybox/_install/* rootfs/

**MTD/UBI:**

.. code-block:: bash

   # MTD
   cat /proc/mtd
   flash_erase /dev/mtd2 0 0
   nandwrite -p /dev/mtd2 image.bin
   
   # UBI
   ubiformat /dev/mtd2
   ubiattach -p /dev/mtd2
   ubimkvol /dev/ubi0 -N rootfs -m
   mount -t ubifs ubi0:rootfs /mnt

**systemd:**

.. code-block:: bash

   systemctl start <service>
   systemctl enable <service>
   systemctl status <service>
   journalctl -u <service> -f

**Process Management:**

.. code-block:: bash

   ps aux; top; htop
   nice -n 10 <cmd>
   renice -n 5 -p <pid>
   chrt -f -p 80 <pid>
   taskset -c 0,1 <cmd>

**Debugging:**

.. code-block:: bash

   # GDB
   gdbserver :1234 ./app
   arm-linux-gdb ./app
   (gdb) target remote 192.168.1.10:1234
   
   # strace/ltrace
   strace -e open,read,write ./app
   ltrace ./app
   
   # perf
   perf record -g ./app
   perf report

**Real-Time:**

.. code-block:: bash

   chrt -f 80 ./rt-app
   cyclictest -p 80 -t4 -n -i 1000 -l 100000
   mlockall(MCL_CURRENT | MCL_FUTURE)

**Security:**

.. code-block:: bash

   # Firewall
   iptables -P INPUT DROP
   iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT
   
   # Encryption
   cryptsetup luksFormat /dev/mmcblk0p2
   cryptsetup luksOpen /dev/mmcblk0p2 cryptroot
   
   # SELinux
   sestatus; getenforce; setenforce 1

================================================================================
Configuration Files Reference
================================================================================

**/etc/inittab (BusyBox):**

.. code-block:: bash

   ::sysinit:/etc/init.d/rcS
   ::respawn:/sbin/getty 115200 console
   ::shutdown:/bin/umount -a -r

**/etc/fstab:**

.. code-block:: bash

   /dev/mmcblk0p1  /boot  ext4  defaults,ro  0  2
   /dev/mmcblk0p2  /      ext4  defaults,noatime  0  1
   tmpfs           /tmp   tmpfs defaults,nodev,nosuid  0  0

**/etc/network/interfaces:**

.. code-block:: bash

   auto eth0
   iface eth0 inet static
       address 192.168.1.10
       netmask 255.255.255.0
       gateway 192.168.1.1

**U-Boot Environment:**

.. code-block:: bash

   bootcmd=run loadkernel; run loadfdt; bootz ${loadaddr} - ${fdt_addr}
   bootargs=console=ttymxc0,115200 root=/dev/mmcblk0p2 rootwait rw
   loadkernel=load mmc 0:1 ${loadaddr} zImage
   loadfdt=load mmc 0:1 ${fdt_addr} imx6q-wandboard.dtb

================================================================================
Kernel Configuration Reference
================================================================================

**Essential Options:**

.. code-block:: bash

   # Device Tree
   CONFIG_OF=y
   CONFIG_OF_FLATTREE=y
   
   # Filesystems
   CONFIG_EXT4_FS=y
   CONFIG_SQUASHFS=y
   CONFIG_TMPFS=y
   
   # MTD/UBI
   CONFIG_MTD=y
   CONFIG_MTD_NAND=y
   CONFIG_MTD_UBI=y
   CONFIG_UBIFS_FS=y
   
   # Networking
   CONFIG_INET=y
   CONFIG_PACKET=y
   
   # USB
   CONFIG_USB=y
   CONFIG_USB_STORAGE=y
   
   # Device Drivers
   CONFIG_I2C=y
   CONFIG_SPI=y
   CONFIG_GPIO_SYSFS=y
   
   # Real-Time
   CONFIG_PREEMPT_RT=y
   CONFIG_HIGH_RES_TIMERS=y
   
   # Security
   CONFIG_SECURITY=y
   CONFIG_SECURITY_SELINUX=y
   CONFIG_SECURITY_APPARMOR=y

================================================================================
Yocto Variables Reference
================================================================================

**Build Configuration:**

.. code-block:: bash

   # Machine
   MACHINE = "wandboard-quad"
   DISTRO = "poky"
   
   # Parallelization
   BB_NUMBER_THREADS = "8"
   PARALLEL_MAKE = "-j 8"
   
   # Download/build directories
   DL_DIR = "/path/to/downloads"
   SSTATE_DIR = "/path/to/sstate-cache"
   TMPDIR = "${TOPDIR}/tmp"
   
   # Package management
   PACKAGE_CLASSES = "package_rpm"
   EXTRA_IMAGE_FEATURES = "debug-tweaks tools-sdk"
   
   # SDK
   SDKMACHINE = "x86_64"

**Recipe Variables:**

.. code-block:: bash

   # Metadata
   SUMMARY = "Package description"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
   
   # Source
   SRC_URI = "git://github.com/user/repo.git;protocol=https"
   SRCREV = "${AUTOREV}"
   S = "${WORKDIR}/git"
   
   # Dependencies
   DEPENDS = "libpng zlib"
   RDEPENDS_${PN} = "bash python3"
   
   # Build
   inherit cmake
   EXTRA_OECMAKE = "-DENABLE_FEATURE=ON"

================================================================================
Device Tree Snippets
================================================================================

**I2C Device:**

.. code-block:: dts

   &i2c1 {
       status = "okay";
       
       sensor@48 {
           compatible = "ti,tmp102";
           reg = <0x48>;
           interrupt-parent = <&gpio1>;
           interrupts = <13 IRQ_TYPE_LEVEL_LOW>;
       };
   };

**SPI Device:**

.. code-block:: dts

   &spi1 {
       status = "okay";
       
       flash@0 {
           compatible = "jedec,spi-nor";
           reg = <0>;
           spi-max-frequency = <25000000>;
       };
   };

**GPIO:**

.. code-block:: dts

   gpio-leds {
       compatible = "gpio-leds";
       
       led0 {
           label = "status";
           gpios = <&gpio3 16 GPIO_ACTIVE_HIGH>;
           linux,default-trigger = "heartbeat";
       };
   };

================================================================================
Troubleshooting Guide
================================================================================

**Boot Issues:**

.. code-block:: text

   Problem: No U-Boot prompt
   - Check serial console settings (115200 8N1)
   - Verify bootloader flash address
   - Test with JTAG
   
   Problem: Kernel panic - not syncing: VFS: Unable to mount root
   - Check bootargs root= parameter
   - Verify root filesystem is accessible
   - Check filesystem type matches fstab
   
   Problem: Kernel loads but no console
   - Verify console= in bootargs
   - Check device tree UART configuration
   - Verify getty in inittab

**Build Issues:**

.. code-block:: text

   Yocto: do_fetch failed
   - Check network connectivity
   - Verify SRC_URI is correct
   - Check SRCREV for git repos
   
   Yocto: do_compile failed
   - Run bitbake -c devshell <recipe>
   - Check build logs in tmp/work/
   - Verify DEPENDS are correct
   
   Kernel: module fails to load
   - Check kernel version mismatch
   - Verify CONFIG_MODVERSIONS
   - Check dependency modules loaded

**Runtime Issues:**

.. code-block:: text

   Problem: Out of memory
   - Check memory usage: free -h
   - Increase swap or reduce services
   - Check for memory leaks: valgrind
   
   Problem: High CPU usage
   - Identify process: top/htop
   - Profile: perf record -g -p <pid>
   - Check infinite loops, polling
   
   Problem: Storage full
   - Check usage: df -h
   - Clean logs: journalctl --vacuum-size=100M
   - Remove unnecessary packages

**Network Issues:**

.. code-block:: text

   Problem: No network
   - Check cable/WiFi: ip link
   - Verify IP: ip addr
   - Check routing: ip route
   - Test connectivity: ping 8.8.8.8
   
   Problem: DNS not working
   - Check /etc/resolv.conf
   - Test: nslookup google.com
   - Verify nameserver reachability

================================================================================
Performance Optimization
================================================================================

**Boot Time:**

.. code-block:: bash

   # Remove unnecessary services
   systemctl disable bluetooth cups
   
   # Parallel init (systemd)
   systemd-analyze blame
   systemd-analyze critical-chain
   
   # Kernel command line
   quiet loglevel=3 fastboot

**Runtime Performance:**

.. code-block:: bash

   # CPU governor
   echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
   
   # Disable swap
   swapoff -a
   
   # I/O scheduler
   echo deadline > /sys/block/mmcblk0/queue/scheduler
   
   # Reduce logging
   journalctl --vacuum-time=1d

**Size Optimization:**

.. code-block:: bash

   # Strip binaries
   arm-linux-gnueabihf-strip --strip-all <binary>
   
   # Compiler flags
   CFLAGS="-Os -ffunction-sections -fdata-sections"
   LDFLAGS="-Wl,--gc-sections"
   
   # BusyBox
   make defconfig
   make menuconfig  # Disable unnecessary applets
   
   # Squashfs root
   mksquashfs rootfs rootfs.squashfs -comp xz

================================================================================
Common Workflows
================================================================================

**Development Cycle:**

.. code-block:: text

   1. Edit code
   2. Cross-compile
   3. Deploy to target (TFTP, NFS, or scp)
   4. Test
   5. Debug (gdbserver, strace, logs)
   6. Repeat

**Yocto Development:**

.. code-block:: text

   1. Create/modify recipe
   2. bitbake <recipe>
   3. Test in QEMU or target
   4. Create patch: git format-patch
   5. Add patch to recipe SRC_URI
   6. Rebuild: bitbake -c clean <recipe> && bitbake <recipe>

**Kernel Development:**

.. code-block:: text

   1. bitbake -c devshell virtual/kernel
   2. Make changes
   3. git commit
   4. git format-patch -1 -o /path/to/recipe/files/
   5. Add to recipe SRC_URI
   6. bitbake -C compile virtual/kernel

**Production Deployment:**

.. code-block:: text

   1. Final testing in target environment
   2. Remove debug tools, symbols
   3. Enable security features
   4. Create production image
   5. Sign bootloader, kernel, rootfs
   6. Flash to production hardware
   7. Verify secure boot chain
   8. Field testing

================================================================================
Useful Resources
================================================================================

**Documentation:**

- Linux Kernel: https://www.kernel.org/doc/
- U-Boot: https://u-boot.readthedocs.io/
- Yocto Project: https://docs.yoctoproject.org/
- Device Tree: https://www.devicetree.org/
- Buildroot: https://buildroot.org/docs.html

**Mailing Lists:**

- linux-kernel@vger.kernel.org
- u-boot@lists.denx.de
- yocto@lists.yoctoproject.org

**Communities:**

- Stack Overflow: embedded, linux-kernel tags
- Embedded Linux Wiki: https://elinux.org/
- Bootlin Training: https://bootlin.com/training/

================================================================================
Cheat Sheet Summary
================================================================================

**1. Toolchains:**
   Cross-compilation setup, GCC, binutils, sysroot, SDK

**2. Bootloaders:**
   U-Boot commands, environment, device tree, boot scenarios

**3. Kernel:**
   Configuration, building, modules, device tree, debugging

**4. Root Filesystem:**
   FHS, BusyBox, init, device nodes, essential files

**5. Yocto:**
   BitBake, recipes, layers, images, SDK generation

**6. BSP:**
   Machine configuration, U-Boot/kernel recipes, WIC images

**7. Application Development:**
   Makefiles, autotools, CMake, Yocto recipes

**8. Storage:**
   Flash memory, MTD, UBI, UBIFS, ext4, SquashFS

**9. Device Drivers:**
   Character, platform, I2C, SPI drivers, GPIO

**10. Init Systems:**
   BusyBox init, systemd, service management

**11. Process Management:**
   Scheduling, memory, cgroups, CPU affinity

**12. Debugging:**
   GDB, strace, perf, ftrace, core dumps

**13. Real-Time:**
   PREEMPT_RT, RT scheduling, cyclictest, latency

**14. Security:**
   Secure boot, encryption, SELinux, hardening

**15. Master Index:**
   Quick reference, troubleshooting, workflows

================================================================================
END OF MASTER INDEX
================================================================================

**Complete Embedded Linux Cheatsheet Collection**
All 15 guides covering toolchains to production deployment.
For the complete embedded Linux development journey.

================================================================================
