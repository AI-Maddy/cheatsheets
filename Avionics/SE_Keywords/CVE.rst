📦 **CVE: Compliance Verification Engineering (Proving Compliance)** (2026 Edition!)
==================================================================================

**Quick ID:** Systematic demonstration that software meets DO-178C requirements
**Key Output:** Compliance matrix (Requirement ↔ Verification Evidence ↔ Coverage)
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—CVE proves software compliant; required for certification

---

✈️ **WHAT IS CVE (COMPLIANCE VERIFICATION ENGINEERING)?**
========================================================

**CVE** = Systematic process of proving software complies with DO-178C by:
  ✅ **Traceability verification** (every requirement linked to design, code, test)
  ✅ **Test evidence collection** (test results show requirements verified)
  ✅ **Coverage analysis** (metrics prove adequate coverage MC/DC, decision, statement)
  ✅ **Objective evidence assembly** (documentation package proves compliance)
  ✅ **Authority demonstration** (FAA/EASA can independently verify compliance)

**Synonym:** "Compliance Case" or "Compliance Verification Strategy" (some docs use these terms)

**Core Question CVE Answers:** "How do we PROVE to FAA that software meets DO-178C and system requirements?"

---

🔄 **CVE PROCESS (5 Steps)**
===========================

**Step 1: Requirement Verification Planning (Month 2–3)**
  🎯 Input: All requirements (HLR + LLR)
  🎯 Question: How will each requirement be verified?
  🎯 Process:
    • Map each requirement to verification method (inspection, unit test, integration test, system test, analysis)
    • Create verification matrix: Requirement ID ↔ Test Case ID ↔ Verification Method
    • Plan test scenarios (realistic, covers normal + error conditions)
  🎯 Output: Verification plan (document describing approach)

  **Example (Altitude Hold Function):**
    • HLR 001: "System shall maintain altitude ±50 feet" → Verification: System Test (flight test)
    • LLR 001.1: "Software shall read altimeter" → Verification: Unit Test (mock altimeter input)
    • LLR 001.2: "Software shall calculate altitude error" → Verification: Unit Test (math check)
    • LLR 001.3: "Software shall send pitch command to autopilot" → Verification: Integration Test (autopilot interface)

**Step 2: Test Case Development (Month 3–6)**
  🎯 Input: Verification plan from Step 1
  🎯 Process:
    • Develop detailed test cases (every test case linked to requirement)
    • Each test case: Input, expected output, how to execute
    • Include normal cases + error cases
    • Maintain test case ID / requirement ID linkage
  🎯 Output: Test specifications (document with 100s of test cases)

  **Example:**
    • TC-001: "Read altimeter (normal case: altitude = 10,000 feet)" → Linked to LLR 001.1
    • TC-002: "Read altimeter (error case: altimeter fails)" → Linked to LLR 001.1
    • TC-003: "Calculate altitude error (target 10,000, actual 10,050)" → Linked to LLR 001.2
    • TC-004: "Send pitch command to autopilot" → Linked to LLR 001.3

**Step 3: Test Execution & Data Collection (Month 6–16)**
  🎯 Input: Test cases from Step 2
  🎯 Process:
    • Execute all test cases (unit testing, integration testing, system testing)
    • Capture test results (inputs, outputs, pass/fail status)
    • Measure coverage (MC/DC, decision, statement coverage %)
    • Document defects found (what failed? how fixed?)
  🎯 Output: Test results (test logs, coverage reports, defect lists)

  **Example Results:**
    • TC-001: PASS (altimeter read correctly, value 10,000 feet as input)
    • TC-002: PASS (altimeter error detected, error handler triggered)
    • Coverage: MC/DC 100%, Decision 95%, Statement 98%
    • Defects: 5 found, 5 fixed (all now passing)

**Step 4: Traceability Verification (Month 16–18)**
  🎯 Input: Verification results from Step 3
  🎯 Process:
    • Verify all requirements have corresponding tests (no requirement left unverified)
    • Verify all tests mapped to requirements (no orphan tests)
    • Verify all passed tests have objective evidence (test logs retained)
    • Create compliance matrix: Requirement ↔ Test Case ↔ Test Result ↔ Coverage Metric
  🎯 Output: Traceability matrix (master document showing all linkages)

  **Example Matrix Row:**
    | Requirement | Test Case | Status | Coverage |
    |:------------|:----------|:-------|:---------|
    | LLR 001.1   | TC-001    | PASS   | MC/DC 100% |
    | LLR 001.1   | TC-002    | PASS   | MC/DC 100% |
    | LLR 001.2   | TC-003    | PASS   | Decision 95% |
    | (Result: Requirement LLR 001.1 verified by 2 tests, both passed, 100% coverage) |

**Step 5: Compliance Evidence Package Assembly (Month 18–22)**
  🎯 Input: All documentation from Steps 1–4
  🎯 Process:
    • Assemble objective evidence (requirements, design, code, tests, coverage metrics, traceability)
    • Create executive summary (high-level compliance story)
    • Prepare compliance case (How does this demonstrate DO-178C compliance?)
    • Organize for FAA review (6–10 volume package, indexed, cross-referenced)
  🎯 Output: Certification package ready for FAA/EASA submission

---

📋 **CVE COMPLIANCE MATRIX (Core Document)**
============================================

**Example for Altitude Hold Function (Simplified)**

| Req ID | Requirement | Design | Code Module | Test Case | Status | Coverage |
|:-------|:-----------|:-------|:-----------|:----------|:-------|:---------|
| HLR001 | Maintain altitude ±50 ft | AltControl arch | altitude_control.c | SYS-TEST-001 | PASS | MC/DC 100% |
| LLR001.1 | Read altimeter | Input module | read_sensor() | UT-001, UT-002 | PASS | Decision 100% |
| LLR001.2 | Calculate error | Math module | calc_error() | UT-003, UT-004 | PASS | MC/DC 100% |
| LLR001.3 | Send pitch cmd | Output module | send_command() | IT-005, SYS-006 | PASS | Statement 99% |
| LLR001.4 | Handle altimeter fail | Error handler | handle_fault() | UT-007, IT-008 | PASS | MC/DC 98% |

**Interpretation:**
  ✅ HLR001 (top-level requirement) traced to 5 LLRs (design + code)
  ✅ Each LLR verified by unit + integration tests
  ✅ All tests PASS (no failures)
  ✅ Coverage targets met (MC/DC 100%, decision 100%)
  ✅ **Conclusion: HLR001 compliant with DO-178C**

---

🎯 **CVE COVERAGE TARGETS (By DAL Level)**
==========================================

**DAL A (Catastrophic—Flight Control)**
  🎯 Structural Coverage: MC/DC 100% (modified condition/decision coverage)
  🎯 Decision Coverage: 100% (every decision true AND false tested)
  🎯 Statement Coverage: 100% (every statement executed)
  
  📝 Example: Altitude hold system (holds altitude within ±50 feet)
  • If altitude > target + 50: Lower pitch (decision true)
  • If altitude < target - 50: Raise pitch (decision false)
  • Both conditions tested ✓

**DAL B (Hazardous—Engine Control)**
  🎯 Structural Coverage: MC/DC 100% or Decision 100%
  🎯 Statement Coverage: 100%
  
**DAL C (Major—ADAS/Warning)**
  🎯 Structural Coverage: Decision 100% (minimum)
  🎯 Statement Coverage: 100%

**DAL D (Minor—Cabin Lighting)**
  🎯 Structural Coverage: Statement 100% (minimum)
  🎯 (or analysis showing code trivial/verified by inspection)

**DAL E (No Safety Impact)**
  🎯 No specific coverage targets

---

📦 **CVE OBJECTIVE EVIDENCE (What Goes in Package)**
===================================================

**Volume 1: Requirements Specification**
  📄 HLRs (High-Level Requirements)
  📄 LLRs (Low-Level Requirements)
  📄 Requirement traceability (Requirement ↔ System function)
  📄 Requirements review evidence (signed-off by team, DER)

**Volume 2: Design Documentation**
  📄 Architecture (high-level design)
  📄 Detailed design (components, interfaces)
  📄 Design reviews (PDR, CDR meeting minutes, approval)
  📄 Design change history (any modifications tracked)

**Volume 3: Verification Results**
  📄 Unit test plans and results (all unit tests documented)
  📄 Integration test plans and results (interface testing documented)
  📄 System test plans and results (end-to-end testing documented)
  📄 Coverage analysis reports (MC/DC, decision, statement %)

**Volume 4: Traceability & Compliance**
  📄 **Compliance matrix** (Requirement ↔ Design ↔ Code ↔ Test)
  📄 **Traceability matrix** (shows linkages)
  📄 **Gap analysis** (any requirements not fully verified? documented)
  📄 **Compliance statement** (narrative: "How does this prove compliance?")

**Volume 5: Tool Qualification**
  📄 Compiler qualification (tool tested, results documented)
  📄 Coverage tool qualification (coverage analyzer tested and approved)
  📄 Static analysis tool qualification (defect finder tested)
  📄 Debugger/IDE tool qualification (development tools)

**Volume 6: Configuration Management**
  📄 Configuration items (source code, requirements, design versions)
  📄 Baselines (configuration snapshots at major milestones)
  📄 Change history (modifications tracked)
  📄 Audit trail (who changed what and when)

**Volume 7–10: Supporting Documentation**
  📄 Problem reports (any issues found? how resolved?)
  📄 Corrective action records (process improvements)
  📄 Process assurance records (SQA reviews, audits)
  📄 Lifecycle data (all project documentation)

---

⚡ **CVE BEST PRACTICES**
======================

✅ **Tip 1: Plan verification early (PSAC Month 2, not Month 16)**
  ❌ Mistake: "Design completion Month 8; realize we can't verify something"
  ✅ Right: "Verify ability to test every requirement before design starts"
  Impact: Verification feasible; no surprises late-project

✅ **Tip 2: Traceability is foundational (Requirement ↔ Test linkage)**
  ❌ Mistake: "Complete testing; can't map tests back to requirements"
  ✅ Right: "Every test linked to requirement ID from start"
  Impact: Compliance clear; FAA can verify independently

✅ **Tip 3: Coverage metrics drive test adequacy (achieve targets per DAL)**
  ❌ Mistake: "Test 80% of code; claim 100% coverage"
  ✅ Right: "Measure coverage; add tests until MC/DC 100% (DAL A)"
  Impact: Coverage credible; compliance proven

✅ **Tip 4: Objective evidence collected as you go (not assembled at end)**
  ❌ Mistake: "Testing complete Month 16; try to gather evidence Month 22 (4-month scramble)"
  ✅ Right: "Test results captured in real-time; packaged throughout project"
  Impact: Evidence complete and authentic; certification smooth

✅ **Tip 5: Compliance matrix is master document (single source of compliance truth)**
  ❌ Mistake: "Multiple documents claiming different compliance status (inconsistent)"
  ✅ Right: "Compliance matrix single source of truth (Requirement ↔ Test ↔ Result)"
  Impact: FAA understands compliance clearly; no disputes

---

⚠️ **COMMON CVE MISTAKES**
=========================

❌ **Mistake 1: Verification planning deferred until late (Month 8+ instead of Month 2)**
  Problem: "Design complete; realize some requirements can't be verified"
  Impact: Rework required (design changes, additional testing)
  Fix: Plan verification approach in PSAC (Month 2); ensure all requirements testable

❌ **Mistake 2: Test cases not linked to requirements (orphan tests)**
  Problem: "Lots of tests executed; can't map back to which requirement verified"
  Impact: Compliance not provable; FAA questions credibility
  Fix: Every test case linked to specific requirement ID from creation

❌ **Mistake 3: Coverage targets not met (80% instead of 100% for DAL A)**
  Problem: "Coverage short of target; claim 'good enough'"
  Impact: FAA rejects; additional testing required; delays
  Fix: Measure coverage throughout project; add tests until targets met

❌ **Mistake 4: Test data not captured (tests run; results not documented)**
  Problem: "Testing complete; can't show FAA what actually tested"
  Impact: No objective evidence; FAA doubts testing occurred
  Fix: Capture test results real-time (test logs, screenshots, reports)

❌ **Mistake 5: Compliance matrix developed at end (Month 22) instead of built up**
  Problem: "20+ volumes of documentation; can't connect to compliance"
  Impact: 4-month scramble to create compliance matrix; assembly errors
  Fix: Build traceability throughout project; compliance matrix grows with project

---

🎓 **LEARNING PATH: CVE**
=======================

**Week 1: CVE Concepts**
  📖 Read: DO-178C Section 3 (verification objectives), Section 5 (traceability)
  📖 Study: Compliance matrix concept, coverage targets by DAL
  🎯 Goal: Understand how CVE proves DO-178C compliance

**Week 2: Traceability & Testing**
  📖 Study: Real project traceability matrix (Requirement ↔ Test ↔ Result)
  📖 Analyze: Coverage metrics (MC/DC, decision, statement), how measured
  🎯 Goal: Understand traceability linkages and coverage verification

**Week 3: Compliance Evidence & Packaging**
  💻 Case study: Real certification package (structure, key documents)
  💻 Practice: Outline CVE strategy for hypothetical altitude hold project
  🎯 Goal: Confidence in building compliance case from requirements through testing

---

✨ **BOTTOM LINE**
=================

**CVE = Systematic proof that software meets DO-178C requirements**

✅ Verification planning early (PSAC, Month 2)
✅ Traceability linkage (Requirement ↔ Design ↔ Code ↔ Test)
✅ Coverage targets achieved (MC/DC per DAL level)
✅ Test results documented (objective evidence captured)
✅ Compliance matrix built throughout project (not scrambled at end)
✅ Package assembled (6–10 volumes with clear compliance story)

**Remember:** 📦 **CVE = "FAA can independently verify we met DO-178C!" Not just "we tested a lot."** ✈️

---

**Last updated:** 2026-01-12 | **CVE**

**Key Takeaway:** 💡 **Good CVE = "Clear requirement ↔ test ↔ result linkage; FAA confident compliance proven!" Bad CVE = "Can't trace tests to requirements; compliance unclear!"** 🛡️
