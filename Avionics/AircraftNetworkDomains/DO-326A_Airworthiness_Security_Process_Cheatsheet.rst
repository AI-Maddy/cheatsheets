🛡️ **DO-326A / ED-202A — Airworthiness Security Process Specification**
═══════════════════════════════════════════════════════════════════════

**Context:** Security risk assessment for safety-critical avionics systems
**Standards:** RTCA DO-326A (2014), EUROCAE ED-202A (European equivalent)
**Applies To:** All aircraft network domains (ACD, AISD, PIESD)
**Certification:** Required for FAA/EASA airworthiness approval

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — DO-326A IN 60 SECONDS**
─────────────────────────────────────

**What is DO-326A?**

::

    DO-326A = Security equivalent of ARP4754A (system safety)
    
    Purpose: Systematic process to identify, assess, and mitigate
             security threats to airborne systems

**Security Assurance Levels (SAL):**

+---------+---------------------------+-------------------------+
| **SAL** | **Threat Actor**          | **Verification Rigor**  |
+=========+===========================+=========================+
| **1**   | Casual/opportunistic      | Basic testing           |
+---------+---------------------------+-------------------------+
| **2**   | Intentional/simple means  | Security analysis       |
+---------+---------------------------+-------------------------+
| **3**   | Sophisticated/determined  | Independent review      |
+---------+---------------------------+-------------------------+

**Key Outputs:**

::

    1. Security Risk Assessment (SRA)
    2. Security Plan (SECP)
    3. Security Cases (evidence of compliance)
    4. Residual security risk statement

════════════════════════════════════════════════════════════════════

📖 **1. DO-326A FUNDAMENTALS**
══════════════════════════════

**1.1 Purpose & Scope**
----------------------

**DO-326A Purpose:**

- ✅ Establish process for security risk management in avionics
- ✅ Define Security Assurance Levels (SAL 1/2/3)
- ✅ Integrate security with safety (DO-178C, ARP4754A)
- ✅ Provide framework for certification authorities

**Scope:**

- **Airborne Systems:** FMS, IFE, EFB, ACARS, datalinks
- **Ground Systems:** ATCs, flight planning, maintenance
- **Interfaces:** Passenger WiFi, satellite links, USB ports
- **Lifecycle:** Development, operation, maintenance, disposal

**Relationship to Other Standards:**

::

    ┌────────────────────────────────────────────┐
    │       ARP4754A (System Safety)             │
    │   Functional Hazard Assessment (FHA)       │
    └───────────────┬────────────────────────────┘
                    │
                    ├──► DO-326A (Security Process)
                    │    ├─► Security Risk Assessment
                    │    └─► SAL Assignment
                    │
                    ├──► DO-178C (Software Development)
                    │    └─► DAL A/B/C/D/E
                    │
                    └──► DO-356A (Security Methods)
                         └─► Threat modeling, testing

**1.2 Security vs Safety**
--------------------------

**Key Difference:**

+-------------------+-------------------------+-------------------------+
| **Aspect**        | **Safety (ARP4754A)**   | **Security (DO-326A)**  |
+===================+=========================+=========================+
| Focus             | Unintentional failures  | Intentional attacks     |
+-------------------+-------------------------+-------------------------+
| Threat Source     | Random, environment     | Adversarial, intelligent|
+-------------------+-------------------------+-------------------------+
| Probability Model | Statistical (10⁻⁹/FH)   | Threat capability       |
+-------------------+-------------------------+-------------------------+
| Mitigation        | Redundancy, monitoring  | Isolation, encryption   |
+-------------------+-------------------------+-------------------------+
| Assurance Levels  | DAL A/B/C/D/E           | SAL 1/2/3               |
+-------------------+-------------------------+-------------------------+

**Example:**

::

    Safety Hazard:  "Sensor fails → incorrect altitude reading"
    Mitigation:     Triple-modular redundancy (3 sensors, voting)
    
    Security Threat: "Attacker injects false altitude data"
    Mitigation:      Cryptographic authentication, data diode

**1.3 Security Assurance Levels (SAL)**
---------------------------------------

**SAL 1: Casual/Opportunistic Threat**

- **Attacker Profile:**
  - Untrained individual
  - No special equipment
  - Opportunistic (finds open port, tries default password)
  
- **Examples:**
  - Passenger attempts to access cabin crew WiFi
  - Technician forgets to lock maintenance port
  - Public exploit available online (script kiddie)

- **Verification:**
  - Basic security testing
  - Code review for obvious vulnerabilities
  - Penetration test (automated tools)

**SAL 2: Intentional/Simple Means**

- **Attacker Profile:**
  - Trained individual (insider, contractor)
  - Limited resources ($1K-$10K budget)
  - Common attack tools (Metasploit, Nmap)
  
- **Examples:**
  - Disgruntled employee with system knowledge
  - Organized crime using off-the-shelf malware
  - Social engineering attack on airline staff

- **Verification:**
  - Comprehensive security analysis
  - Threat modeling (STRIDE, attack trees)
  - Manual penetration testing
  - Vulnerability scanning

**SAL 3: Sophisticated/Determined**

- **Attacker Profile:**
  - Expert team (nation-state, APT)
  - Significant resources ($100K+ budget)
  - Custom exploits, zero-days
  - Physical access capability
  
- **Examples:**
  - Nation-state espionage
  - Targeted campaign against specific airline
  - Supply chain compromise (hardware backdoor)

- **Verification:**
  - Independent security review
  - Red team exercises
  - Formal security analysis
  - Continuous monitoring
  - Regulatory audit

════════════════════════════════════════════════════════════════════

📖 **2. SECURITY RISK ASSESSMENT (SRA)**
════════════════════════════════════════

**2.1 SRA Process Overview**
----------------------------

**5-Step Process:**

::

    Step 1: Asset Identification
         ├─► What needs protection? (data, systems, services)
         └─► Criticality classification (safety, operational, business)
    
    Step 2: Threat Identification
         ├─► Who are the adversaries? (insider, nation-state, hacker)
         └─► What are their motivations? (financial, sabotage, espionage)
    
    Step 3: Vulnerability Analysis
         ├─► Where are the weaknesses? (code bugs, misconfigurations)
         └─► Attack vectors (network, physical, supply chain)
    
    Step 4: Risk Determination
         ├─► Likelihood × Impact = Risk Score
         └─► Assign SAL (1/2/3)
    
    Step 5: Mitigation Planning
         ├─► Security controls (technical, operational, procedural)
         └─► Residual risk acceptance

**2.2 Asset Identification**
----------------------------

**Asset Categories:**

.. code-block:: text

    ┌─────────────────────────────────────────────┐
    │ ASSETS TO PROTECT                           │
    ├─────────────────────────────────────────────┤
    │ 1. Safety-Critical Functions                │
    │    - Flight control algorithms              │
    │    - Navigation data (GPS, IRS)             │
    │    - Engine control parameters              │
    │                                             │
    │ 2. Operational-Critical Functions           │
    │    - ACARS messaging                        │
    │    - Weight & balance calculations          │
    │    - Maintenance logs                       │
    │                                             │
    │ 3. Sensitive Data                           │
    │    - Passenger PII (names, credit cards)    │
    │    - Flight plans (security-sensitive)      │
    │    - Crew credentials                       │
    │                                             │
    │ 4. Services & Availability                  │
    │    - In-Flight Entertainment (IFE)          │
    │    - Passenger WiFi                         │
    │    - Cockpit displays                       │
    └─────────────────────────────────────────────┘

**Asset Classification Matrix:**

+---------------------------+------------+-----------+---------+
| **Asset**                 | **Safety** | **Ops**   | **SAL** |
+===========================+============+===========+=========+
| Flight control algorithms | CRITICAL   | N/A       | 3       |
+---------------------------+------------+-----------+---------+
| Navigation data (GPS)     | HIGH       | HIGH      | 2-3     |
+---------------------------+------------+-----------+---------+
| Passenger PII             | N/A        | MEDIUM    | 2       |
+---------------------------+------------+-----------+---------+
| IFE system                | N/A        | LOW       | 1       |
+---------------------------+------------+-----------+---------+

**2.3 Threat Identification (STRIDE)**
--------------------------------------

**STRIDE Framework:**

.. code-block:: text

    S - Spoofing Identity
        Example: Attacker impersonates maintenance technician
        
    T - Tampering with Data
        Example: Modify flight plan waypoints in FMS
        
    R - Repudiation
        Example: Insider denies making unauthorized changes
        
    I - Information Disclosure
        Example: Intercept passenger credit card data
        
    D - Denial of Service
        Example: DDoS attack on passenger WiFi
        
    E - Elevation of Privilege
        Example: Escape from IFE to access crew systems

**STRIDE Applied to Aircraft Networks:**

+---------------------------+------------------+------------------------+
| **STRIDE Category**       | **ACD Example**  | **PIESD Example**      |
+===========================+==================+========================+
| Spoofing                  | Fake GPS signal  | Rogue WiFi AP          |
+---------------------------+------------------+------------------------+
| Tampering                 | Modify FMS data  | Corrupt IFE content    |
+---------------------------+------------------+------------------------+
| Repudiation               | Hide malware log | Delete access logs     |
+---------------------------+------------------+------------------------+
| Info Disclosure           | Exfiltrate plans | Steal passenger data   |
+---------------------------+------------------+------------------------+
| Denial of Service         | Crash FCC        | Flood WiFi (DDoS)      |
+---------------------------+------------------+------------------------+
| Privilege Escalation      | AISD → ACD jump  | Passenger → crew access|
+---------------------------+------------------+------------------------+

**2.4 Vulnerability Analysis**
------------------------------

**Common Avionics Vulnerabilities:**

.. code-block:: python

    # vulnerability_database.py
    
    AVIONICS_VULNERABILITIES = {
        'VUL-001': {
            'title': 'Weak WiFi Encryption (WPA2)',
            'description': 'Passenger WiFi uses WPA2 with known vulnerabilities',
            'cvss': 7.5,  # High
            'cwe': 'CWE-326',  # Inadequate Encryption Strength
            'affected_domain': 'PIESD',
            'exploit_complexity': 'Low',
            'mitigation': 'Upgrade to WPA3, implement 802.1X'
        },
        'VUL-002': {
            'title': 'Unencrypted Data Diode',
            'description': 'Data diode transmits in cleartext (eavesdropping risk)',
            'cvss': 5.3,  # Medium
            'cwe': 'CWE-319',  # Cleartext Transmission
            'affected_domain': 'ACD-AISD Interface',
            'exploit_complexity': 'Medium',
            'mitigation': 'Encrypt data diode traffic (AES-256)'
        },
        'VUL-003': {
            'title': 'USB Autorun Enabled',
            'description': 'Maintenance ports auto-execute files from USB',
            'cvss': 8.1,  # High
            'cwe': 'CWE-434',  # Unrestricted Upload
            'affected_domain': 'AISD',
            'exploit_complexity': 'Low',
            'mitigation': 'Disable autorun, scan all USB media'
        },
        'VUL-004': {
            'title': 'Hardcoded Credentials',
            'description': 'Default password "admin:admin123" in EFB',
            'cvss': 9.8,  # Critical
            'cwe': 'CWE-798',  # Hardcoded Credentials
            'affected_domain': 'AISD',
            'exploit_complexity': 'Low',
            'mitigation': 'Force password change on first use, MFA'
        }
    }

**2.5 Risk Determination**
--------------------------

**Risk Calculation:**

::

    Risk = Likelihood × Impact
    
    Likelihood Levels:
    - Frequent (5):  Multiple attacks per year
    - Probable (4):  ~1 attack per year
    - Remote (3):    ~1 attack per 10 years
    - Improbable (2): ~1 attack per 100 years
    - Extremely Remote (1): <1 attack per 1000 years
    
    Impact Levels:
    - Catastrophic (5): Loss of aircraft
    - Hazardous (4):    Serious injury
    - Major (3):        Significant disruption
    - Minor (2):        Inconvenience
    - No Safety Effect (1): Nuisance

**Risk Matrix:**

+-------------+---+---+---+---+---+
| Likelihood  |   | Impact Level  |
| ↓           | 1 | 2 | 3 | 4 | 5 |
+=============+===+===+===+===+===+
| **5**       | 5 |10 |15 |20 |25 |
| Frequent    |   |   |   |   |   |
+-------------+---+---+---+---+---+
| **4**       | 4 | 8 |12 |16 |20 |
| Probable    |   |   |   |   |   |
+-------------+---+---+---+---+---+
| **3**       | 3 | 6 | 9 |12 |15 |
| Remote      |   |   |   |   |   |
+-------------+---+---+---+---+---+
| **2**       | 2 | 4 | 6 | 8 |10 |
| Improbable  |   |   |   |   |   |
+-------------+---+---+---+---+---+
| **1**       | 1 | 2 | 3 | 4 | 5 |
| Ext. Remote |   |   |   |   |   |
+-------------+---+---+---+---+---+

**SAL Assignment:**

::

    Risk Score 1-8:   SAL 1 (Low risk)
    Risk Score 9-15:  SAL 2 (Medium risk)
    Risk Score 16-25: SAL 3 (High risk)

**Example:**

.. code-block:: python

    # risk_assessment.py
    
    threat = {
        'name': 'WiFi Man-in-the-Middle Attack',
        'domain': 'PIESD',
        'likelihood': 4,  # Probable (weak WPA2)
        'impact': 2,      # Minor (passenger data only)
        'risk_score': 4 * 2  # = 8
    }
    
    if threat['risk_score'] <= 8:
        sal = 1
    elif threat['risk_score'] <= 15:
        sal = 2
    else:
        sal = 3
    
    print(f"Threat: {threat['name']}")
    print(f"Risk Score: {threat['risk_score']}")
    print(f"Assigned SAL: {sal}")
    
    # Output:
    # Threat: WiFi Man-in-the-Middle Attack
    # Risk Score: 8
    # Assigned SAL: 1

════════════════════════════════════════════════════════════════════

📖 **3. SECURITY PLAN (SECP)**
══════════════════════════════

**3.1 SECP Structure**
---------------------

**Required Sections:**

.. code-block:: text

    1. Introduction
       ├─► System description
       ├─► Regulatory basis (DO-326A, FAA AC 20-170)
       └─► Certification path
    
    2. Security Organization
       ├─► Roles & responsibilities
       ├─► Security team structure
       └─► Authority interaction
    
    3. Security Risk Assessment Summary
       ├─► Asset inventory
       ├─► Threat landscape
       ├─► SAL assignments
       └─► Residual risks
    
    4. Security Development Process
       ├─► Security requirements development
       ├─► Secure coding practices
       ├─► Security verification & testing
       └─► Configuration management
    
    5. Security Evidence
       ├─► Test results
       ├─► Penetration test reports
       ├─► Independent review findings
       └─► Compliance matrices
    
    6. Certification Liaison
       ├─► Authority meetings schedule
       ├─► Issue resolution tracking
       └─► Compliance statement

**3.2 Security Requirements**
-----------------------------

**Types of Security Requirements:**

.. code-block:: text

    Derived Security Requirements (DSR):
    - Derived from Security Risk Assessment
    - Example: "System shall authenticate all maintenance USB devices"
    
    Allocated Security Requirements (ASR):
    - Allocated to specific components
    - Example: "EFB shall implement TLS 1.3 for ground link"
    
    Implementation Security Requirements (ISR):
    - Low-level, implementation-specific
    - Example: "Use OpenSSL 3.0+ for cryptographic functions"

**Security Requirements Traceability:**

::

    Threat (STRIDE)
         ↓
    Security Requirement (DSR)
         ↓
    Design Implementation (ASR)
         ↓
    Code Implementation (ISR)
         ↓
    Security Test Case
         ↓
    Test Result (Pass/Fail)

**3.3 Security Controls**
-------------------------

**Control Categories:**

+-------------------+---------------------------+------------------------+
| **Category**      | **Examples**              | **Domain Application** |
+===================+===========================+========================+
| Access Control    | MFA, RBAC, least privilege| AISD, PIESD            |
+-------------------+---------------------------+------------------------+
| Cryptography      | AES-256, TLS 1.3, ECDSA   | All domains            |
+-------------------+---------------------------+------------------------+
| Network Security  | Firewall, IDS/IPS, VLAN   | AISD ↔ PIESD           |
+-------------------+---------------------------+------------------------+
| Physical Security | Locks, tamper-evident     | ACD (avionics bays)    |
+-------------------+---------------------------+------------------------+
| Monitoring        | SIEM, anomaly detection   | All domains            |
+-------------------+---------------------------+------------------------+
| Secure Boot       | UEFI, code signing        | ACD, AISD              |
+-------------------+---------------------------+------------------------+

**Control Selection Matrix:**

.. code-block:: yaml

    # security_controls.yaml
    
    SAL_1_Controls:
      - Basic firewall (stateful)
      - Password authentication (8+ chars)
      - Antivirus scanning
      - Access logging
      - TLS 1.2+ encryption
    
    SAL_2_Controls:
      - Deep packet inspection firewall
      - Multi-factor authentication (MFA)
      - USB whitelisting
      - Intrusion detection system (IDS)
      - TLS 1.3+ with mutual auth
      - Security event correlation (SIEM)
    
    SAL_3_Controls:
      - Data diode (physical one-way)
      - Hardware security module (HSM)
      - Red team exercises (annual)
      - Formal security verification
      - TLS 1.3 + perfect forward secrecy
      - 24/7 security operations center (SOC)
      - Independent security audit

════════════════════════════════════════════════════════════════════

📖 **4. SECURITY VERIFICATION**
═══════════════════════════════

**4.1 Verification Activities by SAL**
--------------------------------------

**SAL 1 Verification:**

- ✅ Security requirements review
- ✅ Code walkthrough (manual inspection)
- ✅ Automated vulnerability scanning (Nessus, OpenVAS)
- ✅ Basic penetration testing (automated tools)
- ✅ Functional security testing

**SAL 2 Verification:**

- ✅ All SAL 1 activities
- ✅ Threat modeling workshop (STRIDE, attack trees)
- ✅ Manual penetration testing (expert-led)
- ✅ Fuzzing (protocol testing)
- ✅ Cryptographic validation (FIPS 140-2)
- ✅ Security architecture review

**SAL 3 Verification:**

- ✅ All SAL 2 activities
- ✅ Independent security review (external firm)
- ✅ Red team engagement (adversarial simulation)
- ✅ Formal security analysis (mathematical proofs)
- ✅ Supply chain security audit
- ✅ Continuous monitoring (SOC)
- ✅ Regulatory audit (FAA/EASA)

**4.2 Penetration Testing**
---------------------------

**Phases:**

.. code-block:: text

    Phase 1: Reconnaissance
         ├─► Network mapping (Nmap)
         ├─► Service enumeration
         └─► Vulnerability discovery
    
    Phase 2: Exploitation
         ├─► Attempt known exploits
         ├─► Custom exploit development (SAL 2/3)
         └─► Social engineering (SAL 3)
    
    Phase 3: Post-Exploitation
         ├─► Lateral movement attempts
         ├─► Privilege escalation
         └─► Data exfiltration simulation
    
    Phase 4: Reporting
         ├─► Findings documentation
         ├─► Risk rating (CVSS)
         └─► Remediation recommendations

**Sample Penetration Test Report:**

.. code-block:: markdown

    # Penetration Test Report: IFE System
    
    ## Executive Summary
    - Target: Passenger In-Flight Entertainment (PIESD)
    - Duration: 5 days
    - Methodology: OWASP Testing Guide v4
    - Findings: 3 High, 7 Medium, 12 Low
    
    ## Critical Findings
    
    ### FINDING-001: WiFi MITM Attack Possible
    - Severity: HIGH (CVSS 7.5)
    - Description: WPA2 encryption vulnerable to KRACK attack
    - Impact: Passenger data interception
    - Recommendation: Upgrade to WPA3, implement 802.1X
    
    ### FINDING-002: Cross-Domain Data Leak
    - Severity: MEDIUM (CVSS 5.3)
    - Description: Sanitized GPS data includes precise altitude
    - Impact: Operational security (reveals flight profile)
    - Recommendation: Round altitude to nearest 1,000 ft
    
    ## Remediation Verification
    - All HIGH findings must be fixed before certification
    - MEDIUM findings require risk acceptance or mitigation
    - LOW findings documented as residual risk

**4.3 Compliance Matrices**
---------------------------

**DO-326A Objective Compliance:**

+----------------+---------------------------+---------+-----------+
| **Objective**  | **Description**           | **SAL** | **Status**|
+================+===========================+=========+===========+
| OBJ-001        | Perform SRA               | 1/2/3   | ✅ Complete|
+----------------+---------------------------+---------+-----------+
| OBJ-002        | Develop SECP              | 1/2/3   | ✅ Complete|
+----------------+---------------------------+---------+-----------+
| OBJ-003        | Threat modeling (STRIDE)  | 2/3     | ✅ Complete|
+----------------+---------------------------+---------+-----------+
| OBJ-004        | Penetration testing       | 2/3     | ✅ Complete|
+----------------+---------------------------+---------+-----------+
| OBJ-005        | Independent review        | 3       | ✅ Complete|
+----------------+---------------------------+---------+-----------+
| OBJ-006        | Red team exercise         | 3       | 🟡 Planned |
+----------------+---------------------------+---------+-----------+

════════════════════════════════════════════════════════════════════

📖 **5. CERTIFICATION WORKFLOW**
════════════════════════════════

**5.1 Certification Phases**
----------------------------

**Timeline:**

::

    Month 1-3: Planning
         ├─► Security Risk Assessment
         ├─► SECP Development
         └─► Authority meeting #1 (concept review)
    
    Month 4-12: Development
         ├─► Security requirements implementation
         ├─► Security verification (testing)
         └─► Authority meeting #2 (design review)
    
    Month 13-18: Certification
         ├─► Independent security review (SAL 3)
         ├─► Compliance evidence assembly
         ├─► Authority meeting #3 (compliance demo)
         └─► Final certification (SAS approval)

**5.2 Authority Interaction**
-----------------------------

**FAA Issue Papers:**

.. code-block:: text

    Issue Paper Format:
    
    1. Issue Description
       - What is the security concern?
       - Example: "Data diode may leak information via timing"
    
    2. Proposed Approach
       - How will you address it?
       - Example: "Constant-rate transmission (eliminates timing channel)"
    
    3. Supporting Data
       - Evidence, analysis, test results
       - Example: "Timing analysis shows <1 bit/min covert channel"
    
    4. Authority Disposition
       - Approved / Rejected / More Info Needed
       - Follow-up actions

**5.3 Certification Evidence**
------------------------------

**Required Documentation:**

.. code-block:: text

    Security Accomplishment Summary (SAS):
    ├─► Security Risk Assessment Report
    ├─► Security Plan (SECP)
    ├─► Security Case (compliance evidence)
    │   ├─► Requirements traceability
    │   ├─► Test results
    │   ├─► Penetration test reports
    │   └─► Independent review findings
    ├─► Configuration index
    └─► Residual security risk statement

**Evidence Checklist (SAL 3):**

- [ ] Security Risk Assessment (SRA) approved
- [ ] Security Plan (SECP) approved
- [ ] All security requirements traced to threats
- [ ] All security tests passed (100% coverage)
- [ ] Penetration test findings remediated
- [ ] Independent security review complete
- [ ] Red team exercise passed
- [ ] Authority issue papers closed
- [ ] Residual risks documented & accepted
- [ ] Security Accomplishment Summary (SAS) signed

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** What is the difference between DO-326A and DO-178C?

**A1:**

**DO-326A (Security Process):**

- Focus: **Intentional threats** (attackers)
- Purpose: Security risk management
- Levels: SAL 1/2/3 (based on threat capability)
- Example: Prevent attacker from injecting false GPS data

**DO-178C (Safety Process):**

- Focus: **Unintentional failures** (random faults)
- Purpose: Software safety assurance
- Levels: DAL A/B/C/D/E (based on failure impact)
- Example: Prevent software bug causing crash

**Integration:** Both required for modern avionics (DO-326A + DO-178C)

────────────────────────────────────────────────────────────────────

**Q2:** Assign SAL to the following scenarios:

**Scenario A:** Passenger attempts to connect laptop to crew WiFi (fails immediately)

**A:** SAL 1 (Casual/opportunistic)

**Scenario B:** Disgruntled technician uses USB drive to upload malware to AISD

**A:** SAL 2 (Intentional/simple means)

**Scenario C:** Nation-state plants hardware backdoor in avionics supply chain

**A:** SAL 3 (Sophisticated/determined)

────────────────────────────────────────────────────────────────────

**Q3:** You're performing a Security Risk Assessment for a new IFE system. Walk through the 5 steps.

**A:**

**Step 1: Asset Identification**

- Assets: IFE content, passenger data, WiFi service
- Criticality: Low (no safety impact)

**Step 2: Threat Identification**

- Threats: DDoS, malware, data theft, unauthorized access
- Actors: Passengers, external attackers

**Step 3: Vulnerability Analysis**

- Vulnerabilities: Weak WiFi encryption (WPA2), no rate limiting, outdated firmware
- CVEs: CVE-2023-XXXX (known exploit)

**Step 4: Risk Determination**

- Likelihood: Probable (4) - Public exploits available
- Impact: Minor (2) - Passenger inconvenience only
- Risk Score: 4 × 2 = 8 → **SAL 1**

**Step 5: Mitigation Planning**

- Controls: Upgrade to WPA3, rate limiting, firmware update
- Residual risk: Accepted (low impact, cost-effective mitigation)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Understand SAL 1/2/3 definitions and threat profiles
- [ ] Perform Security Risk Assessment (SRA) using STRIDE
- [ ] Develop Security Plan (SECP) with traceability
- [ ] Assign SAL based on risk matrix (Likelihood × Impact)
- [ ] Select security controls appropriate for SAL
- [ ] Conduct penetration testing (SAL 2/3)
- [ ] Complete independent security review (SAL 3)
- [ ] Assemble compliance evidence (SAS)
- [ ] Interact with certification authority (issue papers)
- [ ] Document residual security risks

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **DO-326A complements DO-178C** → Security (intentional threats) + Safety 
(unintentional failures) = Comprehensive assurance

2️⃣ **SAL is threat-driven, not failure-driven** → Based on attacker capability 
(casual, intentional, sophisticated)

3️⃣ **Security Risk Assessment is foundational** → Assets → Threats → 
Vulnerabilities → Risk → SAL

4️⃣ **STRIDE is the standard threat model** → Spoofing, Tampering, Repudiation, 
Information Disclosure, Denial of Service, Elevation of Privilege

5️⃣ **SAL 3 requires independent review** → External security firm + red team 
exercises + continuous monitoring

6️⃣ **Security controls must match SAL** → SAL 1 = basic firewall; SAL 3 = 
data diode + HSM + SOC

7️⃣ **Residual risk must be documented** → Cannot eliminate all risks → Accept 
with justification

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **DO-326A AIRWORTHINESS SECURITY PROCESS COMPLETE**
**Created:** January 14, 2026
**Coverage:** Security Risk Assessment, SAL Assignment, Threat Modeling (STRIDE), 
Security Plan (SECP), Certification Workflow

════════════════════════════════════════════════════════════════════
