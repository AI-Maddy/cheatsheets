
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet comparing AUTOSAR Classic vs AUTOSAR Adaptive** (as of early 2026 – Release R23-11 / R24-11 dominant), with emphasis on **high-level architectural differences**.

📌 1. High-Level Comparison Table

| Aspect                        | AUTOSAR Classic Platform                     | AUTOSAR Adaptive Platform (ARA)                  | Main Architectural Driver / Purpose                  |
|-------------------------------|----------------------------------------------|--------------------------------------------------|------------------------------------------------------|
| **Target Hardware**           | Microcontrollers (small–medium, 8/16/32-bit) | High-performance processors (multi-core ARM64, x86) | Classic = ECU, Adaptive = HPC / central compute      |
| **Execution Model**           | Static, fixed OSEK/VDX schedule              | Dynamic, POSIX threads + event-driven            | Static vs dynamic runtime                            |
| **Communication Paradigm**    | Signal-based (PDU, CAN-FD, FlexRay, LIN)     | Service-oriented (SOME/IP, DDS, Ethernet)        | Signal vs Service-Oriented Architecture (SOA)        |
| **Operating System**          | OSEK/VDX RTOS (static tasks, no threads)     | POSIX-compliant RTOS (Linux, QNX, etc.)          | RTOS vs rich POSIX OS                                |
| **Software Update / OTA**     | Difficult (monolithic image, rarely supported) | Designed for partial OTA & rolling updates       | Software-Defined Vehicle (SDV) requirement           |
⭐ | **Safety Integration**        | ASIL decomposition, static freedom from interference | Mixed-criticality, dynamic supervision (PHM)     | Static vs dynamic safety mechanisms                  |
| **Scalability**               | Limited (fixed resources)                    | High (dynamic resource allocation)               | Legacy ECU vs future zonal/central compute           |
| **Typical Release in Vehicles**| 2010–2025 (still dominant in 2026)           | 2022–2025 ramp-up (first series production ~2022) | Legacy vs emerging high-end                          |
| **Typical Use Cases (2026)**  | Powertrain, chassis, body, gateways          | ADAS, autonomous driving, infotainment, HPC ECU  | Domain vs zonal/central compute                      |

📌 2. Architectural Stack – Side-by-Side View

AUTOSAR Classic                               AUTOSAR Adaptive (ARA)
──────────────────────────────                 ──────────────────────────────
Application Layer                             Application Layer
  ↑   Software Components (SWC)                 ↑   Adaptive Applications (C++ ARA API)
  │                                             │
Runtime Environment (RTE)                       ara::exec, ara::com, ara::phm, ara::ucm, …
  ↑   Virtual Functional Bus (VFB)              ↑   Service-oriented middleware (SOME/IP, DDS)
  │                                             │
Basic Software (BSW)                            Platform Foundation
  ↑   OS (OSEK/VDX), COM, MEMIF, …              ↑   POSIX OS + ara::* modules
  │                                             │
Microcontroller Abstraction Layer (MCAL)        POSIX OS + drivers
  ↑   Drivers, ECU abstraction                  ↑   Linux/QNX kernel + drivers
  │                                             │
Hardware (MCU)                                  Hardware (multi-core SoC)

⭐ 📌 3. Key Architectural Differences – Table View

| Architectural Element          | Classic AUTOSAR                                      | Adaptive AUTOSAR                                      | Architectural Impact / Consequence                          |
|--------------------------------|------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------------|
| **Component Model**            | Runnable-based, static configuration                 | Service-based, dynamic instantiation                  | Fixed vs runtime-adaptive behavior                          |
| **Communication**              | Signal-oriented (PDUs mapped to frames)              | Service-oriented (method, event, field)               | Static routing vs dynamic discovery                         |
| **Scheduling**                 | Static schedule table (OSEK tasks, interrupts)       | Dynamic threads, event queues, executors              | Predictable vs flexible timing                              |
| **Resource Management**        | Static allocation (compile-time)                     | Dynamic (runtime allocation, POSIX)                   | Fixed memory vs elastic resources                           |
| **State & Mode Management**    | Mode-switch manager (static)                         | State Management module (ara::sm) + machine states    | Fixed modes vs runtime lifecycle control                    |
| **Diagnostics**                | UDS over CAN/LIN (DCM module)                        | UDS over SOME/IP (ara::diag)                          | Bus-specific vs Ethernet-based                              |
⭐ | **Persistence**                | NvM (non-volatile memory)                            | ara::persistency (key-value + file)                   | Basic key-value vs modern key-value store                   |
| **Health Monitoring**          | Watchdog, limited supervision                        | Platform Health Management (ara::phm)                 | Basic watchdog vs active heartbeat & error containment      |
| **Update Mechanism**           | Full re-flash (rarely supported)                     | Update & Configuration Management (ara::ucm)          | Monolithic vs partial & rolling OTA                         |
⭐ | **Safety Partitioning**        | Static ASIL decomposition                            | Dynamic + mixed-criticality (QM + ASIL)               | Compile-time vs runtime protection                          |

⚙️ 4. Communication Paradigm – Signal vs Service

| Feature                        | Classic (Signal-based)                               | Adaptive (Service-based)                              |
|--------------------------------|------------------------------------------------------|-------------------------------------------------------|
| **Paradigm**                   | Sender broadcasts signals → receiver consumes        | Client discovers & subscribes to services             |
| **Protocol**                   | CAN-FD, FlexRay, LIN, SOME/IP lite                   | SOME/IP (main), DDS (optional), Ethernet              |
| **Discovery**                  | Static configuration                                 | Dynamic (SOME/IP Service Discovery)                   |
| **QoS**                        | Static priority / deadline                           | Runtime QoS negotiation (deadline, reliability)       |
| **Scalability**                | Limited by bus bandwidth                             | High (Ethernet + service-oriented)                    |
| **Typical Payload**            | 8–64 bytes (CAN-FD)                                  | Variable (kilobytes possible)                         |

📌 5. Quick Mnemonics & Rules of Thumb (2026)

- **Classic** = **small, static, signal-driven, deterministic** → legacy ECUs, powertrain, body
- **Adaptive** = **large, dynamic, service-oriented, POSIX** → future HPC, ADAS, infotainment, zonal compute
- **If you need OTA + Ethernet + multi-core + C++** → Adaptive
- **If you need hard real-time + CAN-FD + ASIL-D static** → Classic
- **Most new vehicles 2025–2030** → **hybrid**: Classic for low-level, Adaptive for high-level compute
- **Zonal architecture** = **Adaptive on central HPC + Classic on zonal controllers**

This cheatsheet summarizes the **high-level architectural differences** between Classic and Adaptive AUTOSAR – the two platforms are fundamentally incompatible at runtime and design level.

🟢 🟢 Good luck with your AUTOSAR project! Let me know if you need deeper dive into any module (e.g. ara::com, ara::exec, UCM).

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
