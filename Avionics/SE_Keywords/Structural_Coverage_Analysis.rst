🛡️ **Structural Coverage Analysis: Proof That All Code Paths Are Tested** (2026 Edition!)
============================================================================================

**Quick ID:** MC/DC, Decision, Statement coverage metrics (proving code paths tested)
**Target Metrics:** 100% MC/DC (DAL A/B), Decision (DAL C), Statement (DAL D/E)
**Tools:** VectorCAST, QualityLogic, CodeScroll, Bullseye Coverage
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Coverage = Proof that code is tested

---

✈️ **WHAT IS STRUCTURAL COVERAGE?**
===================================

**Structural Coverage** = Measurement proving that test cases exercise all code paths (conditions, decisions, statements)

Simple question: "Did our tests actually run every line of code and every branch?"

Example:
  ```c
  int check_altitude(int altitude) {
      if (altitude < 0) {              // Branch 1
          return ERROR;
      } else if (altitude > 50000) {    // Branch 2
          return ERROR;
      } else {
          return OK;                    // Branch 3
      }
  }
  ```
  
  ❌ **Bad Testing:** Only test with altitude = 1000 (normal case)
     → All branches not exercised (lines 2, 3, 6–7 never execute!)
  
  ✅ **Good Testing:** Test with:
     - altitude = -1 (triggers branch 1) ✅
     - altitude = 60000 (triggers branch 2) ✅
     - altitude = 1000 (triggers branch 3) ✅
     → Coverage = 100% (all branches executed)

---

📊 **THREE COVERAGE LEVELS: Increasing Rigor**
================================================

**1️⃣ STATEMENT COVERAGE (Simplest)**
  Definition: Every line of code executed at least once
  Target: 100%
  Example:
    ```c
    a = read_sensor();        // Line 1: Must execute ✅
    if (a > 100)              // Line 2: Must execute (branch doesn't matter)
        alert_flag = 1;       // Line 3: Must execute OR
    total = a + b;            // Line 4: Must execute (always)
    ```
  Reality: Easy to achieve (85%+ typical), misses logic errors
  **Realistic Test for Above:**
    ✅ Test 1: a = 50 (if condition FALSE, but all lines execute)
    ✅ Coverage: 100% statement ✅

  **Problem:** Doesn't test if condition is TRUE! (missing branch)

---

**2️⃣ DECISION COVERAGE (Intermediate)**
  Definition: Every decision (if/else) evaluates both TRUE and FALSE
  Target: 100%
  Example:
    ```c
    if (altitude < 10000) {        // Decision: TRUE or FALSE?
        climb_rate = 500;          // Must execute for TRUE case
    } else {
        climb_rate = 100;          // Must execute for FALSE case
    }
    ```
  Reality: Catches missing branches (~50% harder than statement)
  **Realistic Test for Above:**
    ✅ Test 1: altitude = 5000 (condition TRUE, climb_rate = 500)
    ✅ Test 2: altitude = 15000 (condition FALSE, climb_rate = 100)
    ✅ Coverage: 100% decision ✅

  **Advantage:** Tests both branches of decision

  **Problem:** Doesn't test if individual conditions affect outcome independently!
    Example: `if ((a > 100) AND (b < 50))` — Decision coverage doesn't verify each condition affects result.

---

**3️⃣ MODIFIED CONDITION/DECISION COVERAGE (MC/DC) — Most Rigorous**
  Definition: Every condition independently affects decision outcome
  Target: 100% (required for DAL A/B)
  
  Example:
    ```c
    if ((altitude > 10000) AND (climb_rate > 500)) {
        //     Condition 1         Condition 2
        alert_user();
    }
    ```
  
  MC/DC requires: Each condition causes decision to change (independently)
  
  **Test Cases Needed:**
    ✅ altitude > 10000 = TRUE,  climb_rate > 500 = TRUE   → alert (BOTH true)
    ✅ altitude > 10000 = FALSE, climb_rate > 500 = TRUE   → no alert (alt false)
    ✅ altitude > 10000 = TRUE,  climb_rate > 500 = FALSE  → no alert (climb false)
    ✅ altitude > 10000 = FALSE, climb_rate > 500 = FALSE  → no alert (BOTH false)
  
  MC/DC proof:
    - Change condition 1 (TRUE→FALSE while keeping cond2=TRUE) → decision changes ✅
    - Change condition 2 (TRUE→FALSE while keeping cond1=TRUE) → decision changes ✅
    → Each condition independently affects outcome = MC/DC satisfied!
  
  Reality: Very rigorous (~40% effort), proves deep logic correctness
  **Coverage by DAL:**
    - DAL A/B: 100% MC/DC required (most stringent)
    - DAL C: Decision coverage OK
    - DAL D/E: Statement coverage OK

---

📊 **COVERAGE TARGETS BY DAL**
==============================

| **DAL** | **Coverage Type** | **Target** | **Effort** | **Risk** |
|:--------|:-----------------|:----------|:----------|:---------|
| **A** | MC/DC | 100% ✅ | Very High | Low (comprehensive) |
| **B** | MC/DC | 100% ✅ | Very High | Low (comprehensive) |
| **C** | Decision | 100% ✅ | High | Medium (misses condition effects) |
| **D/E** | Statement | 100% ✅ | Medium | High (misses branches) |

---

🛠️ **COVERAGE TOOLS: How to Measure**
======================================

**Popular Avionics Tools:**

🥇 **VectorCAST (Most Common)**
  ✅ Purpose: Unit testing + structural coverage analysis
  ✅ Features: MC/DC measurement, test case generation, compliance reporting
  ✅ Avionics: 60%+ of projects use VectorCAST
  ✅ Cost: Expensive (~$50K+ setup, $15K/year maintenance)

🥈 **QualityLogic (Specialized Coverage)**
  ✅ Purpose: Deep coverage analysis, report generation
  ✅ Features: MC/DC analysis, coverage gaps identification
  ✅ Avionics: Growing adoption (especially for DO-178C)
  ✅ Cost: Moderate (~$20K setup)

🥉 **CodeScroll**
  ✅ Purpose: Coverage measurement tool
  ✅ Features: Statement, decision, MC/DC measurement
  ✅ Cost: Moderate

**Open Source Options:**
  📖 Bullseye Coverage (C++)
  📖 LLVM Coverage (LLVM compiler toolchain)
  📖 GCC Coverage (gcc --coverage flag)
  ⚠️ **Note:** Open source acceptable for DO-178C, but needs tool qualification (DO-330)

---

⚙️ **COVERAGE ANALYSIS PROCESS**
================================

**Step 1: Define Coverage Targets (Month 2–3)**
  📋 Know your DAL (determines coverage: MC/DC, Decision, or Statement)
  📋 Set targets: 100% for DAL A/B, decision for C, statement for D/E
  📋 Document in Verification Plan
  ➜ Output: Coverage targets documented

**Step 2: Select Coverage Tools (Month 2–4)**
  📋 Evaluate tools (VectorCAST, QualityLogic, others)
  📋 Choose tool(s)
  📋 Plan tool qualification (if needed per DO-330)
  ➜ Output: Tools selected, qualification plan started

**Step 3: Integrate into Build Process (Month 5–6)**
  📋 Configure tool in build pipeline
  📋 Automated at every build: code changes → coverage analysis
  📋 Set up reporting (metrics dashboard, thresholds)
  ➜ Output: Continuous coverage measurement

**Step 4: Analyze & Fill Gaps (Months 9–16)**
  📋 Run tests, measure coverage
  📋 Identify gaps (code paths not exercised)
  📋 Write targeted test cases to fill gaps
  📋 Iterate until 100% achieved
  ➜ Output: 100% coverage achieved (or gaps justified)

**Step 5: Document & Review (Month 17–18)**
  📋 Generate coverage report (proof of 100%)
  📋 Review in Verification Review Meeting (FVR)
  📋 Sign-off: "Coverage targets met"
  ➜ Output: Coverage proof documented, approved

---

💡 **COVERAGE BEST PRACTICES**
=============================

✅ **Tip 1: Automate coverage analysis (don't do manually)**
  ❌ Mistake: "We'll measure coverage by code review"
  ✅ Right: VectorCAST runs at every build (automated, objective)
  Impact: Coverage gaps discovered immediately (not at end)

✅ **Tip 2: Understand MC/DC complexity (don't underestimate)**
  ❌ Mistake: "We'll achieve 100% MC/DC in 1 week"
  ✅ Right: Plan 40% of testing effort for MC/DC (it's rigorous!)
  Impact: Schedule realistic, team prepared

✅ **Tip 3: Design for testability (easier coverage achievement)**
  ❌ Mistake: "This code path is 'unreachable' — can't test it"
  ✅ Right: Design code so all paths testable (simple logic, clear flow)
  Impact: MC/DC easier to achieve, code quality higher

✅ **Tip 4: Document coverage gaps with justification**
  ❌ Mistake: "We have 94% MC/DC" (6% unexplained)
  ✅ Right: "94% MC/DC achieved; 6% is error handling for 'impossible' condition (justified by design)"
  Impact: Auditor can verify gap is acceptable

✅ **Tip 5: Use coverage reports for verification review**
  ❌ Mistake: "We tested the software" (no proof)
  ✅ Right: "Coverage report shows 100% MC/DC achieved" (objective proof)
  Impact: Auditor trusts verification completeness

---

⚠️ **COMMON COVERAGE MISTAKES**
===============================

❌ **Mistake 1: Confusing coverage levels**
  Problem: "We need 100% MC/DC" (but only DAL C, requires decision)
  Impact: Wasted effort on unnecessary rigor
  Fix: Know your DAL targets (MC/DC for A/B, decision for C, statement for D/E)

❌ **Mistake 2: Coverage deferred to end**
  Problem: "We'll measure coverage in Phase 5"
  Impact: Discovering gaps late (expensive rework)
  Fix: Continuous coverage analysis (at every build)

❌ **Mistake 3: Untestable code by design**
  Problem: "This error handling is unreachable"
  Impact: Can't achieve required coverage (design flaw!)
  Fix: Redesign for testability upfront

❌ **Mistake 4: Accepting low coverage without justification**
  Problem: "We have 87% MC/DC"
  Impact: Auditor asks "Why not 100%?" with no answer
  Fix: Either achieve 100% or document gap justification

❌ **Mistake 5: Coverage tool qualification ignored**
  Problem: "We'll use open-source coverage tool"
  Impact: Auditor asks "Is tool qualified per DO-330?"
  Fix: Plan tool qualification upfront (if required for your DAL)

---

📊 **QUICK REFERENCE: Coverage by Code Type**
==============================================

| **Code Type** | **Coverage Challenge** | **MC/DC Strategy** |
|:--------------|:----------------------|:------------------|
| **Simple if/else** | Low (1 condition) | Easy: test TRUE & FALSE |
| **Complex boolean** | High (multiple conditions) | Hard: test condition combinations |
| **Loop logic** | High (boundary conditions) | Hard: test loop entry/exit/middle |
| **Error handling** | Very High (rare paths) | Hard: inject faults to test |
| **State machines** | Very High (many states) | Hard: test state transitions |

---

✨ **BOTTOM LINE**
=================

**Structural coverage = Objective proof that tests exercise all code.**

✅ Three levels: Statement (simplest) → Decision → MC/DC (most rigorous)
✅ Coverage target depends on DAL (100% MC/DC for A/B, decision for C, statement for D/E)
✅ Use automated tools (VectorCAST, QualityLogic) for objective measurement
✅ Continuous analysis (at every build) = gaps found early
✅ Document targets, results, and justifications for audit

**Remember:** High coverage doesn't guarantee correct code, but low coverage guarantees missing bugs! 📊

---

**Last updated:** 2026-01-12 | **Structural Coverage Analysis**

**Key Insight:** 💡 **Coverage = Proof, not luck.** Measure it, analyze gaps, fill them methodically! ✅
