**Linux Device Tree cheatsheet** (focused on modern kernels 6.x / 2025–2026 era, mainline + embedded usage).

### 1. Basic Syntax & Structure

```dts
/dts-v1/;

/ {
    model = "My Custom Board";
    compatible = "vendor,board-name", "vendor,soc-family";

    chosen {
        bootargs = "console=ttyS0,115200 earlycon=uart8250,mmio32,0xfe001000";
        stdout-path = "serial0:115200n8";
    };

    cpus {
        #address-cells = <1>;
        #size-cells = <0>;

        cpu@0 {
            device_type = "cpu";
            compatible = "arm,cortex-a76";
            reg = <0>;
        };
    };

    soc {
        #address-cells = <2>;
        #size-cells = <2>;

        uart@fe001000 {
            compatible = "snps,dw-apb-uart";
            reg = <0x0 0xfe001000 0x0 0x100>;
            interrupts = <GIC_SPI 100 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&cru CLK_UART0>;
            clock-names = "baudclk";
            status = "okay";
        };
    };
};
```

### 2. Most Important Properties (by frequency)

| Property                  | Meaning / Typical Value(s)                              | Required? | Notes / Common mistake |
|---------------------------|------------------------------------------------------------------|-----------|------------------------|
| `compatible`              | Driver matching string(s) – most important property             | Yes       | First match wins; list from specific → generic |
| `reg`                     | Address + size tuple(s)                                          | Usually   | Format depends on parent's `#address-cells`/`#size-cells` |
| `status`                  | `"okay"` / `"disabled"` – controls probing                      | No        | `"disabled"` = don't probe (save memory/power) |
| `interrupts`              | Interrupt spec (GIC: type + number + flags)                     | Often     | Use macros: `GIC_SPI`, `IRQ_TYPE_EDGE_RISING`, etc. |
| `interrupt-parent`        | Phandle to interrupt controller                                  | Often     | Usually inherited from parent node |
| `clocks` / `clock-names`  | Phandles + names of clock providers                              | Common    | Names must match driver expectation |
| `resets` / `reset-names`  | Reset controller phandles + names                                | Sometimes | Similar to clocks |
| `pinctrl-0` / `pinctrl-names` | Phandles to pinctrl states (default, sleep, etc.)           | Very common | Most drivers expect "default" |
| `phy` / `phys`            | Phandle + specifier to PHY node                                  | For USB/Ethernet/PCIe | Often needs `#phy-cells` in PHY node |
| `#address-cells` / `#size-cells` | How children `reg` is interpreted                        | On buses  | 1/0 for simple, 2/2 for 64-bit |
| `ranges`                  | Address translation from child→parent bus                        | On bridges| Critical for PCIe, simple-bus, etc. |
| `dma-coherent`            | Property presence = device supports cache-coherent DMA          | Optional  | Absence = non-coherent (needs dma-mapping API) |

### 3. Common Node Types & Their Typical Properties

| Node type              | Typical compatible examples                              | Must-have properties                          | Common children |
|------------------------|------------------------------------------------------------------|-----------------------------------------------|-----------------|
| `/cpus`                | —                                                                | `#address-cells`, `#size-cells`               | cpu@0, cpu@1…   |
| `cpu@N`                | arm,cortex-a*, riscv,etc                                         | device_type="cpu", reg                        | —               |
| `interrupt-controller` | arm,gic-v3, arm,gic-400, snps,dw-apb-ictl                       | interrupt-controller, #interrupt-cells        | —               |
| `clock-controller`     | fixed-clock, rockchip,rk3588-cru, qcom,gcc-sm8650               | #clock-cells, clocks (sometimes)              | —               |
| `serial@…`             | snps,dw-apb-uart, ns16550a, arm,pl011                           | reg, interrupts, clocks, clock-names          | —               |
| `i2c@…`                | snps,designware-i2c, cdns,i2c-r1p14                             | reg, interrupts, #address-cells=1, #size-cells=0 | child devices   |
| `spi@…`                | spi-dw, cdns,spi-r1p0                                           | reg, interrupts, #address-cells, #size-cells  | spi slaves      |
| `mmc@…` / `sdhci@…`    | snps,dw-mshc, arm,pl18x                                         | reg, interrupts, clocks, bus-width            | —               |
| `ethernet@…`           | snps,dwmac, cadence,macb                                        | reg, interrupts, phy-handle or mdio subnode   | mdio {}         |
| `usb@…`                | snps,dwc3, nxp,imx8mp-usb                                       | reg, interrupts, dr_mode="host/peripheral/otg"| usb-phy, phys   |
| `pci@…`                | pcie-snps, snps,dw-pcie                                         | reg, ranges, dma-coherent (often), #address-cells=3 | —               |
| `simple-bus`           | simple-bus, simple-mfd                                           | compatible, ranges                            | many peripherals|

### 4. Useful Standard / Helper Macros (include/dt-bindings/)

```c
// include/dt-bindings/interrupt-controller/irq.h
IRQ_TYPE_NONE
IRQ_TYPE_EDGE_RISING
IRQ_TYPE_EDGE_FALLING
IRQ_TYPE_EDGE_BOTH
IRQ_TYPE_LEVEL_HIGH
IRQ_TYPE_LEVEL_LOW

// include/dt-bindings/clock/…
CLK_PARENT, CLK_FIXED, etc.

// GIC interrupt types
GIC_SPI     // Shared Peripheral Interrupt
GIC_PPI     // Private Peripheral Interrupt
GIC_SGI     // Software Generated Interrupt

// include/dt-bindings/gpio/gpio.h
GPIO_ACTIVE_HIGH
GPIO_ACTIVE_LOW
GPIO_OPEN_DRAIN
```

### 5. Debugging & Validation Tips

```bash
# Compile DTS → DTB
dtc -I dts -O dtb -o myboard.dtb myboard.dts

# Decompile DTB → DTS (readable)
dtc -I dtb -O dts -o output.dts /boot/dtb/myboard.dtb

# Check boot-time parsing
dmesg | grep -i "OF_"     # OF = OpenFirmware = Device Tree
dmesg | grep -i "of_"     # of_* functions

# Runtime inspection
cat /proc/device-tree/compatible
find /proc/device-tree/ -name status -exec grep -H . {} \;
ls /proc/device-tree/soc/uart@fe001000/

# dtc warnings & strict checking
dtc -I dts -O dtb -o test.dtb -W no_unit_address_vs_reg myboard.dts

# dtc -I fs /proc/device-tree   # live checks on running system
```

### 6. Quick Reference: Address Translation (`ranges`)

```dts
soc {
    #address-cells = <2>;
    #size-cells = <2>;

    simple-bus@0 {
        compatible = "simple-bus";
        ranges = <0x0 0x0  0x0 0xfe000000  0x0 0x1000000>;  // child 0x0.. → parent 0xfe000000..
    };
};
```

Good luck with your Device Tree work — most pain comes from mismatched `#*-cells`, wrong compatible strings, or missing/misordered `ranges`. Start with mainline reference boards (qemu, rockchip, allwinner, amlogic, etc.) as templates.