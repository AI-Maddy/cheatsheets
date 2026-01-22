====================================
U-Boot Complete Reference & Guide
====================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

Das U-Boot ("Universal Bootloader") is the most popular open-source bootloader for embedded systems.

Key Features
------------

+--------------------------------+----------------------------------------------------------+
| **Feature**                    | **Description**                                          |
+================================+==========================================================+
| Architecture Support           | ARM, x86, MIPS, PowerPC, RISC-V, ARC, NDS32, etc.       |
+--------------------------------+----------------------------------------------------------+
| Network Boot                   | TFTP, NFS, HTTP, PXE                                     |
+--------------------------------+----------------------------------------------------------+
| Storage Support                | eMMC, SD, USB, SATA, NVMe, NAND, NOR                    |
+--------------------------------+----------------------------------------------------------+
| File Systems                   | ext2/3/4, FAT, UBIFS, JFFS2, SquashFS                   |
+--------------------------------+----------------------------------------------------------+
| Scripting                      | Hush shell, environment variables                        |
+--------------------------------+----------------------------------------------------------+
| Firmware Update                | DFU, Fastboot, UMS                                       |
+--------------------------------+----------------------------------------------------------+
| Security                       | Verified Boot, Secure Boot, TPM                          |
+--------------------------------+----------------------------------------------------------+

🔧 Essential Commands
======================

Environment Variables
---------------------

.. code-block:: bash

   # Display all variables
   printenv
   env print
   
   # Display specific variable
   printenv bootargs
   
   # Set variable (temporary)
   setenv myvar myvalue
   setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2'
   
   # Save to persistent storage
   saveenv
   
   # Delete variable
   setenv myvar
   
   # Edit interactively
   editenv bootargs

Memory Operations
-----------------

**Memory Display:**

.. code-block:: bash

   # Display memory (hex)
   md.b 0x80000000 100    # Display 100 bytes
   md.w 0x80000000 50     # Display 50 words (16-bit)
   md.l 0x80000000 25     # Display 25 long words (32-bit)
   
   # Memory modify
   mm.l 0x80000000        # Modify memory interactively
   
   # Memory write
   mw.l 0x80000000 0xdeadbeef 1    # Write value to address
   
   # Memory copy
   cp.b 0x80000000 0x82000000 0x100000   # Copy 1MB
   
   # Memory compare
   cmp.b 0x80000000 0x82000000 0x100000
   
   # Memory test
   mtest 0x80000000 0x90000000 100   # Test 256MB, 100 iterations

Storage Operations
------------------

**MMC/SD Card:**

.. code-block:: bash

   # List MMC devices
   mmc list
   
   # Select device
   mmc dev 0              # Select MMC device 0
   mmc dev 1 0            # Select device 1, partition 0
   
   # Display info
   mmc info
   mmc part               # Show partition table
   
   # Read from MMC to RAM
   mmc read 0x80000000 0x0 0x1000    # Read 0x1000 blocks from block 0
   
   # Write from RAM to MMC
   mmc write 0x80000000 0x0 0x1000
   
   # Erase MMC
   mmc erase 0x0 0x1000

**USB Storage:**

.. code-block:: bash

   # Initialize USB
   usb start
   usb reset
   
   # List devices
   usb tree
   usb storage
   usb info
   
   # Read from USB
   usb dev 0
   fatls usb 0:1          # List files on partition 1
   fatload usb 0:1 0x80000000 zImage    # Load file to RAM
   
   # USB Mass Storage mode
   ums 0 mmc 0            # Export MMC 0 as USB mass storage

**NAND Flash:**

.. code-block:: bash

   # Display NAND info
   nand info
   
   # Read NAND
   nand read 0x80000000 0x0 0x100000    # Read 1MB from offset 0
   
   # Write NAND
   nand write 0x80000000 0x0 0x100000
   
   # Erase NAND
   nand erase 0x0 0x100000
   nand erase.chip        # Erase entire chip
   
   # Bad block management
   nand bad
   nand markbad 0x0

Network Commands
----------------

**Network Configuration:**

.. code-block:: bash

   # Set network variables
   setenv ipaddr 192.168.1.100
   setenv serverip 192.168.1.1
   setenv netmask 255.255.255.0
   setenv gatewayip 192.168.1.1
   setenv ethaddr 00:11:22:33:44:55
   
   # Test network
   ping 192.168.1.1
   
   # DHCP
   dhcp
   
   # Display network info
   bdinfo

**TFTP Operations:**

.. code-block:: bash

   # Load file via TFTP
   tftp 0x80000000 zImage
   tftp 0x82000000 device-tree.dtb
   
   # Set TFTP block size (for slow networks)
   setenv tftpblocksize 1024
   
   # TFTP with specific server
   tftpboot 0x80000000 192.168.1.50:zImage

**NFS Boot:**

.. code-block:: bash

   # Set NFS parameters
   setenv nfsroot /export/rootfs
   setenv rootpath /export/rootfs
   setenv bootargs 'console=ttyS0,115200 root=/dev/nfs nfsroot=${serverip}:${nfsroot},v3,tcp ip=dhcp'
   
   # Load kernel and dtb via NFS
   nfs 0x80000000 ${serverip}:/tftpboot/zImage
   nfs 0x82000000 ${serverip}:/tftpboot/dtb

Boot Commands
-------------

.. code-block:: bash

   # Boot kernel from memory
   bootm 0x80000000              # Boot uImage
   booti 0x80000000 - 0x82000000 # Boot Image (kernel + dtb)
   bootz 0x80000000 - 0x82000000 # Boot zImage (kernel + dtb)
   
   # Boot with initrd
   bootm 0x80000000 0x84000000 0x82000000  # kernel, initrd, dtb
   
   # Boot from storage
   ext4load mmc 0:1 0x80000000 /boot/zImage
   ext4load mmc 0:1 0x82000000 /boot/device-tree.dtb
   bootz 0x80000000 - 0x82000000
   
   # Boot distro command (auto-detect)
   run distro_bootcmd
   
   # Boot script
   source 0x80000000      # Execute script at address
   
   # Reset system
   reset

File System Commands
--------------------

**FAT File System:**

.. code-block:: bash

   # List files
   fatls mmc 0:1          # List partition 1
   fatls mmc 0:1 /boot    # List directory
   
   # Load file
   fatload mmc 0:1 0x80000000 zImage
   fatload mmc 0:1 0x80000000 /boot/zImage
   
   # Get file info
   fatinfo mmc 0:1
   fatsize mmc 0:1 zImage
   
   # Write file
   fatwrite mmc 0:1 0x80000000 newfile.bin 0x100000

**ext2/3/4 File System:**

.. code-block:: bash

   # List files
   ext4ls mmc 0:2
   ext4ls mmc 0:2 /boot
   
   # Load file
   ext4load mmc 0:2 0x80000000 /boot/vmlinuz
   
   # Get file size
   ext4size mmc 0:2 /boot/vmlinuz
   
   # Write file (if enabled)
   ext4write mmc 0:2 0x80000000 /boot/newfile 0x100000

📜 U-Boot Scripting
====================

Script Format
-------------

**Boot Script Example:**

.. code-block:: bash

   # boot.cmd - Source file
   echo "Starting custom boot sequence..."
   
   # Set variables
   setenv bootdelay 3
   setenv kernel_addr_r 0x80000000
   setenv fdt_addr_r 0x82000000
   
   # Load kernel
   if ext4load mmc 0:1 ${kernel_addr_r} /boot/zImage; then
       echo "Kernel loaded successfully"
   else
       echo "Failed to load kernel"
       exit
   fi
   
   # Load device tree
   ext4load mmc 0:1 ${fdt_addr_r} /boot/device-tree.dtb
   
   # Set boot arguments
   setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2 rootwait rw'
   
   # Boot
   bootz ${kernel_addr_r} - ${fdt_addr_r}

**Compile script:**

.. code-block:: bash

   # Compile to binary format
   mkimage -A arm -O linux -T script -C none -a 0 -e 0 \
       -n "Boot Script" -d boot.cmd boot.scr
   
   # In U-Boot, execute:
   fatload mmc 0:1 0x80000000 boot.scr
   source 0x80000000

Conditional Logic
-----------------

.. code-block:: bash

   # If-then-else
   if test $bootcount -gt 3; then
       echo "Boot failed 3 times, entering recovery"
       run recovery_boot
   else
       run normal_boot
   fi
   
   # Test file existence
   if ext4load mmc 0:1 0x80000000 /boot/zImage; then
       echo "File exists"
   fi
   
   # Compare strings
   if test "${boot_mode}" = "recovery"; then
       run recovery_boot
   fi
   
   # Numeric comparison
   if test $bootcount -eq 0; then
       echo "First boot"
   fi

Loops
-----

.. code-block:: bash

   # For loop
   for i in 1 2 3 4 5; do
       echo "Iteration $i"
   done
   
   # While loop (limited support)
   setenv counter 0
   while test $counter -lt 10; do
       echo "Counter: $counter"
       setexpr counter $counter + 1
   done

Functions (as environment variables)
-------------------------------------

.. code-block:: bash

   # Define boot functions
   setenv boot_mmc 'ext4load mmc 0:1 ${kernel_addr_r} /boot/zImage; ext4load mmc 0:1 ${fdt_addr_r} /boot/dtb; bootz ${kernel_addr_r} - ${fdt_addr_r}'
   
   setenv boot_net 'tftp ${kernel_addr_r} zImage; tftp ${fdt_addr_r} dtb; bootz ${kernel_addr_r} - ${fdt_addr_r}'
   
   setenv bootcmd 'run boot_mmc || run boot_net'
   
   saveenv

🌐 Network Boot Configuration
===============================

PXE Boot
--------

**U-Boot Configuration:**

.. code-block:: bash

   # Set PXE boot variables
   setenv autoload no
   setenv pxefile_addr_r 0x84000000
   
   # DHCP and PXE
   dhcp
   pxe get
   pxe boot

**PXE Configuration (pxelinux.cfg/default):**

.. code-block:: text

   DEFAULT linux
   PROMPT 0
   TIMEOUT 30
   
   LABEL linux
       MENU LABEL Boot Linux
       KERNEL zImage
       DEVICETREE device-tree.dtb
       APPEND console=ttyS0,115200 root=/dev/nfs nfsroot=192.168.1.1:/export/rootfs ip=dhcp

HTTP Boot
---------

.. code-block:: bash

   # Load via HTTP (if enabled)
   setenv httpserverip 192.168.1.100
   wget 0x80000000 http://192.168.1.100/zImage
   wget 0x82000000 http://192.168.1.100/device-tree.dtb
   bootz 0x80000000 - 0x82000000

🔐 Secure Boot & Verified Boot
================================

Verified Boot (FIT Image)
--------------------------

**Create FIT Image:**

.. code-block:: text

   # kernel.its - FIT image description
   /dts-v1/;
   / {
       description = "Signed Kernel FIT Image";
       #address-cells = <1>;
       
       images {
           kernel@1 {
               description = "Linux Kernel";
               data = /incbin/("zImage");
               type = "kernel";
               arch = "arm";
               os = "linux";
               compression = "none";
               load = <0x80000000>;
               entry = <0x80000000>;
               hash@1 {
                   algo = "sha256";
               };
           };
           
           fdt@1 {
               description = "Device Tree";
               data = /incbin/("device-tree.dtb");
               type = "flat_dt";
               arch = "arm";
               compression = "none";
               hash@1 {
                   algo = "sha256";
               };
           };
       };
       
       configurations {
           default = "conf@1";
           conf@1 {
               description = "Boot Configuration";
               kernel = "kernel@1";
               fdt = "fdt@1";
               signature@1 {
                   algo = "sha256,rsa2048";
                   key-name-hint = "dev";
                   sign-images = "fdt", "kernel";
               };
           };
       };
   };

**Build and Sign:**

.. code-block:: bash

   # Generate keys
   openssl genrsa -F4 -out keys/dev.key 2048
   openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt
   
   # Create FIT image
   mkimage -f kernel.its -K u-boot.dtb -k keys -r image.fit
   
   # Verify signature
   fit_check_sign -f image.fit -k u-boot.dtb

**U-Boot Configuration:**

.. code-block:: kconfig

   # Enable verified boot in defconfig
   CONFIG_FIT=y
   CONFIG_FIT_SIGNATURE=y
   CONFIG_RSA=y
   CONFIG_SPL_FIT_SIGNATURE=y
   CONFIG_OF_CONTROL=y
   CONFIG_OF_SEPARATE=y

**Boot Signed Image:**

.. code-block:: bash

   # Load FIT image
   fatload mmc 0:1 0x80000000 image.fit
   
   # Verify and boot
   bootm 0x80000000

UEFI Secure Boot Integration
-----------------------------

.. code-block:: bash

   # Enable UEFI in U-Boot config
   CONFIG_EFI_LOADER=y
   CONFIG_CMD_BOOTEFI=y
   CONFIG_EFI_SECURE_BOOT=y
   
   # Boot UEFI application
   load mmc 0:1 0x80000000 EFI/BOOT/BOOTARM.EFI
   bootefi 0x80000000

🛠️ Device Tree Manipulation
==============================

FDT Commands
------------

.. code-block:: bash

   # Load device tree
   fatload mmc 0:1 0x82000000 device-tree.dtb
   
   # Set working FDT
   fdt addr 0x82000000
   
   # Display FDT structure
   fdt print /
   fdt print /soc/serial@0
   
   # Get property
   fdt get value status /soc/serial@0 status
   
   # Set property
   fdt set /chosen bootargs "console=ttyS0,115200 root=/dev/mmcblk0p2"
   fdt set /soc/serial@0 status "okay"
   
   # Resize FDT (add space)
   fdt resize 8192
   
   # Create node
   fdt mknode / newnode
   
   # Remove node
   fdt rm /soc/unused_device
   
   # Apply overlays
   fdt apply 0x84000000   # Apply overlay at address

Device Tree Overlays
--------------------

**Overlay Example (i2c-device.dts):**

.. code-block:: dts

   /dts-v1/;
   /plugin/;
   
   / {
       compatible = "vendor,board";
       
       fragment@0 {
           target = <&i2c1>;
           __overlay__ {
               #address-cells = <1>;
               #size-cells = <0>;
               
               sensor@48 {
                   compatible = "ti,tmp102";
                   reg = <0x48>;
                   status = "okay";
               };
           };
       };
   };

**Compile and Apply:**

.. code-block:: bash

   # Compile overlay
   dtc -@ -I dts -O dtb -o i2c-device.dtbo i2c-device.dts
   
   # In U-Boot
   fatload mmc 0:1 0x82000000 device-tree.dtb
   fdt addr 0x82000000
   fdt resize 8192
   fatload mmc 0:1 0x84000000 i2c-device.dtbo
   fdt apply 0x84000000
   bootz ${kernel_addr_r} - 0x82000000

🔨 Building U-Boot
===================

Standard Build
--------------

.. code-block:: bash

   # Clone repository
   git clone https://source.denx.de/u-boot/u-boot.git
   cd u-boot
   
   # List available boards
   ls configs/ | grep defconfig
   
   # Configure for specific board
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- am335x_evm_defconfig
   
   # Optional: customize config
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
   
   # Build
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   
   # Output files:
   # - u-boot.bin (main bootloader)
   # - u-boot.img (with U-Boot header)
   # - u-boot.elf (with debug symbols)
   # - SPL/u-boot-spl.bin (if SPL enabled)

Custom Board Configuration
---------------------------

**Create Board Support:**

.. code-block:: bash

   # Directory structure
   board/vendor/myboard/
   ├── Kconfig
   ├── MAINTAINERS
   ├── Makefile
   ├── myboard.c
   └── README

**board/vendor/myboard/Kconfig:**

.. code-block:: kconfig

   if TARGET_MYBOARD
   
   config SYS_BOARD
       default "myboard"
   
   config SYS_VENDOR
       default "vendor"
   
   config SYS_CONFIG_NAME
       default "myboard"
   
   endif

**configs/myboard_defconfig:**

.. code-block:: text

   CONFIG_ARM=y
   CONFIG_ARCH_MX6=y
   CONFIG_TARGET_MYBOARD=y
   CONFIG_SYS_MALLOC_F_LEN=0x2000
   CONFIG_DM=y
   CONFIG_DM_GPIO=y
   CONFIG_DM_MMC=y
   CONFIG_DM_SERIAL=y
   CONFIG_BOOTDELAY=3
   CONFIG_BOOTCOMMAND="run mmcboot"
   CONFIG_DEFAULT_DEVICE_TREE="imx6ull-myboard"
   # ... more config options

**include/configs/myboard.h:**

.. code-block:: c

   #ifndef __MYBOARD_CONFIG_H
   #define __MYBOARD_CONFIG_H
   
   #include "mx6_common.h"
   
   /* Physical Memory Map */
   #define CONFIG_SYS_SDRAM_BASE       MMDC0_ARB_BASE_ADDR
   #define CONFIG_SYS_INIT_RAM_ADDR    IRAM_BASE_ADDR
   #define CONFIG_SYS_INIT_RAM_SIZE    IRAM_SIZE
   
   /* Environment */
   #define CONFIG_EXTRA_ENV_SETTINGS \
       "console=ttymxc0\0" \
       "baudrate=115200\0" \
       "kernel_addr_r=0x82000000\0" \
       "fdt_addr_r=0x88000000\0" \
       "mmcroot=/dev/mmcblk0p2 rootwait rw\0" \
       "mmcargs=setenv bootargs console=${console},${baudrate} root=${mmcroot}\0" \
       "loadimage=fatload mmc 0:1 ${kernel_addr_r} zImage\0" \
       "loadfdt=fatload mmc 0:1 ${fdt_addr_r} ${fdtfile}\0" \
       "mmcboot=run mmcargs; run loadimage; run loadfdt; bootz ${kernel_addr_r} - ${fdt_addr_r}\0"
   
   #endif /* __MYBOARD_CONFIG_H */

SPL (Secondary Program Loader)
-------------------------------

**Enable SPL:**

.. code-block:: kconfig

   CONFIG_SPL=y
   CONFIG_SPL_FRAMEWORK=y
   CONFIG_SPL_LOAD_FIT=y
   CONFIG_SPL_MMC_SUPPORT=y
   CONFIG_SPL_FAT_SUPPORT=y
   CONFIG_SPL_SERIAL_SUPPORT=y

**Boot Flow with SPL:**

.. code-block:: text

   ROM Code → SPL (u-boot-spl.bin) → U-Boot (u-boot.img) → Kernel

**SPL Configuration:**

.. code-block:: c

   // board/vendor/myboard/spl.c
   void spl_board_init(void)
   {
       /* Initialize DRAM */
       /* Setup pinmux */
       /* Initialize boot device */
   }
   
   int spl_start_uboot(void)
   {
       /* Decide whether to boot U-Boot or directly load OS */
       return 1;  /* Boot U-Boot */
   }

🐛 Debugging U-Boot
====================

Debug Output
------------

**Enable Debug:**

.. code-block:: kconfig

   CONFIG_LOGLEVEL=7
   CONFIG_CMD_LOG=y
   CONFIG_LOG=y
   CONFIG_LOG_MAX_LEVEL=7

**Debug Commands:**

.. code-block:: bash

   # Display board info
   bdinfo
   
   # Display version
   version
   
   # CPU info
   cpu detail
   
   # Display devices
   dm tree
   dm uclass
   
   # Memory map
   base
   
   # Trace execution
   trace stats
   trace calls

Serial Console
--------------

**Connect via Serial:**

.. code-block:: bash

   # Linux
   screen /dev/ttyUSB0 115200
   picocom -b 115200 /dev/ttyUSB0
   minicom -D /dev/ttyUSB0 -b 115200
   
   # Stop autoboot by pressing key during countdown
   # Enter U-Boot command prompt

JTAG Debugging
--------------

**OpenOCD Configuration:**

.. code-block:: text

   # openocd.cfg
   source [find interface/jlink.cfg]
   source [find target/imx6.cfg]
   
   init
   reset init
   halt

**GDB Session:**

.. code-block:: bash

   # Terminal 1: Start OpenOCD
   openocd -f openocd.cfg
   
   # Terminal 2: Start GDB
   arm-linux-gnueabihf-gdb u-boot
   
   (gdb) target remote localhost:3333
   (gdb) load
   (gdb) break board_init_r
   (gdb) continue
   (gdb) step
   (gdb) print *gd

Memory Dump Analysis
--------------------

.. code-block:: bash

   # Save memory to file (via TFTP)
   mw.l 0x80000000 0x12345678 0x100
   tftp 0x80000000 dump.bin 0x400
   
   # Or via USB
   ums 0 mmc 0  # Export as USB mass storage

🚀 Advanced Features
=====================

Fastboot
--------

**Enable Fastboot:**

.. code-block:: kconfig

   CONFIG_USB_GADGET=y
   CONFIG_USB_GADGET_DOWNLOAD=y
   CONFIG_FASTBOOT=y
   CONFIG_FASTBOOT_FLASH=y
   CONFIG_FASTBOOT_FLASH_MMC=y

**U-Boot Commands:**

.. code-block:: bash

   # Start fastboot over USB
   fastboot 0
   
   # Or over UDP
   fastboot udp

**Host Side (Android Tools):**

.. code-block:: bash

   # List devices
   fastboot devices
   
   # Flash partitions
   fastboot flash boot boot.img
   fastboot flash system system.img
   
   # Erase partition
   fastboot erase userdata
   
   # Boot kernel without flashing
   fastboot boot zImage
   
   # Reboot
   fastboot reboot

DFU (Device Firmware Upgrade)
------------------------------

**Enable DFU:**

.. code-block:: kconfig

   CONFIG_USB_GADGET=y
   CONFIG_DFU=y
   CONFIG_DFU_MMC=y
   CONFIG_DFU_RAM=y

**DFU Configuration:**

.. code-block:: bash

   # Define DFU entities
   setenv dfu_alt_info 'bootloader raw 0x0 0x400;kernel part 0 1;rootfs part 0 2'
   
   # Start DFU
   dfu 0 mmc 0

**Host Side:**

.. code-block:: bash

   # List DFU devices
   dfu-util -l
   
   # Upload firmware
   dfu-util -a 0 -D u-boot.bin
   dfu-util -a 1 -D zImage
   
   # Download from device
   dfu-util -a 0 -U backup.bin

A/B Partitioning (Dual Boot)
-----------------------------

**Environment Variables:**

.. code-block:: bash

   # Setup A/B partitions
   setenv bootslot a
   setenv kernel_a /dev/mmcblk0p2
   setenv kernel_b /dev/mmcblk0p3
   setenv rootfs_a /dev/mmcblk0p4
   setenv rootfs_b /dev/mmcblk0p5
   
   # Boot logic
   setenv try_boot_a 'if ext4load mmc 0:2 ${kernel_addr_r} /boot/zImage; then setenv bootargs root=${rootfs_a}; bootz ${kernel_addr_r} - ${fdt_addr_r}; fi'
   
   setenv try_boot_b 'if ext4load mmc 0:3 ${kernel_addr_r} /boot/zImage; then setenv bootargs root=${rootfs_b}; bootz ${kernel_addr_r} - ${fdt_addr_r}; fi'
   
   setenv bootcmd 'if test "${bootslot}" = "a"; then run try_boot_a || run try_boot_b; else run try_boot_b || run try_boot_a; fi'

**Fallback with Boot Counter:**

.. code-block:: bash

   CONFIG_BOOTCOUNT_LIMIT=y
   CONFIG_BOOTCOUNT_ENV=y
   
   # In environment
   setenv bootlimit 3
   setenv bootcmd 'if test ${bootcount} -gt ${bootlimit}; then setenv bootslot b; fi; run normal_boot'

Watchdog
--------

.. code-block:: bash

   # Enable watchdog
   CONFIG_WATCHDOG=y
   CONFIG_WATCHDOG_TIMEOUT_MSECS=60000
   
   # Commands
   wdt dev                # List watchdog devices
   wdt start 60000        # Start with 60s timeout
   wdt reset              # Reset watchdog
   wdt expire 1           # Force expire (test)

💾 Persistent Storage Configuration
====================================

Environment Storage Options
---------------------------

**MMC/SD Card:**

.. code-block:: kconfig

   CONFIG_ENV_IS_IN_MMC=y
   CONFIG_ENV_SIZE=0x2000
   CONFIG_ENV_OFFSET=0x400000
   CONFIG_SYS_MMC_ENV_DEV=0
   CONFIG_SYS_MMC_ENV_PART=0

**SPI Flash:**

.. code-block:: kconfig

   CONFIG_ENV_IS_IN_SPI_FLASH=y
   CONFIG_ENV_SIZE=0x2000
   CONFIG_ENV_OFFSET=0x100000
   CONFIG_ENV_SECT_SIZE=0x10000

**NAND Flash:**

.. code-block:: kconfig

   CONFIG_ENV_IS_IN_NAND=y
   CONFIG_ENV_SIZE=0x20000
   CONFIG_ENV_OFFSET=0x100000
   CONFIG_ENV_RANGE=0x100000

**FAT File System:**

.. code-block:: kconfig

   CONFIG_ENV_IS_IN_FAT=y
   CONFIG_ENV_FAT_INTERFACE="mmc"
   CONFIG_ENV_FAT_DEVICE_AND_PART="0:1"
   CONFIG_ENV_FAT_FILE="uboot.env"

Redundant Environment
---------------------

.. code-block:: kconfig

   CONFIG_ENV_IS_IN_MMC=y
   CONFIG_SYS_REDUNDAND_ENVIRONMENT=y
   CONFIG_ENV_OFFSET=0x400000
   CONFIG_ENV_OFFSET_REDUND=0x410000

📱 Common Board Examples
==========================

Raspberry Pi
------------

.. code-block:: bash

   # Build for Raspberry Pi 4
   make CROSS_COMPILE=aarch64-linux-gnu- rpi_4_defconfig
   make CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
   
   # config.txt additions
   kernel=u-boot.bin
   
   # Boot
   fatload mmc 0:1 ${kernel_addr_r} zImage
   fatload mmc 0:1 ${fdt_addr_r} bcm2711-rpi-4-b.dtb
   bootz ${kernel_addr_r} - ${fdt_addr_r}

BeagleBone Black
----------------

.. code-block:: bash

   # Build
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- am335x_evm_defconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   
   # Install (SD card at /dev/sdb)
   sudo dd if=MLO of=/dev/sdb bs=512 seek=256 conv=fsync
   sudo dd if=u-boot.img of=/dev/sdb bs=512 seek=768 conv=fsync

i.MX6 Boards
------------

.. code-block:: bash

   # Build for i.MX6ULL
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- mx6ull_14x14_evk_defconfig
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j$(nproc)
   
   # Flash to SD (boot from offset 0x400)
   sudo dd if=u-boot.imx of=/dev/sdb bs=1k seek=1 conv=fsync

QEMU Testing
------------

.. code-block:: bash

   # Build for QEMU ARM Virt
   make qemu_arm_defconfig
   make -j$(nproc)
   
   # Run
   qemu-system-arm -M virt -nographic -bios u-boot.bin

🔧 Troubleshooting
===================

Common Issues
-------------

+----------------------------------+-----------------------------------------------+
| **Issue**                        | **Solution**                                  |
+==================================+===============================================+
| Board won't boot                 | Check serial console, verify power supply     |
+----------------------------------+-----------------------------------------------+
| No output on serial              | Verify baud rate, check TX/RX connections    |
+----------------------------------+-----------------------------------------------+
| Environment not saving           | Check CONFIG_ENV_IS_IN_*, run saveenv        |
+----------------------------------+-----------------------------------------------+
| Network not working              | Verify ethaddr, check cable/switch           |
+----------------------------------+-----------------------------------------------+
| MMC detection fails              | Check power, verify device tree              |
+----------------------------------+-----------------------------------------------+
| Kernel won't boot                | Check load addresses, verify bootargs        |
+----------------------------------+-----------------------------------------------+

Recovery Methods
----------------

.. code-block:: bash

   # Reset environment to defaults
   env default -a
   saveenv
   
   # Boot from serial (UART boot mode)
   # Use vendor-specific tools (e.g., NXP mfgtool, TI uniflash)
   
   # JTAG recovery
   # Flash U-Boot via OpenOCD

Performance Tuning
------------------

.. code-block:: bash

   # Optimize boot time
   setenv bootdelay 0        # Skip delay
   setenv silent 1           # Reduce output
   
   # Cache settings
   icache on
   dcache on
   
   # Network optimization
   setenv tftpblocksize 1468  # Optimize for MTU

📚 References
==============

Documentation
-------------

* **Official Documentation**: https://u-boot.readthedocs.io/
* **Source Repository**: https://source.denx.de/u-boot/u-boot
* **Mailing List**: u-boot@lists.denx.de
* **Wiki**: https://www.denx.de/wiki/U-Boot

Key Files
---------

* ``README`` - Main documentation
* ``doc/`` - Detailed documentation
* ``board/`` - Board-specific code
* ``configs/`` - Default configurations
* ``include/configs/`` - Board config headers
* ``arch/`` - Architecture-specific code
* ``drivers/`` - Device drivers
* ``common/`` - Common code

================================
Last Updated: January 2026
Version: 3.0
================================
