================================================================================
Embedded Linux: Bootloaders (U-Boot) - Complete Guide
================================================================================

:Author: Technical Documentation Team
:Date: January 18, 2026
:Version: 1.0
:Target: Embedded Linux Developers
:U-Boot: 2015.07, 2023.10+ compatible
:Reference: Linux Embedded Development (Module 1 Ch3, Module 3 Ch3)

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
TL;DR - Quick Reference
================================================================================

**Bootloader Purpose:**

Bootloaders initialize hardware, load Linux kernel and device tree, pass boot
parameters, and transfer control to kernel.

**U-Boot Quick Commands:**

.. code-block:: bash

   # Boot sequence
   => printenv bootcmd
   => run bootcmd
   
   # Load from SD/MMC
   => mmc dev 0
   => fatload mmc 0:1 ${loadaddr} zImage
   => fatload mmc 0:1 ${fdt_addr} dtb
   => bootz ${loadaddr} - ${fdt_addr}
   
   # Network boot (TFTP)
   => setenv serverip 192.168.1.100
   => tftp ${loadaddr} zImage
   => tftp ${fdt_addr} am335x-boneblack.dtb
   => bootz ${loadaddr} - ${fdt_addr}
   
   # Environment
   => setenv bootargs 'console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw rootwait'
   => saveenv

**Boot Flow:**

.. code-block:: text

   ROM Bootloader (SoC) → SPL (U-Boot Stage 1) → U-Boot → Linux Kernel

**Common U-Boot Environment Variables:**

- ``bootcmd`` - Commands executed at boot
- ``bootargs`` - Kernel command line
- ``loadaddr`` - Kernel load address
- ``fdt_addr`` - Device tree load address
- ``serverip`` - TFTP server IP
- ``ipaddr`` - Board IP address

================================================================================
1. Bootloader Fundamentals
================================================================================

1.1 What is a Bootloader?
--------------------------

**Definition:**

A bootloader is the first software that runs after power-on or reset. It
initializes minimal hardware, loads the operating system kernel into RAM,
and transfers execution to it.

**Key Responsibilities:**

.. code-block:: text

   1. Hardware Initialization
      - CPU clock configuration
      - DDR RAM initialization
      - Flash memory configuration
      - Peripheral initialization (UART, network, storage)
   
   2. Boot Medium Support
      - SD/MMC cards
      - NAND/NOR flash
      - USB
      - Network (TFTP, NFS)
      - SPI flash
   
   3. Kernel Loading
      - Load kernel image from storage
      - Load device tree blob (DTB)
      - Load initial ramdisk (optional)
   
   4. Boot Parameters
      - Construct kernel command line (bootargs)
      - Pass device tree to kernel
      - Set machine ID (legacy ARM)
   
   5. Transfer Control
      - Jump to kernel entry point
      - Kernel takes over system

**Why U-Boot?**

.. code-block:: text

   ✓ Open source (GPL)
   ✓ Supports 1000+ boards and SoCs
   ✓ Active development community
   ✓ Rich feature set
   ✓ Flexible configuration
   ✓ Excellent documentation
   ✓ Industry standard for ARM embedded

**Alternatives to U-Boot:**

+----------------+------------------------+---------------------------------+
| Bootloader     | Use Case               | Characteristics                 |
+================+========================+=================================+
| U-Boot         | General embedded       | Feature-rich, flexible          |
+----------------+------------------------+---------------------------------+
| Barebox        | Modern embedded        | Cleaner codebase, less boards   |
+----------------+------------------------+---------------------------------+
| GRUB           | x86 systems            | PC/server bootloader            |
+----------------+------------------------+---------------------------------+
| UEFI           | Modern x86/ARM         | Standardized, complex           |
+----------------+------------------------+---------------------------------+
| Vendor-specific| Specific SoCs          | Optimized but proprietary       |
| (e.g., iMX boot|                        |                                 |
+----------------+------------------------+---------------------------------+

1.2 Boot Sequence Overview
---------------------------

**Multi-Stage Boot Process:**

.. code-block:: text

   Power-On/Reset
        │
        ▼
   ┌────────────────────────────────────────┐
   │ ROM Bootloader (Boot ROM)              │
   │ - Built into SoC (cannot modify)       │
   │ - Minimal hardware init                │
   │ - Load SPL from boot medium            │
   └────────┬───────────────────────────────┘
            │
            ▼
   ┌────────────────────────────────────────┐
   │ SPL (Secondary Program Loader)         │
   │ - U-Boot SPL or vendor-specific        │
   │ - Initialize DDR RAM                   │
   │ - Size: ~30-100 KB (fits in SRAM)      │
   │ - Load full U-Boot                     │
   └────────┬───────────────────────────────┘
            │
            ▼
   ┌────────────────────────────────────────┐
   │ U-Boot (Full Bootloader)               │
   │ - Complete hardware initialization     │
   │ - User interaction (command line)      │
   │ - Load kernel, DTB, initramfs          │
   │ - Boot Linux                           │
   └────────┬───────────────────────────────┘
            │
            ▼
   ┌────────────────────────────────────────┐
   │ Linux Kernel                           │
   │ - Kernel decompression                 │
   │ - Device tree parsing                  │
   │ - Driver initialization                │
   │ - Mount root filesystem                │
   │ - Start init process                   │
   └────────────────────────────────────────┘

**Why Multi-Stage Boot?**

.. code-block:: text

   ROM Bootloader Limitations:
   - Tiny code space (few KB)
   - No DDR RAM available (only SRAM)
   - Limited boot medium support
   
   SPL (Secondary Program Loader):
   - Small enough to fit in SRAM (64-256 KB typical)
   - Initializes DDR RAM
   - Loads full U-Boot into DDR
   
   U-Boot (Full):
   - Runs from DDR RAM (plenty of space)
   - Full feature set
   - Interactive command line
   - Multiple boot options

**Boot Medium Priority:**

.. code-block:: text

   Typical SoC Boot Sequence (configurable):
   1. SD/MMC card (if present)
   2. eMMC
   3. NAND flash
   4. SPI flash
   5. USB (recovery mode)
   6. Network (TFTP/PXE)
   
   Controlled by:
   - Hardware boot pins
   - eFuses (one-time programmable)
   - Boot ROM configuration

1.3 U-Boot Architecture
------------------------

**Directory Structure:**

.. code-block:: text

   u-boot/
   ├── arch/                  # Architecture-specific code
   │   ├── arm/              # ARM architecture
   │   │   ├── cpu/          # CPU-specific (Cortex-A8, A9, etc.)
   │   │   ├── dts/          # Device tree sources
   │   │   ├── include/      # ARM headers
   │   │   └── lib/          # ARM libraries
   │   ├── mips/             # MIPS architecture
   │   └── x86/              # x86 architecture
   ├── board/                # Board-specific code
   │   ├── ti/               # Texas Instruments boards
   │   │   ├── am335x/       # BeagleBone Black, etc.
   │   │   └── am57xx/
   │   ├── freescale/        # NXP/Freescale boards
   │   └── raspberrypi/
   ├── cmd/                  # U-Boot commands
   │   ├── bootm.c           # Boot commands
   │   ├── mmc.c             # MMC commands
   │   └── net.c             # Network commands
   ├── common/               # Common code
   │   ├── board_f.c         # Board init (before relocation)
   │   ├── board_r.c         # Board init (after relocation)
   │   └── cli.c             # Command line interface
   ├── configs/              # Board defconfig files
   │   ├── am335x_evm_defconfig
   │   ├── rpi_3_defconfig
   │   └── ...
   ├── disk/                 # Partition support
   ├── drivers/              # Device drivers
   │   ├── mmc/              # MMC/SD drivers
   │   ├── mtd/              # Flash drivers
   │   ├── net/              # Ethernet drivers
   │   ├── serial/           # UART drivers
   │   └── usb/              # USB drivers
   ├── fs/                   # Filesystem support
   │   ├── ext4/             # ext4 filesystem
   │   ├── fat/              # FAT filesystem
   │   └── ubifs/            # UBIFS filesystem
   ├── include/              # Header files
   │   ├── configs/          # Board config headers
   │   └── config.h          # Main config
   ├── lib/                  # Libraries
   ├── net/                  # Networking stack
   └── tools/                # Host tools
       ├── mkimage           # Create U-Boot images
       └── mkenvimage        # Create environment images

**U-Boot Components:**

.. code-block:: text

   Core Components:
   ├── SPL (spl/)                  # First-stage loader
   ├── Command Line Interface      # Interactive shell
   ├── Device Drivers              # Hardware abstraction
   ├── File Systems                # FAT, ext4, UBIFS, etc.
   ├── Network Stack               # TCP/IP, TFTP, NFS
   ├── Image Handling              # uImage, FIT, zImage
   └── Device Tree Support         # DTB loading, modification

================================================================================
2. Building U-Boot
================================================================================

2.1 Getting U-Boot Source
--------------------------

**Download U-Boot:**

.. code-block:: bash

   # Clone from official repository
   git clone https://source.denx.de/u-boot/u-boot.git
   cd u-boot
   
   # Checkout stable version
   git checkout v2023.10
   
   # Or download tarball
   wget https://ftp.denx.de/pub/u-boot/u-boot-2023.10.tar.bz2
   tar -xjf u-boot-2023.10.tar.bz2
   cd u-boot-2023.10

**U-Boot Version Naming:**

.. code-block:: text

   Format: YYYY.MM[-rc#]
   Examples:
   - 2023.10      : October 2023 release
   - 2023.07-rc1  : July 2023 release candidate 1
   
   LTS Versions:
   - 2023.10 LTS
   - 2022.04 LTS
   - 2021.10 LTS

2.2 Configuring U-Boot
----------------------

**List Available Configurations:**

.. code-block:: bash

   # Show all board configurations
   ls configs/
   # am335x_evm_defconfig
   # rpi_3_defconfig
   # imx6ull_14x14_evk_defconfig
   # ...
   
   # Search for specific board
   ls configs/ | grep -i beagle
   # am335x_boneblack_defconfig
   # am335x_boneblack_vboot_defconfig

**Configure for Target Board:**

.. code-block:: bash

   # Method 1: Use defconfig (recommended)
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- am335x_boneblack_defconfig
   
   # Method 2: Interactive configuration
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
   
   # Save custom configuration
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- savedefconfig
   mv defconfig configs/my_custom_board_defconfig

**Key Configuration Options:**

.. code-block:: text

   Architecture select
   ├── ARM architecture
   │   └── Target select: AM33xx (BeagleBone)
   
   Boot options
   ├── Boot delay: 2 seconds
   ├── Console: ttyO0,115200n8
   └── Default boot command
   
   Command line interface
   ├── Boot commands: bootm, bootz, booti
   ├── Memory commands: md, mm, mw, cp
   ├── Device access: mmc, usb, ethernet
   └── Environment: printenv, setenv, saveenv
   
   Device Drivers
   ├── MMC/SD/SDIO: Enable
   ├── Ethernet PHY: Enable
   ├── USB: Enable host/device
   ├── SPI/I2C: Enable
   └── GPIO: Enable
   
   File systems
   ├── FAT filesystem: Enable
   ├── ext4 filesystem: Enable
   └── UBIFS: Enable (for NAND flash)

2.3 Building U-Boot
-------------------

**Build Process:**

.. code-block:: bash

   # Set toolchain
   export CROSS_COMPILE=arm-linux-gnueabihf-
   export ARCH=arm
   
   # Clean previous build
   make distclean
   
   # Configure
   make am335x_boneblack_defconfig
   
   # Build (parallel)
   make -j$(nproc)
   
   # Build artifacts:
   # - u-boot.bin       : Raw binary (for SD card)
   # - u-boot.img       : With U-Boot header (legacy)
   # - u-boot.elf       : ELF format (for debugging)
   # - MLO / SPL        : First-stage bootloader
   # - u-boot.dtb       : Device tree blob

**Build Output:**

.. code-block:: bash

   # Check build results
   ls -lh u-boot*
   # -rw-r--r-- 1 user user 456K u-boot.bin
   # -rw-r--r-- 1 user user 457K u-boot.img
   # -rw-r--r-- 1 user user 3.2M u-boot (ELF)
   
   ls -lh MLO SPL
   # -rw-r--r-- 1 user user  89K MLO
   # -rw-r--r-- 1 user user  89K SPL

**Common Build Targets:**

.. code-block:: bash

   # Build specific components
   make u-boot.bin          # Main U-Boot binary
   make u-boot.img          # U-Boot with header
   make u-boot.srec         # Motorola S-Record format
   make tools               # Build host tools (mkimage, etc.)
   
   # Build for different boards
   make ARCH=arm CROSS_COMPILE=arm-linux- rpi_3_defconfig
   make ARCH=arm64 CROSS_COMPILE=aarch64-linux- rpi_4_defconfig

2.4 Installing U-Boot
---------------------

**SD Card Installation (BeagleBone Black Example):**

.. code-block:: bash

   # Insert SD card, identify device
   lsblk
   # sdb      8:16   1  7.4G  0 disk 
   # ├─sdb1   8:17   1  128M  0 part  (boot partition)
   # └─sdb2   8:18   1  7.3G  0 part  (rootfs)
   
   # WARNING: Replace /dev/sdX with your actual SD card device
   export DISK=/dev/sdX
   
   # Method 1: Write to raw device (AM335x - BeagleBone)
   sudo dd if=MLO of=${DISK} count=1 seek=1 bs=128k
   sudo dd if=u-boot.img of=${DISK} count=2 seek=1 bs=384k
   
   # Method 2: Copy to FAT boot partition
   sudo mount ${DISK}1 /mnt
   sudo cp MLO /mnt/
   sudo cp u-boot.img /mnt/
   sudo umount /mnt
   
   # Sync and eject
   sync
   sudo eject ${DISK}

**eMMC Installation:**

.. code-block:: bash

   # From U-Boot console (booted from SD card)
   => mmc dev 1              # Select eMMC (usually device 1)
   => tftp ${loadaddr} MLO
   => mmc write ${loadaddr} 0x100 0x100
   => tftp ${loadaddr} u-boot.img
   => mmc write ${loadaddr} 0x300 0x400

**NAND Flash Installation:**

.. code-block:: bash

   # From U-Boot console
   => nand erase 0x0 0x20000          # Erase SPL area
   => tftp ${loadaddr} MLO
   => nand write ${loadaddr} 0x0 ${filesize}
   
   => nand erase 0x20000 0x100000     # Erase U-Boot area
   => tftp ${loadaddr} u-boot.img
   => nand write ${loadaddr} 0x20000 ${filesize}

================================================================================
3. U-Boot Commands and Usage
================================================================================

3.1 Essential U-Boot Commands
------------------------------

**Help and Information:**

.. code-block:: bash

   # Get command help
   => help
   => help mmc
   => help bootm
   
   # Show version
   => version
   # U-Boot 2023.10 (Jan 18 2026 - 10:00:00 +0000)
   # arm-linux-gnueabihf-gcc (crosstool-NG 1.24.0) 9.3.0
   
   # Board information
   => bdinfo
   # boot_params = 0x80000100
   # DRAM bank   = 0x00000000
   # -> start    = 0x80000000
   # -> size     = 0x20000000  (512 MiB)

**Memory Commands:**

.. code-block:: bash

   # Display memory (md)
   => md 0x80000000 10
   # 80000000: 00000000 00000000 00000000 00000000    ................
   
   # Memory write (mw)
   => mw 0x80000000 0x12345678 1
   
   # Memory copy (cp)
   => cp 0x80000000 0x81000000 100
   
   # Compare memory (cmp)
   => cmp 0x80000000 0x81000000 100

**Environment Commands:**

.. code-block:: bash

   # Print all environment variables
   => printenv
   
   # Print specific variable
   => printenv bootcmd
   # bootcmd=run findfdt; run mmcboot
   
   # Set environment variable
   => setenv myvar 'Hello World'
   => setenv ipaddr 192.168.1.100
   
   # Save environment to persistent storage
   => saveenv
   # Saving Environment to MMC... Writing to MMC(0)... done
   
   # Delete variable
   => setenv myvar
   
   # Reset to default environment
   => env default -a
   => saveenv

3.2 Boot Commands
-----------------

**bootz - Boot zImage:**

.. code-block:: bash

   # Boot zImage with device tree
   => bootz ${kernel_addr_r} - ${fdt_addr_r}
   
   # Example with explicit addresses
   => bootz 0x80800000 - 0x81000000
   
   # Boot with initramfs
   => bootz ${kernel_addr_r} ${ramdisk_addr_r}:${filesize} ${fdt_addr_r}

**bootm - Boot uImage (legacy):**

.. code-block:: bash

   # Boot uImage
   => bootm ${loadaddr}
   
   # Boot with ramdisk and device tree
   => bootm ${kernel_addr} ${ramdisk_addr} ${fdt_addr}

**booti - Boot Image (ARM64):**

.. code-block:: bash

   # Boot ARM64 Image format
   => booti ${kernel_addr_r} - ${fdt_addr_r}

**boot - Execute bootcmd:**

.. code-block:: bash

   # Run default boot sequence
   => boot
   # Equivalent to: run bootcmd

3.3 Storage Device Commands
----------------------------

**MMC/SD Card Commands:**

.. code-block:: bash

   # List MMC devices
   => mmc list
   # OMAP SD/MMC: 0
   # OMAP SD/MMC: 1 (eMMC)
   
   # Select MMC device
   => mmc dev 0              # Select SD card
   => mmc dev 1              # Select eMMC
   
   # Display MMC info
   => mmc info
   # Device: OMAP SD/MMC
   # Manufacturer ID: 3
   # OEM: 5344
   # Name: SU08G
   # Bus Width: 4-bit
   # Mode: SD High Speed (50MHz)
   # Rd Block Len: 512
   # SD version 3.0
   # High Capacity: Yes
   # Capacity: 7.4 GiB
   
   # List partition table
   => mmc part
   # Partition Map for MMC device 0
   # Part   Start LBA   End LBA     Name
   #   1    2048        264191      boot
   #   2    264192      15523839    rootfs
   
   # Read from MMC
   => mmc read ${loadaddr} 0x800 0x2000
   # MMC read: dev # 0, block # 2048, count 8192 ... 8192 blocks read: OK
   
   # Write to MMC
   => mmc write ${loadaddr} 0x800 0x2000

**USB Commands:**

.. code-block:: bash

   # Start USB subsystem
   => usb start
   # starting USB...
   # USB0:   USB EHCI 1.00
   # scanning bus 0 for devices... 2 USB Device(s) found
   
   # List USB devices
   => usb tree
   #  1  Hub (480 Mb/s, 0mA)
   #  |  u-boot EHCI Host Controller
   #  |
   #  +-2  Mass Storage (480 Mb/s, 200mA)
   #       Kingston DataTraveler 2.0 001D0F1E2E3F3E5D
   
   # Scan USB storage
   => usb storage
   #   Device 0: Vendor: Kingston Rev: PMAP Prod: DataTraveler 2.0
   #             Type: Removable Hard Disk
   #             Capacity: 7632.0 MB = 7.4 GB (15630336 x 512)
   
   # Reset USB
   => usb reset

**NAND Flash Commands:**

.. code-block:: bash

   # Display NAND info
   => nand info
   # Device 0: nand0, sector size 128 KiB
   #   Page size       2048 b
   #   OOB size          64 b
   #   Erase size    131072 b
   #   subpagesize     2048 b
   #   options       0x40004200
   #   bbt options   0x00060000
   
   # Erase NAND
   => nand erase 0x0 0x100000        # Erase 1MB from offset 0
   => nand erase.chip                # Erase entire chip (dangerous!)
   
   # Read from NAND
   => nand read ${loadaddr} 0x200000 0x400000
   
   # Write to NAND
   => nand write ${loadaddr} 0x200000 ${filesize}
   
   # Bad block management
   => nand bad
   # Device 0 bad blocks:
   #   0x02400000
   #   0x0a800000

3.4 Network Commands
--------------------

**Network Configuration:**

.. code-block:: bash

   # Set network parameters
   => setenv ipaddr 192.168.1.100
   => setenv netmask 255.255.255.0
   => setenv gatewayip 192.168.1.1
   => setenv serverip 192.168.1.10
   => saveenv
   
   # Show network configuration
   => printenv ipaddr netmask serverip
   
   # Test connectivity
   => ping 192.168.1.10
   # host 192.168.1.10 is alive

**TFTP - Trivial File Transfer Protocol:**

.. code-block:: bash

   # Load file via TFTP
   => tftp ${loadaddr} zImage
   # Using ethernet@4a100000 device
   # TFTP from server 192.168.1.10; our IP address is 192.168.1.100
   # Filename 'zImage'.
   # Load address: 0x82000000
   # Loading: #################################################################
   #          4.5 MiB/s
   # done
   # Bytes transferred = 4521984 (450000 hex)
   
   # Load to specific address
   => tftp 0x82000000 zImage
   => tftp ${fdt_addr} am335x-boneblack.dtb
   
   # Upload via TFTP (if server supports)
   => tftp ${loadaddr} upload_file.bin w

**NFS - Network File System:**

.. code-block:: bash

   # Boot from NFS root
   => setenv bootargs 'console=ttyO0,115200n8 root=/dev/nfs \
      nfsroot=192.168.1.10:/export/rootfs,tcp,vers=3 \
      ip=192.168.1.100:192.168.1.10:192.168.1.1:255.255.255.0::eth0:off'
   
   # Load kernel and DTB via TFTP, mount NFS root
   => tftp ${loadaddr} zImage
   => tftp ${fdt_addr} am335x-boneblack.dtb
   => bootz ${loadaddr} - ${fdt_addr}

3.5 Filesystem Commands
------------------------

**FAT Filesystem:**

.. code-block:: bash

   # List files
   => fatls mmc 0:1
   #    4521984   zImage
   #      45678   am335x-boneblack.dtb
   #       1234   uEnv.txt
   
   # Load file from FAT
   => fatload mmc 0:1 ${loadaddr} zImage
   # reading zImage
   # 4521984 bytes read in 250 ms (17.2 MiB/s)
   
   # Get file size
   => fatsize mmc 0:1 zImage
   # 4521984
   
   # Write file to FAT
   => fatwrite mmc 0:1 ${loadaddr} myfile.bin ${filesize}

**ext4 Filesystem:**

.. code-block:: bash

   # List files
   => ext4ls mmc 0:2 /boot
   # <DIR>       4096 .
   # <DIR>       4096 ..
   #          4521984 vmlinuz
   #            45678 am335x-boneblack.dtb
   
   # Load file from ext4
   => ext4load mmc 0:2 ${loadaddr} /boot/vmlinuz
   # 4521984 bytes read in 250 ms (17.2 MiB/s)
   
   # Get file size
   => ext4size mmc 0:2 /boot/vmlinuz

================================================================================
4. U-Boot Environment and Boot Scripts
================================================================================

4.1 Environment Variables
--------------------------

**Critical Environment Variables:**

.. code-block:: bash

   # Boot configuration
   bootcmd          # Commands executed automatically at boot
   bootdelay        # Delay in seconds before auto-boot (default: 2)
   bootargs         # Kernel command line arguments
   
   # Load addresses (RAM locations)
   loadaddr         # Default load address for files
   kernel_addr_r    # Kernel load address
   fdt_addr_r       # Device tree load address  
   ramdisk_addr_r   # Initramfs load address
   
   # Network configuration
   ipaddr           # Board IP address
   serverip         # TFTP server IP
   netmask          # Network mask
   gatewayip        # Gateway IP
   ethaddr          # MAC address (usually set by bootloader)
   
   # Storage configuration
   mmcdev           # MMC device number (0=SD, 1=eMMC)
   mmcpart          # MMC partition number
   bootpart         # Boot partition identifier
   
   # Console configuration
   console          # Console device (ttyO0, ttyS0, etc.)
   baudrate         # Serial baud rate (115200)

**Example Environment Setup:**

.. code-block:: bash

   # Network boot configuration
   => setenv serverip 192.168.1.10
   => setenv ipaddr 192.168.1.100
   => setenv netmask 255.255.255.0
   => setenv netboot 'tftp ${loadaddr} zImage; tftp ${fdt_addr} dtb; bootz ${loadaddr} - ${fdt_addr}'
   => setenv bootcmd 'run netboot'
   => saveenv
   
   # MMC boot configuration  
   => setenv mmcboot 'mmc dev 0; fatload mmc 0:1 ${loadaddr} zImage; fatload mmc 0:1 ${fdt_addr} am335x-boneblack.dtb; bootz ${loadaddr} - ${fdt_addr}'
   => setenv bootargs 'console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw rootwait'
   => setenv bootcmd 'run mmcboot'
   => saveenv

**Environment Storage Locations:**

.. code-block:: text

   Possible storage:
   - MMC/SD card (common)
   - NAND flash
   - NOR flash
   - SPI flash
   - EEPROM
   - Redundant environments (two copies for safety)
   
   Location configured at build time:
   - CONFIG_ENV_IS_IN_MMC
   - CONFIG_ENV_IS_IN_NAND
   - CONFIG_ENV_OFFSET (offset in storage)
   - CONFIG_ENV_SIZE (size in bytes)

4.2 Boot Scripts (boot.scr)
----------------------------

**Creating Boot Script:**

.. code-block:: bash

   # Create boot script source (boot.cmd)
   cat > boot.cmd << 'EOF'
   echo "Loading kernel..."
   fatload mmc 0:1 ${kernel_addr_r} zImage
   
   echo "Loading device tree..."
   fatload mmc 0:1 ${fdt_addr_r} am335x-boneblack.dtb
   
   echo "Setting bootargs..."
   setenv bootargs console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw rootwait
   
   echo "Booting kernel..."
   bootz ${kernel_addr_r} - ${fdt_addr_r}
   EOF
   
   # Compile boot script with mkimage
   mkimage -A arm -O linux -T script -C none \
           -n "Boot Script" \
           -d boot.cmd boot.scr
   
   # Copy to boot partition
   cp boot.scr /media/boot/

**Using Boot Script in U-Boot:**

.. code-block:: bash

   # Load and execute boot script
   => fatload mmc 0:1 ${loadaddr} boot.scr
   => source ${loadaddr}
   
   # Or set as bootcmd
   => setenv bootcmd 'fatload mmc 0:1 ${loadaddr} boot.scr; source ${loadaddr}'
   => saveenv

**Complex Boot Script Example:**

.. code-block:: bash

   # boot.cmd with fallback logic
   cat > boot.cmd << 'EOF'
   # Try to boot from MMC first
   echo "Attempting MMC boot..."
   if mmc dev 0; then
       if fatload mmc 0:1 ${kernel_addr_r} zImage; then
           if fatload mmc 0:1 ${fdt_addr_r} am335x-boneblack.dtb; then
               setenv bootargs console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw
               echo "Booting from MMC..."
               bootz ${kernel_addr_r} - ${fdt_addr_r}
           fi
       fi
   fi
   
   # Fallback to network boot
   echo "MMC boot failed, trying network..."
   if ping ${serverip}; then
       tftp ${kernel_addr_r} zImage
       tftp ${fdt_addr_r} am335x-boneblack.dtb
       setenv bootargs console=ttyO0,115200n8 root=/dev/nfs nfsroot=${serverip}:/export/rootfs ip=dhcp
       bootz ${kernel_addr_r} - ${fdt_addr_r}
   fi
   
   echo "All boot methods failed!"
   EOF

4.3 uEnv.txt Configuration
---------------------------

**What is uEnv.txt?**

A simple text file that sets environment variables, used by some boards
as an alternative to boot scripts.

**Example uEnv.txt:**

.. code-block:: bash

   # uEnv.txt for BeagleBone Black
   console=ttyO0,115200n8
   ipaddr=192.168.1.100
   serverip=192.168.1.10
   
   bootpart=0:1
   bootdir=/boot
   bootfile=zImage
   fdtfile=am335x-boneblack.dtb
   
   loadkernel=fatload mmc ${bootpart} ${loadaddr} ${bootdir}/${bootfile}
   loadfdt=fatload mmc ${bootpart} ${fdtaddr} ${bootdir}/${fdtfile}
   
   mmcargs=setenv bootargs console=${console} root=/dev/mmcblk0p2 rw rootwait
   
   uenvcmd=run loadkernel; run loadfdt; run mmcargs; bootz ${loadaddr} - ${fdtaddr}

**Loading uEnv.txt in U-Boot:**

.. code-block:: bash

   # U-Boot automatically loads uEnv.txt if configured
   => fatload mmc 0:1 ${loadaddr} uEnv.txt
   => env import -t ${loadaddr} ${filesize}
   => run uenvcmd

================================================================================
5. Device Tree in U-Boot
================================================================================

5.1 Device Tree Basics
-----------------------

**What is Device Tree?**

Device Tree is a data structure describing hardware components, used by
bootloader and kernel to configure drivers without hardcoding board details.

**Device Tree Files:**

.. code-block:: text

   .dts (Device Tree Source)
      ↓ (dtc compiler)
   .dtb (Device Tree Blob - binary)
   
   Location in U-Boot source:
   arch/arm/dts/*.dts
   arch/arm/dts/*.dtsi (include files)

**Device Tree Structure Example:**

.. code-block:: dts

   /dts-v1/;
   
   / {
       model = "TI AM335x BeagleBone Black";
       compatible = "ti,am335x-bone-black", "ti,am33xx";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x20000000>; /* 512 MB */
       };
       
       chosen {
           stdout-path = &uart0;
           bootargs = "console=ttyO0,115200n8";
       };
   };
   
   &uart0 {
       status = "okay";
   };
   
   &mmc1 {
       status = "okay";
       vmmc-supply = <&vmmcsd_fixed>;
       bus-width = <4>;
   };

5.2 Device Tree Commands in U-Boot
-----------------------------------

**FDT Commands:**

.. code-block:: bash

   # Load device tree
   => fatload mmc 0:1 ${fdt_addr} am335x-boneblack.dtb
   
   # Set FDT address for kernel
   => fdt addr ${fdt_addr}
   # Working FDT set to 81f00000
   
   # Print device tree
   => fdt print /
   => fdt print /chosen
   # chosen {
   #     stdout-path = "/ocp/serial@44e09000";
   #     bootargs = "console=ttyO0,115200n8 root=/dev/mmcblk0p2";
   # };
   
   # List nodes
   => fdt list /
   # chosen
   # memory@80000000
   # ocp
   
   # Get property value
   => fdt get value bootargs /chosen bootargs
   => printenv bootargs

**Modifying Device Tree:**

.. code-block:: bash

   # Set property
   => fdt set /chosen bootargs "console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw"
   
   # Add new property
   => fdt set /chosen linux,initrd-start <0x82000000>
   => fdt set /chosen linux,initrd-end <0x82800000>
   
   # Create new node
   => fdt mknode / newnode
   => fdt set /newnode compatible "vendor,device"
   
   # Resize FDT (if modifications need more space)
   => fdt resize 8192

**Boot with Device Tree:**

.. code-block:: bash

   # Standard boot sequence with DTB
   => fatload mmc 0:1 ${loadaddr} zImage
   => fatload mmc 0:1 ${fdt_addr} am335x-boneblack.dtb
   => fdt addr ${fdt_addr}
   => fdt set /chosen bootargs "console=ttyO0,115200n8 root=/dev/mmcblk0p2"
   => bootz ${loadaddr} - ${fdt_addr}

5.3 FIT Images (Flattened Image Tree)
--------------------------------------

**What is FIT?**

FIT (Flattened Image Tree) is a new U-Boot image format that combines
kernel, device tree, and initramfs into a single file with verification.

**FIT Image Source (.its):**

.. code-block:: dts

   /dts-v1/;
   
   / {
       description = "BeagleBone Black FIT Image";
       #address-cells = <1>;
       
       images {
           kernel {
               description = "Linux kernel";
               data = /incbin/("zImage");
               type = "kernel";
               arch = "arm";
               os = "linux";
               compression = "none";
               load = <0x80008000>;
               entry = <0x80008000>;
               hash-1 {
                   algo = "sha256";
               };
           };
           
           fdt {
               description = "Device tree";
               data = /incbin/("am335x-boneblack.dtb");
               type = "flat_dt";
               arch = "arm";
               compression = "none";
               hash-1 {
                   algo = "sha256";
               };
           };
           
           ramdisk {
               description = "Ramdisk";
               data = /incbin/("rootfs.cpio.gz");
               type = "ramdisk";
               arch = "arm";
               os = "linux";
               compression = "gzip";
               hash-1 {
                   algo = "sha256";
               };
           };
       };
       
       configurations {
           default = "conf-1";
           
           conf-1 {
               description = "Boot configuration";
               kernel = "kernel";
               fdt = "fdt";
               ramdisk = "ramdisk";
           };
       };
   };

**Creating FIT Image:**

.. code-block:: bash

   # Create FIT image with mkimage
   mkimage -f image.its image.fit
   
   # Verify FIT image
   mkimage -l image.fit

**Booting FIT Image:**

.. code-block:: bash

   # Load FIT image
   => fatload mmc 0:1 ${loadaddr} image.fit
   
   # Boot from FIT (bootm with FIT support)
   => bootm ${loadaddr}
   # ## Loading kernel from FIT Image at 82000000 ...
   # ## Loading fdt from FIT Image at 82000000 ...
   # ## Loading ramdisk from FIT Image at 82000000 ...

================================================================================
6. Common Boot Scenarios
================================================================================

6.1 Boot from SD/MMC Card
--------------------------

**Complete Boot Sequence:**

.. code-block:: bash

   # U-Boot environment setup
   => setenv mmcdev 0
   => setenv mmcpart 1
   => setenv bootpart 0:1
   
   => setenv loadkernel 'fatload mmc ${bootpart} ${loadaddr} zImage'
   => setenv loadfdt 'fatload mmc ${bootpart} ${fdt_addr} am335x-boneblack.dtb'
   
   => setenv mmcargs 'setenv bootargs console=ttyO0,115200n8 root=/dev/mmcblk0p2 rw rootwait'
   
   => setenv mmcboot 'echo Booting from MMC...; run loadkernel; run loadfdt; run mmcargs; bootz ${loadaddr} - ${fdt_addr}'
   
   => setenv bootcmd 'run mmcboot'
   => saveenv
   
   # Boot
   => boot

**With Initramfs:**

.. code-block:: bash

   => setenv loadramdisk 'fatload mmc ${bootpart} ${ramdisk_addr_r} initramfs.cpio.gz'
   
   => setenv mmcboot 'run loadkernel; run loadfdt; run loadramdisk; run mmcargs; bootz ${loadaddr} ${ramdisk_addr_r}:${filesize} ${fdt_addr}'

6.2 Network Boot (TFTP + NFS)
------------------------------

**TFTP Server Setup (Host):**

.. code-block:: bash

   # Install TFTP server
   sudo apt-get install tftpd-hpa
   
   # Configure /etc/default/tftpd-hpa
   TFTP_USERNAME="tftp"
   TFTP_DIRECTORY="/srv/tftp"
   TFTP_ADDRESS=":69"
   TFTP_OPTIONS="--secure"
   
   # Copy files to TFTP directory
   sudo cp zImage /srv/tftp/
   sudo cp am335x-boneblack.dtb /srv/tftp/
   sudo systemctl restart tftpd-hpa

**NFS Server Setup (Host):**

.. code-block:: bash

   # Install NFS server
   sudo apt-get install nfs-kernel-server
   
   # Configure /etc/exports
   /export/rootfs 192.168.1.0/24(rw,sync,no_root_squash,no_subtree_check)
   
   # Export filesystem
   sudo exportfs -av
   sudo systemctl restart nfs-kernel-server

**U-Boot Network Boot:**

.. code-block:: bash

   => setenv ipaddr 192.168.1.100
   => setenv serverip 192.168.1.10
   => setenv netmask 255.255.255.0
   
   => setenv netboot 'echo Booting from network...; tftp ${loadaddr} zImage; tftp ${fdt_addr} am335x-boneblack.dtb; setenv bootargs console=ttyO0,115200n8 root=/dev/nfs nfsroot=${serverip}:/export/rootfs,tcp,vers=3 ip=${ipaddr}:${serverip}:${gatewayip}:${netmask}::eth0:off; bootz ${loadaddr} - ${fdt_addr}'
   
   => setenv bootcmd 'run netboot'
   => saveenv
   => boot

6.3 Boot from USB
-----------------

**USB Boot Sequence:**

.. code-block:: bash

   => usb start
   => usb storage
   
   => setenv usbboot 'usb start; fatload usb 0:1 ${loadaddr} zImage; fatload usb 0:1 ${fdt_addr} am335x-boneblack.dtb; setenv bootargs console=ttyO0,115200n8 root=/dev/sda2 rw rootwait; bootz ${loadaddr} - ${fdt_addr}'
   
   => setenv bootcmd 'run usbboot'
   => boot

6.4 Boot from NAND Flash
-------------------------

**NAND Boot Configuration:**

.. code-block:: bash

   # Partition layout
   => mtdparts default
   => mtdparts
   # device nand0 <omap2-nand.0>, # parts = 4
   #  #: name                size            offset
   #  0: SPL                 0x00020000      0x00000000
   #  1: U-Boot              0x00100000      0x00020000
   #  2: environment         0x00020000      0x00120000
   #  3: kernel              0x00400000      0x00140000
   #  4: rootfs              0x0fa80000      0x00540000
   
   => setenv nandboot 'echo Booting from NAND...; nand read ${loadaddr} kernel 0x400000; nand read ${fdt_addr} 0x500000 0x20000; setenv bootargs console=ttyO0,115200n8 ubi.mtd=4 root=ubi0:rootfs rootfstype=ubifs; bootz ${loadaddr} - ${fdt_addr}'
   
   => setenv bootcmd 'run nandboot'
   => saveenv

================================================================================
7. Troubleshooting U-Boot
================================================================================

7.1 Common Boot Issues
----------------------

**Issue 1: No U-Boot Output**

.. code-block:: text

   Symptoms: No serial output after power-on
   
   Causes:
   - Wrong serial port or baud rate
   - Incorrect boot pins configuration
   - Corrupted U-Boot image
   - Hardware failure
   
   Solutions:
   1. Verify serial connection (115200 8N1)
   2. Try different serial ports (ttyUSB0, ttyUSB1)
   3. Check boot mode pins
   4. Re-flash U-Boot from recovery mode
   5. Use JTAG debugger

**Issue 2: U-Boot Loads but Kernel Doesn't Boot**

.. code-block:: bash

   # Check kernel load address
   => printenv loadaddr
   => printenv bootargs
   
   # Verify files are loading
   => fatload mmc 0:1 ${loadaddr} zImage
   => printenv filesize
   # filesize=450000  (4.5MB - looks reasonable)
   
   # Check device tree
   => fdt addr ${fdt_addr}
   => fdt print /chosen
   
   # Try booting with debug output
   => setenv bootargs 'console=ttyO0,115200n8 earlyprintk debug'

**Issue 3: Wrong Device Tree**

.. code-block:: bash

   # Symptoms: Kernel boots but drivers fail
   # Solution: Ensure correct DTB for board
   
   => printenv fdtfile
   # Should match your board exactly
   # am335x-boneblack.dtb (BeagleBone Black)
   # am335x-boneblack-wireless.dtb (BBB Wireless)

**Issue 4: Environment Not Saving**

.. code-block:: bash

   => saveenv
   # Saving Environment to MMC... Writing to MMC(0)... failed
   
   # Check MMC status
   => mmc dev 0
   => mmc info
   
   # Try writing to specific location
   => mmc write ${loadaddr} 0x1000 0x10

7.2 Recovery Procedures
------------------------

**Serial Download Mode (UART Boot):**

.. code-block:: bash

   # For AM335x/OMAP processors
   # 1. Hold UART boot button during power-on
   # 2. Use xmodem protocol to send U-Boot SPL
   
   # On host (Linux)
   sudo sx -vv MLO < /dev/ttyUSB0 > /dev/ttyUSB0
   sudo sx -vv u-boot.img < /dev/ttyUSB0 > /dev/ttyUSB0

**USB DFU (Device Firmware Upgrade):**

.. code-block:: bash

   # Enter DFU mode in U-Boot
   => dfu 0 mmc 0
   
   # On host
   sudo dfu-util -l  # List DFU devices
   sudo dfu-util -a 0 -D MLO
   sudo dfu-util -a 1 -D u-boot.img

**JTAG Recovery:**

.. code-block:: bash

   # Using OpenOCD
   openocd -f board/ti_am335x.cfg
   
   # In separate terminal (telnet to OpenOCD)
   telnet localhost 4444
   > halt
   > flash write_image erase u-boot.img 0x80000000
   > reset run

7.3 Debugging with U-Boot
--------------------------

**Memory Testing:**

.. code-block:: bash

   # Test RAM
   => mtest 0x80000000 0x81000000
   # Pattern FFFFFFFF  Writing...  Reading...
   # Tested 256 iteration(s) with 0 errors.
   
   # Quick memory test
   => mw 0x80000000 0xdeadbeef 0x1000
   => md 0x80000000 10
   # Verify pattern written correctly

**Boot Timing:**

.. code-block:: bash

   # Measure boot time
   => setenv bootcmd 'echo Start; run mmcboot'
   => boot
   # Time from "Start" to kernel output

**Verbose Boot:**

.. code-block:: bash

   # Enable maximum debug output
   => setenv bootargs 'console=ttyO0,115200n8 earlyprintk loglevel=8 debug'
   => setenv verify yes  # Verify images before boot

================================================================================
8. Advanced U-Boot Topics
================================================================================

8.1 Secure Boot
----------------

**Verified Boot with FIT:**

.. code-block:: bash

   # FIT image with signature verification
   # Requires public key embedded in U-Boot
   
   # Generate RSA keys
   openssl genrsa -F4 -out keys/dev.key 2048
   openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt
   
   # Sign FIT image
   mkimage -f image.its -k keys -K u-boot.dtb -r image.fit
   
   # U-Boot will verify signature before booting
   => fatload mmc 0:1 ${loadaddr} image.fit
   => bootm ${loadaddr}
   # ## Checking hash(es) for FIT Image at 82000000 ...
   #    Hash(es) for Image 0 (kernel): sha256+ OK
   #    Sign value: OK

**Secure Boot Chain:**

.. code-block:: text

   ROM → SPL (signed) → U-Boot (signed) → Kernel (signed)
   
   Each stage verifies next stage before execution
   Requires eFuse programming for production

8.2 Falcon Mode (Fast Boot)
----------------------------

**What is Falcon Mode?**

SPL directly loads Linux kernel, bypassing full U-Boot for faster boot.

**Setup Falcon Mode:**

.. code-block:: bash

   # In full U-Boot, prepare Falcon boot
   => fatload mmc 0:1 ${loadaddr} zImage
   => fatload mmc 0:1 ${fdt_addr} am335x-boneblack.dtb
   => setenv bootargs 'console=ttyO0,115200n8 root=/dev/mmcblk0p2'
   
   # Create args image for SPL
   => spl export fdt ${loadaddr} - ${fdt_addr}
   # Argument image is now in memory at: 0x80000100
   
   # Save to specific location SPL will read
   => fatwrite mmc 0:1 0x80000100 args 0x1000
   
   # Rebuild U-Boot with Falcon mode enabled
   # CONFIG_SPL_OS_BOOT=y
   # CONFIG_SPL_FALCON_BOOT_MMCSD=y

8.3 Runtime Device Tree Overlays
---------------------------------

**Device Tree Overlays:**

.. code-block:: dts

   // Example overlay: enable I2C
   /dts-v1/;
   /plugin/;
   
   / {
       compatible = "ti,am335x-bone-black";
       
       fragment@0 {
           target = <&i2c2>;
           __overlay__ {
               status = "okay";
               clock-frequency = <100000>;
           };
       };
   };

**Apply Overlay in U-Boot:**

.. code-block:: bash

   # Load base DTB
   => fatload mmc 0:1 ${fdt_addr} am335x-boneblack.dtb
   => fdt addr ${fdt_addr}
   => fdt resize 8192
   
   # Load and apply overlay
   => fatload mmc 0:1 ${loadaddr} overlay-i2c.dtbo
   => fdt apply ${loadaddr}
   
   # Boot with modified tree
   => bootz ${kernel_addr} - ${fdt_addr}

================================================================================
9. Exam-Style Questions
================================================================================

**Q1:** What are the typical stages in an embedded Linux boot sequence?

**A:** ROM Bootloader → SPL → U-Boot → Linux Kernel → Init

**Q2:** What is the difference between bootz, bootm, and booti commands?

**A:** 
- bootz: Boot zImage (ARM/ARM64 compressed kernel)
- bootm: Boot uImage (legacy U-Boot image format)
- booti: Boot Image (ARM64 uncompressed kernel)

**Q3:** How do you load a kernel from SD card partition 1 in U-Boot?

**A:**
.. code-block:: bash

   => mmc dev 0
   => fatload mmc 0:1 ${loadaddr} zImage
   => fatload mmc 0:1 ${fdt_addr} dtb
   => bootz ${loadaddr} - ${fdt_addr}

**Q4:** What is the purpose of the bootargs environment variable?

**A:** Contains kernel command line arguments passed from bootloader to kernel,
specifying console, root filesystem, and other boot parameters.

**Q5:** How do you set U-Boot to wait 5 seconds before auto-booting?

**A:** `=> setenv bootdelay 5; saveenv`

**Q6:** What is a device tree blob (DTB) and why is it needed?

**A:** Binary representation of hardware description, allows kernel to configure
drivers for specific board without recompiling kernel.

**Q7:** How do you modify device tree bootargs in U-Boot?

**A:**
.. code-block:: bash

   => fdt addr ${fdt_addr}
   => fdt set /chosen bootargs "console=ttyO0,115200 root=/dev/mmcblk0p2"

**Q8:** What is SPL and why is it needed?

**A:** Secondary Program Loader - small bootloader that fits in SoC internal SRAM,
initializes DDR RAM, loads full U-Boot. Needed because ROM bootloader cannot
directly load large U-Boot.

**Q9:** How do you recover a board with corrupted U-Boot?

**A:** Use serial download (UART boot), USB DFU mode, or JTAG to reflash bootloader.

**Q10:** What is Falcon mode in U-Boot?

**A:** Fast boot mode where SPL directly loads Linux kernel, bypassing full U-Boot
to reduce boot time.

================================================================================
10. Key Takeaways
================================================================================

.. code-block:: text

   Boot Sequence Essentials:
   =========================
   ROM → SPL → U-Boot → Kernel → Init
   - ROM: Built into SoC, loads SPL
   - SPL: 30-100KB, initializes DDR, loads U-Boot  
   - U-Boot: Full bootloader with commands
   - Kernel: Linux kernel with DTB
   
   Critical Commands:
   ==================
   # Environment
   printenv, setenv, saveenv
   
   # Storage
   mmc dev, mmc list, fatload, ext4load
   
   # Network
   setenv ipaddr/serverip, tftp, ping
   
   # Boot
   bootz ${kernel} - ${fdt}
   bootm ${uImage}
   
   # Device Tree
   fdt addr, fdt print, fdt set
   
   Boot Methods:
   =============
   1. SD/MMC: Most common for development
   2. eMMC: Production devices
   3. NAND/NOR: Legacy embedded systems
   4. Network (TFTP+NFS): Development/testing
   5. USB: Recovery/alternate boot
   
   Environment Variables:
   ======================
   bootcmd      - Auto-boot command
   bootargs     - Kernel cmdline
   bootdelay    - Delay before boot
   loadaddr     - Load address
   ipaddr       - Board IP
   serverip     - TFTP server
   
   Common Issues:
   ==============
   ✗ No serial output → Check baud rate (115200)
   ✗ Kernel won't boot → Verify loadaddr, bootargs
   ✗ Wrong DTB → Match exact board model
   ✗ Can't save env → Check MMC write permissions
   
   Best Practices:
   ===============
   ✓ Always save working environment
   ✓ Use boot scripts for complex sequences
   ✓ Keep backup bootloader on alternate boot medium
   ✓ Document custom environment setup
   ✓ Test network boot for development
   ✓ Use FIT images for production (verification)

================================================================================
END OF CHEATSHEET
================================================================================

