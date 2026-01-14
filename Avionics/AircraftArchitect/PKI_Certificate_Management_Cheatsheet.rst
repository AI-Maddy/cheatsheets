🔐 **PKI & CERTIFICATE MANAGEMENT — Aviation-Grade Public Key Infrastructure**
════════════════════════════════════════════════════════════════════════════════

**Context:** PKI for secure aircraft communications and software updates
**Focus:** Certificate lifecycle, HSM integration, OCSP, June 2026 crisis
**Standards:** X.509, PKCS#11, FIPS 140-2, DO-326A

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — PKI IN 60 SECONDS**
────────────────────────────────

**PKI Hierarchy:**

::

    Root CA (offline, 20-year validity)
         ├── Intermediate CA (online, 10-year validity)
         │   ├── Server Cert (IFE API, 2-year validity)
         │   ├── Client Cert (pilot tablet, 1-year validity)
         │   └── Code Signing Cert (software updates, 3-year validity)
         └── Intermediate CA (backup)

**Certificate Lifecycle:**

::

    1. Issuance:  CSR → CA signs → Certificate
    2. Renewal:   90 days before expiry → Auto-renew
    3. Revocation: Compromised? → CRL/OCSP → Block usage
    4. Expiration: Cert expires → No longer valid

**June 2026 Crisis:**

::

    Problem: 100,000+ aircraft certificates expire June 15, 2026
    Impact:  Entire fleet grounded (no secure comms)
    Solution: Automated renewal + HSM key rotation (start NOW!)

════════════════════════════════════════════════════════════════════

📖 **1. PKI FUNDAMENTALS**
══════════════════════════

**1.1 Certificate Anatomy (X.509)**
-----------------------------------

.. code-block:: text

    Certificate:
        Data:
            Version: 3 (0x2)
            Serial Number: 4096 (0x1000)
            Signature Algorithm: sha256WithRSAEncryption
            Issuer: CN=Airline Intermediate CA, O=Airline Inc, C=US
            Validity
                Not Before: Jan  1 00:00:00 2024 GMT
                Not After : Jan  1 00:00:00 2026 GMT
            Subject: CN=ife-server.airline.com, O=Airline Inc, C=US
            Subject Public Key Info:
                Public Key Algorithm: rsaEncryption
                    RSA Public-Key: (2048 bit)
                    Modulus: 00:c5:3a:...
                    Exponent: 65537 (0x10001)
            X509v3 extensions:
                X509v3 Key Usage: critical
                    Digital Signature, Key Encipherment
                X509v3 Extended Key Usage:
                    TLS Web Server Authentication
                X509v3 Subject Alternative Name:
                    DNS:ife-server.airline.com, DNS:*.airline.com
                X509v3 CRL Distribution Points:
                    URI:http://crl.airline.com/intermediate.crl
                Authority Information Access:
                    OCSP - URI:http://ocsp.airline.com
        Signature Algorithm: sha256WithRSAEncryption
             3f:92:...

**Key Fields:**

- **Subject:** Entity the cert identifies (server, user, device)
- **Issuer:** CA that signed the cert
- **Validity:** Start/end dates (must be current)
- **Public Key:** For encryption/signature verification
- **Extensions:** Usage constraints (server auth, code signing, etc.)

**1.2 PKI Hierarchy**
--------------------

::

    ┌──────────────────────────┐
    │      Root CA             │  ← Offline, air-gapped
    │  (20-year validity)      │     Stored in vault
    └────────────┬─────────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼─────┐    ┌────▼─────┐
    │Intermediate│    │Intermediate│  ← Online, HSM-protected
    │CA (Prod)  │    │CA (Backup)│     Issues end-entity certs
    │10-year    │    │10-year    │
    └────┬──────┘    └───────────┘
         │
    ┌────┴─────────────────────┐
    │                          │
    ▼                          ▼
Server Cert               Client Cert        Code Signing Cert
(IFE API, 2yr)           (EFB tablet, 1yr)  (Software OTA, 3yr)

**Why This Design?**

- **Root CA offline:** If compromised, entire PKI collapses → Keep air-gapped
- **Intermediate CA online:** Issues certs daily → Must be accessible
- **Short-lived end-entity certs:** Reduces risk window (rotate frequently)

**1.3 Certificate Issuance**
----------------------------

**Step 1: Generate CSR (Certificate Signing Request)**

.. code-block:: bash

    # Generate private key
    openssl genpkey -algorithm RSA -out ife-server.key -pkeyopt rsa_keygen_bits:2048
    
    # Generate CSR
    openssl req -new -key ife-server.key -out ife-server.csr \
      -subj "/C=US/O=Airline Inc/CN=ife-server.airline.com"

**Step 2: Submit CSR to CA**

.. code-block:: bash

    # CA signs CSR (offline process for Root CA)
    openssl ca -config ca.conf \
      -in ife-server.csr \
      -out ife-server.crt \
      -days 730 \
      -extensions server_cert

**Step 3: Install Certificate**

.. code-block:: bash

    # Copy cert and key to server
    scp ife-server.crt ife-server.key root@ife-server:/etc/ssl/
    
    # Configure web server
    cat >> /etc/nginx/nginx.conf <<EOF
    server {
        listen 443 ssl;
        server_name ife-server.airline.com;
        ssl_certificate /etc/ssl/ife-server.crt;
        ssl_certificate_key /etc/ssl/ife-server.key;
        ssl_protocols TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
    }
    EOF
    
    # Restart
    systemctl restart nginx

**1.4 Certificate Validation**
------------------------------

**Client-Side (Browser/App):**

::

    1. Check expiration: Not Before ≤ Now ≤ Not After
    2. Verify signature: CA's public key decrypts signature → match cert hash
    3. Check chain: Server → Intermediate CA → Root CA (trusted)
    4. Check revocation: Query OCSP or download CRL
    5. Check hostname: cert.CN == requested.hostname

**Code Example:**

.. code-block:: python

    # cert_validate.py
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    import datetime
    
    def validate_cert(cert_path, ca_cert_path):
        # Load certificates
        with open(cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        with open(ca_cert_path, 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        
        # Check expiration
        now = datetime.datetime.utcnow()
        if not (cert.not_valid_before <= now <= cert.not_valid_after):
            raise ValueError("Certificate expired!")
        
        # Verify signature
        ca_public_key = ca_cert.public_key()
        try:
            ca_public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                cert.signature_algorithm_parameters
            )
            print("✅ Signature valid")
        except Exception as e:
            raise ValueError(f"Signature invalid: {e}")
    
    validate_cert("ife-server.crt", "intermediate-ca.crt")

════════════════════════════════════════════════════════════════════

📖 **2. CERTIFICATE LIFECYCLE**
═══════════════════════════════

**2.1 Automated Renewal (Let's Encrypt Style)**
-----------------------------------------------

**Problem:** Manual renewal → Forgotten → Expired → Outage

**Solution:** Automated renewal 90 days before expiry

.. code-block:: bash

    # cert-renew.sh
    #!/bin/bash
    
    CERT="/etc/ssl/ife-server.crt"
    KEY="/etc/ssl/ife-server.key"
    
    # Check expiry date
    EXPIRY=$(openssl x509 -enddate -noout -in $CERT | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
    NOW_EPOCH=$(date +%s)
    DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))
    
    if [ $DAYS_LEFT -lt 90 ]; then
        echo "⚠️ Certificate expires in $DAYS_LEFT days. Renewing..."
        
        # Generate new CSR
        openssl req -new -key $KEY -out /tmp/ife-server.csr \
          -subj "/C=US/O=Airline Inc/CN=ife-server.airline.com"
        
        # Submit to CA (ACME protocol for automation)
        curl -X POST https://ca.airline.com/acme/new-order \
          --data-binary @/tmp/ife-server.csr \
          -H "Authorization: Bearer $CA_TOKEN" \
          -o /tmp/ife-server-new.crt
        
        # Replace old cert
        cp /tmp/ife-server-new.crt $CERT
        
        # Reload web server
        systemctl reload nginx
        
        echo "✅ Certificate renewed. New expiry: $(openssl x509 -enddate -noout -in $CERT)"
    else
        echo "✅ Certificate valid for $DAYS_LEFT days"
    fi

**Cron Job:**

::

    # Check daily
    0 2 * * * /usr/local/bin/cert-renew.sh

**2.2 Certificate Revocation (CRL)**
------------------------------------

**Scenario:** Private key compromised → Must revoke cert immediately

**Step 1: Revoke Certificate**

.. code-block:: bash

    # CA revokes cert
    openssl ca -config ca.conf \
      -revoke /etc/ssl/certs/ife-server.crt \
      -crl_reason keyCompromise

**Step 2: Generate CRL (Certificate Revocation List)**

.. code-block:: bash

    # Generate CRL
    openssl ca -config ca.conf -gencrl -out /var/www/crl/intermediate.crl

**Step 3: Client Checks CRL**

.. code-block:: python

    # check_crl.py
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    import requests
    
    def check_revocation(cert_path, crl_url):
        # Load certificate
        with open(cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        
        # Download CRL
        crl_data = requests.get(crl_url).content
        crl = x509.load_pem_x509_crl(crl_data, default_backend())
        
        # Check if cert is revoked
        for revoked_cert in crl:
            if revoked_cert.serial_number == cert.serial_number:
                print("🚨 Certificate REVOKED!")
                return False
        
        print("✅ Certificate NOT revoked")
        return True
    
    check_revocation("ife-server.crt", "http://crl.airline.com/intermediate.crl")

**Problem with CRL:** Large file (100,000+ revoked certs), slow download

**2.3 OCSP (Online Certificate Status Protocol)**
-------------------------------------------------

**Better than CRL:** Real-time, single-cert query

**OCSP Request:**

.. code-block:: bash

    # Query OCSP responder
    openssl ocsp \
      -issuer intermediate-ca.crt \
      -cert ife-server.crt \
      -url http://ocsp.airline.com \
      -resp_text

**Output:**

::

    Response verify OK
    ife-server.crt: good
        This Update: Jan 14 12:00:00 2026 GMT
        Next Update: Jan 15 12:00:00 2026 GMT

**OCSP Stapling (Optimization):**

Server caches OCSP response → Sends with TLS handshake → Client doesn't query OCSP

.. code-block:: nginx

    # nginx.conf
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/chain.crt;

════════════════════════════════════════════════════════════════════

📖 **3. HSM INTEGRATION**
═════════════════════════

**3.1 What is HSM?**
-------------------

**Hardware Security Module:** Physical device that stores private keys

**Why HSM?**

- ✅ Keys never leave device (can't be stolen)
- ✅ FIPS 140-2 Level 3 certified (tamper-evident)
- ✅ High-performance crypto operations

**Use Cases:**

- Root CA private key (offline HSM in vault)
- Intermediate CA private key (online HSM in datacenter)
- Code signing key (HSM for OTA updates)

**3.2 PKCS#11 API**
------------------

**Standard:** PKCS#11 (Cryptoki) for HSM access

.. code-block:: c

    // hsm_sign.c
    #include <pkcs11.h>
    
    CK_RV sign_data(CK_SESSION_HANDLE session, CK_OBJECT_HANDLE key, 
                    CK_BYTE_PTR data, CK_ULONG data_len, 
                    CK_BYTE_PTR signature, CK_ULONG_PTR sig_len) {
        CK_MECHANISM mechanism = {CKM_RSA_PKCS, NULL_PTR, 0};
        CK_RV rv;
        
        // Initialize signing operation
        rv = C_SignInit(session, &mechanism, key);
        if (rv != CKR_OK) return rv;
        
        // Sign data
        rv = C_Sign(session, data, data_len, signature, sig_len);
        return rv;
    }

**3.3 OpenSSL with HSM**
-----------------------

.. code-block:: bash

    # Configure OpenSSL to use HSM
    cat >> /etc/ssl/openssl.cnf <<EOF
    openssl_conf = openssl_init
    
    [openssl_init]
    engines = engine_section
    
    [engine_section]
    pkcs11 = pkcs11_section
    
    [pkcs11_section]
    engine_id = pkcs11
    dynamic_path = /usr/lib/engines/pkcs11.so
    MODULE_PATH = /usr/lib/libpkcs11.so
    init = 0
    EOF
    
    # Sign with HSM key
    openssl dgst -sha256 -sign "pkcs11:token=HSM_TOKEN;object=CA_KEY" \
      -out signature.bin data.txt

**3.4 Key Ceremony**
-------------------

**Scenario:** Generate Root CA key in HSM (once-in-a-lifetime event)

**Process:**

::

    1. Assemble quorum (5 people, need 3 to activate HSM)
    2. Enter secure vault (no phones, cameras)
    3. Each person enters their PIN shard
    4. HSM unlocks
    5. Generate Root CA key pair (4096-bit RSA)
    6. Export public key ONLY (private key never leaves HSM)
    7. Lock HSM
    8. Store HSM in vault (offline)

**Audit:**

- Video recording (no audio, no faces)
- Signed attestation by all participants
- Escrow backup HSM in separate location

════════════════════════════════════════════════════════════════════

📖 **4. JUNE 2026 CERTIFICATE CRISIS**
══════════════════════════════════════

**4.1 The Problem**
------------------

**Date:** June 15, 2026

**Impact:** 100,000+ aircraft certificates expire simultaneously

**Root Cause:** Mass deployment in June 2016 (10-year validity)

**Consequences:**

- ✈️ Entire fleet grounded (secure comms disabled)
- 💰 $100M+ losses per day
- 📜 Regulatory violations (DO-326A)

**Why So Bad?**

- Can't renew 100,000 certs manually in time
- Some aircraft lack OTA update capability (need physical access)
- No rollback if renewal fails

**4.2 Pre-Crisis Checklist (Start NOW!)**
-----------------------------------------

**6 Months Before (January 2026):**

- [ ] Inventory all certificates (server, client, code signing)
- [ ] Identify expiry dates (anything June 2026 → RED FLAG)
- [ ] Test automated renewal in staging environment
- [ ] Establish emergency manual process (if automation fails)

**3 Months Before (March 2026):**

- [ ] Deploy automated renewal to 10% of fleet (canary)
- [ ] Monitor for failures (certificate pinning issues?)
- [ ] Prepare rollback plan
- [ ] Train field technicians (manual renewal)

**1 Month Before (May 2026):**

- [ ] Deploy to 100% of fleet
- [ ] 24/7 monitoring (watch for renewal failures)
- [ ] Daily reports to management
- [ ] Freeze other changes (no distractions)

**1 Week Before (June 8, 2026):**

- [ ] Final verification (100% of certs renewed?)
- [ ] Emergency response team on standby
- [ ] Press release prepared (if disaster)

**4.3 Automated Renewal at Scale**
----------------------------------

.. code-block:: python

    # mass_renewal.py
    import asyncio
    import aiohttp
    from datetime import datetime, timedelta
    
    AIRCRAFT_LIST = [f"N{i:05d}" for i in range(1, 100001)]  # 100,000 aircraft
    CA_API = "https://ca.airline.com/api/renew"
    
    async def renew_cert(session, tail_number):
        """Renew certificate for one aircraft"""
        try:
            async with session.post(
                CA_API,
                json={"tail_number": tail_number},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ {tail_number}: Renewed (expires {data['expiry']})")
                    return True
                else:
                    print(f"❌ {tail_number}: Failed (HTTP {resp.status})")
                    return False
        except Exception as e:
            print(f"❌ {tail_number}: Error ({e})")
            return False
    
    async def mass_renew():
        """Renew all aircraft certificates in parallel"""
        async with aiohttp.ClientSession() as session:
            tasks = [renew_cert(session, tail) for tail in AIRCRAFT_LIST]
            results = await asyncio.gather(*tasks)
            
            success = sum(results)
            failed = len(results) - success
            print(f"\n📊 Summary: {success} success, {failed} failed")
    
    # Run
    asyncio.run(mass_renew())

**Monitoring:**

.. code-block:: python

    # monitor_expiry.py
    import sqlite3
    from datetime import datetime, timedelta
    
    def check_expiry():
        """Alert for certs expiring soon"""
        conn = sqlite3.connect('certs.db')
        cursor = conn.cursor()
        
        # Find certs expiring in < 30 days
        threshold = datetime.now() + timedelta(days=30)
        cursor.execute("""
            SELECT tail_number, expiry_date 
            FROM certificates 
            WHERE expiry_date < ?
        """, (threshold,))
        
        expiring = cursor.fetchall()
        if expiring:
            print(f"🚨 {len(expiring)} certificates expiring soon:")
            for tail, expiry in expiring:
                print(f"  - {tail}: {expiry}")
        else:
            print("✅ All certificates valid for > 30 days")
    
    check_expiry()

**4.4 Manual Renewal Process**
------------------------------

**Scenario:** Automated renewal failed for aircraft N12345

**Step 1: Technician Visits Aircraft**

.. code-block:: bash

    # 1. Connect laptop to avionics via maintenance port
    ssh tech@10.0.0.1
    
    # 2. Generate CSR
    openssl req -new -key /etc/ssl/aircraft.key -out /tmp/aircraft.csr \
      -subj "/C=US/O=Airline Inc/CN=N12345"
    
    # 3. Copy CSR to USB
    cp /tmp/aircraft.csr /mnt/usb/

**Step 2: Submit CSR to CA (Offline)**

.. code-block:: bash

    # Technician brings USB to office
    # CA signs CSR
    openssl ca -config ca.conf -in aircraft.csr -out aircraft.crt -days 3650

**Step 3: Install New Certificate**

.. code-block:: bash

    # Copy cert back to USB
    cp aircraft.crt /mnt/usb/
    
    # Technician returns to aircraft
    ssh tech@10.0.0.1
    cp /mnt/usb/aircraft.crt /etc/ssl/
    systemctl restart avionics
    
    # Verify
    openssl x509 -in /etc/ssl/aircraft.crt -noout -dates

════════════════════════════════════════════════════════════════════

📖 **5. BEST PRACTICES**
════════════════════════

**5.1 Certificate Pinning**
---------------------------

**Purpose:** Prevent MITM attacks by hardcoding expected certificate

**Code Example:**

.. code-block:: python

    # cert_pinning.py
    import hashlib
    import ssl
    import socket
    
    EXPECTED_FINGERPRINT = "sha256:1a2b3c..."
    
    def verify_cert_fingerprint(hostname, port=443):
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_der = ssock.getpeercert(binary_form=True)
                fingerprint = hashlib.sha256(cert_der).hexdigest()
                
                if fingerprint != EXPECTED_FINGERPRINT:
                    raise ValueError("Certificate fingerprint mismatch!")
                
                print("✅ Certificate pinned correctly")
    
    verify_cert_fingerprint("ife-server.airline.com")

**⚠️ Risk:** If cert is renewed, pinned fingerprint must be updated

**5.2 Short-Lived Certificates**
--------------------------------

**Philosophy:** Rotate frequently to minimize risk window

+-----------------------+-------------------+
| **Cert Type**         | **Max Validity**  |
+=======================+===================+
| Root CA               | 20 years          |
+-----------------------+-------------------+
| Intermediate CA       | 10 years          |
+-----------------------+-------------------+
| Server cert           | 1 year (398 days) |
+-----------------------+-------------------+
| Client cert           | 90 days           |
+-----------------------+-------------------+
| Code signing          | 3 years           |
+-----------------------+-------------------+

**Why 398 days for server certs?** Chrome/Safari maximum (since 2020)

**5.3 Key Rotation**
-------------------

**Scenario:** Rotate HSM key every 5 years

.. code-block:: bash

    # 1. Generate new key pair in HSM
    pkcs11-tool --module /usr/lib/libpkcs11.so --login \
      --keypairgen --key-type rsa:4096 --label NEW_CA_KEY
    
    # 2. Issue new Intermediate CA cert (signed by Root CA)
    openssl ca -config ca.conf \
      -in intermediate-new.csr \
      -out intermediate-new.crt \
      -extensions v3_intermediate_ca \
      -days 3650
    
    # 3. Publish new Intermediate CA cert
    cp intermediate-new.crt /var/www/pki/
    
    # 4. Transition period (6 months): Both old and new keys active
    # 5. After 6 months: Revoke old Intermediate CA cert

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
════════════════════════

**Q1:** Explain the PKI hierarchy for an airline. Why is the Root CA kept offline?

**A1:**

**Hierarchy:**

::

    Root CA (offline, 20-year validity)
         ├── Intermediate CA (online, 10-year validity)
         │   ├── Server Cert (IFE, 2-year validity)
         │   ├── Client Cert (EFB, 1-year validity)
         │   └── Code Signing Cert (OTA, 3-year validity)

**Why Root CA Offline?**

- **Risk:** If Root CA private key compromised → Entire PKI collapses (all certs invalid)
- **Solution:** Keep Root CA in air-gapped HSM in vault
- **Usage:** Only used to sign Intermediate CA certs (rare event, ~every 10 years)

**Why Intermediate CA Online?**

- **Frequency:** Issues thousands of certs daily (server, client, code signing)
- **Compromise:** Only Intermediate CA certs invalid → Re-issue from Root CA
- **Trade-off:** Convenience vs security (acceptable risk)

────────────────────────────────────────────────────────────────────

**Q2:** Walk through the automated certificate renewal process. How do you prevent June 2026 crisis?

**A2:**

**Automated Renewal:**

.. code-block:: bash

    # 1. Daily cron job checks expiry
    DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
    
    # 2. If < 90 days, trigger renewal
    if [ $DAYS_LEFT -lt 90 ]; then
        # Generate CSR
        openssl req -new -key aircraft.key -out aircraft.csr
        
        # Submit to CA (ACME protocol)
        curl -X POST https://ca.airline.com/acme/new-order \
          --data-binary @aircraft.csr -o aircraft-new.crt
        
        # Replace old cert
        cp aircraft-new.crt /etc/ssl/aircraft.crt
        systemctl reload avionics
    fi

**Prevent June 2026 Crisis:**

1. **Start early:** Begin renewals 6 months before (January 2026)
2. **Canary deployment:** Test on 10% of fleet first
3. **Monitor failures:** 24/7 dashboard tracking renewal success rate
4. **Manual fallback:** Technicians visit aircraft if automation fails
5. **Dry run:** Practice in staging (simulate mass expiry)

────────────────────────────────────────────────────────────────────

**Q3:** What is OCSP stapling? How does it improve performance?

**A3:**

**Without Stapling:**

::

    Client ─────TLS Handshake────▶ Server
    Client ◀────Server Cert───────┘
    Client ─────OCSP Request─────▶ CA's OCSP Responder
    Client ◀────OCSP Response────┘ (Cert is valid)
    Client ─────Encrypted Data───▶ Server

**Problem:** Extra round-trip to OCSP responder (adds latency)

**With Stapling:**

::

    Server ─────OCSP Request─────▶ CA's OCSP Responder (every 24 hrs)
    Server ◀────OCSP Response────┘ (Cache response)
    
    Client ─────TLS Handshake────▶ Server
    Client ◀─(Cert + OCSP Response)─┘ (Stapled!)
    Client ─────Encrypted Data───▶ Server

**Benefits:**

- ✅ Faster: No extra round-trip
- ✅ Reliable: Works even if OCSP responder down
- ✅ Privacy: Client doesn't reveal browsing to CA

**Configuration:**

.. code-block:: nginx

    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/chain.crt;

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
───────────────────────────

- [ ] Understand X.509 certificate structure
- [ ] Design 3-tier PKI hierarchy (Root → Intermediate → End Entity)
- [ ] Implement automated certificate renewal (90-day threshold)
- [ ] Set up OCSP responder + stapling
- [ ] Integrate HSM for Root/Intermediate CA keys (FIPS 140-2 Level 3)
- [ ] Document key ceremony process
- [ ] Build certificate inventory (track all certs across fleet)
- [ ] Monitor expiry dates (alert 30 days before)
- [ ] Prepare June 2026 crisis response plan
- [ ] Test mass renewal at scale (100,000+ certs)
- [ ] Train technicians on manual renewal fallback
- [ ] Implement certificate pinning for critical apps
- [ ] Rotate HSM keys every 5 years

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Root CA must be offline** → Compromise = PKI collapse → Store in air-
gapped HSM

2️⃣ **Automate renewal (90-day threshold)** → Prevents June 2026 crisis → 
Daily cron job

3️⃣ **OCSP stapling improves performance** → Server caches response → No extra 
round-trip

4️⃣ **HSM protects private keys** → Keys never leave device → FIPS 140-2 Level 3

5️⃣ **Short-lived certs reduce risk** → Server: 1 year max → Client: 90 days

6️⃣ **Certificate pinning prevents MITM** → Hardcode expected fingerprint → 
Must update on renewal

7️⃣ **June 2026 crisis is preventable** → Start renewals 6 months early → 
Test on 10% first → Monitor 24/7

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **PKI & CERTIFICATE MANAGEMENT COMPLETE**
**Created:** January 14, 2026
**Coverage:** X.509, Certificate Lifecycle, HSM Integration, OCSP, June 2026 Crisis Response

════════════════════════════════════════════════════════════════════
