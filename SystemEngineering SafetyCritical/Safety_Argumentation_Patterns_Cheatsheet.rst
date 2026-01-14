📋 **Safety Argumentation Patterns**
═══════════════════════════════════════════════════════════════════

**Full Name:** Reusable Safety Argument Templates  
**Type:** Design patterns for safety cases  
**Purpose:** Proven argument structures for common safety scenarios  
**Standards:** GSN Community Standard, ISO/IEC 15026-2

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — SAFETY ARGUMENTATION PATTERNS IN 60 SECONDS**
──────────────────────────────────────────────────────────

**What are Safety Argumentation Patterns?**

::

    Safety Patterns = Reusable templates for common safety arguments
    
    Like design patterns in software engineering, but for safety cases:
    - Proven argument structures
    - Instantiated for specific system
    - Reduce effort, increase quality

**Common Patterns (9 types):**

1. **Hazard Avoidance Pattern**: Eliminate hazard at source
2. **Risk Reduction Pattern**: Reduce likelihood or severity
3. **Fault Tolerance Pattern**: Continue operation despite faults
4. **Diverse Redundancy Pattern**: Multiple independent implementations
5. **Independence Pattern**: No common cause failures
6. **Proven-in-Use Pattern**: Operational experience demonstrates safety
7. **Confidence Pattern**: Quantify assurance in evidence
8. **Compliance Pattern**: Map to standard objectives
9. **ALARP Pattern**: Residual risk as low as reasonably practicable

**Why Use Patterns?**

✅ **Efficiency**: Don't reinvent argument structure  
✅ **Quality**: Proven patterns less likely to have gaps  
✅ **Communication**: Common vocabulary (pattern names)  
✅ **Review**: Assessor recognizes standard pattern  
✅ **Reuse**: Same pattern across multiple systems

**Pattern Structure:**

.. code-block:: text

    PATTERN NAME: <Descriptive name>
    INTENT:       <What problem does it solve?>
    STRUCTURE:    <GSN template>
    EVIDENCE:     <What evidence types needed?>
    EXAMPLE:      <Concrete instantiation>
    VARIANTS:     <Common modifications>
    PITFALLS:     <Common mistakes>

════════════════════════════════════════════════════════════════════

📖 **1. HAZARD AVOIDANCE PATTERN**
══════════════════════════════════

**1.1 Intent**
--------------

**Argue that a hazard cannot occur because the hazardous condition
is prevented by design.**

**When to use:**

- Inherently safe design preferred over mitigation
- Hazard can be eliminated at source
- Example: No explosive fuel → no fire hazard

**1.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Hazard H cannot occur               │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  by hazard   ╱
              ╱   avoidance   ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │
    │Hazardous│   │Design   │  │Design   │
    │condition│   │prevents │  │verified │
    │defined  │   │condition│  │correct  │
    └────┬────┘   └────┬────┘  └────┬────┘
         │             │            │
         ○             ○            ○
        ╱ ╲           ╱ ╲          ╱ ╲
       ──────        ──────       ──────
       │             │            │
    Sn1:          Sn2:         Sn3:
    Hazard        Design       Design
    analysis      specs        review

**1.3 Evidence Required**
-------------------------

- Hazard analysis (defining hazardous condition)
- Design specifications (showing prevention)
- Design review/verification (confirming implementation)
- Test results (demonstrating effectiveness)

**1.4 Example: Railway Electrocution**
--------------------------------------

**Hazard H-1:** Electrocution of maintenance worker

**Avoidance Argument:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Maintenance worker cannot be        │
    │     electrocuted during track work      │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Hazard  ╲
               ╱  avoidance by╱
              ╱   de-energize ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │
    │Hazard = │   │Track de-│  │De-energ │
    │Contact  │   │energized│  │verified │
    │with live│   │before   │  │before   │
    │rail     │   │access   │  │access   │
    └────┬────┘   └────┬────┘  └────┬────┘
         │             │            │
         ○             ○       ◇────┴────◇
        ╱ ╲           ╱ ╲     ╱ S1.3:    ╲
       ──────        ────── ╱  Arg by    ╱
       │             │     ╱   interlocks╱
    Sn1:          Sn2:   ◇──────────────◇
    HAZOP         Proc-        │
    (H-1)         edure   ┌────┼────┐
                  SOP-01  │    │    │
                       ┌──┴┐ ┌─┴─┐ ┌┴──┐
                       │G  │ │G  │ │G  │
                       │1.3│ │1.3│ │1.3│
                       │.1 │ │.2:│ │.3:│
                       └─┬─┘ └─┬─┘ └┬──┘
                         ○     ○    ○
                        ╱╲    ╱╲   ╱╲
                       ──── ──── ────
                       │    │    │
                    Sn3: Sn4: Sn5:
                    Lock Volt Test
                    key  meter cert

**Evidence:**

- Sn1: HAZOP identifying hazardous condition (live rail contact)
- Sn2: Procedure SOP-01 requiring de-energization before access
- Sn3: Lock-out/tag-out (LOTO) system preventing re-energization
- Sn4: Voltage meter test (confirm 0V) before worker access
- Sn5: Test certificates (1000 tests, 100% effective)

**Result:** Hazard eliminated (no live electricity → no electrocution)

════════════════════════════════════════════════════════════════════

📖 **2. RISK REDUCTION PATTERN**
════════════════════════════════

**2.1 Intent**
--------------

**Argue that hazard risk is acceptable by reducing likelihood
and/or severity to tolerable levels.**

**When to use:**

- Hazard cannot be eliminated (avoidance not feasible)
- Risk = Likelihood × Severity can be quantified
- Target risk level defined (e.g., SIL 4: <10⁻⁹/hr)

**2.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Hazard H has acceptable risk        │
    └──────────────────┬────────────────────┬─┘
                       │                    │
              ┌────────┴────────┐      Context: □──────────┐
              │ C1: Acceptable  │      │ Target risk       │
              │ risk = 10⁻⁸/hr  │      │ <10⁻⁸/hr (ASIL D) │
              └─────────────────┘      └───────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  by risk     ╱
              ╱   = L × S     ╱
             ◇───────────────◇
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴────────┐         ┌────────┴────┐
    │ G1.1:       │         │ G1.2:       │
    │ Likelihood  │         │ Severity    │
    │ is low      │         │ is low      │
    │ (<10⁻⁶/hr)  │         │ (≤Minor)    │
    └────┬────────┘         └────┬────────┘
         │                       │
    [Evidence]               [Evidence]

**2.3 Evidence Required**
-------------------------

**Likelihood Reduction:**

- Fault tree analysis (probability calculation)
- Reliability data (MTBF, failure rates)
- Redundancy architecture (N-modular redundancy)
- Diagnostic coverage (fault detection effectiveness)

**Severity Reduction:**

- Consequence analysis (what happens if hazard occurs)
- Protective barriers (containment, isolation)
- Emergency response (time to mitigate)

**2.4 Example: Autonomous Vehicle Collision**
---------------------------------------------

**Hazard H-1:** Collision with pedestrian

**Risk Reduction Argument:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Risk of pedestrian collision is     │
    │     acceptable (<10⁻⁸ events/mile)      │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Risk    ╲
               ╱  reduction   ╱
              ╱   L × S       ╱
             ◇───────────────◇
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴──────────┐       ┌────────┴──────┐
    │ G1.1:         │       │ G1.2:         │
    │ Likelihood    │       │ Severity      │
    │ reduced by    │       │ reduced by    │
    │ redundancy    │       │ speed limit   │
    └────┬──────────┘       └────┬──────────┘
         │                       │
    ◇────┴────◇             ◇────┴────◇
   ╱ S1.1:    ╲           ╱ S1.2:    ╲
  ╱ 3-sensor  ╱          ╱ Geofence  ╱
 ╱  fusion    ╱          ╱  + speed  ╱
◇────────────◇          ◇  limiter  ◇
         │                       │
    ┌────┼────┐             ┌────┼────┐
    │    │    │             │    │    │
  [Cameras] [LIDAR]      [Zone]  [Max]
    │    [RADAR]           [def]  [25mph]
    ○     ○    ○            ○      ○
   ╱╲    ╱╲   ╱╲          ╱╲     ╱╲
  ──── ──── ────         ──── ────
  │    │    │            │    │
Sn1: Sn2: Sn3:        Sn4: Sn5:
FTA  FTA  FTA         Map  Test
Cam  LID  RAD         data cert
P=   P=   P=          (ped (25mph
10⁻⁴ 10⁻⁴ 10⁻⁴        zones) max)

**Risk Calculation:**

- **Baseline likelihood** (no redundancy): 10⁻⁴/mile
- **With 3-sensor fusion** (2oo3 voting): 10⁻⁴ × 10⁻⁴ = 10⁻⁸/mile ✅
- **Severity**: Speed limited to 25 mph in pedestrian zones → Minor injury (not fatal)
- **Result**: Risk = 10⁻⁸/mile × Minor severity = Acceptable ✅

════════════════════════════════════════════════════════════════════

📖 **3. FAULT TOLERANCE PATTERN**
═════════════════════════════════

**3.1 Intent**
--------------

**Argue that system continues to provide essential functionality
despite component failures.**

**When to use:**

- Fail-operational requirement (no safe state exists)
- Example: Aircraft flight control, medical life support
- Continuous operation despite faults

**3.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: System is fault-tolerant for        │
    │     failure mode F                      │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  by redundant╱
              ╱   channels    ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │  │ G1.4:   │
    │Channel  │   │Channel  │  │Channels │  │Reconfig │
    │A        │   │B        │  │indepen- │  │effective│
    │reliable │   │reliable │  │dent     │  │         │
    └────┬────┘   └────┬────┘  └────┬────┘  └────┬────┘
         │             │            │            │
        [Evidence]   [Evidence]  [Evidence]   [Evidence]

**3.3 Evidence Required**
-------------------------

- Reliability analysis for each channel (FMEA, FTA)
- Independence analysis (no common cause failures)
- Reconfiguration logic verification (switching algorithm)
- Testing (fault injection, failure scenarios)

**3.4 Example: Aircraft Fly-by-Wire**
-------------------------------------

**Function:** Aileron control (roll)

**Fault Tolerance Argument:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Aileron control remains available   │
    │     despite single channel failure      │
    └──────────────────┬──────────────────────┘
                       │
              Context: □─────────────┐
                       │ Requirement:│
                       │ Fail-op     │
                       │ (DAL A)     │
                       └─────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Triplex ╲
               ╱  redundancy  ╱
              ╱   (TMR)       ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │  │ G1.4:   │
    │Lane A   │   │Lane B   │  │Lane C   │  │Voter    │
    │MTBF     │   │MTBF     │  │MTBF     │  │correct  │
    │>10⁵ hr  │   │>10⁵ hr  │  │>10⁵ hr  │  │         │
    └────┬────┘   └────┬────┘  └────┬────┘  └────┬────┘
         │             │            │            │
         ○             ○            ○       ◇────┴────◇
        ╱ ╲           ╱ ╲          ╱ ╲     ╱ S1.4:    ╲
       ──────        ──────       ────── ╱  Majority  ╱
       │             │            │     ╱   voting    ╱
    Sn1:          Sn2:         Sn3:   ◇──────────────◇
    FMEA          FMEA         FMEA         │
    Lane A        Lane B       Lane C  ┌────┼────┐
    (MTBF=        (MTBF=       (MTBF=  │    │    │
    2×10⁵hr)      2×10⁵hr)     2×10⁵hr)│   ┌┴┐  ┌┴┐
                                       │   │G│  │G│
                                       │   │1│  │1│
                                       │   │.4│  │.4│
                                       │   │.1│  │.2│
                                       │   └┬┘  └┬┘
                                       │    ○    ○
                                       │   ╱╲   ╱╲
                                       │  ──── ────
                                       │  │    │
                                    Sn4:Sn5: Sn6:
                                    Voter Fault Test
                                    logic inject cert
                                    formal(1000 (100%
                                    proof tests)detect)

**Fault Tolerance Proof:**

- **Single failure**: 2 of 3 channels remain → Voter outputs correct value ✅
- **Probability of loss**: P(2 failures simultaneously) = (10⁻⁵)² = 10⁻¹⁰/hr ✅
- **Meets DAL A requirement**: <10⁻⁹/hr catastrophic failure

════════════════════════════════════════════════════════════════════

📖 **4. DIVERSE REDUNDANCY PATTERN**
════════════════════════════════════

**4.1 Intent**
--------------

**Argue that redundant channels are truly independent by using
diverse implementations (different technology, algorithms, teams).**

**When to use:**

- Common cause failures are a concern (same bug in all channels)
- Software-intensive systems (deterministic failures)
- Highest safety levels (SIL 4, DAL A)

**4.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Redundant channels are independent  │
    │     (no common cause failures)          │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  by diversity╱
              ◇───────────────◇
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │  │ G1.4:   │
    │Tech     │   │Algorithm│  │Team     │  │CCF      │
    │diverse  │   │diverse  │  │diverse  │  │analysis │
    └────┬────┘   └────┬────┘  └────┬────┘  └────┬────┘
         │             │            │            │
        [Evidence]   [Evidence]  [Evidence]   [Evidence]

**4.3 Types of Diversity**
--------------------------

+-------------------+-------------------------+-------------------------+
| **Type**          | **Example**             | **Benefit**             |
+===================+=========================+=========================+
| **Technology**    | Analog + Digital        | Different failure modes |
+-------------------+-------------------------+-------------------------+
| **Algorithm**     | Kalman filter + Median  | Different blind spots   |
+-------------------+-------------------------+-------------------------+
| **Language**      | C + Ada                 | Different compiler bugs |
+-------------------+-------------------------+-------------------------+
| **Development**   | Team A + Team B         | Different human errors  |
| **Team**          |                         |                         |
+-------------------+-------------------------+-------------------------+
| **Tools**         | Compiler X + Compiler Y | Different tool bugs     |
+-------------------+-------------------------+-------------------------+
| **Platform**      | Processor A + Proc B    | Different HW faults     |
+-------------------+-------------------------+-------------------------+

**4.4 Example: Nuclear Reactor Protection System**
--------------------------------------------------

**Function:** Emergency shutdown (SCRAM)

**Diversity Argument:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Reactor protection system has no    │
    │     common cause failure (CCF) for      │
    │     failure to SCRAM                    │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Diverse ╲
               ╱  primary +   ╱
              ╱   secondary   ╱
             ◇───────────────◇
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴──────────┐       ┌────────┴──────┐
    │ G1.1:         │       │ G1.2:         │
    │ Primary sys   │       │ Secondary sys │
    │ diverse from  │       │ diverse from  │
    │ secondary     │       │ primary       │
    └────┬──────────┘       └────┬──────────┘
         │                       │
    ◇────┴────◇             ◇────┴────◇
   ╱ S1.1:    ╲           ╱ S1.2:    ╲
  ╱ Diversity ╱          ╱ Independent╱
 ╱  in 6      ╱          ╱  verification╱
◇  dimensions ◇          ◇──────────────◇
         │                       │
    ┌────┼────┬────┬────┬────┐  ○
    │    │    │    │    │    │ ╱ ╲
  ┌─┴┐ ┌─┴┐ ┌─┴┐ ┌─┴┐ ┌─┴┐ ┌┴┐──────
  │G │ │G │ │G │ │G │ │G │ │G│ │
  │1.│ │1.│ │1.│ │1.│ │1.│ │1│Sn2:
  │1.│ │1.│ │1.│ │1.│ │1.│ │.│CCF
  │1 │ │2 │ │3 │ │4 │ │5 │ │6│analy
  └┬─┘ └┬─┘ └┬─┘ └┬─┘ └┬─┘ └─┘(Beta
   ○   ○   ○   ○   ○         =10⁻⁴)
  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲
 ──── ──── ──── ──── ────
 │    │    │    │    │
Sn1: Sn3: Sn5: Sn7: Sn9:
Tech Algo Team Lang Platf
(Ana (Thres(A:  (C   (Proc
log  hold  vendor vs   A vs
vs   vs    vs    Ada) B)
Digit median B:   
al)  filter)in-hse)

**Diversity Details:**

- **Primary**: Analog electronics, threshold comparators, Team A (vendor), C, Processor A
- **Secondary**: Digital microprocessor, median filter algorithm, Team B (in-house), Ada, Processor B
- **CCF analysis**: Beta factor = 10⁻⁴ (residual CCF probability) → Acceptable for SIL 4

════════════════════════════════════════════════════════════════════

📖 **5. PROVEN-IN-USE PATTERN**
═══════════════════════════════

**5.1 Intent**
--------------

**Argue that component/system is safe based on successful
operational history in similar applications.**

**When to use:**

- COTS (Commercial Off-The-Shelf) components
- Legacy systems with long operational history
- When full development evidence is unavailable

**5.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Component C is safe for use in      │
    │     application A                       │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Proven  ╲
               ╱  in use      ╱
              ╱   argument    ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │  │ G1.4:   │
    │Similar  │   │Operating│  │No safety│  │Lessons  │
    │applic'n │   │history  │  │incidents│  │learned  │
    │         │   │extensive│  │         │  │applied  │
    └────┬────┘   └────┬────┘  └────┬────┘  └────┬────┘
         │             │            │            │
        [Evidence]   [Evidence]  [Evidence]   [Evidence]

**5.3 Evidence Required**
-------------------------

- Similarity analysis (new application vs historical use)
- Operating history (flight hours, operational years)
- Incident reports (no safety-related failures)
- Configuration management (same version/configuration)
- Lessons learned (improvements incorporated)

**5.4 Example: COTS Processor in Medical Device**
-------------------------------------------------

**Component:** Intel Core i7 processor  
**Application:** Surgical robot control system  
**Safety level:** IEC 62304 Class C (safety-critical)

**Proven-in-Use Argument:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Intel Core i7 is safe for use in    │
    │     surgical robot control (Class C)    │
    └──────────────────┬──────────────────────┘
                       │
              Context: □─────────────┐
                       │ IEC 62304   │
                       │ Class C     │
                       │ (surgical)  │
                       └─────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Proven  ╲
               ╱  in use in   ╱
              ╱   similar     ╱
             ◇   applications◇
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │  │ G1.4:   │
    │Similar  │   │Fleet    │  │Safety   │  │Errata   │
    │safety-  │   │history: │  │record:  │  │reviewed │
    │critical │   │10M units│  │No known │  │& mitig  │
    │use      │   │5 years  │  │critical │  │         │
    └────┬────┘   └────┬────┘  │ bugs    │  └────┬────┘
         │             │        └────┬────┘       │
         ○             ○             ○            ○
        ╱ ╲           ╱ ╲           ╱ ╲          ╱ ╲
       ──────        ──────        ──────       ──────
       │             │             │            │
    Sn1:          Sn2:          Sn3:         Sn4:
    Similarity    Fleet data    Intel        Errata
    analysis:     (10M units    bug          review:
    - Aerospace   × 5 yr        database     23 errata
      avionics    × 8760hr/yr   (0 safety    identified
    - Industrial  = 438B        -related     All
      control     device-hrs)   defects)     mitigated
    - Medical                                (WDT,
      imaging                                 ECC RAM)

**Conclusion:** Proven-in-use evidence sufficient (no full DO-254 needed)

════════════════════════════════════════════════════════════════════

📖 **6. CONFIDENCE PATTERN**
════════════════════════════

**6.1 Intent**
--------------

**Argue not just THAT the claim is true, but HOW CONFIDENT we are
in the evidence supporting the claim.**

**When to use:**

- High safety integrity levels (SIL 4, DAL A)
- Evidence quality is variable (some strong, some weak)
- Independent assessment requires confidence justification

**6.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Claim is true with high confidence  │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  with        ╱
              ╱   confidence  ╱
             ◇───────────────◇
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴────────┐         ┌────────┴────────┐
    │ G1.1:       │         │ C1 (Confidence):│
    │ Claim       │         │ Evidence is:    │
    │ substantia- │         │ - Relevant      │
    │ ted         │         │ - Sufficient    │
    └────┬────────┘         │ - Current       │
         │                  │ - Trustworthy   │
         ○                  └─────────────────┘
        ╱ ╲
       ──────
       │
    Sn1: Evidence
    
    Confidence sub-argument explains WHY evidence is trustworthy

**6.3 Confidence Criteria (4 dimensions)**
------------------------------------------

+-------------------+-------------------------+-------------------------+
| **Criterion**     | **Question**            | **Example**             |
+===================+=========================+=========================+
| **Relevant**      | Does evidence actually  | FTA for probability,    |
|                   | support the claim?      | not just description    |
+-------------------+-------------------------+-------------------------+
| **Sufficient**    | Is there enough         | MC/DC 100% not 60%      |
|                   | evidence?               |                         |
+-------------------+-------------------------+-------------------------+
| **Current**       | Is evidence up-to-date? | Test results for v2.3,  |
|                   |                         | not v1.0                |
+-------------------+-------------------------+-------------------------+
| **Trustworthy**   | Is source credible?     | Independent test lab,   |
|                   |                         | not developer self-test |
+-------------------+-------------------------+-------------------------+

**6.4 Example: Software Correctness Claim**
-------------------------------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Flight control software is correct  │
    │     (free from critical defects)        │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: V&V     ╲
               ╱  with high   ╱
              ╱   confidence  ╱
             ◇───────────────◇
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴────────┐         ┌────────┴────────┐
    │ G1.1:       │         │ G1.2 (Confidence│
    │ Software    │         │ Argument):      │
    │ tested      │         │ Testing is:     │
    └────┬────────┘         └────┬────────────┘
         │                       │
         ○                  ◇────┴────◇
        ╱ ╲                ╱ S1.2:    ╲
       ──────             ╱ Confidence╱
       │                 ╱  by 4      ╱
    Sn1: Test           ◇  criteria   ◇
    results                    │
    (10K tests,    ┌───────────┼───────────┬───────────┐
    0 failures)    │           │           │           │
              ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
              │ G1.2.1: │ │ G1.2.2: │ │ G1.2.3: │ │ G1.2.4: │
              │Relevant │ │Suffic't │ │ Current │ │ Trust   │
              └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
                   │           │           │           │
                   ○           ○           ○           ○
                  ╱ ╲         ╱ ╲         ╱ ╲         ╱ ╲
                 ──────      ──────      ──────      ──────
                 │           │           │           │
              Sn2:        Sn3:        Sn4:        Sn5:
              Test        Coverage:   Version     Independent
              scenarios   MC/DC 100%  control:    test lab
              map to      (not just   Tests for   (TÜV SÜD)
              hazards     stmt cov)   v2.3        DO-330
              (H-1 to               (current)    qualified
              H-15)

**Confidence Conclusion:**

- Relevant: Tests cover all hazards ✅
- Sufficient: MC/DC 100% (rigorous) ✅
- Current: Tests for deployed version ✅
- Trustworthy: Independent lab, qualified tools ✅
→ **High confidence** in software correctness claim

════════════════════════════════════════════════════════════════════

📖 **7. COMPLIANCE PATTERN**
════════════════════════════

**7.1 Intent**
--------------

**Argue safety by demonstrating compliance with all objectives
of a recognized safety standard.**

**When to use:**

- Standard is prescriptive (DO-178C, IEC 61508)
- Regulator requires compliance demonstration
- Standard provides comprehensive safety objectives

**7.2 Structure (GSN)**
-----------------------

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: System complies with Standard X     │
    └──────────────────┬──────────────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: Argument╲
               ╱  by compliance╱
              ╱   with all     ╱
             ◇   objectives    ◇
                       │
         ┌─────────────┼─────────────┬──────...──┐
         │             │             │           │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐ ┌────┴────┐
    │ G1.1:   │   │ G1.2:   │  │ G1.3:   │ │ G1.n:   │
    │Objective│   │Objective│  │Objective│ │Objective│
    │1        │   │2        │  │3        │ │n        │
    │satisfied│   │satisfied│  │satisfied│ │satisfied│
    └────┬────┘   └────┬────┘  └─────────┘ └────┬────┘
         │             │                         │
        [Evidence]   [Evidence]                [Evidence]

**7.3 Example: DO-178C DAL A Compliance**
-----------------------------------------

(Simplified - actual DO-178C has 71 objectives for DAL A)

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ G1: Flight control software complies    │
    │     with DO-178C DAL A                  │
    └──────────────────┬──────────────────────┘
                       │
              Context: □─────────────┐
                       │ DO-178C     │
                       │ DAL A       │
                       │ (71 obj)    │
                       └─────────────┘
                       │
                 ◇─────┴─────◇
                ╱ S1: All 71  ╲
               ╱  objectives  ╱
              ╱   satisfied   ╱
             ◇───────────────◇
                       │
         ┌─────────────┼─────────────┬──────...──┐
         │             │             │           │
    ┌────┴────┐   ┌────┴────┐  ┌────┴────┐ ┌────┴────┐
    │ G1.1:   │   │ G1.10:  │  │ G1.50:  │ │ G1.71:  │
    │A-1 SRD  │   │A-4.4.1  │  │A-7.2.4  │ │A-9.9 SQA│
    │complete │   │HLR      │  │MC/DC    │ │records  │
    │         │   │testable │  │coverage │ │         │
    └────┬────┘   └────┬────┘  └────┬────┘ └────┬────┘
         │             │            │            │
         ○             ○            ○            ○
        ╱ ╲           ╱ ╲          ╱ ╲          ╱ ╲
       ──────        ──────       ──────       ──────
       │             │            │            │
    Sn1:          Sn10:        Sn50:        Sn71:
    SRD           Test         Coverage     SQA
    Doc-001       Report       Report       Plan
    (review       (1000        (100%        (audited
    complete      tests,       MC/DC        annually
    signatures)   0 fail)      verified)    by DER)

**Compliance Matrix:**

+-------------+------------------+----------------+-------------+
| **Obj ID**  | **Objective**    | **Evidence**   | **Status**  |
+=============+==================+================+=============+
| A-1         | SRD complete     | Doc-001        | ✅ Satisfied|
+-------------+------------------+----------------+-------------+
| A-4.4.1     | HLR testable     | Test Plan      | ✅ Satisfied|
+-------------+------------------+----------------+-------------+
| A-7.2.4     | MC/DC coverage   | Cov Report     | ✅ Satisfied|
+-------------+------------------+----------------+-------------+
| ...         | ...              | ...            | ...         |
+-------------+------------------+----------------+-------------+
| A-9.9       | SQA records      | SQA Plan       | ✅ Satisfied|
+-------------+------------------+----------------+-------------+

════════════════════════════════════════════════════════════════════

📝 **8. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between the Hazard Avoidance pattern
and the Risk Reduction pattern?

**A1:**

- **Hazard Avoidance**: Eliminate hazard at source (hazard cannot occur)
  - Example: De-energize electrical system → No electrocution possible
  - Preferred when feasible (inherently safe design)

- **Risk Reduction**: Reduce likelihood or severity to acceptable level
  - Example: Triple redundancy → Likelihood reduced to 10⁻¹⁰/hr
  - Used when hazard cannot be eliminated

────────────────────────────────────────────────────────────────────

**Q2:** When should the Proven-in-Use pattern be applied?

**A2:**

**When:**
- COTS components without full development evidence
- Legacy systems with extensive operational history
- Similar application (safety level, operating environment)

**Requirements:**
- Extensive operating history (e.g., 10M device-hours)
- No safety-related incidents
- Configuration management (same version)
- Similarity analysis (new use ≈ historical use)

**NOT applicable:** Novel application, unproven technology

────────────────────────────────────────────────────────────────────

**Q3:** What are the 4 confidence criteria for evaluating evidence?

**A3:**

1. **Relevant**: Evidence actually supports the claim
2. **Sufficient**: Enough evidence (quantitative: 100% MC/DC not 60%)
3. **Current**: Evidence is up-to-date (correct version)
4. **Trustworthy**: Source is credible (independent, qualified)

All 4 must be satisfied for high-confidence argument.

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Pattern Understanding:**
- [ ] Know 9 common safety argumentation patterns
- [ ] Understand when to apply each pattern (intent)
- [ ] Recognize patterns in existing safety cases

**Pattern Application:**
- [ ] Select appropriate pattern for your system
- [ ] Instantiate pattern (fill in specific goals, evidence)
- [ ] Combine patterns (e.g., Risk Reduction + Fault Tolerance)
- [ ] Document rationale for pattern selection

**Evidence Collection:**
- [ ] Identify required evidence types for chosen pattern
- [ ] Collect evidence (analysis, test, review, operational)
- [ ] Evaluate evidence quality (4 confidence criteria)
- [ ] Address evidence gaps (collect missing evidence or justify TBS)

**Best Practices:**
- [ ] Use standard pattern names (common vocabulary)
- [ ] Document deviations from standard pattern (if any)
- [ ] Review patterns with independent assessor
- [ ] Reuse patterns across projects (efficiency)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Safety patterns = reusable argument templates** → Don't reinvent

2️⃣ **9 common patterns** → Hazard avoidance, risk reduction, fault tolerance, diversity, proven-in-use, confidence, compliance, independence, ALARP

3️⃣ **Pattern structure** → Intent, GSN template, evidence, example, variants, pitfalls

4️⃣ **Hazard avoidance preferred** → Eliminate hazard at source (inherently safe)

5️⃣ **Diversity for CCF** → Multiple implementations reduce common cause failures

6️⃣ **Confidence argument** → Not just WHAT but HOW CONFIDENT (4 criteria)

7️⃣ **Combine patterns** → Real systems use multiple patterns together

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **SAFETY ARGUMENTATION PATTERNS CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** 9 reusable safety argument patterns (hazard avoidance, risk reduction,  
fault tolerance, diverse redundancy, proven-in-use, confidence, compliance, independence,  
ALARP), GSN templates, evidence requirements, detailed examples (railway electrocution,  
autonomous vehicle collision, aircraft fly-by-wire, nuclear reactor protection,  
COTS processor, software correctness, DO-178C compliance)

════════════════════════════════════════════════════════════════════
