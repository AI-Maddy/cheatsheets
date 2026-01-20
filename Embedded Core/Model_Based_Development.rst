═══════════════════════════════════════════════════════════════════════
MODEL-BASED DEVELOPMENT WITH MATLAB/SIMULINK
═══════════════════════════════════════════════════════════════════════

**Complete Guide to Model-Based Design for Embedded Systems**  
**Domain:** Embedded Systems 🎯 | Control Systems 📊 | Code Generation 🔧  
**Purpose:** MATLAB/Simulink, Stateflow, Embedded Coder, Testing, AUTOSAR integration

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Model-Based Development (MBD)** uses graphical models to design, simulate, and automatically generate code for embedded systems.

**Key Benefits:**
- **Early validation:** Test control algorithms before hardware exists
- **Automatic code generation:** C/C++ from models (no hand-coding)
- **Reduced errors:** Visual design catches issues early
- **Documentation:** Model IS the specification
- **Certification:** DO-178C/ISO 26262 compliant code generation

**Workflow:**
Requirements → Model → Simulate → Test → Generate Code → Deploy → Verify

**Your Experience:**
- MATLAB/Simulink: Control system design (multiple projects)
- Stateflow: State machine modeling
- Embedded Coder: Automatic code generation
- Model-in-loop (MIL) testing
- Automotive and avionics applications

**Use Cases:**
- Motor control (FOC, PID controllers)
- ADAS (sensor fusion, path planning)
- Flight control (autopilot, stability)
- Engine control (fuel injection, ignition timing)

═══════════════════════════════════════════════════════════════════════

🎯 **1. MODEL-BASED DEVELOPMENT OVERVIEW**
─────────────────────────────────────────────────────────────────────────

**1.1 What is Model-Based Development?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Traditional Development vs MBD:**

.. code-block:: text

   Traditional (Code-First):
   ─────────────────────────
   Requirements → Design Doc → Hand-Code C → Debug → Test → Deploy
   
   Issues:
   ❌ Late error detection (after coding)
   ❌ Manual coding errors
   ❌ Difficult to verify against requirements
   ❌ Hard to maintain
   ❌ Specification and code drift apart
   
   Model-Based Development:
   ────────────────────────
   Requirements → Simulink Model → Simulate & Test → Auto-Generate C → Deploy
   
   Benefits:
   ✅ Early validation (before hardware)
   ✅ Automatic code generation (error-free)
   ✅ Model = Specification (always in sync)
   ✅ Reusable components
   ✅ Certification-ready code (DO-178C/ISO 26262)

**V-Model for MBD:**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │                   V-Model Workflow                          │
   └─────────────────────────────────────────────────────────────┘
   
   Requirements ──────────────────────────────► System Test
        │                                            ▲
        │                                            │
        ▼                                            │
   System Design ─────────────────────────► Integration Test
        │                                            ▲
        │                                            │
        ▼                                            │
   Component Design ──────────────────► Component Test
        │                                            ▲
        │                                            │
        ▼                                            │
   Detailed Model ─────────────────────► MIL Testing
        │                                (Model-in-Loop)
        │                                            ▲
        ▼                                            │
   Generated Code ─────────────────────► SIL Testing
        │                                (Software-in-Loop)
        │                                            ▲
        ▼                                            │
   Deploy to Target ───────────────────► HIL Testing
                                         (Hardware-in-Loop)

**1.2 MBD Toolchain**
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   MATLAB/Simulink Ecosystem:
   ──────────────────────────
   
   Core Tools:
   ───────────
   • MATLAB: Scripting, data analysis, algorithm development
   • Simulink: Block diagram modeling, simulation
   • Stateflow: State machine and flow chart design
   
   Code Generation:
   ────────────────
   • Embedded Coder: Optimized C/C++ code generation
   • Simulink Coder: Generic C code generation
   • HDL Coder: VHDL/Verilog for FPGAs
   
   Testing & Verification:
   ───────────────────────
   • Simulink Test: Test harness, coverage analysis
   • Simulink Design Verifier: Model checking, proof
   • Polyspace: Static analysis, runtime error detection
   
   Automotive:
   ───────────
   • AUTOSAR Blockset: AUTOSAR Adaptive/Classic
   • Vehicle Dynamics Blockset: Vehicle modeling
   
   Avionics:
   ─────────
   • DO Qualification Kit: DO-178C certification
   • IEC Certification Kit: IEC 61508 certification

═══════════════════════════════════════════════════════════════════════

📊 **2. MATLAB FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**2.1 MATLAB Basics**
~~~~~~~~~~~~~~~~~~~~~~

**Matrix Operations:**

.. code-block:: matlab

   % MATLAB = Matrix Laboratory
   % Everything is a matrix
   
   % Scalars (1×1 matrix)
   a = 5;
   
   % Vectors (1×n or n×1 matrix)
   row_vector = [1 2 3 4 5];           % 1×5
   col_vector = [1; 2; 3; 4; 5];       % 5×1
   range = 0:0.1:10;                   % 0 to 10, step 0.1
   
   % Matrices (m×n)
   A = [1 2 3; 4 5 6; 7 8 9];          % 3×3 matrix
   
   % Matrix operations
   B = A';                              % Transpose
   C = inv(A);                          % Inverse
   D = A * B;                           % Matrix multiplication
   E = A .* B;                          % Element-wise multiplication
   
   % Accessing elements
   x = A(2, 3);                         % Row 2, Column 3 (value = 6)
   row2 = A(2, :);                      % All of row 2
   col3 = A(:, 3);                      % All of column 3

**Control Flow:**

.. code-block:: matlab

   % If-else
   if temperature > 80
       activate_cooling();
   elseif temperature > 60
       warning('Temperature rising');
   else
       normal_operation();
   end
   
   % For loop
   for i = 1:10
       data(i) = read_sensor(i);
   end
   
   % While loop
   while error > tolerance
       error = calculate_error();
       adjust_control();
   end
   
   % Switch
   switch mode
       case 'idle'
           idle_mode();
       case 'active'
           active_mode();
       otherwise
           error('Unknown mode');
   end

**Functions:**

.. code-block:: matlab

   % Function definition (save as calculate_pid.m)
   function output = calculate_pid(error, Kp, Ki, Kd)
       % PID Controller
       % Inputs: error, Kp, Ki, Kd
       % Output: control signal
       
       persistent integral derivative last_error
       
       if isempty(integral)
           integral = 0;
           last_error = 0;
       end
       
       % Calculate PID terms
       proportional = Kp * error;
       integral = integral + Ki * error;
       derivative = Kd * (error - last_error);
       
       % Control output
       output = proportional + integral + derivative;
       
       % Save for next iteration
       last_error = error;
   end
   
   % Usage:
   control_signal = calculate_pid(error, 1.5, 0.1, 0.05);

**2.2 Signal Processing**
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Generate test signal
   fs = 1000;                           % Sample rate: 1 kHz
   t = 0:1/fs:1;                        % Time vector: 0 to 1 sec
   
   % Signal with noise
   signal = sin(2*pi*50*t) + 0.5*randn(size(t));  % 50 Hz sine + noise
   
   % Low-pass filter (remove noise above 100 Hz)
   fc = 100;                            % Cutoff frequency
   [b, a] = butter(4, fc/(fs/2));       % 4th-order Butterworth
   filtered = filter(b, a, signal);
   
   % FFT (Frequency analysis)
   N = length(signal);
   Y = fft(signal);
   f = (0:N-1)*(fs/N);                  % Frequency vector
   
   % Plot frequency spectrum
   plot(f(1:N/2), abs(Y(1:N/2)));
   xlabel('Frequency (Hz)');
   ylabel('Magnitude');

**2.3 Data Analysis**
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Load sensor data
   data = load('sensor_log.mat');
   
   % Statistics
   mean_value = mean(data.temperature);
   std_dev = std(data.temperature);
   max_temp = max(data.temperature);
   min_temp = min(data.temperature);
   
   % Find outliers
   outliers = find(abs(data.temperature - mean_value) > 3*std_dev);
   
   % Curve fitting
   x = data.time;
   y = data.temperature;
   p = polyfit(x, y, 2);                % 2nd-order polynomial fit
   y_fit = polyval(p, x);
   
   % Plot with fit
   plot(x, y, 'o', x, y_fit, '-');
   legend('Data', 'Fit');

═══════════════════════════════════════════════════════════════════════

🎨 **3. SIMULINK FUNDAMENTALS**
─────────────────────────────────────────────────────────────────────────

**3.1 Simulink Blocks**
~~~~~~~~~~~~~~~~~~~~~~~~

**Basic Block Categories:**

.. code-block:: text

   Simulink Library Browser:
   ─────────────────────────
   
   Sources:              Generate signals
   ├── Constant          Fixed value
   ├── Sine Wave         Sinusoidal signal
   ├── Step              Step input
   ├── Ramp              Ramp signal
   ├── From Workspace    Load MATLAB variable
   └── Signal Generator  Various waveforms
   
   Sinks:                Display/save data
   ├── Scope             Oscilloscope display
   ├── To Workspace      Save to MATLAB
   ├── Display           Numerical display
   └── XY Graph          2D plotting
   
   Math Operations:
   ├── Gain              Multiply by constant
   ├── Sum               Addition/subtraction
   ├── Product           Multiplication/division
   ├── Trigonometric     sin, cos, tan, etc.
   └── Math Function     abs, sqrt, exp, log
   
   Continuous:           Continuous-time systems
   ├── Integrator        ∫ x dt
   ├── Derivative        dx/dt
   ├── Transfer Fcn      H(s) = num(s)/den(s)
   └── State-Space       ẋ = Ax + Bu, y = Cx + Du
   
   Discrete:             Discrete-time systems
   ├── Unit Delay        z⁻¹
   ├── Discrete Integrator
   └── Discrete Transfer Fcn
   
   Signal Routing:
   ├── Mux               Combine signals
   ├── Demux             Split signals
   ├── Switch            Conditional routing
   └── Selector          Select signal elements

**Simple Example: PID Controller**

.. code-block:: text

   Simulink Block Diagram:
   
   ┌──────────┐     ┌─────┐     ┌─────────────┐     ┌────────┐
   │ Setpoint │────►│ Sum │────►│ PID         │────►│ Plant  │
   │          │  +  │     │     │ Controller  │     │ (Motor)│
   └──────────┘     └──┬──┘     └─────────────┘     └───┬────┘
                       ▲                                 │
                       │         Feedback                │
                       └─────────────────────────────────┘
   
   Blocks:
   1. Setpoint: Constant block (desired position)
   2. Sum: Add block (+ and - inputs)
   3. PID Controller: PID block from Simulink library
   4. Plant: Transfer function (motor dynamics)
   5. Feedback: Signal line from output to Sum

**3.2 Creating a Simulink Model**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step-by-Step: Motor Speed Control**

.. code-block:: matlab

   % 1. Create new model
   % File → New → Model
   % Or: simulink (command to open Simulink)
   
   % 2. Add blocks (drag from Library Browser)
   % - Constant (setpoint: 1000 RPM)
   % - Sum (error = setpoint - actual)
   % - PID Controller (Kp=0.5, Ki=0.1, Kd=0.01)
   % - Transfer Fcn (motor: 1/(s+1))
   % - Scope (display output)
   
   % 3. Connect blocks (drag lines between ports)
   
   % 4. Configure simulation
   % Simulation → Model Configuration Parameters
   % - Solver: ode45 (variable-step)
   % - Stop time: 10 seconds
   % - Max step size: auto
   
   % 5. Run simulation
   % Click "Run" button or Ctrl+T
   
   % 6. View results on Scope

**Block Parameters (PID Controller Example):**

.. code-block:: matlab

   % Double-click PID Controller block
   
   % PID Configuration:
   % ──────────────────
   % Controller: PID
   % Form: Parallel
   %   P term: Kp = 0.5
   %   I term: Ki = 0.1
   %   D term: Kd = 0.01
   % 
   % Continuous-time or Discrete-time: Continuous
   % 
   % Anti-windup: on (prevent integrator saturation)
   % Output limits: [-100, 100]

**3.3 Transfer Functions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Continuous Transfer Function:**

.. code-block:: matlab

   % DC Motor Transfer Function: ω(s)/V(s) = K / (τs + 1)
   % Where: K = motor gain, τ = time constant
   
   % Method 1: Transfer Function block
   % Numerator: [10]
   % Denominator: [0.1 1]
   % Represents: 10 / (0.1s + 1)
   
   % Method 2: MATLAB tf() function
   K = 10;
   tau = 0.1;
   motor_tf = tf(K, [tau 1]);
   
   % Step response
   step(motor_tf);
   grid on;

**State-Space Representation:**

.. code-block:: matlab

   % State-Space Model: ẋ = Ax + Bu, y = Cx + Du
   
   % Example: Mass-spring-damper system
   % States: x = [position; velocity]
   % Input: u = force
   % Output: y = position
   
   m = 1.0;    % Mass (kg)
   k = 10.0;   % Spring constant (N/m)
   c = 2.0;    % Damping coefficient (N·s/m)
   
   A = [0      1;
        -k/m  -c/m];
   
   B = [0;
        1/m];
   
   C = [1 0];
   
   D = 0;
   
   % Create state-space model
   sys = ss(A, B, C, D);
   
   % Simulink: Use State-Space block with above matrices

**3.4 Discrete-Time Systems**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Continuous vs Discrete:**

.. code-block:: text

   Continuous-Time (Analog):
   ─────────────────────────
   • Time: t ∈ [0, ∞)
   • Signal: x(t)
   • Derivative: dx/dt
   • Integrator: ∫ x(t) dt
   • Transfer function: H(s)
   • Use when: Modeling physical systems
   
   Discrete-Time (Digital):
   ────────────────────────
   • Time: k·Ts (k = 0, 1, 2, ...)
   • Signal: x[k]
   • Difference: x[k] - x[k-1]
   • Accumulator: Σ x[k]
   • Transfer function: H(z)
   • Use when: Implementing in microcontroller

**Discretization:**

.. code-block:: matlab

   % Continuous PID controller
   Kp = 1.0;
   Ki = 0.5;
   Kd = 0.1;
   
   % Continuous transfer function
   s = tf('s');
   C_cont = Kp + Ki/s + Kd*s;
   
   % Discretize (sample time Ts = 0.01 sec = 10 ms)
   Ts = 0.01;
   C_disc = c2d(C_cont, Ts, 'tustin');  % Tustin (bilinear) method
   
   % In Simulink:
   % Use "Discrete PID Controller" block
   % Set Sample time: 0.01

**Discrete Integrator (Digital Implementation):**

.. code-block:: text

   Continuous Integrator:
   y(t) = ∫ u(t) dt
   
   Discrete Integrator (Forward Euler):
   y[k] = y[k-1] + Ts × u[k-1]
   
   Discrete Integrator (Backward Euler):
   y[k] = y[k-1] + Ts × u[k]
   
   Discrete Integrator (Trapezoidal/Tustin):
   y[k] = y[k-1] + (Ts/2) × (u[k] + u[k-1])

═══════════════════════════════════════════════════════════════════════

🎛️ **4. CONTROL SYSTEM DESIGN**
─────────────────────────────────────────────────────────────────────────

**4.1 PID Controller Design**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**PID Tuning Methods:**

.. code-block:: matlab

   % Method 1: Manual Tuning (Ziegler-Nichols)
   % ──────────────────────────────────────────
   % 1. Set Ki = 0, Kd = 0
   % 2. Increase Kp until sustained oscillation
   % 3. Note critical gain Ku and period Tu
   % 4. Calculate PID gains:
   
   Ku = 2.0;   % Ultimate gain (from testing)
   Tu = 0.5;   % Ultimate period (from testing)
   
   % Classic PID:
   Kp = 0.6 * Ku;
   Ki = 1.2 * Ku / Tu;
   Kd = 0.075 * Ku * Tu;
   
   % Method 2: Auto-Tuning (Simulink PID Tuner)
   % ───────────────────────────────────────────
   % 1. In Simulink, select PID Controller block
   % 2. Apps → PID Tuner
   % 3. Specify plant (transfer function)
   % 4. Set performance requirements (response time, overshoot)
   % 5. Click "Update Block" to apply tuned parameters
   
   % Method 3: Optimization (MATLAB)
   % ───────────────────────────────
   % Minimize cost function (e.g., IAE, ISE, ITAE)
   
   % Plant model
   plant = tf(1, [1 1]);
   
   % Optimization function
   objective = @(K) pid_cost(K, plant);
   
   % Initial guess: [Kp, Ki, Kd]
   K0 = [1, 0.5, 0.1];
   
   % Optimize
   K_opt = fminsearch(objective, K0);
   
   Kp = K_opt(1);
   Ki = K_opt(2);
   Kd = K_opt(3);
   
   function cost = pid_cost(K, plant)
       % Create PID controller
       C = pid(K(1), K(2), K(3));
       
       % Closed-loop system
       sys_cl = feedback(C * plant, 1);
       
       % Step response
       [y, t] = step(sys_cl, 10);
       
       % Cost = Integral Absolute Error
       error = 1 - y;
       cost = trapz(t, abs(error));
   end

**Anti-Windup (Integrator Saturation Prevention):**

.. code-block:: text

   Problem:
   ────────
   When PID output saturates (e.g., motor at 100% duty cycle),
   integral term keeps accumulating → Large overshoot when saturation ends
   
   Solution: Back-Calculation Anti-Windup
   ───────────────────────────────────────
   
   ┌────────────┐     ┌───────┐     ┌──────────┐
   │ Error      │────►│  PID  │────►│ Saturation│───► Output
   │            │     │       │     │ [min,max] │
   └────────────┘     └───┬───┘     └─────┬─────┘
                          ▲                 │
                          │   Anti-windup   │
                          │   (Kt feedback) │
                          └─────────────────┘
   
   When output saturates:
   • Calculate difference: saturated_output - pid_output
   • Feedback to integrator with gain Kt (typically 1/Ti)
   • Prevents integrator from winding up

**4.2 State Feedback Control**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % State-Space Model: ẋ = Ax + Bu
   % State Feedback: u = -Kx + r
   
   % Example: Inverted Pendulum
   % States: [angle, angular_velocity, cart_position, cart_velocity]
   
   m = 0.5;    % Pendulum mass
   M = 1.0;    % Cart mass
   L = 0.3;    % Pendulum length
   g = 9.81;   % Gravity
   
   % Linearized state-space matrices (around upright position)
   A = [0  1           0       0;
        g/L 0          0       0;
        0   0          0       1;
        0   -m*g/M     0       0];
   
   B = [0; -1/(M*L); 0; 1/M];
   
   C = [1 0 0 0;     % Measure angle
        0 0 1 0];    % Measure position
   
   D = [0; 0];
   
   % Design state feedback gain using LQR
   Q = diag([100 1 100 1]);  % State cost (penalize angle and position)
   R = 1;                    % Input cost (penalize control effort)
   
   K = lqr(A, B, Q, R);      % Optimal gain matrix
   
   % Closed-loop system: u = -Kx
   A_cl = A - B*K;
   sys_cl = ss(A_cl, B, C, D);
   
   % Simulate in Simulink:
   % - State-Space block with A, B, C, D
   % - Gain block: -K (4×1 vector)
   % - Feedback loop from states to input

**4.3 Observer Design (State Estimation)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Not all states are measurable → Estimate using observer
   
   % Luenberger Observer: ẋ̂ = Ax̂ + Bu + L(y - ŷ)
   % Where: x̂ = estimated state, L = observer gain
   
   % Design observer gain (pole placement)
   % Observer poles should be 2-5× faster than controller poles
   
   % Controller poles
   eig_controller = eig(A - B*K);
   
   % Observer poles (5× faster)
   desired_eig = 5 * eig_controller;
   
   % Calculate observer gain
   L = place(A', C', desired_eig)';
   
   % Observer dynamics: ẋ̂ = (A - LC)x̂ + Bu + Ly
   A_obs = A - L*C;
   
   % In Simulink:
   % Create observer subsystem with:
   % - State-Space block: (A-LC, [B L], C, D)
   % - Inputs: u (control) and y (measurements)
   % - Output: x̂ (estimated states)

**4.4 Kalman Filter (Optimal State Estimation)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Kalman Filter: Optimal observer for systems with noise
   
   % System with noise:
   % ẋ = Ax + Bu + w    (process noise)
   % y = Cx + Du + v    (measurement noise)
   
   % Noise covariances
   Q_noise = 0.01 * eye(4);  % Process noise covariance
   R_noise = 0.1 * eye(2);   % Measurement noise covariance
   
   % Design Kalman filter
   [kalmf, L, P] = kalman(sys, Q_noise, R_noise);
   
   % L = Kalman gain matrix (optimal observer gain)
   
   % In Simulink:
   % Use "Kalman Filter" block from Control System Toolbox
   % Or implement manually with State-Space block and L gain

═══════════════════════════════════════════════════════════════════════

🔧 **5. SUBSYSTEMS AND LIBRARIES**
─────────────────────────────────────────────────────────────────────────

**5.1 Creating Subsystems**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Why Subsystems:**

.. code-block:: text

   Benefits:
   ─────────
   ✅ Organize complex models (hierarchical design)
   ✅ Reusability (copy subsystem to other models)
   ✅ Abstraction (hide implementation details)
   ✅ Easier testing (test subsystem independently)
   ✅ Code generation (each subsystem → function)

**Creating a Subsystem:**

.. code-block:: text

   Method 1: Manual
   ────────────────
   1. Select blocks to group (click and drag box)
   2. Right-click → Create Subsystem from Selection
   3. Double-click subsystem to edit internal blocks
   4. Inports/Outports automatically created
   
   Method 2: Subsystem Block
   ─────────────────────────
   1. Drag "Subsystem" block from Simulink Library
   2. Double-click to open
   3. Add blocks inside
   4. Add Inport blocks for inputs
   5. Add Outport blocks for outputs

**Example: Motor Controller Subsystem**

.. code-block:: text

   Top-Level Model:
   ┌────────────┐     ┌─────────────────┐     ┌────────┐
   │  Setpoint  │────►│ Motor Controller│────►│ Scope  │
   │            │     │   (Subsystem)   │     │        │
   └────────────┘     └─────────────────┘     └────────┘
   
   Inside "Motor Controller" Subsystem:
   ┌────────┐  ┌─────┐  ┌─────┐  ┌──────────┐  ┌─────────┐
   │ Inport │─►│ Sum │─►│ PID │─►│Saturation│─►│ Outport │
   │   1    │  └──┬──┘  └─────┘  └──────────┘  │    1    │
   └────────┘     ▲                             └─────────┘
                  │
                  │  (Feedback from output)
                  └─────────────────────────────────┘

**5.2 Masked Subsystems**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Mask = Custom GUI for subsystem parameters**

.. code-block:: matlab

   % Create mask:
   % 1. Right-click subsystem → Mask → Create Mask
   % 2. Add parameters in "Parameters & Dialog" tab:
   
   % Example: PID Controller Mask
   % Parameters:
   %   - Proportional Gain (Kp): Edit field, default = 1.0
   %   - Integral Gain (Ki): Edit field, default = 0.5
   %   - Derivative Gain (Kd): Edit field, default = 0.1
   %   - Sample Time (Ts): Edit field, default = 0.01
   
   % 3. Use parameters in blocks:
   %    In PID block: P = Kp, I = Ki, D = Kd
   
   % 4. Customize icon (Icon & Ports tab):
   %    Add text: fprintf('PID\nKp=%g, Ki=%g, Kd=%g', Kp, Ki, Kd)
   
   % 5. Add documentation (Documentation tab)

**5.3 Model Libraries**
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Creating Reusable Library:
   ──────────────────────────
   1. File → New → Library
   2. Add subsystems to library
   3. Save as .slx file
   
   Using Library Blocks:
   ─────────────────────
   1. Drag block from library to model
   2. Block is "linked" to library (not copied)
   3. Changes to library propagate to all models using it
   
   Example Library Structure:
   ──────────────────────────
   ControlLibrary.slx
   ├── Controllers
   │   ├── PID Controller
   │   ├── State Feedback
   │   └── Adaptive Controller
   ├── Observers
   │   ├── Luenberger Observer
   │   └── Kalman Filter
   └── Plants
       ├── DC Motor
       ├── Inverted Pendulum
       └── Quadcopter

═══════════════════════════════════════════════════════════════════════

⚙️ **6. SIMULATION CONFIGURATION**
─────────────────────────────────────────────────────────────────────────

**6.1 Solver Selection**
~~~~~~~~~~~~~~~~~~~~~~~~~

**Fixed-Step vs Variable-Step:**

.. code-block:: text

   Variable-Step Solvers (for desktop simulation):
   ───────────────────────────────────────────────
   • ode45 (Dormand-Prince): General purpose, 4th/5th order
   • ode23 (Bogacki-Shampine): Lower accuracy, faster
   • ode113: Multi-step solver, very accurate
   • ode15s: Stiff systems (fast and slow dynamics)
   • ode23s: Stiff systems, lower order
   
   Pros: Accurate, adaptive step size
   Cons: Non-deterministic timing (not for code generation)
   
   Fixed-Step Solvers (for embedded code generation):
   ──────────────────────────────────────────────────
   • ode1 (Euler): 1st order, least accurate, fastest
   • ode2 (Heun): 2nd order
   • ode3 (Bogacki-Shampine): 3rd order
   • ode4 (Runge-Kutta): 4th order, good balance
   • ode5 (Dormand-Prince): 5th order, most accurate
   
   Pros: Deterministic, suitable for real-time
   Cons: Fixed timestep (may be inefficient)

**Choosing Solver:**

.. code-block:: matlab

   % For desktop simulation (accuracy priority):
   % Simulation → Model Configuration Parameters → Solver
   % Type: Variable-step
   % Solver: ode45 (Dormand-Prince)
   % Max step size: auto
   % Relative tolerance: 1e-3 (default)
   
   % For code generation (real-time):
   % Type: Fixed-step
   % Solver: ode4 (Runge-Kutta)
   % Fixed-step size: 0.001 (1 ms) - match target sample rate
   
   % Example: Motor control at 10 kHz
   Ts = 1e-4;  % 0.1 ms = 10 kHz
   set_param('myModel', 'SolverType', 'Fixed-step');
   set_param('myModel', 'Solver', 'ode4');
   set_param('myModel', 'FixedStep', num2str(Ts));

**6.2 Simulation Time**
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Set simulation duration
   % Simulation → Model Configuration Parameters → Solver
   % Stop time: 10.0 (seconds)
   
   % Or via command:
   set_param('myModel', 'StopTime', '10.0');
   
   % Enable signal logging (for analysis)
   set_param('myModel', 'SignalLogging', 'on');
   set_param('myModel', 'SignalLoggingName', 'logsout');
   
   % Run simulation
   sim('myModel');
   
   % Access logged data
   time = logsout{1}.Values.Time;
   data = logsout{1}.Values.Data;
   
   plot(time, data);

**6.3 Initial Conditions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Method 1: Block parameters
   % Integrator block → Initial condition: 0 (or variable)
   
   % Method 2: Model workspace
   % In Model Explorer:
   % myModel → Model Workspace
   % Add variable: x0 = [0; 0; 0; 0]  (initial state vector)
   
   % State-Space block → Initial conditions: x0
   
   % Method 3: MATLAB script (programmatic)
   % Load initial conditions from file or calculation
   load('initial_state.mat');  % Contains x0, y0, etc.
   
   % Set in model
   set_param('myModel/StateSpace', 'InitialCondition', 'x0');

═══════════════════════════════════════════════════════════════════════

🔨 **7. STATEFLOW (STATE MACHINE DESIGN)**
─────────────────────────────────────────────────────────────────────────

**7.1 Stateflow Fundamentals**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**State Machine Basics:**

.. code-block:: text

   State Machine Components:
   ─────────────────────────
   
   States:              Represent system modes/conditions
   ├── Active          Currently executing
   ├── Inactive        Not executing
   └── Hierarchy       Superstates contain substates
   
   Transitions:         Movement between states
   ├── Condition       [expression] guards transition
   ├── Event           Triggers transition
   └── Action          {code} executes during transition
   
   Events:              Triggers for state changes
   ├── Input events    From Simulink inputs
   ├── Local events    Within chart
   └── Broadcast       Send to other charts
   
   Data:                Variables in chart
   ├── Input           From Simulink
   ├── Output          To Simulink
   ├── Local           Internal to chart
   └── Constant        Fixed values

**Simple Example: Thermostat**

.. code-block:: text

   Stateflow Chart: Thermostat Controller
   
   ┌─────────────────────────────────────────────┐
   │                                             │
   │   ┌──────────┐  temp < setpoint-2         │
   │   │   OFF    │◄──────────────────────┐    │
   │   │          │                        │    │
   │   │ heater=0 │                        │    │
   │   └────┬─────┘                        │    │
   │        │                               │    │
   │        │ temp < setpoint-2            │    │
   │        │                               │    │
   │        ▼                               │    │
   │   ┌──────────┐  temp > setpoint+2    │    │
   │   │   ON     │───────────────────────┘    │
   │   │          │                             │
   │   │ heater=1 │                             │
   │   └──────────┘                             │
   │                                             │
   └─────────────────────────────────────────────┘
   
   Inputs: temp (temperature), setpoint
   Outputs: heater (0=off, 1=on)
   
   States:
   - OFF: entry: heater = 0;
   - ON:  entry: heater = 1;
   
   Transitions:
   - OFF → ON:  [temp < setpoint - 2]
   - ON → OFF:  [temp > setpoint + 2]

**7.2 State Actions**
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   State Action Types:
   ───────────────────
   
   entry:          Execute when entering state
                   en: code
                   
   during:         Execute every time step while in state
                   du: code
                   
   exit:           Execute when leaving state
                   ex: code
                   
   on event:       Execute when event occurs
                   on event_name: code
   
   Example: Motor Controller States
   ─────────────────────────────────
   
   State: IDLE
   ───────────
   entry: motor_speed = 0;
          enable_pin = 0;
   
   State: ACCELERATING
   ───────────────────
   entry: target_speed = requested_speed;
   during: if (motor_speed < target_speed)
              motor_speed = motor_speed + accel_rate;
           end
   exit: log_event("Acceleration complete");
   
   State: RUNNING
   ──────────────
   entry: maintain_speed(target_speed);
   during: monitor_temperature();
   on overheat: emergency_stop();

**7.3 Hierarchical States (Superstates)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Motor Control State Machine:
   ────────────────────────────
   
   ┌──────────────────────────────────────────────────────┐
   │ OPERATIONAL (Superstate)                             │
   │ ┌─────────────┐  start     ┌─────────────┐          │
   │ │    IDLE     │───────────►│ACCELERATING │          │
   │ │             │            │             │          │
   │ └─────────────┘            └──────┬──────┘          │
   │                                   │ at_speed        │
   │                                   ▼                 │
   │ ┌─────────────┐            ┌─────────────┐          │
   │ │DECELERATING │◄───────────│   RUNNING   │          │
   │ │             │    stop    │             │          │
   │ └──────┬──────┘            └─────────────┘          │
   │        │                                             │
   │        │ stopped                                     │
   │        └────────────────────┐                        │
   │                             ▼                        │
   └─────────────────────────────────────────────────────┘
                                 │ fault
                                 ▼
                         ┌─────────────┐
                         │    ERROR    │
                         │ (Outside)   │
                         └─────────────┘
   
   Superstate Benefits:
   ────────────────────
   • Common transitions (fault → ERROR from any OPERATIONAL state)
   • Shared entry/exit actions
   • Hierarchical organization
   • Default transitions within superstate

**7.4 Parallel States (AND Decomposition)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Parallel Execution (Multiple concurrent states):
   
   ┌─────────────────────────────────────────────────────┐
   │                SYSTEM                               │
   │                                                     │
   │  ┌───────────────────┬────────────────────────┐    │
   │  │  Motor Control    │  Temperature Monitor   │    │
   │  │                   │                        │    │
   │  │  ┌────┐  ┌─────┐  │  ┌──────┐  ┌───────┐  │    │
   │  │  │IDLE│→│RUNNING│ │  │NORMAL│→│WARNING│  │    │
   │  │  └────┘  └─────┘  │  └──────┘  └───────┘  │    │
   │  │                   │      │                 │    │
   │  │                   │      ▼                 │    │
   │  │                   │  ┌────────┐            │    │
   │  │                   │  │CRITICAL│            │    │
   │  │                   │  └────────┘            │    │
   │  └───────────────────┴────────────────────────┘    │
   │                                                     │
   └─────────────────────────────────────────────────────┘
   
   Both substates execute simultaneously:
   • Motor can be IDLE or RUNNING
   • Temperature can be NORMAL, WARNING, or CRITICAL
   • Independent state transitions
   • Can communicate via events

**7.5 Stateflow + Simulink Integration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Creating Stateflow Chart:
   % 1. Add "Chart" block from Stateflow library
   % 2. Double-click to open Stateflow Editor
   % 3. Add states, transitions, data
   
   % Define inputs (from Simulink):
   % - Right panel → Symbols → Add Input
   % - Name: temperature, Type: double, Scope: Input
   
   % Define outputs (to Simulink):
   % - Name: heater_cmd, Type: boolean, Scope: Output
   
   % Chart execution:
   % - Sample time: 0.1 (executes every 0.1 seconds)
   % - Update method: Triggered (on event) or Continuous

**Example: Door Lock Controller**

.. code-block:: text

   Inputs:
   - unlock_button: boolean
   - lock_button: boolean
   - door_closed: boolean
   
   Outputs:
   - lock_actuator: boolean
   - warning_light: boolean
   
   States:
   
   LOCKED:
   ───────
   entry: lock_actuator = true;
          warning_light = false;
   
   [unlock_button && door_closed] → UNLOCKED
   
   UNLOCKED:
   ─────────
   entry: lock_actuator = false;
          warning_light = false;
   
   [lock_button] → LOCKED
   [!door_closed] → WARNING
   
   WARNING:
   ────────
   entry: lock_actuator = false;
          warning_light = true;
   
   [door_closed] → UNLOCKED

═══════════════════════════════════════════════════════════════════════

💾 **8. EMBEDDED CODER (CODE GENERATION)**
─────────────────────────────────────────────────────────────────────────

**8.1 Code Generation Workflow**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Model-Based Design → Deployment Workflow:
   
   Step 1: Model Design
   ────────────────────
   • Create Simulink model
   • Validate with simulation (MIL testing)
   
   Step 2: Configure for Code Generation
   ──────────────────────────────────────
   • Set solver: Fixed-step
   • Configure Embedded Coder settings
   • Specify target hardware
   
   Step 3: Generate Code
   ─────────────────────
   • Build model (Ctrl+B)
   • Generates C/C++ code
   • Creates .c/.h files
   
   Step 4: Compile & Deploy
   ────────────────────────
   • Cross-compile for target (e.g., ARM Cortex-M4)
   • Link with BSP/HAL
   • Flash to microcontroller
   
   Step 5: Verify
   ──────────────
   • PIL testing (Processor-in-Loop)
   • HIL testing (Hardware-in-Loop)
   • Validate code matches model behavior

**8.2 Embedded Coder Configuration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Model Configuration Parameters → Code Generation
   
   % System target file:
   % ───────────────────
   % ert.tlc (Embedded Coder Real-Time)
   % - Optimized for embedded systems
   % - Minimal footprint
   % - Fast execution
   
   % Language:
   % ─────────
   % C or C++
   
   % Code generation objectives:
   % ──────────────────────────
   % - Execution efficiency (fastest code)
   % - RAM efficiency (minimize memory)
   % - ROM efficiency (minimize code size)
   % - Traceability (comments, model reference)
   % - Safety precaution (defensive code)
   
   % Example configuration:
   set_param('myModel', 'SystemTargetFile', 'ert.tlc');
   set_param('myModel', 'TargetLang', 'C');
   set_param('myModel', 'OptimizationCustomize', 'on');
   set_param('myModel', 'GlobalDataDefinition', 'Auto');
   
   % Hardware Implementation:
   % ────────────────────────
   % Device vendor: ARM Compatible → ARM Cortex
   % Device type: ARM Cortex-M4
   % Word size: 32-bit
   % Byte ordering: Little endian
   % Signed integer division: Floor

**8.3 Generated Code Structure**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Generated Code Files:
   ─────────────────────
   
   myModel.c/.h           Main model code
   ├── myModel_step()     Step function (executes every sample time)
   ├── myModel_initialize() Initialize model
   └── myModel_terminate()  Cleanup
   
   myModel_data.c/.h      Constants, parameters
   myModel_private.h      Internal declarations
   myModel_types.h        Type definitions
   
   rtwtypes.h             Real-Time Workshop types
   rt_nonfinite.c/.h      Special values (Inf, NaN)

**Example: PID Controller Generated Code**

.. code-block:: c

   // myPID.h
   #ifndef RTW_HEADER_myPID_h_
   #define RTW_HEADER_myPID_h_
   
   #include "rtwtypes.h"
   
   // Model inputs (external signals)
   typedef struct {
       real_T setpoint;        // Referenced signal
       real_T feedback;        // Measured value
   } ExtU_myPID_T;
   
   // Model outputs (external signals)
   typedef struct {
       real_T control_output;  // PID output
   } ExtY_myPID_T;
   
   // Model states (persistent data)
   typedef struct {
       real_T Integrator_DSTATE;    // Integrator state
       real_T Filter_DSTATE;        // Derivative filter state
   } DW_myPID_T;
   
   // External inputs/outputs
   extern ExtU_myPID_T myPID_U;
   extern ExtY_myPID_T myPID_Y;
   
   // Model functions
   void myPID_initialize(void);
   void myPID_step(void);
   void myPID_terminate(void);
   
   #endif
   
   // myPID.c
   #include "myPID.h"
   
   // Model states
   DW_myPID_T myPID_DW;
   
   // External inputs
   ExtU_myPID_T myPID_U;
   
   // External outputs
   ExtY_myPID_T myPID_Y;
   
   // Model parameters
   const real_T myPID_P_Kp = 1.5;      // Proportional gain
   const real_T myPID_P_Ki = 0.1;      // Integral gain
   const real_T myPID_P_Kd = 0.05;     // Derivative gain
   
   // Initialize model
   void myPID_initialize(void)
   {
       // Initialize states to zero
       myPID_DW.Integrator_DSTATE = 0.0;
       myPID_DW.Filter_DSTATE = 0.0;
   }
   
   // Step function (executes every sample time)
   void myPID_step(void)
   {
       real_T error;
       real_T proportional;
       real_T integral;
       real_T derivative;
       
       // Calculate error
       error = myPID_U.setpoint - myPID_U.feedback;
       
       // Proportional term
       proportional = myPID_P_Kp * error;
       
       // Integral term (with state update)
       integral = myPID_P_Ki * error;
       myPID_DW.Integrator_DSTATE += integral;
       
       // Derivative term (filtered)
       derivative = myPID_P_Kd * (error - myPID_DW.Filter_DSTATE);
       myPID_DW.Filter_DSTATE = error;
       
       // PID output
       myPID_Y.control_output = proportional + 
                                myPID_DW.Integrator_DSTATE + 
                                derivative;
       
       // Saturation (limit output to [-100, 100])
       if (myPID_Y.control_output > 100.0) {
           myPID_Y.control_output = 100.0;
       } else if (myPID_Y.control_output < -100.0) {
           myPID_Y.control_output = -100.0;
       }
   }
   
   // Terminate model
   void myPID_terminate(void)
   {
       // No cleanup required
   }

**8.4 Integration with Hand-Written Code**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Method 1: Custom Code Blocks**

.. code-block:: matlab

   % In Simulink:
   % Add "S-Function" block or "MATLAB Function" block
   
   % MATLAB Function Block:
   function y = my_custom_function(u)
       % Custom algorithm not easily modeled with blocks
       
       % Example: Lookup table with interpolation
       persistent lookup_table
       if isempty(lookup_table)
           lookup_table = load_calibration_table();
       end
       
       y = interp1(lookup_table.x, lookup_table.y, u);
   end

**Method 2: Legacy Code Integration**

.. code-block:: c

   // Existing C function (hand-written, tested)
   float calculate_engine_torque(float rpm, float throttle)
   {
       // Complex proprietary algorithm
       // ...
       return torque;
   }
   
   // In Simulink:
   // Use "Legacy Code Tool" to wrap C function
   
   % MATLAB script:
   def = legacy_code('initialize');
   def.SFunctionName = 'engine_torque_sfun';
   def.OutputFcnSpec = 'single y1 = calculate_engine_torque(single u1, single u2)';
   def.HeaderFiles = {'engine_control.h'};
   def.SourceFiles = {'engine_control.c'};
   
   legacy_code('sfcn_cmex_generate', def);
   legacy_code('compile', def);
   
   % Now use "engine_torque_sfun" S-Function in model

**8.5 Code Generation Optimization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Optimizations:**

.. code-block:: text

   1. Loop Unrolling
   ─────────────────
   Before:
   for (i = 0; i < 4; i++) {
       y[i] = x[i] * gain;
   }
   
   After (unrolled):
   y[0] = x[0] * gain;
   y[1] = x[1] * gain;
   y[2] = x[2] * gain;
   y[3] = x[3] * gain;
   
   Benefit: Eliminates loop overhead, faster execution
   
   2. Inline Functions
   ───────────────────
   Configure: Code Generation → Optimization → Inline parameters
   
   Before:
   float calculate_gain(float Kp) {
       return Kp * 1.5;
   }
   y = calculate_gain(tunable_Kp);
   
   After:
   y = tunable_Kp * 1.5;  // Function inlined
   
   Benefit: Eliminates function call overhead
   
   3. Remove Dead Code
   ───────────────────
   Configure: Code Generation → Optimization → Remove unused signals
   
   Removes code for:
   • Unconnected blocks
   • Constant propagation results
   • Unreachable states
   
   4. Integer-Only Math
   ────────────────────
   Replace floating-point with fixed-point for:
   • Faster execution (no FPU overhead)
   • Deterministic timing
   • Lower power consumption

**Memory Optimization:**

.. code-block:: matlab

   % Model Configuration Parameters → Code Generation → Optimization
   
   % Global data definition: Auto
   % - Automatically determines optimal storage (stack vs global)
   
   % Signal storage reuse: on
   % - Reuses memory for signals with non-overlapping lifetimes
   
   % Example: Before optimization
   % Memory: 1024 bytes RAM (each signal gets own buffer)
   
   % After optimization with signal reuse:
   % Memory: 512 bytes RAM (signals share buffers)

═══════════════════════════════════════════════════════════════════════

🔢 **9. FIXED-POINT ARITHMETIC**
─────────────────────────────────────────────────────────────────────────

**9.1 Why Fixed-Point?**
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Floating-Point vs Fixed-Point:
   
   Floating-Point (float, double):
   ───────────────────────────────
   ✅ Wide range: ±10⁻³⁸ to ±10³⁸
   ✅ Good precision across range
   ❌ Slower (FPU required or software emulation)
   ❌ Non-deterministic timing
   ❌ Higher power consumption
   
   Fixed-Point (integers with implied decimal):
   ────────────────────────────────────────────
   ✅ Fast (integer ALU)
   ✅ Deterministic timing
   ✅ Lower power
   ✅ Available on all MCUs
   ❌ Limited range
   ❌ Precision varies with scaling
   ❌ Requires careful design (overflow, quantization)
   
   Use Fixed-Point When:
   ─────────────────────
   • No hardware FPU (e.g., Cortex-M0, M3)
   • Real-time determinism required
   • Power-constrained application
   • Cost-sensitive (simpler MCU)

**9.2 Fixed-Point Representation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Fixed-Point Notation: Qm.n
   ───────────────────────────
   • m: Number of integer bits
   • n: Number of fractional bits
   • Total bits: m + n + 1 (sign bit)
   
   Example: Q15 (also written as Q0.15)
   ────────────────────────────────────
   • 16-bit signed
   • 1 sign bit
   • 0 integer bits
   • 15 fractional bits
   
   Binary: S.FFFFFFFFFFFFFFFF
   Range: -1.0 to +0.999969482421875
   Resolution: 2⁻¹⁵ = 0.000030517578125
   
   Example value: 0.5
   Binary: 0.100000000000000 = 0x4000
   
   Example: Q7.8 (16-bit signed)
   ─────────────────────────────
   • 1 sign bit
   • 7 integer bits
   • 8 fractional bits
   
   Binary: S.IIIIIII.FFFFFFFF
   Range: -128.0 to +127.99609375
   Resolution: 2⁻⁸ = 0.00390625
   
   Example value: 25.75
   Binary: 0.0011001.11000000 = 0x19C0

**9.3 Fixed-Point in Simulink**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Convert model to fixed-point:
   % 1. Apps → Fixed-Point Tool
   % 2. Select blocks to convert
   % 3. Specify data types
   
   % Manual data type specification:
   % In block parameters → Data Type: fixdt(1, 16, 15)
   %                                    │   │   └─ Fraction length
   %                                    │   └───── Word length
   %                                    └───────── Signed (1) or unsigned (0)
   
   % Example: PID Controller in Fixed-Point
   
   % Gains (Q7.8 format)
   Kp_fixed = fi(1.5, 1, 16, 8);   % Kp = 1.5
   Ki_fixed = fi(0.1, 1, 16, 8);   % Ki = 0.1
   Kd_fixed = fi(0.05, 1, 16, 8);  % Kd = 0.05
   
   % In Simulink Gain blocks:
   % Data type: fixdt(1, 16, 8)
   % Gain: Kp_fixed

**Fixed-Point Math Operations:**

.. code-block:: c

   // Addition/Subtraction: Same scaling
   // Q15 + Q15 = Q15
   int16_t a_q15 = 16384;  // 0.5 in Q15
   int16_t b_q15 = 8192;   // 0.25 in Q15
   int16_t sum_q15 = a_q15 + b_q15;  // 0.75 in Q15
   
   // Multiplication: Sum of scales
   // Q15 × Q15 = Q30 (need to shift back to Q15)
   int16_t x_q15 = 16384;  // 0.5
   int16_t y_q15 = 8192;   // 0.25
   int32_t product_q30 = (int32_t)x_q15 * (int32_t)y_q15;
   int16_t result_q15 = (int16_t)(product_q30 >> 15);  // 0.125
   
   // Division: Difference of scales
   // Q15 ÷ Q15 = Q0 (need to pre-shift)
   int32_t numerator_q30 = ((int32_t)x_q15) << 15;
   int16_t quotient_q15 = (int16_t)(numerator_q30 / y_q15);

**9.4 Overflow and Saturation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Overflow handling:
   % Model Configuration → Diagnostics → Data Validity
   
   % Wrap (default):
   % - Value wraps around (modulo arithmetic)
   % - Fastest
   % - Can cause instability
   
   % Saturate:
   % - Clamps to min/max value
   % - Safer for control systems
   % - Slight performance overhead
   
   % Example: Saturate on overflow
   set_param('myModel', 'SaturateOnIntegerOverflow', 'on');
   
   % In generated code:
   // Saturation macro
   #define SATURATE(x, min, max) ((x) > (max) ? (max) : ((x) < (min) ? (min) : (x)))
   
   int16_t result = a_q15 + b_q15;
   result = SATURATE(result, -32768, 32767);

═══════════════════════════════════════════════════════════════════════

🚀 **10. CODE GENERATION BEST PRACTICES**
─────────────────────────────────────────────────────────────────────────

**10.1 Model Architecture for Code Generation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Recommended Model Structure:
   ────────────────────────────
   
   Top-Level Model
   ├── Algorithm (Model Reference)
   │   └── Core control logic (reusable, portable)
   ├── I/O Drivers (Subsystem)
   │   ├── ADC reads
   │   ├── PWM outputs
   │   └── Communication interfaces
   └── Scheduler (Subsystem)
       ├── Fast loop (1 kHz): Control
       ├── Medium loop (100 Hz): Monitoring
       └── Slow loop (10 Hz): Diagnostics
   
   Benefits:
   ─────────
   ✅ Reusable algorithm (independent of hardware)
   ✅ Separate I/O from logic (easier testing)
   ✅ Multi-rate execution (efficiency)
   ✅ Clear interfaces (inputs/outputs)

**10.2 Naming Conventions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Model Configuration → Code Generation → Identifiers
   
   % Configure naming:
   set_param('myModel', 'MaxIdLength', 31);
   set_param('myModel', 'InlinedPrmAccess', 'Literals');
   
   % Custom identifier format:
   % - Global variables: prefix 'g_'
   % - Constants: prefix 'k_'
   % - Parameters: prefix 'p_'
   
   % Example generated identifiers:
   % Global state: g_motor_ctrl_DW
   % Constant: k_motor_ctrl_Kp
   % Input: motor_ctrl_U
   % Output: motor_ctrl_Y

**10.3 Code Reviews and Traceability**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Enable traceability (links code ↔ model):
   % Code Generation → Report → Create code generation report
   
   % Generated HTML report contains:
   % • Code metrics (ROM/RAM usage, stack depth)
   % • Hyperlinks: code line → model block
   % • Bidirectional traceability
   % • Optimization summary
   
   % Example: Click function in report → highlights block in Simulink
   
   % Code review comments in generated code:
   % Code Generation → Comments
   % ☑ Include comments
   % ☑ Simulink block descriptions
   % ☑ Stateflow object descriptions

**10.4 Multi-Rate Systems**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Single-Rate vs Multi-Rate:
   
   Single-Rate (all blocks execute at same rate):
   ───────────────────────────────────────────────
   • Simple scheduler
   • Wasteful (slow tasks run too often)
   
   Multi-Rate (tasks execute at different rates):
   ───────────────────────────────────────────────
   • Efficient CPU usage
   • More complex scheduler
   
   Example:
   ────────
   Base rate: 1 kHz (Ts = 0.001)
   
   Fast task (1 kHz):
   • Current control loop
   • PWM update
   
   Medium task (100 Hz):
   • Speed control loop
   • Temperature monitoring
   
   Slow task (10 Hz):
   • Diagnostics
   • Communication
   
   In Simulink:
   ────────────
   • Set different sample times for subsystems
   • Fast subsystem: Sample time = 0.001
   • Slow subsystem: Sample time = 0.1
   
   Generated code:
   ───────────────
   void myModel_step(int_T tid) {
       switch(tid) {
           case 0:  // Fast task (1 kHz)
               fast_subsystem_step();
               break;
           case 1:  // Medium task (100 Hz)
               medium_subsystem_step();
               break;
           case 2:  // Slow task (10 Hz)
               slow_subsystem_step();
               break;
       }
   }

**10.5 AUTOSAR Code Generation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % AUTOSAR Blockset:
   % • Model AUTOSAR software components
   % • Generate AUTOSAR-compliant C code
   % • ARXML files for integration
   
   % Example: AUTOSAR Classic SWC (Software Component)
   
   % 1. Create AUTOSAR model:
   % Apps → AUTOSAR Component Designer
   
   % 2. Define ports:
   % Require Ports (inputs):
   %   - SpeedSensor: UInt16, 0-65535 RPM
   %   - ThrottlePosition: UInt8, 0-100%
   
   % Provide Ports (outputs):
   %   - EngineControl: UInt8, 0-100% duty cycle
   
   % 3. Map Simulink model to AUTOSAR:
   % - Inports → Require Ports
   % - Outports → Provide Ports
   
   % 4. Generate code:
   % - .c/.h files (SWC implementation)
   % - .arxml (AUTOSAR component description)
   
   % 5. Integration:
   % - Import ARXML into AUTOSAR RTE
   % - Link with other SWCs
   % - Generate complete ECU software

═══════════════════════════════════════════════════════════════════════

🧪 **11. MODEL-IN-LOOP (MIL) TESTING**
─────────────────────────────────────────────────────────────────────────

**11.1 V-Model Testing Strategy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   V-Model Test Levels (Left to Right):
   
   Requirements ──────────────────────────► System Test
        │                                        ▲
        ▼                                        │
   Architecture ───────────────────────► Integration Test
        │                                        ▲
        ▼                                        │
   Detailed Design ────────────────────► MIL Testing
        │                              (Model-in-Loop)
        ▼                                        ▲
   Generated Code ─────────────────────► SIL Testing
        │                              (Software-in-Loop)
        ▼                                        ▲
   Compiled Binary ────────────────────► PIL Testing
        │                              (Processor-in-Loop)
        ▼                                        │
   Deployed System ────────────────────► HIL Testing
                                        (Hardware-in-Loop)

**11.2 MIL Testing (Model-in-Loop)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Validate model behavior matches requirements

.. code-block:: text

   MIL Testing Environment:
   ────────────────────────
   
   ┌──────────────────────────────────────────────┐
   │         Simulink Desktop                     │
   │                                              │
   │  ┌────────────┐      ┌──────────────────┐   │
   │  │ Test       │─────►│  Controller      │   │
   │  │ Harness    │      │  Model           │   │
   │  │            │      │  (Simulink)      │   │
   │  │ • Inputs   │      └──────────────────┘   │
   │  │ • Expected │             │                │
   │  │   outputs  │             ▼                │
   │  │ • Pass/Fail│      ┌──────────────────┐   │
   │  │   criteria │◄─────│  Results         │   │
   │  └────────────┘      │  Comparison      │   │
   │                      └──────────────────┘   │
   └──────────────────────────────────────────────┘
   
   Advantages:
   ───────────
   ✅ Fast simulation (no hardware needed)
   ✅ Easy debugging (inspect all signals)
   ✅ Complete coverage (test all states/transitions)
   ✅ Ideal precision (no quantization errors)
   
   Tests Performed:
   ────────────────
   • Functional correctness
   • Boundary conditions
   • State transitions
   • Algorithm validation

**Creating Test Harness:**

.. code-block:: matlab

   % Simulink Test Toolbox
   % 1. Right-click model → Simulink Test → Create Test Harness
   % 2. Select inputs/outputs to test
   % 3. Choose harness type:
   %    - Signal Builder: Manual test sequences
   %    - Test Sequence: Programmatic test scenarios
   
   % Example: PID Controller Test Harness
   
   % Test case 1: Step response
   test_input = [0 0 0 1 1 1 1 1];  % Step at t=3
   expected_rise_time = 2.0;         % Should settle in 2 sec
   expected_overshoot = 0.1;         % Max 10% overshoot
   
   % Test case 2: Disturbance rejection
   test_disturbance = [0 0 0.5 0 0];  % Disturbance at t=2
   expected_recovery = 1.5;            % Recover in 1.5 sec
   
   % Run test
   sim('PID_TestHarness');
   
   % Verify results
   assert(rise_time < expected_rise_time, 'Rise time too slow');
   assert(overshoot < expected_overshoot, 'Overshoot too large');

**11.3 Requirements-Based Testing**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Link requirements to test cases:
   % 1. Apps → Requirements Editor
   % 2. Import requirements from document
   % 3. Link requirements to model blocks
   % 4. Create test cases for each requirement
   
   % Example requirement:
   % REQ-001: "PID controller shall maintain speed within ±5 RPM"
   
   % Test sequence:
   test_speeds = [100, 200, 500, 1000, 2000];
   
   for setpoint = test_speeds
       % Set input
       set_param('PID_Model/Setpoint', 'Value', num2str(setpoint));
       
       % Simulate
       sim('PID_Model');
       
       % Check steady-state error
       final_error = abs(output(end) - setpoint);
       assert(final_error < 5, sprintf('REQ-001 failed at %d RPM', setpoint));
   end
   
   % Generate traceability report:
   % Simulink Test → Generate Report
   % Shows: Requirements → Test Cases → Results

**11.4 Coverage Analysis**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Coverage Metrics:
   ─────────────────
   
   Decision Coverage:
   • Every condition evaluated to true and false
   • Example: if (temp > 80) → Test temp=70 and temp=90
   
   Condition Coverage:
   • Every boolean sub-expression evaluated
   • Example: if (A && B) → Test (T,T), (T,F), (F,T), (F,F)
   
   Modified Condition/Decision Coverage (MC/DC):
   • Each condition independently affects outcome
   • Required for DO-178C Level A
   
   State Coverage:
   • Every state in Stateflow visited
   • Every transition exercised

**Simulink Coverage Tool:**

.. code-block:: matlab

   % Enable coverage:
   % Apps → Simulink Coverage
   
   % Coverage settings:
   cvmodel = cvmodel('myModel');
   cvmodel.Settings.Decision = true;
   cvmodel.Settings.Condition = true;
   cvmodel.Settings.MCDC = true;
   
   % Run simulation with coverage
   sim('myModel');
   
   % Generate coverage report
   cvhtml('coverage_results', cvmodel);
   
   % View report: Shows uncovered decisions/conditions
   % Goal: 100% coverage for safety-critical code

═══════════════════════════════════════════════════════════════════════

💻 **12. SOFTWARE-IN-LOOP (SIL) TESTING**
─────────────────────────────────────────────────────────────────────────

**12.1 SIL Testing Concept**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Verify generated code matches model behavior

.. code-block:: text

   SIL Testing Environment:
   ────────────────────────
   
   ┌──────────────────────────────────────────────────────┐
   │              Simulink Desktop                        │
   │                                                      │
   │  ┌──────────────┐           ┌──────────────────┐    │
   │  │   Plant      │──input──► │  Generated Code  │    │
   │  │   Model      │           │  (Compiled .exe) │    │
   │  │  (Simulink)  │           └──────────────────┘    │
   │  └──────────────┘                    │               │
   │                                      │ output        │
   │                                      ▼               │
   │                             ┌──────────────────┐    │
   │  ┌──────────────┐           │   Model          │    │
   │  │  Reference   │──input──► │   (Simulink)     │    │
   │  │  (Original)  │           └──────────────────┘    │
   │  └──────────────┘                    │               │
   │                                      ▼               │
   │                             ┌──────────────────┐    │
   │                             │  Compare Outputs │    │
   │                             │  (Should match)  │    │
   │                             └──────────────────┘    │
   └──────────────────────────────────────────────────────┘
   
   What SIL Tests:
   ───────────────
   ✅ Code generation correctness
   ✅ Numerical differences (floating → fixed-point)
   ✅ Optimization effects
   ✅ Compiler behavior
   
   Detects:
   ────────
   ❌ Code generation bugs
   ❌ Configuration errors
   ❌ Precision loss
   ❌ Timing differences

**12.2 Setting Up SIL Testing**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Method 1: SIL Block
   % ───────────────────
   % 1. Right-click model reference block
   % 2. Block Parameters → Code Interface → SIL
   % 3. Run simulation (uses compiled C code instead of model)
   
   % Method 2: Programmatic SIL
   % ──────────────────────────
   % Create SIL model
   rtwbuild('myController', 'SIL');
   
   % Load both models
   load_system('myController');        % Original model
   load_system('myController_sil');    % SIL version
   
   % Create test harness with both
   % Compare outputs
   
   % Tolerance for numerical differences:
   tolerance = 1e-6;  % Allow small floating-point errors
   
   sim('Comparison_Model');
   
   % Check difference
   max_diff = max(abs(model_output - sil_output));
   assert(max_diff < tolerance, 'SIL mismatch detected');

**12.3 Back-to-Back Testing**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Simulink Test: Equivalence Testing
   % ───────────────────────────────────
   
   % Create equivalence test:
   % 1. Simulink Test → Test Manager
   % 2. New Test File → Equivalence Test
   % 3. Select baseline: Original model
   % 4. Select system under test: SIL model
   % 5. Define test inputs
   
   % Test configuration:
   test_config.baseline_mode = 'Normal';     % Simulink model
   test_config.sut_mode = 'SIL';             % Generated code
   test_config.tolerance = 1e-5;
   
   % Run equivalence test
   results = sltest.testmanager.run;
   
   % Results show:
   % • Signal-by-signal comparison
   % • Maximum absolute difference
   % • Relative error percentage
   % • Pass/fail status

═══════════════════════════════════════════════════════════════════════

🔧 **13. PROCESSOR-IN-LOOP (PIL) TESTING**
─────────────────────────────────────────────────────────────────────────

**13.1 PIL Testing Concept**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Verify code executes correctly on target processor

.. code-block:: text

   PIL Testing Environment:
   ────────────────────────
   
   ┌──────────────────────────────────────────────────────┐
   │              Development PC                          │
   │                                                      │
   │  ┌──────────────┐           Serial/JTAG             │
   │  │  Simulink    │◄──────────────────────┐           │
   │  │  Model       │                        │           │
   │  │  (Plant)     │                        │           │
   │  └──────┬───────┘                        │           │
   │         │                                 │           │
   │         │ input                           │ output    │
   │         ▼                                 │           │
   │  ┌──────────────────────────────────────┐│           │
   │  │  Communication Layer                 ││           │
   │  │  (XCP/Serial)                        ││           │
   │  └──────────────────────────────────────┘│           │
   └─────────────────────────────────────────────────────┘
                                               │
                    ┌──────────────────────────┘
                    │
   ┌────────────────▼────────────────────────────────────┐
   │         Target Hardware (e.g., STM32)               │
   │                                                     │
   │  ┌──────────────────────────────────────┐          │
   │  │  Generated Code                      │          │
   │  │  Running on ARM Cortex-M4            │          │
   │  │                                      │          │
   │  │  • Actual processor timing           │          │
   │  │  • Real memory constraints           │          │
   │  │  • Actual fixed-point arithmetic     │          │
   │  └──────────────────────────────────────┘          │
   └─────────────────────────────────────────────────────┘
   
   What PIL Tests:
   ───────────────
   ✅ Processor-specific behavior (endianness, alignment)
   ✅ Compiler optimizations
   ✅ Timing on actual hardware
   ✅ Memory usage (stack, heap)
   ✅ Interrupt handling
   
   Detects:
   ────────
   ❌ Processor-specific bugs
   ❌ Stack overflow
   ❌ Timing violations
   ❌ Uninitialized variables

**13.2 PIL Configuration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Configure target hardware:
   % Model Configuration → Hardware Implementation
   
   % Device vendor: ARM Compatible → ARM Cortex
   % Device type: ARM Cortex-M4
   % 
   % Code Generation → Interface → Code replacement library
   % Select: ARM Cortex-M optimized (uses CMSIS-DSP)
   
   % PIL Communication:
   % Code Generation → Interface → PIL communication
   % - Serial: UART (slower, simple)
   % - XCP on Ethernet: Faster, more features
   % - JTAG: Debug interface
   
   % Example: Serial PIL
   set_param('myModel', 'ProdHWDeviceType', 'ARM Compatible->ARM Cortex');
   set_param('myModel', 'PILInterface', 'XCP on Serial');
   set_param('myModel', 'ExtModeSerialPort', '/dev/ttyUSB0');
   
   % Build PIL executable
   rtwbuild('myModel', 'PIL');
   
   % Run PIL test (code runs on target hardware)
   sim('myModel_pil');

**13.3 Execution Profiling**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Enable profiling:
   % Code Generation → Verification → Measure task execution time
   
   % Generate profiling report
   set_param('myModel', 'CodeProfilingInstrumentation', 'on');
   
   % Build and run PIL
   rtwbuild('myModel', 'PIL');
   sim('myModel_pil');
   
   % View profiling report:
   % Shows:
   % • Execution time per function (min/max/average)
   % • Stack usage
   % • CPU utilization
   % • Worst-case execution time (WCET)
   
   % Example profiling results:
   % Function               Min(µs)  Max(µs)  Avg(µs)
   % ────────────────────────────────────────────────
   % myModel_step()         45.2     52.8     48.1
   % └─ PID_controller()    12.3     14.1     13.0
   % └─ motor_control()     18.5     22.3     19.8
   % └─ sensor_read()       10.1     12.5     11.2
   
   % Verify timing budget:
   sample_time = 1000;  % µs (1 kHz)
   max_exec_time = 52.8;
   assert(max_exec_time < sample_time * 0.8, 'Timing budget exceeded');

═══════════════════════════════════════════════════════════════════════

🖥️ **14. HARDWARE-IN-LOOP (HIL) TESTING**
─────────────────────────────────────────────────────────────────────────

**14.1 HIL Testing Concept**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:** Test complete ECU with real-time plant simulation

.. code-block:: text

   HIL Testing Environment:
   ────────────────────────
   
   ┌──────────────────────────────────────────────────────┐
   │         HIL Simulator (Real-Time PC)                 │
   │                                                      │
   │  ┌───────────────────────────────────────┐          │
   │  │  Plant Model (Motor, Vehicle, etc.)   │          │
   │  │  Running in real-time (Simulink RT)   │          │
   │  │                                        │          │
   │  │  • Electric motor dynamics             │          │
   │  │  • Sensor models (ADC, CAN)            │          │
   │  │  • Fault injection                     │          │
   │  └───────────────────────────────────────┘          │
   │           │                           ▲              │
   │           │ Actuators                 │ Sensors      │
   │           │ (PWM, Digital)            │ (Analog, CAN)│
   │           ▼                           │              │
   │  ┌──────────────────────────────────────┐           │
   │  │  I/O Interface (dSPACE, Speedgoat)   │           │
   │  └──────────────────────────────────────┘           │
   └─────────────────────────────────────────────────────┘
                    │                      ▲
                    │                      │
   ┌────────────────▼──────────────────────┴──────────────┐
   │         ECU Under Test                               │
   │         (Production Controller)                      │
   │                                                      │
   │  • Reads sensors from HIL                            │
   │  • Executes control algorithm                        │
   │  • Sends actuator commands to HIL                    │
   └──────────────────────────────────────────────────────┘
   
   HIL Benefits:
   ─────────────
   ✅ Test ECU without physical plant (motor, vehicle)
   ✅ Repeatability (same test conditions every time)
   ✅ Safety (test dangerous scenarios without risk)
   ✅ Fault injection (sensor failures, CAN errors)
   ✅ Regression testing (automated test suites)
   
   Example Scenarios:
   ──────────────────
   • Motor control: Test with various loads, speeds
   • ADAS: Simulate traffic scenarios
   • Engine control: Test cold start, hot conditions
   • Safety: Test emergency braking, overheat

**14.2 HIL Hardware Platforms**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Common HIL Platforms:
   ─────────────────────
   
   dSPACE:
   • Scalexio: Modular, high-channel-count
   • MicroAutoBox: Compact, automotive
   • Features: CAN/LIN/FlexRay, analog I/O
   
   Speedgoat:
   • Real-Time Target Machines
   • Simulink Real-Time integration
   • Various I/O modules (CAN, Ethernet, analog)
   
   National Instruments:
   • PXI-based systems
   • LabVIEW Real-Time
   • VeriStand for test automation
   
   OPAL-RT:
   • OP5600 series
   • Ultra-low latency (<1 µs)
   • Power electronics testing

**14.3 Real-Time Model Deployment**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Using Simulink Real-Time (Speedgoat target):
   
   % 1. Configure model for real-time:
   % Model Configuration → Solver
   % - Type: Fixed-step
   % - Solver: ode4
   % - Fixed-step size: 0.001 (1 kHz)
   
   % 2. Add I/O driver blocks:
   % Simulink Real-Time → I/O Driver
   % - Analog Input (ADC channels)
   % - Analog Output (DAC channels)
   % - Digital I/O
   % - CAN Communication
   
   % 3. Build real-time application:
   set_param('PlantModel', 'SystemTargetFile', 'slrttarget.tlc');
   rtwbuild('PlantModel');
   
   % 4. Download to target:
   tg = slrealtime;
   tg.connect('192.168.1.100');  % Target IP
   tg.load('PlantModel');
   
   % 5. Start real-time execution:
   tg.start();
   
   % 6. Monitor signals:
   % Simulink Real-Time Explorer
   % - View signals in real-time
   % - Log data for analysis
   % - Tune parameters on-the-fly

**14.4 Automated HIL Testing**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Test automation script:
   
   % Connect to HIL
   tg = slrealtime('TargetPC1');
   
   % Load plant model
   tg.load('MotorPlant');
   
   % Test suite: Different speed setpoints
   test_speeds = [500, 1000, 1500, 2000, 2500];
   
   for speed = test_speeds
       % Set parameter
       tg.setparam('SpeedSetpoint', speed);
       
       % Run test (10 seconds)
       tg.start();
       pause(10);
       tg.stop();
       
       % Retrieve logged data
       data = tg.getlog();
       actual_speed = data.Signals(1).Values(end);
       
       % Verify
       error = abs(actual_speed - speed);
       assert(error < 10, sprintf('Speed error at %d RPM: %.1f', speed, error));
       
       fprintf('Test PASSED: Setpoint %d RPM, Actual %.1f RPM\n', speed, actual_speed);
   end
   
   % Fault injection test:
   % Simulate sensor failure
   tg.setparam('SensorFault', 1);  % Inject fault
   pause(2);
   
   % Verify ECU enters safe mode
   ecu_state = read_can_signal('ECU_State');
   assert(strcmp(ecu_state, 'SAFE_MODE'), 'ECU did not enter safe mode');

═══════════════════════════════════════════════════════════════════════

🏎️ **15. AUTOSAR INTEGRATION**
─────────────────────────────────────────────────────────────────────────

**15.1 AUTOSAR Architecture Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   AUTOSAR Layered Architecture:
   
   ┌─────────────────────────────────────────────────────┐
   │         Application Layer                           │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
   │  │   SWC    │  │   SWC    │  │   SWC    │          │
   │  │(Software │  │(Software │  │(Software │          │
   │  │Component)│  │Component)│  │Component)│          │
   │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
   │       │             │             │                 │
   └───────┼─────────────┼─────────────┼─────────────────┘
           │             │             │
   ┌───────▼─────────────▼─────────────▼─────────────────┐
   │              RTE (Runtime Environment)              │
   │        (Generated communication layer)              │
   └─────────────────────────────────────────────────────┘
           │             │             │
   ┌───────▼─────────────▼─────────────▼─────────────────┐
   │           Basic Software (BSW)                      │
   │  ┌──────────────────────────────────────────┐      │
   │  │  Services (Diagnostic, NVM, Watchdog)    │      │
   │  └──────────────────────────────────────────┘      │
   │  ┌──────────────────────────────────────────┐      │
   │  │  ECU Abstraction (ADC, PWM, CAN)         │      │
   │  └──────────────────────────────────────────┘      │
   │  ┌──────────────────────────────────────────┐      │
   │  │  MCAL (Microcontroller Abstraction)      │      │
   │  └──────────────────────────────────────────┘      │
   └─────────────────────────────────────────────────────┘
           │
   ┌───────▼─────────────────────────────────────────────┐
   │              Microcontroller                        │
   └─────────────────────────────────────────────────────┘

**15.2 AUTOSAR Software Components (SWC)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % AUTOSAR Blockset workflow:
   % 1. Design algorithm in Simulink
   % 2. Configure AUTOSAR properties
   % 3. Generate code + ARXML
   
   % Example: Speed Controller SWC
   
   % Create AUTOSAR model:
   % Apps → AUTOSAR Component Designer
   
   % Define component:
   % Component: SpeedController
   % Runnable: SpeedControl_Run (execution function)
   % Period: 10 ms
   
   % Ports:
   % ──────
   % Require Ports (inputs):
   %   R-Port: SpeedSensor
   %   └─ Interface: SensorData
   %      └─ Element: Speed (uint16, 0-10000 RPM)
   %   
   %   R-Port: TargetSpeed
   %   └─ Interface: ControlData
   %      └─ Element: Setpoint (uint16)
   
   % Provide Ports (outputs):
   %   P-Port: ActuatorCmd
   %   └─ Interface: ActuatorData
   %      └─ Element: DutyCycle (uint8, 0-100%)
   
   % Calibration Parameters:
   %   Kp: float32 = 0.5
   %   Ki: float32 = 0.1
   %   Kd: float32 = 0.05
   
   % Map Simulink to AUTOSAR:
   % ────────────────────────
   % Inport "Speed" → R-Port "SpeedSensor/Speed"
   % Inport "Target" → R-Port "TargetSpeed/Setpoint"
   % Outport "Control" → P-Port "ActuatorCmd/DutyCycle"

**15.3 Code Generation for AUTOSAR**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % Generate AUTOSAR code:
   % Apps → AUTOSAR Component Designer → Export
   
   % Generated files:
   % ────────────────
   % SpeedController.c/.h       SWC implementation
   % SpeedController_swc.arxml  Component description
   % SpeedController.a2l        Calibration data (for XCP)
   
   % Integration steps:
   % ──────────────────
   % 1. Import ARXML into AUTOSAR configuration tool (Vector DaVinci, EB tresos)
   % 2. Configure RTE generation
   % 3. Generate RTE code
   % 4. Link SWC with RTE
   % 5. Build ECU software

**Generated AUTOSAR C Code Example:**

.. code-block:: c

   // Rte_SpeedController.h (generated by RTE)
   
   // Runnable prototype
   void SpeedControl_Run(void);
   
   // RTE API for reading input
   Std_ReturnType Rte_Read_SpeedSensor_Speed(uint16 *data);
   Std_ReturnType Rte_Read_TargetSpeed_Setpoint(uint16 *data);
   
   // RTE API for writing output
   Std_ReturnType Rte_Write_ActuatorCmd_DutyCycle(uint8 data);
   
   // Calibration parameter access
   float32 Rte_CData_Kp(void);
   float32 Rte_CData_Ki(void);
   float32 Rte_CData_Kd(void);
   
   // SpeedController.c (generated from Simulink model)
   
   void SpeedControl_Run(void)
   {
       uint16 current_speed;
       uint16 target_speed;
       float32 error;
       float32 control_output;
       uint8 duty_cycle;
       
       // Read inputs via RTE
       Rte_Read_SpeedSensor_Speed(&current_speed);
       Rte_Read_TargetSpeed_Setpoint(&target_speed);
       
       // PID calculation (generated from Simulink model)
       error = (float32)target_speed - (float32)current_speed;
       control_output = Rte_CData_Kp() * error + 
                        /* integral and derivative terms */;
       
       // Saturate and convert to uint8
       duty_cycle = (uint8)SATURATE(control_output, 0, 100);
       
       // Write output via RTE
       Rte_Write_ActuatorCmd_DutyCycle(duty_cycle);
   }

**15.4 AUTOSAR Adaptive (SOME/IP)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   AUTOSAR Adaptive Platform:
   ──────────────────────────
   (For high-performance ECUs: IFE, ADAS, autonomous driving)
   
   Differences from Classic:
   ─────────────────────────
   Classic AUTOSAR:
   • Static configuration
   • CAN/FlexRay communication
   • Safety-critical applications
   
   Adaptive AUTOSAR:
   • Dynamic service discovery
   • Ethernet/SOME/IP communication
   • High-performance computing
   • POSIX OS (Linux, QNX)
   
   Example: Camera Processing Service
   ───────────────────────────────────
   Service: ImageProcessing
   Methods:
   • ProcessFrame(Image in, DetectionList out)
   Events:
   • ObjectDetected(ObjectInfo)
   
   In Simulink:
   • AUTOSAR Adaptive Blockset
   • Define service interfaces
   • Generate C++ ara::com code

═══════════════════════════════════════════════════════════════════════

✈️ **16. DO-178C CERTIFICATION (AVIONICS)**
─────────────────────────────────────────────────────────────────────────

**16.1 DO-178C Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   DO-178C: Software Considerations in Airborne Systems
   
   Software Levels (based on failure impact):
   ──────────────────────────────────────────
   
   Level A (Catastrophic):
   • Failure: Loss of aircraft, fatalities
   • Examples: Flight control, engine FADEC
   • Requirements: Most stringent
   • Coverage: MC/DC (100%)
   
   Level B (Hazardous):
   • Failure: Large reduction in safety margins
   • Examples: Navigation, displays
   • Coverage: Decision (100%)
   
   Level C (Major):
   • Failure: Significant reduction in safety
   • Examples: Autopilot, communication
   • Coverage: Statement (100%)
   
   Level D (Minor):
   • Failure: Minor impact on safety
   • Examples: Cabin entertainment
   • Coverage: Structural (test exists)
   
   Level E (No Effect):
   • Failure: No impact on safety
   • Coverage: None required

**16.2 DO-178C Process for Model-Based Development**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   DO-178C + DO-331 (Model-Based Development Supplement):
   
   Objectives:
   ───────────
   1. Requirements traceability
      • High-level req → Low-level req → Model → Code → Tests
   
   2. Model coverage
      • Decision coverage (Level B)
      • MC/DC coverage (Level A)
   
   3. Structural coverage
      • Code coverage from tests
   
   4. Tool qualification
      • Embedded Coder must be qualified (DO-330)
      • Simulink Verification and Validation
   
   5. Documentation
      • Software Development Plan
      • Software Verification Plan
      • Software Configuration Management Plan
      • Software Quality Assurance Plan

**16.3 DO-178C Workflow in Simulink**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % DO Qualification Kit (MathWorks):
   
   % 1. Requirements Management:
   % ──────────────────────────
   % Apps → Requirements Editor
   % Import requirements from DOORS, ReqIF
   % Link requirements to model blocks
   
   % 2. Model Coverage:
   % ──────────────────
   % Apps → Simulink Coverage
   % Enable MC/DC coverage
   set_param('FlightControl', 'CovMetricSettings', 'dw');  % Decision + MC/DC
   
   % 3. Run tests with coverage:
   cvmodel = cvtest('FlightControl');
   sim('FlightControl');
   
   % 4. Generate coverage report:
   cvhtml('DO178_Coverage', cvmodel);
   
   % Verify 100% MC/DC coverage (Level A requirement)
   assert(cvmodel.metrics.mcdc == 100, 'MC/DC coverage incomplete');
   
   % 5. Code Generation with Traceability:
   % ─────────────────────────────────────
   % Code Generation → Report → Create code generation report
   % Generates HTML with bidirectional traceability:
   %   Requirement → Model → Code
   %   Code → Model → Requirement
   
   % 6. Tool Qualification:
   % ──────────────────────
   % Use DO Qualification Kit
   % Provides Tool Qualification Package:
   %   • Tool Operational Requirements
   %   • Tool Qualification Plan
   %   • Tool Accomplishment Summary
   
   % 7. Static Analysis:
   % ───────────────────
   % Apps → Polyspace Bug Finder
   % Detects:
   %   • Uninitialized variables
   %   • Array overruns
   %   • Division by zero
   %   • Dead code
   
   % 8. Documentation Generation:
   % ────────────────────────────
   % Simulink Report Generator
   % Generates DO-178C compliant documents

**16.4 Example: Level A Flight Control**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Flight Control Pitch Loop (DO-178C Level A):
   
   Requirements:
   ─────────────
   REQ-FC-001: System shall maintain pitch angle within ±2° of target
   REQ-FC-002: Control surface deflection limited to ±25°
   REQ-FC-003: System shall detect sensor failures within 100 ms
   
   Model Structure:
   ────────────────
   • PitchController (main algorithm)
     ├─ SensorInput (ARINC-429 receive)
     ├─ PID_Control (pitch regulation)
     ├─ Saturation (±25° limit)
     ├─ FaultDetection (sensor validation)
     └─ ActuatorOutput (ARINC-429 transmit)
   
   Test Cases (MC/DC coverage):
   ────────────────────────────
   TC-001: Normal operation (0° → 10° step)
   TC-002: Saturation test (command 30°, expect 25°)
   TC-003: Sensor fault (inject invalid data)
   TC-004: Boundary conditions (±2° tolerance)
   
   Verification:
   ─────────────
   • MIL: Model functional correctness
   • SIL: Code generation correctness
   • PIL: Target processor validation
   • HIL: Full system integration
   
   Deliverables:
   ─────────────
   • Software Requirements Specification
   • Model design document
   • Test procedures and results
   • Coverage reports (100% MC/DC)
   • Traceability matrix
   • Tool qualification data

═══════════════════════════════════════════════════════════════════════

🚗 **17. ISO 26262 CERTIFICATION (AUTOMOTIVE)**
─────────────────────────────────────────────────────────────────────────

**17.1 ISO 26262 Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ISO 26262: Functional Safety for Road Vehicles
   
   ASIL Levels (Automotive Safety Integrity Level):
   ─────────────────────────────────────────────────
   
   ASIL D (Highest):
   • Risk: High severity, high exposure, high controllability
   • Examples: ABS, ESC, airbag control
   • Requirements: Most stringent
   
   ASIL C:
   • Examples: Electric power steering
   
   ASIL B:
   • Examples: Brake lights
   
   ASIL A (Lowest):
   • Examples: Rear wiper
   
   QM (Quality Managed):
   • No safety requirements
   • Examples: Radio, convenience features

**17.2 ISO 26262 Development Process**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   V-Model for ISO 26262:
   
   Concept Phase:
   ──────────────
   • Hazard analysis (HARA)
   • Safety goals
   • ASIL determination
   
   System Level:
   ─────────────
   • Functional safety requirements
   • Safety architecture (redundancy, monitoring)
   
   Software Level:
   ───────────────
   • Software safety requirements
   • Model-based design
   • Code generation
   
   Verification:
   ─────────────
   • Model reviews
   • Coverage analysis
   • Back-to-back testing (MIL, SIL, PIL, HIL)

**17.3 ISO 26262 in Simulink**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: matlab

   % IEC Certification Kit (MathWorks):
   % Supports ISO 26262 (automotive) and IEC 61508 (industrial)
   
   % 1. Safety Mechanisms in Model:
   % ───────────────────────────────
   
   % Example: Redundant sensor processing (ASIL D)
   
   % Dual sensors with voting
   sensor1 = read_adc(1);
   sensor2 = read_adc(2);
   
   % Plausibility check
   if abs(sensor1 - sensor2) < tolerance
       % Agreement: use average
       sensor_value = (sensor1 + sensor2) / 2;
   else
       % Disagreement: fault detected
       trigger_safe_state();
       sensor_value = fallback_value;
   end
   
   % 2. FMEA (Failure Mode and Effects Analysis):
   % ─────────────────────────────────────────────
   % Document failure modes in model
   % Use Simulink Design Verifier for formal analysis
   
   % 3. Metrics and Coverage:
   % ────────────────────────
   % ASIL D requirements:
   %   • Statement coverage: 100%
   %   • Branch coverage: 100%
   %   • MC/DC coverage: Recommended
   
   set_param('ASIL_D_Model', 'CovMetricSettings', 'abcdw');
   
   % 4. Code Generation Configuration:
   % ─────────────────────────────────
   % Code Generation → Interface → Support: floating-point numbers
   % Set to 'off' for ASIL D (use fixed-point for determinism)
   
   % Enable overflow saturation
   set_param('ASIL_D_Model', 'SaturateOnIntegerOverflow', 'on');
   
   % 5. Static Analysis:
   % ───────────────────
   % Polyspace Code Prover (formal verification)
   % Proves absence of:
   %   • Division by zero
   %   • Array out-of-bounds
   %   • Overflow
   %   • Uninitialized variables

**17.4 Example: ASIL D Motor Controller**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Electric Power Steering (EPS) Controller - ASIL D:
   
   Safety Goals:
   ─────────────
   SG-001: Unintended steering assist shall not occur
   SG-002: Loss of steering assist shall be detected within 20 ms
   
   Safety Mechanisms:
   ──────────────────
   • Dual motor current sensors (redundancy)
   • Plausibility checks (sensor range, rate of change)
   • Watchdog monitoring (software execution)
   • Safe state: Disable motor assist
   
   Model Architecture:
   ───────────────────
   ┌────────────────────────────────────────────────┐
   │  SensorProcessing                              │
   │  ├─ Sensor1 (ADC1)                             │
   │  ├─ Sensor2 (ADC2)                             │
   │  ├─ Plausibility Check                         │
   │  └─ Voting Logic                               │
   └───────────────┬────────────────────────────────┘
                   │
   ┌───────────────▼────────────────────────────────┐
   │  ControlAlgorithm (PID)                        │
   │  ├─ Current Control Loop (10 kHz)              │
   │  ├─ Torque Limiter                             │
   │  └─ Anti-windup                                │
   └───────────────┬────────────────────────────────┘
                   │
   ┌───────────────▼────────────────────────────────┐
   │  SafetyMonitor                                 │
   │  ├─ Range Check (-50A to +50A)                 │
   │  ├─ Rate Limiter (max 100 A/s)                 │
   │  ├─ Watchdog Trigger                           │
   │  └─ Fault Handler → Safe State                 │
   └────────────────────────────────────────────────┘
   
   Testing:
   ────────
   • MIL: Functional validation
   • SIL: Code correctness
   • PIL: Real-time performance on target (Infineon TC3xx ASIL D MCU)
   • HIL: Full system test with motor simulator
   • Fault injection: Sensor failures, software faults
   
   Verification Artifacts:
   ───────────────────────
   • Safety plan
   • FMEA report
   • Coverage reports (100% statement, branch, MC/DC)
   • Tool qualification (Embedded Coder)
   • Traceability matrix (safety requirements → tests)

═══════════════════════════════════════════════════════════════════════

🎯 **18. KEY TAKEAWAYS & INTERVIEW PREPARATION**
─────────────────────────────────────────────────────────────────────────

**18.1 Model-Based Development Benefits**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Why MBD?
   ────────
   ✅ Early validation (before hardware exists)
   ✅ Automatic code generation (eliminates hand-coding errors)
   ✅ Reusable components (model libraries)
   ✅ Faster development (simulation vs build-flash-test)
   ✅ Certification ready (DO-178C, ISO 26262 compliant)
   ✅ Documentation (model IS the specification)
   ✅ Multi-domain (controls, signal processing, state machines)

**18.2 Your MBD Experience (Resume Mapping)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Projects to Highlight:
   ──────────────────────
   
   1. Motor Control (Industrial Gateways):
      • MATLAB/Simulink: FOC (Field-Oriented Control) design
      • Embedded Coder: Generated C code for Kinetis K50
      • Control design: PID tuning, state-space control
      • Fixed-point: Converted floating-point to Q15 for Cortex-M4
   
   2. Automotive ECU Development:
      • AUTOSAR Classic: Software component design
      • Stateflow: State machine implementation (ignition control)
      • Code generation: AUTOSAR-compliant C code
      • Testing: MIL/SIL validation
   
   3. Avionics Fuel Controller (DO-178B Level A):
      • MATLAB/Simulink: Control algorithm design
      • Requirements traceability: DOORS integration
      • Coverage: 100% MC/DC for Level A certification
      • Verification: MIL, SIL, HIL testing
      • Tool qualification: Embedded Coder DO Qualification Kit
   
   4. ADAS Sensor Fusion:
      • Kalman filter design in Simulink
      • Sensor fusion (camera + radar)
      • PIL testing: Verified on Qualcomm SOC
      • ISO 26262: ASIL B development process

**18.3 Technical Interview Talking Points**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Question: "Explain your model-based development experience"
   
   Answer Framework:
   ─────────────────
   "I've used MATLAB/Simulink extensively for [motor control / ADAS / 
   avionics] applications. My typical workflow starts with requirements 
   capture in Simulink, where I design control algorithms using PID, 
   state-space, or Kalman filter blocks.
   
   For [specific project], I developed a [FOC motor controller / sensor 
   fusion algorithm] in Simulink. I validated the model through MIL 
   testing, then used Embedded Coder to generate production C code. 
   I performed SIL testing to verify code correctness, followed by PIL 
   testing on the target [Cortex-M4 / Qualcomm SOC] to validate real-time 
   performance.
   
   For certification, I worked on a DO-178B Level A project where I 
   achieved 100% MC/DC coverage using Simulink Coverage, and generated 
   traceability reports linking requirements to model to code."
   
   ---
   
   Question: "What's the difference between MIL, SIL, PIL, and HIL?"
   
   Answer:
   ───────
   "These are progressive testing stages in the V-model:
   
   • MIL (Model-in-Loop): Tests the Simulink model itself on desktop. 
     Validates algorithm correctness against requirements. Fast iteration.
   
   • SIL (Software-in-Loop): Tests generated C code compiled as executable 
     on desktop. Verifies code generation correctness - compares SIL output 
     vs MIL output. Detects code gen bugs or numerical differences.
   
   • PIL (Processor-in-Loop): Tests code running on actual target processor 
     (e.g., ARM Cortex-M4). Validates real-time performance, timing, memory 
     usage. Detects processor-specific issues.
   
   • HIL (Hardware-in-Loop): Tests complete ECU with real-time plant 
     simulation. Uses dSPACE or Speedgoat to simulate motor/vehicle. 
     Regression testing and fault injection.
   
   I've used all four levels on [project name] to ensure comprehensive 
   verification from algorithm to deployment."
   
   ---
   
   Question: "How did you handle fixed-point conversion?"
   
   Answer:
   ───────
   "For [Cortex-M4 motor controller], I needed to convert floating-point 
   PID controller to fixed-point to avoid FPU overhead and ensure 
   deterministic timing.
   
   I used Simulink Fixed-Point Tool to analyze dynamic range, then selected 
   Q15 format (16-bit signed, 15 fractional bits) for coefficients and Q7.8 
   for intermediate calculations. I verified bit-exact behavior using SIL 
   testing, comparing fixed-point output against floating-point baseline 
   with acceptable tolerance of 1e-4.
   
   For multiplication, I handled Q15 × Q15 = Q30, then shifted right by 15 
   to get Q15 result. I enabled saturation arithmetic to prevent overflow 
   in the generated code."
   
   ---
   
   Question: "Explain AUTOSAR code generation"
   
   Answer:
   ───────
   "I used AUTOSAR Blockset to design software components. For a speed 
   controller, I defined:
   
   • Require ports (inputs): Speed sensor, target setpoint
   • Provide ports (outputs): Motor control signal
   • Runnable: 10 ms periodic execution
   • Calibration parameters: PID gains (Kp, Ki, Kd)
   
   Code generation produced:
   1. C implementation (.c/.h files)
   2. ARXML component description
   3. A2L calibration file for XCP
   
   I imported the ARXML into Vector DaVinci Configurator, integrated with 
   RTE (Runtime Environment), and linked with BSW (Basic Software) stack. 
   The RTE generated communication layer using Rte_Read/Rte_Write APIs."

**18.4 Common Pitfalls and Solutions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Issue: Algebraic loops in model
   ───────────────────────────────
   Symptom: Cannot determine execution order
   Solution: Insert Unit Delay block to break feedback loop
   
   Issue: Sample time mismatch
   ───────────────────────────
   Symptom: Red/orange blocks indicating timing issues
   Solution: Use Rate Transition blocks between different rates
   
   Issue: Excessive code size
   ──────────────────────────
   Symptom: Generated code too large for target
   Solution: Enable optimizations (loop unrolling, function inlining),
             use ROM-efficient data types, remove unused code
   
   Issue: SIL/PIL output mismatch
   ──────────────────────────────
   Symptom: Generated code doesn't match model
   Solution: Check solver settings (fixed-step required),
             verify data types (floating vs fixed-point),
             review optimization settings
   
   Issue: Stack overflow on target
   ───────────────────────────────
   Symptom: Code crashes during PIL/HIL testing
   Solution: Analyze stack usage (profiling report),
             reduce local variable size,
             move large arrays to global memory

═══════════════════════════════════════════════════════════════════════

**✅ MODEL-BASED DEVELOPMENT GUIDE COMPLETE**

**Total:** 1,900 lines across 3 parts

**Part 1 (700 lines):**
- MBD overview, V-Model workflow
- MATLAB fundamentals (matrices, signal processing, control flow)
- Simulink fundamentals (blocks, transfer functions, discrete systems)
- Control system design (PID, LQR, observers, Kalman filters)
- Subsystems and libraries
- Simulation configuration

**Part 2 (600 lines):**
- Stateflow state machines (hierarchical, parallel states)
- Embedded Coder code generation workflow
- Generated code structure and integration
- Fixed-point arithmetic (Q notation, operations)
- Code optimization and best practices
- AUTOSAR code generation

**Part 3 (600 lines):**
- MIL testing (model validation, coverage analysis)
- SIL testing (code verification, back-to-back)
- PIL testing (processor validation, profiling)
- HIL testing (real-time simulation, fault injection)
- AUTOSAR integration (Classic, Adaptive)
- DO-178C avionics certification
- ISO 26262 automotive safety
- Interview preparation and resume mapping

**Mapped to Your Experience:**
- MATLAB/Simulink: Control system design (FOC, PID, Kalman filter)
- Stateflow: State machine modeling
- Embedded Coder: Production code generation
- MIL/SIL testing: Model verification workflows
- AUTOSAR: ECU software development
- DO-178B: Avionics fuel controller (Level A)
- ISO 26262: Automotive ADAS projects

**Ready for Interview:**
Complete guide covers MBD from concept to certification, with emphasis 
on practical experience and industry standards.

═══════════════════════════════════════════════════════════════════════
