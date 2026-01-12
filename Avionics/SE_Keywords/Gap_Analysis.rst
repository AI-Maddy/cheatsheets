🔍 **Gap Analysis: Finding Holes in Compliance** (2026 Edition!)
==============================================================

**Quick ID:** Systematic identification of compliance shortfalls (requirements verified? coverage targets met?)
**Key Question:** "What's missing that could prevent certification?"
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Gaps prevent certification unless addressed

---

✈️ **WHAT IS GAP ANALYSIS?**
=============================

**Gap Analysis** = Systematic review to identify missing or incomplete compliance items:
  ✅ **Requirements not verified** (requirement without corresponding test)
  ✅ **Coverage targets not met** (MC/DC 95% instead of 100% for DAL A)
  ✅ **Objective evidence incomplete** (test run; results not documented)
  ✅ **Design/code quality issues** (design review findings not resolved)
  ✅ **Traceability broken** (requirement not linked to code/test)

**Purpose:** Identify issues before FAA submission; allow project to correct gaps.

**Timing:** Gap analysis performed Month 18–20 (before final certification package assembled Month 22).

**Core Question:** "If FAA reviews our evidence, will they find anything we missed?"

---

🔄 **GAP ANALYSIS PROCESS**
===========================

**Step 1: Requirements Completeness Check (Week 1)**
  🎯 Input: All requirements (HLRs + LLRs) + test results
  🎯 Process:
    1. List all requirements (HLR_001, HLR_002, ..., LLR_001.1, LLR_001.2, ...)
    2. For each requirement, ask: "Is this verified?"
    3. Check traceability matrix: Does requirement have corresponding test case?
    4. Check test results: Did test pass?
  
  🎯 Output: List of gaps (if any)
  
  📋 **Gap Analysis Example:**
    | Req ID | Requirement | Verified? | Test Case | Status | Gap? |
    |:-------|:-----------|:----|:----------|:-------|:------|
    | HLR_001 | Maintain altitude ±50 ft | YES | SYS_001 | PASS | ✓ No |
    | LLR_001.1 | Read altimeter | YES | UT_001 | PASS | ✓ No |
    | LLR_001.2 | Calculate error | YES | UT_002 | PASS | ✓ No |
    | **LLR_001.3** | **Send command** | **NO** | **None** | **N/A** | **❌ YES** |
    | **Interpretation: LLR_001.3 has no test; requires new test or design change** |

**Step 2: Coverage Targets Verification (Week 1)**
  🎯 Input: Coverage analysis reports (MC/DC, decision, statement %)
  🎯 Process:
    1. For each DAL level, check coverage targets:
       • DAL A: MC/DC 100%, Decision 100%, Statement 100%?
       • DAL B: MC/DC 100% or Decision 100%, Statement 100%?
       • DAL C: Decision 100%, Statement 100%?
       • DAL D: Statement 100%?
    2. Identify shortfalls
    3. Assess justification (if coverage < target, why acceptable?)
  
  🎯 Output: Coverage gaps (if any)
  
  📋 **Coverage Gap Analysis:**
    | Module | DAL | Coverage Target | Actual | Gap? |
    |:-------|:------|:-------|:----------|:------|
    | altitude_control.c | A | MC/DC 100% | 100% | ✓ No |
    | error_handler.c | A | MC/DC 100% | 98% | **❌ YES** |
    | command_output.c | A | MC/DC 100% | 100% | ✓ No |
    | **Gap: error_handler.c 2% uncovered; need tests for 2 MC/DC conditions** |

**Step 3: Objective Evidence Completeness (Week 2)**
  🎯 Input: All documentation (requirements, design, code, tests, reviews, approvals)
  🎯 Process:
    1. For each major artifact, verify evidence:
       • Requirements signed/approved? Yes/No
       • Design reviews documented with findings? Yes/No
       • Code reviews completed? Yes/No
       • All tests documented with results? Yes/No
       • Approvals obtained (DER, SQA)? Yes/No
    2. Identify missing evidence
  
  🎯 Output: Evidence gaps (if any)
  
  📋 **Objective Evidence Gap Analysis:**
    | Artifact | Required? | Documented? | Signed? | Gap? |
    |:---------|:----------|:-----------|:---------|:------|
    | HLR approval | YES | YES | YES | ✓ No |
    | Design review | YES | YES | YES | ✓ No |
    | **Code review** | **YES** | **NO** | **N/A** | **❌ YES** |
    | Test results | YES | YES | YES | ✓ No |
    | Coverage report | YES | YES | YES | ✓ No |
    | **Gap: Code review results not documented (need meeting minutes)** |

**Step 4: Traceability Verification (Week 2)**
  🎯 Input: Traceability matrix + all documentation
  🎯 Process:
    1. Forward traceability: Each requirement traced to design?
    2. Backward traceability: Each design traced back to requirement?
    3. Forward traceability: Each design traced to code?
    4. Backward traceability: Each code traced back to design?
    5. Forward traceability: Each code traced to test?
    6. Backward traceability: Each test traced back to code/requirement?
    7. Identify broken links
  
  🎯 Output: Traceability gaps (if any)
  
  📋 **Traceability Gap Analysis:**
    | Link | Forward ✓ | Backward ✓ | Gap? |
    |:-----|:----|:------|:------|
    | Requirement ↔ Design | YES | YES | ✓ No |
    | Design ↔ Code | YES | YES | ✓ No |
    | Code ↔ Test | **Partial** | **Partial** | **❌ YES** |
    | **Gap: 3 functions in altitude_control.c not linked to test cases** |

**Step 5: Design Quality Review (Week 2)**
  🎯 Input: Design review findings from PDR/CDR
  🎯 Process:
    1. List all design review findings (5 items identified at CDR)
    2. For each finding: Resolved or open?
    3. If open: Will it delay certification?
  
  🎯 Output: Design quality gaps (if any)
  
  📋 **Design Quality Gaps:**
    | Finding ID | Description | Status | Impact |
    |:-----------|:-----------|:----------|:----------|
    | F_001 | Interface documentation incomplete | **RESOLVED** | ✓ No |
    | F_002 | Error handling not specified | **RESOLVED** | ✓ No |
    | **F_003** | **Initialization sequence unclear** | **OPEN** | **❌ Impacts code quality** |
    | **Gap: F_003 unresolved; code may not initialize correctly** |

**Step 6: Gap Analysis Report & Action Items**
  🎯 Output: Formal gap analysis report (Gaps identified, severity, remediation plan)
  
  📋 **Gap Analysis Report Format:**
    
    **SECTION A: REQUIREMENTS VERIFICATION GAPS**
    | Gap | Severity | Remediation | Target Date |
    |:---|----|:-----------|:-----------|
    | LLR_001.3 unverified | High | Add IT_006 (integration test) | Month 19 |
    | **Total: 1 requirement gap** |
    
    **SECTION B: COVERAGE GAPS**
    | Gap | Severity | Remediation | Target Date |
    |:---|----|:-----------|:-----------|
    | error_handler.c MC/DC 98% (vs 100% target) | Medium | Add unit tests UT_023, UT_024 | Month 19 |
    | **Total: 1 coverage gap** |
    
    **SECTION C: OBJECTIVE EVIDENCE GAPS**
    | Gap | Severity | Remediation | Target Date |
    |:---|----|:-----------|:-----------|
    | Code review minutes not documented | Medium | Schedule code review; document results | Month 18 |
    | **Total: 1 evidence gap** |
    
    **SECTION D: TRACEABILITY GAPS**
    | Gap | Severity | Remediation | Target Date |
    |:---|----|:-----------|:-----------|
    | 3 functions not linked to tests | High | Link functions to tests UT_025-UT_027 | Month 19 |
    | **Total: 1 traceability gap** |
    
    **SUMMARY**
    Total gaps identified: 4
    High severity: 2 (must fix before certification)
    Medium severity: 2 (should fix before certification)
    Remediation schedule: All gaps closed by Month 19 (3 months before certification submission)

---

⚡ **GAP ANALYSIS TIMELINE**
===========================

**Month 18: Initial Gap Analysis**
  🎯 Project complete; testing finished; verification results finalized
  🎯 Perform gap analysis (identify missing requirements, coverage, evidence)
  🎯 Output: Gap analysis report with remediation plan

**Month 18–19: Remediation Phase**
  🎯 Address identified gaps (add tests, collect evidence, fix design issues)
  🎯 Close-out verifications (retest, remeasure coverage, obtain approvals)

**Month 19: Gap Analysis Review**
  🎯 Verify all gaps closed
  🎯 Update gap analysis report (status: "All gaps resolved")
  🎯 DER and SQA review gap resolution

**Month 20–22: Final Certification Preparation**
  🎯 Gaps resolved; proceed to objective evidence package assembly
  🎯 No surprises during FAA certification review (gaps identified and addressed internally)

---

💡 **GAP ANALYSIS BEST PRACTICES**
=================================

✅ **Tip 1: Gap analysis performed proactively (Month 18, not discovered by FAA Month 24)**
  ❌ Mistake: "Final certification submission; FAA asks 'Why is requirement X not verified?'"
  ✅ Right: "Month 18 gap analysis identifies uncovered requirement; add test Month 19; closed before submission"
  Impact: No certification delays; gaps addressed internally

✅ **Tip 2: Gap analysis systematic & comprehensive (checklist of all potential gaps)**
  ❌ Mistake: "Quick review; miss that 3 functions not linked to tests"
  ✅ Right: "Formal process (requirements ✓, coverage ✓, evidence ✓, traceability ✓)"
  Impact: All gaps identified; nothing missed

✅ **Tip 3: Gaps prioritized by severity (high-severity gaps address first)**
  ❌ Mistake: "Address all gaps equally; run out of time for high-severity items"
  ✅ Right: "High-severity gaps (requirement verification) prioritized; medium-severity (evidence) secondary"
  Impact: High-severity gaps closed first; certification not at risk

✅ **Tip 4: Remediation plan clear with target dates (not vague)**
  ❌ Mistake: "Gap identified; plan to fix it (no specific date)"
  ✅ Right: "Gap: LLR_001.3 unverified; Remediation: Add IT_006; Target: Month 19 Week 2"
  Impact: Clear accountability; gaps track to closure

✅ **Tip 5: Gap resolution verified independently (not self-verified)**
  ❌ Mistake: "Team fixes gap; team says 'fixed'"
  ✅ Right: "Team fixes gap; SQA independently verifies closure"
  Impact: Credible resolution; gaps truly closed

---

⚠️ **COMMON GAP ANALYSIS MISTAKES**
==================================

❌ **Mistake 1: Gap analysis deferred until late (Month 22 instead of Month 18)**
  Problem: "Discover gaps 2 months before certification; time to fix limited"
  Impact: Either gaps remain (certification blocked) or rushed fixes (poor quality)
  Fix: Gap analysis Month 18; 3 months for remediation before Month 22 submission

❌ **Mistake 2: Informal gap analysis (no systematic process; gaps missed)**
  Problem: "Quick review; miss that coverage 2% short on one module"
  Impact: FAA discovers gap; certification delayed
  Fix: Formal gap analysis process (requirements ✓, coverage ✓, evidence ✓, traceability ✓)

❌ **Mistake 3: Gaps not prioritized (spend time on minor items; major gaps ignored)**
  Problem: "Focus on low-severity evidence gaps; miss that 1 requirement unverified"
  Impact: High-severity gap discovered by FAA; certification delayed
  Fix: Prioritize gaps (high-severity requirements/coverage first)

❌ **Mistake 4: Remediation plan vague (no specific actions or dates)**
  Problem: "Gap identified; plan to fix it (no details or deadline)"
  Impact: Gaps languish; not tracked to closure
  Fix: Clear remediation plan (specific action, responsible person, target date)

❌ **Mistake 5: Gap resolution not verified (team says 'fixed'; no independent check)**
  Problem: "Team implements fix; no one verifies fix actually worked"
  Impact: Fix incomplete; gap still exists; FAA finds same gap
  Fix: Independent verification (SQA or DER verifies gap truly closed)

---

🎓 **LEARNING PATH: Gap Analysis**
=================================

**Week 1: Gap Analysis Concepts**
  📖 Read: DO-178C Section 5 (traceability), Section 8 (certification data procedures)
  📖 Study: Types of gaps (requirements, coverage, evidence, traceability)
  🎯 Goal: Understand what constitutes a gap and why important

**Week 2: Gap Analysis Process**
  📖 Study: Real project gap analysis (what gaps found, how fixed)
  📖 Analyze: Gap prioritization (severity levels, remediation plans)
  🎯 Goal: Understand gap analysis execution and remediation planning

**Week 3: Gap Closure Verification**
  💻 Case study: Project with 10 gaps identified, remediation, verification
  💻 Practice: Outline gap analysis process for hypothetical altitude hold project
  🎯 Goal: Confidence in gap identification, prioritization, and closure

---

✨ **BOTTOM LINE**
=================

**Gap Analysis = Proactive internal review to find compliance shortfalls before FAA sees them**

✅ Performed Month 18 (before final certification package)
✅ Systematic review (requirements ✓, coverage ✓, evidence ✓, traceability ✓)
✅ Gaps prioritized by severity (high-severity first)
✅ Remediation plan clear (specific actions, responsible person, target date)
✅ Resolution verified independently (SQA or DER confirms gaps closed)
✅ No surprises during FAA certification review (gaps found internally, addressed)

**Remember:** 🔍 **Gap Analysis = "Find our mistakes before FAA does!"** ✈️

---

**Last updated:** 2026-01-12 | **Gap Analysis**

**Key Takeaway:** 💡 **Good gap analysis = "Internal team finds gaps Month 18, fixes by Month 19!" Bad analysis = "FAA finds gaps Month 24, delays certification!"** 🛡️
