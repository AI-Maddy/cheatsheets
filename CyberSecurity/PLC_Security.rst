====================================================================
PLC Security - Programmable Logic Controller Hardening
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEC 62443-4-2, ISA-99

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**PLC Attack Surface:**

- **Programming interface:** Vulnerable to unauthorized logic changes
- **Network protocols:** Modbus, EtherNet/IP, PROFINET (often unsecured)
- **Firmware:** Can be backdoored or exploited
- **Physical access:** JTAG, serial console

**Security Controls:**

✅ **Access control:** Password-protect programming mode
✅ **Code signing:** Digitally sign PLC programs
✅ **Network segmentation:** Isolate PLC network
✅ **Runtime monitoring:** Detect unauthorized logic changes
✅ **Secure boot:** Verify firmware integrity

Introduction
============

**PLCs (Programmable Logic Controllers)** control industrial processes (manufacturing, utilities, chemical plants).

**Security Challenges:**

1. **Legacy systems:** 20+ year lifespan, no security updates
2. **Vendor lock-in:** Proprietary protocols, limited security features
3. **Safety vs. Security:** Safety systems may bypass security controls
4. **24/7 operation:** Cannot easily patch or reboot

PLC Attack Vectors
==================

**Vector 1: Unauthorized Program Upload**

.. code-block:: python

    # Attacker uploads malicious ladder logic via engineering workstation
    def upload_malicious_logic(plc_ip):
        # Connect to PLC (no authentication in legacy PLCs)
        conn = connect_plc(plc_ip)
        
        # Upload malicious program
        malicious_program = compile_ladder_logic("""
            // Disable safety interlocks
            if safety_sensor_triggered:
                ignore()  // DANGEROUS!
        """)
        
        conn.upload_program(malicious_program)

**Mitigation:**

.. code-block:: c

    // Implement program authentication
    int verify_program_signature(uint8_t *program, size_t len, uint8_t *sig) {
        uint8_t hash[32];
        SHA256(program, len, hash);
        
        // Verify ECDSA signature with OEM public key
        return ecdsa_verify(hash, sig, oem_public_key);
    }

**Vector 2: Man-in-the-Middle (MITM)**

Attacker intercepts HMI ↔ PLC communication and modifies commands.

**Mitigation:** Use TLS or VPN for PLC communication.

**Vector 3: Physical Access (JTAG)**

.. code-block:: bash

    # Attacker extracts firmware via JTAG
    openocd -f interface/jlink.cfg -f target/stm32f4x.cfg
    > dump_image firmware.bin 0x08000000 0x100000

**Mitigation:** Disable JTAG in production, use secure boot.

PLC Hardening Checklist
========================

**1. Access Control:**

- Change default passwords
- Enable role-based access (programmer, operator, viewer)
- Limit engineering workstation IPs (whitelist)

**2. Code Integrity:**

.. code-block:: c

    // Runtime integrity check
    void plc_integrity_monitor(void) {
        while(1) {
            uint32_t crc = compute_program_crc(plc_program, program_size);
            
            if (crc != expected_crc) {
                trigger_alarm("PLC program modified!");
                enter_safe_mode();
            }
            
            sleep(60);  // Check every minute
        }
    }

**3. Network Segmentation:**

.. code-block:: text

    Enterprise Network
         ↓ (Firewall)
    SCADA DMZ
         ↓ (Firewall, IDS)
    PLC Network (isolated VLAN)
         ├─ PLC 1
         ├─ PLC 2
         └─ PLC 3

**4. Logging and Monitoring:**

.. code-block:: python

    # Log all PLC events
    events_to_log = [
        'program_upload',
        'configuration_change',
        'mode_switch (RUN → PROG)',
        'communication_error',
        'unauthorized_login_attempt'
    ]
    
    def log_plc_event(event_type, details):
        syslog.send(f"PLC-{plc_id}: {event_type} - {details}")

Exam Questions
==============

**Q1: Stuxnet Analysis (Hard)**

Stuxnet targeted Siemens PLCs controlling uranium enrichment centrifuges. Describe the attack chain.

**Answer:**

1. **Initial infection:** USB drive infects Windows PC (4 zero-days)
2. **Lateral movement:** Worm spreads to engineering workstation
3. **PLC targeting:** Identifies Siemens S7-300/400 PLCs via WinCC software
4. **Logic injection:** Modifies PLC code to spin centrifuges at destructive speeds
5. **Concealment:** Replays normal sensor values to HMI (operators see normal operation)

**Impact:** Destroyed ~1000 centrifuges in Iran's nuclear program.

**Lessons:**

- Air-gapped networks can be breached (USB)
- PLCs need code signing
- Monitor PLC behavior, not just HMI data

**Q2: Safety vs. Security Trade-off (Medium)**

A safety PLC must activate emergency shutdown within 100ms. Adding cryptographic verification adds 50ms latency. How to balance?

**Answer:**

**Approach 1: Dual-Layer**
- Safety PLC operates without crypto (meets timing)
- Separate monitoring PLC verifies commands with crypto
- If mismatch detected → alert + investigate

**Approach 2: Hardware Acceleration**
- Use HSM for crypto (reduces latency to <5ms)
- Meets both safety timing and security requirements

**Approach 3: Risk-Based**
- Critical commands (emergency stop) bypass crypto
- Non-critical commands (setpoint changes) require authentication

Standards
=========

- **IEC 62443-4-2:** Security requirements for components
- **IEC 61131-3:** PLC programming languages
- **ISA-99:** Industrial automation security

**END OF DOCUMENT**
