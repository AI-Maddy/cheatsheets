═══════════════════════════════════════════════════════════════════════════════
👤 Unicast - One-to-One IP Delivery
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
Unicast is a one-to-one network communication method where data is sent from a single source to a single destination. It's the most common form of IP communication, used for web browsing, email, file transfers, and point-to-point video streaming.

Key Features
------------
- **Point-to-Point**: One sender, one receiver
- **Dedicated Connection**: Unique stream per client
- **Bidirectional**: Two-way communication possible
- **Reliable**: Can use TCP for guaranteed delivery
- **Scalable Addressing**: Each destination has unique IP

How Unicast Works
-----------------
::

    Source (192.168.1.100)
           |
           v
    [Router forwards to specific destination]
           |
           v
    Destination (192.168.1.200)

- Source sends packet to specific IP address
- Routers examine destination IP
- Packet forwarded hop-by-hop to destination
- Only intended recipient processes packet

Common Use Cases
----------------
1. **Web Browsing**: HTTP/HTTPS traffic
2. **Email**: SMTP, POP3, IMAP
3. **File Transfer**: FTP, SFTP, SCP
4. **Video Streaming**: Netflix, YouTube (ABR)
5. **Remote Access**: SSH, RDP, VPN
6. **Video Contribution**: SRT, Zixi point-to-point

💡 Memory Aid
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ 🧠 MEMORY PALACE: Unicast vs Multicast as Pizza Delivery                     │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Think of network delivery methods as PIZZA RESTAURANT delivery options:     │
│                                                                           │
│  🍕 UNICAST = Individual Home Delivery                                      │
│      Netflix sends you a movie                                           │
│      Like ordering pizza to YOUR house                                   │
│                                                                           │
│      Example: 1000 people order same pepperoni pizza                     │
│      → Restaurant makes 1000 separate pizzas                             │
│      → Delivers to 1000 different addresses                              │
│      → Each person gets personal delivery                                │
│      → Very expensive! 1000 drivers, 1000 trips, 1000× gas cost         │
│                                                                           │
│      Network equivalent:                                                 │
│      1000 viewers watch Netflix movie                                    │
│      → Server sends 1000 SEPARATE video streams                          │
│      → Each stream = unique IP address                                   │
│      → 10 Mbps × 1000 viewers = 10 Gbps bandwidth needed!               │
│                                                                           │
│  📺 MULTICAST = Stadium Jumbotron                                           │
│      Live TV broadcast to everyone watching                              │
│      Like putting pizza on big screen for everyone to see                │
│                                                                           │
│      Example: 1000 people want to watch Super Bowl                       │
│      → Stadium puts game on ONE big jumbotron                            │
│      → Everyone watches the SAME display                                 │
│      → Only ONE feed needed                                              │
│      → Super efficient! Same cost for 10 viewers or 10,000               │
│                                                                           │
│      Network equivalent:                                                 │
│      1000 viewers watch live TV channel (239.1.1.1)                      │
│      → Server sends ONE video stream to multicast group                  │
│      → Routers replicate at branch points                                │
│      → 10 Mbps × 1 stream = 10 Mbps bandwidth (1000× savings!)          │
│                                                                           │
│  📢 BROADCAST = Loudspeaker Announcement                                    │
│      Yelling to EVERYONE whether they want it or not                     │
│      Like fire alarm - everyone hears it                                 │
│                                                                           │
│      Example: Network ARP request                                        │
│      → "Who has IP 192.168.1.100? Tell everyone!"                        │
│      → Every device on local network receives it                         │
│      → Only intended device responds                                     │
│      → Everyone else ignores (but still processed interrupt)             │
│                                                                           │
│  🔑 KEY INSIGHT:                                                             │
│  Unicast = Personal delivery (Netflix, YouTube, web browsing)            │
│  Multicast = Shared viewing (live TV, IPTV, large audiences)             │
│  Broadcast = Shout to everyone (ARP, DHCP discovery, local only)         │
│                                                                           │
│  When to use:                                                             │
│  • Unicast: On-demand content, interactive, internet delivery            │
│  • Multicast: Live linear channels, controlled network, large audience   │
│  • Broadcast: Network discovery, local subnet only                       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📊 Unicast Delivery Flow Visualization
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Point-to-Point Unicast Connection                                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Client Request:                                                          │
│  ┌────────────────┐                                                       │
│  │ Viewer Device  │  "I want to watch Movie X"                            │
│  │ 203.0.113.50   │                                                       │
│  └────────┬───────┘                                                       │
│           │ HTTP GET /movie.m3u8                                          │
│           │ Src: 203.0.113.50, Dst: 93.184.216.34                         │
│           ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                    INTERNET ROUTING                             │     │
│  │  (Each router forwards based on destination IP)                 │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│           │                                                               │
│           ▼                                                               │
│  ┌────────────────────┐                                                   │
│  │  CDN Edge Server   │  Nearest Netflix server                           │
│  │  93.184.216.34     │                                                   │
│  └────────┬───────────┘                                                   │
│           │                                                               │
│           │ Server sends UNIQUE stream just for this viewer              │
│           │ TCP connection established                                    │
│           │                                                               │
│           ▼                                                               │
│  ┌───────────────────────────────────────────────────────────┐           │
│  │ HTTP/2 or HLS Stream (Adaptive Bitrate)                  │           │
│  │ ─────────────────────────────────────────────────────────  │           │
│  │ Segment 1: 1080p @ 8 Mbps                                │           │
│  │ Segment 2: 720p @ 4 Mbps (bandwidth dropped)             │           │
│  │ Segment 3: 1080p @ 8 Mbps (recovered)                    │           │
│  │ ─────────────────────────────────────────────────────────  │           │
│  │ • Each segment addressed to 203.0.113.50                  │           │
│  │ • Only this viewer receives these packets                 │           │
│  │ • Can pause, seek, rewind independently                   │           │
│  └───────────────────────────────────────────────────────────┘           │
│           │                                                               │
│           ▼                                                               │
│  ┌────────────────┐                                                       │
│  │ Viewer watches │  Smooth playback, interactive controls                │
│  │ on device      │                                                       │
│  └────────────────┘                                                       │
│                                                                           │
│  KEY CHARACTERISTICS:                                                     │
│  ✅ Dedicated connection (TCP or UDP)                                      │
│  ✅ Interactive (pause, seek, rewind)                                      │
│  ✅ Adaptive quality based on bandwidth                                    │
│  ✅ Works over internet (firewall-friendly)                                │
│  ✅ Scales with CDN (geographic distribution)                              │
│  ❌ Bandwidth scales linearly with viewers                                 │
│  ❌ Server load = N viewers × bitrate                                      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📈 Bandwidth Scaling Comparison
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Unicast vs Multicast Bandwidth Usage (10 Mbps stream example)            │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Scenario: Video streaming at 10 Mbps bitrate                            │
│                                                                           │
│  UNICAST DELIVERY (e.g., Netflix):                                       │
│  ═══════════════════════════════════                                      │
│                                                                           │
│  ┌─────────────┐                                                          │
│  │ Origin CDN  │                                                          │
│  │ Server      │                                                          │
│  └──────┬──────┘                                                          │
│         │                                                                 │
│         │ For each viewer, separate 10 Mbps stream:                      │
│         │                                                                 │
│         ├──────► Viewer 1: 10 Mbps                                       │
│         ├──────► Viewer 2: 10 Mbps                                       │
│         ├──────► Viewer 3: 10 Mbps                                       │
│         ├──────► ...                                                     │
│         └──────► Viewer 1000: 10 Mbps                                    │
│                                                                           │
│  Total bandwidth: 10 Mbps × 1000 = 10,000 Mbps = 10 Gbps                 │
│                                                                           │
│  Bandwidth Growth:                                                        │
│    10 viewers   =    100 Mbps                                            │
│   100 viewers   =  1,000 Mbps (1 Gbps)                                   │
│  1000 viewers   = 10,000 Mbps (10 Gbps)                                  │
│ 10000 viewers   = 100,000 Mbps (100 Gbps) ← Very expensive!              │
│                                                                           │
│  LINEAR SCALING: O(N) where N = number of viewers                        │
│                                                                           │
│  ─────────────────────────────────────────────────────────────────       │
│                                                                           │
│  MULTICAST DELIVERY (e.g., Enterprise IPTV):                             │
│  ═══════════════════════════════════════════════                          │
│                                                                           │
│  ┌─────────────┐                                                          │
│  │ Multicast   │                                                          │
│  │ Source      │                                                          │
│  └──────┬──────┘                                                          │
│         │                                                                 │
│         │ ONE stream to multicast group 239.1.1.1:                       │
│         │                                                                 │
│         └──────► 239.1.1.1 (10 Mbps)                                     │
│                      │                                                    │
│                      ├──► Viewer 1 (joined group)                        │
│                      ├──► Viewer 2 (joined group)                        │
│                      ├──► Viewer 3 (joined group)                        │
│                      ├──► ...                                            │
│                      └──► Viewer 1000 (joined group)                     │
│                                                                           │
│  Total bandwidth: 10 Mbps (fixed, regardless of viewer count!)           │
│                                                                           │
│  Bandwidth Growth:                                                        │
│    10 viewers   =  10 Mbps                                               │
│   100 viewers   =  10 Mbps (same!)                                       │
│  1000 viewers   =  10 Mbps (same!)                                       │
│ 10000 viewers   =  10 Mbps (same!) ← Incredible savings!                 │
│                                                                           │
│  CONSTANT SCALING: O(1) regardless of viewer count                       │
│                                                                           │
│  ═══════════════════════════════════════════════════════════════         │
│                                                                           │
│  COST COMPARISON (1000 viewers):                                          │
│  ┌────────────────────────────────────────────────────────────┐          │
│  │ Delivery Method │ Bandwidth  │ Relative Cost │ Use Case     │          │
│  ├─────────────────┼────────────┼───────────────┼──────────────┤          │
│  │ Unicast         │ 10 Gbps    │ 1000×         │ On-demand    │          │
│  │ Multicast       │ 10 Mbps    │ 1×            │ Live TV      │          │
│  └─────────────────┴────────────┴───────────────┴──────────────┘          │
│                                                                           │
│  WHY UNICAST STILL DOMINATES:                                            │
│  • Works over internet (multicast doesn't traverse internet)              │
│  • CDN geographic distribution (edge caching)                             │
│  • Interactive features (pause, seek, rewind)                             │
│  • Adaptive bitrate (quality adjusts to bandwidth)                        │
│  • Firewall-friendly (standard TCP/UDP)                                   │
│  • No special router configuration needed                                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Unicast vs Multicast vs Broadcast
----------------------------------
+-------------------+---------------+---------------+---------------+
| Feature           | Unicast       | Multicast     | Broadcast     |
+===================+===============+===============+===============+
| Delivery          | One-to-one    | One-to-many   | One-to-all    |
| Bandwidth Usage   | High (N×)     | Efficient     | Wasteful      |
| Addressing        | Single IP     | Group IP      | 255.255...    |
| Routing           | Standard      | Specialized   | Local only    |
| Use Case          | Web, email    | IPTV, live TV | ARP, DHCP     |
+-------------------+---------------+---------------+---------------+

Bandwidth Comparison
--------------------
Example: Streaming 10 Mbps video to 1000 viewers

**Unicast**::

    1000 viewers × 10 Mbps = 10,000 Mbps (10 Gbps)
    Each viewer gets separate stream

**Multicast**::

    1 stream × 10 Mbps = 10 Mbps (1000× savings!)
    Single stream shared by all viewers

Unicast Streaming Protocols
---------------------------
**Adaptive Bitrate (ABR)**:
  - HLS (HTTP Live Streaming)
  - DASH (Dynamic Adaptive Streaming)
  - Uses HTTP over TCP
  - Scales with CDN

**Low-Latency**:
  - SRT (Secure Reliable Transport)
  - Zixi
  - WebRTC
  - Uses UDP for speed

Address Types
-------------
**IPv4 Unicast Ranges**::

    Public:  1.0.0.0 - 223.255.255.255 (excluding private)
    Private: 10.0.0.0/8
             172.16.0.0/12
             192.168.0.0/16
    Loopback: 127.0.0.0/8

**IPv6 Unicast**::

    Global:   2000::/3
    Link-local: fe80::/10
    Unique local: fc00::/7

Routing Behavior
----------------
Unicast packets are routed based on:

1. **Destination IP address**
2. **Routing table lookup** (longest prefix match)
3. **Next-hop determination**
4. **Forwarding to next router**
5. **Repeat until destination reached**

Example routing::

    Source: 192.168.1.10
    Destination: 8.8.8.8 (Google DNS)
    
    Router 1: Forward to ISP gateway
    Router 2: Forward toward Google network
    Router N: Deliver to 8.8.8.8

Load Balancing
--------------
For multiple unicast streams:

**Server-Side**:
  - CDN (Content Delivery Network)
  - Load balancers
  - Geographic distribution

**Client-Side**:
  - Adaptive bitrate switching
  - Failover to backup servers
  - Quality selection

CDN Architecture
----------------
::

    Origin Server
         |
    [CDN Edge Servers Worldwide]
         |
    [Users connect to nearest edge]
    
    Each user: Unicast connection to nearest CDN
    Result: Reduced origin load, better performance

Advantages
----------
- **Flexibility**: Works over internet
- **Simplicity**: Standard routing
- **Interactivity**: Pause, seek, rewind
- **Security**: Private connections
- **CDN Compatible**: Scales globally

Disadvantages
-------------
- **Bandwidth Intensive**: Linear scaling with viewers
- **Server Load**: Each viewer = separate connection
- **Latency**: Higher than multicast (especially with CDN)
- **Cost**: More expensive for large audiences

When to Use Unicast
-------------------
**Use Unicast When**:
  - Viewers geographically distributed
  - Internet delivery required
  - On-demand content (VOD)
  - Interactive features needed
  - Small to medium audience
  - No multicast infrastructure

**Use Multicast When**:
  - Large audience (1000+)
  - Same content to all viewers
  - Controlled network (enterprise/ISP)
  - Live linear channels
  - Bandwidth critical

Real-World Examples
-------------------
**Streaming Services**:
  - Netflix: Unicast HLS/DASH over CDN
  - YouTube: Unicast with adaptive bitrate
  - Twitch: Unicast for interactive streaming

**Enterprise**:
  - Video conferencing: Unicast (Zoom, Teams)
  - File sharing: Unicast (Dropbox, OneDrive)
  - VPN: Unicast encrypted tunnels

Important Notes
---------------
- Most internet traffic is unicast
- Firewall-friendly (works through NAT)
- Can traverse internet without special configuration
- Scales horizontally with CDNs
- TCP provides reliability, UDP provides speed
