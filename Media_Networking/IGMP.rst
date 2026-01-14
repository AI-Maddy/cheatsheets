═══════════════════════════════════════════════════════════════════════════════
📢 IGMP - Internet Group Management Protocol
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
IGMP (Internet Group Management Protocol) is used by hosts and adjacent routers to establish multicast group membership. It enables routers to discover which hosts want to receive multicast traffic and on which interfaces.

Key Features
------------
- **Multicast Management**: Join/leave multicast groups
- **Router Discovery**: Find multicast-capable routers
- **Efficiency**: Only deliver traffic to interested hosts
- **Dynamic**: Membership changes in real-time

IGMP Versions
-------------
**IGMPv1** (RFC 1112)
  - Basic join functionality
  - Router queries group membership
  - No explicit leave message

**IGMPv2** (RFC 2236)
  - Added leave group messages
  - Faster leave latency
  - Querier election mechanism

**IGMPv3** (RFC 3376)
  - Source filtering (include/exclude)
  - SSM (Source-Specific Multicast) support
  - Multiple source support

Message Types
-------------
**Membership Query** (from router)
  - General Query: "Who wants multicast?"
  - Group-Specific Query: "Who wants group X?"

**Membership Report** (from host)
  - "I want to join group X"
  - Response to queries

**Leave Group** (from host - IGMPv2+)
  - "I'm leaving group X"
  - Allows quick group departure

Multicast Join Process
----------------------
::

    Host                     Router
      |                         |
      |--- IGMP Report -------->| (Join 239.1.1.1)
      |   (Join Group)          |
      |                         |
      |<--- Multicast Stream ---| (Router starts forwarding)
      |                         |
      |<--- IGMP Query ---------| (Periodic membership check)
      |                         |
      |--- IGMP Report -------->| (Still interested)

Common Use Cases
----------------
1. **IPTV**: Set-top boxes joining channel groups
2. **Video Production**: Cameras multicasting to switchers
3. **Stock Market Data**: Financial data feeds
4. **Software Updates**: Enterprise software distribution
5. **Video Conferencing**: Multiparty video streams

💡 Memory Aid
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: IGMP as Newsletter Subscription Service                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of IGMP as a NEWSLETTER SUBSCRIPTION MANAGEMENT SYSTEM:            │
│                                                                           │
│  📰 [Multicast Group] = Newsletter/Magazine                              │
│      239.1.1.1 = "Tech Weekly" magazine                                 │
│      239.1.1.2 = "Finance Daily" newsletter                              │
│                                                                           │
│  📬 [IGMP Report] = Subscription Form                                    │
│      Host fills out: "I want to subscribe to Tech Weekly"               │
│      Delivered to: Local post office (router)                            │
│                                                                           │
│  🏢 [Router] = Post Office Distribution Center                           │
│      Keeps list of who subscribes to what                                │
│      Delivers magazines only to subscribers                              │
│      Doesn't waste resources sending to non-subscribers                  │
│                                                                           │
│  ❌ [IGMP Leave] = Cancellation Form                                     │
│      "Please stop sending me Tech Weekly"                                │
│      Post office removes you from distribution list                      │
│      Saves paper & delivery costs                                        │
│                                                                           │
│  📋 [IGMP Query] = Periodic Survey from Post Office                      │
│      Every 125 seconds: "Do you still want these magazines?"            │
│      If no response: Automatic unsubscribe after 260 seconds             │
│      Keeps subscription list fresh and accurate                          │
│                                                                           │
│  🔍 [IGMP Snooping] = Smart Apartment Mailroom                           │
│      Old way: Deliver magazine to ALL apartments (flooding)              │
│      Smart way: Mailroom listens to subscription forms, delivers only    │
│                 to apartments that subscribed                            │
│                                                                           │
│  The beauty: Multicast efficiency! Send one copy of "Tech Weekly",       │
│  but deliver it to 100 subscribers without making 100 copies upfront.    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📊 Multicast Group Management Visualization
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ IGMP Multicast Join/Leave Flow                                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  JOINING A MULTICAST GROUP (239.1.1.1):                                  │
│  ═══════════════════════════════════════                                 │
│                                                                           │
│  ┌──────────┐                               ┌──────────┐                │
│  │  Host A  │                               │  Router  │                │
│  │          │                               │  (PIM)   │                │
│  └─────┬────┘                               └────┬─────┘                │
│        │                                         │                       │
│   [User launches video player]                  │                       │
│        │                                         │                       │
│   ① App calls: setsockopt(IP_ADD_MEMBERSHIP)    │                       │
│        │                                         │                       │
│        │──── IGMP Report (239.1.1.1) ──────────>│                       │
│        │     Type: 0x16 (IGMPv2 Report)         │                       │
│        │     Group: 239.1.1.1                   │                       │
│        │                                         │                       │
│        │                                    ② Router updates             │
│        │                                      multicast forwarding:       │
│        │                                      (*, 239.1.1.1) → eth0      │
│        │                                         │                       │
│        │<════ Multicast Stream 239.1.1.1 ═══════│                       │
│        │     UDP packets flowing...              │                       │
│        │                                         │                       │
│   [Video playing!]                              │                       │
│        │                                         │                       │
│        │<──── IGMP Query (General) ─────────────│ (every 125 sec)       │
│        │      "Who still wants multicast?"      │                       │
│        │                                         │                       │
│        │──── IGMP Report (239.1.1.1) ──────────>│                       │
│        │     "Yes, still watching!"             │                       │
│        │                                         │                       │
│  ┌─────┴────┐                               ┌────┴─────┐                │
│  │  Host A  │                               │  Router  │                │
│  └──────────┘                               └──────────┘                │
│                                                                           │
│  LEAVING A MULTICAST GROUP:                                              │
│  ═══════════════════════════                                             │
│                                                                           │
│  ┌──────────┐                               ┌──────────┐                │
│  │  Host A  │                               │  Router  │                │
│  └─────┬────┘                               └────┬─────┘                │
│        │                                         │                       │
│   [User closes video player]                    │                       │
│        │                                         │                       │
│   ① App calls: setsockopt(IP_DROP_MEMBERSHIP)   │                       │
│        │                                         │                       │
│        │──── IGMP Leave (239.1.1.1) ───────────>│ (IGMPv2+)             │
│        │     Type: 0x17 (Leave Group)           │                       │
│        │     Group: 239.1.1.1                   │                       │
│        │                                         │                       │
│        │                                    ② Router sends              │
│        │                                      Group-Specific Query:      │
│        │<──── IGMP Query (239.1.1.1) ───────────│ "Anyone else?"        │
│        │                                         │                       │
│        │          [No response = No members]     │                       │
│        │                                         │                       │
│        │                                    ③ Router removes             │
│        │                                      forwarding entry           │
│        │                                      (saves bandwidth)          │
│        │                                         │                       │
│  [Stream stopped]                               │                       │
│        │                                         │                       │
│  ┌─────┴────┐                               ┌────┴─────┐                │
│  │  Host A  │                               │  Router  │                │
│  └──────────┘                               └──────────┘                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ IGMP Packet Structure
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ IGMPv2 Membership Report Packet                                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  IP Header:                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Destination IP: 239.1.1.1 (the group being joined)                  │ │
│  │ TTL: 1 (link-local, not routed beyond this subnet)                  │ │
│  │ Protocol: 2 (IGMP - not TCP/UDP!)                                   │ │
│  │ IP Options: Router Alert (tells router to intercept)                │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  IGMP Payload (8 bytes):                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ Type: 0x16 (IGMPv2 Membership Report)                               │ │
│  │ Max Response Time: 0 (not used in Report)                           │ │
│  │ Checksum: 2 bytes                                                    │ │
│  │ Group Address: 239.1.1.1 (multicast group)                          │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  Total IGMP message: Just 8 bytes! Extremely lightweight.                │
│                                                                           │
│  Common IGMP Types:                                                       │
│  • 0x11: Membership Query (from router)                                  │
│  • 0x16: IGMPv2 Membership Report (from host)                            │
│  • 0x17: IGMPv2 Leave Group (from host)                                  │
│  • 0x22: IGMPv3 Membership Report (source filtering)                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📡 IGMP Snooping Deep Dive
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Without IGMP Snooping vs With Snooping                                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  WITHOUT SNOOPING (Multicast Flooding):                                  │
│  ═══════════════════════════════════════                                 │
│                                                                           │
│              ┌──────────────────────────────────┐                        │
│              │     Layer 2 Switch (Dumb)       │                        │
│              └───┬─────┬─────┬─────┬─────┬─────┘                        │
│                  │     │     │     │     │                               │
│            ┌─────┘     │     │     │     └─────┐                        │
│            ▼           ▼     ▼     ▼           ▼                        │
│          Host A     Host B Host C Host D     Host E                      │
│          📺         ❌    ❌    ❌         ❌                             │
│        (wants      (flood) (flood) (flood)   (flood)                     │
│        stream)                                                            │
│                                                                           │
│  Problem: Switch floods multicast 239.1.1.1 to ALL ports!               │
│  • Host A subscribed, gets stream ✅                                      │
│  • Hosts B,C,D,E get unwanted traffic ❌ (wastes bandwidth)               │
│                                                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                           │
│  WITH IGMP SNOOPING (Smart Forwarding):                                  │
│  ═══════════════════════════════════════                                 │
│                                                                           │
│              ┌──────────────────────────────────┐                        │
│              │   Layer 2 Switch (Smart)        │                        │
│              │   🔍 Listens to IGMP Reports     │                        │
│              └───┬─────┬─────┬─────┬─────┬─────┘                        │
│                  │     │     │     │     │                               │
│            ┌─────┘     │     │     │     └─────┐                        │
│            ▼           ▼     ▼     ▼           ▼                        │
│          Host A     Host B Host C Host D     Host E                      │
│          📺         ✅    ✅    ✅         ✅                             │
│        (wants      (quiet)(quiet)(quiet)   (quiet)                       │
│        stream)                                                            │
│                                                                           │
│  Solution: Switch snoops IGMP Report from Host A                         │
│  • Learns: "Port 1 wants group 239.1.1.1"                               │
│  • Forwards multicast ONLY to Port 1 + router uplink                     │
│  • Ports 2,3,4,5 stay quiet ✅ (bandwidth saved!)                         │
│                                                                           │
│  IGMP Snooping Table Example:                                            │
│  ┌────────────────┬───────────────────────┐                             │
│  │ Multicast Group│ Member Ports          │                             │
│  ├────────────────┼───────────────────────┤                             │
│  │ 239.1.1.1      │ Gi0/1, Gi0/24 (uplink)│                             │
│  │ 239.1.1.2      │ Gi0/3, Gi0/5, Gi0/24  │                             │
│  └────────────────┴───────────────────────┘                             │
│                                                                           │
│  Commands:                                                                │
│  • Cisco: show ip igmp snooping groups                                   │
│  • Linux: bridge mdb show                                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Multicast Address Ranges
------------------------
+------------------------+------------------------------+
| Range                  | Purpose                      |
+========================+==============================+
| 224.0.0.0-224.0.0.255  | Link-local (not routed)      |
| 224.0.1.0-238.255...   | Globally routed              |
| 239.0.0.0-239.255...   | Admin-scoped (organization)  |
+------------------------+------------------------------+

Example: IPTV Scenario
----------------------
Set-top box joining channel::

    1. User selects channel on remote
    2. Set-top box sends IGMP Report for 239.100.1.50
    3. Router adds interface to multicast forwarding table
    4. Video stream delivered to set-top box
    5. User changes channel:
       - IGMP Leave for 239.100.1.50
       - IGMP Join for 239.100.1.51

IGMP Snooping
-------------
Layer 2 switches can "snoop" IGMP messages to:
- Forward multicast only to interested ports
- Prevent multicast flooding
- Improve network efficiency

::

    Without Snooping:     With Snooping:
    Flood to all ports    Forward only to
    (wasteful)            requesting ports

Configuration Example
---------------------
Linux join multicast group::

    # Using ip command
    ip maddr add 239.1.1.1 dev eth0

Cisco router enable multicast::

    ip multicast-routing
    interface GigabitEthernet0/0
      ip pim sparse-mode
      ip igmp version 3

Monitor IGMP membership::

    show ip igmp groups
    show ip igmp interface

Important Timers
----------------
- **Query Interval**: 125 seconds (default)
- **Query Response Time**: 10 seconds
- **Group Membership Interval**: 260 seconds
- **Leave Latency**: ~3 seconds (IGMPv2+)

Troubleshooting
---------------
**Problem**: No multicast received
└─ Check: IGMP enabled on router interface
└─ Check: Multicast routing enabled
└─ Check: Firewall allows IGMP protocol
└─ Verify: Host sending IGMP reports

**Problem**: Multicast flooding LAN
└─ Solution: Enable IGMP snooping on switches

**Problem**: Slow channel changes
└─ Solution: Upgrade to IGMPv2/v3 (faster leave)

Important Notes
---------------
- IGMP is IP protocol 2 (not UDP/TCP)
- Requires multicast routing enabled on routers
- Works with PIM (Protocol Independent Multicast)
- Essential for efficient multicast delivery
- Multicast groups are temporary (leave = cleanup)

🔧 Troubleshooting Guide
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 1: Host Not Receiving Multicast Stream                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • Application fails to receive multicast traffic                         │
│ • Unicast works fine, only multicast broken                              │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Verify host is sending IGMP Reports:                                  │
│    tcpdump -i eth0 igmp                                                   │
│    - Look for "IGMP Membership Report" messages                          │
│    - Destination should be the multicast group (e.g., 239.1.1.1)         │
│                                                                           │
│ 2. Check host has joined multicast group:                                │
│    netstat -g                                                             │
│    ip maddr show dev eth0                                                 │
│    - Should list the multicast group IP                                  │
│                                                                           │
│ 3. Verify router sees IGMP membership:                                   │
│    show ip igmp groups                                                    │
│    show ip igmp interface gi0/1                                           │
│    - Interface should show group membership                              │
│                                                                           │
│ 4. Check multicast routing enabled:                                      │
│    show ip mroute 239.1.1.1                                               │
│    show ip pim neighbor                                                   │
│    - Should show multicast forwarding state                              │
│                                                                           │
│ 5. Verify firewall allows IGMP:                                          │
│    iptables -L -n -v | grep igmp                                          │
│    - Need to allow protocol 2 (IGMP)                                     │
│    iptables -A INPUT -p igmp -j ACCEPT                                    │
│                                                                           │
│ Common Causes:                                                            │
│ • Firewall blocking IGMP protocol                                        │
│ • Multicast routing not enabled: ip multicast-routing                    │
│ • Application not calling setsockopt(IP_ADD_MEMBERSHIP)                  │
│ • Wrong network interface selected for multicast                         │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 2: Multicast Flooding Entire Network                             │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • All switch ports receiving multicast, even non-subscribers             │
│ • Network congestion from unnecessary multicast traffic                  │
│ • Bandwidth saturation                                                    │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Check if IGMP snooping is enabled:                                    │
│    show ip igmp snooping (Cisco)                                          │
│    bridge mdb show (Linux bridge)                                         │
│    - Should show "Snooping enabled" globally or per VLAN                │
│                                                                           │
│ 2. Verify snooping table has entries:                                    │
│    show ip igmp snooping groups                                           │
│    - Should show multicast groups with specific ports                    │
│    - Empty table = flooding                                              │
│                                                                           │
│ 3. Check for snooping querier:                                           │
│    show ip igmp snooping querier                                          │
│    - IGMP querier must exist for snooping to work                        │
│    - Router or switch should send periodic IGMP queries                  │
│                                                                           │
│ 4. Capture switch port to verify selective forwarding:                   │
│    monitor session 1 source interface gi0/5                               │
│    tcpdump -i eth0 dst 239.1.1.1                                          │
│    - Non-member port should NOT see multicast                            │
│                                                                           │
│ Solution:                                                                 │
│ Enable IGMP snooping:                                                     │
│   ip igmp snooping (global)                                               │
│   ip igmp snooping vlan 10 (per-VLAN)                                     │
│                                                                           │
│ Enable IGMP querier (if no multicast router):                            │
│   ip igmp snooping querier                                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 3: Slow Channel Changes in IPTV                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • Channel changes take 10+ seconds                                       │
│ • User experience is poor                                                │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Check IGMP version:                                                   │
│    show ip igmp interface                                                 │
│    - IGMPv1 has NO leave message = slow                                  │
│    - IGMPv2/v3 has explicit leave = fast                                 │
│                                                                           │
│ 2. Check leave latency timer:                                            │
│    show ip igmp interface gi0/1                                           │
│    - Last Member Query Interval: should be ~1 second                     │
│    - Last Member Query Count: should be 2                                │
│    - Total leave latency = Interval × Count (~2-3 sec ideal)             │
│                                                                           │
│ 3. Monitor actual leave time:                                            │
│    tcpdump -i eth0 igmp                                                   │
│    - Watch: IGMP Leave → Query → Stream stops                            │
│    - Measure time between Leave and stream stop                          │
│                                                                           │
│ Solution:                                                                 │
│ Upgrade to IGMPv2 or IGMPv3:                                              │
│   interface gi0/1                                                         │
│     ip igmp version 2                                                     │
│                                                                           │
│ Tune fast-leave timers (IGMPv2):                                         │
│   ip igmp last-member-query-interval 1000 (1 second)                     │
│   ip igmp last-member-query-count 2                                       │
│                                                                           │
│ Enable immediate leave (careful - only for single-host ports):           │
│   ip igmp immediate-leave group-list <acl>                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Problem 4: IGMP State Leaking Across VLANs                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Symptoms:                                                                 │
│ • VLAN 10 devices receiving VLAN 20 multicast                            │
│ • Security concern: multicast isolation broken                           │
│                                                                           │
│ Diagnostic Steps:                                                         │
│ 1. Check IGMP snooping per-VLAN:                                         │
│    show ip igmp snooping vlan 10                                          │
│    show ip igmp snooping vlan 20                                          │
│    - Each VLAN should have separate membership tables                    │
│                                                                           │
│ 2. Verify VLAN isolation for multicast:                                  │
│    show ip igmp snooping groups vlan 10                                   │
│    - Group 239.1.1.1 in VLAN 10 should NOT appear in VLAN 20             │
│                                                                           │
│ 3. Check for multicast router ports:                                     │
│    show ip igmp snooping mrouter                                          │
│    - Multicast router ports may forward across VLANs if misconfigured    │
│                                                                           │
│ 4. Verify inter-VLAN routing for multicast:                              │
│    show ip mroute                                                         │
│    - Check if multicast is being routed between VLANs unintentionally    │
│                                                                           │
│ Solution:                                                                 │
│ Enable per-VLAN IGMP snooping:                                            │
│   ip igmp snooping vlan 10                                                │
│   ip igmp snooping vlan 20                                                │
│                                                                           │
│ Restrict multicast routing between VLANs:                                 │
│   ip access-list standard BLOCK_MCAST_CROSS_VLAN                          │
│     deny 239.0.0.0 0.255.255.255                                          │
│     permit any                                                            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ Quick IGMP Diagnostics
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Essential Commands                                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Host-Side Commands:                                                       │
│   netstat -g                          # Show multicast memberships       │
│   ip maddr show                       # Show multicast addresses         │
│   ip maddr add 239.1.1.1 dev eth0     # Manually join group              │
│   ip maddr del 239.1.1.1 dev eth0     # Leave group                      │
│                                                                           │
│ Router Commands (Cisco):                                                  │
│   show ip igmp groups                 # Show group memberships           │
│   show ip igmp interface              # Show IGMP per interface          │
│   show ip mroute                      # Show multicast routing table     │
│   show ip pim neighbor                # Show PIM neighbors               │
│                                                                           │
│ Switch Commands (IGMP Snooping):                                          │
│   show ip igmp snooping                     # Snooping status            │
│   show ip igmp snooping groups              # Group membership table     │
│   show ip igmp snooping mrouter             # Multicast router ports     │
│   show ip igmp snooping querier             # Querier info               │
│                                                                           │
│ Linux Bridge (IGMP Snooping):                                             │
│   bridge mdb show                     # Multicast database               │
│   bridge link show                    # Show bridge ports                │
│                                                                           │
│ Packet Captures:                                                          │
│   tcpdump -i eth0 igmp                      # Capture all IGMP           │
│   tcpdump -i eth0 'igmp[0] == 0x16'         # Only IGMP Reports          │
│   tcpdump -i eth0 dst 239.1.1.1             # Capture multicast group    │
│   tcpdump -i eth0 'ip[9] == 2'              # IGMP (protocol 2)          │
│                                                                           │
│ Wireshark Filters:                                                        │
│   igmp                                # All IGMP traffic                 │
│   igmp.type == 0x16                   # Membership Reports               │
│   igmp.type == 0x11                   # Membership Queries               │
│   ip.dst == 239.1.1.1                 # Specific multicast group         │
│                                                                           │
│ Multicast Group Test:                                                     │
│   Sender: ffmpeg -re -i video.mp4 -f mpegts udp://239.1.1.1:5000         │
│   Receiver: ffplay udp://@239.1.1.1:5000                                  │
│   - @ symbol tells ffplay to join multicast group                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘
