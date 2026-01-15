🌐 **ARINC 664 - Aircraft Ethernet (AFDX)**
═══════════════════════════════════════════

**Last Updated:** January 2026  
**Target Role:** Aircraft Services Architect  
**Relevance:** Primary network for A350, 787, 737 MAX IFE & avionics

════════════════════════════════════════════════════════════════════

📋 **TABLE OF CONTENTS**
────────────────────────

1. Overview & Context
2. AFDX Architecture
3. Virtual Links (VL)
4. Part 7 vs Part 10
5. Network Segregation
6. Quality of Service (QoS)
7. Bandwidth Allocation
8. Redundancy & Reliability
9. Configuration Management
10. Integration with IFE
11. Practical Examples
12. Common Pitfalls
13. Quick Reference Card
14. Exam Questions
15. Further Reading

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — Quick Takeaways**
──────────────────────────────

✅ **AFDX** = Avionics Full-Duplex Switched Ethernet (deterministic 100 Mbps)  
✅ **Virtual Links (VL)** = guaranteed bandwidth channels (BAG = 1-128 ms)  
✅ **Part 7** (safety-critical avionics) vs. **Part 10** (non-critical passenger services)  
✅ **Redundancy**: Dual networks (Network A + Network B) for fault tolerance  
✅ **Segregation**: Flight-critical, IFE, maintenance on separate VLANs  
✅ **Jitter**: <500 µs for avionics, <1 ms for IFE acceptable  
✅ **No collisions**: Full-duplex switched (unlike legacy CSMA/CD Ethernet)

════════════════════════════════════════════════════════════════════

🏢 **1. OVERVIEW & CONTEXT**
────────────────────────────

**What is ARINC 664?**

ARINC 664 defines **deterministic Ethernet** for aircraft systems, replacing:
- **ARINC 429** (slow, 12.5-100 kbps)
- **MIL-STD-1553** (1 Mbps bus)
- **ARINC 629** (2 Mbps linear bus)

**Key Differences from Standard Ethernet:**

+---------------------------+---------------------------+
| Standard Ethernet         | AFDX (ARINC 664)          |
+===========================+===========================+
| CSMA/CD (collisions)      | Full-duplex switched      |
| Best-effort delivery      | Guaranteed bandwidth (VL) |
| Variable latency          | Bounded jitter (<500 µs)  |
| Broadcast storms possible | Traffic shaping per VL    |
| 10/100/1000 Mbps          | Fixed 100 Mbps            |
+---------------------------+---------------------------+

**Aircraft Usage:**

✈️ **Airbus A350, A380**: 150+ End Systems (ES)  
✈️ **Boeing 787**: 100+ ES  
✈️ **Boeing 737 MAX**: 50+ ES (hybrid with ARINC 429)

════════════════════════════════════════════════════════════════════

🏗️ **2. AFDX ARCHITECTURE**
────────────────────────────

**Network Topology:**

::

   Flight Control      IFE Head-End       Maintenance
   Computer (FCC)      Server             Terminal
        │                   │                  │
        │                   │                  │
   ┌────▼──────────────────▼──────────────────▼────┐
   │            AFDX Switch (Redundant A)           │
   └────┬──────────────────┬──────────────────┬────┘
        │                  │                  │
   VL 1 (FCC→FCC)     VL 100 (IFE)      VL 200 (Maint)
        │                  │                  │
   ┌────▼──────────────────▼──────────────────▼────┐
   │            AFDX Switch (Redundant B)           │
   └────┬──────────────────┬──────────────────┬────┘
        │                   │                  │
   Autopilot         IFE Seat Screens     EFB Tablets

**Components:**

1. **End Systems (ES)**:
   - Transmit/receive AFDX frames
   - Connect to both Network A & B
   - Example: Flight Management Computer (FMC)

2. **AFDX Switches**:
   - Store-and-forward (no collisions)
   - Traffic shaping (BAG enforcement)
   - VLAN tagging (802.1Q)

3. **Virtual Links (VL)**:
   - Logical channels (VL ID: 1-32767)
   - Unidirectional (source → destination)
   - Bandwidth guaranteed by BAG

════════════════════════════════════════════════════════════════════

🔗 **3. VIRTUAL LINKS (VL)**
────────────────────────────

**What is a Virtual Link?**

A **VL** is a logical connection from 1 source to 1+ destinations with:
- **Guaranteed bandwidth** (Bandwidth Allocation Gap)
- **Bounded latency** (max 3 ms for critical data)
- **Isolated traffic** (no interference between VLs)

**VL Parameters:**

+------------------+----------------------------------+
| Parameter        | Description                      |
+==================+==================================+
| **VL ID**        | Unique identifier (1-32767)      |
| **BAG**          | Min time between frames (1-128ms)|
| **Max Frame Size**| Typically 1518 bytes            |
| **Source**       | Single ES MAC address            |
| **Destination(s)**| Multicast MAC (up to 256 ES)    |
+------------------+----------------------------------+

**BAG (Bandwidth Allocation Gap):**

BAG defines **minimum transmission interval**:
- BAG = 1 ms → Max 1000 frames/sec
- BAG = 128 ms → Max ~7.8 frames/sec

.. code-block:: text

   Time →
   ├──BAG(1ms)──┼──BAG(1ms)──┼──BAG(1ms)──┼
   [Frame 1]    [Frame 2]    [Frame 3]

**Example VL Configuration:**

.. code-block:: xml

   <VirtualLink>
     <VL_ID>100</VL_ID>
     <Source_ES>FCC1</Source_ES>
     <Destinations>
       <ES>Autopilot_1</ES>
       <ES>Autopilot_2</ES>
     </Destinations>
     <BAG>4</BAG>  <!-- 4 ms -->
     <MaxFrameSize>1024</MaxFrameSize>
     <VLAN_ID>10</VLAN_ID>  <!-- Flight-critical domain -->
   </VirtualLink>

════════════════════════════════════════════════════════════════════

📦 **4. PART 7 vs PART 10**
───────────────────────────

**ARINC 664 Part 7 (AFDX)**

- **Safety-critical** avionics
- **DAL A/B** systems (flight control, navigation)
- **Deterministic** (guaranteed latency)
- **Redundant networks** (A + B)
- **No IP protocol** (raw Ethernet frames)

**Example Systems:**
- Flight Control Computers (FCC)
- Air Data Inertial Reference System (ADIRS)
- Engine FADEC communication

**ARINC 664 Part 10 (ARINC 664 P10)**

- **Non-safety-critical** (IFE, passenger Wi-Fi)
- **DAL D/E** systems
- **IP-based** (TCP/IP, UDP/IP allowed)
- **Single network** (redundancy optional)
- **Higher bandwidth** (up to 1 Gbps)

**Comparison Table:**

+---------------------+------------------+------------------+
| Feature             | Part 7 (AFDX)    | Part 10 (P10)    |
+=====================+==================+==================+
| **Safety Level**    | DAL A/B          | DAL D/E          |
| **Protocol**        | Raw Ethernet     | IP/TCP/UDP       |
| **Redundancy**      | Mandatory (A+B)  | Optional         |
| **Bandwidth**       | 100 Mbps         | 100 Mbps - 1 Gbps|
| **Jitter**          | <500 µs          | <10 ms OK        |
| **Use Case**        | Avionics         | IFE, Passenger   |
+---------------------+------------------+------------------+

**Isolation Between Part 7 & Part 10:**

::

   ┌─────────────────────────────────────────────┐
   │         Aircraft Network Backbone           │
   ├─────────────────┬───────────────────────────┤
   │  AFDX (Part 7)  │   P10 (Part 10)           │
   │  VLAN 1-100     │   VLAN 1000-2000          │
   │  Flight Control │   IFE, Wi-Fi, Cabin       │
   │  Navigation     │   Crew Tablets            │
   └─────────────────┴───────────────────────────┘
         │                      │
   Physical isolation    Firewall / ACL

════════════════════════════════════════════════════════════════════

🔒 **5. NETWORK SEGREGATION**
──────────────────────────────

**Domain Separation (VLANs):**

+-------------+-------------------+------------------+---------+
| VLAN ID     | Domain            | Systems          | DAL     |
+=============+===================+==================+=========+
| **10-50**   | Flight-critical   | FCC, ADIRS, FMS  | A/B     |
| **100-200** | Cabin systems     | ECS, Lighting    | C/D     |
| **1000+**   | Passenger (IFE)   | Movies, Wi-Fi    | E       |
| **2000+**   | Maintenance       | EFB, Diagnostics | E       |
+-------------+-------------------+------------------+---------+

**Firewall Rules (Example):**

.. code-block:: text

   # Allow FCC (VLAN 10) to communicate with Autopilot (VLAN 10)
   permit vlan 10 to vlan 10
   
   # Deny IFE (VLAN 1000) from accessing flight-critical (VLAN 10)
   deny vlan 1000 to vlan 10
   
   # Allow maintenance (VLAN 2000) read-only to all (with auth)
   permit vlan 2000 to vlan * [read-only, authenticated]

**Physical Segregation:**

- **Separate cables** for flight-critical vs. passenger
- **Dedicated switches** (no shared backplane)
- **Red/Black concept** (classified vs. unclassified)

════════════════════════════════════════════════════════════════════

⚡ **6. QUALITY OF SERVICE (QoS)**
──────────────────────────────────

**Priority Queues (802.1p):**

+----------+---------------------------+-------------------+
| Priority | Traffic Class             | Example           |
+==========+===========================+===================+
| **7**    | Network control (highest) | Switch management |
| **6**    | Voice (low latency)       | Cockpit audio     |
| **5**    | Video                     | CCTV, IFE streams |
| **4**    | Controlled load           | FCC data          |
| **3**    | Excellent effort          | IFE metadata      |
| **2**    | Spare                     | -                 |
| **1**    | Background                | Logs, diagnostics |
| **0**    | Best effort (lowest)      | Passenger Wi-Fi   |
+----------+---------------------------+-------------------+

**Traffic Shaping:**

.. code-block:: text

   # Enforce BAG for VL 100 (4 ms BAG)
   # Drop frames if sent faster than 250 fps (1000/4)
   
   if (frame.VL_ID == 100 && time_since_last_frame < 4ms):
       drop(frame)
       log("VL 100 BAG violation")

**Bandwidth Reservation:**

- **Flight-critical**: 40% of 100 Mbps = 40 Mbps reserved
- **IFE**: 30% = 30 Mbps
- **Maintenance**: 10% = 10 Mbps
- **Spare**: 20% = 20 Mbps (overflow)

════════════════════════════════════════════════════════════════════

📊 **7. BANDWIDTH ALLOCATION**
───────────────────────────────

**Calculating VL Bandwidth:**

$$
\text{BW}_{\text{VL}} = \frac{\text{MaxFrameSize} \times 8}{BAG}
$$

**Example:**

VL with MaxFrameSize = 1024 bytes, BAG = 8 ms:

$$
\text{BW} = \frac{1024 \times 8}{0.008} = 1,024,000 \text{ bps} = 1.024 \text{ Mbps}
$$

**Network Utilization:**

For N VLs on a 100 Mbps link:

$$
\text{Utilization} = \frac{\sum_{i=1}^{N} \text{BW}_i}{100 \text{ Mbps}} \times 100\%
$$

**Safe limit**: <70% utilization (leave margin for retransmissions, control traffic)

**Example Network Load:**

+--------+------------+---------+---------------+
| VL ID  | BAG (ms)   | Bytes   | Bandwidth     |
+========+============+=========+===============+
| 1      | 4          | 512     | 1.024 Mbps    |
| 2      | 8          | 1024    | 1.024 Mbps    |
| 10     | 16         | 256     | 0.128 Mbps    |
| 100    | 32         | 512     | 0.128 Mbps    |
| **Total**           |         | **2.304 Mbps**|
+--------+------------+---------+---------------+

Utilization = 2.304 / 100 = **2.3%** ✅ (well below 70%)

════════════════════════════════════════════════════════════════════

🔄 **8. REDUNDANCY & RELIABILITY**
───────────────────────────────────

**Dual Network Architecture:**

::

   End System (ES)
   ┌──────────────┐
   │  Application │
   └───────┬──────┘
           │
       ┌───▼───┐
       │ VL TX │ (Sends on both A & B)
       └┬─────┬┘
        │     │
   ┌────▼──┐ ┌▼────┐
   │Net A  │ │Net B│
   │Port   │ │Port │
   └────┬──┘ └┬────┘
        │     │
   ─────┼─────┼───── Network A (Primary)
        │     │
   ─────┼─────┼───── Network B (Backup)
        │     │
   ┌────▼──┐ ┌▼────┐
   │Net A  │ │Net B│
   │Port   │ │Port │
   └────┬──┘ └┬────┘
       │     │
   ┌───▼─────▼───┐
   │ VL RX       │ (Receives from first)
   │ (Redundancy │
   │  Manager)   │
   └─────────────┘

**Redundancy Manager Logic:**

.. code-block:: python

   def receive_frame(frame_a, frame_b):
       # Use first valid frame received
       if frame_a.valid and frame_a.timestamp < frame_b.timestamp:
           return frame_a
       elif frame_b.valid:
           return frame_b
       else:
           log("Both networks failed!")
           return None

**Failure Modes:**

1. **Single network failure**: System continues (Network A or B)
2. **Switch failure**: Redundant switches per network
3. **Cable cut**: Automatic failover (<1 ms)

**Mean Time Between Failures (MTBF):**

- Single network: 10,000 hours
- Dual network: 100,000,000 hours (10⁴ × 10⁴)

════════════════════════════════════════════════════════════════════

🛠️ **9. CONFIGURATION MANAGEMENT**
────────────────────────────────────

**ICD (Interface Control Document):**

Each VL documented with:
- Source ES, Destination ES(s)
- VL ID, BAG, Max Frame Size
- Data format (Endianness, bit layout)
- Criticality (DAL level)

**Example ICD Snippet:**

.. code-block:: text

   VL_ID: 42
   Name: FCC_to_Autopilot_Attitude
   Source: FCC1 (MAC: 00:1A:2B:3C:4D:5E)
   Destinations: AP1, AP2
   BAG: 8 ms
   MaxFrameSize: 256 bytes
   VLAN: 10 (Flight-critical)
   DAL: A
   
   Data Format:
     Byte 0-3:   Pitch (float32, radians)
     Byte 4-7:   Roll (float32, radians)
     Byte 8-11:  Yaw (float32, radians)
     Byte 12-15: Timestamp (uint32, ms)

**Configuration Tools:**

- **AFDX Config Pro** (Airbus)
- **ARINC 664 Designer** (Rockwell Collins)
- **VLAN Manager** (custom scripts)

════════════════════════════════════════════════════════════════════

🎥 **10. INTEGRATION WITH IFE**
────────────────────────────────

**IFE Network Architecture:**

::

   ┌─────────────────────────────────────────┐
   │        IFE Head-End Server              │
   │  (Video Encoding, Content Library)      │
   └────────────┬────────────────────────────┘
                │ (ARINC 664 P10, VLAN 1000)
   ─────────────┼─────────────────────────────
                │
        ┌───────┼───────┬───────┬───────┐
        │       │       │       │       │
   ┌────▼──┐ ┌─▼───┐ ┌─▼───┐ ┌─▼───┐ ┌─▼───┐
   │Seat 1A│ │Seat│ │Seat│ │Seat│ │Seat│
   │Display│ │ 1B │ │ 1C │ │...│ │30F │
   └───────┘ └────┘ └────┘ └────┘ └────┘

**IFE Traffic Characteristics:**

+-----------------+-------------+-------------+-----------+
| Content Type    | Bandwidth   | Latency     | Protocol  |
+=================+=============+=============+===========+
| 4K Video        | 25 Mbps/seat| <100 ms OK  | UDP/RTP   |
| HD Video (1080p)| 8 Mbps/seat | <100 ms OK  | UDP/RTP   |
| Audio (AAC)     | 128 kbps    | <50 ms      | UDP       |
| UI Metadata     | 10 kbps     | <500 ms     | TCP       |
| Passenger Wi-Fi | 1 Mbps/pax  | <200 ms     | TCP/IP    |
+-----------------+-------------+-------------+-----------+

**Bandwidth Planning (300-seat aircraft):**

- Active IFE users: 80% = 240 seats
- HD video: 240 × 8 Mbps = **1,920 Mbps** = 1.92 Gbps
- **Solution**: Use 10 Gbps backbone, 1 Gbps per zone

**Multicast for Video Streams:**

.. code-block:: text

   # Movie "Top Gun Maverick" streamed to all seats
   VL_ID: 5000
   Source: IFE_Server (239.1.1.100)
   Destinations: Multicast Group (239.1.1.100)
   BAG: 1 ms (1000 fps)
   Bandwidth: 25 Mbps (4K stream)

════════════════════════════════════════════════════════════════════

💻 **11. PRACTICAL EXAMPLES**
──────────────────────────────

**Example 1: Sending AFDX Frame (C++)**

.. code-block:: cpp

   #include <afdx_api.h>
   
   int main() {
       // Initialize AFDX interface
       afdx_port_t port = afdx_open("eth0", VL_ID_100);
       
       // Prepare frame
       afdx_frame_t frame;
       frame.vl_id = 100;
       frame.size = 512;
       memcpy(frame.data, "Flight data...", 14);
       
       // Send on both networks (A & B)
       afdx_send(port, &frame, NETWORK_A | NETWORK_B);
       
       // Verify BAG compliance
       if (afdx_check_bag_violation(port)) {
           printf("WARNING: BAG violation detected!\n");
       }
       
       afdx_close(port);
       return 0;
   }

**Example 2: VLAN Configuration (Linux)**

.. code-block:: bash

   # Create VLAN 10 for flight-critical traffic
   ip link add link eth0 name eth0.10 type vlan id 10
   ip link set eth0.10 up
   
   # Assign IP (Part 10 only)
   ip addr add 10.0.10.100/24 dev eth0.10
   
   # Set QoS priority (802.1p = 4)
   ip link set dev eth0.10 type vlan egress 0:4

**Example 3: Bandwidth Calculator (Python)**

.. code-block:: python

   def calculate_vl_bandwidth(max_frame_size, bag_ms):
       """Calculate VL bandwidth in Mbps"""
       return (max_frame_size * 8) / (bag_ms / 1000) / 1e6
   
   # Example VLs
   vls = [
       {"id": 1, "size": 512, "bag": 4},
       {"id": 2, "size": 1024, "bag": 8},
       {"id": 10, "size": 256, "bag": 16},
   ]
   
   total_bw = sum(calculate_vl_bandwidth(vl["size"], vl["bag"]) 
                  for vl in vls)
   
   utilization = (total_bw / 100) * 100  # % of 100 Mbps link
   print(f"Total BW: {total_bw:.2f} Mbps")
   print(f"Utilization: {utilization:.1f}%")

════════════════════════════════════════════════════════════════════

⚠️ **12. COMMON PITFALLS**
───────────────────────────

❌ **Pitfall 1: BAG Violation**
   - **Problem:** Sending frames faster than BAG allows
   - **Solution:** Implement rate limiting in software

❌ **Pitfall 2: VLAN Misconfiguration**
   - **Problem:** IFE traffic leaks into flight-critical VLAN
   - **Solution:** ACLs, firewall rules, physical isolation

❌ **Pitfall 3: Ignoring Jitter**
   - **Problem:** Avionics expect <500 µs, but IFE causes 5 ms jitter
   - **Solution:** Separate switches, QoS prioritization

❌ **Pitfall 4: Single Point of Failure**
   - **Problem:** Only using Network A (no redundancy)
   - **Solution:** Always configure both A & B networks

❌ **Pitfall 5: Undersized Switches**
   - **Problem:** Switch buffers overflow under peak load
   - **Solution:** Use enterprise-grade switches (Cisco Catalyst, Juniper)

════════════════════════════════════════════════════════════════════

📇 **13. QUICK REFERENCE CARD**
────────────────────────────────

**Key Parameters**

.. code-block:: text

   Bandwidth:      100 Mbps (AFDX), up to 10 Gbps (P10)
   Frame Size:     64-1518 bytes
   BAG Range:      1-128 ms
   Jitter:         <500 µs (avionics), <10 ms (IFE)
   Redundancy:     Dual networks (A + B)
   VL ID Range:    1-32767
   VLAN ID Range:  1-4094

**Common Commands**

.. code-block:: bash

   # Check VLAN config
   cat /proc/net/vlan/config
   
   # Monitor AFDX traffic
   tcpdump -i eth0 vlan 10
   
   # Show QoS stats
   tc -s qdisc show dev eth0.10
   
   # Verify redundancy
   ethtool eth0  # Check Network A link
   ethtool eth1  # Check Network B link

**Bandwidth Formula**

$$
\text{BW}_{\text{VL}} = \frac{\text{FrameSize} \times 8}{\text{BAG (seconds)}}
$$

════════════════════════════════════════════════════════════════════

📝 **14. EXAM QUESTIONS**
──────────────────────────

**Q1:** What is the difference between AFDX and standard Ethernet?

**A1:** AFDX uses full-duplex switched fabric (no collisions), guaranteed bandwidth via Virtual Links (VL) with BAG enforcement, bounded jitter (<500 µs), and mandatory redundancy (dual networks A+B). Standard Ethernet is best-effort with variable latency.

────────────────────────────────────────────────────────────────────

**Q2:** How does BAG (Bandwidth Allocation Gap) work?

**A2:** BAG is the minimum time interval between consecutive frames on a VL. If BAG = 8 ms, maximum 125 frames/second can be sent. Switch enforces BAG by dropping frames sent faster than allowed.

────────────────────────────────────────────────────────────────────

**Q3:** Why use VLAN segregation between flight-critical and IFE?

**A3:** To prevent IFE traffic (potentially malicious or malfunctioning) from interfering with flight-critical systems. VLANs provide Layer 2 isolation, combined with firewalls for Layer 3+ protection (defense in depth).

────────────────────────────────────────────────────────────────────

**Q4:** What happens if Network A fails in a dual-redundant AFDX system?

**A4:** The receiving End System (ES) automatically uses frames from Network B. Redundancy Manager selects the first valid frame received. Failover is transparent (<1 ms), with no data loss.

────────────────────────────────────────────────────────────────────

**Q5:** Calculate bandwidth for VL with 1024-byte frames, BAG = 16 ms.

**A5:**  
$$
\text{BW} = \frac{1024 \times 8}{0.016} = 512,000 \text{ bps} = 0.512 \text{ Mbps}
$$

════════════════════════════════════════════════════════════════════

📚 **15. FURTHER READING**
───────────────────────────

**Standards:**
- ARINC 664 Part 7 (AFDX Specification)
- ARINC 664 Part 10 (Extended Ethernet)
- DO-178C § 11.13 (Network Partitioning)

**Books:**
- *Avionics Networking* — Ian Moir, Allan Seabridge
- *Aircraft Data Networks* — Ed Harcourt

**Online:**
- Airbus AFDX Design Guide (internal)
- Rockwell Collins ARINC 664 Training
- IEEE 802.1Q (VLAN Standard)

**Tools:**
- Wireshark (AFDX plugin)
- AFDX Config Pro (Airbus)
- CANoe/VN5640 (Vector Informatik)

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand VL concept and BAG enforcement
- [ ] Configure VLANs for domain segregation
- [ ] Calculate bandwidth for VL set
- [ ] Set up dual-redundant networks (A+B)
- [ ] Implement QoS priorities (802.1p)
- [ ] Test failover scenarios (Network A/B failure)
- [ ] Review ICD for your aircraft program

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ COMPLETE  
**Created:** January 14, 2026  
**For:** Aircraft Services Architect Role (Portland, PAC)  
**Next:** Review [Verification_Validation_Cheatsheet.rst](Verification_Validation_Cheatsheet.rst)
