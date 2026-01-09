
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**Fault Tolerance Cheat Sheet**  
focused on **software architecture** and **software engineering** level techniques  
⭐ (oriented toward safety-critical / high-availability embedded & real-time systems – automotive ADAS, avionics, industrial, medical, rail – 2025–2026 practice)

📌 1. Fault Tolerance Goals & Categories

Goal                          | Typical Safety Integrity Level | Typical MTTF / FIT target | Typical Downtime target
------------------------------|--------------------------------|----------------------------|-------------------------
Fail-Safe                     | ASIL B / SIL 2 / DAL C         | 10⁶ – 10⁷ h                | seconds to minutes
Fail-Operational (single fault)| ASIL C–D / SIL 3–4 / DAL A–B   | 10⁸ – 10⁹ h                | < 100–500 ms
Fault-Tolerant (multiple faults)| ASIL D decomposed / DAL A     | > 10⁹ h                    | continuous

📌 2. Core Fault Tolerance Strategies at SW Level

Strategy                          | Faults Covered                     | Redundancy Type          | Typical Implementation Cost | Typical ASIL / DAL Target
----------------------------------|------------------------------------|---------------------------|------------------------------|---------------------------
**1oo2 / 1oo2D**                  | Single random / transient faults   | Homogeneous + diagnostic  | Medium                       | ASIL B–C
**2oo2**                          | Single fault (no false negative)   | Homogeneous               | Medium                       | ASIL B–C (with monitoring)
**1oo2D + diverse**               | Single + common-cause faults       | Diverse                   | High                         | ASIL C–D
**N-version programming**         | Design & implementation faults     | Diverse (3+ versions)     | Very high                    | ASIL D / DAL A (rare)
**Recovery blocks**               | Transient & design faults          | Primary + alternates      | High                         | ASIL C–D
**Acceptance / plausibility test**| Transient, sensor, SW faults       | No redundancy             | Low–Medium                   | ASIL B–C
**Watchdog + reset / failover**   | SW hang, timing faults             | Independent timer         | Low                          | ASIL A–B
**Temporal & value monitoring**   | Timing violations, out-of-range    | Independent checker       | Medium                       | ASIL B–D
**Partitioning & freedom from interference** | Cascading faults             | MMU / hypervisor / ARINC 653 | Medium–High                 | ASIL B–D

⭐ 🛡️ 3. Most Common Patterns in Safety-Critical SW Architecture (2025–2026)

⭐ Pattern                               | Description                                                                 | Typical Domain / Level       | Key Techniques / Artifacts
-------------------------------------|-----------------------------------------------------------------------------|-------------------------------|---------------------------
**Primary + Safety Monitor**          | Main channel does control, independent monitor checks plausibility / bounds | ADAS L2+/L3, avionics         | 1oo2D, diverse algorithms, separate core / partition
**Command + Monitor (C&M)**           | Two channels compute same function, compare results                        | Brake-by-wire, steer-by-wire  | Lockstep or diverse 1oo2D
**Triplex / Quad (N-modular redundancy)** | 3 or 4 independent channels vote (2oo3 / 3oo4)                           | Avionics flight control       | N-version + voting middleware
**Degraded Mode / Fail-Safe Ladder**  | Graceful degradation (high → medium → limp-home → safe state)              | Automotive powertrain, ADAS   | State machine + plausibility checks
**Temporal Firewall / Time-Triggered** | Strict time partitioning prevents timing faults propagation               | AUTOSAR Adaptive, ARINC 653   | TT scheduler, ARINC 653 partitions
**Data & Control Flow Monitoring**    | Independent checker validates data ranges, rates, sequences               | Engine control, braking       | Runtime assertions, value + temporal monitors

📡 4. Software Engineering Techniques for Fault Tolerance

Technique                             | Purpose                                      | When / ASIL Target     | Typical Tools / Standards
-------------------------------------|----------------------------------------------|------------------------|---------------------------
**Defensive programming**             | Prevent propagation of invalid data          | All levels             | Assertions, range checks, CRC
**Design by Contract**                | Explicit pre/post/invariants                 | ASIL B–D               | Eiffel-style, Frama-C, SPARK
**Memory protection / partitioning**  | Prevent fault propagation                    | ASIL B–D               | MMU, MPU, hypervisor (Xen, PikeOS)
**Error-correcting codes / CRC / E2E**| Detect / correct transmission errors         | ASIL B–D               | AUTOSAR E2E Profile 1/5, SOME/IP E2E
**Watchdog timer (independent)**      | Detect SW hang / infinite loop               | ASIL A–D               | Windowed watchdog + reset
**Software diversity**                | Reduce common cause failures                 | ASIL C–D               | Different compilers, algorithms, teams
**Formal verification**               | Prove absence of certain faults              | ASIL D / DAL A         | SPARK Ada, Frama-C, Astrée, Coq
**Static analysis with qualification**| Early detection of runtime faults            | ASIL B–D               | Polyspace, Astrée, QAC (TCL-2/3)
**Unit test + fault injection**       | Verify robustness against faults             | ASIL B–D               | VectorCAST, LDRA, Cantata
**Runtime monitoring / health checks**| Detect anomalies during operation            | ASIL B–D               | Heartbeat, sanity checks, plausibility

📚 5. Quick Reference – Fault Tolerance Cost vs Coverage

Technique                        | Cost (effort / compute) | Fault Coverage | Typical ASIL / DAL | Remark
--------------------------------|--------------------------|----------------|---------------------|--------
Defensive programming           | Low                      | Medium         | A–B                 | Baseline – always use
E2E / CRC protection            | Low                      | High (comm)    | B–D                 | Mandatory for comm
Watchdog + reset                | Low                      | Medium         | A–B                 | Almost universal
1oo2D plausibility monitor      | Medium                   | High           | B–C                 | Most common L2 pattern
Diverse 1oo2D                   | High                     | Very high      | C–D                 | L3 highway / braking
N-version + voting              | Very high                | Very high      | D / DAL A           | Avionics flight control
⭐ Formal methods                  | Very high                | Extremely high | D / DAL A           | Critical kernels only

🛡️ 6. Quick One-liners (what architects & safety engineers say)

- “No freedom from interference = no decomposition to B(D) or C(D).”
- “Plausibility monitor must be diverse and independent — same algorithm does not count.”
- “Watchdog must be independent (different clock source / core).”
- “E2E protection profile 5 is the safest for ASIL D communication.”
- “Temporal monitoring catches more than value monitoring in real-time systems.”
- “Software diversity is expensive — use it only when common-cause faults are credible.”
- “Runtime assertions are cheap insurance — turn them on in production for ASIL C/D.”

🟢 🟢 Good luck designing fault-tolerant software architecture!  
⭐ In 2025–2026 the most common realistic pattern in automotive ADAS is still **1oo2D with plausibility monitor + temporal firewall** — full N-version or formal proof remains reserved for the most critical kernels (e.g. braking arbitration, L3 fallback manager).

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
