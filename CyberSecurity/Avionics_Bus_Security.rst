🚌 **AVIONICS BUS SECURITY**
═══════════════════════════════════════════════════════════════════════

**ARINC 429, AFDX/ARINC 664, MIL-STD-1553 Security Considerations**  
**Purpose:** Legacy avionics bus security 📡 | Protocol analysis 🔍 | Mitigation strategies 🛡️  
**Standards:** ARINC 429, ARINC 664 Part 7, MIL-STD-1553, DO-326A

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**Avionics buses** connect flight-critical systems. Most protocols designed in **pre-cybersecurity era** (1970s-1990s) with **NO authentication or encryption**.

**Key buses:**
- **ARINC 429:** One-way, low-speed (12.5-100 kbps), no authentication
- **AFDX (ARINC 664):** Ethernet-based (100 Mbps), traffic policing, some security features
- **MIL-STD-1553:** Military, dual-redundant, command/response, no encryption

**Security:** Legacy buses rely on **physical isolation** and **architectural design** (not cryptography).

════════════════════════════════════════════════════════════════════════════

📡 **ARINC 429 — MARK 33 DIGITAL INFORMATION TRANSFER SYSTEM**
─────────────────────────────────────────────────────────────────────────

**Overview:**
- **Published:** 1977 (pre-dates cybersecurity concerns)
- **Speed:** 12.5 kbps (low-speed) or 100 kbps (high-speed)
- **Topology:** Point-to-point, unidirectional (one transmitter → multiple receivers)
- **Word size:** 32 bits (label + data + parity)
- **Usage:** Flight management, autopilot, navigation

**ARINC 429 Word Format:**

.. code-block:: text

   Bit Layout (32 bits):
   
   |  8   | 2  |  19    |  2   | 1  |
   |------|----|---------|----- |----|
   | Label| SDI|  Data   | SSM  | P  |
   
   - Label (8 bits): Message type (e.g., altitude, airspeed)
   - SDI (2 bits): Source/Destination Identifier
   - Data (19 bits): Actual data payload
   - SSM (2 bits): Sign/Status Matrix (validity indicator)
   - P (1 bit): Parity (odd parity for error detection)

**Security Weaknesses:**

| Vulnerability | Impact | Exploitation Difficulty |
|:--------------|:-------|:------------------------|
| **No authentication** | Any device can transmit (if wired) | Medium (requires physical access to bus) |
| **No encryption** | Data visible to all receivers | Easy (passive sniffing) |
| **No integrity protection** | Malformed messages not detected | Medium (requires message structure knowledge) |
| **No replay protection** | Old messages can be retransmitted | Easy (once physical access gained) |
| **Single parity bit** | Only detects single-bit errors | Easy (multi-bit corruption undetected) |

**Attack Scenarios:**

**Scenario 1: Altitude Spoofing**
```c
// Malicious ARINC 429 transmitter injects false altitude
void inject_false_altitude(int fake_altitude_ft) {
    uint32_t arinc429_word = 0;
    
    // Label 203 (octal) = altitude data
    arinc429_word |= (0203 << 24);  // Label
    
    // Encode altitude in BNR (Binary) format
    int altitude_encoded = (fake_altitude_ft * 4);  // LSB = 0.25 ft
    arinc429_word |= ((altitude_encoded & 0x7FFFF) << 5);  // Data bits
    
    // SSM = 00 (Normal Operation)
    arinc429_word |= (0 << 2);
    
    // Calculate odd parity
    arinc429_word |= (calculate_parity(arinc429_word) << 0);
    
    // Transmit on ARINC 429 bus (requires hardware access)
    transmit_arinc429(arinc429_word);
}
```

**Impact:** Autopilot receives incorrect altitude, could trigger TCAS false alarm or altitude deviation.

**Scenario 2: Airspeed Manipulation**
- Inject false airspeed (Label 206)
- Autopilot maintains incorrect speed
- Potential stall or overspeed

**Mitigations:**

**1. Physical Isolation:**
- ARINC 429 buses physically separate from passenger-accessible systems
- Locked avionics bay (requires key or code)

**2. Protocol Wrapper (Secure ARINC 429):**
```c
// Wrapper adds HMAC authentication to ARINC 429 messages
typedef struct {
    uint32_t arinc429_word;      // Original 32-bit word
    uint32_t sequence_number;    // Anti-replay counter
    uint8_t hmac[16];            // HMAC-SHA256 truncated to 128 bits
} SecureArinc429Message;

bool verify_secure_arinc429(SecureArinc429Message *msg) {
    // Check sequence number (must be greater than last received)
    if (msg->sequence_number <= last_sequence) {
        log_security_event(ARINC429_REPLAY);
        return false;
    }
    
    // Calculate HMAC over word + sequence
    uint8_t calculated_hmac[32];
    hmac_sha256(shared_key, 32,
                (uint8_t*)msg, sizeof(uint32_t) * 2,
                calculated_hmac);
    
    // Compare HMAC (constant-time)
    if (memcmp(msg->hmac, calculated_hmac, 16) != 0) {
        log_security_event(ARINC429_AUTH_FAIL);
        return false;
    }
    
    last_sequence = msg->sequence_number;
    return true;
}
```

**3. Cross-Channel Validation:**
- Triple-redundant systems compare ARINC 429 data
- Voting logic detects outliers (potential attack)

**4. Range Checks:**
```c
// Sanity checks on received data
bool validate_altitude(int altitude_ft) {
    if (altitude_ft < -2000 || altitude_ft > 60000) {
        return false;  // Outside operational envelope
    }
    
    // Rate-of-change check (prevent sudden jumps)
    int delta = abs(altitude_ft - last_altitude);
    if (delta > 5000) {  // 5000 ft/sec impossible
        log_security_event(ALTITUDE_ANOMALY);
        return false;
    }
    
    return true;
}
```

════════════════════════════════════════════════════════════════════════════

🌐 **AFDX / ARINC 664 PART 7 — AVIONICS FULL-DUPLEX SWITCHED ETHERNET**
─────────────────────────────────────────────────────────────────────────

**Overview:**
- **Published:** 2002 (updated 2009, 2018)
- **Speed:** 100 Mbps (modern aircraft, replaces multiple ARINC 429 buses)
- **Topology:** Switched Ethernet with redundancy (dual network)
- **Frame size:** Standard Ethernet (64-1518 bytes)
- **Usage:** Boeing 787, Airbus A380/A350

**AFDX Architecture:**

.. code-block:: text

   ┌───────────┐      ┌───────────┐      ┌───────────┐
   │ End System│      │ End System│      │ End System│
   │  (FMS)    │      │  (Autopilot)│    │ (Display) │
   └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
         │                  │                  │
         │ VL-101          │ VL-202          │ VL-303
         │                  │                  │
    ┌────▼──────────────────▼──────────────────▼────┐
    │       AFDX Switch (Network A - Primary)       │
    │  - Traffic Policing (BAG enforcement)         │
    │  - Priority Queuing (8 levels)                │
    │  - Redundancy Management                      │
    └───────────────────────────────────────────────┘
    
    ┌───────────────────────────────────────────────┐
    │       AFDX Switch (Network B - Backup)        │
    │  - Identical configuration to Network A       │
    └───────────────────────────────────────────────┘

**Virtual Links (VL):**
- Pre-configured data flows (source → destination)
- Each VL has bandwidth allocation
- **BAG (Bandwidth Allocation Gap):** Minimum time between frames (e.g., 4ms)

**Security Features:**

| Feature | Description | Security Benefit |
|:--------|:------------|:-----------------|
| **Traffic policing** | Switch enforces BAG per VL | Prevents flooding DoS |
| **VL isolation** | Each VL logically isolated | Limits lateral movement |
| **Redundancy (A/B)** | Dual independent networks | Fault tolerance (not security) |
| **Static configuration** | VLs defined at design time | Prevents dynamic route manipulation |
| **Port isolation** | End systems see only their VLs | Reduces attack surface |

**Security Weaknesses:**

| Vulnerability | Impact | Mitigation |
|:--------------|:-------|:-----------|
| **No encryption** | Data visible to switch | Physical security of switches |
| **No authentication** | VL can be spoofed if switch compromised | Switch hardening, tamper detection |
| **Limited integrity** | Ethernet CRC only (not cryptographic) | Application-layer HMAC |
| **Replay possible** | Old frames can be retransmitted | Sequence numbers in application protocol |

**Attack Scenarios:**

**Scenario 1: AFDX Flooding Attack**
```python
# Attacker compromises end system, floods AFDX network
def afdx_flood_attack(target_vl, duration_seconds):
    """Attempt to flood AFDX network (will be policed by switch)"""
    start_time = time.time()
    frames_sent = 0
    
    while time.time() - start_time < duration_seconds:
        # Craft AFDX frame for target VL
        frame = create_afdx_frame(
            vl_id=target_vl,
            payload=b"A" * 1400  # Max payload
        )
        
        # Send frame (ignoring BAG restriction)
        send_ethernet_frame(frame)
        frames_sent += 1
    
    print(f"Sent {frames_sent} frames")
    # Expected result: Switch drops excess frames (BAG enforcement)
```

**Mitigation:** AFDX switch enforces BAG, dropping excess frames. Flooding limited to allocated bandwidth.

**Scenario 2: VL Spoofing**
```c
// Attacker spoofs legitimate VL (requires compromised end system or switch)
void spoof_afdx_vl(uint16_t vl_id, uint8_t *payload, size_t len) {
    EthernetFrame frame;
    
    // Set destination MAC (derived from VL ID)
    frame.dest_mac[0] = 0x03;
    frame.dest_mac[1] = 0x00;
    frame.dest_mac[2] = 0x00;
    frame.dest_mac[3] = 0x00;
    frame.dest_mac[4] = (vl_id >> 8) & 0xFF;
    frame.dest_mac[5] = vl_id & 0xFF;
    
    // Set source MAC (attacker's MAC)
    memcpy(frame.src_mac, attacker_mac, 6);
    
    // AFDX payload
    memcpy(frame.payload, payload, len);
    
    // Send via compromised end system
    send_ethernet_frame(&frame);
}
```

**Mitigation:**
- Application-layer authentication (HMAC in payload)
- Switch port security (MAC address filtering)
- IDS monitoring for unexpected VL sources

**AFDX Security Enhancements (Modern Aircraft):**

.. code-block:: c

   // Application-layer security wrapper for AFDX
   typedef struct {
       uint32_t vl_id;              // Virtual Link ID
       uint32_t sequence_number;    // Anti-replay
       uint16_t payload_length;
       uint8_t payload[1400];
       uint8_t hmac[32];            // HMAC-SHA256
   } SecureAFDXPayload;
   
   bool verify_afdx_payload(SecureAFDXPayload *pkt) {
       // Check sequence number
       if (pkt->sequence_number <= last_sequence[pkt->vl_id]) {
           log_security_event(AFDX_REPLAY, pkt->vl_id);
           return false;
       }
       
       // Verify HMAC
       uint8_t calculated_hmac[32];
       hmac_sha256(vl_keys[pkt->vl_id], 32,
                   (uint8_t*)pkt, sizeof(SecureAFDXPayload) - 32,
                   calculated_hmac);
       
       if (memcmp(pkt->hmac, calculated_hmac, 32) != 0) {
           log_security_event(AFDX_AUTH_FAIL, pkt->vl_id);
           return false;
       }
       
       last_sequence[pkt->vl_id] = pkt->sequence_number;
       return true;
   }

════════════════════════════════════════════════════════════════════════════

⚔️ **MIL-STD-1553 — MILITARY AVIONICS DATA BUS**
─────────────────────────────────────────────────────────────────────────

**Overview:**
- **Published:** 1973 (U.S. Department of Defense)
- **Speed:** 1 Mbps
- **Topology:** Dual-redundant bus (Bus A + Bus B)
- **Command/Response:** Bus Controller (BC) commands, Remote Terminals (RT) respond
- **Usage:** F-16, F/A-18, Apache helicopter, military aircraft

**MIL-STD-1553 Architecture:**

.. code-block:: text

         Bus Controller (BC)
         ┌─────────────────┐
         │ Mission Computer│
         └────────┬────────┘
                  │
         ┌────────▼────────────────────────┐
         │   MIL-STD-1553 Bus A (Primary)  │
         └────┬─────┬─────┬─────┬──────────┘
              │     │     │     │
         ┌────▼─┐ ┌─▼──┐ ┌▼───┐ ┌▼────┐
         │ RT 1 │ │RT 2│ │RT 3│ │RT 4 │
         │ INS  │ │Radar│ │FCS │ │Wep │
         └──────┘ └────┘ └────┘ └─────┘
         
         (Bus B identical topology for redundancy)

**Command Word Format (16 bits):**

.. code-block:: text

   | 5     | 5       | 5       | 1  |
   |-------|---------|---------|-----|
   | RT Addr| Subaddr | Count   | T/R |
   
   - RT Address (5 bits): Remote Terminal ID (1-30)
   - Subaddress (5 bits): Function code
   - Count (5 bits): Number of data words (1-32)
   - T/R (1 bit): Transmit (0) or Receive (1)

**Security Weaknesses:**

| Vulnerability | Impact | Exploitation Difficulty |
|:--------------|:-------|:------------------------|
| **No authentication** | Any device can be BC | Difficult (requires bus coupler hardware) |
| **No encryption** | All messages in plaintext | Medium (requires physical access + coupler) |
| **Single parity** | Only detects single-bit errors | Medium (multi-bit injection possible) |
| **Deterministic timing** | Traffic analysis reveals mission profile | Easy (passive monitoring) |

**Attack Scenarios:**

**Scenario 1: Rogue Bus Controller**
```c
// Attacker injects rogue BC commands (requires hardware access)
void rogue_bc_command(uint8_t rt_address, uint8_t subaddr, uint16_t *data, uint8_t count) {
    // Craft BC-to-RT command word
    uint16_t command_word = 0;
    command_word |= (rt_address & 0x1F) << 11;  // RT address
    command_word |= (subaddr & 0x1F) << 6;      // Subaddress
    command_word |= (count & 0x1F) << 1;        // Word count
    command_word |= 1;                          // Receive (BC → RT)
    
    // Add parity bit
    command_word |= (calculate_parity(command_word) << 0);
    
    // Transmit command (requires MIL-STD-1553 transceiver)
    transmit_1553(command_word);
    
    // Transmit data words
    for (int i = 0; i < count; i++) {
        transmit_1553(data[i]);
    }
}
```

**Impact:** Rogue commands to weapon systems, flight control surfaces (catastrophic).

**Scenario 2: Bus Jamming**
- Continuously transmit on bus → deny legitimate communication
- Dual-redundant bus provides resilience (switch to Bus B)

**Mitigations:**

**1. Physical Security:**
- MIL-STD-1553 couplers in secure enclosures
- Tamper detection on avionics bay
- Classified missions use encrypted overlays

**2. Bus Monitor:**
```python
# Intrusion detection for MIL-STD-1553 bus
class MilStd1553IDS:
    def __init__(self):
        self.baseline_traffic = {}
        self.alerts = []
    
    def learn_baseline(self, flight_logs):
        """Learn normal traffic patterns"""
        for log in flight_logs:
            key = (log['bc_addr'], log['rt_addr'], log['subaddr'])
            if key not in self.baseline_traffic:
                self.baseline_traffic[key] = {
                    'avg_rate': 0,
                    'avg_data_words': 0
                }
            # Update statistics...
    
    def detect_anomaly(self, command):
        """Detect unusual 1553 traffic"""
        key = (command['bc_addr'], command['rt_addr'], command['subaddr'])
        
        # Alert on unknown RT address
        if command['rt_addr'] > 30:
            self.alerts.append({
                'type': 'INVALID_RT_ADDRESS',
                'severity': 'HIGH',
                'command': command
            })
            return True
        
        # Alert on unexpected traffic pattern
        if key not in self.baseline_traffic:
            self.alerts.append({
                'type': 'UNEXPECTED_TRAFFIC',
                'severity': 'MEDIUM',
                'key': key
            })
            return True
        
        return False
```

**3. Encrypted MIL-STD-1553 (NSA Type 1):**
- Classified systems use Type 1 encryption devices inline
- Encrypts data words (command words in plaintext for routing)
- Requires COMSEC keying material

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Why does ARINC 429 lack authentication, and how is security achieved?**

**A1:**
**Historical context:** ARINC 429 designed in 1977, pre-dating cybersecurity concerns. Assumptions:
- Aircraft systems physically isolated
- Adversaries have no access to avionics bay
- Focus on **safety** (random failures), not **security** (adversarial threats)

**Security approach:**
1. **Physical isolation:** ARINC 429 buses not connected to passenger systems
2. **Locked avionics bay:** Requires key or access code
3. **Architectural design:** Unidirectional (receiver cannot inject messages)
4. **Cross-channel validation:** Triple-redundant systems vote (detect outliers)
5. **Secure wrapper:** Modern aircraft add HMAC at application layer

**Key insight:** Security relies on **defense-in-depth** (physical + architectural), not protocol-level cryptography.

**Q2: How does AFDX traffic policing mitigate DoS attacks?**

**A2:**
**Traffic policing** enforces Bandwidth Allocation Gap (BAG) per Virtual Link (VL).

**Mechanism:**
- Each VL configured with BAG (e.g., 4ms = max 250 frames/sec)
- AFDX switch drops frames exceeding BAG
- Attacker flooding VL cannot consume more than allocated bandwidth

**Example:**
```
VL-101 (FMS data): BAG = 8ms → max 125 frames/sec
VL-202 (Display): BAG = 16ms → max 62.5 frames/sec

Attacker compromises FMS, sends 1000 frames/sec:
- Switch allows 125 frames/sec (per BAG)
- Drops remaining 875 frames/sec
- Result: DoS limited to VL-101, other VLs unaffected
```

**Defense-in-depth:**
- Traffic policing (network layer)
- Application-layer rate limiting
- IDS monitoring (alert on BAG violations)

**Q3: Describe a realistic attack on MIL-STD-1553 and its impact.**

**A3:**
**Attack: Rogue Bus Controller Command Injection**

**Preconditions:**
- Attacker gains physical access to aircraft (maintenance, insider)
- Installs MIL-STD-1553 coupler on bus (tap + transceiver)

**Execution:**
1. Monitor bus traffic (learn command patterns)
2. Wait for BC to go silent (brief window)
3. Inject rogue BC-to-RT command:
   - Target RT: Flight Control System (RT 3, subaddress 5)
   - Command: "Deflect aileron +10 degrees"
4. Transmit data words with malicious control values

**Impact:**
- Aircraft rolls unexpectedly
- Autopilot compensates (detects error)
- If executed during critical phase (landing), potential crash

**Detection:**
- Dual-redundant bus (Bus B detects discrepancy)
- Voting logic (FCS compares commands from multiple sources)
- IDS alerts on unexpected command sequence

**Mitigation:**
- Tamper-evident seals on avionics bay
- Bus monitoring (detect rogue BC)
- Encrypted MIL-STD-1553 (NSA Type 1 for classified)

**Q4: Compare security features of ARINC 429, AFDX, and MIL-STD-1553.**

**A4:**

| Feature | ARINC 429 | AFDX (ARINC 664) | MIL-STD-1553 |
|:--------|:----------|:-----------------|:-------------|
| **Authentication** | ❌ None | ❌ None (app-layer possible) | ❌ None |
| **Encryption** | ❌ None | ❌ None | ⚠️ Type 1 (classified) |
| **Integrity** | ⚠️ Parity (1 bit) | ⚠️ Ethernet CRC | ⚠️ Parity (1 bit) |
| **DoS protection** | ✅ Unidirectional | ✅ Traffic policing | ⚠️ BC priority |
| **Isolation** | ✅ Physical | ✅ VL isolation | ✅ Physical |
| **Redundancy** | ⚠️ App-dependent | ✅ Dual network | ✅ Dual bus |
| **Speed** | 12.5-100 kbps | 100 Mbps | 1 Mbps |
| **Security model** | Physical + design | Physical + policing | Physical + monitoring |

**Summary:** All three rely primarily on **physical security** and **architectural isolation**, not protocol-level cryptography.

**Q5: What is a "secure wrapper" for legacy avionics buses?**

**A5:**
**Concept:** Add cryptographic security at **application layer** without modifying physical bus protocol.

**Implementation:**
```c
// Original ARINC 429 message
uint32_t arinc429_word = build_altitude_message(35000);

// Secure wrapper adds authentication
SecureWrapper wrapper = {
    .payload = arinc429_word,
    .sequence = get_next_sequence(),
    .hmac = calculate_hmac(arinc429_word, sequence, shared_key)
};

// Transmit wrapper (as multiple ARINC 429 words if needed)
transmit_secure_wrapper(&wrapper);
```

**Receiver:**
```c
// Receive secure wrapper
SecureWrapper wrapper = receive_secure_wrapper();

// Verify sequence (anti-replay)
if (wrapper.sequence <= last_sequence) reject();

// Verify HMAC
if (!verify_hmac(&wrapper)) reject();

// Extract original payload
uint32_t arinc429_word = wrapper.payload;
process_altitude(arinc429_word);
```

**Benefits:**
- No hardware modification (software-only)
- Backward compatible (non-secure receivers ignore wrapper)
- Adds authentication, integrity, replay protection

**Limitations:**
- Increased bandwidth (overhead for crypto metadata)
- Both ends must support wrapper protocol

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~700
