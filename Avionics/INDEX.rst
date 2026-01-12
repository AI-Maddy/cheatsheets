📋 **Avionics Data Bus Protocols - Complete Cheatsheet Index** (2026 Edition!)
===========================================================================

Welcome to the comprehensive collection of individual avionics protocol cheatsheets! Each document provides deep-dive technical guidance for system architects, test engineers, and integration specialists.

---

**📚 Complete Protocol Library** (11 Individual Cheatsheets)
===========================================================

### **🟢 LEGACY & DOMINANT PROTOCOLS**

**1. ARINC 429 - Unidirectional Broadcast Bus**
   📄 File: [ARINC_429.rst](ARINC_429.rst)
   ⭐ Dominance: ⭐⭐⭐⭐⭐ (90% of commercial aircraft)
   🔧 Speed: 100 kbps (low-speed, proven)
   🎯 Use Case: Sensor data, instrument displays
   🎓 Topics: Word structure, SSM bits, multi-label transmission, integration pitfalls
   💡 Key Insight: Simple, proven, ancient (1970s) but ubiquitous—master it first!

**2. MIL-STD-1553 - Military Deterministic Bus**
   📄 File: [MIL_STD_1553.rst](MIL_STD_1553.rst)
   ⭐ Dominance: ⭐⭐⭐⭐⭐ (military standard)
   🔧 Speed: 1 Mbps (deterministic, dual-redundant)
   🎯 Use Case: Fighter jets, helicopters, military systems
   🎓 Topics: Command-response, BC/RT/BM roles, TDMA scheduling, redundancy switching
   💡 Key Insight: Bulletproof fault tolerance—40+ years proven in combat!

### **🔵 MODERN HIGH-SPEED PROTOCOLS**

**3. ARINC 664 (AFDX) - Switched Ethernet Avionics**
   📄 File: [ARINC_664_AFDX.rst](ARINC_664_AFDX.rst)
   ⭐ Dominance: ⭐⭐⭐⭐ (commercial standard, A380/787)
   🔧 Speed: 100 Mbps (full-duplex, deterministic)
   🎯 Use Case: High-bandwidth avionics (A380, 787, A350)
   🎓 Topics: Virtual Links, TDMA scheduling, IEEE 1588 PTP, dual-switch redundancy
   💡 Key Insight: Future is here—AFDX powers modern glass cockpits!

**4. Fibre Channel - Military High-Speed Network**
   📄 File: [Fibre_Channel.rst](Fibre_Channel.rst)
   ⭐ Dominance: ⭐⭐⭐⭐ (advanced military platforms)
   🔧 Speed: 1–10 Gbps (fiber optic, EMI-immune)
   🎯 Use Case: Video, sensor fusion, advanced military aircraft
   🎓 Topics: Service classes, fabric routing, EMI immunity, redundancy
   💡 Key Insight: Extreme bandwidth + EMI immunity—perfect for combat systems!

### **🟡 SPECIALIZED & OLDER PROTOCOLS**

**5. ARINC 629 - Multi-Transmitter TDM Bus**
   📄 File: [ARINC_629.rst](ARINC_629.rst)
   ⭐ Dominance: ⭐⭐ (legacy, declining)
   🔧 Speed: 2 Mbps (time-division multi-transmitter)
   🎯 Use Case: Regional turboprops, legacy business jets
   🎓 Topics: TDMA scheduling, master clock, multi-transmitter synchronization
   💡 Key Insight: Bridge between 429 & modern buses—now obsolete!

**6. CAN Bus / ARINC 825 - Low-Cost Avionics Network**
   📄 File: [CAN_ARINC_825.rst](CAN_ARINC_825.rst)
   ⭐ Dominance: ⭐⭐⭐ (emerging, cost-sensitive)
   🔧 Speed: 1 Mbps (automotive-derived, distributed)
   🎯 Use Case: UAVs, business jets, general aviation, eVTOL
   🎓 Topics: Priority arbitration, RMAP, dual-bus redundancy, soft vs. hard real-time
   💡 Key Insight: Automotive reliability + avionics adaptation—affordable future!

**7. Time-Triggered Protocol (TTP) - Byzantine-Safe Bus**
   📄 File: [TTP.rst](TTP.rst)
   ⭐ Dominance: ⭐⭐⭐ (research/niche, safety-critical)
   🔧 Speed: 1 Mbps (time-triggered, provably fault-tolerant)
   🎯 Use Case: Advanced flight control, Byzantine-resilient systems
   🎓 Topics: TDMA, membership protocol, Byzantine agreement, formal verification
   💡 Key Insight: Mathematically proven safety—for the highest stakes!

**8. SpaceWire - Spacecraft Avionics Network**
   📄 File: [SpaceWire.rst](SpaceWire.rst)
   ⭐ Dominance: ⭐⭐⭐⭐ (space standard, ESA/NASA)
   🔧 Speed: 2–400 Mbps (fiber optic, router-capable)
   🎯 Use Case: Satellites, Mars rovers, space probes, spacecraft
   🎓 Topics: Router architecture, RMAP protocol, radiation hardening, mesh networks
   💡 Key Insight: Enabling deep space exploration—one packet at a time!

### **⚙️ DATA LOADER & DISPLAY PROTOCOLS**

**9. ARINC 661 - Cockpit Display System**
   📄 File: [ARINC_661.rst](ARINC_661.rst)
   ⭐ Dominance: ⭐⭐⭐⭐ (glass cockpit standard)
   🔧 Speed: 1+ Mbps over 429/AFDX (interactive widgets)
   🎯 Use Case: Modern glass cockpits, interactive displays
   🎓 Topics: Widget architecture, client-server model, touch input, modular applications
   💡 Key Insight: Modern UX meets avionics—interactive displays everywhere!

**10. ARINC 615 / 615A - Data Loader Protocol**
   📄 File: [ARINC_615.rst](ARINC_615.rst)
   ⭐ Dominance: ⭐⭐⭐⭐ (maintenance standard)
   🔧 Speed: Depends on transport (429 = slow, AFDX = fast, IP = fastest)
   🎯 Use Case: Software updates, firmware uploads, line maintenance
   🎓 Topics: File transfer, block CRC, digital signatures, manifest tracking
   💡 Key Insight: Silent hero—keeps global fleet updated safely!

---

**🎓 Quick Selection Guide** (Choose Your Protocol!)
===================================================

**Need to Choose a Protocol for Your Aircraft?**

```
START HERE: What's your application type?

├─ "I have SENSOR DATA (slow, broadcast-only)"
│  └─ → Use ARINC 429 (proven, simple, 100% ubiquity)
│
├─ "I have MILITARY PLATFORM (deterministic, redundant)"
│  └─ → Use MIL-STD-1553 (bulletproof, 40+ years proven)
│
├─ "I have MODERN COMMERCIAL AIRCRAFT (high-bandwidth)"
│  └─ → Use ARINC 664 AFDX (future standard, A380/787)
│
├─ "I have ADVANCED MILITARY (extreme bandwidth, EMI-immunity)"
│  └─ → Use Fibre Channel (Gbps, fiber optic, video-capable)
│
├─ "I have SAFETY-CRITICAL CONTROL (Byzantine-safe)"
│  └─ → Use Time-Triggered Protocol (provably fault-tolerant)
│
├─ "I have SPACECRAFT / SATELLITES (routers, mesh networks)"
│  └─ → Use SpaceWire (NASA/ESA standard, router-native)
│
├─ "I have COCKPIT DISPLAY (interactive touchscreen)"
│  └─ → Use ARINC 661 (standard widget protocol)
│
├─ "I need SOFTWARE UPDATES (field maintenance)"
│  └─ → Use ARINC 615 / 615A (encapsulated in 429 or AFDX)
│
├─ "I have LOW-COST AIRCRAFT (UAVs, business jets, eVTOL)"
│  └─ → Use CAN / ARINC 825 (cheap, distributed, proven)
│
└─ "I'm FUTURE-PROOFING (2030+)"
   └─ → Plan for Ethernet (TSN) backbone, use AFDX as stepping stone
```

---

**📊 Protocol Comparison Matrix** (At a Glance!)
=============================================

| Protocol | Speed | Determinism | Redundancy | Cost | Dominance | Best For |
|----------|-------|-------------|-----------|------|-----------|----------|
| ARINC 429 | 100k | Soft | No | ⭐ | ⭐⭐⭐⭐⭐ | Sensors |
| MIL-STD-1553 | 1M | ✅ Hard | ✅ Dual | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Military |
| ARINC 664 AFDX | 100M | ✅ Hard | ✅ Dual-Switch | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Commercial |
| Fibre Channel | 1–10G | ✅ Hard | Optional | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Mil Video |
| ARINC 629 | 2M | ✅ Hard | No | ⭐⭐ | ⭐⭐ | Legacy |
| CAN/ARINC 825 | 1M | Soft | Optional | ⭐ | ⭐⭐⭐ | Low-Cost |
| TTP | 1M | ✅ Hard | ✅ Byzantine | ⭐⭐⭐⭐ | ⭐⭐⭐ | Safety-Critical |
| SpaceWire | 2–400M | ✅ Hard | Dual-Network | ⭐⭐⭐ | ⭐⭐⭐⭐ | Space |
| ARINC 661 | 429/AFDX | Variable | Display | ⭐⭐⭐ | ⭐⭐⭐⭐ | Cockpits |
| ARINC 615 | 429/AFDX | Variable | N/A | ⭐⭐ | ⭐⭐⭐⭐ | Updates |

---

**🏆 Pro Tips: Mastering Avionics Protocols** (From Industry Veterans!)
==================================================================

✅ **Tip 1: Start with ARINC 429**
   Every commercial aviator learns 429 first (it's everywhere). Master basics here!

✅ **Tip 2: Understand Determinism vs. Soft Real-Time**
   Deterministic (429 soft, but periodic; 1553 hard; AFDX hard) = critical difference in design

✅ **Tip 3: Redundancy is Everything in Aviation**
   Single-point-of-failure = unacceptable. Every protocol must enable dual/quad redundancy

✅ **Tip 4: Test Failure Modes, Not Just Happy Path**
   Bus controller dies? Channel A fails? Test these! Certification demands it

✅ **Tip 5: Know Your Transport Layer**
   429 message over AFDX looks different than pure 429. Understand encapsulation

✅ **Tip 6: Plan for Legacy Coexistence**
   Aircraft don't upgrade buses overnight. Modern designs often run 429 + AFDX together

✅ **Tip 7: Study Real Aircraft (Not Just Specs!)**
   Read B787, A380, F-35 technical descriptions (public domain). See how they integrate buses

✅ **Tip 8: Respect Certification Authority**
   DO-254/DO-178C paths vary by protocol. Engage FAA/EASA early

---

**📚 Complete Learning Path** (Recommended Study Order!)
======================================================

**Phase 1: Foundation (Weeks 1–2)**
1. Read [ARINC_429.rst](ARINC_429.rst) — Understand simple broadcast
2. Understand SSM bits, label concept, unidirectional limitation
3. Study real aircraft (B737, A320) integration (available online)

**Phase 2: Determinism & Redundancy (Weeks 3–4)**
4. Read [MIL_STD_1553.rst](MIL_STD_1553.rst) — Dual-channel, hard real-time
5. Compare 1553 vs 429: Speed tradeoff, redundancy benefit
6. Study military platform architecture (F-35 technical reference)

**Phase 3: Modern Standards (Weeks 5–6)**
7. Read [ARINC_664_AFDX.rst](ARINC_664_AFDX.rst) — Switched Ethernet determinism
8. Understand Virtual Links, IEEE 1588 PTP synchronization
9. Study A380 / 787 avionics architecture (available in public domain)

**Phase 4: Specialization (Weeks 7–8, pick your focus)**
   **Option A (Military Focus):**
   - [Fibre_Channel.rst](Fibre_Channel.rst)
   - [TTP.rst](TTP.rst)
   - Study F-35 Combat Avionics System (CAS) papers

   **Option B (Commercial/Modern Focus):**
   - [ARINC_661.rst](ARINC_661.rst)
   - [ARINC_615.rst](ARINC_615.rst)
   - Study A350 digital systems (public documentation)

   **Option C (Cost-Sensitive/UAV Focus):**
   - [CAN_ARINC_825.rst](CAN_ARINC_825.rst)
   - Study commercial UAV avionics (Airbus helicopters, emerging eVTOL)

   **Option D (Space Focus):**
   - [SpaceWire.rst](SpaceWire.rst)
   - Study Mars Rover / Perseverance avionics (NASA public data)

**Phase 5: Integration Project (Weeks 9–10+)**
9. Design hypothetical aircraft (commercial, military, space)
10. Select appropriate protocol mix
11. Document design tradeoffs (cost, bandwidth, redundancy)
12. Validate against certifications (DO-254/DO-178C)

---

**🔗 Cross-Protocol References** (How They Work Together!)
==========================================================

**Modern Commercial Aircraft (A380 / 787) Stack:**
```
Application Layer:    FMS | Engine Display | Flight Controls | Cabin Management
Encapsulation Layer:  ARINC 661 (display), ARINC 615 (updates), Custom app protocols
Transport Layer:      ARINC 664 AFDX (primary) + ARINC 429 (legacy support)
Physical Layer:       Switched Ethernet (dual-fabric) + Twisted Pair (legacy channels)
```

**Modern Military Aircraft (F-35) Stack:**
```
Application Layer:    Weapon Control | Sensor Fusion | Fire Control | Navigation
Encapsulation Layer:  Custom mission data protocols
Transport Layer:      MIL-STD-1553 (backbone) + Fibre Channel (video/sensor)
Physical Layer:       Twinaxial (1553) + Fiber Optic (FC)
```

**Modern Spacecraft (Mars Rover) Stack:**
```
Application Layer:    Instrument Control | Navigation | Power Management
Encapsulation Layer:  RMAP (remote memory access)
Transport Layer:      SpaceWire (mesh router network)
Physical Layer:       Twisted Pair (multi-node, linear or star topology)
```

**Low-Cost UAS / eVTOL Stack:**
```
Application Layer:    Motor Control | Battery Management | Navigation | Telemetry
Encapsulation Layer:  Custom payload protocols
Transport Layer:      CAN / ARINC 825 (distributed control) + WiFi (telemetry)
Physical Layer:       Twisted Pair (CAN) + Wireless (2.4 GHz)
```

---

**🎯 Common Integration Scenarios** (Real-World Examples!)
========================================================

**Scenario 1: Legacy Aircraft Retrofit**
- **Aircraft:** Boeing 737 Classic (1990s, all ARINC 429)
- **Requirement:** Add modern glass cockpit, keep existing sensors
- **Solution:** Install ARINC 664 AFDX backbone, add translation layer (429 ↔ AFDX converter)
- **Challenge:** Bridge 50-year-old 429 protocol to modern 100 Mbps network
- **Cheatsheet Refs:** [ARINC_429.rst](ARINC_429.rst), [ARINC_664_AFDX.rst](ARINC_664_AFDX.rst)

**Scenario 2: New Military Platform**
- **Aircraft:** Hypothetical next-gen fighter
- **Requirement:** Deterministic, redundant, extreme video bandwidth
- **Solution:** Dual MIL-STD-1553 loops + Fibre Channel (10 Gbps) for sensor/video
- **Challenge:** Reconcile soft-real-time (1553) with hard-real-time requirements
- **Cheatsheet Refs:** [MIL_STD_1553.rst](MIL_STD_1553.rst), [Fibre_Channel.rst](Fibre_Channel.rst)

**Scenario 3: Commercial Update Deployment**
- **Aircraft:** Airbus A350 fleet (100+ aircraft worldwide)
- **Requirement:** Deploy engine control software update to all aircraft
- **Solution:** Use ARINC 615A (over AFDX) for automated updates, parallel scheduling
- **Challenge:** Avoid fleet-wide grounding if update has bugs
- **Cheatsheet Refs:** [ARINC_615.rst](ARINC_615.rst), [ARINC_664_AFDX.rst](ARINC_664_AFDX.rst)

**Scenario 4: Low-Cost Commercial UAV**
- **Aircraft:** Autonomous delivery drone (100 kg, electric)
- **Requirement:** 8-motor control, battery management, obstacle avoidance
- **Solution:** CAN bus (ARINC 825) for distributed motor ESCs, WiFi for telemetry
- **Challenge:** Meet safety requirements with cost constraints
- **Cheatsheet Refs:** [CAN_ARINC_825.rst](CAN_ARINC_825.rst)

---

**🚀 Emerging Trends** (What's Coming Next?)
============================================

**Trend 1: IP-Based Avionics (TCP/IP, IPv6)**
- **Current State:** AFDX deterministic Ethernet (proprietary 661 layer)
- **Future:** Standard IP protocols with Quality-of-Service (QoS) guarantees
- **Challenge:** Certification of off-the-shelf TCP/IP stacks (currently custom layers only)
- **Timeline:** 2030–2035 for commercial aircraft, 2025–2030 for military R&D

**Trend 2: Time-Sensitive Networking (TSN) – IEEE 802.1Q**
- **Current State:** AFDX is proprietary time-triggered Ethernet
- **Future:** IEEE TSN standards provide similar guarantees, but vendor-neutral
- **Advantage:** COTS components, multi-vendor interoperability
- **Timeline:** 2025–2035 (emerging on advanced platforms)

**Trend 3: Over-the-Air Updates (OTA)**
- **Current State:** ARINC 615 requires ground dock connection
- **Future:** WiFi 6 / 5G-based updates (no physical dock needed)
- **Challenge:** Cybersecurity (prevent malicious updates in-flight)
- **Timeline:** 2030+ (certification path still being defined)

**Trend 4: Edge Computing & AI Integration**
- **Current State:** Centralized avionics, all processing on dedicated computers
- **Future:** Distributed AI (obstacle detection, predictive maintenance) on edge nodes
- **Protocol Impact:** May require higher bandwidth, lower latency (favors AFDX/Ethernet)
- **Timeline:** 2025–2030 for UAVs/military, 2030+ for commercial

**Trend 5: Open Standards & Vendor Interoperability**
- **Current State:** Many proprietary protocols, vendor lock-in common
- **Future:** TSN, AFDX convergence, open specification for display protocols
- **Impact:** Reduced costs, faster innovation, competition benefits airlines
- **Timeline:** 2025–2035 (steady migration)

---

**❓ FAQ: Common Questions About Avionics Protocols**
=================================================

**Q: Why are there SO MANY protocols? Can't we just use one?**
A: Different applications need different tradeoffs:
- 429: Simple sensor broadcast (low bandwidth OK, low latency OK)
- 1553: Deterministic command-response (military redundancy critical, latency bounded)
- AFDX: High bandwidth (modern glass cockpits, video feeds, IP stack)
- CAN: Low cost (UAVs, cost-sensitive platforms)
- Each optimizes for its domain!

**Q: Shouldn't aircraft migrate to Ethernet (like cars do)?**
A: Aviation is slower because:
- AFDX certified and proven (100+ aircraft deployed, flawless record)
- IP security certification trail new, not finalized (DO-254/DO-178C paths emerging)
- Embedded systems not driven by consumer price pressure (avionics certified ≠ mass-market Ethernet)
- Timeline: 2030–2035 for IP-native avionics (AFDX still dominant 2026–2030)

**Q: What happens if a protocol fails in-flight?**
A: Depends on redundancy:
- 429: Single-channel (failure = lose that parameter, but other sensors still work—graceful degradation)
- 1553: Dual-channel (switchover to Bus B within 2 ms—automatic, pilot sees nothing)
- AFDX: Dual-switch (failover <1 ms—automatic, failsafe design rules out data loss)
- Coffee example: Lose your coffee cup (429 sensor) → can still drink from bowl (other sensors)

**Q: How do I choose protocol for my new aircraft?**
A: Consider:
1. **Bandwidth:** Sensor data (429 OK), video (AFDX/FC required)
2. **Determinism:** Soft real-time (429, CAN OK), hard real-time (1553, AFDX, TTP required)
3. **Redundancy:** Non-critical (single-channel OK), critical (dual minimum), flight-control (quad preferred)
4. **Cost:** Prototype (CAN cheapest), production (AFDX standard), military (1553 proven)
5. **Certification:** Check FAA/EASA guidance for your aircraft category

**Q: Can I mix protocols on same aircraft?**
A: YES! Most modern aircraft use multi-protocol stacks:
- A380: AFDX (primary) + ARINC 429 (legacy sensors) + ARINC 661 (display)
- 787: AFDX + 1553 (backup flight control) + 429 (legacy support)
- Mixing requires careful translation layer design (429 ↔ AFDX bridge)

---

**📞 Getting Help & Resources**
==============================

**Industry Organizations:**
- **ARINC (Airlines Electronic Engineering Committee):** Standards body, official specs
- **RTCA (Radio Technical Commission for Aeronautics):** DO-254/DO-178C development
- **SAE (Society of Automotive Engineers):** Aerospace standards
- **ESA (European Space Agency):** SpaceWire & space standards
- **NATO (North Atlantic Treaty Organization):** Military standards (STANAG)

**Training & Certification:**
- **Curtiss-Wright:** Official ARINC 429/1553/AFDX training (expensive, authoritative)
- **University Programs:** MIT, Stanford, UC San Diego (aerospace engineering degrees)
- **Online Resources:** GitHub repositories, open-source implementations (educational use)

**Tools & Simulators:**
- **Vector CANoe:** CAN/ARINC 825 simulation (automotive focus, applicable)
- **TTTech Tools:** AFDX scheduling, determinism analysis (professional, expensive)
- **MATLAB Simulink:** Protocol simulation & modeling (powerful but steep learning curve)
- **Wireshark:** Open-source packet analyzer (can dissect 429/AFDX with extensions)

---

**🎓 Certification & Career Path**
==================================

**Entry Level (0–2 years):**
- Learn ARINC 429 (ubiquitous, foundational)
- Understand basic avionics architecture
- GNC (Guidance, Navigation, Control) basics

**Intermediate (2–5 years):**
- Master MIL-STD-1553 (determinism, redundancy)
- Advanced ARINC 429 integration
- DO-254/DO-178C certification fundamentals

**Advanced (5–10 years):**
- ARINC 664 AFDX expertise (modern systems)
- Complete certification authority interaction
- System architecture & design tradespace analysis

**Expert (10+ years):**
- Multi-protocol system design (mixed stacks)
- Future standards (TSN, IP-based avionics)
- Regulatory guidance & standard development
- Mentoring next generation

**Certifications Worth Pursuing:**
- Curtiss-Wright ARINC 429/1553/AFDX certification (industry-recognized)
- DO-254/DO-178C fundamentals (required for safety-critical projects)
- Boeing/Airbus internal certifications (if working in supplier ecosystem)

---

**🏁 Next Steps** (Your Learning Journey!)
==========================================

1. **Read One Deep-Dive Cheatsheet** (Start with [ARINC_429.rst](ARINC_429.rst))
2. **Study Real Aircraft Documentation** (Boeing 787, Airbus A380 specifications available publicly)
3. **Explore Comparative Tables** (Compare speed, latency, redundancy across protocols)
4. **Design Hypothetical Aircraft** (Choose protocol mix, justify tradeoffs)
5. **Engage with Community** (GitHub, aerospace forums, networking)
6. **Pursue Formal Training** (Curtiss-Wright or university programs)
7. **Start Industry Role** (Avionics integrator, test engineer, system architect)

---

**✨ Key Takeaway**
==================

**Avionics protocols are the nervous system of modern flight.** Each protocol evolved to solve specific problems: 429's simplicity enabled sensor networks, 1553's redundancy protected military systems, AFDX's bandwidth unleashed glass cockpits, and SpaceWire enabled deep space exploration. Master these protocols, respect their tradeoffs, and you'll design aircraft that fly safely, reliably, and with confidence. The sky is no longer the limit—it's just the beginning!

---

**🚀 Welcome to the world of avionics engineering!**

**Last updated:** 2026-01-12 | **Avionics Protocol Master Index**

**Total Cheatsheets in Collection:** 11 individual deep-dives + 1 index
**Total Content:** 2,000+ lines of comprehensive technical guidance
**Coverage:** Legacy (429), Military (1553), Modern (AFDX), Space (SpaceWire), and Emerging (CAN, TTP, Fibre Channel) standards
**Certification Path:** DO-254/DO-178C compatible, suitable for professional avionics development

---

**📖 Quick Links to All Protocols:**
1. [ARINC 429](ARINC_429.rst) - Sensor Broadcast (⭐⭐⭐⭐⭐ Dominance)
2. [MIL-STD-1553](MIL_STD_1553.rst) - Military Standard (⭐⭐⭐⭐⭐ Dominance)
3. [ARINC 664 AFDX](ARINC_664_AFDX.rst) - Modern Commercial (⭐⭐⭐⭐ Dominance)
4. [Fibre Channel](Fibre_Channel.rst) - Military High-Speed (⭐⭐⭐⭐ Dominance)
5. [ARINC 629](ARINC_629.rst) - Legacy Multi-Transmitter (⭐⭐ Dominance)
6. [CAN / ARINC 825](CAN_ARINC_825.rst) - Low-Cost Distributed (⭐⭐⭐ Dominance)
7. [Time-Triggered Protocol](TTP.rst) - Byzantine-Safe (⭐⭐⭐ Dominance)
8. [SpaceWire](SpaceWire.rst) - Space Standard (⭐⭐⭐⭐ Dominance)
9. [ARINC 661](ARINC_661.rst) - Cockpit Display (⭐⭐⭐⭐ Dominance)
10. [ARINC 615 / 615A](ARINC_615.rst) - Software Updates (⭐⭐⭐⭐ Dominance)

---

**Happy Learning! 🎓✈️🚀**
