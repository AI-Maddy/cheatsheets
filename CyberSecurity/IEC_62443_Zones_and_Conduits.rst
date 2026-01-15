🗺️ **IEC 62443 — ZONES & CONDUITS ARCHITECTURE**
═══════════════════════════════════════════════════════════════════════

**Network Segmentation for Industrial Systems (IEC 62443-3-2)**  
**Purpose:** Defense-in-depth 🛡️ | Network isolation 🔒 | Attack surface reduction 📉  
**Scope:** Zone design, conduit security, Purdue Model alignment

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Zones:** Logical groups of assets with similar security requirements  
**Conduits:** Communication channels between zones (secured with firewalls, encryption)

**Goal:** Limit blast radius of compromise — attacker in Zone 1 cannot easily reach Zone 3.

**Best Practice:** Purdue Model (6 levels) + defense-in-depth.

════════════════════════════════════════════════════════════════════════════

📐 **ZONE DEFINITION (IEC 62443-3-2 Section 3.1)**
─────────────────────────────────────────────────────────────────────────

**What is a Zone?**

A **zone** is a grouping of logical or physical assets that share:
1. **Common security requirements** (same SL-T)
2. **Common consequence of compromise** (similar risk)
3. **Common access control policy** (same trust level)

**Zone Design Principles:**

.. code-block:: python

   class IndustrialZone:
       """IEC 62443-3-2 Zone definition"""
       
       def __init__(self, zone_id, name, sl_t, purdue_level):
           self.zone_id = zone_id
           self.name = name
           self.sl_t = sl_t  # Target Security Level
           self.purdue_level = purdue_level  # ISA-95 level (0-5)
           self.assets = []
           self.conduits = []  # Connections to other zones
       
       def add_asset(self, asset):
           """Add asset to zone (must match SL-T)"""
           if asset.security_level != self.sl_t:
               raise ValueError(f"Asset SL {asset.security_level} != Zone SL-T {self.sl_t}")
           self.assets.append(asset)
       
       def add_conduit(self, conduit):
           """Add conduit connecting to another zone"""
           self.conduits.append(conduit)
       
       def get_zone_summary(self):
           return {
               'zone_id': self.zone_id,
               'name': self.name,
               'sl_t': self.sl_t,
               'purdue_level': self.purdue_level,
               'asset_count': len(self.assets),
               'conduit_count': len(self.conduits)
           }

**Zone Hierarchy (Common Patterns):**

.. code-block:: text

   Corporate Network (IT Domain)
   ├─ Level 5: Enterprise Resource Planning (ERP)
   │  ├─ Zone: Corporate IT
   │  └─ SL-T: SL 1 (standard IT security)
   │
   ├─ Level 4: Business Planning & Logistics
   │  ├─ Zone: Plant Management
   │  └─ SL-T: SL 2
   │
   DMZ (OT/IT Boundary)
   ├─ Level 3.5: Demilitarized Zone
   │  ├─ Zone: Data Historian, HMI Servers
   │  └─ SL-T: SL 2-3
   │
   Operations Network (OT Domain)
   ├─ Level 3: Operations Management
   │  ├─ Zone: SCADA, MES, Engineering Workstations
   │  └─ SL-T: SL 2-3
   │
   ├─ Level 2: Supervisory Control
   │  ├─ Zone: DCS, PLCs, Local HMI
   │  └─ SL-T: SL 3
   │
   ├─ Level 1: Basic Control
   │  ├─ Zone: Intelligent Field Devices (smart sensors)
   │  └─ SL-T: SL 2
   │
   └─ Level 0: Physical Process
      ├─ Zone: Simple sensors/actuators
      └─ SL-T: SL 1

════════════════════════════════════════════════════════════════════════════

🏭 **PURDUE MODEL INTEGRATION (ISA-95)**
─────────────────────────────────────────────────────────────────────────

**Purdue Reference Model for Industrial Control Systems:**

| Level | Name | Function | Example Assets | Typical SL-T |
|:------|:-----|:---------|:---------------|:-------------|
| **5** | Enterprise | Corporate IT, ERP, email | Office PCs, file servers | SL 1 |
| **4** | Business Planning | Plant scheduling, inventory | MES, warehouse mgmt | SL 1-2 |
| **3.5** | DMZ | Data aggregation, remote access | Historians, HMI servers | SL 2-3 |
| **3** | Operations | SCADA supervision, HMI | SCADA servers, engineering workstations | SL 2-3 |
| **2** | Control | Process control logic | PLCs, DCS, PACs | SL 3 |
| **1** | Basic Control | Intelligent devices | Smart sensors, VFDs | SL 2 |
| **0** | Process | Physical equipment | Pumps, valves, motors | SL 1 |

**Purdue Model Security Boundaries:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────────┐
   │ Level 5 (Enterprise)                                         │
   │ ├─ Security: Traditional IT (antivirus, email filtering)    │
   │ └─ Protocols: HTTP, SMTP, SMB                               │
   └────────────────┬─────────────────────────────────────────────┘
                    │ Firewall #1 (IT/DMZ boundary)
   ┌────────────────▼─────────────────────────────────────────────┐
   │ Level 3.5 (DMZ) — CRITICAL SECURITY BOUNDARY               │
   │ ├─ Unidirectional gateway (OT → IT data flow only)         │
   │ ├─ Data diodes (physical isolation)                         │
   │ ├─ Jump servers (restricted admin access)                   │
   │ └─ Protocols: OPC UA, MQTT, database replication           │
   └────────────────┬─────────────────────────────────────────────┘
                    │ Firewall #2 (DMZ/OT boundary)
   ┌────────────────▼─────────────────────────────────────────────┐
   │ Levels 0-3 (OT Domain) — HIGHLY RESTRICTED                 │
   │ ├─ No direct internet access                                │
   │ ├─ No email, web browsing                                   │
   │ ├─ Industrial protocols only (Modbus, PROFINET, OPC UA)    │
   │ └─ Strict change management (all modifications audited)    │
   └──────────────────────────────────────────────────────────────┘

**Python: Purdue Model Zone Generator**

.. code-block:: python

   class PurdueModelArchitecture:
       """Generate IEC 62443 zones aligned with Purdue Model"""
       
       PURDUE_LEVELS = {
           5: {'name': 'Enterprise', 'default_sl_t': 1},
           4: {'name': 'Business Planning', 'default_sl_t': 2},
           3.5: {'name': 'DMZ', 'default_sl_t': 2},
           3: {'name': 'Operations', 'default_sl_t': 3},
           2: {'name': 'Control', 'default_sl_t': 3},
           1: {'name': 'Basic Control', 'default_sl_t': 2},
           0: {'name': 'Process', 'default_sl_t': 1}
       }
       
       def __init__(self, plant_name):
           self.plant_name = plant_name
           self.zones = []
       
       def create_zone_for_level(self, purdue_level, custom_sl_t=None):
           """Create zone based on Purdue level"""
           level_info = self.PURDUE_LEVELS[purdue_level]
           
           zone = IndustrialZone(
               zone_id=f"Zone-L{purdue_level}",
               name=f"{level_info['name']} - {self.plant_name}",
               sl_t=custom_sl_t or level_info['default_sl_t'],
               purdue_level=purdue_level
           )
           
           self.zones.append(zone)
           return zone
       
       def generate_full_architecture(self):
           """Generate complete 7-level Purdue architecture"""
           for level in [5, 4, 3.5, 3, 2, 1, 0]:
               self.create_zone_for_level(level)
           
           # Create conduits between adjacent levels
           for i in range(len(self.zones) - 1):
               upper_zone = self.zones[i]
               lower_zone = self.zones[i + 1]
               
               conduit = Conduit(
                   conduit_id=f"C{i}",
                   source_zone=upper_zone,
                   dest_zone=lower_zone,
                   security_level=max(upper_zone.sl_t, lower_zone.sl_t)
               )
               
               upper_zone.add_conduit(conduit)
               lower_zone.add_conduit(conduit)
   
   # Example: Oil refinery
   refinery = PurdueModelArchitecture("Oil Refinery #3")
   refinery.generate_full_architecture()
   
   # Override default SL-T for critical control zone
   control_zone = refinery.zones[4]  # Level 2 (Control)
   control_zone.sl_t = 4  # Critical safety-related (turbine, pressure control)

════════════════════════════════════════════════════════════════════════════

🔗 **CONDUIT DEFINITION (IEC 62443-3-2 Section 3.2)**
─────────────────────────────────────────────────────────────────────────

**What is a Conduit?**

A **conduit** is a logical grouping of communication channels connecting two or more zones.

**Conduit Security Requirements:**

.. code-block:: python

   class Conduit:
       """IEC 62443-3-2 Conduit with security controls"""
       
       def __init__(self, conduit_id, source_zone, dest_zone, security_level):
           self.conduit_id = conduit_id
           self.source_zone = source_zone
           self.dest_zone = dest_zone
           self.security_level = security_level  # Max of connected zones
           self.security_controls = []
       
       def add_security_control(self, control_type, config):
           """Add security control to conduit"""
           self.security_controls.append({
               'type': control_type,
               'config': config
           })
       
       def validate_conduit_security(self):
           """Verify conduit meets SL requirements"""
           required_controls = self.get_required_controls(self.security_level)
           
           for required in required_controls:
               if not self.has_control(required):
                   raise SecurityError(f"Conduit {self.conduit_id} missing {required}")
           
           return True
       
       def get_required_controls(self, sl):
           """IEC 62443-3-3 conduit security requirements"""
           controls = ['firewall']  # SL 1+
           
           if sl >= 2:
               controls.extend(['encryption', 'authentication'])
           
           if sl >= 3:
               controls.extend(['ids_ips', 'network_segmentation'])
           
           if sl >= 4:
               controls.extend(['data_diode', 'deep_packet_inspection'])
           
           return controls
       
       def has_control(self, control_type):
           """Check if control is implemented"""
           return any(c['type'] == control_type for c in self.security_controls)

**Conduit Security Controls by SL:**

| SL | Required Controls | Implementation Examples |
|:---|:------------------|:------------------------|
| **SL 1** | Basic firewall | Stateful packet filtering, port-based ACLs |
| **SL 2** | + Encryption, Authentication | TLS 1.2+, certificate-based auth, RADIUS |
| **SL 3** | + IDS/IPS, Network segmentation | Industrial protocol inspection, VLANs, anomaly detection |
| **SL 4** | + Data diode, Deep packet inspection | Unidirectional gateway, hardware-enforced isolation, behavioral analysis |

**Common Conduit Types:**

.. code-block:: python

   class ConduitFactory:
       """Create common conduit configurations"""
       
       @staticmethod
       def create_dmz_conduit(it_zone, dmz_zone):
           """IT to DMZ conduit (unidirectional)"""
           conduit = Conduit("C_IT_DMZ", it_zone, dmz_zone, security_level=3)
           
           # Unidirectional gateway (OT → IT only)
           conduit.add_security_control('unidirectional_gateway', {
               'direction': 'OT_TO_IT',
               'protocols': ['OPC UA', 'Database replication']
           })
           
           # Firewall
           conduit.add_security_control('firewall', {
               'type': 'industrial_firewall',
               'rules': [
                   {'src': 'DMZ', 'dst': 'IT', 'port': 443, 'action': 'ALLOW'},
                   {'src': 'IT', 'dst': 'DMZ', 'port': 'ANY', 'action': 'DENY'}
               ]
           })
           
           # IDS for anomaly detection
           conduit.add_security_control('ids_ips', {
               'mode': 'passive',
               'protocols': ['OPC UA', 'Modbus TCP']
           })
           
           return conduit
       
       @staticmethod
       def create_control_conduit(scada_zone, plc_zone):
           """SCADA to PLC conduit"""
           conduit = Conduit("C_SCADA_PLC", scada_zone, plc_zone, security_level=3)
           
           # Managed industrial switch with VLAN
           conduit.add_security_control('network_segmentation', {
               'type': 'VLAN',
               'vlan_id': 100,
               'port_security': True
           })
           
           # TLS encryption for OPC UA
           conduit.add_security_control('encryption', {
               'protocol': 'TLS 1.3',
               'cipher_suite': 'TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384'
           })
           
           # Protocol firewall (only allow Modbus, OPC UA)
           conduit.add_security_control('firewall', {
               'type': 'protocol_firewall',
               'allowed_protocols': ['Modbus TCP', 'OPC UA'],
               'default_action': 'DROP'
           })
           
           return conduit

════════════════════════════════════════════════════════════════════════════

🛡️ **DEFENSE-IN-DEPTH ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**Layered Security Strategy:**

.. code-block:: text

   Layer 1: Perimeter Security (Zone Boundary)
   ├─ Firewall (stateful inspection)
   ├─ VPN gateway (remote access)
   └─ DMZ (external-facing services)
   
   Layer 2: Network Security (Conduit)
   ├─ Network segmentation (VLANs)
   ├─ Managed switches (port security)
   ├─ IDS/IPS (industrial protocol inspection)
   └─ Unidirectional gateways (critical zones)
   
   Layer 3: Host Security (Asset)
   ├─ Application whitelisting
   ├─ Host-based firewall
   ├─ Endpoint detection & response (EDR)
   └─ Secure boot
   
   Layer 4: Application Security
   ├─ Authentication & authorization
   ├─ Input validation
   ├─ Secure coding practices
   └─ Code signing
   
   Layer 5: Data Security
   ├─ Encryption at rest
   ├─ Encryption in transit
   ├─ Database access controls
   └─ Data loss prevention (DLP)

**Real-World Example: Water Treatment Plant**

.. code-block:: python

   class WaterTreatmentPlantArchitecture:
       """IEC 62443 zone/conduit design for water utility"""
       
       def __init__(self):
           self.zones = self.create_zones()
           self.conduits = self.create_conduits()
       
       def create_zones(self):
           """Define zones based on water treatment processes"""
           zones = [
               IndustrialZone(
                   zone_id="Z1",
                   name="Corporate IT",
                   sl_t=1,
                   purdue_level=5
               ),
               IndustrialZone(
                   zone_id="Z2",
                   name="DMZ (SCADA Servers, Historians)",
                   sl_t=2,
                   purdue_level=3.5
               ),
               IndustrialZone(
                   zone_id="Z3",
                   name="Operations (HMI, Engineering)",
                   sl_t=3,
                   purdue_level=3
               ),
               IndustrialZone(
                   zone_id="Z4",
                   name="Chemical Treatment Control (Critical)",
                   sl_t=4,  # SL 4: Public health impact
                   purdue_level=2
               ),
               IndustrialZone(
                   zone_id="Z5",
                   name="Filtration Control",
                   sl_t=3,
                   purdue_level=2
               ),
               IndustrialZone(
                   zone_id="Z6",
                   name="Distribution Monitoring",
                   sl_t=2,
                   purdue_level=1
               )
           ]
           
           return zones
       
       def create_conduits(self):
           """Define secured conduits between zones"""
           conduits = []
           
           # C1: Corporate IT → DMZ (read-only reports)
           c1 = Conduit("C1", self.zones[0], self.zones[1], security_level=2)
           c1.add_security_control('unidirectional_gateway', {
               'direction': 'DMZ_TO_IT'
           })
           c1.add_security_control('firewall', {'type': 'stateful'})
           conduits.append(c1)
           
           # C2: DMZ → Operations (HMI access)
           c2 = Conduit("C2", self.zones[1], self.zones[2], security_level=3)
           c2.add_security_control('firewall', {'type': 'industrial'})
           c2.add_security_control('ids_ips', {'protocols': ['OPC UA']})
           c2.add_security_control('encryption', {'protocol': 'TLS 1.3'})
           conduits.append(c2)
           
           # C3: Operations → Chemical Control (CRITICAL)
           c3 = Conduit("C3", self.zones[2], self.zones[3], security_level=4)
           c3.add_security_control('data_diode', {
               'direction': 'ONE_WAY',
               'technology': 'hardware_enforced'
           })
           c3.add_security_control('deep_packet_inspection', {
               'protocols': ['Modbus TCP'],
               'command_whitelist': ['READ_COILS', 'READ_HOLDING_REGISTERS']
           })
           conduits.append(c3)
           
           return conduits
       
       def generate_security_report(self):
           """Generate IEC 62443-3-2 compliance report"""
           report = "Water Treatment Plant - Zone & Conduit Security Report\n"
           report += "=" * 80 + "\n\n"
           
           report += "ZONES:\n"
           for zone in self.zones:
               report += f"  {zone.zone_id}: {zone.name} (SL-T: {zone.sl_t}, Purdue L{zone.purdue_level})\n"
           
           report += "\nCONDUITS:\n"
           for conduit in self.conduits:
               report += f"  {conduit.conduit_id}: {conduit.source_zone.name} → {conduit.dest_zone.name}\n"
               report += f"    Security Level: {conduit.security_level}\n"
               report += f"    Controls: {[c['type'] for c in conduit.security_controls]}\n\n"
           
           return report
   
   # Deploy architecture
   plant = WaterTreatmentPlantArchitecture()
   print(plant.generate_security_report())

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why is Level 3.5 (DMZ) critical in the Purdue Model?**

**A1:**

**Level 3.5 is the OT/IT boundary** — the most critical security perimeter.

**Purpose:**
1. **Data Aggregation:** Collect OT data (sensor readings, alarms) for IT systems (ERP, business intelligence)
2. **Unidirectional Flow:** IT can read OT data, but cannot write to OT (prevents ransomware spread)
3. **Attack Surface Reduction:** External connections terminate at DMZ, not in OT network

**Without DMZ:**
```
Corporate IT ←──→ SCADA/PLCs (DIRECT CONNECTION)
└─ Risk: Ransomware on office PC spreads to PLC network
```

**With DMZ:**
```
Corporate IT ←──→ DMZ (Historians) ──→ SCADA/PLCs
                    ↑                     ↑
              Unidirectional         Firewall
              gateway                  + IDS
```

**Result:** Attacker compromising IT network cannot send commands to PLCs.

**Real Attack:** 2017 NotPetya ransomware spread through corporate networks to OT systems at Maersk, causing $300M+ damage. Proper DMZ would have contained it.

---

**Q2: What is a unidirectional gateway (data diode) and when is it required?**

**A2:**

**Unidirectional Gateway (Data Diode):**
- **Hardware-enforced** one-way data flow
- Physically impossible to send data in reverse direction (optical transmitter only, no receiver)
- Used for **SL 3-4** critical zones

**How it works:**
```
OT Network (PLCs)  →  [Optical Transmitter]  →  [Optical Receiver]  →  IT Network
                      └─ No return path (hardware limitation)
```

**Use Cases:**
1. **Critical infrastructure:** Power plants, water treatment (prevent remote attacks on control systems)
2. **Safety systems:** Nuclear reactors, chemical plants (IEC 61511 SIL 3-4)
3. **Sensitive data exfiltration:** Export OT telemetry to IT, but IT cannot send commands back

**When Required:**
- SL-T = 4 (nation-state threat level)
- Safety-critical systems (SIL 3-4)
- Regulatory requirement (e.g., nuclear NRC)

**Alternative (Bidirectional):** Application-level firewall with deep packet inspection (weaker than data diode).

---

**Q3: How do you handle legacy equipment that cannot be zoned?**

**A3:**

**Challenge:** Old PLCs, RTUs, sensors lack modern network security features.

**Strategies:**

**1. Micro-Segmentation**
```
Put each legacy device in its own VLAN:
├─ VLAN 100: Legacy PLC #1 (SL-C = 0)
├─ VLAN 101: Legacy PLC #2 (SL-C = 0)
└─ VLAN 102: Modern HMI (SL-C = 2)

Firewall rules:
- HMI can read from VLANs 100-101
- VLANs 100-101 cannot communicate with each other
```

**2. Protocol Gateway**
```
Legacy PLC (no auth) ←──[Serial]──→ Protocol Gateway ←──[TLS]──→ SCADA
                                    └─ Adds encryption, authentication
```

**3. Network-Level Protection**
```
Legacy Zone (multiple old PLCs):
├─ Industrial firewall (protocol whitelist)
├─ IDS (anomaly detection for Modbus, DNP3)
├─ Jump server (all admin access logged)
└─ No direct internet connectivity
```

**4. Out-of-Band Monitoring**
```
Passive tap on network link:
├─ Monitor-only (no writes)
├─ Detect anomalous traffic patterns
└─ Alert SOC without disrupting OT
```

**5. Compensating Controls**
- Physical security (locked enclosures, badge access)
- 2-person rule for configuration changes
- Change management process (all modifications approved)

**Real Example:** 2010 Stuxnet targeted legacy Siemens PLCs (no security). Modern approach: Isolate via VLAN + industrial firewall + IDS.

---

**Q4: Design a 5-zone architecture for an automotive manufacturing plant.**

**A4:**

**Plant:** Car assembly line with body welding, painting, final assembly.

**Zone Architecture:**

```
Zone 1: Corporate IT (SL-T = 1)
├─ Assets: Office PCs, ERP, email
├─ Purdue Level: 5
└─ Protocols: HTTP, SMTP

Zone 2: DMZ (SL-T = 2)
├─ Assets: MES servers, data historians, engineering workstations
├─ Purdue Level: 3.5
└─ Protocols: OPC UA, database replication

Zone 3: SCADA Supervision (SL-T = 2)
├─ Assets: SCADA servers, HMI clients
├─ Purdue Level: 3
└─ Protocols: OPC UA, Modbus TCP

Zone 4: Welding Robots (SL-T = 3)
├─ Assets: Robot controllers (ABB, KUKA), vision systems
├─ Purdue Level: 2
├─ Reason for SL 3: Safety-critical (robot collision → worker injury)
└─ Protocols: PROFINET, EtherNet/IP

Zone 5: Paint Booth (SL-T = 2)
├─ Assets: Spray gun controllers, ventilation PLCs
├─ Purdue Level: 2
├─ Reason for SL 2: Quality impact (bad paint job), no safety risk
└─ Protocols: Modbus TCP, PROFINET
```

**Conduits:**

| Conduit | Source → Dest | Security Controls |
|:--------|:--------------|:------------------|
| **C1** | IT → DMZ | Firewall (allow HTTPS), unidirectional (DMZ→IT data export) |
| **C2** | DMZ → SCADA | Firewall, TLS encryption, IDS (OPC UA inspection) |
| **C3** | SCADA → Welding | Managed switch (VLAN 100), protocol firewall (PROFINET only), IDS |
| **C4** | SCADA → Paint | Managed switch (VLAN 200), firewall (Modbus TCP whitelist) |

**Key Design Decisions:**
- **Welding Zone (SL 3)** higher than Paint (SL 2) due to safety risk
- **Separate zones** for welding/paint (different processes, different risk)
- **DMZ** aggregates data from both OT zones before sending to IT
- **No direct connection** between welding and paint zones (air-gapped)

---

**Q5: Explain the difference between a firewall and an industrial protocol firewall.**

**A5:**

**Standard IT Firewall:**
- **Layer 3-4** (IP, TCP/UDP)
- Rules based on: Source IP, Destination IP, Port, Protocol
- **Example:** "Allow 192.168.1.100:12345 → 10.0.0.50:502 (Modbus TCP)"

**Industrial Protocol Firewall (Deep Packet Inspection):**
- **Layer 7** (Application layer)
- Inspects **industrial protocol commands** (Modbus, OPC UA, DNP3, PROFINET)
- **Example rules:**
  - Allow Modbus **READ** function codes (1, 2, 3, 4)
  - Block Modbus **WRITE** function codes (5, 6, 15, 16)
  - Allow OPC UA **read** operations
  - Block OPC UA **write** to safety-critical nodes

**Comparison:**

| Feature | IT Firewall | Industrial Firewall |
|:--------|:------------|:--------------------|
| **OSI Layer** | Layer 3-4 (IP, TCP) | Layer 7 (Application) |
| **Protocols** | Generic (TCP/UDP) | Industrial-specific (Modbus, OPC UA, DNP3) |
| **Granularity** | Port-based | Command-level (read vs. write) |
| **Performance** | High throughput | Moderate (DPI overhead) |
| **Example** | Cisco ASA, pfSense | Tofino Xenon, Claroty, Nozomi |

**Example Scenario:**

**Attack:** Attacker on HMI network sends Modbus WRITE command to PLC to change setpoint.

**IT Firewall:**
```
Rule: Allow HMI (192.168.10.5) → PLC (192.168.20.10):502
Result: ✅ Allowed (port 502 is Modbus, rule permits)
Attack: ❌ NOT BLOCKED
```

**Industrial Firewall:**
```
Rule: Allow HMI → PLC port 502 (Modbus)
      └─ Sub-rule: Allow function codes 1-4 (READ only)
      └─ Sub-rule: Block function codes 5, 6, 15, 16 (WRITE)

Attack uses function code 6 (Write Single Register):
Result: ❌ Blocked (write command not allowed)
Attack: ✅ BLOCKED
```

**Recommendation:** Use **both** (defense-in-depth):
1. IT firewall for zone boundary (perimeter)
2. Industrial firewall for conduit between SCADA and PLC zones (granular control)

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~800
