═══════════════════════════════════════════════════════════════════════════════
🔀 Layer 2 & Layer 3 Switching
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
Switches operate at different layers of the OSI model. Layer 2 switches forward frames based on MAC addresses, while Layer 3 switches can also route packets based on IP addresses, combining switching and routing functionality.

Layer 2 Switching
-----------------
**Data Link Layer** (OSI Layer 2)

**Key Features**:
  - Forwards frames based on MAC addresses
  - Builds MAC address table (CAM table)
  - Operates within single broadcast domain
  - VLAN support for segmentation
  - Fast and inexpensive

**Switching Methods**:
  - **Store-and-Forward**: Receives entire frame, checks FCS
  - **Cut-Through**: Forwards after reading destination MAC
  - **Fragment-Free**: Reads first 64 bytes before forwarding

Layer 3 Switching
-----------------
**Network Layer** (OSI Layer 3)

**Key Features**:
  - Routes packets based on IP addresses
  - Inter-VLAN routing capability
  - Hardware-accelerated routing (ASIC)
  - Access Control Lists (ACLs)
  - Faster than traditional routers

**Capabilities**:
  - Route between different subnets
  - Apply QoS policies
  - Implement security policies
  - Support routing protocols (OSPF, BGP)

Comparison
----------
+----------------------+-------------------+-------------------+
| Feature              | Layer 2 Switch    | Layer 3 Switch    |
+======================+===================+===================+
| Forwarding Based On  | MAC address       | IP address        |
| Speed                | Very fast         | Fast              |
| Inter-VLAN Routing   | No                | Yes               |
| Broadcast Domains    | Single (per VLAN) | Multiple          |
| Cost                 | Lower             | Higher            |
| Intelligence         | Limited           | Routing capable   |
| Use Case             | LAN segments      | Core/distribution |
+----------------------+-------------------+-------------------+

MAC Address Table (Layer 2)
---------------------------
Example CAM table::

    VLAN   MAC Address         Port    Age
    ----   -----------------   ----    ---
    10     00:1A:2B:3C:4D:5E   Gi1/1   120
    10     00:AA:BB:CC:DD:EE   Gi1/2   45
    20     00:11:22:33:44:55   Gi1/5   200

Learning process:
  1. Frame arrives on port
  2. Source MAC added to table
  3. Destination MAC looked up
  4. Frame forwarded to appropriate port
  5. Unknown destinations flooded

Routing Table (Layer 3)
-----------------------
Example routing table::

    Network          Next Hop       Interface    Metric
    ---------------  -------------  -----------  ------
    10.0.0.0/8       Directly Conn  VLAN10       0
    192.168.1.0/24   Directly Conn  VLAN20       0
    0.0.0.0/0        10.0.0.1       VLAN10       1

Common Use Cases
----------------
**Layer 2 Switching**:
  1. Access layer connectivity (end devices)
  2. Within same subnet/VLAN
  3. High port density requirements
  4. Simple network designs

**Layer 3 Switching**:
  1. Inter-VLAN routing
  2. Distribution/core layers
  3. Network segmentation with routing
  4. Complex routing requirements
  5. Broadcast domain separation

💡 Memory Aid
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: Switching as Postal Delivery System                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of Layer 2 and Layer 3 switching as TWO TYPES OF MAIL DELIVERY:      │
│                                                                           │
│  📬 LAYER 2 SWITCH = Local Mail Sorter in ONE Building                      │
│      Like mail room in apartment building                                │
│      Uses APARTMENT NUMBERS (MAC addresses)                              │
│      Only delivers within the building (same subnet/VLAN)                │
│      Very fast - just looks at apartment number                          │
│                                                                           │
│      Example: Mail arrives addressed to "Apt 3B"                         │
│      → Mail room checks directory (CAM table)                            │
│      → "Apt 3B = Mailbox #12"                                            │
│      → Puts mail in mailbox #12                                          │
│      → DONE! No thinking about street addresses                          │
│                                                                           │
│  🌍 LAYER 3 SWITCH = City Postal Service                                    │
│      Like main post office sorting mail between neighborhoods             │
│      Uses STREET ADDRESSES (IP addresses)                                │
│      Delivers across different buildings (different subnets/VLANs)       │
│      Slightly slower - must read full address and route                  │
│                                                                           │
│      Example: Mail addressed to "123 Main St, Building A"                │
│      → Post office checks routing map (routing table)                    │
│      → "Main St is in North District, send via Truck Route 5"           │
│      → Forwards to correct district post office                          │
│      → That office delivers locally (Layer 2)                            │
│                                                                           │
│  🔑 Key Difference:                                                          │
│  Layer 2 = "Apt 3B" (local delivery, one building)                       │
│  Layer 3 = "123 Main St, Building A" (city-wide delivery, routing)      │
│                                                                           │
│  Why need Layer 3? Same reason you need city post office:                │
│  • Mail room can't deliver to other buildings (VLANs isolated)           │
│  • Need postal service to route between neighborhoods (inter-VLAN)       │
│  • Layer 3 switch = Post office inside your building (fast routing!)    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

🌳 Switching vs Routing Decision Tree
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Packet Arrives at Switch - How is it Forwarded?                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                      📦 FRAME/PACKET ARRIVES                                 │
│                               │                                              │
│                               ▼                                              │
│                  ┌──────────────────────────┐                               │
│                  │ Is this a Layer 2 switch │                               │
│                  │   (no routing enabled)?  │                               │
│                  └────────┬─────────────────┘                               │
│                           │                                                  │
│                  YES ◄────┴────► NO (Layer 3 switch)                         │
│                   │                    │                                     │
│                   ▼                    ▼                                     │
│        ┌─────────────────────┐  ┌──────────────────────────┐               │
│        │ LAYER 2 FORWARDING  │  │ Check destination IP     │               │
│        │                     │  │ in frame                 │               │
│        │ 1. Read Dest MAC    │  └───────┬──────────────────┘               │
│        │ 2. Lookup in CAM    │          │                                   │
│        │ 3. Check VLAN       │          ▼                                   │
│        └──────┬──────────────┘  ┌──────────────────────────┐               │
│               │                 │ Is destination IP in     │               │
│               ▼                 │ same subnet (same VLAN)? │               │
│        ┌─────────────────┐      └────┬────────────┬────────┘               │
│        │ MAC in table?   │           │            │                         │
│        └────┬──────┬─────┘      YES  │            │  NO                     │
│             │      │                  │            │                         │
│         YES │      │ NO               ▼            ▼                         │
│             │      │          ┌────────────┐  ┌─────────────────┐           │
│             ▼      ▼          │LAYER 2     │  │ LAYER 3         │           │
│     ┌──────────┐ ┌─────────┐ │FORWARDING  │  │ ROUTING         │           │
│     │Forward to│ │Flood to │ │            │  │                 │           │
│     │specific  │ │all ports│ │Use CAM     │  │Use Routing      │           │
│     │port      │ │in VLAN  │ │table       │  │table            │           │
│     └────┬─────┘ └────┬────┘ │            │  │                 │           │
│          │            │      └─────┬──────┘  └────┬────────────┘           │
│          ▼            ▼            │              │                         │
│     ┌────────────────────┐         │              ▼                         │
│     │ TRANSMIT on egress │◄────────┘      ┌──────────────────┐             │
│     │ port (wire speed)  │                │ 1. Decrement TTL │             │
│     └────────────────────┘                │ 2. Lookup next-hop│             │
│                                           │ 3. ARP for MAC    │             │
│                                           │ 4. Rewrite MAC    │             │
│                                           │ 5. Forward frame  │             │
│                                           └────────┬──────────┘             │
│                                                    │                         │
│                                                    ▼                         │
│                                           ┌────────────────┐                 │
│                                           │ TRANSMIT on    │                 │
│                                           │ routed port    │                 │
│                                           └────────────────┘                 │
│                                                                           │
│  KEY DIFFERENCES:                                                         │
│  Layer 2: MAC lookup → Forward (1 table lookup, <10μs)                   │
│  Layer 3: IP lookup → Routing table → ARP → Rewrite MAC → Forward       │
│           (multiple lookups, ~50μs but hardware-accelerated)             │
│                                                                           │
│  Layer 3 switch advantage: Does Layer 3 in hardware (ASIC) = wire speed! │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📊 Packet Forwarding Comparison
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Layer 2 Frame Forwarding (Same VLAN)                                     │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Host A (VLAN 10)                          Host B (VLAN 10)              │
│  10.0.10.100                               10.0.10.200                   │
│  MAC: AA:AA:AA:AA:AA:AA                    MAC: BB:BB:BB:BB:BB:BB        │
│        │                                           ▲                       │
│        │ Ethernet Frame:                           │                       │
│        │ [Dst MAC: BB:BB:BB...][Src MAC: AA:AA...][IP Packet][FCS]        │
│        │                                           │                       │
│        └────────────► Layer 2 Switch ──────────────┘                      │
│                            │                                               │
│                            │ CAM Table Lookup:                             │
│                            │ BB:BB:BB... → Port Gi0/2                      │
│                            │ Forward directly!                             │
│                            │                                               │
│  Processing:                                                              │
│  1. Read destination MAC from frame header                                │
│  2. Look up MAC in CAM table                                              │
│  3. Forward frame out port Gi0/2                                          │
│  4. No IP inspection, no packet modification                              │
│  Latency: ~5-10 microseconds (wire speed)                                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Layer 3 Routing Between VLANs (Inter-VLAN)                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Host A (VLAN 10)                                    Host B (VLAN 20)    │
│  10.0.10.100                                         10.0.20.200          │
│  MAC: AA:AA:AA:AA:AA:AA                              MAC: BB:BB:BB:BB:BB:BB│
│  Gateway: 10.0.10.1                                  Gateway: 10.0.20.1  │
│        │                                                     ▲             │
│        │ Frame to gateway:                                  │             │
│        │ [Dst MAC: SW:SW:SW...][Src MAC: AA:AA...][IP: 10.0.20.200][FCS] │
│        │                                                     │             │
│        └──────────────────► Layer 3 Switch ─────────────────┘             │
│                                   │                                        │
│                                   │ SVI: VLAN 10 (10.0.10.1)              │
│                                   │ SVI: VLAN 20 (10.0.20.1)              │
│                                   │                                        │
│                             ┌─────▼──────┐                                │
│                             │  ROUTING   │                                │
│                             │  ENGINE    │                                │
│                             │  (ASIC)    │                                │
│                             └─────┬──────┘                                │
│                                   │                                        │
│  Processing:                      │                                        │
│  1. Receive frame on VLAN 10 port │                                        │
│  2. Dest MAC = switch MAC (gateway)                                       │
│  3. Extract IP packet, check dest IP = 10.0.20.200                        │
│  4. Routing table lookup: 10.0.20.0/24 → VLAN 20                          │
│  5. ARP lookup for 10.0.20.200 → BB:BB:BB:BB:BB:BB                        │
│  6. Rewrite frame: [Dst MAC: BB:BB...][Src MAC: SW:SW...][IP packet][FCS]│
│  7. Forward frame out VLAN 20 port                                        │
│  8. Decrement TTL, recalculate IP checksum                                │
│  Latency: ~50 microseconds (hardware ASIC acceleration)                   │
│                                                                           │
│  Traditional Router (software): ~1-5 milliseconds (100× slower!)          │
│  Layer 3 Switch (hardware): ~50 microseconds (wire speed!)                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ CAM Table vs Routing Table vs ARP Table                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  CAM Table (Layer 2):                                                     │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │ VLAN │ MAC Address       │ Port   │ Type    │ Age                │      │
│  ├──────┼───────────────────┼────────┼─────────┼────────────────────┤      │
│  │ 10   │ AA:AA:AA:AA:AA:AA │ Gi0/1  │ Dynamic │ 120 seconds        │      │
│  │ 10   │ BB:BB:BB:BB:BB:BB │ Gi0/2  │ Dynamic │ 45 seconds         │      │
│  │ 20   │ CC:CC:CC:CC:CC:CC │ Gi0/5  │ Dynamic │ 200 seconds        │      │
│  └──────┴───────────────────┴────────┴─────────┴────────────────────┘      │
│  Purpose: Maps MAC addresses to physical switch ports                     │
│  Built by: Learning source MAC from incoming frames                       │
│  Used for: Layer 2 forwarding decisions                                   │
│                                                                           │
│  ────────────────────────────────────────────────────────────────────    │
│                                                                           │
│  Routing Table (Layer 3):                                                 │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │ Network       │ Mask      │ Next Hop  │ Interface │ Metric │ AD  │      │
│  ├───────────────┼───────────┼───────────┼───────────┼────────┼─────┤      │
│  │ 10.0.10.0     │/24        │ Connected │ VLAN10    │ 0      │ 0   │      │
│  │ 10.0.20.0     │/24        │ Connected │ VLAN20    │ 0      │ 0   │      │
│  │ 0.0.0.0       │/0         │ 10.0.10.1 │ VLAN10    │ 1      │ 1   │      │
│  │ 192.168.50.0  │/24        │ 10.0.10.254│VLAN10    │ 20     │ 110 │      │
│  └───────────────┴───────────┴───────────┴───────────┴────────┴─────┘      │
│  Purpose: Maps destination IP networks to next-hop/interface              │
│  Built by: Direct connections, static routes, dynamic routing protocols   │
│  Used for: Layer 3 routing decisions (inter-VLAN)                         │
│                                                                           │
│  ────────────────────────────────────────────────────────────────────    │
│                                                                           │
│  ARP Table (Layer 2 ↔ Layer 3 mapping):                                  │
│  ┌────────────────────────────────────────────────────────────────┐      │
│  │ IP Address    │ MAC Address       │ Type    │ Interface │ Age     │      │
│  ├───────────────┼───────────────────┼─────────┼───────────┼─────────┤      │
│  │ 10.0.10.100   │ AA:AA:AA:AA:AA:AA │ Dynamic │ VLAN10    │ 120 sec │      │
│  │ 10.0.10.200   │ BB:BB:BB:BB:BB:BB │ Dynamic │ VLAN10    │ 45 sec  │      │
│  │ 10.0.20.100   │ CC:CC:CC:CC:CC:CC │ Dynamic │ VLAN20    │ 200 sec │      │
│  │ 10.0.10.1     │ SW:SW:SW:SW:SW:01 │ Static  │ VLAN10    │ -       │      │
│  └───────────────┴───────────────────┴─────────┴───────────┴─────────┘      │
│  Purpose: Maps Layer 3 IP addresses to Layer 2 MAC addresses              │
│  Built by: ARP requests/replies ("Who has IP X? Tell me your MAC")       │
│  Used for: Layer 3 switch needs MAC to build Ethernet frame              │
│                                                                           │
│  Flow: Routing Table (which interface) → ARP Table (which MAC)           │
│        → CAM Table (which port) → FORWARD!                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Inter-VLAN Routing Example
--------------------------
Without Layer 3 switch::

    VLAN 10 <--> L2 Switch <--> Router <--> L2 Switch <--> VLAN 20
    (Slow, router bottleneck)

With Layer 3 switch::

    VLAN 10 <--> L3 Switch <--> VLAN 20
    (Fast, hardware-accelerated)

Configuration Example (Cisco)
-----------------------------
Layer 2 VLAN configuration::

    vlan 10
      name PRODUCTION
    interface GigabitEthernet1/0/1
      switchport mode access
      switchport access vlan 10

Layer 3 SVI (Switch Virtual Interface)::

    interface vlan 10
      ip address 10.0.10.1 255.255.255.0
      no shutdown
    
    interface vlan 20
      ip address 10.0.20.1 255.255.255.0
      no shutdown
    
    ip routing

Performance Characteristics
---------------------------
**Layer 2 Switching**:
  - Wire-speed forwarding
  - Low latency (<10 microseconds)
  - Gigabit to 100 Gigabit per port

**Layer 3 Switching**:
  - Near wire-speed routing (ASIC-based)
  - Slightly higher latency (~50 microseconds)
  - High throughput (millions of packets per second)

When to Use Each
----------------
**Use Layer 2 Switch When**:
  - All devices in same subnet
  - Simple flat network
  - Budget constraints
  - Access layer deployment

**Use Layer 3 Switch When**:
  - Multiple VLANs need routing
  - Network segmentation required
  - Security policies between subnets
  - Core/distribution layer
  - High-performance routing needed

Important Concepts
------------------
- **SVI** (Switch Virtual Interface): Virtual interface for routing
- **Routed Port**: Physical port configured as Layer 3
- **ARP Table**: Maps IP to MAC (Layer 3)
- **CAM Table**: Maps MAC to port (Layer 2)
- **CEF** (Cisco Express Forwarding): Hardware routing acceleration

Troubleshooting
---------------
**Layer 2 Issues**:
  - MAC address table full
  - Broadcast storms
  - Spanning tree problems
  - Port speed/duplex mismatch

**Layer 3 Issues**:
  - Routing table errors
  - Subnet mask mismatches
  - Default gateway incorrect
  - ACL blocking traffic

Important Notes
---------------
- Layer 3 switches don't replace routers for WAN
- Most modern switches are Layer 3 capable
- Layer 3 switching is done in hardware (ASIC)
- VLANs require Layer 3 to communicate with each other
