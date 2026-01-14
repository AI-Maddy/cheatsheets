═══════════════════════════════════════════════════════════════════════════════
🦈 Wireshark - Network Protocol Analyzer
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
Wireshark is the world's most popular open-source network protocol analyzer. It allows you to capture and interactively browse traffic running on a computer network in real-time or from saved capture files.

Key Features
------------
- **Deep Packet Inspection**: Decodes hundreds of protocols
- **Live Capture**: Real-time packet capture and analysis
- **Filtering**: Display and capture filters for focused analysis
- **Statistics**: Protocol hierarchy, conversations, IO graphs
- **Cross-Platform**: Windows, macOS, Linux support
- **Export Options**: Save as PCAP, CSV, JSON, plain text

Common Use Cases
----------------
1. Network troubleshooting (packet loss, latency)
2. Security analysis (detecting intrusions)
3. Protocol development and debugging
4. Learning network protocols
5. Video streaming quality analysis (RTP/RTCP)

⚡ Essential Display Filters Cheatsheet
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ VIDEO STREAMING FILTERS                                                       │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ RTP (Real-time Transport Protocol):                                          │
│   rtp                                # All RTP packets                       │
│   rtp.ssrc == 0x12345678             # Specific stream by SSRC              │
│   rtp.p_type == 96                   # Specific payload type                │
│   rtp.seq < 100                      # Sequence numbers (detect loss)       │
│   rtp.timestamp                      # Show timestamp field                 │
│                                                                           │
│ RTCP (RTP Control Protocol):                                                 │
│   rtcp                               # All RTCP packets                      │
│   rtcp.pt == 200                     # Sender Reports                       │
│   rtcp.pt == 201                     # Receiver Reports (quality stats)    │
│   rtcp.sender.packetcount            # Packets sent                         │
│   rtcp.sender.octetcount             # Bytes sent                           │
│                                                                           │
│ SMPTE 2110 (Professional Video over IP):                                     │
│   rtp && ip.dst == 239.1.1.1         # Specific multicast video stream     │
│   udp.port == 5004                   # Common RTP port                      │
│   rtp && udp.length > 1400           # Large packets (likely video)        │
│                                                                           │
│ HLS (HTTP Live Streaming):                                                   │
│   http.request.uri contains ".m3u8"   # Playlist requests                   │
│   http.request.uri contains ".ts"     # Transport stream segments          │
│   http.response.code == 200          # Successful downloads                │
│   http.response.code == 404          # Missing segments (error!)           │
│                                                                           │
│ DASH (Dynamic Adaptive Streaming):                                           │
│   http.request.uri contains ".mpd"    # DASH manifest                       │
│   http.request.uri contains ".m4s"    # Media segments                      │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ NETWORK LAYER FILTERS                                                         │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ IP Filtering:                                                                │
│   ip.addr == 192.168.1.100           # Any traffic with this IP             │
│   ip.src == 10.0.0.1                 # Source IP only                       │
│   ip.dst == 10.0.0.2                 # Destination IP only                  │
│   ip.addr == 192.168.1.0/24          # Entire subnet                        │
│   !ip.addr == 192.168.1.100          # Exclude specific IP                  │
│                                                                           │
│ TCP/UDP Ports:                                                               │
│   tcp.port == 80                     # HTTP traffic                         │
│   udp.port == 5004                   # Specific UDP port                    │
│   tcp.dstport == 443                 # HTTPS (destination)                  │
│   tcp.srcport == 1234                # Source port                          │
│   tcp.port >= 49152                  # Ephemeral ports                      │
│                                                                           │
│ Multicast:                                                                   │
│   ip.dst >= 224.0.0.0 && ip.dst <= 239.255.255.255  # All multicast        │
│   igmp                               # IGMP membership                      │
│   ip.dst == 239.1.1.1                # Specific multicast group            │
│                                                                           │
│ Broadcast:                                                                   │
│   eth.dst == ff:ff:ff:ff:ff:ff       # Ethernet broadcast                   │
│   ip.dst == 255.255.255.255          # IP broadcast                         │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ PROTOCOL-SPECIFIC FILTERS                                                     │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ HTTP/HTTPS:                                                                  │
│   http                               # All HTTP                             │
│   http.request                       # HTTP requests only                   │
│   http.response                      # HTTP responses only                  │
│   http.request.method == "GET"       # GET requests                         │
│   http.request.method == "POST"      # POST requests                        │
│   http.host contains "example.com"   # Specific domain                      │
│   http.response.code == 200          # Success                              │
│   http.response.code == 404          # Not found                            │
│   http.response.code >= 400          # Client/server errors                 │
│   http.content_length > 1000000      # Large responses (>1MB)               │
│                                                                           │
│ DNS:                                                                         │
│   dns                                # All DNS queries                      │
│   dns.qry.name contains "example"    # Queries for specific domain         │
│   dns.flags.response == 0            # DNS queries                          │
│   dns.flags.response == 1            # DNS responses                        │
│                                                                           │
│ DHCP:                                                                        │
│   dhcp                               # All DHCP                             │
│   dhcp.option.dhcp == 1              # DHCP Discover                        │
│   dhcp.option.dhcp == 2              # DHCP Offer                           │
│   dhcp.option.dhcp == 3              # DHCP Request                         │
│   dhcp.option.dhcp == 5              # DHCP ACK                             │
│                                                                           │
│ ARP:                                                                         │
│   arp                                # All ARP                              │
│   arp.opcode == 1                    # ARP requests                         │
│   arp.opcode == 2                    # ARP replies                          │
│                                                                           │
│ ICMP (Ping):                                                                 │
│   icmp                               # All ICMP                             │
│   icmp.type == 8                     # Echo request (ping)                  │
│   icmp.type == 0                     # Echo reply (pong)                    │
│   icmp.type == 3                     # Destination unreachable             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ADVANCED FILTERS & COMBINATIONS                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Logical Operators:                                                           │
│   && (and)        tcp.port == 80 && ip.addr == 10.0.0.1                     │
│   || (or)         tcp.port == 80 || tcp.port == 443                          │
│   ! (not)         !arp && !icmp                                              │
│   () grouping     (tcp.port == 80 || tcp.port == 443) && ip.addr == 10.0.0.1│
│                                                                           │
│ TCP Flags:                                                                   │
│   tcp.flags.syn == 1 && tcp.flags.ack == 0   # SYN (connection start)       │
│   tcp.flags.syn == 1 && tcp.flags.ack == 1   # SYN-ACK                      │
│   tcp.flags.reset == 1                       # RST (connection reset)       │
│   tcp.flags.fin == 1                         # FIN (connection close)       │
│   tcp.flags.push == 1                        # PSH (push data)              │
│                                                                           │
│ Packet Size:                                                                 │
│   frame.len > 1500                   # Jumbo frames                         │
│   frame.len < 64                     # Runt frames                          │
│   ip.len > 1400                      # Large IP packets                     │
│                                                                           │
│ Time-based:                                                                  │
│   frame.time_relative > 10           # Packets after 10 seconds            │
│   tcp.time_delta > 1                 # Large gaps between packets          │
│                                                                           │
│ Retransmissions & Errors:                                                    │
│   tcp.analysis.retransmission        # TCP retransmissions                  │
│   tcp.analysis.duplicate_ack         # Duplicate ACKs                       │
│   tcp.analysis.lost_segment          # Lost segments                        │
│   tcp.analysis.out_of_order          # Out of order packets                │
│   tcp.analysis.window_full           # Receive window full                 │
│                                                                           │
│ Expert Info (automatic problem detection):                                   │
│   expert.severity == error           # Errors only                          │
│   expert.severity == warning         # Warnings                             │
│   expert.message contains "retrans"  # Retransmission warnings             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

📊 Useful Analysis Features
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Statistics Menu                                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Protocol Hierarchy:                                                          │
│   Statistics → Protocol Hierarchy                                            │
│   - Shows breakdown of all protocols in capture                              │
│   - Percentage of each protocol                                              │
│   - Good for "what's using bandwidth?"                                       │
│                                                                           │
│ Conversations:                                                               │
│   Statistics → Conversations → TCP/UDP/IP                                    │
│   - Who's talking to whom                                                    │
│   - Bytes transferred per conversation                                       │
│   - Sort by bytes to find heavy users                                        │
│                                                                           │
│ IO Graphs:                                                                   │
│   Statistics → IO Graphs                                                     │
│   - Visual timeline of traffic                                               │
│   - Add filters for comparison (e.g., compare video vs data traffic)         │
│   - Useful for spotting traffic patterns and spikes                          │
│                                                                           │
│ Flow Graph:                                                                  │
│   Statistics → Flow Graph                                                    │
│   - Visual sequence diagram of packet flow                                   │
│   - Great for understanding TCP handshakes                                   │
│                                                                           │
│ RTP Analysis (for video streams):                                            │
│   Telephony → RTP → Stream Analysis                                          │
│   - Jitter, packet loss, sequence errors                                     │
│   - Mean jitter, max jitter                                                  │
│   - Packet loss percentage                                                   │
│   - Delta time between packets                                               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

🎯 Practical Capture Scenarios
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Scenario 1: Video Stream Stuttering - Find the Problem                       │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Steps:                                                                       │
│ ① Start capture on client interface                                          │
│ ② Apply filter: rtp && ip.dst == <video_stream_IP>                           │
│ ③ Statistics → RTP → Stream Analysis                                         │
│    - Check packet loss percentage (should be <0.1%)                          │
│    - Check jitter (should be <50ms for video)                                │
│    - Look for gaps in sequence numbers                                       │
│                                                                           │
│ ④ If seeing packet loss, check:                                              │
│    Filter: icmp.type == 3   (destination unreachable)                        │
│    Filter: tcp.analysis.retransmission                                       │
│                                                                           │
│ ⑤ Check for network congestion:                                              │
│    Statistics → IO Graphs                                                    │
│    - Look for traffic spikes correlating with stutter                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ Scenario 2: Slow Website Loading - Diagnose Latency                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Steps:                                                                       │
│ ① Capture while loading website                                              │
│ ② Filter: http.host == "example.com"                                         │
│ ③ Look at Time column for delays                                             │
│                                                                           │
│ ④ Check TCP handshake time:                                                  │
│    Filter: tcp.flags.syn == 1                                                │
│    - Right-click SYN packet → Follow → TCP Stream                            │
│    - Measure time between SYN → SYN-ACK → ACK                                │
│    - >100ms = network latency issue                                          │
│                                                                           │
│ ⑤ Check DNS resolution time:                                                 │
│    Filter: dns && dns.qry.name contains "example.com"                        │
│    - Time between DNS query and response                                     │
│    - >50ms = DNS server slow                                                 │
│                                                                           │
│ ⑥ Check for TCP issues:                                                      │
│    Filter: tcp.analysis.flags                                                │
│    - Retransmissions = packet loss                                           │
│    - Duplicate ACKs = congestion                                             │
│    - Window full = receiver can't keep up                                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ Capture Filters vs Display Filters
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ CAPTURE FILTERS (BPF syntax - applied during capture)                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Use when: You want to reduce capture file size, focus on specific traffic   │
│                                                                           │
│   host 192.168.1.100                 # Specific host                         │
│   net 192.168.1.0/24                 # Entire subnet                         │
│   port 80                            # Specific port                         │
│   tcp port 443                       # TCP on port 443                       │
│   udp port 5004                      # UDP on port 5004                      │
│   src host 10.0.0.1                  # Source host                           │
│   dst port 80                        # Destination port                      │
│   multicast                          # Multicast traffic only                │
│   not arp and not icmp               # Exclude protocols                     │
│   host 10.0.0.1 and port 5004        # Combine conditions                    │
│   greater 1400                       # Packets larger than 1400 bytes       │
│                                                                           │
│ ⚠ WARNING: Capture filters are permanent! Can't see excluded packets later   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ DISPLAY FILTERS (Wireshark syntax - applied after capture)                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Use when: You want flexibility to explore captured traffic                   │
│                                                                           │
│   ip.addr == 192.168.1.100           # Use Wireshark syntax                 │
│   tcp.port == 80                     # Different from BPF                    │
│   frame.len > 1400                   # More detailed field access            │
│   tcp.flags.syn == 1                 # Access specific flag bits            │
│                                                                           │
│ ✓ ADVANTAGE: Can change filters anytime, all packets remain available       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Useful Display Filters
----------------------
Video streaming::

    rtp                    # All RTP packets
    rtp.ssrc == 0x12345678 # Specific RTP stream
    rtcp                   # RTCP quality reports

HTTP streaming::

    http.request.uri contains "m3u8"  # HLS playlists
    http.response.code == 200         # Successful responses

IP filtering::

    ip.addr == 192.168.1.100  # Packets to/from this IP
    ip.src == 10.0.0.1        # Source IP only
    udp.port == 5004          # Specific UDP port

Troubleshooting Tips
--------------------
**Problem**: Too many packets to analyze
└─ **Solution**: Use capture filters (BPF syntax)
   Example: `host 192.168.1.100 and port 5004`

**Problem**: Can't find specific stream
└─ **Solution**: Right-click packet → Follow → UDP/TCP Stream

**Problem**: Need to see packet timing
└─ **Solution**: Statistics → IO Graphs

Important Features
------------------
- **Capture Filters**: Applied during capture (reduces file size)
- **Display Filters**: Applied after capture (analyze subsets)
- **Color Rules**: Highlight specific packet types
- **Expert Info**: Automatic problem detection
- **Protocol Dissectors**: Decode protocol fields
- **Plugins**: Extend functionality for custom protocols

Common Commands
---------------
Capture to file::

    wireshark -i eth0 -w capture.pcap

Read from file::

    wireshark -r capture.pcap

Command-line capture (tshark)::

    tshark -i eth0 -f "port 5004" -w rtp_capture.pcap
