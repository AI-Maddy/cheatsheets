👤 **DER: Designated Engineering Representative (Authority's Eyes & Ears)** (2026 Edition!)
============================================================================================

**Quick ID:** FAA/EASA-appointed person with authority to represent them during development/testing
**Key Role:** Oversight, approval, sign-off on technical decisions
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—DER approval required for major milestones

---

✈️ **WHAT IS DER (DESIGNATED ENGINEERING REPRESENTATIVE)?**
===========================================================

**DER** = Government-authorized representative (FAA or EASA) embedded in project with power to:
  ✅ **Observe** development activities (code reviews, testing, design reviews)
  ✅ **Approve** technical decisions (DAL assignment, tool qualification, test approach)
  ✅ **Sign-off** on major milestones (design complete, verification complete, validation complete)
  ✅ **Escalate** issues to authority if needed (approach not acceptable? escalate to headquarters)
  ✅ **Represent FAA/EASA** during project (DER = official authority presence)

**Key Distinction:** DER is NOT advisory; DER has approval authority. DER can say "no, this approach not acceptable."

**Alternative Name:** "FAA Principal Inspector" (some regions); "EASA Qualified Person" (EASA equivalent)

---

🤝 **DER ROLES & RESPONSIBILITIES**
==================================

**Role 1: PSAC/Plan Review & Approval**
  🎯 Month 2: Review PSAC draft (before submission to authority)
  🎯 Month 2: Provide feedback on approach, coverage targets, test strategy
  🎯 Month 3: Present PSAC to authority (DER speaks on behalf of development team)
  🎯 Outcome: DER signs off on PSAC; authority issues approval letter

  **DER Approval Questions:**
    • "Is verification approach sufficient for DAL A requirements?" ✓ Yes / ✗ No
    • "Are coverage targets appropriate (MC/DC for A, decision for C)?" ✓ Yes / ✗ No
    • "Is independence approach adequate (separate testers)?" ✓ Yes / ✗ No
    • "Are test scenarios realistic (system conditions)?" ✓ Yes / ✗ No

**Role 2: Design Review Attendance & Sign-off**
  🎯 Month 4–6: Attend Preliminary Design Review (PDR)
  🎯 Month 6–8: Attend Critical Design Review (CDR)
  🎯 DER observes design; notes issues; provides feedback
  🎯 Outcome: DER approves design ("Design acceptable for Phase 3 implementation")

**Role 3: Tool Qualification Verification**
  🎯 Month 2–4: Review tool qualification plans (compiler, coverage analyzer, debugger)
  🎯 DER observes tool testing; verifies testing adequate
  🎯 Outcome: DER approves tools ("Tool qualified; can be used in development")

  **DER Verification Questions:**
    • "Is compiler testing adequate (simple program compiled correctly)?"
    • "Is coverage analyzer qualification sufficient (known test cases measured correctly)?"
    • "Will tool version be locked (no mid-project tool upgrades)?"
    • "Is tool documentation complete (test plans, test results retained)?"

**Role 4: Test Review & Observation**
  🎯 Months 6–16: Observe unit/integration/system testing
  🎯 DER reviews test plans; observes test execution (some tests live, some via data)
  🎯 DER reviews test results; verifies coverage targets being met
  🎯 Outcome: DER confirms testing adequate ("Verification meets DO-178C")

  **DER Test Observation:**
    • Observe unit test execution (watch developer run test suite)
    • Review integration test plan (verify all interfaces tested)
    • Observe system test (watch altitude hold function tested end-to-end)
    • Verify coverage metrics (MC/DC = 100%? Decision = 90%?)

**Role 5: Flight Test Supervision (if applicable)**
  🎯 Month 18–22: Observe system operational testing
  🎯 DER present during flight test (watches real-world operation)
  🎯 DER verifies test scenarios match PSAC (realistic conditions)
  🎯 Outcome: DER confirms system works in real aircraft ("OOT successful")

  **DER Flight Test Presence:**
    • Present at test briefing (understands test objectives)
    • Observes flight maneuvers (altitude hold, autopilot disengagement, mode transitions)
    • Reviews real-time data (system behavior captured)
    • Approves test results (system acceptable for operational use)

**Role 6: Final Certification Review & Sign-off**
  🎯 Month 22: Reviews complete objective evidence package (6–10 volumes)
  🎯 DER verifies all DO-178C compliance objectives met
  🎯 DER ensures all traceability linkages correct (Requirement ↔ Design ↔ Code ↔ Test)
  🎯 Outcome: DER approves package ("Compliant with DO-178C"); signs Type Certificate

---

📅 **DER ENGAGEMENT TIMELINE**
=============================

**Month 1–2: Project Initiation**
  👤 DER assigned to project (formal notification to development company)
  👤 Initial meeting (DER meets project team; learns project scope)
  👤 DER reviews draft PSAC (provides feedback)

**Month 2–3: Plan Approval**
  👤 DER presents/discusses PSAC with authority (SOI #1 preparation)
  👤 DER signs off on PSAC ("Plan acceptable")
  👤 Authority issues approval letter

**Month 3–4: Tool Qualification Planning**
  👤 DER reviews tool qualification plans
  👤 DER verifies test strategies for each tool
  👤 DER signs off on tool qualification approach

**Month 4–6: Design Phase & Tool Qualification**
  👤 DER attends Preliminary Design Review (PDR)
  👤 DER observes tool qualification testing (spot-checks)
  👤 DER reviews design documents (comments on completeness)

**Month 6–8: Critical Design Review**
  👤 DER attends Critical Design Review (CDR)
  👤 DER approves design ("Ready for implementation")
  👤 Tool qualification completion verified by DER

**Month 8–16: Implementation & Verification**
  👤 DER reviews test plans (unit, integration, system)
  👤 DER observes testing (attends key test executions)
  👤 DER tracks coverage metrics (MC/DC targets being met?)
  👤 DER participates in SOI #2 (Month 10) briefing

**Month 16–18: Validation Planning**
  👤 DER reviews validation/OOT test plan (system testing, flight test)
  👤 DER approves validation approach
  👤 DER participates in SOI #3 (Month 18) briefing

**Month 18–22: Validation & Final Certification**
  👤 DER observes validation testing
  👤 DER present at flight test (if applicable) for final validation
  👤 DER reviews objective evidence package
  👤 DER signs off on compliance ("Package acceptable for certification")

**Month 22–24: Authority Decision**
  👤 DER submits recommendation to authority
  👤 Authority issues TSO/Type Certificate
  👤 DER monitors any conditional approval items (additional testing, documentation)

---

💼 **SAMPLE DER COMMUNICATION**
=============================

**Scenario 1: DER Raises Concern at Design Review**

Development Team presents architecture (hardware/software interfaces).

DER: "I see that SoftwareModule A communicates with Hardware Module X via SPI interface. How will you verify this interface works correctly under fault conditions (e.g., SPI communication loss)?"

Development Team: "We have integration tests that simulate SPI loss and verify software response (timeout handler, error flag set)."

DER: "Good. Please ensure those tests are documented in the test plan and are observable during integration testing phase. I'll want to see test execution data."

Development Team: "Understood. We'll include integration test details in test plan and provide DER observation schedule."

**Outcome:** Interface testing plan approved by DER; proceeds to implementation.

---

**Scenario 2: DER Approves Tool Qualification**

Development Team presents compiler qualification test plan.

DER: "You're planning to compile a simple altitude calculation function and verify the executable works correctly. Seems reasonable. How many test cases?"

Development Team: "3 test cases: valid altitude input, zero altitude, and negative altitude (error case)."

DER: "Fine. Document the test cases, show me the compiler output, and confirm the compiled executable produces correct results. When will you complete this?"

Development Team: "We'll have results ready by Month 4."

DER: "Good. I'll review results in Month 4 and sign off if testing adequate."

**Outcome:** Compiler qualification approved by DER; tool can be used in development.

---

⚡ **DER BEST PRACTICES**
=======================

✅ **Tip 1: Engage DER early (Month 1, not Month 10)**
  ❌ Mistake: "DER assigned late; doesn't understand early decisions"
  ✅ Right: "DER assigned Month 1; involved in PSAC planning; understands approach"
  Impact: DER alignment from start; smooth approvals throughout

✅ **Tip 2: Treat DER as authority (because they are; don't argue)**
  ❌ Mistake: "DER raises concern; team dismisses as advisory"
  ✅ Right: "DER raises concern; team addresses immediately and briefs DER on resolution"
  Impact: DER approval for project progress; no surprises late-project

✅ **Tip 3: Provide DER with complete, timely information (don't hide problems)**
  ❌ Mistake: "Defect found Month 8; not reported to DER until Month 12"
  ✅ Right: "Defect found Month 8; reported to DER immediately with remediation plan"
  Impact: DER confidence in team; problem solved early

✅ **Tip 4: Document all DER approvals (meeting minutes, sign-offs, emails)**
  ❌ Mistake: "DER verbally approves something; not documented"
  ✅ Right: "DER approval captured in meeting minutes; documented in objective evidence"
  Impact: Clear audit trail; no disputes over what was approved

✅ **Tip 5: DER observation is mandatory for key milestones (attendance/participation required)**
  ❌ Mistake: "Try to skip DER observation of flight test to save time/cost"
  ✅ Right: "Plan DER presence at flight test; essential to certification"
  Impact: DER confidence in system; validation credible; certification smooth

---

⚠️ **COMMON DER MISTAKES**
=========================

❌ **Mistake 1: DER assigned too late (Month 6 instead of Month 1)**
  Problem: "DER doesn't know early decisions (DAL assignments, approach); conflicts emerge"
  Impact: DER requests rework on decisions made without their input
  Fix: Assign DER Month 1; involve in PSAC planning from start

❌ **Mistake 2: DER concerns treated as advisory (not mandatory)**
  Problem: "DER raises concern about verification approach; team ignores"
  Impact: Same concern re-raised late-project; rework required
  Fix: Treat DER concerns as mandatory; address immediately and brief DER on resolution

❌ **Mistake 3: Problems not disclosed to DER (team tries to solve silently)**
  Problem: "Defect found; not reported to DER; discovered later in authority review"
  Impact: Authority loses confidence; additional verification required; delays
  Fix: Report issues to DER immediately with planned resolution

❌ **Mistake 4: DER approvals not documented (verbal approval only)**
  Problem: "DER verbally approves tool; later question arises over whether tool qualified"
  Impact: No evidence of approval; must re-qualify
  Fix: Document all DER approvals in writing (emails, meeting minutes, sign-off sheets)

❌ **Mistake 5: DER observation skipped (try to save cost/time)**
  Problem: "Flight test conducted without DER present; authority questions validity"
  Impact: Flight test may need to be repeated with DER present
  Fix: Plan DER observation budget/schedule; DER attendance non-negotiable

---

🎓 **LEARNING PATH: DER**
========================

**Week 1: DER Role & Authority**
  📖 Read: DO-178C Section 2 (certification process), AC 20-115 (FAA guidance on DER)
  📖 Study: DER responsibilities, approval authority, relationship to development team
  🎯 Goal: Understand DER role and why DER approval matters

**Week 2: DER Engagement**
  📖 Study: Real project DER interactions (design reviews, test observation, sign-offs)
  📖 Analyze: DER concerns raised, how addressed, outcomes
  🎯 Goal: Understand how DER engages throughout project

**Week 3: DER Communication & Alignment**
  💻 Case study: Project with effective DER engagement (outcomes)
  💻 Practice: Outline DER interaction plan for hypothetical project
  🎯 Goal: Confidence in DER engagement strategy

---

✨ **BOTTOM LINE**
=================

**DER = FAA/EASA representative with approval authority throughout project**

✅ Assigned Month 1 (early, not late)
✅ Involved in PSAC approval (Month 3)
✅ Observes design reviews (Months 4–8)
✅ Verifies tool qualification (Months 2–4)
✅ Observes testing (Months 8–16)
✅ Attends flight test (Month 18–22)
✅ Signs off on final certification (Month 24)
✅ All approvals documented in objective evidence

**Remember:** 👤 **DER ≠ advisory consultant; DER = authority representative with approval power. Treat DER concerns as mandatory!** ✈️

---

**Last updated:** 2026-01-12 | **DER**

**Key Takeaway:** 💡 **Good DER relationship = "Authority happy throughout project!" Bad DER engagement = "Late surprises, rework, delays!"** 🛡️
