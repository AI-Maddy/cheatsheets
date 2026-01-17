================================================================================
Linux Bus Subsystems - Comprehensive Reference
================================================================================

**Focus:** PCIe, I2C, I3C, USB kernel drivers and subsystems  
**Target Audience:** Embedded systems engineers, kernel driver developers  
**Kernel Versions:** 6.1–6.12+ (2026 best practices)  
**Last Updated:** January 2026

================================================================================

TL;DR - Quick Reference
================================================================================

**Bus Protocol Comparison:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Bus
     - Max Speed
     - Typical Use
     - Addressing
     - Power
   * - **I2C**
     - 1 MHz (FM+)
     - Sensors, EEPROMs
     - 7-bit/10-bit
     - 3.3V/1.8V
   * - **I3C**
     - 12.5 MHz (33 MHz HDR)
     - Modern sensors, IoT
     - Dynamic 7-bit
     - 1.2V/1.8V
   * - **PCIe Gen4**
     - 16 GT/s per lane
     - GPUs, NVMe, NICs
     - Bus:Dev:Func
     - 3.3V/12V
   * - **USB 3.2 Gen2**
     - 10 Gbit/s
     - Storage, cameras
     - Address 1-127
     - 5V/20V PD

**Essential Commands:**

.. code-block:: bash

    # I2C
    i2cdetect -l                          # List I2C buses
    i2cdetect -y 1                        # Scan bus 1
    i2cget -y 1 0x48 0x0D                 # Read register
    i2cset -y 1 0x48 0x00 0x40            # Write register
    
    # I3C
    i3cdetect -y 0                        # Scan I3C bus 0
    cat /sys/bus/i3c/devices/*/dynamic_address
    
    # PCIe
    lspci -nn -vvv                        # List all PCI devices
    lspci -d 8086:10d3                    # Find specific vendor:device
    setpci -s 01:00.0 COMMAND             # Read config space
    cat /sys/bus/pci/devices/*/resource   # BAR info
    
    # USB
    lsusb -t                              # USB tree
    lsusb -v -d 046d:c077                 # Verbose device info
    usb-devices | grep -E "Speed|Class"   # Speed & class info

**Key Kernel Structures:**

.. code-block:: c

    // I2C
    struct i2c_client { /* represents I2C device */ };
    struct i2c_driver { .probe, .remove, .id_table };
    struct regmap_config { /* register access abstraction */ };
    
    // I3C
    struct i3c_device { /* I3C target */ };
    struct i3c_driver { .probe, .remove };
    
    // PCIe
    struct pci_dev { .vendor, .device, .resource[6], .irq };
    struct pci_driver { .probe, .remove, .id_table };
    
    // USB
    struct usb_device { /* USB device tree node */ };
    struct usb_driver { .probe, .disconnect, .id_table };
    struct usb_interface { /* one function of device */ };

**Driver Registration Macros:**

.. code-block:: c

    module_i2c_driver(my_i2c_driver);
    module_i3c_driver(my_i3c_driver);
    module_pci_driver(my_pci_driver);
    module_usb_driver(my_usb_driver);

================================================================================

1. I2C Subsystem
================================================================================

1.1 I2C Architecture
---------------------

**I2C Bus Topology:**

::

    SoC/CPU
      ├── I2C Controller 0 (adapter)
      │   ├── I2C Device 0x48 (sensor)
      │   ├── I2C Device 0x50 (EEPROM)
      │   └── I2C Device 0x1A (codec)
      └── I2C Controller 1 (adapter)
          ├── I2C Device 0x68 (RTC)
          └── I2C Device 0x3C (display)

**Key Concepts:**

- **Adapter:** I2C controller hardware (bus master)
- **Client:** I2C slave device (sensor, EEPROM, codec)
- **SMBus:** Simplified subset of I2C with stricter electrical specs
- **7-bit addressing:** Standard (0x03-0x77 valid addresses)
- **10-bit addressing:** Extended mode (rare)

1.2 I2C Client Driver Structure
--------------------------------

**Complete Modern I2C Driver Template:**

.. code-block:: c

    #include <linux/module.h>
    #include <linux/i2c.h>
    #include <linux/of_device.h>
    #include <linux/regmap.h>
    
    #define MY_DRV_NAME "my-i2c-sensor"
    
    /* Per-device private data */
    struct my_sensor {
        struct i2c_client   *client;
        struct regmap       *regmap;
        u32                 variant;
        struct mutex        lock;
    };
    
    /* Regmap configuration (recommended modern pattern) */
    static const struct regmap_config my_regmap_config = {
        .reg_bits       = 8,        // 8-bit register address
        .val_bits       = 8,        // 8-bit register value
        .max_register   = 0x7F,
        .cache_type     = REGCACHE_RBTREE,  // or REGCACHE_NONE
    };
    
    static int my_probe(struct i2c_client *client)
    {
        struct my_sensor *sensor;
        unsigned int chipid;
        int ret;
        
        sensor = devm_kzalloc(&client->dev, sizeof(*sensor), GFP_KERNEL);
        if (!sensor)
            return -ENOMEM;
        
        sensor->client = client;
        i2c_set_clientdata(client, sensor);
        mutex_init(&sensor->lock);
        
        /* Initialize regmap (abstracts register access) */
        sensor->regmap = devm_regmap_init_i2c(client, &my_regmap_config);
        if (IS_ERR(sensor->regmap))
            return PTR_ERR(sensor->regmap);
        
        /* Verify chip ID */
        ret = regmap_read(sensor->regmap, 0x00, &chipid);
        if (ret) {
            dev_err(&client->dev, "Failed to read chip ID: %d\n", ret);
            return ret;
        }
        
        if (chipid != 0xA5) {
            dev_err(&client->dev, "Invalid chip ID: 0x%02X\n", chipid);
            return -ENODEV;
        }
        
        /* Initialize hardware */
        regmap_write(sensor->regmap, 0x01, 0x80);  // Reset
        msleep(10);
        regmap_write(sensor->regmap, 0x02, 0x01);  // Enable
        
        /* Register with subsystem (hwmon, iio, input, etc.) */
        dev_info(&client->dev, "Probed variant %u at 0x%02X\n",
                 sensor->variant, client->addr);
        
        return 0;
    }
    
    static void my_remove(struct i2c_client *client)
    {
        /* Cleanup (most resources are devm_ managed) */
        dev_info(&client->dev, "Removed\n");
    }
    
    /* Device tree match table (preferred in 2026) */
    static const struct of_device_id my_of_match[] = {
        { .compatible = "vendor,my-sensor-v1", .data = (void *)1 },
        { .compatible = "vendor,my-sensor-v2", .data = (void *)2 },
        { }
    };
    MODULE_DEVICE_TABLE(of, my_of_match);
    
    /* Legacy I2C ID table */
    static const struct i2c_device_id my_id_table[] = {
        { "my-sensor", 0 },
        { }
    };
    MODULE_DEVICE_TABLE(i2c, my_id_table);
    
    static struct i2c_driver my_driver = {
        .driver = {
            .name           = MY_DRV_NAME,
            .of_match_table = my_of_match,
        },
        .probe          = my_probe,
        .remove         = my_remove,
        .id_table       = my_id_table,
    };
    
    module_i2c_driver(my_driver);
    
    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Your Name <you@example.com>");
    MODULE_DESCRIPTION("Modern I2C client driver example");

1.3 I2C Transfer Functions
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Function
     - Purpose
     - Return Value
   * - ``i2c_master_send(client, buf, len)``
     - Simple write
     - Bytes sent or <0
   * - ``i2c_master_recv(client, buf, len)``
     - Simple read
     - Bytes read or <0
   * - ``i2c_smbus_read_byte_data(client, reg)``
     - Read 8-bit register
     - 0-255 or <0
   * - ``i2c_smbus_write_byte_data(client, reg, val)``
     - Write 8-bit register
     - 0 or <0
   * - ``i2c_smbus_read_word_data(client, reg)``
     - Read 16-bit register
     - 0-65535 or <0
   * - ``i2c_smbus_read_block_data(client, cmd, buf)``
     - Read block
     - Bytes or <0
   * - ``i2c_transfer(adapter, msgs, num)``
     - Raw I2C messages
     - num or <0
   * - ``regmap_read(map, reg, &val)``
     - Regmap register read
     - 0 or <0
   * - ``regmap_write(map, reg, val)``
     - Regmap register write
     - 0 or <0
   * - ``regmap_bulk_read(map, reg, buf, cnt)``
     - Read multiple registers
     - 0 or <0

1.4 Device Tree Binding Example
--------------------------------

.. code-block:: dts

    &i2c1 {
        clock-frequency = <100000>;  /* 100 kHz */
        status = "okay";
        
        sensor@48 {
            compatible = "vendor,my-sensor-v1";
            reg = <0x48>;
            interrupt-parent = <&gpio1>;
            interrupts = <10 IRQ_TYPE_EDGE_FALLING>;
            reset-gpios = <&gpio1 11 GPIO_ACTIVE_LOW>;
            vdd-supply = <&reg_3v3>;
        };
    };

================================================================================

2. I3C Subsystem
================================================================================

2.1 I3C vs I2C Comparison
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - I2C
     - I3C SDR
     - I3C HDR-DDR
   * - **Max Speed**
     - 1 MHz (FM+)
     - 12.5 MHz
     - 33 MHz
   * - **Data Rate**
     - ~1 Mbit/s
     - ~12.5 Mbit/s
     - ~33 Mbit/s
   * - **Topology**
     - Multi-master, open-drain
     - Single master, push-pull
     - Single master, push-pull
   * - **Addressing**
     - 7-bit/10-bit static
     - 7-bit dynamic + static
     - 7-bit dynamic
   * - **In-Band Interrupt**
     - No (needs GPIO)
     - Yes (IBI)
     - Yes (IBI)
   * - **Hot-Join**
     - No
     - Yes
     - Yes
   * - **Power**
     - Higher (10kΩ pull-ups)
     - Lower (1-4kΩ pull-ups)
     - Lower

2.2 I3C Architecture
---------------------

**I3C Bus Components:**

::

    I3C Main Controller
      ├── I3C Target 0 (Dynamic Addr: 0x08)  ← accelerometer
      ├── I3C Target 1 (Dynamic Addr: 0x09)  ← gyroscope
      ├── I3C Target 2 (Dynamic Addr: 0x0A)  ← temperature sensor
      └── I2C Legacy Device (Static Addr: 0x50)  ← EEPROM

**Key Concepts:**

- **Main Controller:** Bus master (only one active at a time)
- **Target:** Slave device (sensor, EEPROM)
- **Dynamic Address Assignment (DAA):** Runtime address allocation via ENTDAA CCC
- **Static Address:** I2C-compatible fallback address
- **CCC (Common Command Code):** Broadcast commands (ENTDAA, RSTDAA, ENTHDR, etc.)
- **IBI (In-Band Interrupt):** Interrupt signaling on SDA line (no extra GPIO)
- **Hot-Join:** Plug-and-play device addition

2.3 I3C Common Command Codes (CCC)
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 25 40 20

   * - CCC Code
     - Name
     - Purpose
     - Broadcast?
   * - 0x06
     - ENTDAA
     - Enter Dynamic Address Assignment
     - Yes
   * - 0x07
     - RSTDAA
     - Reset Dynamic Address Assignment
     - Yes
   * - 0x08
     - SETDASA
     - Set Dynamic Address from Static
     - Yes
   * - 0x0A
     - SETMWL/GETMWL
     - Set/Get Max Write Length
     - Direct
   * - 0x0B
     - SETMRL/GETMRL
     - Set/Get Max Read Length
     - Direct
   * - 0x0C
     - ENTHDR
     - Enter HDR mode (DDR/TSP/TSL)
     - Yes
   * - 0x1F
     - GETPID
     - Get Provisional ID (48-bit unique)
     - Direct
   * - 0x20
     - GETBCR
     - Get Bus Characteristics Register
     - Direct
   * - 0x21
     - GETDCR
     - Get Device Characteristics Register
     - Direct
   * - 0x29
     - ENEC/DISEC
     - Enable/Disable Events (IBI, Hot-Join)
     - Direct

2.4 I3C Device Registers (BCR/DCR)
-----------------------------------

**Bus Characteristics Register (BCR) - 8 bits:**

.. list-table::
   :header-rows: 1
   :widths: 10 40 50

   * - Bit
     - Name
     - Meaning
   * - 7
     - IBI Support
     - Device supports In-Band Interrupts
   * - 6
     - IBI Payload
     - IBI has data byte
   * - 5
     - Hot-Join Support
     - Device supports Hot-Join
   * - 4
     - HDR Capable
     - Device supports HDR modes
   * - 3
     - HDR-DDR Support
     - Supports HDR Double Data Rate
   * - 2-0
     - Reserved
     - Future use

**Device Characteristics Register (DCR) - 8 bits:**

- 0x0C = Generic I3C sensor
- 0x48 = Temperature sensor
- 0x4A = Accelerometer
- 0x4B = Gyroscope

2.5 I3C Debugging
-----------------

.. code-block:: bash

    # List I3C devices
    ls /sys/bus/i3c/devices/
    
    # Check dynamic address
    cat /sys/bus/i3c/devices/i3c-*/dynamic_address
    
    # Check BCR (Bus Characteristics Register)
    cat /sys/bus/i3c/devices/i3c-*/bcr
    
    # Check PID (Provisional ID - 48-bit unique)
    cat /sys/bus/i3c/devices/i3c-*/pid
    
    # I3C tools (userspace - similar to i2c-tools)
    i3cdetect -y 0
    i3cget -y 0 0x08   # Read from dynamic addr 0x08

================================================================================

3. PCIe Subsystem
================================================================================

3.1 PCIe Hardware Overview
---------------------------

**PCIe Generations (2026):**

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Generation
     - Transfer Rate
     - Per-Lane Speed
     - x16 Bandwidth
     - Typical Use
   * - Gen 1
     - 2.5 GT/s
     - ~250 MB/s
     - ~4 GB/s
     - Legacy
   * - Gen 2
     - 5 GT/s
     - ~500 MB/s
     - ~8 GB/s
     - Old GPUs
   * - Gen 3
     - 8 GT/s
     - ~985 MB/s
     - ~15.75 GB/s
     - Modern GPUs, NVMe
   * - Gen 4
     - 16 GT/s
     - ~1.97 GB/s
     - ~31.5 GB/s
     - Latest NVMe, GPUs
   * - Gen 5
     - 32 GT/s
     - ~3.94 GB/s
     - ~63 GB/s
     - Data center SSDs
   * - Gen 6
     - 64 GT/s
     - ~7.88 GB/s
     - ~126 GB/s
     - 2026+ (emerging)

**PCIe Address Format:**

::

    Domain:Bus:Device.Function
    0000:01:00.0
    ^^^^ ^^ ^^  ^
    |    |  |   └─ Function (0-7)
    |    |  └───── Device (0-31)
    |    └──────── Bus (0-255)
    └───────────── Domain (0-65535, usually 0000)

3.2 PCIe Driver Structure
--------------------------

**Complete PCIe Driver Template:**

.. code-block:: c

    #include <linux/pci.h>
    #include <linux/module.h>
    
    /* PCI device ID table */
    static const struct pci_device_id my_pci_tbl[] = {
        { PCI_DEVICE(0x8086, 0x10D3) },  // Intel E1000E
        { PCI_DEVICE_SUB(0x10EC, 0x8168,
                         PCI_SUBVENDOR_ID_ANY,
                         PCI_SUBDEVICE_ID_ANY) },  // Realtek RTL8168
        { 0, }
    };
    MODULE_DEVICE_TABLE(pci, my_pci_tbl);
    
    /* Private device data */
    struct my_device {
        struct pci_dev  *pdev;
        void __iomem    *regs;
        int             bar;
        /* ... DMA buffers, queues, etc. ... */
    };
    
    static int my_pci_probe(struct pci_dev *pdev,
                            const struct pci_device_id *id)
    {
        struct my_device *dev;
        int ret, bar = 0;
        
        dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
        if (!dev)
            return -ENOMEM;
        
        dev->pdev = pdev;
        pci_set_drvdata(pdev, dev);
        
        /* Enable device */
        ret = pci_enable_device(pdev);
        if (ret) {
            dev_err(&pdev->dev, "Failed to enable device\n");
            return ret;
        }
        
        /* Enable bus mastering (DMA) */
        pci_set_master(pdev);
        
        /* Set DMA mask (64-bit preferred) */
        ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(64));
        if (ret) {
            ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(32));
            if (ret) {
                dev_err(&pdev->dev, "No suitable DMA available\n");
                goto err_disable;
            }
        }
        
        /* Request BAR regions */
        ret = pci_request_regions(pdev, "my_driver");
        if (ret) {
            dev_err(&pdev->dev, "Failed to request regions\n");
            goto err_disable;
        }
        
        /* Map BAR0 */
        dev->regs = pci_iomap(pdev, bar, 0);
        if (!dev->regs) {
            dev_err(&pdev->dev, "Failed to map BAR%d\n", bar);
            ret = -ENOMEM;
            goto err_release;
        }
        
        /* Enable MSI-X interrupts (preferred) */
        ret = pci_alloc_irq_vectors(pdev, 1, 4, PCI_IRQ_MSIX);
        if (ret < 0) {
            /* Fallback to MSI */
            ret = pci_alloc_irq_vectors(pdev, 1, 1, PCI_IRQ_MSI);
            if (ret < 0) {
                dev_err(&pdev->dev, "Failed to enable interrupts\n");
                goto err_iounmap;
            }
        }
        
        /* Request IRQ */
        ret = request_irq(pci_irq_vector(pdev, 0), my_irq_handler,
                          IRQF_SHARED, "my_driver", dev);
        if (ret) {
            dev_err(&pdev->dev, "Failed to request IRQ\n");
            goto err_free_vectors;
        }
        
        dev_info(&pdev->dev, "Probed successfully at %s\n",
                 pci_name(pdev));
        
        return 0;
    
    err_free_vectors:
        pci_free_irq_vectors(pdev);
    err_iounmap:
        pci_iounmap(pdev, dev->regs);
    err_release:
        pci_release_regions(pdev);
    err_disable:
        pci_disable_device(pdev);
        return ret;
    }
    
    static void my_pci_remove(struct pci_dev *pdev)
    {
        struct my_device *dev = pci_get_drvdata(pdev);
        
        free_irq(pci_irq_vector(pdev, 0), dev);
        pci_free_irq_vectors(pdev);
        pci_iounmap(pdev, dev->regs);
        pci_release_regions(pdev);
        pci_disable_device(pdev);
        
        dev_info(&pdev->dev, "Removed\n");
    }
    
    static struct pci_driver my_pci_driver = {
        .name       = KBUILD_MODNAME,
        .id_table   = my_pci_tbl,
        .probe      = my_pci_probe,
        .remove     = my_pci_remove,
    };
    
    module_pci_driver(my_pci_driver);
    
    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Your Name");
    MODULE_DESCRIPTION("Modern PCIe driver example");

3.3 PCIe Key APIs
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Function
     - Purpose
     - Return
   * - ``pci_enable_device(pdev)``
     - Power on device, enable resources
     - 0 or <0
   * - ``pci_disable_device(pdev)``
     - Power off device
     - void
   * - ``pci_set_master(pdev)``
     - Enable bus mastering (DMA)
     - void
   * - ``pci_request_regions(pdev, name)``
     - Claim all BARs
     - 0 or <0
   * - ``pci_release_regions(pdev)``
     - Release all BARs
     - void
   * - ``pci_iomap(pdev, bar, maxlen)``
     - Map BAR to virtual address
     - void __iomem *
   * - ``pci_iounmap(pdev, addr)``
     - Unmap BAR
     - void
   * - ``pci_read_config_word(pdev, offset, &val)``
     - Read config space (16-bit)
     - 0 or <0
   * - ``pci_write_config_dword(pdev, offset, val)``
     - Write config space (32-bit)
     - 0 or <0
   * - ``pci_alloc_irq_vectors(pdev, min, max, flags)``
     - Allocate MSI/MSI-X vectors
     - num or <0
   * - ``pci_free_irq_vectors(pdev)``
     - Free interrupt vectors
     - void
   * - ``pci_irq_vector(pdev, index)``
     - Get Linux IRQ number
     - int
   * - ``dma_set_mask_and_coherent(dev, mask)``
     - Set DMA addressing capability
     - 0 or <0

3.4 PCIe Debugging
------------------

.. code-block:: bash

    # List all PCI devices
    lspci -nn -vvv
    
    # Find specific vendor:device
    lspci -d 8086:10d3
    
    # Show tree topology
    lspci -tv
    
    # Read config space
    lspci -xxx -s 01:00.0
    
    # Sysfs inspection
    cat /sys/bus/pci/devices/0000:01:00.0/vendor
    cat /sys/bus/pci/devices/0000:01:00.0/device
    cat /sys/bus/pci/devices/0000:01:00.0/resource
    cat /sys/bus/pci/devices/0000:01:00.0/irq
    
    # Force remove device
    echo 1 > /sys/bus/pci/devices/0000:01:00.0/remove
    
    # Rescan bus
    echo 1 > /sys/bus/pci/rescan

================================================================================

4. USB Subsystem
================================================================================

4.1 USB Versions & Speeds
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 15 20

   * - USB Version
     - Marketing Name
     - Max Speed
     - Real-World
     - Connectors
   * - USB 2.0
     - Hi-Speed
     - 480 Mbit/s
     - ~350 Mbit/s
     - Type-A, micro-B, Type-C
   * - USB 3.2 Gen 1
     - SuperSpeed 5 Gbps
     - 5 Gbit/s
     - ~4 Gbit/s
     - Type-C, Type-A
   * - USB 3.2 Gen 2
     - SuperSpeed 10 Gbps
     - 10 Gbit/s
     - ~8 Gbit/s
     - Type-C
   * - USB 3.2 Gen 2×2
     - SuperSpeed 20 Gbps
     - 20 Gbit/s
     - ~16 Gbit/s
     - Type-C
   * - USB4 Gen 2
     - USB4 20 Gbps
     - 20 Gbit/s
     - ~16 Gbit/s
     - Type-C
   * - USB4 Gen 3
     - USB4 40 Gbps
     - 40 Gbit/s
     - ~32 Gbit/s
     - Type-C

4.2 USB Class Codes
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 30 30

   * - USB Class
     - Code
     - Linux Driver
     - Typical Devices
   * - Audio
     - 0x01
     - snd-usb-audio
     - Headsets, DACs, microphones
   * - Communications (CDC)
     - 0x02
     - cdc-acm, cdc_ether
     - Serial adapters, USB Ethernet
   * - HID
     - 0x03
     - usbhid
     - Keyboards, mice, gamepads
   * - Mass Storage
     - 0x08
     - usb-storage
     - USB flash drives, card readers
   * - Video (UVC)
     - 0x0E
     - uvcvideo
     - Webcams, endoscopes
   * - Vendor Specific
     - 0xFF
     - Custom driver
     - Proprietary devices

4.3 USB Host Driver Structure
------------------------------

**USB Driver Template:**

.. code-block:: c

    #include <linux/module.h>
    #include <linux/usb.h>
    
    /* USB device ID table */
    static const struct usb_device_id my_usb_table[] = {
        { USB_DEVICE(0x046D, 0xC077) },  // Logitech webcam
        { USB_DEVICE_AND_INTERFACE_INFO(0x0bda, 0x8153,
                                        USB_CLASS_COMM,
                                        USB_CDC_SUBCLASS_ETHERNET,
                                        USB_CDC_PROTO_NONE) },
        { }
    };
    MODULE_DEVICE_TABLE(usb, my_usb_table);
    
    /* Private device data */
    struct my_usb_device {
        struct usb_device       *udev;
        struct usb_interface    *interface;
        struct urb              *bulk_in_urb;
        struct urb              *bulk_out_urb;
        unsigned char           *bulk_in_buffer;
        size_t                  bulk_in_size;
    };
    
    static int my_usb_probe(struct usb_interface *interface,
                            const struct usb_device_id *id)
    {
        struct my_usb_device *dev;
        struct usb_endpoint_descriptor *bulk_in, *bulk_out;
        int ret;
        
        dev = kzalloc(sizeof(*dev), GFP_KERNEL);
        if (!dev)
            return -ENOMEM;
        
        dev->udev = interface_to_usbdev(interface);
        dev->interface = interface;
        
        /* Find bulk endpoints */
        ret = usb_find_common_endpoints(interface->cur_altsetting,
                                         &bulk_in, &bulk_out,
                                         NULL, NULL);
        if (ret) {
            dev_err(&interface->dev,
                    "Could not find bulk endpoints\n");
            goto error;
        }
        
        /* Allocate bulk IN buffer */
        dev->bulk_in_size = usb_endpoint_maxp(bulk_in);
        dev->bulk_in_buffer = kmalloc(dev->bulk_in_size, GFP_KERNEL);
        if (!dev->bulk_in_buffer) {
            ret = -ENOMEM;
            goto error;
        }
        
        /* Create bulk IN URB */
        dev->bulk_in_urb = usb_alloc_urb(0, GFP_KERNEL);
        if (!dev->bulk_in_urb) {
            ret = -ENOMEM;
            goto error;
        }
        
        usb_fill_bulk_urb(dev->bulk_in_urb, dev->udev,
                          usb_rcvbulkpipe(dev->udev,
                                          bulk_in->bEndpointAddress),
                          dev->bulk_in_buffer, dev->bulk_in_size,
                          my_bulk_in_callback, dev);
        
        usb_set_intfdata(interface, dev);
        
        dev_info(&interface->dev, "USB device probed\n");
        return 0;
    
    error:
        if (dev->bulk_in_buffer)
            kfree(dev->bulk_in_buffer);
        kfree(dev);
        return ret;
    }
    
    static void my_usb_disconnect(struct usb_interface *interface)
    {
        struct my_usb_device *dev = usb_get_intfdata(interface);
        
        usb_set_intfdata(interface, NULL);
        
        /* Kill URBs */
        usb_kill_urb(dev->bulk_in_urb);
        usb_free_urb(dev->bulk_in_urb);
        
        kfree(dev->bulk_in_buffer);
        kfree(dev);
        
        dev_info(&interface->dev, "USB device disconnected\n");
    }
    
    static struct usb_driver my_usb_driver = {
        .name       = "my_usb_driver",
        .probe      = my_usb_probe,
        .disconnect = my_usb_disconnect,
        .id_table   = my_usb_table,
    };
    
    module_usb_driver(my_usb_driver);
    
    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Your Name");
    MODULE_DESCRIPTION("USB host driver example");

4.4 USB Gadget (Device Mode)
-----------------------------

**Common USB Gadget Drivers (Embedded):**

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Gadget Driver
     - Purpose
     - Typical Use
   * - g_mass_storage
     - Emulate USB flash drive
     - File transfer, firmware update
   * - g_ether
     - USB Ethernet (RNDIS/ECM/NCM)
     - Network over USB
   * - g_serial
     - Virtual serial port
     - Console, debugging
   * - g_webcam
     - UVC gadget (webcam)
     - Camera streaming
   * - g_audio
     - USB sound card
     - Audio output

**USB Gadget Setup Example (ConfigFS):**

.. code-block:: bash

    # Load composite gadget framework
    modprobe libcomposite
    
    # Create gadget
    mkdir -p /sys/kernel/config/usb_gadget/g1
    cd /sys/kernel/config/usb_gadget/g1
    
    # Set USB IDs
    echo 0x1d6b > idVendor   # Linux Foundation
    echo 0x0104 > idProduct  # Multifunction Composite
    echo 0x0100 > bcdDevice
    echo 0x0200 > bcdUSB
    
    # Device strings
    mkdir strings/0x409
    echo "fedcba9876543210" > strings/0x409/serialnumber
    echo "MyCompany" > strings/0x409/manufacturer
    echo "USB Ethernet Gadget" > strings/0x409/product
    
    # Create configuration
    mkdir configs/c.1
    mkdir configs/c.1/strings/0x409
    echo "Config 1" > configs/c.1/strings/0x409/configuration
    
    # Add ECM (Ethernet) function
    mkdir functions/ecm.usb0
    ln -s functions/ecm.usb0 configs/c.1/
    
    # Bind to UDC (USB Device Controller)
    echo "ci_hdrc.0" > UDC   # or dwc2, dwc3, musb, etc.
    
    # Configure network interface
    ifconfig usb0 192.168.7.2 netmask 255.255.255.0

4.5 USB Debugging
-----------------

.. code-block:: bash

    # List all USB devices
    lsusb
    
    # USB device tree
    lsusb -t
    
    # Verbose device info
    lsusb -v -d 046d:c077
    
    # Show speed & class
    usb-devices | grep -E "Speed|Class"
    
    # Sysfs inspection
    cat /sys/bus/usb/devices/1-1/idVendor
    cat /sys/bus/usb/devices/1-1/idProduct
    cat /sys/bus/usb/devices/1-1/bDeviceClass
    cat /sys/bus/usb/devices/1-1/speed
    
    # Force re-enumeration
    echo 0 > /sys/bus/usb/devices/1-1/authorized
    echo 1 > /sys/bus/usb/devices/1-1/authorized
    
    # USB power state
    cat /sys/bus/usb/devices/1-1/power/level
    echo on > /sys/bus/usb/devices/1-1/power/level
    
    # Unbind driver
    echo -n '1-1' > /sys/bus/usb/drivers/usb/unbind
    
    # Kernel debug messages
    dmesg -w | grep usb

================================================================================

5. Exam Question: Multi-Bus Driver Integration
================================================================================

**Question (16 points):**

You are designing an embedded board with the following peripherals:

- **I2C0:** Temperature sensor (TI TMP102 at 0x48), EEPROM (AT24C256 at 0x50)
- **I3C0:** Accelerometer (dynamic address assignment), Gyroscope (static address 0x68)
- **PCIe:** NVMe SSD (vendor 0x144D device 0xA808)
- **USB:** Webcam (UVC class), USB-to-Serial adapter (CDC-ACM class)

**Part A (4 points):** Write device tree bindings for the I2C and I3C buses.

**Part B (6 points):** Implement a PCIe driver probe function that:
1. Enables the NVMe device
2. Sets 64-bit DMA mask
3. Maps BAR0
4. Enables MSI-X interrupts (4 vectors)

**Part C (4 points):** Write a bash script to:
1. Verify all I2C devices are detected
2. Verify USB webcam is recognized
3. Check NVMe drive is enumerated

**Part D (2 points):** Explain the advantage of I3C dynamic address assignment over I2C static addressing.

**Answer:**

**Part A: Device Tree Bindings**

.. code-block:: dts

    / {
        /* I2C bus */
        &i2c0 {
            clock-frequency = <400000>;  /* 400 kHz Fast Mode */
            status = "okay";
            
            tmp102@48 {
                compatible = "ti,tmp102";
                reg = <0x48>;
                interrupt-parent = <&gpio1>;
                interrupts = <10 IRQ_TYPE_EDGE_FALLING>;
            };
            
            eeprom@50 {
                compatible = "atmel,24c256";
                reg = <0x50>;
                pagesize = <64>;
            };
        };
        
        /* I3C bus */
        &i3c0 {
            status = "okay";
            
            accel@08 {
                compatible = "bosch,bmi323";
                /* Dynamic address assigned at runtime via ENTDAA */
                assigned-address = <0x08>;
            };
            
            gyro@68 {
                compatible = "st,lsm6dsv";
                reg = <0x68>;  /* Static I2C-compatible address */
                assigned-address = <0x09>;  /* I3C dynamic address */
            };
        };
    };

**Part B: PCIe Driver Probe Function**

.. code-block:: c

    static int nvme_pci_probe(struct pci_dev *pdev,
                              const struct pci_device_id *id)
    {
        struct nvme_dev *dev;
        void __iomem *bar0;
        int ret, num_vectors;
        
        /* Allocate private data */
        dev = devm_kzalloc(&pdev->dev, sizeof(*dev), GFP_KERNEL);
        if (!dev)
            return -ENOMEM;
        
        dev->pdev = pdev;
        pci_set_drvdata(pdev, dev);
        
        /* 1. Enable the NVMe device */
        ret = pci_enable_device(pdev);
        if (ret) {
            dev_err(&pdev->dev, "Failed to enable device: %d\n", ret);
            return ret;
        }
        
        /* Enable bus mastering for DMA */
        pci_set_master(pdev);
        
        /* 2. Set 64-bit DMA mask */
        ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(64));
        if (ret) {
            dev_err(&pdev->dev,
                    "Failed to set 64-bit DMA mask, trying 32-bit\n");
            ret = dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(32));
            if (ret) {
                dev_err(&pdev->dev, "No suitable DMA available\n");
                goto err_disable;
            }
        }
        
        /* Request all BAR regions */
        ret = pci_request_regions(pdev, "nvme");
        if (ret) {
            dev_err(&pdev->dev, "Failed to request regions: %d\n", ret);
            goto err_disable;
        }
        
        /* 3. Map BAR0 (NVMe controller registers) */
        bar0 = pci_iomap(pdev, 0, 0);
        if (!bar0) {
            dev_err(&pdev->dev, "Failed to map BAR0\n");
            ret = -ENOMEM;
            goto err_release;
        }
        dev->bar0 = bar0;
        
        /* 4. Enable MSI-X interrupts (4 vectors for admin + 3 I/O queues) */
        num_vectors = pci_alloc_irq_vectors(pdev, 1, 4, PCI_IRQ_MSIX);
        if (num_vectors < 0) {
            dev_err(&pdev->dev,
                    "MSI-X allocation failed, trying MSI: %d\n",
                    num_vectors);
            num_vectors = pci_alloc_irq_vectors(pdev, 1, 1, PCI_IRQ_MSI);
            if (num_vectors < 0) {
                dev_err(&pdev->dev, "Failed to enable interrupts\n");
                ret = num_vectors;
                goto err_iounmap;
            }
        }
        
        dev->num_vectors = num_vectors;
        
        /* Request IRQs for each vector */
        for (int i = 0; i < num_vectors; i++) {
            ret = request_irq(pci_irq_vector(pdev, i),
                              nvme_irq_handler,
                              IRQF_SHARED,
                              "nvme",
                              &dev->queues[i]);
            if (ret) {
                dev_err(&pdev->dev,
                        "Failed to request IRQ %d: %d\n", i, ret);
                goto err_free_irqs;
            }
        }
        
        dev_info(&pdev->dev,
                 "NVMe device enabled: BAR0 mapped, %d MSI-X vectors\n",
                 num_vectors);
        
        return 0;
    
    err_free_irqs:
        while (--i >= 0)
            free_irq(pci_irq_vector(pdev, i), &dev->queues[i]);
        pci_free_irq_vectors(pdev);
    err_iounmap:
        pci_iounmap(pdev, bar0);
    err_release:
        pci_release_regions(pdev);
    err_disable:
        pci_disable_device(pdev);
        return ret;
    }

**Part C: Verification Script**

.. code-block:: bash

    #!/bin/bash
    
    echo "=== Bus Subsystem Verification ==="
    echo
    
    # 1. Verify I2C devices
    echo "1. Checking I2C bus 0..."
    i2cdetect -y 0 | grep -E "48|50" > /dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ I2C devices detected at 0x48 and 0x50"
        i2cdetect -y 0
    else
        echo "   ✗ I2C devices NOT detected"
        exit 1
    fi
    echo
    
    # Verify TMP102 temperature sensor
    if [ -f /sys/bus/i2c/devices/0-0048/temp1_input ]; then
        temp=$(cat /sys/bus/i2c/devices/0-0048/temp1_input)
        echo "   Temperature: $((temp / 1000))°C"
    fi
    echo
    
    # 2. Verify USB webcam (UVC class)
    echo "2. Checking USB webcam (UVC)..."
    lsusb | grep -i "webcam\|camera" > /dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ USB webcam detected"
        lsusb | grep -i "webcam\|camera"
        
        # Check V4L2 device node
        if [ -e /dev/video0 ]; then
            echo "   ✓ V4L2 device node: /dev/video0"
            v4l2-ctl --device=/dev/video0 --list-formats-ext
        fi
    else
        echo "   ✗ USB webcam NOT detected"
    fi
    echo
    
    # Verify USB-to-Serial (CDC-ACM)
    echo "3. Checking USB-to-Serial adapter (CDC-ACM)..."
    if [ -e /dev/ttyACM0 ]; then
        echo "   ✓ CDC-ACM device: /dev/ttyACM0"
        ls -l /dev/ttyACM0
    else
        echo "   ✗ CDC-ACM device NOT found"
    fi
    echo
    
    # 4. Verify NVMe PCIe drive
    echo "4. Checking NVMe PCIe drive (144D:A808)..."
    lspci -d 144d:a808 > /dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ NVMe drive detected"
        lspci -d 144d:a808 -vvv | head -20
        
        # Check NVMe block device
        if [ -e /dev/nvme0 ]; then
            echo "   ✓ NVMe block device: /dev/nvme0"
            nvme list 2>/dev/null || echo "   (nvme-cli not installed)"
        fi
    else
        echo "   ✗ NVMe drive NOT detected"
        exit 1
    fi
    echo
    
    echo "=== Verification Complete ==="

**Part D: I3C Dynamic Address Assignment Advantage**

I3C dynamic address assignment (DAA) offers several advantages over I2C static addressing:

1. **No Address Conflicts:** In I2C, multiple sensors from the same vendor often have identical static addresses (e.g., 0x68 for many IMUs), requiring address translation chips or GPIO-based address selection. I3C assigns unique dynamic addresses at runtime, eliminating conflicts.

2. **Hot-Join Support:** I3C devices can join the bus after initialization via the Hot-Join mechanism, and the controller assigns them an address automatically. I2C requires devices to be present at boot.

3. **Scalability:** I3C supports larger systems with many sensors (up to 127 addresses) without manual address management. I2C requires careful planning to avoid collisions.

4. **Backward Compatibility:** I3C devices fall back to static I2C addresses during enumeration, then switch to dynamic I3C addresses. This allows mixed I2C/I3C buses.

**Example Scenario:**
- Board has 3 accelerometers (same model, all default to I2C address 0x68)
- **I2C:** Requires external address selection (GPIO pins, resistors) to make each unique (0x68, 0x69, 0x6A)
- **I3C:** Controller runs ENTDAA command, assigns 0x08, 0x09, 0x0A dynamically → no hardware changes needed

================================================================================

6. Key Takeaways
================================================================================

**Bus Selection Guide:**

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Use Case
     - I2C
     - I3C
     - PCIe
   * - Low-speed sensors
     - ✓ Perfect
     - ✓ Better (faster)
     - ✗ Overkill
   * - High-speed storage
     - ✗ Too slow
     - ✗ Too slow
     - ✓ Perfect (NVMe)
   * - Multi-sensor systems
     - △ Address conflicts
     - ✓ Dynamic addressing
     - ✗ Not suitable
   * - Power-critical IoT
     - △ Higher power
     - ✓ Push-pull, lower power
     - ✗ High power
   * - In-band interrupts
     - ✗ Needs GPIO
     - ✓ Built-in IBI
     - ✓ MSI/MSI-X
   * - Legacy compatibility
     - ✓ Universal
     - ✓ I2C fallback
     - ✓ Widely supported

**Modern Best Practices (2026):**

1. **I2C:**
   - Use regmap API instead of raw i2c_smbus_* functions
   - Prefer device tree over manual instantiation
   - Use devm_* managed resources
   - Consider I3C for new designs

2. **I3C:**
   - Enable HDR-DDR mode for high-bandwidth sensors
   - Use IBI instead of GPIO interrupts
   - Leverage dynamic addressing for multi-sensor boards
   - Maintain I2C fallback for compatibility

3. **PCIe:**
   - Always try 64-bit DMA mask first
   - Prefer MSI-X over legacy INTx
   - Use pci_iomap() instead of ioremap()
   - Enable AER (Advanced Error Reporting) for production

4. **USB:**
   - Use USB gadget composite drivers (multi-function)
   - Implement USB PD (Power Delivery) for Type-C
   - Use UVC gadget for camera applications
   - Enable USB 3.x for high-bandwidth devices

**Common Pitfalls:**

::

    ✗ I2C: Forgetting to check chip ID in probe
    ✗ I2C: Not handling clock stretching properly
    ✗ I3C: Assuming all devices support HDR mode
    ✗ PCIe: Assuming bus address == physical address (IOMMU!)
    ✗ PCIe: Not checking DMA mask before allocation
    ✗ USB: Not handling device removal gracefully
    ✗ USB: Hardcoding endpoint addresses instead of searching

================================================================================

**Last Updated:** January 2026  
**Kernel Version:** 6.8+  
**Status:** Production Ready

================================================================================
