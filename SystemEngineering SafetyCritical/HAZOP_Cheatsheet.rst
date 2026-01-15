🔍 **HAZOP — Hazard and Operability Study**
═══════════════════════════════════════════════════════════════════

**Full Name:** Hazard and Operability Study (HAZOP)  
**Type:** Structured brainstorming technique for hazard identification  
**Origin:** Imperial Chemical Industries (ICI), UK, 1960s  
**Standards:** IEC 61882, CCPS Guidelines, ISO 31010

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — HAZOP IN 60 SECONDS**
──────────────────────────────────

**What is HAZOP?**

::

    HAZOP = Systematic team-based hazard identification
    
    Method:
    1. Select a node (equipment/line)
    2. Choose process parameter (flow, temp, pressure)
    3. Apply guide word (MORE, LESS, NO, REVERSE)
    4. Generate deviation (e.g., "MORE flow")
    5. Identify causes → consequences → safeguards
    6. Recommend actions
    7. Repeat for all nodes × parameters × guide words

**Standard Guide Words:**

+-------------+------------------------+---------------------------+
| Guide Word  | Meaning                | Example (Flow)            |
+=============+========================+===========================+
| **NO/NOT**  | Complete negation      | No flow                   |
+-------------+------------------------+---------------------------+
| **MORE**    | Quantitative increase  | More flow (higher rate)   |
+-------------+------------------------+---------------------------+
| **LESS**    | Quantitative decrease  | Less flow (lower rate)    |
+-------------+------------------------+---------------------------+
| **AS WELL** | Qualitative addition   | Flow + contamination      |
| **AS**      |                        |                           |
+-------------+------------------------+---------------------------+
| **PART OF** | Qualitative reduction  | Flow of wrong composition |
+-------------+------------------------+---------------------------+
| **REVERSE** | Opposite direction     | Reverse flow (backflow)   |
+-------------+------------------------+---------------------------+
| **OTHER**   | Complete substitution  | Wrong material flowing    |
| **THAN**    |                        |                           |
+-------------+------------------------+---------------------------+

**When to Use HAZOP:**

✅ Chemical/process plants (primary domain)  
✅ Early design phase (P&ID review)  
✅ Complex interactions between equipment  
✅ Team has diverse expertise (process, operations, maintenance)

❌ Software-dominated systems (use STPA instead)  
❌ Late in project (expensive changes)  
❌ Simple single-component failures (use FMEA)

**HAZOP vs FMEA vs FTA:**

+---------------+-------------------+-------------------+-------------------+
| **Aspect**    | **HAZOP**         | **FMEA**          | **FTA**           |
+===============+===================+===================+===================+
| **Approach**  | Brainstorming     | Bottom-up         | Top-down          |
+---------------+-------------------+-------------------+-------------------+
| **Focus**     | Deviations from   | Component failure | Specific hazard   |
|               | design intent     |                   |                   |
+---------------+-------------------+-------------------+-------------------+
| **Domain**    | Process industry  | General (all)     | Complex systems   |
+---------------+-------------------+-------------------+-------------------+
| **Team**      | Required (5-7)    | Optional (1-3)    | Optional (1-2)    |
+---------------+-------------------+-------------------+-------------------+
| **Output**    | Action items      | RPN rankings      | Minimal cut sets  |
+---------------+-------------------+-------------------+-------------------+

════════════════════════════════════════════════════════════════════

📖 **1. HAZOP FUNDAMENTALS**
════════════════════════════

**1.1 Definition & Purpose**
----------------------------

**HAZOP Philosophy:**

    "Challenge every aspect of the design using structured prompts
    (guide words) to imagine what could deviate from the design intent"

**Key Principles:**

1. **Team-based**: Diverse expertise (process, operations, maintenance, safety)
2. **Systematic**: Every node × parameter × guide word examined
3. **Creative**: Brainstorm causes without censorship
4. **Structured**: Recording format ensures consistency
5. **Action-oriented**: Generate recommendations, assign responsibilities

**Objectives:**

✅ Identify hazards not found by individual analysis  
✅ Understand complex process interactions  
✅ Challenge design assumptions  
✅ Capture operational knowledge from experienced staff  
✅ Improve inherent safety (design changes before construction)

**1.2 Process Parameters**
--------------------------

**Standard Parameters (Process Industry):**

+-------------------+-----------------------------+
| **Parameter**     | **Deviations to Consider**  |
+===================+=============================+
| **Flow**          | More, Less, No, Reverse     |
+-------------------+-----------------------------+
| **Pressure**      | More, Less (vacuum)         |
+-------------------+-----------------------------+
| **Temperature**   | More (overheat), Less       |
+-------------------+-----------------------------+
| **Level**         | More (overflow), Less (dry) |
+-------------------+-----------------------------+
| **Composition**   | Part of, As well as, Other  |
+-------------------+-----------------------------+
| **Viscosity**     | More (thick), Less (thin)   |
+-------------------+-----------------------------+
| **Time/Sequence** | Too soon, Too late, Reverse |
+-------------------+-----------------------------+
| **pH**            | More (acidic), Less (basic) |
+-------------------+-----------------------------+

**Extended Parameters (Other Domains):**

.. code-block:: text

    Software HAZOP:
    - Data value (More, Less, Wrong)
    - Timing (Early, Late, Out of sequence)
    - Interfaces (Missing, Extra, Wrong format)
    
    Power Systems:
    - Voltage (High, Low, Transient)
    - Frequency (High, Low, Harmonic)
    - Phase (Missing, Unbalanced)
    
    Medical Devices:
    - Dose (Overdose, Underdose)
    - Duration (Too long, Too short)
    - Target (Wrong patient, Wrong site)

**1.3 Design Intent**
---------------------

**Critical Concept:**

    Each deviation is relative to "design intent"
    (normal operating conditions, not just current state)

**Example:**

.. code-block:: text

    Node: Reactor feed line
    Parameter: Flow
    Design Intent: 100 kg/hr at 5 bar
    
    Deviations:
    - MORE flow: 150 kg/hr (causes?)
    - LESS flow: 50 kg/hr (causes?)
    - NO flow: 0 kg/hr (causes?)
    - REVERSE flow: Backflow into feed tank (causes?)

════════════════════════════════════════════════════════════════════

📖 **2. HAZOP METHODOLOGY**
═══════════════════════════

**2.1 Team Composition**
------------------------

**Typical HAZOP Team (5-7 people):**

+------------------------+------------------------------------------------+
| **Role**               | **Responsibility**                             |
+========================+================================================+
| **Chair/Facilitator**  | Guide discussion, enforce discipline, time     |
|                        | management (experienced, independent)          |
+------------------------+------------------------------------------------+
| **Scribe/Recorder**    | Document causes, consequences, actions         |
|                        | (dedicated role, cannot multitask)             |
+------------------------+------------------------------------------------+
| **Design Engineer**    | Answer technical questions, explain intent     |
|                        | (P&ID creator)                                 |
+------------------------+------------------------------------------------+
| **Process Engineer**   | Chemistry, reaction kinetics, process hazards  |
+------------------------+------------------------------------------------+
| **Operations**         | Real-world experience, startup/shutdown        |
| **Representative**     | scenarios                                      |
+------------------------+------------------------------------------------+
| **Maintenance**        | Equipment failure modes, maintenance issues    |
| **Engineer**           |                                                |
+------------------------+------------------------------------------------+
| **Instrumentation**    | Control system, alarms, interlocks             |
| **/Control Engineer**  |                                                |
+------------------------+------------------------------------------------+
| **Safety Specialist**  | Consequence analysis, risk assessment          |
| **(optional)**         |                                                |
+------------------------+------------------------------------------------+

**2.2 HAZOP Process (7 Steps)**
-------------------------------

**Step 1: Define Scope & Boundaries**

- What system? (specific unit, entire plant, batch vs continuous)
- Which drawings? (P&ID revision, design freeze point)
- Exclusions? (utilities already analyzed, vendor packages)

**Step 2: Divide System into Nodes**

.. code-block:: text

    Node = Section of plant examined together
    
    Guidelines:
    - Each node has clear boundaries (inlet/outlet)
    - Homogeneous equipment (similar hazards)
    - Manageable size (~2-4 hours per node)
    
    Example (Chemical Reactor):
    - Node 1: Reactor feed system
    - Node 2: Reactor vessel
    - Node 3: Reactor cooling system
    - Node 4: Reactor discharge/quench

**Step 3: Select Node & Identify Design Intent**

.. code-block:: text

    Node 1: Reactor feed line (PL-101)
    Design Intent:
    - Feed 100 kg/hr of Reactant A
    - Temperature: 25°C ±5°C
    - Pressure: 5 bar
    - Composition: 95% Reactant A, 5% solvent

**Step 4: Apply Guide Words → Generate Deviations**

For each parameter, systematically apply all guide words:

.. code-block:: text

    Parameter: FLOW
    
    Guide Word → Deviation:
    - NO → No flow in PL-101
    - MORE → Flow > 100 kg/hr
    - LESS → Flow < 100 kg/hr
    - REVERSE → Backflow from reactor to feed tank
    - AS WELL AS → Flow + foreign material (contamination)
    - PART OF → Flow of wrong composition (only solvent)
    - OTHER THAN → Wrong material flowing (Reactant B)

**Step 5: Identify Causes**

Brainstorm all possible causes (no censorship):

.. code-block:: text

    Deviation: NO FLOW
    
    Causes:
    1. Feed pump fails (mechanical, electrical)
    2. Isolation valve closed (human error, control fault)
    3. Line blocked (solid precipitation, frozen)
    4. Feed tank empty (supply chain, level sensor failure)
    5. Control system failure (PLC, I/O card)

**Step 6: Analyze Consequences**

Determine outcomes if deviation occurs:

.. code-block:: text

    Deviation: NO FLOW
    
    Consequences:
    1. Reactor starves → exotherm stops → safe shutdown ✅
    2. But: Incomplete reaction → product off-spec
    3. If other reactants still flowing → imbalance → runaway? 🚨

**Step 7: Evaluate Safeguards & Recommend Actions**

.. code-block:: text

    Existing Safeguards:
    1. Flow transmitter FT-101 (alarms on low flow)
    2. Low-low flow interlock (stops feed pump P-102)
    3. Pump run status monitored by DCS
    
    Risk Assessment:
    - Frequency: LOW (pump reliable, maintained)
    - Consequence: LOW (safe shutdown)
    - ACCEPTABLE ✅
    
    Actions:
    - None required
    
    ---
    
    ALTERNATE SCENARIO:
    
    Deviation: REVERSE FLOW
    
    Consequences:
    - Reactor contents backflow to feed tank
    - Feed tank not rated for reactive mixture
    - POTENTIAL EXPLOSION 🚨
    
    Existing Safeguards:
    - Check valve CV-101 (prevents backflow)
    
    Risk Assessment:
    - Frequency: VERY LOW (check valve reliable)
    - Consequence: CATASTROPHIC
    - NOT ACCEPTABLE ❌
    
    Actions:
    1. Add redundant check valve (CV-101A) [ASME B31.3]
    2. Add pressure relief on feed line (PSV-101) [Responsible: J.Smith]
    3. Interlock: High pressure feed → close isolation valve [Due: 2026-03-01]

**2.3 Recording Format**
------------------------

**Standard HAZOP Table:**

+------+----------+----------+--------+--------+-----------+---------+----------+--------+
| Node | Param    | Guide    | Dev.   | Causes | Conseq.   | Safe-   | Action   | Resp.  |
|      |          | Word     |        |        |           | guards  |          |        |
+======+==========+==========+========+========+===========+=========+==========+========+
| 1    | Flow     | NO       | No     | Pump   | Reactor   | FT-101  | None     | -      |
|      |          |          | flow   | fails  | shutdown  | alarm   |          |        |
+------+----------+----------+--------+--------+-----------+---------+----------+--------+
| 1    | Flow     | REVERSE  | Back-  | Check  | Explosion | CV-101  | Add      | J.S.   |
|      |          |          | flow   | valve  | in feed   |         | 2nd      |        |
|      |          |          |        | fails  | tank      |         | check    |        |
|      |          |          |        |        |           |         | valve    |        |
+------+----------+----------+--------+--------+-----------+---------+----------+--------+

════════════════════════════════════════════════════════════════════

📖 **3. HAZOP EXAMPLE: CHEMICAL REACTOR**
═════════════════════════════════════════

**3.1 Process Description**
---------------------------

**System:** Batch chemical reactor producing polymer

.. code-block:: text

    P&ID Description:
    
    FEED SYSTEM:
    - Tank T-101 (Monomer A, 1000 kg)
    - Pump P-101 (100 kg/hr, 0-150 kg/hr variable)
    - Flow transmitter FT-101 (control, alarm)
    - Control valve CV-101 (flow control)
    
    REACTOR:
    - Vessel R-101 (500 L, rated 10 bar, 200°C)
    - Jacket cooling (chilled water, TT-101 control)
    - Agitator M-101 (500 RPM)
    - Pressure relief PSV-101 (set 9 bar)
    - Temperature transmitter TT-101 (alarm at 180°C)
    
    REACTION:
    - Exothermic polymerization (ΔH = -500 kJ/mol)
    - Runaway risk if cooling lost

**3.2 HAZOP Session Excerpt**
-----------------------------

**Node 1: Monomer Feed Line (P-101 to R-101)**

**Design Intent:**

- Flow: 100 kg/hr for 5 hours (500 kg batch)
- Temperature: 25°C (ambient)
- Pressure: 5 bar
- Composition: 99.5% Monomer A, 0.5% inhibitor

**Full HAZOP Table:**

+------------+----------+----------+--------------------+-------------------+-------------------+-----------------+------------------+
| **Guide**  | **Dev.** | **Causes**           | **Consequences**  | **Severity**      | **Safeguards**  | **Actions**      |
| **Word**   |          |                      |                   |                   |                 |                  |
+============+==========+======================+===================+===================+=================+==================+
| **NO**     | No flow  | 1. Pump P-101 fails  | - Incomplete      | MODERATE          | - FT-101 low    | **None**         |
|            |          | 2. CV-101 closed     |   batch           | (product loss)    |   alarm         | (acceptable)     |
|            |          | 3. T-101 empty       | - Can restart     |                   | - Low flow      |                  |
|            |          | 4. Line blocked      |                   |                   |   interlock     |                  |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **MORE**   | High     | 1. CV-101 fails      | - Overfill R-101  | **HIGH**          | - Level high    | **ACTION 1:**    |
|            | flow     |    open              | - Exceed design   | (vessel rupture)  |   alarm         | Add level        |
|            | (>150    | 2. Flow transmitter  |   volume          | **CATASTROPHIC**  | - LSH-101       | interlock        |
|            | kg/hr)   |    fails high        | - Runaway         |                   |   (high-high    | (close CV-101    |
|            |          | 3. Control system    |   reaction        |                   |   level)        | on LSHH-101)     |
|            |          |    error             |   (exotherm)      |                   | - PSV-101       |                  |
|            |          |                      |                   |                   |   (relief)      | **Resp:** P.M.   |
|            |          |                      |                   |                   |                 | **Due:** 1 month |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **LESS**   | Low flow | 1. Pump wear         | - Longer batch    | LOW               | - FT-101 alarm  | **None**         |
|            | (50-100  | 2. Line partially    |   time            | (minor)           |                 |                  |
|            | kg/hr)   |    blocked           | - No safety       |                   |                 |                  |
|            |          | 3. Control valve     |   impact          |                   |                 |                  |
|            |          |    partially closed  |                   |                   |                 |                  |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **REVERSE**| Backflow | 1. Check valve fails | - Reactor         | **CATASTROPHIC**  | - Check valve   | **ACTION 2:**    |
|            | from     | 2. Pump runs         |   contents        | (tank explosion)  |   CV-102        | Add redundant    |
|            | reactor  |    reverse           |   backflow        | - Reactive mix    |                 | check valve      |
|            | to T-101 | 3. Reactor           | - T-101 not       |   in atmos tank   |                 | (CV-102A)        |
|            |          |    overpressure      |   rated for       |                   |                 |                  |
|            |          |                      |   pressure        |                   |                 | **ACTION 3:**    |
|            |          |                      | - Vapor release   |                   |                 | Add pressure     |
|            |          |                      |   to atmos        |                   |                 | relief PSV-102   |
|            |          |                      |                   |                   |                 | on T-101         |
|            |          |                      |                   |                   |                 |                  |
|            |          |                      |                   |                   |                 | **Resp:** J.D.   |
|            |          |                      |                   |                   |                 | **Due:** ASAP    |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **AS WELL**| Flow +   | 1. T-101             | - Contaminated    | MODERATE          | - Feedstock     | **ACTION 4:**    |
| **AS**     | contam.  |    contaminated      |   product         | (product loss)    |   QC testing    | Add online       |
|            |          | 2. Line flushing     | - Potential       | **HIGH** if       | - Batch records | composition      |
|            |          |    incomplete        |   incompatible    |   incompatible    |                 | analyzer         |
|            |          | 3. Wrong tank        |   reaction        |   material        |                 | (AT-101)         |
|            |          |    connected         |                   |                   |                 |                  |
|            |          |                      |                   |                   |                 | **Resp:** C.E.   |
|            |          |                      |                   |                   |                 | **Due:** 3 mo    |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **PART OF**| Low      | 1. Inhibitor         | - Premature       | **HIGH**          | - Certificate   | **ACTION 5:**    |
|            | inhibitor|    not added         |   polymerization  | (runaway in       |   of analysis   | Add inhibitor    |
|            | conc.    | 2. Inhibitor         |   in T-101        |   storage tank)   |   (supplier)    | concentration    |
|            |          |    degraded          | - Solid formation | **CATASTROPHIC**  |                 | monitor (AIT-101)|
|            |          | 3. Wrong batch       | - Tank rupture    |                   |                 |                  |
|            |          |                      |                   |                   |                 | **Resp:** I&C    |
|            |          |                      |                   |                   |                 | **Due:** 2 mo    |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+
| **OTHER**  | Wrong    | 1. Tank mislabeled   | - Violent         | **CATASTROPHIC**  | - Tank labeling | **ACTION 6:**    |
| **THAN**   | material | 2. Operator error    |   reaction        | (reactor          | - Procedures    | Implement        |
|            | (Monomer | 3. Piping cross-     | - Explosion       |   explosion)      | - Training      | dedicated        |
|            | B)       |    connection        | - Toxic release   |                   |                 | piping (no       |
|            |          |                      |                   |                   |                 | cross-connects)  |
|            |          |                      |                   |                   |                 |                  |
|            |          |                      |                   |                   |                 | **ACTION 7:**    |
|            |          |                      |                   |                   |                 | Add composition  |
|            |          |                      |                   |                   |                 | verification     |
|            |          |                      |                   |                   |                 | (AT-101 +        |
|            |          |                      |                   |                   |                 | operator check)  |
|            |          |                      |                   |                   |                 |                  |
|            |          |                      |                   |                   |                 | **Resp:** Ops    |
|            |          |                      |                   |                   |                 | **Due:** 1 mo    |
+------------+----------+----------------------+-------------------+-------------------+-----------------+------------------+

**Summary:**

- **Deviations examined:** 7 (NO, MORE, LESS, REVERSE, AS WELL AS, PART OF, OTHER THAN)
- **Actions generated:** 7 (interlocks, redundancy, analyzers, procedures)
- **Critical findings:** 3 (REVERSE flow, wrong material, low inhibitor) → All addressed

════════════════════════════════════════════════════════════════════

📖 **4. HAZOP IN DIFFERENT DOMAINS**
════════════════════════════════════

**4.1 Software HAZOP (IEC 61508-7 Annex B)**
--------------------------------------------

**Adapted Guide Words for Software:**

+----------------+------------------------------+--------------------------+
| **Guide Word** | **Software Interpretation**  | **Example**              |
+================+==============================+==========================+
| **NO/NONE**    | Data/signal missing          | Sensor input not         |
|                |                              | received                 |
+----------------+------------------------------+--------------------------+
| **MORE**       | Data value too high          | ADC reading saturated    |
|                | Too many executions          | Loop iterates excessively|
+----------------+------------------------------+--------------------------+
| **LESS**       | Data value too low           | Integer underflow        |
|                | Too few executions           | Timeout too short        |
+----------------+------------------------------+--------------------------+
| **AS WELL AS** | Extra data                   | Unexpected interrupt     |
|                | Spurious execution           | Buffer overflow          |
+----------------+------------------------------+--------------------------+
| **PART OF**    | Incomplete data              | Partial packet received  |
|                | Skipped step                 | Watchdog not serviced    |
+----------------+------------------------------+--------------------------+
| **REVERSE**    | Opposite logic               | Sign error (+ instead -)  |
|                | Backward sequence            | LIFO instead of FIFO     |
+----------------+------------------------------+--------------------------+
| **OTHER THAN** | Wrong data                   | Units mismatch (m vs ft) |
|                | Wrong sequence               | Init after use           |
+----------------+------------------------------+--------------------------+
| **EARLY**      | Timing too soon              | ISR before init          |
+----------------+------------------------------+--------------------------+
| **LATE**       | Timing too slow              | Deadline overrun         |
+----------------+------------------------------+--------------------------+
| **BEFORE**     | Sequence error               | Read before write        |
+----------------+------------------------------+--------------------------+
| **AFTER**      | Sequence error               | Free before last use     |
+----------------+------------------------------+--------------------------+

**Example: Automotive ECU Software HAZOP**

.. code-block:: text

    Node: Torque control algorithm
    Design Intent: Calculate requested torque every 10ms
    
    +------------+------------------+------------------+-----------------+
    | Guide Word | Deviation        | Causes           | Consequences    |
    +============+==================+==================+=================+
    | NO         | No torque        | Task not         | Loss of         |
    |            | calculated       | scheduled        | propulsion      |
    |            |                  | Watchdog reset   |                 |
    +------------+------------------+------------------+-----------------+
    | MORE       | Torque > max     | Integer overflow | Unintended      |
    |            | (>500 Nm)        | Sensor fault     | acceleration    |
    |            |                  | (reads 32767)    | (ASIL D hazard) |
    +------------+------------------+------------------+-----------------+
    | EARLY      | Calculation      | ISR preempts     | Uses stale      |
    |            | before sensor    | before sensor    | sensor data     |
    |            | update           | read complete    |                 |
    +------------+------------------+------------------+-----------------+
    | OTHER THAN | Wrong units      | Pedal in %,      | Factor of 100   |
    |            |                  | torque in Nm/100 | error!          |
    +------------+------------------+------------------+-----------------+

**4.2 Pharmaceutical HAZOP**
----------------------------

**Application:** Drug manufacturing (batch processes)

**Example Deviations:**

.. code-block:: text

    Node: Mixing vessel for API (Active Pharmaceutical Ingredient)
    Parameter: Temperature
    Design Intent: Heat to 80°C ±2°C for 2 hours
    
    Deviations:
    - MORE temp: >82°C → API degradation, impurity formation
    - LESS temp: <78°C → Incomplete reaction, low yield
    - NO heating: Ambient → No reaction
    - AS WELL AS: Heating + pressure → Vessel overpressure
    - OTHER THAN: Wrong temp sensor → Control error

**GMP Integration:**

- HAZOP findings feed into validation protocols
- Critical Process Parameters (CPPs) identified
- Proven Acceptable Range (PAR) confirmed
- Control strategy defined

**4.3 Healthcare HAZOP**
------------------------

**Application:** Clinical procedures, medical device use

**Example: Insulin Pump Infusion**

.. code-block:: text

    Node: Insulin delivery
    Design Intent: 1.5 units/hour basal rate
    
    +-------------+------------------+------------------+-----------------+
    | Guide Word  | Deviation        | Causes           | Consequences    |
    +=============+==================+==================+=================+
    | MORE        | Overdose         | Programming      | Hypoglycemia    |
    |             | (>1.5 units/hr)  | error            | Seizure, death  |
    |             |                  | Occlusion (back- |                 |
    |             |                  | pressure → bolus)|                 |
    +-------------+------------------+------------------+-----------------+
    | LESS        | Underdose        | Empty reservoir  | Hyperglycemia   |
    |             | (<1.5 units/hr)  | Catheter kinked  | Ketoacidosis    |
    |             |                  | Air in line      |                 |
    +-------------+------------------+------------------+-----------------+
    | OTHER THAN  | Wrong patient    | Patient swap     | Adverse event   |
    |             | receiving dose   | Unlabeled pump   | (wrong dose)    |
    +-------------+------------------+------------------+-----------------+

════════════════════════════════════════════════════════════════════

📖 **5. HAZOP BEST PRACTICES**
══════════════════════════════

**5.1 Planning**
----------------

**Before HAZOP:**

✅ **Freeze design**: P&ID approved, major changes locked  
✅ **Assemble team**: 5-7 people, diverse expertise  
✅ **Book time**: 4-hour sessions max (2-3 hours optimal)  
✅ **Distribute drawings**: Team reviews P&ID beforehand  
✅ **Define nodes**: Pre-divide system (save meeting time)  
✅ **Set expectations**: Timeline (2-3 weeks), deliverable format

**5.2 Facilitation**
--------------------

**Chair Responsibilities:**

✅ **Keep pace**: 2-4 hours per node (don't get bogged down)  
✅ **Enforce discipline**: One deviation at a time, no side discussions  
✅ **Challenge design**: Ask "What if...?" persistently  
✅ **Capture creativity**: No censorship during brainstorming  
✅ **Timebox**: If stuck >15 min, note as "further study" and move on  
✅ **Prevent groupthink**: Solicit quiet participants

**Common Pitfalls:**

❌ **Design session**: HAZOP is NOT for solving problems (note actions, solve later)  
❌ **"That can't happen"**: Challenge unlikely assumptions  
❌ **Action fatigue**: Too many actions → prioritize critical issues  
❌ **Over-optimism**: "Operator will notice" is NOT a safeguard  
❌ **Scope creep**: Stay within defined nodes

**5.3 Recording**
-----------------

**Scribe Best Practices:**

✅ Use structured template (digital HAZOP tool preferred)  
✅ Record verbatim (don't interpret/summarize during meeting)  
✅ Project screen (team sees documentation in real-time)  
✅ Action items: SMART (Specific, Measurable, Assignable, Realistic, Time-bound)  
✅ Mark "credible but unlikely" separately (don't ignore, but lower priority)

**5.4 Follow-Up**
-----------------

**After HAZOP:**

1. **Draft report** (within 1 week)
   - Send to team for review
   - Incorporate comments

2. **Final report** (within 2 weeks)
   - Distribute to stakeholders
   - Upload to document control

3. **Action tracking**
   - Assign owners
   - Track progress (monthly review)
   - Verify closure (evidence required)

4. **Re-HAZOP triggers:**
   - Major design change (>20% of nodes affected)
   - Incident/near-miss (re-examine relevant nodes)
   - Operations change (new feedstock, different conditions)

════════════════════════════════════════════════════════════════════

📖 **6. HAZOP TOOLS**
═════════════════════

**6.1 Commercial Software**
---------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Key Features**           |
+======================+==================+============================+
| **PHA-Pro**          | ioMosaic (Baker) | HAZOP, LOPA, Bow-Tie       |
|                      |                  | integration                |
+----------------------+------------------+----------------------------+
| **PHAWorks**         | Sphera           | Team collaboration, report |
|                      |                  | generation                 |
+----------------------+------------------+----------------------------+
| **THESIS**           | ASAP Group       | HAZOP, SIL verification    |
+----------------------+------------------+----------------------------+
| **Relex PHA**        | Relyence         | FMEA/HAZOP integration     |
+----------------------+------------------+----------------------------+

**6.2 Template (Excel/Word)**
-----------------------------

**Simple HAZOP Recording Template:**

.. code-block:: text

    Downloadable: https://www.icheme.org/resources/hazop-worksheet
    
    Columns:
    1. Node/Line ID
    2. Parameter (Flow, Temp, Pressure, etc.)
    3. Guide Word
    4. Deviation
    5. Possible Causes (multiple rows)
    6. Consequences (severity rating)
    7. Existing Safeguards
    8. Risk Rating (Frequency × Severity)
    9. Recommendations
    10. Responsibility
    11. Target Date
    12. Status (Open/Closed)

**6.3 Python HAZOP Matrix Generator**
-------------------------------------

**Automated Deviation Matrix:**

.. code-block:: python

    # hazop_matrix_generator.py
    
    import pandas as pd
    from itertools import product
    
    # Define guide words
    guide_words = ['NO', 'MORE', 'LESS', 'REVERSE', 'AS WELL AS', 
                   'PART OF', 'OTHER THAN']
    
    # Define parameters
    parameters = ['Flow', 'Pressure', 'Temperature', 'Level', 
                  'Composition', 'Viscosity', 'pH']
    
    # Generate all combinations
    deviations = []
    for param, gw in product(parameters, guide_words):
        # Skip nonsensical combinations
        if (param in ['Composition', 'Viscosity'] and gw == 'REVERSE'):
            continue  # Can't reverse composition
        if (param == 'pH' and gw in ['REVERSE', 'AS WELL AS']):
            continue
        
        # Generate deviation phrase
        if gw == 'NO':
            dev = f"No {param.lower()}"
        elif gw == 'MORE':
            dev = f"High {param.lower()}"
        elif gw == 'LESS':
            dev = f"Low {param.lower()}"
        elif gw == 'REVERSE':
            dev = f"Reverse {param.lower()}"
        elif gw == 'AS WELL AS':
            dev = f"{param} + contamination"
        elif gw == 'PART OF':
            dev = f"{param} incomplete"
        elif gw == 'OTHER THAN':
            dev = f"Wrong {param.lower()}"
        
        deviations.append({
            'Parameter': param,
            'Guide_Word': gw,
            'Deviation': dev,
            'Causes': '',
            'Consequences': '',
            'Safeguards': '',
            'Risk': '',
            'Actions': ''
        })
    
    # Create DataFrame
    hazop_df = pd.DataFrame(deviations)
    
    # Export to Excel
    hazop_df.to_excel('HAZOP_Template.xlsx', index=False)
    
    print(f"Generated {len(deviations)} deviation combinations")
    print(hazop_df.head(10))

**Output:**

.. code-block:: text

    Generated 45 deviation combinations
    
       Parameter Guide_Word           Deviation Causes Consequences ...
    0       Flow         NO            No flow                      ...
    1       Flow       MORE          High flow                      ...
    2       Flow       LESS           Low flow                      ...
    3       Flow    REVERSE       Reverse flow                      ...
    4       Flow  AS WELL AS  Flow + contamination                  ...
    ...

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between HAZOP and FMEA?

**A1:**

- **HAZOP**: Team-based brainstorming, uses guide words to challenge design,
  identifies deviations from design intent. Best for process industry.
- **FMEA**: Individual/small team, bottom-up component failure analysis,
  calculates RPN. Best for hardware/equipment.
- **Key difference**: HAZOP finds hazards through structured creativity;
  FMEA systematically analyzes known failure modes.

────────────────────────────────────────────────────────────────────

**Q2:** Name 5 standard HAZOP guide words and give examples.

**A2:**

1. **NO/NOT**: No flow (pump stopped)
2. **MORE**: High pressure (relief valve stuck)
3. **LESS**: Low temperature (heater fails)
4. **REVERSE**: Backflow (check valve fails)
5. **AS WELL AS**: Flow + contamination (wrong material added)

────────────────────────────────────────────────────────────────────

**Q3:** Why is a multi-disciplinary team essential for HAZOP?

**A3:**

Different perspectives uncover different hazards:
- **Design Engineer**: Knows intent, can explain system
- **Operations**: Real-world experience, startup/shutdown scenarios
- **Maintenance**: Equipment failure modes, degradation
- **Process Engineer**: Chemistry, reaction kinetics
- **I&C Engineer**: Control system, interlocks

A single person would miss hazards outside their expertise.

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Planning Phase:**
- [ ] Define scope and boundaries
- [ ] Freeze P&ID (approved design)
- [ ] Assemble multi-disciplinary team (5-7 people)
- [ ] Book HAZOP sessions (2-3 hours each)
- [ ] Distribute P&ID to team (1 week advance)
- [ ] Pre-define nodes (manageable sections)

**Execution Phase:**
- [ ] Define design intent for each node
- [ ] Apply all guide words to each parameter
- [ ] Brainstorm causes (no censorship)
- [ ] Analyze consequences (severity)
- [ ] Identify existing safeguards
- [ ] Assess risk (frequency × severity)
- [ ] Generate recommendations (design changes, interlocks, procedures)
- [ ] Assign actions (owner, due date)

**Follow-Up Phase:**
- [ ] Draft HAZOP report (within 1 week)
- [ ] Team review and comments
- [ ] Final report (within 2 weeks)
- [ ] Track actions to closure
- [ ] Verify implementation (evidence)
- [ ] Update P&ID with changes
- [ ] Re-HAZOP if major design changes

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **HAZOP = Structured creativity** → Guide words challenge design assumptions

2️⃣ **Team-based** → Multi-disciplinary perspectives essential (5-7 people)

3️⃣ **7 guide words** → NO, MORE, LESS, REVERSE, AS WELL AS, PART OF, OTHER THAN

4️⃣ **Process industry** → Best for chemical plants, batch processes, P&ID review

5️⃣ **Deviations from intent** → Not just failures, but any deviation (operational, procedural)

6️⃣ **Action-oriented** → Generate recommendations, assign owners, track closure

7️⃣ **Complement FMEA/FTA** → HAZOP for ideation, FMEA for systematic, FTA for causation

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **HAZOP CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Definition, guide words, methodology, chemical reactor example,  
software/pharma/healthcare HAZOP, best practices, tools, Python automation

════════════════════════════════════════════════════════════════════
