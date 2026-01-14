📋 **Fail-Operational Architecture**
═══════════════════════════════════════════════════════════════════

**Full Name:** Fail-Operational System Design  
**Type:** Architectural pattern for continuous operation  
**Principle:** System continues essential functions despite component failures  
**Standards:** DO-178C/DO-254, ISO 26262, ARP4754A, IEC 61508

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — FAIL-OPERATIONAL IN 60 SECONDS**
─────────────────────────────────────────────

**What is Fail-Operational?**

::

    Fail-Operational = System continues to provide essential functions
                       despite one or more component failures
    
    Key principle: CONTINUOUS OPERATION, not shutdown to safe state
    
    Example: Aircraft fly-by-wire remains functional with 1 of 3 channels failed
             → Pilot retains control → Safe landing possible

**When Fail-Operational is Required:**

✅ **No safe state exists** (aircraft in flight, life support)  
✅ **Mission abort unacceptable** (spacecraft, autonomous vehicle)  
✅ **High availability critical** (medical implant, power grid)

**Core Techniques:**

1. **Redundancy**: Multiple channels (TMR = Triple Modular Redundancy)
2. **Voting**: Majority voter selects correct output
3. **Fault Detection**: Identify failed channel
4. **Reconfiguration**: Disable failed channel, continue with remaining
5. **Graceful Degradation**: Reduced capability if multiple failures

**Fail-Operational vs Fail-Safe:**

+-------------------+---------------------------+---------------------------+
| **Aspect**        | **Fail-Operational**      | **Fail-Safe**             |
+===================+===========================+===========================+
| **Goal**          | Continue operation        | Reach safe state          |
+-------------------+---------------------------+---------------------------+
| **Safe State**    | Not available/acceptable  | Exists and acceptable     |
+-------------------+---------------------------+---------------------------+
| **Redundancy**    | Required (2+ channels)    | Optional (single channel  |
|                   |                           | with de-energize-to-safe) |
+-------------------+---------------------------+---------------------------+
| **Complexity**    | High (voting, reconfig)   | Low (passive safety)      |
+-------------------+---------------------------+---------------------------+
| **Cost**          | High (multiple channels)  | Low (single channel)      |
+-------------------+---------------------------+---------------------------+
| **Example**       | Aircraft flight control   | Railway signal (RED)      |
+-------------------+---------------------------+---------------------------+

**Redundancy Levels:**

+-------------------+-------------------------+-------------------------+
| **Architecture**  | **Description**         | **Fault Tolerance**     |
+===================+=========================+=========================+
| **Simplex**       | 1 channel               | 0 (no redundancy)       |
+-------------------+-------------------------+-------------------------+
| **Duplex (2oo2)** | 2 channels, both needed | 0 (fail-safe, not       |
|                   |                         | fail-operational)       |
+-------------------+-------------------------+-------------------------+
| **TMR (2oo3)**    | 3 channels, majority    | 1 channel failure       |
|                   | vote                    | tolerated               |
+-------------------+-------------------------+-------------------------+
| **Quad (3oo4)**   | 4 channels, 3 needed    | 1 channel failure       |
|                   |                         | tolerated               |
+-------------------+-------------------------+-------------------------+
| **Dual-Dual**     | 2×(2oo2), cross-monitor | 1 lane failure          |
| **(2oo2D)**       |                         | tolerated               |
+-------------------+-------------------------+-------------------------+

════════════════════════════════════════════════════════════════════

📖 **1. REDUNDANCY ARCHITECTURES**
══════════════════════════════════

**1.1 Triple Modular Redundancy (TMR / 2oo3)**
----------------------------------------------

**Architecture:**

.. code-block:: text

    [Input]───┬───→ Channel A ───┐
              │                  │
              ├───→ Channel B ───┼───→ [VOTER] ───→ [Output]
              │                  │        ↓
              └───→ Channel C ───┘   (Majority
                                      selection)

**Voter Logic (Majority):**

.. code-block:: text

    Output = Majority(A, B, C)
    
    Truth Table:
    ┌───┬───┬───┬────────┐
    │ A │ B │ C │ Output │
    ├───┼───┼───┼────────┤
    │ 0 │ 0 │ 0 │   0    │
    │ 0 │ 0 │ 1 │   0    │ ← C failed (disagrees), A & B agree → 0
    │ 0 │ 1 │ 0 │   0    │
    │ 0 │ 1 │ 1 │   1    │ ← A failed, B & C agree → 1
    │ 1 │ 0 │ 0 │   0    │
    │ 1 │ 0 │ 1 │   1    │
    │ 1 │ 1 │ 0 │   1    │ ← C failed, A & B agree → 1
    │ 1 │ 1 │ 1 │   1    │
    └───┴───┴───┴────────┘
    
    Majority: Output = (A·B) + (B·C) + (A·C)

**Fault Tolerance:**

- **Single failure**: 2 of 3 channels remain → Voter outputs correct value ✅
- **Dual failure**: Only 1 channel remains → Voter outputs incorrect value ❌
- **Result**: Tolerates 1 failure (fail-operational), 2 failures → fail

**Failure Probability (Simplified):**

.. code-block:: text

    Assumptions:
    - Each channel reliability: R = 0.999 (99.9%)
    - Channel failure: F = 0.001 (0.1%)
    - Failures are independent
    
    TMR System Fails if ≥2 channels fail:
    P(fail) = P(2 fail) + P(3 fail)
            = C(3,2) × F² × R¹ + C(3,3) × F³
            = 3 × (0.001)² × 0.999 + 1 × (0.001)³
            = 3 × 10⁻⁶ × 0.999 + 1 × 10⁻⁹
            = 2.997 × 10⁻⁶ + 10⁻⁹
            ≈ 3 × 10⁻⁶
    
    TMR System Reliability:
    R_TMR = 1 - P(fail)
          = 1 - 3 × 10⁻⁶
          = 0.999997 (99.9997%)
    
    Compare to Simplex: 0.999 (99.9%)
    Improvement: 10× better reliability

**1.2 Dual-Dual (2oo2D) Architecture**
--------------------------------------

**Architecture:**

.. code-block:: text

    Lane 1:
    [Input]───→ Channel A1 ───┐
                              ├───→ [Comparator 1] ───┐
    [Input]───→ Channel A2 ───┘                       │
                                                       ├───→ [Cross-Monitor] ───→ [Output Selection]
    Lane 2:                                            │
    [Input]───→ Channel B1 ───┐                       │
                              ├───→ [Comparator 2] ───┘
    [Input]───→ Channel B2 ───┘

**Voting Logic:**

.. code-block:: text

    Lane 1: A1 and A2 must agree → Output_1 = A1 (or A2, identical)
    Lane 2: B1 and B2 must agree → Output_2 = B1 (or B2, identical)
    
    Cross-Monitor compares Output_1 vs Output_2:
    - If agree: Use either (both correct)
    - If disagree: Identify failed lane, use good lane

**Fault Tolerance:**

- **Single channel failure** (e.g., A1 fails):
  - Comparator 1 detects disagreement (A1 ≠ A2)
  - Lane 1 disabled
  - Cross-monitor switches to Lane 2 (B1, B2)
  - System continues ✅

- **Single lane failure** (e.g., entire Lane 1 fails):
  - Cross-monitor detects Lane 1 failure
  - Switch to Lane 2
  - System continues ✅

- **Dual failure in same lane** (A1 and A2 both fail identically):
  - Comparator 1 sees agreement (both wrong)
  - Cross-monitor compares Lane 1 vs Lane 2
  - Detects mismatch, switches to Lane 2 ✅

**Advantage over TMR:**

- Dual-Dual can detect AND correct failures (knows which channel is wrong)
- TMR with simple voting cannot identify failed channel (just outvotes it)

**1.3 Quadruplex (Quad / 3oo4)**
--------------------------------

**Architecture:**

.. code-block:: text

    [Input]───┬───→ Channel A ───┐
              │                  │
              ├───→ Channel B ───┤
              │                  ├───→ [VOTER (3oo4)] ───→ [Output]
              ├───→ Channel C ───│
              │                  │
              └───→ Channel D ───┘

**Voter Logic (3 of 4):**

.. code-block:: text

    Output = 1 if at least 3 channels output 1
    Output = 0 if at least 3 channels output 0
    
    If 2 channels say 1, 2 channels say 0:
    → No majority → System fault (very rare)

**Fault Tolerance:**

- **Single failure**: 3 of 4 channels remain → Majority vote correct ✅
- **Higher reliability** than TMR (more redundancy)

**Use Case:**

- Space systems (long mission duration, no repair)
- Ultra-high reliability (10⁻⁹ to 10⁻¹⁰/hr target)

**1.4 Hybrid Architectures**
----------------------------

**TMR with Standby Spare (Hot Spare):**

.. code-block:: text

    Active:
    [Input]───┬───→ Channel A ───┐
              │                  │
              ├───→ Channel B ───┼───→ [VOTER] ───→ [Output]
              │                  │
              └───→ Channel C ───┘
    
    Standby:
    [Input]───────→ Channel D ───→ (monitored, ready to replace failed channel)
    
    If Channel A fails:
    - Detect failure
    - Reconfigure: Activate Channel D, disable Channel A
    - New TMR: B, C, D

**Advantage:**

- Tolerates multiple failures over time (with reconfiguration)
- Requires failure detection and reconfiguration logic

════════════════════════════════════════════════════════════════════

📖 **2. VOTER DESIGN**
══════════════════════

**2.1 Simple Majority Voter (Digital)**
---------------------------------------

**Boolean Logic:**

.. code-block:: text

    Output = (A AND B) OR (B AND C) OR (A AND C)

**VHDL Implementation:**

.. code-block:: vhdl

    library IEEE;
    use IEEE.STD_LOGIC_1164.ALL;
    
    entity Voter_TMR is
        Port ( A : in  STD_LOGIC;
               B : in  STD_LOGIC;
               C : in  STD_LOGIC;
               Output : out  STD_LOGIC);
    end Voter_TMR;
    
    architecture Behavioral of Voter_TMR is
    begin
        Output <= (A and B) or (B and C) or (A and C);
    end Behavioral;

**Fault in Voter:**

- ⚠️ **Single Point of Failure**: If voter fails, entire system fails
- **Mitigation**: Triplicate voter (3 voters, each voting on outputs)

**2.2 Median Voter (Analog/Continuous)**
----------------------------------------

**Purpose:** For analog signals (sensors, actuators)

**Algorithm:**

.. code-block:: text

    Given 3 values: A, B, C
    Median = Middle value
    
    Example:
    A = 10.5, B = 10.3, C = 15.2 (C is faulty)
    Sorted: [10.3, 10.5, 15.2]
    Median = 10.5 ✅ (correct, C outlier rejected)

**Python Implementation:**

.. code-block:: python

    def median_voter(A, B, C):
        """
        Median voter for TMR analog channels.
        Returns median value (rejects outliers).
        """
        values = sorted([A, B, C])
        return values[1]  # Middle value
    
    # Example
    sensor_A = 10.5  # OK
    sensor_B = 10.3  # OK
    sensor_C = 15.2  # Faulty (outlier)
    
    voted_value = median_voter(sensor_A, sensor_B, sensor_C)
    print(f"Voted output: {voted_value}")  # 10.5 (correct)

**Advantage:**

- Rejects outliers (faulty sensors with large deviation)
- Simple, deterministic

**Limitation:**

- If 2 sensors fail, median is incorrect
- Assumes failures are detectable (large deviation)

**2.3 Weighted Average Voter**
------------------------------

**Purpose:** Incorporate confidence in each channel

**Algorithm:**

.. code-block:: text

    Output = (w_A × A + w_B × B + w_C × C) / (w_A + w_B + w_C)
    
    Where:
    - w_A, w_B, w_C = Weights (0 to 1) based on channel health
    - Healthy channel: w = 1.0
    - Degraded channel: w = 0.5
    - Failed channel: w = 0.0

**Example:**

.. code-block:: python

    def weighted_voter(A, B, C, w_A=1.0, w_B=1.0, w_C=1.0):
        """
        Weighted average voter with health weighting.
        """
        total_weight = w_A + w_B + w_C
        if total_weight == 0:
            raise ValueError("All channels failed!")
        
        output = (w_A * A + w_B * B + w_C * C) / total_weight
        return output
    
    # Example: Channel C degraded (50% weight)
    sensor_A = 10.5  # w_A = 1.0
    sensor_B = 10.3  # w_B = 1.0
    sensor_C = 11.0  # w_C = 0.5 (degraded)
    
    voted = weighted_voter(sensor_A, sensor_B, sensor_C, 1.0, 1.0, 0.5)
    print(f"Weighted output: {voted:.2f}")  # 10.48

**2.4 Voter Reliability**
-------------------------

**Voter is SINGLE POINT OF FAILURE!**

**Mitigation 1: Triplicated Voter**

.. code-block:: text

    [Channels A, B, C]──┬───→ Voter_1 ───┐
                        │                │
                        ├───→ Voter_2 ───┼───→ [Meta-Voter] ───→ [Output]
                        │                │
                        └───→ Voter_3 ───┘

**Mitigation 2: Formal Verification**

- Voter logic is simple (combinatorial)
- Formal verification (model checking) can prove correctness
- Hardware implementation (FPGA) with no software vulnerabilities

**Mitigation 3: Diverse Voter Implementations**

- Voter A: Boolean logic
- Voter B: Lookup table
- Voter C: Software algorithm
- Different implementations → Different failure modes → Less CCF

════════════════════════════════════════════════════════════════════

📖 **3. FAULT DETECTION & RECONFIGURATION**
═══════════════════════════════════════════

**3.1 Fault Detection Methods**
-------------------------------

**Method 1: Comparison (Cross-Check)**

.. code-block:: text

    Channel A ──┬───→ Comparator ───→ Mismatch flag
    Channel B ──┘
    
    If |A - B| > Threshold → Fault detected
    
    Example: Dual-redundant sensors
    - Sensor A: 10.5
    - Sensor B: 10.3
    - Threshold: 0.5
    - |10.5 - 10.3| = 0.2 < 0.5 → OK ✅
    
    If Sensor A fails: 15.2
    - |15.2 - 10.3| = 4.9 > 0.5 → FAULT ❌

**Method 2: Parity/Checksums**

.. code-block:: text

    Transmit: [Data] + [Parity Bit]
    Receive:  [Data] + [Parity Bit] → Check parity
    
    If parity mismatch → Data corruption detected
    
    Example: Memory ECC (Error Correcting Code)
    - Single-bit errors: Detected and corrected
    - Dual-bit errors: Detected (not correctable)

**Method 3: Built-In Test (BIT)**

.. code-block:: text

    Periodic self-test:
    1. Inject known stimulus
    2. Check output against expected
    3. If mismatch → Channel faulty
    
    Example: Sensor self-test
    - Apply known calibration signal
    - Measure output
    - Compare to expected value
    - If deviation > tolerance → Sensor fault

**Method 4: Watchdog Monitoring**

.. code-block:: text

    Each channel sends heartbeat to monitor
    - Expected: Heartbeat every 100ms
    - If heartbeat missing for 300ms → Channel presumed failed

**3.2 Reconfiguration Strategies**
----------------------------------

**Strategy 1: Fail-Silent**

- Failed channel outputs neutral value (e.g., 0)
- Voter ignores failed channel
- Example: TMR with 3 channels, 1 fails → 2 remaining → Continue ✅

**Strategy 2: Hot Standby Replacement**

.. code-block:: text

    Active: A, B, C (TMR)
    Standby: D (hot spare, synchronized)
    
    If C fails:
    1. Detect C failure
    2. Disable C
    3. Activate D
    4. New TMR: A, B, D

**Strategy 3: Graceful Degradation**

- Multiple failures → Reduced functionality (not total failure)
- Example: Autonomous vehicle
  - 3 cameras → Full functionality
  - 2 cameras → Reduced ODD (no nighttime driving)
  - 1 camera → Minimal risk condition (safe stop)

**3.3 Reconfiguration Time**
----------------------------

**Critical Requirement:** Reconfiguration must complete before hazard occurs

**Example: Aircraft Fly-by-Wire**

.. code-block:: text

    Failure Detection Time:     20 ms (comparator detects mismatch)
    Fault Isolation Time:       10 ms (identify Channel B failed)
    Reconfiguration Time:       30 ms (switch to A & C only)
    Total:                      60 ms
    
    Hazard Timeline:
    - Loss of control develops in ~200 ms (pilot notices)
    - Reconfiguration complete in 60 ms → SAFE ✅
    
    Margin: 200 ms - 60 ms = 140 ms (sufficient)

**3.4 Reconfiguration Safety**
------------------------------

**Hazard:** Incorrect reconfiguration (disable good channel, keep bad channel)

**Mitigation:**

1. **Conservative reconfiguration**: If uncertain, disable suspected channel
2. **Cross-validation**: Multiple monitors agree before reconfiguration
3. **Hysteresis**: Require fault to persist for N cycles before reconfiguration
4. **Undo capability**: Revert reconfiguration if wrong

════════════════════════════════════════════════════════════════════

📖 **4. FAIL-OPERATIONAL EXAMPLES**
═══════════════════════════════════

**4.1 Aircraft Fly-by-Wire (Boeing 777)**
-----------------------------------------

**System:** Primary Flight Control System (PFCS)

**Architecture:**

.. code-block:: text

    3 Actuator Control Electronics (ACE) units per control surface:
    
    Aileron (Roll Control):
    
    [Pilot Input]──┬───→ ACE Left  (Channel A) ───┐
                   │                              │
                   ├───→ ACE Center (Channel B) ──┼───→ [Voter] ───→ [Hydraulic Actuator]
                   │                              │
                   └───→ ACE Right  (Channel C) ───┘
    
    TMR Architecture (2oo3)

**Redundancy Levels:**

- **Primary Flight Computers**: 3× (Triple)
- **Actuator Control Electronics (ACE)**: 3× per surface
- **Hydraulic Systems**: 3× independent (Left, Center, Right)
- **Sensors**: 6× Air Data Inertial Reference Units (ADIRU)

**Failure Scenarios:**

+-------------------+-------------------------+---------------------------+
| **Failure**       | **Effect**              | **Result**                |
+===================+=========================+===========================+
| 1 ACE fails       | 2 of 3 remain           | ✅ Full operation         |
|                   | → Majority vote         | (no degradation)          |
+-------------------+-------------------------+---------------------------+
| 2 ACE fail        | Only 1 remains          | ⚠️ Degraded (dispatch     |
|                   | → No majority           | restriction)              |
+-------------------+-------------------------+---------------------------+
| 1 hydraulic       | 2 of 3 remain           | ✅ Full operation         |
| system fails      | → Sufficient power      |                           |
+-------------------+-------------------------+---------------------------+
| All hydraulic     | Backup: Ram Air Turbine | ⚠️ Minimal control        |
| systems fail      | (RAT) deploys           | (emergency only)          |
+-------------------+-------------------------+---------------------------+

**Certification:**

- DAL A (Design Assurance Level A) for catastrophic failure conditions
- Probability target: <10⁻⁹ per flight-hour
- TMR achieves target through redundancy + diversity

**4.2 Autonomous Vehicle (SAE Level 4)**
----------------------------------------

**System:** Automated Driving System (ADS)

**Fail-Operational Requirement:**

- No safe state during operation (vehicle in motion)
- Must achieve Minimal Risk Condition (MRC) if failure:
  - Pull over to side of road
  - Activate hazard lights
  - Come to controlled stop

**Architecture:**

.. code-block:: text

    Perception:
    [Cameras (6×)]──────┐
    [LIDAR (4×)]────────┼───→ [Sensor Fusion]──→ [Environment Model]
    [RADAR (5×)]────────┘
    
    Planning:
    [Environment Model]───→ [Path Planner (redundant)]───→ [Trajectory]
    
    Control:
    [Trajectory]──┬───→ Control Unit A ───┐
                  │                       │
                  └───→ Control Unit B ───┼───→ [Voter]───→ [Actuators]

**Redundancy Strategy:**

- **Sensors**: N+2 (can lose 2 sensors per modality)
- **Compute**: Dual-redundant (2 compute platforms, cross-checked)
- **Actuators**: Dual path (primary + backup steering/braking)
- **Power**: Dual power supplies (main + backup battery)

**Failure Management:**

.. code-block:: text

    Fault Severity Levels:
    
    Level 1 (Minor): Single sensor fault
    → Action: Continue operation, log fault
    
    Level 2 (Moderate): Multiple sensors in one modality
    → Action: Reduce ODD (exit highway, slow down), notify user
    
    Level 3 (Major): Primary compute unit failure
    → Action: Switch to backup, achieve MRC within 10 seconds
    
    Level 4 (Critical): Dual compute failure (no redundancy left)
    → Action: Immediate MRC (emergency braking, pull over)

**4.3 Medical Pacemaker**
-------------------------

**System:** Cardiac pacemaker (life-sustaining)

**Fail-Operational Requirement:**

- Patient's life depends on continuous operation
- Battery failure is gradual (months of warning)

**Redundancy:**

.. code-block:: text

    Sensing:
    [Cardiac Sensor A]──┬───→ [Comparator]───→ [Pace Generator]
    [Cardiac Sensor B]──┘
    
    Pacing:
    [Pace Generator]──┬───→ Lead A (primary)
                      │
                      └───→ Lead B (backup, switched if A fails)
    
    Power:
    [Battery]──→ [Voltage Monitor]───→ Warn if < 2.4V (3 months remaining)

**Failure Management:**

- **Battery depletion**: Elective replacement indicator (ERI)
  - 3 months warning before end-of-service (EOS)
  - Patient notified (beeping, wireless alert)
  - Scheduled replacement surgery

- **Lead fracture**: Detect via impedance measurement
  - High impedance → Open circuit → Switch to backup lead
  - Alert patient/physician

- **Sensing failure**: Cross-check with backup sensor
  - If disagreement → Conservative pacing (safe default rate)

**Safety Level:** ISO 14971 risk class (high), IEC 60601 medical electrical equipment

**4.4 Spacecraft Flight Computer (Mars Rover)**
-----------------------------------------------

**System:** Mars Perseverance Rover flight computer

**Fail-Operational Requirement:**

- No ground support during critical maneuvers (20-minute signal delay)
- Mission duration: 10+ years (no repair possible)

**Redundancy:**

.. code-block:: text

    Computers:
    [Primary Computer A]──┬───→ [Health Monitor]
                          │
    [Backup Computer B]───┘
    
    Watchdog architecture:
    - Primary A sends heartbeat to B
    - B monitors A health
    - If A fails → B takes over (cold standby switchover)

**Fault Tolerance:**

- **Dual computers**: A (primary), B (backup)
- **Radiation-hardened**: Single-Event Upset (SEU) protection
  - Triple-redundant memory with voting
  - Error Detection and Correction (EDAC)

**Reconfiguration:**

- Autonomous fault detection (no ground intervention)
- Safe mode: Minimal functionality (maintain power, comms, thermal)
- Recovery: Boot from backup software image

════════════════════════════════════════════════════════════════════

📖 **5. DESIGN CONSIDERATIONS**
═══════════════════════════════

**5.1 Common Cause Failures (CCF)**
-----------------------------------

**Risk:** All redundant channels fail simultaneously due to common cause

**Common Causes:**

1. **Design defect**: Same bug in all channels (software)
2. **Environmental**: EMI, radiation, temperature
3. **Maintenance**: Incorrect procedure applied to all channels
4. **Supply chain**: Same faulty component in all channels

**Mitigation:**

**1. Diversity:**

- **Hardware diversity**: Different processors (A: Intel, B: ARM)
- **Software diversity**: Different implementations (A: C, B: Ada)
- **Algorithm diversity**: Different approaches (A: Kalman filter, B: Particle filter)
- **Development diversity**: Different teams, different tools

**2. Independence:**

- Physical separation (different racks, different power supplies)
- Data separation (independent sensors, no shared buses)
- Software separation (partitioning, no shared memory)

**3. Beta Factor Model (IEC 61508):**

.. code-block:: text

    β (Beta) = Fraction of failures that are common-cause
    
    Example: β = 0.1 (10% of failures are CCF)
    
    TMR Reliability with CCF:
    R_TMR = R³ + 3R²(1-R) - β × (1-R)
    
    Where:
    - R = Single channel reliability
    - β = Beta factor (CCF contribution)

**5.2 Voting Latency**
----------------------

**Issue:** Voter adds delay to control loop

**Example:**

.. code-block:: text

    Control Loop:
    [Sensor]──→ 5ms ──→[Controller]──→ 10ms ──→[Voter]──→ 2ms ──→[Actuator]──→ 8ms
    
    Total latency: 5 + 10 + 2 + 8 = 25 ms
    
    If control loop requires <20 ms for stability:
    25 ms > 20 ms → Unstable ❌

**Mitigation:**

- **Fast voter**: Hardware implementation (FPGA), not software
- **Pipelined voting**: Parallel processing, overlapped stages
- **Relaxed timing**: Design control loop to tolerate 25ms delay

**5.3 Synchronization**
-----------------------

**Requirement:** Redundant channels must be synchronized

**Clock Synchronization:**

.. code-block:: text

    Channel A: Clock_A (100.00 MHz)
    Channel B: Clock_B (100.01 MHz)  ← Slight drift
    Channel C: Clock_C ( 99.99 MHz)
    
    After 1 second:
    - A: 100,000,000 cycles
    - B: 100,010,000 cycles (+100 ppm drift)
    - C:  99,990,000 cycles (-100 ppm drift)
    
    Voter sees outputs at different times → Mismatch ❌

**Solution:**

- **Master clock**: One channel provides reference clock
- **Clock distribution**: Distribute to all channels
- **Phase-Locked Loop (PLL)**: Synchronize local clocks

**Data Synchronization:**

- **Frame synchronization**: All channels process same data frame
- **Timestamp**: Attach timestamp to sensor data
- **Buffering**: Wait for all channels before voting

**5.4 Diagnostic Coverage**
---------------------------

**Definition:** Fraction of failures detected by diagnostics

**Diagnostic Coverage (DC):**

.. code-block:: text

    DC = (Detected dangerous failures) / (Total dangerous failures)
    
    Example:
    - Total dangerous failures: 100
    - Detected by diagnostics: 90
    - DC = 90/100 = 90%

**SIL Requirements (IEC 61508):**

+-------------+-------------------------+
| **SIL**     | **DC Required**         |
+=============+=========================+
| **SIL 4**   | DC ≥ 99% (High)         |
+-------------+-------------------------+
| **SIL 3**   | DC ≥ 90% (Medium)       |
+-------------+-------------------------+
| **SIL 2**   | DC ≥ 60% (Low)          |
+-------------+-------------------------+
| **SIL 1**   | DC < 60%                |
+-------------+-------------------------+

**Improving DC:**

- **Built-in test**: Periodic self-test (inject faults, check detection)
- **Cross-monitoring**: Channels check each other
- **Signature analysis**: Check intermediate results for consistency

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between TMR (2oo3) and Dual-Dual (2oo2D)?

**A1:**

**TMR (2oo3):**
- 3 channels with majority voter
- Tolerates 1 failure (2 of 3 remain)
- Cannot identify which channel failed (just outvotes it)
- Simpler architecture

**Dual-Dual (2oo2D):**
- 2 lanes, each with 2 channels (4 channels total)
- Each lane compares its 2 channels (detect disagreement)
- Cross-monitor compares lanes (identify failed lane)
- Tolerates 1 lane failure (switch to good lane)
- Can identify AND correct failures (knows which channel is wrong)

────────────────────────────────────────────────────────────────────

**Q2:** Why is the voter a single point of failure, and how is it mitigated?

**A2:**

**Problem:**
- Voter fails → Entire system fails (even if all channels healthy)
- Voter is not redundant in basic TMR

**Mitigations:**

1. **Triplicated voter**: 3 voters with meta-voter (voter voting on voters)
2. **Formal verification**: Prove voter correctness (simple logic, verifiable)
3. **Hardware voter**: FPGA implementation (no software bugs)
4. **Diverse voters**: Different implementations (reduce CCF)
5. **Voter self-test**: Built-in test (periodic verification)

────────────────────────────────────────────────────────────────────

**Q3:** When is fail-operational required vs fail-safe?

**A3:**

**Fail-Operational Required:**

✅ No safe state exists (aircraft in flight, spacecraft)  
✅ Mission abort unacceptable (life support, autonomous vehicle)  
✅ High availability critical (telecom, power grid, medical implant)

**Fail-Safe Acceptable:**

✅ Safe state exists (railway signal → RED)  
✅ Shutdown tolerable (industrial machine → E-stop)  
✅ Lower cost preferred (not safety-critical or low availability OK)

**Trade-off:** Fail-operational is more expensive and complex, but necessary when continuous operation is essential.

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Architecture Design:**
- [ ] Identify if fail-operational is required (no safe state, mission-critical)
- [ ] Select redundancy level (TMR, Quad, Dual-Dual) based on safety target
- [ ] Design voter (majority, median, weighted average)
- [ ] Address voter single point of failure (triplicate, formal verification)
- [ ] Plan synchronization (clock, data, frame alignment)

**Fault Management:**
- [ ] Define fault detection methods (comparison, parity, BIT, watchdog)
- [ ] Specify reconfiguration strategy (fail-silent, hot standby, degradation)
- [ ] Calculate reconfiguration time (must be < hazard development time)
- [ ] Validate reconfiguration safety (conservative, cross-validated)

**Common Cause Failures:**
- [ ] Identify CCF sources (design defects, environment, maintenance)
- [ ] Apply diversity (hardware, software, algorithm, development team)
- [ ] Ensure independence (physical, data, software separation)
- [ ] Calculate Beta factor (quantify CCF contribution)

**Verification:**
- [ ] Calculate system reliability (TMR formula with CCF)
- [ ] Measure diagnostic coverage (DC ≥ 90% for SIL 3)
- [ ] Fault injection testing (verify detection and reconfiguration)
- [ ] Safety case (fail-operational argument pattern)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Fail-operational = Continue operation** → No safe state, redundancy required

2️⃣ **TMR (2oo3)** → 3 channels, majority vote, tolerates 1 failure

3️⃣ **Dual-Dual (2oo2D)** → 4 channels, 2 lanes, cross-monitor, identifies failures

4️⃣ **Voter is SPOF** → Mitigate with triplication, formal verification, HW implementation

5️⃣ **Common cause failures** → Diversity (HW, SW, algorithm, team) + Independence

6️⃣ **Synchronization critical** → Clock sync, data frame alignment, buffering

7️⃣ **High DC required** → SIL 4 needs ≥99% diagnostic coverage (BIT, cross-monitor)

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **FAIL-OPERATIONAL ARCHITECTURE CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Redundancy architectures (TMR, Dual-Dual, Quad, hybrid), voter design  
(majority, median, weighted), fault detection & reconfiguration, fail-operational  
examples (aircraft fly-by-wire Boeing 777, autonomous vehicle, pacemaker, Mars Rover),  
design considerations (CCF, voting latency, synchronization, diagnostic coverage)

════════════════════════════════════════════════════════════════════
