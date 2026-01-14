═══════════════════════════════════════════════════════════════════════════════
⏱️ PTP - Precision Time Protocol (IEEE 1588)
═══════════════════════════════════════════════════════════════════════════════

Overview
───────────────────────────────────────────────────────────────────────────────
IEEE 1588 Precision Time Protocol (PTP) is a network protocol designed to
synchronize clocks across distributed systems with sub-microsecond accuracy.
First published in 2002 and revised in 2008 (version 2, IEEE 1588-2008) and 2019
(IEEE 1588-2019), PTP enables devices on a packet-based network to maintain
precise time alignment without expensive GPS receivers or specialized timing
infrastructure at every location.

PTP uses a master-slave hierarchy where a grandmaster clock provides the reference
time, and slave devices synchronize to it through bidirectional message exchanges
that account for network propagation delay. This makes PTP essential for applications
requiring tight synchronization like professional audio/video production (SMPTE 2110),
telecommunications (5G), financial trading, industrial automation, and distributed
control systems. Modern implementations achieve accuracy better than 1 microsecond
on standard Ethernet networks, and sub-100 nanoseconds with hardware timestamping.

Key Features
───────────────────────────────────────────────────────────────────────────────
- Sub-microsecond accuracy: Typical <1 µs with hardware timestamping
- Self-organizing: Automatic best master clock (BMC) selection
- Scalable hierarchy: Master-slave architecture with boundary/transparent clocks
- Network agnostic: Works over Ethernet, UDP/IPv4, UDP/IPv6
- Hardware timestamping: PHY-level timestamps for maximum precision
- Delay measurement: Accounts for asymmetric network paths
- Profile-based: Domain-specific profiles (default, power, telecom, media)
- Fault tolerance: Automatic failover to backup grandmaster
- Transparent to applications: Synchronizes system clock
- IEEE standard: Vendor-neutral, interoperable

PTP Clock Types
───────────────────────────────────────────────────────────────────────────────
Grandmaster Clock (GM):
- Root time source for PTP domain
- Highest priority clock in Best Master Clock Algorithm (BMCA)
- Often GPS-synchronized or atomic clock reference
- Provides reference time to all slaves

Ordinary Clock (OC):
- Single PTP port (master or slave)
- End devices: cameras, audio interfaces, servers

Boundary Clock (BC):
- Multiple PTP ports
- Slave on one port (to upstream), master on others (to downstream)
- Segments network, improves scalability
- Regenerates PTP messages

Transparent Clock (TC):
- Measures packet residence/transit time
- Two types:
  * End-to-End (E2E): Adds residence time to correction field
  * Peer-to-Peer (P2P): Measures link delay between neighbors
- Improves accuracy without full boundary clock complexity

Common Use Cases
───────────────────────────────────────────────────────────────────────────────
1. Professional media production (SMPTE ST 2110 IP video/audio)
2. Broadcast facilities synchronization
3. 5G mobile network fronthaul/backhaul timing
4. Financial trading systems (high-frequency trading)
5. Industrial automation and process control
6. Power grid substations (IEC 61850)
7. Test and measurement equipment synchronization
8. Distributed sensor networks
9. Audio/video streaming and mixing
10. Scientific data acquisition systems

💡 Memory Aid
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: PTP as Orchestra Conductor                             │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of a PTP network as an ORCHESTRA:                                 │
│                                                                           │
│  🎼 [Grandmaster Clock] = CONDUCTOR with a metronome                     │
│     Sets the tempo (time reference) for everyone                         │
│     Has the "master score" (GPS/atomic clock)                            │
│                                                                           │
│  🎻 [Slave Devices] = MUSICIANS                                          │
│     Watch the conductor to stay in sync                                  │
│     Ask: "Am I ahead or behind?" (Delay_Req)                             │
│     Conductor answers: "You're 250 nanoseconds late!" (Delay_Resp)      │
│                                                                           │
│  📯 [Boundary Clocks] = SECTION LEADERS                                  │
│     Violin section leader watches conductor, other violins watch leader  │
│     Reduces load on conductor (scales better)                            │
│                                                                           │
│  📝 [Transparent Clocks] = SOUND DELAY COMPENSATORS                      │
│     "Sound traveled 50 meters, add 147 ms delay compensation"            │
│     Helps musicians in back rows stay perfectly synchronized             │
│                                                                           │
│  🎵 The Result: PERFECT SYNCHRONIZATION                                  │
│     Everyone plays in perfect time, down to the MICROSECOND!             │
│                                                                           │
│  PTP's magic: The conductor's baton moves at the SPEED OF LIGHT          │
│  (well, almost - we just compensate for network delay!)                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

⚡ Clock Hierarchy Visualization
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ PTP Network Topology Examples                                            │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  SIMPLE NETWORK (Ordinary Clocks only):                                  │
│                                                                           │
│         ┌─────────────────────┐                                          │
│         │  📡 GRANDMASTER GM  │  ← GPS/Atomic reference                 │
│         │  (Clock Class 6)    │     Priority1=128                        │
│         │  Accuracy: ±100ns   │     Domain: 127                          │
│         └──────────┬──────────┘                                          │
│                    │ Sync, Follow_Up, Announce                           │
│          ┌─────────┼─────────┬─────────┐                                │
│          │         │         │         │                                 │
│          ↓         ↓         ↓         ↓                                 │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                     │
│    │ SLAVE 1 │ │ SLAVE 2 │ │ SLAVE 3 │ │ SLAVE 4 │                     │
│    │ Camera  │ │  Audio  │ │ Recorder│ │ Monitor │                     │
│    │ +2.3µs  │ │ -1.8µs  │ │ +0.5µs  │ │ -3.1µs  │ ← Offset from GM  │
│    └─────────┘ └─────────┘ └─────────┘ └─────────┘                     │
│          │         │         │         │                                 │
│          └─────────┴─────────┴─────────┘                                │
│                    Delay_Req ↑                                           │
│                    Delay_Resp ↓                                          │
│                                                                           │
│  Limitations: All slaves talk to one GM, doesn't scale beyond ~50 slaves│
│                                                                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  SCALED NETWORK (with Boundary Clocks):                                 │
│                                                                           │
│              ┌─────────────────────┐                                     │
│              │  📡 GRANDMASTER GM  │                                     │
│              │  GPS-Synchronized   │                                     │
│              │  ±25 ns accuracy    │                                     │
│              └──────────┬──────────┘                                     │
│                         │                                                │
│        ┌────────────────┼────────────────┐                              │
│        │                │                │                               │
│        ↓                ↓                ↓                               │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                        │
│  │ BC-1     │     │ BC-2     │     │ BC-3     │ ← Boundary Clocks      │
│  │ Studio A │     │ Studio B │     │  OB Van  │   (Master on downlink) │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘                        │
│       │ Master         │ Master         │ Master                        │
│   ┌───┼───┐        ┌───┼───┐        ┌───┼───┐                          │
│   ↓   ↓   ↓        ↓   ↓   ↓        ↓   ↓   ↓                          │
│  S1  S2  S3       S4  S5  S6       S7  S8  S9                          │
│  📹  🎤  📺       📹  🎤  📺       📹  🎤  📺                          │
│                                                                           │
│  Benefits:                                                               │
│   • Each BC synchronizes <10 slaves (manageable)                         │
│   • BCs segment network (reduced traffic per segment)                    │
│   • Total slaves: Nearly unlimited with proper BC placement              │
│                                                                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  REDUNDANT NETWORK (Failover):                                           │
│                                                                           │
│     ┌─────────────┐           ┌─────────────┐                           │
│     │   GM-1      │           │   GM-2      │                           │
│     │ Priority1=64│ ✅ ACTIVE │ Priority1=128│ 🔄 STANDBY             │
│     │ GPS Lock ✓  │           │ GPS Lock ✓  │                           │
│     └──────┬──────┘           └──────┬──────┘                           │
│            │                         │                                   │
│            └────────┬────────────────┘                                   │
│                     │                                                    │
│                ┌────┴────┐                                               │
│                │ Network │                                               │
│                └────┬────┘                                               │
│                     │                                                    │
│          ┌──────────┼──────────┐                                        │
│          ↓          ↓          ↓                                         │
│       Slave1     Slave2     Slave3                                       │
│                                                                           │
│  Failover Scenario:                                                      │
│   1. GM-1 loses GPS → Clock Class degrades                               │
│   2. BMCA detects GM-2 is now better (has GPS)                           │
│   3. All slaves automatically switch to GM-2                             │
│   4. Switchover time: ~2-5 seconds typical                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

📊 PTP Message Exchange Deep Dive
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Two-Step Synchronization (Most Common)                                   │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  MASTER                                   SLAVE                          │
│  (Grandmaster)                            (Camera)                       │
│     │                                        │                            │
│     │  ①  Sync                               │                            │
│     ├────────────────────────────────────────>                           │
│     │    Timestamp: t1 (approx)              │                            │
│     │                                        │ Receives at t2             │
│     │                                        │ (local clock)              │
│     │                                        │                            │
│     │  ②  Follow_Up                          │                            │
│     ├────────────────────────────────────────>                           │
│     │    Contains: t1_precise                │                            │
│     │    (exact HW timestamp)                │ Now slave knows:           │
│     │                                        │  t1 = master TX time       │
│     │                                        │  t2 = slave RX time        │
│     │                                        │                            │
│     │                                        │ But wait! Need to know     │
│     │                                        │ network delay to calculate │
│     │                                        │ true offset...             │
│     │                                        │                            │
│     │                   ③  Delay_Req         │                            │
│     <────────────────────────────────────────┤                           │
│     │                   Sent at t3           │                            │
│ Receives at t4                               │                            │
│ (local clock)                                │                            │
│     │                                        │                            │
│     │  ④  Delay_Resp                         │                            │
│     ├────────────────────────────────────────>                           │
│     │    Contains: t4                        │                            │
│     │    (when master RX'd Delay_Req)        │                            │
│     │                                        │ Now slave knows all 4      │
│     │                                        │ timestamps!                │
│     │                                        │                            │
│     │                                        │ ⚙️  CALCULATION:           │
│     │                                        │                            │
│     │                                        │ Forward path delay:        │
│     │                                        │   d_fwd = t2 - t1          │
│     │                                        │                            │
│     │                                        │ Reverse path delay:        │
│     │                                        │   d_rev = t4 - t3          │
│     │                                        │                            │
│     │                                        │ Mean path delay:           │
│     │                                        │   delay = (d_fwd + d_rev)/2│
│     │                                        │                            │
│     │                                        │ Clock offset:              │
│     │                                        │   offset = d_fwd - delay   │
│     │                                        │   offset = (t2-t1-t4+t3)/2 │
│     │                                        │                            │
│     │                                        │ ✅ Adjust local clock by   │
│     │                                        │    offset!                 │
│     │                                        │                            │
│  Repeat every 1 second (default Sync interval)                           │
│                                                                           │
├───────────────────────────────────────────────────────────────────────────┤
│ Example with Real Numbers:                                               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Master clock:  10:00:00.000000000 (absolute time)                       │
│  Slave clock:   10:00:00.000002500 (2.5 µs fast!)                        │
│                                                                           │
│  t1 = Master TX Sync:        10:00:00.000000000                          │
│  t2 = Slave RX Sync:         10:00:00.000002700 ← includes 200ns delay  │
│  t3 = Slave TX Delay_Req:    10:00:00.000003000                          │
│  t4 = Master RX Delay_Req:   10:00:00.000000700 ← includes 200ns delay  │
│                                                                           │
│  d_fwd = t2 - t1 = 2700 ns                                               │
│  d_rev = t4 - t3 = -2300 ns (negative because slave clock fast)          │
│                                                                           │
│  delay = (2700 - 2300) / 2 = 200 ns                                      │
│  offset = 2700 - 200 = 2500 ns = 2.5 µs                                  │
│                                                                           │
│  🔧 Slave adjusts clock: -2500 ns                                         │
│     New slave time: 10:00:00.000000000 ← SYNCHRONIZED! ✅                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Technical Specifications
───────────────────────────────────────────────────────────────────────────────
Message Types:
- Sync: Master sends periodic time stamps
- Follow_Up: Contains precise Sync transmission time (two-step)
- Delay_Req: Slave requests delay measurement
- Delay_Resp: Master responds with delay information
- Announce: Grandmaster capabilities and clock quality
- Management: Configuration and monitoring
- Signaling: Unicast negotiation

Two-Step vs One-Step:
Two-Step:
- Sync message sent first
- Follow_Up contains precise timestamp after transmission
- More common, easier to implement

One-Step:
- Timestamp embedded in Sync message at transmission
- Requires hardware support
- Lower latency, higher accuracy

Message Exchange (Delay Request-Response):
1. Master → Slave: Sync (t1 = master TX time)
2. Master → Slave: Follow_Up (contains precise t1)
3. Slave → Master: Delay_Req (t2 = slave RX time, t3 = slave TX time)
4. Master → Slave: Delay_Resp (t4 = master RX time)

Offset Calculation:
- Offset = [(t2 - t1) - (t4 - t3)] / 2
- Delay = [(t2 - t1) + (t4 - t3)] / 2

Slave adjusts local clock based on calculated offset.

PTP Domains
───────────────────────────────────────────────────────────────────────────────
Domain Number (0-255):
- Isolates PTP instances on same network
- Default domain = 0
- Media domain (SMPTE) = 127
- Allows multiple independent timing domains

PTP Profiles
───────────────────────────────────────────────────────────────────────────────
Default Profile:
- General-purpose profile
- Multicast or unicast communication
- Ethernet or UDP/IP transport

Power Profile (IEEE C37.238):
- Electric power substation timing
- <1 µs accuracy requirement
- Peer-to-peer delay mechanism

Telecom Profile (ITU-T G.8265.1, G.8275.1/2):
- Mobile network synchronization (4G/5G)
- Frequency and phase/time sync
- Hierarchical architecture

Media Profile (SMPTE ST 2059):
- Broadcast and professional media
- Domain 127
- <1 µs accuracy
- Integrates with SMPTE 2110 AV-over-IP

Best Master Clock Algorithm (BMCA)
───────────────────────────────────────────────────────────────────────────────
Selects best grandmaster based on:
1. Priority 1 (0-255, lower is better, admin configured)
2. Clock class (GPS, atomic, free-running)
3. Clock accuracy (nanoseconds)
4. Variance (stability)
5. Priority 2 (tiebreaker)
6. Clock identity (MAC-based unique ID)

Automatic failover:
- If grandmaster fails, BMCA elects new GM
- Slaves automatically switch to new master

Hardware vs Software Timestamping
───────────────────────────────────────────────────────────────────────────────
Hardware Timestamping (Recommended):
- Timestamps applied at PHY layer
- Eliminates OS/driver jitter
- Accuracy: <100 ns typical
- Requires NIC support (Intel i210, i350, Mellanox, etc.)

Software Timestamping:
- Timestamps in kernel or user space
- Subject to OS scheduling delays
- Accuracy: 10-100 µs typical
- Works with any NIC

Transport
───────────────────────────────────────────────────────────────────────────────
Layer 2 (Ethernet):
- EtherType: 0x88F7
- Multicast MAC: 01:1B:19:00:00:00 (general)
- Lower overhead, better accuracy
- Limited to single broadcast domain

Layer 3 (UDP/IP):
- UDP ports: 319 (event), 320 (general)
- Multicast IPv4: 224.0.1.129, 224.0.0.107
- Routable across IP networks
- Slightly lower accuracy due to IP stack overhead

Configuration Example (Linux)
───────────────────────────────────────────────────────────────────────────────
Grandmaster:
  ptp4l -i eth0 -m -H -P 1

Slave:
  ptp4l -i eth0 -m -H -s
  phc2sys -a -rr

Options:
- -i eth0: Network interface
- -m: Print messages to stdout
- -H: Hardware timestamping
- -P 1: Priority 1
- -s: Slave only
- phc2sys: Synchronizes system clock to PTP Hardware Clock (PHC)

Monitoring
───────────────────────────────────────────────────────────────────────────────
Key Metrics:
- Offset from master: Current time error (ns/µs)
- Path delay: Network propagation time
- Sync interval: Rate of synchronization messages (default 1/sec)
- Announce interval: Grandmaster advertisement rate
- Clock class/accuracy: Grandmaster quality indicators

Tools:
- ptp4l: Linux PTP daemon
- phc_ctl: PHC control utility
- pmc: PTP management client
- ethtool -T: Check NIC timestamping capabilities
- ptpstat: PTP status monitoring

Challenges
───────────────────────────────────────────────────────────────────────────────
- Asymmetric network delays: Degrades accuracy if TX/RX paths differ
- Packet delay variation (PDV): Switch queuing, congestion
- Non-PTP-aware switches: Add variable delay
- Clock drift: Hardware oscillator stability
- Temperature effects: Clock frequency changes with temperature
- Network topology changes: Can disrupt synchronization

⚙️ Hardware vs Software Timestamping Comparison
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Where Timestamps Are Applied                                             │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  SOFTWARE TIMESTAMPING (Bad for PTP):                                    │
│                                                                           │
│   ┌─────────────┐                                                        │
│   │ Application │                                                        │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐     ⏱️ Software timestamp here                        │
│   │   Kernel    │     (subject to scheduling delays)                    │
│   │ Network Stack│    ❌ Jitter: 10-100 µs                               │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │   Driver    │                                                        │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │  NIC (MAC)  │                                                        │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │  PHY Layer  │                                                        │
│   └──────┬──────┘                                                        │
│          ↓                                                               │
│     [Network Wire]                                                       │
│                                                                           │
│  ════════════════════════════════════════════════════════════════════     │
│                                                                           │
│  HARDWARE TIMESTAMPING (Good for PTP!):                                  │
│                                                                           │
│   ┌─────────────┐                                                        │
│   │ Application │                                                        │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │   Kernel    │                                                        │
│   │ Network Stack│                                                       │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │   Driver    │                                                        │
│   └──────┬──────┘                                                        │
│          │                                                               │
│   ┌──────▼──────┐                                                        │
│   │  NIC (MAC)  │     ⏱️ Hardware timestamp at PHY!                      │
│   └──────┬──────┘    ✅ Precise, no OS jitter                            │
│          │           ✅ Accuracy: <100 ns                                 │
│   ┌──────▼──────┐                                                        │
│   │  PHY Layer  │◄─── PTP-aware hardware                                │
│   │  (PTP HW)   │     Captures exact TX/RX time                          │
│   └──────┬──────┘     Stores in register                                 │
│          ↓                                                               │
│     [Network Wire]                                                       │
│                                                                           │
│  Check NIC support: ethtool -T eth0                                      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Supported NICs (Hardware Timestamping)                                   │
├───────────────────────────────────────────────────────────────────────────┤
│  ✅ Intel i210, i350, i211, 82580, X710                                   │
│  ✅ Mellanox ConnectX-4, ConnectX-5, ConnectX-6                           │
│  ✅ Marvell Alaska 88E1512                                                │
│  ✅ Broadcom BCM5719                                                      │
│  ✅ Solarflare (Xilinx) SFN series                                        │
│  ✅ Many embedded SoCs (TI Sitara, Xilinx Zynq, NXP i.MX)                 │
│                                                                           │
│  ❌ Realtek (most consumer NICs) - software timestamping only             │
│  ❌ USB Ethernet adapters - generally no hardware timestamping            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

🔧 Troubleshooting Guide
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Large offset (>10 µs) or unstable synchronization               │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Check hardware timestamping enabled:                                   │
│   $ ethtool -T eth0 | grep hardware                                      │
│   Should show: hardware-transmit, hardware-receive                       │
│                                                                           │
│ ✓ Verify ptp4l using hardware mode:                                      │
│   ptp4l -i eth0 -m -H     ← -H flag forces hardware timestamping        │
│                                                                           │
│ ✓ Check NIC driver supports PTP:                                         │
│   lsmod | grep ptp                                                       │
│   Should see: ptp, ptp_pch, or similar                                   │
│                                                                           │
│ ✓ Asymmetric network paths: TX/RX taking different routes                │
│   - Use peer-to-peer delay mechanism (P2P) instead of E2E                │
│   - Ensure symmetric network topology                                    │
│                                                                           │
│ ✓ Network congestion adding jitter:                                      │
│   - Enable QoS/DSCP for PTP packets (DSCP EF or CS7)                     │
│   - Use dedicated management VLAN                                        │
│   - Check switch queue depths                                            │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: No synchronization / offset always 0 or never changes           │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Verify PTP domain matches between master and slave:                    │
│   Master: ptp4l -i eth0 -m -H -P 1 -D 127  ← Domain 127                 │
│   Slave:  ptp4l -i eth0 -m -H -s -D 127    ← Must match!                │
│                                                                           │
│ ✓ Check firewall not blocking PTP:                                       │
│   - UDP ports 319 (event) and 320 (general) must be open                │
│   - Layer 2 mode: EtherType 0x88F7                                       │
│   $ iptables -L | grep 319                                               │
│                                                                           │
│ ✓ Multicast not reaching slave:                                          │
│   $ tcpdump -i eth0 port 319 or port 320                                │
│   Should see Sync, Follow_Up, Announce messages                          │
│                                                                           │
│ ✓ IGMP snooping blocking multicast:                                      │
│   - Disable IGMP snooping for PTP VLAN, OR                               │
│   - Configure IGMP querier properly                                      │
│                                                                           │
│ ✓ Slave in master-only mode:                                             │
│   Ensure -s flag present for slave mode                                  │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Synchronization works but system clock not synchronized         │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ phc2sys not running:                                                   │
│   ptp4l synchronizes PHC (PTP Hardware Clock in NIC)                     │
│   phc2sys copies PHC → system clock                                      │
│                                                                           │
│   Start phc2sys:                                                         │
│   $ phc2sys -a -rr                                                       │
│     -a = automatic (find PHC device)                                     │
│     -rr = realtime priority                                              │
│                                                                           │
│ ✓ Check PHC offset from system clock:                                    │
│   $ phc_ctl /dev/ptp0 cmp                                                │
│   Shows: phc offset: XXXX ns                                             │
│                                                                           │
│ ✓ Verify system time after sync:                                         │
│   $ date; cat /sys/class/ptp/ptp0/clock_name                            │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ Problem: Grandmaster failover not working                                │
├───────────────────────────────────────────────────────────────────────────┤
│ ✓ Check Priority1 settings:                                              │
│   Primary GM:   Priority1 = 64 (lower = better)                          │
│   Backup GM:    Priority1 = 128                                          │
│   If equal, BMCA uses Clock Class, Accuracy, Variance                    │
│                                                                           │
│ ✓ Verify Announce messages:                                              │
│   $ pmc -u -b 0 'GET CURRENT_DATA_SET'                                   │
│   Shows active grandmaster clockIdentity                                 │
│                                                                           │
│ ✓ Announce interval too long:                                            │
│   Default: 1 second, increase frequency for faster failover              │
│   ptp4l -i eth0 -m -H --announceInterval -1  ← 2^(-1) = 0.5s            │
│                                                                           │
│ ✓ Slaves not receiving Announce from backup:                             │
│   Ensure backup GM configured as master (not slave-only)                 │
└───────────────────────────────────────────────────────────────────────────┘

⚡ Quick Diagnostic Commands
───────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────┐
│ Check NIC Hardware Timestamping Support:                                 │
│   $ ethtool -T eth0                                                      │
│   Look for: SOF_TIMESTAMPING_TX_HARDWARE, SOF_TIMESTAMPING_RX_HARDWARE   │
│                                                                           │
│ Monitor PTP Status:                                                      │
│   $ ptp4l -i eth0 -m -H -s                                               │
│   Watch: offset from master, path delay                                  │
│                                                                           │
│ Check Current Grandmaster:                                               │
│   $ pmc -u -b 0 'GET CURRENT_DATA_SET'                                   │
│   $ pmc -u -b 0 'GET PARENT_DATA_SET'                                    │
│                                                                           │
│ Verify System Clock Sync:                                                │
│   $ phc2sys -a -rr -m                                                    │
│   Watch: sys offset                                                      │
│                                                                           │
│ Capture PTP Traffic:                                                     │
│   $ tcpdump -i eth0 -vv ether proto 0x88F7                               │
│   $ tcpdump -i eth0 -vv port 319 or port 320                            │
│                                                                           │
│ Check PTP PHC Device:                                                    │
│   $ ls -l /dev/ptp*                                                      │
│   $ cat /sys/class/ptp/ptp0/clock_name                                   │
└───────────────────────────────────────────────────────────────────────────┘

Important Notes
───────────────────────────────────────────────────────────────────────────────
- Hardware timestamping essential for <1 µs accuracy
- PTP-aware switches improve accuracy by handling PTP messages specially
- GPS provides absolute time reference; PTP distributes it across network
- Use boundary clocks to segment large networks and reduce slave count per GM
- Monitor offset and path delay to detect synchronization issues
- IEEE 1588-2019 (v2.1) adds security, enhanced profiles, and performance improvements
- Not all NICs support hardware timestamping; check with `ethtool -T`
- Requires low-latency network; QoS/traffic shaping recommended
- Multicast mode simpler but less scalable than unicast negotiation
- Used in conjunction with NTP for systems requiring both precision and wide-area sync
