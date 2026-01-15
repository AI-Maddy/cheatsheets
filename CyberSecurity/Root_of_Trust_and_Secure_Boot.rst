🔑 **ROOT OF TRUST & SECURE BOOT — Complete Security Foundation**
═══════════════════════════════════════════════════════════════════════

**The Immutable Hardware Anchor for All Embedded System Security**  
**Purpose:** Boot chain security 🔐 | Trust establishment 🏛️ | Attack prevention 🛡️  
**Domains:** Automotive 🚗 | Avionics ✈️ | Industrial 🏭 | Medical 🏥 | IoT 📡

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Root of Trust (RoT)** is the immutable hardware/firmware anchor that establishes trust for the entire system. **Secure Boot** uses this RoT to verify each stage of the boot process, creating an unbroken **chain of trust** from power-on to OS.

**Key Equation:** `RoT → Verify Bootloader → Verify OS → Verify Applications = Trusted System`

**Real-World Impact:** Prevents malware installation, protects against firmware tampering, enables remote attestation. Used in: iPhone Secure Enclave, automotive ECUs (ISO 21434), medical devices (FDA guidance), payment terminals.

════════════════════════════════════════════════════════════════════════════

🏛️ **ROOT OF TRUST (RoT) FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**🎯 Definition:**
A **Root of Trust (RoT)** is the foundational security primitive that cannot be modified or bypassed. It's the "trust anchor" upon which all other security mechanisms depend.

**Three Types of RoT:**

1. **🔐 Root of Trust for Storage (RTS)**
   - Secure storage for cryptographic keys, certificates, secrets
   - Cannot be read or modified by unauthorized software
   - Examples: OTP (One-Time Programmable) fuses, secure EEPROM, TPM NV-RAM

2. **📊 Root of Trust for Reporting (RTR)**
   - Provides attestation of system state
   - Generates signed reports of measurements (PCRs in TPM)
   - Enables remote attestation

3. **✅ Root of Trust for Measurement (RTM)**
   - First code executed at power-on (immutable)
   - Measures/hashes next boot stage
   - Creates chain of measurements

**🏗️ Implementation Forms:**

| Type | Description | Examples | Immutability Level |
|:-----|:------------|:---------|:-------------------|
| 🔥 **Hardware RoT** | Dedicated security processor | TPM 2.0, Secure Enclave, HSM | ✅ Highest (mask ROM, fuses) |
| 🧱 **Firmware RoT** | Immutable boot ROM | Boot ROM in SoC | ✅ High (cannot update) |
| 💾 **Software RoT** | Protected code in flash | UEFI Secure Boot | ⚠️ Medium (can be attacked) |

**Best Practice:** Always use **Hardware RoT** for safety-critical/high-security systems!

════════════════════════════════════════════════════════════════════════════

🚀 **SECURE BOOT PROCESS**
─────────────────────────────────────────────────────────────────────────

**🎯 Goal:** Ensure only **authentic, unmodified** code executes at every boot stage.

**Boot Chain of Trust:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Power-On → ROM Code (RoT) → Bootloader → OS Kernel → Apps     │
│              ↓ Verify        ↓ Verify    ↓ Verify    ↓ Verify  │
│           [Signature]      [Signature]  [Signature] [Signature] │
└─────────────────────────────────────────────────────────────────┘
```

**Step-by-Step Secure Boot:**

**1️⃣ Stage 0: Boot ROM Execution (Hardware RoT)**
   - CPU fetches first instruction from immutable ROM
   - ROM contains public key hash (root public key)
   - ROM code loads Stage 1 bootloader from flash

**2️⃣ Stage 1: Bootloader Verification**
   - ROM calculates hash of bootloader image
   - ROM verifies digital signature using embedded public key
   - If signature valid → execute bootloader
   - If signature invalid → **HALT** (or boot to recovery)

**3️⃣ Stage 2: Kernel Verification**
   - Bootloader verifies OS kernel signature
   - Uses public key stored in bootloader (verified in Stage 1)
   - Extends chain of trust

**4️⃣ Stage 3: Application Verification**
   - OS verifies application signatures before execution
   - Uses OS-level code signing policies

**Code Example: Signature Verification (Pseudocode)**

.. code-block:: c

   // Stage 1: ROM verifies bootloader
   bool verify_bootloader(void) {
       uint8_t *bootloader_addr = (uint8_t *)0x08000000;
       uint32_t bootloader_size = 64 * 1024; // 64 KB
       
       // 1. Calculate SHA-256 hash of bootloader
       uint8_t calculated_hash[32];
       sha256(bootloader_addr, bootloader_size, calculated_hash);
       
       // 2. Read signature from bootloader header
       signature_t *sig = (signature_t *)(bootloader_addr + bootloader_size);
       
       // 3. Verify signature using root public key (in ROM)
       const uint8_t root_pubkey[] = ROOT_PUBLIC_KEY_HASH; // Burned in ROM
       
       if (rsa_verify(calculated_hash, 32, sig->data, sig->len, root_pubkey)) {
           return true; // Signature valid, safe to boot
       }
       
       // Signature invalid - HALT!
       secure_halt("Bootloader verification failed");
       return false;
   }

   void secure_halt(const char *reason) {
       // Disable all peripherals
       // Wipe sensitive RAM
       // Optionally: Enter recovery mode
       while(1); // Infinite loop, no boot
   }

════════════════════════════════════════════════════════════════════════════

🔒 **CRYPTOGRAPHIC MECHANISMS**
─────────────────────────────────────────────────────────────────────────

**Digital Signature Algorithms:**

| Algorithm | Key Size | Performance | Use Case |
|:----------|:---------|:------------|:---------|
| 🔑 **RSA** | 2048-4096 bit | Slow verify | Legacy systems, PC boot |
| 📈 **ECDSA** | 256-384 bit | Fast verify | Modern embedded (ARM, automotive) |
| 🔐 **EdDSA** | 256 bit | Fastest | IoT, resource-constrained |

**Hash Functions:**

- **SHA-256** – Most common, 256-bit output
- **SHA-384/512** – Higher security for critical systems
- **SHA-3** – Modern alternative (Keccak)

**Signature Verification Flow:**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Firmware    │────▶│  SHA-256     │────▶│  Hash        │
│  Image       │     │  Hash        │     │  (32 bytes)  │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Signature   │────▶│  RSA/ECDSA   │────▶│  Valid?      │
│  (attached)  │     │  Verify      │     │  ✅ or ❌    │
└──────────────┘     └──────────────┘     └──────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Public Key     │
                  │  (in ROM/fuses) │
                  └─────────────────┘
```

**Real Implementation: STM32 Secure Boot**

.. code-block:: c

   // STM32H7 secure boot with ECDSA-P256
   #include "stm32h7xx_hal.h"
   #include "mbedtls/ecdsa.h"
   #include "mbedtls/sha256.h"
   
   #define FIRMWARE_START  0x08010000
   #define FIRMWARE_SIZE   (256 * 1024)
   #define SIGNATURE_ADDR  (FIRMWARE_START + FIRMWARE_SIZE)
   
   // Public key stored in OTP (One-Time Programmable) flash
   const uint8_t pubkey_x[32] = { /* X coordinate */ };
   const uint8_t pubkey_y[32] = { /* Y coordinate */ };
   
   bool secure_boot_verify(void) {
       mbedtls_ecdsa_context ctx;
       mbedtls_mpi r, s;
       uint8_t hash[32];
       int ret;
       
       // 1. Calculate firmware hash
       mbedtls_sha256((uint8_t *)FIRMWARE_START, FIRMWARE_SIZE, hash, 0);
       
       // 2. Initialize ECDSA context with public key
       mbedtls_ecdsa_init(&ctx);
       mbedtls_ecp_group_load(&ctx.grp, MBEDTLS_ECP_DP_SECP256R1);
       mbedtls_mpi_read_binary(&ctx.Q.X, pubkey_x, 32);
       mbedtls_mpi_read_binary(&ctx.Q.Y, pubkey_y, 32);
       mbedtls_mpi_lset(&ctx.Q.Z, 1);
       
       // 3. Read signature (r, s)
       uint8_t *sig_data = (uint8_t *)SIGNATURE_ADDR;
       mbedtls_mpi_read_binary(&r, sig_data, 32);
       mbedtls_mpi_read_binary(&s, sig_data + 32, 32);
       
       // 4. Verify signature
       ret = mbedtls_ecdsa_verify(&ctx.grp, hash, 32, &ctx.Q, &r, &s);
       
       mbedtls_ecdsa_free(&ctx);
       mbedtls_mpi_free(&r);
       mbedtls_mpi_free(&s);
       
       return (ret == 0); // 0 = success in mbedTLS
   }

════════════════════════════════════════════════════════════════════════════

🔐 **KEY STORAGE & MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**Root Public Key Storage Options:**

1. **🔥 OTP Fuses (One-Time Programmable)**
   - ✅ **Best security** – Cannot be modified after programming
   - ✅ Survives firmware attacks
   - ❌ Cannot update (permanent)
   - **Use case:** Production devices, automotive ECUs
   
   .. code-block:: c
   
      // STM32: Program OTP fuses (IRREVERSIBLE!)
      HAL_FLASH_Unlock();
      HAL_FLASH_OB_Unlock();
      
      for (int i = 0; i < 32; i++) {
          HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, 
                            OTP_AREA_BASE + i, 
                            pubkey_hash[i]);
      }
      
      HAL_FLASH_OB_Lock();
      HAL_FLASH_Lock();

2. **🧱 Mask ROM (Factory Programmed)**
   - ✅ Highest security – Hardcoded in silicon
   - ❌ Cannot update
   - **Use case:** SoC boot ROM

3. **💾 Secure Flash with Write Protection**
   - ⚠️ Medium security – Requires proper protection
   - ✅ Can update (with secure update process)
   - **Use case:** Devices needing key rotation

4. **🔐 Secure Element / HSM**
   - ✅ Highest flexibility – Dedicated security chip
   - ✅ Tamper detection
   - **Use case:** Payment systems, automotive V2X

**Key Revocation Strategies:**

- **Anti-Rollback Counter:** Monotonic counter prevents downgrade attacks
- **Key Versioning:** Support multiple key generations
- **Certificate Revocation List (CRL):** For connected devices

════════════════════════════════════════════════════════════════════════════

🛡️ **ATTACK VECTORS & MITIGATIONS**
─────────────────────────────────────────────────────────────────────────

**Common Attacks:**

**1. 🔴 Firmware Replacement Attack**
   - **Attack:** Replace legitimate firmware with malicious version
   - **Mitigation:** Signature verification (secure boot)
   - **Detection:** Boot fails if signature invalid

**2. 🔴 Downgrade/Rollback Attack**
   - **Attack:** Install old firmware with known vulnerabilities
   - **Mitigation:** Anti-rollback counter (monotonic version)
   
   .. code-block:: c
   
      // Anti-rollback implementation
      uint32_t stored_version = read_antirollback_counter();
      uint32_t firmware_version = get_firmware_version();
      
      if (firmware_version < stored_version) {
          secure_halt("Rollback attack detected");
      }
      
      // Update counter (can only increment!)
      if (firmware_version > stored_version) {
          write_antirollback_counter(firmware_version);
      }

**3. 🟠 Key Extraction Attack**
   - **Attack:** Read private keys from flash/RAM
   - **Mitigation:** Store keys in OTP, HSM, or Secure Element
   - **Defense-in-depth:** Encrypt keys with device-unique key (PUF)

**4. 🟠 Boot ROM Exploit**
   - **Attack:** Find vulnerability in immutable boot ROM
   - **Mitigation:** Formal verification of boot ROM, minimal code
   - **Real example:** Nintendo Switch Tegra X1 bootROM exploit (CVE-2018-6242)

**5. 🟡 Glitching Attack**
   - **Attack:** Voltage/clock glitching to skip signature check
   - **Mitigation:** Redundant checks, glitch detection sensors
   
   .. code-block:: c
   
      // Redundant signature verification
      bool verify1 = verify_signature(image, sig);
      bool verify2 = verify_signature(image, sig);
      bool verify3 = verify_signature(image, sig);
      
      // All three must agree (prevents single-glitch bypass)
      if (!(verify1 && verify2 && verify3)) {
          secure_halt("Signature verification failed");
      }

**6. 🟢 Time-of-Check to Time-of-Use (TOCTOU)**
   - **Attack:** Modify firmware after verification but before execution
   - **Mitigation:** Execute from read-only region, lock flash before boot

════════════════════════════════════════════════════════════════════════════

🏗️ **INDUSTRY IMPLEMENTATIONS**
─────────────────────────────────────────────────────────────────────────

**🍎 Apple Secure Enclave**

- **Hardware:** Dedicated ARM core with encrypted memory
- **Boot ROM:** Immutable, verifies LLB (Low-Level Bootloader)
- **Chain:** Boot ROM → LLB → iBoot → iOS Kernel
- **UID (Unique ID):** Device-specific key fused at manufacturing
- **Features:** Face ID, Touch ID, Apple Pay, encrypted storage

**🚗 Automotive: AUTOSAR SecOC + Secure Boot**

.. code-block:: c

   // AUTOSAR secure boot integration
   Std_ReturnType SecureBootVerify(void) {
       Csm_ReturnType result;
       uint8 hashValue[32];
       uint8 signature[64];
       
       // Use Crypto Service Manager (CSM) for verification
       result = Csm_Hash(CSM_HASH_CONFIG_ID, 
                         firmware_address, 
                         firmware_length, 
                         hashValue);
       
       if (result != CSM_E_OK) return E_NOT_OK;
       
       // Verify signature using HSM
       result = Csm_SignatureVerify(CSM_SIGNATURE_CONFIG_ID,
                                     hashValue, 32,
                                     signature, 64);
       
       return (result == CSM_E_VER_OK) ? E_OK : E_NOT_OK;
   }

**✈️ Avionics: DO-326A Secure Boot**

- **Requirements:** Software load verification (data loading security)
- **Methods:** Digital signatures, checksums, secure loaders
- **SAL Level:** SAL 3 requires cryptographic verification
- **Integration:** With DO-178C (software) and DO-254 (hardware)

**🏥 Medical: FDA Premarket Guidance**

- **Requirement:** "Authenticate software updates" (2023 guidance)
- **SBOM:** Track all boot components
- **Threat Model:** Malicious firmware replacement
- **Validation:** Demonstrate secure boot in 510(k)/PMA submission

**🏭 Industrial: IEC 62443-4-2 Requirements**

- **SR 1.1:** Human user authentication
- **SR 1.2:** Software process authentication
- **SR 1.13:** Access via untrusted networks
- **SR 3.4:** Software and information integrity (secure boot!)

════════════════════════════════════════════════════════════════════════════

🔬 **ADVANCED TOPICS**
─────────────────────────────────────────────────────────────────────────

**Verified Boot vs Measured Boot**

| Aspect | **Verified Boot** | **Measured Boot** |
|:-------|:------------------|:------------------|
| **Action** | Verify signature, HALT if invalid | Measure (hash) all stages, store in PCR |
| **Enforcement** | Prevents malicious code execution | Records what executed (attestation) |
| **Use Case** | Smartphones, ECUs, embedded devices | Enterprise PCs (TPM), cloud VMs |
| **Standard** | UEFI Secure Boot | TPM 2.0, TCG specifications |

**Trusted Platform Module (TPM 2.0)**

- **Platform Configuration Registers (PCRs):** Store measurements
- **Extend Operation:** `PCR[n] = SHA-256(PCR[n] || measurement)`
- **Quote:** Signed attestation report of PCR values
- **Use Case:** Remote attestation (prove device state to server)

.. code-block:: python

   # TPM 2.0 measured boot (Python with tpm2-pytss)
   from tpm2_pytss import *
   
   # Initialize TPM
   tpm = ESAPI()
   
   # Measure bootloader (extend PCR 0)
   bootloader_hash = hashlib.sha256(bootloader_code).digest()
   tpm.pcr_extend(0, bootloader_hash)
   
   # Measure kernel (extend PCR 1)
   kernel_hash = hashlib.sha256(kernel_code).digest()
   tpm.pcr_extend(1, kernel_hash)
   
   # Generate signed quote (attestation)
   quote = tpm.quote(pcr_selection=[0, 1, 2], signing_key=aik_handle)
   
   # Send quote to remote server for verification
   send_to_server(quote)

**Physical Unclonable Function (PUF)**

- **Concept:** Device-unique key derived from manufacturing variations
- **Advantages:** 
  - ✅ No key storage needed
  - ✅ Cannot be cloned (unique per chip)
- **Implementations:** SRAM PUF, Ring Oscillator PUF, Arbiter PUF
- **Use Case:** Device-unique encryption keys

.. code-block:: c

   // SRAM PUF: Read uninitialized SRAM as entropy source
   uint8_t derive_device_key(uint8_t *key_out, size_t key_len) {
       // SRAM power-on state is device-unique
       uint8_t *puf_sram = (uint8_t *)0x20000000; // Uninitialized SRAM
       
       // Read multiple times, apply fuzzy extractor for stability
       uint8_t readings[128];
       for (int i = 0; i < 128; i++) {
           readings[i] = puf_sram[i];
       }
       
       // Derive key using KDF (Key Derivation Function)
       hkdf_sha256(readings, 128, NULL, 0, key_out, key_len);
       
       return 0;
   }

**ARM TrustZone Secure Boot**

- **Secure World:** RoT executes here
- **Normal World:** Regular OS (Linux, Android)
- **Secure Monitor Call (SMC):** Interface between worlds

.. code-block:: c

   // ARM TrustZone: Secure world boot verification
   __attribute__((section(".secure_rom")))
   void secure_boot_entry(void) {
       // Executing in Secure World (highest privilege)
       
       // 1. Initialize Secure World peripherals
       init_secure_crypto();
       
       // 2. Verify Normal World bootloader
       if (!verify_normal_world_image()) {
           secure_halt();
       }
       
       // 3. Switch to Normal World
       switch_to_normal_world(BOOTLOADER_ENTRY_POINT);
   }

════════════════════════════════════════════════════════════════════════════

📊 **COMPLIANCE & STANDARDS MAPPING**
─────────────────────────────────────────────────────────────────────────

| Standard | Requirement | Implementation |
|:---------|:------------|:---------------|
| 🚗 **ISO 21434** | CAL 3-4: Cryptographic verification | Secure boot with ECDSA |
| ✈️ **DO-326A** | SAL 2-3: Software load verification | Digital signatures, secure loaders |
| 🏭 **IEC 62443-4-2** | SR 3.4: Software integrity | Code signing, secure boot |
| 🏥 **FDA Guidance** | Authenticate software updates | Secure boot + OTA signature verification |
| 🔒 **FIPS 140-3** | Level 2-4: Cryptographic module security | HSM-based secure boot |
| 🌐 **NIST SP 800-193** | Platform firmware resiliency | Firmware protection, recovery |

════════════════════════════════════════════════════════════════════════════

💡 **BEST PRACTICES & RECOMMENDATIONS**
─────────────────────────────────────────────────────────────────────────

**✅ DO:**

1. ✅ **Use Hardware RoT** – Immutable trust anchor (OTP fuses, mask ROM)
2. ✅ **Implement Anti-Rollback** – Prevent downgrade attacks
3. ✅ **Use ECDSA over RSA** – Faster verification, smaller keys
4. ✅ **Verify at Every Stage** – Bootloader → Kernel → Apps
5. ✅ **Fail Securely** – HALT on verification failure, don't bypass
6. ✅ **Use Hardware Crypto** – Accelerators prevent timing attacks
7. ✅ **Test Attack Scenarios** – Fuzzing, fault injection, key extraction
8. ✅ **Implement Secure Recovery** – Authenticated recovery mode

**❌ DON'T:**

1. ❌ **Store Private Keys on Device** – Only public keys/certificates
2. ❌ **Skip Verification "for Speed"** – Performance < Security
3. ❌ **Use Weak Crypto** – No MD5, SHA-1, RSA-1024
4. ❌ **Trust User Input During Boot** – No UART/USB commands before verification
5. ❌ **Ignore Glitching Attacks** – Add redundant checks
6. ❌ **Hard-Code Keys** – Use device-unique or OTP storage
7. ❌ **Allow Debug Access in Production** – Disable JTAG/SWD
8. ❌ **Forget About Timing Attacks** – Use constant-time implementations

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: What is the difference between Root of Trust for Measurement (RTM) and Root of Trust for Verification (RTV)?**

**A1:** 
- **RTM (Root of Trust for Measurement)** is the first code executed at power-on. It measures (hashes) the next boot stage and stores the measurement in a PCR (Platform Configuration Register). It doesn't *prevent* execution, just records what ran.
- **RTV (Root of Trust for Verification)** actually verifies the digital signature of the next boot stage before allowing execution. If verification fails, the system halts.
- **Key Difference:** RTM = measure & record (attestation), RTV = verify & enforce (secure boot)

**Q2: Why is ECDSA preferred over RSA for embedded secure boot?**

**A2:**
1. **Smaller Key Size:** ECDSA-256 provides equivalent security to RSA-3072 (much smaller public keys)
2. **Faster Verification:** ECDSA verification is faster on embedded processors (critical for boot time)
3. **Lower Power:** Important for battery-powered devices
4. **Example:** ECDSA-P256 signature = 64 bytes, RSA-2048 signature = 256 bytes

**Q3: How does anti-rollback protection work?**

**A3:**
Anti-rollback uses a **monotonic counter** (can only increment) stored in secure storage (OTP fuses or RPMB):
1. Each firmware version has a version number
2. During boot, compare firmware version with stored counter
3. If `firmware_version < counter` → **HALT** (rollback attack!)
4. If `firmware_version >= counter` → update counter, continue boot
5. Attacker cannot decrement counter, so cannot install old vulnerable firmware

**Q4: What is a Time-of-Check to Time-of-Use (TOCTOU) attack in secure boot?**

**A4:**
**Attack scenario:**
1. Bootloader verifies firmware signature in flash → ✅ PASS
2. **Attacker modifies flash** between verification and execution
3. CPU executes modified (malicious) code

**Mitigations:**
- Execute from **read-only region** (flash locked before execution)
- Use **Execute-in-Place (XIP)** from flash (no RAM copy)
- Enable **MPU/MMU protection** before jumping to firmware

**Q5: Explain the chain of trust in a typical embedded secure boot.**

**A5:**
```
Power-On → ROM Code (RoT) verifies bootloader signature
           ↓ (public key hash in ROM)
Bootloader verified → Bootloader verifies kernel signature
                      ↓ (public key in bootloader)
Kernel verified → Kernel verifies app signatures
                  ↓ (public key in kernel)
Apps verified → System fully trusted
```

Each stage verifies the next using a key established by the previous stage. If any stage fails verification, the chain breaks and system halts. **Trust flows from immutable ROM to all subsequent stages.**

**Q6: What is the role of a Hardware Security Module (HSM) in secure boot?**

**A6:**
An HSM provides:
1. **Secure Key Storage:** Private keys never exposed to main CPU
2. **Crypto Acceleration:** Fast signature verification (ECDSA, RSA)
3. **Tamper Detection:** Physical/voltage attacks trigger key erasure
4. **Isolated Execution:** Verification logic runs in separate processor

**Example:** Automotive ECU with NXP SHE (Secure Hardware Extension):
- Boot ROM requests HSM to verify bootloader signature
- HSM performs verification using internal key
- HSM returns PASS/FAIL to ROM
- Private signing key never leaves HSM

**Q7: How would you implement secure boot for a Cortex-M4 microcontroller without TrustZone?**

**A7:**
**Architecture:**
1. **Boot ROM** (factory-programmed, immutable at 0x00000000)
2. **Public Key Hash** in OTP fuses
3. **Bootloader** at 0x08000000 (external flash)
4. **Application** at 0x08010000

**Implementation:**
```c
// Boot ROM (executed first)
void boot_rom(void) {
    // 1. Initialize crypto hardware
    crypto_init();
    
    // 2. Read public key hash from OTP
    uint8_t pubkey_hash[32];
    read_otp(OTP_PUBKEY_ADDR, pubkey_hash, 32);
    
    // 3. Verify bootloader
    if (!verify_image(BOOTLOADER_ADDR, BOOTLOADER_SIZE, pubkey_hash)) {
        halt_system(); // Verification failed
    }
    
    // 4. Lock flash, disable debug
    FLASH->CR |= FLASH_CR_LOCK;
    DBGMCU->CR = 0; // Disable JTAG/SWD
    
    // 5. Jump to bootloader
    jump_to_app(BOOTLOADER_ADDR);
}
```

**Q8: What is the difference between verified boot and measured boot?**

**A8:**
| Aspect | **Verified Boot** | **Measured Boot** |
|:-------|:------------------|:------------------|
| **Action** | Verify signature, enforce policy | Measure (hash) components, record in PCR |
| **On Failure** | HALT, prevent execution | Continue, but record "bad" measurement |
| **Goal** | Prevent malicious code | Enable remote attestation |
| **Use Case** | Phones, IoT, embedded | Enterprise PCs with TPM |
| **Standard** | UEFI Secure Boot | TPM 2.0, TCG |

**Both can coexist:** Verified boot prevents local attacks, measured boot enables remote verification.

**Q9: How does a Physical Unclonable Function (PUF) enhance secure boot?**

**A9:**
PUF provides a **device-unique key** without storing it:
1. PUF derives key from physical characteristics (SRAM startup state, wire delays)
2. Key is unique per chip, cannot be cloned
3. **Use in secure boot:**
   - Encrypt bootloader with PUF-derived key
   - Only THIS device can decrypt and boot
   - Prevents firmware copying to other devices
   
**Example:** Xilinx FPGA uses SRAM PUF to derive device-unique encryption key for bitstream authentication.

**Q10: What are the secure boot requirements for ISO 21434 (automotive) CAL 4?**

**A10:**
CAL 4 (highest cybersecurity assurance level) requires:
1. **Cryptographic Verification:** Digital signatures (ECDSA-256 or stronger)
2. **Chain of Trust:** From immutable RoT to all software components
3. **Anti-Rollback:** Prevent installation of vulnerable firmware versions
4. **Secure Key Storage:** Hardware-backed (HSM, OTP fuses, not software)
5. **Tamper Detection:** Monitor voltage, clock, temperature during boot
6. **Fail-Safe:** System halts on any verification failure (no bypass)
7. **Documentation:** Security architecture, threat model, verification evidence
8. **Testing:** Penetration testing, fuzzing, fault injection validation

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 1.0  
**Word count:** ~5,200 words | ~900 lines
