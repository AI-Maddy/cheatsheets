**cheatsheet for Requirements Engineering** (with focus on safety-critical / embedded / automotive / avionics / industrial systems – 2026 perspective).

### 1. Core Concepts & Definitions

| Term / Concept                  | One-line Explanation                                                                 | Typical Standards / Domains                  |
|---------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------|
| **Stakeholder**                 | Anyone affected by or influencing the system (users, regulators, OEMs, maintainers)   | All domains                                  |
| **Requirement**                 | A condition or capability needed by a stakeholder to solve a problem or achieve an objective | ISO 26262, DO-178C, IEC 61508                |
| **Functional Requirement**      | What the system shall do (behavior, output, response)                                | All                                          |
| **Non-Functional Requirement**  | How well the system performs (performance, safety, reliability, security, usability) | Critical in embedded & safety systems        |
| **Safety Requirement**          | Requirement derived from safety goal (prevents/mitigates hazard)                     | ISO 26262 (ASIL), IEC 61508 (SIL), DO-178C   |
| **Derived Requirement**         | Requirement added during design/development (not directly from stakeholder)          | Must be traced & justified (DO-178C)         |
| **Traceability**                | Bidirectional link between requirements, design, code, tests, safety goals           | Mandatory for ASIL B+/DAL B+                 |
| **Verification**                | Did we build the system right? (meets requirements)                                  | Reviews, analysis, testing                   |
| **Validation**                  | Did we build the right system? (satisfies intended use & stakeholder needs)          | System testing, operational scenarios        |

### 2. Requirements Engineering Process (Typical V-Model Flow)

| Phase / Step                     | Main Activities                                                                 | Deliverables / Artifacts                     | Key Standards / Guidelines |
|----------------------------------|---------------------------------------------------------------------------------|----------------------------------------------|----------------------------|
| **Stakeholder Needs**            | Interviews, workshops, use cases, regulatory analysis                           | Stakeholder Needs Document, Use Case Specs   | ISO 15288, INCOSE            |
| **System Requirements**          | Elicit, analyze, prioritize, refine, baseline                                   | System Requirements Specification (SysRS)    | ISO 26262 Part 3, ARP4754A   |
| **Functional Safety Requirements**| Derive from HARA (Hazard Analysis & Risk Assessment)                             | Functional Safety Requirements (FSR)         | ISO 26262 Part 3             |
| **Technical Safety Requirements**| Allocate safety requirements to hardware/software                                | Technical Safety Requirements (TSR)          | ISO 26262 Part 4             |
| **Software Requirements**        | Refine to software level, add derived requirements                              | Software Requirements Specification (SwRS)   | ISO 26262 Part 6, DO-178C    |
| **Requirements Analysis**        | Check completeness, consistency, feasibility, verifiability, unambiguity        | Requirements Review Report                   | DO-178C Table A-2, ASPICE    |
| **Requirements Traceability**    | Trace to safety goals ↔ FSR ↔ TSR ↔ SwRS ↔ design ↔ code ↔ tests                | Traceability Matrix (ReqIF, DOORS, Polarion) | ISO 26262, DO-178C           |
| **Change & Impact Analysis**     | Assess impact of proposed changes on safety & other requirements                | Change Impact Analysis Report                | ASPICE SUP.8, DO-178C        |

### 3. Requirements Quality Attributes (Checklists)

| Attribute               | What it means / Good requirement checklist question                          | Typical Check (ASIL B+/DAL B+) |
|-------------------------|-------------------------------------------------------------------------------|--------------------------------|
| **Correct**             | Accurately reflects stakeholder intent?                                       | Yes                            |
| **Unambiguous**         | Only one interpretation possible?                                             | Yes                            |
| **Complete**            | All necessary conditions stated? No “TBD” or open ends                        | Yes                            |
| **Consistent**          | No contradiction with other requirements?                                     | Yes                            |
| **Verifiable**          | Can be proven true/false by analysis/testing/inspection?                     | Yes (mandatory for ASIL C/D)   |
| **Traceable**           | Linked to parent requirement / safety goal / test?                            | Yes (bidirectional)            |
| **Necessary**           | Needed to meet stakeholder or safety objective?                               | Yes                            |
| **Feasible**            | Can be implemented within cost, time, technology constraints?                 | Yes                            |
| **Atomic**              | One clear, single thought (avoid “and” / “or” in same requirement)            | Yes                            |
| **Quantified**          | Measurable where possible (response time < 100 ms, accuracy ±0.5%, etc.)      | Preferred                       |

### 4. Requirements Types in Safety-Critical Domains

| Requirement Type               | Source / Origin                              | Typical Format / Example                              | Traceability Direction |
|--------------------------------|----------------------------------------------|-------------------------------------------------------|------------------------|
| **Safety Goal**                | HARA (Hazard Analysis & Risk Assessment)     | “Prevent unintended acceleration” (ASIL D)            | Top-level              |
| **Functional Safety Requirement (FSR)** | Derived from Safety Goal                   | “Brake torque shall be applied within 200 ms” (ASIL D) | Safety Goal → FSR      |
| **Technical Safety Requirement (TSR)** | Allocation to HW/SW                         | “Brake ECU shall detect pedal position within 10 ms”  | FSR → TSR              |
| **Software Safety Requirement** | SW-specific refinement                      | “Brake SW shall set fault flag if sensor timeout > 50 ms” | TSR → SwRS             |
| **Software Requirement (non-safety)** | Functional / performance                   | “Display shall refresh at 60 Hz”                      | SysRS → SwRS           |
| **Derived Requirement**        | Added during design/implementation           | “Checksum shall be CRC-32C” (not from stakeholder)    | Must be justified & traced |

### 5. Requirements Engineering Tools (2026 Landscape)

| Tool / Platform               | Strengths / Typical Use Case                          | Domains / Standards Supported | Traceability Strength | Cost / Qualification |
|-------------------------------|-------------------------------------------------------|-------------------------------|-----------------------|----------------------|
| **Polarion**                  | Full ALM, very strong traceability                    | Automotive, medical, railway  | Very high             | High / TQL-2/3       |
| **IBM DOORS / DOORS Next**    | Classic in aerospace & automotive                     | Avionics, automotive, defense | Very high             | High / TQL-1/2       |
| **Jama Connect**              | Modern UI, good collaboration                         | Automotive, medical           | High                  | Medium–High          |
| **Codebeamer**                | Strong ASPICE & ISO 26262 support                     | Automotive                    | High                  | Medium               |
| **ReqIF**                     | Exchange format (tool-independent)                    | All                           | —                     | —                    |
| **Enterprise Architect**      | SysML + requirements modeling                         | Automotive, systems eng       | Medium–High           | Medium               |

### 6. Quick Rules of Thumb (Safety-Critical 2026 Practice)

- **ASIL D / DAL A** → every requirement **must** be verifiable (testable or analyzable)
- **Derived requirements** → must be **explicitly justified** & traced (DO-178C Objective A-2.3 / ISO 26262-6)
- **Traceability matrix** → bidirectional & **complete** (parent ↔ child ↔ test)
- **One requirement = one thought** → avoid “shall do A and B” → split
- **Quantify whenever possible** → “fast” → “response time ≤ 50 ms”
- **ALARP argument** → only allowed when safety target already met (ISO 26262)
- **Change impact analysis** → mandatory for every change in ASIL B+ (ASPICE SUP.8)

This cheatsheet reflects current best practices in requirements engineering for embedded & safety-critical systems.

Good luck with your requirements work!