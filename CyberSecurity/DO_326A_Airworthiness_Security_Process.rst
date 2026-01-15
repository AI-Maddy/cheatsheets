✈️ **DO-326A / ED-202A — AIRWORTHINESS SECURITY PROCESS**
═══════════════════════════════════════════════════════════════════════

**Security Process Specification for Airborne Systems and Equipment**  
**Purpose:** Aviation cybersecurity 🔐 | Type certification 📜 | Threat mitigation 🛡️  
**Authority:** FAA (DO-326A) | EASA (ED-202A) | RTCA/EUROCAE | Mandatory for certification

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**DO-326A** defines the **airworthiness security process** for civil aircraft. It establishes Security Assurance Levels (SAL 0-3), security lifecycle phases, and certification evidence requirements. Think of it as "DO-178C for cybersecurity" — it doesn't tell you HOW to implement security, but WHAT process to follow to achieve certification.

**Key Equation:** `Threat Model + Security Objectives → Security Requirements → Implementation → Verification = SAL Achievement`

**Real-World Impact:** Required for **all new aircraft types** with electronic systems and connectivity (e.g., Boeing 787, Airbus A350). Prevents intentional unauthorized electronic interaction (IUEI) — cyberattacks on aircraft systems. Integrated with DO-178C (software) and DO-254 (hardware).

**Publication:** DO-326A (2014), ED-202A (EASA equivalent, 2014)

════════════════════════════════════════════════════════════════════════════

🎯 **STANDARD OVERVIEW**
─────────────────────────────────────────────────────────────────────────

**Purpose & Scope:**

DO-326A addresses **intentional unauthorized electronic interaction (IUEI)** — cyber threats to airborne systems. It complements existing airworthiness standards:

| Standard | Focus | Security Integration |
|:---------|:------|:---------------------|
| **DO-178C** | Software development | + DO-326A = Secure software |
| **DO-254** | Hardware design | + DO-326A = Secure hardware |
| **ARP4754A** | System development | + DO-326A = Secure systems |
| **DO-326A** | **Security process** | **Applies to all above** |

**Key Definitions:**

- **🔴 IUEI (Intentional Unauthorized Electronic Interaction):** Deliberate attempts to gain unauthorized access or cause unintended behavior via electronic means
- **🎚️ SAL (Security Assurance Level):** 0-3, similar to DAL (Design Assurance Level) in safety
- **🛡️ Security Objectives:** High-level security goals derived from threat analysis
- **📋 Security Requirements:** Specific technical requirements to achieve objectives
- **✅ Security Assurance:** Evidence that security objectives are met

**Relationship with Other Standards:**

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARP4754A (System)                           │
│                   System Safety Process                          │
└────────┬─────────────────────────────────────────────┬──────────┘
         │                                             │
    ┌────▼────────┐                              ┌────▼──────────┐
    │  DO-178C    │                              │   DO-254      │
    │  Software   │                              │   Hardware    │
    └────┬────────┘                              └────┬──────────┘
         │                                             │
         └──────────────────┬──────────────────────────┘
                            │
                   ┌────────▼────────┐
                   │    DO-326A      │
                   │ Security Process │
                   │ (Overlays all)   │
                   └──────────────────┘
```

════════════════════════════════════════════════════════════════════════════

🎚️ **SECURITY ASSURANCE LEVELS (SAL)**
─────────────────────────────────────────────────────────────────────────

**SAL Determination:**

SAL is determined based on the **potential impact** of a successful cyberattack:

| SAL | Impact if Compromised | Aircraft Effect Example | Security Process Rigor |
|:----|:----------------------|:------------------------|:-----------------------|
| **SAL 0** | No safety or security impact | Passenger entertainment (isolated) | None |
| **SAL 1** | Minor impact | Flight information display | Basic |
| **SAL 2** | Major impact | Weather radar, TCAS | Moderate |
| **SAL 3** | Hazardous/catastrophic impact | Flight control, engine control, braking | Rigorous (≈ DAL A) |

**SAL Assignment Process:**

.. code-block:: text

   1. Identify System/Equipment
      ↓
   2. Analyze Connectivity (wireless, wired, removable media)
      ↓
   3. Threat Modeling (What could attacker do?)
      ↓
   4. Safety Impact Assessment (FHA, PSSA from ARP4754A)
      ↓
   5. Determine SAL (based on worst-case impact)
      ↓
   6. Apply DO-326A Process per SAL

**Example SAL Assignment:**

**System:** Flight Management System (FMS)
- **Connectivity:** ARINC 429, datalink (ACARS), USB ports
- **Threat:** Attacker sends malicious route via datalink
- **Impact:** Could cause navigation errors → Hazardous (crew workload, potential CFIT)
- **SAL Assignment:** **SAL 3** (Hazardous impact)

**System:** In-Flight Entertainment (IFE)
- **Connectivity:** Wi-Fi, USB, Ethernet
- **Threat:** Passenger exploits IFE to access avionics (if improperly segregated)
- **Impact:** If isolated properly → No impact; If not isolated → Catastrophic
- **SAL Assignment:** 
  - IFE itself: **SAL 0** (no safety impact)
  - Network isolation: **SAL 3** (prevents catastrophic propagation)

════════════════════════════════════════════════════════════════════════════

🔄 **SECURITY LIFECYCLE PROCESS**
─────────────────────────────────────────────────────────────────────────

DO-326A defines a security lifecycle parallel to the safety lifecycle:

**Phase 1: Security Planning**

Establish security program for the project:

.. code-block:: text

   Security Plan Contents:
   ✓ Security organization (roles, responsibilities)
   ✓ Security development process
   ✓ Security verification process
   ✓ Security configuration management
   ✓ Security assurance process
   ✓ Certification liaison plan

**Example Security Plan Excerpt:**

.. code-block:: text

   SYSTEM: Next-Generation Flight Control Computer (FCC)
   SAL: 3 (Catastrophic impact if compromised)
   
   Security Organization:
   - Security Manager: J. Smith (reports to Chief Engineer)
   - Security Architects: A. Lee, B. Chen
   - Security Verification Lead: C. Davis
   - Independent Security Assessor: External firm (TBD)
   
   Security Development Process:
   - Threat modeling: STRIDE methodology
   - Secure coding: CERT C, MISRA C with security extensions
   - Cryptography: FIPS 140-2 validated modules
   - Key management: Hardware Security Module (HSM)
   
   Security Verification:
   - Penetration testing: External red team
   - Fuzzing: AFL++, Honggfuzz on all interfaces
   - Static analysis: Coverity, Klocwork
   - Formal verification: SPARK for critical functions

**Phase 2: Security Environment & Threat Identification**

Analyze system environment and potential threats:

**Security Environment Analysis:**

.. code-block:: python

   # Threat Modeling for Avionics System
   
   class AvionicsSystem:
       def __init__(self, name, sal):
           self.name = name
           self.sal = sal
           self.connectivity = []
           self.threats = []
   
   # Example: Flight Management System
   fms = AvionicsSystem("FMS", sal=3)
   
   # Identify connectivity (attack surfaces)
   fms.connectivity = [
       {"interface": "ARINC 429", "exposure": "Internal avionics bus"},
       {"interface": "ACARS Datalink", "exposure": "Air-to-ground radio"},
       {"interface": "USB Port", "exposure": "Maintenance access"},
       {"interface": "ARINC 664 (AFDX)", "exposure": "Avionics Ethernet"}
   ]
   
   # Threat identification using STRIDE
   fms.threats = [
       {
           "id": "T-001",
           "type": "Spoofing",
           "description": "Attacker sends forged ACARS messages",
           "impact": "Hazardous - incorrect route data",
           "likelihood": "Remote",
           "mitigation": "Message authentication (HMAC)"
       },
       {
           "id": "T-002",
           "type": "Tampering",
           "description": "Malicious USB device injects code",
           "impact": "Catastrophic - arbitrary code execution",
           "likelihood": "Probable" if no_usb_protection else "Remote",
           "mitigation": "USB disable in flight mode, secure boot"
       },
       {
           "id": "T-003",
           "type": "Denial of Service",
           "description": "Flood AFDX network with packets",
           "impact": "Major - FMS loses sensor data",
           "likelihood": "Remote",
           "mitigation": "Rate limiting, traffic policing"
       }
   ]

**Phase 3: Security Objectives & Requirements**

Derive security objectives from threats, then decompose into requirements:

**Security Objectives (High-Level):**

- **SO-1:** Prevent unauthorized modification of flight plan data
- **SO-2:** Ensure authenticity of received navigation updates
- **SO-3:** Maintain availability of FMS during flight operations
- **SO-4:** Detect and log security-relevant events

**Security Requirements (Specific):**

.. code-block:: text

   From SO-1 (Prevent unauthorized modification):
   ├─ SR-1.1: All flight plan data shall be protected by cryptographic integrity checks
   ├─ SR-1.2: Memory containing flight plan shall be write-protected after validation
   ├─ SR-1.3: Only authenticated pilot inputs shall modify active flight plan
   └─ SR-1.4: Maintenance mode access shall require dual-factor authentication
   
   From SO-2 (Ensure authenticity):
   ├─ SR-2.1: All ACARS messages shall be authenticated using HMAC-SHA256
   ├─ SR-2.2: Navigation database updates shall be digitally signed (ECDSA)
   ├─ SR-2.3: Invalid signatures shall be rejected and logged
   └─ SR-2.4: Public keys for verification shall be stored in immutable memory
   
   From SO-3 (Maintain availability):
   ├─ SR-3.1: System shall continue operation if security threat detected
   ├─ SR-3.2: Rate limiting applied to all external inputs (1000 msgs/sec max)
   ├─ SR-3.3: Redundant processing channels isolated from each other
   └─ SR-3.4: Watchdog timer detects and recovers from DoS conditions

**Phase 4: Security Implementation**

Implement security requirements using appropriate technologies:

.. code-block:: c

   // Example: ACARS Message Authentication (SR-2.1)
   #include <stdint.h>
   #include <string.h>
   #include "crypto/hmac_sha256.h"
   
   #define ACARS_KEY_SIZE 32
   #define HMAC_SIZE 32
   
   // Stored in secure OTP memory (DO-326A SAL 3)
   static const uint8_t acars_key[ACARS_KEY_SIZE] = {
       /* Provisioned during aircraft manufacturing */
   };
   
   typedef struct {
       char msg_id[8];
       char content[220];
       uint8_t hmac[HMAC_SIZE];
   } AcarsMessage;
   
   // Verify ACARS message authenticity
   bool verify_acars_message(const AcarsMessage *msg) {
       uint8_t calculated_hmac[HMAC_SIZE];
       
       // Calculate HMAC over msg_id + content
       hmac_sha256(
           acars_key, ACARS_KEY_SIZE,
           (uint8_t *)msg, sizeof(msg->msg_id) + sizeof(msg->content),
           calculated_hmac
       );
       
       // Constant-time comparison (prevent timing attacks)
       bool valid = constant_time_compare(
           calculated_hmac, 
           msg->hmac, 
           HMAC_SIZE
       );
       
       // Log security event (SR-2.3)
       if (!valid) {
           log_security_event(
               SEC_EVENT_ACARS_AUTH_FAIL,
               msg->msg_id,
               SEVERITY_HIGH
           );
       }
       
       return valid;
   }
   
   // Constant-time comparison (prevent side-channel attacks)
   bool constant_time_compare(const uint8_t *a, const uint8_t *b, size_t len) {
       uint8_t result = 0;
       for (size_t i = 0; i < len; i++) {
           result |= a[i] ^ b[i];
       }
       return (result == 0);
   }

**Phase 5: Security Verification**

Verify that security requirements are met:

**Verification Methods:**

| Method | SAL 1 | SAL 2 | SAL 3 | Example |
|:-------|:------|:------|:------|:--------|
| **Security Review** | ✅ | ✅ | ✅ | Architecture review |
| **Security Analysis** | ✅ | ✅ | ✅ | Threat model validation |
| **Security Testing** | ✅ | ✅ | ✅ | Penetration testing |
| **Formal Methods** | - | Recommended | ✅ | Cryptographic protocol verification |
| **Independent Assessment** | - | - | ✅ | Third-party security audit |

**Example Verification Plan:**

.. code-block:: text

   Security Requirement: SR-2.1 (ACARS message authentication)
   
   Verification Activities:
   ✓ Security Review: Cryptographic design review (HMAC-SHA256 appropriate?)
   ✓ Security Analysis: Key management analysis (secure storage verified)
   ✓ Security Testing:
     - Positive test: Valid HMAC accepted
     - Negative test: Invalid HMAC rejected
     - Fuzzing: Random HMAC values rejected
     - Timing attack: Verification time constant regardless of HMAC value
   ✓ Formal Verification: SPARK proof that constant_time_compare is truly constant-time
   ✓ Independent Assessment: External penetration test (attempt to forge messages)

**Phase 6: Security Configuration Management**

Control changes to security-relevant items:

- Version control for security architecture documents
- Change impact analysis for security requirements
- Regression testing after security patches

**Phase 7: Security Assurance**

Demonstrate to certification authority that security objectives are met:

.. code-block:: text

   Security Assurance Case (SAL 3 Example):
   
   Claim: FMS is protected against IUEI with SAL 3 assurance
   
   Evidence:
   ├─ E1: Security Plan (PSAC - Plan for Security Aspects of Certification)
   ├─ E2: Threat Model (identifies all attack vectors)
   ├─ E3: Security Requirements Trace (objectives → requirements → implementation)
   ├─ E4: Secure Design Documentation (architecture diagrams, data flow)
   ├─ E5: Security Verification Results (test reports, penetration test results)
   ├─ E6: Independent Security Assessment Report
   ├─ E7: Configuration Management Records
   └─ E8: Security Accomplishment Summary (SAS)

════════════════════════════════════════════════════════════════════════════

🔗 **INTEGRATION WITH DO-178C & DO-254**
─────────────────────────────────────────────────────────────────────────

**DO-178C Software Security Integration:**

.. code-block:: text

   DO-178C Objective          DO-326A Security Enhancement
   ────────────────────────   ─────────────────────────────────
   Software Requirements      + Security Requirements
   Software Design            + Security Architecture
   Software Coding            + Secure Coding Standards (CERT C)
   Software Testing           + Security Testing (fuzzing, penetration)
   Verification Process       + Security Verification
   Configuration Management   + Security CM (control security changes)
   Quality Assurance          + Security Assurance

**Combined DAL/SAL Matrix:**

| System | DAL | SAL | Rationale |
|:-------|:----|:----|:----------|
| Flight Control | A | 3 | Catastrophic safety + security impact |
| Engine Control | A | 3 | Catastrophic safety + security impact |
| FMS | A | 3 | Hazardous if compromised |
| Weather Radar | C | 2 | Major safety + security impact |
| IFE (isolated) | E | 0 | No safety impact, isolated |

**Security Requirements in DO-178C Process:**

.. code-block:: c

   /* DO-178C + DO-326A Combined Requirements */
   
   // Safety Requirement (DO-178C): Shall detect sensor failure within 100ms
   // Security Requirement (DO-326A): Shall authenticate sensor data
   
   typedef struct {
       float altitude;
       float airspeed;
       uint32_t timestamp;
       uint8_t signature[64];  // ECDSA signature (DO-326A)
   } SensorData;
   
   bool process_sensor_data(SensorData *data) {
       // Security check (DO-326A SAL 3)
       if (!verify_sensor_signature(data)) {
           log_security_event(SEC_EVENT_SENSOR_AUTH_FAIL);
           return false;  // Reject unauthenticated data
       }
       
       // Safety check (DO-178C DAL A)
       if (!validate_sensor_range(data)) {
           trigger_sensor_fault_flag();
           return false;
       }
       
       // Both security and safety checks passed
       update_flight_control(data);
       return true;
   }

**DO-254 Hardware Security Integration:**

- Secure boot implementation in FPGAs
- Hardware RoT (Root of Trust) for secure storage
- Anti-tamper mechanisms (voltage/temperature sensors)
- Cryptographic accelerators (AES, SHA, ECDSA)

════════════════════════════════════════════════════════════════════════════

🛡️ **THREAT EXAMPLES & MITIGATIONS**
─────────────────────────────────────────────────────────────────────────

**Threat 1: Malicious Software Loading**

**Scenario:** Attacker loads malicious software via USB during maintenance

**Mitigation:**
- Secure boot (verify software signature before execution)
- Dual-person integrity checks during maintenance
- Audit logging of all software loads

.. code-block:: c

   // Secure software loading per DO-326A
   bool load_software_update(const char *file_path) {
       SoftwarePackage pkg;
       
       // 1. Read software package
       if (!read_package(file_path, &pkg)) {
           return false;
       }
       
       // 2. Verify digital signature (ECDSA-P384)
       if (!verify_signature_ecdsa384(pkg.data, pkg.size, pkg.signature)) {
           log_security_event(SEC_EVENT_SW_LOAD_AUTH_FAIL);
           return false;
       }
       
       // 3. Check anti-rollback (prevent downgrade attacks)
       if (pkg.version < get_current_version()) {
           log_security_event(SEC_EVENT_SW_ROLLBACK_ATTEMPT);
           return false;
       }
       
       // 4. Write to backup partition
       write_to_backup_partition(pkg.data, pkg.size);
       
       // 5. Require reboot for activation
       schedule_reboot();
       
       return true;
   }

**Threat 2: Wireless Network Intrusion**

**Scenario:** Attacker exploits Wi-Fi vulnerability to access avionics network

**Mitigation:**
- Network segregation (IFE isolated from avionics)
- Firewalls between network zones
- Intrusion detection systems

.. code-block:: text

   Aircraft Network Architecture (DO-326A Compliant):
   
   ┌────────────────────────────────────────────────────────────┐
   │                  Passenger Wi-Fi (Internet)                │
   │                       SAL 0                                │
   └─────────────────────┬──────────────────────────────────────┘
                         │ Firewall (no inbound traffic)
   ┌─────────────────────▼──────────────────────────────────────┐
   │          In-Flight Entertainment (IFE)                     │
   │          SAL 0 (isolated from avionics)                    │
   └─────────────────────┬──────────────────────────────────────┘
                         │ Air Gap / Data Diode (one-way)
   ┌─────────────────────▼──────────────────────────────────────┐
   │          Aircraft Information Network                      │
   │          SAL 1 (flight info, moving map)                   │
   └─────────────────────┬──────────────────────────────────────┘
                         │ Firewall + IDS
   ┌─────────────────────▼──────────────────────────────────────┐
   │          Control Domain (Avionics)                         │
   │          SAL 2-3 (FMS, flight control, engine)             │
   │          ❌ NO direct connection to IFE                    │
   └────────────────────────────────────────────────────────────┘

**Threat 3: Data Link Message Injection**

**Scenario:** Attacker transmits forged ADS-B or ACARS messages

**Mitigation:**
- Message authentication (HMAC or digital signatures)
- Anomaly detection (cross-check with other sensors)
- Pilot verification of critical changes

════════════════════════════════════════════════════════════════════════════

📋 **CERTIFICATION EVIDENCE**
─────────────────────────────────────────────────────────────────────────

**Required Documentation (SAL 3):**

1. **📘 PSAC (Plan for Security Aspects of Certification)**
   - Security plan equivalent of PSAC in DO-178C
   - Describes security process, organization, tools

2. **📗 Security Environment Analysis**
   - Connectivity analysis
   - Asset identification
   - Threat modeling results

3. **📙 Security Requirements Document**
   - Security objectives
   - Security requirements (traceable)
   - Requirements allocation

4. **📕 Security Architecture**
   - Block diagrams showing security boundaries
   - Data flow diagrams
   - Trust boundaries

5. **📓 Security Verification Report**
   - Test cases and results
   - Penetration test results
   - Independent assessment findings

6. **📔 SAS (Security Accomplishment Summary)**
   - Summary of compliance with DO-326A
   - Submitted to certification authority

**Example SAS Excerpt:**

.. code-block:: text

   SECURITY ACCOMPLISHMENT SUMMARY
   System: Flight Management System (FMS-3000)
   Applicant: Example Avionics Inc.
   SAL: 3
   
   1. Security Process Compliance
      ✓ Security plan established and followed (PSAC-2024-001)
      ✓ Security lifecycle activities completed per DO-326A
      ✓ Independent security assessment performed (Report ISA-2024-042)
   
   2. Security Environment
      ✓ Connectivity identified: ARINC 429, ACARS, USB, AFDX
      ✓ Threat model completed using STRIDE (TM-2024-007)
      ✓ 47 threats identified, all mitigated or accepted
   
   3. Security Assurance Evidence
      ✓ Security requirements: 127 total, all verified
      ✓ Security testing: 1,200+ test cases, 100% pass rate
      ✓ Penetration testing: 15 findings, all remediated
      ✓ Formal verification: Critical crypto functions proven correct
   
   4. Configuration Management
      ✓ Security baseline established
      ✓ All security-relevant changes tracked
      ✓ Problem reports: 12 security-related, all closed
   
   Conclusion: FMS-3000 meets DO-326A requirements for SAL 3

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: What is the relationship between SAL (Security Assurance Level) and DAL (Design Assurance Level)?**

**A1:**
- **DAL** (DO-178C) focuses on **safety** — preventing unintentional failures
- **SAL** (DO-326A) focuses on **security** — preventing intentional attacks
- They are **independent but related**:
  - High DAL system (e.g., flight control, DAL A) typically also needs high SAL (SAL 3) because compromise has catastrophic impact
  - Low DAL system (e.g., passenger entertainment, DAL E) may need SAL 0 if properly isolated, or SAL 3 if it's a gateway to critical systems
- **Key difference:** DAL = probability of failure, SAL = resistance to attacks

**Q2: What is IUEI and why does DO-326A focus on it?**

**A2:**
**IUEI (Intentional Unauthorized Electronic Interaction)** is deliberate cyberattack attempting to:
- Gain unauthorized access to aircraft systems
- Cause unintended behavior
- Disrupt operations

DO-326A focuses on IUEI because:
1. Traditional safety standards (DO-178C, ARP4754A) address **unintentional** failures
2. Cyber threats are **intentional** and adversarial
3. Modern aircraft have extensive connectivity (Wi-Fi, datalinks, USB) increasing attack surface
4. Safety analysis alone doesn't capture malicious intent

**Q3: Describe the DO-326A security lifecycle phases.**

**A3:**
1. **Security Planning** — Establish security program, define roles
2. **Security Environment & Threat Identification** — Analyze connectivity, identify threats
3. **Security Objectives & Requirements** — Derive security objectives from threats, decompose to requirements
4. **Security Implementation** — Implement security controls (crypto, authentication, isolation)
5. **Security Verification** — Test and verify security requirements met
6. **Security Configuration Management** — Control security-relevant changes
7. **Security Assurance** — Demonstrate compliance to certification authority

**Q4: How does network segregation support DO-326A compliance?**

**A4:**
Network segregation creates **security zones** with different SAL levels:
- **Passenger Network** (SAL 0) — Internet-facing, untrusted
- **IFE Network** (SAL 0) — Entertainment, isolated
- **Information Network** (SAL 1) — Flight information displays
- **Control Domain** (SAL 2-3) — Avionics, flight-critical

**Segregation mechanisms:**
- Firewalls between zones
- Data diodes (one-way communication)
- Air gaps (physical isolation)
- VLANs with access control

This limits **blast radius** — compromise of SAL 0 cannot propagate to SAL 3 systems.

**Q5: What cryptographic methods are typically used in DO-326A SAL 3 systems?**

**A5:**
SAL 3 requires strong cryptography:
- **Message Authentication:** HMAC-SHA256 or HMAC-SHA384 (for ACARS, sensor data)
- **Digital Signatures:** ECDSA-P256 or ECDSA-P384 (for software loading, navigation updates)
- **Encryption:** AES-256-GCM (if confidentiality needed, e.g., military)
- **Key Storage:** Hardware Security Module (HSM) or OTP fuses
- **Standards:** FIPS 140-2 Level 2+ validated cryptographic modules

**Rationale:** Catastrophic impact requires high assurance crypto resistant to sophisticated attacks.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
