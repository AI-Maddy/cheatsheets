====================================
Linux Driver IRQ Handling Guide
====================================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic IRQ Request
-----------------

.. code-block:: c

   #include <linux/interrupt.h>
   
   static irqreturn_t mydev_irq_handler(int irq, void *data) {
       struct mydev_data *mydata = data;
       
       /* Quick processing */
       u32 status = readl(mydata->regs + STATUS_REG);
       
       if (!(status & MY_IRQ_BIT))
           return IRQ_NONE;  // Not our interrupt
       
       /* Clear interrupt */
       writel(status, mydata->regs + STATUS_REG);
       
       /* Schedule bottom half */
       schedule_work(&mydata->work);
       
       return IRQ_HANDLED;
   }
   
   /* Request IRQ */
   ret = devm_request_irq(&pdev->dev, irq, mydev_irq_handler,
                          IRQF_SHARED, "mydevice", data);

Threaded IRQ
------------

.. code-block:: c

   static irqreturn_t mydev_hard_irq(int irq, void *data) {
       /* Fast handler - just check if it's our interrupt */
       struct mydev_data *mydata = data;
       u32 status = readl(mydata->regs + STATUS_REG);
       
       if (!(status & MY_IRQ_BIT))
           return IRQ_NONE;
       
       return IRQ_WAKE_THREAD;  // Wake thread handler
   }
   
   static irqreturn_t mydev_thread_irq(int irq, void *data) {
       /* Threaded handler - can sleep */
       struct mydev_data *mydata = data;
       
       /* Process data (can use mutex, I2C, etc.) */
       mutex_lock(&mydata->lock);
       // ... slow processing ...
       mutex_unlock(&mydata->lock);
       
       return IRQ_HANDLED;
   }
   
   ret = devm_request_threaded_irq(&pdev->dev, irq,
                                    mydev_hard_irq,
                                    mydev_thread_irq,
                                    IRQF_ONESHOT,
                                    "mydevice", data);

IRQ Fundamentals
================

IRQ Types
---------

**Hardware Interrupts:**

- External device interrupts
- Shared interrupts (multiple devices)
- MSI/MSI-X (PCI)
- GPIO interrupts

**Software Interrupts:**

- Tasklets
- Softirqs
- Workqueues

IRQ Handler Context
-------------------

.. code-block:: c

   static irqreturn_t handler(int irq, void *data) {
       /* Hard IRQ context constraints:
        * - Cannot sleep
        * - Cannot use mutex
        * - Cannot call schedule()
        * - Should be very fast
        * - Can use spinlocks
        */
       
       /* Check if in interrupt context */
       if (in_interrupt())
           /* Yes, in IRQ context */;
       
       /* Check if interrupts disabled */
       if (irqs_disabled())
           /* Yes, IRQs are disabled */;
       
       return IRQ_HANDLED;
   }

Return Values
-------------

.. code-block:: c

   return IRQ_NONE;         // Not our interrupt
   return IRQ_HANDLED;      // Interrupt handled
   return IRQ_WAKE_THREAD;  // Wake threaded handler

Requesting Interrupts
=====================

Basic Request
-------------

.. code-block:: c

   #include <linux/interrupt.h>
   
   int irq;
   int ret;
   
   /* Get IRQ number (from platform data, DT, etc.) */
   irq = platform_get_irq(pdev, 0);
   if (irq < 0)
       return irq;
   
   /* Request IRQ */
   ret = request_irq(irq, handler, flags, "mydevice", dev_data);
   if (ret) {
       dev_err(&pdev->dev, "Failed to request IRQ: %d\n", ret);
       return ret;
   }
   
   /* Later: Free IRQ */
   free_irq(irq, dev_data);

Managed Request (Recommended)
------------------------------

.. code-block:: c

   /* Automatically freed when device is removed */
   ret = devm_request_irq(&pdev->dev, irq, handler,
                          flags, "mydevice", dev_data);

IRQ Flags
---------

.. code-block:: c

   /* Trigger types */
   IRQF_TRIGGER_NONE        // Default
   IRQF_TRIGGER_RISING      // Rising edge
   IRQF_TRIGGER_FALLING     // Falling edge  
   IRQF_TRIGGER_HIGH        // Active high
   IRQF_TRIGGER_LOW         // Active low
   
   /* Sharing */
   IRQF_SHARED              // Shared interrupt
   IRQF_PROBE_SHARED        // Probe for sharing
   
   /* Threading */
   IRQF_ONESHOT             // Keep IRQ disabled until thread completes
   
   /* Special */
   IRQF_NO_SUSPEND          // Don't disable during suspend
   IRQF_EARLY_RESUME        // Resume before non-early IRQs
   
   /* Example: Shared, falling edge */
   ret = devm_request_irq(&pdev->dev, irq, handler,
                          IRQF_SHARED | IRQF_TRIGGER_FALLING,
                          "mydevice", data);

Threaded IRQ Handlers
=====================

Full Threaded IRQ
-----------------

.. code-block:: c

   static irqreturn_t mydev_hard_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       
       /* Quick check and acknowledgment */
       u32 status = readl(mydata->regs + IRQ_STATUS);
       
       if (!(status & MYDEV_IRQ_MASK))
           return IRQ_NONE;
       
       /* Save status for thread */
       mydata->irq_status = status;
       
       /* Acknowledge interrupt */
       writel(status, mydata->regs + IRQ_CLEAR);
       
       return IRQ_WAKE_THREAD;
   }
   
   static irqreturn_t mydev_thread_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       u32 status = mydata->irq_status;
       
       /* Can sleep here */
       mutex_lock(&mydata->lock);
       
       if (status & DATA_READY_IRQ) {
           /* Read data via slow bus (I2C, SPI) */
           mydev_read_data(mydata);
       }
       
       if (status & ERROR_IRQ) {
           dev_err(mydata->dev, "Device error\n");
           mydev_handle_error(mydata);
       }
       
       mutex_unlock(&mydata->lock);
       
       return IRQ_HANDLED;
   }
   
   ret = devm_request_threaded_irq(&pdev->dev, irq,
                                    mydev_hard_irq,
                                    mydev_thread_irq,
                                    IRQF_ONESHOT | IRQF_TRIGGER_LOW,
                                    "mydevice", data);

Thread-Only Handler
-------------------

.. code-block:: c

   /* No hard IRQ handler, only threaded */
   ret = devm_request_threaded_irq(&pdev->dev, irq,
                                    NULL,  /* No hard IRQ */
                                    mydev_thread_irq,
                                    IRQF_ONESHOT,
                                    "mydevice", data);

Deferred Work
=============

Tasklets
--------

.. code-block:: c

   #include <linux/interrupt.h>
   
   struct mydev_data {
       struct tasklet_struct tasklet;
       spinlock_t lock;
       u32 irq_status;
   };
   
   static void mydev_tasklet_func(unsigned long data) {
       struct mydev_data *mydata = (struct mydev_data *)data;
       
       /* Cannot sleep, but can be preempted */
       spin_lock(&mydata->lock);
       // ... process data ...
       spin_unlock(&mydata->lock);
   }
   
   static irqreturn_t mydev_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       
       /* Read and clear interrupt */
       mydata->irq_status = readl(mydata->regs + STATUS_REG);
       writel(mydata->irq_status, mydata->regs + CLEAR_REG);
       
       /* Schedule tasklet */
       tasklet_schedule(&mydata->tasklet);
       
       return IRQ_HANDLED;
   }
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       /* Initialize tasklet */
       tasklet_init(&data->tasklet, mydev_tasklet_func,
                     (unsigned long)data);
       
       // ... setup IRQ ...
       
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_data *data = platform_get_drvdata(pdev);
       
       /* Kill tasklet */
       tasklet_kill(&data->tasklet);
       
       return 0;
   }

Workqueues
----------

.. code-block:: c

   #include <linux/workqueue.h>
   
   struct mydev_data {
       struct work_struct work;
       struct workqueue_struct *wq;
       struct device *dev;
   };
   
   static void mydev_work_func(struct work_struct *work) {
       struct mydev_data *data = container_of(work,
                                                struct mydev_data, work);
       
       /* Can sleep */
       mutex_lock(&data->mutex);
       // ... slow processing ...
       msleep(10);
       mutex_unlock(&data->mutex);
   }
   
   static irqreturn_t mydev_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       
       /* Queue work */
       queue_work(mydata->wq, &mydata->work);
       
       return IRQ_HANDLED;
   }
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       /* Create workqueue */
       data->wq = create_singlethread_workqueue("mydev_wq");
       if (!data->wq)
           return -ENOMEM;
       
       /* Initialize work */
       INIT_WORK(&data->work, mydev_work_func);
       
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_data *data = platform_get_drvdata(pdev);
       
       /* Flush and destroy workqueue */
       flush_workqueue(data->wq);
       destroy_workqueue(data->wq);
       
       return 0;
   }

Delayed Work
------------

.. code-block:: c

   struct mydev_data {
       struct delayed_work dwork;
   };
   
   static void mydev_delayed_func(struct work_struct *work) {
       struct mydev_data *data = container_of(work,
                                                struct mydev_data,
                                                dwork.work);
       /* Processing */
   }
   
   /* Initialize */
   INIT_DELAYED_WORK(&data->dwork, mydev_delayed_func);
   
   /* Schedule after 100ms */
   schedule_delayed_work(&data->dwork, msecs_to_jiffies(100));
   
   /* Cancel */
   cancel_delayed_work_sync(&data->dwork);

IRQ Control
===========

Enabling/Disabling IRQs
-----------------------

.. code-block:: c

   /* Disable specific IRQ line */
   disable_irq(irq);
   
   /* Disable IRQ and wait for handler to complete */
   disable_irq_nosync(irq);
   
   /* Enable IRQ */
   enable_irq(irq);
   
   /* Disable local CPU interrupts */
   local_irq_disable();
   local_irq_enable();
   
   /* Save and restore interrupt state */
   unsigned long flags;
   local_irq_save(flags);
   // ... critical section ...
   local_irq_restore(flags);

IRQ Affinity
------------

.. code-block:: c

   /* Set IRQ affinity to specific CPUs */
   #include <linux/cpumask.h>
   
   struct cpumask mask;
   
   cpumask_clear(&mask);
   cpumask_set_cpu(2, &mask);  // CPU 2
   cpumask_set_cpu(3, &mask);  // CPU 3
   
   irq_set_affinity_hint(irq, &mask);

Complete Driver Example
========================

Platform Device with IRQ
------------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/platform_device.h>
   #include <linux/interrupt.h>
   #include <linux/io.h>
   #include <linux/of.h>
   #include <linux/miscdevice.h>
   
   #define STATUS_REG    0x00
   #define CONTROL_REG   0x04
   #define DATA_REG      0x08
   #define IRQ_ENABLE    0x0C
   
   #define IRQ_DATA_READY  BIT(0)
   #define IRQ_ERROR       BIT(1)
   
   struct mydev_data {
       struct device *dev;
       void __iomem *regs;
       int irq;
       struct miscdevice mdev;
       spinlock_t lock;
       wait_queue_head_t wait;
       u32 data_ready;
   };
   
   static irqreturn_t mydev_hard_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       u32 status;
       
       status = readl(mydata->regs + STATUS_REG);
       
       if (!(status & (IRQ_DATA_READY | IRQ_ERROR)))
           return IRQ_NONE;
       
       /* Clear interrupt */
       writel(status, mydata->regs + STATUS_REG);
       
       /* Save status for thread */
       mydata->data_ready = status;
       
       return IRQ_WAKE_THREAD;
   }
   
   static irqreturn_t mydev_thread_irq(int irq, void *data) {
       struct mydev_data *mydata = data;
       u32 status = mydata->data_ready;
       
       if (status & IRQ_DATA_READY) {
           /* Wake up readers */
           wake_up_interruptible(&mydata->wait);
       }
       
       if (status & IRQ_ERROR) {
           dev_err(mydata->dev, "Hardware error detected\n");
       }
       
       return IRQ_HANDLED;
   }
   
   static ssize_t mydev_read(struct file *filp, char __user *buf,
                              size_t count, loff_t *ppos) {
       struct mydev_data *data = container_of(filp->private_data,
                                                struct mydev_data, mdev);
       u32 value;
       int ret;
       
       /* Wait for data */
       ret = wait_event_interruptible(data->wait, data->data_ready);
       if (ret)
           return ret;
       
       spin_lock(&data->lock);
       value = readl(data->regs + DATA_REG);
       data->data_ready = 0;
       spin_unlock(&data->lock);
       
       if (count < sizeof(value))
           return -EINVAL;
       
       if (copy_to_user(buf, &value, sizeof(value)))
           return -EFAULT;
       
       return sizeof(value);
   }
   
   static const struct file_operations mydev_fops = {
       .owner = THIS_MODULE,
       .read = mydev_read,
   };
   
   static int mydev_probe(struct platform_device *pdev) {
       struct mydev_data *data;
       struct resource *res;
       int ret;
       
       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       data->dev = &pdev->dev;
       spin_lock_init(&data->lock);
       init_waitqueue_head(&data->wait);
       platform_set_drvdata(pdev, data);
       
       /* Map registers */
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       data->regs = devm_ioremap_resource(&pdev->dev, res);
       if (IS_ERR(data->regs))
           return PTR_ERR(data->regs);
       
       /* Get and request IRQ */
       data->irq = platform_get_irq(pdev, 0);
       if (data->irq < 0)
           return data->irq;
       
       ret = devm_request_threaded_irq(&pdev->dev, data->irq,
                                        mydev_hard_irq,
                                        mydev_thread_irq,
                                        IRQF_ONESHOT,
                                        "mydevice", data);
       if (ret) {
           dev_err(&pdev->dev, "Failed to request IRQ: %d\n", ret);
           return ret;
       }
       
       /* Enable interrupts */
       writel(IRQ_DATA_READY | IRQ_ERROR, data->regs + IRQ_ENABLE);
       
       /* Register character device */
       data->mdev.minor = MISC_DYNAMIC_MINOR;
       data->mdev.name = "mydevice";
       data->mdev.fops = &mydev_fops;
       
       ret = misc_register(&data->mdev);
       if (ret) {
           dev_err(&pdev->dev, "Failed to register misc device\n");
           return ret;
       }
       
       dev_info(&pdev->dev, "Device registered with IRQ %d\n", data->irq);
       return 0;
   }
   
   static int mydev_remove(struct platform_device *pdev) {
       struct mydev_data *data = platform_get_drvdata(pdev);
       
       /* Disable interrupts */
       writel(0, data->regs + IRQ_ENABLE);
       
       misc_deregister(&data->mdev);
       return 0;
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct platform_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
       .probe = mydev_probe,
       .remove = mydev_remove,
   };
   
   module_platform_driver(mydev_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("IRQ Example Driver");

MSI/MSI-X Interrupts
====================

MSI Support (PCI)
-----------------

.. code-block:: c

   #include <linux/pci.h>
   
   static int mydev_setup_msi(struct pci_dev *pdev) {
       int ret, nvec;
       
       /* Request number of MSI vectors */
       nvec = pci_alloc_irq_vectors(pdev, 1, 4, PCI_IRQ_MSI);
       if (nvec < 0) {
           dev_err(&pdev->dev, "Failed to allocate MSI: %d\n", nvec);
           return nvec;
       }
       
       dev_info(&pdev->dev, "Allocated %d MSI vectors\n", nvec);
       
       /* Request IRQs for each vector */
       for (int i = 0; i < nvec; i++) {
           int irq = pci_irq_vector(pdev, i);
           
           ret = request_irq(irq, mydev_irq_handler,
                              0, "mydevice", data);
           if (ret) {
               dev_err(&pdev->dev, "Failed to request IRQ %d\n", irq);
               goto err_free_irqs;
           }
       }
       
       return 0;
       
   err_free_irqs:
       while (--i >= 0)
           free_irq(pci_irq_vector(pdev, i), data);
       pci_free_irq_vectors(pdev);
       return ret;
   }
   
   static void mydev_remove_msi(struct pci_dev *pdev, int nvec) {
       for (int i = 0; i < nvec; i++)
           free_irq(pci_irq_vector(pdev, i), data);
       pci_free_irq_vectors(pdev);
   }

Best Practices
==============

1. **Use threaded IRQs** for slow processing
2. **Keep hard IRQ handlers fast** (<10 microseconds)
3. **Use devm_request_irq()** for automatic cleanup
4. **Always check IRQ ownership** in shared handlers
5. **Clear interrupts** before enabling
6. **Use proper synchronization** (spinlock in hard IRQ)
7. **Test with CONFIG_DEBUG_SHIRQ**
8. **Document IRQ requirements**
9. **Handle spurious interrupts**
10. **Use IRQF_ONESHOT** with threaded IRQs

Common Pitfalls
===============

1. **Sleeping in hard IRQ handler**
2. **Using mutex in hard IRQ**
3. **Not checking return value** of IRQ_NONE
4. **Deadlocks** between IRQ and process context
5. **Not disabling IRQ** before freeing
6. **Race conditions** with enable/disable
7. **Missing IRQF_SHARED** for shared IRQs

Debugging
=========

.. code-block:: bash

   # View interrupts
   cat /proc/interrupts
   
   # View IRQ stats per CPU
   watch -n1 'cat /proc/interrupts'
   
   # Check IRQ affinity
   cat /proc/irq/42/smp_affinity
   
   # Enable IRQ debugging
   echo 1 > /proc/sys/kernel/irq_debug
   
   # Trace interrupts
   trace-cmd record -e irq
   trace-cmd report

See Also
========

- Linux_Kernel_Synchronization.rst
- Linux_Platform_Drivers.rst
- Linux_GPIO_Pinctrl.rst
- Linux_Wait_Queues.rst

References
==========

- Documentation/core-api/genericirq.rst
- include/linux/interrupt.h
- kernel/irq/
