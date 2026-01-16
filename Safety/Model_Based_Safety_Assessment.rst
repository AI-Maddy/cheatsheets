📐 **Model-Based Safety Assessment — Automated Hazard Analysis from System Models**
═══════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for MBSA in Aerospace, Automotive, and Industrial Systems**  
**Languages:** AADL 🏗️ | SysML 📊 | SCADE 🔄 | Simulink/Stateflow 🎮  
**Tools:** OSATE | medini analyze | COMPASS | xSAP | SCADE Safety Architect  
**Standards:** SAE ARP4761 | ISO 26262-3 | EN 50129 | DO-178C (Model-Based Development)

═══════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What is Model-Based Safety Assessment (MBSA)?**

.. code-block:: text

   Traditional Safety Assessment (Manual):
   ❌ Engineer draws system architecture in Visio/PowerPoint
   ❌ Manually creates FMEA spreadsheet (error-prone, inconsistent)
   ❌ Manually traces failures through system (time-consuming)
   ❌ System changes → Manual updates to all documents (versioning nightmare)
   
   Model-Based Safety Assessment (Automated):
   ✅ System architecture modeled in formal language (AADL, SysML)
   ✅ Failure modes annotated in model (Error Model Annex)
   ✅ Automated FMEA generation (tool analyzes fault propagation)
   ✅ System changes → Automatic update to safety artifacts (single source of truth)

**Key Benefits:**

.. code-block:: text

   Benefit                          Impact
   ══════════════════════════════════════════════════════════════
   Consistency                      No discrepancy between architecture and FMEA
   Completeness                     Tool finds all fault propagation paths
   Traceability                     Requirements ↔ Model ↔ FMEA ↔ Tests
   Early detection                  Find safety issues before hardware exists
   Reduced cost                     70% less time on safety analysis (industry data)
   Support certification            Machine-readable evidence for DO-178C, ISO 26262

**AADL Error Model Annex Example:**

.. code-block:: aadl

   -- System: Dual-channel flight control computer
   system FlightControlComputer
   features
     sensor_input: in data port SensorData;
     actuator_cmd: out data port ActuatorCommand;
   annex EMV2 {**
     use types ErrorLibrary;
     
     error propagations
       sensor_input: in propagation {NoValue, BadValue};
       actuator_cmd: out propagation {NoValue, BadValue};
     end propagations;
     
     component error behavior
     transitions
       Operational -[sensor_input{NoValue}]-> Failed;
       Operational -[sensor_input{BadValue}]-> Degraded;
     end component;
   **};
   end FlightControlComputer;

**Output:** Automated fault tree showing how sensor failures lead to system failure.

**Comparison Table:**

+-------------------------+----------------------+-------------------------+
| Aspect                  | Manual (Traditional) | Model-Based (MBSA)      |
+=========================+======================+=========================+
| FMEA creation time      | 2-4 weeks            | 2-4 hours (automated)   |
+-------------------------+----------------------+-------------------------+
| Fault propagation       | Manual trace         | Automated (tool)        |
+-------------------------+----------------------+-------------------------+
| Consistency             | Error-prone          | Guaranteed (single      |
|                         |                      | source)                 |
+-------------------------+----------------------+-------------------------+
| System changes          | Manual updates       | Automatic regeneration  |
+-------------------------+----------------------+-------------------------+
| Certification evidence  | Document-based       | Model-based (traceable) |
+-------------------------+----------------------+-------------------------+

═══════════════════════════════════════════════════════════════════════════════

📖 **1. SYSTEM MODELING LANGUAGES**
═══════════════════════════════════════════════════════════════════════════════

1.1 AADL (Architecture Analysis & Design Language)
---------------------------------------------------

**Purpose:** Model embedded real-time systems (aerospace, automotive, defense)

**Core Concepts:**

.. code-block:: text

   Components:
   - System: Composite component (contains subcomponents)
   - Process: Software execution environment (address space)
   - Thread: Concurrent execution unit (task)
   - Device: Hardware sensor/actuator
   - Processor: Execution platform (CPU)
   - Bus: Communication medium (CAN, ARINC 429)
   - Memory: Storage
   
   Connections:
   - Port connections: Data flow between components
   - Feature group connections: Bundled interfaces

**Example: Simple Flight Control System**

.. code-block:: aadl

   system FlightControlSystem
   end FlightControlSystem;
   
   system implementation FlightControlSystem.basic
   subcomponents
     -- Hardware
     cpu: processor PowerPC;
     can_bus: bus CAN;
     
     -- Sensors
     airspeed_sensor: device AirspeedSensor;
     altitude_sensor: device AltitudeSensor;
     
     -- Software
     fcs_process: process FlightControlProcess;
     
     -- Actuators
     elevator_actuator: device ElevatorActuator;
   
   connections
     -- Sensor → Software
     c1: port airspeed_sensor.data_out -> fcs_process.airspeed_in;
     c2: port altitude_sensor.data_out -> fcs_process.altitude_in;
     
     -- Software → Actuator
     c3: port fcs_process.elevator_cmd -> elevator_actuator.cmd_in;
   
   properties
     -- Deployment
     Actual_Processor_Binding => (reference (cpu)) applies to fcs_process;
     Actual_Connection_Binding => (reference (can_bus)) applies to c1, c2, c3;
   end FlightControlSystem.basic;

────────────────────────────────────────────────────────────────────────────

**1.2 Error Model Annex (EMV2)**
--------------------------------

**Purpose:** Annotate failure modes and propagation in AADL models

**Error Types:**

.. code-block:: aadl

   error types
     NoValue: type;         -- Sensor/actuator not providing data
     BadValue: type;        -- Incorrect value (out of range, corrupted)
     LateValue: type;       -- Data arrives too late (timing failure)
     EarlyValue: type;      -- Data arrives too early
     ServiceOmission: type; -- Component fails to provide service
     ServiceCommission: type; -- Component provides wrong service
   end types;

**Error Propagations:**

.. code-block:: aadl

   device AirspeedSensor
   features
     data_out: out data port Speed;
   annex EMV2 {**
     use types ErrorLibrary;
     
     error propagations
       data_out: out propagation {NoValue, BadValue};
     flows
       ef1: error source data_out{NoValue} when {SensorFailure};
       ef2: error source data_out{BadValue} when {SensorDrift};
     end propagations;
   **};
   end AirspeedSensor;

**Fault Propagation:**

.. code-block:: aadl

   process FlightControlProcess
   features
     airspeed_in: in data port Speed;
     elevator_cmd: out data port ElevatorCommand;
   annex EMV2 {**
     use types ErrorLibrary;
     
     error propagations
       airspeed_in: in propagation {NoValue, BadValue};
       elevator_cmd: out propagation {NoValue, BadValue};
     flows
       -- If input bad, output bad (error propagation)
       ef1: error path airspeed_in{BadValue} -> elevator_cmd{BadValue};
       
       -- Internal failure also causes bad output
       ef2: error source elevator_cmd{BadValue} when {SoftwareBug};
     end propagations;
   **};
   end FlightControlProcess;

**Result:** Tool (OSATE) automatically generates fault tree showing all paths from sensor failure to actuator failure.

────────────────────────────────────────────────────────────────────────────

**1.3 SysML (Systems Modeling Language)**
-----------------------------------------

**Purpose:** General-purpose system engineering (broader than AADL, used in many domains)

**Safety-Relevant Diagrams:**

.. code-block:: text

   1. Block Definition Diagram (BDD):
      - System structure (components, interfaces)
   
   2. Internal Block Diagram (IBD):
      - Component connections, data flow
   
   3. State Machine Diagram:
      - Component behavior (states, transitions)
   
   4. Sequence Diagram:
      - Interaction between components (scenarios)
   
   5. Requirement Diagram:
      - Safety requirements (traceability to design)

**SysML for Safety (Example: Brake System):**

.. code-block:: text

   Block Definition Diagram:
   
   «block» BrakeSystem
   ├── «block» BrakePedal
   ├── «block» BrakeECU
   │   ├── «property» ASIL: ASIL_D
   │   └── «constraint» redundancy: 1oo2
   ├── «block» HydraulicActuator
   └── «block» WheelSpeedSensor (quantity: 4)
   
   Requirements:
   «requirement» SafetyReq_001
   text: "Brake system shall achieve emergency stop within 3 seconds"
   satisfiedBy: BrakeSystem
   
   «requirement» SafetyReq_002
   text: "Single point failure shall not prevent braking"
   satisfiedBy: BrakeECU.redundancy

**Tools:** medini analyze, Cameo Safety and Reliability Analyzer

═══════════════════════════════════════════════════════════════════════════════

📖 **2. AUTOMATED FMEA GENERATION**
═══════════════════════════════════════════════════════════════════════════════

2.1 Process Overview
--------------------

**Steps:**

.. code-block:: text

   1. Model System Architecture (AADL, SysML)
      - Define components (sensors, processors, actuators)
      - Define connections (data flow, control flow)
   
   2. Annotate Error Model
      - Assign failure modes to each component
      - Define error propagations (how failures spread)
      - Specify failure rates (λ, MTBF)
   
   3. Run MBSA Tool
      - Tool analyzes all fault propagation paths
      - Generates FMEA table automatically
      - Generates fault trees for top-level hazards
   
   4. Review & Refine
      - Engineer reviews generated FMEA
      - Adds mitigations (redundancy, diagnostics)
      - Re-run tool to verify effectiveness

────────────────────────────────────────────────────────────────────────────

**2.2 Example: Automated FMEA for Dual-Channel System**
-------------------------------------------------------

**AADL Model:**

.. code-block:: aadl

   system DualChannelController
   end DualChannelController;
   
   system implementation DualChannelController.impl
   subcomponents
     channel_A: system ControlChannel;
     channel_B: system ControlChannel;
     voter: system Voter;
     actuator: device Actuator;
   
   connections
     c1: port channel_A.output -> voter.input_A;
     c2: port channel_B.output -> voter.input_B;
     c3: port voter.output -> actuator.command;
   
   annex EMV2 {**
     use types ErrorLibrary;
     
     error propagations
       -- No external error sources (top-level system)
     flows
       -- End-to-end error path
       ef1: error path channel_A.output{NoValue} -> actuator.command{NoValue};
     end propagations;
     
     composite error behavior
     states
       [channel_A.Failed and channel_B.Failed]-> Failed;
       [channel_A.Failed and not channel_B.Failed]-> Operational;
       [not channel_A.Failed and channel_B.Failed]-> Operational;
       [not channel_A.Failed and not channel_B.Failed]-> Operational;
     end composite;
   **};
   end DualChannelController.impl;

**Generated FMEA (by OSATE tool):**

+----------------+------------------+------------------+------------------+
| Component      | Failure Mode     | Local Effect     | System Effect    |
+================+==================+==================+==================+
| channel_A      | NoValue          | Voter receives   | System           |
|                |                  | only 1 input     | operational      |
|                |                  |                  | (channel_B OK)   |
+----------------+------------------+------------------+------------------+
| channel_B      | NoValue          | Voter receives   | System           |
|                |                  | only 1 input     | operational      |
|                |                  |                  | (channel_A OK)   |
+----------------+------------------+------------------+------------------+
| channel_A AND  | Both NoValue     | Voter has no     | **System         |
| channel_B      |                  | valid inputs     | Failed**         |
+----------------+------------------+------------------+------------------+
| voter          | NoValue          | Actuator gets no | System Failed    |
|                |                  | command          |                  |
+----------------+------------------+------------------+------------------+
| actuator       | Stuck            | No actuation     | System Failed    |
+----------------+------------------+------------------+------------------+

**Automatically Generated Fault Tree:**

.. code-block:: text

                  System Failed
                       |
         ┌─────────────┼─────────────┐
         │             │             │
   Both Channels  Voter Failed  Actuator Failed
      Failed
         |
    ┌────┴────┐
    │         │
Channel_A  Channel_B
 Failed     Failed

────────────────────────────────────────────────────────────────────────────

**2.3 Failure Probability Calculation**
---------------------------------------

**Annotated Failure Rates in AADL:**

.. code-block:: aadl

   system ControlChannel
   annex EMV2 {**
     use types ErrorLibrary;
     use behavior ErrorLibrary::FailStop;
     
     properties
       -- Failure rate: 100 FIT (failures in 10^9 hours)
       EMV2::OccurrenceDistribution => [
         ProbabilityValue => 1.0e-7;  -- λ = 100 FIT = 100e-9 /hr
         Distribution => Poisson;
       ] applies to Failed;
   **};
   end ControlChannel;

**Tool Calculation (Dual-channel 1oo2):**

.. code-block:: text

   Given:
   - Channel A: λ_A = 100 FIT
   - Channel B: λ_B = 100 FIT (identical)
   - Voter: λ_V = 50 FIT
   - Actuator: λ_Act = 200 FIT
   
   System Failure Scenarios:
   1. Both channels fail: P = (λ_A × λ_B) / μ²  (repair rate μ)
   2. Voter fails: P = λ_V
   3. Actuator fails: P = λ_Act
   
   Tool Output:
   Total system failure rate: 250 FIT
   (Dominated by actuator, redundant channels contribute minimally)

═══════════════════════════════════════════════════════════════════════════════

📖 **3. FAULT PROPAGATION ANALYSIS**
═══════════════════════════════════════════════════════════════════════════════

3.1 Forward Propagation (Bottom-Up)
------------------------------------

**Question:** "If sensor X fails, what system-level effects occur?"

**AADL Analysis:**

.. code-block:: text

   Starting Point: AirspeedSensor fails (NoValue)
   
   Tool Traces Propagation:
   1. AirspeedSensor.data_out{NoValue}
      ↓
   2. FlightControlProcess.airspeed_in{NoValue}
      ↓ (error propagation rule)
   3. FlightControlProcess.elevator_cmd{BadValue}
      ↓
   4. ElevatorActuator.cmd_in{BadValue}
      ↓
   5. Aircraft: **Loss of pitch control**
   
   Result: Hazard identified (single sensor failure → loss of control)
   Mitigation Required: Redundant airspeed sensors (triple modular redundancy)

────────────────────────────────────────────────────────────────────────────

**3.2 Backward Propagation (Top-Down)**
---------------------------------------

**Question:** "What failures can cause hazard Y?"

**Example: "Uncommanded Engine Shutdown"**

.. code-block:: text

   Tool Performs Backward Trace:
   
   Hazard: Engine shuts down unexpectedly
   
   Possible Causes (automatically identified):
   1. Fuel sensor failure (BadValue: incorrectly reports empty tank)
   2. Engine controller software bug (ServiceCommission)
   3. Pilot command misinterpreted (communication error)
   4. Cyber attack (malicious shutdown command)
   
   Result: Comprehensive fault tree with ALL contributors

────────────────────────────────────────────────────────────────────────────

**3.3 Common Cause Analysis**
-----------------------------

**Challenge:** Identify shared components that affect multiple redundant channels

**AADL Model:**

.. code-block:: aadl

   system TripleModularRedundant
   subcomponents
     channel_1: system Channel;
     channel_2: system Channel;
     channel_3: system Channel;
     shared_power_supply: device PowerSupply;  -- COMMON CAUSE
     voter: system Voter;
   
   annex EMV2 {**
     composite error behavior
     states
       -- All three channels fail if shared power fails
       [shared_power_supply.Failed]-> Failed;
       
       -- Otherwise, 2oo3 voting protects against single channel failure
       [channel_1.Failed and channel_2.Failed]-> Failed;
       [channel_1.Failed and channel_3.Failed]-> Failed;
       [channel_2.Failed and channel_3.Failed]-> Failed;
     end composite;
   **};
   end TripleModularRedundant;

**Tool Output:**

.. code-block:: text

   ⚠️ WARNING: Common cause failure identified
   
   Component: shared_power_supply
   Impact: ALL redundant channels
   Recommendation: Provide redundant power supplies (diverse sources)

═══════════════════════════════════════════════════════════════════════════════

📖 **4. TOOL ECOSYSTEM**
═══════════════════════════════════════════════════════════════════════════════

4.1 OSATE (Open Source AADL Tool Environment)
----------------------------------------------

**Features:**

.. code-block:: text

   ✅ AADL modeling (graphical + textual)
   ✅ Error Model Annex (EMV2) support
   ✅ Automated fault tree generation
   ✅ Minimal cut sets (MCS) computation
   ✅ Fault impact analysis (forward/backward propagation)
   ✅ Common cause failure detection

**Workflow:**

.. code-block:: bash

   # 1. Create AADL model (Eclipse-based IDE)
   # 2. Annotate with EMV2 error model
   # 3. Run safety analysis plugin
   
   # Example: Generate fault tree
   $ osate-cli --project FlightControl \
               --analysis FaultTree \
               --output fault_tree.xml
   
   # Output: Fault tree in XML format (import to safety tools)

────────────────────────────────────────────────────────────────────────────

**4.2 medini analyze (SysML-based MBSA)**
-----------------------------------------

**Vendor:** Ansys (formerly ReqtifyMBSE)

**Features:**

.. code-block:: text

   ✅ SysML modeling
   ✅ Automated FMEA generation
   ✅ Fault tree analysis (FTA)
   ✅ Reliability block diagrams (RBD)
   ✅ Markov chain analysis
   ✅ ISO 26262 compliance reports

**Example Analysis:**

.. code-block:: text

   Input: SysML model of automotive braking system
   
   Tool Actions:
   1. Extract component structure
   2. Apply failure modes from library (stuck, drift, intermittent)
   3. Trace fault propagation through block diagram
   4. Generate FMEA table (Excel export)
   5. Generate fault trees for ASIL D hazards
   6. Calculate PMHF (Probabilistic Metric for HW Failures)
   
   Output: ISO 26262 Part 5 compliant safety analysis report

────────────────────────────────────────────────────────────────────────────

**4.3 SCADE Safety Architect**
------------------------------

**Vendor:** Ansys (DO-178C qualified)

**Focus:** Avionics, railway (formal methods + MBSA)

.. code-block:: text

   Integration with SCADE Suite:
   - SCADE Suite: Model-based development (Simulink-like, but formal)
   - SCADE Safety Architect: FMEA, FTA, common cause analysis
   
   Key Feature: Qualification data for DO-178C/DO-254
   - Tool qualification per DO-330 (software tool qualification)
   - Enables model-based development for DAL A/B

**Example:**

.. code-block:: text

   1. Design flight control logic in SCADE (state machines, data flow)
   2. Annotate failure modes in Safety Architect
   3. Tool generates fault trees automatically
   4. Export to certification report (DO-178C compliance)
   5. Automatic code generation (C code from verified model)

═══════════════════════════════════════════════════════════════════════════════

📖 **5. ADVANCED TECHNIQUES**
═══════════════════════════════════════════════════════════════════════════════

5.1 Assume-Guarantee Contracts
-------------------------------

**Concept:** Component behavior specified as contract (preconditions → postconditions)

**Example: Sensor Contract**

.. code-block:: text

   Component: AirspeedSensor
   
   Assumptions (what sensor requires to work correctly):
   - Power supply: 28V ± 2V
   - Temperature: -40°C to +85°C
   - Pitot tube: Not iced over
   
   Guarantees (what sensor promises if assumptions hold):
   - Output: Valid airspeed ± 2 knots
   - Update rate: 10 Hz
   - Latency: < 10 ms
   
   Failure Mode (if assumptions violated):
   - Low voltage → NoValue
   - Temperature out of range → BadValue
   - Iced pitot tube → BadValue (erroneously low airspeed)

**AADL Contract Annex:**

.. code-block:: aadl

   device AirspeedSensor
   annex contract {**
     assume:
       voltage >= 26.0 and voltage <= 30.0;
       temperature >= -40.0 and temperature <= 85.0;
     guarantee:
       data_out.accuracy <= 2.0;  -- knots
       data_out.rate == 10;        -- Hz
   **};
   end AirspeedSensor;

**Benefit:** Compositional reasoning (verify components independently, compose guarantees)

────────────────────────────────────────────────────────────────────────────

**5.2 Probabilistic Model Checking**
------------------------------------

**Tool:** PRISM (Probabilistic Model Checker)

**Purpose:** Verify quantitative properties (e.g., "Probability of failure < 10^-9 /hour")

**Example: Redundant System**

.. code-block:: prism

   // PRISM model: Dual-channel system with repair
   ctmc
   
   const double lambda = 1.0e-4;  // Failure rate (per hour)
   const double mu = 0.1;          // Repair rate (per hour)
   
   module dual_channel
     s : [0..2] init 0;  // State: 0=both OK, 1=one failed, 2=both failed
     
     // Transitions
     [] s=0 -> 2*lambda : (s'=1);          // One channel fails
     [] s=1 -> lambda   : (s'=2);          // Second channel fails
     [] s=1 -> mu       : (s'=0);          // Repair completes
   endmodule
   
   // Property to verify
   // "Probability of system failure (state 2) within 1000 hours"
   P=? [ F<=1000 s=2 ]

**Tool Output:**

.. code-block:: text

   Result: P = 4.9876e-10
   
   Interpretation: Probability of both channels failing within 1000 hours
                   is approximately 5×10^-10 (meets 10^-9 /hour requirement)

────────────────────────────────────────────────────────────────────────────

**5.3 Dynamic Fault Trees (DFT)**
---------------------------------

**Limitation of Static FT:** Cannot model spare parts, sequence dependencies

**DFT Gates:**

.. code-block:: text

   SPARE Gate:
   - Primary component runs
   - If primary fails, spare activates
   - System fails only if both fail
   
   Example: Dual-redundant actuator with cold spare
   
             Actuator System Failed
                      |
                  SPARE Gate
                   /     \
            Primary      Spare
            Actuator     Actuator

**FDEP (Functional Dependency) Gate:**

.. code-block:: text

   Power supply failure disables multiple components
   
             System Failed
                  |
              AND Gate
               /    \
          Comp_A   Comp_B
            |        |
         FDEP     FDEP
            \      /
          Power Supply

**Tool Support:** Galileo, DFTCalc (convert DFT to static FT for analysis)

═══════════════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
═══════════════════════════════════════════════════════════════════════════════

**Q1:** What are the key benefits of Model-Based Safety Assessment compared to traditional manual FMEA?

**A1:**

**Benefits:**

.. code-block:: text

   1. Consistency:
      - Manual: Architecture document ≠ FMEA spreadsheet (versioning issues)
      - MBSA: Single source of truth (model), FMEA auto-generated
   
   2. Completeness:
      - Manual: Engineer might miss failure propagation paths
      - MBSA: Tool exhaustively analyzes ALL paths
   
   3. Efficiency:
      - Manual: 2-4 weeks to create FMEA for complex system
      - MBSA: 2-4 hours (tool automates analysis)
   
   4. Traceability:
      - Manual: Difficult to trace FMEA to requirements/design
      - MBSA: Automatic traceability (requirements → model → FMEA)
   
   5. Change Management:
      - Manual: System changes require manual updates to all documents
      - MBSA: Change model → Re-run tool → Updated FMEA automatically
   
   6. Early Detection:
      - Manual: Safety analysis after design complete (expensive to fix)
      - MBSA: Analyze models before hardware exists (catch issues early)

**Industry Data:** 70% reduction in safety analysis time with MBSA tools.

────────────────────────────────────────────────────────────────────────────

**Q2:** Explain AADL Error Model Annex (EMV2) and how it enables automated fault propagation analysis.

**A2:**

**EMV2 Concepts:**

.. code-block:: text

   1. Error Types:
      - Define categories of failures (NoValue, BadValue, LateValue)
   
   2. Error Propagations:
      - Specify how errors enter/exit components via ports
   
   3. Error Flows:
      - error source: Component generates error internally
      - error sink: Component absorbs error (doesn't propagate)
      - error path: Input error causes output error
   
   4. Component Error Behavior:
      - State machine (Operational, Degraded, Failed)
      - Transitions triggered by error events

**Example:**

.. code-block:: aadl

   process Controller
   features
     sensor_in: in data port;
     actuator_out: out data port;
   annex EMV2 {**
     error propagations
       sensor_in: in propagation {NoValue};
       actuator_out: out propagation {NoValue};
     flows
       ef1: error path sensor_in{NoValue} -> actuator_out{NoValue};
     end propagations;
   **};

**Automated Analysis:**

.. code-block:: text

   Tool (OSATE) performs:
   1. Start at sensor failure (error source)
   2. Follow error paths through components
   3. Trace to system-level effect (actuator failure)
   4. Generate fault tree automatically
   
   Result: Complete fault propagation without manual effort

────────────────────────────────────────────────────────────────────────────

**Q3:** What is the difference between forward and backward fault propagation analysis?

**A3:**

**Forward Propagation (Bottom-Up):**

.. code-block:: text

   Question: "If component X fails, what are the system-level consequences?"
   
   Process:
   1. Start: Component failure (e.g., sensor fails)
   2. Trace: Follow error propagation paths FORWARD
   3. End: System-level hazards
   
   Example:
   Wheel speed sensor fails (NoValue)
   → ABS controller receives no data
   → ABS cannot activate
   → Hazard: Increased stopping distance
   
   Use Case: FMEA (identify effects of each failure mode)

**Backward Propagation (Top-Down):**

.. code-block:: text

   Question: "What failures can cause hazard Y?"
   
   Process:
   1. Start: System-level hazard (e.g., loss of braking)
   2. Trace: Follow error paths BACKWARD
   3. End: All possible root causes
   
   Example:
   Hazard: Loss of braking
   → Causes identified by tool:
      - Brake pedal sensor failure
      - Hydraulic pump failure
      - ECU software bug
      - Power supply failure
      - Cyber attack (spoofed CAN message)
   
   Use Case: Fault Tree Analysis (FTA), hazard analysis

**Tool Capability:** MBSA tools perform both directions automatically.

────────────────────────────────────────────────────────────────────────────

**Q4:** How do assume-guarantee contracts enable compositional safety analysis?

**A4:**

**Concept:**

.. code-block:: text

   Component Contract:
   - Assumptions: What component requires from environment
   - Guarantees: What component promises (if assumptions hold)

**Compositional Reasoning:**

.. code-block:: text

   System = Component_A + Component_B + Component_C
   
   Traditional Analysis:
   - Must analyze entire system as monolith (state explosion)
   
   Compositional Analysis:
   1. Verify each component independently (component meets guarantee?)
   2. Check composition (A's guarantees satisfy B's assumptions?)
   3. Compose guarantees to system level
   
   Benefit: Analyze complex system by breaking into manageable pieces

**Example:**

.. code-block:: text

   Component_A (Sensor):
   Assume: Power = 5V ± 0.5V
   Guarantee: Output accuracy ± 2%
   
   Component_B (Controller):
   Assume: Sensor accuracy ± 5%  (✅ A's guarantee satisfies B's assumption)
   Guarantee: Control error ± 10%
   
   System:
   Assume: Power = 5V ± 0.5V
   Guarantee: Control error ± 10%  (composed from components)

**Tool Support:** AGREE (Assume Guarantee REasoning Environment) plugin for AADL.

────────────────────────────────────────────────────────────────────────────

**Q5:** What are Dynamic Fault Trees (DFT) and when are they needed over static fault trees?

**A5:**

**Static Fault Trees (Traditional):**

.. code-block:: text

   Limitations:
   ❌ No spare parts (cannot model cold/hot spare)
   ❌ No sequence dependencies (order of failures matters)
   ❌ No functional dependencies (cascading failures)
   
   Gates: AND, OR, k-out-of-n (static logic)

**Dynamic Fault Trees (DFT):**

.. code-block:: text

   Additional Gates:
   
   1. SPARE Gate:
      - Model spare parts (cold spare, hot spare, warm spare)
      - Example: Redundant power supply with spare activated on failure
   
   2. FDEP (Functional Dependency):
      - Trigger event causes multiple components to fail
      - Example: Power supply failure disables sensor + controller
   
   3. PAND (Priority AND):
      - Failures must occur in specific order
      - Example: Leak occurs, THEN ignition → Explosion
   
   4. SEQ (Sequence Enforcing):
      - Enforce temporal ordering of events

**When Needed:**

.. code-block:: text

   ✅ Standby redundancy (aircraft hydraulic systems with spare pumps)
   ✅ Phased missions (satellite: launch phase, orbit phase, reentry)
   ✅ Cascading failures (power loss disables multiple subsystems)
   ✅ Maintenance modeling (repair affects availability)

**Tool Conversion:**

.. code-block:: text

   DFT tools (Galileo, DFTCalc) convert DFT → Markov chain or static FT
   Then analyze using standard techniques (minimal cut sets, MTTF)

═══════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Fundamentals:**
- [ ] Understand MBSA = Single model → Automated FMEA/FTA
- [ ] Benefits: Consistency, completeness, traceability, efficiency
- [ ] 70% time reduction vs manual safety analysis

**Languages:**
- [ ] AADL for embedded systems (components, connections, deployment)
- [ ] Error Model Annex (EMV2) for fault propagation
- [ ] SysML for general systems (block diagrams, state machines)

**Analysis:**
- [ ] Forward propagation (component failure → system hazard)
- [ ] Backward propagation (hazard → root causes)
- [ ] Common cause failure detection (shared components)

**Tools:**
- [ ] OSATE (open source, AADL + EMV2)
- [ ] medini analyze (SysML, ISO 26262 compliance)
- [ ] SCADE Safety Architect (avionics, DO-178C qualified)

**Advanced:**
- [ ] Assume-guarantee contracts (compositional reasoning)
- [ ] Probabilistic model checking (PRISM)
- [ ] Dynamic fault trees (SPARE, FDEP gates)

═══════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
═══════════════════════════════════════════════════════════════════════════════

1️⃣ **Single source of truth** — Model-based approach eliminates inconsistency between architecture, FMEA, and FTA (all generated from same model)

2️⃣ **Automation = completeness** — Tools exhaustively analyze ALL fault propagation paths (humans miss edge cases in manual analysis)

3️⃣ **Early safety analysis** — Evaluate safety before hardware exists, catch design flaws when cheap to fix (not after production)

4️⃣ **AADL + EMV2 is aerospace standard** — Used in Airbus, Boeing, NASA projects for safety-critical systems (avionics, flight control)

5️⃣ **Traceability for certification** — Requirements ↔ Model ↔ FMEA ↔ Tests automatically linked (DO-178C, ISO 26262 compliance)

6️⃣ **Compositional analysis scales** — Assume-guarantee contracts enable analysis of complex systems by verifying components independently

7️⃣ **Dynamic fault trees handle realistic scenarios** — Spare parts, sequence dependencies, phased missions (beyond static FT capabilities)

═══════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **MODEL-BASED SAFETY ASSESSMENT CHEATSHEET COMPLETE**

**Created:** January 16, 2026  
**Coverage:** AADL and Error Model Annex (EMV2), SysML for safety, automated FMEA generation, fault propagation analysis (forward/backward), tool ecosystem (OSATE, medini analyze, SCADE), assume-guarantee contracts, probabilistic model checking, dynamic fault trees

═══════════════════════════════════════════════════════════════════════════════
