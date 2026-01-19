==============================
Linux SPI Drivers Guide
==============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

SPI Device Driver
-----------------

.. code-block:: c

   #include <linux/spi/spi.h>
   
   static int mydev_probe(struct spi_device *spi) {
       /* Configure SPI mode */
       spi->mode = SPI_MODE_0;
       spi->bits_per_word = 8;
       spi->max_speed_hz = 1000000;  // 1 MHz
       
       int ret = spi_setup(spi);
       if (ret < 0)
           return ret;
       
       /* Simple write */
       u8 tx_buf[] = {0x01, 0x02, 0x03};
       ret = spi_write(spi, tx_buf, sizeof(tx_buf));
       
       /* Simple read */
       u8 rx_buf[4];
       ret = spi_read(spi, rx_buf, sizeof(rx_buf));
       
       /* Write then read */
       ret = spi_write_then_read(spi, tx_buf, 2, rx_buf, 4);
       
       return 0;
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static struct spi_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
       .probe = mydev_probe,
   };
   
   module_spi_driver(mydev_driver);

SPI Transfer Operations
------------------------

.. code-block:: c

   /* Synchronous transfer */
   struct spi_transfer xfer = {
       .tx_buf = tx_data,
       .rx_buf = rx_data,
       .len = 16,
   };
   spi_sync_transfer(spi, &xfer, 1);
   
   /* Message with multiple transfers */
   struct spi_message msg;
   struct spi_transfer xfers[2];
   
   spi_message_init(&msg);
   
   xfers[0].tx_buf = cmd_buf;
   xfers[0].len = 2;
   spi_message_add_tail(&xfers[0], &msg);
   
   xfers[1].rx_buf = data_buf;
   xfers[1].len = 64;
   spi_message_add_tail(&xfers[1], &msg);
   
   spi_sync(spi, &msg);

SPI Fundamentals
================

Introduction
------------

SPI (Serial Peripheral Interface) is a synchronous serial communication protocol used for short-distance communication.

**Key Characteristics:**

- Master-slave architecture
- Full-duplex communication
- Four-wire interface (MOSI, MISO, SCLK, CS)
- No fixed addressing scheme
- Typical speeds: 1-100 MHz

**SPI Signals:**

- **SCLK (SCK):** Serial Clock
- **MOSI (SDI):** Master Out Slave In
- **MISO (SDO):** Master In Slave Out
- **CS (SS):** Chip Select (active low)

SPI Modes
---------

.. code-block:: text

   Mode | CPOL | CPHA | Clock Polarity        | Clock Phase
   -----|------|------|----------------------|-------------------------
   0    | 0    | 0    | Idle low             | Sample on leading edge
   1    | 0    | 1    | Idle low             | Sample on trailing edge
   2    | 1    | 0    | Idle high            | Sample on leading edge
   3    | 1    | 1    | Idle high            | Sample on trailing edge

.. code-block:: c

   /* Set SPI mode */
   spi->mode = SPI_MODE_0;  // CPOL=0, CPHA=0
   spi->mode = SPI_MODE_1;  // CPOL=0, CPHA=1
   spi->mode = SPI_MODE_2;  // CPOL=1, CPHA=0
   spi->mode = SPI_MODE_3;  // CPOL=1, CPHA=1
   
   /* Additional mode flags */
   spi->mode |= SPI_CS_HIGH;      // CS active high
   spi->mode |= SPI_LSB_FIRST;    // LSB first
   spi->mode |= SPI_3WIRE;        // 3-wire mode
   spi->mode |= SPI_LOOP;         // Loopback mode

SPI Device Driver Structure
============================

Basic SPI Driver
----------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/spi/spi.h>
   #include <linux/of.h>
   
   struct mydev_data {
       struct spi_device *spi;
       struct mutex lock;
       u8 *tx_buffer;
       u8 *rx_buffer;
   };
   
   static int mydev_probe(struct spi_device *spi) {
       struct mydev_data *data;
       int ret;
       
       dev_info(&spi->dev, "Probing SPI device\n");
       
       data = devm_kzalloc(&spi->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;
       
       data->spi = spi;
       mutex_init(&data->lock);
       spi_set_drvdata(spi, data);
       
       /* Configure SPI parameters */
       spi->mode = SPI_MODE_0;
       spi->bits_per_word = 8;
       spi->max_speed_hz = 10000000;  // 10 MHz
       
       ret = spi_setup(spi);
       if (ret < 0) {
           dev_err(&spi->dev, "SPI setup failed: %d\n", ret);
           return ret;
       }
       
       /* Allocate DMA-safe buffers */
       data->tx_buffer = devm_kzalloc(&spi->dev, PAGE_SIZE, GFP_KERNEL | GFP_DMA);
       data->rx_buffer = devm_kzalloc(&spi->dev, PAGE_SIZE, GFP_KERNEL | GFP_DMA);
       
       if (!data->tx_buffer || !data->rx_buffer)
           return -ENOMEM;
       
       dev_info(&spi->dev, "SPI device probed successfully\n");
       return 0;
   }
   
   static void mydev_remove(struct spi_device *spi) {
       dev_info(&spi->dev, "Removing SPI device\n");
   }
   
   static const struct of_device_id mydev_of_match[] = {
       { .compatible = "vendor,mydevice", },
       { }
   };
   MODULE_DEVICE_TABLE(of, mydev_of_match);
   
   static const struct spi_device_id mydev_id[] = {
       { "mydevice", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(spi, mydev_id);
   
   static struct spi_driver mydev_driver = {
       .driver = {
           .name = "mydevice",
           .of_match_table = mydev_of_match,
       },
       .probe = mydev_probe,
       .remove = mydev_remove,
       .id_table = mydev_id,
   };
   
   module_spi_driver(mydev_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Kernel Developer");
   MODULE_DESCRIPTION("Example SPI Driver");

SPI Transfer Operations
========================

Simple Read/Write
-----------------

.. code-block:: c

   /* Simple write */
   static int mydev_write_reg(struct spi_device *spi, u8 reg, u8 value) {
       u8 buf[2] = { reg, value };
       return spi_write(spi, buf, sizeof(buf));
   }
   
   /* Simple read */
   static int mydev_read_reg(struct spi_device *spi, u8 reg, u8 *value) {
       u8 tx_buf[1] = { reg | 0x80 };  // Set read bit
       u8 rx_buf[2];
       int ret;
       
       ret = spi_write_then_read(spi, tx_buf, 1, rx_buf, 2);
       if (ret == 0)
           *value = rx_buf[1];
       
       return ret;
   }
   
   /* Bulk read */
   static int mydev_read_block(struct spi_device *spi, u8 reg,
                                u8 *data, size_t len) {
       u8 cmd = reg | 0x80;
       
       return spi_write_then_read(spi, &cmd, 1, data, len);
   }

SPI Transfers
-------------

.. code-block:: c

   static int mydev_transfer(struct spi_device *spi,
                              const void *tx_buf, void *rx_buf, size_t len) {
       struct spi_transfer xfer = {
           .tx_buf = tx_buf,
           .rx_buf = rx_buf,
           .len = len,
           .speed_hz = 5000000,  // 5 MHz for this transfer
           .bits_per_word = 8,
       };
       
       return spi_sync_transfer(spi, &xfer, 1);
   }
   
   /* Transfer with delay */
   static int mydev_transfer_with_delay(struct spi_device *spi) {
       u8 tx_data[] = {0x01, 0x02};
       u8 rx_data[2];
       
       struct spi_transfer xfer = {
           .tx_buf = tx_data,
           .rx_buf = rx_data,
           .len = sizeof(tx_data),
           .delay = {
               .value = 10,
               .unit = SPI_DELAY_UNIT_USECS,
           },
       };
       
       return spi_sync_transfer(spi, &xfer, 1);
   }

SPI Messages
------------

.. code-block:: c

   static int mydev_read_sensor(struct spi_device *spi, u16 *data) {
       u8 cmd = 0x03;  // Read command
       u8 rx_buf[2];
       struct spi_message msg;
       struct spi_transfer xfers[2];
       int ret;
       
       spi_message_init(&msg);
       memset(xfers, 0, sizeof(xfers));
       
       /* Transfer 1: Send command */
       xfers[0].tx_buf = &cmd;
       xfers[0].len = 1;
       spi_message_add_tail(&xfers[0], &msg);
       
       /* Transfer 2: Read data */
       xfers[1].rx_buf = rx_buf;
       xfers[1].len = 2;
       xfers[1].delay.value = 1;
       xfers[1].delay.unit = SPI_DELAY_UNIT_USECS;
       spi_message_add_tail(&xfers[1], &msg);
       
       ret = spi_sync(spi, &msg);
       if (ret == 0)
           *data = (rx_buf[0] << 8) | rx_buf[1];
       
       return ret;
   }

Asynchronous Transfers
-----------------------

.. code-block:: c

   static void mydev_complete(void *context) {
       struct completion *done = context;
       complete(done);
   }
   
   static int mydev_async_transfer(struct spi_device *spi,
                                    const u8 *tx_buf, size_t len) {
       struct spi_message msg;
       struct spi_transfer xfer = {
           .tx_buf = tx_buf,
           .len = len,
       };
       DECLARE_COMPLETION_ONSTACK(done);
       int ret;
       
       spi_message_init(&msg);
       spi_message_add_tail(&xfer, &msg);
       
       msg.complete = mydev_complete;
       msg.context = &done;
       
       ret = spi_async(spi, &msg);
       if (ret == 0) {
           wait_for_completion(&done);
           ret = msg.status;
       }
       
       return ret;
   }

Device Tree Integration
=======================

SPI Device Tree Node
--------------------

.. code-block:: dts

   &spi0 {
       status = "okay";
       
       mydevice@0 {
           compatible = "vendor,mydevice";
           reg = <0>;  /* Chip select 0 */
           spi-max-frequency = <10000000>;  /* 10 MHz */
           spi-cpol;  /* CPOL = 1 */
           spi-cpha;  /* CPHA = 1 */
           /* spi-cs-high;  Uncomment if CS is active high */
           
           interrupt-parent = <&gpio1>;
           interrupts = <5 IRQ_TYPE_EDGE_FALLING>;
           reset-gpios = <&gpio1 6 GPIO_ACTIVE_LOW>;
       };
   };

Reading DT Properties
----------------------

.. code-block:: c

   static int mydev_parse_dt(struct spi_device *spi,
                              struct mydev_data *data) {
       struct device_node *np = spi->dev.of_node;
       u32 value;
       
       if (!np)
           return -ENODEV;
       
       /* Check SPI mode from DT */
       dev_info(&spi->dev, "SPI mode: %d\n", spi->mode);
       dev_info(&spi->dev, "SPI max speed: %d Hz\n", spi->max_speed_hz);
       
       /* Read custom property */
       if (of_property_read_u32(np, "vendor,threshold", &value) == 0)
           data->threshold = value;
       
       /* Get IRQ */
       data->irq = of_irq_get(np, 0);
       if (data->irq > 0) {
           int ret = devm_request_threaded_irq(&spi->dev, data->irq,
                                                NULL, mydev_irq_thread,
                                                IRQF_ONESHOT,
                                                "mydevice", data);
           if (ret)
               dev_err(&spi->dev, "Failed to request IRQ\n");
       }
       
       /* Get GPIO */
       data->reset_gpio = devm_gpiod_get(&spi->dev, "reset", GPIOD_OUT_LOW);
       if (IS_ERR(data->reset_gpio))
           dev_warn(&spi->dev, "No reset GPIO\n");
       else
           gpiod_set_value_cansleep(data->reset_gpio, 1);
       
       return 0;
   }

Advanced Features
=================

DMA Transfers
-------------

.. code-block:: c

   static int mydev_dma_transfer(struct spi_device *spi,
                                  const u8 *tx_buf, u8 *rx_buf, size_t len) {
       struct spi_transfer xfer = {
           .tx_buf = tx_buf,  /* Must be DMA-safe */
           .rx_buf = rx_buf,  /* Must be DMA-safe */
           .len = len,
           .speed_hz = 20000000,  /* 20 MHz */
       };
       struct spi_message msg;
       
       spi_message_init(&msg);
       spi_message_add_tail(&xfer, &msg);
       
       /* DMA will be used automatically if available */
       return spi_sync(spi, &msg);
   }

Chip Select Control
-------------------

.. code-block:: c

   /* Manual CS control */
   static int mydev_transfer_cs(struct spi_device *spi) {
       struct spi_transfer xfers[3];
       struct spi_message msg;
       u8 cmd = 0x9F;
       u8 data[3];
       
       spi_message_init(&msg);
       memset(xfers, 0, sizeof(xfers));
       
       /* Assert CS and send command */
       xfers[0].tx_buf = &cmd;
       xfers[0].len = 1;
       xfers[0].cs_change = 1;  /* Keep CS asserted */
       spi_message_add_tail(&xfers[0], &msg);
       
       /* Read data with CS still asserted */
       xfers[1].rx_buf = data;
       xfers[1].len = 3;
       xfers[1].cs_change = 1;  /* Keep CS asserted */
       spi_message_add_tail(&xfers[1], &msg);
       
       /* Final transfer deasserts CS */
       xfers[2].len = 0;  /* Dummy transfer to deassert CS */
       spi_message_add_tail(&xfers[2], &msg);
       
       return spi_sync(spi, &msg);
   }

Complete Driver Example
========================

SPI EEPROM Driver
-----------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/spi/spi.h>
   #include <linux/miscdevice.h>
   #include <linux/fs.h>
   #include <linux/uaccess.h>
   
   #define EEPROM_SIZE 8192
   #define PAGE_SIZE_BYTES 32
   
   #define CMD_WRITE 0x02
   #define CMD_READ  0x03
   #define CMD_WREN  0x06
   #define CMD_RDSR  0x05
   
   #define SR_WIP    0x01  /* Write In Progress */
   
   struct eeprom_data {
       struct spi_device *spi;
       struct miscdevice mdev;
       struct mutex lock;
   };
   
   static int eeprom_wait_ready(struct spi_device *spi) {
       u8 cmd = CMD_RDSR;
       u8 status;
       int ret;
       int timeout = 100;
       
       do {
           ret = spi_write_then_read(spi, &cmd, 1, &status, 1);
           if (ret < 0)
               return ret;
           
           if (!(status & SR_WIP))
               return 0;
           
           usleep_range(1000, 2000);
       } while (--timeout);
       
       return -ETIMEDOUT;
   }
   
   static int eeprom_write_enable(struct spi_device *spi) {
       u8 cmd = CMD_WREN;
       return spi_write(spi, &cmd, 1);
   }
   
   static int eeprom_read(struct spi_device *spi, loff_t offset,
                          void *buf, size_t len) {
       u8 cmd[3];
       
       cmd[0] = CMD_READ;
       cmd[1] = (offset >> 8) & 0xFF;
       cmd[2] = offset & 0xFF;
       
       return spi_write_then_read(spi, cmd, 3, buf, len);
   }
   
   static int eeprom_write_page(struct spi_device *spi, loff_t offset,
                                 const void *buf, size_t len) {
       u8 cmd[3 + PAGE_SIZE_BYTES];
       int ret;
       
       if (len > PAGE_SIZE_BYTES)
           return -EINVAL;
       
       ret = eeprom_write_enable(spi);
       if (ret)
           return ret;
       
       cmd[0] = CMD_WRITE;
       cmd[1] = (offset >> 8) & 0xFF;
       cmd[2] = offset & 0xFF;
       memcpy(&cmd[3], buf, len);
       
       ret = spi_write(spi, cmd, 3 + len);
       if (ret)
           return ret;
       
       return eeprom_wait_ready(spi);
   }
   
   static ssize_t eeprom_fops_read(struct file *filp, char __user *buf,
                                    size_t count, loff_t *f_pos) {
       struct eeprom_data *eeprom = container_of(filp->private_data,
                                                   struct eeprom_data, mdev);
       u8 *tmp_buf;
       int ret;
       
       if (*f_pos >= EEPROM_SIZE)
           return 0;
       
       if (*f_pos + count > EEPROM_SIZE)
           count = EEPROM_SIZE - *f_pos;
       
       tmp_buf = kmalloc(count, GFP_KERNEL);
       if (!tmp_buf)
           return -ENOMEM;
       
       mutex_lock(&eeprom->lock);
       ret = eeprom_read(eeprom->spi, *f_pos, tmp_buf, count);
       mutex_unlock(&eeprom->lock);
       
       if (ret == 0) {
           ret = copy_to_user(buf, tmp_buf, count);
           if (ret == 0) {
               *f_pos += count;
               ret = count;
           } else {
               ret = -EFAULT;
           }
       }
       
       kfree(tmp_buf);
       return ret;
   }
   
   static ssize_t eeprom_fops_write(struct file *filp,
                                     const char __user *buf,
                                     size_t count, loff_t *f_pos) {
       struct eeprom_data *eeprom = container_of(filp->private_data,
                                                   struct eeprom_data, mdev);
       u8 *tmp_buf;
       size_t written = 0;
       int ret = 0;
       
       if (*f_pos >= EEPROM_SIZE)
           return -ENOSPC;
       
       if (*f_pos + count > EEPROM_SIZE)
           count = EEPROM_SIZE - *f_pos;
       
       tmp_buf = kmalloc(count, GFP_KERNEL);
       if (!tmp_buf)
           return -ENOMEM;
       
       if (copy_from_user(tmp_buf, buf, count)) {
           kfree(tmp_buf);
           return -EFAULT;
       }
       
       mutex_lock(&eeprom->lock);
       
       while (written < count) {
           loff_t page_start = (*f_pos + written) & ~(PAGE_SIZE_BYTES - 1);
           size_t page_offset = (*f_pos + written) & (PAGE_SIZE_BYTES - 1);
           size_t to_write = min_t(size_t, PAGE_SIZE_BYTES - page_offset,
                                    count - written);
           
           ret = eeprom_write_page(eeprom->spi, *f_pos + written,
                                   tmp_buf + written, to_write);
           if (ret)
               break;
           
           written += to_write;
       }
       
       mutex_unlock(&eeprom->lock);
       kfree(tmp_buf);
       
       if (written > 0) {
           *f_pos += written;
           return written;
       }
       
       return ret;
   }
   
   static const struct file_operations eeprom_fops = {
       .owner = THIS_MODULE,
       .read = eeprom_fops_read,
       .write = eeprom_fops_write,
       .llseek = default_llseek,
   };
   
   static int eeprom_probe(struct spi_device *spi) {
       struct eeprom_data *eeprom;
       int ret;
       
       eeprom = devm_kzalloc(&spi->dev, sizeof(*eeprom), GFP_KERNEL);
       if (!eeprom)
           return -ENOMEM;
       
       eeprom->spi = spi;
       mutex_init(&eeprom->lock);
       spi_set_drvdata(spi, eeprom);
       
       spi->mode = SPI_MODE_0;
       spi->bits_per_word = 8;
       spi->max_speed_hz = 10000000;
       
       ret = spi_setup(spi);
       if (ret)
           return ret;
       
       eeprom->mdev.minor = MISC_DYNAMIC_MINOR;
       eeprom->mdev.name = "spi-eeprom";
       eeprom->mdev.fops = &eeprom_fops;
       
       ret = misc_register(&eeprom->mdev);
       if (ret)
           return ret;
       
       dev_info(&spi->dev, "SPI EEPROM registered\n");
       return 0;
   }
   
   static void eeprom_remove(struct spi_device *spi) {
       struct eeprom_data *eeprom = spi_get_drvdata(spi);
       misc_deregister(&eeprom->mdev);
   }
   
   static const struct of_device_id eeprom_of_match[] = {
       { .compatible = "atmel,at25", },
       { }
   };
   MODULE_DEVICE_TABLE(of, eeprom_of_match);
   
   static struct spi_driver eeprom_driver = {
       .driver = {
           .name = "spi-eeprom",
           .of_match_table = eeprom_of_match,
       },
       .probe = eeprom_probe,
       .remove = eeprom_remove,
   };
   
   module_spi_driver(eeprom_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("SPI EEPROM Driver");

Best Practices
==============

1. **Use DMA-safe buffers** for transfers
2. **Check spi_setup() return value**
3. **Handle CS timing** properly
4. **Use appropriate SPI mode** for device
5. **Implement proper locking** for concurrent access
6. **Validate transfer lengths**
7. **Handle errors gracefully**
8. **Use devm_* functions** for resource management
9. **Test at different speeds**
10. **Document timing requirements**

Common Pitfalls
===============

1. **Using stack buffers** for DMA transfers
2. **Not checking alignment** requirements
3. **Incorrect SPI mode** configuration
4. **Missing CS delays**
5. **Buffer size mismatches**
6. **Not handling partial transfers**

Debugging
=========

.. code-block:: bash

   # List SPI devices
   ls /sys/bus/spi/devices/
   
   # Check SPI controller
   cat /sys/class/spi_master/spi0/statistics/*
   
   # Enable SPI debug
   echo 8 > /proc/sys/kernel/printk
   echo 'file spi.c +p' > /sys/kernel/debug/dynamic_debug/control

See Also
========

- Linux_Platform_Drivers.rst
- Linux_I2C_Drivers.rst  
- Linux_Device_Tree_Drivers.rst
- Linux_GPIO_Pinctrl.rst

References
==========

- Documentation/spi/
- include/linux/spi/spi.h
- drivers/spi/
