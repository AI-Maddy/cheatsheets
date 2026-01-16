🔧 **Maintainability Engineering — Design for Serviceability and Support**
════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for MTTR Optimization and Maintenance Design**  
**Metrics:** MTTR | MDT | M̄ | Maintainability Index | Diagnostic Coverage  
**Domains:** Aerospace ✈️ | Automotive 🚗 | Industrial 🏭 | Medical 🏥 | Military 🎖️  
**Purpose:** Reduce lifecycle costs, improve availability, enable rapid repair

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**What is Maintainability?**

*"Ability to restore a system to operational state after failure, measured by ease and speed of maintenance actions"*

**Core Metric:**

.. code-block:: text

   MTTR = Mean Time To Repair (average repair time)
   
   MTTR = Detection + Diagnosis + Repair + Recovery + Verification
   
   Example Breakdown:
   - Detection:    5 min (automated monitoring)
   - Diagnosis:   15 min (fault isolation, logs)
   - Repair:      30 min (component replacement)
   - Recovery:    10 min (restart, reconfigure)
   - Verification: 5 min (functional tests)
   Total MTTR:    65 minutes

**Maintainability Function M(t):**

.. code-block:: text

   M(t) = P(repair completed within time t)
   
   For exponential distribution (constant repair rate μ):
   M(t) = 1 - e^(-μt)
   
   Where: μ = 1/MTTR
   
   Example: MTTR = 30 min = 0.5 hr, μ = 2 /hr
   M(0.5) = 1 - e^(-2×0.5) = 1 - e^(-1) = 0.632
   → 63.2% chance repair completes within 30 minutes

**Design for Maintainability Principles:**

✅ **Accessibility** → Easy physical access to components  
✅ **Modularity** → Line-Replaceable Units (LRUs), plug-and-play  
✅ **Standardization** → Common fasteners, connectors, tools  
✅ **Diagnostics** → Built-In Test (BIT), fault codes, LEDs  
✅ **Documentation** → Clear manuals, wiring diagrams, troubleshooting guides  
✅ **Training** → Skill-appropriate maintenance tasks

**Maintainability vs Maintenance:**

.. code-block:: text

   Maintainability: Design attribute (HOW EASY to maintain)
   Maintenance: Activity (THE ACT of maintaining)
   
   Good maintainability → Low MTTR → High availability

════════════════════════════════════════════════════════════════════════════

📖 **1. MAINTAINABILITY FUNDAMENTALS**
════════════════════════════════════════════════════════════════════════════

1.1 Definitions and Metrics
----------------------------

**Mean Time To Repair (MTTR):**

.. code-block:: text

   MTTR = Total Repair Time / Number of Repairs
   
   Example: 10 failures, repair times: 20, 25, 30, 35, 40, 22, 28, 33, 27, 30 min
   MTTR = (20+25+30+35+40+22+28+33+27+30) / 10
        = 290 / 10 = 29 minutes

**Mean Downtime (MDT):**

.. code-block:: text

   MDT = MTTR + Logistics Time + Administrative Time
   
   Example:
   - MTTR (actual repair):    30 min
   - Logistics (get parts):   60 min
   - Administrative (approval): 15 min
   MDT = 30 + 60 + 15 = 105 minutes

**Mean Preventive Maintenance Time (M̄_p):**

.. code-block:: text

   Average time for scheduled maintenance (inspections, lubrication, calibration)

**Mean Corrective Maintenance Time (M̄_c):**

.. code-block:: text

   Average time for unscheduled repairs (failures)
   Usually M̄_c > M̄_p (corrective takes longer)

────────────────────────────────────────────────────────────────────────────

**1.2 Maintainability Function**
--------------------------------

**Definition:** Probability that maintenance action is completed within time t

.. code-block:: text

   M(t) = P(Repair Time ≤ t)
   
   For exponential repair time distribution:
   M(t) = 1 - e^(-μt)
   
   Where: μ = Repair rate = 1/MTTR

**Example Calculation:**

.. code-block:: python

   import math
   
   MTTR = 2.0  # hours
   mu = 1 / MTTR
   
   # Probability of repair within 1 hour
   t = 1.0
   M_1 = 1 - math.exp(-mu * t)
   print(f"P(repair ≤ 1 hr): {M_1:.4f} ({M_1*100:.2f}%)")
   # Output: 0.3935 (39.35%)
   
   # Probability of repair within 2 hours (MTTR)
   t = 2.0
   M_2 = 1 - math.exp(-mu * t)
   print(f"P(repair ≤ 2 hr): {M_2:.4f} ({M_2*100:.2f}%)")
   # Output: 0.6321 (63.21%)
   
   # Probability of repair within 4 hours (2×MTTR)
   t = 4.0
   M_4 = 1 - math.exp(-mu * t)
   print(f"P(repair ≤ 4 hr): {M_4:.4f} ({M_4*100:.2f}%)")
   # Output: 0.8647 (86.47%)

**Key Insight:** 63.2% of repairs complete within MTTR (for exponential distribution)

────────────────────────────────────────────────────────────────────────────

**1.3 Maintenance Levels**
--------------------------

**Organizational Maintenance (O-Level):**
- Performed by: Operator/crew
- Location: On-site, at equipment
- Tasks: Inspection, lubrication, adjustment, minor repairs
- Tools: Basic hand tools
- Example: Aircraft line maintenance (daily checks)

**Intermediate Maintenance (I-Level):**
- Performed by: Technicians
- Location: Shop/workshop (on-base)
- Tasks: Component replacement, calibration, testing
- Tools: Test equipment, special tools
- Example: Avionics shop (replace LRUs)

**Depot Maintenance (D-Level):**
- Performed by: Specialists/OEM
- Location: Major facility, manufacturer
- Tasks: Overhaul, refurbishment, modifications
- Tools: Advanced test equipment, jigs, fixtures
- Example: Engine overhaul facility

**Maintenance Level Comparison:**

+--------+----------------+-------------------+-----------------+
| Level  | Complexity     | Turnaround Time   | Cost            |
+========+================+===================+=================+
| O      | Low            | Minutes-hours     | Lowest          |
+--------+----------------+-------------------+-----------------+
| I      | Medium         | Hours-days        | Medium          |
+--------+----------------+-------------------+-----------------+
| D      | High           | Weeks-months      | Highest         |
+--------+----------------+-------------------+-----------------+

**Design Goal:** Push maintenance to lowest practical level (minimize D-level)

════════════════════════════════════════════════════════════════════════════

📖 **2. DESIGN FOR MAINTAINABILITY**
════════════════════════════════════════════════════════════════════════════

2.1 Accessibility
-----------------

**Principle:** Provide adequate space and access for maintenance tasks

**Guidelines:**

.. code-block:: text

   Minimum Clearances (MIL-STD-1472):
   - Hand access: 4 inches (100 mm)
   - Arm access: 6 inches (150 mm)
   - Visual access: Line of sight + 30° viewing angle
   - Tool access: 6 inches + tool length

**Examples:**

**❌ Poor Accessibility:**

.. code-block:: text

   Problem: Electronic module buried behind 5 other modules
   Result: Remove 5 modules → Replace 1 module → Reinstall 5 modules
   MTTR: 3 hours (for 10-minute actual repair)

**✅ Good Accessibility:**

.. code-block:: text

   Solution: Quick-release latches, swing-out racks
   Result: Open door → Slide out module → Replace → Slide in → Close
   MTTR: 15 minutes

**Automotive Example:**

.. code-block:: text

   ❌ Bad: Engine buried, must remove intake manifold to change spark plugs
   ✅ Good: Top-mounted coil-on-plug, accessible from hood

────────────────────────────────────────────────────────────────────────────

**2.2 Modularity (Line-Replaceable Units)**
-------------------------------------------

**Concept:** Package functions into swappable modules

**Benefits:**
- ✅ Faster fault isolation (module-level diagnostics)
- ✅ Reduced skill requirements (no board-level repair)
- ✅ Improved logistics (stock spare LRUs)
- ✅ Parallel repair (faulty LRU repaired offline)

**Example: Avionics LRU**

.. code-block:: text

   Traditional Approach:
   1. Troubleshoot to component level (resistor, IC)
   2. Desolder component
   3. Solder new component
   4. Test and calibrate
   MTTR: 4-8 hours, requires skilled technician
   
   LRU Approach:
   1. Fault code points to LRU-5
   2. Remove 4 screws, disconnect 2 connectors
   3. Install replacement LRU
   4. System self-test passes
   MTTR: 15 minutes, requires basic technician

**LRU Design Checklist:**

.. code-block:: text

   - [ ] Self-contained (all components, no external dependencies)
   - [ ] Standard connectors (MIL-DTL-38999, etc.)
   - [ ] Keyed/foolproof installation (can't install backwards)
   - [ ] BIT (Built-In Test) for fault detection
   - [ ] Environmental sealing (dust, moisture protection)
   - [ ] Handling points (carry, lift without damage)

────────────────────────────────────────────────────────────────────────────

**2.3 Standardization**
-----------------------

**Fasteners:**

.. code-block:: text

   ❌ Bad: 6 different screw types (Phillips, Torx, hex, security)
   ✅ Good: Single type (e.g., all 1/4-turn Dzus fasteners)
   
   MTTR Impact: 5 min saved per panel removal

**Connectors:**

.. code-block:: text

   ❌ Bad: Proprietary connectors, require special tools
   ✅ Good: MIL-STD connectors, hand-mate/de-mate
   
   Example: Circular MIL-DTL-38999 (aerospace standard)

**Parts:**

.. code-block:: text

   Commonality: Use same power supply across 10 different systems
   Benefits:
   - Reduced spare parts inventory
   - Interchangeability (cannibalize from other unit)
   - Volume pricing (lower cost)

────────────────────────────────────────────────────────────────────────────

**2.4 Built-In Test (BIT)**
---------------------------

**Levels of BIT:**

**Power-On BIT (PBIT):**
- Runs automatically at startup
- Tests: Memory, I/O, sensors
- Duration: 5-30 seconds
- Abort boot if critical failure

**Continuous BIT (CBIT):**
- Runs during normal operation
- Tests: Range checks, plausibility, cross-checks
- Example: Dual sensor comparison (if differ > 10% → flag fault)

**Initiated BIT (IBIT):**
- Triggered by maintenance command
- Comprehensive diagnostics
- Duration: 1-5 minutes
- Tests: Full functional test, loopback, etc.

**Fault Isolation:**

.. code-block:: text

   Level 1: System-level (Flight Control System fault)
   Level 2: LRU-level (Actuator Controller #2 fault)
   Level 3: Assembly-level (Power supply board fault)
   Level 4: Component-level (Capacitor C15 failed)

**Target:** Isolate to LRU level (90% diagnostic coverage)

**Example BIT Output:**

.. code-block:: text

   Fault Code: FC-2345
   Description: Hydraulic Actuator #2 Position Sensor Fault
   LRU: Actuator Controller, Part Number: 12345-6789
   Action: Replace LRU, perform IBIT, verify operation

────────────────────────────────────────────────────────────────────────────

**2.5 Diagnostic Coverage**
---------------------------

**Definition:** Percentage of faults that diagnostics can detect and isolate

.. code-block:: text

   DC = (Detected Faults / Total Faults) × 100%
   
   Example: 100 possible faults, BIT detects 85
   DC = 85%

**Impact on MTTR:**

.. code-block:: text

   Low DC (50%):  Technician troubleshoots manually → MTTR = 2 hours
   High DC (95%): BIT identifies faulty LRU → MTTR = 15 minutes
   
   MTTR reduction factor: 8×

**EN 50128 Railway Requirements:**

.. code-block:: text

   SIL 4: Diagnostic Coverage ≥ 99% (of dangerous faults)
   SIL 3: Diagnostic Coverage ≥ 90%
   SIL 2: Diagnostic Coverage ≥ 60%

════════════════════════════════════════════════════════════════════════════

📖 **3. MAINTENANCE STRATEGIES**
════════════════════════════════════════════════════════════════════════════

3.1 Corrective Maintenance (Reactive)
--------------------------------------

**Definition:** Fix it when it breaks

**Pros:**
- ✅ No scheduled downtime
- ✅ Maximize component utilization (run to failure)
- ✅ Lower maintenance staff costs

**Cons:**
- ❌ Unpredictable failures (availability risk)
- ❌ Potential secondary damage (e.g., seized bearing damages shaft)
- ❌ Emergency parts procurement (expensive, long lead time)

**Appropriate For:**
- Non-critical components (redundant systems)
- Low-cost, easy-to-replace items (light bulbs, filters)
- Short MTBF components (wear items)

────────────────────────────────────────────────────────────────────────────

**3.2 Preventive Maintenance (Scheduled)**
------------------------------------------

**Definition:** Service at fixed intervals (time or usage-based)

**Examples:**

.. code-block:: text

   Aircraft Engine:
   - Every 100 flight hours: Borescope inspection
   - Every 500 flight hours: Oil change
   - Every 3,000 flight hours: Hot section inspection
   - Every 10,000 flight hours: Overhaul

**Interval Determination:**

.. code-block:: text

   Method 1: MTBF-based
   Interval = 0.5 × MTBF (replace before expected failure)
   
   Method 2: Weibull analysis
   Interval = η × 0.632 (63.2% survival point)
   
   Method 3: Regulatory requirement
   Interval = Mandated by standard (FAA AD, etc.)

**Pros:**
- ✅ Predictable maintenance schedule
- ✅ Reduced catastrophic failures
- ✅ Better parts planning (known demand)

**Cons:**
- ❌ Scheduled downtime (lost production)
- ❌ Replace components with remaining life (wasteful)
- ❌ Induced failures (maintenance errors)

────────────────────────────────────────────────────────────────────────────

**3.3 Predictive Maintenance (Condition-Based)**
------------------------------------------------

**Definition:** Monitor equipment, perform maintenance based on condition

**Technologies:**

**Vibration Analysis:**

.. code-block:: text

   Application: Rotating machinery (motors, pumps, bearings)
   Sensor: Accelerometer
   Indicator: Increased vibration amplitude at bearing frequencies
   Action: Replace bearing before seizure

**Thermography:**

.. code-block:: text

   Application: Electrical systems
   Sensor: Infrared camera
   Indicator: Hot spots (loose connections, overloaded circuits)
   Action: Tighten connections, redistribute load

**Oil Analysis:**

.. code-block:: text

   Application: Engines, gearboxes
   Sample: Lubricating oil
   Indicator: Metal particles (wear), viscosity breakdown
   Action: Replace oil, investigate source of contamination

**Ultrasonic Testing:**

.. code-block:: text

   Application: Compressed air systems, bearings
   Sensor: Ultrasonic detector
   Indicator: Air leaks, bearing defects
   Action: Repair leaks, replace bearing

**Benefits:**

.. code-block:: text

   Traditional PM: Replace every 1000 hours
   Predictive: Replace at 1200 hours (component still good at 1000)
   
   Savings: 20% longer component life × $500 bearing = $100 saved
   ROI: Sensors + software cost amortized over fleet

────────────────────────────────────────────────────────────────────────────

**3.4 Reliability-Centered Maintenance (RCM)**
----------------------------------------------

**Framework:** Systematic approach to determine optimal maintenance strategy

**RCM Process (7 Questions):**

.. code-block:: text

   1. What are the system functions?
   2. How can it fail to fulfill functions? (Functional failures)
   3. What causes each functional failure? (Failure modes - FMEA)
   4. What happens when each failure occurs? (Failure effects)
   5. Does failure matter? (Failure consequences)
   6. What can prevent failure? (Proactive tasks)
   7. What if no preventive task? (Default action - redesign, run-to-failure)

**Maintenance Task Selection:**

.. code-block:: text

   Decision Tree:
   
   Is failure detectable by operator?
   ├─ YES: Consider condition monitoring (predictive)
   │   └─ Effective? → Implement CBM
   │       └─ No: Consider scheduled replacement (preventive)
   │           └─ Effective? → Implement PM
   │               └─ No: Run-to-failure (corrective)
   │
   └─ NO (hidden failure): Scheduled functional test required
       └─ Design improvement to make failure evident

**Example: Aircraft Hydraulic Pump**

.. code-block:: text

   Function: Provide 3000 psi hydraulic pressure
   Failure Mode: Pump seizure (bearing wear)
   Detection: Pressure sensor, vibration monitor
   Consequence: Loss of flight control (critical)
   Strategy: Predictive (vibration monitoring) + PM (oil change every 500 hr)

════════════════════════════════════════════════════════════════════════════

📖 **4. MTTR OPTIMIZATION TECHNIQUES**
════════════════════════════════════════════════════════════════════════════

4.1 Reduce Detection Time
--------------------------

**Automated Monitoring:**

.. code-block:: yaml

   # Prometheus alerting (detect within 30 seconds)
   groups:
   - name: system_health
     rules:
     - alert: HighCPUUsage
       expr: cpu_usage > 90
       for: 30s
       annotations:
         summary: "CPU usage critical on {{ $labels.instance }}"
         action: "Check process list, kill runaway process"

**Health Dashboards:**

.. code-block:: text

   Real-time display:
   - CPU, memory, disk usage
   - Network throughput
   - Application response time
   - Error rates
   
   Alert on threshold violations (visual + audible)

────────────────────────────────────────────────────────────────────────────

**4.2 Reduce Diagnosis Time**
-----------------------------

**Fault Trees (Troubleshooting Guides):**

.. code-block:: text

   Symptom: System won't power on
   │
   ├─ LED indicator OFF?
   │   ├─ YES: Check power supply
   │   │   ├─ Voltage present? → Replace power supply
   │   │   └─ No voltage? → Check fuse, circuit breaker
   │   └─ NO: LED ON, system still off → Check enable signal
   │
   └─ LED indicator ON?
       └─ Check startup logs for boot failure

**Diagnostic Tools:**

.. code-block:: bash

   # Avionics example: Download fault logs
   ./diagnostic_tool --port /dev/ttyUSB0 --download-logs
   
   # Output:
   # Fault Code FC-2345: Sensor #2 out of range
   # Timestamp: 2026-01-15 14:32:07 UTC
   # LRU: Actuator Controller SN:12345
   # Recommended Action: Replace LRU, verify calibration

────────────────────────────────────────────────────────────────────────────

**4.3 Reduce Repair Time**
--------------------------

**Quick-Release Mechanisms:**

.. code-block:: text

   Traditional: 20 screws × 30 sec each = 10 minutes
   Quick-release: 4 quarter-turn fasteners × 5 sec = 20 seconds
   
   Time saved: 9.7 minutes per panel

**Hot-Swappable Components:**

.. code-block:: text

   Traditional: Shutdown system → Replace component → Restart → 10 min downtime
   Hot-swap: Remove failed module → Insert new → Auto-detected → 30 sec downtime
   
   Example: RAID hot-spare disk, redundant power supplies

**Pre-configured Replacements:**

.. code-block:: text

   ❌ Old: Replace component → Configure IP address, settings → 30 min
   ✅ New: Replace LRU → Auto-configure from central DB → 2 min

────────────────────────────────────────────────────────────────────────────

**4.4 Reduce Recovery Time**
----------------------------

**Automated Restart:**

.. code-block:: bash

   # Systemd auto-restart (Linux)
   [Service]
   Restart=always
   RestartSec=5s
   
   # Failed service automatically restarts in 5 seconds

**Configuration Management:**

.. code-block:: bash

   # Ansible playbook: Restore configuration in 2 minutes
   ansible-playbook restore_config.yml --limit failed_server

**Database Replication:**

.. code-block:: text

   Traditional: Restore from backup → 2 hours
   Replication: Promote standby replica → 30 seconds

────────────────────────────────────────────────────────────────────────────

**4.5 Reduce Verification Time**
--------------------------------

**Automated Testing:**

.. code-block:: python

   # Post-repair smoke test
   def verify_repair():
       tests = [
           test_power_on,
           test_sensor_readings,
           test_actuator_response,
           test_communication
       ]
       
       for test in tests:
           if not test():
               return False  # Repair failed verification
       
       return True  # All tests passed
   
   # Run in 2 minutes vs 15 minutes manual testing

════════════════════════════════════════════════════════════════════════════

📖 **5. MAINTAINABILITY ANALYSIS**
════════════════════════════════════════════════════════════════════════════

5.1 Maintainability Prediction
-------------------------------

**MIL-HDBK-472 (Maintainability Prediction)**

**Formula:**

.. code-block:: text

   MTTR_system = Σ (λ_i × MTTR_i) / Σ λ_i
   
   Where:
   - λ_i = Failure rate of component i
   - MTTR_i = Repair time for component i

**Example:**

.. code-block:: text

   System with 3 LRUs:
   
   LRU-1: λ = 100 FIT, MTTR = 15 min
   LRU-2: λ = 50 FIT,  MTTR = 30 min
   LRU-3: λ = 200 FIT, MTTR = 10 min
   
   MTTR_sys = (100×15 + 50×30 + 200×10) / (100+50+200)
            = (1500 + 1500 + 2000) / 350
            = 5000 / 350 = 14.3 minutes

**Interpretation:** Average repair time is 14.3 minutes (weighted by failure rates)

────────────────────────────────────────────────────────────────────────────

**5.2 Logistics Support Analysis (LSA)**
----------------------------------------

**Purpose:** Identify support resources required for maintenance

**Elements:**

.. code-block:: text

   1. Spare Parts:
      - Recommended spares list (RSL)
      - Provisioning: Based on failure rates, lead times
      
   2. Tools & Test Equipment:
      - Special tools required
      - Calibration requirements
      
   3. Personnel:
      - Skill levels (O/I/D maintenance)
      - Training requirements
      
   4. Technical Data:
      - Manuals, wiring diagrams
      - Troubleshooting procedures
      
   5. Facilities:
      - Shop space, environmental controls
      - Safety equipment

**Example: Aircraft Line Maintenance**

.. code-block:: text

   Spare Parts (per aircraft):
   - 2× Navigation light bulbs
   - 1× Hydraulic filter
   - 1× Air filter
   
   Tools:
   - Torque wrench (calibrated)
   - Multimeter
   - Safety wire pliers
   
   Personnel:
   - 2× A&P mechanics (FAA certified)
   - Training: 40 hours type-specific

════════════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════════════════════════════════════════════════════════

**Q1:** Calculate MTTR if repair times for 5 failures are: 10, 15, 20, 25, 30 minutes.

**A1:**

.. code-block:: text

   MTTR = (10 + 15 + 20 + 25 + 30) / 5
        = 100 / 5
        = 20 minutes

────────────────────────────────────────────────────────────────────────────

**Q2:** What is diagnostic coverage, and why does it matter for maintainability?

**A2:**

**Diagnostic Coverage (DC):**

.. code-block:: text

   DC = (Faults Detected and Isolated / Total Faults) × 100%

**Impact on Maintainability:**

.. code-block:: text

   Low DC (50%): Technician must manually troubleshoot
   → Long diagnosis time → High MTTR (e.g., 2 hours)
   
   High DC (95%): BIT identifies faulty LRU
   → Short diagnosis time → Low MTTR (e.g., 15 min)
   
   MTTR reduction factor: 8×

**Safety Standards Requirement:**  
IEC 61508 SIL 3 requires ≥90% diagnostic coverage of dangerous faults.

────────────────────────────────────────────────────────────────────────────

**Q3:** Compare corrective, preventive, and predictive maintenance strategies.

**A3:**

+-------------+-------------------+------------------+-------------------+
| Strategy    | Trigger           | Pros             | Cons              |
+=============+===================+==================+===================+
| Corrective  | Failure occurs    | No scheduled     | Unpredictable     |
|             |                   | downtime         | failures          |
+-------------+-------------------+------------------+-------------------+
| Preventive  | Fixed interval    | Predictable      | Replaces good     |
|             | (time/usage)      | schedule         | components        |
+-------------+-------------------+------------------+-------------------+
| Predictive  | Condition         | Optimize life    | Sensor/software   |
|             | monitoring        | utilization      | cost              |
+-------------+-------------------+------------------+-------------------+

**Best Practice:** Combine strategies based on RCM analysis (different components → different strategies)

────────────────────────────────────────────────────────────────────────────

**Q4:** What is maintainability function M(t), and how is it different from reliability R(t)?

**A4:**

**Maintainability M(t):**

.. code-block:: text

   M(t) = P(Repair completed within time t)
   
   For exponential: M(t) = 1 - e^(-μt), where μ = 1/MTTR
   
   Example: MTTR = 1 hr, t = 1 hr
   M(1) = 1 - e^(-1) = 0.632 (63.2% of repairs done within 1 hr)

**Reliability R(t):**

.. code-block:: text

   R(t) = P(Survive without failure for time t)
   
   For exponential: R(t) = e^(-λt), where λ = 1/MTBF

**Key Difference:**
- **R(t):** How long before failure (decreases with time)
- **M(t):** How quickly can repair (increases with time, approaches 1)

────────────────────────────────────────────────────────────────────────────

**Q5:** Calculate system MTTR given 3 LRUs with different failure rates and repair times (use weighted average).

**A5:**

**Given:**

.. code-block:: text

   LRU-A: λ = 100 FIT, MTTR = 20 min
   LRU-B: λ = 200 FIT, MTTR = 15 min
   LRU-C: λ = 50 FIT,  MTTR = 30 min

**Calculation:**

.. code-block:: text

   MTTR_sys = Σ(λ_i × MTTR_i) / Σλ_i
   
   Numerator:   100×20 + 200×15 + 50×30
              = 2000 + 3000 + 1500 = 6500
   
   Denominator: 100 + 200 + 50 = 350
   
   MTTR_sys = 6500 / 350 = 18.6 minutes

**Interpretation:** LRU-B dominates (highest failure rate), so system MTTR closer to its 15 min than others.

════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Design:**
- [ ] Ensure accessibility (hand, arm, visual clearances)
- [ ] Modularize into Line-Replaceable Units (LRUs)
- [ ] Standardize fasteners, connectors, tools
- [ ] Implement Built-In Test (BIT) with >90% diagnostic coverage
- [ ] Provide clear documentation (manuals, diagrams)

**Analysis:**
- [ ] Calculate MTTR (detection + diagnosis + repair + recovery + test)
- [ ] Predict system MTTR (weighted average by failure rates)
- [ ] Determine maintenance levels (O/I/D)

**Strategy:**
- [ ] Select maintenance approach (corrective, preventive, predictive, RCM)
- [ ] Schedule preventive maintenance intervals (0.5×MTBF or Weibull-based)
- [ ] Implement condition monitoring for critical components

**Optimization:**
- [ ] Reduce detection time (automated monitoring, alerts)
- [ ] Reduce diagnosis time (fault trees, diagnostic tools)
- [ ] Reduce repair time (quick-release, hot-swap, pre-config)
- [ ] Reduce recovery time (auto-restart, config management)

════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════════════════════════════════════════════════════════════

1️⃣ **Maintainability = Design attribute** — Good maintainability → Low MTTR → High availability

2️⃣ **MTTR has 5 components** — Detection, Diagnosis, Repair, Recovery, Verification (optimize each)

3️⃣ **Diagnostic coverage is critical** — 90% DC → 10× faster diagnosis than 50% DC

4️⃣ **Modularity enables fast repair** — LRU swap in 15 min vs component-level repair in 4 hours

5️⃣ **Accessibility drives MTTR** — 5 modules to remove → 3 hr MTTR; quick-release → 15 min MTTR

6️⃣ **RCM optimizes strategy** — Different components need different maintenance approaches

7️⃣ **Preventive ≠ always best** — Predictive (condition-based) avoids replacing good components

════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **MAINTAINABILITY ENGINEERING CHEATSHEET COMPLETE**

**Created:** January 15, 2026  
**Coverage:** Maintainability fundamentals (MTTR, MDT, M(t)), design principles (accessibility, modularity, standardization, BIT, diagnostic coverage), maintenance strategies (corrective, preventive, predictive, RCM), MTTR optimization (detection, diagnosis, repair, recovery, verification), maintainability prediction (MIL-HDBK-472), logistics support analysis

════════════════════════════════════════════════════════════════════════════
