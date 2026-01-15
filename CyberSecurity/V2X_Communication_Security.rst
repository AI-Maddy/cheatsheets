====================================================================
V2X Communication Security (Vehicle-to-Everything)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEEE 1609, SAE J2945, ETSI ITS, ISO 21434, 3GPP C-V2X

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**V2X Security Essentials:**

+------------------+-------------------------------------------------------+
| **V2X Type**     | **Description**                                       |
+==================+=======================================================+
| **V2V**          | Vehicle-to-Vehicle (collision warning, platooning)    |
+------------------+-------------------------------------------------------+
| **V2I**          | Vehicle-to-Infrastructure (traffic lights, RSU)       |
+------------------+-------------------------------------------------------+
| **V2P**          | Vehicle-to-Pedestrian (smartphone alerts)             |
+------------------+-------------------------------------------------------+
| **V2N**          | Vehicle-to-Network (cloud services, cellular)         |
+------------------+-------------------------------------------------------+

**V2X Technologies:**

.. code-block:: text

    DSRC (Dedicated Short-Range Communications)
    ├─ IEEE 802.11p (WiFi variant)
    ├─ 5.9 GHz frequency band
    ├─ Range: 300-1000 meters
    └─ Latency: 20-50 ms
    
    C-V2X (Cellular V2X)
    ├─ LTE-V2X (4G-based)
    ├─ 5G NR-V2X (5G-based)
    ├─ Range: 1-2 km
    └─ Latency: <20 ms (5G), <50 ms (LTE)

**Security Architecture:**

.. code-block:: text

    V2X Message
         ↓
    ┌──────────────────────────────────────┐
    │ Certificate-Based Authentication     │
    │ - X.509 certificates (IEEE 1609.2)   │
    │ - ECDSA P-256 signatures             │
    └──────────────────────────────────────┘
         ↓
    ┌──────────────────────────────────────┐
    │ Security Credential Management       │
    │ System (SCMS)                        │
    │ - Certificate issuance               │
    │ - Pseudonym management               │
    │ - Revocation                         │
    └──────────────────────────────────────┘

**Threat Model:**

1. ⚠️ **Message spoofing**: Fake emergency brake warning
2. ⚠️ **Replay attacks**: Re-broadcast old messages
3. ⚠️ **Sybil attacks**: One vehicle pretends to be many
4. ⚠️ **Privacy violation**: Track vehicle movements
5. ⚠️ **DoS attacks**: Flood V2X channel with fake messages

**Key Security Mechanisms:**

- ✅ Digital signatures (ECDSA P-256) on every message
- ✅ Pseudonymous certificates (changed every 5 minutes)
- ✅ Timestamp validation (reject old messages)
- ✅ Location plausibility checks
- ✅ Certificate revocation (CRL distribution)

Introduction to V2X Communication
==================================

**V2X (Vehicle-to-Everything)** enables vehicles to communicate with each other
and infrastructure to improve safety and efficiency.

**Use Cases:**

1. **Collision Avoidance**: Forward collision warning, intersection collision warning
2. **Cooperative Adaptive Cruise Control (CACC)**: Vehicle platooning
3. **Traffic Optimization**: Traffic light priority for emergency vehicles
4. **Pedestrian Safety**: Alert drivers to pedestrians crossing
5. **Remote Driving**: 5G-enabled teleoperation

**Standards Landscape:**

- **US/Americas**: IEEE 1609 (WAVE), SAE J2945
- **Europe**: ETSI ITS (Intelligent Transport Systems)
- **China**: C-V2X (3GPP standards)
- **Global**: ISO 21434 (cybersecurity), UN R155/R156

V2X Technologies: DSRC vs. C-V2X
=================================

DSRC (Dedicated Short-Range Communications)
--------------------------------------------

**Technology:**

- Based on **IEEE 802.11p** (modified WiFi)
- Frequency: **5.9 GHz** (5.85-5.925 GHz)
- Channel bandwidth: 10 MHz (vs. 20 MHz for WiFi)
- Modulation: OFDM (similar to WiFi)

**Performance:**

- Range: 300-1000 meters (depends on environment)
- Latency: 20-50 ms
- Data rate: 3-27 Mbps (typically 6-12 Mbps used)

**Advantages:**

- Low latency (no infrastructure required)
- Direct V2V communication (ad-hoc network)
- Proven technology (deployed in US, Europe)

**Disadvantages:**

- Limited range (compared to cellular)
- No integration with existing cellular networks
- Requires roadside units (RSU) for V2I

C-V2X (Cellular V2X)
--------------------

**Technology:**

- **LTE-V2X** (4G-based): 3GPP Release 14
- **5G NR-V2X** (5G New Radio): 3GPP Release 16

**Two Modes:**

1. **Direct Mode (PC5 interface)**: V2V, V2I, V2P (no cellular network)
2. **Network Mode (Uu interface)**: V2N via cellular tower

**Performance:**

- Range: 1-2 km (direct mode), unlimited (network mode)
- Latency: <20 ms (5G), <50 ms (LTE)
- Data rate: Up to 1 Gbps (5G)

**Advantages:**

- Higher range and reliability
- Integration with 5G ecosystem (edge computing, slicing)
- Better support for future autonomous vehicles

**Disadvantages:**

- Requires cellular network (for network mode)
- Higher complexity and cost
- Standardization still evolving

V2X Security Architecture (IEEE 1609.2)
========================================

IEEE 1609.2 Security Overview
------------------------------

**IEEE 1609.2** defines cryptographic security for V2X communications.

**Key Components:**

1. **Signed Messages**: Every V2X message digitally signed (ECDSA P-256)
2. **Certificates**: X.509-like certificates for authentication
3. **Pseudonyms**: Short-lived certificates to protect privacy
4. **Certificate Chain**: Root CA → Enrollment CA → Pseudonym CA

**Message Security Format:**

.. code-block:: text

    V2X Message Structure:
    ┌─────────────────────────────────────────────────┐
    │ Header                                          │
    │  - Protocol version                             │
    │  - Message type (BSM, SPAT, MAP, etc.)          │
    ├─────────────────────────────────────────────────┤
    │ Payload (e.g., Basic Safety Message)            │
    │  - Position (lat, lon)                          │
    │  - Speed, heading, acceleration                 │
    │  - Vehicle size, type                           │
    ├─────────────────────────────────────────────────┤
    │ Security Header (IEEE 1609.2)                   │
    │  - Signer certificate (pseudonym)               │
    │  - Generation time (timestamp)                  │
    │  - Generation location (optional)               │
    ├─────────────────────────────────────────────────┤
    │ Signature (ECDSA P-256)                         │
    │  - 64 bytes (32-byte r, 32-byte s)              │
    └─────────────────────────────────────────────────┘

Basic Safety Message (BSM) - SAE J2735
---------------------------------------

**BSM** is the most common V2X message, broadcast 10 times per second.

**BSM Part 1 (Core Data):**

- Position (latitude, longitude, elevation)
- Speed, heading, acceleration
- Brake status, steering wheel angle
- Vehicle size (length, width)

**BSM Part 2 (Optional Data):**

- Path history (last 23 seconds of positions)
- Path prediction (future trajectory)
- Exterior lights status
- Wiper status (indicates rain)

**Security Requirements:**

- Every BSM must be signed (ECDSA P-256)
- Signature verification: <5 ms (to maintain 100 ms processing budget)
- Certificate changed every 5 minutes (pseudonym)

C Code: BSM Generation and Signing
-----------------------------------

.. code-block:: c

    #include <stdint.h>
    #include <string.h>
    #include <openssl/ecdsa.h>
    #include <openssl/sha.h>
    
    // Basic Safety Message structure (simplified)
    typedef struct {
        uint32_t msg_count;      // Message counter (0-127, wraps)
        int32_t  latitude;       // Degrees * 1e7
        int32_t  longitude;      // Degrees * 1e7
        int16_t  elevation;      // Meters * 10
        uint16_t speed;          // m/s * 50
        uint16_t heading;        // Degrees * 80
        int16_t  accel_lon;      // Longitudinal accel (m/s²) * 100
        int16_t  accel_lat;      // Lateral accel (m/s²) * 100
        uint8_t  brake_status;   // Bit flags
        uint16_t vehicle_length; // cm
        uint16_t vehicle_width;  // cm
    } __attribute__((packed)) bsm_core_t;
    
    // IEEE 1609.2 Security Header (simplified)
    typedef struct {
        uint8_t  protocol_version;
        uint8_t  content_type;
        uint64_t generation_time;  // Microseconds since 2004-01-01 UTC
        uint8_t  signer_cert[150]; // Pseudonym certificate (DER)
        uint16_t signer_cert_len;
    } ieee1609_security_header_t;
    
    // Sign BSM with ECDSA P-256
    int sign_bsm(
        const bsm_core_t *bsm,
        const uint8_t *private_key,      // 32-byte ECDSA private key
        const uint8_t *certificate,      // Pseudonym certificate
        uint16_t cert_len,
        uint8_t *signature_r,            // Output: 32 bytes
        uint8_t *signature_s             // Output: 32 bytes
    ) {
        EC_KEY *ec_key = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
        BIGNUM *bn_priv = BN_bin2bn(private_key, 32, NULL);
        EC_KEY_set_private_key(ec_key, bn_priv);
        
        // Compute public key from private key
        const EC_GROUP *group = EC_KEY_get0_group(ec_key);
        EC_POINT *pub_key = EC_POINT_new(group);
        EC_POINT_mul(group, pub_key, bn_priv, NULL, NULL, NULL);
        EC_KEY_set_public_key(ec_key, pub_key);
        
        // Construct data to be signed: BSM + Security Header
        uint8_t to_be_signed[512];
        size_t offset = 0;
        
        // Add BSM
        memcpy(to_be_signed + offset, bsm, sizeof(bsm_core_t));
        offset += sizeof(bsm_core_t);
        
        // Add Security Header (simplified)
        ieee1609_security_header_t sec_hdr = {
            .protocol_version = 0x03,
            .content_type = 0x01,  // Signed data
            .generation_time = get_current_time_microseconds(),
            .signer_cert_len = cert_len
        };
        memcpy(sec_hdr.signer_cert, certificate, cert_len);
        
        memcpy(to_be_signed + offset, &sec_hdr, sizeof(ieee1609_security_header_t));
        offset += sizeof(ieee1609_security_header_t);
        
        // Compute SHA-256 hash
        uint8_t hash[32];
        SHA256(to_be_signed, offset, hash);
        
        // Sign hash with ECDSA
        ECDSA_SIG *sig = ECDSA_do_sign(hash, 32, ec_key);
        const BIGNUM *r = ECDSA_SIG_get0_r(sig);
        const BIGNUM *s = ECDSA_SIG_get0_s(sig);
        
        // Extract r and s
        BN_bn2bin(r, signature_r);
        BN_bn2bin(s, signature_s);
        
        // Cleanup
        ECDSA_SIG_free(sig);
        EC_POINT_free(pub_key);
        BN_free(bn_priv);
        EC_KEY_free(ec_key);
        
        return 0;
    }
    
    // Verify BSM signature
    int verify_bsm(
        const bsm_core_t *bsm,
        const uint8_t *certificate,  // Sender's pseudonym certificate
        uint16_t cert_len,
        const uint8_t *signature_r,
        const uint8_t *signature_s
    ) {
        // Extract public key from certificate (X.509 parsing)
        EC_KEY *ec_key = parse_certificate_public_key(certificate, cert_len);
        
        // Reconstruct data that was signed
        uint8_t to_be_signed[512];
        size_t offset = 0;
        memcpy(to_be_signed + offset, bsm, sizeof(bsm_core_t));
        offset += sizeof(bsm_core_t);
        // ... (add security header)
        
        // Compute hash
        uint8_t hash[32];
        SHA256(to_be_signed, offset, hash);
        
        // Verify signature
        ECDSA_SIG *sig = ECDSA_SIG_new();
        BIGNUM *r = BN_bin2bn(signature_r, 32, NULL);
        BIGNUM *s = BN_bin2bn(signature_s, 32, NULL);
        ECDSA_SIG_set0(sig, r, s);
        
        int valid = ECDSA_do_verify(hash, 32, sig, ec_key);
        
        ECDSA_SIG_free(sig);
        EC_KEY_free(ec_key);
        
        return valid;  // 1 = valid, 0 = invalid
    }

Security Credential Management System (SCMS)
=============================================

SCMS Architecture
-----------------

**SCMS** is a PKI infrastructure for V2X certificate management.

**SCMS Components:**

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │           Root Certificate Authority (Root CA)  │
    │  - Issues certificates to intermediate CAs      │
    │  - Offline, highly secured                      │
    └──────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         ↓                            ↓
    ┌──────────────────────┐   ┌──────────────────────┐
    │ Enrollment CA (ECA)  │   │ Pseudonym CA (PCA)   │
    │ - Long-term identity │   │ - Short-term certs   │
    │ - Vehicle enrollment │   │ - Pseudonym pool     │
    └──────────┬───────────┘   └──────────┬───────────┘
               │                          │
               └──────────┬───────────────┘
                          ↓
                  ┌───────────────┐
                  │   Vehicle OBU │
                  │  (On-Board    │
                  │   Unit)       │
                  └───────────────┘

**Certificate Types:**

1. **Enrollment Certificate**:
   
   - Long-term identity (valid 3 years)
   - Used to request pseudonym certificates
   - Never used for V2X messaging (privacy)

2. **Pseudonym Certificate**:
   
   - Short-term (valid 1 week)
   - Vehicle receives batch of ~1000 pseudonyms
   - Changed every 5 minutes during driving
   - Used for signing BSMs

3. **Authorization Certificate**:
   
   - Grants permission to send specific message types
   - Example: Only emergency vehicles can send SPAT (traffic light control)

Pseudonym Management (Privacy Protection)
------------------------------------------

**Problem:**

If vehicle uses same certificate for all BSMs, attacker can track vehicle
movements (privacy violation).

**Solution: Pseudonym Rotation**

.. code-block:: text

    Time: 0:00   → Certificate A (ID: 0x1234)
    Time: 5:00   → Certificate B (ID: 0x5678)  ← Changed
    Time: 10:00  → Certificate C (ID: 0xABCD)  ← Changed
    Time: 15:00  → Certificate D (ID: 0xDEF0)  ← Changed

**Pseudonym Pool:**

- Vehicle requests 1000 pseudonym certificates from PCA
- Stored in vehicle's HSM (Hardware Security Module)
- Changed every 5 minutes or when entering/exiting privacy zone

**Privacy Zones:**

- Home address, workplace (don't broadcast BSM)
- Parking lots (change pseudonym when leaving)

Python Code: Pseudonym Management
----------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """
    V2X Pseudonym Certificate Manager
    """
    
    import time
    import random
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from datetime import datetime, timedelta
    
    class PseudonymManager:
        def __init__(self, enrollment_cert, enrollment_key):
            self.enrollment_cert = enrollment_cert
            self.enrollment_key = enrollment_key
            self.pseudonym_pool = []
            self.current_pseudonym = None
            self.last_rotation = None
            self.rotation_interval = 300  # 5 minutes (in seconds)
        
        def request_pseudonym_batch(self, pca_url, batch_size=1000):
            """Request batch of pseudonym certificates from PCA"""
            print(f"Requesting {batch_size} pseudonym certificates from PCA...")
            
            # In reality, this would be a secure protocol (TLS with mutual auth)
            # For demo, we generate pseudonyms locally
            
            for i in range(batch_size):
                # Generate ephemeral key pair for pseudonym
                private_key = ec.generate_private_key(ec.SECP256R1())
                public_key = private_key.public_key()
                
                # Create pseudonym certificate (signed by PCA)
                subject = x509.Name([
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "V2X-SCMS"),
                    x509.NameAttribute(NameOID.COMMON_NAME, f"Pseudonym-{random.randint(0, 0xFFFFFFFF):08X}")
                ])
                
                cert = x509.CertificateBuilder().subject_name(
                    subject
                ).issuer_name(
                    self.enrollment_cert.subject
                ).public_key(
                    public_key
                ).serial_number(
                    random.randint(1, 0xFFFFFFFFFFFFFFFF)
                ).not_valid_before(
                    datetime.utcnow()
                ).not_valid_after(
                    datetime.utcnow() + timedelta(days=7)  # Valid 1 week
                ).sign(self.enrollment_key, hashes.SHA256())
                
                self.pseudonym_pool.append({
                    'certificate': cert,
                    'private_key': private_key,
                    'used': False
                })
            
            print(f"Received {len(self.pseudonym_pool)} pseudonym certificates")
        
        def rotate_pseudonym(self):
            """Rotate to next unused pseudonym certificate"""
            if not self.pseudonym_pool:
                print("ERROR: No pseudonym certificates available!")
                return False
            
            # Find unused pseudonym
            unused = [p for p in self.pseudonym_pool if not p['used']]
            if not unused:
                print("WARNING: All pseudonyms used. Requesting new batch...")
                self.request_pseudonym_batch("https://pca.example.com")
                unused = [p for p in self.pseudonym_pool if not p['used']]
            
            # Select random unused pseudonym
            self.current_pseudonym = random.choice(unused)
            self.current_pseudonym['used'] = True
            self.last_rotation = time.time()
            
            cert_id = self.current_pseudonym['certificate'].serial_number
            print(f"Rotated to pseudonym certificate: {cert_id:016X}")
            return True
        
        def should_rotate(self):
            """Check if pseudonym should be rotated"""
            if self.current_pseudonym is None:
                return True
            
            if self.last_rotation is None:
                return True
            
            elapsed = time.time() - self.last_rotation
            return elapsed >= self.rotation_interval
        
        def get_current_certificate(self):
            """Get current pseudonym certificate for signing"""
            if self.should_rotate():
                self.rotate_pseudonym()
            
            return self.current_pseudonym['certificate'], self.current_pseudonym['private_key']
    
    # Example usage
    if __name__ == "__main__":
        # Generate enrollment certificate (normally issued by ECA)
        enrollment_key = ec.generate_private_key(ec.SECP256R1())
        enrollment_cert = x509.CertificateBuilder().subject_name(
            x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Vehicle-123")])
        ).issuer_name(
            x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "ECA")])
        ).public_key(
            enrollment_key.public_key()
        ).serial_number(
            0x123456
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=1095)  # 3 years
        ).sign(enrollment_key, hashes.SHA256())
        
        # Initialize pseudonym manager
        manager = PseudonymManager(enrollment_cert, enrollment_key)
        manager.request_pseudonym_batch("https://pca.example.com", batch_size=10)
        
        # Simulate driving with pseudonym rotation
        for i in range(20):
            cert, key = manager.get_current_certificate()
            print(f"[{i}] Using certificate: {cert.serial_number:016X}")
            time.sleep(1)  # Simulate 1 second (in reality, 5 minutes)

Certificate Revocation
-----------------------

**Problem:**

If vehicle is compromised or misbehaves, its certificates must be revoked.

**Challenge:**

Vehicle has ~1000 pseudonym certificates. Revoke all of them without revealing
vehicle identity (privacy).

**Solution: Certificate Revocation List (CRL)**

.. code-block:: text

    CRL Structure:
    ┌─────────────────────────────────────┐
    │ Revoked Certificate Serial Numbers  │
    │  - 0x1234567890ABCDEF               │
    │  - 0xFEDCBA0987654321               │
    │  - ...                              │
    │  (Thousands of revoked certs)       │
    └─────────────────────────────────────┘

**CRL Distribution:**

- CRLs broadcast via V2I (Roadside Units)
- CRLs embedded in V2X messages (piggyback on BSMs)
- Vehicles download CRLs periodically

**CRL Size Problem:**

- If 1 million vehicles, each with 1000 pseudonyms = 1 billion certificates
- CRL could be gigabytes (impractical)

**Solution: Compressed CRLs**

- Bloom filters (probabilistic data structure)
- Delta CRLs (only changes since last update)

V2X Attack Scenarios and Defenses
==================================

Attack 1: Fake Emergency Brake Warning
---------------------------------------

**Attack:**

Attacker broadcasts fake BSM with emergency brake status:

.. code-block:: python

    fake_bsm = {
        'position': (attacker_lat, attacker_lon),
        'speed': 100,  # 100 m/s (360 km/h) - unrealistic
        'brake_status': 0xFF  # Emergency brake activated
    }

**Impact:**

- Following vehicles receive warning
- Drivers brake unnecessarily
- Potential chain-reaction crash

**Defense:**

**1. Plausibility Checks:**

.. code-block:: python

    def validate_bsm_plausibility(bsm, sender_history):
        """Validate BSM for physical plausibility"""
        
        # Check 1: Speed limit
        if bsm['speed'] > 200:  # 200 m/s = 720 km/h
            return False, "Speed too high (physically impossible)"
        
        # Check 2: Acceleration limit
        if sender_history:
            prev_speed = sender_history[-1]['speed']
            time_delta = bsm['timestamp'] - sender_history[-1]['timestamp']
            accel = (bsm['speed'] - prev_speed) / time_delta
            
            if abs(accel) > 15:  # 15 m/s² (> 1.5G)
                return False, "Acceleration unrealistic"
        
        # Check 3: Position consistency
        if sender_history:
            prev_pos = sender_history[-1]['position']
            distance = calculate_distance(prev_pos, bsm['position'])
            time_delta = bsm['timestamp'] - sender_history[-1]['timestamp']
            implied_speed = distance / time_delta
            
            if abs(implied_speed - bsm['speed']) > 50:
                return False, "Position inconsistent with speed"
        
        return True, "Plausible"

**2. Misbehavior Detection:**

- Track sender's behavior over time
- Flag sender if multiple implausible messages
- Report to SCMS for certificate revocation

Attack 2: Sybil Attack (One Vehicle, Multiple Identities)
----------------------------------------------------------

**Attack:**

Attacker broadcasts multiple BSMs with different pseudonym certificates,
making it appear as if there are multiple vehicles.

**Goal:**

- Create fake traffic congestion
- Manipulate traffic light timing
- Denial of service (exhaust certificate validation resources)

**Defense:**

**1. Position Correlation:**

.. code-block:: python

    def detect_sybil(bsm_list):
        """Detect multiple BSMs from same physical location"""
        
        clusters = {}
        for bsm in bsm_list:
            pos = (bsm['latitude'], bsm['longitude'])
            
            # Group BSMs within 5 meters
            found_cluster = False
            for cluster_center, cluster_bsms in clusters.items():
                if calculate_distance(cluster_center, pos) < 5:
                    cluster_bsms.append(bsm)
                    found_cluster = True
                    break
            
            if not found_cluster:
                clusters[pos] = [bsm]
        
        # Alert if multiple BSMs from same location
        for cluster_center, cluster_bsms in clusters.items():
            if len(cluster_bsms) > 1:
                print(f"ALERT: {len(cluster_bsms)} BSMs from same location!")
                print(f"Potential Sybil attack at {cluster_center}")
                return True
        
        return False

**2. Certificate Linking (SCMS):**

- SCMS knows which pseudonyms belong to same vehicle
- If misbehavior detected, revoke all vehicle's pseudonyms
- Maintain privacy: Don't reveal linkage to public

Attack 3: Replay Attack
-----------------------

**Attack:**

Attacker captures legitimate BSM and replays it later.

**Example:**

- Capture BSM from vehicle on highway (speed = 120 km/h)
- Replay BSM in city (makes it appear vehicle is speeding)

**Defense:**

**Timestamp Validation:**

.. code-block:: c

    #define MAX_MESSAGE_AGE_MS 300  // 300 ms
    
    int validate_timestamp(uint64_t msg_timestamp) {
        uint64_t current_time = get_current_time_microseconds();
        uint64_t age_ms = (current_time - msg_timestamp) / 1000;
        
        if (age_ms > MAX_MESSAGE_AGE_MS) {
            printf("Message too old: %llu ms (threshold: %d ms)\n", 
                   age_ms, MAX_MESSAGE_AGE_MS);
            return 0;  // Reject
        }
        
        // Also check for future timestamps (clock skew attack)
        if (msg_timestamp > current_time + 100000) {  // +100 ms tolerance
            printf("Message from future! Clock skew attack?\n");
            return 0;
        }
        
        return 1;  // Accept
    }

C-V2X Security Considerations
==============================

C-V2X vs. DSRC Security
------------------------

**Similarities:**

- Both use ECDSA P-256 signatures
- Both use certificate-based authentication
- Both require SCMS infrastructure

**Differences:**

+----------------------+-------------------------+-------------------------+
| Aspect               | DSRC (IEEE 1609.2)      | C-V2X (3GPP)            |
+======================+=========================+=========================+
| Key Exchange         | ECIES (PKI-based)       | 5G-AKA (SIM-based)      |
+----------------------+-------------------------+-------------------------+
| Network Auth         | Not applicable          | SIM card (USIM)         |
+----------------------+-------------------------+-------------------------+
| Privacy              | Pseudonym certs         | SUPI concealment (5G)   |
+----------------------+-------------------------+-------------------------+
| V2N Security         | TLS over cellular       | NAS/AS security (3GPP)  |
+----------------------+-------------------------+-------------------------+

**C-V2X Additional Security (5G NR-V2X):**

- **Network slicing**: Dedicated slice for V2X (QoS and isolation)
- **Edge computing (MEC)**: Low-latency processing at cell edge
- **SUPI concealment**: Subscriber identity protection (5G privacy)

5G Security for V2N (Vehicle-to-Network)
-----------------------------------------

**5G Security Architecture:**

.. code-block:: text

    Vehicle ←→ gNodeB (5G Base Station) ←→ 5G Core Network
       │              │                         │
       │  ┌───────────┴─────────────────────────┴────┐
       │  │ NAS (Non-Access Stratum) Security        │
       │  │  - Authentication (5G-AKA)               │
       │  │  - Encryption (AES-128, SNOW 3G)         │
       │  │  - Integrity (HMAC-SHA256)               │
       │  └──────────────────────────────────────────┘
       │  ┌──────────────────────────────────────────┐
       │  │ AS (Access Stratum) Security             │
       │  │  - User plane encryption                 │
       │  │  - Control plane integrity               │
       │  └──────────────────────────────────────────┘

**Threat: IMSI Catching (Rogue Base Station)**

- Attacker sets up fake gNodeB
- Vehicle connects to fake base station
- Attacker captures IMSI (subscriber identity)

**Mitigation:**

- **SUPI concealment** (5G): Vehicle identity encrypted with home network key
- Attacker cannot extract IMSI even with rogue base station

Exam Questions
==============

Question 1: V2X Message Rate (Difficulty: Medium)
--------------------------------------------------

A vehicle broadcasts BSMs at 10 Hz (10 messages per second). Each BSM is 
300 bytes (including IEEE 1609.2 security overhead).

**a)** Calculate the bandwidth required for one vehicle.

**b)** If 100 vehicles are in range, calculate total V2X channel usage.

**c)** DSRC channel capacity is 6 Mbps. What is the maximum number of vehicles
that can coexist?

**Answer:**

**a) Bandwidth per Vehicle:**

- Message size: 300 bytes = 2400 bits
- Frequency: 10 Hz
- Bandwidth: 2400 bits × 10 = **24,000 bits/s = 24 kbps**

**b) Total Channel Usage (100 vehicles):**

- Total: 24 kbps × 100 = **2,400 kbps = 2.4 Mbps**

**c) Maximum Vehicles:**

- Channel capacity: 6 Mbps = 6,000 kbps
- Per vehicle: 24 kbps
- Maximum vehicles: 6,000 / 24 = **250 vehicles**

**However:**

This is **theoretical maximum**. In practice:

- Channel efficiency: ~70% (due to collisions, overhead)
- Effective capacity: 6 Mbps × 0.7 = 4.2 Mbps
- **Practical maximum: ~175 vehicles**

**Congestion Control:**

- SAE J2945/1 defines **Decentralized Congestion Control (DCC)**
- If channel usage > 70%, reduce message rate (e.g., 10 Hz → 5 Hz)

Question 2: Certificate Verification Latency (Difficulty: Hard)
----------------------------------------------------------------

A vehicle receives a BSM every 100 ms (10 Hz). Each BSM requires:

- **Signature verification**: 2 ms (ECDSA P-256)
- **Certificate chain validation**: 5 ms (verify cert against CA)
- **CRL check**: 10 ms (check if cert revoked)

Total: 17 ms per message.

If vehicle receives BSMs from 50 nearby vehicles, total verification time is
50 × 17 ms = 850 ms.

**Problem:** 850 ms > 100 ms (messages arrive faster than they can be verified)

**a)** Propose two optimizations to reduce verification time.

**b)** Design a priority queue for BSM processing.

**Answer:**

**a) Optimizations:**

**Optimization 1: Certificate Caching**

- Cache validated certificates for 5 minutes (pseudonym lifetime)
- On subsequent BSM from same sender:
  
  - Skip certificate chain validation (already done)
  - Only verify signature (2 ms)
  - Check if cached cert expired

**Effect:** 17 ms → 2 ms (8.5x speedup)

**Optimization 2: Batch CRL Checking**

- Instead of checking CRL for every certificate:
  
  - Load CRL into memory (hash table or Bloom filter)
  - Check revocation in O(1) time (~0.01 ms)

**Effect:** 10 ms → 0.01 ms

**Optimization 3: Hardware Acceleration**

- Use dedicated crypto co-processor (HSM) for ECDSA verification
- Parallel verification of multiple signatures

**Effect:** 2 ms → 0.5 ms (4x speedup)

**Combined:**

- Original: 17 ms
- After optimizations: 0.5 ms (signature) + 0.01 ms (CRL) = **0.51 ms**
- 50 vehicles: 50 × 0.51 ms = **25.5 ms** (fits within 100 ms budget) ✅

**b) Priority Queue:**

.. code-block:: python

    import heapq
    from dataclasses import dataclass
    
    @dataclass
    class BSMTask:
        priority: int       # Lower number = higher priority
        distance: float     # Distance to sender (meters)
        bsm: dict          # BSM message
        timestamp: float   # Reception time
        
        def __lt__(self, other):
            return self.priority < other.priority
    
    class BSMVerificationQueue:
        def __init__(self):
            self.queue = []
        
        def add_bsm(self, bsm, sender_distance):
            """Add BSM to priority queue"""
            
            # Determine priority based on:
            # 1. Distance (closer vehicles = higher priority)
            # 2. Message type (emergency > normal)
            # 3. Sender trust score
            
            if bsm.get('emergency_brake'):
                priority = 0  # Highest priority
            elif sender_distance < 50:  # Within 50 meters
                priority = 1
            elif sender_distance < 150:
                priority = 2
            else:
                priority = 3
            
            task = BSMTask(
                priority=priority,
                distance=sender_distance,
                bsm=bsm,
                timestamp=time.time()
            )
            
            heapq.heappush(self.queue, task)
        
        def process_next(self):
            """Process highest-priority BSM"""
            if self.queue:
                task = heapq.heappop(self.queue)
                
                # Check if BSM is still fresh (< 300 ms old)
                age_ms = (time.time() - task.timestamp) * 1000
                if age_ms > 300:
                    print(f"BSM expired ({age_ms:.1f} ms old), skipping")
                    return None
                
                # Verify signature
                if verify_bsm(task.bsm):
                    return task.bsm
                else:
                    print("Signature verification failed!")
                    return None
            
            return None

Question 3: Privacy Attack (Difficulty: Hard)
----------------------------------------------

An attacker installs multiple roadside observers that record all V2X BSMs.
Even though vehicles use pseudonym rotation, the attacker can still track
vehicles by correlating:

- Vehicle size (length, width) - remains constant
- Path history (trajectory pattern)
- Timing of pseudonym changes

**a)** Explain how this tracking attack works.

**b)** Propose three countermeasures (without breaking V2X functionality).

**Answer:**

**a) Tracking Attack:**

**Step 1: Vehicle Fingerprinting**

Observer records BSM features that remain constant across pseudonym changes:

.. code-block:: python

    vehicle_fingerprint = {
        'length': 4800,  # mm (constant)
        'width': 1900,   # mm (constant)
        'type': 'sedan', # vehicle type
        'path_pattern': [...]  # Driving behavior signature
    }

**Step 2: Pseudonym Linkage**

When vehicle changes pseudonym (every 5 minutes):

.. code-block:: text

    Time 0:00 - Pseudonym A:
      Position: (lat1, lon1), Size: 4800×1900 mm
    
    Time 5:00 - Pseudonym B:
      Position: (lat2, lon2), Size: 4800×1900 mm  ← Same size!
      
    Distance(lat1→lat2) / 5min = Average speed
    → Likely same vehicle

**Step 3: Long-Term Tracking**

- Link all pseudonyms with same vehicle fingerprint
- Reconstruct full trajectory (home → work → home)
- De-anonymize vehicle owner

**b) Countermeasures:**

**Countermeasure 1: Pseudonym Change at Unpredictable Locations**

- Don't change pseudonym at fixed time intervals (5 min)
- Change at random locations (e.g., when mixing with other vehicles)
- Change when entering tunnels (no observers)

.. code-block:: python

    def should_change_pseudonym(vehicle_context):
        # Random interval (3-7 minutes)
        if time_since_last_change > random.uniform(180, 420):
            return True
        
        # Change when in dense traffic (hard to correlate)
        if nearby_vehicle_count > 20:
            return True
        
        # Change in privacy zones (tunnels, parking garages)
        if in_privacy_zone(vehicle_context['position']):
            return True
        
        return False

**Countermeasure 2: Suppress Constant Identifiers**

- **Remove vehicle size** from BSM when not safety-critical
- **Quantize vehicle size** (e.g., small/medium/large instead of exact mm)
- **Add noise** to non-safety-critical fields

.. code-block:: python

    def anonymize_bsm(bsm):
        # Quantize vehicle length (instead of exact 4800 mm)
        if bsm['length'] < 4000:
            bsm['length'] = 3500  # "Small"
        elif bsm['length'] < 5000:
            bsm['length'] = 4500  # "Medium"
        else:
            bsm['length'] = 5500  # "Large"
        
        # Similar for width
        bsm['width'] = quantize(bsm['width'], bins=[1500, 1800, 2100])
        
        return bsm

**Countermeasure 3: Silent Period After Pseudonym Change**

- After changing pseudonym, **stop broadcasting BSMs for 10-30 seconds**
- Prevents attacker from correlating "last message from old pseudonym" with
  "first message from new pseudonym"

**Trade-off:**

- Reduces V2X safety (no BSMs for 30 seconds)
- Acceptable in low-risk scenarios (highway cruise, low traffic)
- Not acceptable in high-risk scenarios (intersection, dense traffic)

**Countermeasure 4: Group Pseudonym Change (Cooperative)**

- Multiple nearby vehicles coordinate to change pseudonyms simultaneously
- Attacker cannot determine which new pseudonym corresponds to which old one

.. code-block:: text

    Before change:
      Vehicle A (Pseudonym 1), Vehicle B (Pseudonym 2), Vehicle C (Pseudonym 3)
    
    After simultaneous change:
      Vehicle ? (Pseudonym 4), Vehicle ? (Pseudonym 5), Vehicle ? (Pseudonym 6)
      
    Attacker cannot link old → new pseudonyms (ambiguity)

Question 4: DSRC vs. C-V2X (Difficulty: Medium)
------------------------------------------------

Compare DSRC and C-V2X for a platooning application (trucks driving in formation
at 80 km/h with 10-meter gap).

**Requirements:**

- Latency: <50 ms (reaction time for emergency brake)
- Range: 100 meters (truck-to-truck)
- Reliability: 99.9% (safety-critical)

**a)** Which technology is more suitable? Justify.

**b)** What happens if cellular network is unavailable (no coverage)?

**Answer:**

**a) Technology Comparison:**

+------------------+---------------------+---------------------+
| Metric           | DSRC (802.11p)      | C-V2X (LTE/5G)      |
+==================+=====================+=====================+
| Latency          | 20-50 ms ✅         | <20 ms (5G) ✅      |
|                  |                     | <50 ms (LTE) ✅     |
+------------------+---------------------+---------------------+
| Range            | 300-1000 m ✅       | 1-2 km ✅           |
+------------------+---------------------+---------------------+
| Reliability      | 95-98% ⚠️           | 99%+ ✅             |
+------------------+---------------------+---------------------+
| Infrastructure   | Not required ✅     | Optional            |
| Dependency       |                     | (Direct mode) ✅    |
+------------------+---------------------+---------------------+
| Deployment       | Mature (2010s) ✅   | Emerging (2020s) ⚠️ |
+------------------+---------------------+---------------------+

**Recommendation: C-V2X (with Direct Mode)**

**Justification:**

1. **Lower latency**: 5G NR-V2X provides <20 ms latency (better than requirement)
2. **Higher reliability**: C-V2X uses HARQ (Hybrid ARQ) and better channel coding
3. **Direct Mode (PC5)**: Does not require cellular network infrastructure
4. **Future-proof**: Integration with 5G ecosystem (edge computing, network slicing)

**However:**

- **DSRC is acceptable** if already deployed (meets latency requirement)
- **Hybrid approach**: Use both DSRC and C-V2X for redundancy (99.99% reliability)

**b) Cellular Network Unavailability:**

**C-V2X has two modes:**

1. **Direct Mode (PC5 interface)**: V2V communication **without cellular network**
   
   - Uses dedicated 5.9 GHz spectrum (same as DSRC)
   - Direct truck-to-truck communication
   - **Works even without cellular coverage** ✅

2. **Network Mode (Uu interface)**: V2V communication **via cellular tower**
   
   - Requires cellular network
   - Used for V2N (vehicle-to-cloud) services
   - **Fails if no cellular coverage** ❌

**For platooning:**

- Use **Direct Mode (PC5)** for safety-critical truck-to-truck communication
- Use **Network Mode (Uu)** for non-critical services (route optimization, traffic info)

**Fallback Strategy:**

.. code-block:: text

    If cellular network unavailable:
    1. Continue platooning using C-V2X Direct Mode (PC5) ← Safety maintained
    2. Disable V2N features (cloud connectivity)
    3. Alert driver: "Cellular network unavailable"

**Conclusion:** C-V2X is more suitable and does not depend on cellular network
for safety-critical platooning.

Question 5: SCMS Scalability (Difficulty: Hard)
------------------------------------------------

A country plans to deploy V2X nationwide with 50 million vehicles. Each vehicle
needs 1,000 pseudonym certificates per week.

**a)** Calculate the weekly certificate issuance rate for the SCMS.

**b)** If each certificate issuance requires 10 ms (ECDSA signing), how many
PCA servers are needed?

**c)** Estimate CRL size if 0.1% of certificates are revoked weekly.

**Answer:**

**a) Certificate Issuance Rate:**

- Vehicles: 50 million
- Certificates per vehicle per week: 1,000
- **Total certificates per week**: 50M × 1,000 = **50 billion certificates**

**Per second:**

- 50 billion / (7 days × 86400 sec/day) = **82,672 certificates/second**

**b) Required PCA Servers:**

- Certificate issuance time: 10 ms = 0.01 seconds
- Certificates per server: 1 / 0.01 = **100 certificates/second**
- Required servers: 82,672 / 100 = **827 servers**

**With redundancy (2x for high availability):**

- **1,654 PCA servers**

**Cost Estimate:**

- Server cost: $10,000 per server
- Total: 1,654 × $10,000 = **$16.54 million** (one-time)
- Operational cost: $1,000/server/month = $1.65M/month = **$19.8M/year**

**c) CRL Size:**

**Revoked certificates per week:**

- Total certificates: 50 billion
- Revocation rate: 0.1% = 0.001
- Revoked: 50B × 0.001 = **50 million certificates**

**CRL Size (uncompressed):**

- Certificate serial number: 16 bytes (128-bit)
- CRL size: 50M × 16 bytes = **800 MB per week**

**Problem:** 800 MB CRL is too large for V2X broadcast.

**Solutions:**

**1. Compressed CRL (Bloom Filter):**

- Bloom filter size: ~10 bits per element (for 0.1% false positive rate)
- Size: 50M × 10 bits = 500 Mbits = **62.5 MB** (12.8x smaller)

**2. Delta CRL:**

- Only distribute changes since last CRL
- If 1M new revocations per day: 1M × 16 = **16 MB/day**

**3. Regional CRLs:**

- Distribute only revocations relevant to geographic region
- Each region: 800 MB / 50 regions = **16 MB per region**

**4. CRL Distribution via RSU:**

- Vehicles download CRL when passing Roadside Units
- Background download (not time-critical)

Conclusion
==========

V2X communication enables cooperative safety applications, but introduces
significant cybersecurity and privacy challenges. Key protections include:

1. **IEEE 1609.2**: Certificate-based message authentication (ECDSA P-256)
2. **SCMS**: PKI infrastructure for certificate management and revocation
3. **Pseudonym Rotation**: Privacy protection through short-lived certificates
4. **Misbehavior Detection**: Plausibility checks and trust management
5. **Secure Credential Management**: Hardware Security Module (HSM) for key storage

**Standards Compliance:**

- IEEE 1609.2/3/4: WAVE security and networking
- SAE J2945: V2X application standards
- ETSI TS 102 940: European V2X security
- ISO 21434: Automotive cybersecurity engineering
- UN R155: Cybersecurity management system (CSMS)

References
==========

- IEEE 1609.2-2016: Security Services for Applications and Management Messages
- SAE J2735: Dedicated Short Range Communications (DSRC) Message Set Dictionary
- SAE J2945/1: On-Board System Requirements for V2V Safety Communications
- ETSI TS 102 940: Intelligent Transport Systems (ITS); Security
- 3GPP TS 23.285: Architecture enhancements for V2X services
- ISO 21434: Road vehicles - Cybersecurity engineering

**END OF DOCUMENT**
