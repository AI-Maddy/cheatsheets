====================================================================
Zero Trust Architecture - Never Trust, Always Verify
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: NIST SP 800-207, NSA Zero Trust Framework

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Zero Trust Principles:**

1. **Verify explicitly:** Authenticate every request (user, device, context)
2. **Least privilege:** Minimize access rights
3. **Assume breach:** Segment network, monitor continuously

**Traditional Network:**

.. code-block:: text

    Firewall → Trusted Internal Network (full access)

**Zero Trust:**

.. code-block:: text

    Every request → Policy Decision Point → Grant minimal access

**Key Technologies:**

✅ **Identity:** Multi-factor authentication (MFA)
✅ **Microsegmentation:** Isolate workloads
✅ **Continuous verification:** Monitor behavior, revoke access if suspicious

Introduction
============

**Traditional security:** Castle-and-moat (perimeter defense).

**Problem:** Insider threats, lateral movement after breach.

**Zero Trust:** No implicit trust based on network location.

**Example:**

- Employee laptop on corporate WiFi: Still requires MFA
- Contractor VPN access: Limited to specific servers only
- Compromised device: Blocked after behavioral anomaly detected

Zero Trust for OT/ICS Environments
====================================

**Challenge:** Legacy industrial systems cannot support modern authentication.

**Solution: Zero Trust Overlay**

.. code-block:: text

    ┌─────────────────────────┐
    │ Corporate Network       │
    └────────┬────────────────┘
             │ (Identity Proxy)
    ┌────────▼────────────────┐
    │ Zero Trust Gateway      │
    │ ├─ User auth (MFA)      │
    │ ├─ Device posture check │
    │ └─ Microsegmentation    │
    └────────┬────────────────┘
             │ (Encrypted tunnel per session)
    ┌────────▼────────────────┐
    │ SCADA/PLC Network       │
    │ ├─ Legacy Modbus        │
    │ └─ No authentication    │
    └─────────────────────────┘

**Implementation:**

.. code-block:: python

    class ZeroTrustGateway:
        def __init__(self):
            self.policy_engine = PolicyEngine()
            self.device_inventory = DeviceInventory()
        
        def authorize_access(self, user, device, resource):
            # 1. Verify user identity (MFA)
            if not self.verify_mfa(user):
                return deny("MFA failed")
            
            # 2. Check device posture
            if not self.device_inventory.is_compliant(device):
                return deny("Device not patched")
            
            # 3. Evaluate context (time, location, behavior)
            context = {
                'time': datetime.now(),
                'ip_address': device.ip,
                'risk_score': self.calculate_risk(user, device)
            }
            
            # 4. Policy decision
            if self.policy_engine.evaluate(user, resource, context):
                # Grant minimal access
                return grant_access(user, resource, duration=3600)  # 1 hour
            else:
                return deny("Policy violation")

Microsegmentation
==================

**Concept:** Isolate workloads with granular firewall rules.

**Traditional VLAN:**

.. code-block:: text

    PLC VLAN (192.168.10.0/24)
    ├─ PLC 1 can access PLC 2 ✅
    ├─ PLC 1 can access PLC 3 ✅
    └─ If PLC 1 compromised → all PLCs at risk

**Zero Trust Microsegmentation:**

.. code-block:: text

    PLC 1 (192.168.10.10)
    ├─ Can ONLY talk to HMI (192.168.5.100) on port 502
    ├─ CANNOT talk to PLC 2 or PLC 3
    └─ If PLC 1 compromised → lateral movement blocked

**Linux iptables Example:**

.. code-block:: bash

    # PLC 1 can only communicate with HMI
    iptables -A FORWARD -s 192.168.10.10 -d 192.168.5.100 -p tcp --dport 502 -j ACCEPT
    iptables -A FORWARD -s 192.168.5.100 -d 192.168.10.10 -p tcp --sport 502 -j ACCEPT
    
    # Deny all other traffic from PLC 1
    iptables -A FORWARD -s 192.168.10.10 -j DROP

**Software-Defined Networking (SDN):**

.. code-block:: python

    # OpenFlow controller for dynamic microsegmentation
    def install_flow_rule(switch, src_device, dst_device, protocol, port):
        flow = {
            'match': {
                'ipv4_src': src_device.ip,
                'ipv4_dst': dst_device.ip,
                'ip_proto': protocol,
                'tcp_dst': port
            },
            'actions': ['OUTPUT:1'],
            'priority': 100,
            'idle_timeout': 3600  # 1 hour
        }
        switch.install_flow(flow)
    
    # When engineer needs to access PLC for 1 hour
    install_flow_rule(sdn_switch, engineer_laptop, plc_1, 'TCP', 502)

Continuous Verification
=========================

**Monitor behavior and revoke access if suspicious.**

.. code-block:: python

    class BehaviorMonitor:
        def __init__(self):
            self.baseline = self.build_baseline()
        
        def build_baseline(self):
            """Learn normal user behavior over 30 days"""
            return {
                'typical_login_hours': [8, 9, 10, ..., 17],
                'typical_locations': ['Office', 'Home'],
                'typical_devices': ['Laptop-123', 'Phone-456'],
                'data_exfiltration_rate': 10_000  # bytes/min
            }
        
        def detect_anomaly(self, user, session):
            # Check login time
            if session.hour not in self.baseline['typical_login_hours']:
                self.raise_alert("Off-hours login", user, session)
            
            # Check location (GeoIP)
            if session.location not in self.baseline['typical_locations']:
                self.raise_alert("Unusual location", user, session)
            
            # Check data exfiltration
            if session.bytes_transferred > 1_000_000:  # 1 MB
                self.revoke_access(user, session)
                self.raise_alert("Mass data download", user, session)

Device Posture Assessment
===========================

**Verify device security before granting access.**

.. code-block:: python

    class DevicePostureCheck:
        def __init__(self):
            self.required_patches = ['CVE-2024-1234', 'CVE-2024-5678']
            self.required_av_version = '2024.01.15'
        
        def assess_device(self, device):
            # 1. Check OS patches
            missing_patches = self.check_patches(device)
            if missing_patches:
                return {
                    'compliant': False,
                    'reason': f"Missing patches: {missing_patches}"
                }
            
            # 2. Check antivirus
            av_version = device.get_av_version()
            if av_version < self.required_av_version:
                return {
                    'compliant': False,
                    'reason': "Outdated antivirus"
                }
            
            # 3. Check for malware
            if device.malware_detected():
                return {
                    'compliant': False,
                    'reason': "Malware detected"
                }
            
            # 4. Check disk encryption
            if not device.is_encrypted():
                return {
                    'compliant': False,
                    'reason': "Disk not encrypted"
                }
            
            return {'compliant': True}

**Agent on Device (C Code):**

.. code-block:: c

    // Device agent reports posture to Zero Trust gateway
    #include <openssl/ssl.h>
    
    typedef struct {
        char os_version[32];
        char patch_level[32];
        bool disk_encrypted;
        bool firewall_enabled;
        uint32_t malware_signatures_version;
    } device_posture_t;
    
    void report_posture(SSL *ssl) {
        device_posture_t posture;
        
        // Collect device information
        get_os_version(posture.os_version);
        get_patch_level(posture.patch_level);
        posture.disk_encrypted = check_bitlocker();
        posture.firewall_enabled = check_firewall();
        posture.malware_signatures_version = get_av_version();
        
        // Send to gateway
        SSL_write(ssl, &posture, sizeof(posture));
    }

Exam Questions
==============

**Q1: Zero Trust for SCADA (Medium)**

A power utility has 500 RTUs (Remote Terminal Units) running legacy firmware with no authentication. How to implement Zero Trust without replacing RTUs?

**Answer:**

**Solution: Zero Trust Overlay with Network Gateway**

.. code-block:: text

    Engineer Workstation
           ↓ (1) Authenticate with MFA
    Zero Trust Gateway
           ├─ (2) Verify device posture
           ├─ (3) Create encrypted tunnel to specific RTU
           └─ (4) Log all commands
           ↓ (5) Translate to legacy protocol (Modbus/DNP3)
    RTU (no modification needed)

**Implementation:**

1. **Deploy gateway** in front of RTU network
2. **All access** goes through gateway (no direct RTU access)
3. **Per-session tunnels:** Engineer can only access RTU-17 for 1 hour
4. **Command logging:** All Modbus commands logged for audit
5. **Behavioral analysis:** Alert if engineer reads unexpected registers

**Q2: Zero Trust vs VPN (Hard)**

Compare Zero Trust to traditional VPN. What are the security differences?

**Answer:**

+-------------------------+---------------------------+------------------------+
| Feature                 | Traditional VPN           | Zero Trust             |
+=========================+===========================+========================+
| Access scope            | Full network access       | Per-resource           |
+-------------------------+---------------------------+------------------------+
| Authentication          | Once (at login)           | Continuous             |
+-------------------------+---------------------------+------------------------+
| Device posture          | ❌ Not checked            | ✅ Required            |
+-------------------------+---------------------------+------------------------+
| Lateral movement        | ✅ Possible               | ❌ Blocked             |
+-------------------------+---------------------------+------------------------+
| Visibility              | ⚠️  Limited               | ✅ All requests logged |
+-------------------------+---------------------------+------------------------+

**Attack Scenario:**

**VPN:**
1. Attacker phishes VPN credentials
2. Logs in → full access to internal network
3. Moves laterally to critical servers

**Zero Trust:**
1. Attacker phishes credentials
2. MFA required (attacker blocked)
3. If attacker bypasses MFA, device posture check fails (unrecognized device)
4. If attacker spoofs device, behavioral analysis detects anomaly → access revoked

**Verdict:** Zero Trust provides defense-in-depth.

Standards
=========

- **NIST SP 800-207:** Zero Trust Architecture
- **NSA Zero Trust Framework:** Implementation guidance
- **CISA Zero Trust Maturity Model:** Assessment framework

**END OF DOCUMENT**
