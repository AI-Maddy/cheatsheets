🎯 **THREAT MODELING FOR EMBEDDED SYSTEMS**
═══════════════════════════════════════════════════════════════════════

**Systematic Security Risk Analysis: STRIDE, PASTA, Attack Trees**  
**Purpose:** Identify threats early 🔍 | Prioritize defenses 🛡️ | Design secure systems 🏗️  
**Standards:** DO-356A, ISO 21434, IEC 62443-3-2, NIST SP 800-154

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Threat modeling** = systematic process to identify, categorize, and mitigate security threats **before implementation**.

**"Fix vulnerabilities in design, not in production."**

**Common methodologies:**
- **STRIDE:** Threat categorization (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation)
- **PASTA:** 7-stage attack-centric approach
- **Attack Trees:** Visual goal-oriented threat analysis

**When:** Architecture phase (before coding), then iterate throughout development.

════════════════════════════════════════════════════════════════════════════

🎯 **STRIDE THREAT MODELING**
─────────────────────────────────────────────────────────────────────────

**STRIDE Acronym (Microsoft Security Development Lifecycle):**

| Threat Category | Description | Example (Automotive ECU) | Violated Property |
|:----------------|:------------|:------------------------|:------------------|
| **S** - Spoofing | Pretending to be someone else | Forged CAN message from fake ECU | **Authentication** |
| **T** - Tampering | Modifying data or code | Modified firmware via JTAG | **Integrity** |
| **R** - Repudiation | Denying an action | No audit log of software update | **Non-repudiation** |
| **I** - Information Disclosure | Exposing confidential data | Unencrypted V2X private key in flash | **Confidentiality** |
| **D** - Denial of Service | Making system unavailable | CAN bus flooding (prevent airbag deployment) | **Availability** |
| **E** - Elevation of Privilege | Gaining unauthorized access | Escape from sandbox to kernel mode | **Authorization** |

**STRIDE Analysis Process:**

.. code-block:: text

   Step 1: Create Data Flow Diagram (DFD)
   ┌─────────────┐
   │  User/Actor │  (External entity)
   └──────┬──────┘
          │ Data flow
          ▼
   ┌─────────────┐
   │  Process    │  (Code execution)
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │ Data Store  │  (Database, flash, RAM)
   └─────────────┘
   
   Step 2: Identify trust boundaries
   Step 3: Apply STRIDE to each element
   Step 4: Document threats
   Step 5: Prioritize (DREAD or CVSS)
   Step 6: Mitigate

**Example: Automotive Gateway ECU**

.. code-block:: python

   # STRIDE analysis for automotive gateway
   class ThreatModel:
       def __init__(self, component_name):
           self.component = component_name
           self.threats = []
       
       def add_threat(self, category, description, impact, likelihood, mitigation):
           self.threats.append({
               'category': category,
               'description': description,
               'impact': impact,          # 1-5 (5 = critical)
               'likelihood': likelihood,  # 1-5 (5 = very likely)
               'risk': impact * likelihood,
               'mitigation': mitigation
           })
   
   # Gateway ECU threat model
   gateway = ThreatModel("Automotive Gateway ECU")
   
   # Spoofing threats
   gateway.add_threat(
       category='Spoofing',
       description='Attacker injects forged CAN messages impersonating ABS ECU',
       impact=5,  # Safety-critical
       likelihood=3,  # Requires CAN access
       mitigation='CAN authentication (AUTOSAR SecOC), message sequence numbers'
   )
   
   # Tampering threats
   gateway.add_threat(
       category='Tampering',
       description='Flash memory modified via JTAG debug port',
       impact=5,
       likelihood=2,  # Requires physical access
       mitigation='Disable JTAG in production, secure boot, flash readout protection'
   )
   
   # Information Disclosure threats
   gateway.add_threat(
       category='Info Disclosure',
       description='Private keys extracted via UART debug output',
       impact=4,
       likelihood=2,
       mitigation='Disable debug UART, store keys in HSM/secure element'
   )
   
   # Denial of Service threats
   gateway.add_threat(
       category='DoS',
       description='CAN bus flooding prevents critical messages (e.g., brake signals)',
       impact=5,
       likelihood=4,  # Easy to execute
       mitigation='CAN rate limiting, priority queues, watchdog timers'
   )
   
   # Elevation of Privilege threats
   gateway.add_threat(
       category='Elevation',
       description='Buffer overflow in CAN parser escalates to code execution',
       impact=5,
       likelihood=3,
       mitigation='Memory protection (MPU), bounds checking, MISRA C compliance'
   )
   
   # Generate report
   def print_report(self):
       print(f"Threat Model: {self.component}")
       print("=" * 80)
       
       # Sort by risk (impact × likelihood)
       sorted_threats = sorted(self.threats, key=lambda t: t['risk'], reverse=True)
       
       for i, threat in enumerate(sorted_threats, 1):
           print(f"\nThreat #{i} [{threat['category']}]")
           print(f"  Description: {threat['description']}")
           print(f"  Impact: {threat['impact']}/5 | Likelihood: {threat['likelihood']}/5")
           print(f"  Risk Score: {threat['risk']}/25")
           print(f"  Mitigation: {threat['mitigation']}")
   
   gateway.print_report()

**Output:**
```
Threat Model: Automotive Gateway ECU
================================================================================

Threat #1 [DoS]
  Description: CAN bus flooding prevents critical messages (e.g., brake signals)
  Impact: 5/5 | Likelihood: 4/5
  Risk Score: 20/25
  Mitigation: CAN rate limiting, priority queues, watchdog timers

Threat #2 [Spoofing]
  Description: Attacker injects forged CAN messages impersonating ABS ECU
  Impact: 5/5 | Likelihood: 3/5
  Risk Score: 15/25
  Mitigation: CAN authentication (AUTOSAR SecOC), message sequence numbers

...
```

════════════════════════════════════════════════════════════════════════════

🌳 **ATTACK TREES**
─────────────────────────────────────────────────────────────────────────

**Attack Tree Concept:**
- **Root:** Attacker's goal (e.g., "Execute arbitrary code on ECU")
- **Branches:** Alternative attack paths
- **Leaves:** Specific vulnerabilities or actions

**Example: Remote Code Execution on Avionics FMS**

.. code-block:: text

   Goal: Execute Malicious Code on FMS
   │
   ├─ AND ─ Exploit Network Interface
   │   ├─ OR ─ ACARS Message Injection
   │   │   ├─ Buffer overflow in message parser (Difficulty: High)
   │   │   └─ SQL injection in database query (Difficulty: Medium)
   │   │
   │   └─ OR ─ AFDX Packet Injection
   │       ├─ Compromise adjacent LRU (Difficulty: High)
   │       └─ Physical access to AFDX switch (Difficulty: Very High)
   │
   ├─ AND ─ Exploit Software Loading
   │   ├─ Malicious USB drive (Difficulty: Medium)
   │   ├─ Bypass signature verification (Difficulty: Very High)
   │   └─ Social engineering (maintenance) (Difficulty: Low)
   │
   └─ AND ─ Exploit Physical Access
       ├─ JTAG debug port (Difficulty: High - requires disassembly)
       └─ Replace ROM chip (Difficulty: Very High - tamper detection)

**Attack Tree Analysis:**

.. code-block:: python

   class AttackTree:
       def __init__(self, goal):
           self.goal = goal
           self.paths = []
       
       def add_path(self, steps, difficulty, cost_usd, time_hours):
           self.paths.append({
               'steps': steps,
               'difficulty': difficulty,  # 1-5
               'cost': cost_usd,
               'time': time_hours,
               'feasibility': self.calculate_feasibility(difficulty, cost_usd)
           })
       
       def calculate_feasibility(self, difficulty, cost):
           # Lower difficulty + lower cost = higher feasibility
           return (6 - difficulty) * (1000000 / max(cost, 1))
       
       def prioritize_mitigations(self):
           # Focus on most feasible attacks
           sorted_paths = sorted(self.paths, key=lambda p: p['feasibility'], reverse=True)
           return sorted_paths
   
   # Example: FMS attack analysis
   fms_attack = AttackTree("Execute Code on FMS")
   
   fms_attack.add_path(
       steps=['Social engineering', 'Malicious USB', 'Bypass AV'],
       difficulty=2,  # Low-Medium
       cost_usd=5000,
       time_hours=40
   )
   
   fms_attack.add_path(
       steps=['ACARS buffer overflow', 'Exploit parser', 'Payload execution'],
       difficulty=4,  # High
       cost_usd=50000,  # Requires vulnerability research
       time_hours=500
   )
   
   fms_attack.add_path(
       steps=['Physical access', 'JTAG connection', 'Flash dump', 'Modify firmware'],
       difficulty=4,
       cost_usd=10000,
       time_hours=80
   )
   
   # Prioritize
   for i, path in enumerate(fms_attack.prioritize_mitigations(), 1):
       print(f"Attack Path #{i} (Feasibility: {path['feasibility']:.0f})")
       print(f"  Steps: {' → '.join(path['steps'])}")
       print(f"  Difficulty: {path['difficulty']}/5")
       print(f"  Estimated Cost: ${path['cost']:,}")
       print(f"  Time: {path['time']} hours\n")

**Result: Prioritize defenses against highest-feasibility attacks**

════════════════════════════════════════════════════════════════════════════

🍝 **PASTA THREAT MODELING**
─────────────────────────────────────────────────────────────────────────

**PASTA (Process for Attack Simulation and Threat Analysis):**

**Stage 1: Define Objectives**
- Business goals (e.g., "Protect customer safety data")
- Security requirements (e.g., "Comply with ISO 21434")
- Compliance mandates

**Stage 2: Define Technical Scope**
- Components (ECUs, sensors, networks)
- Interfaces (CAN, Ethernet, wireless)
- Trust boundaries

**Stage 3: Application Decomposition**
- Data flow diagrams
- Component interactions
- Assets (keys, PII, algorithms)

**Stage 4: Threat Analysis**
- STRIDE for each component
- Attack libraries (MITRE ATT&CK, CAPEC)

**Stage 5: Vulnerability & Weakness Analysis**
- Known CVEs
- Design weaknesses (no authentication, weak crypto)

**Stage 6: Attack Modeling**
- Attack trees
- Proof-of-concept exploits

**Stage 7: Risk & Impact Analysis**
- CVSS scoring
- Safety impact (ASIL, DAL)
- Prioritized remediation plan

**PASTA Example: Medical Infusion Pump**

.. code-block:: python

   class PASTAModel:
       def __init__(self, system_name):
           self.system = system_name
           self.stages = {
               'objectives': [],
               'scope': [],
               'decomposition': [],
               'threats': [],
               'vulnerabilities': [],
               'attacks': [],
               'risks': []
           }
       
       def stage1_objectives(self, objectives):
           self.stages['objectives'] = objectives
       
       def stage4_threats(self, component, threats):
           for threat in threats:
               self.stages['threats'].append({
                   'component': component,
                   'threat': threat
               })
       
       def stage7_risk_analysis(self):
           """Calculate risk scores (CVSS + safety impact)"""
           risks = []
           
           for threat in self.stages['threats']:
               # CVSS base score
               cvss = threat.get('cvss', 5.0)
               
               # Safety impact (medical device: 1-5)
               safety_impact = threat.get('safety_impact', 3)
               
               # Combined risk
               risk_score = cvss * safety_impact
               
               risks.append({
                   'component': threat['component'],
                   'threat': threat['threat'],
                   'cvss': cvss,
                   'safety_impact': safety_impact,
                   'risk_score': risk_score
               })
           
           self.stages['risks'] = sorted(risks, key=lambda r: r['risk_score'], reverse=True)
           return self.stages['risks']
   
   # Infusion pump example
   pump = PASTAModel("Medical Infusion Pump")
   
   # Stage 1
   pump.stage1_objectives([
       'Prevent unauthorized dosage changes',
       'Protect patient health data (HIPAA)',
       'Ensure availability (99.9% uptime)',
       'FDA premarket cybersecurity compliance'
   ])
   
   # Stage 4 (threats)
   pump.stage4_threats(
       component='Wireless Interface (Wi-Fi)',
       threats=[
           {'threat': 'Unauthorized dosage modification', 'cvss': 8.5, 'safety_impact': 5},
           {'threat': 'PHI data exfiltration', 'cvss': 6.0, 'safety_impact': 2},
           {'threat': 'Ransomware (DoS)', 'cvss': 7.0, 'safety_impact': 4}
       ]
   )
   
   pump.stage4_threats(
       component='Drug Library',
       threats=[
           {'threat': 'Drug library tampering', 'cvss': 7.5, 'safety_impact': 5},
           {'threat': 'Outdated drug protocols', 'cvss': 5.0, 'safety_impact': 3}
       ]
   )
   
   # Stage 7: Risk analysis
   for i, risk in enumerate(pump.stage7_risk_analysis(), 1):
       print(f"Risk #{i}")
       print(f"  Component: {risk['component']}")
       print(f"  Threat: {risk['threat']}")
       print(f"  CVSS: {risk['cvss']}")
       print(f"  Safety Impact: {risk['safety_impact']}/5")
       print(f"  Risk Score: {risk['risk_score']:.1f}\n")

**Output prioritizes mitigations:**
```
Risk #1
  Component: Wireless Interface (Wi-Fi)
  Threat: Unauthorized dosage modification
  CVSS: 8.5
  Safety Impact: 5/5
  Risk Score: 42.5
  ↳ Mitigation: WPA3-Enterprise, mTLS, dosage change confirmation

Risk #2
  Component: Drug Library
  Threat: Drug library tampering
  CVSS: 7.5
  Safety Impact: 5/5
  Risk Score: 37.5
  ↳ Mitigation: Digital signatures, read-only storage, integrity checks
```

════════════════════════════════════════════════════════════════════════════

🛠️ **PRACTICAL THREAT MODELING WORKFLOW**
─────────────────────────────────────────────────────────────────────────

**When to Threat Model:**

| Development Phase | Threat Modeling Activity | Output |
|:------------------|:------------------------|:-------|
| **Requirements** | High-level security goals | Security requirements document |
| **Architecture** | STRIDE on components | Threat list, security architecture |
| **Design** | Attack trees, data flows | Detailed threat scenarios |
| **Implementation** | Code review for threats | Secure coding checklist |
| **Testing** | Penetration testing | Validated mitigations |
| **Maintenance** | Continuous threat monitoring | Vulnerability patches |

**Tools:**

| Tool | Type | Use Case |
|:-----|:-----|:---------|
| **Microsoft Threat Modeling Tool** | STRIDE | Windows applications, web services |
| **OWASP Threat Dragon** | STRIDE | Open-source, web/desktop apps |
| **IriusRisk** | Automated | Integrated with SDLC, compliance |
| **Cairis** | IRIS framework | Academia, complex systems |

**Threat Modeling Checklist (Automotive ECU):**

.. code-block:: text

   ✅ Architecture Review
   □ Identified all interfaces (CAN, Ethernet, OBD-II, USB)
   □ Marked trust boundaries (internal vs. external networks)
   □ Listed assets (keys, calibration data, PII)
   
   ✅ STRIDE Analysis
   □ Spoofing: CAN message authentication required?
   □ Tampering: Secure boot implemented?
   □ Repudiation: Audit logging for diagnostic access?
   □ Info Disclosure: Keys stored in secure element?
   □ DoS: Rate limiting on external interfaces?
   □ Elevation: Memory protection (MPU) enabled?
   
   ✅ Attack Scenarios
   □ Remote attack via telematics
   □ Physical attack via OBD-II port
   □ Supply chain (malicious component)
   □ Insider threat (service technician)
   
   ✅ Mitigations Documented
   □ Each threat has ≥1 mitigation
   □ Mitigations traceable to requirements
   □ Residual risk accepted by stakeholders

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Apply STRIDE to an automotive OBD-II diagnostic port.**

**A1:**

**Component:** OBD-II Port (Physical connector, CAN access)

| STRIDE | Threat | Mitigation |
|:-------|:-------|:-----------|
| **Spoofing** | Aftermarket scan tool impersonates OEM tool | Authenticate tools via challenge-response |
| **Tampering** | Reflashing ECU firmware via OBD-II | Require signed firmware, secure boot |
| **Repudiation** | No log of who accessed diagnostic functions | Audit logging with timestamp + tool ID |
| **Info Disclosure** | Extract VIN, mileage, driving habits | Encrypt diagnostic data, access control |
| **DoS** | Flood CAN bus via OBD-II (disable airbags) | Rate limiting, separate diagnostic CAN |
| **Elevation** | Exploit diagnostic command to gain kernel access | Memory protection, input validation |

**Highest Risk:** **DoS** (safety impact) and **Tampering** (firmware modification)

**Q2: What is the difference between STRIDE and attack trees?**

**A2:**

| Aspect | STRIDE | Attack Trees |
|:-------|:-------|:-------------|
| **Approach** | Defensive (what can go wrong?) | Offensive (how to achieve goal?) |
| **Structure** | Taxonomy (6 categories) | Hierarchical (goal → sub-goals → actions) |
| **Output** | List of threats per component | Visual attack paths |
| **Best for** | Brainstorming, completeness | Prioritization, feasibility analysis |
| **When to use** | Architecture phase (broad coverage) | Design phase (specific attacks) |

**Complementary:** Use STRIDE to identify threats, then attack trees to model exploitation.

**Q3: How does PASTA differ from STRIDE?**

**A3:**

**STRIDE:**
- Threat categorization framework
- Applied to each component
- Tactical (find threats)

**PASTA:**
- End-to-end threat modeling process (7 stages)
- Business objectives → risk analysis
- Strategic (align security with business goals)

**PASTA includes STRIDE:** Stage 4 (Threat Analysis) uses STRIDE, but PASTA also covers objectives, decomposition, vulnerabilities, attack modeling, and risk scoring.

**Use PASTA when:**
- Need executive buy-in (business context)
- Compliance-driven (ISO 21434, FDA)
- Large project (aerospace, automotive platforms)

**Q4: What is a trust boundary and why is it important?**

**A4:**

**Trust Boundary:** Line separating components with different trust levels.

**Examples:**

```
Automotive Gateway ECU:

[External Network - Untrusted]
    ↓ Trust Boundary (Firewall)
[IFE / Infotainment - Low Trust]
    ↓ Trust Boundary (Data Diode)
[Avionics / Powertrain - High Trust]
```

**Importance:**
- **Attack surface:** External interfaces are primary entry points
- **Defense placement:** Deploy strongest defenses at boundaries (authentication, encryption, firewall)
- **Threat prioritization:** Threats crossing boundaries are highest priority

**DO-326A SAL determination:** Connectivity across trust boundaries increases SAL level.

**Q5: How to integrate threat modeling with agile development?**

**A5:**

**Challenge:** Agile iterates quickly, traditional threat modeling is heavyweight.

**Solution: Incremental Threat Modeling**

**Sprint 0 (Architecture):**
- High-level STRIDE on major components
- Document critical threats
- Define security requirements

**Each Sprint:**
- 30-min threat modeling session for new features
- Update threat model as design evolves
- Link threats to user stories (e.g., "As an attacker, I can...")

**Continuous:**
- Automated threat detection (SAST/DAST tools)
- Threat library (reusable patterns)
- Quarterly threat model review

**Tools:**
- OWASP Threat Dragon (lightweight, web-based)
- Threat modeling as code (YAML definitions in repo)

**Key:** Treat threat model as living document, not one-time activity.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
