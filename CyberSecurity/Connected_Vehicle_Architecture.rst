====================================================================
Connected Vehicle Architecture Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 21434, UN R155/R156, NIST Cybersecurity Framework

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**Connected Vehicle Components:**

+------------------------+--------------------------------------------------+
| **Component**          | **Function**                                     |
+========================+==================================================+
| **TCU**                | Telematics Control Unit (cellular connectivity)  |
+------------------------+--------------------------------------------------+
| **V2X Module**         | Vehicle-to-Everything communication              |
+------------------------+--------------------------------------------------+
| **Infotainment**       | User interface, entertainment, navigation        |
+------------------------+--------------------------------------------------+
| **Gateway ECU**        | Network bridge (CAN/Ethernet/LIN)                |
+------------------------+--------------------------------------------------+
| **OTA Backend**        | Over-the-air update server (cloud)               |
+------------------------+--------------------------------------------------+

**Attack Surface:**

.. code-block:: text

    Cloud Backend
         ↓ (LTE/5G)
    Telematics Control Unit (TCU)
         ↓
    Gateway ECU ← Entry Point
         ↓
    CAN Bus → ECU1, ECU2, ECU3...
    
    Attack Vectors:
    1. Cloud API compromise
    2. Cellular MITM (rogue base station)
    3. TCU firmware vulnerability
    4. Gateway buffer overflow
    5. CAN bus injection

**Security Architecture:**

- ✅ **Defense in Depth**: Multiple security layers
- ✅ **Zero Trust**: Authenticate every connection
- ✅ **Least Privilege**: Limit TCU access to CAN
- ✅ **OTA Security**: Signed firmware with rollback protection
- ✅ **Intrusion Detection**: Monitor abnormal traffic patterns

Introduction
============

**Connected vehicles** integrate cellular (4G/5G), Wi-Fi, and V2X connectivity,
enabling features like remote diagnostics, OTA updates, and autonomous driving.

**Key Technologies:**

1. **Telematics Control Unit (TCU)**: Cellular modem + GPS + application processor
2. **Vehicle-to-Cloud**: Remote monitoring, OTA updates, fleet management
3. **Vehicle-to-Vehicle (V2V)**: Collision avoidance, platooning
4. **Vehicle-to-Infrastructure (V2I)**: Traffic light optimization, smart parking

**Security Challenges:**

- Large attack surface (cellular, Wi-Fi, Bluetooth, V2X)
- Complex supply chain (OEM, Tier-1 suppliers, cloud providers)
- Long vehicle lifecycle (15+ years) vs. fast-evolving cyber threats
- Safety implications (remote attacks can cause physical harm)

**Standards:**

- **ISO 21434**: Automotive cybersecurity engineering lifecycle
- **UN R155**: Cybersecurity Management System (CSMS)
- **UN R156**: Software Update Management System (SUMS)
- **SAE J3061**: Cybersecurity guidebook for cyber-physical vehicle systems

Telematics Control Unit (TCU) Security
=======================================

**TCU Architecture:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ TCU (Telematics Control Unit)           │
    ├─────────────────────────────────────────┤
    │ Cellular Modem (LTE/5G)                 │
    │  - SIM card (authentication)            │
    │  - Baseband processor                   │
    ├─────────────────────────────────────────┤
    │ Application Processor                   │
    │  - Linux/Android OS                     │
    │  - OTA client                           │
    │  - Remote diagnostics                   │
    ├─────────────────────────────────────────┤
    │ CAN/Ethernet Interface                  │
    │  - Gateway to in-vehicle networks       │
    └─────────────────────────────────────────┘

**Threat Model:**

1. **Rogue Base Station**: Attacker impersonates cellular tower
2. **SIM Cloning**: Extract SIM credentials
3. **Baseband Exploitation**: Vulnerability in modem firmware
4. **OS Compromise**: Linux kernel exploit
5. **Privilege Escalation**: TCU → CAN bus access

**C Code: TCU Secure Boot**

.. code-block:: c

    #include <stdint.h>
    #include <openssl/evp.h>
    #include <openssl/ec.h>
    
    // Verify TCU firmware signature before boot
    int tcu_secure_boot(
        const uint8_t *firmware,
        size_t firmware_len,
        const uint8_t *signature,
        const uint8_t *oem_public_key
    ) {
        // Compute SHA-256 hash of firmware
        uint8_t hash[32];
        EVP_MD_CTX *md_ctx = EVP_MD_CTX_new();
        EVP_DigestInit_ex(md_ctx, EVP_sha256(), NULL);
        EVP_DigestUpdate(md_ctx, firmware, firmware_len);
        EVP_DigestFinal_ex(md_ctx, hash, NULL);
        EVP_MD_CTX_free(md_ctx);
        
        // Parse OEM public key (ECDSA P-256)
        EC_KEY *ec_key = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
        EC_POINT *pub_point = EC_POINT_new(EC_KEY_get0_group(ec_key));
        EC_POINT_oct2point(EC_KEY_get0_group(ec_key), pub_point, 
                          oem_public_key, 65, NULL);
        EC_KEY_set_public_key(ec_key, pub_point);
        
        // Verify ECDSA signature
        ECDSA_SIG *sig = d2i_ECDSA_SIG(NULL, &signature, 64);
        int valid = ECDSA_do_verify(hash, 32, sig, ec_key);
        
        ECDSA_SIG_free(sig);
        EC_POINT_free(pub_point);
        EC_KEY_free(ec_key);
        
        if (valid != 1) {
            printf("SECURE BOOT FAILED: Invalid firmware signature!\n");
            return -1;
        }
        
        printf("Secure boot verified. Loading firmware...\n");
        return 0;
    }

Over-The-Air (OTA) Update Security
===================================

**OTA Update Flow:**

.. code-block:: text

    1. OTA Backend → TCU: "Update available (v2.5)"
    2. TCU → Backend: "Request firmware package"
    3. Backend → TCU: Encrypted firmware + signature
    4. TCU: Verify signature (ECDSA P-256)
    5. TCU: Decrypt firmware (AES-256-GCM)
    6. TCU: Flash firmware to ECU
    7. ECU: Verify signature, reboot
    8. ECU → TCU → Backend: "Update successful"

**Python Code: OTA Client (TCU)**

.. code-block:: python

    #!/usr/bin/env python3
    """
    OTA Update Client for Telematics Control Unit
    """
    
    import requests
    import hashlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes
    from cryptography.exceptions import InvalidSignature
    
    class OTAClient:
        def __init__(self, backend_url, vehicle_id, private_key, backend_cert):
            self.backend_url = backend_url
            self.vehicle_id = vehicle_id
            self.private_key = private_key
            self.backend_cert = backend_cert
        
        def check_for_updates(self):
            """Check OTA backend for available updates"""
            response = requests.get(
                f"{self.backend_url}/api/v1/updates/{self.vehicle_id}",
                cert=self.get_client_cert(),
                verify=self.backend_cert,
                timeout=30
            )
            
            if response.status_code == 200:
                update_info = response.json()
                print(f"Update available: {update_info['version']}")
                return update_info
            else:
                print("No updates available")
                return None
        
        def download_firmware(self, update_id):
            """Download encrypted firmware package"""
            response = requests.get(
                f"{self.backend_url}/api/v1/firmware/{update_id}",
                cert=self.get_client_cert(),
                verify=self.backend_cert,
                stream=True,
                timeout=300
            )
            
            if response.status_code != 200:
                raise Exception(f"Download failed: {response.status_code}")
            
            # Download encrypted firmware
            encrypted_firmware = response.content
            signature = response.headers['X-Firmware-Signature']
            
            return encrypted_firmware, bytes.fromhex(signature)
        
        def verify_and_decrypt(self, encrypted_firmware, signature, encryption_key):
            """Verify signature and decrypt firmware"""
            
            # Step 1: Verify ECDSA P-256 signature
            public_key = self.backend_cert.public_key()
            
            try:
                public_key.verify(
                    signature,
                    encrypted_firmware,
                    ec.ECDSA(hashes.SHA256())
                )
                print("✓ Firmware signature verified")
            except InvalidSignature:
                raise Exception("CRITICAL: Invalid firmware signature!")
            
            # Step 2: Decrypt with AES-256-GCM
            aesgcm = AESGCM(encryption_key)
            nonce = encrypted_firmware[:12]
            ciphertext = encrypted_firmware[12:]
            
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            print(f"✓ Firmware decrypted ({len(plaintext)} bytes)")
            
            return plaintext
        
        def flash_firmware(self, ecu_id, firmware_data):
            """Flash firmware to target ECU via CAN"""
            print(f"Flashing firmware to ECU {ecu_id}...")
            
            # Send firmware via UDS (ISO 14229)
            # Service 0x34: RequestDownload
            # Service 0x36: TransferData
            # Service 0x37: RequestTransferExit
            
            chunk_size = 256
            for i in range(0, len(firmware_data), chunk_size):
                chunk = firmware_data[i:i+chunk_size]
                self.send_uds_transfer_data(ecu_id, chunk)
                print(f"Progress: {(i+chunk_size)/len(firmware_data)*100:.1f}%")
            
            print("✓ Firmware flashed successfully")
        
        def rollback_protection(self, current_version, new_version):
            """Prevent downgrade attacks"""
            if new_version <= current_version:
                raise Exception(f"Rollback detected! Current: {current_version}, New: {new_version}")
            
            print(f"✓ Version check passed ({current_version} → {new_version})")

Gateway ECU Security
====================

**Gateway Functions:**

1. **Network bridge**: CAN ↔ Ethernet ↔ LIN
2. **Message filtering**: Block unauthorized frames
3. **Protocol translation**: Convert between bus protocols
4. **Security enforcement**: Firewall for in-vehicle networks

**Attack Scenarios:**

- Compromised TCU sends malicious CAN frames via gateway
- Buffer overflow in gateway firmware
- Gateway bypass (direct CAN access)

**C Code: Gateway Firewall**

.. code-block:: c

    #include <stdint.h>
    #include <stdbool.h>
    
    #define MAX_CAN_ID 0x7FF
    
    typedef struct {
        bool allowed;
        uint8_t source_network;  // 0=CAN, 1=Ethernet, 2=LIN
        uint8_t dest_network;
        bool requires_auth;
    } gateway_rule_t;
    
    gateway_rule_t gateway_rules[MAX_CAN_ID + 1];
    
    // Initialize gateway firewall rules
    void gateway_init_firewall(void) {
        // Default: deny all
        for (int i = 0; i <= MAX_CAN_ID; i++) {
            gateway_rules[i].allowed = false;
        }
        
        // Allow specific CAN IDs from Ethernet (TCU)
        gateway_rules[0x100].allowed = true;  // Diagnostics (authenticated)
        gateway_rules[0x100].source_network = 1;  // Ethernet
        gateway_rules[0x100].dest_network = 0;    // CAN
        gateway_rules[0x100].requires_auth = true;
        
        // Block safety-critical frames from external networks
        gateway_rules[0x200].allowed = false;  // Steering control (never allow from TCU)
        gateway_rules[0x201].allowed = false;  // Brake control
    }
    
    // Process frame through gateway
    int gateway_forward_frame(
        uint8_t source_network,
        uint8_t dest_network,
        uint16_t can_id,
        const uint8_t *data,
        uint8_t dlc,
        bool authenticated
    ) {
        // Check firewall rules
        if (can_id > MAX_CAN_ID) {
            printf("Gateway: Invalid CAN ID 0x%03X\n", can_id);
            return -1;
        }
        
        gateway_rule_t *rule = &gateway_rules[can_id];
        
        if (!rule->allowed) {
            printf("Gateway: Blocked CAN ID 0x%03X (not in whitelist)\n", can_id);
            log_security_event("Gateway blocked frame", can_id);
            return -1;
        }
        
        if (rule->source_network != source_network) {
            printf("Gateway: Wrong source network for CAN ID 0x%03X\n", can_id);
            return -1;
        }
        
        if (rule->requires_auth && !authenticated) {
            printf("Gateway: CAN ID 0x%03X requires authentication\n", can_id);
            return -1;
        }
        
        // Forward frame
        printf("Gateway: Forwarding CAN ID 0x%03X (network %u → %u)\n",
               can_id, source_network, dest_network);
        
        return can_send_frame(can_id, data, dlc);
    }

Cloud Backend Security
======================

**Backend Architecture:**

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │ Cloud Backend (AWS/Azure/GCP)           │
    ├─────────────────────────────────────────┤
    │ API Gateway (authentication)            │
    │  ↓                                      │
    │ Vehicle Management Service              │
    │  - Fleet database                       │
    │  - OTA orchestration                    │
    │  ↓                                      │
    │ Firmware Repository                     │
    │  - Signed firmware packages             │
    │  - Version control                      │
    └─────────────────────────────────────────┘

**Security Requirements:**

1. **Authentication**: Mutual TLS (vehicle ↔ backend)
2. **Authorization**: Role-based access control (RBAC)
3. **Encryption**: TLS 1.3 for data in transit, AES-256 for data at rest
4. **Logging**: Audit all API calls (forensics)
5. **Rate Limiting**: Prevent DoS attacks

**Python Code: Backend API (Flask)**

.. code-block:: python

    from flask import Flask, request, jsonify
    from functools import wraps
    import jwt
    
    app = Flask(__name__)
    
    def require_vehicle_auth(f):
        """Decorator to require vehicle authentication"""
        @wraps(f)
        def decorated(*args, **kwargs):
            # Verify client certificate (mutual TLS)
            cert = request.environ.get('SSL_CLIENT_CERT')
            if not cert:
                return jsonify({'error': 'Client certificate required'}), 401
            
            # Extract vehicle ID from certificate
            vehicle_id = extract_vehicle_id_from_cert(cert)
            
            # Verify vehicle is registered
            if not is_vehicle_registered(vehicle_id):
                return jsonify({'error': 'Vehicle not registered'}), 403
            
            return f(vehicle_id=vehicle_id, *args, **kwargs)
        
        return decorated
    
    @app.route('/api/v1/updates/<vehicle_id>', methods=['GET'])
    @require_vehicle_auth
    def check_updates(vehicle_id):
        """Check if firmware updates are available"""
        
        # Query database for vehicle's current firmware version
        current_version = get_vehicle_firmware_version(vehicle_id)
        
        # Check if newer version exists
        latest_version = get_latest_firmware_version()
        
        if latest_version > current_version:
            return jsonify({
                'update_available': True,
                'version': latest_version,
                'update_id': generate_update_id(),
                'size_bytes': get_firmware_size(latest_version),
                'release_notes': get_release_notes(latest_version)
            })
        else:
            return jsonify({'update_available': False})
    
    @app.route('/api/v1/firmware/<update_id>', methods=['GET'])
    @require_vehicle_auth
    def download_firmware(vehicle_id, update_id):
        """Download encrypted firmware package"""
        
        # Verify update_id belongs to this vehicle
        if not verify_update_ownership(vehicle_id, update_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Load firmware package
        firmware_data = load_firmware_package(update_id)
        
        # Sign firmware (ECDSA P-256)
        signature = sign_firmware(firmware_data, backend_private_key)
        
        # Return encrypted firmware with signature
        response = make_response(firmware_data)
        response.headers['X-Firmware-Signature'] = signature.hex()
        response.headers['Content-Type'] = 'application/octet-stream'
        
        return response

Exam Questions
==============

Question 1: TCU Attack Surface (Difficulty: Medium)
----------------------------------------------------

A vehicle's TCU has the following interfaces:

1. LTE cellular modem (connects to internet)
2. CAN bus (connects to 30 ECUs)
3. Bluetooth (connects to smartphone)
4. GPS receiver

An attacker wants to remotely control the vehicle's brakes.

**a)** Describe the attack path from internet to brake ECU.

**b)** Propose three security controls to prevent this attack.

**Answer:**

**a) Attack Path:**

.. code-block:: text

    Step 1: Exploit cellular modem vulnerability
    Internet → Rogue Base Station → TCU Modem → Buffer Overflow
    
    Step 2: Gain code execution on TCU application processor
    Modem shellcode → Privilege escalation → Root access on Linux OS
    
    Step 3: Send malicious CAN frames from TCU
    TCU → Gateway ECU → CAN Bus → Brake ECU (CAN ID 0x201)
    
    Step 4: Brake ECU receives malicious command
    "Apply full brake" (no authentication) → Accident

**b) Security Controls:**

**Control 1: Gateway Firewall**
- Block TCU from sending brake commands (CAN ID 0x201)
- Whitelist only diagnostic frames (authenticated)

**Control 2: CAN Message Authentication (SecOC)**
- Brake ECU verifies CMAC on every CAN frame
- TCU does not have keys for safety-critical messages

**Control 3: TCU Isolation**
- Run modem baseband in separate security domain (ARM TrustZone)
- Even if modem compromised, cannot access application processor

Question 2: OTA Update Attack (Difficulty: Hard)
-------------------------------------------------

An attacker intercepts an OTA update using MITM attack:

.. code-block:: text

    OTA Backend → [ATTACKER] → TCU

The attacker replaces firmware with malicious version.

**a)** What cryptographic mechanisms prevent this attack?

**b)** If attacker has access to OEM's signing key, how can rollback protection help?

**Answer:**

**a) Cryptographic Protections:**

**Protection 1: Digital Signature (ECDSA P-256)**
- Backend signs firmware with private key
- TCU verifies signature with OEM public key (embedded in secure storage)
- Attacker cannot forge valid signature without private key

**Protection 2: TLS 1.3 (Mutual Authentication)**
- TCU verifies backend's certificate (prevents fake backend)
- Backend verifies TCU's certificate (prevents unauthorized vehicles)
- Attacker cannot MITM without breaking TLS

**Protection 3: Encryption (AES-256-GCM)**
- Firmware encrypted with vehicle-specific key
- Even if attacker captures update, cannot read/modify plaintext

**b) Rollback Protection (Compromised Signing Key):**

If attacker has signing key, they can sign malicious firmware. However:

.. code-block:: c

    // TCU maintains monotonic version counter (stored in secure element)
    uint32_t secure_firmware_version = read_secure_counter();
    
    // New firmware version must be higher
    if (new_firmware_version <= secure_firmware_version) {
        printf("ROLLBACK ATTACK DETECTED!\n");
        return -1;  // Reject update
    }
    
    // After successful update, increment secure counter
    increment_secure_counter(new_firmware_version);

**Attacker cannot:**
- Downgrade to old firmware with known vulnerabilities
- Replay old (signed) firmware packages

**However:**
- Attacker can sign NEW malicious firmware (version > current)
- Rollback protection does not prevent this

**Additional Defense:**
- Hardware Security Module (HSM) should detect abnormal signing requests
- Key ceremony with multiple approvers (threshold signature)

Question 3: Gateway Bypass (Difficulty: Hard)
----------------------------------------------

Design a gateway that prevents a compromised TCU from injecting malicious CAN frames, while still allowing legitimate diagnostics.

**Answer:**

.. code-block:: c

    #include <stdint.h>
    #include <stdbool.h>
    
    // Multi-layer gateway security
    
    // Layer 1: Whitelist + Authentication
    typedef struct {
        uint16_t can_id;
        bool allowed_from_tcu;
        bool requires_authentication;
        bool (*payload_validator)(const uint8_t *data, uint8_t dlc);
    } gateway_policy_t;
    
    gateway_policy_t policies[] = {
        // Diagnostic frames: allowed with auth
        {0x7DF, true, true, validate_diagnostic_request},
        
        // Safety-critical: NEVER allowed from TCU
        {0x200, false, false, NULL},  // Steering
        {0x201, false, false, NULL},  // Brake
        {0x202, false, false, NULL},  // Throttle
    };
    
    // Layer 2: Rate Limiting
    #define MAX_FRAMES_PER_SECOND 10
    uint32_t tcu_frame_count = 0;
    uint64_t last_rate_limit_reset = 0;
    
    // Layer 3: Payload Validation
    bool validate_diagnostic_request(const uint8_t *data, uint8_t dlc) {
        if (dlc < 2) return false;
        
        uint8_t service = data[0];
        
        // Only allow read services, not write/control
        switch (service) {
            case 0x19:  // ReadDTCInformation
            case 0x22:  // ReadDataByIdentifier
                return true;
            
            case 0x2E:  // WriteDataByIdentifier (BLOCKED)
            case 0x31:  // RoutineControl (BLOCKED)
                return false;
            
            default:
                return false;
        }
    }
    
    // Gateway forward with multi-layer checks
    int gateway_secure_forward(
        uint16_t can_id,
        const uint8_t *data,
        uint8_t dlc,
        const uint8_t *hmac_tag
    ) {
        // Layer 1: Find policy
        gateway_policy_t *policy = find_policy(can_id);
        if (!policy || !policy->allowed_from_tcu) {
            return -1;  // Blocked
        }
        
        // Layer 2: Check authentication
        if (policy->requires_authentication) {
            if (!verify_hmac(can_id, data, dlc, hmac_tag)) {
                printf("Authentication failed for CAN ID 0x%03X\n", can_id);
                return -1;
            }
        }
        
        // Layer 3: Validate payload
        if (policy->payload_validator) {
            if (!policy->payload_validator(data, dlc)) {
                printf("Payload validation failed for CAN ID 0x%03X\n", can_id);
                return -1;
            }
        }
        
        // Layer 4: Rate limiting
        uint64_t now = get_time_ms();
        if (now - last_rate_limit_reset > 1000) {
            tcu_frame_count = 0;
            last_rate_limit_reset = now;
        }
        
        if (++tcu_frame_count > MAX_FRAMES_PER_SECOND) {
            printf("Rate limit exceeded for TCU\n");
            return -1;
        }
        
        // All checks passed, forward frame
        return can_send_frame(can_id, data, dlc);
    }

Conclusion
==========

Connected vehicle architecture introduces significant attack surface through
cellular, Wi-Fi, and V2X connectivity. Key security principles:

1. **Defense in Depth**: Multiple security layers (TCU → Gateway → ECU)
2. **Secure OTA**: Signed and encrypted firmware updates
3. **Gateway Firewall**: Restrict TCU access to safety-critical ECUs
4. **Intrusion Detection**: Monitor for abnormal behavior
5. **Zero Trust**: Authenticate every connection and command

**Standards Compliance:**
- ISO 21434: Cybersecurity engineering
- UN R155: CSMS (Cybersecurity Management System)
- UN R156: SUMS (Software Update Management System)
- SAE J3061: Cybersecurity guidebook

**END OF DOCUMENT**
