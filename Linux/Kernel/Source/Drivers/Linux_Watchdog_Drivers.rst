================================
Linux Watchdog Drivers Guide
================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Watchdog Driver
---------------------

.. code-block:: c

   #include <linux/watchdog.h>
   
   static int mywdt_start(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       writel(WDT_ENABLE, data->regs + WDT_CTRL);
       return 0;
   }
   
   static int mywdt_stop(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       writel(WDT_DISABLE, data->regs + WDT_CTRL);
       return 0;
   }
   
   static int mywdt_ping(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       writel(WDT_KICK_VALUE, data->regs + WDT_KICK);
       return 0;
   }
   
   static int mywdt_set_timeout(struct watchdog_device *wdd, unsigned int timeout) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       writel(timeout, data->regs + WDT_TIMEOUT);
       wdd->timeout = timeout;
       return 0;
   }
   
   static const struct watchdog_ops mywdt_ops = {
       .owner = THIS_MODULE,
       .start = mywdt_start,
       .stop = mywdt_stop,
       .ping = mywdt_ping,
       .set_timeout = mywdt_set_timeout,
   };
   
   static const struct watchdog_info mywdt_info = {
       .options = WDIOF_SETTIMEOUT | WDIOF_KEEPALIVEPING | WDIOF_MAGICCLOSE,
       .identity = "My Watchdog",
   };
   
   /* Register watchdog */
   wdd->info = &mywdt_info;
   wdd->ops = &mywdt_ops;
   wdd->timeout = 30;  // Default 30 seconds
   wdd->min_timeout = 1;
   wdd->max_timeout = 255;
   
   ret = devm_watchdog_register_device(&pdev->dev, wdd);

Watchdog Subsystem Overview
============================

Introduction
------------

A watchdog timer is a hardware timer that automatically resets the system if software fails to periodically service it.

**Key Concepts:**

- **Timeout:** Time before system reset if not serviced
- **Ping/Kick:** Resetting the timer before timeout
- **Pretimeout:** Warning before actual timeout
- **Magic Close:** Proper closing prevents reset

Watchdog Info
-------------

.. code-block:: c

   struct watchdog_info {
       __u32 options;      // Supported features
       __u32 firmware_version;
       __u8  identity[32]; // Device name
   };
   
   /* Options flags */
   WDIOF_SETTIMEOUT        // Can set timeout
   WDIOF_MAGICCLOSE        // Supports magic close
   WDIOF_KEEPALIVEPING     // Supports ping
   WDIOF_PRETIMEOUT        // Supports pretimeout
   WDIOF_ALARMONLY         // Alarm only, no reset

Watchdog Device Structure
==========================

Basic Structure
---------------

.. code-block:: c

   struct watchdog_device {
       int id;
       struct device *parent;
       const struct watchdog_info *info;
       const struct watchdog_ops *ops;
       const struct watchdog_governor *gov;
       unsigned int bootstatus;
       unsigned int timeout;      // Current timeout (seconds)
       unsigned int pretimeout;   // Pretimeout (seconds)
       unsigned int min_timeout;
       unsigned int max_timeout;
       unsigned int min_hw_heartbeat_ms;
       unsigned int max_hw_heartbeat_ms;
       struct notifier_block reboot_nb;
       struct notifier_block restart_nb;
       void *driver_data;
       unsigned long status;
   };

Watchdog Operations
-------------------

.. code-block:: c

   struct watchdog_ops {
       struct module *owner;
       int (*start)(struct watchdog_device *);
       int (*stop)(struct watchdog_device *);
       int (*ping)(struct watchdog_device *);
       unsigned int (*status)(struct watchdog_device *);
       int (*set_timeout)(struct watchdog_device *, unsigned int);
       int (*set_pretimeout)(struct watchdog_device *, unsigned int);
       unsigned int (*get_timeleft)(struct watchdog_device *);
       int (*restart)(struct watchdog_device *, unsigned long, void *);
       long (*ioctl)(struct watchdog_device *, unsigned int, unsigned long);
   };

Creating Watchdog Driver
=========================

Platform Watchdog Driver
------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/watchdog.h>
   #include <linux/io.h>
   #include <linux/clk.h>
   #include <linux/of.h>
   
   #define WDT_CTRL_REG    0x00
   #define WDT_TIMEOUT_REG 0x04
   #define WDT_COUNTER_REG 0x08
   #define WDT_KICK_REG    0x0C
   
   #define WDT_ENABLE      BIT(0)
   #define WDT_RESET_EN    BIT(1)
   #define WDT_IRQ_EN      BIT(2)
   
   #define WDT_KICK_VALUE  0x5555AAAA
   
   struct mywdt_data {
       struct watchdog_device wdd;
       void __iomem *regs;
       struct clk *clk;
       unsigned long clk_rate;
       spinlock_t lock;
   };
   
   static int mywdt_start(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       unsigned long flags;
       u32 ctrl;
       
       spin_lock_irqsave(&data->lock, flags);
       
       ctrl = readl(data->regs + WDT_CTRL_REG);
       ctrl |= WDT_ENABLE | WDT_RESET_EN;
       writel(ctrl, data->regs + WDT_CTRL_REG);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       return 0;
   }
   
   static int mywdt_stop(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       unsigned long flags;
       u32 ctrl;
       
       spin_lock_irqsave(&data->lock, flags);
       
       ctrl = readl(data->regs + WDT_CTRL_REG);
       ctrl &= ~WDT_ENABLE;
       writel(ctrl, data->regs + WDT_CTRL_REG);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       return 0;
   }
   
   static int mywdt_ping(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       unsigned long flags;
       
       spin_lock_irqsave(&data->lock, flags);
       writel(WDT_KICK_VALUE, data->regs + WDT_KICK_REG);
       spin_unlock_irqrestore(&data->lock, flags);
       
       return 0;
   }
   
   static int mywdt_set_timeout(struct watchdog_device *wdd,
                                 unsigned int timeout) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       unsigned long flags;
       u32 timeout_ticks;
       
       /* Convert seconds to hardware ticks */
       timeout_ticks = timeout * data->clk_rate;
       
       spin_lock_irqsave(&data->lock, flags);
       writel(timeout_ticks, data->regs + WDT_TIMEOUT_REG);
       spin_unlock_irqrestore(&data->lock, flags);
       
       wdd->timeout = timeout;
       
       return 0;
   }
   
   static unsigned int mywdt_get_timeleft(struct watchdog_device *wdd) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       unsigned long flags;
       u32 counter;
       
       spin_lock_irqsave(&data->lock, flags);
       counter = readl(data->regs + WDT_COUNTER_REG);
       spin_unlock_irqrestore(&data->lock, flags);
       
       /* Convert ticks to seconds */
       return counter / data->clk_rate;
   }
   
   static int mywdt_restart(struct watchdog_device *wdd,
                             unsigned long action, void *data) {
       struct mywdt_data *wdt_data = watchdog_get_drvdata(wdd);
       
       /* Set very short timeout and start */
       writel(1, wdt_data->regs + WDT_TIMEOUT_REG);
       writel(WDT_ENABLE | WDT_RESET_EN, wdt_data->regs + WDT_CTRL_REG);
       
       /* Wait for reset */
       mdelay(1000);
       
       return 0;
   }
   
   static const struct watchdog_ops mywdt_ops = {
       .owner = THIS_MODULE,
       .start = mywdt_start,
       .stop = mywdt_stop,
       .ping = mywdt_ping,
       .set_timeout = mywdt_set_timeout,
       .get_timeleft = mywdt_get_timeleft,
       .restart = mywdt_restart,
   };
   
   static const struct watchdog_info mywdt_info = {
       .options = WDIOF_SETTIMEOUT | WDIOF_KEEPALIVEPING |
                   WDIOF_MAGICCLOSE,
       .identity = "My Watchdog Timer",
   };
   
   static int mywdt_probe(struct platform_device *pdev) {
       struct mywdt_data *data;
       struct resource *res;
       int ret;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       /* Map registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       data->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(data->regs))
           return PTR_ERR(data->regs);
       
       /* Get clock */
       data->clk = devm_clk_get(&pdev->dev, NULL);
       if (IS_ERR(data->clk))
           return PTR_ERR(data->clk);
       
       ret = clk_prepare_enable(data->clk);
       if (ret)
           return ret;
       
       data->clk_rate = clk_get_rate(data->clk);
       
       spin_lock_init(&data->lock);
       platform_set_drvdata(pdev, data);
       
       /* Setup watchdog device */
       data->wdd.info = &mywdt_info;
       data->wdd.ops = &mywdt_ops;
       data->wdd.min_timeout = 1;
       data->wdd.max_timeout = 0xFFFFFFFF / data->clk_rate;
       data->wdd.timeout = 30;  // Default 30 seconds
       data->wdd.parent = &pdev->dev;
       
       watchdog_set_drvdata(&data->wdd, data);
       watchdog_set_restart_priority(&data->wdd, 128);
       
       /* Stop watchdog initially */
       mywdt_stop(&data->wdd);
       
       /* Register watchdog */
       ret = devm_watchdog_register_device(&pdev->dev, &data->wdd);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register watchdog: %d\n", ret);
           clk_disable_unprepare(data->clk);
           return ret;
       }
       
       dev_info(&pdev->dev, "Watchdog registered (timeout=%us)\n",
                data->wdd.timeout);
       
       return 0;
   }
   
   static int mywdt_remove(struct platform_device *pdev) {
       struct mywdt_data *data = platform_get_drvdata(pdev);
       
       clk_disable_unprepare(data->clk);
       return 0;
   }
   
   static const struct of_device_id mywdt_of_match[] = {
       { .compatible = "vendor,watchdog", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mywdt_of_match);
   
   static struct platform_driver mywdt_driver = {
       .driver = {
           .name = "mywatchdog",
           .of_match_table = mywdt_of_match,
       },
       .probe = mywdt_probe,
       .remove = mywdt_remove,
   };
   
   module_platform_driver(mywdt_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Watchdog Timer Driver");

Advanced Features
=================

Pretimeout Support
------------------

.. code-block:: c

   static irqreturn_t mywdt_pretimeout_irq(int irq, void *data) {
       struct mywdt_data *wdt_data = data;
       
       /* Notify watchdog core of pretimeout */
       watchdog_notify_pretimeout(&wdt_data->wdd);
       
       return IRQ_HANDLED;
   }
   
   static int mywdt_set_pretimeout(struct watchdog_device *wdd,
                                    unsigned int pretimeout) {
       struct mywdt_data *data = watchdog_get_drvdata(wdd);
       u32 pretimeout_ticks;
       
       if (pretimeout >= wdd->timeout)
           return -EINVAL;
       
       pretimeout_ticks = pretimeout * data->clk_rate;
       writel(pretimeout_ticks, data->regs + WDT_PRETIMEOUT_REG);
       
       wdd->pretimeout = pretimeout;
       
       return 0;
   }
   
   /* Add to ops */
   .set_pretimeout = mywdt_set_pretimeout,
   
   /* Add to info options */
   .options = ... | WDIOF_PRETIMEOUT,
   
   /* In probe, register IRQ */
   ret = devm_request_irq(&pdev->dev, irq, mywdt_pretimeout_irq,
                           0, "watchdog-pretimeout", data);

Watchdog Helpers
----------------

.. code-block:: c

   /* Set driver data */
   watchdog_set_drvdata(wdd, data);
   void *data = watchdog_get_drvdata(wdd);
   
   /* Set restart priority (0-255, higher = more important) */
   watchdog_set_restart_priority(wdd, 128);
   
   /* Set nowayout (cannot disable once started) */
   watchdog_set_nowayout(wdd, true);
   
   /* Init watchdog timeout from DT */
   watchdog_init_timeout(wdd, 0, &pdev->dev);

Kernel Ping Support
-------------------

.. code-block:: c

   /* Enable automatic kernel pinging */
   set_bit(WDOG_HW_RUNNING, &wdd->status);
   
   /* Set maximum heartbeat time */
   wdd->max_hw_heartbeat_ms = 2000;  // 2 seconds max
   
   /* Watchdog core will ping automatically if userspace doesn't */

Userspace Interface
===================

Using Watchdog from Userspace
------------------------------

.. code-block:: c

   #include <stdio.h>
   #include <stdlib.h>
   #include <unistd.h>
   #include <fcntl.h>
   #include <sys/ioctl.h>
   #include <linux/watchdog.h>
   
   int main(void) {
       int fd;
       int timeout = 30;
       int ret;
       
       /* Open watchdog device */
       fd = open("/dev/watchdog", O_WRONLY);
       if (fd < 0) {
           perror("open");
           return 1;
       }
       
       /* Set timeout */
       ret = ioctl(fd, WDIOC_SETTIMEOUT, &timeout);
       if (ret) {
           perror("WDIOC_SETTIMEOUT");
       }
       printf("Watchdog timeout set to %d seconds\n", timeout);
       
       /* Ping loop */
       while (1) {
           ret = ioctl(fd, WDIOC_KEEPALIVE, NULL);
           if (ret) {
               perror("WDIOC_KEEPALIVE");
               break;
           }
           printf("Ping sent\n");
           sleep(10);  // Sleep less than timeout
       }
       
       /* Magic close */
       write(fd, "V", 1);
       close(fd);
       
       return 0;
   }

IOCTL Commands
--------------

.. code-block:: c

   /* Get info */
   struct watchdog_info info;
   ioctl(fd, WDIOC_GETSUPPORT, &info);
   
   /* Get/set timeout */
   int timeout = 30;
   ioctl(fd, WDIOC_SETTIMEOUT, &timeout);
   ioctl(fd, WDIOC_GETTIMEOUT, &timeout);
   
   /* Get time left */
   int timeleft;
   ioctl(fd, WDIOC_GETTIMELEFT, &timeleft);
   
   /* Ping/keepalive */
   ioctl(fd, WDIOC_KEEPALIVE, NULL);
   
   /* Get boot status */
   int bootstatus;
   ioctl(fd, WDIOC_GETBOOTSTATUS, &bootstatus);
   
   /* Set pretimeout */
   int pretimeout = 5;
   ioctl(fd, WDIOC_SETPRETIMEOUT, &pretimeout);

Sysfs Interface
---------------

.. code-block:: bash

   # Check status
   cat /sys/class/watchdog/watchdog0/state
   cat /sys/class/watchdog/watchdog0/timeout
   cat /sys/class/watchdog/watchdog0/timeleft
   cat /sys/class/watchdog/watchdog0/bootstatus
   cat /sys/class/watchdog/watchdog0/nowayout
   
   # Get info
   cat /sys/class/watchdog/watchdog0/identity

Device Tree Binding
====================

.. code-block:: dts

   watchdog@40010000 {
       compatible = "vendor,watchdog";
       reg = <0x40010000 0x1000>;
       clocks = <&clk_wdt>;
       interrupts = <0 24 IRQ_TYPE_EDGE_RISING>;
       timeout-sec = <30>;
   };

Parsing DT in Driver
---------------------

.. code-block:: c

   static int mywdt_probe(struct platform_device *pdev) {
       struct device_node *np = pdev->dev.of_node;
       u32 timeout;
       
       /* ... */
       
       /* Get timeout from DT */
       if (of_property_read_u32(np, "timeout-sec", &timeout) == 0) {
           data->wdd.timeout = timeout;
       }
       
       /* Check for nowayout */
       if (of_property_read_bool(np, "nowayout")) {
           watchdog_set_nowayout(&data->wdd, true);
       }
       
       /* ... */
   }

Best Practices
==============

1. **Use devm_watchdog_register_device()** for cleanup
2. **Set proper min/max timeout** values
3. **Implement restart handler** for system reboot
4. **Support magic close** if hardware allows
5. **Calculate timeouts** from clock rate
6. **Protect register access** with spinlock
7. **Handle pretimeout** for early warning
8. **Test thoroughly** (don't brick hardware!)
9. **Document hardware** quirks
10. **Set proper restart priority**

Common Pitfalls
===============

1. **Not disabling** watchdog on module unload
2. **Incorrect timeout** calculation
3. **Missing nowayout** handling
4. **Race conditions** in register access
5. **Not testing** actual reset behavior
6. **Wrong clock** selection

Testing Watchdog
================

.. code-block:: bash

   # Simple test
   cat > /dev/watchdog  # Start watchdog
   # Wait for timeout - system should reset
   
   # Ping test
   while true; do
       echo 1 > /dev/watchdog
       sleep 5
   done
   
   # Check if running
   cat /sys/class/watchdog/watchdog0/state
   
   # Get timeout
   cat /sys/class/watchdog/watchdog0/timeout
   
   # Trigger reset
   echo 1 > /dev/watchdog
   # Stop pinging - system resets after timeout

Debugging
=========

.. code-block:: bash

   # List watchdog devices
   ls /dev/watchdog*
   
   # Check sysfs
   ls /sys/class/watchdog/
   
   # View watchdog info
   cat /sys/class/watchdog/watchdog0/identity
   cat /sys/class/watchdog/watchdog0/state
   cat /sys/class/watchdog/watchdog0/timeout
   
   # Test with wdctl
   wdctl
   wdctl /dev/watchdog0

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Driver_IRQ_Handling.rst
- Linux_Device_Tree_Drivers.rst

References
==========

- Documentation/watchdog/watchdog-api.rst
- Documentation/watchdog/watchdog-kernel-api.rst
- include/linux/watchdog.h
