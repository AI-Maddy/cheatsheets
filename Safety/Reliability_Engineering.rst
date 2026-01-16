⏱️ **Reliability Engineering — Quantitative Dependability Analysis**
════════════════════════════════════════════════════════════════════════════

**Your Complete Reference for MTBF, Failure Rate Analysis, and Reliability Prediction**  
**Metrics:** MTBF | MTTF | MTTR | Failure Rate (λ) | FIT | Weibull Analysis  
**Domains:** Automotive 🚗 | Avionics ✈️ | Railway 🚆 | Industrial 🏭 | Telecom 📡  
**Purpose:** Design analysis, component selection, warranty planning, maintenance scheduling

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — Quick Reference** (30-Second Overview!)
────────────────────────────────────────────────────

**Core Reliability Metrics:**

.. code-block:: text

   MTBF  = Mean Time Between Failures (repairable systems)
   MTTF  = Mean Time To Failure (non-repairable items)
   MTTR  = Mean Time To Repair
   λ     = Failure rate (constant rate assumption)
   FIT   = Failures In Time (failures per 10⁹ hours)

**Key Formulas:**

.. code-block:: text

   Reliability Function:
   R(t) = e^(-λt)  [constant failure rate]
   R(t) = e^(-(t/η)^β)  [Weibull distribution]
   
   MTBF = 1 / λ
   FIT  = λ × 10⁹
   
   Example: λ = 100 FIT = 100×10⁻⁹ /hr = 10⁻⁷ /hr
   MTBF = 1/10⁻⁷ = 10⁷ hours (1,142 years)

**Bathtub Curve (Failure Rate vs Time):**

.. code-block:: text

   Failure
   Rate (λ)
      │
      │  ╱───────────────╲___
      │ ╱ Infant      Useful   ╲ Wear-Out
      │╱  Mortality    Life      ╲
      │                           ╲___
      └──────────────────────────────→ Time
      │←─ Phase 1 ─→│←─ Phase 2 ─→│← Phase 3 →│
      
      Phase 1: Burn-in (decreasing λ) - manufacturing defects
      Phase 2: Random failures (constant λ) - exponential distribution
      Phase 3: Wear-out (increasing λ) - aging, fatigue

**Reliability Block Diagram (RBD) Quick Reference:**

+------------+------------------------+-----------------------------+
| Config     | Diagram                | Reliability Formula         |
+============+========================+=============================+
| **Series** | [A]──[B]──[C]          | R = R_A × R_B × R_C         |
+------------+------------------------+-----------------------------+
| **Parallel**| A──┐                  | R = 1 - (1-R_A)(1-R_B)      |
|            | B──┤──Output           |                             |
+------------+------------------------+-----------------------------+
| **k-out-of-n**| Vote (2-of-3)       | R = Σ C(n,k) R^k (1-R)^(n-k)|
+------------+------------------------+-----------------------------+

════════════════════════════════════════════════════════════════════════════

📖 **1. RELIABILITY FUNDAMENTALS**
════════════════════════════════════════════════════════════════════════════

1.1 Definitions
---------------

**Reliability R(t):**

*"Probability that a component/system will perform its intended function without failure for a specified period under stated conditions"*

.. code-block:: text

   R(t) = P(T > t)
   
   Where:
   - T = Time to failure (random variable)
   - t = Mission time (specified period)
   
   Example: R(1000) = 0.95
   → 95% probability of surviving 1000 hours

────────────────────────────────────────────────────────────────────────────

**Failure Rate λ(t):**

*"Instantaneous rate of failure at time t, given survival to time t"*

.. code-block:: text

   λ(t) = f(t) / R(t)
   
   Where:
   - f(t) = Probability density function of failure time
   - R(t) = Reliability function
   
   Special Case (Constant Failure Rate):
   λ(t) = λ = constant → Exponential distribution
   R(t) = e^(-λt)

────────────────────────────────────────────────────────────────────────────

**MTBF vs MTTF:**

**MTBF (Mean Time Between Failures):**
- For **repairable** systems
- Average time between successive failures
- Includes operating time + repair time

.. code-block:: text

   MTBF = Total Operating Time / Number of Failures
   
   Example: System operates 10,000 hours, fails 5 times
   MTBF = 10,000 / 5 = 2,000 hours

**MTTF (Mean Time To Failure):**
- For **non-repairable** components (replace when failed)
- Expected time until first failure
- Integral of reliability function

.. code-block:: text

   MTTF = ∫₀^∞ R(t) dt
   
   For exponential: MTTF = 1/λ = MTBF

────────────────────────────────────────────────────────────────────────────

**FIT (Failures In Time):**

*Industry-standard metric (especially semiconductors)*

.. code-block:: text

   1 FIT = 1 failure per 10⁹ device-hours
   
   Conversion:
   FIT = λ × 10⁹  [λ in failures/hour]
   λ = FIT / 10⁹
   
   MTBF = 10⁹ / FIT
   
   Example: Component rated at 50 FIT
   λ = 50 × 10⁻⁹ /hr = 5 × 10⁻⁸ /hr
   MTBF = 10⁹ / 50 = 2 × 10⁷ hours (2,283 years)

**Typical FIT Rates by Component:**

+-----------------------+------------------+-----------------------+
| Component             | FIT (typical)    | MTBF                  |
+=======================+==================+=======================+
| Resistor (0.1W, 25°C) | 0.01             | 10¹¹ hr (11 million yr)|
+-----------------------+------------------+-----------------------+
| Capacitor (ceramic)   | 1                | 10⁹ hr (114,000 yr)   |
+-----------------------+------------------+-----------------------+
| IC (CMOS logic)       | 10               | 10⁸ hr (11,400 yr)    |
+-----------------------+------------------+-----------------------+
| Microprocessor        | 100              | 10⁷ hr (1,142 yr)     |
+-----------------------+------------------+-----------------------+
| Electromechanical relay| 1,000           | 10⁶ hr (114 yr)       |
+-----------------------+------------------+-----------------------+

════════════════════════════════════════════════════════════════════════════

📖 **2. RELIABILITY DISTRIBUTIONS**
════════════════════════════════════════════════════════════════════════════

2.1 Exponential Distribution
-----------------------------

**When to Use:**
- Constant failure rate (useful life phase of bathtub curve)
- Random failures (not wear-out, not infant mortality)
- Memoryless property (past doesn't affect future)

**Probability Density Function (PDF):**

.. code-block:: text

   f(t) = λ e^(-λt)    for t ≥ 0

**Reliability Function:**

.. code-block:: text

   R(t) = e^(-λt)

**Cumulative Distribution Function (CDF):**

.. code-block:: text

   F(t) = 1 - R(t) = 1 - e^(-λt)

**Mean (MTTF):**

.. code-block:: text

   MTTF = 1/λ

**Example Calculation:**

.. code-block:: python

   import math
   
   # Component: λ = 10⁻⁵ failures/hour
   lambda_rate = 1e-5
   
   # Mission time: 1000 hours
   t_mission = 1000
   
   # Reliability
   R_t = math.exp(-lambda_rate * t_mission)
   print(f"Reliability at 1000 hr: {R_t:.6f} ({R_t*100:.4f}%)")
   # Output: 0.990050 (99.0050%)
   
   # Probability of failure before 1000 hr
   F_t = 1 - R_t
   print(f"Failure probability: {F_t:.6f} ({F_t*100:.4f}%)")
   # Output: 0.009950 (0.9950%)
   
   # MTTF
   MTTF = 1 / lambda_rate
   print(f"MTTF: {MTTF:,.0f} hours ({MTTF/8760:.1f} years)")
   # Output: MTTF: 100,000 hours (11.4 years)

────────────────────────────────────────────────────────────────────────────

**2.2 Weibull Distribution**
----------------------------

**When to Use:**
- Variable failure rate (covers all bathtub curve phases)
- Wear-out analysis (mechanical components, bearings, batteries)
- Accelerated life testing

**Probability Density Function:**

.. code-block:: text

   f(t) = (β/η) (t/η)^(β-1) e^(-(t/η)^β)
   
   Where:
   - β = Shape parameter (determines failure pattern)
   - η = Scale parameter (characteristic life)

**Reliability Function:**

.. code-block:: text

   R(t) = e^(-(t/η)^β)

**Failure Rate (Hazard Function):**

.. code-block:: text

   λ(t) = (β/η) (t/η)^(β-1)

**Shape Parameter β Interpretation:**

+------------+------------------+-----------------------------+
| β value    | Failure Pattern  | Application                 |
+============+==================+=============================+
| **β < 1**  | Decreasing λ(t)  | Infant mortality, burn-in   |
+------------+------------------+-----------------------------+
| **β = 1**  | Constant λ       | Random failures (exponential|
+------------+------------------+-----------------------------+
| **β > 1**  | Increasing λ(t)  | Wear-out, aging, fatigue    |
+------------+------------------+-----------------------------+
| **β = 2**  | Linear increase  | Wear-out (many mechanical)  |
+------------+------------------+-----------------------------+
| **β = 3.5**| Rapid increase   | Fatigue failures            |
+------------+------------------+-----------------------------+

**Example: Bearing Reliability**

.. code-block:: python

   import math
   
   # Bearing parameters (typical):
   beta = 2.0   # Shape (wear-out)
   eta = 10000  # Scale (characteristic life in hours)
   
   # Reliability at 5000 hours
   t = 5000
   R_t = math.exp(-(t/eta)**beta)
   print(f"Bearing reliability at 5000 hr: {R_t:.4f} ({R_t*100:.2f}%)")
   # Output: 0.7788 (77.88%)
   
   # Failure rate at 5000 hours
   lambda_t = (beta/eta) * (t/eta)**(beta-1)
   print(f"Failure rate at 5000 hr: {lambda_t:.2e} /hr")
   # Output: 1.00e-04 /hr
   
   # Mean time to failure (MTTF) for Weibull:
   import math
   from scipy.special import gamma
   MTTF_weibull = eta * gamma(1 + 1/beta)
   print(f"MTTF (Weibull): {MTTF_weibull:.0f} hours")
   # Output: 8,862 hours

────────────────────────────────────────────────────────────────────────────

**2.3 Normal Distribution**
---------------------------

**When to Use:**
- Wear-out failures with known mean and variance
- Fatigue life (cyclic loading)
- When failures cluster around mean lifetime

**Reliability Function (via CDF):**

.. code-block:: text

   R(t) = 1 - Φ((t - μ) / σ)
   
   Where:
   - μ = Mean time to failure
   - σ = Standard deviation
   - Φ = Standard normal CDF

**Example: LED Lifetime**

.. code-block:: python

   from scipy.stats import norm
   
   # LED parameters
   mu = 50000     # Mean lifetime (hours)
   sigma = 5000   # Standard deviation
   
   # Reliability at 40,000 hours
   t = 40000
   R_t = 1 - norm.cdf(t, loc=mu, scale=sigma)
   print(f"LED reliability at 40,000 hr: {R_t:.4f} ({R_t*100:.2f}%)")
   # Output: 0.9772 (97.72%)

────────────────────────────────────────────────────────────────────────────

**2.4 Lognormal Distribution**
------------------------------

**When to Use:**
- Failures from multiplicative effects
- Crack propagation, corrosion, electromigration
- Software debugging time

**Property:** If X ~ Lognormal, then ln(X) ~ Normal

.. code-block:: text

   f(t) = (1/(t σ√(2π))) e^(-(ln(t)-μ)²/(2σ²))

**Example:** Electromigration in IC interconnects

════════════════════════════════════════════════════════════════════════════

📖 **3. RELIABILITY BLOCK DIAGRAMS (RBD)**
════════════════════════════════════════════════════════════════════════════

3.1 Series Configuration
-------------------------

**All components must work for system to work**

.. code-block:: text

   [Component A]──[Component B]──[Component C]──[Output]
   R_A = 0.99      R_B = 0.98      R_C = 0.97
   
   R_system = R_A × R_B × R_C
            = 0.99 × 0.98 × 0.97
            = 0.9415 (94.15%)

**Implication:** System reliability ALWAYS less than weakest component

**Engineering Lesson:**  
Adding components in series **reduces** system reliability.  
*100-component series system with each R=0.99 → R_system = 0.99^100 = 0.366 (36.6%)*

────────────────────────────────────────────────────────────────────────────

**3.2 Parallel Configuration (Active Redundancy)**
---------------------------------------------------

**At least 1 component must work (1-out-of-n)**

.. code-block:: text

          ┌──[Component A]──┐
   Input ─┤                  ├─ Output
          └──[Component B]──┘
   R_A = R_B = 0.95
   
   R_system = 1 - (1 - R_A) × (1 - R_B)
            = 1 - (0.05) × (0.05)
            = 1 - 0.0025 = 0.9975 (99.75%)

**Generalized (n identical components):**

.. code-block:: text

   R_system = 1 - (1 - R)^n

**Example: Dual Redundancy**

.. code-block:: python

   R_component = 0.90
   n = 2
   
   R_system = 1 - (1 - R_component)**n
   print(f"Dual redundancy: {R_system:.4f} ({R_system*100:.2f}%)")
   # Output: 0.9900 (99.00%)
   
   # Triple redundancy
   n = 3
   R_system = 1 - (1 - R_component)**n
   print(f"Triple redundancy: {R_system:.4f} ({R_system*100:.2f}%)")
   # Output: 0.9990 (99.90%)

────────────────────────────────────────────────────────────────────────────

**3.3 k-out-of-n Configuration (Voting)**
-----------------------------------------

**At least k out of n components must work**

**Examples:**
- 2-out-of-3 (TMR with majority voting)
- 3-out-of-5 (high-availability cluster)

**Reliability Formula (binomial):**

.. code-block:: text

   R_system = Σ(i=k to n) C(n,i) R^i (1-R)^(n-i)
   
   Where:
   - C(n,i) = Binomial coefficient (n choose i)

**Example: 2-out-of-3 Voting (TMR)**

.. code-block:: python

   from math import comb
   
   R = 0.95  # Component reliability
   n = 3     # Total components
   k = 2     # Minimum required
   
   R_system = sum(comb(n, i) * R**i * (1-R)**(n-i) for i in range(k, n+1))
   print(f"2-out-of-3 reliability: {R_system:.6f} ({R_system*100:.4f}%)")
   # Output: 0.992750 (99.2750%)
   
   # Breakdown:
   # Exactly 2 work:  C(3,2) × 0.95² × 0.05¹ = 3 × 0.9025 × 0.05 = 0.135375
   # Exactly 3 work:  C(3,3) × 0.95³ × 0.05⁰ = 1 × 0.857375 × 1  = 0.857375
   # Total: 0.992750

────────────────────────────────────────────────────────────────────────────

**3.4 Standby Redundancy (Cold Standby)**
-----------------------------------------

**Backup component activated only when primary fails**

**Assumptions:**
- Perfect switching (instantaneous, 100% reliable)
- Standby doesn't fail while idle (cold standby)

**Reliability Formula (2-component standby):**

.. code-block:: text

   R_system(t) = e^(-λt) [1 + λt]
   
   Where:
   - λ = Failure rate of each component (identical)

**Comparison (R=0.90 per component):**

+--------------------+----------------+
| Configuration      | Reliability    |
+====================+================+
| Single component   | 0.90 (90%)     |
+--------------------+----------------+
| Parallel (active)  | 0.99 (99%)     |
+--------------------+----------------+
| Standby (cold)     | 0.995 (99.5%)  |
+--------------------+----------------+

**Advantage:** Standby better than active redundancy (standby unit doesn't wear)

════════════════════════════════════════════════════════════════════════════

📖 **4. RELIABILITY PREDICTION METHODS**
════════════════════════════════════════════════════════════════════════════

4.1 MIL-HDBK-217 (Parts Count Method)
--------------------------------------

**Purpose:** Predict failure rate from component counts

**Formula:**

.. code-block:: text

   λ_system = Σ (N_i × λ_base_i × π_Q × π_E × π_T × ...)
   
   Where:
   - N_i = Quantity of component type i
   - λ_base = Base failure rate from handbook
   - π_Q = Quality factor (mil-spec vs commercial)
   - π_E = Environment factor (ground fixed, airborne, missile)
   - π_T = Temperature stress factor

**Example: Simple PCB Assembly**

.. code-block:: text

   Component Inventory:
   - 20× Resistors (0.25W, carbon film)
   - 10× Capacitors (ceramic, 50V)
   - 5× ICs (CMOS logic, 14-pin DIP)
   - 1× Microprocessor (32-bit, 100-pin QFP)
   
   Environment: Ground, Benign (GB)
   Quality: Commercial (Grade B)
   
   From MIL-HDBK-217:
   - Resistor λ_base = 0.001 FIT (×20) = 0.02 FIT
   - Capacitor λ_base = 0.01 FIT (×10) = 0.1 FIT
   - IC λ_base = 0.5 FIT (×5) = 2.5 FIT
   - Microprocessor λ_base = 10 FIT (×1) = 10 FIT
   
   Total: 12.62 FIT
   MTBF = 10⁹ / 12.62 = 7.93×10⁷ hours (9,050 years)

**Limitations:**
- Outdated (last update: 1995, Notice 2 in 2019)
- Conservative (overpredicts failures)
- Doesn't account for modern manufacturing quality

────────────────────────────────────────────────────────────────────────────

**4.2 Telcordia SR-332 (Telecom)**
----------------------------------

**Successor to Bellcore TR-332**

**Improvements over MIL-HDBK-217:**
- Field data-driven (actual return rates)
- Accounts for burn-in
- Temperature-humidity stress models

**Application:** Telecom equipment (routers, switches, base stations)

────────────────────────────────────────────────────────────────────────────

**4.3 IEC TR 62380 (Automotive)**
---------------------------------

**Purpose:** Reliability prediction for automotive electronics

**Factors:**
- Automotive environment (temperature cycles, vibration, humidity)
- Mission profile (urban, highway, off-road)
- Quality level (Tier-1 vs Tier-2 supplier)

**Example Mission Profile:**

.. code-block:: text

   Automotive ECU (15-year lifetime):
   - 50% urban (start-stop, thermal cycles)
   - 40% highway (steady-state)
   - 10% off-road (vibration, shock)
   
   Temperature extremes: -40°C to +125°C

────────────────────────────────────────────────────────────────────────────

**4.4 Physics-of-Failure (PoF)**
--------------------------------

**Modern Approach:** Model failure mechanisms, not just statistics

**Common Failure Mechanisms:**

**Thermal Cycling (Solder Joint Fatigue):**

.. code-block:: text

   Coffin-Manson Equation:
   N_f = C (ΔT)^(-m)
   
   Where:
   - N_f = Cycles to failure
   - ΔT = Temperature range
   - C, m = Material constants
   
   Example: ΔT = 100°C → N_f = 1,000 cycles
            ΔT = 50°C  → N_f = 8,000 cycles (2^m factor, m≈3)

**Electromigration (IC Interconnects):**

.. code-block:: text

   Black's Equation:
   MTTF = A j^(-n) e^(E_a / kT)
   
   Where:
   - j = Current density
   - E_a = Activation energy
   - T = Temperature (Kelvin)
   - n ≈ 2

**Advantage:** Predict failures before field deployment (accelerated testing)

════════════════════════════════════════════════════════════════════════════

📖 **5. ACCELERATED LIFE TESTING (ALT)**
════════════════════════════════════════════════════════════════════════════

5.1 Arrhenius Model (Temperature Acceleration)
-----------------------------------------------

**Purpose:** Predict lifetime at normal temperature from high-temp testing

**Acceleration Factor:**

.. code-block:: text

   AF = exp[(E_a/k) × (1/T_use - 1/T_test)]
   
   Where:
   - E_a = Activation energy (eV)
   - k = Boltzmann constant (8.617×10⁻⁵ eV/K)
   - T_use = Use temperature (Kelvin)
   - T_test = Test temperature (Kelvin)

**Example: IC Lifetime Prediction**

.. code-block:: python

   import math
   
   E_a = 0.7  # eV (typical for ICs)
   k = 8.617e-5  # eV/K
   T_use = 25 + 273  # 25°C = 298K
   T_test = 125 + 273  # 125°C = 398K
   
   AF = math.exp((E_a/k) * (1/T_use - 1/T_test))
   print(f"Acceleration Factor: {AF:.1f}×")
   # Output: ~100× (100 hours at 125°C = 10,000 hours at 25°C)
   
   # If 10 failures occur in 100 hours at 125°C:
   failures_test = 10
   hours_test = 100
   lambda_test = failures_test / (hours_test * num_units)
   
   # Actual lifetime at 25°C:
   lambda_use = lambda_test / AF
   MTBF_use = 1 / lambda_use

────────────────────────────────────────────────────────────────────────────

**5.2 Highly Accelerated Life Test (HALT)**
-------------------------------------------

**Purpose:** Find design weaknesses rapidly

**Stresses Applied:**
- Temperature cycling (rapid ramp rates: 50°C/min)
- Vibration (6-axis, 20-80 grms)
- Voltage margining (±20% of nominal)
- Combined stresses (thermal + vibration simultaneously)

**Procedure:**

1. **Step Stress:** Increase stress incrementally until failure
2. **Find Destruct Limit:** Maximum stress before catastrophic failure
3. **Design Margin:** Difference between destruct limit and operational limit

**Example:**

.. code-block:: text

   Operational temperature: -40°C to +85°C
   Destruct limit (HALT): -60°C to +125°C
   Design margin: 20°C on each end
   
   → Confidence in field reliability

────────────────────────────────────────────────────────────────────────────

**5.3 Highly Accelerated Stress Screening (HASS)**
--------------------------------------------------

**Purpose:** Production screening to catch infant mortality

**Applied to:** Every unit shipped (100% screening)

**Typical Profile:**

.. code-block:: text

   Duration: 4-8 hours per unit
   Temperature: -20°C to +60°C (5 cycles)
   Vibration: 10 grms (operating product during cycles)
   
   Result: Precipitate latent defects (solder voids, cracked components)

════════════════════════════════════════════════════════════════════════════

📖 **6. FIELD DATA ANALYSIS**
════════════════════════════════════════════════════════════════════════════

6.1 Calculating MTBF from Field Returns
----------------------------------------

**Scenario:** 1,000 units deployed, 20 failures in first year

.. code-block:: python

   units_deployed = 1000
   failures = 20
   operating_hours_per_unit_per_year = 24 * 365  # Continuous operation
   
   total_operating_hours = units_deployed * operating_hours_per_unit_per_year
   MTBF = total_operating_hours / failures
   
   print(f"Total operating hours: {total_operating_hours:,}")
   print(f"MTBF: {MTBF:,.0f} hours ({MTBF/8760:.1f} years)")
   # Output: 8,760,000 total hours, MTBF = 438,000 hours (50 years)

────────────────────────────────────────────────────────────────────────────

**6.2 Confidence Intervals**
----------------------------

**Chi-Square Method:**

.. code-block:: text

   Lower bound (90% confidence):
   MTBF_lower = 2T / χ²(α/2, 2r+2)
   
   Upper bound:
   MTBF_upper = 2T / χ²(1-α/2, 2r)
   
   Where:
   - T = Total test time
   - r = Number of failures
   - α = 1 - confidence level

**Example:**

.. code-block:: python

   from scipy.stats import chi2
   
   T = 10000  # Test hours
   r = 5      # Failures
   alpha = 0.10  # 90% confidence (two-sided)
   
   MTBF_point = T / r
   
   MTBF_lower = (2*T) / chi2.ppf(1 - alpha/2, 2*r + 2)
   MTBF_upper = (2*T) / chi2.ppf(alpha/2, 2*r)
   
   print(f"MTBF estimate: {MTBF_point:.0f} hours")
   print(f"90% confidence interval: [{MTBF_lower:.0f}, {MTBF_upper:.0f}]")
   # Output: MTBF = 2000 hr, CI = [1075, 4658] hr

**Wide intervals with few failures → Need more data!**

════════════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════════════════════════════════════════════════════════

**Q1:** A system has 3 components in series with reliabilities 0.95, 0.98, and 0.99. Calculate system reliability.

**A1:**

**Series configuration:** All must work

.. code-block:: text

   R_system = R_A × R_B × R_C
            = 0.95 × 0.98 × 0.99
            = 0.921 (92.1%)

**Key insight:** System reliability (92.1%) is less than any individual component.

────────────────────────────────────────────────────────────────────────────

**Q2:** Convert λ = 50 FIT to MTBF in years.

**A2:**

.. code-block:: text

   MTBF (hours) = 10⁹ / FIT
                = 10⁹ / 50
                = 2 × 10⁷ hours
   
   MTBF (years) = 2 × 10⁷ / 8760
                = 2,283 years

────────────────────────────────────────────────────────────────────────────

**Q3:** What is the difference between active redundancy (parallel) and cold standby?

**A3:**

**Active Redundancy (Parallel):**
- Both units operating simultaneously
- Either unit can carry full load
- Standby unit wears even when not needed

**Cold Standby:**
- Backup unit OFF (not operating) until primary fails
- Switching required when primary fails
- Standby unit doesn't age while idle → Higher overall reliability

*Example:* For R=0.90 per component:
- Parallel: R_sys = 1 - (0.1)² = 0.99 (99%)
- Cold standby: R_sys ≈ 0.995 (99.5%) — better!

────────────────────────────────────────────────────────────────────────────

**Q4:** Interpret Weibull shape parameter: β = 0.5, β = 1, β = 3

**A4:**

- **β = 0.5** → **Infant mortality** (decreasing failure rate)
  - Early failures from manufacturing defects
  - Burn-in testing recommended

- **β = 1** → **Random failures** (constant failure rate)
  - Exponential distribution (memoryless)
  - Useful life period

- **β = 3** → **Wear-out** (increasing failure rate)
  - Aging, fatigue, degradation
  - Preventive replacement recommended

────────────────────────────────────────────────────────────────────────────

**Q5:** Calculate 2-out-of-3 voting system reliability if each component R=0.90.

**A5:**

**Method:** At least 2 of 3 must work

.. code-block:: text

   R_system = P(exactly 2 work) + P(all 3 work)
   
   P(exactly 2) = C(3,2) × R² × (1-R)
                = 3 × 0.90² × 0.10
                = 3 × 0.81 × 0.10 = 0.243
   
   P(all 3) = R³ = 0.90³ = 0.729
   
   R_system = 0.243 + 0.729 = 0.972 (97.2%)

**Comparison:**
- Single unit: 90%
- Dual redundancy (1oo2): 99%
- TMR (2oo3): 97.2%

*Why TMR < Dual?* Because 2oo3 requires 2 to work (stricter than 1oo2).

════════════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────────────────────────────────────────────────────

**Metrics:**
- [ ] Calculate MTBF, MTTF, MTTR
- [ ] Convert between λ, FIT, and MTBF
- [ ] Compute reliability R(t) = e^(-λt)

**Distributions:**
- [ ] Apply exponential distribution (constant λ)
- [ ] Interpret Weibull parameters (β, η)
- [ ] Recognize bathtub curve phases

**RBD:**
- [ ] Compute series system reliability (product)
- [ ] Compute parallel redundancy: 1-(1-R)^n
- [ ] Calculate k-out-of-n voting (binomial)

**Prediction:**
- [ ] Use MIL-HDBK-217 parts count method
- [ ] Apply Arrhenius model for temperature acceleration
- [ ] Interpret HALT destruct limits

**Field Analysis:**
- [ ] Calculate MTBF from field returns
- [ ] Compute confidence intervals (Chi-square)
- [ ] Trend failure rates over time

════════════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════════════════════════════════════════════════════════════

1️⃣ **MTBF = 1/λ for exponential** — Only valid for constant failure rate (useful life)

2️⃣ **Series reduces reliability** — R_system = R₁×R₂×R₃ always < min(R₁, R₂, R₃)

3️⃣ **Parallel improves reliability** — R_system = 1-(1-R)ⁿ → approaches 1 as n increases

4️⃣ **Weibull β tells the story** — β<1 infant, β=1 random, β>1 wear-out

5️⃣ **FIT is standard for ICs** — 1 FIT = 10⁹ hours = 114,000 years (!)

6️⃣ **Acceleration testing saves time** — 100× acceleration → 100 hours = 10,000 hours equivalent

7️⃣ **Field data beats predictions** — MIL-HDBK-217 conservative, actual MTBF often higher

════════════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **RELIABILITY ENGINEERING CHEATSHEET COMPLETE**

**Created:** January 15, 2026  
**Coverage:** MTBF/MTTF/FIT metrics, reliability distributions (exponential, Weibull, normal), RBD (series, parallel, k-out-of-n, standby), prediction methods (MIL-HDBK-217, IEC 62380, PoF), ALT (Arrhenius, HALT, HASS), field data analysis

════════════════════════════════════════════════════════════════════════════
