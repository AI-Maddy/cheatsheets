👤 **Human Factors Safety — Preventing Human Error in Safety-Critical Systems**
═══════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for HFE in Aviation, Automotive, Medical, and Industrial Systems**  
**Domains:** Cockpit Design 🛫 | Driving Automation 🚗 | Medical Device UI 🏥 | Control Room 🏭  
**Standards:** DO-178C/DO-254 (HF) | ISO 26262-8 | IEC 62366 | MIL-STD-1472 | NUREG-0711  
**Methods:** SHERPA | CREAM | HTA | NASA-TLX | SAGAT | CRM

═══════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**Why Human Factors Matter for Safety:**

.. code-block:: text

   Human Error Statistics:
   ✈️ Aviation: 70-80% of accidents involve human error (NTSB data)
   🚗 Automotive: 94% of crashes involve human factors (NHTSA)
   🏥 Medical: 70% of adverse events related to human error (IOM report)
   ⚛️ Nuclear: Three Mile Island (1979), Chernobyl (1986) — human error
   
   Key Insight: You cannot eliminate humans from safety-critical systems,
                but you CAN design systems that are resilient to human error.

**Human Error Taxonomy (James Reason):**

.. code-block:: text

   ┌─ SLIPS ─────────────────────────────────────────────────────┐
   │ Execution Error: Correct intention, wrong action            │
   │ Example: Pilot selects wrong autopilot mode (muscle memory) │
   └──────────────────────────────────────────────────────────────┘
   
   ┌─ LAPSES ────────────────────────────────────────────────────┐
   │ Memory Error: Forget step in procedure                      │
   │ Example: Surgeon forgets to remove surgical instrument      │
   └──────────────────────────────────────────────────────────────┘
   
   ┌─ MISTAKES ──────────────────────────────────────────────────┐
   │ Planning Error: Wrong intention (misdiagnosis)              │
   │ Example: Doctor prescribes wrong drug (incorrect diagnosis) │
   └──────────────────────────────────────────────────────────────┘
   
   ┌─ VIOLATIONS ────────────────────────────────────────────────┐
   │ Intentional Deviation: Break rules (routine, situational)   │
   │ Example: Pilot disables safety system to meet schedule      │
   └──────────────────────────────────────────────────────────────┘

**Design Principles (Norman's Design of Everyday Things):**

.. code-block:: text

   1. Affordances: Design makes correct action obvious
      ✅ Good: Push bar on exit door (affords pushing)
      ❌ Bad: Handle on exit door that must be pushed (confusing)
   
   2. Constraints: Design prevents incorrect action
      ✅ Good: USB-C connector (can only insert one way)
      ❌ Bad: Multi-pin connector (wrong orientation damages device)
   
   3. Feedback: System confirms action was received
      ✅ Good: Button clicks, LED lights up
      ❌ Bad: Silent button (did it register?)
   
   4. Mapping: Control layout matches mental model
      ✅ Good: Stove controls arranged like burners
      ❌ Bad: Linear controls for 2×2 burner layout
   
   5. Consistency: Similar operations work the same way
      ✅ Good: All menus accessed the same way
      ❌ Bad: Each subsystem has different UI paradigm

**NASA Task Load Index (TLX) — Measure Cognitive Workload:**

+---------------------+--------------------------------------------------+
| Dimension           | Question                                         |
+=====================+==================================================+
| Mental Demand       | How much mental activity? (0=low, 100=high)     |
+---------------------+--------------------------------------------------+
| Physical Demand     | How much physical activity?                      |
+---------------------+--------------------------------------------------+
| Temporal Demand     | How much time pressure?                          |
+---------------------+--------------------------------------------------+
| Performance         | How successful were you? (0=perfect, 100=fail)  |
+---------------------+--------------------------------------------------+
| Effort              | How hard did you work?                           |
+---------------------+--------------------------------------------------+
| Frustration         | How stressed/annoyed?                            |
+---------------------+--------------------------------------------------+

**Scoring:** Average of 6 dimensions → Overall workload (0-100)
**Target:** < 50 for safety-critical tasks (avoid overload)

═══════════════════════════════════════════════════════════════════════════════

📖 **1. HUMAN ERROR MODELS**
═══════════════════════════════════════════════════════════════════════════════

1.1 Swiss Cheese Model (James Reason)
--------------------------------------

**Concept:** Multiple defensive layers, each with holes (weaknesses)

.. code-block:: text

   Accident occurs when holes align (multiple failures):
   
   Layer 1: Organizational Influences (management, safety culture)
      Hole: Cost pressure → Skip maintenance
   
   Layer 2: Unsafe Supervision (training, procedures)
      Hole: Inadequate training on new system
   
   Layer 3: Preconditions (fatigue, stress, communication)
      Hole: Crew fatigued (worked 12-hour shift)
   
   Layer 4: Unsafe Acts (slips, mistakes, violations)
      Hole: Pilot misinterprets instrument reading
   
   ┌────────────────────────────────────────────────┐
   │   🧀        🧀        🧀        🧀            │
   │ ╱ ╲      ╱ ╲      ╱ ╲      ╱ ╲             │
   │ │ ○│  →  │ ○│  →  │ ○│  →  │ ○│  → Accident│
   │ ╲ ╱      ╲ ╱      ╲ ╱      ╲ ╱             │
   │   ▼        ▼        ▼        ▼              │
   │  Org    Supervision Precond  Act             │
   └────────────────────────────────────────────────┘
   
   All holes align → Hazard passes through → Accident

**Defense:** Add layers, reduce hole size (redundancy, training, procedures)

────────────────────────────────────────────────────────────────────────────

**1.2 SHELL Model (Aviation)**
------------------------------

**Components:**

.. code-block:: text

   S = Software (procedures, checklists, manuals)
   H = Hardware (aircraft, controls, instruments)
   E = Environment (weather, ATC, airports)
   L = Liveware (other humans: crew, ATC, maintenance)
   L = Liveware (center) = PILOT
   
        ┌─────────┐
        │Software │
        └────┬────┘
             │
   ┌─────┬───┴───┬─────┐
   │Liveware│ L │Liveware│
   │(others)│   │(self) │
   └─────┴───┬───┴─────┘
             │
        ┌────┴────┐
        │Hardware │
        └────┬────┘
             │
        ┌────┴─────┐
        │Environment│
        └──────────┘

**Interfaces (Where Errors Occur):**

.. code-block:: text

   L-H (Liveware-Hardware):
   - Cockpit design (can pilot reach controls?)
   - Display readability (glare, font size)
   - Control sensitivity (too sensitive = overcontrol)
   
   L-S (Liveware-Software):
   - Checklist usability (clear steps?)
   - Procedure ambiguity (confusing wording)
   
   L-L (Liveware-Liveware):
   - Crew resource management (communication, authority gradient)
   - Handoff errors (shift change in control room)
   
   L-E (Liveware-Environment):
   - Noise, lighting, temperature (distraction)
   - Time pressure (rushing leads to mistakes)

────────────────────────────────────────────────────────────────────────────

**1.3 CREAM (Cognitive Reliability and Error Analysis Method)**
---------------------------------------------------------------

**Purpose:** Classify cognitive failures

**Common Performance Conditions (CPCs):**

.. code-block:: text

   Factors affecting human reliability:
   
   1. Adequacy of organization (procedures, training)
   2. Working conditions (noise, lighting, space)
   3. Adequacy of MMI (human-machine interface)
   4. Availability of procedures
   5. Number of simultaneous goals (multitasking)
   6. Available time (time pressure)
   7. Time of day (circadian rhythm, fatigue)
   8. Adequacy of training
   9. Crew collaboration quality

**Error Modes:**

.. code-block:: text

   - Observation: Fail to detect signal (missed alarm)
   - Interpretation: Misunderstand information (wrong diagnosis)
   - Planning: Wrong decision (incorrect procedure)
   - Execution: Correct plan, wrong action (slip)

═══════════════════════════════════════════════════════════════════════════════

📖 **2. HUMAN ERROR PREDICTION: SHERPA**
═══════════════════════════════════════════════════════════════════════════════

2.1 SHERPA Method (Systematic Human Error Reduction and Prediction Approach)
-----------------------------------------------------------------------------

**Process:**

.. code-block:: text

   Step 1: Hierarchical Task Analysis (HTA)
   - Break task into subtasks (goals, operations, plans)
   
   Step 2: Task Classification
   - Classify each operation by type (action, retrieval, checking, etc.)
   
   Step 3: Error Identification
   - For each operation, identify credible errors
   
   Step 4: Consequence Analysis
   - Determine effect of each error
   
   Step 5: Recovery Analysis
   - Can error be detected and corrected?
   
   Step 6: Remediation
   - Design mitigations (training, procedures, automation)

────────────────────────────────────────────────────────────────────────────

**2.2 Example: Medical Infusion Pump Programming**
--------------------------------------------------

**Hierarchical Task Analysis:**

.. code-block:: text

   Goal: Set up intravenous drug infusion
   
   Plan: Do 1, then 2, then 3, then 4
   
   1. Select drug from library
      1.1 Navigate menu
      1.2 Confirm selection
   
   2. Enter dose (mg/kg/hr)
      2.1 Enter patient weight (kg)
      2.2 Enter dosage rate (mg/kg/hr)
      2.3 Confirm entry
   
   3. Set volume to be infused (mL)
      3.1 Calculate volume
      3.2 Enter volume
      3.3 Confirm
   
   4. Start infusion
      4.1 Press START button
      4.2 Verify infusion started (check display, listen for pump)

**SHERPA Error Analysis:**

+------------+------------------+-----------------+------------------+----------+
| Task Step  | Error Type       | Error           | Consequence      | Recovery |
+============+==================+=================+==================+==========+
| 1.2        | Action (A3)      | Select wrong    | Wrong drug       | Check    |
|            | wrong action on  | drug from list  | infused          | label    |
|            | right object     |                 | (potentially     | before   |
|            |                  |                 | fatal)           | start    |
+------------+------------------+-----------------+------------------+----------+
| 2.2        | Action (A6)      | Enter 10 instead| 10× overdose     | Confirm  |
|            | wrong action     | of 1.0 (decimal | (CRITICAL)       | dose     |
|            |                  | point error)    |                  | on       |
|            |                  |                 |                  | screen   |
+------------+------------------+-----------------+------------------+----------+
| 2.3        | Checking (C1)    | Fail to verify  | Incorrect dose   | Alarm if |
|            | check omitted    | displayed dose  | proceeds         | dose > 2×|
|            |                  |                 |                  | typical  |
+------------+------------------+-----------------+------------------+----------+
| 4.2        | Checking (C1)    | Assume pump     | Pump malfunction | Visual + |
|            | check omitted    | started (don't  | not detected     | audible  |
|            |                  | verify)         |                  | feedback |
+------------+------------------+-----------------+------------------+----------+

**Mitigations (IEC 62366 - Medical Device Usability):**

.. code-block:: text

   Error 1 (Wrong drug):
   ✅ Drug names with similar spelling displayed differently (color, font)
   ✅ Confirmation screen shows drug name + concentration
   ✅ Barcode scan (match drug vial to selection)
   
   Error 2 (Decimal point error):
   ✅ Soft limit: Alarm if dose > 2× typical dose for drug
   ✅ Hard limit: Reject dose > 10× typical dose (cannot override)
   ✅ Graphical display: Show infusion rate as bar chart (visual check)
   
   Error 3 (Skip verification):
   ✅ Require confirmation (cannot proceed without pressing "Confirm")
   ✅ Display dose in multiple units (mg/hr AND mg/kg/hr)
   
   Error 4 (Assume started):
   ✅ Audible beep when infusion starts
   ✅ Green LED + "INFUSING" message on screen
   ✅ Automatic occlusion detection (alarm if pump stalled)

═══════════════════════════════════════════════════════════════════════════════

📖 **3. SITUATIONAL AWARENESS**
═══════════════════════════════════════════════════════════════════════════════

3.1 Endsley Model (3 Levels of SA)
-----------------------------------

**Level 1: Perception**
- Detect relevant information in environment

.. code-block:: text

   Example (Aviation):
   ✅ Pilot sees altitude on display: 5,000 feet
   ✅ Pilot hears ATC clearance: "Descend to 3,000 feet"

**Level 2: Comprehension**
- Understand meaning of information

.. code-block:: text

   ✅ Pilot comprehends: "I am at 5,000 ft, need to descend to 3,000 ft"
   ✅ Pilot understands: "Currently 2,000 feet above target altitude"

**Level 3: Projection**
- Predict future states

.. code-block:: text

   ✅ Pilot projects: "At current descent rate (500 ft/min), will reach
                       3,000 ft in 4 minutes"
   ✅ Pilot anticipates: "Need to level off before overshooting"

**Loss of SA → Accidents:**

.. code-block:: text

   Level 1 Failure (Perception):
   - Alarm missed (too many alarms, alarm fatigue)
   - Display obscured (sun glare, broken instrument)
   
   Level 2 Failure (Comprehension):
   - Misinterpret display (mode confusion)
   - Incorrect mental model (wrong understanding of system)
   
   Level 3 Failure (Projection):
   - Fail to anticipate future state (slow response to trend)
   - Complacency (assume automation handling it)

────────────────────────────────────────────────────────────────────────────

**3.2 SA Measurement: SAGAT (Situation Awareness Global Assessment Technique)**
-------------------------------------------------------------------------------

**Method:**

.. code-block:: text

   1. Freeze simulation at random time
   2. Blank all displays
   3. Ask operator questions about situation (from memory)
   
   Questions (Aviation Example):
   - What is your current altitude? (Level 1: Perception)
   - How far are you from destination? (Level 2: Comprehension)
   - Will you reach destination before fuel reserve limit? (Level 3: Projection)
   
   Scoring: % correct answers = SA score

**Design Implications:**

.. code-block:: text

   Low SAGAT Score → Redesign Interface:
   ✅ Improve information salience (critical data more prominent)
   ✅ Integrate related data (fuel remaining + time to destination on same display)
   ✅ Trend indicators (show direction of change, not just current value)

────────────────────────────────────────────────────────────────────────────

**3.3 Mode Confusion (Automation Surprises)**
---------------------------------------------

**Problem:** Operator loses track of automation mode

**Example: Airbus A320 Flight Mode Confusion**

.. code-block:: text

   Scenario: Pilots intend to descend at 3,000 ft/min vertical speed
   
   Action: Set autopilot to "3000" (intending vertical speed mode)
   
   Actual Mode: Autopilot interprets as altitude target (3,000 feet)
   
   Result: Aircraft levels off at 3,000 feet (NOT descending at 3,000 ft/min)
   
   Accident: Pilots don't notice mode mismatch → Crash into terrain (multiple incidents)

**Mitigations:**

.. code-block:: text

   ✅ Mode annunciators: Large, clear display of active mode
   ✅ Mode transitions: Announce mode changes (audio callout)
   ✅ Mode reversion: Warn if unexpected mode change (e.g., autopilot disconnect)
   ✅ Consistent mode logic: Minimize number of modes, predictable transitions

**ISO 26262-8 (Automotive HMI):**

.. code-block:: text

   Requirement: Driver shall be aware of automation level at all times
   
   SAE Levels:
   - Level 0: No automation (driver fully in control)
   - Level 1: Assistance (e.g., adaptive cruise control)
   - Level 2: Partial automation (e.g., lane keeping + ACC)
   - Level 3: Conditional automation (driver must take over on request)
   - Level 4: High automation (no driver intervention needed in defined scenarios)
   
   Critical Transition: Level 3 → Level 0 (automation requests driver takeover)
   
   Design: Visual + audible + haptic alerts (steering wheel vibration)
           Escalating urgency if driver doesn't respond

═══════════════════════════════════════════════════════════════════════════════

📖 **4. COGNITIVE WORKLOAD**
═══════════════════════════════════════════════════════════════════════════════

4.1 Workload-Performance Relationship
--------------------------------------

**Inverted-U Curve (Yerkes-Dodson Law):**

.. code-block:: text

          Performance
              ▲
         High │     ┌───────┐  Optimal Zone
              │    ╱         ╲
              │   ╱           ╲
              │  ╱             ╲
              │ ╱               ╲
         Low  │╱                 ╲
              └─────────────────────────►
              Low   Moderate   High   Workload
              
              Under-         Optimal      Over-
              loaded                      loaded

**Implications:**

.. code-block:: text

   Underload (Boredom):
   - Vigilance decrement (fail to detect events)
   - Example: Autopilot monitoring (pilot bored → misses alarm)
   
   Optimal Load:
   - Peak performance, high engagement
   
   Overload (Stress):
   - Tunnel vision (focus on one task, miss others)
   - Increased errors (rushing, skipping steps)
   - Example: Emergency situation (multiple alarms, time pressure)

────────────────────────────────────────────────────────────────────────────

**4.2 NASA-TLX Workload Assessment**
------------------------------------

**Procedure:**

.. code-block:: text

   1. Perform task
   2. Rate 6 dimensions (0-100 scale):
      - Mental Demand: How much thinking/deciding?
      - Physical Demand: How much physical activity?
      - Temporal Demand: How much time pressure?
      - Performance: How successful? (0=perfect, 100=failure)
      - Effort: How hard did you work?
      - Frustration: How stressed/annoyed?
   
   3. Calculate overall workload:
      TLX Score = (Mental + Physical + Temporal + (100-Performance) + Effort + Frustration) / 6

**Example: Emergency Landing**

.. code-block:: text

   Mental Demand:    90  (high: multiple decisions, checklist)
   Physical Demand:  60  (moderate: control inputs, switches)
   Temporal Demand:  95  (very high: limited time before impact)
   Performance:      30  (successful landing = 70/100 = 30 failure score)
   Effort:           85  (very high: maximum concentration)
   Frustration:      75  (high: stress, uncertainty)
   
   TLX Score = (90+60+95+30+85+75) / 6 = 72.5
   
   Interpretation: Very high workload (>70), risk of errors

**Design Goal:** TLX < 50 for routine tasks, < 70 for emergency tasks

────────────────────────────────────────────────────────────────────────────

**4.3 Workload Reduction Strategies**
-------------------------------------

**Automation (Careful!):**

.. code-block:: text

   ✅ Good automation: Reduces routine workload, frees operator for supervision
   ❌ Bad automation: Operator out of loop, skill degradation, mode confusion
   
   Example (Automotive):
   ✅ Adaptive cruise control (ACC): Reduces workload on highway
   ❌ Full self-driving (Level 5 promise): Operator not ready for emergency takeover

**Task Shedding:**

.. code-block:: text

   During high workload, defer non-critical tasks
   
   Example (Aviation):
   Normal: Pilot navigates, communicates with ATC, monitors weather
   Emergency: Pilot focuses ONLY on flying, co-pilot handles communication

**Checklists:**

.. code-block:: text

   Offload memory to external aid (reduce lapse errors)
   
   Design:
   ✅ Short (< 10 items per page)
   ✅ Action-oriented ("Set flaps to 15°", not "Check flaps")
   ✅ Normal vs Emergency (different format, color)

═══════════════════════════════════════════════════════════════════════════════

📖 **5. CREW RESOURCE MANAGEMENT (CRM)**
═══════════════════════════════════════════════════════════════════════════════

5.1 Principles
--------------

**Goal:** Effective team coordination in safety-critical operations

**Core Concepts:**

.. code-block:: text

   1. Communication:
      - Closed-loop: "Set flaps 15" → "Flaps 15, set" (acknowledge + read-back)
      - Assertiveness: Junior crew speaks up if sees error
      - Graded assertiveness: Escalate if ignored (hint → suggest → demand)
   
   2. Decision Making:
      - Shared mental model (all crew understand situation)
      - Situational awareness (maintain SA of all crew)
   
   3. Workload Management:
      - Task delegation (don't overload captain)
      - Mutual monitoring (cross-check each other)
   
   4. Error Management:
      - Catch errors early (challenge assumptions)
      - Recover from errors (don't hide mistakes)

────────────────────────────────────────────────────────────────────────────

**5.2 Authority Gradient**
--------------------------

**Problem:** Junior crew hesitant to question senior authority

**Accidents Due to Steep Gradient:**

.. code-block:: text

   Korean Air Flight 801 (1997):
   - Captain making errors (fatigue, weather)
   - First officer noticed but didn't speak up strongly
   - Crash killed 228 people
   
   Root Cause: Cultural deference to authority (steep gradient)

**Solution: Flatten Gradient**

.. code-block:: text

   Training:
   ✅ Assertiveness training for junior crew
   ✅ Receptiveness training for senior crew ("I might be wrong, speak up!")
   ✅ Role-playing scenarios (practice challenging captain)
   
   Procedures:
   ✅ Standard callouts (first officer MUST call out deviations, not optional)
   ✅ Two-person rule (critical decisions require agreement)

────────────────────────────────────────────────────────────────────────────

**5.3 Graded Assertiveness (PACE)**
-----------------------------------

**Technique:** Escalate challenge if ignored

.. code-block:: text

   P = Probe:     "Captain, what's our altitude?" (soft hint)
   A = Alert:     "Captain, we're at 800 feet, should be 1,500" (direct observation)
   C = Challenge: "Captain, we need to climb NOW" (assertive)
   E = Emergency: "I'M TAKING OVER" (forceful intervention)

**Example:**

.. code-block:: text

   Scenario: Captain descending below safe altitude
   
   First Officer:
   1. Probe: "Captain, what altitude did ATC clear us to?" (hint: check altitude)
   2. Alert: "We're at 1,200 feet, clearance was 2,000" (state problem)
   3. Challenge: "We need to climb back to 2,000 immediately" (demand action)
   4. Emergency: "CLIMB! PULL UP!" (take control if no response)

═══════════════════════════════════════════════════════════════════════════════

📖 **6. DESIGN FOR HUMAN FACTORS**
═══════════════════════════════════════════════════════════════════════════════

6.1 Anthropometry (MIL-STD-1472)
---------------------------------

**Principle:** Design for range of human sizes (5th to 95th percentile)

**Examples:**

.. code-block:: text

   Reach Distance:
   - 5th percentile female: 25.5 inches
   - 95th percentile male: 32.0 inches
   Design: Emergency controls within 25.5 inches of seat

   Eye Height (seated):
   - 5th percentile female: 28.9 inches
   - 95th percentile male: 36.7 inches
   Design: Displays visible from 28.9 to 36.7 inches

────────────────────────────────────────────────────────────────────────────

**6.2 Display Design**
----------------------

**Principles:**

.. code-block:: text

   1. Proximity Compatibility:
      - Related information grouped together
      - Example: Fuel quantity + fuel flow on same display
   
   2. Moving Part vs Moving Scale:
      ✅ Moving pointer (altimeter needle): Shows rate of change
      ❌ Moving scale (digital counter): Hard to see trend
   
   3. Redundancy Coding:
      ✅ Critical information in multiple formats (color + shape + text)
      - Example: Red flashing "ENGINE FIRE" (color + text + flashing)
   
   4. Salience:
      - Critical information larger, brighter, centered
      - Example: Airspeed in center of display, large font

**Color Coding:**

+--------+------------------+---------------------------+
| Color  | Meaning          | Example                   |
+========+==================+===========================+
| Red    | Danger, stop     | Engine fire, overspeed    |
+--------+------------------+---------------------------+
| Yellow | Caution, warning | Low fuel, hydraulic press |
+--------+------------------+---------------------------+
| Green  | Normal, OK       | System operational        |
+--------+------------------+---------------------------+
| Blue   | Advisory, info   | Autopilot engaged         |
+--------+------------------+---------------------------+

────────────────────────────────────────────────────────────────────────────

**6.3 Control Design**
----------------------

**Principles:**

.. code-block:: text

   1. Mapping: Control motion matches expected result
      ✅ Good: Turn wheel right → Vehicle turns right
      ❌ Bad: Inverted controls (counterintuitive)
   
   2. Coding: Controls distinguishable by touch (shape, texture, size)
      ✅ Good: Landing gear lever shaped like wheel, flap lever like airfoil
      ❌ Bad: All levers identical (must look to identify)
   
   3. Guards: Critical controls protected from accidental activation
      ✅ Good: Engine shutdown button has flip-up cover
      ❌ Bad: Shutdown button next to start button (no guard)

═══════════════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═══════════════════════════════════════════════════════════════════════════════

**Q1:** Explain the four types of human error (slips, lapses, mistakes, violations) with examples.

**A1:**

.. code-block:: text

   1. SLIPS (Execution Error):
      - Correct intention, wrong action
      - Cause: Inattention, muscle memory
      - Example: Pilot intends to select autopilot ALT HOLD mode,
                 but presses ALT SEL instead (adjacent button)
      - Mitigation: Physical separation of controls, confirmation prompts
   
   2. LAPSES (Memory Error):
      - Forget step in procedure
      - Cause: Working memory overload, interruption
      - Example: Surgeon forgets to remove surgical sponge before closing
      - Mitigation: Checklists, count procedures (sponge count)
   
   3. MISTAKES (Planning Error):
      - Wrong intention (incorrect understanding)
      - Cause: Misdiagnosis, wrong mental model
      - Example: Pilot believes they are in DESCENT mode, but autopilot
                 is in LEVEL mode → Flies into terrain
      - Mitigation: Mode annunciators, training, cross-checks
   
   4. VIOLATIONS (Intentional Deviation):
      - Deliberate rule-breaking
      - Types:
        - Routine: Habitual shortcuts ("I always do it this way")
        - Situational: Respond to circumstances (time pressure)
        - Exceptional: Rare, intentional sabotage
      - Example: Pilot disables terrain warning system (annoying false alarms)
      - Mitigation: Safety culture, reporting systems, remove incentives
                     to violate (e.g., don't punish delays for following procedure)

────────────────────────────────────────────────────────────────────────────

**Q2:** What is SHERPA and how is it used for human error prediction?

**A2:**

**SHERPA = Systematic Human Error Reduction and Prediction Approach**

**Process:**

.. code-block:: text

   Step 1: Hierarchical Task Analysis (HTA)
   - Break task into subtasks (goals → operations → plans)
   
   Step 2: Classify Tasks
   - Action (A): Physical action
   - Retrieval (R): Information retrieval
   - Checking (C): Verification
   - Selection (S): Choose option
   - Information Communication (I): Transmit info
   
   Step 3: Identify Credible Errors
   - For each operation, ask "What could go wrong?"
   - Example: Action → Wrong action on right object (A3)
   
   Step 4: Consequence Analysis
   - What happens if error occurs?
   - Example: Wrong drug selected → Patient receives wrong medication
   
   Step 5: Recovery Analysis
   - Can error be detected/corrected before consequence?
   - Example: Barcode scan catches wrong drug selection
   
   Step 6: Design Mitigations
   - Eliminate error (design out possibility)
   - Detect error (alarms, checks)
   - Reduce consequence (fail-safe)

**Example Output (Partial SHERPA Table):**

+----------+------------+-----------------+---------------+-----------+
| Task     | Error Type | Error           | Consequence   | Mitigation|
+==========+============+=================+===============+===========+
| Select   | A3 (wrong  | Select morphine | Wrong drug    | Barcode   |
| drug     | action on  | instead of      | (potentially  | scan      |
|          | right obj) | midazolam       | fatal)        | required  |
+----------+------------+-----------------+---------------+-----------+

────────────────────────────────────────────────────────────────────────────

**Q3:** Describe Endsley's 3-level model of situational awareness with aviation examples.

**A3:**

**Level 1: Perception** (Detect information)

.. code-block:: text

   Example: Pilot sees altimeter: 10,000 feet
            Pilot hears ATC: "Descend and maintain 5,000 feet"
   
   Failure: Alarm missed, display obscured by sun glare

**Level 2: Comprehension** (Understand meaning)

.. code-block:: text

   Example: Pilot understands: "I am at 10,000 ft, cleared to 5,000 ft"
            "I need to descend 5,000 feet"
   
   Failure: Mode confusion (pilot thinks autopilot is descending, but it's not)

**Level 3: Projection** (Predict future)

.. code-block:: text

   Example: Pilot projects: "At current descent rate (1,000 ft/min),
                             will reach 5,000 ft in 5 minutes"
            "Terrain ahead at 4,500 ft, safe clearance"
   
   Failure: Fail to anticipate slow descent rate → miss altitude restriction

**SA Loss → Accident Example:**

.. code-block:: text

   Controlled Flight Into Terrain (CFIT):
   - Level 1 OK: Pilot sees altitude, terrain warnings
   - Level 2 FAIL: Pilot misinterprets altitude (thinks it's above terrain)
   - Level 3 FAIL: Doesn't project collision with terrain
   Result: Crash despite functional instruments

────────────────────────────────────────────────────────────────────────────

**Q4:** Explain NASA-TLX and how it measures cognitive workload.

**A4:**

**NASA Task Load Index (TLX):**

**Six Dimensions (0-100 scale):**

.. code-block:: text

   1. Mental Demand: How much thinking/deciding required?
   2. Physical Demand: How much physical activity?
   3. Temporal Demand: How much time pressure?
   4. Performance: How successful? (0=perfect, 100=failure)
   5. Effort: How hard did you work?
   6. Frustration: How stressed/annoyed?

**Scoring:**

.. code-block:: text

   TLX Score = Average of 6 dimensions
   
   Interpretation:
   < 30: Low workload (risk of underload, boredom)
   30-50: Optimal workload
   50-70: High workload (increased error risk)
   > 70: Very high workload (unsustainable, high error rate)

**Example: Medical Device Programming**

.. code-block:: text

   Scenario: Nurse programs IV infusion pump during emergency
   
   Mental Demand:    80  (calculate dose, check drug interaction)
   Physical Demand:  40  (button presses, minimal physical effort)
   Temporal Demand:  90  (patient crashing, extreme time pressure)
   Performance:      20  (successful setup, 80/100 = 20 on failure scale)
   Effort:           75  (maximum concentration)
   Frustration:      70  (confusing UI, multiple confirmation steps)
   
   TLX = (80+40+90+20+75+70) / 6 = 62.5
   
   Conclusion: High workload (>60), redesign UI to reduce steps

**Design Action:** Simplify programming (drug library with pre-set doses)

────────────────────────────────────────────────────────────────────────────

**Q5:** What is Crew Resource Management (CRM) and why is authority gradient important?

**A5:**

**CRM = Crew Resource Management**

.. code-block:: text

   Goal: Effective team coordination in safety-critical operations
   
   Core Principles:
   1. Communication: Closed-loop, assertiveness, graded escalation
   2. Decision Making: Shared mental model, consensus
   3. Workload Management: Delegation, mutual monitoring
   4. Error Management: Speak up, challenge assumptions

**Authority Gradient:**

.. code-block:: text

   Definition: Power difference between senior and junior crew
   
   ┌─ STEEP GRADIENT (Bad) ─────────────────────┐
   │ Captain: High authority, unchallenged      │
   │ First Officer: Hesitant to speak up        │
   │ Result: Junior crew sees error but doesn't │
   │         challenge captain → Accident       │
   └────────────────────────────────────────────┘
   
   ┌─ FLAT GRADIENT (Good) ─────────────────────┐
   │ Captain: Open to input, "I might be wrong" │
   │ First Officer: Confident to challenge      │
   │ Result: Errors caught by team monitoring   │
   └────────────────────────────────────────────┘

**Real Accident Example:**

.. code-block:: text

   Korean Air Flight 801 (1997):
   - Captain making navigation errors (fatigue)
   - First officer noticed but used indirect language ("Don't you think...")
   - Captain didn't respond, continued approach
   - Crash into terrain, 228 fatalities
   
   Root Cause: Steep authority gradient (cultural deference)

**Solution: PACE (Graded Assertiveness):**

.. code-block:: text

   P = Probe:     "Captain, what's our altitude target?" (soft hint)
   A = Alert:     "We're at 500 feet, should be 1,500" (direct fact)
   C = Challenge: "We need to climb NOW" (demand action)
   E = Emergency: "I'm taking control" (forceful intervention)

═══════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Error Models:**
- [ ] Swiss Cheese (multiple defenses, holes align → accident)
- [ ] SHELL model (Liveware interfaces: L-H, L-S, L-L, L-E)
- [ ] Human error types (slips, lapses, mistakes, violations)

**Prediction:**
- [ ] SHERPA (systematic error prediction via HTA)
- [ ] Error classification (action, retrieval, checking, selection)

**Situational Awareness:**
- [ ] Endsley 3 levels (perception, comprehension, projection)
- [ ] SAGAT measurement (freeze simulation, query operator)
- [ ] Mode confusion (automation surprises, wrong mode)

**Workload:**
- [ ] NASA-TLX (6 dimensions, 0-100 scale)
- [ ] Yerkes-Dodson inverted-U (underload/optimal/overload)
- [ ] Target TLX < 50 routine, < 70 emergency

**CRM:**
- [ ] Authority gradient (steep → accidents, flat → safe)
- [ ] PACE graded assertiveness (probe, alert, challenge, emergency)

**Design:**
- [ ] Anthropometry (5th-95th percentile)
- [ ] Display design (proximity, redundancy, salience)
- [ ] Control design (mapping, coding, guards)

═══════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
═══════════════════════════════════════════════════════════════════════════════

1️⃣ **70-80% of safety-critical accidents involve human error** — Cannot eliminate humans, must design systems resilient to error (error-tolerant design)

2️⃣ **Slips ≠ Mistakes** — Slips (execution errors) mitigated by constraints/guards; Mistakes (planning errors) mitigated by training/feedback

3️⃣ **Automation paradox** — Reduces routine workload BUT increases mode confusion, skill degradation, out-of-loop problems (careful automation design critical)

4️⃣ **Situational awareness has 3 levels** — Perception (see), Comprehension (understand), Projection (predict); loss at any level → accidents

5️⃣ **Workload inverted-U** — Underload (boredom) and overload (stress) both degrade performance; target optimal zone (NASA-TLX 30-50)

6️⃣ **Flat authority gradient saves lives** — Steep gradient (junior hesitant) → accidents; flat gradient (open communication) → errors caught early

7️⃣ **SHERPA finds errors before they happen** — Systematic prediction via task analysis, identifies credible errors at design phase (cheaper to fix)

═══════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **HUMAN FACTORS SAFETY CHEATSHEET COMPLETE**

**Created:** January 16, 2026  
**Coverage:** Human error taxonomy (slips/lapses/mistakes/violations), error models (Swiss Cheese, SHELL, CREAM), SHERPA prediction method, situational awareness (Endsley 3-level, SAGAT, mode confusion), cognitive workload (NASA-TLX, Yerkes-Dodson), CRM (authority gradient, PACE), human-centered design (MIL-STD-1472, display/control principles)

═══════════════════════════════════════════════════════════════════════════════
