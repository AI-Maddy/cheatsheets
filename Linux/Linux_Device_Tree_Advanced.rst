=============================================
Linux Device Tree Advanced Guide
=============================================

:Author: Linux Device Driver Documentation
:Date: January 2026
:Version: 1.0
:Focus: Advanced Device Tree usage, bindings, and overlays

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential DT Commands
---------------------

.. code-block:: bash

   # Compile DTS to DTB
   dtc -I dts -O dtb -o output.dtb input.dts
   
   # Decompile DTB to DTS
   dtc -I dtb -O dts -o output.dts input.dtb
   
   # Check DT syntax
   dtc -I dts -O dtb -o /dev/null -W all input.dts
   
   # View current DT
   ls /proc/device-tree/
   cat /proc/device-tree/model
   
   # sysfs DT
   ls /sys/firmware/devicetree/base/
   
   # Apply overlay (runtime)
   mkdir /sys/kernel/config/device-tree/overlays/my_overlay
   cat overlay.dtbo > /sys/kernel/config/device-tree/overlays/my_overlay/dtbo
   
   # Remove overlay
   rmdir /sys/kernel/config/device-tree/overlays/my_overlay

Quick Device Node Template
---------------------------

.. code-block:: dts

   / {
       compatible = "vendor,board";
       
       mydevice@1c00000 {
           compatible = "vendor,mydevice-v1";
           reg = <0x1c00000 0x1000>;
           interrupts = <GIC_SPI 42 IRQ_TYPE_LEVEL_HIGH>;
           clocks = <&clk_controller 15>;
           clock-names = "bus";
           resets = <&reset_controller 10>;
           reset-names = "dev_reset";
           pinctrl-names = "default";
           pinctrl-0 = <&mydev_pins>;
           status = "okay";
       };
   };

Device Tree Basics
==================

DT Structure
------------

.. code-block:: dts

   /dts-v1/;
   
   / {
       // Root node properties
       compatible = "vendor,board-name";
       model = "Vendor Board Name";
       #address-cells = <1>;
       #size-cells = <1>;
       
       // Aliases
       aliases {
           serial0 = &uart0;
           ethernet0 = &eth0;
       };
       
       // Chosen node (bootloader info)
       chosen {
           bootargs = "console=ttyS0,115200 root=/dev/mmcblk0p2";
           stdout-path = "serial0:115200n8";
       };
       
       // Memory node
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x40000000>;  // 1GB
       };
       
       // CPUs
       cpus {
           #address-cells = <1>;
           #size-cells = <0>;
           
           cpu@0 {
               device_type = "cpu";
               compatible = "arm,cortex-a53";
               reg = <0>;
               enable-method = "psci";
           };
       };
       
       // SoC node
       soc {
           compatible = "simple-bus";
           #address-cells = <1>;
           #size-cells = <1>;
           ranges;
           
           // Devices go here
       };
   };

Standard Properties
-------------------

.. code-block:: dts

   device@address {
       // Required
       compatible = "vendor,device-v1", "vendor,device";  // Most specific first
       reg = <address size>;                               // Register address/size
       
       // Common
       status = "okay" | "disabled" | "reserved" | "fail";
       interrupts = <...>;
       interrupt-parent = <&gic>;
       clocks = <&clk_ref>;
       clock-names = "ref_clk";
       resets = <&reset_ctrl 0>;
       reset-names = "dev_reset";
       
       // DMA
       dmas = <&dma 0>, <&dma 1>;
       dma-names = "rx", "tx";
       
       // GPIO
       gpios = <&gpio1 5 GPIO_ACTIVE_HIGH>;
       
       // Power domains
       power-domains = <&pd 0>;
       
       // Pinmux
       pinctrl-names = "default", "sleep";
       pinctrl-0 = <&dev_default_pins>;
       pinctrl-1 = <&dev_sleep_pins>;
       
       // Regulators
       vdd-supply = <&reg_3v3>;
       vio-supply = <&reg_1v8>;
   };

Address Translation
-------------------

.. code-block:: dts

   // #address-cells: Number of <u32> cells to encode address
   // #size-cells: Number of <u32> cells to encode size
   
   soc {
       #address-cells = <1>;  // 32-bit addresses
       #size-cells = <1>;     // 32-bit sizes
       
       // reg = <address size>
       uart@1c28000 {
           reg = <0x1c28000 0x400>;  // Address: 0x1c28000, Size: 0x400
       };
   };
   
   // 64-bit example
   / {
       #address-cells = <2>;  // 64-bit addresses
       #size-cells = <2>;     // 64-bit sizes
       
       memory@80000000 {
           // reg = <addr_high addr_low size_high size_low>
           reg = <0x0 0x80000000 0x0 0x40000000>;
       };
   };
   
   // Multiple regions
   device@1000000 {
       // Two register regions
       reg = <0x1000000 0x1000>,    // Region 0
             <0x2000000 0x2000>;    // Region 1
       reg-names = "control", "data";
   };

Ranges Property
---------------

.. code-block:: dts

   // ranges: <child_addr parent_addr size>
   // Empty ranges = identity mapping
   
   soc {
       #address-cells = <1>;
       #size-cells = <1>;
       ranges = <0x0 0x1c00000 0x400000>;  // Map child 0x0 -> parent 0x1c00000
       
       uart@0 {
           // Child address 0x0 maps to physical 0x1c00000
           reg = <0x0 0x400>;
       };
   };
   
   // Identity mapping
   soc {
       ranges;  // Child addresses = parent addresses
       
       uart@1c28000 {
           reg = <0x1c28000 0x400>;  // Already physical address
       };
   };

Advanced Bindings
=================

Interrupt Specifiers
--------------------

.. code-block:: dts

   // Standard interrupt controller
   gic: interrupt-controller@1c81000 {
       compatible = "arm,gic-400";
       #interrupt-cells = <3>;
       interrupt-controller;
       reg = <0x1c81000 0x1000>,
             <0x1c82000 0x2000>;
   };
   
   // Device using interrupts
   uart0: serial@1c28000 {
       compatible = "snps,dw-apb-uart";
       reg = <0x1c28000 0x400>;
       interrupts = <GIC_SPI 0 IRQ_TYPE_LEVEL_HIGH>;
       // GIC_SPI = SPI interrupt (shared)
       // 0 = Interrupt number
       // IRQ_TYPE_LEVEL_HIGH = Trigger type
       interrupt-parent = <&gic>;
   };
   
   // GPIO interrupt controller
   gpio: gpio@1c20800 {
       compatible = "allwinner,sun8i-h3-pinctrl";
       #gpio-cells = <3>;
       gpio-controller;
       interrupt-controller;
       #interrupt-cells = <3>;
   };
   
   button {
       compatible = "gpio-keys";
       button-power {
           label = "power";
           linux,code = <KEY_POWER>;
           gpios = <&gpio 3 7 GPIO_ACTIVE_LOW>;  // Port C, pin 7
           interrupts = <3 7 IRQ_TYPE_EDGE_FALLING>;
       };
   };

Clock Bindings
--------------

.. code-block:: dts

   // Clock controller
   ccu: clock@1c20000 {
       compatible = "allwinner,sun8i-h3-ccu";
       reg = <0x1c20000 0x400>;
       #clock-cells = <1>;
       #reset-cells = <1>;
   };
   
   // Device using clocks
   mmc0: mmc@1c0f000 {
       compatible = "allwinner,sun8i-h3-mmc";
       reg = <0x1c0f000 0x1000>;
       clocks = <&ccu CLK_BUS_MMC0>, <&ccu CLK_MMC0>;
       clock-names = "ahb", "mmc";
       resets = <&ccu RST_BUS_MMC0>;
       reset-names = "ahb";
   };
   
   // Fixed clocks
   osc24M: oscillator {
       #clock-cells = <0>;
       compatible = "fixed-clock";
       clock-frequency = <24000000>;
       clock-output-names = "osc24M";
   };
   
   // Clock consumer
   timer {
       clocks = <&osc24M>;
   };

DMA Bindings
------------

.. code-block:: dts

   // DMA controller
   dma: dma-controller@1c02000 {
       compatible = "allwinner,sun8i-h3-dma";
       reg = <0x1c02000 0x1000>;
       interrupts = <GIC_SPI 50 IRQ_TYPE_LEVEL_HIGH>;
       clocks = <&ccu CLK_BUS_DMA>;
       #dma-cells = <1>;
   };
   
   // Device using DMA
   spi0: spi@1c68000 {
       compatible = "allwinner,sun8i-h3-spi";
       reg = <0x1c68000 0x1000>;
       dmas = <&dma 23>, <&dma 23>;
       dma-names = "rx", "tx";
   };

GPIO Bindings
-------------

.. code-block:: dts

   // GPIO controller
   pio: pinctrl@1c20800 {
       compatible = "allwinner,sun8i-h3-pinctrl";
       reg = <0x1c20800 0x400>;
       #gpio-cells = <3>;
       gpio-controller;
       
       // Pin groups
       uart0_pins: uart0-pins {
           pins = "PA4", "PA5";
           function = "uart0";
       };
       
       spi0_pins: spi0-pins {
           pins = "PC0", "PC1", "PC2", "PC3";
           function = "spi0";
       };
       
       mmc0_pins: mmc0-pins {
           pins = "PF0", "PF1", "PF2", "PF3", "PF4", "PF5";
           function = "mmc0";
           drive-strength = <30>;
           bias-pull-up;
       };
   };
   
   // Using GPIO
   leds {
       compatible = "gpio-leds";
       
       led-power {
           label = "power";
           gpios = <&pio 0 10 GPIO_ACTIVE_HIGH>;  // PA10
           default-state = "on";
       };
   };
   
   // Using pinctrl
   uart0: serial@1c28000 {
       pinctrl-names = "default";
       pinctrl-0 = <&uart0_pins>;
   };

Regulator Bindings
------------------

.. code-block:: dts

   // Regulator definition
   reg_vcc3v3: vcc3v3 {
       compatible = "regulator-fixed";
       regulator-name = "vcc3v3";
       regulator-min-microvolt = <3300000>;
       regulator-max-microvolt = <3300000>;
       gpio = <&pio 0 8 GPIO_ACTIVE_HIGH>;  // Enable GPIO
       enable-active-high;
       regulator-boot-on;
       regulator-always-on;
   };
   
   // PMIC example
   axp209: pmic@34 {
       compatible = "x-powers,axp209";
       reg = <0x34>;
       interrupt-parent = <&nmi_intc>;
       interrupts = <0 IRQ_TYPE_LEVEL_LOW>;
       
       regulators {
           dcdc2: dcdc2 {
               regulator-name = "vdd-cpu";
               regulator-min-microvolt = <1000000>;
               regulator-max-microvolt = <1400000>;
               regulator-always-on;
           };
           
           ldo2: ldo2 {
               regulator-name = "avcc";
               regulator-min-microvolt = <3000000>;
               regulator-max-microvolt = <3000000>;
               regulator-always-on;
           };
       };
   };
   
   // Consumer
   cpu0: cpu@0 {
       cpu-supply = <&dcdc2>;
   };

Phandles and References
=======================

Using Phandles
--------------

.. code-block:: dts

   // Explicit phandle
   uart0: serial@1c28000 {
       phandle = <100>;
       compatible = "snps,dw-apb-uart";
       reg = <0x1c28000 0x400>;
   };
   
   // Reference by label (preferred)
   aliases {
       serial0 = &uart0;  // Reference using label
   };
   
   // Reference by phandle number
   aliases {
       serial0 = <100>;   // Reference using phandle
   };
   
   // Path reference
   aliases {
       serial0 = "/soc/serial@1c28000";
   };

Phandle with Arguments
----------------------

.. code-block:: dts

   // Provider with cells
   gpio: gpio@1c20800 {
       #gpio-cells = <3>;  // Bank, Pin, Flags
       gpio-controller;
   };
   
   intc: interrupt-controller@1c81000 {
       #interrupt-cells = <3>;  // Type, Number, Flags
       interrupt-controller;
   };
   
   // Consumer with arguments
   button {
       gpios = <&gpio 3 7 GPIO_ACTIVE_LOW>;
       //       ^     ^  ^  ^
       //       |     |  |  +-- Flags
       //       |     |  +----- Pin number
       //       |     +-------- Bank
       //       +-------------- Phandle
       
       interrupts = <GIC_SPI 42 IRQ_TYPE_LEVEL_HIGH>;
   };

Device Tree Overlays
====================

Creating Overlays
-----------------

.. code-block:: dts

   /dts-v1/;
   /plugin/;
   
   // Overlay to enable SPI0
   &{/} {
       fragment@0 {
           target = <&spi0>;
           __overlay__ {
               status = "okay";
               
               spidev@0 {
                   compatible = "spidev";
                   reg = <0>;
                   spi-max-frequency = <1000000>;
               };
           };
       };
   };
   
   // Simplified syntax
   /dts-v1/;
   /plugin/;
   
   &spi0 {
       status = "okay";
       
       spidev@0 {
           compatible = "spidev";
           reg = <0>;
           spi-max-frequency = <1000000>;
       };
   };

Multiple Fragments
------------------

.. code-block:: dts

   /dts-v1/;
   /plugin/;
   
   // I2C device overlay
   / {
       fragment@0 {
           target = <&i2c1>;
           __overlay__ {
               status = "okay";
               clock-frequency = <400000>;
           };
       };
       
       fragment@1 {
           target = <&i2c1>;
           __overlay__ {
               eeprom@50 {
                   compatible = "atmel,24c02";
                   reg = <0x50>;
                   pagesize = <16>;
               };
           };
       };
       
       fragment@2 {
           target-path = "/";
           __overlay__ {
               eeprom_alias: alias {
                   status = "okay";
               };
           };
       };
   };

Conditional Overlays
--------------------

.. code-block:: dts

   /dts-v1/;
   /plugin/;
   
   / {
       compatible = "vendor,board-v1", "vendor,board-v2";
       
       fragment@0 {
           target = <&uart1>;
           __overlay__ {
               status = "okay";
           };
       };
       
       // Only apply to v2
       __overrides__ {
           uart1 = <&uart1>,"status";
       };
   };

Runtime Overlay Application
----------------------------

.. code-block:: bash

   # Using configfs
   mkdir /sys/kernel/config/device-tree/overlays/my_device
   cat my_device.dtbo > /sys/kernel/config/device-tree/overlays/my_device/dtbo
   
   # Check overlay status
   cat /sys/kernel/config/device-tree/overlays/my_device/status
   
   # Remove overlay
   rmdir /sys/kernel/config/device-tree/overlays/my_device

.. code-block:: c

   // Kernel API
   #include <linux/of.h>
   
   int of_overlay_fdt_apply(const void *fdt, u32 *ret_ovcs_id);
   int of_overlay_remove(int *ovcs_id);
   
   // Example
   static int apply_overlay(void *overlay_data, size_t size) {
       int ovcs_id;
       int ret;
       
       ret = of_overlay_fdt_apply(overlay_data, size, &ovcs_id, NULL);
       if (ret) {
           pr_err("Failed to apply overlay\n");
           return ret;
       }
       
       pr_info("Overlay applied with ID %d\n", ovcs_id);
       return 0;
   }

Kernel Driver Integration
==========================

Parsing Device Tree
-------------------

.. code-block:: c

   #include <linux/of.h>
   #include <linux/of_device.h>
   #include <linux/of_address.h>
   #include <linux/of_irq.h>
   
   static int my_probe(struct platform_device *pdev) {
       struct device_node *np = pdev->dev.of_node;
       struct resource *res;
       int irq;
       u32 val;
       const char *str;
       
       // Read property
       if (of_property_read_u32(np, "clock-frequency", &val))
           val = 100000;  // Default
       
       // Read string
       if (of_property_read_string(np, "label", &str))
           str = "default-label";
       
       // Check property existence
       if (of_property_read_bool(np, "enable-dma"))
           enable_dma = true;
       
       // Get resource
       res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
       base = devm_ioremap_resource(&pdev->dev, res);
       
       // Get IRQ
       irq = platform_get_irq(pdev, 0);
       if (irq < 0)
           return irq;
       
       return 0;
   }

OF Match Table
--------------

.. code-block:: c

   static const struct of_device_id my_of_match[] = {
       { .compatible = "vendor,device-v2", .data = &device_v2_config },
       { .compatible = "vendor,device-v1", .data = &device_v1_config },
       { }
   };
   MODULE_DEVICE_TABLE(of, my_of_match);
   
   static struct platform_driver my_driver = {
       .probe  = my_probe,
       .remove = my_remove,
       .driver = {
           .name = "my-driver",
           .of_match_table = my_of_match,
       },
   };
   
   // Get match data
   const struct of_device_id *match;
   match = of_match_device(my_of_match, &pdev->dev);
   if (match && match->data)
       config = match->data;

Reading Arrays
--------------

.. code-block:: c

   // DT: my-array = <1 2 3 4 5>;
   
   u32 array[5];
   int count;
   
   count = of_property_count_u32_elems(np, "my-array");
   if (count > 0 && count <= ARRAY_SIZE(array)) {
       of_property_read_u32_array(np, "my-array", array, count);
   }
   
   // Variable size array
   int len;
   const __be32 *p;
   
   p = of_get_property(np, "my-array", &len);
   if (p) {
       int count = len / sizeof(u32);
       for (int i = 0; i < count; i++) {
           u32 val = be32_to_cpup(&p[i]);
           // Use val
       }
   }

GPIO Parsing
------------

.. code-block:: c

   #include <linux/of_gpio.h>
   #include <linux/gpio/consumer.h>
   
   // DT: reset-gpios = <&gpio 3 7 GPIO_ACTIVE_LOW>;
   
   struct gpio_desc *reset_gpio;
   
   reset_gpio = devm_gpiod_get(&pdev->dev, "reset", GPIOD_OUT_HIGH);
   if (IS_ERR(reset_gpio))
       return PTR_ERR(reset_gpio);
   
   // Use GPIO
   gpiod_set_value(reset_gpio, 1);
   mdelay(10);
   gpiod_set_value(reset_gpio, 0);

Clock Parsing
-------------

.. code-block:: c

   #include <linux/clk.h>
   
   // DT: clocks = <&ccu CLK_BUS_MMC0>, <&ccu CLK_MMC0>;
   //     clock-names = "ahb", "mmc";
   
   struct clk *ahb_clk, *mmc_clk;
   
   ahb_clk = devm_clk_get(&pdev->dev, "ahb");
   if (IS_ERR(ahb_clk))
       return PTR_ERR(ahb_clk);
   
   mmc_clk = devm_clk_get(&pdev->dev, "mmc");
   if (IS_ERR(mmc_clk))
       return PTR_ERR(mmc_clk);
   
   clk_prepare_enable(ahb_clk);
   clk_prepare_enable(mmc_clk);
   
   // Set rate
   clk_set_rate(mmc_clk, 50000000);

Regulator Parsing
-----------------

.. code-block:: c

   #include <linux/regulator/consumer.h>
   
   // DT: vdd-supply = <&reg_3v3>;
   
   struct regulator *vdd;
   
   vdd = devm_regulator_get(&pdev->dev, "vdd");
   if (IS_ERR(vdd))
       return PTR_ERR(vdd);
   
   regulator_set_voltage(vdd, 3300000, 3300000);
   regulator_enable(vdd);

Iterating Child Nodes
----------------------

.. code-block:: c

   struct device_node *child;
   
   for_each_child_of_node(np, child) {
       const char *name;
       u32 reg;
       
       of_property_read_string(child, "name", &name);
       of_property_read_u32(child, "reg", &reg);
       
       pr_info("Child: %s at %x\n", name, reg);
   }
   
   // Get specific child
   child = of_get_child_by_name(np, "ethernet");
   if (child) {
       // Process child
       of_node_put(child);
   }

Best Practices
==============

1. **Use compatible strings** with vendor prefix
2. **Document bindings** in yaml schema
3. **Validate DT** with dtc -W all
4. **Use standard properties** (don't invent new ones)
5. **Keep overlays simple** and focused
6. **Version compatible strings** (device-v1, device-v2)
7. **Use devm_*** functions** for automatic cleanup
8. **Check return values** from OF functions
9. **Put complex info in driver** not DT
10. **Test overlays** thoroughly before deployment

Common Pitfalls
===============

1. **Wrong cell sizes** (#address-cells, #size-cells)
2. **Missing ranges** property
3. **Circular dependencies** in phandles
4. **Incorrect interrupt specifiers**
5. **Not validating bindings** against schema
6. **Memory leaks** (not calling of_node_put)
7. **Hardcoding addresses** instead of using reg

Quick Reference
===============

.. code-block:: c

   // OF API
   of_property_read_u32(np, "prop", &val);
   of_property_read_string(np, "prop", &str);
   of_property_read_bool(np, "prop");
   of_get_property(np, "prop", &len);
   
   // GPIO
   devm_gpiod_get(&dev, "name", flags);
   gpiod_set_value(gpio, val);
   
   // Clock
   devm_clk_get(&dev, "name");
   clk_prepare_enable(clk);
   clk_set_rate(clk, rate);
   
   // Regulator
   devm_regulator_get(&dev, "name");
   regulator_enable(reg);

See Also
========

- Linux_Platform_Drivers.rst
- Linux_GPIO_Drivers.rst
- Linux_SPI_Drivers.rst
- Linux_I2C_Drivers.rst

References
==========

- Device Tree Specification: https://www.devicetree.org/
- Kernel DT bindings: Documentation/devicetree/bindings/
- OF API: https://www.kernel.org/doc/html/latest/driver-api/of.html
