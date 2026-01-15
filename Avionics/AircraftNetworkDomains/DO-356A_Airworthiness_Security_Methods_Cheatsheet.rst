🛡️ **DO-356A / ED-203A — Airworthiness Security Methods & Considerations**
════════════════════════════════════════════════════════════════════════════

**Context:** Security development assurance for safety-critical avionics systems
**Standards:** RTCA DO-356A (2018), EUROCAE ED-203A (European equivalent)
**Purpose:** Security equivalent of DO-178C (development methods & testing)
**Certification:** Provides compliance evidence for DO-326A security process

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — DO-356A IN 60 SECONDS**
─────────────────────────────────────

**What is DO-356A?**

::

    DO-356A = Security methods for implementing DO-326A
    
    Relationship:
    - DO-326A defines WHAT to do (security process, SAL)
    - DO-356A defines HOW to do it (methods, testing, evidence)

**Key Methodologies:**

+---------------------------+----------------------------------+
| **Method**                | **Purpose**                      |
+===========================+==================================+
| Security Requirements     | Derive from threat analysis      |
+---------------------------+----------------------------------+
| Secure Coding             | MISRA C++, CERT C++, static anal |
+---------------------------+----------------------------------+
| Cryptographic Validation  | FIPS 140-2 compliance            |
+---------------------------+----------------------------------+
| Penetration Testing       | Adversarial simulation           |
+---------------------------+----------------------------------+
| Fuzzing                   | Protocol robustness testing      |
+---------------------------+----------------------------------+
| Red Team Exercises        | Sophisticated attack simulation  |
+---------------------------+----------------------------------+

**SAL-Specific Requirements:**

::

    SAL 1: Basic security testing, code review
    SAL 2: Penetration testing, threat modeling, fuzzing
    SAL 3: Red team exercises, independent review, formal methods

════════════════════════════════════════════════════════════════════

📖 **1. SECURITY DEVELOPMENT LIFECYCLE**
════════════════════════════════════════

**1.1 SDL Overview**
-------------------

**Security Development Lifecycle (SDL) Phases:**

::

    ┌────────────────────────────────────────────────┐
    │ Phase 1: Security Requirements                 │
    │  ├─► Threat modeling (STRIDE, attack trees)    │
    │  ├─► Security requirements derivation          │
    │  └─► SAL assignment (from DO-326A SRA)         │
    └──────────────┬─────────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────────┐
    │ Phase 2: Secure Design                         │
    │  ├─► Security architecture review              │
    │  ├─► Defense in depth patterns                 │
    │  └─► Cryptographic design                      │
    └──────────────┬─────────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────────┐
    │ Phase 3: Secure Implementation                 │
    │  ├─► Secure coding standards (MISRA, CERT)     │
    │  ├─► Static analysis (Coverity, CodeSonar)     │
    │  └─► Code review (peer + security expert)      │
    └──────────────┬─────────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────────┐
    │ Phase 4: Security Verification                 │
    │  ├─► Penetration testing                       │
    │  ├─► Fuzzing (protocol testing)                │
    │  ├─► Cryptographic validation (FIPS 140-2)     │
    │  └─► Red team exercises (SAL 3)                │
    └──────────────┬─────────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────────┐
    │ Phase 5: Security Operations & Monitoring      │
    │  ├─► Continuous monitoring (SIEM, IDS)         │
    │  ├─► Incident response                         │
    │  └─► Vulnerability management                  │
    └────────────────────────────────────────────────┘

**1.2 Integration with DO-178C**
--------------------------------

**Parallel Development:**

+------------------------+-------------------------+------------------------+
| **DO-178C Activity**   | **DO-356A Activity**    | **Output**             |
+========================+=========================+========================+
| Requirements Phase     | Threat modeling         | Security requirements  |
+------------------------+-------------------------+------------------------+
| Design Phase           | Security architecture   | Secure design patterns |
+------------------------+-------------------------+------------------------+
| Implementation Phase   | Secure coding, SAST     | Verified source code   |
+------------------------+-------------------------+------------------------+
| Verification Phase     | Penetration testing     | Security test results  |
+------------------------+-------------------------+------------------------+
| Certification Phase    | Independent review      | Security evidence (SAS)|
+------------------------+-------------------------+------------------------+

**Combined Assurance:**

::

    DAL A (Safety) + SAL 3 (Security) = Highest Assurance
    
    Example: Flight Control Computer (FCC)
    - DO-178C DAL A: Prevents unintentional failures
    - DO-356A SAL 3: Prevents intentional attacks
    - Combined: Protects against ALL threats

════════════════════════════════════════════════════════════════════

📖 **2. SECURITY REQUIREMENTS DEVELOPMENT**
═══════════════════════════════════════════

**2.1 Threat Modeling (STRIDE)**
--------------------------------

**STRIDE Applied to Aircraft Network:**

.. code-block:: python

    # threat_model.py
    
    class ThreatModel:
        def __init__(self, system_name, domain):
            self.system_name = system_name
            self.domain = domain  # ACD, AISD, PIESD
            self.threats = []
        
        def stride_analysis(self):
            """STRIDE threat analysis"""
            
            # Spoofing Identity
            self.threats.append({
                'category': 'Spoofing',
                'description': f'Attacker impersonates {self.system_name}',
                'example': 'Fake GPS signal injection',
                'mitigation': 'Cryptographic authentication (ECDSA)',
                'sal_requirement': 2
            })
            
            # Tampering with Data
            self.threats.append({
                'category': 'Tampering',
                'description': 'Attacker modifies data in transit/storage',
                'example': 'Modify FMS flight plan',
                'mitigation': 'Message authentication code (HMAC-SHA256)',
                'sal_requirement': 3
            })
            
            # Repudiation
            self.threats.append({
                'category': 'Repudiation',
                'description': 'Attacker denies actions',
                'example': 'Insider deletes audit logs',
                'mitigation': 'Immutable log storage (WORM)',
                'sal_requirement': 2
            })
            
            # Information Disclosure
            self.threats.append({
                'category': 'Information Disclosure',
                'description': 'Attacker intercepts sensitive data',
                'example': 'Eavesdrop on data diode',
                'mitigation': 'AES-256 encryption',
                'sal_requirement': 2
            })
            
            # Denial of Service
            self.threats.append({
                'category': 'Denial of Service',
                'description': 'Attacker floods system',
                'example': 'DDoS attack on passenger WiFi',
                'mitigation': 'Rate limiting (1 Mbps per device)',
                'sal_requirement': 1
            })
            
            # Elevation of Privilege
            self.threats.append({
                'category': 'Elevation of Privilege',
                'description': 'Attacker gains unauthorized access',
                'example': 'Escape from PIESD to AISD',
                'mitigation': 'Firewall + principle of least privilege',
                'sal_requirement': 3
            })
            
            return self.threats
    
    # Example usage
    ife_system = ThreatModel('IFE Server', 'PIESD')
    threats = ife_system.stride_analysis()
    
    for threat in threats:
        print(f"\n{threat['category']}:")
        print(f"  Description: {threat['description']}")
        print(f"  Mitigation: {threat['mitigation']}")
        print(f"  SAL Requirement: {threat['sal_requirement']}")

**2.2 Attack Trees**
-------------------

**Attack Tree for "Hijack Flight Controls":**

.. code-block:: text

    Goal: Unauthorized Control of Flight Surfaces
         │
         ├─── AND ───────────────────┐
         │                           │
    [Physical Access]          [Bypass Security]
         │                           │
         ├─► Gain cockpit access     ├─► Exploit software vulnerability
         │   (P = 0.001)             │   (P = 0.01)
         │                           │
         ├─► Defeat LOTO             ├─► Escalate privileges
         │   (P = 0.01)              │   (P = 0.1)
         │                           │
         └─► Insert malicious USB    └─► Inject malicious commands
             (P = 0.05)                  (P = 0.2)
    
    Probability Analysis:
    - Physical Path: 0.001 × 0.01 × 0.05 = 0.0000005 (1 in 2M)
    - Cyber Path: 0.01 × 0.1 × 0.2 = 0.0002 (1 in 5,000)
    - Total Risk: 0.0002 → Requires SAL 3 mitigations

**2.3 Security Requirements Specification**
-------------------------------------------

**Security Requirement Template:**

.. code-block:: text

    SR-ID: SR-AISD-001
    Title: Maintenance USB Authentication
    
    Description:
    The AISD maintenance interface shall authenticate all USB devices
    before allowing data transfer.
    
    Rationale:
    Mitigates threat of malware introduction via USB (STRIDE: Tampering)
    
    Derived From:
    - Threat: USB malware injection (SAL 2)
    - DO-326A SRA: Risk Score 12 (Medium)
    
    Acceptance Criteria:
    1. USB device presents valid digital certificate (RSA 2048+)
    2. Certificate chain validated against airline root CA
    3. Device serial number whitelisted in database
    4. All transfers logged with timestamp + technician ID
    
    Verification Method:
    - Test Case: TC-SR-AISD-001 (insert invalid USB, verify rejection)
    - Penetration Test: Attempt to bypass authentication
    
    SAL Level: 2
    Allocated To: AISD Maintenance Module v2.1
    Status: ✅ Implemented, ✅ Verified

**Traceability Matrix:**

+------------+------------------+------------------+------------------+
| **Threat** | **Security Req** | **Design**       | **Test Case**    |
+============+==================+==================+==================+
| STRIDE-T   | SR-AISD-001      | USB Auth Module  | TC-SR-AISD-001   |
| USB Tamper | (USB Auth)       | (Cert Validation)| (Invalid USB)    |
+------------+------------------+------------------+------------------+
| STRIDE-E   | SR-AISD-002      | RBAC Enforcement | TC-SR-AISD-002   |
| Priv Esc   | (Least Privilege)| (Role Check)     | (Unauthorized)   |
+------------+------------------+------------------+------------------+

════════════════════════════════════════════════════════════════════

📖 **3. SECURE CODING PRACTICES**
═════════════════════════════════

**3.1 MISRA C++ / CERT C++ Secure Coding**
------------------------------------------

**Critical Rules for Avionics:**

.. code-block:: cpp

    // Rule 1: Always validate input bounds
    // ❌ BAD: Buffer overflow
    void process_message(const char* msg) {
        char buffer[256];
        strcpy(buffer, msg);  // Unchecked copy!
    }
    
    // ✅ GOOD: Safe string copy
    void process_message_safe(const char* msg) {
        char buffer[256];
        if (msg == nullptr || strlen(msg) >= sizeof(buffer)) {
            log_error("Invalid message length");
            return;
        }
        strncpy(buffer, msg, sizeof(buffer) - 1);
        buffer[sizeof(buffer) - 1] = '\0';
    }
    
    // Rule 2: Avoid integer overflow
    // ❌ BAD: Integer overflow in altitude calculation
    uint16_t calculate_altitude(uint16_t pressure, uint16_t offset) {
        return pressure + offset;  // May overflow!
    }
    
    // ✅ GOOD: Overflow check
    uint16_t calculate_altitude_safe(uint16_t pressure, uint16_t offset) {
        if (pressure > UINT16_MAX - offset) {
            log_error("Altitude overflow");
            return UINT16_MAX;  // Saturate
        }
        return pressure + offset;
    }
    
    // Rule 3: Cryptographically secure random numbers
    // ❌ BAD: Predictable rand()
    uint32_t generate_session_key() {
        return rand();  // NEVER use for crypto!
    }
    
    // ✅ GOOD: Cryptographic PRNG
    uint32_t generate_session_key_secure() {
        uint32_t key;
        if (RAND_bytes((unsigned char*)&key, sizeof(key)) != 1) {
            log_error("Random generation failed");
            abort();
        }
        return key;
    }
    
    // Rule 4: Always clear sensitive data
    // ❌ BAD: Password left in memory
    void authenticate(const char* password) {
        char stored_hash[64];
        // ... authenticate ...
        // Password still in memory!
    }
    
    // ✅ GOOD: Explicit memory clear
    void authenticate_secure(char* password) {
        char stored_hash[64];
        // ... authenticate ...
        
        // Zero password immediately
        explicit_bzero(password, strlen(password));
    }

**3.2 Static Analysis Tools**
-----------------------------

**Tool Configuration:**

.. code-block:: yaml

    # coverity_config.yaml
    
    analysis_settings:
      security_checks:
        - buffer_overflow
        - integer_overflow
        - use_after_free
        - null_pointer_dereference
        - cryptographic_misuse
        - race_conditions
      
      coding_standards:
        - MISRA_C_2012
        - CERT_C_Secure_Coding
        - CWE_Top_25
      
      severity_thresholds:
        SAL_1: HIGH severity required
        SAL_2: MEDIUM severity required
        SAL_3: ALL findings must be reviewed
      
      false_positive_handling:
        - Require justification (security review)
        - Document in compliance matrix
        - Re-validate every release

**Sample Static Analysis Report:**

.. code-block:: text

    ================================================================================
    Static Analysis Report: AISD Maintenance Module v2.1
    Tool: Coverity Scan 2024.1
    Date: 2026-01-14
    ================================================================================
    
    Summary:
    - Total Defects: 42
    - Critical: 0 ✅
    - High: 3 🟡
    - Medium: 15 🟢
    - Low: 24 🟢
    
    Critical Findings (Must Fix):
    None ✅
    
    High Severity Findings:
    
    DEFECT-001: Buffer Overflow (CWE-120)
      File: usb_handler.c:127
      Function: process_usb_data()
      Description: strcpy() without bounds check
      Recommendation: Use strncpy() with size limit
      Status: ✅ FIXED (commit 8a3f9d2)
    
    DEFECT-002: Use After Free (CWE-416)
      File: network.c:453
      Function: close_connection()
      Description: Pointer used after free()
      Recommendation: Set pointer to NULL after free
      Status: ✅ FIXED (commit 7b2e1a4)
    
    DEFECT-003: Integer Overflow (CWE-190)
      File: altitude_calc.c:89
      Function: calculate_pressure()
      Description: Addition may overflow uint16_t
      Recommendation: Add overflow check
      Status: 🟡 IN PROGRESS (ETA: 2026-01-20)
    
    ================================================================================
    Certification Impact: SAL 2 requires all HIGH findings resolved
    ================================================================================

**3.3 Code Review Process**
---------------------------

**Security-Focused Code Review Checklist:**

.. code-block:: markdown

    # Security Code Review Checklist (SAL 2/3)
    
    ## Input Validation
    - [ ] All external inputs validated (bounds, format, type)
    - [ ] No user input directly used in system calls
    - [ ] SQL injection prevention (parameterized queries)
    - [ ] Command injection prevention (no shell exec)
    
    ## Memory Safety
    - [ ] No buffer overflows (bounds checks on all copies)
    - [ ] No use-after-free (pointers nulled after free)
    - [ ] No double-free (freed pointers not re-freed)
    - [ ] Stack overflow prevention (recursion depth limited)
    
    ## Cryptography
    - [ ] No hardcoded keys/passwords
    - [ ] FIPS 140-2 validated algorithms only
    - [ ] Secure random number generation (CSPRNG)
    - [ ] Proper key management (HSM integration)
    
    ## Authentication & Authorization
    - [ ] Multi-factor authentication (MFA) implemented
    - [ ] Principle of least privilege enforced
    - [ ] Session timeout configured (15 min idle)
    - [ ] No credential leakage in logs/error messages
    
    ## Logging & Monitoring
    - [ ] Security events logged (login, access, errors)
    - [ ] Logs tamper-evident (HMAC, append-only)
    - [ ] No sensitive data in logs (passwords, keys)
    - [ ] Log retention policy enforced (180 days)
    
    ## Error Handling
    - [ ] No detailed error messages to user (info leakage)
    - [ ] Graceful degradation (no crash on invalid input)
    - [ ] All exceptions caught and logged
    - [ ] Fail-secure defaults (deny on error)

════════════════════════════════════════════════════════════════════

📖 **4. SECURITY TESTING METHODS**
══════════════════════════════════

**4.1 Penetration Testing**
---------------------------

**Penetration Test Plan Template:**

.. code-block:: yaml

    # penetration_test_plan.yaml
    
    test_metadata:
      target_system: "AISD Maintenance Interface"
      sal_level: 2
      test_duration: "5 days"
      tester: "External Security Firm (SAL 2/3)"
      methodology: "OWASP Testing Guide v4, NIST 800-115"
    
    scope:
      in_scope:
        - Maintenance network (VLAN 500)
        - USB interface authentication
        - Ground link (VPN)
        - Web management console
      
      out_of_scope:
        - ACD (flight-critical, separate engagement)
        - PIESD (passenger network, lower priority)
        - Physical attacks (red team only)
    
    test_phases:
      phase_1_reconnaissance:
        activities:
          - Network mapping (Nmap)
          - Service enumeration
          - Vulnerability scanning (Nessus)
        duration: "1 day"
      
      phase_2_exploitation:
        activities:
          - Attempt known CVEs
          - Custom exploit development
          - Social engineering (phishing simulation)
        duration: "2 days"
      
      phase_3_post_exploitation:
        activities:
          - Lateral movement (PIESD → AISD)
          - Privilege escalation
          - Data exfiltration simulation
        duration: "1 day"
      
      phase_4_reporting:
        deliverables:
          - Executive summary
          - Technical findings report
          - Remediation recommendations
          - Compliance matrix (DO-356A objectives)
        duration: "1 day"
    
    success_criteria:
      - No critical vulnerabilities (CVSS ≥ 9.0)
      - All high vulnerabilities remediated
      - Medium vulnerabilities risk-accepted
      - Compliance with SAL 2 objectives

**4.2 Fuzzing (Protocol Testing)**
----------------------------------

**Fuzzing Configuration:**

.. code-block:: python

    # fuzzing_test.py
    import boofuzz
    
    def fuzz_arinc_664_message():
        """Fuzz ARINC 664 (AFDX) message handling"""
        
        # Define message structure
        s_initialize("AFDX_MESSAGE")
        s_word(0x1234, name="virtual_link_id", fuzzable=True)
        s_word(0x0100, name="sequence_number", fuzzable=True)
        s_size("payload", length=2, name="length", fuzzable=True)
        s_string("NORMAL_DATA", name="payload", fuzzable=True)
        s_dword(0xDEADBEEF, name="crc", fuzzable=True)
        
        # Create session
        session = boofuzz.Session(
            target=boofuzz.Target(
                connection=boofuzz.TCPSocketConnection("10.20.1.100", 5000)
            ),
            crash_detection=True,
            restart_interval=100
        )
        
        # Add test cases
        session.connect(s_get("AFDX_MESSAGE"))
        
        # Run fuzzing campaign
        session.fuzz()
    
    def fuzz_usb_authentication():
        """Fuzz USB authentication protocol"""
        
        s_initialize("USB_AUTH_REQUEST")
        
        # Certificate chain (fuzz lengths, formats)
        s_size("cert_data", length=4, name="cert_length", fuzzable=True)
        s_string("X.509_CERTIFICATE", name="cert_data", fuzzable=True, max_len=4096)
        
        # Signature (fuzz crypto data)
        s_binary("0x" + "A" * 512, name="signature", fuzzable=True)
        
        # Device serial (fuzz format)
        s_string("SN123456789", name="serial_number", fuzzable=True, max_len=64)
        
        session = boofuzz.Session(
            target=boofuzz.Target(
                connection=boofuzz.SocketConnection("10.20.1.50", 8080, proto='udp')
            )
        )
        
        session.connect(s_get("USB_AUTH_REQUEST"))
        session.fuzz()
    
    # Run fuzzing campaigns
    if __name__ == "__main__":
        print("[*] Starting AFDX message fuzzing...")
        fuzz_arinc_664_message()
        
        print("[*] Starting USB authentication fuzzing...")
        fuzz_usb_authentication()

**Fuzzing Results Analysis:**

.. code-block:: text

    ================================================================================
    Fuzzing Report: AISD Maintenance Interface
    Tool: Boofuzz 0.4.2
    Test Cases: 10,000
    Duration: 8 hours
    ================================================================================
    
    Crashes Detected: 3
    
    CRASH-001: NULL Pointer Dereference
      Input: USB certificate length = 0xFFFFFFFF (invalid)
      Effect: Application crash (segmentation fault)
      Impact: Denial of service (restart required)
      CVSS: 5.5 (Medium)
      Remediation: Add bounds check (max cert size 4096 bytes)
    
    CRASH-002: Buffer Overflow
      Input: Device serial number = 128 bytes (expected max 64)
      Effect: Stack corruption, potential RCE
      Impact: Remote code execution possible
      CVSS: 9.8 (Critical)
      Remediation: Use strncpy() with explicit size limit
    
    CRASH-003: Infinite Loop
      Input: AFDX sequence number = 0xFFFF (wrap-around)
      Effect: 100% CPU utilization, system hang
      Impact: Denial of service (maintenance port unresponsive)
      CVSS: 6.5 (Medium)
      Remediation: Add sequence number validation
    
    ================================================================================
    Certification Impact: CRASH-002 must be fixed before SAL 2 approval
    ================================================================================

**4.3 Cryptographic Validation (FIPS 140-2)**
---------------------------------------------

**FIPS 140-2 Testing:**

.. code-block:: bash

    # FIPS 140-2 validation tests
    
    # Test 1: Algorithm Implementation Validation
    openssl version -a
    # Expected: OpenSSL 3.0+ with FIPS module
    
    # Test 2: Known Answer Test (KAT) - AES-256
    echo "PLAINTEXT_BLOCK" | openssl enc -aes-256-cbc \
      -K 0123456789ABCDEF... \
      -iv 0011223344556677... \
      -out encrypted.bin
    
    # Verify against NIST test vectors
    sha256sum encrypted.bin
    # Expected: <NIST_KAT_HASH>
    
    # Test 3: Random Number Generator (DRBG)
    openssl rand -hex 32 > random.txt
    ent random.txt  # Entropy analysis
    # Expected: Entropy = 8.0 bits per byte (perfect randomness)
    
    # Test 4: Key Wrap (AES-KW)
    openssl enc -id-aes256-wrap -K $KEK -in plaintext_key.bin -out wrapped_key.bin
    
    # Test 5: HMAC-SHA256
    echo "MESSAGE" | openssl dgst -sha256 -hmac "SECRET_KEY"
    # Verify HMAC value against known answer

**FIPS 140-2 Compliance Report:**

.. code-block:: markdown

    # FIPS 140-2 Cryptographic Module Validation Report
    
    ## Module Information
    - Name: OpenSSL FIPS Object Module 3.0.8
    - Certificate: #4282 (NIST CMVP)
    - Validation Date: 2023-06-15
    - Security Level: Level 1 (Software)
    
    ## Approved Algorithms
    - AES (128, 192, 256) - Cert #C2677
    - SHA-2 (224, 256, 384, 512) - Cert #C2677
    - RSA (2048, 3072, 4096) - Cert #C2677
    - ECDSA (P-256, P-384, P-521) - Cert #C2677
    - HMAC (SHA-256, SHA-384, SHA-512) - Cert #C2677
    - DRBG (CTR_DRBG, HASH_DRBG) - Cert #C2677
    
    ## Known Answer Tests (KAT) Results
    - AES-256 Encryption: ✅ PASS
    - AES-256 Decryption: ✅ PASS
    - SHA-256 Hash: ✅ PASS
    - RSA-2048 Sign/Verify: ✅ PASS
    - ECDSA-P256 Sign/Verify: ✅ PASS
    - HMAC-SHA256: ✅ PASS
    - DRBG Generate: ✅ PASS
    
    ## Certification Status
    ✅ Approved for avionics use (SAL 2/3)
    ✅ Compliant with DO-356A cryptographic requirements
    ✅ Acceptable to FAA/EASA for certification

════════════════════════════════════════════════════════════════════

📖 **5. RED TEAM EXERCISES (SAL 3)**
════════════════════════════════════

**5.1 Red Team Engagement Plan**
--------------------------------

**Engagement Scope:**

.. code-block:: yaml

    # red_team_plan.yaml
    
    engagement_metadata:
      objective: "Simulate nation-state APT attack on avionics network"
      sal_level: 3
      duration: "3 weeks"
      team: "External Red Team (certified)"
      white_team: "Airline CISO, FAA representative"
      blue_team: "Airline SOC, incident response"
    
    rules_of_engagement:
      allowed:
        - Physical reconnaissance (airport perimeter)
        - Social engineering (airline staff)
        - Custom exploit development (0-days)
        - Supply chain research
        - Persistent access (APT simulation)
      
      forbidden:
        - Actual flight disruption
        - Passenger data theft (live PII)
        - Physical damage to equipment
        - Insider recruitment (bribery)
    
    attack_scenarios:
      scenario_1_supply_chain:
        description: "Plant backdoor in avionics component"
        success_criteria: "Achieve code execution in ACD"
      
      scenario_2_social_engineering:
        description: "Phish airline IT staff, pivot to AISD"
        success_criteria: "Exfiltrate maintenance logs"
      
      scenario_3_physical_access:
        description: "Gain physical access to maintenance bay"
        success_criteria: "Connect rogue device to avionics"
    
    success_metrics:
      - Time to detection (MTTD)
      - Time to response (MTTR)
      - Time to eradication (MTTE)
      - Blue team detection rate (% of techniques detected)
    
    reporting:
      - Daily status updates (white team)
      - Final report (executive + technical)
      - Lessons learned workshop

**5.2 Red Team Tactics (MITRE ATT&CK)**
---------------------------------------

**Attack Chain:**

.. code-block:: text

    TA0043: Reconnaissance
      ├─► T1596: Search Open Websites/Domains
      │   (Research airline's tech stack, vendors)
      └─► T1589: Gather Victim Identity Information
          (LinkedIn reconnaissance on IT staff)
    
    TA0042: Resource Development
      ├─► T1587: Develop Capabilities
      │   (Custom exploit for IFE system)
      └─► T1588: Obtain Capabilities
          (Purchase 0-day from broker)
    
    TA0001: Initial Access
      ├─► T1566: Phishing
      │   (Spear-phish airline IT admin)
      └─► T1199: Trusted Relationship
          (Compromise avionics vendor VPN)
    
    TA0002: Execution
      ├─► T1059: Command and Scripting Interpreter
      │   (PowerShell payload on IT admin laptop)
      └─► T1204: User Execution
          (IT admin opens malicious PDF)
    
    TA0003: Persistence
      ├─► T1547: Boot or Logon Autostart Execution
      │   (Registry key for persistence)
      └─► T1543: Create or Modify System Process
          (Install rootkit)
    
    TA0005: Defense Evasion
      ├─► T1070: Indicator Removal
      │   (Clear event logs)
      └─► T1562: Impair Defenses
          (Disable antivirus)
    
    TA0008: Lateral Movement
      ├─► T1021: Remote Services (RDP)
      │   (Move from IT network to AISD)
      └─► T1080: Taint Shared Content
          (Plant malware in shared maintenance folder)
    
    TA0010: Exfiltration
      └─► T1041: Exfiltration Over C2 Channel
          (Exfiltrate flight plans over HTTPS)

**5.3 Red Team Report**
-----------------------

.. code-block:: markdown

    # Red Team Exercise Report: Airline X Avionics Network
    
    ## Executive Summary
    - Engagement Duration: 3 weeks (2026-01-01 to 2026-01-21)
    - Objective: Simulate nation-state APT attack (SAL 3)
    - Success Rate: 2/3 scenarios successful
    
    ## Scenario Results
    
    ### Scenario 1: Supply Chain Backdoor
    - Status: ❌ UNSUCCESSFUL
    - Description: Attempted to compromise avionics vendor
    - Blue Team Detection: Day 3 (anomalous vendor network traffic)
    - Mitigation: Supplier security audit process effective
    
    ### Scenario 2: Social Engineering + Pivot
    - Status: ✅ SUCCESSFUL
    - Description: Phished IT admin, gained access to AISD
    - Initial Access: Day 5 (spear-phishing email)
    - Lateral Movement: Day 8 (IT network → AISD maintenance VLAN)
    - Exfiltration: Day 12 (flight plans, maintenance logs)
    - Blue Team Detection: Day 14 (SIEM alert on large data transfer)
    - Time to Detection (TTD): 9 days ⚠️
    
    ### Scenario 3: Physical Access
    - Status: ✅ SUCCESSFUL (Partial)
    - Description: Gained physical access to maintenance bay
    - Access Achieved: Day 17 (tailgating during shift change)
    - Rogue Device: Connected to test port (AISD network)
    - Blue Team Detection: Day 18 (physical security audit)
    - Impact: Could have uploaded malware if undetected
    
    ## Key Findings
    
    ### CRITICAL-001: Weak Phishing Defenses
    - Finding: IT staff clicked malicious link (no MFA on email)
    - Impact: Initial access achieved
    - Recommendation: Mandatory MFA + phishing simulation training
    
    ### HIGH-002: Slow Detection (9 days)
    - Finding: SIEM rules insufficient for lateral movement detection
    - Impact: Attacker had 9 days of access before detection
    - Recommendation: Enhanced SIEM correlation rules + EDR deployment
    
    ### MEDIUM-003: Physical Security Gaps
    - Finding: Tailgating possible during shift change
    - Impact: Unauthorized physical access to avionics bay
    - Recommendation: Mantrap access control + CCTV monitoring
    
    ## Lessons Learned
    - ✅ Supply chain security process effective (prevented backdoor)
    - ❌ Phishing training ineffective (staff clicked malicious link)
    - ❌ Lateral movement detection too slow (9 days undetected)
    - ⚠️ Physical security adequate but improvable
    
    ## Recommendations (Priority Order)
    1. Deploy MFA on all IT systems (within 30 days)
    2. Enhance SIEM rules for lateral movement (within 60 days)
    3. Quarterly phishing simulations (ongoing)
    4. Physical security upgrades (within 90 days)

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the relationship between DO-326A and DO-356A?

**A1:**

- **DO-326A:** Security process specification (WHAT to do)
  - Defines Security Risk Assessment (SRA)
  - Assigns Security Assurance Levels (SAL)
  - Establishes security lifecycle

- **DO-356A:** Security methods and considerations (HOW to do it)
  - Provides threat modeling techniques (STRIDE)
  - Defines security testing methods (penetration, fuzzing)
  - Specifies verification activities by SAL

**Analogy:** DO-326A = ARP4754A (process), DO-356A = DO-178C (methods)

────────────────────────────────────────────────────────────────────

**Q2:** You're implementing SAL 2 security for an AISD maintenance interface. List 5 verification activities required by DO-356A.

**A2:**

1. **Threat Modeling:** STRIDE analysis + attack trees
2. **Secure Code Review:** MISRA C++, static analysis (Coverity)
3. **Penetration Testing:** Manual test by external firm
4. **Fuzzing:** Protocol robustness testing (USB auth, network protocols)
5. **Cryptographic Validation:** FIPS 140-2 compliance for all crypto

────────────────────────────────────────────────────────────────────

**Q3:** Explain the difference between penetration testing (SAL 2) and red team exercises (SAL 3).

**A3:**

**Penetration Testing (SAL 2):**

- Scope: Specific system/interface (e.g., maintenance network)
- Duration: 3-7 days
- Objective: Find vulnerabilities
- Rules: Defined scope, no physical attacks
- Team: External security firm
- Report: Technical findings + remediation

**Red Team Exercise (SAL 3):**

- Scope: Entire organization (people, process, technology)
- Duration: 2-4 weeks
- Objective: Simulate real adversary (APT)
- Rules: Minimal constraints (social engineering, physical access OK)
- Team: Adversarial simulation (Red vs Blue)
- Report: Detect/respond effectiveness + strategic recommendations

**Key Difference:** Penetration test finds bugs, red team tests defense posture

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Perform STRIDE threat modeling for all interfaces
- [ ] Develop security requirements with traceability
- [ ] Implement secure coding standards (MISRA C++, CERT)
- [ ] Run static analysis (Coverity, CodeSonar)
- [ ] Conduct security code reviews (peer + expert)
- [ ] Execute penetration testing (SAL 2/3)
- [ ] Perform fuzzing on all protocols (SAL 2/3)
- [ ] Validate cryptography (FIPS 140-2)
- [ ] Run red team exercise (SAL 3 only)
- [ ] Document all findings + remediation
- [ ] Assemble security evidence (compliance matrices)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **DO-356A provides HOW, DO-326A provides WHAT** → Complementary standards 
for security assurance

2️⃣ **STRIDE is the standard threat model** → Every system must undergo STRIDE 
analysis (SAL 2/3)

3️⃣ **Secure coding is mandatory** → MISRA C++, CERT C++ required + static 
analysis tools

4️⃣ **Penetration testing is SAL 2+ requirement** → External firm, manual 
testing, custom exploits

5️⃣ **Fuzzing uncovers protocol bugs** → Automated testing of 10,000+ test 
cases reveals crashes

6️⃣ **FIPS 140-2 validation is critical** → All cryptography must use validated 
algorithms/modules

7️⃣ **Red team = SAL 3 only** → Simulates sophisticated adversary, tests entire 
defense posture

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **DO-356A AIRWORTHINESS SECURITY METHODS COMPLETE**
**Created:** January 14, 2026
**Coverage:** Security Development Lifecycle, STRIDE Threat Modeling, Secure Coding,
Static Analysis, Penetration Testing, Fuzzing, FIPS 140-2, Red Team Exercises

════════════════════════════════════════════════════════════════════
