===================================
Linux Network Protocols Guide
===================================

:Author: Linux Network Documentation
:Date: January 2026
:Version: 1.0

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Protocol Stack
--------------

.. code-block:: text

   Application Layer:  HTTP, FTP, SSH, DNS, SMTP
   Transport Layer:    TCP, UDP
   Network Layer:      IP, ICMP, IGMP
   Data Link Layer:    Ethernet, ARP
   Physical Layer:     Cables, NICs

Common Protocols
----------------

.. code-block:: bash

   # HTTP/HTTPS (80/443)
   curl https://example.com
   
   # SSH (22)
   ssh user@host
   
   # FTP (21)
   ftp ftp.example.com
   
   # DNS (53)
   dig example.com
   
   # SMTP (25, 587)
   telnet mail.example.com 25
   
   # ICMP
   ping example.com
   traceroute example.com

TCP/IP
======

TCP Fundamentals
----------------

.. code-block:: text

   Features:
   - Connection-oriented
   - Reliable delivery
   - Ordered data transfer
   - Flow control
   - Congestion control
   
   TCP Header:
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

TCP States
----------

.. code-block:: text

   CLOSED       -> Initial state
   LISTEN       -> Waiting for connection
   SYN-SENT     -> Sent SYN, waiting for SYN-ACK
   SYN-RECEIVED -> Received SYN, sent SYN-ACK
   ESTABLISHED  -> Connection established
   FIN-WAIT-1   -> Sent FIN
   FIN-WAIT-2   -> Received ACK of FIN
   CLOSE-WAIT   -> Received FIN, waiting to close
   CLOSING      -> Both sides closing
   LAST-ACK     -> Waiting for final ACK
   TIME-WAIT    -> Waiting for network to clear

.. code-block:: bash

   # View TCP connections by state
   ss -tan state established
   ss -tan state time-wait
   ss -tan state close-wait
   
   # Count connections by state
   ss -tan | awk '{print $1}' | sort | uniq -c

UDP Fundamentals
----------------

.. code-block:: text

   Features:
   - Connectionless
   - Unreliable delivery
   - No ordering guarantee
   - No flow control
   - Minimal overhead
   
   UDP Header:
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |            Length             |           Checksum            |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

IP Protocol
===========

IPv4
----

.. code-block:: text

   IPv4 Header:
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   
   Address Classes:
   Class A: 0.0.0.0     - 127.255.255.255  (/8)
   Class B: 128.0.0.0   - 191.255.255.255  (/16)
   Class C: 192.0.0.0   - 223.255.255.255  (/24)
   Class D: 224.0.0.0   - 239.255.255.255  (Multicast)
   Class E: 240.0.0.0   - 255.255.255.255  (Reserved)
   
   Private Ranges:
   10.0.0.0/8        (10.0.0.0 - 10.255.255.255)
   172.16.0.0/12     (172.16.0.0 - 172.31.255.255)
   192.168.0.0/16    (192.168.0.0 - 192.168.255.255)

.. code-block:: bash

   # View IP routing
   ip route show
   
   # IP statistics
   ip -s link show
   
   # netstat IP statistics
   netstat -s | grep -A 10 "Ip:"

IPv6
----

.. code-block:: text

   IPv6 Header:
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version| Traffic Class |           Flow Label                  |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Payload Length        |  Next Header  |   Hop Limit   |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               |
   +                                                               +
   |                                                               |
   +                         Source Address                        +
   |                                                               |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                                                               |
   +                                                               +
   |                                                               |
   +                      Destination Address                      +
   |                                                               |
   +                                                               +
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   
   Address Types:
   ::1/128                  Loopback
   ::/128                   Unspecified
   fe80::/10                Link-local
   fc00::/7                 Unique local (ULA)
   2000::/3                 Global unicast
   ff00::/8                 Multicast

.. code-block:: bash

   # View IPv6 addresses
   ip -6 addr show
   
   # IPv6 routes
   ip -6 route show
   
   # Ping IPv6
   ping6 ipv6.google.com
   
   # Traceroute IPv6
   traceroute6 ipv6.google.com

ICMP
====

ICMP Messages
-------------

.. code-block:: text

   Type 0:  Echo Reply (ping response)
   Type 3:  Destination Unreachable
   Type 5:  Redirect
   Type 8:  Echo Request (ping)
   Type 11: Time Exceeded (traceroute)
   
   Destination Unreachable Codes:
   0:  Network Unreachable
   1:  Host Unreachable
   2:  Protocol Unreachable
   3:  Port Unreachable
   4:  Fragmentation Needed
   5:  Source Route Failed

.. code-block:: bash

   # Send ICMP echo request
   ping -c 4 8.8.8.8
   
   # Capture ICMP packets
   tcpdump -i eth0 icmp
   
   # Statistics
   netstat -s | grep -A 20 "Icmp:"

DNS
===

DNS Record Types
----------------

.. code-block:: text

   A      IPv4 address
   AAAA   IPv6 address
   CNAME  Canonical name (alias)
   MX     Mail exchanger
   NS     Name server
   PTR    Pointer (reverse DNS)
   SOA    Start of authority
   TXT    Text record
   SRV    Service record

.. code-block:: bash

   # Query A record
   dig example.com A
   host -t A example.com
   nslookup -type=A example.com
   
   # Query AAAA record
   dig example.com AAAA
   
   # Query MX records
   dig example.com MX
   host -t MX example.com
   
   # Query NS records
   dig example.com NS
   
   # Query all records
   dig example.com ANY
   
   # Reverse DNS lookup
   dig -x 8.8.8.8
   host 8.8.8.8
   
   # Trace DNS resolution
   dig example.com +trace
   
   # Use specific DNS server
   dig @8.8.8.8 example.com

DNS Zone Transfer
-----------------

.. code-block:: bash

   # Zone transfer (AXFR)
   dig @ns1.example.com example.com AXFR
   
   # Incremental zone transfer (IXFR)
   dig @ns1.example.com example.com IXFR

HTTP/HTTPS
==========

HTTP Methods
------------

.. code-block:: text

   GET     Retrieve resource
   POST    Submit data
   PUT     Update resource
   DELETE  Delete resource
   HEAD    Get headers only
   OPTIONS Get supported methods
   PATCH   Partial update

HTTP Status Codes
-----------------

.. code-block:: text

   1xx Informational:
   100 Continue
   101 Switching Protocols
   
   2xx Success:
   200 OK
   201 Created
   204 No Content
   
   3xx Redirection:
   301 Moved Permanently
   302 Found
   304 Not Modified
   
   4xx Client Error:
   400 Bad Request
   401 Unauthorized
   403 Forbidden
   404 Not Found
   
   5xx Server Error:
   500 Internal Server Error
   502 Bad Gateway
   503 Service Unavailable

.. code-block:: bash

   # GET request
   curl -X GET https://api.example.com/users
   
   # POST request
   curl -X POST -d '{"name":"John"}' \
        -H "Content-Type: application/json" \
        https://api.example.com/users
   
   # PUT request
   curl -X PUT -d '{"name":"Jane"}' \
        -H "Content-Type: application/json" \
        https://api.example.com/users/1
   
   # DELETE request
   curl -X DELETE https://api.example.com/users/1
   
   # HEAD request
   curl -I https://example.com
   
   # OPTIONS request
   curl -X OPTIONS https://api.example.com

HTTPS/TLS
---------

.. code-block:: bash

   # Check TLS version
   openssl s_client -connect example.com:443 -tls1_2
   openssl s_client -connect example.com:443 -tls1_3
   
   # Show certificate
   openssl s_client -connect example.com:443 -showcerts
   
   # Check certificate expiry
   echo | openssl s_client -connect example.com:443 2>/dev/null | \
       openssl x509 -noout -dates
   
   # Test cipher suites
   nmap --script ssl-enum-ciphers -p 443 example.com

DHCP
====

DHCP Process
------------

.. code-block:: text

   DORA Process:
   1. Discover  - Client broadcasts DHCPDISCOVER
   2. Offer     - Server responds with DHCPOFFER
   3. Request   - Client sends DHCPREQUEST
   4. Acknowledge - Server sends DHCPACK

.. code-block:: bash

   # Request DHCP lease
   dhclient eth0
   
   # Release DHCP lease
   dhclient -r eth0
   
   # View DHCP leases
   cat /var/lib/dhcp/dhclient.leases
   
   # Capture DHCP traffic
   tcpdump -i eth0 port 67 or port 68

ARP
===

ARP Process
-----------

.. code-block:: text

   Address Resolution Protocol (ARP):
   Maps IP addresses to MAC addresses
   
   ARP Request:  "Who has IP 192.168.1.10?"
   ARP Reply:    "192.168.1.10 is at MAC 00:11:22:33:44:55"

.. code-block:: bash

   # View ARP cache
   arp -a
   ip neigh show
   
   # Send ARP request
   arping 192.168.1.10
   
   # Capture ARP traffic
   tcpdump -i eth0 arp
   
   # Clear ARP cache
   ip neigh flush all

NAT
===

NAT Types
---------

.. code-block:: text

   SNAT (Source NAT):
   - Changes source IP of outgoing packets
   - Used for internet access from private networks
   
   DNAT (Destination NAT):
   - Changes destination IP of incoming packets
   - Used for port forwarding
   
   Masquerading:
   - SNAT with dynamic IP address

.. code-block:: bash

   # Enable IP forwarding
   sysctl -w net.ipv4.ip_forward=1
   echo 1 > /proc/sys/net/ipv4/ip_forward
   
   # Masquerading (iptables)
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # SNAT
   iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 \
       -j SNAT --to-source 203.0.113.10
   
   # DNAT (port forwarding)
   iptables -t nat -A PREROUTING -p tcp --dport 80 \
       -j DNAT --to-destination 192.168.1.10:8080
   
   # View NAT table
   iptables -t nat -L -v

Multicast
=========

Multicast Addresses
-------------------

.. code-block:: text

   IPv4 Multicast: 224.0.0.0 - 239.255.255.255
   
   Well-known addresses:
   224.0.0.1   All systems on subnet
   224.0.0.2   All routers on subnet
   224.0.0.5   OSPF routers
   224.0.0.6   OSPF designated routers
   224.0.0.9   RIP v2 routers
   224.0.0.13  PIM routers

.. code-block:: bash

   # Join multicast group
   ip maddr add 224.0.0.1 dev eth0
   
   # View multicast groups
   ip maddr show
   
   # Send multicast
   socat - UDP4-DATAGRAM:224.0.0.1:1234,ip-multicast-ttl=1
   
   # Receive multicast
   socat UDP4-RECV:1234,ip-add-membership=224.0.0.1:eth0 -

Protocol Analysis
=================

Packet Analysis
---------------

.. code-block:: bash

   # Capture and analyze TCP handshake
   tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn) != 0'
   
   # Capture TCP RST
   tcpdump -i eth0 'tcp[tcpflags] & (tcp-rst) != 0'
   
   # Capture TCP FIN
   tcpdump -i eth0 'tcp[tcpflags] & (tcp-fin) != 0'
   
   # Analyze protocol distribution
   tshark -r capture.pcap -q -z io,phs
   
   # Protocol hierarchy statistics
   tshark -r capture.pcap -q -z io,phs

Performance Metrics
-------------------

.. code-block:: bash

   # TCP window size
   ss -ti
   
   # Retransmissions
   netstat -s | grep retransmit
   
   # Packet loss
   ss -ti | grep -i loss
   
   # Round-trip time
   ping -c 10 8.8.8.8 | tail -1

Best Practices
==============

1. **Use TCP** for reliable communication
2. **Use UDP** for low-latency applications
3. **Enable IPv6** alongside IPv4
4. **Monitor protocol statistics**
5. **Understand headers** for troubleshooting
6. **Use appropriate** MTU/MSS values
7. **Enable ECN** for congestion notification
8. **Monitor retransmissions**
9. **Use TLS 1.2+** for encryption
10. **Implement timeout** mechanisms

Common Pitfalls
===============

1. **MTU/MSS mismatch** causing fragmentation
2. **Not handling** TCP retransmissions
3. **UDP packet loss** without detection
4. **Ignoring TIME_WAIT** sockets
5. **Not monitoring** protocol errors
6. **Firewall blocking** ICMP

Protocol Tuning
===============

.. code-block:: bash

   # TCP window scaling
   sysctl -w net.ipv4.tcp_window_scaling=1
   
   # TCP timestamps
   sysctl -w net.ipv4.tcp_timestamps=1
   
   # TCP SACK
   sysctl -w net.ipv4.tcp_sack=1
   
   # TCP keepalive
   sysctl -w net.ipv4.tcp_keepalive_time=300
   sysctl -w net.ipv4.tcp_keepalive_intvl=30
   sysctl -w net.ipv4.tcp_keepalive_probes=5
   
   # TCP buffer sizes
   sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
   sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"
   
   # View all TCP settings
   sysctl -a | grep tcp

See Also
========

- Linux_Network_Configuration.rst
- Linux_Network_Tools.rst
- Linux_Network_Performance.rst
- Socket_Programming.rst

References
==========

- RFC 793 (TCP)
- RFC 768 (UDP)
- RFC 791 (IP)
- RFC 792 (ICMP)
- RFC 1035 (DNS)
