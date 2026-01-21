═══════════════════════════════════════════════════════════════════════
ADVANCED NETWORKING FOR AVIONICS SYSTEMS
═══════════════════════════════════════════════════════════════════════

**Comprehensive Guide to Aircraft Network Protocols**  
**Domain:** Avionics ✈️ | Networking 🌐 | IFE Systems 📺  
**Purpose:** VLAN, IGMP, BGP, OSPF, TSN, AFDX for safety-critical systems

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Aircraft Networking** requires deterministic, fault-tolerant protocols for safety-critical and entertainment systems.

**Key Technologies:**
- **VLAN (Virtual LAN):** Isolate safety-critical (flight control) from non-critical (IFE) traffic
- **IGMP (Multicast):** Efficient video streaming to 300+ passengers (one stream → many receivers)
- **TSN (Time-Sensitive Networking):** Deterministic latency for real-time control
- **AFDX (Avionics Full-Duplex Ethernet):** DO-178 certified Ethernet for flight systems
- **BGP/OSPF:** Routing for complex aircraft networks (military, VIP jets)

**Why Different from IT Networks:**
- **Certification:** DO-178C, DO-254, DO-160G compliance required
- **Determinism:** Guaranteed delivery times (no "best effort")
- **Fault Tolerance:** Dual redundant networks, automatic failover
- **Weight/Power:** Optimized for aircraft constraints (lighter cables, lower power)

═══════════════════════════════════════════════════════════════════════

🏗️ **1. VLAN (VIRTUAL LAN) FOR AIRCRAFT**
─────────────────────────────────────────────────────────────────────────

**1.1 VLAN Fundamentals**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why VLANs in Aircraft:**

+----------------------------+----------------------------------------+
| **Requirement**            | **VLAN Solution**                      |
+============================+========================================+
| **Isolation**              | Separate IFE from flight control       |
| **Security**               | Prevent passenger WiFi → avionics      |
| **QoS**                    | Prioritize safety-critical traffic     |
| **Bandwidth**              | Allocate guaranteed bandwidth per VLAN |
| **Cost**                   | Single physical network, multiple      |
|                            | logical networks (less wiring)         |
+----------------------------+----------------------------------------+

**VLAN Architecture for Commercial Aircraft:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │                   Aircraft Network                          │
   ├─────────────────────────────────────────────────────────────┤
   │  Physical: 1 Gbps Ethernet (CAT6A shielded cables)         │
   ├─────────────────────────────────────────────────────────────┤
   │  Logical VLANs:                                             │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 10: Flight Control (ASIL-D, DO-178C DAL A)     │  │
   │  │  - Autopilot, fly-by-wire, engine control            │  │
   │  │  - Priority: Highest (CoS 7)                         │  │
   │  │  - Bandwidth: 50 Mbps guaranteed                     │  │
   │  │  - Redundancy: Dual redundant switches               │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 20: Navigation (DO-178C DAL B)                 │  │
   │  │  - GPS, IRS, flight management system                │  │
   │  │  - Priority: High (CoS 6)                            │  │
   │  │  - Bandwidth: 20 Mbps guaranteed                     │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 30: Communications (DO-178C DAL C)             │  │
   │  │  - SATCOM, VHF radio, ACARS                          │  │
   │  │  - Priority: Medium (CoS 4)                          │  │
   │  │  - Bandwidth: 10 Mbps guaranteed                     │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 100: IFE Video Streaming (QM - not certified)  │  │
   │  │  - Passenger entertainment, video multicast          │  │
   │  │  - Priority: Low (CoS 2)                             │  │
   │  │  - Bandwidth: 100 Mbps (best effort)                 │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 200: Passenger WiFi (QM)                       │  │
   │  │  - Internet access, email, browsing                  │  │
   │  │  - Priority: Lowest (CoS 1)                          │  │
   │  │  - Bandwidth: 50 Mbps (best effort)                  │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 300: Crew Network (QM)                         │  │
   │  │  - Cabin crew tablets, announcements, monitoring     │  │
   │  │  - Priority: Medium (CoS 3)                          │  │
   │  │  - Bandwidth: 10 Mbps                                │  │
   │  └──────────────────────────────────────────────────────┘  │
   │                                                             │
   │  ┌──────────────────────────────────────────────────────┐  │
   │  │  VLAN 999: Management (Isolated)                     │  │
   │  │  - Switch management, monitoring, firmware updates   │  │
   │  │  - Priority: Medium (CoS 3)                          │  │
   │  │  - Bandwidth: 1 Mbps                                 │  │
   │  └──────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────┘

**1.2 VLAN Configuration (Cisco Avionics Switch)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Cisco IE-3400 Configuration:**

.. code-block:: text

   ! Enable VTP (VLAN Trunking Protocol) - optional
   vtp mode transparent
   vtp domain AIRCRAFT_NET
   
   ! Create VLANs
   vlan 10
    name FLIGHT_CONTROL
    exit
   
   vlan 20
    name NAVIGATION
    exit
   
   vlan 30
    name COMMUNICATIONS
    exit
   
   vlan 100
    name IFE_VIDEO
    exit
   
   vlan 200
    name PASSENGER_WIFI
    exit
   
   vlan 300
    name CREW_NETWORK
    exit
   
   vlan 999
    name MANAGEMENT
    exit
   
   ! Configure trunk port (uplink to core switch)
   interface GigabitEthernet1/0/1
    description Uplink to Core Switch
    switchport mode trunk
    switchport trunk allowed vlan 10,20,30,100,200,300,999
    switchport trunk native vlan 999
    spanning-tree portfast trunk
    exit
   
   ! Configure access port for IFE head-end server
   interface GigabitEthernet1/0/2
    description IFE Head-End Server
    switchport mode access
    switchport access vlan 100
    spanning-tree portfast
    exit
   
   ! Configure access ports for seat units (rows 1-10)
   interface range GigabitEthernet1/0/3-12
    description Seat Units Rows 1-10
    switchport mode access
    switchport access vlan 100
    spanning-tree portfast
    exit
   
   ! Configure access port for crew tablet
   interface GigabitEthernet1/0/13
    description Crew Tablet
    switchport mode access
    switchport access vlan 300
    spanning-tree portfast
    exit
   
   ! Configure management interface
   interface vlan 999
    ip address 192.168.1.10 255.255.255.0
    no shutdown
    exit
   
   ! Default gateway for management
   ip default-gateway 192.168.1.1
   
   ! Enable SSH for remote management
   ip domain-name aircraft.local
   crypto key generate rsa modulus 2048
   username admin privilege 15 secret Secure_Password_123
   line vty 0 15
    transport input ssh
    login local
    exit
   
   ! Save configuration
   write memory

**1.3 VLAN QoS (Quality of Service)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Priority Mapping (IEEE 802.1p CoS):**

+----------+----------------------+---------------------------+
| **CoS**  | **Priority**         | **VLAN Usage**            |
+==========+======================+===========================+
| **7**    | Network Control      | VLAN 10 (Flight Control)  |
| **6**    | Voice (IP telephony) | VLAN 20 (Navigation)      |
| **5**    | Video (Broadcast)    | (Reserved)                |
| **4**    | Critical Apps        | VLAN 30 (Communications)  |
| **3**    | Excellent Effort     | VLAN 300 (Crew)           |
| **2**    | Standard Effort      | VLAN 100 (IFE Video)      |
| **1**    | Background           | VLAN 200 (WiFi)           |
| **0**    | Best Effort          | Default                   |
+----------+----------------------+---------------------------+

**QoS Configuration:**

.. code-block:: text

   ! Enable QoS globally
   mls qos
   
   ! Map CoS to queue
   mls qos map cos-queue 0 1 to 1   ! CoS 0,1 → Queue 1 (lowest)
   mls qos map cos-queue 2 3 to 2   ! CoS 2,3 → Queue 2
   mls qos map cos-queue 4 5 to 3   ! CoS 4,5 → Queue 3
   mls qos map cos-queue 6 7 to 4   ! CoS 6,7 → Queue 4 (highest)
   
   ! Configure egress queues (output scheduling)
   interface GigabitEthernet1/0/1
    mls qos trust cos
    
    ! Queue 4 (flight control): 50% bandwidth, strict priority
    priority-queue out
    queue-set 1 queue 4 weight 50
    
    ! Queue 3 (navigation): 20% bandwidth
    queue-set 1 queue 3 weight 20
    
    ! Queue 2 (crew/IFE): 20% bandwidth
    queue-set 1 queue 2 weight 20
    
    ! Queue 1 (WiFi): 10% bandwidth (best effort)
    queue-set 1 queue 1 weight 10
    exit

**1.4 VLAN Security**
~~~~~~~~~~~~~~~~~~~~~~

**Prevent VLAN Hopping Attacks:**

.. code-block:: text

   ! Disable DTP (Dynamic Trunking Protocol) on access ports
   interface range GigabitEthernet1/0/2-48
    switchport mode access
    switchport nonegotiate  ! Disable DTP
    exit
   
   ! Set native VLAN to unused VLAN
   interface GigabitEthernet1/0/1
    switchport trunk native vlan 999
    exit
   
   ! Disable unused VLANs on trunk
   interface GigabitEthernet1/0/1
    switchport trunk allowed vlan 10,20,30,100,200,300,999
    ! NOT: switchport trunk allowed vlan all
    exit
   
   ! Enable port security (limit MAC addresses)
   interface GigabitEthernet1/0/2
    switchport port-security
    switchport port-security maximum 1
    switchport port-security mac-address sticky
    switchport port-security violation restrict
    exit

═══════════════════════════════════════════════════════════════════════

📡 **2. IGMP (INTERNET GROUP MANAGEMENT PROTOCOL)**
─────────────────────────────────────────────────────────────────────────

**2.1 IGMP Fundamentals**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why IGMP for IFE:**

.. code-block:: text

   Problem: Stream video to 300 passengers
   
   ❌ Unicast (Bad):
   - Head-End sends 300 separate streams
   - Bandwidth = 300 passengers × 3 Mbps = 900 Mbps
   - Exceeds 1 Gbps link capacity with overhead
   
   ✅ Multicast with IGMP (Good):
   - Head-End sends 1 multicast stream
   - Passengers join multicast group
   - Switch replicates packets only to interested ports
   - Bandwidth = 1 × 3 Mbps = 3 Mbps per channel
   - Total for 8 channels = 24 Mbps
   
   Savings: 900 Mbps → 24 Mbps (97% reduction)

**IGMP Message Types:**

+-----------------+----------------------------------+---------------------+
| **Message**     | **Direction**                    | **Purpose**         |
+=================+==================================+=====================+
| **Query**       | Router → Hosts                   | "Who wants group X?"||
| **Report**      | Host → Router                    | "I want group X"    |
| **Leave**       | Host → Router                    | "I'm leaving X"     |
+-----------------+----------------------------------+---------------------+

**IGMP Versions:**

+------------+-----------------------+----------------------------+
| **Version**| **Features**          | **Use Case**               |
+============+=======================+============================+
| **IGMPv1** | Basic join/leave      | Legacy (deprecated)        |
| **IGMPv2** | Leave messages        | Standard for most aircraft |
| **IGMPv3** | Source-specific       | Advanced (military)        |
+------------+-----------------------+----------------------------+

**2.2 IGMP Snooping**
~~~~~~~~~~~~~~~~~~~~~~

**Problem without IGMP Snooping:**

.. code-block:: text

   ┌────────────────────────────────────────────────────┐
   │           Switch (No IGMP Snooping)                │
   ├────────────────────────────────────────────────────┤
   │  Multicast packets flooded to ALL ports            │
   │  (like broadcast)                                  │
   └─┬────┬────┬────┬────┬────┬────┬────┬────┬────┬───┘
     │    │    │    │    │    │    │    │    │    │
   Seat Seat Seat Seat Seat Seat Seat Seat Seat Seat
    1A   1B   1C   1D   1E   1F   2A   2B   2C   2D
     ❌   ❌   ❌   ✅   ❌   ❌   ❌   ❌   ❌   ❌
   (Only 1D wants video, but all seats receive it)

**Solution with IGMP Snooping:**

.. code-block:: text

   ┌────────────────────────────────────────────────────┐
   │           Switch (IGMP Snooping Enabled)           │
   │  - Listens to IGMP messages                        │
   │  - Builds multicast forwarding table               │
   │  - Forwards packets only to interested ports       │
   └─┬────┬────┬────┬────┬────┬────┬────┬────┬────┬───┘
     │    │    │    │    │    │    │    │    │    │
   Seat Seat Seat Seat Seat Seat Seat Seat Seat Seat
    1A   1B   1C   1D   1E   1F   2A   2B   2C   2D
                      ✅
   (Only 1D receives video stream)

**IGMP Snooping Configuration:**

.. code-block:: text

   ! Enable IGMP snooping globally
   ip igmp snooping
   
   ! Enable IGMP snooping on VLAN 100 (IFE video)
   ip igmp snooping vlan 100
   
   ! Set multicast router port (uplink to head-end)
   ip igmp snooping vlan 100 mrouter interface GigabitEthernet1/0/1
   
   ! Enable IGMP querier (if no router present)
   ip igmp snooping vlan 100 querier
   ip igmp snooping vlan 100 querier address 10.100.0.254
   
   ! Set query interval (default 60s, can reduce for faster leave)
   ip igmp snooping vlan 100 querier query-interval 30
   
   ! Enable fast leave (for quick channel change)
   ip igmp snooping vlan 100 immediate-leave
   
   ! Verify configuration
   show ip igmp snooping
   show ip igmp snooping vlan 100
   show ip igmp snooping groups

**2.3 Multicast Address Allocation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**IPv4 Multicast Ranges:**

+------------------------------+--------------------------------+
| **Range**                    | **Purpose**                    |
+==============================+================================+
| **224.0.0.0 - 224.0.0.255**  | Reserved (local network)       |
| **224.0.1.0 - 238.255.255.255** | Globally routable multicast |
| **239.0.0.0 - 239.255.255.255** | Private multicast (like RFC 1918) |
+------------------------------+--------------------------------+

**IFE Multicast Allocation:**

.. code-block:: text

   Base: 239.255.1.0/24 (Private multicast for IFE)
   
   Movie Channels:
   239.255.1.1   - Channel 1: Latest Movie 1
   239.255.1.2   - Channel 2: Latest Movie 2
   239.255.1.3   - Channel 3: Classic Movie
   239.255.1.4   - Channel 4: Kids Movie
   239.255.1.5   - Channel 5: Documentary
   239.255.1.6   - Channel 6: TV Series 1
   239.255.1.7   - Channel 7: TV Series 2
   239.255.1.8   - Channel 8: Live TV
   
   Moving Maps:
   239.255.1.10  - Flight Path Map
   239.255.1.11  - Tail Camera
   239.255.1.12  - Weather Radar
   
   Games:
   239.255.1.20  - Multiplayer Game 1
   239.255.1.21  - Multiplayer Game 2

**2.4 IGMP Client (Seat Unit)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Join Multicast Group (C code):**

.. code-block:: c

   #include <stdio.h>
   #include <stdlib.h>
   #include <string.h>
   #include <sys/socket.h>
   #include <netinet/in.h>
   #include <arpa/inet.h>
   
   int join_multicast_group(const char *group_ip, int port) {
       int sockfd;
       struct sockaddr_in local_addr;
       struct ip_mreq mreq;
       
       // Create UDP socket
       sockfd = socket(AF_INET, SOCK_DGRAM, 0);
       if (sockfd < 0) {
           perror("socket");
           return -1;
       }
       
       // Allow multiple sockets to bind to same port
       int reuse = 1;
       setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
       
       // Bind to port
       memset(&local_addr, 0, sizeof(local_addr));
       local_addr.sin_family = AF_INET;
       local_addr.sin_addr.s_addr = htonl(INADDR_ANY);
       local_addr.sin_port = htons(port);
       
       if (bind(sockfd, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0) {
           perror("bind");
           close(sockfd);
           return -1;
       }
       
       // Join multicast group
       mreq.imr_multiaddr.s_addr = inet_addr(group_ip);
       mreq.imr_interface.s_addr = htonl(INADDR_ANY);
       
       if (setsockopt(sockfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
           perror("setsockopt IP_ADD_MEMBERSHIP");
           close(sockfd);
           return -1;
       }
       
       printf("✅ Joined multicast group %s:%d\n", group_ip, port);
       return sockfd;
   }
   
   int main(void) {
       char buffer[2048];
       struct sockaddr_in sender_addr;
       socklen_t sender_len = sizeof(sender_addr);
       
       // Join Channel 1 (Latest Movie)
       int sockfd = join_multicast_group("239.255.1.1", 5004);
       if (sockfd < 0) {
           return 1;
       }
       
       // Receive video packets
       while (1) {
           int recv_len = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                  (struct sockaddr *)&sender_addr, &sender_len);
           if (recv_len < 0) {
               perror("recvfrom");
               break;
           }
           
           printf("Received %d bytes from %s\n", recv_len,
                  inet_ntoa(sender_addr.sin_addr));
           
           // Process video packet (decode H.265, display)
           // ... (integrate with GStreamer pipeline)
       }
       
       // Leave multicast group
       struct ip_mreq mreq;
       mreq.imr_multiaddr.s_addr = inet_addr("239.255.1.1");
       mreq.imr_interface.s_addr = htonl(INADDR_ANY);
       setsockopt(sockfd, IPPROTO_IP, IP_DROP_MEMBERSHIP, &mreq, sizeof(mreq));
       
       close(sockfd);
       return 0;
   }

**Leave Multicast Group (for channel change):**

.. code-block:: python

   import socket
   import struct
   
   def change_channel(old_group, new_group, port=5004):
       """Change from one multicast channel to another"""
       
       # Leave old group
       sock.setsockopt(
           socket.IPPROTO_IP,
           socket.IP_DROP_MEMBERSHIP,
           struct.pack('4s4s', socket.inet_aton(old_group),
                      socket.inet_aton('0.0.0.0'))
       )
       
       # Join new group
       sock.setsockopt(
           socket.IPPROTO_IP,
           socket.IP_ADD_MEMBERSHIP,
           struct.pack('4s4s', socket.inet_aton(new_group),
                      socket.inet_aton('0.0.0.0'))
       )
       
       print(f"Changed channel: {old_group} → {new_group}")
   
   # Example: Switch from Channel 1 to Channel 2
   change_channel('239.255.1.1', '239.255.1.2')

═══════════════════════════════════════════════════════════════════════

🛣️ **3. BGP & OSPF (ROUTING PROTOCOLS)**
─────────────────────────────────────────────────────────────────────────

**3.1 When to Use BGP/OSPF in Aircraft**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical Aircraft (Commercial):**
- ❌ **No BGP/OSPF needed:** Simple switched Ethernet (VLANs only)
- ✅ **Static routes sufficient:** 1-2 routers max

**Complex Aircraft (Military, VIP Jets):**
- ✅ **OSPF useful:** Multiple subnets, dynamic routing, failover
- ✅ **BGP useful:** Integration with ground networks, policy-based routing

**Example: Military Transport Aircraft**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────┐
   │         Military Transport Aircraft Network              │
   ├──────────────────────────────────────────────────────────┤
   │  Cockpit Zone (10.1.0.0/16)                              │
   │  - Flight control, navigation, weapons systems           │
   │  - OSPF Area 0 (backbone)                                │
   ├──────────────────────────────────────────────────────────┤
   │  Cargo Zone (10.2.0.0/16)                                │
   │  - Cargo monitoring, sensors, cameras                    │
   │  - OSPF Area 1                                           │
   ├──────────────────────────────────────────────────────────┤
   │  Passenger Zone (10.3.0.0/16)                            │
   │  - IFE, crew tablets, WiFi                               │
   │  - OSPF Area 2                                           │
   ├──────────────────────────────────────────────────────────┤
   │  External Links                                          │
   │  - SATCOM uplink (BGP AS 65001)                          │
   │  - Tactical data link (BGP AS 65002)                     │
   └──────────────────────────────────────────────────────────┘

**3.2 OSPF Configuration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario: Three Routers in Aircraft**

.. code-block:: text

   Router 1 (Cockpit)     Router 2 (Cargo)     Router 3 (Passenger)
        │                      │                       │
        └───────── OSPF ───────┴───────────────────────┘
             Area 0 (Backbone)

**Router 1 (Cockpit) Configuration:**

.. code-block:: text

   ! Enable OSPF process 1
   router ospf 1
    router-id 10.1.0.1
    
    ! Advertise cockpit network (10.1.0.0/16)
    network 10.1.0.0 0.0.255.255 area 0
    
    ! Passive interface (don't send OSPF hellos to end devices)
    passive-interface GigabitEthernet0/0  ! Cockpit LAN
    
    ! Set reference bandwidth (for cost calculation)
    auto-cost reference-bandwidth 10000  ! 10 Gbps reference
    exit
   
   ! Configure interfaces
   interface GigabitEthernet0/0
    description Cockpit LAN
    ip address 10.1.0.1 255.255.0.0
    no shutdown
    exit
   
   interface GigabitEthernet0/1
    description Link to Router 2 (Cargo)
    ip address 10.100.0.1 255.255.255.252
    ip ospf cost 10
    no shutdown
    exit

**Router 2 (Cargo) Configuration:**

.. code-block:: text

   router ospf 1
    router-id 10.2.0.1
    network 10.2.0.0 0.0.255.255 area 0
    network 10.100.0.0 0.0.0.3 area 0      ! Link to Router 1
    network 10.100.0.4 0.0.0.3 area 0      ! Link to Router 3
    passive-interface GigabitEthernet0/0
    auto-cost reference-bandwidth 10000
    exit

**Router 3 (Passenger/IFE) Configuration:**

.. code-block:: text

   router ospf 1
    router-id 10.3.0.1
    network 10.3.0.0 0.0.255.255 area 0
    network 10.100.0.4 0.0.0.3 area 0      ! Link to Router 2
    passive-interface GigabitEthernet0/0
    auto-cost reference-bandwidth 10000
    exit

**Verify OSPF:**

.. code-block:: text

   ! Show OSPF neighbors
   Router1# show ip ospf neighbor
   
   Neighbor ID     Pri   State       Dead Time   Address         Interface
   10.2.0.1         1    FULL/DR     00:00:35    10.100.0.2      Gi0/1
   
   ! Show OSPF routes
   Router1# show ip route ospf
   
   O    10.2.0.0/16 [110/20] via 10.100.0.2, 00:05:23, GigabitEthernet0/1
   O    10.3.0.0/16 [110/30] via 10.100.0.2, 00:03:15, GigabitEthernet0/1

**3.3 BGP Configuration (VIP Jet with SATCOM)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario: Aircraft with Dual SATCOM Links**

.. code-block:: text

   ┌─────────────────────────────────────────────────┐
   │          VIP Aircraft Router                    │
   │          AS 65001                               │
   ├─────────────────────────────────────────────────┤
   │  Internal Networks: 10.0.0.0/8                  │
   │                                                 │
   │  SATCOM Link 1 (Primary):                       │
   │  - Provider: Inmarsat (AS 65100)                │
   │  - Public IP: 203.0.113.10                      │
   │                                                 │
   │  SATCOM Link 2 (Backup):                        │
   │  - Provider: Iridium (AS 65200)                 │
   │  - Public IP: 198.51.100.20                     │
   └─────────────────────────────────────────────────┘

**BGP Configuration:**

.. code-block:: text

   ! Define BGP AS number
   router bgp 65001
    bgp router-id 10.0.0.1
    
    ! Advertise internal networks
    network 10.0.0.0 mask 255.0.0.0
    
    ! Neighbor 1: Inmarsat (Primary)
    neighbor 203.0.113.1 remote-as 65100
    neighbor 203.0.113.1 description Inmarsat SATCOM Primary
    neighbor 203.0.113.1 weight 200    ! Prefer this link (higher weight)
    
    ! Neighbor 2: Iridium (Backup)
    neighbor 198.51.100.1 remote-as 65200
    neighbor 198.51.100.1 description Iridium SATCOM Backup
    neighbor 198.51.100.1 weight 100   ! Lower weight (backup)
    
    ! Set local preference for incoming routes
    neighbor 203.0.113.1 route-map PREFER_INMARSAT in
    exit
   
   ! Route map to prefer Inmarsat
   route-map PREFER_INMARSAT permit 10
    set local-preference 200
    exit
   
   ! Verify BGP
   show ip bgp summary
   show ip bgp neighbors

**BGP Failover:**

.. code-block:: text

   Normal Operation:
   - All traffic uses Inmarsat (higher weight)
   - Iridium connection established but not used
   
   Failure Scenario:
   1. Inmarsat link goes down (antenna issue, satellite handoff)
   2. BGP detects neighbor down (keepalive timeout ~180s)
   3. Routes withdrawn from routing table
   4. Traffic automatically switches to Iridium
   
   Failover Time: ~3 minutes (BGP convergence)
   
   Optimization:
   - Use BFD (Bidirectional Forwarding Detection) for faster failover (~1s)
   - Configure BGP timers: keepalive 10, hold-time 30

═══════════════════════════════════════════════════════════════════════

⏱️ **4. TSN (TIME-SENSITIVE NETWORKING)**
─────────────────────────────────────────────────────────────────────────

**4.1 TSN Overview**
~~~~~~~~~~~~~~~~~~~~~

**Why TSN for Aircraft:**

+-----------------------+----------------------------------+
| **Requirement**       | **TSN Solution**                 |
+=======================+==================================+
| **Determinism**       | Guaranteed delivery time         |
| **Real-time control** | Flight control, engine updates   |
| **Mixed traffic**     | Safety + entertainment on same   |
|                       | physical network                 |
| **Synchronization**   | Precise time sync across nodes   |
+-----------------------+----------------------------------+

**TSN Key Standards (IEEE 802.1):**

+-------------------+--------------------------------+------------------------+
| **Standard**      | **Feature**                    | **Use Case**           |
+===================+================================+========================+
| **802.1AS**       | Time synchronization (gPTP)    | Sub-microsecond sync   |
| **802.1Qbv**      | Time-aware shaper (TAS)        | Scheduled traffic      |
| **802.1Qbu**      | Frame preemption               | Low latency for urgent |
| **802.1CB**       | Redundancy (FRER)              | Dual path reliability  |
| **802.1Qav**      | Credit-based shaper (CBS)      | AV streaming (video)   |
+-------------------+--------------------------------+------------------------+

**4.2 Time-Aware Shaper (802.1Qbv)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Concept: Schedule Network Access**

.. code-block:: text

   Time-Slotted Transmission (like ARINC 653 for networking):
   
   ┌────────────────────────────────────────────────────────┐
   │            Transmission Schedule (1ms cycle)           │
   ├────────────────────────────────────────────────────────┤
   │  0-200µs:   Flight Control (VLAN 10) - OPEN           │
   │  200-400µs: Navigation (VLAN 20) - OPEN               │
   │  400-600µs: IFE Video (VLAN 100) - OPEN               │
   │  600-800µs: WiFi (VLAN 200) - OPEN                    │
   │  800-1000µs: Reserved - CLOSED                        │
   └────────────────────────────────────────────────────────┘
   
   Benefits:
   - Flight control always gets first 200µs (guaranteed)
   - No interference from WiFi/IFE
   - Deterministic latency (max 1ms to next cycle)

**TSN Configuration (Linux with tc-taprio):**

.. code-block:: bash

   #!/bin/bash
   # Configure TSN Time-Aware Shaper on Ethernet interface
   
   INTERFACE="eth0"
   CYCLE_TIME=1000000  # 1ms in nanoseconds
   
   # Delete existing qdisc
   tc qdisc del dev $INTERFACE root 2>/dev/null
   
   # Add TAPRIO (Time-Aware Priority) qdisc
   tc qdisc add dev $INTERFACE parent root handle 100 taprio \
       num_tc 4 \
       map 0 0 1 2 2 2 3 3 \
       queues 1@0 1@1 1@2 1@3 \
       base-time 0 \
       sched-entry S 0x01 200000 \   # Queue 0 (flight control): 0-200µs
       sched-entry S 0x02 200000 \   # Queue 1 (navigation): 200-400µs
       sched-entry S 0x04 200000 \   # Queue 2 (IFE): 400-600µs
       sched-entry S 0x08 200000 \   # Queue 3 (WiFi): 600-800µs
       sched-entry S 0x00 200000 \   # All closed: 800-1000µs
       clockid CLOCK_TAI \
       flags 0x2
   
   # Verify configuration
   tc qdisc show dev $INTERFACE

**4.3 Frame Preemption (802.1Qbu)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Concept: Interrupt Lower-Priority Frames**

.. code-block:: text

   Without Preemption:
   
   ─────────[Low Priority Frame (1500 bytes)]─────────
                        ▲
                        │ High-priority frame arrives
                        │ Must wait for low-priority to finish
                        │ Wait time: ~12µs @ 1 Gbps
   
   With Preemption:
   
   ───[Low Priority]──║──[High Priority]──║──[Low Priority Resume]───
                       ▲                   ▲
                   Preempted           Completed
   
   Latency reduction: 12µs → 1µs (for small high-priority frame)

**Enable Frame Preemption (ethtool):**

.. code-block:: bash

   # Check if interface supports preemption
   ethtool --show-mm eth0
   
   # Enable preemption
   ethtool --set-mm eth0 \
       tx-enabled on \
       verify-enabled on \
       verify-time 10 \
       tx-min-frag-size 64
   
   # Set which queues are preemptible
   # Queue 0-1 (flight control, nav): non-preemptible (express)
   # Queue 2-3 (IFE, WiFi): preemptible
   ethtool --set-mm eth0 pmac-enabled on

═══════════════════════════════════════════════════════════════════════

🛡️ **5. AFDX (AVIONICS FULL-DUPLEX SWITCHED ETHERNET)**
─────────────────────────────────────────────────────────────────────────

**5.1 AFDX Overview**
~~~~~~~~~~~~~~~~~~~~~~

**AFDX = Deterministic Ethernet for DO-178 Systems**

+-------------------------+---------------------------+
| **Feature**             | **AFDX**                  |
+=========================+===========================+
| **Standard**            | ARINC 664 Part 7          |
| **Topology**            | Full-duplex switched      |
| **Speed**               | 100 Mbps (Part 7)         |
|                         | 1 Gbps (Part 10)          |
| **Protocol**            | IEEE 802.3 + extensions   |
| **Determinism**         | Virtual Links (VL)        |
| **Redundancy**          | Dual networks (A/B)       |
| **Certification**       | DO-178C compatible        |
+-------------------------+---------------------------+

**AFDX vs Standard Ethernet:**

+------------------------+----------------------+----------------------+
| **Aspect**             | **AFDX**             | **Standard Ethernet**|
+========================+======================+======================+
| **Bandwidth Guarantee**| Yes (Virtual Links)  | No (best effort)     |
| **Latency**            | Deterministic        | Variable             |
| **Redundancy**         | Dual A/B networks    | Optional (STP)       |
| **Jitter**             | Bounded              | Unbounded            |
| **Certification**      | DO-178C Part 7       | Not certifiable      |
+------------------------+----------------------+----------------------+

**5.2 Virtual Links (VL)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Concept: Guaranteed Bandwidth Channels**

.. code-block:: text

   Virtual Link = Logical unidirectional connection with guaranteed bandwidth
   
   Example: Flight Control System
   
   VL 1: Autopilot → Flight Surfaces (100 Hz, 512 bytes/frame)
   - Bandwidth Allocation Gap (BAG): 10ms (100 Hz)
   - Max Frame Size: 512 bytes
   - Guaranteed Bandwidth: (512 × 8 bits) / 0.01s = 409 kbps
   
   VL 2: GPS → Navigation Computer (10 Hz, 256 bytes/frame)
   - BAG: 100ms (10 Hz)
   - Max Frame Size: 256 bytes
   - Guaranteed Bandwidth: 20 kbps

**AFDX Frame Format:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────┐
   │                    AFDX Frame                            │
   ├──────────────────────────────────────────────────────────┤
   │  Preamble (7 bytes)                                      │
   │  SFD (1 byte)                                            │
   ├──────────────────────────────────────────────────────────┤
   │  Destination MAC (6 bytes) - VL-specific                 │
   │  Source MAC (6 bytes)                                    │
   ├──────────────────────────────────────────────────────────┤
   │  EtherType (2 bytes): 0x0800 (IPv4)                      │
   ├──────────────────────────────────────────────────────────┤
   │  IP Header (20 bytes)                                    │
   │  - Protocol: UDP (17)                                    │
   ├──────────────────────────────────────────────────────────┤
   │  UDP Header (8 bytes)                                    │
   │  - Port: VL-specific                                     │
   ├──────────────────────────────────────────────────────────┤
   │  Payload (0-1471 bytes)                                  │
   │  - Application data                                      │
   ├──────────────────────────────────────────────────────────┤
   │  FCS (4 bytes) - CRC32 checksum                          │
   └──────────────────────────────────────────────────────────┘

**5.3 AFDX Redundancy (Network A/B)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Dual Redundant Networks:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │              Flight Control Computer                    │
   │  ┌──────────┐              ┌──────────┐                 │
   │  │ Network  │              │ Network  │                 │
   │  │ A Port   │              │ B Port   │                 │
   │  └────┬─────┘              └─────┬────┘                 │
   └───────┼──────────────────────────┼──────────────────────┘
           │                          │
           │ AFDX Network A           │ AFDX Network B
           │ (Primary)                │ (Redundant)
           │                          │
   ┌───────▼──────────┐       ┌───────▼──────────┐
   │  Switch A        │       │  Switch B        │
   │  (Airbus A380)   │       │  (Airbus A380)   │
   └───────┬──────────┘       └───────┬──────────┘
           │                          │
   ┌───────▼──────────┐       ┌───────▼──────────┐
   │  Engine Control  │       │  Engine Control  │
   │  Network A Port  │       │  Network B Port  │
   └──────────────────┘       └──────────────────┘

**Receiver Logic:**

.. code-block:: python

   def receive_afdx_frame(network_a_port, network_b_port):
       """
       AFDX receiver with redundancy management
       Uses first valid frame, discards duplicate
       """
       sequence_number_a = None
       sequence_number_b = None
       
       while True:
           # Non-blocking receive on both networks
           frame_a = network_a_port.receive(non_blocking=True)
           frame_b = network_b_port.receive(non_blocking=True)
           
           # Check Network A first (primary)
           if frame_a and frame_a.validate_crc():
               sequence_number_a = frame_a.sequence_number
               return frame_a.payload
           
           # Fallback to Network B if A failed
           if frame_b and frame_b.validate_crc():
               sequence_number_b = frame_b.sequence_number
               
               # Discard if duplicate (same seq number)
               if sequence_number_b != sequence_number_a:
                   return frame_b.payload
           
           # Both failed - report error
           log_error("AFDX: Both networks failed for VL")
           raise AFDXNetworkError

**5.4 AFDX Part 10 (1 Gbps for IFE)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**AFDX Part 10 = Higher Bandwidth for IFE**

.. code-block:: text

   AFDX Part 7 (Flight Control):
   - Speed: 100 Mbps
   - Use: Safety-critical avionics
   - Certification: DO-178C DAL A/B
   
   AFDX Part 10 (Cabin/IFE):
   - Speed: 1 Gbps
   - Use: IFE, passenger WiFi, crew tablets
   - Certification: DO-178C DAL C/D or non-certified
   
   Benefits:
   - 10× bandwidth for video streaming
   - Same deterministic principles (VLs)
   - Compatible with Part 7 (same protocol)

═══════════════════════════════════════════════════════════════════════

📊 **6. NETWORK MONITORING**
─────────────────────────────────────────────────────────────────────────

**6.1 SNMP Monitoring**
~~~~~~~~~~~~~~~~~~~~~~~~

**Configure SNMP on Switch:**

.. code-block:: text

   ! Enable SNMP v3 (secure)
   snmp-server group AIRCRAFT_ADMINS v3 priv
   snmp-server user ife_monitor AIRCRAFT_ADMINS v3 \
       auth sha AuthPassword123 priv aes 256 PrivPassword456
   
   ! Enable SNMP traps
   snmp-server enable traps snmp linkdown linkup
   snmp-server enable traps vlan-membership
   snmp-server enable traps port-security
   
   ! SNMP trap receiver (monitoring server)
   snmp-server host 10.1.1.100 version 3 priv ife_monitor

**Query Switch via SNMP (Python):**

.. code-block:: python

   from pysnmp.hlapi import *
   
   def get_interface_stats(switch_ip, community='public'):
       """Get interface statistics via SNMP"""
       
       # OIDs for interface statistics
       oid_in_octets = '1.3.6.1.2.1.2.2.1.10.1'   # ifInOctets
       oid_out_octets = '1.3.6.1.2.1.2.2.1.16.1'  # ifOutOctets
       
       iterator = getCmd(
           SnmpEngine(),
           CommunityData(community),
           UdpTransportTarget((switch_ip, 161)),
           ContextData(),
           ObjectType(ObjectIdentity(oid_in_octets)),
           ObjectType(ObjectIdentity(oid_out_octets))
       )
       
       errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
       
       if errorIndication:
           print(f"Error: {errorIndication}")
       else:
           for varBind in varBinds:
               print(f"{varBind[0]} = {varBind[1]}")

**6.2 NetFlow/sFlow**
~~~~~~~~~~~~~~~~~~~~~

**Enable sFlow on Switch:**

.. code-block:: text

   ! Enable sFlow globally
   sflow enable
   
   ! Set sFlow collector (monitoring server)
   sflow destination 10.1.1.100
   
   ! Set sampling rate (1 in 1000 packets)
   sflow sampling-rate 1000
   
   ! Enable sFlow on interfaces
   interface range GigabitEthernet1/0/1-48
    sflow enable
    exit

**Analyze Traffic with sFlow-RT:**

.. code-block:: bash

   # Run sFlow-RT collector
   docker run --rm -p 8008:8008 -p 6343:6343/udp sflow/sflow-rt
   
   # Access web UI
   firefox http://localhost:8008

═══════════════════════════════════════════════════════════════════════

🎓 **7. INTERVIEW PREPARATION**
─────────────────────────────────────────────────────────────────────────

**7.1 Demonstrate Networking Knowledge**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Question: "How would you design the network for an IFE system?"**

**Answer:**

"I'd use VLAN segmentation with IGMP multicast for efficient video streaming:

**VLAN Architecture:**
1. **VLAN 10-30:** Safety-critical (flight control, nav, comms) - Highest priority (CoS 7-6)
2. **VLAN 100:** IFE video streaming - Medium priority (CoS 2)
3. **VLAN 200:** Passenger WiFi - Lowest priority (CoS 1)
4. **VLAN 300:** Crew network - Medium priority (CoS 3)

**IGMP Multicast:**
- 8 video channels: 239.255.1.1 - 239.255.1.8
- Enable IGMP snooping on switches
- Bandwidth: 8 channels × 3 Mbps = 24 Mbps (vs 900 Mbps unicast)
- 97% bandwidth savings

**QoS:**
- Priority queuing (flight control always first)
- Weighted fair queuing for non-critical traffic
- Rate limiting on WiFi (prevent congestion)

**Redundancy:**
- Dual head-end servers with Keepalived
- RAID 1 storage
- Failover < 5 seconds

This is similar to my experience with ARINC 664 networks in avionics systems."

**7.2 Connect to Resume**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Networking Experience Mapping:**

1. **AFIRS SDU (FLYHT):**
   - "Implemented satellite data link (similar to aircraft-ground connectivity)"
   - "Experience with avionics networking protocols"

2. **FDVD (Boeing):**
   - "Developed RTSP video streaming (directly applicable to IFE multicast)"
   - "Implemented network stack for cockpit displays"

3. **Industrial Gateway (Modbus/TCP):**
   - "Worked with Ethernet bridging and protocol conversion"
   - "Experience with real-time networking"

**7.3 Technical Deep-Dive**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q: "Explain IGMP snooping and why it's important for IFE."**

**A:**

"IGMP snooping is a Layer 2 optimization that prevents multicast flooding:

**Problem without snooping:**
- Switch treats multicast like broadcast
- Video stream sent to ALL ports
- 300 seats receive unwanted traffic (wasted bandwidth)

**Solution with snooping:**
- Switch listens to IGMP join/leave messages
- Builds multicast forwarding table
- Sends stream only to interested ports

**Implementation:**
```
ip igmp snooping vlan 100
ip igmp snooping vlan 100 immediate-leave
```

**Benefits for IFE:**
- Bandwidth savings (only send to viewers)
- Reduced CPU load on seat units
- Faster channel switching (immediate-leave)

I've implemented similar multicast optimizations in industrial control networks."

**7.4 Ask Intelligent Questions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. "Does Panasonic use AFDX Part 10 for cabin networks, or standard Ethernet with VLANs?"

2. "What's the typical multicast group allocation for IFE channels?"

3. "How do you handle network monitoring - SNMP, sFlow, or proprietary?"

4. "For redundancy, do you use dual switches or stacking?"

5. "What's the certification level for cabin networks - DO-160G environmental only, or TSO-C139 software?"

═══════════════════════════════════════════════════════════════════════

📚 **QUICK REFERENCE**
─────────────────────────────────────────────────────────────────────────

**Essential Commands**

.. code-block:: bash

   # VLAN
   show vlan brief
   show interfaces switchport
   
   # IGMP
   show ip igmp snooping
   show ip igmp groups
   
   # Routing
   show ip route
   show ip ospf neighbor
   show ip bgp summary
   
   # QoS
   show mls qos
   show policy-map interface <if>
   
   # Monitoring
   show interfaces counters
   show logging

**Multicast Addresses**

- **239.255.1.0/24:** IFE video channels
- **224.0.0.0/24:** Reserved (local network control)
- **239.0.0.0/8:** Private multicast

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**VLANs:**
1. ✅ **Isolation:** Separate safety-critical from entertainment
2. ✅ **QoS:** Priority-based traffic shaping (CoS 0-7)
3. ✅ **Security:** Prevent VLAN hopping, port security
4. ✅ **Bandwidth:** Guaranteed allocation per VLAN

**IGMP Multicast:**
1. ✅ **Efficiency:** One stream → many receivers (97% savings)
2. ✅ **Snooping:** Layer 2 optimization (forward only to interested ports)
3. ✅ **Fast Leave:** Quick channel switching
4. ✅ **Addresses:** 239.255.1.x for IFE channels

**Routing (BGP/OSPF):**
1. ✅ **OSPF:** Dynamic routing for complex aircraft
2. ✅ **BGP:** Multi-link failover (dual SATCOM)
3. ✅ **Use Case:** Military, VIP jets (not typical commercial)

**TSN:**
1. ✅ **Determinism:** Time-aware shaper (scheduled access)
2. ✅ **Preemption:** Low-latency for critical frames
3. ✅ **Standards:** IEEE 802.1AS, 802.1Qbv, 802.1Qbu

**AFDX:**
1. ✅ **Certification:** DO-178C compatible (Part 7)
2. ✅ **Virtual Links:** Guaranteed bandwidth channels
3. ✅ **Redundancy:** Dual A/B networks
4. ✅ **Part 10:** 1 Gbps for cabin/IFE

**Resume Connections:**
- ✅ **AFIRS:** Avionics networking experience
- ✅ **FDVD:** RTSP streaming, multicast
- ✅ **Gateway:** Ethernet bridging, real-time

═══════════════════════════════════════════════════════════════════════

**References:**

- ARINC 664 Part 7/10: Avionics Ethernet Standards
- IEEE 802.1Q: VLAN Standard
- RFC 3376: IGMP Version 3
- IEEE 802.1AS/Qbv: Time-Sensitive Networking
- DO-178C: Software Certification for Airborne Systems

**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════
