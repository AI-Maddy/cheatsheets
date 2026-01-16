🔐⚙️ **Cyber-Physical Systems Safety — Security-Safety Co-Engineering**
═══════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for CPS Safety in the Era of Connected Systems**  
**Domains:** Smart Grid ⚡ | Automotive 🚗 | Industrial IoT 🏭 | Medical Devices 🏥 | Avionics ✈️  
**Standards:** IEC 62443 + IEC 61508 | ISO/SAE 21434 + ISO 26262 | IEC 62351 | IEC 81001-5-1  
**Critical Insight:** Cyber attacks can cause physical harm — security is a safety prerequisite

═══════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What are Cyber-Physical Systems (CPS)?**

.. code-block:: text

   CPS = Computation + Communication + Physical Processes
   
   Examples:
   ✈️ Fly-by-wire aircraft (sensors → computers → actuators)
   🚗 Autonomous vehicles (LIDAR → AI → braking/steering)
   ⚡ Smart grid (meters → control center → breakers)
   🏥 Insulin pumps (glucose sensor → algorithm → pump)
   🏭 Industrial robots (vision → controller → motors)

**Why Security Matters for Safety:**

.. code-block:: text

   Traditional Safety Assumption: Failures are random
   ❌ FALSE in CPS: Attackers cause intentional, malicious failures
   
   Examples of Security → Safety Impact:
   
   🚗 Automotive: Hacker disables brakes remotely
      → ISO/SAE 21434 (cybersecurity) now mandatory with ISO 26262 (safety)
   
   ⚡ Smart Grid: Stuxnet-like attack trips circuit breakers
      → Blackout, cascading failures
   
   🏥 Medical: Ransomware locks infusion pump controls
      → Cannot adjust dosage, patient harm
   
   🏭 Industrial: PLC malware (Triton/TRISIS) disables safety system
      → Explosion, fire risk

**Unified Threat Model:**

.. code-block:: text

   Traditional Approach (WRONG):
   - Safety team: FMEA, FTA (assumes random failures)
   - Security team: Threat modeling (assumes malicious intent)
   - NO COORDINATION → Gaps in coverage
   
   Integrated Approach (CORRECT):
   - Combined FMEA + Threat Analysis
   - Attack trees merged with fault trees
   - Security controls treated as safety barriers
   
   Example: Automotive brake-by-wire
   
   Fault Tree Branch:           Attack Tree Branch:
   Brake ECU fails      +       Hacker spoofs CAN message
   → No braking         +       → Disables brakes
   ↓                            ↓
   Combined Mitigation: Secure CAN (authentication) + Dual ECU redundancy

**Key Standards Integration:**

+-----------------+---------------------+-------------------------+
| Domain          | Safety Standard     | Security Standard       |
+=================+=====================+=========================+
| Automotive      | ISO 26262           | ISO/SAE 21434           |
+-----------------+---------------------+-------------------------+
| Industrial      | IEC 61508           | IEC 62443               |
+-----------------+---------------------+-------------------------+
| Medical         | IEC 62304           | IEC 81001-5-1           |
+-----------------+---------------------+-------------------------+
| Power Grid      | IEC 61850 (safety)  | IEC 62351 (security)    |
+-----------------+---------------------+-------------------------+
| Avionics        | DO-178C/DO-254      | DO-326A/DO-356A         |
+-----------------+---------------------+-------------------------+

**2026 Regulatory Trend:** Security certification is becoming MANDATORY for safety-critical CPS (not optional).

═══════════════════════════════════════════════════════════════════════════════

📖 **1. CPS ARCHITECTURE AND THREAT SURFACE**
═══════════════════════════════════════════════════════════════════════════════

1.1 CPS Components
------------------

**Four-Layer Architecture:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │ Layer 4: Enterprise/Cloud (SCADA, Fleet Management)    │
   │ Threat: Remote access, data exfiltration               │
   └─────────────────────────────────────────────────────────┘
                            ▲
                            │ Internet/WAN
                            ▼
   ┌─────────────────────────────────────────────────────────┐
   │ Layer 3: Control Systems (PLC, ECU, Flight Computer)   │
   │ Threat: Logic tampering, malware injection             │
   └─────────────────────────────────────────────────────────┘
                            ▲
                            │ Industrial Network (CAN, Modbus, EtherCAT)
                            ▼
   ┌─────────────────────────────────────────────────────────┐
   │ Layer 2: Field Devices (Sensors, Actuators, Instruments)│
   │ Threat: Sensor spoofing, actuator hijacking            │
   └─────────────────────────────────────────────────────────┘
                            ▲
                            │ I/O Signals
                            ▼
   ┌─────────────────────────────────────────────────────────┐
   │ Layer 1: Physical Process (Motor, Valve, Brakes, Turbine)│
   │ Threat: Physical damage from cyber attack              │
   └─────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────

**1.2 Attack Vectors in CPS**
-----------------------------

**External Attacks:**

.. code-block:: text

   1. Remote Network Access:
      - Internet-facing interfaces (cloud connectivity, remote diagnostics)
      - Wi-Fi/Bluetooth (medical devices, automotive infotainment)
      - Cellular (telematics, fleet management)
   
   2. Supply Chain Compromise:
      - Malicious firmware in components (hardware trojans)
      - Backdoors in third-party software libraries
      - Counterfeit parts with vulnerabilities

**Insider Attacks:**

.. code-block:: text

   3. Rogue Maintenance Personnel:
      - Physical access to diagnostic ports
      - Upload malicious configuration
   
   4. Malicious Software Updates:
      - Compromised OTA (Over-The-Air) update server
      - Unsigned firmware injection

**Attack Progression Example (Automotive):**

.. code-block:: text

   Step 1: Exploit infotainment system vulnerability (Internet-facing)
   Step 2: Pivot to internal CAN bus (lateral movement)
   Step 3: Spoof sensor messages (GPS, wheel speed)
   Step 4: Override braking commands
   Result: Crash (cyber attack → physical harm)

────────────────────────────────────────────────────────────────────────────

**1.3 Security vs Safety Failures**
-----------------------------------

**Random Failures (Safety Focus):**

.. code-block:: text

   Characteristics:
   - Independent events (component wear, environmental stress)
   - Statistically predictable (MTBF, Weibull distribution)
   - No intent to harm
   
   Example: Sensor drift over time → incorrect reading

**Malicious Failures (Security Focus):**

.. code-block:: text

   Characteristics:
   - Intelligent adversary (adaptive, goal-oriented)
   - Coordinated attacks (multiple simultaneous failures)
   - Designed to bypass safety mechanisms
   
   Example: Attacker spoofs multiple redundant sensors simultaneously
            (defeats 2oo3 voting system)

**Common Cause Failure (Both):**

.. code-block:: text

   Cyber Attack as Common Cause:
   - Single vulnerability in shared software component
   - Affects all redundant channels simultaneously
   
   Example: Automotive dual ECU redundancy (1oo2)
   - Both ECUs run same firmware
   - Zero-day exploit affects both
   - Redundancy provides NO protection against cyber attack
   
   Mitigation: Diverse redundancy (different hardware, different software)

═══════════════════════════════════════════════════════════════════════════════

📖 **2. AUTOMOTIVE: ISO/SAE 21434 + ISO 26262 INTEGRATION**
═══════════════════════════════════════════════════════════════════════════════

2.1 ISO/SAE 21434 Overview (Cybersecurity)
-------------------------------------------

**Standard:** ISO/SAE 21434:2021 — Road vehicles — Cybersecurity engineering

**Lifecycle Phases:**

.. code-block:: text

   1. Concept Phase:
      - Define cybersecurity goals (no unauthorized access to brakes)
      - Asset identification (ECUs, sensors, networks)
   
   2. Product Development:
      - Threat Analysis and Risk Assessment (TARA)
      - Cybersecurity requirements (authentication, encryption)
      - Secure implementation (code review, penetration testing)
   
   3. Production:
      - Supply chain security (verify component authenticity)
   
   4. Operations & Maintenance:
      - Incident response (detect attacks, deploy patches)
      - Vulnerability management (monitor CVEs)
   
   5. Decommissioning:
      - Secure data deletion

────────────────────────────────────────────────────────────────────────────

**2.2 TARA (Threat Analysis and Risk Assessment)**
--------------------------------------------------

**Process:**

.. code-block:: text

   Step 1: Asset Identification
   - ECUs: Engine control, braking, steering
   - Networks: CAN, Ethernet, OBD-II port
   - Data: Vehicle speed, GPS location, personal info
   
   Step 2: Threat Scenarios
   - Attacker gains remote access via cellular modem
   - Attacker spoofs wheel speed sensor via CAN injection
   
   Step 3: Impact Rating (Severity)
   - Safety impact: Critical (potential crash)
   - Financial impact: Medium (warranty costs)
   - Privacy impact: High (location tracking)
   
   Step 4: Attack Feasibility
   - Attack Path: Remote → Telematics → CAN bus → Brake ECU
   - Skill level: Expert (requires reverse engineering)
   - Time: 6 months (for proof-of-concept)
   
   Step 5: CAL (Cybersecurity Assurance Level)
   CAL = f(Impact, Feasibility)
   
   CAL 1-4 (similar to ASIL in ISO 26262)
   - CAL 4: Most stringent (critical safety functions)
   - CAL 1: Least stringent (non-safety, low impact)

**CAL Determination Table:**

+----------------+-------------+-------------+-------------+-------------+
| Impact ↓       | Feasibility: Very Low    | Low         | Medium      | High        |
+================+=============+=============+=============+=============+
| Severe         | CAL 2       | CAL 3       | CAL 4       | CAL 4       |
+----------------+-------------+-------------+-------------+-------------+
| Major          | CAL 1       | CAL 2       | CAL 3       | CAL 3       |
+----------------+-------------+-------------+-------------+-------------+
| Moderate       | CAL 1       | CAL 1       | CAL 2       | CAL 2       |
+----------------+-------------+-------------+-------------+-------------+
| Negligible     | CAL 1       | CAL 1       | CAL 1       | CAL 1       |
+----------------+-------------+-------------+-------------+-------------+

────────────────────────────────────────────────────────────────────────────

**2.3 ISO 26262 + ISO/SAE 21434 Integration**
---------------------------------------------

**Challenge:** Both standards have different risk assessment methods

.. code-block:: text

   ISO 26262 (Safety):
   - Hazard Analysis and Risk Assessment (HARA)
   - ASIL (Automotive Safety Integrity Level) A-D
   - Based on: Severity, Exposure, Controllability
   
   ISO/SAE 21434 (Security):
   - Threat Analysis and Risk Assessment (TARA)
   - CAL (Cybersecurity Assurance Level) 1-4
   - Based on: Impact, Attack Feasibility

**Integrated Approach:**

.. code-block:: text

   Step 1: Conduct HARA (identify safety hazards)
   Example: "Unintended braking at highway speed" → ASIL D
   
   Step 2: Conduct TARA (identify cyber threats to safety functions)
   Example: "Attacker sends malicious CAN message to brake ECU" → CAL 4
   
   Step 3: Combined Requirements
   - Safety: Dual ECU redundancy (1oo2), plausibility checks
   - Security: CAN message authentication (HMAC), secure boot
   
   Step 4: Unified Safety Case
   Argument: "System is safe because:
   1. Random failures mitigated by redundancy (ISO 26262)
   2. Malicious failures prevented by authentication (ISO/SAE 21434)"

**Example: Automotive Brake-by-Wire**

.. code-block:: python

   # Safety requirement (ISO 26262 ASIL D)
   def brake_plausibility_check(pedal_position, wheel_speeds):
       """Detect sensor failures"""
       if pedal_position > 0.9 and all(ws > 100 for ws in wheel_speeds):
           # Brake pedal pressed but wheels still spinning fast (implausible)
           return FAULT_DETECTED
       return OK
   
   # Security requirement (ISO/SAE 21434 CAL 4)
   def verify_can_message_authentication(can_msg):
       """Prevent spoofed CAN messages"""
       received_mac = can_msg.mac
       computed_mac = hmac.new(secret_key, can_msg.data, hashlib.sha256).digest()
       
       if received_mac != computed_mac:
           # Message authentication failed (potential attack)
           return REJECT_MESSAGE
       return ACCEPT_MESSAGE
   
   # Integrated control logic
   def process_brake_command(can_msg):
       # Security check first
       if verify_can_message_authentication(can_msg) == REJECT_MESSAGE:
           log_security_event("Unauthenticated brake command rejected")
           return SAFE_STATE  # Ignore message
       
       # Safety check second
       pedal = can_msg.data['pedal_position']
       wheel_speeds = get_wheel_speeds()
       
       if brake_plausibility_check(pedal, wheel_speeds) == FAULT_DETECTED:
           log_safety_event("Implausible brake sensor readings")
           return SAFE_STATE
       
       # Both checks passed → execute brake command
       apply_brakes(pedal)

═══════════════════════════════════════════════════════════════════════════════

📖 **3. INDUSTRIAL: IEC 62443 + IEC 61508 INTEGRATION**
═══════════════════════════════════════════════════════════════════════════════

3.1 IEC 62443 Overview (Industrial Cybersecurity)
--------------------------------------------------

**Standard:** IEC 62443 — Security for industrial automation and control systems (IACS)

**Four Pillars:**

.. code-block:: text

   IEC 62443-1: General (concepts, terminology)
   IEC 62443-2: Policies & Procedures (asset owner, operator)
   IEC 62443-3: System (network segmentation, security levels)
   IEC 62443-4: Component (device requirements, secure development)

**Security Levels (SL):**

.. code-block:: text

   SL 1: Protection against casual or coincidental violation
   SL 2: Protection against intentional violation using simple means
   SL 3: Protection against intentional violation using sophisticated means
   SL 4: Protection against intentional violation using sophisticated means
         with extended resources

**Example Mapping:**

+---------------------------+----------------+------------------------+
| Asset                     | Security Level | Justification          |
+===========================+================+========================+
| Safety PLC (SIS)          | SL 3-4         | Controls safety        |
|                           |                | shutdown               |
+---------------------------+----------------+------------------------+
| Process control PLC       | SL 2-3         | Production impact      |
+---------------------------+----------------+------------------------+
| HMI workstation           | SL 2           | Operator interface     |
+---------------------------+----------------+------------------------+
| Historian database        | SL 1-2         | Data logging           |
+---------------------------+----------------+------------------------+

────────────────────────────────────────────────────────────────────────────

**3.2 Defense in Depth (Network Segmentation)**
-----------------------------------------------

**Purdue Model (ISA-95):**

.. code-block:: text

   Level 5: Enterprise Network (ERP, business systems)
   ═══════════════════════════════════════════════
   Firewall + DMZ
   ───────────────────────────────────────────────
   Level 4: Site Operations (SCADA, MES)
   ═══════════════════════════════════════════════
   Firewall (deep packet inspection)
   ───────────────────────────────────────────────
   Level 3: Site Control (Supervisory control, HMI)
   ═══════════════════────════════════════════════
   Industrial Firewall (unidirectional gateway for SIS)
   ───────────────────────────────────────────────
   Level 2: Area Control (PLC, DCS, Safety PLC)
   ═══════════════════════════════════════════════
   Network segmentation (VLANs, separate subnets)
   ───────────────────────────────────────────────
   Level 1: Field Devices (Sensors, actuators, drives)
   ═══════════════════════════════════════════════
   Level 0: Physical Process

**Security Zones:**

.. code-block:: text

   Safety Zone (highest protection):
   - Safety Instrumented System (SIS) PLC
   - Emergency shutdown (ESD) logic
   - Unidirectional gateway (data OUT only, no commands IN)
   - IEC 62443 SL-4, IEC 61508 SIL 3/4
   
   Control Zone:
   - Process control PLCs
   - Standard industrial firewall
   - IEC 62443 SL-2/3, IEC 61508 SIL 1/2
   
   Enterprise Zone:
   - IT systems, business logic
   - Standard IT security (TLS, VPN)

────────────────────────────────────────────────────────────────────────────

**3.3 IEC 61508 + IEC 62443 Combined Requirements**
---------------------------------------------------

**Example: Chemical Plant Safety Instrumented System (SIS)**

.. code-block:: text

   Function: Emergency shutdown if pressure exceeds safe limit
   
   IEC 61508 (Safety) Requirements:
   - SIL 3 (Safety Integrity Level 3)
   - 1oo2 voting (two pressure sensors, one must trigger)
   - Proof test interval: 1 year
   - Safe failure fraction (SFF) ≥ 90%
   
   IEC 62443 (Security) Requirements:
   - SL-4 (Security Level 4)
   - Unidirectional gateway (SIS network isolated)
   - Authenticated configuration changes (dual approval)
   - Secure firmware updates (signed, verified)
   
   Combined Architecture:
   
   ┌─────────────────────────────────────────────────┐
   │ SCADA System (Control Network)                  │
   │ IEC 62443 SL-2                                  │
   └─────────────────────────────────────────────────┘
                     │
                     │ Unidirectional Gateway
                     │ (Data OUT only, no commands IN)
                     ▼
   ┌─────────────────────────────────────────────────┐
   │ Safety PLC (Safety Network)                     │
   │ IEC 61508 SIL 3 + IEC 62443 SL-4                │
   │                                                 │
   │ Inputs: Pressure Sensor #1, Pressure Sensor #2  │
   │ Logic: IF P1 > limit OR P2 > limit THEN shutdown│
   │ Output: Close emergency valve                   │
   └─────────────────────────────────────────────────┘

**Key Insight:** Security controls (unidirectional gateway) act as additional safety barriers (prevent malicious commands from disabling safety system).

═══════════════════════════════════════════════════════════════════════════════

📖 **4. UNIFIED THREAT AND HAZARD ANALYSIS**
═══════════════════════════════════════════════════════════════════════════════

4.1 Combined FMEA + Threat Analysis
------------------------------------

**Traditional FMEA (Failure Modes and Effects Analysis):**

.. code-block:: text

   Component: Wheel Speed Sensor
   Failure Mode: Sensor stuck at zero
   Cause: Electrical short, connector corrosion
   Effect: ABS thinks car is stopped, no braking assistance
   Detection: Plausibility check (compare with other sensors)
   RPN = Severity × Occurrence × Detection

**Extended FMEA with Security:**

+------------------+----------------------+------------------+------------------+
| Failure Mode     | Random Cause (Safety)| Malicious Cause  | Combined         |
|                  |                      | (Security)       | Mitigation       |
+==================+======================+==================+==================+
| Sensor stuck     | Electrical short     | CAN bus spoofing | 1. Redundant     |
| at zero          | (random)             | (intentional)    |    sensors       |
|                  |                      |                  | 2. CAN auth      |
+------------------+----------------------+------------------+------------------+
| Sensor drift     | Aging, temperature   | GPS jamming      | 1. Kalman filter |
|                  | (random)             | (intentional)    | 2. Multi-GNSS    |
+------------------+----------------------+------------------+------------------+
| No sensor output | Wiring break         | DoS attack       | 1. Watchdog      |
|                  | (random)             | (intentional)    | 2. Rate limiting |
+------------------+----------------------+------------------+------------------+

────────────────────────────────────────────────────────────────────────────

**4.2 Attack Trees + Fault Trees Integration**
----------------------------------------------

**Example: Autonomous Vehicle Lane Keeping**

**Fault Tree (Safety Focus):**

.. code-block:: text

                 Unintended Lane Departure
                          |
            ┌─────────────┴─────────────┐
            │                           │
      Camera Failure              Steering Failure
            │                           │
      ┌─────┴─────┐             ┌───────┴────────┐
      │           │             │                │
   Lens fog   Sensor   Motor    Controller
              dead     seized   crash

**Attack Tree (Security Focus):**

.. code-block:: text

                 Cause Lane Departure (Attacker Goal)
                          |
            ┌─────────────┴─────────────┐
            │                           │
    Blind Camera                Hijack Steering
            │                           │
      ┌─────┴─────┐             ┌───────┴────────┐
      │           │             │                │
   Laser    Adversarial   CAN bus      Firmware
   dazzle   pattern       injection    backdoor

**Combined Tree:**

.. code-block:: text

                 Unintended Lane Departure
                          |
            ┌─────────────┴──────────────────┐
            │                                │
      Camera Unavailable            Steering Malfunction
            |                                |
   ┌────────┼────────┐            ┌──────────┼──────────┐
   │        │        │            │          │          │
  Fog  Sensor  Laser    Motor  Controller  CAN       Firmware
       dead   dazzle   seized    crash    inject    backdoor
       (R)    (M)      (R)       (R)      (M)       (M)
   
   Legend: (R) = Random failure, (M) = Malicious attack

**Mitigation Strategy:**

.. code-block:: python

   # Multi-sensor fusion (resilient to single sensor attack/failure)
   def lane_keeping_control():
       camera_lane = get_camera_lane_position()
       radar_lane = get_radar_lane_boundaries()
       map_lane = get_hd_map_lane()
       
       # Check for camera attack/failure
       if abs(camera_lane - radar_lane) > THRESHOLD:
           # Camera and radar disagree (potential attack or failure)
           if abs(radar_lane - map_lane) < THRESHOLD:
               # Radar and map agree, trust them
               return radar_lane  # Fallback to radar
           else:
               # Multiple sensor disagreement
               return SAFE_STATE  # Pull over, alert driver
       
       # Normal operation (sensors agree)
       return camera_lane

════════════════════════════════════════════════════════════════════════════════

📖 **5. CASE STUDIES**
════════════════════════════════════════════════════════════════════════════════

5.1 Jeep Cherokee Hack (2015)
------------------------------

**Incident:**

.. code-block:: text

   Researchers Charlie Miller and Chris Valasek demonstrated remote
   control of Jeep Cherokee via cellular connection:
   
   Attack Path:
   1. Exploit vulnerability in Uconnect infotainment system
   2. Gain access to CAN bus
   3. Send spoofed CAN messages to steering, braking, transmission
   
   Result:
   - Vehicle remotely controlled (steering, braking)
   - FCA recalled 1.4 million vehicles
   - $105 million cost

**Root Causes (Security-Safety Gaps):**

.. code-block:: text

   ❌ Infotainment system had Internet access (cellular)
   ❌ No network segmentation (infotainment directly on safety-critical CAN bus)
   ❌ No CAN message authentication (any ECU can send any message)
   ❌ No secure software update mechanism (attacker could upload malicious firmware)

**Mitigations (Post-Incident):**

.. code-block:: text

   ✅ Network segmentation (gateway between infotainment and CAN bus)
   ✅ CAN message authentication (MACsec-like protection)
   ✅ Intrusion detection system (IDS) monitors for anomalous CAN traffic
   ✅ Secure OTA updates (signed firmware, rollback protection)

────────────────────────────────────────────────────────────────────────────

**5.2 Triton/TRISIS Malware (2017)**
------------------------------------

**Incident:**

.. code-block:: text

   Malware targeted Schneider Electric Triconex Safety Instrumented System (SIS)
   at petrochemical plant in Saudi Arabia:
   
   Attack Path:
   1. Initial access via phishing (enterprise network)
   2. Lateral movement to engineering workstation
   3. Upload malicious ladder logic to safety PLC
   4. Malware reprograms safety shutdown logic
   
   Goal: Disable safety system, cause physical explosion
   
   Result:
   - Plant shutdown (attack detected before physical damage)
   - First-known malware targeting SIS (IEC 61508 SIL 3 system)

**Root Causes:**

.. code-block:: text

   ❌ Insufficient network segmentation (enterprise → safety network)
   ❌ No unidirectional gateway protecting SIS
   ❌ Engineering workstation had access to both IT and OT networks
   ❌ Weak authentication on safety PLC (default passwords)

**Mitigations:**

.. code-block:: text

   ✅ Air-gap or unidirectional gateway for SIS network (IEC 62443 SL-4)
   ✅ Dual-approval for safety logic changes (two engineers required)
   ✅ Offline verification of safety logic (compare against golden image)
   ✅ Physical key switch for programming mode (prevent remote tampering)

────────────────────────────────────────────────────────────────────────────

**5.3 Medical Device: Insulin Pump Vulnerability**
--------------------------------------------------

**Incident:**

.. code-block:: text

   Researchers demonstrated wireless attack on Medtronic insulin pumps:
   
   Attack Vector:
   - Unencrypted RF communication (proprietary 915 MHz protocol)
   - No authentication (any device can send commands)
   
   Exploit:
   - Replay attack (capture legitimate command, replay later)
   - Command injection (send bolus command, overdose patient)
   
   Impact:
   - Potential patient harm (hypoglycemia or hyperglycemia)
   - FDA recall and security advisory

**Mitigations (IEC 81001-5-1: Health software cybersecurity):**

.. code-block:: text

   ✅ Encrypted communication (AES-128 for RF link)
   ✅ Device pairing (pump only accepts commands from paired controller)
   ✅ Command authentication (HMAC prevents replay attacks)
   ✅ Dosage limits (hard-coded maximum bolus, cannot be remotely changed)
   ✅ Local override (manual button on pump as backup)

═══════════════════════════════════════════════════════════════════════════════

📖 **6. SECURITY CONTROLS AS SAFETY BARRIERS**
═══════════════════════════════════════════════════════════════════════════════

6.1 Security in Safety Cases
-----------------------------

**Traditional Safety Argument:**

.. code-block:: text

   Claim: Brake-by-wire system is acceptably safe
   
   Evidence:
   - FMEA shows residual risk < 10^-9 /hour
   - Dual ECU redundancy (1oo2)
   - Plausibility checks detect sensor faults
   - Mechanical backup brake system

**Extended Safety Argument (with Security):**

.. code-block:: text

   Claim: Brake-by-wire system is acceptably safe against random
          failures AND malicious attacks
   
   Sub-claim 1 (Random Failures): Same as traditional argument
   
   Sub-claim 2 (Malicious Attacks):
   Evidence:
   - TARA (Threat Analysis) shows attack feasibility is LOW
   - CAN message authentication prevents spoofing
   - Secure boot prevents malicious firmware
   - Intrusion detection system (IDS) alerts on anomalous traffic
   - Incident response plan (patch deployment within 48 hours)

**Dependency:** Safety argument depends on security controls being effective.

────────────────────────────────────────────────────────────────────────────

**6.2 Secure Boot (Example)**
-----------------------------

**Purpose:** Ensure only authentic firmware runs on safety-critical ECU

.. code-block:: python

   # Simplified secure boot process
   import hashlib
   from cryptography.hazmat.primitives import hashes
   from cryptography.hazmat.primitives.asymmetric import padding, rsa
   
   def verify_firmware_signature(firmware_binary, signature, public_key):
       """
       Verify firmware was signed by OEM (prevents malicious firmware)
       """
       try:
           # Compute hash of firmware
           firmware_hash = hashlib.sha256(firmware_binary).digest()
           
           # Verify signature using public key
           public_key.verify(
               signature,
               firmware_hash,
               padding.PSS(
                   mgf=padding.MGF1(hashes.SHA256()),
                   salt_length=padding.PSS.MAX_LENGTH
               ),
               hashes.SHA256()
           )
           return True  # Signature valid
       except Exception as e:
           return False  # Signature invalid (reject firmware)
   
   def secure_boot():
       """
       Boot process for safety-critical ECU
       """
       # Read firmware from flash
       firmware = read_flash_memory()
       signature = read_signature()
       
       # Public key stored in hardware (tamper-resistant)
       oem_public_key = get_hardware_stored_key()
       
       # Verify signature
       if not verify_firmware_signature(firmware, signature, oem_public_key):
           # Firmware not signed by OEM (potential malware)
           enter_safe_mode()  # Refuse to boot
           return
       
       # Signature valid, boot firmware
       execute_firmware(firmware)

**Safety Benefit:** Prevents attacker from uploading malicious firmware that disables safety features.

────────────────────────────────────────────────────────────────────────────

**6.3 Intrusion Detection System (IDS)**
----------------------------------------

**Purpose:** Detect anomalous CAN bus traffic (potential attack)

.. code-block:: python

   # CAN bus IDS for automotive
   class CANIntrusionDetection:
       def __init__(self):
           # Learn normal traffic patterns
           self.allowed_ids = {0x100, 0x200, 0x300}  # Whitelist of CAN IDs
           self.max_rate = {0x100: 100, 0x200: 50, 0x300: 10}  # Max msg/sec
           self.message_count = {id: 0 for id in self.allowed_ids}
       
       def check_message(self, can_id, timestamp):
           """
           Detect anomalous CAN messages
           """
           # Check 1: Unknown CAN ID (potential injection)
           if can_id not in self.allowed_ids:
               self.raise_alert(f"Unknown CAN ID: 0x{can_id:03X}")
               return REJECT
           
           # Check 2: Message rate too high (potential DoS)
           self.message_count[can_id] += 1
           if self.message_count[can_id] > self.max_rate[can_id]:
               self.raise_alert(f"CAN ID 0x{can_id:03X} rate limit exceeded")
               return REJECT
           
           return ACCEPT
       
       def raise_alert(self, message):
           """
           Alert driver and log security event
           """
           display_warning_light()  # Dashboard indicator
           log_security_event(message, timestamp)
           # Optional: Enter limp-home mode (reduced functionality)

**Safety Benefit:** Early detection of attacks allows system to enter safe state before physical harm occurs.

═══════════════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
═══════════════════════════════════════════════════════════════════════════════

**Q1:** Why is cybersecurity essential for safety in cyber-physical systems? Give an automotive example.

**A1:**

**Reason:** Traditional safety assumes failures are random and independent. In CPS, attackers can cause intentional, coordinated failures that bypass safety mechanisms.

**Automotive Example: Brake-by-Wire System**

.. code-block:: text

   Safety Mechanism: Dual ECU redundancy (1oo2)
   - If ECU #1 fails randomly, ECU #2 continues operation
   - Assumes failures are independent
   
   Cyber Attack Scenario:
   - Both ECUs run same firmware
   - Attacker exploits vulnerability in firmware
   - Both ECUs compromised simultaneously
   - Redundancy provides NO protection (common cause failure)
   
   Security Mitigation Required:
   ✅ Secure boot (prevent malicious firmware)
   ✅ CAN message authentication (prevent command injection)
   ✅ Diverse redundancy (different hardware/software stacks)
   
   Conclusion: Safety mechanisms alone are insufficient in connected systems.
               Security is a prerequisite for safety.

────────────────────────────────────────────────────────────────────────────

**Q2:** Explain the integration of ISO 26262 (safety) and ISO/SAE 21434 (cybersecurity) for automotive.

**A2:**

**ISO 26262 (Safety):**
- Hazard Analysis and Risk Assessment (HARA)
- ASIL rating (A, B, C, D) based on Severity, Exposure, Controllability
- Safety requirements (redundancy, diagnostics)

**ISO/SAE 21434 (Cybersecurity):**
- Threat Analysis and Risk Assessment (TARA)
- CAL rating (1, 2, 3, 4) based on Impact, Attack Feasibility
- Security requirements (authentication, encryption)

**Integration Process:**

.. code-block:: text

   Step 1: Conduct HARA
   Example: "Unintended acceleration" → ASIL D (severe, high exposure)
   
   Step 2: Conduct TARA on safety functions
   Example: "Attacker spoofs accelerator pedal sensor" → CAL 4
   
   Step 3: Combined requirements
   Safety (ASIL D):
   - Triple modular redundancy (2oo3 voting)
   - Plausibility checks (cross-sensor validation)
   
   Security (CAL 4):
   - Authenticated CAN messages (HMAC)
   - Secure sensor communication (encrypted link)
   
   Step 4: Unified verification
   - Test random failures (ISO 26262 fault injection)
   - Test cyber attacks (ISO/SAE 21434 penetration testing)
   
   Step 5: Safety case
   Argument: "System safe because random failures AND malicious
             attacks are both mitigated to acceptable level"

────────────────────────────────────────────────────────────────────────────

**Q3:** Describe IEC 62443 security levels (SL) and how they map to IEC 61508 SIL levels.

**A3:**

**IEC 62443 Security Levels:**

.. code-block:: text

   SL-1: Protection against casual violation
         (Attacker: Unskilled, no tools)
   
   SL-2: Protection against intentional violation with simple means
         (Attacker: Skilled, simple tools)
   
   SL-3: Protection against sophisticated means
         (Attacker: Expert, custom tools)
   
   SL-4: Protection against sophisticated means with extended resources
         (Attacker: Nation-state, extensive resources)

**Mapping to IEC 61508 SIL (Recommended):**

+---------------------------+------------------+------------------+
| System Type               | IEC 61508 SIL    | IEC 62443 SL     |
+===========================+==================+==================+
| Safety Instrumented       | SIL 3-4          | SL-3 to SL-4     |
| System (SIS)              | (critical safety)| (high security)  |
+---------------------------+------------------+------------------+
| Process Control           | SIL 1-2          | SL-2 to SL-3     |
|                           | (production)     | (medium security)|
+---------------------------+------------------+------------------+
| Monitoring only           | N/A              | SL-1 to SL-2     |
| (non-safety)              |                  |                  |
+---------------------------+------------------+------------------+

**Rationale:** Higher safety integrity requires higher security (attackers targeting critical systems are more motivated and resourced).

────────────────────────────────────────────────────────────────────────────

**Q4:** What is a unidirectional gateway, and why is it used in industrial safety systems?

**A4:**

**Unidirectional Gateway (Data Diode):**

.. code-block:: text

   Physical device that allows data to flow in only ONE direction
   
   ┌──────────────┐         ┌──────────────┐
   │ SCADA System │ ◄───────│ Safety PLC   │
   │ (monitoring) │  Data   │ (SIL 3/4)    │
   │              │  OUT    │              │
   │              │  only   │              │
   │              │  ╳──────│              │
   │              │ Commands│              │
   │              │ BLOCKED │              │
   └──────────────┘         └──────────────┘
   
   Implementation:
   - Hardware: Fiber optic transmitter (no receiver on SIS side)
   - Software: Protocol converter (replicate data, no reverse path)

**Purpose:**

.. code-block:: text

   ✅ Prevents cyber attacks from SCADA reaching safety PLC
   ✅ Safety PLC can send status data to SCADA for monitoring
   ✅ Attacker who compromises SCADA CANNOT send commands to SIS
   
   Example: Triton/TRISIS malware would be BLOCKED by unidirectional gateway

**IEC 62443 Requirement:** SL-4 systems (like SIS) should use unidirectional gateway to isolate from lower-security networks.

────────────────────────────────────────────────────────────────────────────

**Q5:** How does multi-sensor fusion improve both safety and security in autonomous vehicles?

**A5:**

**Multi-Sensor Fusion:**

.. code-block:: text

   Combine data from multiple independent sensors:
   - Camera (visual lane markings)
   - LIDAR (3D point cloud)
   - Radar (object detection, velocity)
   - GPS + IMU (position, orientation)
   - HD Map (a priori road geometry)

**Safety Benefits (Random Failures):**

.. code-block:: text

   Redundancy: If one sensor fails, others provide fallback
   
   Example: Camera obscured by mud splash
   → Radar and LIDAR still functional
   → Vehicle continues safe operation

**Security Benefits (Malicious Attacks):**

.. code-block:: text

   Attack Resistance: Different sensors require different attack methods
   
   Example 1: Attacker projects fake lane markings (adversarial pattern)
   → Camera fooled, but LIDAR/radar unaffected
   → Cross-sensor validation detects inconsistency
   
   Example 2: GPS spoofing attack (fake position)
   → GPS shows wrong location, but IMU dead reckoning + camera/LIDAR
      visual odometry disagree
   → System detects attack, enters safe mode

**Implementation:**

.. code-block:: python

   def sensor_fusion_with_attack_detection():
       camera_pos = get_camera_position()
       lidar_pos = get_lidar_position()
       gps_pos = get_gps_position()
       map_pos = get_map_matched_position()
       
       # Check for sensor attack or failure
       positions = [camera_pos, lidar_pos, gps_pos, map_pos]
       median_pos = median(positions)
       
       outliers = [p for p in positions if distance(p, median_pos) > THRESHOLD]
       
       if len(outliers) >= 2:
           # Multiple sensors disagree (potential attack or multiple failures)
           return SAFE_STATE  # Pull over, alert driver
       elif len(outliers) == 1:
           # One sensor disagrees (exclude it, use others)
           return median_of_remaining_sensors()
       else:
           # All sensors agree
           return median_pos

**Key Insight:** Diversity of sensor modalities makes system resilient to both random failures AND targeted attacks.

═══════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Fundamentals:**
- [ ] Understand CPS = Computation + Communication + Physical
- [ ] Security attacks can cause physical harm (cyber → safety impact)
- [ ] Common cause failure: Cyber attack affects redundant channels

**Standards Integration:**
- [ ] ISO 26262 (safety) + ISO/SAE 21434 (security) for automotive
- [ ] IEC 61508 (safety) + IEC 62443 (security) for industrial
- [ ] Combined HARA + TARA (unified risk assessment)

**Architecture:**
- [ ] Network segmentation (Purdue model, zones)
- [ ] Unidirectional gateway for SIL 3/4 safety systems
- [ ] Defense in depth (multiple security layers)

**Analysis:**
- [ ] Combined FMEA (random failures + malicious attacks)
- [ ] Attack trees + Fault trees integration
- [ ] Security controls as safety barriers (in safety case)

**Mitigations:**
- [ ] Secure boot (prevent malicious firmware)
- [ ] Message authentication (prevent spoofing)
- [ ] Intrusion detection (early attack detection)
- [ ] Multi-sensor fusion (resilience to sensor attacks)

═══════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
═══════════════════════════════════════════════════════════════════════════════

1️⃣ **Security is a safety prerequisite in CPS** — Cyber attacks cause intentional, coordinated failures that bypass traditional safety mechanisms (redundancy assumes independence)

2️⃣ **Standards convergence (2026 trend)** — Automotive (ISO 26262 + ISO/SAE 21434), Industrial (IEC 61508 + IEC 62443), Medical (IEC 62304 + IEC 81001-5-1) now require BOTH safety AND security certification

3️⃣ **Common cause failure through software** — Single vulnerability affects all redundant channels (e.g., dual ECUs running identical firmware), requires diverse redundancy + security controls

4️⃣ **Defense in depth = network segmentation + access control** — Purdue model for industrial (5 levels), unidirectional gateway for SIL 3/4, prevent lateral movement from IT to OT

5️⃣ **Unified threat modeling** — Combine FMEA (random failures) with threat analysis (malicious attacks), integrate attack trees into fault trees, security controls become safety barriers

6️⃣ **Real incidents prove the risk** — Jeep Cherokee hack (2015), Triton/TRISIS malware (2017), medical device vulnerabilities demonstrate cyber → physical harm is REAL, not theoretical

7️⃣ **Multi-sensor fusion provides resilience** — Different sensor modalities (camera, LIDAR, radar, GPS) require different attack methods, cross-validation detects both failures AND attacks

═══════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **CYBER-PHYSICAL SYSTEMS SAFETY CHEATSHEET COMPLETE**

**Created:** January 15, 2026  
**Coverage:** CPS architecture and threat surface, automotive (ISO 26262 + ISO/SAE 21434 integration), industrial (IEC 61508 + IEC 62443 integration), unified threat modeling (FMEA + attack trees), case studies (Jeep Cherokee, Triton/TRISIS, medical devices), security controls as safety barriers (secure boot, IDS, multi-sensor fusion)

═══════════════════════════════════════════════════════════════════════════════
