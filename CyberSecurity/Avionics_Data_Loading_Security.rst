💾 **AVIONICS DATA LOADING SECURITY**
═══════════════════════════════════════════════════════════════════════

**ARINC 615A & Secure Software Management for Aircraft Systems**  
**Purpose:** Secure software loading 🔒 | ARINC 615/615A standards 📋 | Supply chain integrity 🏭  
**Standards:** ARINC 615A, DO-326A, DO-178C

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Avionics Data Loading** = transferring software/configuration data to Line Replaceable Units (LRUs) on aircraft.

**ARINC 615A** defines standardized, secure loading procedures using **digital signatures** and **dual-person integrity**.

**Key Threats:** Malicious software, unauthorized modifications, supply chain compromise.

**Mitigation:** ECDSA signature verification, CRC integrity checks, two-person authorization, audit logging.

════════════════════════════════════════════════════════════════════════════

📋 **ARINC 615/615A STANDARDS**
─────────────────────────────────────────────────────────────────────────

**ARINC 615 (Original):**
- Published 1995
- Standardized data loading procedures (file transfer protocol)
- **No security features** (no authentication, integrity checks optional)
- Used UDP or proprietary protocols
- **Obsolete** for security-critical systems

**ARINC 615A (Secure):**
- Published 2005 (updated 2014)
- Adds **cryptographic security**:
  - Digital signatures (RSA-2048 or ECDSA-P256/P384)
  - CRC32/SHA-256 integrity checks
  - Dual-person authorization requirements
  - Secure audit logging
- Mandatory for **SAL 2+ systems** (DO-326A)

**Comparison:**

| Feature | ARINC 615 | ARINC 615A |
|:--------|:----------|:-----------|
| **Authentication** | ❌ None | ✅ Digital signatures |
| **Integrity** | ⚠️ Optional CRC | ✅ Mandatory SHA-256 |
| **Authorization** | ❌ Single person | ✅ Dual-person required |
| **Audit logging** | ⚠️ Basic | ✅ Comprehensive |
| **Supply chain security** | ❌ No | ✅ Certificate chain |
| **Rollback protection** | ❌ No | ✅ Version checks |
| **Use case** | Legacy aircraft | Modern aircraft (SAL 2+) |

════════════════════════════════════════════════════════════════════════════

🏭 **AVIONICS SOFTWARE SUPPLY CHAIN**
─────────────────────────────────────────────────────────────────────────

**Software Lifecycle:**

.. code-block:: text

   ┌────────────────────────────────────────────────────────────────┐
   │ 1. OEM Development (Boeing, Airbus, Honeywell, Collins)      │
   │    ├─ Source code (DO-178C certified)                         │
   │    ├─ Build & test (compiler, linker, CI/CD)                  │
   │    └─ Code signing (ECDSA private key in HSM)                 │
   └────────────────┬───────────────────────────────────────────────┘
                    │ Signed binary (.lsf file)
                    ▼
   ┌────────────────────────────────────────────────────────────────┐
   │ 2. OEM Distribution (secure portal)                           │
   │    ├─ Upload to airline portal (HTTPS, multi-factor auth)     │
   │    ├─ Release notes, certification documents                  │
   │    └─ Signature verification instructions                     │
   └────────────────┬───────────────────────────────────────────────┘
                    │ Download by airline
                    ▼
   ┌────────────────────────────────────────────────────────────────┐
   │ 3. Airline Verification (maintenance base)                    │
   │    ├─ Verify ECDSA signature with OEM public key              │
   │    ├─ Check SHA-256 hash against release manifest             │
   │    ├─ Dual-person approval (mechanic + inspector)             │
   │    └─ Copy to portable media (USB, SD card)                   │
   └────────────────┬───────────────────────────────────────────────┘
                    │ Portable media to aircraft
                    ▼
   ┌────────────────────────────────────────────────────────────────┐
   │ 4. Aircraft Loading (maintenance mode)                        │
   │    ├─ Mechanic connects laptop to ARINC 615A port             │
   │    ├─ LRU verifies signature (reject if invalid)              │
   │    ├─ CRC verification during transfer                        │
   │    ├─ Dual-person confirmation (PIN entry)                    │
   │    ├─ BITE (Built-In Test Equipment) post-load tests          │
   │    └─ Audit log entry (who, what, when)                       │
   └────────────────────────────────────────────────────────────────┘

**Supply Chain Attack Risks:**

| Attack Vector | Description | ARINC 615A Mitigation |
|:--------------|:------------|:----------------------|
| **Compromised OEM** | Attacker infiltrates OEM, inserts backdoor | Certificate revocation, code review |
| **Man-in-the-middle** | Attacker intercepts download, replaces binary | HTTPS + signature verification |
| **Malicious insider** | Airline employee loads unauthorized software | Dual-person authorization, audit logs |
| **Portable media** | USB drive with malware | USB whitelisting, signature checks |
| **Maintenance laptop** | Infected laptop propagates malware | Laptop hardening, offline verification |

════════════════════════════════════════════════════════════════════════════

🔐 **CRYPTOGRAPHIC SECURITY MECHANISMS**
─────────────────────────────────────────────────────────────────────────

**Digital Signatures:**

.. code-block:: c

   // ARINC 615A signature verification (ECDSA-P384)
   #include <openssl/ecdsa.h>
   #include <openssl/sha.h>
   
   bool verify_load_file_signature(const char *file_path, const char *sig_file) {
       uint8_t file_hash[48];  // SHA-384
       uint8_t signature[96];  // ECDSA-P384 (r, s)
       EC_KEY *oem_public_key;
       
       // 1. Calculate SHA-384 hash of loadable file
       FILE *f = fopen(file_path, "rb");
       SHA384_CTX ctx;
       SHA384_Init(&ctx);
       
       uint8_t buffer[4096];
       size_t bytes_read;
       while ((bytes_read = fread(buffer, 1, sizeof(buffer), f)) > 0) {
           SHA384_Update(&ctx, buffer, bytes_read);
       }
       SHA384_Final(file_hash, &ctx);
       fclose(f);
       
       // 2. Read signature from .sig file
       read_signature_file(sig_file, signature, sizeof(signature));
       
       // 3. Load OEM public key from certificate store
       oem_public_key = load_oem_certificate("honeywell_fms");
       if (!oem_public_key) {
           log_error("OEM certificate not found");
           return false;
       }
       
       // 4. Verify ECDSA signature
       int result = ECDSA_verify(
           0,                    // type (ignored)
           file_hash, 48,        // hash
           signature, 96,        // signature
           oem_public_key        // public key
       );
       
       EC_KEY_free(oem_public_key);
       
       if (result != 1) {
           log_security_event(LOAD_SIG_FAIL, file_path);
           display_error("SOFTWARE SIGNATURE INVALID - LOADING ABORTED");
           return false;
       }
       
       return true;
   }

**Certificate Chain Validation:**

.. code-block:: text

   Root CA (Aircraft Manufacturer)
   ├─ Boeing Root Certificate Authority
   │  └─ [Stored in aircraft secure storage]
   │
   ├─ Intermediate CA (Avionics OEM)
   │  ├─ Honeywell Avionics Signing Key
   │  ├─ Collins Aerospace Signing Key
   │  └─ Thales Avionics Signing Key
   │     └─ [Certificates signed by Boeing Root CA]
   │
   └─ End-Entity Certificate (Specific LRU)
      ├─ FMS Software Signing Key v3.2
      └─ [Signs actual loadable software files]

**Integrity Checks:**

.. code-block:: c

   // Multi-layer integrity verification
   typedef struct {
       char magic[4];            // "ARINC615A"
       uint32_t version;         // File format version
       uint32_t file_size;       // Total size (bytes)
       uint32_t crc32;           // CRC-32 checksum
       uint8_t sha256[32];       // SHA-256 hash
       uint8_t signature[96];    // ECDSA-P384 signature
       char part_number[32];     // LRU part number
       char software_version[16];// Software version
   } LoadFileHeader;
   
   bool verify_load_file_integrity(const char *path) {
       LoadFileHeader header;
       
       // 1. Read header
       read_file_header(path, &header);
       
       // 2. Verify magic number
       if (memcmp(header.magic, "ARINC615A", 9) != 0) {
           return false;
       }
       
       // 3. Calculate CRC32 of data portion
       uint32_t calculated_crc = calculate_crc32_file(path, sizeof(header));
       if (calculated_crc != header.crc32) {
           log_error("CRC mismatch");
           return false;
       }
       
       // 4. Calculate SHA-256 of entire file
       uint8_t calculated_sha[32];
       calculate_sha256_file(path, calculated_sha);
       if (memcmp(calculated_sha, header.sha256, 32) != 0) {
           log_error("SHA-256 mismatch");
           return false;
       }
       
       // 5. Verify ECDSA signature (as in previous example)
       if (!verify_ecdsa_signature(path, header.signature)) {
           return false;
       }
       
       return true;  // All checks passed
   }

════════════════════════════════════════════════════════════════════════════

👥 **DUAL-PERSON AUTHORIZATION**
─────────────────────────────────────────────────────────────────────────

**Concept:** No single individual can load software alone. Requires:
1. **Mechanic** (initiates load)
2. **Inspector** (approves load)

**Implementation:**

.. code-block:: python

   # Dual-person authorization workflow
   class AircraftSoftwareLoader:
       def __init__(self):
           self.pending_loads = {}
           self.audit_log = []
       
       def initiate_load(self, mechanic_id, mechanic_pin, file_path, lru_id):
           """Step 1: Mechanic initiates load"""
           # Verify mechanic credentials
           if not self.verify_credentials(mechanic_id, mechanic_pin, role='MECHANIC'):
               return {'status': 'ERROR', 'message': 'Invalid credentials'}
           
           # Verify file signature
           if not verify_load_file_signature(file_path):
               return {'status': 'ERROR', 'message': 'Signature verification failed'}
           
           # Create pending load record
           load_id = generate_uuid()
           self.pending_loads[load_id] = {
               'mechanic_id': mechanic_id,
               'file_path': file_path,
               'lru_id': lru_id,
               'timestamp': datetime.now(),
               'status': 'PENDING_APPROVAL'
           }
           
           self.audit_log.append({
               'event': 'LOAD_INITIATED',
               'load_id': load_id,
               'mechanic': mechanic_id,
               'file': file_path,
               'timestamp': datetime.now()
           })
           
           return {
               'status': 'SUCCESS',
               'load_id': load_id,
               'message': 'Load initiated. Awaiting inspector approval.'
           }
       
       def approve_load(self, inspector_id, inspector_pin, load_id):
           """Step 2: Inspector approves load"""
           # Verify inspector credentials
           if not self.verify_credentials(inspector_id, inspector_pin, role='INSPECTOR'):
               return {'status': 'ERROR', 'message': 'Invalid credentials'}
           
           # Check pending load exists
           if load_id not in self.pending_loads:
               return {'status': 'ERROR', 'message': 'Load ID not found'}
           
           load = self.pending_loads[load_id]
           
           # Prevent same person approval (separation of duties)
           if inspector_id == load['mechanic_id']:
               return {'status': 'ERROR', 'message': 'Inspector cannot be same as mechanic'}
           
           # Perform final verification
           if not verify_load_file_signature(load['file_path']):
               return {'status': 'ERROR', 'message': 'Signature verification failed'}
           
           # Execute load
           result = execute_arinc615a_load(load['lru_id'], load['file_path'])
           
           self.audit_log.append({
               'event': 'LOAD_APPROVED',
               'load_id': load_id,
               'inspector': inspector_id,
               'result': result,
               'timestamp': datetime.now()
           })
           
           del self.pending_loads[load_id]
           return result

**Audit Logging:**

.. code-block:: text

   Example Audit Log Entry:
   
   [2026-01-14 08:15:32 UTC] LOAD_INITIATED
     Load ID:      a3f8b2d1-4e9a-4b3c-8f2e-1d9c7a5e4b6f
     Mechanic:     John Smith (ID: M-1234)
     File:         FMS_Software_v8.2.5.lsf
     LRU:          FMS-Left (SN: 98765)
     Signature:    VALID (Honeywell ECDSA-P384)
     
   [2026-01-14 08:18:45 UTC] LOAD_APPROVED
     Load ID:      a3f8b2d1-4e9a-4b3c-8f2e-1d9c7a5e4b6f
     Inspector:    Jane Doe (ID: I-5678)
     Approval:     Confirmed (PIN verified)
     Transfer:     4.2 MB in 87 seconds
     CRC:          PASS
     BITE Test:    PASS (all systems nominal)
     Result:       SUCCESS

════════════════════════════════════════════════════════════════════════════

🛡️ **SECURITY BEST PRACTICES**
─────────────────────────────────────────────────────────────────────────

**1. Version Control & Rollback Protection:**

.. code-block:: c

   // Prevent downgrade attacks
   bool check_software_version(const char *new_version, const char *current_version) {
       int new_major, new_minor, new_patch;
       int cur_major, cur_minor, cur_patch;
       
       sscanf(new_version, "%d.%d.%d", &new_major, &new_minor, &new_patch);
       sscanf(current_version, "%d.%d.%d", &cur_major, &cur_minor, &cur_patch);
       
       // Allow only newer versions (or explicit override by authorized personnel)
       if (new_major < cur_major ||
           (new_major == cur_major && new_minor < cur_minor) ||
           (new_major == cur_major && new_minor == cur_minor && new_patch < cur_patch)) {
           
           log_security_event(VERSION_DOWNGRADE_ATTEMPT, new_version);
           return false;  // Reject downgrade
       }
       
       return true;
   }

**2. Secure Storage of Cryptographic Keys:**

- **OEM private keys:** HSM (Hardware Security Module) at factory
- **Aircraft public keys:** Secure storage in LRU (tamper-resistant memory)
- **Certificate revocation list:** Updated monthly via secure channel

**3. Maintenance Laptop Hardening:**

- Dedicated laptop for avionics (no internet, no USB except during load)
- Full-disk encryption (BitLocker, LUKS)
- Antivirus with daily updates
- Air-gapped from airline network

**4. Portable Media Security:**

- Use only airline-approved USB drives (whitelisted by serial number)
- Format before each use (prevent cross-contamination)
- Virus scan on maintenance PC before load

**5. BITE Post-Load Testing:**

.. code-block:: text

   Mandatory BITE Tests After Software Load:
   
   ✅ Power-on self-test (POST)
   ✅ Memory integrity (CRC of loaded software)
   ✅ Interface checks (ARINC 429, AFDX)
   ✅ Sensor calibration (if applicable)
   ✅ Cross-channel comparison (redundant systems)
   ✅ Safe mode verification (fallback logic)
   
   If ANY test fails → rollback to previous version

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why is ARINC 615A required for SAL 2+ systems instead of ARINC 615?**

**A1:**
ARINC 615 (original) has **no cryptographic security**:
- No authentication (anyone can load software)
- Optional integrity checks (CRC may be skipped)
- No audit trail requirements

ARINC 615A adds **mandatory security**:
- Digital signatures (ECDSA-P256/P384 or RSA-2048)
- SHA-256 hash verification
- Dual-person authorization (mechanic + inspector)
- Comprehensive audit logging

**SAL 2+ systems** (e.g., flight-critical avionics) cannot tolerate risk of malicious software loading → ARINC 615A required per DO-326A.

**Q2: Describe the certificate chain for avionics software signing.**

**A2:**
```
Root CA (Aircraft Manufacturer)
├─ Self-signed certificate (Boeing/Airbus)
└─ Stored in aircraft secure storage (tamper-resistant)

Intermediate CA (Avionics OEM)
├─ Honeywell, Collins, Thales certificates
├─ Signed by Root CA
└─ Valid for 5-10 years

End-Entity Certificate (Software Release)
├─ FMS Software v8.2.5 signing key
├─ Signed by Intermediate CA
├─ Valid for 1-2 years
└─ Used to sign actual .lsf files
```

**Verification process:**
1. LRU verifies end-entity certificate using OEM intermediate certificate
2. LRU verifies intermediate certificate using root CA (stored in secure memory)
3. LRU verifies software signature using end-entity certificate
4. If any step fails → reject load

**Q3: What is dual-person authorization and why is it required?**

**A3:**
**Dual-person authorization:** Two separate individuals required for critical action.

**Implementation:**
- **Person 1 (Mechanic):** Initiates load, connects laptop, selects file
- **Person 2 (Inspector):** Reviews file details, enters PIN to approve

**Security benefits:**
- **Prevents insider threats** (single rogue employee cannot load malware)
- **Reduces errors** (second person reviews before approval)
- **Audit trail** (two identities recorded in log)

**ARINC 615A enforcement:**
- LRU requires two distinct PINs before starting load
- Same person cannot serve both roles (ID check)
- Timeout if approval not received within 15 minutes

**Real-world analogy:** Nuclear launch requires two officers with separate keys.

**Q4: How does ARINC 615A prevent rollback attacks?**

**A4:**
**Rollback attack:** Attacker installs older software version with known vulnerabilities.

**ARINC 615A mitigations:**

1. **Version monotonicity enforcement:**
```c
if (new_version < current_version) {
    reject_load();  // No downgrades allowed
}
```

2. **Certificate validity period:**
- Old software has expired certificate → signature verification fails

3. **Revocation lists:**
- Vulnerable versions added to revocation list
- LRU checks list before load

4. **Audit logging:**
- Downgrade attempts logged → security investigation

**Exception:** Authorized rollback with special override certificate (emergency only).

**Q5: What happens if BITE tests fail after software loading?**

**A5:**
**BITE (Built-In Test Equipment)** runs automatically after load completion.

**Test failures trigger:**

1. **Immediate actions:**
   - Abort activation of new software
   - Display error code to mechanic
   - Log failure in maintenance system

2. **Automatic rollback:**
```c
if (bite_test_failed()) {
    // Restore previous software version from backup
    restore_backup_image();
    
    // Verify backup integrity
    verify_backup_crc();
    
    // Re-run BITE on backup
    run_bite_tests();
}
```

3. **Notification:**
- Alert airline maintenance control
- Create maintenance log entry
- Contact OEM support if persistent failure

4. **Aircraft status:**
- Mark LRU as degraded (if redundant system available)
- Ground aircraft if critical system affected

**Safety principle:** Never leave aircraft with unverified software. Rollback ensures last-known-good state restored.

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~700
