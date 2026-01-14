═══════════════════════════════════════════════════════════════════════════════
🐚 tcpdump - Command-Line Packet Sniffer
═══════════════════════════════════════════════════════════════════════════════

Overview
--------
tcpdump is a powerful command-line packet analyzer for Unix-like systems. It captures and displays network packets matching a boolean expression, ideal for quick troubleshooting and automated capture scenarios.

Key Features
------------
- **Lightweight**: Minimal resource usage
- **Scriptable**: Perfect for automated monitoring
- **BPF Filters**: Berkeley Packet Filter syntax
- **PCAP Format**: Compatible with Wireshark
- **Remote Capture**: Can pipe to remote analysis

Common Use Cases
----------------
1. Quick network diagnostics
2. Automated packet capture in scripts
3. Remote server troubleshooting (SSH)
4. Baseline traffic analysis
5. Security monitoring

⚡ tcpdump Command Reference
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ BASIC SYNTAX                                                                  │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   tcpdump [options] [filter expression]                                      │
│                                                                           │
│ List interfaces:                                                             │
│   tcpdump -D                         # Show available interfaces             │
│   tcpdump --list-interfaces          # Same as -D                            │
│                                                                           │
│ Capture basics:                                                              │
│   tcpdump -i eth0                    # Capture on eth0                       │
│   tcpdump -i any                     # Capture on all interfaces             │
│   tcpdump -i eth0 -c 100             # Capture 100 packets then stop         │
│   tcpdump -i eth0 -n                 # Don't resolve hostnames (faster)      │
│   tcpdump -i eth0 -nn                # Don't resolve hosts or ports          │
│                                                                           │
│ Write to file:                                                               │
│   tcpdump -i eth0 -w capture.pcap    # Save to file                          │
│   tcpdump -i eth0 -w - > capture.pcap  # Same, using stdout                 │
│   tcpdump -i eth0 -G 3600 -w capture_%Y%m%d_%H%M%S.pcap  # Rotate hourly     │
│                                                                           │
│ Read from file:                                                              │
│   tcpdump -r capture.pcap            # Read and display                      │
│   tcpdump -r capture.pcap -n         # Read without DNS resolution          │
│   tcpdump -r capture.pcap 'port 80'  # Read with filter                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ESSENTIAL OPTIONS                                                             │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Verbosity:                                                                   │
│   -v                    Verbose (more packet details)                        │
│   -vv                   More verbose                                         │
│   -vvv                  Maximum verbosity                                    │
│                                                                           │
│ Output format:                                                               │
│   -n                    Don't resolve IP addresses to hostnames              │
│   -nn                   Don't resolve IPs or ports to names                  │
│   -e                    Print link-layer header (MAC addresses)              │
│   -t                    Don't print timestamp                                │
│   -tttt                 Print human-readable timestamp                       │
│   -A                    Print ASCII packet payload                           │
│   -X                    Print hex and ASCII packet payload                   │
│   -xx                   Print full packet in hex including link layer        │
│                                                                           │
│ Packet capture control:                                                      │
│   -c <count>            Capture N packets then exit                          │
│   -s <snaplen>          Capture only first N bytes of each packet            │
│   -s 0                  Capture full packet (default in newer versions)      │
│   -s 96                 Capture headers only (save disk space)               │
│                                                                           │
│ File rotation:                                                               │
│   -C <size>             Rotate files every N MB                              │
│   -W <count>            Keep only N files (ring buffer)                      │
│   -G <seconds>          Rotate files every N seconds                         │
│                                                                           │
│ Example - Rotate capture every 100MB, keep 10 files:                         │
│   tcpdump -i eth0 -w capture.pcap -C 100 -W 10                               │
│                                                                           │
│ Buffering:                                                                   │
│   -U                    Packet-buffered output (write immediately)           │
│   -l                    Line-buffered output (useful with grep)              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ FILTER EXPRESSIONS (BPF syntax)                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Host filters:                                                                │
│   host 192.168.1.100                 # Traffic to/from this host             │
│   src host 10.0.0.1                  # Source host                           │
│   dst host 10.0.0.2                  # Destination host                      │
│   net 192.168.1.0/24                 # Entire subnet                         │
│   net 192.168.1.0 mask 255.255.255.0 # Same subnet (alternative)             │
│                                                                           │
│ Port filters:                                                                │
│   port 80                            # Port 80 (any protocol)                │
│   tcp port 443                       # TCP port 443                          │
│   udp port 5004                      # UDP port 5004                         │
│   src port 1234                      # Source port                           │
│   dst port 80                        # Destination port                      │
│   portrange 5000-5020                # Port range                            │
│                                                                           │
│ Protocol filters:                                                            │
│   tcp                                # All TCP                               │
│   udp                                # All UDP                               │
│   icmp                               # All ICMP (ping)                       │
│   ip                                 # All IPv4                              │
│   ip6                                # All IPv6                              │
│   arp                                # ARP packets                           │
│                                                                           │
│ Multicast/Broadcast:                                                         │
│   multicast                          # Multicast traffic                     │
│   broadcast                          # Broadcast traffic                     │
│   dst 239.1.1.1                      # Specific multicast group             │
│   ether dst ff:ff:ff:ff:ff:ff        # Ethernet broadcast                    │
│                                                                           │
│ Packet size:                                                                 │
│   less 128                           # Packets smaller than 128 bytes       │
│   greater 1400                       # Packets larger than 1400 bytes       │
│   len > 1500                         # Same as 'greater 1500'               │
│                                                                           │
│ Logical operators:                                                           │
│   and (&&)              host 10.0.0.1 and port 80                            │
│   or (||)               port 80 or port 443                                  │
│   not (!)               not port 22                                          │
│   ()                    (tcp port 80 or tcp port 443) and host 10.0.0.1     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

🎯 Practical Examples
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ VIDEO STREAMING                                                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Capture RTP video stream:                                                    │
│   tcpdump -i eth0 -n 'udp port 5004' -w rtp_stream.pcap                      │
│                                                                           │
│ Capture specific multicast group:                                            │
│   tcpdump -i eth0 -n 'dst 239.1.1.1' -w multicast.pcap                       │
│                                                                           │
│ Capture all multicast traffic:                                               │
│   tcpdump -i eth0 -n 'multicast' -w all_multicast.pcap                       │
│                                                                           │
│ Capture SMPTE 2110 video (large packets, multicast):                         │
│   tcpdump -i eth0 -n 'multicast and greater 1400' -w st2110.pcap             │
│                                                                           │
│ Capture RTCP quality reports (usually port 5005):                            │
│   tcpdump -i eth0 -n 'udp port 5005' -w rtcp.pcap                            │
│                                                                           │
│ Capture HLS/DASH streaming (HTTP):                                           │
│   tcpdump -i eth0 -n 'tcp port 80 or tcp port 443' -w http_stream.pcap       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ NETWORK TROUBLESHOOTING                                                       │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Capture traffic between two hosts:                                           │
│   tcpdump -i eth0 -n 'host 10.0.0.1 and host 10.0.0.2'                       │
│                                                                           │
│ Capture only TCP SYN packets (new connections):                              │
│   tcpdump -i eth0 -n 'tcp[tcpflags] & tcp-syn != 0'                          │
│                                                                           │
│ Capture TCP resets (connection problems):                                    │
│   tcpdump -i eth0 -n 'tcp[tcpflags] & tcp-rst != 0'                          │
│                                                                           │
│ Capture ICMP (ping):                                                         │
│   tcpdump -i eth0 -n 'icmp'                                                  │
│                                                                           │
│ Capture DNS queries:                                                         │
│   tcpdump -i eth0 -n 'udp port 53' -vv                                       │
│                                                                           │
│ Capture ARP traffic:                                                         │
│   tcpdump -i eth0 -n 'arp'                                                   │
│                                                                           │
│ Exclude SSH traffic (when troubleshooting via SSH):                          │
│   tcpdump -i eth0 -n 'not port 22'                                           │
│                                                                           │
│ Capture all traffic except common protocols:                                 │
│   tcpdump -i eth0 -n 'not (port 22 or port 53 or arp or icmp)'               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ PRODUCTION MONITORING                                                         │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Continuous capture with 1-hour rotation:                                     │
│   tcpdump -i eth0 -n -G 3600 -w capture_%Y%m%d_%H%M%S.pcap 'port 5004'       │
│   # Creates: capture_20260113_140000.pcap, capture_20260113_150000.pcap      │
│                                                                           │
│ Ring buffer (keep last 10 files, 100MB each):                                │
│   tcpdump -i eth0 -n -w capture.pcap -C 100 -W 10                            │
│   # Creates: capture.pcap0, capture.pcap1, ... capture.pcap9 (循环覆盖)        │
│                                                                           │
│ Capture headers only (save space):                                           │
│   tcpdump -i eth0 -n -s 96 -w headers.pcap                                   │
│   # Only captures first 96 bytes (headers) of each packet                    │
│                                                                           │
│ Real-time monitoring with human timestamps:                                  │
│   tcpdump -i eth0 -n -tttt                                                   │
│   # Output: 2026-01-13 14:30:45.123456 IP 10.0.0.1.5004 > 239.1.1.1.5004     │
│                                                                           │
│ Count packets per second (with timestamps):                                  │
│   tcpdump -i eth0 -n -tttt | awk '{print $1, $2}' | uniq -c                  │
│                                                                           │
│ Capture and pipe to Wireshark remotely:                                      │
│   ssh user@remote-server 'tcpdump -i eth0 -w - port 5004' | wireshark -k -i -│
│   # -k = start capture immediately, -i - = read from stdin                   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│ ADVANCED FILTERS                                                              │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ Capture specific TCP flags:                                                  │
│   tcpdump 'tcp[tcpflags] & tcp-syn != 0'       # SYN packets                 │
│   tcpdump 'tcp[tcpflags] & tcp-ack != 0'       # ACK packets                 │
│   tcpdump 'tcp[tcpflags] & tcp-rst != 0'       # RST packets                 │
│   tcpdump 'tcp[tcpflags] & tcp-fin != 0'       # FIN packets                 │
│   tcpdump 'tcp[tcpflags] == tcp-syn'           # Only SYN, no other flags    │
│                                                                           │
│ Capture by IP protocol number:                                               │
│   tcpdump 'ip proto 2'                          # IGMP (protocol 2)          │
│   tcpdump 'ip proto 89'                         # OSPF (protocol 89)         │
│                                                                           │
│ Capture by TTL:                                                              │
│   tcpdump 'ip[8] == 1'                          # TTL = 1                    │
│   tcpdump 'ip[8] < 10'                          # TTL < 10                   │
│                                                                           │
│ Capture by DSCP/ToS value:                                                   │
│   tcpdump 'ip[1] & 0xfc == 0xb8'                # DSCP 46 (EF - VoIP)       │
│   tcpdump 'ip[1] & 0xfc == 0x88'                # DSCP 34 (AF41 - Video)    │
│                                                                           │
│ Capture fragmented packets:                                                  │
│   tcpdump 'ip[6:2] & 0x1fff != 0'               # Fragmented IP packets      │
│                                                                           │
│ Capture by VLAN:                                                             │
│   tcpdump 'vlan 10'                             # VLAN ID 10                 │
│   tcpdump 'vlan and host 10.0.0.1'              # Host in any VLAN          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

⚡ tcpdump vs Wireshark vs tshark
─────────────────────────────────────────────────────────────────────────────────
┌───────────────────────────────────────────────────────────────────────────────┐
│ Comparison & When to Use Each                                                │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ tcpdump:                                                                     │
│ ✓ Command-line only (no GUI)                                                │
│ ✓ Minimal resource usage                                                    │
│ ✓ Pre-installed on most Unix systems                                        │
│ ✓ Perfect for remote servers (SSH)                                          │
│ ✓ Easy to script and automate                                               │
│ ✗ Limited protocol decoding                                                 │
│ ✗ Basic filtering during replay                                             │
│ Use when: Quick diagnostics, remote servers, automated monitoring            │
│                                                                           │
│ Wireshark:                                                                   │
│ ✓ Rich GUI with protocol dissectors                                         │
│ ✓ Deep packet inspection (hundreds of protocols)                            │
│ ✓ Visual analysis tools (graphs, flows, conversations)                      │
│ ✓ Advanced filtering and search                                             │
│ ✓ Color coding and expert info                                              │
│ ✗ Requires GUI/X11                                                          │
│ ✗ Higher resource usage                                                     │
│ Use when: Deep analysis, learning protocols, complex troubleshooting         │
│                                                                           │
│ tshark (Wireshark CLI):                                                      │
│ ✓ Command-line with Wireshark's protocol decoding                           │
│ ✓ Scriptable with full dissection                                           │
│ ✓ Wireshark display filters                                                 │
│ ✗ More complex syntax than tcpdump                                           │
│ ✗ Requires Wireshark installation                                           │
│ Use when: Need protocol decoding in scripts/automation                       │
│                                                                           │
│ RECOMMENDED WORKFLOW:                                                        │
│ 1. Use tcpdump for quick capture (especially remote)                         │
│ 2. Transfer .pcap file to local machine                                      │
│ 3. Open in Wireshark for detailed analysis                                   │
│                                                                           │
│ Example:                                                                     │
│   # On remote server                                                         │
│   tcpdump -i eth0 -w /tmp/capture.pcap -c 1000 port 5004                     │
│   # Transfer to local                                                        │
│   scp user@remote:/tmp/capture.pcap .                                        │
│   # Analyze locally                                                          │
│   wireshark capture.pcap                                                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────────┘

Essential Commands
------------------
Basic capture::

    tcpdump -i eth0

Capture to file::

    tcpdump -i eth0 -w capture.pcap

Read from file::

    tcpdump -r capture.pcap

Captue specific host::

    tcpdump -i eth0 host 192.168.1.100

Capture specific port::

    tcpdump -i eth0 port 5004

Common Filters
--------------
Video streaming::

    tcpdump -i eth0 'udp port 5004'          # RTP traffic
    tcpdump -i eth0 'multicast'              # Multicast packets
    tcpdump -i eth0 'dst 239.1.1.1'          # Specific multicast group

HTTP traffic::

    tcpdump -i eth0 'tcp port 80 or tcp port 443'

Packet size filtering::

    tcpdump -i eth0 'greater 1400'          # Large packets (likely video)

Useful Options
--------------
+---------------+----------------------------------------+
| Option        | Description                            |
+===============+========================================+
| -i            | Interface to capture                   |
| -w            | Write to file                          |
| -r            | Read from file                         |
| -c            | Capture N packets then stop            |
| -n            | Don't resolve hostnames                |
| -v/-vv/-vvv   | Verbosity levels                       |
| -A            | Print ASCII payload                    |
| -X            | Print hex and ASCII                    |
| -s            | Snapshot length (0 = full packet)      |
+---------------+----------------------------------------+

Advanced Examples
-----------------
Capture with packet count::

    tcpdump -i eth0 -c 100 -w quick_capture.pcap

Rotate capture files::

    tcpdump -i eth0 -w capture.pcap -C 100 -W 10
    # -C 100 = 100MB per file
    # -W 10 = Keep 10 files (ring buffer)

Capture headers only::

    tcpdump -i eth0 -s 96 port 5004
    # -s 96 = Capture only first 96 bytes

Monitor specific conversation::

    tcpdump -i eth0 'host 10.0.0.1 and host 10.0.0.2'

tcpdump vs Wireshark
--------------------
- **tcpdump**: CLI, scriptable, lightweight, server-friendly
- **Wireshark**: GUI, deep analysis, easier for learning
- **Workflow**: Capture with tcpdump, analyze with Wireshark

Important Notes
---------------
- Requires root/sudo privileges
- Use -n to speed up capture (no DNS lookups)
- Combine with awk/grep for real-time analysis
- Output format compatible with Wireshark
