
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for ALARP** (As Low As Reasonably Practicable) — the core risk reduction principle used in safety engineering, especially in automotive (ISO 26262), railway (EN 50126/50128/50129), industrial (IEC 61508), process safety (IEC 61511), and UK HSE-regulated sectors (as of 2026).

⚙️ 1. ALARP – Core Definition & Principle

**ALARP** = **As Low As Reasonably Practicable**  
A risk is ALARP when it has been reduced **so far as is reasonably practicable**, balancing risk reduction against the cost, time, and effort required.

⭐ Three key zones (the classic "ALARP triangle / ALARP region"):

| Zone / Region              | Risk Level                  | Action Required                                      | Typical Acceptability |
|----------------------------|-----------------------------|------------------------------------------------------|-----------------------|
| **Intolerable / Unacceptable** | Very high (e.g. frequent fatalities) | Risk **must** be reduced (unless grossly disproportionate) | Almost never acceptable |
| **ALARP Region**           | Tolerable but not negligible | Reduce risk until further reduction is **not reasonably practicable** | Acceptable only if ALARP demonstrated |
| **Broadly Acceptable / Negligible** | Very low (e.g. < 1 in 10⁶ per year individual risk) | No further action required unless very low cost | Generally acceptable |

⚙️ 2. The ALARP Decision-Making Process (Standard Workflow)

1. **Identify the hazard** → Hazard Log / PHA / FMEA / HAZOP  
2. **Determine initial risk** → Severity × Frequency / Exposure × Controllability (e.g. SIL / ASIL / LOPA)  
3. **Apply inherent safety** → Eliminate / Substitute / Reduce (preferred order)  
4. **Apply safeguards** → Engineering controls → Administrative → PPE (hierarchy of control)  
5. **Calculate residual risk** → After all reasonably practicable measures  
6. **Compare with criteria** → Tolerability matrix / SIL target / quantitative criteria  
7. **Assess further measures** → Cost–Benefit Analysis (CBA), QRA, ALARP argument  
8. **Document ALARP argument** → Grossly Disproportionate Test (see below)  
9. **Independent review** → Safety assessor / independent verification  
10. **Monitor & review** → Throughout lifecycle (changes, incidents, new tech)

🟢 🟢 ✅ 3. Grossly Disproportionate Test – The Key ALARP Test

**UK HSE / IEC 61508 / ISO 26262 principle**  
Further risk reduction is **not** required only if the **cost is grossly disproportionate** to the risk reduction achieved.

**Practical test** (common industry thresholds):

| Risk Reduction Benefit                     | Cost considered grossly disproportionate when… |
|--------------------------------------------|------------------------------------------------|
| Prevents 1 fatality per year               | > £10–30 million                               |
| Prevents 1 serious injury per year         | > £1–5 million                                 |
| Prevents 1 minor injury per year           | > £100k–500k                                   |
| Reduces SIL/ASIL by one level              | > £5–20 million (ASIL D context)               |
| Reduces failure rate 10×                   | > 3–10× the cost of current solution           |

**Rule of thumb (2026)**:  
If the **cost of further reduction is 5–10× greater** than the **risk reduction benefit** (in monetized terms), it is usually considered grossly disproportionate.

⚙️ 4. ALARP Demonstration – Required Evidence (Documentation)

| Document / Artifact                  | Typical Content / Purpose                              | Mandatory for which level? |
|--------------------------------------|--------------------------------------------------------|----------------------------|
| **Hazard Log / Risk Register**       | All hazards, initial & residual risk, controls         | All ASIL / SIL             |
| **ALARP Argument / Justification**   | Why further measures are grossly disproportionate      | ASIL B–D, SIL 2–4          |
| **Cost–Benefit Analysis (CBA)**      | Quantified costs vs. risk reduction (QALY, £/life saved) | ASIL C–D, SIL 3–4          |
| **Options Analysis**                 | All considered alternatives + reasons for rejection    | ASIL C–D                   |
| **Independent Safety Assessment**    | Review & confirmation of ALARP claim                   | ASIL C–D, SIL 3–4          |
| **ALARP Demonstration Report**       | Summary evidence package                               | ASIL D, SIL 4              |

📌 5. ALARP vs Other Risk Criteria (Quick Comparison)

| Criterion / Region          | ALARP (UK / IEC)                              | Tolerable Risk (ISO 26262 / IEC 61508) | Broadly Acceptable Risk |
|-----------------------------|-----------------------------------------------|----------------------------------------|--------------------------|
| Risk must be reduced?       | Yes, unless grossly disproportionate          | Yes, to target SIL/ASIL                | No                       |
| Cost justification required?| Yes (CBA / grossly disproportionate test)     | No (SIL target is sufficient)          | No                       |
| Residual risk acceptable?   | Yes, if ALARP demonstrated                    | Yes, if SIL/ASIL target met            | Yes                      |
| Used in automotive?         | Yes (ISO 26262 allows ALARP argument)         | Primary (ASIL targets)                 | Yes (QM)                 |
| Used in avionics?           | Rarely (🟢 🟢 DO-178C is objective-based)           | Yes (DAL targets)                      | Yes                      |

📌 6. Quick Mnemonics & Rules of Thumb (2026 Practice)

- **ALARP ≠ As Low As Possible** → It is **not** about minimum risk at any cost  
- **Grossly disproportionate** → Cost 5–10× > benefit is usually accepted as disproportionate  
- **ALARP argument** → Must be **documented**, **traceable**, and **independently reviewed** for ASIL C/D  
- **Hierarchy of control** → Eliminate > Substitute > Engineering > Admin > PPE → always try higher levels first  
- **ALARP in ISO 26262** → Allowed when ASIL target is met but further reduction is still considered  
- **ALARP in practice** → Most ASIL D functions use decomposition + ALARP justification for residual risk

Use this cheatsheet when writing safety cases, performing risk assessments, or justifying why a certain risk level is acceptable in automotive, railway, or process safety projects.

🟢 🟢 Good luck with your safety engineering work!

================================================================================

**Last updated:** January 2026
