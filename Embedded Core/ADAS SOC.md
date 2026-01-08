**cheatsheet for ADAS SoCs** (Automotive System-on-Chips) — focused on the most relevant ARM-based and other architectures used in production Advanced Driver Assistance Systems and autonomous driving platforms (status January 2026).

### 1. Leading ADAS / Autonomous SoC Families (Production 2025–2026)

| Vendor / SoC Family               | Main CPU Cores (big.LITTLE)          | NPU / AI TOPS (INT8) | GPU / Vision Accelerators       | Automotive Ethernet / TSN | Safety (ASIL) | Typical ADAS Level / Use Case                  | Main OEM / Tier-1 Adoption |
|-----------------------------------|--------------------------------------|-----------------------|----------------------------------|----------------------------|---------------|------------------------------------------------|----------------------------|
| **NVIDIA DRIVE Orin**             | 12× Cortex-A78AE                     | 254 TOPS              | Ampere GPU + 2× DLA              | 10 Gbps + TSN              | ASIL-D        | L2+ → L4 (high-end ADAS & robotaxi)            | Mercedes, Volvo, XPeng, Li Auto |
| **Qualcomm Snapdragon Ride / SA9000 series** | 8–12× Cortex-A78AE / Oryon custom | 30–700 TOPS (scalable) | Adreno GPU + Hexagon AI          | 10 Gbps + TSN              | ASIL-D        | L2+ → L4 central compute & cockpit fusion      | BMW, Mercedes, GM, VW Group |
| **TI Jacinto 8 (J784S4 / TDA4x)** | 4× Cortex-A72 + 4× A53              | 16–32 TOPS            | C7x DSP + MMA vision accel       | 10 Gbps + TSN              | ASIL-D        | L2+ ADAS, infotainment, domain controller      | Many global OEMs (Tier-1 heavy) |
| **Renesas R-Car V4H / Gen5**      | 4× Cortex-A78AE + 4× A55            | 16–60 TOPS            | CV Engine 3.0 + ISP + NPU        | 10 Gbps + TSN              | ASIL-D        | L2+ → L3 ADAS, cockpit, zonal                  | Toyota, Honda, Nissan, European OEMs |
| **NXP S32G3 / S32Z**              | 8× Cortex-A53 / A55                 | 2–8 TOPS              | eIQ NPU + DSP                    | 10 Gbps + TSN              | ASIL-D        | Vehicle gateway, zonal, safety co-processor    | Many European & Chinese OEMs |
| **Mobileye EyeQ6 / EyeQ Ultra**   | Proprietary + Cortex-A (limited)    | 176–1000+ TOPS        | Custom vision & radar processors | 10 Gbps + TSN              | ASIL-D        | L2+ → L4 perception & planning                 | VW, BMW, Zeekr, Polestar |
| **Tesla FSD Computer (HW4 / HW5)**| Custom ARM-like + proprietary       | 400–1000+ TOPS        | Custom neural net accelerators   | Custom high-bandwidth      | ASIL-D        | L2+ → L4 Full Self-Driving                     | Tesla only                 |
| **Ambarella CV5 / CV3-AD**        | 4–8× Cortex-A78AE                   | 50–200 TOPS           | CVflow vision processor          | 10 Gbps + TSN              | ASIL-D        | L2+ → L3 ADAS, surround view                   | Many Tier-1s & Chinese OEMs |

### 2. Key Safety & Automotive Features in ADAS SoCs

| Feature / Block                   | Purpose / Capability                                         | Typical SoC Support (2026) | ASIL Rating |
|-----------------------------------|--------------------------------------------------------------|-----------------------------|-------------|
| **Lock-step safety cores**        | Dual-core lock-step for fail-safe (Cortex-R52/R5F)           | NXP, TI, Renesas            | ASIL-B/D    |
| **Functional Safety Island**      | Isolated safety domain (power, clock, memory)                | NXP, TI, Renesas, Qualcomm  | ASIL-D      |
| **TSN Ethernet**                  | Deterministic networking (802.1AS, Qbv, CB)                  | All high-end                | ASIL-B/D    |
| **IOMMU / SMMU**                  | Memory isolation for mixed-criticality                       | Almost all ARMv8-A auto     | ASIL-B/D    |
| **Hardware Security Module (HSM)**| Secure boot, key storage, crypto acceleration               | NXP HSM, TI HSM, Qualcomm   | ASIL-B/D    |
| **ECC RAM / Cache**               | Error correction for safety-critical memory                  | All automotive-grade        | ASIL-B/D    |
| **Fail-operational support**      | 1oo2D / 2oo2 voting, lock-step + checker                     | NXP, TI, Renesas            | ASIL-D      |

### 3. Typical Software Stacks for ADAS SoCs

| Stack / Platform                 | RTOS / OS Base              | AUTOSAR Support                     | Safety Certification | Typical Use Case |
|----------------------------------|-----------------------------|-------------------------------------|----------------------|------------------|
| **AUTOSAR Adaptive**             | Linux / QNX                 | Native (EB corbos, Vector, QNX)     | ASIL-B/D             | L2+ → L4 fusion & planning |
| **AUTOSAR Classic**              | OSEK/VDX RTOS               | Native                              | ASIL-B/D             | Low-level control & sensors |
| **QNX SDP / Hypervisor**         | QNX Neutrino                | Adaptive + Classic guests           | ASIL-B/D             | Mixed-criticality            |
| **Linux + PREEMPT_RT / Xenomai** | Linux                       | Adaptive (reference)                | ASIL-B (with effort) | Prototyping & non-critical   |
| **ROS 2 / DDS**                  | Linux                       | Bridge to AUTOSAR Adaptive          | QM–ASIL B            | Development & L3+ prototypes |
| **NVIDIA DRIVE OS**              | Linux + QNX guests          | Adaptive bridge possible            | ASIL-D               | High-end NVIDIA platforms    |

### 4. Quick Decision Guide – Which SoC for Which ADAS Level (2026)

| ADAS Level / Function               | Recommended SoC Family (2026)                     | Why / Strengths                              |
|-------------------------------------|---------------------------------------------------|----------------------------------------------|
| **L2 / L2+ (most vehicles)**        | TI Jacinto 7/8, Renesas R-Car V4H, NXP S32G       | Cost-effective, mature ASIL-D, good vision   |
| **High-end L2+ / L3 Highway Pilot** | Qualcomm SA8295P/SA9000, NVIDIA Orin, Renesas Gen5 | High TOPS, strong CPU + GPU, OTA support     |
| **L4 Urban / Robotaxi**             | NVIDIA DRIVE Orin / Thor, Qualcomm SA9000 series, Tesla HW5 | 200–1000+ TOPS, massive compute for DNN      |
| **Zonal / Gateway / Safety co-proc**| NXP S32G3 / S32Z, TI Jacinto 7                    | ASIL-D, TSN Ethernet, safety islands         |
| **Mid-range / Emerging markets**    | Renesas R-Car V4M, TI TDA4VM, NXP S32G            | Balanced cost & performance                  |

### 5. Quick Mnemonics & Rules of Thumb (Jan 2026)

- **ASIL-D** → lock-step R-cores + HSM + ECC RAM + TSN Ethernet is baseline  
- **Central HPC** → Qualcomm SA9000 / NVIDIA Orin / Renesas Gen5  
- **Zonal controllers** → NXP S32G / TI Jacinto  
- **AUTOSAR Adaptive** → dominant for L2+ → L4 perception & planning  
- **AUTOSAR Classic** → still used for low-level actuators & sensors  
- **NPU / vision TOPS** → 8–30 TOPS for L2+, 50–100+ TOPS for L3, 200+ TOPS for L4  
- **Secure boot** → HAB/AHAB (NXP), PSA Certified RoT, TrustZone + measured boot  
- **Ethernet** → 10 Gbps + TSN is now standard for sensor-to-central communication  

This cheatsheet reflects the real production split seen in 2025–2026 vehicles and Tier-1 roadmaps.

Good luck with your ADAS SoC selection, bring-up, or integration!