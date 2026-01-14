🏥 **IEC 62304: Medical Device Software — Software Lifecycle Processes**
═══════════════════════════════════════════════════════════════════════════

**Your Complete Reference for Medical Device Software Development**  
**Standard:** IEC 62304:2006 + AMD1:2015  
**Domains:** Medical Devices 🏥 | In-Vitro Diagnostics 🔬 | Healthcare IT 💊  
**Purpose:** Software lifecycle compliance, regulatory approval (FDA, MDR, TGA)

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What is IEC 62304?**
International standard defining lifecycle requirements for medical device software

**Key Concepts:**

```
Software Safety Class → Development Activities → Risk Management → Validation
        ↓                       ↓                       ↓               ↓
    Class A/B/C           Planning & Design         ISO 14971      Clinical Use
```

**Software Safety Classes:**

| Class | Risk Level | Injury Possible | Rigor | Examples |
|:-----:|:-----------|:----------------|:------|:---------|
| **C** | Serious injury/death | Yes | ★★★★★ Highest | Insulin pump, ventilator |
| **B** | Non-serious injury | Yes | ★★★ Moderate | Blood pressure monitor |
| **A** | No injury | No | ★ Basic | Patient data viewer |

**Core Processes:**

✅ **Software Development** → Requirements → Design → Implementation → Testing  
✅ **Risk Management** → Hazard analysis → Risk control → Residual risk evaluation (ISO 14971)  
✅ **Configuration Management** → Version control, baselines, change control  
✅ **Problem Resolution** → Bug tracking, root cause analysis, corrective actions

════════════════════════════════════════════════════════════════════════════

📖 **INTRODUCTION**
───────────────────

IEC 62304 Background
~~~~~~~~~~~~~~~~~~~~

**Full Title:**  
*Medical device software — Software life cycle processes*

**Published by:**
- **IEC** (International Electrotechnical Commission)
- **ANSI/AAMI** (US harmonized standard: ANSI/AAMI/IEC 62304:2006)

**Current Version:**  
IEC 62304:2006 + Amendment 1:2015 (AMD1)

**Scope:**
- **Software as a Medical Device (SaMD):** Standalone diagnostic/therapeutic apps
- **Software in a Medical Device (SiMD):** Embedded firmware (pacemakers, infusion pumps)
- **Accessory software:** Lab info systems, picture archiving (PACS)

**Does NOT cover:**
- Pure clinical decision support (CDSS) without direct patient impact
- General-purpose IT systems (unless direct medical use)

**Why IEC 62304?**
Medical software failures kill:
- **Therac-25 (1985-1987):** Radiation overdoses, 6 deaths (software race condition)
- **Infusion pump errors:** Hundreds of deaths from incorrect dosing (FDA recalls)
- **Pacemaker vulnerabilities:** Cybersecurity flaws allowing remote attacks

**Relationship to Other Standards:**

```
ISO 13485 (Quality Management System)
      ↓
IEC 62304 (Software Lifecycle) ← You are here
      ↓                    ↓
ISO 14971 (Risk Mgmt)  IEC 62366 (Usability)
      ↓                    ↓
Clinical Evaluation → Regulatory Approval (FDA 510(k)/PMA, EU MDR)
```

════════════════════════════════════════════════════════════════════════════

🎯 **SOFTWARE SAFETY CLASSIFICATION**
─────────────────────────────────────

Safety Class Determination
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Classification based on potential harm:**

**Step 1: Identify Software Items**

A **software item** is:
- Any distinguishable part of software (module, function, library)
- Can be independently classified

**Step 2: Perform Risk Analysis (per ISO 14971)**

For each software item, ask:
```
IF this software item fails or malfunctions,
WHAT harm could result to the patient or operator?
```

**Step 3: Assign Safety Class**

| Safety Class | Hazard Severity | Probability of Harm | Examples |
|:-------------|:----------------|:--------------------|:---------|
| **Class C** | Death or serious injury possible | Any probability | Ventilator control, insulin delivery, defibrillator |
| **Class B** | Non-serious injury possible | Any probability | Blood glucose meter, thermometer firmware |
| **Class A** | No injury possible | N/A | Patient education app, appointment scheduler |

**Important:**
- **Single failure analysis:** One software item failure → Class C if could cause death
- **Hazard mitigation:** Risk controls (hardware interlocks) may lower class
- **SOUP influence:** Off-the-shelf components (SOUP) inherit class of using system

Safety Class Examples
~~~~~~~~~~~~~~~~~~~~~~

**Class C Examples:**

1. **Insulin Pump Dosing Algorithm**
   - Failure: Delivers 100× dose → hypoglycemia → death
   - Classification: **Class C**

2. **Ventilator Breath Control**
   - Failure: Stops ventilation → asphyxiation → death
   - Classification: **Class C**

3. **Pacemaker Pacing Logic**
   - Failure: No pacing during cardiac arrest → death
   - Classification: **Class C**

**Class B Examples:**

1. **Blood Pressure Monitor Display**
   - Failure: Shows incorrect BP → misdiagnosis → delayed treatment → minor harm
   - Classification: **Class B**

2. **Pulse Oximeter Alarm**
   - Failure: False alarm → clinician disables alarms → potential harm
   - Classification: **Class B**

3. **ECG Signal Filtering**
   - Failure: Artifact not removed → misinterpretation → non-serious injury
   - Classification: **Class B**

**Class A Examples:**

1. **Patient Education App**
   - Failure: Displays outdated info → patient confused (no injury)
   - Classification: **Class A**

2. **Hospital Bed Occupancy Dashboard**
   - Failure: Wrong bed status → administrative inefficiency (no injury)
   - Classification: **Class A**

3. **Medical Equipment Maintenance Scheduler**
   - Failure: Missed reminder → no direct patient harm
   - Classification: **Class A** (Note: If maintenance critical, could be Class B)

Segregation Strategy
~~~~~~~~~~~~~~~~~~~~

**Principle:**  
Isolate high-risk functions from low-risk to simplify compliance

**Example: Medical Device with Mixed Classes**

```
┌────────────────────────────────────────────────┐
│           Medical Infusion Pump                │
├────────────────────────────────────────────────┤
│ Class C: Drug Calculation & Delivery Control  │ ← Full IEC 62304 Class C rigor
├────────────────────────────────────────────────┤
│ Class B: User Interface & Alarms              │ ← Moderate rigor
├────────────────────────────────────────────────┤
│ Class A: Usage Logging & Data Export          │ ← Minimal rigor
└────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ Reduce Class C scope → lower cost
- ✅ Simplify verification (focus on critical parts)
- ✅ Allow commercial libraries in Class A/B portions

**Requirements:**
- **Independence:** Failure in Class A cannot propagate to Class C
- **Freedom from interference:** Memory protection, separate processes
- **Documented rationale:** Justify segregation in risk analysis

════════════════════════════════════════════════════════════════════════════

🏗️ **SOFTWARE DEVELOPMENT PROCESS**
────────────────────────────────────

Development Activities (Clause 5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**IEC 62304 Section 5: Software Development Process**

Organized as V-Model:

```
        Left Side (Decomposition)       Right Side (Integration & Test)
              ↓                                  ↑
    ┌─────────────────┐                ┌─────────────────┐
    │  Requirements   │───────────────▶│ System Testing  │
    │   (5.2)         │                │    (5.7)        │
    └────────┬────────┘                └────────▲────────┘
             ↓                                  │
    ┌─────────────────┐                ┌─────────────────┐
    │  Architecture   │───────────────▶│  Integration    │
    │   (5.3)         │                │    Testing      │
    └────────┬────────┘                │    (5.6)        │
             ↓                          └────────▲────────┘
    ┌─────────────────┐                        │
    │ Detailed Design │──────────────────┐     │
    │   (5.4)         │                  │     │
    └────────┬────────┘                  │     │
             ↓                            │     │
    ┌─────────────────┐         ┌────────┴─────┴────┐
    │ Implementation  │────────▶│   Unit Testing    │
    │   (5.5)         │         │      (5.5)        │
    └─────────────────┘         └───────────────────┘
```

Section 5.1: Software Development Planning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required Outputs:**

**Software Development Plan (SDP)**

**Contents:**
- Development activities & deliverables
- Standards to be followed (coding, design, testing)
- Tools (compilers, IDEs, test frameworks)
- Development team roles & responsibilities
- Schedule & milestones

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Written SDP | ✅ | ✅ | ✅ |
| Identify development standards | ✅ | ✅ | ✅ |
| Plan integration & testing | ✅ | ✅ | ✅ |
| Plan for SOUP mgmt | ✅ | ✅ | ✅ |
| Plan risk management activities | — | ✅ | ✅ |
| Document segregation | — | — | ✅ (if applicable) |

**Example SDP Table of Contents:**

```
1. Introduction & Scope
2. Software Safety Classification (Class B)
3. Development Standards
   3.1 Coding Standard: MISRA C:2012
   3.2 Design Notation: UML 2.5
4. Development Activities
   4.1 Requirements Analysis
   4.2 Architecture Design
   4.3 Detailed Design
   4.4 Implementation
   4.5 Integration & Testing
   4.6 System Testing
5. Tools
   5.1 IDE: Eclipse + GCC 11.2
   5.2 Version Control: Git 2.40
   5.3 Test Framework: CppUTest
   5.4 Static Analysis: PC-Lint Plus
6. SOUP Management
   6.1 FreeRTOS 10.5 (real-time OS)
   6.2 OpenSSL 3.0 (encryption)
7. Risk Management Integration (ISO 14971)
8. Configuration Management (IEC 62304 §8)
9. Problem Resolution (IEC 62304 §9)
10. Team Roles & Responsibilities
```

Section 5.2: Software Requirements Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Define WHAT the software must do (not HOW)

**Required Outputs:**

**Software Requirements Specification (SRS)**

**Requirements must be:**
- **Complete:** All necessary functionality specified
- **Consistent:** No contradictions
- **Unambiguous:** Single interpretation only
- **Verifiable:** Can be tested/proven
- **Traceable:** Linked to system requirements & risks

**Requirement Categories:**

1. **Functional Requirements:**
   - Core features & behaviors
   - Example: "SW shall calculate insulin dose based on blood glucose & carbs"

2. **Performance Requirements:**
   - Timing, throughput, resource usage
   - Example: "SW shall update display within 100 ms of sensor read"

3. **Interface Requirements:**
   - User interface, hardware interfaces, network protocols
   - Example: "SW shall communicate with sensor via I2C at 400 kHz"

4. **Safety Requirements:**
   - Derived from risk analysis (ISO 14971)
   - Example: "SW shall limit max insulin delivery to 25 units/hour"

5. **Security Requirements:** (added in AMD1:2015)
   - Cybersecurity controls
   - Example: "SW shall encrypt patient data using AES-256"

**Example SRS Requirement (Class C Insulin Pump):**

```
REQ-SW-101: Maximum Dose Limit

Description:
  The software shall limit the total insulin delivery to a maximum of 
  25 units per hour, regardless of user input or sensor readings.

Rationale:
  Prevents fatal insulin overdose from sensor error or user mistake.

Safety Class: C

Traceability:
  System Requirement: SYS-REQ-020
  Hazard: HAZ-003 (Insulin overdose)
  Risk Control: RC-HAZ-003-01

Verification Method:
  Test Case: TC-SW-101 (inject fault, verify limit enforced)

Acceptance Criteria:
  Pass if software enforces 25 unit/hour limit under all test scenarios.
```

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Document requirements | ✅ | ✅ | ✅ |
| Ensure requirements consistency | ✅ | ✅ | ✅ |
| Trace to system requirements | ✅ | ✅ | ✅ |
| Trace to risk controls (ISO 14971) | — | ✅ | ✅ |
| Re-evaluate medical device risk analysis | — | ✅ | ✅ |

Section 5.3: Software Architectural Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Divide software into components (modules, libraries, tasks)

**Required Outputs:**

**Software Architecture Document (SAD) or Software Design Document (SDD)**

**Architecture must define:**
- **Software items:** Modules, tasks, libraries
- **Interfaces:** How items communicate (APIs, messages, shared memory)
- **Data flow:** How information moves through system
- **Segregation:** Isolation of high-risk from low-risk items (if applicable)

**Example Architecture (Class C Insulin Pump):**

```
┌──────────────────────────────────────────────────────────────────┐
│                      Insulin Pump Software                       │
├──────────────────────────────────────────────────────────────────┤
│ Software Item       │ Class │ Function                           │
├─────────────────────┼───────┼────────────────────────────────────┤
│ DosingController    │  C    │ Calculate & limit insulin dose     │
│ PumpDriver          │  C    │ Control motor for insulin delivery │
│ SensorInterface     │  C    │ Read glucose sensor via I2C        │
│ SafetyMonitor       │  C    │ Watchdog, sanity checks            │
├─────────────────────┼───────┼────────────────────────────────────┤
│ UserInterface       │  B    │ Display, buttons, alarms           │
│ AlarmManager        │  B    │ Audio/visual alerts                │
├─────────────────────┼───────┼────────────────────────────────────┤
│ DataLogger          │  A    │ Log dosing history                 │
│ USBExport           │  A    │ Export data to PC                  │
└─────────────────────┴───────┴────────────────────────────────────┘
```

**Data Flow Diagram:**

```
┌──────────────┐      Glucose     ┌──────────────┐
│ Glucose      │─────  Value  ───▶│  Dosing      │
│ Sensor (HW)  │                   │  Controller  │
└──────────────┘                   └──────┬───────┘
                                          │ Dose Command
                                          ↓
                    ┌─────────────────────────────────┐
                    │    Safety Monitor (Limit Check) │
                    └──────────────┬──────────────────┘
                                   │ Safe Dose
                                   ↓
                           ┌───────────────┐
                           │  Pump Driver  │──▶ Motor (HW)
                           └───────────────┘
```

**SOUP Identification:**
- **FreeRTOS 10.5:** Real-time operating system (Class C, requires SOUP analysis)
- **Segger emWin 6.x:** GUI library (Class B)

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Document architecture | ✅ | ✅ | ✅ |
| Identify software items & interfaces | ✅ | ✅ | ✅ |
| Specify functional & performance reqs per item | ✅ | ✅ | ✅ |
| Specify interfaces (external, between items) | ✅ | ✅ | ✅ |
| Specify segregation of Class C items | — | — | ✅ (if mixed classes) |

Section 5.4: Software Detailed Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Define HOW each software item will be implemented

**Required Outputs:**

**Detailed Design Document (DDD) or extended SDD**

**Design must define:**
- **Algorithms:** Flowcharts, pseudocode
- **Data structures:** Classes, structs, databases
- **Interfaces:** Function signatures, API specs
- **Control flow:** State machines, sequence diagrams

**Example Detailed Design (Dosing Controller):**

**Module:** DosingController  
**Class:** C (safety-critical)  
**Function:** Calculate insulin dose with safety limits

**Algorithm (Pseudocode):**

```python
def calculate_insulin_dose(glucose_mg_dl, carbs_grams, user_correction):
    """
    Calculate insulin dose with safety limits.
    
    Args:
        glucose_mg_dl: Current blood glucose (mg/dL)
        carbs_grams: Carbohydrates to be consumed (grams)
        user_correction: Manual correction factor
    
    Returns:
        insulin_units: Safe insulin dose (units)
    """
    
    # Constants (from SRS)
    TARGET_GLUCOSE = 100  # mg/dL
    INSULIN_SENSITIVITY = 50  # mg/dL per unit insulin
    CARB_RATIO = 10  # grams carbs per unit insulin
    MAX_DOSE_PER_HOUR = 25  # units (safety limit)
    
    # Correction for high glucose
    if glucose_mg_dl > TARGET_GLUCOSE:
        correction_dose = (glucose_mg_dl - TARGET_GLUCOSE) / INSULIN_SENSITIVITY
    else:
        correction_dose = 0
    
    # Bolus for carbs
    carb_dose = carbs_grams / CARB_RATIO
    
    # Total dose
    total_dose = correction_dose + carb_dose + user_correction
    
    # Safety limit (REQ-SW-101)
    if total_dose > MAX_DOSE_PER_HOUR:
        total_dose = MAX_DOSE_PER_HOUR
        log_safety_limit_event()
        trigger_alarm("Dose limited to 25 units/hour")
    
    # Sanity check (negative dose = error)
    if total_dose < 0:
        total_dose = 0
        trigger_alarm("Invalid dose calculation")
    
    return total_dose
```

**Data Structure (C):**

```c
/* Dosing Controller State */
typedef struct {
    float current_glucose_mg_dl;
    float carbs_grams;
    float user_correction;
    float calculated_dose_units;
    uint32_t last_dose_timestamp;
    bool safety_limit_triggered;
} DosingControllerState_t;
```

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Document detailed design | — | ✅ | ✅ |
| Refine software items into lower-level items | — | ✅ | ✅ |
| Develop detailed design for each item | — | ✅ | ✅ |
| Define interfaces in detail | — | ✅ | ✅ |
| Verify detailed design (review, analysis) | — | ✅ | ✅ |

**Note:** Class A does NOT require detailed design documentation (code is the design)

Section 5.5: Software Unit Implementation & Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Write code & verify each unit (module, function, class)

**Required Outputs:**

1. **Source Code:**
   - Follows coding standards (e.g., MISRA C, CERT C)
   - Commented & readable
   - Under version control

2. **Unit Test Results:**
   - Test cases for each unit
   - Coverage analysis (statement, branch, MC/DC for Class C)

**Coding Standard Example (MISRA C:2012):**

```c
/* MISRA C:2012 Compliant Code */

/* Rule 8.4: Functions shall have prototype declarations */
float calculate_insulin_dose(float glucose, float carbs, float correction);

/* Rule 15.5: Function shall have single point of exit */
float calculate_insulin_dose(float glucose, float carbs, float correction) {
    float dose = 0.0f;  /* Rule 9.1: Initialize all variables */
    
    /* Rule 14.4: Controlling expression shall have boolean type */
    if (glucose > TARGET_GLUCOSE_F) {
        dose = (glucose - TARGET_GLUCOSE_F) / INSULIN_SENSITIVITY_F;
    }
    
    dose += carbs / CARB_RATIO_F;
    dose += correction;
    
    /* Rule 13.5: No side effects in right operand of logical operator */
    if (dose > MAX_DOSE_PER_HOUR_F) {
        dose = MAX_DOSE_PER_HOUR_F;
        log_safety_limit();  /* Separate statement, not in condition */
    }
    
    return dose;  /* Single exit point */
}
```

**Unit Testing:**

**Test Framework:** CppUTest, Unity, Google Test

**Example Unit Test:**

```cpp
// Unit Test: calculate_insulin_dose
TEST(DosingController, MaxDoseLimit) {
    // Test Case: TC-SW-101 (verify maximum dose limit)
    
    // Input: Very high glucose (should trigger limit)
    float glucose = 500.0f;  // mg/dL (dangerously high)
    float carbs = 100.0f;    // grams (large meal)
    float correction = 5.0f; // units (user correction)
    
    // Execute
    float dose = calculate_insulin_dose(glucose, carbs, correction);
    
    // Verify: Dose limited to 25 units
    CHECK_EQUAL(25.0f, dose);
    
    // Verify: Safety event logged
    CHECK(safety_limit_event_logged());
}

TEST(DosingController, NormalDose) {
    // Test Case: Nominal glucose, moderate carbs
    float glucose = 120.0f;
    float carbs = 50.0f;
    float correction = 0.0f;
    
    float dose = calculate_insulin_dose(glucose, carbs, correction);
    
    // Expected: (120-100)/50 + 50/10 = 0.4 + 5 = 5.4 units
    CHECK_CLOSE(5.4f, dose, 0.1f);
}

TEST(DosingController, NegativeDoseProtection) {
    // Test Case: Invalid inputs should not produce negative dose
    float glucose = 50.0f;  // Low glucose
    float carbs = 0.0f;
    float correction = -10.0f;  // Erroneous negative correction
    
    float dose = calculate_insulin_dose(glucose, carbs, correction);
    
    // Verify: Dose is zero (not negative)
    CHECK(dose >= 0.0f);
}
```

**Coverage Analysis (Class C):**

| Metric | Required | Achieved |
|:-------|:---------|:---------|
| Statement Coverage | 100% | 100% ✅ |
| Branch Coverage | 100% | 100% ✅ |
| MC/DC (if complex decisions) | 100% | 100% ✅ |

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Implement software units | ✅ | ✅ | ✅ |
| Follow coding standards | ✅ | ✅ | ✅ |
| Unit testing | — | ✅ | ✅ |
| Additional unit verification (analysis, review) | — | — | ✅ |

Section 5.6: Software Integration & Integration Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Combine units into larger items & verify interactions

**Required Outputs:**

1. **Integration Plan:**
   - Order of integration (bottom-up, top-down, incremental)
   - Test environment (hardware, simulators, stubs)

2. **Integration Test Cases:**
   - Interface testing (API calls, messages, shared memory)
   - Data flow testing (end-to-end scenarios)

3. **Integration Test Results:**
   - Pass/fail for each test case
   - Defects found & resolved

**Integration Strategy (Incremental):**

```
Step 1: Integrate SensorInterface + DosingController
    → Test: Glucose reading triggers dose calculation

Step 2: Add PumpDriver
    → Test: Dose command activates motor

Step 3: Add SafetyMonitor
    → Test: Watchdog detects hung DosingController

Step 4: Add UserInterface
    → Test: Display shows glucose & dose

Step 5: Add AlarmManager
    → Test: Alarms trigger on high/low glucose

Step 6: Add DataLogger
    → Test: Dosing history recorded
```

**Example Integration Test:**

```
Test Case: TC-INT-010 — End-to-End Dosing Flow

Preconditions:
  - Glucose sensor connected & operational
  - Insulin reservoir > 50 units
  - User interface showing home screen

Test Steps:
  1. Inject simulated glucose reading: 180 mg/dL
  2. User enters carbs: 60 grams
  3. User presses "Deliver" button
  4. Verify DosingController calculates dose: (180-100)/50 + 60/10 = 7.6 units
  5. Verify SafetyMonitor checks limit: 7.6 < 25 ✅
  6. Verify PumpDriver delivers 7.6 units
  7. Verify DataLogger records event
  8. Verify UserInterface displays "Delivered 7.6 units"

Expected Result:
  - Dose delivered correctly
  - No alarms triggered
  - Event logged

Actual Result: PASS ✅
```

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| Integration testing per plan | ✅ | ✅ | ✅ |
| Test all interfaces | ✅ | ✅ | ✅ |
| Verify data & control flow | ✅ | ✅ | ✅ |
| Verify risk controls implemented | — | ✅ | ✅ |

Section 5.7: Software System Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Verify complete system meets all software requirements (SRS)

**Required Outputs:**

1. **Software System Test Plan:**
   - Scope (which requirements tested)
   - Test environment (real hardware vs. simulator)
   - Pass/fail criteria

2. **Software System Test Cases:**
   - One or more test cases per requirement
   - Cover normal, boundary, abnormal conditions

3. **Software System Test Results:**
   - Traceability matrix (Requirement → Test Case → Result)
   - Defects & resolutions

**Example System Test:**

```
Test Case: TC-SYS-101 — Maximum Dose Limit Enforcement

Requirement: REQ-SW-101 (Max 25 units/hour)

Objective:
  Verify software enforces maximum dose limit under all scenarios.

Test Environment:
  - Real insulin pump hardware
  - Simulated glucose sensor (inject fault)
  - Load cell to measure actual insulin delivered

Test Procedure:
  1. Set sensor to read 500 mg/dL (extreme high)
  2. Enter 200 grams carbs (unrealistic meal)
  3. Add 20 units manual correction (user error)
  4. Press "Deliver"
  5. Measure actual insulin delivered

Expected Result:
  - Calculated dose: (500-100)/50 + 200/10 + 20 = 48 units
  - Enforced dose: 25 units (limited)
  - Alarm: "Dose limited to 25 units/hour"
  - Actual delivered: 25.0 ± 0.5 units

Actual Result:
  - Delivered: 25.1 units ✅
  - Alarm displayed ✅
  - Event logged ✅

Verdict: PASS
```

**Requirements Traceability Matrix:**

| Requirement ID | Test Case ID | Result | Defects |
|:---------------|:-------------|:-------|:--------|
| REQ-SW-101 | TC-SYS-101 | PASS | None |
| REQ-SW-102 | TC-SYS-102 | PASS | None |
| REQ-SW-103 | TC-SYS-103 | FAIL → PASS | DEF-045 (fixed) |
| ... | ... | ... | ... |

**Class-Specific Requirements:**

| Activity | Class A | Class B | Class C |
|:---------|:--------|:--------|:--------|
| System testing per plan | ✅ | ✅ | ✅ |
| Test all software requirements | ✅ | ✅ | ✅ |
| Re-test after changes | ✅ | ✅ | ✅ |
| Verify risk controls | — | ✅ | ✅ |
| Regression testing | — | ✅ | ✅ |

Section 5.8: Software Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Package software for integration into medical device

**Required Outputs:**

1. **Software Release Documentation:**
   - Known anomalies (bugs, limitations)
   - Configuration (versions, build settings)
   - Installation instructions

2. **Released Software:**
   - Binary executable(s)
   - Configuration files
   - Installation scripts

**Example Software Release Package:**

```
InsulinPump_SW_v2.1.0_Release/
├── README.txt                  (Release notes)
├── KNOWN_ANOMALIES.txt         (Bug list with risk assessment)
├── bin/
│   ├── insulin_pump.elf        (ARM binary)
│   └── checksum.sha256         (Integrity check)
├── config/
│   ├── default_settings.ini
│   └── calibration_data.bin
├── install/
│   └── flash_instructions.pdf
└── docs/
    ├── SoftwareRequirementsSpec_v2.1.pdf
    ├── SoftwareDesignDocument_v2.1.pdf
    └── TestResults_v2.1.pdf
```

**Known Anomalies Document:**

```
Known Anomaly Report — Insulin Pump SW v2.1.0

ANO-023: Display flicker during low battery
  Severity: Cosmetic
  Risk: None (does not affect dosing)
  Workaround: Replace battery
  Plan: Fix in v2.2.0

ANO-045: USB export slow for >1000 records
  Severity: Minor usability
  Risk: None
  Workaround: Export in smaller batches
  Plan: Optimize in v2.2.0
```

════════════════════════════════════════════════════════════════════════════

🛡️ **RISK MANAGEMENT (ISO 14971 Integration)**
───────────────────────────────────────────────

IEC 62304 Section 7: Software Risk Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**  
Integrate software development with medical device risk management

**Process:**

```
┌─────────────────────────────────────────────────────────────────┐
│ ISO 14971: Medical Device Risk Management                      │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │ 1. Hazard Identification              │
        │    (What can go wrong?)               │
        └────────────────┬──────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │ 2. Risk Analysis                      │
        │    (Severity × Probability)           │
        └────────────────┬──────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │ 3. Risk Evaluation                    │
        │    (Acceptable? → No → Risk Control)  │
        └────────────────┬──────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │ 4. Risk Control (Software!)           │ ← IEC 62304 §7
        │    → Software safety requirements     │
        │    → Design features                  │
        │    → Verification                     │
        └────────────────┬──────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │ 5. Residual Risk Evaluation           │
        │    (After controls, still acceptable?)│
        └────────────────┬──────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │ 6. Risk Management Review             │
        │    (Overall risk acceptable?)         │
        └───────────────────────────────────────┘
```

**Example: Insulin Overdose Hazard**

**Hazard Identification:**
- **Hazard:** Software calculates excessive insulin dose
- **Hazardous Situation:** Patient receives 100× intended dose
- **Harm:** Severe hypoglycemia → coma → death

**Risk Analysis (before control):**
- **Severity:** Catastrophic (death)
- **Probability:** Medium (software bugs occur)
- **Risk Level:** Unacceptable (High)

**Risk Control (Software):**

1. **RC-001: Maximum Dose Limit**
   - **Control:** Software enforces 25 units/hour hard limit (REQ-SW-101)
   - **Verification:** Test case TC-SYS-101

2. **RC-002: Plausibility Checks**
   - **Control:** Software rejects glucose readings < 20 or > 600 mg/dL
   - **Verification:** Test case TC-SYS-102

3. **RC-003: Independent Monitoring**
   - **Control:** Safety monitor watchdog checks dosing logic sanity
   - **Verification:** Test case TC-SYS-103

**Residual Risk Evaluation (after controls):**
- **Severity:** Catastrophic (unchanged)
- **Probability:** Very Low (multiple controls reduce likelihood)
- **Residual Risk Level:** Acceptable (Low)

════════════════════════════════════════════════════════════════════════════

🛠️ **SOFTWARE OF UNKNOWN PROVENANCE (SOUP)**
─────────────────────────────────────────────

IEC 62304 Section 8.1.2: SOUP Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**SOUP Definition:**  
*Software item that is already developed and generally available, and that has not been developed for the purpose of being incorporated into the medical device*

**Examples:**
- **Operating systems:** Linux, FreeRTOS, Windows Embedded
- **Libraries:** OpenSSL, zlib, JPEG library
- **Middleware:** MQTT broker, database (SQLite)
- **Commercial components:** GUI frameworks, communication stacks

**Why SOUP is Risky:**
- Not developed per IEC 62304 (unknown quality)
- Bugs may exist (not safety-tested)
- Updates may introduce regressions

SOUP Analysis Process
~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Identify SOUP Items**

| SOUP Item | Version | Purpose | Safety Class |
|:----------|:--------|:--------|:-------------|
| FreeRTOS | 10.5.1 | Real-time OS | C (critical) |
| OpenSSL | 3.0.8 | Encryption | B (moderate) |
| SQLite | 3.40.1 | Data storage | A (non-critical) |

**Step 2: Specify Functional Requirements**

For FreeRTOS:
```
SOUP-REQ-001: FreeRTOS shall provide task scheduling with priority preemption.
SOUP-REQ-002: FreeRTOS shall support mutexes for inter-task synchronization.
SOUP-REQ-003: FreeRTOS shall provide timer services with 1 ms resolution.
```

**Step 3: Specify Performance Requirements**

```
SOUP-REQ-010: Task switch latency shall be < 10 µs.
SOUP-REQ-011: Memory footprint shall be < 50 KB.
```

**Step 4: Document Known Anomalies**

Research SOUP vendor's bug database, CVEs, security advisories:

```
FreeRTOS Known Anomalies:
- CVE-2021-XXXXX: Race condition in queue handling (fixed in 10.4.5)
- Issue #4567: Timer overflow on long uptimes (workaround: periodic reboot)
```

**Step 5: Evaluate SOUP for Intended Use**

**Checklist:**
- ✅ Vendor reputation (AWS/Amazon for FreeRTOS)
- ✅ Community support (active forum, bug reports)
- ✅ Documentation quality (good API reference)
- ✅ Update frequency (regular security patches)
- ⚠️ Known bugs affecting medical use (assess impact)

**Step 6: Verification of SOUP**

- **Functional testing:** Verify SOUP meets specified requirements
- **Anomaly testing:** Test known bugs in context of medical device
- **Regression testing:** Re-test SOUP after updates

**Example SOUP Test (FreeRTOS):**

```c
// SOUP Test: Verify FreeRTOS task scheduling
TEST(FreeRTOS_SOUP, TaskPreemption) {
    // Create high-priority task
    TaskHandle_t high_task;
    xTaskCreate(high_priority_task, "HighTask", 128, NULL, 10, &high_task);
    
    // Create low-priority task
    TaskHandle_t low_task;
    xTaskCreate(low_priority_task, "LowTask", 128, NULL, 5, &low_task);
    
    // Run scheduler
    vTaskStartScheduler();
    
    // Verify: High-priority task runs first
    CHECK(high_task_executed_before_low_task());
}
```

**Step 7: SOUP Configuration Management**

- Version control (specific version, not "latest")
- Document all configuration options used
- Change control for SOUP updates

════════════════════════════════════════════════════════════════════════════

📊 **CONFIGURATION MANAGEMENT (Section 8)**
───────────────────────────────────────────

Purpose
~~~~~~~

Ensure:
- All software items identified & controlled
- Changes tracked & approved
- Released software reproducible

Configuration Management Activities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CM Plan Contents:**
1. Items under CM (source code, docs, tools, SOUP)
2. Version control system (Git, SVN)
3. Baseline definition & approval
4. Change control process
5. Branch strategy (main, release, feature branches)

**Example CM Items:**

```
Source Code:
  - All .c, .h, .cpp files
  - Build scripts (Makefile, CMakeLists.txt)
  - Linker scripts, startup code

Documentation:
  - SRS, SDD, Test Plans, Test Results
  - Risk Management File
  - SOUP documentation

SOUP:
  - FreeRTOS source code (specific version)
  - OpenSSL binaries
  - Configuration files for SOUP

Tools:
  - Compiler (GCC 11.2.0, specific binary)
  - IDE configuration files
  - Static analysis rulesets (MISRA checker config)
```

**Baselines:**

| Baseline | When Established | Contents |
|:---------|:-----------------|:---------|
| Requirements Baseline | After SRS approval | SRS v1.0 |
| Design Baseline | After design review | SDD v1.0, source code v1.0 |
| Test Baseline | After system test | Test plan & results v1.0 |
| Release Baseline | Before product release | All artifacts v1.0 |

**Change Control Workflow:**

```
┌──────────────┐
│ Change       │
│ Request (CR) │
└──────┬───────┘
       ↓
┌──────────────┐
│ Impact       │ (Safety, schedule, cost, re-verification)
│ Analysis     │
└──────┬───────┘
       ↓
┌──────────────┐
│ Approval     │ (Change Control Board reviews)
│ Decision     │
└──────┬───────┘
       ↓ (Approved)
┌──────────────┐
│ Implement    │
│ Change       │
└──────┬───────┘
       ↓
┌──────────────┐
│ Verification │ (Re-test affected areas)
└──────┬───────┘
       ↓
┌──────────────┐
│ Update       │
│ Baseline     │
└──────────────┘
```

════════════════════════════════════════════════════════════════════════════

🐛 **PROBLEM RESOLUTION (Section 9)**
─────────────────────────────────────

Purpose
~~~~~~~

Systematically handle:
- **Bugs:** Software defects found in testing or field use
- **Anomalies:** Unexpected behavior (may or may not be bugs)
- **Enhancement requests:** New features (if safety-related)

Problem Resolution Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Problem Identification:**
Report source: Testing, field complaints, user feedback, security alerts

**Problem Report Template:**

```
Problem Report #: PR-2025-045

Title: Dose calculation incorrect for edge case (glucose = 0)

Reported By: QA Tester (John Doe)
Date: 2025-08-15

Description:
  When glucose sensor reports 0 mg/dL (sensor fault), the dosing algorithm
  calculates a negative dose, which is then clamped to zero. However, no
  alarm is triggered to alert the user of the sensor fault.

Severity: Major (potential harm if sensor fault undetected)

Steps to Reproduce:
  1. Inject glucose reading of 0 mg/dL
  2. Enter carbs: 50 grams
  3. Press "Deliver"
  4. Observe: Dose = 0, but no alarm

Expected: Alarm "Sensor fault detected"

Software Version: v2.0.3
Safety Class: C
```

**2. Problem Investigation:**

Analyze root cause:
```
Root Cause Analysis (PR-2025-045):

Finding:
  - Dose calculation correctly clamps negative dose to zero
  - BUT: Alarm is only triggered if dose > MAX_LIMIT, not if dose < 0

Code Location:
  DosingController.c, line 145

Root Cause:
  Missing alarm trigger for invalid (negative) dose calculation

Risk Assessment:
  - Current: Sensor fault may go unnoticed → patient doesn't dose
  - Harm: Hyperglycemia (high glucose) if meal insulin not delivered
  - Severity: Moderate (non-serious injury)
```

**3. Change Request & Approval:**

```
Change Request #: CR-2025-052 (linked to PR-2025-045)

Proposed Solution:
  Add alarm trigger when calculated dose is negative:
  
  if (total_dose < 0) {
      total_dose = 0;
      trigger_alarm("Sensor fault detected");  // ← ADD THIS LINE
  }

Impact Analysis:
  - Code change: 1 line added
  - Safety impact: Reduces risk (improves fault detection)
  - Re-verification: Test case TC-PR-045 (new), regression tests

CCB Decision: APPROVED (2025-08-20)
```

**4. Implement & Verify:**

```
Implementation:
  - Code updated in DosingController.c
  - Git commit: abc123 "Fix PR-2025-045: Add alarm for negative dose"
  - New test case: TC-PR-045

Verification:
  - TC-PR-045: PASS ✅ (alarm triggers for glucose = 0)
  - Regression tests: PASS ✅ (no new bugs introduced)
```

**5. Problem Report Closure:**

```
Problem Report #: PR-2025-045

Status: CLOSED (2025-08-25)

Resolution:
  - Change CR-2025-052 implemented in SW v2.0.4
  - Verification complete
  - Risk reduced: Moderate → Low

Lessons Learned:
  - Need better coverage of edge cases (sensor faults)
  - Action: Add "invalid input" test category to test plan
```

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS & ANSWERS**
───────────────────────────────

Question 1: What are the three software safety classes?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

| Class | Injury Possible | Examples |
|:-----:|:----------------|:---------|
| **C** | Death or serious injury | Insulin pump, ventilator, pacemaker |
| **B** | Non-serious injury | Blood glucose meter, BP monitor |
| **A** | No injury | Patient education app, data viewer |

**Classification based on:**  
Risk analysis per ISO 14971 (potential harm from software failure)

Question 2: What is SOUP?
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**SOUP = Software of Unknown Provenance**

Definition: Pre-existing software not developed specifically for the medical device (e.g., Linux, OpenSSL, FreeRTOS).

**IEC 62304 Requirements:**
- Document functional & performance requirements for SOUP
- Evaluate SOUP for intended use (vendor reputation, known bugs)
- Verify SOUP in context of medical device
- Configuration management for SOUP (specific versions)

Question 3: What activities are required for Class C but not Class A?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

| Activity | Class A | Class C |
|:---------|:--------|:--------|
| Detailed design documentation | ❌ | ✅ |
| Unit testing | ❌ | ✅ |
| Additional unit verification (review, analysis) | ❌ | ✅ |
| Integration with risk management | ❌ | ✅ |
| Segregation of mixed-class items | ❌ | ✅ (if applicable) |

**Rationale:**  
Class C (serious injury/death possible) requires maximum rigor to minimize risk.

Question 4: How does IEC 62304 integrate with ISO 14971?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**ISO 14971:** Medical device risk management (identifies hazards, evaluates risks)

**IEC 62304 Section 7:** Software risk management process

**Integration:**
1. **Hazard analysis (ISO 14971)** identifies software-related hazards
2. **Safety requirements (IEC 62304)** implement risk controls
3. **Verification (IEC 62304)** proves risk controls work
4. **Residual risk evaluation (ISO 14971)** confirms acceptability

**Example:**
- **Hazard:** Insulin overdose
- **Risk Control:** SW enforces 25 unit/hour limit (IEC 62304 requirement)
- **Verification:** Test case proves limit enforced
- **Residual Risk:** Acceptable (multiple controls reduce probability)

Question 5: What is software segregation?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**Segregation:**  
Isolating high-risk (Class C) software items from low-risk (Class A/B) to simplify compliance

**Benefits:**
- Reduce scope of Class C rigor (lower cost)
- Allow commercial libraries in Class A/B portions

**Requirements:**
- **Independence:** Failure in Class A cannot propagate to Class C
- **Freedom from interference:** Memory protection, separate processes
- **Documented rationale:** Justify segregation in risk analysis

**Example:**
```
Class C: Drug Dosing Algorithm (full rigor)
Class A: Data Export (minimal rigor)
→ Segregation: Data export runs in separate process, cannot corrupt dosing
```

Question 6: What is a problem report?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

A **problem report** is a formal record of a software defect, anomaly, or issue.

**IEC 62304 Section 9:** Problem Resolution Process

**Contents:**
- Problem description & severity
- Steps to reproduce
- Root cause analysis
- Proposed solution (change request)
- Verification results
- Closure status

**Purpose:**
- Track all software problems
- Ensure systematic resolution
- Support regulatory audits (show due diligence)

Question 7: What are the key deliverables for IEC 62304?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

| Deliverable | Purpose |
|:------------|:--------|
| Software Development Plan (SDP) | Master plan for development |
| Software Requirements Spec (SRS) | What software must do |
| Software Architecture (SAD) | High-level design |
| Software Detailed Design (SDD) | Low-level design (Class B/C) |
| Source Code | Implementation |
| Unit Test Results | Verification of modules |
| Integration Test Results | Verification of interfaces |
| System Test Results | Verification of requirements |
| Risk Management File | Hazard analysis & controls (ISO 14971) |
| SOUP Documentation | Analysis of off-the-shelf components |
| Configuration Management Plan | Version control, baselines |
| Problem Reports | Bug tracking & resolution |
| Software Release Documentation | Known anomalies, installation |

Question 8: What is the difference between verification and validation?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

- **Verification:** "Are we building it right?" (SW meets SRS)
- **Validation:** "Are we building the right thing?" (SW meets user needs)

**IEC 62304 Context:**

**Verification (Section 5):**
- Unit testing
- Integration testing
- System testing
- Result: Software complies with SRS ✅

**Validation (Part of ISO 13485 / FDA):**
- Clinical evaluation
- Usability testing (IEC 62366)
- Real-world performance
- Result: Software safe & effective for intended use ✅

Question 9: What is the purpose of the Change Control Board (CCB)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

The **CCB** reviews and approves/rejects changes to baselined software.

**Responsibilities:**
- Review change requests (bugs, enhancements)
- Assess safety impact (risk analysis)
- Approve or reject changes
- Ensure re-verification after changes

**Typical Membership:**
- Software lead
- System engineer
- QA/RA (Quality/Regulatory)
- Risk management lead

Question 10: Can you use Agile for IEC 62304?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Answer:**

**Yes!** IEC 62304 does NOT mandate waterfall.

**Agile + IEC 62304:**
- **Iterative development:** Incremental requirements, design, test (allowed)
- **Traceability:** Must maintain (use tools like Jama, Azure DevOps)
- **Baselines:** Establish per sprint or release
- **Documentation:** Can be living documents (updated incrementally)
- **Verification:** Continuous testing (CI/CD with automated tests)

**Key Principles:**
- All IEC 62304 activities must be completed (just not necessarily in waterfall order)
- Traceability maintained throughout
- Independent reviews at appropriate milestones

**Regulatory Acceptance:**  
FDA, EU notified bodies accept Agile if IEC 62304 requirements met

════════════════════════════════════════════════════════════════════════════

📋 **COMPLETION CHECKLIST**
───────────────────────────

**Planning:**
- [ ] Software Development Plan (SDP) written & approved
- [ ] Software safety classification determined (Class A/B/C)
- [ ] Development standards identified (coding, testing)
- [ ] Risk management plan integrated (ISO 14971)

**Requirements:**
- [ ] Software Requirements Specification (SRS) written & baselined
- [ ] Requirements traced to system requirements & risks
- [ ] Safety requirements identified from risk analysis

**Design:**
- [ ] Software architecture documented (if Class B/C)
- [ ] Detailed design documented (if Class C)
- [ ] SOUP items identified & analyzed
- [ ] Segregation strategy documented (if mixed classes)

**Implementation:**
- [ ] Source code written per coding standards
- [ ] Code under version control (Git, SVN)
- [ ] Unit tests executed (if Class B/C)
- [ ] Code reviews completed (if Class C)

**Verification:**
- [ ] Integration tests executed
- [ ] System tests executed (all requirements)
- [ ] Traceability matrix complete (Req → Test → Result)
- [ ] Risk controls verified

**Configuration Management:**
- [ ] All items under CM
- [ ] Baselines established
- [ ] Change control process operational

**Problem Resolution:**
- [ ] Problem tracking system operational
- [ ] All problems investigated & resolved
- [ ] Change Control Board functional

**Release:**
- [ ] Known anomalies documented
- [ ] Release documentation complete
- [ ] Software released to production

**Regulatory:**
- [ ] All IEC 62304 objectives met for assigned safety class
- [ ] Technical file complete (for EU MDR)
- [ ] Design history file complete (for FDA)

════════════════════════════════════════════════════════════════════════════

📚 **FURTHER READING & REFERENCES**
───────────────────────────────────

**Primary Standards:**
- **IEC 62304:2006 + AMD1:2015:** Medical device software lifecycle
- **ISO 14971:2019:** Medical device risk management
- **ISO 13485:2016:** Medical devices QMS
- **IEC 62366-1:2015:** Usability engineering for medical devices

**Regulatory Guidance:**
- **FDA Guidance:** *General Principles of Software Validation* (2002)
- **FDA Guidance:** *Content of Premarket Submissions for Software in Medical Devices* (2005)
- **EU MDR 2017/745:** Medical Device Regulation (software requirements)

**Books:**
- *IEC 62304 Medical Device Software* by S. Vogel
- *Agile Development for Medical Devices* by J. Schleich

**Training:**
- **Johner Institute:** IEC 62304 compliance courses
- **OrielSTAT:** Medical device software training

**Tools:**
- **Jama Connect:** Requirements management & traceability
- **Helix ALM:** Integrated development & QMS for medical devices
- **PTC Integrity:** Lifecycle management for regulated industries

════════════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 1.0 — Comprehensive IEC 62304 reference  
**Audience:** Medical device software engineers, QA engineers, regulatory specialists
