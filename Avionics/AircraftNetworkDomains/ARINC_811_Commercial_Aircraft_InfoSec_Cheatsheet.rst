🔐 **ARINC 811 — Commercial Aircraft Information Security Concepts**
═══════════════════════════════════════════════════════════════════════

**Context:** Network security guidelines for commercial aviation systems
**Standard:** ARINC Specification 811 (2005, updated 2010)
**Scope:** Domain isolation, firewall requirements, access control, secure protocols
**Applies To:** Commercial aircraft (Boeing, Airbus, regional jets)

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — ARINC 811 IN 60 SECONDS**
───────────────────────────────────────

**What is ARINC 811?**

::

    ARINC 811 = Network security architecture for commercial aircraft
    
    Purpose: Define security baseline for avionics networks to prevent
             unauthorized access between domains (ACD, AISD, PIESD)

**Core Principles:**

+----------------------------------+--------------------------------+
| **Principle**                    | **Implementation**             |
+==================================+================================+
| Domain Isolation                 | Physical separation + firewall |
+----------------------------------+--------------------------------+
| Defense in Depth                 | Multiple security layers       |
+----------------------------------+--------------------------------+
| Least Privilege                  | Minimal access rights          |
+----------------------------------+--------------------------------+
| Secure by Default                | Deny all unless explicit allow |
+----------------------------------+--------------------------------+

**Key Requirements:**

::

    1. Network Segmentation: ACD ⇄ AISD ⇄ PIESD (isolated)
    2. Firewall: Stateful inspection + deep packet inspection
    3. Access Control: Authentication + authorization + audit
    4. Cryptography: TLS 1.2+ for all external connections
    5. Monitoring: Real-time intrusion detection

════════════════════════════════════════════════════════════════════

📖 **1. DOMAIN ISOLATION REQUIREMENTS**
═══════════════════════════════════════

**1.1 Three-Domain Architecture**
---------------------------------

**ARINC 811 Domain Model:**

::

    ┌─────────────────────────────────────────────┐
    │  🔴 Aircraft Control Domain (ACD)           │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Flight-critical systems                    │
    │  - Flight Control Computer (FCC)            │
    │  - FADEC (Engine control)                   │
    │  - Navigation (FMS, ADIRS)                  │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Security: Air gap + Data diode             │
    │  Isolation: Physical + Logical              │
    │  Internet: ❌ NEVER                         │
    └─────────────────────────────────────────────┘
              │ (One-way data diode)
              ↓
    ┌─────────────────────────────────────────────┐
    │  🟡 Airline Information Services (AISD)     │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Crew & operational systems                 │
    │  - Electronic Flight Bag (EFB)              │
    │  - Central Maintenance Computer (CMC)       │
    │  - ACARS (messaging)                        │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Security: Firewall + VPN                   │
    │  Isolation: VLAN + ACL                      │
    │  Internet: ⚠️ Ground link only (encrypted)  │
    └─────────────────────────────────────────────┘
              │ (Firewall + sanitization)
              ↓
    ┌─────────────────────────────────────────────┐
    │  🟢 Passenger Info & Entertainment (PIESD)  │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Passenger-facing systems                   │
    │  - In-Flight Entertainment (IFE)            │
    │  - Passenger Wi-Fi                          │
    │  - Live TV / Connectivity                   │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
    │  Security: Basic firewall + rate limit      │
    │  Isolation: Separate switches               │
    │  Internet: ✅ YES (satellite)               │
    └─────────────────────────────────────────────┘

**1.2 Isolation Mechanisms**
----------------------------

**Physical Isolation (ACD):**

.. code-block:: text

    Requirements:
    - Separate cabling (no shared conduits)
    - Dedicated switches/routers
    - Locked avionics bays (physical access control)
    - Tamper-evident seals
    
    Verification:
    - Visual inspection (cable routing)
    - Physical penetration testing
    - Lockdown procedure audit

**Logical Isolation (AISD ↔ PIESD):**

.. code-block:: text

    Requirements:
    - VLAN segmentation (802.1Q)
    - Firewall between domains (stateful)
    - No direct routing (all traffic via firewall)
    - ACL enforcement (deny by default)
    
    Verification:
    - Network scan (Nmap) from PIESD → AISD (should fail)
    - Firewall rule audit
    - VLAN hopping test (should be blocked)

**1.3 Data Flow Control**
-------------------------

**Allowed Data Paths:**

+-------------+---------+---------+---------+
| From ↓ / To | ACD     | AISD    | PIESD   |
+=============+=========+=========+=========+
| **ACD**     | ✅ Yes  | ✅ Yes  | ❌ NO   |
|             | (Self)  | (1-way) |         |
+-------------+---------+---------+---------+
| **AISD**    | ❌ NO   | ✅ Yes  | ⚠️ GPS  |
|             |         | (Self)  | (sanit.)|
+-------------+---------+---------+---------+
| **PIESD**   | ❌ NO   | ❌ NO   | ✅ Yes  |
|             |         |         | (Self)  |
+-------------+---------+---------+---------+

**Data Sanitization (ACD → AISD → PIESD):**

.. code-block:: python

    # data_sanitization.py
    
    def sanitize_gps_for_moving_map(raw_gps):
        """
        Sanitize GPS data before sending to passenger IFE
        Per ARINC 811: Remove precise position data
        """
        
        # Raw data from ACD (precise)
        # Latitude: 37.7749291° N (±1 meter accuracy)
        # Longitude: -122.4194155° W
        # Altitude: 35,247 ft
        # Ground Speed: 487 knots
        # Track: 085° true
        
        # Sanitized data for PIESD (low resolution)
        sanitized = {
            'latitude': round(raw_gps['latitude'], 1),    # ±10 km
            'longitude': round(raw_gps['longitude'], 1),
            'altitude': round(raw_gps['altitude'], -3),   # Round to nearest 1000 ft
            'ground_speed': None,  # Do NOT expose (security)
            'track': round(raw_gps['track'], -1)  # Round to nearest 10°
        }
        
        # Result:
        # Latitude: 37.8° N (low precision)
        # Longitude: -122.4° W
        # Altitude: 35,000 ft
        # Ground Speed: REDACTED
        # Track: 090° (rounded)
        
        return sanitized

════════════════════════════════════════════════════════════════════

📖 **2. FIREWALL REQUIREMENTS**
═══════════════════════════════

**2.1 Firewall Architecture**
-----------------------------

**ARINC 811 Firewall Specification:**

+----------------------------+----------------------------------+
| **Requirement**            | **Specification**                |
+============================+==================================+
| Type                       | Stateful packet inspection (SPI) |
+----------------------------+----------------------------------+
| Position                   | Between AISD ↔ PIESD             |
+----------------------------+----------------------------------+
| Default Policy             | DENY ALL (explicit allow only)   |
+----------------------------+----------------------------------+
| Logging                    | All denied connections           |
+----------------------------+----------------------------------+
| Inspection Depth           | Layer 3-7 (application-aware)    |
+----------------------------+----------------------------------+
| Redundancy                 | Active-standby (failover <1 sec) |
+----------------------------+----------------------------------+
| Performance                | ≥1 Gbps throughput               |
+----------------------------+----------------------------------+

**Firewall Topology:**

::

    ┌──────────────────────────────────────────┐
    │          AISD Network                    │
    │  (Crew, Maintenance, Operations)         │
    └──────────────┬───────────────────────────┘
                   │
                   ↓
    ┌──────────────────────────────────────────┐
    │      Firewall (Stateful + DPI)           │
    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
    │  Rules:                                  │
    │  1. ALLOW AISD → PIESD (GPS data, port   │
    │     5000/UDP, sanitized)                 │
    │  2. DENY PIESD → AISD (all traffic)      │
    │  3. LOG all denied attempts              │
    │  4. Rate limit: 10 Mbps per passenger    │
    └──────────────┬───────────────────────────┘
                   │
                   ↓
    ┌──────────────────────────────────────────┐
    │         PIESD Network                    │
    │  (Passenger Wi-Fi, IFE, Entertainment)   │
    └──────────────────────────────────────────┘

**2.2 Firewall Rule Set**
-------------------------

**Example Configuration (iptables):**

.. code-block:: bash

    #!/bin/bash
    # ARINC 811 Compliant Firewall Rules
    
    # Flush existing rules
    iptables -F
    iptables -X
    
    # Default policy: DENY ALL
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
    
    # Allow loopback
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
    
    # RULE 1: ALLOW AISD → PIESD (GPS data only)
    iptables -A FORWARD -s 10.20.0.0/16 -d 10.30.0.0/16 \
      -p udp --dport 5000 \
      -m comment --comment "AISD-to-PIESD: Sanitized GPS" \
      -j ACCEPT
    
    # RULE 2: DENY PIESD → AISD (all traffic)
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.20.0.0/16 \
      -m comment --comment "BLOCK PIESD-to-AISD" \
      -j LOG --log-prefix "FIREWALL-BLOCK-PIESD: " --log-level 4
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.20.0.0/16 -j REJECT
    
    # RULE 3: DENY PIESD → ACD (double protection)
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.10.0.0/16 \
      -m comment --comment "BLOCK PIESD-to-ACD" \
      -j LOG --log-prefix "FIREWALL-BLOCK-CRITICAL: " --log-level 1
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.10.0.0/16 -j REJECT
    
    # RULE 4: Rate limiting (per passenger device)
    iptables -A FORWARD -s 10.30.0.0/16 \
      -m hashlimit --hashlimit-above 10mb/s --hashlimit-mode srcip \
      --hashlimit-name passenger_rate_limit \
      -j LOG --log-prefix "RATE-LIMIT-EXCEEDED: "
    iptables -A FORWARD -s 10.30.0.0/16 \
      -m hashlimit --hashlimit-above 10mb/s --hashlimit-mode srcip \
      --hashlimit-name passenger_rate_limit \
      -j DROP
    
    # RULE 5: Allow established/related connections
    iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    # RULE 6: Log all other denied traffic
    iptables -A FORWARD -j LOG --log-prefix "FIREWALL-DENY: " --log-level 4
    iptables -A FORWARD -j REJECT
    
    # Save rules
    iptables-save > /etc/iptables/rules.v4
    
    echo "✅ ARINC 811 firewall rules applied"

**2.3 Deep Packet Inspection (DPI)**
------------------------------------

**DPI Requirements:**

.. code-block:: yaml

    # dpi_config.yaml
    
    inspection_rules:
      
      # HTTP/HTTPS inspection
      http:
        - inspect_headers: true
        - block_patterns:
          - "User-Agent: *sqlmap*"  # SQL injection tool
          - "User-Agent: *nikto*"   # Web scanner
        - rate_limit: 100 requests/min per IP
      
      # DNS inspection
      dns:
        - block_domains:
          - "*.malware.com"
          - "*.phishing.net"
        - rate_limit: 50 queries/min per IP
      
      # FTP inspection (block uploads from PIESD)
      ftp:
        - block_commands: ["STOR", "PUT"]
        - allow_commands: ["LIST", "RETR"]
      
      # SSH inspection
      ssh:
        - whitelist_keys: ["/etc/ssh/authorized_keys"]
        - block_password_auth: true
        - alert_on_failed_login: 3 attempts
      
      # Custom protocol (ARINC 664 AFDX)
      afdx:
        - validate_virtual_link_id: true
        - check_bag_compliance: true  # Bandwidth Allocation Gap
        - drop_invalid_frames: true

════════════════════════════════════════════════════════════════════

📖 **3. ACCESS CONTROL**
════════════════════════

**3.1 Authentication Requirements**
-----------------------------------

**ARINC 811 Authentication Matrix:**

+------------------+------------------+------------------------+
| **Domain**       | **User Type**    | **Authentication**     |
+==================+==================+========================+
| ACD              | Maintenance      | Physical key + 2-person|
|                  | (avionics bay)   | rule                   |
+------------------+------------------+------------------------+
| AISD             | Pilot/Crew       | Username + password    |
|                  |                  | (8+ chars)             |
+------------------+------------------+------------------------+
| AISD             | Maintenance      | Multi-factor auth (MFA)|
|                  | (USB upload)     | (token + biometric)    |
+------------------+------------------+------------------------+
| PIESD            | Passenger        | Captive portal (email) |
|                  |                  | + payment              |
+------------------+------------------+------------------------+

**Multi-Factor Authentication (MFA) Example:**

.. code-block:: python

    # mfa_authentication.py
    
    import pyotp
    import hashlib
    
    def authenticate_maintenance_technician(username, password, totp_token):
        """
        MFA for AISD maintenance access (ARINC 811 SAL 2)
        """
        
        # Factor 1: Username + Password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if not verify_password_hash(username, password_hash):
            log_failed_login(username, "Invalid password")
            return False
        
        # Factor 2: Time-based One-Time Password (TOTP)
        totp = pyotp.TOTP(get_user_secret(username))
        
        if not totp.verify(totp_token, valid_window=1):
            log_failed_login(username, "Invalid TOTP token")
            return False
        
        # Factor 3: Biometric (fingerprint) - hardware device
        if not verify_fingerprint(username):
            log_failed_login(username, "Biometric mismatch")
            return False
        
        # All factors passed
        log_successful_login(username)
        create_session(username, timeout_minutes=15)
        return True

**3.2 Authorization (RBAC)**
---------------------------

**Role-Based Access Control:**

.. code-block:: yaml

    # rbac_policy.yaml
    
    roles:
      
      pilot:
        permissions:
          - read: [efb_charts, weather, flight_plan]
          - write: [flight_log]
          - execute: [send_acars_message]
        domains: [AISD]
      
      flight_attendant:
        permissions:
          - read: [cabin_status, passenger_manifest]
          - write: [service_log]
          - execute: [cabin_announcement]
        domains: [AISD]
      
      maintenance_tech:
        permissions:
          - read: [fault_logs, maintenance_manual]
          - write: [maintenance_log, software_upload]
          - execute: [diagnostic_test, firmware_update]
        domains: [AISD]
        mfa_required: true
      
      passenger:
        permissions:
          - read: [ife_content, moving_map]
          - write: []  # No write access
          - execute: [internet_access, call_attendant]
        domains: [PIESD]
        rate_limit: 10 Mbps

**3.3 Audit Logging**
---------------------

**Log Requirements:**

.. code-block:: text

    ARINC 811 Logging Requirements:
    
    1. Log all authentication attempts (success + failure)
    2. Log all authorization decisions (allow + deny)
    3. Log all firewall denials
    4. Log all administrative actions (config changes)
    5. Log all software uploads/downloads
    
    Log Format:
    - Timestamp (UTC, millisecond precision)
    - Event type (AUTH, AUTHZ, FIREWALL, ADMIN, FILE)
    - User/Source IP
    - Action (LOGIN, ACCESS, UPLOAD, CONFIG_CHANGE)
    - Result (SUCCESS, FAILURE, DENIED)
    - Additional context (file name, command, etc.)
    
    Log Storage:
    - Retention: 180 days minimum
    - Immutable (append-only, WORM media)
    - Encrypted at rest (AES-256)
    - Backed up daily (offsite)

**Example Log Entries:**

.. code-block:: text

    2026-01-14T18:32:15.123Z AUTH jsmith LOGIN SUCCESS source=10.20.1.50 domain=AISD
    2026-01-14T18:32:45.456Z AUTHZ jsmith ACCESS_EFB_CHARTS SUCCESS domain=AISD
    2026-01-14T18:35:10.789Z FIREWALL 10.30.5.67 DENIED dest=10.20.1.100 port=22 reason=PIESD_TO_AISD_BLOCKED
    2026-01-14T18:40:22.012Z FILE maint_tech1 UPLOAD_FIRMWARE SUCCESS file=fms_v2.3.bin size=2.5MB domain=AISD mfa=true
    2026-01-14T18:45:30.345Z ADMIN admin_user CONFIG_CHANGE SUCCESS change=firewall_rule_add rule_id=FW-123
    2026-01-14T19:00:05.678Z AUTH passenger123 LOGIN FAILURE source=10.30.2.34 domain=PIESD reason=invalid_payment

════════════════════════════════════════════════════════════════════

📖 **4. CRYPTOGRAPHIC REQUIREMENTS**
════════════════════════════════════

**4.1 Encryption Standards**
----------------------------

**ARINC 811 Cryptography Baseline:**

+------------------+-------------------------+--------------------+
| **Use Case**     | **Algorithm**           | **Key Length**     |
+==================+=========================+====================+
| Data at Rest     | AES-256-GCM             | 256-bit            |
+------------------+-------------------------+--------------------+
| Data in Transit  | TLS 1.3                 | ECDHE-P384         |
+------------------+-------------------------+--------------------+
| Digital Signature| ECDSA-P384 or RSA-3072  | 384-bit / 3072-bit |
+------------------+-------------------------+--------------------+
| Hashing          | SHA-256 or SHA-384      | N/A                |
+------------------+-------------------------+--------------------+
| Key Derivation   | PBKDF2-HMAC-SHA256      | 10,000+ iterations |
+------------------+-------------------------+--------------------+

**4.2 TLS Configuration**
------------------------

**TLS 1.3 Configuration (AISD Ground Link):**

.. code-block:: nginx

    # nginx.conf (ARINC 811 compliant)
    
    server {
        listen 443 ssl http2;
        server_name aisd-gateway.airline.com;
        
        # TLS 1.3 only (ARINC 811 requirement)
        ssl_protocols TLSv1.3;
        
        # Strong cipher suites (ECDHE for forward secrecy)
        ssl_ciphers TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;
        ssl_prefer_server_ciphers on;
        
        # Certificates
        ssl_certificate /etc/ssl/certs/aisd-gateway.crt;
        ssl_certificate_key /etc/ssl/private/aisd-gateway.key;
        
        # OCSP stapling (performance + privacy)
        ssl_stapling on;
        ssl_stapling_verify on;
        ssl_trusted_certificate /etc/ssl/certs/ca-chain.crt;
        
        # HSTS (force HTTPS)
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        
        # Session tickets (disable for perfect forward secrecy)
        ssl_session_tickets off;
        
        # Client certificate authentication (mutual TLS)
        ssl_client_certificate /etc/ssl/certs/client-ca.crt;
        ssl_verify_client on;
        ssl_verify_depth 2;
        
        # Security headers
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-XSS-Protection "1; mode=block" always;
        
        location / {
            proxy_pass http://aisd-backend:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

**4.3 Key Management**
---------------------

**Key Lifecycle:**

.. code-block:: text

    Generation → Storage → Distribution → Rotation → Destruction
    
    1. Generation:
       - Use FIPS 140-2 validated CSPRNG
       - Generate in HSM (Hardware Security Module)
       - Never export private keys
    
    2. Storage:
       - HSM for long-term keys (Root CA, Intermediate CA)
       - Encrypted key store for operational keys
       - AES-256 wrapping for transport keys
    
    3. Distribution:
       - Secure channels only (TLS 1.3, mutual auth)
       - Key ceremony for Root CA (multi-person)
       - Automated for operational keys (ACME protocol)
    
    4. Rotation:
       - Root CA: 10 years
       - Intermediate CA: 5 years
       - Server certificates: 1 year (398 days max)
       - Symmetric keys: 90 days
    
    5. Destruction:
       - Cryptographic erase (overwrite with random data 7x)
       - Physical destruction for HSM (shred, incinerate)
       - Document destruction in audit log

════════════════════════════════════════════════════════════════════

📖 **5. INTRUSION DETECTION & MONITORING**
══════════════════════════════════════════

**5.1 IDS/IPS Deployment**
--------------------------

**Intrusion Detection System (IDS) Placement:**

::

    ┌──────────────────────────────────────────┐
    │           AISD Network                   │
    │  (Crew, Maintenance, Operations)         │
    └──────────────┬───────────────────────────┘
                   │
                   ├──► [IDS Sensor] (Snort/Suricata)
                   │    Monitor: AISD internal traffic
                   ↓
    ┌──────────────────────────────────────────┐
    │      Firewall (Stateful + DPI)           │
    └──────────────┬───────────────────────────┘
                   │
                   ├──► [IDS Sensor] (Between domains)
                   │    Monitor: Cross-domain attempts
                   ↓
    ┌──────────────────────────────────────────┐
    │         PIESD Network                    │
    │  (Passenger Wi-Fi, IFE, Entertainment)   │
    └──────────────┬───────────────────────────┘
                   │
                   └──► [IDS Sensor] (Passenger traffic)
                        Monitor: DDoS, malware, anomalies

**IDS Rules (Snort Format):**

.. code-block:: text

    # snort_rules.conf (ARINC 811 specific)
    
    # Rule 1: Detect PIESD → AISD attempts (should be blocked by firewall)
    alert tcp 10.30.0.0/16 any -> 10.20.0.0/16 any \
      (msg:"CRITICAL: PIESD attempting to access AISD"; \
       priority:1; classtype:attempted-admin; \
       sid:100001; rev:1;)
    
    # Rule 2: Detect SQL injection attempts
    alert tcp any any -> any 80 \
      (msg:"SQL Injection detected"; \
       content:"UNION SELECT"; nocase; \
       priority:2; classtype:web-application-attack; \
       sid:100002; rev:1;)
    
    # Rule 3: Detect port scanning
    alert tcp any any -> 10.20.0.0/16 any \
      (msg:"Port scan detected on AISD"; \
       flags:S; threshold:type threshold, track by_src, count 20, seconds 60; \
       priority:3; classtype:attempted-recon; \
       sid:100003; rev:1;)
    
    # Rule 4: Detect USB malware (signature-based)
    alert tcp any any -> 10.20.0.0/16 8080 \
      (msg:"Malicious USB device detected"; \
       content:"|4D 5A|"; offset:0; depth:2; \  # MZ header (PE executable)
       content:"This program cannot be run in DOS mode"; \
       priority:1; classtype:trojan-activity; \
       sid:100004; rev:1;)
    
    # Rule 5: Detect data exfiltration (large outbound transfer)
    alert tcp 10.20.0.0/16 any -> any any \
      (msg:"Large data exfiltration detected"; \
       dsize:>10000000; threshold:type threshold, track by_src, count 10, seconds 60; \
       priority:2; classtype:policy-violation; \
       sid:100005; rev:1;)

**5.2 SIEM Integration**
------------------------

**Security Information and Event Management (SIEM):**

.. code-block:: yaml

    # siem_correlation_rules.yaml
    
    rules:
      
      - name: "Multiple Failed Logins"
        description: "Detect brute-force attack"
        conditions:
          - event_type: AUTH
          - result: FAILURE
          - count: >=5
          - timeframe: 5 minutes
        actions:
          - alert: security_team
          - block_ip: 15 minutes
          - log: high_priority
      
      - name: "Unauthorized Cross-Domain Access"
        description: "PIESD attempting to access AISD"
        conditions:
          - event_type: FIREWALL
          - source: 10.30.0.0/16
          - destination: 10.20.0.0/16
          - action: DENIED
          - count: >=3
          - timeframe: 1 minute
        actions:
          - alert: security_team (critical)
          - block_ip: permanent
          - log: critical
          - notify: FAA (if SAL 3)
      
      - name: "Malware Detected"
        description: "Antivirus detected malware"
        conditions:
          - event_type: MALWARE
          - severity: HIGH
        actions:
          - alert: security_team
          - quarantine_file: true
          - isolate_host: true
          - log: critical
      
      - name: "Software Upload Without MFA"
        description: "Maintenance upload without 2FA"
        conditions:
          - event_type: FILE
          - action: UPLOAD
          - mfa: false
          - domain: AISD
        actions:
          - alert: security_team
          - reject_upload: true
          - log: high_priority

**5.3 Anomaly Detection**
-------------------------

**Machine Learning for Anomaly Detection:**

.. code-block:: python

    # anomaly_detection.py
    
    from sklearn.ensemble import IsolationForest
    import numpy as np
    
    def detect_network_anomalies(traffic_data):
        """
        ML-based anomaly detection for aircraft networks
        """
        
        # Features: packet rate, byte rate, connection count, port diversity
        features = np.array([
            traffic_data['packets_per_sec'],
            traffic_data['bytes_per_sec'],
            traffic_data['unique_connections'],
            traffic_data['unique_ports']
        ]).T
        
        # Train Isolation Forest (unsupervised)
        model = IsolationForest(contamination=0.01, random_state=42)
        model.fit(features)
        
        # Predict anomalies (-1 = anomaly, 1 = normal)
        predictions = model.predict(features)
        
        # Alert on anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        
        for idx in anomaly_indices:
            alert_security_team({
                'timestamp': traffic_data['timestamp'][idx],
                'source_ip': traffic_data['source_ip'][idx],
                'anomaly_score': model.decision_function([features[idx]])[0],
                'reason': 'Unusual network behavior detected'
            })

════════════════════════════════════════════════════════════════════

📖 **6. COMPLIANCE & CERTIFICATION**
════════════════════════════════════

**6.1 ARINC 811 Compliance Checklist**
--------------------------------------

.. code-block:: markdown

    # ARINC 811 Compliance Checklist
    
    ## Domain Isolation
    - [ ] Three domains defined (ACD, AISD, PIESD)
    - [ ] Physical separation (ACD air-gapped)
    - [ ] Data diode installed (ACD → AISD, one-way)
    - [ ] Firewall deployed (AISD ↔ PIESD)
    - [ ] VLAN segmentation (within AISD)
    - [ ] No direct routing between domains
    
    ## Firewall
    - [ ] Stateful packet inspection enabled
    - [ ] Deep packet inspection (DPI) configured
    - [ ] Default deny policy
    - [ ] Rule set documented and approved
    - [ ] Logging enabled (all denials)
    - [ ] Redundancy (active-standby)
    - [ ] Performance tested (≥1 Gbps)
    
    ## Access Control
    - [ ] Authentication mechanisms deployed
      - [ ] ACD: Physical key + 2-person rule
      - [ ] AISD: Username/password (8+ chars)
      - [ ] AISD Maintenance: Multi-factor (MFA)
      - [ ] PIESD: Captive portal
    - [ ] Authorization (RBAC) configured
    - [ ] Audit logging enabled (180-day retention)
    - [ ] Log immutability (append-only storage)
    
    ## Cryptography
    - [ ] TLS 1.3 for external connections
    - [ ] AES-256 for data at rest
    - [ ] FIPS 140-2 validated algorithms
    - [ ] Key management procedures documented
    - [ ] Certificate lifecycle managed (auto-renewal)
    
    ## Monitoring
    - [ ] IDS/IPS deployed (all domain boundaries)
    - [ ] SIEM integration (real-time correlation)
    - [ ] Anomaly detection (ML-based)
    - [ ] 24/7 SOC monitoring (SAL 3)
    - [ ] Incident response plan documented
    
    ## Testing
    - [ ] Penetration testing (annual)
    - [ ] Vulnerability scanning (monthly)
    - [ ] Firewall rule audit (quarterly)
    - [ ] Red team exercise (SAL 3, annual)
    - [ ] Disaster recovery drill (annual)

**6.2 Integration with DO-326A/DO-356A**
----------------------------------------

**Mapping ARINC 811 to DO-326A:**

+---------------------------+---------------------------+
| **ARINC 811 Requirement** | **DO-326A Objective**     |
+===========================+===========================+
| Domain Isolation          | Asset Protection          |
+---------------------------+---------------------------+
| Firewall Rules            | Security Controls         |
+---------------------------+---------------------------+
| Access Control            | Authentication/Authz      |
+---------------------------+---------------------------+
| Cryptography              | Confidentiality/Integrity |
+---------------------------+---------------------------+
| IDS/IPS                   | Threat Detection          |
+---------------------------+---------------------------+
| Audit Logging             | Security Monitoring       |
+---------------------------+---------------------------+

**Combined Compliance Matrix:**

+------------+-------------+-------------+---------------+
| **Asset**  | **ARINC811**| **DO-326A** | **Status**    |
+============+=============+=============+===============+
| ACD        | Air gap     | SAL 3       | ✅ Compliant  |
+------------+-------------+-------------+---------------+
| AISD       | Firewall    | SAL 2       | ✅ Compliant  |
+------------+-------------+-------------+---------------+
| PIESD      | Rate limit  | SAL 1       | ✅ Compliant  |
+------------+-------------+-------------+---------------+

════════════════════════════════════════════════════════════════════

📝 **7. EXAM QUESTIONS**
════════════════════════

**Q1:** What are the three core principles of ARINC 811?

**A1:**

1. **Domain Isolation:** Physical and logical separation of ACD, AISD, PIESD
2. **Defense in Depth:** Multiple security layers (firewall, IDS, encryption)
3. **Least Privilege:** Minimal access rights, deny by default

────────────────────────────────────────────────────────────────────

**Q2:** Why does ARINC 811 require a data diode between ACD and AISD instead of a firewall?

**A2:**

- **Data Diode:** Physically one-way (optical transmitter → receiver, no return path)
- **Firewall:** Software-based, can be misconfigured or exploited
- **Reason:** ACD is flight-critical (DAL A) → requires absolute protection from AISD

────────────────────────────────────────────────────────────────────

**Q3:** Configure firewall rules for ARINC 811 compliance: AISD (10.20.0.0/16) → PIESD (10.30.0.0/16), allow GPS only.

**A3:**

.. code-block:: bash

    # Default deny
    iptables -P FORWARD DROP
    
    # Allow AISD → PIESD (GPS data, port 5000/UDP)
    iptables -A FORWARD -s 10.20.0.0/16 -d 10.30.0.0/16 \
      -p udp --dport 5000 -j ACCEPT
    
    # Deny PIESD → AISD (log attempts)
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.20.0.0/16 \
      -j LOG --log-prefix "ARINC811-VIOLATION: "
    iptables -A FORWARD -s 10.30.0.0/16 -d 10.20.0.0/16 -j REJECT

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Implement three-domain architecture (ACD, AISD, PIESD)
- [ ] Deploy data diode (ACD → AISD, one-way)
- [ ] Configure stateful firewall (AISD ↔ PIESD)
- [ ] Implement access control (authentication + RBAC)
- [ ] Deploy cryptography (TLS 1.3, AES-256)
- [ ] Install IDS/IPS (Snort/Suricata)
- [ ] Integrate SIEM (real-time correlation)
- [ ] Enable audit logging (180-day retention)
- [ ] Conduct penetration testing (annual)
- [ ] Document compliance (ARINC 811 + DO-326A)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **ARINC 811 defines network security baseline** → Commercial aviation 
standard for domain isolation

2️⃣ **Three domains with graduated security** → ACD (air gap), AISD (firewall), 
PIESD (basic protection)

3️⃣ **Data diode is mandatory for ACD** → Physical one-way prevents any return 
path to flight-critical systems

4️⃣ **Firewall must be stateful + DPI** → Deep packet inspection catches 
application-layer attacks

5️⃣ **Default deny policy is required** → All traffic blocked unless explicitly 
allowed (secure by default)

6️⃣ **MFA for maintenance access** → Multi-factor authentication prevents 
insider threats

7️⃣ **Continuous monitoring is essential** → IDS/IPS + SIEM + anomaly detection 
catch threats in real-time

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **ARINC 811 COMMERCIAL AIRCRAFT INFOSEC COMPLETE**
**Created:** January 14, 2026
**Coverage:** Domain Isolation, Firewall Requirements, Access Control (RBAC, MFA),
Cryptography (TLS 1.3, AES-256), Intrusion Detection (IDS/IPS, SIEM), Compliance

════════════════════════════════════════════════════════════════════
