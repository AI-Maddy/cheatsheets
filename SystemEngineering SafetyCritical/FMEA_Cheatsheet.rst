🔍 **FMEA — Failure Modes and Effects Analysis**
═══════════════════════════════════════════════════════════════════

**Full Name:** Failure Modes and Effects Analysis (FMEA) / Failure Modes, Effects and Criticality Analysis (FMECA)  
**Type:** Bottom-up inductive safety analysis technique  
**Origin:** US Military (MIL-STD-1629, 1949), Aerospace, Automotive  
**Standards:** IEC 60812, SAE J1739, ISO 26262, VDA (German Automotive)

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — FMEA IN 60 SECONDS**
─────────────────────────────────

**What is FMEA?**

::

    FMEA = Systematic analysis starting from component failures
    
    Question: "What can go wrong with each component?"
    
    Process:
    1. Identify component
    2. List failure modes
    3. Analyze effects on system
    4. Calculate criticality (RPN)
    5. Implement mitigation actions

**Types of FMEA:**

+------------------+--------------------------------+----------------------------+
| **Type**         | **Focus**                      | **When Used**              |
+==================+================================+============================+
| **Design FMEA**  | Product design failures        | Design phase               |
| (DFMEA)          | Hardware/software components   |                            |
+------------------+--------------------------------+----------------------------+
| **Process FMEA** | Manufacturing process failures | Production planning        |
| (PFMEA)          | Assembly, testing, handling    |                            |
+------------------+--------------------------------+----------------------------+
| **System FMEA**  | System-level interactions      | System architecture        |
| (SFMEA)          | Subsystem interfaces           |                            |
+------------------+--------------------------------+----------------------------+

**RPN Formula (Risk Priority Number):**

::

    RPN = Severity × Occurrence × Detection
    
    Severity (S):    1-10 (1 = no effect, 10 = hazardous)
    Occurrence (O):  1-10 (1 = unlikely, 10 = almost certain)
    Detection (D):   1-10 (1 = certain detect, 10 = cannot detect)
    
    RPN Range: 1 to 1000
    
    Action Priority:
    - RPN ≥ 200 → Immediate action required
    - RPN 100-199 → Action recommended
    - RPN < 100 → Monitor

════════════════════════════════════════════════════════════════════

📖 **1. FMEA FUNDAMENTALS**
═══════════════════════════

**1.1 Definition & Purpose**
----------------------------

**FMEA:**

- **Systematic**: Structured, repeatable process
- **Bottom-up**: Starts with component-level failures
- **Inductive**: Reasons from specific failures to system effects
- **Preventive**: Identifies issues before they occur
- **Documented**: Creates traceability for certification

**Objectives:**

✅ Identify potential failure modes  
✅ Assess severity of consequences  
✅ Determine failure likelihood  
✅ Evaluate detection capability  
✅ Prioritize mitigation actions  
✅ Track risk reduction over time

**1.2 FMEA vs FMECA**
---------------------

**FMEA (Failure Modes and Effects Analysis):**

- Qualitative analysis
- Identifies failures + effects
- No criticality ranking (originally)

**FMECA (Failure Modes, Effects and Criticality Analysis):**

- FMEA + Criticality ranking
- Quantitative RPN calculation
- Prioritizes actions by risk level

**Modern Practice:** Most industries use FMECA but call it FMEA (criticality is standard now).

**1.3 When to Use FMEA**
------------------------

**Ideal for:**

✅ Hardware-dominated systems (mechanical, electrical)  
✅ Component-level analysis  
✅ Known failure modes (historical data)  
✅ Serial failure propagation  
✅ Single point failures

**Not ideal for:**

❌ Software-dominated systems (use SFMEA or STPA)  
❌ Complex interactions (use FTA)  
❌ Human error analysis (use HAZOP)  
❌ Systematic failures (use STPA)

════════════════════════════════════════════════════════════════════

📖 **2. FMEA PROCESS (7 STEPS)**
════════════════════════════════

**2.1 Step 1: Define Scope**
----------------------------

**Boundary Definition:**

.. code-block:: text

    System: Electric Power Steering (EPS) System
    Subsystems:
    - Steering column with angle sensor
    - Electric motor
    - Electronic Control Unit (ECU)
    - Power supply (12V battery)
    - Torque sensor
    
    Scope: Design FMEA (DFMEA)
    Phase: Development (before production)
    ASIL Level: ASIL C (per ISO 26262 hazard analysis)

**Team Composition:**

- **FMEA Lead**: Facilitates sessions, ensures methodology
- **Design Engineer**: Component expertise
- **Safety Engineer**: ASIL/SIL requirements
- **Test Engineer**: Detection methods
- **Supplier Rep**: Component failure data (if applicable)

**2.2 Step 2: Functional Analysis**
-----------------------------------

**Function Decomposition:**

::

    Electric Power Steering (EPS) — Functions:
    
    F1: Sense driver steering input
        ├─ F1.1: Measure steering wheel angle
        └─ F1.2: Measure steering torque
    
    F2: Calculate assist torque
        ├─ F2.1: Read vehicle speed
        ├─ F2.2: Compute assist level
        └─ F2.3: Generate motor command
    
    F3: Apply assist torque
        ├─ F3.1: Drive motor (PWM)
        └─ F3.2: Monitor motor current
    
    F4: Safety monitoring
        ├─ F4.1: Plausibility checks
        ├─ F4.2: Redundant sensing
        └─ F4.3: Fail-safe transition

**2.3 Step 3: Identify Failure Modes**
--------------------------------------

**Failure Mode Categories:**

+------------------+----------------------------------+----------------------------+
| **Category**     | **Examples**                     | **Typical Components**     |
+==================+==================================+============================+
| **Mechanical**   | Fracture, wear, deformation      | Gears, shafts, bearings    |
+------------------+----------------------------------+----------------------------+
| **Electrical**   | Open circuit, short circuit      | Wires, connectors, PCB     |
+------------------+----------------------------------+----------------------------+
| **Electronic**   | Stuck-at, bit flip, latch-up     | ICs, sensors, actuators    |
+------------------+----------------------------------+----------------------------+
| **Software**     | Incorrect calculation, timeout   | ECU firmware, algorithms   |
+------------------+----------------------------------+----------------------------+

**Example: Torque Sensor Failure Modes**

.. code-block:: text

    Component: Torque Sensor (strain gauge type)
    Function: Measure driver steering torque (±10 Nm)
    
    Failure Modes:
    1. No output (open circuit)
    2. Stuck at zero (sensor failure)
    3. Stuck at max (sensor failure)
    4. Noisy output (intermittent)
    5. Drift over time (calibration loss)
    6. Out-of-range (mechanical damage)

**2.4 Step 4: Analyze Effects**
-------------------------------

**Effect Levels:**

::

    Local Effect → Next Higher Level → End Effect (System/Vehicle)
    
    Example: Torque Sensor Stuck at Zero
    
    Local Effect:
    - ECU receives 0 Nm torque reading
    
    Next Higher Level:
    - EPS calculates maximum assist (no driver input detected)
    - Motor applies full torque
    
    End Effect (Vehicle):
    - Unexpected steering assist
    - Driver loses control
    - Potential accident (ASIL C hazard)

**2.5 Step 5: Rate Severity (S)**
---------------------------------

**Severity Scale (ISO 26262 / SAE J1739):**

+-------+-------------------+----------------------------------+------------------+
| **S** | **Classification**| **Description**                  | **ASIL**         |
+=======+===================+==================================+==================+
| **10**| Hazardous         | Life-threatening without warning | **ASIL D**       |
+-------+-------------------+----------------------------------+------------------+
| **9** | Hazardous         | Life-threatening with warning    | **ASIL C**       |
+-------+-------------------+----------------------------------+------------------+
| **8** | Very High         | Severe injury, vehicle damage    | **ASIL B**       |
+-------+-------------------+----------------------------------+------------------+
| **7** | High              | Injury, significant damage       | **ASIL A**       |
+-------+-------------------+----------------------------------+------------------+
| **6** | Moderate          | Minor injury, moderate damage    | QM               |
+-------+-------------------+----------------------------------+------------------+
| **5** | Low               | Inconvenience, minor damage      | QM               |
+-------+-------------------+----------------------------------+------------------+
| **4** | Very Low          | Noticeable, no damage            | QM               |
+-------+-------------------+----------------------------------+------------------+
| **3** | Minor             | Barely noticeable                | QM               |
+-------+-------------------+----------------------------------+------------------+
| **2** | Very Minor        | Most customers won't notice      | QM               |
+-------+-------------------+----------------------------------+------------------+
| **1** | None              | No effect                        | QM               |
+-------+-------------------+----------------------------------+------------------+

**Example Rating:**

    Torque Sensor Stuck at Zero → Severity = 9
    (Hazardous: Unexpected steering assist, life-threatening with warning)

**2.6 Step 6: Rate Occurrence (O)**
-----------------------------------

**Occurrence Scale (Failure Rate):**

+-------+-------------------+----------------------------------+-------------------+
| **O** | **Likelihood**    | **Failure Rate (per vehicle)**   | **PPM**           |
+=======+===================+==================================+===================+
| **10**| Almost Certain    | ≥ 1 in 2                         | ≥ 500,000         |
+-------+-------------------+----------------------------------+-------------------+
| **9** | Very High         | 1 in 3                           | 333,333           |
+-------+-------------------+----------------------------------+-------------------+
| **8** | High              | 1 in 8                           | 125,000           |
+-------+-------------------+----------------------------------+-------------------+
| **7** | Moderate High     | 1 in 20                          | 50,000            |
+-------+-------------------+----------------------------------+-------------------+
| **6** | Moderate          | 1 in 80                          | 12,500            |
+-------+-------------------+----------------------------------+-------------------+
| **5** | Low               | 1 in 400                         | 2,500             |
+-------+-------------------+----------------------------------+-------------------+
| **4** | Very Low          | 1 in 2,000                       | 500               |
+-------+-------------------+----------------------------------+-------------------+
| **3** | Remote            | 1 in 15,000                      | 67                |
+-------+-------------------+----------------------------------+-------------------+
| **2** | Very Remote       | 1 in 150,000                     | 6.7               |
+-------+-------------------+----------------------------------+-------------------+
| **1** | Nearly Impossible | < 1 in 1,500,000                 | < 0.67            |
+-------+-------------------+----------------------------------+-------------------+

**Data Sources for Occurrence:**

✅ Historical field data (warranty claims)  
✅ Supplier reliability data (MTBF)  
✅ Industry databases (IEC 61709, MIL-HDBK-217)  
✅ Test data (accelerated life testing)  
✅ Expert judgment (if no data available)

**Example Rating:**

    Torque Sensor Stuck at Zero → Occurrence = 3
    (Remote: 67 PPM based on supplier data, proven design)

**2.7 Step 7: Rate Detection (D)**
----------------------------------

**Detection Scale (Likelihood of Detection Before Customer):**

+-------+-------------------+----------------------------------+
| **D** | **Detection**     | **Description**                  |
+=======+===================+==================================+
| **10**| Almost Impossible | No detection method exists       |
+-------+-------------------+----------------------------------+
| **9** | Very Remote       | Detection unlikely (manual only) |
+-------+-------------------+----------------------------------+
| **8** | Remote            | Detection possible (manual)      |
+-------+-------------------+----------------------------------+
| **7** | Very Low          | Some detection (manual + auto)   |
+-------+-------------------+----------------------------------+
| **6** | Low               | Moderate detection (automated)   |
+-------+-------------------+----------------------------------+
| **5** | Moderate          | Good detection (multiple checks) |
+-------+-------------------+----------------------------------+
| **4** | Moderately High   | High detection (redundant)       |
+-------+-------------------+----------------------------------+
| **3** | High              | Very high detection (fail-safe)  |
+-------+-------------------+----------------------------------+
| **2** | Very High         | Almost certain detection         |
+-------+-------------------+----------------------------------+
| **1** | Almost Certain    | Certain detection (design out)   |
+-------+-------------------+----------------------------------+

**Detection Methods:**

- **Design controls**: Redundancy, plausibility checks, diagnostics
- **Process controls**: Inspection, testing (EOL, HIL)
- **Field controls**: OBD diagnostics, customer feedback

**Example Rating:**

    Torque Sensor Stuck at Zero → Detection = 2
    (Very High: Redundant sensor + plausibility check catches fault)

════════════════════════════════════════════════════════════════════

📖 **3. RPN CALCULATION & PRIORITIZATION**
══════════════════════════════════════════

**3.1 RPN Formula**
-------------------

**Risk Priority Number (RPN):**

.. code-block:: text

    RPN = Severity (S) × Occurrence (O) × Detection (D)
    
    Range: 1 to 1,000
    
    Example: Torque Sensor Stuck at Zero
    - Severity (S) = 9 (hazardous with warning)
    - Occurrence (O) = 3 (remote, 67 PPM)
    - Detection (D) = 2 (very high detection)
    
    RPN = 9 × 3 × 2 = 54

**3.2 Action Priority**
-----------------------

**Thresholds (Industry Standard):**

+-------------------+------------------+--------------------------------+
| **RPN Range**     | **Priority**     | **Action Required**            |
+===================+==================+================================+
| **RPN ≥ 200**     | **Critical**     | Immediate action mandatory     |
+-------------------+------------------+--------------------------------+
| **RPN 100-199**   | **High**         | Action strongly recommended    |
+-------------------+------------------+--------------------------------+
| **RPN 50-99**     | **Medium**       | Action if cost-effective       |
+-------------------+------------------+--------------------------------+
| **RPN < 50**      | **Low**          | Monitor, no action required    |
+-------------------+------------------+--------------------------------+

**ISO 26262 Overrides:**

::

    Special Rule: If Severity ≥ 8 (ASIL B-D), action required even if RPN < 50
    
    Reason: Safety-critical failures cannot be ignored regardless of RPN

**3.3 Mitigation Strategies**
-----------------------------

**Reduce Severity (S):**

- **Fail-safe design**: Safe state on failure
- **Redundancy**: Backup components
- **Error containment**: Limit fault propagation

**Reduce Occurrence (O):**

- **Robust design**: Derating, margin
- **Better components**: Higher quality, proven-in-use
- **Stress testing**: Accelerated life testing

**Improve Detection (D):**

- **Diagnostics**: Built-in self-test (BIST)
- **Redundancy**: Dual sensors with voting
- **Plausibility checks**: Range, rate-of-change limits

**Example Mitigation:**

.. code-block:: text

    Original Design:
    - Single torque sensor
    - RPN = 9 × 6 × 8 = 432 (CRITICAL!)
    
    Mitigation 1: Add redundant sensor (reduce O)
    - Dual sensors with voting
    - RPN = 9 × 3 × 8 = 216 (still HIGH)
    
    Mitigation 2: Add plausibility check (improve D)
    - Compare torque vs. angle sensors
    - RPN = 9 × 3 × 2 = 54 (ACCEPTABLE ✅)

════════════════════════════════════════════════════════════════════

📖 **4. FMEA TABLE EXAMPLE**
════════════════════════════

**4.1 Standard FMEA Format**
----------------------------

**Automotive Example: Electric Power Steering (EPS)**

.. code-block:: text

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DESIGN FMEA (DFMEA) — Electric Power Steering System
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Item: EPS ECU | ASIL Level: ASIL C | FMEA Date: 2026-01-14 | Team: Safety/Design/Test
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ┌──────────┬────────────┬──────────────┬────────────────┬────┬────┬────┬─────┬────────────┬────────────┐
    │ Component│ Function   │ Failure Mode │ Failure Effect │ S  │ O  │ D  │ RPN │ Current    │ Action     │
    │          │            │              │                │    │    │    │     │ Controls   │ Required   │
    ├──────────┼────────────┼──────────────┼────────────────┼────┼────┼────┼─────┼────────────┼────────────┤
    │ Torque   │ Measure    │ Stuck at     │ ECU applies    │ 9  │ 6  │ 8  │ 432 │ None       │ YES ✅     │
    │ Sensor   │ steering   │ zero         │ full assist    │    │    │    │     │            │ Add        │
    │          │ torque     │              │ → Loss of      │    │    │    │     │            │ redundant  │
    │          │            │              │ control        │    │    │    │     │            │ sensor     │
    ├──────────┼────────────┼──────────────┼────────────────┼────┼────┼────┼─────┼────────────┼────────────┤
    │ Torque   │ Measure    │ Stuck at     │ ECU applies    │ 9  │ 3  │ 2  │ 54  │ Redundant  │ NO ✅      │
    │ Sensor   │ steering   │ zero         │ full assist    │    │    │    │     │ sensor +   │ Acceptable │
    │ (REVISED)│ torque     │              │ → DETECTED     │    │    │    │     │ plausibility│            │
    ├──────────┼────────────┼──────────────┼────────────────┼────┼────┼────┼─────┼────────────┼────────────┤
    │ Motor    │ Apply      │ Stuck at     │ No steering    │ 8  │ 4  │ 3  │ 96  │ Current    │ YES ✅     │
    │          │ assist     │ full power   │ assist →       │    │    │    │     │ monitoring │ Add H-     │
    │          │ torque     │              │ Heavy steering │    │    │    │     │            │ bridge     │
    │          │            │              │                │    │    │    │     │            │ failsafe   │
    ├──────────┼────────────┼──────────────┼────────────────┼────┼────┼────┼─────┼────────────┼────────────┤
    │ Power    │ Supply     │ Loss of      │ EPS shutdown   │ 7  │ 3  │ 2  │ 42  │ Battery    │ NO ✅      │
    │ Supply   │ 12V to ECU │ power (12V)  │ → Manual       │    │    │    │     │ monitoring │ Acceptable │
    │          │            │              │ steering only  │    │    │    │     │ + warning  │            │
    ├──────────┼────────────┼──────────────┼────────────────┼────┼────┼────┼─────┼────────────┼────────────┤
    │ Angle    │ Measure    │ Noisy signal │ Erratic assist │ 6  │ 5  │ 4  │ 120 │ Signal     │ YES ✅     │
    │ Sensor   │ steering   │ (EMI)        │ → Driver       │    │    │    │     │ filtering  │ Add        │
    │          │ wheel      │              │ discomfort     │    │    │    │     │            │ shielding  │
    │          │ angle      │              │                │    │    │    │     │            │            │
    └──────────┴────────────┴──────────────┴────────────────┴────┴────┴────┴─────┴────────────┴────────────┘
    
    Summary:
    - Total Failure Modes Analyzed: 15
    - Critical (RPN ≥ 200): 1 → Action: Add redundant torque sensor
    - High (RPN 100-199): 2 → Action: H-bridge failsafe, EMI shielding
    - Acceptable (RPN < 100): 12 → Monitor

════════════════════════════════════════════════════════════════════

📖 **5. FMEA IN DIFFERENT DOMAINS**
═══════════════════════════════════

**5.1 Automotive (ISO 26262)**
------------------------------

**ASIL-Driven FMEA:**

.. code-block:: text

    ISO 26262 Requirements:
    - DFMEA mandatory for ASIL A-D components
    - RPN thresholds stricter for higher ASIL
    - Action required if:
      * Severity ≥ 8 (ASIL B-D) regardless of RPN
      * RPN ≥ 100 for ASIL C-D
      * RPN ≥ 200 for ASIL A-B
    
    Integration with HARA:
    - Hazard Analysis and Risk Assessment (HARA) defines ASIL
    - FMEA ensures design meets ASIL requirements
    - Safety mechanisms reduce RPN to acceptable level

**Automotive FMEA Types:**

1. **System FMEA (SFMEA)**: Vehicle-level interactions
2. **Design FMEA (DFMEA)**: Component hardware/software
3. **Process FMEA (PFMEA)**: Manufacturing/assembly

**5.2 Aerospace (ARP4754A / DO-178C)**
--------------------------------------

**Functional Hazard Assessment (FHA) Integration:**

.. code-block:: text

    Aerospace Term: FHA (Functional Hazard Assessment)
    Equivalent to: FMEA + preliminary hazard analysis
    
    DAL Assignment:
    - Catastrophic (DAL A): Like ASIL D
    - Hazardous (DAL B): Like ASIL C
    - Major (DAL C): Like ASIL B
    - Minor (DAL D): Like ASIL A
    - No Safety Effect (DAL E): Like QM
    
    Key Difference:
    - Aviation: Qualitative FHA first, then quantitative FTA
    - Automotive: FMEA more central to process

**5.3 Medical Devices (IEC 62304)**
-----------------------------------

**Risk Management (ISO 14971):**

.. code-block:: text

    Medical Device FMEA:
    - Called "Risk Analysis" (ISO 14971 terminology)
    - Focus on patient harm (not just device failure)
    - Regulatory requirement (FDA, EU MDR)
    
    Severity Ratings:
    - Catastrophic: Death
    - Critical: Permanent impairment
    - Serious: Temporary impairment
    - Minor: Inconvenience
    - Negligible: No harm
    
    Special Considerations:
    - Use error (human factors)
    - Cybersecurity risks (medical IoT)
    - Long-term implants (wear-out failures)

**5.4 Industrial (IEC 61508)**
------------------------------

**Process Industry FMEA:**

.. code-block:: text

    SIL-Based FMEA:
    - Typically combined with HAZOP for process systems
    - FMEA for hardware (instruments, actuators)
    - HAZOP for process deviations (temperature, pressure)
    
    Quantitative Focus:
    - PFD (Probability of Failure on Demand) calculation
    - λ (failure rate) per component
    - SFF (Safe Failure Fraction) for SIL verification

════════════════════════════════════════════════════════════════════

📖 **6. SOFTWARE FMEA (SFMEA)**
═══════════════════════════════

**6.1 Challenges with Software FMEA**
-------------------------------------

**Why Software FMEA is Different:**

❌ **No wear-out**: Software doesn't degrade over time  
❌ **No random failures**: Failures are systematic (bugs)  
❌ **Occurrence hard to quantify**: How often does bug X trigger?  
❌ **Complex state space**: Millions of possible states

**Better Alternatives for Software:**

✅ **STPA** (Systems-Theoretic Process Analysis): Control structure  
✅ **FTA** (Fault Tree Analysis): Logic-based deduction  
✅ **Formal methods**: Mathematical proof of correctness

**6.2 When Software FMEA Makes Sense**
--------------------------------------

**Appropriate Use Cases:**

✅ Software-hardware interface failures  
✅ Data corruption (bit flips, overflow)  
✅ Timing failures (watchdog timeout)  
✅ Resource exhaustion (memory, CPU)

**Example: ECU Software FMEA**

.. code-block:: text

    Component: Motor Control Algorithm (C code)
    Function: Calculate PWM duty cycle for motor
    
    Failure Modes:
    1. Integer overflow (duty cycle > 100%)
       → Effect: Motor over-voltage → Damage
       → S=8, O=4 (code review finds it), D=6 → RPN=192
       → Action: Add saturation check
    
    2. Divide by zero (speed = 0 in denominator)
       → Effect: CPU exception → ECU reset → Loss of assist
       → S=7, O=3 (edge case), D=2 (exception handler) → RPN=42
       → Action: Add zero check (defensive programming)
    
    3. Watchdog timeout (infinite loop)
       → Effect: ECU reset → Temporary loss of assist
       → S=6, O=2 (unit tested), D=1 (watchdog catches) → RPN=12
       → Action: None (watchdog sufficient)

════════════════════════════════════════════════════════════════════

📖 **7. FMEA TOOLS & AUTOMATION**
═════════════════════════════════

**7.1 Commercial FMEA Tools**
-----------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Key Features**           |
+======================+==================+============================+
| **APIS IQ-FMEA**     | APIS Informations| Automotive (VDA), ISO 26262|
|                      | technologien     | integration                |
+----------------------+------------------+----------------------------+
| **ReliaSoft XFMEA**  | HBK (ReliaSoft)  | Reliability prediction,    |
|                      |                  | FRACAS integration         |
+----------------------+------------------+----------------------------+
| **Relyence FMEA**    | Relyence Corp    | Cloud-based, real-time     |
|                      |                  | collaboration              |
+----------------------+------------------+----------------------------+
| **PTC Windchill**    | PTC              | PLM integration, change    |
|                      |                  | management                 |
+----------------------+------------------+----------------------------+
| **Sphera FMEA**      | Sphera           | Enterprise risk management,|
|                      |                  | compliance tracking        |
+----------------------+------------------+----------------------------+

**7.2 FMEA Template (Excel/CSV)**
---------------------------------

**Minimum Required Columns:**

.. code-block:: python

    # fmea_template.py
    
    import pandas as pd
    
    # Create FMEA template
    fmea_columns = [
        'Item_ID',              # Unique identifier
        'Component',            # Hardware/software component
        'Function',             # What it does
        'Failure_Mode',         # How it fails
        'Failure_Effect_Local', # Effect on component
        'Failure_Effect_System',# Effect on system
        'Severity',             # S (1-10)
        'Failure_Cause',        # Root cause
        'Occurrence',           # O (1-10)
        'Current_Controls',     # Existing mitigations
        'Detection',            # D (1-10)
        'RPN',                  # S × O × D
        'Recommended_Action',   # Mitigation plan
        'Responsibility',       # Who owns action
        'Target_Date',          # When complete
        'Action_Taken',         # What was done
        'Severity_New',         # S after mitigation
        'Occurrence_New',       # O after mitigation
        'Detection_New',        # D after mitigation
        'RPN_New'               # New RPN
    ]
    
    fmea_df = pd.DataFrame(columns=fmea_columns)
    fmea_df.to_csv('FMEA_Template.csv', index=False)
    
    print("✅ FMEA template created: FMEA_Template.csv")

**7.3 Automated RPN Tracking**
------------------------------

**Python Script for RPN Analysis:**

.. code-block:: python

    # fmea_analysis.py
    
    import pandas as pd
    import matplotlib.pyplot as plt
    
    def analyze_fmea(fmea_file):
        """
        Analyze FMEA and generate reports
        """
        
        # Load FMEA data
        df = pd.read_csv(fmea_file)
        
        # Calculate RPN
        df['RPN'] = df['Severity'] * df['Occurrence'] * df['Detection']
        
        # Categorize priority
        def categorize_priority(rpn, severity):
            if rpn >= 200:
                return 'CRITICAL'
            elif rpn >= 100:
                return 'HIGH'
            elif severity >= 8:  # ISO 26262 override
                return 'HIGH (Safety)'
            elif rpn >= 50:
                return 'MEDIUM'
            else:
                return 'LOW'
        
        df['Priority'] = df.apply(
            lambda row: categorize_priority(row['RPN'], row['Severity']), 
            axis=1
        )
        
        # Summary statistics
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("FMEA SUMMARY REPORT")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Total Failure Modes: {len(df)}")
        print(f"\nPriority Breakdown:")
        print(df['Priority'].value_counts())
        print(f"\nHighest RPN: {df['RPN'].max()}")
        print(f"Average RPN: {df['RPN'].mean():.1f}")
        print(f"Median RPN: {df['RPN'].median():.1f}")
        
        # Pareto chart (80/20 rule)
        df_sorted = df.sort_values('RPN', ascending=False)
        df_sorted['Cumulative_Percent'] = (
            df_sorted['RPN'].cumsum() / df_sorted['RPN'].sum() * 100
        )
        
        # Plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.bar(range(len(df_sorted)), df_sorted['RPN'], color='steelblue')
        ax1.set_xlabel('Failure Modes (sorted by RPN)')
        ax1.set_ylabel('RPN', color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')
        
        ax2 = ax1.twinx()
        ax2.plot(range(len(df_sorted)), df_sorted['Cumulative_Percent'], 
                 color='red', marker='o', linewidth=2)
        ax2.set_ylabel('Cumulative %', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.axhline(y=80, color='red', linestyle='--', label='80% line')
        
        plt.title('FMEA Pareto Chart (Focus on Top Contributors)')
        plt.tight_layout()
        plt.savefig('FMEA_Pareto.png', dpi=300)
        print("\n✅ Pareto chart saved: FMEA_Pareto.png")
        
        return df
    
    # Example usage
    if __name__ == "__main__":
        df = analyze_fmea('EPS_FMEA.csv')

════════════════════════════════════════════════════════════════════

📖 **8. FMEA BEST PRACTICES**
═════════════════════════════

**8.1 Team Dynamics**
---------------------

**Successful FMEA Teams:**

✅ **Cross-functional**: Design, safety, test, manufacturing  
✅ **Senior participation**: Experience with failure modes critical  
✅ **Facilitated**: Dedicated FMEA lead keeps process on track  
✅ **Time-boxed**: 2-3 hour sessions (avoid fatigue)  
✅ **Iterative**: Multiple sessions as design evolves

**8.2 Common Pitfalls**
-----------------------

❌ **Too late**: FMEA after design frozen (no time for changes)  
❌ **Too generic**: "Component fails" (not specific enough)  
❌ **Severity bias**: Everything rated 9-10 (loses meaning)  
❌ **Action fatigue**: Too many RPN >200 (unrealistic)  
❌ **One-and-done**: FMEA not updated as design changes

**8.3 FMEA Maturity Levels**
----------------------------

+-------+------------------+----------------------------------+
| Level | Maturity         | Characteristics                  |
+=======+==================+==================================+
| **1** | Ad-hoc           | No standard process, reactive    |
+-------+------------------+----------------------------------+
| **2** | Documented       | Templates exist, used sometimes  |
+-------+------------------+----------------------------------+
| **3** | Standardized     | Mandatory, consistent ratings    |
+-------+------------------+----------------------------------+
| **4** | Quantitative     | Historical data, RPN tracking    |
+-------+------------------+----------------------------------+
| **5** | Optimized        | Continuous improvement, lessons  |
|       |                  | learned database                 |
+-------+------------------+----------------------------------+

════════════════════════════════════════════════════════════════════

📝 **9. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between FMEA and FTA?

**A1:**

- **FMEA**: Bottom-up, starts with component failures, inductive
  - Question: "What can go wrong?"
- **FTA**: Top-down, starts with hazardous event, deductive
  - Question: "Why did it happen?"
- **When to use**: FMEA for design phase, FTA for accident investigation

────────────────────────────────────────────────────────────────────

**Q2:** Calculate RPN: Severity=8, Occurrence=5, Detection=4. Is action required?

**A2:**

::

    RPN = 8 × 5 × 4 = 160
    
    Priority: HIGH (RPN 100-199)
    Action: Strongly recommended
    
    Additional: Severity ≥8 (ASIL B) → Action required per ISO 26262

────────────────────────────────────────────────────────────────────

**Q3:** Why is Software FMEA challenging?

**A3:**

- No random failures (only systematic bugs)
- No wear-out mechanism
- Occurrence hard to quantify (no failure rate data)
- Better alternatives: STPA, FTA, formal methods

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Define FMEA scope (system boundaries, ASIL/SIL level)
- [ ] Assemble cross-functional team (design, safety, test)
- [ ] Decompose system into functions and components
- [ ] Identify failure modes (mechanical, electrical, software)
- [ ] Analyze effects at local, system, and end-user levels
- [ ] Rate Severity (1-10, consider ASIL/DAL)
- [ ] Rate Occurrence (1-10, use historical data if available)
- [ ] Rate Detection (1-10, existing controls)
- [ ] Calculate RPN (S × O × D)
- [ ] Prioritize actions (RPN ≥ 200 critical, ≥ 100 high)
- [ ] Implement mitigations (design, process, or detection improvements)
- [ ] Re-calculate RPN after actions
- [ ] Document in FMEA table (traceability for certification)
- [ ] Review FMEA with stakeholders (safety, management, customer)
- [ ] Update FMEA as design evolves (living document)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **FMEA is bottom-up** → Starts with component failures, analyzes system effects

2️⃣ **RPN = S × O × D** → Risk Priority Number guides action prioritization  
(Severity × Occurrence × Detection, range 1-1000)

3️⃣ **Action thresholds** → RPN ≥200 critical, ≥100 high, but Severity ≥8 always 
requires action (ISO 26262)

4️⃣ **Three types** → Design FMEA (hardware/software), Process FMEA (manufacturing), 
System FMEA (interactions)

5️⃣ **Mitigation strategies** → Reduce Severity (fail-safe), reduce Occurrence 
(better components), improve Detection (diagnostics)

6️⃣ **Software FMEA limited** → Better: STPA, FTA, formal methods (no random 
failures in software)

7️⃣ **Living document** → Update FMEA as design evolves, track RPN reduction over time

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **FMEA CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Definition, 7-step process, RPN calculation, domain-specific applications  
(automotive, aerospace, medical, industrial), software FMEA, tools, best practices

════════════════════════════════════════════════════════════════════
