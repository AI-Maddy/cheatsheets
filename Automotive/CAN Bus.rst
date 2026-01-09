**cheatsheet for CAN (Controller Area Network) interfaces** in embedded systems and Linux (as of early 2026), covering hardware, protocol, Linux SocketCAN usage, kernel drivers, and debugging/porting.

📖 1. CAN Protocol Basics

| Aspect                     | Classic CAN (CAN 2.0B)             | CAN FD (Flexible Data Rate)         | CAN XL (emerging 2025–2026)       |
|----------------------------|------------------------------------|-------------------------------------|------------------------------------|
| Max payload                | 8 bytes                            | 64 bytes                            | 2048 bytes                         |
| Nominal bit rate           | 10 kbit/s – 1 Mbit/s               | 10 kbit/s – 5 Mbit/s                | 10 kbit/s – 10 Mbit/s              |
| Data phase bit rate        | —                                  | Up to 8–15 Mbit/s                   | Up to 20–100 Mbit/s                |
| Arbitration                | Non-destructive bitwise            | Same (only in nominal phase)        | Same + faster modes                |
| CRC / Error detection      | 15-bit CRC + bit stuffing + ACK    | 17/21-bit CRC + stuff count         | 32-bit CRC + enhanced detection    |
| Typical automotive rates   | 500 kbit/s (powertrain), 250 kbit/s (body) | 2–5 Mbit/s nominal, 5–8 Mbit/s data | Emerging in zonal/high-bandwidth   |
| Frame types                | Data, Remote, Error, Overload      | Same + FD variants                  | Same + XL variants                 |

📌 2. Physical Layer & Electrical

| Parameter                  | Value / Typical                              | Notes / Common Issues                      |
|----------------------------|----------------------------------------------|--------------------------------------------|
| Wiring                     | 2-wire differential (CAN_H / CAN_L) + ground | Twisted pair, 120 Ω termination at both ends |
| Voltage levels             | Recessive: ~2.5 V (both lines) <br> Dominant: CAN_H ~3.5 V, CAN_L ~1.5 V | 12 V battery systems use transceiver |
| Transceiver                | ISO 11898-2 (high-speed) / ISO 11898-3 (fault-tolerant) | TJA104x, ATA662x, MCP256x, TCAN104x |
| Cable length               | 40 m @ 1 Mbit/s, 100 m @ 500 kbit/s          | Longer with lower bit rate                 |
| Common problems            | Missing termination → reflections, ringing   | Wrong termination → bus errors             |

📚 3. Linux SocketCAN – Userspace API (most common)

| Socket Type       | Use Case                                 | Creation / Flags                             | Example Command / Code Snippet |
|-------------------|------------------------------------------|----------------------------------------------|--------------------------------|
| ``SOCK_RAW``        | Raw CAN frames (ID + data)               | ``socket(PF_CAN, SOCK_RAW, CAN_RAW)``          | ``cansend can0 123#11223344``    |
| ``SOCK_DGRAM``      | Broadcast/multicast style                | ``socket(PF_CAN, SOCK_DGRAM, CAN_BCM)``        | —                              |
| CAN FD support    | Extended payload & bit rate              | ``setsockopt(fd, SOL_CAN_RAW, CAN_RAW_FD_FRAMES, &enable, sizeof(int))`` | ``cansend can0 18ABCDEF#00112233... (64 bytes)`` |

**Basic SocketCAN send example**

.. code-block:: c

int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
struct sockaddr_can addr = {.can_family = AF_CAN, .can_ifindex = if_nametoindex("can0")};
bind(s, (struct sockaddr*)&addr, sizeof(addr));

struct canfd_frame frame = {.can_id = 0x123 | CAN_EFF_FLAG, .len = 64, .flags = CANFD_BRS};
memcpy(frame.data, payload, 64);
write(s, &frame, CANFD_MTU);

🐧 4. Linux Kernel Drivers & Modules (Embedded)

| Driver / Module          | SoC / Controller                        | Device Tree compatible example               | Typical Use Case                     |
|--------------------------|-----------------------------------------|----------------------------------------------|--------------------------------------|
| ``mcp251xfd``              | Microchip MCP2517/8FD                   | ``microchip,mcp251xfd``                        | External CAN FD controllers          |
| ``flexcan``                | NXP i.MX / Layerscape                   | ``fsl,imx6q-flexcan``                          | i.MX6/7/8 series                     |
| ``spi-mcp251x``            | Microchip MCP2515/251x (SPI)            | ``microchip,mcp2515``                          | Low-cost external CAN                |
| ``slcan``                  | USB-serial CAN adapters                 | — (userspace slcand)                         | Development & debugging              |
| ``vcan``                   | Virtual CAN                             | —                                            | Testing & simulation                 |
| ``can-gw``                 | CAN-to-CAN gateway                      | —                                            | Routing between buses                |

🐧 5. Bring-up & Configuration (Embedded Linux)

**Device Tree example (most common DWC3 + FlexCAN style)**

.. code-block:: dts

&can0 {
    status = "okay";
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_can0>;
    bitrate = <500000>;
    clock-frequency = <80000000>;
};

&can1 {
    status = "okay";
    /* ... */
};

**Interface setup commands**

.. code-block:: bash

================================================================================
Classic CAN
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



ip link set can0 type can bitrate 500000
ip link set can0 up

================================================================================
CAN FD
================================================================================

ip link set can0 type can bitrate 2000000 dbitrate 8000000 fd on
ip link set can0 up

================================================================================
🔴 Check status & errors
================================================================================

ip -details -statistics link show can0

🐛 6. Debugging & Diagnostic Commands

.. code-block:: bash

================================================================================
List interfaces
================================================================================

ip link show type can

================================================================================
🔴 Show detailed stats (errors, bus-off, etc.)
================================================================================

ip -d -s link show can0

================================================================================
💾 Send test frame
================================================================================

cansend can0 123#1122334455667788

================================================================================
Dump traffic (human-readable)
================================================================================

candump -t a can0

================================================================================
💾 CAN FD frame
================================================================================

cansend can0 18ABCDEF#00112233445566778899AABBCCDDEEFF

================================================================================
🔴 Monitor bus errors & state
================================================================================

ip monitor link

📌 7. Quick Rules of Thumb (Embedded CAN 2026)

- **Always terminate** with 120 Ω at both ends of the bus  
- **CAN FD** needs transceiver supporting FD (e.g. TCAN1044, TJA1044)  
- **Bitrate calculation** — sample point 75–85% typical  
- **Bus-off recovery** — automatic in most controllers, but monitor error counters  
- **Linux SocketCAN** — use ``SOCK_RAW`` for full control, ``CAN_RAW_FD_FRAMES`` for FD  
⭐ - **Safety-critical** — add E2E protection (AUTOSAR E2E Profile 1/2) even on CAN  
- **Physical layer** — shielded twisted pair, common-mode choke recommended  

🟢 🟢 Good luck with your CAN interface bring-up or driver porting!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
