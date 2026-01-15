====================================================================
Ventilator Security - Critical Care Device Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: FDA Guidance, IEC 60601-1

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Ventilators:**

- Life-support devices for patients unable to breathe
- **Connectivity:** Hospital network, EHR integration, remote monitoring
- **Attack Impact:** Patient death from altered settings

**Security Priorities:**

✅ **Safety first:** Never compromise patient safety for security
✅ **Fail-safe:** Mechanical override if software fails
✅ **Monitoring:** Detect anomalous settings changes
✅ **Isolation:** Air-gap critical control loops

Introduction
============

**COVID-19 Impact:** Ventilator shortages highlighted supply chain risks.

**Threat Model:**

1. **Ransomware:** Lock ventilator controls
2. **Sabotage:** Modify oxygen/pressure settings
3. **Data breach:** Patient respiratory data (HIPAA)

Attack Scenario: Settings Manipulation
========================================

.. code-block:: python

    # Attacker modifies ventilator settings via network
    import requests
    
    # Legacy ventilator with HTTP API (no auth)
    ventilator_ip = "192.168.1.50"
    
    # Malicious settings (dangerous)
    malicious_settings = {
        'tidal_volume': 1500,  # ml (normal: 500, this causes barotrauma)
        'oxygen_concentration': 100,  # % (prolonged 100% O2 is toxic)
        'respiratory_rate': 50  # breaths/min (normal: 12-20)
    }
    
    # Send to ventilator
    response = requests.post(f"http://{ventilator_ip}/api/settings",
                            json=malicious_settings)

**Impact:** Lung injury, oxygen toxicity, patient death.

Defense: Multi-Layer Safety
=============================

**Layer 1: Input Validation**

.. code-block:: c

    // Validate ventilator settings before applying
    typedef struct {
        uint16_t tidal_volume_ml;
        uint8_t oxygen_percent;
        uint8_t respiratory_rate;
    } ventilator_settings_t;
    
    int validate_settings(ventilator_settings_t *settings) {
        // Check tidal volume range
        if (settings->tidal_volume_ml < 300 || settings->tidal_volume_ml > 800) {
            log_alarm("Tidal volume out of range");
            return -1;
        }
        
        // Check oxygen concentration
        if (settings->oxygen_percent < 21 || settings->oxygen_percent > 100) {
            return -1;
        }
        
        // Check respiratory rate
        if (settings->respiratory_rate < 8 || settings->respiratory_rate > 35) {
            return -1;
        }
        
        return 0;
    }

**Layer 2: Rate Limiting**

.. code-block:: c

    // Limit how quickly settings can change
    #define MAX_SETTING_CHANGES_PER_HOUR 10
    
    int apply_settings(ventilator_settings_t *new_settings) {
        static uint32_t last_change_time[10];
        static uint8_t change_idx = 0;
        
        uint32_t current_time = get_timestamp();
        
        // Count changes in last hour
        uint8_t changes_last_hour = 0;
        for (int i = 0; i < 10; i++) {
            if (current_time - last_change_time[i] < 3600) {
                changes_last_hour++;
            }
        }
        
        if (changes_last_hour >= MAX_SETTING_CHANGES_PER_HOUR) {
            trigger_alert("Excessive setting changes detected");
            return -1;  // Possible attack
        }
        
        // Record change
        last_change_time[change_idx++] = current_time;
        change_idx %= 10;
        
        // Apply settings
        return set_ventilator_parameters(new_settings);
    }

**Layer 3: Mechanical Override**

.. code-block:: text

    Software Control (network-connected)
           ↓
    Safety PLC (independent verification)
           ↓
    Mechanical Relief Valve (hardware failsafe)
    
    If pressure exceeds 40 cmH2O, mechanical valve opens
    (no software dependency)

Network Isolation
==================

.. code-block:: text

    Hospital Network (EMR, Pharmacy)
           ↓ (Firewall: HTTPS only, whitelist)
    Medical Device DMZ
           ├─ Ventilator Monitor (data collection)
           └─ Read-only access to ventilators
           ↓ (Air-gap: NO direct network connection)
    Ventilator Control Network (isolated)
           ├─ Ventilator 1 (critical control loop local only)
           ├─ Ventilator 2
           └─ Bedside monitor

**Data Flow:**

.. code-block:: python

    # Ventilator monitoring (read-only, one-way)
    class VentilatorMonitor:
        def __init__(self):
            self.serial_port = serial.Serial('/dev/ttyUSB0', 9600)
        
        def read_telemetry(self):
            # One-way serial: Ventilator → Monitor
            # NO commands sent back
            data = self.serial_port.readline()
            
            telemetry = parse_ventilator_telemetry(data)
            
            # Send to hospital EMR (read-only)
            send_to_emr(telemetry)

Exam Questions
==============

**Q1: Ventilator Ransomware Response (Hard)**

Ransomware encrypts ventilator control software. Patient is on ventilator. What are immediate actions?

**Answer:**

**Immediate (0-5 minutes):**
1. **Switch to manual ventilation:** Bag-valve-mask (Ambu bag)
2. **Disconnect ventilator from network:** Prevent spread
3. **Notify ICU staff:** All hands on deck

**Short-term (5-60 minutes):**
1. **Deploy backup ventilators:** From operating room, emergency stockpile
2. **Restore from backup:** Load ventilator firmware from USB
3. **Isolate infected units:** Quarantine affected devices

**Long-term (1-24 hours):**
1. **Forensic analysis:** How did ransomware spread?
2. **Patch vulnerability:** Update all ventilators
3. **Network segmentation:** Prevent future attacks

**Q2: Safety vs Security Trade-off (Medium)**

Adding authentication to ventilator settings increases latency from 10ms to 100ms. Respiratory therapist needs to quickly adjust settings during crisis. How to balance?

**Answer:**

**Option 1: Pre-Authentication**
- Therapist logs in at shift start (badge + PIN)
- Session valid for 8 hours
- Settings changes instant (no per-change auth)

**Option 2: Dual-Mode**
- **Normal mode:** Authentication required (100ms latency)
- **Emergency mode:** Physical button on ventilator disables auth for 5 minutes
- Audit log records emergency mode activation

**Option 3: Local Override**
- Physical knobs on ventilator override network commands
- No latency, no authentication needed
- Knob positions logged for audit

**Best Practice:** Option 3 (local override) ensures patient safety.

Standards
=========

- **IEC 60601-1:** Medical electrical equipment safety
- **FDA Guidance (2023):** Cybersecurity for medical devices
- **ISO 80601-2-12:** Ventilator specific requirements

**END OF DOCUMENT**
