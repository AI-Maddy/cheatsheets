====================================================================
HVAC Control Security - Heating, Ventilation, Air Conditioning
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ASHRAE 135, NIST SP 800-82, IEC 62443

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**HVAC Security Risks:**

- **Physical safety:** Overheat/freeze buildings (health risk)
- **Data centers:** HVAC failure → server overheating → downtime
- **Energy theft:** Manipulate demand response (grid instability)
- **Ransomware:** Lock HVAC controls until payment

**Attack Surface:**

- BACnet/IP (UDP 47808) - often unsecured
- Modbus TCP (port 502)
- Web-based HMI (HTTP/HTTPS)
- Building management system (BMS) workstations

Introduction
============

**HVAC systems** control temperature, humidity, and air quality in commercial buildings, data centers, and industrial facilities.

**Cyber-Physical Impact:**

- **Comfort:** Make building uninhabitable
- **Safety:** Carbon monoxide buildup (disabled ventilation)
- **Energy:** $100,000+ electricity bill from malicious settings
- **Business continuity:** Data center outage

HVAC Architecture
==================

.. code-block:: text

    ┌────────────────────────┐
    │ Building Mgmt System   │ (Operator workstation)
    │ ├─ Schneider StruxWare │
    │ └─ BACnet client       │
    └───────────┬────────────┘
                │ BACnet/IP (UDP)
    ┌───────────▼────────────┐
    │ HVAC Controller (DDC)  │ Direct Digital Control
    │ ├─ Temp sensors        │
    │ ├─ Damper actuators    │
    │ └─ Fan control         │
    └───────────┬────────────┘
                │ Modbus RTU (RS-485)
    ┌───────────▼────────────┐
    │ Variable Air Volume    │
    │ (VAV) Boxes            │
    └────────────────────────┘

Attack Scenario: Temperature Manipulation
===========================================

**Attack:** Overheat data center to cause server failures.

.. code-block:: python

    import bacpypes
    from bacpypes.pdu import Address
    from bacpypes.apdu import WritePropertyRequest
    
    # Attacker connects to HVAC controller on BACnet network
    def attack_hvac_setpoint(target_ip):
        # BACnet device address
        device_addr = Address(f"{target_ip}:47808")
        
        # Target: Analog Value object (temperature setpoint)
        request = WritePropertyRequest(
            objectIdentifier=('analogValue', 1),
            propertyIdentifier='presentValue',
            propertyValue=95.0  # Set to 95°F (servers overheat at 80°F)
        )
        
        # Send command (no authentication in legacy BACnet)
        send_bacnet_command(device_addr, request)

**Impact:**

- Servers reach 85°F → thermal throttling
- At 95°F → automatic shutdown
- Estimated downtime: 4 hours
- Revenue loss: $500,000

**Mitigation:**

.. code-block:: c

    // Implement setpoint limits in controller firmware
    #define MIN_SETPOINT 65.0  // °F
    #define MAX_SETPOINT 78.0  // °F
    
    int validate_setpoint(float new_setpoint) {
        if (new_setpoint < MIN_SETPOINT || new_setpoint > MAX_SETPOINT) {
            log_security_event("Invalid setpoint rejected", new_setpoint);
            return -1;  // Reject
        }
        return 0;  // Accept
    }

Ransomware Attack on HVAC
===========================

**Real Case: 2020 - HVAC Ransomware**

Attackers encrypted BMS workstation, demanded $10,000 ransom.

**Attack Vector:**

1. Phishing email → BMS operator workstation infected
2. Ransomware encrypts HVAC control software
3. HVAC stuck in current state (no adjustments possible)
4. Building temperature rises to 85°F

**Mitigation:**

.. code-block:: bash

    # Backup BMS configuration (daily)
    #!/bin/bash
    backup_date=$(date +%Y%m%d)
    
    # Export BACnet database
    bacnet_export --output /backup/bacnet_config_$backup_date.xml
    
    # Export HVAC schedules
    cp /etc/hvac/schedules.json /backup/schedules_$backup_date.json
    
    # Encrypt and upload to offsite storage
    tar -czf - /backup | openssl enc -aes-256-cbc -pbkdf2 | \
        aws s3 cp - s3://hvac-backups/backup_$backup_date.tar.gz.enc

**Recovery Plan:**

1. Isolate infected workstation (disconnect network)
2. Deploy backup BMS on spare workstation
3. Restore from previous day's backup
4. Resume HVAC control within 2 hours

Network Segmentation
=====================

**Best Practice Architecture:**

.. code-block:: text

    Corporate Network (WiFi, Desktops)
           ↓ (Firewall - deny all except HTTPS to BMS)
    Building Management DMZ
           ├─ BMS workstation (read-only from corporate)
           └─ Historian (data logging)
           ↓ (Firewall - whitelist BACnet traffic)
    HVAC Control Network (isolated VLAN)
           ├─ HVAC controllers
           ├─ VAV boxes
           └─ Sensors/actuators

**Firewall Rules:**

.. code-block:: bash

    # Allow BMS workstation → HVAC controllers (BACnet)
    iptables -A FORWARD -s 192.168.10.100 -d 192.168.20.0/24 -p udp --dport 47808 -j ACCEPT
    
    # Allow HVAC controllers → BMS (BACnet responses)
    iptables -A FORWARD -s 192.168.20.0/24 -d 192.168.10.100 -p udp --sport 47808 -j ACCEPT
    
    # Deny all other traffic between VLANs
    iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.20.0/24 -j DROP

Anomaly Detection
==================

**Detect malicious HVAC commands:**

.. code-block:: python

    class HVACAnomalyDetector:
        def __init__(self):
            self.baseline = {
                'setpoint_min': 68.0,
                'setpoint_max': 74.0,
                'typical_change_rate': 2.0  # °F per hour
            }
        
        def detect_anomaly(self, current_setpoint, new_setpoint, time_delta):
            # Check for sudden large changes
            change_rate = abs(new_setpoint - current_setpoint) / (time_delta / 3600)
            
            if change_rate > 10.0:  # 10°F per hour is suspicious
                self.trigger_alert(f"Rapid setpoint change: {change_rate} °F/hr")
                return True
            
            # Check for out-of-range setpoints
            if new_setpoint < 60 or new_setpoint > 80:
                self.trigger_alert(f"Setpoint outside safe range: {new_setpoint}")
                return True
            
            return False
        
        def trigger_alert(self, message):
            # Send SIEM alert
            syslog.send(f"HVAC_ANOMALY: {message}")
            
            # Notify building engineer
            send_sms("+1234567890", message)

Exam Questions
==============

**Q1: HVAC Attack Surface (Medium)**

List 5 attack vectors for compromising HVAC system and rank by likelihood.

**Answer:**

1. **Phishing (High):** Infect BMS operator workstation
2. **Unpatched BMS software (High):** Exploit known vulnerabilities
3. **Default credentials (Medium):** BACnet devices often ship with admin/admin
4. **Insider threat (Medium):** Disgruntled facilities staff
5. **Physical access (Low):** Tamper with controller in mechanical room

**Mitigation Priority:**

1. Security awareness training (phishing)
2. Patch management policy
3. Change default passwords + MFA
4. Background checks for facilities staff
5. Lock mechanical rooms + badge access

**Q2: HVAC Redundancy (Hard)**

Design fault-tolerant HVAC control for critical data center. Single controller failure must not affect cooling.

**Answer:**

**Redundant Architecture:**

.. code-block:: text

    Primary HVAC Controller
           ├─ Controls chillers 1-3
           ├─ Monitors temp sensors
           └─ Heartbeat to secondary
    
    Secondary HVAC Controller (hot standby)
           ├─ Monitors same sensors
           ├─ Takes over if primary fails
           └─ Controls same chillers
    
    Tertiary: Manual Override
           └─ Physical switches (no cyber dependency)

**Failover Logic:**

.. code-block:: c

    #define HEARTBEAT_TIMEOUT 5  // seconds
    
    void secondary_controller_loop(void) {
        while(1) {
            if (time_since_primary_heartbeat() > HEARTBEAT_TIMEOUT) {
                // Primary failed, take over
                log_event("Primary controller failed, activating secondary");
                activate_chiller_control();
                send_alert("HVAC failover activated");
            }
            
            sleep(1);
        }
    }

**Testing:** Monthly failover drills (manually disable primary, verify secondary takes over <30 seconds).

Standards
=========

- **ASHRAE 135:** BACnet protocol
- **IEC 62443:** Industrial control system security
- **NIST SP 800-82:** Guide to ICS security

**END OF DOCUMENT**
