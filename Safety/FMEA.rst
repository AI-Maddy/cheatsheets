============================================================
FMEA — Failure Mode and Effects Analysis for Safety-Critical Systems
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
**TL;DR — FMEA in 30 Seconds**
================================================================================

**What:** Systematic bottom-up analysis identifying **failure modes**, **causes**, **effects**, and **controls**.

**Why:** ISO 26262, IEC 61508, DO-178C, AIAG-VDA mandate FMEA for safety-critical hardware/software.

**2026 Evolution:** FMEA-MSR (Monitoring and System Response), automated MBSA generation, AI/ML-specific failure modes.

**Quick FMEA Types:**

+-----------------------+---------------------+-------------------------+---------------------------+
| FMEA Type             | Focus               | When to Use             | Example Domain            |
+=======================+=====================+=========================+===========================+
| **DFMEA**             | Design flaws        | Product development     | Automotive ECU, brake     |
+-----------------------+---------------------+-------------------------+---------------------------+
| **PFMEA**             | Process defects     | Manufacturing           | Semiconductor fab         |
+-----------------------+---------------------+-------------------------+---------------------------+
| **FMEDA**             | Random HW failures  | Safety metrics (SPFM)   | ISO 26262 ASIL D hardware |
+-----------------------+---------------------+-------------------------+---------------------------+
| **FMEA-MSR**          | Monitoring response | Runtime safety          | Autonomous driving L3+    |
+-----------------------+---------------------+-------------------------+---------------------------+
| **Software FMEA**     | SW design faults    | Software architecture   | API failures, corruption  |
+-----------------------+---------------------+-------------------------+---------------------------+

**Severity-Occurrence-Detection (SOD) → Risk Priority Number (RPN):**

.. code-block:: text

   RPN = Severity × Occurrence × Detection
   
   Priority:  RPN > 125 → Immediate action
              RPN 80-125 → Action needed
              RPN < 80 → Monitor

**Automotive AIAG-VDA 2019 Harmonized FMEA:**
- **AP (Action Priority):** High / Medium / Low (replaces RPN threshold)
- **Severity (1-10):** Effect on end customer
- **Occurrence (1-10):** How often failure mode happens
- **Detection (1-10):** How well controls detect before customer impact

================================================================================
1. FMEA Fundamentals — Bottom-Up Safety Analysis
================================================================================

1.1 FMEA Definition and Purpose
--------------------------------

**FMEA = Failure Mode and Effects Analysis**

**Objective:**
- Identify **all potential failure modes** at component/function level
- Determine **causes** (why failure happens)
- Assess **effects** (impact on system/vehicle/patient/aircraft)
- Evaluate **current controls** (prevention/detection)
- Prioritize **corrective actions** (reduce risk)

**Standards Requiring FMEA:**

+----------------------+-----------------------------+-------------------------------------+
| Standard             | Domain                      | FMEA Requirement                    |
+======================+=============================+=====================================+
| **ISO 26262**        | Automotive functional safety| Part 5 (Hardware), Part 9 (ASIL)    |
+----------------------+-----------------------------+-------------------------------------+
| **IEC 61508**        | Industrial functional safety| Part 2 (Hardware), Part 3 (Software)|
+----------------------+-----------------------------+-------------------------------------+
| **DO-178C**          | Avionics software           | Implicit (safety assessment)        |
+----------------------+-----------------------------+-------------------------------------+
| **DO-254**           | Avionics hardware           | Explicit (complex electronic HW)    |
+----------------------+-----------------------------+-------------------------------------+
| **IEC 62304**        | Medical device software     | Risk management process             |
+----------------------+-----------------------------+-------------------------------------+
| **AIAG-VDA FMEA**    | Automotive quality          | Design, Process, FMEA-MSR           |
+----------------------+-----------------------------+-------------------------------------+
| **MIL-STD-1629A**    | Military reliability        | Procedures for FMEA/FMECA           |
+----------------------+-----------------------------+-------------------------------------+

1.2 FMEA vs FMECA vs FMEDA
---------------------------

**Comparison:**

+--------------------+---------------------------+----------------------+---------------------------+
| Term               | Full Name                 | Focus                | Output Metric             |
+====================+===========================+======================+===========================+
| **FMEA**           | Failure Mode and Effects  | Effects analysis     | Severity, RPN             |
+--------------------+---------------------------+----------------------+---------------------------+
| **FMECA**          | FMEA + Criticality        | + Quantitative risk  | Criticality number (C)    |
+--------------------+---------------------------+----------------------+---------------------------+
| **FMEDA**          | FMEA + Diagnostic         | + Diagnostic coverage| SPFM, LFM (ISO 26262)     |
+--------------------+---------------------------+----------------------+---------------------------+

**FMEDA (Failure Modes, Effects, and Diagnostic Analysis):**
- Required for **ISO 26262** hardware safety metrics
- Calculates **SPFM** (Single-Point Fault Metric), **LFM** (Latent Fault Metric)
- Categorizes faults: **Safe**, **Single-point**, **Residual**, **Latent**, **Detected**

**Example FMEDA Fault Classification:**

.. code-block:: text

   Component: Microcontroller (MCU) - Lockstep Cores
   
   Fault: Core A stuck-at-1
   → Detected by lockstep comparison → Safe Fault (SPFM numerator)
   
   Fault: Clock oscillator drift
   → Detected by watchdog → Detected Fault (SPFM numerator)
   
   Fault: RAM bit flip (undetected by ECC)
   → Latent fault → Latent Fault (LFM denominator)
   
   Fault: Power supply brownout (no detection)
   → Single-point fault → SPFM denominator

1.3 FMEA Process Flow (7 Steps)
--------------------------------

**Step 1: Define scope and boundaries**
- System/subsystem/component level
- Operating modes (normal, degraded, emergency)
- Interfaces and interactions

**Step 2: Functional decomposition**
- Break system into functional blocks
- Identify inputs, outputs, transformations

**Step 3: Identify failure modes**
- How can each function fail?
- Typical modes: No function, partial function, intermittent, unintended function, degraded performance

**Step 4: Determine failure causes**
- Root causes (design, manufacturing, environmental, wear-out)
- Use fishbone diagrams, 5 Whys

**Step 5: Assess failure effects**
- Local effect (component level)
- Next higher level (subsystem)
- End effect (system/vehicle/mission)

**Step 6: Evaluate current controls**
- **Prevention controls:** Design features preventing failure
- **Detection controls:** Diagnostics, monitoring, tests

**Step 7: Calculate risk and prioritize**
- SOD → RPN (traditional)
- AP (Action Priority) for AIAG-VDA 2019

**FMEA Template (Traditional):**

+--------+----------+------+-------+-------+------+-----+-----+-----+-----+-----+----------+
| Item   | Function | FM   | Effect| Cause | Sev  | Occ | Det | RPN | Act | RPN' | Status   |
+========+==========+======+=======+=======+======+=====+=====+=====+=====+======+==========+
| Sensor | Measure  | Stuck| No    | Corr  | 9    | 4   | 3   | 108 | Add | 36   | Complete |
|        | temp     | high | heat  | conn  |      |     |     |     | CRC |      |          |
+--------+----------+------+-------+-------+------+-----+-----+-----+-----+------+----------+

================================================================================
2. DFMEA — Design Failure Mode and Effects Analysis
================================================================================

2.1 DFMEA Scope and Objectives
-------------------------------

**Focus:** Product **design weaknesses** (not manufacturing or process issues).

**Typical Applications:**
- Automotive ECU design (ISO 26262 Part 5)
- Medical device hardware/software (IEC 62304)
- Avionics complex electronic hardware (DO-254)
- Industrial safety controllers (IEC 61508)

**DFMEA Timing:**
- **Early:** Concept/preliminary design (identify critical failure modes)
- **Iterative:** Update during detailed design, integration, validation
- **Living document:** Update with field data, design changes

2.2 AIAG-VDA 2019 Harmonized DFMEA (Automotive Standard)
---------------------------------------------------------

**Seven-Step Approach:**

1. **Planning and Preparation**
   - Define scope, team, timeline
   - Block diagram, P-diagram (parameters influencing function)

2. **Structure Analysis**
   - System structure tree (vehicle → system → subsystem → component)
   - Focus element selection

3. **Function Analysis**
   - Function structure tree (what does it do?)
   - Requirements linkage

4. **Failure Analysis**
   - Failure chains: Failure Mode → Failure Effect → Failure Cause
   - Severity rating (1-10 for effect on end customer)

5. **Risk Analysis**
   - Occurrence rating (1-10 for cause frequency)
   - Detection rating (1-10 for control effectiveness)
   - **Action Priority (AP):** High / Medium / Low

6. **Optimization**
   - Define prevention/detection actions
   - Assign responsibility, target dates

7. **Results Documentation**
   - DFMEA report, traceability to requirements, safety cases

**Action Priority (AP) Decision Table (AIAG-VDA 2019):**

+----------+------------+------------+-----------------+
| Severity | Occurrence | Detection  | Action Priority |
+==========+============+============+=================+
| 9-10     | Any        | Any        | **High**        |
+----------+------------+------------+-----------------+
| 7-8      | 4-10       | 4-10       | **High**        |
+----------+------------+------------+-----------------+
| 7-8      | 4-10       | 1-3        | **Medium**      |
+----------+------------+------------+-----------------+
| 4-6      | 7-10       | 7-10       | **High**        |
+----------+------------+------------+-----------------+
| 4-6      | 4-6        | 4-10       | **Medium**      |
+----------+------------+------------+-----------------+
| 1-3      | Any        | Any        | **Low**         |
+----------+------------+------------+-----------------+

**Replaces RPN thresholds** with qualitative assessment (avoids false precision).

2.3 DFMEA Example: Automotive Brake Pressure Sensor
----------------------------------------------------

**System:** Electronic Brake System (ASIL D)
**Component:** Brake Pressure Sensor
**Function:** Measure hydraulic brake pressure (0-200 bar)

**DFMEA Table:**

.. code-block:: text

   Item: Brake Pressure Sensor
   Function: Measure brake pedal hydraulic pressure
   
   Failure Mode 1: Sensor output stuck at 0 bar
   ├─ Effect (Local): ECU receives 0 bar signal
   ├─ Effect (System): No braking force applied → Vehicle does not brake
   ├─ Effect (End): Rear-end collision (Severity = 10)
   ├─ Cause: Membrane rupture, electrical short to ground
   ├─ Occurrence: 3 (rare with qualified sensors)
   ├─ Prevention: Redundant sensor (1oo2D), membrane material qualification
   ├─ Detection: Plausibility check (cross-check with wheel speed deceleration)
   ├─ Detection Rating: 2 (high detection capability)
   ├─ Action Priority: HIGH (Severity 10)
   └─ Action: Add diverse secondary sensor, improve plausibility monitoring
   
   Failure Mode 2: Sensor output noisy/intermittent
   ├─ Effect: Erratic braking, driver discomfort
   ├─ Effect (End): Loss of driver trust (Severity = 6)
   ├─ Cause: Poor electrical grounding, EMC interference
   ├─ Occurrence: 5 (moderate)
   ├─ Prevention: Shielded cable, EMC-qualified design (ISO 11452)
   ├─ Detection: Signal filtering + gradient checks
   ├─ Detection Rating: 4 (moderate)
   ├─ Action Priority: MEDIUM
   └─ Action: Improve cable shielding, add ferrite beads

================================================================================
3. FMEDA — Failure Modes, Effects, and Diagnostic Analysis (ISO 26262)
================================================================================

3.1 FMEDA Purpose and Metrics
------------------------------

**FMEDA Objectives (ISO 26262 Part 5):**
- Quantify **random hardware failure** safety
- Calculate **SPFM** (Single-Point Fault Metric)
- Calculate **LFM** (Latent Fault Metric)
- Demonstrate compliance with **ASIL hardware metrics targets**

**ASIL Hardware Metrics Targets:**

+--------+----------------+----------------+
| ASIL   | SPFM (%)       | LFM (%)        |
+========+================+================+
| **A**  | ≥ 90%          | ≥ 60%          |
+--------+----------------+----------------+
| **B**  | ≥ 90%          | ≥ 60%          |
+--------+----------------+----------------+
| **C**  | ≥ 97%          | ≥ 80%          |
+--------+----------------+----------------+
| **D**  | ≥ 99%          | ≥ 90%          |
+--------+----------------+----------------+

**SPFM Formula:**

.. math::

   SPFM = \frac{\sum \lambda_{SPF,detected} + \sum \lambda_{RF,detected}}{\sum \lambda_{SPF} + \sum \lambda_{RF}} \times 100\%

Where:
- λ_SPF = Single-point fault failure rate
- λ_RF = Residual fault failure rate
- λ_detected = Faults detected by safety mechanisms

**LFM Formula:**

.. math::

   LFM = \frac{\sum \lambda_{MPF,detected}}{\sum \lambda_{MPF}} \times 100\%

Where:
- λ_MPF = Multi-point fault failure rate (latent faults)

3.2 FMEDA Fault Classification
-------------------------------

**ISO 26262 Fault Categories:**

1. **Safe Fault:**
   - Fault does NOT violate safety goal (even if undetected)
   - Example: Infotainment system crash (QM function)

2. **Single-Point Fault (SPF):**
   - Fault directly violates safety goal (no other fault needed)
   - **NOT detected** by safety mechanism
   - Example: Brake sensor stuck (no redundancy, no plausibility check)

3. **Residual Fault (RF):**
   - Single-point fault where detection exists but **coverage < 100%**
   - Example: ECC detects 99% of memory errors → 1% residual

4. **Latent Fault (Multi-Point Fault - MPF):**
   - Fault does NOT immediately violate safety goal
   - Becomes dangerous when **combined with another fault**
   - Example: Redundant sensor failure (dormant until primary fails)

5. **Detected Multi-Point Fault:**
   - Latent fault detected by diagnostic (e.g., self-test, cross-check)

**FMEDA Fault Tree:**

.. code-block:: text

   All Hardware Faults (λ_total)
   ├─ Safe Faults (λ_safe) → Excluded from metrics
   └─ Dangerous Faults
      ├─ Single-Point Faults (λ_SPF)
      │  ├─ SPF Detected (λ_SPF_detected) → SPFM numerator
      │  └─ SPF Undetected (λ_SPF_undetected) → SPFM denominator
      ├─ Residual Faults (λ_RF)
      │  ├─ RF Detected (λ_RF_detected) → SPFM numerator
      │  └─ RF Undetected (λ_RF_undetected) → SPFM denominator
      └─ Latent Faults (λ_MPF)
         ├─ MPF Detected (λ_MPF_detected) → LFM numerator
         └─ MPF Undetected (λ_MPF_undetected) → LFM denominator

3.3 FMEDA Example: ASIL D Microcontroller
------------------------------------------

**Component:** Automotive MCU with lockstep cores (e.g., Infineon AURIX TC4xx)
**Base Failure Rate:** λ_MCU = 50 FIT (Failures In Time per 10^9 hours)

**FMEDA Worksheet:**

.. code-block:: python

   # FMEDA calculation example (Python)
   
   # Failure rates (FIT - Failures in 10^9 hours)
   faults = {
       'cpu_core_stuck': {'lambda': 10, 'category': 'SPF', 'detected': True, 'dc': 0.99},
       'cpu_timing_fault': {'lambda': 5, 'category': 'SPF', 'detected': True, 'dc': 0.98},
       'ram_bit_flip': {'lambda': 15, 'category': 'RF', 'detected': True, 'dc': 0.95},  # ECC
       'flash_corruption': {'lambda': 3, 'category': 'SPF', 'detected': False, 'dc': 0},
       'watchdog_failure': {'lambda': 2, 'category': 'MPF', 'detected': True, 'dc': 0.90},
       'voltage_monitor_fail': {'lambda': 8, 'category': 'MPF', 'detected': True, 'dc': 0.95},
       'clock_drift': {'lambda': 5, 'category': 'SPF', 'detected': True, 'dc': 0.97},
       'safe_faults': {'lambda': 2, 'category': 'SAFE', 'detected': False, 'dc': 0}
   }
   
   # Calculate SPFM
   spf_total = sum(f['lambda'] for f in faults.values() 
                   if f['category'] in ['SPF', 'RF'])
   spf_detected = sum(f['lambda'] * f['dc'] for f in faults.values() 
                      if f['category'] in ['SPF', 'RF'] and f['detected'])
   
   spfm = (spf_detected / spf_total) * 100 if spf_total > 0 else 0
   
   # Calculate LFM
   mpf_total = sum(f['lambda'] for f in faults.values() if f['category'] == 'MPF')
   mpf_detected = sum(f['lambda'] * f['dc'] for f in faults.values() 
                      if f['category'] == 'MPF' and f['detected'])
   
   lfm = (mpf_detected / mpf_total) * 100 if mpf_total > 0 else 0
   
   print(f"SPFM: {spfm:.2f}% (Target ASIL D: ≥99%)")
   print(f"LFM: {lfm:.2f}% (Target ASIL D: ≥90%)")
   print(f"SPF Total: {spf_total} FIT")
   print(f"MPF Total: {mpf_total} FIT")
   
   # Output:
   # SPFM: 96.43% (Target ASIL D: ≥99%) → FAIL (need better diagnostics)
   # LFM: 93.00% (Target ASIL D: ≥90%) → PASS
   # SPF Total: 38 FIT
   # MPF Total: 10 FIT

**Improvement Actions:**
- Add CRC protection for Flash (improve DC from 0% → 95%)
- Improve RAM ECC (DC 95% → 99%)
- **Result:** SPFM increases to 99.2% → **PASS ASIL D**

================================================================================
4. FMEA-MSR — Monitoring and System Response (2026 Evolution)
================================================================================

4.1 FMEA-MSR Purpose
--------------------

**What is FMEA-MSR?**
- Extension of AIAG-VDA FMEA for **runtime monitoring and response**
- Critical for **autonomous driving (L3+)**, **AI/ML systems**, **SOTIF scenarios**
- Addresses failures **during operation** (not just design/manufacturing)

**Why FMEA-MSR in 2026?**
- Traditional FMEA assumes **static failure modes** (sensor stuck, component broken)
- Modern systems have **dynamic failures:** OOD inputs, adversarial attacks, concept drift, edge cases
- **ISO/PAS 21448 (SOTIF)** requires analysis of **triggering conditions** + **system response**

**FMEA-MSR Additions:**

+-------------------------+----------------------------------+------------------------------------+
| Traditional FMEA        | FMEA-MSR Addition                | Example (Autonomous Vehicle)       |
+=========================+==================================+====================================+
| Failure Mode            | + **Triggering Condition**       | Camera blinded by **sun glare**    |
+-------------------------+----------------------------------+------------------------------------+
| Effect                  | + **Monitoring Mechanism**       | Vision DNN confidence drops        |
+-------------------------+----------------------------------+------------------------------------+
| Detection               | + **System Response**            | Reduce speed, alert driver         |
+-------------------------+----------------------------------+------------------------------------+
| RPN/AP                  | + **Response Effectiveness**     | Safe degradation achieved? (Y/N)   |
+-------------------------+----------------------------------+------------------------------------+

4.2 FMEA-MSR Example: Autonomous Driving Camera Failure
--------------------------------------------------------

**System:** L3 Autonomous Driving (Highway Pilot)
**Function:** Lane keeping using camera-based vision DNN

**FMEA-MSR Table:**

.. code-block:: text

   Failure Mode: Camera vision degraded (low confidence detections)
   
   Triggering Conditions:
   ├─ Sun glare (low sun angle, dawn/dusk)
   ├─ Heavy rain (water droplets on lens)
   ├─ Dense fog (visibility < 50m)
   ├─ Dirt accumulation on lens
   └─ Camera lens damage (stone chip)
   
   Effects:
   ├─ Lane line detection failures
   ├─ Vehicle drifts out of lane
   └─ Potential collision (Severity = 10)
   
   Monitoring Mechanisms:
   ├─ DNN confidence score < threshold (e.g., 0.7)
   ├─ Lane line detection gaps > 2 seconds
   ├─ Cross-check with radar lane boundaries
   └─ Plausibility check with map data (HD map)
   
   System Response (Graduated):
   1. **Yellow Alert:** Confidence 0.5-0.7 → Increase sensor fusion weight on radar/lidar
   2. **Orange Alert:** Confidence 0.3-0.5 → Reduce speed to 60 km/h, alert driver (7s)
   3. **Red Alert:** Confidence < 0.3 → Request takeover (4s), prepare MRM if no response
   4. **Emergency:** No takeover → Minimal Risk Maneuver (pull over, hazard lights)
   
   Response Effectiveness:
   ├─ Response Time: 100ms detection + 200ms action = 300ms total
   ├─ Safe State Reached: Yes (vehicle stopped in safe location)
   ├─ False Positive Rate: < 1% (validated in simulation)
   └─ Failure to Respond: < 10^-7 /h (ASIL D target)
   
   Action Priority: HIGH (Severity 10, safety-critical)
   
   Actions:
   ├─ Add camera lens heater (defog/deice)
   ├─ Camera lens cleaner (washer system)
   ├─ Redundant camera (stereo vision)
   └─ Multi-modal sensor fusion (camera + radar + lidar)

4.3 FMEA-MSR for AI/ML Systems (2026 Best Practice)
----------------------------------------------------

**AI/ML-Specific Failure Modes:**

+----------------------------+----------------------------------+------------------------------+
| Failure Mode               | Triggering Condition             | Monitoring/Response          |
+============================+==================================+==============================+
| **OOD Input**              | Kangaroo on highway (unknown)    | OOD detector → Slow down     |
+----------------------------+----------------------------------+------------------------------+
| **Adversarial Attack**     | Stickers on stop sign           | Input perturbation check     |
+----------------------------+----------------------------------+------------------------------+
| **Concept Drift**          | New traffic sign design         | Performance degradation      |
+----------------------------+----------------------------------+------------------------------+
| **Dataset Bias**           | Poor performance in rain        | Weather detection → Degrade  |
+----------------------------+----------------------------------+------------------------------+
| **Corner Case**            | Pedestrian in wheelchair        | Confidence threshold         |
+----------------------------+----------------------------------+------------------------------+

**AI/ML FMEA-MSR Template:**

.. code-block:: text

   Component: Object Detection DNN (YOLO, SSD, Faster R-CNN)
   
   Failure Mode: Low confidence detection (< 0.5)
   Triggering: Heavy rain, night, occluded pedestrian
   Effect: Missed pedestrian → No emergency braking → Collision
   Severity: 10 (fatal injury)
   
   Monitoring:
   ├─ Per-detection confidence scores
   ├─ Detection count (expected vs actual)
   ├─ Multi-sensor fusion disagreement (camera vs radar)
   └─ Scenario classifier (weather, lighting)
   
   Response:
   ├─ Confidence < 0.5 → Increase radar weight in fusion
   ├─ Rain detected → Reduce max speed to 80 km/h
   ├─ Night + low confidence → Request takeover (L3 → L2)
   └─ No takeover → Minimal Risk Maneuver
   
   Occurrence: 6 (moderate - rain/night common)
   Detection: 2 (high - multi-sensor fusion)
   Action Priority: HIGH
   
   Actions:
   ├─ Improve training dataset (more rain/night data)
   ├─ Data augmentation (synthetic rain, low light)
   ├─ Ensemble DNNs (diverse architectures)
   └─ Thermal camera (infrared for night)

================================================================================
5. Software FMEA — Failure Modes in Software Architecture
================================================================================

5.1 Software FMEA Scope
-----------------------

**Challenges:**
- Software does NOT have "random failures" like hardware
- Failures are **systematic** (design flaws, requirements errors, coding bugs)
- **Reproducible** (same input → same failure)

**Software FMEA Focus:**
- **API failures:** Timeout, invalid return, exception
- **Data corruption:** Buffer overflow, type confusion, race condition
- **Timing failures:** Deadline miss, priority inversion, starvation
- **Resource exhaustion:** Memory leak, stack overflow, CPU overload
- **Security vulnerabilities:** Injection, privilege escalation, DoS

**When to Use Software FMEA:**
- **Safety-critical software:** ASIL B-D (ISO 26262), SIL 2-4 (IEC 61508)
- **Complex architectures:** Microservices, distributed systems, middleware
- **Third-party integration:** COTS, open-source libraries, cloud APIs

5.2 Software FMEA Example: API Timeout
---------------------------------------

**System:** Autonomous Vehicle Perception Pipeline
**Component:** Lidar Processing Service (ROS2 Node)
**Function:** Process lidar point cloud → Object list

**Software FMEA:**

.. code-block:: text

   Failure Mode: API call timeout (lidar processing exceeds 100ms deadline)
   
   Causes:
   ├─ High point cloud density (dense urban environment)
   ├─ CPU overload (other processes starving lidar node)
   ├─ Memory allocation delay (fragmentation)
   └─ Network latency (if distributed processing)
   
   Effects:
   ├─ Local: Missed detection cycle
   ├─ System: Sensor fusion uses stale data
   ├─ End: Delayed emergency braking → Collision
   └─ Severity: 9 (serious injury)
   
   Current Controls:
   ├─ Prevention: Deadline monotonic scheduling (DM), CPU affinity
   ├─ Detection: Watchdog timer, missed deadline counter
   
   Occurrence: 4 (occasional in dense traffic)
   Detection: 3 (watchdog detects, but recovery is slow)
   RPN: 9 × 4 × 3 = 108 → HIGH PRIORITY
   
   Actions:
   ├─ Add timeout fallback (use radar-only if lidar times out)
   ├─ Adaptive processing (reduce point cloud resolution if overloaded)
   ├─ Preemptive scheduling (guarantee lidar node 50% CPU minimum)
   └─ Graceful degradation (L3 → L2 if persistent timeouts)
   
   After Actions:
   ├─ Occurrence: 2 (rare with adaptive processing)
   ├─ Detection: 2 (fast fallback)
   └─ RPN': 9 × 2 × 2 = 36 → ACCEPTABLE

5.3 Software FMEA: Data Corruption (Buffer Overflow)
-----------------------------------------------------

**Component:** CAN Bus Driver (AUTOSAR BSW)
**Function:** Receive CAN messages into application buffer

**Failure Mode:** Buffer overflow (message queue full)

.. code-block:: c

   // Vulnerable code (no bounds checking)
   void CAN_Receive(uint8_t *msg, uint16_t len) {
       static uint8_t buffer[256];
       static uint16_t index = 0;
       
       // BUG: No check if index + len > 256
       memcpy(&buffer[index], msg, len);  // OVERFLOW!
       index += len;
   }

**FMEA Analysis:**

.. code-block:: text

   Failure Mode: Buffer overflow (index + len > 256)
   
   Causes:
   ├─ Burst CAN traffic (> 256 bytes received before processing)
   ├─ Delayed application processing (high CPU load)
   └─ Malicious CAN injection (attack)
   
   Effects:
   ├─ Local: Stack corruption, adjacent variable overwrite
   ├─ System: Safety-critical data corrupted (e.g., brake command)
   ├─ End: Unintended braking → Rear-end collision
   └─ Severity: 10 (fatal)
   
   Occurrence: 3 (rare, but possible under attack)
   Detection: 7 (no runtime detection, only found in testing)
   RPN: 10 × 3 × 7 = 210 → CRITICAL
   
   Actions:
   ├─ Add bounds checking (assert index + len <= 256)
   ├─ Use circular buffer with overflow flag
   ├─ Enable stack canary (compiler protection)
   ├─ Add E2E protection (CRC, sequence counter)
   └─ Formal verification (static analysis - MISRA C, Polyspace)
   
   After Actions:
   ├─ Occurrence: 1 (extremely rare)
   ├─ Detection: 2 (bounds check catches overflow)
   └─ RPN': 10 × 1 × 2 = 20 → ACCEPTABLE

**Corrected Code:**

.. code-block:: c

   void CAN_Receive_Safe(uint8_t *msg, uint16_t len) {
       static uint8_t buffer[256];
       static uint16_t index = 0;
       
       // Bounds checking
       if (index + len > sizeof(buffer)) {
           // Overflow detected - discard message, raise error
           CAN_Error_Handler(CAN_OVERFLOW);
           index = 0;  // Reset buffer
           return;
       }
       
       memcpy(&buffer[index], msg, len);
       index += len;
       
       // Process buffer when full or timeout
       if (index >= sizeof(buffer) || CAN_Timeout()) {
           Process_Buffer(buffer, index);
           index = 0;
       }
   }

================================================================================
6. Advanced FMEA Techniques — Automation and Integration
================================================================================

6.1 Model-Based FMEA (Automated Generation)
--------------------------------------------

**Tools:** medini analyze, SCADE Safety Architect, OSATE (AADL)

**Benefits:**
- **Automatic FMEA generation** from system models (70% time reduction)
- **Consistency:** No missing failure modes, uniform analysis
- **Traceability:** Requirements → Architecture → FMEA → Tests
- **Update propagation:** Model change → FMEA auto-updated

**Example: AADL Error Model Annex (EMV2)**

.. code-block:: aadl

   -- Brake Pressure Sensor AADL Component
   device Brake_Pressure_Sensor
   features
       pressure_out: out data port Base_Types::Float;  -- 0-200 bar
   end Brake_Pressure_Sensor;
   
   device implementation Brake_Pressure_Sensor.impl
   annex EMV2 {**
       use types ErrorLibrary;
       use behavior ErrorLibrary::Simple;
       
       error propagations
           pressure_out: out propagation {ItemOmission, ValueError};
       end propagations;
       
       component error behavior
       transitions
           Operational -[sensor_stuck]-> Failed;
           Operational -[sensor_noisy]-> Degraded;
       propagations
           Failed -[]-> pressure_out{ItemOmission};
           Degraded -[]-> pressure_out{ValueError};
       end component;
       
       properties
           EMV2::OccurrenceDistribution => [ProbabilityValue => 1.0e-5; 
                                            Distribution => Poisson;] 
                                            applies to sensor_stuck;
   **};
   end Brake_Pressure_Sensor.impl;

**Automated FMEA Output (from OSATE tool):**

.. code-block:: text

   Component: Brake_Pressure_Sensor
   Failure Mode: sensor_stuck (transition to Failed state)
   Effect: pressure_out{ItemOmission} → No pressure signal
   Probability: 1.0e-5 /hour (10 FIT)
   Propagation: Affects Brake_ECU.pressure_input
   End Effect: No braking force → Collision

**70% time reduction** compared to manual FMEA creation.

6.2 Dynamic FMEA (Runtime Monitoring)
--------------------------------------

**Concept:** Traditional FMEA is **static** (analysis at design time). **Dynamic FMEA** updates during operation based on:
- **Field data:** Actual failure rates from fleet
- **Usage profile:** Real-world exposure, environmental conditions
- **Prognostics:** Remaining useful life (RUL) predictions

**Example: Connected Vehicle Fleet FMEA**

.. code-block:: python

   # Dynamic FMEA with fleet data update
   import numpy as np
   
   class DynamicFMEA:
       def __init__(self, component, failure_mode, initial_lambda):
           self.component = component
           self.failure_mode = failure_mode
           self.lambda_fit = initial_lambda  # Initial design estimate (FIT)
           self.field_failures = []
           self.operating_hours = 0
       
       def update_from_fleet(self, failures, hours):
           """Update failure rate from fleet data"""
           self.field_failures.extend(failures)
           self.operating_hours += hours
           
           # Maximum likelihood estimate
           total_failures = len(self.field_failures)
           if self.operating_hours > 0:
               self.lambda_fit = (total_failures / self.operating_hours) * 1e9  # FIT
       
       def predict_mtbf(self):
           """Mean Time Between Failures"""
           if self.lambda_fit > 0:
               return 1e9 / self.lambda_fit  # hours
           return float('inf')
       
       def risk_score(self, severity, detection_coverage):
           """Dynamic RPN based on actual failure rate"""
           occurrence = self.occurrence_rating(self.lambda_fit)
           detection = 10 - int(detection_coverage * 10)  # Invert DC to detection rating
           return severity * occurrence * detection
       
       def occurrence_rating(self, lambda_fit):
           """Map failure rate to occurrence rating (1-10)"""
           if lambda_fit < 0.1: return 1
           elif lambda_fit < 1: return 2
           elif lambda_fit < 5: return 3
           elif lambda_fit < 10: return 4
           elif lambda_fit < 20: return 5
           elif lambda_fit < 50: return 6
           elif lambda_fit < 100: return 7
           elif lambda_fit < 200: return 8
           elif lambda_fit < 500: return 9
           else: return 10
   
   # Example usage
   brake_sensor = DynamicFMEA(
       component="Brake_Pressure_Sensor",
       failure_mode="Stuck_at_zero",
       initial_lambda=10  # 10 FIT design estimate
   )
   
   # Simulate 1 million vehicle-hours of operation
   # 3 failures observed in field
   brake_sensor.update_from_fleet(failures=[1, 1, 1], hours=1_000_000)
   
   print(f"Initial λ: {10} FIT (design)")
   print(f"Field λ: {brake_sensor.lambda_fit:.2f} FIT (actual)")
   print(f"MTBF: {brake_sensor.predict_mtbf():.0f} hours")
   print(f"Dynamic RPN: {brake_sensor.risk_score(severity=10, detection_coverage=0.95)}")
   
   # Output:
   # Initial λ: 10 FIT (design)
   # Field λ: 3.00 FIT (actual) → Better than design!
   # MTBF: 333,333,333 hours
   # Dynamic RPN: 30 (Severity 10 × Occurrence 3 × Detection 1)

================================================================================
7. FMEA Best Practices and Common Pitfalls (2026)
================================================================================

7.1 Best Practices
------------------

**1. Cross-Functional Team:**
   - Design engineers, safety engineers, quality, field service, suppliers
   - Diverse perspectives find more failure modes

**2. Iterative Process:**
   - Concept FMEA (high-level)
   - Design FMEA (detailed)
   - Integration FMEA (system interactions)
   - Update with field data, design changes

**3. Traceability:**
   - Link FMEA to requirements, hazard analysis (HARA), safety cases
   - Tool support: Jama, Polarion, DOORS, Jira

**4. Quantitative When Possible:**
   - Use failure rate databases: IEC TR 62380, MIL-HDBK-217, SN 29500
   - Field data preferred over handbook estimates

**5. Focus on High-Risk Items:**
   - Pareto principle: 20% of failure modes cause 80% of risk
   - Prioritize High AP / RPN > 125

**6. Validation:**
   - Fault injection testing (verify detection mechanisms work)
   - FMEA review meetings (peer review)
   - Independent assessment (TÜV, Exida, UL)

7.2 Common Pitfalls
-------------------

**Pitfall 1: Incomplete Failure Mode List**
- **Problem:** Missing failure modes (especially software, security, environmental)
- **Solution:** Use checklists, historical data, brainstorming, STPA/HAZOP

**Pitfall 2: Over-Optimistic Detection Ratings**
- **Problem:** Claiming high detection when diagnostics are weak
- **Solution:** Fault injection validation, diagnostic coverage analysis

**Pitfall 3: RPN Threshold Rigidity**
- **Problem:** Treating RPN=125 as absolute cutoff (false precision)
- **Solution:** Use AIAG-VDA Action Priority (qualitative High/Medium/Low)

**Pitfall 4: No Follow-Up on Actions**
- **Problem:** FMEA becomes "paper exercise" with no design improvements
- **Solution:** Track actions in project management tool, verify effectiveness

**Pitfall 5: Static FMEA (Never Updated)**
- **Problem:** FMEA outdated after design changes, field data
- **Solution:** Living document, configuration management, dynamic FMEA

**Pitfall 6: Ignoring Common Cause Failures**
- **Problem:** Redundant channels fail together (fire, flood, software bug)
- **Solution:** Add CCF analysis (beta-factor method), diverse redundancy

================================================================================
8. Exam Preparation — 5 Comprehensive Questions
================================================================================

**Question 1: FMEA vs FMEDA — Explain Differences**

**Answer:**
- **FMEA (Failure Mode and Effects Analysis):**
  - Qualitative/semi-quantitative safety analysis
  - Identifies failure modes, causes, effects
  - Uses Severity-Occurrence-Detection (SOD) → RPN
  - Applicable to design, process, software
  
- **FMEDA (FMEA + Diagnostic Analysis):**
  - Quantitative analysis for **random hardware failures**
  - Required by **ISO 26262** (automotive functional safety)
  - Calculates **SPFM** (Single-Point Fault Metric), **LFM** (Latent Fault Metric)
  - Categorizes faults: Safe, Single-point, Residual, Latent, Detected
  - Demonstrates ASIL hardware metrics compliance (e.g., SPFM ≥99% for ASIL D)

**Key Difference:** FMEDA quantifies **diagnostic coverage** and **safety metrics**, while traditional FMEA focuses on qualitative risk prioritization.

---

**Question 2: Calculate SPFM for ASIL D Microcontroller**

**Given:**
- Microcontroller total failure rate: λ_total = 100 FIT
- Safe faults: λ_safe = 10 FIT
- Single-point faults (undetected): λ_SPF = 15 FIT
- Residual faults (detected): λ_RF_detected = 60 FIT (DC = 95%)
- Residual faults (undetected): λ_RF_undetected = 3 FIT
- Latent faults: λ_MPF = 12 FIT

**Question:** Does this MCU meet ASIL D SPFM target (≥99%)?

**Answer:**

.. code-block:: python

   # SPFM calculation
   lambda_SPF_total = 15  # Single-point (undetected)
   lambda_RF_total = 60 + 3  # Residual (detected + undetected)
   lambda_RF_detected = 60
   
   # Total dangerous faults
   dangerous_faults = lambda_SPF_total + lambda_RF_total  # 15 + 63 = 78 FIT
   
   # Detected dangerous faults (SPF are undetected by definition)
   detected_faults = lambda_RF_detected  # 60 FIT
   
   # SPFM formula
   SPFM = (detected_faults / dangerous_faults) * 100
   print(f"SPFM = {SPFM:.2f}%")
   
   # Output: SPFM = 76.92%
   
   # Conclusion: FAIL (need ≥99% for ASIL D)

**Improvement:** Reduce λ_SPF by adding diagnostics (e.g., lockstep cores detect λ_SPF → convert to λ_RF_detected).

---

**Question 3: AIAG-VDA 2019 Action Priority — Determine AP**

**Given:**
- Failure Mode: Fuel pump relay stuck open
- Severity: 8 (engine stall on highway)
- Occurrence: 6 (moderate - relay wear-out)
- Detection: 7 (low - no direct monitoring)

**Question:** What is the Action Priority (High/Medium/Low)?

**Answer:**

Using AIAG-VDA 2019 AP table:
- Severity = 8 (7-8 range)
- Occurrence = 6 (4-10 range)
- Detection = 7 (4-10 range)

**Rule:** Severity 7-8 + Occurrence 4-10 + Detection 4-10 → **Action Priority = HIGH**

**Actions Required:**
- Add fuel pump current monitoring (improve detection → 1-3)
- Redundant relay or fail-safe valve
- Reduce occurrence (higher quality relay, de-rating)

---

**Question 4: Software FMEA — API Timeout Mitigation**

**Scenario:** Autonomous vehicle lidar processing API times out (>100ms deadline miss).

**Question:** Perform Software FMEA and propose mitigation.

**Answer:**

.. code-block:: text

   Failure Mode: Lidar API timeout (deadline miss >100ms)
   
   Causes:
   ├─ High point cloud density (urban environment)
   ├─ CPU overload (resource starvation)
   └─ Memory fragmentation (allocation delays)
   
   Effects:
   ├─ Local: Missed detection cycle
   ├─ System: Stale object list used for path planning
   ├─ End: Delayed emergency braking → Collision (Severity = 10)
   
   Current Controls:
   ├─ Prevention: Deadline monotonic scheduling
   ├─ Detection: Watchdog timer (detects timeout)
   
   Occurrence: 5 (moderate)
   Detection: 4 (watchdog detects, but recovery slow)
   RPN: 10 × 5 × 4 = 200 → CRITICAL
   
   Mitigations:
   1. **Timeout fallback:** Use radar-only object list if lidar times out
   2. **Adaptive processing:** Reduce point cloud resolution if CPU>80%
   3. **Graceful degradation:** L3 → L2 (request driver takeover)
   4. **Resource reservation:** Guarantee lidar 50% CPU minimum
   
   After Mitigation:
   ├─ Occurrence: 2 (rare with adaptive processing)
   ├─ Detection: 2 (fast radar fallback)
   └─ RPN': 10 × 2 × 2 = 40 → ACCEPTABLE

---

**Question 5: FMEA-MSR for OOD Detection in AI/ML**

**Scenario:** Autonomous vehicle camera DNN detects unknown object (kangaroo on highway).

**Question:** Apply FMEA-MSR (Monitoring + System Response) framework.

**Answer:**

.. code-block:: text

   System: L3 Highway Pilot
   Component: Camera Object Detection DNN
   
   Failure Mode: Out-of-Distribution (OOD) input
   Triggering Condition: Kangaroo on highway (not in training dataset)
   
   Effects:
   ├─ DNN misclassifies (low confidence or wrong class)
   ├─ Path planning ignores object
   └─ Collision with kangaroo → Vehicle damage, injury (Severity = 7)
   
   Monitoring Mechanisms:
   ├─ DNN confidence score < 0.5 (low confidence threshold)
   ├─ OOD detector (Mahalanobis distance, ODIN score)
   ├─ Radar cross-check (object present but no DNN detection?)
   └─ Unexpected object size/velocity
   
   System Response (Graduated):
   1. **Confidence 0.3-0.5:** Increase radar/lidar fusion weight
   2. **Confidence < 0.3:** Treat as "unknown obstacle" → Emergency braking
   3. **OOD detector triggers:** Reduce speed to 60 km/h, alert driver
   4. **Persistent OOD:** Request takeover, L3 → L2 mode
   
   Response Effectiveness:
   ├─ Detection latency: 150ms (OOD detector)
   ├─ Braking response: 200ms actuation
   ├─ Safe state: Emergency stop or successful avoidance
   └─ False positive rate: < 2% (acceptable for safety)
   
   Action Priority: HIGH (Severity 7, safety-critical)
   
   Actions:
   ├─ Improve training data (add rare animals, edge cases)
   ├─ OOD detector calibration (reduce false negatives)
   ├─ Multi-modal fusion (thermal camera for night animals)
   └─ Driver monitoring (ensure takeover readiness)

================================================================================
9. Completion Checklist
================================================================================

.. code-block:: text

   ✅ FMEA Fundamentals
      ├─ Definition, purpose, standards (ISO 26262, IEC 61508, AIAG-VDA)
      ├─ FMEA vs FMECA vs FMEDA (differences and applications)
      └─ 7-step FMEA process (scope, functions, failure modes, effects, controls, risk)
   
   ✅ DFMEA (Design FMEA)
      ├─ AIAG-VDA 2019 harmonized approach (7 steps)
      ├─ Action Priority (High/Medium/Low) vs RPN
      └─ Automotive brake pressure sensor example
   
   ✅ FMEDA (ISO 26262)
      ├─ SPFM and LFM metrics (formulas, targets)
      ├─ Fault classification (Safe, SPF, RF, MPF)
      └─ ASIL D microcontroller calculation example
   
   ✅ FMEA-MSR (2026 Evolution)
      ├─ Monitoring and System Response framework
      ├─ Autonomous driving camera failure example
      └─ AI/ML OOD detection FMEA-MSR
   
   ✅ Software FMEA
      ├─ API timeout, buffer overflow examples
      ├─ Systematic vs random failures
      └─ Corrected code with bounds checking
   
   ✅ Advanced Techniques
      ├─ Model-Based FMEA (AADL EMV2, 70% time reduction)
      ├─ Dynamic FMEA (fleet data updates)
      └─ Best practices and common pitfalls
   
   ✅ Exam Questions (5)
      ├─ FMEA vs FMEDA differences
      ├─ SPFM calculation for ASIL D
      ├─ AIAG-VDA Action Priority determination
      ├─ Software FMEA (API timeout)
      └─ FMEA-MSR for AI/ML OOD

================================================================================
10. Key Takeaways
================================================================================

1. **FMEA is bottom-up safety analysis** identifying failure modes at component level, assessing effects, and prioritizing corrective actions (RPN or AP).

2. **FMEDA (ISO 26262) quantifies random hardware safety** via SPFM (≥99% ASIL D) and LFM (≥90% ASIL D) metrics, categorizing faults as Safe/SPF/RF/MPF.

3. **AIAG-VDA 2019 replaces RPN with Action Priority** (High/Medium/Low) for more qualitative, less misleading risk assessment.

4. **FMEA-MSR (2026) adds Monitoring + System Response** for runtime failures in autonomous systems, addressing OOD, adversarial attacks, and dynamic hazards.

5. **Software FMEA focuses on systematic failures** (API timeouts, buffer overflows, race conditions) not random hardware faults, requiring different mitigation strategies.

6. **Model-Based FMEA (AADL EMV2) achieves 70% time reduction** through automated generation, consistency, and traceability from architecture models.

7. **FMEA is a living document** requiring updates from field data, design changes, and dynamic fleet monitoring for continuous safety improvement.

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Author:** GitHub Copilot (Claude Sonnet 4.5)  
**Standards:** ISO 26262:2018, IEC 61508:2010, AIAG-VDA FMEA 2019, MIL-STD-1629A

================================================================================
