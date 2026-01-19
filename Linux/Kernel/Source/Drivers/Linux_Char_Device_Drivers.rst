========================================
Linux Character Device Drivers Guide
========================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Char Device Setup
-----------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   
   static dev_t dev_num;
   static struct cdev my_cdev;
   
   static int my_open(struct inode *inode, struct file *filp) {
       return 0;
   }
   
   static int my_release(struct inode *inode, struct file *filp) {
       return 0;
   }
   
   static ssize_t my_read(struct file *filp, char __user *buf,
                           size_t count, loff_t *f_pos) {
       return 0;
   }
   
   static ssize_t my_write(struct file *filp, const char __user *buf,
                            size_t count, loff_t *f_pos) {
       return count;
   }
   
   static const struct file_operations my_fops = {
       .owner = THIS_MODULE,
       .open = my_open,
       .release = my_release,
       .read = my_read,
       .write = my_write,
   };
   
   static int __init my_init(void) {
       int ret;
       
       /* Allocate device number */
       ret = alloc_chrdev_region(&dev_num, 0, 1, "mydev");
       if (ret < 0)
           return ret;
       
       /* Initialize cdev */
       cdev_init(&my_cdev, &my_fops);
       my_cdev.owner = THIS_MODULE;
       
       /* Add cdev to kernel */
       ret = cdev_add(&my_cdev, dev_num, 1);
       if (ret < 0) {
           unregister_chrdev_region(dev_num, 1);
           return ret;
       }
       
       pr_info("Device registered: major=%d, minor=%d\n",
               MAJOR(dev_num), MINOR(dev_num));
       
       return 0;
   }
   
   static void __exit my_exit(void) {
       cdev_del(&my_cdev);
       unregister_chrdev_region(dev_num, 1);
   }
   
   module_init(my_init);
   module_exit(my_exit);
   MODULE_LICENSE("GPL");

Quick Device Number Operations
-------------------------------

.. code-block:: c

   /* Allocate dynamically */
   alloc_chrdev_region(&dev, 0, count, "name");
   
   /* Register specific major */
   register_chrdev_region(MKDEV(major, minor), count, "name");
   
   /* Unregister */
   unregister_chrdev_region(dev, count);
   
   /* Extract major/minor */
   int major = MAJOR(dev);
   int minor = MINOR(dev);
   
   /* Create dev_t */
   dev_t dev = MKDEV(major, minor);

Character Device Fundamentals
==============================

Introduction
------------

Character devices are accessed as a stream of bytes (like a file). They are one of three device types in Linux (char, block, network).

**Examples:**
- Serial ports (/dev/ttyS0)
- Pseudo-terminals (/dev/pts/*)
- Null device (/dev/null)
- Random number generators (/dev/random, /dev/urandom)

**Key Concepts:**

- **Major number:** Identifies the driver
- **Minor number:** Identifies specific device
- **cdev structure:** Represents char device in kernel
- **file_operations:** Defines device operations
- **Device file:** User-space entry point (/dev/*)

Device Numbers
==============

Understanding dev_t
-------------------

.. code-block:: c

   /* dev_t is 32-bit: 12 bits major, 20 bits minor */
   typedef u32 dev_t;
   
   #define MINORBITS 20
   #define MINORMASK ((1U << MINORBITS) - 1)
   
   #define MAJOR(dev) ((unsigned int) ((dev) >> MINORBITS))
   #define MINOR(dev) ((unsigned int) ((dev) & MINORMASK))
   #define MKDEV(ma,mi) (((ma) << MINORBITS) | (mi))

Allocating Device Numbers
--------------------------

Dynamic Allocation
~~~~~~~~~~~~~~~~~~

.. code-block:: c

   static dev_t dev_num;
   static int num_devices = 1;
   
   static int __init driver_init(void) {
       int ret;
       
       /* Allocate major number dynamically */
       ret = alloc_chrdev_region(&dev_num, 0, num_devices, "mydriver");
       if (ret < 0) {
           pr_err("Failed to allocate device number\n");
           return ret;
       }
       
       pr_info("Allocated device number: major=%d, minor=%d\n",
               MAJOR(dev_num), MINOR(dev_num));
       
       return 0;
   }

Static Allocation
~~~~~~~~~~~~~~~~~

.. code-block:: c

   #define MY_MAJOR 250
   #define MY_MINOR 0
   
   static int __init driver_init(void) {
       dev_t dev = MKDEV(MY_MAJOR, MY_MINOR);
       int ret;
       
       ret = register_chrdev_region(dev, 1, "mydriver");
       if (ret < 0) {
           pr_err("Failed to register device number %d:%d\n",
                  MY_MAJOR, MY_MINOR);
           return ret;
       }
       
       return 0;
   }

Multiple Devices
~~~~~~~~~~~~~~~~

.. code-block:: c

   #define NUM_DEVICES 4
   static dev_t first_dev;
   
   static int __init driver_init(void) {
       /* Allocate range of device numbers */
       return alloc_chrdev_region(&first_dev, 0, NUM_DEVICES, "mydriver");
   }
   
   static void get_device_number(int index, dev_t *dev) {
       *dev = MKDEV(MAJOR(first_dev), MINOR(first_dev) + index);
   }

Character Device Structure
==========================

struct cdev
-----------

.. code-block:: c

   struct cdev {
       struct kobject kobj;
       struct module *owner;
       const struct file_operations *ops;
       struct list_head list;
       dev_t dev;
       unsigned int count;
   };

Initialization and Registration
--------------------------------

.. code-block:: c

   static struct cdev my_cdev;
   static dev_t dev_num;
   
   static int register_device(void) {
       int ret;
       
       /* 1. Allocate device number */
       ret = alloc_chrdev_region(&dev_num, 0, 1, "mydev");
       if (ret < 0)
           return ret;
       
       /* 2. Initialize cdev structure */
       cdev_init(&my_cdev, &my_fops);
       my_cdev.owner = THIS_MODULE;
       
       /* 3. Add device to kernel */
       ret = cdev_add(&my_cdev, dev_num, 1);
       if (ret < 0) {
           unregister_chrdev_region(dev_num, 1);
           return ret;
       }
       
       return 0;
   }
   
   static void unregister_device(void) {
       cdev_del(&my_cdev);
       unregister_chrdev_region(dev_num, 1);
   }

File Operations
===============

struct file_operations
----------------------

.. code-block:: c

   struct file_operations {
       struct module *owner;
       loff_t (*llseek) (struct file *, loff_t, int);
       ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
       ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
       __poll_t (*poll) (struct file *, struct poll_table_struct *);
       long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
       int (*mmap) (struct file *, struct vm_area_struct *);
       int (*open) (struct inode *, struct file *);
       int (*flush) (struct file *, fl_owner_t id);
       int (*release) (struct inode *, struct file *);
       int (*fsync) (struct file *, loff_t, loff_t, int datasync);
       /* ... many more ... */
   };

Open and Release
----------------

.. code-block:: c

   struct my_device {
       struct cdev cdev;
       struct mutex lock;
       int open_count;
       void *private_data;
   };
   
   static int my_open(struct inode *inode, struct file *filp) {
       struct my_device *dev;
       
       /* Get device structure from inode */
       dev = container_of(inode->i_cdev, struct my_device, cdev);
       
       /* Store in file's private_data for later use */
       filp->private_data = dev;
       
       mutex_lock(&dev->lock);
       dev->open_count++;
       pr_info("Device opened (%d times)\n", dev->open_count);
       mutex_unlock(&dev->lock);
       
       return 0;
   }
   
   static int my_release(struct inode *inode, struct file *filp) {
       struct my_device *dev = filp->private_data;
       
       mutex_lock(&dev->lock);
       dev->open_count--;
       pr_info("Device closed (%d open)\n", dev->open_count);
       mutex_unlock(&dev->lock);
       
       return 0;
   }

Read and Write Operations
--------------------------

Basic Read
~~~~~~~~~~

.. code-block:: c

   #define BUFFER_SIZE 1024
   
   struct my_device {
       char buffer[BUFFER_SIZE];
       size_t buffer_len;
       struct mutex lock;
   };
   
   static ssize_t my_read(struct file *filp, char __user *buf,
                          size_t count, loff_t *f_pos) {
       struct my_device *dev = filp->private_data;
       size_t to_copy;
       int ret;
       
       mutex_lock(&dev->lock);
       
       /* Check if past end */
       if (*f_pos >= dev->buffer_len) {
           mutex_unlock(&dev->lock);
           return 0;  /* EOF */
       }
       
       /* Calculate bytes to copy */
       to_copy = min(count, dev->buffer_len - (size_t)*f_pos);
       
       /* Copy to user space */
       ret = copy_to_user(buf, dev->buffer + *f_pos, to_copy);
       if (ret) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       /* Update file position */
       *f_pos += to_copy;
       
       mutex_unlock(&dev->lock);
       
       return to_copy;
   }

Basic Write
~~~~~~~~~~~

.. code-block:: c

   static ssize_t my_write(struct file *filp, const char __user *buf,
                           size_t count, loff_t *f_pos) {
       struct my_device *dev = filp->private_data;
       size_t to_write;
       int ret;
       
       mutex_lock(&dev->lock);
       
       /* Check buffer space */
       if (*f_pos >= BUFFER_SIZE) {
           mutex_unlock(&dev->lock);
           return -ENOSPC;
       }
       
       to_write = min(count, BUFFER_SIZE - (size_t)*f_pos);
       
       /* Copy from user space */
       ret = copy_from_user(dev->buffer + *f_pos, buf, to_write);
       if (ret) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       *f_pos += to_write;
       dev->buffer_len = max(dev->buffer_len, (size_t)*f_pos);
       
       mutex_unlock(&dev->lock);
       
       return to_write;
   }

IOCTL Operations
================

Modern IOCTL
------------

.. code-block:: c

   #include <linux/ioctl.h>
   
   /* Define IOCTL commands */
   #define MY_IOC_MAGIC 'k'
   #define MY_IOCRESET    _IO(MY_IOC_MAGIC, 0)
   #define MY_IOCSVAL     _IOW(MY_IOC_MAGIC, 1, int)
   #define MY_IOCGVAL     _IOR(MY_IOC_MAGIC, 2, int)
   #define MY_IOCXVAL     _IOWR(MY_IOC_MAGIC, 3, int)
   
   static long my_ioctl(struct file *filp, unsigned int cmd,
                        unsigned long arg) {
       struct my_device *dev = filp->private_data;
       int val;
       int ret = 0;
       
       /* Verify command magic */
       if (_IOC_TYPE(cmd) != MY_IOC_MAGIC)
           return -ENOTTY;
       
       switch (cmd) {
       case MY_IOCRESET:
           mutex_lock(&dev->lock);
           dev->value = 0;
           mutex_unlock(&dev->lock);
           break;
           
       case MY_IOCSVAL:  /* Set value */
           if (copy_from_user(&val, (int __user *)arg, sizeof(val)))
               return -EFAULT;
           
           mutex_lock(&dev->lock);
           dev->value = val;
           mutex_unlock(&dev->lock);
           break;
           
       case MY_IOCGVAL:  /* Get value */
           mutex_lock(&dev->lock);
           val = dev->value;
           mutex_unlock(&dev->lock);
           
           if (copy_to_user((int __user *)arg, &val, sizeof(val)))
               return -EFAULT;
           break;
           
       case MY_IOCXVAL:  /* Exchange value */
           if (copy_from_user(&val, (int __user *)arg, sizeof(val)))
               return -EFAULT;
           
           mutex_lock(&dev->lock);
           ret = dev->value;
           dev->value = val;
           mutex_unlock(&dev->lock);
           
           if (copy_to_user((int __user *)arg, &ret, sizeof(ret)))
               return -EFAULT;
           break;
           
       default:
           return -ENOTTY;
       }
       
       return 0;
   }

Poll/Select Support
===================

.. code-block:: c

   #include <linux/poll.h>
   
   static __poll_t my_poll(struct file *filp,
                           struct poll_table_struct *wait) {
       struct my_device *dev = filp->private_data;
       __poll_t mask = 0;
       
       /* Add wait queues */
       poll_wait(filp, &dev->read_queue, wait);
       poll_wait(filp, &dev->write_queue, wait);
       
       mutex_lock(&dev->lock);
       
       /* Check if readable */
       if (dev->read_available)
           mask |= POLLIN | POLLRDNORM;
       
       /* Check if writable */
       if (dev->write_available)
           mask |= POLLOUT | POLLWRNORM;
       
       /* Check for errors */
       if (dev->error)
           mask |= POLLERR;
       
       mutex_unlock(&dev->lock);
       
       return mask;
   }

Complete Example Driver
========================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/kernel.h>
   #include <linux/init.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/device.h>
   #include <linux/mutex.h>
   #include <linux/slab.h>
   #include <linux/uaccess.h>
   
   #define DEVICE_NAME "example"
   #define CLASS_NAME "example_class"
   #define BUFFER_SIZE 4096
   
   struct example_device {
       struct cdev cdev;
       struct device *device;
       struct mutex lock;
       char *buffer;
       size_t buffer_size;
       size_t data_len;
       int open_count;
   };
   
   static struct class *example_class;
   static dev_t dev_num;
   static struct example_device *example_dev;
   
   static int example_open(struct inode *inode, struct file *filp) {
       struct example_device *dev;
       
       dev = container_of(inode->i_cdev, struct example_device, cdev);
       filp->private_data = dev;
       
       mutex_lock(&dev->lock);
       dev->open_count++;
       pr_info("%s: Device opened (%d times)\n", DEVICE_NAME,
               dev->open_count);
       mutex_unlock(&dev->lock);
       
       return 0;
   }
   
   static int example_release(struct inode *inode, struct file *filp) {
       struct example_device *dev = filp->private_data;
       
       mutex_lock(&dev->lock);
       dev->open_count--;
       pr_info("%s: Device closed\n", DEVICE_NAME);
       mutex_unlock(&dev->lock);
       
       return 0;
   }
   
   static ssize_t example_read(struct file *filp, char __user *buf,
                                size_t count, loff_t *f_pos) {
       struct example_device *dev = filp->private_data;
       size_t to_copy;
       int ret;
       
       mutex_lock(&dev->lock);
       
       if (*f_pos >= dev->data_len) {
           mutex_unlock(&dev->lock);
           return 0;
       }
       
       to_copy = min(count, dev->data_len - (size_t)*f_pos);
       
       ret = copy_to_user(buf, dev->buffer + *f_pos, to_copy);
       if (ret) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       *f_pos += to_copy;
       mutex_unlock(&dev->lock);
       
       return to_copy;
   }
   
   static ssize_t example_write(struct file *filp,
                                 const char __user *buf,
                                 size_t count, loff_t *f_pos) {
       struct example_device *dev = filp->private_data;
       size_t to_write;
       int ret;
       
       mutex_lock(&dev->lock);
       
       if (*f_pos >= dev->buffer_size) {
           mutex_unlock(&dev->lock);
           return -ENOSPC;
       }
       
       to_write = min(count, dev->buffer_size - (size_t)*f_pos);
       
       ret = copy_from_user(dev->buffer + *f_pos, buf, to_write);
       if (ret) {
           mutex_unlock(&dev->lock);
           return -EFAULT;
       }
       
       *f_pos += to_write;
       if (*f_pos > dev->data_len)
           dev->data_len = *f_pos;
       
       mutex_unlock(&dev->lock);
       
       return to_write;
   }
   
   static loff_t example_llseek(struct file *filp, loff_t offset,
                                 int whence) {
       struct example_device *dev = filp->private_data;
       loff_t new_pos;
       
       mutex_lock(&dev->lock);
       
       switch (whence) {
       case SEEK_SET:
           new_pos = offset;
           break;
       case SEEK_CUR:
           new_pos = filp->f_pos + offset;
           break;
       case SEEK_END:
           new_pos = dev->data_len + offset;
           break;
       default:
           mutex_unlock(&dev->lock);
           return -EINVAL;
       }
       
       if (new_pos < 0 || new_pos > dev->buffer_size) {
           mutex_unlock(&dev->lock);
           return -EINVAL;
       }
       
       filp->f_pos = new_pos;
       mutex_unlock(&dev->lock);
       
       return new_pos;
   }
   
   static const struct file_operations example_fops = {
       .owner = THIS_MODULE,
       .open = example_open,
       .release = example_release,
       .read = example_read,
       .write = example_write,
       .llseek = example_llseek,
   };
   
   static int __init example_init(void) {
       int ret;
       
       /* Allocate device number */
       ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
       if (ret < 0) {
           pr_err("Failed to allocate device number\n");
           return ret;
       }
       
       /* Create device class */
       example_class = class_create(THIS_MODULE, CLASS_NAME);
       if (IS_ERR(example_class)) {
           unregister_chrdev_region(dev_num, 1);
           return PTR_ERR(example_class);
       }
       
       /* Allocate device structure */
       example_dev = kzalloc(sizeof(*example_dev), GFP_KERNEL);
       if (!example_dev) {
           class_destroy(example_class);
           unregister_chrdev_region(dev_num, 1);
           return -ENOMEM;
       }
       
       /* Initialize device */
       mutex_init(&example_dev->lock);
       example_dev->buffer_size = BUFFER_SIZE;
       example_dev->buffer = kzalloc(BUFFER_SIZE, GFP_KERNEL);
       if (!example_dev->buffer) {
           kfree(example_dev);
           class_destroy(example_class);
           unregister_chrdev_region(dev_num, 1);
           return -ENOMEM;
       }
       
       /* Initialize cdev */
       cdev_init(&example_dev->cdev, &example_fops);
       example_dev->cdev.owner = THIS_MODULE;
       
       /* Add cdev */
       ret = cdev_add(&example_dev->cdev, dev_num, 1);
       if (ret < 0) {
           kfree(example_dev->buffer);
           kfree(example_dev);
           class_destroy(example_class);
           unregister_chrdev_region(dev_num, 1);
           return ret;
       }
       
       /* Create device node */
       example_dev->device = device_create(example_class, NULL,
                                            dev_num, NULL, DEVICE_NAME);
       if (IS_ERR(example_dev->device)) {
           cdev_del(&example_dev->cdev);
           kfree(example_dev->buffer);
           kfree(example_dev);
           class_destroy(example_class);
           unregister_chrdev_region(dev_num, 1);
           return PTR_ERR(example_dev->device);
       }
       
       pr_info("%s: Char device initialized (major=%d, minor=%d)\n",
               DEVICE_NAME, MAJOR(dev_num), MINOR(dev_num));
       
       return 0;
   }
   
   static void __exit example_exit(void) {
       device_destroy(example_class, dev_num);
       cdev_del(&example_dev->cdev);
       kfree(example_dev->buffer);
       kfree(example_dev);
       class_destroy(example_class);
       unregister_chrdev_region(dev_num, 1);
       
       pr_info("%s: Char device removed\n", DEVICE_NAME);
   }
   
   module_init(example_init);
   module_exit(example_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Kernel Developer");
   MODULE_DESCRIPTION("Example Character Device Driver");
   MODULE_VERSION("1.0");

Device Class and sysfs
======================

Creating Device Class
---------------------

.. code-block:: c

   static struct class *my_class;
   
   my_class = class_create(THIS_MODULE, "myclass");
   if (IS_ERR(my_class))
       return PTR_ERR(my_class);

Creating Device Node
--------------------

.. code-block:: c

   struct device *dev;
   
   /* device_create automatically creates /dev/ entry */
   dev = device_create(my_class, NULL, dev_num, NULL, "mydev%d", minor);
   if (IS_ERR(dev))
       return PTR_ERR(dev);

sysfs Attributes
----------------

.. code-block:: c

   static ssize_t value_show(struct device *dev,
                             struct device_attribute *attr,
                             char *buf) {
       struct example_device *edev = dev_get_drvdata(dev);
       return sprintf(buf, "%d\n", edev->value);
   }
   
   static ssize_t value_store(struct device *dev,
                              struct device_attribute *attr,
                              const char *buf, size_t count) {
       struct example_device *edev = dev_get_drvdata(dev);
       int ret;
       
       ret = kstrtoint(buf, 10, &edev->value);
       if (ret)
           return ret;
       
       return count;
   }
   
   static DEVICE_ATTR_RW(value);
   
   /* Create attribute */
   device_create_file(dev, &dev_attr_value);
   
   /* Remove attribute */
   device_remove_file(dev, &dev_attr_value);

Memory Mapping (mmap)
=====================

.. code-block:: c

   static int my_mmap(struct file *filp, struct vm_area_struct *vma) {
       struct my_device *dev = filp->private_data;
       unsigned long size = vma->vm_end - vma->vm_start;
       unsigned long pfn;
       
       if (size > dev->mem_size)
           return -EINVAL;
       
       pfn = virt_to_phys(dev->mem_buffer) >> PAGE_SHIFT;
       
       if (remap_pfn_range(vma, vma->vm_start, pfn, size,
                           vma->vm_page_prot))
           return -EAGAIN;
       
       return 0;
   }

Best Practices
==============

1. **Always check copy_to_user/copy_from_user return values**
2. **Use mutex for device synchronization**
3. **Implement proper error handling**
4. **Clean up resources in reverse order**
5. **Use devm_* functions when possible**
6. **Validate user input in ioctl**
7. **Support standard file operations (lseek, etc.)**
8. **Create device nodes with device_create**
9. **Add sysfs attributes for runtime configuration**
10. **Test with multiple concurrent opens**

Common Pitfalls
===============

1. **Forgetting to update file position**
2. **Not handling partial reads/writes**
3. **Memory leaks in error paths**
4. **Race conditions in open/release**
5. **Buffer overflows from user space**
6. **Not validating ioctl commands**

Debugging
=========

.. code-block:: bash

   # Check device numbers
   cat /proc/devices
   
   # List character devices
   ls -l /dev/mydev
   
   # Enable dynamic debug
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Check kernel logs
   dmesg | tail -50

Testing
=======

.. code-block:: bash

   # Create device node manually
   sudo mknod /dev/mydev c 250 0
   sudo chmod 666 /dev/mydev
   
   # Test read/write
   echo "Hello" > /dev/mydev
   cat /dev/mydev
   
   # Test with dd
   dd if=/dev/zero of=/dev/mydev bs=1024 count=1
   dd if=/dev/mydev of=/dev/null bs=1024 count=1

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Device_Tree_Drivers.rst
- LinuxDeviceDriver.rst
- Linux_Kernel_Synchronization.rst

References
==========

- Documentation/driver-api/
- include/linux/cdev.h
- include/linux/fs.h
- drivers/char/
