📚 **SE PROCESS KEYWORDS: Complete Navigation Index** (2026 Edition!)
====================================================================

**Overview:** Comprehensive cheatsheet collection for avionics software engineering process (DO-178C/ED-12C)
**Total Keywords:** 36 individual keyword cheatsheets (covering all phases: Planning → Development → Verification → Certification)
**Format:** Colorful, practical, memorable cheatsheets (~5–15 KB each)
**Use Cases:** Certification preparation, team onboarding, audit readiness, quick reference

---

✈️ **QUICK NAVIGATION: Find Your Keyword**
===========================================

**🔴 CRITICAL STANDARDS & FRAMEWORKS (Read These First!)**
  🛡️ [DO-178C](DO-178C.rst) — THE standard for avionics software (primary reference)
  🛡️ [Development Assurance Level (DAL)](DAL.rst) — Safety criticality (A→B→C→D→E)
  🛡️ [ARP4754A](ARP4754A.rst) — System-level design (complements DO-178C)
  🛡️ [PSAC](PSAC.rst) — Your certification roadmap (submitted to authorities)

**📋 PLANNING & REQUIREMENTS (Foundation Phase)**
  📋 [Planning Process](Planning_Process.rst) — Project initiation, milestone planning
  📋 [Software Development Plan (SDP)](Software_Development_Plan.rst) — Schedules, resources, standards
  📋 [Software Level](Software_Level.rst) — Synonymous with DAL (safety criticality)
  📋 [High-Level Requirements (HLR)](HLR.rst) — System-derived safety requirements
  📋 [Low-Level Requirements (LLR)](LLR.rst) — Detailed software requirements
  📋 [Derived Requirements](Derived_Requirements.rst) — Requirements added during development

---

⚙️ **DEVELOPMENT & DESIGN (Implementation Phase)**
  ⚙️ [Software Development Process](Software_Development_Process.rst) — Activities overview (Req→Design→Code→Integration)
  ⚙️ [Model-Based Development (MBD)](MBD.rst) — Simulink/SCADE (DO-331 supplement)
  ⚙️ [Object-Oriented Technology (OOT)](OOT.rst) — C++, inheritance patterns (DO-332 supplement)

---

✅ **VERIFICATION & VALIDATION (Testing Phase)**
  ✅ [Verification](Verification.rst) — "Are we building it right?" (Tests, reviews, analysis)
  ✅ [Validation](Validation.rst) — "Are we building the right thing?" (System testing)
  ✅ [Structural Coverage Analysis](Structural_Coverage_Analysis.rst) — MC/DC, Decision, Statement coverage
  ✅ [Test Case Development](Test_Case_Development.rst) — Creating test cases per requirements
  ✅ [Integration Testing](Integration_Testing.rst) — Module-to-module interface testing

---

🎯 **TRACEABILITY & QUALITY (Continuous Throughout)**
  🎯 [Traceability](Traceability.rst) — Bidirectional linkage (Req→Code→Test→Proof)
  🎯 [Software Quality Assurance (SQA)](SQA.rst) — Independent audits, process compliance
  🎯 [Independence](Independence.rst) — Verifier ≠ Developer (conflict-of-interest prevention)
  🎯 [Configuration Management (CM)](Configuration_Management.rst) — Version control, baselines, change control

---

🔧 **INTEGRAL & SUPPORTING PROCESSES**
  🔧 [Integral Processes](Integral_Processes.rst) — Verification, SQA, CM, Certification Liaison (parallel to dev)
  🔧 [Lifecycle Data](Lifecycle_Data.rst) — Artifacts as evidence (plans, reviews, tests, traces)
  🔧 [Formal Methods](Formal_Methods.rst) — Mathematical proofs (DO-333 supplement, rare)
  🔧 [Tool Qualification](Tool_Qualification.rst) — DO-330 qualification (compilers, analyzers, generators)

---

🏛️ **CERTIFICATION & AUTHORITY (Compliance Phase)**
  🏛️ [Certification Liaison](Certification_Liaison.rst) — Interface with FAA/EASA, SOI management
  🏛️ [Stage of Involvement (SOI)](SOI.rst) — Structured authority gates (#1–#4)
  🏛️ [Designated Engineering Representative (DER)](DER.rst) — FAA approval authority (expensive but critical)
  🏛️ [Compliance Verification Engineer (CVE)](CVE.rst) — EASA equivalent to DER (European)
  🏛️ [Process Assurance](Process_Assurance.rst) — SQA audits ensuring compliance with plans

---

📊 **AUDITING & COMPLIANCE (Audit Phase)**
  📊 [Objective Evidence](Objective_Evidence.rst) — Verifiable records proving compliance (reviews, tests, traces)
  📊 [Software Aspects of Certification (SOI Audits)](SOI_Audits.rst) — Authority audits of processes/artifacts
  📊 [Corrective Action](Corrective_Action.rst) — Resolving non-conformances (root cause + prevention)
  📊 [Gap Analysis](Gap_Analysis.rst) — Assessment of processes vs. DO-178C (before certification)

---

⚖️ **REGULATORY FRAMEWORKS (Authority Expectations)**
  ⚖️ [FAA Order 8110.49](FAA_Order_8110.49.rst) — FAA-specific software approval guidance
  ⚖️ [EASA AMC 20-115D](EASA_AMC_20-115D.rst) — EASA guidance (often stricter than FAA)
  ⚖️ [Continued Airworthiness](Continued_Airworthiness.rst) — Post-certification updates, fleet management

---

🎯 **QUICK LOOKUP BY ACTIVITY**
===============================

**"I'm just starting my project — what do I need?"**
  1. Read: [DO-178C](DO-178C.rst) overview
  2. Understand: [DAL](DAL.rst) (what's your safety criticality?)
  3. Reference: [ARP4754A](ARP4754A.rst) (system-level context)
  4. Create: [PSAC](PSAC.rst) (your certification roadmap)

**"I'm in planning phase — what's important?"**
  1. Read: [Planning Process](Planning_Process.rst)
  2. Create: [Software Development Plan](Software_Development_Plan.rst), [SQAP](SQA.rst), [SVP](Verification.rst)
  3. Understand: [Traceability](Traceability.rst) strategy
  4. Plan: [Certification Liaison](Certification_Liaison.rst) with authorities ([SOI](SOI.rst) gates)

**"I'm in development phase — how do I stay compliant?"**
  1. Manage: [Traceability](Traceability.rst) (HLR→LLR→Code links)
  2. Review: Code per standards, design reviews
  3. Monitor: [Configuration Management](Configuration_Management.rst) (version control, baselines)
  4. Coordinate: [SQA](SQA.rst) audits (monthly, catch deviations early)

**"I'm testing — what coverage do I need?"**
  1. Target: [Structural Coverage Analysis](Structural_Coverage_Analysis.rst) (MC/DC 100% for DAL A/B)
  2. Create: [Test Case Development](Test_Case_Development.rst) (trace each test to requirement)
  3. Execute: [Verification](Verification.rst) (unit → integration → system testing)
  4. Document: [Objective Evidence](Objective_Evidence.rst) (test results, coverage reports)

**"I'm preparing for audit — am I ready?"**
  1. Verify: [Traceability](Traceability.rst) complete (forward & backward, 100% coverage)
  2. Check: [Objective Evidence](Objective_Evidence.rst) (all reviews documented, test results, coverage proof)
  3. Review: [Gap Analysis](Gap_Analysis.rst) (no deviations from plan)
  4. Prepare: [SOI Audits](SOI_Audits.rst) (know what auditors will examine)

---

📊 **KEYWORD BY PHASE: Development Lifecycle**
==============================================

```
┌─────────────────────────────────────────────────────────────┐
│ PROJECT START: Planning Phase (Months 1–3)                  │
├─────────────────────────────────────────────────────────────┤
│ DO-178C (overview), DAL (determine level), ARP4754A (system) │
│ Planning Process, SDP, PSAC, SQA Plan, SVP                  │
│ Certification Liaison, SOI gates, DER/CVE involvement       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ DEVELOPMENT: Requirements & Design (Months 4–10)            │
├─────────────────────────────────────────────────────────────┤
│ HLR, LLR, Derived Requirements                              │
│ Software Development Process, MBD/OOT, Formal Methods       │
│ Traceability (HLR→LLR→Code links), Configuration Management │
│ SQA audits (continuous), Independence boundaries            │
│ Tool Qualification (compilers, analyzers)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TESTING: Verification & Validation (Months 9–18)            │
├─────────────────────────────────────────────────────────────┤
│ Test Case Development, Verification, Validation             │
│ Structural Coverage Analysis (MC/DC 100% for DAL A/B)       │
│ Integration Testing, System-level testing                   │
│ Objective Evidence collection (reviews, tests, traces)      │
│ Traceability (Req→Test→Result validation)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CERTIFICATION: Audit & Approval (Months 18–24)              │
├─────────────────────────────────────────────────────────────┤
│ SOI Audits (#2, #3, #4), Process Assurance, Gap Analysis    │
│ Corrective Action (resolve non-conformances)                │
│ DER/CVE review & approval                                   │
│ Software Accomplishment Summary (SAS) approval              │
│ Airworthiness approval → Aircraft installation              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ POST-CERTIFICATION: Continued Airworthiness (Years 2+)      │
├─────────────────────────────────────────────────────────────┤
│ Continued Airworthiness (updates, patches, fleet management)│
│ Configuration Management (post-deployment changes)          │
│ Problem Reporting (defect tracking, Airworthiness Directives)
└─────────────────────────────────────────────────────────────┘
```

---

🎓 **LEARNING PATHS: Recommended Reading Sequences**
====================================================

**Path 1: "I'm New to DO-178C" (1–2 weeks)**
  Week 1:
    📖 [DO-178C](DO-178C.rst) (overview, 5-level structure, fundamental concepts)
    📖 [DAL](DAL.rst) (understand safety criticality A→E)
    📖 [ARP4754A](ARP4754A.rst) (system-level context)
  Week 2:
    📖 [PSAC](PSAC.rst) (certification roadmap)
    📖 [Verification](Verification.rst) (testing & proof concepts)
    📖 [Traceability](Traceability.rst) (requirement linkage)

**Path 2: "I'm a Test Lead" (2–3 weeks)**
  Focus on:
    📖 [Verification](Verification.rst) (core testing methodology)
    📖 [Structural Coverage Analysis](Structural_Coverage_Analysis.rst) (MC/DC targets)
    📖 [Test Case Development](Test_Case_Development.rst) (creating test cases)
    📖 [Validation](Validation.rst) (system-level testing)
    📖 [Objective Evidence](Objective_Evidence.rst) (documentation requirements)

**Path 3: "I'm a Certification Manager" (3–4 weeks)**
  Focus on:
    📖 [PSAC](PSAC.rst) (certification strategy)
    📖 [Certification Liaison](Certification_Liaison.rst) (authority interaction)
    📖 [SOI](SOI.rst) (gate management)
    📖 [Process Assurance](Process_Assurance.rst) (SQA oversight)
    📖 [SOI Audits](SOI_Audits.rst) (audit readiness)
    📖 [FAA Order 8110.49](FAA_Order_8110.49.rst), [EASA AMC 20-115D](EASA_AMC_20-115D.rst)

**Path 4: "I'm a Software Architect" (2–3 weeks)**
  Focus on:
    📖 [Software Development Process](Software_Development_Process.rst) (lifecycle overview)
    📖 [HLR](HLR.rst), [LLR](LLR.rst), [Derived Requirements](Derived_Requirements.rst)
    📖 [Traceability](Traceability.rst) (requirement linkage strategy)
    📖 [MBD](MBD.rst), [OOT](OOT.rst) (if using these technologies)
    📖 [Configuration Management](Configuration_Management.rst) (version control strategy)

**Path 5: "I'm SQA/Quality Lead" (2–3 weeks)**
  Focus on:
    📖 [SQA](SQA.rst) (quality assurance role)
    📖 [Traceability](Traceability.rst) (evidence verification)
    📖 [Process Assurance](Process_Assurance.rst) (audit methodology)
    📖 [Gap Analysis](Gap_Analysis.rst) (compliance assessment)
    📖 [Corrective Action](Corrective_Action.rst) (problem resolution)

---

🎯 **QUICK REFERENCE: Definitions At-A-Glance**
===============================================

| **Term** | **Definition** |
|:---------|:--------------|
| **DAL** | Development Assurance Level (A→B→C→D→E, catastrophic to no safety effect) |
| **HLR** | High-Level Requirement (system-derived, safety-related software requirement) |
| **LLR** | Low-Level Requirement (detailed software requirement traceable to HLR) |
| **MC/DC** | Modified Condition/Decision Coverage (100% coverage target for DAL A/B) |
| **PSAC** | Plan for Software Aspects of Certification (compliance roadmap, submitted to authorities) |
| **SDP** | Software Development Plan (schedules, resources, standards) |
| **SQAP** | Software Quality Assurance Plan (SQA audit strategy) |
| **SOI** | Stage of Involvement (authority review gates: #1 Planning, #2 Kickoff, #3 Development, #4 Final) |
| **SFR** | Software Functional Requirements Review (verify HLRs) |
| **PDR** | Preliminary Design Review (verify design concept) |
| **CDR** | Critical Design Review (verify detailed design) |
| **FVR** | Final Verification Review (confirm all objectives met) |
| **DER** | Designated Engineering Representative (FAA approval authority) |
| **CVE** | Compliance Verification Engineer (EASA approval authority) |

---

💡 **HOW TO USE THIS COLLECTION**
=================================

**As a Reference Library:**
  🔍 Find your keyword in the index above
  🔍 Click the link (or search the folder)
  🔍 Read the cheatsheet (5–15 minutes per keyword)
  🔍 Learn the essentials, bookmark for later reference

**As a Learning Path:**
  📚 Pick your role (Test Lead, Architect, Certification Manager, etc.)
  📚 Follow the recommended reading sequence
  📚 Spend 1–2 weeks becoming familiar with your specialty keywords
  📚 Go deeper into related keywords as needed

**As a Project Checklist:**
  ✅ Bookmark cheatsheets relevant to your current project phase
  ✅ Use as gate review checklist (did we cover this keyword's requirements?)
  ✅ Reference during meetings ("What's the definition of MC/DC again?")
  ✅ Share with team (onboarding, quick reference)

**As a Compliance Tool:**
  📋 Match cheatsheet keywords to PSAC sections
  📋 Verify PSAC descriptions match cheatsheet requirements
  📋 Prepare audit answers (cheatsheets provide context)
  📋 Demonstrate compliance (cheatsheets prove understanding)

---

✨ **COLLECTION STATS**
======================

**Coverage:**
  🎯 36 individual keyword cheatsheets
  🎯 ~250 KB total content (50+ pages equivalent)
  🎯 ~8,000 lines of richly-formatted knowledge

**Organization:**
  🎯 Grouped by lifecycle phase (Planning → Development → Verification → Certification)
  🎯 Linked to related keywords (cross-references)
  🎯 Color-coded by priority (Critical, Important, Reference)
  🎯 Includes practical examples, real-world lessons, common mistakes

**Quality:**
  ✅ All keywords from Avionics SE Process.rst
  ✅ Comprehensive (TL;DR, pro tips, pitfalls, learning paths)
  ✅ Practical (real examples, tools, templates)
  ✅ Memorable (emojis, quick reference tables, bottom-line summaries)

---

📞 **NAVIGATION TIPS**
=====================

**Finding Keywords Quickly:**
  1. Use browser Find (Ctrl+F or Cmd+F)
  2. Search for keyword name in filename
  3. Example: `Verification.rst` for "Verification"

**Cross-References:**
  Each cheatsheet includes links to related keywords
  Example: [Verification](Verification.rst) links to [Structural Coverage Analysis](Structural_Coverage_Analysis.rst)

**File Organization:**
  ```
  Avionics/SE_Keywords/
  ├── DO-178C.rst
  ├── DAL.rst
  ├── PSAC.rst
  ├── ... (30+ more)
  └── INDEX.rst (this file)
  ```

---

🎓 **RECOMMENDED FIRST READS**
==============================

**If you have 15 minutes:**
  Read: [DO-178C](DO-178C.rst) (5-level structure overview)

**If you have 30 minutes:**
  Read: [DO-178C](DO-178C.rst) + [DAL](DAL.rst) (understand safety criticality)

**If you have 1 hour:**
  Read: [DO-178C](DO-178C.rst) + [DAL](DAL.rst) + [PSAC](PSAC.rst) (certification roadmap)

**If you have 2 hours:**
  Read: [DO-178C](DO-178C.rst) + [DAL](DAL.rst) + [PSAC](PSAC.rst) + [Verification](Verification.rst) + [Traceability](Traceability.rst)

---

✨ **BOTTOM LINE**
=================

**This collection = Your DO-178C survival guide!**

✅ 36 comprehensive keyword cheatsheets
✅ Covers all phases (Planning → Development → Verification → Certification)
✅ Multiple learning paths (test lead, architect, certification manager, etc.)
✅ Practical, memorable, reference-friendly
✅ Color-coded, emoji-enhanced, bottom-line focused

**Use it daily. Share it with your team. Pass certification with confidence!** 🎯

---

**Last updated:** 2026-01-12 | **SE Process Keywords Complete Reference Library**

**Next Steps:**
  1. Bookmark this INDEX
  2. Read DO-178C, DAL, PSAC first (foundation)
  3. Pick your role's learning path
  4. Reference keywords as needed throughout project
  5. Success! 🛡️
