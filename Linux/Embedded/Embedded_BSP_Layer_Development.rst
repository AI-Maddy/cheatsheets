================================================================================
Embedded Linux: BSP Layer Development - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 1 Ch10-11, Module 2 Ch4)
:Target: Yocto Project BSP Development
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Create BSP Layer:**

.. code-block:: bash

   # Create BSP layer structure
   bitbake-layers create-layer meta-mybsp
   cd meta-mybsp
   
   # BSP structure
   meta-mybsp/
   ├── conf/
   │   ├── layer.conf
   │   └── machine/
   │       └── myboard.conf          # Machine configuration
   ├── recipes-bsp/
   │   └── u-boot/
   │       └── u-boot_%.bbappend     # Bootloader customization
   ├── recipes-kernel/
   │   └── linux/
   │       ├── linux-yocto_%.bbappend
   │       └── files/
   │           ├── defconfig
   │           └── myboard.dts
   └── recipes-core/
       └── images/
           └── myboard-image.bb      # Custom image

**Machine Configuration (conf/machine/myboard.conf):**

.. code-block:: bitbake

   #@TYPE: Machine
   #@NAME: MyBoard
   #@DESCRIPTION: Custom embedded board based on AM335x
   
   require conf/machine/include/ti-soc.inc
   
   MACHINE_FEATURES = "ext2 serial ethernet usb"
   
   PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
   PREFERRED_PROVIDER_virtual/bootloader = "u-boot"
   
   KERNEL_IMAGETYPE = "zImage"
   KERNEL_DEVICETREE = "myboard.dtb"
   
   UBOOT_MACHINE = "am335x_evm_defconfig"
   UBOOT_ENTRYPOINT = "0x80008000"
   UBOOT_LOADADDRESS = "0x80008000"
   
   SERIAL_CONSOLE = "115200 ttyO0"
   
   MACHINE_ESSENTIAL_EXTRA_RDEPENDS = "kernel-devicetree"
   MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS = "kernel-modules"

**U-Boot Customization:**

.. code-block:: bitbake

   # recipes-bsp/u-boot/u-boot_%.bbappend
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   SRC_URI += "file://0001-add-board-support.patch"
   
   UBOOT_MACHINE = "myboard_defconfig"

**Kernel Customization:**

.. code-block:: bitbake

   # recipes-kernel/linux/linux-yocto_%.bbappend
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   SRC_URI += " \
       file://defconfig \
       file://myboard.dts \
       file://0001-add-driver.patch \
       "
   
   KERNEL_DEVICETREE = "myboard.dtb"
   COMPATIBLE_MACHINE = "myboard"

================================================================================
1. BSP Layer Fundamentals
================================================================================

1.1 What is a BSP Layer?
-------------------------

**BSP (Board Support Package) Definition:**

.. code-block:: text

   BSP layer provides hardware-specific support:
   - Machine configuration files
   - Bootloader configuration and patches
   - Kernel configuration and device trees
   - Hardware-specific drivers
   - Firmware binaries
   - Board-specific images
   
   BSP Layer Responsibilities:
   ✓ Define hardware capabilities (MACHINE_FEATURES)
   ✓ Configure bootloader (U-Boot, GRUB)
   ✓ Configure kernel and device tree
   ✓ Provide hardware drivers
   ✓ Set boot parameters and console
   ✓ Define image format (wic, ext4, etc.)

**BSP Layer Structure:**

.. code-block:: text

   meta-<vendor>-bsp/
   ├── conf/
   │   ├── layer.conf                    # Layer configuration
   │   └── machine/                      # Machine definitions
   │       ├── myboard.conf
   │       ├── myboard-variant.conf
   │       └── include/
   │           └── myboard-common.inc
   ├── recipes-bsp/                      # Bootloader recipes
   │   ├── u-boot/
   │   ├── grub/
   │   └── firmware/
   ├── recipes-kernel/                   # Kernel recipes
   │   └── linux/
   │       ├── linux-yocto_%.bbappend
   │       ├── linux-myboard_%.bb
   │       └── files/
   │           ├── defconfig
   │           ├── myboard.dts
   │           └── patches/
   ├── recipes-core/                     # Core modifications
   │   ├── images/
   │   └── packagegroups/
   └── recipes-drivers/                  # Hardware drivers
       └── mydriver/

1.2 Creating BSP Layer
-----------------------

**Step 1: Create Layer Structure:**

.. code-block:: bash

   # Auto-create layer
   bitbake-layers create-layer meta-mybsp
   cd meta-mybsp
   
   # Create BSP-specific directories
   mkdir -p conf/machine
   mkdir -p recipes-bsp/u-boot/files
   mkdir -p recipes-kernel/linux/files
   mkdir -p recipes-core/images

**Step 2: Configure Layer (conf/layer.conf):**

.. code-block:: bitbake

   # We have a conf and classes directory, add to BBPATH
   BBPATH .= ":${LAYERDIR}"
   
   # We have recipes-* directories, add to BBFILES
   BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
               ${LAYERDIR}/recipes-*/*/*.bbappend"
   
   BBFILE_COLLECTIONS += "mybsp"
   BBFILE_PATTERN_mybsp = "^${LAYERDIR}/"
   BBFILE_PRIORITY_mybsp = "7"
   
   LAYERDEPENDS_mybsp = "core yocto"
   LAYERSERIES_COMPAT_mybsp = "kirkstone"

**Step 3: Add to Build:**

.. code-block:: bash

   cd /path/to/build
   bitbake-layers add-layer /path/to/meta-mybsp
   
   # Set MACHINE in conf/local.conf
   echo 'MACHINE = "myboard"' >> conf/local.conf

================================================================================
2. Machine Configuration
================================================================================

2.1 Machine Configuration File
-------------------------------

**Complete Machine Configuration:**

.. code-block:: bitbake

   # conf/machine/myboard.conf
   
   #@TYPE: Machine
   #@NAME: MyBoard Custom Board
   #@DESCRIPTION: Custom embedded board based on TI AM335x SoC
   
   # Include common SoC settings
   require conf/machine/include/ti-soc.inc
   require conf/machine/include/tune-cortexa8.inc
   
   # Machine features
   MACHINE_FEATURES = "ext2 ext4 serial ethernet usb usbhost usbgadget \
                       alsa apm vfat ext2 rtc"
   
   # Kernel provider and configuration
   PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
   PREFERRED_VERSION_linux-yocto = "6.1%"
   KERNEL_IMAGETYPE = "zImage"
   KERNEL_DEVICETREE = "ti/am335x-myboard.dtb"
   KERNEL_EXTRA_ARGS += "LOADADDR=0x80008000"
   
   # Bootloader
   PREFERRED_PROVIDER_virtual/bootloader = "u-boot"
   PREFERRED_PROVIDER_u-boot = "u-boot"
   UBOOT_MACHINE = "am335x_myboard_defconfig"
   UBOOT_ENTRYPOINT = "0x80008000"
   UBOOT_LOADADDRESS = "0x80008000"
   SPL_BINARY = "MLO"
   
   # Serial console
   SERIAL_CONSOLES = "115200;ttyO0"
   SERIAL_CONSOLES_CHECK = "${SERIAL_CONSOLES}"
   
   # Image format
   IMAGE_FSTYPES += "tar.bz2 ext4 wic wic.bz2"
   WKS_FILE = "myboard-sdimage.wks"
   
   # Extra packages for this machine
   MACHINE_ESSENTIAL_EXTRA_RDEPENDS = "kernel-devicetree kernel-image"
   MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS = "kernel-modules"
   MACHINE_EXTRA_RDEPENDS = "myboard-firmware"
   
   # Default tune
   DEFAULTTUNE = "cortexa8thf-neon"

**Machine Feature Flags:**

.. code-block:: text

   Common MACHINE_FEATURES:
   - serial: Serial port support
   - ethernet: Ethernet support
   - wifi: WiFi support
   - bluetooth: Bluetooth support
   - usbhost: USB host mode
   - usbgadget: USB gadget/device mode
   - alsa: Audio (ALSA)
   - screen: Display support
   - touchscreen: Touchscreen
   - ext2, ext4, vfat: Filesystem support
   - rtc: Real-time clock
   - pci: PCI bus
   - pcmcia: PCMCIA support

2.2 Include Files
------------------

**SoC Include File:**

.. code-block:: bitbake

   # conf/machine/include/ti-am335x.inc
   
   # SoC family
   SOC_FAMILY = "ti-am335x"
   
   # Architecture
   require conf/machine/include/arm/armv7a/tune-cortexa8.inc
   
   # Kernel and bootloader providers
   PREFERRED_PROVIDER_virtual/kernel = "linux-ti-staging"
   PREFERRED_PROVIDER_virtual/bootloader = "u-boot-ti-staging"
   
   # Common kernel device trees
   KERNEL_DEVICETREE_append = " \
       ti/am335x-bone.dtb \
       ti/am335x-boneblack.dtb \
       "
   
   # SGX graphics
   MACHINE_FEATURES_append = " sgx"
   
   # Extra firmware
   EXTRA_IMAGEDEPENDS += "u-boot-ti-staging"

**Tune Include File:**

.. code-block:: bitbake

   # Use standard ARM Cortex-A8 tuning
   require conf/machine/include/arm/armv7a/tune-cortexa8.inc
   
   # Or custom tuning
   DEFAULTTUNE ?= "cortexa8thf-neon"
   
   TUNEVALID[cortexa8] = "Enable Cortex-A8 optimizations"
   TUNE_CCARGS .= "${@bb.utils.contains('TUNE_FEATURES', 'cortexa8', ' -mtune=cortex-a8', '', d)}"
   
   AVAILTUNES += "cortexa8thf-neon"
   ARMPKGARCH_tune-cortexa8thf-neon = "cortexa8"
   TUNE_FEATURES_tune-cortexa8thf-neon = "arm armv7a vfp thumb neon callconvention-hard cortexa8"
   PACKAGE_EXTRA_ARCHS_tune-cortexa8thf-neon = "cortexa8hf-neon"

================================================================================
3. Bootloader Configuration
================================================================================

3.1 U-Boot Recipe Customization
--------------------------------

**U-Boot .bbappend:**

.. code-block:: bitbake

   # recipes-bsp/u-boot/u-boot_%.bbappend
   
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   # Board-specific defconfig
   UBOOT_MACHINE_myboard = "am335x_myboard_defconfig"
   
   # Add board support patches
   SRC_URI_append_myboard = " \
       file://0001-add-myboard-support.patch \
       file://0002-custom-environment.patch \
       "
   
   # Custom environment file
   SRC_URI_append = " file://uEnv.txt"
   
   do_deploy_append() {
       install -m 0644 ${WORKDIR}/uEnv.txt ${DEPLOYDIR}/
   }

**U-Boot Patches:**

.. code-block:: bash

   # files/0001-add-myboard-support.patch
   # Adds board configuration to U-Boot
   
   # Generate from U-Boot modifications:
   cd u-boot
   git add board/ti/myboard/
   git commit -m "Add myboard support"
   git format-patch -1
   # Copy patch to meta-mybsp/recipes-bsp/u-boot/files/

**Custom U-Boot Environment:**

.. code-block:: bash

   # files/uEnv.txt
   bootpart=0:2
   bootdir=/boot
   bootfile=zImage
   console=ttyO0,115200n8
   optargs=
   
   mmcargs=setenv bootargs console=${console} ${optargs} \
       root=/dev/mmcblk0p2 rw rootfstype=ext4 rootwait
   
   loadfdt=load mmc ${bootpart} ${fdtaddr} ${bootdir}/${fdtfile}
   loadimage=load mmc ${bootpart} ${loadaddr} ${bootdir}/${bootfile}
   
   mmcboot=run mmcargs; bootz ${loadaddr} - ${fdtaddr}
   
   uenvcmd=run loadimage; run loadfdt; run mmcboot

3.2 Custom U-Boot Recipe
-------------------------

**Full U-Boot Recipe:**

.. code-block:: bitbake

   # recipes-bsp/u-boot/u-boot-myboard_2023.04.bb
   
   require recipes-bsp/u-boot/u-boot.inc
   
   SUMMARY = "U-Boot for MyBoard"
   LICENSE = "GPLv2+"
   LIC_FILES_CHKSUM = "file://Licenses/README;md5=..."
   
   DEPENDS += "flex-native bison-native"
   
   SRC_URI = " \
       git://github.com/u-boot/u-boot.git;protocol=https;branch=master \
       file://0001-myboard-support.patch \
       file://myboard_defconfig \
       "
   
   SRCREV = "abc123..."
   
   S = "${WORKDIR}/git"
   
   UBOOT_MACHINE = "myboard_defconfig"
   
   do_configure_prepend() {
       cp ${WORKDIR}/myboard_defconfig ${S}/configs/
   }
   
   COMPATIBLE_MACHINE = "myboard"

================================================================================
4. Kernel Configuration
================================================================================

4.1 Kernel Recipe Append
-------------------------

**Linux Kernel .bbappend:**

.. code-block:: bitbake

   # recipes-kernel/linux/linux-yocto_%.bbappend
   
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   # Compatible machines
   COMPATIBLE_MACHINE_myboard = "myboard"
   
   # Kernel configuration
   SRC_URI_append_myboard = " \
       file://defconfig \
       file://myboard.cfg \
       file://0001-add-custom-driver.patch \
       "
   
   # Device tree
   SRC_URI_append = " file://myboard.dts"
   
   KERNEL_DEVICETREE_myboard = "ti/am335x-myboard.dtb"
   
   # Copy device tree to kernel source
   do_configure_prepend() {
       cp ${WORKDIR}/myboard.dts ${S}/arch/arm/boot/dts/ti/
   }

**Kernel Configuration Fragment:**

.. code-block:: bash

   # files/myboard.cfg
   CONFIG_CAN=m
   CONFIG_CAN_TI_HECC=m
   CONFIG_SPI=y
   CONFIG_SPI_OMAP24XX=y
   CONFIG_GPIO_SYSFS=y
   CONFIG_LEDS_GPIO=y
   CONFIG_USB_MUSB_HDRC=y
   CONFIG_USB_MUSB_DSPS=y
   # Custom driver
   CONFIG_MYBOARD_CUSTOM_DRIVER=m

**Device Tree Source:**

.. code-block:: dts

   # files/myboard.dts
   /dts-v1/;
   
   #include "am33xx.dtsi"
   #include "am335x-bone-common.dtsi"
   #include <dt-bindings/interrupt-controller/irq.h>
   
   / {
       model = "MyBoard Custom Board";
       compatible = "myvendor,myboard", "ti,am33xx";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x20000000>; /* 512 MB */
       };
       
       leds {
           compatible = "gpio-leds";
           led-status {
               label = "myboard:green:status";
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
   
   &am33xx_pinmux {
       pinctrl-names = "default";
       
       spi0_pins: pinmux_spi0_pins {
           pinctrl-single,pins = <
               AM33XX_PADCONF(AM335X_PIN_SPI0_SCLK, PIN_INPUT_PULLUP, MUX_MODE0)
               AM33XX_PADCONF(AM335X_PIN_SPI0_D0, PIN_INPUT_PULLUP, MUX_MODE0)
               AM33XX_PADCONF(AM335X_PIN_SPI0_D1, PIN_OUTPUT_PULLUP, MUX_MODE0)
               AM33XX_PADCONF(AM335X_PIN_SPI0_CS0, PIN_OUTPUT_PULLUP, MUX_MODE0)
           >;
       };
   };
   
   &spi0 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&spi0_pins>;
       
       flash@0 {
           compatible = "jedec,spi-nor";
           reg = <0>;
           spi-max-frequency = <48000000>;
       };
   };
   
   &mmc1 {
       status = "okay";
       vmmc-supply = <&vmmcsd_fixed>;
       bus-width = <4>;
   };

4.2 Custom Kernel Recipe
-------------------------

**Complete Kernel Recipe:**

.. code-block:: bitbake

   # recipes-kernel/linux/linux-myboard_6.1.bb
   
   require recipes-kernel/linux/linux-yocto.inc
   
   SUMMARY = "Linux kernel for MyBoard"
   LICENSE = "GPLv2"
   LIC_FILES_CHKSUM = "file://COPYING;md5=..."
   
   LINUX_VERSION = "6.1.75"
   LINUX_VERSION_EXTENSION = "-myboard"
   
   SRCREV = "abc123..."
   SRC_URI = " \
       git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;branch=linux-6.1.y \
       file://defconfig \
       file://myboard.dts \
       file://0001-myboard-driver.patch \
       "
   
   S = "${WORKDIR}/git"
   
   KERNEL_DEVICETREE = "am335x-myboard.dtb"
   COMPATIBLE_MACHINE = "myboard"
   
   do_configure_prepend() {
       cp ${WORKDIR}/myboard.dts ${S}/arch/${ARCH}/boot/dts/
       cp ${WORKDIR}/defconfig ${B}/.config
   }

================================================================================
5. BSP Images and Packages
================================================================================

5.1 Custom BSP Image
--------------------

**Board-Specific Image:**

.. code-block:: bitbake

   # recipes-core/images/myboard-image.bb
   
   SUMMARY = "MyBoard custom image"
   LICENSE = "MIT"
   
   inherit core-image
   
   # Image features
   IMAGE_FEATURES += " \
       ssh-server-openssh \
       tools-debug \
       package-management \
       "
   
   # Core packages
   IMAGE_INSTALL = " \
       packagegroup-core-boot \
       packagegroup-base \
       ${CORE_IMAGE_EXTRA_INSTALL} \
       "
   
   # Hardware-specific packages
   IMAGE_INSTALL += " \
       kernel-modules \
       linux-firmware \
       myboard-firmware \
       i2c-tools \
       spi-tools \
       can-utils \
       "
   
   # Application packages
   IMAGE_INSTALL += " \
       python3 \
       opencv \
       gstreamer1.0 \
       myboard-app \
       "
   
   # Image format
   IMAGE_FSTYPES = "tar.bz2 ext4 wic.bz2"
   IMAGE_ROOTFS_EXTRA_SPACE = "1048576"

5.2 Board-Specific Package Group
---------------------------------

**Package Group Recipe:**

.. code-block:: bitbake

   # recipes-core/packagegroups/packagegroup-myboard-base.bb
   
   SUMMARY = "MyBoard base package group"
   LICENSE = "MIT"
   
   inherit packagegroup
   
   RDEPENDS_${PN} = " \
       kernel-modules \
       linux-firmware-iwlwifi \
       myboard-firmware \
       i2c-tools \
       spidev-test \
       can-utils \
       ethtool \
       iperf3 \
       htop \
       "

================================================================================
6. WIC Image Creation
================================================================================

6.1 WIC Kickstart File
-----------------------

**SD Card Image Layout:**

.. code-block:: text

   # wic/myboard-sdimage.wks
   
   # Partition layout for SD card (MBR)
   # part <mountpoint> --source <source> --ondisk <device> --fstype=<type> --label <label> --align <align> --size <size>
   
   # Boot partition (FAT32, 64MB)
   part /boot --source bootimg-partition --ondisk mmcblk0 --fstype=vfat --label boot --active --align 4096 --size 64M
   
   # Root filesystem (ext4, remaining space)
   part / --source rootfs --ondisk mmcblk0 --fstype=ext4 --label root --align 4096
   
   bootloader --ptable msdos

**Advanced WIC Configuration:**

.. code-block:: text

   # myboard-sdimage-advanced.wks
   
   # SPL/MLO at fixed offset (raw)
   part --source rawcopy --sourceparams="file=MLO" --ondisk mmcblk0 --no-table --align 1
   
   # U-Boot at offset 256KB (raw)
   part --source rawcopy --sourceparams="file=u-boot.img" --ondisk mmcblk0 --no-table --align 256
   
   # Boot partition (kernel, dtb, boot scripts)
   part /boot --source bootimg-partition --ondisk mmcblk0 --fstype=vfat --label boot --active --align 4096 --size 128M --use-uuid
   
   # Root filesystem
   part / --source rootfs --ondisk mmcblk0 --fstype=ext4 --label root --align 4096 --size 2G --use-uuid
   
   # Data partition
   part /data --ondisk mmcblk0 --fstype=ext4 --label data --align 4096 --size 1G
   
   bootloader --ptable gpt

6.2 Custom WIC Plugin
---------------------

**Boot Image Plugin:**

.. code-block:: python

   # scripts/lib/wic/plugins/source/myboard-bootimg.py
   
   import os
   from wic.pluginbase import SourcePlugin
   
   class MyBoardBootimgPlugin(SourcePlugin):
       name = 'myboard-bootimg'
       
       @classmethod
       def do_prepare_partition(cls, part, source_params, cr, cr_workdir,
                                oe_builddir, bootimg_dir, kernel_dir,
                                rootfs_dir, native_sysroot):
           
           # Copy MLO
           mlo = "%s/MLO" % kernel_dir
           cls.install_task(part, mlo, bootimg_dir)
           
           # Copy U-Boot
           uboot = "%s/u-boot.img" % kernel_dir
           cls.install_task(part, uboot, bootimg_dir)
           
           # Copy kernel
           kernel = "%s/zImage" % kernel_dir
           cls.install_task(part, kernel, bootimg_dir)
           
           # Copy device tree
           dtb = "%s/am335x-myboard.dtb" % kernel_dir
           cls.install_task(part, dtb, bootimg_dir)
           
           # Copy boot script
           uenv = "%s/uEnv.txt" % kernel_dir
           if os.path.exists(uenv):
               cls.install_task(part, uenv, bootimg_dir)

================================================================================
7. Testing and Validation
================================================================================

7.1 Build and Test
-------------------

**Build BSP:**

.. code-block:: bash

   # Setup environment
   source oe-init-build-env
   
   # Build for myboard
   MACHINE=myboard bitbake myboard-image
   
   # Or set in local.conf and build
   echo 'MACHINE = "myboard"' >> conf/local.conf
   bitbake myboard-image
   
   # Output location
   ls tmp/deploy/images/myboard/
   # myboard-image-myboard.wic.bz2
   # myboard-image-myboard.ext4
   # zImage
   # am335x-myboard.dtb
   # u-boot.img
   # MLO

**Flash SD Card:**

.. code-block:: bash

   # Extract WIC image
   bunzip2 myboard-image-myboard.wic.bz2
   
   # Write to SD card (WARNING: double-check device!)
   sudo dd if=myboard-image-myboard.wic of=/dev/sdX bs=4M status=progress
   sync
   
   # Or use bmaptool (faster)
   sudo bmaptool copy myboard-image-myboard.wic.bz2 /dev/sdX

**Boot and Validate:**

.. code-block:: bash

   # Insert SD card, power on board
   # Watch serial console (115200 8N1)
   
   # Check kernel
   uname -a
   # Linux myboard 6.1.75-myboard #1 PREEMPT Tue Jan 18 2026 armv7l GNU/Linux
   
   # Check device tree
   cat /proc/device-tree/model
   # MyBoard Custom Board
   
   # Check hardware
   cat /proc/cpuinfo
   lsmod
   dmesg | grep -i myboard

7.2 BSP Testing Checklist
--------------------------

**Hardware Validation:**

.. code-block:: bash

   # Serial console
   echo "test" > /dev/ttyO0
   
   # Ethernet
   ifconfig eth0 up
   ping 8.8.8.8
   
   # USB
   lsusb
   dmesg | grep -i usb
   
   # SD/MMC
   fdisk -l /dev/mmcblk0
   mount /dev/mmcblk0p1 /mnt
   
   # GPIO
   echo 60 > /sys/class/gpio/export
   echo out > /sys/class/gpio/gpio60/direction
   echo 1 > /sys/class/gpio/gpio60/value
   
   # I2C
   i2cdetect -y 0
   
   # SPI
   ls /dev/spidev*
   
   # CAN
   ip link set can0 type can bitrate 125000
   ip link set can0 up
   candump can0

================================================================================
8. Key Takeaways
================================================================================

.. code-block:: text

   BSP Layer Structure:
   ====================
   meta-mybsp/
   ├── conf/machine/myboard.conf     # Machine config
   ├── recipes-bsp/u-boot/           # Bootloader
   ├── recipes-kernel/linux/         # Kernel
   └── recipes-core/images/          # Custom images
   
   Machine Configuration:
   ======================
   MACHINE_FEATURES = "serial ethernet usb"
   PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
   KERNEL_IMAGETYPE = "zImage"
   KERNEL_DEVICETREE = "myboard.dtb"
   UBOOT_MACHINE = "myboard_defconfig"
   SERIAL_CONSOLES = "115200;ttyO0"
   IMAGE_FSTYPES = "wic ext4 tar.bz2"
   
   U-Boot Customization:
   =====================
   u-boot_%.bbappend
   - Add patches for board support
   - Custom defconfig
   - Boot environment (uEnv.txt)
   
   Kernel Customization:
   =====================
   linux-yocto_%.bbappend
   - Kernel config fragments (.cfg)
   - Device tree (.dts)
   - Driver patches
   KERNEL_DEVICETREE = "myboard.dtb"
   
   Custom Image:
   =============
   inherit core-image
   IMAGE_INSTALL += "kernel-modules myboard-app"
   IMAGE_FEATURES += "ssh-server-openssh"
   IMAGE_FSTYPES = "wic ext4"
   
   WIC Image:
   ==========
   # myboard.wks
   part /boot --fstype=vfat --size 64M
   part / --source rootfs --fstype=ext4
   bootloader --ptable msdos
   
   Build & Deploy:
   ===============
   MACHINE=myboard bitbake myboard-image
   sudo dd if=image.wic of=/dev/sdX
   
   Validation:
   ===========
   - Boot log analysis
   - Hardware peripherals (I2C, SPI, CAN, USB)
   - Network connectivity
   - GPIO/LED testing
   - Storage (SD, eMMC, Flash)

================================================================================
END OF CHEATSHEET
================================================================================
