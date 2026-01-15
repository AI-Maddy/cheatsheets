====================================================================
Penetration Testing Embedded Systems
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: OWASP Embedded AppSec, PTES

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Embedded Pentesting:**

- Hardware analysis (UART, JTAG, chip-off)
- Firmware reverse engineering
- Network protocol testing
- Side-channel analysis (power, timing, EM)

**Tools:**

✅ **Hardware:** Logic analyzer, oscilloscope, JTAGulator
✅ **Software:** Ghidra, Binwalk, Burp Suite
✅ **Wireless:** HackRF, Ubertooth, WiFi Pineapple

Methodology
===========

**Phase 1: Reconnaissance**

.. code-block:: bash

    # Identify chip markings
    cat /proc/cpuinfo
    
    # Network scanning
    nmap -sV -p- 192.168.1.1
    
    # Firmware extraction
    binwalk -e firmware.bin

**Phase 2: Hardware Interface Discovery**

.. code-block:: python

    # JTAGulator: Find JTAG pinout
    import serial
    
    jtag = serial.Serial('/dev/ttyUSB0', 115200)
    jtag.write(b'i')  # Identify JTAG pins
    # Output: TDI=Pin3, TDO=Pin5, TCK=Pin7, TMS=Pin9

**Phase 3: Firmware Analysis**

.. code-block:: bash

    # Extract filesystem from firmware
    binwalk -e firmware.bin
    
    # Find hardcoded credentials
    strings _firmware.extracted/* | grep -i "password\|secret\|key"
    
    # Reverse engineer with Ghidra
    ghidra firmware.elf

**Phase 4: Exploit Development**

.. code-block:: c

    // Buffer overflow in web interface
    exploit_payload = "A" * 512 + shellcode

Standards
=========

- **OWASP Embedded Application Security**
- **PTES (Penetration Testing Execution Standard)**

**END OF DOCUMENT**
