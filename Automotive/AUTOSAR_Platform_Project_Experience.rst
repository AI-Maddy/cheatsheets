================================================================================
AUTOSAR Platform Architecture - Real-World Implementation
================================================================================

:Author: Madhavan Vivekanandan
:Date: January 21, 2026
:Projects: E-Mobility Systems (2014-2016)
:Standards: AUTOSAR Adaptive & Classic, ISO 26262 ASIL Compliance

================================================================================
Overview
================================================================================

This document captures hands-on implementation of AUTOSAR Adaptive Platform (AP)
and AUTOSAR Classic Platform (CP) from production e-mobility projects:

**Projects:**
1. E-Bike Infotainment Cluster (AUTOSAR Adaptive Platform)
2. Battery Management & Motor Control System (AUTOSAR Classic Platform)

**Platform:** NXP AMP (Adaptive AUTOSAR Platform), ARM Cortex-M4 (Classic)

================================================================================
AUTOSAR Adaptive Platform - Infotainment Cluster
================================================================================

Project Overview
--------------------------------------------------------------------------------

**System:** E-Bike Infotainment Cluster
**Hardware:** NXP S32G (ARM Cortex-A53 + Cortex-M7)
**OS:** Embedded Linux (Yocto-based)
**Network:** CAN, Ethernet (SOME/IP)
**Standards:** ISO 26262 ASIL-B, SAE J1939, ISO 11898

**Architecture:**

::

    ┌─────────────────────────────────────────────────────────────┐
    │           Adaptive AUTOSAR Applications (AA)                │
    ├───────────────┬───────────────┬────────────────┬───────────┤
    │  Navigation   │  Audio/Media  │  Telematics    │   HMI     │
    │  Application  │  Application  │  Application   │  Manager  │
    └───────┬───────┴───────┬───────┴────────┬───────┴───────────┘
            │               │                │
    ┌───────▼───────────────▼────────────────▼───────────────────┐
    │    Adaptive AUTOSAR Runtime for Applications (ARA)         │
    ├────────────────────────────────────────────────────────────┤
    │  ara::com  │ ara::exec │ ara::log │ ara::per │ ara::phm   │
    │ (SOME/IP)  │ (Exec Mgmt)│ (Logging)│ (Storage)│ (Health)   │
    └────────────────────────────────────────────────────────────┘
            │
    ┌───────▼─────────────────────────────────────────────────────┐
    │              Operating System (POSIX Linux)                 │
    └─────────────────────────────────────────────────────────────┘
            │
    ┌───────▼─────────────────────────────────────────────────────┐
    │  Hardware (NXP S32G - Cortex-A53, CAN, Ethernet, GPU)      │
    └─────────────────────────────────────────────────────────────┘

ARA (Adaptive AUTOSAR Runtime) Components
--------------------------------------------------------------------------------

**1. ara::com - Communication Management (SOME/IP)**

Service-Oriented Communication between applications.

.. code-block:: cpp

    // Service Interface Definition (ARXML)
    // NavigationService.arxml
    
    // Service Provider (Navigation App)
    #include <ara/com/service_provider.h>
    
    class NavigationServiceProvider {
    public:
        NavigationServiceProvider() {
            // Register service
            service_instance_ = 
                ara::com::RegisterService<NavigationService>(
                    service_id_,
                    instance_id_
                );
        }
        
        // Service method: GetCurrentPosition
        void GetCurrentPosition(
            std::function<void(Position)> callback
        ) {
            Position pos = gps_driver_->ReadPosition();
            callback(pos);
        }
        
        // Event: PositionUpdated (cyclic 100ms)
        void SendPositionEvent() {
            Position pos = gps_driver_->ReadPosition();
            position_event_.Send(pos);
        }
        
    private:
        ara::com::ServiceInstance<NavigationService> service_instance_;
        ara::com::Event<Position> position_event_;
    };
    
    // Service Consumer (HMI Application)
    #include <ara/com/service_proxy.h>
    
    class NavigationServiceConsumer {
    public:
        NavigationServiceConsumer() {
            // Find and subscribe to service
            auto handles = ara::com::FindService<NavigationService>(
                service_id_
            );
            
            if (!handles.empty()) {
                proxy_ = std::make_unique<NavigationServiceProxy>(
                    handles[0]
                );
                
                // Subscribe to position updates
                proxy_->PositionUpdated.Subscribe([this](Position pos) {
                    UpdateDisplayPosition(pos);
                });
            }
        }
        
        // Call service method
        void RequestCurrentPosition() {
            auto future = proxy_->GetCurrentPosition();
            future.then([](Position pos) {
                std::cout << "Lat: " << pos.latitude 
                          << ", Lon: " << pos.longitude << std::endl;
            });
        }
        
    private:
        std::unique_ptr<NavigationServiceProxy> proxy_;
    };

**SOME/IP Protocol Configuration:**

.. code-block:: json

    {
      "services": [
        {
          "service_id": "0x1234",
          "instance_id": "0x0001",
          "major_version": 1,
          "minor_version": 0,
          "methods": [
            {
              "method_id": "0x0100",
              "name": "GetCurrentPosition",
              "input": ["void"],
              "output": ["Position"]
            }
          ],
          "events": [
            {
              "event_id": "0x8001",
              "name": "PositionUpdated",
              "type": "Position",
              "cycle_time_ms": 100
            }
          ],
          "transport": {
            "protocol": "udp",
            "port": 30501,
            "multicast": "239.0.1.1"
          }
        }
      ]
    }

**SOME/IP Message Format:**

::

    SOME/IP Header (16 bytes):
    ┌─────────────┬──────────┬─────────┬─────────────┬──────────┐
    │ Message ID  │ Length   │ Req ID  │ Protocol Ver│ Msg Type │
    │  (32 bits)  │ (32 bits)│(32 bits)│  (8 bits)   │ (8 bits) │
    └─────────────┴──────────┴─────────┴─────────────┴──────────┘
    
    Message ID = Service ID (16) + Method ID (16)
    Message Type: REQUEST (0x00), RESPONSE (0x80), NOTIFICATION (0x02)

**2. ara::exec - Execution Management**

Application lifecycle and process management.

.. code-block:: cpp

    #include <ara/exec/execution_client.h>
    
    class AdaptiveApplication {
    public:
        AdaptiveApplication() {
            exec_client_ = ara::exec::CreateExecutionClient();
        }
        
        // Application lifecycle
        void Initialize() {
            // Report application state
            exec_client_->ReportExecutionState(
                ara::exec::ExecutionState::kRunning
            );
            
            // Initialize services
            navigation_service_ = std::make_unique<NavigationServiceProvider>();
            
            // Start event loop
            event_loop_running_ = true;
        }
        
        void Run() {
            while (event_loop_running_) {
                // Process events
                ara::com::ProcessEvents();
                
                // Application logic
                ProcessNavigationData();
                
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        }
        
        void Shutdown() {
            exec_client_->ReportExecutionState(
                ara::exec::ExecutionState::kTerminating
            );
            
            // Cleanup
            navigation_service_.reset();
            event_loop_running_ = false;
        }
        
        // Function group state changes (vehicle modes)
        void OnFunctionGroupStateChange(
            ara::exec::FunctionGroup group,
            ara::exec::FunctionGroupState state
        ) {
            if (group == ara::exec::FunctionGroup::kDriving) {
                if (state == ara::exec::FunctionGroupState::kOn) {
                    // Enable driving-related navigation features
                    EnableRoutingFeatures();
                } else {
                    // Disable when vehicle parked
                    DisableRoutingFeatures();
                }
            }
        }
        
    private:
        std::unique_ptr<ara::exec::ExecutionClient> exec_client_;
        std::unique_ptr<NavigationServiceProvider> navigation_service_;
        bool event_loop_running_;
    };
    
    // Application main entry
    int main(int argc, char* argv[]) {
        AdaptiveApplication app;
        
        app.Initialize();
        app.Run();
        app.Shutdown();
        
        return 0;
    }

**Application Manifest (ARXML):**

.. code-block:: xml

    <APPLICATION-SW-COMPONENT-TYPE>
      <SHORT-NAME>NavigationApplication</SHORT-NAME>
      <PORTS>
        <P-PORT-PROTOTYPE>
          <SHORT-NAME>NavigationServicePort</SHORT-NAME>
          <PROVIDED-COM-SPECS>
            <PROVIDED-SERVICE-INSTANCE>
              <SERVICE-INTERFACE-REF>/Services/NavigationService</SERVICE-INTERFACE-REF>
            </PROVIDED-SERVICE-INSTANCE>
          </PROVIDED-COM-SPECS>
        </P-PORT-PROTOTYPE>
      </PORTS>
    </APPLICATION-SW-COMPONENT-TYPE>
    
    <PROCESS>
      <SHORT-NAME>NavigationProcess</SHORT-NAME>
      <EXECUTABLE-REF>/Executables/navigation_app</EXECUTABLE-REF>
      <STATE-DEPENDENT-STARTUP-CONFIGS>
        <STATE-DEPENDENT-STARTUP-CONFIG>
          <FUNCTION-GROUP-STATE-REF>/FunctionGroups/Driving/On</FUNCTION-GROUP-STATE-REF>
          <STARTUP-CONFIG>
            <SCHEDULING-POLICY>SCHED_FIFO</SCHEDULING-POLICY>
            <PRIORITY>50</PRIORITY>
          </STARTUP-CONFIG>
        </STATE-DEPENDENT-STARTUP-CONFIG>
      </STATE-DEPENDENT-STARTUP-CONFIGS>
    </PROCESS>

**3. ara::per - Persistency (Key-Value Storage)**

.. code-block:: cpp

    #include <ara/per/key_value_storage.h>
    
    class NavigationPersistency {
    public:
        NavigationPersistency() {
            // Open key-value storage
            kv_storage_ = ara::per::OpenKeyValueStorage("NavigationStorage");
        }
        
        // Store last known position
        void SaveLastPosition(const Position& pos) {
            ara::per::KeyValuePair kvp;
            kvp.key = "LastPosition";
            
            // Serialize position
            kvp.value.resize(sizeof(Position));
            memcpy(kvp.value.data(), &pos, sizeof(Position));
            
            kv_storage_->SetValue(kvp);
            kv_storage_->SyncToStorage();  // Commit to persistent storage
        }
        
        // Restore position after restart
        Position LoadLastPosition() {
            auto result = kv_storage_->GetValue("LastPosition");
            
            if (result.has_value()) {
                Position pos;
                memcpy(&pos, result.value().data(), sizeof(Position));
                return pos;
            }
            
            // Return default if not found
            return {0.0, 0.0};
        }
        
    private:
        std::unique_ptr<ara::per::KeyValueStorage> kv_storage_;
    };

**4. ara::log - Logging**

.. code-block:: cpp

    #include <ara/log/logger.h>
    
    class NavigationLogger {
    public:
        NavigationLogger() {
            logger_ = ara::log::CreateLogger("NAV", "Navigation Context");
        }
        
        void LogPositionUpdate(const Position& pos) {
            logger_.LogInfo() << "Position updated: "
                              << "Lat=" << pos.latitude
                              << ", Lon=" << pos.longitude;
        }
        
        void LogError(const std::string& error_msg) {
            logger_.LogError() << "Navigation error: " << error_msg;
        }
        
    private:
        ara::log::Logger logger_;
    };

**5. ara::phm - Platform Health Management**

.. code-block:: cpp

    #include <ara/phm/health_channel.h>
    
    class NavigationHealthMonitor {
    public:
        NavigationHealthMonitor() {
            health_channel_ = ara::phm::CreateHealthChannel("NavigationHealth");
        }
        
        void MonitorGpsSensorHealth() {
            auto gps_status = gps_driver_->GetStatus();
            
            if (gps_status == GPS_NO_FIX) {
                // Report degraded health
                health_channel_->ReportCheckpoint(
                    ara::phm::HealthStatus::kFailed,
                    "GPS_NO_FIX"
                );
            } else if (gps_status == GPS_LOW_ACCURACY) {
                health_channel_->ReportCheckpoint(
                    ara::phm::HealthStatus::kDegraded,
                    "GPS_LOW_ACCURACY"
                );
            } else {
                health_channel_->ReportCheckpoint(
                    ara::phm::HealthStatus::kOk,
                    "GPS_HEALTHY"
                );
            }
        }
        
    private:
        std::unique_ptr<ara::phm::HealthChannel> health_channel_;
    };

**6. ara::diag - Diagnostics (UDS)**

.. code-block:: cpp

    #include <ara/diag/diagnostic_server.h>
    
    class NavigationDiagnostics {
    public:
        NavigationDiagnostics() {
            diag_server_ = ara::diag::CreateDiagnosticServer();
            
            // Register DTC (Diagnostic Trouble Code)
            diag_server_->RegisterDTC(
                0x123456,  // DTC ID
                "GPS Sensor Failure",
                ara::diag::DTCSeverity::kMedium
            );
        }
        
        // Set DTC when GPS fails
        void ReportGpsFailure() {
            diag_server_->SetDTC(
                0x123456,
                ara::diag::DTCStatus::kTestFailed
            );
        }
        
        // Clear DTC when GPS recovers
        void ClearGpsFailure() {
            diag_server_->SetDTC(
                0x123456,
                ara::diag::DTCStatus::kTestPassed
            );
        }
        
    private:
        std::unique_ptr<ara::diag::DiagnosticServer> diag_server_;
    };

CAN Communication (ISO 11898)
--------------------------------------------------------------------------------

**CAN Frame Definition:**

.. code-block:: cpp

    #include <ara/com/can/can_frame.h>
    
    // CAN frame structure
    struct BatteryStatusFrame {
        uint8_t state_of_charge;      // 0-100%
        uint16_t voltage_mv;          // Battery voltage in mV
        int16_t current_ma;           // Current in mA (signed)
        uint8_t temperature;          // Temperature in °C
        uint8_t error_flags;
    } __attribute__((packed));
    
    // CAN ID: 0x300 (Battery Status)
    void SendBatteryStatus(const BatteryStatusFrame& status) {
        ara::com::can::CanFrame frame;
        frame.can_id = 0x300;
        frame.dlc = sizeof(BatteryStatusFrame);
        memcpy(frame.data, &status, frame.dlc);
        
        can_interface_->Send(frame);
    }

**CAN Configuration (SAE J1939 for E-Bike):**

.. code-block:: cpp

    // J1939 Parameter Group Number (PGN) definitions
    #define PGN_BATTERY_STATUS     0xF004
    #define PGN_MOTOR_CONTROL      0xF005
    #define PGN_VEHICLE_SPEED      0xFEF1
    
    // J1939 CAN ID format (29-bit extended):
    // Priority (3) | Reserved (1) | Data Page (1) | PDU Format (8) | 
    // PDU Specific (8) | Source Address (8)
    
    uint32_t j1939_compose_can_id(uint8_t priority, uint16_t pgn, uint8_t src_addr) {
        uint32_t can_id = 0;
        can_id |= (priority & 0x07) << 26;
        can_id |= (pgn & 0x3FFFF) << 8;
        can_id |= (src_addr & 0xFF);
        return can_id | 0x80000000;  // Extended frame bit
    }

Network Management
--------------------------------------------------------------------------------

**Function Groups (Vehicle Modes):**

.. code-block:: xml

    <FUNCTION-GROUPS>
      <FUNCTION-GROUP>
        <SHORT-NAME>Parking</SHORT-NAME>
        <FUNCTION-GROUP-STATES>
          <FUNCTION-GROUP-STATE>
            <SHORT-NAME>On</SHORT-NAME>
            <PROCESSES>
              <PROCESS-REF>/Processes/TelematicsProcess</PROCESS-REF>
              <PROCESS-REF>/Processes/HMIProcess</PROCESS-REF>
            </PROCESSES>
          </FUNCTION-GROUP-STATE>
        </FUNCTION-GROUP-STATES>
      </FUNCTION-GROUP>
      
      <FUNCTION-GROUP>
        <SHORT-NAME>Driving</SHORT-NAME>
        <FUNCTION-GROUP-STATES>
          <FUNCTION-GROUP-STATE>
            <SHORT-NAME>On</SHORT-NAME>
            <PROCESSES>
              <PROCESS-REF>/Processes/NavigationProcess</PROCESS-REF>
              <PROCESS-REF>/Processes/HMIProcess</PROCESS-REF>
              <PROCESS-REF>/Processes/TelematicsProcess</PROCESS-REF>
            </PROCESSES>
          </FUNCTION-GROUP-STATE>
        </FUNCTION-GROUP-STATES>
      </FUNCTION-GROUP>
    </FUNCTION-GROUPS>

ISO 26262 Functional Safety
--------------------------------------------------------------------------------

**ASIL-B Compliance for Infotainment:**

**Safety Mechanisms:**
1. **Watchdog Monitoring:** ara::phm health channels
2. **Memory Protection:** POSIX process isolation
3. **Communication CRC:** SOME/IP E2E protection
4. **Fault Detection:** DTC reporting via ara::diag

**E2E (End-to-End) Protection:**

.. code-block:: cpp

    #include <ara/com/e2e/e2e_profile.h>
    
    // E2E Profile 4 (CRC32, Counter, DataID)
    class E2EProtectedNavigation {
    public:
        void SendProtectedPosition(const Position& pos) {
            ara::com::e2e::E2EProfile4 e2e_profile;
            
            // Serialize data
            std::vector<uint8_t> data = SerializePosition(pos);
            
            // Add E2E protection (CRC + Counter)
            e2e_profile.Protect(data, counter_++);
            
            // Send over SOME/IP
            navigation_service_->SendPosition(data);
        }
        
        bool ReceiveProtectedPosition(Position& pos) {
            auto data = navigation_service_->ReceivePosition();
            
            // Check E2E protection
            ara::com::e2e::E2EProfile4 e2e_profile;
            auto result = e2e_profile.Check(data, counter_);
            
            if (result == ara::com::e2e::E2EStatus::kOk) {
                pos = DeserializePosition(data);
                counter_++;
                return true;
            } else {
                // E2E check failed (corruption or lost message)
                return false;
            }
        }
        
    private:
        uint8_t counter_ = 0;
    };

================================================================================
AUTOSAR Classic Platform - Battery Management System
================================================================================

Project Overview
--------------------------------------------------------------------------------

**System:** Battery Management & Motor Control for E-Bike
**Hardware:** NXP Kinetis K5x (ARM Cortex-M4)
**OS:** AUTOSAR OS (OSEK-compliant)
**Network:** CAN (ISO 11898)
**Standards:** ISO 26262 ASIL-C, UL 2580, SAE J1939

**AUTOSAR Classic Architecture:**

::

    ┌─────────────────────────────────────────────────────────────┐
    │               Application Layer (SWC)                       │
    ├──────────┬────────────┬───────────┬───────────┬────────────┤
    │   BMS    │   Motor    │  Cell     │   SOC     │  Charging  │
    │   SWC    │ Control SWC│ Balance   │ Estimator │  Control   │
    └────┬─────┴──────┬─────┴─────┬─────┴─────┬─────┴──────┬─────┘
         │            │           │           │            │
    ┌────▼────────────▼───────────▼───────────▼────────────▼─────┐
    │          Runtime Environment (RTE)                          │
    │   (Inter-SWC Communication & BSW Interface)                │
    └─────────────────────────────────────────────────────────────┘
         │            │           │           │            │
    ┌────▼────────────▼───────────▼───────────▼────────────▼─────┐
    │              Basic Software (BSW)                           │
    ├──────────────────────────────────────────────────────────────┤
    │  Services: NvM, EcuM, Com, CSM, WdgM, Det, SchM           │
    │  ECU Abstraction: CanIf, AdcIf, MemIf                      │
    │  MCAL: Can, Adc, Pwm, Dio, Spi, Gpt, Wdg, Mcu, Port       │
    │  Complex Drivers: Battery Monitor, Motor Driver            │
    └─────────────────────────────────────────────────────────────┘
         │
    ┌────▼─────────────────────────────────────────────────────────┐
    │  Hardware: Kinetis K5x (Cortex-M4, CAN, ADC, PWM, GPIOs)  │
    └─────────────────────────────────────────────────────────────┘

Application Layer - Software Components (SWC)
--------------------------------------------------------------------------------

**1. BMS SWC (Battery Management Software Component)**

.. code-block:: c

    // BMS_Swc.c - Application Software Component
    
    #include "Rte_BMS_Swc.h"
    
    // Runnable: BMS_Main (10ms cyclic task)
    void BMS_Main_Runnable(void) {
        // Read cell voltages via RTE
        uint16_t cell_voltages[96];  // 96S configuration
        for (int i = 0; i < 96; i++) {
            Rte_Read_CellVoltage_Port(i, &cell_voltages[i]);
        }
        
        // Read total current
        int16_t current_ma;
        Rte_Read_BatteryCurrent_Port(&current_ma);
        
        // Read temperature sensors
        int8_t cell_temps[24];  // 24 temp sensors
        for (int i = 0; i < 24; i++) {
            Rte_Read_CellTemperature_Port(i, &cell_temps[i]);
        }
        
        // Calculate SOC (State of Charge)
        float soc = BMS_CalculateSOC(cell_voltages, current_ma);
        
        // Calculate SOH (State of Health)
        float soh = BMS_CalculateSOH(cell_voltages, cell_temps);
        
        // Cell balancing decision
        bool balance_enable[96];
        BMS_CellBalancing(cell_voltages, balance_enable);
        
        // Write outputs via RTE
        Rte_Write_SOC_Port(soc);
        Rte_Write_SOH_Port(soh);
        
        for (int i = 0; i < 96; i++) {
            Rte_Write_BalanceControl_Port(i, balance_enable[i]);
        }
        
        // Safety checks
        if (BMS_CheckOverVoltage(cell_voltages)) {
            Rte_Call_DiagnosticMonitor_SetEventStatus(
                DEM_EVENT_BMS_OVERVOLTAGE,
                DEM_EVENT_STATUS_FAILED
            );
            Rte_Write_SafetyShutdown_Port(TRUE);
        }
        
        if (BMS_CheckOverTemperature(cell_temps)) {
            Rte_Call_DiagnosticMonitor_SetEventStatus(
                DEM_EVENT_BMS_OVERTEMP,
                DEM_EVENT_STATUS_FAILED
            );
            Rte_Write_SafetyShutdown_Port(TRUE);
        }
    }
    
    // SOC Calculation using Coulomb Counting + OCV
    float BMS_CalculateSOC(uint16_t cell_voltages[], int16_t current_ma) {
        static float soc_coulomb = 100.0f;  // Start at 100%
        static uint32_t last_timestamp = 0;
        
        uint32_t current_timestamp = GetSystemTime_ms();
        float delta_time_h = (current_timestamp - last_timestamp) / 3600000.0f;
        
        // Coulomb counting: ΔSOC = (I * Δt) / Capacity
        float capacity_ah = 20.0f;  // 20 Ah battery
        float delta_soc = (current_ma / 1000.0f) * delta_time_h / capacity_ah * 100.0f;
        soc_coulomb -= delta_soc;  // Negative current = discharging
        
        // OCV (Open Circuit Voltage) calibration
        float ocv = CalculateOCV(cell_voltages);
        float soc_ocv = OCV_to_SOC_LookupTable(ocv);
        
        // Kalman filter fusion
        float soc_estimate = KalmanFilter(soc_coulomb, soc_ocv);
        
        last_timestamp = current_timestamp;
        return soc_estimate;
    }

**2. Motor Control SWC**

.. code-block:: c

    // MotorCtrl_Swc.c
    
    #include "Rte_MotorCtrl_Swc.h"
    
    // Runnable: MotorCtrl_Main (1ms cyclic - FOC loop)
    void MotorCtrl_Main_Runnable(void) {
        // Read throttle position (0-100%)
        uint8_t throttle_position;
        Rte_Read_ThrottlePosition_Port(&throttle_position);
        
        // Read motor phase currents (Ia, Ib, Ic)
        int16_t current_a, current_b, current_c;
        Rte_Read_PhaseCurrent_A_Port(&current_a);
        Rte_Read_PhaseCurrent_B_Port(&current_b);
        Rte_Read_PhaseCurrent_C_Port(&current_c);
        
        // Read rotor position (Hall sensors or encoder)
        uint16_t rotor_position;
        Rte_Read_RotorPosition_Port(&rotor_position);
        
        // Calculate electrical angle
        float theta_e = RotorPositionToElectricalAngle(rotor_position);
        
        // Clarke Transform: abc → αβ
        float i_alpha, i_beta;
        ClarkeTra nsform(current_a, current_b, current_c, &i_alpha, &i_beta);
        
        // Park Transform: αβ → dq (rotating frame)
        float i_d, i_q;
        ParkTransform(i_alpha, i_beta, theta_e, &i_d, &i_q);
        
        // PI Controllers for d-q currents
        float i_d_ref = 0.0f;  // Field weakening (0 for SPMSM)
        float i_q_ref = ThrottleToTorqueCurrent(throttle_position);
        
        float v_d = PI_Controller_D(i_d_ref, i_d);
        float v_q = PI_Controller_Q(i_q_ref, i_q);
        
        // Inverse Park Transform: dq → αβ
        float v_alpha, v_beta;
        InverseParkTransform(v_d, v_q, theta_e, &v_alpha, &v_beta);
        
        // Space Vector Modulation (SVM)
        uint16_t pwm_duty_a, pwm_duty_b, pwm_duty_c;
        SpaceVectorModulation(v_alpha, v_beta, &pwm_duty_a, &pwm_duty_b, &pwm_duty_c);
        
        // Write PWM duty cycles via RTE
        Rte_Write_PWM_PhaseA_Port(pwm_duty_a);
        Rte_Write_PWM_PhaseB_Port(pwm_duty_b);
        Rte_Write_PWM_PhaseC_Port(pwm_duty_c);
    }

**3. Cell Balancing SWC**

.. code-block:: c

    // CellBalance_Swc.c
    
    void CellBalance_Main_Runnable(void) {
        uint16_t cell_voltages[96];
        
        // Read all cell voltages
        for (int i = 0; i < 96; i++) {
            Rte_Read_CellVoltage_Port(i, &cell_voltages[i]);
        }
        
        // Find maximum voltage
        uint16_t max_voltage = 0;
        for (int i = 0; i < 96; i++) {
            if (cell_voltages[i] > max_voltage) {
                max_voltage = cell_voltages[i];
            }
        }
        
        // Balance threshold: 10mV
        const uint16_t BALANCE_THRESHOLD_MV = 10;
        
        // Enable balancing for cells above threshold
        for (int i = 0; i < 96; i++) {
            if ((max_voltage - cell_voltages[i]) > BALANCE_THRESHOLD_MV) {
                Rte_Write_BalanceEnable_Port(i, TRUE);
            } else {
                Rte_Write_BalanceEnable_Port(i, FALSE);
            }
        }
    }

Runtime Environment (RTE)
--------------------------------------------------------------------------------

**RTE Generation (from ARXML)**

The RTE is automatically generated from Software Component Description (ARXML).

**Example RTE API:**

.. code-block:: c

    // Rte_BMS_Swc.h (Auto-generated)
    
    // Sender-Receiver Interface
    Std_ReturnType Rte_Read_BMS_Swc_CellVoltage_Port(uint8_t cell_id, uint16_t *data);
    Std_ReturnType Rte_Write_BMS_Swc_SOC_Port(float data);
    
    // Client-Server Interface
    Std_ReturnType Rte_Call_BMS_Swc_DiagnosticMonitor_SetEventStatus(
        Dem_EventIdType EventId,
        Dem_EventStatusType EventStatus
    );
    
    // Mode Switch Interface
    Std_ReturnType Rte_Mode_BMS_Swc_BmsMode_Mode(Rte_ModeType_BmsMode *mode);
    
    // Trigger Interface
    Std_ReturnType Rte_Trigger_BMS_Swc_SafetyShutdown_Event(void);

**RTE Mapping:**

::

    BMS_SWC.SOC_Port  →  RTE  →  MotorCtrl_SWC.BatterySOC_Port
         (write)                        (read)
    
    Mapped via ARXML:
    <SENDER-RECEIVER-TO-SIGNAL-MAPPING>
      <DATA-ELEMENT-IREF>
        <PORT-REF>/BMS_Swc/SOC_Port</PORT-REF>
      </DATA-ELEMENT-IREF>
      <SYSTEM-SIGNAL-REF>/Signals/SOC_Signal</SYSTEM-SIGNAL-REF>
    </SENDER-RECEIVER-TO-SIGNAL-MAPPING>

Basic Software (BSW) - Services Layer
--------------------------------------------------------------------------------

**1. NvM (Non-Volatile Memory Manager)**

.. code-block:: c

    // Store SOC to EEPROM before shutdown
    void BMS_ShutdownHandler(void) {
        float current_soc;
        Rte_Read_SOC_Port(&current_soc);
        
        // Write to NvM block
        NvM_WriteBlock(NvM_BlockId_BMS_SOC, &current_soc);
        
        // Wait for write to complete
        NvM_RequestResultType result;
        do {
            NvM_GetErrorStatus(NvM_BlockId_BMS_SOC, &result);
        } while (result == NVM_REQ_PENDING);
    }
    
    // Restore SOC after startup
    void BMS_StartupHandler(void) {
        float restored_soc;
        
        NvM_ReadBlock(NvM_BlockId_BMS_SOC, &restored_soc);
        
        NvM_RequestResultType result;
        NvM_GetErrorStatus(NvM_BlockId_BMS_SOC, &result);
        
        if (result == NVM_REQ_OK) {
            Rte_Write_SOC_Port(restored_soc);
        } else {
            // Use default value
            Rte_Write_SOC_Port(100.0f);
        }
    }

**2. DEM (Diagnostic Event Manager)**

.. code-block:: c

    // DEM Configuration (Dem_Cfg.c)
    const Dem_EventParameterType Dem_EventParameter[] = {
        // EventId, Priority, EventKind, Storage
        { DEM_EVENT_BMS_OVERVOLTAGE,  1, DEM_EVENT_KIND_BSW, DEM_DTC_ORIGIN_PRIMARY_MEMORY },
        { DEM_EVENT_BMS_OVERTEMP,     1, DEM_EVENT_KIND_BSW, DEM_DTC_ORIGIN_PRIMARY_MEMORY },
        { DEM_EVENT_MOTOR_OVERCURRENT,2, DEM_EVENT_KIND_BSW, DEM_DTC_ORIGIN_PRIMARY_MEMORY },
    };
    
    // Report event from application
    void BMS_ReportOverVoltage(uint8_t cell_id) {
        // Set event status
        Dem_SetEventStatus(DEM_EVENT_BMS_OVERVOLTAGE, DEM_EVENT_STATUS_PREFAILED);
        
        // Store freeze frame data
        uint16_t cell_voltage;
        Rte_Read_CellVoltage_Port(cell_id, &cell_voltage);
        
        Dem_FreezeFrameDataType freeze_data;
        freeze_data.cell_id = cell_id;
        freeze_data.voltage = cell_voltage;
        
        Dem_SetFreezeFrameData(DEM_EVENT_BMS_OVERVOLTAGE, &freeze_data);
    }

**3. DCM (Diagnostic Communication Manager) - UDS**

.. code-block:: c

    // UDS Service 0x22: Read Data By Identifier
    Std_ReturnType Dcm_ReadDataByIdentifier_SOC(
        uint8_t *data,
        uint16_t *dataLength
    ) {
        float soc;
        Rte_Read_SOC_Port(&soc);
        
        // Convert SOC to percentage (0-100)
        data[0] = (uint8_t)soc;
        *dataLength = 1;
        
        return E_OK;
    }
    
    // UDS Service 0x31: Routine Control (Cell Balancing)
    Std_ReturnType Dcm_RoutineControl_StartCellBalancing(
        const uint8_t *requestData,
        uint16_t requestDataLength,
        uint8_t *responseData,
        uint16_t *responseDataLength
    ) {
        // Start cell balancing manually
        Rte_Call_CellBalance_Start();
        
        responseData[0] = 0x00;  // Success
        *responseDataLength = 1;
        
        return E_OK;
    }

**4. Com (Communication Manager) - CAN**

.. code-block:: c

    // Com_Cfg.c - CAN Signal Configuration
    const Com_SignalType Com_Signal_BatterySOC = {
        .ComHandleId = 1,
        .ComBitPosition = 0,
        .ComBitSize = 8,
        .ComSignalEndianness = COM_BIG_ENDIAN,
        .ComSignalType = UINT8,
        .ComTransferProperty = COM_TRIGGERED,
    };
    
    // Com_Cfg.c - CAN PDU (Protocol Data Unit)
    const Com_IpduType Com_Ipdu_BatteryStatus = {
        .ComIPduHandleId = 0x300,
        .ComIPduDirection = COM_SEND,
        .ComIPduType = COM_NORMAL,
        .ComTxIPduMinimumDelayTime = 10,  // 10ms minimum gap
    };
    
    // Application sends signal
    void BMS_SendCANStatus(void) {
        float soc;
        Rte_Read_SOC_Port(&soc);
        
        uint8_t soc_percent = (uint8_t)soc;
        Com_SendSignal(Com_Signal_BatterySOC, &soc_percent);
        
        // Trigger PDU transmission
        Com_TriggerIPDUSend(Com_Ipdu_BatteryStatus);
    }

**5. CanTp (CAN Transport Protocol) - ISO 15765-2**

Multi-frame transmission for diagnostic data.

.. code-block:: c

    // Long diagnostic response (> 8 bytes) using ISO-TP
    
    // Single Frame: Length <= 7 bytes
    // [0x0N] [Data...] where N = length
    
    // First Frame: Length > 7 bytes
    // [0x1L LL] [Data 0-5] where LLL = total length
    
    // Consecutive Frames:
    // [0x2N] [Data...] where N = sequence number (0-15)
    
    // Flow Control Frame:
    // [0x30] [BS] [STmin]
    //   BS = Block Size
    //   STmin = Minimum separation time
    
    void CanTp_TxConfirmation(PduIdType TxPduId) {
        // Multi-frame transmission confirmed
    }

Basic Software (BSW) - MCAL (Microcontroller Abstraction Layer)
--------------------------------------------------------------------------------

**1. Adc (Analog-to-Digital Converter)**

.. code-block:: c

    // Adc_Cfg.c - ADC Configuration for cell voltages
    const Adc_ConfigType AdcConfig = {
        .AdcChannelConfig = {
            // Cell voltage channels (96 channels via multiplexer)
            { ADC_CHANNEL_0, ADC_GROUP_CELL_VOLTAGE, 12 },  // 12-bit resolution
            { ADC_CHANNEL_1, ADC_GROUP_CELL_VOLTAGE, 12 },
            // ... (96 total)
        },
        .AdcSampleTime = ADC_SAMPLE_TIME_15_CYCLES,
        .AdcResolution = ADC_RESOLUTION_12_BIT,
    };
    
    // Read cell voltage
    uint16_t ReadCellVoltage(uint8_t cell_id) {
        Adc_StatusType status;
        Adc_ValueGroupType adc_value;
        
        // Start ADC conversion
        Adc_StartGroupConversion(ADC_GROUP_CELL_VOLTAGE);
        
        // Wait for completion
        do {
            status = Adc_GetGroupStatus(ADC_GROUP_CELL_VOLTAGE);
        } while (status != ADC_COMPLETED);
        
        // Read result
        Adc_ReadGroup(ADC_GROUP_CELL_VOLTAGE, &adc_value);
        
        // Convert ADC value to voltage (mV)
        // ADC range: 0-4095 (12-bit) maps to 0-5000mV
        uint16_t voltage_mv = (adc_value[cell_id] * 5000) / 4095;
        
        return voltage_mv;
    }

**2. Pwm (Pulse Width Modulation) - Motor Control**

.. code-block:: c

    // Pwm_Cfg.c - Three-phase PWM for BLDC motor
    const Pwm_ConfigType PwmConfig = {
        .PwmChannels = {
            { PWM_CHANNEL_PHASE_A, 20000, 50 },  // 20kHz, 50% initial duty
            { PWM_CHANNEL_PHASE_B, 20000, 50 },
            { PWM_CHANNEL_PHASE_C, 20000, 50 },
        },
        .PwmPeriod = 20000,  // 20 kHz (50us period)
        .PwmDeadTime = 2,    // 2us dead time (prevent shoot-through)
    };
    
    // Set motor PWM duty cycles (0-100%)
    void SetMotorPWM(uint8_t duty_a, uint8_t duty_b, uint8_t duty_c) {
        // Convert percentage to timer ticks
        uint16_t duty_ticks_a = (duty_a * PWM_PERIOD_TICKS) / 100;
        uint16_t duty_ticks_b = (duty_b * PWM_PERIOD_TICKS) / 100;
        uint16_t duty_ticks_c = (duty_c * PWM_PERIOD_TICKS) / 100;
        
        Pwm_SetDutyCycle(PWM_CHANNEL_PHASE_A, duty_ticks_a);
        Pwm_SetDutyCycle(PWM_CHANNEL_PHASE_B, duty_ticks_b);
        Pwm_SetDutyCycle(PWM_CHANNEL_PHASE_C, duty_ticks_c);
    }

**3. Can Driver**

.. code-block:: c

    // Can_Cfg.c - CAN Configuration
    const Can_ConfigType CanConfig = {
        .CanControllers = {
            {
                .CanControllerId = 0,
                .CanBaudRate = 500,  // 500 kbps
                .CanPropSeg = 5,
                .CanPhase Seg1 = 6,
                .CanPhaseSeg2 = 4,
                .CanSyncJumpWidth = 1,
            }
        },
        .CanHardwareObjects = {
            { CAN_HOH_TX_BATTERY_STATUS, CAN_TRANSMIT, 0x300 },
            { CAN_HOH_TX_MOTOR_STATUS,   CAN_TRANSMIT, 0x301 },
            { CAN_HOH_RX_CHARGE_CMD,     CAN_RECEIVE,  0x400 },
        }
    };

Model-Based Development (Simulink/Stateflow)
--------------------------------------------------------------------------------

**Simulink Model for SOC Estimation:**

.. code-block:: matlab

    % Simulink Model: SOC_Estimator.slx
    
    % Inputs:
    % - Cell Voltages [1x96 vector]
    % - Battery Current [scalar, mA]
    % - Temperature [1x24 vector]
    
    % Algorithm: Extended Kalman Filter (EKF)
    
    % State vector: x = [SOC, R0, R1, C1]'
    % - SOC: State of Charge
    % - R0: Series resistance
    % - R1, C1: RC network (battery dynamics)
    
    % Measurement: Terminal voltage
    % V_terminal = OCV(SOC) - I*R0 - V_RC
    
    % Code generation settings:
    % - Target: Embedded Coder for AUTOSAR
    % - Generate: RTE-compliant C code
    % - Optimization: Speed (real-time constraints)

**Automatic Code Generation:**

.. code-block:: bash

    # Generate AUTOSAR-compliant C code
    >> Simulink.BlockDiagram.buildTarget('SOC_Estimator', 'AUTOSAR_Coder')
    
    # Generated files:
    # - SOC_Estimator.c/h
    # - Rte_SOC_Estimator.c/h (RTE interface)
    # - SOC_Estimator_ARXML (AUTOSAR XML)

**Model-in-Loop (MIL) Testing:**

.. code-block:: matlab

    % Test harness for SOC estimator
    load('battery_drive_cycle.mat');  % Load test data
    
    % Simulate Simulink model
    sim('SOC_Estimator');
    
    % Validate output
    assert(max(abs(SOC_error)) < 2.0, 'SOC error > 2%');

ISO 26262 ASIL-C Compliance
--------------------------------------------------------------------------------

**Safety Mechanisms:**

**1. Watchdog Monitoring (WdgM)**

.. code-block:: c

    // WdgM_Cfg.c - Watchdog Configuration
    const WdgM_ConfigType WdgMConfig = {
        .WdgMSupervisedEntity = {
            {
                .WdgMSupervisedEntityId = SE_BMS_MAIN,
                .WdgMCheckpointId = { CP_BMS_START, CP_BMS_END },
                .WdgMExpectedAliveIndications = 100,  // 10ms * 100 = 1s timeout
            }
        }
    };
    
    // Application reports checkpoints
    void BMS_Main_Runnable(void) {
        WdgM_CheckpointReached(SE_BMS_MAIN, CP_BMS_START);
        
        // Main BMS logic
        // ...
        
        WdgM_CheckpointReached(SE_BMS_MAIN, CP_BMS_END);
    }

**2. E2E Protection (Com)**

.. code-block:: c

    // CAN message with E2E protection (CRC + Alive Counter)
    typedef struct {
        uint8_t soc;              // State of Charge
        uint16_t voltage;         // Battery voltage
        int16_t current;          // Battery current
        uint8_t alive_counter;   // Rolling counter (0-15)
        uint8_t crc8;            // CRC-8
    } BatteryStatusMessage_t;
    
    void SendBatteryStatus_E2E(BatteryStatusMessage_t *msg) {
        // Increment alive counter
        static uint8_t counter = 0;
        msg->alive_counter = counter++;
        counter &= 0x0F;  // Wrap at 15
        
        // Calculate CRC-8
        msg->crc8 = E2E_CalculateCRC8(msg, sizeof(*msg) - 1);
        
        // Send via Com
        Com_SendSignal(Com_Signal_BatteryStatus, msg);
    }

**3. Memory Protection (MPU)**

.. code-block:: c

    // Os_Cfg.c - Memory Protection Unit Configuration
    const Os_MpuRegionConfigType OsMpuRegions[] = {
        // Region 0: BMS code (Read/Execute only)
        {
            .BaseAddress = 0x00010000,
            .Size = 256 * 1024,  // 256 KB
            .AccessRights = MPU_READ | MPU_EXECUTE,
        },
        // Region 1: BMS data (Read/Write only)
        {
            .BaseAddress = 0x20000000,
            .Size = 64 * 1024,  // 64 KB
            .AccessRights = MPU_READ | MPU_WRITE,
        },
    };

**ASIL-C Requirements:**
- Hardware Fault Metrics: SPFM > 90%, LFM > 60%
- Software Safety Requirements: Verified with DO-178C-like rigor
- FMEA/FTA: Fault tree analysis for all safety goals
- Safety Validation: HIL testing with fault injection

Testing & Validation
--------------------------------------------------------------------------------

**Unit Testing (AUTOSAR compliant):**

.. code-block:: c

    // Test_BMS_Swc.c
    #include "unity.h"  // Unit test framework
    #include "Rte_BMS_Swc.h"
    
    void test_SOC_Calculation_Normal(void) {
        // Setup
        uint16_t cell_voltages[96];
        for (int i = 0; i < 96; i++) {
            cell_voltages[i] = 3700;  // 3.7V per cell (nominal)
        }
        int16_t current_ma = -5000;  // 5A discharge
        
        // Execute
        float soc = BMS_CalculateSOC(cell_voltages, current_ma);
        
        // Assert
        TEST_ASSERT_FLOAT_WITHIN(2.0, 50.0, soc);  // 50% ± 2%
    }

**Hardware-in-the-Loop (HIL) Testing:**

.. code-block:: python

    # HIL test script (dSPACE or Vector CANoe)
    import can
    import time
    
    # Open CAN bus
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # Test case: Battery charging scenario
    def test_charging_profile():
        # Send charge enable command
        msg = can.Message(arbitration_id=0x400,
                          data=[0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                          is_extended_id=False)
        bus.send(msg)
        
        # Monitor battery status messages (0x300)
        for i in range(100):
            msg = bus.recv(timeout=0.1)
            if msg.arbitration_id == 0x300:
                soc = msg.data[0]
                voltage = (msg.data[1] << 8) | msg.data[2]
                current = (msg.data[3] << 8) | msg.data[4]
                
                print(f"SOC: {soc}%, Voltage: {voltage}mV, Current: {current}mA")
                
                # Verify charging behavior
                assert current < 0, "Current should be negative (charging)"
                assert soc <= 100, "SOC should not exceed 100%"
            
            time.sleep(0.01)

Lessons Learned
--------------------------------------------------------------------------------

**AUTOSAR Adaptive Platform:**
✓ SOME/IP provides flexible service-oriented communication
✓ Yocto integration straightforward with proper ARA configuration
✓ Linux provides rich debugging tools (gdb, valgrind, perf)
✓ E2E protection essential for safety-critical data
✓ Function groups enable efficient power management

**AUTOSAR Classic Platform:**
✓ RTE abstracts BSW complexity from application
✓ Model-based development (Simulink) accelerates algorithm development
✓ MCAL drivers provide hardware independence
✓ ISO 26262 compliance requires extensive safety mechanisms
✓ CAN network management critical for multi-ECU systems

**Common Pitfalls:**
✗ Insufficient WCET analysis for high-priority tasks
✗ RTE configuration mismatches between SWCs
✗ CAN bus loading exceeding 70% (performance degradation)
✗ Missing E2E protection on safety-critical signals
✗ Inadequate NvM block sizes for data persistence

Tools Used
--------------------------------------------------------------------------------

- **Configuration:** Vector DaVinci Developer/Configurator
- **Code Generation:** Embedded Coder (Simulink), EB tresos Studio
- **Testing:** VectorCAST (unit tests), dSPACE (HIL), CANoe
- **Debugging:** Trace32 (Lauterbach), Segger J-Link
- **Compliance:** LDRA (DO-178C), Parasoft (MISRA C)

================================================================================
References
================================================================================

**Standards:**
- AUTOSAR Release R19-11 (Adaptive Platform)
- AUTOSAR Release R4.4.0 (Classic Platform)
- ISO 26262:2018 (Functional Safety)
- ISO 11898 (CAN Protocol)
- SAE J1939 (Heavy Duty Vehicle Network)
- ISO 15765-2 (CAN Transport Protocol)
- UL 2580 (Battery Safety)

**Vendors:**
- Vector Informatik (DaVinci, CANoe)
- ETAS (RTA-BSW, ISOLAR-A/B)
- Elektrobit (EB tresos)
- dSPACE (Scalexio, MicroAutoBox)

================================================================================
