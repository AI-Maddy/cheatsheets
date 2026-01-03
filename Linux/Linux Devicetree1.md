**"Device tree and device type"** principle in Linux Device Tree (DT), along with clarifications, common patterns, exceptions, and best practices (based on mainline Linux kernel conventions and DT bindings guidelines as of 2026).

### Core Rule in Practice

**Standard approach (most common case)**  
→ **One node per hardware instance** (physical peripheral / device / block), **not** per unique driver / compatible string / device type.

- Each real piece of hardware gets its own DT node.
- Multiple identical (or very similar) hardware blocks → **multiple nodes**, each with the same `compatible` string.
- The kernel driver binds to the `compatible` string → one driver instance per node.

This is the overwhelming convention in mainline kernels and bindings.

### Examples: One Node per Instance (Correct & Common)

```dts
/* Four identical UART instances on the SoC */
&soc {
    uart0: serial@fe001000 {
        compatible = "snps,dw-apb-uart";
        reg = <0x0 0xfe001000 0x0 0x100>;
        interrupts = <GIC_SPI 100 IRQ_TYPE_LEVEL_HIGH>;
        clocks = <&cru CLK_UART0>;
        status = "okay";
    };

    uart1: serial@fe002000 { /* same compatible, different address/interrupt */
        compatible = "snps,dw-apb-uart";
        reg = <0x0 0xfe002000 0x0 0x100>;
        interrupts = <GIC_SPI 101 IRQ_TYPE_LEVEL_HIGH>;
        clocks = <&cru CLK_UART1>;
        status = "okay";
    };

    uart2: serial@fe003000 { /* ... */ };
    uart3: serial@fe004000 { /* ... */ };
};
```

```dts
/* Multiple I²C controllers */
i2c0: i2c@fe005000 { compatible = "snps,designware-i2c"; /* ... */ };
i2c1: i2c@fe006000 { compatible = "snps,designware-i2c"; /* ... */ };
```

```dts
/* Multiple identical GPIO controllers */
gpio0: gpio@fe100000 { compatible = "snps,dw-apb-gpio"; /* ... */ };
gpio1: gpio@fe101000 { compatible = "snps,dw-apb-gpio"; /* ... */ };
```

### When You Might See "One Node Representing Multiple Instances" (Exceptions / Special Cases)

These are **not** the rule — they are deliberate exceptions.

| Case                              | Description                                                                 | Typical compatible example                  | Why one node? |
|-----------------------------------|-----------------------------------------------------------------------------|---------------------------------------------|---------------|
| **Multi-function / MFD device**   | Single hardware block providing multiple logical functions (clocks + resets + syscon) | `syscon`, `simple-mfd`                      | Child nodes only if they have independent resources (own reg/interrupts) |
| **Multi-channel / aggregated IP** | One IP block controls multiple identical channels (e.g. multi-port Ethernet MAC) | `snps,dwmac`, some PWM drivers              | Driver manages N channels internally; channels described via sub-properties or child nodes only if needed |
| **Virtual / software aggregated** | No real separate hardware (e.g. virtual GPIO chip spanning multiple real controllers) | Rare — usually avoided                      | Driver-specific |
| **Old / deprecated patterns**     | Some very old bindings used arrays in properties instead of child nodes     | Very rare in modern mainline                | Avoid — use child nodes |

**Key guideline from kernel docs (writing bindings)**:  
> DON’T create nodes just for the sake of instantiating drivers.  
> Multi-function devices only need child nodes when the child nodes have their own DT resources.  
> **A single node can be multiple providers** (e.g. clocks + resets + syscon).

### Quick Decision Table

| Scenario                                      | Recommended DT style                          | Reason / Driver impact |
|-----------------------------------------------|-----------------------------------------------|------------------------|
| Two physically separate UARTs                 | Two nodes, same `compatible`                  | Standard — one `platform_device` per node |
| Two I²C temperature sensors on same bus       | Two child nodes under same I²C controller     | Each has own `reg` (I²C address) |
| One hardware block with 4 PWM channels        | Usually one node + `#pwm-cells` + child nodes only if channels differ significantly | Driver loops over channels |
| One IP providing clock + reset controller     | One node, multiple providers (clocks + resets)| Avoid fake child nodes |
| Multiple identical SPI NOR flashes on same SPI bus | Multiple child nodes under SPI controller | Each has own `reg` (chip select) + partitions |

### Summary – Modern Best Practice (2026 era)

- **Default mindset**: **One DT node = one hardware instance** = one `platform_device` / `i2c_client` / `spi_device` / etc.
- Use **multiple nodes** with the **same `compatible`** string when there are multiple instances of the same hardware block.
- Use **child nodes** only when:
  - Devices sit on a bus (I²C, SPI, MDIO, USB…)
  - Child has independent resources (own interrupts, reg ranges…)
  - Explicitly documented in the binding
- Avoid creating artificial nodes just to trigger driver probing — that's an anti-pattern.

This matches the philosophy in `Documentation/devicetree/bindings/writing-bindings.rst` and almost all mainline drivers/bindings.

If you're seeing a binding that violates this (one node controlling many independent instances without child nodes), it's usually because the hardware really is aggregated at the IP level, or it's legacy code that should be refactored.