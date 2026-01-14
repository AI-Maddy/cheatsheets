📋 **Fail-Safe Architecture**
═══════════════════════════════════════════════════════════════════

**Full Name:** Fail-Safe Design (Safety by Default)  
**Type:** Architectural pattern for passive safety  
**Principle:** System defaults to safe state upon failure  
**Standards:** IEC 61508, ISO 13849, EN 50129, IEC 62061

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — FAIL-SAFE ARCHITECTURE IN 60 SECONDS**
───────────────────────────────────────────────────

**What is Fail-Safe Design?**

::

    Fail-Safe = System automatically transitions to safe state
                when failure occurs (no active intervention needed)
    
    Key principle: Safety by DEFAULT, not by CONTROL
    
    Example: Railway signal defaults to RED (stop) when power fails
             → Trains stop → No collision

**Safe State:**

- **Definition**: System condition that prevents hazard
- **Characteristics**:
  - Stable (remains safe without power/control)
  - Achievable (physically possible to reach)
  - Maintainable (stays safe until recovery)

**Fail-Safe Strategies (4 types):**

1. **De-Energize to Safe**: Power loss → safe (spring-return, gravity)
2. **Mechanical Default**: Physical design forces safe state
3. **Redundant Safe Path**: Failure → switch to always-safe channel
4. **Watchdog Failsafe**: Loss of heartbeat → safe shutdown

**Fail-Safe vs Fail-Operational:**

+-------------------+---------------------------+---------------------------+
| **Aspect**        | **Fail-Safe**             | **Fail-Operational**      |
+===================+===========================+===========================+
| **Goal**          | Reach safe state          | Continue operation        |
+-------------------+---------------------------+---------------------------+
| **Example**       | E-stop → halt             | Aircraft: fly with 1/3    |
|                   |                           | engines failed            |
+-------------------+---------------------------+---------------------------+
| **Complexity**    | Low (passive)             | High (active redundancy)  |
+-------------------+---------------------------+---------------------------+
| **Cost**          | Low                       | High                      |
+-------------------+---------------------------+---------------------------+
| **Applicability** | Safe state exists         | No safe state (mission    |
|                   | (can shut down)           | critical)                 |
+-------------------+---------------------------+---------------------------+

**When to Use Fail-Safe:**

✅ Safe state exists and is acceptable  
✅ Mission abort is tolerable  
✅ Lower cost/complexity preferred  
✅ Passive safety required (no active control)

**When NOT to Use:**

❌ No safe state (aircraft in flight)  
❌ Shutdown unacceptable (life support)  
❌ High availability required

════════════════════════════════════════════════════════════════════

📖 **1. FAIL-SAFE PRINCIPLES**
══════════════════════════════

**1.1 De-Energize to Safe**
---------------------------

**Principle:** Loss of power/signal → Safe state

**Mechanism:**

- Spring-return actuators
- Gravity-operated devices
- Normally-open/normally-closed relays
- Magnetic holding (loss of current → release)

**Examples:**

+------------------------+-------------------------+---------------------------+
| **System**             | **Energized State**     | **De-Energized (Safe)**   |
+========================+=========================+===========================+
| Railway signal         | GREEN (proceed)         | RED (stop)                |
+------------------------+-------------------------+---------------------------+
| Elevator brake         | Released (moving)       | Engaged (stopped)         |
+------------------------+-------------------------+---------------------------+
| Machine guard          | Unlocked (operating)    | Locked (safe)             |
+------------------------+-------------------------+---------------------------+
| Fire door              | Open (normal use)       | Closed (fire protection)  |
+------------------------+-------------------------+---------------------------+
| Pneumatic valve        | Open (flow)             | Closed (isolated)         |
+------------------------+-------------------------+---------------------------+

**Railway Signal Example:**

.. code-block:: text

    NORMAL OPERATION:
    
    [Power]──→[Relay Coil]──→[Energized]
                   │
                   └──→ [Relay Contacts Closed]
                             │
                             └──→ [GREEN lamp ON]
                                  [RED lamp OFF]
    
    FAILURE (Power Loss):
    
    [Power FAIL]──X──[Relay Coil]──→[De-Energized]
                         │
                         └──→ [Relay Contacts OPEN (spring return)]
                                   │
                                   ├──→ [GREEN lamp OFF]
                                   └──→ [RED lamp ON (always-powered circuit)]
    
    Result: Signal shows RED → Train stops → SAFE ✅

**1.2 Mechanical Defaults**
---------------------------

**Principle:** Physical design inherently creates safe state

**Examples:**

1. **Deadman Switch (Train/Bus):**
   - Operator must hold button to move
   - Release button → Spring returns → Power cut → Brakes engage → STOP

2. **Elevator Over-Speed Governor:**
   - Centrifugal force at normal speed: Weights held in
   - Excessive speed: Weights fly out → Trigger safety brake → STOP

3. **Pressure Relief Valve:**
   - Normal pressure: Valve closed (spring force)
   - Over-pressure: Spring compressed → Valve opens → Vent gas → SAFE

4. **Guillotine Safety Guard:**
   - Gravity: Guard falls to closed position
   - Operator must lift guard (and hold) to access danger zone
   - Release → Guard falls → Machine stops (interlock) → SAFE

**1.3 Redundant Safe Path**
---------------------------

**Principle:** Failure in primary path → Switch to always-safe channel

**Example: Nuclear Reactor Shutdown**

.. code-block:: text

    PRIMARY PATH (Active Control):
    [Operator]──→[Computer]──→[Withdraw Control Rods]──→[Reactor CRITICAL]
                                   ↑
                                   │ (Active control required)
    
    SAFE PATH (Passive - Gravity):
    [Computer Failure Detected]──→[Release Electromagnets]
                                        │
                                        └──→[Control Rods DROP (gravity)]
                                                    │
                                                    └──→[Reactor SHUTDOWN]
    
    Result: Any failure → Rods drop → Reactor shuts down → SAFE ✅

**1.4 Watchdog Failsafe**
-------------------------

**Principle:** Loss of periodic "heartbeat" → Safe shutdown

**Architecture:**

.. code-block:: text

    [Main Controller]──→ Heartbeat pulse (every 100ms) ──→[Watchdog Timer]
                                                                  │
                                                                  ├─ Heartbeat OK
                                                                  │  → Enable Outputs
                                                                  │
                                                                  └─ Heartbeat MISSING
                                                                     → Timeout (300ms)
                                                                     → Disable Outputs
                                                                     → Safe Shutdown

**Example: Industrial Robot**

- Main CPU sends heartbeat every 100ms
- Watchdog timer resets on each heartbeat
- If 300ms pass without heartbeat:
  - CPU crashed / software hung / power lost
  - Watchdog expires → Cuts motor power → Brakes engage → SAFE

════════════════════════════════════════════════════════════════════

📖 **2. FAIL-SAFE EXAMPLES BY DOMAIN**
══════════════════════════════════════

**2.1 Railway Interlocking**
----------------------------

**System:** Railway signal and point (switch) control

**Hazard:** Conflicting routes → Collision

**Fail-Safe Design:**

+------------------------+-------------------------+---------------------------+
| **Component**          | **Energized (Normal)**  | **De-Energized (Safe)**   |
+========================+=========================+===========================+
| **Signal Aspect**      | GREEN (proceed)         | RED (stop) — DEFAULT      |
+------------------------+-------------------------+---------------------------+
| **Point Lock**         | UNLOCKED (moveable)     | LOCKED (fixed position)   |
+------------------------+-------------------------+---------------------------+
| **Track Circuit**      | Current flows →         | No current → "Occupied"   |
|                        | "Clear" (no train)      | (assume train present)    |
+------------------------+-------------------------+---------------------------+
| **Relay Logic**        | Multiple relays in      | Any relay drop →          |
|                        | series (all energized   | Signal RED                |
|                        | for GREEN)              |                           |
+------------------------+-------------------------+---------------------------+

**Signal Logic (Fail-Safe):**

.. code-block:: text

    Signal shows GREEN if and only if ALL conditions met:
    
    [Route Set]──→ Relay R1 ENERGIZED
        AND
    [Points Locked]──→ Relay R2 ENERGIZED
        AND
    [Track Clear]──→ Relay R3 ENERGIZED
        AND
    [Approach Clear]──→ Relay R4 ENERGIZED
        AND
    [Signal Lamp OK]──→ Relay R5 ENERGIZED
    
    ┌───────────────────────────────────────────┐
    │  R1 ──┬── R2 ──┬── R3 ──┬── R4 ──┬── R5  │──→ GREEN Lamp
    │       │        │        │        │        │
    └───────────────────────────────────────────┘
    
    If ANY relay drops out:
    - Circuit open → GREEN lamp OFF → RED lamp ON (fail-safe) → SAFE ✅

**Point (Switch) Locking:**

- Spring-loaded mechanism: Locks points in last-set position
- Power required to UNLOCK points (for movement)
- Power loss → Points remain LOCKED → Trains cannot diverge unexpectedly → SAFE

**Track Circuit Fail-Safe:**

- Track circuit: Current through rails detects train (wheels shunt circuit)
- Normal (no train): Current flows → Relay energized → "Track Clear"
- Train present: Wheels shunt circuit → Current drops → Relay de-energizes → "Track Occupied"
- **Fail-Safe:** Broken rail (wire break, relay failure) → Current stops → Indicates "Occupied" (conservative) → SAFE

**2.2 Automotive Brake-by-Wire**
--------------------------------

**System:** Electronic brake actuation (no mechanical linkage)

**Hazard:** Loss of braking → Crash

**Fail-Safe Design:**

.. code-block:: text

    PRIMARY: Electronic Brake Control
    [Brake Pedal Sensor]──→[ECU]──→[Electric Actuator]──→[Brake Caliper]
    
    FAIL-SAFE: Mechanical Backup + Spring Brake
    
    IF (ECU fails OR Power loss OR Sensor fault):
        1. Spring-applied brake engages (parking brake)
        2. Mechanical linkage (backup cable) activates
        3. Driver applies force directly to master cylinder
    
    Result: Braking ALWAYS available → SAFE ✅

**Spring-Applied Brake:**

- Parking brake held OPEN by electric actuator
- Power loss → Actuator releases → Spring applies brake → Vehicle stops
- Fail-safe: De-energize to BRAKED (not released)

**2.3 Elevator Safety System**
------------------------------

**System:** Elevator car and counterweight

**Hazards:**
- H-1: Overspeed (cable break, drive failure)
- H-2: Uncontrolled descent

**Fail-Safe Design (3 layers):**

**Layer 1: Governor (Mechanical Fail-Safe)**

.. code-block:: text

    [Governor Pulley]──→ Rotates with elevator speed
              │
              ├─ Normal speed (<1.25 m/s): Centrifugal weights HELD IN
              │                             → No action
              │
              └─ Overspeed (>1.50 m/s): Centrifugal weights FLY OUT
                                        → Trigger safety mechanism
                                        → Pull cable
                                        → Engage SAFETY BRAKE (wedges)
                                        → Car STOPS on guide rails
                                        → SAFE ✅
    
    Note: PURELY MECHANICAL (no electronics, no power needed)

**Layer 2: Electromagnetic Brake (De-Energize to Safe)**

- Normal operation: Electromagnet HOLDS brake pads OPEN → Car can move
- Power loss: Electromagnet de-energizes → Spring applies brake → Car STOPS
- Fail-safe: Power required to RELEASE brake (not to apply)

**Layer 3: Final Limit Switches (Mechanical)**

- Top/bottom limit switches (mechanical)
- If car reaches extreme position (control system failure):
  - Limit switch physically interrupts power → Motor stops → Brake engages → SAFE

**2.4 Process Industry: Emergency Shutdown (ESD)**
--------------------------------------------------

**System:** Chemical reactor pressure control

**Hazard:** Over-pressure → Vessel rupture → Explosion

**Fail-Safe ESD Design:**

.. code-block:: text

    NORMAL OPERATION:
    [PLC Control]──→ Energizes solenoid valve ──→ Air pressure ──→ Valve OPEN
                                                                   (process fluid flows)
    
    EMERGENCY (High Pressure Detected OR Power Failure):
    [Pressure > 8 bar]──→ De-energize solenoid ──→ Air vented ──→ Spring closes valve
                                                                   → Flow STOPPED
                                                                   → Pressure relieved
                                                                   → SAFE ✅
    
    Additionally:
    [Pressure > 9 bar]──→ Pressure Safety Valve (PSV) ──→ Opens mechanically
                                                          (spring-loaded, no power)
                                                          → Vents to flare
                                                          → SAFE ✅

**Fail-Safe Valve Types:**

+------------------------+-------------------------+---------------------------+
| **Valve Type**         | **Fail Position**       | **Application**           |
+========================+=========================+===========================+
| **Fail-Closed (FC)**   | De-energize → CLOSED    | Isolate hazardous flow    |
|                        | (spring closes)         | (shutdown, fire)          |
+------------------------+-------------------------+---------------------------+
| **Fail-Open (FO)**     | De-energize → OPEN      | Emergency cooling water,  |
|                        | (spring opens)          | fire suppression          |
+------------------------+-------------------------+---------------------------+
| **Fail-Last (FL)**     | De-energize → STAYS     | Non-critical (but rare    |
|                        | in last position        | in safety systems)        |
|                        | (locked)                |                           |
+------------------------+-------------------------+---------------------------+

**2.5 Nuclear: Negative Temperature Coefficient**
-------------------------------------------------

**System:** Nuclear reactor fuel design

**Hazard:** Power excursion → Core melt

**Fail-Safe Design (Passive Physics):**

.. code-block:: text

    Temperature increases (due to higher power)
            │
            └──→ Fuel temperature ↑
                        │
                        └──→ Doppler broadening (nuclear physics effect)
                                    │
                                    └──→ Neutron absorption ↑
                                                │
                                                └──→ Reactivity ↓
                                                            │
                                                            └──→ Power ↓
                                                                    │
                                                                    └──→ STABLE ✅
    
    Self-regulating: Higher power → Negative feedback → Power decreases
    Passive safety: No operator action, no control system needed

**Negative Reactivity Coefficient:**

- α_T = Δρ / ΔT < 0 (negative)
- Example: α_T = -5 pcm/°C (5 per-cent milli reactivity per degree Celsius)
- If T increases by 100°C: Reactivity decreases by -500 pcm → Power drops
- **Fail-safe:** Physics automatically limits power (inherent safety)

════════════════════════════════════════════════════════════════════

📖 **3. FAIL-SAFE ELECTRONICS**
═══════════════════════════════

**3.1 Relay Logic (Fail-Safe by Design)**
-----------------------------------------

**Principle:** Use relay contact configuration for fail-safe

**Normally-Open (NO) vs Normally-Closed (NC):**

.. code-block:: text

    NORMALLY-OPEN (NO):
    Relay coil DE-ENERGIZED → Contacts OPEN (no continuity)
    Relay coil ENERGIZED    → Contacts CLOSE (continuity)
    
    Use for: Signals that must be actively maintained
    Example: GREEN signal (must actively energize to show GREEN)
    
    
    NORMALLY-CLOSED (NC):
    Relay coil DE-ENERGIZED → Contacts CLOSED (continuity)
    Relay coil ENERGIZED    → Contacts OPEN (no continuity)
    
    Use for: Safe indications
    Example: "Track Occupied" indication (fail-safe to assume occupied)

**Railway Signal Fail-Safe Relay Logic:**

.. code-block:: text

    GREEN Signal Lamp Circuit:
    
    [+24V]──→[R1-NO]──→[R2-NO]──→[R3-NO]──→[R4-NO]──→[GREEN Lamp]──→[GND]
    
    Where:
    - R1 = Route set relay (NO contact)
    - R2 = Points locked relay (NO contact)
    - R3 = Track clear relay (NO contact)
    - R4 = Approach clear relay (NO contact)
    
    All relays must be ENERGIZED for GREEN lamp to light.
    Any relay failure → De-energizes → Contact opens → GREEN OFF → RED ON (default)
    
    RED Signal Lamp Circuit:
    
    [+24V]──→[RED Lamp]──→[R1-NC]──→[R2-NC]──→[R3-NC]──→[R4-NC]──→[GND]
             ↑                ↑          ↑          ↑          ↑
             │                │          │          │          │
             └────────────────┴──────────┴──────────┴──────────┘
             OR circuit: RED lamp ON if ANY relay DE-ENERGIZED
    
    Result: Default state (all relays off) → RED lamp ON → SAFE ✅

**3.2 Solid-State Fail-Safe Design**
------------------------------------

**Challenge:** Transistors/MOSFETs can fail shorted (conducting) or open

**Solution 1: Dual-Channel Monitored**

.. code-block:: text

    [Control Signal]──→ [MOSFET A]──┬──→ [Load]
                                     │
                    [MOSFET B]───────┘
                         ↑
                         │
                    [Cross-Monitor]──→ Detect if A or B fails shorted
    
    Normal: Both MOSFETs on/off together
    Fault: If one fails shorted → Detected → Safe shutdown

**Solution 2: Current Monitoring**

.. code-block:: text

    [Control Signal]──→[MOSFET]──→[Load]──→[Current Sensor]──→[Monitor]
                                                                    │
                                                                    └─→ If current
                                                                        unexpected
                                                                        → Shutdown

**3.3 Watchdog Timer Architecture**
-----------------------------------

**Purpose:** Detect CPU hang, software crash, infinite loop

**Architecture:**

.. code-block:: text

    ┌─────────────────────────────────────────────────────────┐
    │  Main CPU                                               │
    │                                                         │
    │  while(1) {                                             │
    │      // Main control loop                              │
    │      control_system();                                 │
    │      read_sensors();                                   │
    │      write_outputs();                                  │
    │                                                         │
    │      // Kick watchdog (reset timer)                    │
    │      watchdog_reset();   ────────────────────┐         │
    │  }                                            │         │
    └───────────────────────────────────────────────┼─────────┘
                                                    │
                                                    ↓
                                        ┌───────────────────────┐
                                        │   Watchdog Timer      │
                                        │                       │
                                        │  Timeout = 300 ms     │
                                        │                       │
                                        │  Reset signal         │
                                        │  → Restart timer      │
                                        │                       │
                                        │  No reset for 300ms   │
                                        │  → TIMEOUT            │
                                        │  → Assert SAFE signal │
                                        └───────────┬───────────┘
                                                    │
                                                    ↓
                                        ┌───────────────────────┐
                                        │  Safety Output Driver │
                                        │                       │
                                        │  SAFE signal asserted │
                                        │  → Disable outputs    │
                                        │  → Engage brakes      │
                                        │  → Open relays        │
                                        │  → SAFE STATE ✅      │
                                        └───────────────────────┘

**Window Watchdog (Advanced):**

- Simple watchdog: Kick anytime → Prevents only "CPU stopped"
- Window watchdog: Must kick within time window (e.g., 200-300ms)
  - Too early kick → Fault (software running too fast, skipped code)
  - Too late kick → Fault (software running too slow, infinite loop)
  - Correct window → OK

**Example: Industrial Robot Watchdog**

- Main CPU sends heartbeat every 100 ms ±10 ms
- Window watchdog expects heartbeat between 90-110 ms
- If heartbeat outside window (or missing): Watchdog expires → Cut motor power → Engage brakes → SAFE

════════════════════════════════════════════════════════════════════

📖 **4. FAIL-SAFE ANALYSIS & VERIFICATION**
═══════════════════════════════════════════

**4.1 Failure Mode Analysis**
-----------------------------

**Goal:** Verify all credible failure modes → Safe state

**Method:**

1. Identify all components
2. For each component, list failure modes:
   - Open circuit
   - Short circuit
   - Stuck-at (high/low)
   - Drift (out of tolerance)
   - Mechanical jam
3. For each failure mode, trace effect:
   - Does system reach safe state? ✅
   - Does system reach unsafe state? ❌ (redesign needed)

**Example: Railway Signal Relay**

+-------------------+---------------------+---------------------------+------------+
| **Component**     | **Failure Mode**    | **Effect**                | **Safe?**  |
+===================+=====================+===========================+============+
| Relay R1          | Coil open circuit   | Relay de-energizes →      | ✅ Yes     |
|                   |                     | GREEN OFF, RED ON         |            |
+-------------------+---------------------+---------------------------+------------+
| Relay R1          | Contact welded      | GREEN stays ON            | ❌ NO!     |
|                   | (shorted)           | (unsafe)                  | → Need     |
|                   |                     |                           | monitoring |
+-------------------+---------------------+---------------------------+------------+
| GREEN lamp        | Filament broken     | No GREEN display →        | ✅ Yes     |
|                   |                     | Driver sees RED           |            |
+-------------------+---------------------+---------------------------+------------+
| Wire to relay     | Break (open)        | Relay de-energizes →      | ✅ Yes     |
|                   |                     | RED ON                    |            |
+-------------------+---------------------+---------------------------+------------+

**Failure Mode Coverage:**

- ✅ **Fail-safe failures**: 75% (3/4 modes → safe)
- ❌ **Unsafe failure**: Welded relay contact (1/4 modes)
- **Mitigation**: Add contact monitoring (detect stuck contact)

**4.2 Fault Injection Testing**
-------------------------------

**Goal:** Verify fail-safe behavior by intentionally injecting faults

**Method:**

1. Disconnect power
2. Cut wires
3. Short circuits
4. Jam mechanisms
5. Simulate sensor failures

**Example: Elevator Safety Test**

.. code-block:: text

    Test 1: Power Loss
    - Disconnect main power during ascent
    - Expected: Electromagnetic brake engages → Car stops
    - Result: ✅ PASS (stopped in 0.3 sec)
    
    Test 2: Governor Overspeed
    - Simulate cable break (release car, let fall)
    - Expected: Governor trips → Safety brake wedges engage
    - Result: ✅ PASS (stopped in 1.5 m)
    
    Test 3: Brake Coil Open
    - Disconnect brake coil wire
    - Expected: Brake engages (spring-applied)
    - Result: ✅ PASS (brake engaged immediately)
    
    Test 4: Final Limit Switch
    - Drive car past normal limit
    - Expected: Mechanical switch cuts power → Car stops
    - Result: ✅ PASS (stopped at limit)

**4.3 Common Cause Failure Analysis**
-------------------------------------

**Risk:** Multiple fail-safe mechanisms fail simultaneously

**Example: Railway Signal (Single Power Supply)**

.. code-block:: text

    All relays powered by single 24V supply:
    
    [24V Supply]──┬──→ Relay R1 (Route)
                  ├──→ Relay R2 (Points)
                  ├──→ Relay R3 (Track)
                  └──→ Relay R4 (Approach)
    
    Common Cause Failure: 24V supply fails
    → All relays de-energize
    → All signals show RED
    → SAFE ✅ (but: all trains stopped, no movement)
    
    Result: Fail-safe to RED (correct), but availability impacted

**Mitigation:** Independent power supplies for critical paths

**4.4 Safety Integrity Level (SIL) Calculation**
------------------------------------------------

**Goal:** Quantify fail-safe effectiveness

**Metrics:**

- **PFH** (Probability of dangerous Failure per Hour)
- **PFD** (Probability of Failure on Demand)

**SIL Levels (IEC 61508):**

+-------------+-------------------------+-------------------------+
| **SIL**     | **PFH** (per hour)      | **PFD** (on demand)     |
+=============+=========================+=========================+
| **SIL 4**   | 10⁻⁹ to 10⁻⁸            | 10⁻⁵ to 10⁻⁴            |
+-------------+-------------------------+-------------------------+
| **SIL 3**   | 10⁻⁸ to 10⁻⁷            | 10⁻⁴ to 10⁻³            |
+-------------+-------------------------+-------------------------+
| **SIL 2**   | 10⁻⁷ to 10⁻⁶            | 10⁻³ to 10⁻²            |
+-------------+-------------------------+-------------------------+
| **SIL 1**   | 10⁻⁶ to 10⁻⁵            | 10⁻² to 10⁻¹            |
+-------------+-------------------------+-------------------------+

**Example: Emergency Stop Button (SIL 3 Required)**

.. code-block:: text

    Components:
    - E-stop button:    λ_D = 1×10⁻⁷/hr (dangerous failure rate)
    - Relay (NC):       λ_D = 5×10⁻⁸/hr
    - Final contactor:  λ_D = 2×10⁻⁸/hr
    
    Series Architecture (all must work for safe shutdown):
    PFH = λ_D1 + λ_D2 + λ_D3
        = 1×10⁻⁷ + 5×10⁻⁸ + 2×10⁻⁸
        = 1.7×10⁻⁷/hr
    
    Check against SIL 3 requirement: 10⁻⁸ to 10⁻⁷/hr
    Result: 1.7×10⁻⁷/hr exceeds SIL 3 upper bound ❌
    
    Mitigation: Add redundant channel (dual-channel architecture)
    PFH (dual) ≈ (1.7×10⁻⁷)² / (2 × 1 year)
               ≈ 3×10⁻⁹/hr
    Result: ✅ Meets SIL 3 (within 10⁻⁸ to 10⁻⁷/hr)

════════════════════════════════════════════════════════════════════

📝 **5. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between fail-safe and fail-operational?

**A1:**

- **Fail-Safe**: System transitions to safe state upon failure
  - Safe state exists (can shut down)
  - Example: Railway signal → RED (stop)
  - Lower cost, simpler design
  - Acceptable mission abort

- **Fail-Operational**: System continues operating despite failure
  - No safe state (must continue operation)
  - Example: Aircraft in flight (cannot land immediately)
  - Higher cost, complex (redundancy required)
  - Mission-critical

────────────────────────────────────────────────────────────────────

**Q2:** Why do railway signals default to RED (not GREEN)?

**A2:**

**Fail-Safe Principle:**

- Power/control required to show GREEN (proceed)
- Power loss/failure → Signal de-energizes → Defaults to RED (stop)
- RED is the SAFE state (trains stop → no collision)

**Implementation:**

- Relay logic: Multiple relays in series (NO contacts)
- All relays must be energized for GREEN
- Any relay drop-out → GREEN OFF, RED ON (default)
- Fail-safe to most restrictive aspect (RED)

────────────────────────────────────────────────────────────────────

**Q3:** How does a watchdog timer provide fail-safe protection?

**A3:**

**Mechanism:**

1. Main CPU sends periodic "heartbeat" (e.g., every 100ms)
2. Watchdog timer resets on each heartbeat
3. If heartbeat missing for timeout period (e.g., 300ms):
   - CPU crashed, software hung, or power lost
   - Watchdog expires → Asserts SAFE signal
   - Disables outputs, engages brakes, opens safety relays
   - System reaches safe state

**Fail-Safe Property:**

- Watchdog is INDEPENDENT of main CPU
- Separate power, separate oscillator
- Defaults to safe state if main control fails
- No action from main CPU = SAFE (not dangerous)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Design Phase:**
- [ ] Identify safe state for each hazard
- [ ] Verify safe state is stable (no active control needed)
- [ ] Choose fail-safe mechanism (de-energize, mechanical default, watchdog)
- [ ] Design de-energize-to-safe components (spring-return, gravity, normally-open)
- [ ] Specify fail position for valves/actuators (fail-open vs fail-closed)

**Analysis Phase:**
- [ ] Perform failure mode analysis (FMEA) on all components
- [ ] Verify all credible failures → safe state
- [ ] Identify unsafe failures (e.g., welded relay contacts)
- [ ] Mitigate unsafe failures (monitoring, redundancy)
- [ ] Calculate SIL/PFH (confirm meets target)

**Verification Phase:**
- [ ] Fault injection testing (disconnect power, cut wires, jam mechanisms)
- [ ] Verify fail-safe behavior for all failure modes
- [ ] Test watchdog timeout (ensure safe shutdown)
- [ ] Common cause failure analysis (single point failures)
- [ ] Independent safety assessment

**Documentation:**
- [ ] Document safe state definition for each hazard
- [ ] Failure mode table (mode → effect → safe?)
- [ ] Test results (fault injection pass/fail)
- [ ] SIL calculation (PFH/PFD analysis)
- [ ] Safety case argument (fail-safe pattern)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Fail-safe = De-energize to safe** → Power loss → Safe state (passive)

2️⃣ **Safe state must exist** → Not applicable if no safe state (aircraft, life support)

3️⃣ **Mechanical defaults preferred** → Spring-return, gravity (no electronics)

4️⃣ **Railway signal principle** → Default RED (safe), power needed for GREEN

5️⃣ **Normally-open relays** → Series NO contacts for safety logic (any drop → safe)

6️⃣ **Watchdog timer** → Independent monitor, timeout → safe shutdown

7️⃣ **Verify all failure modes** → FMEA + fault injection testing

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **FAIL-SAFE ARCHITECTURE CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Fail-safe principles (de-energize, mechanical defaults, redundant safe  
path, watchdog), domain examples (railway interlocking, brake-by-wire, elevator,  
ESD, nuclear), fail-safe electronics (relay logic, solid-state, watchdog timer),  
analysis & verification (failure mode analysis, fault injection, CCF, SIL calculation)

════════════════════════════════════════════════════════════════════
