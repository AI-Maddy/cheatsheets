====================================================================
ECU Hardening for Automotive and Industrial Control Systems
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 21434, AUTOSAR, IEC 62443, MISRA C

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**ECU (Electronic Control Unit) Hardening Checklist:**

+-----------------------------+------------------------------------------------+
| **Security Control**        | **Implementation**                             |
+=============================+================================================+
| **Secure Boot**             | Verify firmware signature before execution     |
+-----------------------------+------------------------------------------------+
| **Code Signing**            | Only accept signed software updates            |
+-----------------------------+------------------------------------------------+
| **Memory Protection**       | Enable MPU/MMU, stack canaries, ASLR           |
+-----------------------------+------------------------------------------------+
| **Debug Interface Lockdown**| Disable/lock JTAG/SWD in production            |
+-----------------------------+------------------------------------------------+
| **Cryptographic Storage**   | Store keys in HSM or secure flash              |
+-----------------------------+------------------------------------------------+
| **Runtime Integrity**       | Monitor code/data integrity during execution   |
+-----------------------------+------------------------------------------------+
| **Secure Communication**    | Use SecOC (AUTOSAR) for CAN authentication     |
+-----------------------------+------------------------------------------------+
| **Fail-Safe Design**        | Safe state on security violation               |
+-----------------------------+------------------------------------------------+

**Typical Automotive ECU Architecture:**

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │         Application Layer                       │
    │  (Control algorithms, diagnostics)              │
    ├─────────────────────────────────────────────────┤
    │         AUTOSAR Runtime (RTE)                   │
    ├─────────────────────────────────────────────────┤
    │  Basic Software (BSW)                           │
    │  - OS, Communication (CAN, Ethernet)            │
    │  - Memory, I/O drivers                          │
    ├─────────────────────────────────────────────────┤
    │  Hardware Abstraction Layer (HAL)               │
    ├─────────────────────────────────────────────────┤
    │  Microcontroller (MCU)                          │
    │  - CPU (ARM Cortex-M, Cortex-R, PowerPC)        │
    │  - Memory (Flash, RAM, EEPROM)                  │
    │  - Peripherals (CAN, SPI, ADC)                  │
    │  - Security features (MPU, HSM, secure boot)    │
    └─────────────────────────────────────────────────┘

**Attack Surface of an ECU:**

.. code-block:: text

    🔴 ATTACK VECTORS:
    
    1. Network interfaces (CAN, Ethernet, LIN)
    2. OBD-II diagnostic port
    3. Debug interfaces (JTAG, SWD)
    4. Firmware update process (OTA, local)
    5. Supply chain (compromised components)
    6. Side-channel attacks (power analysis, timing)

**ECU Hardening Maturity Levels (ISO 21434):**

+----------+-------------------------------------------+
| Level    | Description                               |
+==========+===========================================+
| **CAL 0**| No cybersecurity measures                 |
+----------+-------------------------------------------+
| **CAL 1**| Basic protections (authentication)        |
+----------+-------------------------------------------+
| **CAL 2**| Standard protections (secure boot, MPU)   |
+----------+-------------------------------------------+
| **CAL 3**| Enhanced protections (HSM, SecOC)         |
+----------+-------------------------------------------+
| **CAL 4**| Maximum protections (formal verification) |
+----------+-------------------------------------------+

Introduction to ECU Hardening
==============================

An **Electronic Control Unit (ECU)** is an embedded system that controls
electrical systems in vehicles, aircraft, industrial machines, and medical
devices. Modern vehicles have 70-150 ECUs controlling:

- **Powertrain**: Engine, transmission, fuel injection
- **Chassis**: ABS, electronic stability control (ESC), power steering
- **Safety**: Airbags, seatbelt pretensioners
- **Body**: Door locks, windows, lighting
- **Infotainment**: Radio, navigation, connectivity

**Why ECU Hardening Matters:**

- **Safety**: Compromised braking or steering ECU can cause accidents
- **Privacy**: Telematics ECU stores location and driving behavior
- **Compliance**: ISO 21434 (automotive) and IEC 62443 (industrial) mandate
  ECU security
- **Liability**: OEMs are liable for cybersecurity defects (UN R155)

ECU Security Objectives (CIA + Safety)
---------------------------------------

+------------------+----------------------------------------------------+
| Objective        | ECU-Specific Requirements                          |
+==================+====================================================+
| **Confidentiality** | Protect cryptographic keys, calibration data    |
+------------------+----------------------------------------------------+
| **Integrity**    | Prevent unauthorized firmware modifications        |
+------------------+----------------------------------------------------+
| **Availability** | Ensure ECU functions even under attack             |
+------------------+----------------------------------------------------+
| **Safety**       | Fail to a safe state (e.g., engine idles, not     |
|                  | full throttle)                                     |
+------------------+----------------------------------------------------+

Secure Boot for ECUs
=====================

Secure Boot Concept
-------------------

**Secure boot** ensures that only authenticated and authorized firmware runs
on the ECU. The boot process verifies a chain of trust:

.. code-block:: text

    ┌──────────────────────────────────────────────────────────┐
    │  1. ROM Bootloader (immutable, stored in mask ROM)       │
    │     - Verify Stage 1 bootloader signature                │
    │     - Public key embedded in ROM (root of trust)         │
    └──────────────────────────────────────────────────────────┘
                         │
                         ↓ (Signature verified)
    ┌──────────────────────────────────────────────────────────┐
    │  2. Stage 1 Bootloader (in Flash)                        │
    │     - Verify application firmware signature              │
    └──────────────────────────────────────────────────────────┘
                         │
                         ↓ (Signature verified)
    ┌──────────────────────────────────────────────────────────┐
    │  3. Application Firmware                                 │
    │     - Control algorithms, diagnostics, communication     │
    └──────────────────────────────────────────────────────────┘

**If verification fails at any stage:**
- ECU halts boot process
- Enters recovery mode or fail-safe state

Cryptographic Signature Verification
-------------------------------------

**Typical Algorithm: RSA-2048 or ECDSA P-256**

.. code-block:: text

    Firmware Image:
    ┌────────────────────────────┐
    │  Firmware Binary (code)    │
    ├────────────────────────────┤
    │  Signature (RSA/ECDSA)     │  ← Generated by OEM private key
    └────────────────────────────┘
    
    Verification:
    1. Compute hash of firmware binary (SHA-256)
    2. Verify signature using OEM public key (stored in ROM)
    3. If valid: boot; else: halt

**Why RSA-2048 or ECDSA P-256?**

- **RSA-2048**: Widely supported, but slower and larger keys (256 bytes)
- **ECDSA P-256**: Faster, smaller keys (64 bytes), but requires ECC library

**Post-Quantum Consideration:**

- NIST recommends CRYSTALS-Dilithium for post-quantum signatures
- Not yet common in automotive (due to code size and performance)

C Code: Secure Boot Signature Verification (ECDSA)
---------------------------------------------------

.. code-block:: c

    #include <stdint.h>
    #include <string.h>
    #include <mbedtls/ecdsa.h>
    #include <mbedtls/sha256.h>
    
    // Public key (OEM's ECDSA P-256 public key, stored in ROM)
    const uint8_t oem_public_key_x[32] = {
        0x6B, 0x17, 0xD1, 0xF2, 0xE1, 0x2C, 0x42, 0x47,
        // ... (32 bytes total)
    };
    
    const uint8_t oem_public_key_y[32] = {
        0x4F, 0xE3, 0x42, 0xE2, 0xFE, 0x1A, 0x7F, 0x9B,
        // ... (32 bytes total)
    };
    
    // Verify firmware signature before boot
    int secure_boot_verify_firmware(
        const uint8_t *firmware_binary,
        size_t firmware_size,
        const uint8_t *signature_r,  // 32 bytes
        const uint8_t *signature_s   // 32 bytes
    ) {
        mbedtls_ecdsa_context ecdsa;
        mbedtls_mpi r, s;
        uint8_t hash[32];
        int ret;
        
        // Initialize ECDSA context
        mbedtls_ecdsa_init(&ecdsa);
        mbedtls_mpi_init(&r);
        mbedtls_mpi_init(&s);
        
        // Load OEM public key
        mbedtls_ecp_group_load(&ecdsa.grp, MBEDTLS_ECP_DP_SECP256R1);
        mbedtls_mpi_read_binary(&ecdsa.Q.X, oem_public_key_x, 32);
        mbedtls_mpi_read_binary(&ecdsa.Q.Y, oem_public_key_y, 32);
        mbedtls_mpi_lset(&ecdsa.Q.Z, 1);
        
        // Compute SHA-256 hash of firmware
        mbedtls_sha256(firmware_binary, firmware_size, hash, 0);
        
        // Load signature (r, s)
        mbedtls_mpi_read_binary(&r, signature_r, 32);
        mbedtls_mpi_read_binary(&s, signature_s, 32);
        
        // Verify signature
        ret = mbedtls_ecdsa_verify(&ecdsa.grp, hash, 32, &ecdsa.Q, &r, &s);
        
        // Cleanup
        mbedtls_ecdsa_free(&ecdsa);
        mbedtls_mpi_free(&r);
        mbedtls_mpi_free(&s);
        
        if (ret == 0) {
            return 1;  // Signature valid
        } else {
            return 0;  // Signature invalid - HALT BOOT
        }
    }
    
    // Secure boot entry point
    void secure_boot_main(void) {
        extern uint8_t _firmware_start[];  // Linker symbol
        extern uint8_t _firmware_end[];
        extern uint8_t _signature_r[];     // Signature at end of flash
        extern uint8_t _signature_s[];
        
        size_t firmware_size = _firmware_end - _firmware_start;
        
        printf("Secure Boot: Verifying firmware signature...\n");
        
        int valid = secure_boot_verify_firmware(
            _firmware_start, firmware_size,
            _signature_r, _signature_s
        );
        
        if (valid) {
            printf("Secure Boot: Signature valid. Booting firmware...\n");
            // Jump to application firmware
            void (*app_main)(void) = (void (*)(void))_firmware_start;
            app_main();
        } else {
            printf("Secure Boot: SIGNATURE INVALID! Halting.\n");
            // Enter fail-safe mode or recovery
            while (1) {
                // Blink LED to indicate boot failure
                __asm__("wfi");  // Wait for interrupt (low power)
            }
        }
    }

Secure Boot with Hardware Root of Trust
----------------------------------------

**Best Practice:** Use a **Hardware Security Module (HSM)** or **Trusted
Execution Environment (TEE)** to store the public key and perform verification.

**Example: ARM TrustZone for Cortex-M33:**

- Secure Boot code runs in **Secure World**
- Public key stored in **Secure Flash** (inaccessible from Non-Secure World)
- Application firmware runs in **Non-Secure World** after verification

Memory Protection (MPU/MMU)
============================

Why Memory Protection?
-----------------------

Memory protection prevents:

- **Buffer overflow attacks**: Overwrite return address or function pointers
- **Code injection**: Execute attacker-supplied code
- **Privilege escalation**: Access protected memory regions

**Memory Protection Unit (MPU):**

- Available on ARM Cortex-M, Cortex-R, PowerPC
- Divides memory into regions with access permissions (read, write, execute)

**Memory Management Unit (MMU):**

- Available on ARM Cortex-A, x86
- Provides virtual memory, paging, and access control
- More complex than MPU

MPU Configuration for Automotive ECU
-------------------------------------

**Typical MPU Regions:**

+--------+-------------------+-----------+-----------------------------+
| Region | Address Range     | Size      | Permissions                 |
+========+===================+===========+=============================+
| 0      | 0x00000000-...    | 1 MB      | RO (Read-Only) - Flash      |
+--------+-------------------+-----------+-----------------------------+
| 1      | 0x20000000-...    | 128 KB    | RW (Read-Write) - RAM       |
+--------+-------------------+-----------+-----------------------------+
| 2      | 0x20020000-...    | 16 KB     | RW, No Execute - Stack      |
+--------+-------------------+-----------+-----------------------------+
| 3      | 0x40000000-...    | 1 MB      | RW, Device - Peripherals    |
+--------+-------------------+-----------+-----------------------------+
| 4      | 0x08000000-...    | 64 KB     | RO - Bootloader (protected) |
+--------+-------------------+-----------+-----------------------------+

**Security Benefits:**

- **Region 0 (Flash)**: Read-only prevents firmware tampering
- **Region 2 (Stack)**: No-execute prevents stack-based code injection
- **Region 4 (Bootloader)**: Protected from application firmware

C Code: MPU Configuration (ARM Cortex-M)
-----------------------------------------

.. code-block:: c

    #include <stdint.h>
    #include "stm32f4xx.h"  // Or equivalent for your MCU
    
    // MPU Region configuration
    typedef struct {
        uint32_t base_address;
        uint32_t size;         // Size code (2^(size+1) bytes)
        uint32_t permissions;  // Access permissions
        uint8_t  region_num;
    } mpu_region_t;
    
    // MPU permission bits
    #define MPU_RO      (0x05 << 24)  // Read-only
    #define MPU_RW      (0x03 << 24)  // Read-write
    #define MPU_NO_EXEC (1 << 28)     // No execute (XN bit)
    
    void mpu_configure_region(const mpu_region_t *region) {
        // Disable MPU during configuration
        MPU->CTRL = 0;
        
        // Set region number
        MPU->RNR = region->region_num;
        
        // Set base address and region size
        MPU->RBAR = region->base_address;
        MPU->RASR = (1 << 0) |          // Enable region
                    (region->size << 1) | // Size
                    region->permissions;
        
        // Enable MPU with default background region (for peripherals)
        MPU->CTRL = (1 << 0) |  // Enable MPU
                    (1 << 2);   // Enable default memory map for privileged access
    }
    
    void mpu_init(void) {
        mpu_region_t regions[] = {
            // Region 0: Flash (Read-Only, Execute)
            {
                .base_address = 0x08000000,
                .size = 19,  // 2^20 = 1 MB
                .permissions = MPU_RO,
                .region_num = 0
            },
            
            // Region 1: RAM (Read-Write, Execute)
            {
                .base_address = 0x20000000,
                .size = 16,  // 2^17 = 128 KB
                .permissions = MPU_RW,
                .region_num = 1
            },
            
            // Region 2: Stack (Read-Write, No Execute)
            {
                .base_address = 0x20020000,
                .size = 13,  // 2^14 = 16 KB
                .permissions = MPU_RW | MPU_NO_EXEC,
                .region_num = 2
            },
            
            // Region 3: Bootloader (Read-Only, Execute, Protected)
            {
                .base_address = 0x08000000,
                .size = 15,  // 2^16 = 64 KB
                .permissions = MPU_RO,  // Privileged access only
                .region_num = 3
            },
        };
        
        for (int i = 0; i < sizeof(regions)/sizeof(mpu_region_t); i++) {
            mpu_configure_region(&regions[i]);
        }
        
        printf("MPU configured: 4 regions enabled\n");
    }

Stack Protection Mechanisms
----------------------------

**1. Stack Canaries (Compiler Feature):**

.. code-block:: c

    // Enable with GCC: -fstack-protector-all
    void vulnerable_function(const char *input) {
        char buffer[64];
        strcpy(buffer, input);  // Potential buffer overflow
        // Compiler inserts canary check here
    }

**Canary Mechanism:**

- Compiler places a random value (canary) before return address
- Before function returns, canary is checked
- If modified (buffer overflow), program terminates

**2. Address Space Layout Randomization (ASLR):**

- Randomize base addresses of stack, heap, libraries
- Makes ROP (Return-Oriented Programming) attacks harder
- Less common in embedded systems (limited RAM, performance overhead)

Debug Interface Lockdown
=========================

Debug Interfaces as Attack Vectors
-----------------------------------

**JTAG (Joint Test Action Group):**

- Hardware debugging interface (4-5 pins: TDI, TDO, TMS, TCK, TRST)
- Allows:
  
  - Read/write memory
  - Single-step execution
  - Flash programming

**SWD (Serial Wire Debug):**

- ARM-specific (2 pins: SWDIO, SWCLK)
- Similar capabilities to JTAG, but fewer pins

**Attack Scenario:**

1. Attacker gains physical access to ECU
2. Connects JTAG/SWD debugger (e.g., ST-Link, J-Link)
3. Reads Flash memory (extracts firmware and keys)
4. Modifies firmware or calibration data

Debug Lockdown Strategies
--------------------------

**Strategy 1: Disable Debug Interfaces in Production**

.. code-block:: c

    // Disable JTAG/SWD (ARM Cortex-M)
    void disable_debug_interface(void) {
        // Disable JTAG and SWD
        DBGMCU->CR = 0;  // Disable debug in sleep/stop/standby modes
        
        // Disable trace (SWO)
        CoreDebug->DEMCR = 0;
        
        // Optionally: Blow fuse to permanently disable debug
        // (This is MCU-specific and irreversible)
    }

**Strategy 2: Password-Protected Debug Access**

- Debug interface requires authentication (password or challenge-response)
- ARM Debug Authentication Protocol (DAP)

**Strategy 3: Tamper Detection**

- Monitor debug pins for activity
- If debug interface accessed without authorization, erase keys

**Strategy 4: Physical Protection**

- Epoxy resin over debug pads
- Remove debug header from production PCBs

JTAG Lockdown Example (STM32)
------------------------------

.. code-block:: c

    #include "stm32f4xx.h"
    
    // Lock JTAG/SWD debug interface
    void lock_debug_interface(void) {
        // Option 1: Disable JTAG/SWD via RDP (Read Protection)
        // Level 1: Debug disabled, Flash readable only after mass erase
        // Level 2: Debug permanently disabled (irreversible!)
        
        FLASH_OBProgramInitTypeDef ob_config;
        HAL_FLASHEx_OBGetConfig(&ob_config);
        
        if (ob_config.RDPLevel == OB_RDP_LEVEL_0) {
            // Set Read Protection Level 1 (reversible)
            ob_config.RDPLevel = OB_RDP_LEVEL_1;
            HAL_FLASH_Unlock();
            HAL_FLASH_OB_Unlock();
            HAL_FLASHEx_OBProgram(&ob_config);
            HAL_FLASH_OB_Launch();  // Requires system reset
            HAL_FLASH_OB_Lock();
            HAL_FLASH_Lock();
        }
    }

Cryptographic Key Storage
==========================

Key Storage Options
-------------------

+----------------------+------------------+----------------------------------+
| Storage Method       | Security Level   | Typical Use Case                 |
+======================+==================+==================================+
| **Flash (plaintext)**| ❌ Low           | NOT RECOMMENDED                  |
+----------------------+------------------+----------------------------------+
| **Encrypted Flash**  | ⚠️  Medium       | Key encrypted with KEK           |
+----------------------+------------------+----------------------------------+
| **OTP (One-Time      | ✅ High          | Root keys (immutable)            |
| Programmable)**      |                  |                                  |
+----------------------+------------------+----------------------------------+
| **HSM (Hardware      | ✅✅ Very High   | Production ECUs (EVITA HSM)      |
| Security Module)**   |                  |                                  |
+----------------------+------------------+----------------------------------+
| **PUF (Physical      | ✅✅ Very High   | Emerging (device-specific key)   |
| Unclonable Function)**|                 |                                  |
+----------------------+------------------+----------------------------------+

Hardware Security Module (HSM) for Automotive
----------------------------------------------

**EVITA HSM (AUTOSAR Standard):**

- Secure cryptographic co-processor
- Key storage, AES/RSA/ECC acceleration
- Tamper-resistant (side-channel countermeasures)

**HSM Services:**

- Key generation and storage
- Symmetric encryption (AES-128/256)
- Asymmetric encryption (RSA-2048, ECDSA P-256)
- Secure boot (signature verification)
- SecOC MAC generation

**Example: Infineon AURIX TC3xx with HSM**

.. code-block:: c

    #include "hsm_api.h"  // Vendor-specific HSM library
    
    // Generate and store AES key in HSM
    int hsm_generate_aes_key(uint32_t key_id) {
        hsm_key_info_t key_info = {
            .key_id = key_id,
            .key_type = HSM_KEY_TYPE_AES_128,
            .usage = HSM_KEY_USAGE_ENCRYPT | HSM_KEY_USAGE_DECRYPT,
            .exportable = 0  // Key cannot be exported
        };
        
        // Generate key in HSM (never exposed to CPU)
        int ret = hsm_generate_key(&key_info);
        if (ret != HSM_OK) {
            return -1;
        }
        
        printf("AES key generated in HSM (ID=%u)\n", key_id);
        return 0;
    }
    
    // Encrypt data using HSM key
    int hsm_encrypt_data(uint32_t key_id, const uint8_t *plaintext, 
                         size_t len, uint8_t *ciphertext) {
        hsm_cipher_ctx_t ctx;
        
        // Initialize cipher context with HSM key
        hsm_cipher_init(&ctx, HSM_CIPHER_AES_128_CBC, key_id);
        
        // Encrypt (HSM performs encryption, key never leaves HSM)
        hsm_cipher_encrypt(&ctx, plaintext, len, ciphertext);
        
        // Cleanup
        hsm_cipher_free(&ctx);
        
        return 0;
    }

Key Derivation for Multi-ECU Systems
-------------------------------------

**Problem:**

Each ECU needs unique keys, but provisioning individual keys is expensive.

**Solution: Key Derivation Function (KDF)**

.. code-block:: text

    Master Key (stored in HSM at factory)
         │
         ├─ KDF(Master, ECU_ID_1) → Key for ECU 1
         ├─ KDF(Master, ECU_ID_2) → Key for ECU 2
         └─ KDF(Master, ECU_ID_N) → Key for ECU N

.. code-block:: c

    #include <mbedtls/hkdf.h>
    
    // Derive ECU-specific key from master key
    int derive_ecu_key(
        const uint8_t *master_key,  // 256-bit master key
        const uint8_t *ecu_id,      // Unique ECU identifier (VIN + ECU address)
        size_t ecu_id_len,
        uint8_t *derived_key        // Output: 128-bit AES key
    ) {
        const mbedtls_md_info_t *md = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
        
        // HKDF-Expand (RFC 5869)
        int ret = mbedtls_hkdf_expand(
            md,
            master_key, 32,      // Input keying material
            ecu_id, ecu_id_len,  // Context-specific info
            derived_key, 16      // Output key length (128 bits)
        );
        
        if (ret != 0) {
            return -1;
        }
        
        printf("Derived key for ECU ID: ");
        for (size_t i = 0; i < ecu_id_len; i++) {
            printf("%02X", ecu_id[i]);
        }
        printf("\n");
        
        return 0;
    }

Runtime Integrity Monitoring
=============================

Why Runtime Integrity Matters
------------------------------

Secure boot verifies firmware **before execution**, but does not protect
against:

- **Memory corruption attacks** (buffer overflow at runtime)
- **Return-Oriented Programming (ROP)**
- **Fault injection** (voltage glitching, clock glitching)

**Runtime Integrity Monitoring** detects tampering during execution.

Control Flow Integrity (CFI)
-----------------------------

**Control Flow Integrity** ensures that program execution follows valid paths
(no jumping to arbitrary code).

**Techniques:**

1. **Return Address Validation**: Check that return address is valid
2. **Indirect Call Validation**: Check that function pointer is valid
3. **Shadow Stack**: Duplicate call stack in protected memory

**GCC/Clang Support:**

.. code-block:: bash

    # Enable CFI (Clang)
    clang -fsanitize=cfi -flto -fvisibility=hidden -o firmware firmware.c

Watchdog Timers for Availability
---------------------------------

**Watchdog Timer (WDT):**

- Hardware timer that resets ECU if not periodically refreshed
- Detects software hangs (infinite loops, crashes)

.. code-block:: c

    #include "stm32f4xx.h"
    
    // Initialize independent watchdog (IWDG)
    void watchdog_init(uint32_t timeout_ms) {
        // Enable write access to IWDG registers
        IWDG->KR = 0x5555;
        
        // Set prescaler (40 kHz clock / 256 = 156.25 Hz)
        IWDG->PR = IWDG_PR_PR_6;  // Prescaler = 256
        
        // Set reload value (timeout = reload / 156.25 Hz)
        uint32_t reload = (timeout_ms * 156.25) / 1000;
        IWDG->RLR = reload;
        
        // Start watchdog
        IWDG->KR = 0xCCCC;
        
        printf("Watchdog initialized: %u ms timeout\n", timeout_ms);
    }
    
    // Refresh watchdog (call periodically in main loop)
    void watchdog_refresh(void) {
        IWDG->KR = 0xAAAA;  // Reload counter
    }
    
    // Main loop with watchdog
    int main(void) {
        watchdog_init(1000);  // 1-second timeout
        
        while (1) {
            // Perform control tasks
            control_engine();
            process_can_messages();
            
            // Refresh watchdog (if tasks completed successfully)
            watchdog_refresh();
            
            HAL_Delay(100);  // 100 ms loop
        }
    }

Code Integrity Checks (CRC/HMAC)
---------------------------------

**Periodically verify firmware integrity during runtime:**

.. code-block:: c

    #include <mbedtls/md.h>
    
    // Verify Flash integrity at runtime
    int verify_flash_integrity(void) {
        extern uint8_t _firmware_start[];
        extern uint8_t _firmware_end[];
        extern uint8_t _firmware_hmac[];  // Stored HMAC
        
        size_t firmware_size = _firmware_end - _firmware_start;
        uint8_t calculated_hmac[32];
        
        // Calculate HMAC-SHA256 of firmware
        const mbedtls_md_info_t *md = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
        uint8_t hmac_key[32] = { /* Secret key stored in HSM */ };
        
        mbedtls_md_hmac(md, hmac_key, 32, _firmware_start, firmware_size, calculated_hmac);
        
        // Compare with stored HMAC
        if (memcmp(calculated_hmac, _firmware_hmac, 32) == 0) {
            return 1;  // Integrity OK
        } else {
            printf("ERROR: Firmware integrity check failed!\n");
            // Enter fail-safe mode
            return 0;
        }
    }
    
    // Periodic integrity check (every 10 seconds)
    void periodic_integrity_check_task(void) {
        while (1) {
            if (!verify_flash_integrity()) {
                // Firmware tampered - take action
                enter_fail_safe_mode();
            }
            
            vTaskDelay(pdMS_TO_TICKS(10000));  // 10 seconds
        }
    }

Secure Communication (SecOC Integration)
=========================================

**AUTOSAR SecOC** provides authenticated CAN communication. ECU hardening
includes integrating SecOC into the CAN stack.

.. code-block:: c

    #include "secoc.h"  // AUTOSAR SecOC library
    
    // Send authenticated CAN message
    int send_authenticated_can_message(uint32_t can_id, const uint8_t *data, size_t len) {
        uint8_t authenticated_pdu[16];  // Data + MAC + Freshness
        
        // Add SecOC authentication
        secoc_authenticate_pdu(can_id, data, len, authenticated_pdu);
        
        // Send on CAN bus
        can_send(can_id, authenticated_pdu, len + 4);  // +4 for MAC/freshness
        
        return 0;
    }
    
    // Receive and verify authenticated CAN message
    int receive_authenticated_can_message(uint32_t can_id, uint8_t *data, size_t *len) {
        uint8_t authenticated_pdu[16];
        
        // Receive from CAN bus
        can_receive(can_id, authenticated_pdu, len);
        
        // Verify SecOC authentication
        if (!secoc_verify_pdu(can_id, authenticated_pdu, *len)) {
            printf("SecOC verification failed for CAN ID 0x%03X\n", can_id);
            return -1;  // Discard message
        }
        
        // Extract data (remove MAC/freshness)
        memcpy(data, authenticated_pdu, *len - 4);
        *len -= 4;
        
        return 0;
    }

Fail-Safe Design
================

Fail-Safe Principles
--------------------

**Fail-Safe**: System enters a safe state when a security violation is detected.

**Examples:**

- **Engine ECU**: On security violation, limit engine to idle speed (prevent
  sudden acceleration)
- **Braking ECU**: On tampered sensor data, apply gentle braking (prevent
  sudden stop)
- **Airbag ECU**: On integrity check failure, disable airbag deployment
  (prevent unintended deployment)

**ISO 26262 (Functional Safety) + ISO 21434 (Cybersecurity):**

- Security failures can cause safety hazards
- Fail-safe design must consider both security and safety

Fail-Safe Implementation Example
---------------------------------

.. code-block:: c

    typedef enum {
        ECU_STATE_NORMAL,
        ECU_STATE_DEGRADED,  // Limited functionality
        ECU_STATE_FAIL_SAFE  // Minimal safe operation
    } ecu_state_t;
    
    ecu_state_t ecu_state = ECU_STATE_NORMAL;
    
    // Enter fail-safe mode on security violation
    void enter_fail_safe_mode(void) {
        ecu_state = ECU_STATE_FAIL_SAFE;
        
        printf("FAIL-SAFE MODE ACTIVATED\n");
        
        // Limit engine speed to idle
        set_throttle_limit(10);  // 10% max throttle
        
        // Disable non-essential features
        disable_cruise_control();
        disable_remote_start();
        
        // Log incident to secure storage
        log_security_incident("Firmware integrity check failed");
        
        // Notify driver (dashboard warning light)
        set_warning_light(WARNING_SECURITY_FAULT);
    }
    
    // Main control loop with fail-safe logic
    void control_loop(void) {
        while (1) {
            // Periodic integrity check
            if (!verify_flash_integrity()) {
                enter_fail_safe_mode();
            }
            
            // Process control tasks based on ECU state
            switch (ecu_state) {
                case ECU_STATE_NORMAL:
                    perform_full_control();
                    break;
                
                case ECU_STATE_DEGRADED:
                    perform_limited_control();
                    break;
                
                case ECU_STATE_FAIL_SAFE:
                    perform_minimal_safe_control();
                    // Attempt recovery or wait for service
                    break;
            }
            
            watchdog_refresh();
            vTaskDelay(pdMS_TO_TICKS(10));  // 10 ms loop
        }
    }

Supply Chain Security
=====================

Supply Chain Attack Scenarios
------------------------------

**Scenario 1: Compromised ECU from Tier 2 Supplier**

- Supplier's development environment infected with malware
- Malicious code injected into ECU firmware
- OEM receives compromised ECUs

**Scenario 2: Counterfeit Components**

- Fake microcontrollers with backdoors
- Lower-quality chips that fail under stress

**Mitigation: Hardware Authentication**

.. code-block:: c

    // Verify authenticity of microcontroller (check OEM signature)
    int verify_mcu_authenticity(void) {
        uint8_t mcu_uid[12];  // Unique ID of MCU
        
        // Read MCU unique ID (STM32 example)
        mcu_uid[0] = *(uint8_t*)(0x1FFF7A10);
        mcu_uid[1] = *(uint8_t*)(0x1FFF7A11);
        // ... (read all 12 bytes)
        
        // Verify UID against known OEM UID ranges
        if (!is_oem_genuine_mcu(mcu_uid)) {
            printf("ERROR: Counterfeit MCU detected!\n");
            return 0;
        }
        
        return 1;
    }

Exam Questions
==============

Question 1: Secure Boot Chain (Difficulty: Medium)
---------------------------------------------------

An automotive ECU has the following boot sequence:

1. ROM Bootloader (512 bytes, immutable)
2. Stage 1 Bootloader (64 KB, stored in Flash)
3. Application Firmware (512 KB, stored in Flash)

The ROM Bootloader contains an RSA-2048 public key to verify the Stage 1
Bootloader. However, the ROM has limited space (512 bytes total).

**a)** Is it feasible to store an RSA-2048 public key in 512 bytes? Explain.

**b)** If not, propose an alternative.

**Answer:**

**a) Feasibility:**

RSA-2048 public key components:
- **Modulus (n)**: 2048 bits = 256 bytes
- **Public exponent (e)**: Typically 3 bytes (e.g., 65537 = 0x010001)

Total: ~259 bytes

**However**, ROM Bootloader also needs:
- Boot code (~200-300 bytes)
- Signature verification code (~100-200 bytes)
- Total available: 512 bytes

**Conclusion:** RSA-2048 public key (256 bytes) + boot code (~400 bytes) = 
**~656 bytes** → Does NOT fit in 512 bytes.

**b) Alternative Solution:**

**Use ECDSA P-256 instead of RSA-2048:**

- **Public key size**: 64 bytes (32-byte X, 32-byte Y)
- **Security equivalent**: ECDSA P-256 ≈ RSA-2048 (NIST recommendation)
- **Signature size**: 64 bytes (32-byte r, 32-byte s)

**Space requirement:**
- Public key: 64 bytes
- Boot code: ~300 bytes
- Signature verification: ~100 bytes

**Total: ~464 bytes** → Fits in 512 bytes ✅

**Alternative 2: Hash-Based Verification**

- Store **SHA-256 hash** of Stage 1 Bootloader public key in ROM (32 bytes)
- Stage 1 Bootloader includes its own public key
- ROM Bootloader verifies: `SHA256(Stage1_PublicKey) == Stored_Hash`
- Saves space, but less flexible (cannot update public key without ROM change)

Question 2: Memory Protection Attack (Difficulty: Hard)
--------------------------------------------------------

An attacker has identified a buffer overflow vulnerability in an ECU's CAN
message handler:

.. code-block:: c

    void handle_can_message(can_frame_t *frame) {
        char buffer[64];
        memcpy(buffer, frame->data, frame->dlc);  // No bounds check!
        process_data(buffer);
    }

The ECU uses an ARM Cortex-M4 with MPU enabled. The MPU configuration is:

- Region 0: Flash (0x08000000-0x080FFFFF), Read-Only, Execute
- Region 1: RAM (0x20000000-0x2001FFFF), Read-Write, Execute
- Region 2: Stack (0x20020000-0x20023FFF), Read-Write, **No Execute**

**a)** Can the attacker exploit this buffer overflow to inject code? Explain.

**b)** What attack technique can the attacker use instead?

**c)** Propose two additional mitigations.

**Answer:**

**a) Code Injection:**

The attacker can overflow `buffer` (on stack) and overwrite the return address.

**However:**

- Region 2 (Stack) has **No Execute (XN)** permission
- Even if attacker overwrites return address to point to stack, CPU will trigger
  a **MemManage exception** when attempting to execute code from stack

**Conclusion:** Code injection is **blocked by MPU** ✅

**b) Alternative Attack: Return-Oriented Programming (ROP)**

Since stack is non-executable, attacker uses **ROP (Return-Oriented Programming)**:

1. Overflow buffer to overwrite return address
2. Set return address to point to **existing code** in Flash (executable region)
3. Chain multiple "gadgets" (short instruction sequences ending in `ret`)
4. Achieve arbitrary code execution using existing code

**Example ROP chain:**

.. code-block:: text

    Overflow buffer:
    [AAAA...] [Gadget1_addr] [Gadget2_addr] [Gadget3_addr] ...
    
    Gadget1: pop {r0}; ret  ← Load attacker data into r0
    Gadget2: bl memcpy      ← Call memcpy(dest, src, len)
    Gadget3: bl system      ← Execute command

**c) Additional Mitigations:**

**Mitigation 1: Stack Canaries**

.. code-block:: bash

    # Enable stack canaries in GCC
    arm-none-eabi-gcc -fstack-protector-all -o firmware firmware.c

- Compiler places a random canary value before return address
- Before function returns, canary is checked
- If modified (overflow), program aborts

**Mitigation 2: Control Flow Integrity (CFI)**

- Validate that function returns go to valid call sites
- Prevents ROP by checking return address validity

**Mitigation 3: Bounds Checking**

.. code-block:: c

    void handle_can_message(can_frame_t *frame) {
        char buffer[64];
        
        // Bounds check
        size_t copy_len = (frame->dlc > sizeof(buffer)) ? sizeof(buffer) : frame->dlc;
        
        memcpy(buffer, frame->data, copy_len);
        process_data(buffer);
    }

Question 3: Debug Lockdown Trade-Off (Difficulty: Medium)
----------------------------------------------------------

An OEM is deciding between three debug lockdown strategies for production ECUs:

**Option A:** Disable JTAG/SWD completely (no debug access)
**Option B:** Password-protected debug access (require 128-bit password)
**Option C:** Certificate-based debug access (require signed challenge-response)

**a)** Compare the security and operational trade-offs of each option.

**b)** Which option would you recommend for a **safety-critical ECU** (e.g.,
braking system)? Justify.

**Answer:**

**a) Comparison:**

+----------+--------------------+-------------------------+----------------------+
| Option   | Security Level     | Operational Impact      | Recovery Capability  |
+==========+====================+=========================+======================+
| **A**    | ✅✅ Highest       | ❌ No field debugging   | ❌ Cannot recover    |
|          | (No debug access)  | ❌ Difficult failure    | bricked ECU          |
|          |                    | analysis                |                      |
+----------+--------------------+-------------------------+----------------------+
| **B**    | ⚠️  Medium-High    | ✅ Field debugging      | ✅ Can recover with  |
|          | (Password can leak)| possible                | password             |
+----------+--------------------+-------------------------+----------------------+
| **C**    | ✅✅ Highest       | ✅ Field debugging      | ✅ Can recover with  |
|          | (PKI-based)        | with authorization      | OEM certificate      |
+----------+--------------------+-------------------------+----------------------+

**Detailed Analysis:**

**Option A: No Debug Access**

- **Pros**:
  
  - Maximum security (no debug interface for attacker)
  - Simple (no authentication logic)

- **Cons**:
  
  - Cannot debug field failures (e.g., crash after 10,000 miles)
  - Cannot recover bricked ECU (must replace entire ECU)
  - Difficult root cause analysis (no memory dumps)

**Option B: Password-Protected**

- **Pros**:
  
  - Field debugging possible (technicians have password)
  - Can recover bricked ECU

- **Cons**:
  
  - Password can leak (insider threat, social engineering)
  - No audit trail (who debugged the ECU?)
  - Weak if password is short or predictable

**Option C: Certificate-Based (PKI)**

- **Pros**:
  
  - Strong security (requires OEM private key to sign challenge)
  - Audit trail (log all debug sessions with certificate ID)
  - Granular access control (different certificates for different teams)

- **Cons**:
  
  - Complex implementation (PKI infrastructure)
  - Requires secure storage of OEM private key

**b) Recommendation for Safety-Critical ECU:**

**Recommended: Option C (Certificate-Based Debug Access)**

**Justification:**

1. **Safety**: Safety-critical ECUs (braking) require field debugging capability
   for failure analysis (ISO 26262 requires root cause analysis)

2. **Security**: Certificate-based access provides strong authentication without
   the risks of password leakage

3. **Recoverability**: OEM can recover bricked ECUs in field (avoid costly
   replacements)

4. **Compliance**: ISO 21434 recommends PKI for access control in safety-critical
   systems

**Implementation:**

- Debug interface requires challenge-response signed by OEM's private key
- OEM issues time-limited certificates to authorized technicians
- Debug sessions logged to tamper-proof storage for audit

Question 4: Key Derivation (Difficulty: Medium)
------------------------------------------------

An OEM manufactures 1 million ECUs per year. Each ECU needs a unique AES-128
key for SecOC message authentication.

**Option 1:** Provision individual keys at factory (1 million unique keys)
**Option 2:** Use key derivation from a single master key

**a)** Calculate the storage and provisioning overhead for Option 1.

**b)** Design a key derivation scheme for Option 2.

**c)** What is the security risk if the master key is compromised in Option 2?

**Answer:**

**a) Option 1 Overhead:**

**Factory Provisioning:**

- **Key database**: 1,000,000 keys × 16 bytes/key = 16 MB
- **Provisioning time**: Assuming 1 second per ECU to program key → 1,000,000
  seconds = 277 hours = 11.5 days (single production line)
- **Key management**: Track which key assigned to which ECU (VIN mapping)

**Security Considerations:**

- **Key database security**: Must protect database of 1 million keys
- **Logistics**: Transport keys securely to factory
- **Revocation**: If one ECU compromised, only that key needs revocation

**b) Option 2: Key Derivation Scheme:**

**Master Key Storage:**

- Single 256-bit master key stored in HSM at factory
- Master key never leaves HSM

**Derivation Formula:**

.. code-block:: text

    ECU_Key = HKDF-Expand(Master_Key, ECU_ID)
    
    Where:
    - Master_Key: 256-bit secret (in HSM)
    - ECU_ID: Unique identifier (VIN + ECU serial number)
    - HKDF-Expand: Key derivation function (RFC 5869)

**Provisioning Process:**

1. ECU manufactured with unique ECU_ID (burned into OTP memory)
2. Factory HSM derives ECU_Key = HKDF(Master_Key, ECU_ID)
3. ECU_Key provisioned into ECU's secure storage (encrypted flash or HSM)

**Advantages:**

- Only 1 master key to manage (256 bits = 32 bytes)
- No key database required
- Provisioning time: ~same (still need to program derived key into each ECU)

**c) Security Risk if Master Key Compromised:**

**If attacker obtains Master_Key:**

- Attacker can derive **all ECU keys** (1 million keys)
- Compromise is **catastrophic** (all vehicles affected)
- Requires **global key rotation** (OTA update to all vehicles)

**Mitigation:**

1. **Protect Master Key with HSM**: Master key never leaves HSM, even during
   derivation
2. **Split Master Key**: Use Shamir's Secret Sharing (require 3 of 5 key shares
   to reconstruct)
3. **Hierarchical Key Derivation**:
   
   .. code-block:: text
   
       Master_Key → Per-Vehicle-Model Key → Per-ECU Key
   
   - Compromise of one vehicle model key affects only that model
   - Limits blast radius

4. **Key Rotation**: Rotate master key annually, re-derive ECU keys during
   scheduled maintenance

**Recommendation:**

Use **hierarchical key derivation** with **HSM protection** for master key.

Question 5: Secure Boot Bypass (Difficulty: Hard)
--------------------------------------------------

An attacker discovers that an ECU's secure boot process is vulnerable to
**fault injection** (voltage glitching).

**Attack Steps:**

1. Attacker modifies firmware to include malicious code
2. Attacker attempts to boot modified firmware
3. Secure boot signature verification fails
4. During verification failure, attacker triggers voltage glitch
5. Glitch causes CPU to skip the "halt boot" instruction
6. Modified firmware executes

**a)** Explain why this attack succeeds despite secure boot.

**b)** Propose three hardware-level mitigations.

**c)** Propose two software-level mitigations.

**Answer:**

**a) Why Attack Succeeds:**

Secure boot verification code (simplified):

.. code-block:: c

    if (!verify_signature(firmware)) {
        // Halt boot (infinite loop)
        while (1);
    }
    
    // Jump to firmware
    boot_firmware();

**Fault Injection:**

- Attacker triggers voltage glitch during `while (1);` execution
- Glitch causes CPU to:
  
  - Skip instruction (program counter jumps past loop)
  - Corrupt condition flag (signature check bypassed)

- CPU proceeds to `boot_firmware()` despite failed verification

**Root Cause:**

- Verification result stored in CPU register (volatile, susceptible to glitching)
- No hardware enforcement of boot policy

**b) Hardware-Level Mitigations:**

**Mitigation 1: Secure Boot Engine (Hardware)**

- Dedicated hardware block performs signature verification
- Verification result stored in **hardware fuse** (cannot be glitched)
- CPU cannot boot until hardware sets "boot allowed" flag

**Example: ARM TrustZone for Cortex-M33**

- Secure Boot Controller (hardware) verifies firmware
- Only Secure World can set "boot allowed" flag
- Non-Secure World cannot bypass

**Mitigation 2: Voltage/Clock Monitoring (Tamper Detection)**

- Voltage monitor detects abnormal supply voltage (glitch)
- On detection: Halt CPU, erase keys, enter fail-safe mode

**Mitigation 3: Redundant Verification (Triple Modular Redundancy)**

- Verify signature **three times**
- Use majority voting (2 of 3 must agree)
- Glitching one verification is insufficient

**c) Software-Level Mitigations:**

**Mitigation 1: Multiple Verification Points**

.. code-block:: c

    // Verify at multiple points
    int result1 = verify_signature(firmware);
    int result2 = verify_signature(firmware);
    int result3 = verify_signature(firmware);
    
    // All three must pass
    if (result1 && result2 && result3) {
        boot_firmware();
    } else {
        // Even if glitch bypasses one check, others will fail
        enter_recovery_mode();
    }

**Mitigation 2: Infinite Loop with Variable State**

.. code-block:: c

    volatile uint32_t boot_allowed = 0;
    
    if (verify_signature(firmware)) {
        boot_allowed = 0xDEADBEEF;  // Magic value
    }
    
    // Check boot_allowed at multiple points
    if (boot_allowed != 0xDEADBEEF) {
        while (1);  // Halt
    }
    
    if (boot_allowed != 0xDEADBEEF) {
        while (1);  // Redundant check
    }
    
    boot_firmware();

**Mitigation 3: Watchdog with External Reset**

- Watchdog timer monitors boot process
- If boot takes too long (verification failed), watchdog resets ECU
- External watchdog (separate IC) harder to glitch

Conclusion
==========

ECU hardening is essential for automotive, industrial, and safety-critical
systems. Key hardening techniques include:

1. **Secure Boot**: Verify firmware integrity before execution (RSA/ECDSA)
2. **Memory Protection**: Enable MPU/MMU, stack canaries, non-executable stack
3. **Debug Lockdown**: Disable or authenticate JTAG/SWD access
4. **Cryptographic Storage**: Use HSM or secure flash for keys
5. **Runtime Integrity**: Monitor code/data integrity during execution
6. **Fail-Safe Design**: Enter safe state on security violation

**Compliance:**

- **ISO 21434** (Automotive Cybersecurity): Mandates ECU hardening for new vehicles
- **IEC 62443** (Industrial): Requires secure boot and access control
- **UN R155** (CSMS): Requires ECU security for vehicle type approval

References
==========

- ISO 21434: Road vehicles - Cybersecurity engineering
- AUTOSAR: Secure Onboard Communication (SecOC) specification
- IEC 62443: Security for industrial automation and control systems
- ARM TrustZone for Cortex-M: Security architecture
- MISRA C: Guidelines for secure C programming in embedded systems
- EVITA HSM: Hardware security module for automotive applications

**END OF DOCUMENT**
