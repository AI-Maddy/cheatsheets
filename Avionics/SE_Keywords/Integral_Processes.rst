🔀 **Integral Processes: Cross-Cutting Project Activities** (2026 Edition!)
==========================================================================

**Quick ID:** Activities that span entire project lifecycle (not confined to one phase)
**Examples:** Traceability, safety assessment, tool qualification, problem reporting
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—Integral processes ensure completeness

---

✈️ **WHAT ARE INTEGRAL PROCESSES?**
===================================

**Integral Processes** = Activities that happen throughout the entire project (all 7 phases), not just in one phase:
  ✅ **Traceability Management** (Month 2–24: maintain links throughout project)
  ✅ **Safety Assessment** (Month 2–24: ongoing hazard evaluation)
  ✅ **Tool Qualification** (Month 1–8: select, evaluate, qualify tools before coding)
  ✅ **Problem/Change Management** (Month 2–24: track issues, manage changes via CCB)
  ✅ **Corrective Action** (Month 2–24: resolve findings, track closure)

**Key Concept:** Integral processes run "in parallel" with phase-based activities.

**Visual Timeline:**
```
Month:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18
Phase:  P   P   R   R   D   D   I   I   V   V   V   V   V   V   V   A   A   A
        └─────────────────────────────────────────────────────────────────────┘
        Traceability (ongoing)
        └─────────────────────────────────────────────────────────────────────┘
        Safety Assessment (ongoing)
        └─────────────────────────────────────────────────────────────────────┘
        Problem/Change Management (ongoing)
        └─────────────────────────────────────────────────────────────────────┘
        Tool Qualification (early focus)

Legend: P=Planning, R=Requirements, D=Design, I=Implementation, V=Verification, A=Validation/Cert
```

---

📋 **INTEGRAL PROCESSES BY CATEGORY**
====================================

**Integral Process 1: Traceability Management**
  🎯 **What:** Maintaining bidirectional links (System ↔ HLR ↔ LLR ↔ Code ↔ Test ↔ Validation)
  🎯 **Duration:** Month 2 (start) through Month 24 (certification archive)
  
  **Month 2–5:** Establish traceability
    • Create HLR → System Req traceability (Month 2)
    • Create LLR → HLR traceability (Month 5)
    • Develop traceability matrix (spreadsheet or DOORS)
  
  **Month 6–10:** Maintain during implementation
    • Update code → LLR linkage (as code written)
    • Update traceability matrix (code allocations)
  
  **Month 9–16:** Verify during verification
    • Ensure every test case → LLR (each LLR tested)
    • Verify coverage (no orphaned requirements, no untested code)
  
  **Month 16–24:** Finalize for certification
    • Complete traceability: Req → Code → Test → Evidence
    • Archive traceability matrix (read-only, final evidence)

**Integral Process 2: Safety Assessment**
  🎯 **What:** Ongoing evaluation of hazards, safety criticality (DAL), mitigation measures
  🎯 **Duration:** Month 2 (start) through Month 20 (validation)
  
  **Month 2–3:** Hazard Analysis (ARP4754A)
    • Identify all hazards (sensor fails, communication lost, processor hangs)
    • Assign severity (catastrophic, critical, major, minor, no effect)
    • Determine DAL for each hazard (A=catastrophic, B=critical, C=major)
  
  **Month 4–8:** Safety Allocation
    • Allocate mitigation to software (for each hazard)
    • Create Derived Requirements (safety safeguards)
    • Design safety mechanisms (watchdog, error detection, fallback)
  
  **Month 6–16:** Safety Implementation & Verification
    • Code safety features (error handling, timeout, watchdog)
    • Test safety paths (error injection, timeout simulation)
    • Verify mitigations work (objective evidence)
  
  **Month 16–20:** Validation
    • System-level safety testing (hazard simulation, expected responses)
    • Demonstrate hazard can be detected and controlled
    • Produce safety case (evidence all hazards mitigated)

**Integral Process 3: Tool Qualification**
  🎯 **What:** Evaluating and qualifying tools (compiler, debugger, coverage analyzer) before use
  🎯 **Duration:** Month 1–8 (must complete before extensive tool use)
  
  **Month 1–2:** Tool Selection
    • Identify needed tools (compiler, coverage, lint, build)
    • Define tool qualification criteria
    • Plan qualification activity (testing, documentation)
  
  **Month 2–4:** Tool Qualification
    • Obtain tool documentation (user manual, algorithm description)
    • Create qualification tests (does tool work correctly?)
    • Execute qualification tests (objective evidence of tool correctness)
  
  **Month 4–8:** Tool Validation (if applicable)
    • For critical tools (coverage analyzer, compiler), may need formal validation
    • Demonstrate tool produces correct results (measured against known inputs)
  
  **Month 6+:** Tool Use
    • Once qualified, tool is trusted to produce correct results
    • Continue using qualified tool throughout project (no changes mid-project)

  📋 **Example:** Compiler Qualification
    - Tool: GCC C compiler v10.2.1
    - Qualification: Compile test program (known correct output) with GCC, execute, verify output matches expected
    - Result: GCC v10.2.1 qualified for use in project (compiler produces correct code)
    - Requirement: Use ONLY GCC v10.2.1; cannot switch to v11.0 mid-project (would require re-qualification)

**Integral Process 4: Problem/Change Management**
  🎯 **What:** Tracking issues (defects, deviations, change requests) throughout project
  🎯 **Duration:** Month 2 (problems start emerging) through Month 24
  
  **Problem Reporting:**
    • Issue found (code review finds bug, test fails, etc.)
    • Problem report created (ID, description, severity)
    • Severity assigned (critical/major/minor; blocks progress? slows down?)
  
  **Change Control:**
    • For issues affecting baselined items (code baseline, requirements baseline, design baseline)
    • Change Control Request (CCR) submitted to CCB
    • CCB evaluates impact (schedule, cost, scope, risk)
    • CCB approves or rejects change
    • If approved: Change made, baseline version updated, traceability updated
  
  **Tracking:**
    • All problems tracked in database (DOORS, Jira, spreadsheet)
    • Status tracked: open → in-progress → resolved
    • Resolution verified before gate (problem must be fixed before proceeding)
  
  **Example:** Code Defect
    - Test discovers: "altitude calculation overflows at max altitude"
    - Problem Report PR-042 created (severity: major, blocks validation)
    - Root cause: Altitude variable uint16 (max 65535), but max altitude 50000, needs uint32
    - CCR-042 submitted to CCB ("Change data type to uint32")
    - CCB: "Approved (low risk, affects only one variable)"
    - Fix implemented, code re-reviewed, code baseline v1.1, tests re-run
    - PR-042 closed (resolved)

**Integral Process 5: Corrective Action**
  🎯 **What:** Responding to SQA findings, process audit findings, defects
  🎯 **Duration:** Ongoing (Month 2–24)
  
  **Finding Sources:**
    • SQA Finding: "Code review record missing" (process violation)
    • Process Assurance Finding: "SQA gate not enforced" (discipline lapse)
    • Problem Report: Code defect (product issue)
    • Test Finding: "Test failed" (verification issue)
  
  **Corrective Action Process:**
    Step 1: Root Cause Analysis—Why did this happen?
    Step 2: Determine Corrective Action—What must be done?
    Step 3: Implement—Do the work (fix code, re-review, re-test)
    Step 4: Verify—Prove corrective action worked (test passed, review documented)
    Step 5: Close—Mark finding as resolved (SQA sign-off)
  
  **Tracking:**
    • All findings tracked by ID (SQA-001, PA-001, PR-042)
    • Status: open → in-progress → resolved
    • Gate cannot proceed until critical findings resolved
  
  **Example:** Code Review Missing
    - SQA Finding SQA-047: "Module XYZ not code reviewed" (Month 6)
    - Root cause: Module committed to CM before review (developer error)
    - Corrective action: Re-review module XYZ; all findings documented
    - Implementation: Code review meeting held; 2 defects found and fixed
    - Verification: Re-review successful; all issues resolved
    - Close: SQA-047 closed (corrective action complete); gate can proceed

---

💼 **INTEGRAL PROCESSES IN PRACTICE**
====================================

**Real Project Example: Altitude Hold Autopilot (DAL A)**

**Month 2–3 (Planning Phase):**
  ✓ Traceability: Traceability plan created
  ✓ Safety: Hazard analysis identifies "Sensor failure" as catastrophic hazard
  ✓ Tools: Compiler, coverage analyzer, DOORS all selected and qualification plan created
  ✓ Problem Mgmt: Problem tracking database set up (empty at start)
  ✓ Corrective Action: No findings yet; process ready

**Month 4–5 (Requirements Phase):**
  ✓ Traceability: HLR ↔ System Req linkage created (100% coverage)
  ✓ Safety: Safety allocation—"Sensor failure mitigation: detect timeout and disable altitude hold" (Derived Req)
  ✓ Tools: Tool qualification tests executed; compiler and coverage tool qualified
  ✓ Problem Mgmt: HLR review finds 3 issues (vague language, missing error cases, ambiguous requirements)
    - Issues tracked as PR-001, PR-002, PR-003
    - CCB approves updates to HLRs
    - HLRs v1.0 → v1.1 (issues incorporated)
  ✓ Corrective Action: PR-001/002/003 resolved before HLR baseline gate

**Month 6–10 (Implementation Phase):**
  ✓ Traceability: Code ↔ LLR linkage created as developers code modules
  ✓ Safety: Sensor timeout error handling code written (implements Derived Req)
  ✓ Tools: Compiler (qualified) used for all compilation; coverage analyzer (qualified) measures test coverage
  ✓ Problem Mgmt: Code review finds 5 defects (PR-004 through PR-008)
    - Severity: 3 major (must fix), 2 minor (low priority)
    - All major issues fixed and re-reviewed before code baseline
    - Minor issues added to backlog (Month 12 gate decision: fix or defer?)
  ✓ Corrective Action: PR-004/005/006 resolved before code baseline gate

**Month 9–16 (Verification Phase):**
  ✓ Traceability: Test cases ↔ LLR verified; coverage 100%
  ✓ Safety: Sensor timeout test (TC-901) verifies error detection works
  ✓ Tools: Coverage analyzer (qualified) shows 100% MC/DC coverage for DAL A
  ✓ Problem Mgmt: Testing reveals 2 defects (PR-009 altitude rounding, PR-010 watchdog timeout margin)
    - Both fixed and re-tested
    - All tests pass before verification gate
  ✓ Corrective Action: All findings resolved before verification gate (Month 16)

**Month 16–20 (Validation Phase):**
  ✓ Traceability: Final traceability matrix complete (Req → Code → Test; 100% traced)
  ✓ Safety: Flight test validates sensor timeout detection works (sensor failed, altitude hold disabled as designed)
  ✓ Tools: All tools (qualified) continue to be used
  ✓ Problem Mgmt: Validation discovers 1 operational issue (PR-011 display update lag during high-altitude maneuvers)
    - Minor issue; corrective action planned for version 2.0
  ✓ Corrective Action: PR-011 deferred to v2.0 (documented in release notes); validation gate can proceed

**Month 18–24 (Certification):**
  ✓ Traceability: Final archive (read-only, immutable)
  ✓ Safety: Safety case complete (all hazards mitigated, test evidence provided)
  ✓ Tools: Tool qualification evidence included in certification package
  ✓ Problem Mgmt: All critical/major issues resolved; minor issues documented (v2.0 list)
  ✓ Corrective Action: All findings from all phases documented with resolution (objective evidence)

---

⚡ **INTEGRAL PROCESSES BEST PRACTICES**
======================================

✅ **Tip 1: Start integral processes early (not late in project)**
  ❌ Mistake: "We'll establish traceability at the end" (Month 18)
  ✅ Right: "Traceability starts Month 2 and continues throughout"
  Impact: Traceability maintained consistently; no gaps late-discovered

✅ **Tip 2: Assign owners for each integral process**
  ❌ Mistake: "Everyone is responsible for traceability" (nobody is)
  ✅ Right: "Traceability Manager owns traceability; reports status monthly"
  Impact: Process tracked, owned, reported

✅ **Tip 3: Tool qualification before extensive use**
  ❌ Mistake: "Use tool; qualify later if needed"
  ✅ Right: "Qualify tool Month 2–4; start using Month 6 after qualification"
  Impact: Confident tool produces correct results; no surprises late-project

✅ **Tip 4: Problem tracking database (not just email conversations)**
  ❌ Mistake: "Track issues in email; hard to find, easy to lose"
  ✅ Right: "All issues in DOORS/Jira with ID, status, owner, resolution"
  Impact: Nothing falls through cracks; closure verifiable

✅ **Tip 5: Safety assessment continuous (not one-time event)**
  ❌ Mistake: "Do hazard analysis Month 2; done"
  ✅ Right: "Hazard analysis Month 2; revisit monthly as design evolves"
  Impact: New hazards discovered; mitigations stay current

---

⚠️ **COMMON INTEGRAL PROCESS MISTAKES**
======================================

❌ **Mistake 1: Traceability deferred (created at the very end)**
  Problem: "We'll link requirements to code at end of project"
  Impact: Gaps discovered; cannot trace requirement to code; certification fails
  Fix: Maintain traceability throughout (Month 2–24)

❌ **Mistake 2: Tool not qualified (used "as-is" without verification)**
  Problem: "We used GCC compiler; didn't check if it produces correct code"
  Impact: Compiler bugs (unlikely but possible) undetected; produce wrong executable
  Fix: Qualify tools before use (compiler generates correct code, coverage tool accurate)

❌ **Mistake 3: Safety assessment one-time (no ongoing updates)**
  Problem: "Hazard analysis done Month 2; never revisited" (design changes but hazard analysis doesn't)
  Impact: New hazards emerge; mitigations incomplete
  Fix: Revisit safety assessment quarterly (as design evolves)

❌ **Mistake 4: Problem tracking informal (email, chat, spreadsheets)**
  Problem: "Issues discussed on Teams; no formal tracking"
  Impact: Issues lost; closure not verifiable; SQA audit discovers missing problems
  Fix: Formal problem database (DOORS, Jira) with clear workflow

❌ **Mistake 5: Corrective action deferred (findings left open)**
  Problem: "SQA found code review missing; we'll fix later"
  Impact: Finding never resolved; gate should have been held
  Fix: Corrective action completed before next gate (no exceptions)

---

🎓 **LEARNING PATH: Integral Processes**
========================================

**Week 1: Integral Process Concepts**
  📖 Read: DO-178C Sections 4–8 (each section covers integral process aspects)
  📖 Study: Traceability, safety, tool qualification, problem management
  🎯 Goal: Understand what integral processes are and why they run continuously

**Week 2: Implementation Across Phases**
  📖 Study: Real project integral process timeline (when does each activity happen?)
  📖 Analyze: How integral processes interact (traceability + safety + problem management)
  🎯 Goal: Understand how integral processes span entire project

**Week 3: Integral Process Ownership & Tracking**
  💻 Design: Integral process plan for example project (who owns what? reporting?)
  💻 Case study: Project with good integral processes vs. project with gaps (outcomes)
  🎯 Goal: Confidence in implementing integral processes

---

✨ **BOTTOM LINE**
=================

**Integral Processes = Cross-cutting activities spanning entire project lifecycle**

✅ Traceability (maintain Req ↔ Code ↔ Test linkage, Month 2–24)
✅ Safety Assessment (hazard analysis + mitigation, Month 2–20)
✅ Tool Qualification (verify tools work correctly, Month 1–8)
✅ Problem/Change Management (track issues, evaluate changes via CCB, Month 2–24)
✅ Corrective Action (resolve findings, track closure, Month 2–24)

**Remember:** 🔀 **Integral processes glue the project together. Without them, phases are disconnected silos!** ✈️

---

**Last updated:** 2026-01-12 | **Integral Processes**

**Key Takeaway:** 💡 **Integral processes run in parallel with phases. They ensure nothing falls through cracks and all activities are coordinated!** 🛡️
