═══════════════════════════════════════════════════════════════════════════════
🏷️ VLAN - Virtual LAN (IEEE 802.1Q)
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
VLAN (Virtual Local Area Network) is a network segmentation technology defined by IEEE 802.1Q that allows multiple logical networks to coexist on the same physical infrastructure. VLANs improve security, reduce broadcast domains, and enable flexible network design.

Key Features
------------
- **Logical Segmentation**: Separate broadcast domains
- **Security Isolation**: Traffic separation between VLANs
- **Traffic Management**: Control and prioritize flows
- **Flexibility**: Reconfigure without physical changes
- **Cost Savings**: Share physical infrastructure

VLAN Tagging (802.1Q)
---------------------
Ethernet Frame with VLAN Tag::

    [Dest MAC][Src MAC][802.1Q Tag][EtherType][Payload][FCS]
                        └─ 4 bytes ─┘
    
    802.1Q Tag Structure:
    ├─ TPID (Tag Protocol ID): 0x8100
    ├─ PCP (Priority): 3 bits (0-7)
    ├─ DEI (Drop Eligible): 1 bit
    └─ VID (VLAN ID): 12 bits (0-4095)

VLAN ID Ranges
--------------
+----------------+------------------------------+
| VLAN ID        | Purpose                      |
+================+==============================+
| 0              | Priority tagging only        |
| 1              | Default VLAN                 |
| 2-1001         | Normal range VLANs           |
| 1002-1005      | Reserved (legacy protocols)  |
| 1006-4094      | Extended range VLANs         |
| 4095           | Reserved                     |
+----------------+------------------------------+

Common Use Cases
----------------
1. **Department Separation**: HR, Engineering, Finance VLANs
2. **Guest Networks**: Isolated guest WiFi VLAN
3. **Voice/Data Separation**: VoIP traffic on separate VLAN
4. **Video Production**: Separate VLANs for video, audio, control
5. **Security Zones**: DMZ, internal, management VLANs

💡 Memory Aid
─────────────────────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: VLANs as Apartment Building                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of VLANs as SEPARATE FLOORS in an APARTMENT BUILDING:              │
│                                                                           │
│  🏗️ [Single Physical Switch] = One Building                              │
│                                                                           │
│  Each floor = Different VLAN with its own community:                     │
│                                                                           │
│  🟦 VLAN 10 (Engineering Floor):                                        │
│     Developers' computers ← Room 101, 102, 103                            │
│     Can only talk to each other                                           │
│     Share common "hallway" (broadcast domain)                             │
│                                                                           │
│  🟥 VLAN 20 (HR Floor):                                                 │
│     HR systems ← Room 201, 202                                            │
│     Completely isolated from Engineering                                  │
│     Can't hear Engineer's "hallway conversations" (broadcasts)            │
│                                                                           │
│  🛫 [Trunk Port] = ELEVATOR                                               │
│     Carries people (traffic) between ALL floors                           │
│     Each person wears a color-coded badge = VLAN tag                      │
│     Blue badge → Floor 10, Red badge → Floor 20                            │
│                                                                           │
│  🚪 [Access Port] = APARTMENT DOOR                                       │
│     Connects end device (computer) to ONE floor only                      │
│     No badge needed inside apartment (untagged)                           │
│                                                                           │
│  The beauty: One building (switch), but complete isolation between        │
│  floors! Need router/Layer 3 switch to visit other floors (inter-VLAN).  │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

⚡ VLAN Tagging Deep Dive
─────────────────────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────────┐
│ 802.1Q Frame Structure (VLAN Tagging)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  UNTAGGED Ethernet Frame (standard):                                     │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ Dst MAC (6) | Src MAC (6) | EtherType (2) | Payload | FCS (4)      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│  Total: 14 bytes header + payload + 4 FCS                                │
│                                                                           │
│  ───────────────────────────────────────────────────────────────────────  │
│                                                                           │
│  TAGGED Ethernet Frame (802.1Q):                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ Dst MAC (6) | Src MAC (6) | 802.1Q (4) | EType (2) | Payload | FCS│ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                          └───┬───┘                                        │
│                              4-byte 802.1Q tag inserted here             │
│  Total: 18 bytes header + payload + 4 FCS                                │
│                                                                           │
│  802.1Q Tag Breakdown (4 bytes = 32 bits):                               │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ TPID (16 bits) | PCP (3) | DEI (1) | VID (12 bits)                 │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│       │            │         │       │                                     │
│       │            │         │       └─ VLAN ID (0-4095)                 │
│       │            │         │          12 bits = 4096 VLANs max          │
│       │            │         │          Example: 10 = 0x00A              │
│       │            │         │                                              │
│       │            │         └─ DEI (Drop Eligible Indicator)          │
│       │            │            1 bit, hint for QoS dropping             │
│       │            │                                                      │
│       │            └─ PCP (Priority Code Point)                         │
│       │               3 bits = 0-7 priority (802.1p)               │
│       │               0=Best Effort, 7=Highest priority            │
│       │               Used for QoS!                                │
│       │                                                          │
│       └─ TPID (Tag Protocol Identifier)                             │
│          0x8100 = 802.1Q VLAN tag                                   │
│          0x88A8 = 802.1ad (Q-in-Q, double tagging)                  │
│                                                                           │
│  Example 802.1Q Tag (hex):                                               │
│  81 00 (TPID) | 60 0A (PCP=3, DEI=0, VID=10)                            │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

📊 Network Segmentation Visualization
─────────────────────────────────────────────────────────────────────────────────
┌─────────────────────────────────────────────────────────────────────────────┐
│ Broadcast Production Network with VLANs                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    CORE LAYER 3 SWITCH                              │  │
│  │              (Inter-VLAN Routing Enabled)                          │  │
│  └──────────────────────────────┬──────────────────────────────────────┘  │
│                                  │ TRUNK (all VLANs tagged)                │
│                                  │ Gi0/24                                  │
│  ┌───────────────────────────────┼─────────────────────────────────────┐  │
│  │                        ACCESS LAYER SWITCH                          │  │
│  │                     (Layer 2, VLAN-aware)                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│        │           │            │           │                           │
│    Gi0/1       Gi0/2        Gi0/3       Gi0/4                          │
│    ACCESS      ACCESS       ACCESS      ACCESS                         │
│    VLAN 10     VLAN 20      VLAN 30     VLAN 40                        │
│    (untag)     (untag)      (untag)     (untag)                        │
│        │           │            │           │                           │
│        ↓           ↓            ↓           ↓                           │
│  ┌────────┐  ┌────────┐ ┌────────┐  ┌────────┐                    │
│  │ 📹 CAM │  │ 🎤 MIC │ │ 🎮 CCU  │  │ 💻 MGMT│                    │
│  │ VIDEO  │  │ AUDIO  │ │ CONTROL│  │ Switch │                    │
│  │ Stream │  │ AES67  │ │ Camera │  │ WebUI  │                    │
│  └────────┘  └────────┘ └────────┘  └────────┘                    │
│                                                                           │
│  VLAN 10: Video (SMPTE 2110) - 192.168.10.0/24                          │
│  VLAN 20: Audio (AES67)       - 192.168.20.0/24                          │
│  VLAN 30: Control             - 192.168.30.0/24                          │
│  VLAN 40: Management          - 192.168.40.0/24                          │
│                                                                           │
│  ❌ Video camera (VLAN 10) CANNOT directly talk to audio mic (VLAN 20)  │
│  ✅ Must go through Layer 3 switch for inter-VLAN routing                 │
│  ✅ Each VLAN has separate broadcast domain (reduces broadcast storms)    │
│  ✅ QoS can be applied per-VLAN (prioritize video over management)       │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

Port Types
----------
**Access Port**
  - Connects end devices (PCs, cameras)
  - Belongs to single VLAN
  - Untagged traffic

**Trunk Port**
  - Connects switches
  - Carries multiple VLANs
  - Tagged traffic (802.1Q)

**Hybrid Port**
  - Mix of tagged and untagged
  - Less common

Broadcast Production Example
----------------------------
::

    Video Production Facility:
    
    VLAN 10 - Video Streams (RTP/SMPTE 2110)
    VLAN 20 - Audio Streams (AES67)
    VLAN 30 - Control (camera control, tally)
    VLAN 40 - Management (switch management)
    VLAN 50 - Guest/Internet

Configuration Example (Cisco)
-----------------------------
Create VLAN::

    vlan 10
      name VIDEO
    vlan 20
      name AUDIO

Configure access port::

    interface GigabitEthernet1/0/1
      switchport mode access
      switchport access vlan 10

Configure trunk port::

    interface GigabitEthernet1/0/24
      switchport mode trunk
      switchport trunk allowed vlan 10,20,30

Inter-VLAN Routing
------------------
VLANs are Layer 2 constructs - communication between VLANs requires Layer 3 routing:

1. **Router on a Stick**: Single router with subinterfaces
2. **Layer 3 Switch**: Switch with routing capability
3. **Dedicated Router**: Separate router for each VLAN

Benefits
--------
- **Broadcast Control**: Limits broadcast domain size
- **Security**: Prevents direct access between VLANs
- **Performance**: Reduces unnecessary traffic
- **Flexibility**: Easy to reorganize network
- **Cost Effective**: No need for physical separation

VLAN Best Practices
-------------------
- Use VLAN 1 for management only (don't use for data)
- Document VLAN assignments
- Use consistent VLAN IDs across infrastructure
- Implement access control between VLANs
- Use VLANs with QoS for traffic prioritization

Important Notes
---------------
- Native VLAN (untagged) on trunk ports - use with caution
- VLAN hopping attacks possible with misconfiguration
- Maximum 4094 usable VLANs per network
- VLANs don't cross router boundaries (Layer 3 boundary)

🔧 Troubleshooting Guide
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 1: Cannot Communicate Between Devices in Same VLAN               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • Devices assigned to VLAN 10 cannot ping each other                     │
│ • Switch shows ports in correct VLAN                                     │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Verify VLAN membership:                                               │
│    show vlan brief                                                        │
│    show interfaces switchport                                            │
│                                                                           │
│ 2. Check port status:                                                    │
│    show interfaces status                                                │
│    - Look for "connected" state                                          │
│    - Verify correct VLAN assignment                                      │
│                                                                           │
│ 3. Verify MAC address table:                                             │
│    show mac address-table vlan 10                                        │
│    - Ensure devices' MACs are learned on correct ports                   │
│                                                                           │
│ 4. Check for port security blocking:                                     │
│    show port-security interface gi0/1                                    │
│                                                                           │
│ Common Causes:                                                            │
│ • Port configured as trunk instead of access                             │
│ • Native VLAN mismatch                                                   │
│ • Spanning Tree blocking port                                            │
│ • Port security violation                                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 2: Inter-VLAN Routing Not Working                                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • Devices in VLAN 10 cannot reach VLAN 20                                │
│ • Ping to default gateway works, but not across VLANs                    │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Verify Layer 3 switch configuration:                                  │
│    show ip interface brief                                               │
│    - Check VLAN interfaces (SVIs) are up/up                              │
│    show ip route                                                          │
│    - Verify routes exist between VLANs                                   │
│                                                                           │
│ 2. Check IP routing is enabled:                                          │
│    show running-config | include ip routing                              │
│    - Should show "ip routing" command                                    │
│                                                                           │
│ 3. Verify VLAN interfaces configured:                                    │
│    show vlan                                                              │
│    show interfaces vlan 10                                               │
│    show interfaces vlan 20                                               │
│                                                                           │
│ 4. Test routing from Layer 3 switch:                                     │
│    ping vrf <vrf-name> 192.168.20.10 source 192.168.10.1                │
│                                                                           │
│ Common Causes:                                                            │
│ • "ip routing" not enabled on Layer 3 switch                             │
│ • VLAN interface (SVI) shutdown or no IP address                         │
│ • ACL blocking inter-VLAN traffic                                        │
│ • Default gateway incorrectly configured on end devices                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 3: VLAN Traffic Leaking Across Trunk                             │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • Devices seeing broadcast traffic from unexpected VLANs                 │
│ • Security concern: VLAN isolation breached                              │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Check trunk configuration:                                            │
│    show interfaces trunk                                                 │
│    - Verify allowed VLANs list                                           │
│    - Check native VLAN settings                                          │
│                                                                           │
│ 2. Verify trunk encapsulation:                                           │
│    show interfaces gi0/24 switchport                                     │
│    - Should show "Trunking" mode                                         │
│    - Encapsulation should be 802.1Q                                      │
│                                                                           │
│ 3. Check for native VLAN mismatch:                                       │
│    show interfaces gi0/24 switchport | include Native                    │
│    - Compare native VLAN on both ends of trunk                           │
│                                                                           │
│ 4. Capture and analyze tagged frames:                                    │
│    monitor session 1 source interface gi0/24                             │
│    tcpdump -i eth0 -e vlan                                               │
│    - Look for unexpected VLAN tags                                       │
│                                                                           │
│ Common Causes:                                                            │
│ • Native VLAN mismatch between switches                                  │
│ • VLAN hopping attack (double tagging)                                   │
│ • Trunk allowed-VLAN list too permissive                                 │
│ • DTP (Dynamic Trunking Protocol) auto-negotiation                       │
│                                                                           │
│ Prevention:                                                               │
│ • Use non-default native VLAN (not VLAN 1)                               │
│ • Explicitly configure trunk ports (switchport mode trunk)               │
│ • Prune unnecessary VLANs from trunks                                    │
│ • Disable DTP: switchport nonegotiate                                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ Quick VLAN Diagnostics
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Essential Commands                                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Show VLAN database:                                                       │
│   show vlan brief                                                         │
│   show vlan id 10                                                         │
│                                                                           │
│ Show port VLAN membership:                                                │
│   show interfaces gi0/1 switchport                                        │
│   show interfaces status                                                  │
│                                                                           │
│ Show trunk ports:                                                         │
│   show interfaces trunk                                                   │
│   - Shows allowed VLANs, active VLANs, pruned VLANs                      │
│                                                                           │
│ Show MAC addresses per VLAN:                                              │
│   show mac address-table vlan 10                                          │
│                                                                           │
│ Show spanning tree per VLAN:                                              │
│   show spanning-tree vlan 10                                              │
│   - Check for blocking/forwarding states                                 │
│                                                                           │
│ Wireshark VLAN filter:                                                    │
│   vlan.id == 10                                                           │
│   vlan.priority == 5                                                      │
│                                                                           │
│ tcpdump VLAN capture:                                                     │
│   tcpdump -i eth0 -e 'vlan 10'                                            │
│   tcpdump -i eth0 -e 'vlan and icmp'                                      │
│   - The -e flag shows link-layer headers (802.1Q tags)                   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘
