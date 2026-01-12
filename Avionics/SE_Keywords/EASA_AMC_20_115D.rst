📘 **EASA AMC 20-115D: European Aviation Safety Authority Guidance** (2026 Edition!)
===================================================================================

**Quick ID:** EASA's acceptable means of compliance for aircraft type certification (European equivalent to FAA Order 8110.49)
**Key Content:** EASA certification procedures, acceptable standards (including DO-178C), compliance demonstration
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—EASA AMC 20-115D governs European certification (same as FAA in US)

---

✈️ **WHAT IS EASA AMC 20-115D?**
================================

**EASA AMC 20-115D** = European Aviation Safety Agency's acceptable means of compliance for software:
  ✅ **Defines** EASA certification approach (how EASA approves aircraft)
  ✅ **Specifies** DO-178C applicability (EASA recognizes DO-178C as acceptable standard)
  ✅ **Describes** certification procedures (EASA review process, approvals)
  ✅ **Governs** EASA-appointed representatives (similar to FAA's DER concept)
  ✅ **Prescribes** certification data requirements (what must be submitted)
  ✅ **Controls** Type Certificate approval (EASA certification authority)

**Authority:** EASA AMC 20-115D = Law for European aircraft certification (you MUST comply for EASA approval)

**Scope:** Applies to ALL aircraft/engine certification projects in Europe and EASA member states

**Relationship to FAA Order 8110.49:**
  • FAA Order 8110.49: US certification requirements
  • EASA AMC 20-115D: European certification requirements
  • Often aligned (both accept DO-178C)
  • Sometimes different (different emphasis, different interpretation)
  • Both required for global aircraft certification (e.g., A320 certified by BOTH FAA and EASA)

---

📋 **EASA CERTIFICATION FRAMEWORK**
==================================

**EASA Part-21 (Certification Procedures)**
  🎯 EASA's overall certification regulation
  🎯 Defines Type Certificate (TC), Supplemental TC (STC), Approval processes
  🎯 Similar to FAA's 14 CFR Part 21
  🎯 Specifies EASA's approval authority and decision process

**EASA Part-23 (Small Aircraft Design Standards)**
  🎯 Design standards for small aircraft (European version)
  🎯 References acceptable means of compliance (AMCs)
  🎯 References DO-178C for software compliance
  🎯 Example: "Software shall comply with DO-178C or equivalent"

**EASA Part-25 (Large Aircraft Design Standards)**
  🎯 Design standards for large commercial aircraft (European version)
  🎯 Specifies more rigorous requirements (DAL A/B more common)
  🎯 Often requires DO-178C for critical functions
  🎯 Example: "Flight control software shall comply with DO-178C Level A (MC/DC 100%)"

**EASA AMC (Acceptable Means of Compliance)**
  🎯 Advisory guidance on how to comply with regulations
  🎯 AMC 20-115D: Software guidance (references DO-178C)
  🎯 Similar to FAA's Advisory Circulars (ACs)
  🎯 Not mandatory; but widely followed industry practice

---

📚 **EASA AMC 20-115D vs. FAA ORDER 8110.49 (Comparison)**
=========================================================

| Aspect | EASA AMC 20-115D | FAA Order 8110.49 |
|:-------|:---|:---|
| **Jurisdiction** | European Aviation Safety Agency | Federal Aviation Administration (US) |
| **Geographic scope** | Europe, EASA member states | United States |
| **Applicability** | Required for European Type Certificate | Required for US Type Certificate |
| **Software standard** | DO-178C acceptable means of compliance | DO-178C acceptable means of compliance |
| **DAL mapping** | DAL A/B/C/D/E → Design Assurance Level | DAL A/B/C/D/E → Design Assurance Level |
| **Coverage targets** | MC/DC per DAL (same as FAA) | MC/DC per DAL (same as FAA) |
| **DER equivalent** | EASA Appraisal Manager, Competent Authority | FAA's Designated Engineering Representative |
| **Certification gates** | Similar to FAA (planning, design, validation) | ICC, PDR, CDR, CRR milestones |
| **Certification data** | Type Certificate dossier submitted to EASA | Certification file submitted to FAA |
| **Type Certificate** | European Type Certificate (EASA) | Type Certificate (FAA) |
| **Differences** | May require additional EASA-specific items | May require additional FAA-specific items |

**Key Principle:** Both EASA and FAA accept DO-178C; often aligned but sometimes different emphasis.

---

🔄 **EASA CERTIFICATION WORKFLOW (per AMC 20-115D)**
==================================================

**Phase 1: Certification Planning (Month 1–3)**
  📋 Activity: Review EASA Part-23/25 and AMC 20-115D requirements
  📋 Decision: Determine applicable EASA regulations
  📋 Decision: Select means of compliance (DO-178C per AMC 20-115D)
  📋 Meeting: Certification Kick-off Meeting with EASA Competent Authority
  📋 Approval: EASA issues certification specification (certification plan approved)

**Phase 2: Design & Development (Month 3–12)**
  📋 Activity: Develop per EASA AMC 20-115D procedures
  📋 Review: Design review points (similar to FAA's PDR, CDR)
  📋 Authority Oversight: EASA Appraisal Manager monitors (similar to FAA DER)
  📋 Milestones: Progress reviewed at EASA-specified intervals

**Phase 3: Verification & Validation (Month 12–18)**
  📋 Activity: Verify compliance per EASA certification requirements
  📋 Testing: All testing documented per EASA data requirements (similar to FAA)
  📋 Evidence: Objective evidence collected per EASA specifications (similar to FAA)

**Phase 4: Certification Approval (Month 18–24)**
  📋 Review: EASA technical team reviews certification dossier
  📋 Submission: Submit Type Certificate dossier to EASA (similar to FAA submission)
  📋 Approval: EASA issues European Type Certificate (EASA certification approval)

---

📄 **EASA AMC 20-115D KEY REQUIREMENTS**
=======================================

**AMC 1: Software Development Assurance**
  🎯 Applicability of DO-178C:
    • DAL A (Catastrophic): DO-178C Level A (MC/DC 100%, most rigorous)
    • DAL B (Hazardous): DO-178C Level B (MC/DC or Decision 100%)
    • DAL C (Major): DO-178C Level C (Decision 100%, moderate rigor)
    • DAL D (Minor): DO-178C Level D (Statement coverage, less rigor)
    • DAL E (No safety impact): DO-178C not applicable (standard development acceptable)

  🎯 **Coverage targets identical to FAA requirements:**
    • DAL A: MC/DC 100%, Decision 100%, Statement 100%
    • DAL B: MC/DC 100% or Decision 100%, Statement 100%
    • DAL C: Decision 100%, Statement 100%
    • DAL D: Statement 100%

**AMC 2: Tool Qualification**
  🎯 Compilers, code generators, coverage analyzers must be qualified
  🎯 Tool qualification approach similar to FAA (testing, documentation)
  🎯 Tool version must be locked (no mid-project upgrades)
  🎯 Configuration management applies to tools

**AMC 3: Model-Based Development (MBD)**
  🎯 EASA accepts graphical modeling (Simulink, SCADE)
  🎯 Code generation from models acceptable (with tool qualification)
  🎯 Model verification required (same rigor as code verification)
  🎯 Traceability from requirements through model to code required

**AMC 4: Formal Methods**
  🎯 EASA accepts formal methods (Coq, Isabelle, TLA+) as evidence
  🎯 Mathematical proof of correctness acceptable alternative to exhaustive testing
  🎯 Formal methods guidance included in AMC 20-115D

**AMC 5: Configuration Management**
  🎯 Requirements traceability mandatory
  🎯 Baselines (requirements, design, code) required
  🎯 Change control process required
  🎯 Audit trail documentation required

**AMC 6: Independent Verification**
  🎯 Independence requirements by DAL (similar to FAA)
  🎯 DAL A: Independent testers (separate from development)
  🎯 DAL B/C: Independence required (different from development team)
  🎯 DAL D/E: Independence not required (but often implemented)

---

📊 **EASA vs. FAA DUAL CERTIFICATION**
====================================

**Projects Requiring Both EASA & FAA Approval (Global Aircraft)**

| Project | Scope | EASA Requirement | FAA Requirement |
|:--------|:------|:---|:---|
| Airbus A350 Flight Control | Global commercial aircraft | EASA Type Certificate | FAA Type Certificate |
| Typical requirement | Both required (need both approvals) | Comply with AMC 20-115D | Comply with FAA Order 8110.49 |
| Standard | Both require DO-178C | DAL A = Level A (MC/DC 100%) | DAL A = Level A (MC/DC 100%) |
| Difference | EASA emphasis: AMC 20-115D | FAA emphasis: FAA Order 8110.49 |
| Approval | European Type Certificate (EASA) | Type Certificate (FAA) |

**Dual Certification Strategy:**
  1️⃣ Review BOTH AMC 20-115D and FAA Order 8110.49 (Month 1)
  2️⃣ Develop strategy that satisfies BOTH requirements
  3️⃣ Often: Approach that satisfies one authority often satisfies the other (both accept DO-178C)
  4️⃣ EASA and FAA may have different emphasis or interpretation (accommodate both)
  5️⃣ Submit to both authorities (EASA first or parallel, FAA after/parallel)
  6️⃣ Get both Type Certificates

---

⚡ **EASA AMC 20-115D BEST PRACTICES**
====================================

✅ **Tip 1: Review EASA AMC 20-115D BEFORE project starts (if EASA certification required)**
  ❌ Mistake: "Develop for FAA; realize EASA has different requirements late"
  ✅ Right: "Review EASA AMC 20-115D Month 1; align with EASA expectations"
  Impact: Avoid approach conflicts; satisfy both authorities from start

✅ **Tip 2: Align approach with BOTH FAA and EASA early (if dual certification needed)**
  ❌ Mistake: "Certify with FAA first; try EASA after; find conflicts"
  ✅ Right: "Plan approach satisfying both; develop once; submit both"
  Impact: Parallel dual certification; time-efficient

✅ **Tip 3: Use DO-178C as common standard (both EASA and FAA accept)**
  ❌ Mistake: "Different approach for EASA vs. FAA; duplicate work"
  ✅ Right: "Single DO-178C approach; satisfies both authorities"
  Impact: One development, both certifications

✅ **Tip 4: Understand EASA's emphasis vs. FAA's emphasis (may differ)**
  ❌ Mistake: "Copy FAA approach directly; EASA interprets differently"
  ✅ Right: "Understand both requirements; accommodate different emphasis"
  Impact: Smooth certification with both authorities

✅ **Tip 5: Dual certification: Plan parallel submission (not sequential)**
  ❌ Mistake: "Certify FAA first, EASA after; takes 2x time"
  ✅ Right: "Plan parallel certification (same data, both authorities)"
  Impact: Faster global certification

---

⚠️ **COMMON EASA AMC 20-115D MISTAKES**
=====================================

❌ **Mistake 1: Ignore EASA requirements (assume FAA approval sufficient)**
  Problem: "Develop for FAA; later realize EASA certification also needed"
  Impact: Rework required; EASA certification delayed
  Fix: Confirm certification scope early (FAA only, EASA only, or both?)

❌ **Mistake 2: Different approach for EASA vs. FAA (unnecessary duplication)**
  Problem: "FAA wants X; EASA wants Y; do both (wasteful)"
  Impact: Double work; schedule extended; cost increased
  Fix: Use DO-178C common approach (satisfies both authorities)

❌ **Mistake 3: Submit to FAA first; EASA later (sequential, not parallel)**
  Problem: "Get FAA approval Month 24; submit EASA Month 25; approval Month 30"
  Impact: EASA certification takes 6+ months after FAA (unnecessary delay)
  Fix: Plan parallel submission (same data, both authorities)

❌ **Mistake 4: EASA Appraisal Manager not involved early (similar to DER)**
  Problem: "Don't involve EASA oversight until late-project"
  Impact: EASA finds issues late; rework required
  Fix: EASA Appraisal Manager involved Month 1 (parallel to FAA DER)

❌ **Mistake 5: Different data for EASA vs. FAA (instead of common data)**
  Problem: "Compile different data packages for EASA vs. FAA"
  Impact: Inconsistencies; both authorities confused
  Fix: Single data package acceptable to both (DO-178C common standard)

---

🎓 **LEARNING PATH: EASA AMC 20-115D**
====================================

**Week 1: EASA Certification Framework**
  📖 Read: EASA Part-21 (certification procedures), EASA Part-23/25 (design standards)
  📖 Study: EASA certification authority, Type Certificate process, Appraisal Manager role
  🎯 Goal: Understand EASA's certification approach (parallel to FAA)

**Week 2: AMC 20-115D Guidance**
  📖 Read: EASA AMC 20-115D (software guidance, DO-178C applicability)
  📖 Study: Coverage targets per DAL (same as FAA), DO-178C acceptance
  🎯 Goal: Understand EASA's software requirements and acceptable means of compliance

**Week 3: Dual Certification Strategy**
  💻 Study: Dual certification projects (FAA + EASA Type Certificates)
  💻 Practice: Outline certification strategy for aircraft requiring both approvals
  🎯 Goal: Confidence in dual certification planning and execution

---

✨ **BOTTOM LINE**
=================

**EASA AMC 20-115D = European certification guidance (equivalent to FAA Order 8110.49)**

✅ Reviewed early (Month 1, if EASA certification required)
✅ DO-178C acceptable standard (same coverage targets as FAA)
✅ Appraisal Manager involved (parallel to FAA DER)
✅ Dual certification planned (if both FAA and EASA approvals needed)
✅ Parallel submission (same data, both authorities)
✅ Type Certificate issued by both authorities

**Remember:** 📘 **EASA AMC 20-115D = "The law for European certification; same DO-178C standard as FAA!"** ✈️

---

**Last updated:** 2026-01-12 | **EASA AMC 20-115D**

**Key Takeaway:** 💡 **Both EASA and FAA accept DO-178C! Use common standard = efficient dual certification!** 🛡️
