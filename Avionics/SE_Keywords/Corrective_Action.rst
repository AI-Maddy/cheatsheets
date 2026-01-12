🔧 **Corrective Action: Fixing Problems** (2026 Edition!)
=========================================================

**Quick ID:** Structured process for identifying, analyzing, and resolving project problems
**Key Process:** Problem → Root Cause → Fix → Verification → Closure
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Problems ignored = certification delayed or blocked

---

✈️ **WHAT IS CORRECTIVE ACTION?**
=================================

**Corrective Action (CA)** = Structured problem resolution process:
  ✅ **Identify** problem (test failure, defect found, requirement unclear, gap discovered)
  ✅ **Analyze** root cause (why did this happen? design issue? test inadequate? requirement ambiguous?)
  ✅ **Plan correction** (what fix will resolve it? rework, retest, clarification?)
  ✅ **Implement fix** (execute the correction)
  ✅ **Verify closure** (problem truly resolved? independent verification)
  ✅ **Document** (problem record, fix, verification, closure date)

**Opposite:** Discover problem; fix silently; don't track → Problem re-occurs or hidden from authority.

**Key Principle:** "Identify issues fast; fix promptly; track to closure."

---

🔄 **CORRECTIVE ACTION LIFECYCLE**
=================================

**Phase 1: Problem Identification (Trigger)**
  🚨 **When discovered:**
    • Test failure during unit/integration/system testing
    • Code review identifies defect
    • Design review raises concern
    • Gap analysis finds uncovered requirement
    • FAA/DER identifies issue
    • SQA audit finds process deficiency

  📋 **Problem Record Created:**
    • Problem ID (CA_001)
    • Description (altitude calculation error; result off by 50 feet in test case 3)
    • Component affected (altitude_control.c)
    • Date discovered (Month 10)
    • Discoverer (Test Engineer, John Smith)
    • Severity (High—affects DAL A requirement)

**Phase 2: Root Cause Analysis**
  🔍 **What to analyze:**
    • Why did problem occur? (design defect, coding error, test inadequate?)
    • How did this escape detection? (review insufficient? testing gaps?)
    • Could this affect other components? (are there similar issues elsewhere?)

  📋 **Example Root Cause Investigation:**
    ```
    Problem: Altitude calculation error (50-foot error in test)
    
    Test Details:
      Input: altitude = 10,000.0 feet (double precision)
      Expected: error = 0 (target = 10,000)
      Actual: error = 50.0 feet
    
    Investigation:
      Code Review: calc_error() function
        error = target - actual
        error = 10,000 - 10,050 = -50 ✓ Correct mathematically
      
      But test shows +50, not -50. Issue found:
        Code comment says "error = target - actual"
        But actual code: error = actual - target
        Code does NOT match comment
    
    Root Cause: Design/code mismatch
      - Design says error = target - actual
      - Code implements error = actual - target
      - Wrong sign in calculation
    ```

  💡 **Root Causes (Categories):**
    • Design defect (specification incorrect or incomplete)
    • Coding error (implementation doesn't match design)
    • Test inadequate (test doesn't verify requirement fully)
    • Requirement ambiguous (unclear what should be built)
    • Process violation (review skipped, configuration management not followed)

**Phase 3: Corrective Action Plan**
  📋 **Plan documented:**
    • Problem ID (CA_001)
    • Root cause (Design/code mismatch: error calculation sign wrong)
    • Corrective action (Fix code: change "error = actual - target" to "error = target - actual")
    • Verification plan (Retest with same test case; verify error = 0 for target = actual)
    • Target completion date (Month 10, Week 2)
    • Responsible person (Developer, Jane Doe)

  🎯 **Fix Options:**
    • Option 1: Fix code (most likely)
    • Option 2: Fix design (if design truly wrong)
    • Option 3: Fix requirement (if requirement misunderstood)
    • Option 4: Fix test (if test case incorrect)

**Phase 4: Corrective Action Implementation**
  🔨 **Fix applied:**
    • Code changed: `error = target - actual` (corrected from `error = actual - target`)
    • Code review of fix (peer reviews change)
    • Change management: Commit to version control (v1.2), mark as fix for CA_001
    • Testing: Rerun test case with fix
    • Result: Test PASSES (error = 0 as expected)

  📋 **Implementation Record:**
    • Problem ID (CA_001)
    • Fix applied (Code line 42: changed to "error = target - actual")
    • Version affected (v1.2)
    • Date fixed (Month 10, Oct 8)
    • Person responsible (Jane Doe, Developer)

**Phase 5: Verification & Closure**
  ✅ **Verification steps:**
    1. Retest original failure case → PASS (problem solved)
    2. Check for side effects (does fix break other functionality?) → No issues
    3. Check for similar issues (are there other calculations with same error?) → Code review finds none
    4. Independent verification (SQA reviews fix; verifies adequate) → Approved

  ✅ **Problem formally closed:**
    • Problem ID (CA_001)
    • Status (CLOSED)
    • Date closed (Month 10, Oct 9)
    • Closure verification (Test PASS; SQA approved)
    • Lessons learned (Design and code mismatch must be caught in code review; add checklist item)

---

📋 **CORRECTIVE ACTION RECORD TEMPLATE**
======================================

```
═══════════════════════════════════════════════════════════════════════════
CORRECTIVE ACTION RECORD
═══════════════════════════════════════════════════════════════════════════

Problem ID: CA_001
Date Opened: 2025-10-08
Status: CLOSED / OPEN / IN-PROGRESS
Severity: High 🔴 / Medium 🟡 / Low 🟢

PROBLEM DESCRIPTION
───────────────────
Component: altitude_control.c
Title: Altitude calculation returns wrong sign
Description: Test UT_003 expects error = 0 when target = actual, but actual = +50
  Input: target = 10,000 ft, altitude = 10,000 ft
  Expected: error = 0
  Actual: error = +50
  Impact: Altitude hold function calculates error incorrectly; affects DAL A requirement

ROOT CAUSE ANALYSIS
──────────────────
Root Cause: Design/code mismatch
  Design specifies: error = target - actual
  Code implements: error = actual - target
  Wrong sign in calculation

Contributing factors:
  • Code not reviewed against design during code review
  • Test case not executed until late (Month 10)
  • Comments in code don't match implementation

CORRECTIVE ACTION PLAN
─────────────────────
Corrective Action: Change line 42 in altitude_control.c
  FROM: error = actual - target;
  TO:   error = target - actual;

Verification: Retest UT_003 and UT_004 (altitude error tests)
  Expected: Both tests PASS
  Side-effect check: Run full unit test suite; verify no regressions

Target Completion: 2025-10-12
Responsible: Jane Doe (Developer)
SQA Verification: John Smith (SQA Lead)

CORRECTIVE ACTION IMPLEMENTATION
───────────────────────────────
Implementation Date: 2025-10-10
Implemented By: Jane Doe
Code Version: v1.2 (git commit 3f7d8c2)
Description of Fix: Changed error calculation line 42; matches design spec

Verification Date: 2025-10-10
Verified By: John Smith (SQA)
Verification Results:
  • UT_003: PASS (error = 0 when target = actual) ✓
  • UT_004: PASS (error = -50 when target = 10,000 - 50) ✓
  • Regression testing: All 45 unit tests PASS ✓
  • Code review of fix: Approved ✓

CLOSURE DOCUMENTATION
────────────────────
Status: CLOSED
Closure Date: 2025-10-11
Lessons Learned:
  1. Design/code mismatch must be caught in code review
     Action: Add checklist item "Verify code matches design comments"
  2. Test early to find issues before they propagate
     Action: Move unit testing to Month 6 (currently Month 8)
  3. Altitude error calculation is critical; needs additional review
     Action: Schedule dedicated code review of all calculation functions

Follow-up: Monitor for similar issues in other modules

═══════════════════════════════════════════════════════════════════════════
```

---

📊 **CORRECTIVE ACTION METRICS & TRACKING**
===========================================

**CA Metrics (Monitored Throughout Project)**

| Metric | Month 8 | Month 12 | Month 16 | Target |
|:-------|:-----------|:-----------|:-----------|:--------|
| Open CAs | 5 | 2 | 0 | 0 |
| In-Progress CAs | 2 | 1 | 0 | 0 |
| Closed CAs | 0 | 4 | 7 | All |
| Average Closure Time | N/A | 8 days | 5 days | < 7 days |
| High-Severity CA Closure Time | N/A | 3 days | 2 days | < 3 days |

**Status Dashboard:**
  🟢 Green: All CAs on track for closure
  🟡 Yellow: 1+ CA at risk (closure date approaching)
  🔴 Red: High-severity CA overdue (escalate immediately)

---

⚡ **CORRECTIVE ACTION BEST PRACTICES**
====================================

✅ **Tip 1: Act fast on problems (identify, analyze, fix—days, not weeks)**
  ❌ Mistake: "Defect found Month 8; fix planned for Month 12"
  ✅ Right: "Defect found Month 8; fix implemented and verified Month 8 Week 2"
  Impact: Issues resolved immediately; don't block other work

✅ **Tip 2: Root cause analysis before rushing to fix (understand why, not just fix what)**
  ❌ Mistake: "Test fails; change code random values until it passes"
  ✅ Right: "Test fails; analyze why; understand root cause; fix properly"
  Impact: Fix is lasting; won't re-occur in similar code

✅ **Tip 3: Corrective action tracked formally (CA record, not just verbal fix)**
  ❌ Mistake: "Developer fixes defect; tells tester verbally; no documentation"
  ✅ Right: "Problem record created; fix documented; verification recorded"
  Impact: Clear audit trail; closure verifiable by FAA

✅ **Tip 4: All CAs tracked to completion (can't leave open CAs at certification)**
  ❌ Mistake: "Problem found Month 10; still open at Month 22 certification"
  ✅ Right: "All CAs closed by Month 20; certification with zero open CAs"
  Impact: No surprises at FAA review; certification credible

✅ **Tip 5: Lessons learned captured (prevent similar issues in future)**
  ❌ Mistake: "Same type of error found in 3 components (no learning)"
  ✅ Right: "Error found; root cause analyzed; similar areas reviewed proactively"
  Impact: Quality improves; fewer issues in project

---

⚠️ **COMMON CORRECTIVE ACTION MISTAKES**
======================================

❌ **Mistake 1: Problems silently fixed (no tracking, no verification)**
  Problem: "Defect found; developer fixes; no formal problem record"
  Impact: FAA can't verify fix was proper; may discover same issue again
  Fix: Formal CA process (problem record, root cause, verification, closure)

❌ **Mistake 2: Quick fix without root cause analysis (treat symptom, not disease)**
  Problem: "Test fails; change value until test passes; don't understand why"
  Impact: Fix is superficial; issue re-occurs in different context
  Fix: Analyze root cause first; understand problem; fix properly

❌ **Mistake 3: Corrective actions left open at certification (no closure)**
  Problem: "Problem found Month 10; fix planned Month 30; open at certification"
  Impact: FAA sees open CAs; certification delayed (can't have open issues)
  Fix: All CAs closed before Month 22 certification submission

❌ **Mistake 4: No independent verification of fix (developer says it's fixed)**
  Problem: "Developer says fix works; no one else verifies"
  Impact: Fix may be incomplete; similar issue found later
  Fix: Independent verification (SQA or peer review confirms fix adequate)

❌ **Mistake 5: No lessons learned (same error repeats in other places)**
  Problem: "Same error found in 3 components (no process improvement)"
  Impact: Quality doesn't improve; repeat errors waste time/schedule
  Fix: Analyze root cause; fix similar issues proactively; improve processes

---

🎓 **LEARNING PATH: Corrective Action**
=====================================

**Week 1: Corrective Action Concepts**
  📖 Read: DO-178C Section 6 (problem reporting), DO-254 Section 5 (similar processes)
  📖 Study: CA lifecycle (identify → analyze → fix → verify → close)
  🎯 Goal: Understand corrective action purpose and process

**Week 2: Root Cause Analysis**
  📖 Study: Real project CAs (problems, root causes, fixes)
  📖 Analyze: Root cause techniques (5-Why, fishbone diagram)
  🎯 Goal: Understand how to analyze problems systematically

**Week 3: CA Tracking & Metrics**
  💻 Case study: Project CA tracking (open/closed, trends, metrics)
  💻 Practice: Create CA record for hypothetical problem
  🎯 Goal: Confidence in problem identification, analysis, and closure

---

✨ **BOTTOM LINE**
=================

**Corrective Action = Structured process for identifying, analyzing, and resolving problems**

✅ Fast identification (problem discovered immediately)
✅ Root cause analysis (understand why, not just fix what)
✅ Fix properly (address root cause, not just symptom)
✅ Verify closure (independent verification, not self-verification)
✅ Track formally (CA records created, tracked to closure)
✅ No open CAs at certification (all problems resolved before submission)

**Remember:** 🔧 **CA = "Problem → Analysis → Fix → Verification → Closure!"** ✈️

---

**Last updated:** 2026-01-12 | **Corrective Action**

**Key Takeaway:** 💡 **Good CA process = "Problems resolved fast, lessons learned, quality improves!" Bad process = "Problems silently fixed, same errors repeat!"** 🛡️
