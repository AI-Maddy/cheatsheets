📋 **Safety Case Development**
═══════════════════════════════════════════════════════════════════

**Full Name:** Safety Case (Assurance Case for Safety)  
**Type:** Structured argument demonstrating system safety  
**Standards:** UK Defence Standard 00-56, CAP 670 (UK CAA), ISO 26262,  
EN 50129, DO-178C (implicit), EASA Part 21

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — SAFETY CASE IN 60 SECONDS**
─────────────────────────────────────────

**What is a Safety Case?**

::

    Safety Case = Structured argument + evidence that system is
                  acceptably safe for a given application in a
                  given operating environment
    
    Components:
    1. Claims (what you assert is true)
    2. Arguments (logical reasoning linking claims to evidence)
    3. Evidence (data, test results, analysis proving claims)

**Structure:**

.. code-block:: text

    Top Claim: "System X is acceptably safe for use Y"
         │
         ├─ Sub-Claim 1: "Hazards have been identified"
         │      └─ Evidence: HAZOP report, FMEA
         │
         ├─ Sub-Claim 2: "Hazards are mitigated to acceptable levels"
         │      ├─ Evidence: Risk assessment, FTA
         │      └─ Evidence: Test results, design specifications
         │
         └─ Sub-Claim 3: "Safety requirements implemented correctly"
                └─ Evidence: V&V reports, certification tests

**Why Safety Case?**

✅ **Regulatory requirement**: UK CAA, EASA, UK HSE, railways  
✅ **Explicit assurance**: Forces rigorous demonstration of safety  
✅ **Lifecycle management**: Living document, updated with changes  
✅ **Communication**: Clear presentation to regulators, stakeholders  
✅ **Accountability**: Defines who is responsible for safety

**Safety Case vs Traditional Compliance:**

+-------------------+---------------------------+---------------------------+
| **Aspect**        | **Traditional**           | **Safety Case**           |
|                   | **(Checklist)**           | **(Argument)**            |
+===================+===========================+===========================+
| **Approach**      | Prescriptive (do X, Y, Z) | Goal-based (prove safe)   |
+-------------------+---------------------------+---------------------------+
| **Flexibility**   | Low (must follow std)     | High (justify approach)   |
+-------------------+---------------------------+---------------------------+
| **Innovation**    | Difficult (not in std)    | Enabled (if justified)    |
+-------------------+---------------------------+---------------------------+
| **Burden**        | On regulator (check       | On developer (prove       |
|                   | compliance)               | safety)                   |
+-------------------+---------------------------+---------------------------+
| **Documentation** | Checklist completion      | Structured argument +     |
|                   |                           | evidence                  |
+-------------------+---------------------------+---------------------------+

════════════════════════════════════════════════════════════════════

📖 **1. SAFETY CASE FUNDAMENTALS**
══════════════════════════════════

**1.1 Definition & Purpose**
----------------------------

**Safety Case (UK Def Std 00-56):**

    "A structured argument, supported by a body of evidence, that
    provides a compelling, comprehensible and valid case that a
    system is safe for a given application in a given environment."

**Key Elements:**

1. **Structured argument**: Logical decomposition from top claim to evidence
2. **Body of evidence**: Test results, analyses, reviews, operational data
3. **Compelling**: Convinces independent reviewer
4. **Comprehensible**: Clear to technical and non-technical audiences
5. **Valid**: Arguments are sound, evidence is sufficient

**Purpose:**

✅ **Demonstrate safety**: Explicit proof system meets safety requirements  
✅ **Support certification**: Required by regulators (CAA, EASA, HSE)  
✅ **Manage change**: Update argument when design changes  
✅ **Capture rationale**: Why design decisions were made  
✅ **Enable review**: Independent assessment by authority

**1.2 Regulatory Context**
--------------------------

**UK Civil Aviation (CAP 670):**

- Safety case required for Air Traffic Management (ATM) changes
- Explicit argument linking hazards → risks → mitigations
- Independent safety assessment

**UK Defence (Def Stan 00-56):**

- Mandatory for all defence systems
- Through-life safety case (concept → disposal)
- Safety case owner appointed

**UK Railways (EN 50129):**

- Safety case for signalling and control systems
- Generic + specific safety cases
- Common Safety Method (CSM) compliance

**Automotive (ISO 26262):**

- Safety case implicit (not called "safety case")
- Safety argumentation via ASIL decomposition
- Functional Safety Assessment (FSA) report

**Aerospace (DO-178C, DO-254):**

- Compliance-based (not explicit safety case)
- But: Certification plans serve similar purpose
- EASA increasingly requiring explicit safety arguments

**1.3 Safety Case Lifecycle**
-----------------------------

.. code-block:: text

    Phase 1: CONCEPT
    - Preliminary Safety Case (PSC)
    - Identify top-level hazards
    - Define safety strategy
    
    Phase 2: DEVELOPMENT
    - Interim Safety Case (ISC)
    - Develop detailed arguments
    - Collect evidence (design, analysis)
    
    Phase 3: VERIFICATION
    - Final Safety Case (FSC)
    - Complete testing, V&V
    - Independent safety assessment
    
    Phase 4: OPERATION
    - Operational Safety Case (OSC)
    - Maintain and update
    - Incorporate lessons learned
    
    Phase 5: MODIFICATION
    - Change Safety Case
    - Management of Change (MOC)
    - Re-validation
    
    Phase 6: DECOMMISSIONING
    - Disposal Safety Case
    - Safe retirement

════════════════════════════════════════════════════════════════════

📖 **2. SAFETY CASE STRUCTURE**
═══════════════════════════════

**2.1 Claims Hierarchy**
------------------------

**Top Claim (Top-Level Safety Claim):**

    "System X is acceptably safe for operation in context Y"
    
    Example (Aircraft):
    "The Boeing 787 Dreamliner is acceptably safe for commercial
    passenger transport in worldwide operations."

**Decomposition Strategy:**

.. code-block:: text

    Top Claim
         │
         ├─ Strategy 1: Argument by hazard analysis
         │      │
         │      ├─ Sub-Claim 1.1: "All hazards identified"
         │      ├─ Sub-Claim 1.2: "Hazards have acceptable risk"
         │      └─ Sub-Claim 1.3: "Residual risk is ALARP"
         │
         ├─ Strategy 2: Argument by compliance
         │      │
         │      ├─ Sub-Claim 2.1: "Complies with DO-178C DAL A"
         │      ├─ Sub-Claim 2.2: "Complies with DO-254 Level A"
         │      └─ Sub-Claim 2.3: "Complies with FAR 25.1309"
         │
         └─ Strategy 3: Argument by operational experience
                │
                ├─ Sub-Claim 3.1: "Similar systems have safe history"
                └─ Sub-Claim 3.2: "Lessons learned incorporated"

**2.2 Argument Patterns**
-------------------------

**Pattern 1: Hazard-Directed Argument**

.. code-block:: text

    Claim: "System is safe"
         │
         ├─ Claim: "Hazard H1 is acceptable"
         │      ├─ Claim: "H1 severity is Low"
         │      │      └─ Evidence: Hazard analysis (FMEA)
         │      ├─ Claim: "H1 likelihood is Remote"
         │      │      └─ Evidence: FTA (probability < 10⁻⁷)
         │      └─ Claim: "H1 risk matrix: Green (acceptable)"
         │
         ├─ Claim: "Hazard H2 is acceptable"
         │      └─ ...
         │
         └─ Claim: "All hazards identified"
                └─ Evidence: HAZOP, peer review

**Pattern 2: Compliance Argument**

.. code-block:: text

    Claim: "System complies with Standard X"
         │
         ├─ Claim: "Objective 1 satisfied"
         │      └─ Evidence: Test report TR-101
         │
         ├─ Claim: "Objective 2 satisfied"
         │      └─ Evidence: Design review DR-205
         │
         └─ Claim: "All objectives covered"
                └─ Evidence: Traceability matrix

**Pattern 3: Redundancy Argument**

.. code-block:: text

    Claim: "Function F is highly reliable"
         │
         ├─ Claim: "Primary channel reliable"
         │      └─ Evidence: MTBF analysis
         │
         ├─ Claim: "Backup channel reliable"
         │      └─ Evidence: MTBF analysis
         │
         ├─ Claim: "Channels are independent"
         │      └─ Evidence: Common cause failure analysis
         │
         └─ Claim: "Switching mechanism reliable"
                └─ Evidence: Fault injection testing

**2.3 Evidence Types**
----------------------

**Analytical Evidence:**

- FMEA, FTA, HAZOP results
- Formal verification (proof)
- Probabilistic risk assessment (PRA)
- Worst-case timing analysis

**Test Evidence:**

- Unit tests, integration tests, system tests
- Environmental testing (temperature, vibration, EMI)
- Fault injection testing
- Stress testing, soak testing

**Review Evidence:**

- Design reviews (peer review, expert review)
- Code reviews (static analysis, manual inspection)
- Safety audits
- Independent safety assessment

**Process Evidence:**

- Quality management system (ISO 9001)
- Configuration management records
- Verification and validation reports
- Training records (personnel competence)

**Operational Evidence:**

- Field experience (operational hours)
- Incident/accident reports (lessons learned)
- Similar system data (fleet statistics)

**Standards Evidence:**

- Compliance matrices (DO-178C objectives)
- Certification artifacts
- Qualification data (tools, components)

════════════════════════════════════════════════════════════════════

📖 **3. SAFETY CASE EXAMPLE: AUTONOMOUS VEHICLE**
═════════════════════════════════════════════════

**3.1 Top-Level Claim**
-----------------------

.. code-block:: text

    CLAIM: "The AutoDrive Level 4 autonomous vehicle is acceptably
           safe for passenger transport on designated urban routes
           (Operational Design Domain: city streets, <45 mph,
           daylight, dry weather)."

**3.2 Argument Structure**
--------------------------

**Strategy 1: Hazard-Based Argument**

.. code-block:: text

    CLAIM 1: "All significant hazards have been identified and
             mitigated to acceptable levels"
         │
         ├─ CLAIM 1.1: "Hazard identification is complete"
         │      │
         │      ├─ Evidence E1.1.1: STPA analysis report
         │      ├─ Evidence E1.1.2: HAZOP study (48 nodes)
         │      ├─ Evidence E1.1.3: FMEA (127 failure modes)
         │      ├─ Evidence E1.1.4: Lessons learned (industry accidents)
         │      └─ Evidence E1.1.5: Independent review (TÜV SÜD)
         │
         ├─ CLAIM 1.2: "Collision with pedestrian (H-1) is acceptable"
         │      │
         │      ├─ CLAIM 1.2.1: "Collision likelihood is very low"
         │      │      │
         │      │      ├─ Evidence E1.2.1.1: Sensor coverage (360°)
         │      │      ├─ Evidence E1.2.1.2: Redundant sensors (camera+lidar+radar)
         │      │      ├─ Evidence E1.2.1.3: Automatic Emergency Braking (AEB) tested
         │      │      ├─ Evidence E1.2.1.4: FTA calculation (P < 10⁻⁸/hr)
         │      │      └─ Evidence E1.2.1.5: Simulation (10M miles, 0 collisions)
         │      │
         │      ├─ CLAIM 1.2.2: "Collision severity is mitigated"
         │      │      │
         │      │      ├─ Evidence E1.2.2.1: Speed limit (25 mph in pedestrian zones)
         │      │      ├─ Evidence E1.2.2.2: Soft front bumper design
         │      │      └─ Evidence E1.2.2.3: Post-collision notification (911 auto-dial)
         │      │
         │      └─ CLAIM 1.2.3: "Residual risk is ALARP"
         │             │
         │             ├─ Evidence E1.2.3.1: Risk comparison (safer than human driver)
         │             └─ Evidence E1.2.3.2: Cost-benefit analysis (further measures disproportionate)
         │
         ├─ CLAIM 1.3: "Loss of vehicle control (H-2) is acceptable"
         │      └─ [Similar decomposition...]
         │
         └─ CLAIM 1.4: "All other hazards (H-3 to H-15) are acceptable"
                └─ [Decomposed by hazard...]

**Strategy 2: Functional Safety Argument**

.. code-block:: text

    CLAIM 2: "Safety-critical functions are implemented to required
             integrity levels"
         │
         ├─ CLAIM 2.1: "Perception system meets ASIL D requirements"
         │      │
         │      ├─ CLAIM 2.1.1: "Hardware metrics achieved"
         │      │      │
         │      │      ├─ Evidence E2.1.1.1: SPFM = 97% (target ≥90%)
         │      │      ├─ Evidence E2.1.1.2: LFM = 85% (target ≥60%)
         │      │      └─ Evidence E2.1.1.3: PMHF = 3 FIT (target <10 FIT)
         │      │
         │      ├─ CLAIM 2.1.2: "Software developed per ISO 26262 Part 6"
         │      │      │
         │      │      ├─ Evidence E2.1.2.1: Software Safety Requirements (SSR) complete
         │      │      ├─ Evidence E2.1.2.2: MISRA C:2012 compliance (99.8%, deviations justified)
         │      │      ├─ Evidence E2.1.2.3: Static analysis (Polyspace, 0 critical defects)
         │      │      ├─ Evidence E2.1.2.4: Unit test coverage (MC/DC 100%)
         │      │      └─ Evidence E2.1.2.5: Software safety audit (passed)
         │      │
         │      └─ CLAIM 2.1.3: "Perception failures detected and handled"
         │             │
         │             ├─ Evidence E2.1.3.1: Sensor fusion architecture (3-way redundancy)
         │             ├─ Evidence E2.1.3.2: Plausibility checks (cross-sensor validation)
         │             ├─ Evidence E2.1.3.3: Fail-operational capability (2 of 3 sensors sufficient)
         │             └─ Evidence E2.1.3.4: Minimal Risk Condition (safe stop if all fail)
         │
         ├─ CLAIM 2.2: "Planning system meets ASIL D requirements"
         │      └─ [Similar decomposition...]
         │
         └─ CLAIM 2.3: "Control system meets ASIL D requirements"
                └─ [Similar decomposition...]

**Strategy 3: V&V Argument**

.. code-block:: text

    CLAIM 3: "System has been verified and validated"
         │
         ├─ CLAIM 3.1: "Requirements verified complete and correct"
         │      │
         │      ├─ Evidence E3.1.1: Requirements review (3 independent reviewers)
         │      ├─ Evidence E3.1.2: Traceability matrix (Req → Design → Test)
         │      └─ Evidence E3.1.3: Formal methods (model checking critical paths)
         │
         ├─ CLAIM 3.2: "Design verified against requirements"
         │      │
         │      ├─ Evidence E3.2.1: Design FMEAs (system + HW + SW)
         │      ├─ Evidence E3.2.2: Architecture analysis (independence verified)
         │      └─ Evidence E3.2.3: Safety architecture review (passed)
         │
         ├─ CLAIM 3.3: "Implementation verified against design"
         │      │
         │      ├─ Evidence E3.3.1: Code reviews (100% critical code)
         │      ├─ Evidence E3.3.2: Unit tests (10,000+ tests, MC/DC coverage)
         │      └─ Evidence E3.3.3: Integration tests (1,000+ scenarios)
         │
         └─ CLAIM 3.4: "System validated in operational environment"
                │
                ├─ Evidence E3.4.1: Closed-track testing (5,000 miles)
                ├─ Evidence E3.4.2: Public road testing (500,000 miles, 0 at-fault accidents)
                ├─ Evidence E3.4.3: Edge case testing (10,000 synthetic scenarios)
                ├─ Evidence E3.4.4: Regression testing (continuous integration)
                └─ Evidence E3.4.5: Independent validation (TÜV SÜD, DMV approval)

**3.3 Safety Case Summary**
---------------------------

.. code-block:: text

    CONCLUSION:
    
    The AutoDrive Level 4 system has been demonstrated to be
    acceptably safe for operation within its defined ODD through:
    
    1. Comprehensive hazard identification (STPA, HAZOP, FMEA)
    2. Rigorous risk mitigation (redundancy, fail-operational design)
    3. ISO 26262 ASIL D compliance (all safety goals)
    4. Extensive V&V (5 million test miles, formal verification)
    5. Independent assessment (TÜV SÜD certification)
    
    Residual risks are ALARP and comparable to or better than
    experienced human drivers in the same ODD.
    
    Safety case owner: Dr. Jane Smith, Chief Safety Officer
    Independent assessor: TÜV SÜD America
    Regulator: California DMV
    Version: 2.5 (approved for pilot deployment, 50 vehicles)
    Next review: 2026-07-14 (6 months) or upon incident

════════════════════════════════════════════════════════════════════

📖 **4. GRAPHICAL NOTATION (GSN)**
══════════════════════════════════

**4.1 Goal Structuring Notation (GSN)**
---------------------------------------

**GSN is the standard graphical language for safety cases**

**Core Symbols:**

.. code-block:: text

    ┌──────────────┐
    │   GOAL       │   Claim to be substantiated
    │   (Claim)    │   Rectangle
    └──────────────┘
    
        ◇             STRATEGY
       ╱ ╲            How to decompose goal
      ╱   ╲           Diamond
     ───────
    
        ○             SOLUTION
       ╱ ╲            Evidence supporting goal
      ╱   ╲           Circle
     ───────
    
    ┌────────────────┐
    │ □ CONTEXT      │  Information clarifying goal
    │   (rounded)    │  Rounded rectangle
    └────────────────┘
    
    ┌────────────────┐
    │ ☐ ASSUMPTION   │  Unsubstantiated statement
    │   (rounded)    │  Rounded rectangle (different style)
    └────────────────┘
    
    ┌────────────────┐
    │ ⬡ JUSTIFICATION│ Rationale for approach
    │   (ellipse)    │  Oval
    └────────────────┘

**Example GSN Fragment:**

.. code-block:: text

    ┌─────────────────────────────────────┐
    │ G1: System is acceptably safe       │
    └──────────────┬──────────────────────┘
                   │
       ┌───────────┴───────────┐
       │   Context: ODD        │  (rounded rectangle)
       │   Urban, <45mph       │
       └───────────────────────┘
                   │
                   ◇  Strategy: Argument by hazard
                  ╱ ╲
                 ╱   ╲
                ───────
                   │
         ┌─────────┼─────────┐
         │         │         │
    ┌────┴───┐ ┌──┴───┐ ┌───┴────┐
    │ G1.1:  │ │ G1.2 │ │ G1.3:  │
    │ Hazards│ │ H-1  │ │ Other  │
    │ ID'd   │ │ OK   │ │ hazards│
    └────┬───┘ └──┬───┘ └────────┘
         │        │
         ○        ○
        ╱ ╲      ╱ ╲
       ╱   ╲    ╱   ╲
      ───────  ───────
      │        │
    Sn1:      Sn2:
    STPA      FTA
    Report    Calc

**4.2 GSN for Confidence Arguments**
------------------------------------

**Not just WHAT (claims), but HOW CONFIDENT (assurance)**

.. code-block:: text

    ┌─────────────────────────────────────┐
    │ G: Software is correct              │
    └──────────────┬──────────────────────┘
                   │
                   ◇  Strategy: V&V
                  ╱ ╲
                 ╱   ╲
                ───────
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────┴──────────┐   ┌────┴──────────┐
    │ G1: Tested    │   │ G2: Reviewed  │
    └───────┬───────┘   └───────┬───────┘
            │                   │
            │                   │
    ┌───────┴────────┐  ┌───────┴────────┐
    │ Confidence     │  │ Confidence     │
    │ Argument:      │  │ Argument:      │
    │ - 100% MC/DC   │  │ - Independent  │
    │ - 10K tests    │  │ - Expert       │
    │ - Automated    │  │ - Checklist    │
    └────────────────┘  └────────────────┘

════════════════════════════════════════════════════════════════════

📖 **5. SAFETY CASE BEST PRACTICES**
════════════════════════════════════

**5.1 Common Pitfalls**
-----------------------

❌ **"Compliance = Safety"**

- Fallacy: "We follow DO-178C, therefore we're safe"
- Reality: Standards are necessary but not sufficient
- Fix: Argue safety explicitly, use standards as supporting evidence

❌ **Weak Arguments**

- Example: "We did lots of testing" → No quantitative claim
- Fix: "MC/DC coverage 100%, 10,000 tests, 0 critical defects"

❌ **Missing Evidence**

- Argument structure complete, but evidence missing/weak
- Fix: Gap analysis, prioritize evidence collection

❌ **Circular Arguments**

- Claim A depends on Claim B, Claim B depends on Claim A
- Fix: Identify base evidence (ground truth), build up

❌ **Stale Safety Case**

- Safety case not updated after design changes
- Fix: Configuration management, change impact analysis

**5.2 Evidence Quality Criteria**
---------------------------------

**Relevant:**

- Evidence actually supports the claim
- Example: Unit test results → "Software units correct" ✅
- Counter: Unit test results → "System safe" ❌ (too big a leap)

**Sufficient:**

- Enough evidence to convince skeptical reviewer
- Quantitative: 100% MC/DC coverage vs "some testing"
- Multiple sources: Test + Review + Analysis

**Current:**

- Evidence not outdated
- Version control: Link evidence to specific design version

**Trustworthy:**

- Source is credible (independent, qualified)
- Process is rigorous (peer-reviewed, audited)
- Tools qualified (DO-330 for verification tools)

**5.3 Independent Safety Assessment**
-------------------------------------

**Role of Independent Assessor:**

✅ Challenge claims (devil's advocate)  
✅ Verify evidence sufficiency  
✅ Identify gaps, weak arguments  
✅ Provide independent opinion to regulator

**Qualifications:**

- Domain expertise (aviation, automotive, railway)
- Safety standards knowledge
- Independence (no commercial interest in project success)

**Deliverable:**

- Safety Assessment Report (SAR)
- Opinion: Recommend approval / Conditional / Reject
- Conditions: List of outstanding issues

════════════════════════════════════════════════════════════════════

📖 **6. SAFETY CASE TOOLS**
═══════════════════════════

**6.1 Commercial Tools**
------------------------

+----------------------+------------------+----------------------------+
| **Tool**             | **Vendor**       | **Features**               |
+======================+==================+============================+
| **ASCE**             | Adelard          | GSN editor, UK Def Std     |
|                      |                  | 00-56 compliant            |
+----------------------+------------------+----------------------------+
| **NOR-STA**          | SINTEF           | GSN, evidence management   |
+----------------------+------------------+----------------------------+
| **AdvoCATE**         | University of    | Open source, GSN           |
|                      | York (UK)        |                            |
+----------------------+------------------+----------------------------+
| **Astah GSN**        | Change Vision    | GSN diagrams, Japanese     |
+----------------------+------------------+----------------------------+

**6.2 Python Safety Case Generator**
------------------------------------

.. code-block:: python

    # safety_case_builder.py
    
    from dataclasses import dataclass
    from typing import List, Optional
    from enum import Enum
    
    class NodeType(Enum):
        GOAL = "Goal"
        STRATEGY = "Strategy"
        SOLUTION = "Solution"
        CONTEXT = "Context"
        ASSUMPTION = "Assumption"
        JUSTIFICATION = "Justification"
    
    @dataclass
    class SafetyCaseNode:
        id: str
        type: NodeType
        text: str
        parent: Optional['SafetyCaseNode'] = None
        children: List['SafetyCaseNode'] = None
        
        def __post_init__(self):
            if self.children is None:
                self.children = []
        
        def add_child(self, child: 'SafetyCaseNode'):
            self.children.append(child)
            child.parent = self
        
        def to_markdown(self, level=0) -> str:
            indent = "  " * level
            symbol = {
                NodeType.GOAL: "🎯",
                NodeType.STRATEGY: "◆",
                NodeType.SOLUTION: "📄",
                NodeType.CONTEXT: "📌",
                NodeType.ASSUMPTION: "⚠️",
                NodeType.JUSTIFICATION: "💡"
            }.get(self.type, "")
            
            result = f"{indent}{symbol} **{self.id}** ({self.type.value}): {self.text}\n"
            for child in self.children:
                result += child.to_markdown(level + 1)
            return result
    
    class SafetyCase:
        def __init__(self, title: str, system: str, version: str):
            self.title = title
            self.system = system
            self.version = version
            self.root: Optional[SafetyCaseNode] = None
        
        def set_root(self, root: SafetyCaseNode):
            self.root = root
        
        def export_markdown(self, filename: str):
            with open(filename, 'w') as f:
                f.write(f"# {self.title}\n\n")
                f.write(f"**System:** {self.system}\n")
                f.write(f"**Version:** {self.version}\n\n")
                f.write("## Safety Argument\n\n")
                if self.root:
                    f.write(self.root.to_markdown())
            print(f"Safety case exported to {filename}")
        
        def find_unsupported_goals(self) -> List[SafetyCaseNode]:
            """Find goals with no solution (evidence gap)"""
            gaps = []
            
            def traverse(node: SafetyCaseNode):
                if node.type == NodeType.GOAL:
                    has_solution = any(c.type == NodeType.SOLUTION 
                                      for c in node.children)
                    if not has_solution and not node.children:
                        gaps.append(node)
                for child in node.children:
                    traverse(child)
            
            if self.root:
                traverse(self.root)
            return gaps
    
    # Example usage
    if __name__ == "__main__":
        # Create safety case
        sc = SafetyCase(
            title="AutoDrive L4 Safety Case",
            system="Autonomous Vehicle",
            version="2.5"
        )
        
        # Build argument tree
        root = SafetyCaseNode(
            "G1", NodeType.GOAL,
            "AutoDrive L4 is acceptably safe for urban operation"
        )
        
        # Context
        context = SafetyCaseNode(
            "C1", NodeType.CONTEXT,
            "ODD: Urban streets, <45 mph, daylight, dry weather"
        )
        root.add_child(context)
        
        # Strategy
        strategy = SafetyCaseNode(
            "S1", NodeType.STRATEGY,
            "Argument by hazard analysis and mitigation"
        )
        root.add_child(strategy)
        
        # Sub-goals
        g11 = SafetyCaseNode(
            "G1.1", NodeType.GOAL,
            "All significant hazards have been identified"
        )
        strategy.add_child(g11)
        
        # Evidence
        sn1 = SafetyCaseNode(
            "Sn1", NodeType.SOLUTION,
            "STPA Analysis Report (Doc-001)"
        )
        g11.add_child(sn1)
        
        sn2 = SafetyCaseNode(
            "Sn2", NodeType.SOLUTION,
            "HAZOP Study Results (Doc-002)"
        )
        g11.add_child(sn2)
        
        sc.set_root(root)
        
        # Export
        sc.export_markdown("safety_case.md")
        
        # Check for gaps
        gaps = sc.find_unsupported_goals()
        if gaps:
            print(f"\n⚠️ Found {len(gaps)} unsupported goals:")
            for g in gaps:
                print(f"  - {g.id}: {g.text}")

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What are the three main components of a safety case?

**A1:**

1. **Claims**: Assertions about system safety
2. **Arguments**: Logical reasoning linking claims to evidence
3. **Evidence**: Data, test results, analyses proving claims

────────────────────────────────────────────────────────────────────

**Q2:** What does "ALARP" mean in safety case context?

**A2:**

**ALARP** = As Low As Reasonably Practicable

Residual risk is acceptable if:
- Risk reduced to lowest level feasible
- Further reduction is grossly disproportionate (cost vs benefit)
- Must demonstrate cost-benefit analysis

────────────────────────────────────────────────────────────────────

**Q3:** Why is independent safety assessment important?

**A3:**

- **Challenge assumptions**: Independent reviewer questions claims
- **Verify sufficiency**: Check evidence quality and completeness
- **Reduce bias**: Developer has vested interest, assessor is neutral
- **Regulatory confidence**: Regulator trusts independent opinion
- **Identify gaps**: Fresh eyes find missing arguments/evidence

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

**Planning:**
- [ ] Identify regulatory requirements (CAP 670, Def Std 00-56, etc.)
- [ ] Define system scope and Operational Design Domain (ODD)
- [ ] Appoint safety case owner (accountable person)
- [ ] Engage independent safety assessor (early involvement)

**Argument Development:**
- [ ] Define top-level safety claim
- [ ] Decompose into sub-claims (strategies)
- [ ] Identify required evidence for each claim
- [ ] Map hazards to claims (traceability)
- [ ] Review argument structure (peer review)

**Evidence Collection:**
- [ ] Conduct safety analyses (HAZOP, FMEA, FTA, STPA)
- [ ] Perform testing (unit, integration, system, validation)
- [ ] Document design decisions (rationale)
- [ ] Collect operational data (if available)
- [ ] Obtain compliance evidence (standards, certifications)

**Documentation:**
- [ ] Create GSN diagrams (visual argument)
- [ ] Write safety case report (narrative)
- [ ] Link evidence to claims (traceability matrix)
- [ ] Document assumptions and limitations
- [ ] Version control (configuration management)

**Review & Assessment:**
- [ ] Internal review (technical team)
- [ ] Independent safety assessment (ISA)
- [ ] Address findings (close gaps, strengthen arguments)
- [ ] Regulator review (submit for approval)

**Maintenance:**
- [ ] Update safety case for design changes (MOC)
- [ ] Incorporate lessons learned (incidents, near-misses)
- [ ] Periodic review (annual, or after significant events)
- [ ] Re-assessment (if major changes)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Safety case = Argument + Evidence** → Structured proof system is safe

2️⃣ **Goal-based regulation** → Flexibility vs prescriptive standards

3️⃣ **Claims hierarchy** → Top claim decomposes to sub-claims to evidence

4️⃣ **GSN notation** → Standard graphical language for safety arguments

5️⃣ **Evidence quality** → Relevant, sufficient, current, trustworthy

6️⃣ **ALARP principle** → Residual risk as low as reasonably practicable

7️⃣ **Living document** → Maintained through lifecycle, updated with changes

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **SAFETY CASE DEVELOPMENT CHEATSHEET COMPLETE**  
**Created:** January 14, 2026  
**Coverage:** Safety case fundamentals, regulatory context, claims hierarchy,  
argument patterns, evidence types, autonomous vehicle example, GSN notation,  
best practices, tools, Python safety case builder

════════════════════════════════════════════════════════════════════
