═══════════════════════════════════════════════════════════════════════════════
🎚️ Network Switches - L2/L3 Forwarding Devices
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
Network switches are fundamental devices that connect multiple devices within a local area network (LAN). They operate primarily at Layer 2 (Data Link) or Layer 3 (Network) of the OSI model, intelligently forwarding data to specific destinations based on MAC or IP addresses.

Key Features
------------
- **Multiport Connectivity**: 8, 24, 48+ ports typical
- **Full Duplex**: Simultaneous send/receive
- **MAC Learning**: Builds forwarding table automatically
- **VLAN Support**: Logical network segmentation
- **Link Aggregation**: Combine ports for higher bandwidth
- **Power over Ethernet (PoE)**: Power devices via Ethernet

Switch Types
------------
**Unmanaged Switches**
  - Plug-and-play operation
  - No configuration interface
  - Fixed functionality
  - Home/small office use
  - Low cost

**Managed Switches**
  - Full configuration control
  - VLAN, QoS, security features
  - SNMP monitoring
  - Enterprise deployment
  - Higher cost

**Smart/Web-Managed Switches**
  - Basic management features
  - Web interface
  - VLAN support
  - Mid-range option

Port Speeds
-----------
+----------------+-------------------+-------------------+
| Standard       | Speed             | Common Use        |
+================+===================+===================+
| Fast Ethernet  | 100 Mbps          | Legacy devices    |
| Gigabit        | 1 Gbps            | Desktop/servers   |
| 10 Gigabit     | 10 Gbps           | Servers/uplinks   |
| 25 Gigabit     | 25 Gbps           | Data center       |
| 40 Gigabit     | 40 Gbps           | Core backbone     |
| 100 Gigabit    | 100 Gbps          | Core/data center  |
+----------------+-------------------+-------------------+

Common Use Cases
----------------
1. **Access Layer**: Connect end devices (PCs, cameras)
2. **Distribution Layer**: Aggregate access switches
3. **Core Layer**: High-speed backbone
4. **Video Production**: SMPTE 2110 video routing
5. **Data Center**: Server interconnection

⚡ Switch Selection Quick Reference
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Choosing the Right Switch for Your Use Case                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  SMALL OFFICE / HOME (5-10 devices):                                        │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 8-16 port Gigabit unmanaged switch                                     │ │
│  │ • Plug-and-play, no config needed                                      │ │
│  │ • $30-100 range                                                        │ │
│  │ • Examples: Netgear GS308, TP-Link TL-SG108                           │ │
│  │ ✓ Desktop computers, printers, WiFi APs                               │ │
│  │ ✗ No VLAN support, no monitoring                                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  SMALL BUSINESS (10-50 devices):                                            │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 24-48 port Gigabit smart/managed switch                               │ │
│  │ • Basic VLAN support                                                   │ │
│  │ • Web interface for management                                         │ │
│  │ • $200-500 range                                                       │ │
│  │ • Examples: Cisco SG350, HPE OfficeConnect                            │ │
│  │ ✓ VLANs for guest WiFi, IP phones, data separation                    │ │
│  │ ✓ Basic QoS for VoIP                                                  │ │
│  │ ✗ No advanced routing, limited ACLs                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  VIDEO PRODUCTION / BROADCAST (SMPTE 2110):                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 10/25/100 GbE Layer 3 managed switch with PTP support                 │ │
│  │ • Hardware PTP (IEEE 1588)                                             │ │
│  │ • IGMP snooping for multicast                                          │ │
│  │ • Jumbo frames (9000 MTU)                                              │ │
│  │ • $5,000-50,000+ range                                                 │ │
│  │ • Examples: Cisco Nexus, Arista 7050, Mellanox                        │ │
│  │ ✓ Ultra-low latency (<10μs)                                           │ │
│  │ ✓ Non-blocking architecture                                           │ │
│  │ ✓ Large buffers for video bursts                                      │ │
│  │ ⚠ Requires expert configuration                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  ENTERPRISE CORE (100+ devices):                                            │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 48+ port 10GbE + 100GbE uplinks Layer 3 switch                        │ │
│  │ • Full Layer 3 routing (OSPF, BGP)                                    │ │
│  │ • Stacking/chassis redundancy                                          │ │
│  │ • Advanced ACLs and security                                           │ │
│  │ • $10,000-100,000+ range                                               │ │
│  │ • Examples: Cisco Catalyst 9500, Juniper EX4650                       │ │
│  │ ✓ Wire-speed Layer 3 routing                                          │ │
│  │ ✓ High availability features                                          │ │
│  │ ✓ Full network management integration                                 │ │
│  │ ⚠ Requires dedicated network team                                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  KEY DECISION FACTORS:                                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Port Count:     How many devices + 20% growth?                        │ │
│  │ Speed:          1GbE (standard), 10GbE (servers), 25+GbE (video)      │ │
│  │ Management:     Unmanaged (simple), Smart (basic), Managed (full)     │ │
│  │ Layer 3:        Need inter-VLAN routing? Get Layer 3 switch           │ │
│  │ PoE:            Power IP cameras/phones? Get PoE+ (30W per port)      │ │
│  │ Budget:         Unmanaged: $5-10/port, Managed: $50-200/port          │ │
│  │ Latency:        Standard: 50μs, Video production: <10μs               │ │
│  │ PTP:            Video sync? Hardware PTP mandatory                     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

🔧 Practical Troubleshooting Scenarios
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Scenario 1: New Device Not Getting Network Connection                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Problem: Plugged in device, no link light on switch                          │
│                                                                           │
│ Quick Checks:                                                                 │
│ ① Check physical cable:                                                      │
│    • Try different cable                                                     │
│    • Check both ends are firmly seated                                       │
│    • Look for damaged RJ45 connector                                         │
│                                                                           │
│ ② Check switch port LED:                                                     │
│    • No light = No physical connection                                       │
│    • Amber/Orange = 100Mbps or error                                         │
│    • Green = 1Gbps link                                                      │
│                                                                           │
│ ③ Verify port is enabled:                                                    │
│    show interfaces status                                                    │
│    - Look for "disabled" or "err-disabled"                                  │
│    - If disabled: no shutdown                                                │
│                                                                           │
│ ④ Check speed/duplex:                                                        │
│    show interfaces gi0/1                                                     │
│    - Auto-negotiation failures common with old devices                       │
│    - Try forcing: speed 100 / duplex full                                    │
│                                                                           │
│ ⑤ Check VLAN membership:                                                     │
│    show vlan brief                                                           │
│    - Port might be in wrong VLAN                                             │
│    - switchport access vlan 10                                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Scenario 2: Intermittent Network Performance / Packet Loss                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Problem: File transfers slow, video stutters, timeouts                       │
│                                                                           │
│ Diagnostic Steps:                                                             │
│ ① Check interface errors:                                                    │
│    show interfaces gi0/1                                                     │
│    show interfaces counters errors                                           │
│                                                                           │
│    Look for:                                                                 │
│    • Input errors: Bad cable, interference                                   │
│    • CRC errors: Cable too long, EMI                                         │
│    • Output drops: Congestion, insufficient buffers                          │
│    • Collisions: Duplex mismatch (half/full conflict)                       │
│                                                                           │
│ ② Duplex mismatch detection:                                                 │
│    show interfaces gi0/1 | include duplex                                    │
│    - One side auto, other forced = MISMATCH                                  │
│    - Symptoms: Slow, lots of collisions, packet loss                         │
│    - Fix: Set both to auto OR both to forced matching                        │
│                                                                           │
│ ③ Check utilization:                                                         │
│    show interfaces gi0/1 | include rate                                      │
│    - >80% utilization = upgrade link or add LAG                              │
│                                                                           │
│ ④ Monitor for broadcast storms:                                              │
│    show interfaces gi0/1 | include broadcast                                 │
│    - Excessive broadcasts = loop or misbehaving device                       │
│    - Enable storm control:                                                   │
│      storm-control broadcast level 10.00                                     │
│                                                                           │
│ ⑤ Check spanning tree:                                                       │
│    show spanning-tree interface gi0/1                                        │
│    - Frequent topology changes = stability issue                             │
│    - Port flapping between forwarding/blocking                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Scenario 3: Multicast Video Not Working (SMPTE 2110 / IPTV)                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Problem: Multicast video streams not reaching receivers                      │
│                                                                           │
│ Critical Checks:                                                              │
│ ① Verify IGMP snooping:                                                      │
│    show ip igmp snooping                                                     │
│    - Must be ENABLED globally                                                │
│    - ip igmp snooping                                                        │
│                                                                           │
│ ② Check IGMP snooping per VLAN:                                              │
│    show ip igmp snooping vlan 10                                             │
│    - Should show "IGMP snooping is enabled"                                 │
│    - ip igmp snooping vlan 10                                                │
│                                                                           │
│ ③ Verify multicast router ports:                                             │
│    show ip igmp snooping mrouter                                             │
│    - Uplink to multicast source must be mrouter port                         │
│    - Add manually: ip igmp snooping mrouter interface gi0/24                 │
│                                                                           │
│ ④ Check group membership:                                                    │
│    show ip igmp snooping groups                                              │
│    - Should show receivers' ports for multicast group                        │
│    - If empty, check IGMP reports from receivers                             │
│                                                                           │
│ ⑤ Enable IGMP querier (if no multicast router):                              │
│    ip igmp snooping querier                                                  │
│    show ip igmp snooping querier                                             │
│    - Needed for IGMP snooping to work without router                         │
│                                                                           │
│ ⑥ Check for IGMP filtering:                                                  │
│    show ip igmp snooping groups                                              │
│    - Ensure multicast range not filtered                                     │
│    - Check ACLs: show access-list                                            │
│                                                                           │
│ For SMPTE 2110 specifically:                                                  │
│ • Enable jumbo frames: system mtu 9000                                       │
│ • Disable flow control (can cause frame drops)                               │
│ • Verify PTP sync: show ptp clock                                            │
│ • Check multicast routing: show ip mroute                                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ Essential Commands Quick Reference
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Daily Operations                                                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Show all interface status:                                                   │
│   show interfaces status                                                     │
│   show interfaces description                                                │
│                                                                           │
│ Show specific interface details:                                             │
│   show interfaces gigabitEthernet 1/0/1                                      │
│   show interfaces gi1/0/1 switchport                                         │
│                                                                           │
│ Show MAC address table:                                                      │
│   show mac address-table                                                     │
│   show mac address-table address aaaa.bbbb.cccc                              │
│   show mac address-table vlan 10                                             │
│                                                                           │
│ Show VLANs:                                                                  │
│   show vlan brief                                                            │
│   show vlan id 10                                                            │
│                                                                           │
│ Show trunk ports:                                                            │
│   show interfaces trunk                                                      │
│                                                                           │
│ Monitor errors:                                                              │
│   show interfaces counters errors                                            │
│   show interfaces | include error|drop                                       │
│                                                                           │
│ Check port utilization:                                                      │
│   show interfaces gi1/0/1 | include rate                                     │
│   show interfaces counters                                                   │
│                                                                           │
│ Spanning Tree status:                                                        │
│   show spanning-tree                                                         │
│   show spanning-tree interface gi1/0/1 detail                                │
│                                                                           │
│ For Video Production:                                                        │
│   show ip igmp snooping groups            # Multicast viewers               │
│   show ptp clock                          # PTP sync status                 │
│   show qos interface gi1/0/1              # QoS policies                     │
│   show mls qos interface gi1/0/1 statistics  # QoS counters                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Key Technologies
----------------
**Spanning Tree Protocol (STP)**
  - Prevents network loops
  - Blocks redundant paths
  - Automatic failover

**Link Aggregation (LAG)**
  - IEEE 802.3ad / LACP
  - Combines multiple links
  - Increased bandwidth + redundancy

**Power over Ethernet (PoE)**
  - IEEE 802.3af (15.4W)
  - IEEE 802.3at (30W - PoE+)
  - IEEE 802.3bt (60W/100W - PoE++)
  - Powers IP cameras, phones, APs

**Quality of Service (QoS)**
  - Traffic prioritization
  - 802.1p (CoS) marking
  - DSCP support
  - Queue management

Broadcast Production Example
----------------------------
Video facility switching architecture::

    Core Switch (100GbE)
         |
    [Distribution Layer 10GbE Switches]
         |
    [Access Layer 1GbE/10GbE Switches]
         |
    Cameras, Encoders, Monitors
    
    VLANs:
    - VLAN 10: Video streams (SMPTE 2110)
    - VLAN 20: Audio (AES67)
    - VLAN 30: Control
    - VLAN 40: Management

Switch Architecture
-------------------
**Store-and-Forward**
  - Receives entire frame
  - Checks for errors (FCS)
  - Most common method
  - Higher latency but reliable

**Cut-Through**
  - Forwards after reading destination MAC
  - Lower latency
  - No error checking
  - Rare in modern switches

MAC Address Table
-----------------
Switch learns and maintains table::

    Port    MAC Address          VLAN    Age
    ----    -----------------    ----    ---
    1       00:11:22:33:44:55    10      120
    1       AA:BB:CC:DD:EE:FF    10      45
    2       11:22:33:44:55:66    20      300

Forwarding Decision:
  - Known MAC: Forward to specific port
  - Unknown MAC: Flood to all ports in VLAN
  - Broadcast: Flood to all ports in VLAN

Performance Metrics
-------------------
**Switching Capacity**: Total throughput (Gbps)
  - Example: 48-port Gigabit = 96 Gbps (full duplex)

**Forwarding Rate**: Packets per second (pps)
  - Gigabit: ~1.488 million pps (64-byte packets)
  - 10 Gigabit: ~14.88 million pps

**Latency**: Switch delay
  - Typical: 5-50 microseconds
  - Store-and-forward: Higher
  - Cut-through: Lower

Configuration Example (Cisco)
-----------------------------
Basic setup::

    hostname PRODUCTION-SW1
    !
    vlan 10
      name VIDEO
    vlan 20
      name AUDIO
    !
    interface GigabitEthernet1/0/1
      description Camera-1
      switchport mode access
      switchport access vlan 10
    !
    interface GigabitEthernet1/0/24
      description Uplink
      switchport mode trunk
      switchport trunk allowed vlan 10,20

Important Features for Media
----------------------------
**For Video Production**:
  - 10GbE ports minimum
  - Low latency (<10μs)
  - PTP support (IEEE 1588)
  - IGMP snooping for multicast
  - Jumbo frames support (>1500 MTU)
  - QoS with strict priority queuing

**For SMPTE 2110**:
  - 25GbE or 100GbE recommended
  - Hardware PTP (nanosecond accuracy)
  - Large buffer memory
  - Non-blocking architecture

Troubleshooting
---------------
**No Link**:
  - Check cable
  - Verify speed/duplex settings
  - Check port status

**Slow Performance**:
  - Check for errors on port
  - Verify duplex match
  - Check for broadcast storms

**VLAN Issues**:
  - Verify VLAN configuration
  - Check trunk port settings
  - Verify native VLAN matches

Monitoring Commands
-------------------
Show interfaces::

    show interfaces status
    show interfaces GigabitEthernet1/0/1

Show MAC table::

    show mac address-table

Show VLANs::

    show vlan brief

Show port statistics::

    show interfaces counters errors

Important Notes
---------------
- Switches learn MAC addresses dynamically
- Broadcast domains limited by VLANs
- Spanning tree prevents loops but adds convergence time
- Jumbo frames (9000 bytes) reduce overhead for video
- For mission-critical: Use redundant switches + LAG
