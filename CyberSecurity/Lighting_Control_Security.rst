====================================================================
Lighting Control Security - Smart Building Illumination
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: DALI, BACnet, Zigbee

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Lighting Control Protocols:**

- **DALI:** Digital Addressable Lighting Interface (commercial)
- **Zigbee:** Wireless smart lighting (residential)
- **BACnet:** Building automation integration

**Attack Scenarios:**

- Disable emergency lighting during evacuation
- Cause seizures with rapid flashing (photosensitive epilepsy)
- Energy theft (manipulate demand response)

Introduction
============

**Threat Model:** Lighting often overlooked but critical for safety.

DALI Security
==============

.. code-block:: c

    // DALI command to set brightness
    #include <dali.h>
    
    void set_light_level(uint8_t address, uint8_t level) {
        dali_cmd_t cmd;
        cmd.address = address;
        cmd.command = DALI_CMD_DIRECT_ARC_POWER;
        cmd.data = level;  // 0-254
        
        dali_send(&cmd);
    }

**Attack: Rapid Flashing**

.. code-block:: python

    # Malicious script causes seizure-inducing flashing
    import time
    
    while True:
        set_all_lights(255)  # Full brightness
        time.sleep(0.1)
        set_all_lights(0)    # Off
        time.sleep(0.1)
        # Flashing at 5 Hz (dangerous for photosensitive individuals)

**Defense: Rate Limiting**

.. code-block:: c

    #define MAX_TRANSITIONS_PER_SECOND 2
    
    int apply_light_command(uint8_t level) {
        static uint32_t last_change_time = 0;
        static uint8_t transition_count = 0;
        
        uint32_t now = get_millis();
        
        // Reset counter every second
        if (now - last_change_time > 1000) {
            transition_count = 0;
            last_change_time = now;
        }
        
        // Enforce rate limit
        if (transition_count >= MAX_TRANSITIONS_PER_SECOND) {
            return -1;  // Reject
        }
        
        transition_count++;
        set_dali_level(level);
        return 0;
    }

Standards
=========

- **IEC 62386:** DALI standard

**END OF DOCUMENT**
