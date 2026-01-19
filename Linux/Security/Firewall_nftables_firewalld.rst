================================================================================
FIREWALL - nftables & firewalld
================================================================================

**Modern Linux Firewall Configuration with nftables and firewalld**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 4

================================================================================
TL;DR - Essential Commands
================================================================================

**nftables:**

.. code-block:: bash

   # View rules
   sudo nft list ruleset                     # All rules
   sudo nft list table inet filter           # Specific table
   
   # Add rules
   sudo nft add rule inet filter input tcp dport 22 accept
   sudo nft add rule inet filter input tcp dport 80 accept
   
   # Flush rules
   sudo nft flush ruleset                    # All rules
   sudo nft flush table inet filter          # Specific table
   
   # Save/restore
   sudo nft list ruleset > /etc/nftables.conf
   sudo nft -f /etc/nftables.conf

**firewalld:**

.. code-block:: bash

   # Check status
   sudo firewall-cmd --state
   sudo firewall-cmd --list-all
   
   # Add service
   sudo firewall-cmd --add-service=http --permanent
   sudo firewall-cmd --add-service=https --permanent
   sudo firewall-cmd --reload
   
   # Add port
   sudo firewall-cmd --add-port=8080/tcp --permanent
   sudo firewall-cmd --reload
   
   # List zones
   sudo firewall-cmd --get-zones
   sudo firewall-cmd --get-active-zones

================================================================================
PART 1: nftables
================================================================================

1. nftables Fundamentals
=========================

1.1 What is nftables?
---------------------

**nftables** is the modern replacement for iptables, providing:

- Single framework for IPv4, IPv6, ARP, and bridge filtering
- Better performance
- Simplified syntax
- Atomic rule updates
- Better scripting support

**Key Differences from iptables:**

.. code-block:: text

   iptables                  nftables
   ----------------          ----------------
   Multiple tools            Single nft tool
   (iptables, ip6tables,     
   arptables, ebtables)      
   
   Separate tables           Combined tables (inet family)
   for IPv4/IPv6             
   
   Complex syntax            Cleaner syntax
   
   No atomic updates         Atomic updates

1.2 nftables Architecture
--------------------------

**Address Families:**

.. code-block:: text

   ip      - IPv4 packets
   ip6     - IPv6 packets
   inet    - IPv4 and IPv6 (most common)
   arp     - ARP packets
   bridge  - Ethernet bridge packets
   netdev  - Packets from network devices

**Tables:**

.. code-block:: bash

   # Tables contain chains (user-defined structure)
   sudo nft add table inet filter
   sudo nft add table inet nat

**Chains:**

.. code-block:: bash

   # Chains contain rules
   # Base chains: attached to netfilter hooks
   # Regular chains: called from other chains

**Hooks (similar to iptables chains):**

.. code-block:: text

   prerouting   - Before routing decision
   input        - Packets destined for local system
   forward      - Packets being routed through
   output       - Packets from local system
   postrouting  - After routing decision

================================================================================
2. Basic nftables Configuration
================================================================================

2.1 Installation
----------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install nftables
   
   # RHEL/CentOS 8+
   sudo dnf install nftables
   
   # Enable and start
   sudo systemctl enable nftables
   sudo systemctl start nftables
   
   # Check version
   nft --version

2.2 Create Basic Firewall
--------------------------

**Create Table and Chains:**

.. code-block:: bash

   # Create inet table (handles both IPv4 and IPv6)
   sudo nft add table inet filter
   
   # Create input chain (hook: input, priority: 0, policy: drop)
   sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
   
   # Create forward chain
   sudo nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; }
   
   # Create output chain
   sudo nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; }

**Add Rules:**

.. code-block:: bash

   # Allow loopback
   sudo nft add rule inet filter input iif lo accept
   
   # Allow established/related
   sudo nft add rule inet filter input ct state established,related accept
   
   # Allow SSH
   sudo nft add rule inet filter input tcp dport 22 accept
   
   # Allow HTTP/HTTPS
   sudo nft add rule inet filter input tcp dport { 80, 443 } accept
   
   # Allow ping
   sudo nft add rule inet filter input icmp type echo-request accept

2.3 View Rules
--------------

.. code-block:: bash

   # List all rules
   sudo nft list ruleset
   
   # List specific table
   sudo nft list table inet filter
   
   # List specific chain
   sudo nft list chain inet filter input
   
   # List with handles (for deletion)
   sudo nft -a list table inet filter

2.4 Delete Rules
----------------

.. code-block:: bash

   # Delete specific rule by handle
   sudo nft delete rule inet filter input handle 5
   
   # Delete chain
   sudo nft delete chain inet filter input
   
   # Delete table
   sudo nft delete table inet filter
   
   # Flush (delete all rules in chain)
   sudo nft flush chain inet filter input
   
   # Flush entire table
   sudo nft flush table inet filter
   
   # Flush everything
   sudo nft flush ruleset

================================================================================
3. Advanced nftables Rules
================================================================================

3.1 Sets and Maps
-----------------

**Create IP Set:**

.. code-block:: bash

   # Define set in table
   sudo nft add set inet filter blacklist { type ipv4_addr \; }
   
   # Add IPs to set
   sudo nft add element inet filter blacklist { 1.2.3.4, 5.6.7.8 }
   
   # Use set in rule
   sudo nft add rule inet filter input ip saddr @blacklist drop
   
   # Named sets in rules
   sudo nft add rule inet filter input ip saddr { 10.0.0.0/8, 192.168.0.0/16 } drop

**Create Port Set:**

.. code-block:: bash

   # Create set for web ports
   sudo nft add set inet filter webports { type inet_service \; }
   sudo nft add element inet filter webports { 80, 443, 8080 }
   
   # Use in rule
   sudo nft add rule inet filter input tcp dport @webports accept

**Maps (for DNAT/SNAT):**

.. code-block:: bash

   # Create map for port forwarding
   sudo nft add map inet nat portmap { type inet_service : ipv4_addr \; }
   sudo nft add element inet nat portmap { 80 : 192.168.1.10, 443 : 192.168.1.11 }
   
   # Use map for DNAT
   sudo nft add rule inet nat prerouting dnat to tcp dport map @portmap

3.2 Rate Limiting
-----------------

.. code-block:: bash

   # Limit SSH connections
   sudo nft add rule inet filter input tcp dport 22 limit rate 3/minute accept
   
   # Limit with burst
   sudo nft add rule inet filter input tcp dport 80 limit rate 100/second burst 200 packets accept
   
   # Per-source rate limiting
   sudo nft add rule inet filter input ip saddr . tcp dport { 22 } ct count over 3 drop

3.3 Connection Tracking
------------------------

.. code-block:: bash

   # Allow established/related
   sudo nft add rule inet filter input ct state established,related accept
   
   # Drop invalid packets
   sudo nft add rule inet filter input ct state invalid drop
   
   # Allow new connections to specific ports
   sudo nft add rule inet filter input tcp dport 22 ct state new accept
   
   # Connection limit per IP
   sudo nft add rule inet filter input ip protocol tcp ct count over 100 drop

================================================================================
4. Complete nftables Examples
================================================================================

4.1 Basic Workstation Firewall
-------------------------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   # /etc/nftables.conf
   
   # Flush existing rules
   flush ruleset
   
   # Create table
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
           tcp dport 22 accept
           
           # Log dropped
           log prefix "nft-dropped: "
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

4.2 Web Server Firewall
------------------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   
   flush ruleset
   
   table inet filter {
       # Define sets
       set admin_ips {
           type ipv4_addr
           elements = { 192.168.1.100, 192.168.1.101 }
       }
       
       chain input {
           type filter hook input priority 0; policy drop;
           
           iif lo accept
           ct state established,related accept
           ct state invalid drop
           
           # SSH only from admin IPs
           ip saddr @admin_ips tcp dport 22 accept
           
           # HTTP/HTTPS from anywhere with rate limit
           tcp dport 80 limit rate 100/second burst 200 packets accept
           tcp dport 443 limit rate 100/second burst 200 packets accept
           
           # Allow ping with limit
           icmp type echo-request limit rate 1/second accept
           
           # Log and drop
           log prefix "nft-dropped: " limit rate 5/minute
           drop
       }
       
       chain forward {
           type filter hook forward priority 0; policy drop;
       }
       
       chain output {
           type filter hook output priority 0; policy accept;
       }
   }

4.3 NAT Gateway
---------------

.. code-block:: bash

   #!/usr/sbin/nft -f
   
   flush ruleset
   
   table inet filter {
       chain input {
           type filter hook input priority 0; policy drop;
           iif lo accept
           ct state established,related accept
           
           # SSH from LAN only
           iifname "eth1" tcp dport 22 accept
       }
       
       chain forward {
           type filter hook forward priority 0; policy drop;
           ct state established,related accept
           
           # Allow LAN to WAN
           iifname "eth1" oifname "eth0" accept
       }
       
       chain output {
           type filter hook output priority 0; policy accept;
       }
   }
   
   table inet nat {
       chain prerouting {
           type nat hook prerouting priority -100;
           
           # Port forwarding - external 80 to internal 192.168.1.100:80
           iifname "eth0" tcp dport 80 dnat to 192.168.1.100:80
       }
       
       chain postrouting {
           type nat hook postrouting priority 100;
           
           # Masquerade outgoing traffic
           oifname "eth0" masquerade
       }
   }

================================================================================
5. nftables Management
================================================================================

5.1 Save and Restore
--------------------

.. code-block:: bash

   # Save current ruleset
   sudo nft list ruleset > /etc/nftables.conf
   
   # Load ruleset from file
   sudo nft -f /etc/nftables.conf
   
   # Load and check syntax
   sudo nft -c -f /etc/nftables.conf

5.2 Atomic Updates
-------------------

.. code-block:: bash

   # Create new configuration file
   sudo nano /tmp/new-rules.nft
   
   # Test configuration
   sudo nft -c -f /tmp/new-rules.nft
   
   # If OK, apply atomically
   sudo nft -f /tmp/new-rules.nft
   
   # Save if working
   sudo nft list ruleset > /etc/nftables.conf

5.3 Backup and Restore
----------------------

.. code-block:: bash

   # Backup current rules
   sudo nft list ruleset > ~/nftables-backup-$(date +%Y%m%d).conf
   
   # Restore from backup
   sudo nft -f ~/nftables-backup-20260119.conf

================================================================================
PART 2: firewalld
================================================================================

6. firewalld Fundamentals
==========================

6.1 What is firewalld?
----------------------

**firewalld** is a dynamic firewall manager that uses:

- Zones to manage trust levels
- Services and ports
- Rich rules for complex configurations
- Runtime and permanent configurations
- D-Bus interface for dynamic updates
- Backend: nftables (default) or iptables

**Key Concepts:**

.. code-block:: text

   Zones       - Different trust levels for connections
   Services    - Predefined port/protocol combinations
   Ports       - Individual port openings
   Rich Rules  - Complex firewall rules
   Direct Rules - Direct iptables/nftables commands

6.2 Installation and Setup
---------------------------

.. code-block:: bash

   # Install firewalld
   sudo apt install firewalld          # Debian/Ubuntu
   sudo dnf install firewalld          # RHEL/CentOS/Fedora
   
   # Start and enable
   sudo systemctl start firewalld
   sudo systemctl enable firewalld
   
   # Check status
   sudo firewall-cmd --state
   sudo systemctl status firewalld
   
   # Check backend (nftables or iptables)
   sudo firewall-cmd --get-default-backend

================================================================================
7. firewalld Zones
================================================================================

7.1 Understanding Zones
------------------------

**Predefined Zones (least to most trusted):**

.. code-block:: text

   drop       - Drop all incoming, allow outgoing
   block      - Reject incoming with icmp-host-prohibited
   public     - Public networks (default)
   external   - External networks with masquerading
   dmz        - DMZ - limited access to internal
   work       - Work environment
   home       - Home environment
   internal   - Internal networks
   trusted    - All traffic accepted

7.2 Zone Management
-------------------

**View Zones:**

.. code-block:: bash

   # List all zones
   sudo firewall-cmd --get-zones
   
   # Get default zone
   sudo firewall-cmd --get-default-zone
   
   # Get active zones
   sudo firewall-cmd --get-active-zones
   
   # List everything in zone
   sudo firewall-cmd --zone=public --list-all
   
   # List all zones with details
   sudo firewall-cmd --list-all-zones

**Set Default Zone:**

.. code-block:: bash

   # Change default zone
   sudo firewall-cmd --set-default-zone=home
   
   # Assign interface to zone
   sudo firewall-cmd --zone=public --add-interface=eth0 --permanent
   sudo firewall-cmd --reload
   
   # Change interface zone
   sudo firewall-cmd --zone=dmz --change-interface=eth1 --permanent
   sudo firewall-cmd --reload

7.3 Create Custom Zone
-----------------------

.. code-block:: bash

   # Create new zone
   sudo firewall-cmd --permanent --new-zone=webservers
   
   # Set target (default action)
   sudo firewall-cmd --permanent --zone=webservers --set-target=DROP
   
   # Add interface
   sudo firewall-cmd --permanent --zone=webservers --add-interface=eth0
   
   # Reload
   sudo firewall-cmd --reload

================================================================================
8. Services and Ports
================================================================================

8.1 Managing Services
---------------------

**List Services:**

.. code-block:: bash

   # List available services
   sudo firewall-cmd --get-services
   
   # List services in zone
   sudo firewall-cmd --zone=public --list-services
   
   # Get service details
   sudo firewall-cmd --info-service=ssh
   sudo firewall-cmd --info-service=http

**Add/Remove Services:**

.. code-block:: bash

   # Add service (runtime only)
   sudo firewall-cmd --add-service=http
   
   # Add service permanently
   sudo firewall-cmd --add-service=http --permanent
   sudo firewall-cmd --reload
   
   # Add multiple services
   sudo firewall-cmd --add-service={http,https,ssh} --permanent
   sudo firewall-cmd --reload
   
   # Remove service
   sudo firewall-cmd --remove-service=http --permanent
   sudo firewall-cmd --reload
   
   # Add to specific zone
   sudo firewall-cmd --zone=dmz --add-service=http --permanent

8.2 Managing Ports
------------------

.. code-block:: bash

   # List ports
   sudo firewall-cmd --list-ports
   
   # Add port
   sudo firewall-cmd --add-port=8080/tcp --permanent
   sudo firewall-cmd --reload
   
   # Add port range
   sudo firewall-cmd --add-port=3000-3100/tcp --permanent
   
   # Add UDP port
   sudo firewall-cmd --add-port=53/udp --permanent
   
   # Remove port
   sudo firewall-cmd --remove-port=8080/tcp --permanent
   sudo firewall-cmd --reload
   
   # Add to specific zone
   sudo firewall-cmd --zone=public --add-port=9000/tcp --permanent

8.3 Create Custom Service
--------------------------

.. code-block:: bash

   # Create service definition
   sudo firewall-cmd --permanent --new-service=myapp
   
   # Add port to service
   sudo firewall-cmd --permanent --service=myapp --add-port=8080/tcp
   sudo firewall-cmd --permanent --service=myapp --add-port=8081/tcp
   
   # Set description
   sudo firewall-cmd --permanent --service=myapp --set-short="My Application"
   sudo firewall-cmd --permanent --service=myapp --set-description="Custom application service"
   
   # Reload and use
   sudo firewall-cmd --reload
   sudo firewall-cmd --add-service=myapp --permanent
   
   # Service files location: /etc/firewalld/services/

================================================================================
9. Rich Rules
================================================================================

9.1 Rich Rule Syntax
---------------------

**Basic Format:**

.. code-block:: bash

   rule [family="ipv4|ipv6"]
        [source [address="address[/mask]"] [invert="bool"]]
        [destination [address="address[/mask]"] [invert="bool"]]
        [service name="service"] | [port port="port" protocol="tcp|udp"]
        [log [prefix="prefix"] [level="level"]]
        [audit]
        [accept|reject|drop]

9.2 Rich Rule Examples
-----------------------

**Allow from Specific IP:**

.. code-block:: bash

   # Allow SSH from specific IP
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.100" service name="ssh" accept' --permanent
   
   # Allow HTTP from subnet
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="http" accept' --permanent

**Block Specific IP:**

.. code-block:: bash

   # Block IP
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="1.2.3.4" drop' --permanent
   
   # Block subnet
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" drop' --permanent

**Port Forwarding:**

.. code-block:: bash

   # Forward port 80 to 8080
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" forward-port port="80" protocol="tcp" to-port="8080"' --permanent
   
   # Forward to different host
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" forward-port port="80" protocol="tcp" to-port="80" to-addr="192.168.1.100"' --permanent

**Logging:**

.. code-block:: bash

   # Log dropped packets
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="0.0.0.0/0" log prefix="DROPPED: " level="info" drop' --permanent
   
   # Log accepted SSH connections
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" service name="ssh" log prefix="SSH: " level="info" accept' --permanent

**Rate Limiting:**

.. code-block:: bash

   # Limit SSH connections
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" service name="ssh" limit value="3/m" accept' --permanent
   
   # Limit HTTP
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" service name="http" limit value="100/s" accept' --permanent

9.3 Manage Rich Rules
----------------------

.. code-block:: bash

   # List rich rules
   sudo firewall-cmd --list-rich-rules
   
   # Remove rich rule
   sudo firewall-cmd --remove-rich-rule='rule family="ipv4" source address="1.2.3.4" drop' --permanent
   
   # List rich rules in specific zone
   sudo firewall-cmd --zone=public --list-rich-rules

================================================================================
10. Masquerading and Port Forwarding
================================================================================

10.1 Enable Masquerading
-------------------------

.. code-block:: bash

   # Enable masquerading (NAT)
   sudo firewall-cmd --add-masquerade --permanent
   sudo firewall-cmd --reload
   
   # Enable in specific zone
   sudo firewall-cmd --zone=external --add-masquerade --permanent
   
   # Check status
   sudo firewall-cmd --query-masquerade
   
   # Disable masquerading
   sudo firewall-cmd --remove-masquerade --permanent

10.2 Port Forwarding
--------------------

.. code-block:: bash

   # Forward external 8080 to local 80
   sudo firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80 --permanent
   
   # Forward to different host
   sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toport=80:toaddr=192.168.1.100 --permanent
   
   # Multiple forwards using rich rules
   sudo firewall-cmd --add-rich-rule='rule family="ipv4" forward-port port="443" protocol="tcp" to-port="443" to-addr="192.168.1.100"' --permanent
   
   # List forwards
   sudo firewall-cmd --list-forward-ports
   
   # Remove forward
   sudo firewall-cmd --remove-forward-port=port=8080:proto=tcp:toport=80 --permanent

================================================================================
11. Direct Rules
================================================================================

11.1 Using Direct Rules
------------------------

.. code-block:: bash

   # Add direct iptables rule
   sudo firewall-cmd --direct --add-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT
   
   # List direct rules
   sudo firewall-cmd --direct --get-all-rules
   
   # Remove direct rule
   sudo firewall-cmd --direct --remove-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT
   
   # Make permanent
   sudo firewall-cmd --runtime-to-permanent

================================================================================
12. firewalld Management
================================================================================

12.1 Runtime vs Permanent
--------------------------

.. code-block:: bash

   # Runtime changes (lost on reload/reboot)
   sudo firewall-cmd --add-service=http
   
   # Permanent changes (survive reload/reboot)
   sudo firewall-cmd --add-service=http --permanent
   
   # Apply permanent changes
   sudo firewall-cmd --reload
   
   # Make current runtime permanent
   sudo firewall-cmd --runtime-to-permanent

12.2 Reload and Restart
------------------------

.. code-block:: bash

   # Reload firewalld (applies permanent rules)
   sudo firewall-cmd --reload
   
   # Complete restart (breaks active connections)
   sudo firewall-cmd --complete-reload
   
   # Restart service
   sudo systemctl restart firewalld

12.3 Panic Mode
---------------

.. code-block:: bash

   # Enable panic mode (drop all traffic)
   sudo firewall-cmd --panic-on
   
   # Disable panic mode
   sudo firewall-cmd --panic-off
   
   # Query panic mode
   sudo firewall-cmd --query-panic

12.4 Logging
------------

.. code-block:: bash

   # Enable logging for denied packets
   sudo firewall-cmd --set-log-denied=all
   
   # Options: all, unicast, broadcast, multicast, off
   sudo firewall-cmd --set-log-denied=unicast
   
   # Query logging
   sudo firewall-cmd --get-log-denied
   
   # View logs
   sudo journalctl -u firewalld
   sudo tail -f /var/log/messages | grep kernel

================================================================================
13. Complete firewalld Examples
================================================================================

13.1 Basic Web Server
---------------------

.. code-block:: bash

   # Set default zone
   sudo firewall-cmd --set-default-zone=public
   
   # Allow SSH, HTTP, HTTPS
   sudo firewall-cmd --permanent --add-service=ssh
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   
   # Limit SSH to admin network
   sudo firewall-cmd --remove-service=ssh --permanent
   sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept'
   
   # Rate limit HTTP
   sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" service name="http" limit value="100/s" accept'
   
   # Reload
   sudo firewall-cmd --reload

13.2 Database Server
--------------------

.. code-block:: bash

   # Set restrictive default
   sudo firewall-cmd --set-default-zone=drop
   
   # Create database zone
   sudo firewall-cmd --permanent --new-zone=database
   sudo firewall-cmd --permanent --zone=database --set-target=DROP
   
   # Allow SSH from admin network
   sudo firewall-cmd --permanent --zone=database --add-rich-rule='rule family="ipv4" source address="192.168.100.0/24" service name="ssh" accept'
   
   # Allow MySQL from app servers
   sudo firewall-cmd --permanent --zone=database --add-rich-rule='rule family="ipv4" source address="192.168.1.10" port port="3306" protocol="tcp" accept'
   sudo firewall-cmd --permanent --zone=database --add-rich-rule='rule family="ipv4" source address="192.168.1.11" port port="3306" protocol="tcp" accept'
   
   # Assign interface
   sudo firewall-cmd --permanent --zone=database --add-interface=eth0
   
   # Reload
   sudo firewall-cmd --reload

13.3 Gateway/Router
-------------------

.. code-block:: bash

   # External interface - public zone
   sudo firewall-cmd --permanent --zone=public --add-interface=eth0
   
   # Internal interface - internal zone
   sudo firewall-cmd --permanent --zone=internal --add-interface=eth1
   
   # Enable masquerading on external
   sudo firewall-cmd --permanent --zone=public --add-masquerade
   
   # Allow SSH from internal only
   sudo firewall-cmd --permanent --zone=internal --add-service=ssh
   
   # Port forward web server
   sudo firewall-cmd --permanent --zone=public --add-forward-port=port=80:proto=tcp:toport=80:toaddr=192.168.1.100
   sudo firewall-cmd --permanent --zone=public --add-forward-port=port=443:proto=tcp:toport=443:toaddr=192.168.1.100
   
   # Reload
   sudo firewall-cmd --reload

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- Firewall_iptables.rst - Legacy iptables configuration
- Linux_Security_Basics.rst - Network security fundamentals
- Kernel_Hardening.rst - Kernel network stack hardening
- SSH_Hardening.rst - SSH firewall configuration

================================================================================
END OF FIREWALL nftables & firewalld
================================================================================
