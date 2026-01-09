
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for formal verification of embedded systems** (2025–2026 perspective).  
⭐ Focuses on the most commonly used methods, tools, languages, and patterns in safety-critical domains (automotive ASIL B–D, avionics DAL B–A, medical IEC 62304 Class C, industrial IEC 61508 SIL 3–4, railway EN 50128 SIL 3–4).

⚙️ 1. Formal Verification – Core Methods & When to Use

| Method / Technique              | Purpose / What it proves                              | Typical ASIL/DAL/SIL Target | Strength / Coverage | Main Tools (2026)                     | Typical Effort Level |
|---------------------------------|-------------------------------------------------------|------------------------------|----------------------|----------------------------------------|----------------------|
| **Model Checking**              | Exhaustive check that system never violates properties | ASIL B–D, DAL B–A, SIL 3–4  | Very high (complete for finite models) | CBMC, CPAchecker, nuXmv, SPIN, Java PathFinder | Medium–High |
| **Bounded Model Checking (BMC)**| Check properties up to fixed unrolling depth          | ASIL B–C, DAL C, SIL 2–3    | High (up to k steps) | CBMC, Boolector, Yices, Z3 (with BMC) | Medium |
| **k-Induction**                 | Prove properties for all depths (unbounded)           | ASIL C–D, DAL B–A           | Very high            | CPAchecker, nuXmv, Kind2               | High |
| **Theorem Proving**             | Prove correctness mathematically (interactive / automated) | ASIL D, DAL A, SIL 4      | Highest (human-guided soundness) | Isabelle/HOL, Coq, ACL2, Why3, Dafny | Very High |
| **Abstract Interpretation**     | Over-approximate possible states (sound but incomplete) | ASIL B–D, SIL 2–4         | Sound but may have false positives | Astrée, Polyspace Code Prover, Frama-C | Medium–High |
| **Equivalence Checking**        | Prove two implementations are functionally identical  | ASIL C–D (after ECO/refactoring) | Very high for equivalence | Synopsys Formality, Cadence Conformal, Yosys (open-source) | Medium |
| **Bounded Reachability**        | Check if 🔴 🔴 bad state is reachable within k steps        | ASIL B–C                    | High                 | CBMC, nuXmv, CPAchecker                | Medium |

⚙️ 2. Property Specification Languages (Most Used in Embedded)

| Language / Notation          | Typical Use Case                              | Tool Support (2026)                  | Expressiveness / Readability | Example Property |
|------------------------------|-----------------------------------------------|--------------------------------------|-------------------------------|------------------|
| **ACL2 / HOL**               | Theorem proving, full correctness proofs      | ACL2, Isabelle/HOL, Coq              | Very high (logic)             | “No deadlock possible” |
| **LTL (Linear Temporal Logic)** | Model checking of temporal properties       | nuXmv, SPIN, CPAchecker              | High                          | ``G (req → F ack)`` (request always eventually acknowledged) |
| **CTL (Computation Tree Logic)** | Branching-time properties                  | nuXmv, CPAchecker                    | High                          | ``AG (error → AF recover)`` |
| **PSL (Property Specification Language)** | Hardware & firmware properties             | Questa, JasperGold, OneSpin          | Very high (SVA-like)          | ``assert always (req |-> ##[1:5] ack);`` |
| **SVA (SystemVerilog Assertions)** | Assertions in RTL & firmware verification   | Questa, JasperGold, VC Formal        | Very high (industry standard) | ``assert property (@(posedge clk) disable iff (rst) req |-> ##2 ack);`` |
| **ACSLC / FRETish**          | Natural-language to formal properties         | NASA FRET, Kind2, nuXmv              | Medium–High (readable)        | “Always, if brake pressed then speed decreases within 100 ms” |

📌 3. Popular Formal Tools & Their Sweet Spots (2026)

| Tool / Suite                  | Type / Strength                               | 🟢 🟢 Best For (Embedded)                          | Open Source? | Typical Qualification Level | Learning Curve |
|-------------------------------|-----------------------------------------------|----------------------------------------------|--------------|------------------------------|----------------|
| **CBMC**                      | Bounded model checking (C/C++ code)           | Low-level firmware, drivers, RTOS kernels    | Yes          | TQL-2/3 (with evidence)      | Medium         |
| **CPAchecker**                | Configurable program analysis (C/C++)         | C code verification, memory safety           | Yes          | TQL-2/3                      | Medium–High    |
| **Frama-C + WP / EVA**        | Abstract interpretation + deductive verification | C code (bare-metal, RTOS tasks)              | Yes          | TQL-2/3                      | High           |
| **nuXmv**                     | Model checking (NuSMV successor)              | State-machine heavy designs, protocols       | Yes          | TQL-2/3                      | Medium         |
| **Astrée**                    | Static analyzer (sound abstract interpretation) | Runtime error freedom (overflow, pointer)    | No (commercial) | TQL-1/2                      | Medium         |
| **Polyspace Code Prover**     | Sound abstract interpretation (MathWorks)     | Proving absence of runtime errors            | No           | TQL-1/2                      | Medium         |
| **JasperGold / Questa Formal** | Industrial-strength hardware + firmware       | SoC, IP blocks, low-level drivers            | No           | TQL-1                        | High           |
⭐ | **OneSpin / Siemens EDA**     | High-assurance formal verification            | Safety-critical IP, processors               | No           | TQL-1                        | Very High      |
| **Isabelle/HOL / Coq**        | Interactive theorem proving                   | Mathematical correctness proofs              | Yes          | TQL-1 (with evidence)        | Very High      |

⭐ 🛡️ 4. Typical Formal Verification Flow in Safety-Critical Embedded Projects

1. **Requirements → Formal Properties**  
   → Translate safety goals into LTL/CTL/SVA/PSL (use FRETish or ACSLC for readability)

2. **Model Extraction**  
   → C code → CBMC / Frama-C  
   → RTL (Verilog/VHDL) → Questa / JasperGold  
   → System model → nuXmv / Kind2

3. **Bounded Checking (early stage)**  
   → Run BMC up to depth 20–100 (find bugs fast)

4. **Unbounded Proof / k-Induction**  
   → Prove properties hold for all time (ASIL C/D)

5. **Coverage & Evidence**  
   → Structural coverage (statement, branch, MC/DC)  
   → Proof certificates / witness traces

6. **Qualification / Confidence Building**  
   → Tool confidence level (TCL-1–5)  
   → Independent review or independent tool chain

⚙️ 5. Quick Decision Table – Which Technique / Tool?

| Goal / Constraint                          | Recommended Technique / Tool (2026)                 | ASIL / DAL / SIL Target |
|--------------------------------------------|-----------------------------------------------------|--------------------------|
| Prove absence of runtime errors in C code  | Astrée, Polyspace, Frama-C + EVA                    | ASIL B–D, SIL 2–4        |
| Exhaustive check of low-level driver/firmware | CBMC, CPAchecker                                   | ASIL B–C, SIL 2–3        |
| Prove temporal properties of state machine | nuXmv, Kind2, SPIN                                 | ASIL C–D, SIL 3–4        |
| Prove mathematical correctness of algorithm | Isabelle/HOL, Coq, Why3                            | ASIL D, DAL A, SIL 4     |
| Equivalence after ECO / refactoring        | JasperGold, Questa Formal, OneSpin                 | ASIL C–D                 |
| Full-chip / SoC formal sign-off            | JasperGold, OneSpin, Siemens EDA                   | ASIL D                   |

📌 6. Quick Mnemonics & Rules of Thumb (2026)

- **ASIL D / DAL A** → expect **theorem proving** or **industrial model checking** (JasperGold, OneSpin)
- **ASIL B–C / SIL 2–3** → **CBMC / CPAchecker** or **abstract interpretation** (Astrée / Polyspace) are most cost-effective
- **Bounded checking first** — find bugs fast before attempting full proofs
- **Model size limit** — keep state space < 10^6–10^8 states for practical model checking
⭐ - **Tool qualification** — TQL-1 (highest confidence) needed for ASIL D tools in critical paths
- **Property reuse** — write properties in SVA/PSL → reuse across simulation & formal
- **Formal + simulation** — formal proves absence of bugs → simulation shows presence of corner cases

This cheatsheet reflects current 🟢 🟢 best practices in automotive (ISO 26262), avionics (🟢 🟢 DO-178C), and industrial (IEC 61508) domains.

🟢 🟢 Good luck with your formal verification efforts!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
