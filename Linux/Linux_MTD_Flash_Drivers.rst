================================================================================
Linux MTD (Memory Technology Device) and Flash Drivers
================================================================================

:Author: Embedded Systems Cheatsheet Collection
:Date: January 19, 2026
:Version: 1.0
:Source: Embedded Linux System Design and Development (2006)
:Focus: MTD subsystem, NOR/NAND flash, JFFS2, flash mapping

.. contents:: Table of Contents
   :depth: 3
   :local:

================================================================================
1. MTD Subsystem Overview
================================================================================

1.1 What is MTD?
--------------------------------------------------------------------------------

**MTD (Memory Technology Device)** is the Linux subsystem for onboard
storage devices (flash, ROM, RAM). It provides a uniform interface for
flash chips and memory devices that behave differently from traditional
block devices like hard disks.

**Why MTD? Flash vs Hard Disk Differences:**

+---------------------------+---------------------------+
| Hard Disk                 | Flash Memory              |
+===========================+===========================+
| 512-byte sectors          | 64KB-128KB sectors        |
+---------------------------+---------------------------+
| In-place write            | Erase before write        |
+---------------------------+---------------------------+
| Unlimited write cycles    | Limited erase cycles      |
+---------------------------+---------------------------+
| No wear leveling needed   | Requires wear leveling    |
+---------------------------+---------------------------+
| Buffer cache friendly     | Needs special file systems|
+---------------------------+---------------------------+

**MTD Advantages:**

- Direct memory access (no block device overhead)
- Erase region awareness
- Wear leveling support
- Bad block management (for NAND)
- Partition management
- Flash-aware file systems (JFFS2, UBIFS)

1.2 MTD Architecture
--------------------------------------------------------------------------------

::

   User Applications
        ↓
   +---------------------------------------------------+
   | MTD Applications Layer                            |
   | - JFFS2, UBIFS (file systems)                     |
   | - NFTL (NAND Flash Translation Layer)             |
   | - User-space utilities (flashcp, flash_erase)     |
   +---------------------------------------------------+
        ↓
   +---------------------------------------------------+
   | MTD Core (Character + Block Device Interface)     |
   | - /dev/mtd0, /dev/mtd1 (character)                |
   | - /dev/mtdblock0, /dev/mtdblock1 (block)          |
   | - Partition management                            |
   +---------------------------------------------------+
        ↓
   +---------------------------------------------------+
   | Low-Level Flash Drivers                           |
   | - CFI (Common Flash Interface)                    |
   | - NAND driver                                     |
   | - Custom flash drivers                            |
   +---------------------------------------------------+
        ↓
   +---------------------------------------------------+
   | Flash Mapping / BSP Layer                         |
   | - Board-specific flash map                        |
   | - I/O routines (readb/writeb)                     |
   +---------------------------------------------------+
        ↓
   Hardware (Flash Chips + Board)

**MTD Components:**

1. **MTD Core:** Provides character and block device interfaces
2. **Low-level drivers:** CFI, NAND, RAM drivers
3. **Flash mapping:** Board-specific flash location and access
4. **MTD applications:** File systems (JFFS2, UBIFS), utilities

================================================================================
2. NOR vs NAND Flash
================================================================================

2.1 Comparison Table
--------------------------------------------------------------------------------

+---------------------+-------------------------+-------------------------+
| Feature             | NOR Flash               | NAND Flash              |
+=====================+=========================+=========================+
| **Interface**       | Parallel address/data   | Serial I/O, multiplexed |
|                     | bus like SRAM           | command/address/data    |
+---------------------+-------------------------+-------------------------+
| **Access**          | Random byte access      | Page-based access       |
+---------------------+-------------------------+-------------------------+
| **Performance**     | - Fast read (70-100ns)  | - Fast read (25ns)      |
|                     | - Slow write (10μs/byte)| - Fast write (200μs/pg) |
|                     | - Slow erase (1s/64KB)  | - Fast erase (2ms/blk)  |
+---------------------+-------------------------+-------------------------+
| **Execute-in-Place**| Yes (XIP supported)     | No (copy to RAM needed) |
+---------------------+-------------------------+-------------------------+
| **Erase Unit**      | Block (64KB-128KB)      | Block (128KB-256KB)     |
+---------------------+-------------------------+-------------------------+
| **Write Unit**      | Byte/word               | Page (512B-4KB)         |
+---------------------+-------------------------+-------------------------+
| **Bad Blocks**      | None (factory perfect)  | Expected (2% initial)   |
+---------------------+-------------------------+-------------------------+
| **Erase Cycles**    | 100,000                 | 1,000,000               |
+---------------------+-------------------------+-------------------------+
| **Density**         | Lower (up to 256MB)     | Higher (GB range)       |
+---------------------+-------------------------+-------------------------+
| **Cost per Bit**    | Higher                  | Lower (3-5x cheaper)    |
+---------------------+-------------------------+-------------------------+
| **Use Case**        | Code storage, boot      | Data storage, file      |
|                     | loader                  | systems                 |
+---------------------+-------------------------+-------------------------+

2.2 NOR Flash Characteristics
--------------------------------------------------------------------------------

**Organization:**

::

   NOR Flash Chip (e.g., 16MB)
   ├── Block 0  (64KB) - Erase Region 0
   ├── Block 1  (64KB)
   ├── ...
   └── Block 255 (64KB)
   
   Each block:
   - Random byte access
   - Erase to 0xFF (all 1s)
   - Write changes 1 → 0 only

**Operations:**

.. code-block:: c

   /* NOR Flash Operations */
   
   /* Read - random access, no page boundaries */
   uint8_t data = *(volatile uint8_t *)(flash_base + offset);
   
   /* Erase - must erase block before write */
   nor_erase_block(flash_base, block_num);
   
   /* Write - can only change 1 to 0 */
   *(volatile uint8_t *)(flash_base + offset) = data;

**CFI (Common Flash Interface):**

- Industry standard for NOR flash compatibility
- Auto-detection of flash parameters
- Query interface to read:
  - Manufacturer ID
  - Device ID
  - Block sizes
  - Erase timeout
  - Programming timeout

2.3 NAND Flash Characteristics
--------------------------------------------------------------------------------

**Organization:**

::

   NAND Flash Chip (e.g., 256MB)
   ├── Block 0  (128KB)
   │   ├── Page 0  (2KB data + 64B OOB)
   │   ├── Page 1  (2KB data + 64B OOB)
   │   ├── ...
   │   └── Page 63 (2KB data + 64B OOB)
   ├── Block 1  (128KB)
   ├── ...
   └── Block 2047 (128KB)

**Page Structure:**

::

   Page (2048 bytes data + 64 bytes OOB)
   ┌────────────────────────────┬──────────────┐
   │   Main Data (2048 bytes)   │   OOB (64B)  │
   │                            │   - ECC      │
   │                            │   - Bad mark │
   │                            │   - Metadata │
   └────────────────────────────┴──────────────┘

**Operations:**

.. code-block:: c

   /* NAND Flash Operations */
   
   /* Read page */
   nand_read_page(chip, page_addr, buffer, oob_buffer);
   
   /* Write page (must be in erased block) */
   nand_write_page(chip, page_addr, buffer, oob_buffer);
   
   /* Erase block */
   nand_erase_block(chip, block_addr);

**OOB (Out-of-Band) Data:**

- ECC (Error Correction Code) bytes
- Bad block markers
- File system metadata
- Wear leveling info

================================================================================
3. Flash Partitioning and Mapping
================================================================================

3.1 Flash Map Design
--------------------------------------------------------------------------------

**Typical Flash Map (4MB NOR):**

::

   +------------------------------+  0x00000000
   | Bootloader (U-Boot)          |
   | 256KB - Read Only            |
   | Partition: /dev/mtd0         |
   +------------------------------+  0x00040000
   | Kernel Image                 |
   | 640KB - Read Only            |
   | Partition: /dev/mtd1         |
   +------------------------------+  0x000E0000
   | Root FS (CRAMFS)             |
   | 2MB - Read Only              |
   | Partition: /dev/mtd2         |
   +------------------------------+  0x002E0000
   | User Data (JFFS2)            |
   | 1.2MB - Read/Write           |
   | Partition: /dev/mtd3         |
   +------------------------------+  0x00400000

**Design Considerations:**

1. **Bootloader partition:** Must be write-protected
2. **Kernel partition:** Can use LZMA compression
3. **Root filesystem:** CRAMFS (compressed, read-only) or JFFS2
4. **Data partition:** JFFS2 (journaling) or UBIFS (for NAND)

3.2 Flash Mapping Driver
--------------------------------------------------------------------------------

**Location:** ``drivers/mtd/maps/myboard-flash.c``

**Example Flash Map Driver:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/mtd/mtd.h>
   #include <linux/mtd/map.h>
   #include <linux/mtd/partitions.h>
   
   #define FLASH_PHYS_ADDR  0x00000000
   #define FLASH_SIZE       0x00400000  /* 4MB */
   
   static struct mtd_info *mymtd;
   
   /* Define flash partitions */
   static struct mtd_partition myboard_partitions[] = {
       {
           .name   = "bootloader",
           .offset = 0,
           .size   = 0x40000,      /* 256KB */
           .mask_flags = MTD_WRITEABLE,  /* Read-only */
       },
       {
           .name   = "kernel",
           .offset = 0x40000,
           .size   = 0xA0000,      /* 640KB */
           .mask_flags = MTD_WRITEABLE,
       },
       {
           .name   = "rootfs",
           .offset = 0xE0000,
           .size   = 0x200000,     /* 2MB */
           .mask_flags = MTD_WRITEABLE,
       },
       {
           .name   = "userdata",
           .offset = 0x2E0000,
           .size   = MTDPART_SIZ_FULL,  /* Remaining */
       },
   };
   
   /* Map definition */
   static struct map_info myboard_map = {
       .name       = "myboard-flash",
       .phys       = FLASH_PHYS_ADDR,
       .size       = FLASH_SIZE,
       .bankwidth  = 2,  /* 16-bit */
   };
   
   static int __init myboard_flash_init(void)
   {
       /* Request memory region */
       if (!request_mem_region(myboard_map.phys, myboard_map.size,
                               myboard_map.name)) {
           pr_err("Failed to request flash region\n");
           return -EBUSY;
       }
       
       /* Map flash to virtual address */
       myboard_map.virt = ioremap(myboard_map.phys, myboard_map.size);
       if (!myboard_map.virt) {
           release_mem_region(myboard_map.phys, myboard_map.size);
           return -ENOMEM;
       }
       
       /* Set up access functions */
       simple_map_init(&myboard_map);
       
       /* Probe for CFI flash */
       mymtd = do_map_probe("cfi_probe", &myboard_map);
       if (!mymtd) {
           /* Try JEDEC probe if CFI fails */
           mymtd = do_map_probe("jedec_probe", &myboard_map);
       }
       
       if (!mymtd) {
           pr_err("Flash probe failed\n");
           iounmap(myboard_map.virt);
           release_mem_region(myboard_map.phys, myboard_map.size);
           return -ENXIO;
       }
       
       mymtd->owner = THIS_MODULE;
       
       /* Register partitions */
       mtd_device_register(mymtd, myboard_partitions,
                          ARRAY_SIZE(myboard_partitions));
       
       pr_info("Flash: %s registered, %lldKB\n",
               myboard_map.name, (long long)mymtd->size >> 10);
       
       return 0;
   }
   
   static void __exit myboard_flash_exit(void)
   {
       if (mymtd) {
           mtd_device_unregister(mymtd);
           map_destroy(mymtd);
       }
       
       if (myboard_map.virt) {
           iounmap(myboard_map.virt);
           release_mem_region(myboard_map.phys, myboard_map.size);
       }
   }
   
   module_init(myboard_flash_init);
   module_exit(myboard_flash_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Board Vendor");
   MODULE_DESCRIPTION("Flash map for MyBoard");

3.3 Device Tree Flash Mapping
--------------------------------------------------------------------------------

**Modern Method - Device Tree:**

.. code-block:: dts

   /* arch/arm/boot/dts/myboard.dts */
   
   flash@0 {
       compatible = "cfi-flash";
       reg = <0x00000000 0x00400000>;  /* 4MB at address 0 */
       bank-width = <2>;  /* 16-bit */
       
       partitions {
           compatible = "fixed-partitions";
           #address-cells = <1>;
           #size-cells = <1>;
           
           partition@0 {
               label = "bootloader";
               reg = <0x00000000 0x00040000>;
               read-only;
           };
           
           partition@40000 {
               label = "kernel";
               reg = <0x00040000 0x000A0000>;
               read-only;
           };
           
           partition@e0000 {
               label = "rootfs";
               reg = <0x000E0000 0x00200000>;
               read-only;
           };
           
           partition@2e0000 {
               label = "userdata";
               reg = <0x002E0000 0x00120000>;
           };
       };
   };

================================================================================
4. MTD Core Interface
================================================================================

4.1 struct mtd_info
--------------------------------------------------------------------------------

**Key Data Structure:**

.. code-block:: c

   /* include/linux/mtd/mtd.h */
   
   struct mtd_info {
       u_char type;          /* MTD_NORFLASH, MTD_NANDFLASH, etc. */
       uint32_t flags;       /* MTD_WRITEABLE, MTD_BIT_WRITEABLE */
       uint64_t size;        /* Total size in bytes */
       uint32_t erasesize;   /* Erase block size */
       uint32_t writesize;   /* Write size (page for NAND) */
       uint32_t oobsize;     /* OOB size per writesize */
       
       /* Function pointers */
       int (*erase)(struct mtd_info *mtd, struct erase_info *instr);
       int (*read)(struct mtd_info *mtd, loff_t from, size_t len,
                   size_t *retlen, u_char *buf);
       int (*write)(struct mtd_info *mtd, loff_t to, size_t len,
                    size_t *retlen, const u_char *buf);
       
       int (*read_oob)(struct mtd_info *mtd, loff_t from,
                       struct mtd_oob_ops *ops);
       int (*write_oob)(struct mtd_info *mtd, loff_t to,
                        struct mtd_oob_ops *ops);
       
       int (*lock)(struct mtd_info *mtd, loff_t ofs, uint64_t len);
       int (*unlock)(struct mtd_info *mtd, loff_t ofs, uint64_t len);
       
       void (*sync)(struct mtd_info *mtd);
       int (*suspend)(struct mtd_info *mtd);
       void (*resume)(struct mtd_info *mtd);
       
       const char *name;
       int index;
       
       /* ECC information */
       struct mtd_ecc_stats ecc_stats;
       
       /* Master MTD (for partitions) */
       struct mtd_info *master;
       
       void *priv;  /* Driver private data */
   };

4.2 MTD Operations
--------------------------------------------------------------------------------

**Erase Operation:**

.. code-block:: c

   #include <linux/mtd/mtd.h>
   
   int erase_flash_block(struct mtd_info *mtd, loff_t offset, size_t len)
   {
       struct erase_info erase;
       int ret;
       
       memset(&erase, 0, sizeof(erase));
       erase.mtd = mtd;
       erase.addr = offset;
       erase.len = len;
       
       ret = mtd_erase(mtd, &erase);
       if (ret) {
           pr_err("Erase failed at 0x%llx: %d\n", offset, ret);
           return ret;
       }
       
       return 0;
   }

**Read Operation:**

.. code-block:: c

   int read_from_flash(struct mtd_info *mtd, loff_t offset,
                       void *buffer, size_t len)
   {
       size_t retlen;
       int ret;
       
       ret = mtd_read(mtd, offset, len, &retlen, buffer);
       if (ret < 0 && ret != -EUCLEAN) {  /* -EUCLEAN = corrected bitflips */
           pr_err("Read failed at 0x%llx: %d\n", offset, ret);
           return ret;
       }
       
       if (retlen != len) {
           pr_warn("Short read: got %zu, expected %zu\n", retlen, len);
           return -EIO;
       }
       
       return 0;
   }

**Write Operation:**

.. code-block:: c

   int write_to_flash(struct mtd_info *mtd, loff_t offset,
                      const void *buffer, size_t len)
   {
       size_t retlen;
       int ret;
       
       /* Flash must be erased before writing */
       ret = erase_flash_block(mtd, offset, mtd->erasesize);
       if (ret)
           return ret;
       
       ret = mtd_write(mtd, offset, len, &retlen, buffer);
       if (ret) {
           pr_err("Write failed at 0x%llx: %d\n", offset, ret);
           return ret;
       }
       
       if (retlen != len) {
           pr_warn("Short write: wrote %zu, expected %zu\n", retlen, len);
           return -EIO;
       }
       
       return 0;
   }

**Lock/Unlock Operations:**

.. code-block:: c

   /* Protect bootloader partition */
   int lock_bootloader(struct mtd_info *mtd)
   {
       loff_t offset = 0;
       uint64_t len = 0x40000;  /* 256KB */
       
       return mtd_lock(mtd, offset, len);
   }
   
   /* Unlock for firmware upgrade */
   int unlock_for_upgrade(struct mtd_info *mtd)
   {
       loff_t offset = 0;
       uint64_t len = mtd->size;  /* Entire flash */
       
       return mtd_unlock(mtd, offset, len);
   }

================================================================================
5. NAND Flash Driver
================================================================================

5.1 NAND Controller Setup
--------------------------------------------------------------------------------

.. code-block:: c

   #include <linux/mtd/nand.h>
   #include <linux/mtd/nand_ecc.h>
   
   struct mynand_info {
       struct nand_chip    chip;
       struct mtd_info     mtd;
       void __iomem        *io_base;
       int                 irq;
   };
   
   /* Hardware-specific functions */
   static void mynand_cmd_ctrl(struct mtd_info *mtd, int cmd,
                               unsigned int ctrl)
   {
       struct nand_chip *chip = mtd_to_nand(mtd);
       struct mynand_info *info = nand_get_controller_data(chip);
       
       if (ctrl & NAND_CTRL_CHANGE) {
           if (ctrl & NAND_CLE)
               writeb(cmd, info->io_base + NAND_CMD_REG);
           else if (ctrl & NAND_ALE)
               writeb(cmd, info->io_base + NAND_ADDR_REG);
       }
   }
   
   static int mynand_dev_ready(struct mtd_info *mtd)
   {
       struct nand_chip *chip = mtd_to_nand(mtd);
       struct mynand_info *info = nand_get_controller_data(chip);
       
       return readl(info->io_base + NAND_STATUS_REG) & NAND_STATUS_READY;
   }
   
   static void mynand_read_buf(struct mtd_info *mtd, uint8_t *buf, int len)
   {
       struct nand_chip *chip = mtd_to_nand(mtd);
       struct mynand_info *info = nand_get_controller_data(chip);
       
       readsb(info->io_base + NAND_DATA_REG, buf, len);
   }
   
   static void mynand_write_buf(struct mtd_info *mtd, const uint8_t *buf,
                                int len)
   {
       struct nand_chip *chip = mtd_to_nand(mtd);
       struct mynand_info *info = nand_get_controller_data(chip);
       
       writesb(info->io_base + NAND_DATA_REG, buf, len);
   }

5.2 NAND Driver Initialization
--------------------------------------------------------------------------------

.. code-block:: c

   static int mynand_probe(struct platform_device *pdev)
   {
       struct mynand_info *info;
       struct nand_chip *chip;
       struct mtd_info *mtd;
       struct resource *res;
       int ret;
       
       /* Allocate driver structure */
       info = devm_kzalloc(&pdev->dev, sizeof(*info), GFP_KERNEL);
       if (!info)
           return -ENOMEM;
       
       /* Map NAND controller registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       info->io_base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(info->io_base))
           return PTR_ERR(info->io_base);
       
       /* Initialize NAND chip structure */
       chip = &info->chip;
       mtd = &info->mtd;
       
       chip->cmd_ctrl = mynand_cmd_ctrl;
       chip->dev_ready = mynand_dev_ready;
       chip->read_buf = mynand_read_buf;
       chip->write_buf = mynand_write_buf;
       
       chip->chip_delay = 20;  /* 20us command delay */
       chip->options = NAND_NO_SUBPAGE_WRITE;
       
       /* Set ECC mode */
       chip->ecc.mode = NAND_ECC_SOFT;
       chip->ecc.algo = NAND_ECC_HAMMING;
       
       nand_set_controller_data(chip, info);
       nand_set_flash_node(chip, pdev->dev.of_node);
       
       mtd->dev.parent = &pdev->dev;
       mtd->owner = THIS_MODULE;
       
       /* Scan for NAND chip */
       ret = nand_scan(mtd, 1);
       if (ret) {
           dev_err(&pdev->dev, "NAND scan failed: %d\n", ret);
           return ret;
       }
       
       /* Register MTD device with partitions */
       ret = mtd_device_register(mtd, NULL, 0);
       if (ret) {
           nand_release(mtd);
           return ret;
       }
       
       platform_set_drvdata(pdev, info);
       
       dev_info(&pdev->dev, "NAND: %lldMB, page %d, block %d\n",
                (long long)mtd->size >> 20,
                mtd->writesize, mtd->erasesize);
       
       return 0;
   }

5.3 Bad Block Management
--------------------------------------------------------------------------------

.. code-block:: c

   /* Check if block is bad */
   int is_block_bad(struct mtd_info *mtd, loff_t offset)
   {
       return mtd_block_isbad(mtd, offset);
   }
   
   /* Mark block as bad */
   int mark_block_bad(struct mtd_info *mtd, loff_t offset)
   {
       return mtd_block_markbad(mtd, offset);
   }
   
   /* Skip bad blocks when reading */
   int read_skip_bad(struct mtd_info *mtd, loff_t from, size_t len,
                     void *buf)
   {
       size_t retlen;
       int ret;
       loff_t offset = from;
       size_t remaining = len;
       uint8_t *ptr = buf;
       
       while (remaining > 0) {
           /* Check if block is bad */
           if (mtd_block_isbad(mtd, offset)) {
               pr_warn("Skipping bad block at 0x%llx\n", offset);
               offset += mtd->erasesize;
               continue;
           }
           
           /* Read from good block */
           size_t to_read = min_t(size_t, remaining, mtd->erasesize);
           ret = mtd_read(mtd, offset, to_read, &retlen, ptr);
           if (ret < 0 && ret != -EUCLEAN)
               return ret;
           
           ptr += retlen;
           offset += retlen;
           remaining -= retlen;
       }
       
       return 0;
   }

================================================================================
6. Flash File Systems
================================================================================

6.1 JFFS2 (Journaling Flash File System 2)
--------------------------------------------------------------------------------

**Features:**

- Wear leveling
- Compression (zlib, LZO)
- Journaling (crash-safe)
- Bad block handling
- Power-loss protection

**Mount JFFS2:**

.. code-block:: bash

   # Erase flash partition
   flash_erase /dev/mtd3 0 0
   
   # Mount JFFS2
   mount -t jffs2 /dev/mtdblock3 /mnt/data
   
   # Kernel config
   CONFIG_JFFS2_FS=y
   CONFIG_JFFS2_FS_WRITEBUFFER=y  # For NAND
   CONFIG_JFFS2_COMPRESSION_OPTIONS=y
   CONFIG_JFFS2_LZO=y

**JFFS2 in Flash Map:**

.. code-block:: c

   static struct mtd_partition partitions[] = {
       {
           .name   = "data",
           .offset = 0x100000,
           .size   = 0x300000,
       },
   };

.. code-block:: bash

   # Create JFFS2 image
   mkfs.jffs2 -p -l -e 128KiB -r /path/to/rootfs -o rootfs.jffs2
   
   # Flash to device
   flash_erase /dev/mtd2 0 0
   nandwrite -p /dev/mtd2 rootfs.jffs2

6.2 CRAMFS (Compressed ROM File System)
--------------------------------------------------------------------------------

**Features:**

- Read-only
- High compression ratio
- Fast boot
- Low RAM usage

**Create and Mount:**

.. code-block:: bash

   # Create CRAMFS image
   mkcramfs /path/to/rootfs rootfs.cramfs
   
   # Flash to device
   flashcp rootfs.cramfs /dev/mtd2
   
   # Mount
   mount -t cramfs /dev/mtdblock2 /mnt/rootfs
   
   # Kernel config
   CONFIG_CRAMFS=y

6.3 UBIFS (Unsorted Block Image File System)
--------------------------------------------------------------------------------

**Better than JFFS2 for large NAND:**

- Faster mount time
- Better performance on large NAND
- Scalable to GB sizes

**Setup UBI and UBIFS:**

.. code-block:: bash

   # Attach MTD device to UBI
   ubiattach -m 3 -d 0
   
   # Create UBI volume
   ubimkvol /dev/ubi0 -N rootfs -s 100MiB
   
   # Create UBIFS image
   mkfs.ubifs -r /path/to/rootfs -m 2048 -e 124KiB -c 1000 -o rootfs.ubifs
   
   # Create UBI image
   ubinize -o ubi.img -m 2048 -p 128KiB ubinize.cfg
   
   # Flash UBI image
   nandwrite -p /dev/mtd3 ubi.img
   
   # Mount UBIFS
   mount -t ubifs ubi0:rootfs /mnt/rootfs

================================================================================
7. MTD Utilities
================================================================================

7.1 Common Commands
--------------------------------------------------------------------------------

.. code-block:: bash

   # List MTD partitions
   cat /proc/mtd
   
   # Erase partition
   flash_erase /dev/mtd3 0 0
   
   # Read flash
   nanddump -f dump.img /dev/mtd3
   
   # Write flash (with ECC, skip bad blocks)
   nandwrite -p /dev/mtd3 image.bin
   
   # Copy file to flash
   flashcp file.bin /dev/mtd3
   
   # Mark bad block
   nandtest --markbad /dev/mtd3
   
   # Check for bad blocks
   nandtest /dev/mtd3

7.2 User-Space MTD API
--------------------------------------------------------------------------------

.. code-block:: c

   #include <mtd/mtd-user.h>
   #include <sys/ioctl.h>
   #include <fcntl.h>
   
   int fd = open("/dev/mtd3", O_RDWR);
   
   /* Get MTD info */
   struct mtd_info_user info;
   ioctl(fd, MEMGETINFO, &info);
   printf("MTD size: %u, erase size: %u\n", info.size, info.erasesize);
   
   /* Erase block */
   struct erase_info_user erase;
   erase.start = 0;
   erase.length = info.erasesize;
   ioctl(fd, MEMERASE, &erase);
   
   /* Lock/unlock */
   struct erase_info_user lock_info;
   lock_info.start = 0;
   lock_info.length = info.size;
   ioctl(fd, MEMLOCK, &lock_info);    /* Lock */
   ioctl(fd, MEMUNLOCK, &lock_info);  /* Unlock */
   
   close(fd);

================================================================================
8. Best Practices
================================================================================

**Flash Partitioning:**

- Separate read-only and read-write partitions
- Protect bootloader with write-lock
- Use JFFS2/UBIFS for writable data
- Leave extra space for bad block growth (NAND)

**Performance:**

- Use UBIFS instead of JFFS2 for large NAND
- Enable compression for space-constrained systems
- Use hardware ECC if available
- Minimize writes to extend flash lifetime

**Reliability:**

- Always handle bad blocks (NAND)
- Implement power-loss protection
- Use journaling file systems
- Keep backup of critical data

**Development:**

- Test with flash_erase and nandwrite
- Monitor bad block growth
- Profile write patterns for wear leveling
- Use MTD_DEBUG for debugging

================================================================================
End of Linux MTD and Flash Drivers Cheatsheet
================================================================================
