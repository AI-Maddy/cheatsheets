====================================================================
Linux Device Drivers & Kernel Modules — Complete Guide
====================================================================

**Comprehensive coverage of Linux device driver development:** Character drivers, platform drivers, device tree bindings, driver model, sysfs, udev, and kernel modules.

**Current as of:** Linux 6.12–6.16 (January 2026)  
**Architecture focus:** ARM64, x86_64  
**Covers:** Professional Linux Kernel Architecture Chapters 6, 7

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**Linux Device Drivers** interface hardware with kernel subsystems, expose devices to userspace, and manage hardware resources.

**Driver Types:**

.. code-block:: text

   Type                  Access Method          Examples
   ────────────────────  ─────────────────────  ────────────────────────────
   Character Drivers     /dev nodes, read/write Serial ports, GPIOs, sensors
   Block Drivers         Block I/O              Hard drives, SSDs, SD cards
   Network Drivers       Network stack          Ethernet, Wi-Fi, CAN
   Platform Drivers      Device tree/ACPI       SoC peripherals (UART, I2C)
   PCI Drivers           PCI bus enumeration    PCIe devices, GPUs
   USB Drivers           USB subsystem          USB devices, webcams

**Quick Commands:**

.. code-block:: bash

   # Load module
   sudo insmod mydriver.ko
   sudo modprobe mydriver
   
   # Unload module
   sudo rmmod mydriver
   sudo modprobe -r mydriver
   
   # Module info
   modinfo mydriver.ko
   lsmod | grep mydriver
   
   # Check device
   ls -l /dev/mydev
   cat /sys/class/myclass/mydev/uevent
   
   # Check driver binding
   ls /sys/bus/platform/drivers/mydriver/
   cat /sys/bus/platform/devices/*/driver/uevent

================================================================================
1. Character Device Drivers
================================================================================

**1.1 Basic Character Driver Template**
-----------------------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/fs.h>
   #include <linux/cdev.h>
   #include <linux/device.h>
   #include <linux/uaccess.h>
   
   #define DEVICE_NAME "mydev"
   #define CLASS_NAME  "myclass"
   
   static dev_t dev_num;
   static struct class *my_class;
   static struct cdev my_cdev;
   static char msg[256] = "Hello from kernel!\n";
   
   /* File Operations */
   static int my_open(struct inode *inode, struct file *filp) {
       pr_info("%s: device opened\n", DEVICE_NAME);
       return 0;
   }
   
   static int my_release(struct inode *inode, struct file *filp) {
       pr_info("%s: device closed\n", DEVICE_NAME);
       return 0;
   }
   
   static ssize_t my_read(struct file *filp, char __user *buf,
                          size_t len, loff_t *off) {
       size_t to_copy = min(len, strlen(msg) + 1);
       
       if (*off > 0)
           return 0;  /* EOF */
       
       if (copy_to_user(buf, msg, to_copy))
           return -EFAULT;
       
       *off += to_copy;
       return to_copy;
   }
   
   static ssize_t my_write(struct file *filp, const char __user *buf,
                           size_t len, loff_t *off) {
       size_to_copy = min(len, sizeof(msg) - 1);
       
       if (copy_from_user(msg, buf, to_copy))
           return -EFAULT;
       
       msg[to_copy] = '\0';
       pr_info("%s: received %zu bytes\n", DEVICE_NAME, to_copy);
       return to_copy;
   }
   
   static long my_ioctl(struct file *filp, unsigned int cmd,
                        unsigned long arg) {
       switch (cmd) {
       case MY_IOCTL_RESET:
           memset(msg, 0, sizeof(msg));
           return 0;
       default:
           return -ENOTTY;
       }
   }
   
   static const struct file_operations fops = {
       .owner          = THIS_MODULE,
       .open           = my_open,
       .release        = my_release,
       .read           = my_read,
       .write          = my_write,
       .unlocked_ioctl = my_ioctl,
   };
   
   /* Init/Exit */
   static int __init my_init(void) {
       int ret;
       
       /* Allocate device number dynamically */
       ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
       if (ret < 0)
           return ret;
       
       /* Initialize cdev */
       cdev_init(&my_cdev, &fops);
       my_cdev.owner = THIS_MODULE;
       
       /* Add cdev to kernel */
       ret = cdev_add(&my_cdev, dev_num, 1);
       if (ret < 0)
           goto err_chrdev;
       
       /* Create device class */
       my_class = class_create(THIS_MODULE, CLASS_NAME);
       if (IS_ERR(my_class)) {
           ret = PTR_ERR(my_class);
           goto err_cdev;
       }
       
       /* Create device node */
       if (IS_ERR(device_create(my_class, NULL, dev_num, NULL,
                                DEVICE_NAME))) {
           ret = -ENOMEM;
           goto err_class;
       }
       
       pr_info("%s: registered major=%d minor=%d\n",
               DEVICE_NAME, MAJOR(dev_num), MINOR(dev_num));
       return 0;
   
   err_class:
       class_destroy(my_class);
   err_cdev:
       cdev_del(&my_cdev);
   err_chrdev:
       unregister_chrdev_region(dev_num, 1);
       return ret;
   }
   
   static void __exit my_exit(void) {
       device_destroy(my_class, dev_num);
       class_destroy(my_class);
       cdev_del(&my_cdev);
       unregister_chrdev_region(dev_num, 1);
       pr_info("%s: unloaded\n", DEVICE_NAME);
   }
   
   module_init(my_init);
   module_exit(my_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Simple character device driver");
   MODULE_VERSION("1.0");

**1.2 File Operations Reference**
-----------------------------------

.. code-block:: text

   Operation         Purpose                          Return Value
   ────────────────  ───────────────────────────────  ────────────────────────
   .open             Initialize per-open state        0 or -errno
   .release          Cleanup per-open state           0 (almost always)
   .read             Copy data to userspace           bytes read, 0=EOF, -errno
   .write            Copy data from userspace         bytes written, -errno
   .unlocked_ioctl   Custom commands                  0, -ENOTTY, -EINVAL
   .compat_ioctl     32-bit ioctl on 64-bit system    0, -ENOTTY
   .llseek           Change file position             new position, -errno
   .poll             Support select/poll/epoll        POLLIN | POLLOUT | ...
   .mmap             Memory map device memory         0, -errno
   .fasync           Asynchronous notification        0, -errno

**1.3 User↔Kernel Data Transfer**
-----------------------------------

.. code-block:: c

   /* Copy from userspace to kernel */
   unsigned long copy_from_user(void *to, const void __user *from,
                                unsigned long n);
   
   /* Copy from kernel to userspace */
   unsigned long copy_to_user(void __user *to, const void *from,
                              unsigned long n);
   
   /* Get single value from userspace */
   get_user(x, ptr);    /* x = *ptr */
   
   /* Put single value to userspace */
   put_user(x, ptr);    /* *ptr = x */
   
   /* Return value: 0 = success, non-zero = bytes not copied */

**Example:**

.. code-block:: c

   static ssize_t my_read(struct file *filp, char __user *buf,
                          size_t count, loff_t *ppos) {
       char kbuf[256];
       size_t len;
       
       snprintf(kbuf, sizeof(kbuf), "Counter: %d\n", my_counter);
       len = strlen(kbuf);
       
       if (*ppos >= len)
           return 0;  /* EOF */
       
       if (*ppos + count > len)
           count = len - *ppos;
       
       if (copy_to_user(buf, kbuf + *ppos, count))
           return -EFAULT;
       
       *ppos += count;
       return count;
   }

================================================================================
2. Platform Drivers & Device Tree
================================================================================

**2.1 Platform Driver Template**
----------------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/of.h>
   #include <linux/of_device.h>
   
   struct mydev_private {
       void __iomem *base;
       struct device *dev;
       int irq;
   };
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_private *priv;
       struct resource *res;
       int ret;
       
       dev_info(&pdev->dev, "Probing device\n");
       
       /* Allocate private data */
       priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
       if (!priv)
           return -ENOMEM;
       
       priv->dev = &pdev->dev;
       
       /* Get memory resource */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       priv->base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(priv->base))
           return PTR_ERR(priv->base);
       
       /* Get IRQ */
       priv->irq = platform_get_irq(pdev, 0);
       if (priv->irq < 0)
           return priv->irq;
       
       /* Request IRQ */
       ret = devm_request_irq(&pdev->dev, priv->irq, mydev_irq_handler,
                              0, dev_name(&pdev->dev), priv);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ\n");
           return ret;
       }
       
       /* Save private data */
       platform_set_drvdata(pdev, priv);
       
       dev_info(&pdev->dev, "Device probed successfully\n");
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_private *priv = platform_get_drvdata(pdev);
       
       dev_info(&pdev->dev, "Removing device\n");
       /* Cleanup handled by devm_* functions */
       return 0;
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,mydevice-v1.0", },
       { .compatible = "vendor,mydevice", },
       { /* sentinel */ }
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct platform_driver mydev_driver = {
       .probe  = mydev_probe,
       .remove = mydev_remove,
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
   };
   
   module_platform_driver(mydev_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Platform driver example");

**2.2 Device Tree Bindings**
------------------------------

**Example DTS:**

.. code-block:: dts

   / {
       soc {
           mydevice@fe100000 {
               compatible = "vendor,mydevice-v1.0";
               reg = <0x0 0xfe100000 0x0 0x1000>;
               interrupts = <GIC_SPI 50 IRQ_TYPE_LEVEL_HIGH>;
               clocks = <&cru CLK_MYDEV>;
               clock-names = "core";
               resets = <&cru SRST_MYDEV>;
               reset-names = "core";
               status = "okay";
           };
       };
   };

**Common Device Tree Properties:**

.. code-block:: text

   Property              Purpose                          Example
   ────────────────────  ───────────────────────────────  ────────────────────────
   compatible            Driver matching string           "vendor,device-v1.0"
   reg                   Memory-mapped register address   <0x0 0xfe100000 0x0 0x1000>
   interrupts            Interrupt specification          <GIC_SPI 50 IRQ_TYPE_LEVEL_HIGH>
   clocks / clock-names  Clock phandles                   <&cru CLK_UART0>, "baudclk"
   resets / reset-names  Reset controller phandles        <&cru SRST_UART0>, "core"
   pinctrl-0/names       Pin configuration                <&uart0_pins>, "default"
   status                Enable/disable device            "okay" / "disabled"

**Accessing Device Tree Properties:**

.. code-block:: c

   /* Read integer property */
   u32 val;
   ret = of_property_read_u32(np, "clock-frequency", &val);
   
   /* Read string property */
   const char *str;
   ret = of_property_read_string(np, "label", &str);
   
   /* Get phandle */
   struct device_node *clk_np;
   clk_np = of_parse_phandle(np, "clocks", 0);
   
   /* Check if property exists */
   if (of_property_read_bool(np, "dma-coherent")) {
       /* Device supports cache-coherent DMA */
   }

================================================================================
3. Driver Model & Sysfs
================================================================================

**3.1 Sysfs Attributes**
-------------------------

Sysfs exposes kernel objects as files in `/sys/`.

**Create device attribute:**

.. code-block:: c

   static ssize_t value_show(struct device *dev,
                             struct device_attribute *attr,
                             char *buf) {
       struct mydev_private *priv = dev_get_drvdata(dev);
       return sprintf(buf, "%d\n", priv->value);
   }
   
   static ssize_t value_store(struct device *dev,
                              struct device_attribute *attr,
                              const char *buf, size_t count) {
       struct mydev_private *priv = dev_get_drvdata(dev);
       int ret;
       
       ret = kstrtoint(buf, 10, &priv->value);
       if (ret)
           return ret;
       
       return count;
   }
   static DEVICE_ATTR_RW(value);
   
   static struct attribute *mydev_attrs[] = {
       &dev_attr_value.attr,
       NULL,
   };
   ATTRIBUTE_GROUPS(mydev);
   
   /* In driver struct: */
   static struct platform_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .dev_groups = mydev_groups,
       },
   };

**Access from userspace:**

.. code-block:: bash

   cat /sys/devices/platform/mydevice/value
   echo 42 > /sys/devices/platform/mydevice/value

**3.2 Kobjects & Ksets**
-------------------------

Low-level infrastructure for sysfs.

.. code-block:: c

   struct kobject {
       const char *name;
       struct list_head entry;
       struct kobject *parent;
       struct kset *kset;
       struct kobj_type *ktype;
       struct kernfs_node *sd;  /* sysfs directory entry */
       struct kref kref;
       unsigned int state_initialized:1;
       unsigned int state_in_sysfs:1;
       unsigned int state_add_uevent_sent:1;
       unsigned int state_remove_uevent_sent:1;
       unsigned int uevent_suppress:1;
   };

================================================================================
4. Udev — Device Manager
================================================================================

**4.1 Udev Rules**
-------------------

Udev manages `/dev` nodes and device permissions.

**Rule Location:**

.. code-block:: text

   /etc/udev/rules.d/*.rules     (custom rules)
   /lib/udev/rules.d/*.rules     (distribution defaults)

**Rule Syntax:**

.. code-block:: text

   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
       SYMLINK+="serial/ftdi-%s{serial}", MODE="0660", GROUP="dialout"

**Common Match Keys:**

.. code-block:: text

   Key                 Matches On                    Example
   ──────────────────  ────────────────────────────  ────────────────────────
   ACTION              add/remove/change             ACTION=="add"
   KERNEL              Device node name              KERNEL=="ttyUSB[0-9]*"
   SUBSYSTEM           Subsystem (block/usb/tty)     SUBSYSTEM=="usb"
   ATTR{file}          Sysfs attribute value         ATTR{idVendor}=="0bda"
   ATTRS{file}         Parent sysfs attribute        ATTRS{serial}=="ABC123"
   ENV{var}            Environment variable          ENV{ID_MODEL}=="..."

**Common Assignment Keys:**

.. code-block:: text

   Key                 Action                        Example
   ──────────────────  ────────────────────────────  ────────────────────────
   NAME                Device node name              NAME="mydev%d"
   SYMLINK             Create symlink                SYMLINK+="myserial"
   MODE                Permissions                   MODE="0660"
   OWNER/GROUP         Ownership                     GROUP="dialout"
   TAG                 Add tag                       TAG+="uaccess"
   RUN                 Execute program               RUN+="/usr/bin/script.sh"

**Example: USB Serial Device:**

.. code-block:: text

   # /etc/udev/rules.d/70-usb-serial.rules
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
       SYMLINK+="serial/ch340-%s{serial}", MODE="0660", GROUP="dialout", \
       TAG+="uaccess"

**Test udev rule:**

.. code-block:: bash

   sudo udevadm test /sys/class/tty/ttyUSB0
   sudo udevadm trigger

================================================================================
5. Kernel Modules
================================================================================

**5.1 Module Basics**
----------------------

**Minimal Module:**

.. code-block:: c

   #include <linux/module.h>
   #include <linux/kernel.h>
   
   static int __init hello_init(void) {
       pr_info("Hello, kernel!\n");
       return 0;
   }
   
   static void __exit hello_exit(void) {
       pr_info("Goodbye, kernel!\n");
   }
   
   module_init(hello_init);
   module_exit(hello_exit);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Hello world module");
   MODULE_VERSION("1.0");

**5.2 Module Parameters**
--------------------------

.. code-block:: c

   static int debug = 0;
   module_param(debug, int, 0644);
   MODULE_PARM_DESC(debug, "Debug level (0=off, 1=on)");
   
   static char *name = "default";
   module_param(name, charp, 0444);
   MODULE_PARM_DESC(name, "Device name");

**Load with parameters:**

.. code-block:: bash

   sudo insmod mymodule.ko debug=1 name="mydev"
   sudo modprobe mymodule debug=1

**5.3 Module Dependencies**
----------------------------

.. code-block:: c

   /* Export symbol for other modules */
   EXPORT_SYMBOL(my_function);
   EXPORT_SYMBOL_GPL(my_gpl_function);  /* GPL-only */
   
   /* Use external symbol */
   extern int external_function(void);

**5.4 Makefile for Out-of-Tree Module**
-----------------------------------------

.. code-block:: makefile

   obj-m += mydriver.o
   
   # Multi-file module
   mydriver-objs := main.o helper.o
   
   KDIR ?= /lib/modules/$(shell uname -r)/build
   
   all:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules
   
   clean:
   	$(MAKE) -C $(KDIR) M=$(PWD) clean
   
   install:
   	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
   
   load:
   	sudo insmod mydriver.ko
   
   unload:
   	sudo rmmod mydriver

**Build:**

.. code-block:: bash

   make
   sudo make install
   sudo depmod -a

================================================================================
6. Managed Device Resources (devm_*)
================================================================================

**6.1 Overview**
-----------------

`devm_*` functions automatically free resources when driver detaches.

**Benefits:**
- Automatic cleanup on probe failure
- Automatic cleanup on driver removal
- Simpler error handling

**Common devm_* Functions:**

.. code-block:: c

   /* Memory allocation */
   void *devm_kmalloc(struct device *dev, size_t size, gfp_t gfp);
   void *devm_kzalloc(struct device *dev, size_t size, gfp_t gfp);
   
   /* I/O memory mapping */
   void __iomem *devm_ioremap(struct device *dev, resource_size_t offset,
                              resource_size_t size);
   void __iomem *devm_ioremap_resource(struct device *dev,
                                       struct resource *res);
   
   /* Interrupt request */
   int devm_request_irq(struct device *dev, unsigned int irq,
                        irq_handler_t handler, unsigned long flags,
                        const char *name, void *dev_id);
   
   /* Clock management */
   struct clk *devm_clk_get(struct device *dev, const char *id);
   
   /* GPIO */
   int devm_gpio_request(struct device *dev, unsigned gpio,
                         const char *label);
   
   /* Regulator */
   struct regulator *devm_regulator_get(struct device *dev,
                                        const char *id);

**Example:**

.. code-block:: c

   static int mydev_probe(struct platform_device *pdev) {
       struct resource *res;
       void __iomem *base;
       int irq, ret;
       
       /* All of these are auto-freed on error or remove */
       
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(base))
           return PTR_ERR(base);
       
       irq = platform_get_irq(pdev, 0);
       ret = devm_request_irq(&pdev->dev, irq, mydev_irq,
                              0, "mydev", NULL);
       if (ret)
           return ret;
       
       /* No need for explicit cleanup in error path! */
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       /* Nothing to cleanup - devm_* handles it */
       return 0;
   }

================================================================================
7. Debugging Drivers
================================================================================

**7.1 Kernel Logging**
-----------------------

.. code-block:: c

   /* Priority levels */
   pr_emerg("System is unusable\n");
   pr_alert("Action must be taken immediately\n");
   pr_crit("Critical conditions\n");
   pr_err("Error conditions\n");
   pr_warning("Warning conditions\n");
   pr_notice("Normal but significant\n");
   pr_info("Informational\n");
   pr_debug("Debug-level messages\n");  /* Only if DEBUG defined */
   
   /* Device-specific logging */
   dev_err(&pdev->dev, "Failed to initialize\n");
   dev_warn(&pdev->dev, "Low voltage detected\n");
   dev_info(&pdev->dev, "Device ready\n");
   dev_dbg(&pdev->dev, "Register value: 0x%x\n", val);

**View logs:**

.. code-block:: bash

   dmesg
   dmesg | tail -50
   dmesg -w  # Follow mode
   
   journalctl -k  # Kernel messages
   journalctl -kf # Follow kernel messages

**7.2 Dynamic Debug**
----------------------

.. code-block:: bash

   # Enable all debug messages for driver
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific file
   echo 'file drivers/mydriver.c +p' > /sys/kernel/debug/dynamic_debug/control
   
   # Enable debug for specific function
   echo 'func mydev_probe +p' > /sys/kernel/debug/dynamic_debug/control
   
   # View current settings
   cat /sys/kernel/debug/dynamic_debug/control

**7.3 Debugfs**
----------------

.. code-block:: c

   #include <linux/debugfs.h>
   
   static struct dentry *debug_dir;
   static u32 debug_value;
   
   static int mydev_probe(struct platform_device *pdev) {
       /* Create debugfs directory */
       debug_dir = debugfs_create_dir("mydevice", NULL);
       
       /* Create debugfs files */
       debugfs_create_u32("value", 0644, debug_dir, &debug_value);
       debugfs_create_file("status", 0444, debug_dir, NULL,
                           &status_fops);
       
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       debugfs_remove_recursive(debug_dir);
       return 0;
   }

**Access:**

.. code-block:: bash

   cat /sys/kernel/debug/mydevice/value
   echo 42 > /sys/kernel/debug/mydevice/value

================================================================================
8. Exam Preparation — 5 Questions
================================================================================

**Question 1: Character Driver Registration (12 points)**

a) Explain the difference between `register_chrdev()` and `alloc_chrdev_region()` + `cdev_add()`. (4 pts)
b) Why is dynamic major number allocation preferred? (4 pts)
c) What is the role of `class_create()` and `device_create()`? (4 pts)

**Answer:**

a) **Differences:**

- **register_chrdev()** (old API):
  - Allocates entire major number (all 256 minors)
  - Wastes minor numbers
  - Less flexible
  - Deprecated for new drivers

- **alloc_chrdev_region() + cdev_add()** (modern API):
  - Allocates only requested number of minors
  - More flexible (can register multiple devices)
  - Standard approach since kernel 2.6+
  - Allows finer control over device registration

b) **Dynamic allocation advantages:**
- Avoids major number conflicts
- No need to maintain major number registry
- Kernel assigns available number automatically
- Portable across systems
- `/proc/devices` shows assigned number

c) **class_create() and device_create():**
- **class_create()**: Creates device class in `/sys/class/`
- **device_create()**: Creates device node in `/dev/` (via udev)
- Together: Enable automatic `/dev/` node creation
- Without them: Manual `mknod` required

---

**Question 2: Platform Driver Probing (12 points)**

Device tree:
```dts
mydev@fe100000 {
    compatible = "vendor,mydev-v2.0", "vendor,mydev";
    reg = <0x0 0xfe100000 0x0 0x1000>;
    status = "disabled";
};
```

Driver:
```c
static const struct of_device_id mydev_of_match[] = {
    { .compatible = "vendor,mydev-v1.0", },
    { /* sentinel */ }
};
```

a) Will the driver probe? Why? (4 pts)
b) How to fix the driver to probe this device? (4 pts)
c) What happens if `status = "okay"`? (4 pts)

**Answer:**

a) **Will NOT probe** for two reasons:
1. `status = "disabled"` prevents probing
2. `compatible` mismatch (`"vendor,mydev-v2.0"` not in driver's match table)

b) **Fix options:**

Option 1 - Update driver match table:
```c
static const struct of_device_id mydev_of_match[] = {
    { .compatible = "vendor,mydev-v2.0", },
    { .compatible = "vendor,mydev-v1.0", },
    { .compatible = "vendor,mydev", },  /* Generic fallback */
    { /* sentinel */ }
};
```

Option 2 - Update device tree:
```dts
status = "okay";  /* Enable device */
```

c) **If status = "okay":**
- Device still won't probe (compatible mismatch)
- Driver needs matching compatible string
- Kernel logs: "No matching driver found"
- Device visible in `/sys/firmware/devicetree/` but no driver bound

---

**Question 3: Devm vs Manual Resource Management (10 points)**

Compare these two probe functions:

```c
/* Version A: Manual */
static int mydev_probe_a(struct platform_device *pdev) {
    void __iomem *base;
    int irq, ret;
    
    base = ioremap(0xfe100000, 0x1000);
    if (!base)
        return -ENOMEM;
    
    irq = platform_get_irq(pdev, 0);
    ret = request_irq(irq, mydev_irq, 0, "mydev", NULL);
    if (ret) {
        iounmap(base);
        return ret;
    }
    return 0;
}

/* Version B: Devm */
static int mydev_probe_b(struct platform_device *pdev) {
    void __iomem *base;
    int irq, ret;
    
    base = devm_ioremap(&pdev->dev, 0xfe100000, 0x1000);
    if (!base)
        return -ENOMEM;
    
    irq = platform_get_irq(pdev, 0);
    ret = devm_request_irq(&pdev->dev, irq, mydev_irq,
                           0, "mydev", NULL);
    return ret;
}
```

a) What happens if Version A's `request_irq()` fails? (5 pts)
b) Why is Version B better? (5 pts)

**Answer:**

a) **Version A failure:**
- `request_irq()` fails → returns error
- Error path correctly calls `iounmap(base)`
- **But**: if more resources added later, easy to forget cleanup
- **Memory leak risk** if error path not updated

b) **Version B advantages:**
1. **Simpler code**: No manual cleanup
2. **Safer**: Automatic cleanup on any error
3. **Correct ordering**: Resources freed in reverse allocation order
4. **Remove function**: Can be empty (auto-cleanup)
5. **Less bug-prone**: No forgotten cleanup paths

**Full comparison:**

```
Aspect              Manual (A)           Devm (B)
──────────────────  ───────────────────  ──────────────────────
Error handling      Complex, manual      Automatic
Remove function     Must free all        Can be empty
Bug risk            High (forgot free)   Low
Code size           Larger               Smaller
Performance         Identical            Identical
Probe failure       Manual iounmap       Auto iounmap
Driver remove       Manual free_irq      Auto free_irq
```

---

**Question 4: Udev Rule Evaluation (12 points)**

Udev rules:
```
# /etc/udev/rules.d/70-serial.rules
SUBSYSTEM=="tty", KERNEL=="ttyUSB*", GROUP="dialout", MODE="0660"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", SYMLINK+="serial/ch340"
SUBSYSTEM=="tty", ATTRS{idProduct}=="7523", OWNER="myuser"
```

USB device plugged in:
- idVendor: 1a86
- idProduct: 7523
- Kernel assigns: ttyUSB0

a) Which rules match? (4 pts)
b) What are final permissions/ownership? (4 pts)
c) What symlink is created? (4 pts)

**Answer:**

a) **All three rules match:**
1. Rule 1: Matches (`KERNEL=="ttyUSB*"`)
2. Rule 2: Matches (`ATTRS{idVendor}=="1a86"`)
3. Rule 3: Matches (`ATTRS{idProduct}=="7523"`)

b) **Final permissions/ownership:**
```
GROUP="dialout"    (from Rule 1)
MODE="0660"        (from Rule 1)
OWNER="myuser"     (from Rule 3)
```

Final: `-rw-rw---- myuser dialout /dev/ttyUSB0`

c) **Symlink:**
```
/dev/serial/ch340 → ../ttyUSB0
```
(Only Rule 2 creates symlink)

---

**Question 5: Module Loading (10 points)**

Driver `mydriver.ko` depends on `helper.ko`.

a) What happens if you `insmod mydriver.ko` without loading `helper.ko` first? (5 pts)
b) How does `modprobe` differ from `insmod`? (5 pts)

**Answer:**

a) **insmod without dependency:**
```
Error: Unknown symbol in module
insmod: ERROR: could not insert module mydriver.ko: Unknown symbol in module
```

- Kernel tries to resolve symbols
- Finds undefined symbols from `helper.ko`
- **Insertion fails**
- Module not loaded

b) **modprobe vs insmod:**

```
Aspect              insmod                    modprobe
──────────────────  ────────────────────────  ──────────────────────────
Dependencies        Does NOT load             Automatically loads
Module location     Requires full path        Searches /lib/modules/
Module parameters   From command line         From /etc/modprobe.d/
Module removal      rmmod only                modprobe -r (deps too)
Database            Not used                  Uses modules.dep
Example             insmod /path/mydriver.ko  modprobe mydriver
```

**Correct sequence:**
```bash
# Manual (insmod)
sudo insmod helper.ko
sudo insmod mydriver.ko

# Automatic (modprobe)
sudo modprobe mydriver  # Loads helper.ko first automatically
```

================================================================================
9. Completion Checklist
================================================================================

□ Understand character device registration (cdev, class, device)
□ Implement file_operations (open, read, write, ioctl, release)
□ Use copy_to_user/copy_from_user correctly
□ Create platform drivers with device tree bindings
□ Parse device tree properties (of_property_read_*)
□ Use devm_* managed resources
□ Create sysfs attributes (DEVICE_ATTR_RW)
□ Write udev rules for device permissions
□ Load/unload kernel modules (insmod, modprobe, rmmod)
□ Export symbols for other modules (EXPORT_SYMBOL)
□ Debug drivers (pr_debug, dev_dbg, debugfs)
□ Handle interrupts in drivers (request_irq, devm_request_irq)
□ Understand driver probe/remove lifecycle
□ Use MODULE_DEVICE_TABLE for auto-loading
□ Test drivers with simple userspace programs

================================================================================
10. Key Takeaways
================================================================================

1. **alloc_chrdev_region()** preferred over register_chrdev() (dynamic major)
2. **devm_*** functions simplify resource management (auto-cleanup)
3. **copy_to_user/copy_from_user** mandatory for user↔kernel data transfer
4. **Platform drivers** match via device tree `compatible` property
5. **of_property_read_*** functions parse device tree properties
6. **Sysfs attributes** expose driver parameters to userspace
7. **Udev rules** manage `/dev/` nodes and permissions automatically
8. **modprobe** handles dependencies, insmod does not
9. **EXPORT_SYMBOL** makes functions available to other modules
10. **dev_err/dev_info** preferred over pr_err/pr_info (device context)
11. **IS_ERR/PTR_ERR** check pointer errors from kernel APIs
12. **module_platform_driver()** macro simplifies driver registration
13. **Dynamic debug** enables runtime debug message control
14. **Debugfs** useful for driver debugging and testing

================================================================================
References & Further Reading
================================================================================

**Books:**
- Linux Device Drivers (3rd Edition) - Jonathan Corbet, Alessandro Rubini, Greg Kroah-Hartman
- Professional Linux Kernel Architecture - Wolfgang Mauerer (Chapters 6, 7)
- Linux Kernel Development - Robert Love

**Kernel Documentation:**
- Documentation/driver-api/
- Documentation/devicetree/bindings/
- Documentation/filesystems/sysfs.txt
- Documentation/admin-guide/udev.rst

**Source Code:**
- drivers/char/ (character drivers)
- drivers/platform/ (platform drivers)
- drivers/base/ (driver model core)
- include/linux/device.h
- include/linux/platform_device.h

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Kernel Version:** Linux 6.12–6.16

================================================================================
