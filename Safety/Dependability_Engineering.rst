🏆 **Dependability Engineering — Building Trustworthy Systems**
════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for Dependability, RAMS, and System Trustworthiness**  
**Attributes:** Reliability + Availability + Maintainability + Safety + Security  
**Domains:** Automotive 🚗 | Avionics ✈️ | Railway 🚆 | Industrial 🏭 | Medical 🏥  
**Purpose:** System design, assessment, certification, operational excellence

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What is Dependability?**

*"Ability to deliver service that can justifiably be trusted"* — Avizienis et al., 2004

**Dependability Attributes (RAMS-S):**

.. code-block:: text

   R  Reliability      → Continuity of correct service
   A  Availability     → Readiness for correct service
   M  Maintainability  → Ease of maintenance/repair
   S  Safety           → Absence of catastrophic consequences
   S  Security         → Protection against adversaries

**Attribute Relationships:**

.. code-block:: text

                    Dependability
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    Reliability    Availability    Maintainability
         │               │               │
         └───────────────┼───────────────┘
                         │
                    ┌────┴────┐
                  Safety  Security

**Key Metrics Quick Reference:**

+----------------+----------------------+------------------+
| Attribute      | Primary Metric       | Target (Example) |
+================+======================+==================+
| Reliability    | MTBF, Failure Rate   | >10⁵ hours       |
+----------------+----------------------+------------------+
| Availability   | Uptime %             | 99.99% (4-nines) |
+----------------+----------------------+------------------+
| Maintainability| MTTR                 | <30 minutes      |
+----------------+----------------------+------------------+
| Safety         | PFH, SIL             | 10⁻⁸ /hr (SIL 3) |
+----------------+----------------------+------------------+
| Security       | CVSS, Breach Time    | CVSS < 7.0       |
+----------------+----------------------+------------------+

**Dependability Means (How to Achieve):**

✅ **Fault Prevention** → Prevent faults from occurring (design, QA)  
✅ **Fault Tolerance** → Mask faults that occur (redundancy)  
✅ **Fault Removal** → Detect and remove faults (testing, verification)  
✅ **Fault Forecasting** → Predict faults before they occur (reliability modeling)

════════════════════════════════════════════════════════════════════════════

📖 **1. DEPENDABILITY FUNDAMENTALS**
════════════════════════════════════════════════════════════════════════════

1.1 Dependability Taxonomy
---------------------------

**Faults → Errors → Failures (Chain of Events):**

.. code-block:: text

   FAULT (cause) → ERROR (internal state) → FAILURE (service deviation)
   
   Example (Railway Signal):
   - FAULT: Relay contact wears out (physical defect)
   - ERROR: Relay fails to energize (incorrect state)
   - FAILURE: Signal stays RED when should be GREEN (service failure)

**Fault Classification:**

**By Origin:**
- **Development faults**: Design bugs, specification errors
- **Physical faults**: Component aging, radiation, EMI
- **Interaction faults**: Software incompatibility, protocol violations

**By Intention:**
- **Malicious**: Sabotage, cyber attacks, insider threats
- **Non-malicious**: Accidental bugs, manufacturing defects

**By Persistence:**
- **Transient**: Temporary (cosmic ray bit flip)
- **Intermittent**: Recurring (loose connection)
- **Permanent**: Constant (burned-out component)

────────────────────────────────────────────────────────────────────────────

**1.2 Dependability Attributes Defined**
----------------------------------------

**Reliability (R):**

*Definition:* Probability of failure-free operation for a specified period

.. code-block:: text

   R(t) = e^(-λt)
   
   Where:
   - λ = Constant failure rate (failures/hour)
   - t = Time (hours)
   
   Example: λ = 10⁻⁵ /hr, t = 10,000 hr
   R(10,000) = e^(-10⁻⁵ × 10,000) = e^(-0.1) = 0.905 (90.5%)

*Engineering Question:* "Will the system work without failure for T hours?"

────────────────────────────────────────────────────────────────────────────

**Availability (A):**

*Definition:* Proportion of time system is operational (uptime ratio)

.. code-block:: text

   A = MTTF / (MTTF + MTTR)
     = Uptime / (Uptime + Downtime)
   
   Example: MTTF = 10,000 hr, MTTR = 2 hr
   A = 10,000 / (10,000 + 2) = 0.9998 (99.98%)

*Engineering Question:* "Is the system ready when I need it?"

**Availability Levels:**

+--------+------------+-----------------+----------------------+
| Level  | Percentage | Downtime/Year   | Application          |
+========+============+=================+======================+
| 2-nine | 99%        | 3.65 days       | Non-critical systems |
+--------+------------+-----------------+----------------------+
| 3-nine | 99.9%      | 8.76 hours      | Business systems     |
+--------+------------+-----------------+----------------------+
| 4-nine | 99.99%     | 52.6 minutes    | Telecom, industrial  |
+--------+------------+-----------------+----------------------+
| 5-nine | 99.999%    | 5.26 minutes    | Carrier-grade        |
+--------+------------+-----------------+----------------------+
| 6-nine | 99.9999%   | 31.5 seconds    | Mission-critical     |
+--------+------------+-----------------+----------------------+

────────────────────────────────────────────────────────────────────────────

**Maintainability (M):**

*Definition:* Ease of performing maintenance (repair, upgrade, inspection)

.. code-block:: text

   M(t) = 1 - e^(-μt)
   
   Where:
   - μ = Repair rate (1/MTTR)
   - t = Time to repair
   
   Example: MTTR = 30 minutes = 0.5 hr, μ = 2 /hr
   M(0.5) = 1 - e^(-2×0.5) = 1 - e^(-1) = 0.632
   → 63.2% chance repair completes within 30 min

*Engineering Question:* "How quickly can we restore service after failure?"

**Maintainability Categories:**
- **Corrective**: Fault diagnosis and repair
- **Preventive**: Scheduled inspections and replacements
- **Adaptive**: System upgrades and modifications
- **Perfective**: Performance improvements

────────────────────────────────────────────────────────────────────────────

**Safety (S):**

*Definition:* Absence of catastrophic consequences to people, property, environment

.. code-block:: text

   Safety ≠ Reliability
   
   Example (Railway Signal):
   - HIGH RELIABILITY: Signal works continuously for years
   - LOW SAFETY: When signal fails, fails to GREEN (dangerous)
   
   → Need FAIL-SAFE design (fails to RED)

*Engineering Question:* "What happens when the system fails?"

**Safety Metrics:**
- **PFH**: Probability of dangerous Failure per Hour
- **SIL**: Safety Integrity Level (IEC 61508: SIL 1-4)
- **ASIL**: Automotive SIL (ISO 26262: QM, A, B, C, D)
- **DAL**: Design Assurance Level (DO-178C: E, D, C, B, A)

────────────────────────────────────────────────────────────────────────────

**Security:**

*Definition:* Protection against intentional harm (confidentiality, integrity, availability)

.. code-block:: text

   CIA Triad:
   - Confidentiality: No unauthorized disclosure
   - Integrity: No unauthorized modification
   - Availability: Service accessible when needed

*Engineering Question:* "Can the system resist attacks?"

**Security vs Safety:**
- **Safety**: Accidental harm (random failures, design bugs)
- **Security**: Intentional harm (cyber attacks, sabotage)
- **Overlap**: Security breach can cause safety hazard

*Example:* Hacked medical infusion pump → deliver lethal drug dose

════════════════════════════════════════════════════════════════════════════

📖 **2. DEPENDABILITY MEANS (How to Achieve)**
════════════════════════════════════════════════════════════════════════════

2.1 Fault Prevention
--------------------

**Goal:** Stop faults from being introduced during development/manufacturing

**Techniques:**

**Design Phase:**
- Formal methods (mathematical proof of correctness)
- Design reviews (peer inspection, FMEA)
- Adherence to coding standards (MISRA C, CERT C)
- Component selection (automotive-grade, space-qualified parts)

**Implementation Phase:**
- Static analysis (Coverity, Polyspace)
- Code reviews (manual inspection, pair programming)
- Unit testing (branch coverage >90%)
- Continuous integration (automated build+test)

**Manufacturing Phase:**
- Process controls (SPC - Statistical Process Control)
- Incoming inspection (component verification)
- Environmental stress screening (burn-in, temperature cycling)
- Configuration management (version control, traceability)

**Example: MISRA C (Fault Prevention for Automotive)**

.. code-block:: c

   // ❌ VIOLATION: Rule 14.3 (unreachable code)
   int status = 1;
   if (status == 0) {
       // Dead code - never executed
       reset_system();
   }
   
   // ✅ COMPLIANT: Remove unreachable code
   int status = get_sensor_status();
   if (status == 0) {
       reset_system();
   }

────────────────────────────────────────────────────────────────────────────

**2.2 Fault Tolerance**
-----------------------

**Goal:** Mask faults so they don't cause service failure

**Techniques:**

**Hardware Redundancy:**

.. code-block:: text

   TMR (Triple Modular Redundancy):
   
   Input → [ Sensor A ] ───┐
           [ Sensor B ] ───┤→ VOTER → Output
           [ Sensor C ] ───┘
   
   Majority voting: 2-out-of-3 must agree
   → Tolerates 1 sensor failure

**Software Redundancy:**
- N-version programming (independent implementations)
- Recovery blocks (primary + backup algorithms)
- Checkpointing (save state, rollback on error)

**Information Redundancy:**
- CRC (Cyclic Redundancy Check) for error detection
- Hamming codes (detect + correct bit flips)
- Parity (simple error detection)

**Time Redundancy:**
- Re-execution (run same code twice, compare)
- Watchdog timers (detect timing violations)
- Timeouts (abort hung operations)

**Example: TMR in Flight Control (Airbus A380)**

.. code-block:: c

   typedef struct {
       float sensor_a;
       float sensor_b;
       float sensor_c;
   } TripleInput;
   
   float voter(TripleInput inputs) {
       // Simple median voting
       float values[3] = {inputs.sensor_a, inputs.sensor_b, inputs.sensor_c};
       
       // Sort
       if (values[0] > values[1]) swap(&values[0], &values[1]);
       if (values[1] > values[2]) swap(&values[1], &values[2]);
       if (values[0] > values[1]) swap(&values[0], &values[1]);
       
       return values[1];  // Middle value (median)
   }

────────────────────────────────────────────────────────────────────────────

**2.3 Fault Removal**
---------------------

**Goal:** Detect and eliminate faults before deployment

**Techniques:**

**Verification (Design Correctness):**
- Formal verification (model checking, theorem proving)
- Static analysis (control flow, data flow)
- Code inspections (peer review, walkthroughs)
- Safety analysis (FMEA, FTA, HAZOP)

**Validation (Meets Requirements):**
- Functional testing (black-box, requirements-based)
- Structural testing (white-box, MC/DC coverage)
- Integration testing (component interactions)
- System testing (end-to-end scenarios)

**Operational Removal:**
- Fault injection testing (simulate failures)
- Stress testing (overload, boundary conditions)
- Regression testing (ensure fixes don't break existing)
- Field trials (beta testing, pilot deployment)

**Example: MC/DC Coverage (DO-178C DAL A)**

.. code-block:: c

   // Requirement: "Activate brake if (speed > 50) AND (pedal pressed)"
   bool activate_brake(int speed, bool pedal) {
       if (speed > 50 && pedal) {  // Decision with 2 conditions
           return true;
       }
       return false;
   }
   
   // MC/DC Test Cases (each condition independently affects outcome):
   // TC1: speed=60, pedal=true  → true  (baseline: both true)
   // TC2: speed=40, pedal=true  → false (speed affects outcome)
   // TC3: speed=60, pedal=false → false (pedal affects outcome)

────────────────────────────────────────────────────────────────────────────

**2.4 Fault Forecasting**
-------------------------

**Goal:** Predict future faults through modeling and assessment

**Techniques:**

**Qualitative Forecasting:**
- FMEA (identify potential failure modes)
- FTA (systematic fault propagation analysis)
- HAZOP (hazard and operability study)
- Expert judgment (Delphi method)

**Quantitative Forecasting:**
- Reliability prediction (MTBF calculations)
- Markov models (state transition probabilities)
- Petri nets (concurrent system modeling)
- Fault injection (empirical failure data)

**Example: Reliability Block Diagram (RBD)**

.. code-block:: text

   System Reliability Calculation (Series):
   
   [Component A]──[Component B]──[Component C]
   R_A = 0.99     R_B = 0.98     R_C = 0.97
   
   R_system = R_A × R_B × R_C
            = 0.99 × 0.98 × 0.97
            = 0.941 (94.1%)
   
   System Reliability Calculation (Parallel - Redundant):
   
           ┌──[Component A]──┐
   Input ──┤                  ├── Output
           └──[Component B]──┘
   R_A = R_B = 0.95
   
   R_system = 1 - (1 - R_A) × (1 - R_B)
            = 1 - (0.05) × (0.05)
            = 1 - 0.0025 = 0.9975 (99.75%)

════════════════════════════════════════════════════════════════════════════

📖 **3. DEPENDABILITY STANDARDS**
════════════════════════════════════════════════════════════════════════════

3.1 EN 50126 (Railway RAMS)
----------------------------

**Full Title:** Railway applications — The specification and demonstration of Reliability, Availability, Maintainability and Safety (RAMS)

**Scope:** Complete RAMS lifecycle for railway systems

**RAMS Lifecycle (14 Phases):**

1. Concept
2. System definition and application conditions
3. Risk analysis
4. System requirements
5. Apportionment of system requirements
6. Design and implementation
7. Manufacture
8. Installation
9. System validation (RAMS)
10. System acceptance
11. Operation and maintenance
12. Performance monitoring
13. Modification and retrofit
14. Decommissioning/disposal

**RAMS Acceptance Criteria Example:**

+-----------+------------------+-------------------+-------------------+
| Parameter | Requirement      | Demonstration     | Acceptance        |
+===========+==================+===================+===================+
| MTBF      | ≥ 50,000 hr      | 60,000 hr (test)  | ✅ PASS           |
+-----------+------------------+-------------------+-------------------+
| MTTR      | ≤ 30 min         | 25 min (avg)      | ✅ PASS           |
+-----------+------------------+-------------------+-------------------+
| Avail.    | ≥ 99.95%         | 99.97% (calc)     | ✅ PASS           |
+-----------+------------------+-------------------+-------------------+
| SIL       | SIL 4 (critical) | EN 50128/50129    | ✅ PASS           |
+-----------+------------------+-------------------+-------------------+

────────────────────────────────────────────────────────────────────────────

**3.2 IEC 61508 (Functional Safety + Dependability)**
------------------------------------------------------

**Dependability Integration in IEC 61508:**

.. code-block:: text

   Part 1: General requirements (dependability context)
   Part 2: Hardware (reliability prediction, fault tolerance)
   Part 3: Software (systematic fault avoidance)
   Part 6: Guidelines (dependability techniques catalog)

**Safe Failure Fraction (SFF) - Linking Reliability & Safety:**

.. code-block:: text

   SFF = (Safe Failures + Dangerous Detected) / Total Dangerous Failures
   
   Higher SFF → Lower Hardware Fault Tolerance (HFT) required
   
   Example: SIL 3 requirement
   - If SFF < 60%  → Need HFT = 2 (triple redundancy)
   - If SFF ≥ 90%  → Need HFT = 0 (simplex OK)

────────────────────────────────────────────────────────────────────────────

**3.3 ISO 26262 (Automotive Dependability)**
---------------------------------------------

**ASIL Decomposition (Leveraging Redundancy):**

.. code-block:: text

   Original Requirement: ASIL D
   
   Decomposed Approach:
   - Element A: ASIL B (with independence)
   - Element B: ASIL B (with independence)
   → Equivalent to ASIL D (notation: ASIL B(D))
   
   Benefits:
   - Easier to develop ASIL B than ASIL D
   - Reuse existing ASIL B components
   - Still achieve ASIL D system safety

**Safety Mechanisms (Fault Tolerance for Automotive):**

+--------------------------+--------------------------------+
| Safety Mechanism         | Dependability Attribute        |
+==========================+================================+
| Watchdog timer           | Availability (detect hangs)    |
+--------------------------+--------------------------------+
| Plausibility checks      | Safety (detect sensor faults)  |
+--------------------------+--------------------------------+
| E2E protection (CRC)     | Integrity (detect corruption)  |
+--------------------------+--------------------------------+
| Graceful degradation     | Availability (partial service) |
+--------------------------+--------------------------------+

════════════════════════════════════════════════════════════════════════════

📖 **4. DEPENDABILITY ASSESSMENT**
════════════════════════════════════════════════════════════════════════════

4.1 Markov Models
-----------------

**Purpose:** Model system states and transitions over time

**Example: 2-Component Redundant System (1oo2)**

.. code-block:: text

   States:
   - State 2: Both components working
   - State 1: One component failed, one working
   - State 0: Both components failed (system failure)
   
   Transitions:
   - 2→1: One component fails (rate 2λ, since either can fail)
   - 1→0: Remaining component fails (rate λ)
   - 1→2: Repair completes (rate μ)
   
   Markov Diagram:
   
        2λ          λ
   (2) ──→ (1) ──→ (0)
         ←──
          μ

**Steady-State Availability Calculation:**

.. code-block:: python

   import numpy as np
   
   def markov_availability_1oo2(lambda_rate, mu_rate):
       """
       lambda_rate: Failure rate per component (failures/hour)
       mu_rate: Repair rate (repairs/hour)
       """
       # Transition matrix Q (infinitesimal generator)
       Q = np.array([
           [-2*lambda_rate, 2*lambda_rate, 0],
           [mu_rate, -(lambda_rate + mu_rate), lambda_rate],
           [0, 0, 0]
       ])
       
       # Solve π*Q = 0, sum(π) = 1
       # Using normalization: π_0 + π_1 + π_2 = 1
       
       # Simplified result (steady-state probabilities):
       rho = lambda_rate / mu_rate
       π_2 = 1 / (1 + 2*rho + 2*rho**2)
       π_1 = 2*rho * π_2
       π_0 = 2*rho**2 * π_2
       
       # Availability = P(not in failed state)
       A = π_2 + π_1
       return A
   
   # Example: λ = 1e-5 /hr, μ = 0.5 /hr (MTTR = 2 hr)
   A = markov_availability_1oo2(1e-5, 0.5)
   print(f"Availability: {A:.6f} ({A*100:.4f}%)")
   # Output: Availability: 0.999960 (99.9960%)

────────────────────────────────────────────────────────────────────────────

**4.2 Petri Nets**
------------------

**Purpose:** Model concurrent events and resource sharing

**Example: Producer-Consumer System**

.. code-block:: text

   Places:   P1 (buffer empty), P2 (buffer full)
   Transitions: T1 (produce), T2 (consume)
   
   Petri Net:
   
       P1 ──→ [T1] ──→ P2 ──→ [T2] ──┐
        ↑                             │
        └─────────────────────────────┘
   
   Marking: Number of tokens in each place
   - Initial: M0 = {P1:1, P2:0} (buffer empty, ready to produce)
   - After T1 fires: M1 = {P1:0, P2:1} (buffer full, ready to consume)

**Dependability Analysis:**
- **Reachability**: Can system reach unsafe state?
- **Liveness**: Will transitions always be enabled eventually?
- **Boundedness**: Maximum tokens in buffer (resource limits)

────────────────────────────────────────────────────────────────────────────

**4.3 Fault Tree Analysis (FTA) for Dependability**
----------------------------------------------------

**Linking FTA to Dependability Attributes:**

**Reliability:** Calculate top event probability

.. code-block:: text

   Top Event: System Failure
        │
        ◇ (OR gate)
      ┌─┴─┐
   Comp A  Comp B
   P=10⁻³  P=10⁻³
   
   P(System Failure) = P(A) + P(B) - P(A)×P(B)
                     = 10⁻³ + 10⁻³ - 10⁻⁶
                     ≈ 2×10⁻³ (0.2%)
   
   R(System) = 1 - P(System Failure) = 0.998 (99.8%)

**Safety:** Calculate dangerous failure probability

.. code-block:: text

   Dangerous Failures Only (ignore safe failures)
   → Use FTA with only dangerous basic events

**Availability:** Include repair transitions

.. code-block:: text

   Convert FTA to Fault Tree with Repair
   → Use dynamic fault trees or Markov models

════════════════════════════════════════════════════════════════════════════

📖 **5. DEPENDABILITY IN PRACTICE**
════════════════════════════════════════════════════════════════════════════

5.1 Automotive Example: Brake-by-Wire
--------------------------------------

**System:** Electronic brake system (no mechanical backup)

**Dependability Requirements:**

+----------------+----------------------+---------------------------+
| Attribute      | Requirement          | Design Solution           |
+================+======================+===========================+
| Reliability    | MTBF > 10⁶ hours     | Automotive-grade parts    |
+----------------+----------------------+---------------------------+
| Availability   | >99.999% (5-nines)   | Dual ECU, hot standby     |
+----------------+----------------------+---------------------------+
| Maintainability| MTTR < 1 hour        | Modular design, OBD-II    |
+----------------+----------------------+---------------------------+
| Safety         | ASIL D               | Fail-operational (2 lanes)|
+----------------+----------------------+---------------------------+
| Security       | Resist CAN injection | Message authentication    |
+----------------+----------------------+---------------------------+

**Architecture:**

.. code-block:: text

   [Brake Pedal Sensor A] ──┐
                            ├──→ [ECU A] ──┐
   [Brake Pedal Sensor B] ──┘              │
                                           VOTER
   [Brake Pedal Sensor C] ──┐              │
                            ├──→ [ECU B] ──┘
   [Brake Pedal Sensor D] ──┘

**Fault Tolerance:**
- Sensor redundancy: 2oo4 voting (2-out-of-4)
- ECU redundancy: Dual lane, cross-checked
- Power supply: Independent 12V and 48V rails

────────────────────────────────────────────────────────────────────────────

**5.2 Avionics Example: Flight Control Computer**
--------------------------------------------------

**System:** Fly-by-wire flight control (Airbus A350)

**Dependability Architecture:**

.. code-block:: text

   Triple Redundant (TMR):
   - 3× Primary Flight Computers (PRIM1, PRIM2, PRIM3)
   - 2× Secondary Flight Computers (SEC1, SEC2)
   - 2× Backup Flight Control Units (FCCU1, FCCU2)

**Dependability Measures:**

**Reliability:**
- λ per computer = 500 FIT (5×10⁻⁷ /hr)
- TMR MTBF = (1 / (3λ²)) = 4.4×10⁵ hours (50 years)

**Availability:**
- Hot standby switching (< 1ms failover)
- Continuous operation despite 1 computer failure

**Maintainability:**
- Line-Replaceable Units (LRUs) for quick swap
- Built-In Test Equipment (BITE) for fault isolation

**Safety:**
- DO-178C DAL A (Software)
- DO-254 DAL A (Hardware)
- Formal verification for critical functions

────────────────────────────────────────────────────────────────────────────

**5.3 Railway Example: Signaling Interlocking**
------------------------------------------------

**System:** Railway interlocking (prevents conflicting train movements)

**Dependability (EN 50126 RAMS):**

+-----------------+---------------------+----------------------------+
| Attribute       | Target              | Design Approach            |
+=================+=====================+============================+
| **Reliability** | MTBF > 10⁸ hours    | 2oo3 voting                |
+-----------------+---------------------+----------------------------+
| **Availability**| 99.999% (5-nines)   | Hot standby processor      |
+-----------------+---------------------+----------------------------+
| **Maintain.**   | MTTR < 15 min       | Plug-in modules, diagnostics|
+-----------------+---------------------+----------------------------+
| **Safety**      | SIL 4 (EN 50128)    | Fail-safe relay logic      |
+-----------------+---------------------+----------------------------+

**Fail-Safe Design:**

.. code-block:: text

   Relay Logic (De-Energize to Safe):
   
   Signal Aspect:
   - GREEN: Relay energized (power applied, proceed)
   - RED: Relay de-energized (no power, STOP)
   
   Any fault (power loss, relay failure) → RED (safe state)

════════════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════════════════════════════════════════════════════════

**Q1:** What is the difference between Reliability and Availability?

**A1:**

**Reliability:** Probability of failure-free operation for a given time  
**Availability:** Proportion of time system is operational (includes repair time)

*Example:*

.. code-block:: text

   System A: MTBF = 10,000 hr, MTTR = 100 hr
   System B: MTBF = 1,000 hr,  MTTR = 1 hr
   
   Reliability (at 100 hr):
   R_A = e^(-100/10000) = 0.990 (99.0%)
   R_B = e^(-100/1000)  = 0.905 (90.5%)
   → System A more reliable
   
   Availability:
   A_A = 10000/(10000+100) = 0.990 (99.0%)
   A_B = 1000/(1000+1)     = 0.999 (99.9%)
   → System B more available (faster repair)

────────────────────────────────────────────────────────────────────────────

**Q2:** Calculate system availability for a redundant pair (1oo2): MTTF=1000hr each, MTTR=2hr. Assume independent failures.

**A2:**

**Step 1:** Calculate single component availability

.. code-block:: text

   A_component = MTTF / (MTTF + MTTR)
               = 1000 / (1000 + 2) = 0.998

**Step 2:** For parallel redundancy (1oo2 - system works if at least 1 works):

.. code-block:: text

   A_system = 1 - (1 - A_component)²
            = 1 - (1 - 0.998)²
            = 1 - (0.002)²
            = 1 - 0.000004 = 0.999996 (99.9996%)

**Step 3:** Downtime per year

.. code-block:: text

   Downtime = (1 - A) × 365 days
            = 0.000004 × 365 × 24 hours
            = 0.035 hours = 2.1 minutes/year

────────────────────────────────────────────────────────────────────────────

**Q3:** Name the 4 dependability means and give 1 example of each.

**A3:**

1. **Fault Prevention** — MISRA C coding standard (prevent bugs)
2. **Fault Tolerance** — TMR voting (mask faults)
3. **Fault Removal** — MC/DC testing (detect and remove)
4. **Fault Forecasting** — FMEA (predict potential failures)

────────────────────────────────────────────────────────────────────────────

**Q4:** Why is dependability different from just reliability?

**A4:**

**Dependability** is a **composite attribute** encompassing multiple concerns:
- Reliability (continuity of service)
- Availability (readiness of service)
- Maintainability (ease of repair)
- Safety (absence of catastrophic harm)
- Security (resistance to attacks)

**Reliability alone** only addresses failure-free operation time, ignoring:
- How quickly repairs happen (maintainability)
- What happens when failure occurs (safety)
- Whether system is under attack (security)

*Example:* A highly reliable system (MTBF = 10 years) with MTTR = 1 month has poor availability (99.2%). A dependable system optimizes ALL attributes.

────────────────────────────────────────────────────────────────────────────

**Q5:** What is a Safe Failure Fraction (SFF) in IEC 61508, and why does it matter?

**A5:**

**SFF = (Safe Failures + Dangerous Detected Failures) / Total Dangerous Failures**

*Interpretation:* Fraction of dangerous failures that are either safe or detected.

**Why It Matters:**

Higher SFF → Reduced Hardware Fault Tolerance (HFT) requirement

.. code-block:: text

   SIL 3 Requirements:
   - SFF < 60%  → Need HFT = 2 (triple redundancy, expensive)
   - SFF 60-90% → Need HFT = 1 (dual redundancy)
   - SFF ≥ 90%  → Need HFT = 0 (simplex OK, cheaper)

**Engineering Impact:**  
Invest in good diagnostics (increase dangerous detected failures) → achieve SIL 3 with simplex hardware instead of triple redundancy.

*Example:* Pressure sensor with self-test (detects 95% of dangerous faults) → SFF = 95% → SIL 3 with single sensor.

════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Fundamentals:**
- [ ] Understand Faults → Errors → Failures chain
- [ ] Define all 5 RAMS-S attributes (R, A, M, S, S)
- [ ] Explain dependability means (prevention, tolerance, removal, forecasting)

**Metrics:**
- [ ] Calculate reliability: R(t) = e^(-λt)
- [ ] Calculate availability: A = MTTF/(MTTF+MTTR)
- [ ] Compute redundant system availability: 1-(1-A)^n
- [ ] Determine SFF and required HFT (IEC 61508 Table)

**Modeling:**
- [ ] Build Markov model for 2-component redundant system
- [ ] Draw Reliability Block Diagram (series, parallel, mixed)
- [ ] Construct Fault Tree and calculate top event probability

**Standards:**
- [ ] Identify RAMS lifecycle phases (EN 50126)
- [ ] Map dependability to SIL (IEC 61508)
- [ ] Apply ASIL decomposition (ISO 26262)

**Application:**
- [ ] Design fail-safe architecture (railway signal example)
- [ ] Design fail-operational architecture (brake-by-wire)
- [ ] Specify RAMS requirements for new safety-critical system

════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════════════════════════════════════════════════════════════

1️⃣ **Dependability = R + A + M + S + S** — Composite attribute, not single metric

2️⃣ **Reliability ≠ Availability** — Reliability is failure-free time; availability includes repair (uptime ratio)

3️⃣ **4 Dependability Means** — Prevention, Tolerance, Removal, Forecasting (all needed for robust system)

4️⃣ **Fault Tolerance costs** — Redundancy improves availability/reliability but adds complexity, cost, weight

5️⃣ **Safety vs Reliability** — Safe ≠ Reliable; must consider failure mode (fail-safe design)

6️⃣ **Trade-offs exist** — Higher availability often means lower MTTR (faster repair) at expense of maintainability complexity

7️⃣ **Standards integration** — EN 50126 (railway RAMS), IEC 61508 (safety + dependability), ISO 26262 (automotive)

════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **DEPENDABILITY ENGINEERING CHEATSHEET COMPLETE**

**Created:** January 15, 2026  
**Coverage:** Dependability fundamentals, RAMS attributes, dependability means (prevention/tolerance/removal/forecasting), Markov models, Petri nets, FTA integration, standards (EN 50126, IEC 61508, ISO 26262), automotive/avionics/railway examples

════════════════════════════════════════════════════════════════════════════
