✈️ **DO-356A / ED-203A — AIRWORTHINESS SECURITY METHODS**
═══════════════════════════════════════════════════════════════════════

**Security Methods and Considerations for Airborne Systems**  
**Purpose:** Security implementation guidance 🛠️ | Analysis techniques 🔍 | Verification methods ✅  
**Authority:** FAA (DO-356A) | EASA (ED-203A) | RTCA/EUROCAE | Companion to DO-326A

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**DO-356A** is the **"how-to" companion** to DO-326A (the "what" process). While DO-326A defines the security process, DO-356A provides **methods, techniques, and best practices** for implementing security in airborne systems. Think of it as the security engineering handbook for aviation.

**Key Relationship:** `DO-326A (Process) + DO-356A (Methods) = Complete Security Framework`

**Contents:** Threat modeling techniques, security analysis methods, cryptographic guidance, secure coding practices, testing approaches, and real-world examples specific to aviation.

**Publication:** DO-356A (2018), ED-203A (EASA equivalent, 2018)

════════════════════════════════════════════════════════════════════════════

🎯 **STANDARD OVERVIEW**
─────────────────────────────────────────────────────────────────────────

**Relationship with DO-326A:**

| DO-326A | DO-356A |
|:--------|:--------|
| **Process** standard | **Methods** standard |
| Defines "what" to do | Describes "how" to do it |
| SAL determination | Threat modeling techniques |
| Lifecycle phases | Analysis and design methods |
| Certification requirements | Implementation guidance |
| Mandatory for compliance | Recommended (but highly valuable) |

**Document Structure:**

```
DO-356A Contents:
├─ 1. Introduction & Scope
├─ 2. Security Concepts
│  ├─ Assets, Threats, Vulnerabilities
│  ├─ Attack Trees & Graphs
│  └─ Defense-in-Depth
├─ 3. Security Analysis Methods
│  ├─ Threat Modeling (STRIDE, PASTA, Attack Trees)
│  ├─ Vulnerability Assessment
│  ├─ Risk Analysis
│  └─ Security Architecture Review
├─ 4. Security Design Methods
│  ├─ Cryptographic Mechanisms
│  ├─ Authentication & Authorization
│  ├─ Network Segmentation
│  └─ Secure Protocols
├─ 5. Security Verification Methods
│  ├─ Security Testing
│  ├─ Penetration Testing
│  ├─ Fuzzing
│  └─ Code Review
└─ 6. Examples & Case Studies
```

════════════════════════════════════════════════════════════════════════════

🔍 **THREAT MODELING TECHNIQUES**
─────────────────────────────────────────────────────────────────────────

**STRIDE Methodology (Microsoft)**

STRIDE categorizes threats into six types:

| Category | Threat | Aviation Example | Mitigation |
|:---------|:-------|:-----------------|:-----------|
| **S**poofing | Impersonation | Forged ADS-B position | Digital signatures |
| **T**ampering | Data modification | Altered route in FMS | Integrity checks (HMAC) |
| **R**epudiation | Deny actions | Pilot denies command | Audit logs, digital signatures |
| **I**nformation Disclosure | Data leakage | Intercept flight plan | Encryption (AES-GCM) |
| **D**enial of Service | Availability attack | Flood ARINC 664 network | Rate limiting, filtering |
| **E**levation of Privilege | Gain higher access | Maintenance mode exploit | Authentication, least privilege |

**STRIDE Analysis Example:**

.. code-block:: python

   # STRIDE Analysis for Flight Management System (FMS)
   
   class ThreatModel:
       def __init__(self, system_name):
           self.system = system_name
           self.threats = []
       
       def add_threat(self, stride_type, description, impact, mitigation):
           self.threats.append({
               "type": stride_type,
               "description": description,
               "impact": impact,
               "mitigation": mitigation
           })
   
   # FMS Threat Model
   fms_threats = ThreatModel("Flight Management System")
   
   # Spoofing
   fms_threats.add_threat(
       "Spoofing",
       "Attacker sends forged ACARS message claiming to be ATC",
       "Hazardous - incorrect clearance could lead to traffic conflict",
       "Implement ACARS message authentication (HMAC-SHA256)"
   )
   
   # Tampering
   fms_threats.add_threat(
       "Tampering",
       "Malicious navigation database update alters waypoint coordinates",
       "Hazardous - aircraft could deviate from intended route",
       "Digital signature verification (ECDSA-P384) of nav database"
   )
   
   # Repudiation
   fms_threats.add_threat(
       "Repudiation",
       "Pilot claims they didn't enter route modification",
       "Minor - investigation difficulty, but no flight safety impact",
       "Audit log with cryptographic timestamps (NTP + HMAC)"
   )
   
   # Information Disclosure
   fms_threats.add_threat(
       "Information Disclosure",
       "Attacker intercepts wireless datalink containing flight plan",
       "Minor - flight plan exposure (privacy concern, not safety)",
       "Encrypt ACARS messages (AES-256-GCM) if confidentiality required"
   )
   
   # Denial of Service
   fms_threats.add_threat(
       "Denial of Service",
       "Attacker floods AFDX network preventing FMS communication",
       "Major - loss of sensor data could degrade FMS functionality",
       "AFDX traffic policing, rate limiting (per ARINC 664)"
   )
   
   # Elevation of Privilege
   fms_threats.add_threat(
       "Elevation of Privilege",
       "Attacker exploits USB maintenance interface to gain root access",
       "Catastrophic - arbitrary code execution in FMS",
       "Secure boot, USB disabled in flight mode, authentication"
   )

**Attack Tree Analysis:**

Attack trees visualize how an attacker could achieve a goal:

.. code-block:: text

   Goal: Compromise Flight Management System
   
   ┌─────────────────────────────────────────────────┐
   │   Compromise FMS (Goal)                         │
   └──────┬──────────────────────────────────────────┘
          │
          ├─── [OR] ─┐
          │          │
   ┌──────▼──────┐   │   ┌──────────────┐   ┌────────────────┐
   │ Physical     │   ├───│ Remote       │   │ Supply Chain   │
   │ Access       │   │   │ Network      │   │ Attack         │
   └──┬───────────┘   │   └───┬──────────┘   └───┬────────────┘
      │               │       │                  │
      ├─ [AND] ──┐    │       ├─ [OR] ──┐        ├─ [AND] ──┐
      │          │    │       │         │        │          │
   ┌──▼────┐ ┌──▼────┐│    ┌──▼────┐ ┌─▼────┐ ┌─▼────┐ ┌──▼────┐
   │Cockpit│ │Bypass ││    │Exploit│ │Social│ │Insert│ │Modify │
   │Access │ │Secure ││    │Vulner-│ │Eng.  │ │Trojan│ │Source │
   │       │ │Boot   ││    │ability│ │      │ │HW    │ │Code   │
   └───────┘ └───────┘│    └───────┘ └──────┘ └──────┘ └───────┘
                      │
               [Likelihood: High if no USB auth]
               [Impact: Catastrophic]
               [Mitigation: Dual auth, secure boot]

**PASTA (Process for Attack Simulation and Threat Analysis):**

Seven-stage risk-centric threat modeling:

1. **Define Objectives** — Protect flight-critical data integrity
2. **Define Technical Scope** — FMS hardware, software, interfaces
3. **Application Decomposition** — Break down into components (navigation, flight plan, database)
4. **Threat Analysis** — Identify threats using STRIDE, CAPEC
5. **Vulnerability Analysis** — Review code, architecture, configurations
6. **Attack Modeling** — Simulate attack scenarios
7. **Risk & Impact Analysis** — Prioritize threats by likelihood × impact

════════════════════════════════════════════════════════════════════════════

🔐 **CRYPTOGRAPHIC METHODS**
─────────────────────────────────────────────────────────────────────────

**DO-356A Cryptographic Guidance:**

**Symmetric Cryptography:**

| Algorithm | Key Size | Use Case in Aviation | Notes |
|:----------|:---------|:---------------------|:------|
| **AES-128** | 128-bit | ACARS encryption | Fast, widely supported |
| **AES-256** | 256-bit | Software protection, key wrapping | Future-proof |
| **AES-GCM** | 128/256-bit | Authenticated encryption | Preferred (integrity + confidentiality) |

**Asymmetric Cryptography:**

| Algorithm | Key Size | Use Case | Performance |
|:----------|:---------|:---------|:------------|
| **RSA-2048** | 2048-bit | Legacy software signing | Slow verification |
| **RSA-4096** | 4096-bit | High-value assets (master keys) | Very slow |
| **ECDSA-P256** | 256-bit | Modern software signing | Fast ✅ |
| **ECDSA-P384** | 384-bit | SAL 3 systems | Fast, high security ✅ |

**Hash Functions:**

- **SHA-256** — Standard for integrity checks
- **SHA-384/512** — High-security applications
- **SHA-3** — Modern alternative (Keccak)

**Message Authentication:**

.. code-block:: c

   // HMAC-SHA256 for ACARS message authentication
   #include <stdint.h>
   #include "mbedtls/md.h"
   
   #define HMAC_KEY_SIZE 32
   #define HMAC_OUTPUT_SIZE 32
   
   // Stored in HSM or secure OTP
   static const uint8_t hmac_key[HMAC_KEY_SIZE] = { /* ... */ };
   
   bool authenticate_acars_message(
       const uint8_t *message,
       size_t msg_len,
       const uint8_t *received_hmac)
   {
       uint8_t calculated_hmac[HMAC_OUTPUT_SIZE];
       
       // Calculate HMAC
       mbedtls_md_hmac(
           mbedtls_md_info_from_type(MBEDTLS_MD_SHA256),
           hmac_key, HMAC_KEY_SIZE,
           message, msg_len,
           calculated_hmac
       );
       
       // Constant-time comparison (prevent timing attacks)
       int result = 0;
       for (size_t i = 0; i < HMAC_OUTPUT_SIZE; i++) {
           result |= calculated_hmac[i] ^ received_hmac[i];
       }
       
       return (result == 0);
   }

**Digital Signature Verification:**

.. code-block:: c

   // ECDSA-P384 signature verification for software loading
   #include "mbedtls/ecdsa.h"
   #include "mbedtls/sha512.h"
   
   // Public key stored in immutable ROM/OTP
   static const uint8_t pubkey_x[48] = { /* P-384 X coordinate */ };
   static const uint8_t pubkey_y[48] = { /* P-384 Y coordinate */ };
   
   bool verify_software_signature(
       const uint8_t *software,
       size_t sw_len,
       const uint8_t *signature,
       size_t sig_len)
   {
       mbedtls_ecdsa_context ctx;
       mbedtls_mpi r, s;
       uint8_t hash[48];  // SHA-384 output
       int ret;
       
       // 1. Hash software using SHA-384
       mbedtls_sha512(software, sw_len, hash, 1);  // 1 = use SHA-384
       
       // 2. Initialize ECDSA context with public key
       mbedtls_ecdsa_init(&ctx);
       mbedtls_ecp_group_load(&ctx.grp, MBEDTLS_ECP_DP_SECP384R1);
       mbedtls_mpi_read_binary(&ctx.Q.X, pubkey_x, 48);
       mbedtls_mpi_read_binary(&ctx.Q.Y, pubkey_y, 48);
       mbedtls_mpi_lset(&ctx.Q.Z, 1);
       
       // 3. Parse signature (r, s)
       mbedtls_mpi_read_binary(&r, signature, sig_len / 2);
       mbedtls_mpi_read_binary(&s, signature + sig_len / 2, sig_len / 2);
       
       // 4. Verify
       ret = mbedtls_ecdsa_verify(&ctx.grp, hash, 48, &ctx.Q, &r, &s);
       
       // Cleanup
       mbedtls_ecdsa_free(&ctx);
       mbedtls_mpi_free(&r);
       mbedtls_mpi_free(&s);
       
       return (ret == 0);  // 0 = success
   }

════════════════════════════════════════════════════════════════════════════

🛡️ **SECURITY ARCHITECTURE PATTERNS**
─────────────────────────────────────────────────────────────────────────

**Defense-in-Depth Layers:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 7: Policies & Procedures                                  │
│ - Security awareness training for maintenance crews             │
│ - Dual-person integrity for critical operations                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 6: Physical Security                                       │
│ - Cockpit door lock                                              │
│ - Secure equipment racks                                         │
│ - Tamper-evident seals                                           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 5: Perimeter Security                                      │
│ - Firewalls between networks (IFE ↔ Avionics)                   │
│ - Data diodes (one-way communication)                            │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 4: Network Security                                        │
│ - AFDX traffic policing (ARINC 664 Part 7)                      │
│ - VLANs for segregation                                          │
│ - Intrusion detection systems                                    │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 3: Host Security                                           │
│ - Secure boot (verify all code before execution)                │
│ - Memory protection (MPU/MMU)                                    │
│ - Least privilege (ARINC 653 partitioning)                      │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 2: Application Security                                    │
│ - Input validation                                               │
│ - Authentication & authorization                                 │
│ - Secure coding (CERT C, MISRA C)                               │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│ Layer 1: Data Security                                           │
│ - Encryption at rest (AES-256)                                   │
│ - Encryption in transit (TLS 1.3)                                │
│ - Message authentication (HMAC)                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Network Segregation Pattern:**

.. code-block:: text

   Aircraft Network Zones (DO-356A Best Practice):
   
   Zone 1: Public (SAL 0)
   ┌────────────────────────────────────────┐
   │ Passenger Wi-Fi, Cellular              │
   │ Threat: Malicious passengers           │
   └───────────┬────────────────────────────┘
               │ Firewall (deny all inbound)
   Zone 2: IFE (SAL 0)
   ┌───────────▼────────────────────────────┐
   │ In-Flight Entertainment System         │
   │ Threat: Compromised IFE → pivot attack │
   └───────────┬────────────────────────────┘
               │ Data Diode (read-only to Zone 3)
   Zone 3: Aircraft Info (SAL 1)
   ┌───────────▼────────────────────────────┐
   │ Moving map, flight info displays       │
   │ Threat: Misleading information         │
   └───────────┬────────────────────────────┘
               │ Firewall + IDS/IPS
   Zone 4: Avionics (SAL 2-3)
   ┌───────────▼────────────────────────────┐
   │ FMS, Flight Control, Engine Control    │
   │ Threat: Flight safety compromise       │
   │ Protection: No direct path from Zone 1 │
   └────────────────────────────────────────┘

**Secure Protocol Design:**

.. code-block:: c

   // Secure ARINC 429 wrapper with authentication
   typedef struct {
       uint32_t arinc429_word;  // Standard ARINC 429 (32-bit)
       uint32_t sequence_num;   // Prevent replay attacks
       uint8_t hmac[16];        // HMAC-SHA256 truncated to 128 bits
   } SecureARINC429Message;
   
   bool send_secure_arinc429(uint32_t data) {
       SecureARINC429Message msg;
       static uint32_t seq_counter = 0;
       
       // 1. Populate message
       msg.arinc429_word = data;
       msg.sequence_num = seq_counter++;
       
       // 2. Calculate HMAC over word + sequence
       uint8_t hmac_input[8];
       memcpy(hmac_input, &msg.arinc429_word, 4);
       memcpy(hmac_input + 4, &msg.sequence_num, 4);
       
       hmac_sha256(shared_key, 32, hmac_input, 8, msg.hmac);
       
       // 3. Transmit (custom protocol over ARINC 664 or similar)
       return transmit_message(&msg, sizeof(msg));
   }
   
   bool receive_secure_arinc429(uint32_t *data_out) {
       SecureARINC429Message msg;
       static uint32_t last_seq = 0;
       
       // 1. Receive message
       if (!receive_message(&msg, sizeof(msg))) return false;
       
       // 2. Verify HMAC
       uint8_t hmac_input[8];
       memcpy(hmac_input, &msg.arinc429_word, 4);
       memcpy(hmac_input + 4, &msg.sequence_num, 4);
       
       uint8_t calculated_hmac[16];
       hmac_sha256(shared_key, 32, hmac_input, 8, calculated_hmac);
       
       if (memcmp(msg.hmac, calculated_hmac, 16) != 0) {
           log_security_event(SEC_EVENT_HMAC_FAIL);
           return false;
       }
       
       // 3. Check sequence number (replay protection)
       if (msg.sequence_num <= last_seq) {
           log_security_event(SEC_EVENT_REPLAY_ATTACK);
           return false;
       }
       last_seq = msg.sequence_num;
       
       // 4. Extract data
       *data_out = msg.arinc429_word;
       return true;
   }

════════════════════════════════════════════════════════════════════════════

✅ **SECURITY VERIFICATION METHODS**
─────────────────────────────────────────────────────────────────────────

**Penetration Testing Approach:**

.. code-block:: text

   Aviation Penetration Test Plan (DO-356A Guidance):
   
   Phase 1: Reconnaissance
   ✓ Network discovery (identify all interfaces)
   ✓ Service enumeration (open ports, protocols)
   ✓ Wireless signal analysis (Wi-Fi, datalinks)
   
   Phase 2: Vulnerability Assessment
   ✓ Known vulnerability scanning (Nessus, OpenVAS)
   ✓ Configuration review (default passwords, weak crypto)
   ✓ Protocol analysis (ARINC 429, AFDX, ACARS)
   
   Phase 3: Exploitation
   ✓ Attempt network pivot (IFE → Avionics)
   ✓ Test authentication bypass
   ✓ Fuzzing interfaces (USB, ACARS, ARINC 664)
   
   Phase 4: Post-Exploitation
   ✓ Privilege escalation attempts
   ✓ Lateral movement within avionics network
   ✓ Data exfiltration (can we extract flight plan?)
   
   Phase 5: Reporting
   ✓ Findings with severity (Critical/High/Medium/Low)
   ✓ Exploitability rating
   ✓ Remediation recommendations

**Fuzzing Example:**

.. code-block:: python

   # Fuzzing ACARS message parser (DO-356A verification method)
   import random
   import struct
   
   def fuzz_acars_parser():
       """
       Fuzzing test for ACARS message parser
       Goal: Find crashes, hangs, or security vulnerabilities
       """
       
       # Valid ACARS message format
       def generate_valid_message():
           return {
               'msg_id': b'A12B',
               'content': b'CLIMB TO FL350',
               'checksum': 0x1234
           }
       
       # Fuzzing strategies
       def fuzz_length(msg):
           # Test buffer overflows
           msg['content'] = b'A' * random.randint(0, 10000)
           return msg
       
       def fuzz_special_chars(msg):
           # Test injection attacks
           msg['content'] = b'\x00\xff\x0a\x0d' * 50
           return msg
       
       def fuzz_format_strings(msg):
           # Test format string vulnerabilities
           msg['content'] = b'%s%s%s%n%n%n' * 10
           return msg
       
       def fuzz_malformed(msg):
           # Test parser robustness
           return struct.pack('I', random.randint(0, 0xFFFFFFFF)) * 20
       
       # Run fuzzing
       strategies = [fuzz_length, fuzz_special_chars, fuzz_format_strings, fuzz_malformed]
       
       for i in range(10000):
           msg = generate_valid_message()
           strategy = random.choice(strategies)
           fuzzed = strategy(msg)
           
           try:
               # Send to target system
               result = send_to_target(fuzzed)
               
               # Monitor for crashes, hangs, or unexpected behavior
               if result == 'CRASH':
                   log_finding(f"Fuzzing iteration {i}: CRASH detected with {strategy.__name__}")
               elif result == 'HANG':
                   log_finding(f"Fuzzing iteration {i}: HANG detected (DoS potential)")
                   
           except Exception as e:
               log_finding(f"Fuzzing iteration {i}: Exception - {e}")

**Static Analysis:**

.. code-block:: bash

   # Static analysis tools for avionics code (DO-356A recommendation)
   
   # 1. Coverity (commercial)
   cov-build --dir cov-int make
   cov-analyze --dir cov-int --security --concurrency --all
   
   # 2. Clang Static Analyzer
   scan-build make
   
   # 3. MISRA C compliance (with security extensions)
   pc-lint-plus --misra-c-2012 --cert-c src/*.c
   
   # 4. CWE (Common Weakness Enumeration) detection
   flawfinder --minlevel=4 --context src/

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: How does DO-356A complement DO-326A?**

**A1:**
- **DO-326A** defines the **process** (what security activities to perform, when, and what evidence to produce)
- **DO-356A** provides **methods** (how to perform threat modeling, which cryptographic algorithms, testing techniques)
- **Analogy:** DO-326A = recipe instructions, DO-356A = cooking techniques handbook
- **Usage:** DO-326A is mandatory for certification; DO-356A is recommended guidance but not required

**Q2: Describe the STRIDE threat modeling method and apply it to an avionics datalink.**

**A2:**
**STRIDE analysis for ACARS datalink:**
- **Spoofing:** Attacker impersonates ATC sending forged clearances → Mitigate with message authentication (HMAC)
- **Tampering:** Attacker modifies message in transit → Mitigate with integrity checks
- **Repudiation:** Sender denies sending message → Mitigate with digital signatures + audit logs
- **Information Disclosure:** Attacker intercepts flight plan → Mitigate with encryption (if confidentiality required)
- **Denial of Service:** Attacker floods datalink with garbage → Mitigate with rate limiting
- **Elevation of Privilege:** Attacker gains higher access via datalink → Mitigate with least privilege, input validation

**Q3: What cryptographic algorithms does DO-356A recommend for SAL 3 systems?**

**A3:**
SAL 3 (catastrophic impact) recommendations:
- **Symmetric:** AES-256-GCM (authenticated encryption)
- **Asymmetric:** ECDSA-P384 or RSA-4096 (digital signatures)
- **Hash:** SHA-384 or SHA-512
- **MAC:** HMAC-SHA256 minimum (HMAC-SHA384 preferred)
- **Key Storage:** Hardware Security Module (HSM) or OTP fuses
- **Standards Compliance:** FIPS 140-2 Level 2+ cryptographic modules

**Rationale:** Catastrophic impact requires resistance to sophisticated nation-state attacks, future-proof key sizes, and hardware protection.

**Q4: Explain defense-in-depth as applied to avionics networks.**

**A4:**
Defense-in-depth uses multiple independent security layers:

**Layer 1 (Perimeter):** Firewall between IFE and avionics — blocks direct attacks  
**Layer 2 (Network):** AFDX traffic policing — prevents flooding DoS  
**Layer 3 (Host):** Secure boot — prevents malware execution  
**Layer 4 (Application):** Input validation — prevents injection attacks  
**Layer 5 (Data):** Message authentication — detects tampering  

**Benefit:** If one layer fails (e.g., firewall bypass), other layers still protect. Attacker must breach ALL layers to compromise system.

**Q5: What are key differences between penetration testing and vulnerability scanning?**

**A5:**
| Aspect | **Vulnerability Scanning** | **Penetration Testing** |
|:-------|:---------------------------|:------------------------|
| **Approach** | Automated tool (Nessus, OpenVAS) | Manual exploitation by security expert |
| **Scope** | Known vulnerabilities (CVE database) | Unknown vulnerabilities + attack chains |
| **Depth** | Surface-level identification | Deep exploitation + post-exploitation |
| **Output** | List of potential vulnerabilities | Proof of exploitability + business impact |
| **Cost** | Low (tool license) | High (expert time) |
| **Frequency** | Weekly/monthly | Annually or pre-certification |

**DO-356A recommends BOTH:** Scanning for continuous monitoring, penetration testing for SAL 2-3 systems before certification.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~750
