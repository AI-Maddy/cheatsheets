============================
Linux Block Drivers Guide
============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Block Device
------------------

.. code-block:: c

   #include <linux/blkdev.h>
   #include <linux/blk-mq.h>
   
   static blk_status_t myblk_queue_rq(struct blk_mq_hw_ctx *hctx,
                                       const struct blk_mq_queue_data *bd) {
       struct request *rq = bd->rq;
       struct myblk_dev *dev = hctx->queue->queuedata;
       
       blk_mq_start_request(rq);
       
       /* Process request */
       if (rq_data_dir(rq) == WRITE)
           myblk_do_write(dev, rq);
       else
           myblk_do_read(dev, rq);
       
       blk_mq_end_request(rq, BLK_STS_OK);
       return BLK_STS_OK;
   }
   
   static const struct blk_mq_ops myblk_mq_ops = {
       .queue_rq = myblk_queue_rq,
   };
   
   /* Setup and register */
   struct gendisk *disk;
   struct blk_mq_tag_set tag_set;
   
   tag_set.ops = &myblk_mq_ops;
   tag_set.nr_hw_queues = 1;
   tag_set.queue_depth = 128;
   tag_set.numa_node = NUMA_NO_NODE;
   tag_set.flags = BLK_MQ_F_SHOULD_MERGE;
   
   blk_mq_alloc_tag_set(&tag_set);
   
   disk = blk_mq_alloc_disk(&tag_set, dev);
   disk->major = major;
   disk->first_minor = 0;
   disk->minors = 1;
   set_capacity(disk, sectors);
   
   add_disk(disk);

Request Processing
------------------

.. code-block:: c

   static void myblk_do_request(struct myblk_dev *dev, struct request *rq) {
       struct bio_vec bvec;
       struct req_iterator iter;
       sector_t sector = blk_rq_pos(rq);
       
       rq_for_each_segment(bvec, rq, iter) {
           void *buffer = kmap_atomic(bvec.bv_page);
           unsigned int len = bvec.bv_len;
           unsigned int offset = bvec.bv_offset;
           
           if (rq_data_dir(rq) == WRITE)
               myblk_write_sector(dev, sector, buffer + offset, len);
           else
               myblk_read_sector(dev, sector, buffer + offset, len);
           
           kunmap_atomic(buffer);
           sector += len >> 9;  // Convert bytes to sectors
       }
   }

Block Device Basics
===================

Block Layer Architecture
------------------------

.. code-block:: text

   Application
       |
   VFS (Virtual File System)
       |
   Page Cache
       |
   Block Layer (Generic Block Layer)
       |
   Multi-Queue Block Layer (blk-mq)
       |
   Block Driver (Your Code)
       |
   Hardware

Key Structures
--------------

.. code-block:: c

   struct gendisk       // Represents a disk
   struct request_queue // Request queue
   struct request       // I/O request
   struct bio           // Basic I/O unit
   struct bio_vec       // Segment of bio

Block Multi-Queue (blk-mq)
==========================

Modern API
----------

The blk-mq API replaced the old request API and provides better performance on multi-core systems.

Tag Set Setup
-------------

.. code-block:: c

   #include <linux/blk-mq.h>
   
   struct myblk_dev {
       struct gendisk *disk;
       struct blk_mq_tag_set tag_set;
       void *buffer;  // Storage backend
       size_t capacity;
       spinlock_t lock;
   };
   
   static blk_status_t myblk_queue_rq(struct blk_mq_hw_ctx *hctx,
                                       const struct blk_mq_queue_data *bd) {
       struct request *rq = bd->rq;
       struct myblk_dev *dev = hctx->queue->queuedata;
       unsigned long flags;
       
       spin_lock_irqsave(&dev->lock, flags);
       blk_mq_start_request(rq);
       spin_unlock_irqrestore(&dev->lock, flags);
       
       /* Process request */
       myblk_handle_request(dev, rq);
       
       /* Complete request */
       blk_mq_end_request(rq, BLK_STS_OK);
       
       return BLK_STS_OK;
   }
   
   static const struct blk_mq_ops myblk_mq_ops = {
       .queue_rq = myblk_queue_rq,
   };
   
   static int myblk_setup_queue(struct myblk_dev *dev) {
       int ret;
       
       /* Setup tag set */
       memset(&dev->tag_set, 0, sizeof(dev->tag_set));
       dev->tag_set.ops = &myblk_mq_ops;
       dev->tag_set.nr_hw_queues = 1;
       dev->tag_set.queue_depth = 128;
       dev->tag_set.numa_node = NUMA_NO_NODE;
       dev->tag_set.cmd_size = 0;
       dev->tag_set.flags = BLK_MQ_F_SHOULD_MERGE | BLK_MQ_F_BLOCKING;
       dev->tag_set.driver_data = dev;
       
       ret = blk_mq_alloc_tag_set(&dev->tag_set);
       if (ret)
           return ret;
       
       /* Allocate disk */
       dev->disk = blk_mq_alloc_disk(&dev->tag_set, dev);
       if (IS_ERR(dev->disk)) {
           blk_mq_free_tag_set(&dev->tag_set);
           return PTR_ERR(dev->disk);
       }
       
       dev->disk->queue->queuedata = dev;
       
       return 0;
   }

Request Processing
==================

Handling Requests
-----------------

.. code-block:: c

   static void myblk_handle_request(struct myblk_dev *dev,
                                     struct request *rq) {
       struct bio_vec bvec;
       struct req_iterator iter;
       sector_t sector;
       void *buffer;
       unsigned int len, offset;
       
       sector = blk_rq_pos(rq);  // Starting sector
       
       /* Iterate through request segments */
       rq_for_each_segment(bvec, rq, iter) {
           buffer = kmap_atomic(bvec.bv_page);
           len = bvec.bv_len;
           offset = bvec.bv_offset;
           
           if (rq_data_dir(rq) == WRITE) {
               /* Write to device */
               memcpy(dev->buffer + (sector << 9),
                       buffer + offset, len);
           } else {
               /* Read from device */
               memcpy(buffer + offset,
                       dev->buffer + (sector << 9), len);
           }
           
           kunmap_atomic(buffer);
           
           sector += len >> 9;  // Advance by sectors (512 bytes)
       }
   }

DMA Requests
------------

.. code-block:: c

   static void myblk_dma_request(struct myblk_dev *dev,
                                  struct request *rq) {
       struct bio_vec bvec;
       struct req_iterator iter;
       sector_t sector = blk_rq_pos(rq);
       
       rq_for_each_segment(bvec, rq, iter) {
           dma_addr_t dma_addr;
           
           dma_addr = dma_map_page(dev->dev, bvec.bv_page,
                                    bvec.bv_offset, bvec.bv_len,
                                    rq_data_dir(rq) == READ ?
                                    DMA_FROM_DEVICE : DMA_TO_DEVICE);
           
           if (dma_mapping_error(dev->dev, dma_addr)) {
               dev_err(dev->dev, "DMA mapping failed\n");
               continue;
           }
           
           /* Program DMA transfer */
           myblk_dma_transfer(dev, sector, dma_addr, bvec.bv_len,
                               rq_data_dir(rq));
           
           /* Wait for DMA complete (or use interrupts) */
           myblk_wait_dma(dev);
           
           dma_unmap_page(dev->dev, dma_addr, bvec.bv_len,
                           rq_data_dir(rq) == READ ?
                           DMA_FROM_DEVICE : DMA_TO_DEVICE);
           
           sector += bvec.bv_len >> 9;
       }
   }

Gendisk Setup
=============

Disk Registration
-----------------

.. code-block:: c

   static int myblk_add_disk(struct myblk_dev *dev, int major,
                              sector_t capacity) {
       int ret;
       
       /* Allocate gendisk */
       dev->disk = blk_mq_alloc_disk(&dev->tag_set, dev);
       if (IS_ERR(dev->disk))
           return PTR_ERR(dev->disk);
       
       /* Setup disk parameters */
       dev->disk->major = major;
       dev->disk->first_minor = 0;
       dev->disk->minors = 1;
       dev->disk->fops = &myblk_fops;
       dev->disk->private_data = dev;
       snprintf(dev->disk->disk_name, DISK_NAME_LEN, "myblk%d", 0);
       
       /* Set capacity (in sectors) */
       set_capacity(dev->disk, capacity);
       
       /* Set queue limits */
       blk_queue_logical_block_size(dev->disk->queue, 512);
       blk_queue_physical_block_size(dev->disk->queue, 4096);
       blk_queue_max_hw_sectors(dev->disk->queue, 1024);
       
       /* Register disk */
       ret = add_disk(dev->disk);
       if (ret) {
           blk_cleanup_disk(dev->disk);
           return ret;
       }
       
       return 0;
   }

Block Device Operations
-----------------------

.. code-block:: c

   static int myblk_open(struct block_device *bdev, fmode_t mode) {
       struct myblk_dev *dev = bdev->bd_disk->private_data;
       
       /* Increment usage count */
       atomic_inc(&dev->open_count);
       
       return 0;
   }
   
   static void myblk_release(struct gendisk *disk, fmode_t mode) {
       struct myblk_dev *dev = disk->private_data;
       
       /* Decrement usage count */
       atomic_dec(&dev->open_count);
   }
   
   static int myblk_ioctl(struct block_device *bdev, fmode_t mode,
                           unsigned int cmd, unsigned long arg) {
       switch (cmd) {
       case BLKFLSBUF:
           /* Flush buffers */
           return 0;
       default:
           return -ENOTTY;
       }
   }
   
   static const struct block_device_operations myblk_fops = {
       .owner = THIS_MODULE,
       .open = myblk_open,
       .release = myblk_release,
       .ioctl = myblk_ioctl,
   };

Complete Driver Example
========================

RAM Block Device
----------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/blkdev.h>
   #include <linux/blk-mq.h>
   #include <linux/init.h>
   #include <linux/slab.h>
   #include <linux/vmalloc.h>
   
   #define MYBLK_SECTOR_SIZE 512
   #define MYBLK_NSECTORS    (1024 * 1024)  // 512 MB
   
   static int major;
   
   struct myblk_dev {
       struct gendisk *disk;
       struct blk_mq_tag_set tag_set;
       void *data;
       size_t size;
       spinlock_t lock;
   };
   
   static struct myblk_dev *myblk_device;
   
   static void myblk_transfer(struct myblk_dev *dev, sector_t sector,
                               unsigned long nsect, void *buffer, int write) {
       unsigned long offset = sector * MYBLK_SECTOR_SIZE;
       unsigned long nbytes = nsect * MYBLK_SECTOR_SIZE;
       
       if (offset + nbytes > dev->size) {
           pr_err("Beyond end of device (%ld %ld)\n", offset, nbytes);
           return;
       }
       
       if (write)
           memcpy(dev->data + offset, buffer, nbytes);
       else
           memcpy(buffer, dev->data + offset, nbytes);
   }
   
   static blk_status_t myblk_queue_rq(struct blk_mq_hw_ctx *hctx,
                                       const struct blk_mq_queue_data *bd) {
       struct request *rq = bd->rq;
       struct myblk_dev *dev = hctx->queue->queuedata;
       struct bio_vec bvec;
       struct req_iterator iter;
       sector_t sector;
       void *buffer;
       unsigned long flags;
       
       blk_mq_start_request(rq);
       
       spin_lock_irqsave(&dev->lock, flags);
       
       sector = blk_rq_pos(rq);
       
       rq_for_each_segment(bvec, rq, iter) {
           buffer = kmap_atomic(bvec.bv_page);
           
           myblk_transfer(dev, sector, bvec.bv_len >> 9,
                           buffer + bvec.bv_offset,
                           rq_data_dir(rq));
           
           kunmap_atomic(buffer);
           sector += bvec.bv_len >> 9;
       }
       
       spin_unlock_irqrestore(&dev->lock, flags);
       
       blk_mq_end_request(rq, BLK_STS_OK);
       
       return BLK_STS_OK;
   }
   
   static const struct blk_mq_ops myblk_mq_ops = {
       .queue_rq = myblk_queue_rq,
   };
   
   static int myblk_open(struct block_device *bdev, fmode_t mode) {
       return 0;
   }
   
   static void myblk_release(struct gendisk *disk, fmode_t mode) {
   }
   
   static const struct block_device_operations myblk_fops = {
       .owner = THIS_MODULE,
       .open = myblk_open,
       .release = myblk_release,
   };
   
   static int __init myblk_init(void) {
       struct myblk_dev *dev;
       int ret;
       
       /* Allocate device structure */
       dev = kzalloc(sizeof(struct myblk_dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       myblk_device = dev;
       
       /* Allocate storage */
       dev->size = MYBLK_NSECTORS * MYBLK_SECTOR_SIZE;
       dev->data = vmalloc(dev->size);
       if (!dev->data) {
           ret = -ENOMEM;
           goto out_free_dev;
       }
       
       spin_lock_init(&dev->lock);
       
       /* Register block device */
       major = register_blkdev(0, "myblk");
       if (major < 0) {
           ret = major;
           goto out_free_data;
       }
       
       /* Setup tag set */
       dev->tag_set.ops = &myblk_mq_ops;
       dev->tag_set.nr_hw_queues = 1;
       dev->tag_set.queue_depth = 128;
       dev->tag_set.numa_node = NUMA_NO_NODE;
       dev->tag_set.flags = BLK_MQ_F_SHOULD_MERGE;
       
       ret = blk_mq_alloc_tag_set(&dev->tag_set);
       if (ret)
           goto out_unreg_blkdev;
       
       /* Allocate disk */
       dev->disk = blk_mq_alloc_disk(&dev->tag_set, dev);
       if (IS_ERR(dev->disk)) {
           ret = PTR_ERR(dev->disk);
           goto out_free_tagset;
       }
       
       dev->disk->major = major;
       dev->disk->first_minor = 0;
       dev->disk->minors = 1;
       dev->disk->fops = &myblk_fops;
       dev->disk->private_data = dev;
       dev->disk->queue->queuedata = dev;
       snprintf(dev->disk->disk_name, DISK_NAME_LEN, "myblk");
       
       set_capacity(dev->disk, MYBLK_NSECTORS);
       
       /* Set queue limits */
       blk_queue_logical_block_size(dev->disk->queue, MYBLK_SECTOR_SIZE);
       blk_queue_physical_block_size(dev->disk->queue, MYBLK_SECTOR_SIZE);
       
       /* Add disk */
       ret = add_disk(dev->disk);
       if (ret)
           goto out_cleanup_disk;
       
       pr_info("myblk: RAM block device registered (%lu MB)\n",
               dev->size / (1024 * 1024));
       
       return 0;
       
   out_cleanup_disk:
       blk_cleanup_disk(dev->disk);
   out_free_tagset:
       blk_mq_free_tag_set(&dev->tag_set);
   out_unreg_blkdev:
       unregister_blkdev(major, "myblk");
   out_free_data:
       vfree(dev->data);
   out_free_dev:
       kfree(dev);
       return ret;
   }
   
   static void __exit myblk_exit(void) {
       struct myblk_dev *dev = myblk_device;
       
       del_gendisk(dev->disk);
       blk_cleanup_disk(dev->disk);
       blk_mq_free_tag_set(&dev->tag_set);
       unregister_blkdev(major, "myblk");
       vfree(dev->data);
       kfree(dev);
       
       pr_info("myblk: RAM block device unregistered\n");
   }
   
   module_init(myblk_init);
   module_exit(myblk_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Simple RAM Block Device");

Best Practices
==============

1. **Use blk-mq API** for modern kernels
2. **Handle DMA properly** for real hardware
3. **Set appropriate queue limits**
4. **Implement proper error handling**
5. **Use atomic operations** for statistics
6. **Support direct I/O** when applicable
7. **Implement discard/trim** if supported
8. **Test with fio benchmark**
9. **Use appropriate locking**
10. **Document capacity limits**

Common Pitfalls
===============

1. **Not handling partial requests**
2. **Incorrect sector calculations**
3. **Memory leaks** in error paths
4. **Wrong DMA directions**
5. **Not setting capacity**
6. **Missing blk_mq_start_request()**

Debugging
=========

.. code-block:: bash

   # Create filesystem
   mkfs.ext4 /dev/myblk
   
   # Mount device
   mount /dev/myblk /mnt
   
   # Test I/O
   dd if=/dev/zero of=/dev/myblk bs=1M count=100
   dd if=/dev/myblk of=/dev/null bs=1M count=100
   
   # Benchmark
   fio --name=test --rw=randread --bs=4k --size=100M --filename=/dev/myblk
   
   # View block stats
   cat /sys/block/myblk/stat
   iostat -x 1

See Also
========

- Linux_Platform_Drivers.rst
- Linux_DMA.rst
- Linux_Driver_IRQ_Handling.rst

References
==========

- Documentation/block/
- include/linux/blkdev.h
- include/linux/blk-mq.h
