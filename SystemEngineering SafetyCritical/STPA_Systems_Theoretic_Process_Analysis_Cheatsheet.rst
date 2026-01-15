🎯 **STPA — Systems-Theoretic Process Analysis**
═══════════════════════════════════════════════════════════════════

**Full Name:** Systems-Theoretic Process Analysis (STPA)  
**Type:** Modern hazard analysis based on systems theory  
**Origin:** Prof. Nancy Leveson, MIT, 2004  
**Theory:** STAMP (System-Theoretic Accident Model and Processes)  
**Standards:** NASA, FAA, automotive industry adoption

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — STPA IN 60 SECONDS**
─────────────────────────────────

**What is STPA?**

::

    STPA = Hazard analysis based on control theory (not component failure)
    
    Core Insight:
    Accidents occur due to inadequate control, not just failures
    
    Process:
    1. Define losses (accidents to prevent)
    2. Define hazards (system states leading to losses)
    3. Map control structure (controllers, processes, feedback)
    4. Identify Unsafe Control Actions (UCA):
       - Provided when unsafe
       - Not provided when needed
       - Provided too early/late
       - Stopped too soon/applied too long
    5. Identify loss scenarios (causal factors)
    6. Recommend safety constraints

**Why STPA? (Advantages over FMEA/FTA)**

✅ **Software-intensive systems**: Analyzes logic errors, not just hardware  
✅ **Complex interactions**: Captures emergent behavior  
✅ **Human factors**: Treats operators as controllers  
✅ **Design phase**: Early hazard identification  
✅ **Modern systems**: Autonomous vehicles, AI, distributed systems

**STAMP Theory Foundation:**

::

    Traditional View:          STAMP View:
    Accidents = Chain          Accidents = Inadequate
                of failures               control
    
    Focus: Reliability        Focus: Control structure
    (prevent failures)        (enforce constraints)

**Unsafe Control Actions (UCA) — 4 Types:**

+------------------------+--------------------------------------------+
| **UCA Type**           | **Description**                            |
+========================+============================================+
| **1. Provided**        | Control action provided causes hazard      |
| **(unsafe)**           | Example: Throttle opens at max speed       |
+------------------------+--------------------------------------------+
| **2. Not Provided**    | Control action NOT provided causes hazard  |
| **(when needed)**      | Example: Brakes NOT applied before crash   |
+------------------------+--------------------------------------------+
| **3. Too Early/Late**  | Control action timing wrong causes hazard  |
| **or Wrong Order**     | Example: Airbag deploys 5 sec after crash  |
+------------------------+--------------------------------------------+
| **4. Stopped Too**     | Control action duration wrong              |
| **Soon / Applied**     | Example: Brakes released too early         |
| **Too Long**           |                                            |
+------------------------+--------------------------------------------+

════════════════════════════════════════════════════════════════════

📖 **1. STAMP THEORY FUNDAMENTALS**
═══════════════════════════════════

**1.1 STAMP vs Traditional Safety Models**
------------------------------------------

**Traditional Causality Chain Model:**

.. code-block:: text

    Swiss Cheese Model (Reason, 1990):
    
    [Hazard] → [Failure 1] → [Failure 2] → [Failure 3] → [Accident]
              (hole 1)      (hole 2)      (hole 3)
    
    Assumptions:
    - Linear causation
    - Component failures
    - Barriers prevent accidents
    
    Limitations:
    ❌ Software has no "failures" (only logic errors)
    ❌ Complex interactions not captured
    ❌ Emergent behavior ignored
    ❌ Human "error" oversimplified

**STAMP (Systems-Theoretic Accident Model):**

.. code-block:: text

    STAMP View:
    
    Accidents occur when:
    1. Safety constraints violated
    2. Control structure inadequate
    3. Controllers lack correct process model
    
    Focus:
    ✅ Control loops (controller → process → feedback)
    ✅ Mental models (what controller believes vs reality)
    ✅ Emergent behavior (system-level properties)
    ✅ Adaptive systems (learning, AI)

**1.2 Key STAMP Concepts**
--------------------------

**Safety Constraints:**

    Rules that must be enforced to prevent hazards
    
    Example (Automotive):
    - SC-1: Vehicle speed shall not exceed safe speed for conditions
    - SC-2: Brakes shall be applied when collision imminent
    - SC-3: Airbag shall deploy only during actual collision

**Control Structure:**

.. code-block:: text

    Controller (makes decisions)
           │
           ├── Control Actions (commands) ──→ Controlled Process
           │                                       │
           └────────── Feedback (sensors) ←───────┘
    
    Example:
    - Controller: Adaptive Cruise Control ECU
    - Control Actions: Throttle command, brake command
    - Controlled Process: Vehicle dynamics
    - Feedback: Speed sensor, radar (distance to lead vehicle)

**Process Model:**

    Controller's internal representation of the process state
    
    Accidents occur when:
    - Process model ≠ actual process state (inconsistency)
    - Control algorithm uses incorrect model

**Hierarchical Control:**

.. code-block:: text

    Higher-level controllers constrain lower-level controllers
    
    Example (Automotive):
    
    Level 4: Congress ──→ Safety regulations (FMVSS)
                              │
    Level 3: Automaker ──→ Design standards
                              │
    Level 2: Software ──→ Torque limits, fail-safes
                              │
    Level 1: Actuators ──→ Motor, brakes, steering
                              │
    Level 0: Vehicle physics

**1.3 Why STPA for Modern Systems**
-----------------------------------

**Problems with FMEA/FTA for Software:**

❌ **Software doesn't "fail"**: No random failures, only design flaws  
❌ **Combinatorial explosion**: Too many states to enumerate  
❌ **Emergent behavior**: System-level hazards not in components  
❌ **Human-automation interaction**: Not captured by component analysis

**STPA Advantages:**

✅ **Analyzes design flaws**: Logic errors, race conditions, mode confusion  
✅ **Handles complexity**: Control structure reveals interactions  
✅ **Early application**: Works from requirements (no detailed design needed)  
✅ **Human factors**: Operators are controllers in the loop  
✅ **Adaptive systems**: Handles machine learning, autonomy

════════════════════════════════════════════════════════════════════

📖 **2. STPA PROCESS (4 STEPS)**
════════════════════════════════

**2.1 Step 0: Define Purpose**
------------------------------

**Identify Losses (Accidents to Prevent):**

.. code-block:: text

    Loss = Unacceptable outcome (death, injury, damage, mission failure)
    
    Example (Autonomous Vehicle):
    - L-1: Loss of life (pedestrian, occupant, other driver)
    - L-2: Personal injury
    - L-3: Property damage (vehicle, infrastructure)
    - L-4: Environmental damage
    
    Example (Medical Device):
    - L-1: Patient death
    - L-2: Patient injury
    - L-3: Incorrect diagnosis/treatment
    - L-4: Loss of patient data

**Define System-Level Hazards:**

    Hazard = System state that can lead to loss (given worst-case environment)

.. code-block:: text

    Example (Autonomous Vehicle):
    - H-1: Vehicle collides with object [L-1, L-2, L-3]
    - H-2: Vehicle leaves roadway [L-1, L-2, L-3]
    - H-3: Vehicle fails to yield right-of-way [L-1, L-2]
    - H-4: Vehicle exceeds safe speed [L-1, L-2, L-3]
    
    Example (Insulin Pump):
    - H-1: Overdose delivered [L-1, L-2]
    - H-2: No insulin delivered when needed [L-1, L-2]
    - H-3: Insulin delivered to wrong patient [L-1, L-2]

**2.2 Step 1: Identify Control Structure**
------------------------------------------

**Map Hierarchical Control:**

.. code-block:: text

    Example: Autonomous Vehicle Lane Keeping
    
                    ┌─────────────────────┐
                    │ Mission Planner     │ (High-level goal)
                    │ (Navigate A→B)      │
                    └──────────┬──────────┘
                               │ Route
                               ▼
                    ┌─────────────────────┐
                    │ Behavioral Layer    │ (Tactical decisions)
                    │ (Lane keeping)      │
                    └──────────┬──────────┘
                               │ Desired trajectory
                               ▼
                    ┌─────────────────────┐
                    │ Control Layer       │ (Reactive control)
                    │ (Steering, throttle)│
                    └──────────┬──────────┘
                               │ Commands
                               ▼
                    ┌─────────────────────┐
                    │ Actuators           │
                    │ (Steering motor)    │
                    └──────────┬──────────┘
                               │
                               ▼
                        Vehicle Dynamics
                               │
                               │ Feedback
                               ▼
                    ┌─────────────────────┐
                    │ Sensors             │
                    │ (Camera, GPS, IMU)  │
                    └─────────────────────┘

**Detailed Control Loop:**

.. code-block:: text

    Controller: Lane Keeping System
    ┌──────────────────────────────────────────────┐
    │ Process Model:                               │
    │ - Current lane position (offset from center) │
    │ - Vehicle heading                            │
    │ - Road curvature                             │
    │ - Speed                                      │
    └──────────────┬───────────────────────────────┘
                   │
                   │ Control Algorithm
                   │ (PID controller)
                   │
                   ▼
    Control Actions:
    - Steering angle command [-30°, +30°]
    - Torque vectoring (optional)
                   │
                   ▼
    ┌──────────────────────────────┐
    │   Controlled Process:        │
    │   Vehicle lateral dynamics   │
    └──────────────┬───────────────┘
                   │
                   │ Feedback
                   ▼
    Sensors:
    - Camera (lane markings)
    - GPS (absolute position)
    - IMU (yaw rate, lateral accel)

**2.3 Step 2: Identify Unsafe Control Actions (UCAs)**
------------------------------------------------------

**UCA Table Template:**

+--------------------+----------------+-------------------+------------------+------------------+
| **Control Action** | **Provided**   | **Not Provided**  | **Too Early/**   | **Stopped Too**  |
|                    | **(unsafe)**   | **(when needed)** | **Late/Wrong**   | **Soon/Applied** |
|                    |                |                   | **Order**        | **Too Long**     |
+====================+================+===================+==================+==================+
| Steering left      | At highway     | When drifting     | After leaving    | Returns to       |
| (15° command)      | speed on       | right (no         | lane (too late)  | center too       |
|                    | curve → leaves | correction →      |                  | quickly (over-   |
|                    | road [H-2]     | crash) [H-1]      |                  | correction) [H-2]|
+--------------------+----------------+-------------------+------------------+------------------+
| Apply brakes       | On dry road    | Before collision  | After collision  | Brakes locked    |
| (max deceleration) | at highway     | (insufficient     | started (too     | (loss of         |
|                    | speed →        | stopping distance)| late) [H-1]      | steering) [H-1]  |
|                    | unnecessary    | [H-1]             |                  |                  |
|                    | (passenger     |                   |                  |                  |
|                    | injury) [L-2]  |                   |                  |                  |
+--------------------+----------------+-------------------+------------------+------------------+

**Systematic UCA Identification:**

For each control action, ask:

1. **Provided (unsafe)**: When is this control action unsafe if provided?
2. **Not Provided**: When is this control action unsafe if NOT provided?
3. **Timing**: When is timing wrong (too early, too late, wrong order)?
4. **Duration**: When is duration wrong (stopped too soon, applied too long)?

**Example: Autonomous Emergency Braking (AEB)**

.. code-block:: text

    Control Action: AEB applies full braking
    
    UCA-1 (Provided, unsafe):
    - No obstacle present (false positive) → Rear-end collision [H-1]
    - Vehicle stationary (parked) → Passenger injury [L-2]
    - On highway at high speed → Rear-end by following vehicle [H-1]
    
    UCA-2 (Not Provided, when needed):
    - Obstacle detected, collision imminent → Crash [H-1]
    - Pedestrian in crosswalk → Pedestrian injury [L-1]
    
    UCA-3 (Too Early/Late):
    - Too early (>5 sec before collision) → Unnecessary braking [L-2]
    - Too late (<0.5 sec) → Insufficient stopping distance [H-1]
    
    UCA-4 (Duration wrong):
    - Released too soon → Resume toward obstacle [H-1]
    - Applied too long → Traffic obstruction (vehicle stopped in road) [H-1]

**2.4 Step 3: Identify Loss Scenarios (Causal Factors)**
--------------------------------------------------------

**For each UCA, identify WHY it might occur:**

**Causal Factor Categories:**

1. **Inadequate control algorithm**
2. **Incorrect process model** (controller's belief ≠ reality)
3. **Inadequate feedback** (sensors fail, delayed, incorrect)
4. **Control actions not executed** (actuator fails)
5. **Process behavior** (unexpected response)
6. **External disturbances**

**Example: UCA-1 (AEB false positive)**

.. code-block:: text

    UCA-1: AEB applies full braking when no obstacle present
    
    Loss Scenario 1: Inadequate sensor processing
    - Camera detects bridge shadow as obstacle
    - Radar multi-path (reflection) creates ghost object
    - Sensor fusion algorithm insufficient
    → Safety Constraint: SC-1: AEB shall require multi-sensor confirmation
    
    Loss Scenario 2: Incorrect process model
    - Controller believes obstacle at 10m (actually 100m)
    - Sensor calibration error (range scaling)
    → Safety Constraint: SC-2: Sensor calibration verified at startup
    
    Loss Scenario 3: External disturbance
    - Debris on windshield obscures camera
    - Controller interprets as obstacle
    → Safety Constraint: SC-3: Camera health monitoring required
    
    Loss Scenario 4: Software logic error
    - State machine bug (wrong mode)
    - AEB active when vehicle in "Park"
    → Safety Constraint: SC-4: AEB disabled when vehicle stationary

**2.5 Step 4: Derive Safety Requirements**
------------------------------------------

**From UCAs and loss scenarios → Safety constraints:**

.. code-block:: text

    Example: Autonomous Vehicle Lane Keeping
    
    UCA-5: Steering command not provided when drifting out of lane
    
    Loss Scenario: Camera does not detect lane markings
    - Faded paint
    - Snow covering road
    - Sun glare
    
    Safety Requirements:
    - SR-1: Lane keeping shall be disabled if lane markings not detected
            for >2 seconds
    - SR-2: Driver shall be alerted (visual + audible) when lane keeping
            disabled
    - SR-3: Vehicle shall use GPS + map data as backup lane reference
    - SR-4: System shall transition to "minimal risk condition" (safe stop)
            if all lane references lost

════════════════════════════════════════════════════════════════════

📖 **3. STPA EXAMPLE: AUTONOMOUS VEHICLE**
══════════════════════════════════════════

**3.1 System Description**
--------------------------

**Level 2 Autonomous Vehicle (SAE J3016):**

- Adaptive Cruise Control (ACC)
- Lane Keeping Assist (LKA)
- Automatic Emergency Braking (AEB)
- Driver monitoring (hands on wheel)

**3.2 Step 0: Losses & Hazards**
--------------------------------

**Losses:**

.. code-block:: text

    L-1: Death or serious injury (occupant, pedestrian, other driver)
    L-2: Minor injury
    L-3: Property damage
    L-4: Loss of driver trust (brand reputation)

**System-Level Hazards:**

.. code-block:: text

    H-1: Vehicle collides with object [L-1, L-2, L-3]
    H-2: Vehicle leaves roadway [L-1, L-2, L-3]
    H-3: Vehicle fails to maintain safe following distance [L-1, L-2, L-3]
    H-4: Vehicle accelerates when unsafe [L-1, L-2, L-3]
    H-5: Driver not in control when automation disengages [L-1, L-2]

**3.3 Step 1: Control Structure**
---------------------------------

.. code-block:: text

    Driver (Human Controller)
           │
           ├── Hands on wheel? ──→ Monitoring System
           │                            │
           │                            ▼
           │                    [Alert if hands off]
           │
           ▼
    ┌────────────────────┐
    │ ADAS Controller    │
    │ (ACC + LKA)        │
    └─────────┬──────────┘
              │
              ├── Throttle command ──→ Powertrain
              ├── Brake command    ──→ Braking system
              └── Steering command ──→ Steering actuator
                                           │
                                           ▼
                                   Vehicle Dynamics
                                           │
                                           │ Feedback
                                           ▼
                            ┌──────────────────────────┐
                            │ Sensors:                 │
                            │ - Camera (lane, objects) │
                            │ - Radar (distance)       │
                            │ - Speed sensor           │
                            │ - Steering angle         │
                            └──────────────────────────┘

**3.4 Step 2: UCA Table (Excerpt)**
-----------------------------------

**Control Action: Increase Throttle**

+------------------+-------------------+-------------------+------------------+
| **Provided**     | **Not Provided**  | **Too Early/Late**| **Duration**     |
+==================+===================+===================+==================+
| **UCA-1:**       | **UCA-2:**        | **UCA-3:**        | **UCA-4:**       |
| Throttle         | Throttle NOT      | Throttle          | Throttle         |
| increased when:  | increased when:   | increased:        | increased for    |
|                  |                   |                   | too long:        |
| - Collision      | - Below target    | - Too early:      |                  |
|   imminent [H-1] |   speed on clear  |   Before lane     | - Exceeds speed  |
| - Lead vehicle   |   road (driver    |   change complete |   limit [H-4]    |
|   braking [H-3]  |   expects accel)  |   [H-2]           | - Closes gap to  |
| - Approaching    |   [L-4]           | - Too late:       |   lead vehicle   |
|   curve too fast |                   |   Miss merge gap  |   [H-3]          |
|   [H-2]          |                   |   [H-3]           |                  |
| - Speed limit    |                   |                   |                  |
|   decreasing     |                   |                   |                  |
|   [H-4]          |                   |                   |                  |
+------------------+-------------------+-------------------+------------------+

**Control Action: Apply Brakes**

+------------------+-------------------+-------------------+------------------+
| **Provided**     | **Not Provided**  | **Too Early/Late**| **Duration**     |
+==================+===================+===================+==================+
| **UCA-5:**       | **UCA-6:**        | **UCA-7:**        | **UCA-8:**       |
| Brakes applied   | Brakes NOT        | Brakes applied:   | Brakes applied:  |
| when:            | applied when:     |                   |                   |
|                  |                   | - Too early:      | - Too long:      |
| - No obstacle    | - Collision       |   >5 sec before   |   Stopped in     |
|   (false alarm)  |   imminent [H-1]  |   obstacle (rear- |   traffic [H-1]  |
|   → Rear-end     | - Lead vehicle    |   end risk) [H-1] | - Released too   |
|   [H-1]          |   stopped [H-3]   | - Too late:       |   soon: Resume   |
| - Highway speed  | - Pedestrian in   |   <0.5 sec        |   toward obstacle|
|   (unnecessary)  |   path [H-1]      |   (insufficient   |   [H-1]          |
|   [L-2]          |                   |   distance) [H-1] |                  |
+------------------+-------------------+-------------------+------------------+

**3.5 Step 3: Loss Scenarios (Excerpt)**
----------------------------------------

**UCA-1: Throttle increased when collision imminent**

.. code-block:: text

    Loss Scenario 1.1: Radar does not detect stopped vehicle
    Causal factors:
    - Radar mounted low (ground clutter)
    - Stationary vehicle not tracked (Doppler filter)
    - Software assumes "highway" mode (no stopped vehicles)
    
    Safety Requirements:
    - SR-1: Radar shall detect stationary objects at 150m
    - SR-2: Camera shall provide redundant object detection
    - SR-3: ACC shall deactivate if stopped vehicle detected <50m
    
    Loss Scenario 1.2: Driver not monitoring (hands off wheel)
    Causal factors:
    - Driver believes system is "Level 3" (fully autonomous)
    - Driver monitoring system insufficient (torque sensor only)
    - No visual cue that system requires supervision
    
    Safety Requirements:
    - SR-4: Hands-off detection within 15 seconds
    - SR-5: Escalating alerts (visual → audible → braking → MRC)
    - SR-6: Clear HMI: "Hands on wheel required at all times"
    
    Loss Scenario 1.3: Software mode confusion
    Causal factors:
    - ACC believes highway clear (process model incorrect)
    - Camera temporary occlusion (sun glare) → stale data
    - State machine bug (mode transition error)
    
    Safety Requirements:
    - SR-7: Sensor timeout monitoring (max age 200ms)
    - SR-8: Default to safe state (coast/brake) on sensor loss
    - SR-9: Formal verification of state machine

**3.6 Safety Requirements Summary**
-----------------------------------

.. code-block:: text

    Derived from STPA (25 requirements):
    
    Sensing:
    - SR-1 to SR-3: Redundant object detection
    - SR-7 to SR-8: Sensor health monitoring
    
    Human-Machine Interface:
    - SR-4 to SR-6: Driver monitoring and alerts
    - SR-10: Clear engagement/disengagement feedback
    
    Control Logic:
    - SR-9: Formal verification of state machine
    - SR-11: ACC speed limits (never exceed posted + 10%)
    - SR-12: Minimum following distance (2 sec time gap)
    
    Fail-Safe:
    - SR-13: Minimal Risk Condition (safe stop in lane)
    - SR-14: Redundant braking paths
    
    Testing:
    - SR-15 to SR-20: Scenario-based testing (derived from UCAs)

════════════════════════════════════════════════════════════════════

📖 **4. STPA vs FMEA vs FTA**
═════════════════════════════

**4.1 Comparison Table**
------------------------

+--------------------+------------------+------------------+------------------+
| **Aspect**         | **STPA**         | **FMEA**         | **FTA**          |
+====================+==================+==================+==================+
| **Approach**       | Control theory   | Bottom-up        | Top-down         |
+--------------------+------------------+------------------+------------------+
| **Starting Point** | System hazards   | Component        | Specific hazard  |
|                    |                  | failures         |                  |
+--------------------+------------------+------------------+------------------+
| **Focus**          | Unsafe control   | Failure modes    | Causal logic     |
|                    | actions          | & effects        | (gates)          |
+--------------------+------------------+------------------+------------------+
| **Best For**       | Software,        | Hardware,        | Complex          |
|                    | complex systems, | mechanical       | interactions,    |
|                    | human factors    | systems          | accident         |
|                    |                  |                  | investigation    |
+--------------------+------------------+------------------+------------------+
| **Handles**        | ✅ Design flaws  | ❌ Limited       | ❌ Assumes       |
| **Software?**      | ✅ Logic errors  |                  | component fails  |
+--------------------+------------------+------------------+------------------+
| **Handles**        | ✅ Controller-   | ❌ Not explicit  | ✅ If modeled    |
| **Human Factors?** | controlled       |                  | as "gate"        |
|                    | process          |                  |                  |
+--------------------+------------------+------------------+------------------+
| **Quantitative?**  | No (qualitative) | Yes (RPN)        | Yes (prob.)      |
+--------------------+------------------+------------------+------------------+
| **Standards**      | NASA, FAA        | ISO 26262,       | IEC 61025,       |
|                    | (emerging)       | IEC 61508        | ARP4761          |
+--------------------+------------------+------------------+------------------+

**4.2 When to Use Each**
------------------------

**Use STPA when:**

✅ Software-intensive system (autonomous vehicles, avionics, medical devices)  
✅ Early design phase (requirements analysis)  
✅ Complex human-automation interaction (operator in the loop)  
✅ Adaptive/learning systems (AI, machine learning)  
✅ Multiple control loops with feedback  
✅ Traditional methods incomplete (e.g., mode confusion not captured)

**Use FMEA when:**

✅ Hardware-dominated system (mechanical, electrical)  
✅ Component-level analysis  
✅ Quantitative risk assessment needed (RPN)  
✅ ISO 26262 / IEC 61508 compliance required  
✅ Design FMEA (DFMEA) or Process FMEA (PFMEA)

**Use FTA when:**

✅ Specific hazard to investigate (accident follow-up)  
✅ Verify redundancy effectiveness  
✅ Quantitative probability calculation needed  
✅ Regulatory requirement (aerospace ARP4761)  
✅ Minimal cut set analysis

**Best Practice: Use All Three!**

.. code-block:: text

    Comprehensive Safety Analysis:
    
    1. STPA (early design):
       - Identify UCAs
       - Derive safety requirements
       - Define control architecture
    
    2. FMEA (detailed design):
       - Analyze hardware failure modes
       - Calculate RPN
       - Verify detection mechanisms
    
    3. FTA (verification):
       - Verify ASIL/DAL compliance
       - Quantify system-level reliability
       - Identify single points of failure
    
    Cross-check: STPA UCAs should map to FMEA failure modes and FTA events

════════════════════════════════════════════════════════════════════

📖 **5. STPA TOOLS & AUTOMATION**
═════════════════════════════════

**5.1 Commercial Tools**
------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Features**               |
+======================+==================+============================+
| **XSTAMPP**          | Open source      | Free, control structure    |
|                      | (GitHub)         | diagrams, UCA tables       |
+----------------------+------------------+----------------------------+
| **STAMP Workbench**  | MIT (research)   | Academic tool, research    |
+----------------------+------------------+----------------------------+
| **A-STPA**           | Adelard          | Aerospace applications     |
+----------------------+------------------+----------------------------+
| **medini analyze**   | Siemens          | Automotive (ISO 26262)     |
|                      |                  | STPA + FMEA integration    |
+----------------------+------------------+----------------------------+

**5.2 Python UCA Generator**
----------------------------

**Automated UCA Table Generation:**

.. code-block:: python

    # stpa_uca_generator.py
    
    import pandas as pd
    from itertools import product
    
    # Define control actions
    control_actions = [
        "Apply brakes",
        "Increase throttle",
        "Steer left",
        "Steer right",
        "Deploy airbag"
    ]
    
    # Define hazards
    hazards = [
        "H-1: Vehicle collides with object",
        "H-2: Vehicle leaves roadway",
        "H-3: Unsafe following distance",
        "H-4: Excessive speed"
    ]
    
    # UCA types
    uca_types = [
        "Provided (unsafe)",
        "Not Provided (when needed)",
        "Too Early/Late/Wrong Order",
        "Stopped Too Soon / Applied Too Long"
    ]
    
    # Generate UCA table structure
    uca_data = []
    uca_id = 1
    
    for ca in control_actions:
        for uca_type in uca_types:
            uca_data.append({
                'UCA_ID': f'UCA-{uca_id}',
                'Control_Action': ca,
                'UCA_Type': uca_type,
                'Context': '',  # To be filled manually
                'Hazard_Link': '',  # To be filled manually
                'Causal_Factors': '',
                'Safety_Requirement': ''
            })
            uca_id += 1
    
    # Create DataFrame
    uca_df = pd.DataFrame(uca_data)
    
    # Export to Excel for team review
    uca_df.to_excel('STPA_UCA_Template.xlsx', index=False)
    
    print(f"Generated {len(uca_data)} UCA entries")
    print("\nSample UCAs:")
    print(uca_df.head(8))

**5.3 Control Structure Visualizer**
------------------------------------

**Generate control loop diagrams:**

.. code-block:: python

    # stpa_control_structure.py (using Graphviz)
    
    from graphviz import Digraph
    
    def create_control_structure():
        dot = Digraph(comment='STPA Control Structure')
        dot.attr(rankdir='TB')  # Top to bottom
        
        # Define nodes
        dot.node('Driver', 'Human Driver\n(Supervisor)', shape='box')
        dot.node('ADAS', 'ADAS Controller\n(ACC + LKA)', shape='box', 
                 style='filled', fillcolor='lightblue')
        dot.node('Actuators', 'Actuators\n(Throttle, Brake, Steering)', 
                 shape='box')
        dot.node('Vehicle', 'Vehicle Dynamics\n(Controlled Process)', 
                 shape='ellipse', style='filled', fillcolor='lightgrey')
        dot.node('Sensors', 'Sensors\n(Camera, Radar, Speed)', shape='box')
        
        # Control actions (forward)
        dot.edge('Driver', 'ADAS', label='Enable/Disable\nSet target speed')
        dot.edge('ADAS', 'Actuators', 
                 label='Throttle cmd\nBrake cmd\nSteering cmd')
        dot.edge('Actuators', 'Vehicle', label='Forces & Torques')
        
        # Feedback (reverse)
        dot.edge('Vehicle', 'Sensors', label='Motion, Position')
        dot.edge('Sensors', 'ADAS', 
                 label='Speed, Distance,\nLane position', style='dashed')
        dot.edge('ADAS', 'Driver', label='Status, Alerts', style='dashed')
        
        # External disturbances
        dot.node('Env', 'Environment\n(Road, Traffic, Weather)', 
                 shape='diamond', style='filled', fillcolor='lightyellow')
        dot.edge('Env', 'Vehicle', label='Disturbances', style='dotted')
        dot.edge('Env', 'Sensors', label='Visibility, Occlusion', 
                 style='dotted')
        
        # Render
        dot.render('stpa_control_structure', format='png', cleanup=True)
        print("Control structure diagram saved: stpa_control_structure.png")
    
    if __name__ == "__main__":
        create_control_structure()

════════════════════════════════════════════════════════════════════

📖 **6. STPA CASE STUDIES**
═══════════════════════════

**6.1 NASA: NextGen Air Traffic Control**
-----------------------------------------

**Application:** National Airspace System modernization

**Key Findings:**

- Traditional methods missed human-automation interaction hazards
- STPA identified 35% more hazards than FMEA/FTA
- Mode confusion (controller mental model vs. system state)
- Loss of separation due to inadequate feedback

**Example UCA:**

.. code-block:: text

    Control Action: ATC assigns altitude to aircraft
    
    UCA: Altitude assigned conflicts with another aircraft route
    
    Causal Factors:
    - ATC mental model outdated (delayed radar update)
    - Display does not show aircraft intent (future position)
    - Communication delay (pilot acknowledges but doesn't comply)
    
    Safety Requirements:
    - SR: Conflict detection algorithm with 5-minute lookahead
    - SR: Display intent information (flight plan overlay)
    - SR: Automated alert if altitude conflict detected

**6.2 Automotive: Tesla Autopilot Analysis**
--------------------------------------------

**Independent STPA (MIT, 2019):**

**Identified UCAs:**

1. **Autosteer enabled on non-highway road** [H-2: Leaves roadway]
   - Causal: Driver misunderstands operational design domain (ODD)
   - Requirement: Geofencing (disable outside highways)

2. **Autosteer does not disengage when driver unresponsive** [H-1: Collision]
   - Causal: Torque sensor insufficient (hands on wheel but not attentive)
   - Requirement: Eye tracking + escalating alerts

3. **Navigate on Autopilot lane change without checking blind spot** [H-1]
   - Causal: Camera blind spot, late sensor data
   - Requirement: Blind spot monitoring integration

**6.3 Medical: Therac-25 Retrospective**
----------------------------------------

**Therac-25 radiation therapy overdoses (1985-1987):**

    6 patients received 100× radiation dose → Deaths

**Traditional Analysis (at the time):**

- Software bug (race condition)
- Inadequate testing

**STPA Retrospective (what would have been found):**

.. code-block:: text

    Control Action: Deliver radiation beam
    
    UCA-1: Beam delivered at high energy when patient setup incomplete
    
    Loss Scenarios:
    1. Mode confusion: Software believes "X-ray mode" but hardware in 
       "Electron mode" (no flattening filter)
    2. Operator bypasses safety checks (pressure to maintain schedule)
    3. No independent energy verification (single sensor)
    
    Safety Requirements (that were missing):
    - SR-1: Hardware interlock (energy level vs. mode)
    - SR-2: Independent dose measurement (redundant)
    - SR-3: Prevent operator bypass (require supervisor override)
    - SR-4: Display actual beam energy (feedback to operator)

**Lesson:** STPA would have identified mode confusion and inadequate feedback

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What are the 4 types of Unsafe Control Actions (UCAs) in STPA?

**A1:**

1. **Provided (unsafe)**: Control action provided causes hazard
2. **Not Provided (when needed)**: Control action NOT provided causes hazard
3. **Too Early/Late/Wrong Order**: Timing or sequence wrong
4. **Stopped Too Soon / Applied Too Long**: Duration wrong

────────────────────────────────────────────────────────────────────

**Q2:** Why is STPA better than FMEA for software-intensive systems?

**A2:**

- **Software doesn't "fail"**: No random failures, only design flaws
- **STPA analyzes logic errors**: Control flow, mode confusion, timing
- **Handles complexity**: Control structure reveals interactions
- **FMEA assumes component failures**: Not applicable to software bugs

────────────────────────────────────────────────────────────────────

**Q3:** What is a "process model" in STAMP theory?

**A3:**

Controller's internal representation of the controlled process state.

Accidents occur when: **Process model ≠ actual state** (inconsistency)

Example:
- Autopilot believes: "Highway, 65 mph, no obstacles"
- Reality: "Construction zone, 45 mph, stopped truck ahead"
- Result: Collision (inadequate control due to incorrect model)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Step 0: Define Purpose**
- [ ] Identify losses (unacceptable outcomes)
- [ ] Define system-level hazards (states leading to losses)
- [ ] Link hazards to losses

**Step 1: Control Structure**
- [ ] Identify all controllers (human, software, hardware)
- [ ] Map control actions (commands from controllers)
- [ ] Map feedback (sensors, measurements)
- [ ] Identify controlled processes
- [ ] Draw hierarchical control structure
- [ ] Identify process models (what each controller "believes")

**Step 2: Identify UCAs**
- [ ] Create UCA table (control actions × 4 UCA types)
- [ ] For each control action, identify contexts where:
  - [ ] Provided causes hazard
  - [ ] Not Provided causes hazard
  - [ ] Too Early/Late/Wrong Order causes hazard
  - [ ] Duration wrong causes hazard
- [ ] Link each UCA to hazards

**Step 3: Identify Loss Scenarios**
- [ ] For each UCA, brainstorm causal factors:
  - [ ] Inadequate control algorithm
  - [ ] Incorrect process model
  - [ ] Inadequate feedback
  - [ ] Control actions not executed
  - [ ] Process behavior unexpected
  - [ ] External disturbances
- [ ] Document loss scenario paths

**Step 4: Derive Safety Requirements**
- [ ] Convert causal factors to safety constraints
- [ ] Assign requirements to:
  - [ ] Control algorithms (logic)
  - [ ] Feedback mechanisms (sensors, health monitoring)
  - [ ] Human-machine interface (displays, alerts)
  - [ ] Fail-safe mechanisms (default states)
- [ ] Prioritize requirements (by hazard severity)
- [ ] Allocate to design elements
- [ ] Define verification methods

**Integration with Design**
- [ ] Trace requirements to design elements
- [ ] Update safety analysis as design evolves
- [ ] Cross-check with FMEA/FTA
- [ ] Include in safety case

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **STPA = Control theory approach** → Accidents from inadequate control, not just failures

2️⃣ **4 UCA types** → Provided, Not Provided, Timing, Duration (systematic coverage)

3️⃣ **Best for software** → Analyzes logic errors, mode confusion, human factors

4️⃣ **Control structure** → Controllers, control actions, feedback, process models

5️⃣ **Process model** → Controller's belief; accidents when belief ≠ reality

6️⃣ **Early design phase** → Works from requirements (no detailed design needed)

7️⃣ **Complement FMEA/FTA** → Use all three for comprehensive safety analysis

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **STPA CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** STAMP theory, 4-step STPA process, UCA identification,  
control structures, autonomous vehicle example, comparison with FMEA/FTA,  
tools, case studies (NASA, Tesla, Therac-25)

════════════════════════════════════════════════════════════════════
