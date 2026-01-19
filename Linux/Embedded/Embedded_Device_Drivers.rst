================================================================================
Embedded Linux: Device Drivers Development - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Essential Linux Device Drivers + Linux Embedded Development Module 3 Ch8
:Target: Linux Kernel 5.x/6.x Driver Development
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Character Device Driver Template:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/uaccess.h>
   
   static dev_t dev_num;
   static struct cdev my_cdev;
   static struct class *my_class;
   
   static int my_open(struct inode *inode, struct file *file) {
       pr_info("Device opened\n");
       return 0;
   }
   
   static ssize_t my_read(struct file *file, char __user *buf,
                          size_t len, loff_t *offset) {
       char data[] = "Hello from driver\n";
       if (copy_to_user(buf, data, sizeof(data)))
           return -EFAULT;
       return sizeof(data);
   }
   
   static struct file_operations fops = {
       .owner = THIS_MODULE,
       .open = my_open,
       .read = my_read,
   };
   
   static int __init my_init(void) {
       alloc_chrdev_region(&dev_num, 0, 1, "mydev");
       cdev_init(&my_cdev, &fops);
       cdev_add(&my_cdev, dev_num, 1);
       my_class = class_create(THIS_MODULE, "myclass");
       device_create(my_class, NULL, dev_num, NULL, "mydev");
       pr_info("Driver loaded\n");
       return 0;
   }
   
   static void __exit my_exit(void) {
       device_destroy(my_class, dev_num);
       class_destroy(my_class);
       cdev_del(&my_cdev);
       unregister_chrdev_region(dev_num, 1);
       pr_info("Driver unloaded\n");
   }
   
   module_init(my_init);
   module_exit(my_exit);
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Simple character device driver");

**Platform Driver Template:**

.. code-block:: c

   #include <linux/platform_device.h>
   #include <linux/mod_devicetable.h>
   #include <linux/of.h>
   
   static int my_probe(struct platform_device *pdev) {
       dev_info(&pdev->dev, "Device probed\n");
       // Initialize hardware
       return 0;
   }
   
   static int my_remove(struct platform_device *pdev) {
       dev_info(&pdev->dev, "Device removed\n");
       return 0;
   }
   
   static const struct of_device_id my_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_of_match);
   
   static struct platform_driver my_driver = {
       .probe = my_probe,
       .remove = my_remove,
       .driver = {
           .name = "mydriver",
           .of_match_table = my_of_match,
       },
   };
   module_platform_driver(my_driver);
   MODULE_LICENSE("GPL");

**I2C Driver Template:**

.. code-block:: c

   #include <linux/i2c.h>
   
   static int my_i2c_probe(struct i2c_client *client,
                           const struct i2c_device_id *id) {
       // Read from I2C device
       u8 data;
       i2c_smbus_read_byte_data(client, REG_ADDR);
       return 0;
   }
   
   static int my_i2c_remove(struct i2c_client *client) {
       return 0;
   }
   
   static const struct i2c_device_id my_i2c_id[] = {
       { "mydevice", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(i2c, my_i2c_id);
   
   static const struct of_device_id my_i2c_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_i2c_of_match);
   
   static struct i2c_driver my_i2c_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = my_i2c_of_match,
       },
       .probe = my_i2c_probe,
       .remove = my_i2c_remove,
       .id_table = my_i2c_id,
   };
   module_i2c_driver(my_i2c_driver);
   MODULE_LICENSE("GPL");

**Build Makefile:**

.. code-block:: make

   obj-m := mydriver.o
   
   KDIR := /lib/modules/$(shell uname -r)/build
   
   all:
   	make -C $(KDIR) M=$(PWD) modules
   
   clean:
   	make -C $(KDIR) M=$(PWD) clean
   
   install:
   	make -C $(KDIR) M=$(PWD) modules_install

================================================================================
1. Linux Driver Model Fundamentals
================================================================================

1.1 Driver Architecture
------------------------

**Linux Driver Categories:**

.. code-block:: text

   Character Drivers:
   - Serial devices, terminals
   - Input devices (mouse, keyboard, touchscreen)
   - Accessed via /dev/xxx
   - Stream of bytes (no buffering)
   
   Block Drivers:
   - Storage devices (hard drives, SD cards)
   - Block-based I/O with buffering
   - Accessed via /dev/sdX, /dev/mmcblkX
   
   Network Drivers:
   - Ethernet, WiFi, Bluetooth
   - Packet-based communication
   - Accessed via network interfaces (eth0, wlan0)
   
   Platform Drivers:
   - SoC peripherals (I2C, SPI, UART, GPIO)
   - Device tree binding
   - Memory-mapped I/O
   
   USB Drivers:
   - USB devices (storage, HID, serial)
   - Hot-pluggable
   
   PCI Drivers:
   - PCI/PCIe devices
   - Hot-pluggable

**Driver Subsystems:**

.. code-block:: text

   Driver Framework Layers:
   
   Application
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Kernel Space:
   
   VFS / System Call Interface
       ↓
   Device Class (tty, input, block, net)
       ↓
   Bus Driver (platform, i2c, spi, usb, pci)
       ↓
   Device Driver (your code)
       ↓
   Hardware

1.2 Module Basics
------------------

**Module Structure:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/kernel.h>
   #include <linux/init.h>
   
   static int __init my_driver_init(void) {
       printk(KERN_INFO "My driver: Initialized\n");
       return 0;  // 0 = success, negative = error
   }
   
   static void __exit my_driver_exit(void) {
       printk(KERN_INFO "My driver: Exiting\n");
   }
   
   module_init(my_driver_init);
   module_exit(my_driver_exit);
   
   MODULE_LICENSE("GPL");                    // Required
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("My driver description");
   MODULE_VERSION("1.0");

**Module Loading:**

.. code-block:: bash

   # Load module
   insmod mydriver.ko
   modprobe mydriver  # Handles dependencies
   
   # Unload module
   rmmod mydriver
   modprobe -r mydriver
   
   # Check loaded modules
   lsmod | grep mydriver
   
   # View module info
   modinfo mydriver.ko
   
   # Module parameters
   insmod mydriver.ko debug=1
   
   # Kernel log messages
   dmesg | tail
   journalctl -k | tail

**Module Parameters:**

.. code-block:: c

   #include <linux/moduleparam.h>
   
   static int debug = 0;
   module_param(debug, int, 0644);
   MODULE_PARM_DESC(debug, "Enable debug mode (default: 0)");
   
   static char *name = "default";
   module_param(name, charp, 0644);
   MODULE_PARM_DESC(name, "Device name");
   
   // Usage:
   if (debug)
       pr_debug("Debug message\n");
   
   // Load with parameters:
   // insmod mydriver.ko debug=1 name="mydevice"

================================================================================
2. Character Device Drivers
================================================================================

2.1 Character Device Registration
----------------------------------

**Device Number Allocation:**

.. code-block:: c

   #include <linux/fs.h>
   
   dev_t dev_num;  // Major and minor numbers
   
   // Static allocation (deprecated)
   int major = 240;
   dev_num = MKDEV(major, 0);
   register_chrdev_region(dev_num, 1, "mydev");
   
   // Dynamic allocation (recommended)
   alloc_chrdev_region(&dev_num, 0, 1, "mydev");
   
   // Get major/minor
   int major = MAJOR(dev_num);
   int minor = MINOR(dev_num);
   
   // Unregister
   unregister_chrdev_region(dev_num, 1);

**cdev Registration:**

.. code-block:: c

   #include <linux/cdev.h>
   
   struct cdev my_cdev;
   
   // Initialize cdev
   cdev_init(&my_cdev, &fops);
   my_cdev.owner = THIS_MODULE;
   
   // Add to kernel
   cdev_add(&my_cdev, dev_num, 1);
   
   // Remove
   cdev_del(&my_cdev);

**Device Class and Device Creation:**

.. code-block:: c

   struct class *my_class;
   struct device *my_device;
   
   // Create class (/sys/class/myclass)
   my_class = class_create(THIS_MODULE, "myclass");
   
   // Create device (/dev/mydev)
   my_device = device_create(my_class, NULL, dev_num, NULL, "mydev");
   
   // Cleanup
   device_destroy(my_class, dev_num);
   class_destroy(my_class);

2.2 File Operations
--------------------

**Complete file_operations:**

.. code-block:: c

   #include <linux/fs.h>
   #include <linux/uaccess.h>
   
   static int my_open(struct inode *inode, struct file *file) {
       pr_info("Device opened\n");
       // Get private data from cdev
       struct my_device *dev = container_of(inode->i_cdev, 
                                            struct my_device, cdev);
       file->private_data = dev;
       return 0;
   }
   
   static int my_release(struct inode *inode, struct file *file) {
       pr_info("Device closed\n");
       return 0;
   }
   
   static ssize_t my_read(struct file *file, char __user *buf,
                          size_t len, loff_t *offset) {
       struct my_device *dev = file->private_data;
       char data[256];
       ssize_t bytes_read;
       
       // Read from hardware
       bytes_read = snprintf(data, sizeof(data), "Status: OK\n");
       
       if (*offset >= bytes_read)
           return 0;  // EOF
       
       if (len > bytes_read - *offset)
           len = bytes_read - *offset;
       
       if (copy_to_user(buf, data + *offset, len))
           return -EFAULT;
       
       *offset += len;
       return len;
   }
   
   static ssize_t my_write(struct file *file, const char __user *buf,
                           size_t len, loff_t *offset) {
       char data[256];
       
       if (len > sizeof(data) - 1)
           len = sizeof(data) - 1;
       
       if (copy_from_user(data, buf, len))
           return -EFAULT;
       
       data[len] = '\0';
       pr_info("Received: %s\n", data);
       
       // Write to hardware
       
       return len;
   }
   
   static long my_ioctl(struct file *file, unsigned int cmd,
                        unsigned long arg) {
       struct my_device *dev = file->private_data;
       
       switch (cmd) {
       case MY_IOCTL_CMD1:
           // Handle command 1
           break;
       case MY_IOCTL_CMD2:
           // Handle command 2
           break;
       default:
           return -ENOTTY;
       }
       return 0;
   }
   
   static loff_t my_llseek(struct file *file, loff_t offset, int whence) {
       // Implement seek if needed
       return 0;
   }
   
   static unsigned int my_poll(struct file *file,
                               struct poll_table_struct *wait) {
       // Implement poll/select
       return 0;
   }
   
   static struct file_operations fops = {
       .owner = THIS_MODULE,
       .open = my_open,
       .release = my_release,
       .read = my_read,
       .write = my_write,
       .unlocked_ioctl = my_ioctl,
       .llseek = my_llseek,
       .poll = my_poll,
   };

**IOCTL Commands:**

.. code-block:: c

   #include <linux/ioctl.h>
   
   // Define IOCTL commands
   #define MY_IOCTL_MAGIC 'k'
   #define MY_IOCTL_RESET    _IO(MY_IOCTL_MAGIC, 0)
   #define MY_IOCTL_GET_VAL  _IOR(MY_IOCTL_MAGIC, 1, int)
   #define MY_IOCTL_SET_VAL  _IOW(MY_IOCTL_MAGIC, 2, int)
   
   // Userspace usage:
   // int fd = open("/dev/mydev", O_RDWR);
   // int val;
   // ioctl(fd, MY_IOCTL_GET_VAL, &val);
   // ioctl(fd, MY_IOCTL_SET_VAL, &val);

2.3 Complete Character Driver Example
--------------------------------------

**Full Driver Implementation:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/device.h>
   #include <linux/uaccess.h>
   #include <linux/slab.h>
   
   #define DEVICE_NAME "mydevice"
   #define CLASS_NAME "myclass"
   #define BUFFER_SIZE 1024
   
   struct my_device {
       struct cdev cdev;
       char *buffer;
       size_t buffer_size;
       struct mutex lock;
   };
   
   static dev_t dev_num;
   static struct class *my_class;
   static struct my_device *my_dev;
   
   static int my_open(struct inode *inode, struct file *file) {
       struct my_device *dev = container_of(inode->i_cdev,
                                            struct my_device, cdev);
       file->private_data = dev;
       pr_info("%s: Device opened\n", DEVICE_NAME);
       return 0;
   }
   
   static ssize_t my_read(struct file *file, char __user *buf,
                          size_t len, loff_t *offset) {
       struct my_device *dev = file->private_data;
       ssize_t bytes_read = 0;
       
       if (mutex_lock_interruptible(&dev->lock))
           return -ERESTARTSYS;
       
       if (*offset >= dev->buffer_size)
           goto out;
       
       if (*offset + len > dev->buffer_size)
           len = dev->buffer_size - *offset;
       
       if (copy_to_user(buf, dev->buffer + *offset, len)) {
           bytes_read = -EFAULT;
           goto out;
       }
       
       *offset += len;
       bytes_read = len;
       
   out:
       mutex_unlock(&dev->lock);
       return bytes_read;
   }
   
   static ssize_t my_write(struct file *file, const char __user *buf,
                           size_t len, loff_t *offset) {
       struct my_device *dev = file->private_data;
       ssize_t bytes_written = 0;
       
       if (mutex_lock_interruptible(&dev->lock))
           return -ERESTARTSYS;
       
       if (len > BUFFER_SIZE)
           len = BUFFER_SIZE;
       
       if (copy_from_user(dev->buffer, buf, len)) {
           bytes_written = -EFAULT;
           goto out;
       }
       
       dev->buffer_size = len;
       bytes_written = len;
       
   out:
       mutex_unlock(&dev->lock);
       return bytes_written;
   }
   
   static struct file_operations fops = {
       .owner = THIS_MODULE,
       .open = my_open,
       .read = my_read,
       .write = my_write,
   };
   
   static int __init my_driver_init(void) {
       int ret;
       
       // Allocate device structure
       my_dev = kzalloc(sizeof(struct my_device), GFP_KERNEL);
       if (!my_dev)
           return -ENOMEM;
       
       // Allocate buffer
       my_dev->buffer = kzalloc(BUFFER_SIZE, GFP_KERNEL);
       if (!my_dev->buffer) {
           kfree(my_dev);
           return -ENOMEM;
       }
       
       mutex_init(&my_dev->lock);
       
       // Allocate device number
       ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
       if (ret < 0)
           goto fail_alloc;
       
       // Initialize and add cdev
       cdev_init(&my_dev->cdev, &fops);
       my_dev->cdev.owner = THIS_MODULE;
       ret = cdev_add(&my_dev->cdev, dev_num, 1);
       if (ret < 0)
           goto fail_cdev;
       
       // Create class
       my_class = class_create(THIS_MODULE, CLASS_NAME);
       if (IS_ERR(my_class)) {
           ret = PTR_ERR(my_class);
           goto fail_class;
       }
       
       // Create device
       if (IS_ERR(device_create(my_class, NULL, dev_num,
                                NULL, DEVICE_NAME))) {
           ret = PTR_ERR(my_class);
           goto fail_device;
       }
       
       pr_info("%s: Driver loaded (major: %d)\n",
               DEVICE_NAME, MAJOR(dev_num));
       return 0;
   
   fail_device:
       class_destroy(my_class);
   fail_class:
       cdev_del(&my_dev->cdev);
   fail_cdev:
       unregister_chrdev_region(dev_num, 1);
   fail_alloc:
       kfree(my_dev->buffer);
       kfree(my_dev);
       return ret;
   }
   
   static void __exit my_driver_exit(void) {
       device_destroy(my_class, dev_num);
       class_destroy(my_class);
       cdev_del(&my_dev->cdev);
       unregister_chrdev_region(dev_num, 1);
       kfree(my_dev->buffer);
       kfree(my_dev);
       pr_info("%s: Driver unloaded\n", DEVICE_NAME);
   }
   
   module_init(my_driver_init);
   module_exit(my_driver_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Complete character device driver");

================================================================================
3. Platform Drivers
================================================================================

3.1 Platform Device Framework
------------------------------

**Platform Driver Structure:**

.. code-block:: c

   #include <linux/platform_device.h>
   #include <linux/of.h>
   #include <linux/of_device.h>
   
   struct my_platform_data {
       void __iomem *base;
       int irq;
       struct resource *mem_res;
   };
   
   static int my_platform_probe(struct platform_device *pdev) {
       struct my_platform_data *pdata;
       struct resource *res;
       int ret;
       
       dev_info(&pdev->dev, "Probing device\n");
       
       // Allocate private data
       pdata = devm_kzalloc(&pdev->dev, sizeof(*pdata), GFP_KERNEL);
       if (!pdata)
           return -ENOMEM;
       
       // Get memory resource
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       if (!res) {
           dev_err(&pdev->dev, "No memory resource\n");
           return -ENODEV;
       }
       
       // Map I/O memory
       pdata->base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(pdata->base))
           return PTR_ERR(pdata->base);
       
       // Get IRQ
       pdata->irq = platform_get_irq(pdev, 0);
       if (pdata->irq < 0) {
           dev_err(&pdev->dev, "No IRQ resource\n");
           return pdata->irq;
       }
       
       // Request IRQ
       ret = devm_request_irq(&pdev->dev, pdata->irq, my_irq_handler,
                              0, dev_name(&pdev->dev), pdata);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ\n");
           return ret;
       }
       
       // Save private data
       platform_set_drvdata(pdev, pdata);
       
       // Initialize hardware
       writel(ENABLE_BIT, pdata->base + CTRL_REG);
       
       dev_info(&pdev->dev, "Device probed successfully\n");
       return 0;
   }
   
   static int my_platform_remove(struct platform_device *pdev) {
       struct my_platform_data *pdata = platform_get_drvdata(pdev);
       
       // Disable hardware
       writel(0, pdata->base + CTRL_REG);
       
       dev_info(&pdev->dev, "Device removed\n");
       return 0;
   }
   
   static const struct of_device_id my_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { .compatible = "vendor,mydevice-v2", },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_of_match);
   
   static struct platform_driver my_platform_driver = {
       .probe = my_platform_probe,
       .remove = my_platform_remove,
       .driver = {
           .name = "mydevice",
           .of_match_table = my_of_match,
       },
   };
   
   module_platform_driver(my_platform_driver);

**Device Tree Binding:**

.. code-block:: dts

   / {
       mydevice@48040000 {
           compatible = "vendor,mydevice";
           reg = <0x48040000 0x1000>;
           interrupts = <42>;
           interrupt-parent = <&intc>;
           clock-frequency = <48000000>;
           status = "okay";
       };
   };

3.2 Resource Management
------------------------

**Memory-Mapped I/O:**

.. code-block:: c

   #include <linux/io.h>
   
   struct resource *res;
   void __iomem *base;
   
   // Get resource from device tree
   res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
   
   // Request and map (managed)
   base = devm_ioremap_resource(&pdev->dev, res);
   if (IS_ERR(base))
       return PTR_ERR(base);
   
   // Read/write registers
   u32 val = readl(base + OFFSET);
   writel(val | BIT(3), base + OFFSET);
   
   // Memory barriers
   writel_relaxed(val, base + OFFSET);  // No barrier
   wmb();  // Write memory barrier

**IRQ Handling:**

.. code-block:: c

   #include <linux/interrupt.h>
   
   static irqreturn_t my_irq_handler(int irq, void *dev_id) {
       struct my_platform_data *pdata = dev_id;
       u32 status;
       
       // Read interrupt status
       status = readl(pdata->base + STATUS_REG);
       
       // Clear interrupt
       writel(status, pdata->base + STATUS_REG);
       
       // Handle interrupt
       if (status & DATA_READY) {
           // Process data
       }
       
       return IRQ_HANDLED;
   }
   
   // Request IRQ (managed)
   ret = devm_request_irq(&pdev->dev, irq, my_irq_handler,
                          IRQF_TRIGGER_RISING, "mydevice", pdata);

================================================================================
4. I2C and SPI Drivers
================================================================================

4.1 I2C Driver Development
---------------------------

**I2C Driver Template:**

.. code-block:: c

   #include <linux/i2c.h>
   #include <linux/regmap.h>
   
   struct my_i2c_device {
       struct i2c_client *client;
       struct regmap *regmap;
   };
   
   static int my_i2c_probe(struct i2c_client *client,
                           const struct i2c_device_id *id) {
       struct my_i2c_device *dev;
       int ret;
       
       dev_info(&client->dev, "Probing I2C device\n");
       
       dev = devm_kzalloc(&client->dev, sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       dev->client = client;
       i2c_set_clientdata(client, dev);
       
       // Initialize regmap
       dev->regmap = devm_regmap_init_i2c(client, &my_regmap_config);
       if (IS_ERR(dev->regmap))
           return PTR_ERR(dev->regmap);
       
       // Read device ID
       unsigned int id_reg;
       ret = regmap_read(dev->regmap, REG_ID, &id_reg);
       if (ret < 0)
           return ret;
       
       dev_info(&client->dev, "Device ID: 0x%x\n", id_reg);
       
       // Initialize device
       regmap_write(dev->regmap, REG_CTRL, CTRL_ENABLE);
       
       return 0;
   }
   
   static int my_i2c_remove(struct i2c_client *client) {
       struct my_i2c_device *dev = i2c_get_clientdata(client);
       
       // Disable device
       regmap_write(dev->regmap, REG_CTRL, 0);
       
       return 0;
   }
   
   static const struct i2c_device_id my_i2c_id[] = {
       { "mydevice", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(i2c, my_i2c_id);
   
   static const struct of_device_id my_i2c_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_i2c_of_match);
   
   static struct i2c_driver my_i2c_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = my_i2c_of_match,
       },
       .probe = my_i2c_probe,
       .remove = my_i2c_remove,
       .id_table = my_i2c_id,
   };
   module_i2c_driver(my_i2c_driver);

**I2C Communication:**

.. code-block:: c

   // SMBus API (simple)
   s32 val = i2c_smbus_read_byte_data(client, reg);
   i2c_smbus_write_byte_data(client, reg, val);
   
   // I2C messages (advanced)
   struct i2c_msg msgs[2];
   u8 reg_addr = 0x10;
   u8 data[4];
   
   // Write register address
   msgs[0].addr = client->addr;
   msgs[0].flags = 0;
   msgs[0].len = 1;
   msgs[0].buf = &reg_addr;
   
   // Read data
   msgs[1].addr = client->addr;
   msgs[1].flags = I2C_M_RD;
   msgs[1].len = sizeof(data);
   msgs[1].buf = data;
   
   ret = i2c_transfer(client->adapter, msgs, 2);

**Device Tree Binding:**

.. code-block:: dts

   &i2c0 {
       status = "okay";
       
       mydevice@48 {
           compatible = "vendor,mydevice";
           reg = <0x48>;
           interrupt-parent = <&gpio1>;
           interrupts = <10 IRQ_TYPE_EDGE_FALLING>;
       };
   };

4.2 SPI Driver Development
---------------------------

**SPI Driver Template:**

.. code-block:: c

   #include <linux/spi/spi.h>
   
   struct my_spi_device {
       struct spi_device *spi;
       struct mutex lock;
   };
   
   static int my_spi_probe(struct spi_device *spi) {
       struct my_spi_device *dev;
       u8 data[2];
       int ret;
       
       dev_info(&spi->dev, "Probing SPI device\n");
       
       dev = devm_kzalloc(&spi->dev, sizeof(*dev), GFP_KERNEL);
       if (!dev)
           return -ENOMEM;
       
       dev->spi = spi;
       mutex_init(&dev->lock);
       spi_set_drvdata(spi, dev);
       
       // Configure SPI mode
       spi->mode = SPI_MODE_0;
       spi->bits_per_word = 8;
       ret = spi_setup(spi);
       if (ret < 0)
           return ret;
       
       // Read device ID
       data[0] = CMD_READ_ID;
       ret = spi_write_then_read(spi, data, 1, data, 2);
       if (ret < 0)
           return ret;
       
       dev_info(&spi->dev, "Device ID: 0x%02x%02x\n", data[0], data[1]);
       
       return 0;
   }
   
   static int my_spi_remove(struct spi_device *spi) {
       return 0;
   }
   
   static const struct of_device_id my_spi_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_spi_of_match);
   
   static struct spi_driver my_spi_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = my_spi_of_match,
       },
       .probe = my_spi_probe,
       .remove = my_spi_remove,
   };
   module_spi_driver(my_spi_driver);

**SPI Transfers:**

.. code-block:: c

   // Simple read/write
   u8 tx_buf[4] = {CMD, ADDR, DATA1, DATA2};
   u8 rx_buf[4];
   
   // Full duplex
   spi_write_then_read(spi, tx_buf, 2, rx_buf, 2);
   
   // Manual transfer
   struct spi_transfer xfer = {
       .tx_buf = tx_buf,
       .rx_buf = rx_buf,
       .len = sizeof(tx_buf),
   };
   struct spi_message msg;
   
   spi_message_init(&msg);
   spi_message_add_tail(&xfer, &msg);
   spi_sync(spi, &msg);

================================================================================
5. GPIO and Pinctrl
================================================================================

5.1 GPIO Framework
-------------------

**GPIO Descriptor API (modern):**

.. code-block:: c

   #include <linux/gpio/consumer.h>
   
   struct gpio_desc *gpio_enable;
   struct gpio_desc *gpio_reset;
   
   // Get GPIO from device tree
   gpio_enable = devm_gpiod_get(&pdev->dev, "enable", GPIOD_OUT_LOW);
   if (IS_ERR(gpio_enable))
       return PTR_ERR(gpio_enable);
   
   gpio_reset = devm_gpiod_get(&pdev->dev, "reset", GPIOD_OUT_HIGH);
   
   // Set GPIO value
   gpiod_set_value(gpio_enable, 1);  // Set high
   gpiod_set_value(gpio_reset, 0);   // Set low
   
   // Get GPIO value
   int val = gpiod_get_value(gpio_enable);
   
   // Toggle
   gpiod_set_value(gpio_enable, !gpiod_get_value(gpio_enable));

**Device Tree GPIO:**

.. code-block:: dts

   mydevice {
       compatible = "vendor,mydevice";
       enable-gpios = <&gpio1 10 GPIO_ACTIVE_HIGH>;
       reset-gpios = <&gpio2 5 GPIO_ACTIVE_LOW>;
   };

**GPIO Interrupts:**

.. code-block:: c

   #include <linux/gpio.h>
   #include <linux/interrupt.h>
   
   int gpio_num, irq;
   
   // Get GPIO number from descriptor
   gpio_num = desc_to_gpio(gpio_desc);
   
   // Get IRQ from GPIO
   irq = gpio_to_irq(gpio_num);
   
   // Request IRQ
   ret = devm_request_irq(&pdev->dev, irq, my_gpio_irq_handler,
                          IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                          "my_gpio_irq", pdata);

5.2 Pinctrl Framework
----------------------

**Pinctrl Configuration:**

.. code-block:: c

   #include <linux/pinctrl/consumer.h>
   
   struct pinctrl *pctrl;
   struct pinctrl_state *state;
   
   // Get pinctrl
   pctrl = devm_pinctrl_get(&pdev->dev);
   if (IS_ERR(pctrl))
       return PTR_ERR(pctrl);
   
   // Select state
   state = pinctrl_lookup_state(pctrl, "default");
   if (!IS_ERR(state))
       pinctrl_select_state(pctrl, state);
   
   // Alternative states
   state = pinctrl_lookup_state(pctrl, "sleep");
   pinctrl_select_state(pctrl, state);

**Device Tree Pinctrl:**

.. code-block:: dts

   mydevice {
       pinctrl-names = "default", "sleep";
       pinctrl-0 = <&mydevice_default_pins>;
       pinctrl-1 = <&mydevice_sleep_pins>;
   };

================================================================================
6. Key Takeaways
================================================================================

.. code-block:: text

   Driver Types:
   =============
   Character: Stream devices (/dev/xxx)
   Platform:  SoC peripherals (I2C, SPI, GPIO)
   I2C:       I2C bus devices
   SPI:       SPI bus devices
   Block:     Storage devices
   Network:   Network interfaces
   
   Module Basics:
   ==============
   module_init(init_fn);
   module_exit(exit_fn);
   MODULE_LICENSE("GPL");
   
   Character Device:
   =================
   alloc_chrdev_region(&dev, 0, 1, "name");
   cdev_init(&cdev, &fops);
   cdev_add(&cdev, dev, 1);
   class_create()/device_create()
   
   Platform Driver:
   ================
   platform_driver_register(&driver);
   .probe/.remove callbacks
   platform_get_resource()
   devm_ioremap_resource()
   readl()/writel()
   
   I2C Driver:
   ===========
   i2c_add_driver(&driver);
   i2c_smbus_read/write_byte_data()
   regmap API for register access
   
   SPI Driver:
   ===========
   spi_register_driver(&driver);
   spi_write_then_read()
   spi_sync()
   
   GPIO:
   =====
   devm_gpiod_get(&dev, "name", flags);
   gpiod_set_value(gpio, val);
   gpio_to_irq(gpio);
   
   Best Practices:
   ===============
   - Use devm_* functions (auto cleanup)
   - Proper error handling
   - Device tree bindings
   - Managed resources
   - Locking (mutexes, spinlocks)
   - Safe copy_to/from_user()

================================================================================
END OF CHEATSHEET
================================================================================
