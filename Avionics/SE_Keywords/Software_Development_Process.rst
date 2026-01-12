🔄 **Software Development Process: DO-178C Lifecycle** (2026 Edition!)
=====================================================================

**Quick ID:** Full development lifecycle (requirements → design → code → test → verify → validate)
**Duration:** 18–24 months (realistic estimate)
**Key Phases:** 6 sequential phases with gates
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Process integrity determines certification success

---

✈️ **WHAT IS SOFTWARE DEVELOPMENT PROCESS?**
===========================================

**Software Development Process** = The complete lifecycle from initial planning to deployment:

  **6 Major Phases:**
    1️⃣ **Planning** (Months 1–3): Project setup, authority engagement
    2️⃣ **Requirements** (Months 2–5): HLRs and LLRs (high/low-level requirements)
    3️⃣ **Design** (Months 4–8): Architecture, algorithms, data flow
    4️⃣ **Implementation** (Months 6–10): Coding (HLR → LLR → Code)
    5️⃣ **Verification** (Months 9–16): Unit & integration testing
    6️⃣ **Validation** (Months 16–20): System testing, flight test
    7️⃣ **Certification** (Months 18–24): Objective evidence, TSO/certification

  **Key Concept:** Phases overlap (parallel work), but each has entry/exit criteria and SQA gates.

---

📊 **SOFTWARE DEVELOPMENT TIMELINE: DO-178C Realistic Schedule**
==============================================================

```
PHASE           MONTHS          ACTIVITIES
────────────────────────────────────────────────────────────────
Planning        1–3             Kickoff, PSAC, plans, tool selection
    (Gates: Manager approval, authority SOI#1)

Requirements    2–5             HLRs (M3), LLRs (M5), design reviews
    (Gates: HLR baseline, LLR baseline)

Design          4–8             Architecture, algorithms, DMP (design master plan)
    (Gates: Design review, design baseline)

Implementation  6–10            Coding, code reviews, CM
    (Gates: Code reviews pass, code baseline)

Verification    9–16            Unit tests, integration tests, structural coverage
    (Gates: All tests pass, coverage targets met)

Validation      16–20           System test, IFE/aircraft test, FTP (flight test plan)
    (Gates: All objectives complete, authority approval)

Certification   18–24           Objective evidence review, TSO/certification
    (Gates: FAA/EASA approval)

Total Project:  18–24 months (NOT 6–12 months!)
```

**Realistic Estimates:**
  ✅ Small project (10K lines, DAL C): 18 months
  ✅ Medium project (50K lines, DAL B): 22 months
  ✅ Large project (100K lines, DAL A): 24+ months

---

🔍 **PHASE DETAILS: What Happens Each Phase?**
=============================================

**PHASE 1: PLANNING (Months 1–3)**
─────────────────────────────────
  📋 **Entry Criteria:** Project approved, budget allocated
  
  🎯 **Key Activities:**
    • Project kickoff (authority, customer, developer alignment)
    • Define scope, schedule, budget (WBS: Work Breakdown Structure)
    • Identify DO-178C DAL (safety criticality level)
    • Create PSAC (Plan for Software Aspects of Certification)
    • Create SDP (Software Development Plan)
    • Create SQAP (SQA Plan)
    • Select tools (compiler, debugger, DOORS/Confluence for traceability)
    • Establish configuration management (CM) repository
    • Schedule authority meetings (SOI #1)

  📊 **Key Deliverables:**
    • PSAC (approved by authority, Month 2)
    • SDP, SQAP, SVP, SCMP (draft by Month 2, approved by Month 3)
    • Tool qualification plan
    • Project schedule (18–24 months realistic)

  🚪 **Exit Criteria:**
    • Authority approval (SOI #1: Stage of Involvement #1)
    • All plans approved
    • Team assembled
    • Tools procured

**PHASE 2: REQUIREMENTS (Months 2–5)**
──────────────────────────────────────
  📋 **Entry Criteria:** Plans approved, team ready
  
  🎯 **Key Activities:**
    • Derive HLRs from system specification (50–100 HLRs typical)
    • HLR review & baseline (Month 3, authority gate)
    • Derive LLRs from HLRs (200–500 LLRs typical)
    • LLR design review (PDR: Preliminary Design Review)
    • LLR baseline (Month 5, CCB approval)
    • Create verification/validation plan
    • Create test strategy document

  📊 **Key Deliverables:**
    • HLR document (50–100 requirements)
    • LLR document (200–500 requirements)
    • Traceability matrix (System ↔ HLR ↔ LLR)
    • Test strategy (how each LLR will be verified)

  🚪 **Exit Criteria:**
    • HLRs baselined, traced to system requirements
    • LLRs baselined, traced to HLRs
    • Authority review passed
    • Ready for design & coding

**PHASE 3: DESIGN (Months 4–8)**
─────────────────────────────────
  📋 **Entry Criteria:** LLRs baselined
  
  🎯 **Key Activities:**
    • Create design architecture (modules, components, data flow)
    • Design review (CDR: Critical Design Review)
    • Design master plan (DMP): detailed design for all LLRs
    • Tool qualification (if needed): demonstrate compiler/debugger correctness
    • Design baseline in CM (DOORS, Git, SVN)
    • SQA reviews all design artifacts

  📊 **Key Deliverables:**
    • Architecture document (modules, interfaces, data flow)
    • Design design specification (one per module)
    • Design master plan (DMP)
    • Tool qualification report

  🚪 **Exit Criteria:**
    • Design reviewed & approved
    • Design baseline established
    • Design traceability verified (LLR ↔ Design)
    • Ready for implementation

**PHASE 4: IMPLEMENTATION (Months 6–10)**
──────────────────────────────────────────
  📋 **Entry Criteria:** Design baselined
  
  🎯 **Key Activities:**
    • Code each LLR (developers code to design)
    • Code reviews (peer review of all code before commit)
    • Code baseline in CM (Git, SVN with version tags)
    • Create implementation summary (code map to LLRs)
    • SQA verifies code reviews complete

  📊 **Key Deliverables:**
    • Source code files (traceable to LLRs via comments)
    • Code review records (all code reviewed, approved)
    • Implementation summary (code ↔ LLR mapping)
    • CM records (version history, branching)

  🚪 **Exit Criteria:**
    • All code reviewed & approved
    • Code baselined in CM
    • Code traceability verified (LLR ↔ Code)
    • Ready for verification (unit testing)

**PHASE 5: VERIFICATION (Months 9–16)**
────────────────────────────────────────
  📋 **Entry Criteria:** Code baselined, unit tests ready
  
  🎯 **Key Activities:**
    • Unit testing (test each function/module)
    • Integration testing (test module interfaces & interactions)
    • Structural coverage analysis (prove all code paths tested)
    • Static analysis (find code quality issues: unused variables, unreachable code)
    • Code review of test cases (peer review)
    • Verification report (evidence all LLRs verified)

  📊 **Key Deliverables:**
    • Unit test results (pass/fail for each unit test)
    • Integration test results (pass/fail for each integration test)
    • Structural coverage report (% MC/DC by module)
    • Verification report (evidence of test completion)

  🚪 **Exit Criteria:**
    • All LLRs unit tested (100% of code executed)
    • Coverage targets met (DAL A/B: 100% MC/DC; DAL C: 100% decision; DAL D: 100% statement)
    • No critical/major defects remaining
    • Authority review passed (SOI #2)
    • Ready for validation (system testing)

**PHASE 6: VALIDATION (Months 16–20)**
───────────────────────────────────────
  📋 **Entry Criteria:** Verification complete, coverage targets met
  
  🎯 **Key Activities:**
    • System testing (test entire system end-to-end)
    • IFE testing (hardware/software integration on aircraft equipment)
    • Flight test (aircraft simulator or actual flight tests)
    • Validation report (evidence system meets HLRs)
    • Authority observation (FAA/EASA watching test flights)

  📊 **Key Deliverables:**
    • System test results (pass/fail for each system test case)
    • IFE test results (hardware/software integration confirmed)
    • Flight test report (aircraft testing complete, data collected)
    • Validation report (evidence HLRs/system requirements met)

  🚪 **Exit Criteria:**
    • All system tests pass
    • Flight test data acceptable
    • Authority satisfied
    • Ready for certification

**PHASE 7: CERTIFICATION (Months 18–24)**
──────────────────────────────────────────
  📋 **Entry Criteria:** Validation complete, all gates passed
  
  🎯 **Key Activities:**
    • Prepare objective evidence (all required documents for TSO)
    • Final authority review (FAA/EASA certification meeting)
    • Resolve any findings/observations
    • TSO (Technical Standard Order) or Type Certification
    • Release to production

  📊 **Key Deliverables:**
    • Objective evidence (requirements → design → code → test → validation)
    • Certification report (FAA/EASA approval)
    • TSO/Type Cert (official approval document)

  🚪 **Exit Criteria:**
    • TSO/certification received
    • Product released to production

---

📈 **PARALLEL ACTIVITIES (Happening Across Phases)**
==================================================

**SQA (Software Quality Assurance)**: Reviews at every phase gate
**Configuration Management (CM)**: Baseline & version control throughout
**Process Assurance**: Audits confirm DO-178C process compliance
**Documentation**: Records objective evidence (cumulative)
**Authority Liaison**: Regular meetings (SOI #1, SOI #2, SOI #3)

---

📊 **PHASE GATES: Entry/Exit Criteria**
======================================

| **Gate** | **Phase** | **Entry Criteria** | **Exit Criteria** |
|:---------|:----------|:------------------|:------------------|
| **Planning Gate** | 1 | Project approved | PSAC & plans approved by authority (SOI #1) |
| **HLR Gate** | 2 | Plans approved | HLRs baselined, traced to system reqs |
| **LLR Gate** | 2 | HLRs approved | LLRs baselined, design review passed |
| **Design Gate** | 3 | LLRs baselined | Design baselined, CDR passed |
| **Code Gate** | 4 | Design baselined | Code baselined, all reviews passed |
| **Verification Gate** | 5 | Code baselined | Coverage targets met, authority review (SOI #2) |
| **Validation Gate** | 6 | Verification passed | System tests pass, flight test data acceptable |
| **Certification Gate** | 7 | Validation passed | TSO/Type Cert received |

**Golden Rule:** ⚠️ Don't advance to next phase without gate approval!

---

💼 **SQA INVOLVEMENT: Quality at Every Phase**
==============================================

**Phase 1: Planning**
  🔍 SQA reviews: PSAC, SDP, SQAP, SVP completeness
  ✅ Gate decision: Approve or reject

**Phase 2: Requirements**
  🔍 SQA reviews: HLRs testability, traceability completeness
  ✅ Gate decision: Approve HLR baseline

**Phase 3: Design**
  🔍 SQA reviews: Design vs. LLRs, design reviews, tool qualification
  ✅ Gate decision: Approve design baseline

**Phase 4: Implementation**
  🔍 SQA reviews: Code review records, CM discipline, coding standards
  ✅ Gate decision: Approve code baseline

**Phase 5: Verification**
  🔍 SQA reviews: Test coverage, structural coverage, test documentation
  ✅ Gate decision: Approve verification completion

**Phase 6: Validation**
  🔍 SQA reviews: System test results, flight test data, validation report
  ✅ Gate decision: Approve validation completion

**Phase 7: Certification**
  🔍 SQA reviews: Objective evidence completeness, traceability matrix
  ✅ Gate decision: Approve certification submission

---

🎯 **KEY SUCCESS FACTORS**
==========================

✅ **Factor 1: Realistic timeline (18–24 months)**
  ❌ Mistake: "We'll do it in 6 months" (impossible)
  ✅ Right: 18–24 months (proven from 100+ aviation projects)

✅ **Factor 2: Early authority engagement**
  ❌ Mistake: Build system, show to FAA at end (late surprises)
  ✅ Right: Meet FAA/EASA in Month 2 (PSAC approval), get guidance upfront

✅ **Factor 3: Phase gates enforced**
  ❌ Mistake: Skip gate reviews, move forward anyway
  ✅ Right: Gate approval required before next phase

✅ **Factor 4: SQA involved every phase**
  ❌ Mistake: SQA only at the end (too late to fix)
  ✅ Right: SQA reviews every phase, provides feedback continuously

✅ **Factor 5: CM discipline**
  ❌ Mistake: Code changed without version control (chaos)
  ✅ Right: Every change recorded, traced, approved (audit trail)

✅ **Factor 6: Continuous traceability**
  ❌ Mistake: Create traceability matrix at end (incomplete)
  ✅ Right: Maintain traceability throughout (System ↔ HLR ↔ LLR ↔ Code ↔ Test)

---

⚠️ **COMMON MISTAKES IN SOFTWARE DEVELOPMENT PROCESS**
===================================================

❌ **Mistake 1: Overlapping phases (trying to parallelize too much)**
  Problem: Code before LLRs finalized (moving target)
  Impact: Code chases requirements; expensive rework
  Fix: Sequence phases: Planning → Requirements → Design → Implementation → Verification → Validation

❌ **Mistake 2: Skipping or minimizing planning phase**
  Problem: "We'll jump straight to coding" (only 1 month planning)
  Impact: Authority surprises in Month 9; project delays
  Fix: Allocate 3 months (Months 1–3) for planning, PSAC approval, authority engagement

❌ **Mistake 3: Inadequate requirements (HLRs & LLRs vague)**
  Problem: "Each developer interprets HLR differently"
  Impact: Code doesn't meet intent; extensive rework
  Fix: Detailed LLRs (specific, testable, traceable)

❌ **Mistake 4: Postponing verification (testing at the very end)**
  Problem: "We'll do all testing last month"
  Impact: Defects found late; no time to fix
  Fix: Verification parallel with implementation (Months 9–16 as implementation ends)

❌ **Mistake 5: Minimal SQA involvement**
  Problem: "SQA just reviews at the end"
  Impact: Quality issues discovered too late
  Fix: SQA gate reviews every phase (preventive, not just detective)

❌ **Mistake 6: Changing scope mid-project**
  Problem: "Just add this feature real quick" (Month 12)
  Impact: Timeline slips; certification delays
  Fix: Scope locked at planning gate (Month 3); changes via change control

---

🎓 **LEARNING PATH: Software Development Process**
=================================================

**Week 1: Process Overview**
  📖 Read: DO-178C Part 1 (objectives, relationships, V-model)
  📖 Study: 7 phases (planning → certification)
  🎯 Goal: Understand complete lifecycle, entry/exit criteria

**Week 2: Detailed Phases**
  📖 Study: Months 1–24 timeline (realistic schedule)
  📖 Analyze: Gate decisions, SQA involvement, CM discipline
  🎯 Goal: Understand phase sequence, dependencies, risks

**Week 3: Real Project Integration**
  📖 Case study: Real aviation project (schedule, problems, resolutions)
  💻 Review: Project schedule (Gantt chart), critical path
  🎯 Goal: Confidence in process planning, risk mitigation

---

✨ **BOTTOM LINE**
=================

**Software Development Process = V-Model lifecycle (18–24 months)**

✅ 7 phases with phase gates (Planning → Requirements → Design → Implementation → Verification → Validation → Certification)
✅ Realistic timeline (18–24 months, not 6 months)
✅ Early authority engagement (PSAC in Month 2, SOI #1 approval Month 3)
✅ SQA involved every phase (preventive quality control)
✅ Continuous traceability (System ↔ HLR ↔ LLR ↔ Code ↔ Test)
✅ Configuration management (version control, audit trail)

**Remember:** ⏱️ **Planning is not optional—it's 15% of total project time (not 5%)!** 🛡️

---

**Last updated:** 2026-01-12 | **Software Development Process: DO-178C Lifecycle**

**Key Takeaway:** 💡 **Respect the phases. Do each one thoroughly. Authority approval gates prevent last-minute surprises!** ✈️
