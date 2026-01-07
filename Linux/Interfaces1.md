### 1. CAN (Controller Area Network) Cheatsheet

**Purpose**  
Robust, real-time, multi-master serial bus – standard in automotive and industrial control.

| Aspect                  | Classic CAN (2.0B)                  | CAN FD (Flexible Data-rate)         | CAN XL (2024–2026 emerging)       |
|-------------------------|-------------------------------------|-------------------------------------|------------------------------------|
| Max data payload        | 8 bytes                             | 64 bytes                            | 2048 bytes                         |
| Bit rate                | 1 Mbit/s max                        | Nominal 1–5 Mbit/s, data phase up to 8–15 Mbit/s | Up to 20–100 Mbit/s (data phase)   |
| Arbitration             | Non-destructive bitwise             | Same (CAN FD only in nominal phase) | Same + higher-speed modes          |
| Error detection         | CRC + bit stuffing + ACK + form     | Enhanced CRC + stuff count          | Even stronger CRC                  |
| Typical use             | Powertrain, chassis, body           | ADAS, gateways, zonal ECUs          | High-bandwidth backbone (future)   |
| Dominant standard (2026)| Still very common                   | Dominant in new vehicles            | Early adoption (high-end)          |

**Key electrical / physical**  
- Differential 2-wire (CAN_H / CAN_L)  
- 120 Ω termination resistors at both ends  
- Recessive = 2.5 V (both lines), Dominant = CAN_H 3.5 V, CAN_L 1.5 V

**Common bit rates (automotive)**  
500 kbit/s (powertrain), 250 kbit/s (comfort), 125 kbit/s (body), CAN FD 2 Mbit/s nominal / 5–8 Mbit/s data

**Linux / SocketCAN commands**  
```bash
ip link set can0 type can bitrate 500000 dbitrate 2000000 fd on
ip link set can0 up
cansend can0 123#1122334455667788
candump can0
```

### 2. SPI (Serial Peripheral Interface) Cheatsheet

**Purpose**  
Fast, synchronous, full-duplex, master–slave, short-distance chip-to-chip communication.

| Aspect               | Value / Typical                              | Notes / Variants                           |
|----------------------|----------------------------------------------|--------------------------------------------|
| Speed                | 1–100 MHz (common 1–50 MHz)                  | Limited by PCB trace length & capacitance  |
| Lines                | 4-wire: MOSI, MISO, SCLK, /SS (chip select)  | 3-wire possible (MOSI bidirectional)       |
| Master / Slave       | Always master-initiated                      | Multi-slave via multiple /SS lines         |
| Clock modes (CPOL/CPHA) | 0,1,2,3 (idle low/high + sample edge)     | Must match exactly between master & slave  |
| Data frame           | 4–32 bits (most common 8-bit)                | MSB-first or LSB-first                     |
| Typical devices      | Flash (NOR/NAND), sensors, displays, codecs, ADCs/DACs, Ethernet PHY | —                                          |
| Voltage levels       | 1.8 V, 3.3 V, 5 V                            | Level shifters needed if mixed             |

**Common gotchas**  
- Clock polarity & phase must match  
- /SS must be toggled per transaction (or held low for streaming)  
- No built-in error detection (add CRC/checksum if needed)  
- High speed → PCB layout critical (short traces, ground plane)

**Linux spidev example**  
```c
int fd = open("/dev/spidev0.0", O_RDWR);
uint8_t tx[] = {0x9F, 0x00, 0x00, 0x00}; // JEDEC ID read
struct spi_ioc_transfer tr = { .tx_buf = (unsigned long)tx, .len = 4, .speed_hz = 10000000 };
ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
```

### 3. I²C (Inter-Integrated Circuit) / I3C Cheatsheet

**Purpose**  
Low-speed, 2-wire, multi-master/multi-slave, chip-to-chip control & configuration.

| Aspect                  | I²C (classic)                              | I3C (improved successor)                     |
|-------------------------|--------------------------------------------|----------------------------------------------|
| Speed                   | Standard 100 kHz, Fast 400 kHz, Fast+ 1 MHz, High-speed 3.4 MHz | SDR up to 12.5 MHz, HDR-DDR up to 33 Mbit/s  |
| Lines                   | SDA + SCL (open-drain)                     | Same (push-pull + open-drain modes)          |
| Addressing              | 7-bit or 10-bit                            | 7-bit dynamic + static fallback              |
| Max devices             | ~128 (7-bit)                               | Higher (dynamic addressing)                  |
| Features                | Clock stretching, multi-master arbitration | In-band interrupt (IBI), hot-join, dynamic addr |
| Typical devices         | Sensors, EEPROM, codecs, RTC, display controllers | Same + newer high-speed sensors              |
| Pull-up resistors       | 1–10 kΩ (usually 4.7 kΩ @ 3.3 V)           | Much weaker (higher speed)                   |

**I²C common addresses**  
- 0x50–0x57 → EEPROM  
- 0x68 → MPU-6050 / accel+gyro  
- 0x3C/0x3D → OLED displays  
- 0x1C–0x1F → many sensors

**Linux i2c-tools**  
```bash
i2cdetect -y 1                  # scan bus 1
i2cget -y 1 0x50 0x00           # read byte at address 0x00 from device 0x50
i2cset -y 1 0x50 0x00 0xAA      # write 0xAA to register 0x00
```

### 4. LIN (Local Interconnect Network) Cheatsheet

**Purpose**  
Low-cost, single-wire, deterministic, master–slave communication – used for non-safety-critical automotive body functions.

| Aspect                  | Value / Typical                              | Notes / Variants                           |
|-------------------------|----------------------------------------------|--------------------------------------------|
| Speed                   | 1–20 kbit/s (most common 19.2 kbit/s)        | Slow, but very robust                      |
| Topology                | Single-wire + ground (12 V battery ref)      | Up to 16 nodes                             |
| Master–Slave            | Single master, up to 15 slaves               | Master controls schedule                   |
| Frame structure         | Break (13–16 bit low) + Sync (0x55) + ID + Data (0–8 bytes) + Checksum | Enhanced checksum (LIN 2.x)                |
| Protocol versions       | LIN 1.x → LIN 2.0 → LIN 2.1 → LIN 2.2 (most common) | LIN 2.2A adds diagnostic frames            |
| Typical devices         | Window motors, mirrors, seats, lights, rain sensors, steering wheel buttons | —                                          |
| Voltage                 | 12 V dominant, recessive ≈ battery voltage   | Needs transceiver (e.g. ATA662x, TJA102x)  |

**Key timing**  
- Bit time: ~52 µs @ 19.2 kbit/s  
- Frame time: ~5–15 ms typical  
- Schedule table: deterministic, master-defined

**Linux SocketCAN support** (slcan or native drivers)  
```bash
# Example with slcan (USB LIN adapter)
slcan_attach -f /dev/ttyUSB0 -o /dev/slcan0
ip link set slcan0 up type can bitrate 19200
cansend slcan0 123#11223344
candump slcan0
```

**Quick comparison table – when to choose which**

| Requirement                     | CAN                          | SPI                           | I²C / I3C                       | LIN                           |
|---------------------------------|------------------------------|-------------------------------|----------------------------------|-------------------------------|
| Speed                           | High (1–8 Mbit/s)            | Very high (1–100 MHz)         | Medium–high (up to 33 Mbit/s)    | Very low (20 kbit/s)          |
| Wires                           | 2 (diff)                     | 4 (or 3)                      | 2                                | 1 + ground                    |
| Distance                        | 40 m                         | < 30 cm                       | < 1 m                            | 40 m                          |
| Cost / complexity               | Medium                       | Low                           | Very low                         | Very low                      |
| Deterministic / real-time       | Very good                    | Excellent                     | Good (clock stretching risk)     | Excellent (master schedule)   |
| Typical automotive use          | Powertrain, ADAS             | Flash, sensors, displays      | Sensors, EEPROM, codecs          | Body, comfort functions       |

Good luck with your embedded communication bring-up!