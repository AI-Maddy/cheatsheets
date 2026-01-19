================================================================================
FIREWALL CONFIGURATION - iptables
================================================================================

**Complete Guide to Linux iptables Firewall Configuration**

Source: Mastering Linux Security And Hardening
Chapter Coverage: Chapter 3

================================================================================
TL;DR - Essential Commands
================================================================================

.. code-block:: bash

   # View current rules
   sudo iptables -L -v -n                    # List all rules
   sudo iptables -L INPUT -v -n              # List INPUT chain
   sudo iptables -S                          # Show rules as commands
   
   # Basic rules
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT      # Allow SSH
   sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT      # Allow HTTP
   sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT     # Allow HTTPS
   sudo iptables -A INPUT -j DROP                          # Drop everything else
   
   # Delete rules
   sudo iptables -D INPUT 3                  # Delete rule #3 from INPUT
   sudo iptables -F                          # Flush all rules
   sudo iptables -F INPUT                    # Flush INPUT chain
   
   # Save/restore rules
   sudo iptables-save > /tmp/iptables.rules  # Save current rules
   sudo iptables-restore < /tmp/iptables.rules  # Restore rules
   
   # Make persistent (Debian/Ubuntu)
   sudo apt install iptables-persistent
   sudo netfilter-persistent save
   
   # Make persistent (RHEL/CentOS)
   sudo service iptables save

================================================================================
1. iptables Fundamentals
================================================================================

1.1 What is iptables?
---------------------

**iptables** is a user-space utility for configuring Linux kernel firewall (netfilter).

**Key Concepts:**

- **Tables:** Organize rules by function (filter, nat, mangle, raw)
- **Chains:** Lists of rules within tables (INPUT, OUTPUT, FORWARD, etc.)
- **Rules:** Conditions and actions for packets
- **Targets:** Actions to take (ACCEPT, DROP, REJECT, LOG, etc.)

**Packet Flow Diagram:**

.. code-block:: text

   INCOMING PACKET
        |
        v
   [PREROUTING] (nat, mangle, raw)
        |
        v
   [ROUTING DECISION]
        |
        +---> [FORWARD] (filter, mangle) ----> [POSTROUTING] (nat, mangle) --> OUT
        |
        v
   [INPUT] (filter, mangle)
        |
        v
   [LOCAL PROCESS]
        |
        v
   [OUTPUT] (filter, nat, mangle, raw)
        |
        v
   [POSTROUTING] (nat, mangle)
        |
        v
   OUTGOING PACKET

1.2 Tables and Chains
----------------------

**Tables:**

.. code-block:: text

   filter    - Default table for packet filtering
               Chains: INPUT, OUTPUT, FORWARD
   
   nat       - Network Address Translation
               Chains: PREROUTING, POSTROUTING, OUTPUT
   
   mangle    - Packet alteration (QoS, TTL, etc.)
               Chains: PREROUTING, POSTROUTING, INPUT, OUTPUT, FORWARD
   
   raw       - Bypass connection tracking
               Chains: PREROUTING, OUTPUT

**Default Chains:**

.. code-block:: text

   INPUT      - Packets destined for local system
   OUTPUT     - Packets originating from local system
   FORWARD    - Packets routed through system (router/gateway)
   PREROUTING - Packets before routing decision
   POSTROUTING - Packets after routing decision

1.3 Rule Syntax
----------------

**Basic Syntax:**

.. code-block:: bash

   iptables [-t table] -A CHAIN [match criteria] -j TARGET
   
   # Examples:
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

**Common Options:**

.. code-block:: text

   -t, --table         Specify table (default: filter)
   -A, --append        Append rule to chain
   -I, --insert        Insert rule at position
   -D, --delete        Delete rule
   -R, --replace       Replace rule
   -L, --list          List rules
   -F, --flush         Delete all rules
   -P, --policy        Set default policy
   -N, --new-chain     Create new chain
   -X, --delete-chain  Delete user-defined chain

================================================================================
2. Viewing and Managing Rules
================================================================================

2.1 List Rules
--------------

.. code-block:: bash

   # List all rules with line numbers
   sudo iptables -L -v -n --line-numbers
   
   # List specific chain
   sudo iptables -L INPUT -v -n --line-numbers
   
   # Show rules as commands (for backup/restore)
   sudo iptables -S
   sudo iptables -S INPUT
   
   # List specific table
   sudo iptables -t nat -L -v -n
   
   # Options explained:
   # -L: List rules
   # -v: Verbose (show packet/byte counters)
   # -n: Numeric output (don't resolve IPs/ports)
   # --line-numbers: Show rule numbers

2.2 Add Rules
-------------

**Append to end of chain:**

.. code-block:: bash

   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

**Insert at specific position:**

.. code-block:: bash

   # Insert at position 1 (top of chain)
   sudo iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT
   
   # Insert at position 5
   sudo iptables -I INPUT 5 -p tcp --dport 80 -j ACCEPT

**Replace existing rule:**

.. code-block:: bash

   # Replace rule #3
   sudo iptables -R INPUT 3 -p tcp --dport 8080 -j ACCEPT

2.3 Delete Rules
----------------

.. code-block:: bash

   # Delete by rule number
   sudo iptables -D INPUT 3
   
   # Delete by specification (exact match)
   sudo iptables -D INPUT -p tcp --dport 22 -j ACCEPT
   
   # Flush all rules in chain
   sudo iptables -F INPUT
   
   # Flush all rules in all chains
   sudo iptables -F
   
   # Flush specific table
   sudo iptables -t nat -F

2.4 Reset iptables
------------------

.. code-block:: bash

   # Complete reset (DANGEROUS - locks you out if remote!)
   sudo iptables -F                    # Flush all rules
   sudo iptables -X                    # Delete user chains
   sudo iptables -t nat -F
   sudo iptables -t nat -X
   sudo iptables -t mangle -F
   sudo iptables -t mangle -X
   sudo iptables -P INPUT ACCEPT       # Set default policies
   sudo iptables -P FORWARD ACCEPT
   sudo iptables -P OUTPUT ACCEPT

================================================================================
3. Basic Firewall Rules
================================================================================

3.1 Default Policies
--------------------

**Set Default Policies:**

.. code-block:: bash

   # Drop all incoming by default (whitelist approach)
   sudo iptables -P INPUT DROP
   
   # Allow all outgoing by default
   sudo iptables -P OUTPUT ACCEPT
   
   # Drop forwarding (not a router)
   sudo iptables -P FORWARD DROP
   
   # View current policies
   sudo iptables -L | grep policy

3.2 Allow Loopback
------------------

.. code-block:: bash

   # ALWAYS allow loopback (required for many services)
   sudo iptables -A INPUT -i lo -j ACCEPT
   sudo iptables -A OUTPUT -o lo -j ACCEPT

3.3 Allow Established Connections
----------------------------------

.. code-block:: bash

   # Allow established and related connections (ESSENTIAL)
   sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # Or using state module (older)
   sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
   
   # Connection states:
   # NEW          - New connection
   # ESTABLISHED  - Part of existing connection
   # RELATED      - Related to existing connection (FTP data, ICMP errors)
   # INVALID      - Packet doesn't match any connection

3.4 Common Service Rules
-------------------------

**SSH (Port 22):**

.. code-block:: bash

   # Allow SSH from anywhere
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Allow SSH from specific IP
   sudo iptables -A INPUT -p tcp -s 192.168.1.100 --dport 22 -j ACCEPT
   
   # Allow SSH from specific network
   sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT

**HTTP/HTTPS (Ports 80/443):**

.. code-block:: bash

   # Allow HTTP
   sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
   
   # Allow HTTPS
   sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
   
   # Allow both HTTP and HTTPS (multiport)
   sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

**DNS (Port 53):**

.. code-block:: bash

   # Allow DNS queries (UDP and TCP)
   sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 53 -j ACCEPT
   
   # Allow DNS responses (if you're querying external DNS)
   sudo iptables -A INPUT -p udp --sport 53 -j ACCEPT

**MySQL/MariaDB (Port 3306):**

.. code-block:: bash

   # Allow from specific IP
   sudo iptables -A INPUT -p tcp -s 192.168.1.50 --dport 3306 -j ACCEPT
   
   # Allow from specific network
   sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 3306 -j ACCEPT

**PostgreSQL (Port 5432):**

.. code-block:: bash

   sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 5432 -j ACCEPT

**SMTP (Port 25):**

.. code-block:: bash

   sudo iptables -A INPUT -p tcp --dport 25 -j ACCEPT

**Port Range:**

.. code-block:: bash

   # Allow port range
   sudo iptables -A INPUT -p tcp --dport 3000:3100 -j ACCEPT

================================================================================
4. Advanced Filtering
================================================================================

4.1 Source/Destination Filtering
---------------------------------

**By IP Address:**

.. code-block:: bash

   # Allow from specific source IP
   sudo iptables -A INPUT -s 192.168.1.100 -j ACCEPT
   
   # Block specific source IP
   sudo iptables -A INPUT -s 192.168.1.200 -j DROP
   
   # Allow from subnet
   sudo iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
   
   # Block subnet
   sudo iptables -A INPUT -s 10.0.0.0/8 -j DROP
   
   # Multiple IPs (use iprange module)
   sudo iptables -A INPUT -m iprange --src-range 192.168.1.100-192.168.1.200 -j ACCEPT

**By Interface:**

.. code-block:: bash

   # Allow on specific interface
   sudo iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
   
   # Block on interface
   sudo iptables -A INPUT -i eth1 -j DROP
   
   # Allow outgoing on specific interface
   sudo iptables -A OUTPUT -o eth0 -j ACCEPT

**By MAC Address:**

.. code-block:: bash

   # Allow from specific MAC
   sudo iptables -A INPUT -m mac --mac-source 00:11:22:33:44:55 -j ACCEPT
   
   # Block MAC address
   sudo iptables -A INPUT -m mac --mac-source AA:BB:CC:DD:EE:FF -j DROP

4.2 Rate Limiting
-----------------

**Limit Connection Rate:**

.. code-block:: bash

   # Limit SSH connections to 3 per minute
   sudo iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min --limit-burst 5 -j ACCEPT
   sudo iptables -A INPUT -p tcp --dport 22 -j DROP
   
   # Limit HTTP connections
   sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/sec --limit-burst 200 -j ACCEPT

**Limit Connections per IP:**

.. code-block:: bash

   # Limit to 10 concurrent SSH connections per IP
   sudo iptables -A INPUT -p tcp --dport 22 -m connlimit --connlimit-above 10 -j REJECT
   
   # Limit HTTP connections per IP
   sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 50 -j REJECT

**Prevent SSH Brute Force:**

.. code-block:: bash

   # Create new chain for SSH
   sudo iptables -N SSH_CHECK
   
   # Send SSH traffic to custom chain
   sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW -j SSH_CHECK
   
   # Track SSH attempts
   sudo iptables -A SSH_CHECK -m recent --set --name SSH
   
   # Drop if more than 3 attempts in 60 seconds
   sudo iptables -A SSH_CHECK -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
   
   # Accept otherwise
   sudo iptables -A SSH_CHECK -j ACCEPT

4.3 Time-Based Rules
--------------------

.. code-block:: bash

   # Allow SSH only during business hours (9 AM - 5 PM)
   sudo iptables -A INPUT -p tcp --dport 22 -m time --timestart 09:00 --timestop 17:00 -j ACCEPT
   
   # Allow only on weekdays
   sudo iptables -A INPUT -p tcp --dport 22 -m time --weekdays Mon,Tue,Wed,Thu,Fri -j ACCEPT
   
   # Combined: weekdays during business hours
   sudo iptables -A INPUT -p tcp --dport 22 -m time --timestart 09:00 --timestop 17:00 --weekdays Mon,Tue,Wed,Thu,Fri -j ACCEPT

4.4 ICMP Rules
--------------

.. code-block:: bash

   # Allow ping (echo request)
   sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
   
   # Allow ping replies
   sudo iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
   
   # Allow destination unreachable
   sudo iptables -A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT
   
   # Rate limit ping to prevent flood
   sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/sec -j ACCEPT
   sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
   
   # Block all ICMP
   sudo iptables -A INPUT -p icmp -j DROP

================================================================================
5. Logging
================================================================================

5.1 Basic Logging
-----------------

.. code-block:: bash

   # Log dropped packets (before DROP rule)
   sudo iptables -A INPUT -j LOG --log-prefix "iptables-dropped: " --log-level 4
   sudo iptables -A INPUT -j DROP
   
   # Log accepted packets
   sudo iptables -A INPUT -p tcp --dport 22 -j LOG --log-prefix "SSH-accepted: "
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # View logs
   sudo tail -f /var/log/kern.log | grep iptables
   sudo journalctl -k -f | grep iptables

5.2 Targeted Logging
--------------------

.. code-block:: bash

   # Log only specific traffic
   sudo iptables -A INPUT -p tcp --dport 80 -j LOG --log-prefix "HTTP: "
   
   # Log with limit (prevent log flooding)
   sudo iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-denied: " --log-level 4
   
   # Log to specific file (configure rsyslog)
   # /etc/rsyslog.d/10-iptables.conf:
   # :msg,contains,"iptables-" /var/log/iptables.log
   # & stop

5.3 Log Options
---------------

.. code-block:: bash

   # Full logging options
   sudo iptables -A INPUT -j LOG \
       --log-prefix "DROPPED: " \
       --log-level 4 \
       --log-tcp-sequence \
       --log-tcp-options \
       --log-ip-options
   
   # Log levels:
   # 0 = emerg
   # 1 = alert
   # 2 = crit
   # 3 = err
   # 4 = warning
   # 5 = notice
   # 6 = info
   # 7 = debug

================================================================================
6. NAT (Network Address Translation)
================================================================================

6.1 Enable IP Forwarding
-------------------------

.. code-block:: bash

   # Temporary enable
   sudo sysctl -w net.ipv4.ip_forward=1
   
   # Permanent enable
   echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   
   # Verify
   cat /proc/sys/net/ipv4/ip_forward

6.2 SNAT (Source NAT)
---------------------

**Masquerading (Dynamic IP):**

.. code-block:: bash

   # Masquerade outgoing traffic (for dynamic IP/DHCP)
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # Masquerade specific subnet
   sudo iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE

**Static SNAT:**

.. code-block:: bash

   # SNAT to specific IP (for static IP)
   sudo iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 203.0.113.10
   
   # SNAT with port range
   sudo iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 203.0.113.10:1024-65535

6.3 DNAT (Destination NAT)
---------------------------

**Port Forwarding:**

.. code-block:: bash

   # Forward external port 8080 to internal server port 80
   sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80
   
   # Forward SSH from external to internal server
   sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 2222 -j DNAT --to-destination 192.168.1.50:22
   
   # Forward range of ports
   sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 3000:3100 -j DNAT --to-destination 192.168.1.100

**Load Balancing:**

.. code-block:: bash

   # Round-robin between servers
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -m statistic --mode random --probability 0.5 -j DNAT --to-destination 192.168.1.10:80
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.11:80

6.4 REDIRECT
------------

.. code-block:: bash

   # Redirect port 80 to local port 8080
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
   
   # Transparent proxy
   sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128

================================================================================
7. Complete Firewall Examples
================================================================================

7.1 Basic Web Server
--------------------

.. code-block:: bash

   #!/bin/bash
   # Basic web server firewall
   
   # Flush existing rules
   iptables -F
   
   # Set default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Allow loopback
   iptables -A INPUT -i lo -j ACCEPT
   
   # Allow established connections
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # Allow SSH
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   
   # Allow HTTP/HTTPS
   iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
   
   # Allow ping
   iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
   
   # Log dropped packets
   iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: "
   
   # Save rules
   iptables-save > /etc/iptables/rules.v4

7.2 Database Server
-------------------

.. code-block:: bash

   #!/bin/bash
   # Database server firewall (MySQL)
   
   # Flush
   iptables -F
   
   # Default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Loopback
   iptables -A INPUT -i lo -j ACCEPT
   
   # Established connections
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # SSH from management network only
   iptables -A INPUT -p tcp -s 192.168.100.0/24 --dport 22 -j ACCEPT
   
   # MySQL from application servers only
   iptables -A INPUT -p tcp -s 192.168.1.10 --dport 3306 -j ACCEPT
   iptables -A INPUT -p tcp -s 192.168.1.11 --dport 3306 -j ACCEPT
   
   # Drop everything else
   iptables -A INPUT -j DROP

7.3 Router/Gateway
------------------

.. code-block:: bash

   #!/bin/bash
   # Router/Gateway firewall
   
   # Enable IP forwarding
   sysctl -w net.ipv4.ip_forward=1
   
   # Flush
   iptables -F
   iptables -t nat -F
   
   # Default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Loopback
   iptables -A INPUT -i lo -j ACCEPT
   
   # Established connections
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # SSH from LAN only
   iptables -A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT
   
   # Allow LAN to WAN
   iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
   
   # NAT
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # Port forwarding (web server on LAN)
   iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.100:80
   iptables -A FORWARD -p tcp -d 192.168.1.100 --dport 80 -j ACCEPT

================================================================================
8. Persistence and Management
================================================================================

8.1 Save and Restore Rules
---------------------------

**Manual Save/Restore:**

.. code-block:: bash

   # Save current rules
   sudo iptables-save > /tmp/iptables.rules
   
   # Restore rules
   sudo iptables-restore < /tmp/iptables.rules
   
   # Save with timestamp
   sudo iptables-save > /etc/iptables/rules-$(date +%Y%m%d).v4

**Debian/Ubuntu (iptables-persistent):**

.. code-block:: bash

   # Install
   sudo apt install iptables-persistent
   
   # Save current rules
   sudo netfilter-persistent save
   
   # Reload rules
   sudo netfilter-persistent reload
   
   # Rules stored in:
   # /etc/iptables/rules.v4 (IPv4)
   # /etc/iptables/rules.v6 (IPv6)

**RHEL/CentOS:**

.. code-block:: bash

   # Save rules
   sudo service iptables save
   # Saves to /etc/sysconfig/iptables
   
   # Restore on boot (enabled by default)
   sudo systemctl enable iptables
   
   # Reload rules
   sudo systemctl restart iptables

8.2 Backup and Restore
----------------------

.. code-block:: bash

   # Backup current rules
   sudo iptables-save > ~/iptables-backup-$(date +%Y%m%d).rules
   
   # Restore from backup
   sudo iptables-restore < ~/iptables-backup-20260119.rules
   
   # Test rules before making permanent
   sudo iptables-restore < test-rules.txt
   # Test...
   sudo iptables-save > /etc/iptables/rules.v4  # Make permanent

8.3 Automated Backup Script
----------------------------

.. code-block:: bash

   #!/bin/bash
   # /usr/local/bin/backup-iptables.sh
   
   BACKUP_DIR="/var/backups/iptables"
   DATE=$(date +%Y%m%d-%H%M)
   
   mkdir -p $BACKUP_DIR
   
   # Backup IPv4 rules
   iptables-save > $BACKUP_DIR/rules-v4-$DATE.txt
   
   # Backup IPv6 rules
   ip6tables-save > $BACKUP_DIR/rules-v6-$DATE.txt
   
   # Keep only last 30 days
   find $BACKUP_DIR -name "rules-*" -mtime +30 -delete
   
   # Add to crontab:
   # 0 2 * * * /usr/local/bin/backup-iptables.sh

================================================================================
9. Troubleshooting
================================================================================

9.1 Common Issues
-----------------

**Locked Out After Setting Rules:**

.. code-block:: bash

   # ALWAYS test with a timeout:
   sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   sleep 300 && sudo iptables -F  # Resets after 5 minutes
   
   # Or use at command:
   echo "iptables -F" | sudo at now + 5 minutes

**Rule Not Working:**

.. code-block:: bash

   # Check rule order (rules are processed top-to-bottom)
   sudo iptables -L INPUT -v -n --line-numbers
   
   # Check if earlier rule is matching
   # Insert rule at top:
   sudo iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT

**Check Rule Matching:**

.. code-block:: bash

   # View packet/byte counters
   sudo iptables -L -v -n
   
   # Zero counters
   sudo iptables -Z
   
   # Test traffic and check counters again
   sudo iptables -L -v -n

9.2 Debug Rules
---------------

.. code-block:: bash

   # Add logging to debug
   sudo iptables -I INPUT 1 -p tcp --dport 80 -j LOG --log-prefix "HTTP-DEBUG: "
   
   # Watch logs in real-time
   sudo tail -f /var/log/kern.log | grep HTTP-DEBUG
   
   # Test connection
   curl http://localhost
   
   # Remove debug rule when done
   sudo iptables -D INPUT 1

9.3 Performance Issues
----------------------

.. code-block:: bash

   # Check number of rules
   sudo iptables -L | wc -l
   
   # Use ipsets for large IP lists (much faster)
   sudo apt install ipset
   
   # Create IP set
   sudo ipset create blacklist hash:ip
   sudo ipset add blacklist 1.2.3.4
   sudo ipset add blacklist 5.6.7.8
   
   # Use in iptables
   sudo iptables -A INPUT -m set --match-set blacklist src -j DROP

================================================================================
10. Security Best Practices
================================================================================

10.1 Firewall Hardening
-----------------------

.. code-block:: bash

   # 1. Default DROP policy
   sudo iptables -P INPUT DROP
   sudo iptables -P FORWARD DROP
   
   # 2. Drop invalid packets
   sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
   
   # 3. Drop fragmented packets
   sudo iptables -A INPUT -f -j DROP
   
   # 4. Drop XMAS packets
   sudo iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
   
   # 5. Drop NULL packets
   sudo iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
   
   # 6. Drop SYN flood
   sudo iptables -A INPUT -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
   
   # 7. Limit SSH connections
   sudo iptables -A INPUT -p tcp --dport 22 -m connlimit --connlimit-above 3 -j REJECT
   
   # 8. Rate limit connections
   sudo iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min -j ACCEPT

10.2 Complete Hardened Firewall
--------------------------------

.. code-block:: bash

   #!/bin/bash
   # Hardened iptables firewall script
   
   # Flush all rules
   iptables -F
   iptables -X
   iptables -t nat -F
   iptables -t nat -X
   iptables -t mangle -F
   iptables -t mangle -X
   
   # Set default policies
   iptables -P INPUT DROP
   iptables -P FORWARD DROP
   iptables -P OUTPUT ACCEPT
   
   # Allow loopback
   iptables -A INPUT -i lo -j ACCEPT
   iptables -A OUTPUT -o lo -j ACCEPT
   
   # Drop invalid packets
   iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
   
   # Allow established and related
   iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
   
   # Anti-spoofing
   iptables -A INPUT -s 127.0.0.0/8 ! -i lo -j DROP
   iptables -A INPUT -s 0.0.0.0/8 -j DROP
   iptables -A INPUT -s 169.254.0.0/16 -j DROP
   iptables -A INPUT -s 224.0.0.0/4 -j DROP
   iptables -A INPUT -s 240.0.0.0/5 -j DROP
   
   # Drop fragmented packets
   iptables -A INPUT -f -j DROP
   
   # Drop malformed packets
   iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
   iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
   iptables -A INPUT -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
   iptables -A INPUT -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
   
   # Rate-limited SSH with brute force protection
   iptables -N SSH_CHECK
   iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j SSH_CHECK
   iptables -A SSH_CHECK -m recent --set --name SSH
   iptables -A SSH_CHECK -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
   iptables -A SSH_CHECK -j ACCEPT
   
   # Allow HTTP/HTTPS with rate limiting
   iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/sec --limit-burst 200 -j ACCEPT
   iptables -A INPUT -p tcp --dport 443 -m limit --limit 100/sec --limit-burst 200 -j ACCEPT
   
   # Allow ping with rate limit
   iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/sec -j ACCEPT
   
   # Log dropped packets (with limit to prevent log flooding)
   iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: " --log-level 4
   
   # Drop everything else
   iptables -A INPUT -j DROP
   
   # Save rules
   iptables-save > /etc/iptables/rules.v4

================================================================================
CROSS-REFERENCES
================================================================================

Related Cheatsheets:
- Firewall_nftables_firewalld.rst - Modern firewall alternatives
- Linux_Security_Basics.rst - Overall security principles
- SSH_Hardening.rst - Secure SSH configuration
- Kernel_Hardening.rst - Kernel-level network security
- Logging_Log_Security.rst - Firewall log analysis

================================================================================
END OF FIREWALL iptables
================================================================================
