🔒 **DATA DIODE TECHNOLOGY — Physical Network Isolation**
════════════════════════════════════════════════════════════════════

**Context:** Hardware-based unidirectional data flow for high-assurance isolation
**Standard:** EAL7+ (Common Criteria), DO-326A SAL 3 compliant
**Purpose:** Absolute protection for flight-critical systems (ACD)
**Mechanism:** Physical one-way transmission (optical or electrical)

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — DATA DIODES IN 60 SECONDS**
─────────────────────────────────────────

**What is a Data Diode?**

::

    Data Diode = Hardware device that allows data to flow in ONE direction only
    
    ┌───────────┐         ┌───────────┐         ┌───────────┐
    │   ACD     │ ──────> │   DATA    │ ──────> │   AISD    │
    │ (Source)  │  Data   │  DIODE    │  Data   │  (Dest)   │
    └───────────┘  ONLY   └───────────┘  ONLY   └───────────┘
                    →                      →
                 NO RETURN PATH ❌
    
    Physical Guarantee: Mathematically impossible to send data backwards

**Why Use Data Diodes?**

+----------------------------------+--------------------------------+
| **Firewall**                     | **Data Diode**                 |
+==================================+================================+
| Software-based                   | Hardware-based                 |
+----------------------------------+--------------------------------+
| Can be misconfigured             | Cannot be misconfigured        |
+----------------------------------+--------------------------------+
| Can be exploited (0-day)         | Cannot be exploited            |
+----------------------------------+--------------------------------+
| Bidirectional                    | Unidirectional (physically)    |
+----------------------------------+--------------------------------+
| SAL 1-2                          | SAL 3, EAL7+                   |
+----------------------------------+--------------------------------+

**Aviation Use Cases:**

::

    1. ACD → AISD: Flight data for moving map (sensor data, GPS, altitude)
    2. ACD → CMC: Fault codes for maintenance (read-only)
    3. Ground → Aircraft: Software updates (one-way, signed)

**Key Principle:**

    "If there is NO physical return path, there is NO way to hack back."

════════════════════════════════════════════════════════════════════

📖 **1. DATA DIODE FUNDAMENTALS**
═════════════════════════════════

**1.1 Operating Principle**
---------------------------

**Unidirectional Data Flow:**

::

    Traditional Network (Bidirectional):
    
    ┌───────────┐  Request  ┌───────────┐
    │  Client   │ ───────>  │  Server   │
    │           │ <─────── │           │
    └───────────┘  Response └───────────┘
                 ↕
              Both directions → Vulnerable to attacks
    
    ─────────────────────────────────────────────────────
    
    Data Diode (Unidirectional):
    
    ┌───────────┐           ┌───────────┐           ┌───────────┐
    │  Sender   │ ────────> │   DATA    │ ────────> │ Receiver  │
    │  (TX only)│  Data     │  DIODE    │  Data     │ (RX only) │
    └───────────┘    ║      └───────────┘     ║     └───────────┘
                     ║                        ║
                 Physical                 Physical
                   TX                       RX
                   ║                        ║
                 NO RETURN PATH ❌
                 
    Sender:   Can only transmit (no receive capability)
    Receiver: Can only receive (no transmit capability)
    Result:   Attacks from Receiver → Sender = IMPOSSIBLE

**1.2 Physical Implementations**
--------------------------------

**A) Optical Data Diode (Most Common):**

::

    ┌─────────────────────────────────────────────────────────────┐
    │                    OPTICAL DATA DIODE                       │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │                                                             │
    │  ┌────────────┐         ┌────────┐         ┌─────────────┐│
    │  │  Sender    │         │ Fiber  │         │  Receiver   ││
    │  │  Hardware  │         │ Optic  │         │  Hardware   ││
    │  │            │         │ Cable  │         │             ││
    │  │ ┌────────┐ │         │        │         │ ┌─────────┐ ││
    │  │ │  TX    │ │ Light   │  ──>   │  Light  │ │   RX    │ ││
    │  │ │ (LED/  │ │ ──────> │ ──────>│ ──────> │ │ (Photo- │ ││
    │  │ │ Laser) │ │         │        │         │ │  diode) │ ││
    │  │ └────────┘ │         │        │         │ └─────────┘ ││
    │  │            │         │        │         │             ││
    │  │ NO RECEIVE │         │ One-   │         │ NO TRANSMIT ││
    │  │ HARDWARE   │         │ way    │         │ HARDWARE    ││
    │  │     ❌     │         │ only   │         │      ❌     ││
    │  └────────────┘         └────────┘         └─────────────┘│
    │                                                             │
    │  Why it works:                                              │
    │  - Photodiode can ONLY convert light → electrical signal   │
    │  - LED/Laser can ONLY convert electrical → light           │
    │  - No physical mechanism for reverse flow                   │
    └─────────────────────────────────────────────────────────────┘

**Components:**

.. code-block:: text

    Sender Side (TX):
    - Network interface card (data input)
    - Protocol converter (Ethernet → serial)
    - LED or laser transmitter (850nm or 1310nm wavelength)
    - Fiber optic cable (single-mode or multi-mode)
    
    Receiver Side (RX):
    - Photodiode receiver (light detector)
    - Signal amplifier (low-noise amplifier)
    - Protocol converter (serial → Ethernet)
    - Network interface card (data output)

**B) Electrical Data Diode (Less Common):**

::

    ┌─────────────────────────────────────────────────────────────┐
    │                  ELECTRICAL DATA DIODE                      │
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │                                                             │
    │  ┌────────────┐         ┌────────┐         ┌─────────────┐│
    │  │  Sender    │         │ Copper │         │  Receiver   ││
    │  │  Hardware  │         │ Wire   │         │  Hardware   ││
    │  │            │         │        │         │             ││
    │  │ ┌────────┐ │         │        │         │ ┌─────────┐ ││
    │  │ │  TX    │ │ Voltage │  ──>   │ Voltage │ │   RX    │ ││
    │  │ │ Driver │ │ ──────> │ ──────>│ ──────> │ │ (Input  │ ││
    │  │ │        │ │         │        │         │ │  only)  │ ││
    │  │ └────────┘ │         │        │         │ └─────────┘ ││
    │  │            │         │        │         │             ││
    │  │ Receive    │         │ TX wire│         │ Transmit    ││
    │  │ pins       │         │ only   │         │ pins        ││
    │  │ PHYSICALLY │         │ (RX    │         │ PHYSICALLY  ││
    │  │ CUT ✂️     │         │ cut)   │         │ CUT ✂️      ││
    │  └────────────┘         └────────┘         └─────────────┘│
    │                                                             │
    │  Why it works:                                              │
    │  - TX pins physically disconnected on receiver side         │
    │  - RX pins physically disconnected on sender side           │
    │  - No electrical path for reverse flow                      │
    └─────────────────────────────────────────────────────────────┘

**Comparison:**

+------------------+----------------------------+----------------------------+
| **Aspect**       | **Optical Diode**          | **Electrical Diode**       |
+==================+============================+============================+
| **Medium**       | Fiber optic cable          | Copper wire                |
+------------------+----------------------------+----------------------------+
| **Distance**     | 2 km (multi-mode)          | 100 meters                 |
|                  | 100 km (single-mode)       |                            |
+------------------+----------------------------+----------------------------+
| **Security**     | Higher (EMI immune)        | Lower (EMI vulnerable)     |
+------------------+----------------------------+----------------------------+
| **Cost**         | Higher ($5K-$20K)          | Lower ($1K-$5K)            |
+------------------+----------------------------+----------------------------+
| **Certification**| EAL7+ achievable           | EAL6 typical               |
+------------------+----------------------------+----------------------------+
| **Aviation**     | Preferred (ACD isolation)  | Rare (cost-sensitive)      |
+------------------+----------------------------+----------------------------+

**1.3 Protocol Handling**
-------------------------

**Problem: TCP Requires Bidirectional Communication**

.. code-block:: text

    TCP Handshake (Bidirectional):
    
    Client                           Server
      │                                │
      │───── SYN ────────────────────> │
      │ <──── SYN-ACK ───────────────  │
      │───── ACK ────────────────────> │
      │                                │
      └─── CANNOT work with data diode (needs ACK back)
    
    Solution: Use UDP or Custom Protocol (Unidirectional)

**Data Diode Protocol Options:**

.. code-block:: text

    1. UDP (User Datagram Protocol):
       - No acknowledgments required
       - Fire-and-forget
       - Add FEC (Forward Error Correction) for reliability
    
    2. Multicast:
       - One-to-many transmission
       - Ideal for sensor data broadcast
       - No return path needed
    
    3. Custom Reliable UDP:
       - Add sequence numbers
       - Add CRC (Cyclic Redundancy Check)
       - Receiver reconstructs data (best-effort)

**Example: Reliable UDP for Data Diode:**

.. code-block:: python

    # data_diode_protocol.py
    
    import struct
    import zlib
    
    class DataDiodeProtocol:
        """
        Custom protocol for unidirectional data transfer
        Per ARINC 811: Reliable delivery without ACKs
        """
        
        def __init__(self):
            self.sequence_number = 0
        
        def create_packet(self, data):
            """
            Packet Format (32 bytes header + payload):
            
            ┌────────────┬────────────┬────────────┬────────────────────┐
            │ Magic      │ Sequence   │ CRC-32     │ Payload            │
            │ (4 bytes)  │ (4 bytes)  │ (4 bytes)  │ (variable)         │
            └────────────┴────────────┴────────────┴────────────────────┘
            
            Magic: 0xDEADBEEF (data diode signature)
            Sequence: Incrementing counter (detect gaps)
            CRC-32: Error detection
            Payload: Actual data
            """
            
            magic = 0xDEADBEEF
            sequence = self.sequence_number
            crc = zlib.crc32(data)
            
            header = struct.pack('!III', magic, sequence, crc)
            packet = header + data
            
            self.sequence_number += 1
            return packet
        
        def parse_packet(self, packet):
            """
            Receiver side: Parse and validate packet
            """
            
            # Extract header
            magic, sequence, crc = struct.unpack('!III', packet[:12])
            payload = packet[12:]
            
            # Validate magic number
            if magic != 0xDEADBEEF:
                raise ValueError("Invalid magic number")
            
            # Validate CRC
            if zlib.crc32(payload) != crc:
                raise ValueError(f"CRC mismatch (expected {crc})")
            
            # Check for sequence gaps (packet loss)
            if hasattr(self, 'last_sequence'):
                gap = sequence - self.last_sequence - 1
                if gap > 0:
                    print(f"⚠️ WARNING: {gap} packets lost (seq {self.last_sequence + 1} to {sequence - 1})")
            
            self.last_sequence = sequence
            
            return {
                'sequence': sequence,
                'data': payload
            }

**Forward Error Correction (FEC):**

.. code-block:: python

    # fec_example.py
    
    def apply_fec(data, redundancy=0.25):
        """
        Add redundancy for error correction (no ACKs possible)
        
        Example: 25% redundancy (4:1 ratio)
        - Original: 1000 bytes
        - With FEC: 1250 bytes (250 bytes parity)
        - Can recover from 250 bytes corruption
        """
        
        # Simple parity-based FEC (real: use Reed-Solomon)
        block_size = 4
        parity_data = bytearray()
        
        for i in range(0, len(data), block_size):
            block = data[i:i+block_size]
            parity = 0
            for byte in block:
                parity ^= byte  # XOR for simple parity
            parity_data.append(parity)
        
        return data + bytes(parity_data)

════════════════════════════════════════════════════════════════════

📖 **2. COMMON CRITERIA EAL7+ CERTIFICATION**
═════════════════════════════════════════════

**2.1 Evaluation Assurance Levels**
-----------------------------------

**Common Criteria Hierarchy:**

+-------+---------------------------+----------------------------------+
| EAL   | Assurance Level           | Description                      |
+=======+===========================+==================================+
| EAL1  | Functionally tested       | Basic testing                    |
+-------+---------------------------+----------------------------------+
| EAL2  | Structurally tested       | Developer testing + review       |
+-------+---------------------------+----------------------------------+
| EAL3  | Methodically tested       | Moderate security                |
+-------+---------------------------+----------------------------------+
| EAL4  | Methodically designed     | Commercial-grade (most products) |
+-------+---------------------------+----------------------------------+
| EAL5  | Semi-formally designed    | High security (government)       |
+-------+---------------------------+----------------------------------+
| EAL6  | Semi-formally verified    | Very high security               |
+-------+---------------------------+----------------------------------+
| **EAL7** | **Formally verified**  | **Highest assurance (aviation)** |
+-------+---------------------------+----------------------------------+

**EAL7+ Requirements for Data Diodes:**

.. code-block:: text

    1. Formal Security Policy Model:
       - Mathematical proof of unidirectional flow
       - Finite state machine (FSM) model
       - No covert channels (timing, power, EM)
    
    2. Formal Functional Specification:
       - Precise definition of all inputs/outputs
       - Formal methods (Z notation, B-Method)
       - Automated theorem proving (Coq, Isabelle)
    
    3. High-Level Design:
       - Hardware architecture specification
       - Component interaction diagrams
       - Security-critical paths identified
    
    4. Low-Level Design:
       - Circuit schematics (verified)
       - PCB layout (tamper-evident)
       - Firmware source code (formal verification)
    
    5. Implementation:
       - Hardware security (tamper-evident enclosures)
       - Secure boot (signed firmware)
       - Side-channel resistance (constant-time operations)
    
    6. Testing:
       - Penetration testing (red team)
       - Covert channel analysis (timing, power, EM)
       - Physical tamper testing
       - Electromagnetic interference (EMI) testing
    
    7. Vulnerability Assessment:
       - Independent security evaluation
       - Red team adversarial testing
       - Long-term monitoring (no 0-days)

**2.2 Formal Verification Example**
-----------------------------------

**Mathematical Proof of Unidirectionality:**

.. code-block:: text

    Theorem: Data Diode Unidirectionality
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    System: Data Diode (TX, Fiber, RX)
    
    Given:
    - TX = Transmitter hardware (LED/Laser)
    - RX = Receiver hardware (Photodiode)
    - Fiber = Optical fiber cable
    
    Properties:
    1. TX can only emit light (no light detection capability)
    2. RX can only detect light (no light emission capability)
    3. Fiber is unidirectional (light travels one way)
    
    Proof:
    ━━━━━
    
    Step 1: TX → RX path (Forward)
    - TX emits light (photons) → Fiber → RX detects light
    - ✅ Data flow possible (by design)
    
    Step 2: RX → TX path (Backward)
    - For data to flow RX → TX, RX must emit light
    - RX has no light source (only photodiode)
    - Photodiodes CANNOT emit light (physically impossible)
    - ∴ RX → TX path is IMPOSSIBLE
    
    Step 3: Covert Channels
    - Timing channel: RX cannot affect TX timing (no feedback)
    - Power channel: TX and RX on separate power supplies
    - EM channel: Fiber is EM-immune (optical, not electrical)
    - ∴ No covert channels exist
    
    Conclusion:
    ━━━━━━━━━
    ∀ data ∈ Data, ∀ time ∈ Time:
        data flows (RX → TX) = FALSE (provably secure)
    
    Q.E.D. □

**2.3 Covert Channel Analysis**
-------------------------------

**Covert Channels to Prevent:**

+-------------------+----------------------------------+----------------------------+
| **Channel Type**  | **Attack Vector**                | **Mitigation**             |
+===================+==================================+============================+
| **Timing**        | Vary data rate to encode signal  | Constant-rate transmission |
+-------------------+----------------------------------+----------------------------+
| **Power**         | Modulate power consumption       | Separate power supplies    |
+-------------------+----------------------------------+----------------------------+
| **EM Radiation**  | Electromagnetic side-channel     | Shielded enclosures (TEMPEST) |
+-------------------+----------------------------------+----------------------------+
| **Optical**       | Reflections in fiber             | Index-matched termination  |
+-------------------+----------------------------------+----------------------------+
| **Acoustic**      | Ultrasonic signaling             | Acoustic dampening         |
+-------------------+----------------------------------+----------------------------+

**Constant-Rate Transmission (Timing Channel Prevention):**

.. code-block:: python

    # constant_rate_transmission.py
    
    import time
    
    def constant_rate_transmit(data_queue, rate_bps=1_000_000):
        """
        Transmit data at constant rate (prevent timing channel)
        
        Rate: 1 Mbps (constant, regardless of data availability)
        If no data: Send null frames (padding)
        """
        
        frame_size = 1500  # bytes (Ethernet MTU)
        interval = frame_size * 8 / rate_bps  # seconds per frame
        
        while True:
            start_time = time.time()
            
            if not data_queue.empty():
                # Real data available
                frame = data_queue.get()
            else:
                # No data: Send null frame (padding)
                frame = b'\x00' * frame_size
            
            # Transmit frame (via data diode)
            transmit_frame(frame)
            
            # Wait to maintain constant rate
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)
            
            # Result: Attacker cannot infer data availability from timing

════════════════════════════════════════════════════════════════════

📖 **3. AVIATION IMPLEMENTATION**
═════════════════════════════════

**3.1 ACD → AISD Use Case**
---------------------------

**Typical Deployment:**

::

    ┌───────────────────────────────────────────────────────────────┐
    │              AIRCRAFT CONTROL DOMAIN (ACD)                    │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │  Flight-critical systems (DO-178C DAL A)                      │
    │                                                               │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
    │  │ Flight      │  │ Navigation  │  │ Air Data    │          │
    │  │ Control     │  │ (ADIRS)     │  │ Computer    │          │
    │  │ Computer    │  │             │  │             │          │
    │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
    │         │                │                │                  │
    │         └────────────────┴────────────────┘                  │
    │                          │                                   │
    │                   ARINC 429 Bus                              │
    │                          │                                   │
    │                   ┌──────▼──────┐                            │
    │                   │   Gateway   │                            │
    │                   │  (Read-only)│                            │
    │                   └──────┬──────┘                            │
    └───────────────────────────┼───────────────────────────────────┘
                                │
                                ↓ (One-way only)
                    ┌───────────────────────┐
                    │    DATA DIODE         │
                    │  (Optical, EAL7+)     │
                    │                       │
                    │  TX ──> Fiber ──> RX  │
                    │                       │
                    │  NO RETURN PATH ❌    │
                    └───────────┬───────────┘
                                │
                                ↓
    ┌───────────────────────────┼───────────────────────────────────┐
    │              AIRLINE INFORMATION SERVICES (AISD)              │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │  Crew & operational systems (DO-326A SAL 2)                   │
    │                                                               │
    │                   ┌──────▲──────┐                            │
    │                   │  Receiver   │                            │
    │                   │  Hardware   │                            │
    │                   └──────┬──────┘                            │
    │                          │                                   │
    │         ┌────────────────┴────────────────┐                  │
    │         │                                 │                  │
    │  ┌──────▼──────┐                   ┌──────▼──────┐          │
    │  │ Electronic  │                   │ Maintenance │          │
    │  │ Flight Bag  │                   │ Computer    │          │
    │  │ (Moving map)│                   │ (Fault logs)│          │
    │  └─────────────┘                   └─────────────┘          │
    └───────────────────────────────────────────────────────────────┘

**Data Flow Example:**

.. code-block:: python

    # acd_to_aisd_data_flow.py
    
    class ACDGateway:
        """
        ACD side: Read sensor data from ARINC 429 bus
        Transmit via data diode to AISD
        """
        
        def __init__(self, diode_interface):
            self.diode = diode_interface
            self.arinc429_bus = ARINC429Bus()
        
        def collect_flight_data(self):
            """
            Collect data from ACD systems (every 100ms)
            """
            
            data = {
                # Air Data Computer (ADC)
                'altitude': self.arinc429_bus.read_label(0o203),  # Barometric altitude
                'airspeed': self.arinc429_bus.read_label(0o206),  # Indicated airspeed
                'mach': self.arinc429_bus.read_label(0o207),      # Mach number
                
                # ADIRS (Navigation)
                'latitude': self.arinc429_bus.read_label(0o310),  # Latitude
                'longitude': self.arinc429_bus.read_label(0o311), # Longitude
                'heading': self.arinc429_bus.read_label(0o320),   # True heading
                
                # Flight Control Computer (FCC)
                'pitch': self.arinc429_bus.read_label(0o324),     # Pitch angle
                'roll': self.arinc429_bus.read_label(0o325),      # Roll angle
                
                # FADEC (Engine)
                'n1_left': self.arinc429_bus.read_label(0o361),   # N1 (left engine)
                'n1_right': self.arinc429_bus.read_label(0o362),  # N1 (right engine)
            }
            
            return data
        
        def transmit_via_diode(self, data):
            """
            Send data through data diode (one-way only)
            """
            
            # Serialize data (JSON or binary format)
            payload = serialize_flight_data(data)
            
            # Add FEC (25% redundancy for error correction)
            payload_with_fec = apply_fec(payload, redundancy=0.25)
            
            # Create packet (custom protocol, no ACKs)
            packet = self.diode.create_packet(payload_with_fec)
            
            # Transmit (UDP over optical fiber)
            self.diode.send(packet)
            
            # Note: No confirmation, no retry (fire-and-forget)

**3.2 Data Sanitization**
-------------------------

**Security Consideration: Precision Reduction**

.. code-block:: python

    # data_sanitization_acd_to_aisd.py
    
    def sanitize_for_aisd(raw_acd_data):
        """
        Sanitize ACD data before sending to AISD
        
        Reason:
        - ACD has precise data (±1 meter GPS, ±0.1 knot airspeed)
        - AISD does NOT need this precision
        - Reduce precision to prevent information leakage
        """
        
        sanitized = {
            # GPS: Reduce precision to ±10 km (1 decimal place)
            'latitude': round(raw_acd_data['latitude'], 1),
            'longitude': round(raw_acd_data['longitude'], 1),
            
            # Altitude: Round to nearest 100 ft
            'altitude': round(raw_acd_data['altitude'], -2),
            
            # Airspeed: Round to nearest 10 knots
            'airspeed': round(raw_acd_data['airspeed'], -1),
            
            # Heading: Round to nearest 10°
            'heading': round(raw_acd_data['heading'], -1),
            
            # DO NOT send:
            # - Precise control surface positions (security risk)
            # - Autopilot modes (operational security)
            # - Engine thrust settings (competitive intelligence)
        }
        
        return sanitized

**3.3 Installation & Verification**
-----------------------------------

**Installation Procedure:**

.. code-block:: bash

    #!/bin/bash
    # data_diode_installation.sh
    
    echo "📦 Data Diode Installation (ACD → AISD)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Step 1: Physical installation
    echo "Step 1: Install hardware"
    echo "  - Mount TX unit in avionics bay (ACD side)"
    echo "  - Mount RX unit in crew compartment (AISD side)"
    echo "  - Run fiber optic cable (single-mode, 9/125 μm)"
    echo "  - Apply tamper-evident seals"
    
    # Step 2: Power connection
    echo "Step 2: Connect power (separate supplies)"
    echo "  - TX: 28V DC from ACD power bus"
    echo "  - RX: 28V DC from AISD power bus"
    echo "  - Verify isolation (no common ground)"
    
    # Step 3: Network configuration
    echo "Step 3: Configure network"
    echo "  - TX IP: 10.10.1.100 (ACD gateway)"
    echo "  - RX IP: 10.20.1.100 (AISD receiver)"
    echo "  - Protocol: UDP (no TCP)"
    echo "  - Rate: 1 Mbps (constant)"
    
    # Step 4: Verification tests
    echo "Step 4: Verification"
    
    # Test 1: Forward path (should work)
    echo "  Test 1: Forward path (ACD → AISD)"
    ping -c 5 10.20.1.100 && echo "  ✅ Forward path OK" || echo "  ❌ Forward path FAILED"
    
    # Test 2: Reverse path (should FAIL)
    echo "  Test 2: Reverse path (AISD → ACD)"
    timeout 5 ping -c 5 10.10.1.100 && echo "  ❌ SECURITY VIOLATION: Reverse path exists!" || echo "  ✅ Reverse path blocked (expected)"
    
    # Test 3: Port scan from AISD (should timeout)
    echo "  Test 3: Port scan from AISD"
    timeout 10 nmap -p- 10.10.1.100 && echo "  ❌ SECURITY VIOLATION: Ports reachable!" || echo "  ✅ Ports unreachable (expected)"
    
    # Test 4: Data integrity
    echo "  Test 4: Data integrity (FEC)"
    ./test_fec.py && echo "  ✅ FEC working" || echo "  ❌ FEC failed"
    
    # Step 5: Documentation
    echo "Step 5: Generate certificate"
    cat <<EOF > /tmp/data_diode_cert.txt
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    DATA DIODE INSTALLATION CERTIFICATE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Aircraft: N12345
    Date: $(date)
    
    Hardware:
    - Manufacturer: Owl Cyber Defense (OWL-DDE-10G)
    - Certification: EAL7+ (Common Criteria)
    - Serial Number: OWL-2026-001234
    
    Installation:
    - TX Location: Avionics bay, rack 3, slot 5
    - RX Location: Crew compartment, overhead panel
    - Fiber Type: Single-mode, 9/125 μm, 50 meters
    
    Verification:
    - Forward path: ✅ PASS
    - Reverse path: ✅ BLOCKED (expected)
    - Port scan: ✅ BLOCKED (expected)
    - Data integrity: ✅ PASS
    
    Installer: John Smith (AME #123456)
    Inspector: Jane Doe (FAA DER)
    Signature: ________________________
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    EOF
    
    cat /tmp/data_diode_cert.txt
    
    echo "✅ Installation complete"

════════════════════════════════════════════════════════════════════

📖 **4. TIMING CHANNEL PREVENTION**
═══════════════════════════════════

**4.1 Timing Channel Threat**
-----------------------------

**What is a Timing Channel?**

::

    Scenario: Attacker on AISD wants to extract data from ACD
    
    Normal Attack: ❌ Cannot send packets (data diode blocks)
    
    Timing Attack: ⚠️ Try to modulate TIMING of ACD transmissions
    
    ┌─────────────────────────────────────────────────────────────┐
    │  ACD (Compromised software):                                │
    │                                                             │
    │  if secret_bit == 1:                                        │
    │      send_packet_now()        # Fast timing                 │
    │  else:                                                      │
    │      sleep(10ms)                                            │
    │      send_packet_now()        # Slow timing                 │
    │                                                             │
    │  Result: AISD can decode secret by measuring timing        │
    └─────────────────────────────────────────────────────────────┘
    
    Detection on AISD:
    - Packet arrives at T=100ms → Bit = 1
    - Packet arrives at T=110ms → Bit = 0
    
    Over time: Exfiltrate data via timing (covert channel)

**4.2 Constant-Rate Transmission**
----------------------------------

**Solution: Always Send at Fixed Rate**

.. code-block:: c

    // constant_rate_tx.c
    
    #include <stdint.h>
    #include <time.h>
    
    #define FRAME_SIZE 1500          // bytes
    #define RATE_BPS 1000000         // 1 Mbps
    #define INTERVAL_NS (FRAME_SIZE * 8 * 1000000000ULL / RATE_BPS)
    
    void constant_rate_transmitter(void) {
        uint8_t frame[FRAME_SIZE];
        struct timespec start, now, sleep_time;
        uint64_t next_tx_time_ns = 0;
        
        while (1) {
            // Get current time
            clock_gettime(CLOCK_MONOTONIC, &start);
            
            // Check if real data available
            if (has_real_data()) {
                // Send real data
                read_real_data(frame, FRAME_SIZE);
            } else {
                // Send null frame (padding)
                memset(frame, 0x00, FRAME_SIZE);
            }
            
            // Transmit frame
            transmit_frame(frame, FRAME_SIZE);
            
            // Calculate next transmission time (constant interval)
            next_tx_time_ns += INTERVAL_NS;
            
            // Sleep until next transmission time
            clock_gettime(CLOCK_MONOTONIC, &now);
            uint64_t now_ns = now.tv_sec * 1000000000ULL + now.tv_nsec;
            
            if (next_tx_time_ns > now_ns) {
                uint64_t sleep_ns = next_tx_time_ns - now_ns;
                sleep_time.tv_sec = sleep_ns / 1000000000ULL;
                sleep_time.tv_nsec = sleep_ns % 1000000000ULL;
                nanosleep(&sleep_time, NULL);
            }
        }
    }
    
    // Result: Attacker cannot infer data availability from timing

**4.3 Power Analysis Prevention**
---------------------------------

**Power Side-Channel:**

.. code-block:: text

    Problem: Power consumption varies with data content
    
    Transmitting '1' bits: Higher power (LED brightness)
    Transmitting '0' bits: Lower power (LED dimmer)
    
    Solution: Constant power consumption
    
    - Use differential signaling (always same # of transitions)
    - Add power noise (randomize baseline)
    - Separate power supplies (TX and RX)

**Differential Signaling Example:**

.. code-block:: text

    Manchester Encoding (constant power):
    
    Bit '0': Low → High transition (1 transition)
    Bit '1': High → Low transition (1 transition)
    
    Every bit has exactly 1 transition → constant power

════════════════════════════════════════════════════════════════════

📖 **5. VENDOR COMPARISON**
═══════════════════════════

**5.1 Commercial Data Diodes**
------------------------------

+-------------------+------------------+----------------+------------------+
| **Vendor**        | **Model**        | **Throughput** | **Certification**|
+===================+==================+================+==================+
| Owl Cyber Defense | OWL-DDE-10G      | 10 Gbps        | EAL7+            |
+-------------------+------------------+----------------+------------------+
| Waterfall         | WF-D-1000        | 1 Gbps         | EAL5+            |
+-------------------+------------------+----------------+------------------+
| BAE Systems       | BAE-DD-Mil       | 1 Gbps         | EAL7+ (Military) |
+-------------------+------------------+----------------+------------------+
| Advenica          | NetGap 1000      | 1 Gbps         | EAL4+            |
+-------------------+------------------+----------------+------------------+
| Fox DataDiode     | FOX-DD-100       | 100 Mbps       | EAL4+            |
+-------------------+------------------+----------------+------------------+

**Aviation-Grade Selection Criteria:**

.. code-block:: yaml

    # data_diode_requirements_aviation.yaml
    
    minimum_requirements:
      
      certification:
        - common_criteria: "EAL7+"
        - fips_140_2: "Level 3 or higher"
        - do_160g: "Environmental testing (aviation)"
        - do_178c: "Software (if firmware updatable)"
      
      performance:
        - throughput: "≥100 Mbps (sensor data)"
        - latency: "<10 ms (real-time display)"
        - packet_loss: "<0.01% (with FEC)"
      
      physical:
        - form_factor: "Avionics-grade (ARINC 600/700 chassis)"
        - temperature: "-55°C to +85°C (operating)"
        - vibration: "MIL-STD-810 (aircraft environment)"
        - emi_emc: "DO-160G Section 21 (EM compatibility)"
      
      security:
        - covert_channels: "None (formally verified)"
        - tamper_evident: "Physical seals + alerts"
        - side_channel: "Resistant (timing, power, EM)"

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** Explain why a data diode is more secure than a firewall for protecting ACD.

**A1:**

- **Firewall:** Software-based → can be misconfigured or exploited (0-day)
- **Data Diode:** Hardware-based → physically impossible to send data backwards
  - Optical: Photodiode cannot emit light (only detect)
  - Electrical: Transmit pins physically cut
- **Formal verification:** Mathematical proof of unidirectionality (EAL7+)
- **Aviation:** ACD is DAL A (flight-critical) → requires absolute protection

────────────────────────────────────────────────────────────────────

**Q2:** What is a timing covert channel, and how do you prevent it in data diodes?

**A2:**

**Timing Covert Channel:**
- Attacker modulates TIMING of transmissions to encode data
- Example: Fast packet = bit 1, delayed packet = bit 0
- Receiver measures timing to decode secret

**Prevention:**
- **Constant-rate transmission:** Send frames at fixed intervals
- If no data: Send null frames (padding)
- Result: Attacker cannot infer data from timing
- Code: `nanosleep()` to maintain fixed interval

────────────────────────────────────────────────────────────────────

**Q3:** Design a data diode protocol for ACD → AISD with error detection.

**A3:**

.. code-block:: text

    Protocol: Reliable UDP (No ACKs)
    
    Packet Format:
    ┌────────────┬────────────┬────────────┬────────────────────┐
    │ Magic      │ Sequence   │ CRC-32     │ Payload + FEC      │
    │ (4 bytes)  │ (4 bytes)  │ (4 bytes)  │ (variable)         │
    └────────────┴────────────┴────────────┴────────────────────┘
    
    - Magic: 0xDEADBEEF (signature)
    - Sequence: Detect packet loss (gaps in sequence)
    - CRC-32: Detect corruption
    - FEC: Reed-Solomon (25% redundancy) for error correction
    
    Receiver:
    1. Validate magic number
    2. Check CRC (drop if mismatch)
    3. Detect gaps (log warnings, continue)
    4. Apply FEC to recover corrupted data

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Select data diode vendor (EAL7+ certified)
- [ ] Install hardware (TX in ACD, RX in AISD)
- [ ] Run fiber optic cable (single-mode, 50m max for aircraft)
- [ ] Configure constant-rate transmission (timing channel prevention)
- [ ] Implement FEC (25% redundancy for reliability)
- [ ] Verify unidirectionality (reverse path test)
- [ ] Test covert channels (timing, power, EM)
- [ ] Document installation (certificate for FAA)
- [ ] Train maintenance crew (inspection procedures)
- [ ] Schedule periodic verification (annual penetration test)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Data diodes provide absolute isolation** → Physically impossible to send 
data backwards (mathematically provable)

2️⃣ **Optical diodes are preferred for aviation** → Fiber optic, EMI-immune, 
EAL7+ certification achievable

3️⃣ **Constant-rate transmission prevents timing channels** → Always send at 
fixed interval (null frames if no data)

4️⃣ **Use UDP with FEC instead of TCP** → TCP requires ACKs (bidirectional), 
UDP is unidirectional

5️⃣ **EAL7+ certification requires formal verification** → Mathematical proof 
of unidirectionality (theorem proving)

6️⃣ **Data sanitization is critical** → Reduce precision before sending ACD → 
AISD (security + operational)

7️⃣ **Installation requires verification** → Test reverse path (should fail), 
port scan (should timeout)

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **DATA DIODE TECHNOLOGY COMPLETE**
**Created:** January 14, 2026
**Coverage:** Optical/Electrical Diodes, EAL7+ Certification, ACD→AISD Implementation,
Timing Channel Prevention, Protocol Design, Installation & Verification

════════════════════════════════════════════════════════════════════
