🔧 **Derived Requirements: Additional Safety Requirements** (2026 Edition!)
===========================================================================

**Quick ID:** Requirements added during development (not in original HLR/LLR)
**Source:** Hazard analysis, code complexity, hardware constraints
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Derived requirements ensure safety completeness

---

✈️ **WHAT ARE DERIVED REQUIREMENTS?**
====================================

**Derived Requirement** = A requirement that is added during development to ensure completeness and safety, but was NOT in the original High-Level Requirements (HLRs).

**Why Create Them?**
  During design & coding, the team discovers:
    ✅ Safety gaps ("What if ADC fails? Need error handling!")
    ✅ Interface constraints ("Modules call each other—need timeout protection!")
    ✅ Hardware limitations ("Sensor rate is 50 Hz—need buffering!")
    ✅ Algorithm complexity ("This loop could hang—need watchdog!")

  **Result:** New requirements (Derived Requirements) added to ensure safe, complete system.

**Simple Example:**
  Original HLR-201: "Software shall read altitude sensor"
  During coding, discover: "What if ADC communication fails?"
  → **Derived Requirement DR-301:** "Software shall detect ADC timeout (> 100 ms) and set altitude to invalid state"

---

🔍 **DERIVED REQUIREMENTS VS. ORIGINAL REQUIREMENTS**
====================================================

| **Aspect** | **Original HLR** | **Derived Requirement** |
|:-----------|:-----------------|:------------------------|
| **Source** | System specification | Design discovery |
| **Timing** | Month 2–3 (planning) | Month 4–8 (design/code) |
| **Example** | "Read altitude sensor" | "Handle sensor timeout" |
| **Purpose** | System-level function | Safety/completeness gap |
| **Approval** | Customer, authority | Authority (if safety-related) |
| **Process** | Traced to system req | Traced to hazard/gap analysis |

**Key Difference:** Original HLRs define what the system DOES. Derived Requirements define what the system must do to be SAFE and COMPLETE.

---

📝 **WHY DERIVED REQUIREMENTS MATTER (Safety Impact)**
===================================================

**Case 1: Missing Error Handling**
  Original HLR: "Software shall compute altitude hold error"
  Design discovers: "What if altitude sensor is invalid?"
  → DR-301: "If altitude invalid, error shall be 0 and hold mode shall disable"
  Impact: Without DR, invalid altitude → garbage error → uncontrolled climb/descent (CATASTROPHIC)

**Case 2: Race Condition**
  Original HLR: "Software shall update display every 1 second"
  Code discovers: "Display and control module share altitude variable"
  → DR-302: "Access to altitude variable shall be mutually exclusive (lock)"
  Impact: Without DR, race condition → corrupted altitude → trim command to wrong value (CRITICAL)

**Case 3: Watchdog Timer**
  Original HLR: "Software shall control aircraft trim"
  Design discovers: "Infinite loop possible in trim algorithm"
  → DR-303: "If main loop exceeds 100 ms, watchdog shall reset system"
  Impact: Without DR, infinite loop → trim motor stuck → uncontrolled aircraft (CATASTROPHIC)

---

🎯 **DERIVED REQUIREMENTS SOURCES**
==================================

**Source 1: Hazard Analysis**
  📋 Do system-level hazard analysis (ARP4754A methodology)
  📋 Identify hazardous states (sensor fails, communication loss, power loss)
  📋 Allocate mitigation to software
  📋 Create Derived Requirement for each mitigation
  Example: "If airspeed sensor fails (hazard), software shall detect and alert (DR)"

**Source 2: Design Complexity**
  📋 As design details emerge, discover complexity
  📋 Tight timing loops, race conditions, deep recursion
  📋 Allocate safety measures to address complexity
  📋 Create Derived Requirement for each measure
  Example: "If altitude update loop exceeds 50 ms, watchdog reset (DR)"

**Source 3: Hardware Constraints**
  📋 Hardware limitations emerge during integration
  📋 Sensor response time, communication delays, processor speed limits
  📋 Create Derived Requirement to accommodate hardware behavior
  Example: "If CAN message not received within 200 ms, status shall be unknown (DR)"

**Source 4: Software-Hardware Integration**
  📋 Software must interact with hardware in safe ways
  📋 Startup sequences, shutdown procedures, error recovery
  📋 Create Derived Requirements for safe interaction
  Example: "On startup, software shall initialize watchdog before enabling trim motor (DR)"

**Source 5: Code Review Findings**
  📋 Code reviews discover potential issues
  📋 Buffer overflows, uninitialized variables, missing error checks
  📋 Create Derived Requirements to address gaps
  Example: "Altitude array buffer shall not exceed 100 samples (DR)"

---

📊 **DERIVED REQUIREMENTS IN LIFECYCLE**
========================================

```
PHASE            ACTIVITY                              DERIVED REQUIREMENTS
────────────────────────────────────────────────────────────────────────────
Requirements     Create HLRs, LLRs (original)          0 DRs (none yet)
(Months 2–5)

Design           Architecture, design reviews          Discover gaps
(Months 4–8)     → Identify safety needs               Add DR-301, DR-302, DR-303, ...
                 → Hazard mitigation required
                 → Hardware constraints appear

Implementation   Code reviews, static analysis         More gaps discovered
(Months 6–10)    → Buffer overflows, race conditions   Add DR-304, DR-305, ...
                 → Recursion depth limits
                 → Initialization order issues

Verification     Unit/integration testing              Test reveals timing issues
(Months 9–16)    → Discover timing issues              Add DR-306, ...
                 → Stress testing uncovers limits      (late but critical)

Final DRs        All DRs baselined                     Total DRs: ~20–50 per project
(Month 8–12)     Merged into requirements baseline     (depends on complexity & safety)
```

**Key Point:** Derived Requirements NOT discovered at start—they EMERGE during design/code!

---

💼 **DERIVED REQUIREMENTS PROCESS**
==================================

**Step 1: Identify Gaps (During Design & Code)**
  🔍 Activities that trigger DR discovery:
    • Hazard analysis (ARP4754A)
    • Design reviews (PDR, CDR)
    • Code reviews (peer review)
    • Static analysis (lint findings)
    • Stress testing (timing limits discovered)

  📋 Question: "Is this system safe if [gap]?" If NO → Derived Requirement

**Step 2: Document Derived Requirement**
  📋 Create DR document (or add to requirements baseline)
  📋 Format: Same as HLR/LLR
    • DR-301: "If ADC communication timeout (> 100 ms), system shall set altitude to invalid"
    • Trace to source (hazard analysis, design finding, code review)
    • Testable (how will we verify?)

**Step 3: Approval**
  📋 Authority review (if safety-related)
  📋 SQA sign-off
  📋 Baseline in DOORS/Confluence (version control)

**Step 4: Design & Implement**
  📋 Allocate DR to code module
  📋 Implement error handling, timeout logic, watchdog
  📋 Code review verifies DR implementation

**Step 5: Verify**
  📋 Unit test each DR
  📋 Integration test timeout handling, error paths
  📋 Prove DR met

**Step 6: Integrate into Baseline**
  📋 Merge DR into traceability matrix
  📋 Update requirements document (version N.1)
  📋 Objective evidence: DR → Design → Code → Test

---

📋 **DERIVED REQUIREMENTS EXAMPLE: Altitude Hold Autopilot**
==========================================================

**Original HLRs (from system spec):**
  HLR-201: "Software shall read altitude sensor"
  HLR-202: "Software shall compute altitude error"
  HLR-203: "Software shall control trim motor"
  HLR-204: "Software shall display altitude"

**During Design Review, Hazard Analysis Identifies:**
  🔴 "Sensor failure → invalid altitude → uncontrolled trim → CATASTROPHIC"
  → **DR-301:** "If altitude sensor timeout (> 100 ms), altitude shall be marked invalid, error = 0, trim hold mode shall deactivate"

  🔴 "Trim motor stuck → uncontrolled aircraft → CATASTROPHIC"
  → **DR-302:** "Trim motor output shall be limited to ±25° (hardware limit); if exceeded, watchdog shall deactivate motor"

  🟡 "Display race condition → corrupted altitude → MAJOR"
  → **DR-303:** "All access to altitude variable shall be protected by mutex lock (software synchronization)"

**During Code Review:**
  🔴 "Infinite loop in error computation possible → processor hang → CATASTROPHIC"
  → **DR-304:** "Main loop execution time shall be < 100 ms; watchdog shall monitor; if exceeded, system reset"

  🟡 "Altitude buffer overflow in high-rate sampling → MAJOR"
  → **DR-305:** "Altitude samples array size = 100 max; if exceeded, oldest sample shall be discarded (ring buffer)"

**Final Derived Requirements List:**
  DR-301, DR-302, DR-303, DR-304, DR-305 (5 additional requirements)
  Total: 4 HLRs + 5 DRs = 9 requirements for altitude hold system

---

⚡ **DERIVED REQUIREMENTS BEST PRACTICES**
=========================================

✅ **Tip 1: Don't ignore gaps (identify early)**
  ❌ Mistake: "We'll ignore this issue, it won't happen"
  ✅ Right: Identify hazard, create DR to mitigate
  Impact: Prevents safety incidents

✅ **Tip 2: Trace DRs to source (hazard, design, code)**
  ❌ Mistake: "DR-301 added" (no rationale)
  ✅ Right: "DR-301 derives from Hazard #12 (sensor timeout)"
  Impact: Auditor understands necessity

✅ **Tip 3: Authority approval for safety-related DRs**
  ❌ Mistake: Add DR without authority notification
  ✅ Right: Notify authority, get approval (especially if changes safety allocation)
  Impact: Prevents certification surprises

✅ **Tip 4: Baseline DRs with formal configuration management**
  ❌ Mistake: "We added DR but didn't version it"
  ✅ Right: Baseline version 1.1 (requirements v1.0 + DR-301-305)
  Impact: Audit trail, change control

✅ **Tip 5: Test every DR (don't assume it's "obvious")**
  ❌ Mistake: "DR-301 is obviously necessary, no test needed"
  ✅ Right: Unit test timeout detection, error handling paths
  Impact: Objective evidence of DR verification

---

⚠️ **COMMON DERIVED REQUIREMENTS MISTAKES**
==========================================

❌ **Mistake 1: Too many DRs (scope creep)**
  Problem: Every minor design decision becomes a DR
  Impact: Requirements explosion (100+ DRs for 50 HLRs—sign of bad HLRs)
  Fix: DRs should be safety/completeness gaps ONLY, not every design choice

❌ **Mistake 2: DRs not traceable to source**
  Problem: "DR-301 added" (no hazard/design/code reference)
  Impact: Authority asks "Why this DR?" and you can't answer
  Fix: Every DR must trace to source (hazard analysis, code review, design issue)

❌ **Mistake 3: DRs added too late (Month 15)**
  Problem: Discover critical safety gap during verification
  Impact: Major rework, schedule impact
  Fix: Identify DRs during design (Months 4–8) and early implementation

❌ **Mistake 4: DRs not implemented**
  Problem: "We created DR-301 but didn't code it"
  Impact: Requirement not met, failed certification
  Fix: DRs must be allocated to code, reviewed, tested

❌ **Mistake 5: DRs change after baseline**
  Problem: "We'll adjust DR-301 during testing"
  Impact: Change control violation, requirements drift
  Fix: Once baselined, changes require formal approval (CCB)

---

🎓 **LEARNING PATH: Derived Requirements**
==========================================

**Week 1: Concept Understanding**
  📖 Read: DO-178C Part 1 (derived requirements definition)
  📖 Study: Why DRs exist (safety gaps from HLRs)
  🎯 Goal: Understand DR purpose and sources

**Week 2: Practical Application**
  📖 Study: Real project DRs (20–50 examples)
  📖 Analyze: DR source (hazard analysis, design finding, code review)
  🎯 Goal: Recognize when DR is needed

**Week 3: DR Creation & Verification**
  💻 Create: DRs for example system (altitude hold)
  💻 Design: How each DR will be verified (test cases)
  🎯 Goal: Confidence in DR creation and traceability

---

✨ **BOTTOM LINE**
=================

**Derived Requirements = Additional requirements discovered during design/code**

✅ Not in original HLRs (added during design & implementation)
✅ Address safety gaps, hazards, hardware constraints, complexity
✅ Emerge during design reviews, code reviews, hazard analysis
✅ Traced to source (hazard, design finding, code review)
✅ Baselined, tested, integrated into requirements
✅ Typical count: 20–50 per project (depends on complexity)

**Remember:** 🎯 **Good HLRs prevent too many DRs. Bad HLRs = DRs explosion!** Safety thinking upfront saves rework later! 🛡️

---

**Last updated:** 2026-01-12 | **Derived Requirements**

**Key Takeaway:** 💡 **Derived Requirements are NOT failures—they're discoveries! Identify them early, trace them, verify them, and move forward safely.** ✈️
