==========================
Linux RTC Drivers Guide
==========================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic RTC Driver
----------------

.. code-block:: c

   #include <linux/rtc.h>
   
   static int myrtc_read_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       
       /* Read from hardware */
       tm->tm_sec = readl(data->regs + SEC_REG);
       tm->tm_min = readl(data->regs + MIN_REG);
       tm->tm_hour = readl(data->regs + HOUR_REG);
       tm->tm_mday = readl(data->regs + DAY_REG);
       tm->tm_mon = readl(data->regs + MON_REG) - 1;  // 0-11
       tm->tm_year = readl(data->regs + YEAR_REG) - 1900;
       
       return 0;
   }
   
   static int myrtc_set_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       
       /* Write to hardware */
       writel(tm->tm_sec, data->regs + SEC_REG);
       writel(tm->tm_min, data->regs + MIN_REG);
       writel(tm->tm_hour, data->regs + HOUR_REG);
       writel(tm->tm_mday, data->regs + DAY_REG);
       writel(tm->tm_mon + 1, data->regs + MON_REG);  // 1-12
       writel(tm->tm_year + 1900, data->regs + YEAR_REG);
       
       return 0;
   }
   
   static const struct rtc_class_ops myrtc_ops = {
       .read_time = myrtc_read_time,
       .set_time = myrtc_set_time,
   };
   
   /* Register RTC */
   struct rtc_device *rtc;
   rtc = devm_rtc_device_register(&pdev->dev, "myrtc",
                                   &myrtc_ops, THIS_MODULE);

RTC with Alarm
--------------

.. code-block:: c

   static int myrtc_read_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       /* Read alarm time and enabled status */
       return 0;
   }
   
   static int myrtc_set_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       /* Set alarm time and enable if requested */
       return 0;
   }
   
   static int myrtc_alarm_irq_enable(struct device *dev, unsigned int enabled) {
       /* Enable/disable alarm interrupt */
       return 0;
   }
   
   static const struct rtc_class_ops myrtc_ops = {
       .read_time = myrtc_read_time,
       .set_time = myrtc_set_time,
       .read_alarm = myrtc_read_alarm,
       .set_alarm = myrtc_set_alarm,
       .alarm_irq_enable = myrtc_alarm_irq_enable,
   };

RTC Subsystem Overview
=======================

struct rtc_time
---------------

.. code-block:: c

   struct rtc_time {
       int tm_sec;    // 0-59
       int tm_min;    // 0-59
       int tm_hour;   // 0-23
       int tm_mday;   // 1-31 (day of month)
       int tm_mon;    // 0-11 (January = 0)
       int tm_year;   // Years since 1900
       int tm_wday;   // 0-6 (Sunday = 0) - usually ignored
       int tm_yday;   // 0-365 - usually ignored
       int tm_isdst;  // Daylight saving time flag - usually ignored
   };

struct rtc_wkalrm
-----------------

.. code-block:: c

   struct rtc_wkalrm {
       unsigned char enabled;  // 0 = alarm disabled, 1 = enabled
       unsigned char pending;  // 0 = no alarm pending, 1 = pending
       struct rtc_time time;   // Alarm time
   };

RTC Operations
==============

Basic Operations
----------------

.. code-block:: c

   static const struct rtc_class_ops myrtc_ops = {
       .read_time = myrtc_read_time,
       .set_time = myrtc_set_time,
       .read_alarm = myrtc_read_alarm,
       .set_alarm = myrtc_set_alarm,
       .alarm_irq_enable = myrtc_alarm_irq_enable,
   };

Reading Time
------------

.. code-block:: c

   static int myrtc_read_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       unsigned long flags;
       u8 regs[7];
       
       spin_lock_irqsave(&data->lock, flags);
       
       /* Read all registers atomically */
       myrtc_read_regs(data, 0, regs, 7);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       /* Convert BCD to binary if needed */
       tm->tm_sec = bcd2bin(regs[0] & 0x7F);
       tm->tm_min = bcd2bin(regs[1] & 0x7F);
       tm->tm_hour = bcd2bin(regs[2] & 0x3F);
       tm->tm_mday = bcd2bin(regs[3] & 0x3F);
       tm->tm_mon = bcd2bin(regs[4] & 0x1F) - 1;
       tm->tm_year = bcd2bin(regs[5]) + 100;  // Assume 20xx
       tm->tm_wday = bcd2bin(regs[6] & 0x07);
       
       return 0;
   }

Setting Time
------------

.. code-block:: c

   static int myrtc_set_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       unsigned long flags;
       u8 regs[7];
       
       /* Convert binary to BCD if needed */
       regs[0] = bin2bcd(tm->tm_sec);
       regs[1] = bin2bcd(tm->tm_min);
       regs[2] = bin2bcd(tm->tm_hour);
       regs[3] = bin2bcd(tm->tm_mday);
       regs[4] = bin2bcd(tm->tm_mon + 1);
       regs[5] = bin2bcd(tm->tm_year - 100);
       regs[6] = bin2bcd(tm->tm_wday);
       
       spin_lock_irqsave(&data->lock, flags);
       
       /* Write all registers atomically */
       myrtc_write_regs(data, 0, regs, 7);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       return 0;
   }

Alarm Support
=============

Setting Alarms
--------------

.. code-block:: c

   static int myrtc_set_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[4];
       
       /* Set alarm time */
       regs[0] = bin2bcd(alrm->time.tm_sec);
       regs[1] = bin2bcd(alrm->time.tm_min);
       regs[2] = bin2bcd(alrm->time.tm_hour);
       regs[3] = bin2bcd(alrm->time.tm_mday);
       
       myrtc_write_regs(data, ALARM_REG_BASE, regs, 4);
       
       /* Enable/disable alarm */
       if (alrm->enabled)
           myrtc_alarm_irq_enable(dev, 1);
       else
           myrtc_alarm_irq_enable(dev, 0);
       
       return 0;
   }
   
   static int myrtc_read_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[4];
       
       myrtc_read_regs(data, ALARM_REG_BASE, regs, 4);
       
       alrm->time.tm_sec = bcd2bin(regs[0]);
       alrm->time.tm_min = bcd2bin(regs[1]);
       alrm->time.tm_hour = bcd2bin(regs[2]);
       alrm->time.tm_mday = bcd2bin(regs[3]);
       
       /* Check if enabled */
       alrm->enabled = !!(data->control_reg & ALARM_ENABLE_BIT);
       alrm->pending = !!(data->status_reg & ALARM_FLAG_BIT);
       
       return 0;
   }

Alarm IRQ Enable
----------------

.. code-block:: c

   static int myrtc_alarm_irq_enable(struct device *dev, unsigned int enabled) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       unsigned long flags;
       u8 ctrl;
       
       spin_lock_irqsave(&data->lock, flags);
       
       ctrl = myrtc_read_reg(data, CONTROL_REG);
       
       if (enabled)
           ctrl |= ALARM_INT_ENABLE;
       else
           ctrl &= ~ALARM_INT_ENABLE;
       
       myrtc_write_reg(data, CONTROL_REG, ctrl);
       
       spin_unlock_irqrestore(&data->lock, flags);
       
       return 0;
   }

IRQ Handler
-----------

.. code-block:: c

   static irqreturn_t myrtc_irq(int irq, void *data) {
       struct myrtc_data *rtc_data = data;
       u8 status;
       
       status = myrtc_read_reg(rtc_data, STATUS_REG);
       
       if (status & ALARM_FLAG) {
           /* Clear alarm flag */
           myrtc_write_reg(rtc_data, STATUS_REG, status & ~ALARM_FLAG);
           
           /* Notify RTC core */
           rtc_update_irq(rtc_data->rtc, 1, RTC_AF | RTC_IRQF);
           
           return IRQ_HANDLED;
       }
       
       return IRQ_NONE;
   }

Complete Driver Example
========================

I2C RTC Driver
--------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/i2c.h>
   #include <linux/rtc.h>
   #include <linux/bcd.h>
   #include <linux/interrupt.h>
   #include <linux/of.h>
   
   #define RTC_SEC_REG     0x00
   #define RTC_MIN_REG     0x01
   #define RTC_HOUR_REG    0x02
   #define RTC_WDAY_REG    0x03
   #define RTC_DAY_REG     0x04
   #define RTC_MON_REG     0x05
   #define RTC_YEAR_REG    0x06
   
   #define RTC_CONTROL_REG 0x07
   #define RTC_STATUS_REG  0x08
   
   #define RTC_ALARM_SEC   0x09
   #define RTC_ALARM_MIN   0x0A
   #define RTC_ALARM_HOUR  0x0B
   #define RTC_ALARM_DAY   0x0C
   
   #define CTRL_ALARM_IE   BIT(0)
   #define STATUS_ALARM_F  BIT(0)
   
   struct myrtc_data {
       struct i2c_client *client;
       struct rtc_device *rtc;
       struct mutex lock;
       int irq;
   };
   
   static int myrtc_read_regs(struct myrtc_data *data, u8 reg,
                               u8 *buf, int len) {
       int ret;
       
       ret = i2c_smbus_read_i2c_block_data(data->client, reg, len, buf);
       if (ret < 0)
           return ret;
       
       return 0;
   }
   
   static int myrtc_write_regs(struct myrtc_data *data, u8 reg,
                                u8 *buf, int len) {
       int ret;
       
       ret = i2c_smbus_write_i2c_block_data(data->client, reg, len, buf);
       if (ret < 0)
           return ret;
       
       return 0;
   }
   
   static int myrtc_read_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[7];
       int ret;
       
       mutex_lock(&data->lock);
       ret = myrtc_read_regs(data, RTC_SEC_REG, regs, 7);
       mutex_unlock(&data->lock);
       
       if (ret)
           return ret;
       
       tm->tm_sec = bcd2bin(regs[0] & 0x7F);
       tm->tm_min = bcd2bin(regs[1] & 0x7F);
       tm->tm_hour = bcd2bin(regs[2] & 0x3F);
       tm->tm_wday = bcd2bin(regs[3] & 0x07);
       tm->tm_mday = bcd2bin(regs[4] & 0x3F);
       tm->tm_mon = bcd2bin(regs[5] & 0x1F) - 1;
       tm->tm_year = bcd2bin(regs[6]) + 100;
       
       return 0;
   }
   
   static int myrtc_set_time(struct device *dev, struct rtc_time *tm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[7];
       int ret;
       
       regs[0] = bin2bcd(tm->tm_sec);
       regs[1] = bin2bcd(tm->tm_min);
       regs[2] = bin2bcd(tm->tm_hour);
       regs[3] = bin2bcd(tm->tm_wday);
       regs[4] = bin2bcd(tm->tm_mday);
       regs[5] = bin2bcd(tm->tm_mon + 1);
       regs[6] = bin2bcd(tm->tm_year - 100);
       
       mutex_lock(&data->lock);
       ret = myrtc_write_regs(data, RTC_SEC_REG, regs, 7);
       mutex_unlock(&data->lock);
       
       return ret;
   }
   
   static int myrtc_read_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[4];
       u8 ctrl, status;
       int ret;
       
       mutex_lock(&data->lock);
       
       ret = myrtc_read_regs(data, RTC_ALARM_SEC, regs, 4);
       if (ret)
           goto out;
       
       ret = myrtc_read_regs(data, RTC_CONTROL_REG, &ctrl, 1);
       if (ret)
           goto out;
       
       ret = myrtc_read_regs(data, RTC_STATUS_REG, &status, 1);
       
   out:
       mutex_unlock(&data->lock);
       
       if (ret)
           return ret;
       
       alrm->time.tm_sec = bcd2bin(regs[0] & 0x7F);
       alrm->time.tm_min = bcd2bin(regs[1] & 0x7F);
       alrm->time.tm_hour = bcd2bin(regs[2] & 0x3F);
       alrm->time.tm_mday = bcd2bin(regs[3] & 0x3F);
       
       alrm->enabled = !!(ctrl & CTRL_ALARM_IE);
       alrm->pending = !!(status & STATUS_ALARM_F);
       
       return 0;
   }
   
   static int myrtc_set_alarm(struct device *dev, struct rtc_wkalrm *alrm) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 regs[4];
       int ret;
       
       regs[0] = bin2bcd(alrm->time.tm_sec);
       regs[1] = bin2bcd(alrm->time.tm_min);
       regs[2] = bin2bcd(alrm->time.tm_hour);
       regs[3] = bin2bcd(alrm->time.tm_mday);
       
       mutex_lock(&data->lock);
       
       ret = myrtc_write_regs(data, RTC_ALARM_SEC, regs, 4);
       if (ret)
           goto out;
       
       ret = myrtc_alarm_irq_enable(dev, alrm->enabled);
       
   out:
       mutex_unlock(&data->lock);
       return ret;
   }
   
   static int myrtc_alarm_irq_enable(struct device *dev, unsigned int enabled) {
       struct myrtc_data *data = dev_get_drvdata(dev);
       u8 ctrl;
       int ret;
       
       mutex_lock(&data->lock);
       
       ret = myrtc_read_regs(data, RTC_CONTROL_REG, &ctrl, 1);
       if (ret)
           goto out;
       
       if (enabled)
           ctrl |= CTRL_ALARM_IE;
       else
           ctrl &= ~CTRL_ALARM_IE;
       
       ret = myrtc_write_regs(data, RTC_CONTROL_REG, &ctrl, 1);
       
   out:
       mutex_unlock(&data->lock);
       return ret;
   }
   
   static const struct rtc_class_ops myrtc_ops = {
       .read_time = myrtc_read_time,
       .set_time = myrtc_set_time,
       .read_alarm = myrtc_read_alarm,
       .set_alarm = myrtc_set_alarm,
       .alarm_irq_enable = myrtc_alarm_irq_enable,
   };
   
   static irqreturn_t myrtc_irq_handler(int irq, void *data) {
       struct myrtc_data *rtc_data = data;
       u8 status;
       
       mutex_lock(&rtc_data->lock);
       myrtc_read_regs(rtc_data, RTC_STATUS_REG, &status, 1);
       mutex_unlock(&rtc_data->lock);
       
       if (!(status & STATUS_ALARM_F))
           return IRQ_NONE;
       
       /* Clear alarm flag */
       status &= ~STATUS_ALARM_F;
       mutex_lock(&rtc_data->lock);
       myrtc_write_regs(rtc_data, RTC_STATUS_REG, &status, 1);
       mutex_unlock(&rtc_data->lock);
       
       /* Notify RTC core */
       rtc_update_irq(rtc_data->rtc, 1, RTC_AF | RTC_IRQF);
       
       return IRQ_HANDLED;
   }
   
   static int myrtc_probe(struct i2c_client *client) {
       struct myrtc_data *data;
       int ret;
       
       data = devm_kzalloc(&client->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       data->client = client;
       mutex_init(&data->lock);
       i2c_set_clientdata(client, data);
       
       /* Register RTC device */
       data->rtc = devm_rtc_allocate_device(&client->dev);
       if (IS_ERR(data->rtc))
           return PTR_ERR(data->rtc);
       
       data->rtc->ops = &myrtc_ops;
       data->rtc->range_min = RTC_TIMESTAMP_BEGIN_2000;
       data->rtc->range_max = RTC_TIMESTAMP_END_2099;
       
       /* Setup IRQ if available */
       if (client->irq > 0) {
           ret = devm_request_threaded_irq(&client->dev, client->irq,
                                            NULL, myrtc_irq_handler,
                                            IRQF_ONESHOT,
                                            "myrtc", data);
           if (ret) {
               dev_warn(&client->dev, "Failed to request IRQ: %d\n", ret);
           } else {
               data->irq = client->irq;
               device_init_wakeup(&client->dev, true);
           }
       }
       
       ret = rtc_register_device(data->rtc);
       if (ret)
           return ret;
       
       dev_info(&client->dev, "RTC registered\n");
       return 0;
   }
   
   static const struct of_device_id myrtc_of_match[] = {
       { .compatible = "vendor,rtc", },
       { }
   };
   MODULE_DEVICE_TABLE(of, myrtc_of_match);
   
   static const struct i2c_device_id myrtc_id[] = {
       { "myrtc", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(i2c, myrtc_id);
   
   static struct i2c_driver myrtc_driver = {
       .driver = {
           .name = "myrtc",
           .of_match_table = myrtc_of_match,
       },
       .probe_new = myrtc_probe,
       .id_table = myrtc_id,
   };
   
   module_i2c_driver(myrtc_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("RTC Driver");

Best Practices
==============

1. **Use devm_rtc_allocate_device()** and rtc_register_device()
2. **Set range_min and range_max** for proper validation
3. **Handle BCD conversion** carefully
4. **Protect reads/writes** with mutex
5. **Read registers atomically** to avoid race conditions
6. **Clear alarm flags** in IRQ handler
7. **Enable wakeup** if RTC supports it
8. **Validate user input**
9. **Test year 2038 problem** for 32-bit systems
10. **Document register layout**

Common Pitfalls
===============

1. **Month indexing** (0-11 in struct rtc_time, 1-12 in hardware)
2. **Year offset** (years since 1900 in struct rtc_time)
3. **Not clearing alarm flags**
4. **Missing BCD conversion**
5. **Race conditions** during time read
6. **Incorrect range settings**

Debugging
=========

.. code-block:: bash

   # Read RTC time
   cat /sys/class/rtc/rtc0/time
   cat /sys/class/rtc/rtc0/date
   
   # Read since epoch
   cat /sys/class/rtc/rtc0/since_epoch
   
   # Set system time from RTC
   hwclock -s
   
   # Set RTC from system time
   hwclock -w
   
   # Read/set alarm
   cat /sys/class/rtc/rtc0/wakealarm
   echo +60 > /sys/class/rtc/rtc0/wakealarm  # 60 seconds from now

See Also
========

- Linux_I2C_Drivers.rst
- Linux_Platform_Drivers.rst
- Linux_Driver_IRQ_Handling.rst

References
==========

- Documentation/rtc.txt
- include/linux/rtc.h
- drivers/rtc/
