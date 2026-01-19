===================================
Linux iptables Firewall Guide
===================================

:Author: Linux Security Documentation
:Date: January 2026
:Version: 1.0
:Focus: iptables - Linux firewall and packet filtering

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Essential iptables Commands
----------------------------

.. code-block:: bash

   # View current rules
   sudo iptables -L -n -v
   sudo iptables -L INPUT -n -v --line-numbers
   
   # Save rules
   sudo iptables-save > /etc/iptables/rules.v4
   sudo ip6tables-save > /etc/iptables/rules.v6
   
   # Restore rules
   sudo iptables-restore < /etc/iptables/rules.v4
   
   # Flush all rules (DANGER!)
   sudo iptables -F
   sudo iptables -X
   sudo iptables -Z
   
   # Set default policies
   sudo iptables -P INPUT DROP
   sudo iptables -P FORWARD DROP
   sudo iptables -P OUTPUT ACCEPT
   
   # Allow SSH
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Allow established connections
   sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # Allow loopback
   sudo iptables -A INPUT -i lo -j ACCEPT
   
   # Drop invalid packets
   sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

Quick Firewall Setup
---------------------

.. code-block:: bash

   #!/bin/bash
   # Basic secure firewall
   
   # Flush existing rules
   iptables -F
   iptables -X
   iptables -Z
   
   # Default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Allow loopback
   iptables -A INPUT -i lo -j ACCEPT
   
   # Allow established/related
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # Drop invalid
   iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
   
   # Allow SSH
   iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
   
   # Allow HTTP/HTTPS
   iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
   iptables -A INPUT -p tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
   
   # Allow ping
   iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
   
   # Log dropped packets
   iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-INPUT: " --log-level 7
   
   # Save
   iptables-save > /etc/iptables/rules.v4

iptables Basics
===============

Tables and Chains
-----------------

.. code-block:: text

   Tables:
   - filter: Default table for packet filtering
   - nat: Network Address Translation
   - mangle: Packet alteration
   - raw: Connection tracking exemption
   - security: Mandatory Access Control rules
   
   Built-in Chains (filter table):
   - INPUT: Packets destined for local system
   - OUTPUT: Packets originating from local system
   - FORWARD: Packets routed through system
   
   Built-in Chains (nat table):
   - PREROUTING: Alter packets before routing
   - POSTROUTING: Alter packets after routing
   - OUTPUT: NAT for locally generated packets

.. code-block:: bash

   # Specify table
   iptables -t nat -L -n -v
   iptables -t mangle -L -n -v
   
   # Default is filter table
   iptables -L -n -v  # Same as -t filter

Rule Structure
--------------

.. code-block:: bash

   # Basic syntax
   iptables [-t table] -A chain match-criteria -j target
   
   # Examples:
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   iptables -A INPUT -s 192.168.1.100 -j DROP
   iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
   
   # Match criteria:
   # -p protocol (tcp, udp, icmp, all)
   # -s source IP/network
   # -d destination IP/network
   # -i input interface
   # -o output interface
   # --sport source port
   # --dport destination port
   
   # Targets:
   # ACCEPT: Allow packet
   # DROP: Silently discard
   # REJECT: Discard and send error
   # LOG: Log packet
   # RETURN: Stop processing in current chain

Managing Rules
==============

Viewing Rules
-------------

.. code-block:: bash

   # List all rules
   sudo iptables -L
   
   # Numeric output (faster, no DNS)
   sudo iptables -L -n
   
   # Verbose with packet/byte counters
   sudo iptables -L -n -v
   
   # Show line numbers
   sudo iptables -L -n --line-numbers
   
   # Specific chain
   sudo iptables -L INPUT -n -v
   
   # Specific table
   sudo iptables -t nat -L -n -v
   
   # Show rules as commands
   sudo iptables-save

Adding Rules
------------

.. code-block:: bash

   # Append rule (add to end)
   sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   
   # Insert rule at position
   sudo iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT
   
   # Replace rule
   sudo iptables -R INPUT 5 -p tcp --dport 8080 -j ACCEPT
   
   # Insert before specific rule
   sudo iptables -I INPUT 3 -s 192.168.1.0/24 -j ACCEPT

Deleting Rules
--------------

.. code-block:: bash

   # Delete by specification
   sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT
   
   # Delete by line number
   sudo iptables -L INPUT -n --line-numbers
   sudo iptables -D INPUT 5
   
   # Flush chain (delete all rules)
   sudo iptables -F INPUT
   
   # Flush all chains
   sudo iptables -F
   
   # Delete custom chain
   sudo iptables -X CUSTOM_CHAIN

Match Criteria
==============

Protocol Matching
-----------------

.. code-block:: bash

   # TCP
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   iptables -A INPUT -p tcp --sport 1024:65535 -j ACCEPT
   iptables -A INPUT -p tcp --tcp-flags SYN,ACK SYN -j ACCEPT
   
   # UDP
   iptables -A INPUT -p udp --dport 53 -j ACCEPT
   
   # ICMP
   iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
   iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
   
   # All protocols
   iptables -A INPUT -p all -j ACCEPT

Address Matching
----------------

.. code-block:: bash

   # Source IP
   iptables -A INPUT -s 192.168.1.100 -j ACCEPT
   
   # Source network
   iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
   
   # Destination IP
   iptables -A OUTPUT -d 10.0.0.1 -j ACCEPT
   
   # Multiple IPs with iprange
   iptables -A INPUT -m iprange --src-range 192.168.1.100-192.168.1.200 -j ACCEPT
   
   # Negate (NOT)
   iptables -A INPUT ! -s 192.168.1.0/24 -j DROP

Interface Matching
------------------

.. code-block:: bash

   # Input interface
   iptables -A INPUT -i eth0 -j ACCEPT
   
   # Output interface
   iptables -A OUTPUT -o eth1 -j ACCEPT
   
   # Wildcard
   iptables -A INPUT -i eth+ -j ACCEPT  # All ethX interfaces

Port Matching
-------------

.. code-block:: bash

   # Single port
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   
   # Port range
   iptables -A INPUT -p tcp --dport 1024:65535 -j ACCEPT
   
   # Multiple ports with multiport
   iptables -A INPUT -p tcp -m multiport --dports 80,443,8080 -j ACCEPT
   iptables -A INPUT -p tcp -m multiport --sports 80,443 -j ACCEPT
   
   # Source and destination ports
   iptables -A INPUT -p tcp --sport 1024:65535 --dport 80 -j ACCEPT

Extended Matches
================

Connection Tracking
-------------------

.. code-block:: bash

   # Connection state
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   iptables -A INPUT -m conntrack --ctstate NEW -j ACCEPT
   iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
   
   # States:
   # NEW: New connection
   # ESTABLISHED: Part of existing connection
   # RELATED: Related to existing connection (FTP data)
   # INVALID: Invalid packet
   # UNTRACKED: Not tracked
   
   # Limit NEW connections
   iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW -m limit --limit 60/minute -j ACCEPT

Rate Limiting
-------------

.. code-block:: bash

   # Limit connections
   iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/minute --limit-burst 5 -j ACCEPT
   
   # Limit by source
   iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 20 --connlimit-mask 32 -j REJECT
   
   # Recent module for rate limiting
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --rttl --name SSH -j DROP

Time-based Rules
----------------

.. code-block:: bash

   # Allow during business hours
   iptables -A INPUT -p tcp --dport 80 -m time --timestart 09:00 --timestop 17:00 -j ACCEPT
   
   # Weekdays only
   iptables -A INPUT -p tcp --dport 80 -m time --weekdays Mon,Tue,Wed,Thu,Fri -j ACCEPT
   
   # Specific date range
   iptables -A INPUT -m time --datestart 2026-01-01 --datestop 2026-12-31 -j ACCEPT

String Matching
---------------

.. code-block:: bash

   # Match string in packet
   iptables -A INPUT -p tcp --dport 80 -m string --string "GET" --algo bm -j ACCEPT
   
   # Block specific content
   iptables -A FORWARD -p tcp --dport 80 -m string --string "blocked.com" --algo kmp -j DROP

MAC Address
-----------

.. code-block:: bash

   # Match MAC address
   iptables -A INPUT -m mac --mac-source 00:11:22:33:44:55 -j ACCEPT
   
   # Only works on INPUT/FORWARD/PREROUTING

Targets and Actions
===================

Standard Targets
----------------

.. code-block:: bash

   # ACCEPT: Allow packet
   iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   
   # DROP: Silently discard
   iptables -A INPUT -s 192.168.1.100 -j DROP
   
   # REJECT: Discard with ICMP response
   iptables -A INPUT -p tcp --dport 23 -j REJECT
   iptables -A INPUT -p tcp --dport 23 -j REJECT --reject-with icmp-host-prohibited
   
   # RETURN: Stop processing in current chain
   iptables -A INPUT -s 192.168.1.0/24 -j RETURN

Logging
-------

.. code-block:: bash

   # Log packets
   iptables -A INPUT -j LOG --log-prefix "iptables-INPUT: " --log-level 4
   
   # Log with rate limiting
   iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-DROP: " --log-level 7
   
   # Log and then drop
   iptables -A INPUT -p tcp --dport 23 -j LOG --log-prefix "Telnet-attempt: "
   iptables -A INPUT -p tcp --dport 23 -j DROP
   
   # View logs
   sudo tail -f /var/log/kern.log | grep iptables
   sudo journalctl -k -f | grep iptables

Custom Chains
-------------

.. code-block:: bash

   # Create custom chain
   iptables -N LOGGING
   
   # Add rules to custom chain
   iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "Dropped: " --log-level 4
   iptables -A LOGGING -j DROP
   
   # Jump to custom chain
   iptables -A INPUT -j LOGGING
   
   # Delete custom chain
   iptables -F LOGGING  # Flush first
   iptables -X LOGGING  # Then delete

NAT Configuration
=================

SNAT (Source NAT)
-----------------

.. code-block:: bash

   # Enable IP forwarding
   echo 1 > /proc/sys/net/ipv4/ip_forward
   
   # SNAT (static IP)
   iptables -t nat -A POSTROUTING -o eth0 -s 192.168.1.0/24 -j SNAT --to-source 203.0.113.10
   
   # MASQUERADE (dynamic IP)
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # Multiple IPs
   iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 203.0.113.10-203.0.113.20

DNAT (Destination NAT)
----------------------

.. code-block:: bash

   # Port forwarding
   iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
   
   # Forward to multiple servers (load balancing)
   iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10-192.168.1.20
   
   # Forward specific interface
   iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10

Redirect
--------

.. code-block:: bash

   # Redirect to local port
   iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
   
   # Transparent proxy
   iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128

Common Scenarios
================

Web Server Protection
---------------------

.. code-block:: bash

   # Allow HTTP/HTTPS
   iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
   iptables -A INPUT -p tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
   
   # Rate limit connections
   iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 50 --connlimit-mask 32 -j REJECT
   
   # Protect against SYN flood
   iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
   iptables -A INPUT -p tcp --syn -j DROP
   
   # Block specific user agents (requires string match)
   iptables -A INPUT -p tcp --dport 80 -m string --string "BadBot" --algo bm -j DROP

SSH Protection
--------------

.. code-block:: bash

   # Allow SSH from specific network
   iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT
   iptables -A INPUT -p tcp --dport 22 -j DROP
   
   # Rate limit SSH attempts
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
   iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 --rttl --name SSH -j DROP
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Port knocking (simplified)
   iptables -A INPUT -p tcp --dport 1234 -m recent --name knock1 --set -j DROP
   iptables -A INPUT -p tcp --dport 2345 -m recent --name knock1 --rcheck --seconds 10 -m recent --name knock2 --set -j DROP
   iptables -A INPUT -p tcp --dport 22 -m recent --name knock2 --rcheck --seconds 10 -j ACCEPT

DDoS Mitigation
---------------

.. code-block:: bash

   # SYN flood protection
   iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j RETURN
   iptables -A INPUT -p tcp --syn -j DROP
   
   # Ping flood
   iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT
   iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
   
   # Drop invalid packets
   iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
   
   # Block fragmented packets
   iptables -A INPUT -f -j DROP
   
   # Limit connections per IP
   iptables -A INPUT -p tcp --syn -m connlimit --connlimit-above 20 -j REJECT

Persistence
===========

Saving Rules
------------

.. code-block:: bash

   # Debian/Ubuntu - using iptables-persistent
   sudo apt install iptables-persistent
   
   # Save current rules
   sudo iptables-save > /etc/iptables/rules.v4
   sudo ip6tables-save > /etc/iptables/rules.v6
   
   # Or use netfilter-persistent
   sudo netfilter-persistent save
   
   # RHEL/CentOS
   sudo service iptables save
   # Saves to /etc/sysconfig/iptables

Restoring Rules
---------------

.. code-block:: bash

   # Restore from file
   sudo iptables-restore < /etc/iptables/rules.v4
   
   # Test rules before applying
   sudo iptables-restore -t < /etc/iptables/rules.v4
   
   # Restore and flush existing
   sudo iptables-restore -n < /etc/iptables/rules.v4

Automatic Loading
-----------------

.. code-block:: bash

   # Debian/Ubuntu with iptables-persistent
   sudo systemctl enable netfilter-persistent
   
   # Systemd service
   # /etc/systemd/system/iptables-restore.service
   [Unit]
   Description=Restore iptables rules
   Before=network-pre.target
   
   [Service]
   Type=oneshot
   ExecStart=/sbin/iptables-restore /etc/iptables/rules.v4
   ExecStart=/sbin/ip6tables-restore /etc/iptables/rules.v6
   
   [Install]
   WantedBy=multi-user.target
   
   sudo systemctl enable iptables-restore

Best Practices
==============

1. **Always allow loopback** traffic first
2. **Allow established connections** early in chain
3. **Default DROP policy** for INPUT and FORWARD
4. **Test rules carefully** - lock yourself out protection
5. **Use connection tracking** for stateful filtering
6. **Log suspicious activity** with rate limiting
7. **Document complex rules** with comments
8. **Save rules** to persistent storage
9. **Test before saving** changes
10. **Regular rule audits** and cleanup

Common Pitfalls
===============

1. **Locking yourself out** - test SSH access before saving
2. **Wrong rule order** - specific rules before general
3. **Not saving rules** - lost on reboot
4. **Too much logging** - fills disk
5. **Forgetting to enable** IP forwarding for NAT
6. **Not using conntrack** - inefficient rules
7. **Complex rules** without testing

Troubleshooting
===============

.. code-block:: bash

   # Enable packet logging temporarily
   iptables -I INPUT 1 -j LOG --log-prefix "DEBUG-INPUT: "
   iptables -I OUTPUT 1 -j LOG --log-prefix "DEBUG-OUTPUT: "
   
   # Watch logs
   tail -f /var/log/kern.log | grep iptables
   
   # Check packet counters
   iptables -L -n -v
   
   # Reset counters
   iptables -Z
   
   # Temporarily flush rules (DANGER!)
   iptables -F
   iptables -P INPUT ACCEPT
   iptables -P FORWARD ACCEPT
   iptables -P OUTPUT ACCEPT
   
   # Restore from backup
   iptables-restore < /etc/iptables/rules.v4.backup

Quick Reference
===============

.. code-block:: bash

   # View
   iptables -L -n -v
   iptables-save
   
   # Add
   iptables -A chain -j target
   iptables -I chain position -j target
   
   # Delete
   iptables -D chain rulenum
   iptables -F chain
   
   # Save/Restore
   iptables-save > file
   iptables-restore < file
   
   # Policy
   iptables -P chain target

See Also
========

- Linux_Firewall_nftables.rst
- Linux_Network_Configuration.rst
- Linux_Security_Hardening.rst

References
==========

- man iptables
- man iptables-extensions
- https://netfilter.org/
- iptables Tutorial: https://www.frozentux.net/iptables-tutorial/
