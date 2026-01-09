**cheatsheet for the PCIe Data Link Layer** (DLL) – PCIe 3.0 to 6.0 era (valid ~2025–2026 perspective).  
⭐ Focuses on the most important mechanisms, packet types, sequencing, retry, flow control, and key behaviors seen by driver developers and hardware engineers.

📌 1. Data Link Layer – Core Responsibilities

- Reliable delivery of **TLPs** (Transaction Layer Packets) over the link
- Adds **Sequence Number** + **LCRC** (Link CRC)
- Implements **ACK/NAK** protocol + replay buffer
- Manages **Flow Control** (credit-based)
- Handles **DLLPs** (Data Link Layer Packets) for link management
- Link error detection & recovery (together with Physical layer)

📨 2. DLLP Types (Data Link Layer Packets)

| DLLP Type              | Purpose / When sent                                      | Typical Payload | Direction     | Reliability |
|------------------------|------------------------------------------------------------------|-----------------|---------------|-------------|
| Ack                    | Acknowledge received TLPs up to sequence number N-1              | Sequence #      | Both          | Unreliable  |
| Nak                    | Negative acknowledge – replay from Nak sequence number           | Sequence #      | Both          | Unreliable  |
| InitFC1 / InitFC2      | Initial Flow Control credits (sent during link training)         | VC credits      | Both          | Once per VC |
| UpdateFC               | Periodic / on-demand credit update                               | VC credits      | Both          | Unreliable  |
| PM_Enter_L1 / PM_ReqAck| Power management state transitions                                | —               | Both          | —           |
| Vendor-Specific        | Vendor-defined (rare)                                            | Variable        | Both          | —           |

📌 3. TLP Sequence Number & Replay Window

- **Sequence Number** (12 bits): 0–4095, rolls over
- Added by transmitter DLL before LCRC
- **Replay Window**: typically 2–4 KB (implementation dependent)
  - Contains unacknowledged TLPs (posted, non-posted, completions)
- **Ack** advances the lower boundary of the replay buffer
- **Nak** triggers replay from the Nak'd sequence number
- **Replay Timeout** (if no Ack/NAK): usually ~3× max round-trip time → link retraining or error reporting

📌 4. Flow Control – Credit Types & Rules

PCIe uses **credit-based flow control** – no back-pressure via stalls.

| Credit Type          | What it credits                          | Separate per VC? | Units                  |
|----------------------|------------------------------------------|------------------|------------------------|
| Posted Headers       | Memory Write / Message requests          | Yes              | Headers (1 credit = 1 header) |
| Posted Data          | Payload of posted requests               | Yes              | 4-byte DWs             |
| Non-Posted Headers   | Memory/I/O/Config Read/Write, I/O        | Yes              | Headers                |
| Non-Posted Data      | Payload of non-posted writes             | Yes              | DWs                    |
| Completion Headers   | All Completion TLPs                      | Yes              | Headers                |
| Completion Data      | Payload of Completion with Data          | Yes              | DWs                    |

⭐ **Key FC Rules**:
- Sender only transmits if enough credits available
- Credits are **cumulative** (advertised delta)
- **InitFC1/2** sent during link up – establishes baseline
- **UpdateFC** sent periodically or when credits consumed ≥ threshold (usually 1/2 buffer)
- Completions **never blocked** by FC (requester must pre-allocate space)

🔴 5. LCRC & Error Handling

- **LCRC** (32-bit Link CRC) — protects entire TLP (header + payload + sequence number)
- **ECRC** (optional End-to-End CRC) — protected by LCRC but not generated/checked by DLL
- **🔴 🔴 Bad LCRC** → receiver sends **NAK**, requests replay
- **🔴 🔴 Bad Sequence Number** → NAK + replay
- **Replay Buffer Overflow / Timeout** → usually AER (Advanced Error Reporting) logged, link may go to Recovery or retrain

📨 6. ACK/NAK Protocol – Simplified State Machine

| Event / Condition                  | Transmitter Action                          | Receiver Action                     |
|------------------------------------|---------------------------------------------|-------------------------------------|
| TLP transmitted                    | Add to replay buffer, start timer           | —                                   |
| 🟢 🟢 Good TLP received                  | Send Ack DLLP (cumulative up to N-1)        | —                                   |
| 🔴 🔴 Bad LCRC / sequence / framing      | —                                           | Send Nak DLLP + discard TLP         |
| Ack received                       | Free replay buffer up to Ack’d sequence     | —                                   |
| Nak received                       | Replay from Nak sequence number             | —                                   |
| No Ack for timeout                 | Replay entire window                        | —                                   |
| Periodic UpdateFC received         | Update available credits                    | —                                   |

⭐ 🐛 7. Important Behavioral Notes for Drivers / Debug

- **Posted writes** — fire-and-forget at Transaction Layer → no success confirmation (use MSI/MSI-X)
- **Non-posted reads** — can take very long if link is congested or replaying
- **MSI/MSI-X** messages are **posted** → no ordering guarantee relative to memory writes
- **Relaxed Ordering (RO bit)** — mostly affects memory ordering, not DLL
- **ECN (Error Containment & Notification)** — modern PCIe uses AER + DPC (Downstream Port Containment)
- **Link retraining** (LTSSM → Recovery) — triggered by too many errors, FC timeout, etc.
⭐ - **Replay buffer size** — larger = better tolerance to long round-trip times (important for extended reach / switches)

🐛 8. Quick Debug Commands / Locations (Linux 6.x)

.. code-block:: bash

================================================================================
AER stats (if enabled)
================================================================================

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:



dmesg | grep -i aer
cat /sys/bus/pci/devices/.../aer_stats  # if driver exposes

================================================================================
Link status / width / speed
================================================================================

lspci -vvv -s 01:00.0 | grep LnkSta

================================================================================
🔴 PCIe error counters (some drivers)
================================================================================

cat /sys/kernel/debug/pci/.../stats

================================================================================
🐛 ⭐ 🐛 Trace TLPs / DLLPs (hardware analyzer needed – LeCroy, Teledyne, Keysight)
================================================================================

**🟢 🟢 Best deep references**:
- PCIe Base Specification (PCI-SIG) – Chapter 3 (Data Link Layer)
- MindShare PCIe books (very practical)
- Linux kernel: ``drivers/pci/pcie/aer.c``, ``Documentation/PCI/pcieaer-howto.rst``

Use this cheatsheet when debugging link-level issues, replay storms, flow control starvation, or writing low-level PCIe verification code.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
