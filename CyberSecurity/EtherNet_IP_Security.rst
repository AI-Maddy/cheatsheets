====================================================================
EtherNet/IP Security - Industrial Protocol (ODVA)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ODVA CIP Security, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**EtherNet/IP:**

- **Developer:** ODVA (Open DeviceNet Vendors Association)
- **Common in:** Rockwell Automation (Allen-Bradley PLCs)
- **Port:** TCP 44818, UDP 2222
- **Protocol:** CIP (Common Industrial Protocol) over Ethernet

**Security:**

✅ **CIP Security:** TLS 1.2, certificate-based authentication
✅ **DTLS:** For UDP traffic
✅ **Firewall integration:** Port-based filtering

Introduction
============

**EtherNet/IP** is used in automotive assembly, food & beverage, and packaging.

**Vulnerability:** Legacy devices lack authentication.

CIP Security Implementation
============================

.. code-block:: c

    #include <cip_security.h>
    
    void establish_secure_cip_session(const char *plc_ip) {
        // TLS 1.2 for TCP-based CIP
        cip_session_t session;
        cip_security_init(&session);
        
        // Load certificates
        cip_load_certificate(&session, "device.crt", "device.key");
        cip_set_ca_cert(&session, "ca.crt");
        
        // Connect with mutual TLS
        if (cip_connect_secure(&session, plc_ip, 44818) == 0) {
            printf("Secure CIP session established\n");
        }
    }

**Attack: Modify Tag Values**

.. code-block:: python

    # Attacker changes production counter
    from pycomm3 import LogixDriver
    
    plc = LogixDriver('192.168.1.10')
    plc.write('production_count', 0)  # Reset counter → reporting fraud

**Defense: Tag-Level Access Control**

.. code-block:: text

    Tag: production_count
      - Read: HMI, SCADA, MES
      - Write: PLC_Program only (no external write)

Exam Questions
==============

**Q1: CIP Security vs Legacy (Medium)**

What changes are needed to add CIP Security to legacy EtherNet/IP network?

**Answer:** 
1. Certificate infrastructure (CA)
2. Firmware updates for devices
3. Engineering software update (RSLogix/Studio 5000)
4. Network time synchronization (for certificate validation)

Standards
=========

- **ODVA CIP Security Specification**
- **IEC 62443**

**END OF DOCUMENT**
