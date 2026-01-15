✈️ **SECURITY ASSURANCE LEVELS (SAL) — Aviation Security Classification**
═══════════════════════════════════════════════════════════════════════

**SAL 0-3 Determination and Application in Airborne Systems**  
**Purpose:** Security risk classification 🎚️ | Assurance rigor 📊 | Compliance mapping ✅  
**Standard:** DO-326A / ED-202A | Similar to DAL (Design Assurance Level) for safety

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Security Assurance Level (SAL)** is the aviation equivalent of security severity rating. It determines **how much security rigor** to apply during design, verification, and certification. SAL ranges from **0 (no security requirements) to 3 (maximum rigor, similar to DAL A for safety)**.

**Key Equation:** `Threat Impact + Attack Feasibility → SAL → Required Security Process Rigor`

**Real-World Example:** Flight control computer = **SAL 3** (catastrophic if compromised), passenger entertainment = **SAL 0** (if properly isolated).

════════════════════════════════════════════════════════════════════════════

🎚️ **SAL LEVELS DEFINED**
─────────────────────────────────────────────────────────────────────────

**SAL 0: No Security Requirements**

| Aspect | Description |
|:-------|:------------|
| **Impact if Compromised** | No safety or security consequences |
| **Attack Surface** | Completely isolated OR externally facing but non-critical |
| **Examples** | Isolated IFE, passenger USB charging ports |
| **Security Process** | None required (but good practice: basic hardening) |
| **Verification** | Not required by DO-326A |
| **Analogy to Safety** | Similar to DAL E (no safety impact) |

**Example System: Isolated In-Flight Entertainment**
- Passengers can watch movies, play games
- **No connection** to avionics network
- Physical air gap enforced
- Compromise = annoyed passengers, not safety issue
- **SAL 0** appropriate

**SAL 1: Basic Security**

| Aspect | Description |
|:-------|:------------|
| **Impact if Compromised** | Minor: Annoyance, limited operational impact |
| **Attack Surface** | Limited connectivity, low-value target |
| **Examples** | Flight information display, cabin announcement system |
| **Security Process** | Basic threat modeling, security review |
| **Verification** | Security testing, vulnerability assessment |
| **Analogy to Safety** | Similar to DAL D (minor safety effect) |

**Example System: Passenger Information Display**
- Shows altitude, speed, route map to passengers
- Receives data from avionics (one-way)
- Compromise = incorrect display (crew has real data)
- Operational nuisance but not safety issue
- **SAL 1** appropriate

**SAL 2: Moderate Security**

| Aspect | Description |
|:-------|:------------|
| **Impact if Compromised** | Major: Significant operational degradation |
| **Attack Surface** | Moderate connectivity, valuable target |
| **Examples** | Weather radar, TCAS, ACARS datalink |
| **Security Process** | Detailed threat modeling, security architecture, secure coding |
| **Verification** | Penetration testing, security code review, analysis |
| **Analogy to Safety** | Similar to DAL C (major safety effect) |

**Example System: Traffic Collision Avoidance System (TCAS)**
- Provides collision avoidance advisories (RA/TA)
- Wireless interface (Mode S transponder)
- Compromise = false alerts, nuisance RAs
- Pilots can override, but increased workload
- **SAL 2** appropriate

**SAL 3: High Security (Rigorous)**

| Aspect | Description |
|:-------|:------------|
| **Impact if Compromised** | Hazardous or Catastrophic: Flight safety directly affected |
| **Attack Surface** | Critical system with any connectivity |
| **Examples** | Flight control, engine control, FMS, braking |
| **Security Process** | Comprehensive threat modeling, formal security architecture, FIPS crypto, independent assessment |
| **Verification** | Extensive penetration testing, formal methods, fuzzing, red team assessment |
| **Analogy to Safety** | Similar to DAL A/B (catastrophic/hazardous) |

**Example System: Flight Management System (FMS)**
- Calculates flight path, manages autopilot
- Multiple interfaces: ACARS, USB, ARINC 429/664
- Compromise = incorrect navigation → CFIT, wrong runway
- Direct flight safety impact
- **SAL 3** required

════════════════════════════════════════════════════════════════════════════

📊 **SAL DETERMINATION PROCESS**
─────────────────────────────────────────────────────────────────────────

**Step-by-Step SAL Assignment:**

.. code-block:: text

   1. IDENTIFY SYSTEM/FUNCTION
      │ What are we analyzing? (e.g., FMS, IFE, TCAS)
      ▼
   2. ANALYZE CONNECTIVITY
      │ What interfaces exist? (wireless, wired, USB, datalink)
      │ Can attacker access remotely? Physically? Via adjacent system?
      ▼
   3. THREAT MODELING
      │ What could attacker do if system compromised?
      │ - Modify data (tampering)
      │ - Deny service (availability)
      │ - Impersonate (spoofing)
      │ - Escalate privileges
      ▼
   4. IMPACT ASSESSMENT (use ARP4754A methods)
      │ What is SAFETY impact? (align with FHA, PSSA, SSA)
      │ - Catastrophic: Multiple fatalities likely
      │ - Hazardous: Serious injury likely, reduced safety margins
      │ - Major: Passenger discomfort, crew high workload
      │ - Minor: Slight inconvenience
      │ - No Effect: No operational or safety impact
      ▼
   5. MAP IMPACT → SAL
      │ Catastrophic/Hazardous → SAL 3
      │ Major → SAL 2
      │ Minor → SAL 1
      │ No Effect (and isolated) → SAL 0
      ▼
   6. DOCUMENT RATIONALE
      │ Record SAL assignment in security plan
      │ Include threat model, impact analysis, assumptions
      ▼
   7. APPLY DO-326A PROCESS PER SAL
      (Security objectives, requirements, implementation, verification)

**SAL Assignment Example: Airborne Internet Gateway**

.. code-block:: python

   # SAL determination for airborne internet router
   
   class SystemSecurityAssessment:
       def __init__(self, system_name):
           self.system = system_name
           self.connectivity = []
           self.threats = []
           self.impact = None
           self.sal = None
       
       def analyze_connectivity(self):
           """Identify all attack surfaces"""
           return [
               {
                   'interface': 'Ku-band Satellite',
                   'direction': 'Bidirectional',
                   'exposure': 'Internet-facing',
                   'attacker_access': 'Remote (worldwide)'
               },
               {
                   'interface': 'Passenger Wi-Fi',
                   'direction': 'Bidirectional',
                   'exposure': 'Passenger devices',
                   'attacker_access': 'Physical (on aircraft)'
               },
               {
                   'interface': 'Avionics Ethernet (AFDX)',
                   'direction': 'Inbound only (one-way data diode)',
                   'exposure': 'Receives flight data for display',
                   'attacker_access': 'Via pivot from internet'
               }
           ]
       
       def identify_threats(self):
           """STRIDE analysis"""
           return [
               {
                   'type': 'Spoofing',
                   'description': 'Attacker impersonates aircraft to ground system',
                   'impact': 'Minor - billing fraud, not flight safety'
               },
               {
                   'type': 'Tampering',
                   'description': 'Attacker modifies flight data sent to passengers',
                   'impact': 'Minor - incorrect moving map display'
               },
               {
                   'type': 'Elevation of Privilege',
                   'description': 'Attacker pivots from internet gateway to avionics',
                   'impact': 'CATASTROPHIC - if data diode bypassed or failed'
               },
               {
                   'type': 'Denial of Service',
                   'description': 'Attacker floods gateway, denies internet',
                   'impact': 'Minor - passengers lose connectivity'
               }
           ]
       
       def determine_sal(self):
           """
           Key decision: Is the data diode foolproof?
           
           Scenario A: Data diode is hardware-enforced, formally verified
                       → SAL 1 (gateway itself is low-impact)
           
           Scenario B: Data diode is software-based, could be bypassed
                       → SAL 3 (gateway is potential pivot point to avionics)
           """
           
           if self.has_hardware_data_diode() and self.diode_formally_verified():
               self.sal = 1
               self.rationale = "Gateway isolated from avionics by hardware data diode"
           else:
               self.sal = 3
               self.rationale = "Gateway is potential attack vector to SAL 3 avionics"
           
           return self.sal
   
   # Assessment
   assessment = SystemSecurityAssessment("Airborne Internet Gateway")
   assessment.connectivity = assessment.analyze_connectivity()
   assessment.threats = assessment.identify_threats()
   assessment.sal = assessment.determine_sal()
   
   print(f"Assigned SAL: {assessment.sal}")
   print(f"Rationale: {assessment.rationale}")

════════════════════════════════════════════════════════════════════════════

🔗 **SAL vs DAL RELATIONSHIP**
─────────────────────────────────────────────────────────────────────────

**Key Differences:**

| Aspect | **DAL (Design Assurance Level)** | **SAL (Security Assurance Level)** |
|:-------|:----------------------------------|:-----------------------------------|
| **Standard** | DO-178C (software), DO-254 (hardware) | DO-326A (security) |
| **Focus** | Unintentional failures (bugs, HW faults) | Intentional attacks (cyber threats) |
| **Threat Model** | Random failures, single faults | Intelligent adversary, attack chains |
| **Determination** | Probability × Severity | Impact of successful attack |
| **Levels** | A (catastrophic) → E (no effect) | 3 (catastrophic) → 0 (no effect) |

**Combined Assessment:**

Many systems need BOTH safety and security assurance:

.. code-block:: text

   Flight Control Computer:
   ├─ DAL A (catastrophic failure → loss of aircraft)
   ├─ SAL 3 (catastrophic compromise → loss of aircraft)
   └─ Process: DO-178C + DO-254 + DO-326A integrated
   
   Weather Radar:
   ├─ DAL C (major failure → crew high workload, CFIT risk in IMC)
   ├─ SAL 2 (major compromise → false weather data)
   └─ Process: DO-178C + DO-326A
   
   Passenger Entertainment (isolated):
   ├─ DAL E (no safety effect)
   ├─ SAL 0 (no security effect if isolated)
   └─ Process: Minimal DO-178C, no DO-326A required

**SAL/DAL Matrix for Typical Systems:**

| System | DAL | SAL | Justification |
|:-------|:----|:----|:--------------|
| Flight Control | A | 3 | Catastrophic for both safety and security |
| Engine FADEC | A | 3 | Loss of engine control = catastrophic |
| FMS | A | 3 | Navigation errors = hazardous |
| Autopilot | A | 3 | Control authority = high impact |
| TCAS | B | 2 | Collision avoidance, but pilot can override |
| Weather Radar | C | 2 | Situational awareness, workload |
| ACARS | C | 2 | Communication, operational data |
| IFE (w/ gateway) | E | 2 | If gateway to avionics data |
| IFE (isolated) | E | 0 | No connectivity to safety systems |
| Cabin Lights | E | 0 | No safety or security impact |

════════════════════════════════════════════════════════════════════════════

🛠️ **SECURITY PROCESS BY SAL**
─────────────────────────────────────────────────────────────────────────

**SAL 0 Process (None Required):**
- No DO-326A obligations
- Optional: Basic hardening (good practice)

**SAL 1 Process (Basic):**
- ✓ Security plan (basic)
- ✓ Threat identification (simple STRIDE)
- ✓ Security requirements (10-20 requirements typical)
- ✓ Security review (architecture review)
- ✓ Security testing (functional security tests)
- ✗ No independent assessment
- ✗ No formal methods

**SAL 2 Process (Moderate):**
- ✓ Security plan (detailed)
- ✓ Threat modeling (STRIDE + attack trees)
- ✓ Security requirements (50-100 requirements typical)
- ✓ Security architecture (defined trust boundaries)
- ✓ Secure coding standards (CERT C, MISRA C)
- ✓ Cryptography (FIPS 140-2 Level 1+)
- ✓ Penetration testing (external team)
- ✓ Security code review
- ⚠️ Independent assessment (recommended)
- ✗ Formal verification (optional)

**SAL 3 Process (Rigorous):**
- ✓ Security plan (comprehensive, integrated with safety)
- ✓ Threat modeling (STRIDE, PASTA, attack trees, adversary TTPs)
- ✓ Security requirements (100-300 requirements typical)
- ✓ Security architecture (formal model, trust boundaries, data flow diagrams)
- ✓ Secure coding standards (CERT C, MISRA C, security extensions)
- ✓ Cryptography (FIPS 140-2 Level 2+, hardware-backed)
- ✓ Penetration testing (multiple rounds, red team)
- ✓ Security code review (manual + automated)
- ✓ Fuzzing (AFL, libFuzzer on all interfaces)
- ✓ Independent security assessment (mandatory)
- ✓ Formal methods (critical protocols, crypto implementation)
- ✓ Security regression testing
- ✓ Supply chain security (SBOM, component verification)

**Effort Comparison:**

.. code-block:: text

   Typical Security Effort by SAL (as % of total development):
   
   SAL 0: 0-2% (optional basic hardening)
   SAL 1: 5-10% (basic security activities)
   SAL 2: 15-25% (moderate security rigor)
   SAL 3: 30-40% (comprehensive security program)
   
   Note: SAL 3 with DAL A = 50-60% total assurance effort
   (Safety + Security combined)

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Can a system have different DAL and SAL levels? Provide an example.**

**A1:**
Yes, absolutely. DAL and SAL assess different risks:

**Example: Weather Radar**
- **DAL C** (Major safety impact)
  - Rationale: Failure in IMC could lead to CFIT or turbulence encounter
  - Major safety effect, high crew workload
- **SAL 2** (Major security impact)
  - Rationale: False weather display could mislead crew
  - But pilot cross-checks with other sources (ATC, PIREPS)
  - Not catastrophic because crew has situational awareness

**Why different?**
- Unintentional failure (DAL C) = major
- Intentional attack (SAL 2) = also major, but pilot can detect anomalies
- Not SAL 3 because not direct control authority

**Q2: How do you determine SAL for a system with multiple interfaces?**

**A2:**
Use **highest-impact** pathway:

**Example: Electronic Flight Bag (EFB)**
- Interface 1: Wi-Fi to internet → Low impact (EFB just displays charts)
- Interface 2: USB to avionics → **HIGH impact** (could load malicious app)
- Interface 3: ARINC 429 from FMS → Medium impact (receives data, doesn't send)

**SAL determination:**
- Worst-case: Attacker uses USB to load malware → pivots to avionics → **SAL 3**
- Mitigation: If USB disabled in flight mode AND app signing enforced → **SAL 1**

**Rule:** Assign SAL based on **highest-risk attack path**, considering mitigations.

**Q3: What is the security verification difference between SAL 2 and SAL 3?**

**A3:**

| Activity | SAL 2 | SAL 3 |
|:---------|:------|:------|
| **Penetration Testing** | Basic (1 round, known techniques) | Advanced (multiple rounds, zero-day research) |
| **Independent Assessment** | Recommended (not mandatory) | **Mandatory** (third-party security firm) |
| **Formal Methods** | Optional | **Required** for critical components |
| **Fuzzing** | Recommended | **Extensive** (AFL, coverage-guided, 48+ hours per interface) |
| **Cryptography** | FIPS 140-2 Level 1 | **FIPS 140-2 Level 2+** (hardware-backed) |
| **Red Team** | Not required | **Recommended** (simulated nation-state attack) |

**Key difference:** SAL 3 assumes **sophisticated attacker** (nation-state capability), SAL 2 assumes skilled individual.

**Q4: Can a SAL 0 system become SAL 3 due to architecture changes?**

**A4:**
Yes! Common scenario:

**Initial Design:**
- In-Flight Entertainment (IFE)
- Completely isolated from avionics (air gap)
- **SAL 0** (no security requirements)

**Modified Design:**
- IFE now displays moving map (needs aircraft position)
- Connection to avionics network added
- **NEW SAL:** If connection is read-only (hardware data diode) → **SAL 1**
- **NEW SAL:** If connection is bidirectional → **SAL 3** (IFE becomes attack vector)

**Lesson:** Architecture changes can dramatically affect SAL. Re-assess security when adding connectivity!

**Q5: How does SAL 3 align with DAL A certification evidence?**

**A5:**
**Integrated approach for flight-critical systems:**

**DO-178C (DAL A) Evidence:**
- Software Requirements (SRS)
- Software Design (SDD)
- Source Code
- Test cases + coverage (MC/DC)
- Verification results

**DO-326A (SAL 3) Evidence (ADDED):**
- Security Requirements (integrated with SRS)
- Security Architecture (trust boundaries in SDD)
- Threat Model
- Penetration Test Results
- Security Code Review Results
- Cryptographic Module Validation (FIPS 140-2)
- Independent Security Assessment Report

**Combined Review:**
- Certification authority reviews BOTH safety and security evidence
- Security vulnerabilities that affect safety are major findings
- Example: Buffer overflow = DAL A verification failure (safety) + SAL 3 finding (security)

**Result:** SAL 3 + DAL A systems undergo most rigorous aerospace certification process.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~650
