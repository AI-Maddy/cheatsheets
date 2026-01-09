
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**functional cheatsheet for MIPI DSI** (Display Serial Interface) focused on **how it actually works functionally**, packet flows, modes, timing, commands, and typical operation sequences (MIPI DSI 1.02/1.3 + common extensions as used in 2025–2026 devices).

🎓 1. Two Fundamental Operation Modes

| Mode              | Description                                                                 | When used                              | Bandwidth usage | Power / Tear effect |
|-------------------|-----------------------------------------------------------------------------|----------------------------------------|---------------------|---------------------|
| **Command Mode**  | Host writes pixel data + DCS commands directly to panel GRAM              | Most phone/tablet/automotive panels    | Bursty (only when updating) | Low – panel can self-refresh |
| **Video Mode**    | Continuous streaming of pixel data (like HDMI) – no GRAM refresh needed   | High-refresh, large or video-oriented panels | Constant high       | Higher – no self-refresh |

**Most common in 2026 embedded/mobile**: **Command Mode** + partial update + PSR (Panel Self Refresh)

⚙️ 2. DSI Link States & Transitions (Simplified)

| State / Phase       | What happens                                      | Triggered by                  | Typical duration |
|---------------------|---------------------------------------------------|-------------------------------|------------------|
| LP-11               | Both CLK & Data lanes high (reset/idle)           | Power-on / reset              | —                |
| LP-10 → Init        | Clock lane starts toggling                        | Host enables clock            | —                |
| HS (High-Speed)     | Data lanes enter HS mode (burst)                  | After LP escape → HS prepare  | During packet    |
| BTA (Bus Turn Around) | Panel takes control of bus to send read response | After Short/Long Read         | ~few µs          |
| ULPS (Ultra Low Power State) | All lanes low-power (very low consumption)     | After long idle               | mW range         |

📚 3. Packet Structure & Types (Functional View)

| Packet Type          | Size       | Direction     | Payload? | Ack/Response? | Functional purpose                          |
|----------------------|------------|---------------|----------|---------------|---------------------------------------------|
| **Short Write**      | 4 bytes    | Host → Panel  | No       | No            | Send DCS command (most common)              |
| **Long Write**       | 6+ bytes   | Host → Panel  | Yes      | No            | Write pixel data / large register / init seq|
| **Short Read**       | 4 bytes    | Host → Panel  | No       | Yes (short)   | Read status / ID / short register           |
| **Long Read**        | 6+ bytes   | Host → Panel  | Yes      | Yes (long)    | Read large data (frame buffer, OTP, etc.)   |
| **Acknowledge & Error Report** | 2/4 bytes | Panel → Host | No       | —             | Reports ECC/CRC errors, protocol violations |
| **DCS NOP**          | —          | —             | —        | —             | Dummy packet (used for timing)              |

**Payload in Long Write** → usually starts with DCS command (0x2C = Memory Write, 0x3C = Continue Write)

📌 4. Most Frequently Used DCS Commands (Command Mode)

| Command (Hex) | Name                     | Parameters                          | Functional effect                                      | Typical timing |
|---------------|--------------------------|-------------------------------------|--------------------------------------------------------|----------------|
| 0x11          | Sleep Out                | None                                | Exit sleep – power on display                          | >120 ms wait   |
| 0x10          | Sleep In                 | None                                | Enter deep sleep (lowest power)                        | —              |
| 0x29          | Display On               | None                                | Turn on display output                                 | After init seq |
| 0x28          | Display Off              | None                                | Blank display (still powered)                          | —              |
| 0x2C          | Memory Write             | Pixel data (RGB565/666/888/...)     | Write full frame to GRAM                               | Burst transfer |
| 0x3C          | Memory Continue Write    | Pixel data                          | Continue writing from last address                     | Partial update |
| 0x2B          | Set Page Address         | 4 bytes: Ystart, Yend               | Set vertical window for partial update                 | Before 0x2C    |
| 0x2A          | Set Column Address       | 4 bytes: Xstart, Xend               | Set horizontal window                                  | Before 0x2C    |
| 0x36          | Memory Access Control    | 1 byte (MADCTL)                     | Flip/mirror/invert RGB order                           | Init sequence  |
| 0xB0–0xFF     | Vendor-specific          | Varies                              | Gamma, timing, OTP, factory calibration                | Init only      |

📚 5. Typical Command-Mode Bring-up Sequence (Functional Steps)

1. Power rails on (VDDI, VDD, etc.)
2. Reset GPIO low → high (≥10 µs pulse)
3. Wait >10–100 ms (depending on panel datasheet)
4. Send DCS commands (via Short/Long Write):
   - 0x11 Sleep Out
   - Wait ≥120 ms
   - Set gamma / voltage / timing registers (vendor)
   - 0x36 MADCTL (orientation)
   - 0x3A Pixel Format (0x77 = 24-bit, 0x66 = 18-bit, 0x55 = 16-bit)
   - 0xB0–0xFF vendor init (very panel-specific)
   - 0x29 Display On
5. Start sending 0x2C + pixel data (or use partial updates)

⚙️ 6. Partial Update / Tear Effect Synchronization

| Mechanism          | How it works                                       | Purpose / Benefit                              |
|--------------------|----------------------------------------------------|------------------------------------------------|
| **TE (Tearing Effect)** | Panel pulses TE pin at VSYNC                       | Sync host writes to 🔴 🔴 avoid tearing              |
| **Partial Update** | Set 0x2A/0x2B window → send only changed region   | Save bandwidth & power                         |
| **PSR / PSR2**     | Panel self-refreshes static image from GRAM        | Zero traffic when frame unchanged              |
| **Auto Mode**      | Some panels auto-detect changed regions            | Rare – usually host-controlled                 |

⚙️ 7. Read Operations (Much Less Common)

- Host sends Short Read (e.g. DCS 0x0A = Get Power Mode)
- Panel does **BTA** (Bus Turn Around)
- Panel sends Short Response packet
- Host reads ECC-protected 1–2 byte payload

**Most panels 🟢 🟢 do not support reliable readback** – use only during init or debug.

🔴 8. Functional Gotchas (Common Field Issues)

- **Sleep Out delay** — missing 120 ms wait → panel shows garbage
- **MADCTL wrong** → image flipped/mirrored/rainbow colors
- **Pixel format mismatch** → shifted colors or black screen
- **No TE sync in video mode** → tearing visible
- **Long Write timeout** → host stops sending mid-frame
- **Vendor init missing** → washed colors, low brightness, ghosting

This cheatsheet focuses purely on **functional operation** and real-world sequences rather than electrical D-PHY details or Linux DRM internals.

Use it when writing panel initialization sequences, debugging black/white/garbage screens, or optimizing power/bandwidth on MIPI DSI displays.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
