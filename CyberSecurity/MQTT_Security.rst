====================================================================
MQTT Security - Message Queue Telemetry Transport
====================================================================

:Author: Cybersecurity Expert
:Date: January 2026
:Version: 1.0
:Standards: OASIS MQTT 5.0, ISO 20922

.. contents:: Table of Contents
   :depth: 2

TL;DR - Quick Reference
=======================

**MQTT Overview:**

- **Purpose:** Lightweight pub/sub messaging for IoT
- **Port:** TCP 1883 (plaintext), 8883 (TLS)
- **Quality of Service:** QoS 0 (fire-and-forget), QoS 1 (at least once), QoS 2 (exactly once)

**Security Mechanisms:**

✅ **TLS encryption:** Protect data in transit
✅ **Username/password auth:** Basic authentication
✅ **Client certificates:** Mutual TLS (preferred)
✅ **ACLs (Access Control Lists):** Topic-based authorization

Introduction
============

**MQTT (Message Queue Telemetry Transport)** is used in IoT, smart home, industrial sensors, and automotive telemetry.

**Publish/Subscribe Model:**

.. code-block:: text

    Publisher (Temperature Sensor)
           ↓ publish("sensors/temp", "72°F")
    MQTT Broker (Mosquitto, HiveMQ)
           ↓ forward to subscribers
    Subscriber (HVAC Controller)

MQTT Security Threats
======================

**Threat 1: Eavesdropping (No TLS)**

.. code-block:: python

    # Attacker sniffs MQTT traffic on port 1883
    from scapy.all import sniff
    
    def mqtt_sniffer(packet):
        if packet.haslayer('TCP') and packet['TCP'].dport == 1883:
            payload = str(packet['TCP'].payload)
            if 'sensors/temp' in payload:
                print(f"[INTERCEPTED] {payload}")
    
    sniff(filter="tcp port 1883", prn=mqtt_sniffer)

**Threat 2: Unauthorized Publishing**

.. code-block:: python

    # Attacker publishes false sensor data
    import paho.mqtt.client as mqtt
    
    client = mqtt.Client()
    client.connect("mqtt-broker.example.com", 1883)
    
    # Publish fake temperature (causes HVAC malfunction)
    client.publish("sensors/temp", "150°F")  # Actual: 72°F

**Threat 3: Topic Wildcard Abuse**

.. code-block:: python

    # Attacker subscribes to ALL topics
    client.subscribe("#")  # Wildcard: receive all messages
    
    # Can spy on:
    # - sensors/temp
    # - actuators/valve/control
    # - admin/firmware/update

TLS Encryption for MQTT
=========================

**Server-Side: Configure Mosquitto Broker**

.. code-block:: text

    # /etc/mosquitto/mosquitto.conf
    
    listener 8883
    cafile /etc/mosquitto/ca.crt
    certfile /etc/mosquitto/server.crt
    keyfile /etc/mosquitto/server.key
    
    # Require TLS 1.3
    tls_version tlsv1.3
    
    # Disable plaintext port 1883
    # listener 1883

**Client-Side: Python with TLS**

.. code-block:: python

    import paho.mqtt.client as mqtt
    import ssl
    
    client = mqtt.Client()
    
    # Configure TLS
    client.tls_set(
        ca_certs="ca.crt",
        certfile="client.crt",
        keyfile="client.key",
        tls_version=ssl.PROTOCOL_TLSv1_3
    )
    
    # Connect to TLS port
    client.connect("mqtt-broker.example.com", 8883)
    
    # Publish (encrypted)
    client.publish("sensors/temp", "72°F")

Authentication Mechanisms
==========================

**1. Username/Password (Basic)**

.. code-block:: python

    # Client authentication
    client.username_pw_set("sensor_001", "SecurePassword123")
    client.connect("mqtt-broker.example.com", 8883)

**Mosquitto password file:**

.. code-block:: bash

    # Create password file
    mosquitto_passwd -c /etc/mosquitto/passwd sensor_001
    # Enter password when prompted
    
    # Add to mosquitto.conf
    password_file /etc/mosquitto/passwd

**2. Client Certificates (Mutual TLS - Preferred)**

.. code-block:: text

    # mosquitto.conf
    require_certificate true
    use_identity_as_username true

**Embedded C Client (mbedTLS):**

.. code-block:: c

    #include <mbedtls/ssl.h>
    #include <MQTTClient.h>
    
    void mqtt_connect_tls(void) {
        MQTTClient client;
        MQTTClient_SSLOptions ssl_opts = MQTTClient_SSLOptions_initializer;
        
        ssl_opts.trustStore = "ca.crt";
        ssl_opts.keyStore = "client.crt";
        ssl_opts.privateKey = "client.key";
        ssl_opts.enabledCipherSuites = "TLS_AES_256_GCM_SHA384";
        
        MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
        conn_opts.ssl = &ssl_opts;
        
        MQTTClient_create(&client, "ssl://mqtt-broker:8883", "sensor_001",
                          MQTTCLIENT_PERSISTENCE_NONE, NULL);
        
        MQTTClient_connect(client, &conn_opts);
    }

Topic-Based Access Control (ACL)
==================================

**Mosquitto ACL File:**

.. code-block:: text

    # /etc/mosquitto/acl
    
    # Temperature sensors can only publish to sensors/temp
    user sensor_001
    topic write sensors/temp/#
    
    # HVAC controller can read sensors and write to actuators
    user hvac_controller
    topic read sensors/#
    topic write actuators/hvac/#
    
    # Admin can access everything
    user admin
    topic readwrite #

**Testing ACL:**

.. code-block:: python

    # sensor_001 tries to publish to admin topic
    client.username_pw_set("sensor_001", "password")
    client.connect("mqtt-broker", 8883)
    
    # This will be rejected by ACL
    result = client.publish("admin/firmware/update", "malicious_payload")
    # Result: MQTT_ERR_ACL

Enhanced Authentication (MQTT 5.0)
====================================

**SCRAM (Salted Challenge Response Authentication):**

.. code-block:: python

    # MQTT 5.0 with SCRAM-SHA-256
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    
    client.username_pw_set(
        username="sensor_001",
        password="SecurePassword123"
    )
    
    # Broker configuration (mosquitto.conf)
    # auth_plugin /usr/lib/mosquitto_scram.so
    # password_file /etc/mosquitto/scram_passwords

**Benefits:**

- Password never sent in plaintext (even over TLS)
- Resistant to replay attacks
- Salted hashes stored on broker

Exam Questions
==============

**Q1: MQTT vs HTTPS for IoT (Medium)**

Compare MQTT and HTTPS for sensor data transmission. When to use each?

**Answer:**

+----------------------+---------------------------+---------------------------+
| Feature              | MQTT                      | HTTPS                     |
+======================+===========================+===========================+
| Protocol             | Pub/Sub                   | Request/Response          |
+----------------------+---------------------------+---------------------------+
| Overhead             | Low (2-byte header)       | High (HTTP headers)       |
+----------------------+---------------------------+---------------------------+
| Battery life         | ✅ Better (keep-alive)    | ⚠️  Worse (reconnect)     |
+----------------------+---------------------------+---------------------------+
| Real-time            | ✅ Push notifications     | ❌ Polling required       |
+----------------------+---------------------------+---------------------------+
| Security             | TLS + ACLs                | TLS + API auth            |
+----------------------+---------------------------+---------------------------+

**Use MQTT for:**
- Constrained devices (low power, bandwidth)
- Real-time updates (sensor → cloud → actuator)
- Many-to-many communication

**Use HTTPS for:**
- RESTful APIs (CRUD operations)
- Web dashboards
- Strong authentication (OAuth 2.0)

**Q2: MQTT Retained Messages Security (Hard)**

MQTT allows "retained messages" (last message stored on broker for new subscribers). What are the security implications?

**Answer:**

**Security Risks:**

1. **Stale data attack:**
   - Attacker publishes malicious retained message
   - Even after disconnection, new clients receive it
   - Example: "sensors/fire_alarm" → "no_alarm" (retained)

2. **Sensitive data exposure:**
   - Password or key published as retained message
   - Persists on broker indefinitely
   - Any subscriber can retrieve

3. **Denial of Service:**
   - Publish large retained message (1 MB)
   - Broker runs out of memory
   - Legitimate messages rejected

**Mitigations:**

.. code-block:: python

    # 1. Clear retained messages after use
    client.publish("sensors/temp", None, retain=True)  # Delete retained
    
    # 2. Set message expiry (MQTT 5.0)
    properties = mqtt.Properties()
    properties.MessageExpiryInterval = 3600  # 1 hour
    client.publish("sensors/temp", "72°F", properties=properties)
    
    # 3. Restrict retained messages in ACL
    # /etc/mosquitto/acl
    # user sensor_001
    # topic write sensors/temp (no retain allowed)

**Best Practice:** Avoid retained messages for security-critical topics.

Standards
=========

- **OASIS MQTT 5.0:** Enhanced authentication, message expiry
- **ISO 20922:** MQTT 3.1.1 standard
- **RFC 6749:** OAuth 2.0 (for MQTT authentication)

**END OF DOCUMENT**
