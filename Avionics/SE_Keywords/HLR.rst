📋 **HLR (High-Level Requirements): System-Derived Safety Requirements** (2026 Edition!)
========================================================================================

**Quick ID:** System requirements allocated to software (safety-critical)
**Derived From:** System specification (ARP4754A allocated requirements)
**Traceable To:** Low-Level Requirements (LLRs), design, verification tests
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—HLRs drive entire software

---

✈️ **WHAT IS AN HLR?**
======================

**HLR (High-Level Requirement)** = A software requirement that is:
  ✅ **Safety-related** (failure could impact aircraft/crew/passengers)
  ✅ **System-derived** (allocated from system specification to software)
  ✅ **Testable** (verification possible through testing, review, or analysis)
  ✅ **Traceable** (links to system requirement + design + code + test)
  ✅ **Baselined** (version controlled, change history maintained)

**Simple Example:**
  System Requirement: "Flight control system shall maintain aircraft attitude within ±10 degrees"
  Allocation: "Software must support attitude hold autopilot function"
  HLR: "Autopilot software shall read attitude sensors (pitch, roll, yaw) and compute control commands"

---

🔍 **HLR VS. LLR: Key Difference**
=================================

| **Aspect** | **HLR** | **LLR** |
|:-----------|:--------|:--------|
| **Scope** | System-level, high-level | Code-level, detailed |
| **Source** | System specification | HLR decomposition |
| **Detail** | What the system must do | How code implements it |
| **Example** | "Software shall read altitude sensor" | "Function read_altitude_adc() shall read ADC channel 3" |
| **Testable** | Via system testing | Via unit/integration testing |
| **Number** | Fewer (50–100 typical) | More (200–500 typical) |

**Relationship:** HLR → (decomposes to) → Multiple LLRs

Example:
  HLR: "Software shall compute and display altitude"
  ├─ LLR-1: "Function read_altitude_adc() shall read ADC input"
  ├─ LLR-2: "Function convert_altitude() shall apply scale factor"
  └─ LLR-3: "Function display_altitude() shall write to display device"

---

📝 **HLR CHARACTERISTICS: What Makes a Good HLR?**
================================================

**1️⃣ SAFETY-RELATED (not all software requirements are HLRs)**
  ✅ Does failure impact aircraft/crew/passengers? → HLR
  ❌ Is it purely convenience? → Not an HLR (informational only)

**2️⃣ DERIVED FROM SYSTEM (traceable source)**
  ✅ "Software shall monitor engine temperature per system spec Section 3.2.1"
  ❌ "Software should be fast" (vague, not traceable)

**3️⃣ UNAMBIGUOUS (clear, not open to interpretation)**
  ✅ "Software shall provide altitude to ±100 feet accuracy"
  ❌ "Software shall provide good altitude accuracy" (what's "good"?)

**4️⃣ TESTABLE (verification possible)**
  ✅ "Software shall read altitude within 100 ms of request"
  ❌ "Software shall be reliable" (how do you test "reliable"?)

**5️⃣ BOUNDED (defines limits, ranges, conditions)**
  ✅ "Software shall operate with ambient temperature 0–50°C"
  ❌ "Software shall operate in all conditions" (undefined)

**6️⃣ DECOMPOSABLE (to detailed requirements)**
  ✅ HLR can be broken into 2–5 LLRs
  ❌ Cannot be broken further (too detailed for HLR)

---

💼 **HLR PROCESS: Creating HLRs**
================================

**Step 1: Identify System Requirements (Month 2)**
  📋 From Aircraft Specification or System Requirements Document
  📋 Focus on safety-related requirements (criticality, hazard analysis)
  📋 Examples:
    ✅ "Altimeter shall display altitude ±100 feet"
    ✅ "Engine monitor shall alert pilot if temp > 200°C"
    ✅ "Flight control shall respond to pilot input within 50 ms"
  ➜ Output: System requirements list (50–100 items)

**Step 2: Allocate to Software (Month 2–3)**
  📋 Which system requirements → software (vs. hardware)?
  📋 Example:
    System Req: "Altimeter shall display altitude ±100 feet"
    Allocation: Part hardware (sensor), part software (processing)
    Software HLR: "Software shall read altimeter sensor and display altitude to ±100 feet"
  📋 Document traceability (system req # → HLR #)
  ➜ Output: HLR list with traceability to system requirements

**Step 3: Baseline HLRs (Month 3)**
  📋 Formal review (SFR—Software Functional Requirements Review)
  📋 Check for completeness (all system reqs covered?)
  📋 Check for unambiguity (each HLR clear, testable?)
  📋 Authority approval (FAA/EASA agrees requirements are complete)
  📋 Baseline in DOORS or Confluence (version control)
  ➜ Output: Baselined HLR list (locked, changes require formal approval)

**Step 4: Design Phase (Month 4–6)**
  📋 For each HLR, determine architecture/design
  📋 Decompose HLR → Design architecture elements
  ➜ Output: Design derived from HLRs

**Step 5: Implementation (Month 7–10)**
  📋 For each HLR, code is implemented (via LLRs)
  ➜ Output: Code traceable to HLRs

**Step 6: Verification (Month 9–18)**
  📋 For each HLR, test/review proves it works
  ➜ Output: Test results, review minutes proving HLR verification

---

📊 **HLR EXAMPLE: Altitude Hold Autopilot**
==========================================

**System Requirement (from Aircraft Specification):**
  "Autopilot shall maintain aircraft altitude within ±50 feet of target altitude"

**Allocated to Software HLRs:**
  HLR-201: "Software shall read altitude sensor input"
    • Sensor: IRS (Inertial Reference System)
    • Input: Pressure altitude (0–50,000 feet range)
    • Frequency: 50 Hz (update every 20 ms)
    • Accuracy: ±100 feet (raw sensor capability)

  HLR-202: "Software shall compute altitude error"
    • Input: Current altitude, target altitude (both in feet)
    • Output: Error (current - target)
    • Example: Current=10,000 ft, Target=10,050 ft → Error=−50 ft
    • Range: −50,000 to +50,000 feet

  HLR-203: "Software shall compute pitch control command"
    • Input: Altitude error, error trend (rate of change)
    • Output: Pitch command (−10 to +10 degrees)
    • Method: Proportional-Integral (PI) controller
    • Stability: Critically damped (no oscillation)

  HLR-204: "Software shall command elevator control surface"
    • Input: Pitch command
    • Output: Voltage to elevator servo (0–5V)
    • Mapping: −10° command → 0V, +10° command → 5V
    • Fail-safe: Loss of signal → 2.5V (neutral)

**HLR Traceability Matrix:**
  System Req: "Maintain altitude ±50 feet"
  ├─ HLR-201: Read altitude sensor
  ├─ HLR-202: Compute altitude error
  ├─ HLR-203: Compute pitch control command
  └─ HLR-204: Command elevator control
  ├─ Design: Altitude hold controller (architecture diagram)
  ├─ Code: flight_control.c (functions read_altitude, compute_error, etc.)
  └─ Test: Test-100 (verify altitude maintained ±50 feet in 50 test cases)

**Verification:**
  ✅ Test-100: 50 test cases (normal ops, edge cases, failure modes)
  ✅ Result: PASS (all cases successful, altitude maintained ±45 feet actual)
  ✅ Proof: HLR-201/202/203/204 all verified

---

⚡ **HLR BEST PRACTICES**
=======================

✅ **Tip 1: HLRs should be sparse (not detailed)**
  ❌ Mistake: 500 HLRs (too detailed, should be LLRs)
  ✅ Right: 50–100 HLRs (high-level, decompose to 200–500 LLRs)
  Impact: HLRs capture architecture, LLRs capture implementation

✅ **Tip 2: Number HLRs for traceability**
  ❌ Mistake: "Requirement: Read altitude sensor" (no ID)
  ✅ Right: "HLR-201: Read altitude sensor" (traceable ID)
  Impact: Easy to link to design, code, tests

✅ **Tip 3: Baseline HLRs early (before design)**
  ❌ Mistake: "We'll finalize HLRs during design"
  ✅ Right: HLR baseline in Month 3 (before Month 4 design phase)
  Impact: Design constrained by requirements, not vice versa

✅ **Tip 4: Link HLRs to system requirements**
  ❌ Mistake: HLRs exist in isolation
  ✅ Right: Each HLR → System requirement trace (matrix)
  Impact: Auditor verifies system requirements covered

✅ **Tip 5: Make HLRs testable**
  ❌ Mistake: "Software shall be reliable" (not testable)
  ✅ Right: "Software shall detect altitude error within 50 ms" (testable)
  Impact: Verification is objective, not subjective

---

⚠️ **COMMON HLR MISTAKES**
=========================

❌ **Mistake 1: HLRs too detailed (should be LLRs)**
  Problem: "Function read_altitude_adc() shall read ADC channel 3, 12-bit conversion"
  Impact: Too detailed for HLR; should be LLR
  Fix: HLRs stay at system level; decompose to LLRs for implementation details

❌ **Mistake 2: HLRs not traceable to system requirements**
  Problem: HLR exists without clear system requirement source
  Impact: Auditor asks "Why is this HLR required?"
  Fix: Maintain traceability matrix (HLR # ← System Req #)

❌ **Mistake 3: HLRs not testable**
  Problem: "Software shall be safe" (impossible to test)
  Impact: Cannot verify HLR (verification failure!)
  Fix: Make HLRs measurable (±100 feet, <50 ms, etc.)

❌ **Mistake 4: HLRs not baselined**
  Problem: HLRs are living document, change without control
  Impact: No stable foundation for design/code; confusion
  Fix: Baseline in DOORS (version control, change history)

❌ **Mistake 5: Too many/too few HLRs**
  Problem: 500 HLRs (too detailed) or 10 HLRs (too sparse)
  Impact: Either not enough architecture guidance or too much detail
  Fix: Target 50–100 HLRs (system-level, decompose to 200–500 LLRs)

---

🎓 **LEARNING PATH: HLRs**
==========================

**Week 1: Understanding HLRs**
  📖 Read: DO-178C Chapter 4 (requirements objectives)
  📖 Study: ARP4754A (system-level allocation)
  🎯 Goal: Understand HLR definition, purpose

**Week 2: Creating HLRs**
  📖 Study: Real project HLR document (50–100 examples)
  📖 Analyze: Traceability matrix (system → HLR → design)
  🎯 Goal: Understand HLR creation process

**Week 3: Practice**
  💻 Create: HLRs for example system (autopilot, engine monitor, etc.)
  💻 Verify: Are they testable? Traceable? At right level?
  🎯 Goal: Confidence in creating HLRs

---

✨ **BOTTOM LINE**
=================

**HLRs = System requirements allocated to software**

✅ Safety-related, system-derived, testable
✅ High-level (50–100 per project), decomposed to LLRs
✅ Baselined early (Month 3)
✅ Traceable (system → HLR → design → code → test)
✅ Reviewed & approved before design starts

**Remember:** Good HLRs = clear architecture. Vague HLRs = confused project! 📋

---

**Last updated:** 2026-01-12 | **HLR: High-Level Requirements**

**Key Takeaway:** 💡 **HLRs are your system-to-software bridge.** Write them clearly, baseline them early, trace them meticulously! 🛡️
