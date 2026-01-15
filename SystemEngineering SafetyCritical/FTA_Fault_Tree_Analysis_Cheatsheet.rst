🌲 **FTA — Fault Tree Analysis**
═══════════════════════════════════════════════════════════════════

**Full Name:** Fault Tree Analysis (FTA)  
**Type:** Top-down deductive safety analysis technique  
**Origin:** Bell Telephone Laboratories (1962), Boeing Minuteman missile program  
**Standards:** IEC 61025, NASA, MIL-STD-882E, ISO 26262, ARP4761

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — FTA IN 60 SECONDS**
────────────────────────────────

**What is FTA?**

::

    FTA = Deductive analysis starting from a top hazardous event
    
    Question: "WHY did this hazard occur?"
    
    Process:
    1. Define top event (hazard)
    2. Identify immediate causes (AND/OR gates)
    3. Decompose recursively until basic events
    4. Calculate probability (quantitative FTA)
    5. Identify minimal cut sets
    6. Recommend safety improvements

**FTA vs FMEA:**

+------------------+--------------------------------+----------------------------+
| **Aspect**       | **FTA (Fault Tree Analysis)**  | **FMEA**                   |
+==================+================================+============================+
| **Direction**    | Top-down (deductive)           | Bottom-up (inductive)      |
+------------------+--------------------------------+----------------------------+
| **Starting**     | Hazardous event               | Component failure          |
| **Point**        |                               |                            |
+------------------+--------------------------------+----------------------------+
| **Question**     | "WHY did it happen?"          | "WHAT can go wrong?"       |
+------------------+--------------------------------+----------------------------+
| **Logic**        | Boolean (AND, OR gates)       | Sequential effects         |
+------------------+--------------------------------+----------------------------+
| **Output**       | Minimal cut sets, probability | RPN (risk priority number) |
+------------------+--------------------------------+----------------------------+
| **Best For**     | Accident investigation        | Design phase               |
|                  | Complex interactions          | Component-level analysis   |
+------------------+--------------------------------+----------------------------+

**Basic Logic Gates:**

::

    AND Gate (◇):        OR Gate (⊃):         NOT Gate (⎯◇):
    
    ┌───┐               ┌───┐                ┌───┐
    │ A │──┐            │ A │──┐             │ A │──┐
    └───┘  │  ◇         └───┘  │  ⊃          └───┘  │ ⎯◇
    ┌───┐  ├──→         ┌───┐  ├──→                 └──→
    │ B │──┘            │ B │──┘                     
    └───┘               └───┘                        
    
    A AND B             A OR B              NOT A
    (Both required)     (Either sufficient) (Negation)

**Top Event Probability:**

::

    For independent events:
    
    P(A AND B) = P(A) × P(B)
    P(A OR B) = P(A) + P(B) - P(A) × P(B)
    P(NOT A) = 1 - P(A)

════════════════════════════════════════════════════════════════════

📖 **1. FTA FUNDAMENTALS**
══════════════════════════

**1.1 Definition & Purpose**
----------------------------

**Fault Tree Analysis:**

- **Deductive**: Works backward from effect to causes
- **Graphical**: Tree structure with logic gates
- **Quantitative**: Calculates failure probabilities
- **Systematic**: Identifies all possible paths to failure
- **Certification**: Required for aerospace (ARP4761), automotive (ISO 26262)

**Objectives:**

✅ Understand failure causation (accident investigation)  
✅ Identify critical failure paths (minimal cut sets)  
✅ Calculate system reliability/safety  
✅ Verify redundancy effectiveness  
✅ Guide design improvements (eliminate single points of failure)  
✅ Support certification (demonstrate compliance)

**1.2 When to Use FTA**
-----------------------

**Ideal for:**

✅ Complex systems with interactions  
✅ Redundant architectures (need to verify)  
✅ Accident investigation (post-mortem)  
✅ Safety-critical systems (ASIL C/D, DAL A/B)  
✅ Compliance requirements (ISO 26262, ARP4761)

**Not ideal for:**

❌ Early design phase (use FMEA first)  
❌ Unknown failure modes (use HAZOP)  
❌ Software-dominated logic (use STPA)  
❌ Time-dependent sequences (use Event Tree)

**1.3 FTA Terminology**
-----------------------

+-------------------+----------------------------------+
| **Term**          | **Definition**                   |
+===================+==================================+
| **Top Event**     | Undesired hazardous event        |
+-------------------+----------------------------------+
| **Basic Event**   | Lowest-level cause (no further   |
|                   | decomposition)                   |
+-------------------+----------------------------------+
| **Intermediate**  | Cause requiring further          |
| **Event**         | decomposition                    |
+-------------------+----------------------------------+
| **Gate**          | Logic relationship (AND, OR, etc)|
+-------------------+----------------------------------+
| **Cut Set**       | Combination of basic events      |
|                   | causing top event                |
+-------------------+----------------------------------+
| **Minimal Cut**   | Smallest combination (remove any |
| **Set (MCS)**     | event → top event doesn't occur) |
+-------------------+----------------------------------+

════════════════════════════════════════════════════════════════════

📖 **2. FTA SYMBOLS & GATES**
═════════════════════════════

**2.1 Event Symbols**
---------------------

**Standard IEC 61025 Symbols:**

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │                    FTA EVENT SYMBOLS                        │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  ┌───────────┐                                             │
    │  │   ███████ │  TOP EVENT (Rectangle)                      │
    │  │   ███████ │  The undesired hazardous event              │
    │  └───────────┘  Example: "Aircraft crashes"                │
    │                                                             │
    │  ┌───────────┐                                             │
    │  │           │  INTERMEDIATE EVENT (Rectangle)             │
    │  │           │  Event requiring further decomposition      │
    │  └───────────┘  Example: "Engine fails"                    │
    │                                                             │
    │       ○                                                     │
    │      ╱ ╲        BASIC EVENT (Circle)                       │
    │     ╱   ╲       Lowest-level cause (no further analysis)   │
    │    ╱     ╲      Example: "Fuel line ruptures"              │
    │   ╱       ╲                                                 │
    │  ───────────                                                │
    │                                                             │
    │      ◇          UNDEVELOPED EVENT (Diamond)                │
    │     ╱ ╲         Cause not analyzed (insufficient info)     │
    │    ╱   ╲        Example: "External factor" (lightning)     │
    │   ╱     ╲                                                   │
    │  ─────────                                                  │
    │                                                             │
    │      △          HOUSE EVENT (Triangle)                     │
    │     ╱ ╲         Event normally expected to occur           │
    │    ╱   ╲        Example: "System is powered on"            │
    │   ───────                                                   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

**2.2 Logic Gates**
-------------------

**Primary Gates:**

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │                     FTA LOGIC GATES                         │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │        ◇         AND GATE                                   │
    │       ╱ ╲        Output occurs if ALL inputs occur         │
    │      ╱   ╲       Example: Dual sensor failure (both fail)  │
    │     ╱     ╲      Probability: P(A AND B) = P(A) × P(B)     │
    │    ───┬───                                                  │
    │       │                                                     │
    │   ────┴────                                                 │
    │   │   │   │                                                 │
    │   A   B   C                                                 │
    │                                                             │
    │        ⊃         OR GATE                                    │
    │       ╱ ╲        Output occurs if ANY input occurs         │
    │      ╱   ╲       Example: Single point failures            │
    │     ╱     ╲      Probability: P(A OR B) = P(A) + P(B)      │
    │    ───┬───                            - P(A) × P(B)        │
    │       │                                                     │
    │   ────┴────                                                 │
    │   │   │   │                                                 │
    │   A   B   C                                                 │
    │                                                             │
    │      ⎯◇         PRIORITY AND GATE                          │
    │     ╱ ╲         Output if inputs occur in order            │
    │    ╱   ╲        Example: A before B (sequence matters)     │
    │   ╱     ╲                                                   │
    │  ───┬───                                                    │
    │     │                                                       │
    │  ───┴───                                                    │
    │  │  │  │                                                    │
    │  A  B  C  (order: A→B→C)                                   │
    │                                                             │
    │       ⊕         EXCLUSIVE OR (XOR) GATE                    │
    │      ╱ ╲        Output if exactly ONE input occurs         │
    │     ╱   ╲       Example: Conflict (mutually exclusive)     │
    │    ╱     ╲      Probability: P(A XOR B) = P(A) + P(B)      │
    │   ───┬───                            - 2×P(A)×P(B)         │
    │      │                                                      │
    │  ────┴────                                                  │
    │  │       │                                                  │
    │  A       B                                                  │
    │                                                             │
    │      ⊖          INHIBIT GATE                               │
    │     ╱ ╲         Output if input AND condition true         │
    │    ╱   ╲        Example: Failure only if system active     │
    │   ╱     ╲       Condition shown as oval below gate         │
    │  ───┬───                                                    │
    │     │                                                       │
    │  ───┴───                                                    │
    │  │     │                                                    │
    │  A   ⟨Cond⟩                                                │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

**2.3 Probability Calculations**
--------------------------------

**Boolean Algebra for Independent Events:**

.. code-block:: text

    1. AND Gate:
       P(A AND B) = P(A) × P(B)
       
       Example: Both sensors fail
       P(Sensor1=10⁻³) × P(Sensor2=10⁻³) = 10⁻⁶
    
    2. OR Gate (Exact):
       P(A OR B) = P(A) + P(B) - P(A) × P(B)
       
       Example: Either sensor fails
       P = 10⁻³ + 10⁻³ - (10⁻³ × 10⁻³) = 0.001999 ≈ 2×10⁻³
    
    3. OR Gate (Rare Event Approximation):
       If P(A), P(B) << 1, then P(A OR B) ≈ P(A) + P(B)
       
       Example: 10⁻³ + 10⁻³ ≈ 2×10⁻³ (error < 0.1%)
    
    4. NOT Gate:
       P(NOT A) = 1 - P(A)
       
       Example: Sensor does NOT fail
       P = 1 - 10⁻³ = 0.999
    
    5. XOR Gate:
       P(A XOR B) = P(A) + P(B) - 2×P(A)×P(B)
    
    6. k-out-of-n Gate:
       At least k out of n components fail
       Uses binomial probability

════════════════════════════════════════════════════════════════════

📖 **3. FTA CONSTRUCTION PROCESS**
══════════════════════════════════

**3.1 Step 1: Define Top Event**
--------------------------------

**Top Event Characteristics:**

✅ **Specific**: "Engine fails during takeoff" (not "engine problem")  
✅ **Undesired**: Hazardous or failure condition  
✅ **Observable**: Can be detected/measured  
✅ **System-level**: Not component-specific

**Example Top Events:**

.. code-block:: text

    Automotive:
    - "Unintended acceleration" (ASIL D)
    - "Loss of braking" (ASIL D)
    - "Airbag fails to deploy" (ASIL C)
    
    Aerospace:
    - "Loss of flight control" (DAL A)
    - "Engine thrust reverser deploys in flight" (Catastrophic)
    - "Cabin depressurization" (Hazardous)
    
    Medical:
    - "Insulin pump overdose" (Critical)
    - "Pacemaker fails to pace" (Catastrophic)
    - "Ventilator delivers no oxygen" (Critical)

**3.2 Step 2: Identify Immediate Causes**
-----------------------------------------

**Deductive Reasoning:**

    "What failures or conditions could directly cause this top event?"

**Example: Automotive Brake Failure**

.. code-block:: text

    Top Event: "Vehicle fails to brake"
    
    Immediate Causes (OR gate — any ONE causes failure):
    1. Hydraulic system failure
    2. Electronic control failure (ABS/ESC)
    3. Mechanical failure (pads, rotors)
    4. Driver error (not pressing pedal — typically excluded)
    
    FTA Structure:
    
           ┌──────────────────────────┐
           │ Vehicle fails to brake   │
           │      (Top Event)         │
           └────────────┬─────────────┘
                        │
                        ⊃  OR Gate
                ┌───────┼───────┐
                │       │       │
    ┌───────────┴──┐ ┌──┴────────────┐ ┌─────────────┐
    │ Hydraulic    │ │ Electronic    │ │ Mechanical  │
    │ failure      │ │ control fails │ │ failure     │
    └──────────────┘ └───────────────┘ └─────────────┘

**3.3 Step 3: Decompose Recursively**
-------------------------------------

**Continue until Basic Events:**

- Hardware failures (e.g., "Pump fails")
- Software faults (e.g., "Algorithm error")
- Human errors (e.g., "Maintenance mistake")
- Environmental conditions (e.g., "Temperature >85°C")

**Example: Hydraulic System Decomposition**

.. code-block:: text

    ┌────────────────────┐
    │ Hydraulic failure  │
    └─────────┬──────────┘
              │
              ⊃  OR
      ┌───────┼───────┬─────────┐
      │       │       │         │
    ┌─┴──┐  ┌─┴──┐  ┌─┴──┐   ┌─┴──┐
    │Leak│  │Pump│  │Line│   │Fluid│
    │    │  │fails│  │block│  │empty│
    └────┘  └────┘  └─────┘   └────┘
     (○)     (○)      (○)       (○)
    Basic   Basic    Basic     Basic
    Events  Events   Events    Events

**3.4 Step 4: Add Redundancy Logic**
------------------------------------

**Redundant Systems Use AND Gates:**

.. code-block:: text

    Example: Dual-Redundant Sensor System
    
    Top Event: "Sensor system fails"
    
           ┌────────────────────────┐
           │ Sensor system fails    │
           └───────────┬────────────┘
                       │
                       ◇  AND Gate (BOTH must fail)
                 ┌─────┴─────┐
                 │           │
           ┌─────┴─────┐ ┌───┴───────┐
           │ Sensor A  │ │ Sensor B  │
           │  fails    │ │  fails    │
           └───────────┘ └───────────┘
              (○)            (○)
           P = 10⁻³       P = 10⁻³
    
    System Failure Probability:
    P = 10⁻³ × 10⁻³ = 10⁻⁶ (1000× improvement!)

**3.5 Step 5: Calculate Probabilities**
---------------------------------------

**Bottom-Up Calculation:**

1. Assign probabilities to basic events (from data or estimates)
2. Calculate intermediate events using gate logic
3. Propagate upward to top event

**Example Calculation:**

.. code-block:: python

    # fta_calculation.py
    
    # Basic event probabilities (per hour)
    P_sensor_A = 1e-3  # 0.001
    P_sensor_B = 1e-3
    P_power_supply = 1e-4
    P_wiring = 1e-5
    
    # Intermediate event: Sensor system fails (AND gate)
    P_sensor_system = P_sensor_A * P_sensor_B  # Both must fail
    print(f"Sensor system failure: {P_sensor_system:.2e}")  # 1.00e-06
    
    # Intermediate event: Power fails (OR gate)
    P_power = P_power_supply + P_wiring - (P_power_supply * P_wiring)
    print(f"Power failure: {P_power:.2e}")  # 1.10e-04
    
    # Top event: System fails (OR gate)
    P_top = P_sensor_system + P_power - (P_sensor_system * P_power)
    print(f"Top event probability: {P_top:.2e}")  # 1.11e-04

════════════════════════════════════════════════════════════════════

📖 **4. MINIMAL CUT SETS (MCS)**
════════════════════════════════

**4.1 Definition**
------------------

**Minimal Cut Set (MCS):**

    Smallest combination of basic events that, if they ALL occur,
    will cause the top event to occur.
    
    "Minimal" means: Remove any event → top event won't occur

**Example:**

.. code-block:: text

    Fault Tree:
    
           ┌─────────┐
           │ Top     │
           └────┬────┘
                ⊃ OR
          ┌─────┴─────┐
          ◇           ○
       ┌──┴──┐        C
       ○     ○
       A     B
    
    Minimal Cut Sets:
    1. {A, B}  — Both A AND B must fail
    2. {C}     — C alone causes top event
    
    Interpretation:
    - MCS {C} is most critical (single point of failure)
    - MCS {A, B} requires dual failure (less critical)

**4.2 Finding MCS (Boolean Algebra)**
-------------------------------------

**Reduction Rules:**

.. code-block:: text

    1. Absorption: A + A·B = A
       (If A occurs, A AND B is redundant)
    
    2. Idempotent: A + A = A, A·A = A
    
    3. Distributive: A·(B+C) = A·B + A·C
    
    4. Null: A·0 = 0, A+1 = 1

**Example Reduction:**

.. code-block:: text

    Fault Tree:
    
           Top
            ⊃
       ┌────┴────┐
       ◇         ◇
     ┌─┴─┐     ┌─┴─┐
     A   B     C   D
    
    Boolean Expression:
    Top = (A·B) + (C·D)
    
    Minimal Cut Sets:
    1. {A, B}
    2. {C, D}
    
    No reduction possible (already minimal)

**4.3 MCS Importance Ranking**
------------------------------

**Criticality Criteria:**

1. **Order**: Lower order = more critical
   - Order 1: Single event (SPOF - Single Point of Failure)
   - Order 2: Dual failure required
   - Order 3+: Multiple failures required

2. **Probability**: Higher probability = more critical

**Example Ranking:**

.. code-block:: text

    MCS Analysis Results:
    
    | MCS | Events      | Order | Probability | Criticality |
    |-----|-------------|-------|-------------|-------------|
    | 1   | {C}         | 1     | 10⁻³        | CRITICAL ⚠️ |
    | 2   | {A, B}      | 2     | 10⁻⁶        | HIGH        |
    | 3   | {D, E, F}   | 3     | 10⁻⁹        | LOW         |
    
    Action:
    - MCS 1: Eliminate single point of failure (add redundancy)
    - MCS 2: Monitor (already dual redundant)
    - MCS 3: Accept (triple failure unlikely)

════════════════════════════════════════════════════════════════════

📖 **5. FTA EXAMPLE: AUTOMOTIVE**
═════════════════════════════════

**5.1 Case Study: Unintended Acceleration**
-------------------------------------------

**Top Event:** "Vehicle accelerates without driver input" (ASIL D)

**Complete Fault Tree:**

.. code-block:: text

                ┌──────────────────────────────────┐
                │ Unintended Acceleration          │
                │        (Top Event)               │
                └─────────────┬────────────────────┘
                              ⊃ OR
                 ┌────────────┼────────────┐
                 │            │            │
    ┌────────────┴──────┐ ┌──┴──────────┐ │
    │ Throttle stuck    │ │ ECU commands│ │
    │ open mechanically │ │ acceleration│ │
    └───────────────────┘ └──────┬──────┘ │
                                 ◇ AND     │
                          ┌──────┼──────┐  │
                          │      │      │  │
                   ┌──────┴─┐ ┌──┴────┐ │ │
                   │Software│ │Sensor │ │ │
                   │ fault  │ │ fault │ │ │
                   └────────┘ └───────┘ │ │
                      (○)        (○)     │ │
                   P=10⁻⁷     P=10⁻⁴    │ │
                                         │ │
              ┌──────────────────────────┘ │
              │                            │
    ┌─────────┴──────────┐   ┌─────────────┴──────────┐
    │ Pedal stuck        │   │ Cruise control         │
    │ (floor mat)        │   │ malfunction            │
    └────────────────────┘   └────────────────────────┘
           (○)                        (○)
        P=10⁻⁵                     P=10⁻⁶

**Probability Calculations:**

.. code-block:: python

    # Unintended acceleration FTA
    
    # Basic events
    P_throttle_stuck = 1e-5  # Mechanical jam
    P_software_fault = 1e-7  # ECU software bug
    P_sensor_fault = 1e-4    # Pedal position sensor
    P_pedal_stuck = 1e-5     # Floor mat interference
    P_cruise_fault = 1e-6    # Cruise control logic
    
    # Intermediate: ECU commands acceleration (AND gate)
    P_ecu_commands = P_software_fault * P_sensor_fault
    print(f"ECU commands unintended: {P_ecu_commands:.2e}")  # 1.00e-11
    
    # Top event (OR gate - rare event approximation)
    P_top = (P_throttle_stuck + P_ecu_commands + 
             P_pedal_stuck + P_cruise_fault)
    print(f"Unintended acceleration: {P_top:.2e}")  # 2.10e-05
    
    # Minimal Cut Sets
    MCS = [
        ('Throttle stuck', 1, P_throttle_stuck),
        ('Pedal stuck', 1, P_pedal_stuck),
        ('Cruise fault', 1, P_cruise_fault),
        ('Software AND Sensor', 2, P_ecu_commands)
    ]
    
    print("\nMinimal Cut Sets (ranked by criticality):")
    for mcs, order, prob in sorted(MCS, key=lambda x: -x[2]):
        print(f"  {mcs:25s} Order {order}  P={prob:.2e}")

**Output:**

.. code-block:: text

    ECU commands unintended: 1.00e-11
    Unintended acceleration: 2.10e-05
    
    Minimal Cut Sets (ranked by criticality):
      Throttle stuck            Order 1  P=1.00e-05
      Pedal stuck               Order 1  P=1.00e-05
      Cruise fault              Order 1  P=1.00e-06
      Software AND Sensor       Order 2  P=1.00e-11

**Safety Improvements:**

✅ **Eliminate MCS 1**: Add throttle return spring (redundant)  
✅ **Mitigate MCS 2**: Floor mat retention clips  
✅ **Mitigate MCS 3**: Independent cruise control monitoring  
✅ **MCS 4**: Already dual failure (acceptable)

════════════════════════════════════════════════════════════════════

📖 **6. FTA TOOLS & SOFTWARE**
══════════════════════════════

**6.1 Commercial FTA Tools**
----------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Key Features**           |
+======================+==================+============================+
| **OpenFTA**          | Open source      | Free, basic FTA            |
|                      | (Formal-safety.org)| Cut set analysis          |
+----------------------+------------------+----------------------------+
| **Relex Fault Tree** | Relyence (HBK)   | Monte Carlo, common cause  |
|                      |                  | failures                   |
+----------------------+------------------+----------------------------+
| **isograph           | isograph         | Event tree integration     |
| Reliability**        |                  | Dynamic FTA                |
| **Workbench**        |                  |                            |
+----------------------+------------------+----------------------------+
| **PTC Windchill**    | PTC              | FMEA/FTA integration       |
|                      |                  | PLM workflow               |
+----------------------+------------------+----------------------------+
| **Item ToolKit**     | Item Software    | ISO 26262, IEC 61508       |
|                      |                  | Automotive focus           |
+----------------------+------------------+----------------------------+

**6.2 Python FTA Library**
--------------------------

**Basic FTA Implementation:**

.. code-block:: python

    # fta_library.py
    
    from enum import Enum
    from typing import List, Set
    
    class GateType(Enum):
        AND = "AND"
        OR = "OR"
        NOT = "NOT"
    
    class Event:
        def __init__(self, name: str, probability: float = None):
            self.name = name
            self.probability = probability
        
        def __repr__(self):
            return f"Event('{self.name}', P={self.probability})"
    
    class Gate:
        def __init__(self, gate_type: GateType, inputs: List):
            self.gate_type = gate_type
            self.inputs = inputs
        
        def calculate_probability(self) -> float:
            """Calculate output probability based on inputs"""
            probs = [inp.calculate_probability() if isinstance(inp, Gate) 
                     else inp.probability 
                     for inp in self.inputs]
            
            if self.gate_type == GateType.AND:
                result = 1.0
                for p in probs:
                    result *= p
                return result
            
            elif self.gate_type == GateType.OR:
                # Exact formula: P(A∪B) = P(A) + P(B) - P(A)P(B)
                result = probs[0]
                for p in probs[1:]:
                    result = result + p - (result * p)
                return result
            
            elif self.gate_type == GateType.NOT:
                return 1.0 - probs[0]
        
        def find_minimal_cut_sets(self) -> List[Set[str]]:
            """Find minimal cut sets (simplified algorithm)"""
            # Recursive algorithm to find MCS
            # (Simplified - production code more complex)
            pass
    
    # Example usage
    if __name__ == "__main__":
        # Define basic events
        sensor_a = Event("Sensor_A_fails", 1e-3)
        sensor_b = Event("Sensor_B_fails", 1e-3)
        power = Event("Power_supply_fails", 1e-4)
        
        # Build fault tree
        # Top = (Sensor_A AND Sensor_B) OR Power
        sensor_system = Gate(GateType.AND, [sensor_a, sensor_b])
        top_event = Gate(GateType.OR, [sensor_system, power])
        
        # Calculate
        P_top = top_event.calculate_probability()
        print(f"Top event probability: {P_top:.6f}")
        
        # Expected: (1e-3 * 1e-3) + 1e-4 ≈ 1.01e-4

════════════════════════════════════════════════════════════════════

📖 **7. ADVANCED FTA CONCEPTS**
═══════════════════════════════

**7.1 Common Cause Failures (CCF)**
-----------------------------------

**Problem:** Independent failure assumption violated

**Example:**

.. code-block:: text

    Redundant sensors assumed independent:
    P(Both fail) = 10⁻³ × 10⁻³ = 10⁻⁶
    
    BUT: Common cause failures exist:
    - Same design flaw (software bug)
    - Same environmental stress (temperature)
    - Same manufacturing lot (defective batch)
    
    Reality: P(Both fail) = 10⁻⁶ + P_CCF
    
    If P_CCF = 10⁻⁴ → Dominates! (100× worse than calculated)

**Beta Factor Model (IEC 61508):**

.. code-block:: text

    β = Fraction of failures due to common cause
    
    P(Single fails) = (1-β) × λ
    P(Both fail CCF) = β × λ
    
    Example:
    - λ = 10⁻³ (total failure rate)
    - β = 0.1 (10% common cause)
    
    P(Independent) = (1-0.1)×10⁻³ = 9×10⁻⁴
    P(CCF) = 0.1×10⁻³ = 1×10⁻⁴
    
    P(Both fail) = 9×10⁻⁴ × 9×10⁻⁴ + 1×10⁻⁴ = 1.81×10⁻⁴
                   (independent)        (CCF)

**7.2 Dynamic Fault Trees**
---------------------------

**Standard FTA Limitation:** Static (no time/sequence)

**Dynamic Gates:**

- **PAND (Priority AND)**: Inputs must occur in order
- **SPARE**: Standby redundancy with switching
- **FDEP (Functional Dependency)**: Trigger causes cascading failures

**Example: Standby Redundancy**

.. code-block:: text

    Primary pump + Standby pump (auto-switchover)
    
    Standard FTA (incorrect):
    P(Both fail) = P_primary × P_standby
    
    Dynamic FTA (correct):
    P(Both fail) = P(Primary fails) × P(Switch fails OR Standby fails)
                 = 10⁻³ × (10⁻² + 10⁻³) ≈ 1.1×10⁻⁵

**7.3 Importance Measures**
---------------------------

**Ranking Basic Events by Criticality:**

1. **Fussell-Vesely Importance:**
   
   FV_i = P(Top | Event_i occurs) / P(Top)
   
   Measures: "How much does Event_i contribute to top event?"

2. **Birnbaum Importance:**
   
   B_i = ∂P(Top) / ∂P(Event_i)
   
   Measures: "Sensitivity of top event to Event_i probability"

3. **Risk Achievement Worth (RAW):**
   
   RAW_i = P(Top | Event_i certain) / P(Top)
   
   Measures: "How much worse if Event_i always occurs?"

**Example Calculation:**

.. code-block:: python

    # Importance measures
    
    import numpy as np
    
    # Baseline probabilities
    P_A = 1e-3
    P_B = 1e-3
    P_C = 1e-4
    
    # Top = (A AND B) OR C
    def calc_top(pA, pB, pC):
        return (pA * pB) + pC - (pA * pB * pC)
    
    P_top_baseline = calc_top(P_A, P_B, P_C)
    
    # Fussell-Vesely for C
    P_top_if_C = calc_top(P_A, P_B, 1.0)  # C occurs
    FV_C = P_top_if_C / P_top_baseline
    print(f"Fussell-Vesely (C): {FV_C:.2f}")  # Close to 1.0 (dominant)
    
    # Birnbaum for C (numerical derivative)
    epsilon = 1e-8
    P_top_plus = calc_top(P_A, P_B, P_C + epsilon)
    B_C = (P_top_plus - P_top_baseline) / epsilon
    print(f"Birnbaum (C): {B_C:.4f}")  # ≈1.0 (direct contribution)

════════════════════════════════════════════════════════════════════

📖 **8. FTA IN DIFFERENT DOMAINS**
══════════════════════════════════

**8.1 Automotive (ISO 26262)**
------------------------------

**Quantitative FTA Requirements:**

.. code-block:: text

    ISO 26262-10: Safety Analysis
    - FTA mandatory for ASIL C/D
    - Verify hardware metrics:
      * SPFM (Single Point Fault Metric) ≥ 90% (ASIL D)
      * LFM (Latent Fault Metric) ≥ 60% (ASIL D)
    
    Process:
    1. Start from ASIL-rated hazard (from HARA)
    2. Decompose to hardware failures
    3. Calculate PMHF (Probabilistic Metric for Hardware Failures)
    4. Verify PMHF < 10 FIT (10⁻⁸/hour) for ASIL D

**8.2 Aerospace (ARP4761)**
---------------------------

**Aircraft Safety Assessment:**

.. code-block:: text

    ARP4761 Process:
    1. FHA (Functional Hazard Assessment) → DAL assignment
    2. PSSA (Preliminary System Safety Assessment) → Early FTA
    3. SSA (System Safety Assessment) → Final FTA
    
    Requirements:
    - Catastrophic (DAL A): < 10⁻⁹ per flight hour
    - Hazardous (DAL B): < 10⁻⁷ per flight hour
    - Major (DAL C): < 10⁻⁵ per flight hour
    
    Example: Flight control failure
    - Top event: "Loss of flight control" (Catastrophic)
    - Target: < 10⁻⁹/hour
    - Typical approach: Triple redundancy + dissimilar architecture

**8.3 Nuclear (PRA)**
---------------------

**Probabilistic Risk Assessment:**

.. code-block:: text

    NRC Requirements:
    - Core damage frequency (CDF) < 10⁻⁴ per reactor-year
    - Large early release frequency (LERF) < 10⁻⁵ per reactor-year
    
    Methods:
    - Level 1 PRA: Core damage (FTA + Event Trees)
    - Level 2 PRA: Containment failure
    - Level 3 PRA: Off-site consequences
    
    Extensive use of:
    - Dynamic fault trees (thermal-hydraulics)
    - Human reliability analysis (HRA)
    - Common cause failure modeling

════════════════════════════════════════════════════════════════════

📝 **9. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between FTA and FMEA? When to use each?

**A1:**

- **FTA**: Top-down (start with hazard), deductive, "WHY did it happen?"
  - Use for: Accident investigation, complex interactions, verify redundancy
- **FMEA**: Bottom-up (start with component), inductive, "WHAT can go wrong?"
  - Use for: Design phase, systematic component analysis

────────────────────────────────────────────────────────────────────

**Q2:** Calculate: P(A OR B) where P(A)=0.001, P(B)=0.002. Independent events.

**A2:**

::

    Exact formula: P(A OR B) = P(A) + P(B) - P(A)×P(B)
    
    P = 0.001 + 0.002 - (0.001 × 0.002)
    P = 0.003 - 0.000002
    P = 0.002998 ≈ 0.003
    
    Rare event approximation (if P << 1):
    P ≈ 0.001 + 0.002 = 0.003 ✅ (error < 0.1%)

────────────────────────────────────────────────────────────────────

**Q3:** What is a Minimal Cut Set? Why important?

**A3:**

- **MCS**: Smallest combination of basic events causing top event
- **Importance**: 
  - Order 1 MCS = Single point of failure (CRITICAL)
  - Guides design improvements (eliminate SPOFs first)
  - Enables quantitative risk assessment

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Define top event (specific, undesired, observable)
- [ ] Identify immediate causes (AND/OR logic)
- [ ] Decompose recursively to basic events
- [ ] Draw fault tree using standard symbols
- [ ] Assign probabilities to basic events (data or estimates)
- [ ] Calculate intermediate and top event probabilities
- [ ] Find minimal cut sets (Boolean algebra)
- [ ] Rank MCS by criticality (order, probability)
- [ ] Consider common cause failures (Beta factor)
- [ ] Calculate importance measures (Fussell-Vesely, Birnbaum)
- [ ] Recommend design improvements (eliminate SPOFs)
- [ ] Document assumptions and data sources
- [ ] Review FTA with stakeholders
- [ ] Integrate with FMEA (cross-check)
- [ ] Update FTA as design evolves

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **FTA is top-down** → Starts with hazardous event, decomposes to root causes

2️⃣ **Boolean logic** → AND gates (all required), OR gates (any sufficient)

3️⃣ **Probability calculations** → P(AND)=P(A)×P(B), P(OR)=P(A)+P(B)-P(A)×P(B)

4️⃣ **Minimal Cut Sets** → Identify single points of failure (Order 1 = critical)

5️⃣ **Redundancy verification** → AND gates prove dual failure required (10⁻³×10⁻³=10⁻⁶)

6️⃣ **Common cause failures** → Beta factor accounts for shared failure modes

7️⃣ **Complementary to FMEA** → FTA for "why", FMEA for "what" (use both!)

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **FTA CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Definition, symbols, gates, construction process, MCS analysis,  
probability calculations, automotive/aerospace examples, tools, advanced concepts

════════════════════════════════════════════════════════════════════
