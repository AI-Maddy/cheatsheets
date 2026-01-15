🛡️ **EMBEDDED CYBERSECURITY — Master Keywords Reference**
═══════════════════════════════════════════════════════════════════════

**Visual Memory Palace for Security Concepts Across All Embedded Domains**  
**Purpose:** Quick recall 🧠 | Interview prep 💼 | Design reviews 🔍 | Standards navigation 📚  
**Coverage:** Automotive 🚗 | Avionics ✈️ | Industrial 🏭 | Medical 🏥 | Buildings 🏢

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

🔐 **GENERAL EMBEDDED SYSTEMS CYBERSECURITY**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"SCREAM HAT" Defense Framework**  
*(S-ecure boot, C-rypto, R-oot of Trust, E-nvironment, A-ttack mitigation, M-emory protection + H-ardware, A-rchitecture, T-hreat modeling)*

**🏰 Foundation Layer — Root of Trust**

- 🔑 **Root of Trust (RoT)** – Immutable hardware anchor (OTP fuses, secure ROM)
- 🔐 **Hardware Root of Trust (HRoT)** – Dedicated secure processor (e.g., ARM TrustZone, TPM)
- 🏛️ **Trusted Execution Environment (TEE)** – Isolated secure world (TrustZone, Intel SGX)
- 🔒 **Hardware Security Module (HSM)** – Crypto acceleration + tamper-resistant key storage
- 💎 **Secure Element (SE)** – Isolated chip for cryptographic operations (SIM card-like)
- 🗝️ **Secure Key Storage** – Hardware-backed keystore (no keys in software!)

**⚙️ Boot & Update Security**

- 🚀 **Secure Boot** – Chain of trust from ROM → Bootloader → OS (verify signatures)
- 📦 **Secure Firmware Update / OTA** – Encrypted, authenticated, rollback-protected updates
- ✍️ **Code Signing / Digital Signatures** – RSA/ECDSA signatures (verify authenticity)
- 🔄 **Rollback Protection** – Prevent downgrade to vulnerable versions (monotonic counter)

**🧱 Memory & Access Control**

- 🛡️ **Memory Protection Unit (MPU)** – Region-based access control (ARM Cortex-M/R)
- 🗺️ **Memory Management Unit (MMU)** – Virtual memory, page-level protection (Cortex-A)
- 🚫 **Stack Smashing Protection** – Canaries detect buffer overflows
- 💥 **Buffer Overflow Mitigation** – ASLR, DEP/NX (no-execute pages)
- 🔐 **Privilege Separation** – User mode vs kernel mode, least privilege principle

**🎭 Attack Surface & Threat Modeling**

- 🎯 **Attack Surface Reduction** – Minimize exposed interfaces, disable unused features
- 🏗️ **Defense-in-Depth** – Layered security (perimeter → network → host → app)
- 🌀 **Threat Modeling** – STRIDE (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation)
- 🔍 **Vulnerability Management** – CVE tracking, patching, coordinated disclosure
- 🚫 **Zero-Trust Architecture** – "Never trust, always verify" (adapted for embedded)

**⚡ Physical & Side-Channel Attacks**

- ⏱️ **Side-Channel Attacks** – Timing attacks, power analysis (DPA/SPA), EM radiation
- 💥 **Fault Injection / Glitching** – Voltage/clock glitching to bypass security
- 🔬 **Invasive Attacks** – Chip delayering, probing (requires lab equipment)
- 🛡️ **Countermeasures** – Constant-time crypto, power filtering, sensors (temp/voltage)

**🔐 Cryptography Essentials**

- 🔑 **AES (Advanced Encryption Standard)** – Symmetric cipher (128/192/256-bit)
- 📈 **ECC (Elliptic Curve Cryptography)** – Efficient public-key crypto (smaller keys than RSA)
- 🔒 **RSA** – Traditional public-key (2048/4096-bit, slower than ECC)
- #️⃣ **SHA-256/SHA-3** – Cryptographic hash functions (integrity, signatures)
- 🔐 **HMAC** – Keyed-hash message authentication (verify message authenticity)
- 🌐 **TLS 1.3** – Secure communication (HTTPS, certificate-based trust)

**🏗️ Development & Lifecycle**

- 🔄 **Secure SDLC** – Security integrated throughout development lifecycle
- 🎯 **Secure-by-Design** – Security requirements from day 1 (not bolt-on)
- 📦 **Software Bill of Materials (SBOM)** – Inventory of components (CycloneDX, SPDX)
- ⚠️ **Resource Constraints** – Limited CPU, RAM, power (affects crypto choices)  

════════════════════════════════════════════════════════════════════════════

🚗 **AUTOMOTIVE CYBERSECURITY**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"TARA UN-CARS"**  
*(TARA = Threat Analysis, UN = Regulations, CARS = CAN/Attack/Response/Supply chain)*

**📜 Standards & Regulations (Mandatory for EU/Global)**

- 🌍 **ISO/SAE 21434** – Automotive cybersecurity engineering standard (road vehicle CSMS)
- 🇪🇺 **UNECE WP.29** – UN vehicle cyber regulations (mandatory for EU type approval)
  - 🛡️ **UN R155** – Cybersecurity Management System (CSMS) requirements
  - 🔄 **UN R156** – Software Update Management System (SUMS) requirements
- 🔗 **ISO 26262 + Cybersecurity** – Safety meets security (ASIL + CAL alignment)

**🔍 Risk & Threat Analysis**

- 🎯 **TARA (Threat Analysis & Risk Assessment)** – Core ISO 21434 methodology
  - 🔴 **CAL (Cybersecurity Assurance Level)** – CAL 1 (low) → CAL 4 (high)
  - 📊 **Attack Feasibility Rating** – Basic / Enhanced / Moderate / High
- 🏢 **CSMS (Cybersecurity Management System)** – Organizational cyber process
- 📦 **SBOM (Software Bill of Materials)** – Track all software components & vulnerabilities

**🔌 Vehicle Networks & Attack Vectors**

- 🚌 **CAN Bus Security** – Controller Area Network (no encryption by default!)
  - ⚡ **CAN-FD** – Faster CAN (still lacks native security)
  - 🔒 **CAN MAC (Message Authentication)** – Add authentication to CAN messages
- 🌐 **Automotive Ethernet** – TCP/IP in vehicles (MACsec for security)
- 📡 **V2X Security** – Vehicle-to-Everything (V2V, V2I) with PKI certificates
- 🔧 **OBD-II Attacks** – Diagnostic port as entry point (physical access)
- 📱 **Infotainment Attacks** – Android Auto, CarPlay vulnerabilities
- 📞 **Telematics Gateway** – Remote connectivity (T-Box, TCU)

**🛡️ Defense Mechanisms**

- 🚨 **Vehicle IDS (Intrusion Detection System)** – Monitor CAN/Ethernet for anomalies
- 🔐 **ECU Hardening** – Secure boot, code signing, memory protection on Electronic Control Units
- 🔄 **Secure OTA Updates** – Over-the-air firmware with encryption + rollback protection
- 🔑 **Automotive PKI** – Public Key Infrastructure for V2X certificates
- 🔗 **Supply Chain Security** – Verify component authenticity (anti-counterfeit)
- 🔮 **Post-Quantum Crypto** – Preparing for quantum computers (NIST PQC algorithms)

**💡 Quick Recall:** *"CAN buses are highways without traffic lights — add guards (IDS/MAC)!"*

════════════════════════════════════════════════════════════════════════════

✈️ **AVIONICS CYBERSECURITY**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"DO-326 SAL Security Airborne Data"**  
*(DO-326 = Process, SAL = Levels, Focus on airborne systems)*

**📜 Standards & Guidelines**

- 📘 **DO-326A / ED-202A** – Airworthiness Security Process Specification
- 📗 **DO-356A / ED-203A** – Airworthiness Security Methods and Considerations
- 📙 **DO-355 / ED-204** – Information Security Guidance for Continuing Airworthiness
- 🔗 **Integration:** DO-178C (software) + DO-254 (hardware) + ARP4754A (systems)

**🎚️ Security Assurance Levels (SAL)**

- 🟢 **SAL 0** – No security requirements (no connectivity)
- 🟡 **SAL 1** – Basic security (low impact)
- 🟠 **SAL 2** – Moderate security (significant impact)
- 🔴 **SAL 3** – High security (catastrophic impact, similar to DAL A)

**⚠️ Threats to Airborne Systems**

- 🦠 **Malware Prevention** – Virus/worm detection & prevention
- 🔓 **Intentional Unauthorized Electronic Interaction (IUEI)** – Hacking attempts
- 📡 **Remote Access Threats** – Wi-Fi, satcom, cellular connectivity risks
- 💾 **Data Loading Security** – ARINC 615/615A secure software loading
- 🔌 **Physical Access** – Maintenance ports, USB, removable media

**🛡️ Security Process**

- 🔍 **Threat Modeling** – Identify assets, threats, attack vectors
- 🌊 **Data Flow Analysis** – Map connectivity & trust boundaries
- 🛡️ **Protection Profiles** – Reusable security requirements
- 📊 **Security Risk Assessment** – Likelihood × severity = risk level
- 🔄 **Continuing Airworthiness Security** – Post-certification monitoring (DO-355)

**💡 Quick Recall:** *"SAL levels protect planes like DAL protects safety — both go to level 3!"*

════════════════════════════════════════════════════════════════════════════

🏢 **BUILDING AUTOMATION CYBERSECURITY**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"BACnet KNX Zones = Building IoT Protection"**  
*(Focus on protocol security + segmentation)*

**🏗️ Building Automation Protocols**

- 🏢 **BACnet** – Building Automation and Control networks
  - 🔓 **BACnet/IP** – IP-based (plaintext by default — vulnerable!)
  - 🔐 **BACnet/SC (Secure Connect)** – TLS 1.3, WebSocket security (modern!)
- 🏠 **KNX** – European building automation standard
  - 🔑 **KNX Data Secure** – AES-128 CCM encryption for group communication
  - 🌐 **KNX/IP Secure** – TLS for IP tunneling
- 🏭 **Modbus/TCP** – Industrial protocol (also used in buildings, no security!)

**🚨 Building IoT (BIoT) Risks**

- 🌡️ **HVAC System Attacks** – Temperature manipulation, energy theft
- 💡 **Lighting Control** – Unauthorized access to lighting systems
- 🚪 **Access Control Integration** – Physical + cyber security convergence
- 🎥 **Surveillance Systems** – Camera hijacking, privacy breaches
- 🔥 **Fire/Life Safety** – Critical systems requiring high integrity

**🛡️ Defense Strategies**

- 🧱 **Zones & Conduits** – Network segmentation (IEC 62443 adapted)
  - 🔒 **Zone:** Group of assets with similar security requirements
  - 🚇 **Conduit:** Secure communication path between zones
- 🔐 **TLS Encryption** – Encrypt BACnet/SC, KNX/IP Secure traffic
- 🔑 **Authentication & Authorization** – Role-based access control (RBAC)
- 🏰 **Legacy Protocol Hardening** – VLANs, firewall rules for old BACnet/IP
- 🌐 **Network Segmentation** – Isolate building automation from corporate IT

**💡 Quick Recall:** *"Buildings run on BACnet & KNX — lock them down with SC (Secure Connect)!"*

════════════════════════════════════════════════════════════════════════════

🏭 **INDUSTRIAL AUTOMATION CYBERSECURITY (ICS/OT)**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"IEC 62443 — 4 Security Levels, Zones & Conduits, Purdue Model"**  
*(The gold standard for industrial cybersecurity)*

**📜 IEC 62443 Standard Family**

- 🌍 **IEC 62443** – Comprehensive industrial automation security standard
  - 📘 **IEC 62443-1-x** – General concepts, terminology, metrics
  - 📗 **IEC 62443-2-x** – Policies & procedures (CSMS for asset owners)
  - 📙 **IEC 62443-3-x** – System requirements (zones, conduits, security levels)
  - 📕 **IEC 62443-4-x** – Component requirements (secure development, technical specs)

**🎚️ Security Levels (SL)**

- **SL-T (Target)** – Required security level based on risk assessment
- **SL-A (Achieved)** – Actual security level implemented
- **SL-C (Capability)** – Component/product security rating

| Level | Threat Profile | Example Scenario |
|:------|:---------------|:-----------------|
| 🟢 **SL 1** | Casual attacker | Basic protection |
| 🟡 **SL 2** | Intentional attacker (low resources) | Most industrial sites |
| 🟠 **SL 3** | Skilled attacker (moderate resources) | Critical infrastructure |
| 🔴 **SL 4** | Highly skilled attacker (extensive resources) | National security |

**🏗️ Architecture Models**

- 🏛️ **Purdue Model** – Reference architecture for industrial networks
  - **Level 0:** Physical process (sensors, actuators)
  - **Level 1:** Intelligent devices (PLCs, RTUs)
  - **Level 2:** Supervisory control (SCADA, HMI)
  - **Level 3:** Operations management (MES, historians)
  - **Level 4:** Business logistics (ERP, enterprise)
  - **Level 5:** Enterprise network
- 🧱 **Zones & Conduits** – Logical segmentation (like firewalls between zones)

**🔌 Industrial Protocols (Often Insecure!)**

- 🔧 **Modbus/TCP** – Serial protocol over TCP/IP (no authentication/encryption)
- 🏭 **OPC UA (Unified Architecture)** – Modern, supports security (certificates, encryption)
- ⚙️ **PROFINET** – Ethernet-based automation (PROFINET Security in newer versions)
- 📡 **DNP3** – Power grid protocol (DNP3 Secure Authentication added)
- 🔌 **EtherNet/IP** – Industrial Ethernet (CIP Security for newer devices)

**⚠️ ICS-Specific Threats**

- 🦠 **Stuxnet** – Famous PLC malware (centrifuge attack)
- 💥 **Industroyer / Crashover** – Power grid attacks
- 🔥 **Triton / Trisis** – Safety system targeting (Schneider Electric Triconex)
- ⏱️ **Availability > Confidentiality** – Downtime = major cost (different from IT!)

**🛡️ Defense Strategies**

- 👥 **Shared Responsibility Model** – Asset owner + system integrator + component supplier
- 🔄 **Secure Development Lifecycle** – IEC 62443-4-1 requirements for vendors
- 🔧 **Patch Management** – Challenge: OT systems can't reboot easily (maintenance windows)
- 🌉 **OT/IT Convergence** – Industrial + enterprise networks (need DMZ, firewalls)
- 🔍 **Risk Assessment** – HAZOP, bow-tie analysis adapted for cyber

**💡 Quick Recall:** *"Purdue 0-5 levels = factory floor to executive suite. Zone it, conduit it, secure it!"*

════════════════════════════════════════════════════════════════════════════

🏥 **MEDICAL DEVICE CYBERSECURITY**
─────────────────────────────────────────────────────────────────────────

**🎯 Memory Hook:** **"FDA 524B + SBOM = Patient Safety First"**  
*(Medical devices = patient harm risk, unique regulatory landscape)*

**📜 Regulations & Standards**

- 🇺🇸 **FDA Cybersecurity Guidance** – U.S. regulatory requirements
  - 📘 **Premarket Guidance (2023)** – Cybersecurity in device design (before approval)
  - 📗 **Postmarket Guidance** – Vulnerability management after market release
  - ⚖️ **Section 524B FD&C Act** – Cyber devices requiring FDA attention
- 🌍 **IEC 81001-5-1** – Health software & health IT systems security lifecycle
- 🏥 **IEC 80001-1** – Risk management for networked medical devices
- 💊 **ISO 14971** – Medical device risk management (safety + security integration)
- 🔐 **IEC 62304 + Security** – Software lifecycle (Class A/B/C with cyber considerations)

**🔒 Key Security Requirements**

- 📦 **SBOM (Software Bill of Materials)** – FDA mandatory (CycloneDX/SPDX format)
  - 📋 Track all components (OS, libraries, SOUP)
  - 🔍 Monitor for CVEs (Common Vulnerabilities and Exposures)
- 🚨 **Coordinated Vulnerability Disclosure** – Responsible disclosure process
- 🔄 **Secure Update / Patch Management** – Remote patches without clinic visits
- 👤 **Patient Safety Integration** – Cybersecurity risk → patient harm analysis
- 🔐 **Authentication & Authorization** – Clinician/patient/admin roles

**⚠️ Medical Device Attack Vectors**

- 💉 **Infusion Pumps** – Wireless dosing manipulation (deadly!)
- 🫀 **Implantables** – Pacemakers, ICDs (physical proximity attacks)
- 🧪 **Diagnostic Devices** – Alter test results (glucose meters, lab equipment)
- 🏥 **Hospital Networks** – Ransomware spreading to life-critical devices
- 📡 **Wireless Interfaces** – Bluetooth, Wi-Fi, NFC vulnerabilities

**🛡️ Defense & Compliance**

- 🔍 **Threat Modeling** – STRIDE adapted for medical context (harm scenarios)
- 🏥 **HIPAA Overlap** – Patient data privacy + device security
- 📋 **Premarket Submission Artifacts:**
  - Cybersecurity risk assessment
  - Threat model & SBOM
  - Security architecture diagram
  - Update/patch plan
- 🔄 **Postmarket Monitoring** – Continuous vulnerability scanning & patching
- 🗣️ **CVD (Coordinated Vulnerability Disclosure)** – 90-day disclosure timeline

**💡 Quick Recall:** *"SBOM = Safety BOM — track every component to protect patients!"*

════════════════════════════════════════════════════════════════════════════

🎓 **MEMORIZATION AIDS & MNEMONICS**
─────────────────────────────────────────────────────────────────────────

**🌈 Color Coding System**

- 🔴 **Red = Critical/Regulatory** – ISO 21434, UN R155, FDA 524B, IEC 62443
- 🟠 **Orange = Threats** – Attacks, vulnerabilities, risk scenarios
- 🟡 **Yellow = Architecture** – Zones, conduits, TEE, Purdue model
- 🟢 **Green = Defense** – Crypto, secure boot, IDS, hardening
- 🔵 **Blue = Protocols** – CAN, BACnet, Modbus, OPC UA
- 🟣 **Purple = Lifecycle** – SDLC, TARA, threat modeling, patching

**🔢 Number Associations**

- **21434** – Automotive (ISO/SAE 21434)
- **62443** – Industrial (IEC 62443, also 4 security levels!)
- **155/156** – UN Regulations (R155 = CSMS, R156 = SUMS)
- **326/356/355** – Avionics DO standards
- **524B** – Medical FDA section
- **0-3** – SAL levels (avionics) / Security Levels 0-4 (IEC 62443)

**🎯 Domain Quick ID**

| Emoji | Domain | Key Standard | Core Threat |
|:------|:-------|:-------------|:------------|
| 🚗 | Automotive | ISO 21434 | CAN bus attacks |
| ✈️ | Avionics | DO-326A | IUEI (hacking) |
| 🏢 | Buildings | BACnet/SC | Legacy plaintext |
| 🏭 | Industrial | IEC 62443 | Stuxnet-like |
| 🏥 | Medical | FDA 524B | Patient harm |

**📚 Acronym Decoder**

- **TARA** = Threat Analysis & Risk Assessment
- **CSMS** = Cybersecurity Management System
- **SUMS** = Software Update Management System
- **SBOM** = Software Bill of Materials
- **HSM** = Hardware Security Module
- **TEE** = Trusted Execution Environment
- **SAL** = Security Assurance Level (avionics)
- **SL** = Security Level (industrial)
- **CAL** = Cybersecurity Assurance Level (automotive)
- **IDS** = Intrusion Detection System
- **PKI** = Public Key Infrastructure
- **OTA** = Over-the-Air (updates)
- **IUEI** = Intentional Unauthorized Electronic Interaction

**🧠 Memory Palace Technique**

Imagine walking through a **secure building** (your memory palace):

1. 🚪 **Entrance (Boot)** – Secure boot checks credentials (Root of Trust)
2. 🏛️ **Lobby (TEE/HSM)** – Secure vault in the center (hardware security)
3. 🚗 **Parking Garage** – Cars with CAN bus (automotive cybersecurity)
4. ✈️ **Rooftop Helipad** – Helicopters with DO-326A (avionics)
5. 🏭 **Basement Factory** – Industrial equipment with IEC 62443
6. 🏥 **Medical Wing** – Infusion pumps with FDA SBOM requirements
7. 🏢 **HVAC Room** – BACnet controllers (building automation)
8. 🔐 **Server Room** – Crypto keys, update servers (secure lifecycle)

**Walk through this building mentally to recall all domains!**

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Recall**
─────────────────────────────────────────────────────────────────────────

**Foundation:** Root of Trust → Secure Boot → TEE/HSM → Crypto (AES/ECC) → Defense-in-Depth

**Automotive 🚗:** ISO 21434 + UN R155/R156 | TARA + CAL | CAN/V2X security | Vehicle IDS

**Avionics ✈️:** DO-326A/356A/355 | SAL 0-3 | IUEI threats | Data loading security

**Buildings 🏢:** BACnet/SC + KNX Secure | Zones & Conduits | Legacy protocol hardening

**Industrial 🏭:** IEC 62443 (SL 1-4) | Purdue Model | Zones/Conduits | OPC UA security

**Medical 🏥:** FDA 524B + Premarket | SBOM mandatory | Patient safety = cybersecurity

**Key Concept:** Security = **Confidentiality + Integrity + Availability** (CIA triad)  
**Embedded twist:** Often **Availability > Confidentiality** (safety-critical systems can't afford downtime!)

════════════════════════════════════════════════════════════════════════════

📊 **Standards Cross-Reference Matrix**
─────────────────────────────────────────────────────────────────────────

| Domain | Primary Standard | Regulation | Risk Method | Security Levels |
|:-------|:-----------------|:-----------|:------------|:----------------|
| 🚗 Automotive | ISO/SAE 21434 | UN R155/R156 | TARA | CAL 1-4 |
| ✈️ Avionics | DO-326A/356A | FAA/EASA | Threat Model | SAL 0-3 |
| 🏭 Industrial | IEC 62443 | (Varies) | Risk Assessment | SL 1-4 |
| 🏥 Medical | IEC 81001-5-1 | FDA 524B | ISO 14971 | (Risk-based) |
| 🏢 Buildings | BACnet/SC, KNX | (Varies) | IEC 62443 adapted | (Varies) |

════════════════════════════════════════════════════════════════════════════

**🎯 Study Strategy:**
1. Master **general concepts** first (Root of Trust, TEE, crypto)
2. Learn **domain standards** (ISO 21434, IEC 62443, DO-326A)
3. Practice **threat scenarios** (CAN attack, infusion pump hack, Stuxnet)
4. Memorize **acronyms** using the decoder above
5. Use the **memory palace** technique for domain recall

**📚 Deep Dive References:**
- ISO/SAE 21434 (automotive CSMS)
- IEC 62443 series (industrial automation security)
- DO-326A/ED-202A (airworthiness security process)
- FDA Premarket Cybersecurity Guidance (2023)
- BACnet/SC specification (ASHRAE Addendum 135-2016bj)

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 2.0 (Enhanced with visual mnemonics, color coding, memory aids)  

**Version:** 2.0 (Enhanced with visual mnemonics, color coding, memory aids)