
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


⭐ **Platform Health Management (PHM)** – Comprehensive cheatsheet for AUTOSAR Adaptive Platform Health Management (ara::phm) – Release R25-11, covering supervision strategies, checkpoint reporting, watchdog handling, recovery actions, and safety patterns.

📌 1. PHM Overview – Purpose & Architecture

**What is Platform Health Management?**

Platform Health Management (PHM) is a fundamental Adaptive AUTOSAR service that monitors the health of applications, processes, and system components. It provides:

- **Alive supervision** – Monitors if processes/threads are executing correctly via checkpoints
- **Deadline supervision** – Ensures timing constraints are met
- **Logical supervision** – Verifies correct execution flow and state transitions
- **Recovery actions** – Automatic fault handling (restart, shutdown, etc.)
- **Hardware watchdog integration** – Ensures system-level fault tolerance

| Aspect                    | Description                                              | Key API                        |
|---------------------------|----------------------------------------------------------|--------------------------------|
| **Namespace**             | ara::phm                                                 | All PHM APIs in ara::phm       |
| **Release**               | R25-11 (latest as of Jan 2026)                           | Removed Health Channel concept |
| **Primary Use**           | Safety-critical supervision, ASIL-B/D applications       | Checkpoint reporting           |
| **Integration**           | Works with Execution Management (ara::exec)              | Auto-start/stop supervision    |

📌 2. Core PHM Concepts

⭐ **2.1 Supervised Entity**

A Supervised Entity is any application, process, or functional component that requires health monitoring.

.. code-block:: cpp

    // Each Supervised Entity has:
    // - Unique identifier
    // - Set of Checkpoints
    // - Supervision configuration (alive, deadline, logical)
    // - Recovery action specification

**2.2 Checkpoint**

A Checkpoint is a reporting point in code where the application signals its health status to PHM.

⭐ .. code-block:: cpp

    #include <ara/phm/supervised_entity.h>
    
    // Report checkpoint - indicates application is alive and progressing
    auto se = ara::phm::SupervisedEntity::GetInstance();
    se->ReportCheckpoint(ara::phm::CheckpointId::kMainLoopCheckpoint);

**2.3 Supervision Types**

| Supervision Type          | Purpose                                           | Configuration Elements                     |
|---------------------------|---------------------------------------------------|--------------------------------------------|
| **Alive Supervision**     | Verifies process/thread is executing              | Expected alive period, tolerance           |
| **Deadline Supervision**  | Ensures checkpoints are reported within deadline  | Max deadline, checkpoint sequence          |
| **Logical Supervision**   | Validates correct execution flow/state machine    | Valid checkpoint sequences, transitions    |

⭐ **2.4 Elementary vs Global Supervision**

- **Elementary Supervision** – Individual supervision instance for one Supervised Entity
- **Global Supervision Status** – Aggregated status across all supervised entities in the system

📌 3. PHM API Reference (R25-11)

⭐ **3.1 SupervisedEntity Class**

.. code-block:: cpp

    namespace ara::phm {
    
    class SupervisedEntity {
    public:
        // Get instance for current process/application
        static core::Result<SupervisedEntity> GetInstance() noexcept;
        
        // Report checkpoint - alive indication
        core::Result<void> ReportCheckpoint(CheckpointId checkpoint) noexcept;
        
        // Get current supervision status
        core::Result<SupervisionStatus> GetStatus() noexcept;
        
        // Stop supervision (graceful shutdown)
        core::Result<void> StopSupervision() noexcept;
    };
    
    } // namespace ara::phm

**3.2 CheckpointId**

.. code-block:: cpp

    // CheckpointId is a strongly-typed identifier
    enum class CheckpointId : uint32_t {
        kInitCheckpoint = 0,
        kMainLoopCheckpoint = 1,
        kShutdownCheckpoint = 2,
        // ... application-defined checkpoints
    };

⭐ **3.3 SupervisionStatus**

.. code-block:: cpp

    namespace ara::phm {
    
    enum class SupervisionStatus : uint8_t {
        kOk = 0,           // All supervisions passing
        kFailed = 1,       // At least one supervision failed
        kExpired = 2,      // Deadline expired
        kStopped = 3,      // Supervision stopped
        kDeactivated = 4   // Supervision deactivated at runtime
    };
    
    } // namespace ara::phm

**3.4 Recovery Actions**

⭐ .. code-block:: cpp

    namespace ara::phm {
    
    // Recovery action types configured in manifest
    enum class RecoveryAction : uint8_t {
        kNoAction = 0,              // Only log error
        kRestartProcess = 1,        // Restart the failed process
        kRestartMachine = 2,        // Reboot the entire machine
        kShutdownMachine = 3,       // Safe shutdown
        kCustomRecovery = 4         // Application-specific recovery
    };
    
    } // namespace ara::phm

📌 4. PHM Usage Patterns

⭐ **4.1 Basic Alive Supervision**

.. code-block:: cpp

    #include <ara/phm/supervised_entity.h>
    #include <ara/core/result.h>
    #include <thread>
    #include <chrono>
    
    class NavigationApplication {
    public:
        NavigationApplication() {
            // Get supervised entity instance
            auto result = ara::phm::SupervisedEntity::GetInstance();
            if (result.HasValue()) {
                supervised_entity_ = result.Value();
            }
        }
        
        void Run() {
            // Report initial checkpoint
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kInitCheckpoint);
            
            // Main application loop
            while (running_) {
                // Perform work
                ProcessNavigationData();
                
                // Report checkpoint periodically (e.g., every 100ms)
                supervised_entity_.ReportCheckpoint(
                    ara::phm::CheckpointId::kMainLoopCheckpoint);
                
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            
            // Report shutdown checkpoint
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kShutdownCheckpoint);
        }
        
    private:
        ara::phm::SupervisedEntity supervised_entity_;
        bool running_ = true;
    };

**4.2 Deadline Supervision Pattern**

.. code-block:: cpp

    class SensorFusionApp {
    public:
        void ProcessSensorData() {
            // Report start of critical section
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kSensorFusionStart);
            
            // Critical processing with deadline requirement
            auto start_time = std::chrono::steady_clock::now();
            
            FuseLidarAndRadar();
            
            auto elapsed = std::chrono::steady_clock::now() - start_time;
            
            // Report end checkpoint (must be within deadline)
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kSensorFusionEnd);
            
            // If deadline exceeded, PHM triggers recovery action
        }
    };

⭐ **4.3 Logical Supervision – State Machine Validation**

.. code-block:: cpp

    class ADASController {
    public:
        enum class State {
            kIdle,
            kActive,
            kDegraded,
            kEmergency
        };
        
        void TransitionTo(State new_state) {
            // Report state transitions to PHM for logical supervision
            switch (new_state) {
                case State::kIdle:
                    supervised_entity_.ReportCheckpoint(
                        ara::phm::CheckpointId::kStateIdle);
                    break;
                case State::kActive:
                    supervised_entity_.ReportCheckpoint(
                        ara::phm::CheckpointId::kStateActive);
                    break;
                case State::kDegraded:
                    supervised_entity_.ReportCheckpoint(
                        ara::phm::CheckpointId::kStateDegraded);
                    break;
                case State::kEmergency:
                    supervised_entity_.ReportCheckpoint(
                        ara::phm::CheckpointId::kStateEmergency);
                    break;
            }
            
            current_state_ = new_state;
            
            // PHM validates that state transitions follow configured sequence
            // Invalid transitions trigger recovery action
        }
        
    private:
        State current_state_ = State::kIdle;
        ara::phm::SupervisedEntity supervised_entity_;
    };

**4.4 Error Handling & Status Checking**

.. code-block:: cpp

    #include <ara/phm/phm_error_domain.h>
    
    void MonitorApplicationHealth() {
        auto se = ara::phm::SupervisedEntity::GetInstance().Value();
        
        // Check current supervision status
        auto status_result = se.GetStatus();
        
        if (status_result.HasValue()) {
            auto status = status_result.Value();
            
            switch (status) {
                case ara::phm::SupervisionStatus::kOk:
                    // All good
                    break;
                    
                case ara::phm::SupervisionStatus::kFailed:
                    // Supervision failed - recovery action will be triggered
                    LogError("Supervision failed!");
                    break;
                    
                case ara::phm::SupervisionStatus::kExpired:
                    // Deadline expired
                    LogError("Deadline supervision expired!");
                    break;
                    
                case ara::phm::SupervisionStatus::kStopped:
                    // Supervision stopped (graceful)
                    break;
                    
                case ara::phm::SupervisionStatus::kDeactivated:
                    // Supervision deactivated at runtime
                    break;
            }
        } else {
            // Handle error
            auto error = status_result.Error();
            if (error.Domain() == ara::phm::GetPhmErrorDomain()) {
                // PHM-specific error
                LogError("PHM error: " + error.Message());
            }
        }
    }

📌 5. Configuration & Manifest

⭐ **5.1 Supervised Entity Manifest (ARXML)**

.. code-block:: xml

    <SupervisedEntity>
        <shortName>NavigationApp</shortName>
        <identifier>NavApp_SE_001</identifier>
        
        <!-- Alive Supervision Configuration -->
        <aliveSupervision>
            <expectedAliveIndications>10</expectedAliveIndications>
            <expectedAliveCycle>100</expectedAliveCycle>  <!-- milliseconds -->
            <minMargin>10</minMargin>
            <maxMargin>20</maxMargin>
        </aliveSupervision>
        
        <!-- Deadline Supervision Configuration -->
        <deadlineSupervision>
            <checkpoint ref="/Checkpoints/SensorFusionStart"/>
            <checkpoint ref="/Checkpoints/SensorFusionEnd"/>
            <deadline>50</deadline>  <!-- milliseconds -->
        </deadlineSupervision>
        
        <!-- Recovery Action -->
        <recoveryAction>
            <actionType>RestartProcess</actionType>
            <delay>100</delay>  <!-- milliseconds -->
        </recoveryAction>
    </SupervisedEntity>

**5.2 Checkpoint Definition**

.. code-block:: xml

    <Checkpoint>
        <shortName>MainLoopCheckpoint</shortName>
        <checkpointId>1</checkpointId>
        <description>Reported every main loop iteration</description>
    </Checkpoint>

⭐ **5.3 Supervision Mode Configuration**

.. code-block:: xml

    <SupervisionMode>
        <shortName>NormalMode</shortName>
        <supervisions>
            <supervisionRef ref="/Supervisions/AliveSupervision_Nav"/>
            <supervisionRef ref="/Supervisions/DeadlineSupervision_Sensor"/>
        </supervisions>
    </SupervisionMode>
    
    <SupervisionMode>
        <shortName>DegradedMode</shortName>
        <supervisions>
            <!-- Relaxed supervision in degraded mode -->
            <supervisionRef ref="/Supervisions/AliveSupervision_Nav_Relaxed"/>
        </supervisions>
    </SupervisionMode>

📌 6. Hardware Watchdog Integration

⭐ **6.1 Watchdog Interface**

.. code-block:: cpp

    namespace ara::phm {
    
    // PHM manages hardware watchdog triggering
    // Applications don't directly interact with HW watchdog
    // PHM triggers watchdog based on global supervision status
    
    class WatchdogInterface {
    public:
        // Internal PHM interface - not exposed to applications
        void TriggerWatchdog() noexcept;
        void StopWatchdog() noexcept;
    };
    
    } // namespace ara::phm

**6.2 Watchdog Behavior**

| Scenario                          | PHM Behavior                                        |
|-----------------------------------|-----------------------------------------------------|
| All supervisions OK               | PHM triggers hardware watchdog periodically         |
| Supervision failure detected      | PHM stops triggering watchdog (→ HW reset)          |
| Graceful shutdown                 | PHM triggers watchdog during shutdown sequence      |
| Recovery action = RestartMachine  | PHM stops watchdog to force HW reset                |

📌 7. Advanced Topics

⭐ **7.1 Multiple Supervised Entity Occurrences**

.. code-block:: cpp

    // R25-11 supports multiple instances of same Supervised Entity
    // Useful for multi-instance applications (e.g., multiple camera processors)
    
    class CameraProcessor {
    public:
        CameraProcessor(uint32_t camera_id) : camera_id_(camera_id) {
            // Each instance gets its own supervised entity
            auto se_result = ara::phm::SupervisedEntity::GetInstance();
            if (se_result.HasValue()) {
                supervised_entity_ = se_result.Value();
            }
        }
        
        void ProcessFrame() {
            // Each instance reports independently
            supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kFrameProcessed);
        }
        
    private:
        uint32_t camera_id_;
        ara::phm::SupervisedEntity supervised_entity_;
    };

**7.2 Mode-Dependent Supervision**

.. code-block:: cpp

    // Different supervision configurations for different operating modes
    // Configured in manifest, switched by State Management
    
    // Example: Parking mode vs Highway mode
    // - Parking: Relaxed supervision (longer deadlines)
    // - Highway: Strict supervision (tight deadlines)

⭐ **7.3 Deactivation of Supervision at Runtime**

.. code-block:: cpp

    class DiagnosticMode {
    public:
        void EnterDiagnosticMode() {
            // During diagnostics, may need to pause supervision
            auto se = ara::phm::SupervisedEntity::GetInstance().Value();
            
            // Stop supervision temporarily
            auto result = se.StopSupervision();
            
            if (result.HasValue()) {
                // Supervision stopped successfully
                // Can now perform diagnostic operations without timeouts
            }
        }
        
        void ExitDiagnosticMode() {
            // Supervision will restart automatically on next checkpoint report
            // Or via Execution Management state transition
        }
    };

**7.4 Recovery Action Delays**

.. code-block:: xml

    <!-- Configurable delay before executing recovery action -->
    <!-- Useful for transient faults -->
    <recoveryAction>
        <actionType>RestartProcess</actionType>
        <delay>500</delay>  <!-- Wait 500ms before restart -->
    </recoveryAction>

📌 8. PHM Integration with Other ARA Services

⭐ **8.1 PHM + Execution Management**

.. code-block:: cpp

    // PHM automatically integrates with Execution Management
    // - Supervision starts when EM transitions to "Running" state
    // - Supervision stops when EM initiates shutdown
    
    // Application code doesn't need explicit start/stop
    // Just report checkpoints

**8.2 PHM + State Management**

.. code-block:: cpp

    // State Management can trigger supervision mode changes
    // Example: Switch from Normal to Degraded supervision
    // when system enters power-save mode

**8.3 PHM + Diagnostics**

.. code-block:: cpp

    // PHM failures can trigger DTC (Diagnostic Trouble Code) events
    // Configured in manifest
    
    // Example: Supervision failure → DTC stored → UDS readable

**8.4 PHM + Logging**

.. code-block:: cpp

    #include <ara/log/logger.h>
    #include <ara/phm/supervised_entity.h>
    
    class SafetyApp {
    public:
        void ReportAndLog() {
            auto result = supervised_entity_.ReportCheckpoint(
                ara::phm::CheckpointId::kCriticalCheckpoint);
            
            if (!result.HasValue()) {
                // Log PHM errors
                logger_.LogError() << "Failed to report checkpoint: " 
                                   << result.Error().Message();
            }
        }
        
    private:
        ara::phm::SupervisedEntity supervised_entity_;
        ara::log::Logger logger_;
    };

📌 9. Safety Considerations & Best Practices

⭐ **9.1 Checkpoint Placement Guidelines**

.. code-block:: cpp

    // ✅ DO: Place checkpoints in critical sections
    void ProcessSafetyData() {
        supervised_entity_.ReportCheckpoint(kStartProcessing);
        
        // Critical safety computation
        PerformSafetyCheck();
        
        supervised_entity_.ReportCheckpoint(kEndProcessing);
    }
    
    // ❌ DON'T: Place checkpoints in exception handlers
    void BadPattern() {
        try {
            DoWork();
            supervised_entity_.ReportCheckpoint(kWorkDone);  // ❌ Wrong
        } catch (...) {
            supervised_entity_.ReportCheckpoint(kWorkDone);  // ❌ Wrong
        }
    }
    
    // ✅ DO: Report only on successful completion
    void GoodPattern() {
        try {
            DoWork();
            supervised_entity_.ReportCheckpoint(kWorkDone);  // ✅ Correct
        } catch (...) {
            // Don't report checkpoint - let supervision timeout
            // PHM will trigger recovery
        }
    }

**9.2 Supervision Timing**

| Rule                              | Recommendation                                      |
|-----------------------------------|-----------------------------------------------------|
| Alive indication frequency        | 5-10x faster than expected alive cycle              |
| Deadline margins                  | 10-20% margin for jitter tolerance                  |
| Recovery action delay             | Consider transient fault duration (100-500ms)       |
| Watchdog timeout                  | 2-3x longer than longest critical path              |

⭐ **9.3 ASIL Compliance**

.. code-block:: cpp

    // For ASIL-B/D applications:
    // 1. Always check Result<> return values
    // 2. Use strict deadline supervision
    // 3. Configure appropriate recovery actions
    // 4. Enable hardware watchdog integration
    // 5. Test supervision failure scenarios
    
    // Example ASIL-compliant pattern:
    auto se_result = ara::phm::SupervisedEntity::GetInstance();
    if (!se_result.HasValue()) {
        // Fatal error - cannot proceed without supervision
        ara::exec::ReportExecutionError(
            ara::exec::ExecutionErrorCode::kSupervisionInitFailed);
        std::terminate();
    }
    
    auto& se = se_result.Value();
    
    auto checkpoint_result = se.ReportCheckpoint(kCriticalCheckpoint);
    if (!checkpoint_result.HasValue()) {
        // Log and potentially trigger safe state
        LogCriticalError("Checkpoint reporting failed");
    }

**9.4 Common Pitfalls**

.. code-block:: cpp

    // ❌ PITFALL 1: Reporting checkpoints too frequently
    void BadLoop() {
        while (true) {
            DoMinimalWork();
            supervised_entity_.ReportCheckpoint(kLoop);  // ❌ Every iteration
        }
    }
    
    // ✅ SOLUTION: Report at reasonable intervals
    void GoodLoop() {
        while (true) {
            for (int i = 0; i < 10; ++i) {
                DoMinimalWork();
            }
            supervised_entity_.ReportCheckpoint(kLoop);  // ✅ Every 10 iterations
        }
    }
    
    // ❌ PITFALL 2: Blocking operations without checkpoints
    void BadBlockingOp() {
        supervised_entity_.ReportCheckpoint(kStart);
        
        // Long blocking operation (e.g., network I/O)
        WaitForNetworkResponse(timeout=10s);  // ❌ No checkpoints during wait
        
        supervised_entity_.ReportCheckpoint(kEnd);  // ❌ May timeout
    }
    
    // ✅ SOLUTION: Report periodically during long operations
    void GoodBlockingOp() {
        supervised_entity_.ReportCheckpoint(kStart);
        
        // Poll with periodic checkpoints
        while (!NetworkResponseAvailable() && elapsed < 10s) {
            std::this_thread::sleep_for(100ms);
            supervised_entity_.ReportCheckpoint(kWaiting);  // ✅ Periodic
        }
        
        supervised_entity_.ReportCheckpoint(kEnd);
    }

📌 10. PHM R25-11 Changes & Migration

⭐ **10.1 Key Changes from R24-11 → R25-11**

| Change                            | Impact                                              | Migration Required |
|-----------------------------------|-----------------------------------------------------|--------------------|
| Removed Health Channel concept    | Direct SupervisedEntity API only                    | ✅ Yes             |
| Removed RS_PHM_00107              | No multiple PHM instances                           | ⚠️  Check config   |
| Removed daisy chaining            | Simplified supervision flow                         | ✅ Yes (if used)   |
| Clarified supervision modes       | Better mode-dependent configuration                 | ℹ️  Optional       |

**10.2 Migration from Health Channel to SupervisedEntity**

.. code-block:: cpp

    // ❌ OLD (R23-11 and earlier):
    #include <ara/phm/health_channel.h>
    
    auto health_channel = ara::phm::CreateHealthChannel("MyApp");
    health_channel->ReportCheckpoint(ara::phm::HealthStatus::kOk, "checkpoint1");
    
    // ✅ NEW (R25-11):
    #include <ara/phm/supervised_entity.h>
    
    auto se = ara::phm::SupervisedEntity::GetInstance().Value();
    se.ReportCheckpoint(ara::phm::CheckpointId::kCheckpoint1);

📌 11. Quick Reference & Cheat Codes

⭐ **11.1 Essential Includes**

.. code-block:: cpp

    #include <ara/phm/supervised_entity.h>      // SupervisedEntity class
    #include <ara/phm/checkpoint_id.h>          // CheckpointId enum
    #include <ara/phm/supervision_status.h>     // SupervisionStatus enum
    #include <ara/phm/phm_error_domain.h>       // Error handling
    #include <ara/core/result.h>                 // Result<> wrapper

**11.2 Typical Usage Pattern**

.. code-block:: cpp

    // 1. Get SupervisedEntity instance
    auto se = ara::phm::SupervisedEntity::GetInstance().Value();
    
    // 2. Report checkpoints in application logic
    se.ReportCheckpoint(ara::phm::CheckpointId::kMainLoop);
    
    // 3. Optionally check status
    auto status = se.GetStatus().Value();
    
    // 4. Graceful shutdown (optional)
    se.StopSupervision();

⭐ **11.3 Mnemonics**

- **PHM = Personal Health Monitor** (but for software processes)
- **Checkpoint = Heartbeat** (signals "I'm alive and progressing")
- **Alive Supervision = Pulse Check** (is it beating?)
- **Deadline Supervision = Stopwatch** (did it finish on time?)
- **Logical Supervision = Traffic Cop** (did it follow the rules?)
- **Recovery Action = Emergency Response** (what to do when things fail?)

📚 12. References & Further Reading

- AUTOSAR_AP_RS_PlatformHealthManagement.pdf (R25-11)
- AUTOSAR_AP_SWS_PlatformHealthManagement.pdf (R25-11)
- ISO 26262 (Road vehicles – Functional safety)
- AUTOSAR Execution Management specification
- AUTOSAR State Management specification

---

**Document Version**: 1.0 (Jan 2026)  
**AUTOSAR Release**: R25-11  
**Status**: Production-ready reference
