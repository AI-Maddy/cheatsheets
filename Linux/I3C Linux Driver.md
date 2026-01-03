**cheatsheet for the Linux I3C subsystem and drivers** (as of January 2026, Linux kernel ~6.12–6.14 era).  
The I3C subsystem has been mainline since ~4.20/5.0 (2018–2019), with steady improvements in recent kernels.

### 1. Kernel Subsystem Overview

- **Location**: `drivers/i3c/`
  - `master/` → I3C controller drivers
  - `device.c` → device core (probe/match/remove)
  - `master.c` → core IBI (In-Band Interrupt) & generic helpers
- **Kconfig**: `CONFIG_I3C=y` (core) + specific master driver (e.g. `CONFIG_DW_I3C_MASTER`, `CONFIG_SVC_I3C_MASTER`, `CONFIG_MIPI_I3C_HCI`)
- **Device Tree**: `compatible = "mipi,i3c-master"` or vendor-specific; child nodes for targets
- **Sysfs**: `/sys/bus/i3c/devices/` (one entry per attached I3C device)
  - `dynamic_address`, `bcr`, `dcr`, `pid`, `max_read_len`, `max_write_len`, etc.

### 2. Main Structures

| Structure                  | Purpose / Key Fields                                                                 | Owner / Usage |
|----------------------------|--------------------------------------------------------------------------------------|---------------|
| `struct i3c_master_controller` | Represents I3C bus master (controller ops, bus lock, dev list)                       | Master driver |
| `struct i3c_dev_desc`      | Internal desc of each I3C target (dynamic addr, BCR, DCR, PID, priv data)            | Core          |
| `struct i3c_device`        | Public view of I3C target (embedded `dev`, `desc`, `info`)                           | Client driver |
| `struct i3c_driver`        | Client driver registration (probe/remove, id_table with `MATCH_I3C_DCR`)             | Sensor/EEPROM driver |
| `struct i3c_ibi_setup`     | IBI config (max_payload_len, num_slots, handler callback)                            | Client driver → master |
| `struct i3c_generic_ibi_pool` | Generic IBI slot allocator (pre-allocated for low-latency)                        | Master driver |

### 3. Client Driver Skeleton (Typical Sensor / EEPROM)

```c
#include <linux/i3c/i3c_master.h>
#include <linux/i3c/i3c_device.h>
#include <linux/module.h>

static int my_probe(struct i3c_device *i3cdev)
{
    struct i3c_ibi_setup ibisetup = {
        .max_payload_len = 64,
        .num_slots = 4,
        .handler = my_ibi_handler,
    };
    int ret;

    ret = i3c_device_request_ibi(i3cdev, &ibisetup);
    if (ret)
        return ret;

    /* Optional: enable IBI events via CCC_ENEC */
    ret = i3c_device_enable_ibi(i3cdev);
    if (ret)
        goto err_disable_ibi;

    /* Read BCR/DCR/PID already fetched by core */

    return 0;

err_disable_ibi:
    i3c_device_free_ibi(i3cdev);
    return ret;
}

static void my_remove(struct i3c_device *i3cdev)
{
    i3c_device_disable_ibi(i3cdev);
    i3c_device_free_ibi(i3cdev);
}

static const struct i3c_device_id my_id_table[] = {
    I3C_DEVICE(DCR_TYPE_TEMP_SENSOR),       /* or specific PID match */
    {}
};

static struct i3c_driver my_driver = {
    .driver = {
        .name = "my-i3c-sensor",
        .owner = THIS_MODULE,
    },
    .probe = my_probe,
    .remove = my_remove,
    .id_table = my_id_table,
};

module_i3c_driver(my_driver);
MODULE_LICENSE("GPL");
```

### 4. Key APIs (Client Driver Perspective)

| API / Function                             | Purpose / When to call                                      | Notes / Return |
|--------------------------------------------|-------------------------------------------------------------|----------------|
| `i3c_driver_register()` / `module_i3c_driver()` | Register driver (use macro)                                 | — |
| `i3c_device_request_ibi()`                 | Request IBI pool setup (before enable)                      | 0 or -errno |
| `i3c_device_enable_ibi()`                  | Enable IBI via CCC_ENEC                                     | — |
| `i3c_device_disable_ibi()`                 | Disable via CCC_DISEC                                       | — |
| `i3c_device_free_ibi()`                    | Free pool/slots                                             | — |
| `i3c_device_do_xfers()`                    | Do private SDR transfers (read/write)                       | Supports retry on NACK |
| `i3c_device_read()` / `i3c_device_write()` | Simple byte transfers                                       | Wrapper around do_xfers |
| `i3cdev_set_drvdata()` / `i3cdev_get_drvdata()` | Private data                                                | — |

### 5. Master Controller Driver Responsibilities

- Implement `struct i3c_master_controller_ops`
  - `.add_i3c_dev()` / `.remove_i3c_dev()`
  - `.send_ccc()` (Common Command Code)
  - `.priv_xfers()` (private SDR/HDR transfers)
  - `.alloc_ibi_pool()` / `.free_ibi_pool()` / `.queue_ibi()` / `.recycle_ibi()`
  - `.enable_ibi()` / `.disable_ibi()`
- Call `i3c_master_register()` in probe
- Handle dynamic address assignment (ENTDAA / SETDASA)
- Support IBI reception (find slot, queue payload)

### 6. Common Mainline Master Drivers (2026)

| Driver                     | Compatible / SoC Examples                  | Features / Status |
|----------------------------|--------------------------------------------|-------------------|
| `dw-i3c-master`            | DesignWare (Synopsys), Intel IPU, many SoCs | HDR-DDR, IBI, hot-join |
| `svc-i3c-master`           | Silvaco / NXP i.MX93, some custom          | Good IBI support |
| `mipi-i3c-hci`             | MIPI HCI spec (newer controllers)          | Emerging, upstreaming |
| `cdns-i3c-master`          | Cadence IP                                 | Legacy but functional |

### 7. Debugging & Tools

```bash
# Enable I3C in kernel config
CONFIG_I3C=y
CONFIG_DW_I3C_MASTER=y   # or your controller

# Runtime inspection
ls /sys/bus/i3c/devices/
cat /sys/bus/i3c/devices/i3c-*/dynamic_address
cat /sys/bus/i3c/devices/i3c-*/bcr   # Bus Characteristics Register
cat /sys/bus/i3c/devices/i3c-*/dcr   # Device Characteristics Register
cat /sys/bus/i3c/devices/i3c-*/pid

# Userspace tools (i3c-tools similar to i2c-tools)
i3cdetect -y <busnum>
i3cget -y <bus> <da> <reg>
i3cset -y <bus> <da> <reg> <val>

# Kernel debug
echo 0x1 > /sys/kernel/debug/dynamic_debug/control  # for drivers/i3c/*
dmesg | grep i3c
```

### 8. Key Documentation Locations (kernel.org)

- `Documentation/driver-api/i3c/` (main index)
  - `device-driver-api.rst` → client driver API
  - `master-driver-api.rst` → controller API
  - `protocol.rst` → protocol overview
- Source: `drivers/i3c/`

The subsystem is stable for most use cases (sensors, EEPROM, thermal, accelerometers), with ongoing work on HDR modes, better hot-join, and new controllers. For production, test IBI/hot-join thoroughly, as they are the most complex parts.

Good luck with your I3C Linux integration!