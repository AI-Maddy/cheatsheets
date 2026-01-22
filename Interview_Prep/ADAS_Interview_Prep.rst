
═══════════════════════════════════════════════════════════════════════
ADAS (ADVANCED DRIVER ASSISTANCE SYSTEMS) INTERVIEW PREPARATION
═══════════════════════════════════════════════════════════════════════

**Target Roles:** ADAS Engineer, Autonomous Driving SW Engineer, Perception Engineer
**Difficulty:** Intermediate to Advanced
**Preparation Time:** 4-6 hours
**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════

⚡ **QUICK REVISION (12-MINUTE READ)**
─────────────────────────────────────────────────────────────────────────

**ADAS System Architecture:**

.. code-block:: text

    ┌─────────────────────────────────────────────────────────┐
    │                ADAS ECU (Central Compute)               │
    ├─────────────────────────────────────────────────────────┤
    │  Application Layer                                      │
    │  ┌──────────┬──────────┬──────────┬──────────────────┐ │
    │  │ Path     │ Decision │ Behavior │ HMI              │ │
    │  │ Planning │ Making   │ Planning │ (Visualization)  │ │
    │  └──────────┴──────────┴──────────┴──────────────────┘ │
    ├─────────────────────────────────────────────────────────┤
    │  Perception & Sensor Fusion                             │
    │  ┌──────────┬──────────┬──────────┬──────────────────┐ │
    │  │ Object   │ Lane     │ Free     │ Sensor           │ │
    │  │ Detection│ Detection│ Space    │ Fusion           │ │
    │  └──────────┴──────────┴──────────┴──────────────────┘ │
    ├─────────────────────────────────────────────────────────┤
    │  Sensor Abstraction Layer                               │
    │  ┌────────┬────────┬────────┬────────┬──────────────┐  │
    │  │ Camera │ Radar  │ LiDAR  │ USS    │ V2X          │  │
    │  │ Driver │ Driver │ Driver │ Driver │ Driver       │  │
    │  └────────┴────────┴────────┴────────┴──────────────┘  │
    └─────────────────────────────────────────────────────────┘
              ↕            ↕         ↕         ↕
    ┌─────────────┐ ┌──────────┐ ┌──────┐ ┌─────────┐
    │ Camera (8)  │ │ Radar (5)│ │LiDAR │ │ USS (12)│
    │ - Front     │ │ - Front  │ │ (1-4)│ │ Parking │
    │ - Rear      │ │ - Corner │ │      │ │ Sensors │
    │ - Surround  │ │ - Rear   │ │      │ │         │
    └─────────────┘ └──────────┘ └──────┘ └─────────┘

**SAE Autonomy Levels:**

.. code-block:: text

    Level 0: No Automation (manual driving)
    Level 1: Driver Assistance (ACC or LKA)
    Level 2: Partial Automation (ACC + LKA, hands-on)
    Level 3: Conditional Automation (hands-off, eyes-off allowed)
    Level 4: High Automation (no driver needed in ODD)
    Level 5: Full Automation (anywhere, anytime)

**Key ADAS Features:**

1. **ACC (Adaptive Cruise Control)** - Maintains safe distance
2. **LKA (Lane Keeping Assist)** - Centers vehicle in lane
3. **AEB (Automatic Emergency Braking)** - Collision avoidance
4. **BSD (Blind Spot Detection)** - Warns of adjacent vehicles
5. **TSR (Traffic Sign Recognition)** - Reads speed limits, signs
6. **APA (Automated Parking Assist)** - Self-parking

**Sensor Comparison:**

| Sensor | Range | FOV | Weather | Resolution | Cost | Use Case |
|--------|-------|-----|---------|------------|------|----------|
| **Camera** | 150m | 120° | Poor (rain/fog) | High (pixels) | Low | Lane, signs, objects |
| **Radar** | 250m | 30° | Excellent | Low (sparse) | Medium | Speed, distance |
| **LiDAR** | 200m | 360° | Fair | Very High | High | 3D mapping |
| **Ultrasonic** | 5m | Wide | Good | Low | Very Low | Parking |

**ISO 26262 ASIL Levels:**

.. code-block:: text

    ASIL D → Highest safety (AEB, steering)
    ASIL C → High safety
    ASIL B → Medium safety (ACC)
    ASIL A → Low safety
    QM     → No safety requirements

**Sensor Fusion Algorithms:**

- **Kalman Filter** - Linear state estimation
- **Extended Kalman Filter (EKF)** - Non-linear state estimation
- **Particle Filter** - Multi-modal distributions
- **Bayesian Fusion** - Probabilistic data association

═══════════════════════════════════════════════════════════════════════

🎯 **TOP 25 INTERVIEW QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**BEGINNER LEVEL (8 Questions)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q1: Explain the difference between ADAS and autonomous driving**

**Answer:**

| Aspect | ADAS | Autonomous Driving |
|--------|------|-------------------|
| **SAE Level** | L0-L2 | L3-L5 |
| **Driver Role** | Always responsible | Conditional/no responsibility |
| **Hands on Wheel** | Required (L2) | Not required (L3+) |
| **Attention** | Required | Not required (L4+) |
| **Liability** | Driver | OEM/System (L4+) |
| **Examples** | ACC, LKA, AEB | Tesla FSD, Waymo |
| **ASIL** | ASIL B-D | ASIL D + redundancy |
| **Sensors** | 3-5 cameras, 2-3 radars | 8+ cameras, 5+ radars, LiDAR |

**Key Difference:**
- **ADAS** - Driver assistance (driver in control)
- **Autonomous** - System in control (driver optional/not needed)

*Talking Point:* "In our Level 2 ADAS system, we had driver monitoring (DMS) to ensure hands-on-wheel and attention. For Level 3+, we'd need redundant systems and fail-operational architecture."

───────────────────────────────────────────────────────────────────────

**Q2: What is sensor fusion and why is it necessary?**

**Answer:**
Sensor fusion combines data from multiple sensors (camera, radar, LiDAR) to create a more accurate and reliable perception of the environment.

**Why Necessary:**

1. **Complementary Strengths**
   - Camera: Good object classification, poor range
   - Radar: Excellent range/speed, poor resolution
   - LiDAR: Precise 3D, expensive, poor in rain

2. **Redundancy**
   - Camera fails in fog → Radar continues
   - Radar misses stationary objects → Camera detects

3. **Accuracy**
   - Single sensor: 85% detection
   - Fused sensors: 95%+ detection

**Sensor Fusion Example:**

.. code-block:: text

    Scenario: Detecting a car at night
    
    Camera:
      ✓ Detects taillights
      ✓ Classifies as "car"
      ✗ Poor distance estimation
    
    Radar:
      ✓ Accurate distance (50m)
      ✓ Relative speed (-20 km/h)
      ✗ Cannot classify object type
    
    Fusion Result:
      ✓ Object: Car
      ✓ Distance: 50m
      ✓ Speed: -20 km/h (approaching)
      ✓ Confidence: 95%

**Fusion Algorithm (Simplified):**

.. code-block:: python

    # Weighted average based on confidence
    fused_distance = (camera_dist * camera_conf + 
                     radar_dist * radar_conf) / 
                    (camera_conf + radar_conf)
    
    # Object classification (camera primary)
    if camera_conf > 0.8:
        object_type = camera_class
    else:
        object_type = "unknown"

───────────────────────────────────────────────────────────────────────

**Q3: Explain Adaptive Cruise Control (ACC) architecture**

**Answer:**

**ACC System Components:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │         ACC Application                 │
    ├─────────────────────────────────────────┤
    │  1. Target Selection                    │
    │     - Select vehicle to follow          │
    │     - Track ID, distance, speed         │
    ├─────────────────────────────────────────┤
    │  2. Velocity Controller                 │
    │     - PID control for speed             │
    │     - Maintain set speed or follow      │
    ├─────────────────────────────────────────┤
    │  3. Distance Controller                 │
    │     - Time gap control (1.5-2.5s)       │
    │     - Safe following distance           │
    ├─────────────────────────────────────────┤
    │  4. Actuation                           │
    │     - Throttle control                  │
    │     - Brake control                     │
    └─────────────────────────────────────────┘
              ↓                    ↑
    ┌─────────────────┐   ┌────────────────┐
    │ CAN Bus         │   │ Sensor Inputs  │
    │ - Throttle      │   │ - Radar        │
    │ - Brake         │   │ - Camera       │
    │ - Steering      │   │ - Vehicle Speed│
    └─────────────────┘   └────────────────┘

**ACC Control Logic:**

.. code-block:: c

    // Simplified ACC controller
    typedef enum {
        ACC_CRUISE,        // No target, maintain set speed
        ACC_FOLLOW,        // Target detected, follow mode
        ACC_APPROACH,      // Approaching target, reduce speed
        ACC_EMERGENCY      // Critical distance, hard brake
    } acc_state_t;
    
    acc_state_t acc_update(void) {
        float target_distance = radar_get_distance();
        float target_speed = radar_get_relative_speed();
        float ego_speed = vehicle_get_speed();
        
        // Calculate time gap
        float time_gap = target_distance / ego_speed;
        
        if (target_distance == NO_TARGET) {
            // No vehicle ahead, cruise at set speed
            set_throttle_position(cruise_speed);
            return ACC_CRUISE;
        }
        else if (time_gap < TIME_GAP_CRITICAL) {
            // Emergency braking
            set_brake_pressure(MAX_BRAKE);
            return ACC_EMERGENCY;
        }
        else if (time_gap < TIME_GAP_TARGET) {
            // Reduce speed to increase gap
            float brake = pid_controller(TIME_GAP_TARGET - time_gap);
            set_brake_pressure(brake);
            return ACC_APPROACH;
        }
        else {
            // Follow mode, match target speed
            float target_accel = target_speed / time_gap;
            set_throttle_position(target_accel);
            return ACC_FOLLOW;
        }
    }

**ACC Performance Requirements:**

- **Reaction time:** < 200ms
- **Time gap:** 1.5 - 2.5 seconds (adjustable)
- **Speed range:** 30 - 180 km/h
- **Max deceleration:** 3 m/s² (comfort), 6 m/s² (emergency)
- **ASIL:** ASIL B

───────────────────────────────────────────────────────────────────────

**Q4: What is Lane Keeping Assist (LKA) and how does it work?**

**Answer:**

**LKA System Architecture:**

.. code-block:: text

    ┌──────────────────────────────────────┐
    │  Front Camera (Windshield)           │
    │  - Lane markers detection            │
    │  - 60° FOV, 720p @ 30 FPS            │
    └──────────────────────────────────────┘
                  ↓
    ┌──────────────────────────────────────┐
    │  Lane Detection Algorithm            │
    │  - Edge detection (Canny)            │
    │  - Hough transform (line detection)  │
    │  - Lane model (polynomial fit)       │
    └──────────────────────────────────────┘
                  ↓
    ┌──────────────────────────────────────┐
    │  Lane Keeping Controller             │
    │  - Calculate lateral offset          │
    │  - Calculate heading error           │
    │  - PID controller for steering       │
    └──────────────────────────────────────┘
                  ↓
    ┌──────────────────────────────────────┐
    │  Electric Power Steering (EPS)       │
    │  - Apply corrective torque           │
    │  - Smooth intervention               │
    └──────────────────────────────────────┘

**Lane Detection Pipeline:**

.. code-block:: python

    import cv2
    import numpy as np
    
    def detect_lanes(image):
        # 1. Grayscale conversion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Gaussian blur (noise reduction)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 3. Edge detection
        edges = cv2.Canny(blur, 50, 150)
        
        # 4. Region of interest (trapezoid)
        height, width = edges.shape
        roi = np.array([
            [(0, height),
             (width/2 - 50, height/2 + 50),
             (width/2 + 50, height/2 + 50),
             (width, height)]
        ], dtype=np.int32)
        mask = np.zeros_like(edges)
        cv2.fillPoly(mask, roi, 255)
        masked_edges = cv2.bitwise_and(edges, mask)
        
        # 5. Hough line detection
        lines = cv2.HoughLinesP(masked_edges, 
                                rho=2, 
                                theta=np.pi/180, 
                                threshold=100,
                                minLineLength=40,
                                maxLineGap=5)
        
        # 6. Separate left and right lanes
        left_lines, right_lines = [], []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            
            if slope < -0.5:  # Left lane (negative slope)
                left_lines.append(line)
            elif slope > 0.5:  # Right lane (positive slope)
                right_lines.append(line)
        
        return left_lines, right_lines

**LKA Control Algorithm:**

.. code-block:: c

    // Lateral controller
    typedef struct {
        float lateral_offset;    // Distance from lane center (m)
        float heading_error;     // Angle to lane direction (rad)
        float curvature;         // Lane curvature (1/m)
    } lane_state_t;
    
    float lka_controller(lane_state_t *lane, float vehicle_speed) {
        // PID gains (tuned for vehicle dynamics)
        const float Kp = 0.5;   // Proportional
        const float Kd = 0.1;   // Derivative
        
        // Calculate desired steering angle
        float steering_p = Kp * lane->lateral_offset;
        float steering_d = Kd * lane->heading_error;
        
        // Feedforward for curvature
        float steering_ff = lane->curvature * vehicle_speed * vehicle_speed;
        
        // Total steering command
        float steering = steering_p + steering_d + steering_ff;
        
        // Limit steering torque (driver override)
        if (steering > MAX_TORQUE)
            steering = MAX_TORQUE;
        
        return steering;
    }

**LKA Requirements:**

- **Activation speed:** > 60 km/h
- **Lane width:** 2.5 - 4.0 meters
- **Max lateral offset:** ± 0.5 meters
- **Steering intervention:** < 3 Nm (gentle)
- **Driver override:** Immediate (hands on wheel)
- **ASIL:** ASIL B

───────────────────────────────────────────────────────────────────────

**Q5: Explain Automatic Emergency Braking (AEB) system**

**Answer:**

**AEB System Architecture:**

.. code-block:: text

    ┌────────────────────────────────────────┐
    │  Sensors (Redundant)                   │
    │  - Front camera (object detection)     │
    │  - Front radar (distance, speed)       │
    │  - (Optional) LiDAR                    │
    └────────────────────────────────────────┘
                    ↓
    ┌────────────────────────────────────────┐
    │  Threat Assessment                     │
    │  - Time To Collision (TTC)             │
    │  - Collision probability               │
    │  - Brake demand calculation            │
    └────────────────────────────────────────┘
                    ↓
    ┌────────────────────────────────────────┐
    │  AEB Decision Logic                    │
    │  ┌──────┬──────┬──────┬──────────────┐ │
    │  │ No   │ Pre- │ Partial │ Full       │ │
    │  │Action│ Warn │ Brake   │ Brake      │ │
    │  └──────┴──────┴──────┴──────────────┘ │
    └────────────────────────────────────────┘
                    ↓
    ┌────────────────────────────────────────┐
    │  Brake Actuation (ESP/ABS)             │
    │  - Hydraulic brake pressure            │
    │  - Max deceleration: 10 m/s²           │
    └────────────────────────────────────────┘

**AEB Decision Stages:**

.. code-block:: c

    typedef enum {
        AEB_NO_ACTION,      // TTC > 2.5s
        AEB_PRE_WARNING,    // TTC 2.0-2.5s (visual/audio)
        AEB_PARTIAL_BRAKE,  // TTC 1.5-2.0s (50% brake)
        AEB_FULL_BRAKE      // TTC < 1.5s (100% brake)
    } aeb_state_t;
    
    aeb_state_t aeb_decision(float distance, float relative_speed, float ego_speed) {
        // Time To Collision
        float ttc = distance / relative_speed;
        
        // Deceleration required to avoid collision
        float required_decel = (relative_speed * relative_speed) / (2 * distance);
        
        // Maximum comfortable deceleration
        const float MAX_COMFORT_DECEL = 3.0;  // m/s²
        const float MAX_EMERGENCY_DECEL = 10.0;  // m/s²
        
        if (ttc > 2.5 || relative_speed <= 0) {
            // No collision risk
            return AEB_NO_ACTION;
        }
        else if (ttc > 2.0) {
            // Warn driver
            display_warning();
            sound_alert();
            return AEB_PRE_WARNING;
        }
        else if (ttc > 1.5 || required_decel < MAX_COMFORT_DECEL) {
            // Partial braking (driver reaction time)
            set_brake_pressure(0.5 * MAX_BRAKE);
            return AEB_PARTIAL_BRAKE;
        }
        else {
            // Emergency full braking
            set_brake_pressure(MAX_BRAKE);
            log_aeb_activation();  // For ASIL traceability
            return AEB_FULL_BRAKE;
        }
    }

**False Positive Mitigation:**

.. code-block:: c

    // Confirm threat over multiple frames
    typedef struct {
        int threat_count;
        int frame_count;
        float ttc_min;
    } threat_tracker_t;
    
    bool confirm_threat(threat_tracker_t *tracker, float ttc) {
        tracker->frame_count++;
        
        if (ttc < 2.0) {
            tracker->threat_count++;
            if (ttc < tracker->ttc_min)
                tracker->ttc_min = ttc;
        }
        
        // Require 3 consecutive frames of threat
        if (tracker->threat_count >= 3 && tracker->frame_count <= 5)
            return true;
        
        // Reset if threat disappears
        if (tracker->frame_count > 10) {
            tracker->threat_count = 0;
            tracker->frame_count = 0;
            tracker->ttc_min = 999.0;
        }
        
        return false;
    }

**AEB Test Scenarios (Euro NCAP):**

1. **Car-to-Car Rear Stationary (CCRs)** - Stationary vehicle
2. **Car-to-Car Rear Moving (CCRm)** - Slower moving vehicle
3. **Car-to-Car Rear Braking (CCRb)** - Sudden braking ahead
4. **Pedestrian Adult (CPFA)** - Adult crossing street
5. **Pedestrian Child (CPNC)** - Child running from behind parked car

**ASIL:** ASIL D (highest safety integrity level)

───────────────────────────────────────────────────────────────────────

**Q6: What are the key sensors used in ADAS and their roles?**

**Answer:**

**1. Camera (Vision Sensor)**

**Specifications:**
- Resolution: 1280x720 (720p) to 1920x1080 (1080p)
- Frame rate: 30-60 FPS
- FOV: 50° (telephoto) to 120° (wide-angle)
- Range: Up to 150 meters

**Advantages:**
✓ High resolution (object classification)
✓ Color information (traffic lights, signs)
✓ Low cost ($50-200 per camera)
✓ Lane marking detection

**Disadvantages:**
✗ Poor performance in low light, fog, rain
✗ Limited range estimation accuracy
✗ Requires image processing compute

**Use Cases:**
- Lane detection (LKA)
- Traffic sign recognition (TSR)
- Object classification (car, pedestrian, bike)
- Forward collision warning (FCW)

**Example Camera Configuration:**

.. code-block:: text

    Front Windshield:
    - Main camera: 52° FOV, 100m range
    - Wide camera: 120° FOV, 50m range
    
    Surround View (4 cameras):
    - Front: 190° fisheye
    - Rear: 190° fisheye
    - Left/Right: 180° each

───────────────────────────────────────────────────────────────────────

**2. Radar (Radio Detection and Ranging)**

**Specifications:**
- Frequency: 77 GHz (automotive radar)
- Range: 250 meters (long-range), 30m (short-range)
- FOV: 30° (LRR), 150° (SRR)
- Update rate: 50-100 Hz

**Advantages:**
✓ Excellent in all weather (rain, fog, snow)
✓ Accurate range and velocity measurement (Doppler)
✓ Works in darkness
✓ Mature technology

**Disadvantages:**
✗ Low resolution (cannot classify objects)
✗ Poor elevation measurement
✗ Metallic objects only (misses foam, cardboard)

**Use Cases:**
- ACC (distance and speed)
- AEB (collision detection)
- Blind spot detection (BSD)
- Cross-traffic alert (RCTA)

**Radar Configuration:**

.. code-block:: text

    5-Radar Setup:
    - Front LRR: 250m, 30° FOV (ACC, AEB)
    - Front-Left SRR: 30m, 150° FOV (BSD)
    - Front-Right SRR: 30m, 150° FOV (BSD)
    - Rear-Left SRR: 30m, 150° FOV (BSD)
    - Rear-Right SRR: 30m, 150° FOV (RCTA)

───────────────────────────────────────────────────────────────────────

**3. LiDAR (Light Detection and Ranging)**

**Specifications:**
- Wavelength: 905nm or 1550nm (infrared)
- Range: 200-300 meters
- FOV: 360° (rotating) or 120° (solid-state)
- Resolution: 128+ lines, 0.1° angular resolution
- Update rate: 10-20 Hz

**Advantages:**
✓ Precise 3D point cloud
✓ Accurate range (cm-level)
✓ High resolution (object shape)
✓ Works in darkness

**Disadvantages:**
✗ High cost ($1,000-$10,000+)
✗ Degraded in heavy rain, fog
✗ Cannot detect material type
✗ High data rate (requires compute)

**Use Cases:**
- 3D mapping and localization
- Free space detection
- Object detection (pedestrians, cyclists)
- Parking (360° view)

**LiDAR Types:**

| Type | Cost | FOV | Range | Use Case |
|------|------|-----|-------|----------|
| **Mechanical** (Rotating) | High | 360° | 300m | Robotaxis |
| **Solid-State** (MEMS) | Medium | 120° | 200m | Production ADAS |
| **Flash LiDAR** | Low | 30° | 50m | Parking |

───────────────────────────────────────────────────────────────────────

**4. Ultrasonic Sensors (USS)**

**Specifications:**
- Frequency: 40 kHz
- Range: 0.15 - 5 meters
- FOV: 120° cone
- Update rate: 20 Hz

**Advantages:**
✓ Very low cost ($5-10 each)
✓ Short-range accuracy
✓ Reliable in all conditions

**Disadvantages:**
✗ Very limited range (< 5m)
✗ Slow update rate
✗ Cannot classify objects

**Use Cases:**
- Parking assist (APA)
- Park distance control (PDC)
- Low-speed collision avoidance

**USS Configuration (12 sensors):**

.. code-block:: text

    Front: 4 sensors (bumper)
    Rear: 4 sensors (bumper)
    Front-Left: 2 sensors (side)
    Front-Right: 2 sensors (side)

───────────────────────────────────────────────────────────────────────

**5. V2X (Vehicle-to-Everything)**

**Types:**
- **V2V** (Vehicle-to-Vehicle) - Car-to-car communication
- **V2I** (Vehicle-to-Infrastructure) - Traffic lights, RSUs
- **V2P** (Vehicle-to-Pedestrian) - Smartphone pedestrian warning

**Technology:**
- **DSRC** (802.11p) - 5.9 GHz, 300m range
- **C-V2X** (Cellular) - 4G/5G based

**Use Cases:**
- Intersection collision warning
- Emergency vehicle alert
- Traffic light optimization
- Cooperative ACC (CACC)

**Sensor Fusion Example:**

.. code-block:: text

    Scenario: Detecting pedestrian at night crossing street
    
    Camera: ✗ Poor visibility (dark)
    Radar: ✗ Non-metallic target (low return)
    LiDAR: ✓ Detects 3D point cloud (pedestrian shape)
    
    Fusion: LiDAR primary, camera confirms (if visible)

═══════════════════════════════════════════════════════════════════════

**INTERMEDIATE LEVEL (10 Questions)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q7: Explain Kalman Filter for sensor fusion**

**Answer:**

**Kalman Filter** is an algorithm that estimates the state of a system from noisy sensor measurements.

**Key Concepts:**

- **State:** Position, velocity (what we want to estimate)
- **Prediction:** Estimate next state based on motion model
- **Update:** Correct prediction with sensor measurement
- **Uncertainty:** Covariance matrix (how confident we are)

**Kalman Filter Steps:**

.. code-block:: text

    1. Prediction (Time Update)
       - Predict state: x̂ₖ = F·x̂ₖ₋₁ + B·uₖ
       - Predict covariance: Pₖ = F·Pₖ₋₁·Fᵀ + Q
    
    2. Update (Measurement Update)
       - Innovation: yₖ = zₖ - H·x̂ₖ
       - Kalman Gain: Kₖ = Pₖ·Hᵀ·(H·Pₖ·Hᵀ + R)⁻¹
       - Update state: x̂ₖ = x̂ₖ + Kₖ·yₖ
       - Update covariance: Pₖ = (I - Kₖ·H)·Pₖ

**Example: Tracking Vehicle Position**

.. code-block:: c

    #include <stdio.h>
    #include <math.h>
    
    typedef struct {
        float x;      // Position (m)
        float v;      // Velocity (m/s)
        float P[2][2]; // Covariance matrix
    } kalman_state_t;
    
    void kalman_predict(kalman_state_t *state, float dt) {
        // State transition matrix F
        // [1  dt]
        // [0  1 ]
        float x_pred = state->x + state->v * dt;
        float v_pred = state->v;
        
        // Predict covariance P = F·P·Fᵀ + Q
        float P00 = state->P[0][0] + 2*dt*state->P[0][1] + dt*dt*state->P[1][1];
        float P01 = state->P[0][1] + dt*state->P[1][1];
        float P10 = state->P[1][0] + dt*state->P[1][1];
        float P11 = state->P[1][1];
        
        // Process noise Q (uncertainty in motion model)
        float Q_pos = 0.1;  // Position process noise
        float Q_vel = 0.1;  // Velocity process noise
        
        state->x = x_pred;
        state->v = v_pred;
        state->P[0][0] = P00 + Q_pos;
        state->P[0][1] = P01;
        state->P[1][0] = P10;
        state->P[1][1] = P11 + Q_vel;
    }
    
    void kalman_update(kalman_state_t *state, float measurement, float R) {
        // Measurement matrix H = [1  0] (we measure position only)
        
        // Innovation (measurement residual)
        float y = measurement - state->x;
        
        // Innovation covariance S = H·P·Hᵀ + R
        float S = state->P[0][0] + R;
        
        // Kalman gain K = P·Hᵀ·S⁻¹
        float K0 = state->P[0][0] / S;
        float K1 = state->P[1][0] / S;
        
        // Update state x̂ = x̂ + K·y
        state->x += K0 * y;
        state->v += K1 * y;
        
        // Update covariance P = (I - K·H)·P
        float P00 = (1 - K0) * state->P[0][0];
        float P01 = (1 - K0) * state->P[0][1];
        float P10 = state->P[1][0] - K1 * state->P[0][0];
        float P11 = state->P[1][1] - K1 * state->P[0][1];
        
        state->P[0][0] = P00;
        state->P[0][1] = P01;
        state->P[1][0] = P10;
        state->P[1][1] = P11;
    }
    
    // Example usage
    int main() {
        kalman_state_t state = {
            .x = 0.0,
            .v = 0.0,
            .P = {{1000, 0}, {0, 1000}}  // High initial uncertainty
        };
        
        float dt = 0.1;  // 100ms update cycle
        float R = 5.0;   // Measurement noise (radar: ±5m)
        
        // Simulation: vehicle moving at 10 m/s
        for (int i = 0; i < 100; i++) {
            // Predict
            kalman_predict(&state, dt);
            
            // Simulate noisy measurement
            float true_pos = 10.0 * i * dt;
            float noise = (rand() / (float)RAND_MAX - 0.5) * 10.0;
            float measurement = true_pos + noise;
            
            // Update
            kalman_update(&state, measurement, R);
            
            printf("t=%.1f: true=%.2f, measured=%.2f, estimated=%.2f\n",
                   i*dt, true_pos, measurement, state.x);
        }
        
        return 0;
    }

**When to Use Kalman Filter:**
- Tracking vehicles (position, velocity)
- Fusing radar + camera
- Lane position estimation
- Ego vehicle localization

**Limitations:**
- Assumes linear system (use EKF for non-linear)
- Assumes Gaussian noise
- Requires tuning Q and R matrices

───────────────────────────────────────────────────────────────────────

**Q8: How does object detection work in ADAS? (Deep Learning)**

**Answer:**

**Object Detection Pipeline:**

.. code-block:: text

    Camera Image (1280x720)
          ↓
    ┌────────────────────────────┐
    │ Preprocessing              │
    │ - Resize to network input  │
    │ - Normalize (0-1 or -1,1)  │
    │ - Color space (RGB)        │
    └────────────────────────────┘
          ↓
    ┌────────────────────────────┐
    │ Neural Network             │
    │ - CNN backbone (ResNet)    │
    │ - Feature extraction       │
    │ - Object proposal          │
    │ - Classification & Bbox    │
    └────────────────────────────┘
          ↓
    ┌────────────────────────────┐
    │ Post-processing            │
    │ - Non-Max Suppression (NMS)│
    │ - Confidence thresholding  │
    │ - Coordinate transformation│
    └────────────────────────────┘
          ↓
    Detected Objects:
    [Car: (x,y,w,h), conf=0.95]
    [Pedestrian: (x,y,w,h), conf=0.89]

**Popular Object Detection Networks:**

| Network | Speed (FPS) | Accuracy (mAP) | Use Case |
|---------|-------------|----------------|----------|
| **YOLOv5** | 140 | 50.7% | Real-time ADAS |
| **YOLOv8** | 100 | 53.9% | High accuracy |
| **SSD** | 59 | 46.5% | Embedded systems |
| **Faster R-CNN** | 7 | 42.0% | Offline processing |

**YOLOv5 Example (PyTorch):**

.. code-block:: python

    import torch
    import cv2
    
    # Load pre-trained model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.eval()
    
    # Classes relevant to ADAS
    adas_classes = ['person', 'bicycle', 'car', 'motorcycle', 
                    'bus', 'truck', 'traffic light', 'stop sign']
    
    def detect_objects(image_path):
        # Read image
        img = cv2.imread(image_path)
        
        # Run inference
        results = model(img)
        
        # Parse results
        detections = results.pandas().xyxy[0]
        
        for idx, det in detections.iterrows():
            if det['name'] in adas_classes and det['confidence'] > 0.5:
                x1, y1, x2, y2 = int(det['xmin']), int(det['ymin']), \
                                 int(det['xmax']), int(det['ymax'])
                label = f"{det['name']} {det['confidence']:.2f}"
                
                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                print(f"Detected: {label} at [{x1},{y1},{x2},{y2}]")
        
        return img, detections
    
    # Process camera frame
    output_img, detections = detect_objects('dashcam.jpg')
    cv2.imshow('ADAS Detection', output_img)
    cv2.waitKey(0)

**Real-Time Optimization (Automotive ECU):**

1. **Model Quantization** (INT8 vs FP32)
   - Reduce model size: 100MB → 25MB
   - Increase speed: 2x-4x faster
   - Slight accuracy loss: ~2%

.. code-block:: python

    # TensorRT quantization (NVIDIA)
    import tensorrt as trt
    
    # Convert model to TensorRT INT8
    with trt.Builder(TRT_LOGGER) as builder:
        builder.max_batch_size = 1
        builder.int8_mode = True
        builder.int8_calibrator = calibrator
        engine = builder.build_cuda_engine(network)

2. **Hardware Acceleration**
   - GPU: NVIDIA Xavier (30 TOPS)
   - NPU: Qualcomm SA8295 (60 TOPS)
   - FPGA: Custom accelerator

3. **Network Pruning**
   - Remove redundant weights
   - Reduce compute by 50%

**Safety Considerations (ISO 26262):**

.. code-block:: c

    // Confidence thresholding
    #define CONFIDENCE_THRESHOLD 0.7
    
    // Temporal filtering (require 3 consecutive detections)
    typedef struct {
        int detection_count;
        bbox_t last_bbox;
    } object_tracker_t;
    
    bool confirm_object(object_tracker_t *tracker, bbox_t bbox, float conf) {
        if (conf < CONFIDENCE_THRESHOLD)
            return false;
        
        // Check if bbox is close to previous detection
        float iou = calculate_iou(tracker->last_bbox, bbox);
        if (iou > 0.5) {
            tracker->detection_count++;
        } else {
            tracker->detection_count = 1;
        }
        
        tracker->last_bbox = bbox;
        
        // Require 3 consecutive detections
        return (tracker->detection_count >= 3);
    }

───────────────────────────────────────────────────────────────────────

**Q9: Explain ISO 26262 and ASIL levels in ADAS context**

**Answer:**

**ISO 26262** is the international standard for functional safety of electrical/electronic systems in road vehicles.

**ASIL (Automotive Safety Integrity Level):**

.. code-block:: text

    ASIL D → Highest (severe injury/death risk)
    ASIL C → High
    ASIL B → Medium
    ASIL A → Low
    QM (Quality Management) → No safety requirements

**ASIL Determination:**

ASIL = f(Severity, Exposure, Controllability)

| Factor | Description | Scale |
|--------|-------------|-------|
| **Severity (S)** | Injury consequence | S0-S3 (S3=fatal) |
| **Exposure (E)** | Frequency of situation | E0-E4 (E4=high) |
| **Controllability (C)** | Driver can avoid? | C0-C3 (C3=uncontrollable) |

**Example: AEB System**

- **Severity:** S3 (potential fatality if AEB fails)
- **Exposure:** E4 (daily driving)
- **Controllability:** C3 (driver cannot react in time)
- **Result:** ASIL D

**ADAS Feature ASIL Classification:**

| Feature | ASIL | Justification |
|---------|------|---------------|
| **AEB** | D | Life-critical, uncontrollable |
| **LKA** | B | Driver can override, lower severity |
| **ACC** | B | Driver monitors, can brake |
| **BSD** | A | Warning only, driver controls |
| **Parking Assist** | A | Low speed, driver supervises |
| **TSR** | QM | Informational, no actuation |

**ISO 26262 V-Model:**

.. code-block:: text

    Concept Phase
    ├─ Hazard Analysis & Risk Assessment (HARA)
    └─ Functional Safety Concept
    
    System Level
    ├─ Technical Safety Concept
    ├─ System Design
    └─ System Integration & Test
    
    Hardware Level
    ├─ Hardware Safety Requirements
    ├─ Hardware Design
    └─ Hardware Integration & Test
    
    Software Level
    ├─ Software Safety Requirements
    ├─ Software Architectural Design
    ├─ Software Unit Design & Implementation
    └─ Software Unit Test

**Safety Mechanisms (Examples):**

1. **Redundancy** (ASIL D requirement)

.. code-block:: c

    // Dual sensor fusion (camera + radar)
    typedef struct {
        bool camera_detected;
        bool radar_detected;
        float camera_distance;
        float radar_distance;
    } redundant_detection_t;
    
    bool aeb_trigger(redundant_detection_t *det) {
        // Require both sensors to agree
        if (det->camera_detected && det->radar_detected) {
            float diff = fabs(det->camera_distance - det->radar_distance);
            if (diff < 5.0) {  // Distances agree within 5m
                return true;
            }
        }
        return false;
    }

2. **Watchdog** (Alive monitoring)

.. code-block:: c

    // Software watchdog
    #define WATCHDOG_TIMEOUT_MS 100
    
    void adas_main_loop(void) {
        while (1) {
            kick_watchdog();  // Reset watchdog timer
            
            process_sensors();
            run_perception();
            update_control();
            
            // If loop hangs, watchdog resets ECU
        }
    }

3. **Plausibility Checks**

.. code-block:: c

    // Check sensor values are physically possible
    bool radar_plausibility_check(float distance, float speed) {
        if (distance < 0 || distance > 250)  // Radar max range
            return false;
        
        if (speed < -50 || speed > 80)  // Reasonable speed range
            return false;
        
        // Check if speed is consistent with previous frame
        static float last_distance = 0;
        static uint32_t last_time = 0;
        
        uint32_t now = get_time_ms();
        float dt = (now - last_time) / 1000.0;
        float calculated_speed = (last_distance - distance) / dt;
        
        if (fabs(calculated_speed - speed) > 10.0)  // ±10 m/s tolerance
            return false;
        
        last_distance = distance;
        last_time = now;
        return true;
    }

4. **Graceful Degradation**

.. code-block:: c

    typedef enum {
        SYSTEM_NORMAL,
        SYSTEM_DEGRADED_L1,  // One sensor failed
        SYSTEM_DEGRADED_L2,  // Two sensors failed
        SYSTEM_FAIL_SAFE     // Critical failure
    } system_state_t;
    
    system_state_t determine_system_state(void) {
        bool camera_ok = check_camera_health();
        bool radar_ok = check_radar_health();
        
        if (camera_ok && radar_ok) {
            return SYSTEM_NORMAL;
        } else if (camera_ok || radar_ok) {
            log_degradation();
            display_warning_to_driver();
            return SYSTEM_DEGRADED_L1;  // Continue with one sensor
        } else {
            disable_adas_features();
            display_critical_error();
            return SYSTEM_FAIL_SAFE;  // Disable ADAS
        }
    }

**Safety Case (Evidence):**
- **Requirements traceability** - Each safety requirement tested
- **Code review** - Peer review for ASIL C/D
- **Unit testing** - 100% statement coverage (ASIL D)
- **Integration testing** - Fault injection
- **Validation** - Real-world testing (millions of km)

───────────────────────────────────────────────────────────────────────

**Q10: How do you handle sensor failures in ADAS?**

**Answer:**

**Sensor Failure Types:**

1. **Hard Failure** - Sensor completely dead (no data)
2. **Soft Failure** - Sensor provides erroneous data
3. **Degraded Performance** - Reduced accuracy (fog, dirt)

**Failure Detection Methods:**

**1. Hardware Monitoring:**

.. code-block:: c

    typedef struct {
        bool power_ok;
        bool communication_ok;
        bool temperature_ok;
        uint32_t last_update_ms;
    } sensor_health_t;
    
    sensor_health_t check_camera_health(void) {
        sensor_health_t health = {0};
        
        // Check power supply
        health.power_ok = (read_voltage(CAMERA_PWR) > 11.0);
        
        // Check CAN communication
        uint32_t now = get_time_ms();
        health.communication_ok = (now - camera_last_msg_time < 200);
        
        // Check temperature
        float temp = read_temperature(CAMERA_TEMP_SENSOR);
        health.temperature_ok = (temp < 85.0);  // Max operating temp
        
        health.last_update_ms = now;
        
        return health;
    }

**2. Plausibility Checks:**

.. code-block:: c

    // Check if radar data is physically possible
    bool validate_radar_data(radar_data_t *data) {
        // Range check
        if (data->distance < 0.5 || data->distance > 250.0)
            return false;
        
        // Velocity check (relative speed)
        if (data->velocity < -50.0 || data->velocity > 80.0)
            return false;
        
        // RCS (Radar Cross Section) check
        if (data->rcs < -10.0 || data->rcs > 40.0)  // dBsm
            return false;
        
        // Temporal consistency
        static float last_distance = 0;
        float expected_distance = last_distance + data->velocity * 0.02;  // 20ms cycle
        if (fabs(data->distance - expected_distance) > 5.0)
            return false;
        
        last_distance = data->distance;
        return true;
    }

**3. Cross-Sensor Validation:**

.. code-block:: c

    // Compare camera and radar for same object
    bool cross_validate_object(camera_obj_t *cam_obj, radar_obj_t *radar_obj) {
        // Distance agreement (within 10%)
        float dist_diff = fabs(cam_obj->distance - radar_obj->distance);
        if (dist_diff / radar_obj->distance > 0.1)
            return false;
        
        // Lateral position agreement (within 1m)
        float lateral_diff = fabs(cam_obj->lateral_pos - radar_obj->lateral_pos);
        if (lateral_diff > 1.0)
            return false;
        
        return true;
    }

**Failure Mitigation Strategies:**

**1. Sensor Redundancy:**

.. code-block:: c

    typedef struct {
        bool camera_available;
        bool radar_available;
        bool lidar_available;
        int sensor_count;
    } sensor_availability_t;
    
    sensor_availability_t get_sensor_availability(void) {
        sensor_availability_t avail = {0};
        
        avail.camera_available = check_camera_health().communication_ok;
        avail.radar_available = check_radar_health().communication_ok;
        avail.lidar_available = check_lidar_health().communication_ok;
        
        avail.sensor_count = avail.camera_available + 
                            avail.radar_available + 
                            avail.lidar_available;
        
        return avail;
    }
    
    // Adapt ADAS features based on available sensors
    void adapt_adas_features(sensor_availability_t *avail) {
        if (avail->sensor_count >= 2) {
            // Full ADAS functionality
            enable_acc();
            enable_lka();
            enable_aeb();
        } else if (avail->sensor_count == 1) {
            // Degraded mode (limited features)
            if (avail->radar_available) {
                enable_acc();       // Radar sufficient for ACC
                disable_lka();      // LKA needs camera
                enable_aeb_limited(); // Radar-only AEB
            } else if (avail->camera_available) {
                disable_acc();      // ACC needs precise range (radar)
                enable_lka();       // LKA works with camera
                enable_aeb_limited(); // Camera-only AEB
            }
        } else {
            // Fail-safe mode (disable all ADAS)
            disable_all_adas();
            notify_driver("ADAS unavailable - Service required");
        }
    }

**2. Temporal Filtering:**

.. code-block:: c

    // Require N consecutive valid readings before trusting sensor
    #define VALID_COUNT_THRESHOLD 5
    
    typedef struct {
        int valid_count;
        int invalid_count;
        bool trusted;
    } sensor_trust_t;
    
    void update_sensor_trust(sensor_trust_t *trust, bool valid) {
        if (valid) {
            trust->valid_count++;
            trust->invalid_count = 0;
            
            if (trust->valid_count >= VALID_COUNT_THRESHOLD)
                trust->trusted = true;
        } else {
            trust->invalid_count++;
            trust->valid_count = 0;
            
            if (trust->invalid_count >= 3)
                trust->trusted = false;
        }
    }

**3. Limp-Home Mode:**

.. code-block:: c

    // Provide minimal functionality to safely stop vehicle
    void enter_limp_home_mode(void) {
        // Disable autonomous features
        disable_acc();
        disable_lka();
        
        // Keep critical safety features if possible
        if (radar_available) {
            enable_forward_collision_warning();  // Warning only, no braking
        }
        
        // Limit vehicle speed
        set_max_speed(60);  // km/h
        
        // Notify driver
        display_warning("ADAS malfunction - Manual control required");
        sound_alert();
        
        // Log fault for service
        log_dtc(DTC_ADAS_SENSOR_FAILURE);
    }

**4. Sensor Cleaning/Recovery:**

.. code-block:: c

    // Attempt to recover degraded sensor (e.g., dirty camera)
    bool attempt_sensor_recovery(sensor_type_t sensor) {
        switch (sensor) {
            case SENSOR_CAMERA:
                // Activate washer/wiper
                activate_camera_washer();
                msleep(5000);  // Wait for cleaning
                
                // Re-test camera
                if (check_camera_health().communication_ok) {
                    log_event("Camera recovered after cleaning");
                    return true;
                }
                break;
                
            case SENSOR_RADAR:
                // Radar self-test/recalibration
                send_radar_command(RADAR_CMD_SELF_TEST);
                msleep(2000);
                
                if (check_radar_health().communication_ok) {
                    log_event("Radar recovered after self-test");
                    return true;
                }
                break;
        }
        
        return false;
    }

**Real-World Example:**

*Talking Point:* "In our Level 2+ ADAS system, we implemented a 3-tier degradation strategy:
1. **Normal:** Camera + Radar → Full ADAS (ACC, LKA, AEB)
2. **Degraded:** Radar only → ACC + Radar-based AEB (no LKA)
3. **Fail-Safe:** No sensors → Disable ADAS, manual driving only

This allowed the vehicle to continue operating safely even with a camera failure, which occurred in ~0.5% of field deployments (due to wiper malfunction or extreme weather)."

═══════════════════════════════════════════════════════════════════════

📝 **RESUME TALKING POINTS**
─────────────────────────────────────────────────────────────────────────

**When asked: "Tell me about your ADAS experience"**

**1. Sensor Integration**
- "Integrated front camera (OV10635) and 77 GHz radar (Bosch MRR) for ACC/AEB"
- "Implemented sensor fusion using Extended Kalman Filter"
- "Achieved 95% object detection accuracy in real-world testing"

**2. Feature Development**
- "Developed ACC feature supporting 30-180 km/h with 1.5-2.5s time gap"
- "Implemented LKA using Canny edge detection and Hough transform"
- "Achieved < 0.5m lateral accuracy for lane centering"

**3. Safety (ISO 26262)**
- "Designed AEB system to ASIL D requirements with redundant sensing"
- "Implemented watchdog, plausibility checks, and fail-safe mechanisms"
- "Reduced false positives from 15% to < 2% through temporal filtering"

**4. Performance Optimization**
- "Optimized YOLOv5 object detection: 30 FPS → 60 FPS (TensorRT INT8)"
- "Reduced boot time from 15s to 3s for ADAS ECU"
- "Achieved < 100ms end-to-end latency (sensor to actuation)"

**Quantifiable Results:**
- 95% object detection accuracy
- < 100ms latency
- < 2% false positive rate
- 1 million km validation testing

═══════════════════════════════════════════════════════════════════════

**Last Updated:** January 2026
**Good Luck with Your Interview! 🚀**

═══════════════════════════════════════════════════════════════════════
