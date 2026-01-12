🟨 **ARINC 629 - Shared Data Bus** (2026 Edition!)
=====================================================

**Quick ID:** 629 | **Dominance:** ⭐⭐ Legacy | **Speed:** 2 Mbps

---

**📌 One-Line Summary**
Multi-transmitter, time-division, 2 Mbps shared bus—predecessor to AFDX, now legacy but still found on regional aircraft.

---

**📋 Essential Specifications**
=====================================

**Data Format:**
  • Multi-transmitter, time-division multiplexed (TDM) bus
  • 32-bit words (similar structure to ARINC 429)
  • Label-based message format (256 possible labels per transmitter)
  • Synchronous transmission timing (all devices synchronized to common clock)

**Performance Characteristics:**
  • **Bandwidth:** 2 Mbps (20× faster than ARINC 429, but slower than 1553)
  • **Transmitters:** Up to 3 simultaneous transmitters (time-slotted access)
  • **Word Rate:** ~6,250 words per second
  • **Latency:** ~2 ms per word
  • **Range:** 100 meters typical
  • **Topology:** Daisy-chain or star (less strict than 1553)

**Physical Layer:**
  • **Connector:** Twin coaxial cables (similar to 1553, but only single pair)
  • **Wiring:** Single shielded twisted pair (not dual-redundant)
  • **Voltage:** ±5V differential (similar Manchester encoding to 429)
  • **Impedance:** 78 Ω nominal

**Protocol Features:**
  • **Multiple Transmitters:** Up to 3 devices can transmit (TDM schedule)
  • **Label Format:** 8-bit label per transmitter (256 possible per device)
  • **Word Structure:** Similar to 429 (label, data, SSM/status bits)
  • **Synchronization:** All devices locked to common clock (external timing source)
  • **Deterministic Scheduling:** Pre-assigned time slots per transmitter

---

**🏛️ Historical Context & Evolution**
======================================

**Origin:** 1985–1990 (ARINC, developed as interim solution between 429 & higher-speed buses)
**Development Drivers:** Need for faster than 429, but simpler than dual-channel 1553
**Timeline:**
  • **1985–1990:** Development & standardization
  • **1990s–2000s:** Adoption in regional turboprops (ATR-42/72, Dash 8, Saab 340)
  • **2000s–2010s:** Continued use in new designs, but overshadowed by AFDX
  • **2010s–present:** Declining (being replaced by AFDX in new programs, legacy aircraft only)

**Why 629 Was Developed:**
  ✅ Faster than ARINC 429 (2 Mbps vs. 100 kbps)
  ✅ Simpler than MIL-STD-1553 (no command-response complexity, no BC/RT roles)
  ✅ Multi-transmitter capability (enables sensor-to-sensor data sharing)
  ✅ Cost-effective (single coaxial pair vs. twinax)
  ✅ Lower latency than 429 (suitable for control loop feedback)

---

**⚙️ Technical Deep Dive**
=========================

**629 Bus Architecture:**

1. **Master Clock Source:**
   • External timing source (IRS, dedicated clock module)
   • Broadcast sync signal (1 kHz frame rate, 1 ms frame period)
   • All devices phase-locked to master

2. **Transmitter (Multiple Allowed):**
   • Assigned time slots within frame (e.g., TX1: 0.0–0.3 ms, TX2: 0.3–0.6 ms, TX3: 0.6–1.0 ms)
   • Transmits only during assigned slot (collision avoidance)
   • Can transmit multiple labels per slot (if time permits)
   • Responsible for timing accuracy (critical for slot boundaries)

3. **Receiver (All Other Devices):**
   • Passive listening (similar to 429 receiver)
   • Filters labels of interest
   • Timestamps data (reference to master frame)
   • No transmission capability (only TX devices transmit)

**Word Structure (32 bits, similar to 429):**
  ```
  [Label: 8] [Data: 19] [SSM: 2] [Parity: 1] [Control: 2]
  └──────────────────────────────────────────────────────┘
               32-Bit WORD (629 format)
  ```

**Frame Structure:**
  • **Frame Rate:** 1 kHz (1 ms frame period)
  • **TX1 Slot:** 0.0–0.3 ms (300 µs for TX1 data)
  • **TX2 Slot:** 0.3–0.6 ms (300 µs for TX2 data)
  • **TX3 Slot:** 0.6–0.9 ms (300 µs for TX3 data)
  • **Sync Pulse:** 0.9–1.0 ms (frame synchronization marker)
  • **Word Rate:** ~6 words per slot (6,250 words/sec total)

**Label Ranges (Example Assignment):**
  • **TX1 (Air Data Computer):** Labels 0–50 (altitude, airspeed, pressure)
  • **TX2 (Inertial System):** Labels 100–150 (heading, roll, pitch, accelerations)
  • **TX3 (Flight Control):** Labels 200–250 (control surface positions, trim)
  • **All RX:** Labels 0–250 available for any receiver

---

**🎯 Real-World Use Cases**
===========================

**Regional Turboprops (ATR 42/72, Dash 8, Saab 340):**
  ✅ Engine parameters (N1, N2, EGT, fuel flow)
  ✅ Navigation (heading, altitude, attitude)
  ✅ Flight control feedback (control surface positions)
  ✅ System status (hydraulic pressure, electrical bus)
  ✅ Some military variants (transport, patrol, surveillance)

**Legacy Business Jets:**
  ✅ Avionics data bus (integrated flight management system)
  ✅ Navigation & guidance
  ✅ Cockpit displays

**Some Military Transport Aircraft:**
  ✅ Cargo/system control
  ✅ Telemetry (limited deployment)

---

**🔌 Integration & Implementation**
===================================

**Transmitter Design:**
  • Waits for assigned time slot (monitored via master sync signal)
  • Transmits labels during slot (typically 3–6 words)
  • Returns to receive mode after slot ends
  • Watchdog timer detects loss of master clock (fail-safe mode)

**Receiver Design:**
  • Passive listening during all transmitter slots
  • Extracts label of interest
  • Updates internal data buffer (overwriting previous values)
  • Validates data (parity, SSM bits)

**Clock Distribution:**
  • Master clock derived from IRS (navigation system) or atomic clock module
  • Distributed to all devices via separate clock line (1 kHz square wave)
  • Critical for frame synchronization (slot timing accuracy)

**Cable Routing:**
  • Single shielded twisted pair (vs. twinax for 1553)
  • Linear daisy-chain topology (less forgiving than 1553 of stub lengths)
  • Ground at one end (or both, for military variants)

---

**📊 Comparison: ARINC 629 vs Other Buses**
==========================================

| Feature | 629 | 429 | 1553 | AFDX |
|---------|-----|-----|------|------|
| Speed | 2 Mbps | 100 kbps | 1 Mbps | 100 Mbps |
| Transmitters | 3 (multi) | 1 | 1 (BC) | Many |
| Direction | Shared | Unidirectional | Bidirectional | Full-Duplex |
| Determinism | ✅ Perfect | Soft | ✅ Perfect | ✅ Perfect |
| Latency | ~2 ms | ~10–20 ms | ~2 ms | <10 µs |
| Redundancy | No | No | Dual-channel | Dual-switch |
| Complexity | ⭐⭐ Low | ⭐ Very Low | ⭐⭐⭐ High | ⭐⭐⭐⭐ Very High |
| Dominance | ⭐⭐ Legacy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

**❌ Common Integration Pitfalls** (Avoid These!)
================================================

**Mistake 1: Multiple Transmitters Colliding**
  ❌ Problem: TX devices not synchronized, sending during overlapping slots
  ❌ Solution: Implement hardware watchdog; ensure master clock distribution to all devices

**Mistake 2: Ignoring Master Clock Loss**
  ❌ Problem: Master clock fails, frame synchronization lost, data corruption
  ❌ Solution: Implement watchdog timer (detect missing sync pulse); trigger fail-safe mode

**Mistake 3: Daisy-Chain Stub Length Violations**
  ❌ Problem: Impedance mismatches, signal reflections
  ❌ Solution: Keep stubs short; use star topology with hub if needed

**Mistake 4: Over-Allocating Labels to Slots**
  ❌ Problem: Too many labels crammed into slot, timing violations
  ❌ Solution: Plan label-to-slot mapping carefully (max ~6 words per 300 µs slot)

**Mistake 5: Not Validating SSM Bits (Similar to 429)**
  ❌ Problem: Using invalid/stale data (SSM = failure indicator)
  ❌ Solution: Check SSM on every receive; discard if not "normal" (00 status)

---

**🛠️ Tools & Development Resources**
====================================

**Protocol Analyzers:**
  • **Curtiss-Wright ICD-629:** Protocol analyzer (less common than 429/1553)
  • **Peak Systems:** Limited 629 support (focus on CAN, 1553)
  • **Astronics ACES:** Some 629 modules (declining support)

**Development Standards:**
  • **ARINC 629:** Official specification (less detailed than 429, now deprecated)
  • **DO-178C:** Avionics software development
  • **DO-254:** Avionics hardware design

**Legacy Support:**
  • **COTS Modules:** Rare (manufacturers phasing out)
  • **Custom FPGA:** Only option for new designs needing 629 (if any)

---

**💡 Pro Tips for Legacy Avionics Maintenance**
===============================================

✅ **Tip 1: Master Clock is Critical**
  Monitor master clock health obsessively; loss of sync = data corruption

✅ **Tip 2: Multi-Transmitter Scheduling Must Be Foolproof**
  Document slot assignments; test on bench before flight

✅ **Tip 3: Plan Eventual Replacement**
  629 support declining; newer avionics should migrate to AFDX

✅ **Tip 4: Keep Spare COTS Modules**
  Finding replacement components is increasingly difficult; stockpile during end-of-life windows

---

**📚 Further Reading**
======================

📖 **ARINC 629 Specification:** Official standard (less comprehensive than 429)
📖 **"Avionics Systems 2nd Edition" by A. J. Peacock:** 629 overview (limited)
📖 **Regional Aircraft Maintenance Manuals:** ATR-42/72, Dash 8 integration details

---

**🎯 Key Takeaway**
==================

✨ **ARINC 629 was a noble attempt to bridge the gap between 429 and higher-speed buses.** It successfully deployed on hundreds of regional aircraft and remains in service. However, AFDX has made it obsolete for new designs. If you encounter 629 in legacy systems, respect the multi-transmitter complexity and master clock criticality—they're less forgiving than 429, but simpler than 1553!

---

**Last updated:** 2026-01-12 | **ARINC 629 Historical Reference**
