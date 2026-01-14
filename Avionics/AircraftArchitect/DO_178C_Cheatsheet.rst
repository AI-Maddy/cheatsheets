✈️ **DO-178C (ED-12C) — Software Certification Cheatsheet**
══════════════════════════════════════════════════════════

**Standard:** Software Considerations in Airborne Systems and Equipment Certification  
**Authority:** RTCA/EUROCAE  
**Version:** DO-178C (2011) replaces DO-178B (1992)  
**Application:** Commercial and military aircraft software certification

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **WHAT IS DO-178C?**
───────────────────────

DO-178C is the **primary standard** for developing and certifying airborne software. 
It defines objectives and activities for software development based on the criticality 
of the system (Design Assurance Level).

**Key Principles:**

✅ **Objective-based:** Focuses on what must be achieved, not how  
✅ **Scalable rigor:** More critical = more objectives + evidence  
✅ **Traceability:** Requirements → Design → Code → Tests  
✅ **Independence:** Some activities require independent verification  
✅ **Configuration management:** Strict control of artifacts

════════════════════════════════════════════════════════════════════

🏅 **DESIGN ASSURANCE LEVELS (DAL)**
────────────────────────────────────

**Criticality Classification:**

| DAL | Failure Condition | Effect | Examples | PFH Target |
|:----|:------------------|:-------|:---------|:-----------|
| **A** | Catastrophic | Multiple fatalities, aircraft loss | Flight control, FADEC | < 10⁻⁹ |
| **B** | Hazardous | Large reduction in safety margin | Navigation, autopilot | < 10⁻⁷ |
| **C** | Major | Significant reduction in safety | Communications | < 10⁻⁵ |
| **D** | Minor | Slight reduction in safety | Passenger info | < 10⁻³ |
| **E** | No Safety Effect | No impact on safety | Entertainment | N/A |

**Memorization Trick:** **"A-B-C-D-E = Always Be Careful During Execution"**

════════════════════════════════════════════════════════════════════

📊 **OBJECTIVES BY DAL LEVEL**
──────────────────────────────

**High-Level Requirements (HLR):**

| Objective | DAL A | DAL B | DAL C | DAL D | DAL E |
|:----------|:------|:------|:------|:------|:------|
| Derived from system reqs | Yes | Yes | Yes | Yes | Optional |
| Traceable to system reqs | Yes | Yes | Yes | Yes | Optional |
| Verifiable | Yes | Yes | Yes | Yes | Optional |
| Consistent | Yes | Yes | Yes | Yes | Optional |
| Algorithm accuracy | Yes | Yes | Yes | Yes | N/A |

**Low-Level Requirements (LLR):**

| Objective | DAL A | DAL B | DAL C | DAL D | DAL E |
|:----------|:------|:------|:------|:------|:------|
| Compliant with HLR | Yes | Yes | Yes | Yes | N/A |
| Verifiable | Yes | Yes | Yes | Yes | N/A |
| Traceable to HLR | Yes | Yes | Yes | Yes | N/A |
| Algorithm accuracy | Yes | Yes | Yes | Optional | N/A |

**Source Code:**

| Objective | DAL A | DAL B | DAL C | DAL D | DAL E |
|:----------|:------|:------|:------|:------|:------|
| Compliant with LLR | Yes | Yes | Yes | Yes | N/A |
| Traceable to LLR | Yes | Yes | Yes | Yes | N/A |
| Verifiable | Yes | Yes | Yes | Yes | N/A |
| Accurate & consistent | Yes | Yes | Yes | Yes | N/A |

**Testing:**

| Objective | DAL A | DAL B | DAL C | DAL D | DAL E |
|:----------|:------|:------|:------|:------|:------|
| Requirements-based | Yes | Yes | Yes | Yes | Optional |
| MC/DC coverage | Yes | Yes | No | No | No |
| Decision coverage | N/A | N/A | Yes | No | No |
| Statement coverage | N/A | N/A | N/A | Yes | No |

════════════════════════════════════════════════════════════════════

🔑 **KEY CONCEPTS**
───────────────────

**📝 Traceability:**

```
System Requirements
      ↓ (allocate)
High-Level Requirements (HLR)
      ↓ (refine)
Low-Level Requirements (LLR)
      ↓ (implement)
Source Code
      ↓ (verify)
Test Cases
      ↓ (results)
Test Evidence
```

**✅ Coverage Metrics:**

🎯 **MC/DC (Modified Condition/Decision Coverage):**
- Required for DAL A & B
- Each condition independently affects decision outcome
- Most rigorous coverage metric

🎯 **Decision Coverage:**
- Required for DAL C
- Every decision outcome (true/false) executed once

🎯 **Statement Coverage:**
- Required for DAL D
- Every executable statement executed once

**🔍 Verification vs. Validation:**

| Activity | Focus | Question |
|:---------|:------|:---------|
| **Verification** | Process correctness | "Are we building it right?" |
| **Validation** | Product correctness | "Are we building the right thing?" |

════════════════════════════════════════════════════════════════════

🛠️ **DEVELOPMENT PROCESSES**
─────────────────────────────

**Planning Process:**

✅ Plan for Software Aspects of Certification (PSAC)  
✅ Software Development Plan (SDP)  
✅ Software Verification Plan (SVP)  
✅ Software Configuration Management Plan (SCMP)  
✅ Software Quality Assurance Plan (SQAP)

**Development Process:**

1. **Requirements:** Capture HLR from system requirements
2. **Design:** Create architecture and LLR
3. **Coding:** Implement LLR in source code
4. **Integration:** Combine components

**Verification Process:**

1. **Reviews & Analysis:** Requirements review, design review, code review
2. **Testing:** Unit tests, integration tests, system tests
3. **Coverage Analysis:** Structural coverage (statement/branch/MC/DC)

**Configuration Management:**

✅ Baseline management  
✅ Change control  
✅ Problem reporting  
✅ Archive & retrieval

**Quality Assurance:**

✅ Process monitoring  
✅ Tool qualification  
✅ Conformity review  
✅ Audit preparation

════════════════════════════════════════════════════════════════════

📂 **REQUIRED DELIVERABLES**
────────────────────────────

**Planning Data:**

📄 PSAC — Plan for Software Aspects of Certification  
📄 SDP — Software Development Plan  
📄 SVP — Software Verification Plan  
📄 SCMP — Software Configuration Management Plan  
📄 SQAP — Software Quality Assurance Plan

**Development Data:**

📄 SRS — Software Requirements Standards  
📄 SDS — Software Design Standards  
📄 SCS — Software Code Standards

**Verification Data:**

📄 SVR — Software Verification Results  
📄 SECI — Software Executable Object Code  
📄 SCR — Software Configuration Index  
📄 SVP — Software Verification Plan

**Lifecycle Data:**

📄 SAS — Software Accomplishment Summary (key document!)  
📄 SCMR — Software Configuration Management Records  
📄 SQAR — Software Quality Assurance Records  
📄 PSACR — Plan for Software Aspects of Certification Review

════════════════════════════════════════════════════════════════════

🔧 **TOOL QUALIFICATION**
─────────────────────────

**When is tool qualification required?**

Tools must be qualified if they:
1. **Eliminate verification activities** (e.g., auto-code generators)
2. **Create outputs that can't be verified** (e.g., compilers, linkers)

**Tool Qualification Levels:**

| TQL | Definition | Verification Approach |
|:----|:-----------|:----------------------|
| **TQL-1** | Tool output cannot be verified | Full qualification required |
| **TQL-2** | Tool eliminates verification | Partial qualification |
| **TQL-3** | Tool failure detected | Minimal qualification |
| **TQL-4** | Tool failure cannot affect output | No qualification |
| **TQL-5** | Tool only used for development | No qualification |

════════════════════════════════════════════════════════════════════

⚠️ **COMMON PITFALLS**
──────────────────────

**❌ Late Planning:**
- Problem: Starting DO-178C compliance after development
- Solution: Create plans BEFORE development starts

**❌ Incomplete Traceability:**
- Problem: Requirements not traced to tests
- Solution: Maintain bidirectional traceability throughout

**❌ Insufficient Independence:**
- Problem: Same person developing and verifying
- Solution: Separate verification team for DAL A/B

**❌ Poor Configuration Management:**
- Problem: Lost track of which code version was tested
- Solution: Rigorous CM from day one

**❌ Inadequate Coverage:**
- Problem: MC/DC not achieved for DAL A/B
- Solution: Design for testability early

════════════════════════════════════════════════════════════════════

✨ **QUICK REFERENCE CARD**
───────────────────────────

**DO-178C in 10 Points:**

1. ⭐ **5 DAL levels:** A (catastrophic) to E (no effect)
2. 📊 **71 objectives total** (varies by DAL)
3. 🎯 **MC/DC required** for DAL A & B
4. 🔗 **Traceability required** at all levels
5. 🔍 **Independence required** for DAL A (and B for some objectives)
6. 📝 **5 key plans:** PSAC, SDP, SVP, SCMP, SQAP
7. 🛠️ **Tools must be qualified** if they eliminate verification
8. ✅ **SAS is the key deliverable** for certification
9. 🔄 **Configuration management** is mandatory
10. 🎓 **Process-driven, not prescriptive** methodology

**Quick Decision Tree:**

```
Is your software safety-critical?
  ├─ YES → Determine DAL based on failure effect
  │         ├─ Catastrophic → DAL A (full rigor)
  │         ├─ Hazardous → DAL B (high rigor)
  │         ├─ Major → DAL C (medium rigor)
  │         ├─ Minor → DAL D (low rigor)
  │         └─ No effect → DAL E (minimal rigor)
  └─ NO → Consider other standards (e.g., ISO 9001)
```

════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────

**Q1: What's the difference between DAL A and DAL D?**
→ DAL A = catastrophic failure, full MC/DC, independence required  
→ DAL D = minor failure, statement coverage, no independence

**Q2: What is MC/DC and when is it required?**
→ Modified Condition/Decision Coverage  
→ Required for DAL A & B  
→ Each condition independently affects decision outcome

**Q3: What are the 5 key planning documents?**
→ PSAC, SDP, SVP, SCMP, SQAP

**Q4: When must tools be qualified?**
→ When they eliminate verification or produce unverifiable output

**Q5: What's the most important deliverable for certification?**
→ SAS (Software Accomplishment Summary) — summarizes all compliance data

════════════════════════════════════════════════════════════════════

📚 **FURTHER READING**
──────────────────────

📖 DO-178C Official Standard (RTCA/EUROCAE)  
📖 "DO-178C Software Development for Airborne Systems" — Leanna Rierson  
📖 DO-330 (Tool Qualification)  
📖 DO-331 (Model-Based Development supplement)  
📖 DO-332 (Object-Oriented supplement)  
📖 DO-333 (Formal Methods supplement)

════════════════════════════════════════════════════════════════════

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Target Audience:** Aircraft Services Architects, Avionics Engineers, Certification Specialists
