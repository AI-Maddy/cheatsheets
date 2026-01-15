====================================================================
JTAG/SWD Security - Debug Interface Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEEE 1149.1, ARM CoreSight

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**JTAG/SWD:**

- **Purpose:** Debug, programming, boundary scan
- **JTAG:** 4-5 pins (TDI, TDO, TCK, TMS, TRST)
- **SWD:** 2 pins (SWDIO, SWCLK) - ARM Cortex-M

**Attack Surface:**

- Firmware extraction via JTAG
- Memory dump (encryption keys)
- Debug port injection (modify execution)

**Defense:**

✅ **Disable in production:** Fuse blow, software lock
✅ **Debug authentication:** Password/certificate required
✅ **Secure debug:** ARM TrustZone controlled access

Introduction
============

**Threat:** Attacker with physical access extracts firmware or keys.

JTAG Firmware Extraction
=========================

.. code-block:: bash

    # Extract firmware via JTAG (OpenOCD)
    
    # Connect to target
    openocd -f interface/jlink.cfg -f target/stm32f4x.cfg
    
    # Dump flash memory
    > dump_image firmware.bin 0x08000000 0x100000
    # 1 MB firmware extracted

**Attack: Extract AES Key from RAM**

.. code-block:: python

    # Use JTAG to read AES key from memory
    import openocd
    
    def extract_aes_key():
        ocd = openocd.connect()
        
        # Read key from known location (0x20000100)
        key_addr = 0x20000100
        key = ocd.read_memory(key_addr, 16)
        
        print(f"AES Key: {key.hex()}")

Defense: Disable JTAG
======================

**Method 1: Fuse Blow (Irreversible)**

.. code-block:: c

    // STM32: Blow JTAG disable fuse
    #include <stm32f4xx.h>
    
    void disable_jtag_permanent(void) {
        // WARNING: Irreversible!
        FLASH_OBProgramInitTypeDef ob_config;
        
        // Read current option bytes
        HAL_FLASHEx_OBGetConfig(&ob_config);
        
        // Disable JTAG
        ob_config.RDPLevel = OB_RDP_LEVEL_1;  // Read protection
        ob_config.USERConfig |= OB_IWDG_SW | OB_STOP_NO_RST | OB_STDBY_NO_RST;
        
        // Program option bytes
        HAL_FLASH_Unlock();
        HAL_FLASH_OB_Unlock();
        HAL_FLASHEx_OBProgram(&ob_config);
        HAL_FLASH_OB_Launch();
        HAL_FLASH_OB_Lock();
        HAL_FLASH_Lock();
    }

**Method 2: Software Lock (Reversible)**

.. code-block:: c

    // Disable JTAG/SWD in software (early in main())
    void disable_debug_interface(void) {
        // Disable JTAG, keep SWD (for emergency recovery)
        __HAL_AFIO_REMAP_SWJ_NOJTAG();
        
        // OR disable both JTAG and SWD
        //__HAL_AFIO_REMAP_SWJ_DISABLE();
    }

Secure Debug (ARM TrustZone)
=============================

.. code-block:: c

    // ARM CoreSight: Require authentication for debug access
    
    #include <arm_cmse.h>
    
    // Debug authentication handler
    int debug_auth_handler(uint8_t *password) {
        uint8_t correct_password[32] = {...};  // Stored securely
        
        // Verify password
        if (memcmp_secure(password, correct_password, 32) != 0) {
            return -1;  // Authentication failed
        }
        
        // Enable debug access
        CoreDebug->DHCSR |= CoreDebug_DHCSR_C_DEBUGEN_Msk;
        
        return 0;
    }

**Certificate-Based Debug:**

.. code-block:: c

    // Require signed debug certificate
    int verify_debug_certificate(uint8_t *cert, uint8_t *signature) {
        // Verify ECDSA signature with OEM public key
        uint8_t hash[32];
        mbedtls_sha256(cert, sizeof(cert), hash, 0);
        
        if (ecdsa_verify(hash, signature, oem_public_key) != 0) {
            return -1;  // Invalid certificate
        }
        
        // Check expiry, permissions in certificate
        if (cert_expired(cert) || !cert_allows_debug(cert)) {
            return -1;
        }
        
        // Enable debug
        enable_jtag_access();
        return 0;
    }

Exam Questions
==============

**Q1: Production Debug Access (Hard)**

Automotive ECU needs debug disabled in production but enabled for field diagnostics. Design solution.

**Answer:**

**Option 1: Debug Certificate**
- Field engineer obtains time-limited debug certificate from OEM
- Certificate signed with OEM private key
- ECU verifies certificate, enables debug for 24 hours
- Audit log records debug access

**Option 2: Challenge-Response**
- Engineer calls OEM support with ECU serial number
- OEM generates one-time unlock code
- Engineer enters code, debug enabled for 1 hour
- Code expires after use

**Option 3: Hardware Key**
- Physical debug adapter with certificate chip
- ECU authenticates adapter via I2C before enabling JTAG
- Only authorized service centers have adapter

**Q2: JTAG Disable Trade-offs (Medium)**

What are consequences of permanently disabling JTAG?

**Answer:**

**Pros:**
- Maximum security (firmware cannot be extracted)
- Prevents key extraction from RAM

**Cons:**
- Cannot debug field failures
- Cannot update firmware if OTA fails
- Device is "bricked" if software bug exists

**Recommendation:** Use software lock + secure debug for field serviceability.

Standards
=========

- **IEEE 1149.1:** JTAG boundary scan
- **ARM CoreSight:** Debug architecture

**END OF DOCUMENT**
