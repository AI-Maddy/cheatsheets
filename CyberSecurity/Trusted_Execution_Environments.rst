🏛️ **TRUSTED EXECUTION ENVIRONMENTS (TEE) — Isolated Security Worlds**
═══════════════════════════════════════════════════════════════════════

**Hardware-Enforced Isolation for Security-Critical Code & Data**  
**Purpose:** Secure computation 🔐 | Trusted applications 📱 | Key protection 🔑  
**Domains:** Mobile 📱 | Automotive 🚗 | IoT 📡 | Payment 💳 | DRM 🎬

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

A **Trusted Execution Environment (TEE)** is a hardware-isolated secure area within a main processor that guarantees code and data confidentiality, integrity, and authentication. Think of it as a "secure vault" inside your CPU that even the operating system cannot access.

**Key Equation:** `Normal World (Linux/Android) + Secure World (TEE) = Complete System`

**Real-World Impact:** Enables mobile payments (Apple Pay, Google Pay), biometric authentication (Face ID, fingerprint), DRM content protection, automotive key storage. Over **3 billion** devices use ARM TrustZone TEE.

════════════════════════════════════════════════════════════════════════════

🎯 **TEE FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**What is a TEE?**

A TEE provides:
1. **🔐 Isolated Execution** – Security-sensitive code runs in protected environment
2. **💾 Secure Storage** – Data protected from normal OS access
3. **🔒 Cryptographic Services** – Key management, encryption/decryption
4. **🛡️ Attestation** – Prove code integrity to remote parties

**TEE vs Other Security Technologies:**

| Technology | Isolation Level | Performance | Use Case |
|:-----------|:----------------|:------------|:---------|
| 🏛️ **TEE** | Hardware-enforced | Near-native | Mobile payments, DRM, automotive |
| 🔒 **HSM** | Separate chip | Medium (I/O overhead) | Banking, PKI, key management |
| 🧱 **Secure Enclave** | Dedicated CPU core | High | Apple devices (Face ID, Secure Boot) |
| 💻 **SGX** | CPU enclave | High | Cloud confidential computing |
| 🔐 **SE** | Smart card chip | Low (serial interface) | SIM cards, payment cards |

**GlobalPlatform TEE Architecture:**

```
┌────────────────────────────────────────────────────────────────┐
│                        NORMAL WORLD                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Android OS   │  │  Linux       │  │  Rich Apps   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                 │
│  ┌──────▼──────────────────▼──────────────────▼─────────┐     │
│  │        Client Application (CA)                        │     │
│  │        Calls Trusted App via GP TEE API               │     │
│  └───────────────────────┬───────────────────────────────┘     │
└──────────────────────────┼─────────────────────────────────────┘
                           │ SMC (Secure Monitor Call)
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│                        SECURE WORLD                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │            TEE OS (OP-TEE, Trustonic, QSEE)            │    │
│  └──────┬────────────┬────────────┬────────────┬─────────┘    │
│         │            │            │            │                │
│  ┌──────▼─────┐ ┌───▼─────┐ ┌───▼─────┐ ┌───▼─────┐          │
│  │  TA: Keys  │ │ TA: DRM │ │TA:Crypto│ │ TA:Auth │          │
│  │  Storage   │ │ Content │ │ Engine  │ │ (Biom.) │          │
│  └────────────┘ └─────────┘ └─────────┘ └─────────┘          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │      Secure Hardware (Crypto accelerator, TRNG)      │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

════════════════════════════════════════════════════════════════════════════

🔐 **ARM TRUSTZONE**
─────────────────────────────────────────────────────────────────────────

**Architecture Overview:**

ARM TrustZone divides the system into two worlds:
- **Normal World (NS=1):** Rich OS (Linux, Android, RTOS)
- **Secure World (NS=0):** TEE OS and Trusted Applications

**Hardware Security Features:**

1. **🔒 NS-bit in Memory** – All bus transactions tagged as Secure/Non-Secure
2. **🧱 TZASC (TrustZone Address Space Controller)** – Partitions memory
3. **🔐 TZPC (TrustZone Protection Controller)** – Partitions peripherals
4. **🔑 Secure Configuration Register (SCR)** – Controls world switching

**TrustZone for Cortex-A (Application Processors):**

.. code-block:: c

   // Cortex-A: Switch from Normal World to Secure World
   // This happens via SMC (Secure Monitor Call) instruction
   
   // Normal World Code (Linux kernel driver)
   #include <linux/arm-smccc.h>
   
   uint32_t call_trusted_app(uint32_t cmd, uint32_t param) {
       struct arm_smccc_res res;
       
       // SMC call: switch to Secure World
       arm_smccc_smc(
           TRUSTED_APP_CMD,  // Function ID
           cmd,              // Command
           param,            // Parameter
           0, 0, 0, 0, 0,    // Additional params
           &res              // Result
       );
       
       return res.a0; // Return value from Secure World
   }
   
   // Secure World Code (OP-TEE Trusted App)
   #include <tee_internal_api.h>
   
   TEE_Result TA_InvokeCommandEntryPoint(
       void *session,
       uint32_t cmd,
       uint32_t param_types,
       TEE_Param params[4])
   {
       switch (cmd) {
           case CMD_ENCRYPT_DATA:
               return do_secure_encryption(params);
           case CMD_STORE_KEY:
               return store_secure_key(params);
           default:
               return TEE_ERROR_BAD_PARAMETERS;
       }
   }

**TrustZone for Cortex-M (Microcontrollers):**

ARM v8-M architecture adds TrustZone-M for microcontrollers:

.. code-block:: c

   // Cortex-M33: TrustZone-M Security Attribution Unit (SAU)
   // Configure memory regions as Secure or Non-Secure
   
   void configure_trustzone_m(void) {
       // Enable SAU
       SAU->CTRL = SAU_CTRL_ENABLE_Msk;
       
       // Region 0: Secure Flash (0x00000000 - 0x0007FFFF)
       SAU->RNR = 0;  // Region Number Register
       SAU->RBAR = 0x00000000;  // Base address
       SAU->RLAR = (0x0007FFFF & SAU_RLAR_LADDR_Msk) | 
                   SAU_RLAR_ENABLE_Msk;  // Secure
       
       // Region 1: Non-Secure Flash (0x00080000 - 0x000FFFFF)
       SAU->RNR = 1;
       SAU->RBAR = 0x00080000 | SAU_RBAR_NSC_Msk;  // Non-Secure Callable
       SAU->RLAR = (0x000FFFFF & SAU_RLAR_LADDR_Msk) | 
                   SAU_RLAR_ENABLE_Msk;
       
       // Region 2: Secure RAM (0x20000000 - 0x2001FFFF)
       SAU->RNR = 2;
       SAU->RBAR = 0x20000000;
       SAU->RLAR = (0x2001FFFF & SAU_RLAR_LADDR_Msk) | 
                   SAU_RLAR_ENABLE_Msk;
   }
   
   // Secure function callable from Non-Secure world
   __attribute__((cmse_nonsecure_entry))
   uint32_t secure_encrypt(uint8_t *data, uint32_t len) {
       // This function can be called from Non-Secure code
       // But executes with Secure privileges
       return crypto_engine_encrypt(data, len);
   }

**Memory Partitioning Example:**

```
Physical Memory Map with TrustZone:

0xFFFFFFFF ┌─────────────────────────────┐
           │   Secure Peripherals        │ ← Crypto engine, TRNG
           │   (NS=0 only)               │
0xE0000000 ├─────────────────────────────┤
           │   Normal Peripherals        │ ← UART, GPIO, timers
           │   (NS=1 accessible)         │
0x40000000 ├─────────────────────────────┤
           │   Non-Secure RAM            │ ← Linux/Android uses this
0x30000000 ├─────────────────────────────┤
           │   Secure RAM                │ ← TEE OS and TAs only
0x20000000 ├─────────────────────────────┤
           │   Non-Secure Flash          │ ← Normal OS code
0x08000000 ├─────────────────────────────┤
           │   Secure Flash              │ ← Secure boot, TEE code
0x00000000 └─────────────────────────────┘
```

════════════════════════════════════════════════════════════════════════════

🍎 **APPLE SECURE ENCLAVE**
─────────────────────────────────────────────────────────────────────────

**Architecture:**

The Secure Enclave is a dedicated **Secure Enclave Processor (SEP)** (ARM core) with:
- Separate boot ROM and OS (sepOS)
- Encrypted memory
- Direct access to cryptographic accelerators
- Isolated from main application processor

**Security Features:**

1. **🔑 UID (Unique ID)** – Device-specific 256-bit key fused during manufacturing
2. **🔐 GID (Group ID)** – Processor class key (shared across same chip family)
3. **💾 Secure Storage** – Data encrypted with UID (cannot move to another device)
4. **🔒 Secure Boot** – Independent boot chain from main CPU

**Use Cases:**

- **Touch ID / Face ID:** Biometric data never leaves Secure Enclave
- **Apple Pay:** Payment credentials stored in Secure Enclave
- **Secure Boot:** Stores boot nonce (anti-replay)
- **Encrypted Storage:** FileVault, iOS Data Protection

**Data Protection Example:**

.. code-block:: swift

   // iOS: Store sensitive data with Secure Enclave protection
   import Security
   
   func storeSecureKey() {
       // Create key in Secure Enclave (cannot be exported)
       let access = SecAccessControlCreateWithFlags(
           kCFAllocatorDefault,
           kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
           .privateKeyUsage,
           nil
       )
       
       let keyAttributes: [String: Any] = [
           kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
           kSecAttrKeySizeInBits as String: 256,
           kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
           kSecPrivateKeyAttrs as String: [
               kSecAttrIsPermanent as String: true,
               kSecAttrApplicationTag as String: "com.example.key",
               kSecAttrAccessControl as String: access!
           ]
       ]
       
       var error: Unmanaged<CFError>?
       guard let privateKey = SecKeyCreateRandomKey(
           keyAttributes as CFDictionary,
           &error
       ) else {
           print("Failed to create key: \(error!.takeRetainedValue())")
           return
       }
       
       // Key is now stored in Secure Enclave, protected by UID
       print("Secure key created successfully")
   }

════════════════════════════════════════════════════════════════════════════

💻 **INTEL SGX (SOFTWARE GUARD EXTENSIONS)**
─────────────────────────────────────────────────────────────────────────

**Enclave Model:**

Intel SGX creates **enclaves** – isolated memory regions protected from:
- Operating system
- Hypervisor
- BIOS/firmware
- Other applications

**Key Features:**

1. **🔐 Memory Encryption (MEE)** – Enclave memory encrypted with CPU key
2. **✅ Attestation** – Prove enclave code integrity to remote parties
3. **🛡️ Sealing** – Encrypt data for persistent storage
4. **🔒 Protected Mode** – CPU enforces access control

**Enclave Lifecycle:**

.. code-block:: c

   // Intel SGX: Create and use enclave
   #include <sgx_urts.h>
   #include <sgx_tcrypto.h>
   
   // Untrusted application (normal code)
   int main() {
       sgx_enclave_id_t eid;
       sgx_status_t ret;
       
       // 1. Create enclave
       ret = sgx_create_enclave(
           "enclave.signed.so",  // Signed enclave binary
           SGX_DEBUG_FLAG,
           NULL,
           NULL,
           &eid,
           NULL
       );
       
       if (ret != SGX_SUCCESS) {
           printf("Failed to create enclave\n");
           return -1;
       }
       
       // 2. Call enclave function (ECALL)
       uint8_t plaintext[] = "Secret data";
       uint8_t ciphertext[128];
       size_t cipher_len;
       
       ret = ecall_encrypt_data(
           eid,
           plaintext, sizeof(plaintext),
           ciphertext, sizeof(ciphertext),
           &cipher_len
       );
       
       // 3. Destroy enclave
       sgx_destroy_enclave(eid);
       
       return 0;
   }
   
   // Trusted code (inside enclave) - enclave.c
   #include <sgx_trts.h>
   #include <sgx_tcrypto.h>
   
   sgx_status_t ecall_encrypt_data(
       uint8_t *plaintext, size_t plain_len,
       uint8_t *ciphertext, size_t cipher_max,
       size_t *cipher_len)
   {
       // This code runs in protected enclave memory
       
       // Generate random key (inside enclave)
       sgx_aes_gcm_128bit_key_t key;
       sgx_read_rand((uint8_t *)&key, sizeof(key));
       
       // Encrypt data
       uint8_t iv[12] = {0};
       uint8_t mac[16];
       
       sgx_status_t ret = sgx_rijndael128GCM_encrypt(
           &key,
           plaintext, plain_len,
           ciphertext,
           iv, 12,
           NULL, 0,  // No AAD
           (sgx_aes_gcm_128bit_tag_t *)mac
       );
       
       *cipher_len = plain_len + sizeof(mac);
       return ret;
   }

**Remote Attestation:**

SGX enables proving to a remote server that code is running in genuine enclave:

.. code-block:: python

   # Intel SGX Remote Attestation (simplified)
   import requests
   
   # 1. Generate quote (signed enclave measurement)
   quote = sgx_get_quote(enclave_id, report_data)
   
   # 2. Send quote to Intel Attestation Service (IAS)
   response = requests.post(
       "https://api.trustedservices.intel.com/sgx/dev/attestation/v4/report",
       headers={"Content-Type": "application/json"},
       json={"isvEnclaveQuote": quote}
   )
   
   # 3. IAS returns signed verification report
   verification_report = response.json()
   
   # 4. Send report to relying party (your server)
   server_response = requests.post(
       "https://your-server.com/verify",
       json={"attestation": verification_report}
   )
   
   # Server now trusts this enclave and can send secrets

════════════════════════════════════════════════════════════════════════════

🔧 **TEE IMPLEMENTATIONS**
─────────────────────────────────────────────────────────────────────────

**OP-TEE (Open Portable TEE)**

Open-source TEE OS implementing GlobalPlatform APIs:

.. code-block:: c

   // OP-TEE Trusted Application Example
   #include <tee_internal_api.h>
   #include <tee_internal_api_extensions.h>
   
   TEE_Result TA_CreateEntryPoint(void) {
       // Initialize TA
       return TEE_SUCCESS;
   }
   
   TEE_Result TA_OpenSessionEntryPoint(
       uint32_t param_types,
       TEE_Param params[4],
       void **sess_ctx)
   {
       // Open session with client
       return TEE_SUCCESS;
   }
   
   TEE_Result TA_InvokeCommandEntryPoint(
       void *sess_ctx,
       uint32_t cmd_id,
       uint32_t param_types,
       TEE_Param params[4])
   {
       switch (cmd_id) {
           case CMD_GENERATE_KEY:
               return generate_secure_key(params);
               
           case CMD_SIGN_DATA:
               return sign_with_secure_key(params);
               
           case CMD_VERIFY_SIGNATURE:
               return verify_signature(params);
               
           default:
               return TEE_ERROR_BAD_PARAMETERS;
       }
   }
   
   static TEE_Result generate_secure_key(TEE_Param params[4]) {
       TEE_ObjectHandle key_handle;
       TEE_Result res;
       
       // Generate ECDSA P-256 key pair
       res = TEE_AllocateTransientObject(
           TEE_TYPE_ECDSA_KEYPAIR,
           256,  // Key size
           &key_handle
       );
       if (res != TEE_SUCCESS) return res;
       
       res = TEE_GenerateKey(
           key_handle,
           256,
           NULL, 0
       );
       if (res != TEE_SUCCESS) {
           TEE_FreeTransientObject(key_handle);
           return res;
       }
       
       // Store key in secure storage
       TEE_ObjectHandle persistent_key;
       res = TEE_CreatePersistentObject(
           TEE_STORAGE_PRIVATE,
           "signing_key", 11,
           TEE_DATA_FLAG_ACCESS_WRITE,
           key_handle,
           NULL, 0,
           &persistent_key
       );
       
       TEE_CloseObject(persistent_key);
       TEE_FreeTransientObject(key_handle);
       
       return res;
   }

**Qualcomm QSEE (Qualcomm Secure Execution Environment)**

Proprietary TEE used in Snapdragon SoCs:
- Integrated with Android Keystore
- Supports Widevine DRM (L1)
- Secure boot and attestation

**Trustonic Kinibi**

Commercial TEE solution:
- Used in Samsung devices
- FIPS 140-2 Level 2 certified
- Supports GlobalPlatform APIs

════════════════════════════════════════════════════════════════════════════

🚗 **TEE IN AUTOMOTIVE**
─────────────────────────────────────────────────────────────────────────

**Use Cases:**

1. **🔑 V2X Certificate Storage** – Secure storage for vehicle-to-everything credentials
2. **🔐 Secure OTA Updates** – Verify and apply firmware updates
3. **🛡️ AUTOSAR SecOC** – Message authentication using TEE-stored keys
4. **📡 Infotainment Security** – DRM content protection

**Example: V2X Key Management**

.. code-block:: c

   // AUTOSAR: Use HSM (TEE-like) for V2X certificate storage
   #include "Crypto.h"
   #include "Csm.h"
   
   Std_ReturnType V2X_SignMessage(
       const uint8 *message,
       uint32 msg_len,
       uint8 *signature,
       uint32 *sig_len)
   {
       Csm_ReturnType result;
       
       // Use Crypto Service Manager to access HSM/TEE
       result = Csm_SignatureGenerate(
           CSM_KEY_V2X_SIGNING,  // Key stored in HSM
           message,
           msg_len,
           signature,
           sig_len
       );
       
       return (result == CSM_E_OK) ? E_OK : E_NOT_OK;
   }

**ISO 21434 Requirements:**

- CAL 3-4 requires hardware-backed key storage (TEE/HSM)
- Cryptographic operations in isolated environment
- Protection against side-channel attacks

════════════════════════════════════════════════════════════════════════════

🏥 **TEE IN MEDICAL DEVICES**
─────────────────────────────────────────────────────────────────────────

**FDA Guidance Alignment:**

TEE addresses multiple cybersecurity requirements:
1. **Authentication** – Biometric authentication using TEE
2. **Key Storage** – Patient data encryption keys in TEE
3. **Secure Boot** – Boot chain verification via TEE
4. **Attestation** – Prove device integrity to hospital systems

**Example: Insulin Pump with TEE**

.. code-block:: c

   // Medical device: Secure dosing control via TEE
   typedef struct {
       uint32_t patient_id;
       float basal_rate;      // Units/hour
       float bolus_amount;    // Units
       uint8_t signature[64]; // ECDSA signature
   } DoseCommand;
   
   // Normal World: UI and communication
   bool send_dose_command(DoseCommand *cmd) {
       // 1. Sign command in TEE
       if (!tee_sign_dose_command(cmd)) {
           log_error("Failed to sign dose command");
           return false;
       }
       
       // 2. Send to pump controller (also verifies in TEE)
       return transmit_to_pump(cmd);
   }
   
   // Secure World (TEE): Verify and execute dose
   TEE_Result verify_and_dose(DoseCommand *cmd) {
       // 1. Verify signature
       if (!verify_dose_signature(cmd)) {
           return TEE_ERROR_SECURITY;
       }
       
       // 2. Check safety limits (in TEE, cannot be bypassed)
       if (cmd->bolus_amount > MAX_BOLUS_LIMIT) {
           alarm_trigger("Bolus exceeds safety limit");
           return TEE_ERROR_BAD_PARAMETERS;
       }
       
       // 3. Execute dose command
       return pump_deliver_insulin(cmd->bolus_amount);
   }

════════════════════════════════════════════════════════════════════════════

🛡️ **TEE SECURITY CONSIDERATIONS**
─────────────────────────────────────────────────────────────────────────

**Attack Vectors:**

**1. 🔴 Side-Channel Attacks**
   - **Threat:** Leak secrets via timing, power, EM radiation
   - **Example:** Spectre/Meltdown on SGX enclaves
   - **Mitigation:** Constant-time crypto, data-independent control flow

**2. 🔴 Rollback Attacks**
   - **Threat:** Restore old TEE state with known vulnerabilities
   - **Mitigation:** Secure replay-protected memory (RPMB), monotonic counters

**3. 🟠 Physical Attacks**
   - **Threat:** Invasive attacks on secure memory
   - **Mitigation:** Encrypted memory (SGX MEE), tamper detection

**4. 🟠 Malicious TEE OS/TA**
   - **Threat:** Compromised Trusted Application
   - **Mitigation:** TA code signing, OP-TEE signature verification

**5. 🟡 Interface Attacks**
   - **Threat:** Attack via Normal World ↔ Secure World interface
   - **Mitigation:** Input validation in TEE, minimize attack surface

**Best Practices:**

.. code-block:: c

   // ✅ GOOD: Validate all inputs from Normal World
   TEE_Result secure_function(uint8_t *buffer, size_t len) {
       // 1. Check pointer is in Normal World memory
       if (!TEE_CheckMemoryAccessRights(
               TEE_MEMORY_ACCESS_READ | TEE_MEMORY_ACCESS_ANY_OWNER,
               buffer, len)) {
           return TEE_ERROR_BAD_PARAMETERS;
       }
       
       // 2. Validate size limits
       if (len > MAX_BUFFER_SIZE) {
           return TEE_ERROR_BAD_PARAMETERS;
       }
       
       // 3. Copy to Secure World memory (prevent TOCTOU)
       uint8_t secure_buffer[MAX_BUFFER_SIZE];
       TEE_MemMove(secure_buffer, buffer, len);
       
       // 4. Process data securely
       return process_data(secure_buffer, len);
   }
   
   // ❌ BAD: Directly using Normal World pointer
   TEE_Result insecure_function(uint8_t *buffer, size_t len) {
       // Normal World could modify buffer during processing (TOCTOU!)
       return process_data(buffer, len);  // VULNERABLE!
   }

════════════════════════════════════════════════════════════════════════════

📊 **COMPLIANCE & STANDARDS**
─────────────────────────────────────────────────────────────────────────

| Standard | Requirement | TEE Implementation |
|:---------|:------------|:-------------------|
| 🚗 **ISO 21434** | CAL 3-4: Hardware-backed key storage | TrustZone for automotive ECUs |
| 🏭 **IEC 62443-4-2** | SR 1.1-1.13: Authentication, crypto | TEE for industrial controllers |
| 🏥 **FDA Guidance** | Secure key storage, authentication | TEE in connected medical devices |
| 💳 **PCI DSS** | Key management, secure crypto | TEE for payment terminals |
| 📱 **FIDO2** | Biometric authentication | TEE for fingerprint/face data |
| 🌐 **GlobalPlatform** | TEE API specifications | OP-TEE, QSEE, Trustonic |

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Explain the difference between TrustZone for Cortex-A and TrustZone-M for Cortex-M.**

**A1:**
- **Cortex-A (TrustZone):** Application processors with rich OS (Linux/Android). Uses Secure Monitor (EL3) to switch between worlds via SMC instruction. Supports complex TEE OS (OP-TEE) with multiple Trusted Apps.
- **Cortex-M (TrustZone-M):** Microcontrollers with RTOS. Uses SAU (Security Attribution Unit) and IDAU to partition memory. Simpler model: Secure callable functions (NSC) instead of full TEE OS. Lower overhead, suitable for resource-constrained IoT.

**Q2: How does Intel SGX differ from ARM TrustZone?**

**A2:**
| Aspect | **Intel SGX** | **ARM TrustZone** |
|:-------|:--------------|:------------------|
| **Granularity** | Per-application enclaves | Two system-wide worlds |
| **OS Trust** | Doesn't trust OS/hypervisor | Trusts Secure World OS |
| **Memory** | Encrypted (MEE) | Isolated (NS-bit) |
| **Attestation** | Remote attestation (IAS) | Local attestation |
| **Use Case** | Cloud confidential computing | Mobile/embedded devices |

**Q3: What is a Secure Monitor Call (SMC) in ARM TrustZone?**

**A3:**
SMC is an instruction that triggers a transition from Normal World to Secure World:
```assembly
; ARM64 assembly
ldr x0, =FUNCTION_ID
ldr x1, =PARAM1
smc #0  ; Triggers SMC exception, switches to Secure World
; Returns to Normal World after Secure World completes
```
CPU switches to Secure Monitor (EL3), which handles the request and returns result to Normal World.

**Q4: How does Apple Secure Enclave protect Face ID data?**

**A4:**
1. Face scan captured by TrueDepth camera
2. **Mathematical model** (not image) sent to Secure Enclave
3. Secure Enclave compares with stored template (never leaves enclave)
4. UID encrypts template (unique per device, cannot extract)
5. Match/no-match result returned to iOS
6. **Face data NEVER accessible to iOS, apps, or Apple**

**Q5: What is RPMB and why is it important for TEE?**

**A5:**
**RPMB (Replay Protected Memory Block)** is secure storage in eMMC/UFS:
- Authenticated writes using HMAC key
- Monotonic counter prevents rollback
- Only TEE can access (via secure channel)
- **Use cases:** Store encryption keys, anti-rollback counters, secure boot state
- **Protection:** Attacker cannot restore old TEE storage even with physical access

**Last updated:** January 14, 2026 | **Version:** 1.0
