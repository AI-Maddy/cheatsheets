🏭 **IEC 62443 — INDUSTRIAL CYBERSECURITY OVERVIEW**
═══════════════════════════════════════════════════════════════════════

**Industrial Automation and Control Systems Security (IEC 62443 Series)**  
**Purpose:** SCADA/ICS security 🏭 | Defense-in-depth 🛡️ | OT/IT convergence 🔗  
**Scope:** Process control, manufacturing, utilities, critical infrastructure

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**IEC 62443** is the **global standard for industrial automation cybersecurity** (SCADA, PLC, DCS, ICS).

**Key concepts:**
- **Defense-in-depth:** Multiple security layers (network, application, device)
- **Zones & Conduits:** Network segmentation with controlled data flows
- **Security Levels (SL):** SL 1-4 (similar to ASIL, CAL)
- **Lifecycle:** Secure development, deployment, operations

**Applicable:** Manufacturing, oil & gas, power plants, water treatment, building automation.

════════════════════════════════════════════════════════════════════════════

📚 **IEC 62443 STANDARD STRUCTURE**
─────────────────────────────────────────────────────────────────────────

**Four-Part Series (62443-X-Y):**

.. code-block:: text

   IEC 62443-1: General
   ├─ 62443-1-1: Terminology, concepts, models
   ├─ 62443-1-2: Master glossary
   ├─ 62443-1-3: System security conformance metrics
   └─ 62443-1-4: IACS security lifecycle & use cases
   
   IEC 62443-2: Policies & Procedures (Asset Owner)
   ├─ 62443-2-1: IACS security management system
   ├─ 62443-2-3: Patch management
   ├─ 62443-2-4: Requirements for IACS service providers
   └─ 62443-2-5: Implementation guidance (TR)
   
   IEC 62443-3: System (Integration & Network)
   ├─ 62443-3-1: Security technologies for IACS (TR)
   ├─ 62443-3-2: Security risk assessment for zones/conduits
   ├─ 62443-3-3: System security requirements & security levels
   └─ 62443-3-4: Secure development lifecycle requirements (TR)
   
   IEC 62443-4: Component (Product Development)
   ├─ 62443-4-1: Secure product development lifecycle
   ├─ 62443-4-2: Component security requirements
   └─ 62443-4-3: Host/network device requirements (TR)

**Most Critical Standards:**

| Standard | Focus | Audience |
|:---------|:------|:---------|
| **62443-2-1** | Security management system | Asset owners (plant operators) |
| **62443-3-2** | Risk assessment (zones/conduits) | System integrators |
| **62443-3-3** | System security levels & requirements | System integrators, architects |
| **62443-4-1** | Secure development lifecycle | Product vendors (PLC, SCADA) |
| **62443-4-2** | Component technical requirements | Product vendors |

════════════════════════════════════════════════════════════════════════════

🎯 **SECURITY LEVELS (SL-T, SL-C, SL-A)**
─────────────────────────────────────────────────────────────────────────

**Three Security Level Types:**

**SL-T (Target Security Level):**
- **Who defines:** Asset owner (based on risk assessment)
- **What it means:** Desired security level for zone/system
- **Example:** "Control room network shall achieve SL 3"

**SL-C (Capability Security Level):**
- **Who defines:** Product vendor or system integrator
- **What it means:** Maximum security level product/system can achieve
- **Example:** "This PLC is certified IEC 62443-4-2 SL 2"

**SL-A (Achieved Security Level):**
- **Who defines:** Auditor or integrator (after deployment)
- **What it means:** Actual security level achieved in production
- **Example:** "Installed system achieved SL 2 (SL-T was 3 - gap identified)"

**Security Level Definitions (62443-3-3):**

| SL | Threat Actor | Capability | Motivation | Means | Example Attacker |
|:---|:-------------|:-----------|:-----------|:------|:-----------------|
| **SL 1** | Casual | Low | Low | Generic tools | Curious employee, script kiddie |
| **SL 2** | Intentional | Moderate | Moderate | Simple custom tools | Disgruntled insider, hacktivist |
| **SL 3** | Sophisticated | High | High | Sophisticated tools, resources | Organized crime, terrorist |
| **SL 4** | Nation-state | Very high | Very high | Advanced persistent threat (APT) | Nation-state, cyber warfare |

**SL-to-Security Requirements Mapping:**

.. code-block:: text

   SL 1 (Protect against casual violations)
   ├─ User authentication
   ├─ Basic access control
   └─ Audit logging
   
   SL 2 (adds - Protect against intentional violations)
   ├─ Role-based access control (RBAC)
   ├─ Encrypted communications (TLS)
   ├─ Software/firmware integrity checking
   └─ Malware protection
   
   SL 3 (adds - Protect against sophisticated attacks)
   ├─ Multi-factor authentication
   ├─ Network segmentation (zones/conduits)
   ├─ Intrusion detection systems (IDS)
   ├─ Secure boot
   └─ Penetration testing
   
   SL 4 (adds - Protect against nation-state attacks)
   ├─ Hardware security modules (HSM)
   ├─ Formal verification
   ├─ Red team assessment
   ├─ Continuous monitoring
   └─ Advanced threat intelligence

════════════════════════════════════════════════════════════════════════════

🏗️ **ZONES & CONDUITS (62443-3-2)**
─────────────────────────────────────────────────────────────────────────

**Zone Definition:**
A logical grouping of assets with **similar security requirements** and **risk profile**.

**Conduit Definition:**
A logical grouping of communication channels connecting two or more zones.

**Example: Manufacturing Plant Network Architecture**

.. code-block:: text

   ┌────────────────────────────────────────────────────────────┐
   │ Zone 0: Corporate Network (IT) - SL-T: SL 1              │
   │ ├─ Email, ERP, business applications                      │
   │ └─ Assets: Office PCs, file servers                       │
   └────────────────┬───────────────────────────────────────────┘
                    │ Conduit 0-1 (DMZ Firewall, IDS)
   ┌────────────────▼───────────────────────────────────────────┐
   │ Zone 1: DMZ / Historian - SL-T: SL 2                      │
   │ ├─ Data historian, HMI servers, engineering workstations  │
   │ └─ Assets: SCADA servers, database servers                │
   └────────────────┬───────────────────────────────────────────┘
                    │ Conduit 1-2 (Firewall, unidirectional gateway)
   ┌────────────────▼───────────────────────────────────────────┐
   │ Zone 2: Supervisory Control (Level 3) - SL-T: SL 3       │
   │ ├─ SCADA, HMI, MES (Manufacturing Execution System)       │
   │ └─ Assets: Supervisory controllers, operator stations     │
   └────────────────┬───────────────────────────────────────────┘
                    │ Conduit 2-3 (Managed switch, VLANs)
   ┌────────────────▼───────────────────────────────────────────┐
   │ Zone 3: Process Control (Level 2) - SL-T: SL 3           │
   │ ├─ PLCs, RTUs, local HMIs                                 │
   │ └─ Assets: Controllers, I/O modules                       │
   └────────────────┬───────────────────────────────────────────┘
                    │ Conduit 3-4 (Industrial Ethernet, I/O bus)
   ┌────────────────▼───────────────────────────────────────────┐
   │ Zone 4: Field Devices (Level 1-0) - SL-T: SL 2           │
   │ ├─ Sensors, actuators, drives, field instruments          │
   │ └─ Assets: Smart sensors, variable frequency drives       │
   └────────────────────────────────────────────────────────────┘

**Zone Design Principles:**

1. **Purdue Model Alignment** (ISA-95)
   - Level 0: Physical process
   - Level 1: Sensing & actuation
   - Level 2: Process control (PLC, DCS)
   - Level 3: Supervisory control (SCADA, MES)
   - Level 4: Business logistics (ERP)
   - Level 5: Enterprise

2. **Security Level Consistency**
   - All assets in zone have same SL-T
   - If mixed criticality → split into multiple zones

3. **Minimal Conduits**
   - Reduce inter-zone connections
   - Default deny, explicit allow

4. **Defense-in-Depth**
   - Multiple security layers (firewall, IDS, authentication)

════════════════════════════════════════════════════════════════════════════

🛡️ **FOUNDATIONAL REQUIREMENTS (FR)**
─────────────────────────────────────────────────────────────────────────

**62443-3-3 defines 7 Foundational Requirements:**

**FR 1: Identification & Authentication Control (IAC)**

.. code-block:: python

   # FR 1.1: Unique identification & authentication
   class IndustrialUserAuth:
       def __init__(self):
           self.users = {}
           self.failed_attempts = {}
       
       def authenticate(self, username, password, security_level):
           """IEC 62443 authentication requirements"""
           # FR 1.1 (RE 1): User identification
           if username not in self.users:
               self.log_event("Unknown user", username)
               return False
           
           # FR 1.2 (RE 1): Password complexity (SL 1+)
           if security_level >= 1:
               if len(password) < 8:
                   return False
           
           # FR 1.5 (RE 2): Multi-factor authentication (SL 3+)
           if security_level >= 3:
               if not self.verify_second_factor(username):
                   return False
           
           # FR 1.7 (RE 1): Account lockout after failed attempts
           if self.failed_attempts.get(username, 0) >= 3:
               self.log_event("Account locked", username)
               return False
           
           # Verify password
           if not self.verify_password(username, password):
               self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
               return False
           
           # Success
           self.failed_attempts[username] = 0
           self.log_event("Login successful", username)
           return True

**FR 2: Use Control (UC)**

.. code-block:: c

   // FR 2.1: Role-based access control (RBAC)
   typedef enum {
       ROLE_OPERATOR,      // Read-only access to HMI
       ROLE_ENGINEER,      // Read/write configuration
       ROLE_ADMINISTRATOR  // Full system access
   } UserRole;
   
   typedef struct {
       char username[32];
       UserRole role;
       uint32_t permissions;
   } User;
   
   // FR 2.1 (RE 1): Authorization enforcement
   bool check_permission(User *user, const char *resource, const char *action) {
       // SL 1+: Basic RBAC
       if (user->role == ROLE_OPERATOR && strcmp(action, "write") == 0) {
           log_security_event("Unauthorized write attempt", user->username);
           return false;  // Operators cannot modify configuration
       }
       
       // FR 2.4 (RE 1): Least privilege
       if (user->role == ROLE_ENGINEER) {
           // Engineers can only modify their assigned equipment
           if (!is_assigned_equipment(user->username, resource)) {
               log_security_event("Out-of-scope access attempt", user->username);
               return false;
           }
       }
       
       return true;
   }

**FR 3: System Integrity (SI)**

.. code-block:: c

   // FR 3.3: Software/firmware integrity verification
   bool verify_plc_firmware_integrity(const char *firmware_path) {
       // FR 3.3 (RE 1): Digital signature verification (SL 2+)
       if (!verify_ecdsa_signature(firmware_path)) {
           log_security_event("Firmware signature invalid");
           return false;
       }
       
       // FR 3.4 (RE 1): Detect malicious code
       if (scan_for_malware(firmware_path)) {
           log_security_event("Malware detected in firmware");
           return false;
       }
       
       // FR 3.9 (RE 1): Secure boot (SL 3+)
       if (security_level >= 3) {
           if (!verify_secure_boot_chain()) {
               log_critical("Secure boot chain broken");
               return false;
           }
       }
       
       return true;
   }

**FR 4: Data Confidentiality (DC)**

.. code-block:: c

   // FR 4.1: Encrypted communication (SL 2+)
   bool establish_secure_connection(const char *remote_host) {
       // FR 4.1 (RE 2): TLS 1.2+ for network communication
       tls_context_t ctx;
       
       if (!tls_init(&ctx, TLS_VERSION_1_2)) {
           return false;
       }
       
       // FR 4.1 (RE 3): Strong cipher suites (SL 3+)
       if (security_level >= 3) {
           // Only allow ECDHE, no RSA key exchange
           tls_set_ciphersuites(&ctx, "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384");
       }
       
       if (!tls_connect(&ctx, remote_host)) {
           log_security_event("TLS handshake failed", remote_host);
           return false;
       }
       
       return true;
   }

**FR 5: Restricted Data Flow (RDF)**

.. code-block:: python

   # FR 5.1: Network segmentation (zones/conduits)
   class ZoneFirewall:
       def __init__(self, source_zone, dest_zone):
           self.source_zone = source_zone
           self.dest_zone = dest_zone
           self.rules = []  # Whitelist
       
       def allow_traffic(self, src_ip, dst_ip, dst_port, protocol):
           """FR 5.1 (RE 1): Default deny, explicit allow"""
           for rule in self.rules:
               if (rule['src_ip'] == src_ip and
                   rule['dst_ip'] == dst_ip and
                   rule['dst_port'] == dst_port):
                   return True
           
           # Default deny
           self.log_blocked_traffic(src_ip, dst_ip, dst_port)
           return False

**FR 6: Timely Response to Events (TRE)**

.. code-block:: python

   # FR 6.1: Audit logging
   class IECAuditLogger:
       def log_event(self, event_type, user, resource, result):
           """FR 6.1 (RE 1): Comprehensive audit logging"""
           log_entry = {
               'timestamp': datetime.utcnow().isoformat(),
               'event_type': event_type,
               'user': user,
               'resource': resource,
               'result': result,
               'source_ip': get_source_ip()
           }
           
           # FR 6.1 (RE 2): Tamper-resistant storage (SL 2+)
           write_to_secure_log(log_entry)
           
           # FR 6.2 (RE 1): Real-time alerting for critical events
           if event_type in ['UNAUTHORIZED_ACCESS', 'FIRMWARE_MODIFY']:
               send_alert_to_soc(log_entry)

**FR 7: Resource Availability (RA)**

.. code-block:: c

   // FR 7.3: DoS protection
   void protect_against_dos(const char *src_ip) {
       // FR 7.3 (RE 1): Rate limiting
       uint32_t request_count = get_request_count(src_ip, 60);  // Last 60 seconds
       
       if (request_count > MAX_REQUESTS_PER_MINUTE) {
           log_security_event("Rate limit exceeded", src_ip);
           block_ip_temporary(src_ip, 300);  // Block for 5 minutes
           return;
       }
       
       // FR 7.8 (RE 1): Backup & restore
       if (time_for_backup()) {
           backup_plc_configuration();
       }
   }

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Explain the difference between SL-T, SL-C, and SL-A.**

**A1:**

**SL-T (Target):** What security level you **want** (risk-driven)
**SL-C (Capability):** What security level product **can provide** (design-driven)
**SL-A (Achieved):** What security level you **actually get** (deployment reality)

**Example:**

```
Manufacturing Plant Process Control Zone:
- Risk assessment determines: SL-T = SL 3
- PLC vendor claims: SL-C = SL 2 (62443-4-2 certified)
- Issue: SL-C < SL-T (gap!)
  
Options:
1. Accept residual risk (document & justify)
2. Add compensating controls (firewall, IDS)
3. Replace PLC with SL 3 capable model

After deployment:
- Independent audit: SL-A = SL 2
- Gap analysis: SL-T (3) vs. SL-A (2) = 1 level gap
- Mitigation: Network segmentation + IDS (increases SL-A to 3)
```

**Q2: How do zones and conduits implement defense-in-depth?**

**A2:**

**Zones:** Group assets by security requirements
**Conduits:** Control inter-zone communication

**Defense-in-Depth Layers:**

```
Layer 1: Zone boundary (firewall)
├─ Default deny all traffic
├─ Whitelist only required protocols/ports
└─ Stateful inspection

Layer 2: Conduit security (IDS/IPS)
├─ Deep packet inspection
├─ Protocol validation (Modbus, OPC UA)
└─ Anomaly detection

Layer 3: Zone internal security
├─ VLAN segmentation
├─ Switch port security
└─ MAC address filtering

Layer 4: Asset-level security
├─ Host-based firewall
├─ Application whitelisting
└─ Secure boot
```

**Example:** Attacker compromises HMI in Zone 1
→ Firewall blocks access to Zone 3 (PLC network)
→ IDS detects unusual traffic pattern
→ Network segmentation limits lateral movement

**Q3: What are the 7 Foundational Requirements in IEC 62443-3-3?**

**A3:**

| FR | Name | Key Requirement |
|:---|:-----|:----------------|
| **FR 1** | Identification & Authentication Control | User authentication, MFA (SL 3+) |
| **FR 2** | Use Control | RBAC, least privilege |
| **FR 3** | System Integrity | Secure boot, firmware signing |
| **FR 4** | Data Confidentiality | Encryption (TLS), key management |
| **FR 5** | Restricted Data Flow | Network segmentation, firewalls |
| **FR 6** | Timely Response to Events | Audit logging, SIEM integration |
| **FR 7** | Resource Availability | DoS protection, backup/restore |

**Each FR has multiple Requirements (RE) at different Enhancement Levels (RE 1-3).**

**Q4: How does IEC 62443 apply to OT/IT convergence?**

**A4:**

**Challenge:** Traditional OT (operational technology) networks isolated, now connecting to IT networks.

**IEC 62443 Solution:**

**Purdue Model Alignment:**
```
IT Domain (Level 4-5)
├─ ERP, business applications
└─ Security: Traditional IT security (firewalls, antivirus)

DMZ (Level 3.5)
├─ Data historian, HMI servers
└─ Security: Demilitarized zone (62443-3-2 conduit)

OT Domain (Level 0-3)
├─ SCADA, PLCs, field devices
└─ Security: Industrial-specific (62443-4-2 components)
```

**Key Principles:**
1. **Zones & Conduits:** Separate IT and OT into different zones
2. **Unidirectional Gateways:** IT can read OT data, but cannot write (prevent ransomware spread)
3. **Protocol Inspection:** Deep packet inspection for industrial protocols (Modbus, OPC UA)
4. **Compensating Controls:** Legacy OT devices lack security → network-level protection

**Q5: What is the relationship between IEC 62443 and NIST Cybersecurity Framework?**

**A5:**

**NIST CSF:** High-level risk management framework (5 functions: Identify, Protect, Detect, Respond, Recover)
**IEC 62443:** Detailed technical requirements for industrial systems

**Complementary:**

| NIST CSF Function | IEC 62443 Mapping |
|:------------------|:------------------|
| **Identify** | 62443-2-1 (Risk assessment), 62443-3-2 (Zone definition) |
| **Protect** | 62443-3-3 (System security requirements), 62443-4-2 (Component requirements) |
| **Detect** | FR 6 (Timely Response to Events - logging, monitoring) |
| **Respond** | 62443-2-1 (Incident response procedures) |
| **Recover** | FR 7 (Resource Availability - backup/restore) |

**Usage:** NIST CSF for **organizational strategy**, IEC 62443 for **technical implementation**.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~900
