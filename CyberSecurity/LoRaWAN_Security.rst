====================================================================
LoRaWAN Security - Long Range Wide Area Network
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: LoRaWAN 1.1 Specification

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**LoRaWAN:**

- **Purpose:** Low-power, long-range IoT (10+ km range)
- **Applications:** Smart cities, agriculture, asset tracking
- **Frequency:** ISM bands (868 MHz EU, 915 MHz US)

**Security (LoRaWAN 1.1):**

✅ **AES-128 encryption:** End-to-end payload protection
✅ **Mutual authentication:** Join-Server verifies device
✅ **Network/application separation:** Dual-key architecture

Introduction
============

**LoRaWAN** enables battery-powered sensors with 10-year lifespan.

**Security Architecture:**

.. code-block:: text

    End Device (sensor)
         ↓ LoRa radio
    Gateway (LoRa → IP)
         ↓ Internet
    Network Server (routing)
         ↓
    Application Server (your app)

LoRaWAN 1.1 Security
=====================

**Dual-Key System:**

.. code-block:: c

    // Network session key (for MAC commands)
    uint8_t NwkSKey[16];
    
    // Application session key (for payload encryption)
    uint8_t AppSKey[16];
    
    // Encrypt payload with AppSKey
    void encrypt_lora_payload(uint8_t *payload, size_t len) {
        aes128_encrypt(payload, len, AppSKey);
    }

**Join Procedure (OTAA - Over-The-Air Activation):**

.. code-block:: c

    #include <lorawan.h>
    
    void lorawan_join(void) {
        // Device unique keys
        uint8_t DevEUI[8];   // Device identifier
        uint8_t AppKey[16];  // Root key (pre-shared)
        
        // Send Join Request
        lora_join_request_t req;
        memcpy(req.DevEUI, DevEUI, 8);
        req.DevNonce = get_random_nonce();  // Prevent replay
        
        // Compute MIC (Message Integrity Code)
        req.MIC = aes128_cmac(AppKey, &req, sizeof(req) - 4);
        
        // Transmit join request
        lora_transmit(&req);
        
        // Receive Join Accept (encrypted with AppKey)
        lora_join_accept_t *accept = lora_receive();
        
        // Derive session keys
        derive_session_keys(AppKey, accept->AppNonce, req.DevNonce,
                           NwkSKey, AppSKey);
    }

**Attack: Replay Attack (LoRaWAN 1.0.x)**

.. code-block:: python

    # Attacker captures Join Request and replays
    captured_join_request = sniff_lora_packet()
    
    # Replay to network server
    transmit_lora(captured_join_request)
    # In LoRaWAN 1.0.x: Accepted (no DevNonce verification)
    # In LoRaWAN 1.1: Rejected (Join-Server tracks DevNonce)

**Defense (LoRaWAN 1.1):**

.. code-block:: python

    # Join-Server maintains DevNonce history
    class JoinServer:
        def __init__(self):
            self.used_nonces = {}  # DevEUI → set of used DevNonces
        
        def process_join_request(self, req):
            dev_eui = req.DevEUI
            dev_nonce = req.DevNonce
            
            # Check for replay
            if dev_eui in self.used_nonces:
                if dev_nonce in self.used_nonces[dev_eui]:
                    return reject("DevNonce already used")
            else:
                self.used_nonces[dev_eui] = set()
            
            # Store DevNonce
            self.used_nonces[dev_eui].add(dev_nonce)
            
            # Generate Join Accept
            return self.generate_join_accept(req)

Exam Questions
==============

**Q1: LoRaWAN 1.0 vs 1.1 Security (Medium)**

What are key security improvements in LoRaWAN 1.1?

**Answer:**

1. **Join-Server:** Centralized key management (prevents roaming attacks)
2. **DevNonce tracking:** Prevents Join Request replay
3. **Separate NwkSKey/AppSKey:** Network cannot decrypt application data
4. **Roaming security:** Secure handoff between networks

**Q2: LoRaWAN Key Extraction (Hard)**

If attacker extracts AppKey from LoRa device, what data is compromised?

**Answer:**

**Compromised:**
- Future Join Accepts (derive session keys)
- Past session keys IF attacker recorded Join procedures

**Not Compromised:**
- Past encrypted payloads (if AppSKey not derived)

**Mitigation:**
- Revoke device (blacklist DevEUI)
- Re-provision with new AppKey
- Use secure element (HSM) for key storage

Standards
=========

- **LoRaWAN 1.1 Specification:** Security architecture
- **LoRa Alliance Technical Recommendations**

**END OF DOCUMENT**
