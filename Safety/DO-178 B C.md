**DO-178B / DO-178C Cheat Sheet**  
(Comparison & Key Concepts – valid for avionics software certification in 2025–2026)

DO-178B (1992) is now **obsolete** for new projects, but still appears in legacy systems.  
DO-178C (2011 + supplements) is the **current standard** required by FAA/EASA for new airborne software.

### 1. Quick Comparison Table – DO-178B vs DO-178C

Aspect                        | DO-178B (1992)                          | DO-178C (2011 + supplements)                     | Practical Impact (2025–2026)
------------------------------|------------------------------------------|--------------------------------------------------|-------------------------------------
**Objective tables**          | 6 tables (A–F)                           | Consolidated into Table A-1 to A-9               | Easier to navigate
**Tool qualification**        | Very strict – almost all tools qualified | TCL (Tool Confidence Level) 1–3                  | Much less painful
**Model-based development**   | Not supported                            | Explicitly supported (DO-331 supplement)         | MBDA / Simulink widely used
**Formal methods**            | Barely mentioned                         | Explicit supplement (DO-333)                     | Used for high-criticality code
**Object code verification**  | Required for Level A                     | More flexible with supplements                   | Less rework if using qualified compilers
**Traceability**              | Required                                 | Stronger emphasis + automation encouraged        | Tools like Polarion / DOORS mandatory
**Supplements**               | None                                     | 4 official: DO-330,331,332,333                   | Critical for modern workflows
**Legacy acceptance**         | Still accepted for changes to old systems| Not accepted for new certification               | Reverse engineering common

### 2. Software Levels (Development Assurance Level – DAL)

Level | Failure Condition Category          | Typical Function Examples                     | Objectives to satisfy
------|--------------------------------------|-----------------------------------------------|-----------------------
**A** | Catastrophic (aircraft loss / fatalities) | Primary flight controls, engine FADEC, autopilot servos | Highest – ~71 objectives
**B** | Hazardous / Severe-Major             | Flight management, display systems, TCAS      | High – ~69 objectives
**C** | Major                                | Weather radar, cabin pressurization           | Medium – ~50 objectives
**D** | Minor                                | Non-critical displays, maintenance functions  | Low – ~30 objectives
**E** | No safety effect                     | Passenger entertainment, cabin lights         | Minimal – traceability only

**Most avionics projects are Level A or B.**

### 3. Key Process Documents (DO-178C)

Document / Activity              | Purpose / When Produced                     | Typical Review / Audit Focus
---------------------------------|---------------------------------------------|--------------------------------
**Plan for Software Aspects of Certification (PSAC)** | Top-level planning document                 | FAA/EASA review early
**Software Development Plan**    | How you will develop (tools, methods, standards) | Consistency with PSAC
**Software Verification Plan**   | How you will verify (reviews, tests, analysis) | Coverage metrics
**Software Configuration Management Plan** | Version control, baselines, problem reporting | Traceability & reproducibility
**Software Quality Assurance Plan** | Independence, audits, non-conformance       | SQA independence
**Software Requirements Standards** | Criteria for writing low-level requirements | Consistency, verifiability
**Software Design Standards**    | How architecture & low-level design is done | Modularity, safety patterns
**Software Code Standards**      | Coding rules (MISRA C subset, CERT-C, etc.) | Static analysis compliance

### 4. Verification & Testing Objectives (Table A-6 / A-7 simplified)

Activity                              | Level A | Level B | Level C | Level D | Notes
--------------------------------------|---------|---------|---------|---------|-------
**Requirements-based testing**        | 100%    | 100%    | 100%    | —       | Normal & robustness cases
**MC/DC coverage**                    | 100%    | —       | —       | —       | Modified Condition/Decision Coverage (Level A only)
**Statement coverage**                | —       | 100%    | 100%    | —       | 
**Decision coverage**                 | —       | 100%    | —       | —       | 
**Data coupling & control coupling**  | 100%    | 100%    | —       | —       | 
**Object code to source traceability**| 100%    | —       | —       | —       | Especially if compiler not qualified
**Low-level requirements coverage**   | 100%    | 100%    | —       | —       | 

### 5. Supplements – Quick Reference (DO-178C ecosystem)

Supplement | Title / Focus                               | When you must reference it
-----------|---------------------------------------------|---------------------------
**DO-330** | Software Tool Qualification Considerations  | Every tool used in development/verification
**DO-331** | Model-Based Development & Verification      | Simulink/Stateflow, SCADE, SysML
**DO-332** | Object-Oriented Technology & Related Techniques | C++, Java (rare in avionics)
**DO-333** | Formal Methods Supplement                   | Model checking, theorem proving (e.g. Astrée, Frama-C, Coq)

### 6. Tool Qualification Levels (DO-330 – much easier than DO-178B)

TCL | Criteria                                    | Typical Tools
----|---------------------------------------------|---------------
**TCL-1** | Output directly used as safety artifact     | Code generator that produces Level A code
**TCL-2** | Output affects development/verification     | Static analyzer, test generator, compiler
**TCL-3** | Support tool – no direct impact             | Most configuration management, requirements tools

**TCL-3 is the most common qualification level in 2025–2026.**

### 7. Quick One-liners (what certification auditors & engineers say)

- “Level A code still needs MC/DC — no way around it.”
- “If you use Simulink, you must follow DO-331.”
- “Compiler is TCL-2 unless you prove it otherwise.”
- “We use Astrée for stack & WCET analysis — helps Level A.”
- “Traceability from high-level requirements to object code is non-negotiable.”
- “Change impact analysis is critical for incremental certification.”
- “SQA must be independent — no exceptions.”

### 8. Modern Reality (2025–2026)

- **Most new avionics** → DO-178C + DO-331 (model-based)
- **Formal methods (DO-333)** → growing for Level A critical code
- **Agile + DO-178C** → possible with strong planning & tool support
- **Toolchain** → VectorCAST, LDRA, Cantata, QAC, Polyspace, SCADE, Simulink Design Verifier, Astrée
- **Certification time** → 18–36 months typical for Level A/B

Good luck with your avionics certification effort!  
The biggest time sinks are usually **MC/DC coverage**, **tool qualification**, **traceability gaps**, and **change impact analysis** — start early with PSAC and tool selection.