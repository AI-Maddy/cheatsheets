🔍 **Verification & Validation — Comprehensive Cheatsheet**
═══════════════════════════════════════════════════════════

**Context:** DO-178C compliance for airborne software systems  
**Focus:** Requirements-based testing, structural coverage, integration strategies  
**Target Audience:** V&V engineers, test managers, certification authorities

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — V&V IN 60 SECONDS**
─────────────────────────────────

**The Two Questions:**

✅ **Verification:** "Are we building the product **right**?"  
   → Does code implement requirements correctly?

✅ **Validation:** "Are we building the **right** product?"  
   → Do requirements meet stakeholder needs?

**Memorization Device: "Right vs. Right Product"**

.. code-block:: text

   Requirements ──────────► Design ──────────► Code
        │                      │                  │
        │ Validation           │ Verification     │ Verification
        ▼                      ▼                  ▼
   "Right product?"      "Correct design?"   "Bug-free code?"

**Key Coverage Metrics (DAL A):**

+-----------------+----------+-----------+-----------+
| Coverage Type   | DAL A    | DAL B     | DAL C     |
+=================+==========+===========+===========+
| **MC/DC**       | ✅ 100%  | ✅ 100%   | ❌ N/A    |
| **Decision**    | ✅ 100%  | ✅ 100%   | ✅ 100%   |
| **Statement**   | ✅ 100%  | ✅ 100%   | ✅ 100%   |
+-----------------+----------+-----------+-----------+

**The V-Model (Simplified):**

.. code-block:: text

   Requirements ◄──────────────────────► System Test
        ▼                                      ▲
   High-Level Design ◄────────────────► Integration Test
        ▼                                      ▲
   Low-Level Design ◄─────────────────► Module Test
        ▼                                      ▲
        └────────► Source Code ◄──────────────┘
                   (Unit Test)

════════════════════════════════════════════════════════════════════

📖 **1. VERIFICATION VS. VALIDATION — THE FUNDAMENTALS**
═════════════════════════════════════════════════════════

**IEEE Definitions:**

🔍 **Verification (IEEE 1012)**  
   "The process of evaluating a system or component to determine whether 
   the products of a given development phase satisfy the conditions 
   imposed at the start of that phase."

   **Translation:** Did we follow the blueprint correctly?

✅ **Validation (IEEE 1012)**  
   "The process of evaluating a system or component during or at the end 
   of the development process to determine whether it satisfies specified 
   requirements."

   **Translation:** Is this what the customer actually needs?

**Practical Examples:**

+--------------------------------+--------------------------------+
| Verification (Building Right)  | Validation (Right Product)     |
+================================+================================+
| Code review against low-level  | User acceptance test (UAT)     |
| requirements                   |                                |
+--------------------------------+--------------------------------+
| Traceability analysis          | Pilot-in-the-loop simulation   |
| (Req → Code → Test)            | (operational scenario)         |
+--------------------------------+--------------------------------+
| MC/DC coverage analysis        | Stakeholder review of HLR      |
| (100% for DAL A)               | (before design starts)         |
+--------------------------------+--------------------------------+
| Static code analysis           | Flight test campaign           |
| (MISRA C, Polyspace)           | (actual aircraft operation)    |
+--------------------------------+--------------------------------+

**Mnemonic: "VVVC" (Verify Validate Verify Code)**
- **V**alidate requirements (right product)
- **V**erify design (correct architecture)
- **V**erify code (implements design)
- **C**ertify system (regulatory acceptance)

════════════════════════════════════════════════════════════════════

🧪 **2. REQUIREMENTS-BASED TESTING**
════════════════════════════════════

**DO-178C Objective:** Every requirement must have at least one test case

**Test Case Structure (DO-178C Compliant):**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │ Test Case ID: TC-FCC-001                                │
   │ Requirement: REQ-FCC-123 "Autopilot engages at >500 ft" │
   │                                                          │
   │ Preconditions:                                          │
   │   • Aircraft on ground (altitude = 0 ft)                │
   │   • Engines running                                     │
   │   • Autopilot armed but not engaged                     │
   │                                                          │
   │ Test Steps:                                             │
   │   1. Takeoff and climb to 499 ft MSL                    │
   │   2. Press "AP ENGAGE" button                           │
   │   3. Verify autopilot does NOT engage (Expected)        │
   │   4. Continue climb to 500 ft MSL                       │
   │   5. Press "AP ENGAGE" button again                     │
   │   6. Verify autopilot ENGAGES (Expected)                │
   │                                                          │
   │ Expected Results:                                       │
   │   • Step 3: AP_STATUS = "ARMED" (not "ENGAGED")         │
   │   • Step 6: AP_STATUS = "ENGAGED"                       │
   │                                                          │
   │ Pass/Fail Criteria:                                     │
   │   PASS if both expected results match actual            │
   │   FAIL if autopilot engages below 500 ft                │
   │                                                          │
   │ Traceability:                                           │
   │   REQ-FCC-123 → LLR-FCC-456 → TC-FCC-001               │
   └─────────────────────────────────────────────────────────┘

**Coverage Matrix Example:**

+-------------+------------------+------------------+-----------+
| Requirement | Test Case        | Verification     | Status    |
|             |                  | Method           |           |
+=============+==================+==================+===========+
| REQ-FCC-123 | TC-FCC-001       | Test (T)         | ✅ Passed |
|             | TC-FCC-002       | Analysis (A)     | ✅ Passed |
+-------------+------------------+------------------+-----------+
| REQ-FCC-124 | TC-FCC-003       | Test (T)         | ⚠️ Review |
+-------------+------------------+------------------+-----------+
| REQ-FCC-125 | TC-FCC-004       | Inspection (I)   | ✅ Passed |
|             | TC-FCC-005       | Test (T)         | ✅ Passed |
+-------------+------------------+------------------+-----------+

**Verification Methods (DO-178C Table A-3):**

📝 **T (Test):**  
   Execute code with inputs, observe outputs

🔍 **I (Inspection):**  
   Manual review (e.g., code walk-through)

📊 **A (Analysis):**  
   Mathematical proof, simulation, timing analysis

🎯 **D (Demonstration):**  
   Qualitative check (e.g., GUI layout)

**Normal-Case vs. Robustness Testing:**

.. code-block:: text

   Normal Case:     Valid inputs → Expected outputs
   Example:         altitude = 500 ft → AP engages

   Robustness:      Invalid/edge inputs → Safe handling
   Example:         altitude = -999 ft → AP does NOT engage
                    altitude = NULL → Error logged, AP disabled

════════════════════════════════════════════════════════════════════

📊 **3. STRUCTURAL COVERAGE ANALYSIS**
═══════════════════════════════════════

**Coverage Hierarchy (Strictest to Weakest):**

.. code-block:: text

   MC/DC (Modified Condition/Decision Coverage)
     │
     ├─► Decision Coverage
     │      │
     │      └─► Branch Coverage
     │             │
     │             └─► Statement Coverage
     │                    │
     │                    └─► Function Coverage

**3.1 Statement Coverage**

**Definition:** Every executable statement runs at least once

**Example Code:**

.. code-block:: c

   void autopilot_engage(int altitude, bool button_pressed) {
       if (altitude > 500) {          // Line 1
           if (button_pressed) {      // Line 2
               engage_autopilot();    // Line 3
           }
       }
       log_status();                  // Line 4
   }

**Test Cases for 100% Statement Coverage:**

+----------+----------+------------------+-------------------+
| Test     | altitude | button_pressed   | Lines Executed    |
+==========+==========+==================+===================+
| TC1      | 600      | true             | 1, 2, 3, 4        |
| TC2      | 400      | false            | 1, 4              |
+----------+----------+------------------+-------------------+

**Result:** All 4 lines executed → ✅ 100% Statement Coverage

────────────────────────────────────────────────────────────────────

**3.2 Decision Coverage (Branch Coverage)**

**Definition:** Each boolean expression evaluates to both TRUE and FALSE

**Test Cases for 100% Decision Coverage:**

+----------+----------+------------------+-------------------+
| Test     | altitude | button_pressed   | Decisions         |
+==========+==========+==================+===================+
| TC1      | 600      | true             | (L1=T, L2=T)      |
| TC2      | 400      | false            | (L1=F)            |
| TC3      | 600      | false            | (L2=F)            |
+----------+----------+------------------+-------------------+

**Result:**  
- Line 1: T (TC1) and F (TC2) → ✅  
- Line 2: T (TC1) and F (TC3) → ✅  
→ **100% Decision Coverage**

────────────────────────────────────────────────────────────────────

**3.3 MC/DC (Modified Condition/Decision Coverage)**

**Definition:** Each condition in a decision independently affects the outcome

**Complex Example:**

.. code-block:: c

   // Autopilot engages if:
   // altitude > 500 AND button_pressed AND NOT hydraulic_fail
   
   if (altitude > 500 && button_pressed && !hydraulic_fail) {
       engage_autopilot();
   }

**Conditions:**
- A: altitude > 500
- B: button_pressed
- C: !hydraulic_fail

**Decision:** D = A AND B AND C

**MC/DC Test Matrix:**

+----+---+---+---+---+------------------------+
| TC | A | B | C | D | Independence Check     |
+====+===+===+===+===+========================+
| 1  | T | T | T | T | (baseline TRUE)        |
+----+---+---+---+---+------------------------+
| 2  | F | T | T | F | A alone changed D      |
|    |   |   |   |   | (proves A's influence) |
+----+---+---+---+---+------------------------+
| 3  | T | F | T | F | B alone changed D      |
+----+---+---+---+---+------------------------+
| 4  | T | T | F | F | C alone changed D      |
+----+---+---+---+---+------------------------+

**Minimum MC/DC Tests: N+1 (where N = # of conditions)**  
For 3 conditions → 4 test cases minimum

**MC/DC Visualization:**

.. code-block:: text

   Condition A flips:
   TC1: (T,T,T) → D=T  }
   TC2: (F,T,T) → D=F  }─► A independently affects D ✅

   Condition B flips:
   TC1: (T,T,T) → D=T  }
   TC3: (T,F,T) → D=F  }─► B independently affects D ✅

   Condition C flips:
   TC1: (T,T,T) → D=T  }
   TC4: (T,T,F) → D=F  }─► C independently affects D ✅

**Why MC/DC for DAL A?**

💀 **Without MC/DC:** Bug could hide in untested condition combinations  
✅ **With MC/DC:** Every condition proven to matter independently

════════════════════════════════════════════════════════════════════

🧰 **4. COVERAGE TOOLS & AUTOMATION**
═════════════════════════════════════

**Tool Qualification (DO-178C §12.2):**

.. code-block:: text

   Coverage Tool (e.g., VectorCAST, LDRA)
       │
       ├─► Tool Qualification Level (TQL)
       │   └─► TQL-1: Tool output used as DO-178C evidence
       │       (requires Tool Qualification Data Package)
       │
       └─► Verification Methods
           ├─► Tool Operational Requirements (TOR)
           ├─► Test cases for tool itself
           └─► Service history / conformity review

**Popular Coverage Tools:**

🛠️ **VectorCAST (Vector Software)**  
   - MC/DC, statement, branch coverage
   - Automated test harness generation
   - DO-178C qualified (TQL-1 compliant)

🛠️ **LDRA Testbed**  
   - Static + dynamic analysis
   - MISRA C/C++ checking
   - Coverage visualization

🛠️ **Rapita Verification Suite (RVS)**  
   - Timing analysis + coverage
   - Target hardware support (PowerPC, ARM)

🛠️ **CTC++ (Testwell)**  
   - Embedded C/C++ coverage
   - Host-target cross-compilation

**Tool Workflow Example:**

.. code-block:: bash

   # Step 1: Instrument source code
   vectorcast instrument autopilot.c -o autopilot_inst.c
   
   # Step 2: Compile instrumented code
   gcc autopilot_inst.c -o autopilot_test
   
   # Step 3: Run test cases
   ./autopilot_test < test_inputs.txt
   
   # Step 4: Generate coverage report
   vectorcast report --format html --mcdc
   
   # Output: coverage_report.html
   # Shows: 100% MC/DC (24/24 conditions tested)

════════════════════════════════════════════════════════════════════

🔬 **5. INTEGRATION TESTING STRATEGIES**
════════════════════════════════════════

**Integration Levels (Bottom-Up):**

.. code-block:: text

   Level 1: Module/Unit Test
       ├─► Individual functions tested in isolation
       └─► Stubs for dependencies
   
   Level 2: Component Integration
       ├─► Multiple modules combined
       └─► Test interfaces between components
   
   Level 3: Subsystem Integration
       ├─► Major subsystems (e.g., FCC + sensors)
       └─► Hardware-in-the-loop (HIL) testing
   
   Level 4: System Integration
       ├─► Complete aircraft system
       └─► Iron-bird rig or flight test

**Integration Approaches:**

**A. Big Bang Integration ❌ (Not recommended for safety-critical)**

.. code-block:: text

   All modules → Integrate at once → Hope it works
   Problem: Too many variables, hard to isolate bugs

**B. Incremental Integration ✅ (DO-178C preferred)**

.. code-block:: text

   Module A ──┐
              ├─► Test A+B ──┐
   Module B ──┘              ├─► Test A+B+C ──► ...
                             │
   Module C ─────────────────┘

**C. Sandwich Integration (Hybrid)**

.. code-block:: text

   Top-Down:    GUI → Controller → (stubs)
   Bottom-Up:   (drivers) → Sensors → Actuators
   Middle:      Join the two layers at integration test

**Example: Flight Control Computer Integration**

.. code-block:: text

   Step 1: Unit Test
       ├─► pitch_controller() tested with stubs
       ├─► roll_controller() tested with stubs
       └─► yaw_controller() tested with stubs
   
   Step 2: Component Integration
       ├─► Combine pitch + roll + yaw controllers
       ├─► Test with simulated sensor inputs
       └─► Verify control law coordination
   
   Step 3: Subsystem Integration (HIL)
       ├─► Real sensors (IMU, GPS, air data)
       ├─► Real actuators (servo motors)
       └─► Test in iron-bird rig (6DOF motion platform)
   
   Step 4: System Integration (Flight Test)
       ├─► Install in actual aircraft
       ├─► Test envelope expansion (low speed → high speed)
       └─► Certification authority witnessed flights

════════════════════════════════════════════════════════════════════

🎯 **6. TRACEABILITY — THE GOLDEN THREAD**
═══════════════════════════════════════════

**Bi-Directional Traceability (DO-178C §6.3):**

.. code-block:: text

   Stakeholder Needs
         ↕
   System Requirements (HLR)
         ↕
   Software High-Level Requirements (HLR)
         ↕
   Software Low-Level Requirements (LLR)
         ↕
   Source Code
         ↕
   Test Cases
         ↕
   Test Results

**Forward Traceability:**  
HLR → LLR → Code → Test Cases  
*Proves: "Every requirement is implemented and tested"*

**Backward Traceability:**  
Test Cases → Code → LLR → HLR  
*Proves: "No orphan code (untraceable to requirements)"*

**Example Traceability Matrix:**

+---------+---------+--------------+--------------+-----------+
| HLR     | LLR     | Source File  | Test Case    | Status    |
+=========+=========+==============+==============+===========+
| HLR-001 | LLR-023 | autopilot.c  | TC-AP-001    | ✅ Passed |
|         | LLR-024 | autopilot.c  | TC-AP-002    | ✅ Passed |
+---------+---------+--------------+--------------+-----------+
| HLR-002 | LLR-025 | navigation.c | TC-NAV-001   | ⚠️ Failed |
+---------+---------+--------------+--------------+-----------+

**Orphan Detection:**

.. code-block:: sql

   -- Find code not traced to requirements
   SELECT source_file, function_name 
   FROM source_code 
   WHERE function_name NOT IN (SELECT code_ref FROM traceability);
   
   -- Result: Warning! Potential dead code or undocumented feature

════════════════════════════════════════════════════════════════════

⚠️ **7. COMMON V&V PITFALLS**
══════════════════════════════

❌ **Pitfall 1: "We have 100% code coverage, we're done!"**

**Problem:** Code coverage ≠ requirements coverage

**Example:**  
✅ Every line executed  
❌ But missing test for "autopilot should NOT engage below 500 ft"

**Solution:** Requirements-based testing FIRST, then verify coverage

────────────────────────────────────────────────────────────────────

❌ **Pitfall 2: Writing tests after code is frozen**

**Problem:** Tests become "verification theater" (just to pass)

**Solution:** Test-Driven Development (TDD) for DO-178C:
1. Write requirement
2. Write test case (expected to fail initially)
3. Write code to pass the test
4. Refactor code, test remains stable

────────────────────────────────────────────────────────────────────

❌ **Pitfall 3: Ignoring equivalence partitioning**

**Problem:** Testing 500, 501, 502 ft individually (redundant)

**Solution:** Partition input space:

.. code-block:: text

   Partition 1: altitude < 500 (invalid)
   Partition 2: altitude = 500 (boundary)
   Partition 3: altitude > 500 (valid)
   
   Test: One case per partition + boundaries

────────────────────────────────────────────────────────────────────

❌ **Pitfall 4: Not testing failure modes**

**Problem:** Only testing happy path (normal operation)

**Solution:** Robustness testing:
- Sensor failure (GPS unavailable)
- Communication timeout (CAN bus down)
- Out-of-range values (altitude = -99999)

────────────────────────────────────────────────────────────────────

❌ **Pitfall 5: Using modified code for coverage**

**Problem:** Developer tweaks code to hit 100% coverage

**Solution:** Configuration management:
- Coverage measured on BASELINED code
- No changes allowed without CCB approval
- Version control (Git tags for DO-178C releases)

════════════════════════════════════════════════════════════════════

🛠️ **8. PRACTICAL V&V WORKFLOW (DAL C Example)**
═════════════════════════════════════════════════

**Project:** Cabin Pressure Controller (DAL C)

**Phase 1: Requirements Analysis**

.. code-block:: text

   1. Receive System Requirements from aircraft OEM
   2. Derive Software High-Level Requirements (HLR)
      Example: "System shall maintain 8,000 ft cabin alt at 41,000 ft cruise"
   3. Validation: Stakeholder review (engineers + pilots)
   4. Traceability: Map HLR to System Req

**Phase 2: Design & Low-Level Requirements**

.. code-block:: text

   1. Create software architecture (control loop diagram)
   2. Derive Low-Level Requirements (LLR)
      Example: "PID controller shall run at 10 Hz"
   3. Verification: Design review, analysis
   4. Traceability: Map LLR to HLR

**Phase 3: Coding**

.. code-block:: text

   1. Implement LLR in C (MISRA C:2012 compliant)
   2. Peer code review (at least 2 reviewers)
   3. Static analysis (Polyspace, Coverity)
   4. Traceability: Map code to LLR

**Phase 4: Unit Testing**

.. code-block:: text

   1. Write test cases for each LLR
   2. Run tests with instrumented code (VectorCAST)
   3. Measure coverage:
      ✅ Statement: 100%
      ✅ Decision: 100%
      ❌ MC/DC: Not required for DAL C
   4. Traceability: Map tests to LLR

**Phase 5: Integration Testing**

.. code-block:: text

   1. Integrate with pressure sensors + outflow valves
   2. Hardware-in-the-loop (HIL) rig testing
   3. Test scenarios:
      - Normal climb to cruise
      - Emergency descent
      - Dual sensor failure
   4. Traceability: Map tests to HLR

**Phase 6: Certification**

.. code-block:: text

   1. Generate DO-178C deliverables:
      - Software Accomplishment Summary (SAS)
      - Software Configuration Index (SCI)
      - Problem reports log
      - Traceability matrices
   2. DER (Designated Engineering Representative) review
   3. FAA/EASA approval

════════════════════════════════════════════════════════════════════

📇 **9. QUICK REFERENCE CARD**
═══════════════════════════════

**Coverage Requirements by DAL:**

+------------+-----------+----------+----------+----------+
| DAL Level  | Statement | Decision | MC/DC    | Priority |
+============+===========+==========+==========+==========+
| **A**      | ✅ 100%   | ✅ 100%  | ✅ 100%  | Highest  |
| **B**      | ✅ 100%   | ✅ 100%  | ✅ 100%  | High     |
| **C**      | ✅ 100%   | ✅ 100%  | ❌ N/A   | Medium   |
| **D**      | ✅ 100%   | ⚠️ Goal  | ❌ N/A   | Low      |
| **E**      | ⚠️ Goal   | ❌ N/A   | ❌ N/A   | Minimal  |
+------------+-----------+----------+----------+----------+

**Verification Methods (DO-178C):**

- **T (Test):** Execute code, observe results
- **I (Inspection):** Manual review (peer, walkthrough)
- **A (Analysis):** Mathematical proof, timing calculation
- **D (Demonstration):** Qualitative check (GUI, cosmetic)

**MC/DC Formula:**

Minimum test cases = N + 1 (where N = # of conditions)

**Traceability Chain:**

.. code-block:: text

   System Req → HLR → LLR → Code → Unit Test → Integration Test

════════════════════════════════════════════════════════════════════

📝 **10. EXAM QUESTIONS**
═════════════════════════

**Q1:** What is the difference between verification and validation?

**A1:**  
- **Verification:** "Are we building the product **right**?" (implementation correctness)
- **Validation:** "Are we building the **right** product?" (requirements correctness)

Example: Verification checks if code matches LLR. Validation checks if HLR meets stakeholder needs.

────────────────────────────────────────────────────────────────────

**Q2:** For DAL A software, you have a condition `(A && B && C)`. How many minimum test cases are needed for MC/DC?

**A2:** **4 test cases** (N+1 rule, where N=3 conditions).  
Each test must independently toggle one condition while holding others constant to prove that condition affects the decision outcome.

────────────────────────────────────────────────────────────────────

**Q3:** Your code has 100% statement coverage but a bug still escapes. Why?

**A3:** Statement coverage does NOT guarantee:
- Both TRUE and FALSE branches tested (need decision coverage)
- Independent condition testing (need MC/DC for DAL A/B)
- Requirements coverage (need requirements-based tests)

Example: `if (A && B)` might only be tested with A=T, B=T, missing the case where A=F.

────────────────────────────────────────────────────────────────────

**Q4:** What is bi-directional traceability and why is it required?

**A4:**  
- **Forward:** HLR → LLR → Code → Tests (proves all requirements implemented)
- **Backward:** Tests → Code → LLR → HLR (proves no orphan code)

Required by DO-178C §6.3 to demonstrate complete coverage and prevent undocumented features.

────────────────────────────────────────────────────────────────────

**Q5:** When is tool qualification (TQL-1) required for a coverage analyzer?

**A5:** When the tool's output is used as **DO-178C certification evidence** without independent verification. If the DER (Designated Engineering Representative) relies on VectorCAST's MC/DC report, the tool must have a Tool Qualification Data Package proving its correctness.

Alternative: Manually verify a sample of coverage results (but impractical for large projects).

════════════════════════════════════════════════════════════════════

📚 **11. FURTHER READING**
═══════════════════════════

**Standards:**

📜 **RTCA DO-178C / EUROCAE ED-12C**  
   Software Considerations in Airborne Systems (2011)  
   https://www.rtca.org/content/standards-documents

📜 **ISO 26262-6** (Automotive equivalent)  
   Product development at the software level

📜 **IEC 61508-3** (Industrial functional safety)  
   Software requirements for safety-related systems

**Books:**

📖 *"DO-178C / ED-12C Explained"* — Leanna Rierson  
📖 *"Software Testing and Continuous Quality Improvement"* — Burnstein  
📖 *"Practical Software Testing"* — Ilene Burnstein

**Papers:**

📄 "MC/DC vs. Decision Coverage: Empirical Study" (IEEE Aerospace 2015)  
📄 "Traceability in Safety-Critical Systems" (SafeComp 2018)

**Training:**

🎓 **AFuzion DO-178C Training** (5-day course, includes V&V module)  
🎓 **Rapita Systems Coverage Analysis Workshop**  
🎓 **Vector Software VectorCAST Certification**

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Understand verification vs. validation (two-question test)
- [ ] Memorize coverage requirements for DAL A/B/C
- [ ] Calculate MC/DC test cases (N+1 formula)
- [ ] Explain bi-directional traceability
- [ ] List 4 verification methods (T, I, A, D)
- [ ] Describe integration testing strategies
- [ ] Identify tool qualification criteria (TQL-1)
- [ ] Recognize common V&V pitfalls (5 listed)

════════════════════════════════════════════════════════════════════

🎓 **MEMORABLE ANALOGIES**
═══════════════════════════

**Verification = Building Inspector**  
- Checks if house matches blueprints (code matches design)

**Validation = Homeowner Walkthrough**  
- Checks if house meets family needs (requirements meet stakeholder intent)

**MC/DC = Circuit Breaker Testing**  
- Must prove each breaker independently trips the system

**Traceability = Supply Chain Tracking**  
- Follow coffee bean from farm → roaster → cafe → cup

**100% Coverage = No Dark Corners**  
- Every room in the house has been walked through (but doesn't guarantee furniture is correct!)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **V&V ≠ Just Testing:**  
   Verification includes reviews, analysis, inspections (not just test execution)

2️⃣ **Requirements-Based Testing Comes First:**  
   Coverage is a verification activity, not a test design method

3️⃣ **MC/DC is Expensive but Necessary:**  
   For DAL A/B, MC/DC catches bugs that decision coverage misses

4️⃣ **Traceability is Your Legal Defense:**  
   In an accident investigation, traceability proves due diligence

5️⃣ **Tool Qualification is NOT Optional:**  
   If FAA relies on your tool, the tool needs its own certification

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **COMPREHENSIVE V&V GUIDE COMPLETE**  
**Created:** January 14, 2026  
**Next Steps:** Apply to actual project, customize for specific DAL level

════════════════════════════════════════════════════════════════════
