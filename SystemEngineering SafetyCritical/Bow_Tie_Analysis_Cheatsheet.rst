🎀 **Bow-Tie Analysis**
═══════════════════════════════════════════════════════════════════

**Full Name:** Bow-Tie Diagram / Barrier Analysis  
**Type:** Visual risk assessment combining causes and consequences  
**Origin:** Shell Oil, 1970s; IEC 31010:2019  
**Metaphor:** Necktie shape (threats converge, consequences diverge)

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — BOW-TIE IN 60 SECONDS**
─────────────────────────────────────

**What is Bow-Tie Analysis?**

::

    Bow-Tie = Visual combination of FTA (left) + ETA (right)
    
    Structure:
    
        Threats         Prevention      HAZARD      Mitigation      Consequences
        (Causes)        Barriers                    Barriers        (Outcomes)
    
    ───┐               ║               ╔═══╗               ║               ┌───
    ───┤───Barrier 1───║───Barrier 3───║ H ║───Barrier 5───║───Barrier 6───┤───
    ───┘               ║               ║ A ║               ║               └───
    ───────Barrier 2───║               ║ Z ║               ║───────────────────
    ───────────────────║───Barrier 4───║ A ║───────────────║───────────────────
                                       ║ R ║
                                       ║ D ║
                                       ╚═══╝

**Key Concepts:**

- **Central Hazard**: Undesired event (loss of containment, fire, collision)
- **Threats (Left)**: Causes that could lead to hazard
- **Prevention Barriers (Left)**: Controls to stop threats
- **Consequences (Right)**: Outcomes if hazard occurs
- **Mitigation Barriers (Right)**: Controls to reduce severity
- **Escalation Factors**: Degraded/failed barriers

**Bow-Tie vs FTA/ETA:**

+------------------+----------------------------+----------------------------+
| **Aspect**       | **Bow-Tie**                | **FTA + ETA**              |
+==================+============================+============================+
| **Visual**       | Single diagram (compact)   | Two separate trees         |
+------------------+----------------------------+----------------------------+
| **Focus**        | Barriers (controls)        | Logic gates, probabilities |
+------------------+----------------------------+----------------------------+
| **Audience**     | Management, operations     | Safety engineers, analysts |
+------------------+----------------------------+----------------------------+
| **Quantitative** | Qualitative (or semi)      | Fully quantitative         |
+------------------+----------------------------+----------------------------+
| **Use Case**     | Risk communication         | Detailed analysis          |
|                  | SMS (Safety Management)    | PRA, certification         |
+------------------+----------------------------+----------------------------+

**When to Use Bow-Tie:**

✅ Major Accident Hazards (MAH) — process industry  
✅ Safety Management Systems (SMS) — aviation, offshore  
✅ Risk communication to non-technical stakeholders  
✅ Barrier management (lifecycle tracking)  
✅ Incident investigation (visualize what failed)

════════════════════════════════════════════════════════════════════

📖 **1. BOW-TIE FUNDAMENTALS**
══════════════════════════════

**1.1 Definition & Purpose**
----------------------------

**Bow-Tie Diagram:**

    Graphical representation showing pathways from causes through
    a central hazardous event to consequences, with barriers/controls
    to prevent or mitigate the event.

**Origin of Name:**

.. code-block:: text

    Visual resembles a bow-tie (or butterfly):
    
         Threats           HAZARD        Consequences
           (fan out)     (narrow point)    (fan out)
    
    ─────┐             ┌─────┐             ┌─────
    ─────┤             │     │             ├─────
    ─────┤═════════════│ HAZ │═════════════┤─────
    ─────┤             │     │             ├─────
    ─────┘             └─────┘             └─────
    
     LEFT SIDE          CENTER          RIGHT SIDE
     (Prevention)     (Hazard Event)   (Mitigation)

**Objectives:**

✅ **Visual clarity**: Single-page overview of risk scenario  
✅ **Barrier identification**: Enumerate all controls (prevention + mitigation)  
✅ **Gap analysis**: Identify missing or weak barriers  
✅ **Communication**: Explain risk to management, regulators  
✅ **Barrier management**: Track performance, degradation, testing  
✅ **Incident investigation**: Show what barriers failed

**1.2 Components of Bow-Tie**
-----------------------------

**1. Central Hazard (Top Event):**

    The undesired event that releases energy/material or causes harm
    
    Examples:
    - Loss of containment (toxic gas release)
    - Fire/explosion
    - Aircraft collision
    - Vehicle crash
    - Equipment failure

**2. Threats (Left Side):**

    Causes or initiating events that can trigger the hazard
    
    Examples (for "Loss of containment"):
    - Corrosion
    - Overpressure
    - External impact
    - Human error (wrong valve opened)
    - Design flaw

**3. Prevention Barriers (Left Side):**

    Controls that prevent threats from causing the hazard
    
    Types:
    - Physical: Corrosion coating, pressure relief valve
    - Procedural: Inspection schedule, training
    - Administrative: Permit-to-work system, double-check
    - Technical: Alarm, interlock, redundancy

**4. Consequences (Right Side):**

    Outcomes if the hazard occurs (escalation paths)
    
    Examples (for "Fire"):
    - Minor fire (localized, controlled)
    - Major fire (spreads to adjacent equipment)
    - Explosion (if confined space)
    - Fatalities (personnel exposure)

**5. Mitigation Barriers (Right Side):**

    Controls that reduce severity of consequences
    
    Examples:
    - Fire suppression system
    - Emergency shutdown
    - Evacuation procedures
    - Personal protective equipment (PPE)
    - Firewall/blast wall

**6. Escalation Factors:**

    Conditions that degrade or defeat barriers
    
    Examples:
    - Maintenance backlog (barrier not tested)
    - Bypassed safety systems
    - Inadequate training
    - Budget cuts (reduced inspection frequency)

**1.3 Barrier Types**
---------------------

**Hardware Barriers:**

- Physical separation (firewall, dike)
- Pressure relief devices (PSV, rupture disk)
- Detection systems (gas detector, smoke alarm)
- Shutdown systems (interlock, emergency stop)

**Human Barriers:**

- Operator intervention (manual shutdown)
- Inspection/monitoring (walk-around checks)
- Maintenance activities (calibration, repair)
- Emergency response (firefighting, evacuation)

**Systems Barriers:**

- Procedures (work instructions, checklists)
- Training/competence (operator qualification)
- Management systems (permit-to-work, MOC)
- Design standards (codes, specifications)

**Layer of Protection Analysis (LOPA) Integration:**

.. code-block:: text

    Independent Protection Layers (IPLs) on Bow-Tie:
    
    Each barrier should be:
    ✅ Effective (high reliability, low PFD)
    ✅ Independent (one failure doesn't affect others)
    ✅ Auditable (can verify functionality)

════════════════════════════════════════════════════════════════════

📖 **2. BOW-TIE CONSTRUCTION PROCESS**
══════════════════════════════════════

**2.1 Step 1: Select Hazard**
-----------------------------

**Criteria for Hazard Selection:**

- High consequence (fatality, major environmental, large financial loss)
- Major Accident Hazard (MAH) as per regulations
- Significant stakeholder concern
- Historical incidents (learn from failures)

**Example Hazards:**

.. code-block:: text

    Process Industry:
    - Loss of containment (toxic gas, flammable liquid)
    - Fire/explosion
    - Runaway reaction
    
    Aviation:
    - Mid-air collision
    - Controlled Flight Into Terrain (CFIT)
    - Loss of control
    
    Automotive:
    - Unintended acceleration
    - Loss of braking
    - Pedestrian collision
    
    Offshore Oil & Gas:
    - Blowout
    - Structural collapse (platform)
    - Helicopter crash

**2.2 Step 2: Identify Threats**
--------------------------------

**Methods:**

- HAZOP study results
- FMEA failure modes
- Historical incident data
- Brainstorming (team workshop)
- Industry best practices

**Example: Loss of Containment (LOC) from Storage Tank**

.. code-block:: text

    Threats:
    1. Corrosion (internal/external)
    2. Overpressure (relief valve failure)
    3. Overfilling (level control failure)
    4. External impact (vehicle collision, dropped object)
    5. Structural failure (foundation settlement, fatigue)
    6. Human error (wrong valve opened, maintenance error)
    7. Design flaw (inadequate wall thickness)
    8. Natural hazard (earthquake, flood, lightning)

**2.3 Step 3: Identify Prevention Barriers**
--------------------------------------------

**For each threat, list controls that prevent hazard:**

.. code-block:: text

    Threat: Corrosion
    Prevention Barriers:
    - B1: Corrosion-resistant coating (internal lining)
    - B2: Cathodic protection system
    - B3: Ultrasonic thickness monitoring (annual inspection)
    - B4: Corrosion inhibitor injection
    - B5: Material selection (stainless steel)
    
    Threat: Overpressure
    Prevention Barriers:
    - B6: Pressure relief valve (PSV)
    - B7: Pressure transmitter + high alarm
    - B8: High-high pressure interlock (closes inlet)
    - B9: Rupture disk (secondary relief)
    - B10: Design margin (vessel rated 150% MAWP)
    
    Threat: External Impact
    Prevention Barriers:
    - B11: Bollards/crash barriers around tank
    - B12: Restricted access zone (signage, fence)
    - B13: Vehicle speed limit enforcement
    - B14: Tank elevated on foundation (out of vehicle reach)

**2.4 Step 4: Identify Consequences**
-------------------------------------

**Escalation paths if hazard occurs:**

.. code-block:: text

    Hazard: Loss of Containment (toxic gas release)
    
    Consequences:
    1. Minor release (< 1 kg) → Localized exposure, no offsite impact
    2. Moderate release (1-100 kg) → Onsite injuries, plant shutdown
    3. Major release (> 100 kg) → Offsite exposure, evacuation, fatalities
    
    Escalation factors:
    - Wind direction (toward populated area)
    - Time of day (shift change, high personnel count)
    - Emergency response delay (inadequate training)

**2.5 Step 5: Identify Mitigation Barriers**
--------------------------------------------

**For each consequence, list controls to reduce severity:**

.. code-block:: text

    Consequence: Major Toxic Release
    Mitigation Barriers:
    - M1: Gas detection system (early warning)
    - M2: Emergency shutdown system (ESD) — isolate source
    - M3: Water spray deluge system (knockdown vapor cloud)
    - M4: Emergency alarm (alert personnel)
    - M5: Evacuation procedures (muster points)
    - M6: Breathing apparatus (SCBA) availability
    - M7: Emergency response team (trained firefighters)
    - M8: Community notification system (sirens, alerts)
    - M9: Wind sock (visible wind direction)
    - M10: Offsite emergency plan (shelter-in-place)

**2.6 Step 6: Draw Bow-Tie Diagram**
------------------------------------

**Layout Rules:**

1. **Hazard in center** (prominent box)
2. **Threats on left** (fan out from hazard)
3. **Consequences on right** (fan out from hazard)
4. **Barriers as vertical lines** crossing threat/consequence paths
5. **Color coding** (optional):
   - Hardware barriers: Blue
   - Human barriers: Yellow
   - Procedural barriers: Green
   - Degraded/bypassed: Red

**Example ASCII Bow-Tie:**

.. code-block:: text

    THREATS         PREVENTION        HAZARD      MITIGATION      CONSEQUENCES
                    BARRIERS                      BARRIERS
    
    Corrosion ──────║─────────────╔═══════════╗──║──────────── Minor Release
                    ║   Coating   ║           ║  ║  Gas        
                    ║   Inspection║   Loss    ║  ║  Detection  
    Overpressure ───║─────────────║   of      ║──║──────────── Moderate Release
                    ║   PSV       ║ Container ║  ║  ESD        
                    ║   Alarm     ║           ║  ║  Deluge     
    External ───────║─────────────║           ║──║──────────── Major Release
    Impact          ║   Bollards  ║           ║  ║  Evacuation (Fatalities)
                    ║             ╚═══════════╝  ║  Response   
    Overfilling ────║─────────────────────────────║─────────────
                    ║   Level                     ║
                    ║   Interlock                 ║

════════════════════════════════════════════════════════════════════

📖 **3. BOW-TIE EXAMPLE: PROCESS INDUSTRY**
═══════════════════════════════════════════

**3.1 Case Study: Chlorine Storage Tank**
-----------------------------------------

**System:**

- 50-ton chlorine storage tank (liquid under pressure)
- Major Accident Hazard (MAH) — toxic gas
- Nearby residential area (< 1 km)

**Hazard:** Loss of Containment (LOC) — Chlorine Release

**3.2 Threats & Prevention Barriers**
------------------------------------

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │                    PREVENTION (LEFT SIDE)                   │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  THREAT 1: Corrosion (internal/external)                   │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B1: Internal rubber lining                               │
    │  - B2: External paint coating                               │
    │  - B3: Ultrasonic thickness testing (UT) — annual           │
    │  - B4: Dry chlorine spec (< 50 ppm moisture)                │
    │                                                             │
    │  THREAT 2: Overpressure                                     │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B5: Pressure relief valve (PSV-101, set 8 bar)           │
    │  - B6: Pressure transmitter + high alarm (7.5 bar)          │
    │  - B7: High-high pressure interlock (7.8 bar, close inlet)  │
    │  - B8: Pressure gauge (local indication)                    │
    │  - B9: Tank design margin (MAWP 10 bar, normal 6 bar)       │
    │                                                             │
    │  THREAT 3: Overfilling                                      │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B10: Level transmitter + high alarm (85%)                │
    │  - B11: High-high level interlock (90%, stop fill)          │
    │  - B12: Level gauge (local sight glass)                     │
    │  - B13: Fill procedure (checklist, double-check)            │
    │  - B14: Weighing system (mass measurement)                  │
    │                                                             │
    │  THREAT 4: External Impact (vehicle collision)              │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B15: Concrete bollards (crash rated, 50 kph)             │
    │  - B16: Exclusion zone (10m, fenced)                        │
    │  - B17: Speed limit (10 kph, speed bumps)                   │
    │  - B18: Tank elevated on foundation (1.5m high)             │
    │                                                             │
    │  THREAT 5: Equipment Failure (valve, flange leak)           │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B19: Double-block-and-bleed valves                       │
    │  - B20: Spiral-wound gaskets (chlorine service)             │
    │  - B21: Torque wrench procedure (bolt tightening)           │
    │  - B22: Preventive maintenance (PM) schedule (6-month)      │
    │  - B23: Leak detection (chlorine sensor)                    │
    │                                                             │
    │  THREAT 6: Human Error (wrong valve opened)                 │
    │  ──────────────────────────────────────────────────────────│
    │  Barriers:                                                  │
    │  - B24: Valve labeling (color-coded tags)                   │
    │  - B25: Lock-out/Tag-out (LOTO) procedure                   │
    │  - B26: Operator training (chlorine handling certification) │
    │  - B27: Two-person rule (critical operations)               │
    │  - B28: Permit-to-work system (hot work, entry)             │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

**3.3 Consequences & Mitigation Barriers**
------------------------------------------

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │                    MITIGATION (RIGHT SIDE)                  │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  CONSEQUENCE 1: Minor Release (< 100 kg, < 5 min)           │
    │  ──────────────────────────────────────────────────────────│
    │  Mitigation Barriers:                                       │
    │  - M1: Chlorine gas detectors (4 sensors, 1 ppm alarm)      │
    │  - M2: Operator intervention (manual isolation)             │
    │  - M3: Water spray system (neutralization)                  │
    │  - M4: Wind direction monitoring (wind sock)                │
    │  Outcome: Onsite exposure only, no offsite impact           │
    │                                                             │
    │  CONSEQUENCE 2: Moderate Release (100-1000 kg, 5-30 min)    │
    │  ──────────────────────────────────────────────────────────│
    │  Mitigation Barriers:                                       │
    │  - M5: Emergency shutdown (ESD) — auto isolation            │
    │  - M6: Deluge system (water curtain, 300 m³/hr)             │
    │  - M7: Emergency alarm (plant-wide)                         │
    │  - M8: Evacuation procedures (muster points)                │
    │  - M9: Breathing apparatus (SCBA) — 20 sets available       │
    │  - M10: Emergency response team (ERT) — trained, 24/7       │
    │  Outcome: Onsite injuries, plant shutdown, investigation    │
    │                                                             │
    │  CONSEQUENCE 3: Major Release (> 1000 kg, > 30 min)         │
    │  ──────────────────────────────────────────────────────────│
    │  Mitigation Barriers:                                       │
    │  - M11: Community alarm system (sirens, 3 km radius)        │
    │  - M12: Offsite emergency plan (shelter-in-place)           │
    │  - M13: Emergency services notification (fire, police)      │
    │  - M14: Media communication plan (public information)       │
    │  - M15: Incident command system (ICS) activation            │
    │  Outcome: Offsite exposure, evacuations, potential          │
    │           fatalities, regulatory investigation, litigation  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

**3.4 Barrier Performance**
---------------------------

.. code-block:: text

    Barrier Performance Monitoring:
    
    | Barrier | Type      | Test Freq | Last Test | Status |
    |---------|-----------|-----------|-----------|--------|
    | B1      | Hardware  | Visual    | 2026-01-10| ✅ OK  |
    | B3      | Hardware  | Annual UT | 2025-12-05| ✅ OK  |
    | B5      | Hardware  | 6-month   | 2025-07-15| ⚠️OVERDUE|
    | B13     | Procedural| Audit     | 2025-11-20| ✅ OK  |
    | B26     | Human     | Annual    | 2025-09-30| ✅ OK  |
    | M5      | Hardware  | Monthly   | 2026-01-12| ✅ OK  |
    | M10     | Human     | Quarterly | 2025-10-05| ⚠️OVERDUE|
    
    Actions:
    - B5 (PSV): Schedule test ASAP (overdue 6 months)
    - M10 (ERT): Conduct drill this week

════════════════════════════════════════════════════════════════════

📖 **4. BOW-TIE IN DIFFERENT DOMAINS**
══════════════════════════════════════

**4.1 Aviation: Mid-Air Collision**
-----------------------------------

**Hazard:** Mid-Air Collision (MAC)

.. code-block:: text

    THREATS               PREVENTION          MITIGATION
    
    ATC error ────────║───────────╔═══╗───║─────── Partial collision
                      ║  Radar    ║   ║   ║  Evasive  (survivable)
                      ║  TCAS     ║ M ║   ║  maneuver
    Pilot error ──────║───────────║ A ║───║─────── Total loss
    (CFIT)            ║  Training ║ C ║   ║  Emergency (fatalities)
                      ║  SOP      ║   ║   ║  landing
    Weather (IMC) ────║───────────╚═══╝   ║
                      ║  Weather            ║
                      ║  briefing           ║

**Key Barriers:**

- Prevention: TCAS (Traffic Collision Avoidance System), ATC separation
- Mitigation: Evasive maneuver, crashworthiness (limited effectiveness)

**4.2 Automotive: Unintended Acceleration**
-------------------------------------------

**Hazard:** Unintended Acceleration

.. code-block:: text

    THREATS               PREVENTION          MITIGATION
    
    Throttle stuck ───║───────────╔═══╗───║─────── Collision
                      ║  Return   ║   ║   ║  Braking  (injury)
                      ║  spring   ║ U ║   ║  override
    Software fault ───║───────────║ A ║───║─────── Severe crash
                      ║  ASIL D   ║   ║   ║  Airbag   (fatality)
                      ║  testing  ║   ║   ║  deploy
    Pedal misapply ───║───────────╚═══╝   ║
                      ║  Training           ║  Crash    
                      ║  Ergonomics         ║  structure

**Key Barriers:**

- Prevention: Brake override (brake pedal cancels throttle)
- Mitigation: Airbag, crumple zones

**4.3 Medical: Insulin Overdose**
---------------------------------

**Hazard:** Insulin Overdose (Hypoglycemia)

.. code-block:: text

    THREATS               PREVENTION          MITIGATION
    
    Pump malfunction ─║───────────╔═══╗───║─────── Mild symptoms
                      ║  Occlusion║   ║   ║  CGM alert (dizziness)
                      ║  detection║ O ║   ║  Patient  
    Programming ──────║───────────║ D ║───║─────── Seizure
    error             ║  Double   ║   ║   ║  Glucagon (severe)
                      ║  check    ║   ║   ║  injection
    Wrong patient ────║───────────╚═══╝   ║  Emergency (death)
                      ║  Barcode            ║  services
                      ║  scan               ║

**Key Barriers:**

- Prevention: Dose limits (max bolus), barcode patient ID
- Mitigation: Continuous glucose monitor (CGM), glucagon rescue

════════════════════════════════════════════════════════════════════

📖 **5. BARRIER MANAGEMENT**
════════════════════════════

**5.1 Barrier Performance Indicators**
--------------------------------------

**Key Questions for Each Barrier:**

✅ **Availability**: Is the barrier in place and functional?  
✅ **Reliability**: Does it work when demanded? (PFD)  
✅ **Effectiveness**: Does it prevent/mitigate sufficiently?  
✅ **Independence**: Is it independent of other barriers? (CCF)  
✅ **Auditability**: Can we verify it's working?

**Performance Metrics:**

.. code-block:: text

    Example: Pressure Relief Valve (PSV)
    
    - Availability: 99.5% (0.5% unavailable due to maintenance)
    - Reliability: PFD = 1 × 10⁻² (1% probability of failure on demand)
    - Effectiveness: Prevents overpressure in 98% of cases
    - Independence: Independent of process control system
    - Auditability: Tested every 6 months (documented)

**5.2 Barrier Degradation (Escalation Factors)**
------------------------------------------------

**Causes of Barrier Degradation:**

.. code-block:: text

    1. Maintenance Backlog:
       - PSV not tested (overdue)
       - Gas detector calibration expired
       → Barrier effectiveness reduced
    
    2. Management Bypass:
       - Interlock overridden (production pressure)
       - Permit-to-work skipped (time pressure)
       → Barrier defeated
    
    3. Design Limitation:
       - Single PSV (no redundancy)
       - Alarm not annunciated (operator doesn't see)
       → Barrier insufficient
    
    4. Human Factors:
       - Operator fatigue (12-hour shift)
       - Inadequate training (contractor vs employee)
       → Barrier reliability reduced
    
    5. Organizational:
       - Budget cuts (defer maintenance)
       - High turnover (loss of competence)
       → Multiple barriers degraded

**Bow-Tie with Degradation Factors:**

.. code-block:: text

    Add "Escalation Factor Boxes" on barriers:
    
    Threat ────║─── Barrier ───║─── HAZARD
               ║      ▲         ║
               ║      │         ║
               ║  [Degraded?]  ║
               ║   - Bypassed  ║
               ║   - Not tested║

**5.3 Barrier Testing & Verification**
--------------------------------------

**Test Schedule:**

.. code-block:: text

    Barrier Type         Test Frequency        Acceptance Criteria
    ────────────────────────────────────────────────────────────────
    Hardware (PSV)       6 months              Opens at setpoint ±3%
    Hardware (ESD)       Monthly (partial)     Response time < 2 sec
    Detection (gas)      Weekly (bump test)    Alarm at 1 ppm ±10%
    Human (drill)        Quarterly             < 5 min muster time
    Procedural (audit)   Annual                100% compliance
    Design (review)      Major change (MOC)    Meets code (ASME)

════════════════════════════════════════════════════════════════════

📖 **6. BOW-TIE TOOLS & SOFTWARE**
══════════════════════════════════

**6.1 Commercial Tools**
------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Features**               |
+======================+==================+============================+
| **BowTieXP**         | CGE Risk Mgmt    | Industry standard, LOPA    |
|                      |                  | integration                |
+----------------------+------------------+----------------------------+
| **Risktec BowTie**   | Risktec          | Offshore oil & gas focus   |
+----------------------+------------------+----------------------------+
| **THESIS**           | ASAP Group       | Safety case management     |
+----------------------+------------------+----------------------------+
| **Cameo Safety**     | PTC              | Systems engineering        |
|                      |                  | integration                |
+----------------------+------------------+----------------------------+

**6.2 Python Bow-Tie Visualizer**
---------------------------------

.. code-block:: python

    # bowtie_visualizer.py (using Graphviz)
    
    from graphviz import Digraph
    
    class BowTie:
        def __init__(self, hazard: str):
            self.hazard = hazard
            self.threats = []
            self.consequences = []
            self.prevention_barriers = {}  # threat -> [barriers]
            self.mitigation_barriers = {}  # consequence -> [barriers]
        
        def add_threat(self, threat: str, barriers: list):
            self.threats.append(threat)
            self.prevention_barriers[threat] = barriers
        
        def add_consequence(self, consequence: str, barriers: list):
            self.consequences.append(consequence)
            self.mitigation_barriers[consequence] = barriers
        
        def render(self, filename='bowtie'):
            dot = Digraph(comment='Bow-Tie Diagram')
            dot.attr(rankdir='LR')  # Left to right
            dot.attr('node', shape='box')
            
            # Central hazard
            dot.node('HAZ', self.hazard, shape='box', 
                     style='filled', fillcolor='red', fontcolor='white',
                     fontsize='16', width='2', height='1')
            
            # Threats (left)
            for i, threat in enumerate(self.threats):
                t_id = f'T{i}'
                dot.node(t_id, threat, fillcolor='yellow', style='filled')
                
                # Prevention barriers
                for j, barrier in enumerate(self.prevention_barriers[threat]):
                    b_id = f'B{i}_{j}'
                    dot.node(b_id, barrier, shape='ellipse', 
                             fillcolor='lightblue', style='filled')
                    dot.edge(t_id, b_id)
                    dot.edge(b_id, 'HAZ')
            
            # Consequences (right)
            for i, consequence in enumerate(self.consequences):
                c_id = f'C{i}'
                dot.node(c_id, consequence, fillcolor='orange', style='filled')
                
                # Mitigation barriers
                for j, barrier in enumerate(self.mitigation_barriers[consequence]):
                    m_id = f'M{i}_{j}'
                    dot.node(m_id, barrier, shape='ellipse',
                             fillcolor='lightgreen', style='filled')
                    dot.edge('HAZ', m_id)
                    dot.edge(m_id, c_id)
            
            # Render
            dot.render(filename, format='png', cleanup=True)
            print(f"Bow-Tie diagram saved: {filename}.png")
    
    # Example usage
    if __name__ == "__main__":
        bt = BowTie("Loss of Containment\n(Chlorine Release)")
        
        # Add threats with prevention barriers
        bt.add_threat("Corrosion", 
                      ["Coating", "UT Inspection", "Inhibitor"])
        bt.add_threat("Overpressure", 
                      ["PSV", "High Alarm", "Interlock"])
        bt.add_threat("External Impact", 
                      ["Bollards", "Exclusion Zone"])
        
        # Add consequences with mitigation barriers
        bt.add_consequence("Minor Release", 
                           ["Gas Detection", "Water Spray"])
        bt.add_consequence("Major Release", 
                           ["ESD", "Evacuation", "ERT"])
        
        bt.render('chlorine_bowtie')

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the key difference between prevention and mitigation barriers in a Bow-Tie?

**A1:**

- **Prevention Barriers (Left)**: Stop threats from causing the hazard  
  Example: Pressure relief valve prevents overpressure
- **Mitigation Barriers (Right)**: Reduce severity of consequences after hazard occurs  
  Example: Fire suppression reduces fire damage

────────────────────────────────────────────────────────────────────

**Q2:** What are "escalation factors" in Bow-Tie analysis?

**A2:**

Conditions that degrade or defeat barriers, increasing risk:
- Maintenance backlog (barrier not tested)
- Management override (bypass interlock)
- Inadequate training (human barrier ineffective)
- Budget cuts (deferred maintenance)

────────────────────────────────────────────────────────────────────

**Q3:** How does Bow-Tie integrate FTA and ETA?

**A3:**

- **Left side (FTA)**: Threats → Prevention → Hazard (backward causation)
- **Right side (ETA)**: Hazard → Mitigation → Consequences (forward progression)
- **Single diagram**: Combines both in one visual (bow-tie shape)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Hazard Selection:**
- [ ] Identify Major Accident Hazard (MAH) — high consequence
- [ ] Define hazard scope (specific event, not general "fire")
- [ ] Engage stakeholders (operations, safety, management)

**Threat Analysis:**
- [ ] Identify all threats (causes of hazard)
- [ ] Use HAZOP, FMEA, incident data
- [ ] Prioritize threats (frequency, severity)

**Prevention Barriers:**
- [ ] For each threat, list controls
- [ ] Classify barriers (hardware, human, procedural, design)
- [ ] Verify independence (avoid common cause failures)
- [ ] Assign performance metrics (PFD, test frequency)

**Consequence Analysis:**
- [ ] Identify escalation paths (minor, moderate, major)
- [ ] Consider worst-case conditions (wind, time of day)
- [ ] Estimate consequences (fatalities, environmental, financial)

**Mitigation Barriers:**
- [ ] For each consequence, list controls
- [ ] Detection (early warning)
- [ ] Response (emergency shutdown, firefighting)
- [ ] Escape/evacuation (muster, shelter-in-place)

**Bow-Tie Diagram:**
- [ ] Draw diagram (hazard center, threats left, consequences right)
- [ ] Add barriers as vertical lines crossing paths
- [ ] Color-code barrier types (hardware, human, procedural)
- [ ] Review with team (operations, maintenance, safety)

**Barrier Management:**
- [ ] Define test schedule for each barrier
- [ ] Track barrier performance (availability, reliability)
- [ ] Identify degradation factors (escalation factors)
- [ ] Implement corrective actions (overdue tests, bypassed barriers)
- [ ] Periodic review (annual, or after incident)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Bow-Tie = FTA + ETA** → Single visual combining causes and consequences

2️⃣ **Barriers are central** → Prevention (left) + Mitigation (right)

3️⃣ **Communication tool** → Simple visual for management, regulators

4️⃣ **Barrier management** → Track performance, testing, degradation

5️⃣ **Process industry** → Standard for Major Accident Hazards (MAH)

6️⃣ **Escalation factors** → Show how barriers degrade (maintenance, bypass)

7️⃣ **Living document** → Update after incidents, design changes, audits

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **BOW-TIE ANALYSIS CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Bow-Tie fundamentals, construction process, barrier types,  
chlorine tank example, aviation/automotive/medical applications, barrier  
management, degradation factors, tools, Python visualizer

════════════════════════════════════════════════════════════════════
