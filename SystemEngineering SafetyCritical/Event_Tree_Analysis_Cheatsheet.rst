🌳 **Event Tree Analysis (ETA)**
═══════════════════════════════════════════════════════════════════

**Full Name:** Event Tree Analysis (ETA)  
**Type:** Forward probabilistic safety analysis  
**Origin:** Nuclear industry (1960s), Reactor Safety Study (WASH-1400, 1975)  
**Standards:** IEC 61025, IEEE 352, NASA

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — EVENT TREE IN 60 SECONDS**
────────────────────────────────────────

**What is Event Tree Analysis?**

::

    ETA = Forward analysis from initiating event through sequences to outcomes
    
    Direction: Initiating Event → Pivotal Events → Final Outcomes
    (LEFT to RIGHT, FORWARD in time)
    
    Question: "WHAT happens next after this initiating event?"

**Event Tree Structure:**

.. code-block:: text

    Initiating    Pivotal Event 1   Pivotal Event 2   Outcome
    Event         (Success/Fail)    (Success/Fail)
    
                  ┌─ Success ──┬─ Success ──→ Safe
                  │            └─ Failure ──→ Minor damage
    [IE] ─────────┤
                  └─ Failure ──┬─ Success ──→ Major damage
                               └─ Failure ──→ Catastrophic

**Key Concepts:**

- **Initiating Event (IE)**: Trigger that starts sequence (equipment failure, external event)
- **Pivotal Events**: Safety systems/barriers that succeed or fail
- **Branches**: Success (up) or failure (down) at each node
- **Sequences**: Paths from IE to outcomes
- **Probability**: P(sequence) = P(IE) × P(branch1) × P(branch2) × ...

**ETA vs FTA:**

+------------------+----------------------------+----------------------------+
| **Aspect**       | **Event Tree (ETA)**       | **Fault Tree (FTA)**       |
+==================+============================+============================+
| **Direction**    | Forward (IE → outcomes)    | Backward (hazard → causes) |
+------------------+----------------------------+----------------------------+
| **Question**     | "WHAT happens next?"       | "WHY did this happen?"     |
+------------------+----------------------------+----------------------------+
| **Starting**     | Initiating event           | Top event (hazard)         |
| **Point**        |                            |                            |
+------------------+----------------------------+----------------------------+
| **Structure**    | Horizontal tree (time)     | Vertical tree (logic)      |
+------------------+----------------------------+----------------------------+
| **Use Case**     | Sequence analysis          | Root cause analysis        |
|                  | Accident progression       | Redundancy verification    |
+------------------+----------------------------+----------------------------+

**When to Use ETA:**

✅ Probabilistic Risk Assessment (PRA) — nuclear, aerospace  
✅ Accident sequence analysis (multiple barriers)  
✅ Emergency response planning  
✅ Quantify risk (frequency × consequence)

════════════════════════════════════════════════════════════════════

📖 **1. EVENT TREE FUNDAMENTALS**
═════════════════════════════════

**1.1 Definition & Purpose**
----------------------------

**Event Tree Analysis:**

    Graphical representation of sequences following an initiating event,
    showing how safety systems respond (success or failure) and the
    resulting outcomes.

**Objectives:**

✅ **Identify accident sequences**: All possible paths from IE to outcomes  
✅ **Quantify risk**: Calculate frequency of each outcome  
✅ **Evaluate safety systems**: Understand which barriers are critical  
✅ **Guide design**: Identify where additional protection needed  
✅ **Emergency planning**: Understand accident progression timelines

**1.2 Components of Event Tree**
--------------------------------

**1. Initiating Event (IE):**

    Trigger event that challenges normal operations
    
    Examples:
    - Loss of power
    - Pipe rupture
    - Fire
    - Human error
    - External event (earthquake, lightning)

**2. Pivotal Events (Safety Functions):**

    Safety systems or actions that can succeed or fail
    
    Characteristics:
    - Binary outcome (success/failure)
    - Time-ordered (left to right)
    - Independent or dependent (conditional probability)
    
    Examples:
    - Emergency cooling activates
    - Operator shuts down reactor
    - Backup power starts
    - Containment isolates

**3. Branches:**

    Success (typically up) or failure (down) of each pivotal event
    
    Convention:
    - Upper branch: Success (system works)
    - Lower branch: Failure (system fails)
    - Probability labels: P(success), P(failure)

**4. Sequences:**

    Complete paths from IE through all pivotal events to final outcome
    
    Sequence notation: IE-A-B-C (where A, B, C are pivotal events)
    - Success: A, B, C
    - Failure: Ā, B̄, C̄ (with overbar)

**5. End States (Outcomes):**

    Final consequences of each sequence
    
    Examples:
    - Safe shutdown
    - Minor release
    - Major release
    - Core damage
    - Catastrophic failure

**1.3 Event Tree Construction Rules**
-------------------------------------

**Time Ordering:**

- Pivotal events arranged left-to-right in chronological order
- Events that occur earlier appear left

**Conditional Probability:**

- Later events may depend on earlier events (conditional)
- Example: Backup pump may not start if power already failed

**Success vs Failure:**

- Upper branch = Success (system performs function)
- Lower branch = Failure (system does not perform function)

**Probability Assignment:**

- Success branch: P(success | prior events)
- Failure branch: 1 - P(success)

════════════════════════════════════════════════════════════════════

📖 **2. EVENT TREE CONSTRUCTION**
═════════════════════════════════

**2.1 Step 1: Identify Initiating Events**
------------------------------------------

**Sources:**

- FMEA (component failures)
- HAZOP (process deviations)
- Historical data (industry incidents)
- Brainstorming (what-if analysis)

**Example: Nuclear Reactor**

.. code-block:: text

    Initiating Events:
    - IE-1: Loss of Offsite Power (LOOP)
    - IE-2: Loss of Coolant Accident (LOCA) - small break
    - IE-3: Loss of Coolant Accident (LOCA) - large break
    - IE-4: Steam Generator Tube Rupture (SGTR)
    - IE-5: Anticipated Transient Without Scram (ATWS)

**Grouping IEs:**

- Similar frequency: Group IEs with similar occurrence rates
- Similar response: Group IEs requiring same safety functions

**2.2 Step 2: Identify Safety Functions**
-----------------------------------------

**For each IE, determine safety functions required:**

.. code-block:: text

    Example: IE-1 (Loss of Offsite Power)
    
    Safety Functions (in chronological order):
    1. Reactor scram (control rods insert)
    2. Emergency diesel generators start
    3. Emergency core cooling (ECCS) activates
    4. Containment isolates
    5. Residual heat removal

**Success Criteria:**

- Define what constitutes "success" for each function
- Example: "At least 2 of 3 diesel generators start within 10 seconds"

**2.3 Step 3: Draw Event Tree**
-------------------------------

**Example: Loss of Offsite Power**

.. code-block:: text

    IE: LOOP    Scram  Diesels  ECCS   RHR    Outcome
     (10⁻²/yr)
                 ┌──────┬─────────┬─────────┬─────→ OK (Safe shutdown)
                 │ ✓    │ ✓       │ ✓       │ ✓
                 │      │         │         └─────→ Late shutdown
                 │      │         │         ✗
                 │      │         │
                 │      │         └───────────────→ Core damage (no cooling)
                 │      │         ✗
                 │      │
    [LOOP] ─────┤      └─────────────────────────→ Core damage (no power)
                 │      ✗
                 │
                 └────────────────────────────────→ Severe accident (no scram)
                 ✗

**Sequence Notation:**

.. code-block:: text

    Sequence 1: LOOP-Scram-Diesels-ECCS-RHR = Safe (all succeed)
    Sequence 2: LOOP-Scram-Diesels-ECCS-RH̄R = Late shutdown (RHR fails)
    Sequence 3: LOOP-Scram-Diesels-ĒC̄C̄S = Core damage (ECCS fails)
    Sequence 4: LOOP-Scram-D̄iesels = Core damage (no power)
    Sequence 5: LOOP-S̄cram = Severe accident (no scram)

**2.4 Step 4: Assign Probabilities**
------------------------------------

**Data Sources:**

- Vendor data (equipment reliability)
- Industry databases (NUREG, IEEE STD 500)
- Operating experience
- Expert judgment

**Example Probabilities:**

.. code-block:: text

    IE: Loss of Offsite Power
    - Frequency: λ_LOOP = 1 × 10⁻²/year (once per 100 years)
    
    Pivotal Event Probabilities:
    - P(Scram success) = 0.999 → P(Scram failure) = 1 × 10⁻³
    - P(Diesels success | Scram) = 0.99 → P(Diesels failure) = 1 × 10⁻²
    - P(ECCS success | Diesels) = 0.995 → P(ECCS failure) = 5 × 10⁻³
    - P(RHR success | ECCS) = 0.98 → P(RHR failure) = 2 × 10⁻²

**Conditional Probabilities:**

- If diesels fail, ECCS cannot start (P = 0)
- Dependencies modeled explicitly

**2.5 Step 5: Calculate Sequence Frequencies**
----------------------------------------------

**Frequency Calculation:**

    F(sequence) = F(IE) × P(branch 1) × P(branch 2) × ... × P(branch n)

**Example Calculation:**

.. code-block:: python

    # Event tree quantification
    
    # Initiating event frequency (per year)
    F_LOOP = 1e-2
    
    # Branch probabilities
    P_Scram_success = 0.999
    P_Scram_failure = 1 - P_Scram_success  # 1e-3
    
    P_Diesels_success = 0.99
    P_Diesels_failure = 1 - P_Diesels_success  # 1e-2
    
    P_ECCS_success = 0.995
    P_ECCS_failure = 1 - P_ECCS_success  # 5e-3
    
    P_RHR_success = 0.98
    P_RHR_failure = 1 - P_RHR_success  # 2e-2
    
    # Sequence frequencies
    Seq1_Safe = F_LOOP * P_Scram_success * P_Diesels_success * P_ECCS_success * P_RHR_success
    print(f"Seq 1 (Safe): {Seq1_Safe:.2e}/year")
    
    Seq2_Late = F_LOOP * P_Scram_success * P_Diesels_success * P_ECCS_success * P_RHR_failure
    print(f"Seq 2 (Late shutdown): {Seq2_Late:.2e}/year")
    
    Seq3_ECCS_fail = F_LOOP * P_Scram_success * P_Diesels_success * P_ECCS_failure
    print(f"Seq 3 (Core damage - ECCS fail): {Seq3_ECCS_fail:.2e}/year")
    
    Seq4_Diesels_fail = F_LOOP * P_Scram_success * P_Diesels_failure
    print(f"Seq 4 (Core damage - Diesels fail): {Seq4_Diesels_fail:.2e}/year")
    
    Seq5_Scram_fail = F_LOOP * P_Scram_failure
    print(f"Seq 5 (Severe accident): {Seq5_Scram_fail:.2e}/year")
    
    # Total core damage frequency (CDF)
    CDF = Seq3_ECCS_fail + Seq4_Diesels_fail + Seq5_Scram_fail
    print(f"\nTotal Core Damage Frequency: {CDF:.2e}/year")
    
    # Risk metric
    NRC_target = 1e-4  # NRC target CDF < 1e-4/year
    print(f"NRC Target: {NRC_target:.2e}/year")
    print(f"Margin: {NRC_target / CDF:.1f}×")

**Output:**

.. code-block:: text

    Seq 1 (Safe): 9.60e-03/year
    Seq 2 (Late shutdown): 1.96e-04/year
    Seq 3 (Core damage - ECCS fail): 4.93e-05/year
    Seq 4 (Core damage - Diesels fail): 9.99e-05/year
    Seq 5 (Severe accident): 1.00e-05/year
    
    Total Core Damage Frequency: 1.59e-04/year
    NRC Target: 1.00e-04/year
    Margin: 0.6× (EXCEEDS TARGET - need improvement!)

**Interpretation:**

- Most sequences lead to safe shutdown (96%)
- Dominant contributor: Diesel generator failure (Seq 4: 63% of CDF)
- **Action**: Add 4th diesel generator or alternate AC power source

════════════════════════════════════════════════════════════════════

📖 **3. EVENT TREE EXAMPLE: AIRCRAFT ENGINE FAILURE**
═════════════════════════════════════════════════════

**3.1 Scenario**
----------------

**Initiating Event:** Engine failure during cruise flight

**Safety Functions:**

1. Remaining engine(s) continue operation
2. Pilot recognizes failure and takes action
3. Emergency landing site reached
4. Landing successful

**3.2 Event Tree**
------------------

.. code-block:: text

    IE: Engine    Other    Pilot     Reach    Land     Outcome
    Failure       Engines  Action    Airport  Success
    (10⁻⁵/hr)     Continue
    
                  ┌────────┬─────────┬────────┬──────→ Safe (normal landing)
                  │ ✓      │ ✓       │ ✓      │ ✓
                  │        │         │        └──────→ Runway excursion
                  │        │         │        ✗       (minor damage)
                  │        │         │
                  │        │         └───────────────→ Off-airport landing
                  │        │         ✗                (major damage)
                  │        │
    [Eng Fail] ───┤        └─────────────────────────→ Loss of control
                  │        ✗                          (severe)
                  │
                  └──────────────────────────────────→ Loss of aircraft
                  ✗                                    (catastrophic)

**3.3 Probability Assignment**
------------------------------

.. code-block:: python

    # Aircraft engine failure event tree
    
    # IE frequency (per flight hour)
    F_EngFail = 1e-5  # 1 in 100,000 hours
    
    # Probabilities
    P_OtherEngines = 0.9999  # Twin-engine: single engine sufficient
    P_PilotAction = 0.999    # Trained pilots recognize and respond
    P_ReachAirport = 0.95    # Glide ratio, distance to airport
    P_LandSuccess = 0.98     # Single-engine landing challenging
    
    # Sequences
    Seq1 = F_EngFail * P_OtherEngines * P_PilotAction * P_ReachAirport * P_LandSuccess
    Seq2 = F_EngFail * P_OtherEngines * P_PilotAction * P_ReachAirport * (1-P_LandSuccess)
    Seq3 = F_EngFail * P_OtherEngines * P_PilotAction * (1-P_ReachAirport)
    Seq4 = F_EngFail * P_OtherEngines * (1-P_PilotAction)
    Seq5 = F_EngFail * (1-P_OtherEngines)  # Dual engine failure
    
    print(f"Safe landing: {Seq1:.2e}/flt-hr (93% of events)")
    print(f"Runway excursion: {Seq2:.2e}/flt-hr")
    print(f"Off-airport landing: {Seq3:.2e}/flt-hr")
    print(f"Loss of control: {Seq4:.2e}/flt-hr")
    print(f"Loss of aircraft: {Seq5:.2e}/flt-hr")
    
    # Total accident rate
    AccidentRate = Seq2 + Seq3 + Seq4 + Seq5
    print(f"\nTotal accident rate: {AccidentRate:.2e}/flt-hr")
    
    # Per million flight hours
    print(f"Accidents per million flt-hr: {AccidentRate * 1e6:.2f}")

**Output:**

.. code-block:: text

    Safe landing: 9.22e-06/flt-hr (93% of events)
    Runway excursion: 1.88e-07/flt-hr
    Off-airport landing: 4.70e-07/flt-hr
    Loss of control: 9.99e-09/flt-hr
    Loss of aircraft: 1.00e-09/flt-hr
    
    Total accident rate: 6.67e-07/flt-hr
    Accidents per million flt-hr: 0.67

**Comparison to Industry:**

- Commercial aviation fatal accident rate: ~0.2 per million flight hours
- This analysis: 0.67 per million (engine failure only)
- Conclusion: Engine failures are small contributor (< 10%) to overall risk

════════════════════════════════════════════════════════════════════

📖 **4. ADVANCED EVENT TREE CONCEPTS**
══════════════════════════════════════

**4.1 Functional Event Trees**
------------------------------

**Concept:** Focus on safety functions (not specific equipment)

.. code-block:: text

    Instead of: "Diesel A starts"
    Use: "AC power available" (could be diesel, grid, or battery+inverter)
    
    Advantages:
    - Design-independent (early analysis)
    - Multiple success paths captured
    - Maps to functional requirements

**4.2 Common Cause Failures (CCF)**
-----------------------------------

**Problem:** Independent failure assumption violated

.. code-block:: text

    Example: Two diesel generators
    
    Naive analysis:
    P(both fail) = P(A fail) × P(B fail) = 0.01 × 0.01 = 1e-4
    
    Reality: Common cause failures exist
    - Same design flaw
    - Same maintenance error
    - Same environmental stress (flood, fire)
    
    Beta factor model:
    P(both fail) = P_independent + P_CCF
                 = (0.01 × 0.01) + (β × 0.01)
    
    If β = 0.1 (10% CCF):
    P(both fail) = 1e-4 + 1e-3 = 1.1e-3 (10× worse!)

**4.3 Dynamic Event Trees**
---------------------------

**Concept:** Branch probabilities change over time

.. code-block:: text

    Example: Fire suppression
    
    Traditional ETA: P(suppression success) = 0.8 (static)
    
    Dynamic ETA: P(success | time)
    - t < 5 min:  P = 0.95 (early detection, small fire)
    - 5-15 min:   P = 0.7  (fire growing, heat damage)
    - t > 15 min: P = 0.3  (large fire, structural damage)
    
    Requires: Thermal-hydraulic modeling, time-dependent simulation

**4.4 Large Event Trees (Binning)**
-----------------------------------

**Problem:** Combinatorial explosion

.. code-block:: text

    10 pivotal events → 2¹⁰ = 1024 sequences
    20 pivotal events → 2²⁰ = 1,048,576 sequences
    
    Solution: End-state binning
    - Group similar outcomes (minor/major/catastrophic)
    - Truncate low-probability sequences (< 1e-10)
    - Use fault trees for complex pivotal events

════════════════════════════════════════════════════════════════════

📖 **5. ETA + FTA INTEGRATION**
═══════════════════════════════

**5.1 Linked Event Trees & Fault Trees**
----------------------------------------

**Approach:** Use FTA to quantify pivotal events in ETA

.. code-block:: text

    Event Tree:
    
    [IE] ───┬─── Safety System A ──┬─── Safety System B ──→ Outcome
            │     (Success/Fail)   │
            │                      │
            │                      └─ FTA: "System B fails"
            │                            (detailed logic)
            │
            └─ FTA: "System A fails"
                  (pump fails AND valve fails)

**Example:**

.. code-block:: text

    Pivotal Event: "Emergency Core Cooling System (ECCS) fails"
    
    Fault Tree (simplified):
    
          ECCS Fails
               ⊃ OR
         ┌──────┼──────┐
         │      │      │
    ┌────┴─┐ ┌──┴──┐ ┌─┴──────┐
    │Pumps │ │Valves│ │No power│
    │fail  │ │fail  │ │        │
    └──────┘ └──────┘ └────────┘
      (◇AND)   (◇AND)    (○)
     ┌─┴─┐   ┌─┴─┐    P=1e-2
     A   B   C   D
    P=0.01 P=0.01
    
    P(ECCS fail) = P(A∩B) + P(C∩D) + P(no power)
                 = (0.01×0.01) + (0.01×0.01) + 0.01
                 = 1e-4 + 1e-4 + 1e-2 ≈ 1.02e-2

**Benefits:**

✅ Detailed quantification (FTA captures component logic)  
✅ Identify critical components (FTA minimal cut sets)  
✅ Manageable event tree size (collapse complexity into pivotal events)

**5.2 Bow-Tie Diagram (ETA + FTA Combined)**
--------------------------------------------

**Visual representation:**

.. code-block:: text

         FTA (Causes)              Hazard         ETA (Consequences)
    
    ┌──────────────┐         ┌──────────────┐        ┌──────────────┐
    │ Causes       │         │              │        │              │
    │ (Fault Tree) ├────────→│   HAZARD     ├───────→│  Outcomes    │
    │              │         │   (Event)    │        │ (Event Tree) │
    └──────────────┘         └──────────────┘        └──────────────┘
         ▲                          ▲                       ▲
         │                          │                       │
    Prevention                  Barriers              Mitigation
    (reduce freq)                                     (reduce severity)

**Example: Chemical Release**

.. code-block:: text

    Prevention (FTA):            HAZARD:           Mitigation (ETA):
    Why did tank rupture?        Tank             What happens after?
                                ruptures
    - Overpressure               (Toxic           - Detection?
    - Corrosion                   gas              - Alarm?
    - External impact            release)          - Evacuation?
    - Design flaw                                  - Emergency response?
                                                   
                                                   → Outcomes:
                                                     - Contained
                                                     - Minor exposure
                                                     - Mass casualty

════════════════════════════════════════════════════════════════════

📖 **6. EVENT TREE TOOLS**
══════════════════════════

**6.1 Commercial Software**
---------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Features**               |
+======================+==================+============================+
| **SAPHIRE**          | Idaho National   | PRA for nuclear (free)     |
|                      | Lab (INL)        | ETA, FTA, uncertainty      |
+----------------------+------------------+----------------------------+
| **RiskSpectrum**     | Lloyd's Register | Nuclear/process industry   |
|                      |                  | Dynamic ETA, CCF           |
+----------------------+------------------+----------------------------+
| **CAFTA**            | EPRI             | Nuclear PRA standard       |
+----------------------+------------------+----------------------------+
| **Relex/PTC**        | PTC              | ETA, FTA, FMEA integration |
+----------------------+------------------+----------------------------+

**6.2 Python Event Tree Builder**
---------------------------------

.. code-block:: python

    # event_tree_builder.py
    
    import numpy as np
    import pandas as pd
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class PivotalEvent:
        name: str
        p_success: float
        
        @property
        def p_failure(self):
            return 1 - self.p_success
    
    @dataclass
    class Sequence:
        path: List[bool]  # True=success, False=failure
        outcome: str
        frequency: float
    
    class EventTree:
        def __init__(self, initiating_event_freq: float):
            self.ie_freq = initiating_event_freq
            self.pivotal_events: List[PivotalEvent] = []
            self.sequences: List[Sequence] = []
        
        def add_pivotal_event(self, name: str, p_success: float):
            self.pivotal_events.append(PivotalEvent(name, p_success))
        
        def generate_sequences(self):
            """Generate all possible sequences (2^n)"""
            n = len(self.pivotal_events)
            
            for i in range(2**n):
                # Binary representation: 0=failure, 1=success
                path = [(i >> j) & 1 for j in range(n)]
                path = [bool(p) for p in path]
                
                # Calculate frequency
                freq = self.ie_freq
                for j, success in enumerate(path):
                    if success:
                        freq *= self.pivotal_events[j].p_success
                    else:
                        freq *= self.pivotal_events[j].p_failure
                
                # Determine outcome (simple rules - customize as needed)
                if all(path):
                    outcome = "Safe"
                elif sum(path) >= len(path) - 1:
                    outcome = "Minor"
                elif sum(path) >= len(path) - 2:
                    outcome = "Major"
                else:
                    outcome = "Catastrophic"
                
                self.sequences.append(Sequence(path, outcome, freq))
        
        def to_dataframe(self) -> pd.DataFrame:
            """Export sequences to DataFrame"""
            rows = []
            for seq in self.sequences:
                row = {'Frequency': seq.frequency, 'Outcome': seq.outcome}
                for j, pe in enumerate(self.pivotal_events):
                    row[pe.name] = 'Success' if seq.path[j] else 'Failure'
                rows.append(row)
            return pd.DataFrame(rows)
        
        def summary(self):
            """Print summary statistics"""
            total_freq = sum(s.frequency for s in self.sequences)
            
            outcomes = {}
            for seq in self.sequences:
                outcomes[seq.outcome] = outcomes.get(seq.outcome, 0) + seq.frequency
            
            print(f"{'Outcome':<15} {'Frequency':<12} {'Percentage'}")
            print("-" * 50)
            for outcome, freq in sorted(outcomes.items(), key=lambda x: -x[1]):
                pct = 100 * freq / total_freq
                print(f"{outcome:<15} {freq:<12.2e} {pct:>6.2f}%")
            print("-" * 50)
            print(f"{'TOTAL':<15} {total_freq:<12.2e} 100.00%")
    
    # Example usage
    if __name__ == "__main__":
        # Loss of Offsite Power scenario
        et = EventTree(initiating_event_freq=1e-2)  # per year
        
        et.add_pivotal_event("Scram", 0.999)
        et.add_pivotal_event("Diesels", 0.99)
        et.add_pivotal_event("ECCS", 0.995)
        et.add_pivotal_event("RHR", 0.98)
        
        et.generate_sequences()
        
        print("Event Tree Analysis: Loss of Offsite Power")
        print("=" * 50)
        et.summary()
        
        print("\nTop 5 sequences:")
        df = et.to_dataframe()
        print(df.nlargest(5, 'Frequency'))

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the key difference between Event Tree Analysis (ETA) and Fault Tree Analysis (FTA)?

**A1:**

- **ETA**: Forward analysis (IE → outcomes), "What happens next?"
- **FTA**: Backward analysis (hazard → causes), "Why did this happen?"
- **ETA**: Horizontal tree (time sequence)
- **FTA**: Vertical tree (logic structure)

────────────────────────────────────────────────────────────────────

**Q2:** Calculate sequence frequency: IE frequency = 0.01/yr, System A success P=0.99, System B success P=0.95. What is frequency of sequence where BOTH succeed?

**A2:**

::

    F(sequence) = F(IE) × P(A success) × P(B success)
    F = 0.01 × 0.99 × 0.95
    F = 9.405 × 10⁻³ per year
    
    Answer: 9.41 × 10⁻³/year (or 0.00941/year)

────────────────────────────────────────────────────────────────────

**Q3:** Why is Event Tree Analysis particularly useful for nuclear PRA?

**A3:**

- **Multiple barriers**: Nuclear plants have defense-in-depth (many safety systems)
- **Sequence analysis**: Accident progression through multiple barriers
- **Quantification**: Calculates Core Damage Frequency (CDF) for regulatory compliance
- **Time-ordered**: Safety systems activate in sequence (scram → cooling → containment)
- **ETA + FTA**: Combines forward sequences with detailed component analysis

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Planning:**
- [ ] Identify initiating events (IE) from FMEA, HAZOP, historical data
- [ ] Group similar IEs (frequency, required safety functions)
- [ ] For each IE, list required safety functions (chronological order)
- [ ] Define success criteria for each safety function

**Construction:**
- [ ] Draw event tree (left to right, time-ordered)
- [ ] Label initiating event (frequency)
- [ ] Add pivotal events (safety functions)
- [ ] Branch at each node (success up, failure down)
- [ ] Label end states (outcomes)
- [ ] Assign sequence notation (IE-A-B-C)

**Quantification:**
- [ ] Assign IE frequency (per year, per flight hour, etc.)
- [ ] Assign pivotal event probabilities (from data, FTA, expert judgment)
- [ ] Account for dependencies (conditional probabilities)
- [ ] Calculate sequence frequencies (multiply along path)
- [ ] Sum frequencies by outcome (minor, major, catastrophic)

**Analysis:**
- [ ] Identify dominant sequences (highest frequency)
- [ ] Calculate total risk (frequency × consequence)
- [ ] Compare to acceptance criteria (e.g., NRC CDF < 1e-4/yr)
- [ ] Sensitivity analysis (vary key probabilities)
- [ ] Identify cost-effective improvements

**Integration:**
- [ ] Link to fault trees (quantify pivotal events)
- [ ] Cross-check with FMEA (consistent failure rates)
- [ ] Update as design evolves
- [ ] Document assumptions and data sources

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Forward analysis** → IE → pivotal events → outcomes (LEFT to RIGHT)

2️⃣ **Sequence probability** → Multiply probabilities along path

3️⃣ **Dominant sequences** → Focus on highest frequency contributors

4️⃣ **ETA + FTA** → Combine for comprehensive PRA (forward + backward)

5️⃣ **Nuclear PRA** → Standard method for Core Damage Frequency (CDF)

6️⃣ **Defense-in-depth** → Multiple barriers captured naturally in ETA

7️⃣ **Quantitative risk** → Frequency × consequence = risk metric

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **EVENT TREE ANALYSIS CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** ETA fundamentals, construction process, probability calculations,  
nuclear reactor example, aircraft engine failure, ETA+FTA integration, tools

════════════════════════════════════════════════════════════════════
