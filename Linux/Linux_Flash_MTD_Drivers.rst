========================================
Linux Flash and MTD Drivers Guide
========================================

:Author: Linux Device Driver Documentation
:Date: January 2026
:Version: 1.0
:Focus: Memory Technology Device (MTD) subsystem and flash drivers

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential MTD Commands
----------------------

.. code-block:: bash

   # List MTD devices
   cat /proc/mtd
   ls -l /dev/mtd*
   
   # MTD information
   mtdinfo /dev/mtd0
   mtdinfo -a  # All devices
   
   # Flash erase
   flash_erase /dev/mtd0 0 0  # Erase all
   flash_erase /dev/mtd0 0x10000 1  # Erase one block at offset
   
   # Read/Write
   dd if=/dev/mtd0 of=backup.img
   dd if=image.bin of=/dev/mtd0
   
   # NAND flash tools
   nandwrite /dev/mtd0 image.bin
   nanddump /dev/mtd0 -f backup.bin
   
   # UBI management
   ubiformat /dev/mtd0
   ubiattach -m 0 -d 0
   ubimkvol /dev/ubi0 -N rootfs -s 100MiB

Quick MTD Partitioning
----------------------

.. code-block:: dts

   // Device tree MTD partitions
   flash@0 {
       compatible = "jedec,spi-nor";
       reg = <0>;
       spi-max-frequency = <50000000>;
       
       partitions {
           compatible = "fixed-partitions";
           #address-cells = <1>;
           #size-cells = <1>;
           
           bootloader@0 {
               label = "bootloader";
               reg = <0x000000 0x040000>;
               read-only;
           };
           
           kernel@40000 {
               label = "kernel";
               reg = <0x040000 0x400000>;
           };
           
           rootfs@440000 {
               label = "rootfs";
               reg = <0x440000 0xbc0000>;
           };
       };
   };

MTD Subsystem Overview
======================

MTD Architecture
----------------

.. code-block:: text

   MTD Layer Architecture:
   
   User Space
   ├── /dev/mtdX (char device)
   ├── /dev/mtdblockX (block device)
   └── MTD utilities (mtdinfo, flash_erase, etc.)
   
   Kernel Space
   ├── MTD Core
   │   ├── Character device interface
   │   ├── Block device interface (mtdblock)
   │   └── Partition management
   │
   ├── MTD Translation Layer
   │   ├── NFTL (NAND Flash Translation Layer)
   │   ├── FTL (Flash Translation Layer)
   │   └── JFFS2/UBIFS filesystem support
   │
   ├── MTD Device Drivers
   │   ├── CFI (Common Flash Interface)
   │   ├── JEDEC
   │   ├── NAND drivers
   │   └── NOR drivers
   │
   └── Hardware Layer
       ├── SPI NOR controllers
       ├── Parallel NOR controllers
       └── NAND controllers

Flash Types
-----------

.. code-block:: text

   NOR Flash:
   - Random access (XIP capable)
   - Byte-level read
   - Block erase required for write
   - Higher cost per bit
   - Better for code execution
   - Typical sizes: 1-128 MB
   - Use cases: Bootloaders, firmware
   
   NAND Flash:
   - Page-based access
   - Faster write/erase
   - Requires error correction (ECC)
   - Bad block management needed
   - Lower cost per bit
   - Higher density
   - Typical sizes: 128 MB - 256 GB
   - Use cases: Data storage, filesystems
   
   SPI NOR Flash:
   - Serial interface (SPI)
   - Lower pin count
   - Smaller sizes (typically < 16 MB)
   - Easy to interface
   - Use cases: Settings, small code storage

MTD Driver Structure
====================

Basic MTD Driver
----------------

.. code-block:: c

   #include <linux/mtd/mtd.h>
   #include <linux/module.h>
   #include <linux/platform_device.h>
   
   struct my_flash_info {
       struct mtd_info mtd;
       void __iomem *base;
       struct mutex lock;
   };
   
   static int my_flash_read(struct mtd_info *mtd, loff_t from, size_t len,
                            size_t *retlen, u_char *buf) {
       struct my_flash_info *info = mtd->priv;
       
       mutex_lock(&info->lock);
       memcpy_fromio(buf, info->base + from, len);
       *retlen = len;
       mutex_unlock(&info->lock);
       
       return 0;
   }
   
   static int my_flash_write(struct mtd_info *mtd, loff_t to, size_t len,
                             size_t *retlen, const u_char *buf) {
       struct my_flash_info *info = mtd->priv;
       
       mutex_lock(&info->lock);
       memcpy_toio(info->base + to, buf, len);
       *retlen = len;
       mutex_unlock(&info->lock);
       
       return 0;
   }
   
   static int my_flash_erase(struct mtd_info *mtd, struct erase_info *instr) {
       struct my_flash_info *info = mtd->priv;
       
       mutex_lock(&info->lock);
       // Erase implementation
       memset_io(info->base + instr->addr, 0xff, instr->len);
       mutex_unlock(&info->lock);
       
       return 0;
   }
   
   static int my_flash_probe(struct platform_device *pdev) {
       struct my_flash_info *info;
       struct resource *res;
       int ret;
       
       info = devm_kzalloc(&pdev->dev, sizeof(*info), GFP_KERNEL);
       if (!info)
           return -ENOMEM;
       
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       info->base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(info->base))
           return PTR_ERR(info->base);
       
       mutex_init(&info->lock);
       
       // Initialize MTD structure
       info->mtd.name = "my-flash";
       info->mtd.type = MTD_NORFLASH;
       info->mtd.flags = MTD_CAP_NORFLASH;
       info->mtd.size = resource_size(res);
       info->mtd.erasesize = 0x10000;  // 64KB erase block
       info->mtd.writesize = 1;         // Byte write
       info->mtd.writebufsize = 0;
       info->mtd.owner = THIS_MODULE;
       info->mtd.priv = info;
       info->mtd._read = my_flash_read;
       info->mtd._write = my_flash_write;
       info->mtd._erase = my_flash_erase;
       
       platform_set_drvdata(pdev, info);
       
       ret = mtd_device_register(&info->mtd, NULL, 0);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register MTD device\n");
           return ret;
       }
       
       dev_info(&pdev->dev, "MTD device registered: %llu bytes\n",
                info->mtd.size);
       return 0;
   }
   
   static int my_flash_remove(struct platform_device *pdev) {
       struct my_flash_info *info = platform_get_drvdata(pdev);
       
       mtd_device_unregister(&info->mtd);
       return 0;
   }
   
   static const struct of_device_id my_flash_of_match[] = {
       { .compatible = "vendor,my-flash" },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_flash_of_match);
   
   static struct platform_driver my_flash_driver = {
       .probe  = my_flash_probe,
       .remove = my_flash_remove,
       .driver = {
           .name = "my-flash",
           .of_match_table = my_flash_of_match,
       },
   };
   module_platform_driver(my_flash_driver);

MTD Partitions
--------------

.. code-block:: c

   #include <linux/mtd/partitions.h>
   
   static struct mtd_partition my_partitions[] = {
       {
           .name   = "bootloader",
           .offset = 0,
           .size   = 0x40000,  // 256KB
           .mask_flags = MTD_WRITEABLE,  // Read-only
       },
       {
           .name   = "kernel",
           .offset = MTDPART_OFS_APPEND,
           .size   = 0x400000,  // 4MB
       },
       {
           .name   = "rootfs",
           .offset = MTDPART_OFS_APPEND,
           .size   = MTDPART_SIZ_FULL,  // Rest of flash
       },
   };
   
   // Register with partitions
   ret = mtd_device_register(&info->mtd, my_partitions,
                             ARRAY_SIZE(my_partitions));

SPI NOR Flash Driver
====================

SPI NOR Example
---------------

.. code-block:: c

   #include <linux/mtd/spi-nor.h>
   #include <linux/spi/spi.h>
   
   struct my_nor {
       struct spi_nor nor;
       struct spi_device *spi;
   };
   
   static int my_nor_read_reg(struct spi_nor *nor, u8 opcode, u8 *buf, size_t len) {
       struct my_nor *flash = nor->priv;
       struct spi_transfer t[2] = {};
       struct spi_message m;
       
       spi_message_init(&m);
       
       t[0].tx_buf = &opcode;
       t[0].len = 1;
       spi_message_add_tail(&t[0], &m);
       
       t[1].rx_buf = buf;
       t[1].len = len;
       spi_message_add_tail(&t[1], &m);
       
       return spi_sync(flash->spi, &m);
   }
   
   static int my_nor_write_reg(struct spi_nor *nor, u8 opcode, const u8 *buf,
                               size_t len) {
       struct my_nor *flash = nor->priv;
       u8 *cmd = kmalloc(len + 1, GFP_KERNEL);
       int ret;
       
       if (!cmd)
           return -ENOMEM;
       
       cmd[0] = opcode;
       memcpy(&cmd[1], buf, len);
       
       ret = spi_write(flash->spi, cmd, len + 1);
       kfree(cmd);
       
       return ret;
   }
   
   static ssize_t my_nor_read(struct spi_nor *nor, loff_t from, size_t len,
                              u_char *buf) {
       struct my_nor *flash = nor->priv;
       struct spi_transfer t[2] = {};
       struct spi_message m;
       u8 cmd[4];
       
       cmd[0] = SPINOR_OP_READ;
       cmd[1] = (from >> 16) & 0xff;
       cmd[2] = (from >> 8) & 0xff;
       cmd[3] = from & 0xff;
       
       spi_message_init(&m);
       
       t[0].tx_buf = cmd;
       t[0].len = 4;
       spi_message_add_tail(&t[0], &m);
       
       t[1].rx_buf = buf;
       t[1].len = len;
       spi_message_add_tail(&t[1], &m);
       
       spi_sync(flash->spi, &m);
       return len;
   }
   
   static ssize_t my_nor_write(struct spi_nor *nor, loff_t to, size_t len,
                               const u_char *buf) {
       struct my_nor *flash = nor->priv;
       u8 *cmd = kmalloc(len + 4, GFP_KERNEL);
       int ret;
       
       if (!cmd)
           return -ENOMEM;
       
       cmd[0] = SPINOR_OP_PP;
       cmd[1] = (to >> 16) & 0xff;
       cmd[2] = (to >> 8) & 0xff;
       cmd[3] = to & 0xff;
       memcpy(&cmd[4], buf, len);
       
       ret = spi_write(flash->spi, cmd, len + 4);
       kfree(cmd);
       
       return ret < 0 ? ret : len;
   }
   
   static int my_nor_erase(struct spi_nor *nor, loff_t offset) {
       struct my_nor *flash = nor->priv;
       u8 cmd[4];
       
       cmd[0] = SPINOR_OP_SE;  // Sector erase
       cmd[1] = (offset >> 16) & 0xff;
       cmd[2] = (offset >> 8) & 0xff;
       cmd[3] = offset & 0xff;
       
       return spi_write(flash->spi, cmd, 4);
   }
   
   static const struct spi_nor_controller_ops my_nor_controller_ops = {
       .read_reg   = my_nor_read_reg,
       .write_reg  = my_nor_write_reg,
       .read       = my_nor_read,
       .write      = my_nor_write,
       .erase      = my_nor_erase,
   };
   
   static int my_nor_probe(struct spi_device *spi) {
       struct my_nor *flash;
       struct spi_nor *nor;
       int ret;
       
       flash = devm_kzalloc(&spi->dev, sizeof(*flash), GFP_KERNEL);
       if (!flash)
           return -ENOMEM;
       
       flash->spi = spi;
       spi_set_drvdata(spi, flash);
       
       nor = &flash->nor;
       nor->dev = &spi->dev;
       nor->priv = flash;
       spi_nor_set_flash_node(nor, spi->dev.of_node);
       nor->controller_ops = &my_nor_controller_ops;
       
       ret = spi_nor_scan(nor, NULL, &hwcaps);
       if (ret)
           return ret;
       
       return mtd_device_register(&nor->mtd, NULL, 0);
   }
   
   static int my_nor_remove(struct spi_device *spi) {
       struct my_nor *flash = spi_get_drvdata(spi);
       
       mtd_device_unregister(&flash->nor.mtd);
       return 0;
   }

NAND Flash Driver
=================

NAND Controller Driver
-----------------------

.. code-block:: c

   #include <linux/mtd/rawnand.h>
   
   struct my_nand_controller {
       struct nand_controller controller;
       void __iomem *regs;
       struct clk *clk;
   };
   
   struct my_nand_chip {
       struct nand_chip chip;
       struct my_nand_controller *controller;
   };
   
   static int my_nand_exec_op(struct nand_chip *chip,
                              const struct nand_operation *op,
                              bool check_only) {
       struct my_nand_chip *my_chip = to_my_nand(chip);
       const struct nand_op_instr *instr;
       int i, ret = 0;
       
       if (check_only)
           return 0;
       
       for (i = 0; i < op->ninstrs; i++) {
           instr = &op->instrs[i];
           
           switch (instr->type) {
           case NAND_OP_CMD_INSTR:
               writeb(instr->ctx.cmd.opcode, my_chip->controller->regs + CMD_REG);
               break;
               
           case NAND_OP_ADDR_INSTR:
               for (unsigned int j = 0; j < instr->ctx.addr.naddrs; j++)
                   writeb(instr->ctx.addr.addrs[j],
                          my_chip->controller->regs + ADDR_REG);
               break;
               
           case NAND_OP_DATA_IN_INSTR:
               ioread8_rep(my_chip->controller->regs + DATA_REG,
                          instr->ctx.data.buf.in,
                          instr->ctx.data.len);
               break;
               
           case NAND_OP_DATA_OUT_INSTR:
               iowrite8_rep(my_chip->controller->regs + DATA_REG,
                           instr->ctx.data.buf.out,
                           instr->ctx.data.len);
               break;
               
           case NAND_OP_WAITRDY_INSTR:
               ret = my_nand_wait_ready(my_chip, instr->ctx.waitrdy.timeout_ms);
               if (ret)
                   return ret;
               break;
           }
       }
       
       return 0;
   }
   
   static const struct nand_controller_ops my_nand_controller_ops = {
       .exec_op = my_nand_exec_op,
       .attach_chip = my_nand_attach_chip,
       .detach_chip = my_nand_detach_chip,
   };
   
   static int my_nand_probe(struct platform_device *pdev) {
       struct my_nand_controller *nfc;
       struct my_nand_chip *my_chip;
       struct nand_chip *chip;
       struct mtd_info *mtd;
       struct resource *res;
       int ret;
       
       nfc = devm_kzalloc(&pdev->dev, sizeof(*nfc), GFP_KERNEL);
       if (!nfc)
           return -ENOMEM;
       
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       nfc->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(nfc->regs))
           return PTR_ERR(nfc->regs);
       
       nand_controller_init(&nfc->controller);
       nfc->controller.ops = &my_nand_controller_ops;
       
       my_chip = devm_kzalloc(&pdev->dev, sizeof(*my_chip), GFP_KERNEL);
       if (!my_chip)
           return -ENOMEM;
       
       chip = &my_chip->chip;
       mtd = nand_to_mtd(chip);
       
       chip->controller = &nfc->controller;
       my_chip->controller = nfc;
       
       mtd->dev.parent = &pdev->dev;
       nand_set_flash_node(chip, pdev->dev.of_node);
       
       // Scan NAND device
       ret = nand_scan(chip, 1);
       if (ret)
           return ret;
       
       ret = mtd_device_register(mtd, NULL, 0);
       if (ret) {
           nand_cleanup(chip);
           return ret;
       }
       
       platform_set_drvdata(pdev, nfc);
       return 0;
   }

ECC (Error Correction Code)
----------------------------

.. code-block:: c

   static int my_nand_attach_chip(struct nand_chip *chip) {
       struct mtd_info *mtd = nand_to_mtd(chip);
       
       // Configure ECC
       if (!chip->ecc.engine_type) {
           chip->ecc.engine_type = NAND_ECC_ENGINE_TYPE_ON_HOST;
           chip->ecc.algo = NAND_ECC_ALGO_HAMMING;
           chip->ecc.size = 512;
           chip->ecc.bytes = 3;
           chip->ecc.strength = 1;
           chip->ecc.read_page = my_nand_read_page_hwecc;
           chip->ecc.write_page = my_nand_write_page_hwecc;
       }
       
       return 0;
   }
   
   static int my_nand_read_page_hwecc(struct nand_chip *chip, uint8_t *buf,
                                      int oob_required, int page) {
       struct mtd_info *mtd = nand_to_mtd(chip);
       int ret, i, eccsize = chip->ecc.size;
       int eccbytes = chip->ecc.bytes;
       int eccsteps = chip->ecc.steps;
       uint8_t *p = buf;
       uint8_t *ecc_code = chip->ecc.code_buf;
       uint8_t *ecc_calc = chip->ecc.calc_buf;
       unsigned int max_bitflips = 0;
       
       // Read page
       ret = nand_read_page_op(chip, page, 0, NULL, 0);
       if (ret)
           return ret;
       
       for (i = 0; eccsteps; eccsteps--, i += eccbytes, p += eccsize) {
           chip->ecc.hwctl(chip, NAND_ECC_READ);
           
           ret = nand_read_data_op(chip, p, eccsize, false, false);
           if (ret)
               return ret;
           
           chip->ecc.calculate(chip, p, &ecc_calc[i]);
       }
       
       // Read OOB (ECC codes)
       ret = nand_read_data_op(chip, chip->oob_poi, mtd->oobsize, false, false);
       if (ret)
           return ret;
       
       // Extract ECC from OOB
       for (i = 0; i < chip->ecc.total; i++)
           ecc_code[i] = chip->oob_poi[chip->ecc.layout->eccpos[i]];
       
       // Correct errors
       eccsteps = chip->ecc.steps;
       p = buf;
       
       for (i = 0; eccsteps; eccsteps--, i += eccbytes, p += eccsize) {
           int stat;
           
           stat = chip->ecc.correct(chip, p, &ecc_code[i], &ecc_calc[i]);
           if (stat < 0) {
               mtd->ecc_stats.failed++;
           } else {
               mtd->ecc_stats.corrected += stat;
               max_bitflips = max_t(unsigned int, max_bitflips, stat);
           }
       }
       
       return max_bitflips;
   }

Bad Block Management
--------------------

.. code-block:: c

   // Check if block is bad
   int nand_block_isbad(struct mtd_info *mtd, loff_t ofs);
   
   // Mark block as bad
   int nand_block_markbad(struct mtd_info *mtd, loff_t ofs);
   
   // Example: Skip bad blocks
   static int write_with_bad_block_skip(struct mtd_info *mtd,
                                        loff_t to, size_t len,
                                        const u_char *buf) {
       size_t retlen;
       int ret;
       
       while (len > 0) {
           size_t block_start = to & ~(mtd->erasesize - 1);
           
           // Check if block is bad
           if (nand_block_isbad(mtd, block_start)) {
               pr_warn("Bad block at 0x%llx, skipping\n", block_start);
               to = block_start + mtd->erasesize;
               continue;
           }
           
           size_t write_len = min_t(size_t, len,
                                    mtd->erasesize - (to - block_start));
           
           ret = mtd_write(mtd, to, write_len, &retlen, buf);
           if (ret)
               return ret;
           
           buf += retlen;
           to += retlen;
           len -= retlen;
       }
       
       return 0;
   }

Flash Filesystems
=================

JFFS2
-----

.. code-block:: bash

   # Create JFFS2 image
   mkfs.jffs2 -r rootfs/ -o rootfs.jffs2 -e 0x10000 -n
   
   # Flash and mount
   flash_erase /dev/mtd2 0 0
   nandwrite -p /dev/mtd2 rootfs.jffs2
   mount -t jffs2 /dev/mtdblock2 /mnt

UBI/UBIFS
---------

.. code-block:: bash

   # Format MTD for UBI
   ubiformat /dev/mtd2
   
   # Attach UBI device
   ubiattach -m 2 -d 0
   
   # Create UBI volume
   ubimkvol /dev/ubi0 -N rootfs -s 100MiB
   
   # Create UBIFS image
   mkfs.ubifs -r rootfs/ -m 2048 -e 126976 -c 1000 -o rootfs.ubifs
   
   # Write UBIFS
   ubiupdatevol /dev/ubi0_0 rootfs.ubifs
   
   # Mount UBIFS
   mount -t ubifs ubi0:rootfs /mnt
   
   # UBI in fstab
   # /dev/ubi0_0    /mnt    ubifs    defaults    0    0

MTD Utilities
=============

Common Tools
------------

.. code-block:: bash

   # Device information
   mtdinfo -a
   mtdinfo /dev/mtd0
   
   # Erase
   flash_erase /dev/mtd0 0 0
   flash_erase -j /dev/mtd0 0 0  # With JFFS2 cleanmarkers
   
   # Read/Write
   nanddump /dev/mtd0 -f backup.bin
   nandwrite -p /dev/mtd0 image.bin
   
   # Copy
   nandwrite -m -n -p /dev/mtd0 /dev/mtd1
   
   # Test
   flash_torture /dev/mtd0
   nandtest /dev/mtd0

Debugging
=========

MTD Debugging
-------------

.. code-block:: bash

   # Enable MTD debugging
   echo 8 > /proc/sys/kernel/printk
   
   # MTD debug messages
   echo -n 'module mtd =p' > /sys/kernel/debug/dynamic_debug/control
   echo -n 'module mtdblock =p' > /sys/kernel/debug/dynamic_debug/control
   
   # Check MTD devices
   cat /proc/mtd
   
   # MTD stats
   cat /sys/class/mtd/mtd0/ecc_failures
   cat /sys/class/mtd/mtd0/corrected_bits
   cat /sys/class/mtd/mtd0/bad_blocks

Best Practices
==============

1. **Always erase before write** (flash requirement)
2. **Implement ECC** for NAND flash
3. **Handle bad blocks** properly
4. **Use wear leveling** (UBI)
5. **Align to erase blocks**
6. **Validate writes** after programming
7. **Use write protection** for critical partitions
8. **Implement power-fail safety** (atomic operations)
9. **Monitor ECC errors** (increasing errors indicate wear)
10. **Use UBI/UBIFS** for NAND (better than raw MTD)

Common Pitfalls
===============

1. **Writing without erasing** first
2. **Ignoring bad blocks** in NAND
3. **Not implementing ECC** for NAND
4. **Misaligned writes** (not aligned to write size)
5. **Power loss during write** (no atomic operations)
6. **Wear-out** (excessive writes to same blocks)
7. **Wrong partition sizes** (not aligned to erase blocks)

Quick Reference
===============

.. code-block:: c

   // MTD operations
   mtd_read(mtd, from, len, &retlen, buf);
   mtd_write(mtd, to, len, &retlen, buf);
   mtd_erase(mtd, &instr);
   mtd_block_isbad(mtd, ofs);
   mtd_block_markbad(mtd, ofs);
   
   // Registration
   mtd_device_register(&mtd, partitions, nr_parts);
   mtd_device_unregister(&mtd);
   
   // UBI
   ubi_open_volume(ubi_num, vol_id, mode);
   ubi_leb_read(desc, lnum, buf, offset, len, check);
   ubi_leb_write(desc, lnum, buf, offset, len);
   ubi_close_volume(desc);

See Also
========

- Linux_SPI_Drivers.rst
- Linux_Platform_Drivers.rst
- Linux_DMA.rst

References
==========

- MTD Documentation: https://www.kernel.org/doc/html/latest/driver-api/mtd/
- UBI Documentation: http://www.linux-mtd.infradead.org/doc/ubi.html
- drivers/mtd/ in Linux kernel source
