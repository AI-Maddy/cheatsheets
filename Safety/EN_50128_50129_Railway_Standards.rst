🚆 **EN 50128 / EN 50129: Railway Signalling & Safety Systems Standards**
════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for Railway Safety-Critical Systems**  
**Standards:** EN 50128 (Software) | EN 50129 (Systems) | CENELEC  
**Domains:** Railway 🚆 | Metro 🚇 | Tramway 🚊 | Signalling ⚡  
**Purpose:** Railway certification, safety case development, SIL compliance

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What are EN 50128 and EN 50129?**
European standards for railway signalling and control/protection systems

**Key Concepts:**

```
Railway Safety → SIL Classification → Software/System Development → Safety Case
        ↓                ↓                      ↓                        ↓
  Hazard Analysis    SIL 0-4           EN 50128/50129              Acceptance
```

**Railway Safety Integrity Levels (SIL):**

| SIL | Tolerable Hazard Rate | Risk Level | Examples |
|:---:|:---------------------:|:-----------|:---------|
| **4** | 10⁻⁹ to 10⁻⁸ /hr | Catastrophic | Interlocking, ATP, train control |
| **3** | 10⁻⁸ to 10⁻⁷ /hr | Critical | Level crossing, track circuits |
| **2** | 10⁻⁷ to 10⁻⁶ /hr | Marginal | Warning systems, operator aids |
| **1** | 10⁻⁶ to 10⁻⁵ /hr | Negligible | Information displays |
| **0** | > 10⁻⁵ /hr | Non-safety | Passenger info, entertainment |

**Core Processes:**

✅ **EN 50128 (Software)** → Requirements → Design → Code → Test → Validation  
✅ **EN 50129 (Systems)** → Safety case → Evidence → Technical Safety Report  
✅ **SIL Assignment** → Hazard analysis → Risk assessment → SIL allocation  
✅ **Lifecycle** → Development → Validation → Assessment → Operation

════════════════════════════════════════════════════════════════════════════

📖 **INTRODUCTION**
───────────────────

Standards Background
~~~~~~~~~~~~~~~~~~~~

**EN 50128: Railway applications — Communication, signalling and processing systems — Software for railway control and protection systems**

**Published by:**
- **CENELEC** (European Committee for Electrotechnical Standardization)
- Originally published: 2001, Updated: 2011, Latest: 2011 + A1:2020

**EN 50129: Railway applications — Communication, signalling and processing systems — Safety related electronic systems for signalling**

**Published by:**
- **CENELEC**
- Originally published: 2003, Updated: 2018

**Scope:**

**EN 50128 covers:**
- Software for railway control systems (interlocking, ATP, ATO, ETCS)
- Software development lifecycle
- Software safety requirements & techniques
- Software V&V, validation, assessment

**EN 50129 covers:**
- Safety-related electronic systems (hardware + software)
- System safety lifecycle
- Safety case structure & content
- Technical Safety Report (TSR)
- Safety approval process

**Geographic Coverage:**
- **EU:** Mandatory for TSI (Technical Specifications for Interoperability)
- **UK:** Adopted as BS EN 50128/50129
- **Global:** Widely referenced (Australia, Asia, Middle East)

**Why Railway Standards?**

Railway accidents caused by software/system failures:
- **Ladbroke Grove (1999):** 31 deaths, ATP system not operational
- **Eschede (2000):** Metro collision, signalling software error
- **Santiago de Compostela (2013):** 79 deaths, speed control failure

**Relationship to Other Standards:**

```
IEC 61508 (Generic Functional Safety)
      ↓
EN 50126 (Railway Reliability, Availability, Maintainability, Safety - RAMS)
      ↓
┌─────────────────┬─────────────────┐
│                 │                 │
EN 50128         EN 50129         EN 50657 (Assurance)
(Software)       (Systems)        (Assessment)
      ↓                 ↓                 ↓
  ETCS Level 2    Interlocking    Independent Safety
  Software        System          Assessment (ISA)
```

════════════════════════════════════════════════════════════════════════════

🎯 **SAFETY INTEGRITY LEVELS (SIL)**
────────────────────────────────────

SIL Classification
~~~~~~~~~~~~~~~~~~

**EN 50129 defines 5 SIL levels (0-4):**

**SIL 4 — Catastrophic:**

**Definition:**  
Intolerable risk: Multiple deaths, major environmental damage

**Tolerable Hazard Rate (THR):**  
10⁻⁹ to 10⁻⁸ hazardous events per hour

**Examples:**
- **Interlocking systems:** Prevents conflicting train movements
- **Automatic Train Protection (ATP):** Enforces speed limits, prevents collisions
- **Train control centers:** Centralized traffic control
- **ETCS Level 2/3:** European Train Control System

**Requirements:**
- ✅ Comprehensive hazard analysis (HAZOP, FTA, FMEA)
- ✅ Diverse redundancy (2oo3, 2oo2D architectures)
- ✅ Formal methods or exhaustive testing
- ✅ Independent Safety Assessment (ISA)
- ✅ Full safety case with quantitative evidence

**SIL 3 — Critical:**

**Definition:**  
High risk: Single death or serious multiple injuries

**THR:** 10⁻⁸ to 10⁻⁷ /hr

**Examples:**
- **Level crossing protection:** Barriers, lights, detection
- **Track circuits:** Detect train presence
- **Axle counters:** Track occupancy detection
- **Points (turnouts) control:** Switch track paths

**Requirements:**
- ✅ Systematic hazard analysis
- ✅ Redundancy (1oo2D or better)
- ✅ Extensive testing or formal methods
- ✅ Independent review
- ✅ Safety case with qualitative/quantitative evidence

**SIL 2 — Marginal:**

**Definition:**  
Moderate risk: Minor injuries to multiple people

**THR:** 10⁻⁷ to 10⁻⁶ /hr

**Examples:**
- **Warning systems:** Platform edge warnings, train approach alarms
- **Operator advisory systems:** Speed advisories, scheduling aids
- **Door control systems:** Train door interlocks

**Requirements:**
- ✅ Hazard analysis
- ✅ Design verification
- ✅ Structured testing
- ✅ Safety case

**SIL 1 — Negligible:**

**Definition:**  
Low risk: Possible single minor injury

**THR:** 10⁻⁶ to 10⁻⁵ /hr

**Examples:**
- **Passenger information displays:** Real-time train info
- **Station announcement systems**
- **CCTV monitoring (non-safety)**

**SIL 0 — Non-safety:**

**Definition:**  
No safety impact

**THR:** > 10⁻⁵ /hr

**Examples:**
- **Entertainment systems**
- **Wi-Fi networks**
- **Ticketing systems** (unless safety-related)

SIL Allocation Process
~~~~~~~~~~~~~~~~~~~~~~

**Step 1: System Hazard Analysis**

Identify hazards using:
- **HAZOP:** Structured brainstorming with guide words
- **FTA:** Top-down deductive fault tree
- **FMEA:** Bottom-up failure modes analysis

**Example Hazard:**
```
Hazard: Train passes red signal (SPAD - Signal Passed At Danger)
Consequence: Collision with another train
Severity: Catastrophic (multiple deaths)
```

**Step 2: Risk Assessment**

Evaluate risk using **Risk Matrix** (Severity × Frequency):

| Frequency | Catastrophic | Critical | Marginal | Negligible |
|:----------|:-------------|:---------|:---------|:-----------|
| Frequent | SIL 4 | SIL 3 | SIL 2 | SIL 1 |
| Probable | SIL 4 | SIL 3 | SIL 2 | SIL 0 |
| Occasional | SIL 3 | SIL 2 | SIL 1 | SIL 0 |
| Remote | SIL 2 | SIL 1 | SIL 0 | — |
| Improbable | SIL 1 | SIL 0 | — | — |

**Step 3: SIL Allocation**

Assign SIL to each safety function:

```
Safety Function: Prevent SPAD
→ Hazard: Train collision (Catastrophic)
→ Frequency before mitigation: Probable
→ Required SIL: SIL 4
→ Allocated to: ATP system (SIL 4)
```

**Step 4: Apportionment**

Distribute SIL across subsystems (hardware + software):

```
ATP System (SIL 4 overall)
├── Onboard Computer (SIL 4)
│   ├── Hardware: SIL 4 (diverse redundancy)
│   └── Software: SIL 4 (EN 50128)
├── Track-side Equipment (SIL 4)
│   ├── Balise (SIL 3 + SIL 2 diverse)
│   └── Radio Block Center (SIL 4)
└── Braking Interface (SIL 4)
    └── Diverse actuation (2oo3)
```

════════════════════════════════════════════════════════════════════════════

🏗️ **EN 50128: SOFTWARE LIFECYCLE**
────────────────────────────────────

Software Development Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**EN 50128 Lifecycle Phases:**

```
┌──────────────────────────────────────────────────────────────┐
│ Phase 1: Software Planning & Quality Assurance              │
│   → Software Development Plan, SQAP, V&V Plan               │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 2: Software Requirements                               │
│   → System requirements → Software requirements spec (SRS)   │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 3: Software Architecture & Design                      │
│   → High-level design, module breakdown, interfaces          │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 4: Component Design                                    │
│   → Detailed design for each module/component                │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 5: Software Component Implementation & Test            │
│   → Code modules, unit test, static analysis                 │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 6: Software Integration                                │
│   → Integrate modules, integration testing                   │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 7: Software Validation                                 │
│   → Test against SRS, validation testing                     │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 8: Software Assessment                                 │
│   → Independent Safety Assessor reviews all artifacts        │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 9: Software Approval & Deployment                      │
│   → Safety Authority approves, software released             │
└──────────────────────────────────────────────────────────────┘
```

Phase 1: Software Planning
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required Documents:**

**1. Software Development Plan (SDP)**

Contents:
- Scope & safety requirements
- Development standards (coding, design, testing)
- Lifecycle model (V-model, iterative)
- Tools & environments
- Team roles & responsibilities
- Schedule & milestones

**2. Software Quality Assurance Plan (SQAP)**

Contents:
- QA activities (reviews, audits, inspections)
- Metrics & KPIs
- Non-conformance handling
- Configuration management
- Documentation standards

**3. Software Verification & Validation Plan (SVVP)**

Contents:
- V&V strategy (testing, reviews, analysis)
- Test coverage targets (statement, branch, MC/DC)
- Independence requirements
- Tools for V&V
- Acceptance criteria

**SIL-Specific Requirements:**

| Activity | SIL 0/1 | SIL 2 | SIL 3/4 |
|:---------|:--------|:------|:--------|
| Software Development Plan | R | HR | HR |
| SQAP | R | HR | HR |
| SVVP | R | HR | HR |
| Independent Safety Assessor | — | R | HR |
| Formal methods consideration | — | R | HR |

**Legend:** HR = Highly Recommended, R = Recommended, — = Not required

Phase 2: Software Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Software Requirements Specification (SRS)**

**Contents:**
- Functional requirements (what software does)
- Performance requirements (timing, throughput)
- Interface requirements (hardware, software, user)
- Safety requirements (from hazard analysis)
- Security requirements (cyber security)

**Requirements Quality:**
- ✅ **Complete:** All necessary functions specified
- ✅ **Consistent:** No contradictions
- ✅ **Unambiguous:** Single interpretation
- ✅ **Verifiable:** Can be tested
- ✅ **Traceable:** Linked to system requirements & hazards

**Example SRS Requirement (SIL 4 Interlocking):**

```
REQ-SW-101: Route Locking

Description:
  The software shall prevent route cancellation or modification while 
  a train occupies any section of the route.

Rationale:
  Prevents conflicting train movements (SPAD prevention)

Safety Class: SIL 4

Traceability:
  System Requirement: SYS-REQ-020
  Hazard: HAZ-003 (Train collision due to conflicting routes)
  Risk Control: RC-HAZ-003-01

Verification Method:
  Test Case: TC-SW-101 (simulate train occupation, attempt route change)
  
Acceptance Criteria:
  Route modification rejected while train present (100% pass rate)
```

**Techniques by SIL:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Structured methodology | R | R | HR | HR | HR |
| Semi-formal methods | — | R | R | HR | HR |
| Formal methods | — | — | R | R | HR |
| Traceability | R | R | HR | HR | HR |

Phase 3: Software Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Architecture Definition:**

Define top-level structure:
- **Modules:** Major software components
- **Interfaces:** Communication between modules
- **Data flow:** Information flow through system
- **Safety mechanisms:** Watchdogs, voting, monitoring

**Example Architecture (SIL 4 ATP System):**

```
┌────────────────────────────────────────────────────────────┐
│              ATP Onboard Computer (SIL 4)                  │
├────────────────────────────────────────────────────────────┤
│ Software Module          │ SIL │ Function                  │
├──────────────────────────┼─────┼───────────────────────────┤
│ BaliseReader             │  4  │ Read track data           │
│ SpeedCalculator          │  4  │ Compute train speed       │
│ MovementAuthority        │  4  │ Calculate safe braking    │
│ BrakeController          │  4  │ Command emergency brake   │
├──────────────────────────┼─────┼───────────────────────────┤
│ SafetyMonitor (diverse)  │  4  │ Independent verification  │
│ Watchdog                 │  4  │ Detect hung processes     │
├──────────────────────────┼─────┼───────────────────────────┤
│ HMI (Driver Display)     │  2  │ Show speed, MA status     │
│ DataLogger               │  0  │ Record events             │
└──────────────────────────┴─────┴───────────────────────────┘
```

**Redundancy Strategy:**

```
Primary Channel (2oo2D)
├── Channel A: SpeedCalculator_A → BrakeController_A
├── Channel B: SpeedCalculator_B → BrakeController_B
└── Comparator: Verify A == B, trigger fault if mismatch
```

**Techniques by SIL:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Modular approach | HR | HR | HR | HR | HR |
| Diverse programming | — | — | R | R | HR |
| Safety architecture patterns | — | R | HR | HR | HR |
| Failure analysis (FMEA) | — | R | HR | HR | HR |

Phase 5: Implementation & Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Coding Standards:**

EN 50128 mandates strict coding practices:

**For C/C++:**
- **MISRA C:2012** or **MISRA C++:2008** (Highly Recommended for SIL 3/4)
- Subset of language (avoid dangerous constructs)
- No dynamic memory allocation (for SIL 3/4)
- No recursion (for SIL 3/4)

**Example MISRA-Compliant Code (SIL 4):**

```c
/* MISRA C:2012 Compliant - Speed Limiter */

#include <stdint.h>
#include <stdbool.h>

/* Global constants (MISRA 8.9: static scope) */
static const uint16_t MAX_SPEED_KMH = 160U;
static const uint16_t BRAKE_MARGIN_KMH = 5U;

/* Function: Check if brake required */
bool is_brake_required(uint16_t current_speed_kmh, 
                       uint16_t authorized_speed_kmh) {
    bool brake_needed = false;
    
    /* MISRA 14.4: Boolean controlling expression */
    if (current_speed_kmh > (authorized_speed_kmh + BRAKE_MARGIN_KMH)) {
        brake_needed = true;
    }
    
    /* MISRA 15.5: Single exit point */
    return brake_needed;
}

/* Function: Apply emergency brake */
void apply_emergency_brake(void) {
    /* Direct hardware access (safety-critical) */
    BRAKE_RELAY_PORT |= BRAKE_RELAY_BIT;
    
    /* Verify brake applied (read-back check) */
    if ((BRAKE_STATUS_PORT & BRAKE_STATUS_BIT) == 0U) {
        /* Brake verification failed - trigger diverse backup */
        trigger_diverse_brake();
    }
}
```

**Static Analysis:**

Required for SIL 3/4:
- **Tools:** PC-Lint, Polyspace, LDRA, CodeSonar
- **Checks:** MISRA compliance, data flow, control flow
- **Metrics:** Cyclomatic complexity < 10 (SIL 3/4)

**Unit Testing:**

| Coverage Metric | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------------|:------|:------|:------|:------|:------|
| Statement | — | R | HR | HR | HR |
| Branch | — | R | HR | HR | HR |
| MC/DC | — | — | R | HR | HR |

**MC/DC Example:**

```c
/* Decision: Apply brake if overspeed OR signal at danger */
bool brake = (speed > limit) || (signal == RED);
```

**MC/DC Test Cases:**

| Test | speed > limit | signal == RED | brake | Covers |
|:----:|:-------------:|:-------------:|:-----:|:-------|
| 1 | FALSE | FALSE | FALSE | Both FALSE |
| 2 | TRUE | FALSE | TRUE | speed condition |
| 3 | FALSE | TRUE | TRUE | signal condition |

Phase 7: Software Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Validation Testing:**

Verify software meets SRS (end-to-end):

**Test Environment:**
- **HIL (Hardware-In-Loop):** Real hardware, simulated train/track
- **SIL (Software-In-Loop):** Simulated hardware & environment
- **Field trials:** Real train, controlled scenarios

**Example Validation Test (SIL 4 ATP):**

```
Test Case: TC-VAL-010 — SPAD Prevention

Objective:
  Verify ATP prevents train from passing red signal

Preconditions:
  - Train approaching red signal at 80 km/h
  - Movement Authority (MA) ends before signal
  - Service brake available

Test Procedure:
  1. Start train 1000m before red signal
  2. Set speed to 80 km/h
  3. Set MA end point 50m before signal
  4. Monitor ATP response

Expected Result:
  - ATP calculates emergency brake curve
  - Brake command issued ≥ 100m before signal
  - Train stops ≥ 50m before signal (safety margin)
  - No SPAD event

Actual Result:
  - Brake triggered at 120m before signal ✅
  - Train stopped at 60m before signal ✅
  - Safety margin: 60m (> 50m required) ✅

Verdict: PASS
```

**Validation Coverage:**

- ✅ All SRS requirements tested
- ✅ Normal operation scenarios
- ✅ Boundary conditions (edge cases)
- ✅ Fault injection (sensor failures, communication loss)
- ✅ Environmental stress (temperature, vibration, EMI)

Phase 8: Software Assessment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Independent Safety Assessment (ISA):**

**Who:**  
Independent assessor (not involved in development)

**What:**  
Review all lifecycle artifacts for EN 50128 compliance

**Checklist:**
- ✅ SDP, SQAP, SVVP complete & followed
- ✅ SRS traceable to system requirements & hazards
- ✅ Architecture appropriate for SIL
- ✅ Code complies with standards (MISRA)
- ✅ Test coverage adequate (MC/DC for SIL 3/4)
- ✅ Validation complete (all requirements tested)
- ✅ Configuration management in place
- ✅ Non-conformances resolved

**Assessment Report:**

```
Independent Safety Assessment Report
Software: ATP Onboard System v2.1.0
SIL: 4

Findings:
  - Minor non-conformance: 2 requirements lack MC/DC coverage
    → Resolution: Additional test cases added (TC-SW-205, TC-SW-206)
  - Observation: Cyclomatic complexity = 11 in SpeedCalculator module
    → Resolution: Module refactored, complexity now = 8

Conclusion:
  Software meets EN 50128 requirements for SIL 4.
  Recommend approval for deployment.

Assessor: John Smith, TÜV Rheinland
Date: 2025-11-15
```

════════════════════════════════════════════════════════════════════════════

🏛️ **EN 50129: SYSTEM SAFETY CASE**
────────────────────────────────────

Safety Case Structure
~~~~~~~~~~~~~~~~~~~~~

**EN 50129 Safety Case Contents:**

```
Safety Case
├── 1. Definition of System & Application
│   ├── System description (interlocking, ATP, etc.)
│   ├── Operational context (mainline, metro, tram)
│   ├── System boundaries & interfaces
│   └── Assumptions & constraints
├── 2. Quality Management Report
│   ├── QA processes followed
│   ├── Reviews, audits, inspections
│   └── Non-conformances & resolutions
├── 3. Safety Management Report
│   ├── Hazard log (all identified hazards)
│   ├── Risk assessment (SIL assignment)
│   ├── Safety requirements allocation
│   └── Residual risk evaluation
├── 4. Technical Safety Report (TSR)
│   ├── System architecture (hardware + software)
│   ├── Failure modes analysis (FMEA, FTA)
│   ├── Safety mechanisms (redundancy, monitoring)
│   ├── Software safety (EN 50128 compliance)
│   ├── Hardware safety (fault tolerance, diagnostics)
│   ├── Verification & validation results
│   └── Safety integrity demonstration (SIL proof)
├── 5. Related Safety Cases
│   ├── Generic products used (e.g., PLC, RTOS)
│   ├── Previous applications (proven-in-use)
│   └── Certificates (TÜV, Lloyds Register, etc.)
├── 6. Conclusion
│   ├── Compliance statement (EN 50129 requirements met)
│   ├── Residual risk acceptable
│   └── Recommendation for approval
└── 7. Appendices
    ├── Hazard log
    ├── Test reports
    ├── Configuration index
    └── Assessment reports
```

Technical Safety Report (TSR)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**TSR is the core technical evidence:**

**Example TSR Section (Interlocking System):**

**Section 4.1: System Architecture**

```
┌──────────────────────────────────────────────────────────────┐
│           Interlocking System (SIL 4)                        │
├──────────────────────────────────────────────────────────────┤
│ Subsystem              │ SIL │ Redundancy │ Diagnostics     │
├────────────────────────┼─────┼────────────┼─────────────────┤
│ Input Module (Tracks)  │  4  │ 2oo2       │ Cross-check     │
│ Logic Processor        │  4  │ 2oo2D      │ Diverse CPUs    │
│ Output Module (Points) │  4  │ 2oo2       │ Feedback verify │
│ Power Supply           │  4  │ 1oo2       │ Voltage monitor │
│ Communication          │  3  │ Redundant  │ CRC, timeout    │
└────────────────────────┴─────┴────────────┴─────────────────┘
```

**Section 4.2: Failure Modes Analysis**

```
Component: Logic Processor (2oo2D)

Failure Mode Analysis:
  Single Processor Failure:
    - Detection: Comparator detects mismatch
    - Response: Switch to safe state (all signals RED)
    - Probability: 1×10⁻⁶ /hr (per processor)
    - Diagnostic Coverage: 99.5%
    - Residual: 5×10⁻⁹ /hr ✅ (< SIL 4 target)

  Common Cause Failure:
    - Prevention: Diverse processors (ARM + PowerPC)
    - β-factor: 2% (low due to diversity)
    - Probability: 2×10⁻⁸ × 0.02 = 4×10⁻¹⁰ /hr ✅

  Software Common Mode:
    - Mitigation: EN 50128 SIL 4 process followed
    - Probability: Qualitatively acceptable (systematic)
```

**Section 4.3: Safety Integrity Demonstration**

```
SIL 4 Target: THR < 10⁻⁸ /hr

Quantitative Analysis:
  Hardware dangerous failures: 3×10⁻⁹ /hr
  Software (qualitative): EN 50128 SIL 4 ✅
  Systematic failures: Design reviews, V&V ✅
  
Total Residual Risk: 3×10⁻⁹ /hr < 10⁻⁸ /hr ✅

Conclusion: System meets SIL 4 requirements
```

Proven-in-Use
~~~~~~~~~~~~~

**EN 50129 allows credit for operational experience:**

**Conditions:**
- System operated in similar application
- Sufficient operating time (evidence-based)
- Incident log reviewed (no safety-critical failures)
- Configuration matches (same hardware/software version)

**Example Proven-in-Use Argument:**

```
Product: Interlocking Controller Model XYZ-100
Manufacturer: Siemens Mobility

Previous Application:
  - London Underground, Victoria Line (2015-2025)
  - 10 installations, 24/7 operation
  - Total operating hours: 876,000 hours (100 years equivalent)
  
Safety Record:
  - Zero safety-critical failures
  - 3 non-safety incidents (false alarms, resolved by maintenance)
  
Conclusion:
  Proven-in-use demonstrates THR < 10⁻⁸ /hr (SIL 4)
  Credit: Reduce required evidence for similar application
```

════════════════════════════════════════════════════════════════════════════

⚙️ **TECHNIQUES & METHODS**
───────────────────────────

Software Techniques (EN 50128 Annex A)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Techniques are categorized:**
- **HR:** Highly Recommended (mandatory for compliance in practice)
- **R:** Recommended (should be used unless justified otherwise)
- **—:** Not recommended (or neutral)

**Selected Techniques by SIL:**

**Requirements Phase:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Structured methodology | R | HR | HR | HR | HR |
| Semi-formal methods | — | R | R | HR | HR |
| Formal methods | — | — | R | R | HR |
| Modeling | — | R | HR | HR | HR |

**Design Phase:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Structured design | HR | HR | HR | HR | HR |
| Modular approach | HR | HR | HR | HR | HR |
| Design patterns | R | R | HR | HR | HR |
| Diverse programming | — | — | R | R | HR |

**Implementation Phase:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Coding standards (MISRA) | R | HR | HR | HR | HR |
| Structured programming | HR | HR | HR | HR | HR |
| No dynamic memory | — | R | HR | HR | HR |
| No recursion | — | R | HR | HR | HR |
| Static analysis | R | R | HR | HR | HR |

**Testing Phase:**

| Technique | SIL 0 | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|:----------|:------|:------|:------|:------|:------|
| Boundary value analysis | R | HR | HR | HR | HR |
| Equivalence classes | R | HR | HR | HR | HR |
| Error guessing | R | R | R | R | R |
| Performance testing | R | HR | HR | HR | HR |
| Statement coverage | — | R | HR | HR | HR |
| Branch coverage | — | R | HR | HR | HR |
| MC/DC coverage | — | — | R | HR | HR |

System Techniques (EN 50129)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fault Tolerance Architectures:**

**1oo1 — Single Channel (Not suitable for SIL 3/4):**
```
Input → Processor → Output
(No redundancy, single point of failure)
```

**1oo2 — 1-out-of-2 (Fail-safe, SIL 2/3):**
```
Input ─┬→ Channel A ─┬→ Output
       └→ Channel B ─┘
(Failure in either channel → safe state)
```

**2oo2 — 2-out-of-2 (Fail-safe, SIL 3):**
```
Input → Channel A ──┐
                    AND → Output
Input → Channel B ──┘
(Both must agree, failure → safe state)
```

**2oo2D — 2-out-of-2 with Diagnostics (Fail-safe, SIL 4):**
```
Input → Channel A ──┐
                    AND → Output
Input → Channel B ──┘
       ↓
   Comparator (detects mismatch)
       ↓
   Safe State (if mismatch)
```

**2oo3 — 2-out-of-3 Voting (Fail-operational, SIL 4):**
```
Input ─┬→ Channel A ─┬
       ├→ Channel B ─┼→ Majority Voter → Output
       └→ Channel C ─┘
(Tolerates single channel failure)
```

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS & ANSWERS**
───────────────────────────────

Question 1: What are the 5 SIL levels in EN 50129?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

| SIL | Tolerable Hazard Rate | Risk | Examples |
|:---:|:---------------------:|:-----|:---------|
| **4** | 10⁻⁹ to 10⁻⁸ /hr | Catastrophic | Interlocking, ATP |
| **3** | 10⁻⁸ to 10⁻⁷ /hr | Critical | Level crossing |
| **2** | 10⁻⁷ to 10⁻⁶ /hr | Marginal | Warning systems |
| **1** | 10⁻⁶ to 10⁻⁵ /hr | Negligible | Info displays |
| **0** | > 10⁻⁵ /hr | Non-safety | Entertainment |

Question 2: What is the difference between EN 50128 and EN 50129?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

- **EN 50128:** Software lifecycle standard for railway control/protection systems
  - Covers: Software development process, coding standards, testing, V&V
  - Focus: Software safety requirements & techniques

- **EN 50129:** System safety case standard for signalling electronic systems
  - Covers: Overall system safety (hardware + software), safety case structure
  - Focus: Safety evidence, Technical Safety Report, approval process

**Relationship:**  
EN 50128 compliance is required evidence in the EN 50129 safety case.

Question 3: What is MC/DC and why is it important for SIL 3/4?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**MC/DC (Modified Condition/Decision Coverage):**  
Test coverage metric where every condition in a decision independently affects the outcome.

**Why important:**  
Ensures thorough testing of complex logic in safety-critical code (SIL 3/4).

**Example:**
```c
brake = (speed > limit) || (signal == RED);
```

**MC/DC requires:**
- Test where `speed > limit` changes outcome
- Test where `signal == RED` changes outcome

Question 4: What is 2oo2D architecture?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**2oo2D = 2-out-of-2 with Diagnostics**

- **Dual redundant channels** (both must agree)
- **Comparator** detects mismatch between channels
- **Fail-safe:** Any disagreement → safe state (signals RED, brakes applied)

**Used for:** SIL 4 interlocking, ATP systems

**Benefits:**
- High diagnostic coverage (> 99%)
- Fail-safe behavior
- Suitable for catastrophic hazards

Question 5: What is proven-in-use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**Proven-in-use:**  
EN 50129 concept allowing credit for operational experience.

**Requirements:**
- Sufficient operating time in similar application
- No safety-critical failures in service
- Same configuration (hardware/software version)

**Benefit:**  
Reduces evidence burden for reused components (e.g., off-the-shelf PLCs, proven interlocking controllers).

Question 6: What coding standard is required for SIL 3/4?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**MISRA C:2012** or **MISRA C++:2008** (Highly Recommended)

**Key restrictions for SIL 3/4:**
- ✅ No dynamic memory allocation (malloc/free)
- ✅ No recursion
- ✅ Limited pointer usage
- ✅ No goto statements
- ✅ Explicit variable initialization
- ✅ Single exit point per function

**Rationale:**  
Eliminate undefined behavior and make code deterministic/verifiable.

Question 7: What is a Technical Safety Report (TSR)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**TSR:** Core document in EN 50129 safety case providing technical evidence.

**Contents:**
- System architecture (block diagrams, interfaces)
- Failure modes analysis (FMEA, FTA)
- Safety mechanisms (redundancy, diagnostics)
- Software safety evidence (EN 50128 compliance)
- Hardware safety evidence (fault tolerance)
- Verification & validation results
- SIL demonstration (quantitative/qualitative)

**Purpose:**  
Demonstrate system meets SIL requirements.

Question 8: What is Independent Safety Assessment (ISA)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**ISA:**  
Independent review of safety-critical system by third-party assessor.

**Who:**  
Assessor not involved in development (e.g., TÜV, Lloyds Register, independent consultant)

**What:**  
Review all safety artifacts for EN 50128/50129 compliance

**Outcome:**  
Assessment report with findings, recommendations, approval/rejection

**Required for:**  
SIL 2/3/4 (Recommended for SIL 2, Highly Recommended for SIL 3/4)

Question 9: What is the difference between fail-safe and fail-operational?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

- **Fail-safe:** System enters safe state upon failure
  - Example: Interlocking → all signals RED, trains stop
  - Architecture: 2oo2D (both channels must agree)
  - Suitable for: Systems where stopping is safe

- **Fail-operational:** System continues safe operation despite failure
  - Example: ATP with 2oo3 voting continues with 2 good channels
  - Architecture: 2oo3, 3oo4 (majority voting)
  - Suitable for: Systems where stopping is dangerous (e.g., moving train)

Question 10: What is CENELEC?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**CENELEC = European Committee for Electrotechnical Standardization**

- Standards body for European electrical/electronic standards
- Publishes EN 50xxx series for railway applications
- Members: 34 European countries
- Standards adopted as national standards (e.g., BS EN 50128 in UK)

**Key Railway Standards:**
- EN 50126: RAMS (Reliability, Availability, Maintainability, Safety)
- EN 50128: Software
- EN 50129: Systems
- EN 50657: Assessment

════════════════════════════════════════════════════════════════════════════

📋 **COMPLIANCE CHECKLIST**
───────────────────────────

**EN 50128 Software Compliance (SIL 4):**

**Planning:**
- [ ] Software Development Plan (SDP) approved
- [ ] Software Quality Assurance Plan (SQAP) approved
- [ ] Software V&V Plan (SVVP) approved
- [ ] Independent Safety Assessor appointed

**Requirements:**
- [ ] Software Requirements Specification (SRS) complete
- [ ] Requirements traceable to system requirements & hazards
- [ ] Semi-formal or formal notation used
- [ ] Requirements reviewed & approved

**Design:**
- [ ] Software architecture documented
- [ ] Modular design with clear interfaces
- [ ] Safety mechanisms identified (redundancy, monitoring)
- [ ] Diverse programming considered (for SIL 4)
- [ ] Design reviewed & approved

**Implementation:**
- [ ] MISRA C:2012 coding standard followed
- [ ] No dynamic memory allocation
- [ ] No recursion
- [ ] Static analysis performed (zero defects)
- [ ] Code reviews completed

**Testing:**
- [ ] Unit tests executed (statement, branch, MC/DC coverage)
- [ ] Integration tests executed
- [ ] Software validation tests executed (all SRS requirements)
- [ ] Test coverage analyzed (MC/DC > 99% for SIL 4)
- [ ] Test results documented

**Assessment:**
- [ ] Independent Safety Assessment completed
- [ ] All non-conformances resolved
- [ ] Assessment report approved

**EN 50129 Safety Case:**

**System Safety:**
- [ ] Hazard analysis completed (HAZOP, FTA, FMEA)
- [ ] SIL assigned to all safety functions
- [ ] Safety requirements allocated to subsystems
- [ ] Residual risk evaluated & acceptable

**Technical Safety Report:**
- [ ] System architecture documented
- [ ] Failure modes analysis completed
- [ ] Safety mechanisms described & justified
- [ ] EN 50128 compliance demonstrated (software)
- [ ] Hardware fault tolerance demonstrated
- [ ] Verification & validation results included
- [ ] SIL quantitative/qualitative demonstration

**Safety Case:**
- [ ] Quality Management Report complete
- [ ] Safety Management Report complete
- [ ] Technical Safety Report complete
- [ ] Related safety cases referenced (generic products)
- [ ] Conclusion & recommendation for approval
- [ ] Independent assessment report included

**Approval:**
- [ ] Safety case submitted to Safety Authority
- [ ] Safety Authority approval received
- [ ] Certificate issued

════════════════════════════════════════════════════════════════════════════

📚 **FURTHER READING & REFERENCES**
───────────────────────────────────

**Primary Standards:**
- **EN 50128:2011+A1:2020:** Railway software lifecycle
- **EN 50129:2018:** Railway safety-related electronic systems
- **EN 50126-1:2017:** Railway RAMS (Reliability, Availability, Maintainability, Safety)
- **EN 50657:2017:** Railway safety assurance
- **IEC 61508:2010:** Generic functional safety (basis for EN 50xxx)

**European Regulations:**
- **EU Regulation 2016/919:** TSI (Technical Specification for Interoperability) for signalling
- **EU Regulation 2018/545:** ERTMS/ETCS requirements

**Books:**
- *Railway Signalling and Interlocking* by S. Patra
- *CENELEC 50128 and IEC 62279 Software* by I. Crick
- *Railway Safety Principles and Guidance* by UK RSSB

**Training:**
- **TÜV Rheinland:** EN 50128/50129 certification courses
- **Lloyds Register:** Railway safety training
- **IRSE (Institution of Railway Signal Engineers):** Professional development

**Tools:**
- **SCADE Suite:** Model-based development for EN 50128 (SIL 3/4)
- **LDRA Testbed:** Static/dynamic analysis, MC/DC coverage
- **Prover AB:** Formal verification for interlocking
- **IBM DOORS:** Requirements management & traceability

**Assessment Bodies:**
- **TÜV Rheinland, TÜV SÜD, TÜV Nord** (Germany)
- **Lloyd's Register** (UK)
- **CERTIFER** (France)
- **SQS** (Switzerland)

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 1.0 — Comprehensive EN 50128/50129 reference  
**Audience:** Railway signal engineers, software engineers, safety assessors, certification specialists
