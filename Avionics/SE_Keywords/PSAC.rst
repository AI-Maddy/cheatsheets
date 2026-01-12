🛡️ **PSAC: Your Certification Roadmap to FAA/EASA** (2026 Edition!)
==================================================================

**Quick ID:** Plan for Software Aspects of Certification (YOUR DO-178C approach)
**Submitted:** Early in project (before SOI #1, ideally in planning phase)
**Authority:** Sent to FAA/EASA for formal acceptance
**Criticality Level:** ⭐⭐⭐⭐⭐ CRITICAL—This is your ticket to certification

---

✈️ **WHAT IS THE PSAC?**
========================

The **PSAC** (Plan for Software Aspects of Certification) is a critical document that:

📋 **Outlines your compliance approach** → How you'll meet DO-178C objectives
📋 **Justifies your DAL assignment** → Why this software is safety-critical
📋 **Describes your processes** → Planning, development, verification, audits
📋 **Defines your independence strategy** → How you'll avoid conflicts of interest
📋 **Lists your tools & methods** → Compilers, test frameworks, static analyzers
📋 **Sets authority expectations** → What FAA/EASA will see and approve

**The Golden Rule:** PSAC approved early = project proceeds with confidence. Late PSAC = surprises = rework!

---

📊 **WHAT GOES IN A PSAC?**
===========================

**Section 1: Executive Summary (1–2 pages)**
  ✅ Aircraft/system identification (e.g., "Boeing 737 MAX Flight Control System")
  ✅ Software identification (e.g., "FCS-v2.1 Autopilot Control Software")
  ✅ DAL assignment (e.g., "DAL A - Catastrophic")
  ✅ Compliance statement (e.g., "This software complies with DO-178C and FAA Order 8110.49")
  ✅ Overview of certification approach (1 paragraph)

**Section 2: DAL Justification (2–3 pages)**
  ✅ System-level hazard analysis reference (ARP4754A)
  ✅ Software failure modes & consequences
  ✅ Why DAL A/B/C/D/E is appropriate
  ✅ Mitigation strategies (redundancy, monitoring, error detection)
  Example:
    "Flight control software failure → Loss of aircraft control → Catastrophic
     Therefore: DAL A required (highest assurance)"

**Section 3: Compliance Approach (3–5 pages)**
  ✅ Overview of planning process (PSAC, SDP, SQAP, SVP—reference them)
  ✅ Development approach (requirements → design → code → integration)
  ✅ Verification & validation strategy (testing, reviews, coverage targets)
  ✅ SQA & CM approach (audits, configuration management, problem reporting)
  ✅ Certification liaison strategy (SOI gates, interaction with authority)

**Section 4: Development Process (5–10 pages)**
  ✅ Requirements management (HLRs from system, baselined, traced)
  ✅ Design process (architecture, design reviews, reusable components)
  ✅ Coding process (standards—MISRA C/C++, complexity limits, reviews)
  ✅ Integration process (module combining, integration testing)
  ✅ Verification process (unit test, integration test, coverage analysis)
  ✅ Validation process (system-level testing, aircraft demo)

**Section 5: Verification & Validation (3–5 pages)**
  ✅ Test strategy (unit, integration, system levels)
  ✅ Structural coverage approach (MC/DC targets, tools, analysis method)
  ✅ Independence strategy (who verifies vs. who develops)
  ✅ Coverage analysis tools (VectorCAST, QualityLogic, CodeScroll, etc.)
  ✅ Expected coverage targets (100% MC/DC for DAL A, decision for C, etc.)

**Section 6: Software Quality Assurance (2–3 pages)**
  ✅ SQA audits (frequency, auditor qualifications, audit scope)
  ✅ Process compliance checks (adherence to plans, standards)
  ✅ Objective evidence collection (reviews, test results, traces)
  ✅ Non-conformance reporting & corrective action process
  ✅ SQA independence from development team

**Section 7: Configuration Management (2–3 pages)**
  ✅ Baselines (planning, requirements, design, implementation, final)
  ✅ Version control (tools—Git, Subversion, Perforce)
  ✅ Change control process (change advisory board, approval authority)
  ✅ Problem reporting (bug tracking, traceability, resolution)
  ✅ Audit trails (who changed what, when, why)

**Section 8: Tools & Techniques (3–5 pages)**
  ✅ Development tools (compiler, IDE, debugger)
  ✅ Verification tools (static analyzer, coverage tool, test framework)
  ✅ Traceability tools (DOORS, Confluence, Polarion)
  ✅ Configuration management tools (Git, Subversion)
  ✅ Tool qualification approach (which tools need DO-330 qualification)

**Section 9: Standards & Processes (2–3 pages)**
  ✅ Applicable standards (MISRA C/C++, IEC 61508, ARP4754A, etc.)
  ✅ Coding standards (naming conventions, comment requirements)
  ✅ Design standards (module size limits, complexity limits)
  ✅ Testing standards (test case template, coverage metrics)
  ✅ Documentation standards (plans, reviews, traceability matrices)

**Section 10: Certification Liaison (1–2 pages)**
  ✅ Point of contact (Certification Manager name, email, phone)
  ✅ SOI gates planned (SOI #1, #2, #3, #4 schedule)
  ✅ Authority expectations (FAA/EASA requirements, DER/CVE involvement)
  ✅ Compliance schedules (milestones, reviews, audits)
  ✅ Authority involvement (briefings, document reviews, on-site audits)

**Section 11: Lifecycle Data Management (1–2 pages)**
  ✅ Artifacts as evidence (plans, reviews, tests, traces, coverage reports)
  ✅ Retention policy (minimum 2 years post-certification, often indefinite)
  ✅ Organization (folder structure, version control)
  ✅ Accessibility (who can access, audit trail for access)

**Section 12: References (1 page)**
  ✅ DO-178C (primary standard)
  ✅ ARP4754A (system-level design, DAL assignment)
  ✅ FAA Order 8110.49 (FAA-specific guidance)
  ✅ EASA AMC 20-115D (European guidance)
  ✅ Project-specific documents (SDP, SQA Plan, etc.)

---

⏱️ **TIMELINE: When & How to Submit PSAC**
===========================================

**Ideal Scenario:**
  📅 **Month 1 (Project Kickoff):** Draft PSAC (2–3 weeks)
  📅 **Month 2:** Internal review & refinement (2 weeks)
  📅 **Month 2 (Day 45):** Submit to authority (FAA/EASA)
  📅 **Month 3–4:** Authority review & questions (4–6 weeks typical)
  📅 **Month 4 (Day 105):** Authority accepts PSAC → **SOI #1 Gate Passed!** ✅
  📅 **Month 5+:** Development begins (with authority blessing)

**Why Early Submission Matters:**
  ✅ Authority feedback incorporated BEFORE development
  ✅ No surprises late in project (changes expensive)
  ✅ Team has clear, approved roadmap
  ✅ Schedule confidence (no rework due to compliance questions)

**What If You Submit Late?**
  ❌ Authority questions compliance approach 6 months into development
  ❌ Rework required (expensive & time-consuming)
  ❌ Schedule slips, costs balloon
  ❌ Project confidence eroded
  ➜ Lesson: Submit PSAC ASAP! It's your insurance policy!

---

🎯 **KEY QUESTIONS THE PSAC MUST ANSWER**
==========================================

**Q1: What software are we certifying?**
  A: Aircraft/system name, software name, version, function
  Document: Identification section (executive summary)

**Q2: Why is this software safety-critical?**
  A: Failure consequences, DAL assignment, hazard analysis reference
  Document: DAL justification section

**Q3: How will we develop this software safely?**
  A: Process description (requirements → design → code → test)
  Document: Development process section (reference SDP for details)

**Q4: How will we verify it works?**
  A: Testing strategy, coverage targets, independence approach
  Document: Verification & validation section

**Q5: How will we ensure quality throughout the project?**
  A: SQA audits, configuration management, problem reporting
  Document: SQA & CM sections

**Q6: What tools will we use?**
  A: Compiler, static analyzer, coverage tool, traceability tool
  Document: Tools & techniques section (plus DO-330 qualification plan)

**Q7: Who's in charge of certification?**
  A: Certification Liaison Manager (name, contact, authority)
  Document: Certification Liaison section

**Q8: How will we prove compliance?**
  A: Objective evidence (plans, reviews, tests, coverage reports)
  Document: Lifecycle Data Management section

---

💼 **PSAC BEST PRACTICES: Lessons from Real Projects**
=====================================================

✅ **Tip 1: Write PSAC as a narrative, not a checklist**
  ✅ Right: "We will develop requirements using a staged process: HLRs derived from system specification, baselined, then LLRs derived from HLRs with traceability maintained throughout..."
  ❌ Wrong: "Requirements: ☐ HLRs ☐ LLRs ☐ Baseline"
  Impact: Authority understands your approach, feels confidence

✅ **Tip 2: Reference other plans, don't repeat them**
  ✅ Right: "See Software Development Plan (SDP) Section 3 for detailed design process"
  ❌ Wrong: Repeat SDP content in PSAC (duplicates information, hard to maintain)
  Impact: PSAC stays concise (15–20 pages), easier to update

✅ **Tip 3: Be specific about tools & techniques**
  ✅ Right: "We will use VectorCAST for structural coverage analysis, targeting 100% MC/DC for DAL A code"
  ❌ Wrong: "We will analyze coverage thoroughly"
  Impact: Authority knows exactly what to expect, can assess feasibility

✅ **Tip 4: Include contingencies for critical risks**
  ✅ Right: "If coverage analysis identifies untestable code, we will use formal methods (DO-333) to verify correctness"
  ❌ Wrong: No mention of how to handle coverage gaps
  Impact: Authority sees you've thought through challenges, increases confidence

✅ **Tip 5: Tailor PSAC to YOUR project, don't use boilerplate**
  ✅ Right: "This software controls flight surfaces; failure → loss of aircraft. Therefore, DAL A with full independence & 100% MC/DC required."
  ❌ Wrong: Copy-paste generic PSAC from similar project (different context!)
  Impact: Authority sees you understand YOUR unique risks

✅ **Tip 6: Involve authority early (informal questions)**
  ✅ Right: Call FAA/EASA 2–3 weeks before formal PSAC submission, describe approach, ask for early feedback
  ❌ Wrong: Submit PSAC cold (first authority sees approach is in formal document)
  Impact: Authority suggestions incorporated before formal review, smoother approval

✅ **Tip 7: Budget 4–6 weeks for authority review**
  ✅ Right: Submit PSAC in Month 2, plan SOI #1 for Month 4
  ❌ Wrong: "Authority will review in 2 weeks" (unrealistic; they're busy!)
  Impact: No schedule pressure on authority, smoother approval

---

⚠️ **COMMON PSAC MISTAKES**
============================

❌ **Mistake 1: Vague DAL justification**
  Problem: "Software is critical, so DAL A"
  Impact: Authority asks "Why? Explain failure modes." → Delays review
  Fix: Include system hazard analysis, failure condition specifics

❌ **Mistake 2: Over-promising on schedule**
  Problem: "We'll achieve 100% MC/DC in 6 months"
  Impact: Authority skeptical (unrealistic) → Credibility damaged
  Fix: Be honest about timeline; include schedule buffers

❌ **Mistake 3: Insufficient independence description**
  Problem: "We'll have some independence"
  Impact: Authority unclear → Asks for clarification → Review delayed
  Fix: Be specific: "Verifier will be separate person/team, trained independently, reviewed by SQA"

❌ **Mistake 4: No contingency plan**
  Problem: PSAC doesn't address "What if coverage analysis finds untestable code?"
  Impact: Authority concerned about plan feasibility
  Fix: Include contingencies (formal methods, design change, waiver request)

❌ **Mistake 5: Outdated after submission**
  Problem: PSAC approved Month 4, but project changes approach in Month 8
  Impact: No longer reflects actual project (audit failure!)
  Fix: Update PSAC with changes; submit as amendment; get authority re-approval

❌ **Mistake 6: Too generic (not project-specific)**
  Problem: PSAC could apply to any aircraft software
  Impact: Authority questions whether author understands THIS project
  Fix: Include specific examples from YOUR system (flight control, hydraulics, etc.)

---

📋 **PSAC OUTLINE TEMPLATE (Customize for Your Project)**
=========================================================

```
PLAN FOR SOFTWARE ASPECTS OF CERTIFICATION
[Aircraft/System Name]
[Software Name & Version]
[Date]
[Revision Number]

1. EXECUTIVE SUMMARY
    1.1 Aircraft/System Identification
    1.2 Software Identification
    1.3 DAL Assignment
    1.4 Certification Approach (1 paragraph overview)

2. DAL JUSTIFICATION
    2.1 System-Level Hazard Analysis Reference
    2.2 Software Failure Modes
    2.3 Consequences Assessment
    2.4 DAL Assignment Rationale
    2.5 Mitigation Strategies

3. COMPLIANCE APPROACH
    3.1 Planning Process Overview
    3.2 Development Approach Overview
    3.3 Verification & Validation Overview
    3.4 SQA & Configuration Management Overview
    3.5 Certification Liaison Approach

4. DEVELOPMENT PROCESS
    4.1 Requirements Management
    4.2 Design Process
    4.3 Coding Process
    4.4 Integration Process

5. VERIFICATION & VALIDATION
    5.1 Test Strategy
    5.2 Structural Coverage Approach
    5.3 Independence Strategy
    5.4 Coverage Analysis Tools & Methods

6. SOFTWARE QUALITY ASSURANCE
    6.1 SQA Audits
    6.2 Process Compliance
    6.3 Objective Evidence Collection

7. CONFIGURATION MANAGEMENT
    7.1 Baselines
    7.2 Version Control
    7.3 Change Control
    7.4 Problem Reporting

8. TOOLS & TECHNIQUES
    8.1 Development Tools
    8.2 Verification Tools
    8.3 Traceability Tools
    8.4 Tool Qualification Approach

9. STANDARDS & PROCESSES
    9.1 Applicable Standards
    9.2 Coding Standards
    9.3 Design Standards

10. CERTIFICATION LIAISON
    10.1 Point of Contact
    10.2 SOI Gates
    10.3 Authority Involvement

11. LIFECYCLE DATA MANAGEMENT
    11.1 Artifacts as Evidence
    11.2 Retention & Organization

12. REFERENCES
    (DO-178C, ARP4754A, FAA Order 8110.49, EASA AMC 20-115D, etc.)
```

---

✨ **BOTTOM LINE**
=================

**The PSAC is your certification contract with authorities.**

✅ Submit EARLY (before development) → authority agrees on approach
✅ Be specific (not vague) → authority understands your plan
✅ Include contingencies → authority sees you've thought through risks
✅ Keep it updated → reflects actual project approach
✅ Get approval → gives project confidence to proceed

**Remember:** PSAC approved = SOI #1 gate passed = project proceeds with authority blessing! 🎯

---

**Last updated:** 2026-01-12 | **PSAC: Plan for Software Aspects of Certification**

**Key Insight:** 💡 **PSAC = Your insurance policy.** Submit early, get approval, sleep better at night! 🛡️
