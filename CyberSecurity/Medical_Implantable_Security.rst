====================================================================
Medical Implantable Device Security - Pacemakers & Defibrillators
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: FDA Guidance, ISO 14708

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Implantable Devices:**

- Cardiac pacemakers, ICDs (Implantable Cardioverter-Defibrillators)
- Insulin pumps, neurostimulators, cochlear implants
- **Communication:** Medical Implant Communication Service (MICS 402-405 MHz)

**Security Challenges:**

- **Battery life:** Crypto drains battery (10-year lifespan)
- **Emergency access:** Doctors need access without password
- **Range:** RF communication 0-2 meters

**Security Controls:**

✅ **Rolling codes:** One-time use authentication
✅ **Proximity detection:** Require physical contact for programming
✅ **Audit logging:** Record all configuration changes

Introduction
============

**Threat Model:**

1. **Malicious shock delivery** (ICD)
2. **Pacing rate manipulation** (pacemaker)
3. **Battery drain** (DoS)
4. **Privacy breach** (patient data exfiltration)

Attack Scenario: Unauthorized Shock
=====================================

.. code-block:: python

    # Research demonstration (2008 - Barnaby Jack)
    # Attacker sends RF command to deliver shock
    
    import gnuradio
    
    def send_icd_shock_command(device_id):
        # MICS band (402-405 MHz)
        rf = gnuradio.RF_Transmitter(frequency=403e6)
        
        # Craft command (no encryption in legacy devices)
        command = {
            'device_id': device_id,
            'command': 'DELIVER_SHOCK',
            'energy': 35  # Joules (maximum)
        }
        
        rf.transmit(encode_mics_packet(command))

**Impact:** Patient death from inappropriate shock.

Defense: Proximity-Based Access
=================================

.. code-block:: c

    // Require programmer to be within 10 cm (RSSI-based)
    #define MIN_RSSI -40  // dBm (very close range)
    
    int authenticate_programmer(rf_packet_t *packet) {
        int rssi = get_rssi(packet);
        
        // Reject if programmer too far away
        if (rssi < MIN_RSSI) {
            log_event("Programmer too far (RSSI: %d)", rssi);
            return -1;
        }
        
        // Verify rolling code
        if (!verify_rolling_code(packet->auth_code)) {
            return -1;
        }
        
        return 0;
    }

**Rolling Code Authentication:**

.. code-block:: c

    // Generate one-time use codes
    uint32_t generate_rolling_code(void) {
        static uint32_t counter = 0;
        uint8_t seed[16];
        
        // Seed = Device unique key
        get_device_key(seed);
        
        // Code = HMAC(seed, counter)
        uint32_t code;
        mbedtls_md_hmac(MBEDTLS_MD_SHA256, seed, 16,
            (uint8_t*)&counter, 4, (uint8_t*)&code);
        
        counter++;
        return code;
    }

Battery-Efficient Crypto
=========================

.. code-block:: c

    // Minimize crypto to preserve 10-year battery life
    
    // Option 1: Event-triggered crypto (only when programmer nearby)
    void power_on_crypto_module(void) {
        if (detect_programmer_rf()) {
            enable_aes_accelerator();
            // Crypto active for 60 seconds
            set_timeout(crypto_power_off, 60);
        }
    }
    
    // Option 2: Lightweight crypto (ChaCha20 instead of AES)
    void encrypt_telemetry_lightweight(uint8_t *data, size_t len) {
        chacha20_ctx ctx;
        chacha20_init(&ctx, device_key, nonce);
        chacha20_encrypt(&ctx, data, len);
        // ChaCha20: 2× faster than AES, lower power
    }

Exam Questions
==============

**Q1: Emergency Access Dilemma (Hard)**

A patient collapses. Paramedics need to interrogate pacemaker but don't have password. Design solution.

**Answer:**

**Option 1: Emergency Override Code**
- Manufacturer provides time-limited override code to hospitals
- Code valid for 24 hours
- Requires phone call to manufacturer + patient ID verification

**Option 2: Emergency Mode**
- Physical magnet placed over device enables temporary access
- Limited to reading only (no programming)
- Audit log records magnet activation

**Option 3: Multi-Party Authorization**
- Require 2 doctors to authorize emergency access
- Both must enter PIN on programmer
- Legal liability protection

**Q2: Battery Life vs Security (Medium)**

Adding AES encryption reduces battery life from 10 years to 7 years. Is this acceptable?

**Answer:**

**Risk-Benefit Analysis:**
- **Risk:** Increased surgeries (battery replacement)
- **Benefit:** Protection against remote attacks

**Solution: Hybrid Approach**
- Encrypt only during programming sessions (1% of device lifetime)
- Telemetry uses lightweight authentication (rolling codes)
- Achieves 9.5-year battery life with adequate security

Standards
=========

- **FDA Guidance (2023):** Cybersecurity for medical devices
- **ISO 14708:** Active implantable medical devices

**END OF DOCUMENT**
