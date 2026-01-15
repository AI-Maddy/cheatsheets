✈️ **DO-355 / ED-204 — CONTINUING AIRWORTHINESS SECURITY**
═══════════════════════════════════════════════════════════════════════

**Information Security Guidance for Continuing Airworthiness**  
**Purpose:** Post-certification security 🔄 | Vulnerability management 🛡️ | Fleet monitoring 📊  
**Authority:** FAA (DO-355) | EASA (ED-204) | RTCA/EUROCAE | Operational phase security

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**DO-355** addresses security **AFTER** aircraft certification — the operational lifecycle. While DO-326A/DO-356A focus on design-time security, DO-355 covers: **vulnerability monitoring, patch management, incident response, and threat intelligence** for in-service aircraft.

**Key Insight:** Aircraft fly for 20-30 years. New vulnerabilities discovered continuously. DO-355 ensures aircraft security evolves with threat landscape.

**Real-World Example:** When WannaCry ransomware emerged (2017), DO-355 guidance helped airlines assess aircraft exposure, deploy patches, and monitor for indicators of compromise.

**Publication:** DO-355 (2016), ED-204 (EASA equivalent, 2016)

════════════════════════════════════════════════════════════════════════════

🎯 **SCOPE & OBJECTIVES**
─────────────────────────────────────────────────────────────────────────

**Continuing Airworthiness Security (CAS):**

The ongoing process of ensuring aircraft security throughout operational life:

```
┌─────────────────────────────────────────────────────────────┐
│                   Aircraft Lifecycle                         │
└───────┬───────────────────────────────────────┬─────────────┘
        │                                       │
   ┌────▼────────┐                        ┌────▼─────────────┐
   │ Design Phase│                        │ Operational Phase│
   │ (DO-326A)   │                        │ (DO-355)         │
   │             │                        │                  │
   │ • Security  │──────────────────────▶ │ • Vulnerability  │
   │   planning  │    Handoff             │   monitoring     │
   │ • Threat    │   Security             │ • Patch mgmt     │
   │   modeling  │   Baseline             │ • Incident       │
   │ • Implement │                        │   response       │
   │ • Verify    │                        │ • Threat intel   │
   └─────────────┘                        └──────────────────┘
       (Years 0-5)                           (Years 5-30+)
```

**Key Stakeholders:**

| Role | Responsibility | DO-355 Activities |
|:-----|:---------------|:------------------|
| **Aircraft Manufacturer** | Design authority | Provide security baseline, issue service bulletins |
| **Airline Operator** | Operations | Monitor fleet, apply patches, incident response |
| **Maintenance Organization** | Service | Secure maintenance procedures, software loading |
| **Regulatory Authority** | Oversight | Enforce continuing airworthiness directives |
| **Equipment Supplier** | Component support | Vulnerability disclosure, patch development |

════════════════════════════════════════════════════════════════════════════

🔍 **VULNERABILITY MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**Vulnerability Lifecycle:**

.. code-block:: text

   1. Discovery
      │ (Internal testing, external researcher, threat intel)
      ▼
   2. Assessment
      │ (Impact analysis: Does it affect safety? Which aircraft?)
      ▼
   3. Prioritization
      │ (Critical/High/Medium/Low based on exploitability + impact)
      ▼
   4. Patch Development
      │ (OEM develops fix, tests with DO-178C/DO-254 rigor)
      ▼
   5. Patch Distribution
      │ (Service bulletin, MMEL/MEL update, AD if critical)
      ▼
   6. Patch Deployment
      │ (Operator applies during maintenance window)
      ▼
   7. Verification
      │ (Confirm patch applied correctly, monitor for issues)
      ▼
   8. Closure
      (Document, update security baseline)

**Vulnerability Scoring Example:**

.. code-block:: python

   # Aviation-specific vulnerability scoring (DO-355)
   
   class AviationVulnerability:
       def __init__(self, cve_id, description):
           self.cve_id = cve_id
           self.description = description
           self.cvss_score = 0.0
           self.aviation_impact = None
           self.affected_systems = []
           self.priority = None
       
       def assess_aviation_impact(self):
           """
           Assess impact specific to aviation operations
           Beyond CVSS: Consider safety, operational, regulatory impact
           """
           
           # Safety Impact (highest priority)
           if any(sys in ['FMS', 'Flight Control', 'Engine Control'] 
                  for sys in self.affected_systems):
               self.aviation_impact = 'SAFETY_CRITICAL'
               self.priority = 'P0'  # Immediate action
               
           # Operational Impact
           elif any(sys in ['Navigation', 'Communication', 'Weather Radar']
                    for sys in self.affected_systems):
               self.aviation_impact = 'OPERATIONALLY_SIGNIFICANT'
               self.priority = 'P1'  # Next maintenance window
               
           # Non-critical
           else:
               self.aviation_impact = 'LOW'
               self.priority = 'P2'  # Routine update
       
       def requires_airworthiness_directive(self):
           """
           Determine if FAA Airworthiness Directive (AD) required
           """
           return (self.aviation_impact == 'SAFETY_CRITICAL' and
                   self.cvss_score >= 7.0)
   
   # Example: Vulnerability in FMS navigation database parser
   vuln = AviationVulnerability(
       'CVE-2024-XXXX',
       'Buffer overflow in FMS navigation database parser'
   )
   vuln.cvss_score = 9.8  # Critical CVSS
   vuln.affected_systems = ['FMS']
   vuln.assess_aviation_impact()
   
   print(f"Priority: {vuln.priority}")  # P0
   print(f"AD Required: {vuln.requires_airworthiness_directive()}")  # True

**Vulnerability Disclosure Process:**

.. code-block:: text

   Coordinated Vulnerability Disclosure (CVD) for Avionics:
   
   Day 0: Researcher discovers vulnerability in avionics system
   ├─ Contact: CISA (Cyber Infrastructure Security Agency)
   │  or manufacturer security team
   │
   Day 1-7: Initial triage
   ├─ Manufacturer validates vulnerability
   ├─ Impact assessment (which aircraft/systems affected?)
   ├─ Determine if safety-related
   │
   Day 8-90: Patch development
   ├─ Develop fix following DO-178C/DO-254 processes
   ├─ Regression testing (ensure no new issues)
   ├─ Coordination with airlines for field testing
   │
   Day 90: Public disclosure
   ├─ If not safety-critical: Standard 90-day disclosure
   ├─ If safety-critical: Expedited (may be <90 days)
   ├─ Issue service bulletin + security advisory
   ├─ FAA may issue Emergency AD if catastrophic risk
   │
   Post-disclosure: Monitoring
   ├─ Monitor for exploitation in the wild
   ├─ Track patch deployment across fleet
   └─ Update threat intelligence

════════════════════════════════════════════════════════════════════════════

🔄 **PATCH MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**Challenges in Aviation:**

Aviation patch management is more complex than IT:

| Challenge | IT Environment | Aviation Environment |
|:----------|:---------------|:---------------------|
| **Downtime** | Minutes-hours acceptable | Aircraft downtime costs $10K-$50K/hour |
| **Testing** | Staging environment | Must test with full DO-178C rigor |
| **Rollback** | Easy (snapshot restore) | Difficult (certified configuration) |
| **Approval** | IT manager | FAA/EASA approval may be required |
| **Fleet size** | Homogeneous | Heterogeneous (different avionics configs) |

**Patch Classification:**

.. code-block:: text

   Emergency Patch (Deploy within 24-48 hours):
   ✓ Actively exploited vulnerability
   ✓ Safety-critical system affected
   ✓ No workaround available
   ✓ Example: Remote code execution in flight control computer
   
   High-Priority Patch (Deploy within 30 days):
   ✓ High-severity vulnerability (CVSS 7.0+)
   ✓ Affects safety-significant systems
   ✓ Workaround available but cumbersome
   ✓ Example: Authentication bypass in FMS
   
   Routine Patch (Deploy within 90-180 days):
   ✓ Medium severity (CVSS 4.0-6.9)
   ✓ Non-safety systems
   ✓ Example: Denial-of-service in IFE system
   
   Deferred Patch (Next major upgrade):
   ✓ Low severity (CVSS < 4.0)
   ✓ No operational impact
   ✓ Example: Information disclosure in maintenance interface

**Patch Deployment Process:**

.. code-block:: python

   # Aviation patch deployment workflow
   
   class AviationPatch:
       def __init__(self, patch_id, systems_affected):
           self.patch_id = patch_id
           self.systems = systems_affected
           self.status = 'PENDING'
       
       def validate_prerequisites(self):
           """
           Check if aircraft configuration supports patch
           """
           checks = [
               self.check_baseline_version(),
               self.check_hardware_compatibility(),
               self.check_regulatory_approval()
           ]
           return all(checks)
       
       def deploy_to_aircraft(self, aircraft_id):
           """
           Secure patch deployment process
           """
           
           # 1. Pre-deployment checks
           if not self.validate_prerequisites():
               return False
           
           # 2. Backup current configuration
           backup_config(aircraft_id)
           
           # 3. Verify patch signature (ECDSA-P384)
           if not verify_patch_signature(self.patch_id):
               log_security_event('PATCH_SIGNATURE_FAIL', aircraft_id)
               return False
           
           # 4. Apply patch to staging partition
           apply_patch_to_staging(self.patch_id, aircraft_id)
           
           # 5. Run built-in tests (BITE)
           if not run_bite_tests(aircraft_id):
               rollback_to_backup(aircraft_id)
               return False
           
           # 6. Activate patch (require reboot)
           schedule_activation(aircraft_id)
           
           # 7. Post-deployment verification
           self.status = 'DEPLOYED'
           log_deployment(aircraft_id, self.patch_id)
           
           return True
   
   # Example usage
   patch = AviationPatch('SB-2024-042', ['FMS', 'ACARS'])
   success = patch.deploy_to_aircraft('N12345')

**Secure Software Loading:**

.. code-block:: c

   // DO-355: Secure software loading station (ARINC 615A)
   #include <stdint.h>
   #include "arinc615a.h"
   #include "crypto/ecdsa.h"
   
   typedef struct {
       char part_number[20];
       char version[10];
       uint32_t crc32;
       uint8_t signature[96];  // ECDSA-P384
       uint8_t data[];
   } SoftwareLoadablePackage;
   
   bool load_software_secure(const char *file_path, const char *target_lru) {
       SoftwareLoadablePackage *pkg;
       
       // 1. Read load file from portable media
       if (!read_load_file(file_path, &pkg)) {
           return false;
       }
       
       // 2. Verify digital signature
       if (!verify_package_signature(pkg)) {
           log_event(LOAD_FAIL_SIGNATURE, target_lru);
           display_error("INVALID SIGNATURE - LOAD ABORTED");
           return false;
       }
       
       // 3. Check part number compatibility
       if (!check_part_compatibility(pkg->part_number, target_lru)) {
           log_event(LOAD_FAIL_COMPATIBILITY, target_lru);
           display_error("INCOMPATIBLE PART NUMBER");
           return false;
       }
       
       // 4. Verify CRC32 integrity
       uint32_t calculated_crc = calc_crc32(pkg->data, pkg->data_size);
       if (calculated_crc != pkg->crc32) {
           log_event(LOAD_FAIL_CRC, target_lru);
           display_error("DATA CORRUPTION DETECTED");
           return false;
       }
       
       // 5. Transfer to LRU via ARINC 615A protocol
       if (!arinc615a_upload(target_lru, pkg->data, pkg->data_size)) {
           log_event(LOAD_FAIL_TRANSFER, target_lru);
           return false;
       }
       
       // 6. Verify load success
       if (!arinc615a_verify_load(target_lru, pkg->version)) {
           log_event(LOAD_FAIL_VERIFICATION, target_lru);
           return false;
       }
       
       // 7. Log successful load (for continuing airworthiness records)
       log_event(LOAD_SUCCESS, target_lru);
       record_software_change(target_lru, pkg->part_number, pkg->version);
       
       // 8. Require dual-person integrity check (DO-355 recommendation)
       require_supervisor_approval();
       
       return true;
   }

════════════════════════════════════════════════════════════════════════════

🚨 **INCIDENT RESPONSE**
─────────────────────────────────────────────────────────────────────────

**Aviation Security Incident Categories:**

| Category | Example | Response Time | Authority Notification |
|:---------|:--------|:--------------|:-----------------------|
| **Critical** | Active cyberattack on flight-critical system | Immediate | FAA, CISA, FBI |
| **High** | Malware detected on avionics network | <4 hours | FAA, airline security |
| **Medium** | Unauthorized access attempt | <24 hours | Airline security |
| **Low** | Security policy violation | <7 days | Internal only |

**Incident Response Plan:**

.. code-block:: text

   DO-355 Incident Response Framework:
   
   Phase 1: DETECTION
   ├─ Intrusion detection system alerts
   ├─ Anomaly in system logs
   ├─ Crew reports unusual behavior
   └─ Threat intelligence indicators
   
   Phase 2: CONTAINMENT
   ├─ Isolate affected systems (if safe to do so)
   ├─ Disable compromised interfaces
   ├─ Switch to backup systems
   └─ Notify flight crew (if in flight)
   
   Phase 3: ANALYSIS
   ├─ Forensics: What happened? How?
   ├─ Impact assessment: Safety implications?
   ├─ Root cause: Vulnerability? Misconfiguration?
   └─ Attribution: Who? Why? (if possible)
   
   Phase 4: ERADICATION
   ├─ Remove malware/backdoors
   ├─ Patch vulnerability
   ├─ Reset credentials
   └─ Restore from clean backup
   
   Phase 5: RECOVERY
   ├─ Return to service (with approval)
   ├─ Enhanced monitoring
   ├─ Crew briefing
   └─ Update security baseline
   
   Phase 6: POST-INCIDENT
   ├─ Lessons learned
   ├─ Update incident response plan
   ├─ Fleet-wide assessment (other aircraft vulnerable?)
   └─ Regulatory reporting (NTSB if safety event)

**Example: In-Flight Security Event:**

.. code-block:: text

   Scenario: Malware Detected on In-Flight Entertainment (IFE)
   
   T+0 min: IFE shows signs of compromise (unusual network traffic)
   Actions:
   ✓ Cabin crew notifies flight deck
   ✓ Flight deck disables IFE network (isolate from avionics)
   ✓ Continue flight normally (IFE isolated, no safety impact)
   
   T+30 min: Ground security team notified via ACARS
   Actions:
   ✓ Security Operations Center (SOC) begins remote analysis
   ✓ Check if other aircraft in fleet affected
   ✓ Prepare incident response team at destination
   
   Landing: Aircraft arrives safely
   Actions:
   ✓ IR team boards aircraft, collects forensics
   ✓ IFE system reimaged from clean baseline
   ✓ Network logs analyzed for IoC (Indicators of Compromise)
   ✓ FAA notified (informational, no safety impact)
   
   T+24 hours: Root cause identified
   Cause: Passenger exploited unpatched IFE vulnerability
   Actions:
   ✓ Emergency patch developed and tested
   ✓ Fleet-wide deployment within 48 hours
   ✓ Service bulletin issued
   ✓ Update IFE monitoring rules

════════════════════════════════════════════════════════════════════════════

📡 **THREAT INTELLIGENCE**
─────────────────────────────────────────────────────────────────────────

**Aviation Threat Intelligence Sources:**

.. code-block:: text

   1. CISA (Cybersecurity & Infrastructure Security Agency)
      - Aviation Cyber Initiative (ACI)
      - ICS-CERT advisories
      - Threat briefings for TSA/FAA
   
   2. Aviation-ISAC (Information Sharing and Analysis Center)
      - Industry threat intelligence sharing
      - Member-contributed indicators
      - Best practice dissemination
   
   3. Manufacturer Security Bulletins
      - OEM-specific vulnerability disclosures
      - Patch availability notifications
   
   4. Open-Source Intelligence (OSINT)
      - CVE database monitoring
      - Aviation security research (conferences, papers)
      - Dark web monitoring (threat actor discussions)
   
   5. Commercial Threat Intelligence
      - Mandiant, CrowdStrike, FireEye feeds
      - Sector-specific analysis

**Threat Intelligence Integration:**

.. code-block:: python

   # Automated threat intelligence processing
   import requests
   import json
   
   class AviationThreatIntel:
       def __init__(self):
           self.indicators = []
           self.affected_systems = []
       
       def fetch_cisa_advisories(self):
           """
           Fetch latest CISA ICS-CERT advisories
           Filter for aviation/avionics systems
           """
           url = "https://www.cisa.gov/uscert/ics/advisories.json"
           response = requests.get(url)
           advisories = response.json()
           
           aviation_advisories = [
               adv for adv in advisories
               if any(keyword in adv['title'].lower() 
                      for keyword in ['avionics', 'aircraft', 'aviation', 
                                       'arinc', 'flight'])
           ]
           
           return aviation_advisories
       
       def correlate_with_fleet(self, advisory):
           """
           Determine if advisory affects our fleet
           """
           affected_products = advisory.get('affected_products', [])
           
           # Check against fleet inventory
           fleet_affected = []
           for aircraft in get_fleet_inventory():
               for system in aircraft['avionics_systems']:
                   if system['part_number'] in affected_products:
                       fleet_affected.append({
                           'aircraft': aircraft['tail_number'],
                           'system': system['name'],
                           'advisory': advisory['id']
                       })
           
           return fleet_affected
       
       def generate_action_items(self, correlation_results):
           """
           Create actionable tasks for security team
           """
           actions = []
           
           for result in correlation_results:
               actions.append({
                   'priority': self.determine_priority(result),
                   'aircraft': result['aircraft'],
                   'action': 'Apply patch per advisory ' + result['advisory'],
                   'deadline': self.calculate_deadline(result)
               })
           
           return actions

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: What is the primary difference between DO-326A and DO-355?**

**A1:**
- **DO-326A** covers **design-time security** (development, certification)
- **DO-355** covers **runtime security** (operational phase, continuing airworthiness)

**Analogy:** DO-326A = building a secure house; DO-355 = maintaining house security over decades

**Key DO-355 activities:**
- Vulnerability monitoring (new CVEs discovered years after certification)
- Patch management (update fleet without recertification)
- Incident response (handle security events in operations)
- Threat intelligence (adapt to evolving threats)

**Q2: Why is patch management more challenging in aviation than traditional IT?**

**A2:**
**Challenges:**
1. **Safety certification:** Patches must undergo DO-178C/DO-254 rigor (months, not days)
2. **Downtime costs:** Aircraft generates revenue only when flying ($10K-50K/hour idle)
3. **Fleet heterogeneity:** Different aircraft may have different avionics configurations
4. **Regulatory approval:** FAA/EASA may need to approve critical patches
5. **Testing requirements:** Cannot simply "deploy and monitor" — must prove safety
6. **Rollback difficulty:** Cannot quickly revert certified configuration

**Example:** IT patch deployed in days/weeks; aviation patch may take 3-6 months from discovery to fleet-wide deployment.

**Q3: Describe the coordinated vulnerability disclosure process for avionics.**

**A3:**
**Timeline:**
- **Day 0:** Vulnerability discovered (researcher or internal)
- **Day 1-7:** Triage by manufacturer, impact assessment
- **Day 8-90:** Patch development (following DO-178C/DO-254 processes)
- **Day 90:** Public disclosure + service bulletin release
- **Exception:** If safety-critical, expedited process (<90 days) + FAA Emergency AD

**Key differences from general IT:**
- **Safety focus:** Assessment includes safety impact analysis
- **Regulatory involvement:** FAA/EASA may issue Airworthiness Directives
- **Industry coordination:** Aviation-ISAC used for information sharing
- **Longer patch cycle:** 90 days often insufficient for full DO-178C/DO-254 cycle

**Q4: What is an Airworthiness Directive (AD) and when is it issued for cybersecurity?**

**A4:**
**Airworthiness Directive (AD):** Legally enforceable FAA regulation requiring corrective action on aircraft.

**Issued for cybersecurity when:**
1. Vulnerability affects **flight safety** (not just security)
2. Exploitable with **reasonable attacker capability**
3. No acceptable **operational workaround**
4. Affects **certified aircraft in service**

**Example AD scenario:**
*"Remote code execution vulnerability in flight control computer discovered. All operators of Boeing 737 MAX must apply software patch SB-737-31-1234 within 30 days."*

**Compliance:** Mandatory (aircraft cannot fly without compliance)

**Q5: How should an airline respond to malware detected on an in-flight avionics system?**

**A5:**
**Immediate Actions (In-Flight):**
1. **Isolate:** Disconnect affected system from network (if safe to do so)
2. **Assess:** Determine if safety-of-flight affected (consult MEL/MMEL)
3. **Notify:** Inform ATC if operational capabilities degraded
4. **Monitor:** Enhanced monitoring of remaining systems
5. **Continue safely:** Land at nearest suitable airport if safety impacted

**Post-Flight Actions:**
1. **Quarantine aircraft:** Ground until cleared by security team
2. **Forensics:** Analyze logs, memory dumps, network traffic
3. **Eradicate:** Remove malware, restore from clean baseline
4. **Verify:** Comprehensive testing before return to service
5. **Report:** Notify FAA, CISA, airline security leadership
6. **Fleet assessment:** Check other aircraft for same vulnerability

**Regulatory Reporting:** If safety event, report to NTSB within 24 hours.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
