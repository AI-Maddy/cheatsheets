
═══════════════════════════════════════════════════════════════════════
SAFETY-CRITICAL SYSTEMS INTERVIEW PREPARATION
═══════════════════════════════════════════════════════════════════════

**Target Roles:** Safety Engineer, Functional Safety Engineer, Certification Engineer
**Difficulty:** Advanced
**Preparation Time:** 5-6 hours
**Last Updated:** January 2026

═══════════════════════════════════════════════════════════════════════

⚡ **QUICK REVISION (15-MINUTE READ)**
─────────────────────────────────────────────────────────────────────────

**Safety Standards Overview:**

| Standard | Domain | SIL/ASIL Levels | Certification |
|----------|--------|-----------------|---------------|
| **ISO 26262** | Automotive | QM, ASIL A-D | TÜV, SGS |
| **DO-178C** | Avionics (Software) | DAL E-A | FAA, EASA |
| **DO-254** | Avionics (Hardware) | DAL E-A | FAA, EASA |
| **IEC 61508** | Industrial | SIL 1-4 | TÜV, UL |
| **IEC 62304** | Medical | Class A-C | FDA, CE |
| **EN 50128** | Railway | SIL 0-4 | CENELEC |

**Safety Integrity Levels:**

.. code-block:: text

    Automotive (ISO 26262):
    ASIL D → Highest (10⁻⁸ failures/hour)
    ASIL C → High
    ASIL B → Medium
    ASIL A → Low
    QM     → No safety requirements
    
    Avionics (DO-178C):
    DAL A → Catastrophic (10⁻⁹ failures/hour)
    DAL B → Hazardous
    DAL C → Major
    DAL D → Minor
    DAL E → No safety effect
    
    Industrial (IEC 61508):
    SIL 4 → Highest (10⁻⁵ to 10⁻⁴ failures/hour)
    SIL 3 → High
    SIL 2 → Medium
    SIL 1 → Low

**Key Safety Concepts:**

1. **Hazard Analysis & Risk Assessment (HARA)**
   - Identify hazards
   - Assess severity, exposure, controllability
   - Determine safety goals

2. **Safety Requirements**
   - Functional Safety Requirements (FSR)
   - Technical Safety Requirements (TSR)
   - Traceability to hazards

3. **Safety Mechanisms**
   - Redundancy (dual/triple modular redundancy)
   - Diversity (different implementations)
   - Monitoring (watchdog, plausibility checks)
   - Graceful degradation

4. **Verification & Validation**
   - Unit testing (100% coverage for highest levels)
   - Integration testing
   - System testing
   - Requirements-based testing

5. **Safety Case**
   - Evidence that system meets safety requirements
   - Certification artifacts

═══════════════════════════════════════════════════════════════════════

🎯 **TOP 25 INTERVIEW QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**BEGINNER LEVEL (8 Questions)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q1: What is functional safety and why is it important?**

**Answer:**

**Functional Safety** = Freedom from unacceptable risk due to hazards caused by malfunctioning behavior of E/E systems.

**Key Points:**
- Not about preventing hardware failures (reliability)
- About detecting and mitigating failures safely
- Systematic approach to safety throughout lifecycle

**Example - Automotive AEB System:**

.. code-block:: text

    Hazard: AEB fails to brake → collision
    
    Without Functional Safety:
    - Sensor fails → no braking → crash
    - Software bug → wrong decision → crash
    
    With Functional Safety:
    - Dual sensors (camera + radar)
    - Plausibility checks
    - Safe state: disable AEB, warn driver
    - Result: No crash (degraded mode)

**Safety Lifecycle (V-Model):**

.. code-block:: text

    Concept Phase
    ├─ Item Definition
    ├─ Hazard Analysis & Risk Assessment (HARA)
    └─ Safety Goals
    
    System Development
    ├─ Functional Safety Concept
    ├─ Technical Safety Concept
    ├─ System Design
    └─ System Integration & Test
    
    Hardware/Software Development
    ├─ Requirements
    ├─ Design
    ├─ Implementation
    └─ Unit Test
    
    Validation
    └─ Safety Validation

**Why Important:**
- **Legal:** Liability (OEM responsible for failures)
- **Ethical:** Prevent injuries/deaths
- **Commercial:** Certification required for market access
- **Reputation:** Product recalls costly

*Talking Point:* "In our ISO 26262 ASIL D AEB project, we implemented dual sensor fusion (camera + radar) to achieve 10⁻⁸ failures/hour target, preventing single-point failures that could lead to collisions."

───────────────────────────────────────────────────────────────────────

**Q2: Explain ASIL determination in ISO 26262**

**Answer:**

**ASIL (Automotive Safety Integrity Level)** determined by:

1. **Severity (S)** - Injury consequence
2. **Exposure (E)** - Frequency of operational situation
3. **Controllability (C)** - Driver's ability to avoid harm

**ASIL Matrix:**

.. code-block:: text

    S3 (Life-threatening)   C1   C2   C3
    E4 (High probability)   C    D    D
    E3 (Medium)             B    C    D
    E2 (Low)                A    B    C
    E1 (Very low)           QM   A    B
    
    S2 (Severe injury)      C1   C2   C3
    E4                      B    C    C
    E3                      A    B    C
    E2                      QM   A    B
    E1                      QM   QM   A
    
    S1 (Light injury)       C1   C2   C3
    E4                      A    B    B
    E3                      QM   A    B
    E2                      QM   QM   A
    E1                      QM   QM   QM

**Severity Classes:**

- **S0:** No injuries
- **S1:** Light to moderate injuries
- **S2:** Severe to life-threatening injuries (survival probable)
- **S3:** Life-threatening to fatal injuries

**Exposure Classes:**

- **E0:** Incredible
- **E1:** Very low probability (< 1%)
- **E2:** Low probability (1-10%)
- **E3:** Medium probability (10-50%)
- **E4:** High probability (> 50%)

**Controllability Classes:**

- **C0:** Controllable in general
- **C1:** Simply controllable (> 99% drivers)
- **C2:** Normally controllable (> 90% drivers)
- **C3:** Difficult to control or uncontrollable (< 90% drivers)

**Example 1: AEB Failure**

.. code-block:: text

    Hazard: AEB doesn't brake → collision
    
    Severity: S3 (fatal injury possible)
    Exposure: E4 (daily driving)
    Controllability: C3 (driver cannot react in time)
    
    ASIL = D (highest)

**Example 2: Lane Keeping Assist Failure**

.. code-block:: text

    Hazard: LKA steers incorrectly → lane departure
    
    Severity: S2 (severe injury)
    Exposure: E4 (highway driving)
    Controllability: C1 (driver can easily override)
    
    ASIL = B

**Example 3: Parking Assist Failure**

.. code-block:: text

    Hazard: Parking sensor fails → minor collision
    
    Severity: S1 (light injury, property damage)
    Exposure: E3 (parking situations)
    Controllability: C1 (driver monitors, low speed)
    
    ASIL = A or QM

───────────────────────────────────────────────────────────────────────

**Q3: What is the difference between systematic and random failures?**

**Answer:**

| Aspect | Systematic Failure | Random Failure |
|--------|-------------------|----------------|
| **Cause** | Design defects, spec errors | Component wear-out, aging |
| **Predictability** | Deterministic (repeatable) | Stochastic (probabilistic) |
| **Detection** | Testing, review | Runtime monitoring |
| **Mitigation** | Process quality (V-model) | Redundancy, diagnostics |
| **Examples** | Software bug, wrong algorithm | Transistor failure, EMI |
| **Standard Focus** | ISO 26262 (automotive) | IEC 61508 (industrial) |

**Systematic Failure Examples:**

1. **Software Bug:**

.. code-block:: c

    // Bug: Division by zero not checked
    int calculate_speed(int distance, int time) {
        return distance / time;  // ❌ Crash if time = 0
    }
    
    // Fix: Add check
    int calculate_speed(int distance, int time) {
        if (time == 0) {
            log_error("Invalid time");
            return 0;  // Safe default
        }
        return distance / time;
    }

2. **Specification Error:**

.. code-block:: text

    Requirement: "AEB shall brake if object < 10m"
    Problem: No mention of vehicle speed
    Result: Brakes at 10m even at 200 km/h (too late!)
    
    Correct: "AEB shall brake at safe distance based on speed"

**Random Failure Examples:**

1. **Hardware Failure:**

.. code-block:: text

    Sensor fails due to aging
    → Detected by plausibility check
    → Switch to redundant sensor
    → Continue operation (degraded mode)

2. **Electromagnetic Interference:**

.. code-block:: text

    EMI causes bit flip in RAM
    → Detected by ECC (Error Correcting Code)
    → Corrected or flagged
    → System continues or enters safe state

**Mitigation Strategies:**

**Systematic:**
- Requirements review
- Design review
- Code review
- Static analysis
- Unit testing (100% coverage for ASIL D)

**Random:**
- Hardware redundancy (dual/triple modular)
- Diagnostic coverage (self-test)
- Fail-safe states
- Watchdog timers

───────────────────────────────────────────────────────────────────────

**Q4: Explain redundancy and its types**

**Answer:**

**Redundancy** = Duplicate hardware/software to tolerate failures.

**Types of Redundancy:**

**1. Dual Modular Redundancy (DMR):**

.. code-block:: text

    ┌─────────────┐
    │  Channel A  │────┐
    └─────────────┘    │
                       ├──→ Comparator → Output
    ┌─────────────┐    │
    │  Channel B  │────┘
    └─────────────┘
    
    - If outputs differ → fault detected
    - Cannot determine which channel is faulty
    - Used for detection, not correction

**Example Code:**

.. code-block:: c

    // DMR for critical calculation
    float calculate_throttle_dmr(float pedal_pos) {
        // Channel A
        float throttle_a = calculate_throttle_primary(pedal_pos);
        
        // Channel B (independent calculation)
        float throttle_b = calculate_throttle_secondary(pedal_pos);
        
        // Compare results
        if (fabs(throttle_a - throttle_b) > 0.05) {  // 5% tolerance
            log_error("DMR mismatch: A=%.2f, B=%.2f", throttle_a, throttle_b);
            enter_safe_state();  // Limp-home mode
            return 0.0;  // Safe value (no throttle)
        }
        
        // Outputs match, use average
        return (throttle_a + throttle_b) / 2.0;
    }

**2. Triple Modular Redundancy (TMR):**

.. code-block:: text

    ┌─────────────┐
    │  Channel A  │────┐
    └─────────────┘    │
                       ├──→ Voter → Output
    ┌─────────────┐    │     (2 of 3)
    │  Channel B  │────┤
    └─────────────┘    │
                       │
    ┌─────────────┐    │
    │  Channel C  │────┘
    └─────────────┘
    
    - Majority voting (2 out of 3)
    - Can tolerate 1 failure
    - Output is the majority result

**Example Code:**

.. code-block:: c

    // TMR for safety-critical sensor reading
    typedef struct {
        float value;
        bool valid;
    } sensor_reading_t;
    
    sensor_reading_t tmr_sensor_read(void) {
        // Read from 3 independent sensors
        float sensor_a = read_sensor(SENSOR_A);
        float sensor_b = read_sensor(SENSOR_B);
        float sensor_c = read_sensor(SENSOR_C);
        
        // Tolerance for agreement
        #define TOLERANCE 0.1
        
        // Vote: Find majority (2 out of 3 agree)
        if (fabs(sensor_a - sensor_b) < TOLERANCE) {
            // A and B agree
            return (sensor_reading_t){(sensor_a + sensor_b) / 2.0, true};
        }
        else if (fabs(sensor_a - sensor_c) < TOLERANCE) {
            // A and C agree
            return (sensor_reading_t){(sensor_a + sensor_c) / 2.0, true};
        }
        else if (fabs(sensor_b - sensor_c) < TOLERANCE) {
            // B and C agree
            return (sensor_reading_t){(sensor_b + sensor_c) / 2.0, true};
        }
        else {
            // No agreement (all 3 differ)
            log_error("TMR failed: A=%.2f, B=%.2f, C=%.2f", 
                     sensor_a, sensor_b, sensor_c);
            return (sensor_reading_t){0.0, false};
        }
    }

**3. Hot Standby:**

.. code-block:: text

    ┌─────────────┐
    │   Primary   │──→ Output (active)
    └─────────────┘
          │
          │ Heartbeat
          ↓
    ┌─────────────┐
    │   Backup    │──→ Standby (takes over if primary fails)
    └─────────────┘

**Example Code:**

.. code-block:: c

    typedef enum {
        CHANNEL_PRIMARY,
        CHANNEL_BACKUP
    } active_channel_t;
    
    active_channel_t active_channel = CHANNEL_PRIMARY;
    uint32_t primary_heartbeat_count = 0;
    
    void monitor_primary_health(void) {
        static uint32_t last_heartbeat = 0;
        
        if (primary_heartbeat_count == last_heartbeat) {
            // Primary failed (no heartbeat update)
            log_error("Primary channel failed, switching to backup");
            active_channel = CHANNEL_BACKUP;
            activate_backup_channel();
        }
        
        last_heartbeat = primary_heartbeat_count;
    }
    
    float get_sensor_value(void) {
        if (active_channel == CHANNEL_PRIMARY) {
            return read_primary_sensor();
        } else {
            return read_backup_sensor();
        }
    }

**4. Software Diversity:**

.. code-block:: c

    // Two independent implementations of same function
    
    // Implementation A (lookup table)
    float calculate_temp_a(uint16_t adc) {
        return temp_lookup_table[adc];
    }
    
    // Implementation B (formula)
    float calculate_temp_b(uint16_t adc) {
        float voltage = (adc / 4095.0) * 3.3;
        return (voltage - 0.5) / 0.01;  // LM35 sensor
    }
    
    // Compare results
    float get_temperature(uint16_t adc) {
        float temp_a = calculate_temp_a(adc);
        float temp_b = calculate_temp_b(adc);
        
        if (fabs(temp_a - temp_b) < 2.0) {  // 2°C tolerance
            return (temp_a + temp_b) / 2.0;
        } else {
            log_error("Temperature calculation mismatch");
            return TEMP_INVALID;
        }
    }

**When to Use:**

- **DMR:** Detection of failures (cost-effective)
- **TMR:** Correction of failures (high reliability)
- **Hot Standby:** Fast failover (minimal downtime)
- **Diversity:** Prevent common-mode failures (systematic faults)

───────────────────────────────────────────────────────────────────────

**Q5: What is a watchdog timer and how is it used in safety systems?**

**Answer:**

**Watchdog Timer** = Hardware/software timer that resets system if not refreshed (kicked) within timeout period.

**Purpose:**
- Detect software hangs (infinite loops, deadlocks)
- Detect task scheduling failures
- Ensure system liveness

**Types:**

**1. Hardware Watchdog:**

.. code-block:: c

    // External watchdog IC (e.g., MAX706)
    #define WDI_PIN GPIO_PIN_5
    
    void init_watchdog(void) {
        // Configure WDI pin as output
        gpio_set_mode(WDI_PIN, GPIO_MODE_OUTPUT);
    }
    
    void kick_watchdog(void) {
        // Toggle WDI pin to reset watchdog
        gpio_toggle(WDI_PIN);
    }
    
    void main_loop(void) {
        while (1) {
            // Normal processing
            process_sensors();
            update_control();
            
            // Kick watchdog (must be done every < 1 second)
            kick_watchdog();
            
            delay_ms(500);
        }
    }
    
    // If kick_watchdog() not called within 1s → hardware reset

**2. Software Watchdog (RTOS):**

.. code-block:: c

    // FreeRTOS software watchdog
    #include "FreeRTOS.h"
    #include "timers.h"
    
    #define WATCHDOG_TIMEOUT_MS 5000
    TimerHandle_t xWatchdogTimer;
    
    void vWatchdogCallback(TimerHandle_t xTimer) {
        // Watchdog expired → critical error
        printf("ERROR: Watchdog timeout! System hang detected.\n");
        
        // Log fault
        log_critical_error("WATCHDOG_TIMEOUT");
        
        // Reset system
        NVIC_SystemReset();
    }
    
    void init_software_watchdog(void) {
        xWatchdogTimer = xTimerCreate(
            "Watchdog",
            pdMS_TO_TICKS(WATCHDOG_TIMEOUT_MS),
            pdFALSE,  // One-shot timer
            NULL,
            vWatchdogCallback
        );
        
        xTimerStart(xWatchdogTimer, 0);
    }
    
    void kick_software_watchdog(void) {
        // Reset timer
        xTimerReset(xWatchdogTimer, 0);
    }
    
    void vCriticalTask(void *pvParameters) {
        for (;;) {
            // Critical work
            control_motor();
            
            // Pet the watchdog
            kick_software_watchdog();
            
            vTaskDelay(pdMS_TO_TICKS(1000));
        }
    }

**3. Window Watchdog:**

.. code-block:: c

    // Watchdog must be kicked within a time window
    // Too early or too late → reset
    
    #define WATCHDOG_MIN_MS 100
    #define WATCHDOG_MAX_MS 500
    
    uint32_t last_kick_time = 0;
    
    void kick_window_watchdog(void) {
        uint32_t now = get_time_ms();
        uint32_t elapsed = now - last_kick_time;
        
        if (elapsed < WATCHDOG_MIN_MS) {
            // Kicked too early (task running too fast?)
            log_error("Watchdog kicked too early");
            // Could indicate timing issue
        }
        else if (elapsed > WATCHDOG_MAX_MS) {
            // Kicked too late (task running too slow?)
            log_error("Watchdog kicked too late");
            system_reset();
        }
        else {
            // Kicked within window (OK)
            reset_hardware_watchdog();
            last_kick_time = now;
        }
    }

**4. Multi-Task Watchdog (RTOS):**

.. code-block:: c

    // Monitor multiple critical tasks
    typedef struct {
        TaskHandle_t task_handle;
        const char *task_name;
        uint32_t last_kick_time;
        uint32_t timeout_ms;
        bool alive;
    } task_watchdog_t;
    
    #define NUM_MONITORED_TASKS 3
    task_watchdog_t monitored_tasks[NUM_MONITORED_TASKS];
    
    void register_task_watchdog(int index, TaskHandle_t handle, 
                               const char *name, uint32_t timeout) {
        monitored_tasks[index].task_handle = handle;
        monitored_tasks[index].task_name = name;
        monitored_tasks[index].timeout_ms = timeout;
        monitored_tasks[index].last_kick_time = get_time_ms();
        monitored_tasks[index].alive = true;
    }
    
    void task_kick_watchdog(int index) {
        monitored_tasks[index].last_kick_time = get_time_ms();
        monitored_tasks[index].alive = true;
    }
    
    void vWatchdogMonitor(void *pvParameters) {
        for (;;) {
            uint32_t now = get_time_ms();
            
            for (int i = 0; i < NUM_MONITORED_TASKS; i++) {
                uint32_t elapsed = now - monitored_tasks[i].last_kick_time;
                
                if (elapsed > monitored_tasks[i].timeout_ms) {
                    // Task timeout
                    printf("ERROR: Task '%s' timeout (%u ms)\n",
                           monitored_tasks[i].task_name, elapsed);
                    
                    monitored_tasks[i].alive = false;
                    
                    // Decide action (reset, disable feature, etc.)
                    handle_task_failure(i);
                }
            }
            
            // Check every 100ms
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }
    
    // Usage in task
    void vMotorControlTask(void *pvParameters) {
        for (;;) {
            control_motor();
            
            // Kick task-specific watchdog
            task_kick_watchdog(TASK_MOTOR_CONTROL);
            
            vTaskDelay(pdMS_TO_TICKS(10));
        }
    }

**Safety Considerations:**

.. code-block:: c

    // DO NOT kick watchdog unconditionally in ISR
    // ❌ Bad practice
    void timer_isr(void) {
        kick_watchdog();  // Masks software hang!
    }
    
    // ✓ Good practice: Let tasks kick watchdog
    void vMainTask(void *pvParameters) {
        for (;;) {
            if (system_healthy()) {
                kick_watchdog();
            }
            // If system unhealthy, watchdog expires → reset
        }
    }

*Talking Point:* "In our ASIL C motor control ECU, we implemented a window watchdog (100-500ms) to detect both task hangs and timing violations. This caught a deadlock bug during integration testing that would have caused field failures."

───────────────────────────────────────────────────────────────────────

**Q6: What is DO-178C and its software levels?**

**Answer:**

**DO-178C** = Software Considerations in Airborne Systems and Equipment Certification (aviation software standard).

**Design Assurance Levels (DAL):**

| DAL | Failure Condition | Failure Rate | Examples |
|-----|-------------------|--------------|----------|
| **DAL A** | Catastrophic (aircraft loss) | < 10⁻⁹/hour | Flight control, autopilot |
| **DAL B** | Hazardous (serious injury) | < 10⁻⁷/hour | Engine control |
| **DAL C** | Major (passenger discomfort) | < 10⁻⁵/hour | Navigation display |
| **DAL D** | Minor (inconvenience) | < 10⁻³/hour | Cabin lighting |
| **DAL E** | No safety effect | No requirement | Entertainment system |

**DO-178C Objectives:**

| Activity | DAL A | DAL B | DAL C | DAL D |
|----------|-------|-------|-------|-------|
| **Requirements Review** | Yes | Yes | Yes | Yes |
| **Design Review** | Yes | Yes | Yes | Partial |
| **Code Review** | Yes | Yes | Partial | No |
| **Unit Testing** | Yes | Yes | Yes | Partial |
| **MC/DC Coverage** | Yes | Yes | No | No |
| **Statement Coverage** | Yes | Yes | Yes | Yes |
| **Branch Coverage** | Yes | Yes | Yes | No |

**MC/DC (Modified Condition/Decision Coverage):**

.. code-block:: c

    // Example: Requires MC/DC for DAL A/B
    bool should_activate_autopilot(bool pilot_engaged, bool system_healthy, 
                                   bool altitude_ok) {
        // Decision with 3 conditions
        return pilot_engaged && system_healthy && altitude_ok;
    }
    
    // MC/DC Test Cases (each condition independently affects outcome):
    // Test 1: F && T && T = F  (pilot_engaged affects result)
    // Test 2: T && T && T = T  (pilot_engaged affects result)
    // Test 3: T && F && T = F  (system_healthy affects result)
    // Test 4: T && T && T = T  (system_healthy affects result)
    // Test 5: T && T && F = F  (altitude_ok affects result)
    // Test 6: T && T && T = T  (altitude_ok affects result)

**DO-178C Supplements:**

- **DO-330:** Software Tool Qualification
- **DO-331:** Model-Based Development
- **DO-332:** Object-Oriented Technology
- **DO-333:** Formal Methods

═══════════════════════════════════════════════════════════════════════

📝 **RESUME TALKING POINTS**
─────────────────────────────────────────────────────────────────────────

**When asked: "Tell me about your safety-critical experience"**

**1. ISO 26262 (Automotive)**
- "Led ASIL D AEB development: dual sensor fusion (camera + radar) with 10⁻⁸ failures/hour target"
- "Conducted HARA for 15 ADAS features, determined ASIL levels (A through D)"
- "Implemented safety mechanisms: redundancy, plausibility checks, fail-safe states"
- "Achieved 100% MC/DC code coverage for ASIL D components"

**2. DO-178C (Avionics)**
- "Developed DAL A flight control software with full traceability"
- "Implemented TMR (Triple Modular Redundancy) for critical sensors"
- "Achieved MC/DC coverage for all safety-critical functions"
- "Passed FAA certification audit (zero findings)"

**3. Safety Mechanisms**
- "Designed DMR comparator for throttle control (5% tolerance)"
- "Implemented window watchdog (100-500ms) to detect timing violations"
- "Created graceful degradation: 3-tier fallback (normal→degraded→safe)"

**Quantifiable Results:**
- ASIL D certification achieved
- Zero safety-related field failures in 1M+ deployed units
- 100% MC/DC coverage (DAL A requirement)
- Reduced false positives from 15% to < 2%

═══════════════════════════════════════════════════════════════════════

**Last Updated:** January 2026
**Good Luck with Your Interview! 🚀**

═══════════════════════════════════════════════════════════════════════
