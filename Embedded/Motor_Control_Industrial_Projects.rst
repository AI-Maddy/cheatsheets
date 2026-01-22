================================================================================
Motor Control & Industrial Systems - Project Experience
================================================================================

:Author: Madhavan Vivekanandan
:Date: January 21, 2026
:Projects: Industrial Motor Controllers, Thermal Imaging, HVAC Systems
:Domains: Industrial Automation, Building Management, Defense/Aerospace

================================================================================
Overview
================================================================================

This document captures hands-on implementation of motor control systems and
industrial automation across 5 major projects:

**Projects:**
1. **BLDC Motor Controller** - Industrial pumps/fans
2. **Servo Motor Control** - Aircraft actuation systems
3. **HVAC Variable Speed Drive** - Water heater control
4. **Thermal Imaging Camera** - Defense applications
5. **Motor Control Energy Optimization** - Energy Star compliance

**Standards:** IEC 61131-3, IEC 61508, IEC 60730, IEC 61800, Modbus RTU/TCP,
OPC UA, Energy Star, UL 508C

================================================================================
BLDC Motor Control - Sensorless Field-Oriented Control (FOC)
================================================================================

Project: Industrial Pump Controller
--------------------------------------------------------------------------------

**Hardware:**
- MCU: STM32F405 (ARM Cortex-M4, 168 MHz, FPU)
- Motor: 3-phase BLDC (500W, 24V, 4-pole pairs)
- Gate Driver: IR2136 (3-phase half-bridge)
- Current Sensing: ACS712 Hall-effect sensors (Ia, Ib, Ic)
- Position Sensing: Sensorless (Back-EMF estimation)

**Control Architecture:**

::

    ┌──────────────────────────────────────────────────────────────┐
    │                    Speed Reference (RPM)                     │
    └───────────────────────────┬──────────────────────────────────┘
                                │
    ┌───────────────────────────▼──────────────────────────────────┐
    │           Speed PI Controller                                │
    │           Kp=0.5, Ki=0.1, Output: Torque Reference (Iq*)    │
    └───────────────────────────┬──────────────────────────────────┘
                                │
    ┌───────────────────────────▼──────────────────────────────────┐
    │                  Current Reference (Id*, Iq*)                │
    │                  Id* = 0 (for SPMSM)                         │
    └────────────┬─────────────────────────────┬────────────────────┘
                 │                             │
    ┌────────────▼──────────┐     ┌────────────▼──────────────────┐
    │  Current PI (d-axis)  │     │  Current PI (q-axis)          │
    │  Kp=5.0, Ki=500       │     │  Kp=5.0, Ki=500               │
    │  Output: Vd           │     │  Output: Vq                   │
    └────────────┬──────────┘     └────────────┬──────────────────┘
                 │                             │
    ┌────────────▼─────────────────────────────▼──────────────────┐
    │         Inverse Park Transform (dq → αβ)                    │
    │         Requires: Electrical Angle (θe)                     │
    └────────────┬─────────────────────────────────────────────────┘
                 │
    ┌────────────▼─────────────────────────────────────────────────┐
    │         Space Vector Modulation (SVM)                        │
    │         Output: PWM Duty Cycles (Ta, Tb, Tc)                │
    └────────────┬─────────────────────────────────────────────────┘
                 │
    ┌────────────▼─────────────────────────────────────────────────┐
    │         Three-Phase Inverter (IR2136)                        │
    │         20 kHz PWM, 2µs dead-time                            │
    └──────────────────────────────────────────────────────────────┘
                 │
    ┌────────────▼─────────────────────────────────────────────────┐
    │              BLDC Motor (3-phase)                            │
    └──────────────────────────────────────────────────────────────┘
                 │ (Back-EMF)
    ┌────────────▼─────────────────────────────────────────────────┐
    │      Back-EMF Observer (Sensorless Position)                │
    │      Estimates: θe (electrical angle), ωe (speed)           │
    └──────────────────────────────────────────────────────────────┘

FOC Algorithm Implementation
--------------------------------------------------------------------------------

**1. Clarke Transform (abc → αβ)**

Converts 3-phase currents to 2-phase stationary frame.

.. code-block:: c

    // Clarke Transform
    typedef struct {
        float alpha;
        float beta;
    } AlphaBeta_t;
    
    void Clarke_Transform(float Ia, float Ib, float Ic, AlphaBeta_t *ab) {
        // Simplified Clarke (assuming balanced 3-phase)
        ab->alpha = Ia;
        ab->beta = (Ia + 2.0f * Ib) / sqrtf(3.0f);
        
        // Full Clarke (if Ic independent):
        // ab->alpha = (2.0f/3.0f) * (Ia - 0.5f*Ib - 0.5f*Ic);
        // ab->beta = (2.0f/3.0f) * (0.866f*Ib - 0.866f*Ic);
    }

**2. Park Transform (αβ → dq)**

Transforms to rotating reference frame aligned with rotor flux.

.. code-block:: c

    typedef struct {
        float d;  // Direct axis (flux component)
        float q;  // Quadrature axis (torque component)
    } DQ_t;
    
    void Park_Transform(AlphaBeta_t *ab, float theta_e, DQ_t *dq) {
        float cos_theta = arm_cos_f32(theta_e);
        float sin_theta = arm_sin_f32(theta_e);
        
        dq->d =  ab->alpha * cos_theta + ab->beta * sin_theta;
        dq->q = -ab->alpha * sin_theta + ab->beta * cos_theta;
    }

**3. PI Controllers (d-axis and q-axis)**

.. code-block:: c

    typedef struct {
        float Kp;
        float Ki;
        float integral;
        float output_min;
        float output_max;
    } PI_Controller_t;
    
    float PI_Update(PI_Controller_t *pi, float reference, float measurement, float dt) {
        float error = reference - measurement;
        
        // Proportional term
        float p_term = pi->Kp * error;
        
        // Integral term (with anti-windup)
        pi->integral += error * dt;
        float i_term = pi->Ki * pi->integral;
        
        // Output
        float output = p_term + i_term;
        
        // Anti-windup clamping
        if (output > pi->output_max) {
            output = pi->output_max;
            pi->integral -= error * dt;  // Back-calculate
        } else if (output < pi->output_min) {
            output = pi->output_min;
            pi->integral -= error * dt;
        }
        
        return output;
    }
    
    // Current loop PI controllers (d and q axes)
    PI_Controller_t pi_d = { .Kp = 5.0f, .Ki = 500.0f, .output_min = -24.0f, .output_max = 24.0f };
    PI_Controller_t pi_q = { .Kp = 5.0f, .Ki = 500.0f, .output_min = -24.0f, .output_max = 24.0f };
    
    void Current_Loop_Control(DQ_t *current_ref, DQ_t *current_meas, DQ_t *voltage_out, float dt) {
        voltage_out->d = PI_Update(&pi_d, current_ref->d, current_meas->d, dt);
        voltage_out->q = PI_Update(&pi_q, current_ref->q, current_meas->q, dt);
    }

**4. Inverse Park Transform (dq → αβ)**

.. code-block:: c

    void Inverse_Park_Transform(DQ_t *dq, float theta_e, AlphaBeta_t *ab) {
        float cos_theta = arm_cos_f32(theta_e);
        float sin_theta = arm_sin_f32(theta_e);
        
        ab->alpha = dq->d * cos_theta - dq->q * sin_theta;
        ab->beta  = dq->d * sin_theta + dq->q * cos_theta;
    }

**5. Space Vector Modulation (SVM)**

Generates optimal PWM duty cycles for 3-phase inverter.

.. code-block:: c

    typedef struct {
        uint16_t duty_a;  // Phase A duty cycle (0-1000)
        uint16_t duty_b;  // Phase B duty cycle
        uint16_t duty_c;  // Phase C duty cycle
    } PWM_Duty_t;
    
    #define PWM_PERIOD 1000  // Timer period (0-1000)
    
    void Space_Vector_Modulation(AlphaBeta_t *ab, float v_dc, PWM_Duty_t *pwm) {
        // Normalize voltages
        float v_alpha_norm = ab->alpha / v_dc;
        float v_beta_norm = ab->beta / v_dc;
        
        // Calculate sector (1-6)
        float angle = atan2f(v_beta_norm, v_alpha_norm);
        if (angle < 0) angle += 2.0f * PI;
        uint8_t sector = (uint8_t)(angle / (PI / 3.0f)) + 1;
        
        // Calculate reference voltage magnitude
        float v_ref_mag = sqrtf(v_alpha_norm * v_alpha_norm + v_beta_norm * v_beta_norm);
        
        // Time calculation for active vectors
        float t1, t2, t0;
        float sqrt3 = 1.732050808f;
        
        switch (sector) {
            case 1:
                t1 = v_ref_mag * sinf(PI/3.0f - angle);
                t2 = v_ref_mag * sinf(angle);
                break;
            case 2:
                t1 = v_ref_mag * sinf(angle - PI/3.0f);
                t2 = v_ref_mag * sinf(2.0f*PI/3.0f - angle);
                break;
            // ... cases 3-6
        }
        
        t0 = 1.0f - t1 - t2;  // Zero vector time
        
        // Calculate duty cycles (space vector PWM)
        float ta, tb, tc;
        switch (sector) {
            case 1:
                ta = t1 + t2 + t0/2.0f;
                tb = t2 + t0/2.0f;
                tc = t0/2.0f;
                break;
            case 2:
                ta = t1 + t0/2.0f;
                tb = t1 + t2 + t0/2.0f;
                tc = t0/2.0f;
                break;
            // ... cases 3-6
        }
        
        // Convert to timer compare values
        pwm->duty_a = (uint16_t)(ta * PWM_PERIOD);
        pwm->duty_b = (uint16_t)(tb * PWM_PERIOD);
        pwm->duty_c = (uint16_t)(tc * PWM_PERIOD);
    }

**6. Sensorless Position Estimation (Back-EMF Observer)**

.. code-block:: c

    typedef struct {
        float theta_e;      // Estimated electrical angle
        float omega_e;      // Estimated electrical speed
        float bemf_alpha;   // Back-EMF alpha component
        float bemf_beta;    // Back-EMF beta component
    } BackEMF_Observer_t;
    
    void BackEMF_Estimator(AlphaBeta_t *v_ab, AlphaBeta_t *i_ab, 
                           BackEMF_Observer_t *observer, float dt) {
        // Motor parameters
        const float Rs = 0.5f;    // Stator resistance (Ohm)
        const float Ls = 0.001f;  // Stator inductance (H)
        
        // Back-EMF calculation: e = v - Rs*i - Ls*di/dt
        static AlphaBeta_t i_ab_prev = {0, 0};
        
        float di_alpha = (i_ab->alpha - i_ab_prev.alpha) / dt;
        float di_beta = (i_ab->beta - i_ab_prev.beta) / dt;
        
        observer->bemf_alpha = v_ab->alpha - Rs * i_ab->alpha - Ls * di_alpha;
        observer->bemf_beta = v_ab->beta - Rs * i_ab->beta - Ls * di_beta;
        
        // Angle estimation from back-EMF
        observer->theta_e = atan2f(observer->bemf_beta, observer->bemf_alpha);
        if (observer->theta_e < 0) observer->theta_e += 2.0f * PI;
        
        // Speed estimation (derivative of angle)
        static float theta_prev = 0;
        observer->omega_e = (observer->theta_e - theta_prev) / dt;
        theta_prev = observer->theta_e;
        
        // Low-pass filter for noise reduction
        static float omega_filtered = 0;
        const float alpha_lpf = 0.1f;
        omega_filtered = alpha_lpf * observer->omega_e + (1.0f - alpha_lpf) * omega_filtered;
        observer->omega_e = omega_filtered;
        
        i_ab_prev = *i_ab;
    }

**7. Main FOC Control Loop (10 kHz)**

.. code-block:: c

    void FOC_Control_Loop(void) {
        const float dt = 0.0001f;  // 10 kHz = 100µs period
        
        // 1. Read phase currents (ADC)
        float Ia = Read_Current_A();
        float Ib = Read_Current_B();
        float Ic = -(Ia + Ib);  // Kirchhoff's law
        
        // 2. Clarke Transform (abc → αβ)
        AlphaBeta_t i_ab;
        Clarke_Transform(Ia, Ib, Ic, &i_ab);
        
        // 3. Back-EMF estimation for position
        BackEMF_Observer_t observer;
        AlphaBeta_t v_ab_prev;  // Previous voltage commands
        BackEMF_Estimator(&v_ab_prev, &i_ab, &observer, dt);
        
        // 4. Park Transform (αβ → dq)
        DQ_t i_dq;
        Park_Transform(&i_ab, observer.theta_e, &i_dq);
        
        // 5. Speed control (outer loop, 1 kHz)
        static uint16_t speed_loop_counter = 0;
        static float torque_ref = 0;
        if (++speed_loop_counter >= 10) {  // Every 10 cycles = 1ms
            speed_loop_counter = 0;
            
            float speed_ref_rpm = Get_Speed_Reference();
            float speed_rpm = observer.omega_e * 60.0f / (2.0f * PI * POLE_PAIRS);
            
            PI_Controller_t pi_speed = { .Kp = 0.5f, .Ki = 0.1f, 
                                          .output_min = -10.0f, .output_max = 10.0f };
            torque_ref = PI_Update(&pi_speed, speed_ref_rpm, speed_rpm, 0.001f);
        }
        
        // 6. Current references
        DQ_t i_ref = { .d = 0.0f, .q = torque_ref };  // Id=0 for SPMSM
        
        // 7. Current control (inner loop)
        DQ_t v_dq;
        Current_Loop_Control(&i_ref, &i_dq, &v_dq, dt);
        
        // 8. Inverse Park Transform (dq → αβ)
        AlphaBeta_t v_ab;
        Inverse_Park_Transform(&v_dq, observer.theta_e, &v_ab);
        v_ab_prev = v_ab;
        
        // 9. Space Vector Modulation
        PWM_Duty_t pwm;
        Space_Vector_Modulation(&v_ab, 24.0f, &pwm);  // 24V DC bus
        
        // 10. Update PWM registers
        TIM1->CCR1 = pwm.duty_a;
        TIM1->CCR2 = pwm.duty_b;
        TIM1->CCR3 = pwm.duty_c;
    }

Startup Sequence (Open-Loop to Closed-Loop Transition)
--------------------------------------------------------------------------------

Sensorless FOC requires initial rotor alignment and acceleration.

.. code-block:: c

    typedef enum {
        MOTOR_IDLE,
        MOTOR_ALIGNMENT,
        MOTOR_OPEN_LOOP,
        MOTOR_CLOSED_LOOP,
        MOTOR_FAULT
    } Motor_State_t;
    
    Motor_State_t motor_state = MOTOR_IDLE;
    
    void Motor_Startup_StateMachine(void) {
        static uint32_t state_timer = 0;
        static float open_loop_angle = 0;
        
        switch (motor_state) {
            case MOTOR_IDLE:
                if (Start_Command_Received()) {
                    motor_state = MOTOR_ALIGNMENT;
                    state_timer = 0;
                }
                break;
            
            case MOTOR_ALIGNMENT:
                // Apply DC current to align rotor to known position
                DQ_t i_ref = { .d = 0.0f, .q = 2.0f };  // 2A alignment current
                DQ_t v_dq = { .d = 0.0f, .q = 5.0f };
                
                AlphaBeta_t v_ab;
                Inverse_Park_Transform(&v_dq, 0.0f, &v_ab);  // θ = 0° alignment
                
                PWM_Duty_t pwm;
                Space_Vector_Modulation(&v_ab, 24.0f, &pwm);
                Set_PWM_Duty(pwm);
                
                if (state_timer++ > 1000) {  // 1 second alignment
                    motor_state = MOTOR_OPEN_LOOP;
                    state_timer = 0;
                    open_loop_angle = 0;
                }
                break;
            
            case MOTOR_OPEN_LOOP:
                // Ramp up speed in open-loop (no position feedback)
                open_loop_angle += 0.01f;  // Slow ramp
                if (open_loop_angle > 2.0f * PI) open_loop_angle -= 2.0f * PI;
                
                DQ_t i_ref_ol = { .d = 0.0f, .q = 3.0f };  // 3A torque current
                DQ_t v_dq_ol = { .d = 0.0f, .q = 10.0f };
                
                AlphaBeta_t v_ab_ol;
                Inverse_Park_Transform(&v_dq_ol, open_loop_angle, &v_ab_ol);
                
                PWM_Duty_t pwm_ol;
                Space_Vector_Modulation(&v_ab_ol, 24.0f, &pwm_ol);
                Set_PWM_Duty(pwm_ol);
                
                // Transition to closed-loop when back-EMF sufficient
                BackEMF_Observer_t observer;
                if (observer.omega_e > 100.0f) {  // 100 rad/s minimum speed
                    motor_state = MOTOR_CLOSED_LOOP;
                }
                break;
            
            case MOTOR_CLOSED_LOOP:
                // Normal FOC operation (sensorless)
                FOC_Control_Loop();
                break;
            
            case MOTOR_FAULT:
                // Fault handling (overcurrent, overvoltage, etc.)
                Disable_PWM();
                break;
        }
    }

================================================================================
Servo Motor Control - Aircraft Actuation
================================================================================

Project: AFCU (Aircraft Fuel Control Unit)
--------------------------------------------------------------------------------

**Hardware:**
- MCU: Freescale MPC5643L (Power Architecture, Dual-Core)
- Motor: Brushed DC Servo with encoder (1024 PPR)
- H-Bridge: L6234 (2A continuous, 5A peak)
- Position Feedback: Incremental encoder + potentiometer (redundant)
- Communication: ARINC-429

**Control:** Cascaded PID (Position → Velocity → Current)

.. code-block:: c

    // Cascaded PID Control
    typedef struct {
        float Kp, Ki, Kd;
        float integral, derivative;
        float prev_error;
        float output_min, output_max;
    } PID_Controller_t;
    
    float PID_Update(PID_Controller_t *pid, float setpoint, float measurement, float dt) {
        float error = setpoint - measurement;
        
        // Proportional
        float p_term = pid->Kp * error;
        
        // Integral (with anti-windup)
        pid->integral += error * dt;
        float i_term = pid->Ki * pid->integral;
        
        // Derivative (with low-pass filter)
        pid->derivative = (error - pid->prev_error) / dt;
        float d_term = pid->Kd * pid->derivative;
        
        // Output
        float output = p_term + i_term + d_term;
        
        // Clamping
        if (output > pid->output_max) {
            output = pid->output_max;
            pid->integral -= error * dt;  // Anti-windup
        } else if (output < pid->output_min) {
            output = pid->output_min;
            pid->integral -= error * dt;
        }
        
        pid->prev_error = error;
        return output;
    }
    
    // Control loop (1 kHz)
    void Servo_Control_Loop(void) {
        const float dt = 0.001f;  // 1 ms
        
        // Read position feedback
        int32_t encoder_counts = Read_Encoder();
        float position_deg = (encoder_counts * 360.0f) / (1024.0f * 4.0f);  // Quadrature
        
        // Read velocity (from encoder derivative)
        static float position_prev = 0;
        float velocity_dps = (position_deg - position_prev) / dt;
        position_prev = position_deg;
        
        // Outer loop: Position PID
        static PID_Controller_t pid_pos = {
            .Kp = 10.0f, .Ki = 0.5f, .Kd = 0.1f,
            .output_min = -500.0f, .output_max = 500.0f
        };
        float position_ref = Get_Position_Command();  // From ARINC-429
        float velocity_ref = PID_Update(&pid_pos, position_ref, position_deg, dt);
        
        // Middle loop: Velocity PID
        static PID_Controller_t pid_vel = {
            .Kp = 0.5f, .Ki = 0.1f, .Kd = 0.01f,
            .output_min = -5.0f, .output_max = 5.0f
        };
        float current_ref = PID_Update(&pid_vel, velocity_ref, velocity_dps, dt);
        
        // Inner loop: Current control (H-bridge PWM)
        float current_meas = Read_Motor_Current();
        static PID_Controller_t pid_curr = {
            .Kp = 2.0f, .Ki = 50.0f, .Kd = 0.0f,
            .output_min = -100.0f, .output_max = 100.0f
        };
        float pwm_duty = PID_Update(&pid_curr, current_ref, current_meas, dt);
        
        // Set PWM duty cycle (-100 to +100)
        Set_Motor_PWM(pwm_duty);
    }

**Safety Features (DO-178B Level A):**

.. code-block:: c

    // Dual-redundant position feedback
    bool Position_Cross_Check(void) {
        float encoder_pos = Read_Encoder_Position();
        float pot_pos = Read_Potentiometer_Position();
        
        float error = fabsf(encoder_pos - pot_pos);
        
        const float MAX_POSITION_ERROR = 2.0f;  // 2 degrees
        if (error > MAX_POSITION_ERROR) {
            // Disagreement detected
            Report_Fault(FAULT_POSITION_MISMATCH);
            return false;
        }
        
        return true;
    }
    
    // Watchdog monitoring
    void Servo_Watchdog_Check(void) {
        static uint32_t last_update_time = 0;
        uint32_t current_time = Get_System_Time_ms();
        
        if ((current_time - last_update_time) > 10) {  // 10ms timeout
            // Control loop not running
            Emergency_Stop();
            Report_Fault(FAULT_WATCHDOG_TIMEOUT);
        }
        
        last_update_time = current_time;
        
        // Reset hardware watchdog
        WDOG_Refresh();
    }

================================================================================
Variable Speed Drive (VSD) - HVAC Control
================================================================================

Project: Smart Water Heater
--------------------------------------------------------------------------------

**System:** Variable-speed pump for hot water circulation
**Motor:** AC Induction Motor (1/4 HP, 230VAC)
**Drive:** V/f control with energy optimization
**Standards:** IEC 60730, Energy Star

**V/f Control (Volts per Hertz):**

.. code-block:: c

    // V/f control maintains constant flux
    typedef struct {
        float frequency_hz;
        float voltage_rms;
        float base_frequency;   // 60 Hz
        float base_voltage;     // 230V RMS
    } VF_Control_t;
    
    void VF_Control_Update(VF_Control_t *vf, float speed_ref_percent) {
        // Speed reference: 0-100%
        vf->frequency_hz = (speed_ref_percent / 100.0f) * vf->base_frequency;
        
        // Linear V/f relationship
        vf->voltage_rms = (vf->frequency_hz / vf->base_frequency) * vf->base_voltage;
        
        // Voltage boost at low frequencies (for starting torque)
        if (vf->frequency_hz < 10.0f) {
            vf->voltage_rms += 20.0f;  // Add 20V boost
        }
        
        // Generate 3-phase sinusoidal PWM
        Generate_Sinusoidal_PWM(vf->frequency_hz, vf->voltage_rms);
    }
    
    void Generate_Sinusoidal_PWM(float freq_hz, float voltage_rms) {
        // Calculate modulation index
        const float V_DC = 325.0f;  // 230V RMS × √2
        float modulation_index = (voltage_rms * sqrtf(2.0f)) / V_DC;
        
        if (modulation_index > 1.0f) modulation_index = 1.0f;
        
        // 3-phase sine wave generation (120° apart)
        float angle_rad = 2.0f * PI * freq_hz * Get_Time_Seconds();
        
        float sin_a = modulation_index * sinf(angle_rad);
        float sin_b = modulation_index * sinf(angle_rad - 2.0f * PI / 3.0f);
        float sin_c = modulation_index * sinf(angle_rad + 2.0f * PI / 3.0f);
        
        // Convert to PWM duty cycles (0-100%)
        uint16_t duty_a = (uint16_t)((sin_a + 1.0f) / 2.0f * 1000.0f);
        uint16_t duty_b = (uint16_t)((sin_b + 1.0f) / 2.0f * 1000.0f);
        uint16_t duty_c = (uint16_t)((sin_c + 1.0f) / 2.0f * 1000.0f);
        
        Set_PWM_Duty_Cycles(duty_a, duty_b, duty_c);
    }

**Energy Optimization (Energy Star Compliance):**

.. code-block:: c

    // Adaptive speed control based on water demand
    float Calculate_Optimal_Speed(float water_flow_gpm, float temp_setpoint, 
                                   float temp_actual) {
        // PID controller for temperature
        static PID_Controller_t pid_temp = {
            .Kp = 5.0f, .Ki = 0.1f, .Kd = 0.5f,
            .output_min = 30.0f, .output_max = 100.0f
        };
        
        float speed_ref = PID_Update(&pid_temp, temp_setpoint, temp_actual, 0.1f);
        
        // Reduce speed during low demand (energy savings)
        if (water_flow_gpm < 0.5f) {
            speed_ref *= 0.5f;  // 50% speed reduction
        }
        
        // Maximum efficiency point tracking (MEPT)
        float efficiency = Calculate_System_Efficiency();
        if (efficiency < 0.85f) {
            // Adjust speed for better efficiency
            speed_ref *= 0.95f;
        }
        
        return speed_ref;
    }
    
    float Calculate_System_Efficiency(void) {
        float power_in_watts = Read_AC_Power();
        float power_out_thermal = Calculate_Thermal_Power();
        
        return power_out_thermal / power_in_watts;
    }

================================================================================
Thermal Imaging Camera - Motor-Driven Lens Control
================================================================================

Project: Military Thermal Camera
--------------------------------------------------------------------------------

**System:** Motorized zoom/focus for infrared camera
**Motor:** Stepper motor (200 steps/rev, microstepping 1/16)
**Control:** Position control with image sharpness feedback

**Stepper Motor Control:**

.. code-block:: c

    // Stepper motor driver (A4988)
    #define STEPS_PER_REV 200
    #define MICROSTEPS 16
    
    typedef struct {
        int32_t current_position;  // In microsteps
        int32_t target_position;
        uint16_t speed_steps_per_sec;
    } Stepper_t;
    
    void Stepper_Move_To_Position(Stepper_t *stepper, int32_t target_pos) {
        stepper->target_position = target_pos;
        
        int32_t steps_to_move = stepper->target_position - stepper->current_position;
        
        // Set direction
        if (steps_to_move > 0) {
            GPIO_SetBit(STEPPER_DIR_PIN);  // Forward
        } else {
            GPIO_ClearBit(STEPPER_DIR_PIN);  // Reverse
            steps_to_move = -steps_to_move;
        }
        
        // Generate step pulses
        uint32_t step_delay_us = 1000000 / stepper->speed_steps_per_sec;
        
        for (int32_t i = 0; i < steps_to_move; i++) {
            GPIO_SetBit(STEPPER_STEP_PIN);
            Delay_us(5);
            GPIO_ClearBit(STEPPER_STEP_PIN);
            Delay_us(step_delay_us - 5);
            
            stepper->current_position += (steps_to_move > 0) ? 1 : -1;
        }
    }

**Autofocus Using Image Sharpness:**

.. code-block:: c

    // Image sharpness metric (Laplacian variance)
    float Calculate_Image_Sharpness(uint8_t *image, uint16_t width, uint16_t height) {
        float laplacian_sum = 0.0f;
        
        // Laplacian kernel:
        // [ 0 -1  0]
        // [-1  4 -1]
        // [ 0 -1  0]
        
        for (uint16_t y = 1; y < height - 1; y++) {
            for (uint16_t x = 1; x < width - 1; x++) {
                int idx = y * width + x;
                
                int laplacian = 4 * image[idx]
                              - image[idx - 1]
                              - image[idx + 1]
                              - image[idx - width]
                              - image[idx + width];
                
                laplacian_sum += laplacian * laplacian;
            }
        }
        
        return laplacian_sum / (width * height);
    }
    
    // Autofocus algorithm (hill climbing)
    void Autofocus_Control(Stepper_t *focus_motor) {
        const int SEARCH_STEP = 100;  // Microsteps
        float sharpness_prev = 0.0f;
        float sharpness_current = 0.0f;
        int direction = 1;  // Start moving forward
        
        while (1) {
            // Capture image
            uint8_t *image = Capture_Thermal_Image();
            sharpness_current = Calculate_Image_Sharpness(image, 640, 480);
            
            if (sharpness_current < sharpness_prev) {
                // Passed peak, reverse direction and reduce step
                direction = -direction;
                focus_motor->speed_steps_per_sec /= 2;
                
                if (focus_motor->speed_steps_per_sec < 10) {
                    break;  // Converged to focus
                }
            }
            
            // Move motor
            focus_motor->current_position += direction * SEARCH_STEP;
            Stepper_Move_To_Position(focus_motor, focus_motor->current_position);
            
            sharpness_prev = sharpness_current;
        }
    }

================================================================================
Industrial Communication Protocols
================================================================================

Modbus RTU/TCP - HMI Interface
--------------------------------------------------------------------------------

**Modbus RTU (RS-485):**

.. code-block:: c

    // Modbus RTU frame structure
    typedef struct {
        uint8_t slave_addr;
        uint8_t function_code;
        uint16_t starting_addr;
        uint16_t quantity;
        uint16_t crc16;
    } Modbus_RTU_Frame_t;
    
    // Function 0x03: Read Holding Registers
    void Modbus_Read_Holding_Registers(uint8_t slave_addr, uint16_t start_addr, 
                                         uint16_t num_regs, uint16_t *data_out) {
        Modbus_RTU_Frame_t request;
        request.slave_addr = slave_addr;
        request.function_code = 0x03;
        request.starting_addr = htons(start_addr);
        request.quantity = htons(num_regs);
        request.crc16 = Modbus_Calculate_CRC16((uint8_t*)&request, 6);
        
        // Send request
        UART_Send_Bytes((uint8_t*)&request, sizeof(request));
        
        // Wait for response
        uint8_t response[256];
        uint16_t response_len = UART_Receive_Bytes(response, 256, 1000);  // 1s timeout
        
        // Parse response
        if (response[0] == slave_addr && response[1] == 0x03) {
            uint8_t byte_count = response[2];
            for (int i = 0; i < num_regs; i++) {
                data_out[i] = (response[3 + i*2] << 8) | response[4 + i*2];
            }
        }
    }
    
    // CRC-16 calculation (Modbus polynomial)
    uint16_t Modbus_Calculate_CRC16(uint8_t *data, uint16_t length) {
        uint16_t crc = 0xFFFF;
        
        for (uint16_t i = 0; i < length; i++) {
            crc ^= data[i];
            
            for (uint8_t j = 0; j < 8; j++) {
                if (crc & 0x0001) {
                    crc = (crc >> 1) ^ 0xA001;
                } else {
                    crc >>= 1;
                }
            }
        }
        
        return crc;
    }

**Modbus TCP (Ethernet):**

.. code-block:: c

    // Modbus TCP frame (MBAP header + PDU)
    typedef struct {
        uint16_t transaction_id;
        uint16_t protocol_id;  // Always 0x0000
        uint16_t length;
        uint8_t unit_id;
    } Modbus_MBAP_Header_t;
    
    void Modbus_TCP_Read_Registers(int socket_fd, uint16_t start_addr, 
                                     uint16_t num_regs, uint16_t *data_out) {
        uint8_t request[12];
        Modbus_MBAP_Header_t *header = (Modbus_MBAP_Header_t*)request;
        
        header->transaction_id = htons(1);
        header->protocol_id = htons(0);
        header->length = htons(6);
        header->unit_id = 1;
        
        request[7] = 0x03;  // Function code
        *((uint16_t*)&request[8]) = htons(start_addr);
        *((uint16_t*)&request[10]) = htons(num_regs);
        
        // Send TCP request
        send(socket_fd, request, 12, 0);
        
        // Receive response
        uint8_t response[256];
        recv(socket_fd, response, 256, 0);
        
        // Parse data
        uint8_t byte_count = response[8];
        for (int i = 0; i < num_regs; i++) {
            data_out[i] = (response[9 + i*2] << 8) | response[10 + i*2];
        }
    }

OPC UA - Industrial IoT Integration
--------------------------------------------------------------------------------

.. code-block:: c

    // OPC UA server (open62541 library)
    #include <open62541/server.h>
    
    void Setup_OPC_UA_Server(void) {
        UA_Server *server = UA_Server_new();
        UA_ServerConfig_setDefault(UA_ServerConfig_get(server));
        
        // Add variable node: Motor Speed
        UA_VariableAttributes attr = UA_VariableAttributes_default;
        UA_Double motor_speed = 0.0;
        UA_Variant_setScalar(&attr.value, &motor_speed, &UA_TYPES[UA_TYPES_DOUBLE]);
        attr.displayName = UA_LOCALIZEDTEXT("en-US", "Motor Speed (RPM)");
        attr.accessLevel = UA_ACCESSLEVELMASK_READ | UA_ACCESSLEVELMASK_WRITE;
        
        UA_NodeId motor_speed_node_id = UA_NODEID_STRING(1, "MotorSpeed");
        UA_Server_addVariableNode(server, motor_speed_node_id,
                                   UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER),
                                   UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES),
                                   UA_QUALIFIEDNAME(1, "MotorSpeed"),
                                   UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE),
                                   attr, NULL, NULL);
        
        // Start server
        UA_Server_run(server, &running);
        UA_Server_delete(server);
    }

IEC 61131-3 - PLC Programming
--------------------------------------------------------------------------------

**Structured Text (ST) - PID Control:**

.. code-block:: iecst

    PROGRAM PID_Motor_Control
    VAR
        SetPoint : REAL := 1500.0;     (* RPM *)
        ProcessValue : REAL;
        Output : REAL;
        
        Kp : REAL := 0.5;
        Ki : REAL := 0.1;
        Kd : REAL := 0.05;
        
        Error : REAL;
        LastError : REAL := 0.0;
        Integral : REAL := 0.0;
        Derivative : REAL;
        
        CycleTime : TIME := T#100ms;
        dt : REAL := 0.1;
    END_VAR
    
    (* Read motor speed from encoder *)
    ProcessValue := Read_Motor_Speed();
    
    (* Calculate error *)
    Error := SetPoint - ProcessValue;
    
    (* Proportional term *)
    Output := Kp * Error;
    
    (* Integral term *)
    Integral := Integral + (Error * dt);
    Output := Output + Ki * Integral;
    
    (* Derivative term *)
    Derivative := (Error - LastError) / dt;
    Output := Output + Kd * Derivative;
    
    (* Clamp output *)
    IF Output > 100.0 THEN
        Output := 100.0;
    ELSIF Output < 0.0 THEN
        Output := 0.0;
    END_IF;
    
    (* Write PWM duty cycle *)
    Write_Motor_PWM(Output);
    
    LastError := Error;
    END_PROGRAM

================================================================================
Lessons Learned
================================================================================

**FOC Motor Control:**
✓ ARM Cortex-M4 FPU essential for real-time trigonometric calculations
✓ Sensorless control requires careful back-EMF filtering
✓ Startup sequence (alignment → open-loop → closed-loop) critical
✓ Current loop bandwidth must be 10x higher than speed loop
✓ Space vector modulation provides 15% better DC bus utilization than SPWM

**Servo Control:**
✓ Cascaded PID provides excellent dynamic response
✓ Dual-redundant feedback mandatory for safety-critical applications
✓ Anti-windup necessary for integral terms
✓ Encoder resolution directly impacts position accuracy

**Modbus/OPC UA:**
✓ Modbus RTU limited to ~19200 baud for reliable RS-485 communication
✓ Modbus TCP eliminates need for CRC (TCP checksums)
✓ OPC UA provides security and interoperability for Industry 4.0

**Energy Optimization:**
✓ Variable-speed drives save 30-50% energy vs. fixed-speed
✓ V/f control simple but limited performance; FOC preferred for precise control
✓ Dead-time compensation important to avoid voltage distortion

**Common Pitfalls:**
✗ Insufficient ADC sampling rate for current measurements
✗ PWM dead-time too short (shoot-through) or too long (voltage error)
✗ Not accounting for motor parameter variations (temperature, saturation)
✗ Ignoring current limits during transients (motor/inverter protection)

================================================================================
References
================================================================================

**Standards:**
- IEC 61131-3: PLC Programming Languages
- IEC 61508: Functional Safety (Industrial)
- IEC 60730: Automatic Electrical Controls (Appliances)
- IEC 61800-5-1: Adjustable Speed Drives - Safety Requirements
- Modbus Protocol Specification V1.1b3
- OPC UA Specification Part 1-14

**Tools:**
- MATLAB Simulink: Motor control algorithm development
- STM32CubeMX: Peripheral configuration
- CANoe: CAN/Modbus testing
- TI InstaSPIN: FOC motor control library

================================================================================
