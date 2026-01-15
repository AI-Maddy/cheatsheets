====================================================================
NFC Security - Near Field Communication
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO/IEC 14443, ISO/IEC 18092

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**NFC:**

- **Purpose:** Short-range wireless (4-10 cm)
- **Applications:** Mobile payments, access control, ticketing
- **Frequency:** 13.56 MHz

**Security Features:**

✅ **Short range:** Physical proximity required
✅ **Encryption:** For payment (EMV, Apple Pay)
✅ **Secure Element:** Isolated chip for credentials

**Threats:**

❌ **Eavesdropping:** Attacker with antenna (1-2 meters)
❌ **Relay attack:** Extend NFC range
❌ **Cloning:** Duplicate NFC tags

Introduction
============

**NFC Modes:**

1. **Card emulation:** Phone acts as credit card
2. **Reader/writer:** Phone reads NFC tags
3. **Peer-to-peer:** Two phones exchange data

NFC Secure Element
===================

.. code-block:: c

    // Secure Element (SE) stores payment credentials
    // Isolated from main application processor
    
    typedef struct {
        uint8_t card_number[16];
        uint8_t cvv[3];
        uint8_t expiry[4];
        uint8_t private_key[32];  // For EMV transactions
    } secure_element_data_t;
    
    // Access to SE requires authentication
    int se_authenticate(uint8_t *pin) {
        // PIN verified in hardware (cannot be extracted)
        return se_verify_pin(pin);
    }
    
    // Generate EMV cryptogram (secure transaction)
    void generate_payment_cryptogram(uint8_t *cryptogram) {
        // Transaction data
        uint8_t tx_data[32];
        get_transaction_data(tx_data);
        
        // Sign with SE private key (never leaves SE)
        se_sign(tx_data, 32, cryptogram);
    }

**Attack: NFC Relay (Extend Range)**

.. code-block:: python

    # Attacker Device A (near victim's phone in pocket)
    # Attacker Device B (near payment terminal)
    # Relay NFC communication over WiFi
    
    def nfc_relay_attack():
        # Device A: Read NFC from victim's phone
        nfc_data = read_nfc_from_phone()
        
        # Send over WiFi to Device B
        send_via_wifi(device_b_ip, nfc_data)
        
        # Device B: Emulate victim's NFC to terminal
        emulate_nfc(nfc_data)
        # Terminal accepts payment (thinks phone is nearby)

**Defense: Time-Based Verification**

.. code-block:: c

    // Detect relay attacks by measuring latency
    #define MAX_NFC_LATENCY_MS 100  // Typical: <50ms
    
    int verify_nfc_transaction(void) {
        uint32_t start = get_millis();
        
        // Send challenge to card
        uint8_t challenge[16];
        generate_random(challenge, 16);
        nfc_transmit(challenge);
        
        // Receive response
        uint8_t response[16];
        nfc_receive(response);
        
        uint32_t latency = get_millis() - start;
        
        if (latency > MAX_NFC_LATENCY_MS) {
            log_alert("Possible NFC relay attack (latency: %d ms)", latency);
            return -1;
        }
        
        return verify_response(response);
    }

NFC Tag Security
=================

**Attack: Malicious NFC Tag**

.. code-block:: text

    Attacker places NFC tag with malicious URL:
    nfc://evil.com/malware.apk
    
    User taps phone → Automatically opens browser → Downloads malware

**Defense: URL Filtering**

.. code-block:: java

    // Android app verifies NFC URLs before opening
    public void onNewIntent(Intent intent) {
        if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(intent.getAction())) {
            Parcelable[] msgs = intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
            NdefMessage msg = (NdefMessage) msgs[0];
            String url = new String(msg.getRecords()[0].getPayload());
            
            // Verify URL is trusted
            if (!isWhitelistedDomain(url)) {
                showWarning("Untrusted NFC tag detected");
                return;
            }
            
            openUrl(url);
        }
    }

Exam Questions
==============

**Q1: NFC vs QR Code for Payments (Medium)**

Compare NFC and QR code for mobile payments. Which is more secure?

**Answer:**

+-------------------+-------------------------+------------------------+
| Feature           | NFC                     | QR Code                |
+===================+=========================+========================+
| Range             | 4-10 cm (hard to relay) | Visual (easier relay)  |
+-------------------+-------------------------+------------------------+
| Secure Element    | ✅ Hardware-isolated    | ❌ Software-only       |
+-------------------+-------------------------+------------------------+
| Phishing          | ⚠️  Rogue terminals     | ✅ User sees URL       |
+-------------------+-------------------------+------------------------+

**Verdict:** NFC more secure (Secure Element), but both have trade-offs.

**Q2: NFC Cloning Attack (Hard)**

Attacker clones employee badge (MIFARE Classic). How to prevent?

**Answer:**

**Vulnerability:** MIFARE Classic uses weak CRYPTO1 cipher (broken in 2008).

**Mitigation:**

1. **Upgrade to MIFARE DESFire:** AES-128 encryption (unbroken)
2. **Challenge-response:** Badge computes HMAC(secret, challenge)
3. **Certificate-based:** Badge has unique private key
4. **Multi-factor:** NFC badge + PIN

**Implementation:**

.. code-block:: c

    // DESFire authentication
    void authenticate_mifare_desfire(uint8_t *badge_id) {
        uint8_t challenge[16];
        generate_random(challenge, 16);
        
        // Send challenge to badge
        desfire_send_challenge(badge_id, challenge);
        
        // Badge computes: response = AES(key, challenge)
        uint8_t response[16];
        desfire_receive_response(response);
        
        // Verify response
        uint8_t expected[16];
        aes128_encrypt(challenge, badge_keys[badge_id], expected);
        
        if (memcmp(response, expected, 16) == 0) {
            unlock_door();
        }
    }

Standards
=========

- **ISO/IEC 14443:** Contactless smart cards
- **ISO/IEC 18092:** NFC interface and protocol
- **EMV:** Payment card security

**END OF DOCUMENT**
