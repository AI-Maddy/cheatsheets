# IEC 61508 Part 3 Cheatsheet (Edition 2, 2010)

**Standard Title**: Functional safety of electrical/electronic/programmable electronic safety-related systems – Part 3: Software requirements

**Scope**: Applies to safety-related software in E/E/PE systems. Focuses on avoiding and controlling systematic faults in software to achieve required **Systematic Capability (SC)** (replaces SIL for software in Edition 2; SC 1–4 corresponds to SIL 1–4).

**Key Concepts**:
- Software safety functions and systematic capability must be specified.
- Uses V-model lifecycle.
- Techniques/measures graded by SC level (higher SC = more rigorous).
- Emphasis on independence in verification/validation for higher SC.

## Software Safety Lifecycle (Clause 7, Figure 3)

| Phase | Description | Key Outputs |
|-------|-------------|-------------|
| 7.1 Software safety requirements specification | Specify software safety functions, SC, properties (e.g., capacity, response time). | Software safety requirements spec. |
| 7.2 Software architecture design | Design modular, semi-formal methods; avoid/control faults. | Software architecture. |
| 7.3 Support tools and languages | Select suitable tools/languages (e.g., qualified compilers). | Tool qualification records. |
| 7.4 Software detailed design & implementation | Detailed design, coding; use structured methods. | Module design, source code. |
| 7.5 Software module testing | Test individual modules. | Module test results. |
| 7.6 Software integration testing | Integrate and test (hardware-software + software-software). | Integration test results. |
| 7.7 Software safety validation | Validate against requirements. | Validation report. |
| 7.8 Software modification | Impact analysis, re-verification/validation. | Modification records. |
| 7.9 Software verification | Ongoing checks throughout lifecycle. | Verification reports. |

## Key Techniques and Measures (Annex A – Normative Guide)

Techniques are **HR** (Highly Recommended), **R** (Recommended), **NR** (Not Recommended), or -- (no recommendation) depending on SC level.

### Common Tables Summary

| Table | Topic | SC1 | SC2 | SC3 | SC4 |
|-------|-------|-----|-----|-----|-----|
| A.1 | Software safety requirements specification | Semi-formal methods R | Semi-formal HR | Formal methods R | Formal methods HR |
| A.2 | Software architecture | Modularization HR, defensive programming R | Error detecting/correcting codes R | Diverse programming HR for higher |
| A.3 | Support tools and languages | Suitable languages (e.g., limited subsets) | Avoid full variability languages unless justified |
| A.4 | Detailed design | Structured programming HR | Forward traceability HR |
| A.5 | Code implementation | Structured code HR, no dynamic objects for higher SC |
| A.6 | Module testing | Boundary value analysis R | Probabilistic testing HR for SC4 |
| A.7 | Integration testing | Dynamic analysis HR for higher |
| A.8 | Validation | Functional/black-box testing HR |
| A.9 | Modification | Impact analysis HR |

**Notes on Recommendations**:
- **HR**: Strongly advised; alternatives need strong justification.
- For SC4: Very rigorous (e.g., formal proofs, diverse teams).
- Avoid recursion, dynamic memory, interrupts unless justified for higher SC.

### Popular Techniques by Phase

- **Specification/Architecture**: Semi-formal (e.g., UML), modular design, fault detection (watchdogs).
- **Coding**: Limited language subsets (e.g., MISRA C), no goto/unconditional branches.
- **Testing**: 100% statement/branch coverage for higher SC; static analysis HR.
- **Tools**: Qualification required if tool can insert errors (T-class: T1 low, T3 high impact).

## Systematic Capability (SC)

- Confidence that systematic safety integrity meets SIL requirements.
- Achieved via techniques in tables + competence + processes.

## Other Important Clauses

- **Clause 6**: Management of safety-related software (competence, procedures).
- **Clause 8**: Functional safety assessment (independent for higher SC).
- **Annex F**: Non-interference (for mixed SC elements).
- **Annex G**: Tailoring for data-driven systems (e.g., AI/ML – guidance only).

**Tips for Compliance**:
- Use V-model: Left side specification/design, right side testing/validation.
- Traceability throughout.
- Higher SC requires more independence and rigor.
- Justify any deviations from HR techniques.

This cheatsheet summarizes key elements for quick reference. For full compliance, consult the official IEC 61508-3:2010 standard.