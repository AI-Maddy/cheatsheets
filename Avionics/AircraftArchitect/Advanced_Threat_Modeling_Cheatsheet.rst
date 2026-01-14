🔐 **ADVANCED THREAT MODELING — Deep-Dive STRIDE, PASTA, Attack Trees**
═══════════════════════════════════════════════════════════════════════════

**Context:** Advanced threat modeling for safety-critical aviation systems
**Focus:** Attack trees, quantitative risk, MITRE ATT&CK, red team exercises
**Certification:** DO-326A (Airworthiness Security), ED-203A

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — ADVANCED THREAT MODELING IN 60 SECONDS**
──────────────────────────────────────────────────────

**Attack Trees:**

::

    Goal: Hijack IFE System
         ├── AND: Gain physical access + Exploit USB
         └── OR: Remote exploit (WiFi MITM)

**Quantitative Risk:**

::

    ALE (Annual Loss Expectancy) = SLE × ARO
    
    Example:
    - SLE (Single Loss): $2M (incident response + downtime)
    - ARO (Annual Rate): 0.1 (1 incident per 10 years)
    - ALE = $2M × 0.1 = $200K/year
    
    Mitigation cost: $50K/year → ROI = $150K/year

**MITRE ATT&CK for Aviation:**

- **TA0001 Initial Access:** Phishing, USB insertion
- **TA0003 Persistence:** Bootkit in BIOS
- **TA0040 Impact:** Disable IFE, corrupt FMS data

════════════════════════════════════════════════════════════════════

📖 **1. ATTACK TREES**
══════════════════════

**1.1 Concept**
--------------

**Attack Tree:** Hierarchical diagram of attacker goals

**Nodes:**

- **Root:** Ultimate goal (e.g., "Hijack IFE")
- **AND:** All children must succeed
- **OR:** Any child can succeed
- **Leaf:** Atomic attack (e.g., "Exploit CVE-2023-1234")

**1.2 Example: Hijack IFE System**
----------------------------------

::

    Goal: Hijack IFE System [OR]
         ├── Physical Attack [AND]
         │   ├── Gain cockpit access [OR]
         │   │   ├── Insider threat (crew member)
         │   │   └── Breach security checkpoint
         │   └── Exploit USB interface [OR]
         │       ├── Plug malicious USB drive
         │       └── Connect rogue device to maintenance port
         │
         └── Remote Attack [OR]
             ├── WiFi Man-in-the-Middle [AND]
             │   ├── Passenger WiFi enabled
             │   ├── Weak WPA2 key
             │   └── Exploit IFE app vulnerability
             │
             └── Satellite Link Exploit [AND]
                 ├── Intercept Inmarsat traffic
                 ├── Decrypt session key
                 └── Inject malicious commands

**1.3 Quantitative Analysis**
-----------------------------

**Assign probabilities to each path:**

.. code-block:: text

    Physical Attack [AND] → P = 0.001 × 0.01 = 0.00001 (1 in 100,000)
      ├── Gain cockpit access → P = 0.001 (rigorous security)
      └── Exploit USB interface → P = 0.01 (patch CVE)
    
    WiFi MITM [AND] → P = 0.05 × 0.2 × 0.1 = 0.001 (1 in 1,000)
      ├── Passenger WiFi enabled → P = 0.05 (disabled on 95% of flights)
      ├── Weak WPA2 key → P = 0.2 (20% of airlines use default)
      └── Exploit IFE app vuln → P = 0.1 (10% unpatched)
    
    Satellite Link Exploit [AND] → P = 0.001 × 0.0001 × 0.01 = 0.0000000001
      ├── Intercept traffic → P = 0.001 (encryption)
      ├── Decrypt session key → P = 0.0001 (AES-256)
      └── Inject commands → P = 0.01 (authentication)
    
    Total risk = 0.00001 + 0.001 + 0.0000000001 ≈ 0.00101 (0.1%)

**Conclusion:** WiFi MITM is highest risk → Prioritize WPA3 upgrade

**1.4 Cost-Benefit Analysis**
-----------------------------

.. code-block:: python

    # attack_tree_analysis.py
    
    class AttackNode:
        def __init__(self, name, probability, cost, node_type='OR'):
            self.name = name
            self.probability = probability  # Probability of success
            self.cost = cost                # Cost of mitigation
            self.node_type = node_type      # 'AND' or 'OR'
            self.children = []
        
        def add_child(self, child):
            self.children.append(child)
        
        def calculate_risk(self):
            if not self.children:
                return self.probability
            
            if self.node_type == 'AND':
                # All children must succeed
                return np.prod([child.calculate_risk() for child in self.children])
            else:  # OR
                # At least one child succeeds (1 - all fail)
                fail_probs = [1 - child.calculate_risk() for child in self.children]
                return 1 - np.prod(fail_probs)
    
    # Example tree
    root = AttackNode("Hijack IFE", probability=0, cost=0, node_type='OR')
    
    physical = AttackNode("Physical Attack", probability=0, cost=50000, node_type='AND')
    physical.add_child(AttackNode("Gain Access", probability=0.001, cost=10000))
    physical.add_child(AttackNode("Exploit USB", probability=0.01, cost=5000))
    
    wifi = AttackNode("WiFi MITM", probability=0, cost=20000, node_type='AND')
    wifi.add_child(AttackNode("WiFi Enabled", probability=0.05, cost=0))
    wifi.add_child(AttackNode("Weak Key", probability=0.2, cost=10000))
    wifi.add_child(AttackNode("Exploit App", probability=0.1, cost=5000))
    
    root.add_child(physical)
    root.add_child(wifi)
    
    print(f"Overall risk: {root.calculate_risk():.5f}")
    
    # Output: Overall risk: 0.00101

════════════════════════════════════════════════════════════════════

📖 **2. PASTA FRAMEWORK (DEEP-DIVE)**
═════════════════════════════════════

**Process for Attack Simulation and Threat Analysis**

**2.1 Stage 1: Define Objectives**
----------------------------------

**Business Objectives:**

- Protect passenger safety (DO-326A compliance)
- Maintain brand reputation
- Avoid regulatory fines ($10M+ per incident)

**Security Objectives:**

- Prevent unauthorized IFE access
- Ensure FMS data integrity
- Protect passenger PII (GDPR/CCPA)

**Compliance Requirements:**

- DO-326A (Airworthiness Security Process Specification)
- DO-356A (Airworthiness Security Methods and Considerations)
- NIST CSF (Cybersecurity Framework)

**2.2 Stage 2: Define Technical Scope**
---------------------------------------

**System Components:**

+----------------------+-------------------+-------------------------+
| **Component**        | **Criticality**   | **Attack Surface**      |
+======================+===================+=========================+
| FMS (Flight Mgmt)    | DAL A (critical)  | ARINC 429, CAN bus      |
+----------------------+-------------------+-------------------------+
| IFE (Entertainment)  | DAL E (low)       | WiFi, USB, Ethernet     |
+----------------------+-------------------+-------------------------+
| ACARS (Comms)        | DAL B (high)      | Satellite, VHF          |
+----------------------+-------------------+-------------------------+
| EFB (Electronic FB)  | DAL C (medium)    | WiFi, Bluetooth, USB    |
+----------------------+-------------------+-------------------------+

**Trust Boundaries:**

::

    Passenger WiFi ─────X───── IFE Gateway ─────X───── Avionics Network
                   (DMZ)                    (Firewall)
    
    X = Trust boundary (requires authentication + encryption)

**2.3 Stage 3: Application Decomposition**
------------------------------------------

**Data Flow Diagram (Level 1):**

::

    ┌──────────┐       ┌───────────┐       ┌──────────┐
    │ Passenger│──WiFi─▶│ IFE Server│──────▶│ Content  │
    │  Device  │       │           │       │  CDN     │
    └──────────┘       └───────────┘       └──────────┘
                            │
                            │ ARINC 664 (AFDX)
                            ▼
                       ┌───────────┐
                       │   FMS     │
                       └───────────┘

**Entry Points:**

1. WiFi (passenger devices)
2. USB (maintenance ports)
3. Satellite link (ACARS)
4. Ethernet (crew tablet)

**Assets:**

- Flight plan data (FMS)
- Passenger PII (credit cards, passports)
- Entertainment content (licensing $$$)

**2.4 Stage 4: Threat Analysis**
--------------------------------

**Threat Actors:**

+-----------------------+----------------+----------------------------+
| **Actor**             | **Motivation** | **Capability**             |
+=======================+================+============================+
| Script kiddie         | Fun, fame      | Low (use public exploits)  |
+-----------------------+----------------+----------------------------+
| Organized crime       | Financial gain | Medium (custom malware)    |
+-----------------------+----------------+----------------------------+
| Nation-state (APT)    | Espionage      | High (0-day exploits)      |
+-----------------------+----------------+----------------------------+
| Insider (disgruntled) | Revenge        | High (authorized access)   |
+-----------------------+----------------+----------------------------+

**MITRE ATT&CK Mapping:**

.. code-block:: yaml

    - Tactic: TA0001 (Initial Access)
      Technique: T1566 (Phishing)
      Scenario: Spear-phish airline IT staff
    
    - Tactic: TA0002 (Execution)
      Technique: T1059.003 (Command-Line Interface)
      Scenario: Execute malicious script via USB
    
    - Tactic: TA0003 (Persistence)
      Technique: T1542.001 (System Firmware - BIOS)
      Scenario: Flash bootkit to IFE BIOS
    
    - Tactic: TA0005 (Defense Evasion)
      Technique: T1562.001 (Disable Security Tools)
      Scenario: Kill antivirus on IFE server
    
    - Tactic: TA0040 (Impact)
      Technique: T1499 (Endpoint Denial of Service)
      Scenario: Flood IFE with packets → crash system

**2.5 Stage 5: Vulnerability Analysis**
---------------------------------------

**Vulnerability Sources:**

1. **CVE Database:** Known vulnerabilities (e.g., CVE-2023-12345)
2. **Penetration Testing:** Simulate attacks
3. **Code Review:** Static/dynamic analysis
4. **Bug Bounty:** Crowdsourced security

**Example Vulnerabilities:**

+--------------------+----------+--------------------------------+
| **Vulnerability**  | **CVSS** | **Exploit**                    |
+====================+==========+================================+
| Weak WPA2 key      | 7.5 H    | WiFi MITM                      |
+--------------------+----------+--------------------------------+
| SQL injection      | 9.8 C    | Steal passenger PII            |
+--------------------+----------+--------------------------------+
| Hardcoded password | 8.1 H    | Default admin:admin123         |
+--------------------+----------+--------------------------------+
| Buffer overflow    | 9.0 C    | Remote code execution          |
+--------------------+----------+--------------------------------+

**Prioritization:**

::

    Risk = Likelihood × Impact
    
    Example:
    - SQL injection: 0.3 (likely) × 10 (critical) = 3.0 (HIGH)
    - Weak WPA2: 0.8 (very likely) × 5 (medium) = 4.0 (CRITICAL)

**2.6 Stage 6: Attack Modeling**
--------------------------------

**Scenario 1: WiFi Man-in-the-Middle**

::

    1. Passenger enables WiFi on laptop
    2. Attacker sets up rogue AP ("Free_Airline_WiFi")
    3. Passenger connects to rogue AP
    4. Attacker intercepts traffic (HTTP, no HTTPS!)
    5. Attacker injects malicious JavaScript
    6. JavaScript exploits IFE app vulnerability
    7. Attacker gains shell on IFE server
    8. Pivot to avionics network (if firewall misconfigured)

**Kill Chain:**

::

    Reconnaissance → Weaponization → Delivery → Exploitation →
    Installation → C2 → Actions on Objectives

**2.7 Stage 7: Risk & Impact Analysis**
---------------------------------------

**Quantitative Risk:**

.. code-block:: python

    # Annualized Loss Expectancy (ALE)
    SLE = 2_000_000  # Single Loss Expectancy ($2M)
    ARO = 0.1        # Annual Rate of Occurrence (10% chance/year)
    ALE = SLE * ARO  # $200,000/year
    
    # Mitigation cost
    mitigation_cost = 50_000  # WPA3 upgrade
    
    # ROI
    roi = ALE - mitigation_cost  # $150,000/year
    print(f"ROI: ${roi:,.0f}/year → IMPLEMENT MITIGATION")

**Impact Classification:**

+-----------------+-----------------+---------------------------+
| **Category**    | **Impact**      | **Example**               |
+=================+=================+===========================+
| Safety          | Catastrophic    | FMS tampered → crash      |
+-----------------+-----------------+---------------------------+
| Financial       | Major           | $10M regulatory fine      |
+-----------------+-----------------+---------------------------+
| Reputation      | Significant     | Customer trust loss       |
+-----------------+-----------------+---------------------------+
| Operational     | Minor           | IFE down for 1 flight     |
+-----------------+-----------------+---------------------------+

════════════════════════════════════════════════════════════════════

📖 **3. THREAT INTELLIGENCE**
═════════════════════════════

**3.1 MITRE ATT&CK for ICS/Aviation**
-------------------------------------

**Relevant Tactics:**

.. code-block:: text

    TA0108: Initial Access (ICS)
      └── T0817: Drive-by Compromise (malicious USB)
    
    TA0109: Execution (ICS)
      └── T0873: Project File Infection (modify IFE config)
    
    TA0110: Persistence (ICS)
      └── T0857: System Firmware (flash BIOS)
    
    TA0111: Privilege Escalation (ICS)
      └── T0890: Exploitation for Privilege Escalation
    
    TA0113: Lateral Movement (ICS)
      └── T0867: Lateral Tool Transfer (move from IFE to FMS)
    
    TA0104: Impact (ICS)
      └── T0831: Manipulation of Control (disable autopilot)

**Mapping to Aviation:**

+-----------------------+-----------------------------------+
| **ATT&CK Technique**  | **Aviation Scenario**             |
+=======================+===================================+
| T0817 (Drive-by)      | Malicious USB in maintenance port |
+-----------------------+-----------------------------------+
| T0867 (Lateral Mov)   | IFE → EFB → FMS network jump      |
+-----------------------+-----------------------------------+
| T0831 (Control)       | Disable IFE, corrupt FMS waypoint |
+-----------------------+-----------------------------------+

**3.2 CVE Monitoring**
---------------------

**Workflow:**

.. code-block:: python

    # cve_monitor.py
    import requests
    
    def check_cves(software, version):
        """Query NVD for CVEs affecting software"""
        url = f"https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            "keyword": software,
            "resultsPerPage": 10
        }
        response = requests.get(url, params=params)
        cves = response.json()['result']['CVE_Items']
        
        for cve in cves:
            cve_id = cve['cve']['CVE_data_meta']['ID']
            desc = cve['cve']['description']['description_data'][0]['value']
            cvss = cve['impact']['baseMetricV3']['cvssV3']['baseScore']
            
            if cvss >= 7.0:  # High/Critical
                print(f"🚨 {cve_id} (CVSS {cvss}): {desc}")
    
    # Example
    check_cves("linux kernel", "5.15")

**Output:**

::

    🚨 CVE-2023-1234 (CVSS 9.8): Buffer overflow in kernel module
    🚨 CVE-2023-5678 (CVSS 8.1): Privilege escalation via ioctl

**3.3 Threat Intel Feeds**
--------------------------

**Sources:**

- **US-CERT:** Government advisories
- **CISA ICS-CERT:** Industrial control systems
- **AlienVault OTX:** Open Threat Exchange
- **MISP:** Malware Information Sharing Platform

**Integration:**

.. code-block:: python

    # threat_intel.py
    from OTXv2 import OTXv2
    
    otx = OTXv2("YOUR_API_KEY")
    
    # Check if IP is malicious
    ip = "192.0.2.1"
    alerts = otx.get_indicator_details_full(OTXv2.IndicatorTypes.IPv4, ip)
    
    if alerts['general']['pulse_info']['count'] > 0:
        print(f"⚠️ {ip} flagged in {alerts['general']['pulse_info']['count']} threat reports")

════════════════════════════════════════════════════════════════════

📖 **4. RED TEAM EXERCISES**
════════════════════════════

**4.1 Purple Team Approach**
----------------------------

**Purple Team = Red Team (attackers) + Blue Team (defenders)**

**Workflow:**

::

    1. Red Team: Simulate attack (e.g., phishing campaign)
    2. Blue Team: Detect and respond
    3. Review: Analyze gaps in detection
    4. Improve: Update SIEM rules, IDS signatures

**4.2 Attack Scenarios**
-----------------------

**Scenario 1: Phishing + Lateral Movement**

.. code-block:: text

    Day 1:
      - Red Team sends spear-phish to IT staff (fake Airbus email)
      - Email contains malicious PDF (CVE-2023-XXXX)
      - Blue Team: Does antivirus catch it?
    
    Day 2:
      - PDF exploits Acrobat Reader → reverse shell
      - Red Team establishes C2 (Command & Control)
      - Blue Team: Does EDR (Endpoint Detection) alert?
    
    Day 3:
      - Red Team pivots to IFE server (mimikatz for credentials)
      - Blue Team: Does SIEM correlate anomalous login?
    
    Day 4:
      - Red Team exfiltrates FMS database
      - Blue Team: Does DLP (Data Loss Prevention) block?

**Metrics:**

- **MTTD:** Mean Time To Detect (2 hours)
- **MTTR:** Mean Time To Respond (30 minutes)
- **MTTE:** Mean Time To Eradicate (24 hours)

**4.3 Tabletop Exercises**
--------------------------

**Scenario:** IFE ransomware attack mid-flight

**Participants:**

- Incident Response Team
- Flight Operations
- Legal/PR
- CISO

**Timeline:**

::

    T+00:00 - Ransomware detected on IFE server (seat displays locked)
    T+00:15 - IR team isolates IFE from network
    T+00:30 - Confirm: No spread to avionics (FMS unaffected)
    T+01:00 - Legal: Do we pay ransom? ($50K in Bitcoin)
    T+02:00 - Decision: Restore from backup (no ransom payment)
    T+06:00 - IFE restored, passengers notified
    T+48:00 - Post-mortem: Update firewall rules, patch IFE OS

**Lessons Learned:**

- ✅ Network segmentation worked (IFE isolated from FMS)
- ❌ Backup recovery took 6 hours (too slow)
- ❌ No playbook for ransom decision (create one)

════════════════════════════════════════════════════════════════════

📖 **5. INCIDENT RESPONSE**
═══════════════════════════

**5.1 Playbook: IFE Compromise**
--------------------------------

**Phase 1: Preparation**

- [ ] IR team trained
- [ ] SIEM alerts configured
- [ ] Backup tested monthly
- [ ] Legal contact (ransom decision)

**Phase 2: Detection**

::

    Alert: Unusual outbound traffic from IFE server
    
    SIEM Rule:
      IF (src = 10.1.1.100 AND dst_port = 443 AND bytes > 100MB)
      THEN trigger_alert("IFE Data Exfiltration")

**Phase 3: Containment**

.. code-block:: bash

    # Isolate IFE server
    iptables -A OUTPUT -s 10.1.1.100 -j DROP
    
    # Preserve evidence
    dd if=/dev/sda of=/mnt/forensics/ife-disk.img bs=4M
    
    # Snapshot memory
    avml /mnt/forensics/ife-memory.lime

**Phase 4: Eradication**

.. code-block:: bash

    # Identify malware
    clamscan -r / --infected --log=/var/log/clamscan.log
    
    # Remove malware
    rm -rf /tmp/.hidden_backdoor
    
    # Reinstall OS
    ansible-playbook ife-rebuild.yml

**Phase 5: Recovery**

.. code-block:: bash

    # Restore from backup
    rsync -avz /mnt/backup/ife/ /opt/ife/
    
    # Verify integrity
    sha256sum -c /opt/ife/checksums.txt
    
    # Restart service
    systemctl start ife-server

**Phase 6: Lessons Learned**

::

    Root Cause: Weak SSH password (brute-forced)
    Fix: Enforce SSH key-only authentication
    
    $ cat /etc/ssh/sshd_config
    PasswordAuthentication no
    PubkeyAuthentication yes

**5.2 Forensic Analysis**
-------------------------

.. code-block:: python

    # log_analysis.py
    import re
    from collections import Counter
    
    def analyze_logs(logfile):
        """Detect brute-force attacks"""
        with open(logfile) as f:
            lines = f.readlines()
        
        # Extract failed SSH logins
        failed_logins = []
        for line in lines:
            if "Failed password" in line:
                ip = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line).group(1)
                failed_logins.append(ip)
        
        # Count attempts per IP
        attempts = Counter(failed_logins)
        
        # Alert if > 10 attempts
        for ip, count in attempts.items():
            if count > 10:
                print(f"🚨 Brute-force from {ip}: {count} attempts")
    
    analyze_logs("/var/log/auth.log")

**Output:**

::

    🚨 Brute-force from 203.0.113.5: 47 attempts

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** Construct an attack tree for "Disable IFE System". Include at least 3 attack paths and calculate probabilities.

**A1:**

::

    Goal: Disable IFE System [OR]
         ├── Physical Attack [AND]                    P = 0.001 × 0.05 = 0.00005
         │   ├── Gain physical access (cockpit)       P = 0.001
         │   └── Disconnect power cable                P = 0.05
         │
         ├── Software Exploit [AND]                   P = 0.1 × 0.2 = 0.02
         │   ├── Exploit known CVE                     P = 0.1 (unpatched)
         │   └── Crash IFE service                     P = 0.2 (exploit success)
         │
         └── DoS Attack [AND]                          P = 0.05 × 0.8 = 0.04
             ├── Passenger WiFi enabled                P = 0.05
             └── Flood IFE with packets                P = 0.8
    
    Total risk: 0.00005 + 0.02 + 0.04 ≈ 0.06 (6%)

**Highest risk:** DoS attack (4%) → Prioritize rate limiting

────────────────────────────────────────────────────────────────────

**Q2:** Explain the 7 stages of PASTA framework with aviation examples.

**A2:**

1. **Define Objectives:** Protect FMS integrity (DO-326A compliance)
2. **Define Technical Scope:** FMS, IFE, ACARS, EFB + trust boundaries
3. **Application Decomposition:** Data flow diagram (passenger → IFE → FMS)
4. **Threat Analysis:** Identify threat actors (nation-state APT, insider)
5. **Vulnerability Analysis:** CVE scan, pen test (find SQL injection)
6. **Attack Modeling:** Simulate WiFi MITM → IFE compromise → FMS pivot
7. **Risk & Impact:** Calculate ALE ($200K/year), prioritize mitigations

────────────────────────────────────────────────────────────────────

**Q3:** Your SIEM alerts to unusual outbound traffic from IFE server (10 GB to unknown IP). Walk through the incident response steps.

**A3:**

**1. Detection:**

::

    SIEM Alert: IFE server (10.1.1.100) sent 10 GB to 203.0.113.5:443

**2. Containment:**

.. code-block:: bash

    # Isolate IFE from network
    iptables -A OUTPUT -s 10.1.1.100 -j DROP
    
    # Preserve evidence
    dd if=/dev/sda of=/forensics/ife-disk.img

**3. Investigation:**

.. code-block:: bash

    # Check processes
    ps aux | grep -i suspicious
    
    # Analyze network connections
    netstat -antp | grep 203.0.113.5
    
    # Search logs
    grep "203.0.113.5" /var/log/syslog

**4. Eradication:**

.. code-block:: bash

    # Kill malicious process
    kill -9 <PID>
    
    # Remove backdoor
    rm /tmp/.backdoor
    
    # Reinstall OS (if compromised)

**5. Recovery:**

.. code-block:: bash

    # Restore from backup
    rsync -avz /backup/ife/ /opt/ife/
    
    # Verify integrity
    sha256sum -c /opt/ife/checksums.txt

**6. Post-Mortem:**

- Root cause: Weak SSH password
- Fix: SSH key-only auth + fail2ban
- Update playbook: Add SIEM rule for large outbound transfers

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Construct attack trees for critical assets
- [ ] Assign probabilities to attack paths
- [ ] Calculate ALE for top risks
- [ ] Map threats to MITRE ATT&CK for ICS
- [ ] Complete all 7 PASTA stages
- [ ] Set up CVE monitoring automation
- [ ] Integrate threat intel feeds (OTX, CISA)
- [ ] Conduct tabletop exercise (ransomware scenario)
- [ ] Run red team engagement quarterly
- [ ] Document incident response playbooks
- [ ] Train IR team on forensic analysis
- [ ] Review and update SIEM rules monthly

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Attack trees quantify risk** → Assign probabilities, calculate ALE, 
prioritize mitigations

2️⃣ **PASTA is comprehensive** → 7 stages from business objectives to risk 
analysis

3️⃣ **MITRE ATT&CK for ICS** → Map aviation threats to standardized tactics/
techniques

4️⃣ **Threat intel automates detection** → CVE monitoring + OTX feeds catch 
emerging threats

5️⃣ **Purple team > Red team alone** → Collaboration improves detection and 
response

6️⃣ **Tabletop exercises are cheap** → Practice incident response without real 
incidents

7️⃣ **ALE drives decisions** → If mitigation cost < ALE → implement it!

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **ADVANCED THREAT MODELING COMPLETE**
**Created:** January 14, 2026
**Coverage:** Attack Trees, PASTA Framework, MITRE ATT&CK, Red Team, Incident Response

════════════════════════════════════════════════════════════════════
