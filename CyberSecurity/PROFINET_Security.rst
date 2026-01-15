====================================================================
PROFINET Security - Industrial Ethernet Protocol
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEC 61784-2, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**PROFINET Overview:**

- **Purpose:** Real-time industrial Ethernet (Siemens standard)
- **Applications:** Factory automation, process control
- **Variants:** PROFINET IO, PROFINET CBA
- **Security:** PROFINET Security (PROFIsafe for safety)

**Security Features:**

✅ **Authentication:** TLS 1.2+ for PROFINET over IP
✅ **Integrity:** Cyclic Redundancy Check (CRC)
✅ **Access control:** Role-based configuration
✅ **PROFIsafe:** Safety-critical communication (black channel)

Introduction
============

**PROFINET** is widely used in automotive, pharmaceutical, and discrete manufacturing.

**Attack Surface:**

- Engineering workstation (TIA Portal)
- PROFINET controllers (PLC)
- PROFINET devices (I/O modules, drives)
- Switch infrastructure

PROFINET Security Extensions
==============================

**TLS-based Protection:**

.. code-block:: c

    #include <profinet_api.h>
    #include <mbedtls/ssl.h>
    
    void profinet_secure_connect(const char *device_ip) {
        mbedtls_ssl_context ssl;
        mbedtls_ssl_config conf;
        
        // Configure TLS 1.2
        mbedtls_ssl_config_defaults(&conf, MBEDTLS_SSL_IS_CLIENT,
            MBEDTLS_SSL_TRANSPORT_STREAM, MBEDTLS_SSL_PRESET_DEFAULT);
        
        mbedtls_ssl_conf_min_version(&conf, MBEDTLS_SSL_MAJOR_VERSION_3,
            MBEDTLS_SSL_MINOR_VERSION_3);  // TLS 1.2
        
        // Load device certificates
        mbedtls_x509_crt_parse_file(&device_cert, "controller.crt");
        mbedtls_ssl_conf_own_cert(&conf, &device_cert, &device_key);
        
        // Connect to PROFINET device
        profinet_connect_secure(device_ip, &ssl);
    }

**Attack Scenario: Unauthorized Configuration**

.. code-block:: python

    # Attacker modifies PLC configuration via PROFINET
    from pycomm3 import LogixDriver
    
    # Connect to PROFINET controller (no auth in legacy)
    plc = LogixDriver('192.168.1.100')
    
    # Read/modify process parameters
    plc.write('conveyor_speed', 1000)  # Normal: 100, Attack: 10× overspeed

**Defense: Access Control Lists**

.. code-block:: text

    # PROFINET ACL configuration
    Device: PLC_Station_1
      - Allow: Engineering_Workstation (192.168.1.50)
      - Allow: HMI_Panel (192.168.1.51)
      - Deny: All other devices

PROFIsafe for Safety-Critical
===============================

**Black Channel Principle:**

.. code-block:: c

    // PROFIsafe adds safety layer (CRC-32, sequence numbers)
    typedef struct {
        uint8_t data[32];
        uint16_t sequence_num;
        uint32_t crc;
    } profisafe_frame_t;
    
    int verify_profisafe_frame(profisafe_frame_t *frame) {
        // Compute CRC
        uint32_t computed_crc = crc32(frame->data, 32);
        computed_crc = crc32_update(computed_crc, &frame->sequence_num, 2);
        
        if (computed_crc != frame->crc) {
            return -1;  // Integrity check failed
        }
        
        // Check sequence number (prevent replay)
        if (frame->sequence_num <= last_sequence_num) {
            return -1;  // Replay attack
        }
        
        last_sequence_num = frame->sequence_num;
        return 0;
    }

Exam Questions
==============

**Q1: PROFINET vs Modbus Security (Medium)**

Compare PROFINET and Modbus security features.

**Answer:**

- **PROFINET:** TLS support, CRC integrity, PROFIsafe for safety
- **Modbus:** No built-in security (use Modbus/TLS or VPN)
- **Recommendation:** PROFINET for new deployments, retrofit Modbus with security gateway

**Q2: PROFIsafe Black Channel (Hard)**

Explain how PROFIsafe provides safety over untrusted network.

**Answer:** PROFIsafe adds safety layer with CRC-32 and sequence numbers, treating underlying network as "black channel" (untrusted). Even if attacker modifies packets, safety receiver detects corruption via CRC mismatch.

Standards
=========

- **IEC 61784-2:** PROFINET specification
- **IEC 62443:** Industrial security

**END OF DOCUMENT**
