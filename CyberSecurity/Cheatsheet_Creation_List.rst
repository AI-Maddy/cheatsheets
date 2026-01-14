📋 **CYBERSECURITY CHEATSHEETS — Master Creation List**
═══════════════════════════════════════════════════════════════════════

**Comprehensive Roadmap for Embedded Cybersecurity Documentation**  
**Purpose:** Track cheatsheet development priorities 🎯 | Coverage planning 📊 | Learning path 🗺️  
**Status:** Planning phase → Development → Review → Complete ✅

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

🏆 **PRIORITY LEVELS**
─────────────────────────────────────────────────────────────────────────

- 🔴 **P0 (Critical)** – Essential, industry-standard topics
- 🟠 **P1 (High)** – Important, frequently referenced
- 🟡 **P2 (Medium)** – Valuable, domain-specific deep dives
- 🟢 **P3 (Low)** – Nice-to-have, emerging topics

════════════════════════════════════════════════════════════════════════════

🔐 **GENERAL EMBEDDED SECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**Foundation & Architecture (6 cheatsheets)**

1. 🔴 **Root_of_Trust_and_Secure_Boot.rst** [P0]
   - Hardware Root of Trust (HRoT) architectures
   - Secure boot chain of trust (ROM → Bootloader → OS)
   - OTP fuses, secure ROM, boot ROM security
   - Verified boot vs measured boot
   - Boot attestation and remote verification
   - Common vulnerabilities and mitigations
   - Examples: ARM TrustZone, TPM 2.0, Apple Secure Enclave

2. 🔴 **Trusted_Execution_Environments.rst** [P0]
   - TEE architecture and isolation mechanisms
   - ARM TrustZone (Cortex-A, Cortex-M)
   - Intel SGX enclaves
   - AMD SEV (Secure Encrypted Virtualization)
   - RISC-V PMP (Physical Memory Protection)
   - Secure world vs normal world
   - Trusted applications (TAs) development
   - GlobalPlatform TEE specifications

3. 🔴 **Hardware_Security_Module_HSM.rst** [P0]
   - HSM vs TPM vs Secure Element comparison
   - Cryptographic acceleration
   - Tamper detection and response
   - Key generation, storage, and lifecycle
   - FIPS 140-2/140-3 compliance levels
   - HSM use cases: automotive, payment systems, IoT
   - Examples: NXP EdgeLock, STM32 secure storage

4. 🟠 **Cryptography_for_Embedded_Systems.rst** [P1]
   - Symmetric crypto: AES (128/192/256), ChaCha20
   - Asymmetric crypto: RSA (2048/4096), ECC (P-256, P-384)
   - Hash functions: SHA-256, SHA-3, BLAKE2
   - MAC: HMAC, CMAC, Poly1305
   - Key derivation: HKDF, PBKDF2
   - Authenticated encryption: AES-GCM, ChaCha20-Poly1305
   - Post-quantum cryptography (NIST PQC: Kyber, Dilithium)
   - Constant-time implementations
   - Hardware crypto accelerators

5. 🟠 **Secure_Firmware_Updates_OTA.rst** [P1]
   - OTA update architectures (A/B partitions, recovery mode)
   - Update package format and signing
   - Delta updates vs full updates
   - Rollback protection mechanisms
   - Update verification and attestation
   - Secure download channels (TLS, HTTPS)
   - Fail-safe recovery strategies
   - Standards: SUIT (IETF), OMA-DM, automotive SUMS

6. 🟠 **Memory_Protection_and_Exploitation.rst** [P1]
   - MPU vs MMU architectures
   - Stack smashing attacks and canaries
   - Heap exploitation (use-after-free, double-free)
   - Buffer overflows and ROP chains
   - ASLR, DEP/NX, W^X policies
   - Privilege separation (user/kernel modes)
   - Embedded-specific challenges (no MMU on Cortex-M)

**Threats & Attack Vectors (4 cheatsheets)**

7. 🟠 **Side_Channel_Attacks.rst** [P1]
   - Timing attacks (cache timing, instruction timing)
   - Power analysis: SPA (Simple), DPA (Differential)
   - Electromagnetic (EM) analysis
   - Acoustic cryptanalysis
   - Countermeasures: constant-time code, noise injection, power filtering
   - Tools: ChipWhisperer, oscilloscopes
   - Real-world cases: AES side-channel attacks

8. 🟡 **Fault_Injection_Attacks.rst** [P2]
   - Voltage glitching (VCC/GND manipulation)
   - Clock glitching (frequency manipulation)
   - Laser fault injection
   - EM fault injection
   - Rowhammer attacks
   - Countermeasures: voltage monitors, duplicate checks, error detection codes
   - Tools: ChipSHOUTER, laser setups

9. 🟡 **Physical_Attacks_and_Tamper_Protection.rst** [P2]
   - Invasive attacks: chip delayering, probing
   - Semi-invasive: laser, UV light
   - Package tampering detection
   - Tamper-evident designs
   - Mesh sensors, active shields
   - Secure chip packaging
   - Anti-reverse engineering techniques

10. 🟢 **Supply_Chain_Security.rst** [P3]
    - Hardware trojans detection
    - Counterfeit component identification
    - SBOM (Software Bill of Materials) for embedded
    - Secure manufacturing and supply chain
    - Component authentication
    - Third-party code auditing
    - Open-source software (OSS) risk management

**Security Development & Process (3 cheatsheets)**

11. 🔴 **Threat_Modeling_for_Embedded_Systems.rst** [P0]
    - STRIDE methodology (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation)
    - Attack trees and attack graphs
    - Data flow diagrams (DFD)
    - Trust boundaries identification
    - Asset identification and valuation
    - Threat prioritization (likelihood × impact)
    - Domain-specific threat catalogs (automotive, medical, industrial)

12. 🟠 **Secure_SDLC_for_Embedded.rst** [P1]
    - Security requirements gathering
    - Secure design principles (least privilege, defense-in-depth)
    - Secure coding standards (CERT C, MISRA C)
    - Static analysis tools (Coverity, Klocwork, CodeSonar)
    - Dynamic analysis and fuzzing
    - Penetration testing for embedded
    - Security verification and validation
    - Continuous security monitoring

13. 🟡 **Vulnerability_Management_and_Patching.rst** [P2]
    - CVE tracking and monitoring
    - Coordinated vulnerability disclosure (CVD)
    - Patch development and testing
    - Emergency patching procedures
    - Patch deployment strategies (staged rollout)
    - Version control and update logs
    - End-of-life (EOL) device handling

════════════════════════════════════════════════════════════════════════════

🚗 **AUTOMOTIVE CYBERSECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**Standards & Compliance (4 cheatsheets)**

14. 🔴 **ISO_SAE_21434_Automotive_Cybersecurity.rst** [P0]
    - Standard structure and lifecycle phases
    - Concept phase: item definition, threat analysis
    - Product development: cybersecurity requirements, design, implementation
    - TARA (Threat Analysis & Risk Assessment) methodology
    - CAL (Cybersecurity Assurance Level) 1-4
    - Attack feasibility rating (Basic, Enhanced, Moderate, High)
    - Cybersecurity validation and verification
    - Post-development: incident response, updates, decommissioning
    - Integration with ISO 26262 (functional safety)

15. 🔴 **UN_R155_R156_CSMS_SUMS.rst** [P0]
    - UNECE WP.29 overview and scope
    - UN R155: Cybersecurity Management System (CSMS) requirements
    - UN R156: Software Update Management System (SUMS) requirements
    - Type approval process for EU/global markets
    - CSMS organizational requirements
    - Risk assessment and mitigation
    - Cybersecurity monitoring and incident response
    - Update validation and verification processes

16. 🟠 **Automotive_TARA_and_CAL.rst** [P1]
    - TARA process step-by-step
    - Asset identification (ECUs, data, functions)
    - Threat scenario development
    - Impact rating: Safety, Financial, Operational, Privacy
    - Attack path analysis
    - CAL determination formulas
    - Mitigation strategy selection
    - Residual risk acceptance
    - TARA documentation templates

17. 🟡 **Automotive_Functional_Safety_Cybersecurity_Integration.rst** [P2]
    - ISO 26262 + ISO 21434 overlap
    - ASIL vs CAL correlation
    - Safety-related cybersecurity threats
    - Combined HARA and TARA
    - Safety of the Intended Functionality (SOTIF) + cybersecurity
    - Dual assurance: safe AND secure
    - Example: ADAS system safety + security analysis

**Vehicle Networks & Protocols (5 cheatsheets)**

18. 🔴 **CAN_Bus_Security.rst** [P0]
    - CAN protocol fundamentals (no authentication/encryption)
    - CAN message injection attacks
    - CAN ID spoofing and masquerading
    - Bus-off attacks (DoS)
    - CAN-FD security considerations
    - CAN message authentication (MAC)
    - Intrusion detection for CAN
    - SecOC (Secure Onboard Communication) - AUTOSAR
    - CAN encryption approaches

19. 🟠 **Automotive_Ethernet_Security.rst** [P1]
    - 100BASE-T1, 1000BASE-T1 physical layer
    - MACsec (802.1AE) for link-layer encryption
    - IPsec for network-layer security
    - TLS for application-layer security
    - VLAN segmentation in vehicles
    - Switch security and port authentication
    - Time-Sensitive Networking (TSN) security
    - DoIP (Diagnostics over IP) security

20. 🟠 **V2X_Security_and_PKI.rst** [P1]
    - V2V, V2I, V2P, V2N communication types
    - DSRC vs C-V2X technologies
    - PKI architecture for V2X
    - Certificate lifecycle management
    - Misbehavior detection
    - Privacy preservation (pseudonymous certificates)
    - Revocation mechanisms
    - Standards: IEEE 1609.2, ETSI ITS security

21. 🟡 **FlexRay_Security.rst** [P2]
    - FlexRay protocol overview
    - Time-triggered vs event-triggered security
    - FlexRay vulnerabilities
    - Authentication and encryption add-ons
    - Safety-critical network protection

22. 🟢 **Automotive_Diagnostics_Security.rst** [P3]
    - OBD-II attack vectors
    - UDS (Unified Diagnostic Services) security
    - Diagnostic authentication (seed-key, certificate)
    - Physical security of OBD port
    - Remote diagnostics security

**ECU & System Security (3 cheatsheets)**

23. 🔴 **ECU_Hardening.rst** [P0]
    - Secure boot for automotive ECUs
    - Memory protection (MPU/MMU)
    - Code integrity verification
    - Debug port disabling/locking
    - Secure key storage in ECUs
    - AUTOSAR security modules (CSM, CryIf, Crypto)
    - HSM integration in automotive SoCs

24. 🟠 **Vehicle_Intrusion_Detection_Systems.rst** [P1]
    - HIDS (Host-based IDS) for ECUs
    - NIDS (Network-based IDS) for CAN/Ethernet
    - Anomaly detection algorithms
    - Signature-based detection
    - Machine learning for vehicle IDS
    - Response actions: logging, alerting, isolation
    - Commercial IDS solutions (Argus, Karamba, GuardKnox)

25. 🟡 **Automotive_Gateway_Security.rst** [P2]
    - Central gateway architecture
    - Firewall rules for vehicle networks
    - CAN to Ethernet translation security
    - Zone-based vehicle architecture
    - Gateway hardening techniques

════════════════════════════════════════════════════════════════════════════

✈️ **AVIONICS CYBERSECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**Standards & Airworthiness (4 cheatsheets)**

26. 🔴 **DO_326A_Airworthiness_Security_Process.rst** [P0]
    - Airworthiness security process overview
    - Security lifecycle phases
    - Security assurance levels (SAL 0-3)
    - Security plan development
    - Security environment and threat identification
    - Security objectives and requirements
    - Integration with DO-178C (software) and DO-254 (hardware)
    - Certification evidence and artifacts

27. 🟠 **DO_356A_Airworthiness_Security_Methods.rst** [P1]
    - Security analysis methods
    - Threat modeling for avionics
    - Security testing techniques
    - Vulnerability assessment
    - Security configuration management
    - Secure coding practices for avionics
    - Security verification methods

28. 🟡 **DO_355_Continuing_Airworthiness_Security.rst** [P2]
    - Post-certification security monitoring
    - Vulnerability management in fielded aircraft
    - Security incident response
    - Security updates and patches
    - Continuing airworthiness security plan
    - Threat intelligence integration

29. 🟡 **SAL_Levels_and_Determination.rst** [P2]
    - SAL 0: No security requirements
    - SAL 1: Basic security
    - SAL 2: Moderate security
    - SAL 3: High security (catastrophic impact)
    - SAL determination methodology
    - Mapping SAL to safety DAL
    - Security objectives per SAL level

**Avionics-Specific Threats (3 cheatsheets)**

30. 🟠 **IUEI_Intentional_Unauthorized_Electronic_Interaction.rst** [P1]
    - IUEI definition and scope
    - Attack vectors: wireless, wired, physical
    - Remote access threats
    - Malware in avionics systems
    - Countermeasures and mitigations
    - IUEI assessment process

31. 🟡 **Avionics_Data_Loading_Security.rst** [P2]
    - ARINC 615/615A data loading
    - Software load authentication
    - Load verification procedures
    - Secure transfer mechanisms
    - Portable media security (USB, SD cards)

32. 🟢 **Avionics_Bus_Security.rst** [P3]
    - ARINC 429 security considerations
    - MIL-STD-1553 vulnerabilities
    - AFDX (ARINC 664) security
    - Avionics Full-Duplex Switched Ethernet
    - Bus monitoring and intrusion detection

════════════════════════════════════════════════════════════════════════════

🏢 **BUILDING AUTOMATION CYBERSECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**Protocols & Standards (4 cheatsheets)**

33. 🔴 **BACnet_Security.rst** [P0]
    - BACnet protocol overview
    - BACnet/IP vulnerabilities (plaintext by default)
    - BACnet/SC (Secure Connect) with TLS 1.3
    - WebSocket security for BACnet
    - Certificate management
    - Authentication and authorization
    - Migration from legacy BACnet/IP to BACnet/SC
    - ASHRAE standards (135, Addendum 135-2016bj)

34. 🟠 **KNX_Security.rst** [P1]
    - KNX protocol fundamentals
    - KNX Data Secure (AES-128 CCM)
    - KNX IP Secure (TLS for IP tunneling)
    - Key management and commissioning
    - Security modes (legacy vs secure)
    - KNX security best practices

35. 🟡 **Modbus_Security_in_Buildings.rst** [P2]
    - Modbus/TCP vulnerabilities
    - Modbus security add-ons (TLS wrapper)
    - Authentication mechanisms
    - Network segmentation for Modbus
    - Firewall rules

36. 🟢 **LonWorks_and_Legacy_Protocol_Security.rst** [P3]
    - LonWorks/LonTalk security
    - Legacy BAS protocol hardening
    - Protocol gateway security
    - Retrofitting security in old buildings

**Building IoT & Systems (3 cheatsheets)**

37. 🟠 **HVAC_System_Security.rst** [P1]
    - HVAC control vulnerabilities
    - Chiller, boiler, AHU security
    - Temperature manipulation attacks
    - Energy theft prevention
    - Remote access security for HVAC technicians

38. 🟡 **Access_Control_and_Physical_Security_Integration.rst** [P2]
    - Electronic access control systems (EACS)
    - Badge readers and biometric systems
    - Integration with IT networks
    - Physical + cyber security convergence
    - Tailgating and social engineering

39. 🟡 **Smart_Building_IoT_Security.rst** [P2]
    - IoT sensors and actuators
    - Lighting control security (DALI, 0-10V)
    - Occupancy sensors and privacy
    - Building management system (BMS) security
    - Cloud integration security

════════════════════════════════════════════════════════════════════════════

🏭 **INDUSTRIAL AUTOMATION (ICS/OT) CYBERSECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**IEC 62443 Standard (6 cheatsheets)**

40. 🔴 **IEC_62443_Overview.rst** [P0]
    - Standard family structure (1-x, 2-x, 3-x, 4-x)
    - IACS (Industrial Automation & Control Systems)
    - Security lifecycle overview
    - Roles: asset owner, system integrator, product supplier
    - Shared responsibility model
    - Relationship to other standards (ISO 27001, NIST CSF)

41. 🔴 **IEC_62443_Security_Levels.rst** [P0]
    - SL-T (Target Security Level) determination
    - SL-A (Achieved Security Level) assessment
    - SL-C (Component Capability Security Level) rating
    - Security Level 1-4 threat profiles
    - Risk-based SL determination
    - SL gap analysis

42. 🔴 **IEC_62443_Zones_and_Conduits.rst** [P0]
    - Zone definition and boundaries
    - Conduit as secure communication path
    - Zone risk analysis
    - Conduit security requirements
    - Implementation examples (VLANs, firewalls, encryption)
    - Zone/conduit diagrams

43. 🟠 **IEC_62443_4_1_Secure_Development_Lifecycle.rst** [P1]
    - Security requirements specification
    - Secure-by-design principles
    - Security testing and validation
    - Vulnerability handling process
    - Security patch management
    - Product supplier security documentation

44. 🟠 **IEC_62443_4_2_Component_Requirements.rst** [P1]
    - Foundation requirements (FR 1-7)
    - System requirements (SR 1.1 - 7.8)
    - Component authentication
    - Access control and authorization
    - Data integrity and confidentiality
    - Resource availability
    - Restricted data flow

45. 🟡 **IEC_62443_3_3_System_Requirements.rst** [P2]
    - System-level security requirements
    - Security capabilities per SL
    - Access control at system level
    - Security monitoring and logging
    - Backup and restore security

**Industrial Protocols (5 cheatsheets)**

46. 🔴 **OPC_UA_Security.rst** [P0]
    - OPC UA architecture and profiles
    - Security modes: None, Sign, Sign & Encrypt
    - Certificate-based authentication
    - User authentication (username/password, X.509)
    - Application instance certificates
    - Secure Channel establishment
    - GDS (Global Discovery Server) for key management
    - OPC UA for TSN (Time-Sensitive Networking)

47. 🟠 **Modbus_TCP_Security.rst** [P1]
    - Modbus/TCP vulnerabilities (no authentication)
    - TLS wrapper for Modbus
    - Firewall rules for Modbus
    - Modbus security gateway
    - Protocol whitelisting

48. 🟠 **PROFINET_Security.rst** [P1]
    - PROFINET I/O and IRT (Isochronous Real-Time)
    - PROFINET Security (PN Security)
    - Authentication and encryption
    - Integration with industrial firewalls
    - Siemens security hardening guides

49. 🟡 **EtherNet_IP_Security.rst** [P2]
    - CIP (Common Industrial Protocol) over Ethernet
    - CIP Security specification
    - Authentication and encryption
    - Rockwell Automation security features

50. 🟢 **DNP3_and_Power_Grid_Protocols.rst** [P3]
    - DNP3 protocol overview
    - DNP3 Secure Authentication (SAv5, SAv6)
    - IEC 60870-5-104 security
    - IEC 61850 MMS security
    - SCADA security best practices

**ICS Architecture & Operations (4 cheatsheets)**

51. 🔴 **Purdue_Model_and_Industrial_Network_Architecture.rst** [P0]
    - Purdue Enterprise Reference Architecture (PERA)
    - Levels 0-5 detailed explanation
    - Air gap vs secure connectivity
    - DMZ and data diodes
    - Industrial firewall placement
    - Remote access architecture

52. 🟠 **OT_IT_Convergence_Security.rst** [P1]
    - Differences between OT and IT security
    - Availability > Confidentiality in OT
    - Integration challenges and solutions
    - Secure remote access for OT
    - Network segmentation strategies
    - SOC (Security Operations Center) for OT

53. 🟡 **SCADA_Security.rst** [P2]
    - SCADA architecture and components
    - HMI (Human-Machine Interface) security
    - RTU (Remote Terminal Unit) hardening
    - Historian security
    - SCADA protocol security (DNP3, Modbus, proprietary)

54. 🟡 **PLC_Security.rst** [P2]
    - Programmable Logic Controller fundamentals
    - PLC vulnerabilities and exploits
    - Ladder logic security
    - PLC hardening techniques
    - Secure programming practices
    - PLC authentication and access control

**ICS Threats & Incidents (2 cheatsheets)**

55. 🟠 **ICS_Threat_Landscape.rst** [P1]
    - Stuxnet case study (Iran nuclear, 2010)
    - Industroyer/Crashover (Ukraine power grid, 2016)
    - Triton/Trisis (Saudi Aramco SIS, 2017)
    - WannaCry/NotPetya impact on OT
    - Ransomware in manufacturing
    - Nation-state vs cybercriminal threats

56. 🟡 **ICS_Incident_Response.rst** [P2]
    - Incident detection in OT environments
    - Containment strategies (can't just reboot!)
    - Forensics for industrial systems
    - Recovery and restoration
    - Lessons learned and process improvement

════════════════════════════════════════════════════════════════════════════

🏥 **MEDICAL DEVICE CYBERSECURITY CHEATSHEETS**
─────────────────────────────────────────────────────────────────────────

**Regulations & Standards (5 cheatsheets)**

57. 🔴 **FDA_Cybersecurity_Premarket_Guidance.rst** [P0]
    - FDA 2023 Premarket Guidance overview
    - Cybersecurity requirements for 510(k), PMA, De Novo
    - Security risk management plan
    - Software Bill of Materials (SBOM) requirements
    - Threat modeling and TARA for medical devices
    - Security architecture documentation
    - Security testing and validation
    - Premarket submission checklist

58. 🔴 **FDA_Cybersecurity_Postmarket_Guidance.rst** [P0]
    - Postmarket vulnerability management
    - Coordinated vulnerability disclosure (CVD)
    - Security patch process (90-day timeline)
    - Medical Device Safety Action Plans
    - Communication with stakeholders
    - Incident response for medical devices
    - Legacy device handling

59. 🟠 **Section_524B_FD&C_Act.rst** [P1]
    - Cyber device definition
    - Enhanced cybersecurity requirements
    - Mandatory SBOM for cyber devices
    - Post-market monitoring obligations
    - FDA enforcement and compliance

60. 🟠 **IEC_81001_5_1_Health_Software_Security.rst** [P1]
    - Health software security lifecycle
    - Threat modeling for health IT
    - Security risk management
    - Integration with IEC 62304 (software lifecycle)
    - Networked medical device considerations

61. 🟡 **ISO_14971_Risk_Management_and_Cybersecurity.rst** [P2]
    - Medical device risk management overview
    - Cybersecurity risk as safety risk
    - Residual risk evaluation
    - Risk-benefit analysis
    - Post-production information and risk monitoring

**Medical Device Security (5 cheatsheets)**

62. 🔴 **SBOM_for_Medical_Devices.rst** [P0]
    - SBOM formats: CycloneDX, SPDX
    - Component identification and versioning
    - Vulnerability tracking (CVE, NVD)
    - SOUP (Software of Unknown Provenance) management
    - Open-source license compliance
    - SBOM generation tools
    - SBOM maintenance and updates

63. 🟠 **Infusion_Pump_Security.rst** [P1]
    - Infusion pump vulnerabilities
    - Wireless communication security (Bluetooth, Wi-Fi)
    - Dosing manipulation attacks
    - Authentication for clinician access
    - Drug library security
    - FDA guidance specific to pumps

64. 🟡 **Implantable_Device_Security.rst** [P2]
    - Pacemaker and ICD security
    - Short-range wireless attacks (MICS band)
    - Battery depletion attacks
    - Firmware update security
    - Emergency access mechanisms
    - Privacy considerations

65. 🟡 **Diagnostic_Equipment_Security.rst** [P2]
    - CT, MRI, X-ray machine vulnerabilities
    - Medical imaging (DICOM) security
    - Lab equipment (blood analyzers, sequencers)
    - Result manipulation attacks
    - Network isolation strategies

66. 🟢 **Wearable_and_Consumer_Medical_Security.rst** [P3]
    - Fitness trackers and health monitors
    - Continuous glucose monitors (CGM)
    - Mobile health apps (mHealth)
    - Data privacy (HIPAA compliance)
    - Bluetooth Low Energy security

**Healthcare IT Integration (2 cheatsheets)**

67. 🟠 **Medical_Device_Network_Security.rst** [P1]
    - Hospital network architecture
    - Medical device VLAN segmentation
    - Network access control (NAC) for devices
    - Wireless security for medical devices
    - Remote monitoring security
    - Telemedicine security

68. 🟡 **HIPAA_and_Cybersecurity.rst** [P2]
    - HIPAA Security Rule overview
    - Administrative, physical, technical safeguards
    - Medical device data protection
    - Breach notification requirements
    - Business associate agreements (BAA)

════════════════════════════════════════════════════════════════════════════

🌐 **CROSS-CUTTING & EMERGING TOPICS**
─────────────────────────────────────────────────────────────────────────

**Advanced Security Topics (5 cheatsheets)**

69. 🟠 **Post_Quantum_Cryptography_for_Embedded.rst** [P1]
    - Quantum computing threat to current crypto
    - NIST PQC selected algorithms:
      - Kyber (key encapsulation)
      - Dilithium (digital signatures)
      - Falcon, SPHINCS+ (alternate signatures)
    - Migration strategies for embedded systems
    - Hybrid classical/PQC approaches
    - Performance considerations (large key sizes)

70. 🟡 **AI_ML_Security_in_Embedded_Systems.rst** [P2]
    - Adversarial machine learning attacks
    - Model poisoning and backdoors
    - Evasion attacks on neural networks
    - Privacy-preserving ML (federated learning)
    - Secure inference on edge devices
    - TinyML security considerations

71. 🟡 **Blockchain_and_Distributed_Ledger_in_Embedded.rst** [P2]
    - Blockchain for supply chain verification
    - Distributed trust in IoT networks
    - Lightweight blockchain protocols
    - Smart contracts for embedded systems
    - Energy constraints and proof-of-work alternatives

72. 🟡 **5G_and_Edge_Computing_Security.rst** [P2]
    - 5G security architecture (3GPP)
    - Network slicing security
    - Multi-access edge computing (MEC) threats
    - Low-latency security challenges
    - 5G in automotive, industrial IoT

73. 🟢 **Quantum_Random_Number_Generation.rst** [P3]
    - QRNG principles
    - True random vs pseudo-random
    - Entropy sources for embedded systems
    - Hardware RNG integration

**Industry Trends & Best Practices (3 cheatsheets)**

74. 🟠 **Zero_Trust_Architecture_for_Embedded.rst** [P1]
    - Zero-trust principles adapted for embedded/OT
    - Micro-segmentation in embedded networks
    - Continuous authentication and authorization
    - Policy-based access control
    - Challenges in resource-constrained systems

75. 🟡 **DevSecOps_for_Embedded_Systems.rst** [P2]
    - Security in CI/CD pipelines
    - Automated security testing (SAST, DAST, IAST)
    - Container security for embedded Linux
    - Secrets management in build systems
    - Security scanning for firmware images

76. 🟡 **Cyber_Insurance_and_Risk_Transfer.rst** [P2]
    - Cyber insurance market for OT/embedded
    - Risk quantification and assessment
    - Insurance policy requirements
    - Incident response planning
    - Cost-benefit analysis

════════════════════════════════════════════════════════════════════════════

📊 **SUMMARY & STATISTICS**
─────────────────────────────────────────────────────────────────────────

**Total Cheatsheets Identified:** 76

**By Priority:**
- 🔴 P0 (Critical): 18 cheatsheets (24%)
- 🟠 P1 (High): 24 cheatsheets (32%)
- 🟡 P2 (Medium): 26 cheatsheets (34%)
- 🟢 P3 (Low): 8 cheatsheets (10%)

**By Domain:**
- 🔐 General Embedded: 13 cheatsheets
- 🚗 Automotive: 12 cheatsheets
- ✈️ Avionics: 7 cheatsheets
- 🏢 Building Automation: 7 cheatsheets
- 🏭 Industrial (ICS/OT): 17 cheatsheets
- 🏥 Medical Devices: 12 cheatsheets
- 🌐 Cross-cutting/Emerging: 8 cheatsheets

**Recommended Development Sequence:**

**Phase 1 (Foundation)** — 6-8 weeks
1. Root_of_Trust_and_Secure_Boot
2. Trusted_Execution_Environments
3. Hardware_Security_Module_HSM
4. Threat_Modeling_for_Embedded_Systems
5. Cryptography_for_Embedded_Systems
6. Secure_Firmware_Updates_OTA

**Phase 2 (Domain Standards)** — 8-10 weeks
7. ISO_SAE_21434_Automotive_Cybersecurity
8. UN_R155_R156_CSMS_SUMS
9. IEC_62443_Overview
10. IEC_62443_Security_Levels
11. IEC_62443_Zones_and_Conduits
12. DO_326A_Airworthiness_Security_Process
13. FDA_Cybersecurity_Premarket_Guidance
14. FDA_Cybersecurity_Postmarket_Guidance
15. BACnet_Security

**Phase 3 (Domain Deep Dives)** — 10-12 weeks
16-30: Automotive networks (CAN, Ethernet, V2X)
31-40: Industrial protocols (OPC UA, Modbus, PROFINET)
41-50: Medical devices (SBOM, infusion pumps)
51-60: Avionics & building automation

**Phase 4 (Advanced & Emerging)** — 6-8 weeks
61-76: Post-quantum crypto, AI/ML security, zero-trust

════════════════════════════════════════════════════════════════════════════

🎯 **USAGE GUIDE**
─────────────────────────────────────────────────────────────────────────

**For Learning:**
- Start with P0 cheatsheets for foundational knowledge
- Follow domain-specific paths based on your industry
- Use cross-references between related cheatsheets

**For Teaching:**
- Use as curriculum planning tool
- Assign priority-based reading order
- Combine related cheatsheets into course modules

**For Organizations:**
- Map cheatsheets to job roles and responsibilities
- Create custom learning paths for teams
- Track coverage against regulatory requirements

**For Certification Prep:**
- CISSP: Focus on General + ICS + Medical
- GICSP (ICS Security): Industrial automation section
- Automotive: ISO 21434 + UN R155/R156 + automotive deep dives
- Medical: FDA + IEC + medical device security

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Status:** Planning complete, ready for development prioritization  
**Estimated total content:** ~60,000+ lines across all 76 cheatsheets
