====================================================================
BACnet/SC Deep Dive - BACnet Secure Connect
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: ASHRAE 135-2020, ISO 16484-5

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**BACnet/SC (Secure Connect):**

- **Purpose:** Secure replacement for legacy BACnet/IP
- **Transport:** WebSocket over TLS 1.3
- **Port:** TCP 443 (HTTPS) or 47808
- **Features:** Certificate-based auth, encryption, firewall-friendly

**Migration Path:**

.. code-block:: text

    Legacy BACnet/IP (UDP 47808, plaintext)
           ↓
    BACnet/SC Hub (gateway for legacy devices)
           ↓
    Full BACnet/SC (all devices support TLS)

Introduction
============

**BACnet (Building Automation and Control Network)** is used in HVAC, lighting, fire, and security systems.

**Legacy BACnet Vulnerabilities:**

- **No encryption:** Attacker sniffs temperature setpoints
- **No authentication:** Spoofed commands (e.g., "disable fire alarm")
- **UDP broadcast:** Easy to inject malicious packets

**BACnet/SC Solution:**

- TLS 1.3 encryption (AES-256-GCM)
- X.509 certificate authentication
- WebSocket (firewall-friendly, NAT traversal)

BACnet/SC Architecture
=======================

.. code-block:: text

    ┌─────────────────┐
    │ BACnet/SC Hub   │ (Central certificate authority)
    │ ├─ Issue certs  │
    │ └─ Route msgs   │
    └────────┬────────┘
             │ TLS 1.3 (port 443)
        ┌────┴────┬────────────┐
        │         │            │
    ┌───▼───┐ ┌──▼──┐  ┌──────▼─────┐
    │ HVAC  │ │ VAV │  │ Thermostat │
    │ Unit  │ │ Box │  │            │
    └───────┘ └─────┘  └────────────┘
    (All devices have X.509 certificates)

Certificate Provisioning
=========================

**Step 1: Device Certificate Request**

.. code-block:: python

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    
    # Generate device key pair
    private_key = ec.generate_private_key(ec.SECP256R1())
    
    # Create CSR (Certificate Signing Request)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, u"HVAC-Zone1-Controller"),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, u"Building-A"),
    ])).sign(private_key, hashes.SHA256())
    
    # Send CSR to BACnet/SC Hub
    response = requests.post('https://bacnet-hub/api/certificate', data=csr.public_bytes())

**Step 2: Hub Issues Certificate**

.. code-block:: python

    # Hub signs CSR with CA private key
    from datetime import datetime, timedelta
    
    cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(ca_private_key, hashes.SHA256())
    
    return cert

TLS 1.3 Connection Establishment
==================================

**C Implementation (mbedTLS):**

.. code-block:: c

    #include <mbedtls/ssl.h>
    #include <mbedtls/net_sockets.h>
    
    void bacnet_sc_connect(const char *hub_address) {
        mbedtls_ssl_context ssl;
        mbedtls_ssl_config conf;
        mbedtls_x509_crt cacert, device_cert;
        mbedtls_pk_context device_key;
        
        // Load device certificate and key
        mbedtls_x509_crt_parse_file(&device_cert, "device.crt");
        mbedtls_pk_parse_keyfile(&device_key, "device.key", NULL);
        
        // Load CA certificate (to verify hub)
        mbedtls_x509_crt_parse_file(&cacert, "ca.crt");
        
        // Configure TLS 1.3
        mbedtls_ssl_config_defaults(&conf, MBEDTLS_SSL_IS_CLIENT,
            MBEDTLS_SSL_TRANSPORT_STREAM, MBEDTLS_SSL_PRESET_DEFAULT);
        
        mbedtls_ssl_conf_min_version(&conf, MBEDTLS_SSL_MAJOR_VERSION_3,
            MBEDTLS_SSL_MINOR_VERSION_4);  // TLS 1.3
        
        // Mutual TLS: client and server authenticate
        mbedtls_ssl_conf_authmode(&conf, MBEDTLS_SSL_VERIFY_REQUIRED);
        mbedtls_ssl_conf_ca_chain(&conf, &cacert, NULL);
        mbedtls_ssl_conf_own_cert(&conf, &device_cert, &device_key);
        
        // Connect
        mbedtls_net_context server_fd;
        mbedtls_net_connect(&server_fd, hub_address, "443", MBEDTLS_NET_PROTO_TCP);
        
        mbedtls_ssl_setup(&ssl, &conf);
        mbedtls_ssl_set_bio(&ssl, &server_fd, mbedtls_net_send, mbedtls_net_recv, NULL);
        
        // TLS handshake
        int ret = mbedtls_ssl_handshake(&ssl);
        if (ret == 0) {
            printf("BACnet/SC connection established\n");
        }
    }

WebSocket Messaging
====================

**BACnet message over WebSocket:**

.. code-block:: python

    import websocket
    
    def send_bacnet_command(ws, command):
        # BACnet/SC message format
        message = {
            'type': 'BVLC',  # BACnet Virtual Link Control
            'function': 'OriginalUnicastNPDU',
            'data': encode_bacnet_apdu(command)
        }
        
        # Send over WebSocket (encrypted by TLS)
        ws.send(json.dumps(message))

**Example: Change temperature setpoint**

.. code-block:: python

    # Secure command to set HVAC temperature to 72°F
    command = {
        'object_type': 'ANALOG_VALUE',
        'object_instance': 1,
        'property': 'PRESENT_VALUE',
        'value': 72.0
    }
    
    ws = websocket.create_connection('wss://bacnet-hub/device/HVAC-Zone1')
    send_bacnet_command(ws, command)
    ws.close()

Migration from Legacy BACnet
==============================

**Phase 1: BACnet/SC Hub as Gateway**

.. code-block:: text

    Legacy Devices (BACnet/IP UDP)
           ↓
    BACnet/SC Hub
           ├─ Listens on UDP 47808 (legacy)
           ├─ Listens on TCP 443 (BACnet/SC)
           └─ Translates between protocols
           ↓
    Modern BACnet/SC Devices (TLS)

**Phase 2: Gradual Device Upgrade**

- Replace devices during normal maintenance cycles
- Prioritize critical systems (fire, security)
- Maintain legacy support for 5-10 years

Exam Questions
==============

**Q1: BACnet/SC vs VPN (Medium)**

Compare BACnet/SC to deploying legacy BACnet over VPN. What are the trade-offs?

**Answer:**

+-------------------------+---------------------------+------------------------+
| Feature                 | BACnet/SC                 | BACnet/IP over VPN     |
+=========================+===========================+========================+
| Encryption              | ✅ Per-device (TLS 1.3)   | ✅ Tunnel-level        |
+-------------------------+---------------------------+------------------------+
| Authentication          | ✅ Certificate-based      | ❌ Shared VPN key      |
+-------------------------+---------------------------+------------------------+
| Firewall traversal      | ✅ WebSocket (port 443)   | ⚠️  VPN port blocking  |
+-------------------------+---------------------------+------------------------+
| Device compromise       | ✅ Isolated (per cert)    | ❌ Full VPN access     |
+-------------------------+---------------------------+------------------------+
| Complexity              | ⚠️  Certificate mgmt      | ✅ Standard VPN        |
+-------------------------+---------------------------+------------------------+

**Best Practice:** BACnet/SC for new deployments. VPN for quick legacy protection.

**Q2: Certificate Revocation (Hard)**

A thermostat's private key is compromised. How to revoke its certificate in BACnet/SC network?

**Answer:**

**Step 1: Add to CRL (Certificate Revocation List)**

.. code-block:: python

    # Hub generates CRL
    crl = x509.CertificateRevocationListBuilder().issuer_name(
        ca_cert.subject
    ).last_update(
        datetime.utcnow()
    ).next_update(
        datetime.utcnow() + timedelta(days=1)
    ).add_revoked_certificate(
        x509.RevokedCertificateBuilder()
        .serial_number(compromised_cert_serial)
        .revocation_date(datetime.utcnow())
        .build()
    ).sign(ca_private_key, hashes.SHA256())

**Step 2: Distribute CRL to all devices**

- Push update via BACnet/SC Hub
- Devices check CRL before accepting connections

**Step 3: Re-provision device**

- Generate new key pair
- Issue new certificate
- Update device firmware/config

Standards
=========

- **ASHRAE 135-2020:** BACnet/SC specification
- **ISO 16484-5:** Building automation protocols
- **RFC 6455:** WebSocket protocol

**END OF DOCUMENT**
