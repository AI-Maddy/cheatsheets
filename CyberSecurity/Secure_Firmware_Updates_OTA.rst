🔄 **SECURE FIRMWARE UPDATES / OTA**
═══════════════════════════════════════════════════════════════════════

**Over-the-Air (OTA) Updates with Cryptographic Security & Rollback Protection**  
**Purpose:** Secure software delivery 📦 | Update integrity 🔒 | Failsafe mechanisms 🛡️  
**Standards:** ISO 21434, DO-326A, IEC 62443-4-2, UNECE R156

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Secure firmware updates** enable **remote vulnerability patching** while preventing **malicious code injection**.

**Critical requirements:**
1. **Authentication:** Digital signatures (ECDSA, RSA)
2. **Integrity:** Hash verification (SHA-256)
3. **Rollback protection:** Version monotonicity
4. **Secure delivery:** Encrypted transport (TLS)
5. **Fail-safe:** Fallback to last-known-good version

**Use cases:** Automotive OTA, avionics software loading (ARINC 615A), IoT firmware updates.

════════════════════════════════════════════════════════════════════════════

🏗️ **UPDATE ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**End-to-End OTA Update Flow:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────────┐
   │ 1. OEM Server (Update Provider)                            │
   │    ├─ Build firmware image                                  │
   │    ├─ Sign with ECDSA-P384 (HSM private key)              │
   │    ├─ Encrypt update package (AES-256-GCM)                │
   │    └─ Upload to CDN (HTTPS)                                │
   └────────────────┬─────────────────────────────────────────────┘
                    │ TLS 1.3 (mutual authentication)
                    ▼
   ┌──────────────────────────────────────────────────────────────┐
   │ 2. Vehicle Gateway / TCU (Telematics Control Unit)         │
   │    ├─ Poll for updates (campaign management)               │
   │    ├─ Download encrypted package                            │
   │    ├─ Verify signature (OEM public key)                    │
   │    ├─ Decrypt update package                                │
   │    └─ Distribute to target ECUs (CAN/Ethernet)             │
   └────────────────┬─────────────────────────────────────────────┘
                    │ Secure CAN (AUTOSAR SecOC)
                    ▼
   ┌──────────────────────────────────────────────────────────────┐
   │ 3. Target ECU (e.g., Engine Control Module)                │
   │    ├─ Receive update chunks                                 │
   │    ├─ Verify signature again (defense-in-depth)            │
   │    ├─ Store in staging area (flash bank B)                 │
   │    ├─ Perform integrity checks (SHA-256, CRC32)            │
   │    ├─ Validate version (prevent rollback)                  │
   │    ├─ Install update (write to boot partition)             │
   │    ├─ Reboot and verify                                     │
   │    └─ Commit or rollback                                    │
   └──────────────────────────────────────────────────────────────┘

**Update Package Structure:**

.. code-block:: c

   typedef struct {
       char magic[8];              // "OTAPKG01"
       uint32_t version_major;
       uint32_t version_minor;
       uint32_t version_patch;
       uint64_t timestamp;         // Unix time
       char target_ecu[32];        // ECU identifier
       uint32_t payload_size;
       uint8_t payload_sha256[32];
       uint8_t signature[96];      // ECDSA-P384
       uint8_t encrypted_payload[];  // AES-256-GCM encrypted
   } OTAPackage;

════════════════════════════════════════════════════════════════════════════

🔐 **CRYPTOGRAPHIC PROTECTIONS**
─────────────────────────────────────────────────────────────────────────

**Digital Signature Verification:**

.. code-block:: c

   #include <mbedtls/ecdsa.h>
   #include <mbedtls/sha256.h>
   
   bool verify_update_signature(const OTAPackage *pkg) {
       mbedtls_ecdsa_context ctx;
       mbedtls_ecdsa_init(&ctx);
       
       // Load OEM public key (stored in secure flash)
       load_oem_public_key(&ctx);
       
       // Calculate SHA-256 hash of package metadata + payload
       uint8_t hash[32];
       mbedtls_sha256_context sha_ctx;
       mbedtls_sha256_init(&sha_ctx);
       mbedtls_sha256_starts(&sha_ctx, 0);
       
       // Hash header (exclude signature field)
       mbedtls_sha256_update(&sha_ctx, (uint8_t*)pkg, 
                             offsetof(OTAPackage, signature));
       
       // Hash encrypted payload
       mbedtls_sha256_update(&sha_ctx, pkg->encrypted_payload, 
                             pkg->payload_size);
       
       mbedtls_sha256_finish(&sha_ctx, hash);
       
       // Verify ECDSA signature
       mbedtls_mpi r, s;
       mbedtls_mpi_init(&r);
       mbedtls_mpi_init(&s);
       mbedtls_mpi_read_binary(&r, pkg->signature, 48);
       mbedtls_mpi_read_binary(&s, pkg->signature + 48, 48);
       
       int result = mbedtls_ecdsa_verify(&ctx.grp, hash, 32, 
                                          &ctx.Q, &r, &s);
       
       mbedtls_mpi_free(&r);
       mbedtls_mpi_free(&s);
       mbedtls_ecdsa_free(&ctx);
       
       if (result != 0) {
           log_security_event(UPDATE_SIG_FAIL, pkg->version_major);
           return false;
       }
       
       log_audit("Update signature verified", pkg->version_major);
       return true;
   }

**Encrypted Update Transport:**

.. code-block:: c

   // Decrypt update payload
   bool decrypt_update_payload(const OTAPackage *pkg, uint8_t *plaintext) {
       // Derive decryption key from vehicle-specific master key
       uint8_t dec_key[32];
       derive_update_key(dec_key, "firmware-decrypt");
       
       // Extract IV from first 12 bytes of payload
       const uint8_t *iv = pkg->encrypted_payload;
       const uint8_t *ciphertext = pkg->encrypted_payload + 12;
       const uint8_t *tag = pkg->encrypted_payload + pkg->payload_size - 16;
       size_t ct_len = pkg->payload_size - 12 - 16;
       
       // Decrypt with AES-256-GCM
       mbedtls_gcm_context gcm_ctx;
       mbedtls_gcm_init(&gcm_ctx);
       mbedtls_gcm_setkey(&gcm_ctx, MBEDTLS_CIPHER_ID_AES, dec_key, 256);
       
       int ret = mbedtls_gcm_auth_decrypt(
           &gcm_ctx,
           ct_len,
           iv, 12,
           NULL, 0,      // No additional authenticated data
           tag, 16,
           ciphertext,
           plaintext
       );
       
       mbedtls_gcm_free(&gcm_ctx);
       memset(dec_key, 0, 32);  // Secure cleanup
       
       if (ret != 0) {
           log_security_event(UPDATE_DECRYPT_FAIL);
           memset(plaintext, 0, ct_len);
           return false;
       }
       
       return true;
   }

════════════════════════════════════════════════════════════════════════════

🔄 **ROLLBACK PROTECTION**
─────────────────────────────────────────────────────────────────────────

**Version Monotonicity Enforcement:**

.. code-block:: c

   typedef struct {
       uint32_t major;
       uint32_t minor;
       uint32_t patch;
       uint64_t commit_timestamp;  // Monotonic counter
   } FirmwareVersion;
   
   // Compare versions (returns: 1 if new > current, 0 if equal, -1 if new < current)
   int compare_versions(const FirmwareVersion *new_ver, 
                        const FirmwareVersion *current_ver) {
       if (new_ver->major != current_ver->major)
           return (new_ver->major > current_ver->major) ? 1 : -1;
       if (new_ver->minor != current_ver->minor)
           return (new_ver->minor > current_ver->minor) ? 1 : -1;
       if (new_ver->patch != current_ver->patch)
           return (new_ver->patch > current_ver->patch) ? 1 : -1;
       return 0;
   }
   
   // Enforce rollback protection
   bool validate_update_version(const OTAPackage *pkg) {
       FirmwareVersion current_ver;
       get_current_firmware_version(&current_ver);
       
       FirmwareVersion new_ver = {
           .major = pkg->version_major,
           .minor = pkg->version_minor,
           .patch = pkg->version_patch,
           .commit_timestamp = pkg->timestamp
       };
       
       int cmp = compare_versions(&new_ver, &current_ver);
       
       if (cmp < 0) {
           // Downgrade attempt!
           log_security_event(ROLLBACK_ATTEMPT, new_ver.major, new_ver.minor);
           return false;
       }
       
       if (cmp == 0) {
           // Same version (re-flash allowed for factory reset scenarios)
           log_warn("Re-flashing same version");
       }
       
       // Check monotonic timestamp (additional protection)
       if (new_ver.commit_timestamp <= current_ver.commit_timestamp) {
           log_security_event(TIMESTAMP_ROLLBACK);
           return false;
       }
       
       return true;
   }

**Secure Version Storage:**

.. code-block:: c

   // Store version in tamper-resistant memory
   void commit_firmware_version(const FirmwareVersion *ver) {
       // Write to secure EEPROM or OTP (One-Time Programmable) fuses
       uint32_t secure_version = calculate_version_word(ver);
       
       // Anti-rollback fuse (can only increment, never decrement)
       if (has_arb_fuse()) {
           write_arb_fuse(secure_version);
       }
       
       // Redundant storage (3 copies with voting)
       for (int i = 0; i < 3; i++) {
           write_secure_flash(VERSION_STORAGE_BASE + i * sizeof(FirmwareVersion),
                              ver, sizeof(FirmwareVersion));
       }
       
       log_audit("Firmware version committed", ver->major, ver->minor, ver->patch);
   }

════════════════════════════════════════════════════════════════════════════

🛡️ **FAIL-SAFE MECHANISMS**
─────────────────────────────────────────────────────────────────────────

**Dual-Bank Flash (A/B Partitioning):**

.. code-block:: text

   Flash Memory Layout:
   
   ┌─────────────────────────────────────┐ 0x08000000
   │  Bootloader (Secure, Read-Only)     │ 32 KB
   ├─────────────────────────────────────┤ 0x08008000
   │  Bank A (Active Firmware)           │ 512 KB
   │  - Current running version          │
   ├─────────────────────────────────────┤ 0x08088000
   │  Bank B (Staging Area)              │ 512 KB
   │  - New firmware downloaded here     │
   ├─────────────────────────────────────┤ 0x08108000
   │  Configuration Data                 │ 64 KB
   │  - Boot flags, version info         │
   └─────────────────────────────────────┘

**Update Installation Flow:**

.. code-block:: c

   typedef enum {
       BOOT_BANK_A,
       BOOT_BANK_B,
       BOOT_RECOVERY
   } BootBank;
   
   typedef struct {
       BootBank active_bank;
       uint32_t bank_a_version;
       uint32_t bank_b_version;
       uint8_t boot_attempts;      // Rollback after 3 failures
       bool update_in_progress;
       uint32_t crc_bank_a;
       uint32_t crc_bank_b;
   } BootConfig;
   
   // Bootloader logic
   void bootloader_main(void) {
       BootConfig config;
       load_boot_config(&config);
       
       // Check if update in progress
       if (config.update_in_progress) {
           // New firmware staged in Bank B, attempt boot
           config.active_bank = BOOT_BANK_B;
           config.boot_attempts = 0;
           save_boot_config(&config);
       }
       
       // Verify active bank integrity
       uint32_t calculated_crc = calculate_flash_crc(
           config.active_bank == BOOT_BANK_A ? BANK_A_BASE : BANK_B_BASE,
           BANK_SIZE
       );
       
       uint32_t expected_crc = (config.active_bank == BOOT_BANK_A) ?
                                config.crc_bank_a : config.crc_bank_b;
       
       if (calculated_crc != expected_crc) {
           // Integrity failure! Rollback
           log_critical("Bank %d integrity check failed", config.active_bank);
           rollback_to_previous_bank(&config);
           return;
       }
       
       // Boot from active bank
       void (*firmware_entry)(void) = (void(*)(void))(
           config.active_bank == BOOT_BANK_A ? BANK_A_BASE : BANK_B_BASE
       );
       
       firmware_entry();
       
       // If we reach here, firmware crashed - rollback
       config.boot_attempts++;
       if (config.boot_attempts >= 3) {
           log_critical("Firmware boot failed 3 times - rolling back");
           rollback_to_previous_bank(&config);
       }
       
       save_boot_config(&config);
       system_reset();
   }
   
   void rollback_to_previous_bank(BootConfig *config) {
       // Switch back to previous working bank
       config->active_bank = (config->active_bank == BOOT_BANK_A) ?
                             BOOT_BANK_B : BOOT_BANK_A;
       config->boot_attempts = 0;
       config->update_in_progress = false;
       save_boot_config(config);
       
       log_audit("Rolled back to Bank %c", 
                 config->active_bank == BOOT_BANK_A ? 'A' : 'B');
   }

**Watchdog-Based Rollback:**

.. code-block:: c

   // Firmware confirms successful boot within timeout
   void firmware_main(void) {
       // Initialize hardware
       init_hardware();
       
       // Start watchdog (5-minute timeout for complex init)
       start_watchdog(300000);  // 5 minutes
       
       // Perform safety-critical checks
       if (!self_test_passed()) {
           // Deliberately don't feed watchdog - force rollback
           log_error("Self-test failed - triggering rollback");
           while(1);  // Watchdog will reset system
       }
       
       // All checks passed - commit update
       mark_update_successful();
       
       // Feed watchdog regularly
       while(1) {
           feed_watchdog();
           application_loop();
       }
   }
   
   void mark_update_successful(void) {
       BootConfig config;
       load_boot_config(&config);
       
       config.update_in_progress = false;
       config.boot_attempts = 0;
       
       // Persist current bank as "known-good"
       save_boot_config(&config);
       
       log_audit("Update successful - firmware operational");
   }

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why is signature verification insufficient alone? What else is needed?**

**A1:**
**Signature verification alone prevents:**
✅ Unauthorized firmware (attacker can't sign)
✅ Tampering (modified firmware fails verification)

**But doesn't prevent:**
❌ **Rollback attacks** (attacker replays old signed firmware with known vulnerabilities)
❌ **Replay attacks** (reuse legitimate update multiple times)
❌ **TOCTOU attacks** (firmware modified after verification, before installation)

**Complete solution requires:**
1. **Signature verification** (authentication + integrity)
2. **Version monotonicity** (prevent rollback)
3. **Nonce/timestamp** (prevent replay)
4. **Secure installation** (write to protected memory immediately)
5. **Integrity re-check before boot** (bootloader verifies again)

**Q2: Explain dual-bank flash and its fail-safe benefits.**

**A2:**
**Dual-Bank Architecture:**
- **Bank A:** Currently running firmware (known-good)
- **Bank B:** Staging area for new firmware

**Update Process:**
1. Download new firmware to Bank B (Bank A still operational)
2. Verify signature, integrity in Bank B
3. Reboot, bootloader attempts Bank B
4. If Bank B fails (crash, integrity error) → automatic rollback to Bank A
5. If Bank B succeeds → mark as active, Bank A becomes backup

**Benefits:**
✅ **No brick risk** (always have fallback)
✅ **Fast rollback** (just switch banks, no re-download)
✅ **Test before commit** (new firmware runs in "trial" mode)

**Cost:** 2× flash size (512 KB × 2 = 1 MB required)

**Q3: How does watchdog-based rollback work?**

**A3:**
**Principle:** New firmware must prove it's operational within timeout, or automatic rollback.

**Implementation:**
```c
Bootloader:
1. Install new firmware in Bank B
2. Start watchdog timer (5 minutes)
3. Boot Bank B
4. If watchdog expires → rollback to Bank A
5. If firmware feeds watchdog → update successful

Firmware:
1. Initialize (sensors, networks, crypto)
2. Run self-tests (BITE, RAM test, crypto verify)
3. If tests pass → feed watchdog, mark update successful
4. If tests fail → don't feed watchdog (force rollback)
```

**Safety mechanism:** Corrupt firmware (crashes before feeding watchdog) triggers automatic recovery.

**Q4: What is the risk of encrypting updates, and when is it required?**

**A4:**
**Risk:**
- Encryption **does NOT provide authentication** (attacker can modify ciphertext)
- Requires secure key distribution (how does ECU get decryption key?)
- Performance overhead (decryption adds latency)

**When required:**
✅ **Intellectual property protection** (prevent firmware reverse engineering)
✅ **Regulatory compliance** (ITAR for aerospace, export control)
✅ **Confidential algorithms** (proprietary engine tuning, safety logic)

**When NOT required:**
❌ Firmware will be in flash unencrypted anyway (secure boot provides integrity)
❌ No reverse-engineering concern (open-source components)

**Best practice:** Always sign (authentication), encrypt only if IP/compliance requires it.

**Q5: How does ISO 21434 / UN R156 mandate OTA security?**

**A5:**
**UN R156 (Automotive Software Updates):**
- **Effective:** July 2022 (mandatory for new vehicles in EU/Japan/Korea)
- **Requirements:**
  - Secure update distribution (authenticated, integrity-protected)
  - Version management (track installed versions)
  - Rollback prevention (monotonicity)
  - Update verification (before installation)
  - Logging (audit trail of updates)

**ISO 21434 Requirements:**
- **CAL 2+:** Digital signatures required
- **CAL 3+:** Encrypted transport + secure key storage (HSM)
- **CAL 4:** Formal verification of update process

**Compliance checklist:**
□ ECDSA or RSA signatures (2048-bit minimum)
□ TLS 1.2+ transport security
□ Rollback protection (version checks)
□ Fail-safe mechanisms (dual-bank or recovery partition)
□ Audit logging (who, what, when)
□ Field monitoring (detect update failures in fleet)

**Penalty for non-compliance:** Type approval denial (cannot sell vehicles in regulated markets).

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~850
