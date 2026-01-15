====================================================================
5G and Edge Computing Security
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: 3GPP, ETSI MEC

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**5G Security Features:**

✅ **Enhanced encryption:** 256-bit encryption (vs 128-bit in 4G)
✅ **Network slicing:** Isolated virtual networks
✅ **SUPI encryption:** Hide subscriber identity
✅ **Home routing:** Roaming security

**Edge Computing Threats:**

- Distributed attack surface
- Data sovereignty (processing at edge)
- Physical tampering (edge nodes in field)

5G Security Architecture
=========================

.. code-block:: text

    UE (Device) ↔ gNB (5G Base Station) ↔ Core Network
                                            ↓
                                    Edge Computing (MEC)

**Network Slicing Security:**

.. code-block:: python

    # Isolate IoT devices on separate slice
    slice_iot = {
        'slice_id': '5G_IoT_Slice',
        'qos': 'low_latency',
        'encryption': 'AES-256-GCM',
        'allowed_services': ['MQTT', 'CoAP']
    }
    
    # Critical infrastructure on high-security slice
    slice_critical = {
        'slice_id': '5G_Critical_Slice',
        'qos': 'ultra_reliable',
        'encryption': 'AES-256-GCM + IPsec',
        'allowed_services': ['SCADA', 'IEC61850']
    }

Edge Computing Security
=========================

.. code-block:: c

    // Secure edge node with TPM attestation
    #include <tpm2.h>
    
    void edge_node_attestation(void) {
        // Generate attestation quote
        uint8_t pcr_values[32];
        TPM2_Quote(pcr_values, sizeof(pcr_values));
        
        // Send to cloud for verification
        send_attestation_to_cloud(pcr_values);
        
        // Cloud verifies PCR values match expected state
        // If valid → allow edge processing
        // If invalid → quarantine edge node
    }

Exam Questions
==============

**Q1: 5G vs 4G Security (Medium)**

What are key security improvements in 5G?

**Answer:**

1. **Encryption:** 256-bit (vs 128-bit)
2. **SUPI concealment:** IMSI no longer sent in clear
3. **Home routing:** Roaming traffic authenticated by home network
4. **Integrity protection:** User plane encryption (optional in 4G)

Standards
=========

- **3GPP TS 33.501:** 5G security architecture
- **ETSI MEC:** Multi-access Edge Computing

**END OF DOCUMENT**
