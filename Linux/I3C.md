**cheatsheet for I3C** (Improved Inter Integrated Circuit) – the modern successor to I²C, designed for sensors, mobile, IoT, and low-power embedded systems (as of 2026, widely adopted in new SoCs, sensors from Bosch, ST, TI, etc.).

### 1. I3C vs I²C Quick Comparison

| Feature                  | I²C (Classic)                  | I3C (MIPI I3C / I3C Basic)                  | Winner / Notes |
|--------------------------|--------------------------------|----------------------------------------------|----------------|
| Max Speed                | 400 kHz (std), 1 MHz (FM+)     | Up to 12.5 MHz (SDR), 33 MHz (HDR-DDR)       | I3C            |
| Data Rate (effective)    | ~0.4–1 Mbit/s                  | Up to ~33 Mbit/s (HDR modes)                 | I3C            |
| Bus Topology             | Multi-master, open-drain       | Single master (dynamic), push-pull + open-drain | I3C            |
| Addressing               | 7-bit or 10-bit                | 7-bit dynamic + static (I3C Basic)           | I3C            |
| In-band Interrupts       | No (needs extra pin)           | Yes (IBI)                                    | I3C            |
| Hot-join                 | No                             | Yes                                          | I3C            |
| Dynamic Address Assignment | No                           | Yes (via CCC)                                | I3C            |
| Backward Compatibility   | —                              | I3C devices can fall back to I²C mode        | I3C            |
| Power Consumption        | Higher (open-drain pull-ups)   | Lower (push-pull + smaller pull-ups)         | I3C            |
| Pins Required            | 2 (SDA + SCL)                  | 2 (SDA + SCL), optional 3rd for HDR          | Tie            |

### 2. Key I3C Modes & Data Rates

| Mode          | Abbreviation | Data Rate (typical) | Encoding / Features                          | Use Case / Notes |
|---------------|--------------|----------------------|----------------------------------------------|------------------|
| Standard Data Rate | SDR         | Up to ~12.5 MHz     | Open-drain + push-pull fallback              | Default / I²C-like |
| High Data Rate – DDR | HDR-DDR   | Up to ~25–33 Mbit/s | Double Data Rate (rising + falling edge)     | High-throughput sensors |
| High Data Rate – TSP | HDR-TSP   | Similar to DDR      | Ternary Symbol Pure (3-level signaling)      | Power-efficient, newer |
| High Data Rate – TSL | HDR-TSL   | Similar             | Ternary Symbol Legacy (back-compat)          | Mixed buses      |
| High Data Rate – TS4 | HDR-TS4   | Higher efficiency   | 4-level ternary (experimental/2025+)         | Future high-speed |

**Most common in 2026**: SDR (for compatibility) + HDR-DDR (for bandwidth).

### 3. I3C Roles & Addressing

| Role                  | Description                                      | Dynamic Address? | Static Address? |
|-----------------------|--------------------------------------------------|------------------|-----------------|
| **Main Controller**   | Only one active at a time (no multi-master)      | —                | Yes (7-bit)     |
| **I3C Target**        | Slave device (sensor, EEPROM, etc.)              | Yes (assigned)   | Yes (optional)  |
| **I3C Secondary Controller** | Can request bus ownership (hot-join / IBI) | Yes              | Yes             |

- **Dynamic Address** (DA): 7-bit, assigned at runtime via `SETDASA` / `SETNEWDA` CCC
- **Static Address** (SA): 7-bit I²C-compatible fallback
- **Broadcast Address**: `7’h7E` (for Common Command Codes – CCC)

### 4. Most Important Common Command Codes (CCC)

| CCC Code (Direct) | Name              | Purpose / When used                              | Broadcast? |
|-------------------|-------------------|--------------------------------------------------|------------|
| 0x06              | ENTDAA            | Enter Dynamic Address Assignment                 | Yes        |
| 0x07              | RSTDAA            | Reset Dynamic Address Assignment                 | Yes        |
| 0x08              | SETDASA           | Set Dynamic Address from Static                  | Yes        |
| 0x0A              | GETMWL / SETMWL   | Get/Set Max Write Length                         | Direct     |
| 0x0B              | GETMRL / SETMRL   | Get/Set Max Read Length                          | Direct     |
| 0x0C              | ENTHDR            | Enter HDR mode (DDR/TSP/TSL)                     | Yes        |
| 0x1F              | GETPID            | Get Provisional ID (48-bit unique)               | Direct     |
| 0x20              | GETBCR            | Get Bus Characteristics Register                 | Direct     |
| 0x21              | GETDCR            | Get Device Characteristics Register              | Direct     |
| 0x29              | CCC_ENEC / DISEC  | Enable/Disable Events (IBI, Hot-Join, etc.)      | Direct     |

### 5. Key Features & Signals

| Feature              | How it works / Pins involved                     | Benefit |
|----------------------|--------------------------------------------------|---------|
| **In-Band Interrupt (IBI)** | Target pulls SDA low during 7th ACK bit          | Saves GPIO pin |
| **Hot-Join**         | New device pulls SDA low after reset/power-up    | Plug-and-play |
| **Push-Pull**        | Controller drives SCL/SDA high/low actively      | Faster rise time, lower power |
| **SDA Pull-up**      | Much weaker (1–4 kΩ) than I²C (often 10–100 kΩ)  | Power savings |
| **Error Detection**  | Parity bit + CRC (in HDR modes)                  | Better reliability |

### 6. Typical Device Registers (BCR / DCR)

**Bus Characteristics Register (BCR)** – 8 bits

| Bit | Meaning |
|-----|---------|
| 7   | IBI support |
| 6   | IBI payload (has data byte) |
| 5   | Hot-Join support |
| 4   | HDR capable |
| 3   | HDR-DDR support |
| 2–0 | Reserved / future |

**Device Characteristics Register (DCR)** – 8 bits (examples)

- 0x0C = Generic I3C sensor
- 0x48 = Temperature sensor
- 0x4A = Accelerometer

### 7. Debugging & Tools (2026 era)

```bash
# Linux kernel I3C support (since ~5.10, mainline)
modprobe i3c_master

# Sysfs inspection
ls /sys/bus/i3c/devices/
cat /sys/bus/i3c/devices/i3c-*/dynamic_address
cat /sys/bus/i3c/devices/i3c-*/bcr
cat /sys/bus/i3c/devices/i3c-*/pid

# i3c-tools (userspace, similar to i2c-tools)
i3cdetect -y 0
i3cget -y 0 0x08  # read BCR from dynamic addr 0x08
i3cset -y 0 0x08 0x0A 0x04  # example SETMWL

# Protocol analyzers
Total Phase Beagle I3C, Teledyne LeCroy, Saleae Logic Pro (with I3C decoder)
```

### 8. Adoption & Status (early 2026)

- **Very common** in new mobile SoCs (Qualcomm Snapdragon 8 Gen 3+, MediaTek Dimensity 9300+, Google Tensor G4+)
- **Sensors**: Bosch BMI323, ST LSM6DSV, TI TMP144, many new accelerometers/gyros
- **Backward compat**: Almost all I3C devices support I²C fallback (useful during bring-up)
- **Linux mainline support**: Solid since kernel 6.1–6.12 (drivers/i3c/)
- **I3C Basic** (royalty-free subset) widely used in cost-sensitive designs

**Quick mnemonic**:  
I3C = **I²C + In-Band interrupts + 3× speed + Dynamic addressing + lower power**

Good luck integrating I3C sensors or controllers! Start with SDR mode for simplicity, then enable HDR-DDR once stable.