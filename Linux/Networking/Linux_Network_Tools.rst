===================================
Linux Network Tools Guide
===================================

:Author: Linux Network Documentation
:Date: January 2026
:Version: 1.0

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential Tools
---------------

.. code-block:: bash

   # Connectivity
   ping google.com
   ping6 ipv6.google.com
   
   # DNS lookup
   dig google.com
   nslookup google.com
   host google.com
   
   # Trace route
   traceroute google.com
   mtr google.com
   
   # Port scan
   nmap -p 80,443 example.com
   
   # Network stats
   netstat -tuln
   ss -tuln
   
   # Capture packets
   tcpdump -i eth0 port 80
   
   # Transfer speed
   iperf3 -s  # Server
   iperf3 -c server_ip  # Client
   
   # HTTP requests
   curl -I https://example.com
   wget https://example.com/file.txt

Diagnostic Tools
================

ping
----

.. code-block:: bash

   # Basic ping
   ping google.com
   
   # IPv6
   ping6 ipv6.google.com
   
   # Count
   ping -c 4 google.com
   
   # Interval
   ping -i 0.5 google.com
   
   # Packet size
   ping -s 1000 google.com
   
   # Flood ping (requires root)
   ping -f google.com
   
   # Set TTL
   ping -t 64 google.com
   
   # Don't fragment
   ping -M do -s 1472 google.com

traceroute / mtr
----------------

.. code-block:: bash

   # Basic traceroute
   traceroute google.com
   
   # IPv6
   traceroute6 ipv6.google.com
   
   # Don't resolve hostnames
   traceroute -n google.com
   
   # Use ICMP instead of UDP
   traceroute -I google.com
   
   # TCP traceroute
   traceroute -T -p 80 google.com
   
   # MTR (My Traceroute) - continuous
   mtr google.com
   
   # MTR report mode
   mtr --report google.com
   
   # MTR with TCP
   mtr --tcp -P 443 google.com

DNS Tools
=========

dig
---

.. code-block:: bash

   # Basic lookup
   dig google.com
   
   # Short answer
   dig google.com +short
   
   # Specific record type
   dig google.com A
   dig google.com AAAA
   dig google.com MX
   dig google.com NS
   dig google.com TXT
   dig google.com SOA
   
   # Reverse lookup
   dig -x 8.8.8.8
   
   # Use specific DNS server
   dig @8.8.8.8 google.com
   
   # Trace DNS resolution
   dig google.com +trace
   
   # Show only answer section
   dig google.com +noall +answer
   
   # Query all records
   dig google.com ANY

nslookup
--------

.. code-block:: bash

   # Basic lookup
   nslookup google.com
   
   # Use specific server
   nslookup google.com 8.8.8.8
   
   # Reverse lookup
   nslookup 8.8.8.8
   
   # Interactive mode
   nslookup
   > server 8.8.8.8
   > set type=MX
   > google.com

host
----

.. code-block:: bash

   # Basic lookup
   host google.com
   
   # All records
   host -a google.com
   
   # Specific type
   host -t MX google.com
   
   # Reverse lookup
   host 8.8.8.8
   
   # Use specific server
   host google.com 8.8.8.8

Network Statistics
==================

netstat (Legacy)
----------------

.. code-block:: bash

   # Show all connections
   netstat -a
   
   # TCP connections
   netstat -t
   
   # UDP connections
   netstat -u
   
   # Listening ports
   netstat -l
   
   # Listening TCP ports
   netstat -tln
   
   # Show programs
   netstat -tlnp
   
   # Routing table
   netstat -r
   
   # Interface statistics
   netstat -i
   
   # Continuous monitoring
   netstat -c

ss (Modern Replacement)
-----------------------

.. code-block:: bash

   # Show all sockets
   ss -a
   
   # TCP sockets
   ss -t
   
   # UDP sockets
   ss -u
   
   # Listening sockets
   ss -l
   
   # Listening TCP with process
   ss -tlnp
   
   # Show TCP statistics
   ss -s
   
   # Filter by state
   ss state established
   ss state listening
   
   # Filter by port
   ss -t sport = :80
   ss -t dport = :443
   
   # Show timer information
   ss -to
   
   # Show memory usage
   ss -tm

lsof
----

.. code-block:: bash

   # Network connections
   lsof -i
   
   # TCP connections
   lsof -i TCP
   
   # Specific port
   lsof -i :80
   lsof -i :443
   
   # Specific protocol and port
   lsof -i TCP:80
   
   # By user
   lsof -u www-data -i
   
   # Established connections
   lsof -i -sTCP:ESTABLISHED

Packet Capture
==============

tcpdump
-------

.. code-block:: bash

   # Capture on interface
   tcpdump -i eth0
   
   # Capture specific port
   tcpdump -i eth0 port 80
   tcpdump -i eth0 port 443
   
   # Capture host
   tcpdump -i eth0 host 192.168.1.10
   
   # Capture network
   tcpdump -i eth0 net 192.168.1.0/24
   
   # Save to file
   tcpdump -i eth0 -w capture.pcap
   
   # Read from file
   tcpdump -r capture.pcap
   
   # Verbose output
   tcpdump -i eth0 -v
   tcpdump -i eth0 -vv
   tcpdump -i eth0 -vvv
   
   # Show ASCII
   tcpdump -i eth0 -A
   
   # Show hex and ASCII
   tcpdump -i eth0 -XX
   
   # Don't resolve hostnames
   tcpdump -i eth0 -n
   
   # Don't resolve ports
   tcpdump -i eth0 -nn
   
   # Capture count
   tcpdump -i eth0 -c 100
   
   # Complex filters
   tcpdump -i eth0 'tcp and port 80'
   tcpdump -i eth0 'tcp and (port 80 or port 443)'
   tcpdump -i eth0 'src host 192.168.1.10 and dst port 80'
   tcpdump -i eth0 'icmp'
   
   # Capture HTTP GET requests
   tcpdump -i eth0 -s 0 -A 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
   
   # Capture DNS queries
   tcpdump -i eth0 port 53

tshark (Wireshark CLI)
----------------------

.. code-block:: bash

   # Capture on interface
   tshark -i eth0
   
   # Capture with filter
   tshark -i eth0 -f "port 80"
   
   # Display filter
   tshark -i eth0 -Y "http"
   
   # Save to file
   tshark -i eth0 -w capture.pcap
   
   # Read from file
   tshark -r capture.pcap
   
   # Show specific fields
   tshark -i eth0 -T fields -e ip.src -e ip.dst -e tcp.port
   
   # Statistics
   tshark -r capture.pcap -q -z io,phs

Port Scanning
=============

nmap
----

.. code-block:: bash

   # Basic scan
   nmap 192.168.1.10
   
   # Scan specific ports
   nmap -p 80,443 192.168.1.10
   
   # Scan port range
   nmap -p 1-1000 192.168.1.10
   
   # Scan all ports
   nmap -p- 192.168.1.10
   
   # Fast scan (top 100 ports)
   nmap -F 192.168.1.10
   
   # Service version detection
   nmap -sV 192.168.1.10
   
   # OS detection
   nmap -O 192.168.1.10
   
   # Aggressive scan
   nmap -A 192.168.1.10
   
   # TCP SYN scan
   nmap -sS 192.168.1.10
   
   # TCP connect scan
   nmap -sT 192.168.1.10
   
   # UDP scan
   nmap -sU 192.168.1.10
   
   # Scan network
   nmap 192.168.1.0/24
   
   # Ping scan (host discovery)
   nmap -sn 192.168.1.0/24
   
   # No ping
   nmap -Pn 192.168.1.10
   
   # Script scan
   nmap --script=default 192.168.1.10
   nmap --script=vuln 192.168.1.10

nc (netcat)
-----------

.. code-block:: bash

   # Port scan
   nc -zv 192.168.1.10 1-1000
   
   # TCP connect
   nc 192.168.1.10 80
   
   # UDP connect
   nc -u 192.168.1.10 53
   
   # Listen on port
   nc -l -p 8080
   
   # Transfer file
   # Receiver
   nc -l -p 8080 > file.txt
   # Sender
   nc 192.168.1.10 8080 < file.txt
   
   # Banner grabbing
   echo "" | nc 192.168.1.10 80
   
   # Chat
   # Server
   nc -l -p 8080
   # Client
   nc 192.168.1.10 8080

Performance Testing
===================

iperf3
------

.. code-block:: bash

   # Server
   iperf3 -s
   
   # Client
   iperf3 -c server_ip
   
   # Set duration
   iperf3 -c server_ip -t 30
   
   # Parallel streams
   iperf3 -c server_ip -P 4
   
   # UDP test
   iperf3 -c server_ip -u
   
   # Bidirectional test
   iperf3 -c server_ip --bidir
   
   # Reverse direction
   iperf3 -c server_ip -R
   
   # JSON output
   iperf3 -c server_ip -J

HTTP Tools
==========

curl
----

.. code-block:: bash

   # Basic request
   curl https://example.com
   
   # Save to file
   curl -o output.html https://example.com
   curl -O https://example.com/file.txt
   
   # Follow redirects
   curl -L https://example.com
   
   # Show headers only
   curl -I https://example.com
   
   # Show headers with body
   curl -i https://example.com
   
   # Verbose
   curl -v https://example.com
   
   # POST request
   curl -X POST https://example.com/api
   
   # POST data
   curl -X POST -d "key=value" https://example.com/api
   
   # POST JSON
   curl -X POST -H "Content-Type: application/json" \
        -d '{"key":"value"}' https://example.com/api
   
   # Custom header
   curl -H "Authorization: Bearer token" https://example.com/api
   
   # Basic auth
   curl -u username:password https://example.com
   
   # Download with progress
   curl -# -O https://example.com/largefile.iso
   
   # Resume download
   curl -C - -O https://example.com/largefile.iso
   
   # Rate limit
   curl --limit-rate 1M -O https://example.com/file.txt
   
   # Timing
   curl -w "@curl-format.txt" -o /dev/null -s https://example.com

wget
----

.. code-block:: bash

   # Download file
   wget https://example.com/file.txt
   
   # Save as different name
   wget -O output.txt https://example.com/file.txt
   
   # Continue download
   wget -c https://example.com/largefile.iso
   
   # Download in background
   wget -b https://example.com/file.txt
   
   # Recursive download
   wget -r https://example.com
   
   # Mirror site
   wget -m https://example.com
   
   # Download list of URLs
   wget -i urls.txt
   
   # Limit rate
   wget --limit-rate=1M https://example.com/file.txt
   
   # Spider (check links)
   wget --spider https://example.com
   
   # Retry
   wget --tries=10 https://example.com/file.txt

ARP Tools
=========

.. code-block:: bash

   # Show ARP cache
   arp -a
   ip neigh show
   
   # Add static entry
   arp -s 192.168.1.10 00:11:22:33:44:55
   ip neigh add 192.168.1.10 lladdr 00:11:22:33:44:55 dev eth0
   
   # Delete entry
   arp -d 192.168.1.10
   ip neigh del 192.168.1.10 dev eth0
   
   # Flush ARP cache
   ip neigh flush all

Network Monitoring
==================

iftop
-----

.. code-block:: bash

   # Monitor interface
   iftop -i eth0
   
   # Show port numbers
   iftop -i eth0 -P
   
   # No DNS resolution
   iftop -i eth0 -n

nethogs
-------

.. code-block:: bash

   # Monitor by process
   nethogs eth0
   
   # View specific interface
   nethogs eth0 eth1

nload
-----

.. code-block:: bash

   # Monitor bandwidth
   nload
   
   # Specific interface
   nload eth0
   
   # Multiple interfaces
   nload eth0 eth1

bmon
----

.. code-block:: bash

   # Bandwidth monitor
   bmon
   
   # Specific interface
   bmon -p eth0

Best Practices
==============

1. **Use ss instead of netstat**
2. **Save tcpdump captures** for analysis
3. **Use filters** to reduce packet capture size
4. **Test with multiple tools** to verify results
5. **Document network baselines**
6. **Monitor continuously** with tools like mtr
7. **Use wireshark** for detailed analysis
8. **Scan responsibly** - own systems only
9. **Rate limit** downloads to avoid congestion
10. **Keep tools updated**

Common Pitfalls
===============

1. **Running tcpdump without filters** (too much data)
2. **Not using -n** (slow DNS lookups)
3. **Forgetting sudo** for privileged operations
4. **Not saving captures** before analysis
5. **Scanning without permission**
6. **Not checking tool versions**

Quick Troubleshooting
======================

.. code-block:: bash

   # Can't reach host
   ping host
   traceroute host
   mtr host
   
   # DNS issues
   dig example.com
   dig @8.8.8.8 example.com
   
   # Port not reachable
   nc -zv host port
   nmap -p port host
   
   # High bandwidth usage
   iftop -i eth0
   nethogs eth0
   
   # Connection issues
   ss -tlnp
   netstat -tlnp
   
   # Packet loss
   ping -c 100 host
   mtr --report host
   
   # Capture traffic
   tcpdump -i eth0 -w problem.pcap
   tshark -i eth0 -w problem.pcap

See Also
========

- Linux_Network_Configuration.rst
- Linux_Network_Protocols.rst
- Linux_Network_Performance.rst

References
==========

- man tcpdump
- man ss
- man curl
- man nmap
