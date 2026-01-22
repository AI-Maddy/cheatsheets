=======================================
OpenBMC Quick Reference Guide
=======================================

:Author: Technical Documentation
:Date: January 2026
:Version: 2.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 3
   :local:
   :backlinks: top

📋 TL;DR - Quick Start
======================

**What is OpenBMC?**
Open-source Linux distribution for Baseboard Management Controllers (BMCs) - the tiny computers that remotely manage servers.

**Quick Access:**

.. code-block:: bash

   # Access via Web UI
   https://bmc-ip-address
   
   # Via Redfish API
   curl -k -u admin:password https://bmc-ip/redfish/v1/Systems/system
   
   # Via IPMI
   ipmitool -I lanplus -H bmc-ip -U admin -P password power status
   
   # SSH Access
   ssh root@bmc-ip

**Common Operations:**

+-----------------------+------------------------------------------+
| **Operation**         | **Command**                              |
+=======================+==========================================+
| Power on server       | ``ipmitool power on``                    |
+-----------------------+------------------------------------------+
| Power off server      | ``ipmitool power off``                   |
+-----------------------+------------------------------------------+
| Check sensors         | ``ipmitool sensor list``                 |
+-----------------------+------------------------------------------+
| View event log        | ``ipmitool sel list``                    |
+-----------------------+------------------------------------------+
| Access console        | ``ipmitool sol activate``                |
+-----------------------+------------------------------------------+

🔧 IPMI Commands Reference
===========================

Power Management
----------------

.. code-block:: bash

   # Check power status
   ipmitool -I lanplus -H <bmc-ip> -U <user> -P <pass> power status
   
   # Power on
   ipmitool power on
   
   # Power off (graceful)
   ipmitool power soft
   
   # Power off (hard/forced)
   ipmitool power off
   
   # Power cycle
   ipmitool power cycle
   
   # Reset server
   ipmitool power reset
   
   # Power diag (diagnostic interrupt)
   ipmitool power diag

Sensor Monitoring
-----------------

.. code-block:: bash

   # List all sensors
   ipmitool sensor list
   
   # Specific sensor type
   ipmitool sensor list | grep -i temp
   ipmitool sensor list | grep -i fan
   ipmitool sensor list | grep -i voltage
   
   # Get sensor reading
   ipmitool sensor get "CPU0 Temp"
   
   # Set sensor thresholds
   ipmitool sensor thresh "CPU0 Temp" upper 80 85 90
   
   # SDR (Sensor Data Record) info
   ipmitool sdr list
   ipmitool sdr type temperature
   ipmitool sdr type fan

System Event Log (SEL)
----------------------

.. code-block:: bash

   # View all events
   ipmitool sel list
   
   # View last 10 events
   ipmitool sel list last 10
   
   # View events with timestamps
   ipmitool sel elist
   
   # Get SEL info (used space, etc.)
   ipmitool sel info
   
   # Clear event log (requires confirmation)
   ipmitool sel clear
   
   # Save log to file
   ipmitool sel save sel_log_$(date +%Y%m%d).txt
   
   # Watch for new events (live monitoring)
   watch -n 5 'ipmitool sel elist | tail -20'

Serial Over LAN (SOL)
---------------------

.. code-block:: bash

   # Activate serial console
   ipmitool -I lanplus -H <bmc-ip> -U admin -P password sol activate
   
   # Deactivate (type this during active session)
   ~.
   
   # Check SOL configuration
   ipmitool sol info
   
   # Set SOL parameters
   ipmitool sol set enabled true
   ipmitool sol set privilege-level admin
   ipmitool sol set force-encryption true
   
   # Deactivate SOL (from another terminal)
   ipmitool sol deactivate

FRU (Field Replaceable Unit) Information
-----------------------------------------

.. code-block:: bash

   # List all FRU
   ipmitool fru list
   
   # Print detailed FRU info
   ipmitool fru print
   
   # Print specific FRU ID
   ipmitool fru print 0
   
   # Edit FRU data
   ipmitool fru edit 0 field b 1 "My Custom Board"

LAN Configuration
-----------------

.. code-block:: bash

   # Show LAN configuration
   ipmitool lan print
   ipmitool lan print 1  # Channel 1
   
   # Set static IP
   ipmitool lan set 1 ipsrc static
   ipmitool lan set 1 ipaddr 192.168.1.100
   ipmitool lan set 1 netmask 255.255.255.0
   ipmitool lan set 1 defgw ipaddr 192.168.1.1
   
   # Set to DHCP
   ipmitool lan set 1 ipsrc dhcp
   
   # Set VLAN
   ipmitool lan set 1 vlan id 100
   ipmitool lan set 1 vlan priority 0
   
   # View MAC address
   ipmitool lan print 1 | grep "MAC Address"

User Management
---------------

.. code-block:: bash

   # List users
   ipmitool user list 1
   
   # Set user password
   ipmitool user set password 2 newpassword
   
   # Enable/disable user
   ipmitool user enable 2
   ipmitool user disable 2
   
   # Set user privilege (1=callback, 2=user, 3=operator, 4=admin)
   ipmitool user priv 2 4 1
   
   # Create new user
   ipmitool user set name 3 johndoe
   ipmitool user set password 3 secretpass
   ipmitool user enable 3

Chassis Commands
----------------

.. code-block:: bash

   # Chassis status
   ipmitool chassis status
   
   # Chassis power policy
   ipmitool chassis policy list
   ipmitool chassis policy always-on
   ipmitool chassis policy previous
   ipmitool chassis policy always-off
   
   # Identify LED control
   ipmitool chassis identify       # Blink indefinitely
   ipmitool chassis identify 10    # Blink for 10 seconds
   ipmitool chassis identify 0     # Turn off identify LED
   
   # Chassis restart
   ipmitool chassis restart_cause
   
   # Boot device selection
   ipmitool chassis bootdev pxe
   ipmitool chassis bootdev disk
   ipmitool chassis bootdev cdrom
   ipmitool chassis bootdev bios
   
   # Boot options
   ipmitool chassis bootparam get 5

BMC Management
--------------

.. code-block:: bash

   # BMC info
   ipmitool bmc info
   ipmitool mc info
   
   # BMC reset (cold reset)
   ipmitool mc reset cold
   
   # BMC reset (warm reset)
   ipmitool mc reset warm
   
   # GUID
   ipmitool mc guid
   
   # Watchdog status
   ipmitool mc watchdog get
   ipmitool mc watchdog off
   
   # Self-test
   ipmitool mc selftest

Raw Commands
------------

.. code-block:: bash

   # Send raw IPMI command (example: get device ID)
   ipmitool raw 0x06 0x01
   
   # Get BMC cold reset cause
   ipmitool raw 0x06 0x02

📡 Redfish API Reference
=========================

Authentication
--------------

**Session-Based Authentication:**

.. code-block:: bash

   # Create session
   curl -k -H "Content-Type: application/json" -X POST \
     https://<bmc-ip>/redfish/v1/SessionService/Sessions \
     -d '{"UserName":"admin", "Password":"password"}' \
     -i
   
   # Extract X-Auth-Token from response headers
   # Use token in subsequent requests:
   curl -k -H "X-Auth-Token: <token>" \
     https://<bmc-ip>/redfish/v1/Systems/system

**Basic Authentication:**

.. code-block:: bash

   curl -k -u admin:password https://<bmc-ip>/redfish/v1/Systems/system

Service Root
------------

.. code-block:: bash

   # Get Redfish service root
   curl -k https://<bmc-ip>/redfish/v1
   
   # Get supported versions
   curl -k https://<bmc-ip>/redfish

System Information
------------------

.. code-block:: bash

   # Get system collection
   curl -k -u admin:password https://<bmc-ip>/redfish/v1/Systems
   
   # Get specific system
   curl -k -u admin:password https://<bmc-ip>/redfish/v1/Systems/system
   
   # Get system details (pretty print)
   curl -k -u admin:password https://<bmc-ip>/redfish/v1/Systems/system | jq .
   
   # Get processor info
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/Processors
   
   # Get memory info
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/Memory
   
   # Get storage info
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/Storage

Power Control
-------------

.. code-block:: bash

   # Get power state
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system | jq .PowerState
   
   # Power on
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ResetType": "On"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
   
   # Power off (graceful)
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ResetType": "GracefulShutdown"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
   
   # Power off (forced)
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ResetType": "ForceOff"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
   
   # Power cycle
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ResetType": "ForceRestart"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/Actions/ComputerSystem.Reset
   
   # Graceful restart
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ResetType": "GracefulRestart"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/Actions/ComputerSystem.Reset

**Reset Types:**

+----------------------+------------------------------------------+
| **ResetType**        | **Description**                          |
+======================+==========================================+
| On                   | Power on the system                      |
+----------------------+------------------------------------------+
| ForceOff             | Immediate power off (hard)               |
+----------------------+------------------------------------------+
| GracefulShutdown     | OS-aware shutdown                        |
+----------------------+------------------------------------------+
| ForceRestart         | Hard reboot                              |
+----------------------+------------------------------------------+
| GracefulRestart      | OS-aware restart                         |
+----------------------+------------------------------------------+
| Nmi                  | Send NMI (diagnostic interrupt)          |
+----------------------+------------------------------------------+

Sensors & Thermal
-----------------

.. code-block:: bash

   # Get chassis info
   curl -k -u admin:password https://<bmc-ip>/redfish/v1/Chassis/chassis
   
   # Get thermal sensors
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Chassis/chassis/Thermal | jq .
   
   # Get specific temperature sensor
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Chassis/chassis/Thermal | \
     jq '.Temperatures[] | select(.Name=="CPU0 Temp")'
   
   # Get fan speeds
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Chassis/chassis/Thermal | \
     jq .Fans
   
   # Get power consumption
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Chassis/chassis/Power | \
     jq '.PowerControl[0].PowerConsumedWatts'

Event Logs
----------

.. code-block:: bash

   # Get log service
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/LogServices
   
   # Get event log entries
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/LogServices/EventLog/Entries
   
   # Get specific log entry
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/LogServices/EventLog/Entries/1
   
   # Clear event log
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"Action": "LogService.ClearLog"}' \
     https://<bmc-ip>/redfish/v1/Systems/system/LogServices/EventLog/Actions/LogService.ClearLog

Firmware Update
---------------

.. code-block:: bash

   # Get update service
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/UpdateService
   
   # Get firmware inventory
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/UpdateService/FirmwareInventory
   
   # Upload firmware (multipart form)
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/octet-stream" \
     --data-binary @firmware.bin \
     https://<bmc-ip>/redfish/v1/UpdateService
   
   # Simple update (via URI)
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"ImageURI":"http://fileserver/firmware.bin"}' \
     https://<bmc-ip>/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate

Account Management
------------------

.. code-block:: bash

   # List accounts
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/AccountService/Accounts
   
   # Get specific account
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/AccountService/Accounts/admin
   
   # Create account
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{"UserName":"newuser","Password":"newpass","RoleId":"Operator"}' \
     https://<bmc-ip>/redfish/v1/AccountService/Accounts
   
   # Modify account
   curl -k -u admin:password -X PATCH \
     -H "Content-Type: application/json" \
     -d '{"Password":"newpassword"}' \
     https://<bmc-ip>/redfish/v1/AccountService/Accounts/newuser
   
   # Delete account
   curl -k -u admin:password -X DELETE \
     https://<bmc-ip>/redfish/v1/AccountService/Accounts/newuser

Virtual Media
-------------

.. code-block:: bash

   # Get virtual media collection
   curl -k -u admin:password \
     https://<bmc-ip>/redfish/v1/Systems/system/VirtualMedia
   
   # Mount ISO image
   curl -k -u admin:password -X POST \
     -H "Content-Type: application/json" \
     -d '{
       "Image": "http://fileserver/ubuntu.iso",
       "Inserted": true,
       "WriteProtected": true
     }' \
     https://<bmc-ip>/redfish/v1/Systems/system/VirtualMedia/1/Actions/VirtualMedia.InsertMedia
   
   # Eject media
   curl -k -u admin:password -X POST \
     https://<bmc-ip>/redfish/v1/Systems/system/VirtualMedia/1/Actions/VirtualMedia.EjectMedia

🐍 Python Redfish Library
===========================

Installation
------------

.. code-block:: bash

   pip install redfish

Basic Usage
-----------

.. code-block:: python

   import redfish
   
   # Create client
   REDFISH_OBJ = redfish.redfish_client(
       base_url="https://192.168.1.100",
       username="admin",
       password="password",
       default_prefix="/redfish/v1"
   )
   
   # Login
   REDFISH_OBJ.login(auth="session")
   
   # Get system info
   response = REDFISH_OBJ.get("/redfish/v1/Systems/system")
   print(response.dict)
   
   # Logout
   REDFISH_OBJ.logout()

Power Control Script
--------------------

.. code-block:: python

   #!/usr/bin/env python3
   import redfish
   import sys
   
   BMC_IP = "192.168.1.100"
   USERNAME = "admin"
   PASSWORD = "password"
   
   def power_control(action):
       """Control server power"""
       reset_types = {
           'on': 'On',
           'off': 'ForceOff',
           'graceful_off': 'GracefulShutdown',
           'reset': 'ForceRestart',
           'graceful_reset': 'GracefulRestart'
       }
       
       if action not in reset_types:
           print(f"Invalid action. Use: {', '.join(reset_types.keys())}")
           return 1
       
       # Connect
       client = redfish.redfish_client(
           base_url=f"https://{BMC_IP}",
           username=USERNAME,
           password=PASSWORD
       )
       client.login(auth="session")
       
       # Get current power state
       response = client.get("/redfish/v1/Systems/system")
       current_state = response.dict["PowerState"]
       print(f"Current state: {current_state}")
       
       # Send reset command
       body = {"ResetType": reset_types[action]}
       client.post(
           "/redfish/v1/Systems/system/Actions/ComputerSystem.Reset",
           body=body
       )
       print(f"Action '{action}' sent successfully")
       
       client.logout()
       return 0
   
   if __name__ == "__main__":
       if len(sys.argv) != 2:
           print("Usage: power_control.py <on|off|graceful_off|reset|graceful_reset>")
           sys.exit(1)
       sys.exit(power_control(sys.argv[1]))

Sensor Monitoring Script
-------------------------

.. code-block:: python

   #!/usr/bin/env python3
   import redfish
   import time
   
   def monitor_sensors(bmc_ip, username, password, interval=5):
       """Monitor temperature and fan sensors"""
       client = redfish.redfish_client(
           base_url=f"https://{bmc_ip}",
           username=username,
           password=password
       )
       client.login(auth="session")
       
       try:
           while True:
               # Get thermal data
               response = client.get("/redfish/v1/Chassis/chassis/Thermal")
               thermal_data = response.dict
               
               # Print temperatures
               print("\n" + "="*60)
               print("TEMPERATURE SENSORS:")
               for sensor in thermal_data.get("Temperatures", []):
                   name = sensor.get("Name", "Unknown")
                   temp = sensor.get("ReadingCelsius", "N/A")
                   status = sensor.get("Status", {}).get("Health", "Unknown")
                   print(f"  {name:30s} {temp:>6}°C  [{status}]")
               
               # Print fan speeds
               print("\nFAN SPEEDS:")
               for fan in thermal_data.get("Fans", []):
                   name = fan.get("Name", "Unknown")
                   speed = fan.get("Reading", "N/A")
                   units = fan.get("ReadingUnits", "RPM")
                   status = fan.get("Status", {}).get("Health", "Unknown")
                   print(f"  {name:30s} {speed:>6} {units}  [{status}]")
               
               time.sleep(interval)
       
       except KeyboardInterrupt:
           print("\n\nMonitoring stopped.")
       finally:
           client.logout()
   
   if __name__ == "__main__":
       monitor_sensors("192.168.1.100", "admin", "password")

🔐 SSH Commands (On BMC)
=========================

D-Bus Commands
--------------

.. code-block:: bash

   # List all D-Bus services
   busctl list | grep phosphor
   
   # Show D-Bus tree
   busctl tree xyz.openbmc_project.Inventory.Manager
   
   # Get property
   busctl get-property xyz.openbmc_project.Inventory.Manager \
     /xyz/openbmc_project/inventory/system/chassis \
     xyz.openbmc_project.Inventory.Item \
     Present
   
   # Set property (example: LED)
   busctl set-property xyz.openbmc_project.LED.GroupManager \
     /xyz/openbmc_project/led/groups/enclosure_identify \
     xyz.openbmc_project.Led.Group \
     Asserted b true
   
   # Call method (example: power on)
   busctl call xyz.openbmc_project.State.Host \
     /xyz/openbmc_project/state/host0 \
     xyz.openbmc_project.State.Host \
     RequestedHostTransition s \
     xyz.openbmc_project.State.Host.Transition.On

System Information
------------------

.. code-block:: bash

   # BMC version
   cat /etc/os-release
   
   # Kernel version
   uname -a
   
   # Uptime
   uptime
   
   # Memory usage
   free -h
   
   # Disk usage
   df -h
   
   # Running processes
   ps aux | grep phosphor
   
   # Network configuration
   ip addr show
   ifconfig
   
   # Route table
   ip route

Service Management
------------------

.. code-block:: bash

   # List all services
   systemctl list-units --type=service
   
   # Check service status
   systemctl status phosphor-hwmon@.service
   systemctl status bmcweb.service
   
   # Start/stop/restart service
   systemctl start phosphor-fan-monitor@0.service
   systemctl stop phosphor-fan-monitor@0.service
   systemctl restart bmcweb.service
   
   # Enable/disable service at boot
   systemctl enable bmcweb.service
   systemctl disable phosphor-fan-monitor@0.service
   
   # View service logs
   journalctl -u bmcweb.service
   journalctl -u phosphor-hwmon@.service -f  # Follow logs

Log Files
---------

.. code-block:: bash

   # View system journal
   journalctl
   
   # Recent logs
   journalctl -n 100
   
   # Follow logs (live)
   journalctl -f
   
   # Logs for specific unit
   journalctl -u bmcweb
   
   # Logs since boot
   journalctl -b
   
   # Logs with priority (err and above)
   journalctl -p err
   
   # Export logs
   journalctl --since "1 hour ago" > /tmp/bmc_logs.txt

Hardware Monitoring
-------------------

.. code-block:: bash

   # I2C bus scan
   i2cdetect -y 0
   i2cdetect -y 1
   
   # Read I2C device
   i2cdump -y 0 0x50
   
   # GPIO status
   cat /sys/class/gpio/gpio*/value
   
   # Temperature sensors (hwmon)
   cat /sys/class/hwmon/hwmon*/temp*_input
   
   # Fan speeds
   cat /sys/class/hwmon/hwmon*/fan*_input

Network Configuration
---------------------

.. code-block:: bash

   # View network config
   cat /etc/systemd/network/00-bmc-eth0.network
   
   # Restart networking
   systemctl restart systemd-networkd
   
   # Test connectivity
   ping -c 4 google.com
   
   # Check listening ports
   netstat -tuln
   ss -tuln

Firmware Information
--------------------

.. code-block:: bash

   # BMC firmware version
   cat /etc/os-release | grep VERSION
   
   # U-Boot version
   fw_printenv ver
   
   # BIOS/UEFI version (from host)
   busctl get-property xyz.openbmc_project.Software.BMC.Updater \
     /xyz/openbmc_project/software/bios_active \
     xyz.openbmc_project.Software.Version \
     Version

📊 Monitoring & Automation
===========================

Prometheus Exporter
-------------------

.. code-block:: yaml

   # prometheus.yml configuration
   scrape_configs:
     - job_name: 'openbmc'
       static_configs:
         - targets: ['192.168.1.100:443']
       scheme: https
       tls_config:
         insecure_skip_verify: true
       basic_auth:
         username: 'admin'
         password: 'password'
       metrics_path: '/redfish/v1/Chassis/chassis/Thermal'
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance

Ansible Playbook
----------------

.. code-block:: yaml

   ---
   # bmc_power_management.yml
   - name: Manage OpenBMC Power
     hosts: localhost
     gather_facts: no
     vars:
       bmc_ip: "192.168.1.100"
       bmc_user: "admin"
       bmc_pass: "password"
     
     tasks:
       - name: Get power state
         uri:
           url: "https://{{ bmc_ip }}/redfish/v1/Systems/system"
           method: GET
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
         register: power_state
       
       - name: Display power state
         debug:
           msg: "Current power state: {{ power_state.json.PowerState }}"
       
       - name: Power on server if off
         uri:
           url: "https://{{ bmc_ip }}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
           method: POST
           user: "{{ bmc_user }}"
           password: "{{ bmc_pass }}"
           force_basic_auth: yes
           validate_certs: no
           body_format: json
           body:
             ResetType: "On"
           status_code: 204
         when: power_state.json.PowerState == "Off"

Nagios Check Script
-------------------

.. code-block:: bash

   #!/bin/bash
   # check_openbmc_health.sh
   
   BMC_IP="$1"
   USERNAME="$2"
   PASSWORD="$3"
   
   if [ -z "$BMC_IP" ] || [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
       echo "Usage: $0 <bmc-ip> <username> <password>"
       exit 3
   fi
   
   # Get thermal data
   RESPONSE=$(curl -sk -u "${USERNAME}:${PASSWORD}" \
     "https://${BMC_IP}/redfish/v1/Chassis/chassis/Thermal")
   
   # Check for critical temperatures
   CRITICAL=$(echo "$RESPONSE" | jq -r \
     '.Temperatures[] | select(.Status.Health=="Critical") | .Name' | wc -l)
   
   # Check for warning temperatures
   WARNING=$(echo "$RESPONSE" | jq -r \
     '.Temperatures[] | select(.Status.Health=="Warning") | .Name' | wc -l)
   
   if [ "$CRITICAL" -gt 0 ]; then
       echo "CRITICAL - $CRITICAL sensors in critical state"
       exit 2
   elif [ "$WARNING" -gt 0 ]; then
       echo "WARNING - $WARNING sensors in warning state"
       exit 1
   else
       echo "OK - All sensors healthy"
       exit 0
   fi

🛠️ Troubleshooting Commands
=============================

Common Issues
-------------

**Issue: Cannot connect to BMC**

.. code-block:: bash

   # Check network connectivity
   ping <bmc-ip>
   
   # Check if BMC services are running
   nmap -p 443,623 <bmc-ip>
   
   # Verify credentials
   curl -k -u admin:password https://<bmc-ip>/redfish/v1
   
   # Check from BMC console
   ssh root@<bmc-ip>
   systemctl status bmcweb
   ip addr show

**Issue: Sensors not reporting**

.. code-block:: bash

   # On BMC, check hwmon services
   systemctl status phosphor-hwmon@*.service
   
   # Restart hwmon
   systemctl restart 'phosphor-hwmon@*.service'
   
   # Check I2C devices
   i2cdetect -y -r 0
   
   # View sensor D-Bus objects
   busctl tree xyz.openbmc_project.Hwmon

**Issue: Fan control not working**

.. code-block:: bash

   # Check fan service
   systemctl status phosphor-fan-*
   
   # View fan D-Bus properties
   busctl tree xyz.openbmc_project.FanSensor
   
   # Manual fan control (if available)
   echo 100 > /sys/class/hwmon/hwmon0/pwm1

**Issue: Firmware update failed**

.. code-block:: bash

   # Check update service status
   systemctl status xyz.openbmc_project.Software.BMC.Updater.service
   
   # View software inventory
   busctl tree xyz.openbmc_project.Software.BMC.Updater
   
   # Check for errors
   journalctl -u xyz.openbmc_project.Software.BMC.Updater.service -n 100
   
   # Recover from bad update (if serial console available)
   # Boot to recovery mode and reflash

Factory Reset
-------------

.. code-block:: bash

   # Via IPMI
   ipmitool mc reset cold
   
   # Via SSH (on BMC)
   systemctl reboot
   
   # Factory reset (may vary by platform)
   busctl call xyz.openbmc_project.Software.BMC.Updater \
     /xyz/openbmc_project/software \
     xyz.openbmc_project.Common.FactoryReset \
     Reset

Debug Mode
----------

.. code-block:: bash

   # Enable debug logging
   busctl call xyz.openbmc_project.Logging \
     /xyz/openbmc_project/logging \
     xyz.openbmc_project.Logging.Settings \
     SetLogLevel s "xyz.openbmc_project" s "Debug"
   
   # View debug logs
   journalctl -p debug -f

📚 Quick Reference Tables
=========================

IPMI vs Redfish Comparison
---------------------------

+---------------------+-------------------------+--------------------------------------+
| **Operation**       | **IPMI**                | **Redfish**                          |
+=====================+=========================+======================================+
| Power on            | ``ipmitool power on``   | ``POST .../ComputerSystem.Reset``    |
|                     |                         | ``{"ResetType":"On"}``               |
+---------------------+-------------------------+--------------------------------------+
| Sensor list         | ``ipmitool sensor``     | ``GET .../Thermal``                  |
|                     | ``list``                |                                      |
+---------------------+-------------------------+--------------------------------------+
| Event log           | ``ipmitool sel list``   | ``GET .../LogServices/EventLog/``    |
|                     |                         | ``Entries``                          |
+---------------------+-------------------------+--------------------------------------+
| User management     | ``ipmitool user``       | ``GET/POST/PATCH .../Accounts``      |
+---------------------+-------------------------+--------------------------------------+

HTTP Status Codes
-----------------

+-------------+---------------------------+--------------------------------------+
| **Code**    | **Meaning**               | **Typical Cause**                    |
+=============+===========================+======================================+
| 200         | OK                        | Successful GET                       |
+-------------+---------------------------+--------------------------------------+
| 201         | Created                   | Successful POST (resource created)   |
+-------------+---------------------------+--------------------------------------+
| 204         | No Content                | Successful action (no body returned) |
+-------------+---------------------------+--------------------------------------+
| 400         | Bad Request               | Malformed JSON                       |
+-------------+---------------------------+--------------------------------------+
| 401         | Unauthorized              | Invalid credentials                  |
+-------------+---------------------------+--------------------------------------+
| 404         | Not Found                 | Invalid URI                          |
+-------------+---------------------------+--------------------------------------+
| 500         | Internal Server Error     | BMC software error                   |
+-------------+---------------------------+--------------------------------------+

Common D-Bus Interfaces
-----------------------

+-------------------------------------------+----------------------------------+
| **Interface**                             | **Purpose**                      |
+===========================================+==================================+
| xyz.openbmc_project.State.Host            | Host power state                 |
+-------------------------------------------+----------------------------------+
| xyz.openbmc_project.Sensor.Value          | Sensor readings                  |
+-------------------------------------------+----------------------------------+
| xyz.openbmc_project.LED.Physical          | LED control                      |
+-------------------------------------------+----------------------------------+
| xyz.openbmc_project.Control.FanPwm        | Fan speed control                |
+-------------------------------------------+----------------------------------+
| xyz.openbmc_project.Inventory.Item        | Hardware inventory               |
+-------------------------------------------+----------------------------------+
| xyz.openbmc_project.Software.Version      | Firmware versions                |
+-------------------------------------------+----------------------------------+

🔗 Useful Resources
===================

Official Links
--------------

* **Main Repository**: https://github.com/openbmc/openbmc
* **Documentation**: https://github.com/openbmc/docs
* **Web UI (bmcweb)**: https://github.com/openbmc/bmcweb
* **Mailing List**: https://lists.ozlabs.org/listinfo/openbmc
* **Discord**: OpenBMC Community Server

Standard Specifications
-----------------------

* **Redfish**: https://www.dmtf.org/standards/redfish
* **IPMI**: https://www.intel.com/content/www/us/en/products/docs/servers/ipmi/ipmi-home.html
* **PLDM**: https://www.dmtf.org/standards/pmci

Development Resources
---------------------

* **Yocto Project**: https://www.yoctoproject.org/
* **D-Bus**: https://www.freedesktop.org/wiki/Software/dbus/
* **Redfish Python**: https://github.com/DMTF/python-redfish-library

========================================
Last Updated: January 2026
Version: 2.0
========================================
