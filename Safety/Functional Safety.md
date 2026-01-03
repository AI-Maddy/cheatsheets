**Functional Safety Cheat Sheet**  
(focused on **ISO 26262** — the dominant standard for road vehicles in 2025–2026, especially relevant for ADAS, autonomous driving, powertrain, chassis, and e-mobility)

### 1. ASIL Levels at a Glance

Level | Random Hardware Failure Targets          | Typical Diagnostic Coverage | Typical Use in Automotive (2025–2026)
------|------------------------------------------|------------------------------|---------------------------------------
**QM** | —                                        | —                            | Infotainment, comfort functions, non-safety UI
**A**  | SPFM ≥ 90%, LFM ≥ 60%                    | Low                          | Informative warnings (e.g. TSR display only)
**B**  | SPFM ≥ 90%, LFM ≥ 60%                    | Medium                       | Most L2 ADAS (AEB, LKA, ACC), many actuators
**C**  | SPFM ≥ 97%, LFM ≥ 80%                    | High                         | Some L2+ highway actuation, monitoring channels
**D**  | SPFM ≥ 99%, LFM ≥ 90%                    | Very high                    | Braking intervention, steering, L3 fallback & monitoring

**SPFM** = Single-point fault Metric  
**LFM**  = Latent-fault Metric

### 2. Most Important Safety Mechanisms (Hardware + Software)

Mechanism                        | Purpose                                      | Typical ASIL | Common Implementation
---------------------------------|----------------------------------------------|--------------|-------------------------
**Lockstep cores**               | Detect transient & permanent faults          | B–D          | Dual-core comparison (AURIX, R-Car, S32E)
**ECC memory**                   | Detect & correct single-bit errors           | B–D          | DDR5/LPDDR5 with ECC, on-chip SRAM
**E2E Protection**               | End-to-End communication integrity           | B–D          | CRC32 + Counter + Alive + Data ID (SOME/IP, CAN-FD)
**Watchdog**                     | Detects timing & sequence failures           | A–D          | Windowed + independent clock source
**Voltage & Temperature Monitoring** | Detects out-of-range conditions         | B–D          | On-chip sensors + external PMIC
**Diverse redundancy**           | Avoids common cause failures                 | C–D          | Different algorithms / suppliers / cores
**Plausibility checks**          | Cross-checks sensor/actuator values          | B–C          | Independent plausibility monitor
**1oo2D / 2oo2**                 | Voting architectures                         | C–D          | 1-out-of-2 with diagnostics

### 3. Decomposition Patterns (Very Common in 2025–2026)

Notation      | Meaning                                      | Effective Safety | Typical Example in ADAS
--------------|----------------------------------------------|------------------|-------------------------
**ASIL B(D)** | ASIL B + independent QM part                 | ≈ ASIL D         | Main braking path (B) + plausibility check (QM)
**ASIL C(D)** | ASIL C + independent ASIL B part             | ≈ ASIL D         | Actuation (C) + diverse perception monitor (B)
**ASIL D(D)** | Two independent ASIL D channels              | ASIL D           | Dual SoC lockstep (expensive – rare)
**ASIL B + QM** | Safety-relevant part ASIL B, rest QM       | ASIL B           | Perception pipeline (B), non-critical post-processing (QM)

### 4. Key ISO 26262 Parts – Quick Reference

Part | Title / Focus                               | When you read it most
-----|---------------------------------------------|-------------------------
Part 3 | Concept phase – Item definition, HARA      | Early project phase
Part 4 | Product development at system level        | Technical Safety Concept
Part 5 | Product development at hardware level      | FMEDA, metrics calculation
Part 6 | Product development at software level      | Software unit & integration testing
Part 8 | Supporting processes                       | Tool qualification (TCL), configuration management
Part 9 | ASIL-oriented and decomposition            | Decomposition justification
Part 10| Guideline on ISO 26262                     | Explanations & examples
Part 11| Guideline on application of ISO 26262 to semiconductors | SoC suppliers & complex ICs

### 5. Hazard Analysis & Risk Assessment (HARA) – Severity × Exposure × Controllability

Severity (S) | Meaning                          | Example
-------------|----------------------------------|---------
S0           | No injuries                      | —
S1           | Light to moderate injuries       | Whiplash
S2           | Severe injuries (survival probable) | Broken limbs
S3           | Life-threatening / fatal injuries | —

Exposure (E) | Meaning                          | Probability class
-------------|----------------------------------|------------------
E0           | Incredible                       | —
E1           | Very low                         | <0.01%
E2           | Low                              | 0.1–1%
E3           | Medium                           | 1–10%
E4           | High                             | >10%

Controllability (C) | Meaning                     | Driver can avoid?
--------------------|-----------------------------|-------------------
C0                  | Controllable in general     | Yes
C1                  | Normally controllable       | Usually
C2                  | Difficult to control        | Rarely
C3                  | Uncontrollable              | Almost never

**ASIL assignment table** (simplified)

S3 + E4 + C3 → **ASIL D**  
S3 + E3 + C3 → **ASIL C**  
S2 + E4 + C3 → **ASIL B**  
Most ADAS perception → **ASIL B** (S1–S2, medium E, medium C)

### 6. Quick One-liners (what people actually say in meetings 2025–2026)

- “We target ASIL B for perception and decompose actuation to B(D).”
- “The fallback manager must be ASIL D — that’s non-negotiable for L3.”
- “No freedom from interference between QM and ASIL B software.”
- “We use E2E protection profile 1 on all SOME/IP safety-relevant messages.”
- “FMEDA shows SPFM 99.1% — good for ASIL D.”
- “Tool is TCL3 — we performed qualification according to Part 8.”
- “SOTIF analysis is required because perception can fail without fault.”

This cheat sheet covers the ~80% of functional safety vocabulary and concepts you will encounter in automotive projects in 2026. Keep ISO 26262 Part 9 (decomposition) and Part 5 (hardware metrics) close when justifying designs.