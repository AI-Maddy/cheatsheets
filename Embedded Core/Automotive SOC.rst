
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for ARM-based Automotive SoCs** (2025–2026 status), focused on the most relevant families, features, safety capabilities, and ecosystem used in production vehicles (ADAS, infotainment, zonal controllers, central compute, gateways, domain controllers).

⭐ 🚗 1. Key ARM Automotive SoC Families (2026 Production)

| Vendor / SoC Family              | Main Cortex Cores (big.LITTLE)       | Safety Cores (lock-step) | NPU / Vision Accelerators | Max Automotive Ethernet | Typical ASIL Target | Main Applications (2026) |
|----------------------------------|--------------------------------------|---------------------------|----------------------------|--------------------------|---------------------|---------------------------|
| **NXP S32G / S32G2 / S32G3**     | 4–8× Cortex-A53 / A55               | 4–8× Cortex-R52           | eIQ NPU (0.5–2 TOPS)       | 2.5/10 Gbps + TSN        | ASIL-B/D            | Vehicle gateway, zonal, safety co-processor |
| **NXP S32K**                     | Cortex-M7 / M33                     | Cortex-R52 (lock-step)    | —                          | —                        | ASIL-B/D            | MCU / body / chassis control |
| **TI Jacinto 7 (TDA4VM, J721E)** | 2× Cortex-A72 + 4× A53              | 6–8× Cortex-R5F           | C7x DSP + MMA (8 TOPS)     | 2.5/10 Gbps + TSN        | ASIL-B/D            | ADAS, infotainment, domain controller |
| **TI Jacinto 8 / J784S4**        | 4× Cortex-A72 + 4× A53              | 8× Cortex-R5F             | C7x + MMA (16 TOPS)        | 10 Gbps + TSN            | ASIL-B/D            | High-end ADAS, L2+/L3 fusion |
| **Qualcomm SA8295P / SA8255P**   | 8× Cortex-A78AE                     | —                         | Hexagon AI (30 TOPS)       | 10 Gbps + TSN            | ASIL-B/D            | Central compute, cockpit, ADAS |
| **Qualcomm SA9000 series**       | Cortex-A78AE + A55                  | —                         | Hexagon (higher TOPS)      | 10 Gbps + TSN            | ASIL-B/D            | Next-gen zonal / central compute |
| **Renesas R-Car V4H / V4M**      | 4× Cortex-A78AE + 4× A55            | 4× Cortex-R52             | CV Engine (16 TOPS)        | 10 Gbps + TSN            | ASIL-B/D            | ADAS, cockpit, infotainment |
| **Renesas R-Car Gen5 (2026–)**   | Cortex-A78AE / A55                  | Cortex-R52                | CV Engine + NPU            | 10 Gbps + TSN            | ASIL-B/D            | L3/L4 central compute |
| **NVIDIA DRIVE Orin**            | 12× Cortex-A78AE                    | —                         | 254 TOPS DLA + GPU         | 10 Gbps + TSN            | ASIL-B/D            | High-end L2+/L3/L4 ADAS |
| **MediaTek Auto**                | Cortex-A78AE / A55                  | Cortex-R52                | APU (10–30 TOPS)           | 10 Gbps                  | ASIL-B/D            | Emerging in mid-range vehicles |

⭐ 🛡️ 2. Key Safety & Automotive Features in ARM Automotive SoCs

| Feature / Block                  | Purpose / Capability                                      | Typical SoC Support (2026)          | ASIL Rating Support |
|----------------------------------|-----------------------------------------------------------|-------------------------------------|---------------------|
| **Lock-step Cortex-R52 / R5F**   | Dual-core lock-step for fail-safe operation               | NXP S32G, TI Jacinto, Renesas R-Car | ASIL-B/D            |
| **Functional Safety Island**     | Isolated safety domain (separate power, clock, memory)    | NXP, TI, Renesas, Qualcomm          | ASIL-D              |
| **TSN (Time-Sensitive Networking)** | Deterministic Ethernet (802.1AS, 802.1Qbv, 802.1CB)     | Most high-end (10 Gbps)             | ASIL-B/D            |
| **ASIL-B/D capable peripherals** | CAN-FD, Ethernet, PCIe, MIPI CSI-2, I²S, UART, etc.       | NXP, TI, Renesas, Qualcomm          | ASIL-B/D            |
⭐ | **Hardware Security Module (HSM)** | Secure boot, key storage, crypto acceleration            | NXP CSEc / HSM, TI HSM, Renesas HSM | ASIL-B/D            |
⭐ | **IOMMU / SMMU**                 | Memory isolation for mixed-criticality                    | Most ARMv8-A automotive SoCs        | ASIL-B/D            |
⭐ | **ECC on RAM / Cache**           | Error correction for safety-critical memory               | Almost all automotive-grade         | ASIL-B/D            |

📡 3. Common ARM Automotive SoC Software Stacks (2026)

| Stack / Platform               | RTOS / OS Base                     | AUTOSAR Support                  | Safety Certification Level | Typical OEM / Tier-1 Users |
|--------------------------------|------------------------------------|----------------------------------|-----------------------------|----------------------------|
| **AUTOSAR Classic**            | OSEK/VDX (SafeRTOS, FreeRTOS)      | Yes (MICROSAR, RTA-OS)           | ASIL-B/D                    | Most powertrain, chassis   |
| **AUTOSAR Adaptive**           | Linux / QNX                        | Yes (corboS, MICROSAR Adaptive)  | ASIL-B/D                    | ADAS, HPC, cockpit         |
| **QNX SDP / Hypervisor**       | QNX Neutrino                       | Adaptive + Classic guests        | ASIL-B/D                    | Many North American OEMs   |
⭐ | **Linux + PREEMPT_RT / Xenomai**| Linux                             | Adaptive (reference)             | ASIL-B (with effort)        | Prototyping, non-critical  |
| **Android Automotive OS**      | Android (Linux base)               | Adaptive bridge possible         | QM–ASIL B                   | Infotainment / cockpit     |
⭐ | **Green Hills INTEGRITY**      | INTEGRITY-178                      | Classic + Adaptive support       | ASIL-D / DAL A              | High-end safety-critical   |

📚 4. Quick Reference – Popular ARM Automotive SoCs (2026)

| SoC Family                     | Cores (big.LITTLE)             | NPU / TOPS           | Ethernet / TSN | Safety (ASIL) | Main OEM / Tier-1 Adoption |
|--------------------------------|--------------------------------|----------------------|----------------|---------------|----------------------------|
| NXP S32G3                      | 8× A53                         | 2 TOPS               | 10 Gbps + TSN  | ASIL-D        | Many European / Chinese    |
| TI Jacinto 8 (J784S4)          | 4× A72 + 4× A53                | 16 TOPS              | 10 Gbps + TSN  | ASIL-D        | Many global OEMs           |
| Qualcomm SA8295P / SA9000      | 8× A78AE                       | 30–50 TOPS           | 10 Gbps + TSN  | ASIL-D        | Premium European / US      |
| Renesas R-Car V4H / Gen5       | 4× A78AE + 4× A55              | 16–30 TOPS           | 10 Gbps + TSN  | ASIL-D        | Japanese & European OEMs   |
| NVIDIA DRIVE Orin              | 12× A78AE                      | 254 TOPS (DLA+GPU)   | 10 Gbps + TSN  | ASIL-D        | High-end L2+/L3/L4         |

📌 5. Quick Mnemonics & Rules of Thumb (2026)

- **ASIL-D** → lock-step Cortex-R52/R5F + HSM + ECC RAM + TSN Ethernet  
- **Central compute / HPC** → Qualcomm SA8xxx / Renesas R-Car Gen5 / NVIDIA Orin  
- **Zonal controllers** → NXP S32G / TI Jacinto 7/8  
- **AUTOSAR Classic** → still dominant for low-level control (powertrain, chassis)  
- **AUTOSAR Adaptive** → dominant for ADAS fusion, cockpit, OTA  
- **TSN + 10 Gbps Ethernet** → standard for sensor-to-central communication  
- **Secure boot** → HAB/AHAB (NXP), PSA Certified RoT, TrustZone + measured boot  
- **NPU / vision** → 8–50 TOPS typical for L2+/L3, 100–250 TOPS for L4  

🟢 🟢 Good luck with your ARM automotive SoC selection, bring-up, or integration work!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
