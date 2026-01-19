================================================================================
Embedded Linux: Storage & Filesystems - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 3 Ch7)
:Target: Flash Memory, MTD, Filesystems
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Flash Memory Types:**

.. code-block:: text

   NOR Flash:
   - Random access (XIP capable)
   - Slow write, fast read
   - Expensive, reliable
   - Use: Bootloaders, small storage
   
   NAND Flash:
   - Block access, no XIP
   - Fast write, slower read
   - Cheaper, needs error correction
   - Use: Large storage (>16MB)
   
   eMMC/SD:
   - Managed NAND with controller
   - Wear leveling built-in
   - Standard block device
   - Use: Easy integration, large storage

**MTD Commands:**

.. code-block:: bash

   # Flash information
   cat /proc/mtd
   mtdinfo /dev/mtd0
   mtdinfo -a
   
   # Erase flash
   flash_erase /dev/mtd2 0 0
   
   # Read/Write
   nanddump /dev/mtd2 -f backup.img
   nandwrite -p /dev/mtd2 rootfs.ubi
   
   # UBI operations
   ubiformat /dev/mtd2
   ubiattach -p /dev/mtd2
   ubimkvol /dev/ubi0 -N rootfs -s 200MiB
   mount -t ubifs ubi0:rootfs /mnt

**Filesystem Selection:**

.. code-block:: text

   ext4:
   ✓ General purpose
   ✓ Journaling, robust
   ✗ Not flash-optimized
   Use: eMMC, SD cards
   
   SquashFS:
   ✓ Read-only, compressed
   ✓ Very small footprint
   ✗ No updates
   Use: Root filesystem, immutable data
   
   UBIFS:
   ✓ Flash-optimized
   ✓ Wear leveling, compression
   ✓ Power-fail safe
   Use: Raw NAND flash
   
   JFFS2:
   ✓ Flash-optimized
   ✗ Slow mount, deprecated
   Use: Legacy, small (<128MB)
   
   F2FS:
   ✓ Flash-friendly
   ✓ Optimized for eMMC/SD
   Use: Modern eMMC/SD systems

================================================================================
1. Flash Memory Overview
================================================================================

1.1 NOR Flash
-------------

**Characteristics:**

.. code-block:: text

   Architecture:
   - Random access (byte/word addressable)
   - Execute-in-place (XIP) capable
   - Direct memory mapping
   - Reliable, long life
   
   Performance:
   - Read: Fast (100-150 MB/s)
   - Write: Slow (10-40 KB/s)
   - Erase: Very slow (seconds)
   
   Organization:
   - Block size: 64-128 KB (large)
   - No bad blocks (manufacturing)
   - Uniform erase blocks
   
   Cost:
   - Expensive ($/GB)
   - Typically 1-128 MB
   
   Applications:
   - Bootloaders (U-Boot)
   - Kernel storage
   - Small embedded systems
   - Code storage (XIP)

**Linux NOR Flash Support:**

.. code-block:: bash

   # Kernel config
   CONFIG_MTD=y
   CONFIG_MTD_CFI=y
   CONFIG_MTD_JEDEC_PROBE=y
   CONFIG_MTD_CFI_AMDSTD=y
   CONFIG_MTD_CFI_INTELEXT=y
   
   # Device tree (SPI NOR)
   &spi0 {
       flash@0 {
           compatible = "jedec,spi-nor";
           reg = <0>;
           spi-max-frequency = <25000000>;
           
           partitions {
               compatible = "fixed-partitions";
               #address-cells = <1>;
               #size-cells = <1>;
               
               partition@0 {
                   label = "bootloader";
                   reg = <0x0 0x40000>;
                   read-only;
               };
               
               partition@40000 {
                   label = "kernel";
                   reg = <0x40000 0x400000>;
               };
               
               partition@440000 {
                   label = "rootfs";
                   reg = <0x440000 0xbc0000>;
               };
           };
       };
   };

1.2 NAND Flash
--------------

**Characteristics:**

.. code-block:: text

   Architecture:
   - Block access (page-based)
   - No XIP (cannot execute directly)
   - Requires error correction (ECC)
   - Bad blocks expected
   
   Performance:
   - Read: 10-40 MB/s
   - Write: Fast (5-20 MB/s)
   - Erase: Fast (milliseconds)
   
   Organization:
   - Page size: 2-4 KB
   - Block size: 128-256 KB (small)
   - Out-of-band (OOB) area for metadata
   - Bad block management required
   
   Cost:
   - Cheap ($/GB)
   - Typically 128 MB - 128 GB
   
   Applications:
   - Root filesystem
   - Data storage
   - High-capacity embedded systems

**Linux NAND Flash Support:**

.. code-block:: bash

   # Kernel config
   CONFIG_MTD=y
   CONFIG_MTD_NAND=y
   CONFIG_MTD_NAND_ECC=y
   CONFIG_MTD_UBI=y
   CONFIG_UBIFS_FS=y
   
   # Check NAND info
   cat /proc/mtd
   mtdinfo /dev/mtd0
   nand_info=$(cat /sys/class/mtd/mtd0/*)

**Device Tree (NAND):**

.. code-block:: dts

   &gpmi {
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_gpmi_nand>;
       status = "okay";
       
       nand@0 {
           compatible = "fsl,imx6q-gpmi-nand";
           #address-cells = <1>;
           #size-cells = <1>;
           
           partition@0 {
               label = "bootloader";
               reg = <0x0 0x400000>;
           };
           
           partition@400000 {
               label = "kernel";
               reg = <0x400000 0x800000>;
           };
           
           partition@c00000 {
               label = "rootfs";
               reg = <0xc00000 0x1f400000>;
           };
       };
   };

1.3 eMMC and SD Cards
---------------------

**Characteristics:**

.. code-block:: text

   eMMC (Embedded MultiMediaCard):
   - Managed NAND flash
   - Built-in controller (wear leveling, bad block management, ECC)
   - Standard block device interface
   - High performance (200+ MB/s)
   - Soldered to board
   - Sizes: 4 GB - 256 GB
   
   SD/microSD:
   - Removable eMMC
   - Same managed NAND architecture
   - Removable, hot-pluggable
   - Performance varies (Class 10, UHS-I/II)
   - Sizes: 1 GB - 1 TB
   
   Advantages:
   ✓ Simple block device interface
   ✓ No MTD/UBI complexity
   ✓ Wear leveling handled by controller
   ✓ Easy to use (standard filesystem)
   
   Disadvantages:
   ✗ Controller adds cost
   ✗ No direct flash access
   ✗ Reliability depends on controller quality

**Linux eMMC/SD Support:**

.. code-block:: bash

   # Kernel config
   CONFIG_MMC=y
   CONFIG_MMC_BLOCK=y
   CONFIG_MMC_SDHCI=y
   CONFIG_MMC_SDHCI_PLTFM=y
   
   # Check devices
   ls /dev/mmcblk*
   cat /sys/block/mmcblk0/device/*
   
   # Partition
   fdisk /dev/mmcblk0
   mkfs.ext4 /dev/mmcblk0p1
   
   # Mount
   mount /dev/mmcblk0p1 /mnt

================================================================================
2. MTD Subsystem
================================================================================

2.1 MTD Architecture
--------------------

**MTD Layers:**

.. code-block:: text

   Applications
        |
        v
   MTD Character Device (/dev/mtdX)
   MTD Block Device (/dev/mtdblockX)
        |
        v
   MTD Core (drivers/mtd/mtdcore.c)
        |
        v
   MTD Device Drivers
   - NAND (mtdnand.c)
   - NOR (cfi_cmdset_*.c)
   - SPI (m25p80.c)
        |
        v
   Hardware

**MTD Partitions:**

.. code-block:: bash

   # View partitions
   cat /proc/mtd
   dev:    size   erasesize  name
   mtd0: 00400000 00020000 "bootloader"
   mtd1: 00800000 00020000 "kernel"
   mtd2: 1f400000 00020000 "rootfs"
   
   # Get detailed info
   mtdinfo /dev/mtd0
   mtdinfo -a   # All MTD devices

**Kernel Command Line Partitioning:**

.. code-block:: bash

   # U-Boot bootargs
   setenv bootargs mtdparts=gpmi-nand:4m(boot),8m(kernel),-(rootfs)
   
   # Alternative: OF_MTD_PARTS in device tree
   partitions {
       compatible = "fixed-partitions";
       ...
   };

2.2 MTD Utilities
-----------------

**Flash Operations:**

.. code-block:: bash

   # Erase entire MTD partition
   flash_erase /dev/mtd2 0 0
   
   # Erase specific blocks (offset, count)
   flash_erase /dev/mtd2 0x100000 64
   
   # Mark bad block
   flash_erase -j /dev/mtd2 0x200000 1
   
   # Read NAND
   nanddump /dev/mtd2 -f backup.img
   nanddump -o -f oob.img /dev/mtd2   # Include OOB
   
   # Write NAND
   nandwrite -p /dev/mtd2 image.bin
   nandwrite -p -m /dev/mtd2 image.bin  # Mark bad blocks
   
   # Test NAND
   nandtest /dev/mtd2
   flash_speed /dev/mtd2
   
   # Lock/Unlock
   flash_lock /dev/mtd0 0 -1
   flash_unlock /dev/mtd0 0 -1

**MTD Debug:**

.. code-block:: bash

   # Enable MTD debug messages
   echo 8 > /proc/sys/kernel/printk
   
   # Kernel config
   CONFIG_MTD_DEBUG=y
   CONFIG_MTD_DEBUG_VERBOSE=3
   
   # View flash statistics
   cat /sys/class/mtd/mtd0/bad_blocks
   cat /sys/class/mtd/mtd0/ecc_failures

================================================================================
3. UBI (Unsorted Block Images)
================================================================================

3.1 UBI Overview
----------------

**UBI Features:**

.. code-block:: text

   Purpose:
   - Wear leveling across all blocks
   - Bad block management
   - Atomic LEB changes
   - Volume management
   - Works with UBIFS
   
   Architecture:
   MTD Device (raw NAND)
        |
        v
   UBI Layer
   - Physical Erase Blocks (PEB)
   - Logical Erase Blocks (LEB)
   - Volume management
        |
        v
   UBI Volumes (/dev/ubi0_0, /dev/ubi0_1, ...)
        |
        v
   UBIFS Filesystem

**UBI Terminology:**

.. code-block:: text

   PEB: Physical Erase Block
   - Actual flash erase block
   
   LEB: Logical Erase Block
   - Virtual erase block exposed to upper layer
   - Mapped to PEB (may change due to wear leveling)
   
   UBI Volume:
   - Logical partition within UBI device
   - Can be dynamic or static
   
   VID Header:
   - Volume ID header
   - Stored in flash, describes LEB
   
   EC Header:
   - Erase Counter header
   - Tracks erase count per PEB

3.2 UBI Operations
------------------

**UBI Setup:**

.. code-block:: bash

   # Format MTD device for UBI
   ubiformat /dev/mtd2
   ubiformat /dev/mtd2 -f image.ubi   # Flash UBI image
   
   # Attach MTD device to UBI
   ubiattach -p /dev/mtd2
   ubiattach -m 2   # By MTD number
   
   # Detach
   ubidetach -p /dev/mtd2
   ubidetach -d 0   # By UBI device number
   
   # Create volume
   ubimkvol /dev/ubi0 -N rootfs -s 200MiB
   ubimkvol /dev/ubi0 -N data -m   # Max available size
   
   # Remove volume
   ubirmvol /dev/ubi0 -N rootfs
   
   # Resize volume
   ubiupdatevol /dev/ubi0_0 -s 300MiB
   
   # Get info
   ubinfo -a
   ubinfo -d 0
   ubinfo -d 0 -n 0

**UBI Volume Types:**

.. code-block:: bash

   # Dynamic volume (read/write, UBIFS)
   ubimkvol /dev/ubi0 -N rootfs -s 200MiB -t dynamic
   
   # Static volume (read-only, integrity check)
   ubimkvol /dev/ubi0 -N kernel -s 8MiB -t static
   
   # Update static volume
   ubiupdatevol /dev/ubi0_1 zImage

**Automatic UBI Attach (Kernel):**

.. code-block:: bash

   # Kernel config
   CONFIG_MTD_UBI=y
   CONFIG_MTD_UBI_BLOCK=y
   CONFIG_MTD_UBI_FASTMAP=y
   
   # Kernel command line
   ubi.mtd=2 ubi.mtd=rootfs root=ubi0:rootfs rootfstype=ubifs
   
   # Alternative: ubiblock for read-only
   ubi.mtd=2 ubi.block=0,0 root=/dev/ubiblock0_0 ro

================================================================================
4. UBIFS Filesystem
================================================================================

4.1 UBIFS Features
------------------

**Characteristics:**

.. code-block:: text

   Features:
   ✓ Flash-optimized (designed for raw NAND)
   ✓ Wear leveling aware
   ✓ Compression (lzo, zlib)
   ✓ Power-fail resilient
   ✓ Fast mount
   ✓ Journaling (recovery)
   ✓ No fsck needed
   
   Performance:
   - Fast read/write
   - Minimal flash wear
   - Efficient for frequent updates
   
   Limitations:
   - Requires UBI layer
   - More complex than ext4
   - Works only on MTD devices

**UBIFS Usage:**

.. code-block:: bash

   # Mount UBIFS
   mount -t ubifs ubi0:rootfs /mnt
   mount -t ubifs ubi0_0 /mnt   # By device node
   
   # Mount options
   mount -t ubifs -o sync ubi0:rootfs /mnt   # Synchronous
   mount -t ubifs -o compr=zlib ubi0:rootfs /mnt
   
   # Check space
   df -h /mnt
   
   # UBIFS info
   cat /sys/class/ubi/ubi0_0/*

4.2 Creating UBIFS Images
--------------------------

**mkfs.ubifs:**

.. code-block:: bash

   # Get MTD info
   PAGE_SIZE=2048
   BLOCK_SIZE=131072
   LEB_SIZE=$((BLOCK_SIZE - 2*PAGE_SIZE))   # 126976
   
   # Create UBIFS image
   mkfs.ubifs -r rootfs/ -m $PAGE_SIZE -e $LEB_SIZE -c 2048 \
              -o rootfs.ubifs
   
   # With compression
   mkfs.ubifs -r rootfs/ -m 2048 -e 126976 -c 2048 \
              -x lzo -o rootfs.ubifs
   
   # Options:
   # -r: Root directory
   # -m: Min I/O size (page size)
   # -e: LEB size
   # -c: Max LEB count
   # -x: Compression (lzo, zlib, none)

**ubinize (UBI Image):**

.. code-block:: bash

   # Create ubinize config: ubinize.cfg
   cat > ubinize.cfg << EOF
   [ubifs]
   mode=ubi
   image=rootfs.ubifs
   vol_id=0
   vol_type=dynamic
   vol_name=rootfs
   vol_flags=autoresize
   EOF
   
   # Create UBI image
   ubinize -o rootfs.ubi -m 2048 -p 128KiB -s 2048 ubinize.cfg
   
   # Flash UBI image
   ubiformat /dev/mtd2 -f rootfs.ubi
   
   # Or write directly
   flash_erase /dev/mtd2 0 0
   nandwrite -p /dev/mtd2 rootfs.ubi

================================================================================
5. Filesystem Types
================================================================================

5.1 ext4
--------

**Characteristics:**

.. code-block:: text

   Features:
   ✓ Mature, robust
   ✓ Journaling (data integrity)
   ✓ Large file support (16TB files, 1EB volume)
   ✓ Good performance
   ✗ Not flash-optimized (wear)
   
   Use Cases:
   - eMMC storage
   - SD cards
   - Hard drives
   - General-purpose embedded systems

**ext4 Usage:**

.. code-block:: bash

   # Create filesystem
   mkfs.ext4 /dev/mmcblk0p1
   mkfs.ext4 -L rootfs /dev/mmcblk0p1   # With label
   
   # Reduce reserved blocks (default 5%)
   mkfs.ext4 -m 1 /dev/mmcblk0p1   # 1% reserved
   
   # Mount
   mount /dev/mmcblk0p1 /mnt
   
   # Mount options (flash-friendly)
   mount -o noatime,nodiratime /dev/mmcblk0p1 /mnt
   mount -o data=writeback /dev/mmcblk0p1 /mnt   # Less wear
   
   # fstab entry
   /dev/mmcblk0p1  /  ext4  defaults,noatime  0  1
   
   # Check/repair
   e2fsck -f /dev/mmcblk0p1
   e2fsck -p /dev/mmcblk0p1   # Automatic repair

5.2 SquashFS
------------

**Characteristics:**

.. code-block:: text

   Features:
   ✓ Read-only, compressed
   ✓ High compression (60-80%)
   ✓ Fast decompression
   ✓ Small memory footprint
   ✓ Integrity check
   
   Use Cases:
   - Root filesystem (immutable)
   - Read-only data
   - Firmware images
   - Space-constrained systems

**SquashFS Usage:**

.. code-block:: bash

   # Create SquashFS image
   mksquashfs rootfs/ rootfs.squashfs -comp lzo
   mksquashfs rootfs/ rootfs.squashfs -comp xz -b 256K
   
   # Compression algorithms
   # -comp lzo: Fast decompression
   # -comp xz: Best compression
   # -comp gzip: Balanced
   
   # Mount
   mount -t squashfs rootfs.squashfs /mnt
   mount -t squashfs -o loop rootfs.squashfs /mnt
   
   # Kernel config
   CONFIG_SQUASHFS=y
   CONFIG_SQUASHFS_XZ=y
   CONFIG_SQUASHFS_LZO=y
   
   # Common pattern: SquashFS root + tmpfs overlay
   mount -t squashfs /dev/mtdblock2 /mnt/rootfs
   mount -t tmpfs tmpfs /mnt/overlay
   mount -t overlay overlay -o lowerdir=/mnt/rootfs,upperdir=/mnt/overlay,workdir=/mnt/work /

5.3 F2FS
--------

**Flash-Friendly Filesystem:**

.. code-block:: bash

   # Kernel config
   CONFIG_F2FS_FS=y
   CONFIG_F2FS_STAT_FS=y
   
   # Create F2FS
   mkfs.f2fs /dev/mmcblk0p1
   mkfs.f2fs -l rootfs /dev/mmcblk0p1
   
   # Mount
   mount -t f2fs /dev/mmcblk0p1 /mnt
   
   # Optimized for eMMC/SD cards
   # Better wear leveling than ext4
   # Good for high-write workloads

5.4 JFFS2 (Legacy)
------------------

**Journaling Flash File System v2:**

.. code-block:: bash

   # Kernel config
   CONFIG_JFFS2_FS=y
   CONFIG_JFFS2_COMPRESSION_OPTIONS=y
   
   # Create JFFS2 image
   mkfs.jffs2 -r rootfs/ -o rootfs.jffs2 -e 128 -l -n
   
   # Flash and mount
   flash_eraseall /dev/mtd2
   nandwrite -p /dev/mtd2 rootfs.jffs2
   mount -t jffs2 /dev/mtdblock2 /mnt
   
   # Limitations:
   # - Slow mount (scans entire flash)
   # - Deprecated (use UBIFS instead)
   # - Only for small flash (<128MB)

================================================================================
6. Storage Best Practices
================================================================================

6.1 Flash Wear Management
--------------------------

**Wear Leveling Strategies:**

.. code-block:: text

   NAND Flash (MTD):
   - Use UBI layer (automatic wear leveling)
   - Use UBIFS filesystem
   - Avoid ext4 on raw NAND
   
   eMMC/SD:
   - Controller handles wear leveling
   - Use noatime mount option
   - Minimize write amplification
   - Consider F2FS for write-heavy workloads
   
   General:
   - Use read-only root where possible
   - Separate writable data to different partition
   - Use tmpfs for temporary files
   - Disable swap on flash

**Mount Options:**

.. code-block:: bash

   # Reduce writes (ext4)
   mount -o noatime,nodiratime,data=writeback /dev/mmcblk0p1 /mnt
   
   # fstab
   /dev/mmcblk0p1  /  ext4  noatime,nodiratime,errors=remount-ro  0  1
   tmpfs  /tmp  tmpfs  defaults,size=50M  0  0
   tmpfs  /var/log  tmpfs  defaults,size=10M  0  0

6.2 Data Integrity
------------------

**Power-Fail Safety:**

.. code-block:: bash

   # UBIFS: Power-fail safe by design
   mount -t ubifs ubi0:rootfs /mnt
   
   # ext4: Journaling mode
   mount -o data=journal /dev/mmcblk0p1 /mnt   # Slowest, safest
   mount -o data=ordered /dev/mmcblk0p1 /mnt   # Default, balanced
   
   # Sync critical writes
   sync
   fsync <file>

================================================================================
7. Key Takeaways
================================================================================

.. code-block:: text

   Flash Types:
   ============
   NOR: Bootloaders, XIP, small, expensive
   NAND: Large storage, cheap, needs ECC
   eMMC/SD: Managed NAND, easy to use
   
   MTD Tools:
   ==========
   cat /proc/mtd
   mtdinfo -a
   flash_erase /dev/mtd2 0 0
   nanddump -f backup.img /dev/mtd2
   nandwrite -p /dev/mtd2 image.bin
   
   UBI Commands:
   =============
   ubiformat /dev/mtd2
   ubiattach -p /dev/mtd2
   ubimkvol /dev/ubi0 -N rootfs -m
   mount -t ubifs ubi0:rootfs /mnt
   
   Filesystems:
   ============
   ext4: eMMC/SD, general purpose
   SquashFS: Read-only, compressed
   UBIFS: Raw NAND, wear leveling
   F2FS: eMMC/SD, flash-friendly
   JFFS2: Legacy, small flash
   
   Best Practices:
   ===============
   - Use UBI+UBIFS for raw NAND
   - Use ext4/F2FS for eMMC/SD
   - Mount with noatime
   - Use tmpfs for logs/tmp
   - Read-only root when possible
   - Separate data partitions

================================================================================
END OF CHEATSHEET
================================================================================
