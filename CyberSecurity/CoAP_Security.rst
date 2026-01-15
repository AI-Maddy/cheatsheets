====================================================================
CoAP Security - Constrained Application Protocol
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: RFC 7252, RFC 7925 (DTLS for IoT)

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**CoAP:**

- **Purpose:** Lightweight HTTP for IoT (constrained devices)
- **Transport:** UDP (port 5683), DTLS (port 5684)
- **Methods:** GET, POST, PUT, DELETE (like HTTP)

**Security:**

✅ **DTLS 1.2/1.3:** Encryption and authentication
✅ **Pre-shared keys (PSK):** Lightweight crypto
✅ **Certificate-based:** For more secure deployments

Introduction
============

**CoAP** is used in smart home, industrial sensors, and low-power networks.

**Vulnerability:** CoAP over UDP (no encryption) → eavesdropping, spoofing.

CoAP with DTLS
===============

.. code-block:: python

    from aiocoap import *
    import ssl
    
    async def coap_secure_request():
        # Create DTLS context
        context = await Context.create_client_context()
        
        # CoAPS (DTLS) request
        request = Message(code=GET, uri='coaps://sensor.local/temperature')
        
        # Send encrypted request
        response = await context.request(request).response
        print(f"Temperature: {response.payload.decode()}")

**Embedded C Client (tinydtls):**

.. code-block:: c

    #include <tinydtls.h>
    #include <coap.h>
    
    void coap_dtls_get(const char *server, const char *resource) {
        dtls_context_t *dtls_ctx;
        coap_context_t *coap_ctx;
        
        // Initialize DTLS with PSK
        uint8_t psk_key[16] = {...};
        dtls_set_psk(dtls_ctx, psk_key, 16);
        
        // Create CoAP GET request
        coap_pdu_t *request = coap_new_pdu(COAP_MESSAGE_CON, COAP_REQUEST_GET, coap_new_message_id());
        coap_add_option(request, COAP_OPTION_URI_PATH, strlen(resource), resource);
        
        // Send via DTLS
        dtls_send(dtls_ctx, request);
    }

**Attack: CoAP Amplification (DDoS)**

.. code-block:: python

    # Attacker spoofs source IP → victim receives amplified traffic
    
    import socket
    
    def coap_amplification_attack(coap_servers, victim_ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for server in coap_servers:
            # CoAP GET request (4 bytes) → response (1000+ bytes)
            coap_request = b'\x40\x01\x00\x00'  # Minimal CoAP GET
            
            # Spoof source IP to victim
            sock.sendto(coap_request, (server, 5683))
            # Server sends large response to victim (amplification factor: 250×)

**Defense: Rate Limiting**

.. code-block:: c

    // Limit CoAP responses per IP
    #define MAX_RESPONSES_PER_MINUTE 60
    
    int process_coap_request(coap_pdu_t *request, struct sockaddr *src_addr) {
        // Track request count per IP
        uint32_t count = get_request_count(src_addr);
        
        if (count > MAX_RESPONSES_PER_MINUTE) {
            // Drop request (possible amplification attack)
            return -1;
        }
        
        increment_request_count(src_addr);
        return coap_handle_request(request);
    }

Exam Questions
==============

**Q1: CoAP vs HTTPS for Sensors (Medium)**

Compare CoAP/DTLS and HTTPS for battery-powered temperature sensors.

**Answer:**

+-------------------+-------------------------+------------------------+
| Feature           | CoAP/DTLS               | HTTPS                  |
+===================+=========================+========================+
| Overhead          | 4-byte header           | 100+ byte headers      |
+-------------------+-------------------------+------------------------+
| Transport         | UDP (stateless)         | TCP (connection state) |
+-------------------+-------------------------+------------------------+
| Battery life      | ✅ 2× better            | ⚠️  Worse              |
+-------------------+-------------------------+------------------------+

**Recommendation:** CoAP/DTLS for constrained devices.

Standards
=========

- **RFC 7252:** CoAP specification
- **RFC 7925:** DTLS profile for IoT

**END OF DOCUMENT**
