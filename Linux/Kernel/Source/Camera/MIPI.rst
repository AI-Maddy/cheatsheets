
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**MIPI Alliance Cheat Sheet** (as of early 2026 — based on MIPI specifications up to ~v4.1 for CSI-2, v2.x for DSI-2, v1.2 for I3C Basic, C-PHY v3.0+, D-PHY v2.x+, A-PHY v2.0).

MIPI Alliance defines the most widely used interfaces in smartphones, tablets, automotive ADAS, IoT cameras/displays, laptops, and industrial vision.

📖 1. MIPI Overview – Main Interfaces Quick Table

⭐ Interface       | Full Name                          | Primary Use                          | Physical Layer Options          | Typical Max Speed (2026)       | Lanes / Wires                  | Key Applications (2026)
---------------|------------------------------------|--------------------------------------|---------------------------------|--------------------------------|--------------------------------|---------------------------
**CSI-2**      | Camera Serial Interface 2          | Image sensor → processor             | D-PHY / C-PHY / A-PHY / I3C     | ~6–10+ Gbps total (multi-lane) | 1–4 data + clock (D-PHY) / trios (C-PHY) | Smartphones, automotive cameras, machine vision, drones
**DSI / DSI-2**| Display Serial Interface / v2      | Processor → display panel            | D-PHY / C-PHY                   | ~2.5–10+ Gbps/lane             | 1–4 data + clock               | OLED/AMOLED/LCD in phones, laptops, AR/VR, automotive clusters
**I3C / I3C Basic** | Improved Inter-Integrated Circuit | Sensors, control, low-speed peripherals | 2-wire (SDA+SCL)               | SDR ~12.5 Mbps, HDR ~25–50 Mbps | 2 wires                        | Always-on sensors, power mgmt, debug, bridge to legacy I²C
**C-PHY**      | —                                  | High-speed short-reach PHY           | 3-phase tri-level signaling     | Up to ~6–8 Gsym/s/trio (~17–24 Gbps effective) | 3 wires per trio               | Next-gen high-res cameras & displays (replaces D-PHY in many designs)
**D-PHY**      | —                                  | Legacy high-speed PHY                | Differential HS + LP            | Up to ~2.5–4.5 Gbps/lane       | 2 wires per lane + clock       | Still dominant in cost-sensitive & legacy products
**A-PHY**      | Automotive SerDes Payload          | Long-reach automotive connectivity   | Asymmetric SerDes               | Up to 16–48 Gbps (v2.0)        | Coax / shielded twisted pair   | ADAS, in-vehicle infotainment, zonal architecture (mass production started 2025–2026)

📌 2. PHY Comparison – C-PHY vs D-PHY vs I3C (most frequent choices)

Feature                  | MIPI C-PHY (v3.0+)                  | MIPI D-PHY (v2.x)                   | MIPI I3C / I3C Basic (v1.2)
-------------------------|-------------------------------------|-------------------------------------|-----------------------------------
**Signaling**            | 3-level (ternary) per trio          | 2-level differential HS + single LP | Push-pull after init (from open-drain)
**Effective bits/symbol** | ~2.28 bits (6→3 wire-state coding)  | 1 bit (DDR)                         | 1 bit (SDR/HDR modes)
**Power efficiency**     | 🟢 🟢 Best (~30–50% better than D-PHY)    | 🟢 🟢 Good                                | Excellent for low/medium speed
**EMI / emissions**      | Lowest (no clock lane needed)       | Higher                              | Very low
**Reach**                | Up to ~4–8 m (with 🟢 🟢 good PCB)        | Up to ~4 m                          | Short (board-level)
**Pin count (4-lane equiv.)** | 9 wires (3 trios)                | 10 wires (4 lanes + clock)          | 2 wires
**Backward compat.**     | No (new designs)                    | Yes (still everywhere)              | Yes – full I²C slave compat.
**Typical 2026 choice**  | High-res / high-FPS cameras & displays | Cost-optimized / legacy             | Always-on sensors, control bus

⭐ 📨 3. CSI-2 Cheat Sheet – Most Important Packet / Data Types (2026 – v4.1)

Category              | Data Type (Hex) | Description / Use-case
----------------------|-----------------|--------------------------------------
**Frame sync**        | 0x00            | Frame Start – Short packet
0x01–0x03             | Frame End variants
**Line sync**         | 0x10–0x17       | Line Start / End (optional)
**Raw Bayer**         | 0x28–0x2F       | RAW6/7/8/10/12/14/16/20 (most sensors)
**RGB**               | 0x24            | RGB888 (common)
0x21–0x23             | RGB565/666/555
**YUV / compressed**  | 0x2C–0x2F       | YUV422 8/10-bit, JPEG, etc.
**User-defined**      | 0x30–0x37       | Metadata, embedded data lines
**Virtual channels**  | —               | Up to 32 (v2.0+), great for multi-camera / stereo

⭐ **Key 2026 features**:
- Always-On Sentinel Conduit (AOSC) — ultra-low-power sentinel frames
- Unified Serial Link (USL) over I3C — low-pin camera control
- Smart Region of Interest (SROI) — AI/machine-vision friendly cropping

📌 4. DSI / DSI-2 Cheat Sheet – Common DCS Commands

Command (Hex) | Name                        | Typical Use
--------------|-----------------------------|---------------------
0x11          | Exit Sleep                  | Power on / wake display
0x29          | Display ON                  | Start showing pixels
0x28          | Display OFF                 | Blank screen
0x10          | Enter Sleep                 | Power saving
0x2C          | Memory Write                | Send full frame RGB data
0x3C          | Memory Write Continue       | Burst continuation
0x2A          | Set Column Address          | x-start / x-end
0x2B          | Set Page Address            | y-start / y-end
0x36          | Memory Access Control (MADCTL) | Rotation / mirror / color order
0xB0–0xFF     | Vendor-specific             | Gamma, contrast, power, etc.

**Modes**:
- **Command Mode** — panel has frame buffer → low power, sporadic writes
- **Video Mode** — continuous streaming → burst mode, higher bandwidth

🏗️ Quick Decision Tree (2026 embedded designs)

- High-res camera (8K/120fps / multi-camera) → CSI-2 over **C-PHY**
- Automotive long-reach (>4 m) → CSI-2 over **A-PHY**
- Low-cost / legacy camera → CSI-2 over **D-PHY**
- Always-on sensor array / control → **I3C**
- High-res OLED/AMOLED display → DSI-2 over **C-PHY**
- Cost-sensitive / older panel → DSI over **D-PHY**

📚 Linux Ecosystem Quick Reference (2026)

Subsystem       | Main drivers / bindings
----------------|-------------------------
Camera          | v4l2 + media-controller + libcamera (embedded) / direct v4l2 (USB fallback)
Display         | drm/panel-simple + panel drivers (panel-simple for custom DCS init)
PHY             | phy-mipi-dphy / phy-c-phy / phy combo drivers
I3C             | i3c core (drivers/i3c/)

MIPI remains the dominant ecosystem for imaging & display in mobile/embedded/automotive — with **C-PHY + CSI-2 v4.1** and **A-PHY** seeing the fastest adoption in new 2025–2026 designs.

If you want a deeper dive into one part (CSI-2 packet format, C-PHY signaling states, A-PHY in automotive, Linux examples, etc.), let me know!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
