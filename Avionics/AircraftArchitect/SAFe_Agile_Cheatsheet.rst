🔄 **SAFe (Scaled Agile Framework) — Aviation Cheatsheet**
══════════════════════════════════════════════════════════

**Framework:** Scaled Agile Framework for Lean Enterprises  
**Version:** SAFe 6.0 (2023)  
**Authority:** Scaled Agile, Inc.  
**Application:** Large-scale aerospace/defense programs with compliance requirements

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **WHAT IS SAFe?**
────────────────────

SAFe is a **framework for scaling agile practices** to large organizations with 
multiple teams working on complex systems. In aerospace, it enables agile development 
while maintaining compliance with standards like DO-178C and ED-203A.

**SAFe Configurations:**

| Configuration | Teams | Use Case | Complexity |
|:--------------|:------|:---------|:-----------|
| **Essential SAFe** | 1 ART (50-125 people) | Single value stream | Low |
| **Large Solution SAFe** | Multiple ARTs | Complex solutions | Medium |
| **Portfolio SAFe** | Enterprise-wide | Strategic alignment | High |
| **Full SAFe** | All layers | Complete transformation | Very High |

**For Aircraft Services:** **Essential SAFe** or **Large Solution SAFe**

════════════════════════════════════════════════════════════════════

🚂 **AGILE RELEASE TRAIN (ART)**
─────────────────────────────────

**Definition:** Long-lived team of agile teams (50-125 people) that delivers value 
on a regular cadence through Program Increments (PIs).

**ART Structure:**

```
                    Release Train Engineer (RTE)
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   Agile Team 1         Agile Team 2         Agile Team 3
   (5-11 people)        (5-11 people)        (5-11 people)
        │                    │                    │
    ┌───┴───┐            ┌───┴───┐            ┌───┴───┐
    Dev Test Scrum       Dev Test Scrum       Dev Test Scrum
            Master               Master               Master
```

**ART Roles:**

👤 **Release Train Engineer (RTE):**
- Chief Scrum Master for the ART
- Facilitates PI Planning and Inspect & Adapt
- Escalates impediments
- Manages risk and dependencies

👤 **Product Management:**
- Defines and prioritizes Program Backlog
- Represents customer voice
- Content authority for features

👤 **System Architect:**
- Technical leadership for the ART
- Defines architectural runway
- Works with teams on technical direction

👤 **Business Owners:**
- Key stakeholders who fund/govern the ART
- Set business objectives
- Participate in PI Planning

════════════════════════════════════════════════════════════════════

📅 **PROGRAM INCREMENT (PI)**
─────────────────────────────

**Definition:** Fixed timebox (8-12 weeks) during which an ART delivers incremental 
value through multiple iterations.

**PI Structure (Typical 10-week PI):**

```
┌─────────────────────────────────────────────────────────────┐
│ PI PLANNING (2 days)                                        │
│  Day 1: Vision, Context, Team Planning                      │
│  Day 2: Draft Plan, Risk Review, Confidence Vote            │
└─────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────┐
│ ITERATION 1 (2 weeks)                                       │
│  ├─ Sprint Planning                                         │
│  ├─ Daily Standup                                           │
│  ├─ Development & Testing                                   │
│  └─ Sprint Review & Retrospective                           │
└─────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────┐
│ ITERATION 2-4 (6 weeks)                                     │
│  └─ Same cadence as Iteration 1                             │
│                                                             │
│ Every 2 weeks: System Demo (integrated solution)           │
└─────────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────────┐
│ INNOVATION & PLANNING SPRINT (2 weeks)                      │
│  ├─ Innovation: Hackathons, technical debt reduction        │
│  ├─ Training: Learning new technologies                     │
│  ├─ Planning: Prepare for next PI                           │
│  └─ Inspect & Adapt (I&A) Workshop                          │
└─────────────────────────────────────────────────────────────┘
```

**PI Objectives:**

Each team commits to **PI Objectives** with **Business Value** assigned:

```
Example PI Objective:
  "Complete IFE authentication module with OAuth 2.0 support"
  Business Value: 8/10
  Stretch: "Add biometric authentication support"
  Business Value: 3/10
```

════════════════════════════════════════════════════════════════════

🎯 **PI PLANNING EVENT**
────────────────────────

**The heartbeat of SAFe** — All teams come together to plan the next 10 weeks.

**Day 1 Agenda:**

```
08:00 - 09:00  Business Context (Product Management)
09:00 - 09:30  Product Vision (Product Owner)
09:30 - 10:00  Architecture Vision (System Architect)
10:00 - 11:30  Team Breakouts: Draft Plan
11:30 - 12:00  Team Draft Plan Reviews
12:00 - 13:00  Lunch
13:00 - 15:00  Team Breakouts: Finalize Draft Plan
15:00 - 16:00  Draft Plan Presentations
16:00 - 16:30  Parking Lot (Risks & Impediments)
```

**Day 2 Agenda:**

```
08:00 - 09:00  Planning Adjustments
09:00 - 12:00  Team Breakouts: Finalize Plan
12:00 - 13:00  Lunch
13:00 - 14:00  Final Plan Review
14:00 - 14:30  Program Risk Review (ROAM Board)
14:30 - 15:00  PI Confidence Vote
15:00 - 15:30  Planning Retrospective
```

**Confidence Vote:**

Each person holds up fingers (1-5) indicating confidence in achieving PI objectives:

- **5 fingers:** High confidence
- **4 fingers:** Mostly confident
- **3 fingers:** Neutral (target minimum)
- **2 fingers:** Low confidence (need to address)
- **1 finger:** No confidence (replanning required)

**Target:** Average 3+ fingers across all participants

════════════════════════════════════════════════════════════════════

🎨 **PROGRAM BOARD**
────────────────────

Visual representation of PI plan showing features, dependencies, and milestones:

```
             Iteration 1  Iteration 2  Iteration 3  Iteration 4  IP Sprint
Team 1       [Feature 1]  [Feature 2]  [Feature 3]  
             ────────────────────────────────────▶
Team 2                    [Feature 4]  [Feature 5]  [Feature 6]
                          ─────────────────────────────────────▶
Team 3       [Feature 7]               [Feature 8]
             ──────────────────────────────────────────────────▶

Dependencies: ──────────────┐
                            ▼
Milestones:   🎯 Safety Review (Iteration 2)
              🎯 Security Audit (Iteration 3)
              🎯 Certification Readiness (IP Sprint)
```

**Dependency Types:**

🔴 **Critical:** Blocking dependency  
🟡 **High Risk:** Possible blocker  
🟢 **Low Risk:** Informational

════════════════════════════════════════════════════════════════════

🔍 **INSPECT & ADAPT (I&A)**
────────────────────────────

**Purpose:** Reflect on the PI and identify improvements.

**I&A Workshop Structure:**

```
Part 1: PI System Demo (60 min)
  └─ Integrated solution demonstration to stakeholders

Part 2: Quantitative Measurement (30 min)
  ├─ Program Predictability Measure
  ├─ Velocity trends
  ├─ Defect trends
  └─ Quality metrics

Part 3: Problem-Solving Workshop (2-3 hours)
  ├─ Step 1: Identify problems
  ├─ Step 2: Vote on top problems
  ├─ Step 3: Root cause analysis (5 Whys, Fishbone)
  ├─ Step 4: Brainstorm solutions
  └─ Step 5: Create improvement backlog items
```

**Program Predictability Measure:**

```
Planned Business Value: 100 points
Achieved Business Value: 85 points
Predictability = 85%

Target: > 80% predictability
```

════════════════════════════════════════════════════════════════════

🛡️ **SAFe FOR AVIATION COMPLIANCE**
────────────────────────────────────

**Challenge:** Agile vs. DO-178C waterfall expectations

**Solution:** **Continuous Compliance**

**Mapping SAFe to DO-178C:**

| DO-178C Artifact | SAFe Practice | When Created |
|:-----------------|:--------------|:-------------|
| **PSAC** | Program Backlog item | PI 0 (setup) |
| **SDP/SVP/SCMP/SQAP** | Definition of Done | PI 0 (setup) |
| **HLR** | Features & Stories | Each PI |
| **LLR** | Acceptance Criteria | Each Sprint |
| **Source Code** | Sprint Deliverables | Each Sprint |
| **Test Cases** | Acceptance Tests (BDD) | Each Sprint |
| **Test Results** | CI/CD Pipeline | Continuous |
| **Traceability** | ALM Tool (Jira, Codebeamer) | Continuous |
| **SAS** | Aggregated at milestones | Each PI |

**Key Practices:**

✅ **Automated Testing:** CI/CD pipeline runs tests every commit  
✅ **Continuous Documentation:** Docs generated from code (Doxygen, Sphinx)  
✅ **Incremental Reviews:** Code review in every pull request  
✅ **Traceability Automation:** Tools link requirements → code → tests  
✅ **SQA Integrated:** SQA attends all ceremonies, provides real-time feedback

**Example: DO-178C DAL D with SAFe:**

```
Sprint 1:
  ├─ HLR defined in User Stories
  ├─ LLR in Acceptance Criteria
  ├─ Code developed & reviewed
  ├─ Unit tests executed (statement coverage)
  ├─ Traceability links updated
  └─ SQA audits Definition of Done

Sprint 2:
  ├─ Integration testing
  ├─ System-level verification
  ├─ Coverage analysis (automated)
  ├─ Defect tracking & resolution
  └─ SQA reviews test evidence

IP Sprint:
  ├─ Documentation review
  ├─ Compliance verification
  ├─ SAS section completion
  └─ Certification Authority interaction
```

════════════════════════════════════════════════════════════════════

📊 **KEY METRICS**
──────────────────

**Program-Level Metrics:**

📈 **Program Predictability Measure (PPM):**
- Percentage of planned business value delivered
- Target: > 80%

📈 **Velocity:**
- Story points completed per iteration
- Track trends, not absolute numbers

📈 **Quality:**
- Defect density (defects per KLOC)
- Escaped defects (found post-release)
- Test coverage percentage

📈 **Flow Efficiency:**
- Active time / Total time
- Target: > 40%

**Team-Level Metrics:**

📊 Sprint Burndown  
📊 Team Velocity  
📊 Defect Removal Efficiency  
📊 Code Review Turnaround Time

════════════════════════════════════════════════════════════════════

⚠️ **COMMON PITFALLS**
──────────────────────

**❌ Fake PI Planning:**
- Problem: Pre-planned work, not collaborative planning
- Solution: Genuine breakouts, emergent planning

**❌ Waterfall in Sprints:**
- Problem: Each sprint has analysis, design, code, test phases
- Solution: Cross-functional teams, incremental delivery

**❌ Ignoring Dependencies:**
- Problem: Teams plan in isolation, dependencies cause delays
- Solution: Dependency visualization, cross-team coordination

**❌ No System Demo:**
- Problem: Teams demo individually, no integrated view
- Solution: Mandatory integrated system demo every 2 weeks

**❌ Skipping I&A:**
- Problem: No continuous improvement, repeating same mistakes
- Solution: Mandatory I&A workshop, action items tracked

════════════════════════════════════════════════════════════════════

✨ **QUICK REFERENCE CARD**
───────────────────────────

**SAFe in 10 Points:**

1. 🚂 **ART is the core:** 50-125 people, single value stream
2. 📅 **PI is 8-12 weeks:** Fixed cadence for planning & delivery
3. 🎯 **PI Planning is sacred:** 2-day event, everyone participates
4. 🔄 **Iterations are 2 weeks:** Standard sprint length
5. 🎨 **System Demo every 2 weeks:** Integrated solution
6. 🚀 **IP Sprint for innovation:** Last iteration for tech debt, learning
7. 🔍 **I&A for improvement:** Reflect & adapt at PI end
8. 📊 **Predictability > 80%:** Key success metric
9. 👥 **Cross-functional teams:** Dev, test, QA together
10. 🛡️ **Continuous compliance:** For DO-178C, ED-203A

**PI Planning Checklist:**

✅ Business context presented  
✅ Product vision shared  
✅ Architecture vision explained  
✅ Teams create draft plans  
✅ Dependencies identified  
✅ Risks documented (ROAM board)  
✅ Confidence vote conducted (target: 3+)  
✅ PI objectives committed  
✅ Program board created  
✅ Management review & approval

════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────

**Q1: What is an Agile Release Train?**
→ Long-lived team of agile teams (50-125 people) delivering value on a fixed cadence

**Q2: How long is a typical Program Increment?**
→ 8-12 weeks (typically 10 weeks = 4 iterations + 1 IP sprint)

**Q3: What happens during the Innovation & Planning Sprint?**
→ Innovation (hackathons, tech debt), training, PI planning prep, I&A workshop

**Q4: What is the minimum confidence vote target?**
→ Average 3+ fingers (out of 5) across all participants

**Q5: How does SAFe support DO-178C compliance?**
→ Continuous compliance through automated testing, traceability, and incremental documentation

════════════════════════════════════════════════════════════════════

📚 **FURTHER READING**
──────────────────────

📖 SAFe 6.0 Framework (scaledagileframework.com)  
📖 "SAFe 6.0 Distilled" — Richard Knaster & Dean Leffingwell  
📖 "Agile Software Development in the Large" — Jutta Eckstein  
📖 "Scaling Software Agility" — Dean Leffingwell  
📖 SAFe Certifications: SA (Agilist), POPM, RTE, SP, SSM

════════════════════════════════════════════════════════════════════

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Target Audience:** Aircraft Services Architects, Agile Coaches, Program Managers
