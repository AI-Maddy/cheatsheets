====================================================================
DNP3 Security - Distributed Network Protocol
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEEE 1815-2012, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**DNP3 Overview:**

- **Purpose:** SCADA protocol for electric utilities, water/wastewater
- **Port:** TCP 20000 (default)
- **Security:** DNP3 Secure Authentication (SAv5)
- **Vulnerabilities:** Replay attacks, unauthorized commands, eavesdropping

**DNP3 Secure Authentication (SAv5):**

✅ Challenge-response authentication
✅ HMAC-SHA256 message authentication
✅ Session key management
✅ Prevents replay attacks with sequence numbers

Introduction
============

**DNP3 (Distributed Network Protocol)** is used in electric utilities and SCADA systems for communication between master stations and remote terminal units (RTUs).

**Security Evolution:**

1. **DNP3 v1-v4:** No security (plaintext)
2. **DNP3 SAv5 (IEEE 1815-2012):** Adds authentication

DNP3 Secure Authentication (SAv5)
==================================

**Authentication Process:**

.. code-block:: text

    Master → RTU: Challenge Request
    RTU → Master: Challenge + HMAC
    Master → RTU: Challenge Response + HMAC
    ← Session Established →

**Python Implementation:**

.. code-block:: python

    import hmac
    import hashlib
    import os
    
    class DNP3SecureAuth:
        def __init__(self, update_key):
            self.update_key = update_key
            self.sequence_num = 0
        
        def generate_challenge(self):
            return os.urandom(16)
        
        def compute_hmac(self, data, key):
            return hmac.new(key, data, hashlib.sha256).digest()
        
        def authenticate(self, challenge, user_number):
            # Session key = HMAC(update_key, challenge + user_number)
            session_data = challenge + user_number.to_bytes(2, 'big')
            session_key = self.compute_hmac(session_data, self.update_key)
            
            # Response HMAC
            response = self.compute_hmac(challenge, session_key)
            return response, session_key
        
        def authenticate_message(self, message, session_key):
            self.sequence_num += 1
            auth_data = message + self.sequence_num.to_bytes(4, 'big')
            return self.compute_hmac(auth_data, session_key)

Attack Scenarios
=================

**Attack 1: Unauthorized Trip Command**

.. code-block:: python

    # Attacker sends breaker trip without authentication
    dnp3_frame = {
        'function': 0x05,  # Operate
        'object': 'CROB',  # Control Relay Output Block
        'point': 1,
        'control_code': 0x81  # Trip/Close
    }
    # Without SAv5: Command accepted
    # With SAv5: Command rejected (no valid HMAC)

**Attack 2: Replay Attack**

Without sequence numbers, attacker could replay legitimate commands.

**Mitigation:** SAv5 includes sequence numbers in HMAC calculation.

Exam Questions
==============

**Q1: Why is SAv5 critical for utilities? (Medium)**

**Answer:** Prevents unauthorized breaker trips, pump control, and data falsification that could cause:
- Power outages
- Water contamination
- Equipment damage
- Safety incidents

**Q2: Compare DNP3 SAv5 vs TLS (Hard)**

**Answer:**

+-------------------+-------------------------+------------------------+
| Feature           | DNP3 SAv5               | TLS                    |
+===================+=========================+========================+
| Authentication    | Challenge-response      | Certificate-based      |
+-------------------+-------------------------+------------------------+
| Encryption        | ❌ None                 | ✅ AES-GCM             |
+-------------------+-------------------------+------------------------+
| Deployment        | RTU firmware update     | Requires TLS stack     |
+-------------------+-------------------------+------------------------+

**Best Practice:** Use both (DNP3 SAv5 for application auth + TLS for transport encryption)

Standards
=========

- **IEEE 1815-2012:** DNP3 Secure Authentication
- **IEC 62443-3-3:** Network security requirements
- **NERC CIP-007:** Cyber security - Systems security management

**END OF DOCUMENT**
