**ADAS + ASIL Cheat Sheet**  
(oriented toward automotive embedded systems in 2025–2026, focusing on L2+/L3 systems, ISO 26262 functional safety levels, and realistic ASIL allocations)

### 1. ADAS Levels & Typical ASIL Requirements (2025–2026 production reality)

SAE Level | Name                        | Key Functions (series production 2025–2026)                  | Dominant ASIL Allocation
----------|-----------------------------|---------------------------------------------------------------|----------------------------
L1        | Driver Assistance           | ACC, AEB (basic), LKA (informative)                           | Mostly **ASIL B**
L2        | Partial Automation          | Adaptive Cruise + Lane Centering + AEB + TSR + ISA            | **ASIL B** (perception & control), **ASIL B(D)** for braking/steering intervention
L2+       | Enhanced L2                 | Highway Assist, Auto Lane Change, Traffic Jam Assist          | **ASIL B(D)** (actuation paths), **ASIL B** perception
L3        | Conditional Automation      | Eyes-off highway driving (hands-off in defined ODD)           | **ASIL D** (fallback & monitoring), **ASIL C/D** actuation, **ASIL B** perception
L4        | High Automation             | Robotaxi prototypes / very limited ODD                        | **ASIL D** across critical paths + redundancy

**Most common pattern in 2025–2026 mass production**  
→ **ASIL B(D)** decomposition for actuation  
→ **ASIL B** for perception & planning  
→ **QM / ASIL A** for infotainment overlays & HMI

### 2. ASIL Quick Reference Table (ISO 26262)

ASIL | Random Hardware Failure Target (SPFM / LFM) | Typical Diagnostic Coverage | Typical Architectural Measures                     | Typical ADAS Functions
-----|---------------------------------------------|------------------------------|-----------------------------------------------------|-------------------------
QM   | —                                           | —                            | Basic quality management                            | HMI, logging, non-safety-critical UI
A    | SPFM ≥ 90%, LFM ≥ 60%                       | Low                          | Single core + basic watchdog                            | Informative warnings (e.g. TSR display)
B    | SPFM ≥ 90%, LFM ≥ 60%                       | Medium                       | Lockstep cores, ECC memory, E2E protection          | Most L2 features: AEB, LKA, ACC
C    | SPFM ≥ 97%, LFM ≥ 80%                       | High                         | Independent monitoring channel, diverse software    | Some L2+ highway actuation paths
D    | SPFM ≥ 99%, LFM ≥ 90%                       | Very high                    | Dual diverse channels, high diagnostic coverage     | Fallback computer, braking/steering intervention, L3 monitoring

**SPFM** = Single Point Fault Metric  
**LFM**  = Latent Fault Metric

### 3. Typical ASIL Decomposition Patterns in ADAS (very common 2025–2026)

Decomposition       | Meaning                                      | Example in ADAS system
--------------------|----------------------------------------------|-----------------------------------------------
**ASIL B(D)**       | QM + ASIL B = effective ASIL D               | Main braking ECU path + independent plausibility check
**ASIL C(D)**       | ASIL B + ASIL C = effective ASIL D           | Perception ASIL B + diverse monitoring path ASIL C
**ASIL D(D)**       | Two independent ASIL D paths                 | Dual SoC lockstep (very expensive – rare)
**ASIL B + QM**     | ASIL B for safety-relevant, QM for rest      | Perception pipeline ASIL B, non-critical post-processing QM

### 4. Common ASIL Allocation by Subsystem (2025–2026 series vehicles)

Subsystem / Function           | Typical ASIL | Rationale / Notes
-------------------------------|--------------|-------------------------
Perception (camera/radar fusion) | **ASIL B**   | High diagnostic coverage difficult → usually not decomposed higher
Path planning / decision making  | **ASIL B**   | Same as perception
Trajectory control / actuators   | **ASIL B(D)** or **ASIL C(D)** | Actuation path needs higher integrity
Fallback / degradation manager   | **ASIL D**   | Must guarantee safe state in L3+
Redundancy / monitoring channel  | **ASIL C/D** | Independent from main channel
Sensor drivers / ISP             | **ASIL B**   | Raw data integrity
Communication (Ethernet/CAN-FD)  | **ASIL B**   | E2E protection mandatory
Power supply monitoring          | **ASIL D**   | Critical for fail-operational
HSM / security module            | **ASIL B**   | Cyber-security + functional safety overlap

### 5. Quick ASIL vs Development Effort Comparison

ASIL | Tool Qualification (TCL) | Verification Effort | Coding Restrictions (MISRA) | Typical Cost Multiplier
-----|---------------------------|----------------------|------------------------------|-------------------------
QM   | TCL1–TCL2                 | Low                  | Recommended                  | 1×
A    | TCL2                      | Medium               | Strongly recommended         | ~1.5–2×
B    | TCL2–TCL3                 | High                 | Mandatory + deviation report | ~3–5×
C    | TCL3                      | Very high            | Strict + static analysis     | ~6–10×
D    | TCL3                      | Extremely high       | Very strict + formal methods | ~10–20×

### 6. Key Standards & Guidelines (ADAS + Safety 2025–2026)

Standard / Guideline          | Scope / Focus                               | Mandatory for series production?
------------------------------|---------------------------------------------|------------------------------------
**ISO 26262**                 | Functional safety                           | Yes (main standard)
**ISO/SAE 21434**             | Cybersecurity                               | Yes (Type Approval 2024+)
**ISO 21448 (SOTIF)**         | Safety Of The Intended Functionality        | Yes (especially L2+/L3)
**AUTOSAR Adaptive**          | High-performance perception & planning      | Common in domain controllers
**SAE J3061**                 | Cybersecurity process                       | Guidance
**ISO 21434 + UNECE WP.29 R155/R156** | Cybersecurity management & updates   | Mandatory in EU, China, Japan
**Aspice 4.0**                | Process maturity                            | OEM requirement (BMW, VW, etc.)

### 7. Quick Memory & One-liners (what people actually say)

- “We run perception ASIL B and decompose actuation to B(D) with a safety island.”
- “L3 needs ASIL D on the fallback path — that’s why we have two independent SoCs.”
- “Never trust perception above ASIL B without independent monitoring.”
- “Most OEMs still target ASIL B for camera fusion — higher is too expensive.”
- “Use E2E protection on SOME/IP and Automotive Ethernet.”
- “HSM is ASIL B but needs to support ASIL D use-cases via partitioning.”

Good luck with your ADAS safety case!  
In 2026 the sweet spot for most L2+ systems is still **ASIL B perception + ASIL B(D) actuation** with strong monitoring — full ASIL D everywhere remains very rare outside of L3 highway pilots and braking systems.