============================================================
ARINC 404A — ATR Equipment Form Factors
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 404A** defines standard mechanical packaging sizes for **Air Transport Rackable (ATR)** avionics equipment.

**Key Characteristics:**
- **Standard Sizes:** 1/4, 1/2, 3/4, 1, 1.5, 2, 3, 4 ATR (width multiples of 1.2")
- **Mounting:** Rail system with captive screws (1/4-turn or slide-lock)
- **Cooling:** Forced air (front-to-back), specified airflow rates
- **Connectors:** Rear-mounted (ARINC 600 series), EMI-shielded
- **Applications:** LRU packaging for commercial/military aircraft

**Common ATR Sizes:**

.. code-block:: text

   Size    Width    Height   Depth    Typical Use
   ──────  ───────  ───────  ───────  ───────────────────────────
   1/4 ATR 1.2"     7.88"    14.5"    Small modules (PSU, I/O)
   1/2 ATR 2.4"     7.88"    14.5"    Radio tuners, converters
   3/4 ATR 3.6"     7.88"    14.5"    Comm radios, TCAS
   1 ATR   4.8"     7.88"    14.5"    FMS, GPS, transponder
   2 ATR   9.625"   7.88"    14.5"    Flight control computer
   
   **Most Common:** 1/2 ATR (54% of avionics LRUs)

**Cooling Airflow:**
- Requirement: 10-30 CFM (cubic feet per minute) per ATR unit
- Direction: Front (connector side) → Back (exhaust)
- Temperature: 55°C max inlet, ΔT = 20°C rise

**ARINC 404A Benefits:**
- **Interchangeability:** Any 1 ATR fits in 1 ATR slot (multi-vendor)
- **Reduced Weight:** Standardized rails vs custom mounting brackets
- **Ease of Maintenance:** Slide-lock for quick removal (no tools)
- **Modularity:** Mix sizes (e.g., 2× 1/2 ATR = 1× 1 ATR space)

================================================================================
1. Overview & Background
================================================================================

**1.1 Why Standardized Form Factors?**
----------------------------------------

**Pre-ARINC 404 (1950s-1960s):**
- Each avionics vendor had proprietary mounting
- Custom brackets, cutouts, wiring harnesses
- Aircraft modification required for equipment changes
- Heavy (15-20 kg per LRU for mounting hardware)

**ARINC 404 Introduction (1966):**
- Defined 5 standard widths (1/4, 1/2, 3/4, 1, 1.5 ATR)
- Standard rail system (aircraft installs rails, LRU slides in)
- Weight savings: 40% reduction in mounting hardware
- First adoption: Boeing 747 (1970)

**ARINC 404A Revision (1995):**
- Added 2, 3, 4 ATR sizes (larger FMS, flight control computers)
- Improved EMI shielding requirements
- Updated cooling specifications (higher TDP for modern avionics)
- Incorporated DO-160 environmental testing

**1.2 Market Adoption**
------------------------

**Commercial Aircraft:**
- Boeing 737 MAX: 28× ATR slots per aircraft
- Airbus A320neo: 32× ATR slots
- Boeing 787: 45× ATR slots (more systems, more LRUs)

**Military Aircraft:**
- F-16: Mission computers, EW pods
- C-130J: Avionics upgrade (legacy round-dial → glass cockpit)
- AH-64 Apache: Fire control, communication, navigation

**Avionics Vendors:**
- Honeywell, Collins Aerospace, Thales, Garmin all produce ATR-compliant LRUs

================================================================================
2. ATR Sizes & Dimensions
================================================================================

**2.1 Standard ATR Sizes**
---------------------------

**Dimensional Standards (ARINC 404A Table 2-1):**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────────┐
   │                   ATR SIZE SPECIFICATIONS                     │
   ├──────┬──────────┬──────────┬──────────┬─────────────────────┤
   │ Size │ Width    │ Height   │ Depth    │ Volume              │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 1/4  │ 1.2"     │ 7.875"   │ 14.5"    │ 137 in³             │
   │      │ (30.5mm) │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 1/2  │ 2.4"     │ 7.875"   │ 14.5"    │ 274 in³             │
   │      │ (61mm)   │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 3/4  │ 3.6"     │ 7.875"   │ 14.5"    │ 411 in³             │
   │      │ (91.5mm) │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 1    │ 4.8"     │ 7.875"   │ 14.5"    │ 548 in³             │
   │      │ (122mm)  │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 1.5  │ 7.2"     │ 7.875"   │ 14.5"    │ 822 in³             │
   │      │ (183mm)  │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 2    │ 9.625"   │ 7.875"   │ 14.5"    │ 1,099 in³           │
   │      │ (244mm)  │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 3    │ 14.425"  │ 7.875"   │ 14.5"    │ 1,648 in³           │
   │      │ (366mm)  │ (200mm)  │ (368mm)  │                     │
   ├──────┼──────────┼──────────┼──────────┼─────────────────────┤
   │ 4    │ 19.25"   │ 7.875"   │ 14.5"    │ 2,198 in³           │
   │      │ (489mm)  │ (200mm)  │ (368mm)  │                     │
   └──────┴──────────┴──────────┴──────────┴─────────────────────┘
   
   **Width Increment:** 1.2" per 1/4 ATR (30.5 mm)
   **Height:** Fixed 7.875" (includes 0.125" clearance for rails)
   **Depth:** 14.5" max (some LRUs shorter, e.g., 10" for low-profile)

**Visual Comparison:**

.. code-block:: text

   Front View (looking into rack):
   
   ┌──┐  ┌────┐  ┌──────┐  ┌────────┐  ┌────────────┐
   │  │  │    │  │      │  │        │  │            │
   │1/4 │1/2 │  │  3/4 │  │   1    │  │     1.5    │
   │  │  │    │  │      │  │        │  │            │
   └──┘  └────┘  └──────┘  └────────┘  └────────────┘
   1.2"   2.4"     3.6"      4.8"         7.2"

**2.2 Modular Combinations**
-----------------------------

**Space Allocation:**
Aircraft racks can accommodate different combinations:

.. code-block:: text

   Example: 4.8" wide slot can hold:
   - 1× 1 ATR unit
   - 2× 1/2 ATR units (side-by-side)
   - 4× 1/4 ATR units
   - 1× 3/4 ATR + 1× 1/4 ATR
   
   Boeing 737 Avionics Bay:
   ┌──────────────────────────────────────┐
   │  Rack 1 (Left Side)                  │
   ├────────────┬────────────┬────────────┤
   │  2 ATR     │  1 ATR     │  1 ATR     │  Slot 1-3
   │  FMS       │  TCAS      │  Transponder│
   ├──────┬─────┼──────┬─────┼──────┬─────┤
   │ 1/2  │ 1/2 │ 3/4  │ 1/4 │ 1/2  │ 1/2 │  Slot 4-6
   │ Radio│ VHF │ DME  │ ADF │ Marker│ GPS │
   └──────┴─────┴──────┴─────┴──────┴─────┘

================================================================================
3. Mounting System
================================================================================

**3.1 Rail System**
--------------------

**Aircraft-Side Rails:**

.. code-block:: text

   Side View (cross-section of rack):
   
   ┌───────────────────────────────────────┐
   │        Aircraft Rack Structure         │
   ├───┐                               ┌───┤
   │   │←── Upper Rail (0.125" track) ─│   │
   │   │                               │   │
   │   │          Empty Space          │   │
   │   │        (for LRU insertion)    │   │
   │   │                               │   │
   │   │←── Lower Rail (0.125" track) ─│   │
   └───┘                               └───┘
   
   Rails are T-shaped extrusions:
   - Material: Aluminum alloy (6061-T6)
   - Finish: Anodized (corrosion protection)
   - Tolerance: ±0.005" (tight for smooth sliding)

**LRU-Side Guide Rails:**

.. code-block:: text

   LRU has matching guide rails on sides:
   
   Top View (LRU cross-section):
   
   ┌─────────────────────────────────────┐
   │                                     │
   │           LRU Chassis               │
   │                                     │
   ├──┐                               ┌──┤
   │  │← Guide rail (slides into rack)│  │
   └──┘                               └──┘
   
   - Stainless steel (wear resistance)
   - Teflon coating (low friction)
   - Curved front edge (guide into rack slot)

**3.2 Retention Mechanisms**
------------------------------

**1/4-Turn Captive Screws (Most Common):**

.. code-block:: text

   Front Panel (LRU):
   
   ┌─────────────────────────────────────┐
   │  ┌───┐                       ┌───┐  │
   │  │ ○ │  LRU Front Panel      │ ○ │  │ ← Captive screws
   │  └───┘                       └───┘  │    (1/4-turn lock)
   │                                     │
   │       [Equipment Label]             │
   │                                     │
   └─────────────────────────────────────┘
   
   Installation:
   1. Slide LRU into rails (push until seated)
   2. Rotate captive screws 90° (clockwise)
   3. Screws engage threads in rack front panel
   4. LRU locked in place (cannot slide out)

**Slide-Lock Mechanism (Quick Release):**
- Used for frequently-removed LRUs (e.g., FMS database updates)
- Lever on front panel
- Push lever → releases lock → LRU slides out
- No tools required

**3.3 Connector Engagement**
------------------------------

**Rear Connector Mating:**

.. code-block:: text

   Side View (LRU insertion):
   
   Step 1: Insert LRU into rails
   ┌────────────┐
   │    LRU     │──────────►
   └────────────┘
         Rails guide LRU into position
   
   Step 2: Push LRU to mate connector
   ┌────────────┐            ┌─Rack Connector
   │    LRU     │───────────►│ (fixed to aircraft)
   └────┬───────┘            └─┘
        │
        Connector on LRU rear
   
   Step 3: Lock captive screws
   ┌────────────┐
   │    LRU     │ [LOCKED]
   └────────────┘

**Insertion Force:**
- Typical: 20-40 lbf (89-178 N)
- Connector: ARINC 600 series (multiple pins: 50-200)
- Extraction force: 30-50 lbf (with slide-lock released)

================================================================================
4. Cooling & Thermal Management
================================================================================

**4.1 Forced Air Cooling**
---------------------------

**Airflow Direction:**

.. code-block:: text

   Top View (LRU airflow):
   
   Front (Connector Side)       Back (Exhaust)
   ─────────────────────►────────────────────
        Cool Air                  Hot Air
        (55°C max)               (75°C max)
   
   ┌───────────────────────────────────────┐
   │  ┌──────┐  ┌──────┐  ┌──────┐         │
   │  │ PCB  │  │ PCB  │  │ PCB  │         │
   │  └──────┘  └──────┘  └──────┘         │
   │                                        │
   │  Heat dissipated to airflow            │
   └───────────────────────────────────────┘
   
   - Inlet vents: Front panel (honeycomb pattern)
   - Exhaust vents: Rear panel
   - Airflow path: Straight through (no baffles)

**Airflow Requirements (ARINC 404A Table 4-1):**

.. code-block:: text

   ATR Size   Min Airflow   Max TDP (Thermal Design Power)
   ─────────  ────────────  ────────────────────────────────
   1/4 ATR    5 CFM         25 W
   1/2 ATR    10 CFM        50 W
   3/4 ATR    15 CFM        75 W
   1 ATR      20 CFM        100 W
   1.5 ATR    30 CFM        150 W
   2 ATR      40 CFM        200 W
   
   CFM = Cubic Feet per Minute
   TDP assumes ΔT = 20°C (inlet to exhaust)

**Aircraft Cooling System:**
- **Blowers:** Centrifugal fans (28 VDC, 5-10 A per fan)
- **Ductwork:** Distributes air to each rack slot
- **Filters:** HEPA (High-Efficiency Particulate Air) to prevent dust
- **Temperature sensors:** Monitor exhaust temp (>80°C = overheat alarm)

**4.2 Heat Sink Design**
-------------------------

**Component Thermal Management:**

.. code-block:: text

   Cross-Section (PCB with power components):
   
                Airflow →
   ┌─────────────────────────────────────┐
   │  ┌────┐    ┌────┐    ┌────┐         │
   │  │HS1 │    │HS2 │    │HS3 │         │ ← Heat sinks
   │  └─┬──┘    └─┬──┘    └─┬──┘         │
   │    │         │         │             │
   │  ┌─┴───┐  ┌─┴───┐  ┌─┴───┐          │
   │  │FPGA │  │ PSU │  │ CPU │          │ ← Components
   │  └─────┘  └─────┘  └─────┘          │
   ├─────────────────────────────────────┤
   │             PCB                      │
   └─────────────────────────────────────┘
   
   Heat Sink Guidelines:
   - Orientation: Fins parallel to airflow (minimize resistance)
   - Material: Aluminum 6063 (thermal conductivity 200 W/m·K)
   - Fin spacing: 3-5 mm (balance surface area vs airflow)
   - Thermal interface: Thermal pad or paste (0.5 W/m·K)

**Thermal Resistance Calculation:**

.. code-block:: python

   def calculate_junction_temp(P_diss, R_ja, T_amb):
       """
       Calculate component junction temperature.
       
       P_diss: Power dissipation (W)
       R_ja: Junction-to-ambient thermal resistance (°C/W)
       T_amb: Ambient temperature (°C)
       
       Returns: Junction temperature (°C)
       """
       T_j = T_amb + (P_diss * R_ja)
       return T_j
   
   # Example: FPGA in 1 ATR LRU
   P_fpga = 15  # Watts
   R_ja = 2.5   # °C/W (with heat sink + airflow)
   T_inlet = 55 # °C (max inlet air temp)
   
   T_junction = calculate_junction_temp(P_fpga, R_ja, T_inlet)
   print(f"FPGA junction temp: {T_junction}°C")
   
   # Output: 92.5°C (within FPGA max 125°C spec)

================================================================================
5. EMI/EMC Shielding
================================================================================

**5.1 Conductive Enclosure**
------------------------------

**Shielding Requirements (DO-160G Section 21):**

.. code-block:: text

   Material: Aluminum alloy chassis (natural shielding)
   Thickness: 0.063" minimum (1.6 mm)
   Finish: Chromate conversion coating (MIL-DTL-5541, conductive)
   
   Gaps/Seams:
   - All seams <0.1" gap (λ/10 rule @ 300 MHz)
   - Gaskets at removable panels (beryllium-copper fingers)
   - Vent holes <0.125" diameter (honeycomb pattern)

**Front Panel EMI Gasket:**

.. code-block:: text

   Cross-Section (front panel to rack):
   
   ┌─────────────────┐
   │   LRU Panel     │
   └────┬────────────┘
        │  ╔════════╗  ← EMI gasket (0.125" thick)
        └──╢ Rack   ║
           ╚════════╝
   
   Gasket Types:
   - Beryllium-copper fingers (most common)
   - Conductive elastomer (silicone + silver particles)
   - Wire mesh (stainless steel)
   
   Purpose: Prevent RF leakage at panel interface

**5.2 Connector Backshell Grounding**
---------------------------------------

**ARINC 600 Connector Grounding:**

.. code-block:: text

   Rear View (connector on LRU):
   
   ┌─────────────────────────────────────┐
   │         LRU Chassis (ground)         │
   └────────────────┬────────────────────┘
                    │
              ┌─────┴─────┐
              │ Connector │
              │ Backshell │ ← 360° shield termination
              └─────┬─────┘
                    │
              ┌─────┴─────┐
              │  Cable    │
              │  Shield   │
              └───────────┘
   
   Grounding Points:
   - Connector backshell bonded to chassis (4× screws)
   - Cable shield terminated to backshell (360° crimp)
   - Rack connector bonded to aircraft structure

**Bonding Resistance:**
- Requirement: <2.5 mΩ (DC resistance, chassis to rack)
- Test: 100 A DC current, measure voltage drop
- Ensures lightning protection (low-impedance ground path)

================================================================================
6. Mechanical Specifications
================================================================================

**6.1 Material & Construction**
--------------------------------

**Chassis Materials:**

.. code-block:: text

   Component          Material              Reason
   ─────────────────  ────────────────────  ─────────────────────────
   Chassis            Al 6061-T6            Lightweight, machinable
   Front panel        Al 5052-H32           Corrosion-resistant
   Rails (guide)      Stainless 304         Wear-resistant
   Captive screws     Stainless 316         Corrosion-resistant
   PCB standoffs      Brass (nickel-plated) Conductive, vibration
   
   Weight Budget (1 ATR):
   - Chassis: 1.2 kg
   - PCBs: 0.5 kg
   - Components: 1.0 kg
   - Connectors: 0.3 kg
   ─────────────────
   Total: ~3 kg (vs 5 kg for non-standard packaging)

**6.2 Vibration & Shock Requirements**
----------------------------------------

**DO-160G Section 8 (Vibration):**

.. code-block:: text

   Operational Vibration (Category D):
   
   Frequency (Hz)   Acceleration (G)   Duration
   ───────────────  ─────────────────  ────────
   5-18.8           0.008 in DA        15 min per axis
   18.8-50          1.04 G             15 min per axis
   50-500           Random (0.04 G²/Hz) 15 min per axis
   
   Axes: X, Y, Z (3 axes)
   Total test time: 45 min operational + 45 min powered-off
   
   Critical Resonances:
   - PCB: 100-300 Hz (avoid by stiffening)
   - Connector pins: 400-600 Hz (use proper retention)

**Crash Safety (DO-160G Section 8.6):**

.. code-block:: text

   Crash Pulse: 6 G triangle wave (20 ms duration)
   
   Acceleration →
   
     6G ┌──┐
        │  │
        │  │
        │  │
     0  └──┘────────
        0  20 ms
   
   LRU must remain mounted (no separation from rack)
   Captive screws must hold 10× operating load

================================================================================
7. Common ATR Avionics Examples
================================================================================

**7.1 Flight Management System (FMS)**
----------------------------------------

**Honeywell Pegasus FMS:**
- **Size:** 2 ATR (9.625" wide)
- **Weight:** 8.5 kg
- **Power:** 28 VDC, 3.5 A (98 W)
- **Cooling:** 35 CFM forced air
- **Connectors:** 2× ARINC 600 (78-pin + 156-pin)
- **Features:**
  - Dual GPS/IRS integration
  - RNAV/RNP flight planning
  - Database: ARINC 424 navigation data

**FMS Internal Layout (2 ATR):**

.. code-block:: text

   Top View:
   
   ┌─────────────────────────────────────────┐
   │ ┌─────┐  ┌─────────┐  ┌──────┐  ┌────┐ │
   │ │ PSU │  │  CPU    │  │ I/O  │  │Fan │ │
   │ │     │  │ (SBC)   │  │ FPGA │  │    │ │
   │ └─────┘  └─────────┘  └──────┘  └────┘ │
   │                                         │
   │ ┌───────────────────────────────────┐   │
   │ │       Memory (128 GB SSD)         │   │
   │ └───────────────────────────────────┘   │
   └─────────────────────────────────────────┘
           ▲
           Airflow

**7.2 Transponder (1 ATR)**
----------------------------

**Garmin GTX 345 ADS-B Transponder:**
- **Size:** 1 ATR (4.8" wide)
- **Weight:** 1.8 kg
- **Power:** 28 VDC, 1.5 A (42 W)
- **Cooling:** 18 CFM
- **Features:**
  - Mode S Extended Squitter (1090 MHz)
  - ADS-B Out (position broadcast)
  - ADS-B In (traffic reception)
  - UAT support (978 MHz)

**7.3 VHF Communication Radio (1/2 ATR)**
------------------------------------------

**Collins Aerospace VHF-422D:**
- **Size:** 1/2 ATR (2.4" wide)
- **Frequency:** 118-137 MHz (AM, 25 kHz / 8.33 kHz spacing)
- **Power:** 10 W RF output
- **Cooling:** 10 CFM
- **Weight:** 1.2 kg

================================================================================
8. Installation & Maintenance
================================================================================

**8.1 Installation Procedure**
-------------------------------

**Step-by-Step LRU Installation:**

.. code-block:: text

   Pre-Installation:
   □ Verify LRU part number matches installation drawing
   □ Inspect LRU for damage (cracks, bent pins)
   □ Check connector pins (none bent, debris-free)
   □ Verify aircraft power OFF (circuit breaker open)
   
   Installation:
   □ Align LRU with rack rails
   □ Slide LRU into rack (firm, steady push)
   □ Ensure connector fully seated (audible click or mark)
   □ Rotate captive screws 90° clockwise (1/4-turn)
   □ Verify front panel flush with rack
   
   Post-Installation:
   □ Connect any required external cables (if applicable)
   □ Close aircraft circuit breaker (apply power)
   □ Perform Built-In Test (BIT)
   □ Verify operational (check displays, indicators)
   □ Update aircraft logbook (part number, serial number, date)

**8.2 Removal Procedure**
---------------------------

.. code-block:: text

   Pre-Removal:
   □ Open circuit breaker (remove power)
   □ Disconnect external cables (if any)
   
   Removal:
   □ Rotate captive screws 90° counter-clockwise
   □ Pull LRU straight out (firm, steady pull)
   □ Support LRU weight (do not drop)
   
   Post-Removal:
   □ Inspect rack connector (bent pins, corrosion)
   □ Install blank panel if slot empty (EMI shielding)
   □ Label removed LRU with reason (fault code, replacement)

**8.3 Common Issues**
----------------------

**Problem: LRU won't slide into rack**

.. code-block:: text

   Possible Causes:
   - Bent guide rails on LRU
   - Obstructed rack rails (debris, corrosion)
   - Wrong ATR size (1 ATR in 3/4 ATR slot)
   
   Troubleshooting:
   1. Inspect LRU rails (straighten if bent)
   2. Clean rack rails (solvent, wire brush)
   3. Verify LRU size matches rack slot

**Problem: Connector won't mate**

.. code-block:: text

   Possible Causes:
   - Bent pins on LRU or rack connector
   - Foreign object in connector (FOD)
   - Misalignment (LRU not centered in rails)
   
   Troubleshooting:
   1. Remove LRU, inspect connector with flashlight
   2. Use pin-straightening tool (DO NOT force)
   3. Re-insert LRU, ensure centered in rails

**Problem: Overheating**

.. code-block:: text

   Possible Causes:
   - Insufficient airflow (fan failure, clogged filter)
   - Excessive TDP (over-spec components)
   - Blocked vents (dust, tape)
   
   Troubleshooting:
   1. Check blower operation (28 VDC at fan connector)
   2. Inspect/replace HEPA filters (every 500 flight hours)
   3. Verify exhaust vents clear

================================================================================
9. Exam Preparation — 5 Questions
================================================================================

**Question 1: Size Calculations (10 points)**

An avionics rack has 14.4" width available.

a) What ATR combinations fit? (list 3 different) (6 pts)
b) Which combination maximizes space utilization? (2 pts)
c) If each slot requires 0.1" clearance, recalculate. (2 pts)

**Answer:**

a) **ATR Combinations for 14.4" width:**

.. code-block:: text

   Option 1: 3× 1 ATR (3 × 4.8" = 14.4") ✓
   Option 2: 6× 1/2 ATR (6 × 2.4" = 14.4") ✓
   Option 3: 2× 1.5 ATR (2 × 7.2" = 14.4") ✓
   Option 4: 1× 2 ATR + 1× 1 ATR (9.625" + 4.8" = 14.425") ✗ (too wide)
   Option 5: 1× 3 ATR (14.425") ✗ (too wide)
   Option 6: 4× 3/4 ATR (4 × 3.6" = 14.4") ✓
   
   Valid: Options 1, 2, 3, 6

b) **Maximum Utilization:**
   - **Option 2 (6× 1/2 ATR) or Option 6 (4× 3/4 ATR)**
   - Both use exactly 14.4" (100% utilization)
   - More smaller units = more flexibility (modularity)

c) **With 0.1" Clearance per Slot:**

.. code-block:: text

   Usable width per ATR:
   - 1 ATR = 4.8" - 0.1" = 4.7"
   - 1/2 ATR = 2.4" - 0.1" = 2.3"
   - 3/4 ATR = 3.6" - 0.1" = 3.5"
   - 1.5 ATR = 7.2" - 0.1" = 7.1"
   
   Revised combinations:
   - Option 1: 3× 1 ATR = 3 × 4.7" = 14.1" (0.3" unused) ✓
   - Option 2: 6× 1/2 ATR = 6 × 2.3" = 13.8" (0.6" unused) ✓
   - Option 3: 2× 1.5 ATR = 2 × 7.1" = 14.2" (0.2" unused) ✓

---

**Question 2: Thermal Design (12 points)**

Design cooling for 1 ATR FMS:
- CPU: 15 W
- FPGA: 12 W
- PSU: 8 W (losses)
- Other: 5 W

a) Calculate total TDP (2 pts)
b) Determine required airflow (assume ΔT=20°C) (6 pts)
c) Select blower (given options) (4 pts)

**Answer:**

a) **Total TDP:**
   - TDP = 15 + 12 + 8 + 5 = **40 W**

b) **Required Airflow:**

.. code-block:: text

   Heat equation: Q = ṁ × Cp × ΔT
   
   Where:
   - Q = Heat (40 W = 40 J/s)
   - ṁ = Mass flow rate (kg/s)
   - Cp = Specific heat of air = 1005 J/(kg·K)
   - ΔT = Temperature rise = 20°C = 20 K
   
   ṁ = Q / (Cp × ΔT) = 40 / (1005 × 20) = 0.00199 kg/s
   
   Convert to CFM (Cubic Feet per Minute):
   - Air density @ 55°C = 1.05 kg/m³
   - Volume flow = ṁ / ρ = 0.00199 / 1.05 = 0.00190 m³/s
   - CFM = 0.00190 × 2118.88 (m³/s → CFM) = 4.0 CFM
   
   **Safety factor:** 2× (account for non-uniform flow, aging)
   **Required airflow:** 4.0 × 2 = **8 CFM**

c) **Blower Selection:**

.. code-block:: text

   Available Blowers:
   A) 5 CFM @ 0.5" H2O (insufficient) ✗
   B) 10 CFM @ 0.3" H2O (adequate) ✓
   C) 20 CFM @ 0.8" H2O (overkill, higher power) ✗
   
   **Select B (10 CFM blower)**
   - Provides 25% margin over required 8 CFM
   - Lower static pressure (0.3") saves power

---

**Question 3: EMI Shielding (10 points)**

a) Calculate maximum gap size for 1 GHz shielding (λ/10 rule) (4 pts)
b) Why use beryllium-copper EMI gaskets? (3 pts)
c) What bonding resistance required? (3 pts)

**Answer:**

a) **Maximum Gap Size (λ/10 Rule):**

.. code-block:: text

   Wavelength: λ = c / f
   
   Where:
   - c = Speed of light = 3 × 10⁸ m/s
   - f = Frequency = 1 GHz = 1 × 10⁹ Hz
   
   λ = 3 × 10⁸ / 1 × 10⁹ = 0.3 m = 300 mm
   
   Maximum gap: λ / 10 = 300 mm / 10 = 30 mm
   
   **Practical limit:** Much smaller (1-2 mm) for better shielding
   - 30 mm allows significant RF leakage
   - DO-160G typically requires <3 mm gaps

b) **Beryllium-Copper Gaskets:**
   - **High conductivity:** Excellent RF shielding (σ = 2 × 10⁷ S/m)
   - **Spring force:** Maintains contact under vibration
   - **Corrosion-resistant:** Beryllium oxide layer protects
   - **Ductile:** Conforms to uneven surfaces (panel tolerances)

c) **Bonding Resistance:**
   - **Requirement:** <2.5 mΩ (DO-160G Section 16)
   - **Measurement:** 100 A DC, measure voltage drop (V = I × R)
   - **Purpose:**
     - Lightning protection (low-impedance ground path)
     - EMI shielding (equipotential bonding)
     - Prevents voltage differentials (electrostatic discharge)

---

**Question 4: Vibration Analysis (8 points)**

1 ATR LRU has PCB resonance at 180 Hz. DO-160G Category D vibration:
- 50-500 Hz: 0.04 G²/Hz random PSD

a) What is RMS acceleration at 180 Hz? (4 pts)
b) Is this acceptable? (2 pts)
c) How to mitigate? (2 pts)

**Answer:**

a) **RMS Acceleration:**

.. code-block:: text

   Power Spectral Density (PSD): 0.04 G²/Hz
   
   For random vibration:
   G_rms = √(PSD × Δf)
   
   Where:
   - Δf = Bandwidth around resonance (assume 10 Hz)
   
   G_rms = √(0.04 × 10) = √0.4 = 0.63 G
   
   At resonance, amplification factor Q ≈ 10 (typical PCB)
   
   Peak acceleration: 0.63 G × 10 = **6.3 G at 180 Hz**

b) **Acceptability:**
   - **NOT acceptable** for fragile components (connectors, solder joints)
   - 6.3 G can cause:
     - Solder joint fatigue (over time)
     - Connector fretting (intermittent contact)
     - Component lead failures

c) **Mitigation Strategies:**
   - **Increase PCB stiffness:** Thicker PCB (0.093" vs 0.062"), edge stiffeners
   - **Damping:** Viscoelastic damping material on PCB underside
   - **Standoff spacing:** Reduce span between mounting points (shift resonance >300 Hz)
   - **Component placement:** Keep heavy components (connectors, transformers) near standoffs

---

**Question 5: Installation Scenario (10 points)**

During 1 ATR FMS installation, connector mates but LRU front panel doesn't sit flush (0.25" gap). Captive screws won't engage.

a) What are 3 possible causes? (6 pts)
b) What is the correct troubleshooting sequence? (4 pts)

**Answer:**

a) **Possible Causes:**

1. **Connector Backshell Interference:**
   - Cable bundle behind rack connector blocking full insertion
   - Connector shell bottoming on rack (not fully seated)
   
2. **Foreign Object Debris (FOD):**
   - Washer, wire, or debris in rail tracks
   - Prevents LRU from sliding all the way forward
   
3. **Bent/Damaged Rails:**
   - LRU guide rails bent outward (won't fit in track)
   - Rack rails damaged (obstruction)

b) **Troubleshooting Sequence:**

.. code-block:: text

   Step 1: Remove LRU (do not force)
   - Pull straight out (avoid twisting)
   
   Step 2: Visual Inspection
   - Inspect LRU rails (bent, damaged?)
   - Inspect rack rails (debris, corrosion?)
   - Check connector backshell clearance
   
   Step 3: Verify Empty Rack
   - Slide dummy LRU (or ruler) into rails
   - Confirm rails clear, no obstructions
   
   Step 4: Check Connector Depth
   - Measure rack connector protrusion (should be <1")
   - Verify LRU connector receptacle depth matches
   
   Step 5: Reinstall with Observation
   - Slide LRU slowly, watch for binding point
   - Identify where interference occurs
   
   Step 6: Correct Issue
   - Remove debris, straighten rails, reroute cables
   - Retest until flush fit achieved

================================================================================
10. Completion Checklist
================================================================================

□ Know standard ATR sizes (1/4, 1/2, 3/4, 1, 1.5, 2, 3, 4 ATR)
□ Understand rail mounting system (captive screws, slide-locks)
□ Calculate airflow requirements (CFM for given TDP)
□ Design heat sinks (thermal resistance, fin spacing)
□ Apply EMI shielding (gaskets, bonding resistance)
□ Analyze vibration (resonance, PSD, G_rms)
□ Perform installation/removal procedures
□ Troubleshoot common issues (won't insert, overheat)
□ Select materials (Al 6061, stainless 304, beryllium-copper)
□ Understand DO-160G environmental testing

================================================================================
11. Key Takeaways
================================================================================

1. **ATR = Standardized Packaging:** 1.2" width increments, 7.875" height, 14.5" depth

2. **Rail System:** T-shaped rails, LRU slides in, 1/4-turn captive screws lock

3. **Cooling:** Forced air, front-to-back, 20 CFM per 1 ATR (100 W TDP)

4. **EMI Shielding:** Conductive chassis, beryllium-copper gaskets, <2.5 mΩ bonding

5. **Most Common:** 1/2 ATR (54% of avionics), modular (2× 1/2 = 1× 1 ATR)

6. **Weight Savings:** 40% reduction vs custom mounting (standardized rails)

7. **DO-160G Compliance:** Vibration Category D, crash 6G, temperature -55 to +85°C

8. **Connector Engagement:** ARINC 600 rear connector, 20-40 lbf insertion force

9. **Modular Combinations:** Mix sizes in rack slots (flexibility)

10. **Quick Removal:** Slide-lock for frequently-accessed LRUs (no tools)

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 404A — ATR Equipment Form Factors
- ARINC 600 — Air Transport Connector System
- RTCA DO-160G — Environmental Conditions and Test Procedures
- MIL-DTL-5541 — Chromate Conversion Coating
- MIL-DTL-38999 — Connectors (EMI shielded)

**Avionics Equipment:**
- Honeywell Pegasus FMS
- Collins Aerospace VHF-422D Radio
- Garmin GTX 345 Transponder

**Aircraft Installation Manuals:**
- Boeing 737 AMM (Aircraft Maintenance Manual) Chapter 34 (Navigation)
- Airbus A320 AMM Chapter 31 (Indicating/Recording Systems)

**Thermal Management:**
- "Thermal Management of Electronics" by Avram Bar-Cohen
- MIL-HDBK-217 (Reliability Prediction)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** ARINC 404A, ARINC 600, DO-160G

================================================================================
