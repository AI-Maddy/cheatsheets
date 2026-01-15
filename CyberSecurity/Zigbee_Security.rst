====================================================================
Zigbee Security - Wireless Mesh Networking
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: Zigbee 3.0, IEEE 802.15.4

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Zigbee:**

- **Purpose:** Low-power mesh networking (smart home, industrial)
- **Frequency:** 2.4 GHz (802.15.4)
- **Range:** 10-100 meters, multi-hop mesh

**Security:**

✅ **AES-128-CCM encryption**
✅ **Trust Center:** Centralized key distribution
✅ **Install codes:** Secure commissioning (Zigbee 3.0)

Introduction
============

**Zigbee** powers Philips Hue, smart locks, thermostats, and industrial sensors.

**Attack Surface:**

- Pairing (commissioning)
- Key transport
- Mesh routing

Zigbee Security Architecture
==============================

**Trust Center (Coordinator):**

.. code-block:: c

    // Zigbee Trust Center distributes network key
    typedef struct {
        uint8_t network_key[16];     // Shared by all devices
        uint8_t link_keys[MAX_DEVICES][16];  // Per-device keys
    } zigbee_trust_center_t;
    
    void zigbee_join_device(uint64_t device_ieee_addr) {
        // Generate unique link key for device
        uint8_t link_key[16];
        generate_random(link_key, 16);
        
        // Send network key encrypted with link key
        zigbee_transport_key(device_ieee_addr, network_key, link_key);
        
        // Store link key
        trust_center.link_keys[device_ieee_addr] = link_key;
    }

**Install Code Commissioning (Zigbee 3.0):**

.. code-block:: c

    // Secure pairing with install code (QR code on device)
    void zigbee_join_with_install_code(uint64_t ieee_addr, uint8_t *install_code) {
        // Derive link key from install code
        uint8_t link_key[16];
        aes_mmo_hash(install_code, 18, link_key);  // 16-byte code + 2-byte CRC
        
        // Use link key to encrypt network key transport
        zigbee_transport_key_encrypted(ieee_addr, network_key, link_key);
    }

**Attack: Key Sniffing (Legacy Pairing)**

.. code-block:: python

    # Attacker sniffs Zigbee network key during device join
    
    import scapy_zbee
    
    def sniff_zigbee_key():
        # Capture Zigbee packets
        packets = sniff_802_15_4(timeout=60)
        
        for pkt in packets:
            if pkt.has_layer('ZigbeeSecurityHeader'):
                if pkt.command == 'TRANSPORT_KEY':
                    # In legacy Zigbee: Network key sent encrypted with default link key
                    default_key = b'ZigBeeAlliance09'
                    network_key = aes_decrypt(pkt.payload, default_key)
                    print(f"[!] Network key extracted: {network_key.hex()}")

**Defense: Install Codes (Zigbee 3.0)**

.. code-block:: python

    # User scans QR code on device to get install code
    install_code = scan_qr_code()  # e.g., "83FED3407A939723A5C639B26916D505"
    
    # Coordinator derives unique link key
    link_key = aes_mmo_hash(install_code)
    
    # Network key transport encrypted with unique link key
    # Attacker cannot decrypt (doesn't know install code)

Exam Questions
==============

**Q1: Zigbee vs BLE for Smart Home (Medium)**

Compare Zigbee and BLE for smart home security.

**Answer:**

+-------------------+-------------------------+------------------------+
| Feature           | Zigbee                  | BLE                    |
+===================+=========================+========================+
| Range             | 100m (mesh)             | 50m (direct)           |
+-------------------+-------------------------+------------------------+
| Mesh networking   | ✅ Built-in             | ⚠️  BLE Mesh (complex) |
+-------------------+-------------------------+------------------------+
| Security          | AES-128-CCM + TC        | AES-128-CCM + pairing  |
+-------------------+-------------------------+------------------------+
| Power             | Low (coin cell → 2yr)   | Very low (coin → 5yr)  |
+-------------------+-------------------------+------------------------+

**Recommendation:** Zigbee for whole-home (lights, locks), BLE for wearables.

**Q2: Zigbee Network Key Compromise (Hard)**

Attacker extracts Zigbee network key from one smart bulb. What is the impact?

**Answer:**

**Impact:**
- Attacker can decrypt ALL Zigbee traffic in home
- Can join network as rogue device
- Can send commands (unlock doors, disable alarms)

**Mitigation:**
1. **Immediate:** Revoke compromised device, generate new network key
2. **Re-key procedure:** Trust Center sends new network key to all devices
3. **Long-term:** Use link keys for sensitive devices (locks)

Standards
=========

- **Zigbee 3.0:** Unified application layer + security
- **IEEE 802.15.4:** PHY/MAC layer

**END OF DOCUMENT**
