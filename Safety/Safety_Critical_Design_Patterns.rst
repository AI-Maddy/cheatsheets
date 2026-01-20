═══════════════════════════════════════════════════════════════════════
SAFETY-CRITICAL DESIGN PATTERNS
═══════════════════════════════════════════════════════════════════════

**Complete Guide to Fault-Tolerant Embedded System Design**  
**Domain:** Safety-Critical Systems 🛡️ | Fault Tolerance 🔧 | Reliability 🎯  
**Purpose:** Design patterns for avionics, automotive, medical, and industrial safety systems

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Safety-critical design patterns** ensure systems operate correctly even in the presence of faults, preventing catastrophic failures.

**Key Concepts:**
- **Redundancy:** Multiple independent channels (dual, triple, quadruple)
- **Fault Detection:** Watchdogs, plausibility checks, CRC, parity
- **Fault Tolerance:** Graceful degradation, safe state, fail-operational
- **Diversity:** Different implementations to avoid common-mode failures

**Common Patterns:**
- **Dual-Channel Redundancy:** Two independent systems with comparison (e.g., ABS braking)
- **Triple Modular Redundancy (TMR):** Three channels with 2-out-of-3 voting (e.g., flight control)
- **Watchdog Monitor:** Detects software failures, forces reset/safe state
- **Safe State:** Predictable behavior when fault detected (e.g., power off motor)

**Your Experience:**
- DO-178B Level A: Redundant fuel controller channels
- ADAS: Sensor fusion with plausibility checks
- Automotive ECU: Watchdog monitoring, safe state transitions
- Industrial: Dual-channel safety architecture

**Core Principle:**
Assume failures will occur → Detect, isolate, and mitigate before catastrophe

═══════════════════════════════════════════════════════════════════════

🎯 **1. FUNDAMENTALS OF SAFETY-CRITICAL DESIGN**
─────────────────────────────────────────────────────────────────────────

**1.1 Safety vs Reliability**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Safety vs Reliability (Often Confused):
   
   Reliability:
   ────────────
   Definition: Probability system operates correctly over time
   Focus: Preventing all failures
   Metric: MTTF (Mean Time To Failure)
   
   Example: Server uptime 99.999% ("five nines")
   
   Safety:
   ───────
   Definition: Freedom from unacceptable risk of harm
   Focus: Preventing hazardous failures
   Metric: Probability of hazardous event
   
   Example: Airbag must deploy when needed, even if infotainment fails
   
   Key Insight:
   ────────────
   A system can be:
   • Safe but unreliable: Airbag that often fails to deploy (false negative)
     but never deploys incorrectly (no false positive harm)
   • Reliable but unsafe: Brake system that works 99.9% of the time
     but catastrophic 0.1% failure
   
   Safety-Critical Design:
   ───────────────────────
   Prioritizes safety over reliability
   • Better to shut down safely than operate incorrectly
   • "Fail-safe" over "fail-operational" (unless high availability required)

**1.2 Hazard Analysis**
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Hazard Analysis Methods:
   
   FMEA (Failure Mode and Effects Analysis):
   ──────────────────────────────────────────
   Bottom-up: Start with component failures, analyze effects
   
   Example: Motor Controller FMEA
   
   Component      Failure Mode           Effect              Severity  Probability  RPN
   ═══════════════════════════════════════════════════════════════════════════════════
   Speed Sensor   Open circuit           No speed reading    Critical  Medium       8
   Speed Sensor   Short circuit          Zero speed reading  Critical  Low          6
   Speed Sensor   Drift (out of cal)     Incorrect speed     Major     Medium       7
   PWM Driver     Stuck high             Full speed always   Critical  Low          6
   PWM Driver     Stuck low              Motor won't start   Minor     Low          3
   MCU            Runaway code           Unpredictable       Critical  Very Low     5
   Power Supply   Overvoltage            Component damage    Major     Low          5
   
   RPN = Risk Priority Number (Severity × Probability × Detectability)
   
   FTA (Fault Tree Analysis):
   ──────────────────────────
   Top-down: Start with hazard, trace to root causes
   
   Example: Unintended Motor Acceleration
   
                   Unintended Acceleration
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Software Fault              Hardware Fault
              │                           │
       ┌──────┴──────┐           ┌────────┴────────┐
       │             │           │                 │
   Runaway      Incorrect    PWM Stuck       Sensor
    Code         Control       High          Failure
                  Law

**1.3 Safety Integrity Levels**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Safety Standards and Integrity Levels:
   
   DO-178C (Avionics):
   ───────────────────
   Level A: Catastrophic (loss of aircraft)
   Level B: Hazardous
   Level C: Major
   Level D: Minor
   Level E: No effect
   
   ISO 26262 (Automotive):
   ───────────────────────
   ASIL D: Highest (airbag, brake-by-wire)
   ASIL C: High (electric power steering)
   ASIL B: Medium (brake lights)
   ASIL A: Low
   QM: Quality managed (no safety requirement)
   
   IEC 61508 (Industrial):
   ───────────────────────
   SIL 4: Highest (10⁻⁵ to 10⁻⁴ probability of failure per hour)
   SIL 3: High (10⁻⁴ to 10⁻³)
   SIL 2: Medium (10⁻³ to 10⁻²)
   SIL 1: Low (10⁻² to 10⁻¹)
   
   IEC 62304 (Medical):
   ────────────────────
   Class C: Serious injury or death (pacemaker)
   Class B: Injury (infusion pump)
   Class A: No injury (diagnostic)

═══════════════════════════════════════════════════════════════════════

🔄 **2. REDUNDANCY PATTERNS**
─────────────────────────────────────────────────────────────────────────

**2.1 Dual-Channel Redundancy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Dual-Channel Architecture (2-Channel):
   
   ┌─────────────────────────────────────────────────────┐
   │              Input (Sensor)                         │
   └────────────────┬────────────────────────────────────┘
                    │
           ┌────────┴────────┐
           │                 │
   ┌───────▼──────┐  ┌───────▼──────┐
   │  Channel A   │  │  Channel B   │
   │              │  │              │
   │ • MCU A      │  │ • MCU B      │
   │ • Software A │  │ • Software B │
   │ • Power A    │  │ • Power B    │
   └───────┬──────┘  └───────┬──────┘
           │                 │
           │    ┌────────────┴────────────┐
           │    │   Comparison Logic      │
           └───►│   (Watchdog Monitor)    │
                │                         │
                │   If A ≠ B: Fault       │
                └────────┬────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Safe Action  │
                  │ (Disable)    │
                  └──────────────┘
   
   Applications:
   ─────────────
   • Railway signaling (vital relay control)
   • Automotive safety (airbag deployment)
   • Industrial safety PLCs
   • Medical devices (insulin pump)
   
   Advantages:
   ───────────
   ✅ Detects single-point failures
   ✅ Lower cost than triple redundancy
   ✅ Simpler than voting logic
   
   Disadvantages:
   ──────────────
   ❌ Fail-safe only (cannot continue operation)
   ❌ Cannot tolerate failures (only detect)
   ❌ Both channels must agree (conservative)

**Implementation Example: Dual-Channel Motor Controller**

.. code-block:: c

   // Dual-channel motor control with comparison
   
   typedef struct {
       uint16_t speed;
       uint16_t current;
       uint16_t position;
       uint16_t crc;
   } MotorState_t;
   
   // Channel A computation
   MotorState_t channel_a_compute(SensorData_t *sensors)
   {
       MotorState_t state;
       
       // Channel A control algorithm
       state.speed = pid_compute_a(sensors->encoder_a);
       state.current = current_control_a(sensors->current_a);
       state.position = sensors->encoder_a;
       
       // Add CRC for data integrity
       state.crc = calculate_crc16((uint8_t*)&state, 
                                   sizeof(MotorState_t) - sizeof(uint16_t));
       
       return state;
   }
   
   // Channel B computation (independent implementation)
   MotorState_t channel_b_compute(SensorData_t *sensors)
   {
       MotorState_t state;
       
       // Channel B control algorithm (possibly different algorithm for diversity)
       state.speed = pid_compute_b(sensors->encoder_b);
       state.current = current_control_b(sensors->current_b);
       state.position = sensors->encoder_b;
       
       state.crc = calculate_crc16((uint8_t*)&state, 
                                   sizeof(MotorState_t) - sizeof(uint16_t));
       
       return state;
   }
   
   // Comparison and fault detection
   bool compare_channels(MotorState_t *ch_a, MotorState_t *ch_b)
   {
       // Check CRC first
       if (!verify_crc(ch_a) || !verify_crc(ch_b)) {
           log_fault(FAULT_CRC_ERROR);
           return false;
       }
       
       // Compare outputs with tolerance
       #define SPEED_TOLERANCE    10   // RPM
       #define CURRENT_TOLERANCE  50   // mA
       #define POSITION_TOLERANCE 5    // encoder counts
       
       if (abs(ch_a->speed - ch_b->speed) > SPEED_TOLERANCE) {
           log_fault(FAULT_SPEED_MISMATCH);
           return false;
       }
       
       if (abs(ch_a->current - ch_b->current) > CURRENT_TOLERANCE) {
           log_fault(FAULT_CURRENT_MISMATCH);
           return false;
       }
       
       if (abs(ch_a->position - ch_b->position) > POSITION_TOLERANCE) {
           log_fault(FAULT_POSITION_MISMATCH);
           return false;
       }
       
       return true;  // Channels agree
   }
   
   // Main control loop
   void motor_control_task(void)
   {
       SensorData_t sensors;
       MotorState_t channel_a, channel_b;
       
       // Read sensors
       read_sensors(&sensors);
       
       // Compute both channels independently
       channel_a = channel_a_compute(&sensors);
       channel_b = channel_b_compute(&sensors);
       
       // Compare channels
       if (compare_channels(&channel_a, &channel_b)) {
           // Agreement: Use average (or just one channel)
           uint16_t output_speed = (channel_a.speed + channel_b.speed) / 2;
           set_motor_speed(output_speed);
           
           // Feed watchdog (both channels healthy)
           watchdog_refresh();
       } else {
           // Disagreement: Enter safe state
           enter_safe_state();
           
           // Do NOT feed watchdog → System will reset
       }
   }
   
   // Safe state: Disable motor, set outputs to known safe values
   void enter_safe_state(void)
   {
       // Disable PWM outputs
       disable_pwm();
       
       // Set enable pins low
       GPIO_ResetBits(MOTOR_ENABLE_PORT, MOTOR_ENABLE_PIN);
       
       // Activate brake (if available)
       GPIO_SetBits(MOTOR_BRAKE_PORT, MOTOR_BRAKE_PIN);
       
       // Log fault for diagnostics
       log_fault(FAULT_CHANNEL_MISMATCH);
       
       // Indicate fault via LED/CAN message
       set_fault_led(true);
       send_can_fault_message(FAULT_DUAL_CHANNEL_MISMATCH);
       
       // Wait for watchdog reset (do not feed)
       while(1);
   }

**2.2 Triple Modular Redundancy (TMR)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Triple Modular Redundancy (3-Channel with Voting):
   
   ┌─────────────────────────────────────────────────────┐
   │              Input (Sensor)                         │
   └──────┬─────────────┬────────────┬───────────────────┘
          │             │            │
   ┌──────▼──────┐ ┌────▼─────┐ ┌───▼───────┐
   │ Channel A   │ │Channel B │ │ Channel C │
   │             │ │          │ │           │
   │ • MCU A     │ │ • MCU B  │ │ • MCU C   │
   │ • SW A      │ │ • SW B   │ │ • SW C    │
   └──────┬──────┘ └────┬─────┘ └───┬───────┘
          │             │            │
          │      ┌──────▼──────┐     │
          └─────►│   Voter     │◄────┘
                 │  (2-of-3)   │
                 └──────┬──────┘
                        │
                        ▼
                  ┌───────────┐
                  │  Output   │
                  └───────────┘
   
   Voting Logic:
   ─────────────
   If A = B = C:  Use agreed value (all healthy)
   If A = B ≠ C:  Use A (C is faulty)
   If A = C ≠ B:  Use A (B is faulty)
   If B = C ≠ A:  Use B (A is faulty)
   If A ≠ B ≠ C:  FAULT (multiple failures or voter error)
   
   Applications:
   ─────────────
   • Flight control (fly-by-wire)
   • Spacecraft computers
   • Nuclear reactor control
   • High-availability servers
   
   Advantages:
   ───────────
   ✅ Fail-operational (can tolerate one failure)
   ✅ Automatic fault masking (no service interruption)
   ✅ High reliability
   
   Disadvantages:
   ──────────────
   ❌ High cost (3× hardware)
   ❌ Complex voter logic
   ❌ Cannot tolerate two simultaneous failures
   ❌ Common-mode failures (all three use same design)

**TMR Implementation:**

.. code-block:: c

   // Triple Modular Redundancy with 2-out-of-3 voting
   
   #define NUM_CHANNELS 3
   
   typedef struct {
       int16_t value;
       bool valid;
       uint32_t timestamp;
   } ChannelOutput_t;
   
   // Voting function (median voter - works for analog values)
   int16_t vote_median(ChannelOutput_t outputs[NUM_CHANNELS])
   {
       int16_t values[NUM_CHANNELS];
       int count = 0;
       
       // Collect valid values
       for (int i = 0; i < NUM_CHANNELS; i++) {
           if (outputs[i].valid) {
               values[count++] = outputs[i].value;
           }
       }
       
       // Need at least 2 valid channels
       if (count < 2) {
           log_fault(FAULT_INSUFFICIENT_CHANNELS);
           return 0;  // Or trigger safe state
       }
       
       // Sort values
       for (int i = 0; i < count - 1; i++) {
           for (int j = i + 1; j < count; j++) {
               if (values[i] > values[j]) {
                   int16_t temp = values[i];
                   values[i] = values[j];
                   values[j] = temp;
               }
           }
       }
       
       // Return median
       return values[count / 2];
   }
   
   // Voting function (majority voter - for discrete values)
   int16_t vote_majority(ChannelOutput_t outputs[NUM_CHANNELS])
   {
       #define TOLERANCE 5  // Tolerance for "equality"
       
       int16_t a = outputs[0].value;
       int16_t b = outputs[1].value;
       int16_t c = outputs[2].value;
       
       // Check validity
       if (!outputs[0].valid || !outputs[1].valid || !outputs[2].valid) {
           // At least one channel invalid
           if (outputs[0].valid && outputs[1].valid) {
               if (abs(a - b) <= TOLERANCE) return (a + b) / 2;
           }
           if (outputs[0].valid && outputs[2].valid) {
               if (abs(a - c) <= TOLERANCE) return (a + c) / 2;
           }
           if (outputs[1].valid && outputs[2].valid) {
               if (abs(b - c) <= TOLERANCE) return (b + c) / 2;
           }
           
           log_fault(FAULT_INSUFFICIENT_VALID_CHANNELS);
           return 0;
       }
       
       // All three valid - check agreement
       if (abs(a - b) <= TOLERANCE && abs(b - c) <= TOLERANCE) {
           // All agree
           return (a + b + c) / 3;
       }
       
       if (abs(a - b) <= TOLERANCE) {
           // A and B agree, C is outlier
           log_fault(FAULT_CHANNEL_C_MISMATCH);
           return (a + b) / 2;
       }
       
       if (abs(a - c) <= TOLERANCE) {
           // A and C agree, B is outlier
           log_fault(FAULT_CHANNEL_B_MISMATCH);
           return (a + c) / 2;
       }
       
       if (abs(b - c) <= TOLERANCE) {
           // B and C agree, A is outlier
           log_fault(FAULT_CHANNEL_A_MISMATCH);
           return (b + c) / 2;
       }
       
       // No agreement
       log_fault(FAULT_NO_MAJORITY);
       return 0;  // Or safe state
   }
   
   // Flight control example with TMR
   void flight_control_task(void)
   {
       ChannelOutput_t pitch_cmd[NUM_CHANNELS];
       
       // Each channel computes independently
       pitch_cmd[0] = channel_a_compute_pitch();
       pitch_cmd[1] = channel_b_compute_pitch();
       pitch_cmd[2] = channel_c_compute_pitch();
       
       // Vote on outputs
       int16_t voted_pitch = vote_majority(pitch_cmd);
       
       // Apply command
       set_pitch_actuator(voted_pitch);
       
       // Monitor for degraded mode
       int fault_count = 0;
       for (int i = 0; i < NUM_CHANNELS; i++) {
           if (!pitch_cmd[i].valid) fault_count++;
       }
       
       if (fault_count >= 2) {
           // Two channels failed → Cannot continue safely
           enter_degraded_mode();
       } else if (fault_count == 1) {
           // One channel failed → Continued operation with warning
           set_degraded_mode_flag(true);
       }
   }

**2.3 Quadruple Redundancy (Quad)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Quadruple Redundancy (4-Channel):
   
   Used when:
   • Must tolerate two simultaneous failures
   • Extremely high reliability required
   • Space missions (no repair possible)
   
   Voting: 2-out-of-4 or 3-out-of-4
   
   Example: Space Shuttle General Purpose Computer (GPC)
   ──────────────────────────────────────────────────────
   • 4 identical computers running same software
   • 1 backup computer with dissimilar software
   • Voting on all outputs
   • Can tolerate 2 failures and still operate

═══════════════════════════════════════════════════════════════════════

🐕 **3. WATCHDOG PATTERNS**
─────────────────────────────────────────────────────────────────────────

**3.1 Hardware Watchdog**
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Hardware Watchdog Timer:
   
   ┌──────────────────────────────────────────────────┐
   │         Microcontroller                          │
   │                                                  │
   │  ┌────────────────────────────────────┐          │
   │  │  Software Task                     │          │
   │  │                                    │          │
   │  │  while(1) {                        │          │
   │  │      do_control();                 │          │
   │  │      watchdog_refresh(); ◄─────────┼──────┐   │
   │  │  }                                 │      │   │
   │  └────────────────────────────────────┘      │   │
   │                                              │   │
   │  ┌───────────────────────────────────────────┼──┐│
   │  │  Hardware Watchdog Timer                  │  ││
   │  │                                           │  ││
   │  │  Counter: 1000 ms                         │  ││
   │  │  ├─ Decrements every 1 ms                 │  ││
   │  │  ├─ Reloaded on refresh  ◄────────────────┘  ││
   │  │  └─ Triggers reset if reaches 0              ││
   │  └──────────────────────────────────────────────┘│
   │                        │                          │
   │                        │ (timeout)                │
   │                        ▼                          │
   │              ┌──────────────────┐                 │
   │              │   System Reset   │                 │
   │              └──────────────────┘                 │
   └──────────────────────────────────────────────────┘
   
   Purpose:
   ────────
   Detect software failures:
   • Infinite loops
   • Deadlocks
   • Stack overflow (crashes)
   • Runaway code
   
   Operation:
   ──────────
   1. Software must periodically "kick" (refresh) watchdog
   2. If software fails to refresh (hung/crashed), timeout occurs
   3. Watchdog triggers system reset
   4. System restarts to known safe state

**Hardware Watchdog Implementation:**

.. code-block:: c

   // STM32 Independent Watchdog (IWDG) configuration
   
   void watchdog_init(void)
   {
       // Enable write access to IWDG registers
       IWDG->KR = 0x5555;
       
       // Set prescaler: 32 kHz / 64 = 512 Hz
       IWDG->PR = IWDG_PR_PR_2;  // Prescaler = 64
       
       // Set reload value: 512 Hz / 512 = 1 second timeout
       IWDG->RLR = 511;  // 0-4095 range
       
       // Start watchdog
       IWDG->KR = 0xCCCC;
       
       // First refresh
       IWDG->KR = 0xAAAA;
   }
   
   void watchdog_refresh(void)
   {
       // Reload counter (must be called within timeout period)
       IWDG->KR = 0xAAAA;
   }
   
   // Main control loop
   int main(void)
   {
       system_init();
       watchdog_init();  // 1-second timeout
       
       while (1) {
           // Normal operation
           read_sensors();
           compute_control();
           update_actuators();
           
           // Check system health before refreshing watchdog
           if (system_health_check()) {
               watchdog_refresh();  // System OK, feed watchdog
           } else {
               // System unhealthy, let watchdog reset system
               // Do NOT refresh watchdog
           }
           
           delay_ms(100);  // 10 Hz control loop
       }
   }
   
   // Health check before watchdog refresh
   bool system_health_check(void)
   {
       // Check stack usage
       if (get_stack_usage() > 80) {
           log_fault(FAULT_STACK_OVERFLOW_IMMINENT);
           return false;  // Don't refresh → Reset
       }
       
       // Check critical task execution
       if (!critical_task_executed_this_cycle()) {
           log_fault(FAULT_TASK_NOT_RUNNING);
           return false;
       }
       
       // Check sensor validity
       if (!sensors_within_range()) {
           log_fault(FAULT_SENSOR_OUT_OF_RANGE);
           return false;
       }
       
       // All checks passed
       return true;
   }

**3.2 Software Watchdog (Task Monitoring)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Multi-task watchdog monitoring (RTOS environment)
   
   #define MAX_TASKS 10
   
   typedef struct {
       const char *name;
       uint32_t timeout_ms;
       uint32_t last_checkin;
       bool enabled;
   } TaskWatchdog_t;
   
   TaskWatchdog_t task_watchdogs[MAX_TASKS];
   int num_tasks = 0;
   
   // Register task for watchdog monitoring
   int watchdog_register_task(const char *name, uint32_t timeout_ms)
   {
       if (num_tasks >= MAX_TASKS) return -1;
       
       task_watchdogs[num_tasks].name = name;
       task_watchdogs[num_tasks].timeout_ms = timeout_ms;
       task_watchdogs[num_tasks].last_checkin = get_tick_count();
       task_watchdogs[num_tasks].enabled = true;
       
       return num_tasks++;
   }
   
   // Task checks in (called periodically by each task)
   void watchdog_checkin(int task_id)
   {
       if (task_id < 0 || task_id >= num_tasks) return;
       
       task_watchdogs[task_id].last_checkin = get_tick_count();
   }
   
   // Watchdog monitor task (runs periodically, e.g., 100 ms)
   void watchdog_monitor_task(void *param)
   {
       while (1) {
           uint32_t now = get_tick_count();
           bool all_ok = true;
           
           // Check all registered tasks
           for (int i = 0; i < num_tasks; i++) {
               if (!task_watchdogs[i].enabled) continue;
               
               uint32_t elapsed = now - task_watchdogs[i].last_checkin;
               
               if (elapsed > task_watchdogs[i].timeout_ms) {
                   // Task timeout
                   log_fault(FAULT_TASK_TIMEOUT);
                   printf("WATCHDOG: Task '%s' timeout (%lu ms)\n",
                          task_watchdogs[i].name, elapsed);
                   
                   all_ok = false;
                   
                   // Take action
                   handle_task_timeout(i);
               }
           }
           
           if (all_ok) {
               // All tasks healthy, refresh hardware watchdog
               watchdog_refresh();
           } else {
               // At least one task unhealthy
               // Do NOT refresh hardware watchdog → System will reset
           }
           
           vTaskDelay(pdMS_TO_TICKS(100));  // Check every 100 ms
       }
   }
   
   // Example: Critical control task
   void control_task(void *param)
   {
       int wd_id = watchdog_register_task("ControlTask", 200);  // 200 ms timeout
       
       while (1) {
           // Do control work
           read_sensors();
           compute_pid();
           update_outputs();
           
           // Check in with watchdog
           watchdog_checkin(wd_id);
           
           vTaskDelay(pdMS_TO_TICKS(10));  // 100 Hz
       }
   }

**3.3 Window Watchdog**
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Window Watchdog (Advanced):
   
   Problem with standard watchdog:
   ────────────────────────────────
   If software stuck in tight loop that includes watchdog_refresh(),
   watchdog will not detect the fault
   
   while(1) {
       watchdog_refresh();  // Stuck here, but watchdog is happy!
   }
   
   Solution: Window Watchdog
   ─────────────────────────
   
   Valid refresh window: 50-100 ms
   
   ┌─────────────────────────────────────────┐
   │  0ms   50ms   75ms  100ms  150ms        │
   ├────────┼──────┼─────┼──────┼────────────┤
   │  Too   │ Valid│     │ Too  │  Timeout   │
   │  Early │Window│     │ Late │            │
   └────────┴──────┴─────┴──────┴────────────┘
   
   • Refresh before 50 ms → Reset (too fast)
   • Refresh between 50-100 ms → OK
   • Refresh after 100 ms → Reset (too slow)
   • No refresh by 150 ms → Reset (timeout)
   
   Benefits:
   ─────────
   ✅ Detects runaway fast loops
   ✅ Detects timing violations
   ✅ Ensures deterministic task execution

.. code-block:: c

   // STM32 Window Watchdog (WWDG) configuration
   
   void window_watchdog_init(void)
   {
       // Enable WWDG clock
       RCC->APB1ENR |= RCC_APB1ENR_WWDGEN;
       
       // Configure:
       // - Counter: 0x7F (127) down to 0x40 (64) = valid window
       // - Prescaler: PCLK1 / 4096 / 8 = ~1 ms per decrement
       
       WWDG->CFR = (0x7F << 0) |   // Window value = 127
                   (WWDG_CFR_WDGTB_1);  // Prescaler = 8
       
       WWDG->CR = (0x7F << 0) |    // Counter start value = 127
                  WWDG_CR_WDGA;     // Enable watchdog
       
       // Valid refresh window: Counter between 127 and 64
       // = about 50-100 ms window
   }
   
   void window_watchdog_refresh(void)
   {
       // Refresh (reload counter to 0x7F)
       WWDG->CR = 0x7F | WWDG_CR_WDGA;
   }

═══════════════════════════════════════════════════════════════════════

🛡️ **4. FAULT DETECTION PATTERNS**
─────────────────────────────────────────────────────────────────────────

**4.1 Plausibility Checks**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Sensor plausibility checking
   
   typedef struct {
       float min_value;
       float max_value;
       float max_rate_of_change;  // per second
       float last_valid_value;
       uint32_t last_update_time;
   } SensorLimits_t;
   
   typedef enum {
       SENSOR_OK,
       SENSOR_OUT_OF_RANGE,
       SENSOR_RATE_LIMIT_EXCEEDED,
       SENSOR_STUCK,
       SENSOR_NOISY
   } SensorStatus_t;
   
   // Check if sensor value is plausible
   SensorStatus_t check_sensor_plausibility(float value, SensorLimits_t *limits)
   {
       uint32_t now = get_tick_count_ms();
       
       // Range check
       if (value < limits->min_value || value > limits->max_value) {
           return SENSOR_OUT_OF_RANGE;
       }
       
       // Rate of change check
       if (limits->last_update_time > 0) {
           float dt = (now - limits->last_update_time) / 1000.0f;  // seconds
           float delta = fabs(value - limits->last_valid_value);
           float rate = delta / dt;
           
           if (rate > limits->max_rate_of_change) {
               return SENSOR_RATE_LIMIT_EXCEEDED;
           }
       }
       
       // Stuck sensor check (value hasn't changed in long time)
       #define STUCK_THRESHOLD_MS 5000
       if (now - limits->last_update_time > STUCK_THRESHOLD_MS) {
           if (fabs(value - limits->last_valid_value) < 0.01f) {
               return SENSOR_STUCK;
           }
       }
       
       // Update for next check
       limits->last_valid_value = value;
       limits->last_update_time = now;
       
       return SENSOR_OK;
   }
   
   // Example: Temperature sensor
   void read_temperature_sensor(void)
   {
       static SensorLimits_t temp_limits = {
           .min_value = -40.0f,     // °C
           .max_value = 150.0f,     // °C
           .max_rate_of_change = 10.0f,  // °C/sec (physical limit)
           .last_valid_value = 25.0f,
           .last_update_time = 0
       };
       
       float raw_temp = read_adc_temperature();
       
       SensorStatus_t status = check_sensor_plausibility(raw_temp, &temp_limits);
       
       switch (status) {
           case SENSOR_OK:
               // Use value
               current_temperature = raw_temp;
               break;
               
           case SENSOR_OUT_OF_RANGE:
               log_fault(FAULT_TEMP_OUT_OF_RANGE);
               // Use last known good value or safe default
               current_temperature = temp_limits.last_valid_value;
               break;
               
           case SENSOR_RATE_LIMIT_EXCEEDED:
               log_fault(FAULT_TEMP_RATE_LIMIT);
               // Physical impossibility, likely sensor failure
               enter_safe_state();
               break;
               
           case SENSOR_STUCK:
               log_fault(FAULT_TEMP_STUCK);
               // Sensor not responding
               enter_degraded_mode();
               break;
               
           default:
               break;
       }
   }

**4.2 Cross-Channel Correlation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Multi-sensor correlation (sensor fusion validation)
   
   // Example: Vehicle speed from multiple sources
   typedef struct {
       float wheel_speed_fl;    // Front left wheel
       float wheel_speed_fr;    // Front right
       float wheel_speed_rl;    // Rear left
       float wheel_speed_rr;    // Rear right
       float gps_speed;
       float accelerometer_integrated_speed;
   } SpeedSources_t;
   
   // Validate speed measurement using correlation
   bool validate_speed_measurement(SpeedSources_t *sources, float *validated_speed)
   {
       #define SPEED_TOLERANCE 5.0f  // km/h
       
       // Calculate average wheel speed
       float avg_wheel_speed = (sources->wheel_speed_fl + 
                                sources->wheel_speed_fr +
                                sources->wheel_speed_rl + 
                                sources->wheel_speed_rr) / 4.0f;
       
       // Check individual wheel speeds for outliers
       int outlier_count = 0;
       if (fabs(sources->wheel_speed_fl - avg_wheel_speed) > SPEED_TOLERANCE) outlier_count++;
       if (fabs(sources->wheel_speed_fr - avg_wheel_speed) > SPEED_TOLERANCE) outlier_count++;
       if (fabs(sources->wheel_speed_rl - avg_wheel_speed) > SPEED_TOLERANCE) outlier_count++;
       if (fabs(sources->wheel_speed_rr - avg_wheel_speed) > SPEED_TOLERANCE) outlier_count++;
       
       if (outlier_count > 1) {
           // Multiple wheel speed sensors disagree
           log_fault(FAULT_WHEEL_SPEED_CORRELATION);
           return false;
       }
       
       // Cross-check with GPS
       if (fabs(avg_wheel_speed - sources->gps_speed) > 10.0f) {
           // Significant difference from GPS
           // (Could be normal during acceleration, or GPS error)
           
           // Cross-check with accelerometer integration
           if (fabs(avg_wheel_speed - sources->accelerometer_integrated_speed) < SPEED_TOLERANCE) {
               // Wheel speed and accelerometer agree, GPS is outlier
               *validated_speed = avg_wheel_speed;
               return true;
           } else {
               // None agree - possible fault
               log_fault(FAULT_SPEED_CORRELATION_FAILED);
               return false;
           }
       }
       
       // All sources correlate
       *validated_speed = avg_wheel_speed;
       return true;
   }

**4.3 CRC and Parity Protection**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Memory and data integrity checks
   
   // CRC-16 CCITT calculation
   uint16_t crc16_ccitt(const uint8_t *data, size_t length)
   {
       uint16_t crc = 0xFFFF;
       
       for (size_t i = 0; i < length; i++) {
           crc ^= (uint16_t)data[i] << 8;
           
           for (int j = 0; j < 8; j++) {
               if (crc & 0x8000) {
                   crc = (crc << 1) ^ 0x1021;
               } else {
                   crc = crc << 1;
               }
           }
       }
       
       return crc;
   }
   
   // Protected data structure
   typedef struct {
       uint32_t critical_param_1;
       uint32_t critical_param_2;
       float    critical_param_3;
       uint16_t crc;  // Protects above fields
   } ProtectedData_t;
   
   // Write protected data
   void write_protected_data(ProtectedData_t *data, uint32_t p1, uint32_t p2, float p3)
   {
       data->critical_param_1 = p1;
       data->critical_param_2 = p2;
       data->critical_param_3 = p3;
       
       // Calculate and store CRC
       data->crc = crc16_ccitt((uint8_t*)data, 
                               sizeof(ProtectedData_t) - sizeof(uint16_t));
   }
   
   // Read and verify protected data
   bool read_protected_data(ProtectedData_t *data)
   {
       // Calculate CRC of current data
       uint16_t calculated_crc = crc16_ccitt((uint8_t*)data, 
                                             sizeof(ProtectedData_t) - sizeof(uint16_t));
       
       // Compare with stored CRC
       if (calculated_crc != data->crc) {
           log_fault(FAULT_CRC_MISMATCH);
           return false;  // Data corrupted
       }
       
       return true;  // Data valid
   }
   
   // RAM test pattern (March algorithm)
   bool ram_test(uint32_t *start_addr, uint32_t *end_addr)
   {
       uint32_t *addr;
       
       // Write 0x00000000 to all locations
       for (addr = start_addr; addr < end_addr; addr++) {
           *addr = 0x00000000;
       }
       
       // Read and verify 0x00000000, then write 0xFFFFFFFF
       for (addr = start_addr; addr < end_addr; addr++) {
           if (*addr != 0x00000000) {
               return false;  // RAM fault
           }
           *addr = 0xFFFFFFFF;
       }
       
       // Read and verify 0xFFFFFFFF
       for (addr = start_addr; addr < end_addr; addr++) {
           if (*addr != 0xFFFFFFFF) {
               return false;  // RAM fault
           }
       }
       
       return true;  // RAM OK
   }

**4.4 Stack Overflow Detection**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Stack canary pattern (stack overflow detection)
   
   #define STACK_CANARY_PATTERN 0xDEADBEEF
   
   // Place canary at bottom of stack
   void stack_init_canary(uint32_t *stack_bottom)
   {
       *stack_bottom = STACK_CANARY_PATTERN;
   }
   
   // Check if stack canary is intact
   bool stack_check_canary(uint32_t *stack_bottom)
   {
       if (*stack_bottom != STACK_CANARY_PATTERN) {
           log_fault(FAULT_STACK_OVERFLOW);
           return false;  // Stack overflow detected
       }
       return true;
   }
   
   // Stack usage measurement
   uint32_t stack_get_usage(uint32_t *stack_bottom, uint32_t *stack_top)
   {
       uint32_t *ptr = stack_bottom;
       
       // Find first non-pattern value (stack has grown to here)
       while (ptr < stack_top && *ptr == STACK_CANARY_PATTERN) {
           ptr++;
       }
       
       uint32_t used = (uint32_t)(stack_top - ptr) * sizeof(uint32_t);
       uint32_t total = (uint32_t)(stack_top - stack_bottom) * sizeof(uint32_t);
       
       return (used * 100) / total;  // Percentage
   }
   
   // Monitor stack usage periodically
   void stack_monitor_task(void)
   {
       extern uint32_t _stack_bottom;
       extern uint32_t _stack_top;
       
       while (1) {
           // Check canary
           if (!stack_check_canary(&_stack_bottom)) {
               // Stack overflow!
               enter_safe_state();
           }
           
           // Check usage
           uint32_t usage = stack_get_usage(&_stack_bottom, &_stack_top);
           
           if (usage > 80) {
               log_fault(FAULT_STACK_USAGE_HIGH);
               // Consider entering degraded mode or resetting
           }
           
           vTaskDelay(pdMS_TO_TICKS(1000));  // Check every second
       }
   }

═══════════════════════════════════════════════════════════════════════

🚨 **5. SAFE STATE DESIGN**
─────────────────────────────────────────────────────────────────────────

**5.1 Safe State Principles**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Safe State Definition:
   ──────────────────────
   A system state where no hazard can occur, even if the system
   is non-functional or degraded.
   
   Characteristics:
   ────────────────
   ✓ Predictable behavior
   ✓ No risk of injury or damage
   ✓ Easy to achieve from any state
   ✓ Can be maintained indefinitely
   ✓ Allows safe system restart
   
   Examples by Domain:
   ───────────────────
   
   Motor Control:
   • Safe state: Motor OFF, brake engaged
   • Hazard: Unintended motion
   
   Elevator Control:
   • Safe state: Brakes engaged, doors locked
   • Hazard: Movement with doors open
   
   Airbag Controller:
   • Safe state: Squib disabled, capacitor discharged
   • Hazard: Unintended deployment
   
   Flight Control:
   • Safe state: Control surfaces neutral, alerts active
   • Hazard: Loss of control authority
   
   Industrial Robot:
   • Safe state: All axes stopped, power off, safety fence active
   • Hazard: Unexpected movement causing injury

**5.2 Safe State Implementation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Safe state state machine
   
   typedef enum {
       STATE_INIT,
       STATE_SELF_TEST,
       STATE_OPERATIONAL,
       STATE_DEGRADED,
       STATE_SAFE,
       STATE_FAULT
   } SystemState_t;
   
   SystemState_t current_state = STATE_INIT;
   
   // Safe state entry
   void enter_safe_state(FaultCode_t fault)
   {
       // Log fault for diagnostics
       log_fault(fault);
       
       // 1. Disable all actuators
       disable_all_outputs();
       
       // 2. Apply mechanical safeties
       engage_brakes();
       close_safety_relays();
       
       // 3. Discharge energy storage
       discharge_capacitors();
       
       // 4. Set all outputs to known safe values
       set_pwm_duty(0);
       set_gpio_outputs(SAFE_OUTPUT_PATTERN);
       
       // 5. Disable interrupts (optional, depending on system)
       // __disable_irq();
       
       // 6. Update state
       current_state = STATE_SAFE;
       
       // 7. Indicate fault to user
       set_fault_led(true);
       set_status_led(LED_RED);
       send_fault_message_to_hmi(fault);
       
       // 8. Stop feeding watchdog (trigger reset)
       // (Or continue if safe state should be maintained)
       
       // 9. Wait for manual intervention or automatic recovery
       while (current_state == STATE_SAFE) {
           // Monitor for recovery conditions
           if (recovery_button_pressed()) {
               attempt_recovery();
           }
           
           delay_ms(100);
       }
   }
   
   // Disable all actuator outputs
   void disable_all_outputs(void)
   {
       // Disable PWM outputs
       TIM1->CCER &= ~(TIM_CCER_CC1E | TIM_CCER_CC2E | 
                       TIM_CCER_CC3E | TIM_CCER_CC4E);
       
       // Set enable pins low
       GPIO_ResetBits(GPIOA, MOTOR_ENABLE_PIN);
       GPIO_ResetBits(GPIOB, SOLENOID_ENABLE_PIN);
       GPIO_ResetBits(GPIOC, HEATER_ENABLE_PIN);
       
       // Open safety relays (if normally closed = safe)
       GPIO_SetBits(GPIOD, SAFETY_RELAY_PIN);
   }
   
   // Mechanical safety engagement
   void engage_brakes(void)
   {
       // Engage electromagnetic brake (energize to release, de-energize to brake)
       GPIO_ResetBits(BRAKE_PORT, BRAKE_RELEASE_PIN);
       
       // Wait for brake engagement
       delay_ms(50);
       
       // Verify brake engaged (if sensor available)
       if (!is_brake_engaged()) {
           log_fault(FAULT_BRAKE_ENGAGEMENT_FAILED);
       }
   }
   
   // Recovery attempt (after fault cleared)
   void attempt_recovery(void)
   {
       // 1. Verify fault condition cleared
       if (!verify_fault_cleared()) {
           return;  // Cannot recover yet
       }
       
       // 2. Re-run self-tests
       current_state = STATE_SELF_TEST;
       
       if (!run_self_tests()) {
           enter_safe_state(FAULT_SELF_TEST_FAILED);
           return;
       }
       
       // 3. Reset fault counters (or don't, depending on policy)
       // reset_fault_counters();
       
       // 4. Transition to operational
       current_state = STATE_OPERATIONAL;
       
       log_event(EVENT_RECOVERY_SUCCESSFUL);
   }

**5.3 Graceful Degradation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Graceful degradation (fail-operational with reduced capability)
   
   typedef enum {
       CAPABILITY_FULL,
       CAPABILITY_REDUCED,
       CAPABILITY_MINIMAL,
       CAPABILITY_NONE
   } CapabilityLevel_t;
   
   CapabilityLevel_t current_capability = CAPABILITY_FULL;
   
   // Degrade system capability based on faults
   void evaluate_degradation(void)
   {
       int fault_count = count_active_faults();
       int sensor_failures = count_sensor_failures();
       
       if (sensor_failures >= 2) {
           // Multiple sensors failed, cannot operate safely
           degrade_to_level(CAPABILITY_NONE);
           enter_safe_state(FAULT_MULTIPLE_SENSORS);
       }
       else if (sensor_failures == 1) {
           // One sensor failed, can operate with reduced performance
           degrade_to_level(CAPABILITY_REDUCED);
       }
       else if (fault_count > 0) {
           // Minor faults present
           degrade_to_level(CAPABILITY_MINIMAL);
       }
       else {
           // No faults
           degrade_to_level(CAPABILITY_FULL);
       }
   }
   
   void degrade_to_level(CapabilityLevel_t level)
   {
       if (level == current_capability) return;
       
       current_capability = level;
       
       switch (level) {
           case CAPABILITY_FULL:
               // All features enabled
               max_speed = 100.0f;
               max_acceleration = 10.0f;
               enable_advanced_features();
               break;
               
           case CAPABILITY_REDUCED:
               // Reduced performance
               max_speed = 50.0f;
               max_acceleration = 5.0f;
               disable_advanced_features();
               set_warning_indicator(true);
               break;
               
           case CAPABILITY_MINIMAL:
               // Limp-home mode
               max_speed = 20.0f;
               max_acceleration = 2.0f;
               disable_all_optional_features();
               set_warning_indicator(true);
               break;
               
           case CAPABILITY_NONE:
               // Safe state
               enter_safe_state(FAULT_CAPABILITY_EXHAUSTED);
               break;
       }
       
       log_event(EVENT_CAPABILITY_CHANGED);
   }
   
   // Example: ADAS sensor fusion degradation
   void adas_sensor_fusion_degraded(void)
   {
       bool camera_ok = check_camera_health();
       bool radar_ok = check_radar_health();
       bool lidar_ok = check_lidar_health();
       
       int sensor_count = camera_ok + radar_ok + lidar_ok;
       
       if (sensor_count == 3) {
           // Full capability
           enable_lane_keeping();
           enable_adaptive_cruise();
           enable_collision_avoidance();
           enable_pedestrian_detection();
       }
       else if (sensor_count == 2) {
           // Reduced capability
           if (camera_ok && radar_ok) {
               // Camera + Radar: Most functions available
               enable_lane_keeping();
               enable_adaptive_cruise();
               enable_collision_avoidance();
               disable_pedestrian_detection();  // Needs lidar
           }
           else {
               // Other combinations: More limited
               disable_lane_keeping();
               enable_adaptive_cruise();  // Radar-only cruise
               enable_collision_avoidance();
               disable_pedestrian_detection();
           }
           
           display_warning("ADAS Limited Functionality");
       }
       else if (sensor_count == 1) {
           // Minimal capability
           disable_lane_keeping();
           disable_adaptive_cruise();
           enable_collision_avoidance();  // Basic radar/camera only
           disable_pedestrian_detection();
           
           display_warning("ADAS Severely Degraded");
       }
       else {
           // No sensors available
           disable_all_adas_functions();
           display_error("ADAS Unavailable - Manual Driving Only");
       }
   }

**5.4 Energy Dissipation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Safe discharge of stored energy
   
   // Capacitor discharge (e.g., airbag system)
   void discharge_capacitor_safe(void)
   {
       // 1. Disconnect charging circuit
       GPIO_ResetBits(CHARGE_ENABLE_PORT, CHARGE_ENABLE_PIN);
       
       // 2. Connect discharge resistor
       GPIO_SetBits(DISCHARGE_PORT, DISCHARGE_PIN);
       
       // 3. Monitor voltage during discharge
       const float SAFE_VOLTAGE = 5.0f;  // Volts
       uint32_t timeout = 5000;  // ms
       uint32_t start_time = get_tick_count_ms();
       
       while (get_tick_count_ms() - start_time < timeout) {
           float voltage = read_capacitor_voltage();
           
           if (voltage < SAFE_VOLTAGE) {
               // Discharge complete
               log_event(EVENT_CAPACITOR_DISCHARGED);
               return;
           }
           
           delay_ms(10);
       }
       
       // Timeout - capacitor did not discharge
       log_fault(FAULT_CAPACITOR_DISCHARGE_TIMEOUT);
   }
   
   // Motor coast-down (controlled deceleration)
   void motor_safe_stop(void)
   {
       // Option 1: Coast (passive deceleration)
       set_pwm_duty(0);
       disable_motor();
       
       // Option 2: Active braking (faster stop)
       // Short motor windings through low-side FETs
       set_low_side_fets(true);
       
       // Monitor speed
       uint32_t timeout = 2000;  // ms
       uint32_t start = get_tick_count_ms();
       
       while (get_tick_count_ms() - start < timeout) {
           float speed = read_motor_speed();
           
           if (speed < 1.0f) {  // Nearly stopped
               break;
           }
           
           delay_ms(10);
       }
       
       // Apply mechanical brake
       engage_mechanical_brake();
       
       // Disable all motor FETs
       disable_motor();
   }

═══════════════════════════════════════════════════════════════════════

🔐 **6. MEMORY PROTECTION**
─────────────────────────────────────────────────────────────────────────

**6.1 MPU Configuration (ARM Cortex-M)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Memory Protection Unit (MPU) configuration
   
   void mpu_init(void)
   {
       // Disable MPU during configuration
       MPU->CTRL = 0;
       
       // Region 0: Flash (read-only, executable)
       MPU->RBAR = 0x08000000 | MPU_RBAR_VALID_Msk | 0;  // Region 0
       MPU->RASR = (0x1D << MPU_RASR_SIZE_Pos) |  // 1 MB
                   (0x06 << MPU_RASR_AP_Pos) |     // Read-only
                   MPU_RASR_C_Msk |                // Cacheable
                   MPU_RASR_ENABLE_Msk;
       
       // Region 1: RAM (read-write, non-executable)
       MPU->RBAR = 0x20000000 | MPU_RBAR_VALID_Msk | 1;  // Region 1
       MPU->RASR = (0x11 << MPU_RASR_SIZE_Pos) |  // 128 KB
                   (0x03 << MPU_RASR_AP_Pos) |     // Read-write
                   MPU_RASR_C_Msk |                // Cacheable
                   MPU_RASR_XN_Msk |               // Non-executable (prevent code injection)
                   MPU_RASR_ENABLE_Msk;
       
       // Region 2: Critical data (read-write, guarded)
       MPU->RBAR = 0x20010000 | MPU_RBAR_VALID_Msk | 2;
       MPU->RASR = (0x0C << MPU_RASR_SIZE_Pos) |  // 8 KB
                   (0x03 << MPU_RASR_AP_Pos) |     // Read-write
                   MPU_RASR_C_Msk |
                   MPU_RASR_XN_Msk |
                   MPU_RASR_ENABLE_Msk;
       
       // Region 3: Stack (read-write, non-executable, with guard)
       MPU->RBAR = 0x20012000 | MPU_RBAR_VALID_Msk | 3;
       MPU->RASR = (0x0B << MPU_RASR_SIZE_Pos) |  // 4 KB
                   (0x03 << MPU_RASR_AP_Pos) |
                   MPU_RASR_XN_Msk |
                   MPU_RASR_ENABLE_Msk;
       
       // Enable MPU with default background region disabled
       MPU->CTRL = MPU_CTRL_ENABLE_Msk | MPU_CTRL_PRIVDEFENA_Msk;
       
       // Enable MemManage fault
       SCB->SHCSR |= SCB_SHCSR_MEMFAULTENA_Msk;
   }
   
   // MemManage fault handler (MPU violation)
   void MemManage_Handler(void)
   {
       uint32_t fault_addr = SCB->MMFAR;  // Faulting address
       
       log_fault(FAULT_MEMORY_PROTECTION);
       printf("MPU Violation at address 0x%08lX\n", fault_addr);
       
       // Cannot recover from MPU violation
       enter_safe_state(FAULT_MPU_VIOLATION);
       
       // Reset system
       NVIC_SystemReset();
   }

**6.2 Dual-Copy Critical Data**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   // Dual-copy data protection (detect corruption)
   
   typedef struct {
       uint32_t value;
       uint16_t crc;
   } ProtectedValue_t;
   
   typedef struct {
       ProtectedValue_t copy_a;
       ProtectedValue_t copy_b;
       ProtectedValue_t copy_c;  // Third copy for voting
   } TripleProtectedValue_t;
   
   // Write protected value (triple redundant with CRC)
   void write_protected_value(TripleProtectedValue_t *data, uint32_t value)
   {
       // Copy A
       data->copy_a.value = value;
       data->copy_a.crc = crc16_ccitt((uint8_t*)&value, sizeof(uint32_t));
       
       // Copy B
       data->copy_b.value = value;
       data->copy_b.crc = crc16_ccitt((uint8_t*)&value, sizeof(uint32_t));
       
       // Copy C
       data->copy_c.value = value;
       data->copy_c.crc = crc16_ccitt((uint8_t*)&value, sizeof(uint32_t));
   }
   
   // Read protected value (with error correction)
   bool read_protected_value(TripleProtectedValue_t *data, uint32_t *value)
   {
       // Verify CRCs
       bool a_valid = (crc16_ccitt((uint8_t*)&data->copy_a.value, sizeof(uint32_t)) 
                       == data->copy_a.crc);
       bool b_valid = (crc16_ccitt((uint8_t*)&data->copy_b.value, sizeof(uint32_t)) 
                       == data->copy_b.crc);
       bool c_valid = (crc16_ccitt((uint8_t*)&data->copy_c.value, sizeof(uint32_t)) 
                       == data->copy_c.crc);
       
       int valid_count = a_valid + b_valid + c_valid;
       
       if (valid_count == 0) {
           // All copies corrupted
           log_fault(FAULT_DATA_CORRUPTION_ALL);
           return false;
       }
       
       if (valid_count == 3) {
           // All valid, check if they agree
           if (data->copy_a.value == data->copy_b.value && 
               data->copy_b.value == data->copy_c.value) {
               *value = data->copy_a.value;
               return true;
           }
           
           // All valid but disagree - use majority
           if (data->copy_a.value == data->copy_b.value) {
               *value = data->copy_a.value;
               log_fault(FAULT_DATA_COPY_C_MISMATCH);
               // Repair copy C
               data->copy_c.value = *value;
               data->copy_c.crc = crc16_ccitt((uint8_t*)value, sizeof(uint32_t));
               return true;
           }
           
           if (data->copy_a.value == data->copy_c.value) {
               *value = data->copy_a.value;
               log_fault(FAULT_DATA_COPY_B_MISMATCH);
               // Repair copy B
               data->copy_b.value = *value;
               data->copy_b.crc = crc16_ccitt((uint8_t*)value, sizeof(uint32_t));
               return true;
           }
           
           if (data->copy_b.value == data->copy_c.value) {
               *value = data->copy_b.value;
               log_fault(FAULT_DATA_COPY_A_MISMATCH);
               // Repair copy A
               data->copy_a.value = *value;
               data->copy_a.crc = crc16_ccitt((uint8_t*)value, sizeof(uint32_t));
               return true;
           }
       }
       
       if (valid_count == 2) {
           // Two valid - use one and repair the other
           if (a_valid && b_valid) {
               if (data->copy_a.value == data->copy_b.value) {
                   *value = data->copy_a.value;
                   // Repair C
                   write_protected_value(data, *value);
                   log_fault(FAULT_DATA_COPY_C_CORRUPTED);
                   return true;
               }
           }
           // Similar for other combinations...
       }
       
       // Unrepairable
       log_fault(FAULT_DATA_CORRUPTION_UNREPAIRABLE);
       return false;
   }

═══════════════════════════════════════════════════════════════════════

🔀 **7. DIVERSE REDUNDANCY**
─────────────────────────────────────────────────────────────────────────

**7.1 Software Diversity**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Software Diversity (Defense against common-mode failures):
   
   Problem:
   ────────
   Triple redundancy with identical software can fail identically
   due to same software bug
   
   Solution: Diverse Implementation
   ─────────────────────────────────
   
   Channel A: Implementation 1 (Algorithm A, Compiler A)
   Channel B: Implementation 2 (Algorithm B, Compiler B)
   Channel C: Implementation 1 (Dissimilar to A and B)
   
   Example: Airbus A320 Flight Control
   ────────────────────────────────────
   • 2 channels: Primary flight control (Ada language)
   • 1 channel: Alternate law (Assembly language, different team)
   
   If both primary channels fail due to common bug,
   alternate law takes over with simpler, dissimilar implementation

**Diverse Algorithms Example:**

.. code-block:: c

   // Channel A: PID controller (standard implementation)
   float channel_a_compute_control(float setpoint, float measurement)
   {
       static float integral = 0.0f;
       static float last_error = 0.0f;
       
       float error = setpoint - measurement;
       
       float proportional = KP * error;
       integral += KI * error * DT;
       float derivative = KD * (error - last_error) / DT;
       
       last_error = error;
       
       float output = proportional + integral + derivative;
       
       // Saturation
       if (output > MAX_OUTPUT) output = MAX_OUTPUT;
       if (output < MIN_OUTPUT) output = MIN_OUTPUT;
       
       return output;
   }
   
   // Channel B: State-space controller (diverse implementation)
   float channel_b_compute_control(float setpoint, float measurement)
   {
       // State-space representation: x_dot = Ax + Bu, y = Cx
       static float state[2] = {0.0f, 0.0f};  // [position, velocity]
       
       // State feedback gain (computed offline via LQR)
       const float K[2] = {-15.0f, -3.0f};
       
       // Update state estimate
       state[0] = measurement;
       state[1] = (measurement - state[0]) / DT;  // Simple derivative
       
       // Compute control: u = -K*x + r
       float output = setpoint;
       output -= K[0] * state[0];
       output -= K[1] * state[1];
       
       // Saturation
       if (output > MAX_OUTPUT) output = MAX_OUTPUT;
       if (output < MIN_OUTPUT) output = MIN_OUTPUT;
       
       return output;
   }
   
   // Voting between diverse implementations
   float vote_diverse_controllers(float setpoint, float measurement)
   {
       float output_a = channel_a_compute_control(setpoint, measurement);
       float output_b = channel_b_compute_control(setpoint, measurement);
       
       #define DIVERSITY_TOLERANCE 5.0f
       
       if (fabs(output_a - output_b) < DIVERSITY_TOLERANCE) {
           // Agreement - use average
           return (output_a + output_b) / 2.0f;
       } else {
           // Disagreement - potential fault or algorithmic difference
           log_warning(WARNING_DIVERSE_CONTROLLER_MISMATCH);
           
           // Use more conservative output (depends on application)
           if (fabs(output_a) < fabs(output_b)) {
               return output_a;
           } else {
               return output_b;
           }
       }
   }

**7.2 Hardware Diversity**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Hardware Diversity:
   
   Different Microcontrollers:
   ───────────────────────────
   Channel A: STM32F4 (ARM Cortex-M4)
   Channel B: Infineon TC3xx (TriCore)
   Channel C: Renesas RH850 (V850)
   
   Benefits:
   • Different silicon bugs
   • Different peripheral implementations
   • Different compiler toolchains
   
   Different Sensors:
   ──────────────────
   Speed measurement:
   • Hall effect encoder (Channel A)
   • Optical encoder (Channel B)
   • Resolver (Channel C)
   
   Benefits:
   • Different failure modes
   • Different environmental sensitivities
   
   Different Communication Protocols:
   ──────────────────────────────────
   Command transmission:
   • CAN (Channel A)
   • SPI (Channel B)
   • UART (Channel C)
   
   Benefits:
   • Different EMI susceptibility
   • Different protocol vulnerabilities

═══════════════════════════════════════════════════════════════════════

📊 **8. PRACTICAL FMEA EXAMPLES**
─────────────────────────────────────────────────────────────────────────

**8.1 Motor Control System FMEA**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   System: Brushless DC Motor Controller (BLDC) for Electric Power Steering
   Safety Level: ASIL D (ISO 26262)
   
   Component         Failure Mode              Effect                  Severity  Prob  Detect  RPN  Mitigation
   ════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   Position Sensor   Open circuit              No position feedback    10        3     2       60   • Dual sensors with comparison
                                                                                                      • Plausibility check (rate limit)
                                                                                                      • Enter safe state if fault
   
   Position Sensor   Short to ground           Incorrect position      10        2     3       60   • Voltage range check
                                                                                                      • Cross-check with other sensors
   
   Position Sensor   Drift (uncalibrated)      Gradual position error  8         4     5       160  • Periodic calibration check
                                                                                                      • Home position verification
   
   Current Sensor    Stuck at zero             No current limiting     10        2     2       40   • Dual current sensors
                                                                                                      • Software current estimation
                                                                                                      • Timeout protection
   
   PWM Driver        Stuck high                Continuous full power   10        1     1       10   • Hardware overcurrent protection
                                                                                                      • Watchdog monitoring
                                                                                                      • Thermal shutdown
   
   PWM Driver        Stuck low                 No motor drive          6         1     1       6    • Dual H-bridge
                                                                                                      • Diagnostic self-test
   
   Microcontroller   Software runaway          Unpredictable behavior  10        2     2       40   • Hardware watchdog
                                                                                                      • Stack canary
                                                                                                      • Code CRC check
   
   Microcontroller   Stack overflow            System crash            10        3     3       90   • Stack usage monitoring
                                                                                                      • MPU guard pages
                                                                                                      • Static analysis
   
   Power Supply      Overvoltage (>16V)        Component damage        8         2     2       32   • Overvoltage clamp (TVS)
                                                                                                      • Voltage monitoring
                                                                                                      • Shutdown on overvoltage
   
   Power Supply      Undervoltage (<9V)        Loss of function        7         3     1       21   • Brown-out detection
                                                                                                      • Graceful shutdown
                                                                                                      • Capacitor hold-up time
   
   Communication     CAN bus off               No external commands    9         2     1       18   • CAN error detection
   (CAN)                                                                                             • Automatic bus recovery
                                                                                                      • Timeout on commands
   
   Temperature       Over-temperature          Thermal damage          9         3     2       54   • Temperature monitoring
   Sensor                                                                                            • Thermal model (estimate)
                                                                                                      • Forced shutdown >85°C
   
   Gate Driver       Shoot-through             Short circuit           10        1     1       10   • Dead-time insertion (hardware)
                                                                                                      • Interlock logic
                                                                                                      • Overcurrent shutdown
   
   Legend:
   Severity:     1-10 (10 = catastrophic)
   Probability:  1-5 (5 = very likely)
   Detectability: 1-5 (1 = easily detected, 5 = undetectable)
   RPN = Severity × Probability × Detectability
   
   High RPN items (>100) require design changes to reduce risk

**8.2 Avionics Fuel Controller FMEA**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   System: Aircraft Fuel Controller
   Safety Level: DO-178C Level A
   
   Function: Fuel Flow Control
   Hazard: Loss of engine power, uncontrolled fuel flow
   
   Component            Failure Mode           Effect                    DAL    Mitigation
   ═══════════════════════════════════════════════════════════════════════════════════════
   Fuel Flow Sensor     Open circuit           No fuel feedback          A      • Dual sensors (A/B)
                                                                                 • Cross-check with RPM
                                                                                 • Model-based estimation
   
   Fuel Flow Sensor     Out of range high      Incorrect fuel reading    A      • Range checking (0-1000 gal/hr)
                                                                                 • Rate limit (max change 100 gal/hr/sec)
                                                                                 • Comparison with calculated flow
   
   Fuel Valve Actuator  Stuck open             Excessive fuel flow       A      • Dual valves in series
                                                                                 • Flow monitoring
                                                                                 • Shutdown valve (independent)
   
   Fuel Valve Actuator  Stuck closed           Engine fuel starvation    A      • Parallel redundant valve
                                                                                 • Position feedback
                                                                                 • Manual override
   
   Software             Infinite loop          Loss of fuel control      A      • Hardware watchdog (100 ms timeout)
                                                                                 • Software watchdog (task monitoring)
                                                                                 • DO-178C Level A development
   
   Software             Incorrect calculation  Wrong fuel flow           A      • Dual-channel computation
                                                                                 • Cross-channel comparison
                                                                                 • 100% MC/DC coverage
                                                                                 • Back-to-back testing (MIL/SIL/PIL/HIL)
   
   Communication        ARINC-429 failure      No fuel commands          A      • Dual ARINC-429 buses
                                                                                 • Timeout detection (200 ms)
                                                                                 • Revert to safe fuel flow
   
   Power Supply         Loss of power          Loss of fuel control      A      • Dual power supplies (28V DC)
                                                                                 • Automatic switchover
                                                                                 • Capacitor hold-up (50 ms)
   
   Processor            Single event upset     Data corruption           A      • ECC memory
   (Radiation)                                                                  • Triple modular redundancy (TMR)
                                                                                 • Scrubbing (error correction)

═══════════════════════════════════════════════════════════════════════

🎯 **9. INTERVIEW PREPARATION**
─────────────────────────────────────────────────────────────────────────

**9.1 Your Safety-Critical Experience**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Projects to Highlight:
   ──────────────────────
   
   1. Avionics Fuel Controller (DO-178B Level A):
   ───────────────────────────────────────────────
   • Dual-channel redundancy with cross-checking
   • Watchdog monitoring (hardware + software)
   • Safe state: Fuel valve to idle position
   • FMEA analysis: Identified 47 failure modes
   • Fault detection: Sensor plausibility, CRC on critical data
   • Tool qualification: MATLAB Embedded Coder (DO-330 TQL-1)
   
   2. Automotive ADAS (ISO 26262 ASIL B):
   ───────────────────────────────────────
   • Sensor fusion with cross-validation (camera, radar, lidar)
   • Graceful degradation: Full → Reduced → Minimal capability
   • Watchdog monitoring of sensor processing tasks
   • Safe state: Disable autonomous features, alert driver
   • FMEA: Sensor failures, software faults, communication errors
   
   3. Industrial Gateway (Functional Safety):
   ──────────────────────────────────────────
   • Dual-channel safety architecture for emergency stop
   • Watchdog with health monitoring (stack, task execution)
   • Safe state: De-energize all outputs, engage mechanical brakes
   • Memory protection: MPU regions for critical data
   • CRC protection on configuration parameters
   
   4. Smart Home Platform (Security-Critical):
   ───────────────────────────────────────────
   • Secure boot with HAB (High Assurance Boot)
   • Watchdog for firmware hang detection
   • Safe state: Disconnect network, factory reset capability
   • OTA update with dual-partition rollback
   • Fail-safe firmware recovery

**9.2 Technical Interview Questions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Q: "Explain dual-channel vs triple-redundancy. When would you use each?"
   
   A: "Dual-channel redundancy uses two independent systems with comparison. 
   If they disagree, the system enters a safe state. It's fail-safe - it 
   detects faults but cannot continue operating. I used this on industrial 
   safety systems where the safe action is to shut down.
   
   Triple redundancy (TMR) uses three channels with 2-out-of-3 voting. 
   If one channel fails, the other two outvote it and the system continues. 
   It's fail-operational - tolerates one failure. I've seen this in flight 
   control systems where continued operation is critical.
   
   The choice depends on safety requirements:
   • Fail-safe acceptable? → Dual-channel (lower cost)
   • Must remain operational? → Triple redundancy (higher cost, complexity)
   
   For the avionics fuel controller, we used dual-channel because entering 
   a safe fuel flow state was acceptable, whereas flight control needs TMR 
   to maintain aircraft control."
   
   ---
   
   Q: "How do you implement a safe state?"
   
   A: "A safe state is where the system cannot cause harm even if non-functional. 
   Implementation depends on the system:
   
   For the motor controller project:
   1. Disable all PWM outputs (no power to motor)
   2. Engage mechanical brake (de-energize electromagnetic brake)
   3. Discharge energy storage (capacitors)
   4. Set all GPIOs to safe values
   5. Update state machine to SAFE state
   6. Indicate fault (LED, CAN message)
   7. Stop feeding watchdog (triggers reset for recovery attempt)
   
   The key is ensuring the safe state can be reached from ANY operational state, 
   even if the system is partially failed. For example, if software crashes, 
   the hardware watchdog timeout will disable outputs via dedicated circuitry.
   
   I also use MPU (Memory Protection Unit) to prevent code execution from RAM, 
   which protects against certain fault conditions."
   
   ---
   
   Q: "Explain watchdog monitoring strategy"
   
   A: "I use a layered watchdog approach:
   
   Layer 1: Hardware watchdog (external IC or MCU IWDG)
   • Independent of software (cannot be disabled)
   • 1-second timeout
   • Triggers system reset if not refreshed
   
   Layer 2: Software watchdog (task monitoring)
   • RTOS task that monitors other tasks
   • Each critical task checks in periodically
   • If any task misses check-in, software watchdog doesn't refresh hardware watchdog
   • Catches deadlocks, infinite loops, task crashes
   
   Layer 3: Health monitoring (before watchdog refresh)
   • Check stack usage (<80% threshold)
   • Verify sensor data validity
   • Check communication timeouts
   • Only refresh watchdog if ALL health checks pass
   
   For the avionics project, we also used window watchdog (WWDG) which triggers 
   if refreshed too early OR too late. This catches runaway fast loops that 
   a standard watchdog would miss.
   
   The philosophy: Watchdog is not just a timeout, it's a health verification gate."
   
   ---
   
   Q: "How do you handle sensor failures?"
   
   A: "Multi-layered approach:
   
   1. Redundancy:
   • Dual sensors for critical measurements (e.g., motor position)
   • Diverse sensor types (encoder + resolver)
   
   2. Plausibility checks:
   • Range: Value within physically possible limits (-40°C to 150°C)
   • Rate: Change rate within physical limits (10°C/sec max for temperature)
   • Stuck detection: Value unchanged for >5 seconds
   
   3. Cross-correlation:
   • Compare related sensors (wheel speed vs GPS vs accelerometer)
   • Use sensor fusion (Kalman filter gives statistical confidence)
   
   4. Graceful degradation:
   • One sensor failed: Switch to backup, continue operation
   • Two sensors failed: Enter degraded mode (reduced performance)
   • All sensors failed: Safe state
   
   For ADAS sensor fusion, we had camera, radar, and lidar. Loss of one sensor 
   degraded functionality but didn't disable the system. For example, losing 
   lidar disabled pedestrian detection but kept lane-keeping (camera+radar).
   
   The key is defining degradation levels: Full → Reduced → Minimal → Safe State."
   
   ---
   
   Q: "Explain your FMEA experience"
   
   A: "FMEA (Failure Mode and Effects Analysis) is bottom-up hazard analysis. 
   For each component, we identify failure modes, effects, and mitigations.
   
   Process I followed on the fuel controller project:
   
   1. Identify components: Sensors, actuators, MCU, power supply, software modules
   
   2. For each component, list failure modes:
      • Sensor: Open circuit, short circuit, drift, noise
      • Actuator: Stuck open, stuck closed, slow response
      • Software: Runaway, deadlock, stack overflow, incorrect calculation
   
   3. Analyze effects:
      • Local: Component itself
      • System: Impact on system function
      • Safety: Hazard analysis
   
   4. Assign severity, probability, detectability (RPN calculation)
   
   5. Define mitigations:
      • Redundancy (dual sensors)
      • Monitoring (plausibility checks)
      • Safe state (shutdown on fault)
      • Design changes (if RPN >100)
   
   6. Verification:
      • Test each failure mode (fault injection)
      • Verify mitigation works
      • Document in test results
   
   For DO-178C Level A, we had to show that all credible failure modes with 
   catastrophic effects had mitigations achieving <10⁻⁹ probability per flight hour. 
   This drove our dual-channel architecture with cross-checking."

**9.3 Design Pattern Selection Guide**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   When to Use Each Pattern:
   
   Dual-Channel Redundancy:
   ────────────────────────
   ✓ Safety-critical industrial controls
   ✓ Railway signaling
   ✓ Airbag deployment logic
   ✓ When fail-safe (shutdown) is acceptable
   ✓ Cost-sensitive applications
   
   Triple Modular Redundancy (TMR):
   ─────────────────────────────────
   ✓ Flight control systems
   ✓ Spacecraft computers
   ✓ Nuclear reactor control
   ✓ When fail-operational is required
   ✓ High-reliability requirements
   
   Hardware Watchdog:
   ──────────────────
   ✓ All safety-critical systems
   ✓ Independent fault detection
   ✓ Software hang/crash protection
   ✓ Mandatory for automotive ASIL C/D
   
   Software Watchdog (Task Monitoring):
   ─────────────────────────────────────
   ✓ RTOS-based systems
   ✓ Multi-task safety monitoring
   ✓ Deadlock detection
   ✓ Complements hardware watchdog
   
   Plausibility Checks:
   ────────────────────
   ✓ All sensor inputs
   ✓ Range, rate, correlation validation
   ✓ Low overhead, high effectiveness
   ✓ Required for ISO 26262, DO-178C
   
   Memory Protection (MPU):
   ────────────────────────
   ✓ Systems with ARM Cortex-M4+ or better
   ✓ Prevent code injection attacks
   ✓ Stack overflow detection
   ✓ Critical data protection
   
   Graceful Degradation:
   ─────────────────────
   ✓ Systems with multiple capability levels
   ✓ ADAS, avionics navigation
   ✓ User experience important
   ✓ Partial functionality acceptable
   
   Diverse Redundancy:
   ───────────────────
   ✓ Protection against common-mode failures
   ✓ Highest safety levels (DO-178C Level A, ASIL D)
   ✓ When software bugs are concern
   ✓ Budget allows for complexity

═══════════════════════════════════════════════════════════════════════

**✅ SAFETY-CRITICAL DESIGN PATTERNS COMPLETE**

**Total:** 2,100 lines across 2 parts

**Part 1 (1,500 lines):**
- Fundamentals: Safety vs reliability, hazard analysis (FMEA, FTA), SIL levels
- Redundancy patterns: Dual-channel, TMR, quad with voting
- Watchdog patterns: Hardware, software task monitoring, window watchdog
- Fault detection: Plausibility checks, correlation, CRC, stack protection

**Part 2 (600 lines):**
- Safe state design: Entry procedures, energy dissipation, recovery
- Graceful degradation: Capability levels, ADAS sensor fusion example
- Memory protection: MPU configuration, dual-copy critical data
- Diverse redundancy: Software (algorithms, languages), hardware (MCUs, sensors)
- Practical FMEA: Motor controller (ASIL D), avionics fuel controller (Level A)
- Interview preparation: Resume mapping, technical Q&A, pattern selection

**Mapped to Your Experience:**
- DO-178B Level A: Avionics fuel controller (dual-channel, watchdog, FMEA)
- ISO 26262 ASIL B: ADAS sensor fusion (graceful degradation, plausibility)
- Industrial safety: Emergency stop dual-channel, watchdog monitoring
- i.MX 93: Secure boot (HAB), watchdog, safe firmware recovery

**Complete Coverage:**
All major safety-critical design patterns with production C code, practical 
FMEA examples, and interview talking points demonstrating 18 years of 
safety-critical embedded systems experience.

═══════════════════════════════════════════════════════════════════════
