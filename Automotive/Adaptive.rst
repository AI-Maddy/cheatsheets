
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **cheatsheet for Adaptive AUTOSAR** (AUTOSAR Adaptive Platform) – focused on the most important concepts, architecture, and practical aspects for embedded automotive software development (status early 2026 – Release 23-11 / 24-11 dominant in production vehicles).

📌 1. Adaptive AUTOSAR vs Classic AUTOSAR – Quick Comparison

| Aspect                     | Classic AUTOSAR                              | Adaptive AUTOSAR (ARA)                          | Main Driver / Use Case                     |
|----------------------------|----------------------------------------------|--------------------------------------------------|--------------------------------------------|
| Target ECU type            | Microcontroller (small–medium)               | High-performance processor (multi-core)          | HPC ECUs, central compute                  |
| Execution model            | Static, fixed schedule (OSEK/VDX)            | Dynamic, POSIX threads + event-driven            | Service-oriented, runtime adaptive         |
| Communication              | Signal-based (CAN, CAN-FD, FlexRay, LIN)     | Service-oriented (SOME/IP, DDS, Ethernet)        | High-bandwidth Ethernet                    |
| OS                         | OSEK/VDX RTOS (static tasks)                 | POSIX RTOS (Linux, QNX, etc.)                    | Flexibility & rich middleware              |
| Update / OTA               | Difficult (monolithic image)                 | Designed for OTA / partial updates               | Software-defined vehicle (SDV)             |
⭐ | Safety                     | ASIL-B–D (static)                            | ASIL-B–D + mixed-criticality (QM + ASIL)         | Zonal / central compute                    |
| Typical release year       | 2010–2020 dominant                           | 2020–2025 ramp-up (first series 2022–2023)       | Level 2+/3+ ADAS, infotainment, HPC        |

📌 2. Core Adaptive AUTOSAR Layers & Blocks

⭐ | Layer / Module             | Abbreviation | Main Responsibility / Key APIs                          | Typical Implementation | Detailed Guide |
|----------------------------|--------------|----------------------------------------------------------|------------------------|----------------|
| Application                | —            | User SWCs (Adaptive Applications)                        | C++ / ARA::com           |                |
| Execution Management       | EM           | Lifecycle, state machine, mode management                | ara::exec              |                |
| Communication Management   | CM           | SOME/IP service discovery, RPC, event subscription       | ara::com               |                |
| Platform Health Management | PHM          | Alive supervision, heartbeat, error reporting           | ara::phm               | See `Platform_Health_Management.rst`_ |
| Update & Configuration Management | UCM     | OTA, manifest parsing, software package installation    | ara::ucm               |                |
| State Management           | SM           | Machine state transitions (Startup, Running, Shutdown)   | ara::sm                |                |
⭐ | Persistency                | —            | Key-value store, file-based persistence                  | ara::persistency       |                |
| Diagnostics                | —            | UDS over SOME/IP, DTC handling                           | ara::diag              |                |
| Time Synchronization       | —            | gPTP / PTP time sync across ECUs                         | ara::timesync          |                |
| RESTful / HTTP             | —            | Optional web services                                    | ara::rest              |                |
| Safe Hardware Acceleration | SHWA         | GPU/FPGA/DSP acceleration for ADAS, AI inference         | ara::shwa              | See `Safe_Hardware_Acceleration_API.rst`_ |

.. _Platform_Health_Management.rst: Platform_Health_Management.rst
.. _Safe_Hardware_Acceleration_API.rst: Safe_Hardware_Acceleration_API.rst

⭐ 📚 3. Key ARA APIs & Usage Patterns (C++)

.. code-block:: cpp

// ara::com – Service-oriented communication
ara::com::ServiceHandleContainer handles = proxy->FindService("Service/Instance");
auto proxy = proxyFactory->CreateProxy(handles[0]);

proxy->MethodAsync(args).then([](auto result) { /* handle */ });
proxy->Event.Subscribe([](auto value) { /* callback */ });

// ara::exec – Execution context
ara::exec::AdaptiveApplication app;
app.Initialize(argc, argv);
app.Run();

// ara::phm – Platform Health Management
ara::phm::HealthMonitoring healthMonitoring;
healthMonitoring.ReportEvent("Checkpoint1", ara::phm::HealthStatus::kOk);

// ara::ucm – Update & Configuration
ara::ucm::UpdateManager updateMgr;
updateMgr.ProcessUpdatePackage(packagePath);

⭐ ⚙️ 4. Important Manifests & Configuration Files

| File / Artifact              | Purpose                                              | Location / Tooling                  |
|------------------------------|------------------------------------------------------|-------------------------------------|
| **ARXML**                    | System description, service interfaces, deployment   | Design tool (DaVinci, EB tresos, Vector) |
| **Application Manifest**     | SWC ports, QoS, dependencies                         | ``application.arxml``                 |
| **Execution Manifest**       | Threads, scheduling, resource groups                 | ``execution.arxml``                   |
| **Service Instance Manifest**| SOME/IP service discovery config                     | ``service.arxml``                     |
| **Machine Manifest**         | State machine, startup/shutdown sequence             | ``machine.arxml``                     |
| **Update Manifest**          | OTA package description (signature, version)         | ``update.arxml``                      |

🌐 5. Communication Stack (SOME/IP + Ethernet)

| Component               | Protocol / Standard               | Typical Use in Adaptive AUTOSAR                  | Notes |
|-------------------------|-----------------------------------|--------------------------------------------------|-------|
| SOME/IP                 | Scalable service-Oriented MiddlewarE over IP | Service discovery, RPC, events, fields           | Dominant |
| Service Discovery       | SOME/IP-SD                        | Dynamic service find/offer                       | Multicast |
| RPC / Events            | SOME/IP PDU                       | Method invocation, event subscription            | Reliable / unreliable |
⭐ | DDS (optional)          | Data Distribution Service         | Publish-subscribe (pub/sub)                      | Safety-critical use |
| Time-Sensitive Networking (TSN) | IEEE 802.1 standards         | Deterministic Ethernet                           | Emerging in zonal |

⭐ 🛡️ 6. Safety & Mixed-Criticality Patterns

| Pattern                        | Description                                      | Typical RTOS / Hypervisor |
|--------------------------------|--------------------------------------------------|----------------------------|
| **QM + ASIL partition**        | QM Linux + ASIL guest in VM / partition          | QNX Hypervisor, Jailhouse, Xen |
| **ASIL decomposition**         | ASIL-D → (ASIL-B(D) + ASIL-B(D))                 | Lock-step + monitoring     |
| **Freedom from interference**  | Time & space partitioning                        | ARINC 653 style (PikeOS, INTEGRITY) |
| **Health monitoring**          | PHM + heartbeat + error containment              | ara::phm + watchdog        |

💻 7. Popular Adaptive AUTOSAR Implementations (2026)

| Vendor / Stack             | RTOS Base             | Strength / Focus                              | Typical OEMs / Tier-1 |
|----------------------------|-----------------------|-----------------------------------------------|-----------------------|
| **EB corbos Adaptive**     | QNX / Linux           | Full stack, strong SOME/IP                    | Continental, Bosch    |
| **Vector MICROSAR Adaptive** | Linux / QNX         | Toolchain integration (DaVinci)               | Many German OEMs      |
| **AUTOSAR Adaptive (open)**| Linux (reference)     | Open-source parts, learning                   | Research / startups   |
| **QNX Adaptive Platform**  | QNX Neutrino          | Safety-certified, hypervisor support          | North American OEMs   |
| **Elektrobit corbos**      | QNX / Linux           | High safety & OTA                             | Global Tier-1         |

📌 8. Quick Mnemonics & Rules of Thumb

- **Adaptive ≠ Classic** – completely different runtime & communication model
- **SOME/IP is the heart** – learn SD, RPC, events, serialization
- **POSIX + C++** – no OSEK tasks, use threads & futures/promises
- **OTA is mandatory** – UCM + signed packages + rollback
- **Safety still applies** – ASIL decomposition + PHM + partitioning
- **Ethernet backbone** – 100/1000BASE-T1 → zonal architecture
- **First project pain** – manifest consistency, service discovery, PHM timeouts

📌 9. New in R25-11 (2025-2026)

**Key Updates:**

⭐ - **Platform Health Management (ara::phm)** – Major API refinement
  
  - Removed deprecated Health Channel concept
  - Simplified SupervisedEntity API
  - Enhanced supervision modes and recovery actions
  - Better integration with hardware watchdog
  - **See:** `Platform_Health_Management.rst`_ for complete guide

⭐ - **Safe Hardware Acceleration API (ara::shwa)** – First stable release
  
  - Standardized GPU/FPGA/DSP acceleration
  - ASIL-B/D certified parallel computing
  - Queue, Buffer, Accessor abstractions (SYCL-inspired)
  - Device health monitoring for safety-critical use
  - **See:** `Safe_Hardware_Acceleration_API.rst`_ for complete guide

- **Security & Crypto Updates**
  
  - Enhanced ara::crypto with post-quantum algorithms
  - Improved key management

- **Time Synchronization**
  
  - Better gPTP support for TSN networks

⭐ This cheatsheet covers the essentials for understanding, developing, or integrating with Adaptive AUTOSAR in modern automotive HPC ECUs.

🟢 🟢 Good luck with your Adaptive AUTOSAR project!

================================================================================

**Last updated:** January 2026 (R25-11)

================================================================================

**Last updated:** January 2026
