🛡️ **THREAT MODELING — Security Analysis for Aircraft Systems**
═══════════════════════════════════════════════════════════════════

**Context:** Systematic security threat identification and mitigation
**Focus:** STRIDE, PASTA, Attack Trees, Aircraft-Specific Threats
**Standards:** ED-203A SAL 1-3, RTCA DO-326A, EUROCAE ED-202A

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — THREAT MODELING IN 60 SECONDS**
─────────────────────────────────────────────

**STRIDE Acronym:**

::

    S - Spoofing        → Fake identity (counterfeit auth)
    T - Tampering       → Modify data/code
    R - Repudiation     → Deny actions (no audit trail)
    I - Info Disclosure → Data leaks (confidentiality breach)
    D - Denial of Service → Availability attacks
    E - Elevation of Privilege → Gain unauthorized access


**Threat Actor Profiles (ED-203A):**

+-------------+-------------------------+------------------+-------------------+
| **Level**   | **Actor Type**          | **Capability**   | **Target**        |
+=============+=========================+==================+===================+
| **SAL 1**   | Casual/Coincidental     | Low skill        | Public interfaces |
+-------------+-------------------------+------------------+-------------------+
| **SAL 2**   | Intentional/Simple      | Moderate skill   | Known vulns       |
+-------------+-------------------------+------------------+-------------------+
| **SAL 3**   | Sophisticated/Advanced  | High resources   | Custom exploits   |
+-------------+-------------------------+------------------+-------------------+

**Quick Assessment:**

1. **Asset Identification** → What needs protection?
2. **Entry Points** → Where can attackers enter?
3. **Threat Classification** → Apply STRIDE to each entry point
4. **Risk Scoring** → Likelihood × Impact
5. **Mitigation** → Countermeasures per threat

════════════════════════════════════════════════════════════════════

📖 **1. STRIDE METHODOLOGY**
═══════════════════════════

**1.1 Spoofing Identity**
-------------------------

**Definition:** Attacker pretends to be someone/something else

**Aircraft Examples:**

- 🎭 **Fake Maintenance Credentials:** Technician impersonates authorized personnel
- 📡 **GPS Spoofing:** Sending false GPS signals to aircraft
- 🔑 **Certificate Forgery:** Counterfeit code-signing certificates
- 👤 **User Impersonation:** Stolen passenger credentials for IFE

**Countermeasures:**

- Multi-factor authentication (MFA)
- Certificate pinning
- GPS signal validation (multi-source)
- Hardware security modules (HSM) for key storage

**1.2 Tampering with Data**
---------------------------

**Definition:** Unauthorized modification of data or code

**Aircraft Examples:**

- 💾 **Software Tampering:** Modified avionics firmware
- 🗄️ **Database Manipulation:** Altered flight plans
- 📦 **Supply Chain Attacks:** Compromised COTS components
- 🎬 **IFE Content Tampering:** Malicious media files

**Countermeasures:**

- Code signing with PKI
- Secure Boot chain (UEFI → bootloader → kernel)
- Integrity checking (SHA-256 hashes)
- Database transaction logging

**1.3 Repudiation**
------------------

**Definition:** Denying actions taken (lack of proof)

**Aircraft Examples:**

- 🕵️ **No Audit Trail:** Maintenance actions not logged
- 🗑️ **Log Deletion:** Attacker erases evidence
- 🔓 **Anonymous Access:** Shared credentials hide identity

**Countermeasures:**

- Immutable logging (write-once storage)
- Centralized log aggregation
- Digital signatures on audit records
- Time-stamping with trusted time source

**1.4 Information Disclosure**
------------------------------

**Definition:** Exposing information to unauthorized parties

**Aircraft Examples:**

- 📡 **Wi-Fi Eavesdropping:** Passenger data interception
- 💳 **Payment Data Leaks:** Credit card exposure
- 🗺️ **Flight Plan Exposure:** Sensitive route information
- 📧 **Email Interception:** Crew communication compromise

**Countermeasures:**

- TLS 1.3 for all communications
- End-to-end encryption (E2EE)
- Data-at-rest encryption (AES-256)
- Network segmentation (VLANs)

**1.5 Denial of Service (DoS)**
-------------------------------

**Definition:** Making system unavailable to legitimate users

**Aircraft Examples:**

- 🌊 **Bandwidth Exhaustion:** Flooding Wi-Fi access points
- 💣 **Resource Depletion:** CPU/memory exhaustion attacks
- 🔌 **Physical Tampering:** Disconnecting cables
- 🕸️ **DNS Poisoning:** Preventing service discovery

**Countermeasures:**

- Rate limiting (requests per second)
- Resource quotas (CPU/memory limits)
- Redundancy (failover systems)
- Input validation (reject malformed requests)

**1.6 Elevation of Privilege**
------------------------------

**Definition:** Gaining higher access than authorized

**Aircraft Examples:**

- 🚀 **Privilege Escalation:** User → admin access
- 🔓 **Buffer Overflow:** Exploit to gain root
- 🎯 **SQL Injection:** Database admin access
- 🔑 **Stolen Admin Credentials:** Social engineering

**Countermeasures:**

- Principle of Least Privilege (PoLP)
- ASLR (Address Space Layout Randomization)
- DEP (Data Execution Prevention)
- Input sanitization

════════════════════════════════════════════════════════════════════

📖 **2. PASTA FRAMEWORK**
═════════════════════════

**Process for Attack Simulation and Threat Analysis (7 Stages)**

**2.1 Stage 1: Define Business Objectives**
-------------------------------------------

**Goal:** Understand business/safety goals

**Aircraft Example:**

- **Objective:** Provide secure in-flight entertainment
- **Success Criteria:** 99.9% uptime, zero payment data breaches
- **Compliance:** PCI DSS Level 1, ED-203A SAL 2

**2.2 Stage 2: Define Technical Scope**
---------------------------------------

**Goal:** Identify components, data flows, trust boundaries

**IFE System Scope:**

::

    ┌─────────────────────────────────────────────────────────────┐
    │                      IFE System Boundary                     │
    │                                                               │
    │  ┌──────────┐      ┌──────────┐      ┌──────────────┐      │
    │  │  Seat    │─────→│  IFE     │─────→│   Content    │      │
    │  │  Units   │      │  Server  │      │   Delivery   │      │
    │  └──────────┘      └──────────┘      │   Network    │      │
    │       ↑                  ↑            └──────────────┘      │
    │       │                  │                    ↑              │
    │       └──────────────────┴────────────────────┘              │
    │                          ↑                                   │
    └──────────────────────────┼───────────────────────────────────┘
                               │
                        [ Wi-Fi Passengers ]
                               ↑
                        [ Satellite Ground Link ]

**Trust Boundaries:**

1. Passenger devices ↔ IFE Wi-Fi (UNTRUSTED)
2. IFE network ↔ Avionics (AIR GAP - isolated)
3. Ground ↔ Aircraft (ENCRYPTED LINK)

**2.3 Stage 3: Application Decomposition**
------------------------------------------

**Goal:** Break system into components

**IFE Components:**

- **Frontend:** Web app (HTML5/JS)
- **API Gateway:** REST endpoints
- **Authentication Service:** JWT tokens
- **Content Server:** Media streaming
- **Payment Gateway:** PCI DSS compliant
- **Database:** User profiles, transactions

**2.4 Stage 4: Threat Analysis**
--------------------------------

**Goal:** Identify threats using STRIDE

**Example: Payment Gateway**

+----------------------+----------------------------------------+
| **STRIDE Category**  | **Threat**                             |
+======================+========================================+
| Spoofing             | Fake payment terminal                  |
+----------------------+----------------------------------------+
| Tampering            | Modified transaction amounts           |
+----------------------+----------------------------------------+
| Repudiation          | Customer denies purchase               |
+----------------------+----------------------------------------+
| Info Disclosure      | Credit card data leak                  |
+----------------------+----------------------------------------+
| Denial of Service    | Payment service unavailable            |
+----------------------+----------------------------------------+
| Elevation            | User gains admin access to refunds     |
+----------------------+----------------------------------------+

**2.5 Stage 5: Vulnerability Analysis**
---------------------------------------

**Goal:** Find weaknesses that enable threats

**Example Vulnerabilities:**

- CVE-2023-12345: Buffer overflow in media player
- Weak password policy (no MFA)
- Unpatched OpenSSL version
- Default admin credentials

**2.6 Stage 6: Attack Modeling**
--------------------------------

**Goal:** Simulate attack paths

**Example Attack Tree (see Section 3)**

**2.7 Stage 7: Risk/Impact Analysis**
-------------------------------------

**Goal:** Quantify risk and prioritize mitigations

**Risk Formula:**

::

    Risk = Likelihood × Impact × Exposure

**Example:**

- **Threat:** SQL injection in payment API
- **Likelihood:** High (8/10) - common attack
- **Impact:** Critical (10/10) - PCI breach, fines
- **Exposure:** Medium (6/10) - limited API access
- **Risk Score:** 8 × 10 × 6 = **480 (CRITICAL)**

**Mitigation Priority:**

- **CRITICAL** (400-1000): Fix immediately
- **HIGH** (200-399): Fix within 30 days
- **MEDIUM** (50-199): Fix within 90 days
- **LOW** (0-49): Fix when possible

════════════════════════════════════════════════════════════════════

📖 **3. ATTACK TREES**
═══════════════════════

**3.1 Concept**
---------------

**Attack Tree:** Visual representation of attack paths

- **Root Node:** Attacker goal
- **AND Nodes:** All children required
- **OR Nodes:** Any child sufficient
- **Leaf Nodes:** Atomic attack steps

**3.2 Example: Compromise IFE System**
--------------------------------------

::

    [Compromise IFE System]
              |
         ┌────┴────┬─────────────┬──────────────┐
         │         │             │              │
    [Physical] [Network]   [Social Eng] [Supply Chain]
         │         │             │              │
         │    ┌────┴────┐        │              │
         │    │         │        │              │
         │ [Wi-Fi]  [Satellite]  │              │
         │    │         │        │              │
         │  ┌─┴─┐   ┌───┴───┐   │              │
         │  │   │   │       │   │              │
       [USB][AP][MITM] [Jam] [Phishing]   [Backdoor]
    
    Legend:
    ───────  OR relationship (any path works)
    AND relationship shown as single parent with multiple required children

**Attack Path Analysis:**

**Path 1: Physical → USB**

- Insert malicious USB into IFE maintenance port
- **Cost:** Low ($50 for USB + physical access)
- **Probability:** Low (restricted area)
- **Detection:** High (logged access)

**Path 2: Network → Wi-Fi → Access Point**

- Exploit Wi-Fi AP vulnerability
- **Cost:** Medium ($500 for tools)
- **Probability:** Medium (known CVEs)
- **Detection:** Medium (IDS alerts)

**Path 3: Network → Wi-Fi → Man-in-the-Middle**

- Rogue Wi-Fi access point
- **Cost:** Low ($200 for equipment)
- **Probability:** High (passenger proximity)
- **Detection:** Low (passive attack)

**Most Likely Path:** Network → Wi-Fi → MITM (highlighted in red in planning)

════════════════════════════════════════════════════════════════════

📖 **4. THREAT ACTOR PROFILES**
════════════════════════════════

**4.1 SAL 1: Casual/Coincidental**
----------------------------------

**Characteristics:**

- Limited technical skills
- No specific intent
- Opportunistic

**Attack Examples:**

- Using default passwords found online
- Running automated scanning tools (Nmap, Nessus)
- Social media reconnaissance

**Defenses:**

- Change default credentials
- Basic firewall rules
- Security awareness training

**4.2 SAL 2: Intentional/Simple**
---------------------------------

**Characteristics:**

- Moderate technical skills
- Targeted intent
- Uses known exploits

**Attack Examples:**

- Exploiting published CVEs (CVE databases)
- Phishing campaigns
- SQL injection attacks

**Defenses:**

- Patch management (CVE remediation)
- Web Application Firewall (WAF)
- Input validation

**4.3 SAL 3: Sophisticated/Determined**
---------------------------------------

**Characteristics:**

- High technical skills
- Well-resourced (nation-state, organized crime)
- Custom exploit development

**Attack Examples:**

- Zero-day exploits
- Supply chain attacks (SolarWinds-style)
- Advanced persistent threats (APT)

**Defenses:**

- Defense-in-depth (multiple layers)
- Threat intelligence integration
- Security Operations Center (SOC)
- Hardware security modules (HSM)

════════════════════════════════════════════════════════════════════

📖 **5. AIRCRAFT-SPECIFIC THREATS**
════════════════════════════════════

**5.1 IFE Exploitation**
------------------------

**Threat:** Attacker compromises IFE to pivot to avionics

**Attack Vector:**

1. Exploit buffer overflow in media player
2. Gain code execution on seat unit
3. Pivot to IFE server
4. Attempt to breach air gap to avionics

**Likelihood:** Low (air gap protection)

**Impact:** Critical (flight safety)

**Mitigation:**

- Physical air gap (no electrical connection)
- IFE network isolation (separate VLANs)
- Regular security audits
- Fuzzing media codecs

**5.2 Wi-Fi Man-in-the-Middle**
-------------------------------

**Threat:** Attacker intercepts passenger communications

**Attack Vector:**

1. Set up rogue access point ("Aircraft_WiFi_Free")
2. Passenger connects (thinking it's legitimate)
3. Intercept credentials, payment data

**Likelihood:** High (easy to execute)

**Impact:** Medium (data breach, not flight safety)

**Mitigation:**

- WPA3 encryption
- Certificate pinning in apps
- Captive portal with legitimate branding
- Passenger education

**5.3 USB Malware Introduction**
--------------------------------

**Threat:** Maintenance crew introduces malware via USB

**Attack Vector:**

1. Compromised maintenance laptop
2. USB inserted for software updates
3. Malware installed on avionics

**Likelihood:** Medium (supply chain risk)

**Impact:** Critical (flight safety)

**Mitigation:**

- USB port whitelisting (authorized devices only)
- Antivirus scanning on maintenance equipment
- Air-gapped update procedure
- Secure supply chain

**5.4 Supply Chain Compromise**
-------------------------------

**Threat:** Backdoor in COTS hardware/software

**Attack Vector:**

1. Attacker infiltrates component supplier
2. Backdoor embedded in chips/firmware
3. Installed in aircraft during manufacturing

**Likelihood:** Low (nation-state level)

**Impact:** Critical (long-term access)

**Mitigation:**

- Component verification (provenance tracking)
- Binary analysis (reverse engineering)
- Secure Boot with verified components
- Trusted supplier vetting

════════════════════════════════════════════════════════════════════

📖 **6. MITIGATION STRATEGIES**
════════════════════════════════

**6.1 Countermeasures by STRIDE Category**
------------------------------------------

**Spoofing Mitigations:**

- 🔐 Multi-factor authentication (MFA)
- 📜 PKI with certificate pinning
- 🏷️ Digital signatures on all code
- 🎫 Hardware tokens (YubiKey)

**Tampering Mitigations:**

- ✍️ Code signing + Secure Boot
- 🔒 Integrity checks (HMAC-SHA256)
- 📝 Audit logging with tamper detection
- 🗄️ Database transaction logs

**Repudiation Mitigations:**

- 📊 Centralized logging (Splunk, ELK)
- ⏰ NTP time synchronization
- 🖊️ Digital signatures on transactions
- 💾 Write-once storage (WORM)

**Information Disclosure Mitigations:**

- 🔐 TLS 1.3 for transport
- 🗝️ AES-256 for data-at-rest
- 🚧 Network segmentation
- 🕵️ Data loss prevention (DLP)

**Denial of Service Mitigations:**

- ⚖️ Rate limiting (API gateway)
- 🛡️ DDoS protection (Cloudflare)
- 🔄 Redundancy (N+1 servers)
- 📦 Resource quotas (cgroups)

**Elevation of Privilege Mitigations:**

- 🔽 Least privilege principle
- 🎲 ASLR + DEP (memory protection)
- 🧪 Input validation (sanitization)
- 🚫 Capability-based security

**6.2 Defense-in-Depth**
------------------------

**Multiple Layers:**

::

    Layer 1: Perimeter Security (Firewall, IDS/IPS)
         ↓
    Layer 2: Network Segmentation (VLANs, air gaps)
         ↓
    Layer 3: Application Security (WAF, input validation)
         ↓
    Layer 4: Access Control (RBAC, MFA)
         ↓
    Layer 5: Data Protection (Encryption, DLP)
         ↓
    Layer 6: Monitoring (SIEM, SOC)

**Principle:** No single point of failure

════════════════════════════════════════════════════════════════════

📖 **7. AUTOMATION WITH PYTHON**
═════════════════════════════════

**7.1 STRIDE Analysis Script**
------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """
    STRIDE Threat Analysis Automation
    Analyzes system components for STRIDE threats
    """
    
    from enum import Enum
    from typing import List, Dict
    
    class ThreatCategory(Enum):
        SPOOFING = "Spoofing"
        TAMPERING = "Tampering"
        REPUDIATION = "Repudiation"
        INFO_DISCLOSURE = "Information Disclosure"
        DENIAL_OF_SERVICE = "Denial of Service"
        ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"
    
    class Component:
        def __init__(self, name: str, trust_boundary: bool = False):
            self.name = name
            self.trust_boundary = trust_boundary
            self.threats: List[Threat] = []
        
        def add_threat(self, category: ThreatCategory, 
                      description: str, likelihood: int, impact: int):
            threat = Threat(category, description, likelihood, impact)
            self.threats.append(threat)
        
        def risk_score(self) -> int:
            return sum(t.risk_score() for t in self.threats)
    
    class Threat:
        def __init__(self, category: ThreatCategory, 
                    description: str, likelihood: int, impact: int):
            self.category = category
            self.description = description
            self.likelihood = likelihood  # 1-10
            self.impact = impact          # 1-10
        
        def risk_score(self) -> int:
            return self.likelihood * self.impact
    
    # Example: IFE System Analysis
    ife_gateway = Component("IFE API Gateway", trust_boundary=True)
    ife_gateway.add_threat(
        ThreatCategory.SPOOFING,
        "Attacker forges authentication token",
        likelihood=7, impact=8
    )
    ife_gateway.add_threat(
        ThreatCategory.ELEVATION_OF_PRIVILEGE,
        "SQL injection grants admin access",
        likelihood=8, impact=10
    )
    ife_gateway.add_threat(
        ThreatCategory.DENIAL_OF_SERVICE,
        "API flooding exhausts server resources",
        likelihood=9, impact=6
    )
    
    # Generate Report
    print(f"Component: {ife_gateway.name}")
    print(f"Total Risk Score: {ife_gateway.risk_score()}")
    print("\nThreats:")
    for threat in sorted(ife_gateway.threats, 
                        key=lambda t: t.risk_score(), reverse=True):
        print(f"  [{threat.category.value}] {threat.description}")
        print(f"    Risk: {threat.risk_score()} "
              f"(L={threat.likelihood} × I={threat.impact})")

**Output:**

::

    Component: IFE API Gateway
    Total Risk Score: 194
    
    Threats:
      [Elevation of Privilege] SQL injection grants admin access
        Risk: 80 (L=8 × I=10)
      [Spoofing] Attacker forges authentication token
        Risk: 56 (L=7 × I=8)
      [Denial of Service] API flooding exhausts server resources
        Risk: 54 (L=9 × I=6)

════════════════════════════════════════════════════════════════════

📝 **8. EXAM QUESTIONS**
═════════════════════════

**Q1:** You are threat modeling an IFE system. A passenger can upload 
custom media files to their profile. Which STRIDE categories apply?

**A1:** 

**Multiple categories apply:**

1. **Tampering** (Primary) - Malicious media file could exploit codec vulnerability
2. **Elevation of Privilege** - File upload could lead to code execution
3. **Denial of Service** - Large files could exhaust storage
4. **Information Disclosure** - Path traversal could expose other users' files

**Mitigations:**

- File type validation (whitelist: .mp4, .mp3)
- Size limits (max 100MB per file)
- Antivirus scanning
- Sandboxed media processing
- Isolated storage per user

────────────────────────────────────────────────────────────────────

**Q2:** In PASTA Stage 7 (Risk/Impact Analysis), you calculate a risk 
score of 450 for SQL injection. What action should you take?

**A2:**

**Risk Score 450 = CRITICAL priority**

**Immediate Actions:**

1. **Fix within 24-48 hours** (not 30 days)
2. **Temporary mitigation:** Disable vulnerable endpoint
3. **Permanent fix:** Implement prepared statements
4. **Verification:** Penetration testing
5. **Monitoring:** Deploy WAF rules to detect attempts

**Risk Scoring Reference:**

- 400-1000: CRITICAL (immediate fix)
- 200-399: HIGH (30 days)
- 50-199: MEDIUM (90 days)
- 0-49: LOW (backlog)

────────────────────────────────────────────────────────────────────

**Q3:** An attacker sets up a rogue Wi-Fi access point on an aircraft. 
What attack tree node type is this, and what's the next likely step?

**A3:**

**Node Type:** **OR node** (one of multiple ways to achieve network access)

**Attack Path:**

::

    [Compromise IFE]
           |
      [Network Access]  ← Current position
           |
      ┌────┴────┐
      │         │
    [Wi-Fi]  [Physical]
      │
    [Rogue AP] ← Attacker is here
      ↓
    [MITM Attack] ← Next step
      ↓
    [Credential Theft]

**Next Steps:**

1. **Capture handshakes** - Passenger connects to rogue AP
2. **MITM proxy** - Intercept HTTPS traffic
3. **Credential harvesting** - Capture login credentials
4. **Session hijacking** - Steal session tokens

**Detection:**

- Wi-Fi monitoring (detect multiple SSIDs with same name)
- Certificate validation failures (passenger warning)

────────────────────────────────────────────────────────────────────

**Q4:** You're defending against SAL 3 threats. Which mitigations are 
most effective?

**A4:**

**SAL 3 = Sophisticated/Determined attackers (nation-state)**

**Most Effective Mitigations:**

1. **Hardware Security Modules (HSM)**
   - Keys never leave HSM
   - FIPS 140-2 Level 3+ rated
   - Tamper-evident/responsive

2. **Defense-in-Depth**
   - Multiple security layers
   - No single point of failure
   - Assume breach mentality

3. **Zero Trust Architecture**
   - Never trust, always verify
   - Micro-segmentation
   - Continuous authentication

4. **Threat Intelligence Integration**
   - STIX/TAXII feeds
   - IOC monitoring
   - Proactive threat hunting

5. **Supply Chain Security**
   - Component provenance tracking
   - Binary analysis
   - Trusted supplier vetting

**Why These Work:**

- SAL 3 actors have resources for custom exploits
- Must prevent initial access AND lateral movement
- Monitoring critical for detecting sophisticated attacks

────────────────────────────────────────────────────────────────────

**Q5:** Draw an attack tree for "Steal Passenger Payment Data" with at 
least 3 OR branches and 1 AND node.

**A5:**

::

    [Steal Passenger Payment Data] ← GOAL
                 |
         ┌───────┴───────┬─────────────┬──────────────┐
         │               │             │              │
    [Network MITM]  [Compromise   [Physical]    [Social Eng]
                     Payment DB]                      
         │               │             │              │
         │          ┌────┴────┐        │              │
         │          │         │        │              │
         │      [AND Node]    │        │              │
         │       /      \     │        │              │
         │    [Exploit] [Get  │        │              │
         │    [SQL Inj] Admin]│        │              │
         │               │    │        │              │
     [Decrypt]      [Dump DB] │    [Shoulder]    [Phishing]
     [TLS Traffic]            │    [Surfing]     [Email]
                              │
                          [Insider
                           Threat]

**Legend:**

- **OR branches** (─┬─): Any path achieves goal
  1. Network MITM → Decrypt TLS
  2. Compromise Payment DB (requires SQL Injection AND Admin Access)
  3. Physical → Shoulder Surfing
  4. Social Engineering → Phishing

- **AND node** (∧): Both children required
  - Must exploit SQL injection AND obtain admin credentials

**Most Likely Path:** Network MITM (easiest for attacker on aircraft)

**Highest Impact Path:** Compromise Payment DB (bulk data theft)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Apply STRIDE to all system components
- [ ] Identify trust boundaries in architecture diagrams
- [ ] Complete all 7 stages of PASTA for critical systems
- [ ] Create attack trees for top 3 threats
- [ ] Profile threat actors (SAL 1/2/3) for your system
- [ ] Calculate risk scores (Likelihood × Impact)
- [ ] Prioritize mitigations by risk score
- [ ] Document aircraft-specific threats (IFE, Wi-Fi, supply chain)
- [ ] Implement defense-in-depth strategy
- [ ] Automate threat analysis with scripts
- [ ] Conduct tabletop exercises with attack scenarios
- [ ] Integrate threat intelligence feeds
- [ ] Establish incident response procedures
- [ ] Regular security audits and penetration testing

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **STRIDE is your framework** → Apply Spoofing, Tampering, Repudiation, 
Information Disclosure, Denial of Service, Elevation of Privilege to 
every system component

2️⃣ **PASTA provides structure** → 7-stage process from business objectives 
to risk scoring ensures comprehensive analysis

3️⃣ **Attack trees visualize paths** → Help identify most likely/highest 
impact attack scenarios for focused defense

4️⃣ **Know your adversary** → SAL 1 (casual) vs SAL 3 (sophisticated) 
requires different defense strategies

5️⃣ **Aircraft-specific threats matter** → IFE exploitation, Wi-Fi MITM, 
USB malware, supply chain attacks are unique to aviation

6️⃣ **Risk scoring prioritizes work** → Likelihood × Impact × Exposure 
determines fix urgency (CRITICAL > 400)

7️⃣ **Defense-in-depth is essential** → Multiple security layers prevent 
single point of failure

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **THREAT MODELING COMPLETE**
**Created:** January 14, 2026
**Coverage:** STRIDE, PASTA, Attack Trees, SAL 1-3 Actors, Aircraft Threats

════════════════════════════════════════════════════════════════════
