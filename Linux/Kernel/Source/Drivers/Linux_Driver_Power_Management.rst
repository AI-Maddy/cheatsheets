=========================================
Linux Driver Power Management Guide
=========================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

System Sleep PM
---------------

.. code-block:: c

   static int mydev_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       /* Save state */
       data->saved_state = readl(data->regs + CTRL_REG);
       
       /* Disable device */
       mydev_disable(data);
       
       return 0;
   }
   
   static int mydev_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       /* Restore state */
       writel(data->saved_state, data->regs + CTRL_REG);
       
       /* Re-enable device */
       mydev_enable(data);
       
       return 0;
   }
   
   static SIMPLE_DEV_PM_OPS(mydev_pm_ops, mydev_suspend, mydev_resume);
   
   static struct platform_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .pm = &mydev_pm_ops,
       },
   };

Runtime PM
----------

.. code-block:: c

   #include <linux/pm_runtime.h>
   
   static int mydev_runtime_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       /* Turn off clocks/power */
       clk_disable_unprepare(data->clk);
       
       return 0;
   }
   
   static int mydev_runtime_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       /* Turn on clocks/power */
       return clk_prepare_enable(data->clk);
   }
   
   static const struct dev_pm_ops mydev_pm_ops = {
       SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                          mydev_runtime_resume, NULL)
       SET_SYSTEM_SLEEP_PM_OPS(mydev_suspend, mydev_resume)
   };
   
   /* In probe */
   pm_runtime_enable(&pdev->dev);
   
   /* Use device */
   pm_runtime_get_sync(&pdev->dev);
   // ... use device ...
   pm_runtime_put(&pdev->dev);

Power Management Overview
==========================

PM Types
--------

**System Sleep:**

- Suspend to RAM (S3)
- Hibernate (S4)
- Freeze
- Standby

**Runtime PM:**

- Dynamic device power state
- Automatic power down when idle
- On-demand activation

**Frequency Scaling:**

- DVFS (Dynamic Voltage and Frequency Scaling)
- CPU frequency governors

System Sleep PM
===============

dev_pm_ops Structure
--------------------

.. code-block:: c

   struct dev_pm_ops {
       int (*prepare)(struct device *dev);
       void (*complete)(struct device *dev);
       int (*suspend)(struct device *dev);
       int (*resume)(struct device *dev);
       int (*freeze)(struct device *dev);
       int (*thaw)(struct device *dev);
       int (*poweroff)(struct device *dev);
       int (*restore)(struct device *dev);
       int (*suspend_late)(struct device *dev);
       int (*resume_early)(struct device *dev);
       int (*freeze_late)(struct device *dev);
       int (*thaw_early)(struct device *dev);
       int (*poweroff_late)(struct device *dev);
       int (*restore_early)(struct device *dev);
       int (*suspend_noirq)(struct device *dev);
       int (*resume_noirq)(struct device *dev);
       int (*freeze_noirq)(struct device *dev);
       int (*thaw_noirq)(struct device *dev);
       int (*poweroff_noirq)(struct device *dev);
       int (*restore_noirq)(struct device *dev);
   };

Basic Suspend/Resume
--------------------

.. code-block:: c

   static int mydev_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       unsigned long flags;
       
       /* Stop any ongoing activity */
       cancel_work_sync(&data->work);
       
       spin_lock_irqsave(&data->lock, flags);
       
       /* Save device state */
       data->saved_ctrl = readl(data->regs + CTRL_REG);
       data->saved_config = readl(data->regs + CONFIG_REG);
       
       /* Disable device */
       writel(0, data->regs + CTRL_REG);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       /* Disable clocks */
       clk_disable_unprepare(data->clk);
       
       return 0;
   }
   
   static int mydev_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       unsigned long flags;
       int ret;
       
       /* Enable clocks */
       ret = clk_prepare_enable(data->clk);
       if (ret)
           return ret;
       
       spin_lock_irqsave(&data->lock, flags);
       
       /* Restore device state */
       writel(data->saved_config, data->regs + CONFIG_REG);
       writel(data->saved_ctrl, data->regs + CTRL_REG);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       /* Resume operations */
       schedule_work(&data->work);
       
       return 0;
   }

PM Macros
---------

.. code-block:: c

   /* Simple PM ops (suspend/resume only) */
   static SIMPLE_DEV_PM_OPS(mydev_pm_ops, mydev_suspend, mydev_resume);
   
   /* Define PM ops conditionally */
   static DEFINE_SIMPLE_DEV_PM_OPS(mydev_pm_ops, mydev_suspend, mydev_resume);
   
   /* Set system sleep ops */
   SET_SYSTEM_SLEEP_PM_OPS(mydev_suspend, mydev_resume)
   
   /* Set runtime PM ops */
   SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                      mydev_runtime_resume,
                      NULL)
   
   /* Combined */
   static const struct dev_pm_ops mydev_pm_ops = {
       SET_SYSTEM_SLEEP_PM_OPS(mydev_suspend, mydev_resume)
       SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                          mydev_runtime_resume, NULL)
   };

Runtime PM
==========

Runtime PM Functions
--------------------

.. code-block:: c

   #include <linux/pm_runtime.h>
   
   /* Increment usage count and resume device */
   int pm_runtime_get_sync(struct device *dev);
   
   /* Async version */
   int pm_runtime_get(struct device *dev);
   
   /* Decrement usage count, may suspend */
   int pm_runtime_put(struct device *dev);
   
   /* Decrement and auto-suspend */
   int pm_runtime_put_autosuspend(struct device *dev);
   
   /* Enable runtime PM */
   void pm_runtime_enable(struct device *dev);
   
   /* Disable runtime PM */
   void pm_runtime_disable(struct device *dev);
   
   /* Set autosuspend delay (milliseconds) */
   void pm_runtime_set_autosuspend_delay(struct device *dev, int delay);
   
   /* Use autosuspend */
   void pm_runtime_use_autosuspend(struct device *dev);
   
   /* Mark device as active */
   void pm_runtime_set_active(struct device *dev);
   
   /* Mark device as suspended */
   void pm_runtime_set_suspended(struct device *dev);

Runtime PM Implementation
-------------------------

.. code-block:: c

   static int mydev_runtime_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       dev_dbg(dev, "Runtime suspend\n");
       
       /* Disable clocks to save power */
       clk_disable_unprepare(data->clk);
       
       /* May turn off regulators */
       regulator_disable(data->vdd);
       
       return 0;
   }
   
   static int mydev_runtime_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       int ret;
       
       dev_dbg(dev, "Runtime resume\n");
       
       /* Turn on regulators */
       ret = regulator_enable(data->vdd);
       if (ret)
           return ret;
       
       /* Enable clocks */
       ret = clk_prepare_enable(data->clk);
       if (ret) {
           regulator_disable(data->vdd);
           return ret;
       }
       
       return 0;
   }
   
   static const struct dev_pm_ops mydev_pm_ops = {
       SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                          mydev_runtime_resume, NULL)
   };

Using Runtime PM
----------------

.. code-block:: c

   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       int ret;
       
       /* ... allocation and setup ... */
       
       /* Enable runtime PM */
       pm_runtime_enable(&pdev->dev);
       
       /* Set autosuspend delay (2 seconds) */
       pm_runtime_set_autosuspend_delay(&pdev->dev, 2000);
       pm_runtime_use_autosuspend(&pdev->dev);
       
       /* Initially active */
       pm_runtime_set_active(&pdev->dev);
       pm_runtime_get_noresume(&pdev->dev);
       
       /* ... */
       
       pm_runtime_put(&pdev->dev);
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       /* Disable runtime PM */
       pm_runtime_disable(&pdev->dev);
       pm_runtime_set_suspended(&pdev->dev);
       
       /* ... */
       return 0;
   }
   
   static int mydev_do_work(struct mydev_data *data) {
       int ret;
       
       /* Resume device before use */
       ret = pm_runtime_get_sync(data->dev);
       if (ret < 0) {
           pm_runtime_put_noidle(data->dev);
           return ret;
       }
       
       /* Use device */
       mydev_perform_operation(data);
       
       /* Allow suspend */
       pm_runtime_mark_last_busy(data->dev);
       pm_runtime_put_autosuspend(data->dev);
       
       return 0;
   }

Complete Driver Example
========================

Driver with Full PM Support
----------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/pm_runtime.h>
   #include <linux/clk.h>
   #include <linux/regulator/consumer.h>
   #include <linux/io.h>
   
   struct mydev_data {
       struct device *dev;
       void __iomem *regs;
       struct clk *clk;
       struct regulator *vdd;
       
       /* Saved state for system PM */
       u32 saved_ctrl;
       u32 saved_config;
       
       spinlock_t lock;
       struct work_struct work;
   };
   
   static int mydev_hw_init(struct mydev_data *data) {
       /* Initialize hardware */
       writel(0x01, data->regs + CTRL_REG);
       writel(0xFF, data->regs + CONFIG_REG);
       return 0;
   }
   
   /* System PM */
   static int mydev_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       dev_dbg(dev, "System suspend\n");
       
       /* Cancel pending work */
       cancel_work_sync(&data->work);
       
       /* Save state */
       data->saved_ctrl = readl(data->regs + CTRL_REG);
       data->saved_config = readl(data->regs + CONFIG_REG);
       
       /* Disable hardware */
       writel(0, data->regs + CTRL_REG);
       
       /* Runtime PM handles clock/regulator if active */
       if (!pm_runtime_status_suspended(dev)) {
           clk_disable_unprepare(data->clk);
           regulator_disable(data->vdd);
       }
       
       return 0;
   }
   
   static int mydev_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       int ret;
       
       dev_dbg(dev, "System resume\n");
       
       if (!pm_runtime_status_suspended(dev)) {
           ret = regulator_enable(data->vdd);
           if (ret)
               return ret;
           
           ret = clk_prepare_enable(data->clk);
           if (ret) {
               regulator_disable(data->vdd);
               return ret;
           }
       }
       
       /* Restore state */
       writel(data->saved_config, data->regs + CONFIG_REG);
       writel(data->saved_ctrl, data->regs + CTRL_REG);
       
       return 0;
   }
   
   /* Runtime PM */
   static int mydev_runtime_suspend(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       
       dev_dbg(dev, "Runtime suspend\n");
       
       clk_disable_unprepare(data->clk);
       regulator_disable(data->vdd);
       
       return 0;
   }
   
   static int mydev_runtime_resume(struct device *dev) {
       struct mydev_data *data = dev_get_drvdata(dev);
       int ret;
       
       dev_dbg(dev, "Runtime resume\n");
       
       ret = regulator_enable(data->vdd);
       if (ret)
           return ret;
       
       ret = clk_prepare_enable(data->clk);
       if (ret) {
           regulator_disable(data->vdd);
           return ret;
       }
       
       return 0;
   }
   
   static const struct dev_pm_ops mydev_pm_ops = {
       SET_SYSTEM_SLEEP_PM_OPS(mydev_suspend, mydev_resume)
       SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                          mydev_runtime_resume, NULL)
   };
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       struct resource *res;
       int ret;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       data->dev = &pdev->dev;
       platform_set_drvdata(pdev, data);
       spin_lock_init(&data->lock);
       
       /* Map registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       data->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(data->regs))
           return PTR_ERR(data->regs);
       
       /* Get clock */
       data->clk = devm_clk_get(&pdev->dev, NULL);
       if (IS_ERR(data->clk))
           return PTR_ERR(data->clk);
       
       /* Get regulator */
       data->vdd = devm_regulator_get(&pdev->dev, "vdd");
       if (IS_ERR(data->vdd))
           return PTR_ERR(data->vdd);
       
       /* Enable power */
       ret = regulator_enable(data->vdd);
       if (ret)
           return ret;
       
       ret = clk_prepare_enable(data->clk);
       if (ret)
           goto err_regulator;
       
       /* Initialize hardware */
       ret = mydev_hw_init(data);
       if (ret)
           goto err_clk;
       
       /* Setup runtime PM */
       pm_runtime_set_active(&pdev->dev);
       pm_runtime_enable(&pdev->dev);
       pm_runtime_set_autosuspend_delay(&pdev->dev, 2000);
       pm_runtime_use_autosuspend(&pdev->dev);
       
       dev_info(&pdev->dev, "Device initialized\n");
       return 0;
       
   err_clk:
       clk_disable_unprepare(data->clk);
   err_regulator:
       regulator_disable(data->vdd);
       return ret;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_data *data = platform_get_drvdata(pdev);
       
       pm_runtime_disable(&pdev->dev);
       
       if (!pm_runtime_status_suspended(&pdev->dev)) {
           clk_disable_unprepare(data->clk);
           regulator_disable(data->vdd);
       }
       
       pm_runtime_set_suspended(&pdev->dev);
       
       return 0;
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,device", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct platform_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
           .pm = &mydev_pm_ops,
       },
       .probe = mydev_probe,
       .remove = mydev_remove,
   };
   
   module_platform_driver(mydev_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Device Driver with PM Support");

Wakeup Sources
==============

.. code-block:: c

   /* Enable wakeup */
   device_init_wakeup(&pdev->dev, true);
   
   /* In suspend */
   if (device_may_wakeup(dev))
       enable_irq_wake(data->irq);
   
   /* In resume */
   if (device_may_wakeup(dev))
       disable_irq_wake(data->irq);
   
   /* Report wakeup event */
   pm_wakeup_event(dev, 0);

Best Practices
==============

1. **Use runtime PM** for automatic power management
2. **Implement both system and runtime PM**
3. **Use autosuspend** to avoid thrashing
4. **Save minimal state** in suspend
5. **Handle PM in probe/remove**
6. **Test PM transitions** thoroughly
7. **Use pm_runtime_get_sync()** before HW access
8. **Always pair get/put** calls
9. **Handle errors** in PM callbacks
10. **Document power states**

Common Pitfalls
===============

1. **Forgetting pm_runtime_put()**
2. **Accessing HW** without pm_runtime_get()
3. **Not handling PM** in probe/remove
4. **Race conditions** with PM state
5. **Missing pm_runtime_enable()**
6. **Not testing** all PM paths

Debugging
=========

.. code-block:: bash

   # Check PM status
   cat /sys/devices/.../power/runtime_status
   cat /sys/devices/.../power/runtime_active_time
   cat /sys/devices/.../power/runtime_suspended_time
   
   # Control PM
   echo auto > /sys/devices/.../power/control
   echo on > /sys/devices/.../power/control
   
   # Enable PM debug
   echo 1 > /sys/power/pm_debug_messages
   echo 8 > /proc/sys/kernel/printk
   
   # Test suspend
   echo mem > /sys/power/state

See Also
========

- Linux_Platform_Drivers.rst
- Linux_Regulator_API.rst
- Linux_Clock_Framework.rst

References
==========

- Documentation/driver-api/pm/
- Documentation/power/runtime_pm.rst
- include/linux/pm_runtime.h
