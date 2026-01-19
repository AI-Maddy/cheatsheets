=============================
Linux Regmap API Guide
=============================

:Author: Linux Kernel Documentation
:Date: January 2026
:Version: 1.0
:Kernel: 5.x, 6.x

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic Regmap Setup
------------------

.. code-block:: c

   #include <linux/regmap.h>
   
   static const struct regmap_config mydev_regmap_config = {
       .reg_bits = 8,
       .val_bits = 8,
       .max_register = 0xFF,
   };
   
   /* I2C device */
   struct regmap *regmap;
   regmap = devm_regmap_init_i2c(client, &mydev_regmap_config);
   
   /* SPI device */
   regmap = devm_regmap_init_spi(spi, &mydev_regmap_config);
   
   /* Read/Write */
   unsigned int val;
   regmap_read(regmap, 0x10, &val);
   regmap_write(regmap, 0x20, 0x55);
   
   /* Update bits */
   regmap_update_bits(regmap, 0x30, 0x0F, 0x05);  // Mask and value

Regmap with Caching
-------------------

.. code-block:: c

   static const struct regmap_config mydev_regmap_config = {
       .reg_bits = 8,
       .val_bits = 8,
       .max_register = 0xFF,
       
       /* Enable caching */
       .cache_type = REGCACHE_RBTREE,
       
       /* Mark volatile registers (not cached) */
       .volatile_reg = mydev_volatile_reg,
       
       /* Mark precious registers (read clears) */
       .precious_reg = mydev_precious_reg,
   };
   
   static bool mydev_volatile_reg(struct device *dev, unsigned int reg) {
       switch (reg) {
       case STATUS_REG:
       case IRQ_STATUS_REG:
           return true;
       default:
           return false;
       }
   }

Regmap Introduction
===================

What is Regmap?
---------------

Regmap is a generic register map abstraction that provides:

- **Unified API** for I2C, SPI, MMIO devices
- **Register caching** to reduce bus traffic
- **Read-modify-write** operations
- **Bulk operations**
- **Register ranges**
- **Debugfs integration**

**Benefits:**

- Reduces boilerplate code
- Automatic caching and synchronization
- Built-in locking
- Power management integration
- Debug interface

Supported Bus Types
-------------------

.. code-block:: c

   /* I2C */
   regmap = devm_regmap_init_i2c(i2c_client, &config);
   
   /* SPI */
   regmap = devm_regmap_init_spi(spi_device, &config);
   
   /* MMIO (Memory-mapped I/O) */
   void __iomem *base = devm_ioremap_resource(&pdev->dev, res);
   regmap = devm_regmap_init_mmio(&pdev->dev, base, &config);
   
   /* Custom bus */
   regmap = devm_regmap_init(&dev, &custom_bus, ctx, &config);

Regmap Configuration
====================

Basic Configuration
-------------------

.. code-block:: c

   static const struct regmap_config basic_config = {
       /* Register and value sizes */
       .reg_bits = 8,           // 8-bit register addresses
       .val_bits = 8,           // 8-bit register values
       
       /* Maximum register address */
       .max_register = 0xFF,
       
       /* Use fast I/O (no delays) */
       .use_single_rw = false,
       
       /* Disable range checks for performance */
       .disable_locking = false,
   };

Advanced Configuration
----------------------

.. code-block:: c

   static const struct regmap_range mydev_wr_table_ranges[] = {
       regmap_reg_range(0x00, 0x0F),  // Writable
       regmap_reg_range(0x20, 0x2F),
   };
   
   static const struct regmap_range mydev_rd_table_ranges[] = {
       regmap_reg_range(0x00, 0x3F),  // Readable
   };
   
   static const struct regmap_range mydev_volatile_ranges[] = {
       regmap_reg_range(0x10, 0x1F),  // Volatile (not cached)
   };
   
   static const struct regmap_access_table mydev_wr_table = {
       .yes_ranges = mydev_wr_table_ranges,
       .n_yes_ranges = ARRAY_SIZE(mydev_wr_table_ranges),
   };
   
   static const struct regmap_access_table mydev_rd_table = {
       .yes_ranges = mydev_rd_table_ranges,
       .n_yes_ranges = ARRAY_SIZE(mydev_rd_table_ranges),
   };
   
   static const struct regmap_access_table mydev_volatile_table = {
       .yes_ranges = mydev_volatile_ranges,
       .n_yes_ranges = ARRAY_SIZE(mydev_volatile_ranges),
   };
   
   static const struct regmap_config advanced_config = {
       .reg_bits = 8,
       .val_bits = 8,
       .max_register = 0xFF,
       
       /* Access tables */
       .wr_table = &mydev_wr_table,
       .rd_table = &mydev_rd_table,
       .volatile_table = &mydev_volatile_table,
       
       /* Caching */
       .cache_type = REGCACHE_RBTREE,
       
       /* Register defaults */
       .reg_defaults = mydev_reg_defaults,
       .num_reg_defaults = ARRAY_SIZE(mydev_reg_defaults),
       
       /* Byte order */
       .val_format_endian = REGMAP_ENDIAN_BIG,
   };
   
   static const struct reg_default mydev_reg_defaults[] = {
       { 0x00, 0x00 },
       { 0x01, 0xFF },
       { 0x02, 0x80 },
   };

Cache Types
-----------

.. code-block:: c

   /* No caching */
   .cache_type = REGCACHE_NONE,
   
   /* Flat array cache (simple, memory intensive) */
   .cache_type = REGCACHE_FLAT,
   
   /* Red-black tree cache (balanced memory/performance) */
   .cache_type = REGCACHE_RBTREE,
   
   /* Maple tree cache (modern, efficient) */
   .cache_type = REGCACHE_MAPLE,

Basic Operations
================

Read and Write
--------------

.. code-block:: c

   struct regmap *regmap;
   unsigned int val;
   int ret;
   
   /* Single register read */
   ret = regmap_read(regmap, 0x10, &val);
   if (ret) {
       dev_err(dev, "Read failed: %d\n", ret);
       return ret;
   }
   
   /* Single register write */
   ret = regmap_write(regmap, 0x20, 0xAA);
   if (ret) {
       dev_err(dev, "Write failed: %d\n", ret);
       return ret;
   }
   
   /* Raw read (no cache) */
   ret = regmap_raw_read(regmap, 0x30, &val, sizeof(val));
   
   /* Raw write (no cache) */
   ret = regmap_raw_write(regmap, 0x40, &val, sizeof(val));

Bulk Operations
---------------

.. code-block:: c

   /* Bulk read */
   u8 buffer[16];
   ret = regmap_bulk_read(regmap, 0x00, buffer, ARRAY_SIZE(buffer));
   
   /* Bulk write */
   u8 data[] = {0x11, 0x22, 0x33, 0x44};
   ret = regmap_bulk_write(regmap, 0x10, data, ARRAY_SIZE(data));
   
   /* Raw bulk read */
   ret = regmap_raw_read(regmap, 0x20, buffer, sizeof(buffer));

Bit Operations
--------------

.. code-block:: c

   /* Update bits (read-modify-write) */
   ret = regmap_update_bits(regmap, 0x30, 0x0F, 0x05);
   // Mask: 0x0F, Value: 0x05
   // Result: (old_val & ~0x0F) | 0x05
   
   /* Set bits */
   ret = regmap_set_bits(regmap, 0x40, BIT(3) | BIT(5));
   
   /* Clear bits */
   ret = regmap_clear_bits(regmap, 0x50, BIT(2));
   
   /* Test bits */
   unsigned int val;
   ret = regmap_read(regmap, 0x60, &val);
   if (val & BIT(7))
       dev_info(dev, "Bit 7 is set\n");
   
   /* Update bits with check (returns true if changed) */
   bool changed;
   ret = regmap_update_bits_check(regmap, 0x70, 0xFF, 0xAA, &changed);
   if (changed)
       dev_info(dev, "Register was modified\n");

Multi-Register Operations
--------------------------

.. code-block:: c

   /* Multi-register write */
   static const struct reg_sequence init_sequence[] = {
       { 0x00, 0x80 },  // Reset
       { 0x01, 0x00 },  // Clear status
       { 0x02, 0x0F },  // Enable features
       { 0x03, 0xAA },  // Configuration
   };
   
   ret = regmap_multi_reg_write(regmap, init_sequence,
                                  ARRAY_SIZE(init_sequence));

Field Operations
================

Register Fields
---------------

.. code-block:: c

   #include <linux/regmap.h>
   
   /* Define register layout */
   #define CTRL_REG       0x00
   #define STATUS_REG     0x01
   
   /* CTRL_REG fields */
   #define CTRL_ENABLE    BIT(0)
   #define CTRL_MODE_MASK GENMASK(3, 1)
   #define CTRL_IRQ_EN    BIT(7)
   
   struct mydev_data {
       struct regmap *regmap;
       struct regmap_field *enable_field;
       struct regmap_field *mode_field;
       struct regmap_field *irq_field;
   };
   
   static const struct reg_field enable_field = REG_FIELD(CTRL_REG, 0, 0);
   static const struct reg_field mode_field = REG_FIELD(CTRL_REG, 1, 3);
   static const struct reg_field irq_field = REG_FIELD(CTRL_REG, 7, 7);
   
   static int mydev_init_fields(struct mydev_data *data) {
       data->enable_field = devm_regmap_field_alloc(data->dev,
                                                     data->regmap,
                                                     enable_field);
       if (IS_ERR(data->enable_field))
           return PTR_ERR(data->enable_field);
       
       data->mode_field = devm_regmap_field_alloc(data->dev,
                                                   data->regmap,
                                                   mode_field);
       if (IS_ERR(data->mode_field))
           return PTR_ERR(data->mode_field);
       
       data->irq_field = devm_regmap_field_alloc(data->dev,
                                                  data->regmap,
                                                  irq_field);
       if (IS_ERR(data->irq_field))
           return PTR_ERR(data->irq_field);
       
       return 0;
   }
   
   /* Using fields */
   static int mydev_enable(struct mydev_data *data, bool enable) {
       return regmap_field_write(data->enable_field, enable ? 1 : 0);
   }
   
   static int mydev_set_mode(struct mydev_data *data, unsigned int mode) {
       if (mode > 7)
           return -EINVAL;
       return regmap_field_write(data->mode_field, mode);
   }
   
   static int mydev_get_mode(struct mydev_data *data, unsigned int *mode) {
       return regmap_field_read(data->mode_field, mode);
   }

IRQ Support
===========

Regmap IRQ Chip
---------------

.. code-block:: c

   #include <linux/regmap.h>
   
   #define IRQ_STATUS_REG  0x10
   #define IRQ_MASK_REG    0x11
   
   #define IRQ_BIT_MOTION  BIT(0)
   #define IRQ_BIT_TEMP    BIT(1)
   #define IRQ_BIT_ERROR   BIT(7)
   
   static const struct regmap_irq mydev_irqs[] = {
       [0] = { .reg_offset = 0, .mask = IRQ_BIT_MOTION },
       [1] = { .reg_offset = 0, .mask = IRQ_BIT_TEMP },
       [2] = { .reg_offset = 0, .mask = IRQ_BIT_ERROR },
   };
   
   static const struct regmap_irq_chip mydev_irq_chip = {
       .name = "mydev-irq",
       .irqs = mydev_irqs,
       .num_irqs = ARRAY_SIZE(mydev_irqs),
       .num_regs = 1,
       .status_base = IRQ_STATUS_REG,
       .mask_base = IRQ_MASK_REG,
       .ack_base = IRQ_STATUS_REG,  // Write 1 to clear
   };
   
   static int mydev_setup_irq(struct mydev_data *data, int irq) {
       int ret;
       
       ret = devm_regmap_add_irq_chip(data->dev, data->regmap, irq,
                                       IRQF_ONESHOT, 0,
                                       &mydev_irq_chip,
                                       &data->irq_data);
       if (ret) {
           dev_err(data->dev, "Failed to add IRQ chip: %d\n", ret);
           return ret;
       }
       
       /* Get virtual IRQ numbers */
       data->motion_irq = regmap_irq_get_virq(data->irq_data, 0);
       data->temp_irq = regmap_irq_get_virq(data->irq_data, 1);
       data->error_irq = regmap_irq_get_virq(data->irq_data, 2);
       
       /* Request individual IRQs */
       ret = devm_request_threaded_irq(data->dev, data->motion_irq,
                                        NULL, mydev_motion_handler,
                                        IRQF_ONESHOT, "motion", data);
       
       return ret;
   }

Complete Driver Example
========================

I2C Sensor with Regmap
-----------------------

.. code-block:: c

   #include <linux/module.h>
   #include <linux/i2c.h>
   #include <linux/regmap.h>
   #include <linux/iio/iio.h>
   
   #define CHIP_ID_REG     0x00
   #define CTRL_REG        0x01
   #define STATUS_REG      0x02
   #define DATA_REG        0x10
   
   #define CHIP_ID         0x42
   
   struct sensor_data {
       struct i2c_client *client;
       struct regmap *regmap;
       struct regmap_field *enable;
       struct regmap_field *mode;
   };
   
   static const struct regmap_range sensor_wr_ranges[] = {
       regmap_reg_range(0x01, 0x0F),
   };
   
   static const struct regmap_range sensor_rd_ranges[] = {
       regmap_reg_range(0x00, 0x1F),
   };
   
   static const struct regmap_range sensor_volatile_ranges[] = {
       regmap_reg_range(0x02, 0x02),  // Status
       regmap_reg_range(0x10, 0x1F),  // Data
   };
   
   static const struct regmap_access_table sensor_wr_table = {
       .yes_ranges = sensor_wr_ranges,
       .n_yes_ranges = ARRAY_SIZE(sensor_wr_ranges),
   };
   
   static const struct regmap_access_table sensor_rd_table = {
       .yes_ranges = sensor_rd_ranges,
       .n_yes_ranges = ARRAY_SIZE(sensor_rd_ranges),
   };
   
   static const struct regmap_access_table sensor_volatile_table = {
       .yes_ranges = sensor_volatile_ranges,
       .n_yes_ranges = ARRAY_SIZE(sensor_volatile_ranges),
   };
   
   static const struct regmap_config sensor_regmap_config = {
       .reg_bits = 8,
       .val_bits = 8,
       .max_register = 0x1F,
       
       .wr_table = &sensor_wr_table,
       .rd_table = &sensor_rd_table,
       .volatile_table = &sensor_volatile_table,
       
       .cache_type = REGCACHE_RBTREE,
   };
   
   static const struct reg_field enable_field = REG_FIELD(CTRL_REG, 0, 0);
   static const struct reg_field mode_field = REG_FIELD(CTRL_REG, 1, 3);
   
   static int sensor_read_raw(struct iio_dev *indio_dev,
                               struct iio_chan_spec const *chan,
                               int *val, int *val2, long mask) {
       struct sensor_data *data = iio_priv(indio_dev);
       unsigned int reg_val;
       int ret;
       
       switch (mask) {
       case IIO_CHAN_INFO_RAW:
           ret = regmap_read(data->regmap, DATA_REG + chan->channel,
                              &reg_val);
           if (ret)
               return ret;
           *val = reg_val;
           return IIO_VAL_INT;
       default:
           return -EINVAL;
       }
   }
   
   static const struct iio_info sensor_info = {
       .read_raw = sensor_read_raw,
   };
   
   static const struct iio_chan_spec sensor_channels[] = {
       {
           .type = IIO_TEMP,
           .info_mask_separate = BIT(IIO_CHAN_INFO_RAW),
           .channel = 0,
       },
   };
   
   static int sensor_probe(struct i2c_client *client) {
       struct iio_dev *indio_dev;
       struct sensor_data *data;
       unsigned int chip_id;
       int ret;
       
       indio_dev = devm_iio_device_alloc(&client->dev, sizeof(*data));
       if (!indio_dev)
           return -ENOMEM;
       
       data = iio_priv(indio_dev);
       data->client = client;
       i2c_set_clientdata(client, indio_dev);
       
       /* Initialize regmap */
       data->regmap = devm_regmap_init_i2c(client, &sensor_regmap_config);
       if (IS_ERR(data->regmap)) {
           dev_err(&client->dev, "Failed to init regmap\n");
           return PTR_ERR(data->regmap);
       }
       
       /* Verify chip ID */
       ret = regmap_read(data->regmap, CHIP_ID_REG, &chip_id);
       if (ret) {
           dev_err(&client->dev, "Failed to read chip ID\n");
           return ret;
       }
       
       if (chip_id != CHIP_ID) {
           dev_err(&client->dev, "Invalid chip ID: 0x%02x\n", chip_id);
           return -ENODEV;
       }
       
       /* Allocate register fields */
       data->enable = devm_regmap_field_alloc(&client->dev, data->regmap,
                                               enable_field);
       if (IS_ERR(data->enable))
           return PTR_ERR(data->enable);
       
       data->mode = devm_regmap_field_alloc(&client->dev, data->regmap,
                                             mode_field);
       if (IS_ERR(data->mode))
           return PTR_ERR(data->mode);
       
       /* Enable sensor */
       ret = regmap_field_write(data->enable, 1);
       if (ret)
           return ret;
       
       /* Setup IIO device */
       indio_dev->name = "sensor";
       indio_dev->info = &sensor_info;
       indio_dev->channels = sensor_channels;
       indio_dev->num_channels = ARRAY_SIZE(sensor_channels);
       indio_dev->modes = INDIO_DIRECT_MODE;
       
       ret = devm_iio_device_register(&client->dev, indio_dev);
       if (ret) {
           dev_err(&client->dev, "Failed to register IIO device\n");
           return ret;
       }
       
       dev_info(&client->dev, "Sensor initialized\n");
       return 0;
   }
   
   static const struct of_device_id sensor_of_match[] = {
       { .compatible = "vendor,sensor", },
       { }
   };
   MODULE_DEVICE_TABLE(of, sensor_of_match);
   
   static const struct i2c_device_id sensor_id[] = {
       { "sensor", 0 },
       { }
   };
   MODULE_DEVICE_TABLE(i2c, sensor_id);
   
   static struct i2c_driver sensor_driver = {
       .driver = {
           .name = "sensor",
           .of_match_table = sensor_of_match,
       },
       .probe_new = sensor_probe,
       .id_table = sensor_id,
   };
   
   module_i2c_driver(sensor_driver);
   
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Sensor Driver with Regmap");

Cache Management
================

.. code-block:: c

   /* Mark cache dirty */
   regcache_mark_dirty(regmap);
   
   /* Sync cache to hardware */
   ret = regcache_sync(regmap);
   
   /* Drop cache (invalidate) */
   regcache_drop_region(regmap, 0x00, 0x0F);
   
   /* Bypass cache temporarily */
   regcache_cache_bypass(regmap, true);
   regmap_read(regmap, 0x10, &val);  // Direct hardware read
   regcache_cache_bypass(regmap, false);

Best Practices
==============

1. **Use devm_regmap_init_*()** for automatic cleanup
2. **Define access tables** for large register spaces
3. **Use register fields** for bit manipulation
4. **Enable caching** for frequently accessed registers
5. **Mark volatile registers** correctly
6. **Use bulk operations** when possible
7. **Leverage regmap IRQ** support
8. **Test cache synchronization**
9. **Document register map**
10. **Use debugfs** for development

Common Pitfalls
===============

1. **Wrong cache type** for device characteristics
2. **Not marking volatile registers**
3. **Incorrect endianness** configuration
4. **Missing range checks**
5. **Cache coherency issues**

Debugging
=========

.. code-block:: bash

   # View regmap registers
   cat /sys/kernel/debug/regmap/*/registers
   
   # View regmap cache
   cat /sys/kernel/debug/regmap/*/cache
   
   # View regmap access
   cat /sys/kernel/debug/regmap/*/access

See Also
========

- Linux_I2C_Drivers.rst
- Linux_SPI_Drivers.rst
- Linux_Platform_Drivers.rst
- Linux_Driver_IRQ_Handling.rst

References
==========

- Documentation/driver-api/regmap.rst
- include/linux/regmap.h
- drivers/base/regmap/
