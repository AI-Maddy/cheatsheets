============================================================
ARINC 825 — CAN Bus for General Aviation Avionics
============================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC 825** adapts the automotive **Controller Area Network (CAN)** bus standard (ISO 11898) for use in general aviation avionics systems.

**Key Characteristics:**
- **Base Technology:** ISO 11898 CAN 2.0B (29-bit extended identifiers)
- **Speed:** Up to 1 Mbps (typical: 250-500 kbps for avionics)
- **Topology:** Multi-drop bus, up to 32 nodes (practical: 15-20)
- **Arbitration:** Non-destructive bitwise arbitration (priority-based)
- **Applications:** General aviation, engine monitoring, experimental aircraft, UAVs
- **Advantages:** Lower cost than ARINC 429, automotive heritage, multi-drop capability

**Typical Systems:**
- Garmin G1000/G3000 avionics suites
- Cirrus Perspective flight decks
- Experimental aircraft (Dynon, MGL, etc.)
- UAV control systems
- Engine FADEC interfaces

**ARINC 825 vs ARINC 429:**
- **Cost:** 50-70% lower hardware cost
- **Topology:** Multi-drop (vs point-to-point)
- **Speed:** Up to 1 Mbps (vs 100 kbps)
- **Certification:** Simpler for GA (Part 23) vs transport (Part 25)

================================================================================
1. Overview & Background
================================================================================

**1.1 Why CAN for Aviation?**
-------------------------------

**Automotive CAN Success:**
- Proven in 1 billion+ vehicles since 1986
- Robust error detection (15-bit CRC, stuffing, ACK)
- Real-time performance (deterministic latency)
- Low cost silicon ($1-5 per node vs $50+ for ARINC 429)

**General Aviation Needs:**
- Cost-sensitive market (experimental aircraft, LSA, Part 23)
- Smaller aircraft (fewer systems than Boeing 787)
- Multi-drop reduces wiring weight
- Integration with automotive-grade sensors (OBD-II, etc.)

**ARINC 825 Adaptations:**
- Maps avionics parameters to CAN message IDs
- Defines standard Service Codes (similar to J1939)
- Specifies redundancy for critical systems
- Provides certification guidance for Part 23

**1.2 Market Adoption**
------------------------

**Garmin G1000 (2004):**
- First major GA avionics suite using ARINC 825
- 2× CAN buses (primary + backup)
- Integrates PFD, MFD, AHRS, ADC, GPS, autopilot
- Certified for Cessna 172/182/206, Beechcraft, Diamond, Cirrus

**Cirrus Perspective (2008):**
- Dual ARINC 825 buses
- Cirrus SR20/SR22 standard equipment
- Integrates with CAPS (parachute system)

**Experimental Aircraft (Dynon, MGL, etc.):**
- EFIS systems use ARINC 825 or proprietary CAN
- Engine monitoring (EGT, CHT, fuel flow)
- Autopilot integration

================================================================================
2. CAN Bus Fundamentals
================================================================================

**2.1 Physical Layer (ISO 11898-2)**
--------------------------------------

**Differential Signaling:**
- **CAN_H (CAN High):** Dominant = 3.5V, Recessive = 2.5V
- **CAN_L (CAN Low):** Dominant = 1.5V, Recessive = 2.5V
- **Differential Voltage:**
  - Dominant (logic 0): CAN_H - CAN_L = 2V
  - Recessive (logic 1): CAN_H - CAN_L = 0V

**Bus Topology:**

.. code-block:: text

                120Ω
   ┌─────────────────────────────────────┐
   │                                     │
   │  Node1    Node2    Node3    Node4   │
   │    │        │        │        │     │
   ├────┴────────┴────────┴────────┴─────┤  CAN_H
   │                                     │
   ├─────────────────────────────────────┤  CAN_L
   │                                     │
   └─────────────────────────────────────┘
                120Ω
   
   - Twisted pair cable (120Ω impedance)
   - 120Ω termination resistors at both ends
   - Maximum length: ~40m @ 1 Mbps, ~500m @ 125 kbps
   - Stub length: < 30 cm per node

**Bit Timing:**

.. code-block:: text

   Bit period divided into segments:
   
   │←─ SYNC ─→│←─ PROP ─→│←─ PHASE1 ─→│←─ PHASE2 ─→│
   
   Typical 500 kbps (2 μs bit time):
   - SYNC: 1 time quantum (TQ)
   - PROP: 2 TQ (propagation delay)
   - PHASE1: 3 TQ (before sample point)
   - PHASE2: 3 TQ (after sample point)
   - Total: 10 TQ × 200 ns = 2 μs = 500 kbps

**2.2 Data Link Layer**
------------------------

**CAN Frame Format (Extended, 29-bit ID):**

.. code-block:: text

   ┌───┬───┬────┬───┬───┬─────────┬───┬─────┬───────┬─────┬───┬───┬───┐
   │SOF│ ID │SRR │IDE│RTR│   EID   │r0 │ DLC │ DATA  │ CRC │ACK│EOF│IFS│
   └───┴───┴────┴───┴───┴─────────┴───┴─────┴───────┴─────┴───┴───┴───┘
    1   11   1    1   1     18      1    4    0-64     16   2   7   3
   
   SOF: Start of Frame (dominant bit)
   ID: Base Identifier (11 bits, high priority = low value)
   SRR: Substitute Remote Request (recessive)
   IDE: Identifier Extension (recessive for 29-bit)
   RTR: Remote Transmission Request (0=data frame)
   EID: Extended Identifier (18 bits)
   r0: Reserved bit
   DLC: Data Length Code (0-8 bytes)
   DATA: Payload (0-8 bytes)
   CRC: 15-bit Cyclic Redundancy Check + delimiter
   ACK: Acknowledge slot + delimiter
   EOF: End of Frame (7 recessive bits)
   IFS: Inter-Frame Space (3 recessive bits)

**Full 29-bit Identifier:**
- Bits 28-18: Base ID (11 bits)
- Bits 17-0: Extended ID (18 bits)
- **ARINC 825 uses extended IDs** to encode Service Code, Node ID, Data Type

**2.3 Arbitration & Priority**
--------------------------------

**Non-Destructive Bitwise Arbitration:**
- Multiple nodes can transmit simultaneously
- During ID transmission, dominant (0) wins over recessive (1)
- Node transmitting recessive bit sees dominant → stops transmitting
- Winning node continues, losing nodes retry later

**Priority Example:**

.. code-block:: text

   Time →
   
   Node A (ID 0x100): 0 0 0 1 0 0 0 0 0 0 0 0
   Node B (ID 0x0FF): 0 0 0 0 1 1 1 1 1 1 1 1
   Bus (wired-AND):   0 0 0 0 ↑
                             Arbitration lost (Node A wins)
   
   Lower ID = Higher Priority

**ARINC 825 Priority Scheme:**
- Critical data (altitude, airspeed): Low IDs (high priority)
- Periodic status: Medium IDs
- Configuration/diagnostics: High IDs (low priority)

================================================================================
3. ARINC 825 Message Structure
================================================================================

**3.1 29-Bit Identifier Encoding**
------------------------------------

ARINC 825 defines identifier format:

.. code-block:: text

   Bits 28-24: Service Code (5 bits) - Message type/function
   Bits 23-21: Message Code (3 bits) - Subtype within service
   Bits 20-16: Node ID (5 bits) - Source node (0-31)
   Bits 15-8:  Data Type ID (8 bits) - Parameter identifier
   Bits 7-0:   Reserved / Subtype (8 bits)
   
   Example: Altitude from Air Data Computer (Node 5)
   Service Code: 0x02 (Flight Data)
   Message Code: 0x1 (Periodic data)
   Node ID: 0x05
   Data Type: 0x10 (Pressure Altitude)
   
   Full ID: 0x02A51000 (binary: 00010 001 00101 00010000 00000000)

**3.2 Service Codes**
----------------------

.. code-block:: text

   Code  Service                    Description
   ────  ─────────────────────────  ──────────────────────────────
   0x00  Node Service               Node status, heartbeat, errors
   0x01  Identified Data Service    User-defined parameters
   0x02  High-Speed Data Service    Periodic flight data (>1 Hz)
   0x03  Normal Operation Service   Standard periodic data
   0x04  Node Configuration Service Configuration requests/responses
   0x05  Test Service               Built-in test, diagnostics
   0x06  Download Service           Software/database loading
   0x07-0x1F Reserved / Proprietary  Vendor-specific extensions

**3.3 Data Encoding**
----------------------

**Little-Endian (Intel format):**
ARINC 825 specifies little-endian byte order (unlike ARINC 429 big-endian):

.. code-block:: text

   Example: 32-bit altitude = 0x12345678
   
   Byte order in CAN frame:
   Data[0] = 0x78 (LSB)
   Data[1] = 0x67
   Data[2] = 0x56
   Data[3] = 0x12 (MSB)

**Common Data Types:**

.. code-block:: c

   // Pressure Altitude (4 bytes, little-endian)
   typedef struct {
       int32_t altitude_ft;  // -1,000 to 50,000 ft
   } AltitudeMsg;
   
   // Airspeed (4 bytes)
   typedef struct {
       uint16_t ias_knots;   // Indicated airspeed, 0.1 kt resolution
       uint16_t tas_knots;   // True airspeed, 0.1 kt resolution
   } AirspeedMsg;
   
   // Attitude (6 bytes)
   typedef struct {
       int16_t pitch_deg;    // ±90°, 0.01° resolution
       int16_t roll_deg;     // ±180°, 0.01° resolution
       uint16_t heading_deg; // 0-360°, 0.01° resolution
   } AttitudeMsg;

================================================================================
4. ARINC 825 Implementation Example
================================================================================

**4.1 Hardware Setup**
-----------------------

**Typical GA Avionics System:**

.. code-block:: text

   ┌────────────────────────────────────────────────────┐
   │                  CAN Bus (500 kbps)                 │
   ├────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬──┤
        │    │    │    │    │    │    │    │    │    │
        │    │    │    │    │    │    │    │    │    │
      ┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐┌─┴─┐
      │PFD││MFD││ADC││AHRS│GPS││ENG││AP ││COM││NAV││AXI│
      └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘
      Node Node Node Node Node Node Node Node Node Node
       1    2    3    4    5    6    7    8    9   10
   
   PFD: Primary Flight Display
   MFD: Multi-Function Display
   ADC: Air Data Computer
   AHRS: Attitude & Heading Reference System
   GPS: GPS Navigator
   ENG: Engine Monitor
   AP: Autopilot
   COM: Communication Radio
   NAV: Navigation Radio
   AXI: Audio Panel

**4.2 C Code Example (Transmitter)**
--------------------------------------

.. code-block:: c

   #include <stdint.h>
   #include "can_driver.h"  // Hardware-specific CAN driver
   
   // ARINC 825 definitions
   #define SERVICE_HIGH_SPEED_DATA  0x02
   #define MSG_CODE_PERIODIC        0x01
   #define NODE_ID_ADC              0x03
   #define DATATYPE_ALTITUDE        0x10
   #define DATATYPE_AIRSPEED        0x11
   
   // Build ARINC 825 extended ID
   uint32_t build_arinc825_id(uint8_t service_code, uint8_t msg_code,
                               uint8_t node_id, uint8_t data_type) {
       uint32_t id = 0;
       id |= ((uint32_t)service_code & 0x1F) << 24;
       id |= ((uint32_t)msg_code & 0x07) << 21;
       id |= ((uint32_t)node_id & 0x1F) << 16;
       id |= ((uint32_t)data_type & 0xFF) << 8;
       return id;
   }
   
   // Send altitude message
   void send_altitude(int32_t altitude_ft) {
       can_msg_t msg;
       
       // Build ID
       msg.id = build_arinc825_id(SERVICE_HIGH_SPEED_DATA,
                                   MSG_CODE_PERIODIC,
                                   NODE_ID_ADC,
                                   DATATYPE_ALTITUDE);
       msg.ide = 1;  // Extended ID
       msg.rtr = 0;  // Data frame
       msg.dlc = 4;  // 4 bytes
       
       // Encode data (little-endian)
       msg.data[0] = (altitude_ft >> 0) & 0xFF;
       msg.data[1] = (altitude_ft >> 8) & 0xFF;
       msg.data[2] = (altitude_ft >> 16) & 0xFF;
       msg.data[3] = (altitude_ft >> 24) & 0xFF;
       
       // Transmit
       can_transmit(&msg);
   }
   
   // Periodic task (10 Hz)
   void adc_periodic_task(void) {
       int32_t altitude = read_pressure_sensor();  // Read ADC
       send_altitude(altitude);
   }

**4.3 C Code Example (Receiver)**
-----------------------------------

.. code-block:: c

   // Receive and decode altitude
   void can_receive_callback(can_msg_t *msg) {
       // Decode ARINC 825 ID
       uint8_t service_code = (msg->id >> 24) & 0x1F;
       uint8_t msg_code = (msg->id >> 21) & 0x07;
       uint8_t node_id = (msg->id >> 16) & 0x1F;
       uint8_t data_type = (msg->id >> 8) & 0xFF;
       
       // Check if this is altitude from ADC
       if (service_code == SERVICE_HIGH_SPEED_DATA &&
           node_id == NODE_ID_ADC &&
           data_type == DATATYPE_ALTITUDE) {
           
           // Decode little-endian int32
           int32_t altitude = (int32_t)(
               (msg->data[0] << 0) |
               (msg->data[1] << 8) |
               (msg->data[2] << 16) |
               (msg->data[3] << 24)
           );
           
           // Update display
           update_altitude_display(altitude);
       }
   }
   
   // Hardware CAN interrupt handler
   void CAN_RX_IRQHandler(void) {
       can_msg_t msg;
       if (can_read_message(&msg)) {
           can_receive_callback(&msg);
       }
   }

**4.4 Python Simulation Example**
-----------------------------------

.. code-block:: python

   import can
   import struct
   import time
   
   class ARINC825:
       # Service codes
       SERVICE_HIGH_SPEED = 0x02
       MSG_PERIODIC = 0x01
       
       # Node IDs
       NODE_ADC = 0x03
       NODE_PFD = 0x01
       
       # Data types
       DATATYPE_ALTITUDE = 0x10
       DATATYPE_AIRSPEED = 0x11
       
       @staticmethod
       def build_id(service, msg_code, node_id, data_type):
           """Build ARINC 825 29-bit identifier"""
           return ((service & 0x1F) << 24 |
                   (msg_code & 0x07) << 21 |
                   (node_id & 0x1F) << 16 |
                   (data_type & 0xFF) << 8)
       
       @staticmethod
       def decode_id(can_id):
           """Decode ARINC 825 identifier"""
           return {
               'service': (can_id >> 24) & 0x1F,
               'msg_code': (can_id >> 21) & 0x07,
               'node_id': (can_id >> 16) & 0x1F,
               'data_type': (can_id >> 8) & 0xFF
           }
   
   # Transmitter (Air Data Computer)
   def adc_transmitter():
       bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
       
       altitude_ft = 10000
       while True:
           # Build message
           msg_id = ARINC825.build_id(
               ARINC825.SERVICE_HIGH_SPEED,
               ARINC825.MSG_PERIODIC,
               ARINC825.NODE_ADC,
               ARINC825.DATATYPE_ALTITUDE
           )
           
           # Encode altitude (little-endian int32)
           data = struct.pack('<i', altitude_ft)
           
           # Send CAN message
           msg = can.Message(
               arbitration_id=msg_id,
               data=data,
               is_extended_id=True
           )
           bus.send(msg)
           
           altitude_ft += 100  # Simulate climbing
           time.sleep(0.1)  # 10 Hz update
   
   # Receiver (Primary Flight Display)
   def pfd_receiver():
       bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
       
       for msg in bus:
           # Decode ID
           decoded = ARINC825.decode_id(msg.arbitration_id)
           
           if (decoded['service'] == ARINC825.SERVICE_HIGH_SPEED and
               decoded['node_id'] == ARINC825.NODE_ADC and
               decoded['data_type'] == ARINC825.DATATYPE_ALTITUDE):
               
               # Decode altitude
               altitude = struct.unpack('<i', msg.data)[0]
               print(f"Altitude: {altitude} ft")

================================================================================
5. Error Detection & Fault Tolerance
================================================================================

**5.1 CAN Error Detection Mechanisms**
----------------------------------------

**Five Error Detection Methods:**

1. **CRC (Cyclic Redundancy Check):**
   - 15-bit CRC on entire frame
   - Hamming distance = 6 (detects up to 5-bit errors)

2. **Bit Stuffing:**
   - After 5 consecutive identical bits, insert opposite bit
   - Receiver removes stuffed bits
   - Violation detected if 6+ consecutive bits seen

3. **Frame Check:**
   - Fixed-format fields (SOF, EOF, ACK, etc.)
   - Violation if format incorrect

4. **ACK Check:**
   - Transmitter sends recessive ACK slot
   - At least one receiver must send dominant ACK
   - No ACK → transmission error

5. **Bit Monitoring:**
   - Transmitter reads back each bit
   - Mismatch (except during arbitration) → error

**Error Statistics:**
- **Undetected error probability:** < 4.7 × 10⁻¹¹ per message
- **Residual error rate:** < 10⁻¹³ (better than ARINC 429)

**5.2 Redundant Bus Architecture**
------------------------------------

For critical systems (e.g., Garmin G1000):

.. code-block:: text

   ┌─────────────────────────────────────┐
   │          CAN Bus A (Primary)         │
   ├───┬───┬───┬───┬───┬───┬───┬───┬───┬─┤
       │   │   │   │   │   │   │   │   │
       ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
     Nodes with dual CAN controllers
       │   │   │   │   │   │   │   │   │
       ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
   ├───┴───┴───┴───┴───┴───┴───┴───┴───┴─┤
   │          CAN Bus B (Backup)          │
   └─────────────────────────────────────┘
   
   - Both buses transmit same data
   - Receiver validates CRC on both
   - Use Bus A if valid, else Bus B
   - Alerts crew if one bus fails

**Voting Logic:**

.. code-block:: c

   typedef struct {
       int32_t altitude_a;  // From Bus A
       int32_t altitude_b;  // From Bus B
       bool valid_a;
       bool valid_b;
   } RedundantAltitude;
   
   int32_t get_validated_altitude(RedundantAltitude *alt) {
       if (alt->valid_a && alt->valid_b) {
           // Both valid - check agreement
           if (abs(alt->altitude_a - alt->altitude_b) < 100) {
               return alt->altitude_a;  // Use primary
           } else {
               // Disagreement - flag error
               set_altitude_fail_flag();
               return alt->altitude_a;  // Use primary with caution
           }
       } else if (alt->valid_a) {
           set_bus_b_fail_flag();
           return alt->altitude_a;
       } else if (alt->valid_b) {
           set_bus_a_fail_flag();
           return alt->altitude_b;
       } else {
           set_altitude_invalid_flag();
           return 0;  // No valid data
       }
   }

================================================================================
6. ARINC 825 vs ARINC 429 Comparison
================================================================================

.. code-block:: text

   Feature              ARINC 825 (CAN)        ARINC 429
   ──────────────────── ─────────────────────  ────────────────────
   Topology             Multi-drop bus         Point-to-point
   Max Nodes            32 (practical: 20)     1 transmitter, 20 receivers
   Speed                Up to 1 Mbps           12.5 / 100 kbps
   Arbitration          Priority-based         N/A (single transmitter)
   Cost per Node        $5-20                  $50-200
   Wiring               Single twisted pair    Separate wire per link
   Heritage             Automotive (ISO 11898) Aerospace (1970s)
   Error Detection      5 mechanisms, <10⁻¹¹   Parity + SSM, ~10⁻⁹
   Certification        Part 23 (GA)           Part 25 (transport)
   Latency              Variable (arbitration) Fixed (periodic)
   Bandwidth Efficiency High (multi-drop)      Low (point-to-point)

**When to Use ARINC 825:**
- General aviation (Part 23)
- Experimental / homebuilt aircraft
- UAV systems
- Cost-sensitive applications
- Systems with many nodes

**When to Use ARINC 429:**
- Transport category (Part 25)
- Critical systems requiring determinism
- Retrofit of existing ARINC 429 systems
- Integration with legacy avionics

================================================================================
7. Real-World Applications
================================================================================

**7.1 Garmin G1000 Integrated Flight Deck**
---------------------------------------------

**Architecture:**
- **2× CAN buses** (ARINC 825-compliant)
- **10+ nodes:** PFD, MFD, GIA (integrated avionics), GRS (AHRS), GDC (ADC), GTX (transponder), etc.
- **Message rate:** 10-50 Hz for flight data, 1 Hz for status
- **Redundancy:** Dual buses, cross-channel monitoring

**Typical Messages:**
- Altitude: 10 Hz (100 ms period)
- Airspeed: 10 Hz
- Attitude (pitch/roll): 20 Hz
- GPS position: 5 Hz
- Engine parameters: 2 Hz

**7.2 Dynon SkyView (Experimental Aircraft)**
----------------------------------------------

**Open CAN Protocol:**
- Dynon publishes CAN message format
- Enables third-party integration (engine monitors, autopilots)
- Popular in homebuilt / experimental aircraft

**Example Integration:**
- Dynon SkyView EFIS (Node 1)
- Dynon ADAHRS (Node 2)
- UAvionix AV-30 backup (Node 3)
- MGL EMS engine monitor (Node 4)

================================================================================
8. Certification & DO-160 Compliance
================================================================================

**8.1 Part 23 Certification (GA Aircraft)**
---------------------------------------------

**FAA Requirements:**
- RTCA DO-160G environmental testing (vibration, EMI, temperature)
- Software: DO-178C (typically DAL C or D for GA)
- Hardware: DO-254 (DAL C or D)

**ARINC 825 Benefits for Certification:**
- Mature automotive CAN standard (proven reliability)
- Published ARINC 825 specification aids approval
- Redundant bus architecture for critical functions

**8.2 DO-160G Environmental Testing**
---------------------------------------

**Key Tests for CAN Transceivers:**
- **Temperature:** -55°C to +85°C (altitude -54°C to +55°C cockpit)
- **Vibration:** 5G operational, 15G crash
- **EMI/EMC:** Radiated/conducted emissions, susceptibility
- **Lightning:** Indirect effects (voltage transients)
- **Humidity:** 95% RH, salt fog

**CAN-Specific Concerns:**
- Bus termination resistor tolerance (must handle temp extremes)
- Differential voltage margin (ensure >2V dominant state)
- Common-mode rejection (protect against EMI)

================================================================================
9. Exam Preparation — 5 Questions
================================================================================

**Question 1: CAN Arbitration (10 points)**

Three nodes attempt to transmit simultaneously:
- Node A: ID 0x100
- Node B: ID 0x0FF
- Node C: ID 0x101

a) Which node wins arbitration? (3 pts)
b) At which bit position does each losing node detect loss? (4 pts)
c) What happens to the losing nodes' messages? (3 pts)

**Answer:**

a) **Node B wins** (ID 0x0FF is lowest, highest priority)

b) **Arbitration bit-by-bit (11-bit base ID):**

.. code-block:: text

   Bit:     10 9 8 7 6 5 4 3 2 1 0
   Node A:  0 0 0 1 0 0 0 0 0 0 0
   Node B:  0 0 0 0 1 1 1 1 1 1 1
   Node C:  0 0 0 1 0 0 0 0 0 0 1
   Bus:     0 0 0 0 ← Arbitration point
   
   - Bit 7: All transmit 0, all continue
   - Bit 6: Node A transmits 1 (recessive), sees 0 on bus → **loses**
   - Bit 6: Node C transmits 1 (recessive), sees 0 on bus → **loses**
   - Node B continues alone

c) **Losing nodes' behavior:**
   - Stop transmitting immediately (become receivers)
   - Receive Node B's message
   - Retry transmission after Node B finishes
   - Automatic retransmission (no software intervention)

---

**Question 2: ARINC 825 ID Encoding (12 points)**

Encode ARINC 825 extended ID for:
- Service: High-Speed Data (0x02)
- Message Code: Periodic (0x01)
- Node ID: AHRS (0x04)
- Data Type: Pitch Angle (0x20)

a) Calculate 29-bit identifier (show work) (6 pts)
b) Convert to hexadecimal (3 pts)
c) What is message priority relative to altitude (Data Type 0x10)? (3 pts)

**Answer:**

a) **29-bit ID Calculation:**

.. code-block:: text

   Bits 28-24: Service = 0x02 = 00010
   Bits 23-21: Msg Code = 0x01 = 001
   Bits 20-16: Node ID = 0x04 = 00100
   Bits 15-8:  Data Type = 0x20 = 00100000
   Bits 7-0:   Reserved = 0x00 = 00000000
   
   Full ID (binary):
   00010 001 00100 00100000 00000000
   
   Group into bytes:
   00010001 00100001 00000000 00000
   
b) **Hexadecimal:**
   - 29 bits = 0x11100000 (need to align)
   - Proper alignment: **0x11102000**

c) **Priority Comparison:**
   - Altitude ID: 0x02A50**10**00 (Data Type 0x10)
   - Pitch ID:    0x02A51**20**00 (Data Type 0x20)
   - **Pitch has lower priority** (0x20 > 0x10, higher numerical ID)
   - Altitude messages win arbitration over pitch

---

**Question 3: Error Detection (10 points)**

a) List three error detection mechanisms in CAN (3 pts)
b) Calculate probability two nodes receive different data (4 pts)
c) How does redundant bus architecture improve reliability? (3 pts)

**Answer:**

a) **Three Error Detection Mechanisms:**
   1. **15-bit CRC:** Cyclic redundancy check on entire frame
   2. **Bit Stuffing:** Insert opposite bit after 5 consecutive identical bits
   3. **ACK Check:** At least one receiver must acknowledge

b) **Probability of Undetected Error:**
   - CAN undetected error rate: < 4.7 × 10⁻¹¹ per message
   - If two nodes receive same message independently:
   - Both corrupted differently: (4.7 × 10⁻¹¹)² ≈ **2.2 × 10⁻²¹**
   - **Extremely unlikely** (once per 10¹⁴ years at 1 msg/sec)

c) **Redundant Bus Benefits:**
   - **Single fault tolerance:** Failure of one bus doesn't lose data
   - **Error detection:** Compare data from both buses (cross-check)
   - **Continued operation:** Switch to backup bus if primary fails
   - **Crew alerting:** Warn pilots of degraded redundancy

---

**Question 4: ARINC 825 vs 429 (8 points)**

a) Why is ARINC 825 cheaper than ARINC 429 for multi-node systems? (4 pts)
b) What advantage does ARINC 429 have over ARINC 825 for critical systems? (4 pts)

**Answer:**

a) **ARINC 825 Cost Advantages:**
   - **Automotive silicon:** CAN controllers mass-produced ($1-5 vs $50+)
   - **Single bus:** One twisted pair serves all nodes
     - ARINC 429: N transmitters × M receivers = N×M wire pairs
     - ARINC 825: 1 twisted pair for all nodes
   - **Example:** 10-node system
     - ARINC 429: 45 point-to-point links (10×9/2) = 90 wires
     - ARINC 825: 1 bus = 2 wires (97% reduction)

b) **ARINC 429 Advantages:**
   - **Deterministic timing:** Fixed transmission schedule (no arbitration delays)
     - Critical for flight control (predictable latency)
   - **Isolation:** Point-to-point prevents single-point-of-failure
     - Faulty node can't disrupt entire bus (ARINC 825 risk: "babbling node")
   - **Certification heritage:** 40+ years Part 25 transport aircraft
   - **Unidirectional:** Simplified fault analysis (no arbitration complexity)

---

**Question 5: Message Design (10 points)**

Design ARINC 825 message for engine parameters:
- RPM (0-3000, 1 RPM resolution)
- Oil Pressure (0-100 psi, 0.1 psi resolution)
- Oil Temperature (0-200°C, 0.1°C resolution)
- Fuel Flow (0-50 gal/hr, 0.01 gal/hr resolution)

a) Choose data types and sizes (4 pts)
b) Calculate total message size (2 pts)
c) Determine update rate (justify) (4 pts)

**Answer:**

a) **Data Types:**
   - **RPM:** uint16_t (0-65535, more than enough for 0-3000)
   - **Oil Pressure:** uint16_t (0-1000 for 0.1 psi resolution)
   - **Oil Temp:** uint16_t (0-2000 for 0.1°C resolution)
   - **Fuel Flow:** uint16_t (0-5000 for 0.01 gal/hr resolution)

b) **Total Message Size:**
   - 4 parameters × 2 bytes = **8 bytes** (exactly fills CAN DLC=8)
   - Perfect fit for single CAN message

c) **Update Rate:**
   - **Recommended: 2-5 Hz**
   - **Justification:**
     - Engine parameters change relatively slowly (seconds, not milliseconds)
     - 2 Hz (500 ms) sufficient for pilot awareness
     - Higher rates waste bandwidth
     - Lower rates (1 Hz) acceptable for non-critical monitoring
   - **Critical consideration:** If fuel flow used for totalizer, 5 Hz better accuracy

================================================================================
10. Completion Checklist
================================================================================

□ Understand CAN bus physical layer (differential signaling, 120Ω termination)
□ Know CAN frame format (29-bit extended ID, 0-8 byte data)
□ Understand bitwise arbitration (lower ID = higher priority)
□ Decode ARINC 825 identifier (Service Code, Node ID, Data Type)
□ Encode/decode little-endian parameters
□ Implement CAN transmitter in C
□ Implement CAN receiver with ID filtering
□ Design redundant bus architecture
□ Calculate bus loading and message rates
□ Compare ARINC 825 vs ARINC 429 tradeoffs
□ Apply DO-160G environmental considerations
□ Understand Part 23 certification requirements

================================================================================
11. Key Takeaways
================================================================================

1. **ARINC 825 = CAN for Aviation:** Adapts automotive ISO 11898 CAN for avionics with standardized message IDs

2. **Cost Advantage:** 70% cheaper than ARINC 429 for multi-node systems (automotive silicon, single bus)

3. **Multi-Drop Topology:** Up to 32 nodes on single twisted pair (vs point-to-point ARINC 429)

4. **Priority Arbitration:** Lower ID = higher priority, non-destructive bitwise arbitration

5. **Extended IDs:** 29-bit identifiers encode Service Code, Node ID, Data Type per ARINC 825 spec

6. **High Reliability:** 5 error detection mechanisms, <10⁻¹¹ undetected error rate

7. **GA Market Dominant:** Garmin G1000/G3000, Cirrus Perspective, experimental aircraft (Dynon, MGL)

8. **Redundant Buses:** Critical systems use dual CAN buses for fault tolerance

9. **Little-Endian:** ARINC 825 specifies Intel byte order (unlike ARINC 429 big-endian)

10. **Part 23 Certification:** Proven path for GA aircraft, DO-160G environmental compliance required

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 825 Specification (General Aviation CAN Bus)
- ISO 11898-1 (CAN Data Link Layer)
- ISO 11898-2 (CAN Physical Layer - High Speed)
- RTCA DO-160G (Environmental Conditions and Test Procedures)

**Avionics Systems:**
- Garmin G1000 Integrated Flight Deck (Pilot's Guide)
- Dynon SkyView CAN Protocol Documentation
- Cirrus Perspective Flight Deck

**CAN Protocol:**
- "A Comprehensive Guide to CAN" by Wilfried Voss
- "Controller Area Network Prototyping" by Wilfried Voss
- Bosch CAN Specification 2.0

**Certification:**
- FAA Part 23 (Normal Category Airworthiness)
- RTCA DO-178C (Software Considerations)
- RTCA DO-254 (Hardware Considerations)

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Standards:** ARINC 825, ISO 11898, DO-160G

================================================================================
