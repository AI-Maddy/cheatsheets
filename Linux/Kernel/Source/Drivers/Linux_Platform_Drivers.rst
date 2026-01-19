======================================
Linux Platform Drivers Guide
======================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Platform Driver
---------------------

.. code-block:: c

   #include <linux/platform_device.h>
   #include <linux/module.h>
   #include <linux/mod_devicetable.h>
   
   static int my_probe(struct platform_device *pdev) {
       dev_info(&pdev->dev, "Probing device\n");
       
       /* Get resources */
       struct resource *res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       void __iomem *base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(base))
           return PTR_ERR(base);
       
       /* Get IRQ */
       int irq = platform_get_irq(pdev, 0);
       if (irq < 0)
           return irq;
       
       return 0;
   }
   
   static int my_remove(struct platform_device *pdev) {
       dev_info(&pdev->dev, "Removing device\n");
       return 0;
   }
   
   static const struct of_device_id my_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { },
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

Platform Device Fundamentals
=============================

Introduction
------------

Platform devices represent devices that are not discoverable by hardware enumeration (unlike PCI or USB). They are typically described in device tree or board files.

**Examples:**
- On-chip peripherals (UART, I2C, SPI controllers)
- Memory-mapped devices
- GPIO controllers
- Watchdog timers

**Key Components:**

- **platform_device:** Represents the device hardware
- **platform_driver:** Driver that handles the device
- **Resources:** Memory, IRQs, DMA channels
- **Device Tree:** Hardware description

Platform Driver Structure
=========================

struct platform_driver
-----------------------

.. code-block:: c

   struct platform_driver {
       int (*probe)(struct platform_device *);
       int (*remove)(struct platform_device *);
       void (*shutdown)(struct platform_device *);
       int (*suspend)(struct platform_device *, pm_message_t state);
       int (*resume)(struct platform_device *);
       struct device_driver driver;
       const struct platform_device_id *id_table;
   };

Probe Function
--------------

.. code-block:: c

   static int mydev_probe(struct platform_device *pdev) {
       struct device *dev = &pdev->dev;
       struct mydev_priv *priv;
       int ret;
       
       dev_info(dev, "Probing %s\n", pdev->name);
       
       /* Allocate private data */
       priv = devm_kzalloc(dev, sizeof(*priv), GFP_KERNEL);
       if (!priv)
           return -ENOMEM;
       
       /* Store private data */
       platform_set_drvdata(pdev, priv);
       priv->dev = dev;
       
       /* Initialize device */
       ret = mydev_hw_init(priv);
       if (ret)
           return ret;
       
       dev_info(dev, "Successfully probed\n");
       return 0;
   }

Remove Function
---------------

.. code-block:: c

   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_priv *priv = platform_get_drvdata(pdev);
       
       dev_info(&pdev->dev, "Removing device\n");
       
       /* Cleanup device */
       mydev_hw_shutdown(priv);
       
       /* devm_* resources automatically freed */
       
       return 0;
   }

Device Resources
================

Getting Memory Resources
------------------------

.. code-block:: c

   static int get_memory_resources(struct platform_device *pdev) {
       struct resource *res;
       void __iomem *base;
       resource_size_t size;
       
       /* Get memory resource */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       if (!res) {
           dev_err(&pdev->dev, "No memory resource\n");
           return -ENODEV;
       }
       
       size = resource_size(res);
       dev_info(&pdev->dev, "Memory: 0x%llx - 0x%llx (size: %llu)\n",
                res->start, res->end, size);
       
       /* Map memory - automatically unmapped on remove */
       base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(base))
           return PTR_ERR(base);
       
       /* Use base for register access */
       writel(0x1234, base + SOME_REGISTER);
       
       return 0;
   }

Getting IRQ Resources
---------------------

.. code-block:: c

   static irqreturn_t mydev_irq_handler(int irq, void *dev_id) {
       struct mydev_priv *priv = dev_id;
       
       /* Handle interrupt */
       dev_dbg(priv->dev, "Interrupt received\n");
       
       return IRQ_HANDLED;
   }
   
   static int setup_irq(struct platform_device *pdev,
                        struct mydev_priv *priv) {
       int irq, ret;
       
       /* Get IRQ number */
       irq = platform_get_irq(pdev, 0);
       if (irq < 0) {
           dev_err(&pdev->dev, "No IRQ resource\n");
           return irq;
       }
       
       priv->irq = irq;
       
       /* Request IRQ - automatically freed on remove */
       ret = devm_request_irq(&pdev->dev, irq, mydev_irq_handler,
                              IRQF_SHARED, dev_name(&pdev->dev), priv);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ %d\n", irq);
           return ret;
       }
       
       dev_info(&pdev->dev, "IRQ %d registered\n", irq);
       return 0;
   }

Multiple Resources
------------------

.. code-block:: c

   static int get_multiple_resources(struct platform_device *pdev) {
       struct resource *res;
       void __iomem *reg_base, *ctrl_base;
       int i;
       
       /* Get first memory region */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       reg_base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(reg_base))
           return PTR_ERR(reg_base);
       
       /* Get second memory region */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 1);
       ctrl_base = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(ctrl_base))
           return PTR_ERR(ctrl_base);
       
       /* Get all IRQs */
       for (i = 0; ; i++) {
           int irq = platform_get_irq(pdev, i);
           if (irq < 0)
               break;
           dev_info(&pdev->dev, "IRQ %d: %d\n", i, irq);
       }
       
       return 0;
   }

Device Tree Integration
=======================

OF Match Table
--------------

.. code-block:: c

   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,device-v1", },
       { .compatible = "vendor,device-v2", },
       { },
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct platform_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
   };

Reading Device Tree Properties
-------------------------------

.. code-block:: c

   #include <linux/of.h>
   #include <linux/of_device.h>
   
   static int read_dt_properties(struct platform_device *pdev) {
       struct device_node *np = pdev->dev.of_node;
       u32 value;
       const char *string;
       int ret;
       
       if (!np) {
           dev_err(&pdev->dev, "No device tree node\n");
           return -ENODEV;
       }
       
       /* Read u32 property */
       ret = of_property_read_u32(np, "reg-width", &value);
       if (ret == 0)
           dev_info(&pdev->dev, "reg-width = %u\n", value);
       
       /* Read string property */
       ret = of_property_read_string(np, "label", &string);
       if (ret == 0)
           dev_info(&pdev->dev, "label = %s\n", string);
       
       /* Check boolean property */
       if (of_property_read_bool(np, "enable-feature"))
           dev_info(&pdev->dev, "Feature enabled\n");
       
       /* Read array */
       u32 array[4];
       ret = of_property_read_u32_array(np, "config", array, 4);
       if (ret == 0) {
           dev_info(&pdev->dev, "Config: %u %u %u %u\n",
                    array[0], array[1], array[2], array[3]);
       }
       
       return 0;
   }

Getting Clock from DT
---------------------

.. code-block:: c

   #include <linux/clk.h>
   
   struct mydev_priv {
       struct clk *clk;
       unsigned long clk_rate;
   };
   
   static int setup_clock(struct platform_device *pdev,
                          struct mydev_priv *priv) {
       int ret;
       
       /* Get clock - automatically released on remove */
       priv->clk = devm_clk_get(&pdev->dev, "functional");
       if (IS_ERR(priv->clk)) {
           dev_err(&pdev->dev, "Failed to get clock\n");
           return PTR_ERR(priv->clk);
       }
       
       /* Prepare and enable clock */
       ret = clk_prepare_enable(priv->clk);
       if (ret) {
           dev_err(&pdev->dev, "Failed to enable clock\n");
           return ret;
       }
       
       priv->clk_rate = clk_get_rate(priv->clk);
       dev_info(&pdev->dev, "Clock rate: %lu Hz\n", priv->clk_rate);
       
       return 0;
   }
   
   static void shutdown_clock(struct mydev_priv *priv) {
       clk_disable_unprepare(priv->clk);
   }

Getting GPIO from DT
--------------------

.. code-block:: c

   #include <linux/gpio/consumer.h>
   
   static int setup_gpios(struct platform_device *pdev,
                          struct mydev_priv *priv) {
       struct gpio_desc *reset_gpio;
       
       /* Get GPIO descriptor - automatically freed on remove */
       reset_gpio = devm_gpiod_get(&pdev->dev, "reset", GPIOD_OUT_HIGH);
       if (IS_ERR(reset_gpio)) {
           dev_err(&pdev->dev, "Failed to get reset GPIO\n");
           return PTR_ERR(reset_gpio);
       }
       
       priv->reset_gpio = reset_gpio;
       
       /* Toggle reset */
       gpiod_set_value(reset_gpio, 0);
       msleep(10);
       gpiod_set_value(reset_gpio, 1);
       
       return 0;
   }

Regulator Support
-----------------

.. code-block:: c

   #include <linux/regulator/consumer.h>
   
   static int setup_regulators(struct platform_device *pdev,
                                struct mydev_priv *priv) {
       int ret;
       
       /* Get regulator - automatically released on remove */
       priv->vdd = devm_regulator_get(&pdev->dev, "vdd");
       if (IS_ERR(priv->vdd)) {
           dev_err(&pdev->dev, "Failed to get VDD regulator\n");
           return PTR_ERR(priv->vdd);
       }
       
       /* Set voltage */
       ret = regulator_set_voltage(priv->vdd, 3300000, 3300000);
       if (ret) {
           dev_err(&pdev->dev, "Failed to set voltage\n");
           return ret;
       }
       
       /* Enable regulator */
       ret = regulator_enable(priv->vdd);
       if (ret) {
           dev_err(&pdev->dev, "Failed to enable regulator\n");
           return ret;
       }
       
       return 0;
   }

Devm Resource Management
=========================

Advantages of devm_*
--------------------

Resources allocated with ``devm_*`` functions are automatically freed when the device is removed or probe fails.

.. code-block:: c

   static int mydev_probe_with_devm(struct platform_device *pdev) {
       struct mydev_priv *priv;
       void __iomem *base;
       int irq, ret;
       
       /* All these are automatically freed on error or remove */
       
       priv = devm_kzalloc(&pdev->dev, sizeof(*priv), GFP_KERNEL);
       if (!priv)
           return -ENOMEM;
       
       base = devm_platform_ioremap_resource(pdev, 0);
       if (IS_ERR(base))
           return PTR_ERR(base);
       
       irq = platform_get_irq(pdev, 0);
       if (irq < 0)
           return irq;
       
       ret = devm_request_irq(&pdev->dev, irq, mydev_irq_handler,
                              0, dev_name(&pdev->dev), priv);
       if (ret)
           return ret;
       
       priv->clk = devm_clk_get(&pdev->dev, NULL);
       if (IS_ERR(priv->clk))
           return PTR_ERR(priv->clk);
       
       /* No cleanup needed - all automatic! */
       return 0;
   }

Common devm Functions
---------------------

.. code-block:: c

   /* Memory */
   devm_kzalloc()
   devm_kmalloc()
   devm_kfree()
   
   /* I/O memory */
   devm_ioremap()
   devm_ioremap_resource()
   devm_platform_ioremap_resource()
   
   /* Interrupts */
   devm_request_irq()
   devm_request_threaded_irq()
   
   /* Clocks */
   devm_clk_get()
   devm_clk_get_optional()
   
   /* GPIO */
   devm_gpiod_get()
   devm_gpiod_get_index()
   
   /* Regulators */
   devm_regulator_get()
   
   /* Misc */
   devm_kasprintf()
   devm_kmemdup()

Power Management
================

Suspend and Resume
------------------

.. code-block:: c

   static int mydev_suspend(struct device *dev) {
       struct mydev_priv *priv = dev_get_drvdata(dev);
       
       dev_info(dev, "Suspending\n");
       
       /* Save state if needed */
       mydev_save_state(priv);
       
       /* Disable hardware */
       mydev_hw_disable(priv);
       
       /* Disable clocks */
       clk_disable_unprepare(priv->clk);
       
       return 0;
   }
   
   static int mydev_resume(struct device *dev) {
       struct mydev_priv *priv = dev_get_drvdata(dev);
       int ret;
       
       dev_info(dev, "Resuming\n");
       
       /* Enable clocks */
       ret = clk_prepare_enable(priv->clk);
       if (ret)
           return ret;
       
       /* Restore state */
       mydev_restore_state(priv);
       
       /* Re-enable hardware */
       mydev_hw_enable(priv);
       
       return 0;
   }
   
   static const struct dev_pm_ops mydev_pm_ops = {
       .suspend = mydev_suspend,
       .resume = mydev_resume,
   };
   
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
       struct mydev_priv *priv = dev_get_drvdata(dev);
       
       clk_disable_unprepare(priv->clk);
       return 0;
   }
   
   static int mydev_runtime_resume(struct device *dev) {
       struct mydev_priv *priv = dev_get_drvdata(dev);
       
       return clk_prepare_enable(priv->clk);
   }
   
   static const struct dev_pm_ops mydev_pm_ops = {
       SET_RUNTIME_PM_OPS(mydev_runtime_suspend,
                          mydev_runtime_resume, NULL)
       SET_SYSTEM_SLEEP_PM_OPS(mydev_suspend, mydev_resume)
   };
   
   /* In probe */
   pm_runtime_enable(&pdev->dev);
   pm_runtime_get_sync(&pdev->dev);
   
   /* Before accessing hardware */
   pm_runtime_get_sync(&pdev->dev);
   /* ... use hardware ... */
   pm_runtime_put(&pdev->dev);

Complete Platform Driver Example
=================================

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/of.h>
   #include <linux/io.h>
   #include <linux/interrupt.h>
   #include <linux/clk.h>
   #include <linux/reset.h>
   
   #define REG_CTRL    0x00
   #define REG_STATUS  0x04
   #define REG_DATA    0x08
   
   struct mydev_priv {
       void __iomem *base;
       struct clk *clk;
       struct reset_control *reset;
       int irq;
       struct device *dev;
   };
   
   static irqreturn_t mydev_irq_handler(int irq, void *dev_id) {
       struct mydev_priv *priv = dev_id;
       u32 status;
       
       status = readl(priv->base + REG_STATUS);
       dev_dbg(priv->dev, "IRQ status: 0x%x\n", status);
       
       /* Clear interrupt */
       writel(status, priv->base + REG_STATUS);
       
       return IRQ_HANDLED;
   }
   
   static int mydev_hw_init(struct mydev_priv *priv) {
       int ret;
       
       /* Assert reset */
       ret = reset_control_assert(priv->reset);
       if (ret)
           return ret;
       
       usleep_range(10, 20);
       
       /* Deassert reset */
       ret = reset_control_deassert(priv->reset);
       if (ret)
           return ret;
       
       usleep_range(100, 200);
       
       /* Initialize hardware */
       writel(0x1, priv->base + REG_CTRL);
       
       dev_info(priv->dev, "Hardware initialized\n");
       return 0;
   }
   
   static int mydev_probe(struct platform_device *pdev) {
       struct device *dev = &pdev->dev;
       struct mydev_priv *priv;
       int ret;
       
       dev_info(dev, "Probing device\n");
       
       priv = devm_kzalloc(dev, sizeof(*priv), GFP_KERNEL);
       if (!priv)
           return -ENOMEM;
       
       priv->dev = dev;
       platform_set_drvdata(pdev, priv);
       
       /* Get and map memory */
       priv->base = devm_platform_ioremap_resource(pdev, 0);
       if (IS_ERR(priv->base))
           return PTR_ERR(priv->base);
       
       /* Get clock */
       priv->clk = devm_clk_get(dev, NULL);
       if (IS_ERR(priv->clk)) {
           dev_err(dev, "Failed to get clock\n");
           return PTR_ERR(priv->clk);
       }
       
       ret = clk_prepare_enable(priv->clk);
       if (ret) {
           dev_err(dev, "Failed to enable clock\n");
           return ret;
       }
       
       /* Get reset control */
       priv->reset = devm_reset_control_get(dev, NULL);
       if (IS_ERR(priv->reset)) {
           ret = PTR_ERR(priv->reset);
           goto err_clk;
       }
       
       /* Initialize hardware */
       ret = mydev_hw_init(priv);
       if (ret)
           goto err_clk;
       
       /* Get and request IRQ */
       priv->irq = platform_get_irq(pdev, 0);
       if (priv->irq < 0) {
           ret = priv->irq;
           goto err_clk;
       }
       
       ret = devm_request_irq(dev, priv->irq, mydev_irq_handler,
                              0, dev_name(dev), priv);
       if (ret) {
           dev_err(dev, "Failed to request IRQ\n");
           goto err_clk;
       }
       
       dev_info(dev, "Device probed successfully\n");
       return 0;
   
   err_clk:
       clk_disable_unprepare(priv->clk);
       return ret;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_priv *priv = platform_get_drvdata(pdev);
       
       dev_info(&pdev->dev, "Removing device\n");
       
       /* Disable hardware */
       writel(0, priv->base + REG_CTRL);
       
       clk_disable_unprepare(priv->clk);
       
       return 0;
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { },
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct platform_driver mydev_driver = {
       .probe = mydev_probe,
       .remove = mydev_remove,
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
   };
   
   module_platform_driver(mydev_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Kernel Developer");
   MODULE_DESCRIPTION("Example Platform Driver");

Best Practices
==============

1. **Use devm_* functions** for automatic resource management
2. **Validate all resources** in probe
3. **Handle probe deferral** (-EPROBE_DEFER)
4. **Implement power management** if applicable
5. **Use device tree** for hardware description
6. **Add proper error handling** in probe
7. **Clean up in reverse order** of initialization
8. **Use dev_* logging** functions
9. **Support runtime PM** for power savings
10. **Test suspend/resume** cycles

Common Pitfalls
===============

1. **Not checking devm_* return values**
2. **Forgetting to disable clocks on error**
3. **Incorrect resource cleanup order**
4. **Not handling -EPROBE_DEFER**
5. **Memory leaks in error paths**

Debugging
=========

.. code-block:: bash

   # List platform devices
   ls /sys/bus/platform/devices/
   
   # Check device tree
   ls /sys/firmware/devicetree/base/
   
   # Enable driver debug
   echo 8 > /proc/sys/kernel/printk
   echo 'module mydriver +p' > /sys/kernel/debug/dynamic_debug/control

See Also
========

- Linux_Device_Tree_Drivers.rst
- Linux_Char_Device_Drivers.rst
- Linux Device tree.rst
- Linux_GPIO_Pinctrl.rst

References
==========

- Documentation/driver-api/driver-model/platform.rst
- include/linux/platform_device.h
- drivers/base/platform.c
