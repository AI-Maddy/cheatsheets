🔐 **HARDWARE SECURITY MODULE (HSM)**
═══════════════════════════════════════════════════════════════════════

**Tamper-Resistant Cryptographic Key Storage & Processing**  
**Purpose:** Secure key management 🔑 | Cryptographic acceleration ⚡ | Tamper protection 🛡️  
**Standards:** FIPS 140-2/3, Common Criteria EAL4+, PCI HSM

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**HSM (Hardware Security Module)** = tamper-resistant hardware device for **secure cryptographic key storage** and **cryptographic operations**.

**Key principle:** Private keys **never leave HSM** in plaintext. All crypto operations (sign, decrypt, MAC) performed **inside HSM**.

**Use cases:** Certificate authorities, payment systems, code signing, automotive security (V2X keys), aerospace (software signing).

**Certifications:** FIPS 140-2 Level 2-4, Common Criteria EAL4+.

════════════════════════════════════════════════════════════════════════════

🏛️ **HSM FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**What is an HSM?**

Hardware Security Module combines:
1. **Secure key storage** (tamper-resistant memory)
2. **Cryptographic accelerators** (AES, RSA, ECC hardware engines)
3. **Physical tamper detection** (sensors, mesh, epoxy coating)
4. **Secure APIs** (PKCS#11, CNG, JCE)
5. **Audit logging** (who accessed which keys, when)

**HSM vs. Software Crypto:**

| Aspect | Software Crypto | HSM |
|:-------|:----------------|:----|
| **Key storage** | RAM, disk (encrypted) | Tamper-resistant secure element |
| **Key extraction** | Possible (memory dump, debugger) | **Impossible** (hardware protection) |
| **Performance** | CPU-bound (slower) | Hardware acceleration (faster) |
| **Tamper detection** | None | Active sensors (voltage, temperature, drilling) |
| **Certification** | None (application-level) | FIPS 140-2, CC EAL4+ |
| **Cost** | Free (software libraries) | $1K-$100K+ per device |
| **Use case** | Low-security applications | High-value keys (CA root, payments) |

**HSM Form Factors:**

1. **PCIe Card** (internal server HSM)
   - Example: Thales Luna PCIe HSM
   - ~10K-50K operations/sec

2. **Network Appliance** (centralized HSM)
   - Example: nCipher nShield Connect
   - Shared by multiple servers via network

3. **Embedded HSM** (on-chip secure element)
   - Example: NXP EdgeLock SE050, Infineon SLI97
   - Used in automotive ECUs, IoT devices

4. **Cloud HSM** (managed service)
   - Example: AWS CloudHSM, Azure Dedicated HSM
   - FIPS 140-2 Level 3, pay-per-use

════════════════════════════════════════════════════════════════════════════

🔒 **FIPS 140-2/3 SECURITY LEVELS**
─────────────────────────────────────────────────────────────────────────

**FIPS 140-2 (Federal Information Processing Standard):**

| Level | Security Features | Tamper Protection | Use Case |
|:------|:------------------|:------------------|:---------|
| **Level 1** | Basic crypto correctness | None | Development, non-critical |
| **Level 2** | Role-based auth, tamper-evident | Coatings, seals | Commercial applications |
| **Level 3** | Identity-based auth, tamper-responsive | Active sensors, zeroization | Financial, government |
| **Level 4** | Environmental protection, full zeroization | Voltage/temp/radiation detection | Military, critical infrastructure |

**Level 2 Requirements:**
- Tamper-evident seals (detect physical intrusion)
- Role-based authentication (Crypto Officer vs. User)
- Audit logging

**Level 3 Requirements (adds):**
- Identity-based authentication (not just role)
- Tamper-responsive zeroization (erase keys on intrusion attempt)
- Physical sensors (voltage glitching, temperature extremes)

**Level 4 Requirements (adds):**
- Environmental fault protection (extreme voltage, radiation)
- Immediate zeroization on any anomaly
- Rare/expensive (military-grade)

**FIPS 140-3 (2019 update):**
- Aligns with ISO/IEC 19790
- Adds software module validation
- Stricter entropy requirements
- Algorithm transitions (deprecate 3DES, SHA-1)

════════════════════════════════════════════════════════════════════════════

🔑 **KEY LIFECYCLE MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**Key Generation Inside HSM:**

.. code-block:: c

   // Generate ECDSA-P384 key pair inside HSM (PKCS#11 API)
   #include <cryptoki.h>
   
   CK_RV generate_ecc_keypair_in_hsm(CK_SESSION_HANDLE session,
                                      CK_OBJECT_HANDLE *pub_key,
                                      CK_OBJECT_HANDLE *priv_key) {
       // Define ECC parameters (NIST P-384)
       CK_BYTE ec_params[] = {0x06, 0x05, 0x2B, 0x81, 0x04, 0x00, 0x22};
       
       // Public key template
       CK_ATTRIBUTE pub_template[] = {
           {CKA_EC_PARAMS, ec_params, sizeof(ec_params)},
           {CKA_VERIFY, &true_val, sizeof(CK_BBOOL)},
           {CKA_TOKEN, &true_val, sizeof(CK_BBOOL)},  // Persistent
           {CKA_LABEL, "Avionics-Code-Signing-Pub", 27}
       };
       
       // Private key template
       CK_ATTRIBUTE priv_template[] = {
           {CKA_SIGN, &true_val, sizeof(CK_BBOOL)},
           {CKA_TOKEN, &true_val, sizeof(CK_BBOOL)},
           {CKA_PRIVATE, &true_val, sizeof(CK_BBOOL)},
           {CKA_SENSITIVE, &true_val, sizeof(CK_BBOOL)},  // Cannot export
           {CKA_EXTRACTABLE, &false_val, sizeof(CK_BBOOL)},  // Never leaves HSM
           {CKA_LABEL, "Avionics-Code-Signing-Priv", 28}
       };
       
       // Generate keypair (private key never exposed)
       CK_MECHANISM mech = {CKM_EC_KEY_PAIR_GEN, NULL, 0};
       CK_RV rv = C_GenerateKeyPair(
           session,
           &mech,
           pub_template, 4,
           priv_template, 5,
           pub_key,
           priv_key
       );
       
       if (rv != CKR_OK) {
           log_error("HSM key generation failed: %lu", rv);
           return rv;
       }
       
       log_info("ECDSA-P384 keypair generated in HSM");
       return CKR_OK;
   }

**Signing with HSM Private Key:**

.. code-block:: c

   // Sign data using HSM private key (key never leaves HSM)
   CK_RV sign_with_hsm(CK_SESSION_HANDLE session,
                       CK_OBJECT_HANDLE priv_key,
                       uint8_t *data, size_t data_len,
                       uint8_t *signature, size_t *sig_len) {
       // Calculate SHA-384 hash (can be done outside HSM)
       uint8_t hash[48];
       SHA384(data, data_len, hash);
       
       // Sign hash with HSM private key
       CK_MECHANISM mech = {CKM_ECDSA, NULL, 0};
       CK_RV rv = C_SignInit(session, &mech, priv_key);
       if (rv != CKR_OK) return rv;
       
       // HSM performs ECDSA signature (private key never exposed)
       rv = C_Sign(session, hash, 48, signature, sig_len);
       
       if (rv == CKR_OK) {
           log_audit("Signature generated using HSM key", priv_key);
       }
       
       return rv;
   }

**Key Backup & Recovery:**

.. code-block:: python

   # Secure key backup using key wrapping
   def backup_hsm_key(hsm_session, key_handle, backup_kek):
       """
       Wrap HSM key with Key Encryption Key (KEK) for backup.
       Key leaves HSM only in encrypted form.
       """
       # Generate AES-256-GCM key wrapping key (if not exists)
       if not backup_kek:
           backup_kek = hsm_session.generate_key(
               mechanism='CKM_AES_KEY_GEN',
               attributes={
                   'key_type': 'CKK_AES',
                   'value_len': 32,
                   'label': 'Backup-KEK',
                   'wrap': True,
                   'extractable': False  # KEK also non-extractable
               }
           )
       
       # Wrap target key with KEK (AES-GCM authenticated encryption)
       wrapped_key = hsm_session.wrap_key(
           wrapping_key=backup_kek,
           key_to_wrap=key_handle,
           mechanism='CKM_AES_GCM',
           iv=os.urandom(12)
       )
       
       # Store wrapped key in secure backup (encrypted at rest)
       backup_metadata = {
           'wrapped_key': wrapped_key,
           'wrapping_kek_label': 'Backup-KEK',
           'key_label': hsm_session.get_attribute(key_handle, 'label'),
           'timestamp': datetime.now().isoformat(),
           'hsm_serial': hsm_session.get_info()['serialNumber']
       }
       
       # Encrypt backup metadata with HSM master key
       encrypted_backup = encrypt_backup(backup_metadata)
       
       # Store in geographically distributed locations
       store_backup(encrypted_backup, locations=['primary', 'dr_site', 'cloud'])
       
       return encrypted_backup

**Key Destruction (Zeroization):**

.. code-block:: c

   // Secure key destruction
   CK_RV destroy_hsm_key(CK_SESSION_HANDLE session, CK_OBJECT_HANDLE key) {
       // PKCS#11 key destruction
       CK_RV rv = C_DestroyObject(session, key);
       
       if (rv == CKR_OK) {
           log_audit("Key destroyed", key);
           // HSM overwrites key storage with zeros (FIPS requirement)
       }
       
       return rv;
   }

════════════════════════════════════════════════════════════════════════════

⚡ **CRYPTOGRAPHIC OPERATIONS**
─────────────────────────────────────────────────────────────────────────

**Supported Algorithms (typical HSM):**

**Symmetric:**
- AES (128/192/256-bit): ECB, CBC, CTR, GCM
- 3DES (legacy, deprecated)
- HMAC-SHA256/384/512

**Asymmetric:**
- RSA (2048/3072/4096-bit): Sign, verify, encrypt, decrypt
- ECDSA (P-256/P-384/P-521): Sign, verify
- ECDH (P-256/P-384): Key agreement

**Hash:**
- SHA-256/384/512
- SHA-3 (newer HSMs)

**Performance (Thales Luna SA-7 example):**

| Operation | Performance |
|:----------|:------------|
| RSA-2048 Sign | 10,000 ops/sec |
| RSA-2048 Verify | 60,000 ops/sec |
| ECDSA-P256 Sign | 15,000 ops/sec |
| AES-256-GCM Encrypt | 5 GB/sec |
| HMAC-SHA256 | 8 GB/sec |

**Automotive Use Case: V2X Message Signing**

.. code-block:: c

   // V2X (Vehicle-to-Everything) message signing with HSM
   typedef struct {
       uint64_t timestamp;
       float latitude;
       float longitude;
       float speed;
       float heading;
       uint8_t message_type;
   } V2XMessage;
   
   bool sign_v2x_message(CK_SESSION_HANDLE hsm,
                         CK_OBJECT_HANDLE v2x_priv_key,
                         V2XMessage *msg,
                         uint8_t *signature) {
       // Serialize message
       uint8_t serialized[256];
       size_t len = serialize_v2x(msg, serialized);
       
       // Hash message (SHA-256)
       uint8_t hash[32];
       SHA256(serialized, len, hash);
       
       // Sign with HSM (ECDSA-P256, 100ms latency requirement)
       CK_MECHANISM mech = {CKM_ECDSA, NULL, 0};
       C_SignInit(hsm, &mech, v2x_priv_key);
       
       size_t sig_len = 64;  // ECDSA-P256 signature
       CK_RV rv = C_Sign(hsm, hash, 32, signature, &sig_len);
       
       if (rv != CKR_OK || sig_len != 64) {
           log_error("V2X signing failed");
           return false;
       }
       
       // V2X requires <100ms end-to-end (HSM adds ~2-5ms)
       return true;
   }

**Aerospace Use Case: Software Signing**

.. code-block:: python

   # Avionics software signing with HSM (DO-326A compliance)
   class AvionicsSoftwareSigner:
       def __init__(self, hsm_session, signing_key_label):
           self.hsm = hsm_session
           self.key = hsm_session.find_objects(label=signing_key_label)[0]
       
       def sign_loadable_software(self, software_path, output_path):
           """Sign avionics software per ARINC 615A requirements"""
           # Calculate SHA-384 hash of software binary
           hasher = hashlib.sha384()
           with open(software_path, 'rb') as f:
               while chunk := f.read(8192):
                   hasher.update(chunk)
           software_hash = hasher.digest()
           
           # Sign hash with HSM private key (ECDSA-P384)
           signature = self.hsm.sign(
               key=self.key,
               data=software_hash,
               mechanism='CKM_ECDSA'
           )
           
           # Create ARINC 615A loadable file
           load_file = {
               'software': open(software_path, 'rb').read(),
               'sha384': software_hash,
               'signature': signature,
               'certificate': self.get_certificate(),
               'part_number': 'FMS-SW-8.2.5',
               'version': '8.2.5',
               'signing_date': datetime.now().isoformat()
           }
           
           # Write signed load file
           with open(output_path, 'wb') as f:
               f.write(self.serialize_load_file(load_file))
           
           # Audit log
           self.hsm.log_audit({
               'event': 'SOFTWARE_SIGNED',
               'file': software_path,
               'key_label': self.key.label,
               'signature_length': len(signature)
           })
           
           return signature

════════════════════════════════════════════════════════════════════════════

🛡️ **TAMPER PROTECTION MECHANISMS**
─────────────────────────────────────────────────────────────────────────

**Physical Tamper Detection:**

1. **Tamper-Evident Coatings** (FIPS 140-2 Level 2)
   - Epoxy coating over chip
   - Breaking coating leaves visible marks
   - Inspection required at regular intervals

2. **Tamper-Responsive Sensors** (Level 3)
   - Voltage glitch detection
   - Temperature sensors (detect heating/freezing attacks)
   - Optical sensors (detect laser probing)
   - Mesh layer (detects drilling, milling)
   
   **Response:** Immediate zeroization of all keys

3. **Active Shields** (Level 4)
   - Continuous monitoring of power rails
   - Clock frequency monitoring (detect underclocking)
   - Radiation detectors
   - Acoustic sensors (detect ultrasonic attacks)

**Zeroization Logic:**

.. code-block:: c

   // Tamper response: immediate key zeroization
   void tamper_detected_handler(TamperEvent event) {
       log_critical("TAMPER DETECTED: %s", event.type);
       
       // Disable all cryptographic operations
       disable_crypto_engine();
       
       // Overwrite all key storage with zeros (FIPS requirement: 3 passes)
       for (int pass = 0; pass < 3; pass++) {
           memset(key_storage, 0x00, KEY_STORAGE_SIZE);
           memset(key_storage, 0xFF, KEY_STORAGE_SIZE);
           memset(key_storage, 0xAA, KEY_STORAGE_SIZE);
       }
       
       // Cut power to secure memory
       disable_secure_memory_power();
       
       // Set tamper flag (persistent, requires factory reset)
       set_nvram_flag(TAMPER_FLAG, 1);
       
       // Halt all operations
       while(1) {
           __asm__("hlt");
       }
   }

**Side-Channel Attack Mitigations:**

.. code-block:: c

   // Constant-time ECDSA signing (prevent timing attacks)
   void ecdsa_sign_constant_time(const uint8_t *hash,
                                  const EC_KEY *priv_key,
                                  uint8_t *signature) {
       // Use constant-time scalar multiplication
       EC_POINT *R = EC_POINT_new(group);
       
       // Randomized nonce (RFC 6979 deterministic + additional entropy)
       BIGNUM *k = generate_nonce_constant_time(hash, priv_key);
       
       // k * G (constant-time multiplication, no branches)
       EC_POINT_mul(group, R, k, NULL, NULL, ctx);
       
       // Extract r coordinate
       BIGNUM *r = BN_new();
       EC_POINT_get_affine_coordinates(group, R, r, NULL, ctx);
       
       // s = k^-1 * (hash + r * priv_key) mod n (constant-time)
       BIGNUM *s = BN_new();
       compute_s_constant_time(s, k, r, hash, priv_key);
       
       // Encode signature
       encode_ecdsa_signature(signature, r, s);
       
       // Secure cleanup (prevent key recovery from memory)
       BN_clear_free(k);
       BN_clear_free(r);
       BN_clear_free(s);
   }

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why use HSM instead of software-based key storage?**

**A1:**

| Threat | Software Storage | HSM |
|:-------|:-----------------|:----|
| **Memory dump** | ❌ Private key exposed | ✅ Key never in system RAM |
| **Debugger** | ❌ Can extract key | ✅ No debugger interface |
| **Physical access** | ❌ Disk encryption crackable | ✅ Tamper sensors zeroize keys |
| **Side-channel** | ❌ Timing/power analysis possible | ✅ Constant-time operations |
| **Compliance** | ❌ No certification | ✅ FIPS 140-2, CC EAL4+ |

**Use HSM when:**
- High-value keys (CA root, payment processing, code signing)
- Regulatory compliance (PCI DSS, FIPS, ISO 21434 CAL 4)
- Long key lifetime (10-30 years for aerospace/automotive)

**Q2: Explain FIPS 140-2 Level 3 vs. Level 4.**

**A2:**

**Level 3:**
- Identity-based auth (not just role-based)
- Tamper-responsive (zeroize on intrusion attempt)
- Physical sensors (voltage, temperature, optical)
- Use case: Financial services, government

**Level 4 (adds):**
- Environmental protection (extreme voltage, temperature, radiation)
- Immediate zeroization on ANY anomaly (no grace period)
- Multi-layer active shields
- Use case: Military, critical infrastructure
- Cost: 5-10× more expensive than Level 3

**Key difference:** Level 4 protects against **environmental attacks** (e.g., attacker heats HSM to 150°C to induce faults).

**Q3: How does HSM key wrapping enable secure backup?**

**A3:**
**Problem:** Need to backup HSM keys, but extracting plaintext keys defeats HSM purpose.

**Solution: Key Wrapping**
1. Generate Key Encryption Key (KEK) inside HSM (non-extractable)
2. Wrap target key with KEK using AES-GCM
3. Export wrapped key (encrypted blob)
4. Store encrypted blob in backup system

**Recovery:**
1. Import wrapped key to HSM
2. HSM unwraps using KEK (plaintext key never leaves HSM)
3. Original key restored to HSM secure storage

**Security:** Wrapped key useless without KEK (which never leaves HSM).

**Q4: Describe automotive V2X key management with HSM.**

**A4:**
**V2X (Vehicle-to-Everything) Requirements:**
- Each vehicle has unique ECDSA-P256 key pair
- Messages signed with private key (authenticate sender)
- 100ms latency budget (including signature generation)

**HSM Role:**
```
ECU (Application Processor)
    ↓ Sign V2X message (via API)
HSM (Secure Element)
    ↓ ECDSA-P256 signature (~2-5ms)
V2X Radio
    ↓ Broadcast signed message
Other Vehicles
    ↓ Verify signature (public key)
Accept/Reject message
```

**Key Lifecycle:**
- **Generation:** Factory HSM generates key pair, provisions to vehicle HSM
- **Storage:** Private key in vehicle HSM (NXP SHE, Infineon AURIX HSM)
- **Usage:** 10 messages/sec × 15 years = 4.7B signatures (HSM rated for >10B)
- **Revocation:** Certificate expires after 3 years, new key issued

**Q5: What happens when HSM detects tamper attempt?**

**A5:**
**FIPS 140-2 Level 3 Tamper Response:**

**Detection:** Sensor triggers (voltage glitch, temperature >85°C, mesh breach)

**Immediate Actions (hardware):**
1. Disable crypto engine (all operations halt)
2. Zeroize key storage (3-pass overwrite: 0x00, 0xFF, 0xAA)
3. Cut power to secure memory
4. Set persistent tamper flag (requires factory reset)

**Aftermath:**
- HSM enters "error state" (all APIs return CKR_DEVICE_ERROR)
- Physical return to vendor required (cannot be reset in field)
- Keys lost forever (must restore from backup via key wrapping)

**Audit Trail:**
- Log tamper event (type, timestamp, sensor ID)
- Notify security operations center
- Trigger incident response procedure

**Real-world:** Protects against insider attacks (maintenance technician attempting key extraction).

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
