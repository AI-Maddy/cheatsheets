================================================================================
Matter Smart Home & IoT Communication Protocols - Project Experience
================================================================================

:Author: Madhavan Vivekanandan
:Date: January 21, 2026
:Current Project: i.MX 93 Smart Home Platform (2024-Present)
:Standards: Matter, Thread, Zigbee 3.0, WiFi 802.11ax, Bluetooth 5.2/BLE
:Security: HAB Secure Boot, ARM TrustZone, OTA Updates

================================================================================
Overview
================================================================================

This document captures hands-on implementation of Matter protocol and modern
IoT communication stack for smart home platforms.

**Current Project: i.MX 93 Smart Home Gateway (2024-Present)**
- **Hardware:** i.MX 93 (Dual Cortex-A55 + Cortex-M33), EdgeLock secure enclave
- **OS:** Embedded Linux (Yocto custom BSW with meta-imx)
- **Protocols:** Matter, Thread, Zigbee 3.0, WiFi 6, BLE 5.2
- **Voice:** Alexa, Google Home integration
- **Security:** HAB secure boot, ARM TrustZone, encrypted OTA
- **Build:** Yocto Project (custom meta-layer)

**Key Features:**
- Multi-protocol smart home hub (Matter + Zigbee + WiFi + BLE)
- Heterogeneous processing (A55 application + M33 real-time)
- Thread border router for mesh networking
- Local voice processing with edge AI
- Energy-efficient always-on architecture

================================================================================
Matter Protocol - Application Layer
================================================================================

Matter Overview
--------------------------------------------------------------------------------

**Matter** (formerly CHIP - Connected Home over IP) is an IP-based, unified
smart home standard developed by the Connectivity Standards Alliance (CSA).

**Key Characteristics:**
- Application layer protocol over IPv6
- Transport: Thread, WiFi, Ethernet (BLE for commissioning)
- Data model: Clusters (attributes, commands, events)
- Security: Device Attestation Certificates, CASE/PASE sessions
- Multi-admin: Multiple ecosystems (Apple, Google, Amazon) control same device

**Architecture:**

::

    ┌─────────────────────────────────────────────────────────────┐
    │           Cloud Services (Alexa, Google Home, HomeKit)      │
    └───────────────────────────┬─────────────────────────────────┘
                                │ (HTTPS, MQTT)
    ┌───────────────────────────▼─────────────────────────────────┐
    │           Matter Controller (iOS/Android App)               │
    │           - Commissioning                                   │
    │           - Device control                                  │
    │           - Multi-fabric management                         │
    └───────────────────────────┬─────────────────────────────────┘
                                │ (Matter over Thread/WiFi)
    ┌───────────────────────────▼─────────────────────────────────┐
    │     i.MX 93 Smart Home Gateway (Matter Border Router)      │
    ├─────────────────────────────────────────────────────────────┤
    │  Matter Stack (Open Source - Project CHIP SDK)             │
    │  ┌──────────────────────────────────────────────────────┐  │
    │  │  Application Layer                                   │  │
    │  │  - Device Types (Light, Thermostat, Lock, etc.)     │  │
    │  │  - Data Model (Clusters, Attributes, Commands)      │  │
    │  ├──────────────────────────────────────────────────────┤  │
    │  │  Interaction Model                                   │  │
    │  │  - Read/Write/Invoke/Subscribe                       │  │
    │  ├──────────────────────────────────────────────────────┤  │
    │  │  Security (CASE, PASE, Group Keys)                  │  │
    │  ├──────────────────────────────────────────────────────┤  │
    │  │  Message Layer (Reliable/Unreliable Messaging)      │  │
    │  ├──────────────────────────────────────────────────────┤  │
    │  │  Transport Layer (UDP, TCP, BLE)                    │  │
    │  └──────────────────────────────────────────────────────┘  │
    ├─────────────────────────────────────────────────────────────┤
    │  Network Stack                                              │
    │  - Thread (802.15.4 mesh)                                   │
    │  - WiFi 6 (802.11ax)                                        │
    │  - Bluetooth 5.2 (commissioning)                            │
    └─────────────────────────────────────────────────────────────┘
                                │
    ┌───────────────────────────▼─────────────────────────────────┐
    │     End Devices (Smart Lights, Sensors, Locks, etc.)       │
    └─────────────────────────────────────────────────────────────┘

Matter Device Implementation
--------------------------------------------------------------------------------

**Device Types:**
Matter defines standard device types with specific cluster requirements.

**Example: Smart Light (On/Off Light)**

.. code-block:: cpp

    // Matter SDK (Project CHIP)
    #include <app/server/Server.h>
    #include <app/clusters/on-off-server/on-off-server.h>
    #include <platform/CHIPDeviceLayer.h>
    
    using namespace chip;
    using namespace chip::app;
    using namespace chip::DeviceLayer;
    
    class SmartLight {
    public:
        SmartLight(EndpointId endpoint) : endpoint_(endpoint) {}
        
        // Initialize Matter endpoint with On/Off cluster
        void Initialize() {
            // Register On/Off cluster (0x0006)
            emberAfEndpointEnableDisable(endpoint_, true);
            
            // Set device type: On/Off Light (0x0100)
            emberAfSetDeviceTypeList(endpoint_, 
                Span<const EmberAfDeviceType>(device_types_, 1));
            
            // Register attribute change callback
            registerAttributeAccessOverride(this);
        }
        
        // Matter command: On/Off cluster - ON command (0x01)
        CHIP_ERROR HandleOnCommand() {
            ChipLogProgress(Zcl, "Light ON command received");
            
            // Turn on physical LED/relay
            GPIO_SetBit(LED_GPIO_PIN);
            
            // Update Matter attribute: OnOff (0x0000)
            Clusters::OnOff::Attributes::OnOff::Set(endpoint_, true);
            
            return CHIP_NO_ERROR;
        }
        
        // Matter command: On/Off cluster - OFF command (0x00)
        CHIP_ERROR HandleOffCommand() {
            ChipLogProgress(Zcl, "Light OFF command received");
            
            // Turn off physical LED/relay
            GPIO_ClearBit(LED_GPIO_PIN);
            
            // Update Matter attribute
            Clusters::OnOff::Attributes::OnOff::Set(endpoint_, false);
            
            return CHIP_NO_ERROR;
        }
        
        // Matter command: On/Off cluster - TOGGLE command (0x02)
        CHIP_ERROR HandleToggleCommand() {
            bool current_state;
            Clusters::OnOff::Attributes::OnOff::Get(endpoint_, &current_state);
            
            if (current_state) {
                return HandleOffCommand();
            } else {
                return HandleOnCommand();
            }
        }
        
    private:
        EndpointId endpoint_;
        EmberAfDeviceType device_types_[1] = {{0x0100, 1}};  // On/Off Light, v1
    };
    
    // Matter application main
    void MatterApplicationInit() {
        // Initialize Matter stack
        chip::Server::GetInstance().Init();
        
        // Create smart light endpoint 1
        SmartLight light(1);
        light.Initialize();
        
        // Start Matter server
        chip::Server::GetInstance().Run();
    }

**Matter Data Model - Clusters:**

.. code-block:: cpp

    // Common Matter clusters
    
    // 1. On/Off Cluster (0x0006)
    namespace Clusters::OnOff {
        // Attributes
        constexpr AttributeId kOnOffAttribute = 0x0000;  // bool
        
        // Commands
        constexpr CommandId kOffCommand = 0x00;
        constexpr CommandId kOnCommand = 0x01;
        constexpr CommandId kToggleCommand = 0x02;
    }
    
    // 2. Level Control Cluster (0x0008) - Dimming
    namespace Clusters::LevelControl {
        // Attributes
        constexpr AttributeId kCurrentLevelAttribute = 0x0000;  // uint8 (0-254)
        constexpr AttributeId kMinLevelAttribute = 0x0002;
        constexpr AttributeId kMaxLevelAttribute = 0x0003;
        
        // Commands
        constexpr CommandId kMoveToLevelCommand = 0x00;
        struct MoveToLevelParams {
            uint8_t level;
            uint16_t transition_time;  // 1/10 seconds
        };
    }
    
    // 3. Color Control Cluster (0x0300) - RGB/HSV
    namespace Clusters::ColorControl {
        // Attributes
        constexpr AttributeId kCurrentHueAttribute = 0x0000;  // uint8 (0-254)
        constexpr AttributeId kCurrentSaturationAttribute = 0x0001;  // uint8
        constexpr AttributeId kColorTemperatureMiredsAttribute = 0x0007;  // uint16
        
        // Commands
        constexpr CommandId kMoveToHueCommand = 0x00;
        constexpr CommandId kMoveToSaturationCommand = 0x03;
        constexpr CommandId kMoveToHueAndSaturationCommand = 0x06;
    }
    
    // 4. Temperature Measurement Cluster (0x0402) - Sensors
    namespace Clusters::TemperatureMeasurement {
        // Attributes
        constexpr AttributeId kMeasuredValueAttribute = 0x0000;  // int16 (°C * 100)
        constexpr AttributeId kMinMeasuredValueAttribute = 0x0001;
        constexpr AttributeId kMaxMeasuredValueAttribute = 0x0002;
    }

**Matter Interaction Model - Subscriptions:**

.. code-block:: cpp

    // Subscribe to attribute changes (for controller/bridge)
    #include <app/InteractionModelEngine.h>
    
    class MatterSubscriptionHandler : public ReadClient::Callback {
    public:
        // Subscribe to temperature sensor updates
        CHIP_ERROR SubscribeToTemperature(NodeId node_id, EndpointId endpoint) {
            // Create attribute path
            AttributePathParams attr_path;
            attr_path.mEndpointId = endpoint;
            attr_path.mClusterId = Clusters::TemperatureMeasurement::Id;
            attr_path.mAttributeId = 
                Clusters::TemperatureMeasurement::Attributes::MeasuredValue::Id;
            
            // Subscribe with min/max intervals
            ReadPrepareParams params(SessionHandle());
            params.mAttributePathParamsListSize = 1;
            params.mpAttributePathParamsList = &attr_path;
            params.mMinIntervalFloorSeconds = 5;    // Min 5 seconds
            params.mMaxIntervalCeilingSeconds = 60;  // Max 60 seconds
            
            // Create read client for subscription
            read_client_ = std::make_unique<ReadClient>(
                InteractionModelEngine::GetInstance(),
                /* exchangeMgr */ nullptr,
                *this,
                ReadClient::InteractionType::Subscribe
            );
            
            return read_client_->SendSubscribeRequest(params);
        }
        
        // Callback: Attribute report received
        void OnAttributeData(const ConcreteDataAttributePath &path,
                             TLV::TLVReader *data) override {
            if (path.mClusterId == Clusters::TemperatureMeasurement::Id &&
                path.mAttributeId == 
                    Clusters::TemperatureMeasurement::Attributes::MeasuredValue::Id) {
                
                int16_t temp_raw;
                data->Get(temp_raw);
                
                float temperature_celsius = temp_raw / 100.0f;
                ChipLogProgress(Zcl, "Temperature update: %.2f°C", 
                                temperature_celsius);
                
                // Forward to cloud service
                SendToCloudService(temperature_celsius);
            }
        }
        
    private:
        std::unique_ptr<ReadClient> read_client_;
    };

Matter Commissioning (Device Pairing)
--------------------------------------------------------------------------------

**Commissioning Process:**

1. **BLE Advertisement** (device not commissioned)
2. **PASE Session** (Password-Authenticated Session Establishment)
3. **Network Provisioning** (WiFi/Thread credentials)
4. **Operational Certificate Installation**
5. **CASE Session** (Certificate-Authenticated Session Establishment)

.. code-block:: cpp

    // Commissioning server setup
    #include <platform/CommissionableDataProvider.h>
    #include <setup_payload/QRCodeSetupPayloadGenerator.h>
    
    class MatterCommissioningManager {
    public:
        void Initialize() {
            // Set commissioning parameters
            CommissionableDataProvider *data_provider = 
                DeviceLayer::GetCommissionableDataProvider();
            
            // Setup discriminator (12-bit, unique per device)
            data_provider->SetSetupDiscriminator(0x0F00);
            
            // Setup PIN code (27-bit, for QR code/manual entry)
            data_provider->SetSetupPasscode(20202021);
            
            // Vendor ID and Product ID
            data_provider->SetVendorId(0xFFF1);  // Test vendor ID
            data_provider->SetProductId(0x8001);
            
            // Generate QR code payload
            GenerateQRCode();
            
            // Enable BLE advertising for commissioning
            ConnectivityMgr().SetBLEAdvertisingEnabled(true);
        }
        
        void GenerateQRCode() {
            SetupPayload payload;
            payload.version = 0;
            payload.vendorID = 0xFFF1;
            payload.productID = 0x8001;
            payload.setUpPINCode = 20202021;
            payload.discriminator = 0x0F00;
            
            QRCodeSetupPayloadGenerator generator(payload);
            std::string qr_code;
            generator.payloadBase38Representation(qr_code);
            
            ChipLogProgress(AppServer, "QR Code: %s", qr_code.c_str());
            // Example: MT:Y.K90SO527JA0648G00
        }
        
        // Commissioning complete callback
        void OnCommissioningComplete(NodeId node_id, FabricIndex fabric) {
            ChipLogProgress(AppServer, "Device commissioned: NodeId=0x%llx, Fabric=%d",
                            node_id, fabric);
            
            // Disable BLE advertising (commissioned)
            ConnectivityMgr().SetBLEAdvertisingEnabled(false);
            
            // Enable operational network (Thread/WiFi)
            StartOperationalNetwork();
        }
    };

Matter Security - Device Attestation
--------------------------------------------------------------------------------

**Device Attestation Certificate (DAC):**

.. code-block:: cpp

    // Device attestation for factory provisioning
    #include <credentials/DeviceAttestationCredsProvider.h>
    
    class CustomDeviceAttestationCredentials : 
        public Credentials::DeviceAttestationCredentialsProvider {
    public:
        // Get Device Attestation Certificate (X.509)
        CHIP_ERROR GetDeviceAttestationCert(MutableByteSpan &out_buffer) override {
            // Load DAC from secure storage (EdgeLock on i.MX 93)
            size_t cert_size;
            uint8_t cert_data[512];
            ReadFromSecureElement(DAC_KEY_ID, cert_data, &cert_size);
            
            return CopySpanToMutableSpan(ByteSpan(cert_data, cert_size), out_buffer);
        }
        
        // Get Product Attestation Intermediate (PAI) certificate
        CHIP_ERROR GetProductAttestationIntermediateCert(
            MutableByteSpan &out_buffer) override {
            // Load PAI from flash
            const uint8_t pai_cert[] = { /* ... DER encoded cert ... */ };
            return CopySpanToMutableSpan(ByteSpan(pai_cert, sizeof(pai_cert)), 
                                          out_buffer);
        }
        
        // Sign with Device Attestation private key
        CHIP_ERROR SignWithDeviceAttestationKey(const ByteSpan &message,
                                                 MutableByteSpan &signature) override {
            // Use secure element for signing (private key never leaves HW)
            return SecureElement_Sign(DAC_KEY_ID, message.data(), message.size(),
                                       signature.data(), &signature.size());
        }
    };

================================================================================
Thread Protocol - Mesh Networking
================================================================================

Thread Overview
--------------------------------------------------------------------------------

**Thread** is an IPv6-based, low-power mesh networking protocol for IoT devices.

**Key Features:**
- IEEE 802.15.4 PHY/MAC (2.4 GHz)
- IPv6 addressing (6LoWPAN compression)
- Self-healing mesh topology
- No single point of failure
- AES-128 encryption
- Border Router for external connectivity

**Thread Network Architecture:**

::

    ┌───────────────────────────────────────────────────────────────┐
    │              Internet / Cloud Services                        │
    └────────────────────────────┬──────────────────────────────────┘
                                 │ (IPv6)
    ┌────────────────────────────▼──────────────────────────────────┐
    │     Thread Border Router (i.MX 93 Gateway)                   │
    │     - Routes between Thread mesh and external networks        │
    │     - Provides IPv6 prefix to Thread network                  │
    └────────────────────────────┬──────────────────────────────────┘
                                 │ (802.15.4)
    ┌────────────────────────────▼──────────────────────────────────┐
    │            Thread Mesh Network                                │
    │                                                               │
    │  ┌──────────┐        ┌──────────┐        ┌──────────┐       │
    │  │  Router  │◄──────►│  Router  │◄──────►│  Router  │       │
    │  │  Node    │        │  Node    │        │  Node    │       │
    │  └────┬─────┘        └────┬─────┘        └────┬─────┘       │
    │       │                   │                   │              │
    │  ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐       │
    │  │   End    │        │   End    │        │Sleepy End│       │
    │  │  Device  │        │  Device  │        │  Device  │       │
    │  │ (Light)  │        │ (Sensor) │        │ (Sensor) │       │
    │  └──────────┘        └──────────┘        └──────────┘       │
    └───────────────────────────────────────────────────────────────┘

**Device Roles:**
- **Border Router:** Gateway between Thread and external networks
- **Router:** Full-function device, always on, forwards packets
- **End Device:** Communicates through parent router
- **Sleepy End Device (SED):** Low-power, wakes periodically

Thread Border Router Implementation
--------------------------------------------------------------------------------

.. code-block:: cpp

    // OpenThread library (open-source Thread stack)
    #include <openthread/instance.h>
    #include <openthread/thread.h>
    #include <openthread/ip6.h>
    #include <openthread/border_router.h>
    
    class ThreadBorderRouter {
    public:
        ThreadBorderRouter() {
            // Initialize OpenThread instance
            ot_instance_ = otInstanceInitSingle();
        }
        
        void Initialize() {
            // Set network parameters
            otOperationalDataset dataset;
            otDatasetCreateNewNetwork(ot_instance_, &dataset);
            
            // Network Name
            const char *network_name = "SmartHome-Thread";
            strncpy(dataset.mNetworkName.m8, network_name, OT_NETWORK_NAME_MAX_SIZE);
            
            // PAN ID (16-bit)
            dataset.mPanId = 0x1234;
            
            // Extended PAN ID (64-bit)
            uint8_t ext_pan_id[OT_EXT_PAN_ID_SIZE] = 
                {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77};
            memcpy(dataset.mExtendedPanId.m8, ext_pan_id, OT_EXT_PAN_ID_SIZE);
            
            // Network Key (128-bit AES)
            uint8_t network_key[OT_NETWORK_KEY_SIZE] = 
                {0x00, 0x11, 0x22, /* ... 16 bytes ... */};
            memcpy(dataset.mNetworkKey.m8, network_key, OT_NETWORK_KEY_SIZE);
            
            // Channel (11-26, 2.4 GHz)
            dataset.mChannel = 15;
            
            // Apply dataset
            otDatasetSetActive(ot_instance_, &dataset);
            
            // Enable border router functionality
            otBorderRouterSetEnabled(ot_instance_, true);
            
            // Add external route (to Internet)
            otBorderRouterConfig config;
            otIp6AddressFromString("::/0", &config.mPrefix.mPrefix);  // Default route
            config.mPrefix.mLength = 0;
            config.mPreference = OT_ROUTE_PREFERENCE_MED;
            config.mStable = true;
            otBorderRouterAddRoute(ot_instance_, &config);
            
            // Start Thread network
            otIp6SetEnabled(ot_instance_, true);
            otThreadSetEnabled(ot_instance_, true);
            
            ChipLogProgress(DeviceLayer, "Thread Border Router started");
        }
        
        // Forward packets between Thread and Ethernet/WiFi
        void ProcessIncomingPacket(const uint8_t *packet, size_t length) {
            otMessage *message = otIp6NewMessage(ot_instance_, NULL);
            otMessageAppend(message, packet, length);
            
            // Send to Thread network
            otIp6Send(ot_instance_, message);
        }
        
    private:
        otInstance *ot_instance_;
    };

Thread End Device (Smart Sensor)
--------------------------------------------------------------------------------

.. code-block:: c

    // Thread end device (minimal configuration)
    #include <openthread/thread.h>
    
    void Thread_EndDevice_Init(void) {
        otInstance *ot = otInstanceInitSingle();
        
        // Join existing network (commissioning credentials pre-configured)
        otThreadSetEnabled(ot, true);
        
        // Wait for role assignment
        while (otThreadGetDeviceRole(ot) != OT_DEVICE_ROLE_CHILD) {
            otTaskletsProcess(ot);
            usleep(1000);
        }
        
        ChipLogProgress(DeviceLayer, "Thread: Attached as End Device");
        
        // Get IPv6 addresses
        const otNetifAddress *unicast_addrs = otIp6GetUnicastAddresses(ot);
        for (const otNetifAddress *addr = unicast_addrs; addr; addr = addr->mNext) {
            char addr_str[OT_IP6_ADDRESS_STRING_SIZE];
            otIp6AddressToString(&addr->mAddress, addr_str, sizeof(addr_str));
            ChipLogProgress(DeviceLayer, "IPv6 Address: %s", addr_str);
        }
    }
    
    // Send sensor data over Thread
    void SendTemperatureData(float temperature) {
        otInstance *ot = otInstanceInitSingle();
        
        // Create UDP socket
        otUdpSocket socket;
        otUdpOpen(ot, &socket, NULL, NULL);
        
        // Destination: Border router CoAP server
        otMessageInfo message_info;
        otIp6AddressFromString("fd00::1", &message_info.mPeerAddr);  // Border router
        message_info.mPeerPort = 5683;  // CoAP port
        
        // Construct CoAP message (simplified)
        uint8_t coap_payload[32];
        int payload_len = snprintf((char*)coap_payload, sizeof(coap_payload),
                                    "{\"temp\":%.2f}", temperature);
        
        // Send UDP packet
        otMessage *message = otUdpNewMessage(ot, NULL);
        otMessageAppend(message, coap_payload, payload_len);
        otUdpSend(ot, &socket, message, &message_info);
        
        ChipLogProgress(DeviceLayer, "Temperature sent: %.2f°C", temperature);
    }

================================================================================
Zigbee 3.0 - Legacy Device Integration
================================================================================

Zigbee Overview
--------------------------------------------------------------------------------

**Zigbee 3.0:** Unified standard combining Zigbee PRO, Zigbee LL, Zigbee HA

**Key Features:**
- IEEE 802.15.4 PHY/MAC (2.4 GHz)
- Mesh networking (up to 65,000 nodes)
- Application profiles (Home Automation, Light Link, etc.)
- Bindings and groups for direct device-to-device control

**Device Types:**
- **Coordinator:** Network creator (1 per network)
- **Router:** Mesh node, always powered
- **End Device:** Battery-powered, sleeps

Zigbee Coordinator (Gateway)
--------------------------------------------------------------------------------

.. code-block:: c

    // Z-Stack (Texas Instruments Zigbee stack)
    #include "ZComDef.h"
    #include "OSAL.h"
    #include "AF.h"
    #include "ZDApp.h"
    
    // Application endpoint definition
    #define SMARTHOME_ENDPOINT 1
    #define SMARTHOME_PROFID 0x0104  // Home Automation profile
    #define SMARTHOME_DEVICEID 0x0050  // Smart Plug
    
    // Cluster IDs
    #define ZCL_CLUSTER_ID_GEN_ON_OFF 0x0006
    #define ZCL_CLUSTER_ID_MS_TEMPERATURE_MEASUREMENT 0x0402
    
    // Endpoint descriptor
    SimpleDescriptionFormat_t SmartHomeEP = {
        SMARTHOME_ENDPOINT,
        SMARTHOME_PROFID,
        SMARTHOME_DEVICEID,
        0,  // Device version
        0,  // Reserved
        2,  // Input cluster count
        (cId_t[]){ZCL_CLUSTER_ID_GEN_ON_OFF, 
                   ZCL_CLUSTER_ID_MS_TEMPERATURE_MEASUREMENT},
        0,  // Output cluster count
        NULL
    };
    
    // Start Zigbee network as coordinator
    void Zigbee_StartCoordinator(void) {
        // Set device type
        zgDeviceLogicalType = ZG_DEVICETYPE_COORDINATOR;
        
        // Network parameters
        _NIB.nwkLogicalChannel = 15;  // Channel 15 (2.4 GHz)
        _NIB.channelList = 0x00008000;  // Bit mask: only channel 15
        zgDefaultChannelList = 0x00008000;
        
        // PAN ID
        _NIB.nwkPanId = 0x1A2B;
        
        // Extended PAN ID
        uint8_t ext_pan_id[Z_EXTADDR_LEN] = 
            {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77};
        osal_nv_write(ZCD_NV_EXTADDR, 0, Z_EXTADDR_LEN, ext_pan_id);
        
        // Register endpoint
        afRegister(&SmartHomeEP);
        
        // Start network formation
        ZDOInitDevice(0);
    }
    
    // Handle incoming Zigbee messages
    void Zigbee_MessageHandler(afIncomingMSGPacket_t *pkt) {
        switch (pkt->clusterId) {
            case ZCL_CLUSTER_ID_GEN_ON_OFF:
                // On/Off command from remote
                uint8_t command = pkt->cmd.Data[2];
                if (command == 0x01) {
                    // Turn on device
                    GPIO_SetBit(RELAY_PIN);
                } else if (command == 0x00) {
                    // Turn off device
                    GPIO_ClearBit(RELAY_PIN);
                }
                break;
            
            case ZCL_CLUSTER_ID_MS_TEMPERATURE_MEASUREMENT:
                // Temperature report from sensor
                int16_t temp_raw = BUILD_UINT16(pkt->cmd.Data[3], pkt->cmd.Data[4]);
                float temperature = temp_raw / 100.0f;
                
                // Forward to Matter bridge
                BridgeToMatter(pkt->srcAddr.addr.shortAddr, temperature);
                break;
        }
    }

Zigbee to Matter Bridge
--------------------------------------------------------------------------------

.. code-block:: cpp

    // Bridge Zigbee devices to Matter ecosystem
    class ZigbeeToMatterBridge {
    public:
        // Map Zigbee device to Matter endpoint
        void RegisterZigbeeDevice(uint16_t zigbee_short_addr, 
                                   uint16_t zigbee_device_id,
                                   EndpointId matter_endpoint) {
            BridgedDevice device;
            device.zigbee_addr = zigbee_short_addr;
            device.matter_endpoint = matter_endpoint;
            
            bridged_devices_[zigbee_short_addr] = device;
            
            // Create Matter dynamic endpoint
            CreateMatterBridgedEndpoint(matter_endpoint, zigbee_device_id);
        }
        
        // Forward Zigbee attribute to Matter
        void OnZigbeeAttributeReport(uint16_t zigbee_addr, 
                                       uint16_t cluster_id,
                                       uint16_t attribute_id,
                                       const uint8_t *data, size_t length) {
            auto it = bridged_devices_.find(zigbee_addr);
            if (it == bridged_devices_.end()) return;
            
            EndpointId matter_ep = it->second.matter_endpoint;
            
            // Map Zigbee cluster to Matter cluster
            if (cluster_id == 0x0006) {  // Zigbee On/Off
                bool on_off = data[0];
                Clusters::OnOff::Attributes::OnOff::Set(matter_ep, on_off);
            } else if (cluster_id == 0x0402) {  // Temperature Measurement
                int16_t temp_raw = (data[1] << 8) | data[0];
                Clusters::TemperatureMeasurement::Attributes::MeasuredValue::Set(
                    matter_ep, temp_raw
                );
            }
        }
        
        // Forward Matter command to Zigbee
        void OnMatterCommand(EndpointId matter_ep, uint32_t cluster_id, 
                              uint32_t command_id) {
            // Find Zigbee device for this Matter endpoint
            uint16_t zigbee_addr = 0;
            for (const auto &pair : bridged_devices_) {
                if (pair.second.matter_endpoint == matter_ep) {
                    zigbee_addr = pair.first;
                    break;
                }
            }
            
            if (zigbee_addr == 0) return;
            
            // Send Zigbee command
            if (cluster_id == Clusters::OnOff::Id) {
                if (command_id == Clusters::OnOff::Commands::On::Id) {
                    SendZigbeeOnCommand(zigbee_addr);
                } else if (command_id == Clusters::OnOff::Commands::Off::Id) {
                    SendZigbeeOffCommand(zigbee_addr);
                }
            }
        }
        
    private:
        struct BridgedDevice {
            uint16_t zigbee_addr;
            EndpointId matter_endpoint;
        };
        
        std::map<uint16_t, BridgedDevice> bridged_devices_;
    };

================================================================================
Security - HAB Secure Boot & OTA Updates
================================================================================

i.MX HAB (High Assurance Boot)
--------------------------------------------------------------------------------

**HAB** ensures only authenticated firmware boots on i.MX processors.

.. code-block:: bash

    # Generate RSA key pair (4096-bit)
    openssl genrsa -out hab_rsa_key.pem 4096
    openssl rsa -in hab_rsa_key.pem -pubout -out hab_rsa_pubkey.pem
    
    # Convert to DER format
    openssl rsa -in hab_rsa_key.pem -outform DER -out hab_rsa_key.der
    
    # Generate Certificate Signing Request (CSR)
    openssl req -new -key hab_rsa_key.pem -out hab_csr.pem
    
    # Self-sign certificate
    openssl x509 -req -days 3650 -in hab_csr.pem -signkey hab_rsa_key.pem \
                 -out hab_cert.pem
    
    # Generate Super Root Key (SRK) hash
    # Fuse SRK hash into i.MX eFuses (one-time programmable)
    srktool -h 4 -t hab_cert.pem -o srk_table.bin -f srk_fuse.bin

**Signing U-Boot and Linux kernel:**

.. code-block:: bash

    # Sign U-Boot using Code Signing Tool (CST)
    ./cst --input u-boot-sign.csf --output u-boot-signed.imx
    
    # CSF (Command Sequence File) example:
    cat > u-boot-sign.csf << EOF
    [Header]
    Version = 4.3
    Hash Algorithm = sha256
    Engine Configuration = 0
    Certificate Format = X509
    Signature Format = CMS
    
    [Install SRK]
    File = "../crts/SRK_table.bin"
    Source index = 0
    
    [Install CSFK]
    File = "../crts/CSF1_1_sha256_4096_65537_v3_usr_crt.pem"
    
    [Authenticate CSF]
    
    [Install Key]
    Verification index = 0
    Target Index = 2
    File = "../crts/IMG1_1_sha256_4096_65537_v3_usr_crt.pem"
    
    [Authenticate Data]
    Verification index = 2
    Blocks = 0x877FF400 0x00000000 0x00090000 "u-boot.imx"
    EOF

**Runtime verification:**

.. code-block:: c

    // Check HAB status in U-Boot
    int check_hab_status(void) {
        hab_rvt_report_event_t *hab_event_func = 
            (hab_rvt_report_event_t *)HAB_RVT_REPORT_EVENT;
        
        hab_status_t status;
        uint8_t event_data[512];
        size_t event_len = sizeof(event_data);
        
        status = hab_event_func(HAB_STATUS_ANY, 0, event_data, &event_len);
        
        if (status == HAB_STATUS_SUCCESS) {
            printf("HAB: No events found\n");
            return 0;
        } else {
            printf("HAB: Security violation detected!\n");
            // Parse event_data for details
            return -1;
        }
    }

OTA (Over-the-Air) Updates
--------------------------------------------------------------------------------

**Secure OTA with signature verification:**

.. code-block:: cpp

    // OTA update manager
    #include <lib/support/logging/CHIPLogging.h>
    #include <platform/OTAImageProcessor.h>
    
    class SecureOTAImageProcessor : public OTAImageProcessorImpl {
    public:
        CHIP_ERROR ProcessBlock(ByteSpan &block) override {
            // Write block to staging partition
            if (staging_fd_ < 0) {
                staging_fd_ = open("/dev/mmcblk0p2", O_WRONLY);  // Staging partition
            }
            
            write(staging_fd_, block.data(), block.size());
            bytes_downloaded_ += block.size();
            
            // Update progress
            float progress = (float)bytes_downloaded_ / total_size_ * 100.0f;
            ChipLogProgress(SoftwareUpdate, "OTA Progress: %.1f%%", progress);
            
            return CHIP_NO_ERROR;
        }
        
        CHIP_ERROR Finalize() override {
            close(staging_fd_);
            
            // Verify firmware signature
            if (!VerifyFirmwareSignature("/dev/mmcblk0p2")) {
                ChipLogError(SoftwareUpdate, "OTA: Signature verification failed!");
                return CHIP_ERROR_INTEGRITY_CHECK_FAILED;
            }
            
            // Mark staging partition as bootable
            SetBootPartition(2);  // Boot from partition 2 on next reboot
            
            ChipLogProgress(SoftwareUpdate, "OTA: Update complete, rebooting...");
            system("reboot");
            
            return CHIP_NO_ERROR;
        }
        
    private:
        bool VerifyFirmwareSignature(const char *firmware_path) {
            // Read firmware
            FILE *fw_file = fopen(firmware_path, "rb");
            fseek(fw_file, 0, SEEK_END);
            size_t fw_size = ftell(fw_file);
            fseek(fw_file, 0, SEEK_SET);
            
            uint8_t *fw_data = (uint8_t*)malloc(fw_size);
            fread(fw_data, 1, fw_size, fw_file);
            fclose(fw_file);
            
            // Extract signature (last 512 bytes)
            const size_t signature_size = 512;
            uint8_t *signature = fw_data + fw_size - signature_size;
            
            // Compute SHA-256 hash of firmware (excluding signature)
            uint8_t hash[32];
            mbedtls_sha256_context sha_ctx;
            mbedtls_sha256_init(&sha_ctx);
            mbedtls_sha256_starts(&sha_ctx, 0);  // SHA-256
            mbedtls_sha256_update(&sha_ctx, fw_data, fw_size - signature_size);
            mbedtls_sha256_finish(&sha_ctx, hash);
            
            // Verify RSA signature with public key
            mbedtls_rsa_context rsa_ctx;
            mbedtls_rsa_init(&rsa_ctx, MBEDTLS_RSA_PKCS_V21, MBEDTLS_MD_SHA256);
            
            // Load public key from secure storage
            LoadRSAPublicKey(&rsa_ctx);
            
            int ret = mbedtls_rsa_pkcs1_verify(&rsa_ctx, NULL, NULL, 
                                                MBEDTLS_RSA_PUBLIC,
                                                MBEDTLS_MD_SHA256,
                                                32, hash, signature);
            
            free(fw_data);
            mbedtls_rsa_free(&rsa_ctx);
            
            return (ret == 0);  // 0 = success
        }
        
        int staging_fd_ = -1;
        size_t bytes_downloaded_ = 0;
        size_t total_size_ = 0;
    };

================================================================================
Yocto Build System Integration
================================================================================

Custom Yocto Layer for Smart Home Gateway
--------------------------------------------------------------------------------

.. code-block:: bash

    # meta-smarthome/conf/layer.conf
    BBPATH .= ":${LAYERDIR}"
    BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
    BBFILE_COLLECTIONS += "meta-smarthome"
    BBFILE_PATTERN_meta-smarthome := "^${LAYERDIR}/"
    LAYERSERIES_COMPAT_meta-smarthome = "kirkstone"

**BitBake recipe for Matter stack:**

.. code-block:: bash

    # meta-smarthome/recipes-connectivity/matter/matter_1.0.bb
    
    SUMMARY = "Matter (Project CHIP) smart home protocol"
    LICENSE = "Apache-2.0"
    
    DEPENDS = "openthread zap glib-2.0 openssl"
    
    SRC_URI = "git://github.com/project-chip/connectedhomeip.git;protocol=https;branch=master"
    SRCREV = "${AUTOREV}"
    
    S = "${WORKDIR}/git"
    
    inherit cmake python3native
    
    EXTRA_OECMAKE = " \
        -DCHIP_ENABLE_WIFI=ON \
        -DCHIP_ENABLE_OPENTHREAD=ON \
        -DCHIP_ENABLE_BLE=ON \
        -DBUILD_TESTS=OFF \
    "
    
    do_install() {
        install -d ${D}${bindir}
        install -m 0755 ${B}/chip-tool ${D}${bindir}/
        install -m 0755 ${B}/chip-all-clusters-app ${D}${bindir}/
    }
    
    FILES_${PN} += "${bindir}/*"

**local.conf customization:**

.. code-block:: bash

    # conf/local.conf
    
    MACHINE = "imx93evk"
    DISTRO = "fsl-imx-xwayland"
    
    # Enable systemd
    DISTRO_FEATURES_append = " systemd"
    VIRTUAL-RUNTIME_init_manager = "systemd"
    
    # Add custom layer
    BBLAYERS += "${BSPDIR}/sources/meta-smarthome"
    
    # Security features
    DISTRO_FEATURES_append = " secure-boot"
    UBOOT_SIGN_ENABLE = "1"
    
    # Image features
    IMAGE_INSTALL_append = " \
        matter \
        openthread \
        zigbee-gateway \
        python3-homeassistant \
    "

================================================================================
Lessons Learned
================================================================================

**Matter Protocol:**
✓ Matter simplifies multi-ecosystem support (Apple, Google, Amazon)
✓ IPv6-based architecture allows direct cloud communication
✓ Device Attestation Certificates essential for security
✓ Subscription model efficient for real-time updates
✓ BLE commissioning user-friendly but requires careful UX design

**Thread Mesh:**
✓ Self-healing mesh more reliable than star topology (Zigbee/Z-Wave)
✓ Border router critical for internet connectivity
✓ Sleepy End Devices require careful power management (parent polling)
✓ Channel selection important to avoid WiFi interference

**Security:**
✓ HAB secure boot prevents unauthorized firmware
✓ TrustZone isolates sensitive operations (key storage, crypto)
✓ OTA signature verification mandatory for production
✓ Encrypted storage (EdgeLock) protects credentials

**Yocto Integration:**
✓ Custom meta-layers enable reproducible builds
✓ Recipe dependencies must be carefully managed
✓ Kernel device tree customization required for hardware peripherals
✓ Image size optimization critical for flash-constrained devices

**Common Pitfalls:**
✗ Matter commissioning fails if device time not synchronized
✗ Thread network formation delayed if radio not properly initialized
✗ Zigbee-Matter bridge introduces latency (>100ms command propagation)
✗ OTA updates can brick device if power lost during flash write

================================================================================
References
================================================================================

**Standards:**
- Matter 1.0 Specification (Connectivity Standards Alliance)
- Thread 1.3.0 Specification
- Zigbee 3.0 Specification
- IEEE 802.15.4-2020 (Low-Rate Wireless Networks)
- RFC 6282 (6LoWPAN Compression)

**Open Source Projects:**
- Project CHIP SDK: https://github.com/project-chip/connectedhomeip
- OpenThread: https://github.com/openthread/openthread
- Z-Stack (TI Zigbee): https://www.ti.com/tool/Z-STACK

**Tools:**
- Wireshark with Thread/Zigbee dissectors
- nRF Sniffer (802.15.4 packet capture)
- ZAP Tool (Zigbee/Matter cluster configuration)
- i.MX Code Signing Tool (CST)

================================================================================
