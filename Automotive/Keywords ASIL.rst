
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **ASIL Keywords List with One-Line Explanations**  
(ISO 26262 Automotive Functional Safety – most relevant terms used in 2025–2026 ADAS/AD projects)

📌 Core ASIL Levels

- **QM** – Quality Management: no specific safety requirements (normal automotive quality level)  
- **ASIL A** – Automotive Safety Integrity Level A: lowest safety integrity – very low risk of harm  
- **ASIL B** – Automotive Safety Integrity Level B: most common in series ADAS (AEB, LKA, ACC)  
- **ASIL C** – Automotive Safety Integrity Level C: high integrity – used in some actuation/monitoring paths  
⭐ - **ASIL D** – Automotive Safety Integrity Level D: highest integrity – required for critical braking, steering, fallback in L3+  

⭐ 📌 Key Metrics & Targets

- **SPFM** – Single-point fault Metric: measures coverage of single random hardware faults (≥90% ASIL B, ≥99% ASIL D)  
- **LFM** – Latent-fault Metric: coverage of latent (multiple) faults (≥60% ASIL B, ≥90% ASIL D)  
- **PMHF** – Probabilistic Metric for random Hardware Failures: residual failure rate target (FIT rate)  
- **Diagnostic Coverage** – Percentage of faults detected by safety mechanisms (low / medium / high / very high)  

⚙️ Decomposition & Independence

- **ASIL Decomposition** – Splitting a higher ASIL requirement into lower ASIL sub-parts (e.g. ASIL D → ASIL B(D))  
- **ASIL B(D)** – Decomposition result where the effective safety equals ASIL D via ASIL B + independent QM part  
- **ASIL C(D)** – Decomposition giving effective ASIL D via ASIL C + independent ASIL B part  
- **Independence** – Freedom from interference between elements (crucial for decomposition to work)  
- **Freedom from Interference (FFI)** – No cascading failures between mixed-ASIL software/hardware elements  

📌 Architectural & Technical Terms

- **Safety Element out of Context (SEooC)** – Component developed without knowing the full system context (common for sensors/SoCs)  
- **Safety Mechanism** – Hardware or software measure to detect/control faults (watchdog, lockstep, ECC, E2E)  
- **Lockstep** – Dual-core execution with comparison to detect faults (widely used in ASIL B–D MCUs/SoCs)  
- **Diverse Redundancy** – Using different implementations to 🔴 🔴 avoid common-cause failures  
- **1oo2D** – 1-out-of-2 with diagnostics (typical for fail-operational actuation paths)  
- **E2E Protection** – End-to-End communication protection (CRC + sequence counter + alive counter)  
- **Safety Manual** – Supplier document describing assumed safety requirements and usage constraints  

⚙️ Process & Documentation

- **HARA** – Hazard Analysis and Risk Assessment: identifies hazards, ASILs and safety goals  
- **Functional Safety Concept** – High-level safety requirements allocation to system elements  
- **Technical Safety Concept** – Detailed hardware/software architecture fulfilling FSC  
- **FMEA / FMEDA** – Failure Modes Effects (and Diagnostic) Analysis: fault injection & coverage calculation  
- **Safety Case** – Argument + evidence that safety requirements are fulfilled  
- **Confirmation Measures** – Independent reviews (confirmation reviews, audits, assessments)  
- **Tool Confidence Level (TCL)** – Qualification level of development tools (TCL1–TCL3)  

📌 Related/Overlapping Standards

- **SOTIF** – Safety Of The Intended Functionality (ISO 21448): addresses hazards without system failure  
- **ISO 21434** – Road vehicle cybersecurity engineering (complements ISO 26262)  
- **Fail-Operational** – System continues safe operation after single failure (required for L3+)  
- **Fail-Safe** – System goes to safe state after failure (typical L2)  

This list covers the ~40 most frequently used ASIL-related terms in automotive safety meetings, requirements specs, supplier discussions, and safety assessments in 2026.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
