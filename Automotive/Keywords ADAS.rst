
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **ADAS Keyword List with One-Line Explanations**  
(most relevant terms used in modern ADAS / AD systems in 2025–2026)

📚 Core ADAS Functions & Features

- **AEB** – Automatic Emergency Braking: autonomously applies brakes to 🔴 🔴 avoid or mitigate collision  
- **ACC** – Adaptive Cruise Control: maintains set speed and safe following distance using radar/camera  
- **LKA** – Lane Keeping Assist: gently steers to keep vehicle in lane (hands-on)  
- **LCA** – Lane Change Assist: assists or automates lane changes (with driver confirmation)  
- **ELKA** – Emergency Lane Keeping Assist: emergency steering to 🔴 🔴 avoid obstacle or stay in lane  
- **TSR** – Traffic Sign Recognition: detects and displays speed limits, no-overtaking, etc.  
- **ISA** – Intelligent Speed Assistance: warns or actively limits speed according to signs  
- **FCW** – Forward Collision 🟡 🟡 Warning: audio/visual alert before potential front collision  
- **LDW** – Lane Departure 🟡 🟡 Warning: alerts driver when unintentionally leaving lane  
- **BSD** – Blind Spot Detection: warns of vehicles in adjacent blind spots  
- **RCTA** – Rear Cross Traffic Alert: warns of approaching traffic when reversing  
- **APA** – Automated Parking Assist: semi/full automatic parallel/perpendicular parking  
- **TJA** – Traffic Jam Assist: low-speed ACC + LKA in congested traffic  
- **HWA** – Highway Assist: hands-off lane centering + ACC on highways (L2+)  
- **NOA** – Navigate on Autopilot: highway autonomous driving with on/off-ramp handling (L2+/L3)  

📡 Sensors & Perception

- **Mono Camera** – Single forward-facing camera (basic ADAS)  
- **Stereo Camera** – Two cameras for depth estimation  
- **4D Imaging Radar** – High-resolution radar with elevation & velocity (corner radars)  
- **LiDAR** – Laser scanner for precise 3D point cloud (mostly L2+ / L3)  
- **Ultrasonic** – Short-range sensors for parking & low-speed obstacle detection  
- **Thermal Camera** – Infrared camera for night & adverse weather detection  
- **Sensor Fusion** – Combining camera + radar + LiDAR data for robust perception  
- **BEV** – Bird’s Eye View: top-down surround view created from multiple sensors  
- **Occupancy Network** – Modern AI model predicting 3D space occupancy instead of objects  

🧮 Compute & Architecture

- **SoC** – System-on-Chip: main ADAS compute unit (Orin, EyeQ6, TDA4, Snapdragon Ride, etc.)  
- **Domain Controller** – Central high-performance ECU for ADAS/AD functions  
- **Zonal Architecture** – Vehicle divided into physical zones with zonal controllers  
- **Safety Island** – Isolated ASIL-D partition for monitoring & fallback  
- **Redundancy** – Dual-channel or diverse compute for fail-operational systems  

⚙️ AI & Perception Models

- **YOLO** – You Only Look Once: real-time object detection family (v8/v9/v10 common in 2026)  
- **DETR** – Detection Transformer: end-to-end object detection without anchors  
- **BEVFormer** – Bird’s-Eye-View Transformer: temporal & multi-camera fusion  
- **Occupancy Network** – Predicts 3D voxel occupancy instead of discrete objects  
- **Transformer** – Dominant architecture in modern perception models  
- **End-to-End** – Direct mapping from sensor input to driving commands (emerging trend)  

🛡️ Safety & Standards

- **ASIL** – Automotive Safety Integrity Level (A–D, D = highest)  
- **ASIL B(D)** – Most common decomposition for L2 actuation paths  
- **ISO 26262** – Functional safety standard for road vehicles  
- **SOTIF** (ISO 21448) – Safety Of The Intended Functionality (non-failure hazards)  
- **Fail-Operational** – System remains functional after single failure (L3+)  
- **Fail-Safe** – System goes to safe state after failure (L2)  
- **ODD** – Operational Design Domain: conditions under which system is valid  
- **E2E Protection** – End-to-End data integrity protection on communication  

📌 Other Frequently Used Terms

- **V2X** – Vehicle-to-Everything communication (C-V2X / DSRC)  
- **HD Map** – High-Definition map with lane-level precision  
- **SLAM** – Simultaneous Localization And Mapping (used in mapping & positioning)  
⭐ - **OTA** – Over-The-Air update (critical for perception & planning improvements)  
- **SOME/IP** – Scalable service-Oriented MiddlewarE over IP (AUTOSAR Adaptive)  
- **DDS** – Data Distribution Service (real-time pub/sub middleware)  
- **ROS2** – Robot Operating System 2 (widely used in prototyping & some production)  
- **AUTOSAR Adaptive** – High-performance AUTOSAR variant for ADAS/AD  

This list covers ~95% of the terms you will see in ADAS meetings, papers, requirements, and job descriptions in 2026.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
