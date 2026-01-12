🔧 **LLR (Low-Level Requirements): Detailed Software Requirements** (2026 Edition!)
==================================================================================

**Quick ID:** Detailed software requirements (decomposed from HLRs)
**Derived From:** High-Level Requirements (HLRs)
**Traceable To:** Code (design-to-code linkage)
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—LLRs drive code implementation

---

✈️ **WHAT IS AN LLR?**
======================

**LLR (Low-Level Requirement)** = A detailed software requirement that is:
  ✅ **Derived from HLR** (decomposition of high-level requirement)
  ✅ **Design-level detail** (describes what code must do, not how)
  ✅ **Testable** (unit testing or code review can verify)
  ✅ **Traceable** (links to HLR, design, code, unit test)
  ✅ **Implementation-focused** (guides coder toward implementation)

**Simple Example:**
  HLR: "Software shall read altitude sensor"
  LLR-501: "Function read_altitude_adc() shall read ADC input from channel 3"
  LLR-502: "Function convert_altitude() shall apply scale factor 0.5 feet/LSB"
  LLR-503: "Function validate_altitude() shall check range 0–50,000 feet"

---

🔍 **HLR VS. LLR: Clear Distinction**
====================================

| **Aspect** | **HLR** | **LLR** |
|:-----------|:--------|:--------|
| **Source** | System specification | HLR decomposition |
| **Detail Level** | System-level architecture | Code-level implementation |
| **Example** | "Read altitude sensor" | "Function read_altitude_adc() shall read ADC channel 3" |
| **Quantity** | 50–100 per project | 200–500 per project |
| **Verification** | System testing, reviews | Unit testing, integration testing |
| **Audience** | Architects, customers | Developers, testers |
| **Decomposition** | 1 HLR → 2–5 LLRs | LLR → code (implementation) |

**Relationship:**
  ```
  System Requirement (10 items)
  ↓
  HLR (50 items)
  ↓
  LLR (300 items)
  ↓
  Code (3,000 lines)
  ```

---

📝 **LLR CHARACTERISTICS: What Makes Good LLRs?**
================================================

**1️⃣ DERIVED FROM HLR (traceable source)**
  ✅ "LLR-501 derived from HLR-201 (read altitude sensor)"
  ❌ "LLR-501: Read altitude" (no HLR source, floating requirement)

**2️⃣ UNAMBIGUOUS (clear, specific, no interpretation needed)**
  ✅ "Function read_altitude_adc() shall read ADC input from channel 3, return 12-bit unsigned value"
  ❌ "Function shall read altitude sensor" (which sensor? which data type?)

**3️⃣ TESTABLE (verification possible)**
  ✅ "Function shall return value 0–4095" (testable: check outputs for inputs 0, 4095)
  ❌ "Function shall be fast" (not testable: what is "fast"?)

**4️⃣ IMPLEMENTATION-FOCUSED (guides code design)**
  ✅ "Altitude error = current_altitude − target_altitude (both feet)"
  ❌ "Compute error correctly" (vague, no guidance)

**5️⃣ BOUNDED (specifies limits, ranges, types)**
  ✅ "Altitude range: 0–50,000 feet (unsigned 16-bit)"
  ❌ "Altitude can be any value" (unbounded)

**6️⃣ INDEPENDENT (one function per LLR, ideally)**
  ✅ "LLR-501: Read ADC input" (single function)
  ✅ "LLR-502: Convert ADC to feet" (another function)
  ❌ "LLR-501: Read ADC, convert, validate, display" (too much in one LLR)

---

💼 **LLR PROCESS: Creating LLRs**
===============================

**Step 1: HLRs Baselined (Month 3)**
  📋 Prerequisites: HLRs exist, reviewed, approved
  ➜ Ready for LLR decomposition

**Step 2: Decompose HLRs → LLRs (Month 4–5)**
  📋 For each HLR, determine design-level requirements
  📋 Estimate 2–5 LLRs per HLR (typical)
  📋 Example:
    HLR-201: "Software shall read altitude sensor"
    ├─ LLR-501: "Function read_altitude_adc() shall read ADC channel 3"
    ├─ LLR-502: "Function convert_altitude() shall apply scale factor"
    └─ LLR-503: "Function validate_altitude() shall check range"
  📋 Number LLRs (LR-001, LR-002, etc.) for traceability
  ➜ Output: LLR list with HLR traceability

**Step 3: Design Review (Month 5)**
  📋 Design Review Meeting (PDR or CDR)
  📋 Check: Are LLRs complete? Traceable? At right detail level?
  📋 Verify: LLRs guide implementation (developers understand what to code)
  ➜ Output: Approved LLRs

**Step 4: Baseline LLRs (Month 5)**
  📋 Lock LLRs in DOORS or Confluence (version control)
  📋 Changes require formal approval (change control board)
  ➜ Output: Baselined LLR list

**Step 5: Implementation (Month 6–10)**
  📋 Developers implement each LLR as function/method
  📋 Code traceable to LLR (via comments or tool)
  ➜ Output: Code files with LLR references

**Step 6: Unit Testing (Month 9–16)**
  📋 Test cases derived from LLRs
  📋 Each LLR → one or more unit tests
  ➜ Output: Unit tests proving each LLR works

---

📊 **LLR EXAMPLE: Altitude Processing**
======================================

**HLR-201: "Software shall read altitude sensor"**

**Decomposed to LLRs:**

LLR-501: **Read ADC Input**
  Input: ADC channel 3
  Output: 12-bit unsigned integer (0–4095)
  Function: `uint16_t read_altitude_adc(void)`
  Constraints:
    • Must read within 20 ms (50 Hz sampling rate)
    • Must return raw ADC value (no processing)
  Unit Test:
    • Test 1: CALL read_altitude_adc() multiple times → consistent values ✅
    • Test 2: Inject known voltage → verify ADC reads correspond correctly ✅

LLR-502: **Convert ADC to Altitude Feet**
  Input: ADC value (0–4095)
  Output: Altitude in feet (0–50,000)
  Function: `uint16_t convert_adc_to_feet(uint16_t adc)`
  Formula: `altitude_feet = adc * 0.5` (scale factor 0.5 feet/LSB)
  Constraints:
    • Scale factor 0.5 feet per LSB
    • Range: 0–2,048 feet (only lower range, sensor limited)
  Unit Tests:
    • Test 1: ADC=0 → altitude=0 feet ✅
    • Test 2: ADC=4095 → altitude=2,048 feet ✅
    • Test 3: ADC=2048 → altitude=1,024 feet ✅

LLR-503: **Validate Altitude Range**
  Input: Altitude in feet (from convert function)
  Output: Status (VALID or INVALID)
  Function: `uint8_t validate_altitude(uint16_t altitude)`
  Constraints:
    • Valid range: 0–50,000 feet
    • Invalid: < 0 or > 50,000 (impossible with unsigned int, but check anyway)
  Unit Tests:
    • Test 1: altitude=1000 → VALID ✅
    • Test 2: altitude=0 → VALID (boundary) ✅
    • Test 3: altitude=50000 → VALID (boundary) ✅
    • Test 4: altitude=50001 → INVALID (out of range) ✅

LLR-504: **Display Altitude**
  Input: Altitude in feet (validated)
  Output: Display update (pushes to display device)
  Function: `void display_altitude(uint16_t altitude)`
  Constraints:
    • Format: "Altitude: 12345 ft" (5-digit, feet suffix)
    • Update frequency: 1 Hz (once per second)
  Unit Test:
    • Test 1: Call display_altitude(1234) → verify display shows "1234 ft" ✅

---

🔗 **TRACEABILITY: HLR → LLR → Code → Test**
==============================================

```
HLR-201: "Read altitude sensor"
│
├─ LLR-501: Read ADC input
│  ├─ Code: flight_control.c, function read_altitude_adc() (lines 45–50)
│  └─ Test: test_100.c, test_read_adc() (verified ✅)
│
├─ LLR-502: Convert to feet
│  ├─ Code: flight_control.c, function convert_adc_to_feet() (lines 52–55)
│  └─ Test: test_100.c, test_convert_adc() (verified ✅)
│
├─ LLR-503: Validate range
│  ├─ Code: flight_control.c, function validate_altitude() (lines 57–60)
│  └─ Test: test_100.c, test_validate_altitude() (verified ✅)
│
└─ LLR-504: Display altitude
   ├─ Code: flight_control.c, function display_altitude() (lines 62–66)
   └─ Test: test_100.c, test_display_altitude() (verified ✅)

Matrix:
  HLR-201 → LLR-501/502/503/504 → Code → Test → ✅ VERIFIED
```

---

⚡ **LLR BEST PRACTICES**
=======================

✅ **Tip 1: LLRs should be specific (not vague)**
  ❌ Mistake: "Function shall read sensor" (vague)
  ✅ Right: "Function read_altitude_adc() shall read ADC channel 3, return 12-bit value"
  Impact: Developers know exactly what to code

✅ **Tip 2: Number LLRs for traceability**
  ❌ Mistake: LLRs unnamed or loosely identified
  ✅ Right: "LR-501, LR-502, etc." (consistent numbering)
  Impact: Easy to link to code, tests, design

✅ **Tip 3: One function per LLR (roughly)**
  ❌ Mistake: "LR-501: Read ADC, convert, validate, display"
  ✅ Right: Four separate LRs (one per function)
  Impact: Clear 1:1 mapping LLR↔function

✅ **Tip 4: Include derived requirements rationale**
  ❌ Mistake: "LR-501: Read ADC channel 3" (no why)
  ✅ Right: "LR-501: Read ADC channel 3 (altitude sensor connection per hardware pinout doc)"
  Impact: Future maintainers understand design decisions

✅ **Tip 5: Baseline LLRs before coding**
  ❌ Mistake: "We'll finalize LLRs after coding"
  ✅ Right: LLRs baseline in Month 5 (before Month 6 coding)
  Impact: Code constrained by requirements, not vice versa

---

⚠️ **COMMON LLR MISTAKES**
=========================

❌ **Mistake 1: LLRs too high-level (should be HLRs)**
  Problem: "Software shall handle altitude" (too broad)
  Impact: Developers don't know what to implement
  Fix: LLRs are specific (read ADC, convert, validate, display separately)

❌ **Mistake 2: LLRs not traceable**
  Problem: LLR exists, but no link to HLR source
  Impact: Auditor asks "Why does this LLR exist?"
  Fix: Maintain traceability (LLR ← HLR)

❌ **Mistake 3: LLRs not testable**
  Problem: "Function shall be reliable" (not testable)
  Impact: Cannot verify LLR (unit test impossible)
  Fix: Make LLRs measurable (return value range, timing, etc.)

❌ **Mistake 4: LLRs not baselined**
  Problem: LLRs change during coding (no version control)
  Impact: Code chases moving requirements; confusion
  Fix: Baseline LLRs in DOORS, changes require approval

❌ **Mistake 5: Too many/too few LLRs**
  Problem: 1,000 LLRs (too detailed) or 20 LLRs (too sparse)
  Impact: Either over-specification or under-specification
  Fix: Target 200–500 LLRs (roughly 2–5 per HLR)

---

🎓 **LEARNING PATH: LLRs**
==========================

**Week 1: Understanding LLRs**
  📖 Read: DO-178C Chapter 4 (low-level requirements objectives)
  📖 Study: Relationship between HLR and LLR
  🎯 Goal: Understand LLR definition, decomposition process

**Week 2: Creating LLRs**
  📖 Study: Real project LLR document (200–500 examples)
  📖 Analyze: How LLRs guide code implementation
  🎯 Goal: Understand LLR creation, detail level

**Week 3: Practice**
  💻 Create: LLRs for example HLRs (autopilot altitude hold)
  💻 Design: Code functions to implement each LLR
  🎯 Goal: Confidence in LLR creation and coding

---

✨ **BOTTOM LINE**
=================

**LLRs = Detailed requirements guiding code implementation**

✅ Decomposed from HLRs (2–5 LLRs per HLR)
✅ Design-level detail (not implementation, not architecture)
✅ Testable (unit tests verify each LLR)
✅ Baselined (version controlled, changes require approval)
✅ Traceable (HLR ← LLR → Code → Test)

**Remember:** Good LLRs = clear implementation. Vague LLRs = coder confusion! 🔧

---

**Last updated:** 2026-01-12 | **LLR: Low-Level Requirements**

**Key Takeaway:** 💡 **LLRs bridge design and implementation.** Write them specifically, baseline them early, code to them faithfully! 🛡️
