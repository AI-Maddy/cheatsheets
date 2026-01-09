
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **3 concise cheat sheets** for the three MIPI standards you mentioned: **MIPI I3C**, **MIPI DSI**, and **MIPI I3C** (with a focus on key differences from legacy I²C, as it's commonly compared). These are practical quick-reference summaries based on the latest available specs (I3C v1.1.1+, DSI-2 v2.x / DCS v2.1 as of 2026).

📌 1. MIPI I3C Cheat Sheet – Core Features & Comparison to I²C

**Purpose** — Modern successor to I²C for sensors / peripherals (lower power, higher speed, in-band interrupts, dynamic addressing).

| Feature                  | I3C (v1.1+)                              | I²C (legacy)                          | Winner / Notes
|--------------------------|------------------------------------------|---------------------------------------|---------------
**Wires**                | 2 (SDA + SCL)                            | 2 (SDA + SCL)                         | Same
**Max SDR speed**        | ~12.5 Mbps (typ. 11.1 Mbps effective)    | FM+ = 1 Mbps                          | I3C ~10× faster
**HDR modes**            | HDR-DDR (~25 Mbps), HDR-TSP/TSL (~~33–50 Mbps ternary) | None                                  | I3C only
**Addressing**           | Dynamic (7-bit after ENTDAA CCC) + static fallback | Static 7/10-bit                       | I3C (hot-join, auto-assign)
**Pull-up / Drive**      | Open-drain start → push-pull after       | Always open-drain                     | I3C lower power
**In-band interrupt**    | Yes (IBI) – no extra wire                | No – needs IRQ pin                    | I3C
**Hot-join**             | Yes (devices join live bus)              | No                                    | I3C
**Multi-controller**     | Yes (dynamic role change)                | Rare (multi-master collision risky)   | I3C
**Backward compat.**     | Yes – I²C devices work on I3C bus        | —                                     | I3C
**Power per bit**        | Much lower at high speed                 | Higher                                | I3C
**Common Command Codes (CCC)** | Broadcast / Directed (see below)         | None standardized                     | I3C

⭐ **Most Important CCCs (Common Command Codes)** — used for bus management

Code (Hex) | Name          | Type       | Purpose
-----------|---------------|------------|---------
0x01       | ENTDAA        | Broadcast  | Enter Dynamic Address Assignment
0x02       | RSTACT        | Dir/Bcast  | Target Reset Action
0x06       | ENTHDR        | Broadcast  | Enter HDR mode (followed by HDR code)
0x07       | EXITPTRN      | Broadcast  | Exit HDR / restart SDR
0x09       | GETMWL        | Directed   | Get Max Write Length
0x0A       | GETMRL        | Directed   | Get Max Read Length
0x0B       | GETPID        | Directed   | Get Provisional ID
0x0D       | GETBCR        | Directed   | Get Bus Characteristic Register
0x0E       | GETDCR        | Directed   | Get Device Characteristic Register
0x0F       | GETSTATUS     | Directed   | Get status / events
0x10       | GETCAPS       | Directed   | Get capabilities
0x11       | SETNEWDA      | Directed   | Set new dynamic address
0x1F       | DISEC         | Bcast/Dir  | Disable Events (IBI, Hot-Join, …)
0x20       | ENEC          | Bcast/Dir  | Enable Events

**Quick Rule** — Start with ENTDAA after bus init → use private SDR transfers like I²C → enable HDR for bulk data.

📌 2. MIPI DSI Cheat Sheet – Display Serial Interface

**Purpose** — High-speed serial link from SoC → display panel (LCD/OLED) using D-PHY.

| Feature               | Details / Values
|-----------------------|---------------------
**Physical Layer**    | MIPI D-PHY (HS + LP modes), 1–4 data lanes + 1 clock lane
**Modes**             | Command Mode (with frame buffer in panel) vs Video Mode (continuous streaming)
**Data Types (short packet)** | 0x05–0x37 (sync events), 0x01–0x03 (RGB), etc.
**Packet Types**      | Short (4 bytes) — commands, sync<br>Long (header + payload + ECC/CRC) — pixel data, DCS commands
**Pixel Formats**     | RGB888 (0x24), RGB666 (0x22), RGB565 (0x21), YCbCr, etc.
**Typical Speeds**    | HS mode: 80–2500 Mbps/lane (2026 common: 1.5–2.5 Gbps/lane)
**Compression**       | Optional VESA DSC (Display Stream Compression)
**Turn-around (BTA)** | Lane 0 bidirectional for readback / status

⭐ **Key Initialization Sequence (Command Mode – typical)**

1. LP-11 state (reset/power-on)
2. Send DCS commands via Long Write (Data Type 0x39) or Short Write (0x05/0x15)
3. Common first commands: 0x11 (Exit Sleep), 0x29 (Display ON)
4. Set column/row address (0x2A / 0x2B)
5. Memory Write (0x2C) → send pixel data in bursts

**Most Common DCS Commands** (Display Command Set – from panel driver IC datasheet)

Code (Hex) | Name                     | Type     | Typical Use
-----------|--------------------------|----------|------------
0x11       | Exit Sleep Mode          | Write    | Power on display
0x29       | Set Display ON           | Write    | Show content
0x28       | Set Display OFF          | Write    | Blanking
0x10       | Enter Sleep Mode         | Write    | Power saving
0x2C       | Memory Write             | Long     | Send full frame (RGB data)
0x3C       | Memory Write Continue    | Long     | Burst continuation
0x2A       | Set Column Address       | Write    | x-start, x-end
0x2B       | Set Page Address         | Write    | y-start, y-end
0x36       | Memory Access Control    | Write    | Flip/mirror (MADCTL)
0xB0–0xFF  | Manufacturer-specific    | —        | Gamma, power control, etc.

📌 3. MIPI I3C vs MIPI DSI – Quick Side-by-Side Comparison

(For context when both appear in mobile/embedded SoCs)

Aspect                  | MIPI I3C                                   | MIPI DSI                                   | Typical Use
------------------------|--------------------------------------------|--------------------------------------------|--------------------
**Main Purpose**        | Sensor / peripheral control & data         | Display output (high-res video / graphics) | I3C = sensors, DSI = screen
**Wires**               | 2 (SDA/SCL)                                | 3–5+ (CLK + 1–4 Data lanes)                | I3C fewer pins
**Speed (typ. 2026)**   | SDR 12.5 Mbps, HDR up to ~50 Mbps          | 1–10+ Gbps total (multi-lane)              | DSI much faster
**Topology**            | Multi-drop bus (many targets)              | Point-to-point (host → panel)              | I3C shared bus
**Data Flow**           | Bidirectional, small packets               | Mostly unidirectional (host → display), occasional readback
**Power Focus**         | Very low (push-pull + in-band int)         | High bandwidth, higher power               | I3C for always-on sensors
**Typical Devices**     | Accelerometer, gyro, temp, ALS, …          | LCD/OLED panels, touch sometimes via I3C   | —
**Linux Drivers**       | i3c core + per-device                      | drm/panel + mipi-dsi                       | —
**Backward Compat.**    | With I²C slaves                            | None (dedicated)                           | I3C wins

These cheat sheets cover the 80/20 most-used parts in real designs (kernel drivers, embedded bring-up, debugging with protocol analyzers). For full details → MIPI Alliance specs (member access) or public whitepapers / Linux kernel docs (drivers/i3c/, drivers/gpu/drm/panel/, drivers/staging/media/). If you need one expanded (e.g. full HDR modes, more DCS commands, or Linux examples), let me know!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
