=====================================
Embedded Linux Connectivity Protocols - Complete Guide
=====================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Reference: Smart Home Hub (i.MX 93), E-Bike Infotainment, Avionics Platform (Intel Atom)

.. contents:: Table of Contents
   :depth: 4
   :local:

====================
1. Overview
====================

Comprehensive guide to connectivity protocols for embedded Linux systems, covering wireless 
(Wi-Fi, Bluetooth, Zigbee, Matter), wired (CAN, Ethernet, AFDX), and network stack implementation.

**Project Context**:

- **Smart Home Hub** (i.MX 93): Wi-Fi, Zigbee, Matter, Thread
- **E-Bike Infotainment**: CAN bus, Bluetooth audio
- **Avionics Platform** (Intel Atom): AFDX (ARINC 664), Ethernet AVB
- **AFIRS SDU**: AFDX dual-redundant network

**Protocols Covered**:

.. code-block:: text

    Wireless:
    - Wi-Fi (802.11a/b/g/n/ac/ax)
    - Bluetooth (Classic, BLE 5.x)
    - Zigbee (IEEE 802.15.4)
    - Thread (6LoWPAN)
    - Matter (application layer)
    
    Wired:
    - CAN / CAN-FD
    - AFDX (ARINC 664 Part 7)
    - Ethernet (Switch, VLAN, QoS)
    - Ethernet AVB/TSN

====================
2. Wi-Fi (802.11)
====================

2.1 Wi-Fi Stack Architecture
-----------------------------

**Linux Wireless Stack**:

.. code-block:: text

    ┌───────────────────────────────────────┐
    │      User Space Applications          │
    │  (wpa_supplicant, NetworkManager)     │
    └────────────────┬──────────────────────┘
                     │ nl80211 (netlink)
    ┌────────────────▼──────────────────────┐
    │          cfg80211 (kernel)            │
    │  (Configuration, scan, auth)          │
    └────────────────┬──────────────────────┘
                     │
    ┌────────────────▼──────────────────────┐
    │          mac80211 (kernel)            │
    │  (802.11 MAC layer, crypto)           │
    └────────────────┬──────────────────────┘
                     │
    ┌────────────────▼──────────────────────┐
    │      Hardware Driver (e.g., ath10k)   │
    └────────────────┬──────────────────────┘
                     │
    ┌────────────────▼──────────────────────┐
    │           Wi-Fi Hardware              │
    └───────────────────────────────────────┘

2.2 Wi-Fi Configuration (wpa_supplicant)
-----------------------------------------

**WPA2-PSK Configuration**:

.. code-block:: text

    # /etc/wpa_supplicant/wpa_supplicant.conf
    
    ctrl_interface=/var/run/wpa_supplicant
    ctrl_interface_group=netdev
    update_config=1
    country=US
    
    network={
        ssid="SmartHome"
        psk="secure_password_here"
        key_mgmt=WPA-PSK
        proto=RSN
        pairwise=CCMP
        group=CCMP
    }

**WPA3-SAE (Enhanced Security)**:

.. code-block:: text

    network={
        ssid="SmartHome_5G"
        sae_password="very_secure_password"
        key_mgmt=SAE
        ieee80211w=2  # Require PMF (Protected Management Frames)
    }

**Enterprise WPA2 (802.1X)**:

.. code-block:: text

    network={
        ssid="Corporate_Network"
        key_mgmt=WPA-EAP
        eap=PEAP
        identity="user@example.com"
        password="user_password"
        phase2="auth=MSCHAPV2"
        ca_cert="/etc/ssl/certs/ca.pem"
    }

**Start wpa_supplicant**:

.. code-block:: bash

    # Manual start
    wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
    
    # Get IP address
    dhclient wlan0
    
    # Or use systemd service
    systemctl enable wpa_supplicant@wlan0
    systemctl start wpa_supplicant@wlan0

2.3 Wi-Fi Direct (P2P)
----------------------

**P2P Configuration**:

.. code-block:: bash

    # Enable P2P on interface
    wpa_cli -i wlan0 p2p_find
    
    # Show discovered peers
    wpa_cli -i wlan0 p2p_peers
    
    # Connect to peer
    wpa_cli -i wlan0 p2p_connect <peer_mac> pbc
    
    # Create P2P group (GO - Group Owner)
    wpa_cli -i wlan0 p2p_group_add

**P2P Client Example** (Smart Home Hub):

.. code-block:: c

    #include <wpa_ctrl.h>
    
    struct wpa_ctrl *ctrl;
    
    int wifi_p2p_connect(const char *peer_mac)
    {
        char cmd[256], reply[4096];
        size_t reply_len = sizeof(reply);
        
        /* Connect to wpa_supplicant control interface */
        ctrl = wpa_ctrl_open("/var/run/wpa_supplicant/wlan0");
        if (!ctrl)
            return -1;
        
        /* Start P2P find */
        wpa_ctrl_request(ctrl, "P2P_FIND", 8, reply, &reply_len, NULL);
        sleep(5);
        
        /* Connect using PBC (Push Button Configuration) */
        snprintf(cmd, sizeof(cmd), "P2P_CONNECT %s pbc", peer_mac);
        reply_len = sizeof(reply);
        wpa_ctrl_request(ctrl, cmd, strlen(cmd), reply, &reply_len, NULL);
        
        wpa_ctrl_close(ctrl);
        return 0;
    }

2.4 Wi-Fi Power Management
---------------------------

**Enable Power Save Mode**:

.. code-block:: bash

    # Check current power save state
    iw dev wlan0 get power_save
    
    # Enable power save
    iw dev wlan0 set power_save on
    
    # Driver-specific tuning (iwlwifi example)
    echo 5 > /sys/module/iwlwifi/parameters/power_level  # 1-5, 5=most aggressive

**802.11 Power Save Parameters**:

.. code-block:: c

    /* Set PS mode via nl80211 */
    #include <netlink/genl/genl.h>
    #include <netlink/genl/ctrl.h>
    #include <linux/nl80211.h>
    
    int set_power_save(const char *ifname, bool enable)
    {
        struct nl_sock *sock;
        struct nl_msg *msg;
        int ifindex, ret;
        
        sock = nl_socket_alloc();
        genl_connect(sock);
        
        ifindex = if_nametoindex(ifname);
        
        msg = nlmsg_alloc();
        genlmsg_put(msg, 0, 0, genl_ctrl_resolve(sock, "nl80211"), 0,
                   0, NL80211_CMD_SET_POWER_SAVE, 0);
        
        nla_put_u32(msg, NL80211_ATTR_IFINDEX, ifindex);
        nla_put_u32(msg, NL80211_ATTR_PS_STATE,
                   enable ? NL80211_PS_ENABLED : NL80211_PS_DISABLED);
        
        ret = nl_send_auto(sock, msg);
        nlmsg_free(msg);
        nl_socket_free(sock);
        
        return ret;
    }

**Project Results** (Smart Home Hub):

.. code-block:: text

    Wi-Fi Power Consumption:
    - Active (no PS): 280mW average
    - Power Save enabled: 95mW average (66% reduction)
    - Listen interval: 3 beacon intervals (307ms)
    - Wake-up latency: <10ms
    
    Throughput Impact:
    - No PS: 85 Mbps TCP
    - PS enabled: 78 Mbps TCP (8% reduction)

2.5 Hotspot / Access Point Mode
--------------------------------

**hostapd Configuration**:

.. code-block:: text

    # /etc/hostapd/hostapd.conf
    
    interface=wlan0
    driver=nl80211
    
    # Network configuration
    ssid=SmartHomeHub
    hw_mode=g
    channel=6
    country_code=US
    
    # Security
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=CCMP
    wpa_passphrase=secure_ap_password
    
    # 802.11n
    ieee80211n=1
    ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
    
    # 802.11ac (5 GHz)
    # hw_mode=a
    # channel=36
    # ieee80211ac=1
    # vht_oper_chwidth=1
    # vht_oper_centr_freq_seg0_idx=42

**Start Access Point**:

.. code-block:: bash

    # Configure IP address
    ip addr add 192.168.50.1/24 dev wlan0
    ip link set wlan0 up
    
    # Start hostapd
    hostapd /etc/hostapd/hostapd.conf &
    
    # Start DHCP server
    dnsmasq --interface=wlan0 --dhcp-range=192.168.50.10,192.168.50.100,12h

====================
3. Bluetooth
====================

3.1 Bluetooth Stack (BlueZ)
----------------------------

**Architecture**:

.. code-block:: text

    ┌───────────────────────────────────────┐
    │      Applications                     │
    │  (bluetoothctl, custom apps)          │
    └────────────────┬──────────────────────┘
                     │ D-Bus
    ┌────────────────▼──────────────────────┐
    │          bluetoothd (daemon)          │
    │  (Device management, pairing, SDP)    │
    └────────────────┬──────────────────────┘
                     │ Sockets (HCI, L2CAP, RFCOMM)
    ┌────────────────▼──────────────────────┐
    │       BlueZ Kernel (HCI, L2CAP)       │
    └────────────────┬──────────────────────┘
                     │ HCI UART/USB
    ┌────────────────▼──────────────────────┐
    │       Bluetooth Controller            │
    └───────────────────────────────────────┘

3.2 BlueZ Configuration
-----------------------

**Enable Bluetooth**:

.. code-block:: bash

    # Start BlueZ daemon
    systemctl start bluetooth
    
    # Check status
    hciconfig -a
    
    # hci0:   Type: Primary  Bus: UART
    #         BD Address: AA:BB:CC:DD:EE:FF  ACL MTU: 1021:8  SCO MTU: 64:1
    #         UP RUNNING
    #         RX bytes:1234 acl:0 sco:0 events:56 errors:0
    #         TX bytes:789 acl:0 sco:0 commands:45 errors:0
    
    # Power on
    hciconfig hci0 up
    
    # Or using bluetoothctl
    bluetoothctl
    [bluetooth]# power on
    [bluetooth]# agent on
    [bluetooth]# default-agent

3.3 Bluetooth Classic (A2DP Audio)
----------------------------------

**Pairing and Connection**:

.. code-block:: bash

    bluetoothctl
    
    # Scan for devices
    [bluetooth]# scan on
    
    # Pair with device
    [bluetooth]# pair AA:BB:CC:DD:EE:FF
    
    # Trust device
    [bluetooth]# trust AA:BB:CC:DD:EE:FF
    
    # Connect
    [bluetooth]# connect AA:BB:CC:DD:EE:FF

**A2DP Audio Sink (E-Bike Infotainment)**:

.. code-block:: text

    # /etc/bluetooth/main.conf
    
    [General]
    Name = E-Bike Audio
    Class = 0x200414  # Audio Sink
    DiscoverableTimeout = 0
    
    [Policy]
    AutoEnable=true

**PulseAudio Integration**:

.. code-block:: bash

    # Load Bluetooth modules
    pactl load-module module-bluetooth-discover
    pactl load-module module-bluetooth-policy
    
    # Set Bluetooth as default sink
    pactl set-default-sink bluez_sink.AA_BB_CC_DD_EE_FF.a2dp_sink
    
    # Test audio
    aplay -D bluez_sink.AA_BB_CC_DD_EE_FF.a2dp_sink test.wav

**A2DP Source (Stream from device)**:

.. code-block:: bash

    # Configure device as A2DP source
    pactl load-module module-loopback \
        source=bluez_source.AA_BB_CC_DD_EE_FF.a2dp_source \
        sink=alsa_output.platform

3.4 Bluetooth Low Energy (BLE)
-------------------------------

**GATT Server** (Heart Rate Service Example):

.. code-block:: python

    #!/usr/bin/env python3
    import dbus
    import dbus.mainloop.glib
    from gi.repository import GLib
    
    GATT_SERVICE_IFACE = 'org.bluez.GattService1'
    GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
    
    class HeartRateService(dbus.service.Object):
        PATH = '/org/bluez/example/service0'
        UUID = '0000180d-0000-1000-8000-00805f9b34fb'  # Heart Rate Service
        
        def __init__(self, bus, index):
            self.path = self.PATH + str(index)
            dbus.service.Object.__init__(self, bus, self.path)
            
        @dbus.service.method(dbus.PROPERTIES_IFACE,
                           in_signature='s',
                           out_signature='a{sv}')
        def GetAll(self, interface):
            if interface != GATT_SERVICE_IFACE:
                raise InvalidArgsException()
            
            return {
                'UUID': self.UUID,
                'Primary': True,
            }
    
    class HeartRateMeasurementCharacteristic(dbus.service.Object):
        UUID = '00002a37-0000-1000-8000-00805f9b34fb'  # Heart Rate Measurement
        
        def __init__(self, bus, index, service):
            self.path = service.path + '/char' + str(index)
            self.service = service
            self.notifying = False
            dbus.service.Object.__init__(self, bus, self.path)
        
        @dbus.service.method(dbus.PROPERTIES_IFACE,
                           in_signature='s',
                           out_signature='a{sv}')
        def GetAll(self, interface):
            if interface != GATT_CHRC_IFACE:
                raise InvalidArgsException()
            
            return {
                'UUID': self.UUID,
                'Service': self.service.path,
                'Flags': ['notify', 'read'],
            }
        
        @dbus.service.method(GATT_CHRC_IFACE,
                           in_signature='a{sv}',
                           out_signature='ay')
        def ReadValue(self, options):
            # Return heart rate value (BPM)
            return dbus.Array([dbus.Byte(0), dbus.Byte(75)], signature='y')
        
        @dbus.service.method(GATT_CHRC_IFACE)
        def StartNotify(self):
            if self.notifying:
                return
            self.notifying = True
            # Start sending notifications
        
        @dbus.service.method(GATT_CHRC_IFACE)
        def StopNotify(self):
            self.notifying = False

**BLE Advertisement**:

.. code-block:: python

    class HeartRateAdvertisement(dbus.service.Object):
        def __init__(self, bus, index):
            self.path = '/org/bluez/example/advertisement' + str(index)
            self.type = 'peripheral'
            self.service_uuids = ['0000180d-0000-1000-8000-00805f9b34fb']
            self.local_name = 'HeartRate Sensor'
            self.include_tx_power = True
            dbus.service.Object.__init__(self, bus, self.path)

**BLE Scanner** (Central Role):

.. code-block:: bash

    # Scan for BLE devices
    hcitool lescan
    
    # Or using bluetoothctl
    bluetoothctl
    [bluetooth]# scan on
    [bluetooth]# devices
    
    # Connect to BLE device
    gatttool -b AA:BB:CC:DD:EE:FF -I
    [AA:BB:CC:DD:EE:FF][LE]> connect
    [AA:BB:CC:DD:EE:FF][LE]> primary  # List services
    [AA:BB:CC:DD:EE:FF][LE]> characteristics  # List characteristics
    [AA:BB:CC:DD:EE:FF][LE]> char-read-hnd 0x0010  # Read characteristic

3.5 Bluetooth Mesh
------------------

**Mesh Provisioning** (Smart Home Hub):

.. code-block:: bash

    # Start mesh-cfgclient
    mesh-cfgclient
    
    # Create network
    [mesh-cfgclient]# create
    
    # Provision new node
    [mesh-cfgclient]# provision <UUID>
    
    # Configure node
    [mesh-cfgclient]# menu config
    [mesh-cfgclient/config]# target 0001
    [mesh-cfgclient/config]# appkey-add 0 0  # Add application key

====================
4. Zigbee & Thread
====================

4.1 Zigbee Stack (Zigbee2MQTT)
-------------------------------

**Architecture**:

.. code-block:: text

    ┌───────────────────────────────────────┐
    │         Home Assistant / MQTT         │
    └────────────────┬──────────────────────┘
                     │ MQTT
    ┌────────────────▼──────────────────────┐
    │          Zigbee2MQTT (Node.js)        │
    │  (Device management, MQTT bridge)     │
    └────────────────┬──────────────────────┘
                     │ Serial
    ┌────────────────▼──────────────────────┐
    │      Zigbee Coordinator               │
    │  (Texas Instruments CC2652, etc.)     │
    └────────────────┬──────────────────────┘
                     │ 802.15.4 (2.4 GHz)
    ┌────────────────▼──────────────────────┐
    │         Zigbee End Devices            │
    │  (Sensors, lights, switches)          │
    └───────────────────────────────────────┘

**Zigbee2MQTT Configuration**:

.. code-block:: yaml

    # /opt/zigbee2mqtt/data/configuration.yaml
    
    homeassistant: true
    
    permit_join: false  # Allow new devices to join
    
    mqtt:
      base_topic: zigbee2mqtt
      server: mqtt://localhost:1883
      user: mqtt_user
      password: mqtt_password
    
    serial:
      port: /dev/ttyUSB0
      adapter: zstack  # TI CC2652
    
    advanced:
      log_level: info
      pan_id: 0x1a62
      ext_pan_id: [0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD]
      channel: 11
      network_key: [1, 3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 13]

**Device Pairing**:

.. code-block:: bash

    # Allow devices to join
    mosquitto_pub -t 'zigbee2mqtt/bridge/request/permit_join' -m '{"value": true}'
    
    # Put device in pairing mode (device-specific)
    # Monitor for new devices
    mosquitto_sub -t 'zigbee2mqtt/#'

**Control Devices**:

.. code-block:: bash

    # Turn on light
    mosquitto_pub -t 'zigbee2mqtt/living_room_light/set' -m '{"state": "ON"}'
    
    # Set brightness
    mosquitto_pub -t 'zigbee2mqtt/living_room_light/set' \
        -m '{"state": "ON", "brightness": 128}'
    
    # Read sensor
    mosquitto_sub -t 'zigbee2mqtt/temperature_sensor'
    # {"temperature": 22.5, "humidity": 45, "battery": 95}

4.2 Thread / OpenThread
------------------------

**OpenThread Border Router** (Smart Home Hub):

.. code-block:: bash

    # Install OpenThread Border Router
    git clone https://github.com/openthread/ot-br-posix
    cd ot-br-posix
    ./script/bootstrap
    ./script/setup
    
    # Configure
    sudo ot-ctl dataset init new
    sudo ot-ctl dataset commit active
    sudo ot-ctl ifconfig up
    sudo ot-ctl thread start

**Thread Network Configuration**:

.. code-block:: bash

    # Get network credentials
    sudo ot-ctl dataset active -x
    # 0e080000000000010000000300000f...
    
    # Commission new device
    sudo ot-ctl commissioner start
    sudo ot-ctl commissioner joiner add * J01NME  # Joiner credential

**Project Implementation** (Smart Home Hub):

.. code-block:: text

    Network Topology:
    ┌────────────────────────────────────────┐
    │         i.MX 93 (Border Router)        │
    │  ┌──────────┐         ┌────────────┐  │
    │  │  Linux   │◄───────►│  Thread   │  │
    │  │  (Wi-Fi) │         │  Radio    │  │
    │  └──────────┘         └────────────┘  │
    └─────────────────┬──────────────────────┘
                      │ Thread (802.15.4)
         ┌────────────┼────────────┐
         │            │            │
    ┌────▼───┐   ┌───▼────┐  ┌───▼────┐
    │ Sensor │   │ Switch │  │  Bulb  │
    │  Node  │   │  Node  │  │  Node  │
    └────────┘   └────────┘  └────────┘

====================
5. Matter Protocol
====================

5.1 Matter Overview
-------------------

**Architecture**:

.. code-block:: text

    Application Layer: Matter Data Model (Clusters, Attributes, Commands)
                    ↓
    Interaction Model: Read, Write, Subscribe, Invoke
                    ↓
    Security: CASE (Certificate Authenticated Session Establishment)
                    ↓
    Transport: UDP, TCP, BLE
                    ↓
    Network: Wi-Fi, Thread, Ethernet

**Matter Device Types**:

.. code-block:: text

    - On/Off Light (0x0100)
    - Dimmable Light (0x0101)
    - Color Temperature Light (0x010C)
    - Door Lock (0x000A)
    - Temperature Sensor (0x0302)
    - Thermostat (0x0301)

5.2 Matter SDK Integration
---------------------------

**Build Matter SDK**:

.. code-block:: bash

    # Clone Matter SDK
    git clone --recurse-submodules https://github.com/project-chip/connectedhomeip.git
    cd connectedhomeip
    
    # Bootstrap
    source scripts/bootstrap.sh
    source scripts/activate.sh
    
    # Build lighting-app example
    cd examples/lighting-app/linux
    gn gen out/debug
    ninja -C out/debug

**Commission Matter Device**:

.. code-block:: bash

    # Start chip-tool (Matter controller)
    ./chip-tool pairing code 1 MT:Y.K9042C00KA0648G00  # QR code payload
    
    # Control device
    ./chip-tool onoff on 1 1      # Turn on endpoint 1
    ./chip-tool onoff off 1 1     # Turn off
    
    # Read attribute
    ./chip-tool onoff read on-off 1 1

**Matter Device Implementation** (C++):

.. code-block:: cpp

    #include <app-common/zap-generated/attributes/Accessors.h>
    #include <app/clusters/on-off-server/on-off-server.h>
    
    using namespace chip;
    using namespace chip::app::Clusters;
    
    void MatterPostAttributeChangeCallback(const chip::app::ConcreteAttributePath & path,
                                          uint8_t type, uint16_t size, uint8_t * value)
    {
        if (path.mClusterId == OnOff::Id &&
            path.mAttributeId == OnOff::Attributes::OnOff::Id)
        {
            bool onOffValue = *value;
            
            // Control actual hardware (GPIO, relay, etc.)
            if (onOffValue) {
                gpio_set_value(LED_GPIO, 1);
                printf("Light turned ON\n");
            } else {
                gpio_set_value(LED_GPIO, 0);
                printf("Light turned OFF\n");
            }
        }
    }

**Project Configuration** (Smart Home Hub):

.. code-block:: text

    Matter Fabric:
    - Fabric ID: 1
    - Node IDs: 1-100
    - Devices: 23 (lights, sensors, locks)
    
    Network Transport:
    - Wi-Fi: Primary
    - Thread: Secondary (battery devices)
    
    Commissioning:
    - QR code scanning
    - BLE pairing (for non-IP devices)
    - Average commissioning time: 18 seconds

====================
6. CAN Bus
====================

6.1 SocketCAN
-------------

**Enable CAN Interface**:

.. code-block:: bash

    # Load CAN modules
    modprobe can
    modprobe can-dev
    modprobe can-raw
    
    # Configure bitrate (500 kbps)
    ip link set can0 type can bitrate 500000
    
    # Bring up interface
    ip link set can0 up
    
    # Check status
    ip -details link show can0

**Send/Receive CAN Frames**:

.. code-block:: bash

    # Send CAN frame (ID 0x123, data: 01 02 03 04)
    cansend can0 123#01020304
    
    # Receive CAN frames
    candump can0
    
    # Filter by ID
    candump can0,123:7FF  # Receive only ID 0x123

**SocketCAN C API**:

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    #include <sys/socket.h>
    #include <sys/ioctl.h>
    #include <net/if.h>
    
    int can_init(const char *ifname)
    {
        int s;
        struct sockaddr_can addr;
        struct ifreq ifr;
        
        /* Create socket */
        s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        
        /* Get interface index */
        strcpy(ifr.ifr_name, ifname);
        ioctl(s, SIOCGIFINDEX, &ifr);
        
        /* Bind socket */
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;
        bind(s, (struct sockaddr *)&addr, sizeof(addr));
        
        return s;
    }
    
    int can_send(int s, uint32_t id, uint8_t *data, uint8_t len)
    {
        struct can_frame frame;
        
        frame.can_id = id;
        frame.can_dlc = len;
        memcpy(frame.data, data, len);
        
        return write(s, &frame, sizeof(frame));
    }
    
    int can_recv(int s, struct can_frame *frame)
    {
        return read(s, frame, sizeof(*frame));
    }

**CAN Filters**:

.. code-block:: c

    /* Set filter to receive only specific IDs */
    struct can_filter rfilter[2];
    
    /* Accept ID 0x100-0x1FF */
    rfilter[0].can_id   = 0x100;
    rfilter[0].can_mask = 0x700;  /* Mask bits [10:8] */
    
    /* Accept ID 0x500 exactly */
    rfilter[1].can_id   = 0x500;
    rfilter[1].can_mask = 0x7FF;  /* All bits must match */
    
    setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &rfilter, sizeof(rfilter));

6.2 CAN-FD (Flexible Data-rate)
--------------------------------

**Configure CAN-FD**:

.. code-block:: bash

    # Set CAN-FD bitrates (arbitration: 500k, data: 2M)
    ip link set can0 type can bitrate 500000 dbitrate 2000000 fd on
    ip link set can0 up

**CAN-FD Frame Transmission**:

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    
    int canfd_send(int s, uint32_t id, uint8_t *data, uint8_t len)
    {
        struct canfd_frame frame;
        
        frame.can_id = id;
        frame.len = len;  /* Up to 64 bytes */
        frame.flags = CANFD_BRS | CANFD_ESI;  /* Bit Rate Switch, Error State Indicator */
        memcpy(frame.data, data, len);
        
        return write(s, &frame, sizeof(frame));
    }

**Project Implementation** (E-Bike Infotainment):

.. code-block:: text

    CAN Network:
    - Battery Management System (BMS): ID 0x100-0x11F
    - Motor Controller: ID 0x200-0x21F
    - Dashboard: ID 0x300-0x31F
    - Infotainment (this device): ID 0x400-0x41F
    
    Bitrate: 500 kbps
    Frame Rate: 10 Hz (BMS), 50 Hz (Motor), 20 Hz (Dashboard)
    
    Example Messages:
    - 0x100: Battery voltage (16-bit, 0.1V resolution)
    - 0x101: Battery current (16-bit, 0.1A resolution)
    - 0x102: State of charge (8-bit, 1% resolution)
    - 0x200: Motor RPM (16-bit)
    - 0x201: Motor temperature (8-bit, °C)

6.3 J1939 (Heavy Vehicle CAN)
------------------------------

**J1939 Socket**:

.. code-block:: c

    #include <linux/can/j1939.h>
    
    int j1939_socket(uint8_t addr)
    {
        int s;
        struct sockaddr_can addr_can;
        
        s = socket(PF_CAN, SOCK_DGRAM, CAN_J1939);
        
        addr_can.can_family = AF_CAN;
        addr_can.can_addr.j1939.name = J1939_NO_NAME;
        addr_can.can_addr.j1939.addr = addr;  /* Source address */
        addr_can.can_addr.j1939.pgn = J1939_NO_PGN;
        addr_can.can_ifindex = if_nametoindex("can0");
        
        bind(s, (struct sockaddr *)&addr_can, sizeof(addr_can));
        
        return s;
    }
    
    /* Send J1939 message (PGN 0xFEF1 - Engine Temperature) */
    int j1939_send_engine_temp(int s, uint8_t temp_celsius)
    {
        struct sockaddr_can dest;
        uint8_t data[8] = {0};
        
        dest.can_family = AF_CAN;
        dest.can_addr.j1939.name = J1939_NO_NAME;
        dest.can_addr.j1939.pgn = 0xFEF1;  /* Engine Temperature 1 */
        dest.can_addr.j1939.addr = 0xFF;    /* Broadcast */
        dest.can_ifindex = if_nametoindex("can0");
        
        data[0] = temp_celsius + 40;  /* 0-250°C, offset -40 */
        
        return sendto(s, data, sizeof(data), 0,
                     (struct sockaddr *)&dest, sizeof(dest));
    }

====================
7. AFDX (ARINC 664 Part 7)
====================

7.1 AFDX Overview
-----------------

**AFDX Characteristics**:

.. code-block:: text

    - Based on Ethernet (100 Mbps, full-duplex)
    - Dual-redundant networks (Network A & B)
    - Virtual Links (VL) for traffic segregation
    - Bandwidth Allocation Gap (BAG) for determinism
    - Built-in integrity checking (CRC-32)

**Virtual Link Concept**:

.. code-block:: text

    VL Parameters:
    - VL_ID: Unique identifier
    - BAG: Minimum interval between frames (1ms, 2ms, 4ms, ..., 128ms)
    - Max Frame Size: e.g., 1518 bytes
    - Src/Dst MAC addresses

7.2 AFDX Driver Implementation
-------------------------------

**Virtual Link Configuration**:

.. code-block:: c

    /* drivers/net/ethernet/afdx/afdx_core.c */
    
    struct afdx_vl {
        u16 vl_id;
        u32 bag_us;          /* BAG in microseconds */
        u16 max_frame_size;
        u8 src_mac[ETH_ALEN];
        u8 dst_mac[ETH_ALEN];
        u16 dst_port;
        
        struct sk_buff_head tx_queue;
        struct hrtimer bag_timer;
        ktime_t last_tx;
    };
    
    /* BAG enforcement */
    static enum hrtimer_restart afdx_bag_timer_handler(struct hrtimer *timer)
    {
        struct afdx_vl *vl = container_of(timer, struct afdx_vl, bag_timer);
        struct sk_buff *skb;
        ktime_t now, next_tx;
        
        now = ktime_get();
        next_tx = ktime_add_us(vl->last_tx, vl->bag_us);
        
        if (ktime_after(now, next_tx)) {
            /* Time to transmit */
            skb = skb_dequeue(&vl->tx_queue);
            if (skb) {
                afdx_hw_tx(vl, skb);
                vl->last_tx = now;
            }
            
            /* Schedule next transmission */
            hrtimer_forward_now(timer, us_to_ktime(vl->bag_us));
            return HRTIMER_RESTART;
        }
        
        return HRTIMER_NORESTART;
    }

**AFDX Frame Format**:

.. code-block:: c

    struct afdx_frame {
        /* Ethernet header */
        u8 dst_mac[6];
        u8 src_mac[6];
        u16 ethertype;  /* 0x0800 for IPv4 */
        
        /* IP header */
        u8 version_ihl;
        u8 tos;
        u16 total_length;
        u16 identification;
        u16 flags_fragment;
        u8 ttl;
        u8 protocol;  /* 0x11 for UDP */
        u16 header_checksum;
        u32 src_ip;
        u32 dst_ip;
        
        /* UDP header */
        u16 src_port;
        u16 dst_port;
        u16 length;
        u16 checksum;
        
        /* AFDX payload */
        u8 data[1];  /* Variable length */
        
        /* AFDX trailer (32-bit CRC) */
        u32 fcs;
    } __packed;

**Userspace API** (sendmsg with VL ID):

.. code-block:: c

    int afdx_send(int sockfd, uint16_t vl_id, const void *data, size_t len)
    {
        struct sockaddr_ll addr = {0};
        struct msghdr msg = {0};
        struct iovec iov;
        struct cmsghdr *cmsg;
        char control[CMSG_SPACE(sizeof(vl_id))];
        
        addr.sll_family = AF_PACKET;
        addr.sll_protocol = htons(ETH_P_IP);
        addr.sll_ifindex = if_nametoindex("afdx0");
        
        iov.iov_base = (void *)data;
        iov.iov_len = len;
        
        msg.msg_name = &addr;
        msg.msg_namelen = sizeof(addr);
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        msg.msg_control = control;
        msg.msg_controllen = sizeof(control);
        
        /* Add VL ID as ancillary data */
        cmsg = CMSG_FIRSTHDR(&msg);
        cmsg->cmsg_level = SOL_PACKET;
        cmsg->cmsg_type = PACKET_VL_ID;  /* Custom control message */
        cmsg->cmsg_len = CMSG_LEN(sizeof(vl_id));
        memcpy(CMSG_DATA(cmsg), &vl_id, sizeof(vl_id));
        
        return sendmsg(sockfd, &msg, 0);
    }

**Project Configuration** (Avionics Platform):

.. code-block:: text

    AFDX Network Configuration:
    - Network A: eth0 (192.168.1.x)
    - Network B: eth1 (192.168.2.x)
    
    Virtual Links:
    - VL 1: Flight Management System (BAG=16ms, 512 bytes)
    - VL 2: Weather Radar Data (BAG=64ms, 1024 bytes)
    - VL 3: Engine Parameters (BAG=32ms, 256 bytes)
    - VL 4: Maintenance Data (BAG=128ms, 1024 bytes)
    
    Redundancy Management:
    - Transmit on both networks
    - Receive first valid frame, discard duplicate
    - Frame sequence numbers for ordering
    
    Measured Performance:
    - Frame loss: <10^-9 (dual redundancy)
    - Latency: <1ms (99.9th percentile)
    - Jitter: <50µs

====================
8. Ethernet Advanced Features
====================

8.1 VLAN Configuration
----------------------

.. code-block:: bash

    # Create VLAN interface
    ip link add link eth0 name eth0.100 type vlan id 100
    ip addr add 192.168.100.1/24 dev eth0.100
    ip link set eth0.100 up
    
    # Tag outgoing traffic
    tc qdisc add dev eth0 root handle 1: prio
    tc filter add dev eth0 parent 1: protocol ip prio 1 \
        u32 match ip dst 192.168.100.0/24 flowid 1:1

8.2 QoS (Quality of Service)
-----------------------------

**Traffic Control (tc)**:

.. code-block:: bash

    # Create HTB (Hierarchical Token Bucket) qdisc
    tc qdisc add dev eth0 root handle 1: htb default 30
    
    # Create classes with bandwidth limits
    tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit
    tc class add dev eth0 parent 1:1 classid 1:10 htb rate 50mbit ceil 80mbit prio 1  # High priority
    tc class add dev eth0 parent 1:1 classid 1:20 htb rate 30mbit ceil 60mbit prio 2  # Medium priority
    tc class add dev eth0 parent 1:1 classid 1:30 htb rate 20mbit ceil 40mbit prio 3  # Low priority
    
    # Add filters to classify traffic
    tc filter add dev eth0 parent 1: protocol ip prio 1 u32 \
        match ip dport 5060 0xffff \  # SIP (VoIP)
        flowid 1:10
    
    tc filter add dev eth0 parent 1: protocol ip prio 2 u32 \
        match ip dport 80 0xffff \    # HTTP
        flowid 1:20

**DSCP Marking**:

.. code-block:: c

    /* Set DSCP value on socket */
    int set_dscp(int sockfd, uint8_t dscp)
    {
        int tos = dscp << 2;  /* DSCP is upper 6 bits of TOS */
        return setsockopt(sockfd, IPPROTO_IP, IP_TOS, &tos, sizeof(tos));
    }
    
    /* Example DSCP values */
    #define DSCP_EF    0x2E  /* Expedited Forwarding (46) - VoIP */
    #define DSCP_AF41  0x22  /* Assured Forwarding 41 (34) - Video */
    #define DSCP_AF21  0x12  /* Assured Forwarding 21 (18) - Bulk data */
    #define DSCP_CS0   0x00  /* Best effort (0) */

8.3 Ethernet AVB/TSN (Time-Sensitive Networking)
-------------------------------------------------

**802.1Qav (Credit-Based Shaper)**:

.. code-block:: bash

    # Configure CBS on network interface
    tc qdisc replace dev eth0 parent root handle 100 mqprio \
        num_tc 3 \
        map 2 2 1 0 2 2 2 2 2 2 2 2 2 2 2 2 \
        queues 1@0 1@1 2@2 \
        hw 0
    
    # Configure CBS for Class A (Audio) - 8000 bps reserved
    tc qdisc replace dev eth0 parent 100:1 cbs \
        idleslope 8000 sendslope -992000 \
        hicredit 12 locredit -113 \
        offload 1
    
    # Configure CBS for Class B (Video) - 16000 bps reserved
    tc qdisc replace dev eth0 parent 100:2 cbs \
        idleslope 16000 sendslope -984000 \
        hicredit 24 locredit -227 \
        offload 1

**802.1AS (gPTP - Precision Time Protocol)**:

.. code-block:: bash

    # Install linuxptp
    apt-get install linuxptp
    
    # Start ptp4l (PTP daemon)
    ptp4l -i eth0 -m -s
    
    # Check synchronization status
    pmc -u -b 0 'GET TIME_STATUS_NP'
    
    # Synchronize system clock
    phc2sys -s eth0 -w

====================
9. Network Stack Optimization
====================

9.1 Kernel Network Tuning
--------------------------

.. code-block:: bash

    # Increase network buffer sizes
    sysctl -w net.core.rmem_max=536870912     # 512 MB
    sysctl -w net.core.wmem_max=536870912
    sysctl -w net.core.rmem_default=33554432  # 32 MB
    sysctl -w net.core.wmem_default=33554432
    
    # TCP tuning
    sysctl -w net.ipv4.tcp_rmem="4096 87380 536870912"
    sysctl -w net.ipv4.tcp_wmem="4096 65536 536870912"
    sysctl -w net.ipv4.tcp_congestion_control=bbr
    
    # Increase connection tracking
    sysctl -w net.netfilter.nf_conntrack_max=1000000
    
    # Reduce TIME_WAIT sockets
    sysctl -w net.ipv4.tcp_tw_reuse=1
    
    # Enable TCP Fast Open
    sysctl -w net.ipv4.tcp_fastopen=3

9.2 Interrupt Coalescing
-------------------------

.. code-block:: bash

    # View current settings
    ethtool -c eth0
    
    # Set interrupt coalescing (reduce interrupts)
    ethtool -C eth0 rx-usecs 50 rx-frames 32 \
                    tx-usecs 50 tx-frames 32

9.3 RSS (Receive Side Scaling)
-------------------------------

.. code-block:: bash

    # View RSS settings
    ethtool -x eth0
    
    # Set number of RSS queues
    ethtool -L eth0 combined 4
    
    # Distribute IRQs to CPUs
    echo 1 > /proc/irq/45/smp_affinity  # IRQ 45 → CPU 0
    echo 2 > /proc/irq/46/smp_affinity  # IRQ 46 → CPU 1
    echo 4 > /proc/irq/47/smp_affinity  # IRQ 47 → CPU 2
    echo 8 > /proc/irq/48/smp_affinity  # IRQ 48 → CPU 3

====================
10. Project Integration Examples
====================

**Smart Home Hub Network Stack**:

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │          i.MX 93 Smart Home Hub         │
    │                                         │
    │  ┌──────────┐  ┌──────────┐            │
    │  │  Matter  │  │  Zigbee  │            │
    │  │  /Thread │  │  2MQTT   │            │
    │  └─────┬────┘  └─────┬────┘            │
    │        │             │ MQTT            │
    │  ┌─────▼─────────────▼────┐            │
    │  │    Application Layer   │            │
    │  └─────┬──────────────────┘            │
    │  ┌─────▼──────┐  ┌────────┐            │
    │  │  TCP/IP    │  │  BLE   │            │
    │  │  (Wi-Fi)   │  │        │            │
    │  └─────┬──────┘  └────┬───┘            │
    │        │              │                │
    │  ┌─────▼──────┐  ┌────▼────┐           │
    │  │  wlan0     │  │  hci0   │           │
    │  │  (802.11ax)│  │         │           │
    │  └────────────┘  └─────────┘           │
    └─────────────────────────────────────────┘

**E-Bike Network Integration**:

.. code-block:: text

    ┌─────────────────────────────────────────┐
    │       E-Bike Infotainment System        │
    │                                         │
    │  ┌──────────┐  ┌──────────────┐        │
    │  │   UI     │  │  Bluetooth   │        │
    │  │          │  │  Audio (A2DP)│        │
    │  └────┬─────┘  └──────┬───────┘        │
    │       │               │                │
    │  ┌────▼───────────────▼───┐            │
    │  │   Application Layer    │            │
    │  └────┬───────────────────┘            │
    │       │                                │
    │  ┌────▼────────┐                       │
    │  │  SocketCAN  │                       │
    │  └────┬────────┘                       │
    │       │                                │
    │  ┌────▼────────┐                       │
    │  │   can0      │                       │
    │  │  (500 kbps) │                       │
    │  └─────────────┘                       │
    │       │                                │
    │       ▼ CAN Bus                        │
    │  [BMS] [Motor] [Dashboard]            │
    └─────────────────────────────────────────┘

====================
11. References
====================

**Wi-Fi**:
- IEEE 802.11 standards
- wpa_supplicant: https://w1.fi/wpa_supplicant/
- hostapd: https://w1.fi/hostapd/

**Bluetooth**:
- Bluetooth Core Specification 5.3
- BlueZ: http://www.bluez.org/

**Zigbee & Thread**:
- Zigbee2MQTT: https://www.zigbee2mqtt.io/
- OpenThread: https://openthread.io/

**Matter**:
- Matter Specification 1.0
- Project CHIP: https://github.com/project-chip/connectedhomeip

**CAN**:
- SocketCAN: https://www.kernel.org/doc/html/latest/networking/can.html
- ISO 11898 (CAN specification)

**AFDX**:
- ARINC 664 Part 7

**Linux Networking**:
- Linux Advanced Routing & Traffic Control HOWTO
- https://www.kernel.org/doc/html/latest/networking/

---

**Revision History**:

========  ==========  ====================================
Version   Date        Changes
========  ==========  ====================================
1.0       2026-01-22  Initial comprehensive connectivity guide
========  ==========  ====================================
