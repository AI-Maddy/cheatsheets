====================================================================
Purdue Model for Industrial Network Security (ISA-95 / IEC 62443)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISA-95, IEC 62443, NIST SP 800-82

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**Purdue Reference Model Essentials:**

+------------+------------------------+----------------------------------+------------------+
| Level      | Name                   | Function                         | Security Focus   |
+============+========================+==================================+==================+
| **Level 5**| Enterprise Network     | ERP, business planning           | IT security      |
+------------+------------------------+----------------------------------+------------------+
| **Level 4**| Site Business Planning | MES, scheduling, logistics       | IT/OT DMZ        |
+------------+------------------------+----------------------------------+------------------+
| **Level 3**| Site Operations        | HMI, SCADA, historian            | OT security      |
+------------+------------------------+----------------------------------+------------------+
| **Level 2**| Area Supervisory       | Supervisory control, PLC/RTU     | Critical control |
+------------+------------------------+----------------------------------+------------------+
| **Level 1**| Basic Control          | PLC, DCS, local controllers      | Real-time control|
+------------+------------------------+----------------------------------+------------------+
| **Level 0**| Physical Process       | Sensors, actuators, field devices| Physical layer   |
+------------+------------------------+----------------------------------+------------------+

**Critical Security Zones:**

.. code-block:: text

    🌐 ENTERPRISE ZONE (Level 5)
         │  
         │ [Firewall + IDS/IPS]
         ↓
    🏭 MANUFACTURING ZONE (Level 4)
         │ DMZ with:
         │ - Data diodes (unidirectional)
         │ - Secure file transfer
         │ - No direct internet access
         ↓
    ⚙️  CELL/AREA ZONE (Levels 2-3)
         │ Industrial firewall
         │ Deep packet inspection
         ↓
    🤖 PROCESS ZONE (Levels 0-1)
         │ Physically isolated
         │ Air-gapped if critical

**Key Principles:**

- ✅ **Defense-in-Depth**: Multiple security layers at zone boundaries
- ✅ **Least Privilege**: Minimal access required for function
- ✅ **Network Segmentation**: Isolate zones with conduits (secured connections)
- ✅ **Unidirectional Flow**: Data diodes for Level 3→4 when appropriate
- ✅ **Monitoring**: Continuous visibility at all boundaries

Introduction to the Purdue Model
==================================

The **Purdue Enterprise Reference Architecture (PERA)**, also known as the
**Purdue Reference Model**, is a hierarchical framework for organizing
industrial control systems (ICS) and manufacturing operations. Originally
developed by Theodore Williams at Purdue University in the 1990s, it has
become the de facto standard for ICS network architecture.

The model is codified in:

- **ISA-95** (IEC 62264): Enterprise-Control System Integration
- **ISA-99** (IEC 62443): Security for Industrial Automation and Control Systems
- **NIST SP 800-82**: Guide to Industrial Control Systems (ICS) Security

Purpose of the Purdue Model
----------------------------

1. **Standardized Architecture**: Common language for IT and OT professionals
2. **Security Segmentation**: Clear boundaries for defense-in-depth
3. **Functional Separation**: Isolate real-time control from business systems
4. **Risk Management**: Identify and protect critical assets
5. **Regulatory Compliance**: Framework for IEC 62443, NERC CIP, and other standards

The Six Levels of the Purdue Model
===================================

Level 0: Physical Process
--------------------------

**Description:**
The actual physical equipment and processes being controlled. Includes sensors,
actuators, motors, valves, pumps, and other field devices.

**Components:**

- Temperature sensors, pressure transmitters
- Control valves, variable frequency drives (VFDs)
- Limit switches, proximity sensors
- Pneumatic actuators, electric motors

**Communication:**

- 4-20mA analog signals
- Digital I/O (24V DC)
- HART protocol (analog + digital)
- Fieldbus protocols (Foundation Fieldbus, PROFIBUS PA)

**Security Considerations:**

- **Physical security**: Prevent unauthorized access to field devices
- **Tamper detection**: Seals, enclosures with tamper switches
- **Signal integrity**: Shielded cables, surge protection
- **Fail-safe design**: Devices return to safe state on power loss

**Attack Scenarios:**

- Physical manipulation of sensors/actuators
- Signal injection or man-in-the-middle on analog loops
- Cutting communication cables to cause process disruption

Level 1: Basic Control
-----------------------

**Description:**
Local control systems that directly interface with Level 0 devices. Provides
real-time control without network dependency.

**Components:**

- Programmable Logic Controllers (PLCs)
- Distributed Control Systems (DCS)
- Remote Terminal Units (RTUs)
- Local Human-Machine Interfaces (HMIs)

**Communication:**

- Ethernet/IP, PROFINET, Modbus TCP within the cell
- Serial protocols (Modbus RTU, DNP3) to field devices
- Proprietary protocols (Siemens S7, Allen-Bradley)

**Security Considerations:**

- **Secure boot**: Prevent unauthorized firmware modifications
- **Code signing**: Verify integrity of ladder logic / control programs
- **Physical access control**: Lockout unauthorized programming
- **Network isolation**: No direct internet access

**Attack Scenarios:**

- Uploading malicious ladder logic (Stuxnet-style)
- Exploiting vulnerabilities in PLC/DCS firmware
- Man-in-the-middle attacks on control commands

Level 2: Area Supervisory Control
----------------------------------

**Description:**
Supervisory control and data acquisition for a specific cell or area.
Monitors and coordinates multiple Level 1 controllers.

**Components:**

- SCADA systems
- Area controllers
- Local historians
- Engineering workstations

**Communication:**

- Industrial Ethernet (switched, VLANs)
- OPC (OLE for Process Control) - now OPC UA
- Modbus TCP, EtherNet/IP
- Proprietary SCADA protocols

**Security Considerations:**

- **Network segmentation**: VLANs or physical separation from Level 3
- **Industrial firewall**: Between Level 2 and Level 3
- **Authentication**: Strong passwords, multi-factor if possible
- **Patch management**: Controlled updates to SCADA software

**Attack Scenarios:**

- Exploiting SCADA vulnerabilities (e.g., HMI web servers)
- Credential theft for engineering workstations
- Man-in-the-middle on OPC communications

Level 3: Site Operations & Control
-----------------------------------

**Description:**
Site-wide manufacturing operations management. Provides workflow management
and optimization for the entire facility.

**Components:**

- Manufacturing Execution Systems (MES)
- Centralized SCADA / HMI
- Plant historians (OSIsoft PI, GE Proficy)
- Asset management systems

**Communication:**

- Plant-wide Ethernet network
- OPC UA for data aggregation
- SQL databases for MES and historians
- Web-based dashboards

**Security Considerations:**

- **DMZ architecture**: Place at boundary between IT and OT
- **Data diodes**: Unidirectional flow from Level 3 to Level 4 (historians)
- **Access control**: Role-based access to MES and SCADA
- **Monitoring**: Intrusion detection systems (IDS) at boundaries

**Attack Scenarios:**

- SQL injection on MES databases
- Lateral movement from compromised Level 3 to Level 2
- Data exfiltration through historian exports

Level 4: Site Business Planning & Logistics
--------------------------------------------

**Description:**
Enterprise resource planning (ERP) and manufacturing intelligence systems.
Manages scheduling, material tracking, and plant performance.

**Components:**

- Enterprise Resource Planning (ERP) - SAP, Oracle
- Manufacturing Intelligence systems
- Scheduling and logistics
- Inventory and quality management

**Communication:**

- Corporate Ethernet network
- Internet connectivity for B2B, cloud services
- Database replication from Level 3 historians
- RESTful APIs for integration

**Security Considerations:**

- **IT security practices**: Standard enterprise security controls
- **Controlled data flow**: Only aggregated data from Level 3
- **No direct control**: Cannot directly command Level 1/2 systems
- **Incident response**: Coordinate IT and OT teams

**Attack Scenarios:**

- Phishing attacks on ERP users
- Compromised credentials used for lateral movement to Level 3
- Supply chain attacks through ERP integrations

Level 5: Enterprise Network
----------------------------

**Description:**
Corporate IT infrastructure, business systems, and external connectivity.

**Components:**

- Corporate email, file servers
- Business intelligence and analytics
- Internet gateway, VPN access
- Cloud services (AWS, Azure)

**Communication:**

- Enterprise LAN/WAN
- Internet connectivity
- VPN tunnels to remote sites
- Cloud APIs

**Security Considerations:**

- **Standard IT security**: Firewalls, antivirus, endpoint detection
- **Zero trust**: Do not assume Level 5 is trustworthy
- **Air gap or DMZ**: Strong isolation from Levels 0-3
- **Monitoring**: SIEM integration for IT and OT events

**Attack Scenarios:**

- Standard IT attacks (ransomware, malware, phishing)
- Pivot from Level 5 to Level 4, then to OT network
- Insider threats with corporate credentials

Security Zones and Conduits
============================

IEC 62443 Zones
---------------

A **zone** is a logical grouping of assets with similar security requirements.
The Purdue Model naturally defines zones:

+----------------+----------------------------+--------------------+
| Zone           | Purdue Levels              | Security Level (SL)|
+================+============================+====================+
| Enterprise     | Level 5                    | SL 1-2             |
+----------------+----------------------------+--------------------+
| DMZ            | Level 4 (boundary)         | SL 2-3             |
+----------------+----------------------------+--------------------+
| Manufacturing  | Levels 3-4                 | SL 2-3             |
+----------------+----------------------------+--------------------+
| Cell/Area      | Levels 2-3                 | SL 3-4             |
+----------------+----------------------------+--------------------+
| Safety Critical| Levels 0-2 (safety systems)| SL 4               |
+----------------+----------------------------+--------------------+

IEC 62443 Conduits
------------------

A **conduit** is a secured communication channel between zones. Security
controls applied to conduits include:

- **Firewalls**: Allow-list only required protocols and ports
- **VPNs/IPsec**: Encrypted tunnels for remote access
- **Data diodes**: Hardware-enforced unidirectional flow
- **Proxy servers**: Application-layer filtering
- **Network TAPs**: Passive monitoring for IDS

DMZ Architecture Between IT and OT
===================================

The **Demilitarized Zone (DMZ)** is a critical security boundary between
the enterprise network (Levels 4-5) and the control network (Levels 0-3).

DMZ Design Patterns
-------------------

**Pattern 1: Dual-Firewall DMZ**

.. code-block:: text

    [Level 5: Enterprise]
            │
       [Firewall 1] ← Enterprise firewall (IT managed)
            │
    ┌───────────────────┐
    │   DMZ (Level 4)   │
    │ - Data aggregation│
    │ - File transfer   │
    │ - Read-only access│
    └───────────────────┘
            │
       [Firewall 2] ← Industrial firewall (OT managed)
            │
    [Level 3: Manufacturing]

**Pattern 2: Data Diode DMZ** (High Security)

.. code-block:: text

    [Level 3: SCADA/Historian]
            │
      [Data Diode] ← One-way hardware device
            │ (Unidirectional: OT → DMZ only)
    ┌───────────────────┐
    │   DMZ (Level 4)   │
    │ - Read-only DB    │
    │ - Reporting only  │
    └───────────────────┘
            │
       [Firewall]
            │
    [Level 5: Enterprise BI]

Data Diode Benefits:

- **Physical one-way**: Hardware-enforced, cannot be bypassed
- **No command injection**: Enterprise cannot send commands to OT
- **Compliance**: Required for critical infrastructure (NERC CIP, nuclear)

Defense-in-Depth with Purdue Model
===================================

Layered Security Strategy
--------------------------

1. **Perimeter Security** (Level 5 ↔ Level 4):
   
   - Enterprise firewall
   - VPN concentrator
   - Web application firewall (WAF)

2. **DMZ Security** (Level 4):
   
   - Jump servers for remote access
   - Intrusion detection/prevention systems (IDS/IPS)
   - Secure file transfer (SFTP, HTTPS only)

3. **OT Firewall** (Level 3 ↔ Level 2):
   
   - Industrial protocol firewall (e.g., Tofino, Claroty)
   - Deep packet inspection for Modbus, OPC, DNP3
   - Application allow-listing

4. **Cell Security** (Level 2):
   
   - VLAN segmentation
   - Port security on switches
   - MAC address filtering

5. **Device Security** (Levels 0-1):
   
   - Physical locks on cabinets
   - PLC password protection
   - Firmware integrity checks

Real-World Implementation Examples
===================================

Example 1: Manufacturing Plant
-------------------------------

**Scenario:** Automotive assembly plant with 5 production lines.

.. code-block:: text

    [Level 5: Corporate ERP (SAP)]
            │
    ┌───────┴───────────────────────┐
    │    Level 4: Plant MES + DMZ   │
    │    - Production scheduling     │
    │    - Quality tracking (SQL DB) │
    └───────┬───────────────────────┘
            │ Industrial Firewall
    ┌───────┴────────────────────────┐
    │ Level 3: Plant SCADA           │
    │ - Wonderware System Platform   │
    │ - Historian (OSIsoft PI)       │
    └──┬───┬───┬───┬───┬─────────────┘
       │   │   │   │   │
     Line1 Line2 Line3 Line4 Line5
      (L2)  (L2)  (L2)  (L2)  (L2)
       │     │     │     │     │
     PLCs  PLCs  PLCs  PLCs  PLCs
     (L1)  (L1)  (L1)  (L1)  (L1)
       │     │     │     │     │
    Robots Robots Robots Robots Robots
    (L0)   (L0)   (L0)   (L0)   (L0)

**Security Controls:**

- Each production line is a separate VLAN (Level 2)
- Industrial firewall between Level 3 and Level 2
- Data diode from historian (Level 3) to MES database (Level 4)
- No internet access for Levels 0-3
- Remote access via jump server in DMZ (Level 4)

Example 2: Electric Utility (NERC CIP Compliant)
-------------------------------------------------

**Scenario:** Power generation and transmission utility.

.. code-block:: text

    [Level 5: Corporate IT]
            │
       [Firewall + IDS]
            │
    [Level 4: Business DMZ]
    - Outage management
    - GIS mapping
            │
      [Data Diode] ← One-way only
            │
    [Level 3: Control Center SCADA]
    - EMS (Energy Management System)
    - Historian
            │
    [Industrial Firewall + IPS]
            │
    [Level 2: Substation RTUs]
    - Protection relays
    - SCADA RTUs (DNP3)
            │
    [Level 1: Field Controllers]
            │
    [Level 0: Switchgear, Transformers]

**Security Controls (NERC CIP):**

- Electronic Security Perimeter (ESP) around Levels 0-3
- Data diode between Level 3 and Level 4 (NERC CIP-005)
- Multi-factor authentication for remote access (NERC CIP-005)
- Continuous monitoring of ESP (NERC CIP-007)
- Physical security for substation equipment (NERC CIP-006)

Example 3: Pharmaceutical Manufacturing (FDA 21 CFR Part 11)
-------------------------------------------------------------

**Scenario:** Sterile drug manufacturing facility.

**Zones:**

- **Clean Room Production** (Levels 0-2): Air-gapped, no external connectivity
- **Batch Control** (Level 3): Recipe management, batch historians
- **MES / Quality** (Level 4): Electronic batch records, LIMS integration
- **Corporate** (Level 5): ERP (SAP), regulatory reporting

**Security Controls:**

- Clean room systems physically isolated (no network connection)
- USB drives disabled on all OT workstations
- Audit trails for all recipe changes (21 CFR Part 11)
- Electronic signatures for batch approval
- Backup and disaster recovery for Level 3-4 systems

Python Implementation: Purdue Model Architecture
=================================================

Purdue Zone Definition and Monitoring
--------------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """
    Purdue Model Zone Definition and Security Policy Enforcement
    """
    
    from enum import Enum
    from dataclasses import dataclass
    from typing import List, Set, Dict
    import ipaddress
    
    class PurdueLevel(Enum):
        """Purdue Reference Model Levels"""
        LEVEL_0_PHYSICAL = 0        # Sensors, actuators
        LEVEL_1_BASIC_CONTROL = 1   # PLCs, DCS
        LEVEL_2_SUPERVISORY = 2     # SCADA, area controllers
        LEVEL_3_OPERATIONS = 3      # MES, plant-wide SCADA
        LEVEL_4_BUSINESS = 4        # ERP, scheduling
        LEVEL_5_ENTERPRISE = 5      # Corporate IT
        DMZ_BOUNDARY = 99           # DMZ zone
    
    class SecurityLevel(Enum):
        """IEC 62443 Security Levels"""
        SL0 = 0  # No protection
        SL1 = 1  # Protection against casual violation
        SL2 = 2  # Protection against intentional violation (low skill)
        SL3 = 3  # Protection against intentional violation (moderate skill)
        SL4 = 4  # Protection against intentional violation (high skill)
    
    @dataclass
    class Zone:
        """Security zone in Purdue Model"""
        name: str
        purdue_levels: List[PurdueLevel]
        security_level: SecurityLevel
        network_ranges: List[ipaddress.IPv4Network]
        allowed_protocols: Set[str]
        criticality: str  # 'high', 'medium', 'low'
        
        def contains_ip(self, ip: str) -> bool:
            """Check if IP address belongs to this zone"""
            ip_obj = ipaddress.IPv4Address(ip)
            return any(ip_obj in net for net in self.network_ranges)
    
    @dataclass
    class Conduit:
        """Secured communication channel between zones"""
        name: str
        from_zone: Zone
        to_zone: Zone
        allowed_protocols: Set[str]
        firewall_rules: List[Dict]
        unidirectional: bool = False  # Data diode?
        
        def validate_communication(self, protocol: str, direction: str) -> bool:
            """Validate if communication is allowed"""
            if self.unidirectional and direction == 'to_from':
                return False  # Data diode blocks return traffic
            return protocol in self.allowed_protocols
    
    class PurdueArchitecture:
        """Complete Purdue Model network architecture"""
        
        def __init__(self):
            self.zones: Dict[str, Zone] = {}
            self.conduits: List[Conduit] = []
        
        def add_zone(self, zone: Zone):
            """Add security zone to architecture"""
            self.zones[zone.name] = zone
        
        def add_conduit(self, conduit: Conduit):
            """Add secured conduit between zones"""
            self.conduits.append(conduit)
        
        def find_zone_for_ip(self, ip: str) -> Zone:
            """Determine which zone an IP address belongs to"""
            for zone in self.zones.values():
                if zone.contains_ip(ip):
                    return zone
            return None
        
        def validate_communication(self, src_ip: str, dst_ip: str, 
                                   protocol: str) -> tuple[bool, str]:
            """
            Validate if communication between two IPs is allowed
            Returns (allowed: bool, reason: str)
            """
            src_zone = self.find_zone_for_ip(src_ip)
            dst_zone = self.find_zone_for_ip(dst_ip)
            
            if not src_zone or not dst_zone:
                return False, "Unknown zone"
            
            if src_zone == dst_zone:
                # Intra-zone communication
                if protocol in src_zone.allowed_protocols:
                    return True, "Intra-zone communication allowed"
                else:
                    return False, f"Protocol {protocol} not allowed in zone"
            
            # Inter-zone communication - check conduits
            for conduit in self.conduits:
                if (conduit.from_zone == src_zone and 
                    conduit.to_zone == dst_zone):
                    if conduit.validate_communication(protocol, 'from_to'):
                        return True, f"Allowed via conduit {conduit.name}"
                    else:
                        return False, f"Protocol blocked by conduit {conduit.name}"
                
                # Check reverse direction (unless unidirectional)
                if (conduit.from_zone == dst_zone and 
                    conduit.to_zone == src_zone and 
                    not conduit.unidirectional):
                    if conduit.validate_communication(protocol, 'to_from'):
                        return True, f"Allowed via conduit {conduit.name} (reverse)"
                    else:
                        return False, f"Protocol blocked by conduit {conduit.name}"
            
            return False, "No conduit exists between zones"
        
        def generate_firewall_rules(self, conduit_name: str) -> str:
            """Generate firewall rules for a conduit"""
            conduit = next((c for c in self.conduits if c.name == conduit_name), None)
            if not conduit:
                return "Conduit not found"
            
            rules = [
                f"# Firewall rules for conduit: {conduit.name}",
                f"# From: {conduit.from_zone.name} → To: {conduit.to_zone.name}",
                ""
            ]
            
            for protocol in conduit.allowed_protocols:
                for src_net in conduit.from_zone.network_ranges:
                    for dst_net in conduit.to_zone.network_ranges:
                        rules.append(
                            f"allow {protocol} from {src_net} to {dst_net}"
                        )
            
            rules.append("# Default deny")
            rules.append("deny all")
            
            return "\n".join(rules)
    
    # Example: Manufacturing Plant Purdue Architecture
    def create_manufacturing_plant_architecture():
        """Create a sample Purdue architecture for a manufacturing plant"""
        arch = PurdueArchitecture()
        
        # Define zones
        enterprise_zone = Zone(
            name="Enterprise",
            purdue_levels=[PurdueLevel.LEVEL_5_ENTERPRISE],
            security_level=SecurityLevel.SL1,
            network_ranges=[ipaddress.IPv4Network("10.10.0.0/16")],
            allowed_protocols={'HTTP', 'HTTPS', 'SMTP', 'SQL'},
            criticality='medium'
        )
        
        dmz_zone = Zone(
            name="DMZ",
            purdue_levels=[PurdueLevel.DMZ_BOUNDARY],
            security_level=SecurityLevel.SL3,
            network_ranges=[ipaddress.IPv4Network("10.20.0.0/24")],
            allowed_protocols={'HTTPS', 'SFTP', 'OPC-UA'},
            criticality='high'
        )
        
        manufacturing_zone = Zone(
            name="Manufacturing",
            purdue_levels=[PurdueLevel.LEVEL_3_OPERATIONS, 
                          PurdueLevel.LEVEL_4_BUSINESS],
            security_level=SecurityLevel.SL3,
            network_ranges=[ipaddress.IPv4Network("192.168.10.0/24")],
            allowed_protocols={'OPC-UA', 'Modbus-TCP', 'SQL'},
            criticality='high'
        )
        
        cell_zone = Zone(
            name="Cell",
            purdue_levels=[PurdueLevel.LEVEL_2_SUPERVISORY],
            security_level=SecurityLevel.SL4,
            network_ranges=[ipaddress.IPv4Network("192.168.20.0/24")],
            allowed_protocols={'OPC-UA', 'Modbus-TCP', 'EtherNet/IP'},
            criticality='critical'
        )
        
        control_zone = Zone(
            name="Control",
            purdue_levels=[PurdueLevel.LEVEL_1_BASIC_CONTROL, 
                          PurdueLevel.LEVEL_0_PHYSICAL],
            security_level=SecurityLevel.SL4,
            network_ranges=[ipaddress.IPv4Network("192.168.30.0/24")],
            allowed_protocols={'Modbus-TCP', 'PROFINET', 'EtherNet/IP'},
            criticality='critical'
        )
        
        # Add zones to architecture
        for zone in [enterprise_zone, dmz_zone, manufacturing_zone, 
                     cell_zone, control_zone]:
            arch.add_zone(zone)
        
        # Define conduits (secured connections between zones)
        
        # Enterprise ↔ DMZ (bidirectional, through firewall)
        conduit_enterprise_dmz = Conduit(
            name="Enterprise-DMZ",
            from_zone=enterprise_zone,
            to_zone=dmz_zone,
            allowed_protocols={'HTTPS', 'SFTP'},
            firewall_rules=[
                {"action": "allow", "protocol": "HTTPS", "port": 443},
                {"action": "allow", "protocol": "SFTP", "port": 22},
            ],
            unidirectional=False
        )
        
        # DMZ → Manufacturing (unidirectional data diode for historian data)
        conduit_dmz_manufacturing = Conduit(
            name="DMZ-Manufacturing-DataDiode",
            from_zone=manufacturing_zone,
            to_zone=dmz_zone,
            allowed_protocols={'OPC-UA'},
            firewall_rules=[
                {"action": "allow", "protocol": "OPC-UA", "port": 4840},
            ],
            unidirectional=True  # Data diode: Manufacturing → DMZ only
        )
        
        # Manufacturing ↔ Cell (bidirectional, through industrial firewall)
        conduit_manufacturing_cell = Conduit(
            name="Manufacturing-Cell",
            from_zone=manufacturing_zone,
            to_zone=cell_zone,
            allowed_protocols={'OPC-UA', 'Modbus-TCP'},
            firewall_rules=[
                {"action": "allow", "protocol": "OPC-UA", "port": 4840},
                {"action": "allow", "protocol": "Modbus-TCP", "port": 502},
            ],
            unidirectional=False
        )
        
        # Cell ↔ Control (bidirectional, within OT network)
        conduit_cell_control = Conduit(
            name="Cell-Control",
            from_zone=cell_zone,
            to_zone=control_zone,
            allowed_protocols={'Modbus-TCP', 'PROFINET', 'EtherNet/IP'},
            firewall_rules=[
                {"action": "allow", "protocol": "Modbus-TCP", "port": 502},
                {"action": "allow", "protocol": "PROFINET", "port": 34964},
                {"action": "allow", "protocol": "EtherNet/IP", "port": 44818},
            ],
            unidirectional=False
        )
        
        for conduit in [conduit_enterprise_dmz, conduit_dmz_manufacturing,
                       conduit_manufacturing_cell, conduit_cell_control]:
            arch.add_conduit(conduit)
        
        return arch
    
    # Test the architecture
    if __name__ == "__main__":
        print("=" * 70)
        print("Purdue Model Architecture Validation")
        print("=" * 70)
        
        arch = create_manufacturing_plant_architecture()
        
        # Test cases
        test_cases = [
            # (src_ip, dst_ip, protocol, expected_result)
            ("10.10.1.10", "10.20.0.5", "HTTPS", True),     # Enterprise → DMZ
            ("192.168.10.5", "10.20.0.5", "OPC-UA", True),  # Manufacturing → DMZ
            ("10.20.0.5", "192.168.10.5", "OPC-UA", False), # DMZ → Manufacturing (blocked by data diode)
            ("192.168.10.5", "192.168.20.10", "OPC-UA", True),  # Manufacturing → Cell
            ("192.168.20.10", "192.168.30.15", "Modbus-TCP", True),  # Cell → Control
            ("10.10.1.10", "192.168.30.15", "Modbus-TCP", False),  # Enterprise → Control (no conduit)
        ]
        
        for src, dst, proto, expected in test_cases:
            allowed, reason = arch.validate_communication(src, dst, proto)
            status = "✓" if allowed == expected else "✗"
            print(f"\n{status} {src} → {dst} [{proto}]")
            print(f"   Result: {allowed}, Reason: {reason}")
        
        # Generate firewall rules for a conduit
        print("\n" + "=" * 70)
        print("Firewall Rules for Manufacturing-Cell Conduit")
        print("=" * 70)
        print(arch.generate_firewall_rules("Manufacturing-Cell"))

Integration with IEC 62443
===========================

The Purdue Model provides the architectural framework, while IEC 62443
provides the security requirements and controls.

Mapping Purdue Levels to IEC 62443 Zones
-----------------------------------------

+-------------------+------------------+----------------------+
| Purdue Levels     | IEC 62443 Zone   | Typical SL-T         |
+===================+==================+======================+
| Levels 0-2        | Control System   | SL 3-4               |
+-------------------+------------------+----------------------+
| Level 3           | Supervisory      | SL 2-3               |
+-------------------+------------------+----------------------+
| Level 4           | DMZ / Business   | SL 2                 |
+-------------------+------------------+----------------------+
| Level 5           | Enterprise       | SL 1                 |
+-------------------+------------------+----------------------+

Applying IEC 62443 Foundational Requirements
---------------------------------------------

**FR 1 - Identification and Authentication Control (IAC):**

- Unique user accounts (no shared passwords)
- Multi-factor authentication for remote access (Level 4-5)
- Machine authentication (X.509 certificates for OPC UA)

**FR 2 - Use Control (UC):**

- Role-based access control (RBAC)
- Least privilege (operators cannot modify PLC programs)
- Authorization enforcement at each Purdue level

**FR 3 - System Integrity (SI):**

- Code signing for PLC firmware and ladder logic
- Secure boot for Level 1 controllers
- Configuration change detection (Level 2-3)

**FR 4 - Data Confidentiality (DC):**

- TLS for OPC UA communications (Level 2-3)
- VPN for remote access (Level 4-5)
- Encrypted at rest for MES databases (Level 4)

**FR 5 - Restricted Data Flow (RDF):**

- Firewall rules at zone boundaries (Purdue level transitions)
- VLANs for network segmentation (Level 2 cells)
- Data diodes between Level 3 and Level 4

**FR 6 - Timely Response to Events (TRE):**

- Intrusion detection systems (IDS) at Level 3-4 boundary
- SIEM integration for IT and OT events
- Automated alerting for unauthorized access attempts

**FR 7 - Resource Availability (RA):**

- Redundant controllers (Level 1-2)
- Backup power (UPS) for critical systems
- DoS protection on industrial firewalls

Common Misconfigurations and Security Gaps
===========================================

1. **Flat Network (No Segmentation)**
   
   - All devices on same subnet (no Purdue separation)
   - Single breach compromises entire plant
   - **Mitigation**: Implement VLANs and firewalls at boundaries

2. **Direct Internet Access to OT**
   
   - Level 2-3 systems exposed to internet for remote monitoring
   - No DMZ or VPN
   - **Mitigation**: All remote access through DMZ jump servers

3. **IT/OT Convergence Without Security**
   
   - IT network directly connected to OT network
   - No industrial firewall
   - **Mitigation**: Implement dual-firewall DMZ

4. **Shared Credentials Across Levels**
   
   - Same password for Level 1 PLCs and Level 3 SCADA
   - **Mitigation**: Unique credentials per Purdue level

5. **No Monitoring at Zone Boundaries**
   
   - Traffic flows freely between zones without logging
   - **Mitigation**: Deploy IDS/IPS at all conduits

6. **Legacy Systems Without Patches**
   
   - Windows XP machines at Level 2 (HMI)
   - Cannot patch without downtime
   - **Mitigation**: Air-gap or strict firewall rules, compensating controls

7. **USB Drives and Removable Media**
   
   - Engineers bring infected USB drives from Level 5 to Level 1
   - **Mitigation**: USB port lockdown, media scanning stations in DMZ

Attack Scenarios and Defenses
==============================

Attack Scenario 1: Phishing → Lateral Movement
-----------------------------------------------

**Attack Path:**

1. Attacker sends phishing email to employee (Level 5)
2. Employee clicks link, malware installed on corporate laptop
3. Attacker pivots from Level 5 to Level 4 (ERP/MES)
4. Attacker exploits unpatched MES server to reach Level 3 SCADA
5. Attacker sends malicious commands to Level 2 PLCs

**Defense with Purdue Model:**

- **Level 5 → Level 4**: Enterprise firewall blocks lateral movement
- **Level 4 → Level 3**: Industrial firewall with deep packet inspection
- **Level 3 → Level 2**: Application allow-listing (only known SCADA software)
- **Level 2**: PLC password + code signing prevents unauthorized program upload

Attack Scenario 2: Insider Threat
----------------------------------

**Attack Path:**

1. Disgruntled employee with Level 3 access
2. Modifies historian data to hide production issues
3. Uploads malicious ladder logic to Level 1 PLC

**Defense with Purdue Model:**

- **Role-based access**: Operators cannot modify historian configuration
- **Audit logs**: All configuration changes logged and reviewed
- **Code signing**: PLC rejects unsigned ladder logic
- **Two-person rule**: Critical changes require dual approval

Attack Scenario 3: Supply Chain Compromise
-------------------------------------------

**Attack Path:**

1. Attacker compromises vendor's engineering laptop
2. Vendor connects to Level 2 network for maintenance
3. Malware spreads from laptop to PLCs

**Defense with Purdue Model:**

- **Jump server**: Vendor accesses through Level 4 DMZ jump server
- **Network segmentation**: Vendor can only access specific VLANs
- **Temporary access**: Credentials expire after maintenance window
- **Media scanning**: All USB drives scanned in DMZ before use in OT

Exam Questions
==============

Question 1: Purdue Model Levels (Difficulty: Medium)
-----------------------------------------------------

You are designing a water treatment plant control system. Place the following
components at the correct Purdue level:

A. Valve actuators
B. PLC controlling chlorine injection
C. Plant-wide SCADA system
D. Billing and customer management (ERP)
E. Supervisory controller for Treatment Area 1

**Answer:**

- **Level 0**: A. Valve actuators (physical process)
- **Level 1**: B. PLC controlling chlorine injection (basic control)
- **Level 2**: E. Supervisory controller for Treatment Area 1 (area supervisory)
- **Level 3**: C. Plant-wide SCADA system (site operations)
- **Level 4**: D. Billing and customer management ERP (business planning)

**Explanation:**

The Purdue Model organizes systems by function. Level 0 is the physical process
(sensors and actuators). Level 1 provides direct control (PLCs). Level 2
supervises an area. Level 3 covers plant-wide operations (SCADA). Level 4 is
business systems (ERP).

Question 2: DMZ Architecture (Difficulty: Hard)
------------------------------------------------

Your company wants to provide corporate executives (Level 5) with real-time
production dashboards sourced from the plant historian (Level 3). The CISO
insists that the corporate network cannot send commands to the control system.

Design a DMZ architecture that satisfies this requirement.

**Answer:**

.. code-block:: text

    [Level 3: Plant Historian (OSIsoft PI)]
              │
        [Data Diode] ← Hardware-enforced unidirectional
              │ (Historian → DMZ only, no return path)
              ↓
    ┌────────────────────────────────────┐
    │  DMZ (Level 4)                     │
    │  - Read-only SQL database replica  │
    │  - Web server for dashboards       │
    └────────────────────────────────────┘
              │
         [Firewall] ← Standard IT firewall
              │ (HTTPS only, port 443)
              ↓
    [Level 5: Corporate Network]
    - Executive dashboards
    - Business intelligence (Tableau, Power BI)

**Key Design Decisions:**

1. **Data Diode**: Hardware device that physically allows data to flow only in
   one direction (Historian → DMZ). Even if Level 5 is compromised, attacker
   cannot send commands back to Level 3.

2. **Read-Only Replica**: DMZ contains a read-only copy of historian data. No
   direct access to Level 3 historian database.

3. **Web Server in DMZ**: Dashboard web server sits in DMZ, not in Level 3.
   Executives access dashboards via HTTPS, never touch OT network.

4. **Firewall**: Standard IT firewall between DMZ and Level 5. Only HTTPS
   outbound from DMZ to Level 5.

**Alternative (if data diode is too expensive):**

- Use a one-way replication service (e.g., historian replication with disabled
  reverse path).
- Deploy a "data pump" server in Level 3 that pushes data to DMZ, but cannot
  receive commands.

Question 3: IEC 62443 and Purdue Integration (Difficulty: Hard)
----------------------------------------------------------------

A pharmaceutical manufacturing facility has the following zones:

- **Zone A** (Levels 0-2): Sterile production (SIL 3 safety systems)
- **Zone B** (Level 3): Manufacturing execution system (MES)
- **Zone C** (Level 4-5): Corporate ERP and quality management

Determine the appropriate IEC 62443 Security Level Target (SL-T) for each zone
and justify your answer.

**Answer:**

+---------+----------------+----------------------+------------------------+
| Zone    | Purdue Levels  | Recommended SL-T     | Justification          |
+=========+================+======================+========================+
| Zone A  | 0-2            | **SL 4**             | Safety-critical (SIL 3)|
|         |                |                      | Patient safety risk    |
|         |                |                      | Regulatory (FDA)       |
+---------+----------------+----------------------+------------------------+
| Zone B  | 3              | **SL 3**             | Production integrity   |
|         |                |                      | GMP compliance         |
|         |                |                      | Batch record tampering |
+---------+----------------+----------------------+------------------------+
| Zone C  | 4-5            | **SL 2**             | Standard IT security   |
|         |                |                      | Business systems       |
|         |                |                      | Non-safety-critical    |
+---------+----------------+----------------------+------------------------+

**Justification:**

- **Zone A (SL 4)**: Sterile production directly impacts patient safety (drug
  contamination risk). SIL 3 safety systems require highest cybersecurity
  (IEC 61508 + IEC 62443). Any compromise could cause patient harm (FDA
  regulatory action). SL 4 protects against sophisticated attackers.

- **Zone B (SL 3)**: MES controls batch recipes and production parameters. A
  compromise could lead to product quality issues or data integrity violations
  (21 CFR Part 11). SL 3 defends against intentional attacks by skilled
  adversaries, meeting GMP requirements.

- **Zone C (SL 2)**: Corporate systems handle business data but do not directly
  control production. Standard IT security controls (firewalls, antivirus)
  provide SL 2. Lower risk tolerance since not safety-critical.

**Conduit Security:**

- **Zone A ↔ Zone B**: Industrial firewall + application allow-listing
- **Zone B ↔ Zone C**: Data diode (unidirectional: B → C) for batch reports
- **Zone C ↔ Internet**: Standard enterprise firewall

Question 4: Defense-in-Depth (Difficulty: Medium)
--------------------------------------------------

An attacker has compromised an engineering workstation at Level 2 (SCADA).
List five defense-in-depth controls that would prevent the attacker from
reaching Level 1 PLCs.

**Answer:**

1. **Network Segmentation (VLAN):**
   
   - Level 2 workstation on VLAN 20
   - Level 1 PLCs on VLAN 30
   - Layer 3 switch enforces inter-VLAN routing rules

2. **Industrial Firewall:**
   
   - Firewall between Level 2 and Level 1
   - Allow-list: Only Modbus TCP port 502, only from SCADA server IP
   - Deep packet inspection for Modbus protocol anomalies

3. **Application Allow-Listing:**
   
   - Level 2 workstation can only run approved SCADA software
   - Attacker's malware is blocked by allow-listing (e.g., AppLocker)

4. **PLC Password Protection:**
   
   - PLCs require authentication for program uploads
   - Strong passwords, not default credentials
   - Password rotated quarterly

5. **Code Signing:**
   
   - PLCs only accept digitally signed ladder logic
   - Attacker cannot upload malicious program without signing key
   - Signing key stored in HSM (Hardware Security Module)

**Additional Controls (Bonus):**

6. **Intrusion Detection System (IDS):**
   
   - Monitors traffic from Level 2 to Level 1
   - Alerts on unauthorized Modbus function codes (e.g., "Write Program")

7. **Audit Logging:**
   
   - All PLC program changes logged to read-only historian
   - Alerts on unexpected program modifications

Question 5: Regulatory Compliance (Difficulty: Hard)
-----------------------------------------------------

You are the OT Security Manager for an electric utility. A NERC CIP auditor
asks: "How do you ensure that only authorized personnel can access Critical
Cyber Assets (CCAs) in your control center (Level 3)?"

Describe your answer using the Purdue Model and IEC 62443 concepts.

**Answer:**

**Purdue Model Architecture:**

Our control center (Level 3) is designated as the **Electronic Security
Perimeter (ESP)** per NERC CIP-005. We have implemented the following controls:

**1. Physical Security (NERC CIP-006):**

- Control center is a Physical Security Perimeter (PSP)
- Badge access required (two-factor: badge + PIN)
- 24/7 security cameras with 90-day retention
- Visitor log maintained

**2. Electronic Security Perimeter (NERC CIP-005):**

- **Purdue Level 3** (SCADA servers, historians) inside ESP
- **Purdue Level 4** (business network) outside ESP
- DMZ between Level 3 and Level 4:
  
  - Dual firewalls (industrial firewall + enterprise firewall)
  - Data diode for unidirectional data flow (Level 3 → Level 4)
  - Jump server for remote access (only authorized personnel)

**3. Identification and Authentication (NERC CIP-005 + IEC 62443 FR 1):**

- **Multi-factor authentication (MFA)** for remote access:
  
  - RSA SecurID tokens for VPN access
  - Privilege escalation requires second factor

- **Unique user accounts** (no shared passwords):
  
  - Active Directory integration
  - Disabled default accounts on all CCAs

- **Password requirements**:
  
  - Minimum 12 characters
  - Complexity requirements (uppercase, lowercase, numbers, symbols)
  - Changed every 90 days
  - Account lockout after 5 failed attempts

**4. Access Control (IEC 62443 FR 2 - Use Control):**

- **Role-Based Access Control (RBAC)**:
  
  - **Operators**: Read-only access to SCADA displays
  - **Engineers**: Can modify setpoints, but not SCADA configuration
  - **Administrators**: Full access, but requires two-person rule for critical changes

- **Least Privilege**:
  
  - Users granted minimum access necessary for job function
  - Quarterly access reviews

**5. Monitoring and Logging (NERC CIP-007 + IEC 62443 FR 6):**

- **Security Event Logging**:
  
  - All login attempts (successful and failed) logged
  - Logs retained for 90 days (per NERC CIP-007)
  - SIEM (Splunk) aggregates logs from all CCAs

- **Alerting**:
  
  - Real-time alerts for unauthorized access attempts
  - IDS/IPS at ESP boundary

**6. Incident Response (NERC CIP-008):**

- Incident response plan tested annually
- Escalation procedures for cyber incidents
- Coordination with E-ISAC (Electricity ISAC)

**Purdue Model Benefit for NERC CIP:**

By organizing our network using the Purdue Model, we can clearly define the
**ESP boundary** (Level 3) and enforce strict access controls. The separation
of Level 3 (critical control) from Level 4 (business) ensures that a compromise
of the corporate network does not directly impact the control center.

Conclusion
==========

The Purdue Enterprise Reference Architecture provides a proven framework for
securing industrial control systems through network segmentation and defense-
in-depth. By organizing systems into distinct levels and zones, organizations
can:

- Apply appropriate security controls at each level
- Isolate critical control systems from enterprise IT
- Meet regulatory requirements (NERC CIP, IEC 62443, FDA)
- Detect and contain security incidents before they impact operations

**Key Takeaways:**

1. **Segmentation is critical**: Do not allow direct connectivity between
   enterprise IT (Level 5) and control systems (Levels 0-2).

2. **DMZ architecture**: Use a DMZ (Level 4) with dual firewalls or data diodes
   to control data flow between IT and OT.

3. **Conduit security**: Secure communication channels (conduits) between zones
   with firewalls, VPNs, and monitoring.

4. **Defense-in-depth**: Multiple layers of security controls at each Purdue
   level.

5. **Regulatory alignment**: Purdue Model maps naturally to IEC 62443 zones and
   NERC CIP Electronic Security Perimeters.

References
==========

- ISA-95 / IEC 62264: Enterprise-Control System Integration
- ISA-99 / IEC 62443: Security for Industrial Automation and Control Systems
- NIST SP 800-82 Rev 2: Guide to Industrial Control Systems (ICS) Security
- NERC CIP (Critical Infrastructure Protection) Standards
- Theodore Williams, "The Purdue Enterprise Reference Architecture" (1994)
- SANS ICS410: ICS/SCADA Security Essentials

**END OF DOCUMENT**
