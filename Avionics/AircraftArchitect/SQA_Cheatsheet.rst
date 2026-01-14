🔎 **Software Quality Assurance (SQA) — Comprehensive Cheatsheet**
═══════════════════════════════════════════════════════════════════

**Context:** DO-178C compliance for airborne software systems  
**Focus:** Process audits, tool qualification, configuration management  
**Target Audience:** SQA engineers, quality managers, certification auditors

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — SQA IN 60 SECONDS**
─────────────────────────────────

**What is SQA?**

Software Quality Assurance = **Independent process watchdog**

.. code-block:: text

   Development Team    SQA Team (Independent)
         │                    │
         ├─► Writes code      ├─► Audits process
         ├─► Runs tests       ├─► Verifies traceability
         └─► Fixes bugs       └─► Reports non-conformances

**Key SQA Responsibilities (DO-178C §8):**

✅ **Process Monitoring:** Verify plans are followed  
✅ **Process Audits:** Regular checks (in-process + transition)  
✅ **Configuration Management:** Verify CM records are accurate  
✅ **Problem Reporting:** Track non-conformances, deviations  
✅ **Tool Qualification:** Verify development/verification tools  

**Mnemonic: "PACPT" (Process, Audit, CM, Problems, Tools)**

**SQA Independence:**

.. code-block:: text

   ❌ Developer audits own work (conflict of interest)
   ❌ Test lead performs SQA (same team bias)
   ✅ Separate SQA group reports to Quality Manager
   ✅ SQA has authority to halt releases

════════════════════════════════════════════════════════════════════

📖 **1. SQA FUNDAMENTALS**
═══════════════════════════

**DO-178C Definition (§8.1):**

*"SQA is a set of planned and systematic activities to provide confidence 
that processes and their outputs satisfy defined requirements and 
objectives."*

**Translation:** SQA checks the **HOW** (process), not just the **WHAT** (product)

**Example:**

+---------------------------------------+---------------------------------------+
| Product Quality (V&V checks this)     | Process Quality (SQA checks this)     |
+=======================================+=======================================+
| "Does the code work correctly?"       | "Was the code reviewed per SQAP?"     |
| "Are test cases passing?"             | "Were test results documented?"       |
| "Is coverage 100%?"                   | "Was coverage measured with qualified |
|                                       | tool?"                                |
+---------------------------------------+---------------------------------------+

**SQA vs. QA vs. QC:**

🔍 **SQA (Software Quality Assurance):**  
   Process-focused, proactive, DO-178C specific

📊 **QA (Quality Assurance):**  
   Broader term (includes hardware, manufacturing)

🔬 **QC (Quality Control):**  
   Product-focused, reactive (inspecting finished goods)

**Memorization Device:**  
SQA = **S**crutinizes **P**rocess, QC = **C**hecks **P**roduct

════════════════════════════════════════════════════════════════════

🛠️ **2. TOOL QUALIFICATION (DO-178C §12)**
═══════════════════════════════════════════

**Why Tool Qualification?**

Problem: If a buggy compiler generates incorrect code, the aircraft 
could crash (even if source code is perfect).

Solution: Qualify development/verification tools to ensure they don't 
introduce errors.

**Tool Qualification Levels (TQL):**

.. code-block:: text

   ┌────────────────────────────────────────────────────────┐
   │  TQL-1: Tool output used as DO-178C evidence           │
   │         (without independent verification)             │
   │         Example: Coverage analyzer (VectorCAST)        │
   │         Requirement: Full Tool Qualification Data      │
   │                                                        │
   │  TQL-2: Tool automates verification process            │
   │         (but output is independently checked)          │
   │         Example: Code generator (MATLAB/Simulink)      │
   │         Requirement: Reduced qualification data        │
   │                                                        │
   │  TQL-3: Tool could insert errors (but cannot fail      │
   │         to detect them)                                │
   │         Example: Compiler (GCC, LLVM)                  │
   │         Requirement: Confidence via service history    │
   │                                                        │
   │  TQL-4: Tool cannot insert/fail to detect errors       │
   │         Example: Word processor, text editor           │
   │         Requirement: NONE (no qualification needed)    │
   │                                                        │
   │  TQL-5: Tool used ONLY for documentation/support       │
   │         Example: Diagram tool, version control         │
   │         Requirement: NONE                              │
   └────────────────────────────────────────────────────────┘

**Tool Qualification Decision Tree:**

.. code-block:: text

   Q1: Does tool output replace DO-178C verification activity?
       ├─► YES → TQL-1 (Full qualification required)
       └─► NO → Q2
   
   Q2: Could tool output introduce errors into software?
       ├─► YES → Q3
       └─► NO → TQL-4 or TQL-5 (No qualification)
   
   Q3: Can errors be detected by normal verification?
       ├─► YES → TQL-2 (Reduced qualification)
       └─► NO → TQL-1 (Full qualification)

**Example 1: VectorCAST Coverage Analyzer (TQL-1)**

.. code-block:: text

   Tool Function: Measure MC/DC coverage
   
   Risk: If tool incorrectly reports "100% MC/DC" when it's actually 
         85%, untested code ships to aircraft
   
   Mitigation: Tool Qualification Data Package (TQDP) includes:
       ✅ Tool Operational Requirements (TOR)
       ✅ Tool test cases (test the tool itself!)
       ✅ Tool configuration management
       ✅ Service history (proven track record)
   
   Acceptance: FAA DER reviews TQDP, approves tool for project

**Example 2: GCC Compiler (TQL-3)**

.. code-block:: text

   Tool Function: Compile C source to binary
   
   Risk: Compiler optimization bug could generate incorrect assembly
   
   Mitigation: NOT fully qualified, but:
       ✅ Service history (GCC used on 1000+ projects)
       ✅ Test suite (GCC's own regression tests)
       ✅ Verification detects errors (MC/DC catches bad codegen)
   
   Note: Some projects use DO-178C-qualified compilers (e.g., Green Hills)

**Tool Qualification Artifacts:**

📄 **Tool Operational Requirements (TOR):**  
   "What must the tool do correctly?"

📄 **Tool Qualification Plan (TQP):**  
   "How will we prove the tool works?"

📄 **Tool Test Cases:**  
   Tests for the tool itself (not the software under test)

📄 **Tool Accomplishment Summary:**  
   "Here's proof we qualified the tool"

════════════════════════════════════════════════════════════════════

🔍 **3. PROCESS AUDITS**
═════════════════════════

**Audit Types (DO-178C §8.3):**

🔄 **In-Process Audits:**  
   Continuous monitoring during development (weekly/monthly)

🎯 **Transition Audits:**  
   Major milestone checks (e.g., code freeze, before certification)

📊 **Configuration Audits:**  
   Verify CM records match actual deliverables

**Audit Workflow:**

.. code-block:: text

   Step 1: SQA reviews Software Quality Assurance Plan (SQAP)
           ├─► Understand process requirements
           └─► Create audit checklist
   
   Step 2: Schedule audit (with 2-week notice to dev team)
           ├─► Request artifacts (code, test results, reviews)
           └─► Announce scope (e.g., "LLR review process")
   
   Step 3: Conduct audit
           ├─► Review artifacts against SQAP
           ├─► Interview developers/testers
           └─► Note non-conformances
   
   Step 4: Generate audit report
           ├─► List findings (minor, major, critical)
           ├─► Assign corrective actions
           └─► Set deadlines
   
   Step 5: Verify corrective actions closed
           ├─► Re-audit if critical findings
           └─► Sign-off when resolved

**Sample Audit Checklist (Code Review Process):**

+------+--------------------------------------------+---------+--------+
| Item | Check                                      | Pass/   | Notes  |
|      |                                            | Fail    |        |
+======+============================================+=========+========+
| 1    | Was code review scheduled per SQAP?        | ✅ PASS |        |
| 2    | Did review have ≥2 reviewers (independent)?| ✅ PASS |        |
| 3    | Were review comments documented?           | ❌ FAIL | Missing|
|      |                                            |         | minutes|
| 4    | Were all defects resolved before baseline? | ✅ PASS |        |
| 5    | Was traceability verified (LLR→Code)?      | ✅ PASS |        |
+------+--------------------------------------------+---------+--------+

**Result:** 1 non-conformance (NCR-2026-003 opened for missing minutes)

**Non-Conformance Report (NCR) Template:**

.. code-block:: text

   ┌────────────────────────────────────────────────────────┐
   │ NCR ID: NCR-2026-003                                   │
   │ Date: January 14, 2026                                 │
   │ Auditor: Jane Smith (SQA Lead)                         │
   │                                                        │
   │ Finding:                                               │
   │   Code review for autopilot.c (v2.3) did NOT have     │
   │   documented review minutes. SQAP §4.2 requires       │
   │   meeting minutes with action items.                   │
   │                                                        │
   │ Severity: MAJOR (process violation, not safety impact) │
   │                                                        │
   │ Corrective Action:                                     │
   │   1. Recreate review minutes from email thread        │
   │   2. Update code review template to include minutes   │
   │   3. Re-train team on SQAP requirements               │
   │                                                        │
   │ Owner: Bob Jones (Software Manager)                    │
   │ Due Date: January 21, 2026                             │
   │                                                        │
   │ Status: OPEN → CLOSED (verified by SQA on 1/20/26)    │
   └────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════

📦 **4. CONFIGURATION MANAGEMENT (CM) VERIFICATION**
════════════════════════════════════════════════════

**SQA's CM Responsibilities (DO-178C §7.2 + §8.3):**

✅ Verify CM Plan is followed  
✅ Audit baselines (ensure integrity)  
✅ Check change control (CCB approvals)  
✅ Verify traceability (SCI accuracy)  

**Configuration Items (CI) for DO-178C:**

.. code-block:: text

   ┌─────────────────────────────────────────────────┐
   │  Configuration Items (Version-Controlled)       │
   ├─────────────────────────────────────────────────┤
   │  📄 Plans: PSAC, SDP, SCMP, SQAP, SVP          │
   │  📄 Requirements: HLR, LLR                      │
   │  💻 Source Code: .c, .h files                   │
   │  🔧 Build Scripts: Makefiles, linker configs    │
   │  🧪 Test Cases: Test procedures, test data      │
   │  📊 Traceability: Matrices (Req→Code→Test)      │
   │  🐛 Problem Reports: Defect logs, NCRs          │
   └─────────────────────────────────────────────────┘

**CM Audit Example:**

.. code-block:: bash

   # SQA task: Verify that SCI matches actual repository
   
   # Step 1: Get Software Configuration Index (SCI) from CM team
   cat SCI_v1.3.txt
   # Output: autopilot.c v2.3 (SHA: a1b2c3d4)
   
   # Step 2: Check actual Git repository
   git log --oneline autopilot.c | head -1
   # Output: a1b2c3d4 "Fix altitude threshold bug"
   
   # Step 3: Verify checksum matches
   sha256sum autopilot.c
   # Output: a1b2c3d4... (matches SCI) ✅
   
   # Step 4: Check for unauthorized changes
   git status --porcelain
   # Output: (empty) ✅ No uncommitted changes

**Change Control Board (CCB) Audit:**

.. code-block:: text

   SQA Question: Was this change approved by CCB before implementation?
   
   Artifact Review:
   ├─► Change Request: CR-2026-042 (requested 1/10/26)
   ├─► CCB Meeting Minutes: Approved 1/12/26 (4 votes yes, 0 no)
   ├─► Implementation: Code committed 1/13/26
   └─► Result: ✅ COMPLIANT (approval before implementation)

════════════════════════════════════════════════════════════════════

🐛 **5. PROBLEM REPORTING**
═══════════════════════════

**Problem Report (PR) Lifecycle:**

.. code-block:: text

   1. DETECTED → Bug found (by test, review, or field)
   2. OPENED → PR created, assigned severity
   3. ANALYZED → Root cause identified
   4. RESOLVED → Fix implemented, verified
   5. CLOSED → SQA confirms fix is correct

**PR Categories:**

🔴 **Critical:** Safety-impacting, blocks certification  
🟡 **Major:** Process violation, non-compliant deliverable  
🟢 **Minor:** Typo, cosmetic issue, documentation clarity

**Example Problem Report:**

.. code-block:: text

   ┌────────────────────────────────────────────────────────┐
   │ PR ID: PR-2026-087                                     │
   │ Date Opened: January 10, 2026                          │
   │ Reporter: Alice Chen (Test Engineer)                   │
   │                                                        │
   │ Title: Autopilot engages below 500 ft (REQ-FCC-123)    │
   │                                                        │
   │ Description:                                           │
   │   Test case TC-AP-001 FAILED. Autopilot engaged at    │
   │   altitude = 495 ft, violating requirement that       │
   │   engagement must occur ONLY above 500 ft.            │
   │                                                        │
   │ Severity: CRITICAL (safety requirement violated)       │
   │                                                        │
   │ Root Cause:                                            │
   │   Code used ">=" instead of ">" in altitude check:    │
   │   if (altitude >= 500) → Changed to (altitude > 500)  │
   │                                                        │
   │ Fix:                                                   │
   │   Commit: d4e5f6a7 "Fix altitude threshold bug"       │
   │   Verified by: Regression test TC-AP-001 (PASSED)     │
   │                                                        │
   │ Status: CLOSED (SQA verified fix on 1/13/26)          │
   └────────────────────────────────────────────────────────┘

**SQA's Problem Reporting Duties:**

✅ Verify all PRs are tracked (nothing falls through cracks)  
✅ Audit severity classifications (critical vs. minor)  
✅ Confirm regression testing after fixes  
✅ Report PR metrics to management (open/closed rates)

**PR Metrics Dashboard:**

.. code-block:: text

   Project: Autopilot Software v3.0 (DAL B)
   
   Total PRs Opened: 143
   ├─► Critical: 7 (all closed)
   ├─► Major: 35 (2 open)
   └─► Minor: 101 (15 open)
   
   Average Time to Close: 4.2 days
   Oldest Open PR: PR-2025-211 (opened 45 days ago) ⚠️

════════════════════════════════════════════════════════════════════

📋 **6. SOFTWARE ACCOMPLISHMENT SUMMARY (SAS) REVIEW**
═══════════════════════════════════════════════════════

**What is SAS?**

The **Software Accomplishment Summary** is the TOP-LEVEL certification 
document submitted to FAA/EASA. It summarizes ALL DO-178C activities.

**SQA's Role:**  
Review SAS for accuracy before submission to DER (Designated Engineering Representative)

**SAS Contents (DO-178C §11.20):**

.. code-block:: text

   1. System Overview
      ├─► Aircraft type (e.g., Boeing 787)
      ├─► Software function (e.g., Flight Control Computer)
      └─► DAL level (e.g., DAL A)
   
   2. Software Life Cycle Process Compliance
      ├─► Plans used (PSAC, SDP, SCMP, SQAP, SVP)
      ├─► Deviations from DO-178C (if any)
      └─► Alternative methods (with justification)
   
   3. Software Development Summary
      ├─► Requirements (HLR, LLR counts)
      ├─► Design methods (UML, flow charts)
      └─► Coding standards (MISRA C:2012)
   
   4. Verification Summary
      ├─► Test cases executed (count, pass/fail)
      ├─► Coverage achieved (Statement, Decision, MC/DC)
      └─► Tools used (and qualification status)
   
   5. Configuration Management Summary
      ├─► Baselines created (dates, versions)
      ├─► Change control (CCB meetings)
      └─► SCI (Software Configuration Index)
   
   6. Quality Assurance Summary
      ├─► Audits performed (count, findings)
      ├─► Non-conformances (all closed?)
      └─► SQA independence statement
   
   7. Problem Reports Summary
      ├─► Total PRs opened/closed
      ├─► Critical PRs (must be zero open)
      └─► Deferred PRs (with justification)
   
   8. Certification Credit
      ├─► Service history (if applicable)
      ├─► Tool qualification credits
      └─► Previously approved data (if reused)

**SQA SAS Review Checklist:**

+------+--------------------------------------------+---------+
| Item | Check                                      | Status  |
+======+============================================+=========+
| 1    | All critical PRs closed?                   | ✅      |
| 2    | Coverage metrics match tool reports?       | ✅      |
| 3    | All deviations documented?                 | ✅      |
| 4    | SQA independence confirmed?                | ✅      |
| 5    | SCI matches baseline?                      | ⚠️ Review |
+------+--------------------------------------------+---------+

════════════════════════════════════════════════════════════════════

🛡️ **7. SQA INDEPENDENCE**
═══════════════════════════

**DO-178C Requirement (§8.2):**

"SQA activities should be conducted with a degree of independence 
commensurate with the software level."

**Translation:**

+----------+-------------------------------------------+
| DAL A/B  | FULL independence (separate reporting     |
|          | chain, veto authority)                    |
+----------+-------------------------------------------+
| DAL C    | PARTIAL independence (different team,     |
|          | same manager acceptable)                  |
+----------+-------------------------------------------+
| DAL D/E  | MINIMAL independence (can be same team    |
|          | if conflicts avoided)                     |
+----------+-------------------------------------------+

**Independence Violations (Examples):**

❌ Developer audits own code review  
❌ Test lead performs SQA (conflict of interest)  
❌ SQA reports to Software Manager (not independent)

**Acceptable SQA Structure:**

.. code-block:: text

   CTO (Chief Technology Officer)
    │
    ├─► VP Engineering
    │      └─► Software Manager
    │             ├─► Developers
    │             └─► Test Engineers
    │
    └─► VP Quality
           └─► SQA Manager ← Reports OUTSIDE dev chain ✅
                  └─► SQA Engineers

════════════════════════════════════════════════════════════════════

⚠️ **8. COMMON SQA PITFALLS**
══════════════════════════════

❌ **Pitfall 1: "SQA is just paperwork"**

**Problem:** Treating SQA as checkbox exercise (rubber stamp)

**Reality:** SQA catches process failures that lead to bugs

**Example:** Developer skipped code review due to schedule pressure. 
SQA audit caught it, forced review, found 3 critical bugs.

────────────────────────────────────────────────────────────────────

❌ **Pitfall 2: Late SQA involvement**

**Problem:** Calling SQA only at end of project (too late!)

**Solution:** In-process audits throughout development

────────────────────────────────────────────────────────────────────

❌ **Pitfall 3: Using unqualified tools**

**Problem:** VectorCAST used without Tool Qualification Data Package

**Risk:** FAA rejects certification evidence, must re-test manually

────────────────────────────────────────────────────────────────────

❌ **Pitfall 4: Closing PRs without regression tests**

**Problem:** "We fixed the bug" but no test to prove it

**SQA Check:** Every PR must have associated test case (new or updated)

────────────────────────────────────────────────────────────────────

❌ **Pitfall 5: Missing traceability**

**Problem:** Code exists but not traced to LLR (orphan code!)

**SQA Audit:** Run traceability report, flag any gaps

════════════════════════════════════════════════════════════════════

📇 **9. QUICK REFERENCE CARD**
═══════════════════════════════

**SQA Key Responsibilities:**

1. **P**rocess monitoring (verify plans followed)
2. **A**udits (in-process + transition)
3. **C**onfiguration management checks
4. **P**roblem reporting (track all PRs)
5. **T**ool qualification (verify TQL compliance)

**Tool Qualification Levels:**

- **TQL-1:** Tool output = DO-178C evidence (full qualification)
- **TQL-2:** Tool automates, but output verified (reduced)
- **TQL-3:** Could introduce errors, but detectable (service history)
- **TQL-4/5:** No qualification needed (no safety impact)

**Audit Frequency:**

- **In-Process:** Every sprint/iteration (Agile) or monthly (Waterfall)
- **Transition:** Major milestones (code freeze, before certification)

**SAS Review Focus:**

✅ All critical PRs closed  
✅ Coverage metrics accurate  
✅ Deviations documented  
✅ SQA independence confirmed

════════════════════════════════════════════════════════════════════

📝 **10. EXAM QUESTIONS**
═════════════════════════

**Q1:** What is the primary difference between SQA and V&V?

**A1:**  
- **SQA:** Checks the **process** (was the plan followed?)
- **V&V:** Checks the **product** (does the code work correctly?)

Example: V&V verifies test results are correct. SQA verifies tests were executed per the plan.

────────────────────────────────────────────────────────────────────

**Q2:** When is tool qualification (TQL-1) required?

**A2:** When tool output is used as **DO-178C certification evidence** 
without independent verification. Example: VectorCAST coverage analyzer 
reports "100% MC/DC" → FAA relies on this → Tool must be qualified.

────────────────────────────────────────────────────────────────────

**Q3:** Why must SQA be independent from development?

**A3:** To avoid **conflict of interest**. If a developer audits their 
own work, they may overlook mistakes. Independent SQA provides objective 
process oversight.

────────────────────────────────────────────────────────────────────

**Q4:** What should SQA do if a critical PR is still open 1 week before certification?

**A4:**  
1. Escalate to management (cannot certify with open critical PRs)
2. Assess impact (can PR be deferred safely?)
3. Options: Fix immediately OR re-classify as non-critical (with justification)
4. Document decision in SAS

────────────────────────────────────────────────────────────────────

**Q5:** What is the difference between an in-process audit and a transition audit?

**A5:**  
- **In-Process:** Continuous monitoring during development (weekly/monthly)
- **Transition:** One-time check at major milestones (e.g., code complete, before release)

════════════════════════════════════════════════════════════════════

📚 **11. FURTHER READING**
═══════════════════════════

**Standards:**

📜 **RTCA DO-178C §8** (Software Quality Assurance Process)  
📜 **RTCA DO-178C §12** (Software Tool Qualification)  
📜 **ISO 9001:2015** (General quality management systems)

**Books:**

📖 *"DO-178C / ED-12C Explained"* (Chapter 8: SQA) — Leanna Rierson  
📖 *"Software Quality Assurance"* — Daniel Galin  
📖 *"Practical Guide to Software Quality Management"* — John Horch

**Training:**

🎓 **AFuzion DO-178C SQA Training** (2-day course)  
🎓 **SAE ARP4754A + DO-178C Integration** (covers SQA role)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand SQA vs. V&V difference (process vs. product)
- [ ] Memorize tool qualification levels (TQL-1 to TQL-5)
- [ ] Explain SQA independence requirements (DAL A/B/C)
- [ ] Describe audit types (in-process vs. transition)
- [ ] List SQA responsibilities (PACPT mnemonic)
- [ ] Recognize common SQA pitfalls (5 listed)

════════════════════════════════════════════════════════════════════

🎓 **MEMORABLE ANALOGIES**
═══════════════════════════

**SQA = Health Inspector**  
Checks if restaurant follows food safety procedures (not if food tastes good)

**V&V = Food Critic**  
Checks if food is delicious and correctly prepared

**Tool Qualification = Calibrating a Scale**  
Must prove the scale itself is accurate before trusting its measurements

**Independent SQA = Jury**  
Cannot have defendant's family on the jury (conflict of interest)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **SQA is NOT optional for DO-178C:**  
   All projects (DAL A-E) require SQA, just varying degrees of rigor

2️⃣ **Independence prevents bias:**  
   SQA must report outside development chain (especially DAL A/B)

3️⃣ **Tool qualification saves time:**  
   Qualified tools (TQL-1) allow automated evidence collection

4️⃣ **Audits catch mistakes early:**  
   In-process audits prevent expensive late-stage fixes

5️⃣ **SAS is your certification passport:**  
   SQA must review SAS for accuracy before FAA submission

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **COMPREHENSIVE SQA GUIDE COMPLETE**  
**Created:** January 14, 2026  
**Next Steps:** Integrate into project SQAP, customize audit checklists

════════════════════════════════════════════════════════════════════
