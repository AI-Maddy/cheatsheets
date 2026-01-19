============================================================
ARINC 717 — Flight Data Acquisition & Recording Interface
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 717** defines the high-speed digital interface for flight data acquisition and recording systems, replacing older ARINC 573 standard.

**Key Characteristics:**
- **Purpose:** Transfer flight data from aircraft systems to Flight Data Recorder (FDR) and Quick Access Recorder (QAR)
- **Encoding:** Harvard Bi-Phase (self-clocking, no separate clock line needed)
- **Speed Options:** 64, 128, 256, 512, 1024, 2048, 4096 words/second
- **Word Size:** 12-bit words organized in frames and subframes
- **Applications:** Cockpit Voice Recorder (CVR), Flight Data Recorder (FDR), Aircraft Condition Monitoring System (ACMS)
- **Certification:** Required for FAR Part 121/135, EASA CS-25 commercial aircraft

**Typical Setup:**
- Flight Data Acquisition Unit (FDAU) collects data from ARINC 429, discrete inputs, analog sensors
- FDAU formats data per ARINC 717
- Transmits to FDR (crash-protected) and QAR (quick analysis)

================================================================================
1. Overview & Regulatory Background
================================================================================

**1.1 Flight Data Recording Requirements**
--------------------------------------------

**Regulatory Mandate:**
- **FAA FAR 121.343/344:** Requires FDR on commercial aircraft (>12,500 lbs)
- **EASA CS-25.1459:** European equivalent requirements
- **ICAO Annex 6:** International standards for flight recorders
- **Minimum Parameters:** 88+ parameters for modern aircraft (altitude, airspeed, heading, control positions, engine data, etc.)

**Recording Duration:**
- **FDR:** Minimum 25 hours (many modern systems: 50+ hours)
- **CVR:** Minimum 2 hours (as of 2021: 25 hours for new aircraft)

**Crash Survival:**
- FDR must survive 3,400 G impact, 1,100°C fire for 1 hour, 20,000 ft seawater submersion
- Underwater Locator Beacon (ULB): 30-day battery, 37.5 kHz pinger

**1.2 ARINC 717 vs ARINC 573**
--------------------------------

**ARINC 573 (Legacy):**
- Older analog/digital hybrid format
- Lower data rates
- Less standardized frame structure
- Still found on 1980s-1990s aircraft

**ARINC 717 (Modern):**
- Fully digital Harvard Bi-Phase encoding
- Higher data rates (up to 4096 wps)
- Standardized 12-bit word, 64/128/256/512/1024 word frames
- Improved error detection
- Easier integration with digital FDAU
- Used on Boeing 737NG/MAX, 777, 787, Airbus A320neo, A350, A380

================================================================================
2. Harvard Bi-Phase Encoding
================================================================================

**2.1 Encoding Principles**
-----------------------------

Harvard Bi-Phase is a **self-clocking** encoding scheme:
- Each bit period has a **mandatory transition** in the middle
- Data encoded by presence/absence of transition at bit boundary
- Receiver extracts clock from data stream (no separate clock wire needed)

**Encoding Rules:**
- **Logic 1:** Transition at bit start + transition at bit middle
- **Logic 0:** No transition at bit start + transition at bit middle (mandatory)

**Waveform Example:**

.. code-block:: text

   Data:     1    0    1    1    0    0    1
           ┌────┐    ┌────┬────┬────┐    ┌────┐
   Signal: │    │    │    │    │    │    │    │
   ────────┘    └────┘    └────┘    └────┘    └────
           ↑mid ↑mid ↑mid ↑mid ↑mid ↑mid ↑mid
           ↑start    ↑start ↑start       ↑start
           
   Key:
   - ↑ at middle of bit: Mandatory (provides clock)
   - ↑ at start of bit: Indicates logic 1
   - No ↑ at start: Indicates logic 0

**Advantages:**
- **No separate clock line:** Simplifies wiring, reduces EMI
- **Self-synchronizing:** Receiver locks to data stream automatically
- **DC balanced:** Equal positive/negative voltage (no DC offset)
- **Error detection:** Missing transitions indicate corruption

**Bit Rates (depending on word rate):**

.. code-block:: text

   Word Rate    Bits/Word    Bit Rate
   ──────────   ─────────    ────────
   64 wps       12 bits      768 bps
   128 wps      12 bits      1,536 bps
   256 wps      12 bits      3,072 bps
   512 wps      12 bits      6,144 bps
   1024 wps     12 bits      12,288 bps
   2048 wps     12 bits      24,576 bps
   4096 wps     12 bits      49,152 bps

**2.2 Signal Characteristics**
--------------------------------

**Voltage Levels:**
- Differential signaling (similar to ARINC 429)
- **High:** +10V nominal (±1V tolerance)
- **Low:** -10V nominal (±1V tolerance)
- **Null (no data):** 0V ± 0.5V

**Connector:**
- Typically BNC coaxial or twisted-pair shielded cable
- 75-ohm impedance matching
- Maximum cable length: ~300 feet (depends on data rate)

================================================================================
3. Frame Structure
================================================================================

**3.1 12-Bit Word Format**
----------------------------

Each word is **12 bits:**

.. code-block:: text

   Bit Position:  1  2  3  4  5  6  7  8  9  10 11 12
                 ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
   Word:         │            Data (11 bits)          │P│
                 └────────────────────────────────────┴──┘
   
   - Bits 1-11: Parameter data (MSB first)
   - Bit 12: Parity bit (odd parity)

**Parity:**
- **Odd parity:** Count of 1s in word (including parity bit) must be odd
- Example: 101010101010 → 6 ones → add parity=1 → 1010101010101 (7 ones, odd ✓)

**3.2 Frame Organization**
----------------------------

Data organized hierarchically:

.. code-block:: text

   Superframe (4 frames)
   ├── Frame 1 (64/128/256/512/1024 words)
   │   ├── Subframe 1 (4/8/16/32/64 words)
   │   ├── Subframe 2
   │   ├── Subframe 3
   │   └── Subframe 4
   ├── Frame 2
   ├── Frame 3
   └── Frame 4

**Typical Configuration (256 wps, 64-word frames):**

.. code-block:: text

   Frame = 64 words
   Subframe = 16 words
   
   Word 1: Sync word (frame synchronization)
   Words 2-64: Parameter data
   
   Frame repeats 256 times/second → 4 ms per frame
   Superframe = 4 frames = 16 ms

**3.3 Synchronization Word**
------------------------------

First word of each frame is a **sync word** for frame alignment:

.. code-block:: text

   Sync Word (12 bits): 101010110100
   
   Purpose:
   - Receiver searches for this pattern to align frame boundaries
   - Different sync patterns for Frame 1, 2, 3, 4 (superframe sync)
   - Allows recovery from data corruption or startup

**Sync Word Patterns:**

.. code-block:: text

   Frame 1 Sync: 0xAD4 (101010110100)
   Frame 2 Sync: 0x5B2 (010110110010)
   Frame 3 Sync: 0x2D9 (001011011001)
   Frame 4 Sync: 0x96C (100101101100)

================================================================================
4. Parameter Encoding
================================================================================

**4.1 Parameter Mapping**
---------------------------

Each flight parameter assigned to specific word(s) in frame:

**Example Parameter Map (simplified):**

.. code-block:: text

   Word  Parameter                 Units        Resolution   Range
   ────  ────────────────────────  ───────────  ───────────  ─────────────
   1     Sync Word                 -            -            -
   2     Pressure Altitude         feet         4 ft         -1,000 to 50,000
   3     Calibrated Airspeed       knots        1 kt         0 to 500
   4     Heading (Magnetic)        degrees      0.18°        0 to 360
   5     Pitch Angle               degrees      0.18°        -90 to +90
   6     Roll Angle                degrees      0.18°        -180 to +180
   7     Vertical Acceleration     g            0.01g        -3 to +6
   8     Engine 1 N1               %            0.1%         0 to 120
   9     Engine 1 EGT              °C           1°C          0 to 1200
   ...
   64    Last parameter

**Multi-Word Parameters:**
Large parameters (e.g., latitude/longitude, date/time) span multiple words:

.. code-block:: text

   Latitude:
   - Word 10: Degrees + Hemisphere (N/S)
   - Word 11: Minutes + fractional minutes
   
   Longitude:
   - Word 12: Degrees + Hemisphere (E/W)
   - Word 13: Minutes + fractional minutes

**4.2 BNR (Binary) Encoding**
-------------------------------

Most parameters use **Binary Number Representation (BNR):**

.. code-block:: text

   11-bit signed integer (Bit 12 = parity):
   
   Bit 1: Sign bit (0=positive, 1=negative)
   Bits 2-11: Magnitude (10 bits, 0-1023)
   
   Value = (sign ? -1 : 1) × magnitude × resolution
   
   Example: Pressure Altitude
   - Range: -1,000 to 50,000 ft
   - Span: 51,000 ft
   - Resolution: 51,000 / 1024 ≈ 50 ft
   - Encoded: altitude_ft / 50 → 10-bit integer

**Python Decoder:**

.. code-block:: python

   def decode_bnr(word_12bit, resolution, min_value):
       """Decode ARINC 717 BNR parameter"""
       # Remove parity bit (bit 12)
       data = (word_12bit >> 1) & 0x7FF  # 11 bits
       
       # Check sign bit (bit 1)
       sign = (data >> 10) & 0x1
       magnitude = data & 0x3FF  # 10 bits
       
       if sign:
           magnitude = -magnitude
       
       value = min_value + magnitude * resolution
       return value
   
   # Example: Altitude
   word = 0b101010101010  # 12-bit word from recorder
   altitude = decode_bnr(word, resolution=50, min_value=-1000)
   print(f"Altitude: {altitude} ft")

**4.3 BCD (Binary Coded Decimal)**
------------------------------------

Some parameters (especially discrete states) use BCD:

.. code-block:: text

   Each 4 bits = one decimal digit (0-9)
   
   Example: Engine N1 = 87.3%
   Encoded: 8 | 7 | 3
           1000 0111 0011 (12 bits)

**4.4 Discrete Bits**
----------------------

On/off states packed into single words:

.. code-block:: text

   Word 15: Discrete States
   Bit 1: Gear Down (1=down, 0=up)
   Bit 2: Flaps Extended (1=extended, 0=retracted)
   Bit 3: Engine 1 Fire (1=fire, 0=no fire)
   Bit 4: Master Caution
   Bit 5: Master Warning
   ...
   Bit 11: Parking Brake

================================================================================
5. Flight Data Acquisition Unit (FDAU)
================================================================================

**5.1 FDAU Architecture**
---------------------------

.. code-block:: text

   ┌──────────────────────────────────────────────────┐
   │             Flight Data Acquisition Unit          │
   │                                                   │
   │  ┌────────────────────────────────────────────┐  │
   │  │          Input Processing                   │  │
   │  │  - ARINC 429 buses (10-20 channels)        │  │
   │  │  - Discrete inputs (100+ signals)          │  │
   │  │  - Analog inputs (voltage, frequency)      │  │
   │  │  - Serial data (RS-422, etc.)              │  │
   │  └────────────────────────────────────────────┘  │
   │                      ↓                            │
   │  ┌────────────────────────────────────────────┐  │
   │  │     Parameter Conversion & Formatting       │  │
   │  │  - Scale/convert to engineering units       │  │
   │  │  - Apply calibration tables                 │  │
   │  │  - Encode to ARINC 717 BNR/BCD/discrete     │  │
   │  └────────────────────────────────────────────┘  │
   │                      ↓                            │
   │  ┌────────────────────────────────────────────┐  │
   │  │        Frame Assembly & Output              │  │
   │  │  - Build 12-bit words                       │  │
   │  │  - Insert sync words                        │  │
   │  │  - Apply parity                             │  │
   │  │  - Harvard Bi-Phase encoding                │  │
   │  └────────────────────────────────────────────┘  │
   │                      ↓                            │
   │           ARINC 717 Output                       │
   └──────────────────┬───────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         ↓                         ↓
   ┌─────────┐              ┌──────────┐
   │   FDR   │              │   QAR    │
   │(Crash-  │              │(Quick    │
   │Protected)│              │Access)   │
   └─────────┘              └──────────┘

**5.2 Input Sources**
-----------------------

**ARINC 429 Buses:**
- Air Data Computer (ADC): Altitude, airspeed, Mach, temperature
- Inertial Reference System (IRS): Attitude, position, velocity
- Flight Management Computer (FMC): Navigation, autopilot modes
- Engine FADEC: N1, N2, EGT, fuel flow

**Discrete Inputs:**
- Gear position switches
- Flap position sensors
- Fire detection circuits
- Master warning/caution lights
- Control surface positions (via synchros/resolvers)

**Analog Inputs:**
- Stick shaker activation
- Control column forces
- Hydraulic pressures
- Radio altimeter (some installations)

**5.3 FDAU Configuration**
----------------------------

FDAU programmed with **Parameter Allocation Table (PAT):**

.. code-block:: text

   Parameter: PRESSURE_ALTITUDE
   - Input Source: ARINC 429 Bus 1, Label 0x203
   - Conversion: Raw data × 0.125 (ft)
   - Range: -1,000 to 50,000 ft
   - Resolution: 4 ft
   - ARINC 717 Word: 2
   - Encoding: BNR
   - Sample Rate: 256 wps (every frame)

PAT typically loaded via ARINC 615A during aircraft maintenance.

================================================================================
6. Quick Access Recorder (QAR) Applications
================================================================================

**6.1 QAR vs FDR**
-------------------

.. code-block:: text

   Feature              FDR                    QAR
   ───────────────────  ─────────────────────  ─────────────────────
   Purpose              Accident investigation Fleet health monitoring
   Location             Tail (crash-protected) Cockpit/avionics bay
   Survival             3,400G, 1,100°C fire   No crash protection
   Access               Requires removal       Quick access (USB, CF)
   Capacity             25-50 hours            200+ hours
   Data Format          ARINC 717 raw          CSV, processed
   Cost                 $50k-200k              $5k-20k
   Regulatory Required  Yes (FAR 121/135)      No (optional)

**6.2 QAR Data Analysis**
---------------------------

Airlines use QAR data for:

**Flight Operations Quality Assurance (FOQA):**
- Hard landings (>2.0G vertical acceleration)
- Unstable approaches (high sink rate, late configuration)
- Speed/altitude exceedances
- Engine over-temp events

**Predictive Maintenance:**
- Engine trending (EGT, N1 degradation over time)
- Hydraulic system performance
- Brake wear estimation
- APU health monitoring

**Fuel Efficiency:**
- Actual vs planned fuel consumption
- Climb/descent profile optimization
- Cruise altitude selection

**Python QAR Analysis Example:**

.. code-block:: python

   import numpy as np
   import pandas as pd
   
   def analyze_landing(qar_data):
       """Detect hard landings from QAR data"""
       # qar_data: DataFrame with columns ['time', 'vert_accel', 'radio_alt', 'gear_down']
       
       # Find touchdown (radio altitude < 10 ft, gear down)
       touchdown_mask = (qar_data['radio_alt'] < 10) & (qar_data['gear_down'] == 1)
       touchdown_indices = qar_data[touchdown_mask].index
       
       if len(touchdown_indices) == 0:
           return None
       
       touchdown_idx = touchdown_indices[0]
       
       # Get vertical acceleration at touchdown ±2 seconds
       window_start = max(0, touchdown_idx - 16)  # 8 samples/sec × 2 sec
       window_end = min(len(qar_data), touchdown_idx + 16)
       
       vert_accel_window = qar_data.loc[window_start:window_end, 'vert_accel']
       max_accel = vert_accel_window.max()
       
       # Classify landing
       if max_accel > 2.0:
           severity = "HARD"
       elif max_accel > 1.6:
           severity = "FIRM"
       else:
           severity = "NORMAL"
       
       return {
           'touchdown_time': qar_data.loc[touchdown_idx, 'time'],
           'max_vert_accel': max_accel,
           'severity': severity
       }
   
   # Example usage
   qar = pd.read_csv('flight_AAL123_2026-01-15.csv')
   landing = analyze_landing(qar)
   if landing:
       print(f"Landing at {landing['touchdown_time']}: {landing['severity']} "
             f"({landing['max_vert_accel']:.2f}G)")

================================================================================
7. FDR Decoding & Analysis
================================================================================

**7.1 FDR File Formats**
-------------------------

**Raw ARINC 717:**
- Binary file, continuous stream of 12-bit words
- No file header (pure data stream)
- Sync word detection required for frame alignment

**Processed Formats:**
- **CSV:** Parameters converted to engineering units, timestamped
- **MATLAB:** .mat files for analysis
- **HDF5:** Hierarchical format for large datasets
- **Proprietary:** Vendor-specific (Teledyne, L3Harris, etc.)

**7.2 Decoding Process**
--------------------------

.. code-block:: python

   import struct
   
   class ARINC717Decoder:
       def __init__(self, words_per_frame=64, frames_per_second=4):
           self.words_per_frame = words_per_frame
           self.fps = frames_per_second
           self.sync_patterns = {
               1: 0b101010110100,  # Frame 1
               2: 0b010110110010,  # Frame 2
               3: 0b001011011001,  # Frame 3
               4: 0b100101101100   # Frame 4
           }
           
       def read_fdr_file(self, filepath):
           """Read raw ARINC 717 binary file"""
           with open(filepath, 'rb') as f:
               data = f.read()
           
           # Pack bits into 12-bit words
           words = []
           bit_buffer = 0
           bit_count = 0
           
           for byte in data:
               bit_buffer = (bit_buffer << 8) | byte
               bit_count += 8
               
               while bit_count >= 12:
                   word = (bit_buffer >> (bit_count - 12)) & 0xFFF
                   words.append(word)
                   bit_count -= 12
           
           return words
       
       def find_sync(self, words):
           """Find frame synchronization"""
           for i in range(len(words) - self.words_per_frame):
               word = words[i] >> 1  # Remove parity bit
               if word == self.sync_patterns[1]:
                   # Verify subsequent frames
                   if self._verify_sync_pattern(words, i):
                       return i
           return -1
       
       def _verify_sync_pattern(self, words, start_idx):
           """Verify 4-frame superframe sync pattern"""
           for frame_num in range(1, 5):
               idx = start_idx + (frame_num - 1) * self.words_per_frame
               if idx >= len(words):
                   return False
               word = words[idx] >> 1
               if word != self.sync_patterns[frame_num]:
                   return False
           return True
       
       def decode_parameter(self, word, param_type, resolution, offset=0):
           """Decode parameter based on type"""
           # Check parity
           if not self._check_parity(word):
               return None  # Parity error
           
           data = (word >> 1) & 0x7FF  # 11 bits
           
           if param_type == 'BNR':
               sign = (data >> 10) & 0x1
               magnitude = data & 0x3FF
               if sign:
                   magnitude = -magnitude
               return offset + magnitude * resolution
           elif param_type == 'BCD':
               # Decode BCD
               digit1 = (data >> 8) & 0xF
               digit2 = (data >> 4) & 0xF
               digit3 = data & 0xF
               return digit1 * 100 + digit2 * 10 + digit3
           elif param_type == 'DISCRETE':
               return data  # Return raw bits
           
       def _check_parity(self, word):
           """Check odd parity"""
           ones = bin(word).count('1')
           return ones % 2 == 1
   
   # Usage
   decoder = ARINC717Decoder(words_per_frame=64, frames_per_second=4)
   words = decoder.read_fdr_file('fdr_recording.dat')
   sync_idx = decoder.find_sync(words)
   
   if sync_idx >= 0:
       print(f"Frame sync found at word {sync_idx}")
       # Decode altitude from word 2
       alt_word = words[sync_idx + 1]
       altitude = decoder.decode_parameter(alt_word, 'BNR', resolution=4, offset=-1000)
       print(f"Altitude: {altitude} ft")

================================================================================
8. Accident Investigation Usage
================================================================================

**8.1 NTSB/EASA FDR Analysis**
--------------------------------

When aircraft accident occurs:

1. **Recovery:** FDR retrieved from wreckage (orange "black box", ULB pinger)
2. **Extraction:** Data downloaded in lab (may require cleaning, repair)
3. **Decoding:** ARINC 717 stream decoded to engineering units
4. **Visualization:** Parameters plotted vs time
5. **Analysis:** Reconstruct sequence of events

**Key Parameters for Investigation:**
- **Last 30 seconds:** Critical for determining cause
- **Control inputs:** Pilot actions (stick, rudder, throttle)
- **Flight path:** Altitude, airspeed, heading changes
- **System status:** Warnings, failures, autopilot modes
- **Engine data:** Thrust levels, temperatures

**8.2 Famous Examples**
------------------------

**Air France 447 (2009):**
- FDR recovered after 2 years underwater
- ARINC 717 data showed pitot tube icing → autopilot disconnect → aerodynamic stall
- Pilots pulled back on stick (incorrect recovery), aircraft descended into ocean

**Asiana 214 (2013):**
- FDR showed decreasing airspeed on approach to KSFO
- Autothrottle not engaged, pilots unaware until too late
- Hard landing short of runway, tail strike

================================================================================
9. Exam Preparation — 5 Questions
================================================================================

**Question 1: Harvard Bi-Phase Encoding (10 points)**

a) Draw the Harvard Bi-Phase waveform for binary sequence: 1 0 1 1 0 (5 pts)
b) Explain why this encoding is "self-clocking" (3 pts)
c) What advantage does this provide for ARINC 717? (2 pts)

**Answer:**

a) Waveform:

.. code-block:: text

   Data:     1    0    1    1    0
           ┌────┐    ┌────┬────┐    
   Signal: │    │    │    │    │    
   ────────┘    └────┘    └────┘────
           ↑    ↑    ↑    ↑    ↑  (mandatory mid-bit transitions)
           ↑         ↑    ↑        (start transitions = 1)

b) **Self-clocking explanation:**
   - Every bit period has transition at middle (mandatory)
   - Receiver Phase-Locked Loop (PLL) locks to these transitions
   - Clock extracted from data stream (no separate clock wire needed)

c) **Advantage for ARINC 717:**
   - Simplifies wiring (only 1 differential pair, not 2)
   - Reduces electromagnetic interference (fewer wires)
   - Receiver can start anywhere in stream (finds sync word)

---

**Question 2: Frame Structure (12 points)**

Given ARINC 717 configuration:
- Word rate: 512 wps
- Frame size: 128 words
- Subframes: 4 (32 words each)

a) Calculate frame rate (frames/second) (3 pts)
b) Calculate time duration of one frame (3 pts)
c) Calculate superframe duration (3 pts)
d) How many times per second is each parameter sampled? (3 pts)

**Answer:**

a) **Frame rate:**
   - Words/second = 512
   - Words/frame = 128
   - Frame rate = 512 / 128 = **4 frames/second**

b) **Frame duration:**
   - Duration = 1 / frame_rate = 1 / 4 = **0.25 seconds = 250 ms**

c) **Superframe duration:**
   - Superframe = 4 frames
   - Duration = 4 × 250 ms = **1 second**

d) **Parameter sample rate:**
   - If parameter in every frame: **4 samples/second**
   - If parameter in every subframe: **16 samples/second** (4 frames × 4 subframes)
   - If parameter in only Frame 1: **1 sample/second**

---

**Question 3: BNR Parameter Decoding (10 points)**

ARINC 717 word (12 bits): 0b101010101011

a) Extract data bits (remove parity) (2 pts)
b) Check if parity is correct (odd parity) (3 pts)
c) Decode as BNR with resolution=0.5, offset=100 (5 pts)

**Answer:**

a) **Extract data bits:**
   - Word: 101010101011
   - Parity bit (bit 12): 1
   - Data bits (1-11): **10101010101**

b) **Parity check:**
   - Count 1s in full word: 1+0+1+0+1+0+1+0+1+0+1+1 = **7 ones**
   - 7 is odd → **Parity correct ✓**

c) **BNR Decoding:**
   - Data: 10101010101 (11 bits)
   - Sign bit (bit 1): 1 (negative)
   - Magnitude (bits 2-11): 0101010101 = 341 decimal
   - Signed magnitude: -341
   - Value = offset + magnitude × resolution
   - Value = 100 + (-341) × 0.5 = 100 - 170.5 = **-70.5**

---

**Question 4: FDAU Configuration (8 points)**

Design parameter allocation for these flight parameters in 64-word frame:
- Pressure Altitude (critical, high rate)
- Engine 1 N1 (moderate rate)
- Gear Position (low rate, discrete)

a) Assign word positions (justify choices) (4 pts)
b) Choose encoding type for each (2 pts)
c) Determine sample rates (2 pts)

**Answer:**

a) **Word Assignments:**
   - **Word 1:** Sync word (mandatory)
   - **Word 2:** Pressure Altitude
     - Justification: Critical parameter, assign early in frame
   - **Word 3:** Engine 1 N1
     - Justification: Important, but less critical than altitude
   - **Word 10:** Gear Position
     - Justification: Low-rate discrete, can be later in frame

b) **Encoding Types:**
   - **Pressure Altitude:** BNR (continuous value, -1000 to 50,000 ft)
   - **Engine 1 N1:** BNR or BCD (percentage, 0-120%)
   - **Gear Position:** DISCRETE (3 states: up/down/transit)

c) **Sample Rates:**
   - **Pressure Altitude:** Every frame (256/sec for 256 wps config)
   - **Engine 1 N1:** Every frame or every 2 frames (128/sec)
   - **Gear Position:** Every 4 frames (64/sec) - changes infrequently

---

**Question 5: QAR vs FDR (10 points)**

a) List 3 key differences between QAR and FDR (6 pts)
b) Why do airlines install QAR if FDR is already required? (4 pts)

**Answer:**

a) **Three Key Differences:**
   
   1. **Crash Protection:**
      - FDR: Survives 3,400G impact, 1,100°C fire, 20,000 ft seawater
      - QAR: No crash protection (normal avionics bay environment)
   
   2. **Data Access:**
      - FDR: Requires aircraft downtime, physical removal
      - QAR: Quick access via USB, CompactFlash, or network download
   
   3. **Capacity:**
      - FDR: 25-50 hours (regulatory minimum)
      - QAR: 200-1000+ hours (large storage for trending)

b) **Why Install QAR:**
   - **Proactive Safety (FOQA):** Detect unsafe trends before accidents (hard landings, unstable approaches)
   - **Predictive Maintenance:** Engine/system health monitoring reduces unscheduled downtime
   - **Fuel Efficiency:** Analyze flight profiles to optimize fuel consumption
   - **Pilot Training:** Provide feedback on technique without punitive intent
   - **Cost Savings:** FDR analysis requires accident, QAR enables continuous improvement

================================================================================
10. Completion Checklist
================================================================================

□ Understand Harvard Bi-Phase encoding (self-clocking principle)
□ Know 12-bit word structure (11 data bits + parity)
□ Understand frame/subframe/superframe hierarchy
□ Decode BNR (binary) parameters
□ Decode BCD (binary coded decimal) parameters
□ Identify sync word patterns
□ Calculate sample rates from word/frame rates
□ Understand FDAU architecture and input sources
□ Differentiate FDR vs QAR purposes and capabilities
□ Decode raw ARINC 717 binary data
□ Perform parity checking
□ Analyze QAR data for FOQA applications

================================================================================
11. Key Takeaways
================================================================================

1. **ARINC 717 = FDR/QAR Interface:** High-speed digital format for flight data recording (replaces ARINC 573)

2. **Harvard Bi-Phase = Self-Clocking:** No separate clock line needed, simplifies wiring and improves reliability

3. **12-Bit Words:** 11 data bits + 1 parity bit, organized in frames/subframes/superframes

4. **Variable Word Rates:** 64 to 4096 wps, determines sample rate and data resolution

5. **BNR Encoding Dominant:** Most parameters use binary with sign bit + 10-bit magnitude

6. **FDAU = Data Hub:** Collects from ARINC 429, discretes, analog → formats to ARINC 717

7. **FDR = Accident Investigation:** Crash-protected, 25-50 hours, regulatory required

8. **QAR = Fleet Monitoring:** Quick access, 200+ hours, FOQA/predictive maintenance

9. **Sync Words:** Enable frame alignment, different patterns for superframe synchronization

10. **Regulatory Critical:** FAR 121/135, EASA CS-25 mandate FDR with 88+ parameters

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 717 Specification (Mark 33 Digital Flight Data Acquisition)
- EUROCAE ED-112 (European equivalent)
- FAA TSO-C124b (FDR Technical Standards)
- FAA TSO-C176 (QAR approval)

**Regulatory:**
- FAR 121.343/344 (FDR requirements)
- EASA CS-25.1459 (Flight data recorders)
- ICAO Annex 6 (Operation of Aircraft)

**Equipment Vendors:**
- Teledyne Controls (FDR/QAR systems)
- L3Harris (FDAU, recorders)
- Honeywell (Integrated recorders)
- Collins Aerospace (Flight data systems)

**Software:**
- AGS FlightViz (QAR analysis)
- Teledyne MPADS (FDR decoding)
- NTSB FDR Lab Tools

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** ARINC 717, EUROCAE ED-112, FAA TSO-C124b

================================================================================
