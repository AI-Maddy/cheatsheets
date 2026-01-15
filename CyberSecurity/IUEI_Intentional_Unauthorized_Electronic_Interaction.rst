✈️ **IUEI — INTENTIONAL UNAUTHORIZED ELECTRONIC INTERACTION**
═══════════════════════════════════════════════════════════════════════

**Cyberattacks on Airborne Systems: Threats, Vectors, and Mitigations**  
**Purpose:** Aviation cyber threat taxonomy 🎯 | Attack scenario analysis 🔍 | Defense strategies 🛡️  
**Standard:** DO-326A / DO-356A | Core concept in airworthiness security

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**IUEI (Intentional Unauthorized Electronic Interaction)** is the DO-326A term for **cyberattacks on aircraft systems**. Unlike unintentional failures (hardware faults, software bugs), IUEI involves an **intelligent adversary** deliberately exploiting vulnerabilities to cause harm.

**Key Distinction:** Safety standards (DO-178C, ARP4754A) address random failures. DO-326A addresses **adversarial threats** (IUEI).

**Examples:** Remote hack of flight management system, malware via USB maintenance port, spoofed GPS signals, malicious software load, Wi-Fi exploitation to access avionics.

════════════════════════════════════════════════════════════════════════════

🎯 **IUEI DEFINITION & SCOPE**
─────────────────────────────────────────────────────────────────────────

**Official Definition (DO-326A):**

*"Intentional Unauthorized Electronic Interaction (IUEI) is a deliberate attempt to gain unauthorized access to, or cause unintended behavior in, airborne systems via electronic means."*

**Key Characteristics:**

| Aspect | Traditional Failure | IUEI (Cyberattack) |
|:-------|:-------------------|:-------------------|
| **Intent** | Accidental | **Deliberate** |
| **Intelligence** | None (random) | **Adversarial** (adaptive) |
| **Probability** | Statistically predictable | Non-deterministic (depends on attacker motivation) |
| **Attack Surface** | Hardware/software complexity | **Electronic interfaces** (wireless, wired, removable media) |
| **Evolution** | Degrades over time (wear) | **Improves** (0-days discovered, exploits refined) |
| **Mitigation** | Redundancy, monitoring | **Security controls** (authentication, encryption, isolation) |

**Why "Intentional Unauthorized"?**

- **Intentional:** Not accidental (excludes pilot error, HW failure)
- **Unauthorized:** Attacker has no legitimate access right
- **Electronic:** Via electronic means (excludes physical sabotage like bombs)
- **Interaction:** Active engagement with system (not passive eavesdropping)

════════════════════════════════════════════════════════════════════════════

🚪 **IUEI ATTACK VECTORS**
─────────────────────────────────────────────────────────────────────────

**Category 1: Wireless Interfaces**

**1.1 Wi-Fi (Passenger/Crew)**
- **Exposure:** Passenger devices, IFE systems
- **Attack:** Exploit IFE vulnerability → pivot to avionics
- **Example:** 2015 researcher claimed to control aircraft via IFE (disputed)
- **Mitigation:** Network segregation (firewall/air gap between IFE and avionics)

**1.2 Cellular/Datalink (ACARS, FANS, ADS-B)**
- **Exposure:** Air-ground communication
- **Attack:** Message injection, spoofing, man-in-the-middle
- **Example:** Researchers demonstrated forged ATC clearances via ACARS
- **Mitigation:** Message authentication (HMAC), encryption

**1.3 GPS/GNSS**
- **Exposure:** Navigation receivers
- **Attack:** GPS spoofing (false position), jamming
- **Example:** Iranian RQ-170 drone reportedly captured via GPS spoofing (2011)
- **Mitigation:** Multi-constellation GNSS, integrity monitoring (RAIM)

**1.4 Satcom**
- **Exposure:** Broadband satellite communication
- **Attack:** Exploit satellite modem, eavesdrop on link
- **Example:** 2018 research showed satcom modems vulnerable to remote code execution
- **Mitigation:** Firmware signing, network isolation

**Category 2: Wired Interfaces**

**2.1 USB Ports (Maintenance, EFB)**
- **Exposure:** Cockpit USB ports for EFB, maintenance laptop connection
- **Attack:** Malicious USB device (BadUSB), infected navigation database
- **Example:** Stuxnet used USB as infection vector (not aviation, but demonstrates risk)
- **Mitigation:** USB disabled in flight mode, device whitelisting, database signature verification

**2.2 ARINC 664 (AFDX Ethernet)**
- **Exposure:** Avionics Ethernet network
- **Attack:** Packet injection, ARP spoofing, flooding DoS
- **Example:** Researchers demonstrated traffic injection on AFDX (lab environment)
- **Mitigation:** AFDX traffic policing (ARINC 664 Part 7), VLANs, integrity checks

**2.3 ARINC 429**
- **Exposure:** Traditional avionics bus (unidirectional)
- **Attack:** Difficult (one-way), but receiver could be exploited with malformed messages
- **Example:** Fuzzing ARINC 429 parsers to find buffer overflows
- **Mitigation:** Input validation, bounds checking

**Category 3: Removable Media**

**3.1 Software Loading (ARINC 615A)**
- **Exposure:** Maintenance laptop loads software via portable media
- **Attack:** Malicious software disguised as legitimate update
- **Example:** Malware in navigation database update
- **Mitigation:** Digital signatures (ECDSA), dual-person integrity checks

**3.2 Navigation Databases**
- **Exposure:** Monthly database updates via USB/SD card
- **Attack:** Modified waypoint coordinates, altered approach procedures
- **Example:** Hypothetical attack shifting runway threshold by 500 feet
- **Mitigation:** Database signing, CRC checks, pilot verification

**Category 4: Supply Chain**

**4.1 Compromised Components**
- **Exposure:** Hardware/software from supplier
- **Attack:** Trojan in FPGA bitstream, backdoor in firmware
- **Example:** Counterfeit components with hidden functionality
- **Mitigation:** Component authentication, SBOM (Software Bill of Materials), supplier audits

**4.2 Insider Threats**
- **Exposure:** Manufacturing, maintenance, engineering
- **Attack:** Malicious code inserted by insider during development
- **Example:** Disgruntled employee inserting logic bomb
- **Mitigation:** Code review, access controls, monitoring

**Attack Vector Summary:**

.. code-block:: text

   IUEI Attack Surface by Connectivity Type:
   
   📡 Wireless (HIGH RISK)
   ├─ Wi-Fi: IFE, crew tablets
   ├─ Cellular: ACARS, FANS
   ├─ Satellite: Broadband, Iridium
   ├─ GPS: Spoofing, jamming
   └─ ADS-B: Spoofing (no authentication)
   
   🔌 Wired (MEDIUM RISK)
   ├─ USB: Maintenance, EFB
   ├─ Ethernet: AFDX, avionics network
   ├─ ARINC 429: Limited (one-way)
   └─ RS-232/422: Legacy interfaces
   
   💾 Removable Media (MEDIUM RISK)
   ├─ USB drives: Software loads
   ├─ SD cards: Navigation databases
   └─ DVDs: Manuals, documentation
   
   🏭 Supply Chain (LOW FREQUENCY, HIGH IMPACT)
   ├─ Compromised hardware
   ├─ Malicious firmware
   └─ Insider threats

════════════════════════════════════════════════════════════════════════════

💀 **IUEI THREAT ACTORS**
─────────────────────────────────────────────────────────────────────────

**Threat Actor Classification:**

| Actor Type | Capability | Motivation | Likelihood | Example Attacks |
|:-----------|:-----------|:-----------|:-----------|:----------------|
| **Nation-State** | High (zero-days, custom tools) | Espionage, sabotage | Low | GPS spoofing, supply chain compromise |
| **Terrorist** | Medium (off-the-shelf exploits) | Mass casualties, publicity | Low | Remote hijack attempt, crash via FMS |
| **Cybercriminal** | Medium (exploit kits) | Financial gain (rare in aviation) | Very Low | Ransomware on airline IT (not aircraft) |
| **Hacktivist** | Low-Medium | Publicity, political statement | Low | Website defacement, not direct aircraft attack |
| **Insider** | Varies (depends on access) | Revenge, ideology | Low | Logic bomb, backdoor in maintenance |
| **Researcher** | Medium-High (security expertise) | Responsible disclosure, academic | Medium | Vulnerability discovery in IFE, ACARS |

**Attacker Capabilities by SAL:**

| SAL | Assumed Attacker Capability |
|:----|:----------------------------|
| **SAL 0** | No protection needed (no safety/security impact) |
| **SAL 1** | Casual attacker (low sophistication, opportunistic) |
| **SAL 2** | Skilled attacker (exploits known vulnerabilities, moderate resources) |
| **SAL 3** | Sophisticated attacker (nation-state, zero-day exploits, high resources) |

════════════════════════════════════════════════════════════════════════════

🛡️ **IUEI MITIGATION STRATEGIES**
─────────────────────────────────────────────────────────────────────────

**Defense-in-Depth Layers:**

**Layer 1: Isolation**
- **Network segmentation:** IFE ↔ Avionics air gap
- **Physical isolation:** Disable unused interfaces
- **Logical isolation:** VLANs, firewalls

.. code-block:: text

   Example: Boeing 787 Network Architecture
   
   ┌─────────────────────────────────────────┐
   │ Common Data Network (CDN)               │
   │ (Avionics data bus - ARINC 664)         │
   │ SAL 2-3 systems: FMS, flight control    │
   └───────────────┬─────────────────────────┘
                   │
            ┌──────▼──────┐
            │  Firewall   │ (One-way data diode)
            │  + IDS      │
            └──────┬──────┘
                   │
   ┌───────────────▼─────────────────────────┐
   │ Passenger Information System            │
   │ SAL 1: Moving map display               │
   └───────────────┬─────────────────────────┘
                   │
            ┌──────▼──────┐
            │  Firewall   │ (No inbound allowed)
            └──────┬──────┘
                   │
   ┌───────────────▼─────────────────────────┐
   │ In-Flight Entertainment (IFE)           │
   │ SAL 0: Passenger entertainment          │
   │ Connected to: Passenger Wi-Fi           │
   └─────────────────────────────────────────┘

**Layer 2: Authentication**
- Message authentication (HMAC for ACARS)
- Device authentication (USB whitelist)
- User authentication (dual-factor for maintenance)

.. code-block:: c

   // ACARS message authentication
   bool verify_acars_message(AcarsMessage *msg) {
       // 1. Verify HMAC
       uint8_t calculated_hmac[32];
       hmac_sha256(shared_key, 32, msg->content, msg->length, calculated_hmac);
       
       if (memcmp(msg->hmac, calculated_hmac, 32) != 0) {
           log_security_event(ACARS_AUTH_FAIL, msg->msg_id);
           return false;  // Reject forged message
       }
       
       // 2. Check sequence number (anti-replay)
       if (msg->sequence <= last_sequence) {
           log_security_event(ACARS_REPLAY, msg->msg_id);
           return false;
       }
       
       last_sequence = msg->sequence;
       return true;
   }

**Layer 3: Integrity**
- Digital signatures for software loading
- CRC/checksums for data integrity
- Secure boot (verify all code before execution)

.. code-block:: c

   // Navigation database integrity verification
   bool load_navigation_database(const char *file_path) {
       NavDatabase db;
       
       // 1. Read database file
       read_database(file_path, &db);
       
       // 2. Verify ECDSA-P384 signature
       if (!verify_signature_ecdsa384(db.data, db.size, db.signature)) {
           display_error("NAV DATABASE SIGNATURE INVALID");
           log_security_event(DB_SIG_FAIL);
           return false;  // Reject tampered database
       }
       
       // 3. Verify CRC32 (additional integrity check)
       uint32_t crc = calculate_crc32(db.data, db.size);
       if (crc != db.crc32) {
           display_error("NAV DATABASE CORRUPTED");
           return false;
       }
       
       // 4. Load into protected memory
       memcpy(protected_nav_db, db.data, db.size);
       return true;
   }

**Layer 4: Monitoring & Detection**
- Intrusion detection systems (IDS)
- Anomaly detection (unusual traffic patterns)
- Security logging and alerting

.. code-block:: python

   # IDS for avionics network (simplified)
   class AvionicsIDS:
       def __init__(self):
           self.baseline = {}
           self.alerts = []
       
       def learn_baseline(self, traffic_logs):
           """Learn normal traffic patterns"""
           for log in traffic_logs:
               src_dst = (log['src'], log['dst'])
               if src_dst not in self.baseline:
                   self.baseline[src_dst] = {
                       'avg_rate': 0,
                       'avg_size': 0,
                       'protocols': set()
                   }
               # Update statistics...
       
       def detect_anomaly(self, packet):
           """Detect unusual traffic"""
           src_dst = (packet['src'], packet['dst'])
           
           # Check 1: Unknown source/destination pair
           if src_dst not in self.baseline:
               self.alerts.append({
                   'type': 'UNKNOWN_TRAFFIC',
                   'severity': 'HIGH',
                   'description': f'Traffic from {packet["src"]} to {packet["dst"]} not in baseline'
               })
               return True
           
           # Check 2: Abnormal packet rate
           current_rate = calculate_rate(packet)
           baseline_rate = self.baseline[src_dst]['avg_rate']
           
           if current_rate > baseline_rate * 3:  # 3x threshold
               self.alerts.append({
                   'type': 'TRAFFIC_FLOOD',
                   'severity': 'MEDIUM',
                   'description': f'Packet rate {current_rate} exceeds baseline'
               })
               return True
           
           return False

**Layer 5: Rapid Response**
- Incident response plan
- Automated containment (isolate compromised system)
- Rapid patching capability

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: How does IUEI differ from traditional airworthiness concerns?**

**A1:**

| Aspect | Traditional Airworthiness | IUEI (Cybersecurity) |
|:-------|:--------------------------|:---------------------|
| **Threat** | Random failures, wear-out | Intelligent adversary |
| **Intent** | Unintentional | **Deliberate attack** |
| **Predictability** | Statistical (MTBF, failure rates) | Non-deterministic (depends on attacker) |
| **Standards** | DO-178C, DO-254, ARP4754A | **DO-326A, DO-356A** |
| **Mitigation** | Redundancy, monitoring, safe design | **Security controls** (auth, encryption, isolation) |
| **Evolution** | Degrades over time | **Improves** (new vulnerabilities discovered) |

**Key insight:** Safety standards assume no malicious intent. IUEI requires different mindset: **assume adversary** exists and will find/exploit weaknesses.

**Q2: Describe a realistic IUEI attack scenario on a flight management system.**

**A2:**
**Scenario: USB-based FMS Attack**

**Stage 1: Initial Access**
- Attacker targets airline maintenance contractor
- Delivers malicious USB device disguised as navigation database update
- Social engineering: "Urgent NOTAM update required"

**Stage 2: Execution**
- Maintenance technician plugs USB into FMS during routine update
- Malware exploits buffer overflow in database parser
- Payload executes with FMS privileges

**Stage 3: Persistence**
- Malware modifies waypoint coordinates in active flight plan
- Changes stored in non-volatile memory (survives reboot)
- Subtle changes (5-10nm offset) to avoid immediate detection

**Stage 4: Impact**
- Aircraft follows modified flight plan
- Deviation not noticed until ATC query or terrain warning
- Potential CFIT in mountainous terrain

**Mitigations:**
1. Digital signature verification (reject unsigned databases)
2. USB disabled except in maintenance mode (require authentication)
3. Waypoint sanity checks (compare with onboard database)
4. Pilot cross-check (compare FMS route with charts)
5. Dual-person integrity (two maintenance personnel verify updates)

**Q3: Why is network segregation critical for IUEI prevention?**

**A3:**
**Without segregation:** Attack path from passenger Wi-Fi → IFE → Avionics → Flight Control (catastrophic)

**With segregation:**
- **Layer 1:** Firewall between Wi-Fi and IFE (blocks most attacks)
- **Layer 2:** Air gap or one-way data diode between IFE and avionics info system
- **Layer 3:** Firewall + IDS between info system and control domain
- **Result:** Attacker must breach MULTIPLE independent barriers

**Defense-in-depth principle:** Even if IFE compromised (SAL 0), attacker cannot reach SAL 3 flight control systems.

**Real-world:** Boeing 787 uses physical separation + firewalls. Airbus A350 similar architecture.

**Q4: What is the role of ACARS message authentication in IUEI mitigation?**

**A4:**
**Problem:** ACARS (Aircraft Communications Addressing and Reporting System) traditionally has NO authentication
- Anyone with radio equipment can send ACARS messages
- Attacker could impersonate ATC, airline ops, or other aircraft

**IUEI Risk:**
- Forged clearances ("Descend to 1000 feet" over mountains)
- False weather data
- Malicious route changes

**Mitigation: Message Authentication**
```c
ACARS_Message {
    char message_id[8];
    char content[220];
    uint8_t hmac[32];  // HMAC-SHA256 using shared key
}
```

**Process:**
1. Ground system calculates HMAC using shared secret key
2. Aircraft verifies HMAC before trusting message
3. Forged messages rejected (no valid HMAC)

**Deployment challenge:** Legacy aircraft don't support authentication (expensive retrofit)

**Q5: How do threat actors differ in aviation IUEI scenarios?**

**A5:**

**Nation-State (Highest Threat to SAL 3):**
- **Capability:** Custom zero-days, supply chain compromise, GPS spoofing
- **Motivation:** Military advantage, espionage
- **Example:** Iranian capture of RQ-170 drone (alleged GPS spoofing)
- **Defense:** SAL 3 process assumes this threat level

**Terrorist (Medium Threat):**
- **Capability:** Off-the-shelf exploits, insider recruitment
- **Motivation:** Mass casualties, publicity
- **Example:** Hypothetical remote hijack attempt
- **Defense:** Network isolation, authentication, monitoring

**Security Researcher (Low Threat):**
- **Capability:** Vulnerability discovery, proof-of-concept exploits
- **Motivation:** Responsible disclosure, academic
- **Example:** Chris Roberts IFE research (2015), Ruben Santamarta satcom research (2014)
- **Defense:** Coordinated vulnerability disclosure, bug bounty programs

**Key Insight:** DO-326A SAL 3 designed for nation-state adversary. Lower SAL levels may accept higher risk.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~800
