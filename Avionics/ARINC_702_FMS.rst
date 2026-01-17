===================================================================
ARINC 702 / 702A — Advanced Flight Management Computer System
===================================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 702/702A** defines the **Advanced Flight Management Computer System (AFMCS)** interface, also known as the **Flight Management System (FMS)**.

**Key Characteristics:**
- **Purpose:** Automated flight planning, navigation, performance optimization
- **Core Functions:** Flight plan management, navigation (RNAV/RNP), autopilot coupling, performance calculations
- **Interfaces:** ARINC 429 (primary I/O), ARINC 615A (database loading), CDU (Control Display Unit)
- **Databases:** ARINC 424 navigation data, aircraft performance, airport/runway data
- **Navigation:** GPS, IRS, VOR/DME, RNAV (Area Navigation), RNP (Required Navigation Performance)
- **4D Trajectory:** Latitude, longitude, altitude, **time** (required time of arrival - RTA)

**Typical FMS Capabilities:**
- **Flight Planning:** Route optimization, waypoint sequencing, alternate airports
- **Navigation:** Auto-tuning of navaids, GPS/IRS blending, position accuracy monitoring
- **Autopilot Coupling:** LNAV (lateral), VNAV (vertical), approach modes
- **Performance:** Fuel prediction, time-to-waypoint, optimal altitude/speed
- **RNP/RNAV:** Precision navigation (RNP 0.1 = ±0.1 nm 95% accuracy)

**ARINC 702 vs 702A:**

.. code-block:: text

   Feature              ARINC 702          ARINC 702A
   ──────────────────── ─────────────────  ─────────────────────
   Publication          1996               2004
   RNP Support          Basic (RNP 1.0)    Advanced (RNP 0.1, AR)
   4D Trajectory        Limited            Full RTA support
   Datalink Integration Minimal            CPDLC, ADS-C/B
   Database Format      ARINC 424-15       ARINC 424-18+
   Autopilot Modes      Basic LNAV/VNAV    Advanced (RF legs, FAS)
   Performance Calc     Standard           Enhanced (cost index)

================================================================================
1. Overview & Background
================================================================================

**1.1 Flight Management System Evolution**
--------------------------------------------

**Pre-FMS Era (1950s-1970s):**
- Manual navigation: Pilots calculated headings, fuel, time
- VOR/DME navigation: Point-to-point between ground stations
- Inertial Navigation Systems (INS): Self-contained, but drift over time
- Autopilot: Basic heading/altitude hold, no route following

**First Generation FMS (1980s):**
- **Boeing 767 (1982):** First commercial aircraft with integrated FMS
- **Database:** ARINC 424 navigation data (waypoints, airways, procedures)
- **INS Integration:** Automatic position updates from VOR/DME
- **Autopilot Coupling:** LNAV (lateral navigation) follows flight plan
- **Performance:** Basic fuel/time predictions

**Modern FMS (ARINC 702/702A, 1990s-2000s):**
- **GPS Integration:** Primary navigation source (±5 m accuracy)
- **RNAV/RNP:** Area Navigation, Required Navigation Performance
- **VNAV:** Vertical navigation (altitude/speed profiles)
- **4D Trajectory:** Time-constrained arrivals (Required Time of Arrival)
- **Datalink:** CPDLC (Controller-Pilot Data Link Communications)

**1.2 ARINC 702A Key Features**
--------------------------------

**Advanced Navigation:**
- **RNP AR (Authorization Required):** RNP 0.1-0.3 for curved approaches
- **RF Legs (Radius-to-Fix):** Curved flight path segments
- **FAS (Final Approach Segment):** GBAS/SBAS precision approaches
- **Multi-Sensor Fusion:** GPS, IRS, VOR/DME, DME/DME, SBAS

**4D Flight Path Management:**
- **RTA (Required Time of Arrival):** ATC time constraints at waypoints
- **Speed/Altitude Optimization:** Cost Index-based performance
- **Wind Model:** Real-time wind updates from aircraft sensors

**Datalink Integration:**
- **CPDLC:** Text-based ATC clearances, route amendments
- **ADS-C (Automatic Dependent Surveillance - Contract):** Periodic position reports
- **ADS-B (Broadcast):** 1 Hz position broadcast to ATC/other aircraft

================================================================================
2. FMS Architecture
================================================================================

**2.1 System Components**
--------------------------

.. code-block:: text

   ┌──────────────────────────────────────────────────────────────┐
   │                    FMS Architecture                           │
   ├──────────────────────────────────────────────────────────────┤
   │                                                               │
   │  ┌────────────┐   ┌────────────┐   ┌────────────┐           │
   │  │    CDU     │   │    CDU     │   │    MCDU    │           │
   │  │ (Pilot/Co) │   │ (Pilot/Co) │   │  (A320)    │           │
   │  └─────┬──────┘   └─────┬──────┘   └─────┬──────┘           │
   │        │                 │                 │                 │
   │        └─────────────────┴─────────────────┘                 │
   │                          │                                   │
   │                          ▼                                   │
   │              ┌────────────────────────┐                      │
   │              │   FMC (Flight Mgmt     │                      │
   │              │   Computer) - ARINC 702│                      │
   │              │                        │                      │
   │              │  • Flight Plan Engine  │                      │
   │              │  • Navigation Solver   │                      │
   │              │  • Performance Model   │                      │
   │              │  • Database Manager    │                      │
   │              └────────┬───────────────┘                      │
   │                       │                                      │
   │        ┌──────────────┼──────────────┐                       │
   │        ▼              ▼              ▼                       │
   │  ┌─────────┐   ┌─────────┐   ┌─────────┐                    │
   │  │ ARINC   │   │  GPS    │   │  IRS    │                    │
   │  │ 429 I/O │   │ (GNSS)  │   │ (Gyro)  │                    │
   │  └────┬────┘   └────┬────┘   └────┬────┘                    │
   │       │             │             │                          │
   │       ▼             ▼             ▼                          │
   │  Autopilot       Position      Attitude                     │
   │  VOR/DME         Updates        Data                        │
   └──────────────────────────────────────────────────────────────┘

**Key Components:**

1. **FMC (Flight Management Computer):**
   - CPU: Typically PowerPC or ARM (DO-178C DAL A certified)
   - Memory: 128-512 MB RAM, 4-16 GB SSD (navigation database)
   - I/O: 8-16 ARINC 429 RX, 4-8 ARINC 429 TX, 2× AFDX (modern)

2. **CDU/MCDU (Control Display Unit):**
   - Display: 6×10 line alphanumeric (older), 10×20 (modern)
   - Input: QWERTY keyboard, line select keys (LSK), function keys
   - Interface: ARINC 429 or ARINC 661 (modern glass cockpits)

3. **Navigation Databases:**
   - **ARINC 424:** Waypoints, airways, SIDs, STARs, approaches (updated every 28 days - AIRAC cycle)
   - **Performance DB:** Aircraft-specific (fuel flow, climb/descent rates)
   - **Airport/Runway:** Runway length, ILS frequencies, taxiway data

**2.2 Data Flow**
------------------

.. code-block:: text

   Sensors → FMC → Flight Plan → Autopilot/Display
   
   1. Sensor Inputs (ARINC 429 RX):
      - GPS: Position (lat/lon), velocity, time
      - IRS: Position, heading, attitude, acceleration
      - VOR/DME: Bearing, distance to stations
      - Air Data: Altitude, airspeed, temperature
   
   2. FMC Processing:
      - Kalman filter: Blend GPS/IRS/VOR for optimal position
      - Flight plan sequencing: Current leg, next waypoint, ETA
      - Performance calculations: Fuel remaining, top of descent
   
   3. Outputs (ARINC 429 TX):
      - Autopilot: Steering commands (LNAV/VNAV)
      - Displays: PFD (heading/altitude bugs), ND (map, waypoints)
      - ACARS: Position reports (ADS-C)

================================================================================
3. Flight Plan Management
================================================================================

**3.1 Flight Plan Structure**
-------------------------------

**Typical Flight Plan Segments:**

.. code-block:: text

   Departure → SID → Enroute → STAR → Approach → Missed Approach
   
   Example: KSFO (San Francisco) to KLAX (Los Angeles)
   
   1. Departure:
      - KSFO Runway 28R
      - SID: OFFSHORE6 (Standard Instrument Departure)
      - Waypoints: SEPDY, FAITH, NTELL
   
   2. Enroute:
      - Airway: J501 (Jet Route)
      - Waypoints: CATLI, GMN (Gila Bend VOR), BZA (Blythe VOR)
   
   3. Arrival:
      - STAR: SEAVU3 (Standard Terminal Arrival)
      - Waypoints: SEAVU, SADDE, ELMOO
   
   4. Approach:
      - ILS 24L (Instrument Landing System)
      - Final Approach Fix: LIMMA
      - Decision Height: 200 ft AGL

**Flight Plan Data Structure:**

.. code-block:: c

   typedef struct {
       char ident[8];           // Waypoint identifier (e.g., "CATLI")
       double latitude;          // Degrees, WGS-84
       double longitude;         // Degrees, WGS-84
       int32_t altitude_ft;      // Constraint altitude (or 0 if none)
       uint16_t speed_kts;       // Constraint speed (or 0)
       uint8_t leg_type;         // TF, RF, CF, etc. (ARINC 424)
       uint8_t flyover;          // 0=flyby, 1=flyover
       uint16_t course_deg;      // Magnetic course to waypoint
       float distance_nm;        // Distance from previous waypoint
   } FMS_Waypoint;
   
   typedef struct {
       FMS_Waypoint waypoints[200];  // Max 200 waypoints per plan
       uint8_t active_leg;           // Current leg index
       uint16_t total_distance_nm;   // Total flight plan distance
       uint32_t total_time_sec;      // Estimated total time
       uint32_t fuel_required_lbs;   // Fuel required for plan
   } FMS_FlightPlan;

**3.2 Leg Types (ARINC 424 Path Terminators)**
------------------------------------------------

.. code-block:: text

   Code  Type                    Description
   ────  ─────────────────────── ──────────────────────────────────
   TF    Track to Fix            Straight line to waypoint
   RF    Radius to Fix           Curved path (constant radius turn)
   CF    Course to Fix           Fly specific course to waypoint
   DF    Direct to Fix           Direct from present position
   IF    Initial Fix             Start of approach/procedure
   AF    Arc to Fix              DME arc
   CA    Course to Altitude      Climb/descend on course to altitude
   FA    Fix to Altitude         From fix until reaching altitude
   FM    From Fix to Manual      Fly heading from fix (radar vectors)
   VM    Heading to Manual       Fly heading until ATC vectors

**Example RF Leg (Curved Approach):**

.. code-block:: text

   RNP AR Approach (Innsbruck, Austria - LOWI):
   
   ┌─────────────────────────────────────────┐
   │  Curved approach between mountains      │
   │                                         │
   │        ╭───────╮                        │
   │       ╱         ╲                       │
   │      │   RF Leg  │  Radius: 3 nm        │
   │       ╲    ⤵     ╱   Turn: 90°          │
   │        ╰────────╯                       │
   │            │                            │
   │            ▼                            │
   │        Runway 26                        │
   └─────────────────────────────────────────┘
   
   - RF legs allow curved flight paths (no need for multiple waypoints)
   - Required for terrain avoidance in mountainous areas
   - RNP 0.1-0.3 accuracy required

================================================================================
4. Navigation & Position Determination
================================================================================

**4.1 Multi-Sensor Navigation**
---------------------------------

**Sensor Hierarchy (Modern FMS):**

.. code-block:: text

   Priority  Sensor    Accuracy   Update Rate  Notes
   ────────  ────────  ─────────  ───────────  ──────────────────────
   1         GPS       ±5 m       1 Hz         Primary (if available)
   2         SBAS      ±1 m       1 Hz         GPS + corrections
   3         DME/DME   ±0.1 nm    Varies       Requires 2+ DME stations
   4         VOR/DME   ±0.5 nm    Varies       Single station
   5         IRS       ±2 nm/hr   50 Hz        Drift over time

**Kalman Filter (Sensor Fusion):**

.. code-block:: python

   import numpy as np
   
   class FMS_Navigation:
       def __init__(self):
           # State vector: [lat, lon, velocity_x, velocity_y]
           self.state = np.zeros(4)
           
           # Covariance matrix (uncertainty)
           self.P = np.eye(4) * 1e-6
           
           # Process noise (aircraft motion uncertainty)
           self.Q = np.diag([1e-8, 1e-8, 1e-4, 1e-4])
       
       def predict(self, dt):
           """Predict next state (dead reckoning from IRS)"""
           # State transition matrix (constant velocity model)
           F = np.array([
               [1, 0, dt, 0],
               [0, 1, 0, dt],
               [0, 0, 1, 0],
               [0, 0, 0, 1]
           ])
           
           self.state = F @ self.state
           self.P = F @ self.P @ F.T + self.Q
       
       def update_gps(self, lat_gps, lon_gps, accuracy):
           """Update state with GPS measurement"""
           # Measurement matrix (GPS measures position only)
           H = np.array([
               [1, 0, 0, 0],
               [0, 1, 0, 0]
           ])
           
           # Measurement noise (GPS accuracy)
           R = np.eye(2) * accuracy**2
           
           # Innovation (difference between prediction and measurement)
           z = np.array([lat_gps, lon_gps])
           y = z - (H @ self.state)
           
           # Kalman gain
           S = H @ self.P @ H.T + R
           K = self.P @ H.T @ np.linalg.inv(S)
           
           # Update state and covariance
           self.state = self.state + K @ y
           self.P = (np.eye(4) - K @ H) @ self.P
       
       def get_position(self):
           """Get current best estimate of position"""
           return self.state[0], self.state[1]  # lat, lon
   
   # Example usage
   fms_nav = FMS_Navigation()
   fms_nav.state = np.array([37.6213, -122.3790, 0.001, 0.001])  # SFO
   
   # Predict for 1 second
   fms_nav.predict(dt=1.0)
   
   # Update with GPS measurement
   fms_nav.update_gps(lat_gps=37.6214, lon_gps=-122.3791, accuracy=5.0)
   
   lat, lon = fms_nav.get_position()
   print(f"Position: {lat:.4f}°N, {lon:.4f}°W")

**4.2 RNP (Required Navigation Performance)**
-----------------------------------------------

**RNP Levels:**

.. code-block:: text

   RNP Value  95% Accuracy  Applications
   ─────────  ────────────  ──────────────────────────────────
   RNP 10     ±10 nm        Oceanic (MNPS - Minimum Nav Perf)
   RNP 4      ±4 nm         Oceanic/remote areas
   RNP 2      ±2 nm         Continental enroute
   RNP 1      ±1 nm         Terminal area
   RNP 0.3    ±0.3 nm       Approach (RNAV approach)
   RNP 0.1    ±0.1 nm       RNP AR (special authorization)
   
   **RNP AR (Authorization Required):**
   - RNP 0.1-0.3 for curved approaches
   - Requires aircraft certification, crew training
   - Enables access to challenging airports (LOWI Innsbruck, KASE Aspen)

**RNP Monitoring:**

.. code-block:: c

   // FMS continuously monitors navigation accuracy
   typedef struct {
       float anp;        // Actual Navigation Performance (estimated error)
       float rnp_req;    // Required Navigation Performance (from procedure)
       bool rnp_valid;   // ANP ≤ RNP required?
   } RNP_Status;
   
   void check_rnp(RNP_Status *status, float gps_accuracy, float irs_drift) {
       // Calculate ANP (worst-case from all sensors)
       status->anp = fmax(gps_accuracy, irs_drift);
       
       // Check if RNP requirement met
       status->rnp_valid = (status->anp <= status->rnp_req);
       
       if (!status->rnp_valid) {
           // Alert crew: "RNP UNABLE"
           // Autopilot may disengage if approach active
           trigger_warning("RNP UNABLE");
       }
   }

================================================================================
5. VNAV (Vertical Navigation)
================================================================================

**5.1 Vertical Profile**
-------------------------

**Climb/Descent Profile:**

.. code-block:: text

   Altitude
   (ft)
   
   35,000  ─────────────────────────── Cruise
                                     │
   30,000                            │ TOD (Top of Descent)
                                     ▼ 
   25,000                          ╱
                                  ╱
   20,000                        ╱  3° descent path
                               ╱
   15,000                     ╱
                            ╱
   10,000                 ╱
                        ╱
    5,000             ╱
                    ╱
        0  ────────╯──────────────────  Runway
   
           ←──────────────────────────→
                 Distance (nm)

**VNAV Calculations:**

.. code-block:: python

   def calculate_top_of_descent(current_alt_ft, target_alt_ft, 
                                 descent_rate_fpm, ground_speed_kts):
       """
       Calculate distance to Top of Descent (TOD).
       
       Args:
           current_alt_ft: Current altitude (feet)
           target_alt_ft: Target altitude at waypoint (feet)
           descent_rate_fpm: Descent rate (feet per minute)
           ground_speed_kts: Ground speed (knots)
       
       Returns:
           Distance to TOD (nautical miles)
       """
       # Altitude to lose
       alt_diff = current_alt_ft - target_alt_ft
       
       # Time to descend
       time_min = alt_diff / descent_rate_fpm
       
       # Distance to TOD
       distance_nm = (ground_speed_kts / 60.0) * time_min
       
       return distance_nm
   
   # Example: Descent from FL350 to 10,000 ft at 2000 fpm, GS 450 kts
   tod_dist = calculate_top_of_descent(
       current_alt_ft=35000,
       target_alt_ft=10000,
       descent_rate_fpm=2000,
       ground_speed_kts=450
   )
   print(f"Begin descent in {tod_dist:.1f} nm")
   # Output: Begin descent in 93.8 nm

**5.2 Speed/Altitude Constraints**
------------------------------------

**Constraint Types:**

.. code-block:: text

   Type         Notation     Example
   ───────────  ───────────  ────────────────────────────
   At           "10000"      Cross at exactly 10,000 ft
   At or Above  "10000A"     Cross at or above 10,000 ft
   At or Below  "10000B"     Cross at or below 10,000 ft
   Between      "10000-12000" Between 10,000-12,000 ft
   
   Speed Constraints:
   "250K"       Cross at 250 knots
   "250KB"      Cross at or below 250 knots

**Example STAR (Standard Terminal Arrival):**

.. code-block:: text

   SEAVU3 STAR (KLAX):
   
   Waypoint   Altitude Constraint   Speed Constraint
   ────────── ───────────────────── ─────────────────
   SEAVU      -                     -
   SADDE      11000B (at or below)  250KB
   ELMOO      9000                  -
   DARTS      6000                  -
   
   FMS ensures aircraft meets all constraints

================================================================================
6. Autopilot Coupling
================================================================================

**6.1 LNAV (Lateral Navigation)**
-----------------------------------

**Cross-Track Error Correction:**

.. code-block:: python

   def calculate_lnav_steering(aircraft_pos, current_leg, next_waypoint):
       """
       Calculate steering command for LNAV (lateral navigation).
       
       Returns: Desired track (magnetic heading)
       """
       # Calculate desired track (from current leg start to next waypoint)
       desired_track = calculate_bearing(current_leg.start, next_waypoint)
       
       # Calculate cross-track error (perpendicular distance from desired path)
       xte_nm = calculate_cross_track_error(aircraft_pos, current_leg)
       
       # Proportional steering (1° per 0.1 nm XTE, max ±20°)
       xte_correction = np.clip(xte_nm * 10.0, -20, 20)
       
       # Final steering command
       commanded_track = desired_track + xte_correction
       
       return commanded_track
   
   # Example
   aircraft_pos = (37.62, -122.38)  # Current position
   next_wpt = (37.65, -122.35)       # Next waypoint
   
   track = calculate_lnav_steering(aircraft_pos, current_leg, next_wpt)
   print(f"Autopilot commanded track: {track:.1f}°")

**6.2 VNAV (Vertical Navigation)**
------------------------------------

**Altitude/Speed Control:**

.. code-block:: c

   typedef enum {
       VNAV_CLIMB,      // Climbing to altitude
       VNAV_CRUISE,     // Maintaining cruise altitude
       VNAV_DESCENT,    // Descending on profile
       VNAV_APPROACH    // Final approach descent
   } VNAV_Mode;
   
   void vnav_autopilot(VNAV_Mode mode, float target_alt, 
                       float current_alt, float *pitch_cmd) {
       float alt_error = target_alt - current_alt;
       
       switch (mode) {
           case VNAV_CLIMB:
               // Pitch to maintain climb rate (e.g., 1500 fpm)
               *pitch_cmd = 7.0;  // degrees nose-up
               break;
           
           case VNAV_DESCENT:
               // Pitch for descent rate (e.g., -1000 fpm)
               if (alt_error < -500) {
                   *pitch_cmd = -2.5;  // degrees nose-down
               } else {
                   *pitch_cmd = alt_error / 200.0;  // soften near target
               }
               break;
           
           case VNAV_CRUISE:
               // Maintain altitude (±50 ft tolerance)
               *pitch_cmd = alt_error / 100.0;  // proportional control
               break;
       }
   }

================================================================================
7. 4D Trajectory & RTA (Required Time of Arrival)
================================================================================

**7.1 Time-Constrained Navigation**
-------------------------------------

**RTA Concept:**

.. code-block:: text

   ATC assigns Required Time of Arrival (RTA) at specific waypoint:
   
   "Descend to cross SADDE at 1845Z"
   
   FMS calculates:
   1. Current time: 1830Z
   2. Distance to SADDE: 120 nm
   3. Ground speed required: 120 nm / 15 min = 480 kts
   4. Adjusts speed to meet RTA (within aircraft limits)

**RTA Algorithm:**

.. code-block:: python

   def calculate_rta_speed(distance_nm, time_available_sec, 
                           min_speed_kts=210, max_speed_kts=350):
       """
       Calculate speed required to meet RTA.
       
       Returns: Required speed (knots) or None if impossible
       """
       # Convert time to hours
       time_hr = time_available_sec / 3600.0
       
       # Required speed
       required_speed = distance_nm / time_hr
       
       # Check if achievable
       if required_speed < min_speed_kts:
           # Too slow - path stretch needed (add distance)
           return min_speed_kts
       elif required_speed > max_speed_kts:
           # Too fast - cannot meet RTA
           return None
       else:
           return required_speed
   
   # Example: 120 nm to waypoint, 15 minutes available
   speed = calculate_rta_speed(distance_nm=120, 
                               time_available_sec=15*60)
   if speed:
       print(f"Adjust speed to {speed:.0f} kts to meet RTA")
   else:
       print("RTA NOT ACHIEVABLE")

**7.2 Path Stretching**
------------------------

**Techniques to Delay Arrival:**

.. code-block:: text

   1. Speed Reduction:
      - Slow to minimum clean speed (e.g., 210 kts)
      - Limited by stall speed, passenger comfort
   
   2. Path Extension:
      - Fly direct to waypoint, then hold (racetrack pattern)
      - FMS calculates hold time to meet RTA
   
   3. Step Descent:
      - Delay descent (stay at higher altitude longer)
      - Increases distance flown (headwind component)
   
   Holding Pattern Example:
   
          ┌───────────────┐
          │               │
          ▼               │  1 minute legs
      Waypoint ───────────┘
      (RTA target)
   
   FMS calculates: "Hold for 2 minutes to meet RTA"

================================================================================
8. Performance Optimization
================================================================================

**8.1 Cost Index**
-------------------

**Definition:**
Cost Index (CI) = Time Cost / Fuel Cost (in cents per minute / cents per kg)

.. code-block:: text

   CI Value  Strategy             Speed            Fuel Burn
   ────────  ───────────────────  ───────────────  ──────────
   0         Maximum Range        Slow (LRC-10%)   Minimum
   50        Balanced             LRC (Long Range  Moderate
                                   Cruise)
   100       Maximum Speed        Fast (MMO-5%)    High
   999       Maximum Speed        Maximum          Maximum
   
   Typical Airline CI: 30-80 (depending on fuel prices, schedule)

**Optimal Altitude/Speed:**

.. code-block:: python

   def calculate_optimal_speed(cost_index, altitude_ft, weight_lbs):
       """
       Calculate optimal speed for given cost index.
       
       Simplified model (actual FMS uses detailed performance tables)
       """
       # Long Range Cruise (LRC) - baseline
       lrc_mach = 0.78
       
       # Adjust for cost index (higher CI = faster)
       ci_factor = cost_index / 100.0
       optimal_mach = lrc_mach + (0.05 * ci_factor)
       
       # Limit to max cruise Mach (e.g., 0.85)
       optimal_mach = min(optimal_mach, 0.85)
       
       # Convert Mach to TAS (True Airspeed)
       temp_c = -56.5  # ISA temp at cruise altitude
       speed_of_sound = 661.5  # kts at -56.5°C
       tas_kts = optimal_mach * speed_of_sound
       
       return tas_kts
   
   # Example: CI=50, FL350
   speed = calculate_optimal_speed(cost_index=50, altitude_ft=35000, 
                                   weight_lbs=150000)
   print(f"Optimal cruise speed: {speed:.0f} kts")

**8.2 Fuel Prediction**
------------------------

**Fuel Calculation:**

.. code-block:: c

   typedef struct {
       float fuel_flow_lbs_hr;  // Current fuel flow
       float fuel_remaining;     // Fuel on board (lbs)
       float distance_to_dest;   // Distance to destination (nm)
       float ground_speed;       // Ground speed (kts)
   } FuelState;
   
   float predict_fuel_at_destination(FuelState *state) {
       // Time to destination
       float time_to_dest_hr = state->distance_to_dest / state->ground_speed;
       
       // Fuel burned
       float fuel_burned = state->fuel_flow_lbs_hr * time_to_dest_hr;
       
       // Fuel remaining at destination
       float fuel_at_dest = state->fuel_remaining - fuel_burned;
       
       return fuel_at_dest;
   }
   
   // Example
   FuelState fuel_state = {
       .fuel_flow_lbs_hr = 6000,
       .fuel_remaining = 20000,
       .distance_to_dest = 500,
       .ground_speed = 450
   };
   
   float fuel_dest = predict_fuel_at_destination(&fuel_state);
   printf("Predicted fuel at destination: %.0f lbs\n", fuel_dest);
   // Output: 13,333 lbs (500 nm / 450 kts = 1.11 hr × 6000 lbs/hr)

================================================================================
9. Database Management (ARINC 424)
================================================================================

**9.1 AIRAC Cycle**
--------------------

**28-Day Update Cycle:**

.. code-block:: text

   AIRAC (Aeronautical Information Regulation And Control):
   
   - New navigation database every 28 days
   - Effective dates: Fixed calendar (e.g., Jan 25, Feb 22, Mar 21...)
   - Distributed via ARINC 615A (Ethernet data loading)
   
   Database Providers:
   - Jeppesen (70% market share)
   - Lufthansa Systems
   - NavBlue (Airbus)

**Database Loading:**

.. code-block:: python

   def load_nav_database(database_file):
       """
       Load ARINC 424 navigation database into FMS.
       
       Process:
       1. Validate database signature (ARINC 827 security)
       2. Check effective dates (must be current AIRAC cycle)
       3. Load waypoints, airways, procedures into memory
       4. Build spatial index for fast lookup
       """
       import hashlib
       
       # 1. Validate signature
       with open(database_file, 'rb') as f:
           data = f.read()
       
       signature = hashlib.sha256(data).hexdigest()
       if signature != expected_signature:
           raise ValueError("Database signature mismatch - LOAD REJECTED")
       
       # 2. Check effective dates
       effective_date = parse_effective_date(data)
       if not is_current_airac(effective_date):
           raise ValueError("Database out of date")
       
       # 3. Load data (simplified)
       waypoints = parse_waypoints(data)
       airways = parse_airways(data)
       procedures = parse_procedures(data)
       
       print(f"Loaded {len(waypoints)} waypoints, {len(airways)} airways")
       return waypoints, airways, procedures

================================================================================
10. Exam Preparation — 5 Questions
================================================================================

**Question 1: Flight Plan Leg Types (12 points)**

An RNAV approach has the following legs:
1. CATLI (IF) to BASER (TF leg, 10 nm)
2. BASER to FINAL (RF leg, 90° turn, 3 nm radius)
3. FINAL to runway (CF leg, course 240°)

a) What does RF leg stand for? (2 pts)
b) Calculate the arc length of the RF leg. (4 pts)
c) Why are RF legs used instead of multiple TF legs? (3 pts)
d) What RNP level typically required for RF legs? (3 pts)

**Answer:**

a) **RF = Radius to Fix**
   - Constant-radius curved flight path

b) **Arc Length Calculation:**

.. code-block:: text

   Arc length = Radius × Angle (in radians)
   
   Radius = 3 nm
   Angle = 90° = π/2 radians
   
   Arc length = 3 × (π/2) = 4.71 nm

c) **Advantages of RF Legs:**
   - **Single leg vs multiple:** 90° turn requires ~10 TF waypoints for smoothness
   - **Precise path definition:** Exact radius ensures terrain clearance
   - **Reduced pilot workload:** Autopilot follows smooth curve, no abrupt turns
   - **Mountainous terrain:** Critical for curved approaches (LOWI, KASE)

d) **RNP Requirement:**
   - **RNP 0.3** (minimum for RF legs)
   - **RNP 0.1-0.2** for RNP AR approaches with tight RF turns
   - RNP AR (Authorization Required) certification needed

---

**Question 2: VNAV Top of Descent (10 points)**

Aircraft at FL350 (35,000 ft), descending to cross waypoint SADDE at 10,000 ft.
- Descent rate: 2,500 fpm
- Ground speed: 480 kts
- Wind: 50 kts tailwind

a) Calculate time to descend. (3 pts)
b) Calculate distance to Top of Descent (TOD). (4 pts)
c) If SADDE is 100 nm ahead, what action should FMS take? (3 pts)

**Answer:**

a) **Time to Descend:**

.. code-block:: text

   Altitude change = 35,000 - 10,000 = 25,000 ft
   Descent rate = 2,500 fpm
   
   Time = 25,000 / 2,500 = 10 minutes

b) **Distance to TOD:**

.. code-block:: text

   Ground speed = 480 kts
   Time = 10 minutes = 10/60 hours
   
   Distance = 480 × (10/60) = 80 nm

c) **FMS Action (SADDE is 100 nm ahead):**
   - **TOD at 80 nm, SADDE at 100 nm → TOD is 20 nm BEFORE SADDE**
   - **Problem:** Will arrive at SADDE ABOVE 10,000 ft (still descending)
   - **FMS Actions:**
     1. **Alert crew:** "UNABLE ALTITUDE CONSTRAINT"
     2. **Options:**
        - Increase descent rate (if safe: 3,000-3,500 fpm)
        - Request early descent from ATC
        - Level off early, then descend steeper closer to SADDE
   - **Calculation:** Need 100 nm descent:
     - Required descent rate = 25,000 ft / (100 nm / 480 kts × 60) = 2,000 fpm ✓
     - Actually ACHIEVABLE at 2,000 fpm (less than current 2,500 fpm)
   - **Correct Answer:** FMS will adjust descent to start at 100 nm (earlier TOD)

---

**Question 3: RNP Monitoring (10 points)**

FMS is flying RNP 0.3 approach. Sensor accuracies:
- GPS: 5 m (95%)
- IRS: 0.5 nm

a) Calculate Actual Navigation Performance (ANP). (4 pts)
b) Is RNP requirement met? (2 pts)
c) What happens if GPS fails? (4 pts)

**Answer:**

a) **ANP Calculation:**

.. code-block:: text

   GPS accuracy: 5 m = 5 / 1852 nm = 0.0027 nm
   IRS accuracy: 0.5 nm
   
   ANP = max(GPS, IRS) = 0.5 nm
   
   (FMS uses worst-case sensor for ANP)

b) **RNP Check:**

.. code-block:: text

   RNP required: 0.3 nm
   ANP: 0.5 nm
   
   0.5 nm > 0.3 nm → RNP NOT MET ✗
   
   FMS displays: "RNP UNABLE 0.3"

c) **GPS Failure:**
   - **ANP degrades to IRS-only:** 0.5 nm (may worsen over time, 2 nm/hr drift)
   - **Cannot meet RNP 0.3:** Approach not authorized
   - **Crew Action:**
     - Go-around or missed approach
     - Request radar vectors for ILS approach (not RNP-dependent)
   - **Autopilot:** May disengage LNAV/VNAV (reverts to heading/altitude hold)
   - **Alternative:** If DME/DME available (2+ DME stations), may provide 0.2-0.5 nm accuracy

---

**Question 4: Cost Index & Speed (8 points)**

Airline operates with CI=50. Fuel price: $3/kg, Time cost: $150/minute.

a) What does CI=50 represent? (3 pts)
b) If optimal speed is Mach 0.80, what is the trade-off? (3 pts)
c) When would airline increase CI? (2 pts)

**Answer:**

a) **CI=50 Interpretation:**

.. code-block:: text

   CI = Time Cost / Fuel Cost = 150 / 3 = 50
   
   "For every 1 kg of fuel saved, airline willing to spend 50 cents"
   
   Balanced strategy between speed and fuel efficiency

b) **Speed Trade-off (M0.80):**
   - **Faster than LRC (M0.78):** +2% speed
   - **Fuel penalty:** +5-10% fuel burn
   - **Time savings:** 120 nm at M0.78 = 154 min, M0.80 = 150 min → 4 min saved
   - **Economic:** 4 min × $150 = $600 saved vs. ~50 kg fuel × $3 = $150 extra cost
   - **Net benefit:** $450 (time savings > fuel cost)

c) **When to Increase CI:**
   1. **Low fuel prices:** Fuel cheap, speed more valuable
   2. **Flight delays:** Need to make up time
   3. **Tight connections:** Passengers transferring at hub
   4. **High-value cargo:** Perishable goods, express freight

---

**Question 5: 4D Trajectory RTA (10 points)**

ATC assigns RTA: "Cross ELMOO at 1930Z"
- Current time: 1915Z (15 min available)
- Distance to ELMOO: 90 nm
- Aircraft limits: 210-350 kts

a) Calculate required speed. (3 pts)
b) Is RTA achievable? (2 pts)
c) If RTA is 1925Z (10 min), how can FMS meet it? (5 pts)

**Answer:**

a) **Required Speed:**

.. code-block:: text

   Distance: 90 nm
   Time: 15 min = 0.25 hr
   
   Speed = 90 / 0.25 = 360 kts

b) **Achievability:**

.. code-block:: text

   Required: 360 kts
   Max speed: 350 kts
   
   360 > 350 → RTA NOT ACHIEVABLE ✗

c) **RTA 1925Z (10 min):**

.. code-block:: text

   Required speed = 90 nm / (10/60 hr) = 540 kts
   
   Far exceeds aircraft capability!
   
   FMS Strategies:
   
   1. **Path Stretching:**
      - Cannot fly faster, so ADD DISTANCE
      - Hold pattern at ELMOO (racetrack)
      - Calculate: At 210 kts (min speed), 90 nm = 25.7 min
      - Arrive 15.7 min early, hold for 15.7 min
   
   2. **Step Climb/Descent:**
      - If currently low, climb to catch headwind (slow down)
      - If high, descend early (tailwind increases GS)
   
   3. **Direct Routing:**
      - If on airway, request direct ELMOO (shortcut)
      - Reduces distance, easier to meet RTA
   
   Practical: Alert crew "RTA NOT ACHIEVABLE, REQUEST DELAY"

================================================================================
11. Completion Checklist
================================================================================

□ Understand FMS architecture (FMC, CDU, databases, sensors)
□ Know flight plan structure (SID, enroute, STAR, approach)
□ Decode ARINC 424 leg types (TF, RF, CF, etc.)
□ Calculate VNAV top of descent (time, distance)
□ Understand multi-sensor navigation (GPS, IRS, VOR/DME)
□ Implement Kalman filter for sensor fusion
□ Know RNP levels and monitoring (ANP vs RNP required)
□ Calculate LNAV steering (cross-track error correction)
□ Understand 4D trajectory and RTA (time-constrained navigation)
□ Calculate Cost Index optimal speed/altitude
□ Manage AIRAC database cycle (28-day updates)
□ Integrate with autopilot (LNAV/VNAV modes)

================================================================================
12. Key Takeaways
================================================================================

1. **FMS = Flight Automation:** Automates flight planning, navigation, performance optimization

2. **ARINC 702A = Advanced FMS:** RNP AR, 4D trajectory, CPDLC datalink integration

3. **Multi-Sensor Navigation:** GPS primary, IRS backup, Kalman filter blends all sources

4. **RNP = Navigation Accuracy:** RNP 0.1 = ±0.1 nm (95%), critical for curved approaches

5. **VNAV = Vertical Guidance:** Calculates Top of Descent, manages altitude/speed constraints

6. **LNAV = Lateral Guidance:** Follows flight plan, corrects cross-track error

7. **4D Trajectory = Time Dimension:** RTA (Required Time of Arrival) for ATC sequencing

8. **Cost Index = Speed/Fuel Trade-off:** CI=0 (slow, efficient), CI=999 (fast, burn fuel)

9. **ARINC 424 Database = Navigation Data:** 28-day AIRAC cycle, Jeppesen/Lufthansa providers

10. **ARINC 615A = Database Loading:** Ethernet-based high-speed loading (vs legacy 615 serial)

11. **RF Legs = Curved Flight Paths:** Constant-radius turns, required for RNP AR approaches

12. **Integration = FMS + Autopilot + Displays:** Seamless automation from takeoff to landing

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 702 — Advanced Flight Management Computer System (1996)
- ARINC 702A — Advanced FMS with RNP/4D (2004)
- ARINC 424 — Navigation System Database
- ARINC 615A — Software Data Loader Using Ethernet

**Navigation:**
- FAA Order 8260.58 — RNP Authorization Required (AR) Procedures
- ICAO PBN Manual (Doc 9613) — Performance-Based Navigation
- RTCA DO-236C — Minimum Aviation System Performance Standards (MASPS) for RNP

**Aircraft Systems:**
- Boeing 737 FMC User's Guide
- Airbus A320 FMGS (Flight Management Guidance System) Manual
- Honeywell Epic FMS Documentation

**Software:**
- Kalman Filtering: Theory and Practice (Grewal & Andrews)
- Flight Management Systems (Raimund Wyatt)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Standards:** ARINC 702/702A, ARINC 424, DO-236C

================================================================================
