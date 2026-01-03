**ADAS Sensor Fusion & Sensor Types Cheat Sheet**  
(oriented toward production vehicles in 2025–2026 – L2+/L3 highway & urban systems)

### 1. Sensor Types Comparison Table

Sensor Type       | Typical Specs (2025–2026)                  | Strengths                                      | Weaknesses                                   | Main ADAS Functions                          | Cost Level | Redundancy Role
------------------|---------------------------------------------|------------------------------------------------|----------------------------------------------|----------------------------------------------|------------|-----------------
**Mono Camera**   | 1–3 MP, 30–120° FOV, HDR                    | Rich semantic info, lane/traffic sign detection| Weather/light sensitive, no direct distance  | TSR, LKA, FCW, object classification         | Low        | Primary perception
**Stereo Camera** | Dual 2–8 MP, baseline 10–30 cm              | Good depth up to ~50–80 m                      | Limited range, compute heavy                 | Depth estimation, AEB, pedestrian detection  | Medium     | Distance in good conditions
**4D Imaging Radar** | 77/79 GHz, 120–300 m range, 120° FOV      | All-weather, direct velocity & elevation       | Low resolution, poor classification          | ACC, AEB, BSD, RCTA, cut-in detection        | Medium     | Robust long-range backup
**LiDAR (mid/long)** | 905/1550 nm, 120–300 m, 120–360° FOV       | Very accurate 3D point cloud, good in darkness | Weather degradation (rain/snow/fog), high cost| Precise object localization, occupancy grid | High       | High-confidence 3D mapping
**Ultrasonic**    | 40–58 kHz, <5–7 m range                     | Very cheap, excellent close-range              | Extremely short range, no velocity           | Parking, low-speed obstacle detection        | Very low   | Short-range complement
**Thermal (IR) Camera** | 640×512 or higher, LWIR/MWIR             | Works in total darkness, fog, glare            | Low resolution, poor detail in good weather  | Night-time pedestrian/cyclist detection      | Medium-High| Adverse weather complement
**V2X (C-V2X)**   | 5.9 GHz, DSRC/PC5                           | Beyond line-of-sight awareness                 | Infrastructure dependency, latency issues    | Intersection assist, platoon info            | Medium     | Cooperative perception

### 2. Sensor Fusion Strategies (2025–2026 dominant approaches)

Strategy                  | Description                                                                 | Typical Sensors Combined                          | Strengths                                  | Most Common In
-------------------------|-----------------------------------------------------------------------------|---------------------------------------------------|--------------------------------------------|--------------------
**Early / Low-level Fusion** | Raw sensor data fused before object detection                              | Camera + Radar + LiDAR point clouds               | Highest accuracy, best handling of occlusion| Premium L2+/L3 (Mercedes Drive Pilot style)
**Mid-level / Feature-level Fusion** | Features (bounding boxes, points, velocities) fused                       | Camera detections + Radar points + LiDAR clusters | Good balance of compute & accuracy         | Most mass-market L2+ (Tesla, Mobileye, Bosch)
**Late / High-level / Object-level Fusion** | Independent detections from each sensor → fused tracks / objects         | Separate camera tracker + radar tracker           | Simple, modular, fault-tolerant            | Many Tier-1 suppliers (Continental, Aptiv)
**Centralized Fusion**    | One central perception module fuses everything                              | All sensors → single BEV/occupancy network        | Optimal fusion, end-to-end learning possible| NVIDIA Orin / Qualcomm Ride / Mobileye EyeQ6
**Distributed / Zonal Fusion** | Sensors fused locally in zones → results sent to central planner         | Corner radars + zonal camera → zonal BEV          | Reduces bandwidth, fault isolation         | Emerging zonal E/E architectures

### 3. Modern Perception Output Representations (2025–2026)

Representation             | Description                                                                 | Best For                                   | Typical Models / Frameworks
--------------------------|-----------------------------------------------------------------------------|--------------------------------------------|---------------------------
**BEV (Bird’s Eye View)** | Top-down 2D/3D grid around ego vehicle                                     | Surround view, path planning               | BEVFormer, BEVFusion, UniAD
**Occupancy Network**     | Voxel / grid predicting occupancy probability per cell                     | Free space, drivable area                  | OccNet, OpenOccupancy
**3D Object Detection**   | Bounding boxes in 3D space with class, velocity, yaw                       | Object tracking & prediction               | CenterPoint, DETR3D, Sparse4D
**Multi-modal Fusion**    | Explicit fusion of camera + LiDAR/radar features                            | Robustness in adverse weather              | TransFusion, AutoAlign, CLOCs

### 4. Key Performance Metrics for Sensor Fusion

Metric                    | Target (L2+/L3 highway 2025–2026) | Why It Matters
-------------------------|------------------------------------|---------------
**Detection Range**       | 150–250 m (pedestrian/car)         | Early braking / decision making
**False Positive Rate**   | <1 per 1000 km                     | Driver trust & avoid unnecessary interventions
**False Negative Rate**   | Extremely low (<0.1% critical cases)| Safety – missing a pedestrian is catastrophic
**Perception Latency**    | 50–150 ms end-to-end               | Reaction time in emergency
**Update Rate**           | 10–30 Hz                           | Smooth tracking & prediction
**Adverse Weather Robustness** | ≥80–90% of clear-weather performance | Regulatory & consumer expectation

### 5. Quick One-liners (what perception engineers say in 2025–2026)

- “Camera is still king for semantics; radar is king for velocity & weather.”
- “LiDAR is becoming a commodity – but only for high-confidence distance.”
- “BEV fusion is the 2026 standard – almost everyone moved away from separate trackers.”
- “Occupancy networks are replacing traditional object lists for free-space reasoning.”
- “Sensor fusion must provide uncertainty estimates – deterministic outputs are dead.”
- “Early fusion gives the best results but needs 10× more compute.”
- “Redundancy is perception + monitoring channel – not just duplicate sensors.”

### 6. Typical Sensor Suites (2025–2026 production examples)

Vehicle Class / OEM Example       | Typical Suite (2025–2026)
----------------------------------|--------------------------------
Mass-market L2 (VW, Hyundai, etc.)| 1 mono + 4 surround cameras + 5–7 radars + 12 ultrasonics
Premium L2+ (BMW, Mercedes)       | 1–3 stereo + 8–12 surround cameras + 6–9 radars + 1–3 mid-range LiDAR
L3 Highway (Mercedes Drive Pilot) | 3 LiDAR + 12 cameras + 6 radars + thermal + V2X
Tesla (Vision-only)               | 8–11 cameras + radar (reinforced 2025+) – no LiDAR
Mobileye / Tier-1 reference       | 11 cameras + 6 radars + 1–3 LiDAR (scalable)

Good luck with your ADAS perception & fusion design!  
In 2026 the winning formula is usually **camera + 4D radar fusion in BEV space** with **LiDAR as high-confidence complement** for L3 highway systems – and **occupancy networks** are rapidly becoming the standard output format for planning.