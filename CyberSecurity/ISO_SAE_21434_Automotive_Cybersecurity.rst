🚗 **ISO/SAE 21434 — AUTOMOTIVE CYBERSECURITY**
═══════════════════════════════════════════════════════════════════════

**Road Vehicles — Cybersecurity Engineering (ISO/SAE 21434:2021)**  
**Purpose:** Automotive lifecycle security 🔄 | Risk assessment 🎯 | CSMS framework 🛡️  
**Status:** International standard (mandatory for new vehicles in many markets)

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**ISO 21434** is the **automotive cybersecurity standard** covering the **entire vehicle lifecycle** from concept to decommissioning.

**Key concepts:**
- **CSMS:** Cybersecurity Management System (organizational processes)
- **TARA:** Threat Analysis and Risk Assessment
- **CAL:** Cybersecurity Assurance Levels (CAL 1-4, like ASIL for security)
- **Integration:** Works with ISO 26262 (safety), UNECE R155/R156 (regulations)

**Mandatory:** EU, Japan, Korea (via UN R155 type approval)

════════════════════════════════════════════════════════════════════════════

🏗️ **STANDARD STRUCTURE**
─────────────────────────────────────────────────────────────────────────

**ISO 21434 Organization (15 Clauses):**

.. code-block:: text

   Organizational Level:
   ├─ Clause 5: Organizational Cybersecurity Management
   ├─ Clause 6: Project-Dependent Cybersecurity Management
   └─ Clause 7: Distributed Cybersecurity Activities
   
   Product Development (V-Model):
   ├─ Clause 8: Concept Phase
   │   └─ Item definition, TARA, cybersecurity goals
   ├─ Clause 9: Product Development
   │   ├─ System design, HW/SW development
   │   └─ Integration & verification
   ├─ Clause 10: Cybersecurity Validation
   └─ Clause 11: Production
   
   Post-Production:
   ├─ Clause 12: Operations & Maintenance
   ├─ Clause 13: End of Cybersecurity Support / Decommissioning
   
   Cross-Cutting:
   ├─ Clause 14: Threat Information Sharing
   └─ Clause 15: Cybersecurity Audits

**V-Model Alignment with ISO 26262:**

.. code-block:: text

   Concept Phase (Clause 8)
   ├─ Item definition
   ├─ TARA (Threat Analysis & Risk Assessment)
   ├─ Cybersecurity goals (CAL assignment)
   └─ Cybersecurity concept
   
   Development Phase (Clause 9)
   ├─ System design
   │   ├─ Architecture with trust boundaries
   │   ├─ Cybersecurity requirements
   │   └─ Interface specifications
   ├─ Hardware development
   │   ├─ HSM integration
   │   ├─ Secure boot implementation
   │   └─ Physical tamper protection
   └─ Software development
       ├─ Secure coding (MISRA C with security extensions)
       ├─ Cryptographic implementations
       └─ Penetration testing
   
   Validation Phase (Clause 10)
   ├─ Vulnerability scanning
   ├─ Penetration testing
   ├─ Fuzz testing
   └─ Red team assessment (CAL 4)
   
   Production Phase (Clause 11)
   └─ Key provisioning, secure manufacturing
   
   Post-Production (Clauses 12-13)
   ├─ Vulnerability monitoring
   ├─ Incident response
   ├─ OTA updates
   └─ Decommissioning (key revocation)

════════════════════════════════════════════════════════════════════════════

🎯 **TARA — THREAT ANALYSIS & RISK ASSESSMENT**
─────────────────────────────────────────────────────────────────────────

**TARA Process (Clause 8, Annex H):**

**Step 1: Asset Identification**

.. code-block:: python

   class VehicleAsset:
       def __init__(self, name, asset_type, damage_scenarios):
           self.name = name
           self.asset_type = asset_type  # Data, Function, Component
           self.damage_scenarios = damage_scenarios
           self.cybersecurity_properties = {
               'confidentiality': False,
               'integrity': False,
               'availability': False
           }
   
   # Example: Engine Control Module
   ecm_asset = VehicleAsset(
       name="Engine Control Module",
       asset_type="Component",
       damage_scenarios=[
           {
               'scenario': 'Unauthorized engine tuning',
               'safety_impact': 'ASIL D (potential loss of vehicle control)',
               'financial_impact': 'Warranty claims, emissions violations',
               'operational_impact': 'Engine damage, reduced lifespan',
               'privacy_impact': 'None'
           },
           {
               'scenario': 'Denial of service (engine shutdown)',
               'safety_impact': 'ASIL D (loss of propulsion)',
               'financial_impact': 'Towing costs, brand reputation',
               'operational_impact': 'Vehicle inoperable',
               'privacy_impact': 'None'
           }
       ]
   )
   
   # Determine cybersecurity properties
   ecm_asset.cybersecurity_properties['integrity'] = True  # Prevent unauthorized tuning
   ecm_asset.cybersecurity_properties['availability'] = True  # Prevent DoS

**Step 2: Threat Scenario Identification (STRIDE)**

.. code-block:: python

   class ThreatScenario:
       def __init__(self, asset, threat_category, attack_path, attack_feasibility):
           self.asset = asset
           self.threat_category = threat_category  # STRIDE
           self.attack_path = attack_path
           self.attack_feasibility = attack_feasibility  # High/Medium/Low/Very Low
       
       def calculate_risk(self, impact):
           """ISO 21434 risk matrix"""
           feasibility_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4}
           impact_map = {'Negligible': 1, 'Moderate': 2, 'Major': 3, 'Severe': 4}
           
           risk_score = feasibility_map[self.attack_feasibility] + impact_map[impact]
           
           if risk_score >= 7:
               return 'High Risk'
           elif risk_score >= 5:
               return 'Medium Risk'
           else:
               return 'Low Risk'
   
   # Threat: Remote ECM reflash via OBD-II
   threat_ecm_reflash = ThreatScenario(
       asset=ecm_asset,
       threat_category='Tampering',
       attack_path=[
           'Attacker gains physical access to OBD-II port',
           'Connects malicious scan tool',
           'Exploits diagnostic protocol vulnerability',
           'Flashes unauthorized ECM firmware'
       ],
       attack_feasibility='Medium'  # Requires OBD tool + exploit knowledge
   )
   
   risk = threat_ecm_reflash.calculate_risk('Severe')
   print(f"Risk Level: {risk}")  # Output: High Risk

**Step 3: Impact Rating (ISO 21434 Table A.1)**

| Impact Category | Severe (4) | Major (3) | Moderate (2) | Negligible (1) |
|:----------------|:-----------|:----------|:-------------|:---------------|
| **Safety** | ASIL D (life-threatening) | ASIL C (serious injury) | ASIL B (light injury) | ASIL QM (no injury) |
| **Financial** | >$100M loss | $10M-$100M | $1M-$10M | <$1M |
| **Operational** | Complete vehicle loss | Major functionality loss | Minor functionality loss | No impact |
| **Privacy** | Sensitive data breach (medical, location tracking) | Personal data breach | Anonymized data | No data exposure |

**Step 4: Attack Feasibility Rating (ISO 21434 Annex G)**

| Factor | High (4) | Medium (3) | Low (2) | Very Low (1) |
|:-------|:---------|:-----------|:--------|:-------------|
| **Elapsed Time** | <1 day | <1 month | <6 months | >6 months |
| **Specialist Expertise** | Layperson | Proficient | Expert | Multiple experts |
| **Knowledge of Item** | Public | Restricted | Confidential | Strictly confidential |
| **Window of Opportunity** | Unlimited | Easy | Moderate | Difficult |
| **Equipment** | Standard (<$1K) | Specialized ($1K-$10K) | Bespoke ($10K-$100K) | Multiple bespoke (>$100K) |

**Attack Feasibility = Σ(factors) / 5 (rounded up)**

**Step 5: Risk Determination**

.. code-block:: python

   def determine_risk(attack_feasibility, impact):
       """ISO 21434 Risk Matrix"""
       # Feasibility: 1 (Very Low) to 4 (High)
       # Impact: 1 (Negligible) to 4 (Severe)
       
       risk_value = attack_feasibility + impact
       
       if risk_value >= 7:
           return 'CAL 4', 'High Risk - Requires extensive mitigations'
       elif risk_value >= 5:
           return 'CAL 3', 'Medium Risk - Requires mitigations'
       elif risk_value >= 3:
           return 'CAL 2', 'Low Risk - Basic mitigations'
       else:
           return 'CAL 1', 'Very Low Risk - Minimal mitigations'
   
   # Example: ECM reflash threat
   cal_level, risk_desc = determine_risk(
       attack_feasibility=3,  # Medium
       impact=4               # Severe
   )
   
   print(f"Assigned CAL: {cal_level}")  # CAL 4
   print(f"Risk: {risk_desc}")

════════════════════════════════════════════════════════════════════════════

🔐 **CAL — CYBERSECURITY ASSURANCE LEVELS**
─────────────────────────────────────────────────────────────────────────

**CAL 1-4 (Similar to ASIL for Safety):**

| CAL | Risk Level | Verification Requirements | Example Systems |
|:----|:-----------|:--------------------------|:----------------|
| **CAL 1** | Low | Basic testing, code review | Radio, HVAC controls |
| **CAL 2** | Medium | Vulnerability scanning, static analysis | Infotainment, door locks |
| **CAL 3** | High | Penetration testing, fuzz testing, dynamic analysis | Gateway ECU, telematics |
| **CAL 4** | Critical | Red team assessment, formal verification, independent security audit | Powertrain, ADAS, braking |

**CAL-Specific Requirements:**

**CAL 1:**
- Secure coding guidelines (MISRA C)
- Basic input validation
- Code review by peers

**CAL 2 (adds):**
- Static analysis tools (Coverity, Klocwork)
- Vulnerability scanning
- Secure boot recommended

**CAL 3 (adds):**
- Penetration testing (black-box, grey-box)
- Fuzz testing (AFL++, Honggfuzz)
- Dynamic analysis (ASAN, Valgrind)
- Secure boot required
- Cryptographic protections (authentication, encryption)

**CAL 4 (adds):**
- Red team assessment (dedicated adversarial team)
- Formal verification (SPARK, Frama-C for critical code)
- Independent security audit (third-party)
- Hardware security module (HSM) required
- Continuous monitoring & threat intelligence

════════════════════════════════════════════════════════════════════════════

🛡️ **CYBERSECURITY CONCEPT & REQUIREMENTS**
─────────────────────────────────────────────────────────────────────────

**Cybersecurity Goal → Cybersecurity Claim → Cybersecurity Requirement:**

.. code-block:: text

   Cybersecurity Goal (high-level):
   "Prevent unauthorized modification of ECM software"
   
   Cybersecurity Claim (decomposed):
   1. Only authenticated software shall be executed
   2. Software integrity shall be verified before execution
   3. Rollback attacks shall be prevented
   
   Cybersecurity Requirements (detailed):
   REQ-SEC-001: ECM shall implement secure boot per AUTOSAR standard
   REQ-SEC-002: ECM shall verify ECDSA-P256 signature before executing software
   REQ-SEC-003: ECM shall reject software with version < current version
   REQ-SEC-004: ECM shall store software version in tamper-resistant memory
   REQ-SEC-005: ECM shall log all software update attempts (timestamp, result)

**Example Implementation:**

.. code-block:: c

   // REQ-SEC-002: Verify ECDSA-P256 signature
   bool verify_ecm_software(const uint8_t *software, size_t size) {
       // Extract signature from software footer
       const uint8_t *signature = software + size - 64;
       
       // Calculate SHA-256 hash
       uint8_t hash[32];
       SHA256(software, size - 64, hash);
       
       // Load OEM public key (stored in secure flash)
       EC_KEY *oem_pubkey = load_oem_pubkey();
       
       // Verify ECDSA signature
       int result = ECDSA_verify(0, hash, 32, signature, 64, oem_pubkey);
       
       EC_KEY_free(oem_pubkey);
       
       if (result != 1) {
           log_security_event(SW_SIG_FAIL);
           return false;  // REQ-SEC-002 enforced
       }
       
       return true;
   }
   
   // REQ-SEC-003: Reject rollback
   bool check_software_version(uint32_t new_version) {
       uint32_t current_version = read_secure_version();
       
       if (new_version < current_version) {
           log_security_event(VERSION_ROLLBACK_ATTEMPT, new_version);
           return false;  // REQ-SEC-003 enforced
       }
       
       return true;
   }

════════════════════════════════════════════════════════════════════════════

🔄 **CSMS — CYBERSECURITY MANAGEMENT SYSTEM**
─────────────────────────────────────────────────────────────────────────

**Organizational Requirements (Clause 5):**

**Elements of CSMS:**

1. **Cybersecurity Policy**
   - Top management commitment
   - Scope (entire organization or specific divisions)
   - Integration with quality management (ISO 9001)

2. **Roles & Responsibilities**
   - Cybersecurity Officer (executive sponsor)
   - Cybersecurity Team (engineers, analysts)
   - Product Security Incident Response Team (PSIRT)

3. **Competence & Training**
   - Security awareness training (annual)
   - Specialized training (penetration testing, threat modeling)
   - Certification (CISSP, CEH, OSCP recommended)

4. **Continuous Improvement**
   - Lessons learned from incidents
   - Metrics (vulnerabilities found/fixed, time to patch)
   - Management review (quarterly)

**CSMS Audit Checklist:**

.. code-block:: text

   ☑ Cybersecurity policy documented & communicated
   ☑ Cybersecurity Officer appointed
   ☑ PSIRT established (24/7 contact)
   ☑ Vulnerability disclosure policy published
   ☑ Security training completed (all engineers)
   ☑ Penetration testing performed (annual)
   ☑ Threat intelligence feeds integrated
   ☑ Incident response plan tested (tabletop exercise)
   ☑ Supplier cybersecurity assessments conducted
   ☑ Cybersecurity metrics tracked & reported

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: How does ISO 21434 integrate with ISO 26262 (functional safety)?**

**A1:**

**Integration Points:**

| Aspect | ISO 26262 (Safety) | ISO 21434 (Security) | Integration |
|:-------|:-------------------|:---------------------|:------------|
| **Risk metric** | ASIL (A-D) | CAL (1-4) | Combined assessment |
| **Threat model** | Random failures | Adversarial attacks | Security failures → safety hazards |
| **V-Model** | Safety lifecycle | Security lifecycle | Parallel processes |
| **Verification** | Safety testing | Penetration testing | Combined test plans |

**Example:**
- **ASIL D braking system** (safety-critical)
- **Threat:** Attacker remotely disables brakes via CAN bus
- **Security requirement:** CAN authentication (AUTOSAR SecOC)
- **Combined requirement:** Braking system must be **ASIL D + CAL 4**

**Key principle:** Security enables safety (if security compromised, safety cannot be guaranteed).

**Q2: Explain the TARA process and its output.**

**A2:**

**TARA (Threat Analysis & Risk Assessment):**

**Inputs:**
- Item definition (system architecture, interfaces)
- Damage scenarios (safety, financial, operational, privacy impacts)

**Process:**
1. **Asset identification:** What needs protection? (ECU firmware, CAN data, V2X keys)
2. **Threat scenarios:** How can it be attacked? (STRIDE analysis)
3. **Attack feasibility:** How difficult? (Elapsed time, expertise, equipment)
4. **Impact rating:** How severe? (Severe, Major, Moderate, Negligible)
5. **Risk determination:** Feasibility + Impact → CAL level

**Outputs:**
- List of threat scenarios (prioritized by risk)
- CAL assignment per cybersecurity goal
- Cybersecurity goals (high-level security objectives)
- Cybersecurity concept (architecture decisions)

**Example Output:**
```
Threat: Remote ECM reflash via OBD-II
Attack Feasibility: Medium (3/4)
Impact: Severe (4/4)
Risk: High (CAL 4)
Cybersecurity Goal: Prevent unauthorized ECM software modification
```

**Q3: What are the key differences between CAL 2 and CAL 4?**

**A3:**

| Aspect | CAL 2 | CAL 4 |
|:-------|:------|:------|
| **Risk level** | Medium | Critical (safety-related) |
| **Verification** | Vulnerability scanning, static analysis | Red team, formal verification, independent audit |
| **Cryptography** | Optional | HSM required, FIPS 140-2 Level 2+ |
| **Secure boot** | Recommended | Mandatory |
| **Penetration testing** | Basic (automated tools) | Advanced (manual exploitation, 0-day research) |
| **Development cost** | +10-20% | +30-50% |
| **Examples** | Infotainment, door locks | Powertrain, ADAS, braking |

**Key difference:** CAL 4 assumes sophisticated attacker (nation-state capability), CAL 2 assumes opportunistic attacker.

**Q4: How does ISO 21434 address supply chain security?**

**A4:**

**Clause 7: Distributed Cybersecurity Activities**

**Requirements:**
1. **Supplier assessment:** Evaluate supplier's cybersecurity maturity (questionnaire, audit)
2. **Contractual obligations:** Specify security requirements in purchase orders
3. **Component verification:** Validate received components (signature checks, SBOM)
4. **Vulnerability disclosure:** Establish communication channel for security issues
5. **Incident notification:** Supplier must report breaches within 24 hours

**Example: Tier 1 Supplier Providing Gateway ECU**

**OEM Requirements:**
- Supplier must have CSMS (ISO 21434 compliant)
- Gateway ECU must achieve CAL 3 verification
- Source code escrow (if supplier goes out of business)
- Vulnerability patching SLA (critical: 48h, high: 30d)
- Annual security audit by OEM or third-party

**Acceptance criteria:**
- Penetration test report (no critical findings)
- SBOM (Software Bill of Materials) provided
- Cryptographic keys generated in HSM (OEM-controlled)

**Q5: What is the relationship between ISO 21434 and UN R155/R156?**

**A5:**

**UN R155 (Cybersecurity Management System):**
- **Type approval regulation** (mandatory for vehicle sales in EU/Japan/Korea)
- Requires OEM to demonstrate **CSMS** (aligns with ISO 21434 Clause 5)
- Audited by national authorities (KBA in Germany, JARI in Japan)

**UN R156 (Software Update Management System):**
- **Type approval regulation** for OTA updates
- Requires secure update process (aligns with ISO 21434 Clause 12)
- Verify, track, and log all software updates

**Relationship:**

```
ISO 21434 (Standard)
├─ Provides detailed technical guidance
└─ Voluntary (but becomes de facto mandatory via UN regulations)

UN R155/R156 (Regulations)
├─ Legal requirements for type approval
├─ References ISO 21434 as acceptable implementation
└─ Mandatory (cannot sell vehicles without compliance)
```

**Compliance path:**
1. Implement ISO 21434 CSMS + product development process
2. Demonstrate compliance in UN R155 audit
3. Receive type approval certificate
4. Sell vehicles in regulated markets

**Penalty for non-compliance:** Type approval denial = cannot sell vehicles.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~900
