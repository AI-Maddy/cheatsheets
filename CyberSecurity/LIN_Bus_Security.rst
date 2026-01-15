====================================================================
LIN Bus Security - Low-Cost In-Vehicle Network
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 17987 (LIN 2.x), ISO 21434, SAE J2602

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**LIN Bus Essentials:**

+--------------------+-----------------------------------------------------+
| **Parameter**      | **Value**                                           |
+====================+=====================================================+
| **Data Rate**      | 1-20 kbps (typically 19.2 kbps)                     |
+--------------------+-----------------------------------------------------+
| **Topology**       | Single-wire bus (plus ground)                       |
+--------------------+-----------------------------------------------------+
| **Master/Slave**   | 1 Master, up to 16 Slaves                           |
+--------------------+-----------------------------------------------------+
| **Cost**           | ~$0.50 per node (very low cost)                     |
+--------------------+-----------------------------------------------------+
| **Applications**   | Windows, mirrors, seats, HVAC, lighting            |
+--------------------+-----------------------------------------------------+
| **Security**       | ⚠️ **No native authentication/encryption**          |
+--------------------+-----------------------------------------------------+

**LIN Frame Structure:**

.. code-block:: text

    ┌──────────────────────────────────────────────────────┐
    │ LIN Frame (Master Header + Slave Response)          │
    ├──────────────────────────────────────────────────────┤
    │ Break (13+ bits)        │ ← Synchronization          │
    │ Sync Byte (0x55)        │ ← Baud rate calibration    │
    │ Protected ID (8 bits)   │ ← Frame ID + parity        │
    ├──────────────────────────────────────────────────────┤
    │ Data Bytes (0-8 bytes)  │ ← Payload                  │
    │ Checksum (1 byte)       │ ← Error detection          │
    └──────────────────────────────────────────────────────┘

**Security Status:**

- ❌ **No authentication**: Any node can respond to frame ID
- ❌ **No encryption**: Plaintext data
- ✅ **Checksum (8-bit)**: Detects errors, NOT tampering
- ❌ **Master-slave vulnerability**: Compromise master → control all slaves
- ❌ **Single-wire**: Easy to tap (physical access)

**Threat Model:**

1. ⚠️ **Master impersonation**: Fake master node controls slaves
2. ⚠️ **Frame injection**: Send malicious commands (e.g., open all windows)
3. ⚠️ **Eavesdropping**: Capture plaintext commands
4. ⚠️ **Diagnostic manipulation**: UDS over LIN (unauthorized access)
5. ⚠️ **Gateway attack**: LIN gateway to CAN (lateral movement)

**Key Defense Strategies:**

- ✅ **Gateway filtering**: Firewall between LIN and CAN/Ethernet
- ✅ **Message authentication**: Add HMAC to payload
- ✅ **Physical security**: Limit access to LIN bus wiring
- ✅ **Anomaly detection**: Monitor for unexpected frame IDs
- ✅ **Secure boot**: Authenticate LIN master firmware

Introduction to LIN Bus
========================

**LIN (Local Interconnect Network)** is a low-cost, single-wire serial bus for
non-critical automotive functions.

**Why LIN?**

CAN bus overkill for simple actuators:

- Window motors: Just need "up" or "down" commands
- Seat adjustment: Simple position control
- Mirror adjustment: Two motors (horizontal, vertical)
- HVAC: Fan speed, temperature setpoint

**LIN Advantages:**

- **Low cost**: ~$0.50 per node (vs. $2-5 for CAN node)
- **Simple**: Single-wire (vs. twisted pair for CAN)
- **Low bandwidth**: Sufficient for simple sensors/actuators
- **Deterministic**: Master-scheduled (no bus arbitration)

**LIN Disadvantages (Security Perspective):**

- **No authentication**: Any node can send frames
- **No encryption**: Plaintext data
- **Master-centric**: Compromise master → control all slaves
- **Physical vulnerability**: Single-wire easy to tap

**Typical Deployment:**

.. code-block:: text

    CAN Bus (High-Speed, 500 kbps)
         ↓
    ┌─────────────────────────┐
    │ LIN Gateway (Master ECU)│
    │  - Converts CAN ↔ LIN   │
    │  - Schedules LIN frames │
    └─────────────────────────┘
         ↓
    LIN Bus (19.2 kbps, Single Wire)
         ├─ Door Module (Slave 1): Window, lock, mirror
         ├─ Seat Module (Slave 2): Position, heating
         ├─ HVAC Module (Slave 3): Fan, temperature
         └─ Lighting Module (Slave 4): Interior lights

LIN Protocol Architecture
==========================

Master-Slave Communication
---------------------------

**LIN is strictly master-slave:**

- **Master**: Initiates all communication (sends frame headers)
- **Slaves**: Respond only when addressed (provide data bytes)

**Communication Flow:**

.. code-block:: text

    Master                    Slave (ID=0x21)
      │                              │
      ├──► Frame Header (ID=0x21) ──►│  ← Master schedules frame
      │                              │
      │◄── Data Bytes (8 bytes) ────┤  ← Slave responds
      │◄── Checksum (1 byte) ───────┤

**Master Responsibilities:**

1. Generate Break field (sync signal)
2. Send Sync Byte (0x55) for baud rate calibration
3. Send Protected ID (frame identifier)
4. Schedule all frame transmissions (deterministic)

**Slave Responsibilities:**

1. Listen for frame header with matching ID
2. Provide data bytes when addressed
3. Compute and append checksum

LIN Frame Format (ISO 17987)
-----------------------------

**Frame Components:**

.. code-block:: text

    ┌────────────────────────────────────────┐
    │ 1. Break Field (13-16 bits low)       │  ← Synchronization
    ├────────────────────────────────────────┤
    │ 2. Sync Byte (0x55 = 01010101)        │  ← Baud rate calibration
    ├────────────────────────────────────────┤
    │ 3. Protected ID (8 bits)              │  ← 6-bit ID + 2-bit parity
    │    - ID[5:0]: Frame identifier        │
    │    - P0, P1: Parity bits              │
    ├────────────────────────────────────────┤
    │ 4. Data Bytes (0, 2, 4, or 8 bytes)   │  ← Payload
    ├────────────────────────────────────────┤
    │ 5. Checksum (8 bits)                  │  ← Error detection
    └────────────────────────────────────────┘

**Protected ID Calculation:**

.. code-block:: c

    // Compute protected ID with parity bits
    uint8_t compute_protected_id(uint8_t frame_id) {
        // Frame ID must be 0-63 (6 bits)
        frame_id &= 0x3F;
        
        // Parity P0 = ID0 ^ ID1 ^ ID2 ^ ID4
        uint8_t p0 = ((frame_id >> 0) & 1) ^
                     ((frame_id >> 1) & 1) ^
                     ((frame_id >> 2) & 1) ^
                     ((frame_id >> 4) & 1);
        
        // Parity P1 = ~(ID1 ^ ID3 ^ ID4 ^ ID5)
        uint8_t p1 = ~(((frame_id >> 1) & 1) ^
                       ((frame_id >> 3) & 1) ^
                       ((frame_id >> 4) & 1) ^
                       ((frame_id >> 5) & 1)) & 1;
        
        // Protected ID = ID[5:0] | P0 << 6 | P1 << 7
        return frame_id | (p0 << 6) | (p1 << 7);
    }

**Checksum Calculation:**

.. code-block:: c

    // LIN 2.x enhanced checksum (includes Protected ID)
    uint8_t compute_lin_checksum(uint8_t protected_id, const uint8_t *data, size_t len) {
        uint16_t sum = protected_id;  // Include Protected ID
        
        for (size_t i = 0; i < len; i++) {
            sum += data[i];
            if (sum > 0xFF) {
                sum = (sum & 0xFF) + 1;  // Carry
            }
        }
        
        return (uint8_t)(0xFF - (sum & 0xFF));  // Inverted sum
    }

**Schedule Table (Master):**

Master executes a fixed schedule:

.. code-block:: text

    Time (ms) │ Frame ID │ Sender │ Data Length │ Description
    ──────────┼──────────┼────────┼─────────────┼─────────────────
    0         │ 0x21     │ Slave1 │ 8 bytes     │ Window status
    20        │ 0x22     │ Slave2 │ 8 bytes     │ Seat position
    40        │ 0x23     │ Slave3 │ 4 bytes     │ HVAC status
    60        │ 0x24     │ Slave4 │ 2 bytes     │ Lighting status
    80        │ 0x3C     │ Master │ 8 bytes     │ Master command

LIN Security Vulnerabilities
=============================

Vulnerability 1: No Master Authentication
------------------------------------------

**Problem:**

LIN has **no mechanism to authenticate the master**. Any device that generates
valid LIN frames can act as master.

**Attack Scenario:**

Attacker injects rogue master device:

.. code-block:: text

    Legitimate Master                 Rogue Master (Attacker)
         │                                     │
         ├──► Frame ID=0x21 ───┐              │
         │                     │              │
         │                     └──── Collision! ───┐
         │                                     │   │
         │                                     ├───┘
         │                                     ├──► Frame ID=0x3D (malicious)

**Result:**

- Rogue master sends malicious commands (e.g., unlock doors, open windows)
- Slaves cannot distinguish legitimate vs. rogue master

**Real-World Impact:**

- **Car theft**: Rogue master unlocks doors, disables alarm
- **Privacy**: Capture seat position data (driver behavior profiling)

Vulnerability 2: Plaintext Communication
-----------------------------------------

**Problem:**

All LIN data is transmitted in **plaintext** (no encryption).

**Attack:**

Attacker taps LIN bus (single-wire, easy to access):

.. code-block:: python

    # Attacker captures LIN traffic
    captured_frames = [
        {'id': 0x21, 'data': b'\x00\x01\x00\x00\x00\x00\x00\x00'},  # Window open
        {'id': 0x22, 'data': b'\x00\x50\x00\x30\x00\x00\x00\x00'},  # Seat position
        {'id': 0x23, 'data': b'\x15\x00\x00\x00'},                  # HVAC: 21°C
    ]
    
    # Attacker learns:
    # - Frame ID 0x21 = window control
    # - Byte 1 = 0x01 means "window open"
    # - Can replay or modify commands

**Impact:**

- Reverse-engineer proprietary protocols
- Prepare targeted injection attacks
- Privacy violation (track driver behavior)

Vulnerability 3: Weak Checksum (Not Cryptographic)
---------------------------------------------------

**Problem:**

LIN checksum is 8-bit sum (inverted). It detects **accidental errors**, not
**intentional tampering**.

**Attack:**

.. code-block:: c

    // Attacker modifies data and recomputes checksum
    uint8_t original_data[] = {0x00, 0x01, 0x00, 0x00};  // Window open
    uint8_t checksum1 = compute_lin_checksum(0x21, original_data, 4);
    
    // Attacker changes to "window close"
    uint8_t malicious_data[] = {0x00, 0x00, 0x00, 0x00};  // Window close
    uint8_t checksum2 = compute_lin_checksum(0x21, malicious_data, 4);  // Valid!

**Defense:**

Replace 8-bit checksum with **HMAC-SHA256** (cryptographic MAC).

Vulnerability 4: Frame Injection
---------------------------------

**Attack:**

Attacker injects malicious LIN frames:

.. code-block:: c

    // Attacker sends "Unlock All Doors" command
    uint8_t protected_id = compute_protected_id(0x25);  // Door control frame
    uint8_t unlock_cmd[] = {0xFF, 0xFF, 0xFF, 0xFF};   // Unlock all
    uint8_t checksum = compute_lin_checksum(protected_id, unlock_cmd, 4);
    
    // Inject frame on LIN bus
    lin_send_break();
    lin_send_byte(0x55);              // Sync
    lin_send_byte(protected_id);      // Frame ID
    lin_send_bytes(unlock_cmd, 4);    // Data
    lin_send_byte(checksum);          // Checksum

**Result:**

- All doors unlock
- No authentication check performed

Vulnerability 5: Diagnostic Manipulation (UDS over LIN)
--------------------------------------------------------

**Problem:**

LIN supports **UDS (Unified Diagnostic Services)** for reprogramming and
diagnostics. Attacker can send UDS commands over LIN.

**Attack:**

.. code-block:: python

    # UDS Service 0x27: Security Access
    uds_request = b'\x27\x01'  # Request seed
    
    # Send over LIN frame ID 0x3C (diagnostic request)
    lin_send_frame(0x3C, uds_request)
    
    # ECU responds with seed
    seed = lin_receive_frame(0x3D)['data']  # Diagnostic response
    
    # Compute key (if algorithm known/weak)
    key = compute_uds_key(seed)
    
    # Send key to unlock diagnostic functions
    uds_unlock = b'\x27\x02' + key
    lin_send_frame(0x3C, uds_unlock)
    
    # Now attacker can:
    # - Flash new firmware (Service 0x34, 0x36)
    # - Read fault codes (Service 0x19)
    # - Control actuators (Service 0x31)

**Impact:**

- Firmware tampering
- Unauthorized diagnostics (privacy violation)
- Disable safety features

LIN Security Countermeasures
=============================

Countermeasure 1: Gateway Filtering
------------------------------------

**Approach:**

Place **security gateway** between LIN and CAN/Ethernet networks.

**Gateway Functions:**

1. **Whitelist**: Only allow authorized frame IDs to pass
2. **Rate limiting**: Prevent DoS via frame flooding
3. **Command validation**: Check data sanity before forwarding

**Architecture:**

.. code-block:: text

    CAN Bus (500 kbps)
         ↓
    ┌─────────────────────────────────────────┐
    │ Security Gateway                        │
    │  - Frame ID whitelist                   │
    │  - Payload validation                   │
    │  - Rate limiting (max 10 frames/sec)    │
    │  - Logging (forensics)                  │
    └─────────────────────────────────────────┘
         ↓
    LIN Bus (19.2 kbps)
         ├─ Door Module
         ├─ Seat Module
         └─ HVAC Module

**C Code: LIN Gateway with Filtering**

.. code-block:: c

    #include <stdint.h>
    #include <stdbool.h>
    #include <string.h>
    
    #define MAX_LIN_FRAME_ID 64
    
    typedef struct {
        bool allowed;
        uint8_t expected_length;
        bool (*validator)(const uint8_t *data, size_t len);
    } lin_frame_policy_t;
    
    // Whitelist of allowed LIN frames
    lin_frame_policy_t lin_whitelist[MAX_LIN_FRAME_ID] = {
        [0x21] = {.allowed = true, .expected_length = 8, .validator = validate_window_cmd},
        [0x22] = {.allowed = true, .expected_length = 8, .validator = validate_seat_cmd},
        [0x23] = {.allowed = true, .expected_length = 4, .validator = validate_hvac_cmd},
        [0x3C] = {.allowed = false},  // Diagnostic frame: BLOCKED
        // ... other frame IDs
    };
    
    // Validate window control command
    bool validate_window_cmd(const uint8_t *data, size_t len) {
        if (len != 8) return false;
        
        // Byte 0: Window ID (0x00-0x03 for 4 windows)
        if (data[0] > 0x03) return false;
        
        // Byte 1: Command (0x00=close, 0x01=open, 0x02=stop)
        if (data[1] > 0x02) return false;
        
        return true;
    }
    
    // Gateway: Forward CAN → LIN with security checks
    int gateway_can_to_lin(const can_frame_t *can_frame) {
        // Extract LIN frame ID from CAN payload
        uint8_t lin_frame_id = can_frame->data[0];
        
        // Check 1: Frame ID in whitelist?
        if (lin_frame_id >= MAX_LIN_FRAME_ID || !lin_whitelist[lin_frame_id].allowed) {
            printf("Gateway: Blocked LIN Frame ID 0x%02X (not in whitelist)\n", lin_frame_id);
            log_security_event("Blocked LIN frame", lin_frame_id);
            return -1;
        }
        
        // Check 2: Expected length?
        size_t data_len = can_frame->dlc - 1;
        if (data_len != lin_whitelist[lin_frame_id].expected_length) {
            printf("Gateway: Length mismatch for Frame 0x%02X (expected %u, got %zu)\n",
                   lin_frame_id, lin_whitelist[lin_frame_id].expected_length, data_len);
            return -1;
        }
        
        // Check 3: Custom validator
        if (lin_whitelist[lin_frame_id].validator != NULL) {
            if (!lin_whitelist[lin_frame_id].validator(&can_frame->data[1], data_len)) {
                printf("Gateway: Validation failed for Frame 0x%02X\n", lin_frame_id);
                return -1;
            }
        }
        
        // Forward to LIN bus
        lin_frame_t lin_frame = {
            .protected_id = compute_protected_id(lin_frame_id),
            .data_len = data_len
        };
        memcpy(lin_frame.data, &can_frame->data[1], data_len);
        lin_frame.checksum = compute_lin_checksum(lin_frame.protected_id, 
                                                   lin_frame.data, data_len);
        
        printf("Gateway: Forwarding Frame 0x%02X to LIN bus\n", lin_frame_id);
        return lin_send_frame(&lin_frame);
    }

**Benefits:**

- ✅ Prevents unauthorized frame IDs (e.g., diagnostic frames from CAN)
- ✅ Validates payload sanity (detect malformed commands)
- ✅ Centralized security policy (easier to update)

Countermeasure 2: Message Authentication (HMAC)
------------------------------------------------

**Approach:**

Add **HMAC-SHA256** authentication tag to LIN payload.

**Challenge:**

LIN has limited bandwidth (19.2 kbps) and payload (8 bytes). Full HMAC-SHA256
(32 bytes) doesn't fit.

**Solution: Truncated HMAC**

Use 4-byte truncated HMAC:

.. code-block:: text

    Original LIN Payload (8 bytes):
    ┌────────────────────────────────┐
    │ Window ID (1 byte)             │
    │ Command (1 byte)               │
    │ Position (2 bytes)             │
    │ Reserved (4 bytes)             │
    └────────────────────────────────┘
    
    Authenticated LIN Payload (8 bytes):
    ┌────────────────────────────────┐
    │ Window ID (1 byte)             │
    │ Command (1 byte)               │
    │ Position (2 bytes)             │
    │ Counter (2 bytes)              │ ← Freshness value
    │ HMAC Tag (2 bytes)             │ ← Truncated authentication
    └────────────────────────────────┘

**C Code: LIN Message Authentication**

.. code-block:: c

    #include <openssl/hmac.h>
    
    #define LIN_HMAC_LEN 2  // Truncated to 16 bits (security trade-off)
    
    // Compute truncated HMAC for LIN message
    int lin_compute_hmac(
        uint8_t frame_id,
        const uint8_t *data,
        size_t data_len,
        uint16_t counter,
        const uint8_t *key,      // 128-bit shared secret
        uint8_t *hmac_tag        // Output: 2 bytes
    ) {
        uint8_t full_hmac[32];
        unsigned int hmac_len;
        
        // Construct data to authenticate: frame_id || data || counter
        uint8_t auth_data[64];
        size_t offset = 0;
        
        auth_data[offset++] = frame_id;
        memcpy(auth_data + offset, data, data_len);
        offset += data_len;
        memcpy(auth_data + offset, &counter, sizeof(counter));
        offset += sizeof(counter);
        
        // Compute HMAC-SHA256
        HMAC(EVP_sha256(), key, 16, auth_data, offset, full_hmac, &hmac_len);
        
        // Truncate to 2 bytes (most significant)
        memcpy(hmac_tag, full_hmac, LIN_HMAC_LEN);
        
        return 0;
    }
    
    // Send authenticated LIN frame
    int lin_send_authenticated(
        uint8_t frame_id,
        const uint8_t *payload,
        size_t payload_len,
        uint16_t *counter,
        const uint8_t *shared_key
    ) {
        // Reserve 4 bytes for counter + HMAC
        if (payload_len > 4) {
            printf("ERROR: Payload too large (%zu bytes, max 4 for authenticated)\n", payload_len);
            return -1;
        }
        
        // Increment counter
        (*counter)++;
        
        // Construct authenticated payload
        uint8_t auth_payload[8];
        memcpy(auth_payload, payload, payload_len);
        memcpy(auth_payload + payload_len, counter, sizeof(*counter));
        
        // Compute HMAC
        uint8_t hmac_tag[LIN_HMAC_LEN];
        lin_compute_hmac(frame_id, payload, payload_len, *counter, shared_key, hmac_tag);
        
        // Append HMAC
        memcpy(auth_payload + payload_len + sizeof(*counter), hmac_tag, LIN_HMAC_LEN);
        
        // Send LIN frame
        uint8_t protected_id = compute_protected_id(frame_id);
        uint8_t checksum = compute_lin_checksum(protected_id, auth_payload, 
                                                 payload_len + 4);
        
        lin_send_break();
        lin_send_byte(0x55);
        lin_send_byte(protected_id);
        lin_send_bytes(auth_payload, payload_len + 4);
        lin_send_byte(checksum);
        
        return 0;
    }
    
    // Verify authenticated LIN frame
    bool lin_verify_authenticated(
        uint8_t frame_id,
        const uint8_t *received_payload,
        size_t total_len,
        uint16_t *last_counter,
        const uint8_t *shared_key
    ) {
        if (total_len < 4) return false;  // Minimum: counter + HMAC
        
        size_t data_len = total_len - 4;
        
        // Extract counter and HMAC
        uint16_t received_counter;
        uint8_t received_hmac[LIN_HMAC_LEN];
        memcpy(&received_counter, received_payload + data_len, sizeof(received_counter));
        memcpy(received_hmac, received_payload + data_len + 2, LIN_HMAC_LEN);
        
        // Check freshness (prevent replay)
        if (received_counter <= *last_counter) {
            printf("ALERT: Replay attack detected! Counter: %u (expected > %u)\n",
                   received_counter, *last_counter);
            return false;
        }
        
        // Compute expected HMAC
        uint8_t expected_hmac[LIN_HMAC_LEN];
        lin_compute_hmac(frame_id, received_payload, data_len, received_counter, 
                         shared_key, expected_hmac);
        
        // Compare HMACs
        if (memcmp(received_hmac, expected_hmac, LIN_HMAC_LEN) != 0) {
            printf("ALERT: Authentication failed! HMAC mismatch.\n");
            return false;
        }
        
        // Update counter
        *last_counter = received_counter;
        return true;
    }

**Trade-offs:**

- ✅ Prevents spoofing and modification
- ✅ Prevents replay attacks (counter)
- ❌ Reduced effective payload (4 bytes data, 4 bytes overhead)
- ❌ 2-byte HMAC is weak (2^16 = 65,536 forgery attempts possible)

**Better Alternative: 4-byte HMAC**

- Use 4-byte HMAC (more secure: 2^32 forgery difficulty)
- Reduce data payload to 2 bytes
- Acceptable for simple commands (e.g., window open/close)

Countermeasure 3: Physical Security
------------------------------------

**Problem:**

LIN is a single-wire bus, easy to tap with physical access.

**Mitigations:**

**1. Secure Wiring:**

- Route LIN wiring inside protected conduits (not exposed)
- Use tamper-evident seals on connectors

**2. Intrusion Detection:**

- Monitor LIN bus for unexpected voltage levels (indicates tap)
- Use current sensors to detect additional loads

**3. Secure Diagnostic Connector:**

- OBD-II port provides access to LIN via gateway
- Use **challenge-response authentication** before enabling LIN access

.. code-block:: python

    def obd_authenticate_lin_access(obd_client, ecu_public_key):
        """Authenticate before allowing LIN access via OBD-II"""
        
        # Generate random challenge
        challenge = os.urandom(32)
        
        # Send challenge to ECU
        obd_client.send_uds_request(0x27, 0x01, challenge)
        
        # ECU signs challenge with private key
        response = obd_client.receive_uds_response()
        signature = response['data']
        
        # Verify signature with ECU's public key
        try:
            ecu_public_key.verify(signature, challenge, padding.PSS(...), hashes.SHA256())
            print("Authentication successful. LIN access granted.")
            return True
        except:
            print("Authentication failed. LIN access DENIED.")
            return False

Countermeasure 4: Anomaly Detection (IDS)
------------------------------------------

**Approach:**

Monitor LIN bus for deviations from expected behavior.

**Python Code: LIN Intrusion Detection System**

.. code-block:: python

    import time
    from collections import defaultdict
    
    class LIN_IDS:
        def __init__(self):
            self.frame_baseline = {}  # Frame ID → expected timing
            self.frame_counts = defaultdict(int)
            self.alert_threshold = 10  # Alerts per minute
        
        def learn_baseline(self, frame_id, interval_ms):
            """Learn normal LIN traffic pattern"""
            self.frame_baseline[frame_id] = {
                'interval': interval_ms,
                'last_seen': None,
                'deviations': 0
            }
        
        def monitor_frame(self, frame_id, timestamp):
            """Detect anomalies in LIN traffic"""
            
            # Anomaly 1: Unexpected frame ID
            if frame_id not in self.frame_baseline:
                self.raise_alert(
                    severity='HIGH',
                    message=f"Unknown LIN Frame ID: 0x{frame_id:02X}"
                )
                return False
            
            baseline = self.frame_baseline[frame_id]
            
            # Anomaly 2: Timing deviation
            if baseline['last_seen'] is not None:
                actual_interval = (timestamp - baseline['last_seen']) * 1000  # ms
                expected_interval = baseline['interval']
                
                if abs(actual_interval - expected_interval) > 50:  # 50 ms tolerance
                    baseline['deviations'] += 1
                    if baseline['deviations'] > 3:
                        self.raise_alert(
                            severity='MEDIUM',
                            message=f"Timing anomaly: Frame 0x{frame_id:02X} " \
                                    f"(expected {expected_interval} ms, got {actual_interval:.1f} ms)"
                        )
            
            baseline['last_seen'] = timestamp
            
            # Anomaly 3: Rate limiting (DoS detection)
            self.frame_counts[frame_id] += 1
            if self.frame_counts[frame_id] > 60:  # > 60 frames/min abnormal
                self.raise_alert(
                    severity='CRITICAL',
                    message=f"DoS attack: Frame 0x{frame_id:02X} flooding " \
                            f"({self.frame_counts[frame_id]} frames/min)"
                )
                return False
            
            return True
        
        def raise_alert(self, severity, message):
            print(f"[{severity}] LIN IDS: {message}")
            # Log to SIEM, trigger incident response
    
    # Example usage
    if __name__ == "__main__":
        ids = LIN_IDS()
        
        # Learn baseline
        ids.learn_baseline(0x21, 20)  # Window status every 20 ms
        ids.learn_baseline(0x22, 50)  # Seat position every 50 ms
        
        # Simulate monitoring
        ids.monitor_frame(0x21, time.time())
        time.sleep(0.02)
        ids.monitor_frame(0x21, time.time())  # OK
        
        ids.monitor_frame(0xFF, time.time())  # Unknown frame → Alert

Exam Questions
==============

Question 1: LIN vs. CAN Security (Difficulty: Easy)
----------------------------------------------------

Compare the security of LIN and CAN bus for door lock control.

**Answer:**

+---------------------+-------------------------+-------------------------+
| Aspect              | LIN                     | CAN                     |
+=====================+=========================+=========================+
| Authentication      | ❌ None                 | ❌ None (native)        |
+---------------------+-------------------------+-------------------------+
| Encryption          | ❌ None                 | ❌ None (native)        |
+---------------------+-------------------------+-------------------------+
| Checksum            | 8-bit (weak)            | CRC-15 (stronger)       |
+---------------------+-------------------------+-------------------------+
| Topology            | Master-slave (single    | Multi-master (more      |
|                     | point of failure)       | resilient)              |
+---------------------+-------------------------+-------------------------+
| Physical Access     | Single-wire (easy tap)  | Twisted pair (harder)   |
+---------------------+-------------------------+-------------------------+
| Bandwidth           | 19.2 kbps (low)         | 500 kbps (high)         |
+---------------------+-------------------------+-------------------------+

**Recommendation for Door Lock:**

**CAN is more secure** due to:

1. **Higher bandwidth**: Can accommodate SecOC authentication overhead
2. **Twisted pair**: Harder to tap than single-wire LIN
3. **Multi-master**: No single point of failure

**However:**

For non-critical applications (interior lighting, mirror adjustment), LIN is
acceptable if protected by **security gateway**.

**Best Practice:**

- **Critical actuators (door locks, immobilizer)**: Use CAN with SecOC
- **Non-critical (windows, seats)**: LIN with gateway filtering

Question 2: Gateway Attack (Difficulty: Hard)
----------------------------------------------

An attacker compromises a LIN slave node (seat control module). Describe how
the attacker can use this to:

**a)** Attack other LIN nodes
**b)** Laterally move to the CAN network
**c)** Propose mitigations

**Answer:**

**a) Attack Other LIN Nodes:**

**Step 1: Impersonate Master**

Compromised slave can pretend to be master (no authentication):

.. code-block:: c

    // Compromised slave sends master frame headers
    void attack_other_lin_nodes() {
        // Send frame header for Door Module (Frame ID 0x25)
        lin_send_break();
        lin_send_byte(0x55);
        lin_send_byte(compute_protected_id(0x25));
        
        // Send malicious command (unlock all doors)
        uint8_t unlock_cmd[] = {0xFF, 0xFF, 0xFF, 0xFF};
        lin_send_bytes(unlock_cmd, 4);
        lin_send_byte(compute_lin_checksum(0x25, unlock_cmd, 4));
    }

**Result:**

- Door module receives command, unlocks doors
- No way to verify sender authenticity

**Step 2: DoS Attack**

- Flood LIN bus with frames (19.2 kbps capacity exhausted)
- Legitimate master cannot communicate

**b) Lateral Movement to CAN:**

**Attack Vector: LIN Gateway**

.. code-block:: text

    Compromised Seat Module (LIN Slave)
              ↓
    Sends crafted LIN frame to Gateway
              ↓
    ┌─────────────────────────────────┐
    │ LIN Gateway (potential vuln)    │
    │  - Buffer overflow in parser?   │
    │  - Command injection?           │
    └─────────────────────────────────┘
              ↓
    Gateway compromised → Full CAN access

**Example: Buffer Overflow in Gateway**

.. code-block:: c

    // Vulnerable gateway code
    void gateway_process_lin_frame(lin_frame_t *frame) {
        char buffer[8];  // Fixed size buffer
        
        // BUG: No bounds checking!
        memcpy(buffer, frame->data, frame->data_len);  // Overflow if data_len > 8
        
        // Process buffer...
    }
    
    // Attacker sends oversized LIN frame
    lin_frame_t attack_frame = {
        .protected_id = compute_protected_id(0x22),
        .data_len = 32,  // Exceeds buffer size!
        .data = "\x41\x41\x41\x41..."  // Shellcode
    };

**Result:**

- Gateway crashes or executes attacker code
- Attacker gains code execution on gateway
- Full access to CAN network

**c) Mitigations:**

**Mitigation 1: Input Validation (Gateway)**

.. code-block:: c

    void gateway_process_lin_frame_secure(lin_frame_t *frame) {
        // Check maximum length
        if (frame->data_len > 8) {
            log_security_event("Oversized LIN frame detected");
            return;  // Drop frame
        }
        
        // Whitelist frame IDs
        if (!is_allowed_frame_id(frame->protected_id)) {
            log_security_event("Unauthorized LIN frame ID");
            return;
        }
        
        // Safe processing
        char buffer[8];
        memcpy(buffer, frame->data, frame->data_len);
        // ...
    }

**Mitigation 2: Gateway Segmentation**

- Gateway should have **two isolated CPUs**:
  
  - CPU1: LIN interface (untrusted)
  - CPU2: CAN interface (trusted)
  - Communication via secure channel (authenticated messages)

**Mitigation 3: LIN Node Authentication**

- Use challenge-response to verify slave nodes on boot:

.. code-block:: python

    def authenticate_lin_slave(slave_id, expected_key):
        # Master sends challenge
        challenge = os.urandom(16)
        lin_send_frame(slave_id, challenge)
        
        # Slave computes HMAC
        response = lin_receive_frame(slave_id + 1)
        received_hmac = response['data']
        
        # Verify
        expected_hmac = hmac.new(expected_key, challenge, hashlib.sha256).digest()[:4]
        
        if received_hmac == expected_hmac:
            print(f"Slave {slave_id} authenticated successfully")
            return True
        else:
            print(f"Slave {slave_id} authentication FAILED")
            # Isolate slave (do not schedule its frames)
            return False

**Mitigation 4: Runtime Monitoring**

- Monitor gateway for anomalies:
  
  - Unexpected CAN frames after receiving LIN frame
  - High CPU usage (shellcode execution?)
  - Memory corruption (watchdog, MPU)

Question 3: Performance Impact (Difficulty: Medium)
----------------------------------------------------

A LIN network operates at 19.2 kbps with 10 ms frame interval. Each frame
contains 8 bytes of data.

**a)** Calculate the maximum bandwidth utilization.

**b)** If HMAC authentication adds 4 bytes overhead, will frames fit within
10 ms?

**Answer:**

**a) Maximum Bandwidth:**

**LIN Frame Structure:**

- Break: 13 bits
- Sync: 8 bits
- Protected ID: 8 bits
- Data: 8 bytes = 64 bits
- Checksum: 8 bits

**Total:** 13 + 8 + 8 + 64 + 8 = **101 bits**

**Transmission Time:**

- Bit rate: 19,200 bps
- Time per frame: 101 bits / 19,200 bps = **5.26 ms**

**Bandwidth Utilization:**

- Frame interval: 10 ms
- Utilization: 5.26 ms / 10 ms = **52.6%** ✅

**b) With HMAC (4 bytes overhead):**

**LIN Frame with Auth:**

- Data: 4 bytes (reduced payload)
- Counter: 2 bytes (freshness)
- HMAC: 2 bytes (truncated)
- Total payload: 8 bytes (same as before)

**Transmission Time:** Still **5.26 ms** ✅

**Answer:** Yes, fits within 10 ms (52.6% bandwidth).

**However:**

- Effective data payload reduced from 8 bytes to 4 bytes (50% overhead)
- May need to split commands across multiple frames

Question 4: Diagnostic Security (Difficulty: Hard)
---------------------------------------------------

A mechanic connects a diagnostic tool to the OBD-II port, which has access to
the LIN network via gateway. The tool sends a UDS request to reflash the seat
control module firmware.

**a)** Describe the attack surface.

**b)** Design a secure diagnostic protocol for LIN.

**Answer:**

**a) Attack Surface:**

**Step 1: OBD-II Access**

- OBD-II port is physically accessible (inside vehicle)
- No authentication required to connect

**Step 2: Gateway Access**

- Diagnostic tool sends CAN frames to gateway
- Gateway forwards UDS requests to LIN

**Step 3: UDS Security Access (Service 0x27)**

.. code-block:: text

    Tool → Gateway → LIN Master → Seat Module
    
    UDS Request (Service 0x27, Subfunction 0x01): Request Seed
    Seat Module → Master → Gateway → Tool
    
    UDS Response: Seed = 0x1234ABCD
    
    Tool computes Key = SeedToKey(Seed)  ← Weak algorithm?
    Tool → Gateway → Master → Seat Module
    
    UDS Request (Service 0x27, Subfunction 0x02): Send Key
    Seat Module → Master → Gateway → Tool
    
    UDS Response: Security Unlocked ✅

**Step 4: Flash Firmware (Service 0x34, 0x36)**

- Tool uploads malicious firmware
- Seat module accepts (authenticated via seed-key)

**Vulnerabilities:**

1. **Weak seed-key algorithm**: Attacker can brute-force or reverse-engineer
2. **No tool authentication**: Any tool with correct algorithm can access
3. **No firmware signature verification**: Seat module accepts unsigned firmware

**b) Secure Diagnostic Protocol:**

**Enhancement 1: Tool Authentication (Mutual TLS)**

.. code-block:: python

    def secure_diagnostic_session(obd_tool, ecu):
        # Step 1: Tool authenticates to ECU
        tool_cert = obd_tool.get_certificate()  # X.509 certificate
        ecu.verify_certificate(tool_cert, trusted_ca_list)
        
        # Step 2: ECU authenticates to Tool
        ecu_cert = ecu.get_certificate()
        obd_tool.verify_certificate(ecu_cert, trusted_ca_list)
        
        # Step 3: Establish encrypted channel (TLS)
        session_key = diffie_hellman_exchange(obd_tool, ecu)
        
        return session_key

**Enhancement 2: Firmware Signature Verification**

.. code-block:: c

    // ECU verifies firmware signature before flashing
    bool verify_firmware_signature(
        const uint8_t *firmware,
        size_t firmware_len,
        const uint8_t *signature,
        const uint8_t *oem_public_key
    ) {
        // Compute SHA-256 hash of firmware
        uint8_t hash[32];
        SHA256(firmware, firmware_len, hash);
        
        // Verify ECDSA P-256 signature
        EC_KEY *ec_key = parse_public_key(oem_public_key);
        ECDSA_SIG *sig = parse_signature(signature);
        
        int valid = ECDSA_do_verify(hash, 32, sig, ec_key);
        
        if (!valid) {
            printf("ERROR: Firmware signature invalid!\n");
            return false;
        }
        
        printf("Firmware signature verified. Flashing...\n");
        return true;
    }

**Enhancement 3: Secure Boot (ECU)**

- ECU verifies firmware signature on every boot
- If signature invalid → refuse to start, enter recovery mode

**Enhancement 4: Rate Limiting**

- Limit diagnostic requests (e.g., max 1 flash per day)
- Prevents brute-force attacks on seed-key

Conclusion
==========

LIN bus is a low-cost, simple network for non-critical automotive functions, but
**lacks native security**. Key vulnerabilities:

1. **No authentication**: Any device can act as master
2. **No encryption**: Plaintext data
3. **Weak checksum**: Not cryptographically secure
4. **Master-slave topology**: Single point of failure

**Security Enhancements:**

1. **Gateway filtering**: Whitelist frames, validate payloads
2. **Message authentication**: HMAC with rolling counters
3. **Physical security**: Secure wiring, tamper detection
4. **Intrusion detection**: Anomaly detection for LIN traffic
5. **Secure diagnostics**: Tool authentication, firmware signatures

**Standards Compliance:**

- ISO 17987: LIN protocol specification
- ISO 21434: Automotive cybersecurity engineering
- SAE J2602: LIN network protocol specification
- UN R155: Cybersecurity Management System (CSMS)

References
==========

- ISO 17987: Road Vehicles - Local Interconnect Network (LIN)
- ISO 21434: Road Vehicles - Cybersecurity Engineering
- SAE J2602: LIN Network Protocol Specification
- AUTOSAR: Specification of LIN Interface

**END OF DOCUMENT**
