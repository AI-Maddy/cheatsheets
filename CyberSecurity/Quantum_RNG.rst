====================================================================
Quantum Random Number Generators (QRNG)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NIST SP 800-90B

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**QRNG:**

- **Purpose:** Generate cryptographically secure random numbers
- **Quantum source:** Photon arrival time, vacuum fluctuations
- **Advantage:** Provably random (quantum mechanics)

**Applications:**

- Cryptographic key generation
- Nonce/IV generation
- Challenge-response authentication

QRNG vs PRNG
=============

.. code-block:: text

    PRNG (Pseudo-Random):
    - Deterministic algorithm
    - Seed required
    - Theoretically predictable
    
    QRNG (Quantum Random):
    - Non-deterministic (quantum noise)
    - No seed needed
    - Provably unpredictable

Embedded QRNG Integration
===========================

.. code-block:: c

    // Use QRNG for AES key generation
    #include <qrng.h>
    
    void generate_aes_key(uint8_t *key) {
        // Read from quantum RNG chip
        qrng_read(key, 32);  // 256-bit key
        
        // Verify entropy
        if (entropy_test(key, 32) < 7.9) {  // NIST requirement
            // Insufficient entropy, retry
            generate_aes_key(key);
        }
    }

**Commercial QRNG Chips:**

- ID Quantique Quantis QRNG
- QuintessenceLabs qStream

Exam Questions
==============

**Q1: QRNG Necessity (Medium)**

Is QRNG necessary for embedded devices, or is PRNG sufficient?

**Answer:**

**PRNG Sufficient for:**
- Most applications (AES key generation with good seed)
- Cost-sensitive devices

**QRNG Recommended for:**
- High-security applications (financial, military)
- Long-term key generation (30+ year secrets)
- Post-quantum crypto (conservative approach)

Standards
=========

- **NIST SP 800-90B:** Entropy source validation

**END OF DOCUMENT**
