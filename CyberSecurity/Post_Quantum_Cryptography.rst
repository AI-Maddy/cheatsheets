====================================================================
Post-Quantum Cryptography - Quantum-Resistant Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NIST FIPS 203/204/205, NSA CNSA 2.0

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Quantum Threat:**

- **Shor's Algorithm:** Breaks RSA, ECDSA, Diffie-Hellman
- **Grover's Algorithm:** Weakens AES (256-bit → 128-bit security)
- **Timeline:** Large-scale quantum computers (10,000+ qubits) by 2035

**NIST Post-Quantum Algorithms (2024):**

✅ **ML-KEM (Kyber):** Key encapsulation (FIPS 203)
✅ **ML-DSA (Dilithium):** Digital signatures (FIPS 204)
✅ **SLH-DSA (SPHINCS+):** Hash-based signatures (FIPS 205)

**Migration Strategy:**

1. **Inventory:** Identify all uses of RSA/ECDSA
2. **Hybrid:** Deploy PQC + classical (transition period)
3. **Pure PQC:** Full migration by 2030

Introduction
============

**Quantum computers** can break current public-key cryptography (RSA, ECC) using **Shor's algorithm**.

**Impact on Embedded Systems:**

- **Firmware signing:** ECDSA signatures breakable
- **TLS:** Key exchange (ECDHE) vulnerable
- **Secure boot:** RSA verification bypassed
- **Code signing:** Attacker can sign malicious firmware

**"Harvest Now, Decrypt Later":**

Attackers record encrypted traffic today, decrypt when quantum computers available.

NIST Post-Quantum Algorithms
==============================

**ML-KEM (Kyber) - Key Encapsulation**

Replaces RSA/ECDH for key exchange.

.. code-block:: c

    #include <kyber512.h>
    
    // Server generates key pair
    uint8_t public_key[KYBER_PUBLICKEYBYTES];
    uint8_t secret_key[KYBER_SECRETKEYBYTES];
    crypto_kem_keypair(public_key, secret_key);
    
    // Send public key to client
    send_to_client(public_key);
    
    // Client encapsulates shared secret
    uint8_t ciphertext[KYBER_CIPHERTEXTBYTES];
    uint8_t shared_secret_client[KYBER_BYTES];
    crypto_kem_enc(ciphertext, shared_secret_client, public_key);
    
    // Client sends ciphertext to server
    send_to_server(ciphertext);
    
    // Server decapsulates to get same shared secret
    uint8_t shared_secret_server[KYBER_BYTES];
    crypto_kem_dec(shared_secret_server, ciphertext, secret_key);
    
    // Both now have shared_secret for AES encryption

**Performance (ARM Cortex-M4 @ 168 MHz):**

- Keygen: 500 µs
- Encapsulation: 600 µs
- Decapsulation: 700 µs

**ML-DSA (Dilithium) - Digital Signatures**

Replaces RSA/ECDSA for signing.

.. code-block:: c

    #include <dilithium2.h>
    
    // Generate signing key
    uint8_t public_key[DILITHIUM_PUBLICKEYBYTES];
    uint8_t secret_key[DILITHIUM_SECRETKEYBYTES];
    crypto_sign_keypair(public_key, secret_key);
    
    // Sign firmware
    uint8_t firmware[1024];
    uint8_t signature[DILITHIUM_BYTES];
    size_t sig_len;
    
    crypto_sign_signature(signature, &sig_len, firmware, 1024, secret_key);
    
    // Verify signature
    int valid = crypto_sign_verify(signature, sig_len, firmware, 1024, public_key);
    if (valid == 0) {
        flash_firmware(firmware);
    }

**Signature Size:** 2420 bytes (vs. ECDSA 64 bytes) - **38× larger!**

Hybrid Cryptography (Transition Strategy)
===========================================

**Combine classical + PQC for security during migration.**

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric import ec, x25519
    import kyber  # Post-quantum library
    
    def hybrid_key_exchange():
        # Classical ECDH
        ecdh_private = ec.generate_private_key(ec.SECP256R1())
        ecdh_public = ecdh_private.public_key()
        
        # Post-quantum Kyber
        kyber_public, kyber_secret = kyber.keygen()
        
        # Exchange both public keys
        send_to_peer(ecdh_public, kyber_public)
        
        # Derive shared secrets
        peer_ecdh_public, peer_kyber_public = receive_from_peer()
        
        ecdh_shared = ecdh_private.exchange(ec.ECDH(), peer_ecdh_public)
        kyber_shared = kyber.decapsulate(peer_kyber_public, kyber_secret)
        
        # Combine with KDF
        hybrid_key = HKDF(ecdh_shared + kyber_shared)
        
        # Secure against both classical and quantum attacks
        return hybrid_key

Embedded PQC Implementation Challenges
========================================

**Challenge 1: Flash Storage**

- **RSA-2048 public key:** 256 bytes
- **Dilithium-2 public key:** 1312 bytes (**5× larger**)

**Solution: Compression**

.. code-block:: c

    // Store compressed public keys
    #include <lz4.h>
    
    uint8_t dilithium_pubkey[1312];
    uint8_t compressed[512];
    int compressed_size = LZ4_compress_default(dilithium_pubkey, compressed, 1312, 512);
    
    // Typical compression: 1312 → 600 bytes (2× reduction)

**Challenge 2: RAM**

Kyber requires temporary buffers during key generation.

**Optimization:**

.. code-block:: c

    // Use stack instead of heap
    __attribute__((aligned(4)))
    uint8_t kyber_buffer[16384];  // On stack (16 KB)
    
    crypto_kem_keypair_with_buffer(public_key, secret_key, kyber_buffer);

**Challenge 3: Real-Time Constraints**

Signature verification takes 2 ms (vs. ECDSA 0.5 ms).

**Solution: Hardware Acceleration**

.. code-block:: c

    // Use FPGA or crypto accelerator
    #define USE_NTT_ACCELERATOR  // Number Theoretic Transform
    
    // Reduces Dilithium verification from 2 ms → 0.3 ms

Automotive Use Case
====================

**V2X Communication with PQC:**

.. code-block:: c

    // Vehicle signs safety message with Dilithium
    typedef struct {
        uint32_t timestamp;
        float speed_mps;
        float heading_deg;
        uint8_t signature[DILITHIUM_BYTES];
    } v2x_message_t;
    
    void send_v2x_pqc(void) {
        v2x_message_t msg;
        msg.timestamp = get_timestamp();
        msg.speed_mps = get_vehicle_speed();
        msg.heading_deg = get_heading();
        
        // Sign with Dilithium
        crypto_sign_signature(msg.signature, NULL,
            (uint8_t*)&msg, sizeof(msg) - DILITHIUM_BYTES,
            vehicle_private_key);
        
        // Broadcast (signed message resistant to quantum attacks)
        dsrc_broadcast(&msg, sizeof(msg));
    }

**Performance:**

- Signing: 1.5 ms (within 10 ms V2X latency budget)
- Verification: 2.0 ms (receiving vehicle)
- Message size: 2500 bytes (vs. ECDSA 150 bytes)

Exam Questions
==============

**Q1: PQC Migration Timeline (Medium)**

Your company manufactures automotive ECUs with 15-year lifespan. Current firmware uses ECDSA. Design migration plan to PQC.

**Answer:**

**Phase 1 (2024-2026): Preparation**
- Inventory all uses of ECDSA (firmware updates, V2X, secure boot)
- Evaluate PQC libraries (liboqs, PQClean)
- Benchmark performance on target MCU

**Phase 2 (2026-2028): Hybrid Deployment**
- New ECUs: Dual-sign firmware (ECDSA + Dilithium)
- Bootloader verifies either signature (backward compatible)
- Increase flash by 4 KB for larger signatures

**Phase 3 (2028-2030): Pure PQC**
- New ECUs: Dilithium only
- Legacy ECUs: Still accept ECDSA (until retired)

**Phase 4 (2030-2035): Legacy Phase-Out**
- ECDSA support deprecated
- All firmware signed with Dilithium only

**Rollback Plan:** If quantum computers delayed, extend ECDSA support.

**Q2: Grover's Algorithm Impact (Hard)**

Grover's algorithm reduces AES-256 security to 128-bit. Should embedded systems migrate to AES-512?

**Answer:**

**No, AES-256 is sufficient.**

**Reasoning:**

1. **Grover's algorithm** requires $2^{128}$ operations to break AES-256
2. **Quantum computer requirements:**
   - 10^9 qubits
   - 10^12 gates
   - Not feasible for 50+ years
3. **AES-256 → AES-512 migration cost:**
   - Performance penalty (slower encryption)
   - No standard AES-512 (would require new NIST approval)
   - Minimal security benefit

**Recommended:**

- Keep AES-256 for symmetric encryption
- Focus on **public-key** migration (RSA/ECDSA → PQC)
- If paranoid: Use AES-256 in CBC or GCM mode with longer keys

**Alternative:** Prepare for **quantum-resistant symmetric algorithms** (if NIST standardizes).

Standards
=========

- **NIST FIPS 203:** ML-KEM (Kyber)
- **NIST FIPS 204:** ML-DSA (Dilithium)
- **NIST FIPS 205:** SLH-DSA (SPHINCS+)
- **NSA CNSA 2.0:** Post-quantum migration guidance

**END OF DOCUMENT**
