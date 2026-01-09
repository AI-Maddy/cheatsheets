
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for system engineering in automotive avionics & embedded systems development** (2025–2026 perspective).

Focuses on the most important standards, processes, tools, architectures, and trade-offs used in modern automotive (ADAS, autonomous driving, zonal, software-defined vehicles) and avionics (🟢 🟢 DO-178C, ARINC 653, integrated modular avionics) projects.

🛡️ 1. Core Safety & Certification Standards

⭐ | Domain       | Standard              | SIL/ASIL Level Mapping          | Key Focus / Artifacts Required                          | Typical Certification Level (2025–2026) |
|--------------|-----------------------|----------------------------------|----------------------------------------------------------|------------------------------------------|
| Automotive   | ISO 26262             | ASIL A–D                        | HARA, FMEA, FTA, safety goals, freedom from interference | ASIL B–D dominant (ADAS, powertrain)     |
| Automotive   | ISO/SAE 21434         | —                               | Cybersecurity risk assessment, TARA, SBOM, secure boot   | Mandatory in UNECE WP.29 R155/R156       |
| Automotive   | AUTOSAR Adaptive      | —                               | Service-oriented architecture, SOME/IP, ARA::COM         | High-end ADAS / autonomous (Level 3+)    |
| Automotive   | AUTOSAR Classic       | —                               | OSEK/VDX RTOS, CAN-FD, SOME/IP lite                      | Powertrain, chassis, body                |
| Avionics     | 🟢 🟢 DO-178C               | DAL A–E                         | Objectives table A-1 to A-9, traceability, structural coverage | DAL B–C most common (display, comms)     |
| Avionics     | 🟢 🟢 DO-254                | DAL A–E                         | Hardware design assurance (FPGA/ASIC)                    | DAL B–C for complex electronics          |
| Avionics     | ARINC 653             | —                               | Time & space partitioning, APEX API                      | IMA (Integrated Modular Avionics)        |
| Avionics     | ARP4754A              | —                               | System development process, FHA, PSSA, SSA               | Top-level civil aircraft systems         |
| Cross-domain | IEC 61508             | SIL 1–4                         | Generic functional safety                                | Reference for non-automotive/avionics    |

📌 2. Typical Development Process Comparison

| Phase / Activity              | Automotive (ISO 26262 + ASPICE)                  | Avionics (🟢 🟢 DO-178C + ARP4754A)                     | Key Differences / Trade-offs |
|-------------------------------|--------------------------------------------------|---------------------------------------------------|--------------------------------|
| Hazard Analysis               | HARA (ASIL decomposition possible)               | FHA / PSSA                                        | Automotive allows ASIL decomposition |
| Requirements                  | SysRS / TechRS, bidirectional traceability       | High-Level / Low-Level Requirements               | Avionics stricter on derived requirements |
| Design                        | Software architecture + detailed design          | Software & hardware detailed design               | Automotive more agile, avionics more waterfall |
| Implementation                | MISRA C 2023 / AUTOSAR C++14                     | MISRA C / subset + qualified compiler             | Avionics compiler qualification mandatory |
| Verification                  | Unit + integration + HIL + back-to-back          | Structural coverage (MC/DC for DAL A/B), SOI      | Avionics MC/DC coverage mandatory |
| Validation                    | Vehicle / road testing + simulation              | System integration lab + flight test              | Automotive simulation-heavy (MiL/SiL/HiL) |
| Configuration Management      | ASPICE SUP.1 + Git / Perforce                    | Strict CM + problem reporting (PRR)               | Avionics enforces tool qualification |
| Change & Problem Management   | ASPICE SUP.8 + Jira / Polarion                   | Problem reports, change impact analysis           | Avionics change impact more rigorous |

🏗️ 3. Common Architectural Patterns (2025–2026)

⭐ | Pattern / Architecture         | Domain                  | Key Characteristics                                      | Typical RTOS / Framework |
|--------------------------------|-------------------------|------------------------------------------------------------------|---------------------------|
| Zonal E/E Architecture         | Automotive (SDV)        | Domain → zonal, high-speed Ethernet backbone, central compute   | AUTOSAR Adaptive / QNX / Linux |
| Centralized Compute (SDV)      | Automotive Level 3+     | Few powerful ECUs + service-oriented (SOME/IP, DDS)             | Adaptive AUTOSAR / ROS2 / DDS |
| Federated (classic)            | Automotive legacy       | Many ECUs, CAN-FD, LIN, FlexRay                                 | Classic AUTOSAR / OSEK       |
| Integrated Modular Avionics (IMA) | Avionics             | ARINC 653 partitioning, time & space separated                  | PikeOS, INTEGRITY-178, VxWorks 653 |
⭐ | Mixed-Criticality              | Both                    | AMP / SMP + partitioning / hypervisor                           | QNX, PikeOS, seL4, Jailhouse |
| Fail-Operational (ASIL-D)      | Automotive              | 1oo2D / 2oo2 voting, lock-step cores, diverse redundancy        | SafeRTOS, QNX Safe Kernel    |

⚙️ 4. Toolchain & Qualification Landscape

| Category               | Automotive (common 2026)                  | Avionics (common 2026)                     | Qualification Level |
|------------------------|-------------------------------------------|--------------------------------------------|----------------------|
| Compiler               | GCC / LLVM (with MISRA checker)           | Green Hills, TASKING, IAR (qualified)      | TQL-1 / QSK          |
| RTOS                   | QNX, INTEGRITY, FreeRTOS (with cert kit)  | INTEGRITY-178 tuMP, PikeOS, VxWorks 653    | ASIL-D / DAL A       |
| Static Analysis        | Polyspace, Coverity, Cppcheck, Astrée     | Astrée, Polyspace (qualified)              | TQL-2/3              |
| Requirements / Trace   | Polarion, DOORS, Jama, Codebeamer         | DOORS NG, Visure, ReqIF                     | —                    |
| Model-Based Design     | Simulink / TargetLink (ASIL-D qualified)  | SCADE (🟢 🟢 DO-178C qualified)                  | TQL-1                |
⭐ | HIL / Test Automation  | dSPACE, Vector VT, NI VeriStand           | dSPACE, Speedgoat, Keysight                | —                    |
| Cybersecurity          | Vector Security, Argus, ID Quantique      | Collins, Garmin internal tools             | ISO 21434            |

⭐ 📚 5. Quick Reference – Critical Trade-offs (2025–2026)

| Decision Point                | Automotive Preference                     | Avionics Preference                        | Reason / Driver |
|-------------------------------|-------------------------------------------|--------------------------------------------|-----------------|
| Linux vs RTOS                 | Linux + PREEMPT_RT / Xenomai (ADAS)       | Certifiable RTOS (PikeOS, INTEGRITY)       | Certification cost vs flexibility |
| AUTOSAR vs ROS2               | AUTOSAR Adaptive (OEMs)                   | —                                          | Standardization vs ecosystem |
| Ethernet vs CAN-FD            | Automotive Ethernet (100/1000BASE-T1)     | ARINC 664 / AFDX                           | Bandwidth & future-proofing |
| Hardware redundancy           | 1oo2D / lock-step + diverse design        | 1oo2 / 2oo2 voting                         | ASIL-D / DAL A requirements |
| OTA / FOTA                    | Mandatory (R156)                          | Very limited / controlled                  | Safety vs business model |
| Agile / DevOps                | Increasing (SAFe + ASPICE hybrid)         | Very restricted                            | Speed vs certification |

📌 6. Quick Mnemonics & Rules of Thumb

- **ASIL-D / DAL-A** → assume **2× effort** compared to ASIL-B / DAL-C
- **MC/DC coverage** → ~30–50% more test cases than statement coverage
- **ASIL decomposition** → D→(C+D) or C→(B+D) — most common pattern
- **Freedom from interference** → spatial (memory protection) + temporal (timing partitioning)
- **Secure boot + root of trust** → mandatory for ISO 21434 / UNECE compliance
- **zonal + central compute** → 2025–2030 dominant trend in premium vehicles

Use this cheatsheet as a quick reference when switching domains, preparing for audits, or comparing automotive vs avionics development constraints.

🟢 🟢 Good luck with your next safety-critical embedded project!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
