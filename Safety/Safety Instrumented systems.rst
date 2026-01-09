
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**Safety Instrumented System (SIS) Cheat Sheet**  
(focused on **IEC 61508 / IEC 61511** standards – functional safety of safety instrumented systems, with emphasis on **hardware**, **software** and **system-level** aspects – valid for industrial/process/automation projects in 2025–2026)

🎓 1. Core SIS Concepts & Architecture

Term / Concept                | One-Line Explanation
------------------------------|---------------------------------------------------------------
**SIS**                       | Safety Instrumented System – dedicated system that implements one or more safety instrumented functions (SIFs)
**SIF**                       | Safety Instrumented Function – function intended to achieve or maintain a safe state (sensor → logic → final element)
**Safety Integrity Level (SIL)** | Discrete level (1–4) defining required risk reduction (higher SIL = lower acceptable failure probability)
**Process Safety Time (PST)** | Maximum time allowed from hazardous event detection to safe state achievement
**Proof Test Interval (PTI)** | Time between periodic proof tests (strongly influences achievable SIL)
**Safe Failure Fraction (SFF)** | (Safe + Dangerous Detected) / Total dangerous failures (used in Route 1H hardware fault tolerance)
**Hardware Fault Tolerance (HFT)** | Number of faults that can occur without losing the safety function (HFT=0 → 1oo1, HFT=1 → 1oo2)
⭐ **PFDavg**                    | Average Probability of Failure on Demand – key metric for low-demand mode SIFs
⭐ **PFH**                       | Probability of dangerous Failure per Hour – key metric for continuous/high-demand mode SIFs

📌 2. SIL Requirements Table (IEC 61508 / 61511 simplified – most used targets)

SIL | Low Demand Mode (PFDavg) | High / Continuous Demand Mode (PFH) | Typical HFT (1oo1 architecture) | Typical Application Examples
----|---------------------------|--------------------------------------|----------------------------------|--------------------------------
⭐ **SIL 1** | 10⁻² – 10⁻¹               | 10⁻⁶ – 10⁻⁵                         | HFT = 0                          | Non-critical alarms, basic interlocks
**SIL 2** | 10⁻³ – 10⁻²               | 10⁻⁷ – 10⁻⁶                         | HFT = 0                          | Most common in process industry (pressure relief, ESD)
**SIL 3** | 10⁻⁴ – 10⁻³               | 10⁻⁸ – 10⁻⁷                         | HFT = 1 (1oo2)                   | High-risk shutdowns, burner management
**SIL 4** | 10⁻⁵ – 10⁻⁴               | 10⁻⁹ – 10⁻⁸                         | HFT ≥ 1 (often 1oo2D or 2oo3)    | Very rare – nuclear, some railway signaling

🏗️ 3. System-Level Architecture Patterns

Architecture   | Voting       | HFT | Typical Achievable SIL | Common Use Case                          | Diagnostic Coverage Needed
--------------|--------------|-----|------------------------|------------------------------------------|---------------------------
1oo1          | Single       | 0   | SIL 1–2 (limited)      | Simple low-risk interlocks               | Medium–High
1oo1D         | Single + diag| 0   | SIL 2–3                | Monolithic PLC with 🟢 🟢 good diagnostics     | Very high
1oo2          | 1-out-of-2   | 1   | SIL 2–3                | Most common redundant sensor/logic setup | Medium–High
1oo2D         | 1oo2 + diag  | 1   | SIL 3                  | High-demand shutdown systems             | Very high
2oo3          | 2-out-of-3   | 1   | SIL 3–4                | High-integrity voting (tolerates 1 fault)| High
⭐ 2oo4D         | 2oo4 + diag  | 2   | SIL 4                  | Extremely critical (rare)                | Extremely high

⭐ 🔧 4. Hardware (HW) Level – Key Requirements & Techniques

Aspect                        | SIL 1–2                          | SIL 3                              | SIL 4                              | Typical Techniques / Components
------------------------------|----------------------------------|------------------------------------|------------------------------------|--------------------------------
**Hardware Fault Tolerance**  | HFT=0 (1oo1 possible)            | HFT≥1 (1oo2 or better)             | HFT≥1–2 (diverse 1oo2D or 2oo3)    | Redundant I/O modules, diverse suppliers
**Safe Failure Fraction (SFF)** | Route 1H: ≥60–90%                | Route 1H: ≥90%                     | Route 1H: ≥99%                     | High diagnostic coverage sensors/actuators
**Route 2H**                  | Proven-in-use data               | Proven-in-use + high diagnostic    | Rarely used                        | Field failure data + FMEDA
**Diagnostic Coverage**       | 60–90%                           | 90–99%                             | >99%                               | Watchdog, loop monitoring, partial stroke testing
**Common Components**         | Standard PLC, solenoid valve     | SIL-certified PLC (Triconex, HIMA) | Diverse redundant controllers      | Safety relays, certified transmitters

⭐ 📡 5. Software (SW) Level – Key Requirements & Techniques

Aspect                        | SIL 1–2                          | SIL 3                              | SIL 4                              | Typical Techniques / Tools
------------------------------|----------------------------------|------------------------------------|------------------------------------|---------------------------
**Development Lifecycle**     | Simplified V-model               | Full V-model + formal methods      | Very strict + formal verification  | IEC 61508 Part 3 lifecycle
**Programming Language**      | Structured text, ladder, C       | Restricted subset (MISRA-like)     | Very restricted / formally verified| Structured text, SPARK Ada
**Modularity & Partitioning** | Recommended                      | Mandatory                          | Mandatory + strong isolation       | Separate safety & non-safety code
**Diagnostic Software**       | Basic self-test                  | Extensive self-diagnostics         | Comprehensive + diversity          | Watchdog, CRC, plausibility checks
**Verification & Validation** | Reviews + testing                | 100% coverage + fault injection    | Formal proof + exhaustive testing  | LDRA, VectorCAST, Astrée
**Change & Configuration**    | Controlled                       | Strict impact analysis             | Full re-verification on change     | Version control + baseline management

📚 6. Quick Reference – Most Painful Points at Each Level

Level       | Hardware Pain Points                          | Software Pain Points                          | System-Level Pain Points
------------|-----------------------------------------------|-----------------------------------------------|--------------------------
**SIL 2**   | Achieving sufficient SFF & diagnostic coverage| Unit test coverage & traceability             | Proof test interval too short → low PFD
**SIL 3**   | Need for HFT ≥ 1 & diverse redundancy         | Restricted coding + high diagnostic coverage  | Common-cause failure analysis (β-factor)
**SIL 4**   | Very high SFF, diverse HW channels            | Formal methods, extreme verification effort   | Extremely low PFH, full dependent failure analysis

📚 7. Quick One-liners (what functional safety engineers say)

- “SIL 3 almost always requires 1oo2D or better – 1oo1 is usually impossible.”
- “PFDavg is dominated by proof test interval – test more often or use better diagnostics.”
- “β-factor (common-cause failure) can kill your SIL 3 architecture.”
- “For SIL 4 you need formal methods or extremely proven-in-use data – no shortcuts.”
- “Partial stroke testing is the easiest way to get high diagnostic coverage on valves.”
- “Software for SIL 3/4 must be developed with strong independence from BPCS.”
- “FMEDA + field failure data is the only realistic way to prove Route 2H.”

🟢 🟢 Good luck with your SIS design!  
The majority of industrial/process SIS projects in 2026 target **SIL 2 or SIL 3** — **SIL 4** is very rare and extremely expensive. Focus on **🟢 🟢 good diagnostic coverage**, **reasonable proof test intervals**, and **dependent failure analysis** to achieve realistic targets.

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
