================================================================================
Embedded Linux: Kernel Configuration and Building - Complete Guide
================================================================================

:Author: Technical Documentation Team
:Date: January 18, 2026
:Version: 1.0
:Target: Embedded Linux Developers
:Kernel: 4.1+, 6.8+ compatible
:Reference: Linux Embedded Development (Module 1 Ch4, Module 3 Ch4)

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**Kernel Build Quick Start:**

.. code-block:: bash

   # Get kernel source
   git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
   cd linux
   git checkout v6.1.75
   
   # Configure for target
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabihf-
   make multi_v7_defconfig
   make menuconfig  # Customize
   
   # Build (parallel)
   make -j$(nproc) zImage modules dtbs
   
   # Install
   make INSTALL_MOD_PATH=/path/to/rootfs modules_install
   cp arch/arm/boot/zImage /path/to/boot/
   cp arch/arm/boot/dts/*.dtb /path/to/boot/

**Common Configuration Targets:**

- ``defconfig`` - Minimal default configuration
- ``multi_v7_defconfig`` - ARM multi-platform (ARMv7)
- ``menuconfig`` - Interactive text menu
- ``savedefconfig`` - Save minimal config

**Build Outputs:**

- ``zImage`` - Compressed kernel (arch/arm/boot/)
- ``Image`` - Uncompressed kernel (arm64)
- ``modules`` - Loadable kernel modules (.ko)
- ``*.dtb`` - Device tree blobs

**Key Configuration Areas:**

1. Platform/SoC selection
2. Device drivers
3. Filesystems
4. Networking
5. Real-time (PREEMPT_RT)
6. Security features

================================================================================
1. Kernel Source Management
================================================================================

1.1 Obtaining Kernel Source
----------------------------

**Official Kernel Repository:**

.. code-block:: bash

   # Clone from kernel.org (official)
   git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
   cd linux
   
   # Or specific version
   git clone --depth=1 --branch v6.1.75 \
       https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
   
   # List tags
   git tag | grep "^v6.1"
   # v6.1
   # v6.1.1
   # v6.1.75
   
   # Checkout specific version
   git checkout v6.1.75

**Download Tarball:**

.. code-block:: bash

   # From kernel.org
   wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.75.tar.xz
   tar -xf linux-6.1.75.tar.xz
   cd linux-6.1.75

**Vendor Kernels:**

.. code-block:: bash

   # Raspberry Pi kernel
   git clone --depth=1 https://github.com/raspberrypi/linux.git
   cd linux
   git checkout rpi-6.1.y
   
   # TI (Texas Instruments) kernel
   git clone https://git.ti.com/git/ti-linux-kernel/ti-linux-kernel.git
   cd ti-linux-kernel
   git checkout ti-linux-6.1.y
   
   # NXP/Freescale kernel
   git clone https://github.com/nxp-imx/linux-imx.git
   cd linux-imx
   git checkout lf-6.1.y

**Kernel Version Naming:**

.. code-block:: text

   Format: <major>.<minor>.<patch>[-rc<N>]
   
   Examples:
   6.1          - Mainline release
   6.1.75       - Stable release (75th patch)
   6.2-rc5      - Release candidate 5
   
   LTS (Long Term Support) Versions:
   - 6.1.x  (until Dec 2026)
   - 5.15.x (until Oct 2026)
   - 5.10.x (until Dec 2026)
   - 4.19.x (until Dec 2024)

1.2 Kernel Source Structure
----------------------------

**Top-Level Directories:**

.. code-block:: text

   linux/
   ├── arch/              # Architecture-specific code
   │   ├── arm/          # 32-bit ARM
   │   ├── arm64/        # 64-bit ARM (AArch64)
   │   ├── mips/         # MIPS architecture
   │   ├── x86/          # x86 and x86_64
   │   └── powerpc/      # PowerPC
   ├── block/            # Block layer (storage subsystem)
   ├── certs/            # Kernel module signing certificates
   ├── crypto/           # Cryptographic API
   ├── Documentation/    # Kernel documentation
   ├── drivers/          # Device drivers
   │   ├── char/        # Character devices
   │   ├── block/       # Block devices
   │   ├── net/         # Network devices
   │   ├── gpio/        # GPIO drivers
   │   ├── i2c/         # I2C drivers
   │   ├── spi/         # SPI drivers
   │   ├── mmc/         # MMC/SD card drivers
   │   └── usb/         # USB drivers
   ├── fs/               # Filesystems
   │   ├── ext4/        # ext4 filesystem
   │   ├── ubifs/       # UBIFS (flash filesystem)
   │   ├── nfs/         # NFS client
   │   └── proc/        # procfs
   ├── include/          # Header files
   │   ├── linux/       # Linux kernel headers
   │   ├── uapi/        # User-space API headers
   │   └── dt-bindings/ # Device tree binding headers
   ├── init/             # Initialization code
   ├── ipc/              # Inter-process communication
   ├── kernel/           # Core kernel code
   │   ├── sched/       # Scheduler
   │   ├── time/        # Time management
   │   └── locking/     # Locking primitives
   ├── lib/              # Library functions
   ├── mm/               # Memory management
   ├── net/              # Networking stack
   │   ├── ipv4/        # IPv4 protocol
   │   ├── ipv6/        # IPv6 protocol
   │   └── core/        # Network core
   ├── samples/          # Sample code
   ├── scripts/          # Build scripts
   ├── security/         # Security modules (SELinux, AppArmor)
   ├── sound/            # Sound subsystem (ALSA)
   ├── tools/            # User-space tools
   ├── usr/              # initramfs
   ├── virt/             # Virtualization (KVM)
   ├── Kconfig           # Top-level configuration
   ├── Makefile          # Top-level makefile
   └── MAINTAINERS       # Kernel maintainers list

**Architecture-Specific Structure:**

.. code-block:: text

   arch/arm/
   ├── boot/
   │   ├── dts/         # Device tree sources (.dts)
   │   └── compressed/  # Kernel decompressor
   ├── configs/         # Default configurations
   │   ├── multi_v7_defconfig
   │   ├── omap2plus_defconfig
   │   └── bcm2835_defconfig
   ├── include/
   │   └── asm/         # ARM assembly headers
   ├── kernel/          # ARM kernel code
   ├── mach-*/          # Machine/SoC specific code
   │   ├── mach-omap2/  # TI OMAP/AM335x
   │   ├── mach-bcm/    # Broadcom (Raspberry Pi)
   │   └── mach-imx/    # NXP i.MX
   ├── mm/              # ARM memory management
   └── Kconfig          # ARM configuration options

================================================================================
2. Kernel Configuration
================================================================================

2.1 Configuration Methods
--------------------------

**Using Default Configuration:**

.. code-block:: bash

   # Set architecture and toolchain
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabihf-
   
   # List available defconfigs
   ls arch/arm/configs/
   # bcm2835_defconfig          (Raspberry Pi)
   # multi_v7_defconfig         (Multi-platform ARMv7)
   # omap2plus_defconfig        (TI OMAP/AM335x)
   # imx_v6_v7_defconfig        (NXP i.MX6/7)
   # sunxi_defconfig            (Allwinner)
   
   # Load defconfig
   make multi_v7_defconfig
   # configuration written to .config
   
   # For ARM64
   export ARCH=arm64
   export CROSS_COMPILE=aarch64-linux-gnu-
   make defconfig

**Interactive Configuration:**

.. code-block:: bash

   # Text-based menu (requires ncurses)
   make menuconfig
   
   # Graphical Qt-based (requires Qt)
   make xconfig
   
   # GTK-based (requires GTK+)
   make gconfig
   
   # Line-oriented (for scripts)
   make oldconfig  # Update old config for new kernel
   make olddefconfig  # Use defaults for new options

**Configuration File (.config):**

.. code-block:: bash

   # Configuration stored in .config
   ls -la .config
   # -rw-r--r-- 1 user user 234K .config
   
   # View specific options
   grep CONFIG_MMC .config
   # CONFIG_MMC=y
   # CONFIG_MMC_BLOCK=y
   # CONFIG_MMC_SDHCI=y
   
   # Enable/disable options manually
   echo "CONFIG_USB_STORAGE=y" >> .config
   echo "# CONFIG_SOUND is not set" >> .config
   
   # Validate and update
   make oldconfig

2.2 Configuration Options
--------------------------

**Configuration Symbols:**

.. code-block:: text

   Format:
   CONFIG_<OPTION>=<value>
   
   Values:
   y   - Built into kernel (static)
   m   - Build as module (loadable)
   n   - Not set / disabled
   
   Examples:
   CONFIG_MMC=y                 # MMC support built-in
   CONFIG_USB_STORAGE=m         # USB storage as module
   # CONFIG_DEBUG_FS is not set  # Debug FS disabled
   
   String/Integer:
   CONFIG_LOCALVERSION="-custom"
   CONFIG_HZ=100

**Key Configuration Areas:**

.. code-block:: text

   General setup
   ├── Local version (-custom appended to kernel version)
   ├── Default hostname
   ├── Cross-compiler prefix (arm-linux-gnueabihf-)
   └── Kernel compression (gzip, xz, lzo, lz4)
   
   System Type (arch/arm)
   ├── Multiple platform selection (multi_v7)
   ├── TI OMAP/AM335x support
   ├── Broadcom BCM2835 (Raspberry Pi)
   └── NXP i.MX6/7 support
   
   Kernel Features
   ├── Preemption Model
   │   ├── No Forced Preemption (Server)
   │   ├── Voluntary Kernel Preemption (Desktop)
   │   └── Preemptible Kernel (Low-Latency Desktop / RT)
   ├── Timer frequency (100/250/300/1000 HZ)
   └── High Resolution Timer support
   
   Boot options
   ├── Default kernel command string
   └── Built-in kernel command line
   
   CPU Power Management
   ├── CPU Frequency scaling
   └── CPU idle PM support

**Device Drivers Configuration:**

.. code-block:: text

   Device Drivers
   ├── Generic Driver Options
   │   └── Firmware loader
   ├── Block devices
   │   ├── Loopback device support
   │   └── RAM block device support
   ├── MMC/SD/SDIO card support
   │   ├── MMC block device driver
   │   ├── Secure Digital Host Controller Interface
   │   └── SDHCI platform support
   ├── Network device support
   │   ├── Ethernet driver support
   │   └── Wireless LAN
   ├── Input device support
   │   ├── Keyboards
   │   ├── Mouse
   │   └── Touchscreens
   ├── Character devices
   │   ├── Serial drivers
   │   └── I2C support
   ├── SPI support
   ├── GPIO support
   ├── USB support
   │   ├── USB Mass Storage support
   │   ├── USB Serial support
   │   └── USB Gadget support
   ├── Real Time Clock
   └── Watchdog Timer Support

**Filesystem Configuration:**

.. code-block:: text

   File systems
   ├── Second extended fs support (ext2)
   ├── The Extended 4 (ext4) filesystem
   ├── UBIFS file system support (flash)
   ├── Network File Systems
   │   ├── NFS client support
   │   └── Root file system on NFS
   ├── DOS/FAT/VFAT/EXFAT
   │   ├── VFAT (Windows-95) fs support
   │   └── Default codepage (437)
   └── Pseudo filesystems
       ├── /proc file system support
       ├── sysfs file system support
       └── Tmpfs virtual memory file system

2.3 Using menuconfig
--------------------

**Navigation:**

.. code-block:: text

   Keys:
   Arrow keys    - Navigate menu
   Enter         - Enter submenu / Toggle option
   Space         - Cycle through [*] (y), < > (n), <M> (m)
   Y             - Set to built-in (*)
   N             - Set to excluded ( )
   M             - Set to module (M)
   /             - Search for symbol
   ?             - Help for current option
   ESC ESC       - Go back / Exit
   
   Symbol legend:
   [ ]  - Option not set
   [*]  - Built into kernel
   <M>  - Build as module
   < >  - Disabled (can be enabled)
   -M-  - Must be module
   -*-  - Must be built-in (dependency)

**Example Configuration Session:**

.. code-block:: bash

   make menuconfig
   
   # Navigate: General setup
   # -> General setup
   #    -> Local version - append to kernel release
   #       (-myboard)
   
   # Navigate: Enable MMC
   # -> Device Drivers
   #    -> MMC/SD/SDIO card support
   #       [*] MMC/SD/SDIO card support
   #       <*>   MMC block device driver
   #       <*>   Secure Digital Host Controller Interface support
   
   # Search for option
   # Press '/' then type: USB_STORAGE
   # Shows: Symbol: USB_STORAGE [=m]
   #        Location: Device Drivers -> USB support -> USB Mass Storage
   
   # Save and exit
   # <Save> -> OK
   # <Exit> -> Exit

**Handling Dependencies:**

.. code-block:: text

   Dependencies are automatically handled:
   
   Example: Enabling ext4
   CONFIG_EXT4_FS=y
   Automatically selects:
   - CONFIG_JBD2=y (journaling)
   - CONFIG_CRC32C=y (checksum)
   - CONFIG_CRYPTO=y (crypto API)
   
   If dependency can't be met:
   --- Grayed out or hidden
   
   View dependencies:
   - Select option and press '?'
   - Shows "Depends on:" line

2.4 Minimal Configuration
--------------------------

**Saving Minimal Config:**

.. code-block:: bash

   # After configuring with menuconfig
   make savedefconfig
   
   # Creates 'defconfig' file (minimal configuration)
   ls -lh defconfig .config
   # -rw-r--r-- 1 user user  10K defconfig
   # -rw-r--r-- 1 user user 234K .config
   
   # defconfig only contains non-default options
   # .config contains all options (default + custom)
   
   # Save as custom defconfig
   cp defconfig arch/arm/configs/myboard_defconfig
   
   # Later, load custom defconfig
   make myboard_defconfig

**Creating Minimal Embedded Config:**

.. code-block:: bash

   # Start from minimal
   make allnoconfig  # All options disabled
   
   # Enable only essentials in menuconfig
   make menuconfig
   
   # Essential options for embedded:
   # - Platform/SoC support
   # - Serial console driver
   # - MMC/SD driver
   # - Root filesystem (ext4 or UBIFS)
   # - Network driver (if needed)
   # - GPIO, I2C, SPI (for peripherals)
   
   # Save minimal config
   make savedefconfig
   mv defconfig arch/arm/configs/minimal_embedded_defconfig

**Size Optimization:**

.. code-block:: bash

   # Optimize for size
   make menuconfig
   
   # General setup
   # -> Compiler optimization level
   #    (X) Optimize for size (-Os)
   
   # Kernel Features
   # -> Kernel compression mode
   #    (X) XZ (best compression, slower boot)
   #    (X) LZ4 (fast decompression, larger size)
   
   # Disable debugging
   # -> Kernel hacking
   #    [ ] Kernel debugging
   #    [ ] Debug Filesystem
   #    [ ] KGDB
   
   # Result: Kernel size 2-3MB vs 5-6MB unoptimized

================================================================================
3. Building the Kernel
================================================================================

3.1 Basic Build Process
------------------------

**Standard Build Sequence:**

.. code-block:: bash

   # Set environment
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabihf-
   
   # Configure
   make multi_v7_defconfig
   make menuconfig  # Optional customization
   
   # Build kernel image
   make -j$(nproc) zImage
   
   # Build modules
   make -j$(nproc) modules
   
   # Build device tree blobs
   make -j$(nproc) dtbs
   
   # Or build all at once
   make -j$(nproc) zImage modules dtbs

**Build Targets:**

.. code-block:: bash

   # Kernel images (architecture-specific)
   make zImage      # ARM compressed kernel
   make Image       # ARM64 uncompressed
   make uImage      # U-Boot wrapped image (legacy)
   make bzImage     # x86/x86_64 compressed
   
   # Modules
   make modules     # Build all modules
   make M=drivers/net/wireless  # Build specific directory
   
   # Device trees
   make dtbs        # All device tree blobs
   make am335x-boneblack.dtb  # Specific DTB
   
   # Everything
   make all         # Kernel + modules + DTBs
   
   # Cleaning
   make clean       # Remove build artifacts (keep .config)
   make mrproper    # Remove .config and build artifacts
   make distclean   # mrproper + editor backup files

**Build Output Locations:**

.. code-block:: bash

   # Kernel images
   arch/arm/boot/zImage                    # Compressed kernel
   arch/arm/boot/Image                     # Uncompressed
   arch/arm/boot/uImage                    # U-Boot format
   
   # Device tree blobs
   arch/arm/boot/dts/*.dtb
   arch/arm/boot/dts/ti/am335x-boneblack.dtb
   
   # Modules
   drivers/**/*.ko
   
   # Kernel symbols (for debugging)
   vmlinux          # Uncompressed ELF kernel with symbols
   System.map       # Symbol table

**Parallel Building:**

.. code-block:: bash

   # Use all CPU cores
   make -j$(nproc)
   
   # Or specify number
   make -j8
   
   # Typical build times (depends on config):
   # Full kernel:      5-15 minutes (8 cores)
   # Modules:          3-10 minutes
   # Single module:    10-30 seconds

3.2 Installing Kernel and Modules
----------------------------------

**Module Installation:**

.. code-block:: bash

   # Install modules to target rootfs
   make INSTALL_MOD_PATH=/path/to/rootfs modules_install
   
   # Creates:
   # /path/to/rootfs/lib/modules/6.1.75/
   # ├── kernel/          # Kernel modules
   # │   ├── drivers/
   # │   ├── fs/
   # │   └── net/
   # ├── modules.builtin  # Built-in modules list
   # ├── modules.dep      # Module dependencies
   # └── modules.order    # Module load order
   
   # For current running system (not cross-compile)
   sudo make modules_install  # Installs to /lib/modules/

**Kernel Image Installation:**

.. code-block:: bash

   # Copy kernel to boot partition
   cp arch/arm/boot/zImage /path/to/boot/
   
   # Copy device tree
   cp arch/arm/boot/dts/am335x-boneblack.dtb /path/to/boot/
   
   # Copy System.map (for debugging)
   cp System.map /path/to/boot/System.map-6.1.75
   
   # Update version file
   echo "6.1.75" > /path/to/boot/kernel_version

**SD Card Installation Example:**

.. code-block:: bash

   # Mount SD card boot partition
   sudo mount /dev/sdX1 /mnt/boot
   sudo mount /dev/sdX2 /mnt/rootfs
   
   # Install kernel
   sudo cp arch/arm/boot/zImage /mnt/boot/
   sudo cp arch/arm/boot/dts/am335x-boneblack.dtb /mnt/boot/
   
   # Install modules
   sudo make INSTALL_MOD_PATH=/mnt/rootfs modules_install
   
   # Unmount
   sudo umount /mnt/boot /mnt/rootfs
   sync

3.3 Building External Modules
------------------------------

**Out-of-Tree Module Build:**

.. code-block:: bash

   # Module directory structure
   mymodule/
   ├── mymodule.c
   └── Makefile
   
   # Makefile content
   obj-m := mymodule.o
   
   KDIR := /path/to/linux
   PWD := $(shell pwd)
   
   all:
   	$(MAKE) ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- \
   		-C $(KDIR) M=$(PWD) modules
   
   clean:
   	$(MAKE) -C $(KDIR) M=$(PWD) clean
   
   # Build module
   make
   # Creates: mymodule.ko
   
   # Install module
   sudo cp mymodule.ko /path/to/rootfs/lib/modules/6.1.75/extra/

**Multi-File Module:**

.. code-block:: make

   # Makefile for module with multiple source files
   obj-m := complexmodule.o
   complexmodule-objs := main.o helper.o device.o
   
   KDIR := /path/to/linux
   
   all:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules
   
   # Source files:
   # main.c, helper.c, device.c, module.h

**Building Against Running Kernel:**

.. code-block:: bash

   # On target (native build)
   apt-get install linux-headers-$(uname -r)
   
   # Makefile uses running kernel headers
   KDIR := /lib/modules/$(shell uname -r)/build
   
   all:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules

3.4 Kernel Build Troubleshooting
---------------------------------

**Common Build Errors:**

.. code-block:: bash

   # Error: No rule to make target
   # Cause: Missing dependency or wrong path
   # Fix: Clean and rebuild
   make mrproper
   make multi_v7_defconfig
   make -j$(nproc)
   
   # Error: arm-linux-gnueabihf-gcc: command not found
   # Cause: Toolchain not in PATH
   # Fix: Set CROSS_COMPILE correctly
   export PATH=$PATH:/path/to/toolchain/bin
   export CROSS_COMPILE=arm-linux-gnueabihf-
   
   # Error: *** mixed implicit and normal rules: deprecated syntax
   # Cause: Old make version
   # Fix: Upgrade make to 4.0+
   make --version  # Should be 4.0 or newer
   
   # Error: BTF: .tmp_vmlinux.btf: pahole not found
   # Cause: Missing pahole tool (BTF debugging)
   # Fix: Install or disable BTF
   apt-get install dwarves
   # Or disable: CONFIG_DEBUG_INFO_BTF=n

**Build Performance:**

.. code-block:: bash

   # Speed up builds with ccache
   apt-get install ccache
   export CC="ccache ${CROSS_COMPILE}gcc"
   
   # Monitor build progress
   make -j$(nproc) V=1  # Verbose output
   
   # Build only changed files
   make -j$(nproc)  # Incremental build (automatic)

================================================================================
4. Device Tree Configuration
================================================================================

4.1 Device Tree Fundamentals
-----------------------------

**Device Tree Purpose:**

.. code-block:: text

   Device Tree describes hardware to the kernel:
   - CPU, memory configuration
   - Peripherals (UART, I2C, SPI, GPIO, etc.)
   - Clocks, regulators, power domains
   - Pinmux configuration
   - Board-specific customizations
   
   Benefits:
   ✓ Single kernel for multiple boards
   ✓ No board-specific code in kernel
   ✓ Runtime hardware discovery
   ✓ Easy board customization

**Device Tree Source Structure:**

.. code-block:: dts

   /dts-v1/;
   #include "am33xx.dtsi"         /* SoC DTSI */
   #include "am335x-bone-common.dtsi"  /* Common BeagleBone */
   
   / {
       model = "TI AM335x BeagleBone Black";
       compatible = "ti,am335x-bone-black", "ti,am335x-bone", "ti,am33xx";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x20000000>; /* 512 MB */
       };
       
       leds {
           compatible = "gpio-leds";
           led0 {
               label = "beaglebone:green:usr0";
               gpios = <&gpio1 21 GPIO_ACTIVE_HIGH>;
               linux,default-trigger = "heartbeat";
           };
       };
       
       vmmcsd_fixed: fixedregulator0 {
           compatible = "regulator-fixed";
           regulator-name = "vmmcsd_fixed";
           regulator-min-microvolt = <3300000>;
           regulator-max-microvolt = <3300000>;
       };
   };
   
   /* Override/extend SoC definitions */
   &am33xx_pinmux {
       pinctrl-names = "default";
       pinctrl-0 = <&clkout2_pin>;
       
       i2c0_pins: pinmux_i2c0_pins {
           pinctrl-single,pins = <
               AM33XX_PADCONF(AM335X_PIN_I2C0_SDA, PIN_INPUT_PULLUP, MUX_MODE0)
               AM33XX_PADCONF(AM335X_PIN_I2C0_SCL, PIN_INPUT_PULLUP, MUX_MODE0)
           >;
       };
   };
   
   &i2c0 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&i2c0_pins>;
       clock-frequency = <400000>;
       
       /* I2C device */
       eeprom: eeprom@50 {
           compatible = "atmel,24c256";
           reg = <0x50>;
       };
   };
   
   &mmc1 {
       status = "okay";
       bus-width = <4>;
       pinctrl-names = "default";
       pinctrl-0 = <&mmc1_pins>;
       vmmc-supply = <&vmmcsd_fixed>;
   };

4.2 Compiling Device Trees
---------------------------

**Device Tree Compiler (dtc):**

.. code-block:: bash

   # Compile DTS to DTB
   dtc -I dts -O dtb -o am335x-boneblack.dtb am335x-boneblack.dts
   
   # Decompile DTB to DTS
   dtc -I dtb -O dts -o output.dts am335x-boneblack.dtb
   
   # With kernel build system
   make dtbs
   # Compiles all DTS in arch/arm/boot/dts/
   
   # Compile specific DTB
   make am335x-boneblack.dtb

**Including Device Tree Sources:**

.. code-block:: dts

   /* File: custom-board.dts */
   /dts-v1/;
   
   #include "am33xx.dtsi"               /* SoC definitions */
   #include <dt-bindings/gpio/gpio.h>    /* GPIO constants */
   #include <dt-bindings/pinctrl/am33xx.h>  /* Pin definitions */
   
   / {
       model = "Custom Board";
       compatible = "vendor,custom-board", "ti,am33xx";
       
       /* Board-specific nodes */
   };

**Device Tree Overlays:**

.. code-block:: dts

   /* Overlay to add I2C device */
   /dts-v1/;
   /plugin/;
   
   / {
       compatible = "ti,am335x-bone-black";
       
       fragment@0 {
           target = <&i2c1>;
           __overlay__ {
               #address-cells = <1>;
               #size-cells = <0>;
               
               sensor@48 {
                   compatible = "ti,tmp102";
                   reg = <0x48>;
               };
           };
       };
   };
   
   /* Compile overlay */
   dtc -@ -I dts -O dtb -o sensor-overlay.dtbo sensor-overlay.dts

**Checking Device Tree:**

.. code-block:: bash

   # Verify DTB structure
   fdtdump am335x-boneblack.dtb | less
   
   # On running system
   ls /sys/firmware/devicetree/base/
   # compatible
   # model
   # memory@80000000/
   # ocp/
   
   # View compatible string
   cat /sys/firmware/devicetree/base/compatible
   # ti,am335x-bone-blackti,am335x-boneti,am33xx

4.3 Device Tree Bindings
-------------------------

**Standard Properties:**

.. code-block:: dts

   node_name@address {
       compatible = "vendor,device";  /* Required: driver matching */
       reg = <address size>;           /* Register address/size */
       status = "okay" | "disabled";   /* Enable/disable node */
       interrupts = <IRQ_NUM FLAGS>;   /* Interrupt number */
       clocks = <&phandle>;            /* Clock reference */
       pinctrl-0 = <&pin_config>;      /* Pin configuration */
       #address-cells = <1>;           /* Address cells in children */
       #size-cells = <1>;              /* Size cells in children */
   };

**GPIO Bindings:**

.. code-block:: dts

   gpio-leds {
       compatible = "gpio-leds";
       
       led-heartbeat {
           label = "heartbeat";
           gpios = <&gpio1 21 GPIO_ACTIVE_HIGH>;
           linux,default-trigger = "heartbeat";
           default-state = "off";
       };
   };
   
   gpio-keys {
       compatible = "gpio-keys";
       
       button-user {
           label = "User Button";
           gpios = <&gpio0 30 GPIO_ACTIVE_LOW>;
           linux,code = <KEY_ENTER>;
           wakeup-source;
       };
   };

**I2C Device Binding:**

.. code-block:: dts

   &i2c1 {
       status = "okay";
       clock-frequency = <400000>;  /* 400 kHz */
       
       eeprom@50 {
           compatible = "atmel,24c256";
           reg = <0x50>;
           pagesize = <64>;
       };
       
       rtc@68 {
           compatible = "maxim,ds1307";
           reg = <0x68>;
           interrupt-parent = <&gpio1>;
           interrupts = <10 IRQ_TYPE_EDGE_FALLING>;
       };
   };

**SPI Device Binding:**

.. code-block:: dts

   &spi0 {
       status = "okay";
       pinctrl-0 = <&spi0_pins>;
       
       flash@0 {
           compatible = "jedec,spi-nor";
           reg = <0>;  /* Chip select 0 */
           spi-max-frequency = <25000000>;
           
           partitions {
               compatible = "fixed-partitions";
               #address-cells = <1>;
               #size-cells = <1>;
               
               partition@0 {
                   label = "bootloader";
                   reg = <0x0 0x40000>;  /* 256KB */
               };
               
               partition@40000 {
                   label = "kernel";
                   reg = <0x40000 0x400000>;  /* 4MB */
               };
           };
       };
   };

4.4 Custom Device Tree Creation
--------------------------------

**Creating Custom Board DTS:**

.. code-block:: bash

   # 1. Copy reference board DTS
   cd arch/arm/boot/dts/
   cp ti/am335x-boneblack.dts ti/myboard.dts
   
   # 2. Edit myboard.dts
   # - Update model and compatible
   # - Modify memory size
   # - Enable/disable peripherals
   # - Add custom devices
   
   # 3. Add to Makefile
   vim ti/Makefile
   # Add: dtb-$(CONFIG_SOC_AM33XX) += myboard.dtb
   
   # 4. Build
   make ti/myboard.dtb

**Example Custom Board:**

.. code-block:: dts

   /dts-v1/;
   #include "am33xx.dtsi"
   #include <dt-bindings/gpio/gpio.h>
   
   / {
       model = "My Custom AM335x Board";
       compatible = "myvendor,myboard", "ti,am33xx";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x40000000>;  /* 1GB instead of 512MB */
       };
       
       leds {
           compatible = "gpio-leds";
           status-led {
               label = "status:green";
               gpios = <&gpio2 10 GPIO_ACTIVE_HIGH>;
               default-state = "on";
           };
       };
       
       custom-device {
           compatible = "myvendor,custom-device";
           reg = <0x44e00000 0x1000>;
           interrupt-parent = <&intc>;
           interrupts = <42>;
       };
   };
   
   &uart0 {
       status = "okay";
       pinctrl-0 = <&uart0_pins>;
   };
   
   &i2c0 {
       status = "okay";
       clock-frequency = <100000>;
   };
   
   &mmc2 {
       status = "okay";
       vmmc-supply = <&vmmcsd_fixed>;
       bus-width = <8>;  /* eMMC */
       ti,non-removable;
   };

================================================================================
5. Kernel Modules
================================================================================

5.1 Module Basics
-----------------

**What are Kernel Modules?**

.. code-block:: text

   Kernel modules (.ko files):
   - Loadable kernel code
   - Can be loaded/unloaded at runtime
   - Extend kernel functionality without reboot
   - Reduce kernel size (load only needed drivers)
   
   Built-in vs Module:
   Built-in (=y): Compiled into kernel image, always loaded
   Module (=m):   Separate .ko file, loaded on demand
   
   Trade-offs:
   Built-in: Faster boot, always available, larger kernel
   Module:   Smaller kernel, flexible, runtime loading

**Module Commands:**

.. code-block:: bash

   # List loaded modules
   lsmod
   # Module                  Size  Used by
   # xt_tcpudp              16384  2
   # ip_tables              32768  0
   # x_tables               40960  2 xt_tcpudp,ip_tables
   
   # Load module
   modprobe usb_storage
   insmod /lib/modules/6.1.75/kernel/drivers/usb/storage/usb-storage.ko
   
   # Unload module
   modprobe -r usb_storage
   rmmod usb_storage
   
   # Module information
   modinfo usb_storage
   # filename:       /lib/modules/6.1.75/kernel/drivers/usb/storage/usb-storage.ko
   # license:        GPL
   # description:    USB Mass Storage driver for Linux
   # author:         Matthew Dharm
   # depends:        scsi_mod,usb-common
   
   # Module dependencies
   modprobe --show-depends usb_storage
   # insmod /lib/modules/6.1.75/kernel/drivers/scsi/scsi_mod.ko
   # insmod /lib/modules/6.1.75/kernel/drivers/usb/common/usb-common.ko
   # insmod /lib/modules/6.1.75/kernel/drivers/usb/storage/usb-storage.ko

5.2 Module Configuration
-------------------------

**Selecting Modules in menuconfig:**

.. code-block:: text

   Device Drivers
   -> USB support
      -> USB Mass Storage support
         < >  Not set
         <M>  Build as module  ← Press 'M'
         <*>  Built-in
   
   Result in .config:
   CONFIG_USB_STORAGE=m

**Module Parameters:**

.. code-block:: bash

   # View module parameters
   modinfo -p usb_storage
   # delay_use: seconds to delay before using a new device (uint)
   # option_zero_cd: ZeroCD mode (1=Force Modem (default)...) (uint)
   
   # Load module with parameters
   modprobe usb_storage delay_use=5
   
   # Persistent parameters in /etc/modprobe.d/
   echo "options usb_storage delay_use=5" > /etc/modprobe.d/usb_storage.conf

**Automatic Module Loading:**

.. code-block:: bash

   # List modules to load at boot
   cat /etc/modules
   # i2c-dev
   # spidev
   
   # Module blacklist (prevent loading)
   cat /etc/modprobe.d/blacklist.conf
   # blacklist nouveau  # Disable nouveau (use nvidia instead)
   
   # Auto-load based on hardware detection (udev)
   # Kernel sends uevent -> udev loads appropriate module

5.3 Module Dependencies
------------------------

**modules.dep File:**

.. code-block:: bash

   # Module dependency database
   cat /lib/modules/6.1.75/modules.dep
   # kernel/drivers/usb/storage/usb-storage.ko: kernel/drivers/scsi/scsi_mod.ko
   
   # Generated during modules_install
   depmod -a
   
   # Modprobe uses this to load dependencies automatically
   modprobe usb_storage  # Automatically loads scsi_mod first

**Manual Dependency Handling:**

.. code-block:: bash

   # Load modules in order (insmod doesn't handle deps)
   insmod /lib/modules/6.1.75/kernel/drivers/scsi/scsi_mod.ko
   insmod /lib/modules/6.1.75/kernel/drivers/usb/storage/usb-storage.ko
   
   # Or use modprobe (handles dependencies)
   modprobe usb_storage

================================================================================
6. Kernel Command Line (bootargs)
================================================================================

6.1 Common Kernel Parameters
-----------------------------

**Console Configuration:**

.. code-block:: bash

   console=ttyO0,115200n8     # UART console (OMAP/AM335x)
   console=ttyS0,115200       # Standard serial port
   console=tty0               # VGA console
   console=ttyAMA0,115200     # ARM PrimeCell UART
   
   # Multiple consoles (output to both)
   console=ttyO0,115200 console=tty0

**Root Filesystem:**

.. code-block:: bash

   root=/dev/mmcblk0p2              # SD card partition 2
   root=/dev/sda1                   # USB/SATA disk
   root=/dev/mtdblock3              # NAND flash MTD partition
   root=ubi0:rootfs rootfstype=ubifs  # UBIFS on UBI volume
   root=/dev/nfs nfsroot=192.168.1.10:/export/rootfs  # NFS root
   
   # Root filesystem type (if auto-detect fails)
   rootfstype=ext4
   rootfstype=ubifs
   
   # Root mount options
   rw                  # Mount read-write (default for development)
   ro                  # Mount read-only (production)
   rootwait            # Wait for root device (needed for slow MMC)
   rootdelay=5         # Wait 5 seconds before mounting root

**Network Boot Parameters:**

.. code-block:: bash

   # NFS root
   root=/dev/nfs \
   nfsroot=192.168.1.10:/export/rootfs,tcp,vers=3 \
   ip=192.168.1.100:192.168.1.10:192.168.1.1:255.255.255.0:myboard:eth0:off
   #  <client-ip>:<server-ip>:<gw-ip>:<netmask>:<hostname>:<device>:<autoconf>
   
   # Or use DHCP
   ip=dhcp

**Debugging Parameters:**

.. code-block:: bash

   earlyprintk            # Enable early boot messages
   debug                  # Verbose kernel messages
   loglevel=8             # Maximum log level (0-8, 8=most verbose)
   ignore_loglevel        # Print all kernel messages
   initcall_debug         # Show initcall timing
   
   # Quiet boot (minimal messages)
   quiet loglevel=3

**Memory Parameters:**

.. code-block:: bash

   mem=512M               # Limit memory to 512MB
   mem=1G@0x80000000      # 1GB at address 0x80000000
   memtest=4              # Run memory test (4 patterns)

**Init System:**

.. code-block:: bash

   init=/sbin/init        # Default init
   init=/bin/sh           # Emergency shell (debugging)
   init=/usr/lib/systemd/systemd  # systemd

**Complete Example:**

.. code-block:: bash

   # U-Boot bootargs
   setenv bootargs 'console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw rootwait'
   
   # Production system
   setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk1p2 ro rootfstype=ext4 quiet'
   
   # Network development
   setenv bootargs 'console=ttyO0,115200 root=/dev/nfs nfsroot=192.168.1.10:/export/rootfs,tcp ip=192.168.1.100:192.168.1.10:192.168.1.1:255.255.255.0::eth0:off earlyprintk debug'

6.2 Built-in Command Line
--------------------------

**Compile-time Default:**

.. code-block:: bash

   # In menuconfig
   # Boot options
   #   -> Default kernel command string
   #      "console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw"
   
   # In .config
   CONFIG_CMDLINE="console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw"
   CONFIG_CMDLINE_EXTEND=y  # Append bootloader args
   # or
   CONFIG_CMDLINE_FORCE=y   # Ignore bootloader args

================================================================================
7. Exam-Style Questions
================================================================================

**Q1:** What is the difference between zImage and Image?

**A:** zImage is compressed kernel (self-extracting), Image is uncompressed.
zImage boots faster due to smaller size, Image is used when decompressor not
available (some bootloaders, ARM64).

**Q2:** How do you build kernel for ARM BeagleBone Black?

**A:**
.. code-block:: bash

   export ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
   make multi_v7_defconfig
   make -j$(nproc) zImage modules dtbs
   make INSTALL_MOD_PATH=/path/to/rootfs modules_install

**Q3:** What does CONFIG_USB_STORAGE=m mean?

**A:** Build USB Mass Storage support as loadable kernel module (.ko file),
not built into kernel. Can be loaded/unloaded at runtime.

**Q4:** How do you create minimal custom defconfig?

**A:** 
.. code-block:: bash

   make allnoconfig
   make menuconfig  # Enable required options
   make savedefconfig
   cp defconfig arch/arm/configs/myboard_defconfig

**Q5:** What is the purpose of Device Tree?

**A:** Describes hardware to kernel in a data structure, allowing single
kernel to support multiple boards without recompilation.

**Q6:** How do you compile single device tree blob?

**A:** `make am335x-boneblack.dtb`

**Q7:** What kernel parameter specifies root filesystem?

**A:** `root=/dev/mmcblk0p2` (example for SD card partition 2)

**Q8:** How to build only network drivers?

**A:** `make M=drivers/net`

**Q9:** What is the difference between modprobe and insmod?

**A:** modprobe handles dependencies automatically, insmod requires manual
dependency loading in correct order.

**Q10:** Where are compiled DTBs located for ARM?

**A:** `arch/arm/boot/dts/*.dtb`

================================================================================
8. Key Takeaways
================================================================================

.. code-block:: text

   Configuration Essentials:
   =========================
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-gnueabihf-
   make <board>_defconfig
   make menuconfig
   
   Build Commands:
   ===============
   make -j$(nproc) zImage     # Kernel
   make -j$(nproc) modules    # Modules
   make -j$(nproc) dtbs       # Device trees
   make INSTALL_MOD_PATH=/rootfs modules_install
   
   Output Locations:
   =================
   arch/arm/boot/zImage            # Compressed kernel
   arch/arm/boot/dts/*.dtb         # Device tree blobs
   drivers/**/*.ko                 # Kernel modules
   vmlinux                         # Uncompressed with symbols
   
   Device Tree:
   ============
   .dts → (dtc) → .dtb
   Describes hardware to kernel
   Single kernel, multiple boards
   
   Modules (=m vs =y):
   ===================
   =y  Built-in, always loaded, larger kernel
   =m  Loadable module, flexible, smaller kernel
   modprobe handles dependencies
   insmod requires manual ordering
   
   Kernel Parameters:
   ==================
   console=ttyO0,115200n8
   root=/dev/mmcblk0p2
   rootwait rw
   
   Size Optimization:
   ==================
   - Use -Os (optimize for size)
   - Disable debugging (DEBUG_FS, KGDB)
   - Use XZ compression
   - Disable unused features
   Result: 2-3MB vs 5-6MB

================================================================================
END OF CHEATSHEET
================================================================================

