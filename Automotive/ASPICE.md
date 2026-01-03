**Automotive SPICE (ASPICE) Cheat Sheet**  
(current as of ASPICE 4.0 – 2023 release, widely used in 2025–2026 automotive projects)

### 1. ASPICE Basics

- **Full name**: Automotive Software Process Improvement and Capability dEtermination  
- **Current version** (2025–2026): **ASPICE 4.0** (released Nov 2023)  
- **Purpose**: Process capability & maturity assessment for automotive software & system development  
- **Sponsors / Owners**: VDA QMC, intacs (international assessor community)  
- **Main domains covered**: System Engineering, Software Engineering, Hardware Engineering, Management, Support, Reuse  
- **Most assessed PAMs** (Process Assessment Models):  
  - **SWE** (Software Engineering) → most projects  
  - **SYS** (System Engineering) → for domain controllers / ADAS  
  - **HWE** (Hardware Engineering) → ECU hardware  
  - **MAN** (Management) → Project & Risk Management  
  - **SUP** (Supporting Processes) → Configuration, Change, Problem Resolution  

### 2. Capability Levels (CL) – Quick Overview

Level | Name                        | Meaning / What it proves                              | Typical Customer Expectation (OEMs 2025–2026)
------|-----------------------------|-------------------------------------------------------|-----------------------------------------------
**0** | Incomplete                  | Process not performed or does not achieve purpose     | Unacceptable
**1** | Performed                   | All base practices (BPs) performed                    | Minimum for many Tier-2 suppliers
**2** | Managed                     | Process is planned, monitored, adjusted               | Most common requirement (BMW, VW, Stellantis)
**3** | Established                 | Process is standardized across organization           | Increasingly required (especially ADAS Tier-1)
**4** | Predictable                 | Process is quantitatively managed & predictable       | Rare – high-end projects only
**5** | Optimizing                  | Continuous process improvement from data & innovation | Extremely rare

**Most OEMs demand CL2 (sometimes CL3) on SWE/SYS + MAN.3 + SUP processes.**

### 3. Key Process Areas (Most Frequently Assessed in 2025–2026)

Process ID | Name                              | Most Painful / Important Base Practices (BPs)
-----------|-----------------------------------|----------------------------------------------
**MAN.3**  | Project Management                | Planning, estimation, monitoring, risk mgmt, deviation handling
**SWE.1**  | Software Requirements Analysis    | Traceability to system reqs, consistency, feasibility
**SWE.2**  | Software Architectural Design     | Detailed design, interfaces, allocation to SW units
**SWE.3**  | Software Detailed Design & Unit Construction | Detailed design, coding standards, unit test prep
**SWE.4**  | Software Unit Verification        | Unit testing, static analysis, coverage
**SWE.5**  | Software Integration & Integration Test | Integration strategy, interface testing
**SWE.6**  | Software Qualification Test       | Requirements-based system-level testing
**SYS.2**  | System Requirements Analysis      | Traceability, consistency, feasibility
**SYS.3**  | System Architectural Design       | HW/SW allocation, partitioning
**SUP.1**  | Quality Assurance                 | Independence, audits, non-conformance management
**SUP.8**  | Configuration Management          | Baselines, versioning, release control
**SUP.10** | Change Request Management         | Impact analysis, traceability of changes

### 4. Rating & Compliance Quick Reference (ASPICE 4.0)

Rating | Meaning                                      | Typical Finding / Consequence
-------|----------------------------------------------|--------------------------------
**Fully Achieved (FA)** | ≥ 86% achievement                            | Green – good
**Largely Achieved (LA)** | 51–85%                                       | Yellow – acceptable but improvement needed
**Partially Achieved (PA)** | 16–50%                                       | Orange – major finding
**Not Achieved (NA)** | 0–15%                                        | Red – serious non-conformance
**Not Rated (NR)** | Process not in scope or not assessed         | —

**Most OEMs require no “NA” or “PA” in key processes (SWE.1–6, MAN.3, SUP.1/8/10).**

### 5. ASPICE vs Other Standards – Quick Mapping (2025–2026)

Standard / Model      | Typical Mapping / Overlap with ASPICE
----------------------|----------------------------------------
**ISO 26262**         | Functional safety (ASIL) → orthogonal but complementary  
**IATF 16949**        | Quality management system → ASPICE focuses on engineering processes
**CMMI**              | Capability Maturity Model → ASPICE is more automotive-specific
**DO-178C**           | Avionics → much stricter coverage & independence
**AUTOSAR**           | Classic / Adaptive → ASPICE assesses processes around AUTOSAR usage

### 6. Most Common Findings / Pain Points (2025–2026 assessments)

1. Weak **traceability** (requirements ↔ design ↔ test ↔ code)  
2. Missing or poor **impact analysis** on change requests  
3. Insufficient **unit test coverage** or justification  
4. **No independence** in verification / quality assurance  
5. **Inconsistent estimation & risk management** in MAN.3  
6. Poor **configuration & baseline management** (no reproducible builds)  
7. Missing **deviation handling** when plans are not followed

### 7. Quick One-liners (what assessors & project managers say)

- “ASPICE is about **process discipline** – not about the product.”
- “No traceability = automatic PA or NA.”
- “If you cannot show how a requirement was tested, you fail SWE.6.”
- “Change without impact analysis is a classic SUP.10 finding.”
- “CL2 means managed – not perfect. But you must close the gaps.”
- “OEMs are pushing CL3 for ADAS – get ready for more standardization.”
- “Static analysis + unit tests are not optional for SWE.4 anymore.”

### 8. Modern Reality (2025–2026)

- **CL2** is the baseline for most Tier-1 / Tier-2 suppliers  
- **CL3** increasingly required for ADAS, domain controllers, high-voltage BMS  
- **Polarion / Codebeamer / Jira + Confluence** are dominant for traceability  
- **VectorCAST / LDRA / Cantata** for unit & integration testing  
- **Git + Jenkins / GitLab CI** for reproducible builds & configuration  
- **ASPICE 4.0** brought better alignment with ISO 26262 & more explicit hardware support

Good luck with your ASPICE assessment!  
The secret to passing: **strong bidirectional traceability**, **documented deviations**, **independent QA**, and **reproducible builds** — start preparing these early.