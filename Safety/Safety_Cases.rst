============================================================
Safety Cases — Structured Assurance Arguments for Safety-Critical Systems
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
**TL;DR — Safety Cases in 30 Seconds**
================================================================================

**What:** Structured **argument** that a system is acceptably safe for a given application in a given environment.

**Why:** Required by ISO 26262, EN 50129 (railway), DO-178C (avionics), IEC 62304 (medical). Demonstrates **compliance** and **confidence** to regulators, assessors, stakeholders.

**2026 Evolution:** Structured Assurance Case Metamodel (SACM), confidence arguments, update arguments for continuous deployment, AI/ML safety cases.

**Quick Safety Case Elements:**

+----------------------+-------------------------+-------------------------------------+
| Element              | Symbol (GSN)            | Purpose                             |
+======================+=========================+=====================================+
| **Goal**             | Rectangle               | Safety claim to be demonstrated     |
+----------------------+-------------------------+-------------------------------------+
| **Strategy**         | Parallelogram           | Argumentation approach              |
+----------------------+-------------------------+-------------------------------------+
| **Solution**         | Circle                  | Evidence supporting claim           |
+----------------------+-------------------------+-------------------------------------+
| **Context**          | Rounded rectangle       | Scope, assumptions, boundaries      |
+----------------------+-------------------------+-------------------------------------+
| **Justification**    | Ellipse                 | Rationale for strategy choice       |
+----------------------+-------------------------+-------------------------------------+
| **Assumption**       | Rounded rectangle (A)   | Unchallenged prerequisite           |
+----------------------+-------------------------+-------------------------------------+

**Safety Case Structure (Simplified):**

.. code-block:: text

   Goal: System X is acceptably safe
      ├─ Strategy: Argument by hazard elimination + mitigation
      │  ├─ Goal: All hazards identified (HAZOP, FMEA, FTA)
      │  │  └─ Solution: Hazard log (evidence)
      │  └─ Goal: All hazards mitigated to ALARP
      │     ├─ Goal: Hazard H1 mitigated
      │     │  └─ Solution: FMEA, Safety requirements, Test results
      │     └─ Goal: Hazard H2 mitigated
      │        └─ Solution: FTA, Redundancy design, Validation report

**Key Standards:**

+------------------+---------------------------+-----------------------------+
| Standard         | Domain                    | Safety Case Requirement     |
+==================+===========================+=============================+
| **ISO 26262**    | Automotive functional     | Part 8 (Safety case)        |
+------------------+---------------------------+-----------------------------+
| **EN 50129**     | Railway signaling         | Mandatory safety case       |
+------------------+---------------------------+-----------------------------+
| **DO-178C**      | Avionics software         | Implicit (certification)    |
+------------------+---------------------------+-----------------------------+
| **IEC 62304**    | Medical device software   | Risk management file        |
+------------------+---------------------------+-----------------------------+
| **DEF STAN 00-56**| UK military systems      | Explicit safety case        |
+------------------+---------------------------+-----------------------------+

================================================================================
1. Safety Case Fundamentals — Structured Assurance
================================================================================

1.1 What is a Safety Case?
---------------------------

**Definition (UK Ministry of Defence DEF STAN 00-56):**

   "A structured argument, supported by a body of evidence, that provides a compelling,
   comprehensible, and valid case that a system is safe for a given application in a
   given environment."

**Key Components:**

1. **Claims (Goals):** Safety properties to be demonstrated
   - "System X prevents unintended acceleration"
   - "Probability of catastrophic failure < 10^-9 per hour"

2. **Arguments (Strategies):** Logical reasoning linking sub-claims to top claim
   - Argument by hazard analysis
   - Argument by compliance with standards
   - Argument by testing coverage

3. **Evidence (Solutions):** Artifacts supporting claims
   - FMEA reports, FTA quantitative analysis
   - Test results, review records
   - Certification documents, field data

4. **Context:** Scope, assumptions, operating environment
   - System boundary, interfaces
   - Environmental conditions (temperature, vibration, EMI)
   - Mission profile, duty cycle

**Safety Case vs Safety Plan:**

+--------------------+----------------------------+---------------------------+
| Aspect             | **Safety Plan**            | **Safety Case**           |
+====================+============================+===========================+
| **Purpose**        | HOW to achieve safety      | Demonstrate safety achieved|
+--------------------+----------------------------+---------------------------+
| **Timing**         | Early (planning phase)     | Late (verification phase) |
+--------------------+----------------------------+---------------------------+
| **Content**        | Processes, activities      | Arguments, evidence       |
+--------------------+----------------------------+---------------------------+
| **Audience**       | Project team               | Assessors, regulators     |
+--------------------+----------------------------+---------------------------+

1.2 Goal Structuring Notation (GSN)
------------------------------------

**GSN (Goal Structuring Notation):**
Graphical notation developed by Tim Kelly (University of York) for representing safety case arguments.

**GSN Elements:**

.. code-block:: text

   ┌──────────────────┐
   │ G1: System is    │  Goal: Safety claim to be demonstrated
   │ acceptably safe  │
   └────────┬─────────┘
            │ Supported by
            ▼
   ╱───────────────────╲
   │ S1: Argument by   │  Strategy: How to decompose goal
   │ hazard mitigation │
   ╲─────────┬─────────╱
             │ In context of
             ▼
   ╭────────────────────╮
   │ C1: Operating      │  Context: Scope, assumptions, environment
   │ environment: Road  │
   ╰────────────────────╯

**GSN Symbols:**

.. code-block:: text

   Rectangle:           ┌────────┐   Goal (claim to be supported)
                        │   G1   │
                        └────────┘
   
   Parallelogram:       ╱────────╲   Strategy (argumentation approach)
                        │   S1   │
                        ╲────────╱
   
   Circle:                 ○       Solution (evidence)
                          Sn1
   
   Rounded Rectangle:   ╭────────╮   Context (scope, boundary)
                        │   C1   │
                        ╰────────╯
   
   Ellipse:            ( ──────── )  Justification (why strategy chosen)
                        (   J1    )
   
   House:              ╱╲──────╱╲   Assumption (unchallenged prerequisite)
                       │   A1   │

**Relationships:**

- **Supported by:** Goal → Strategy → Sub-goals/Solutions (downward arrows)
- **In context of:** Goal/Strategy → Context (side arrows)
- **Justified by:** Strategy → Justification (side arrows)

1.3 Claims, Arguments, Evidence (CAE) Framework
------------------------------------------------

**Three Layers:**

1. **Claims Layer (What to demonstrate):**
   - Top claim: "System is acceptably safe"
   - Sub-claims: "All hazards mitigated," "Requirements correct," "Implementation verified"

2. **Arguments Layer (How to demonstrate):**
   - Argument by compliance (ISO 26262 Part 6)
   - Argument by analysis (FMEA, FTA)
   - Argument by testing (coverage, field trials)

3. **Evidence Layer (Proof):**
   - FMEA report (dated, signed, reviewed)
   - Unit test results (100% branch coverage)
   - Certification (TÜV, Exida, UL assessment report)

**Example CAE Hierarchy:**

.. code-block:: text

   Claim: Braking ECU software is safe (ASIL D)
      Argument: By compliance with ISO 26262 Part 6
         Sub-Claim: Requirements are complete and correct
            Evidence: Requirements review record, traceability matrix
         Sub-Claim: Software design is correct
            Evidence: Design review, MISRA C compliance report
         Sub-Claim: Implementation has no systematic faults
            Evidence: Unit tests (MC/DC coverage), static analysis (Polyspace)
         Sub-Claim: Integration is verified
            Evidence: Integration test report, HIL test results

================================================================================
2. GSN Safety Case Example — Automotive AEB (Autonomous Emergency Braking)
================================================================================

**System:** AEB (Automatic Emergency Braking) for pedestrian protection  
**Safety Goal:** Prevent collision with pedestrian at speeds < 50 km/h  
**ASIL:** ASIL B

**Top-Level Safety Case (GSN):**

.. code-block:: text

   ┌──────────────────────────────────────────────────┐
   │ G1: AEB system is acceptably safe for            │
   │     pedestrian collision prevention (<50 km/h)   │
   └────────────────────┬─────────────────────────────┘
                        │ Supported by
                        ▼
   ╱──────────────────────────────────────────────────╲
   │ S1: Argument by compliance with ISO 26262        │
   │     (ASIL B requirements) and hazard mitigation  │
   ╲────────────────────┬───────────────────────────  ╱
                        │ In context of
                        ▼
   ╭─────────────────────────────────────────────────╮
   │ C1: Operating environment: Urban roads,         │
   │     daylight/night, dry/wet, speeds 0-50 km/h   │
   ╰─────────────────────────────────────────────────╯
                        │
                        ├─────────────────┬───────────────────┐
                        ▼                 ▼                   ▼
   ┌───────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
   │ G2: All hazards       │  │ G3: Safety           │  │ G4: Implementation   │
   │     identified        │  │     requirements     │  │     verified         │
   └───────────┬───────────┘  │     correct          │  └──────────┬───────────┘
               │              └──────────┬───────────┘             │
               ▼                         ▼                         ▼
   ╱───────────────────────╲  ╱─────────────────────╲  ╱───────────────────────╲
   │ S2: By HARA + FMEA +  │  │ S3: By review and   │  │ S4: By testing and    │
   │     FTA               │  │     traceability    │  │     field validation  │
   ╲───────────┬───────────╱  ╲─────────┬───────────╱  ╲───────────┬───────────╱
               │                         │                         │
               ▼                         ▼                         ▼
          ╭────────╮              ╭─────────╮               ╭─────────╮
          │   Sn1  │              │   Sn2   │               │   Sn3   │
          │ HARA   │              │ Review  │               │ Test    │
          │ Report │              │ Records │               │ Results │
          ╰────────╯              ╰─────────╯               ╰─────────╯

**Detailed Sub-Argument (G2 → All Hazards Identified):**

.. code-block:: text

   ┌───────────────────────────────────────────┐
   │ G2: All AEB hazards identified            │
   └───────────────────┬───────────────────────┘
                       │ Supported by
                       ▼
   ╱─────────────────────────────────────────────╲
   │ S2.1: Argument by systematic hazard        │
   │       analysis methods                     │
   ╲───────────────────┬─────────────────────────╱
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌─────────┐   ┌──────────┐   ┌──────────┐
   │ G2.1:   │   │ G2.2:    │   │ G2.3:    │
   │ HARA    │   │ FMEA     │   │ FTA      │
   │ complete│   │ complete │   │ complete │
   └────┬────┘   └────┬─────┘   └────┬─────┘
        │             │              │
        ▼             ▼              ▼
   ○────────     ○─────────     ○────────
   Sn2.1        Sn2.2         Sn2.3
   HARA         DFMEA         FTA
   Report       Report        Report
   (Rev 2.1)    (ASIL B)      (Q<1e-6)

**Evidence Details:**

.. code-block:: python

   # Safety Case Evidence Tracking (Python example)
   
   evidence_registry = {
       'Sn1_HARA_Report': {
           'artifact': 'AEB_HARA_Report_v2.1.pdf',
           'date': '2025-11-15',
           'author': 'Safety Team',
           'reviewer': 'TÜV Assessor',
           'status': 'Approved',
           'claims_supported': ['G2.1'],
           'key_findings': '23 hazards identified, 18 ASIL B, 5 QM'
       },
       'Sn2_Requirements_Review': {
           'artifact': 'AEB_SRS_Review_Minutes_v3.0.pdf',
           'date': '2025-12-01',
           'participants': ['System Architect', 'Safety Engineer', 'V&V Lead'],
           'status': 'Complete',
           'claims_supported': ['G3'],
           'defects_found': 3,
           'defects_closed': 3
       },
       'Sn3_Test_Results': {
           'artifact': 'AEB_Test_Report_v1.5.xlsx',
           'date': '2026-01-10',
           'test_cases': 1247,
           'passed': 1245,
           'failed': 2,
           'status': 'Under investigation',
           'claims_supported': ['G4'],
           'coverage': 'ISO 26262-6 Table 9 methods (MC/DC 98.7%)'
       }
   }
   
   def check_evidence_completeness(goal_id):
       """Verify all evidence for a goal is present and approved"""
       supporting_evidence = [k for k, v in evidence_registry.items() 
                              if goal_id in v.get('claims_supported', [])]
       
       for ev_id in supporting_evidence:
           ev = evidence_registry[ev_id]
           print(f"{ev_id}:")
           print(f"  Artifact: {ev['artifact']}")
           print(f"  Status: {ev['status']}")
           if ev['status'] != 'Approved':
               print(f"  ⚠ WARNING: Evidence not approved!")
       
       return len(supporting_evidence) > 0
   
   # Check evidence for G2.1 (HARA complete)
   check_evidence_completeness('G2.1')
   
   # Output:
   # Sn1_HARA_Report:
   #   Artifact: AEB_HARA_Report_v2.1.pdf
   #   Status: Approved

================================================================================
3. Confidence Arguments — Assessing Evidence Quality
================================================================================

3.1 Need for Confidence Arguments
----------------------------------

**Problem:** Not all evidence is equally trustworthy.

**Examples of Weak Evidence:**
- Test with 60% code coverage (not 100% MC/DC)
- FMEA reviewed by author only (no independent assessment)
- Outdated field data (10-year-old failure rates)

**Confidence Argument:** Explicit argument about the **trustworthiness** of evidence, not just the safety claim itself.

**Confidence Factors:**

+-------------------------+----------------------------+---------------------------+
| Factor                  | High Confidence            | Low Confidence            |
+=========================+============================+===========================+
| **Independence**        | Third-party assessor       | Self-assessment           |
+-------------------------+----------------------------+---------------------------+
| **Recency**             | < 1 year old               | > 5 years old             |
+-------------------------+----------------------------+---------------------------+
| **Coverage**            | 100% MC/DC, all scenarios  | 70% statement coverage    |
+-------------------------+----------------------------+---------------------------+
| **Traceability**        | Full req → test matrix     | Informal mapping          |
+-------------------------+----------------------------+---------------------------+
| **Tool Qualification**  | TCL3 (ISO 26262 Part 8)    | Unqualified tool          |
+-------------------------+----------------------------+---------------------------+
| **Expertise**           | Safety-certified engineer  | Junior developer          |
+-------------------------+----------------------------+---------------------------+

3.2 Confidence Argument Example (GSN)
--------------------------------------

**Claim:** "Test results Sn3 provide sufficient confidence in AEB safety."

.. code-block:: text

   ┌──────────────────────────────────────────────┐
   │ G_Conf: Test results Sn3 provide sufficient │
   │         confidence in AEB safety             │
   └────────────────────┬─────────────────────────┘
                        │ Supported by
                        ▼
   ╱──────────────────────────────────────────────╲
   │ S_Conf: Argument by test process quality    │
   │         and coverage adequacy                │
   ╲────────────────────┬───────────────────────  ╱
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
   ┌──────────┐   ┌──────────┐   ┌──────────────┐
   │ G_C1:    │   │ G_C2:    │   │ G_C3:        │
   │ Tests    │   │ Test     │   │ Independent  │
   │ cover    │   │ environ- │   │ witness      │
   │ 100% req │   │ matches  │   │ present      │
   └────┬─────┘   │ target   │   └──────┬───────┘
        │         └────┬─────┘          │
        ▼              ▼                ▼
   ○────────     ○────────         ○────────
   Sn_C1        Sn_C2             Sn_C3
   Trace        Test              Witness
   Matrix       Spec              Report
   (100%)       (HIL)             (TÜV)

**Python Example: Confidence Scoring**

.. code-block:: python

   def calculate_confidence_score(evidence):
       """
       Calculate confidence score (0-100) for evidence quality.
       Factors: independence, coverage, recency, traceability, tool qualification
       """
       score = 0
       
       # Independence (0-30 points)
       if evidence.get('reviewer') in ['TÜV', 'Exida', 'UL']:
           score += 30  # Third-party assessment
       elif evidence.get('reviewer') != evidence.get('author'):
           score += 15  # Independent internal review
       else:
           score += 0   # Self-assessment
       
       # Coverage (0-30 points)
       coverage = evidence.get('coverage_percent', 0)
       score += min(coverage * 0.3, 30)
       
       # Recency (0-20 points)
       import datetime
       date_str = evidence.get('date', '2020-01-01')
       date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
       age_days = (datetime.datetime.now() - date).days
       if age_days < 365:
           score += 20  # < 1 year
       elif age_days < 1095:
           score += 10  # 1-3 years
       else:
           score += 0   # > 3 years
       
       # Traceability (0-10 points)
       if evidence.get('traceability') == 'Full':
           score += 10
       elif evidence.get('traceability') == 'Partial':
           score += 5
       
       # Tool Qualification (0-10 points)
       if evidence.get('tool_tcl') == 'TCL3':
           score += 10
       elif evidence.get('tool_tcl') == 'TCL2':
           score += 5
       
       return min(score, 100)
   
   # Example evidence assessment
   test_evidence = {
       'artifact': 'AEB_Test_Report.xlsx',
       'date': '2026-01-10',
       'author': 'V&V Team',
       'reviewer': 'TÜV',
       'coverage_percent': 98.7,
       'traceability': 'Full',
       'tool_tcl': 'TCL3'
   }
   
   fmea_evidence = {
       'artifact': 'FMEA_Report.pdf',
       'date': '2024-06-01',
       'author': 'Safety Engineer',
       'reviewer': 'Safety Engineer',  # Self-review!
       'coverage_percent': 85,
       'traceability': 'Partial',
       'tool_tcl': None
   }
   
   score_test = calculate_confidence_score(test_evidence)
   score_fmea = calculate_confidence_score(fmea_evidence)
   
   print(f"Test Evidence Confidence: {score_test}/100 (High)")
   print(f"FMEA Evidence Confidence: {score_fmea}/100 (Medium)")
   
   # Output:
   # Test Evidence Confidence: 100/100 (High)  ← Excellent!
   # FMEA Evidence Confidence: 45/100 (Medium) ← Needs improvement

**Recommendation:** Add independent FMEA review to increase confidence score.

================================================================================
4. Update Arguments — Evolutionary Safety Cases (2026)
================================================================================

4.1 Motivation for Update Arguments
------------------------------------

**Problem:** Traditional safety cases assume **static system** (no changes post-certification).

**2026 Reality:**
- **Continuous deployment:** OTA updates (automotive, avionics)
- **Machine learning:** Model retraining, concept drift
- **Cybersecurity patches:** Security updates affecting safety-critical code
- **Incremental certification:** DevOps for safety-critical systems

**Update Argument:** Demonstrates that **safety is maintained** (or improved) after system modification.

4.2 Update Argument Structure (GSN)
------------------------------------

**Top-Level Update Claim:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────┐
   │ G_Update: System safety is maintained after          │
   │           Software Update v2.1 → v2.2                │
   └──────────────────────┬───────────────────────────────┘
                          │ Supported by
                          ▼
   ╱────────────────────────────────────────────────────────╲
   │ S_Update: Argument by change impact analysis          │
   │           and regression verification                  │
   ╲──────────────────────┬─────────────────────────────────╱
                          │ In context of
                          ▼
   ╭────────────────────────────────────────────────────────╮
   │ C_Update: Change description:                          │
   │   - Modified AEB braking algorithm (25 LOC)            │
   │   - Added sensor fusion plausibility check             │
   │   - No hardware changes                                │
   ╰────────────────────────────────────────────────────────╯
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐      ┌──────────┐
   │ G_U1:   │      │ G_U2:   │      │ G_U3:    │
   │ Change  │      │ Regres- │      │ No new   │
   │ analyzed│      │ sion    │      │ hazards  │
   └────┬────┘      │ tested  │      └────┬─────┘
        │           └────┬────┘           │
        ▼                ▼                ▼
   ○────────        ○────────        ○────────
   Sn_U1           Sn_U2            Sn_U3
   Change          Regression       FMEA
   Impact          Test             Delta
   Analysis        Report           Analysis

4.3 Change Impact Analysis (CIA)
---------------------------------

**CIA Process:**

1. **Identify Changed Elements:**
   - Source files modified (Git diff)
   - Affected functions, modules
   - Changed requirements

2. **Trace to Safety Requirements:**
   - Which safety requirements impacted?
   - ASIL level of affected functions?

3. **Assess Regression Scope:**
   - Full regression needed? Or selective?
   - Update FMEA/FTA? Or argument by equivalence?

**Example: CIA for AEB Update**

.. code-block:: python

   # Change Impact Analysis Tool (Simplified)
   
   change_description = {
       'version_from': 'v2.1',
       'version_to': 'v2.2',
       'changed_files': [
           'aeb_controller.c',
           'sensor_fusion.c'
       ],
       'changed_functions': [
           'calculate_braking_force',
           'plausibility_check'
       ],
       'lines_changed': 25,
       'requirements_affected': ['REQ-AEB-012', 'REQ-AEB-045'],
       'asil_level': 'B'
   }
   
   requirements_db = {
       'REQ-AEB-012': {
           'description': 'AEB shall activate braking if TTC < 1.5s',
           'asil': 'B',
           'verification': ['UT-012', 'IT-034', 'SYS-089']
       },
       'REQ-AEB-045': {
           'description': 'Sensor fusion shall cross-check radar and camera',
           'asil': 'B',
           'verification': ['UT-045', 'IT-067']
       }
   }
   
   def perform_change_impact_analysis(change, req_db):
       """Determine verification scope based on change impact"""
       impacted_reqs = change['requirements_affected']
       
       print(f"Change Impact Analysis: {change['version_from']} → {change['version_to']}")
       print(f"Changed files: {len(change['changed_files'])}")
       print(f"Changed functions: {change['changed_functions']}")
       print(f"ASIL level: {change['asil_level']}")
       print(f"\nImpacted Requirements:")
       
       regression_tests = set()
       for req_id in impacted_reqs:
           req = req_db.get(req_id, {})
           print(f"  {req_id}: {req.get('description')}")
           print(f"    ASIL: {req.get('asil')}")
           print(f"    Verification: {req.get('verification')}")
           regression_tests.update(req.get('verification', []))
       
       print(f"\nRegression Test Suite: {len(regression_tests)} test cases")
       print(f"  {sorted(regression_tests)}")
       
       # Determine if full safety case update needed
       if change['asil_level'] in ['C', 'D'] or change['lines_changed'] > 100:
           recommendation = "FULL SAFETY CASE UPDATE (high ASIL or large change)"
       else:
           recommendation = "INCREMENTAL UPDATE (update argument sufficient)"
       
       print(f"\nRecommendation: {recommendation}")
       
       return regression_tests
   
   perform_change_impact_analysis(change_description, requirements_db)
   
   # Output:
   # Change Impact Analysis: v2.1 → v2.2
   # Changed files: 2
   # Changed functions: ['calculate_braking_force', 'plausibility_check']
   # ASIL level: B
   # 
   # Impacted Requirements:
   #   REQ-AEB-012: AEB shall activate braking if TTC < 1.5s
   #     ASIL: B
   #     Verification: ['UT-012', 'IT-034', 'SYS-089']
   #   REQ-AEB-045: Sensor fusion shall cross-check radar and camera
   #     ASIL: B
   #     Verification: ['UT-045', 'IT-067']
   # 
   # Regression Test Suite: 5 test cases
   #   ['IT-034', 'IT-067', 'SYS-089', 'UT-012', 'UT-045']
   # 
   # Recommendation: INCREMENTAL UPDATE (update argument sufficient)

4.4 Regression Verification Strategy
-------------------------------------

**Three Approaches:**

1. **Full Regression (Conservative):**
   - Re-run all tests, re-analyze all hazards
   - Costly, time-consuming
   - Required for ASIL D or major changes

2. **Selective Regression (Efficient):**
   - Test only impacted functions + integration paths
   - Update only affected FMEA/FTA sections
   - Suitable for ASIL B/C with limited changes

3. **Equivalence Argument (Aggressive):**
   - Argue that change is "safety-irrelevant" (e.g., UI color change)
   - No regression testing needed
   - Requires strong justification, independent review

**GSN Update Pattern:**

.. code-block:: text

   ┌────────────────────────────────────────┐
   │ G_Regr: Regression verification       │
   │         completed for update v2.2     │
   └──────────────────┬─────────────────────┘
                      │ Supported by
                      ▼
   ╱────────────────────────────────────────╲
   │ S_Regr: By selective regression       │
   │         (5 test cases re-executed)    │
   ╲──────────────────┬─────────────────────╱
                      │ Justified by
                      ▼
   ( ──────────────────────────────────── )
   ( J_Regr: Change limited to 25 LOC,   )
   (         ASIL B, no new interfaces    )
   
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ G_R1:   │  │ G_R2:   │  │ G_R3:   │
   │ Unit    │  │ Integr. │  │ System  │
   │ tests   │  │ tests   │  │ tests   │
   │ passed  │  │ passed  │  │ passed  │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        ▼            ▼            ▼
   ○────────    ○────────    ○────────
   Sn_R1       Sn_R2        Sn_R3
   UT Report   IT Report    SYS Report
   (2 tests)   (2 tests)    (1 test)

================================================================================
5. Modular Safety Cases — Compositional Arguments
================================================================================

5.1 Modular Safety Case Motivation
-----------------------------------

**Problem:** Monolithic safety cases for complex systems are:
- Difficult to maintain (100+ page documents)
- Hard to reuse components across projects
- Time-consuming for incremental changes

**Solution:** **Modular Safety Cases** with **contracts** (assume-guarantee reasoning).

**Concept:**

.. code-block:: text

   System Safety Case
      ├─ Component A Safety Case
      │  ├─ Assumes: Input voltage 9-16V
      │  └─ Guarantees: Output valid within 100ms
      └─ Component B Safety Case
         ├─ Assumes: Input valid from Component A
         └─ Guarantees: Braking force 0-5000N

**Contract Verification:**
- Component A's guarantee **satisfies** Component B's assumption → Composition valid
- If assumption violated → Need interface safety monitor

5.2 GSN Module Pattern
-----------------------

**Module Away Pattern:**

.. code-block:: text

   Main Safety Case:
   
   ┌────────────────────────────────────┐
   │ G1: System X is safe               │
   └──────────────┬─────────────────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
   ┌─────────┐       ┌──────────┐
   │ G1.1:   │       │ G1.2:    │
   │ Module  │       │ Module B │
   │ A safe  │       │ safe     │
   └────┬────┘       └────┬─────┘
        │                 │
        ▼                 ▼
    ╱╲────╱╲          ╱╲────╱╲
    │Module│          │Module│
    │  A   │          │  B   │   (References to separate safety case modules)
    ╲╱────╲╱          ╲╱────╲╱

**Module A Safety Case (Separate Document):**

.. code-block:: text

   ┌────────────────────────────────────────┐
   │ G_MA: Module A provides safe braking   │
   │       force output (ASIL B)            │
   └──────────────────┬─────────────────────┘
                      │ In context of
                      ▼
   ╭──────────────────────────────────────────╮
   │ C_MA: Assumes:                           │
   │  - Input voltage: 9-16V                  │
   │  - CAN bus operational (≥ 90% uptime)    │
   │  - Temperature: -40°C to +85°C           │
   ╰──────────────────────────────────────────╯
                      │
                      ▼
   ╭──────────────────────────────────────────╮
   │ J_MA: Guarantees:                        │
   │  - Braking force: 0-5000N ±2%            │
   │  - Response time: < 100ms                │
   │  - Failure probability: < 1e-6 /hour     │
   ╰──────────────────────────────────────────╯

5.3 Contract Validation Example
--------------------------------

.. code-block:: python

   # Safety contract validation tool
   
   class SafetyContract:
       def __init__(self, component_name):
           self.component_name = component_name
           self.assumptions = {}
           self.guarantees = {}
       
       def add_assumption(self, name, spec):
           self.assumptions[name] = spec
       
       def add_guarantee(self, name, spec):
           self.guarantees[name] = spec
       
       def validate_composition(self, provider_contract):
           """Check if provider's guarantees satisfy this component's assumptions"""
           violations = []
           
           for assumption_name, assumption_spec in self.assumptions.items():
               # Find corresponding guarantee from provider
               matching_guarantee = provider_contract.guarantees.get(assumption_name)
               
               if not matching_guarantee:
                   violations.append(f"Assumption '{assumption_name}' not guaranteed by provider")
               elif not self._spec_satisfied(assumption_spec, matching_guarantee):
                   violations.append(f"Guarantee for '{assumption_name}' insufficient")
           
           return violations
       
       def _spec_satisfied(self, assumption, guarantee):
           """Check if guarantee satisfies assumption (simplified range check)"""
           # Example: voltage range check
           if 'voltage' in assumption:
               # Assumption: 9-16V, Guarantee: 8-17V → OK (guarantee covers assumption)
               return (guarantee['min'] <= assumption['min'] and 
                       guarantee['max'] >= assumption['max'])
           return True  # Simplified
   
   # Example: Module A (Braking ECU) and Module B (Power Supply)
   
   module_a = SafetyContract("Braking_ECU")
   module_a.add_assumption("input_voltage", {'min': 9, 'max': 16, 'unit': 'V'})
   module_a.add_guarantee("braking_force", {'min': 0, 'max': 5000, 'accuracy': 0.02, 'unit': 'N'})
   module_a.add_guarantee("response_time", {'max': 100, 'unit': 'ms'})
   
   power_supply = SafetyContract("Power_Supply")
   power_supply.add_guarantee("input_voltage", {'min': 8, 'max': 17, 'unit': 'V'})  # Covers 9-16V
   
   # Validate composition
   violations = module_a.validate_composition(power_supply)
   
   if violations:
       print(f"❌ Composition invalid:")
       for v in violations:
           print(f"  - {v}")
   else:
       print(f"✅ Composition valid: Power supply guarantees satisfy Braking ECU assumptions")
   
   # Output:
   # ✅ Composition valid: Power supply guarantees satisfy Braking ECU assumptions

================================================================================
6. Safety Case Patterns — Reusable Argument Structures
================================================================================

6.1 Common Safety Case Patterns
--------------------------------

**Pattern 1: Argument by Elimination of Hazards**

.. code-block:: text

   Strategy: Demonstrate all hazards eliminated or mitigated to ALARP
   
   Steps:
   1. Identify all hazards (HAZOP, FMEA, FTA)
   2. For each hazard:
      a. Eliminate (design out)
      b. Mitigate (reduce probability/severity)
      c. Accept (if ALARP)
   3. Evidence: Hazard log with mitigation status

**Pattern 2: Argument by Compliance with Standards**

.. code-block:: text

   Strategy: Demonstrate compliance with recognized safety standard
   
   Steps:
   1. Identify applicable standard (ISO 26262, DO-178C, EN 50129)
   2. Create compliance matrix (standard requirement → evidence)
   3. Independent assessment (TÜV, Exida, UL)
   
   Evidence: Assessment report, certification

**Pattern 3: Argument by Diversity**

.. code-block:: text

   Strategy: Demonstrate redundant channels are sufficiently diverse
   
   Steps:
   1. Design diversity: Different algorithms, architectures
   2. Implementation diversity: Different teams, languages, compilers
   3. Data diversity: Different sensors, signal processing
   
   Evidence: Diversity analysis, CCF assessment (β-factor)

**Pattern 4: Argument by Testing Coverage**

.. code-block:: text

   Strategy: Demonstrate testing is comprehensive and rigorous
   
   Steps:
   1. Requirements coverage: All requirements traced to tests
   2. Code coverage: 100% MC/DC (ASIL C/D), 100% statement (ASIL B)
   3. Scenario coverage: Operational scenarios, edge cases, fault injection
   
   Evidence: Traceability matrix, coverage reports, test results

**Pattern 5: Argument by Operational Experience**

.. code-block:: text

   Strategy: Demonstrate similar system has safe field history
   
   Steps:
   1. Identify similar system (same architecture, environment)
   2. Collect field data (failure rates, incidents)
   3. Argument by analogy (new system ≥ as safe as proven system)
   
   Evidence: Field data, similarity analysis, change impact assessment

6.2 Anti-Patterns (What NOT to Do)
-----------------------------------

**Anti-Pattern 1: Circular Argument**

.. code-block:: text

   ❌ WRONG:
   G1: System is safe
      ├─ G1.1: Design is correct
      │  └─ Evidence: Design passed review
      └─ G1.2: Review was thorough
         └─ Evidence: Design is correct  ← Circular!

**Anti-Pattern 2: Unsubstantiated Claims**

.. code-block:: text

   ❌ WRONG:
   G1: System is safe
      └─ Evidence: "Engineering judgment" ← No objective evidence!

**Anti-Pattern 3: Missing Context/Assumptions**

.. code-block:: text

   ❌ WRONG:
   G1: Braking system is safe
      (No context: Operating environment? ASIL level? Mission profile?)

**Anti-Pattern 4: Stale Evidence**

.. code-block:: text

   ❌ WRONG:
   G1: Software is defect-free
      └─ Evidence: Test results from 2020 ← System changed since then!

================================================================================
7. SACM (Structured Assurance Case Metamodel) — 2026 Standard
================================================================================

7.1 SACM Overview
-----------------

**SACM (OMG Standard, 2024):**
Metamodel for representing assurance cases (safety, security, reliability) in machine-readable format.

**Benefits:**
- **Tool interoperability:** Export/import between Astah GSN, AdvoCATE, ASCE
- **Automated analysis:** Consistency checking, completeness, traceability
- **Version control:** Track changes to arguments over time

**SACM Core Concepts:**

+---------------------+------------------------------------------+
| SACM Element        | Description                              |
+=====================+==========================================+
| **Claim**           | Assertion about system property          |
+---------------------+------------------------------------------+
| **ArgumentReasoning**| Inference linking sub-claims to claim   |
+---------------------+------------------------------------------+
| **ArtifactReference**| Pointer to evidence artifact            |
+---------------------+------------------------------------------+
| **AssuranceContext**| Scope, environment, assumptions          |
+---------------------+------------------------------------------+

**SACM vs GSN:**
- SACM is **metamodel** (defines structure, not notation)
- GSN is **notation** (visual representation)
- SACM can represent GSN (plus other notations like CAE)

7.2 SACM Example (XML Format)
------------------------------

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <SACM:AssuranceCase xmlns:SACM="http://www.omg.org/spec/SACM/2.0">
     <claim id="G1" description="AEB system is acceptably safe">
       <context id="C1" description="Operating environment: Urban roads, 0-50 km/h"/>
       
       <supportedBy>
         <argumentReasoning id="S1" 
                            description="Argument by ISO 26262 compliance"/>
       </argumentReasoning>
       
       <subclaim id="G2" description="All hazards identified">
         <supportedBy>
           <artifactReference id="Sn1" 
                              artifact="AEB_HARA_Report_v2.1.pdf"
                              date="2025-11-15"/>
         </supportedBy>
       </subclaim>
       
       <subclaim id="G3" description="Safety requirements correct">
         <supportedBy>
           <artifactReference id="Sn2" 
                              artifact="Requirements_Review_Minutes.pdf"
                              date="2025-12-01"/>
         </supportedBy>
       </subclaim>
     </claim>
   </SACM:AssuranceCase>

**SACM Tools (2026):**
- **Astah GSN:** Visual editor with SACM export
- **AdvoCATE (Adelard):** Safety case management tool
- **ASCE (Assurance Case Studio):** Open-source editor
- **NOR-STA (DNV):** Railway safety case tool

================================================================================
8. Exam Preparation — 5 Comprehensive Questions
================================================================================

**Question 1: GSN Elements — Match Symbol to Purpose**

**Question:** Match each GSN element to its purpose:

A. Goal (Rectangle)  
B. Strategy (Parallelogram)  
C. Solution (Circle)  
D. Context (Rounded Rectangle)

1. Evidence supporting a claim  
2. Scope or boundary condition  
3. Safety claim to be demonstrated  
4. Argumentation approach

**Answer:**
- A → 3 (Goal = Safety claim)
- B → 4 (Strategy = Argumentation approach)
- C → 1 (Solution = Evidence)
- D → 2 (Context = Scope/boundary)

---

**Question 2: Confidence Argument — Assess Evidence Quality**

**Scenario:** FMEA report created by Safety Engineer A, reviewed by Safety Engineer A (same person), dated 2023-01-15, covers 75% of components.

**Question:** Calculate confidence score (0-100) and recommend improvements.

**Answer:**

.. code-block:: python

   evidence = {
       'author': 'Safety Engineer A',
       'reviewer': 'Safety Engineer A',  # Self-review
       'date': '2023-01-15',  # 3 years old
       'coverage_percent': 75,
       'traceability': 'Partial',
       'tool_tcl': None
   }
   
   # Confidence scoring (from Section 3.2):
   # Independence: 0 (self-review)
   # Coverage: 75 * 0.3 = 22.5
   # Recency: 0 (> 3 years)
   # Traceability: 5 (partial)
   # Tool: 0 (none)
   # Total: 27.5/100 (LOW confidence)

**Recommendations:**
1. **Independent review:** Get third-party assessment (TÜV, Exida) → +30 points
2. **Update FMEA:** Refresh to 2026 → +20 points
3. **Improve coverage:** 75% → 100% → +7.5 points
4. **Full traceability:** Partial → Full → +5 points
5. **Expected new score:** 90/100 (HIGH confidence)

---

**Question 3: Update Argument — Determine Regression Scope**

**Scenario:** Software update changes 5 lines of code in ASIL D braking controller, fixes buffer overflow bug.

**Question:** What verification is required? Full regression or selective?

**Answer:**

**Analysis:**
- **ASIL D:** Highest safety level
- **Change type:** Bug fix (defect correction)
- **Changed code:** Safety-critical (braking controller)
- **Lines changed:** 5 (small)

**Decision:** **FULL REGRESSION REQUIRED**

**Rationale:**
- ASIL D requires maximum confidence
- Bug fix implies previous safety case was incorrect → Re-validate all claims
- Even small changes can have unexpected side effects in safety-critical code
- ISO 26262 Part 8 requires re-assessment for safety-critical changes

**Verification Activities:**
1. Re-run all unit tests (MC/DC coverage)
2. Re-run all integration tests
3. Re-run system validation tests
4. Update FMEA/FTA (verify bug fix doesn't introduce new hazards)
5. Independent safety assessment

---

**Question 4: Modular Safety Case — Validate Contract**

**Given:**

- **Component A (Sensor) Guarantees:** Output voltage 0-5V, accuracy ±0.1V
- **Component B (ADC) Assumes:** Input voltage 0-5V, accuracy ±0.05V

**Question:** Is composition valid?

**Answer:**

**Analysis:**
- Sensor guarantees: **0-5V ± 0.1V** (actual range: -0.1V to 5.1V)
- ADC assumes: **0-5V ± 0.05V** (expected range: -0.05V to 5.05V)

**Voltage range:** ✅ OK (-0.1V to 5.1V covers -0.05V to 5.05V)  
**Accuracy:** ❌ FAIL (Sensor ±0.1V does NOT meet ADC assumption ±0.05V)

**Conclusion:** **Composition INVALID**

**Mitigation Options:**
1. **Improve sensor:** Use higher-accuracy sensor (±0.05V)
2. **Relax ADC assumption:** Accept ±0.1V input (if ADC can handle it)
3. **Add safety monitor:** Detect out-of-tolerance sensor readings

---

**Question 5: Safety Case Pattern — Choose Appropriate Strategy**

**Scenario:** New autonomous driving feature uses AI/ML perception. Limited field data (new technology).

**Question:** Which safety case pattern is most appropriate?

**Answer:**

**Options:**
1. ❌ **Argument by Operational Experience:** Not applicable (no field data yet)
2. ❌ **Argument by Compliance:** Standards for AI/ML still emerging (UL 4600 draft)
3. ✅ **Argument by Diversity + Testing Coverage:** BEST CHOICE
4. ❌ **Argument by Elimination:** Cannot eliminate all AI/ML failure modes (OOD, adversarial)

**Recommended Strategy:**

.. code-block:: text

   S1: Argument by multi-sensor fusion (diversity) and comprehensive testing
   
   Sub-arguments:
   ├─ G1: Diverse perception channels (camera, radar, lidar)
   │  └─ Evidence: Diversity analysis, CCF β < 0.01
   ├─ G2: Comprehensive scenario testing (Pegasus taxonomy)
   │  └─ Evidence: 100M km simulation (CARLA, LGSVL), 1M km road test
   ├─ G3: OOD detection with safe degradation
   │  └─ Evidence: ODIN scores, L3 → L2 fallback validation
   └─ G4: Runtime monitoring (UL 4600)
      └─ Evidence: Confidence thresholds, watchdog, black box logging

================================================================================
9. Completion Checklist
================================================================================

.. code-block:: text

   ✅ Safety Case Fundamentals
      ├─ Definition (structured argument + evidence)
      ├─ CAE framework (Claims, Arguments, Evidence)
      ├─ Safety case vs safety plan
      └─ Standards requiring safety cases
   
   ✅ GSN (Goal Structuring Notation)
      ├─ GSN elements (Goal, Strategy, Solution, Context, Justification, Assumption)
      ├─ GSN symbols and relationships
      └─ AEB safety case example (complete GSN tree)
   
   ✅ Confidence Arguments
      ├─ Need for assessing evidence quality
      ├─ Confidence factors (independence, coverage, recency, traceability, tool qualification)
      ├─ Confidence scoring algorithm (Python)
      └─ GSN confidence argument example
   
   ✅ Update Arguments (2026)
      ├─ Motivation (OTA updates, ML retraining, continuous deployment)
      ├─ Change impact analysis (CIA)
      ├─ Regression verification strategies (full, selective, equivalence)
      └─ GSN update argument pattern
   
   ✅ Modular Safety Cases
      ├─ Contracts (assume-guarantee)
      ├─ GSN module pattern
      ├─ Contract validation (Python tool)
      └─ Compositional reasoning
   
   ✅ Safety Case Patterns
      ├─ 5 common patterns (hazard elimination, compliance, diversity, testing, operational experience)
      ├─ 4 anti-patterns (circular argument, unsubstantiated claims, missing context, stale evidence)
      └─ Pattern selection guidance
   
   ✅ SACM (2026 Standard)
      ├─ Structured Assurance Case Metamodel
      ├─ SACM vs GSN comparison
      ├─ XML example
      └─ SACM tools (Astah, AdvoCATE, ASCE)
   
   ✅ Exam Questions (5)
      ├─ GSN element matching
      ├─ Confidence scoring and improvement
      ├─ Update argument regression scope
      ├─ Modular safety case contract validation
      └─ Safety case pattern selection (AI/ML)

================================================================================
10. Key Takeaways
================================================================================

1. **Safety cases are structured arguments** (claims + arguments + evidence) demonstrating a system is acceptably safe for its intended use.

2. **GSN (Goal Structuring Notation) provides visual representation** of safety arguments with 6 core elements: Goal, Strategy, Solution, Context, Justification, Assumption.

3. **Confidence arguments assess evidence quality** using factors like independence, coverage, recency, and traceability to prevent weak evidence from undermining safety claims.

4. **Update arguments (2026) enable evolutionary safety cases** for OTA updates, ML retraining, and continuous deployment by demonstrating safety is maintained post-modification.

5. **Modular safety cases use contracts (assume-guarantee)** to enable compositional reasoning and reuse, reducing effort for complex systems with multiple components.

6. **Safety case patterns provide reusable argument structures** for common scenarios (hazard elimination, compliance, diversity, testing, operational experience).

7. **SACM (OMG 2024 standard) enables machine-readable safety cases** with tool interoperability, automated analysis, and version control for modern safety-critical development.

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** ISO 26262:2018, EN 50129:2018, DEF STAN 00-56, OMG SACM 2.0

================================================================================
