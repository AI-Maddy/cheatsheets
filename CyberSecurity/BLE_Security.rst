====================================================================
BLE Security - Bluetooth Low Energy
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: Bluetooth Core Spec 5.4, NIST IR 8278

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**BLE Security Features:**

- **Pairing:** Just Works, Passkey Entry, Numeric Comparison, OOB
- **Encryption:** AES-128-CCM
- **Key derivation:** ECDH (Elliptic Curve Diffie-Hellman)
- **Privacy:** Address randomization (random vs. public)

**Common Vulnerabilities:**

❌ **Just Works pairing:** No MITM protection
❌ **Legacy pairing:** Weak key derivation
❌ **Passive eavesdropping:** Sniff pairing to derive keys
❌ **Relay attacks:** BLE "man-in-the-middle" proxy

Introduction
============

**BLE (Bluetooth Low Energy)** is used in medical devices, wearables, smart locks, automotive, and industrial sensors.

**Security Goals:**

1. **Confidentiality:** Encrypt sensor data
2. **Authentication:** Verify device identity
3. **Privacy:** Prevent tracking via MAC address

BLE Pairing Methods
====================

**1. Just Works (Insecure)**

.. code-block:: text

    Phone → Fitness Tracker: Pairing request
    Tracker → Phone: Accept (no PIN)
    ← Keys exchanged (no authentication) →

**Vulnerability:** Attacker can perform MITM during pairing.

**2. Passkey Entry (Secure)**

.. code-block:: python

    # Device displays 6-digit PIN
    passkey = 123456
    display_on_screen(passkey)
    
    # User enters PIN on smartphone
    # Pairing only succeeds if PIN matches

**3. Numeric Comparison (Most Secure)**

.. code-block:: text

    Phone displays: 837492
    Device displays: 837492
    User confirms: "Do numbers match? YES/NO"

**4. Out-of-Band (OOB)**

Exchange keys via NFC tap or QR code (secure channel).

BLE Encryption (AES-CCM)
=========================

**Link Layer Encryption:**

.. code-block:: c

    #include <mbedtls/ccm.h>
    
    void ble_encrypt_packet(uint8_t *plaintext, size_t len, uint8_t *ciphertext) {
        uint8_t ltk[16];  // Long-Term Key (from pairing)
        uint8_t nonce[13];  // Includes packet counter
        
        mbedtls_ccm_context ccm;
        mbedtls_ccm_init(&ccm);
        mbedtls_ccm_setkey(&ccm, MBEDTLS_CIPHER_ID_AES, ltk, 128);
        
        // Encrypt with AES-128-CCM
        mbedtls_ccm_encrypt_and_tag(&ccm, len, nonce, 13,
            NULL, 0,  // No additional data
            plaintext, ciphertext,
            ciphertext + len, 4);  // 4-byte MIC
    }

**Key Derivation (ECDH):**

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    
    # Generate device key pair
    device_private = ec.generate_private_key(ec.SECP256R1())
    device_public = device_private.public_key()
    
    # Receive phone's public key
    phone_public = receive_public_key()
    
    # Perform ECDH
    shared_secret = device_private.exchange(ec.ECDH(), phone_public)
    
    # Derive encryption key
    ltk = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b'BLE LTK'
    ).derive(shared_secret)

Attack Scenario: BLE Sniffer
==============================

**Tool: Ubertooth One (BLE Sniffer)**

.. code-block:: bash

    # Capture BLE pairing
    ubertooth-btle -f -c pairing_capture.pcap
    
    # If "Just Works" pairing used, derive LTK
    crackle -i pairing_capture.pcap -o ltk.txt

**Mitigation:** Use Numeric Comparison or Passkey Entry.

**Passive Eavesdropping:**

If attacker sniffs pairing, they can derive LTK and decrypt future traffic.

**Defense: LE Secure Connections (BLE 4.2+)**

.. code-block:: c

    // Use ECDH instead of legacy P-192 key exchange
    #define BLE_SECURITY_MODE_SC  // Secure Connections
    
    // Protects against passive eavesdropping
    // Attacker must actively MITM during pairing

BLE Relay Attack (Smart Lock)
===============================

**Attack:** Unlock car from 100 meters away.

.. code-block:: text

    Car (BLE peripheral)
         ↑ 
    Attacker Relay Device (near car)
         ↑ (WiFi)
    Attacker Relay Device (near victim's phone)
         ↑
    Victim's Phone (BLE central)

**Steps:**

1. Victim's phone is in pocket (BLE enabled)
2. Attacker Device A (near phone) detects key fob signal
3. Relays to Device B (near car) over WiFi
4. Car unlocks (thinks phone is nearby)

**Mitigation: Distance Bounding**

.. code-block:: python

    import time
    
    def verify_proximity():
        # Challenge-response with time measurement
        start = time.time()
        
        # Send challenge
        challenge = os.urandom(16)
        send_ble_packet(challenge)
        
        # Measure round-trip time
        response = receive_ble_packet()
        rtt = time.time() - start
        
        # BLE speed: ~1 Mbps, 16 bytes = 0.000128 seconds
        # If RTT > 0.001 seconds, device is >150 meters away
        if rtt > 0.001:
            print("Relay attack detected!")
            deny_unlock()

Privacy (Address Randomization)
=================================

**Problem:** Static MAC address enables tracking.

**Solution: Resolvable Private Address (RPA)**

.. code-block:: c

    #include <mbedtls/aes.h>
    
    void generate_rpa(uint8_t *irk, uint8_t *rpa) {
        // IRK = Identity Resolving Key (shared secret)
        uint8_t prand[3];  // Random value
        generate_random(prand, 3);
        prand[2] &= 0x3F;  // Clear top 2 bits
        
        // Hash = AES(IRK, prand || padding)
        uint8_t plaintext[16] = {0};
        memcpy(plaintext, prand, 3);
        
        uint8_t hash[16];
        mbedtls_aes_context aes;
        mbedtls_aes_setkey_enc(&aes, irk, 128);
        mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT, plaintext, hash);
        
        // RPA = prand || hash[0:2]
        rpa[0] = prand[0];
        rpa[1] = prand[1];
        rpa[2] = prand[2] | 0x40;  // Set RPA flag
        rpa[3] = hash[0];
        rpa[4] = hash[1];
        rpa[5] = hash[2];
    }

**Rotation:** Change RPA every 15 minutes (prevents long-term tracking).

Exam Questions
==============

**Q1: BLE Medical Device Pairing (Medium)**

A glucose monitor uses BLE to transmit readings to smartphone. Which pairing method is appropriate and why?

**Answer:**

**Recommended: Passkey Entry**

**Rationale:**

- **Numeric Comparison:** Requires display on both devices (glucose monitor may have small screen)
- **Passkey Entry:** Display 6-digit PIN on glucose monitor, user enters on phone
- **Just Works:** ❌ Insecure (MITM possible)

**Implementation:**

.. code-block:: c

    uint32_t passkey = generate_random_6_digit();
    lcd_display_passkey(passkey);
    
    // Wait for smartphone to enter passkey
    ble_set_passkey(passkey);
    ble_start_pairing();

**Threat Model:**

- Attacker in Bluetooth range during pairing
- If passkey displayed on device, attacker cannot MITM
- After pairing, data encrypted with derived LTK

**Q2: BLE vs WiFi for IoT (Hard)**

Compare BLE and WiFi for battery-powered sensors. Consider security and power consumption.

**Answer:**

+-------------------+-------------------------+------------------------+
| Feature           | BLE                     | WiFi                   |
+===================+=========================+========================+
| Power (idle)      | 10 µA                   | 10 mA (100× worse)     |
+-------------------+-------------------------+------------------------+
| Range             | 50 m                    | 100+ m                 |
+-------------------+-------------------------+------------------------+
| Data rate         | 1-2 Mbps                | 54-600 Mbps            |
+-------------------+-------------------------+------------------------+
| Pairing           | ✅ Built-in             | ⚠️  Manual (WPA2-PSK)  |
+-------------------+-------------------------+------------------------+
| Encryption        | AES-128-CCM             | AES-128-CCMP           |
+-------------------+-------------------------+------------------------+

**Use BLE for:**

- Battery-powered sensors (coin cell → 2 years)
- Wearables
- Proximity-based applications (smart lock)

**Use WiFi for:**

- High-bandwidth (camera, audio)
- Internet connectivity
- Always-powered devices

**Hybrid Approach:**

- BLE for sensor data collection (low power)
- WiFi gateway uploads to cloud
- Example: BLE thermometer → WiFi hub → HTTPS to server

Standards
=========

- **Bluetooth Core Spec 5.4:** LE Secure Connections, Extended Advertising
- **NIST IR 8278:** Bluetooth Security Guide
- **FDA Guidance:** Wireless medical device security

**END OF DOCUMENT**
