🏢 **BACNET SECURITY FOR BUILDING AUTOMATION SYSTEMS**
═══════════════════════════════════════════════════════════════════════

**BACnet Protocol Security (ASHRAE Standard 135)**  
**Purpose:** Building automation security 🏢 | BACnet/SC (Secure Connect) 🔐 | HVAC protection 🌡️  
**Scope:** Commercial buildings, HVAC, lighting, access control, fire safety

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**BACnet** (Building Automation and Control Networks) is the dominant protocol for building management systems (BMS).

**Legacy BACnet:** No native security (plaintext, no authentication)  
**BACnet/SC (2016+):** Secure Connect with TLS 1.3, certificate-based authentication

**Common deployments:** HVAC control, lighting, fire alarms, access control, energy management.

════════════════════════════════════════════════════════════════════════════

📐 **BACNET PROTOCOL OVERVIEW**
─────────────────────────────────────────────────────────────────────────

**ASHRAE Standard 135 (BACnet)**

.. code-block:: text

   BACnet Protocol Stack:
   
   ┌─────────────────────────────────────┐
   │ Application Layer (BACnet Services) │  ← Read/Write properties, alarms
   ├─────────────────────────────────────┤
   │ Network Layer                       │  ← Routing, addressing
   ├─────────────────────────────────────┤
   │ Data Link Layer                     │  ← BACnet/IP, BACnet/MSTP, BACnet/SC
   ├─────────────────────────────────────┤
   │ Physical Layer                      │  ← Ethernet, RS-485, IP
   └─────────────────────────────────────┘

**BACnet Transport Options:**

| Transport | Description | Security | Use Case |
|:----------|:------------|:---------|:---------|
| **BACnet/IP** | BACnet over UDP (port 47808) | None (legacy) | Most common, LAN-based |
| **BACnet/MSTP** | Master-Slave Token Passing (RS-485) | None | Field devices, low-cost |
| **BACnet/SC** | Secure Connect (TLS 1.3) | ✅ Strong | Modern, secure deployments |
| **BACnet/WS** | WebSocket (HTTP/HTTPS) | ⚠️ Depends on TLS | Cloud integration |

**BACnet Objects (Addressable entities):**

.. code-block:: python

   # BACnet object types (ASHRAE 135 Annex L)
   BACNET_OBJECTS = {
       'ANALOG_INPUT': 0,      # Temperature sensor, pressure sensor
       'ANALOG_OUTPUT': 1,     # Valve position, damper control
       'ANALOG_VALUE': 2,      # Setpoint, calculated value
       'BINARY_INPUT': 3,      # Motion detector, door contact
       'BINARY_OUTPUT': 4,     # Relay, fan on/off
       'BINARY_VALUE': 5,      # Status flag
       'DEVICE': 8,            # BACnet device (controller)
       'FILE': 10,             # File transfer
       'SCHEDULE': 17,         # Time-based schedules
       'TREND_LOG': 20,        # Historical data
       'NOTIFICATION_CLASS': 15  # Alarm routing
   }

════════════════════════════════════════════════════════════════════════════

🔓 **LEGACY BACNET SECURITY ISSUES**
─────────────────────────────────────────────────────────────────────────

**BACnet/IP (UDP) — No Native Security:**

.. code-block:: text

   Vulnerabilities:
   ├─ No authentication (anyone can send commands)
   ├─ No encryption (plaintext communication)
   ├─ No integrity checking (commands can be modified)
   ├─ Broadcast discovery (attackers can enumerate devices)
   └─ UDP-based (spoofing, amplification attacks)

**Attack Scenarios:**

.. code-block:: python

   # Example: Unauthenticated BACnet command (legacy)
   import socket
   
   def send_bacnet_write_property(target_ip, object_type, object_instance, property_id, value):
       """
       Send BACnet WriteProperty command (NO AUTHENTICATION).
       
       WARNING: This demonstrates legacy BACnet vulnerability.
       Do NOT use on production systems without authorization.
       """
       BACNET_PORT = 47808
       
       # Construct BACnet Write-Property APDU (simplified)
       # In reality, uses BACnet encoding (ASN.1)
       bacnet_packet = bytearray([
           0x81,  # BACnet/IP BVLC Type
           0x0A,  # Original-Unicast-NPDU
           0x00, 0x11,  # Length
           0x01,  # NPDU version
           0x20,  # Control flags (expecting reply)
           0x0F,  # APDU Type: Confirmed-Request, Write-Property
           0x00,  # Invoke ID
           # Object ID, Property ID, Value (simplified)
           # ... (actual encoding complex)
       ])
       
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       sock.sendto(bacnet_packet, (target_ip, BACNET_PORT))
       sock.close()
       
       print(f"Sent WriteProperty to {target_ip} (NO AUTH REQUIRED)")
   
   # Attack: Change thermostat setpoint from 72°F to 90°F
   # send_bacnet_write_property('192.168.1.100', 'ANALOG_VALUE', 1, 'PRESENT_VALUE', 90.0)

**Real-World Attacks:**

```
2013: BACnet devices exposed on Shodan (100,000+ devices)
2017: Researchers remotely controlled HVAC in commercial buildings
2019: Ransomware groups targeting BMS (disabled HVAC to force payment)
2021: Multiple CVEs for BACnet devices (authentication bypass, RCE)
```

════════════════════════════════════════════════════════════════════════════

🔐 **BACNET/SC (SECURE CONNECT) — MODERN SECURITY**
─────────────────────────────────────────────────────────────────────────

**BACnet/SC (Addendum 135-2016bj):**

Introduced **Secure Connect** using TLS 1.3 and WebSockets.

**Architecture:**

.. code-block:: text

   BACnet/SC Hub-and-Spoke Model:
   
   ┌──────────────────────────────────────────────────────────┐
   │ BACnet/SC Hub (Central Security Gateway)               │
   │ ├─ Certificate Authority (issues device certs)          │
   │ ├─ TLS 1.3 termination                                  │
   │ └─ Access control lists (ACLs)                          │
   └─────────────┬────────────────────────────────────────────┘
                 │ TLS 1.3 WebSocket
   ┌─────────────▼──────────┬──────────────┬─────────────────┐
   │ BACnet/SC Node 1       │ Node 2       │ Node 3          │
   │ (HVAC Controller)      │ (Lighting)   │ (Access Control)│
   │ - Has certificate      │              │                 │
   │ - Authenticates to Hub │              │                 │
   └────────────────────────┴──────────────┴─────────────────┘

**Security Features:**

| Feature | Description |
|:--------|:------------|
| **TLS 1.3** | Strong encryption (AES-GCM), forward secrecy |
| **Certificate-based auth** | X.509 certificates for device identity |
| **Hub architecture** | Central policy enforcement point |
| **Access control** | ACLs define which nodes can communicate |
| **Integrity** | TLS MAC prevents command tampering |

**BACnet/SC Configuration:**

.. code-block:: python

   # BACnet/SC Hub configuration
   class BACnetSCHub:
       """
       BACnet/SC Hub (ASHRAE 135-2016bj).
       Central security gateway for BACnet network.
       """
       
       def __init__(self, hub_cert, hub_key, ca_cert):
           self.hub_cert = hub_cert
           self.hub_key = hub_key
           self.ca_cert = ca_cert
           self.connected_nodes = {}
           self.access_control_lists = {}
       
       def authenticate_node(self, node_cert):
           """
           Authenticate BACnet/SC node using X.509 certificate.
           """
           # Verify certificate chain
           if not self.verify_certificate(node_cert, self.ca_cert):
               print("Certificate verification failed")
               return False
           
           # Extract device ID from certificate CN
           device_id = self.extract_device_id(node_cert)
           
           # Check if device authorized
           if device_id not in self.access_control_lists:
               print(f"Device {device_id} not in ACL")
               return False
           
           print(f"Node {device_id} authenticated successfully")
           self.connected_nodes[device_id] = {
               'cert': node_cert,
               'connected_at': datetime.utcnow()
           }
           return True
       
       def enforce_access_control(self, source_device, dest_device, bacnet_service):
           """
           Enforce ACL for BACnet communication.
           
           Example ACL:
           - HVAC_Controller → Chiller: Allow ReadProperty, WriteProperty
           - Lighting_Controller → HVAC: Deny WriteProperty
           """
           acl_key = (source_device, dest_device)
           
           if acl_key not in self.access_control_lists:
               print(f"No ACL for {source_device} → {dest_device}")
               return False
           
           allowed_services = self.access_control_lists[acl_key]
           
           if bacnet_service in allowed_services:
               return True
           else:
               print(f"ACL denied: {source_device} cannot {bacnet_service} on {dest_device}")
               return False
       
       def configure_acl(self, source, dest, allowed_services):
           """Configure access control list"""
           self.access_control_lists[(source, dest)] = allowed_services
   
   # Example: Configure BACnet/SC Hub
   hub = BACnetSCHub(
       hub_cert='/etc/bacnet/hub.crt',
       hub_key='/etc/bacnet/hub.key',
       ca_cert='/etc/bacnet/ca.crt'
   )
   
   # Define ACLs
   hub.configure_acl(
       source='HVAC_Controller',
       dest='Chiller_1',
       allowed_services=['ReadProperty', 'WriteProperty', 'SubscribeCOV']
   )
   
   hub.configure_acl(
       source='Operator_Workstation',
       dest='HVAC_Controller',
       allowed_services=['ReadProperty', 'WriteProperty']  # Full access
   )
   
   hub.configure_acl(
       source='Guest_Portal',
       dest='HVAC_Controller',
       allowed_services=['ReadProperty']  # Read-only
   )

════════════════════════════════════════════════════════════════════════════

🛡️ **SECURING LEGACY BACNET DEPLOYMENTS**
─────────────────────────────────────────────────────────────────────────

**Challenge:** Most existing BACnet networks use legacy BACnet/IP (no security).

**Mitigation Strategies:**

**1. Network Segmentation (VLAN Isolation)**

.. code-block:: text

   Network Architecture:
   
   ┌─────────────────────────────────────────────────────────┐
   │ Corporate Network (VLAN 10)                            │
   │ ├─ Office PCs, email, internet                         │
   └────────────┬────────────────────────────────────────────┘
                │ Firewall (deny all by default)
   ┌────────────▼────────────────────────────────────────────┐
   │ BMS DMZ (VLAN 100)                                     │
   │ ├─ BMS operator workstations (controlled access)       │
   │ └─ BACnet gateway (protocol translation)               │
   └────────────┬────────────────────────────────────────────┘
                │ Firewall (port 47808 only)
   ┌────────────▼────────────────────────────────────────────┐
   │ BACnet Network (VLAN 200) — ISOLATED                  │
   │ ├─ HVAC controllers                                     │
   │ ├─ Lighting controllers                                 │
   │ ├─ Access control panels                               │
   │ └─ Fire alarm system                                    │
   └─────────────────────────────────────────────────────────┘

**2. BACnet Firewall (Protocol Filter)**

.. code-block:: python

   class BACnetFirewall:
       """
       Application-layer firewall for BACnet/IP.
       Filters based on BACnet services, object types, properties.
       """
       
       def __init__(self):
           self.rules = []
       
       def add_rule(self, rule):
           """
           Add firewall rule.
           
           Rule structure:
           {
               'source_subnet': '192.168.100.0/24',  # BMS workstations
               'dest_subnet': '192.168.200.0/24',    # BACnet devices
               'allowed_services': ['ReadProperty', 'ReadPropertyMultiple'],
               'denied_services': ['WriteProperty', 'DeviceCommunicationControl'],
               'allowed_objects': ['ANALOG_INPUT', 'ANALOG_VALUE', 'BINARY_INPUT'],
               'action': 'ALLOW'
           }
           """
           self.rules.append(rule)
       
       def filter_bacnet_packet(self, packet):
           """
           Inspect BACnet packet and apply rules.
           
           Returns: True (allow), False (block)
           """
           src_ip = packet['source_ip']
           dst_ip = packet['dest_ip']
           service = packet['bacnet_service']
           object_type = packet['object_type']
           
           for rule in self.rules:
               if (self.ip_in_subnet(src_ip, rule['source_subnet']) and
                   self.ip_in_subnet(dst_ip, rule['dest_subnet'])):
                   
                   # Check service whitelist
                   if service in rule.get('denied_services', []):
                       self.log_blocked(packet, rule, "Denied service")
                       return False
                   
                   if service in rule.get('allowed_services', []):
                       return True
           
           # Default deny
           self.log_blocked(packet, None, "No matching rule")
           return False
       
       def ip_in_subnet(self, ip, subnet):
           """Check if IP in subnet (simplified)"""
           # In production: use ipaddress module
           return True  # Placeholder
       
       def log_blocked(self, packet, rule, reason):
           """Log blocked BACnet packets"""
           print(f"BLOCKED: {packet['source_ip']} → {packet['dest_ip']}")
           print(f"  Service: {packet['bacnet_service']}")
           print(f"  Reason: {reason}")
   
   # Example: Configure BACnet firewall
   firewall = BACnetFirewall()
   
   # Rule 1: Operators can read/write
   firewall.add_rule({
       'source_subnet': '192.168.100.0/24',  # BMS workstations
       'dest_subnet': '192.168.200.0/24',    # BACnet devices
       'allowed_services': ['ReadProperty', 'WriteProperty', 'ReadPropertyMultiple'],
       'action': 'ALLOW'
   })
   
   # Rule 2: Block dangerous services from all sources
   firewall.add_rule({
       'source_subnet': '0.0.0.0/0',  # All sources
       'dest_subnet': '192.168.200.0/24',
       'denied_services': [
           'DeviceCommunicationControl',  # Can disable device
           'ReinitializeDevice',          # Can reboot device
           'WriteFile'                    # Firmware upload
       ],
       'action': 'DENY'
   })

**3. BACnet Gateway (Protocol Proxy)**

.. code-block:: python

   class BACnetGateway:
       """
       Secure gateway between untrusted network and BACnet devices.
       Adds authentication and logging to legacy BACnet/IP.
       """
       
       def __init__(self):
           self.authenticated_users = {}
           self.audit_log = []
       
       def authenticate_user(self, username, password):
           """Require authentication before BACnet access"""
           if self.verify_credentials(username, password):
               session_token = self.generate_session_token()
               self.authenticated_users[session_token] = username
               return session_token
           return None
       
       def proxy_bacnet_request(self, session_token, bacnet_request):
           """
           Proxy BACnet request (with authentication + logging).
           
           Flow:
           1. Verify session token
           2. Log request
           3. Forward to BACnet device
           4. Log response
           5. Return to client
           """
           if session_token not in self.authenticated_users:
               print("Unauthenticated request blocked")
               return None
           
           username = self.authenticated_users[session_token]
           
           # Audit log
           self.audit_log.append({
               'timestamp': datetime.utcnow().isoformat(),
               'user': username,
               'service': bacnet_request['service'],
               'target': bacnet_request['device_id'],
               'object': bacnet_request['object_id']
           })
           
           # Forward to BACnet device (legacy BACnet/IP)
           response = self.send_to_bacnet_device(bacnet_request)
           
           return response
       
       def verify_credentials(self, username, password):
           """Verify against LDAP/AD"""
           # In production: LDAP authentication
           return True  # Placeholder
       
       def generate_session_token(self):
           """Generate secure session token"""
           import secrets
           return secrets.token_hex(32)
       
       def send_to_bacnet_device(self, request):
           """Send BACnet request to device"""
           # In production: construct BACnet APDU, send UDP
           return {'status': 'OK'}

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why is legacy BACnet/IP insecure, and how does BACnet/SC address this?**

**A1:**

**Legacy BACnet/IP Vulnerabilities:**

```
1. No Authentication
   ├─ Anyone on network can send commands
   └─ Example: Change thermostat setpoint without credentials

2. No Encryption
   ├─ Commands sent in plaintext (UDP port 47808)
   └─ Example: Wireshark captures reveal building configuration

3. No Integrity Protection
   ├─ Commands can be modified in transit (MITM)
   └─ Example: Attacker changes setpoint value mid-flight

4. Broadcast Discovery
   ├─ Who-Is broadcasts reveal all devices
   └─ Example: Attacker enumerates network, identifies targets

5. UDP-Based
   ├─ Source IP spoofing
   └─ Example: DDoS amplification attacks
```

**BACnet/SC Solution:**

```
Security Feature          | Addresses Vulnerability
─────────────────────────┼────────────────────────────
TLS 1.3 encryption       | No encryption (plaintext)
X.509 certificates       | No authentication
TLS MAC                  | No integrity protection
Hub access control (ACL) | Unauthorized access
WebSocket (TCP)          | UDP vulnerabilities
```

**Migration Path:**
```
Phase 1: Network segmentation (isolate legacy BACnet)
Phase 2: Deploy BACnet/SC Hub
Phase 3: Replace devices with BACnet/SC nodes (over time)
Phase 4: Decommission legacy BACnet/IP
```

---

**Q2: Design a secure BACnet network for a 50-story office building.**

**A2:**

**Building Profile:**
- 50 floors, 2,000 occupants
- Systems: HVAC, lighting, elevators, fire alarms, access control
- 500+ BACnet devices

**Network Architecture:**

```
Level 1: Corporate IT Network (VLAN 10)
├─ Separated from BMS (firewall)
└─ No direct BACnet access

Level 2: BMS Management (VLAN 100)
├─ BACnet/SC Hub (central security gateway)
├─ Operator workstations (Windows, BMS software)
├─ BACnet gateway (legacy device support)
└─ SIEM integration (security monitoring)

Level 3: BACnet Backbone (VLAN 200)
├─ BACnet/SC nodes (modern controllers)
├─ BACnet/IP devices (legacy, isolated)
└─ Segmentation by system:
   ├─ HVAC subnet (192.168.201.0/24)
   ├─ Lighting subnet (192.168.202.0/24)
   ├─ Access control subnet (192.168.203.0/24) — HIGH SECURITY
   └─ Fire alarm subnet (192.168.204.0/24) — CRITICAL

Level 4: Field Devices (VLAN 300)
├─ BACnet/MSTP (RS-485) networks
├─ Connected via BACnet routers
└─ Read-only access from upper levels
```

**Security Controls:**

```
1. BACnet/SC for Critical Systems
   ├─ Access control panels (security-sensitive)
   ├─ Fire alarm system (life safety)
   └─ Central plant (chillers, boilers)

2. Legacy BACnet/IP (Retrofit)
   ├─ BACnet firewall (limit WriteProperty)
   ├─ VLAN isolation (no internet access)
   └─ Gateway with authentication

3. Access Control
   ├─ Operators: Full access (read/write all systems)
   ├─ Facility staff: Read-only (view status, alarms)
   ├─ Tenants: No BACnet access (web portal only)
   └─ Vendors: Temporary VPN, restricted to specific devices

4. Monitoring
   ├─ IDS for BACnet network (detect anomalies)
   ├─ SIEM integration (correlate with IT security events)
   └─ Audit logging (all WriteProperty commands)
```

**Threat Mitigation:**

```
Threat                    | Mitigation
─────────────────────────┼────────────────────────────────────
Ransomware from IT       | Firewall between IT and BMS VLANs
Unauthorized HVAC control| BACnet/SC ACLs, operator auth
Insider threat           | Audit logging, least privilege
Physical access          | Locked equipment rooms, badge readers
Legacy device exploits   | Network segmentation, firmware updates
```

---

**Q3: What BACnet services should be restricted to prevent malicious control?**

**A3:**

**High-Risk BACnet Services (Should Restrict):**

| Service | Risk | Mitigation |
|:--------|:-----|:-----------|
| **WriteProperty** | Modify device parameters (setpoints, schedules) | ACL: Operators only, log all writes |
| **WritePropertyMultiple** | Batch modification (multiple objects) | Same as WriteProperty |
| **DeviceCommunicationControl** | Disable device communication | Block via firewall |
| **ReinitializeDevice** | Reboot device, factory reset | Block or require 2FA |
| **WriteFile** | Upload firmware, configuration files | Block (use secure update process) |
| **CreateObject** | Create new BACnet objects | Restrict to commissioning phase |
| **DeleteObject** | Delete BACnet objects | Restrict to administrators |

**Medium-Risk Services (Monitor):**

| Service | Risk | Mitigation |
|:--------|:-----|:-----------|
| **ReadProperty** | Information disclosure (building layout) | Rate limit, log extensive queries |
| **ReadPropertyMultiple** | Bulk data exfiltration | Monitor for excessive reads |
| **SubscribeCOV** | Subscribe to Change-of-Value notifications | Limit subscriptions per client |
| **ConfirmedCOVNotification** | Alarm spoofing | Verify source, BACnet/SC auth |

**Firewall Rule Example:**

```python
ALLOWED_SERVICES = {
    'Operator': ['ReadProperty', 'WriteProperty', 'ReadPropertyMultiple', 
                 'WritePropertyMultiple', 'SubscribeCOV'],
    'Engineer': ['ReadProperty', 'ReadPropertyMultiple', 'WriteProperty',
                 'ReinitializeDevice'],  # Limited write access
    'Viewer': ['ReadProperty', 'ReadPropertyMultiple'],  # Read-only
    'Guest': []  # No access
}

GLOBALLY_BLOCKED = [
    'DeviceCommunicationControl',  # Can disable entire device
    'WriteFile',                   # Firmware upload risk
    'DeleteObject'                 # Can corrupt configuration
]
```

---

**Q4: How does BACnet/SC integrate with IEC 62443 zones and conduits?**

**A4:**

**IEC 62443 Alignment:**

BACnet/SC Hub acts as a **conduit security gateway** between zones.

**Example: Manufacturing Facility with BMS**

```
Zone 1: Corporate IT (IEC 62443 Level 5)
├─ SL-T: 1
└─ BACnet: No direct access

Conduit 1-2: Firewall + BACnet/SC Hub
├─ TLS 1.3 encryption
├─ Certificate-based authentication
└─ ACL enforcement

Zone 2: Building Management (IEC 62443 Level 3.5)
├─ SL-T: 2
├─ BACnet/SC Hub (security gateway)
└─ Operator workstations

Conduit 2-3: BACnet/SC Encrypted Tunnel
├─ Only authenticated nodes
└─ Separate VLANs per system

Zone 3: HVAC Control (IEC 62443 Level 2)
├─ SL-T: 2
├─ BACnet/SC nodes (modern)
└─ BACnet/IP devices (legacy, isolated)

Conduit 3-4: BACnet Router (read-only)
├─ Field devices cannot initiate connections
└─ Supervisory control only

Zone 4: Field Devices (IEC 62443 Level 1)
├─ SL-T: 1
├─ BACnet/MSTP (RS-485)
└─ Temperature sensors, damper actuators
```

**Security Level Mapping:**

```
BACnet/SC Security      | IEC 62443 Requirement     | Implementation
───────────────────────┼───────────────────────────┼────────────────────
TLS 1.3                | FR 4 (Confidentiality)    | Encrypted conduit
X.509 certificates     | FR 1 (Authentication)     | Node identity
Hub ACLs               | FR 2 (Authorization)      | Access control
Audit logging          | FR 6 (Event response)     | SIEM integration
```

**Result:** BACnet/SC provides **SL 2-3** capabilities for building automation in IEC 62443 framework.

---

**Q5: A building owner wants to remotely access BACnet HVAC from home. How to secure this?**

**A5:**

**Risk:** Direct internet access to BACnet = high vulnerability.

**Secure Remote Access Architecture:**

```
1. VPN-Based Access (Most Secure)

   Home PC → VPN Client
      ↓
   Corporate Firewall → VPN Gateway (MFA required)
      ↓
   BMS VLAN → BACnet/SC Hub
      ↓
   HVAC Controllers (BACnet/SC nodes)

Security:
├─ Multi-factor authentication (TOTP)
├─ VPN tunnel (IPsec or WireGuard)
├─ Role-based access (read-only for home access)
└─ Session timeout (4 hours max)
```

**2. Web Portal (Convenience vs. Security)**

```
Home Browser → HTTPS (TLS 1.3)
   ↓
Cloud-based BMS Gateway (Vendor-hosted)
   ↓
On-premise BACnet Gateway → BACnet/SC Hub
   ↓
HVAC Controllers

Security:
├─ OAuth 2.0 authentication (not direct BACnet access)
├─ API rate limiting (10 requests/minute)
├─ Read-only by default (write requires elevated privileges)
├─ Audit logging (all actions logged)
└─ No direct BACnet/IP exposure
```

**3. Jump Server (Enterprise)**

```
Home PC → SSH/RDP to Jump Server (MFA)
   ↓
Jump Server (BMS VLAN) → BACnet tools installed
   ↓
BACnet network (local access)

Security:
├─ Jump server hardened (CIS benchmarks)
├─ All sessions recorded (compliance)
├─ Time-based access (revoked after maintenance window)
└─ Anomaly detection (unusual commands flagged)
```

**Best Practice Recommendation:**

```
For Building Owner:
├─ Use vendor web portal (limited functionality)
├─ Read-only access (view temperatures, alarms)
├─ No direct WriteProperty capability from home
└─ Critical changes require on-site access or VPN + approval

For Facility Manager:
├─ VPN access with MFA
├─ Full BACnet access (read/write)
├─ Session logging and monitoring
└─ Automatic logout after 30 minutes idle
```

**Red Flags to Avoid:**
❌ Port forwarding BACnet/IP (port 47808) to internet  
❌ Default credentials on BMS software  
❌ No VPN (direct access to BACnet VLAN)  
❌ Unencrypted remote desktop (RDP without TLS)

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~750
