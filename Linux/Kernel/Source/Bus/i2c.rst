**Linux I2C client driver cheat sheet** 
(focused on modern kernels ~6.1–6.12 as of early 2026).  
It covers the **I2C client/driver** side (the sensor/EEPROM/codec/expander you attach to an I2C bus), not the adapter/controller side.

📌 1. Minimal Modern I2C Client Driver Skeleton (2025–2026 style)

.. code-block:: c

#include <linux/module.h>
#include <linux/i2c.h>
#include <linux/of_device.h>    // for of_*
#include <linux/regmap.h>       // highly recommended wrapper

#define MY_DRV_NAME   "my-i2c-sensor"

/* ────────────────────────────────────────
   Private data (per-device instance)
───────────────────────────────────────── */
struct my_sensor {
    struct i2c_client   *client;
    struct regmap       *regmap;
    u32                 variant;        // from .data in of_match or id_table
    /* ... your registers state, mutex, etc ... */
};

/* ────────────────────────────────────────
   Regmap config (very common & clean pattern)
───────────────────────────────────────── */
static const struct regmap_config my_regmap_config = {
    .reg_bits       = 8,                // most I²C chips use 8-bit registers
    .val_bits       = 8,                // or 16
    .max_register   = 0x7f,             // adjust to your chip
    .cache_type     = REGCACHE_NONE,    // or REGCACHE_RBTREE / FLAT
};

/* ────────────────────────────────────────
   Probe / Remove
───────────────────────────────────────── */
static int my_probe(struct i2c_client *client)
{
    struct my_sensor *sensor;
    int ret;

    sensor = devm_kzalloc(&client->dev, sizeof(*sensor), GFP_KERNEL);
    if (!sensor)
        return -ENOMEM;

    sensor->client = client;
    i2c_set_clientdata(client, sensor);

    sensor->regmap = devm_regmap_init_i2c(client, &my_regmap_config);
    if (IS_ERR(sensor->regmap))
        return PTR_ERR(sensor->regmap);

    /* Optional: read chip ID / reset chip */
    ret = regmap_read(sensor->regmap, 0x00 /* CHIP_ID_REG */, &chipid);
    if (ret || chipid != EXPECTED_ID)
        return -ENODEV;

    dev_info(&client->dev, "probed variant %u at 0x%02x\n",
             sensor->variant, client->addr);

    /* Register your subsystem here (hwmon, iio, input, etc) */
    /* e.g. hwmon_device_register_with_groups(...) */

    return 0;
}

static void my_remove(struct i2c_client *client)
{
    /* Cleanup if needed (most things are devm_ managed) */
    dev_info(&client->dev, "removed\n");
}

/* ────────────────────────────────────────
   Device Tree match table (preferred in 2026)
───────────────────────────────────────── */
static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,my-sensor-v1", .data = (void *)1 },
    { .compatible = "vendor,my-sensor-v2", .data = (void *)2 },
    { /* sentinel */ }
};
MODULE_DEVICE_TABLE(of, my_of_match);

/* ────────────────────────────────────────
   Legacy I2C ID table (still needed for non-DT platforms)
───────────────────────────────────────── */
static const struct i2c_device_id my_id_table[] = {
    { "my-sensor", 0 },
    { /* sentinel */ }
};
MODULE_DEVICE_TABLE(i2c, my_id_table);

/* ────────────────────────────────────────
   The driver structure
───────────────────────────────────────── */
static struct i2c_driver my_driver = {
    .driver = {
        .name           = MY_DRV_NAME,
        .of_match_table = my_of_match,
        .pm             = pm_sleep_ptr(&my_pm_ops),     // optional
    },
    .probe          = my_probe,
    .remove         = my_remove,
    .id_table       = my_id_table,
};

module_i2c_driver(my_driver);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("You <you@example.com>");
MODULE_DESCRIPTION("Minimal modern I2C client driver example");

📚 2. Quick Reference: Core I²C Transfer Functions

| Function                              | Purpose                                      | Return                  | Notes / When to use
|---------------------------------------|----------------------------------------------|-------------------------|---------------------
| ``i2c_master_send(client, buf, len)``   | Simple write (one message)                   | bytes sent or <0 errno  | Plain write, no reg addr
| ``i2c_master_recv(client, buf, len)``   | Simple read                                  | bytes read or <0        | After write-reg or combined
| ``i2c_smbus_read_byte_data(client, reg)``   | SMBus Read Byte Data                         | 0–255 or <0             | Most common for 8-bit regs
| ``i2c_smbus_write_byte_data(client, reg, val)`` | SMBus Write Byte Data               | 0 or <0                 | —
| ``i2c_smbus_read_word_data()``          | Read 16-bit value (MSB first)                | 0–65535 or <0           | —
| ``i2c_smbus_write_i2c_block_data()``    | Write block (SMBus style)                    | 0 or <0                 | —
| ``i2c_transfer(adapter, msgs, num)``    | Raw I²C messages (repeated start possible)   | num or <0               | When SMBus not enough
| ``regmap_read(map, reg, &val)``         | Clean register access (recommended)          | 0 or <0                 | Use with regmap-i2c
| ``regmap_write(map, reg, val)``         | —                                            | 0 or <0                 | —
| ``regmap_bulk_read()`` / ``regmap_bulk_write()`` | Multiple consecutive registers     | 0 or <0                 | Efficient for burst

🐧 3. Instantiation Methods (How the Kernel Finds Your Device)

Method                  | DT compatible string                          | When to use (2026)
------------------------|-----------------------------------------------|-------------------------------
**Device Tree** (🟢 🟢 best)  | ``compatible = "vendor,my-sensor-v1";``         | Almost everything embedded
**ACPI**                | ``_CID`` / ``_HID`` matching                      | x86 / server boards
**Old-style board file**| ``i2c_register_board_info()``                   | Legacy, 🔴 🔴 avoid
**Manual user-space**   | ``echo my-sensor 0x48 > /sys/bus/i2c/devices/i2c-1/new_device`` | Testing / no DT
**Probe / detect**      | ``.detect`` callback + ``.class`` + ``address_list`` | Rare (old hwmon style)

🏗️ 4. Common Patterns & Helpers

Pattern / Helper                        | Code snippet / Tip
----------------------------------------|--------------------------------------------------------------------------------
**Chip ID check**                       | ``regmap_read(regmap, REG_ID, &id); if (id != 0xA5) return -ENODEV;``
**Regmap + cache**                      | ``.cache_type = REGCACHE_RBTREE`` for frequent small reads
**PM runtime**                          | Add ``.pm = pm_ptr(&my_pm_ops)`` with runtime PM ops
**Error codes**                         | ``-EIO``, ``-ENXIO`` (no device), ``-ETIMEDOUT``, ``-EPROTO``
**Debugging**                           | ``i2cset -y 1 0x48 0x00 0x01`` / ``i2cget -y 1 0x48 0x00`` / ``i2cdetect -y 1``
**sysfs location**                      | ``/sys/bus/i2c/devices/1-0048/`` (bus-devaddr)
**Common addresses**                    | 0x48–0x4F (many sensors), 0x50–0x57 (EEPROMs), 0x68 (IMU/RTC)

🟢 🟢 ✅ 5. Quick Testing Commands (userspace)

.. code-block:: bash

================================================================================
List I²C buses
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



i2cdetect -l

================================================================================
🔧 Scan bus 1 for devices
================================================================================

i2cdetect -y 1

================================================================================
🔧 Read register 0x0D from device at 0x1C on bus 1
================================================================================

i2cget -y 1 0x1c 0x0d

================================================================================
Write 0x40 to register 0x00
================================================================================

i2cset -y 1 0x1c 0x00 0x40

================================================================================
🟢 ✅ 🟢 🟢 ✅ Force instantiate for testing (no DT)
================================================================================

echo my-sensor 0x1c > /sys/bus/i2c/devices/i2c-1/new_device

💡 Modern Tips (2025–2026)

- Prefer **regmap** over raw ``i2c_smbus_*`` — cleaner, cacheable, bulk support
- Use **device tree** + ``.compatible`` + ``.data`` for variants (almost mandatory)
- ``module_i2c_driver()`` macro → saves boilerplate registration
- 🔴 🔴 Avoid old ``struct i2c_driver .probe_new`` — it's gone; use plain ``.probe``
- For complex devices → use subsystem API (IIO, hwmon, input, led-class, etc.)
- Check ``Documentation/devicetree/bindings/i2c/`` for binding examples

Start with the skeleton above, adapt the regmap bits to your chip datasheet, and add your subsystem registration in probe. 🟢 🟢 Good luck with your I²C driver!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
