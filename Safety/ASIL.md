Here is a concise **cheatsheet for ASIL (Automotive Safety Integrity Level)** — the core safety classification system defined in **ISO 26262** (Functional Safety for Road Vehicles), widely used in automotive embedded systems (ECUs, ADAS, powertrain, chassis, etc.) as of early 2026.

### 1. ASIL Levels – Overview & Mapping

| ASIL Level | Severity (S) | Exposure (E) | Controllability (C) | Typical Safety Goal Example | Typical Failure Rate Target (FIT) | Redundancy / Effort Level | Typical Systems / Functions |
|------------|--------------|--------------|----------------------|------------------------------|------------------------------------|---------------------------|-----------------------------|
| **QM**     | —            | —            | —                    | No safety requirement        | —                                  | Lowest                    | Infotainment, comfort, non-critical UI |
| **ASIL A** | S1 (light)   | E1–E2 (low)  | C1–C2 (easy)         | Minor injury possible        | ~1000–100 FIT                      | Low                       | Rear lights, parking sensors (low risk) |
| **ASIL B** | S1–S2        | E2–E4        | C2–C3                | Moderate injury possible     | ~100–10 FIT                        | Medium                    | Adaptive cruise control, lane assist, most ADAS L1–L2 |
| **ASIL C** | S2–S3        | E3–E4        | C3                   | Severe injury possible       | ~10–1 FIT                          | High                      | Emergency braking (AEB), steering assist |
| **ASIL D** | S3 (life-threatening) | E4 (very high) | C3 (difficult) | Life-threatening / fatal     | <1 FIT                             | Very High                 | Fail-operational steering, braking, autonomous driving L3+ |

**Severity (S)** — consequence of failure  
**Exposure (E)** — probability of situation occurring  
**Controllability (C)** — likelihood driver can mitigate

### 2. ASIL Decomposition – Most Common Patterns

ASIL decomposition allows splitting a high ASIL requirement into lower ASIL sub-parts with independence.

| Original Goal | Decomposition Pattern | Resulting Sub-Goals | Typical Use Case | Freedom from Interference Required? |
|---------------|-----------------------|----------------------|------------------|-------------------------------------|
| ASIL D        | D → (C + D)           | One part ASIL C, redundant ASIL D | Steering, braking | Yes (strong) |
| ASIL D        | D → (B + D)           | One part ASIL B, redundant ASIL D | Most common in practice | Yes |
| ASIL C        | C → (B + C)           | One part ASIL B, redundant ASIL C | Lane keep, ACC | Yes |
| ASIL B        | B → (A + B)           | One part ASIL A, redundant ASIL B | Some sensors | Yes (moderate) |

**Key rule**:  
The decomposed parts must be **independent** (freedom from interference) — use separate cores, memory protection, diverse software, or lock-step + checker.

### 3. ASIL Requirements by Development Phase (ISO 26262)

| Phase / Activity              | QM | ASIL A | ASIL B | ASIL C | ASIL D | Typical Effort Multiplier (vs QM) |
|-------------------------------|----|--------|--------|--------|--------|-----------------------------------|
| Hazard Analysis & Risk Assessment (HARA) | —  | Yes    | Yes    | Yes    | Yes    | 2–5×                              |
| Safety Goals & Functional Safety Requirements | —  | Yes    | Yes    | Yes    | Yes    | 3–10×                             |
| Technical Safety Requirements | —  | Yes    | Yes    | Yes    | Yes    | 5–15×                             |
| System Design                 | —  | Yes    | Yes    | Yes    | Yes    | 5–20×                             |
| Hardware Development          | —  | Basic  | Medium | High   | Very High | 10–50× (ASIL D)                   |
| Software Development          | —  | Basic  | Medium | High   | Very High | 10–50× (ASIL D)                   |
| Unit Testing                  | —  | Yes    | Yes    | Yes    | Yes    | 5–20×                             |
| Integration Testing           | —  | Yes    | Yes    | Yes    | Yes    | 10–30×                            |
| Fault Injection / FMEA / FTA  | —  | Optional | Recommended | Required | Mandatory | 20–100× (ASIL D)                  |
| MC/DC Code Coverage           | —  | —      | —      | Recommended | Mandatory (most parts) | Very high |
| Freedom from Interference     | —  | Basic  | Medium | High   | Very High | Critical for decomposition |

### 4. Common ASIL-Safe Implementation Patterns (2026)

| Safety Mechanism              | Typical ASIL Target | Description / Examples                              | Common RTOS / Tools |
|-------------------------------|---------------------|-----------------------------------------------------|---------------------|
| **Lock-step cores**           | B–D                 | Two cores run same code, compare outputs            | Cortex-R52, TriCore, RH850 |
| **Diverse software**          | C–D                 | Two independent implementations                     | ASIL C + ASIL D path |
| **E2E Protection**            | B–D                 | End-to-end data integrity (CRC + sequence counter)  | AUTOSAR E2E library |
| **Memory Protection Unit (MPU)** | B–D              | Prevent erroneous access between software units     | ARM MPU, RISC-V PMP |
| **Watchdog / Alive Supervision** | B–D            | External or internal watchdog + heartbeat           | AUTOSAR WdgM / PHM |
| **Freedom from Interference** | B–D                 | Time & space partitioning                           | QNX, INTEGRITY, PikeOS |
| **Fail-operational (1oo2D)**  | D                   | 1-out-of-2 with diagnostics                         | Lock-step + voter   |
| **Mixed-criticality**         | B–D                 | QM + ASIL on same SoC (hypervisor)                  | Jailhouse, Xen, QNX Hypervisor |

### 5. Quick Reference – ASIL in Practice (2026 Vehicles)

| Vehicle Function / Level | Typical ASIL (2026) | AUTOSAR Platform | Common Decomposition |
|---------------------------|----------------------|------------------|----------------------|
| Emergency Braking (AEB)   | B–D                  | Classic          | D → (C + D)          |
| Adaptive Cruise Control   | B–C                  | Classic          | C → (B + C)          |
| Lane Keep Assist          | B–C                  | Classic          | B–C                  |
| Highway Pilot (L3)        | D                    | Adaptive         | D → (C + D)          |
| Steering-by-Wire          | D                    | Classic / Adaptive | D → (C + D)       |
| Sensor Fusion (central)   | C–D                  | Adaptive         | C–D                  |
| Infotainment / HMI        | QM                   | Adaptive / Linux | —                    |

**Golden Rules (2026)**  
- **ASIL D** = 10–50× effort vs QM → avoid unless mandatory  
- **Decomposition is king** — D → (C + D) or (B + D) is most common pattern  
- **Freedom from interference** must be proven (MPU, hypervisor, timing analysis)  
- **E2E protection** is mandatory for communication in ASIL B+  
- **Tool qualification** (TQL-1 to TQL-5) is required for ASIL C/D development tools  
- **AUTOSAR Classic** still dominates for ASIL B–D low-level control  
- **AUTOSAR Adaptive** is growing fast for L3+ and central compute  

Use this cheatsheet when doing HARA, decomposition decisions, safety requirements, or comparing ASIL effort across functions.

Good luck with your automotive safety-critical project!