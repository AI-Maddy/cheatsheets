====================================================================
Automotive Ethernet Security (IEEE 802.1 & SOME/IP)
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEEE 802.1AE (MACsec), IEEE 802.1AS, SOME/IP, AVB/TSN, BroadR-Reach

.. contents:: Table of Contents
   :depth: 3

TL;DR - Quick Reference
=======================

**Automotive Ethernet Key Points:**

+-------------------------+------------------------------------------------+
| **Property**            | **Details**                                    |
+=========================+================================================+
| **Physical Layer**      | 100BASE-T1 (100 Mbps), 1000BASE-T1 (1 Gbps)   |
|                         | BroadR-Reach (single twisted pair)             |
+-------------------------+------------------------------------------------+
| **Bandwidth**           | 100x higher than CAN (1 Mbps)                  |
+-------------------------+------------------------------------------------+
| **Protocols**           | SOME/IP, DoIP, AVB/TSN, TCP/IP                 |
+-------------------------+------------------------------------------------+
| **Security**            | MACsec (802.1AE), TLS, IPsec                   |
+-------------------------+------------------------------------------------+
| **Applications**        | ADAS cameras, infotainment, gateway, OTA       |
+-------------------------+------------------------------------------------+

**Security Stack:**

.. code-block:: text

    Application Layer
    ├─ SOME/IP over TLS ← Message authentication & encryption
    ├─ DoIP (Diagnostics over IP)
    └─ AVB/TSN (Audio/Video Bridging, Time-Sensitive Networking)
    
    Transport Layer
    ├─ TCP/UDP
    └─ IPsec ← Network-layer encryption (optional)
    
    Network Layer
    ├─ IPv4/IPv6
    └─ DHCP, ARP
    
    Data Link Layer
    ├─ Ethernet (IEEE 802.3)
    └─ MACsec (IEEE 802.1AE) ← Link-layer encryption
    
    Physical Layer
    └─ 100BASE-T1, 1000BASE-T1 (BroadR-Reach)

**MACsec (IEEE 802.1AE) Overview:**

.. code-block:: text

    Ethernet Frame with MACsec:
    ┌────────────────────────────────────────────────────┐
    │ Dest MAC │ Src MAC │ EtherType (0x88E5)            │
    ├────────────────────────────────────────────────────┤
    │ MACsec Header (8 bytes):                           │
    │  - TCI (2 bytes): Flags (encrypted, ICV present)   │
    │  - PN (4 bytes): Packet Number (anti-replay)       │
    ├────────────────────────────────────────────────────┤
    │ Encrypted Payload (original Ethernet payload)      │
    ├────────────────────────────────────────────────────┤
    │ ICV (16 bytes): Integrity Check Value (GCM tag)    │
    └────────────────────────────────────────────────────┘

**Common Automotive Ethernet Use Cases:**

1. **ADAS**: Camera sensors (360° surround view, front camera 8 MP)
2. **Infotainment**: High-resolution displays, streaming audio/video
3. **Gateway**: Central gateway ECU connecting CAN, LIN, FlexRay
4. **OTA Updates**: Download firmware over cellular → Ethernet backbone
5. **Vehicle-to-Cloud**: Telematics, remote diagnostics

Introduction to Automotive Ethernet
====================================

**Why Automotive Ethernet?**

Traditional automotive networks (CAN, LIN, FlexRay) have bandwidth limitations:

- **CAN**: 1 Mbps (insufficient for camera data)
- **CAN-FD**: 5-8 Mbps (still limited)
- **FlexRay**: 10 Mbps

**Modern ADAS requires:**

- Front camera: 8 MP @ 30 fps = ~240 Mbps
- 360° surround view: 4 cameras @ 2 MP = ~192 Mbps
- LiDAR point cloud: ~10 Mbps
- Radar: ~1 Mbps

**Total: >500 Mbps** → CAN cannot handle this.

**Automotive Ethernet Solution:**

- **100BASE-T1**: 100 Mbps over single twisted pair (IEEE 802.3bw)
- **1000BASE-T1**: 1 Gbps over single twisted pair (IEEE 802.3bp)
- **BroadR-Reach**: Broadcom's physical layer technology (adopted by IEEE)

Physical Layer: BroadR-Reach & 100BASE-T1
==========================================

BroadR-Reach (100 Mbps)
------------------------

**Key Features:**

- **Single twisted pair**: Reduces cable weight (critical for automotive)
- **100 Mbps full-duplex**: Bidirectional communication
- **Up to 15 meters**: Sufficient for in-vehicle networks
- **EMI resistant**: Operates in harsh automotive environment

**Cable Specification:**

- Unshielded twisted pair (UTP) or shielded (STP)
- Typically 2 x 0.5 mm² copper wire

**Connector:**

- Standard: OPEN Alliance TC9 (automotive-grade RJ45 variant)
- Locking mechanism for vibration resistance

1000BASE-T1 (1 Gbps)
---------------------

**Use Cases:**

- ADAS domain controllers (central processing unit for sensors)
- High-resolution camera backbones
- Zonal architectures (zone controllers)

**Performance:**

- 1 Gbps over single twisted pair
- Up to 15-40 meters (depending on cable quality)

Automotive Ethernet Architecture
=================================

Typical In-Vehicle Network Topology
------------------------------------

.. code-block:: text

    ┌───────────────────────────────────────────────────────────┐
    │                  Central Gateway ECU                      │
    │  - Route between CAN, LIN, FlexRay, Ethernet              │
    │  - Firewall (filter messages between domains)             │
    └───────────┬───────────────┬───────────────┬───────────────┘
                │               │               │
         ┌──────┴──────┐  ┌─────┴─────┐  ┌──────┴──────┐
         │ Powertrain  │  │  Chassis  │  │ Infotainment │
         │  CAN Bus    │  │  CAN Bus  │  │   Ethernet   │
         └─────────────┘  └───────────┘  └───────┬──────┘
                                                  │
                                         ┌────────┴────────┐
                                         │   ADAS Ethernet │
                                         │  (Camera ring)  │
                                         └────────┬────────┘
                                                  │
                             ┌────────────────────┼────────────────────┐
                             │                    │                    │
                        ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
                        │ Camera 1│          │ Camera 2│          │ Camera 3│
                        │ (Front) │          │ (Rear)  │          │ (Side)  │
                        └─────────┘          └─────────┘          └─────────┘

**Security Zones:**

- **Powertrain/Chassis CAN**: Safety-critical (IEC 62443 SL-4)
- **Infotainment Ethernet**: Low criticality (SL-1)
- **ADAS Ethernet**: High criticality (SL-3, safety-related)
- **Gateway**: DMZ between zones (SL-3)

MACsec (IEEE 802.1AE) for Link-Layer Security
==============================================

MACsec Overview
---------------

**MACsec (Media Access Control Security)** provides:

- **Confidentiality**: AES-128-GCM or AES-256-GCM encryption
- **Integrity**: GCM authentication tag (ICV)
- **Anti-replay**: Packet number (PN) sequence validation

**Standards:**

- IEEE 802.1AE-2018: MACsec protocol
- IEEE 802.1X: Port-based authentication (optional, for key exchange)
- IEEE 802.1AR: Secure device identity (DevID certificates)

MACsec Frame Format
-------------------

**Original Ethernet Frame:**

.. code-block:: text

    ┌──────────┬──────────┬───────────┬─────────┬─────┐
    │ Dest MAC │ Src MAC  │ EtherType │ Payload │ FCS │
    └──────────┴──────────┴───────────┴─────────┴─────┘

**MACsec-Protected Frame:**

.. code-block:: text

    ┌──────────┬──────────┬────────────┬────────────────┬──────────────┬─────┬─────┐
    │ Dest MAC │ Src MAC  │ EtherType  │ MACsec Header  │ Encrypted    │ ICV │ FCS │
    │          │          │  (0x88E5)  │  (8 bytes)     │ Payload      │(16B)│     │
    └──────────┴──────────┴────────────┴────────────────┴──────────────┴─────┴─────┘

**MACsec Header (SecTAG):**

- **TCI/AN** (2 bytes): Tag Control Information, Association Number
- **SL** (1 byte): Short Length (for short frames)
- **PN** (4 bytes): Packet Number (monotonically increasing counter)
- **SCI** (8 bytes, optional): Secure Channel Identifier

MACsec Encryption (AES-GCM)
----------------------------

**Algorithm: AES-128-GCM or AES-256-GCM**

.. code-block:: text

    Inputs:
    - Key: 128-bit or 256-bit AES key (pre-shared or derived)
    - IV (Initialization Vector): Constructed from SCI + PN
    - AAD (Additional Authenticated Data): MACsec header
    - Plaintext: Original Ethernet payload
    
    Outputs:
    - Ciphertext: Encrypted payload
    - ICV (Integrity Check Value): 16-byte GCM authentication tag

**GCM Mode Benefits:**

- Authenticated encryption (confidentiality + integrity in one operation)
- Efficient hardware acceleration (AES-NI instructions)
- Suitable for high-speed networks (1 Gbps line rate)

C Code: MACsec Frame Processing (Conceptual)
---------------------------------------------

.. code-block:: c

    #include <openssl/evp.h>
    #include <stdint.h>
    #include <string.h>
    
    // MACsec header structure
    typedef struct {
        uint16_t tci_an;     // TCI (1 byte) + AN (1 byte)
        uint8_t  sl;         // Short Length
        uint32_t pn;         // Packet Number
        uint8_t  sci[8];     // Secure Channel Identifier (optional)
    } __attribute__((packed)) macsec_header_t;
    
    // Encrypt Ethernet frame with MACsec (AES-128-GCM)
    int macsec_encrypt_frame(
        const uint8_t *key,           // 128-bit AES key
        const uint8_t *plaintext,     // Original Ethernet payload
        size_t plaintext_len,
        uint32_t packet_number,       // Packet number (anti-replay)
        const uint8_t *sci,           // Secure Channel ID (8 bytes)
        uint8_t *ciphertext,          // Output: encrypted payload
        uint8_t *icv                  // Output: 16-byte ICV (GCM tag)
    ) {
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        
        // Construct IV from SCI and Packet Number
        uint8_t iv[12];
        memcpy(iv, sci, 8);              // First 8 bytes: SCI
        memcpy(iv + 8, &packet_number, 4); // Last 4 bytes: PN
        
        // Initialize AES-128-GCM
        EVP_EncryptInit_ex(ctx, EVP_aes_128_gcm(), NULL, key, iv);
        
        // Set AAD (Additional Authenticated Data): MACsec header
        macsec_header_t macsec_hdr;
        macsec_hdr.pn = htonl(packet_number);
        memcpy(macsec_hdr.sci, sci, 8);
        
        int len;
        EVP_EncryptUpdate(ctx, NULL, &len, (uint8_t*)&macsec_hdr, sizeof(macsec_hdr));
        
        // Encrypt payload
        int ciphertext_len;
        EVP_EncryptUpdate(ctx, ciphertext, &ciphertext_len, plaintext, plaintext_len);
        
        // Finalize (generates ICV)
        int final_len;
        EVP_EncryptFinal_ex(ctx, ciphertext + ciphertext_len, &final_len);
        
        // Get GCM tag (ICV)
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, icv);
        
        EVP_CIPHER_CTX_free(ctx);
        
        return ciphertext_len + final_len;
    }
    
    // Decrypt and verify MACsec frame
    int macsec_decrypt_frame(
        const uint8_t *key,
        const uint8_t *ciphertext,
        size_t ciphertext_len,
        uint32_t packet_number,
        const uint8_t *sci,
        const uint8_t *icv,           // Received ICV (16 bytes)
        uint8_t *plaintext            // Output: decrypted payload
    ) {
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        
        // Construct IV
        uint8_t iv[12];
        memcpy(iv, sci, 8);
        memcpy(iv + 8, &packet_number, 4);
        
        // Initialize AES-128-GCM for decryption
        EVP_DecryptInit_ex(ctx, EVP_aes_128_gcm(), NULL, key, iv);
        
        // Set AAD (MACsec header)
        macsec_header_t macsec_hdr;
        macsec_hdr.pn = htonl(packet_number);
        memcpy(macsec_hdr.sci, sci, 8);
        
        int len;
        EVP_DecryptUpdate(ctx, NULL, &len, (uint8_t*)&macsec_hdr, sizeof(macsec_hdr));
        
        // Set expected ICV
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, 16, (void*)icv);
        
        // Decrypt payload
        int plaintext_len;
        EVP_DecryptUpdate(ctx, plaintext, &plaintext_len, ciphertext, ciphertext_len);
        
        // Finalize (verifies ICV)
        int final_len;
        int ret = EVP_DecryptFinal_ex(ctx, plaintext + plaintext_len, &final_len);
        
        EVP_CIPHER_CTX_free(ctx);
        
        if (ret > 0) {
            return plaintext_len + final_len;  // Success
        } else {
            return -1;  // ICV verification failed (tampered or wrong key)
        }
    }

MACsec Key Management
---------------------

**Options:**

1. **Static Pre-Shared Keys (PSK):**
   
   - Keys provisioned at factory
   - Stored in ECU secure flash or HSM
   - Simple but requires key rotation mechanism

2. **IEEE 802.1X with MKA (MACsec Key Agreement):**
   
   - Dynamic key exchange using EAP (Extensible Authentication Protocol)
   - Requires authentication server (RADIUS)
   - More complex, but supports key rotation

3. **IKEv2 (Internet Key Exchange):**
   
   - Used in conjunction with IPsec
   - Certificate-based authentication

**Typical Automotive: Static PSK** (simpler for embedded systems)

SOME/IP (Scalable service-Oriented MiddlewarE over IP)
=======================================================

SOME/IP Overview
----------------

**SOME/IP** is an automotive middleware protocol for service-oriented
communication over Ethernet.

**Key Features:**

- **Service discovery**: Dynamic discovery of ECU services
- **Publish-subscribe**: Event notifications
- **RPC (Remote Procedure Call)**: Request-response communication
- **Serialization**: Efficient binary encoding

**Use Cases:**

- ADAS sensor fusion (camera, radar, LiDAR data aggregation)
- Infotainment services (navigation, media streaming)
- OTA update management

SOME/IP Message Format
-----------------------

.. code-block:: text

    SOME/IP Header (16 bytes):
    ┌────────────────────────────────────────────────┐
    │ Message ID (32 bits)                           │
    │  - Service ID (16 bits)                        │
    │  - Method ID (16 bits)                         │
    ├────────────────────────────────────────────────┤
    │ Length (32 bits): Payload length + 8 bytes     │
    ├────────────────────────────────────────────────┤
    │ Request ID (32 bits)                           │
    │  - Client ID (16 bits)                         │
    │  - Session ID (16 bits)                        │
    ├────────────────────────────────────────────────┤
    │ Protocol Version (8 bits)                      │
    │ Interface Version (8 bits)                     │
    │ Message Type (8 bits): REQUEST, RESPONSE, etc. │
    │ Return Code (8 bits): OK, ERROR, etc.          │
    └────────────────────────────────────────────────┘
    
    Payload (variable length)

SOME/IP Security (SOME/IP-TP with TLS)
---------------------------------------

**Problem:**

SOME/IP does not provide built-in encryption or authentication.

**Solution:**

**SOME/IP over TLS (SOME/IP Secure)**

.. code-block:: text

    Application
         ↓
    SOME/IP (Serialization)
         ↓
    TLS 1.3 ← Encryption + Authentication
         ↓
    TCP/UDP
         ↓
    IP
         ↓
    MACsec (optional, link-layer encryption)

**TLS Configuration:**

- **TLS 1.3**: Modern, fast handshake
- **Cipher suite**: TLS_AES_128_GCM_SHA256 (AESGCM for efficiency)
- **Certificates**: X.509 certificates per ECU (IEEE 802.1AR DevID)
- **Mutual authentication**: Both client and server authenticate

Python Code: SOME/IP over TLS
------------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """
    SOME/IP server with TLS encryption
    """
    
    import socket
    import ssl
    import struct
    
    class SOMEIPServer:
        def __init__(self, host='0.0.0.0', port=30509):
            self.host = host
            self.port = port
            
            # Create SSL context
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.context.load_cert_chain('server.crt', 'server.key')
            
            # Require client certificate (mutual TLS)
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_verify_locations('ca.crt')
            
            # Modern cipher suites only
            self.context.set_ciphers('TLS_AES_128_GCM_SHA256')
        
        def parse_someip_header(self, data):
            """Parse SOME/IP header (16 bytes)"""
            if len(data) < 16:
                return None
            
            service_id = struct.unpack('>H', data[0:2])[0]
            method_id = struct.unpack('>H', data[2:4])[0]
            length = struct.unpack('>I', data[4:8])[0]
            client_id = struct.unpack('>H', data[8:10])[0]
            session_id = struct.unpack('>H', data[10:12])[0]
            protocol_version = data[12]
            interface_version = data[13]
            message_type = data[14]
            return_code = data[15]
            
            return {
                'service_id': service_id,
                'method_id': method_id,
                'length': length,
                'client_id': client_id,
                'session_id': session_id,
                'message_type': message_type
            }
        
        def create_someip_response(self, request, response_data):
            """Create SOME/IP response message"""
            header = bytearray(16)
            
            # Copy Message ID from request
            header[0:4] = request[0:4]
            
            # Length = payload length + 8
            length = len(response_data) + 8
            struct.pack_into('>I', header, 4, length)
            
            # Copy Request ID
            header[8:12] = request[8:12]
            
            # Protocol version, Interface version
            header[12] = 0x01
            header[13] = 0x01
            
            # Message Type: RESPONSE (0x80)
            header[14] = 0x80
            
            # Return Code: OK (0x00)
            header[15] = 0x00
            
            return bytes(header) + response_data
        
        def handle_client(self, conn):
            """Handle SOME/IP client connection"""
            print(f"Client connected: {conn.getpeercert()['subject']}")
            
            while True:
                # Receive SOME/IP message over TLS
                data = conn.recv(4096)
                if not data:
                    break
                
                # Parse SOME/IP header
                header = self.parse_someip_header(data)
                if not header:
                    continue
                
                print(f"Received SOME/IP: Service={header['service_id']:04X}, "
                      f"Method={header['method_id']:04X}")
                
                # Process request (example: echo service)
                payload = data[16:]
                response_data = b"ACK: " + payload
                
                # Create response
                response = self.create_someip_response(data, response_data)
                
                # Send response over TLS
                conn.send(response)
        
        def start(self):
            """Start SOME/IP TLS server"""
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, self.port))
                sock.listen(5)
                print(f"SOME/IP TLS server listening on {self.host}:{self.port}")
                
                with self.context.wrap_socket(sock, server_side=True) as ssock:
                    while True:
                        conn, addr = ssock.accept()
                        print(f"Connection from {addr}")
                        self.handle_client(conn)
                        conn.close()
    
    if __name__ == "__main__":
        server = SOMEIPServer()
        server.start()

AVB/TSN (Audio Video Bridging / Time-Sensitive Networking)
===========================================================

AVB/TSN Overview
----------------

**AVB (Audio Video Bridging)** and **TSN (Time-Sensitive Networking)** are
IEEE standards for **deterministic, low-latency Ethernet**.

**Key Standards:**

- **IEEE 802.1AS**: Time synchronization (gPTP - generalized Precision Time Protocol)
- **IEEE 802.1Qav**: Credit-Based Shaper (CBS) for bandwidth reservation
- **IEEE 802.1Qbv**: Time-Aware Shaper (TAS) for scheduled traffic
- **IEEE 802.1Qbu**: Frame Preemption (split large frames)

**Use Cases in Automotive:**

- ADAS sensor data (camera frames must arrive within 10 ms)
- Vehicle control (steering, braking commands)
- Audio streaming (infotainment)

Time Synchronization (IEEE 802.1AS - gPTP)
-------------------------------------------

**Problem:**

Multiple ECUs need synchronized clocks for:

- Sensor fusion (camera timestamps must align)
- Scheduled traffic (TAS requires time sync)

**Solution: gPTP (generalized Precision Time Protocol)**

.. code-block:: text

    Grandmaster Clock (GPS-synchronized)
           │
           ├─ Sync Message (timestamp T1)
           ↓
        ECU 1 (Bridge)
           │
           ├─ Follow-Up Message (actual T1)
           ↓
        ECU 2 (End Station)

**Accuracy:** ~1 microsecond synchronization

Security Concerns with TSN
---------------------------

**Vulnerability 1: Time Synchronization Attacks**

- Attacker sends forged gPTP Sync messages with incorrect timestamps
- ECUs desynchronize, causing sensor fusion failures

**Mitigation:**

- **IEEE 802.1AS-Rev**: Add authentication to gPTP messages
- Use MACsec to authenticate gPTP frames

**Vulnerability 2: Traffic Shaping Manipulation**

- Attacker modifies TAS schedule (changes which traffic class gets priority)
- Safety-critical messages delayed

**Mitigation:**

- Digitally sign TAS configuration
- Verify configuration integrity at boot

DoIP (Diagnostics over IP)
===========================

DoIP Overview
-------------

**DoIP (ISO 13400)** replaces CAN-based diagnostics (ISO 15765) for
high-bandwidth Ethernet diagnostics.

**Use Cases:**

- Flash programming (firmware updates)
- Fault code reading (DTCs)
- ECU configuration

**Protocol Stack:**

.. code-block:: text

    UDS (ISO 14229) ← Diagnostic services
         ↓
    DoIP (ISO 13400) ← Transport over IP
         ↓
    TCP/UDP
         ↓
    IPv4/IPv6
         ↓
    Automotive Ethernet

DoIP Security Risks
-------------------

**Risk 1: Unauthorized Diagnostics**

- Attacker connects to OBD-II port (or remote network)
- Sends DoIP diagnostic requests
- Reads/writes ECU memory

**Mitigation:**

- **Authentication**: UDS Security Access (Service 0x27)
- **Authorization**: Role-based access control
- **TLS**: Encrypt DoIP traffic

**Risk 2: Flash Programming Attacks**

- Attacker uploads malicious firmware via DoIP

**Mitigation:**

- **Code signing**: Verify firmware signature before flashing
- **Secure boot**: Reject unsigned firmware

Python Code: DoIP with TLS
---------------------------

.. code-block:: python

    import socket
    import ssl
    import struct
    
    class DoIPClient:
        def __init__(self, ecu_ip, port=13400):
            self.ecu_ip = ecu_ip
            self.port = port
            
            # TLS context
            self.context = ssl.create_default_context()
            self.context.load_cert_chain('client.crt', 'client.key')
        
        def send_doip_request(self, payload):
            """Send DoIP diagnostic request"""
            # DoIP header (8 bytes)
            protocol_version = 0x02  # ISO 13400-2
            inverse_version = 0xFD
            payload_type = 0x8001  # Diagnostic message
            payload_length = len(payload)
            
            header = struct.pack('>BBHI', protocol_version, inverse_version,
                                payload_type, payload_length)
            
            doip_message = header + payload
            
            # Send over TLS
            with socket.create_connection((self.ecu_ip, self.port)) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.ecu_ip) as ssock:
                    ssock.send(doip_message)
                    
                    # Receive response
                    response = ssock.recv(4096)
                    return response[8:]  # Strip DoIP header
        
        def read_dtc(self):
            """Read Diagnostic Trouble Codes (UDS Service 0x19)"""
            # UDS request: Service 0x19 (ReadDTCInformation), Sub-function 0x02
            uds_request = bytes([0x19, 0x02, 0xFF])
            
            response = self.send_doip_request(uds_request)
            print(f"DTC Response: {response.hex()}")
            return response

Exam Questions
==============

Question 1: MACsec vs. IPsec (Difficulty: Medium)
--------------------------------------------------

Compare MACsec (IEEE 802.1AE) and IPsec for securing automotive Ethernet:

**a)** Which OSI layer does each operate at?

**b)** For ADAS camera data (raw sensor frames), which is more suitable? Justify.

**c)** Can both be used simultaneously? If so, what is the security benefit?

**Answer:**

**a) OSI Layers:**

- **MACsec (IEEE 802.1AE)**: **Layer 2 (Data Link Layer)**
  
  - Encrypts entire Ethernet frame (after MAC addresses)
  - Operates below IP layer

- **IPsec**: **Layer 3 (Network Layer)**
  
  - Encrypts IP packets
  - Operates above Ethernet, below TCP/UDP

**b) For ADAS Camera Data:**

**Recommendation: MACsec**

**Justification:**

1. **Performance**:
   
   - MACsec operates at hardware layer (Ethernet PHY or switch)
   - Hardware-accelerated AES-GCM (line-rate encryption at 1 Gbps)
   - IPsec operates in software (CPU overhead)

2. **Simplicity**:
   
   - ADAS camera sends raw Ethernet frames (no IP stack required)
   - MACsec protects all Ethernet traffic (including non-IP protocols)

3. **Latency**:
   
   - MACsec adds <1 microsecond latency
   - IPsec adds several microseconds (software processing)

4. **Broadcast/Multicast**:
   
   - MACsec supports broadcast (useful for SOME/IP service discovery)
   - IPsec does not natively support broadcast

**c) Simultaneous Use:**

**Yes, MACsec + IPsec can be used together** (defense-in-depth):

.. code-block:: text

    Application (SOME/IP)
         ↓
    TLS (optional, application-layer)
         ↓
    TCP/UDP
         ↓
    IPsec (ESP) ← Network-layer encryption
         ↓
    IP
         ↓
    MACsec ← Link-layer encryption
         ↓
    Ethernet PHY

**Security Benefit:**

- **MACsec**: Protects against attacks on local Ethernet segment (attacker with
  physical access to Ethernet cable)
- **IPsec**: Protects end-to-end across gateways and routers (attacker on
  different network segment)

**Trade-off:** Increased latency and CPU overhead. Typically, **MACsec alone**
is sufficient for in-vehicle networks.

Question 2: SOME/IP Service Discovery Attack (Difficulty: Hard)
----------------------------------------------------------------

An attacker compromises an infotainment ECU and sends fake SOME/IP Service
Discovery (SD) messages advertising a malicious "Firmware Update Service".

**a)** Explain how this attack could succeed.

**b)** Propose three mitigations.

**Answer:**

**a) Attack Scenario:**

**Step 1: Attacker advertises fake service**

- SOME/IP-SD uses multicast (UDP port 30490) to advertise services
- Attacker sends OfferService message:
  
  .. code-block:: text
  
      Service ID: 0x1234 (Firmware Update Service)
      Instance ID: 0x01
      IP Address: 192.168.1.100 (attacker's IP)
      Port: 30500

**Step 2: Legitimate ECU discovers fake service**

- Gateway ECU scans for "Firmware Update Service"
- Finds attacker's advertisement (no authentication in SOME/IP-SD)
- Adds attacker's service to service registry

**Step 3: ECU requests firmware update**

- Gateway ECU sends SOME/IP request to 192.168.1.100:30500
- Attacker responds with malicious firmware
- Gateway installs malicious firmware (if no code signing)

**Result:** Entire vehicle compromised via fake service.

**b) Mitigations:**

**Mitigation 1: SOME/IP-SD Authentication**

- Require digital signatures on SD messages
- Each ECU has X.509 certificate (IEEE 802.1AR DevID)
- SD message includes signature over (Service ID, IP, Port, Timestamp)

.. code-block:: python

    # Pseudo-code for authenticated SD
    sd_message = {
        'service_id': 0x1234,
        'ip': '192.168.1.100',
        'port': 30500,
        'timestamp': int(time.time())
    }
    
    signature = ecu_private_key.sign(json.dumps(sd_message), 'SHA256')
    
    sd_message['signature'] = signature
    sd_message['certificate'] = ecu_certificate
    
    multicast_send(sd_message)

**Verification:**

- Receiver verifies signature using sender's certificate
- Checks certificate against trusted CA
- Rejects unsigned or invalid SD messages

**Mitigation 2: Service Allow-Listing**

- Gateway maintains allow-list of authorized services:
  
  .. code-block:: text
  
      Service ID: 0x1234, IP: 192.168.1.50 (legitimate update server)

- Ignore SD messages for services not in allow-list
- Configure allow-list at factory or via secure OTA update

**Mitigation 3: Network Segmentation**

- Isolate infotainment ECU from safety-critical ECUs
- Gateway filters SOME/IP-SD multicast:
  
  - Infotainment → Gateway: Allow SD for entertainment services only
  - Gateway → Powertrain: Allow SD for control services only

**Mitigation 4: TLS with Mutual Authentication**

- Even if attacker advertises fake service, ECU will not connect without
  valid TLS certificate
- TLS handshake fails (attacker does not have legitimate certificate)

Question 3: Automotive Ethernet Gateway Design (Difficulty: Hard)
------------------------------------------------------------------

Design a secure gateway ECU that connects:

- **CAN Bus** (Powertrain, 500 kbps)
- **Automotive Ethernet** (ADAS cameras, 1 Gbps)
- **LTE Modem** (Remote diagnostics, cellular)

Specify:

**a)** Network segmentation and firewall rules

**b)** MACsec configuration for Ethernet interfaces

**c)** Logging and monitoring strategy

**Answer:**

**a) Network Segmentation & Firewall Rules:**

**Physical Interfaces:**

.. code-block:: text

    Gateway ECU:
    ├─ CAN0 (Powertrain): 192.168.1.0/24
    ├─ ETH0 (ADAS): 192.168.2.0/24
    └─ LTE0 (Cellular): DHCP (public IP)

**Security Zones:**

- **Zone 1 (Powertrain CAN)**: SL-4 (safety-critical)
- **Zone 2 (ADAS Ethernet)**: SL-3 (safety-related)
- **Zone 3 (LTE Modem)**: SL-1 (untrusted)

**Firewall Rules:**

.. code-block:: text

    # LTE → ADAS/Powertrain: DENY ALL (no remote control)
    iptables -A FORWARD -i lte0 -o eth0 -j DROP
    iptables -A FORWARD -i lte0 -o can0 -j DROP
    
    # LTE → Gateway: Allow HTTPS (OTA updates) only
    iptables -A INPUT -i lte0 -p tcp --dport 443 -j ACCEPT
    iptables -A INPUT -i lte0 -j DROP
    
    # ADAS → Powertrain CAN: Allow specific messages only
    # (Implement in application layer, not iptables)
    # Example: ADAS can read vehicle speed (CAN ID 0x161)
    #          ADAS cannot send brake commands
    
    # Powertrain → ADAS: Allow status messages (read-only)
    # Example: Engine RPM (CAN ID 0x100) → Ethernet for display
    
    # Default: DROP all other traffic
    iptables -P FORWARD DROP

**b) MACsec Configuration:**

**ADAS Ethernet (eth0):**

.. code-block:: bash

    # Enable MACsec on eth0
    ip link add link eth0 macsec0 type macsec
    
    # Set encryption (AES-128-GCM)
    ip macsec add macsec0 tx sa 0 pn 1 on key 00 \
      0123456789ABCDEF0123456789ABCDEF
    
    # Set decryption (receive key from peer)
    ip macsec add macsec0 rx address <peer_mac> port 1
    ip macsec add macsec0 rx address <peer_mac> port 1 sa 0 pn 1 on key 01 \
      FEDCBA9876543210FEDCBA9876543210
    
    # Bring up MACsec interface
    ip link set macsec0 up
    ip addr add 192.168.2.1/24 dev macsec0

**Key Management:**

- Pre-shared keys provisioned at factory
- Stored in gateway HSM (Hardware Security Module)
- Key rotation every 30 days (via OTA update)

**c) Logging & Monitoring Strategy:**

**Log Events:**

1. **Firewall denials**:
   
   .. code-block:: bash
   
       iptables -A FORWARD -j LOG --log-prefix "FW_DENY: "

2. **MACsec failures** (ICV verification failed):
   
   - Log to secure storage (tamper-proof)
   - Alert if > 10 failures/minute (potential attack)

3. **SOME/IP service discovery**:
   
   - Log all SD advertisements
   - Detect fake services (unknown IP addresses)

4. **CAN message anomalies**:
   
   - Monitor message frequency (detect bus flooding)
   - Detect unknown CAN IDs

**Monitoring Infrastructure:**

.. code-block:: python

    # Gateway monitoring daemon
    class GatewayMonitor:
        def __init__(self):
            self.alert_threshold = 10  # alerts per minute
            self.alert_count = 0
        
        def monitor_firewall_logs(self):
            """Parse iptables logs and detect attacks"""
            with open('/var/log/kern.log', 'r') as f:
                for line in f:
                    if 'FW_DENY' in line:
                        self.alert_count += 1
                        if self.alert_count > self.alert_threshold:
                            self.trigger_alert("Firewall attack detected")
        
        def monitor_macsec_failures(self):
            """Monitor MACsec decryption failures"""
            # Check kernel MACsec stats
            output = subprocess.check_output(['ip', 'macsec', 'show'])
            if 'decrypt_fail' in output.decode():
                self.trigger_alert("MACsec ICV verification failed")
        
        def trigger_alert(self, message):
            """Send alert to SOC (Security Operations Center)"""
            print(f"[ALERT] {message}")
            # Send to remote SIEM (Security Information and Event Management)
            # over LTE with TLS
            send_siem_alert(message)

**Storage:**

- Logs stored in **secure flash** (encrypted, tamper-evident)
- Uploaded to cloud SOC daily (over LTE with TLS)
- Retention: 90 days (regulatory compliance)

Question 4: TSN Scheduler Manipulation (Difficulty: Hard)
----------------------------------------------------------

An automotive ECU uses IEEE 802.1Qbv Time-Aware Shaper (TAS) with the following
schedule:

.. code-block:: text

    Time Slot 0 (0-1 ms): Priority 7 (Safety-critical ADAS)
    Time Slot 1 (1-2 ms): Priority 5 (Infotainment)
    Time Slot 2 (2-10 ms): Priority 3 (Diagnostics)

An attacker modifies the TAS schedule to:

.. code-block:: text

    Time Slot 0 (0-1 ms): Priority 5 (Infotainment)  ← Changed
    Time Slot 1 (1-2 ms): Priority 7 (ADAS)
    Time Slot 2 (2-10 ms): Priority 3 (Diagnostics)

**a)** What is the safety impact?

**b)** How can the attacker modify the schedule?

**c)** Propose a defense.

**Answer:**

**a) Safety Impact:**

**Before Attack:**

- ADAS safety messages (emergency braking command) sent in Time Slot 0 (0-1 ms)
- Maximum latency: 1 ms
- Safety requirement met (ISO 26262: <10 ms for ASIL-D)

**After Attack:**

- ADAS messages delayed to Time Slot 1 (1-2 ms)
- Infotainment (video streaming) occupies Time Slot 0
- ADAS messages blocked by infotainment traffic
- **Maximum latency: 2 ms** (still acceptable for ASIL-D)
- **BUT**: If infotainment floods the bus, ADAS messages may be delayed further
  (> 10 ms) → **Safety violation**

**Worst Case:**

- Emergency braking command delayed by 50 ms
- Vehicle cannot stop in time → **Accident**

**b) How Attacker Modifies Schedule:**

**Attack Vector 1: Configuration Exploit**

- TAS schedule stored in switch/ECU EEPROM
- Attacker exploits firmware vulnerability (buffer overflow)
- Overwrites TAS schedule in EEPROM
- Switch reboots with malicious schedule

**Attack Vector 2: Management Protocol**

- Some switches use NETCONF/RESTCONF for configuration
- Attacker compromises management interface (weak password)
- Sends new TAS schedule via NETCONF

**Attack Vector 3: Physical Access**

- Attacker connects JTAG debugger to switch
- Directly modifies EEPROM/Flash

**c) Defense:**

**Defense 1: Digitally Sign TAS Configuration**

.. code-block:: c

    // TAS configuration structure
    typedef struct {
        uint32_t time_slot[8];  // Time slot durations (ns)
        uint8_t  priority[8];   // Priority queues for each slot
        uint8_t  signature[64]; // ECDSA P-256 signature
    } tas_config_t;
    
    // Verify TAS configuration at boot
    int verify_tas_config(const tas_config_t *config) {
        // Compute hash of configuration
        uint8_t hash[32];
        sha256((uint8_t*)config, sizeof(tas_config_t) - 64, hash);
        
        // Verify signature using OEM public key
        if (!ecdsa_verify(oem_public_key, hash, config->signature)) {
            printf("ERROR: TAS configuration signature invalid!\n");
            return 0;  // Use default safe configuration
        }
        
        return 1;
    }

**Defense 2: Immutable TAS Configuration**

- Store TAS schedule in **OTP (One-Time Programmable) memory**
- Cannot be modified after factory programming
- Trade-off: Cannot update schedule in field (but safer)

**Defense 3: Hardware-Enforced TAS**

- Use switch with **hardware TAS enforcement**
- TAS schedule stored in secure flash (read-only for firmware)
- Configuration updates require signed firmware update

**Defense 4: Runtime Monitoring**

- Monitor actual transmission times
- Detect if ADAS messages are delayed beyond expected latency
- Alert and failover to backup schedule

Question 5: OTA Update Security (Difficulty: Medium)
-----------------------------------------------------

A vehicle receives an OTA firmware update over LTE → Automotive Ethernet →
Gateway → Target ECU (Powertrain).

**a)** Identify three attack points in this update path.

**b)** For each attack point, propose a mitigation.

**Answer:**

**a) Attack Points:**

**Attack Point 1: LTE Link (Man-in-the-Middle)**

- Attacker intercepts OTA download over cellular network
- Replaces legitimate firmware with malicious version

**Attack Point 2: Gateway ECU (Compromised Gateway)**

- Gateway ECU compromised (previous exploit)
- Attacker modifies firmware before forwarding to Powertrain ECU

**Attack Point 3: Target ECU (Unsigned Firmware Acceptance)**

- Powertrain ECU accepts unsigned firmware
- Attacker bypasses gateway and directly uploads malicious firmware (via OBD-II)

**b) Mitigations:**

**Mitigation 1: LTE Link Protection**

**Use TLS 1.3 with Certificate Pinning:**

.. code-block:: python

    import requests
    
    # Download OTA update over HTTPS
    response = requests.get('https://ota.example.com/firmware.bin',
                            cert=('client.crt', 'client.key'),
                            verify='ca.crt')  # Certificate pinning
    
    firmware = response.content
    
    # Verify firmware signature before installation
    if not verify_signature(firmware, 'firmware.sig'):
        raise Exception("Firmware signature invalid!")

**Benefit:** TLS encrypts and authenticates download, preventing MITM.

**Mitigation 2: Gateway Integrity Protection**

**Runtime Integrity Monitoring:**

- Gateway periodically verifies its own firmware integrity
- Compute HMAC-SHA256 of firmware, compare with known-good value
- If mismatch: Gateway enters fail-safe mode, refuses to forward updates

.. code-block:: c

    int verify_gateway_integrity(void) {
        extern uint8_t _firmware_start[];
        extern uint8_t _firmware_end[];
        
        uint8_t calculated_hmac[32];
        hmac_sha256(hmac_key, _firmware_start, 
                    _firmware_end - _firmware_start, calculated_hmac);
        
        if (memcmp(calculated_hmac, expected_hmac, 32) != 0) {
            printf("Gateway firmware tampered!\n");
            return 0;
        }
        return 1;
    }

**Mitigation 3: Target ECU Secure Boot & Code Signing**

**Require Digital Signature:**

- OTA firmware package includes:
  
  - Firmware binary
  - RSA-2048 or ECDSA P-256 signature (signed by OEM private key)

- Powertrain ECU verifies signature before flashing:

.. code-block:: c

    int install_ota_update(const uint8_t *firmware, size_t size,
                           const uint8_t *signature) {
        // Verify signature
        if (!verify_firmware_signature(firmware, size, signature)) {
            printf("OTA update signature invalid! Rejecting.\n");
            return -1;
        }
        
        // Signature valid - flash firmware
        flash_write(FIRMWARE_ADDR, firmware, size);
        
        // Reboot to apply update
        system_reset();
        return 0;
    }

**Additional Layer: A/B Partitioning**

- Maintain two firmware partitions (A and B)
- Install update to inactive partition
- On reboot: Verify new partition, switch if valid
- If verification fails: Rollback to previous partition

Conclusion
==========

Automotive Ethernet provides high bandwidth for ADAS, infotainment, and OTA
updates, but introduces security challenges. Key protections include:

1. **MACsec (IEEE 802.1AE)**: Link-layer encryption with AES-GCM
2. **SOME/IP over TLS**: Application-layer security for service-oriented communication
3. **TSN (IEEE 802.1Qbv)**: Time-aware scheduling with integrity protection
4. **DoIP with Authentication**: Secure diagnostics over IP
5. **Network Segmentation**: Gateway firewall between domains

**Compliance:**

- ISO 21434: Cybersecurity engineering for road vehicles
- IEEE 802.1AE: MACsec standard
- IEEE 802.1AS: Time synchronization (gPTP)

References
==========

- IEEE 802.1AE-2018: Media Access Control (MAC) Security
- IEEE 802.1AS-2020: Timing and Synchronization for Time-Sensitive Applications
- AUTOSAR: Specification of SOME/IP Protocol
- ISO 13400: Road vehicles - Diagnostic communication over Internet Protocol (DoIP)
- BroadR-Reach Physical Layer Specification (Broadcom)

**END OF DOCUMENT**
