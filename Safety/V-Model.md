**V-Model Cheat Sheet for Safety-Critical Systems**  
(oriented toward ISO 26262, DO-178C, IEC 61508, IEC 62304, and similar standards in automotive, avionics, rail, medical, and industrial domains – 2025–2026 practice)

### 1. Core Idea of the V-Model in Safety-Critical Context

```
                System Requirements
                       ↓
             System Architectural Design
                       ↓
           Hardware & Software Requirements
                       ↓
             Hardware & Software Design
                       ↓
         Implementation (HW / SW coding / synthesis)
                       ↓
                       ┼───────────────────────────────
                       │                               │
             Integration & Unit Testing              Verification
                       │                               │
          Software / Hardware Integration Testing    Validation
                       │                               │
                 System Integration Testing          Confirmation Measures
                       │                               │
                  System Validation & Testing        Safety Case / Assessment
                       ↓
                 Acceptance & Field Operation
```

**Left side** = **decomposition** (specification & design – “what” & “how”)  
**Right side** = **integration & verification/validation** (testing & proving correctness)  
**Crossing point** = Implementation (code / hardware)

### 2. V-Model Phases with Safety-Critical Emphasis

Phase (Left → Right)                     | Key Activities in Safety-Critical Systems                          | Typical Standards Reference          | Main Artifacts / Deliverables
------------------------------------------|---------------------------------------------------------------------|--------------------------------------|--------------------------------
**Item Definition / Concept**             | Hazard Analysis & Risk Assessment (HARA), safety goals              | ISO 26262 Part 3, IEC 61508-1        | Item definition, safety goals, ASIL/SIL
**System Requirements**                   | Functional + safety requirements, ASIL allocation                   | ISO 26262-4, DO-178C Table A-2       | System requirements spec
**System Architectural Design**           | Partitioning, freedom from interference, safety mechanisms         | ISO 26262-4, DO-178C A-4             | Technical safety concept, architecture
**Hardware / Software Requirements**      | Detailed reqs + traceability to safety goals                        | ISO 26262-5/6, DO-178C A-2/A-3       | HW/SW requirements spec
**HW / SW Architectural Design**          | Detailed design, fault injection targets, diversity                | ISO 26262-5/6, DO-178C A-4           | Design description, FMEDA
**Implementation**                        | Coding / RTL / synthesis with strict standards (MISRA, CERT-C)      | ISO 26262-6/8, DO-178C A-5           | Source code, binaries, HDL
**Unit / Module Verification**            | Unit testing + static analysis + reviews + coverage                | ISO 26262-6 Table 10–12, DO-178C A-6 | Unit test cases/results, coverage report
**Integration & Integration Testing**     | HW/SW integration, interface testing, fault injection              | ISO 26262-6/4, DO-178C A-5/A-7       | Integration test plan/results
**System Integration & Testing**          | Full system testing, HIL, environmental testing                    | ISO 26262-4, DO-178C A-7             | System test cases/results
**Validation**                            | Validation against safety goals & operational scenarios            | ISO 26262-4, DO-178C A-8             | Validation report
**Verification of Verification**          | Independence checks, coverage closure, traceability                | ISO 26262-8, DO-178C A-9             | Verification report
**Confirmation Measures**                 | Independent safety assessment, audits, reviews                     | ISO 26262-8, DO-178C PSAC/SQAP       | Safety assessment report
**Safety Case**                           | Final argument + evidence package                                  | All standards                        | Safety case / certification dossier

### 3. Quick Reference – Verification & Testing Intensity by Safety Level

Level (ISO 26262 / IEC 61508 / DO-178C) | Unit Testing | Integration Testing | MC/DC Coverage | Independence of Verification
----------------------------------------|--------------|----------------------|----------------|------------------------------
**ASIL A / SIL 1 / Level D**            | Recommended  | Recommended          | —              | Low
**ASIL B / SIL 2 / Level C**            | Highly rec.  | Highly rec.          | —              | Medium
**ASIL C / SIL 3 / Level B**            | Required     | Required             | Decision       | High
**ASIL D / SIL 4 / Level A**            | Required     | Required             | 100% MC/DC     | Very high (independent)

### 4. Most Common Tools & Techniques in Safety-Critical V-Model (2025–2026)

Activity                              | Common Tools / Methods
--------------------------------------|-------------------------
Requirements management & traceability | Polarion, DOORS, Jama, Codebeamer
Model-based development               | Simulink + Embedded Coder, SCADE, QGen
Static analysis & MISRA compliance    | Polyspace, QAC, PC-lint, Coverity, Astrée
Unit & integration testing            | VectorCAST, LDRA, Cantata, RTRT
Model coverage                        | Simulink Coverage, SCADE Suite Verifier
Code coverage                         | gcov/lcov (with qualification), VectorCAST
Fault injection / FMEA/FMEDA          | medini analyze, Ansys medini, Exida
Simulation (MIL/SIL/HIL)              | dSPACE, NI VeriStand, Vector VT System
Formal methods                        | Simulink Design Verifier (Prover), Astrée, Frama-C
Configuration & change management     | Git + Polarion / Helix ALM

### 5. Quick One-liners (what safety engineers actually say)

- “Left side defines what must be safe — right side proves it is.”
- “No traceability gap between safety goal → requirement → test → result.”
- “For ASIL D / Level A you need 100% MC/DC — no shortcuts.”
- “Verification must be at least as independent as the ASIL requires.”
- “Model-based? Then DO-331 / MB.2 workflow is mandatory.”
- “Safety case is not a document — it’s the living argument backed by evidence.”
- “Every change requires impact analysis — regression testing is non-negotiable.”

### 6. Modern Reality (2025–2026)

- Most projects use **hybrid V-Model + agile elements** (sprints within phases)
- **Model-based development** (DO-331) is dominant for control algorithms
- **Traceability automation** (requirements ↔ model ↔ code ↔ tests) is critical
- **Formal methods** are increasingly used for Level A / ASIL D kernels
- **Certification time** for Level A / ASIL D systems: 18–48 months typical

Good luck applying the V-Model in your safety-critical project!  
The biggest killers are usually **missing traceability**, **incomplete coverage**, **non-independent verification**, and **poor change impact analysis** — plan these rigorously from the beginning.