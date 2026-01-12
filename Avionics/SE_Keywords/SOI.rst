📊 **SOI: Stages of Involvement (Authority Checkpoints)** (2026 Edition!)
========================================================================

**Quick ID:** Three formal certification gates with FAA/EASA (Months 3, 10, 18)
**Key Meeting:** SOI #1 (PSAC approval), SOI #2 (verification complete), SOI #3 (validation complete)
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Missing SOI gates causes certification delays

---

✈️ **WHAT IS SOI (STAGES OF INVOLVEMENT)?**
============================================

**SOI** = Three formal certification meetings where FAA/EASA provides approval and guidance:
  🎯 **SOI #1 (Month 3):** Authority approves plan (PSAC); proceed with development
  🎯 **SOI #2 (Month 10):** Authority reviews design/verification progress; confirm on track
  🎯 **SOI #3 (Month 18):** Authority reviews validation readiness; final certification approach approved

**Purpose:** Authority oversight throughout project (not just at end); reduces surprises, maintains confidence.

**Alternative Name:** "Certification Review Points" (some companies use this term)

---

📅 **SOI TIMELINE (Critical Dates)**
==================================

**Month 2–3: SOI #1**
  ⏰ Month 2: Finish PSAC (Plan for Software Aspects of Certification)
  ⏰ Month 2: Submit PSAC to FAA/EASA (formal submission)
  ⏰ Week: Authority reviews PSAC (feedback in ~2 weeks)
  ⏰ Month 3: SOI #1 meeting (authority approval)
  ✅ Outcome: PSAC approved; project can proceed to detailed design (Month 4)
  
  **CRITICAL:** SOI #1 absolutely required in Month 3. Cannot skip or delay.

**Month 8–10: SOI #2**
  ⏰ Month 8: Prepare SOI #2 presentation (design/verification progress)
  ⏰ Month 9: Submit presentation to authority (for review)
  ⏰ Month 9–10: SOI #2 meeting (authority feedback)
  ✅ Outcome: Authority satisfied with progress; verification approach confirmed
  
  **Impact:** If major issues identified, may require design rework (extends schedule).

**Month 16–18: SOI #3**
  ⏰ Month 16: Prepare SOI #3 presentation (verification complete; validation ready)
  ⏰ Month 17: Submit presentation to authority
  ⏰ Month 18: SOI #3 meeting (authority approval of validation approach)
  ✅ Outcome: Authority approves validation/testing plan; final certification approach confirmed
  
  **Impact:** Validation (system test, flight test) can proceed confidently.

**Month 22–24: Final Certification**
  ⏰ Month 22: Submit objective evidence package (complete certification dossier)
  ⏰ Month 22–24: Authority final review and decision
  ✅ Outcome: TSO/Type Certificate issued; software approved for use

---

🔍 **SOI #1 DETAIL: Plan Approval (Month 3)**
===========================================

**Purpose:** Authority reviews and approves development approach before work begins

**What Gets Approved:**
  ✅ **Development approach** (V-model lifecycle, 7 phases, 18–24 month timeline)
  ✅ **DAL assignment** (which requirements are DAL A/B/C/D/E?)
  ✅ **Verification approach** (how will requirements be verified? unit/integration/system testing)
  ✅ **Validation approach** (how will system be validated? flight test?)
  ✅ **Tools** (development tools, verification tools, code generators—which will be qualified?)
  ✅ **Methodologies** (traditional code, MBD, formal methods?)
  ✅ **Independence approach** (who will do independent review/testing?)
  ✅ **Test coverage targets** (MC/DC for DAL A/B; decision coverage for DAL C; etc.)

**Meeting Structure:**
  1️⃣ Development team presents PSAC (30–45 min)
  2️⃣ Authority asks questions (30 min)
  3️⃣ Team addresses concerns (real-time or follow-up)
  4️⃣ Authority provides approval (in writing; official letter)

**Authority Concerns (Common Issues Raised at SOI #1):**
  ❓ "Your verification approach seems incomplete; how will you verify safety-critical functions?"
     ➜ Team explains approach; authority satisfied
  
  ❓ "Tool XYZ not mentioned; will it be qualified?"
     ➜ Team adds tool to qualification plan
  
  ❓ "Independence approach doesn't meet DO-178C; testers involved in design?"
     ➜ Team adjusts organization; independent testers separate
  
  ❓ "Test coverage target too low (80% vs 100% for DAL A)?"
     ➜ Team increases coverage target to match authority expectations

**Approval Outcome:** Authority letter saying "PSAC approved; proceed with development"

---

🔍 **SOI #2 DETAIL: Design & Verification Verification (Month 10)**
=============================================================

**Purpose:** Authority confirms design/verification complete and on schedule

**What Gets Reviewed:**
  ✅ **Design completion** (High-Level Requirements complete? Design reviews passed?)
  ✅ **Verification progress** (Unit testing complete? Coverage targets being met?)
  ✅ **Risk assessment** (any unexpected issues discovered? how being addressed?)
  ✅ **Schedule status** (on track for Month 22 certification?)
  ✅ **Objective evidence beginning** (design reviews, test results being documented?)

**Meeting Structure:**
  1️⃣ Development team presents progress (20–30 min)
  2️⃣ Authority asks questions (20 min)
  3️⃣ Team addresses concerns
  4️⃣ Authority provides guidance (any course corrections needed?)

**Authority Concerns (Common Issues Raised at SOI #2):**
  ❓ "Verification coverage only 75% at this stage; should be 90%+?"
     ➜ Team explains test plan completion dates; confident reaching 95%
  
  ❓ "Testing found 15 defects in Month 8; concerning rate?"
     ➜ Team explains defect types (mostly minor); trend decreasing; quality improving
  
  ❓ "Risk of missing validation phase; schedule slipping?"
     ➜ Team confirms schedule buffer; validation will be complete by Month 22
  
  ❓ "Design review findings not all resolved?"
     ➜ Team lists resolved/pending items; timeline for completion

**Non-Approval Outcome:** Authority letter saying "Progress satisfactory; continue per PSAC" (or conditional approval "Address these issues before SOI #3")

---

🔍 **SOI #3 DETAIL: Validation Readiness (Month 18)**
===================================================

**Purpose:** Authority confirms verification complete, validation approach solid, ready for final phase

**What Gets Reviewed:**
  ✅ **Verification completion** (all unit/integration/system testing complete? coverage targets met?)
  ✅ **Objective evidence package** (draft of all required documentation)
  ✅ **Validation approach** (system testing, flight testing planned for Months 18–22)
  ✅ **Corrective actions** (any defects found? how being corrected?)
  ✅ **Final certification approach** (what will be submitted Month 22?)

**Meeting Structure:**
  1️⃣ Development team presents completion status (30 min)
  2️⃣ Authority asks questions (20 min)
  3️⃣ Team addresses concerns
  4️⃣ Authority provides final guidance

**Authority Concerns (Common Issues Raised at SOI #3):**
  ❓ "Testing completed; but 3 defects still open?"
     ➜ Team explains defects non-critical; rework planned; completion in 2 weeks
  
  ❓ "Coverage targets met, but some areas marginal (MC/DC 99.8% vs target 100%)?"
     ➜ Team explains areas (error handling paths difficult to test); coverage adequate for safety
  
  ❓ "Validation flight test planned for 15 hours; sufficient?"
     ➜ Team explains test scenarios; 15 hours covers all critical functions
  
  ❓ "Documentation draft reviewed; gaps identified?"
     ➜ Team commits to resolving gaps before Month 22 submission

**Final Approval:** Authority letter saying "Validation approach approved; ready for certification" (conditional "Resolve listed items before final submission")

---

📋 **SOI PREPARATION CHECKLIST**
==============================

**SOI #1 Preparation (Month 2)**
  ☑ PSAC draft complete (12 sections)
  ☑ Development approach defined (V-model, phases, timeline)
  ☑ DAL assignments confirmed (safety criticality for all requirements)
  ☑ Verification/validation approach documented (testing strategy)
  ☑ Tools identified (development, verification, qualification planned)
  ☑ Independence approach defined (who will do independent testing?)
  ☑ Test coverage targets specified (MC/DC for DAL A, etc.)
  ☑ Presentation prepared (20–30 slides, practice delivered)
  ☑ Q&A prepared (anticipate authority questions)

**SOI #2 Preparation (Month 9)**
  ☑ Design reviews completed (HLRs complete, architecture approved)
  ☑ Verification progress documented (test results, coverage metrics)
  ☑ Risk register updated (issues/risks identified and tracked)
  ☑ Schedule status confirmed (on track for Month 22?)
  ☑ Objective evidence beginning (design reviews, test plans documented)
  ☑ Presentation prepared (progress briefs, metrics, risk updates)
  ☑ Corrective actions tracked (any issues from SOI #1? resolved?)

**SOI #3 Preparation (Month 17)**
  ☑ Verification completion confirmed (testing complete, coverage targets met)
  ☑ Objective evidence package drafted (major documents assembled)
  ☑ Validation test plan finalized (system testing, flight testing scenarios)
  ☑ Defect status documented (defects closed/resolved)
  ☑ Final certification approach defined (what's being submitted Month 22)
  ☑ Presentation prepared (completion status, validation readiness, final approach)
  ☑ Corrective actions completed (no open items from SOI #2)

---

⚡ **SOI BEST PRACTICES**
=======================

✅ **Tip 1: SOI #1 is non-negotiable (Month 3 absolute deadline)**
  ❌ Mistake: "SOI #1 pushed to Month 6; lost 3 months"
  ✅ Right: "PSAC submitted Month 2; SOI #1 meeting Month 3; approved on schedule"
  Impact: Development stays on critical path; no delays

✅ **Tip 2: Prepare thoroughly for each SOI (presentations, data, Q&A)**
  ❌ Mistake: "Unprepared for SOI; authority raises issues; rework required"
  ✅ Right: "Practice presentation; prepare data; anticipate questions"
  Impact: Smooth meetings; authority confidence; no surprises

✅ **Tip 3: Act on authority feedback immediately (don't brush off concerns)**
  ❌ Mistake: "Authority concern raised; team defers action"
  ✅ Right: "Authority concern raised; team addresses before SOI #3"
  Impact: Issues resolved early; no rework late-project

✅ **Tip 4: Document SOI outcomes (meeting minutes, authority letters, decisions)**
  ❌ Mistake: "SOI meeting held; no formal documentation"
  ✅ Right: "Meeting minutes captured; authority approval documented in writing"
  Impact: Objective evidence of authority approval; audit trail clear

✅ **Tip 5: Balance schedule (push hard) with authority engagement (can't skip SOIs)**
  ❌ Mistake: "Skip SOI #2 to save time"
  ✅ Right: "Plan SOI meetings as project milestones; essential to certification"
  Impact: Schedule realistic; authority oversight integrated

---

⚠️ **COMMON SOI MISTAKES**
=========================

❌ **Mistake 1: SOI #1 delayed (Month 6 instead of Month 3)**
  Problem: "PSAC not ready early; development delayed waiting for approval"
  Impact: 3-month project delay; misses delivery date
  Fix: Start PSAC Month 1; submit Month 2; SOI #1 Month 3 (mandatory date)

❌ **Mistake 2: Unprepared for SOI (ad-hoc presentation; authority frustrated)**
  Problem: "Presentation disorganized; data incomplete; authority questions unanswered"
  Impact: Authority doubts development capability; requests extra verification
  Fix: Prepare 3 weeks ahead; practice presentation; compile data; anticipate Q&A

❌ **Mistake 3: Authority concern at SOI #1 ignored (not addressed until SOI #3)**
  Problem: "Authority notes verification approach weak; team doesn't change approach"
  Impact: Same concern re-raised at SOI #3; late rework required
  Fix: Address concerns immediately; brief authority on resolution before SOI #2

❌ **Mistake 4: No formal documentation of SOI outcomes (what was approved?)**
  Problem: "Authority feedback given verbally; later disputed what was approved"
  Impact: No audit trail; certification review challenging
  Fix: Meeting minutes documented; authority approval letter obtained

❌ **Mistake 5: Schedule assumes SOIs not needed (try to compress or skip)**
  Problem: "Plan developed without SOI gates; SOIs required by regulation"
  Impact: SOIs can't be skipped; schedule must accommodate (Months 3, 10, 18)
  Fix: Build SOI gates into project plan from start

---

🎓 **LEARNING PATH: SOI**
========================

**Week 1: SOI Concepts**
  📖 Read: DO-178C Section 2 (certification process), AC 20-115 (FAA guidance)
  📖 Study: Three SOI gates, purposes, approval criteria
  🎯 Goal: Understand SOI purpose and critical dates (Month 3, 10, 18)

**Week 2: SOI Content & Preparation**
  📖 Study: Real project PSAC (what gets approved at SOI #1)
  📖 Analyze: SOI #2 presentation (how to demonstrate verification progress)
  🎯 Goal: Understand what's reviewed at each SOI

**Week 3: SOI Execution & Authority Engagement**
  💻 Case study: Project with successful SOI gates (outcomes)
  💻 Practice: Outline SOI #1 presentation for hypothetical project
  🎯 Goal: Confidence in SOI preparation and execution

---

✨ **BOTTOM LINE**
=================

**SOI = Three mandatory authority gates ensuring oversight throughout certification**

✅ **SOI #1 (Month 3):** Plan approval (PSAC approved; proceed)
✅ **SOI #2 (Month 10):** Design/verification confirmation (progress satisfactory)
✅ **SOI #3 (Month 18):** Validation readiness (approach approved; final submission imminent)
✅ **Cannot be skipped or delayed** (regulatory requirement; authority oversight mandatory)
✅ **Preparation essential** (presentations, data, documentation required)
✅ **Authority feedback must be acted upon** (issues addressed by next SOI or end-of-project)

**Remember:** 📊 **SOI gates = "Authority saying 'yes, approved' at Months 3, 10, 18!" Build these into your plan from Day 1.** ✈️

---

**Last updated:** 2026-01-12 | **SOI**

**Key Takeaway:** 💡 **SOI #1 Month 3 = non-negotiable gate! Plan around it. Authority oversight = confidence throughout.** 🛡️
