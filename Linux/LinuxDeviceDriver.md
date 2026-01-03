Linux Device Driver Cheat Sheet (focused on modern kernels ~6.1–6.12, early 2026 timeframe).
It covers the most commonly needed patterns for character drivers (most starter drivers), with notes about other types.1. 
# Minimal "Hello World" Style Module

```c
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("You");
MODULE_DESCRIPTION("Hello world driver");

static int __init hello_init(void) {
    pr_info("Hello, kernel!\n");
    return 0;
}

static void __exit hello_exit(void) {
    pr_info("Goodbye, kernel!\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

# Build (example Makefile for out-of-tree):
makefile

obj-m += hello.o

KDIR ?= /lib/modules/$(shell uname -r)/build

all:
    make -C $(KDIR) M=$(PWD) modules

clean:
    make -C $(KDIR) M=$(PWD) clean

# Basic Character Device Driver Skeleton (most common pattern 2025+)c
```c

#include <linux/module.h>
#include <linux/fs.h>           // alloc_chrdev_region
#include <linux/cdev.h>         // cdev_*
#include <linux/device.h>       // class_create, device_create
#include <linux/uaccess.h>      // copy_to_user / copy_from_user
#include <linux/errno.h>

#define DEVICE_NAME "mydev"
#define CLASS_NAME  "myclass"

static dev_t dev_num = 0;
static struct class *my_class;
static struct cdev my_cdev;
static char msg[256] = "Hello from kernel!\n";   // example buffer

/* ────────────────────────────────────────
   File operations (the heart of char driver)
───────────────────────────────────────── */
static int     my_open(struct inode *inode, struct file *filp) {
    pr_info("%s: device opened\n", DEVICE_NAME);
    return 0;
}

static int     my_release(struct inode *inode, struct file *filp) {
    pr_info("%s: device closed\n", DEVICE_NAME);
    return 0;
}

static ssize_t my_read(struct file *filp, char __user *buf,
                       size_t len, loff_t *off) {
    int to_copy = min(len, strlen(msg) + 1);
    if (*off > 0) return 0;                     // EOF after first read
    if (copy_to_user(buf, msg, to_copy))
        return -EFAULT;
    *off += to_copy;
    return to_copy;
}

static ssize_t my_write(struct file *filp, const char __user *buf,
                        size_t len, loff_t *off) {
    size_t to_copy = min(len, sizeof(msg)-1);
    if (copy_from_user(msg, buf, to_copy))
        return -EFAULT;
    msg[to_copy] = '\0';
    pr_info("%s: received %zu bytes\n", DEVICE_NAME, to_copy);
    return to_copy;
}

static long my_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    pr_info("%s: ioctl cmd=%u\n", DEVICE_NAME, cmd);
    return -ENOTTY;     // "Inappropriate ioctl for device"
}

/* Modern designated initializers (preferred since ~4.x) */
static const struct file_operations fops = {
    .owner          = THIS_MODULE,
    .open           = my_open,
    .release        = my_release,
    .read           = my_read,
    .write          = my_write,
    .unlocked_ioctl = my_ioctl,     // or .compat_ioctl_32 if 32-bit userland
    // .llseek      = noop_llseek,  // or custom
    // .mmap        = my_mmap,      // if needed
};

/* ────────────────────────────────────────
   Init / Exit
───────────────────────────────────────── */
static int __init my_init(void) {
    int ret;

    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) return ret;

    cdev_init(&my_cdev, &fops);
    my_cdev.owner = THIS_MODULE;

    ret = cdev_add(&my_cdev, dev_num, 1);
    if (ret < 0) goto err_chrdev;

    my_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(my_class)) {
        ret = PTR_ERR(my_class);
        goto err_cdev;
    }

    if (IS_ERR(device_create(my_class, NULL, dev_num, NULL, DEVICE_NAME))) {
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
MODULE_DESCRIPTION("Simple modern char device driver");
```

## Quick Reference Tables
# Major registration styles (char drivers)Style

| Style | Function used | When to use |
|-------|---------------|------------|
| Old (deprecated) | `register_chrdev()` | Very old code only |
| Classic static | `register_chrdev_region()` + `cdev_add()` | Still ok, common |
| Dynamic (preferred) | `alloc_chrdev_region()` + `cdev_add()` | Most new drivers |

# Important function pointers (file_operations)

| Member | Purpose | Common return values |
|--------|---------|----------------------|
| `.open` | Initialize per-open state | 0 or negative errno |
| `.release` | Cleanup per-open state | 0 (almost always) |
| `.read` | `copy_to_user()` | bytes read, 0=EOF, -errno |
| `.write` | `copy_from_user()` | bytes written, -errno |
| `.unlocked_ioctl` | Custom commands | 0, -ENOTTY, -ENOIOCTLCMD |
| `.mmap` | Memory mapping (rare in simple drv) | 0 or -errno |
| `.poll` / `.epoll` | Support poll/select/epoll | POLLIN \| POLLRDNORM etc |


# Memory & Safety Helpers
| Helper | Purpose |
|--------|---------|
| `pr_info` / `pr_err` | Better than `printk(KERN_INFO ...)` |
| `copy_to_user` / `copy_from_user` | Safe user ↔ kernel copy |
| `kmalloc` / `kfree` | Normal allocation (GFP_KERNEL) |
| `kzalloc` | `kmalloc` + zeroing |
| `devm_kmalloc` | Managed (auto-free on driver detach) |
| `container_of` | Get private struct from `struct device *` |
| `dev_err` / `dev_info` | Print with device name prefix |

# Common Minor Numbers / Devices (for testing)
| Device | Major | Minor | Path |
|--------|-------|-------|------|
| Your driver | dynamic | 0 | /dev/mydev |
| Null | 1 | 3 | /dev/null |
| Zero | 1 | 5 | /dev/zero |
| Random | 1 | 8/9 | /dev/random, /dev/urandom |

Loading / Testing
bash

# Build & load
```bash
#!/bin/bash
# Load/test script for mydev driver

set -e

DEVICE_NAME="mydev"
DRIVER_MODULE="mydev"

# Build
echo "Building module..."
make

# Load module
echo "Loading module..."
sudo insmod ${DRIVER_MODULE}.ko

# Get major number and create device node
MAJOR=$(grep $DEVICE_NAME /proc/devices | awk '{print $1}')
echo "Creating device node /dev/$DEVICE_NAME (major=$MAJOR)..."
sudo mknod -f /dev/$DEVICE_NAME c $MAJOR 0
sudo chmod 666 /dev/$DEVICE_NAME

# Show dmesg
echo "Kernel messages:"
sudo dmesg | tail -5

# Test read/write
echo "Testing write..."
echo "Hello Device!" | sudo tee /dev/$DEVICE_NAME > /dev/null

echo "Testing read..."
sudo cat /dev/$DEVICE_NAME

# Cleanup
echo "Unloading module..."
sudo rmmod $DRIVER_MODULE
sudo rm -f /dev/$DEVICE_NAME

echo "Done!"
```

# Quick Tips (2025–2026 kernels)
Use designated initializers → .open = my_open,
Prefer devm_ managed functions when possible
Always check pointers with IS_ERR()
Use modern logging: dev_err(dev, ...), pr_fmt("mydrv: ")
For platform drivers → use of_match_table / acpi_match_table
For new drivers → strongly consider using a proper subsystem (gpio, iio, hwmon, etc.) instead of raw char device
Read Documentation/driver-api/ (especially driver-model, device-io)

