**cheatsheet for ARM SoCs** (System-on-Chip) commonly used in embedded systems, mobile devices, automotive, IoT, servers, and industrial applications (status early 2026).

### 1. Current Main ARM Cortex Families (2026)

| Family / Architecture     | Core Examples (2025–2026)             | Target Markets / Typical Use Cases                          | Max Clock (typical) | Process Node (typical) | Big.LITTLE / DynamIQ Support |
|----------------------------|----------------------------------------|-------------------------------------------------------------|----------------------|--------------------------|-------------------------------|
| **Cortex-A7x series**      | A76, A77, A78, A710, A715, A720       | High-performance mobile, automotive HPC, edge AI            | 2.8–3.5 GHz          | 4–5 nm                   | Yes (DynamIQ)                 |
| **Cortex-A5x series**      | A55, A510, A520                       | Power-efficient application processor                       | 1.8–2.5 GHz          | 5–7 nm                   | Yes                           |
| **Cortex-X series**        | X1, X2, X3, X4, X925                  | Flagship mobile performance (big core)                      | 3.4–4.0+ GHz         | 3–4 nm                   | Yes                           |
| **Cortex-R series**        | R52, R82                              | Real-time, safety-critical (automotive, industrial)         | 1.0–2.0 GHz          | 7–16 nm                  | No (lock-step capable)        |
| **Cortex-M series**        | M7, M33, M55, M85, M7+                | Microcontrollers, low-power IoT, sensors                    | 100–800 MHz          | 22–40 nm                 | No                            |
| **Neoverse**               | N1, N2, V1, V2, E1, N3, V3            | Servers, HPC, networking, edge cloud                        | 2.5–3.8 GHz          | 5–7 nm                   | Yes (multi-chip)              |

### 2. Major ARM SoC Vendors & Popular Chips (2026)

| Vendor / Silicon Company       | Key SoC Families (2025–2026)                        | Cortex Cores (typical)       | Target Markets                          | Notable Features / Strengths |
|--------------------------------|-----------------------------------------------------|-------------------------------|-----------------------------------------|--------------------------------|
| **Qualcomm**                   | Snapdragon 8 Gen 3/4, Snapdragon SA8xxx (auto)      | X4 + A720 + A520             | Mobile flagship, automotive ADAS/HPC    | Oryon custom cores, strong NPU, 5G |
| **MediaTek**                   | Dimensity 9300/9400, Genio series                   | X4 + A720 + A520             | Mobile mid-high, IoT, automotive        | Cost-effective, good power efficiency |
| **Samsung**                    | Exynos 2400/2500, Exynos Auto V920                  | X4 + A720 + A520             | Mobile, automotive infotainment         | Strong AMOLED integration |
| **NXP**                        | i.MX 8/9 series, S32G/S32K                          | A76/A55, R52                  | Automotive (ADAS, gateway, MCU)         | ASIL-B/D support, strong safety |
| **Texas Instruments**          | Jacinto 7/8 (TDA4, J721E, J784S4)                   | A72/A53, R5F                  | Automotive ADAS, infotainment           | Strong DSP, vision accelerators |
| **Rockchip**                   | RK3588 / RK3588S, RV1126                            | A76 + A55                     | Industrial, SBC, AI edge                | Cost-effective, good multimedia |
| **Allwinner**                  | H616, H700, A733                                    | A53 / A55                     | Low-cost consumer, IoT                  | Very low price |
| **Amlogic**                    | S905X5, S928X                                       | A76 + A55                     | Set-top boxes, smart displays           | AV1 decoding, good video |
| **Broadcom**                   | BCM2712 (Raspberry Pi 5)                            | Cortex-A76                    | SBC, hobbyist                           | Raspberry Pi ecosystem |
| **Ampere**                     | AmpereOne, Altra                                    | Neoverse N1/N2                | Cloud, edge servers                     | High core count (up to 192) |

### 3. Key ARM SoC Features in 2026

| Feature / Block               | Typical Implementation (2025–2026)                     | Benefit / Use Case                              |
|-------------------------------|--------------------------------------------------------|-------------------------------------------------|
| **DynamIQ Shared Unit**       | Shared L3 cache, power domains, cluster topology       | Better power/performance scaling                |
| **NPU / AI Accelerator**      | Qualcomm Hexagon, MediaTek APU, NXP eIQ, TI C7x        | On-device ML inference (object detection, etc.) |
| **GPU**                       | ARM Mali-G720/G720 Immortalis, Adreno, PowerVR         | UI, infotainment, light gaming                  |
| **Safety Islands**            | Lock-step Cortex-R52, ASIL-D capable                   | Functional safety (ASIL B–D)                    |
| **TSN / Automotive Ethernet** | 100/1000BASE-T1, 2.5/10GBASE-T1                        | Zonal architecture, high-bandwidth              |
| **Secure Enclave / HSM**      | ARM TrustZone, PSA Certified RoT, DICE                 | Secure boot, key storage, attestation           |
| **USB & PCIe**                | USB 3.2 Gen 2, PCIe 4.0/5.0 lanes                      | High-speed peripherals, storage                 |

### 4. Common Development & Bring-up Tools for ARM SoCs

| Tool / Environment            | Primary Use Case                              | Typical SoCs / Vendors                     | Notes |
|-------------------------------|-----------------------------------------------|--------------------------------------------|-------|
| **Buildroot / Yocto**         | Custom Linux distribution                     | Almost all                                      | Yocto dominant in automotive |
| **U-Boot**                    | Bootloader (SPL + main)                       | All i.MX, Rockchip, Allwinner, NXP          | FIT image + HAB/AHAB |
| **TF-A (Trusted Firmware-A)** | BL31 / secure monitor                         | Most ARMv8-A SoCs                           | Secure boot base |
| **OP-TEE**                    | Trusted OS in TrustZone                       | Qualcomm, NXP, MediaTek                     | Secure storage, RPMB |
| **scp / M33 firmware**        | System control processor (power, clocks)      | NXP, TI, MediaTek                           | Low-power management |
| **Lauterbach TRACE32**        | JTAG/SWD debugging, trace                     | All high-end ARM SoCs                       | Industry standard |
| **Segger J-Link / Ozone**     | Debugging, flashing                           | Most embedded ARM                           | Cost-effective |
| **NXP MCUXpresso**            | i.MX / LPC development                        | NXP i.MX, RT series                         | Vendor-specific IDE |

### 5. Quick Reference – Popular ARM SoC Families (2026)

| SoC Family / Series      | Cortex Cores (big.LITTLE)      | NPU / GPU                     | Typical Applications                  | Secure Boot Mechanism |
|---------------------------|--------------------------------|-------------------------------|----------------------------------------|-----------------------|
| Qualcomm Snapdragon 8 Gen 4 | Oryon + A720 + A520           | Hexagon NPU, Adreno           | Flagship phones, automotive HPC        | HAB / AHAB + TrustZone |
| MediaTek Dimensity 9400   | X4 + A720 + A520              | MediaTek APU 890              | Mid-high phones, IoT gateways          | HAB / AHAB            |
| NXP i.MX 93               | A55 + Cortex-M33              | 0.5–2.5 TOPS NPU              | Industrial, automotive zonal           | AHAB                  |
| TI Jacinto 7/8            | A72 + R5F                     | C7x DSP + vision accelerators | ADAS, infotainment                     | HABv4 / custom        |
| Rockchip RK3588           | 4×A76 + 4×A55                 | 6 TOPS NPU, Mali-G610         | SBC, edge AI, industrial               | HABv4                 |

### Quick Mnemonics & Rules of Thumb

- **New high-end** → Cortex-X + A720 + A520 + big NPU  
- **Automotive safety** → Cortex-R52 lock-step + ASIL-B/D qualified peripherals  
- **Low-cost / IoT** → Cortex-A55 + M33 + small NPU  
- **Secure boot** → HABv4 (old i.MX) → AHAB (new i.MX) → fuses + CSF/AHAB container  
- **Bring-up pain** → DDR timing, clock tree, power domains, pinctrl, ATF/OP-TEE integration  
- **Linux support** → mainline kernel 6.6–6.12 has good support for i.MX93, RK3588, Snapdragon 8 Gen 3

Good luck with your ARM SoC bring-up or selection!