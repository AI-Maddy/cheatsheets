📋 **Software Level: Your Safety Criticality Classification** (2026 Edition!)
===========================================================================

**Quick ID:** Synonymous with DAL (Development Assurance Level)
**Alternative Names:** Software Assurance Level, Software Safety Level
**Range:** 5 levels (A → B → C → D → E)
**Also Called:** "Safety Integrity Level" (in IEC 61508 context)
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Determines project rigor

---

✈️ **WHAT IS SOFTWARE LEVEL?**
==============================

**Software Level** = The safety criticality classification of your software

**Key Point:** "Software Level" and "DAL" are **synonymous terms**—they mean the same thing!

✅ Software Level A = DAL A (Catastrophic)
✅ Software Level B = DAL B (Hazardous)
✅ Software Level C = DAL C (Major)
✅ Software Level D = DAL D (Minor)
✅ Software Level E = DAL E (No Safety Effect)

**Why Two Names?**
  • **DAL** = Formal DO-178C terminology (Development Assurance Level)
  • **Software Level** = Alternative term (sometimes used in system architecture docs, ARP4754A)
  • Both refer to identical concept—choose one term and use consistently throughout project!

---

📊 **5-LEVEL CLASSIFICATION: Quick Mapping**
============================================

| **Level** | **Failure Severity** | **Assurance Required** | **Example System** |
|:----------|:-------------------|:----------------------|:------------------|
| **A** | Catastrophic (loss of life) | Maximum | Flight control |
| **B** | Hazardous (serious injury) | Very High | Hydraulic monitoring |
| **C** | Major (major malfunction) | High | In-flight entertainment |
| **D** | Minor (annoyance) | Medium | Cabin lighting |
| **E** | None (no safety impact) | Minimal | Magazine display |

---

🎯 **SOFTWARE LEVEL VS. DAL: Are They Different?**
==================================================

**Simple Answer: NO—They're identical!**

**DO-178C Terminology:** "Development Assurance Level" (DAL)
  Used in: PSAC, plans, compliance documents, authority interactions
  Example: "This software is DAL A"

**System-Level Terminology:** "Software Level" 
  Used in: ARP4754A system requirements, architecture documents
  Example: "Software level assigned = Level A"

**Real-World Usage:**
  ✅ Most common: "DAL" (used 90% of time in avionics)
  ✅ Also valid: "Software Level" (used in system architecture context)
  ✅ Either term acceptable—just be consistent!

**Important:** Don't confuse software level with:
  ❌ Software version (v1.0, v1.1, etc.)—different concept!
  ❌ Software maturity level (CMMI) — different framework!
  ✅ Both refer to safety criticality only

---

📋 **WHEN YOU HEAR "SOFTWARE LEVEL"**
====================================

**In System Architecture Meeting:**
  Speaker: "The autopilot software level is A"
  Translation: "DAL A (catastrophic failures possible)"
  Action: Plan maximum assurance (100% MC/DC, full independence, monthly SQA)

**In Requirements Document (ARP4754A context):**
  Statement: "Software must meet Level C requirements"
  Translation: "DAL C (major failures possible)"
  Action: Plan decision coverage 100%, moderate independence, quarterly SQA

**In FAA Communication:**
  FAA: "What is the software level for this function?"
  Your Answer: "DAL A, because autopilot failure → catastrophic"
  FAA: ✅ (understands you know your safety assignment)

---

💡 **HOW TO DETERMINE SOFTWARE LEVEL**
======================================

**Step 1: System-Level Hazard Analysis (ARP4754A)**
  • What happens if this software fails?
  • What are the consequences? (loss of life, injury, major malfunction, etc.)
  • Use failure modes and effects analysis (FMEA)

**Step 2: Classify Failure Severity**
  • Catastrophic = Level A (loss of aircraft/lives)
  • Hazardous = Level B (serious injury, major system loss)
  • Major = Level C (major system malfunction)
  • Minor = Level D (minor inconvenience)
  • No Safety Effect = Level E (purely informational)

**Step 3: Assign Software Level**
  • Based on failure severity determined in Step 2
  • Document in PSAC (justification required)
  • Get authority approval (FAA/EASA agrees on assignment)

**Step 4: Allocate Assurance Rigor**
  • Level A → 100% MC/DC, full independence, monthly SQA
  • Level B → 100% MC/DC, partial independence, monthly SQA
  • Level C → 100% decision coverage, minimal independence, quarterly SQA
  • Level D → 100% statement coverage, no independence required, annual SQA
  • Level E → No specific requirements, developer discretion

---

⚙️ **SOFTWARE LEVEL IMPLICATIONS: What It Means**
===============================================

**If Your Software is Level A (Catastrophic):**
  🔴 You're working on most critical system
  🔴 Budget 2x schedule & cost vs. normal project
  🔴 Plan monthly SQA audits (non-negotiable)
  🔴 Expect strict independence (verifier ≠ developer, separate team)
  🔴 MC/DC coverage = mandatory (100%, automated)
  🔴 Every review is formal (documented, recorded, signed)
  🔴 Tool qualification = extensive
  🔴 Authority heavily involved (SOI gates intense)
  🔴 No shortcuts allowed (auditors scrutinize everything)
  ⏰ Timeline: 24+ months typical

**If Your Software is Level B (Hazardous):**
  🟠 High criticality, but not catastrophic
  🟠 Budget 1.5x schedule & cost vs. normal project
  🟠 Plan monthly SQA audits (regular)
  🟠 Expect partial independence (at least different person/team)
  🟠 MC/DC coverage = mandatory (100%, automated)
  🟠 Most reviews are formal (key ones recorded)
  🟠 Tool qualification = risk-based
  🟠 Authority moderately involved (SOI gates important)
  🟠 Some flexibility on process (with justification)
  ⏰ Timeline: 20 months typical

**If Your Software is Level C (Major):**
  🟡 Moderate criticality (major system impact)
  🟡 Budget 1.25x schedule & cost vs. normal project
  🟡 Plan quarterly SQA audits (regular)
  🟡 Independence = nice-to-have (not required)
  🟡 Decision coverage = mandatory (100%)
  🟡 Key reviews are formal (design & code)
  🟡 Tool qualification = minimal
  🟡 Authority less involved (fewer SOI gates)
  🟡 More flexibility on process (risk-based approach)
  ⏰ Timeline: 16 months typical

**If Your Software is Level D (Minor):**
  🟢 Low criticality (minor system impact)
  🟢 Minimal overhead vs. normal project
  🟢 Plan annual SQA audits (light touch)
  🟢 Independence = optional (developer OK)
  🟢 Statement coverage = target (100%)
  🟢 Reviews = as needed (not all formal)
  🟢 Tool qualification = minimal/none
  🟢 Authority minimally involved
  🟢 Maximum process flexibility (agile OK)
  ⏰ Timeline: 12 months typical

**If Your Software is Level E (No Safety Effect):**
  ⚪ No safety impact (convenience system)
  ⚪ Normal project overhead (no additional rigor)
  ⚪ SQA = optional (no regulatory requirement)
  ⚪ Independence = N/A (developer tests own work)
  ⚪ Coverage = optional (developer discretion)
  ⚪ Reviews = minimal (documentation priority)
  ⚪ Tool qualification = N/A (any tools fine)
  ⚪ Authority not involved
  ⚪ Full agile/rapid development OK
  ⏰ Timeline: 6 months typical

---

🛠️ **DETERMINING SOFTWARE LEVEL: Practical Example**
===================================================

**Example: Cabin Temperature Control System**

**Step 1: Hazard Analysis**
  ❓ What if cabin temperature control software fails?
  ❓ Possible failure modes:
    - Software crashes (no temperature control)
    - Temperature rises to 120°F (passenger discomfort)
    - Temperature drops to 40°F (passenger discomfort, health risk)
    - Control loops oscillate wildly (instability)

**Step 2: Classify Severity**
  ❓ What are consequences?
    - Passenger discomfort (yes)
    - Health impact? (minimal, humans tolerate wide temp ranges)
    - Safety threat? (no—flight safety not affected)
  ✅ Failure Severity: **Minor** (passenger annoyance, no safety impact)

**Step 3: Assign Software Level**
  ✅ **Assigned Level: D** (Minor)
  ✅ Justification: Cabin temperature non-critical; redundant systems provide fallback

**Step 4: Allocate Assurance**
  ✅ 100% statement coverage (not decision/MC/DC)
  ✅ No independent verification required
  ✅ Minimal SQA involvement
  ✅ Standard tools (no qualification needed)
  ✅ Standard development process
  ✅ Expected duration: 12 months

**Authority Agreement:** FAA approves Level D assignment (no rework needed!)

---

📊 **SOFTWARE LEVEL ASSIGNMENT: Real-World Examples**
====================================================

**Flight Control System (Autopilot)**
  Failure: Software crash → Loss of aircraft control
  Severity: **Catastrophic** → **Level A**
  Rigor: Maximum (100% MC/DC, full independence, monthly SQA)

**Engine Monitoring System**
  Failure: Software fails to detect engine overspeed
  Severity: **Hazardous** (engine damage, possible power loss) → **Level B**
  Rigor: Very High (100% MC/DC, partial independence, monthly SQA)

**Hydraulic System Monitoring**
  Failure: Software fails to alert pilot to low pressure
  Severity: **Hazardous** (hydraulic failure possible) → **Level B**
  Rigor: Very High (100% MC/DC, independence, monthly SQA)

**In-Flight Entertainment System**
  Failure: Software crashes (no video)
  Severity: **Major** (passenger annoyance, system loss) → **Level C**
  Rigor: High (100% decision coverage, minimal independence)

**Cabin Lighting System**
  Failure: Lights won't dim/brighten
  Severity: **Minor** (passenger inconvenience) → **Level D**
  Rigor: Medium (100% statement coverage, no special requirements)

**Flight Magazine Delivery System**
  Failure: App crashes (passengers read physical magazine instead)
  Severity: **No Safety Effect** (purely convenience) → **Level E**
  Rigor: Minimal (no special requirements, standard development)

---

⚠️ **COMMON MISTAKES: Software Level Assignment Errors**
========================================================

❌ **Mistake 1: Assigning Level too low to save schedule**
  Problem: "Let's call it Level E to avoid rigor"
  Impact: Auditor disagrees → rework required, schedule worse!
  Fix: Justify level based on failure analysis, not convenience

❌ **Mistake 2: Assigning Level too high "to be safe"**
  Problem: "Everything is Level A to ensure quality"
  Impact: Project costs 4x more, takes 2x longer (unnecessary rigor)
  Fix: Use risk-based approach; justify each level assignment

❌ **Mistake 3: Changing Level mid-project**
  Problem: "Now we think it's Level B, not Level C"
  Impact: Entire verification/audit plan invalidated (expensive rework!)
  Fix: Get level right in PSAC (before development); changes require authority approval

❌ **Mistake 4: Not documenting Level rationale**
  Problem: "We assigned Level C; authority asks why"
  Impact: Can't justify decision → audit failure
  Fix: Document hazard analysis, failure modes, justification in PSAC

❌ **Mistake 5: Confusing Software Level with software version**
  Problem: "This is software level 2.0"
  Impact: Confusion (do they mean DAL or version number?)
  Fix: Use clear terminology: "Level A" (DAL) vs. "v2.0" (version)

---

🎓 **LEARNING PATH: Understanding Software Level**
=================================================

**Week 1: Fundamentals**
  📖 Read: ARP4754A (system-level hazard analysis—explains level assignment)
  📖 Read: [DAL](DAL.rst) cheatsheet (understand 5-level system)
  🎯 Goal: Understand software level concept and mapping to DAL

**Week 2: Practical Application**
  📖 Study: Real project PSAC (see actual level assignments)
  📖 Analyze: System failure modes (practice level determination)
  🎯 Goal: Apply level determination to example systems

**Week 3: Integration**
  📖 Understand: How level determines project rigor
  📖 Plan: Assurance activities based on assigned level
  🎯 Goal: Plan realistic project schedule/cost per level

---

✨ **BOTTOM LINE**
=================

**Software Level = Safety Criticality Classification**

✅ Synonymous with DAL (Development Assurance Level)
✅ 5 levels: A (catastrophic) → B (hazardous) → C (major) → D (minor) → E (none)
✅ Determined by system-level hazard analysis (ARP4754A)
✅ Assigned in PSAC (before development)
✅ Drives assurance rigor (coverage targets, independence, SQA frequency)

**Remember:** Software level = your safety mandate. Justify rigorously, plan accordingly! 📋

---

**Last updated:** 2026-01-12 | **Software Level Classification**

**Key Takeaway:** 💡 **Software Level is just another name for DAL.** Understand the 5 levels, determine yours early, plan accordingly, and you'll have a smooth certification! 🛡️
