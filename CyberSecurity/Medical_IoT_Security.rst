====================================================================
Medical IoT Security - Connected Healthcare Device Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: FDA, HIPAA, GDPR, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Medical IoT Devices:**

- **Examples:** Glucose monitors, wearable ECG, smart pills, remote patient monitoring
- **Connectivity:** Bluetooth, WiFi, LoRaWAN, cellular (4G/5G)
- **Data:** PHI (Protected Health Information) - HIPAA regulated

**Security Priorities:**

✅ **Patient safety:** Device malfunction cannot harm patient
✅ **Data privacy:** Encrypt PHI at rest and in transit
✅ **Authentication:** Prevent unauthorized device control
✅ **Availability:** Device must function during network outage

Introduction
============

**Medical IoT** includes connected devices that monitor or treat patients remotely.

**Threat Model:**

1. **Patient harm:** Malicious insulin dose adjustment
2. **Privacy breach:** Leak patient health data
3. **Ransomware:** Lock device until payment
4. **Supply chain:** Counterfeit devices with backdoors

Medical IoT Architecture
=========================

.. code-block:: text

    ┌──────────────┐
    │   Patient    │
    └───────┬──────┘
            │
    ┌───────▼────────────┐
    │ Wearable ECG       │  (Bluetooth Low Energy)
    │ ├─ Sensors         │
    │ ├─ ARM Cortex-M4   │
    │ └─ BLE 5.0         │
    └───────┬────────────┘
            │ BLE
    ┌───────▼────────────┐
    │ Smartphone Gateway │  (WiFi/LTE)
    │ ├─ Health App      │
    │ └─ Encrypted upload│
    └───────┬────────────┘
            │ HTTPS (TLS 1.3)
    ┌───────▼────────────┐
    │ Cloud EHR          │
    │ ├─ HIPAA compliant │
    │ └─ Doctor access   │
    └────────────────────┘

BLE Security for Medical Wearables
====================================

**Vulnerability: BLE Pairing (MITM)**

.. code-block:: python

    # Attacker intercepts pairing between ECG and smartphone
    def ble_mitm_attack():
        # Sniff BLE pairing
        pairing_packet = sniff_ble_pairing()
        
        # If using "Just Works" pairing (no PIN)
        if pairing_packet.method == 'JUST_WORKS':
            # Attacker can impersonate device
            fake_device = BLE_Device(name='ECG Monitor')
            fake_device.accept_pairing(smartphone)
            
            # Smartphone now sends patient data to attacker
            data = smartphone.send_ecg_data()
            print(f"Stolen ECG data: {data}")

**Mitigation: Secure BLE Pairing**

.. code-block:: c

    #include <bluez/bluetooth.h>
    
    // Use "Passkey Entry" or "Numeric Comparison" pairing
    void ble_secure_pairing(void) {
        // Display 6-digit PIN on ECG device screen
        uint32_t passkey = generate_random_passkey();  // e.g., 123456
        display_on_screen(passkey);
        
        // User enters passkey on smartphone
        // Pairing only succeeds if passkey matches
        if (entered_passkey == passkey) {
            // Generate encryption keys
            generate_ltk();  // Long-Term Key
            enable_encryption();
        }
    }

Data Encryption (HIPAA Compliance)
===================================

**Requirement:** Encrypt PHI at rest and in transit.

**Example: Glucose Monitor**

.. code-block:: c

    #include <mbedtls/aes.h>
    #include <mbedtls/gcm.h>
    
    typedef struct {
        uint32_t timestamp;
        uint16_t glucose_mg_dl;
        uint8_t patient_id[16];
    } glucose_reading_t;
    
    // Encrypt glucose reading with AES-GCM
    void encrypt_glucose_reading(glucose_reading_t *reading, uint8_t *ciphertext) {
        mbedtls_gcm_context gcm;
        uint8_t key[32];  // Device-unique encryption key
        uint8_t iv[12];   // Random IV for each reading
        uint8_t tag[16];  // Authentication tag
        
        // Initialize AES-GCM
        mbedtls_gcm_init(&gcm);
        mbedtls_gcm_setkey(&gcm, MBEDTLS_CIPHER_ID_AES, key, 256);
        
        // Encrypt
        mbedtls_gcm_crypt_and_tag(&gcm, MBEDTLS_GCM_ENCRYPT,
            sizeof(glucose_reading_t), iv, 12,
            NULL, 0,  // No additional authenticated data
            (uint8_t*)reading, ciphertext, 16, tag);
        
        // Transmit: IV + Ciphertext + Tag
        ble_transmit(iv, 12);
        ble_transmit(ciphertext, sizeof(glucose_reading_t));
        ble_transmit(tag, 16);
    }

Cloud Backend Security
=======================

**Authentication: OAuth 2.0 + JWT**

.. code-block:: python

    from flask import Flask, request, jsonify
    import jwt
    
    app = Flask(__name__)
    SECRET_KEY = 'your-secret-key'  # Store in HSM/vault
    
    @app.route('/api/upload_ecg', methods=['POST'])
    def upload_ecg():
        # Verify JWT token
        token = request.headers.get('Authorization').split(' ')[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            device_id = payload['device_id']
            patient_id = payload['patient_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Verify device is authorized for this patient
        if not is_authorized(device_id, patient_id):
            return jsonify({'error': 'Unauthorized device'}), 403
        
        # Store ECG data (encrypted at rest)
        ecg_data = request.get_json()
        store_encrypted(patient_id, ecg_data)
        
        return jsonify({'status': 'success'})

**Database Encryption (at rest):**

.. code-block:: sql

    -- PostgreSQL with pgcrypto extension
    CREATE EXTENSION pgcrypto;
    
    CREATE TABLE patient_ecg (
        patient_id UUID,
        timestamp TIMESTAMP,
        ecg_data BYTEA  -- Encrypted with AES-256
    );
    
    -- Insert encrypted data
    INSERT INTO patient_ecg (patient_id, timestamp, ecg_data)
    VALUES (
        'a1b2c3...',
        NOW(),
        pgp_sym_encrypt('{"heart_rate": 72, "rhythm": "sinus"}', 'encryption-key')
    );
    
    -- Query decrypted data (only authorized users)
    SELECT patient_id, timestamp, 
           pgp_sym_decrypt(ecg_data, 'encryption-key') AS decrypted_data
    FROM patient_ecg
    WHERE patient_id = 'a1b2c3...';

Exam Questions
==============

**Q1: HIPAA Breach Scenario (Medium)**

A wearable glucose monitor transmits data to cloud over HTTP (no TLS). Attacker intercepts traffic and obtains 1000 patient glucose readings. What are the consequences?

**Answer:**

**HIPAA Violation:**

- **Breach notification required** (notify affected patients within 60 days)
- **HHS reporting** (if >500 patients affected)
- **Fines:** $100-$50,000 per violation (potentially $50M for 1000 patients)

**Manufacturer Liability:**

- **FDA enforcement action** (recall, warning letter)
- **Class action lawsuit** from patients
- **Reputational damage**

**Required Remediation:**

1. **Immediate:** Firmware update enforcing TLS 1.3
2. **Notify patients:** Offer credit monitoring (identity theft risk)
3. **Root cause analysis:** Why was TLS not required?
4. **Process improvement:** Security review in design phase

**Q2: Remote Patient Monitoring Resilience (Hard)**

A cardiac monitor sends real-time ECG to cloud. If internet fails, patient could die before alert reaches doctor. Design resilient architecture.

**Answer:**

**Tiered Alerting:**

.. code-block:: text

    Tier 1: Local Alert (0 seconds delay)
    ├─ Abnormal ECG detected on device
    ├─ Vibration + audible alarm
    └─ Patient calls 911

    Tier 2: Smartphone Alert (1 second delay)
    ├─ BLE notification to paired phone
    ├─ App displays "Seek medical attention"
    └─ Auto-dial emergency contact

    Tier 3: Cloud Alert (5 seconds delay)
    ├─ HTTPS upload to cloud
    ├─ Doctor notification (SMS + app)
    └─ EMS dispatch (if no response)

**Failover Mechanisms:**

1. **Offline buffering:** Device stores 24 hours of ECG data
2. **Multiple connectivity:** WiFi → cellular → Bluetooth tethering
3. **Edge processing:** Detect life-threatening arrhythmias locally (no cloud needed)

Standards
=========

- **HIPAA Security Rule:** PHI encryption requirements
- **FDA Guidance (2023):** Cybersecurity for medical devices
- **GDPR:** European patient data protection
- **IEC 62443:** Industrial/medical device security

**END OF DOCUMENT**
