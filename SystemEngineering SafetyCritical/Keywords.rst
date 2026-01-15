🛡️ **Safety-Critical Systems Engineering — Essential Keywords**
═══════════════════════════════════════════════════════════════════

**Your Complete Reference for High-Integrity Systems Terminology**  
**Domains:** Automotive ⚙️ | Aerospace ✈️ | Medical 🏥 | Railway 🚆 | Nuclear ⚛️  
**Purpose:** Exam prep, literature search, safety case development, team training

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

📖 **INTRODUCTION**
───────────────────

This comprehensive keyword list covers **Safety-Critical Systems Engineering** 
(also called safety-critical engineering, high-integrity systems engineering, or 
functional safety engineering). Terms are grouped thematically with visual markers 
for rapid scanning and memorization.

**Use Cases:**
✅ Literature search & academic research
✅ Safety case development & argumentation
✅ Exam preparation (ASIL, SIL, DAL certifications)
✅ Team training & knowledge transfer
✅ Glossary creation & documentation
✅ Taxonomy building for safety domains

════════════════════════════════════════════════════════════════════🎯 **CORE CONCEPTS & DEFINITIONS**
───────────────────────────────────

**System Criticality:**

⭐ **Safety-critical system**  
   System whose failure could result in death, injury, or environmental damage

💊 **Life-critical system**  
   System directly responsible for sustaining human life (e.g., pacemakers)

🎯 **Mission-critical system**  
   System whose failure prevents mission completion (may not cause harm)

🛡️ **Functional safety**  
   Part of overall safety depending on correct functioning of E/E/PE systems

🔗 **Safety-related system**  
   System implementing safety functions (broader than safety-critical)

⚡ **E/E/PE system**  
   Electrical/Electronic/Programmable Electronic system

**Quality Attributes:**

🏆 **Dependability**  
   Ability to deliver service that can justifiably be trusted

⏱️ **Reliability**  
   Probability of failure-free operation over time

✅ **Availability**  
   Proportion of time system is operational

🔧 **Maintainability**  
   Ease of performing maintenance activities

🛡️ **Safety integrity**  
   Probability of safety function performing correctly

⚠️ **RISK & HAZARD MANAGEMENT**
────────────────────────────────

**Hazard Identification:**

🔥 **Hazard**  
   Source of potential harm (potential cause of accident)

⚡ **Hazardous event**  
   Event that can lead to harm (hazard + trigger conditions)

💥 **Accident**  
   Unplanned event resulting in death, injury, or damage

**Risk Analysis:**

📊 **Risk assessment**  
   Process of analyzing and evaluating risk (severity × likelihood)

🔍 **Hazard analysis**  
   Systematic identification of hazards and their consequences

📉 **Risk reduction**  
   Measures to reduce likelihood or severity of hazards

🎯 **Safety goal**  
   Top-level safety requirement derived from hazard analysis

🟢 **Tolerable risk**  
   Risk accepted in a given context (ALARP principle)

🟡 **Residual risk**  
   Risk remaining after risk reduction measures applied

**Analysis Models:**

🎀 **Bow-tie diagram / Bow-tie analysis**  
   Visual showing hazard → event → consequences + barriers

🧀 **Swiss cheese model**  
   Defense-in-depth layers with holes (James Reason model)

🌲 **Fault tree**  
   Top-down deductive analysis using logic gates (AND/OR)

🌳 **Event tree**  
   Bottom-up inductive analysis showing event sequences

🔬 **ANALYSIS & MODELING TECHNIQUES**
──────────────────────────────────────

**Bottom-Up Techniques (Start with Component Failures):**

📋 **FMEA** (Failure Modes and Effects Analysis)  
   Systematic review of component failure modes and their effects

📊 **FMECA** (Failure Modes, Effects and Criticality Analysis)  
   FMEA + criticality ranking (RPN = Severity × Occurrence × Detection)

**Top-Down Techniques (Start with Hazardous Events):**

🌲 **FTA** (Fault Tree Analysis)  
   Deductive logic tree from top event → basic events (AND/OR gates)

🧪 **HAZOP** (Hazard and Operability Study)  
   Structured brainstorming using guide words (MORE, LESS, NO, etc.)

🔄 **STPA** (Systems-Theoretic Process Analysis)  
   Modern technique based on systems theory & control loops (Nancy Leveson)

**Early-Phase Analysis:**

🚀 **Preliminary Hazard Analysis (PHA)**  
   Initial hazard identification during concept/design phase

🏗️ **System hazard analysis**  
   System-level hazard identification across all subsystems

💻 **Software hazard analysis**  
   Software-specific hazard identification (logic errors, timing)

**Failure Dependencies:**

🔗 **Common cause failure**  
   Single event causing multiple component failures

❌ **Single point of failure (SPOF)**  
   Component whose failure causes system failure (no redundancy)

🔁 **Common mode failure**  
   Identical failures in redundant components due to shared flaw

🏅 **SAFETY INTEGRITY & CLASSIFICATION**
─────────────────────────────────────────

**Safety Levels by Domain:**

🔢 **SIL** (Safety Integrity Level)  
   IEC 61508 levels 1–4 (SIL 4 = highest, 10⁻⁸ to 10⁻⁹ PFH)

🚗 **ASIL** (Automotive Safety Integrity Level)  
   ISO 26262 levels QM, A, B, C, D (ASIL D = highest integrity)

✈️ **DAL** (Design Assurance Level)  
   DO-178C/DO-254 levels E, D, C, B, A (DAL A = catastrophic)

**Automotive Specific:**

🔴 **ASIL D**  
   Highest automotive safety level (life-threatening hazards)

⚪ **QM** (Quality Management)  
   No specific safety requirements (managed by quality processes)

**Industrial Levels:**

🟢 **SIL 1** → Low risk (minor injury)  
🟡 **SIL 2** → Medium risk (serious injury)  
🟠 **SIL 3** → High risk (death, multiple injuries)  
🔴 **SIL 4** → Very high risk (catastrophic, multiple deaths)

**Safety Metrics:**

📉 **PFD** (Probability of dangerous Failure on Demand)  
   For low-demand systems (safety function requested < 1/year)

⏱️ **PFH** (Probability of dangerous Failure per Hour)  
   For high-demand/continuous systems (e.g., automotive, process)

✅ **SFF** (Safe Failure Fraction)  
   Percentage of safe failures + detected dangerous failures

🔧 **HFT** (Hardware Fault Tolerance)  
   Number of faults system can tolerate (0, 1, 2 faults)

🏗️ **DEVELOPMENT & ASSURANCE PROCESSES**
──────────────────────────────────────────

**Lifecycle Models:**

📐 **V-model / V-lifecycle**  
   Left side = decomposition, right side = integration/verification

🔄 **Safety lifecycle**  
   Complete process from concept → decommissioning (IEC 61508)

**Requirements:**

📝 **Requirements engineering**  
   Elicitation, analysis, specification, validation of requirements

🛡️ **Safety requirements specification**  
   Formal documentation of safety-related requirements

🔗 **Traceability**  
   Bidirectional links between requirements → design → tests

**Verification & Validation:**

✅ **Verification & validation (V&V)**  
   Verification = "Are we building it right?" | Validation = "Are we building the right thing?"

🔍 **Independent verification and validation (IV&V)**  
   V&V performed by independent team (reduces confirmation bias)

**Model-Based Engineering:**

🎨 **MBSE** (Model-Based Systems Engineering)  
   Using models as primary artifacts (vs. documents)

📊 **SysML**  
   Systems Modeling Language (UML profile for systems engineering)

**Formal Techniques:**

🔬 **Formal methods / formal verification**  
   Mathematical proof of correctness (eliminates testing gaps)

✓ **Model checking**  
   Automated verification exhaustively checking all states

📐 **Theorem proving**  
   Interactive/automated proof using mathematical logic

**Coverage Metrics:**

🎯 **MC/DC** (Modified Condition/Decision Coverage)  
   Each condition independently affects decision outcome (DO-178C DAL A)

📊 **Structural coverage analysis**  
   Measuring code/model coverage (statement, branch, MC/DC)

🛠️ **FAULT HANDLING & ARCHITECTURE**
──────────────────────────────────────

**Resilience Strategies:**

🛡️ **Fault tolerance**  
   System continues operating despite faults (via redundancy)

⛔ **Fail-safe**  
   System enters safe state upon failure (e.g., traffic light → red)

✅ **Fail-operational / fail-active**  
   System continues full operation despite failure (aviation, autonomous)

**Redundancy Techniques:**

🔄 **Redundancy**  
   Duplicate components for fault tolerance (2oo2, 2oo3, TMR)

🎨 **Diversity**  
   Different implementations to avoid common mode failures

🔀 **Dissimilar redundancy**  
   Different technologies/algorithms (hardware + software diversity)

**Fault Management:**

🔍 **Fault detection**  
   Identifying presence of faults (built-in self-test, watchdogs)

🔬 **Fault isolation**  
   Determining fault location (diagnostics, voting)

♻️ **Recovery**  
   Restoring system to operational state (reboot, failover)

📉 **Graceful degradation**  
   Reduced functionality maintained (degrade vs. total failure)

📚 **STANDARDS & GUIDELINES** (Most Influential)
────────────────────────────────────────────────

**Foundation Standard:**

⭐ **IEC 61508**  
   *Functional safety of electrical/electronic/programmable electronic safety-related systems*  
   → Universal standard, basis for domain-specific standards (SIL 1–4)

**Domain-Specific Standards:**

🚗 **ISO 26262**  
   *Road vehicles – Functional safety*  
   → Automotive (ASIL QM, A, B, C, D) | Based on IEC 61508

✈️ **DO-178C**  
   *Software Considerations in Airborne Systems and Equipment Certification*  
   → Aviation software (DAL A-E) | Replaces DO-178B

🔌 **DO-254**  
   *Design Assurance Guidance for Airborne Electronic Hardware*  
   → Aviation hardware (complex electronic hardware)

🚆 **EN 50128 / EN 50129**  
   *Railway applications – Software / Safety-related electronic systems*  
   → Rail (SIL 0-4 per EN 50129)

🏭 **IEC 61511**  
   *Functional safety – Safety instrumented systems for the process industry*  
   → Chemical plants, oil & gas (SIL 1–4)

🏥 **IEC 62304**  
   *Medical device software – Software life cycle processes*  
   → Medical devices (Class A, B, C risk classification)

**Coding Standards:**

💻 **MISRA C / MISRA C++**  
   *Motor Industry Software Reliability Association guidelines*  
   → Subset of C/C++ for safety-critical (mandatory rules + advisory)

**Architectural Standards:**

🔧 **AUTOSAR**  
   *Automotive Open System Architecture*  
   → Standardized ECU software architecture (includes safety mechanisms)

✈️ **ARP4754 / ARP4761**  
   *Guidelines for development of civil aircraft systems / safety assessment*  
   → System development (ARP4754A) + safety assessment (ARP4761A)

🎓 **ADDITIONAL IMPORTANT TERMS**
──────────────────────────────────

**Assurance & Argumentation:**

📜 **Safety case / assurance case**  
   Structured argument + evidence that system is acceptably safe

🎯 **GSN** (Goal Structuring Notation)  
   Graphical notation for safety arguments (goals → strategies → evidence)

💬 **Safety argumentation**  
   Logical reasoning demonstrating safety claims are valid

🔍 **Confidence argument**  
   Argument about trustworthiness of evidence itself

**Reuse & Legacy:**

🔧 **Tool qualification**  
   Demonstrating development/verification tools won't introduce errors

✅ **Proven-in-use**  
   Credit for components with successful operational history

❓ **SOUP** (Software of Unknown Pedigree)  
   Pre-existing software not developed per safety standards (IEC 62304)

📦 **COTS** (Commercial Off-The-Shelf)  
   Commercial components used in safety systems (qualification challenges)

**Modern Practices:**

🔄 **Agile in safety-critical development**  
   Adapting agile methods for regulated environments (continuous compliance)

⚙️ **DevOps in safety-critical systems**  
   Continuous integration/deployment with safety assurance

════════════════════════════════════════════════════════════════════

✨ **TL;DR — QUICK MEMORIZATION GUIDE**
────────────────────────────────────────

**🎯 The Safety Triangle (Remember This First!):**

```
         HAZARD
           ⬇️
      HAZARDOUS EVENT
           ⬇️
        ACCIDENT
           ⬇️
          HARM
```

**🏅 Safety Levels by Domain (Memorize!):**

| Domain | Standard | Levels | Highest |
|:-------|:---------|:-------|:--------|
| 🚗 Automotive | ISO 26262 | QM, A, B, C, **D** | ASIL D |
| 🏭 Industrial | IEC 61508 | 1, 2, 3, **4** | SIL 4 |
| ✈️ Aerospace | DO-178C | E, D, C, B, **A** | DAL A |
| 🚆 Railway | EN 50128 | 0, 1, 2, 3, **4** | SIL 4 |
| 🏥 Medical | IEC 62304 | A, B, **C** | Class C |

**🔑 Key Analysis Techniques (Know These!):**

✅ **FMEA** → Bottom-up: What can fail?  
✅ **FTA** → Top-down: Why did it fail?  
✅ **HAZOP** → Brainstorm: What deviations?  
✅ **STPA** → Systems theory: What control failures?

**⭐ The V-Model (Universal Process!):**

```
Requirements → Design → Implementation
     ⬇️           ⬇️          ⬇️
Validation ← Integration ← Unit Testing
```

**🛡️ Fault Tolerance Hierarchy (Memorize!):**

1. **Fail-safe** → Go to safe state (best for trains)
2. **Fail-operational** → Keep working (best for aircraft)
3. **Graceful degradation** → Reduced function (good for autonomous)

**🎯 Traceability Chain (Always Required!):**

```
Hazards → Safety Goals → Safety Requirements → 
Design → Implementation → Tests → Evidence
```

════════════════════════════════════════════════════════════════════

📊 **USAGE GUIDE**
──────────────────

This keyword list is designed for:

✅ **Literature searches** — Use keywords in database queries  
✅ **Safety case development** — Terminology for argumentation  
✅ **Exam preparation** — Core concepts for certifications  
✅ **Team training** — Knowledge transfer to new engineers  
✅ **Glossary creation** — Building project documentation  
✅ **Taxonomy building** — Structuring safety knowledge bases

**🎯 Focus Areas by Domain:**

🚗 **Automotive:** ISO 26262, ASIL, AUTOSAR, FMEA, FTA  
✈️ **Aerospace:** DO-178C, DO-254, DAL, MC/DC, formal methods  
🏥 **Medical:** IEC 62304, SOUP, risk management, traceability  
🚆 **Railway:** EN 50128/50129, SIL, proven-in-use  
🏭 **Industrial:** IEC 61508, SIL, PFD/PFH, HAZOP

════════════════════════════════════════════════════════════════════

🎓 **COMMON EXAM QUESTIONS**
─────────────────────────────

❓ **What's the difference between SIL and ASIL?**  
   → SIL = IEC 61508 (industrial), ASIL = ISO 26262 (automotive)

❓ **What's the highest safety level?**  
   → SIL 4 (industrial), ASIL D (automotive), DAL A (aerospace)

❓ **FMEA vs. FTA — which to use?**  
   → FMEA = bottom-up (component view), FTA = top-down (system view)

❓ **What does MC/DC mean?**  
   → Modified Condition/Decision Coverage (each condition independently affects decision)

❓ **Fail-safe vs. fail-operational?**  
   → Fail-safe = safe shutdown, Fail-operational = keep working

❓ **What's a safety case?**  
   → Structured argument + evidence proving system is acceptably safe

════════════════════════════════════════════════════════════════════

**🚀 Next Steps**
─────────────────

If you need:

📖 **Expanded definitions** → Request detailed explanations  
🎯 **Domain filtering** → Focus on automotive/aerospace/medical/rail/nuclear  
📊 **Prioritization** → Rank by frequency/importance  
🗺️ **Mind maps** → Visual concept relationships  
📚 **Study guide** → Structured learning path

════════════════════════════════════════════════════════════════════

**Last updated:** January 14, 2026  
**Version:** 2.0 — Enhanced with emojis & memorization aids  
**Domains covered:** Automotive | Aerospace | Medical | Railway | Industrial

