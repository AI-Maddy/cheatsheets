👀 **SQA (Software Quality Assurance): Independent Quality Oversight** (2026 Edition!)
====================================================================================

**Quick ID:** Independent oversight ensuring DO-178C compliance, process discipline, quality
**Role:** SQA representative reviews every phase gate
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—SQA prevents compliance failures

---

✈️ **WHAT IS SQA?**
==================

**SQA (Software Quality Assurance)** = Independent oversight function ensuring:
  ✅ **DO-178C compliance** (processes followed correctly)
  ✅ **Objective evidence** (documentation complete)
  ✅ **No shortcuts** (phase gates enforced)
  ✅ **Quality discipline** (standards maintained)

**Key Concept:** SQA is NOT testing (that's verification). SQA is auditing processes.

**SQA Responsibility:**
  "We don't test the code. We verify the PROCESS that produces the code is correct."

---

🔍 **SQA VS. VERIFICATION (Critical Distinction)**
=================================================

| **Aspect** | **Verification (Testing)** | **SQA (Process Audit)** |
|:-----------|:---------------------------|:------------------------|
| **Question** | "Does the code work?" | "Is the process correct?" |
| **Method** | Execute code, check outputs | Review processes, documents, records |
| **Example** | Unit test verifies read_adc() works | SQA verifies code review was performed for read_adc() |
| **Finding** | "Function returned wrong value" | "Code review record missing" |
| **Impact** | Bug found, fix code | Process issue found, enforce discipline |
| **Timing** | Throughout development | Every phase gate |
| **Role** | Testers, developers | Independent SQA team |

**Relationship:**
  Verification = Quality of PRODUCT (does code work?)
  SQA = Quality of PROCESS (was process followed correctly?)

---

📋 **SQA ACTIVITIES BY PHASE**
=============================

**PHASE 1: PLANNING (Month 1–3)**
─────────────────────────────────
🔍 **SQA Reviews:**
  ✓ PSAC document (complete? addresses all DO-178C sections?)
  ✓ SDP, SQAP, SVP, SCMP (plans exist? tailoring justified?)
  ✓ Tool selection (decision documented? qualifications planned?)
  ✓ Authority engagement (PSAC submitted? SOI #1 response received?)

📋 **SQA Audit Questions:**
  • Are all 12 PSAC sections complete?
  • Does SQAP define SQA activities for each phase?
  • Are project risks identified and mitigated?
  • Is authority engagement documented?

🚪 **Gate Decision:** "SQA approves planning phase" or "SQA rejects—rework required"

**PHASE 2: REQUIREMENTS (Month 2–5)**
──────────────────────────────────────
🔍 **SQA Reviews:**
  ✓ HLRs (traceable to system? testable? baselined?)
  ✓ LLRs (traceable to HLR? testable? detail correct?)
  ✓ Traceability matrix (complete? gaps?)
  ✓ HLR baseline (formal approval, configuration management?)
  ✓ Design review meeting (SQA present? findings documented?)

📋 **SQA Audit Questions:**
  • Are all HLRs traced to system requirements?
  • Is each HLR testable (not vague)?
  • Are LLRs at correct detail level (not too high, not too low)?
  • Is traceability matrix 100% complete (no floating requirements)?
  • Was design review held? Were findings resolved?

🚪 **Gate Decision:** "SQA approves HLR baseline" or "Rework required"

**PHASE 3: DESIGN (Month 4–8)**
────────────────────────────────
🔍 **SQA Reviews:**
  ✓ Design documents (architecture, design specs complete?)
  ✓ Design-to-LLR traceability (every LLR allocated to design?)
  ✓ Design reviews (CDR held? attendees? findings resolved?)
  ✓ Tool qualification plan (if needed; status?)
  ✓ Design baseline (version control, configuration management?)

📋 **SQA Audit Questions:**
  • Is design architecture documented clearly?
  • Does every LLR have design allocated to it?
  • Were design reviews held and findings documented?
  • Is design baseline formally established?
  • Are deviations from plan justified?

🚪 **Gate Decision:** "SQA approves design baseline" or "Rework required"

**PHASE 4: IMPLEMENTATION (Month 6–10)**
──────────────────────────────────────────
🔍 **SQA Reviews:**
  ✓ Code review records (all code reviewed before baseline?)
  ✓ Code review findings (all major/critical findings resolved?)
  ✓ Coding standards compliance (checked? violations documented?)
  ✓ Configuration management (code baseline in CM? change control working?)
  ✓ Traceability (code-to-LLR mapping complete?)

📋 **SQA Audit Questions:**
  • Was 100% of code reviewed (not skipped)?
  • Were code review findings resolved (not ignored)?
  • Does code follow project coding standards?
  • Is all code checked into version control?
  • Can we trace every code line to an LLR?

🚪 **Gate Decision:** "SQA approves code baseline" or "Rework required"

**PHASE 5: VERIFICATION (Month 9–16)**
────────────────────────────────────────
🔍 **SQA Reviews:**
  ✓ Test case specifications (traceable to LLR? measurable?)
  ✓ Test execution records (all tests run? results documented?)
  ✓ Structural coverage analysis (coverage targets met? tools qualified?)
  ✓ Static analysis (lint checks run? findings resolved?)
  ✓ Verification report (evidence of test completion? defects closed?)

📋 **SQA Audit Questions:**
  • Is there a test case for each LLR?
  • Were all test cases executed (not skipped)?
  • Did all tests pass (or are failures investigated/resolved)?
  • Are coverage targets met (MC/DC % correct for DAL)?
  • Are all defects closed before moving to validation?

🚪 **Gate Decision:** "SQA approves verification completion" or "Testing incomplete—gate held"

**PHASE 6: VALIDATION (Month 16–20)**
──────────────────────────────────────
🔍 **SQA Reviews:**
  ✓ System test cases (traceable to HLR? complete coverage?)
  ✓ System test results (all tests passed?)
  ✓ Flight test plan (approved? executed?)
  ✓ Flight test data (adequate? anomalies resolved?)
  ✓ Validation report (complete? objective evidence?)

📋 **SQA Audit Questions:**
  • Are all system tests documented and traced to HLRs?
  • Did system testing occur (not skipped)?
  • Was flight testing completed successfully?
  • Are all anomalies resolved (not ignored)?
  • Is validation objective evidence complete?

🚪 **Gate Decision:** "SQA approves validation completion" or "Additional testing required"

**PHASE 7: CERTIFICATION (Month 18–24)**
──────────────────────────────────────────
🔍 **SQA Reviews:**
  ✓ Objective evidence package (complete? all sections?)
  ✓ Traceability matrix (requirement → design → code → test complete?)
  ✓ Configuration management records (all baselines documented?)
  ✓ Process compliance (PSAC objectives met? all processes followed?)
  ✓ Certification readiness (authority approval likely?)

📋 **SQA Audit Questions:**
  • Is objective evidence package complete and organized?
  • Does every requirement trace all the way to test?
  • Are all configuration baselines documented?
  • Were all DO-178C processes followed (no shortcuts)?
  • Is product ready for certification authority review?

🚪 **Gate Decision:** "SQA approves certification submission" or "Gaps must be closed"

---

💼 **SQA ROLE & RESPONSIBILITIES**
================================

**SQA Team Composition:**
  👤 SQA Lead (reports to project manager, NOT development manager)
  👤 SQA Engineers (2–3, attend phase gates, conduct audits)

**Independence Requirement:**
  ⚠️ **SQA must be INDEPENDENT from development**
  ✅ SQA reports to project manager or higher
  ❌ SQA CANNOT report to development manager (conflict of interest)
  Impact: SQA can make objective gate decisions without development pressure

**SQA Responsibilities:**
  ✅ **Audit all processes** (requirements, design, code, test)
  ✅ **Attend and gate all phase reviews** (participate in go/no-go decision)
  ✅ **Enforce configuration management** (verify baselines, change control)
  ✅ **Verify objective evidence** (documentation complete? traceability OK?)
  ✅ **Issue findings** (process violations, missing evidence, quality issues)
  ✅ **Track findings to closure** (violations must be resolved before next phase)

**SQA Authority:**
  ✅ **SQA can hold gates** ("Cannot proceed until evidence complete")
  ✅ **SQA can demand rework** (if process not followed correctly)
  ✅ **SQA escalates to management** (if significant findings unresolved)
  ✅ **SQA represents authority** (at authority meetings, briefs FAA/EASA)

---

📊 **SQA AUDIT EXAMPLE: Code Review Audit**
===========================================

**Audit Question:** "Was 100% of code reviewed before baseline?"

**SQA Audit Process:**
  Step 1: Obtain list of all code files (200 files, 50K lines total)
  Step 2: Obtain code review records (spreadsheet or tool)
  Step 3: Verify: Every file listed? Every line reviewed?
  Step 4: Sample-check code (randomly select 10 files, verify review records match code)
  Step 5: Document findings

**Possible Findings:**
  🟢 **FINDING 1 (Minor):** "File xyz.c marked reviewed, but review notes dated AFTER code baseline"
    Impact: Review happened after code was locked in CM (process violation)
    Corrective Action: Re-review code, document timestamp correctly, update CM records
    SQA Decision: Finding resolved, gate proceeds

  🔴 **FINDING 2 (Major):** "3 files not listed in code review log (xyz_2.c, abc_3.c, test.c)"
    Impact: ~5K lines of code not reviewed before baseline (significant gap)
    Corrective Action: Perform code review immediately, document findings, update records
    SQA Decision: Major finding—gate HELD until resolved

  🟡 **FINDING 3 (Medium):** "Code review checklist incomplete for 8 files (missing security check)"
    Impact: Security review not performed; potential vulnerability
    Corrective Action: Complete security review for all 8 files, update records
    SQA Decision: Gate held until security review complete

**Resolution:**
  All findings resolved → SQA approves code baseline gate ✅

---

⚡ **SQA BEST PRACTICES**
=======================

✅ **Tip 1: SQA involved EVERY phase (not just at the end)**
  ❌ Mistake: "SQA will review at final certification gate"
  ✅ Right: SQA present every phase gate (planning, requirements, design, code, test)
  Impact: Problems caught early, easier to fix

✅ **Tip 2: SQA independent from development**
  ❌ Mistake: SQA reports to development manager
  ✅ Right: SQA reports to project manager or higher
  Impact: SQA can make objective gate decisions

✅ **Tip 3: SQA holds gates (authority to stop progress)**
  ❌ Mistake: "SQA makes suggestions; development can ignore"
  ✅ Right: "SQA approves or rejects gate; cannot proceed without SQA approval"
  Impact: Process discipline enforced

✅ **Tip 4: SQA findings tracked to closure**
  ❌ Mistake: "SQA finds issue; never follow up on fix"
  ✅ Right: "SQA documents finding, tracks resolution, verifies closure"
  Impact: All issues actually fixed

✅ **Tip 5: SQA provides objective evidence summary**
  ❌ Mistake: "Keep SQA findings internal"
  ✅ Right: "SQA briefs authority on compliance, objective evidence"
  Impact: Authority confidence, smooth certification

---

⚠️ **COMMON SQA MISTAKES**
=========================

❌ **Mistake 1: SQA not independent (reports to development)**
  Problem: SQA manager pressured by development to approve incomplete work
  Impact: Quality slips; certification delays
  Fix: SQA must report to project manager or higher (independent authority)

❌ **Mistake 2: SQA not involved early (only reviews at end)**
  Problem: Problems not discovered until late in project
  Impact: Major rework required, schedule delays
  Fix: SQA present every phase gate (preventive, not detective)

❌ **Mistake 3: SQA findings ignored (findings logged but not fixed)**
  Problem: "We'll fix it later" (later never comes)
  Impact: Compliance issues, certification delays
  Fix: SQA tracks findings to closure, gate held if not resolved

❌ **Mistake 4: SQA scope too narrow (only audits code, ignores other processes)**
  Problem: Requirements not reviewed, design not audited, etc.
  Impact: Major gaps (bad requirements, poor design) not caught
  Fix: SQA audits all phases (requirements → design → code → test)

❌ **Mistake 5: SQA meetings are rubber stamps (gates never actually held)**
  Problem: "SQA meeting approves everything" (gate decision meaningless)
  Impact: Process discipline erodes
  Fix: SQA genuinely evaluates gate, holds gate if criteria not met

---

🎓 **LEARNING PATH: SQA**
=========================

**Week 1: SQA Concepts**
  📖 Read: DO-178C Chapter 8 (SQA objectives and activities)
  📖 Study: SQA independence requirement, phase gate authority
  🎯 Goal: Understand SQA role and responsibilities

**Week 2: SQA Activities by Phase**
  📖 Study: Real project SQA audit plans (requirements audit, design audit, code audit)
  📖 Analyze: What does SQA check at each phase? What are findings?
  🎯 Goal: Understand SQA activities, audit focus areas

**Week 3: SQA Gate Decisions**
  💻 Case study: Project with SQA finding (code review gap); resolution
  💻 Analyze: How SQA held gate; how issue resolved
  🎯 Goal: Confidence in SQA gate authority and finding closure

---

✨ **BOTTOM LINE**
=================

**SQA = Independent process auditing ensuring DO-178C compliance**

✅ Reviews every phase (planning → certification)
✅ Independent from development (reports to project manager)
✅ Audits processes (not tests code)
✅ Attends phase gates (approves or rejects progress)
✅ Issues findings (process violations, missing evidence)
✅ Tracks findings to closure (all issues resolved)
✅ Represents authority (FAA/EASA confidence)

**Remember:** 👀 **SQA's job is to prevent embarrassment at the FAA gate!** Process discipline = certification success! 🛡️

---

**Last updated:** 2026-01-12 | **SQA: Software Quality Assurance**

**Key Takeaway:** 💡 **Good SQA finds problems in the process. No SQA finds problems at the FAA audit!** ✈️
