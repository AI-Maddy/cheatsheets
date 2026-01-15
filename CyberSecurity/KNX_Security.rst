====================================================================
KNX Security - Building Automation Protocol
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO/IEC 14543-3, KNX Secure

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**KNX:**

- European building automation standard (lighting, HVAC, access control)
- **Variants:** KNX TP (twisted pair), KNX IP, KNX RF (wireless)
- **Security:** KNX Secure (introduced 2018)

**KNX Secure Features:**

✅ **Authentication:** AES-128-CCM with group keys
✅ **Encryption:** Per-device session keys
✅ **Data integrity:** Message authentication codes

Introduction
============

**Legacy KNX Vulnerability:** No encryption → eavesdropping, command injection.

**KNX Secure Solution:** Adds cryptographic layer without breaking compatibility.

KNX Secure Implementation
===========================

.. code-block:: python

    from knxip import KNXIPClient
    
    # Connect to KNX/IP gateway with security
    client = KNXIPClient(
        gateway_ip='192.168.1.100',
        secure=True,
        password='building_key_123'
    )
    
    # Send encrypted command (turn on lights)
    client.group_write('1/2/3', True)  # Group address, Value

**Attack: Command Injection (Legacy KNX)**

.. code-block:: python

    # Attacker sends malicious KNX telegram
    def inject_knx_command(knx_bus):
        # Craft telegram: Unlock all doors
        telegram = KNXTelegram(
            source='0.0.0',
            destination='5/1/1',  # Door lock group address
            command='UNLOCK'
        )
        
        knx_bus.transmit(telegram)  # No authentication in legacy

**Defense: KNX Secure**

.. code-block:: c

    // Encrypt KNX telegram with AES-128-CCM
    #include <mbedtls/ccm.h>
    
    void knx_secure_send(uint8_t *plaintext, size_t len) {
        uint8_t ciphertext[64];
        uint8_t tag[16];
        
        // Use group key or device key
        uint8_t key[16];
        get_knx_secure_key(key);
        
        // Encrypt with CCM
        mbedtls_ccm_context ccm;
        mbedtls_ccm_init(&ccm);
        mbedtls_ccm_setkey(&ccm, MBEDTLS_CIPHER_ID_AES, key, 128);
        mbedtls_ccm_encrypt_and_tag(&ccm, len, nonce, 13,
            NULL, 0, plaintext, ciphertext, tag, 16);
        
        // Transmit encrypted telegram
        knx_transmit(ciphertext, len, tag);
    }

Exam Questions
==============

**Q1: KNX Secure Migration (Medium)**

Building has 200 KNX devices (10 years old, no security). Design migration to KNX Secure.

**Answer:**

1. **Install KNX Secure gateway** (bridge legacy ↔ secure)
2. **Replace critical devices first** (door locks, alarms)
3. **Maintain legacy compatibility** for 5 years
4. **Full migration** over 10-year replacement cycle

Standards
=========

- **ISO/IEC 14543-3:** KNX standard
- **KNX Secure:** Cryptographic extension

**END OF DOCUMENT**
