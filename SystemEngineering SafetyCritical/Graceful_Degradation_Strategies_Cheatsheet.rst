📋 **Graceful Degradation Strategies**
═══════════════════════════════════════════════════════════════════

**Full Name:** Graceful Degradation (Fault-Tolerant Service Reduction)  
**Type:** Architectural pattern for managed failure response  
**Principle:** Maintain partial functionality when full capability lost  
**Standards:** ISO 26262, SAE J3016, DO-178C, IEC 62304

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — GRACEFUL DEGRADATION IN 60 SECONDS**
─────────────────────────────────────────────────

**What is Graceful Degradation?**

::

    Graceful Degradation = System reduces functionality in controlled manner
                           when failures occur (rather than catastrophic failure)
    
    Key principle: PARTIAL SERVICE > NO SERVICE > DANGEROUS FAILURE
    
    Example: Autonomous vehicle loses cameras
             → Degrade from Level 4 (full automation) to Level 2 (driver assist)
             → Notify driver, request takeover
             → Maintain safe minimum functionality until handover

**Degradation Levels:**

.. code-block:: text

    LEVEL 0: FULL FUNCTIONALITY (All systems operational)
                    ↓
    LEVEL 1: REDUCED FUNCTIONALITY (Some features disabled)
                    ↓
    LEVEL 2: MINIMAL FUNCTIONALITY (Essential services only)
                    ↓
    LEVEL 3: SAFE MODE (Maintain safety, minimal operation)
                    ↓
    LEVEL 4: CONTROLLED SHUTDOWN (Orderly transition to safe state)

**vs Related Concepts:**

+-------------------+---------------------------+---------------------------+
| **Concept**       | **Description**           | **Example**               |
+===================+===========================+===========================+
| **Fail-Safe**     | → Safe state immediately  | Railway signal → RED      |
+-------------------+---------------------------+---------------------------+
| **Fail-          | → Full operation despite  | Aircraft fly-by-wire      |
| Operational**     | failure (redundancy)      | (TMR continues)           |
+-------------------+---------------------------+---------------------------+
| **Graceful**      | → Reduced functionality   | ADAS: Full auto →         |
| **Degradation**   | → Gradual reduction       | Driver assist →           |
|                   | → Notify user             | Manual (with warning)     |
+-------------------+---------------------------+---------------------------+
| **Limp-Home**     | → Minimal function to     | Engine control: Max       |
| **Mode**          | reach safety              | 3000 RPM, 30 mph          |
+-------------------+---------------------------+---------------------------+

**When to Use Graceful Degradation:**

✅ **Partial functionality useful** (better than total failure)  
✅ **Time needed for transition** (handover to human, reach safe location)  
✅ **Multiple failure modes** (different degradation levels)  
✅ **User notification critical** (driver must know system limits)

════════════════════════════════════════════════════════════════════

📖 **1. DEGRADATION LEVEL DESIGN**
══════════════════════════════════

**1.1 Defining Degradation Levels**
-----------------------------------

**Principle:** Map system capabilities to available resources

**Example: Autonomous Vehicle Sensor Degradation**

+--------+----------------------+---------------------+----------------------+
| Level  | **Available**        | **Capability**      | **ODD**              |
| **#**  | **Sensors**          |                     | **(Operational       |
|        |                      |                     | Design Domain)**     |
+========+======================+=====================+======================+
| **0**  | 6 cameras            | SAE Level 4         | Urban streets,       |
|        | 4 LIDAR              | Full automation     | <45 mph, day/night,  |
| (FULL) | 5 RADAR              |                     | rain/dry             |
+--------+----------------------+---------------------+----------------------+
| **1**  | 4 cameras (2 lost)   | SAE Level 4         | Urban streets,       |
|        | 4 LIDAR              | Reduced ODD         | <45 mph, DAYLIGHT    |
| (RED)  | 5 RADAR              |                     | ONLY, dry (no rain)  |
+--------+----------------------+---------------------+----------------------+
| **2**  | 4 cameras            | SAE Level 3         | Highways only,       |
|        | 2 LIDAR (2 lost)     | Conditional auto    | <65 mph, daylight,   |
| (MIN)  | 5 RADAR              | (user ready)        | dry, 10-sec takeover |
+--------+----------------------+---------------------+----------------------+
| **3**  | 2 cameras (4 lost)   | SAE Level 2         | Highways only,       |
|        | 4 LIDAR              | Driver assist       | <65 mph, DRIVER      |
| (SAFE) | 5 RADAR              | (LKAS + ACC)        | MUST MONITOR         |
+--------+----------------------+---------------------+----------------------+
| **4**  | 0-1 cameras (≥5 lost)| Minimal Risk        | Immediate safe stop: |
|        | OR all LIDAR lost    | Condition (MRC)     | Pull over, hazards   |
| (MRC)  |                      | STOP VEHICLE        | on, notify occupants |
+--------+----------------------+---------------------+----------------------+

**1.2 Degradation Triggers**
----------------------------

**Trigger Types:**

1. **Sensor Failure**: Camera offline, LIDAR malfunction
2. **Compute Failure**: CPU overheating, GPU crash
3. **Environmental**: Heavy rain (cameras blinded), fog (LIDAR limited)
4. **Geofence Exit**: Vehicle leaves mapped area
5. **Communication Loss**: V2X link down, cloud connection lost

**Example Trigger Logic:**

.. code-block:: python

    def determine_degradation_level(system_state):
        """
        Determine appropriate degradation level based on system health.
        
        Returns: 0 (Full) to 4 (MRC)
        """
        cameras_ok = system_state['cameras_functional']
        lidar_ok = system_state['lidar_functional']
        radar_ok = system_state['radar_functional']
        weather = system_state['weather_condition']
        location = system_state['location_type']
        
        # Level 0: Full functionality
        if (cameras_ok >= 6 and lidar_ok >= 4 and radar_ok >= 5 
            and weather in ['clear', 'light_rain'] 
            and location == 'urban'):
            return 0  # Level 4 automation, full ODD
        
        # Level 1: Reduced ODD (daylight only)
        if (cameras_ok >= 4 and lidar_ok >= 4 and radar_ok >= 5 
            and weather == 'clear' 
            and system_state['is_daylight']):
            return 1  # Level 4 automation, reduced ODD
        
        # Level 2: Conditional automation (highways only)
        if (cameras_ok >= 4 and lidar_ok >= 2 and radar_ok >= 5 
            and location == 'highway'):
            return 2  # Level 3 automation, conditional
        
        # Level 3: Driver assist only
        if (cameras_ok >= 2 and lidar_ok >= 4 and radar_ok >= 5):
            return 3  # Level 2 automation, LKAS + ACC only
        
        # Level 4: Minimal Risk Condition (MRC)
        return 4  # Stop vehicle safely

**1.3 Transition Management**
-----------------------------

**Principle:** Smooth, predictable transitions between levels

**State Machine:**

.. code-block:: text

    ┌─────────────┐
    │  Level 0    │ Camera lost
    │  FULL       │───────────────────┐
    └─────────────┘                   │
           ↕ Camera restored           ↓
    ┌─────────────┐              ┌─────────────┐
    │  Level 1    │ LIDAR lost   │  Level 2    │
    │  REDUCED    │──────────────→  MINIMAL    │
    └─────────────┘              └─────────────┘
           ↑                            │
           │                            │ Sensor failure
           │ LIDAR restored             ↓
           │                      ┌─────────────┐
           └──────────────────────│  Level 3    │
                                  │  SAFE MODE  │
                                  └─────────────┘
                                        │
                                        │ Critical failure
                                        ↓
                                  ┌─────────────┐
                                  │  Level 4    │
                                  │  MRC (STOP) │
                                  └─────────────┘

**Transition Rules:**

1. **Downgrade**: Immediate (< 1 second) when failure detected
2. **Upgrade**: Delayed (10+ seconds) to verify stability
3. **Hysteresis**: Prevent rapid oscillation between levels
4. **User Notification**: Alert user at each transition

**Example Hysteresis:**

.. code-block:: text

    DOWNGRADE (Level 0 → Level 1):
    - Trigger: Camera lost
    - Action: Immediate (within 100 ms)
    - Reason: Safety-critical, must respond fast
    
    UPGRADE (Level 1 → Level 0):
    - Trigger: Camera restored
    - Action: Wait 10 seconds, verify camera stable
    - Reason: Prevent false recovery (intermittent fault)
    
    Hysteresis prevents "flapping":
    Camera flickers on/off → System stays at Level 1 (degraded)
                            → Upgrades only after 10 sec continuous OK

════════════════════════════════════════════════════════════════════

📖 **2. USER NOTIFICATION & HANDOVER**
══════════════════════════════════════

**2.1 Notification Methods**
----------------------------

**Multi-Modal Alerts (Critical for Safety):**

1. **Visual**: Dashboard display, LED indicators
2. **Auditory**: Chimes, voice messages
3. **Haptic**: Steering wheel vibration, seat vibration
4. **Olfactory**: (Rare) Scent alert for emergency (experimental)

**Alert Escalation:**

.. code-block:: text

    LEVEL 1 (Informational):
    - Visual: Yellow icon on display
    - Message: "Night driving disabled"
    - Action: None (system continues)
    
    LEVEL 2 (Warning):
    - Visual: Orange icon + text message
    - Auditory: Single chime
    - Message: "Automation reduced. Driver standby required."
    - Action: Driver must monitor (10-second takeover time)
    
    LEVEL 3 (Urgent):
    - Visual: Red flashing icon + full-screen message
    - Auditory: Repeated chimes (every 2 seconds)
    - Haptic: Steering wheel vibration
    - Message: "DRIVER TAKE OVER IMMEDIATELY"
    - Action: Driver must take control NOW
    
    LEVEL 4 (Critical):
    - Visual: Red flashing + hazard lights
    - Auditory: Continuous alarm
    - Haptic: Seat vibration + steering wheel pulse
    - Message: "EMERGENCY STOP - PULLING OVER"
    - Action: Vehicle executing MRC (automatic safe stop)

**2.2 Takeover Time Budget**
----------------------------

**SAE J3016 Requirements:**

+-------------+-------------------------+-------------------------+
| **SAE**     | **Takeover Time**       | **Description**         |
| **Level**   |                         |                         |
+=============+=========================+=========================+
| **Level 5** | N/A (no driver)         | Full automation, no     |
|             |                         | takeover                |
+-------------+-------------------------+-------------------------+
| **Level 4** | ≥60 seconds             | Conditional auto, user  |
|             | (or MRC if no takeover) | may be sleeping         |
+-------------+-------------------------+-------------------------+
| **Level 3** | ≥10 seconds             | User must be ready,     |
|             |                         | not engaged in tasks    |
+-------------+-------------------------+-------------------------+
| **Level 2** | Immediate (hands on)    | Driver must monitor at  |
|             |                         | all times               |
+-------------+-------------------------+-------------------------+

**Example: Level 3 → Level 2 Degradation**

.. code-block:: text

    t=0s:     Sensor failure detected
              → Degrade to Level 2 (driver assist only)
              → Display: "TAKE OVER IN 10 SECONDS"
              → Chime: Auditory alert
    
    t=2s:     Steering wheel vibration (haptic alert)
              → Display countdown: "8 seconds"
    
    t=5s:     Repeat chime
              → Display: "5 seconds - HANDS ON WHEEL"
    
    t=8s:     Driver hands detected on wheel ✅
              → Transition complete
              → Display: "Driver assist mode - MONITOR ROAD"
    
    t=10s:    (Alternative) Driver NOT responsive ❌
              → Escalate to Level 4 (MRC)
              → Execute automatic safe stop

**2.3 Driver Monitoring**
-------------------------

**Purpose:** Verify driver is alert and capable of takeover

**Monitoring Methods:**

1. **Hands on Wheel**: Torque sensor (detect steering input)
2. **Eye Tracking**: Camera + IR (monitor gaze direction)
3. **Heart Rate**: Seat sensor (detect consciousness)
4. **Facial Recognition**: Detect drowsiness, distraction

**Example: Eye Tracking Escalation**

.. code-block:: text

    Driver Attention Level (0-100%):
    
    100%-80%: Eyes on road → GREEN (OK)
              No alerts
    
    80%-60%:  Eyes off road for >2 sec → YELLOW (Warning)
              Visual: "Keep eyes on road"
              Auditory: Single chime
    
    60%-40%:  Eyes off road for >5 sec → ORANGE (Urgent)
              Visual: Flashing "LOOK AT ROAD"
              Auditory: Repeated chimes
              Haptic: Steering vibration
    
    <40%:     Eyes off road for >10 sec → RED (Critical)
              Driver unresponsive
              → Assume driver incapacitated
              → Execute MRC (safe stop)

════════════════════════════════════════════════════════════════════

📖 **3. LIMP-HOME MODE (AUTOMOTIVE)**
════════════════════════════════════

**3.1 Limp-Home Definition**
----------------------------

**Limp-Home Mode:**

    Minimal engine/vehicle functionality to reach safe location
    (home, repair shop, roadside) after critical failure

**Typical Limp-Home Limits:**

+-------------------+-------------------------+-------------------------+
| **Parameter**     | **Normal**              | **Limp-Home**           |
+===================+=========================+=========================+
| **Engine Speed**  | 6500 RPM max            | 3000 RPM max            |
+-------------------+-------------------------+-------------------------+
| **Vehicle Speed** | 120 mph max             | 30 mph max              |
+-------------------+-------------------------+-------------------------+
| **Gear**          | All gears (1-8)         | 3rd gear only (locked)  |
+-------------------+-------------------------+-------------------------+
| **Boost Pressure**| 20 psi (turbo)          | 0 psi (no turbo)        |
+-------------------+-------------------------+-------------------------+
| **Power Output**  | 300 HP                  | 50 HP (reduced)         |
+-------------------+-------------------------+-------------------------+

**3.2 Limp-Home Triggers**
--------------------------

**Common Failure Modes:**

1. **Transmission Fault**: Solenoid failure, TCU error
   - Limp-Home: Lock in 3rd gear (compromise between torque + speed)

2. **Turbo Failure**: Wastegate stuck, overboost
   - Limp-Home: Disable turbo (naturally aspirated mode)

3. **Sensor Failure**: MAF sensor, throttle position sensor
   - Limp-Home: Use default tables (conservative fueling)

4. **Emissions Fault**: Catalytic converter failure, O2 sensor
   - Limp-Home: Rich fuel mixture (protect engine, sacrifice emissions)

**Example: Transmission Limp-Home**

.. code-block:: text

    NORMAL OPERATION:
    [TCU] → [Solenoids] → [Hydraulic Valves] → [Clutch Packs] → [8-Speed Auto]
    
    FAILURE: Solenoid #4 stuck open
    - TCU cannot control gear 5, 6, 7, 8
    - Risk: Unpredictable shifts, transmission damage
    
    LIMP-HOME ACTION:
    1. Detect failure (solenoid current out of range)
    2. Set DTC (Diagnostic Trouble Code): P0730 "Incorrect Gear Ratio"
    3. Illuminate "Check Engine" light (MIL)
    4. Lock transmission in 3rd gear (hydraulic default)
       - 3rd gear provides reasonable torque + speed
       - Max speed: ~30 mph (vs 120 mph normal)
    5. Display message: "TRANSMISSION FAULT - LIMP HOME MODE - VISIT DEALER"
    
    Result: Driver can reach safe location (home, dealer) at reduced speed ✅

**3.3 Limp-Home Safety**
------------------------

**Safety Considerations:**

1. **Predictable Behavior**: Limp-home must be stable (no oscillation)
2. **Adequate Performance**: Sufficient power to merge, climb hills
3. **Clear Notification**: Driver must know limitations
4. **No Further Damage**: Limp-home must not worsen failure

**Example: Overheating Limp-Home**

.. code-block:: text

    Engine Coolant Temp > 115°C (239°F):
    
    Stage 1 (Warning): 115-120°C
    - Display: "Engine hot - reduce speed"
    - Action: None (driver discretion)
    
    Stage 2 (Derate): 120-125°C
    - Display: "Engine overheating - power reduced"
    - Action: Reduce power to 50% (less heat generation)
    
    Stage 3 (Limp-Home): 125-130°C
    - Display: "ENGINE CRITICAL - STOP SOON"
    - Action: Reduce power to 25%, max 30 mph
    
    Stage 4 (Emergency Shutdown): >130°C
    - Display: "ENGINE SHUTDOWN - PULL OVER"
    - Action: Disable engine (prevent catastrophic damage)

════════════════════════════════════════════════════════════════════

📖 **4. MINIMAL RISK CONDITION (MRC)**
══════════════════════════════════════

**4.1 MRC Definition**
----------------------

**Minimal Risk Condition (MRC):**

    Stable, stationary state with minimized risk to occupants and others
    when autonomous system cannot continue operation

**MRC Requirements (SAE J3016):**

✅ Vehicle brought to standstill  
✅ Hazard lights activated  
✅ Occupants notified  
✅ Emergency services contacted (if needed)  
✅ Vehicle secured (parking brake engaged)

**4.2 MRC Execution**
---------------------

**MRC Sequence:**

.. code-block:: text

    1. DETECT failure (critical sensor loss, compute failure)
       → System determines MRC is necessary
    
    2. NOTIFY occupants
       → Visual: "EMERGENCY STOP"
       → Auditory: Continuous alarm
       → Haptic: Seat vibration
    
    3. IDENTIFY safe location
       → Evaluate: Shoulder, parking lane, emergency lane
       → Avoid: Travel lanes (high risk)
    
    4. ACTIVATE hazards
       → Hazard lights ON (all 4 turn signals flashing)
       → High beam flash (increase visibility)
    
    5. MANEUVER to safe location
       → Gradual deceleration (0.3g max, comfortable)
       → Signal lane change (if moving to shoulder)
       → Monitor traffic (avoid collision)
    
    6. STOP vehicle
       → Deceleration to 0 mph
       → Engage parking brake
       → Shift to PARK
    
    7. SECURE & NOTIFY
       → Unlock doors (allow egress)
       → Display: "VEHICLE STOPPED - EXIT SAFELY"
       → Call emergency services (eCall, if severe failure)
       → Transmit telemetry to fleet operator

**MRC Time Budget:**

.. code-block:: text

    Example: Highway at 65 mph
    
    Distance to shoulder: 200 ft (safe lane change)
    Deceleration: 0.3g = 10 ft/s² (comfortable)
    
    Time to stop from 65 mph (95 ft/s):
    t = v / a = 95 ft/s / 10 ft/s² = 9.5 seconds
    
    Distance traveled:
    d = v² / (2a) = (95)² / (2 × 10) = 450 ft
    
    Total: 200 ft (lane change) + 450 ft (stop) = 650 ft (0.12 miles)
          Time: ~12 seconds
    
    Result: MRC achievable within 15 seconds ✅

**4.3 MRC Fallback Levels**
---------------------------

**Fallback Hierarchy (if preferred MRC location unavailable):**

1. **Preferred**: Emergency shoulder (wide, paved, low traffic)
2. **Acceptable**: Right-most travel lane (slow lane)
3. **Last Resort**: Current lane (if no other option)

**Example Scenario: No Shoulder Available**

.. code-block:: text

    Situation: Dense urban street, no shoulder, 2-lane road
    
    MRC Decision Tree:
    
    Q1: Can reach parking spot within 30 seconds?
    → YES: Navigate to parking spot, execute MRC ✅
    → NO: Continue to Q2
    
    Q2: Can reach wide area (plaza, gas station)?
    → YES: Navigate to wide area, execute MRC ✅
    → NO: Continue to Q3
    
    Q3: Can stop in right lane with hazards ON?
    → YES: Gradual stop in right lane, hazards ON ⚠️ (acceptable)
    → NO: Continue to Q4
    
    Q4: Must stop in current lane (no alternative)
    → Action: Immediate stop, hazards ON, emergency flashers ❌ (last resort)
              Alert emergency services (vehicle blocking traffic)

════════════════════════════════════════════════════════════════════

📖 **5. IMPLEMENTATION EXAMPLES**
═════════════════════════════════

**5.1 Autonomous Vehicle State Manager (Python)**
-------------------------------------------------

.. code-block:: python

    from enum import Enum
    import time
    
    class DegradationLevel(Enum):
        FULL = 0          # Full automation
        REDUCED = 1       # Reduced ODD
        MINIMAL = 2       # Conditional auto
        SAFE_MODE = 3     # Driver assist
        MRC = 4           # Minimal Risk Condition
    
    class AVStateManager:
        def __init__(self):
            self.current_level = DegradationLevel.FULL
            self.downgrade_time = None
            self.upgrade_delay = 10.0  # seconds (hysteresis)
        
        def evaluate_system_health(self):
            """
            Evaluate sensors and determine appropriate degradation level.
            Returns: (new_level, reason)
            """
            # Simulate sensor health check
            cameras_ok = self.get_camera_count()
            lidar_ok = self.get_lidar_count()
            radar_ok = self.get_radar_count()
            
            if cameras_ok >= 6 and lidar_ok >= 4 and radar_ok >= 5:
                return (DegradationLevel.FULL, "All sensors nominal")
            elif cameras_ok >= 4 and lidar_ok >= 4 and radar_ok >= 5:
                return (DegradationLevel.REDUCED, "Camera degraded")
            elif cameras_ok >= 4 and lidar_ok >= 2 and radar_ok >= 5:
                return (DegradationLevel.MINIMAL, "LIDAR degraded")
            elif cameras_ok >= 2 and lidar_ok >= 2 and radar_ok >= 3:
                return (DegradationLevel.SAFE_MODE, "Multiple sensor loss")
            else:
                return (DegradationLevel.MRC, "Critical sensor failure")
        
        def update(self):
            """
            State machine update (called every 100ms).
            Manages degradation level transitions with hysteresis.
            """
            new_level, reason = self.evaluate_system_health()
            
            # DOWNGRADE (immediate, safety-critical)
            if new_level.value > self.current_level.value:
                self.current_level = new_level
                self.downgrade_time = time.time()
                self.notify_user(new_level, reason, urgent=True)
                print(f"⚠️ DOWNGRADE to {new_level.name}: {reason}")
            
            # UPGRADE (delayed, with hysteresis)
            elif new_level.value < self.current_level.value:
                if self.downgrade_time is None:
                    self.downgrade_time = time.time()
                
                # Check if system has been stable for upgrade_delay
                stable_time = time.time() - self.downgrade_time
                if stable_time >= self.upgrade_delay:
                    self.current_level = new_level
                    self.downgrade_time = None
                    self.notify_user(new_level, reason, urgent=False)
                    print(f"✅ UPGRADE to {new_level.name}: {reason}")
                else:
                    remaining = self.upgrade_delay - stable_time
                    print(f"Upgrade pending... {remaining:.1f}s remaining")
        
        def notify_user(self, level, reason, urgent):
            """
            Multi-modal user notification.
            """
            if level == DegradationLevel.FULL:
                print("📘 INFO: Full automation restored")
            elif level == DegradationLevel.REDUCED:
                print("📙 WARNING: Reduced automation - daylight only")
            elif level == DegradationLevel.MINIMAL:
                print("📕 CAUTION: Conditional automation - standby required")
            elif level == DegradationLevel.SAFE_MODE:
                print("🔴 URGENT: Driver assist only - TAKE OVER")
                self.play_chime()
                self.vibrate_steering()
            elif level == DegradationLevel.MRC:
                print("🚨 CRITICAL: Executing Minimal Risk Condition - STOP")
                self.play_alarm()
                self.vibrate_seat()
                self.execute_mrc()
        
        def execute_mrc(self):
            """
            Execute Minimal Risk Condition (safe stop).
            """
            print("1. Activating hazard lights...")
            print("2. Identifying safe shoulder...")
            print("3. Signaling lane change...")
            print("4. Decelerating (0.3g)...")
            print("5. Stopping vehicle...")
            print("6. Engaging parking brake...")
            print("7. Unlocking doors...")
            print("8. Notifying emergency services...")
            print("✅ MRC complete - Vehicle secured")
        
        def get_camera_count(self):
            # Simulate sensor health (replace with actual sensor query)
            return 6  # Example: All 6 cameras OK
        
        def get_lidar_count(self):
            return 4  # Example: All 4 LIDAR OK
        
        def get_radar_count(self):
            return 5  # Example: All 5 RADAR OK
        
        def play_chime(self):
            print("🔔 Chime: Beep")
        
        def vibrate_steering(self):
            print("📳 Steering wheel vibration")
        
        def play_alarm(self):
            print("🚨 Alarm: Continuous beeping")
        
        def vibrate_seat(self):
            print("📳 Seat vibration")
    
    # Example usage
    if __name__ == "__main__":
        av = AVStateManager()
        
        # Simulate degradation scenario
        print("=== Autonomous Vehicle State Manager ===\n")
        
        for i in range(20):
            print(f"\n--- Cycle {i+1} ---")
            av.update()
            time.sleep(0.5)  # Simulate 100ms update rate (5× speed for demo)

**5.2 ADAS Feature Degradation Table**
--------------------------------------

+-------------------+-------------------------+-------------------------+-------------------------+
| **Failure Mode**  | **Affected Features**   | **Degraded Features**   | **User Notification**   |
+===================+=========================+=========================+=========================+
| **Camera lost**   | Lane Keeping (LKAS),    | LKAS disabled,          | "Lane keeping           |
| **(1 of 6)**      | Traffic Sign Recog      | TSR OFF                 | unavailable"            |
+-------------------+-------------------------+-------------------------+-------------------------+
| **LIDAR lost**    | Adaptive Cruise (ACC),  | ACC max speed 45 mph    | "Cruise control         |
| **(1 of 4)**      | Emergency Braking (AEB) | (vs 80 mph), AEB        | limited"                |
|                   |                         | sensitivity reduced     |                         |
+-------------------+-------------------------+-------------------------+-------------------------+
| **RADAR lost**    | Blind Spot Monitoring   | BSM + RCTA OFF          | "Blind spot system      |
| **(1 of 5)**      | (BSM), Rear Cross       |                         | fault - check mirrors"  |
|                   | Traffic (RCTA)          |                         |                         |
+-------------------+-------------------------+-------------------------+-------------------------+
| **GPS lost**      | Navigation, Traffic     | Manual routing,         | "GPS unavailable"       |
|                   | Info, Speed Limit       | no traffic, speed       |                         |
|                   | Display                 | limit unknown           |                         |
+-------------------+-------------------------+-------------------------+-------------------------+

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between graceful degradation and limp-home mode?

**A1:**

**Graceful Degradation:**
- Gradual reduction of functionality through multiple levels
- Example: Autonomous vehicle Level 4 → 3 → 2 → MRC
- User notified at each level, given time to respond
- Multiple degradation states

**Limp-Home Mode:**
- Minimal functionality to reach safe location (repair shop, home)
- Example: Transmission locked in 3rd gear, max 30 mph
- Specific automotive term (engine/transmission faults)
- Usually binary: Normal OR Limp-Home (not gradual)

────────────────────────────────────────────────────────────────────

**Q2:** Why is hysteresis important in degradation level transitions?

**A2:**

**Problem without hysteresis:**
- Sensor flickers on/off → System rapidly oscillates between levels
- Example: Camera intermittent → Level 0 → 1 → 0 → 1 (every second)
- Confusing to user, unstable behavior

**Solution with hysteresis:**
- **Downgrade**: Immediate (safety-critical)
- **Upgrade**: Delayed (e.g., 10 seconds stable before upgrading)
- Prevents "flapping" between levels
- Example: Camera restored → Wait 10 sec to verify stable → Then upgrade to Level 0

────────────────────────────────────────────────────────────────────

**Q3:** What are the key requirements for Minimal Risk Condition (MRC)?

**A3:**

**MRC Requirements (SAE J3016):**

1. **Standstill**: Vehicle brought to complete stop (0 mph)
2. **Hazard Lights**: Activated to warn other traffic
3. **Notification**: Occupants informed of emergency stop
4. **Location**: Safe location if possible (shoulder, not travel lane)
5. **Secured**: Parking brake engaged, shift to PARK
6. **Egress**: Doors unlocked (occupants can exit safely)
7. **Emergency Services**: Contact if needed (eCall, severe failure)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Design Phase:**
- [ ] Define degradation levels (0=Full to 4=MRC)
- [ ] Map capabilities to available resources (sensor count → ODD)
- [ ] Identify degradation triggers (sensor loss, environment, geofence)
- [ ] Design state machine (transitions, hysteresis)
- [ ] Specify user notifications (visual, auditory, haptic)

**Implementation:**
- [ ] Implement sensor health monitoring
- [ ] Develop degradation level determination logic
- [ ] Code state machine with hysteresis (downgrade immediate, upgrade delayed)
- [ ] Integrate multi-modal alerts (display, chimes, vibration)
- [ ] Implement MRC execution sequence

**Verification:**
- [ ] Test all degradation transitions (0→1→2→3→4)
- [ ] Verify user notification effectiveness (driver response time)
- [ ] Test hysteresis (prevent flapping)
- [ ] Validate MRC execution (time budget, safe location selection)
- [ ] Fault injection testing (sensor failures, compute failures)

**Documentation:**
- [ ] Document degradation levels and triggers
- [ ] User manual (explain degradation behavior, alerts)
- [ ] Safety case (degradation pattern argument)
- [ ] Traceability (requirements → degradation levels)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Graceful degradation = Controlled reduction** → Partial service > none

2️⃣ **Multiple levels** → Full → Reduced → Minimal → Safe → MRC (stop)

3️⃣ **Hysteresis critical** → Downgrade immediate, upgrade delayed (prevent flapping)

4️⃣ **User notification essential** → Visual + auditory + haptic alerts

5️⃣ **MRC execution** → Safe stop sequence (hazards, shoulder, notify, secure)

6️⃣ **Limp-home mode** → Minimal function to reach safety (automotive-specific)

7️⃣ **State machine** → Predictable transitions, clear triggers, stable behavior

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **GRACEFUL DEGRADATION STRATEGIES CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Degradation level design (0-4 levels), user notification & handover  
(multi-modal alerts, takeover time budget, driver monitoring), limp-home mode  
(automotive transmission/engine faults), Minimal Risk Condition (MRC execution,  
fallback hierarchy), Python implementation (AVStateManager state machine)

════════════════════════════════════════════════════════════════════
