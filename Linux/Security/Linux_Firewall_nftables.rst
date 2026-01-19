===================================
Linux nftables Firewall Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: nftables - Modern Linux firewall framework

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential nftables Commands
----------------------------

.. code-block:: bash

   # View current ruleset
   sudo nft list ruleset
   sudo nft list table inet filter
   sudo nft list chain inet filter input
   
   # Save ruleset
   sudo nft list ruleset > /etc/nftables.conf
   
   # Load ruleset
   sudo nft -f /etc/nftables.conf
   
   # Flush ruleset
   sudo nft flush ruleset
   
   # Add rule
   sudo nft add rule inet filter input tcp dport 22 accept
   
   # Delete rule by handle
   sudo nft -a list chain inet filter input
   sudo nft delete rule inet filter input handle 10

Quick Firewall Setup
---------------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   
   # Flush existing rules
   flush ruleset
   
   # Define table
   table inet filter {
     # Input chain
     chain input {
       type filter hook input priority 0; policy drop;
       
       # Allow loopback
       iif lo accept
       
       # Allow established/related
       ct state established,related accept
       
       # Drop invalid
       ct state invalid drop
       
       # Allow ICMP
       ip protocol icmp accept
       ip6 nexthdr icmpv6 accept
       
       # Allow SSH
       tcp dport 22 ct state new accept
       
       # Allow HTTP/HTTPS
       tcp dport { 80, 443 } ct state new accept
     }
     
     # Forward chain
     chain forward {
       type filter hook forward priority 0; policy drop;
     }
     
     # Output chain
     chain output {
       type filter hook output priority 0; policy accept;
     }
   }

Apply this configuration:

.. code-block:: bash

   sudo nft -f /etc/nftables.conf
   sudo systemctl enable nftables
   sudo systemctl start nftables

nftables vs iptables
=====================

Key Differences
---------------

.. code-block:: text

   Advantages of nftables:
   
   1. Single framework - Replaces iptables, ip6tables, arptables, ebtables
   2. Better performance - Improved packet classification
   3. Simpler syntax - More readable and consistent
   4. Atomic updates - All-or-nothing rule updates
   5. Better scripting - Native scripting support
   6. Sets and maps - Efficient large rule sets
   7. No built-in chains - Create only what you need
   8. Better userspace/kernel API
   
   Migration:
   - iptables-translate tool converts rules
   - Can run simultaneously (different tables)
   - nft replaces all *tables utilities

Syntax Comparison
-----------------

.. code-block:: bash

   # iptables
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   
   # nftables
   nft add rule inet filter input tcp dport 80 accept
   
   # iptables NAT
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # nftables NAT
   nft add rule inet nat postrouting oif eth0 masquerade

Basic Concepts
==============

Tables
------

.. code-block:: bash

   # Create table (address family: ip, ip6, inet, arp, bridge, netdev)
   nft add table inet filter
   nft add table ip nat
   
   # List tables
   nft list tables
   
   # List table contents
   nft list table inet filter
   
   # Delete table
   nft delete table inet filter
   
   # Address families:
   # inet: IPv4 and IPv6 (recommended for most uses)
   # ip: IPv4 only
   # ip6: IPv6 only
   # arp: ARP
   # bridge: Bridge filtering
   # netdev: Ingress filtering

Chains
------

.. code-block:: bash

   # Create base chain (attached to hook)
   nft add chain inet filter input { type filter hook input priority 0 \; policy accept \; }
   
   # Create regular chain (not attached)
   nft add chain inet filter custom_chain
   
   # List chains
   nft list chains
   
   # List chain rules
   nft list chain inet filter input
   
   # Delete chain
   nft delete chain inet filter custom_chain
   
   # Chain types:
   # filter: Standard packet filtering
   # nat: Network Address Translation
   # route: Reroute packets
   
   # Hooks:
   # prerouting: Before routing decision
   # input: Packets to local system
   # forward: Packets routed through system
   # output: Packets from local system
   # postrouting: After routing decision
   # ingress: Very early filtering (netdev family)
   
   # Priority (lower = earlier):
   # Negative: Before connection tracking
   # 0: Default
   # Positive: After connection tracking

Rules
-----

.. code-block:: bash

   # Add rule to end
   nft add rule inet filter input tcp dport 22 accept
   
   # Insert rule at beginning
   nft insert rule inet filter input tcp dport 22 accept
   
   # Add rule at position (by handle)
   nft -a list chain inet filter input
   nft add rule inet filter input position 10 tcp dport 80 accept
   
   # Replace rule
   nft replace rule inet filter input handle 10 tcp dport 8080 accept
   
   # Delete rule
   nft delete rule inet filter input handle 10

Match Criteria
==============

Protocol Matching
-----------------

.. code-block:: bash

   # TCP
   nft add rule inet filter input tcp dport 80 accept
   nft add rule inet filter input tcp dport 1024-65535 accept
   nft add rule inet filter input tcp flags syn tcp dport 80 accept
   
   # UDP
   nft add rule inet filter input udp dport 53 accept
   
   # ICMP
   nft add rule inet filter input icmp type echo-request accept
   nft add rule inet filter input ip protocol icmp accept
   
   # ICMPv6
   nft add rule inet filter input icmpv6 type { echo-request, echo-reply } accept
   nft add rule inet filter input ip6 nexthdr icmpv6 accept
   
   # Multiple protocols
   nft add rule inet filter input ip protocol { tcp, udp } accept

Address Matching
----------------

.. code-block:: bash

   # Source IP
   nft add rule inet filter input ip saddr 192.168.1.100 accept
   
   # Source network
   nft add rule inet filter input ip saddr 192.168.1.0/24 accept
   
   # Destination IP
   nft add rule inet filter output ip daddr 10.0.0.1 accept
   
   # IPv6
   nft add rule inet filter input ip6 saddr 2001:db8::/32 accept
   
   # Negate (NOT)
   nft add rule inet filter input ip saddr != 192.168.1.0/24 drop
   
   # Multiple IPs
   nft add rule inet filter input ip saddr { 192.168.1.1, 192.168.1.2, 192.168.1.3 } accept

Interface Matching
------------------

.. code-block:: bash

   # Input interface
   nft add rule inet filter input iif eth0 accept
   
   # Output interface
   nft add rule inet filter output oif eth1 accept
   
   # Interface wildcard
   nft add rule inet filter input iifname "eth*" accept
   
   # Interface type
   nft add rule inet filter input iiftype ether accept

Port Matching
-------------

.. code-block:: bash

   # Single port
   nft add rule inet filter input tcp dport 80 accept
   
   # Port range
   nft add rule inet filter input tcp dport 1024-65535 accept
   
   # Multiple ports (anonymous set)
   nft add rule inet filter input tcp dport { 80, 443, 8080 } accept
   
   # Source port
   nft add rule inet filter input tcp sport 1024-65535 accept
   
   # Both source and destination
   nft add rule inet filter input tcp sport 1024-65535 tcp dport 80 accept

Connection Tracking
===================

Conntrack States
----------------

.. code-block:: bash

   # Allow established/related
   nft add rule inet filter input ct state established,related accept
   
   # Allow new connections
   nft add rule inet filter input ct state new tcp dport 80 accept
   
   # Drop invalid
   nft add rule inet filter input ct state invalid drop
   
   # States: new, established, related, invalid, untracked

Conntrack Helpers
-----------------

.. code-block:: bash

   # Define table for helpers
   table inet filter {
     ct helper ftp {
       type "ftp" protocol tcp
     }
     
     chain input {
       tcp dport 21 ct helper set "ftp"
     }
   }

Sets and Maps
=============

Anonymous Sets
--------------

.. code-block:: bash

   # Anonymous set (defined inline)
   nft add rule inet filter input ip saddr { 192.168.1.1, 192.168.1.2 } accept
   nft add rule inet filter input tcp dport { 22, 80, 443 } accept

Named Sets
----------

.. code-block:: bash

   # Create named set
   nft add set inet filter allowed_ips { type ipv4_addr \; }
   
   # Add elements
   nft add element inet filter allowed_ips { 192.168.1.1, 192.168.1.2 }
   
   # Use in rule
   nft add rule inet filter input ip saddr @allowed_ips accept
   
   # Dynamic sets (timeout)
   nft add set inet filter blacklist { type ipv4_addr \; flags timeout \; }
   nft add element inet filter blacklist { 10.0.0.1 timeout 1h }
   
   # List set
   nft list set inet filter allowed_ips
   
   # Delete element
   nft delete element inet filter allowed_ips { 192.168.1.1 }

Maps
----

.. code-block:: bash

   # Create map (key -> value)
   nft add map inet nat portforward { type inet_service : ipv4_addr \; }
   
   # Add elements
   nft add element inet nat portforward { 80 : 192.168.1.10, 443 : 192.168.1.11 }
   
   # Use in rule (DNAT example)
   nft add rule inet nat prerouting dnat to tcp dport map @portforward
   
   # Verdict maps
   nft add map inet filter ports_verdict { type inet_service : verdict \; }
   nft add element inet filter ports_verdict { 22 : accept, 23 : drop }
   nft add rule inet filter input tcp dport vmap @ports_verdict

NAT Configuration
=================

SNAT (Source NAT)
-----------------

.. code-block:: bash

   # Complete NAT table
   table inet nat {
     chain postrouting {
       type nat hook postrouting priority 100; policy accept;
       
       # SNAT to fixed IP
       oif eth0 ip saddr 192.168.1.0/24 snat to 203.0.113.10
       
       # Masquerade (dynamic IP)
       oif eth0 masquerade
       
       # SNAT with port range
       oif eth0 snat to 203.0.113.10:1024-65535
       
       # Persistent NAT
       oif eth0 snat to 203.0.113.10 persistent
     }
   }

DNAT (Destination NAT)
----------------------

.. code-block:: bash

   table inet nat {
     chain prerouting {
       type nat hook prerouting priority -100; policy accept;
       
       # Port forwarding
       iif eth0 tcp dport 80 dnat to 192.168.1.10:8080
       
       # Forward to multiple IPs (load balancing)
       iif eth0 tcp dport 80 dnat to numgen inc mod 3 map { \
         0 : 192.168.1.10, \
         1 : 192.168.1.11, \
         2 : 192.168.1.12 }
     }
   }

Redirect
--------

.. code-block:: bash

   # Redirect to local port
   nft add rule inet nat prerouting tcp dport 80 redirect to :8080
   
   # Redirect with port range
   nft add rule inet nat prerouting tcp dport 80 redirect to :8080-8090

Rate Limiting
=============

Limit Module
------------

.. code-block:: bash

   # Basic rate limit
   nft add rule inet filter input tcp dport 22 limit rate 10/minute accept
   
   # Burst limit
   nft add rule inet filter input tcp dport 80 limit rate 100/second burst 200 packets accept
   
   # Per source IP (using meters)
   nft add rule inet filter input tcp dport 80 meter mymeter { ip saddr limit rate 10/second } accept
   
   # Quota
   nft add rule inet filter input quota 10 mbytes accept

Logging
=======

.. code-block:: bash

   # Basic logging
   nft add rule inet filter input tcp dport 23 log prefix \"Telnet attempt: \" drop
   
   # Log with level
   nft add rule inet filter input log level warn prefix \"Dropped: \" drop
   
   # Log group (NFLOG to userspace)
   nft add rule inet filter input tcp dport 22 log group 1
   
   # Log flags
   nft add rule inet filter input log flags all prefix \"DEBUG: \"
   
   # Log with rate limit
   nft add rule inet filter input limit rate 5/minute log prefix \"Rate-limited: \" drop

Complete Firewall Examples
===========================

Basic Server Firewall
---------------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   
   flush ruleset
   
   table inet filter {
     chain input {
       type filter hook input priority 0; policy drop;
       
       # Allow loopback
       iif lo accept
       
       # Allow established/related
       ct state established,related accept
       
       # Drop invalid
       ct state invalid drop
       
       # Allow ICMP/ICMPv6
       ip protocol icmp accept
       ip6 nexthdr icmpv6 accept
       
       # Allow SSH from management network
       ip saddr 192.168.1.0/24 tcp dport 22 ct state new accept
       
       # Allow HTTP/HTTPS
       tcp dport { 80, 443 } ct state new accept
       
       # Log dropped packets
       limit rate 5/minute log prefix \"nft-drop: \" drop
     }
     
     chain forward {
       type filter hook forward priority 0; policy drop;
     }
     
     chain output {
       type filter hook output priority 0; policy accept;
     }
   }

Router with NAT
---------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   
   flush ruleset
   
   table inet filter {
     chain input {
       type filter hook input priority 0; policy drop;
       
       iif lo accept
       ct state established,related accept
       ct state invalid drop
       
       # Allow from LAN
       iif eth1 accept
       
       # Allow SSH from anywhere
       tcp dport 22 ct state new accept
     }
     
     chain forward {
       type filter hook forward priority 0; policy drop;
       
       # Allow LAN to WAN
       iif eth1 oif eth0 accept
       
       # Allow established back
       ct state established,related accept
     }
     
     chain output {
       type filter hook output priority 0; policy accept;
     }
   }
   
   table inet nat {
     chain postrouting {
       type nat hook postrouting priority 100; policy accept;
       
       # Masquerade WAN interface
       oif eth0 masquerade
     }
     
     chain prerouting {
       type nat hook prerouting priority -100; policy accept;
       
       # Port forwarding
       iif eth0 tcp dport 80 dnat to 192.168.1.10
       iif eth0 tcp dport 443 dnat to 192.168.1.10
     }
   }

Advanced Features
=================

Counters
--------

.. code-block:: bash

   # Named counter
   nft add counter inet filter ssh_counter
   nft add rule inet filter input tcp dport 22 counter name ssh_counter accept
   
   # Anonymous counter
   nft add rule inet filter input tcp dport 80 counter accept
   
   # View counters
   nft list counter inet filter ssh_counter

Reject with Custom Message
---------------------------

.. code-block:: bash

   # TCP reset
   nft add rule inet filter input tcp dport 23 reject with tcp reset
   
   # ICMP unreachable
   nft add rule inet filter input reject with icmp type host-prohibited
   nft add rule inet filter input reject with icmpv6 type admin-prohibited

Flowtable Offload
-----------------

.. code-block:: bash

   # Hardware offload for established connections
   table inet filter {
     flowtable f {
       hook ingress priority 0
       devices = { eth0, eth1 }
     }
     
     chain forward {
       type filter hook forward priority 0; policy accept;
       ip protocol { tcp, udp } flow offload @f
       ct state established,related accept
     }
   }

Persistence
===========

Save and Load
-------------

.. code-block:: bash

   # Save current ruleset
   sudo nft list ruleset > /etc/nftables.conf
   
   # Load ruleset
   sudo nft -f /etc/nftables.conf
   
   # Test without applying
   sudo nft -c -f /etc/nftables.conf
   
   # Flush and load
   sudo nft flush ruleset
   sudo nft -f /etc/nftables.conf

Systemd Service
---------------

.. code-block:: bash

   # Enable nftables service
   sudo systemctl enable nftables
   sudo systemctl start nftables
   
   # Edit rules
   sudo nano /etc/nftables.conf
   
   # Reload rules
   sudo systemctl reload nftables
   
   # View status
   sudo systemctl status nftables

Migration from iptables
=======================

Translation Tool
----------------

.. code-block:: bash

   # Translate single rule
   iptables-translate -A INPUT -p tcp --dport 22 -j ACCEPT
   # Output: nft add rule ip filter INPUT tcp dport 22 counter accept
   
   # Translate entire ruleset
   iptables-save > iptables-rules.txt
   iptables-restore-translate -f iptables-rules.txt > nftables-rules.nft
   
   # Review and apply
   sudo nft -c -f nftables-rules.nft  # Test
   sudo nft -f nftables-rules.nft     # Apply

Common Translations
-------------------

.. code-block:: bash

   # iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   nft add rule inet filter input tcp dport 80 accept
   
   # iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   nft add rule inet filter input ct state established,related accept
   
   # iptables -A INPUT -m limit --limit 5/min -j LOG
   nft add rule inet filter input limit rate 5/minute log
   
   # iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   nft add rule inet nat postrouting oif eth0 masquerade

Best Practices
==============

1. **Use inet family** for dual-stack (IPv4/IPv6) rules
2. **Atomic updates** - load entire ruleset at once
3. **Named sets** for dynamic IP lists
4. **Counters** for monitoring
5. **Log with rate limits** to prevent log flooding
6. **Test configurations** with -c flag
7. **Version control** your ruleset files
8. **Document complex rules** with comments
9. **Use includes** for modular configuration
10. **Regular backups** of working configurations

Troubleshooting
===============

.. code-block:: bash

   # View with handles
   nft -a list ruleset
   
   # Verbose output
   nft -e list ruleset
   
   # Check syntax
   nft -c -f /etc/nftables.conf
   
   # Debug mode
   nft -d list ruleset
   
   # Monitor events
   nft monitor
   
   # Trace packets
   nft add rule inet filter input meta nftrace set 1
   nft monitor trace
   
   # Temporarily disable
   nft flush ruleset
   
   # Restore from backup
   nft flush ruleset
   nft -f /etc/nftables.conf.backup

Quick Reference
===============

.. code-block:: bash

   # Tables
   nft add table inet filter
   nft list tables
   nft delete table inet filter
   
   # Chains
   nft add chain inet filter input { type filter hook input priority 0 \; }
   nft list chains
   nft delete chain inet filter input
   
   # Rules
   nft add rule inet filter input tcp dport 22 accept
   nft insert rule inet filter input tcp dport 22 accept
   nft -a list chain inet filter input
   nft delete rule inet filter input handle 10
   
   # Sets
   nft add set inet filter myset { type ipv4_addr \; }
   nft add element inet filter myset { 192.168.1.1 }
   
   # Save/Load
   nft list ruleset > file.nft
   nft -f file.nft

See Also
========

- Linux_Firewall_iptables.rst
- Linux_Network_Configuration.rst
- Linux_Security_Hardening.rst

References
==========

- man nft
- https://wiki.nftables.org/
- https://netfilter.org/projects/nftables/
