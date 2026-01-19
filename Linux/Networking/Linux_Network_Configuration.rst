===================================
Linux Network Configuration Guide
===================================

:Author: Linux Network Documentation
:Date: January 2026
:Version: 1.0

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Interface Configuration
-----------------------

.. code-block:: bash

   # View interfaces
   ip link show
   ip addr show
   
   # Bring interface up/down
   ip link set eth0 up
   ip link set eth0 down
   
   # Add IP address
   ip addr add 192.168.1.10/24 dev eth0
   
   # Delete IP address
   ip addr del 192.168.1.10/24 dev eth0
   
   # Add default route
   ip route add default via 192.168.1.1
   
   # Add static route
   ip route add 10.0.0.0/8 via 192.168.1.254

Persistent Network Configuration
---------------------------------

**NetworkManager (Ubuntu/Fedora)**

.. code-block:: bash

   # Using nmcli
   nmcli con add type ethernet con-name eth0 ifname eth0 \
       ip4 192.168.1.10/24 gw4 192.168.1.1
   
   nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
   nmcli con up eth0

**netplan (Ubuntu 18.04+)**

.. code-block:: yaml

   # /etc/netplan/01-netcfg.yaml
   network:
     version: 2
     ethernets:
       eth0:
         dhcp4: no
         addresses:
           - 192.168.1.10/24
         gateway4: 192.168.1.1
         nameservers:
           addresses: [8.8.8.8, 8.8.4.4]
   
   # Apply
   sudo netplan apply

**Debian/Ubuntu interfaces**

.. code-block:: bash

   # /etc/network/interfaces
   auto eth0
   iface eth0 inet static
       address 192.168.1.10
       netmask 255.255.255.0
       gateway 192.168.1.1
       dns-nameservers 8.8.8.8 8.8.4.4

Interface Management
====================

ip Command
----------

.. code-block:: bash

   # Show all interfaces
   ip link show
   
   # Show specific interface
   ip link show eth0
   
   # Show all addresses
   ip addr show
   
   # Show specific address
   ip addr show dev eth0
   
   # Set interface up
   ip link set eth0 up
   
   # Set interface down
   ip link set eth0 down
   
   # Set MTU
   ip link set eth0 mtu 9000
   
   # Set MAC address
   ip link set eth0 address 00:11:22:33:44:55
   
   # Rename interface
   ip link set eth0 name lan0

Adding IP Addresses
-------------------

.. code-block:: bash

   # Add IPv4 address
   ip addr add 192.168.1.10/24 dev eth0
   
   # Add secondary address
   ip addr add 192.168.1.20/24 dev eth0
   
   # Add with broadcast
   ip addr add 192.168.1.10/24 brd + dev eth0
   
   # Add IPv6 address
   ip addr add 2001:db8::10/64 dev eth0
   
   # Delete address
   ip addr del 192.168.1.10/24 dev eth0
   
   # Flush all addresses
   ip addr flush dev eth0

Virtual Interfaces
------------------

.. code-block:: bash

   # Create VLAN interface
   ip link add link eth0 name eth0.100 type vlan id 100
   ip addr add 192.168.100.10/24 dev eth0.100
   ip link set eth0.100 up
   
   # Create bridge
   ip link add br0 type bridge
   ip link set eth0 master br0
   ip link set eth1 master br0
   ip link set br0 up
   
   # Create bond
   ip link add bond0 type bond mode 802.3ad
   ip link set eth0 master bond0
   ip link set eth1 master bond0
   ip link set bond0 up
   
   # Create dummy interface
   ip link add dummy0 type dummy
   ip addr add 10.0.0.1/32 dev dummy0
   ip link set dummy0 up

Routing Configuration
=====================

Basic Routing
-------------

.. code-block:: bash

   # Show routing table
   ip route show
   ip route show table all
   
   # Add default route
   ip route add default via 192.168.1.1
   ip route add default via 192.168.1.1 dev eth0
   
   # Add network route
   ip route add 10.0.0.0/8 via 192.168.1.254
   
   # Add host route
   ip route add 192.168.2.10 via 192.168.1.254
   
   # Delete route
   ip route del 10.0.0.0/8
   
   # Replace route
   ip route replace default via 192.168.1.2
   
   # Change route metric
   ip route add default via 192.168.1.1 metric 100

Multiple Routing Tables
------------------------

.. code-block:: bash

   # Define custom table in /etc/iproute2/rt_tables
   echo "200 custom" >> /etc/iproute2/rt_tables
   
   # Add route to custom table
   ip route add 10.0.0.0/8 via 192.168.2.1 table custom
   
   # Add rule to use custom table
   ip rule add from 192.168.2.0/24 table custom
   
   # Show rules
   ip rule show
   
   # Show specific table
   ip route show table custom

Policy Routing
--------------

.. code-block:: bash

   # Route based on source address
   ip rule add from 192.168.1.0/24 table 100
   ip route add default via 10.0.0.1 table 100
   
   # Route based on destination
   ip rule add to 172.16.0.0/12 table 101
   ip route add default via 10.0.0.2 table 101
   
   # Route based on interface
   ip rule add iif eth1 table 102
   
   # Priority
   ip rule add from 192.168.1.0/24 table 100 priority 100

DNS Configuration
=================

resolv.conf
-----------

.. code-block:: bash

   # /etc/resolv.conf
   nameserver 8.8.8.8
   nameserver 8.8.4.4
   search example.com
   options timeout:2 attempts:3

systemd-resolved
----------------

.. code-block:: bash

   # Status
   resolvectl status
   
   # Set DNS for interface
   resolvectl dns eth0 8.8.8.8 8.8.4.4
   
   # Set domain
   resolvectl domain eth0 example.com
   
   # Configuration file
   # /etc/systemd/resolved.conf
   [Resolve]
   DNS=8.8.8.8 8.8.4.4
   FallbackDNS=1.1.1.1
   Domains=example.com
   
   # Restart
   systemctl restart systemd-resolved

Network Bonding
===============

Creating Bond
-------------

.. code-block:: bash

   # Load bonding module
   modprobe bonding
   
   # Create bond interface
   ip link add bond0 type bond mode 802.3ad
   
   # Set bond parameters
   echo 802.3ad > /sys/class/net/bond0/bonding/mode
   echo 100 > /sys/class/net/bond0/bonding/miimon
   
   # Add slaves
   ip link set eth0 down
   ip link set eth0 master bond0
   ip link set eth1 down
   ip link set eth1 master bond0
   
   # Configure bond IP
   ip addr add 192.168.1.10/24 dev bond0
   ip link set bond0 up

Bond Modes
----------

.. code-block:: bash

   # mode 0: balance-rr (round-robin)
   # mode 1: active-backup
   # mode 2: balance-xor
   # mode 3: broadcast
   # mode 4: 802.3ad (LACP)
   # mode 5: balance-tlb
   # mode 6: balance-alb
   
   # Check bond status
   cat /proc/net/bonding/bond0

VLAN Configuration
==================

Creating VLANs
--------------

.. code-block:: bash

   # Load 8021q module
   modprobe 8021q
   
   # Create VLAN
   ip link add link eth0 name eth0.100 type vlan id 100
   
   # Configure VLAN
   ip addr add 192.168.100.10/24 dev eth0.100
   ip link set eth0.100 up
   
   # Multiple VLANs
   ip link add link eth0 name eth0.200 type vlan id 200
   ip addr add 192.168.200.10/24 dev eth0.200
   ip link set eth0.200 up
   
   # Delete VLAN
   ip link delete eth0.100

Bridge Configuration
====================

Creating Bridge
---------------

.. code-block:: bash

   # Create bridge
   ip link add br0 type bridge
   
   # Add interfaces to bridge
   ip link set eth0 master br0
   ip link set eth1 master br0
   
   # Configure bridge
   ip addr add 192.168.1.10/24 dev br0
   ip link set br0 up
   
   # Enable STP
   ip link set br0 type bridge stp_state 1
   
   # Set bridge priority
   ip link set br0 type bridge priority 32768
   
   # Remove interface from bridge
   ip link set eth0 nomaster

brctl (Legacy)
--------------

.. code-block:: bash

   # Create bridge
   brctl addbr br0
   
   # Add interface
   brctl addif br0 eth0
   brctl addif br0 eth1
   
   # Show bridges
   brctl show
   
   # Enable STP
   brctl stp br0 on
   
   # Delete bridge
   brctl delbr br0

NAT and Masquerading
====================

iptables NAT
------------

.. code-block:: bash

   # Enable IP forwarding
   echo 1 > /proc/sys/net/ipv4/ip_forward
   
   # Masquerade (SNAT with dynamic IP)
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   
   # SNAT (static IP)
   iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 \
       -j SNAT --to-source 203.0.113.10
   
   # DNAT (port forwarding)
   iptables -t nat -A PREROUTING -p tcp --dport 80 \
       -j DNAT --to-destination 192.168.1.10:8080
   
   # Save rules
   iptables-save > /etc/iptables/rules.v4

nftables NAT
------------

.. code-block:: bash

   # Create NAT table
   nft add table nat
   nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
   
   # Masquerade
   nft add rule nat postrouting oif eth0 masquerade
   
   # SNAT
   nft add rule nat postrouting ip saddr 192.168.1.0/24 oif eth0 \
       snat to 203.0.113.10
   
   # DNAT
   nft add chain nat prerouting { type nat hook prerouting priority -100 \; }
   nft add rule nat prerouting tcp dport 80 \
       dnat to 192.168.1.10:8080

NetworkManager
==============

Connection Management
---------------------

.. code-block:: bash

   # List connections
   nmcli con show
   
   # Show connection details
   nmcli con show eth0
   
   # Create connection
   nmcli con add type ethernet con-name eth0 ifname eth0
   
   # Modify connection
   nmcli con mod eth0 ipv4.addresses 192.168.1.10/24
   nmcli con mod eth0 ipv4.gateway 192.168.1.1
   nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
   nmcli con mod eth0 ipv4.method manual
   
   # Activate connection
   nmcli con up eth0
   
   # Deactivate connection
   nmcli con down eth0
   
   # Delete connection
   nmcli con delete eth0

Device Management
-----------------

.. code-block:: bash

   # List devices
   nmcli dev status
   
   # Show device details
   nmcli dev show eth0
   
   # Connect device
   nmcli dev connect eth0
   
   # Disconnect device
   nmcli dev disconnect eth0

WiFi Configuration
==================

wpa_supplicant
--------------

.. code-block:: bash

   # /etc/wpa_supplicant/wpa_supplicant.conf
   network={
       ssid="MyNetwork"
       psk="password"
   }
   
   # Connect
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
   
   # Get IP
   dhclient wlan0

NetworkManager WiFi
-------------------

.. code-block:: bash

   # List networks
   nmcli dev wifi list
   
   # Connect to network
   nmcli dev wifi connect MyNetwork password "mypassword"
   
   # Show saved connections
   nmcli con show
   
   # Connect to saved network
   nmcli con up MyNetwork

Best Practices
==============

1. **Use ip command** instead of ifconfig/route
2. **Make configurations persistent**
3. **Document network changes**
4. **Test before making permanent**
5. **Use NetworkManager** for desktops
6. **Use static IPs** for servers
7. **Enable IP forwarding** only when needed
8. **Configure proper DNS**
9. **Use policy routing** for complex setups
10. **Monitor network statistics**

Common Pitfalls
===============

1. **Forgetting to save** configurations
2. **Not enabling IP forwarding** for NAT
3. **Conflicting network managers**
4. **Wrong subnet masks**
5. **Missing default gateway**
6. **DNS not configured**

Diagnostic Commands
===================

.. code-block:: bash

   # Interface status
   ip link show
   ip addr show
   
   # Routing table
   ip route show
   
   # ARP cache
   ip neigh show
   
   # Network statistics
   ip -s link show eth0
   
   # Connection tracking
   conntrack -L
   
   # Test connectivity
   ping 8.8.8.8
   traceroute 8.8.8.8
   mtr 8.8.8.8

See Also
========

- Linux_Network_Tools.rst
- Linux_Network_Protocols.rst
- Socket_Programming.rst

References
==========

- man ip
- man nmcli
- man netplan
