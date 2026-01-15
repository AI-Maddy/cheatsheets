====================================================================
Access Control System Security - Physical Security Integration
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: OSDP, Wiegand, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Access Control Systems:**

- Badge readers, biometric scanners, door locks
- **Protocols:** OSDP (Open Supervised Device Protocol), Wiegand
- **Components:** Controller, reader, electric strike/mag lock

**Security Threats:**

❌ **Badge cloning:** Copy RFID credentials
❌ **Wiegand sniffing:** Intercept reader→controller communication
❌ **Credential stuffing:** Replay captured badge data
❌ **Tailgating:** Physical security (not cyber)

Introduction
============

**Attack Impact:** Unauthorized building access, data center breach, theft.

OSDP vs Wiegand
================

.. code-block:: text

    Wiegand (Legacy):
    - Plaintext communication
    - No encryption
    - Susceptible to wire tapping
    
    OSDP Secure Channel:
    - AES-128 encryption
    - Mutual authentication
    - Tamper detection

**OSDP Secure Channel Implementation:**

.. code-block:: c

    #include <osdp.h>
    
    // Establish secure channel between controller and reader
    void osdp_secure_connect(osdp_t *ctx) {
        uint8_t scbk[16];  // Secure Channel Base Key
        
        // Load pre-shared key
        load_scbk(scbk);
        
        // Initialize secure channel
        osdp_sc_init(ctx, scbk);
        
        // All subsequent commands encrypted
        osdp_cmd_led(ctx, LED_GREEN, CMD_LED_ON);
    }

**Badge Cloning Defense:**

.. code-block:: python

    # Implement challenge-response (prevents cloning)
    class SecureBadgeReader:
        def __init__(self):
            self.server_key = load_key()
        
        def authenticate_badge(self, badge_id):
            # Send random challenge
            challenge = os.urandom(16)
            send_to_badge(challenge)
            
            # Badge computes: response = HMAC(badge_key, challenge)
            response = receive_from_badge()
            
            # Verify response
            expected = hmac.new(self.server_key, challenge, hashlib.sha256).digest()
            
            if response == expected:
                unlock_door()
            else:
                log_security_event("Invalid badge response")

Exam Questions
==============

**Q1: Wiegand to OSDP Migration (Medium)**

Migrate 500-door facility from Wiegand to OSDP. How to minimize disruption?

**Answer:**

**Phase 1:** Replace controllers with OSDP-capable models (support both)
**Phase 2:** Gradually replace readers (Wiegand → OSDP)
**Phase 3:** Disable Wiegand after 100% migration

Standards
=========

- **OSDP Specification:** Secure access control protocol
- **IEC 62443:** Security for building automation

**END OF DOCUMENT**
