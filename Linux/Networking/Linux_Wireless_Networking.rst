===================================
Linux Wireless Networking Guide
===================================

:Author: Linux Network Documentation
:Date: January 2026
:Version: 1.0

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

Basic WiFi Commands
-------------------

.. code-block:: bash

   # List WiFi interfaces
   iw dev
   ip link show
   
   # Scan networks
   iw dev wlan0 scan
   nmcli dev wifi list
   
   # Connect with NetworkManager
   nmcli dev wifi connect "SSID" password "PASSWORD"
   
   # Connect with wpa_supplicant
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
   dhclient wlan0
   
   # Check connection
   iw dev wlan0 link
   iw dev wlan0 station dump

WiFi Tools
==========

iw Command
----------

.. code-block:: bash

   # List wireless devices
   iw dev
   
   # Show device info
   iw dev wlan0 info
   
   # Scan for networks
   iw dev wlan0 scan
   
   # Show current connection
   iw dev wlan0 link
   
   # Get station statistics
   iw dev wlan0 station dump
   
   # Set interface up
   ip link set wlan0 up
   
   # Set interface down
   ip link set wlan0 down
   
   # Connect to open network
   iw dev wlan0 connect "OpenNetwork"
   
   # Disconnect
   iw dev wlan0 disconnect
   
   # Set channel
   iw dev wlan0 set channel 6
   
   # Set power save
   iw dev wlan0 set power_save on
   iw dev wlan0 set power_save off

iwconfig (Legacy)
-----------------

.. code-block:: bash

   # Show wireless info
   iwconfig wlan0
   
   # Set ESSID
   iwconfig wlan0 essid "MyNetwork"
   
   # Set channel
   iwconfig wlan0 channel 6
   
   # Set mode
   iwconfig wlan0 mode managed
   iwconfig wlan0 mode ad-hoc
   
   # Set TX power
   iwconfig wlan0 txpower 20dBm
   
   # Set rate
   iwconfig wlan0 rate 54M

iwlist
------

.. code-block:: bash

   # Scan for networks
   iwlist wlan0 scan
   
   # List supported channels
   iwlist wlan0 channel
   
   # List supported rates
   iwlist wlan0 rate
   
   # List supported frequencies
   iwlist wlan0 frequency
   
   # Show power management
   iwlist wlan0 power

WPA Supplicant
==============

Configuration
-------------

.. code-block:: bash

   # /etc/wpa_supplicant/wpa_supplicant.conf
   
   # WPA/WPA2-PSK
   network={
       ssid="MyNetwork"
       psk="MyPassword"
   }
   
   # WPA/WPA2-PSK with hidden SSID
   network={
       ssid="HiddenNetwork"
       scan_ssid=1
       psk="MyPassword"
   }
   
   # Open network
   network={
       ssid="OpenNetwork"
       key_mgmt=NONE
   }
   
   # WEP
   network={
       ssid="WEPNetwork"
       key_mgmt=NONE
       wep_key0="1234567890"
       wep_tx_keyidx=0
   }
   
   # WPA-Enterprise (EAP-PEAP/MSCHAPv2)
   network={
       ssid="EnterpriseNetwork"
       key_mgmt=WPA-EAP
       eap=PEAP
       identity="username"
       password="password"
       phase2="auth=MSCHAPV2"
   }
   
   # WPA-Enterprise (EAP-TLS)
   network={
       ssid="EnterpriseNetwork"
       key_mgmt=WPA-EAP
       eap=TLS
       identity="username"
       client_cert="/path/to/client-cert.pem"
       private_key="/path/to/private-key.pem"
       private_key_passwd="password"
       ca_cert="/path/to/ca-cert.pem"
   }

Running wpa_supplicant
----------------------

.. code-block:: bash

   # Start wpa_supplicant
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
   
   # With logging
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf \
       -f /var/log/wpa_supplicant.log
   
   # Debug mode
   wpa_supplicant -dd -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
   
   # With specific driver
   wpa_supplicant -B -i wlan0 -D nl80211 \
       -c /etc/wpa_supplicant/wpa_supplicant.conf
   
   # Generate PSK
   wpa_passphrase "SSID" "password"
   
   # Add to config
   wpa_passphrase "SSID" "password" >> /etc/wpa_supplicant/wpa_supplicant.conf

wpa_cli
-------

.. code-block:: bash

   # Interactive mode
   wpa_cli
   
   # Status
   wpa_cli status
   
   # Scan
   wpa_cli scan
   wpa_cli scan_results
   
   # List networks
   wpa_cli list_networks
   
   # Add network
   wpa_cli add_network
   wpa_cli set_network 0 ssid '"MyNetwork"'
   wpa_cli set_network 0 psk '"MyPassword"'
   wpa_cli enable_network 0
   
   # Select network
   wpa_cli select_network 0
   
   # Remove network
   wpa_cli remove_network 0
   
   # Save configuration
   wpa_cli save_config
   
   # Reconnect
   wpa_cli reassociate
   wpa_cli reconnect
   
   # Disconnect
   wpa_cli disconnect

NetworkManager
==============

WiFi with nmcli
---------------

.. code-block:: bash

   # List available networks
   nmcli dev wifi list
   
   # Rescan
   nmcli dev wifi rescan
   
   # Connect to network
   nmcli dev wifi connect "SSID" password "PASSWORD"
   
   # Connect to hidden network
   nmcli dev wifi connect "SSID" password "PASSWORD" hidden yes
   
   # Show saved connections
   nmcli con show
   
   # Show connection details
   nmcli con show "SSID"
   
   # Modify connection
   nmcli con mod "SSID" wifi-sec.psk "NewPassword"
   
   # Connect to saved network
   nmcli con up "SSID"
   
   # Disconnect
   nmcli con down "SSID"
   nmcli dev disconnect wlan0
   
   # Delete connection
   nmcli con delete "SSID"
   
   # Turn WiFi on/off
   nmcli radio wifi on
   nmcli radio wifi off

Connection Profiles
-------------------

.. code-block:: bash

   # Create WiFi connection
   nmcli con add type wifi con-name "MyWiFi" ifname wlan0 ssid "SSID"
   
   # Set password
   nmcli con mod "MyWiFi" wifi-sec.key-mgmt wpa-psk
   nmcli con mod "MyWiFi" wifi-sec.psk "PASSWORD"
   
   # Set static IP
   nmcli con mod "MyWiFi" ipv4.method manual
   nmcli con mod "MyWiFi" ipv4.addresses 192.168.1.10/24
   nmcli con mod "MyWiFi" ipv4.gateway 192.168.1.1
   nmcli con mod "MyWiFi" ipv4.dns "8.8.8.8 8.8.4.4"
   
   # Autoconnect
   nmcli con mod "MyWiFi" connection.autoconnect yes
   
   # Priority
   nmcli con mod "MyWiFi" connection.autoconnect-priority 10

Access Point Mode
=================

hostapd
-------

.. code-block:: bash

   # /etc/hostapd/hostapd.conf
   interface=wlan0
   driver=nl80211
   ssid=MyAccessPoint
   hw_mode=g
   channel=6
   
   # WPA2
   wpa=2
   wpa_passphrase=MyPassword
   wpa_key_mgmt=WPA-PSK
   wpa_pairwise=CCMP
   rsn_pairwise=CCMP
   
   # Optional: Hide SSID
   ignore_broadcast_ssid=1
   
   # Optional: MAC filtering
   macaddr_acl=1
   accept_mac_file=/etc/hostapd/hostapd.accept
   deny_mac_file=/etc/hostapd/hostapd.deny
   
   # Start hostapd
   hostapd /etc/hostapd/hostapd.conf
   
   # Background
   hostapd -B /etc/hostapd/hostapd.conf

DHCP Server for AP
------------------

.. code-block:: bash

   # Configure interface
   ip addr add 192.168.10.1/24 dev wlan0
   ip link set wlan0 up
   
   # Install and configure dnsmasq
   # /etc/dnsmasq.conf
   interface=wlan0
   dhcp-range=192.168.10.10,192.168.10.100,255.255.255.0,24h
   
   # Start dnsmasq
   dnsmasq -C /etc/dnsmasq.conf
   
   # Enable forwarding
   sysctl -w net.ipv4.ip_forward=1
   
   # NAT
   iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

Create AP with NetworkManager
------------------------------

.. code-block:: bash

   # Create hotspot
   nmcli dev wifi hotspot ifname wlan0 ssid "MyHotspot" password "MyPassword"
   
   # Custom configuration
   nmcli con add type wifi ifname wlan0 con-name "MyAP" \
       autoconnect no ssid "MyAccessPoint"
   nmcli con mod "MyAP" 802-11-wireless.mode ap
   nmcli con mod "MyAP" 802-11-wireless.band bg
   nmcli con mod "MyAP" 802-11-wireless.channel 6
   nmcli con mod "MyAP" ipv4.method shared
   nmcli con mod "MyAP" wifi-sec.key-mgmt wpa-psk
   nmcli con mod "MyAP" wifi-sec.psk "MyPassword"
   
   # Start AP
   nmcli con up "MyAP"

WiFi Diagnostics
================

Signal Strength
---------------

.. code-block:: bash

   # Using iw
   iw dev wlan0 link
   iw dev wlan0 station dump
   
   # Using iwconfig
   iwconfig wlan0
   
   # Watch signal strength
   watch -n 1 iw dev wlan0 station dump
   
   # Signal quality
   cat /proc/net/wireless

Link Quality Metrics
--------------------

.. code-block:: bash

   # Get detailed stats
   iw dev wlan0 station dump
   
   # Output includes:
   # - signal (dBm)
   # - rx/tx bitrate
   # - rx/tx packets
   # - retries
   # - failed packets
   
   # Monitor in real-time
   wavemon  # If installed

Troubleshooting
===============

Common Issues
-------------

.. code-block:: bash

   # Check if interface exists
   ip link show wlan0
   iw dev
   
   # Check driver
   lspci -k | grep -A 3 -i network
   lsusb | grep -i wireless
   
   # Check kernel module
   lsmod | grep -i wifi
   lsmod | grep -i 80211
   
   # Reload driver
   modprobe -r iwlwifi
   modprobe iwlwifi
   
   # Check rfkill
   rfkill list
   rfkill unblock wifi
   rfkill unblock all
   
   # Check interface state
   ip link set wlan0 up
   
   # Reset interface
   ip link set wlan0 down
   ip link set wlan0 up
   
   # Restart NetworkManager
   systemctl restart NetworkManager
   
   # Restart wpa_supplicant
   killall wpa_supplicant
   wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf

Debug Logging
-------------

.. code-block:: bash

   # wpa_supplicant debug
   wpa_supplicant -dd -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
   
   # iw event monitoring
   iw event
   
   # NetworkManager debug
   nmcli general logging level DEBUG
   journalctl -u NetworkManager -f
   
   # Kernel messages
   dmesg | grep -i wifi
   dmesg | grep -i wlan
   
   # System log
   journalctl -b | grep -i wifi

Advanced Configuration
======================

Power Management
----------------

.. code-block:: bash

   # Disable power save
   iw dev wlan0 set power_save off
   
   # Enable power save
   iw dev wlan0 set power_save on
   
   # Check power save status
   iw dev wlan0 get power_save
   
   # Persistent (in /etc/NetworkManager/conf.d/wifi-powersave.conf)
   [connection]
   wifi.powersave = 2  # 0=default, 1=ignore, 2=disable, 3=enable

Multiple Networks
-----------------

.. code-block:: bash

   # wpa_supplicant with priorities
   network={
       ssid="HomeNetwork"
       psk="password1"
       priority=10
   }
   
   network={
       ssid="WorkNetwork"
       psk="password2"
       priority=5
   }
   
   # Higher priority connects first

Best Practices
==============

1. **Use WPA2** or WPA3 encryption
2. **Disable WPS** for security
3. **Hide SSID** for additional security
4. **Use strong passwords** (12+ characters)
5. **Monitor signal strength**
6. **Update firmware** regularly
7. **Use 5GHz** when available
8. **Avoid channel congestion**
9. **Enable power save** for laptops
10. **Use MAC filtering** for APs

Common Pitfalls
===============

1. **Wrong password** syntax in configs
2. **Interface not up** before connecting
3. **Multiple network managers** conflicting
4. **Driver not loaded**
5. **rfkill blocking** WiFi
6. **Wrong channel** for region

Performance Tips
================

.. code-block:: bash

   # Choose less congested channel
   iw dev wlan0 survey dump
   
   # Prefer 5GHz over 2.4GHz
   nmcli con mod "MyWiFi" 802-11-wireless.band a
   
   # Set specific BSSID
   nmcli con mod "MyWiFi" 802-11-wireless.bssid XX:XX:XX:XX:XX:XX
   
   # Disable IPv6 if not needed
   nmcli con mod "MyWiFi" ipv6.method ignore

See Also
========

- Linux_Network_Configuration.rst
- Linux_Network_Tools.rst
- Linux_Network_Performance.rst

References
==========

- man iw
- man wpa_supplicant
- man hostapd
- man nmcli
