====================================================================
Fire Safety System Security - Life Safety Network Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NFPA 72, UL 864

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Fire Alarm Systems:**

- Smoke detectors, pull stations, notification devices (strobes, horns)
- **Protocols:** Proprietary (Notifier, Simplex), BACnet integration
- **Safety-Critical:** UL 864 certified

**Attack Impact:**

- **False alarm:** Evacuation fatigue, complacency
- **Disabled alarm:** No warning during actual fire → fatalities
- **Notification device manipulation:** Excessive volume → panic

Introduction
============

**Threat Model:** Life safety systems must be highly reliable.

**Defense Strategy:**

✅ **Network isolation:** Fire alarm network separate from IT
✅ **Tamper detection:** Physical seals on devices
✅ **Redundancy:** Dual notification paths
✅ **Fail-safe:** Wired connections preferred over wireless

Attack Scenario: Alarm Disable
================================

.. code-block:: python

    # Attacker disables fire alarm via network
    import requests
    
    # Fire alarm panel with web interface (poor security)
    panel_ip = "192.168.1.200"
    
    # Disable alarm zones
    requests.post(f"http://{panel_ip}/api/zone/disable",
                  json={'zones': [1, 2, 3, 4, 5]})  # All zones disabled

**Defense: Physical Override**

.. code-block:: c

    // Fire alarm cannot be disabled via software alone
    int disable_alarm_zone(uint8_t zone_id) {
        // Check physical key switch
        if (!read_key_switch_position()) {
            log_event("Attempted software disable without key switch");
            return -1;
        }
        
        // Require dual authorization
        if (!verify_second_operator()) {
            return -1;
        }
        
        // Time-limited disable (max 1 hour for maintenance)
        disable_zone_with_timeout(zone_id, 3600);
        return 0;
    }

Exam Questions
==============

**Q1: Fire Alarm Network Segmentation (Medium)**

Fire alarm system integrated with BACnet for HVAC smoke control. How to secure integration without compromising fire safety?

**Answer:**

**Solution: One-Way Gateway**

.. code-block:: text

    Fire Alarm Network (isolated)
           ↓ (One-way data diode)
    BACnet Gateway (read-only)
           ↓
    HVAC System (receives fire alarm status)

Fire alarm sends status to HVAC (smoke detected → shut down air handlers)
HVAC CANNOT send commands back to fire alarm

Standards
=========

- **NFPA 72:** National Fire Alarm Code
- **UL 864:** Fire alarm control panel certification

**END OF DOCUMENT**
