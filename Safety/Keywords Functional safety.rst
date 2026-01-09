
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **Keyword List related to Functional Safety**  
⭐ covering Fault Analysis, Fault Tolerance, HARA, and related Functional Safety concepts (especially relevant for ISO 26262, ADAS, and safety-critical embedded systems in 2025–2026) including **MTBF** and other key statistical / reliability terms commonly used in fault analysis, fault tolerance, HARA, FMEDA, and functional safety (ISO 26262, IEC 61508, etc.) as of 2026.

🛡️ Hazard Analysis & Risk Assessment (HARA) & Safety Goals

- **HARA** – Hazard Analysis and Risk Assessment: systematic process to identify hazards, evaluate risks, and assign ASILs  
- **Item** – System or component under consideration in the safety lifecycle (the “thing” being analyzed)  
- **Hazard** – Potential source of harm (e.g. unintended acceleration, loss of steering)  
- **Safety Goal** – Top-level safety requirement derived from HARA (e.g. “prevent unintended braking”)  
- **Severity (S)** – Expected harm level if hazard occurs (S0–S3 scale)  
- **Exposure (E)** – Likelihood of the hazardous situation occurring (E0–E4)  
- **Controllability (C)** – Ability of driver/system to 🔴 🔴 avoid or mitigate harm (C0–C3)  
- **ASIL** – Automotive Safety Integrity Level: safety integrity requirement (QM to D)  
- **Operational Situation** – Specific driving condition in which hazard can occur  

📌 Fault & Failure Related Terms

- **Fault** – Defect or anomaly in hardware/software (root cause)  
- **Error** – Incorrect internal state caused by a fault  
- **Failure** – Incorrect service delivered to user/environment (manifestation)  
- **Random Hardware Failure** – Failure due to aging, wear-out, radiation, etc.  
- **Systematic Failure** – Design, manufacturing, or process error (not random)  
- **Single Point of Failure (SPF)** – One element whose failure directly violates safety goal  
- **Latent Fault** – Dormant fault that becomes dangerous only when combined with others  
- **Common-Cause Failure** – Single root cause affects multiple redundant elements  
- **Cascading Failure** – Failure in one element propagates to others (violates freedom from interference)  

📌 Reliability & Statistical Terms

- **MTBF** – Mean Time Between Failures: average time between two consecutive failures (higher = more reliable)  
- **MTTF** – Mean Time To Failure: expected time until first failure (used for non-repairable items)  
- **MTTR** – Mean Time To Repair: average time required to repair a failed system  
- **FIT** – Failures In Time: number of failures per 10⁹ device-hours (common unit in FMEDA)  
- **Failure Rate (λ)** – Instantaneous failure rate (failures per unit time, usually in FIT)  
- **Hazard Rate** – Time-dependent failure rate (often assumed constant in exponential model)  
- **Probability of Failure on Demand (PFD)** – Probability that safety function fails when needed (IEC 61508)  
- **Probability of Dangerous Failure per Hour (PFH)** – Dangerous failure rate per hour (IEC 61508 SIL)  
- **Residual Failure Rate** – Failure rate remaining after safety mechanisms are applied  
- **Diagnostic Coverage (DC)** – Percentage of dangerous faults detected/controlled by diagnostics  

📌 Fault Tolerance & Redundancy

- **Fail-Safe** – System transitions to a safe state upon fault detection  
- **Fail-Operational** – System continues to provide safe service after single fault  
- **1oo2 / 1oo2D** – 1-out-of-2 architecture (with diagnostics) – detects single fault  
- **2oo2** – 2-out-of-2 voting – both channels must agree (no false negative)  
- **2oo3** – 2-out-of-3 voting – tolerates one faulty channel  
- **Diverse Redundancy** – Using different implementations/algorithms to 🔴 🔴 avoid common-cause faults  
- **Freedom from Interference (FFI)** – No fault in one element affects another (partitioning requirement)  
- **Plausibility Check** – Independent sanity check of sensor/actuator values or outputs  
- **Temporal Monitoring** – Checks timing properties (rate, deadline, sequence)  
- **Value Monitoring** – Checks if output is within expected range/bounds  

📌 Fault Analysis & Diagnostic Techniques

- **FMEA** – Failure Modes and Effects Analysis: bottom-up analysis of component failures  
- **FMEDA** – Failure Modes, Effects and Diagnostic Analysis: quantitative version with coverage & FIT metrics  
- **FTA** – Fault Tree Analysis: top-down deductive analysis of fault combinations  
- **DFA** – Dependent Failure Analysis: identifies common-cause and cascading failures  
- **SPFM** – Single-point fault Metric: coverage of single random hardware faults  
- **LFM** – Latent-fault Metric: coverage of latent/multiple faults  
- **PMHF** – Probabilistic Metric for random Hardware Failures: residual failure rate (FIT)  

⚙️ Decomposition & Independence

- **ASIL Decomposition** – Splitting higher ASIL requirement into lower ASIL sub-parts  
- **ASIL B(D)** – Decomposition achieving effective ASIL D via ASIL B + independent QM  
- **ASIL C(D)** – Decomposition achieving effective ASIL D via ASIL C + independent ASIL B  
- **Independence** – No interference or common cause between decomposed elements  
- **SEooC** – Safety Element out of Context: component developed without full system knowledge  

📌 Other Frequently Used Terms

- **Safety Mechanism** – HW/SW measure that detects or mitigates faults  
- **Watchdog** – Independent timer detecting timing/sequence failures  
- **E2E Protection** – End-to-End communication integrity (CRC + sequence + alive counter)  
- **SOTIF** – Safety Of The Intended Functionality: hazards without system fault (ISO 21448)  
- **ODD** – Operational Design Domain: conditions where system is designed to operate safely  

⭐ This list now includes the most important statistical/reliability terms (MTBF, MTTF, FIT, PFH, etc.) that appear regularly in FMEDA spreadsheets, safety manuals, supplier datasheets, and reliability discussions in automotive functional safety projects.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
