
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for ADAS (Advanced Driver Assistance Systems) in combination with AUTOSAR** (both Classic and Adaptive platforms) – reflecting the state of the industry in early 2026.

🚗 1. ADAS + AUTOSAR – High-Level Landscape (2026)

⭐ | ADAS Function / Level       | Typical AUTOSAR Platform (2026) | Main Communication Bus       | Typical Compute Platform          | Safety Target (ASIL) | Key Challenges in AUTOSAR Context |
|-----------------------------|----------------------------------|------------------------------|-----------------------------------|----------------------|-----------------------------------|
| Adaptive Cruise Control (ACC) | Classic (most)                  | CAN-FD / Ethernet            | Zonal ECU or Domain controller    | B–C                  | Deterministic timing, latency     |
| Lane Keep Assist / LKA      | Classic                         | CAN-FD                       | Zonal / Domain ECU                | B–C                  | Sensor fusion latency             |
| Emergency Braking (AEB)     | Classic                         | CAN-FD                       | Zonal ECU                         | C–D                  | Fault containment, freedom from interference |
⭐ | Traffic Jam Assist / L2+    | Classic + Adaptive hybrid       | Ethernet + CAN-FD            | Domain + HPC                      | C–D                  | Mixed-criticality, OTA            |
| Highway Pilot / L3          | Adaptive dominant               | Automotive Ethernet          | Central HPC ECU                   | D                    | Dynamic resource allocation, service discovery |
| Urban Automated Driving / L4| Adaptive                        | Ethernet + TSN               | Central compute + zonal gateways  | D                    | High-bandwidth fusion, safety monitoring |
| Sensor Fusion (camera+radar+lidar) | Adaptive (central)       | Ethernet                     | HPC (NVIDIA Orin, Qualcomm SA8xxx, TI Jacinto) | D                    | Zero-copy DMA-BUF, low-latency    |

🚗 2. AUTOSAR Platform Choice for ADAS (2026 Reality)

| ADAS Level / Function       | AUTOSAR Classic | AUTOSAR Adaptive | Hybrid (Classic + Adaptive) | Why this combination dominates in 2026 |
|-----------------------------|-----------------|------------------|------------------------------|----------------------------------------|
| Pure L1–L2 functions        | Yes             | Rarely           | Sometimes                    | Classic is mature, deterministic, cheaper |
| L2+ with OTA & rich HMI     | Limited         | Yes              | Very common                  | Adaptive for OTA, infotainment integration |
| L3 Highway / Automated Valet| No              | Yes              | Common (Classic low-level)   | Adaptive for dynamic compute & Ethernet |
| L4 Urban / Robotaxi         | No              | Yes              | Very common                  | Central HPC needs Adaptive + service-oriented |
| Sensor data acquisition     | Yes (zonal)     | Yes (central)    | Dominant                     | Classic on camera/radar ECUs, Adaptive on fusion ECU |

📡 3. Typical ADAS Software Architecture with AUTOSAR (2026)

Vehicle Level
  ↓
Central/High-Performance Compute (HPC) ECU
  ├─ AUTOSAR Adaptive
  │   ├─ ara::com (SOME/IP) → service discovery, RPC, events
  │   ├─ ara::exec → dynamic threads & executors
  │   ├─ ara::phm → platform health monitoring
  │   ├─ ara::ucm → OTA & software package management
  │   └─ Perception stack (sensor fusion, object detection, path planning)
  │
  └─ Middleware / ROS2 bridge (optional for prototyping)
      ↓
Zonal ECUs / Domain Controllers
  ├─ AUTOSAR Classic (low-level control)
  │   ├─ CAN-FD / Ethernet gateway
  │   ├─ Sensor drivers (camera, radar, ultrasonic)
  │   └─ Actuator control (brake, steering)
  │
  └─ Raw sensor data → Ethernet → HPC (DMA-BUF, zero-copy)

⭐ 🚗 4. Key AUTOSAR Modules Used in ADAS

| AUTOSAR Module              | Platform     | ADAS Relevance / Typical Use Case                          |
|-----------------------------|--------------|------------------------------------------------------------|
| ara::com                    | Adaptive     | Camera object list, radar tracks, fusion service           |
| ara::exec                   | Adaptive     | Dynamic scheduling of perception threads                   |
| ara::phm                    | Adaptive     | Supervision of DNN inference, watchdog                     |
| ara::ucm                    | Adaptive     | OTA of perception models & maps                            |
| ara::diag                   | Both         | UDS diagnostics over Ethernet (DoIP)                       |
| ara::persistency            | Adaptive     | Store calibration data, maps, learned models               |
| DCM / DEM                   | Classic      | Diagnostic stack on zonal ECUs                             |
| COM / PDU Router            | Classic      | Signal-based low-level control (steering torque, braking)  |

🛡️ 5. Safety & Timing in ADAS + AUTOSAR

| Requirement                 | Classic AUTOSAR Solution                     | Adaptive AUTOSAR Solution                          | Typical ASIL Target |
|-----------------------------|----------------------------------------------|----------------------------------------------------|---------------------|
| Deterministic execution     | Static schedule table                        | End-to-end deadlines + executor scheduling         | ASIL B–D            |
⭐ | Freedom from interference   | Static ASIL decomposition                    | Mixed-criticality + partitioning (hypervisor)      | ASIL D              |
| Fault containment           | Watchdog, E2E protection                     | PHM + error handling + recovery                    | ASIL C–D            |
| Low-latency sensor data     | Direct CAN-FD                                | Ethernet + TSN + zero-copy DMA-BUF                 | <10 ms end-to-end   |
| Functional safety certification | Established (many ASIL-D certified stacks) | Growing (QNX, EB corbos, Vector certified stacks)  | ASIL B–D            |

📌 6. Current Industry Practice (Jan 2026)

- **L2 / L2+ systems** (most vehicles sold 2024–2026)  
  → Mostly **AUTOSAR Classic** on domain/zonal ECUs + **some Adaptive** for infotainment/ADAS fusion

- **L3 Highway Pilot** (Mercedes Drive Pilot, BMW Personal Pilot, etc.)  
  → **Hybrid**: Classic for actuators/sensors + **Adaptive** for central perception/planning

- **L4 robotaxi / urban AD** (Waymo, Cruise, Baidu Apollo, etc.)  
  → **Adaptive AUTOSAR** on HPC + custom middleware (ROS2/DDS bridge) or pure Linux stack

- **Zonal E/E architecture** (VW, Tesla, BMW Neue Klasse, Stellantis STLA)  
⭐   → **Zonal Classic** (low-cost, safety-critical) + **Central Adaptive** (high-performance compute)

- **Ethernet backbone** → 1000BASE-T1 / 2.5/10GBASE-T1 + TSN → standard for sensor-to-HPC communication

📌 Quick Summary Mnemonics (2026)

- **Classic AUTOSAR** → **small, static, CAN-FD, deterministic, ASIL-D legacy**
- **Adaptive AUTOSAR** → **large, dynamic, Ethernet, service-oriented, OTA, HPC future**
- **ADAS L1–L2** → mostly Classic today
- **ADAS L2+ / L3** → hybrid Classic + Adaptive
- **L4+ / SDV** → Adaptive dominant + custom perception stack

This cheatsheet reflects the real split seen in production vehicles and Tier-1 roadmaps in early 2026.

Let me know if you want deeper details on any part (e.g. ara::com in ADAS, PHM for perception, or zonal vs domain architecture).

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
