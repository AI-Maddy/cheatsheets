====================================================================
Infusion Pump Security - Critical Medical Device Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: FDA Guidance, IEC 62304, UL 2900-2-1

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Infusion Pump Threats:**

- **Drug library tampering:** Modify dose limits → overdose
- **Wireless hijacking:** Bluetooth/WiFi interception
- **Physical access:** USB/UART modification
- **Supply chain:** Counterfeit consumables with malware

**Security Controls:**

✅ **Encrypted drug library** (AES-256)
✅ **Wireless authentication** (certificate-based)
✅ **Dose verification** (independent safety check)
✅ **Tamper detection** (hardware seals)
✅ **Secure boot** (verify firmware signature)

Introduction
============

**Infusion pumps** deliver medications, fluids, and nutrients intravenously. Security failures can cause **patient death**.

**Attack Consequences:**

- Overdose (10× insulin dose → hypoglycemic shock)
- Underdose (pain medication → patient suffering)
- Wrong drug delivery
- Data breach (patient medical records)

Infusion Pump Architecture
===========================

.. code-block:: text

    ┌─────────────────────────────┐
    │   Nurse Station (EMR)       │
    │   Prescribes: Morphine 2mg/h│
    └──────────────┬──────────────┘
                   │ WiFi (TLS)
    ┌──────────────▼──────────────┐
    │   Infusion Pump Controller  │
    │   ├─ Drug Library           │
    │   ├─ Dose Calculator        │
    │   └─ Motor Control          │
    └──────────────┬──────────────┘
                   │
    ┌──────────────▼──────────────┐
    │   Stepper Motor (IV line)   │
    └─────────────────────────────┘

Attack Scenario: Drug Library Tampering
========================================

**Vulnerability:** Drug library stored in plaintext on flash memory.

**Attack:**

.. code-block:: python

    # Attacker extracts drug library via UART
    def tamper_drug_library():
        # Connect to debug UART (inside pump housing)
        uart = serial.Serial('/dev/ttyUSB0', 115200)
        
        # Dump drug library from flash
        drug_library = read_flash(0x10000, 4096)
        
        # Modify max dose limit for morphine
        modified = drug_library.replace(
            b'morphine_max_dose=10',  # 10 mg/h
            b'morphine_max_dose=99'   # 99 mg/h (LETHAL)
        )
        
        # Write back to flash
        write_flash(0x10000, modified)

**Impact:** Pump accepts lethal dose without alarm.

**Mitigation:**

.. code-block:: c

    // Encrypt drug library with AES-256
    #include <mbedtls/aes.h>
    
    void encrypt_drug_library(uint8_t *library, size_t len) {
        uint8_t key[32];  // Derived from HSM or device unique key
        uint8_t iv[16];
        
        mbedtls_aes_context aes;
        mbedtls_aes_setkey_enc(&aes, key, 256);
        mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_ENCRYPT, len, iv, library, library);
    }
    
    // Verify integrity with HMAC
    int verify_drug_library_integrity(uint8_t *library, size_t len, uint8_t *hmac) {
        uint8_t computed_hmac[32];
        mbedtls_md_hmac(MBEDTLS_MD_SHA256, secret_key, 32, library, len, computed_hmac);
        
        return memcmp(hmac, computed_hmac, 32) == 0;
    }

Wireless Security (WiFi/Bluetooth)
===================================

**Attack: Man-in-the-Middle on WiFi**

.. code-block:: python

    # Attacker intercepts nurse → pump command
    def mitm_infusion_pump():
        # Sniff WiFi traffic
        packet = sniff_wifi(ssid='Hospital_Medical_Devices')
        
        # Modify infusion rate
        if 'infusion_rate' in packet:
            packet['infusion_rate'] = 100  # Increase from 10 to 100 ml/h
            forward(packet, pump_ip)

**Mitigation: TLS with Mutual Authentication**

.. code-block:: c

    // Pump authenticates to server AND server authenticates pump
    mbedtls_ssl_context ssl;
    mbedtls_ssl_config conf;
    
    // Load pump certificate (unique per device)
    mbedtls_x509_crt_parse_file(&pump_cert, "pump_12345.crt");
    mbedtls_pk_parse_keyfile(&pump_key, "pump_12345.key", NULL);
    
    // Require server certificate verification
    mbedtls_ssl_conf_authmode(&conf, MBEDTLS_SSL_VERIFY_REQUIRED);
    mbedtls_ssl_conf_ca_chain(&conf, &hospital_ca, NULL);
    
    // Connect with TLS 1.3
    mbedtls_ssl_handshake(&ssl);

Independent Safety Check
=========================

**Concept:** Separate microcontroller verifies dose calculations (defense-in-depth).

.. code-block:: c

    // Main MCU calculates dose
    float main_dose = calculate_dose(prescription);
    
    // Safety MCU independently verifies
    float safety_dose = safety_calculate_dose(prescription);
    
    if (fabs(main_dose - safety_dose) > 0.01) {
        // Mismatch detected → halt pump
        trigger_alarm("Dose calculation mismatch!");
        stop_motor();
        enter_safe_state();
    }

**Implementation:**

.. code-block:: text

    Main MCU (ARM Cortex-M4)
         ├─ Runs Linux
         ├─ WiFi stack
         └─ Complex dose algorithms
    
    Safety MCU (ARM Cortex-M0)
         ├─ No OS (bare metal)
         ├─ Simple dose verification
         ├─ Independent power supply
         └─ Watchdog timer

Exam Questions
==============

**Q1: FDA Recall Case Study (Hard)**

In 2019, FDA recalled infusion pumps due to cybersecurity vulnerabilities allowing unauthorized remote access. Describe the vulnerabilities and required fixes.

**Answer:**

**Vulnerabilities (Hospira Plum 360):**

1. **Hardcoded passwords:** Default admin password in firmware
2. **Cleartext telnet:** No encryption for remote access
3. **Unauthenticated firmware updates:** Anyone on network could upload malicious firmware
4. **No network isolation:** Pumps on same VLAN as guest WiFi

**Required Fixes (FDA Enforcement):**

1. **Disable telnet:** Use SSH with key-based auth
2. **Firmware signing:** ECDSA signature verification
3. **Network segmentation:** Pumps on isolated medical VLAN
4. **Patch management:** Automated security updates
5. **Monitoring:** IDS to detect unauthorized access attempts

**Q2: Safety vs. Security Conflict (Medium)**

An infusion pump must deliver emergency epinephrine within 5 seconds. Firmware signature verification takes 8 seconds at boot. How to resolve?

**Answer:**

**Option 1: Verified Boot with Cached Result**
- First boot: Verify signature (8 seconds)
- Store verification result in tamper-resistant memory
- Subsequent boots: Use cached result (instant)
- Re-verify if firmware update detected

**Option 2: Emergency Mode**
- Normal boot: Verify signature (8 seconds)
- Emergency button pressed: Boot without verification
- After emergency: Force full verification + audit log review

**Option 3: Hardware Acceleration**
- Use hardware crypto accelerator (reduces verification to <1 second)
- Meets both safety timing and security requirements

**Best Practice:** Option 3 (hardware acceleration) is preferred.

Standards
=========

- **FDA Guidance (2023):** Cybersecurity for medical devices
- **IEC 62304:** Medical device software lifecycle
- **UL 2900-2-1:** Security for network-connectable medical devices

**END OF DOCUMENT**
