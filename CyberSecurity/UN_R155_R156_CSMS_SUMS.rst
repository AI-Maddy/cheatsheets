🚦 **UNECE R155 & R156 — AUTOMOTIVE CYBERSECURITY REGULATIONS**
═══════════════════════════════════════════════════════════════════════

**UN Regulations for Vehicle Type Approval: Cybersecurity (R155) & Software Updates (R156)**  
**Purpose:** Mandatory compliance 📋 | Type approval 🚗 | Market access 🌍  
**Effective:** July 2022 (new vehicles), July 2024 (all vehicles)

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**UN R155 (Cybersecurity) & R156 (Software Updates)** are **mandatory type approval regulations** for vehicles sold in **EU, Japan, Korea, and 60+ countries**.

**Key requirements:**
- **R155:** Cybersecurity Management System (CSMS), risk assessment, vulnerability management
- **R156:** Secure software update process, version tracking, rollback protection

**Non-compliance = Cannot obtain type approval = Cannot sell vehicles**

**Implementation:** ISO 21434 provides technical guidance to meet R155/R156 requirements.

════════════════════════════════════════════════════════════════════════════

📋 **UN R155 — CYBERSECURITY MANAGEMENT SYSTEM (CSMS)**
─────────────────────────────────────────────────────────────────────────

**Regulation Overview:**

| Aspect | Details |
|:-------|:--------|
| **Full Name** | UN Regulation No. 155 — Uniform provisions concerning the approval of vehicles with regards to cyber security and cyber security management system |
| **Adopted** | June 2020 (WP.29) |
| **Effective** | July 2022 (new vehicle types), July 2024 (all new vehicles) |
| **Scope** | M, N, O category vehicles (passenger cars, trucks, trailers) |
| **Authority** | UNECE WP.29 (World Forum for Harmonization of Vehicle Regulations) |
| **Enforced by** | National type approval authorities (KBA Germany, JARI Japan, etc.) |

**R155 Requirements (Annex 5):**

**Part A: Organizational (CSMS)**

1. **Cybersecurity Governance**
   - Management responsibility & oversight
   - Cybersecurity policy documented
   - Resources allocated (budget, personnel)

2. **Risk Assessment Process**
   - Systematic threat analysis (per vehicle model)
   - Vulnerability identification
   - Risk mitigation strategies

3. **Verification & Validation**
   - Security testing (penetration testing, vulnerability scanning)
   - Independent assessment (optional but recommended)

4. **Cybersecurity Monitoring**
   - Vulnerability monitoring (CVE databases, threat intelligence)
   - Field incident detection & response
   - Continuous improvement

5. **Supplier Management**
   - Security requirements in supplier contracts
   - Component security assessment
   - Supply chain risk management

**Part B: Vehicle Type (Product-Specific)**

**Vehicle Type Approval Requirements:**

.. code-block:: text

   Mitigations for Key Threat Categories:
   
   1. Back-end Server Attacks
      ├─ Secure server infrastructure
      ├─ Regular security updates
      └─ Access control & authentication
   
   2. Update Procedures
      ├─ Authenticity verification (digital signatures)
      ├─ Integrity checks (hash verification)
      └─ Secure delivery (TLS, encrypted channels)
   
   3. Vehicle Communication Channels
      ├─ CAN bus: Authentication (AUTOSAR SecOC)
      ├─ Ethernet: Firewall, VLANs, IDS
      ├─ Wireless: WPA3, certificate-based auth
      └─ OBD-II: Access control, audit logging
   
   4. Data/Code
      ├─ Secure boot (verify code integrity)
      ├─ Memory protection (MPU, ASLR)
      └─ Code signing (all executable code)
   
   5. External Connectivity & Interfaces
      ├─ Telematics: Mutual TLS authentication
      ├─ Wi-Fi/Bluetooth: Strong encryption
      ├─ USB: Disable autorun, whitelist devices
      └─ Diagnostic ports: Rate limiting, authentication

**R155 Audit Process:**

.. code-block:: python

   class R155Audit:
       def __init__(self, oem_name, vehicle_model):
           self.oem = oem_name
           self.vehicle = vehicle_model
           self.findings = []
       
       def audit_csms(self):
           """Part A: Organizational CSMS Audit"""
           checklist = {
               'Management Commitment': [
                   'Cybersecurity policy signed by CEO/CTO',
                   'Annual cybersecurity budget allocated',
                   'Executive cybersecurity officer appointed'
               ],
               'Risk Assessment': [
                   'TARA performed for vehicle model',
                   'Threat scenarios documented (STRIDE)',
                   'Risk mitigation plan approved'
               ],
               'Testing & Validation': [
                   'Penetration testing report available',
                   'Vulnerability scanning performed',
                   'Independent security assessment (optional)'
               ],
               'Monitoring': [
                   'Vulnerability monitoring process established',
                   'PSIRT (Product Security Incident Response Team) operational',
                   'Incident response plan documented & tested'
               ],
               'Supplier Management': [
                   'Security requirements in supplier contracts',
                   'Supplier security assessments conducted',
                   'Component SBOM (Software Bill of Materials) provided'
               ]
           }
           
           for category, items in checklist.items():
               for item in items:
                   # Auditor verification logic
                   if not self.verify_evidence(item):
                       self.findings.append({
                           'category': category,
                           'item': item,
                           'severity': 'Major',
                           'status': 'Non-Conformance'
                       })
       
       def audit_vehicle_type(self):
           """Part B: Vehicle-Specific Requirements"""
           threat_categories = [
               'Back-end server attacks',
               'Update procedures',
               'Vehicle communication channels',
               'Data/Code integrity',
               'External connectivity'
           ]
           
           for threat in threat_categories:
               mitigations = self.get_mitigations(threat)
               if not mitigations:
                   self.findings.append({
                       'threat': threat,
                       'severity': 'Critical',
                       'status': 'Missing Mitigation'
                   })
       
       def generate_certificate(self):
           """Issue R155 type approval certificate"""
           if len(self.findings) == 0:
               return {
                   'status': 'APPROVED',
                   'certificate_number': f'R155-{self.oem}-{self.vehicle}-2026',
                   'valid_until': '2031-01-14',
                   'remarks': 'All requirements met'
               }
           else:
               return {
                   'status': 'REJECTED',
                   'findings': self.findings,
                   'action_required': 'Address all findings and resubmit'
               }
   
   # Example audit
   audit = R155Audit(oem_name='ACME Motors', vehicle_model='EV-2026')
   audit.audit_csms()
   audit.audit_vehicle_type()
   result = audit.generate_certificate()
   
   print(f"Type Approval Status: {result['status']}")

════════════════════════════════════════════════════════════════════════════

📦 **UN R156 — SOFTWARE UPDATE MANAGEMENT SYSTEM (SUMS)**
─────────────────────────────────────────────────────────────────────────

**Regulation Overview:**

| Aspect | Details |
|:-------|:--------|
| **Full Name** | UN Regulation No. 156 — Software update and software update management system |
| **Adopted** | June 2020 (WP.29) |
| **Effective** | July 2022 (new vehicle types), January 2023 (all new vehicles) |
| **Scope** | All software updates (OTA and workshop-based) |

**R156 Requirements (Annex 5):**

**1. Software Update Management System (SUMS)**

.. code-block:: text

   SUMS Components:
   
   ┌─────────────────────────────────────────────────────┐
   │ A. Software Identification                          │
   │    ├─ Unique software version numbering             │
   │    ├─ SBOM (Software Bill of Materials)             │
   │    └─ Version tracking database                     │
   └─────────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────────┐
   │ B. Security & Authenticity                          │
   │    ├─ Digital signatures (ECDSA, RSA)               │
   │    ├─ Secure delivery channels (TLS 1.3)            │
   │    └─ Integrity verification (SHA-256)              │
   └─────────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────────┐
   │ C. Installation & Verification                      │
   │    ├─ Pre-installation checks (compatibility)       │
   │    ├─ Secure installation process                   │
   │    ├─ Post-installation verification (BITE)         │
   │    └─ Rollback capability (fail-safe)               │
   └─────────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────────┐
   │ D. Update Records & Traceability                    │
   │    ├─ What: Software component, version             │
   │    ├─ When: Timestamp (UTC)                         │
   │    ├─ Where: VIN, ECU identifier                    │
   │    └─ Result: Success/Failure with reason           │
   └─────────────────────────────────────────────────────┘

**2. Update Procedures (Annex 6)**

**OTA (Over-the-Air) Update Flow:**

.. code-block:: c

   typedef struct {
       char vin[17];
       char software_id[32];  // e.g., "ECM-Firmware-2.5.3"
       char version_old[16];
       char version_new[16];
       time_t timestamp;
       enum {SUCCESS, FAILED_SIGNATURE, FAILED_INSTALL, ROLLED_BACK} result;
       char reason[256];
   } R156_UpdateRecord;
   
   // R156-compliant update procedure
   bool perform_r156_update(const char *vin, const uint8_t *update_pkg, size_t pkg_size) {
       R156_UpdateRecord record = {0};
       strncpy(record.vin, vin, 17);
       record.timestamp = time(NULL);
       
       // Step 1: Verify digital signature (R156 requirement)
       if (!verify_signature_ecdsa(update_pkg, pkg_size)) {
           record.result = FAILED_SIGNATURE;
           strcpy(record.reason, "Digital signature verification failed");
           log_r156_update(&record);
           return false;
       }
       
       // Step 2: Extract metadata
       SoftwareMetadata metadata;
       extract_metadata(update_pkg, &metadata);
       strncpy(record.software_id, metadata.component_id, 32);
       strncpy(record.version_new, metadata.version, 16);
       
       // Step 3: Check compatibility
       if (!check_compatibility(metadata)) {
           record.result = FAILED_INSTALL;
           strcpy(record.reason, "Incompatible with current vehicle configuration");
           log_r156_update(&record);
           return false;
       }
       
       // Step 4: Install update
       if (!install_software(update_pkg, pkg_size)) {
           record.result = FAILED_INSTALL;
           strcpy(record.reason, "Installation failed - hardware error");
           log_r156_update(&record);
           return false;
       }
       
       // Step 5: Post-installation verification
       if (!verify_installation()) {
           // Automatic rollback (R156 requirement)
           rollback_to_previous_version();
           record.result = ROLLED_BACK;
           strcpy(record.reason, "Post-installation verification failed");
           log_r156_update(&record);
           return false;
       }
       
       // Success!
       record.result = SUCCESS;
       strcpy(record.reason, "Update completed successfully");
       log_r156_update(&record);
       
       // Notify OEM server (R156 requirement)
       notify_update_success(vin, metadata.version);
       
       return true;
   }
   
   // R156-mandated audit logging
   void log_r156_update(const R156_UpdateRecord *record) {
       // Store in tamper-resistant log (EEPROM or backend server)
       // Must be retained for vehicle lifetime + 10 years (R156 requirement)
       
       char log_entry[512];
       snprintf(log_entry, sizeof(log_entry),
                "[%ld] VIN:%s | SW:%s | %s -> %s | Result:%d | Reason:%s",
                record->timestamp,
                record->vin,
                record->software_id,
                record->version_old,
                record->version_new,
                record->result,
                record->reason);
       
       append_to_audit_log(log_entry);
       send_to_backend_server(log_entry);  // Redundant storage
   }

**3. Workshop-Based Updates**

.. code-block:: python

   class WorkshopUpdateProcess:
       def __init__(self, workshop_id, technician_id):
           self.workshop_id = workshop_id
           self.technician_id = technician_id
       
       def perform_workshop_update(self, vin, update_file):
           """R156-compliant workshop update procedure"""
           # R156 requires same security as OTA
           
           # 1. Authenticate technician
           if not self.authenticate_technician():
               return {'status': 'FAILED', 'reason': 'Technician authentication failed'}
           
           # 2. Verify update authenticity
           if not verify_signature(update_file):
               return {'status': 'FAILED', 'reason': 'Update signature invalid'}
           
           # 3. Check workshop authorization (OEM-approved dealer)
           if not self.check_workshop_authorization():
               return {'status': 'FAILED', 'reason': 'Workshop not authorized'}
           
           # 4. Load update to vehicle
           result = load_update_via_obd(vin, update_file)
           
           # 5. Log update (same as OTA logging)
           log_entry = {
               'vin': vin,
               'workshop_id': self.workshop_id,
               'technician_id': self.technician_id,
               'timestamp': datetime.now().isoformat(),
               'result': result
           }
           log_r156_update(log_entry)
           
           return result

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: What is the difference between UN R155 and ISO 21434?**

**A1:**

| Aspect | UN R155 | ISO 21434 |
|:-------|:--------|:----------|
| **Type** | **Regulation** (legal requirement) | **Standard** (voluntary guidance) |
| **Enforced by** | National type approval authorities | Not enforced (industry best practice) |
| **Scope** | Type approval (market access) | Full product lifecycle (concept to decommissioning) |
| **Detail level** | High-level requirements | Detailed technical guidance |
| **Compliance** | Mandatory (cannot sell without) | Voluntary (but enables R155 compliance) |
| **Audit** | Government auditors | Internal or third-party auditors |

**Relationship:** ISO 21434 provides the **"how"** to meet R155 **"what"** requirements.

**Example:**
- **R155 requirement:** "Manufacturer shall have risk assessment process"
- **ISO 21434 guidance:** "Use TARA methodology (Clause 8) with STRIDE, attack feasibility rating, etc."

**Q2: How does R156 ensure update authenticity?**

**A2:**

**R156 Authenticity Requirements (Annex 5, Section B):**

1. **Digital Signatures:**
```c
// Update package signed by OEM private key
UpdatePackage {
    metadata: {version, target_ecu, timestamp},
    payload: encrypted_software_binary,
    signature: ECDSA_P384(hash(metadata + payload))
}
```

2. **Verification Before Installation:**
```c
// Vehicle verifies signature with OEM public key (stored in secure flash)
if (!ecdsa_verify(update.signature, oem_public_key)) {
    reject_update();
    log_event("Update authenticity check failed");
}
```

3. **Secure Delivery:**
- TLS 1.3 for OTA (encrypted, authenticated channel)
- USB/SD card: Signature still required (prevent malicious media)

4. **Certificate Chain:**
```
OEM Root CA → Intermediate CA → Update Signing Key
```

**Result:** Only OEM can produce valid updates (attacker cannot forge signature without private key).

**Q3: What happens if a vehicle fails R155 type approval?**

**A3:**

**Consequences:**

**Immediate:**
- **Type approval denied** (vehicle model cannot be sold)
- OEM receives non-conformance report with findings
- Must remediate all findings and re-submit

**Remediation Examples:**

| Finding | Remediation | Timeline |
|:--------|:------------|:---------|
| "No CSMS documented" | Create CSMS manual, appoint cybersecurity officer | 3-6 months |
| "No penetration testing performed" | Commission third-party pentest, fix vulnerabilities | 2-4 months |
| "CAN bus has no authentication" | Implement AUTOSAR SecOC, re-validate | 6-12 months |
| "No vulnerability monitoring" | Establish PSIRT, integrate threat intelligence feeds | 1-3 months |

**After Remediation:**
- Re-submit to type approval authority
- Additional audit (focus on previous findings)
- If successful → issue R155 certificate

**Cost:** Failed type approval can delay vehicle launch by 6-12 months, costing $10M-$100M (lost sales, engineering rework).

**Q4: How does R156 require rollback protection?**

**A4:**

**R156 Annex 5, Part C: Installation & Verification**

**Requirement:** "The update procedure shall prevent the installation of software that is older than the current version (rollback attacks)."

**Implementation:**

**Method 1: Version Monotonicity**
```c
// Store current version in tamper-resistant memory
uint32_t current_version = read_secure_version_register();

if (update_version <= current_version) {
    log_security_event(ROLLBACK_ATTEMPT);
    return false;  // Reject update
}
```

**Method 2: Secure Counter (OTP Fuses)**
```c
// One-Time Programmable fuses (can only increment, never decrement)
// Burn fuse for each major version
if (update_major_version <= read_otp_fuse()) {
    return false;  // Hardware-enforced rollback protection
}
```

**Method 3: Timestamp Validation**
```c
// Reject updates older than 90 days (prevents replay of old signed updates)
time_t update_timestamp = extract_timestamp(update_pkg);
time_t now = get_system_time();

if (now - update_timestamp > 90 * 86400) {
    log_event("Update too old - potential replay attack");
    return false;
}
```

**R156 Audit Check:** Auditor will attempt to install old firmware version and verify rejection.

**Q5: What are the penalties for R155/R156 non-compliance after type approval?**

**A5:**

**Post-Approval Non-Compliance Scenarios:**

**Scenario 1: Vulnerability Discovered, OEM Fails to Patch**
- **R155 requirement:** Continuous monitoring + timely remediation
- **Penalty:** Type approval can be **withdrawn** by national authority
- **Example:** If critical vulnerability remains unpatched >180 days

**Scenario 2: OEM Updates Vehicle Without R156 Compliance**
- **R156 requirement:** All updates must follow SUMS process (logging, verification)
- **Penalty:** Individual vehicle recalls, fines up to €30K per vehicle (EU)

**Scenario 3: Security Incident Not Reported**
- **R155 requirement:** Report cybersecurity incidents to authority within reasonable time
- **Penalty:** Administrative fines, reputational damage

**Real-World Example (Hypothetical):**
```
2025: OEM discovers vulnerability in gateway ECU (affects 500K vehicles)
- Day 0: Vulnerability discovered
- Day 30: OEM must notify type approval authority (R155)
- Day 90: Patch must be available (R156)
- Day 180: All vehicles patched via OTA or recall

If Day 180 deadline missed:
→ Type approval authority investigation
→ Potential type approval suspension
→ Mandatory recall at OEM expense
→ Fines: €5M-€50M (depending on severity)
```

**Key takeaway:** R155/R156 compliance is **continuous**, not one-time. Ongoing obligations for vehicle lifetime.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
