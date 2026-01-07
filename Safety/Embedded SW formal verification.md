**cheatsheet for formal verification of embedded software** (2025–2026 perspective), focused on safety-critical domains (automotive ISO 26262 ASIL B–D, avionics DO-178C DAL A–C, industrial IEC 61508 SIL 3–4, medical IEC 62304 Class C, railway EN 50128 SIL 3–4).

### 1. Core Objectives in Embedded Formal Verification

| Objective                              | What it proves / prevents                              | Typical ASIL / DAL / SIL Target | Most Common Techniques / Tools |
|----------------------------------------|--------------------------------------------------------|----------------------------------|--------------------------------|
| Absence of runtime errors              | No overflow, null-pointer, division-by-zero, out-of-bounds | ASIL B–D, DAL B–A, SIL 2–4       | Abstract interpretation, bounded model checking |
| Freedom from undefined behavior        | No uninitialized variables, signed overflow, etc.      | ASIL B–D                         | CBMC, Frama-C + EVA, Astrée, Polyspace |
| Memory safety                          | No use-after-free, double-free, invalid pointer ops    | ASIL B–C, SIL 3                  | CBMC, CPAchecker, Frama-C WP   |
| Functional correctness                 | Code matches high-level specification / model          | ASIL C–D, DAL A, SIL 4           | Theorem proving (Coq, Isabelle), deductive verification |
| Absence of unreachable bad states      | No deadlock, livelock, overflow of critical variables  | ASIL C–D                         | Model checking (nuXmv, Kind2), k-induction |
| Timing & schedulability                | Worst-case execution time (WCET), no deadline miss     | ASIL B–D                         | aiT WCET, OTAWA, formal schedulability analysis |
| Freedom from interference              | Lower-ASIL code cannot corrupt higher-ASIL code        | ASIL B–D                         | MPU/PMU proofs, separation kernels (seL4 style) |
| Equivalence after refactoring / ECO    | Old & new version behave identically                   | ASIL C–D                         | Equivalence checking (JasperGold, OneSpin) |

### 2. Property Specification Languages & Notations

| Notation / Language        | Primary Use Case                              | Typical Tool Support                  | Readability / Expressiveness | Example (simplified) |
|----------------------------|-----------------------------------------------|---------------------------------------|-------------------------------|----------------------|
| **SVA (SystemVerilog Assertions)** | Temporal properties in RTL & low-level firmware | Questa Formal, JasperGold, OneSpin    | Very high                     | `assert property (@(posedge clk) req |-> ##[1:3] ack);` |
| **PSL (Property Specification Language)** | Hardware & firmware properties               | OneSpin, Questa, JasperGold           | High                          | `assert always (req -> next[2] ack);` |
| **LTL (Linear Temporal Logic)** | Linear-time properties on state machines     | nuXmv, SPIN, CPAchecker               | High                          | `G (req → F ack)` |
| **CTL (Computation Tree Logic)** | Branching-time properties                    | nuXmv, CPAchecker                     | High                          | `AG (error → AF recover)` |
| **ACSL (ANSI/ISO C Specification Language)** | C code contracts & invariants               | Frama-C + WP, Astrée                  | High (C-like)                 | `/*@ requires \valid(p); ensures \result == \old(*p) + 1; */` |
| **FRETish / Natural Language** | Human-readable → formal translation          | NASA FRET → LTL / SVA / ACSL          | Very high (readable)          | “Always, if brake pressed then speed decreases within 100 ms” |

### 3. Most Widely Used Tools & Their Sweet Spots (2026)

| Tool / Suite                  | Primary Target Code / Model | Main Verification Type                        | Open Source? | Qualification Level (ISO 26262 / DO-178C) | Typical Use Case in Embedded |
|-------------------------------|------------------------------|-----------------------------------------------|--------------|--------------------------------------------|------------------------------|
| **CBMC**                      | C / C++ firmware             | Bounded model checking + symbolic execution   | Yes          | TCL-2/3 / TQL-2/3                          | Drivers, RTOS kernels, low-level control |
| **CPAchecker**                | C / C++                      | Configurable (BMC, k-induction, abstract interp.) | Yes       | TCL-2/3 / TQL-2/3                          | Memory safety, protocol verification |
| **Frama-C + WP / EVA**        | C (bare-metal & RTOS)        | Deductive verification + abstract interpretation | Yes       | TCL-2/3 / TQL-2/3                          | Safety-critical C code (AUTOSAR, bare-metal) |
| **Astrée**                    | C (safety-critical)          | Sound abstract interpretation (no false negatives) | No        | TCL-1/2 / TQL-1/2                          | Runtime error freedom (ASIL C/D) |
| **Polyspace Code Prover**     | C / C++                      | Sound abstract interpretation                 | No           | TCL-1/2 / TQL-1/2                          | Automotive & avionics code bases |
| **nuXmv**                     | Finite-state models          | Symbolic model checking (LTL/CTL)             | Yes          | TCL-2/3 / TQL-2/3                          | State-machine verification, protocol |
| **JasperGold / Questa Formal**| RTL + firmware + SoC         | Industrial-strength model & equivalence checking | No        | TCL-1 / TQL-1                              | SoC, IP blocks, low-level drivers |
| **Isabelle/HOL / Coq**        | Algorithms, protocols, kernels | Interactive theorem proving                   | Yes          | TCL-1 (with evidence) / TQL-1              | Highest-assurance proofs (seL4 style) |

### 4. Property Types & Typical Formal Properties in Embedded Software

| Property Category              | Typical Formal Property (simplified)                        | Language / Tool Example                  | ASIL / SIL Target |
|--------------------------------|-------------------------------------------------------------|------------------------------------------|-------------------|
| No runtime error               | No overflow, no invalid pointer dereference                 | Astrée / Polyspace / CBMC                | B–D               |
| Memory safety                  | No use-after-free, no double-free                           | CBMC, CPAchecker                         | B–C               |
| Deadlock freedom               | Always possible to make progress                            | LTL in nuXmv                             | C–D               |
| Response guarantee             | If request then eventually acknowledge                      | `G (req → F ack)` in LTL                 | B–D               |
| Timing constraint              | If event then response within k cycles / time units        | Timed CTL / SVA                          | C–D               |
| Invariant preservation         | Critical variable always stays in safe range                | ACSL invariant in Frama-C                | C–D               |
| No buffer overflow             | Array index always within bounds                            | Astrée / Polyspace                       | B–D               |
| Functional equivalence         | Refactored code behaves exactly like original               | JasperGold / OneSpin                     | C–D               |

### 5. Quick Decision Guide – Which Technique / Tool?

| Goal / Constraint                          | Recommended Technique / Tool (2026)                 | ASIL / DAL / SIL Target |
|--------------------------------------------|-----------------------------------------------------|--------------------------|
| Prove no runtime errors in C code          | Astrée, Polyspace Code Prover, Frama-C + EVA        | ASIL B–D, SIL 2–4        |
| Find deep bugs in low-level firmware       | CBMC (bounded), CPAchecker                          | ASIL B–C, SIL 2–3        |
| Prove temporal properties of state machine | nuXmv, Kind2, SPIN                                  | ASIL C–D, SIL 3–4        |
| Prove mathematical correctness of algorithm | Isabelle/HOL, Coq, Why3                             | ASIL D, DAL A, SIL 4     |
| Prove equivalence after change             | JasperGold, Questa Formal, OneSpin                  | ASIL C–D                 |
| Full-chip / SoC formal sign-off            | JasperGold, OneSpin, Siemens EDA                    | ASIL D                   |

This cheatsheet covers the terminology, tools, and methods you will most frequently encounter in formal verification plans, safety manuals, and certification evidence for embedded software.

Good luck with your formal verification activities!