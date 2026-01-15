====================================================================
FlexRay Security - Time-Triggered In-Vehicle Network
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ISO 17458, ISO 21434, FlexRay Specification v3.0.1

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**FlexRay Essentials:**

+--------------------+-----------------------------------------------------+
| **Parameter**      | **Value**                                           |
+====================+=====================================================+
| **Data Rate**      | 10 Mbps (per channel)                               |
+--------------------+-----------------------------------------------------+
| **Topology**       | Dual-channel (redundancy)                           |
+--------------------+-----------------------------------------------------+
| **Determinism**    | Time-Triggered (TDMA slots)                         |
+--------------------+-----------------------------------------------------+
| **Applications**   | X-by-wire (steer, brake), ADAS, powertrain          |
+--------------------+-----------------------------------------------------+
| **Security**       | ⚠️ **No native encryption/authentication**          |
+--------------------+-----------------------------------------------------+

**FlexRay Frame Structure:**

.. code-block:: text

    ┌────────────────────────────────────────────────────────┐
    │ FlexRay Frame (5 bytes header + 0-254 bytes payload)   │
    ├────────────────────────────────────────────────────────┤
    │ Header (5 bytes)                                       │
    │  - Frame ID (11 bits)                                  │
    │  - Payload length (7 bits)                             │
    │  - Header CRC (11 bits)                                │
    │  - Cycle count (6 bits)                                │
    ├────────────────────────────────────────────────────────┤
    │ Payload (0-254 bytes)                                  │
    ├────────────────────────────────────────────────────────┤
    │ CRC (24 bits)                                          │
    └────────────────────────────────────────────────────────┘

**Security Status:**

- ❌ **No message-level authentication** (anyone can send if synchronized)
- ❌ **No encryption** (plaintext payload)
- ✅ **CRC error detection** (detects corruption, not tampering)
- ✅ **Deterministic timing** (harder to inject messages)
- ✅ **Dual-channel redundancy** (fault tolerance)

**Threat Model:**

1. ⚠️ **Message injection**: Attacker sends malicious FlexRay frames
2. ⚠️ **Message modification**: Alter brake/steering commands in-flight
3. ⚠️ **Replay attacks**: Re-send previously captured frames
4. ⚠️ **DoS attacks**: Flood bus with high-priority frames
5. ⚠️ **Timing attacks**: Desynchronize FlexRay cluster

Introduction to FlexRay
========================

**FlexRay** is a high-speed, deterministic automotive bus designed for
safety-critical X-by-wire systems (steer-by-wire, brake-by-wire).

**Why FlexRay?**

Traditional CAN bus limitations:

- CAN: 1 Mbps max (insufficient for X-by-wire)
- CAN: Non-deterministic (arbitration delays)
- CAN: No redundancy (single point of failure)

**FlexRay Advantages:**

- **High bandwidth**: 10 Mbps (10x faster than CAN)
- **Deterministic**: Time-triggered TDMA (predictable latency)
- **Redundant**: Dual-channel (fault tolerance)
- **Flexible**: Supports event-triggered AND time-triggered

**Applications:**

- **Steer-by-wire**: Electronic steering (no mechanical linkage)
- **Brake-by-wire**: Electronic braking
- **Active suspension**: Real-time damping control
- **Powertrain**: Engine control, transmission
- **ADAS**: Sensor fusion, high-bandwidth camera data

**Deployment:**

- BMW 7-Series, X5, X6 (chassis dynamics)
- Audi A8 (active suspension)
- Mercedes S-Class (powertrain)

FlexRay Architecture
====================

Time-Triggered TDMA (Time Division Multiple Access)
----------------------------------------------------

**FlexRay Cycle:**

.. code-block:: text

    FlexRay Communication Cycle (5 ms typical)
    ┌─────────────────────────────────────────────────────────┐
    │ Static Segment      │ Dynamic Segment │ Symbol Window │
    │  (Time-Triggered)   │  (Event-Trig)   │  (Sync)       │
    ├─────────────────────────────────────────────────────────┤
    │ Slot 1 │ Slot 2 │...│ Slot N │ Mini   │ CAS/MTS       │
    │ ECU A  │ ECU B  │   │ ECU Z  │ Slots  │ Wakeup        │
    └─────────────────────────────────────────────────────────┘

**Static Segment (Deterministic):**

- Fixed time slots (TDMA)
- Each ECU assigned specific slot (e.g., Steering ECU → Slot 5)
- Guaranteed bandwidth and latency
- Used for safety-critical messages (brake, steering commands)

**Dynamic Segment (Flexible):**

- Mini-slots for event-triggered messages
- Lower priority than static segment
- Used for non-critical diagnostics, status messages

**Dual-Channel Topology:**

.. code-block:: text

    Channel A:  ECU1 ←→ ECU2 ←→ ECU3 ←→ ECU4
                 ↕      ↕      ↕      ↕
    Channel B:  ECU1 ←→ ECU2 ←→ ECU3 ←→ ECU4
    
    Redundancy: If Channel A fails, Channel B continues

FlexRay Frame Format (ISO 17458)
---------------------------------

**Header (5 bytes = 40 bits):**

.. code-block:: text

    ┌───────────────────────────────────────────────────┐
    │ Bit Field            │ Bits │ Description        │
    ├───────────────────────────────────────────────────┤
    │ Reserved             │   1  │ Must be 0          │
    │ Payload Preamble     │   1  │ 0=data, 1=NULL     │
    │ NULL Frame Indicator │   1  │ 0=valid, 1=null    │
    │ Sync Frame Indicator │   1  │ Sync bit           │
    │ Startup Frame Ind    │   1  │ Startup frame      │
    │ Frame ID             │  11  │ 1-2047             │
    │ Payload Length       │   7  │ 0-127 words        │
    │ Header CRC           │  11  │ CRC-11             │
    │ Cycle Count          │   6  │ 0-63 (wraps)       │
    └───────────────────────────────────────────────────┘

**Payload:**

- Length: 0-254 bytes (0-127 16-bit words)
- **Plaintext** (no encryption in FlexRay spec) ⚠️

**CRC (24 bits):**

- Polynomial: 0x5D6DCB (CRC-24)
- Covers header + payload
- **Detects errors, does NOT prevent tampering** ⚠️

FlexRay Security Vulnerabilities
=================================

Vulnerability 1: No Message Authentication
-------------------------------------------

**Problem:**

FlexRay has **no authentication mechanism**. Any ECU can send a frame in its
assigned time slot, even if compromised.

**Attack Scenario:**

.. code-block:: text

    Normal Operation:
    Slot 5: Steering ECU sends steering angle (45°)
    
    Attack:
    Slot 5: Compromised Steering ECU sends malicious angle (90°)
    
    Result: Vehicle steers sharply (crash potential)

**Why This Is Critical:**

- X-by-wire systems have **no mechanical fallback**
- Compromised steering/brake command = immediate safety impact
- No way for receiving ECU to verify sender authenticity

Vulnerability 2: No Encryption
-------------------------------

**Problem:**

FlexRay payload is **plaintext**. Attacker with physical access (CAN tap,
FlexRay tap) can read all messages.

**Attack Scenario:**

.. code-block:: python

    # Attacker captures FlexRay traffic
    captured_frame = {
        'frame_id': 0x105,  # Steering command
        'payload': b'\x00\x2D\x00\x00',  # Steering angle: 45°
        'crc': 0xABC123
    }
    
    # Attacker learns:
    # - Frame ID 0x105 = steering command
    # - Payload format (16-bit angle)
    # - Timing (every 5 ms in Slot 5)

**Impact:**

- Reverse-engineer proprietary protocols
- Prepare targeted attacks
- Clone ECU functionality

Vulnerability 3: CRC Is Not Cryptographic
------------------------------------------

**Problem:**

CRC-24 detects **accidental errors**, not **malicious tampering**.

**Attack:**

Attacker can modify payload AND recompute CRC:

.. code-block:: c

    // Original frame
    uint8_t original_payload[] = {0x00, 0x2D, 0x00, 0x00};  // 45°
    uint32_t original_crc = compute_crc24(original_payload, 4);
    
    // Attacker modifies
    uint8_t malicious_payload[] = {0x00, 0x5A, 0x00, 0x00};  // 90°
    uint32_t malicious_crc = compute_crc24(malicious_payload, 4);  // ← Valid!

**Defense:**

CRC should be replaced with **HMAC-SHA256** or **CMAC-AES** (authenticated MAC).

Vulnerability 4: Replay Attacks
--------------------------------

**Problem:**

FlexRay has no **freshness mechanism** (no timestamp, no nonce).

**Attack:**

.. code-block:: text

    Time 0 ms:  Steering ECU sends "Steer Left" (Frame ID 0x105)
    Time 5 ms:  Attacker captures frame
    Time 100 ms: Attacker replays "Steer Left" (out of context)
    
    Result: Vehicle steers left unexpectedly

**Mitigation:**

Add **rolling counter** or **timestamp** to payload:

.. code-block:: c

    typedef struct {
        uint16_t counter;       // Rolling counter (0-65535)
        uint16_t steering_angle;
        uint32_t timestamp;     // Microseconds since boot
    } steering_command_t;

Vulnerability 5: Bus-Off Attack (DoS)
--------------------------------------

**Problem:**

If malicious ECU sends frames outside its time slot, it can cause
**FlexRay cluster desynchronization** (bus-off state).

**Attack:**

.. code-block:: text

    Slot 5: Malicious ECU sends frame (correct)
    Slot 6: Malicious ECU sends frame again (WRONG! Not its slot)
    
    Result:
    - Other ECUs detect collision
    - Cluster loses synchronization
    - FlexRay bus shuts down (safety mode)

**Impact:**

- X-by-wire systems become inoperable
- Vehicle enters safe mode (limp home)
- Driver loses control (if no mechanical fallback)

FlexRay Security Countermeasures
=================================

Countermeasure 1: Message Authentication (SecOC)
-------------------------------------------------

**AUTOSAR SecOC** (Secure Onboard Communication) can be applied to FlexRay.

**Approach:**

Add **CMAC-AES-128** authentication tag to payload:

.. code-block:: text

    Original Payload (8 bytes):
    ┌────────────────────────────────┐
    │ Steering Angle (2 bytes)       │
    │ Torque (2 bytes)               │
    │ Status Flags (4 bytes)         │
    └────────────────────────────────┘
    
    SecOC-Protected Payload (16 bytes):
    ┌────────────────────────────────┐
    │ Steering Angle (2 bytes)       │
    │ Torque (2 bytes)               │
    │ Status Flags (4 bytes)         │
    │ Freshness Value (4 bytes)      │ ← Rolling counter
    │ CMAC Tag (4 bytes)             │ ← Authentication
    └────────────────────────────────┘

**C Code: FlexRay Message Authentication**

.. code-block:: c

    #include <stdint.h>
    #include <string.h>
    #include <openssl/cmac.h>
    
    #define FLEXRAY_MAX_PAYLOAD 254
    #define CMAC_TAG_LEN 4  // Truncated to 32 bits (vs. 128 bits full)
    
    // FlexRay frame structure
    typedef struct {
        uint16_t frame_id;
        uint8_t  payload_len;
        uint8_t  payload[FLEXRAY_MAX_PAYLOAD];
        uint32_t crc24;
    } flexray_frame_t;
    
    // Compute CMAC-AES-128 for FlexRay payload
    int flexray_compute_cmac(
        const uint8_t *payload,
        size_t payload_len,
        uint32_t freshness_value,
        const uint8_t *key,       // 128-bit AES key
        uint8_t *cmac_tag         // Output: 4 bytes (truncated)
    ) {
        CMAC_CTX *cmac_ctx = CMAC_CTX_new();
        CMAC_Init(cmac_ctx, key, 16, EVP_aes_128_cbc(), NULL);
        
        // Authenticate: payload + freshness value
        CMAC_Update(cmac_ctx, payload, payload_len);
        CMAC_Update(cmac_ctx, (uint8_t*)&freshness_value, sizeof(freshness_value));
        
        // Compute full CMAC (16 bytes)
        uint8_t full_cmac[16];
        size_t cmac_len;
        CMAC_Final(cmac_ctx, full_cmac, &cmac_len);
        
        // Truncate to 4 bytes (most significant)
        memcpy(cmac_tag, full_cmac, CMAC_TAG_LEN);
        
        CMAC_CTX_free(cmac_ctx);
        return 0;
    }
    
    // Send authenticated FlexRay frame
    int flexray_send_authenticated(
        flexray_frame_t *frame,
        uint32_t *freshness_counter,
        const uint8_t *shared_key
    ) {
        // Increment freshness counter (rolling)
        (*freshness_counter)++;
        
        // Embed freshness value in payload
        size_t data_len = frame->payload_len - 8;  // Reserve 8 bytes
        uint32_t freshness = *freshness_counter;
        memcpy(frame->payload + data_len, &freshness, 4);
        
        // Compute CMAC
        uint8_t cmac_tag[CMAC_TAG_LEN];
        flexray_compute_cmac(
            frame->payload,
            data_len,
            freshness,
            shared_key,
            cmac_tag
        );
        
        // Embed CMAC tag in payload
        memcpy(frame->payload + data_len + 4, cmac_tag, CMAC_TAG_LEN);
        
        // Update payload length
        frame->payload_len = data_len + 8;
        
        // Compute CRC (FlexRay protocol requirement)
        frame->crc24 = compute_flexray_crc24(frame);
        
        // Transmit frame
        return flexray_transmit(frame);
    }
    
    // Verify authenticated FlexRay frame
    int flexray_verify_authenticated(
        const flexray_frame_t *frame,
        uint32_t expected_freshness,
        const uint8_t *shared_key
    ) {
        size_t data_len = frame->payload_len - 8;
        
        // Extract freshness value and CMAC tag
        uint32_t received_freshness;
        uint8_t received_cmac[CMAC_TAG_LEN];
        memcpy(&received_freshness, frame->payload + data_len, 4);
        memcpy(received_cmac, frame->payload + data_len + 4, CMAC_TAG_LEN);
        
        // Freshness check (must be > last received)
        if (received_freshness <= expected_freshness) {
            printf("Replay attack detected! Freshness: %u (expected > %u)\n",
                   received_freshness, expected_freshness);
            return -1;
        }
        
        // Compute expected CMAC
        uint8_t expected_cmac[CMAC_TAG_LEN];
        flexray_compute_cmac(
            frame->payload,
            data_len,
            received_freshness,
            shared_key,
            expected_cmac
        );
        
        // Compare CMACs
        if (memcmp(received_cmac, expected_cmac, CMAC_TAG_LEN) != 0) {
            printf("Authentication failed! CMAC mismatch.\n");
            return -1;
        }
        
        printf("Frame authenticated successfully.\n");
        return 0;
    }

**Trade-offs:**

- ✅ Prevents message spoofing and modification
- ✅ Prevents replay attacks (freshness value)
- ❌ Reduces effective payload (8 bytes overhead)
- ❌ Processing latency (~0.5 ms per CMAC)

Countermeasure 2: Encryption (AES-CTR)
---------------------------------------

**Problem:**

FlexRay payload is plaintext (confidentiality risk).

**Solution:**

Encrypt payload with **AES-128-CTR** (Counter Mode):

.. code-block:: c

    #include <openssl/evp.h>
    
    // Encrypt FlexRay payload
    int flexray_encrypt_payload(
        const uint8_t *plaintext,
        size_t plaintext_len,
        const uint8_t *key,        // 128-bit AES key
        uint32_t counter,          // Counter value (freshness)
        uint8_t *ciphertext        // Output
    ) {
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        
        // AES-128-CTR mode
        // IV = counter (32-bit) padded to 128-bit
        uint8_t iv[16] = {0};
        memcpy(iv, &counter, 4);
        
        EVP_EncryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, key, iv);
        
        int len;
        EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len);
        
        int ciphertext_len = len;
        EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
        ciphertext_len += len;
        
        EVP_CIPHER_CTX_free(ctx);
        return ciphertext_len;
    }

**Pros:**

- ✅ Confidentiality (attacker cannot read payload)
- ✅ Fast (CTR mode is parallelizable)

**Cons:**

- ❌ Requires key management (shared secret between ECUs)
- ❌ Does NOT provide authentication (need CMAC separately)

**Best Practice: Encrypt-then-MAC**

1. Encrypt payload with AES-CTR
2. Compute CMAC over (ciphertext + freshness value)
3. Send: ciphertext || freshness || CMAC

Countermeasure 3: Network Segmentation
---------------------------------------

**Approach:**

Isolate FlexRay networks for different functions:

.. code-block:: text

    ┌────────────────────────────────────────┐
    │ FlexRay Network 1: Chassis Control    │
    │  - Steering ECU                        │
    │  - Brake ECU                           │
    │  - Suspension ECU                      │
    └────────────────────────────────────────┘
    
    ┌────────────────────────────────────────┐
    │ FlexRay Network 2: Powertrain          │
    │  - Engine ECU                          │
    │  - Transmission ECU                    │
    └────────────────────────────────────────┘
    
    ┌────────────────────────────────────────┐
    │ CAN Gateway (isolated)                 │
    │  - Filters messages between networks   │
    │  - Enforces security policies          │
    └────────────────────────────────────────┘

**Benefits:**

- Limits attack propagation (compromised infotainment → no FlexRay access)
- Reduces attack surface

Countermeasure 4: Intrusion Detection System (IDS)
---------------------------------------------------

**Approach:**

Monitor FlexRay traffic for anomalies:

.. code-block:: python

    class FlexRayIDS:
        def __init__(self):
            self.frame_baseline = {}  # Frame ID → expected timing
            self.freshness_counter = {}  # Frame ID → last counter
        
        def learn_baseline(self, frame_id, slot_number, cycle_time):
            """Learn normal FlexRay behavior"""
            self.frame_baseline[frame_id] = {
                'slot': slot_number,
                'cycle_time': cycle_time
            }
        
        def detect_anomaly(self, frame, actual_slot, actual_time):
            """Detect violations of FlexRay schedule"""
            
            frame_id = frame['frame_id']
            
            # Check 1: Frame sent in correct slot?
            if frame_id in self.frame_baseline:
                expected_slot = self.frame_baseline[frame_id]['slot']
                if actual_slot != expected_slot:
                    return f"ALERT: Frame {frame_id} in wrong slot " \
                           f"(expected {expected_slot}, got {actual_slot})"
            
            # Check 2: Frame timing correct?
            expected_cycle = self.frame_baseline[frame_id]['cycle_time']
            if abs(actual_time - expected_cycle) > 0.001:  # 1 ms tolerance
                return f"ALERT: Frame {frame_id} timing violation"
            
            # Check 3: Freshness counter increasing?
            if 'freshness' in frame:
                last_counter = self.freshness_counter.get(frame_id, 0)
                if frame['freshness'] <= last_counter:
                    return f"ALERT: Replay attack on Frame {frame_id}"
                self.freshness_counter[frame_id] = frame['freshness']
            
            return None  # No anomaly

Countermeasure 5: Hardware Security Module (HSM)
-------------------------------------------------

**Approach:**

Store cryptographic keys in **Hardware Security Module** (not in ECU flash memory).

**HSM Functions:**

1. **Key storage**: AES keys for CMAC/encryption
2. **CMAC computation**: Offload from main CPU
3. **Secure boot**: Verify ECU firmware integrity

**Example: NXP SPC58 (FlexRay ECU with HSM):**

.. code-block:: c

    // Use HSM for CMAC computation (instead of software)
    int hsm_compute_cmac(
        const uint8_t *data,
        size_t data_len,
        uint8_t key_id,       // Key stored in HSM (not exposed)
        uint8_t *cmac_tag
    ) {
        // HSM command: Compute CMAC using key_id
        hsm_command_t cmd = {
            .opcode = HSM_CMAC_COMPUTE,
            .key_id = key_id,
            .data_ptr = (uint32_t)data,
            .data_len = data_len
        };
        
        // Send command to HSM (secure channel)
        hsm_send_command(&cmd);
        
        // Wait for HSM response
        hsm_response_t resp;
        hsm_receive_response(&resp);
        
        // Extract CMAC tag
        memcpy(cmac_tag, resp.cmac_tag, 16);
        
        return 0;
    }

**Benefits:**

- ✅ Keys never leave HSM (immune to firmware extraction)
- ✅ Hardware-accelerated crypto (faster than software)
- ✅ Tamper detection (HSM locks if physical attack detected)

Exam Questions
==============

Question 1: FlexRay vs. CAN Security (Difficulty: Medium)
----------------------------------------------------------

Compare the security of FlexRay and CAN for a steer-by-wire application.

**a)** Which bus has better intrinsic security? Justify.

**b)** If both buses use AUTOSAR SecOC, which is more secure?

**Answer:**

**a) Intrinsic Security (Without SecOC):**

+---------------------+-------------------------+-------------------------+
| Aspect              | CAN                     | FlexRay                 |
+=====================+=========================+=========================+
| Authentication      | ❌ None                 | ❌ None                 |
+---------------------+-------------------------+-------------------------+
| Encryption          | ❌ None                 | ❌ None                 |
+---------------------+-------------------------+-------------------------+
| Message Integrity   | CRC-15 (weak)           | CRC-24 (stronger)       |
+---------------------+-------------------------+-------------------------+
| Arbitration         | Priority-based (DoS     | Time-triggered (harder  |
|                     | risk)                   | to DoS)                 |
+---------------------+-------------------------+-------------------------+
| Timing Predictability| Non-deterministic      | Deterministic ✅        |
+---------------------+-------------------------+-------------------------+

**Winner: FlexRay (slightly)**

**Reasoning:**

1. **CRC-24 vs. CRC-15**: FlexRay has better error detection (but still not cryptographic)
2. **Deterministic timing**: FlexRay's TDMA makes timing attacks harder
3. **Dual-channel redundancy**: FlexRay can detect/correct single-channel attacks

**However:**

- Both lack authentication/encryption (equally vulnerable to injection)
- FlexRay's complexity can introduce implementation flaws

**b) With AUTOSAR SecOC:**

+---------------------+-------------------------+-------------------------+
| Aspect              | CAN + SecOC             | FlexRay + SecOC         |
+=====================+=========================+=========================+
| Authentication      | CMAC-AES-128 ✅         | CMAC-AES-128 ✅         |
+---------------------+-------------------------+-------------------------+
| Freshness           | Rolling counter ✅      | Rolling counter ✅      |
+---------------------+-------------------------+-------------------------+
| Replay Protection   | ✅                      | ✅                      |
+---------------------+-------------------------+-------------------------+
| Bandwidth Overhead  | 8-12 bytes per msg      | 8-12 bytes per msg      |
+---------------------+-------------------------+-------------------------+
| Timing Impact       | +0.5-1 ms (CMAC)        | +0.5-1 ms (CMAC)        |
+---------------------+-------------------------+-------------------------+

**Winner: FlexRay + SecOC**

**Reasoning:**

- **Same authentication strength** (both use CMAC-AES-128)
- **FlexRay has higher bandwidth** (10 Mbps vs. 1 Mbps CAN)
  
  - Can absorb SecOC overhead better
  - 8-byte overhead on 254-byte FlexRay frame = 3% overhead
  - 8-byte overhead on 8-byte CAN frame = 100% overhead (requires second frame!)

- **Deterministic timing preserved**: FlexRay's static segment ensures SecOC
  processing fits within time budget

**Conclusion:**

For steer-by-wire, **FlexRay + SecOC** is more secure due to higher bandwidth
and deterministic timing.

Question 2: Replay Attack on FlexRay (Difficulty: Hard)
--------------------------------------------------------

An attacker captures a FlexRay steering command at time T=0:

.. code-block:: text

    Frame ID: 0x105
    Payload: [0x00, 0x2D, 0x00, 0x00, 0x00, 0x00, 0x01, 0x23, 0xAB, 0xCD, 0xEF, 0x12]
             └──────────────────┴──────────────┴──────────┴──────────────┘
                Steering Angle (45°)   Freshness (0x00000123)   CMAC Tag

The attacker replays this frame at T=1000 ms.

**a)** Will the replay be detected? Explain the detection mechanism.

**b)** Design a freshness value scheme that is robust to clock skew (±100 ms).

**Answer:**

**a) Replay Detection:**

**Yes, replay will be detected** if receiving ECU maintains a freshness counter.

**Detection Mechanism:**

.. code-block:: c

    // Receiving ECU maintains last valid freshness per sender
    uint32_t last_freshness_frame_0x105 = 0x00000122;  // Previous frame
    
    // Receive frame
    uint32_t received_freshness = 0x00000123;  // From replayed frame
    
    // Check: Freshness must be > last received
    if (received_freshness <= last_freshness_frame_0x105) {
        // Replay detected!
        log_security_event("Replay attack on Frame 0x105");
        return REJECT_FRAME;
    }
    
    // Update last valid freshness
    last_freshness_frame_0x105 = received_freshness;

**Why Replay Fails:**

At T=1000 ms, the legitimate Steering ECU has already sent ~200 frames
(1000 ms / 5 ms per frame). The current freshness counter is likely ~0x00000223.

When attacker replays old frame with freshness=0x00000123:

- Receiving ECU expects freshness > 0x00000223
- Received freshness = 0x00000123 (< 0x00000223)
- **Rejected as replay** ✅

**b) Clock Skew-Robust Freshness:**

**Problem:**

If sender's clock is 100 ms ahead of receiver's clock:

.. code-block:: text

    Sender clock: 10.100 seconds → Freshness counter = 2020
    Receiver clock: 10.000 seconds → Expected counter ≈ 2000
    
    Receiver might reject frame (counter "too high")

**Solution: Freshness Window**

Allow freshness values within a window:

.. code-block:: c

    #define FRESHNESS_WINDOW 50  // Allow ±50 counts (~250 ms at 5 ms/frame)
    
    int validate_freshness(uint32_t received, uint32_t last_valid) {
        // Freshness must be greater than last valid
        if (received <= last_valid) {
            return REPLAY_DETECTED;
        }
        
        // Freshness must not be too far ahead (future message)
        if (received > last_valid + FRESHNESS_WINDOW) {
            printf("WARNING: Freshness too far ahead (%u > %u + %u)\n",
                   received, last_valid, FRESHNESS_WINDOW);
            printf("Possible clock skew or spoofing attack\n");
            return FRESHNESS_TOO_HIGH;
        }
        
        return FRESHNESS_VALID;
    }

**Alternative: Timestamp-Based Freshness**

Instead of simple counter, use microsecond timestamp:

.. code-block:: c

    typedef struct {
        uint32_t timestamp_us;  // Microseconds since boot (wraps at ~71 minutes)
        uint16_t counter;       // Additional counter for same-timestamp messages
    } freshness_value_t;
    
    int validate_timestamp_freshness(
        freshness_value_t received,
        freshness_value_t last_valid,
        uint32_t current_time_us
    ) {
        // Check 1: Timestamp must be > last valid
        if (received.timestamp_us <= last_valid.timestamp_us) {
            return REPLAY_DETECTED;
        }
        
        // Check 2: Timestamp must not be from future (with clock skew tolerance)
        if (received.timestamp_us > current_time_us + 200000) {  // +200 ms
            return FUTURE_MESSAGE;
        }
        
        // Check 3: Timestamp must not be too old (stale message)
        if (current_time_us - received.timestamp_us > 500000) {  // 500 ms
            return STALE_MESSAGE;
        }
        
        return FRESHNESS_VALID;
    }

**Trade-off:**

- ✅ Robust to clock skew (±200 ms tolerance)
- ✅ Detects stale messages (> 500 ms old)
- ❌ Requires synchronized clocks (FlexRay global time helps)
- ❌ Larger freshness value (6 bytes vs. 4 bytes)

Question 3: Performance Impact of SecOC (Difficulty: Hard)
-----------------------------------------------------------

A FlexRay network has the following parameters:

- Cycle time: 5 ms
- Static segment: 64 slots
- Slot duration: 50 µs
- Per-slot data: 20 bytes (without SecOC)

With SecOC:

- Freshness value: 4 bytes
- CMAC tag: 4 bytes
- CMAC computation time: 0.5 ms

**a)** Calculate the bandwidth overhead of SecOC.

**b)** Will the SecOC-protected messages fit within the 50 µs slot time?

**c)** Propose optimizations to meet the timing constraint.

**Answer:**

**a) Bandwidth Overhead:**

**Original:**

- Payload: 20 bytes
- Transmission time: 20 bytes × 8 bits/byte / (10 Mbps) = **16 µs**

**With SecOC:**

- Payload: 20 + 4 (freshness) + 4 (CMAC) = 28 bytes
- Transmission time: 28 bytes × 8 bits/byte / (10 Mbps) = **22.4 µs**

**Overhead:**

- Bandwidth: (28 - 20) / 20 = **40% increase**
- Transmission time: 22.4 - 16 = **6.4 µs additional**

**b) Timing Analysis:**

**Slot duration: 50 µs**

**Time budget breakdown:**

1. **Transmission time**: 22.4 µs
2. **CMAC computation**: 500 µs (0.5 ms) ⚠️

**Total: 522.4 µs** ❌

**Problem:**

CMAC computation (500 µs) >> Slot duration (50 µs)

**This does NOT fit!**

**However:**

CMAC computation can be done **before transmission** (during previous cycle):

.. code-block:: text

    Cycle N-1:
    ├─ Compute CMAC for next frame (500 µs, in background)
    └─ Store CMAC tag in buffer
    
    Cycle N (Slot 5, 50 µs):
    ├─ Retrieve pre-computed CMAC (0 µs)
    ├─ Transmit frame (22.4 µs) ✅
    └─ Fits within 50 µs!

**Answer: Yes, if CMAC pre-computed**

**c) Optimizations:**

**Optimization 1: Hardware CMAC Accelerator (HSM)**

- Use dedicated hardware for CMAC (e.g., HSM in NXP SPC58)
- CMAC time: 500 µs → **50 µs** (10x speedup)

**Optimization 2: Truncate CMAC Tag**

- Use 4-byte truncated CMAC (currently standard)
- Could truncate to 2 bytes if security requirements allow
  
  - Security: 2^16 = 65,536 forgery attempts (weak, not recommended)
  - Bandwidth: Save 2 bytes (28 → 26 bytes)

**Optimization 3: Shared Freshness Value**

- Instead of per-message freshness, use **global FlexRay cycle counter**
- Payload: 20 bytes (data) + 4 bytes (CMAC) = 24 bytes
- Save 4 bytes freshness value

**Trade-off:**

- ✅ Reduced bandwidth (24 vs. 28 bytes)
- ❌ Weaker replay protection (freshness granularity = 5 ms cycle vs. per-message)

**Optimization 4: Selective SecOC**

- Apply SecOC only to **safety-critical messages** (steering, brake)
- Non-critical messages (diagnostics): No SecOC

**Result:**

- Critical frames: 28 bytes (with SecOC) ✅
- Non-critical frames: 20 bytes (no SecOC)
- Average bandwidth reduced

Question 4: FlexRay IDS (Difficulty: Medium)
---------------------------------------------

Design an Intrusion Detection System (IDS) for FlexRay that detects:

1. Frames sent in the wrong time slot
2. Unexpected frame IDs
3. Payload length violations

Provide pseudocode for the IDS.

**Answer:**

.. code-block:: python

    class FlexRayIDS:
        def __init__(self):
            # Baseline: Frame ID → (expected slot, expected length)
            self.baseline = {}
            self.alert_count = {}
        
        def configure_baseline(self, config_file):
            """Load expected FlexRay schedule from config"""
            # Example config:
            # Frame_ID, Slot, Payload_Length
            # 0x105, 5, 20
            # 0x106, 6, 16
            
            with open(config_file) as f:
                for line in f:
                    frame_id, slot, length = line.strip().split(',')
                    self.baseline[int(frame_id, 16)] = {
                        'slot': int(slot),
                        'length': int(length)
                    }
        
        def monitor_frame(self, frame, actual_slot, cycle_count):
            """Monitor received FlexRay frame"""
            
            frame_id = frame['frame_id']
            payload_len = frame['payload_len']
            
            # Anomaly 1: Unexpected Frame ID
            if frame_id not in self.baseline:
                self.raise_alert(
                    severity='HIGH',
                    message=f"Unknown Frame ID: 0x{frame_id:03X} in Slot {actual_slot}",
                    action='BLOCK'
                )
                return False
            
            expected = self.baseline[frame_id]
            
            # Anomaly 2: Frame in wrong slot
            if actual_slot != expected['slot']:
                self.raise_alert(
                    severity='CRITICAL',
                    message=f"Frame 0x{frame_id:03X} in wrong slot " \
                            f"(expected {expected['slot']}, got {actual_slot})",
                    action='BLOCK'
                )
                return False
            
            # Anomaly 3: Payload length violation
            if payload_len != expected['length']:
                self.raise_alert(
                    severity='MEDIUM',
                    message=f"Frame 0x{frame_id:03X} length mismatch " \
                            f"(expected {expected['length']}, got {payload_len})",
                    action='LOG'
                )
                # Allow frame (might be legitimate SecOC addition)
            
            # Anomaly 4: Rate limiting (detect flooding)
            key = (frame_id, cycle_count)
            if key in self.alert_count:
                self.raise_alert(
                    severity='CRITICAL',
                    message=f"Duplicate Frame 0x{frame_id:03X} in same cycle!",
                    action='BLOCK'
                )
                return False
            
            self.alert_count[key] = 1
            
            return True  # Frame passed all checks
        
        def raise_alert(self, severity, message, action):
            """Log security alert and take action"""
            print(f"[{severity}] FlexRay IDS Alert: {message}")
            print(f"Action: {action}")
            
            if action == 'BLOCK':
                # Drop frame, notify system monitor
                notify_security_module(message)
            elif action == 'LOG':
                # Log for forensics, allow frame
                log_to_file(message)

**Enhancements:**

**1. Machine Learning-Based IDS:**

- Train model on normal FlexRay traffic patterns
- Detect deviations (e.g., unusual payload values, timing jitter)

**2. Cross-Layer Correlation:**

- Correlate FlexRay traffic with vehicle state (speed, steering angle)
- Example: If vehicle speed = 0, reject steering commands with high angle

**3. Reputation System:**

- Track sender behavior over time
- Flag ECU if multiple anomalies detected
- Report to diagnostic tool for ECU replacement

Question 5: Key Management (Difficulty: Hard)
----------------------------------------------

A FlexRay network has 10 ECUs, all using SecOC with shared AES-128 keys.

**a)** How many keys are needed if each pair of ECUs shares a unique key?

**b)** Design a key hierarchy to reduce key storage requirements.

**c)** How should keys be provisioned during vehicle manufacturing?

**Answer:**

**a) Number of Keys (Pairwise Keys):**

If each pair of ECUs shares a unique key:

- Number of pairs: C(10, 2) = 10! / (2! × 8!) = **45 keys**

**Storage per ECU:**

- Each ECU communicates with 9 others
- Each ECU stores: **9 keys**

**Total keys in system: 45**

**b) Key Hierarchy:**

**Problem:**

45 keys is manageable for 10 ECUs, but for 50 ECUs:

- C(50, 2) = 1,225 keys (impractical)

**Solution: Key Hierarchy**

.. code-block:: text

    Root Key (Master Secret)
         ↓
    ┌────────────────────────────────────────┐
    │ Key Derivation Function (KDF)          │
    │  Derive per-ECU keys from Root Key     │
    └────────────────────────────────────────┘
         ↓
    ECU1_Key = KDF(Root_Key, "ECU1")
    ECU2_Key = KDF(Root_Key, "ECU2")
    ...
    ECU10_Key = KDF(Root_Key, "ECU10")

**Per-Message Key Derivation:**

.. code-block:: c

    #include <openssl/kdf.h>
    
    // Derive message key for sender → receiver communication
    int derive_message_key(
        const uint8_t *root_key,
        const char *sender_id,
        const char *receiver_id,
        uint8_t *message_key   // Output: 16 bytes
    ) {
        // Use HKDF (HMAC-based KDF)
        EVP_PKEY_CTX *pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_HKDF, NULL);
        EVP_PKEY_derive_init(pctx);
        EVP_PKEY_CTX_set_hkdf_md(pctx, EVP_sha256());
        EVP_PKEY_CTX_set1_hkdf_key(pctx, root_key, 16);
        
        // Info: "ECU1→ECU2"
        char info[64];
        snprintf(info, sizeof(info), "%s→%s", sender_id, receiver_id);
        EVP_PKEY_CTX_set1_hkdf_info(pctx, (uint8_t*)info, strlen(info));
        
        size_t keylen = 16;
        EVP_PKEY_derive(pctx, message_key, &keylen);
        
        EVP_PKEY_CTX_free(pctx);
        return 0;
    }

**Storage:**

- Each ECU stores: **1 Root Key** (16 bytes)
- Derive message keys on-the-fly (adds ~0.1 ms latency)

**Total keys in system: 1 Root Key** ✅

**c) Key Provisioning (Manufacturing):**

**Step 1: Key Generation (OEM Secure Facility)**

- Generate Root Key (random 128-bit value)
- Store in Hardware Security Module (HSM)

**Step 2: ECU Provisioning (Production Line)**

.. code-block:: text

    ┌────────────────────────────────────────┐
    │ Secure Programming Station             │
    │  - Connected to OEM HSM                │
    │  - Provisions Root Key into ECU        │
    └────────────────────────────────────────┘
         ↓
    ┌────────────────────────────────────────┐
    │ ECU (with HSM)                         │
    │  - Receive Root Key via encrypted      │
    │    channel                             │
    │  - Store in HSM (one-time write)       │
    │  - Lock HSM (prevent extraction)       │
    └────────────────────────────────────────┘

**Step 3: Vehicle Assembly**

- ECUs installed in vehicle
- First boot: ECUs perform mutual authentication using derived keys
- If authentication fails → Alert (ECU replaced with counterfeit?)

**Step 4: Key Rotation (Post-Production)**

- Root Key remains fixed (stored in HSM, cannot change)
- Derive **session keys** that rotate periodically:

.. code-block:: c

    // Derive session key (changes daily)
    uint32_t day_counter = get_days_since_manufacture();
    
    uint8_t session_key[16];
    derive_session_key(root_key, day_counter, session_key);
    
    // Use session_key for CMAC (valid for 24 hours)

**Benefits:**

- ✅ Compromised session key only affects 1 day
- ✅ No over-the-air key update needed (keys derived locally)

Conclusion
==========

FlexRay provides high-speed, deterministic communication for safety-critical
automotive systems, but **lacks native security** (no authentication/encryption).

**Key Security Enhancements:**

1. **AUTOSAR SecOC**: Message authentication with CMAC-AES-128
2. **Encryption**: AES-CTR for payload confidentiality
3. **Freshness Values**: Rolling counters to prevent replay attacks
4. **Intrusion Detection**: Monitor FlexRay traffic for anomalies
5. **Hardware Security Module (HSM)**: Secure key storage and crypto acceleration

**Standards Compliance:**

- ISO 17458: FlexRay protocol specification
- ISO 21434: Automotive cybersecurity engineering
- AUTOSAR SecOC: Secure onboard communication
- UN R155: Cybersecurity Management System (CSMS)

References
==========

- ISO 17458: FlexRay Communications System
- ISO 21434: Road Vehicles - Cybersecurity Engineering
- AUTOSAR SecOC Specification (R22-11)
- FlexRay Consortium: FlexRay Protocol Specification v3.0.1

**END OF DOCUMENT**
