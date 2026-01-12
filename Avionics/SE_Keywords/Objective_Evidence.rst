📚 **Objective Evidence: Proof That Software Meets Requirements** (2026 Edition!)
=================================================================================

**Quick ID:** Tangible, documented proof (test results, design reviews, coverage metrics, code)
**Key Format:** Documents, test logs, reports, artifacts with dates and author names
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—No objective evidence = no certification possible

---

✈️ **WHAT IS OBJECTIVE EVIDENCE?**
==================================

**Objective Evidence** = Documented, verifiable proof that software meets DO-178C requirements:
  ✅ **Tangible** (not verbal; written documentation, test logs, code, metrics)
  ✅ **Traceable** (linked to specific requirement; can trace from requirement to evidence)
  ✅ **Auditable** (FAA can independently verify; includes dates, signatures, approval)
  ✅ **Complete** (covers all DO-178C requirements and safety objectives)
  ✅ **Credible** (produced throughout project in real-time, not reconstructed at end)

**Core Question:** "What proof can you SHOW FAA that software meets requirements?"

**Opposite:** "We tested thoroughly" (oral claim) ≠ "Here are test logs proving all tests passed" (objective evidence)

---

📋 **TYPES OF OBJECTIVE EVIDENCE**
=================================

**Evidence Type 1: Requirements Specifications**
  📄 **High-Level Requirements (HLRs)**
    • Document: HLR_1.0.docx (v1.0, released Month 3)
    • Content: "System shall maintain altitude within ±50 feet" (HLR_001)
    • Objective Evidence: 
      ✓ Requirements document signed/approved
      ✓ Version control (v1.0, v1.1 with change log)
      ✓ Traceability to system function
      ✓ Verification method specified (System Test SOI_001)
  
  📄 **Low-Level Requirements (LLRs)**
    • Document: LLR_1.0.docx (v1.0, released Month 6)
    • Content: "Software shall read altimeter" (LLR_001.1)
    • Objective Evidence:
      ✓ Detailed requirements with design inputs
      ✓ Derived requirements captured (LLR_D_001 = discovered during design)
      ✓ Version control and changes tracked

**Evidence Type 2: Design Documentation**
  📄 **Preliminary Design Review (PDR)**
    • Document: PDR_Minutes_Month4.docx
    • Content: Architecture review, feedback from reviewers, approval decision
    • Objective Evidence:
      ✓ Meeting minutes (date, attendees, topics)
      ✓ Review findings (5 findings identified, 5 resolved)
      ✓ Approval sign-off (PDR passed; ready for detailed design)
      ✓ Design changes required (4 changes planned)
  
  📄 **Critical Design Review (CDR)**
    • Document: CDR_Minutes_Month7.docx
    • Content: Detailed design approval, integration points, test strategy confirmation
    • Objective Evidence:
      ✓ Design complete (all modules designed)
      ✓ Interfaces documented (hardware/software interfaces)
      ✓ Verification approach confirmed (unit test, integration test plans attached)
      ✓ Final approval (ready for implementation)

**Evidence Type 3: Code**
  📄 **Source Code Files**
    • Document: altitude_control.c (v1.2, released Month 10)
    • Content: Implementation of altitude hold logic
    • Objective Evidence:
      ✓ Version control (committed to git Month 10)
      ✓ Code comments (explaining logic, especially complex decisions)
      ✓ Code reviews (peer review comments, approvals)
      ✓ Traceability (comments link code to LLR IDs)
      ✓ Example: `// LLR_001.2: Calculate altitude error` (comment shows linkage)

**Evidence Type 4: Test Plans**
  📄 **Unit Test Plan (UT_Plan_v1.0.docx)**
    • Document: UT_Plan_Month5.docx
    • Content: Unit test strategy, test case descriptions, coverage approach
    • Objective Evidence:
      ✓ Test approach (how will unit tests verify requirements?)
      ✓ Test case IDs (UT_001, UT_002, etc. linked to LLRs)
      ✓ Coverage targets (MC/DC 100% for DAL A)
      ✓ Approval (DER reviews and approves plan)

  📄 **Integration Test Plan (IT_Plan_v1.0.docx)**
    • Document: IT_Plan_Month6.docx
    • Content: Module-to-module interface testing
    • Objective Evidence:
      ✓ Integration scenarios (how modules interact)
      ✓ Test cases linked to requirements
      ✓ Coverage targets and approach

  📄 **System Test Plan (SYS_Plan_v1.0.docx)**
    • Document: SYS_Plan_Month8.docx
    • Content: End-to-end system testing (all functions together)
    • Objective Evidence:
      ✓ System test scenarios (altitude hold in various conditions)
      ✓ Expected results (defined before testing)
      ✓ Test environment (lab setup, flight test setup)

**Evidence Type 5: Test Results & Logs**
  📄 **Unit Test Results (UT_Results_Month10.xls)**
    • Document: UT_Results.xls
    • Content: All unit tests executed, results captured
    • Objective Evidence:
      ✓ Test case ID (UT_001)
      ✓ Input (test data values)
      ✓ Expected output (what should happen)
      ✓ Actual output (what did happen)
      ✓ Result (PASS/FAIL)
      ✓ Coverage metrics (code statement coverage for this test)
      ✓ Date executed (Month 10)
      ✓ Tester name (who ran the test)
  
  📄 **Integration Test Results**
    • Document: IT_Results_Month12.xls
    • Content: Interface testing results
    • Objective Evidence:
      ✓ Each IT_xxx test case: input, output, PASS/FAIL
      ✓ Interface verification (messages between modules correct)
      ✓ Defects found and fixed (defect ID, description, fix, re-test result)

  📄 **System Test Results**
    • Document: SYS_Results_Month16.xls
    • Content: End-to-end testing (altitude hold function in real conditions)
    • Objective Evidence:
      ✓ Test scenario (maintain altitude 10,000 feet, climb rate 500 ft/min)
      ✓ Actual result (altitude held 10,020 feet, within ±50 specification)
      ✓ PASS/FAIL status
      ✓ Date, tester, environment

**Evidence Type 6: Coverage Analysis Reports**
  📄 **Structural Coverage Report (Coverage_Report_Month16.pdf)**
    • Document: Coverage_Month16.pdf (from coverage analyzer)
    • Content: MC/DC coverage, decision coverage, statement coverage metrics
    • Objective Evidence:
      ✓ Coverage percentages (MC/DC 100%, Decision 100%, Statement 98%)
      ✓ Module-by-module breakdown (which modules at what coverage)
      ✓ Uncovered code identified (2 error paths not exercised)
      ✓ Justification for uncovered code (unreachable/defensive code)
      ✓ Tool qualification evidence (coverage tool itself qualified)

**Evidence Type 7: Defect Tracking**
  📄 **Defect Report (Defect_001_Altitude_Calculation.docx)**
    • Document: Defect_001.docx
    • Content: Issue found during testing
    • Objective Evidence:
      ✓ Defect ID (Defect_001)
      ✓ Date found (Month 10)
      ✓ Component (altitude_control.c)
      ✓ Symptom (altitude error > 100 feet in some cases)
      ✓ Root cause (calculation logic bug)
      ✓ Fix applied (code correction, v1.1)
      ✓ Verification (re-tested, PASS)
      ✓ Closure date (Month 10, same week)

**Evidence Type 8: Traceability Matrix**
  📄 **Compliance Matrix (Traceability_v1.0.xls)**
    • Document: Traceability_Matrix_Month18.xls
    • Content: Master linkage document
    • Objective Evidence:
      | HLR_ID | LLR_ID | Test_Case | Result | Coverage |
      |:-------|:-------|:----------|:-------|:---------|
      | HLR_001 | LLR_001.1 | UT_001 | PASS | MC/DC 100% |
      | HLR_001 | LLR_001.2 | UT_002 | PASS | Decision 100% |
      | HLR_001 | LLR_001.3 | IT_001 | PASS | Statement 99% |
      | HLR_001 | LLR_001.4 | SYS_001 | PASS | MC/DC 98% |

**Evidence Type 9: Review & Approval Records**
  📄 **Design Review Minutes (DRB_Minutes_Month7.docx)**
    • Document: DRB_Minutes.docx
    • Content: Design Review Board (DRB) meeting record
    • Objective Evidence:
      ✓ Date, attendees (team, DER, SQA, independent reviewer)
      ✓ Design reviewed (architecture, modules, interfaces)
      ✓ Findings (issues identified: 3 found, 3 resolved)
      ✓ Approval decision (APPROVED for implementation)
      ✓ Signatures (DRB chair, DER signature authorizing approval)

  📄 **SQA Review Records (SQA_Review_Phase3.docx)**
    • Document: SQA_Review_Phase3.docx (Month 8)
    • Content: Independent quality assurance verification
    • Objective Evidence:
      ✓ Requirements traceability adequate (all requirements linked to design/test)
      ✓ Test coverage adequate (coverage metrics on track)
      ✓ Configuration management effective (baselines, change control working)
      ✓ SQA findings (0 findings; quality satisfactory)

**Evidence Type 10: Tool Qualification**
  📄 **Compiler Qualification Report (Tool_Qualification_GCC.docx)**
    • Document: Compiler_Qual.docx
    • Content: Proof that compiler is trustworthy
    • Objective Evidence:
      ✓ Tool: GCC version 9.3.0
      ✓ Test case (compile simple altitude calculation program)
      ✓ Test result (compiled executable runs correctly)
      ✓ Conclusion (compiler qualified for use)
      ✓ Version locked (GCC 9.3.0 used throughout project; no mid-project upgrades)

---

📦 **OBJECTIVE EVIDENCE PACKAGE STRUCTURE**
==========================================

**Standard 6-Volume Certification Package:**

**Volume 1: Requirements**
  📄 Requirements specification (HLRs + LLRs)
  📄 Requirements review records (approved)
  📄 Derived requirements (discovered during design, documented, approved)
  📄 Requirements traceability (to design/code/test)

**Volume 2: Design**
  📄 Architecture document
  📄 Detailed design (modules, interfaces)
  📄 Design reviews (PDR, CDR minutes, approvals)
  📄 Design changes (change history)

**Volume 3: Implementation**
  📄 Source code (key files, well-commented)
  📄 Code reviews (peer review records, approvals)
  📄 Code checklist (safety practices followed: error handling, initialization, etc.)

**Volume 4: Verification & Test**
  📄 Test plans (UT, IT, SYS plans)
  📄 Test results (all tests documented, PASS/FAIL)
  📄 Coverage analysis (MC/DC, decision, statement %)
  📄 Defect history (found, fixed, re-tested, closed)

**Volume 5: Compliance & Traceability**
  📄 Compliance matrix (Requirement ↔ Test ↔ Result)
  📄 Traceability matrix (all linkages documented)
  📄 Gap analysis (any unverified requirements? No.)
  📄 Compliance statement (narrative: how does evidence prove DO-178C compliance?)

**Volume 6: Supporting Records**
  📄 Tool qualification (compiler, coverage analyzer, static analysis)
  📄 Configuration management records (baselines, changes, CM audit)
  📄 SQA findings (quality assurance oversight records)
  📄 Process assurance (independent audits of SQA process)

---

💡 **OBJECTIVE EVIDENCE BEST PRACTICES**
=======================================

✅ **Tip 1: Collect objective evidence throughout project (real-time), not at the end**
  ❌ Mistake: "Testing complete Month 16; spend Months 17–22 collecting evidence"
  ✅ Right: "Evidence captured as produced (test results same day test runs)"
  Impact: Evidence authentic, complete, accurate; no 4-month scramble

✅ **Tip 2: Objective evidence must be traceable (linked to specific requirement)**
  ❌ Mistake: "Lots of test results; can't connect to which requirement verified"
  ✅ Right: "Every test result includes requirement ID it verifies"
  Impact: FAA can trace requirement → test → result independently

✅ **Tip 3: Include actual artifacts (test logs, code, metrics), not summaries**
  ❌ Mistake: "Test summary: 'All tests passed; coverage good'"
  ✅ Right: "Test log spreadsheet (50 rows of individual test results) + coverage report (100% MC/DC)"
  Impact: FAA sees authentic evidence, not interpreted summaries

✅ **Tip 4: Objective evidence must be signed/approved (author, date, approver)**
  ❌ Mistake: "Design document with no approval signature"
  ✅ Right: "Design approved Month 7, signed by PDR chair + DER"
  Impact: Authority clear; approval documented

✅ **Tip 5: Objective evidence organized hierarchically (top-level requirement → detailed tests)**
  ❌ Mistake: "Hundreds of artifacts scattered; no organization"
  ✅ Right: "Organized by requirement ID; traceability matrix connects all"
  Impact: FAA can navigate and verify independently

---

⚠️ **COMMON OBJECTIVE EVIDENCE MISTAKES**
=========================================

❌ **Mistake 1: Insufficient evidence (only high-level summary; no test details)**
  Problem: "Say 'altitude hold verified by system test'; no actual test log"
  Impact: FAA can't verify independently; demands rework
  Fix: Include actual test logs (inputs, outputs, PASS/FAIL, dates, testers)

❌ **Mistake 2: Unsigned/unapproved evidence (document without approval)**
  Problem: "Test results documented; no signature of who ran them or approved"
  Impact: FAA questions credibility (who performed testing?)
  Fix: All objective evidence signed (author name, date, reviewer approval)

❌ **Mistake 3: Collected at end (Month 22, after testing complete)**
  Problem: "Reconstruct test logs Month 22 from memory; incomplete/inaccurate"
  Impact: Evidence appears fabricated; FAA skeptical
  Fix: Capture evidence in real-time as testing occurs

❌ **Mistake 4: Not traceable to requirements (test results not linked to HLR/LLR)**
  Problem: "Test results documented; can't determine which requirement each test verifies"
  Impact: Compliance not demonstrable
  Fix: Every test case includes requirement ID it verifies

❌ **Mistake 5: Inconsistent/contradictory evidence (different documents show different coverage %)**
  Problem: "Test summary says 90% coverage; coverage report says 85%"
  Impact: FAA questions which is accurate; entire evidence package credibility damaged
  Fix: Compliance matrix single source of truth (derived from actual test/coverage data)

---

🎓 **LEARNING PATH: Objective Evidence**
=======================================

**Week 1: What Is Objective Evidence**
  📖 Read: DO-178C Section 8 (certification data and procedures)
  📖 Study: Types of evidence (requirements, design, code, tests, metrics)
  🎯 Goal: Understand what counts as objective evidence vs. claims

**Week 2: Collecting & Organizing Evidence**
  📖 Study: Real project evidence collection (test logs, coverage reports, reviews)
  📖 Analyze: Traceability matrix (how evidence linked to requirements)
  🎯 Goal: Understand evidence organization and linkage

**Week 3: Evidence Package Assembly**
  💻 Case study: Complete 6-volume certification package
  💻 Practice: Outline evidence structure for hypothetical altitude hold project
  🎯 Goal: Confidence in evidence package compilation and presentation to FAA

---

✨ **BOTTOM LINE**
=================

**Objective Evidence = Documented, traceable proof that software meets DO-178C requirements**

✅ **Real artifacts** (test logs, code, metrics—not summaries)
✅ **Traceable** (linked to specific requirement IDs)
✅ **Signed/approved** (author name, date, approver signature)
✅ **Collected in real-time** (throughout project, not reconstructed at end)
✅ **Organized hierarchically** (traceability matrix connects all evidence)
✅ **Independently verifiable** (FAA can trace requirement → design → code → test → result)

**Remember:** 📚 **Objective Evidence = "Proof!" Not "We say so."** ✈️

---

**Last updated:** 2026-01-12 | **Objective Evidence**

**Key Takeaway:** 💡 **Good OE = "FAA reviews evidence, independently verifies compliance!" Bad OE = "FAA says 'show me the proof,' team has nothing!"** 🛡️
