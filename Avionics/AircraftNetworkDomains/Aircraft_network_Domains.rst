✈️ **Aircraft Network Domains — Complete Reference**
═══════════════════════════════════════════════════════

**Last Updated:** January 2026  
**Aircraft Focus:** Boeing 787, Airbus A350/A380, 737 MAX  
**Standards:** ARINC 811/664, RTCA DO-326A/ED-202A, DO-178C

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — Quick Mental Model**
──────────────────────────────────

Think of aircraft networks like **concentric security zones**:

::

   ┌─────────────────────────────────────────────┐
   │  🔴 CORE (ACD)                              │
   │  Flight Controls, Engines                   │
   │  ┌───────────────────────────────────────┐ │
   │  │ 🟡 MIDDLE (AISD)                      │ │
   │  │ Crew Tools, Maintenance               │ │
   │  │ ┌───────────────────────────────────┐ │ │
   │  │ │ 🟢 OUTER (PIESD)                  │ │ │
   │  │ │ Passenger Wi-Fi, Movies           │ │ │
   │  │ └───────────────────────────────────┘ │ │
   │  └───────────────────────────────────────┘ │
   └─────────────────────────────────────────────┘
        │              │              │
     NO ACCESS    One-Way Gate    Internet
                   (Data Diode)

**Mnemonic:** **"ACD = Absolutely Critical Domain, AISD = Airline Internal Stuff Domain, PIESD = Passenger Internet Entertainment Domain"**

✅ **3 Domains, 3 Isolation Levels, 3 Security Postures**  
✅ **Zero Trust:** Each domain assumes others are compromised  
✅ **Defense in Depth:** Multiple barriers between zones  
✅ **Data Diodes:** Physical one-way data flow (ACD → AISD, never reverse)

════════════════════════════════════════════════════════════════════

📋 **TABLE OF CONTENTS**
────────────────────────

1. Overview & Architecture
2. Domain 1: Aircraft Control Domain (ACD) 🔴
3. Domain 2: Airline Information Services Domain (AISD) 🟡
4. Domain 3: Passenger Information & Entertainment (PIESD) 🟢
5. Isolation Technologies
6. Security Threat Matrix
7. Certification & Compliance
8. Real-World Incidents
9. Cross-Domain Data Flow
10. Practical Examples
11. Common Pitfalls
12. Quick Reference Card
13. Exam Questions
14. Further Reading

════════════════════════════════════════════════════════════════════

🏢 **1. OVERVIEW & ARCHITECTURE**
──────────────────────────────────

**Why Network Segmentation?**

Modern aircraft (787, A350) have **100+ networked systems**. Without isolation:
- ❌ Passenger laptop malware could reach autopilot
- ❌ IFE bug could crash flight computers
- ❌ Wi-Fi DDoS could disable navigation

**Solution:** **3-Domain Architecture** (originated ~2000s with Boeing 787)

**Historical Context:**

+------------------+--------------------------------+
| Era              | Network Approach               |
+==================+================================+
| **Pre-2000**     | Isolated buses (ARINC 429)     |
| **2000-2010**    | Ethernet adoption (A380, 787)  |
| **2010-2020**    | Domain segregation mandatory   |
| **2020+**        | Zero-trust, AI monitoring      |
+------------------+--------------------------------+

**Regulatory Drivers:**

- **DO-326A/ED-202A** (2014): Airworthiness security process
- **DO-356A/ED-203A** (2018): Security development assurance
- **FAA AC 20-170** (2019): Cybersecurity certification

════════════════════════════════════════════════════════════════════

🔴 **2. AIRCRAFT CONTROL DOMAIN (ACD)**
════════════════════════════════════════

**🏆 Criticality:** MAXIMUM — "This is where the plane flies"  
**🔒 Security:** DAL A/B (Design Assurance Level)  
**⚡ Real-Time:** <1 ms latency for flight control loops  
**🚫 Internet:** NEVER connected (air-gapped)

────────────────────────────────────────────────────────────────────

**What's Inside ACD?**

🛫 **Flight-Critical Systems:**

1. **Flight Control Computers (FCC)**
   - Primary flight control (elevators, ailerons, rudder)
   - Fly-by-wire actuators
   - Envelope protection (stall prevention)

2. **Engine Control (FADEC)**
   - Full Authority Digital Engine Control
   - Thrust management
   - Fuel optimization

3. **Navigation Systems**
   - Air Data Inertial Reference System (ADIRS)
   - Flight Management System (FMS)
   - GPS/IRS integration

4. **Cockpit Displays**
   - Primary Flight Display (PFD)
   - Navigation Display (ND)
   - Engine Indication & Crew Alerting (EICAS)

**Network Topology (Example: Boeing 787):**

::

   ┌──────────────────────────────────────────────┐
   │       AFDX Network (Redundant A + B)         │
   └───────┬──────────────┬───────────────────┬───┘
           │              │                   │
      ┌────▼────┐    ┌────▼────┐        ┌────▼────┐
      │  FCC 1  │    │  FCC 2  │        │  FCC 3  │
      │(Primary)│    │ (Backup)│        │(Monitor)│
      └────┬────┘    └────┬────┘        └────┬────┘
           │              │                   │
           └──────────────┴───────────────────┘
                          │
                   Actuator Control

**Security Architecture:**

🛡️ **Defense Layers:**

1. **Physical Isolation**
   - Separate cables (no shared infrastructure)
   - Locked avionics bays (LOTO procedures)
   - Tamper-evident seals

2. **Network Isolation**
   - AFDX Virtual Links (VL) — guaranteed bandwidth
   - NO IP routing (raw Ethernet frames)
   - MAC address whitelisting

3. **Cryptographic Protection**
   - Code signing (ECDSA-P384)
   - Secure boot (UEFI)
   - Memory encryption (if applicable)

4. **Intrusion Detection**
   - Anomaly detection (packet timing)
   - Behavioral analysis (control law monitoring)
   - Alert to cockpit (EICAS message)

**Threat Model:**

+------------------------------+------------------+--------------------------+
| Threat                       | Likelihood       | Mitigation               |
+==============================+==================+==========================+
| Supply chain backdoor        | Low              | Supplier audits, testing |
| Insider sabotage             | Very Low         | Two-person rule, audits  |
| Physical access (ground)     | Low              | Locks, cameras, logs     |
| Remote exploit               | **Nearly Zero**  | Air gap, no external I/O |
| Software bug (safety impact) | Low              | DO-178C verification     |
+------------------------------+------------------+--------------------------+

**Key Protocols & Standards:**

📡 **Communication:**
- **ARINC 429**: Point-to-point (legacy, 12.5-100 kbps)
- **ARINC 664 (AFDX)**: Ethernet-based, deterministic (100 Mbps)
- **MIL-STD-1553**: Military variant (1 Mbps bus)

📜 **Certification:**
- **DO-178C**: Software development (DAL A = <10⁻⁹ failures/hr)
- **DO-254**: Hardware development
- **DO-326A**: Security process
- **ARP4754A**: System safety assessment

**Memorable Analogy:**

*"ACD is like a submarine's reactor room: sealed, monitored 24/7, no Wi-Fi, and if someone unauthorized gets in, everyone knows immediately."*

**Example Configuration (AFDX):**

.. code-block:: xml

   <VirtualLink>
     <VL_ID>1</VL_ID>
     <Name>FCC_to_Actuator_Roll</Name>
     <BAG>4</BAG>  <!-- 4 ms Bandwidth Allocation Gap -->
     <MaxFrameSize>256</MaxFrameSize>
     <Source>FCC1</Source>
     <Destinations>
       <ES>Actuator_Left_Aileron</ES>
       <ES>Actuator_Right_Aileron</ES>
     </Destinations>
     <Priority>7</Priority>  <!-- Highest (802.1p) -->
     <VLAN>10</VLAN>  <!-- Flight-critical VLAN -->
   </VirtualLink>

────────────────────────────────────────────────────────────────────

**🔑 ACD Keywords (Memorize These!)**

Core Concepts:
✈️ Avionics network, Flight control system, AFDX, ARINC 429/664  
🔐 Data diode, Air gap isolation, Zero-trust model  
⚡ Deterministic network, Fault-tolerant architecture  
🛡️ Intrusion detection system (IDS), Cybersecurity certification (DO-326A)  
🎯 Common Core System (CCS), EICAS, Residual risk minimization  
🏅 Safety Integrity Level (SIL 4 equivalent), DAL A/B

════════════════════════════════════════════════════════════════════

🟡 **3. AIRLINE INFORMATION SERVICES DOMAIN (AISD)**
═════════════════════════════════════════════════════

**🏆 Criticality:** HIGH — "Crew tools and airline operations"  
**🔒 Security:** DAL C/D (Important but not flight-critical)  
**⚡ Real-Time:** <100 ms for most operations  
**🌐 External Access:** Limited (ground links, maintenance ports)

────────────────────────────────────────────────────────────────────

**What's Inside AISD?**

🧑‍✈️ **Crew & Operations Systems:**

1. **Electronic Flight Bag (EFB)**
   - Class 1: Portable (iPad with ForeFlight)
   - Class 2: Mounted tablet
   - Class 3: Installed system
   - Charts, manuals, performance calculations

2. **Maintenance Systems**
   - Central Maintenance Computer (CMC)
   - Aircraft Condition Monitoring System (ACMS)
   - Fault logging and diagnostics

3. **Cabin Management**
   - Lighting control
   - Temperature zones
   - Lavatory status
   - Door/slide monitoring

4. **Operational Data**
   - Flight data recorder (FDR) interface
   - ACARS (Aircraft Communications Addressing and Reporting System)
   - Weight & balance calculations

**Network Topology:**

::

   ┌──────────────────────────────────────────────┐
   │        Airline Secure Network (AISD)         │
   └─┬──────────────┬───────────────────┬────────┬┘
     │              │                   │        │
   ┌─▼──────┐  ┌────▼────┐       ┌─────▼────┐  │
   │  EFB   │  │   CMC   │       │  Cabin   │  │
   │(Class 3│  │(Maint.) │       │Management│  │
   └────────┘  └─────────┘       └──────────┘  │
                    │                            │
              ┌─────▼─────┐              ┌──────▼──────┐
              │ Data Diode│◄─────────────│  ACD Data   │
              │(One-Way)  │  (Read-only) │  (Sensors)  │
              └───────────┘              └─────────────┘

**Interface to ACD (One-Way Only):**

📤 **Allowed (ACD → AISD):**
- Engine parameters (for EFB performance calcs)
- Fault codes (for maintenance diagnostics)
- Flight phase (for cabin automation)

🚫 **Forbidden (AISD → ACD):**
- NO commands to flight systems
- NO software uploads from AISD to ACD
- NO bidirectional communication

**Security Architecture:**

🛡️ **Defense Layers:**

1. **Firewall Segmentation**
   - Deep packet inspection (DPI)
   - Stateful filtering
   - Application-layer gateway (ALG)

2. **VLAN Isolation**
   - VLAN 100-200: Crew systems
   - VLAN 500: Maintenance (special access)
   - 802.1X authentication

3. **Secure Gateway**
   - Between AISD ↔ Ground Networks
   - VPN tunnels (IPsec)
   - Rate limiting (DDoS protection)

4. **Access Control**
   - Role-Based Access Control (RBAC)
   - Multi-factor authentication (for maintenance)
   - Session timeout (15 min idle)

**Threat Model:**

+------------------------------+------------------+--------------------------+
| Threat                       | Likelihood       | Mitigation               |
+==============================+==================+==========================+
| Malware from maintenance USB | Medium           | USB whitelisting, scan   |
| Data exfiltration (leaks)    | Medium           | DLP (Data Loss Prevent.) |
| Unauthorized EFB access      | Low              | PIN/biometric lock       |
| Ground link MITM attack      | Low              | Encrypted channels (TLS) |
| Cross-domain privilege esc.  | Very Low         | Principle of least priv. |
+------------------------------+------------------+--------------------------+

**Memorable Analogy:**

*"AISD is like a hospital's internal network: doctors (pilots) have tablets, maintenance logs go to a separate system, and while it's not the ICU (ACD), you still can't let random people plug in USB drives."*

**Example Access Control List (ACL):**

.. code-block:: text

   # Allow EFB to read engine data from ACD (via data diode)
   permit ip vlan100 to vlan10 [read-only, logged]
   
   # Deny any write attempts
   deny ip vlan100 to vlan10 [any write, alert admin]
   
   # Allow maintenance VLAN to upload software to AISD (not ACD!)
   permit ip vlan500 to vlan200 [authenticated, MFA required]
   
   # Block all other cross-domain traffic
   deny ip any to vlan10

────────────────────────────────────────────────────────────────────

**🔑 AISD Keywords (Memorize These!)**

Core Concepts:
🧑‍✈️ Electronic Flight Bag (EFB), Central Maintenance Computer (CMC)  
🔧 Maintenance data link, ARINC 811, Firewall segmentation  
🌐 Virtual LAN (VLAN), Secure gateway, Software loading (part 25)  
🔐 Data integrity check, Access control list (ACL), Vulnerability assessment  
📋 Incident response plan, Operational risk, Redundancy protocol

════════════════════════════════════════════════════════════════════

🟢 **4. PASSENGER INFORMATION & ENTERTAINMENT (PIESD)**
════════════════════════════════════════════════════════

**🏆 Criticality:** LOW — "Passenger comfort, not flight safety"  
**🔒 Security:** DAL E or No DAL (non-certified)  
**⚡ Real-Time:** <1 second acceptable (video buffering OK)  
**🌐 Internet:** YES (via satellite, air-to-ground)

────────────────────────────────────────────────────────────────────

**What's Inside PIESD?**

🎬 **Passenger-Facing Systems:**

1. **In-Flight Entertainment (IFE)**
   - Seatback screens (movies, TV, games)
   - Personal device streaming
   - Moving map (flight path display)
   - Sky Mall shopping

2. **Passenger Wi-Fi**
   - Satellite connectivity (Inmarsat, Viasat, Starlink)
   - Air-to-ground (Gogo, regional coverage)
   - Payment gateway integration
   - Bandwidth throttling per user

3. **Cabin Services**
   - Call attendant button
   - Seat controls (recline, lights)
   - USB charging ports
   - Passenger announcements (pre-recorded)

4. **Live TV / Connectivity**
   - Live news feeds
   - Sports scores
   - Weather radar (passenger view)

**Network Topology:**

::

   ┌──────────────────────────────────────────────┐
   │     Passenger Network (PIESD) — Internet     │
   └─┬──────────────┬───────────────────┬────────┬┘
     │              │                   │        │
   ┌─▼──────┐  ┌────▼────┐       ┌─────▼────┐  │
   │IFE Head│  │ Wi-Fi   │       │  Cabin   │  │
   │  End   │  │  AP     │       │  Crew    │  │
   │ Server │  │(Passenger│      │  Panel   │  │
   └────┬───┘  └────┬────┘       └──────────┘  │
        │           │                            │
   ┌────▼───────────▼─────┐              ┌──────▼──────┐
   │   Satellite Modem    │              │  Firewall   │
   │   (Inmarsat/Viasat)  │              │ (Block All  │
   └──────────────────────┘              │  to ACD)    │
                                         └─────────────┘

**Interface to Other Domains:**

🚫 **ZERO Direct Connection to ACD/AISD**

✅ **Limited Data (Via Firewall):**
- **Flight info** for moving map (read-only, sanitized):
  - Position, altitude, speed
  - Destination, ETA
  - Origin, route
- **No sensitive data** (fuel, engine params, flight plan details)

**Security Architecture:**

🛡️ **Defense Layers:**

1. **Network Segregation**
   - Physically separate switches
   - NO cable sharing with ACD/AISD
   - Dedicated power (to prevent reboot attacks on ACD)

2. **Firewall (Stateful)**
   - Block all outbound from PIESD to ACD/AISD
   - Allow only sanitized flight data (GPS → moving map)
   - Rate limiting (1 Mbps per passenger device)

3. **Malware Protection**
   - Antivirus on IFE servers
   - USB port lockdown (no passenger USB writes)
   - Content scanning (movies, apps)

4. **Passenger Device Isolation**
   - Each device in separate VLAN (client isolation)
   - No device-to-device communication
   - Captive portal (terms of service, payment)

**Threat Model:**

+------------------------------+------------------+--------------------------+
| Threat                       | Likelihood       | Mitigation               |
+==============================+==================+==========================+
| DDoS attack (Wi-Fi flood)    | High             | Rate limiting, blacklist |
| Ransomware on IFE server     | Medium           | Antivirus, backup/restore|
| Passenger device malware     | High             | Isolated VLANs, firewall |
| Content piracy (illegal)     | Medium           | DRM, legal compliance    |
| Cross-domain exploit         | **Very Low**     | No physical connection   |
+------------------------------+------------------+--------------------------+

**Real-World Incident Example:**

🔥 **2015: Security Researcher Claims (Debunked)**
- Researcher claimed to "hack" 737 via IFE
- Investigation: NO evidence of ACD access
- Reality: IFE is isolated, researcher overstated claims
- Outcome: Reinforced importance of public education on isolation

**Memorable Analogy:**

*"PIESD is like a hotel's guest Wi-Fi: anyone can connect, it might get hacked, but there's a massive firewall between it and the hotel's security cameras / door locks. If the Wi-Fi goes down, the hotel still operates."*

**Example Wi-Fi Captive Portal Flow:**

.. code-block:: text

   Passenger Device
         │
         ├─► Connect to "AirlineWiFi" SSID
         │
         ├─► Redirect to captive portal (192.168.1.1)
         │       │
         │       ├─► Display Terms of Service
         │       ├─► Payment options ($5/hr, $15/flight)
         │       └─► Create session token (SHA-256 hash)
         │
         ├─► Assign VLAN (e.g., VLAN 2000 + seat number)
         │
         ├─► Apply bandwidth limit (1 Mbps down, 256 Kbps up)
         │
         └─► Allow internet access via satellite
                 │
                 └─► Monitor for abuse (DDoS, illegal content)

────────────────────────────────────────────────────────────────────

**🔑 PIESD Keywords (Memorize These!)**

Core Concepts:
🎬 In-Flight Entertainment (IFE), Passenger Wi-Fi, Onboard connectivity  
🌐 Ethernet-based IFE, Network segregation, Content management system  
🛡️ Malware protection, Encryption (WPA3 for Wi-Fi)  
📱 Passenger Owned Device (POD) policy, Cyber threat monitoring  
🔒 Privacy compliance (GDPR-like), Service Level Agreement (SLA)  
🎯 Non-essential system, Graceful degradation

════════════════════════════════════════════════════════════════════

🔧 **5. ISOLATION TECHNOLOGIES**
═════════════════════════════════

**How Domains Stay Separate**

+------------------------+------------------+---------------------------+
| Technology             | Use Case         | How It Works              |
+========================+==================+===========================+
| **Data Diode**         | ACD → AISD       | One-way optical/physical  |
|                        |                  | (literally cut RX wire)   |
+------------------------+------------------+---------------------------+
| **Air Gap**            | ACD ↔ PIESD      | NO physical connection    |
|                        |                  | (separate cables/switches)|
+------------------------+------------------+---------------------------+
| **Firewall**           | AISD ↔ PIESD     | Stateful packet filter    |
|                        |                  | (blocks unauthorized)     |
+------------------------+------------------+---------------------------+
| **VLAN (802.1Q)**      | Within AISD      | Logical segmentation      |
|                        |                  | (single switch, isolated) |
+------------------------+------------------+---------------------------+
| **VPN (IPsec/TLS)**    | Ground ↔ AISD    | Encrypted tunnel          |
|                        |                  | (over satellite)          |
+------------------------+------------------+---------------------------+

**Data Diode Deep Dive:**

.. code-block:: text

   ACD                           AISD
   ┌───────┐                     ┌───────┐
   │ Sensor│──┐                  │  EFB  │
   │ Data  │  │                  │Display│
   └───────┘  │                  └───────┘
              │  One-Way Only       ▲
              ▼                     │
         ┌─────────────┐            │
         │ Data Diode  │────────────┘
         │  (Optical)  │
         │  TX ──►  RX │  (No reverse path exists!)
         │  RX = CUT   │
         └─────────────┘

**Physical Implementation:**
- Optical transmitter (LED/laser) on ACD side
- Optical receiver (photodiode) on AISD side
- NO electrical connection (prevents signal backflow)
- Certified to EAL7+ (highest security)

════════════════════════════════════════════════════════════════════

🚨 **6. SECURITY THREAT MATRIX**
═════════════════════════════════

**Comprehensive Risk Assessment**

+-------------------+----------+----------+----------+-------------+
| Threat Scenario   | ACD      | AISD     | PIESD    | Mitigation  |
+===================+==========+==========+==========+=============+
| Remote Exploit    | CRITICAL | HIGH     | MEDIUM   | Air gap,    |
| (Internet-based)  | (N/A)    | (Ground) | (Common) | firewall    |
+-------------------+----------+----------+----------+-------------+
| Malware (USB)     | HIGH     | HIGH     | MEDIUM   | Whitelist,  |
|                   | (Maint.) | (Crew)   | (None)   | scanning    |
+-------------------+----------+----------+----------+-------------+
| Insider Threat    | HIGH     | MEDIUM   | LOW      | 2-person    |
|                   | (Sabotage| (Data    | (Annoy)  | rule, logs  |
|                   | )        | leak)    |          |             |
+-------------------+----------+----------+----------+-------------+
| Supply Chain      | CRITICAL | HIGH     | MEDIUM   | Vendor      |
| (Backdoor HW/SW)  | (Catast.)| (Ops     | (Nuisan.)| audits      |
|                   |          | impact)  |          |             |
+-------------------+----------+----------+----------+-------------+
| Physical Access   | HIGH     | MEDIUM   | LOW      | Locks,      |
| (Ground tampering)| (Flight  | (Maint.  | (Public  | cameras     |
|                   | impact)  | delay)   | access)  |             |
+-------------------+----------+----------+----------+-------------+
| Software Bug      | CRITICAL | HIGH     | MEDIUM   | DO-178C,    |
| (Unintentional)   | (Crash)  | (Ops     | (Reboot) | testing     |
|                   |          | impact)  |          |             |
+-------------------+----------+----------+----------+-------------+

**Attack Tree Example: "Hijack Flight Controls"**

::

   [Goal: Unauthorized Control of Flight Surfaces]
            │
       ┌────┴────┐
       │         │
   [Via ACD] [Via Cross-Domain Exploit]
       │         │
   ┌───┴───┐ ┌──┴───────────────────┐
   │       │ │                      │
 Physical Supply  [PIESD→AISD→ACD]  [Ground→AISD→ACD]
 Access   Chain       │                    │
 (LOTO)  (Audits)  ┌──┴──────┐      ┌─────┴──────┐
                   │         │      │            │
                Firewall  Data    VPN         USB
                Bypass    Diode   Exploit     Malware
                (Blocked) (One-   (TLS        (Scanned)
                          Way!)   Cert)

**Conclusion:** All paths BLOCKED except insider with physical access (mitigated by 2-person rule + cameras).

════════════════════════════════════════════════════════════════════

📜 **7. CERTIFICATION & COMPLIANCE**
════════════════════════════════════

**Regulatory Landscape**

+-------------------+--------------------------------+---------------+
| Standard          | Purpose                        | Applies To    |
+===================+================================+===============+
| **DO-178C**       | Software development (safety)  | ACD, AISD     |
| (DAL A/B/C/D/E)   | Verification & validation      | (by DAL)      |
+-------------------+--------------------------------+---------------+
| **DO-254**        | Hardware development           | ACD           |
|                   | (FPGA, ASIC certification)     |               |
+-------------------+--------------------------------+---------------+
| **DO-326A**       | Airworthiness security process | ALL domains   |
| (ED-202A)         | Risk assessment, STRIDE        |               |
+-------------------+--------------------------------+---------------+
| **DO-356A**       | Security development assurance | ACD, AISD     |
| (ED-203A)         | (like DO-178C but for security)|               |
+-------------------+--------------------------------+---------------+
| **ARINC 811**     | Network security guidelines    | AISD, PIESD   |
|                   | (commercial aviation)          |               |
+-------------------+--------------------------------+---------------+
| **ARP4754A**      | System safety assessment       | ACD           |
|                   | (FHA, PSSA, SSA)               |               |
+-------------------+--------------------------------+---------------+
| **FAA AC 20-170** | Certification memo (security)  | ALL (USA)     |
+-------------------+--------------------------------+---------------+
| **EASA CS-25**    | Certification spec (Europe)    | ALL (EU)      |
+-------------------+--------------------------------+---------------+

**Design Assurance Levels (DAL):**

+-------+------------------------+--------------------+----------+
| DAL   | Failure Condition      | Probability Req.   | Domain   |
+=======+========================+====================+==========+
| **A** | Catastrophic           | <10⁻⁹ per FH       | ACD      |
|       | (loss of aircraft)     | (Extremely remote) | (core)   |
+-------+------------------------+--------------------+----------+
| **B** | Hazardous              | <10⁻⁷ per FH       | ACD      |
|       | (serious injury)       | (Remote)           | (secondary |
+-------+------------------------+--------------------+----------+
| **C** | Major                  | <10⁻⁵ per FH       | AISD     |
|       | (significant reduction)| (Probable)

+-------+------------------------+--------------------+----------+
| **D** | Minor                  | <10⁻³ per FH       | AISD     |
|       | (inconvenience)        | (Probable)         | (secondary |
+-------+------------------------+--------------------+----------+
| **E** | No Safety Effect       | No requirement     | PIESD    |
|       | (nuisance)             | (Frequent OK)      |          |
+-------+------------------------+--------------------+----------+

FH = Flight Hour

════════════════════════════════════════════════════════════════════

🔥 **8. REAL-WORLD INCIDENTS**
═══════════════════════════════

**Case Studies (Lessons Learned)**

📅 **2008: Boeing 787 Development**
- **Issue:** Initial design had shared network between domains
- **Discovery:** FAA review flagged insufficient isolation
- **Fix:** Redesigned with physical separation (data diodes)
- **Lesson:** "Air gap everything flight-critical"

📅 **2015: "Researcher Hacks 737 via IFE" (Debunked)**
- **Claim:** Chris Roberts said he accessed engine controls via seat IFE
- **Investigation:** FBI found no evidence, IFE completely isolated
- **Reality:** Researcher misunderstood architecture or exaggerated
- **Lesson:** "Security through publicity ≠ actual breach"

📅 **2018: Wi-Fi Vulnerability on Airbus A350**
- **Issue:** Wi-Fi system had outdated firmware (WPA2 KRACK vuln)
- **Impact:** Passenger data potentially interceptable
- **Isolation:** NO impact on flight systems (PIESD isolated)
- **Fix:** Firmware update via ground maintenance
- **Lesson:** "PIESD can fail without safety impact"

📅 **2020: Supply Chain Trojan (Hypothetical Scenario)**
- **Scenario:** Malicious chip in avionics component
- **Detection:** Anomaly monitoring caught unexpected network traffic
- **Response:** Component quarantined, traced to supplier
- **Mitigation:** Enhanced supplier audits, hardware verification
- **Lesson:** "Trust but verify, even certified suppliers"

════════════════════════════════════════════════════════════════════

🔄 **9. CROSS-DOMAIN DATA FLOW**
═════════════════════════════════

**Allowed Data Paths (Simplified)**

.. code-block:: text

   ┌──────────────────────────────────────────────┐
   │                                              │
   │  ████████████  ACD (Flight Systems)          │
   │  █ SEALED █                                  │
   │  ████████████                                │
   │       │                                      │
   │       │ (One-Way Data Diode)                 │
   │       ▼                                      │
   │  ┌───────────┐                               │
   │  │   AISD    │ (Crew, Maintenance)           │
   │  │           │◄──────────┐                   │
   │  └─────┬─────┘           │                   │
   │        │              (Firewall)             │
   │        │ (Sanitized      │                   │
   │        │  GPS data)      │                   │
   │        ▼                 │                   │
   │  ┌───────────┐           │                   │
   │  │  PIESD    │───────────┘                   │
   │  │ (Passengers) Internet Access              │
   │  └───────────┘                               │
   │                                              │
   └──────────────────────────────────────────────┘

**Data Flow Matrix:**

+--------+-------+-------+-------+
| From ↓ | ACD   | AISD  | PIESD |
| To →   |       |       |       |
+========+=======+=======+=======+
| **ACD**| ✅    | ❌    | ❌    |
|        | (Self)| NEVER | NEVER |
+--------+-------+-------+-------+
| **AISD**| ✅   | ✅    | ❌    |
|        | (One- | (Self)| NO    |
|        | way)  |       |       |
+--------+-------+-------+-------+
| **PIESD**| ⚠️  | ⚠️   | ✅    |
|        | (Sani-| (GPS  | (Self)|
|        | tized)| only) |       |
+--------+-------+-------+-------+

**Example: Moving Map Data Flow**

.. code-block:: text

   Step 1: ACD GPS sensor reads position
           ├─► Latitude: 37.7749° N
           ├─► Longitude: -122.4194° W
           └─► Altitude: 35,000 ft
   
   Step 2: Data passes through Data Diode to AISD
           (No return path possible)
   
   Step 3: AISD Sanitization Filter removes:
           ❌ Precise GPS (<1 meter accuracy)
           ❌ Ground speed vectors
           ❌ Flight plan waypoints
           ✅ Keeps: rounded position (±0.1°), altitude
   
   Step 4: Sanitized data sent to PIESD via Firewall
           ├─► Filtered position: 37.8° N, -122.4° W
           └─► Altitude: 35,000 ft (for moving map icon)
   
   Step 5: IFE server renders moving map
           (Passenger sees approximate location on screen)

════════════════════════════════════════════════════════════════════

💻 **10. PRACTICAL EXAMPLES**
══════════════════════════════

**Example 1: Firewall Rule Set (AISD ↔ PIESD)**

.. code-block:: bash

   # Firewall between AISD and PIESD
   
   # DENY all by default
   iptables -P FORWARD DROP
   
   # ALLOW sanitized GPS data (AISD → PIESD)
   iptables -A FORWARD -s 10.20.0.0/16 -d 10.30.0.0/16 \
     -p udp --dport 5000 -m comment --comment "GPS-to-IFE" -j ACCEPT
   
   # DENY all PIESD → AISD attempts
   iptables -A FORWARD -s 10.30.0.0/16 -d 10.20.0.0/16 -j REJECT
   
   # LOG all rejected traffic
   iptables -A FORWARD -j LOG --log-prefix "CROSS-DOMAIN-REJECT: "

**Example 2: Data Diode Configuration (ACD → AISD)**

.. code-block:: python

   # Conceptual Python for Data Diode TX (ACD side)
   
   import serial
   import json
   
   # One-way serial link (TX only, RX wire physically cut)
   tx_port = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)
   
   while True:
       # Read engine parameters from ACD
       engine_data = {
           'N1': read_sensor('engine_n1'),       # RPM
           'EGT': read_sensor('exhaust_temp'),   # °C
           'fuel_flow': read_sensor('fuel_rate') # lbs/hr
       }
       
       # Serialize and transmit (one-way only!)
       tx_port.write(json.dumps(engine_data).encode('utf-8'))
       tx_port.write(b'\n')
       
       time.sleep(0.1)  # 10 Hz update rate
   
   # Note: There is NO receive function (physically impossible)

**Example 3: Passenger Wi-Fi Isolation (PIESD)**

.. code-block:: text

   # Network switch config (802.1X with client isolation)
   
   interface GigabitEthernet0/1
     description "Passenger Wi-Fi Access Point"
     switchport mode access
     switchport access vlan 2000
     spanning-tree portfast
     spanning-tree bpduguard enable
     # Client isolation: prevent device-to-device comms
     protected
   
   vlan 2000
     name "Passenger_Devices"
     # Each passenger gets a /32 subnet (isolated)
   
   # Firewall rule: Block VLAN 2000 from reaching ACD/AISD
   access-list 100 deny ip 10.200.0.0 0.0.255.255 10.10.0.0 0.0.255.255
   access-list 100 deny ip 10.200.0.0 0.0.255.255 10.20.0.0 0.0.255.255
   access-list 100 permit ip 10.200.0.0 0.0.255.255 any

════════════════════════════════════════════════════════════════════

⚠️ **11. COMMON PITFALLS**
═══════════════════════════

❌ **Pitfall 1: "It's Just Wi-Fi, Who Cares?"**
   - **Problem:** Treating PIESD as low-priority
   - **Reality:** Passenger data breaches = PR nightmare, lawsuits
   - **Solution:** Apply basic cybersecurity (encryption, logging)

❌ **Pitfall 2: Shared Infrastructure to Save Costs**
   - **Problem:** Using same switches/cables for multiple domains
   - **Risk:** Single hardware failure could cascade
   - **Solution:** Physical separation, even if more expensive

❌ **Pitfall 3: Maintenance USB Drives**
   - **Problem:** Technician brings infected USB to upload software
   - **Attack Vector:** Malware jumps from USB → AISD → (attempt) ACD
   - **Solution:** USB whitelisting, scan all media, air-gapped updates

❌ **Pitfall 4: "We Passed Certification, We're Done"**
   - **Problem:** Security is not a one-time event
   - **Reality:** New vulnerabilities discovered daily (0-days)
   - **Solution:** Continuous monitoring, patch management, threat intel

❌ **Pitfall 5: Ignoring Supply Chain**
   - **Problem:** Trusting all certified suppliers blindly
   - **Example:** Malicious chip in avionics hardware
   - **Solution:** Supplier audits, hardware verification, diversity

════════════════════════════════════════════════════════════════════

📇 **12. QUICK REFERENCE CARD**
════════════════════════════════

**Domain Summary Table**

+----------+------------+----------+-----------+-------------+
| Domain   | Criticality| Internet?| Isolation | Key Systems |
+==========+============+==========+===========+=============+
| **ACD**  | MAXIMUM    | ❌ NEVER | Air gap   | FCC, FADEC  |
| 🔴       | DAL A/B    |          | Data diode| ADIRS, EICAS|
+----------+------------+----------+-----------+-------------+
| **AISD** | HIGH       | ⚠️ Ground| Firewall  | EFB, CMC    |
| 🟡       | DAL C/D    | link only| VLAN      | ACMS, Cabin |
+----------+------------+----------+-----------+-------------+
| **PIESD**| LOW        | ✅ YES   | Physical  | IFE, Wi-Fi  |
| 🟢       | DAL E/None | (sat)    | separation| Moving map  |
+----------+------------+----------+-----------+-------------+

**Memorization Mnemonics:**

🎯 **"Red-Yellow-Green = Stop-Caution-Go"**
   - 🔴 ACD: STOP all external access
   - 🟡 AISD: CAUTION, controlled access
   - 🟢 PIESD: GO ahead, it's public

🎯 **"CIA vs DAL"**
   - ACD: **Integrity** > Availability (must be correct)
   - AISD: **Availability** > Confidentiality (must be up)
   - PIESD: **Availability** >> Integrity (can reboot)

🎯 **"Onion Layers"**
   - ACD = core (sealed)
   - AISD = middle (filtered)
   - PIESD = outer (exposed)

════════════════════════════════════════════════════════════════════

📝 **13. EXAM QUESTIONS**
══════════════════════════

**Q1:** Why is a data diode used between ACD and AISD instead of a firewall?

**A1:** A firewall is software-based and can be misconfigured or exploited. A data diode is **physically one-way** (optical transmitter on ACD, receiver on AISD, no return path exists), making it impossible for data to flow backward even with perfect exploit. This guarantees ACD cannot be compromised from AISD.

────────────────────────────────────────────────────────────────────

**Q2:** Passenger Wi-Fi goes down mid-flight. What domains are affected?

**A2:** Only **PIESD**. ACD (flight controls) and AISD (crew tools) are completely isolated and continue operating normally. Passengers experience entertainment outage but flight safety is unaffected.

────────────────────────────────────────────────────────────────────

**Q3:** What is "sanitized GPS data" for the IFE moving map?

**A3:** Precise GPS coordinates from ACD are **filtered** before reaching PIESD:
- Original: 37.774929° N (1-meter accuracy)
- Sanitized: 37.8° N (rounded to ±0.1°, ~10 km accuracy)
- Rationale: Prevents passengers from seeing exact position (privacy, security)

────────────────────────────────────────────────────────────────────

**Q4:** A maintenance technician plugs in a USB drive to upload software. Which domain(s) can they access?

**A4:** Only **AISD** (maintenance port). The USB is scanned for malware, and software is cryptographically verified before installation. They **cannot** access ACD directly (requires special authorization, two-person rule, and physical access to locked avionics bay).

────────────────────────────────────────────────────────────────────

**Q5:** Explain the difference between DAL A (ACD) and DAL E (PIESD) in practical terms.

**A5:**  
- **DAL A (ACD):** Catastrophic failure probability <10⁻⁹/FH. Example: If flight control software fails, plane crashes. Requires extensive testing (MC/DC coverage, formal verification).
- **DAL E (PIESD):** No safety requirement. Example: IFE crashes, passenger sees blank screen. Software can be commodity (Linux, standard apps), minimal certification.

════════════════════════════════════════════════════════════════════

📚 **14. FURTHER READING**
═══════════════════════════

**Standards & Guidelines:**

📜 **RTCA DO-326A / EUROCAE ED-202A**
   - Airworthiness Security Process Specification
   - https://www.rtca.org/content/standards-guidance-materials

📜 **RTCA DO-356A / EUROCAE ED-203A**
   - Airworthiness Security Methods and Considerations
   - Focus: Threat modeling (STRIDE), security testing

📜 **ARINC 811**
   - Commercial Aircraft Information Security Concepts
   - Domain isolation, firewall requirements

📜 **DO-178C**
   - Software Considerations in Airborne Systems
   - DAL levels, verification methods

📜 **FAA AC 20-170**
   - Certification Memo on Cybersecurity
   - https://www.faa.gov/regulations_policies/advisory_circulars/

**Books:**

📖 *"Avionics: Development and Implementation"* — Cary Spitzer  
📖 *"Aircraft Data Networks"* — Ed Harcourt  
📖 *"Cybersecurity for Aerospace"* — AIAA Publication  

**Articles & Papers:**

📄 "Boeing 787 Network Architecture" (IEEE Aerospace Conference)  
📄 "Securing In-Flight Entertainment Systems" (USENIX Security)  
📄 "Supply Chain Security in Avionics" (SAE International)

**Training & Certification:**

🎓 **RTCA Training Courses:** DO-326A/DO-356A workshops  
🎓 **SAE International:** Aerospace Cybersecurity seminars  
🎓 **SANS:** ICS515 (Industrial Control Systems Security)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand 3-domain architecture (ACD, AISD, PIESD)
- [ ] Memorize DAL levels (A/B/C/D/E) and criticality
- [ ] Explain data diode vs. firewall vs. air gap
- [ ] Draw network topology from memory
- [ ] Describe one real-world incident (2015 "IFE hack")
- [ ] Configure basic firewall rules for domain isolation
- [ ] Understand supply chain security risks
- [ ] Explain sanitized data flow (GPS → moving map)

════════════════════════════════════════════════════════════════════

🎓 **BONUS: MEMORABLE ANALOGIES**
═══════════════════════════════════

**ACD = Nuclear Submarine Reactor Room**
- Sealed, no Wi-Fi, two-person rule, catastrophic if breached

**AISD = Hospital Staff Network**
- Doctors have tablets, maintenance logs, not patient-facing

**PIESD = Hotel Guest Wi-Fi**
- Anyone can connect, if it goes down hotel still operates

**Data Diode = One-Way Mirror**
- You can see through (ACD → AISD), but can't reach back

**Air Gap = Two Islands**
- No bridge, no boat, no connection whatsoever

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Three Domains, Three Mindsets:**
   - ACD: "Zero defects, zero access"
   - AISD: "Controlled, audited, verified"
   - PIESD: "Isolated, monitored, expendable"

2️⃣ **Isolation is Physical, Not Just Logical:**
   - Data diodes have **cut wires** (not software filters)
   - Air gaps mean **separate cables** (not VLANs)

3️⃣ **Defense in Depth:**
   - If PIESD is hacked → firewall blocks
   - If firewall is bypassed → data diode stops
   - If data diode fails → air gap remains

4️⃣ **Certification Drives Design:**
   - DAL A/B systems cannot use commodity tech
   - DO-178C verification = years of effort
   - Security is now equal to safety (DO-326A)

5️⃣ **Human Factors Matter:**
   - Insider threat is real (two-person rule)
   - USB drives are vectors (whitelisting)
   - Training prevents 90% of incidents

════════════════════════════════════════════════════════════════════

📖 **7. SECURITY CERTIFICATION COMPLIANCE**
═══════════════════════════════════════════

**7.1 DO-326A Compliance Matrices**
-----------------------------------

**Security Assurance Level (SAL) Assignment:**

+------------------+------------------+----------------------------------+
| **Domain**       | **SAL Level**    | **Rationale**                    |
+==================+==================+==================================+
| **ACD**          | **SAL 3**        | Flight-critical (DAL A/B)        |
|                  |                  | Sophisticated threat protection  |
|                  |                  | Red team testing required        |
+------------------+------------------+----------------------------------+
| **AISD**         | **SAL 2**        | Crew/ops systems (DAL C/D)       |
|                  |                  | Intentional threat protection    |
|                  |                  | Penetration testing required     |
+------------------+------------------+----------------------------------+
| **PIESD**        | **SAL 1**        | Passenger systems (non-critical) |
|                  |                  | Casual threat protection         |
|                  |                  | Basic security testing           |
+------------------+------------------+----------------------------------+

**DO-326A Objectives per Domain:**

**ACD (SAL 3) — 42 Objectives:**

.. code-block:: text

    Security Development Objectives (25 objectives):
    ✅ SEC-1.1: Security Requirements Definition
    ✅ SEC-1.2: Threat Modeling (STRIDE analysis)
    ✅ SEC-1.3: Attack Surface Analysis
    ✅ SEC-1.4: Secure Architecture Design
    ✅ SEC-1.5: Cryptographic Design (AES-256, TLS 1.3)
    ...
    ✅ SEC-1.25: Security Assurance Case
    
    Security Verification Objectives (17 objectives):
    ✅ SEC-2.1: Security Requirements Review
    ✅ SEC-2.2: Security Architecture Review
    ✅ SEC-2.3: Penetration Testing (comprehensive)
    ✅ SEC-2.4: Fuzzing (all protocols)
    ✅ SEC-2.5: Red Team Exercise (SAL 3 only)
    ✅ SEC-2.6: Cryptographic Validation (FIPS 140-2)
    ✅ SEC-2.7: Side-Channel Analysis (timing, power, EM)
    ✅ SEC-2.8: Code Security Review (MISRA C++)
    ...
    ✅ SEC-2.17: Security Accomplishment Summary (SAS)

**AISD (SAL 2) — 28 Objectives:**

.. code-block:: text

    Security Development: 17 objectives (subset of SAL 3)
    Security Verification: 11 objectives
    
    Key Differences from SAL 3:
    - No red team exercise (SAL 3 only)
    - No side-channel analysis (SAL 3 only)
    - Reduced fuzzing scope (critical interfaces only)
    - Standard penetration testing (not comprehensive)

**PIESD (SAL 1) — 15 Objectives:**

.. code-block:: text

    Security Development: 9 objectives (basic requirements)
    Security Verification: 6 objectives
    
    Key Differences from SAL 2:
    - No formal threat modeling (basic threat list)
    - No code security review (automated only)
    - Basic penetration testing (OWASP Top 10)
    - No fuzzing (optional)

**7.2 DO-356A Verification Methods**
------------------------------------

**Security Testing by Domain:**

+------------------+---------------------+---------------------+---------------------+
| **Test Type**    | **ACD (SAL 3)**     | **AISD (SAL 2)**    | **PIESD (SAL 1)**   |
+==================+=====================+=====================+=====================+
| Penetration Test | Comprehensive       | Standard            | Basic               |
|                  | (30 days)           | (10 days)           | (5 days)            |
+------------------+---------------------+---------------------+---------------------+
| Fuzzing          | All protocols       | Critical only       | Optional            |
|                  | (ARINC 429, 664,    | (ARINC 664,         |                     |
|                  | CAN, Ethernet)      | Ethernet)           |                     |
+------------------+---------------------+---------------------+---------------------+
| Red Team         | ✅ Required         | ❌ Not required     | ❌ Not required     |
|                  | (APT simulation)    |                     |                     |
+------------------+---------------------+---------------------+---------------------+
| Static Analysis  | MISRA C++ (all)     | MISRA C++ (sec)     | Automated only      |
|                  | CERT C++ (all)      | CERT C++ (sec)      |                     |
+------------------+---------------------+---------------------+---------------------+
| FIPS 140-2       | ✅ Required         | ✅ Required         | ⚠️ Recommended      |
|                  | (Level 3+)          | (Level 2+)          |                     |
+------------------+---------------------+---------------------+---------------------+
| Side-Channel     | ✅ Required         | ❌ Not required     | ❌ Not required     |
|                  | (timing, power, EM) |                     |                     |
+------------------+---------------------+---------------------+---------------------+

**Penetration Testing Results (Example):**

.. code-block:: yaml

    # penetration_test_results.yaml
    
    aircraft: N12345 (Boeing 787-9)
    date: 2026-01-10
    tester: Independent Security Lab (ISL-2026-001)
    
    domains:
      
      acd_sal3:
        duration: 30 days
        scope: [ARINC 429 bus, ARINC 664 AFDX, gateway, data diode]
        findings:
          critical: 0
          high: 0
          medium: 2
          low: 5
        
        medium_findings:
          - id: ACD-M-001
            title: "Weak RNG in boot process"
            cvss: 5.3
            status: FIXED (upgraded to FIPS 140-2 DRBG)
          
          - id: ACD-M-002
            title: "Timing variation in CAN bus parsing"
            cvss: 4.8
            status: FIXED (constant-time implementation)
        
        conclusion: "ACD meets SAL 3 requirements (0 critical/high findings)"
      
      aisd_sal2:
        duration: 10 days
        scope: [EFB, CMC, ACARS, firewall, VLAN]
        findings:
          critical: 0
          high: 1
          medium: 8
          low: 12
        
        high_findings:
          - id: AISD-H-001
            title: "SQL injection in maintenance interface"
            cvss: 8.2
            status: FIXED (parameterized queries)
        
        conclusion: "AISD meets SAL 2 requirements after remediation"
      
      piesd_sal1:
        duration: 5 days
        scope: [Wi-Fi portal, IFE server, passenger app]
        findings:
          critical: 0
          high: 3
          medium: 15
          low: 25
        
        high_findings:
          - id: PIESD-H-001
            title: "Cross-site scripting (XSS) in passenger portal"
            cvss: 7.5
            status: FIXED (input sanitization)
          
          - id: PIESD-H-002
            title: "Weak TLS cipher suites (3DES enabled)"
            cvss: 7.2
            status: FIXED (TLS 1.3 only)
          
          - id: PIESD-H-003
            title: "Excessive file upload size (10 GB)"
            cvss: 6.8
            status: FIXED (limited to 10 MB)
        
        conclusion: "PIESD meets SAL 1 requirements after remediation"

**Fuzzing Campaign Results (AISD — SAL 2):**

.. code-block:: text

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    FUZZING CAMPAIGN REPORT — AISD DOMAIN (SAL 2)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Target: ARINC 664 AFDX Gateway (AISD)
    Tool: Boofuzz v0.4.2
    Duration: 7 days (continuous)
    Test Cases: 1,250,000
    
    Results:
    ━━━━━━━
    
    Crashes Detected: 3
    
    1. NULL Pointer Dereference
       - Trigger: Malformed Virtual Link ID (0xFFFFFFFF)
       - Impact: Gateway restart (5 second downtime)
       - Severity: MEDIUM (CVSS 5.5)
       - Status: FIXED (input validation added)
    
    2. Buffer Overflow
       - Trigger: Oversized AFDX payload (>1536 bytes)
       - Impact: Memory corruption (potential RCE)
       - Severity: HIGH (CVSS 8.1)
       - Status: FIXED (bounds checking added)
    
    3. Infinite Loop
       - Trigger: Circular routing in virtual link table
       - Impact: CPU 100% (gateway unresponsive)
       - Severity: MEDIUM (CVSS 6.2)
       - Status: FIXED (loop detection added)
    
    Code Coverage: 87% (AISD gateway firmware)
    
    Conclusion: All crashes fixed, regression testing passed ✅
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Red Team Exercise (ACD — SAL 3 Only):**

.. code-block:: markdown

    # Red Team Exercise Report — ACD Domain (SAL 3)
    
    ## Executive Summary
    
    **Objective:** Simulate sophisticated APT (Advanced Persistent Threat) attack on ACD
    **Duration:** 3 weeks (21 days)
    **Team:** 5 security researchers (nation-state expertise)
    **Budget:** $150,000
    
    **Scenario:** Supply chain compromise + insider threat + physical access
    
    ## Attack Phases
    
    ### Phase 1: Reconnaissance (7 days)
    - ✅ Identified avionics vendor (Honeywell FMC)
    - ✅ Analyzed firmware update process (ARINC 615A)
    - ✅ Social engineering (3 employees profiled)
    - ❌ Failed to extract source code (code signing blocked)
    
    ### Phase 2: Initial Access (7 days)
    - ✅ Compromised USB stick (malware payload)
    - ✅ Delivered to maintenance hangar (social engineering)
    - ❌ USB autorun blocked (whitelist policy)
    - ❌ Manual execution blocked (two-person rule enforced)
    - Conclusion: **Initial access FAILED** ✅
    
    ### Phase 3: Privilege Escalation (7 days)
    - Attempted: Physical access to avionics bay
    - Result: **Locked bay, tamper-evident seals, CCTV** ✅
    - Attempted: Network attack via AISD
    - Result: **Data diode blocked all attempts** ✅
    - Conclusion: **Privilege escalation IMPOSSIBLE** ✅
    
    ## Key Findings
    
    ✅ **PASS:** ACD isolation is robust (air gap + data diode)
    ✅ **PASS:** Two-person rule prevents insider attacks
    ✅ **PASS:** USB whitelisting blocks malware delivery
    ⚠️ **WARNING:** Social engineering success rate 60% (training needed)
    
    ## Recommendations
    
    1. **Increase security awareness training** (quarterly, not annual)
    2. **Implement biometric authentication** (fingerprint for avionics bay)
    3. **Add honeypot USB ports** (detect insertion attempts)
    
    ## Conclusion
    
    **ACD meets SAL 3 requirements:** No successful attack paths found despite 
    sophisticated adversary (nation-state level) over 3 weeks. Defense-in-depth 
    strategy effective. ✅

**7.3 Security Certification Workflow**
---------------------------------------

**Phase 1: Planning (6-12 months):**

.. code-block:: text

    Step 1: Security Risk Assessment (SRA)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Identify assets (ACD, AISD, PIESD)
    - Identify threats (STRIDE analysis)
    - Assess vulnerabilities (architecture review)
    - Determine risk (Likelihood × Impact)
    - Assign SAL (ACD=3, AISD=2, PIESD=1)
    
    Step 2: Security Plan (SECP)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Define security objectives (DO-326A)
    - Define verification methods (DO-356A)
    - Define tools (Coverity, Boofuzz, Metasploit)
    - Define schedule (Gantt chart)
    - Define budget ($500K for SAL 3)
    
    Step 3: FAA Coordination
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Submit SECP to FAA (ACO)
    - Issue paper (if novel architecture)
    - Certification basis agreement
    - Milestone reviews (quarterly)

**Phase 2: Development & Verification (12-24 months):**

.. code-block:: text

    Month 1-12: Secure Development
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Secure coding (MISRA C++, CERT C++)
    - Threat modeling (STRIDE per feature)
    - Cryptographic design (TLS 1.3, AES-256)
    - Code reviews (security-focused)
    - Static analysis (weekly scans)
    
    Month 13-18: Security Testing
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Penetration testing (external lab)
    - Fuzzing (all protocols)
    - Red team (SAL 3 only)
    - FIPS 140-2 validation
    - Side-channel analysis (SAL 3 only)
    
    Month 19-24: Remediation & Regression
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Fix all critical/high findings
    - Re-test (regression testing)
    - Document fixes (traceability)
    - Update SAS (Security Accomplishment Summary)

**Phase 3: Certification (3-6 months):**

.. code-block:: text

    Step 1: Submit Security Accomplishment Summary (SAS)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Objective compliance matrix (DO-326A objectives)
    - Test results (penetration, fuzzing, red team)
    - Threat analysis (STRIDE, attack trees)
    - Risk assessment (residual risks documented)
    - Certification evidence (traceability matrix)
    
    Step 2: FAA Audit
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Document review (SAS, SECP, test reports)
    - Technical interviews (security team)
    - On-site inspection (if required)
    - Findings (major/minor observations)
    
    Step 3: Type Certificate (TC) or STC
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Issue findings closure report
    - FAA approval (DER sign-off)
    - TC/STC granted
    - Continued airworthiness (monitoring plan)

**Authority Interaction Procedures:**

.. code-block:: yaml

    # faa_interaction_procedures.yaml
    
    issue_paper_required:
      - reason: "Novel architecture (data diode for ACD isolation)"
      - when: "No existing certification precedent"
      - process:
        - draft_issue_paper: "Technical description, rationale, compliance"
        - submit_to_faa: "ACO (Aircraft Certification Office)"
        - faa_review: "30-60 days"
        - resolution: "Agree on certification approach"
    
    milestone_reviews:
      frequency: quarterly
      attendees: [applicant, FAA_ACO, DER]
      agenda:
        - progress_update: "Objectives completed"
        - findings_review: "Open security findings"
        - schedule_review: "On-track vs delayed"
        - risk_review: "New threats identified"
    
    finding_closure:
      major_finding:
        - impact: "Certification delayed (must fix)"
        - response_time: "30 days"
        - closure: "Fix + regression test + FAA re-review"
      
      minor_finding:
        - impact: "Documentation issue (no design change)"
        - response_time: "60 days"
        - closure: "Update documentation + FAA approval"

**7.4 Audit Evidence Requirements**
-----------------------------------

**Required Documentation for FAA Audit:**

.. code-block:: markdown

    # Security Certification Evidence Package
    
    ## 1. Security Planning (DO-326A Section 4)
    
    - [ ] Security Risk Assessment (SRA)
      - [ ] Asset inventory (ACD, AISD, PIESD components)
      - [ ] Threat model (STRIDE analysis per domain)
      - [ ] Vulnerability assessment (architecture + code)
      - [ ] Risk matrix (Likelihood × Impact)
      - [ ] SAL assignment (ACD=3, AISD=2, PIESD=1)
    
    - [ ] Security Plan (SECP)
      - [ ] Security objectives (DO-326A objectives per SAL)
      - [ ] Verification methods (DO-356A methods per objective)
      - [ ] Tools & techniques (Coverity, Boofuzz, Metasploit)
      - [ ] Schedule (Gantt chart with milestones)
      - [ ] Resources (team, budget, external labs)
    
    ## 2. Security Development (DO-326A Section 5)
    
    - [ ] Security requirements specification
      - [ ] Functional security requirements (authentication, encryption, etc.)
      - [ ] Derived security requirements (from threats)
      - [ ] Traceability (threats → requirements → design → code → tests)
    
    - [ ] Secure architecture design
      - [ ] Domain isolation architecture (physical + logical)
      - [ ] Data flow diagrams (ACD → AISD → PIESD)
      - [ ] Security controls (firewall, data diode, encryption)
      - [ ] Threat mitigation mapping (controls → threats)
    
    - [ ] Secure coding evidence
      - [ ] MISRA C++ compliance report (no violations)
      - [ ] CERT C++ compliance report (no violations)
      - [ ] Static analysis reports (Coverity: 0 critical/high)
      - [ ] Code review checklists (security-focused)
    
    ## 3. Security Verification (DO-356A Section 6)
    
    - [ ] Penetration testing report
      - [ ] Scope (systems, interfaces, duration)
      - [ ] Methodology (OWASP, NIST 800-115)
      - [ ] Findings (critical/high/medium/low)
      - [ ] Remediation evidence (fixes + regression tests)
    
    - [ ] Fuzzing campaign report
      - [ ] Tool (Boofuzz, AFL, Peach)
      - [ ] Targets (protocols, interfaces)
      - [ ] Test cases executed (# of iterations)
      - [ ] Crashes found (root cause analysis)
      - [ ] Code coverage (% of firmware exercised)
    
    - [ ] Red team exercise report (SAL 3 only)
      - [ ] Scenario (APT, supply chain, insider)
      - [ ] Attack phases (reconnaissance, access, persistence)
      - [ ] Success/failure per phase
      - [ ] Lessons learned + recommendations
    
    - [ ] FIPS 140-2 validation certificate
      - [ ] Algorithm: AES-256-GCM
      - [ ] Certificate number: #XXXX
      - [ ] Validation date
      - [ ] Known Answer Tests (KAT) results
    
    ## 4. Security Accomplishment Summary (SAS)
    
    - [ ] Compliance matrix (DO-326A objectives)
      - [ ] ACD: 42/42 objectives met ✅
      - [ ] AISD: 28/28 objectives met ✅
      - [ ] PIESD: 15/15 objectives met ✅
    
    - [ ] Residual risk analysis
      - [ ] Accepted risks (documented + justified)
      - [ ] Mitigations (compensating controls)
      - [ ] Monitoring plan (continued airworthiness)
    
    - [ ] Configuration management
      - [ ] Security baselines (hardware + software versions)
      - [ ] Change control (security impact analysis)
      - [ ] Traceability (requirements → design → code → tests)

**Traceability Matrix Example:**

+-------------+-----------------+-----------------+-----------------+-----------------+
| **Threat**  | **Requirement** | **Design**      | **Code**        | **Test**        |
+=============+=================+=================+=================+=================+
| PIESD→AISD  | SEC-REQ-001:    | Firewall        | iptables        | PEN-TEST-001:   |
| unauthorized| Block all       | (stateful)      | rules.sh        | Verified blocked|
| access      | PIESD→AISD      | between domains | (lines 45-67)   | (0 packets)     |
+-------------+-----------------+-----------------+-----------------+-----------------+
| SQL         | SEC-REQ-015:    | Parameterized   | db_query.cpp    | FUZZ-TEST-015:  |
| injection   | Input           | queries         | (line 234)      | No SQLi found   |
| (AISD)      | validation      |                 |                 | (10K test cases)|
+-------------+-----------------+-----------------+-----------------+-----------------+
| Weak        | SEC-REQ-023:    | TLS 1.3 only    | tls_config.c    | SCAN-TEST-023:  |
| crypto      | TLS 1.3+        | (ECDHE-P384)    | (line 89)       | Verified TLS1.3 |
| (AISD)      | AES-256         |                 |                 | only            |
+-------------+-----------------+-----------------+-----------------+-----------------+

**7.5 Continued Airworthiness (Post-Certification)**
----------------------------------------------------

**Security Monitoring Plan:**

.. code-block:: text

    Ongoing Security Activities (Post-TC/STC):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    1. Vulnerability Monitoring (Daily)
       - Subscribe to CVE feeds (NVD, CERT)
       - Monitor vendor security advisories
       - Assess impact on aircraft systems
       - Deploy patches (risk-based prioritization)
    
    2. Incident Response (24/7)
       - SIEM alerts (real-time)
       - Security Operations Center (SOC)
       - Incident investigation (forensics)
       - FAA notification (if required)
    
    3. Periodic Security Assessments (Annual)
       - Penetration testing (annual refresh)
       - Vulnerability scanning (monthly)
       - Threat modeling update (new threats)
       - Red team exercise (SAL 3, every 2 years)
    
    4. Configuration Management (Ongoing)
       - Change control (security impact analysis)
       - Version control (security baselines)
       - Audit trail (all changes logged)
    
    5. Training (Quarterly)
       - Security awareness (crew, maintenance)
       - Phishing simulations (test readiness)
       - Incident response drills (tabletop exercises)

════════════════════════════════════════════════════════════════════

📝 **ADDITIONAL EXAM QUESTIONS (SECURITY CERTIFICATION)**
═════════════════════════════════════════════════════════

**Q7:** What are the DO-326A SAL levels for ACD, AISD, and PIESD? Why?

**A7:**

- **ACD: SAL 3** (sophisticated threat) — Flight-critical (DAL A/B), requires 
  absolute protection, red team testing, side-channel analysis
- **AISD: SAL 2** (intentional threat) — Crew/ops systems (DAL C/D), penetration 
  testing, fuzzing, MFA required
- **PIESD: SAL 1** (casual threat) — Passenger systems (non-critical), basic 
  security testing, isolated from ACD/AISD

────────────────────────────────────────────────────────────────────

**Q8:** What is the difference between DO-326A and DO-356A?

**A8:**

- **DO-326A:** WHAT to do (security process specification)
  - Defines SAL levels, Security Risk Assessment (SRA), Security Plan (SECP)
- **DO-356A:** HOW to do it (security development methods)
  - Defines secure coding, penetration testing, fuzzing, red team, FIPS 140-2

────────────────────────────────────────────────────────────────────

**Q9:** Why is red team testing required for ACD (SAL 3) but not AISD (SAL 2)?

**A9:**

- **ACD (SAL 3):** Flight-critical → requires protection against sophisticated 
  adversaries (nation-state APT)
- **Red Team:** Simulates APT attack (supply chain, insider, physical access) 
  for 3 weeks
- **AISD (SAL 2):** Intentional threat only → penetration testing sufficient
- **Cost:** Red team costs $150K-$300K, justified for flight-critical systems only

════════════════════════════════════════════════════════════════════

🌟 **ADDITIONAL KEY TAKEAWAYS (SECURITY CERTIFICATION)**
═════════════════════════════════════════════════════════

6️⃣ **SAL assignment drives security effort** → ACD (SAL 3) requires 10x more 
effort than PIESD (SAL 1) — budget accordingly

7️⃣ **Red team testing is expensive but essential for ACD** → $150K-$300K for 
3-week APT simulation validates defense-in-depth

8️⃣ **Traceability is critical for certification** → Threats → Requirements → 
Design → Code → Tests (full chain documented)

9️⃣ **Continued airworthiness requires ongoing security monitoring** → 
CVE feeds, incident response, annual penetration testing

🔟 **FAA issue papers required for novel architectures** → Data diodes (no 
precedent) need 30-60 day FAA review before certification

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **SECURITY CERTIFICATION SECTIONS ADDED**  
**Created:** January 14, 2026  
**Enhancements:** DO-326A compliance matrices, DO-356A verification methods,  
SAL verification examples, red team reports, authority interaction procedures,  
audit evidence requirements, continued airworthiness monitoring  
**Next:** Apply to specific aircraft (787, A350) or use in certification audit

════════════════════════════════════════════════════════════════════