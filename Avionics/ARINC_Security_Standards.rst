====================================================================
ARINC Security Standards — 827/835/842 (Cybersecurity)
====================================================================

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

================================================================================
TL;DR — Quick Reference
================================================================================

**ARINC Security Standards** define **cybersecurity** for avionics software distribution, authentication, and continued airworthiness in the modern threat landscape.

**Core Standards:**

.. code-block:: text

   Standard   Title                              Focus
   ─────────  ─────────────────────────────────  ────────────────────
   ARINC 827  Electronic Distribution System     PKI, encryption
   ARINC 835  Digital Signatures                 Code signing
   ARINC 842  Continued Airworthiness Security   Vulnerability mgmt

**Key Concepts:**

1. **EDS (Electronic Distribution System) — ARINC 827:**
   - **PKI (Public Key Infrastructure):** Certificate-based authentication
   - **Encryption:** AES-256 for LSP distribution
   - **EDS Crate:** Secure container for LSAP delivery
   - **Certificate Management:** Issuance, renewal, revocation

2. **Digital Signatures — ARINC 835:**
   - **Code Signing:** All LSPs/LSAPs signed by OEM
   - **Algorithms:** RSA-2048/4096, ECDSA P-256/P-384
   - **Hash Functions:** SHA-256, SHA-384, SHA-512
   - **Chain of Trust:** Developer → OEM → Aircraft

3. **Continued Airworthiness — ARINC 842:**
   - **Vulnerability Management:** CVE tracking, threat assessment
   - **Patch Distribution:** Secure delivery of security updates
   - **Audit Requirements:** Traceability for regulatory compliance
   - **DO-326A Alignment:** Airworthiness Security Process Specification

**Security Evolution:**

.. code-block:: text

   Era        Threat Model                 ARINC Response
   ─────────  ──────────────────────────  ───────────────────────
   Pre-2010   Physical security only       None (air gap)
   2011-2015  USB malware, insider threat  ARINC 827 (encryption)
   2016-2020  Network attacks, ransomware  ARINC 835 (signatures)
   2021+      Supply chain, zero-day       ARINC 842 (lifecycle)

================================================================================
1. ARINC 827 — Electronic Distribution System (EDS)
================================================================================

**1.1 Purpose & Motivation**
-----------------------------

**Problem:**
- **Pre-2015:** LSPs distributed via unencrypted FTP, USB drives, CDs
- **Risks:** Man-in-the-middle attacks, malware injection, unauthorized software
- **Real Incident (2015):** Polish LOT Airlines grounded by ground IT ransomware (not EDS, but wake-up call)

**Solution:**
ARINC 827 defines secure, encrypted distribution of LSAPs from OEM to aircraft.

**1.2 Architecture**
---------------------

**EDS Components:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────────┐
   │                  OEM (Boeing, Airbus)                     │
   │  ┌────────────────────────────────────────────────────┐  │
   │  │  LSAP Creation & Signing                           │  │
   │  │  - Compile software                                │  │
   │  │  - Sign with OEM private key (ARINC 835)          │  │
   │  │  - Package into EDS Crate                         │  │
   │  └───────────────────┬────────────────────────────────┘  │
   │                      │                                   │
   │                      ▼                                   │
   │  ┌────────────────────────────────────────────────────┐  │
   │  │  EDS Server (OEM-hosted)                           │  │
   │  │  - Encrypt LSAP with AES-256                      │  │
   │  │  - TLS 1.3 transport                              │  │
   │  └───────────────────┬────────────────────────────────┘  │
   └──────────────────────┼───────────────────────────────────┘
                          │ Encrypted Channel (Internet)
                          ▼
   ┌──────────────────────────────────────────────────────────┐
   │              Airline Ground Network                       │
   │  ┌────────────────────────────────────────────────────┐  │
   │  │  EDS Client (Airline IT)                           │  │
   │  │  - Download encrypted LSAP                        │  │
   │  │  - Verify OEM certificate                         │  │
   │  │  - Decrypt with airline private key               │  │
   │  └───────────────────┬────────────────────────────────┘  │
   │                      │                                   │
   │                      ▼                                   │
   │  ┌────────────────────────────────────────────────────┐  │
   │  │  Ground Storage (Airline Server)                   │  │
   │  │  - Store decrypted LSAP                           │  │
   │  │  - Distribute to aircraft (ARINC 615A)            │  │
   │  └────────────────────────────────────────────────────┘  │
   └──────────────────────────────────────────────────────────┘

**1.3 EDS Crate Format**
--------------------------

**Structure:**

.. code-block:: text

   EDS Crate (encrypted container):
   
   ┌───────────────────────────────────────────────────────┐
   │  Header (512 bytes)                                   │
   │  - Magic number: 0x45445343 ("EDSC")                 │
   │  - Version: 2.0                                       │
   │  - OEM ID: "BOEING-001", "AIRBUS-002"                │
   │  - Certificate ID: OEM cert fingerprint (SHA-256)    │
   │  - Encryption algorithm: AES-256-GCM                 │
   │  - IV (Initialization Vector): 96 bits               │
   ├───────────────────────────────────────────────────────┤
   │  Encrypted Payload                                    │
   │  - LSAP file (1 MB - 10 GB)                          │
   │  - Metadata (part number, version, dependencies)     │
   │  - Digital signature (ARINC 835)                     │
   │  - Build manifest (traceability)                     │
   ├───────────────────────────────────────────────────────┤
   │  Authentication Tag (128 bits)                        │
   │  - GCM tag for integrity/authenticity                │
   └───────────────────────────────────────────────────────┘

**1.4 Encryption Details**
----------------------------

**AES-256-GCM:**

.. code-block:: python

   from cryptography.hazmat.primitives.ciphers.aead import AESGCM
   import os
   
   class EDS_Crate:
       def __init__(self, oem_id, cert_id):
           self.oem_id = oem_id
           self.cert_id = cert_id
           self.version = "2.0"
       
       def create_crate(self, lsap_data, aes_key):
           """
           Create EDS crate with encrypted LSAP.
           
           Args:
               lsap_data: Raw LSAP bytes
               aes_key: 256-bit AES key (symmetric, session key)
           
           Returns:
               EDS crate (encrypted container)
           """
           # Generate random IV (96 bits for GCM)
           iv = os.urandom(12)
           
           # Initialize AES-GCM cipher
           aesgcm = AESGCM(aes_key)
           
           # Associated Data (authenticated but not encrypted)
           aad = self.build_header(iv)
           
           # Encrypt LSAP
           ciphertext = aesgcm.encrypt(iv, lsap_data, aad)
           
           # Build crate
           crate = aad + ciphertext
           return crate
       
       def build_header(self, iv):
           """Build EDS crate header (512 bytes)"""
           header = bytearray(512)
           
           # Magic number
           header[0:4] = b'EDSC'
           
           # Version
           header[4:8] = self.version.encode('ascii').ljust(4)
           
           # OEM ID
           header[8:24] = self.oem_id.encode('ascii').ljust(16)
           
           # Certificate ID (SHA-256 fingerprint)
           header[24:56] = bytes.fromhex(self.cert_id)
           
           # Encryption algorithm ID (0x01 = AES-256-GCM)
           header[56] = 0x01
           
           # IV (Initialization Vector)
           header[57:69] = iv
           
           return bytes(header)
       
       def decrypt_crate(self, crate, aes_key):
           """Decrypt EDS crate to retrieve LSAP"""
           # Extract header (512 bytes)
           header = crate[:512]
           ciphertext = crate[512:]
           
           # Verify magic number
           if header[0:4] != b'EDSC':
               raise ValueError("Invalid EDS crate (bad magic number)")
           
           # Extract IV
           iv = header[57:69]
           
           # Decrypt
           aesgcm = AESGCM(aes_key)
           lsap_data = aesgcm.decrypt(iv, ciphertext, header)
           
           return lsap_data
   
   # Example usage
   oem_crate = EDS_Crate(oem_id="BOEING-001", 
                         cert_id="a3f5b2..." )  # SHA-256 fingerprint
   
   # Encrypt LSAP
   with open('FMS_Update_v4.3.0.lsap', 'rb') as f:
       lsap_data = f.read()
   
   aes_key = os.urandom(32)  # 256-bit key (generated per-crate)
   crate = oem_crate.create_crate(lsap_data, aes_key)
   
   # Save encrypted crate
   with open('FMS_Update_v4.3.0.edsc', 'wb') as f:
       f.write(crate)
   
   print(f"EDS crate created: {len(crate)} bytes")

**1.5 Key Exchange (PKI)**
---------------------------

**Problem:**
How does airline receive AES session key securely?

**Solution:**
Hybrid encryption (RSA + AES):

.. code-block:: text

   1. OEM generates random AES-256 key (session key)
   2. OEM encrypts LSAP with AES key → EDS crate
   3. OEM encrypts AES key with airline's RSA public key
   4. OEM sends: [Encrypted AES key] + [EDS crate]
   
   5. Airline decrypts AES key with airline's RSA private key
   6. Airline decrypts EDS crate with AES key → LSAP

**Code Example:**

.. code-block:: python

   from cryptography.hazmat.primitives.asymmetric import rsa, padding
   from cryptography.hazmat.primitives import hashes
   
   # OEM side: Encrypt session key with airline's public key
   def oem_encrypt_session_key(aes_session_key, airline_public_key):
       """Encrypt AES session key with RSA public key"""
       encrypted_key = airline_public_key.encrypt(
           aes_session_key,
           padding.OAEP(
               mgf=padding.MGF1(algorithm=hashes.SHA256()),
               algorithm=hashes.SHA256(),
               label=None
           )
       )
       return encrypted_key
   
   # Airline side: Decrypt session key
   def airline_decrypt_session_key(encrypted_key, airline_private_key):
       """Decrypt AES session key with RSA private key"""
       aes_session_key = airline_private_key.decrypt(
           encrypted_key,
           padding.OAEP(
               mgf=padding.MGF1(algorithm=hashes.SHA256()),
               algorithm=hashes.SHA256(),
               label=None
           )
       )
       return aes_session_key
   
   # Full workflow
   # 1. Generate airline RSA key pair (one-time setup)
   airline_private_key = rsa.generate_private_key(
       public_exponent=65537,
       key_size=4096
   )
   airline_public_key = airline_private_key.public_key()
   
   # 2. OEM encrypts LSAP
   aes_key = os.urandom(32)  # 256-bit session key
   crate = oem_crate.create_crate(lsap_data, aes_key)
   
   # 3. OEM encrypts session key
   encrypted_aes_key = oem_encrypt_session_key(aes_key, airline_public_key)
   
   # 4. Airline receives [encrypted_aes_key] + [crate]
   # 5. Airline decrypts session key
   aes_key_decrypted = airline_decrypt_session_key(encrypted_aes_key, 
                                                    airline_private_key)
   
   # 6. Airline decrypts EDS crate
   lsap_data = oem_crate.decrypt_crate(crate, aes_key_decrypted)
   print(f"LSAP decrypted: {len(lsap_data)} bytes")

**1.6 Certificate Management**
--------------------------------

**Certificate Hierarchy:**

.. code-block:: text

   Root CA (e.g., DigiCert, Entrust)
      │
      ├─→ OEM Certificate (Boeing, Airbus)
      │    - Valid: 5 years
      │    - Usage: Code signing, key encipherment
      │    - Subject: CN=Boeing Commercial Airplanes
      │
      └─→ Airline Certificate (Delta, Lufthansa)
           - Valid: 2 years
           - Usage: Key encipherment
           - Subject: CN=Delta Air Lines

**Certificate Operations:**

.. code-block:: python

   from cryptography import x509
   from cryptography.x509.oid import NameOID
   from datetime import datetime, timedelta
   
   def issue_airline_certificate(airline_name, airline_public_key, 
                                  ca_private_key):
       """Issue certificate to airline (signed by Root CA)"""
       # Build certificate subject
       subject = x509.Name([
           x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
           x509.NameAttribute(NameOID.ORGANIZATION_NAME, airline_name),
           x509.NameAttribute(NameOID.COMMON_NAME, f"{airline_name} EDS")
       ])
       
       # Build certificate
       cert = x509.CertificateBuilder().subject_name(
           subject
       ).issuer_name(
           x509.Name([
               x509.NameAttribute(NameOID.COMMON_NAME, "ARINC Root CA")
           ])
       ).public_key(
           airline_public_key
       ).serial_number(
           x509.random_serial_number()
       ).not_valid_before(
           datetime.utcnow()
       ).not_valid_after(
           datetime.utcnow() + timedelta(days=730)  # 2 years
       ).add_extension(
           x509.KeyUsage(
               digital_signature=False,
               content_commitment=False,
               key_encipherment=True,  # For RSA key exchange
               data_encipherment=False,
               key_agreement=False,
               key_cert_sign=False,
               crl_sign=False,
               encipher_only=False,
               decipher_only=False
           ),
           critical=True
       ).sign(ca_private_key, hashes.SHA256())
       
       return cert
   
   # Example: Issue certificate to Delta
   delta_cert = issue_airline_certificate(
       airline_name="Delta Air Lines",
       airline_public_key=airline_public_key,
       ca_private_key=root_ca_private_key
   )
   
   print(f"Certificate issued: {delta_cert.subject}")
   print(f"Valid until: {delta_cert.not_valid_after}")

**Certificate Revocation:**

.. code-block:: text

   Scenario: Airline's private key compromised
   
   1. Airline reports breach to Root CA
   2. Root CA adds certificate to CRL (Certificate Revocation List)
   3. OEM checks CRL before encrypting LSAP
   4. If certificate revoked → reject distribution
   
   CRL Distribution:
   - Published by Root CA (updated hourly)
   - OEMs download CRL before each LSAP distribution
   - OCSP (Online Certificate Status Protocol) for real-time checks

================================================================================
2. ARINC 835 — Digital Signatures
================================================================================

**2.1 Purpose**
----------------

**Digital signatures ensure:**
1. **Authenticity:** LSAP created by legitimate OEM (not malware)
2. **Integrity:** LSAP not modified during distribution
3. **Non-repudiation:** OEM cannot deny creating LSAP

**2.2 Signing Algorithm**
---------------------------

**Supported Algorithms:**

.. code-block:: text

   Algorithm      Key Size  Hash       Security Level
   ─────────────  ────────  ─────────  ──────────────
   RSA-PSS        2048-bit  SHA-256    Medium (2030+)
   RSA-PSS        4096-bit  SHA-384    High (2040+)
   ECDSA          P-256     SHA-256    Medium (2030+)
   ECDSA          P-384     SHA-384    High (2040+)
   
   Preferred: ECDSA P-384 (smaller keys, faster, quantum-resistant)

**2.3 Signing Process**
-------------------------

**Workflow:**

.. code-block:: text

   1. Developer compiles LSAP binary
   2. Build system calculates SHA-256 hash of binary
   3. Build system signs hash with OEM private key
   4. Signature appended to LSAP file
   5. LSAP + signature distributed via ARINC 827

**Code Example (ECDSA P-384):**

.. code-block:: python

   from cryptography.hazmat.primitives.asymmetric import ec
   from cryptography.hazmat.primitives import hashes, serialization
   
   class ARINC835_Signer:
       def __init__(self):
           # Generate OEM signing key (one-time setup)
           self.private_key = ec.generate_private_key(ec.SECP384R1())
           self.public_key = self.private_key.public_key()
       
       def sign_lsap(self, lsap_data):
           """
           Sign LSAP with ECDSA P-384 + SHA-384.
           
           Returns: Digital signature (DER-encoded)
           """
           signature = self.private_key.sign(
               lsap_data,
               ec.ECDSA(hashes.SHA384())
           )
           return signature
       
       def export_public_key(self):
           """Export public key for distribution to airlines"""
           pem = self.public_key.public_bytes(
               encoding=serialization.Encoding.PEM,
               format=serialization.PublicFormat.SubjectPublicKeyInfo
           )
           return pem
   
   class ARINC835_Verifier:
       def __init__(self, oem_public_key_pem):
           # Load OEM public key
           self.public_key = serialization.load_pem_public_key(
               oem_public_key_pem
           )
       
       def verify_lsap(self, lsap_data, signature):
           """
           Verify LSAP signature.
           
           Returns: True if valid, False if invalid/tampered
           """
           try:
               self.public_key.verify(
                   signature,
                   lsap_data,
                   ec.ECDSA(hashes.SHA384())
               )
               return True
           except Exception as e:
               print(f"Signature verification failed: {e}")
               return False
   
   # OEM side: Sign LSAP
   signer = ARINC835_Signer()
   
   with open('FMS_Update_v4.3.0.lsap', 'rb') as f:
       lsap_data = f.read()
   
   signature = signer.sign_lsap(lsap_data)
   
   # Save signature
   with open('FMS_Update_v4.3.0.sig', 'wb') as f:
       f.write(signature)
   
   # Export public key
   public_key_pem = signer.export_public_key()
   with open('oem_public_key.pem', 'wb') as f:
       f.write(public_key_pem)
   
   print(f"LSAP signed: {len(signature)} byte signature")
   
   # Aircraft side: Verify signature
   verifier = ARINC835_Verifier(public_key_pem)
   
   with open('FMS_Update_v4.3.0.lsap', 'rb') as f:
       lsap_data = f.read()
   
   with open('FMS_Update_v4.3.0.sig', 'rb') as f:
       signature = f.read()
   
   if verifier.verify_lsap(lsap_data, signature):
       print("✓ Signature valid - LSAP authenticated")
   else:
       print("✗ Signature INVALID - REJECT LSAP")

**2.4 Chain of Trust**
------------------------

**Multi-Level Signing:**

.. code-block:: text

   Level 1: Developer Signature
   - Developer signs source code commit (git GPG signature)
   - Proves: Code written by authorized developer
   
   Level 2: Build Signature
   - Build system signs compiled binary
   - Proves: Binary matches signed source code
   
   Level 3: OEM Release Signature (ARINC 835)
   - OEM signs final LSAP before distribution
   - Proves: OEM authorizes release to customers
   
   Verification:
   - Aircraft verifies Level 3 signature (OEM)
   - Audit trail includes all three signatures

**Example: Multi-Signature LSAP:**

.. code-block:: python

   class Multi_Signature_LSAP:
       def __init__(self, lsap_data):
           self.lsap_data = lsap_data
           self.signatures = {
               'developer': None,
               'build_system': None,
               'oem_release': None
           }
       
       def add_signature(self, level, signature):
           """Add signature at specified trust level"""
           if level not in self.signatures:
               raise ValueError(f"Invalid signature level: {level}")
           self.signatures[level] = signature
       
       def verify_chain_of_trust(self, public_keys):
           """Verify all signatures in chain"""
           for level, signature in self.signatures.items():
               verifier = ARINC835_Verifier(public_keys[level])
               if not verifier.verify_lsap(self.lsap_data, signature):
                   print(f"✗ {level} signature INVALID")
                   return False
           
           print("✓ All signatures valid - chain of trust verified")
           return True
   
   # Usage
   lsap = Multi_Signature_LSAP(lsap_data)
   lsap.add_signature('developer', dev_signature)
   lsap.add_signature('build_system', build_signature)
   lsap.add_signature('oem_release', oem_signature)
   
   # Verify (airline side)
   public_keys = {
       'developer': dev_public_key,
       'build_system': build_public_key,
       'oem_release': oem_public_key
   }
   lsap.verify_chain_of_trust(public_keys)

================================================================================
3. ARINC 842 — Continued Airworthiness Security
================================================================================

**3.1 Motivation**
-------------------

**Problem:**
- **Software vulnerabilities** discovered post-delivery (zero-day exploits)
- **Supply chain attacks** (SolarWinds, Log4j precedents)
- **Regulatory requirements:** DO-326A/DO-356A mandate ongoing security

**Solution:**
ARINC 842 defines processes for managing security throughout aircraft operational life.

**3.2 Vulnerability Management**
----------------------------------

**Process:**

.. code-block:: text

   Step 1: Vulnerability Discovery
   - CVE (Common Vulnerabilities and Exposures) monitoring
   - Threat intelligence feeds
   - Bug bounty programs
   - Internal security audits
   
   Step 2: Risk Assessment
   - CVSS score (0-10, critical ≥ 9.0)
   - Exploit availability (public exploit code?)
   - Aircraft impact analysis (safety-critical?)
   
   Step 3: Patch Development
   - OEM creates LSP with vulnerability fix
   - Sign with ARINC 835
   - Encrypt with ARINC 827
   
   Step 4: Distribution
   - Prioritize by CVSS score:
     - Critical (9.0+): Within 7 days
     - High (7.0-8.9): Within 30 days
     - Medium (4.0-6.9): Within 90 days
   - Distribute via ARINC 615A to fleet
   
   Step 5: Verification
   - Audit logs: Which aircraft patched?
   - Compliance reporting to FAA/EASA
   - Post-patch validation (BIT)

**Example: CVE Tracking System:**

.. code-block:: python

   import requests
   from datetime import datetime, timedelta
   
   class ARINC842_VulnManager:
       def __init__(self, oem_software_list):
           self.software_list = oem_software_list  # List of LSPs in fleet
           self.vulnerabilities = []
       
       def check_cve_database(self):
           """Query NVD (National Vulnerability Database) for CVEs"""
           for software in self.software_list:
               # Query NVD API (example)
               url = f"https://nvd.nist.gov/rest/json/cves/2.0"
               params = {
                   'keywordSearch': software['name'],
                   'resultsPerPage': 100
               }
               response = requests.get(url, params=params)
               
               if response.status_code == 200:
                   cves = response.json().get('vulnerabilities', [])
                   for cve in cves:
                       self.process_cve(cve, software)
       
       def process_cve(self, cve_data, software):
           """Assess CVE and determine action"""
           cve_id = cve_data['cve']['id']
           cvss_score = cve_data['cve'].get('metrics', {}).get(
               'cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseScore', 0)
           
           # Risk assessment
           if cvss_score >= 9.0:
               priority = "CRITICAL"
               deadline = datetime.now() + timedelta(days=7)
           elif cvss_score >= 7.0:
               priority = "HIGH"
               deadline = datetime.now() + timedelta(days=30)
           elif cvss_score >= 4.0:
               priority = "MEDIUM"
               deadline = datetime.now() + timedelta(days=90)
           else:
               priority = "LOW"
               deadline = datetime.now() + timedelta(days=180)
           
           vuln = {
               'cve_id': cve_id,
               'software': software['name'],
               'cvss_score': cvss_score,
               'priority': priority,
               'deadline': deadline,
               'status': 'OPEN'
           }
           
           self.vulnerabilities.append(vuln)
           
           # Alert if critical
           if priority == "CRITICAL":
               self.send_alert(vuln)
       
       def send_alert(self, vuln):
           """Alert security team for critical vulnerabilities"""
           print(f"""
   ┌────────────────────────────────────────────────────────┐
   │  CRITICAL VULNERABILITY ALERT                          │
   ├────────────────────────────────────────────────────────┤
   │  CVE ID:       {vuln['cve_id']}                        │
   │  Software:     {vuln['software']}                      │
   │  CVSS Score:   {vuln['cvss_score']} (CRITICAL)         │
   │  Deadline:     {vuln['deadline'].strftime('%Y-%m-%d')} │
   │                                                        │
   │  ACTION REQUIRED: Develop and distribute patch         │
   └────────────────────────────────────────────────────────┘
       
       def generate_compliance_report(self):
           """Generate report for regulatory submission"""
           report = "ARINC 842 Vulnerability Management Report\n"
           report += "=" * 60 + "\n"
           report += f"Report Date: {datetime.now().isoformat()}\n\n"
           
           for vuln in self.vulnerabilities:
               report += f"CVE: {vuln['cve_id']}\n"
               report += f"  Software: {vuln['software']}\n"
               report += f"  CVSS: {vuln['cvss_score']} ({vuln['priority']})\n"
               report += f"  Deadline: {vuln['deadline'].strftime('%Y-%m-%d')}\n"
               report += f"  Status: {vuln['status']}\n\n"
           
           return report
   
   # Example usage
   software_list = [
       {'name': 'Honeywell FMS', 'version': '4.3.0'},
       {'name': 'Rockwell Collins Display', 'version': '2.1.5'}
   ]
   
   vuln_mgr = ARINC842_VulnManager(software_list)
   vuln_mgr.check_cve_database()
   
   report = vuln_mgr.generate_compliance_report()
   print(report)

**3.3 Patch Distribution**
----------------------------

**Secure Patch Workflow:**

.. code-block:: python

   class ARINC842_PatchManager:
       def __init__(self, fleet):
           self.fleet = fleet  # List of aircraft tail numbers
           self.patch_status = {}
       
       def distribute_security_patch(self, patch_lsap, vulnerability_id):
           """
           Distribute security patch to entire fleet.
           
           Uses ARINC 615A for loading, tracks compliance.
           """
           print(f"Distributing patch for {vulnerability_id}...")
           
           for aircraft in self.fleet:
               # Upload patch via ARINC 615A
               loader = ARINC615A_Loader(aircraft['ip_address'])
               
               success = loader.upload_lsp(
                   lsp_file=patch_lsap,
                   target_lru=aircraft['fms_lru']
               )
               
               if success:
                   loader.activate_lsp(aircraft['fms_lru'], patch_lsap)
                   self.patch_status[aircraft['tail_number']] = {
                       'status': 'PATCHED',
                       'timestamp': datetime.now(),
                       'vulnerability': vulnerability_id
                   }
               else:
                   self.patch_status[aircraft['tail_number']] = {
                       'status': 'FAILED',
                       'timestamp': datetime.now(),
                       'vulnerability': vulnerability_id
                   }
       
       def audit_compliance(self, vulnerability_id):
           """Generate audit report for regulators"""
           total = len(self.fleet)
           patched = sum(1 for status in self.patch_status.values() 
                        if status['status'] == 'PATCHED' and 
                        status['vulnerability'] == vulnerability_id)
           
           compliance_rate = (patched / total) * 100
           
           print(f"""
   Patch Compliance Report: {vulnerability_id}
   ────────────────────────────────────────────
   Total Aircraft: {total}
   Patched:        {patched} ({compliance_rate:.1f}%)
   Failed:         {total - patched}
   
   Regulatory Requirement: 100% within deadline
           """)
           
           return compliance_rate
   
   # Example
   fleet = [
       {'tail_number': 'N12345', 'ip_address': '192.168.10.100', 'fms_lru': 'FMS1'},
       {'tail_number': 'N67890', 'ip_address': '192.168.10.101', 'fms_lru': 'FMS1'}
   ]
   
   patch_mgr = ARINC842_PatchManager(fleet)
   patch_mgr.distribute_security_patch('CVE-2026-1234_patch.lsap', 'CVE-2026-1234')
   patch_mgr.audit_compliance('CVE-2026-1234')

**3.4 Audit Requirements**
----------------------------

**Traceability Records:**

.. code-block:: text

   Required Documentation (per DO-326A):
   
   1. Vulnerability Log:
      - All CVEs affecting avionics software
      - Risk assessment (CVSS score)
      - Mitigation timeline
   
   2. Patch Distribution Log:
      - Which aircraft received patch
      - Installation timestamp
      - Success/failure status
   
   3. Signature Verification Log:
      - All LSP signature checks
      - Certificate validation results
   
   4. Incident Response Log:
      - Security breaches (if any)
      - Root cause analysis
      - Corrective actions
   
   Retention: 10 years (FAA requirement)

**Example Audit Log:**

.. code-block:: python

   import json
   
   class ARINC842_AuditLog:
       def __init__(self, log_file='arinc842_audit.json'):
           self.log_file = log_file
           self.events = []
       
       def log_vulnerability(self, cve_id, cvss_score, software):
           """Log new vulnerability discovery"""
           event = {
               'timestamp': datetime.now().isoformat(),
               'event_type': 'VULNERABILITY_DISCOVERED',
               'cve_id': cve_id,
               'cvss_score': cvss_score,
               'affected_software': software
           }
           self.events.append(event)
           self.save()
       
       def log_patch_distribution(self, cve_id, aircraft, status):
           """Log patch installation attempt"""
           event = {
               'timestamp': datetime.now().isoformat(),
               'event_type': 'PATCH_DISTRIBUTION',
               'cve_id': cve_id,
               'aircraft_tail': aircraft,
               'status': status
           }
           self.events.append(event)
           self.save()
       
       def log_signature_verification(self, lsap, result):
           """Log LSP signature check"""
           event = {
               'timestamp': datetime.now().isoformat(),
               'event_type': 'SIGNATURE_VERIFICATION',
               'lsap_file': lsap,
               'result': 'VALID' if result else 'INVALID'
           }
           self.events.append(event)
           self.save()
       
       def save(self):
           """Persist audit log to disk"""
           with open(self.log_file, 'w') as f:
               json.dump(self.events, f, indent=2)
       
       def query_events(self, event_type=None, start_date=None):
           """Query audit log for compliance reporting"""
           filtered = self.events
           
           if event_type:
               filtered = [e for e in filtered if e['event_type'] == event_type]
           
           if start_date:
               filtered = [e for e in filtered 
                          if datetime.fromisoformat(e['timestamp']) >= start_date]
           
           return filtered
   
   # Example usage
   audit_log = ARINC842_AuditLog()
   
   audit_log.log_vulnerability('CVE-2026-1234', 9.8, 'Honeywell FMS v4.3.0')
   audit_log.log_patch_distribution('CVE-2026-1234', 'N12345', 'SUCCESS')
   audit_log.log_signature_verification('FMS_Patch_v4.3.1.lsap', True)
   
   # Query for compliance report
   patches = audit_log.query_events(
       event_type='PATCH_DISTRIBUTION',
       start_date=datetime(2026, 1, 1)
   )
   print(f"Patches distributed in 2026: {len(patches)}")

================================================================================
4. Exam Preparation — 5 Questions
================================================================================

**Question 1: EDS Crate Encryption (12 points)**

An OEM distributes LSAP (5 GB) via ARINC 827 EDS.

a) Why is hybrid encryption (RSA + AES) used instead of RSA-only? (4 pts)
b) Describe the key exchange process. (4 pts)
c) What happens if airline's certificate is revoked? (4 pts)

**Answer:**

a) **Why Hybrid Encryption:**
   - **RSA limitations:** Slow for large data (5 GB would take hours)
   - **RSA size limit:** Can only encrypt data up to key size (e.g., 4096-bit RSA = 512 bytes max)
   - **AES speed:** 1000× faster than RSA for bulk encryption
   - **Solution:** Use fast AES-256 to encrypt LSAP, use RSA to encrypt small AES key

b) **Key Exchange Process:**

.. code-block:: text

   1. OEM generates random AES-256 key (32 bytes)
   2. OEM encrypts 5 GB LSAP with AES key → EDS crate
   3. OEM retrieves airline's RSA public key from certificate
   4. OEM encrypts AES key (32 bytes) with airline's RSA public key
   5. OEM sends to airline: [Encrypted AES key (512 bytes)] + [EDS crate (5 GB)]
   
   6. Airline receives package
   7. Airline decrypts AES key using airline's RSA private key
   8. Airline decrypts EDS crate using AES key → LSAP (5 GB)
   
   Total encryption: 32 bytes (RSA) + 5 GB (AES) = Fast + Secure

c) **Certificate Revocation:**
   - **Detection:** OEM checks CRL (Certificate Revocation List) before encryption
   - **If revoked:**
     1. OEM **rejects** distribution request
     2. Airline must obtain new certificate from Root CA
     3. Airline generates new RSA key pair (old private key compromised)
     4. Root CA issues new certificate (2-year validity)
     5. OEM updates airline public key in distribution system
   - **Security:** Prevents LSAP distribution to compromised airline system

---

**Question 2: Digital Signature Verification (10 points)**

Aircraft receives LSAP with ECDSA P-384 signature.

a) What does the aircraft verify? (4 pts)
b) If signature invalid, what are possible causes? (4 pts)
c) Why ECDSA P-384 instead of RSA-2048? (2 pts)

**Answer:**

a) **Verification Process:**

.. code-block:: python

   1. Extract OEM public key from certificate (pre-installed on aircraft)
   2. Calculate SHA-384 hash of LSAP data
   3. Decrypt signature with OEM public key (ECDSA verify operation)
   4. Compare decrypted hash with calculated hash
   
   If match: ✓ Signature valid (LSAP authentic, unmodified)
   If mismatch: ✗ Signature invalid (tampered or wrong OEM)

b) **Possible Causes of Invalid Signature:**
   1. **LSAP tampered:** Malware injection, bit flips during transmission
   2. **Wrong public key:** Aircraft has old OEM certificate (expired/renewed)
   3. **Wrong OEM:** LSAP signed by different OEM (e.g., Honeywell LSAP, Boeing aircraft)
   4. **Signature file corrupted:** Network transmission error

c) **ECDSA P-384 Advantages:**
   - **Smaller keys:** 384-bit ECDSA ≈ 7680-bit RSA (same security, 95% smaller)
   - **Faster verification:** Critical for aircraft (limited CPU, real-time constraints)
   - **Future-proof:** More resistant to quantum computing attacks

---

**Question 3: Vulnerability Response Timeline (10 points)**

CVE-2026-5678 discovered: CVSS 9.8 (critical) in FMS software.

a) Per ARINC 842, what is the patch distribution deadline? (2 pts)
b) Describe the complete response workflow (OEM → aircraft). (6 pts)
c) How is compliance verified? (2 pts)

**Answer:**

a) **Deadline:**
   - **CVSS 9.8 = CRITICAL (≥9.0)**
   - **ARINC 842 requirement:** Patch within **7 days** of vulnerability disclosure

b) **Response Workflow:**

.. code-block:: text

   Day 0: CVE-2026-5678 published (CVSS 9.8)
   ─────────────────────────────────────────
   
   Hour 0-2: OEM Security Team
   - Assess impact (which FMS versions affected?)
   - Confirm exploitability (public exploit code?)
   - Prioritize: CRITICAL (drop all non-critical work)
   
   Hour 2-24: Patch Development
   - Developers create fix (code patch)
   - QA testing (DO-178C verification)
   - Build patched LSAP (FMS_v4.3.1_SECURITY_PATCH.lsap)
   
   Day 1-2: Signing & Distribution Prep
   - Sign LSAP with ARINC 835 (ECDSA P-384)
   - Encrypt with ARINC 827 (AES-256 EDS crate)
   - Notify airlines: "CRITICAL SECURITY UPDATE"
   
   Day 2-5: Fleet Distribution
   - Airlines download EDS crate from OEM server
   - Decrypt with airline private key
   - Upload to aircraft via ARINC 615A (Ethernet)
     - At gate: 5 minutes per aircraft
     - Can load while passengers boarding
   
   Day 5-7: Installation & Verification
   - Aircraft FMS validates signature (ARINC 835)
   - Activate patch (reboot FMS - 30 seconds)
   - BIT confirms patch applied correctly
   - Log installation (ARINC 842 audit trail)
   
   Day 7: Deadline
   - 100% of fleet must be patched
   - Compliance report to FAA/EASA

c) **Compliance Verification:**

.. code-block:: python

   # Audit query: Which aircraft patched for CVE-2026-5678?
   patched_aircraft = audit_log.query_events(
       event_type='PATCH_DISTRIBUTION',
       cve_id='CVE-2026-5678',
       status='SUCCESS'
   )
   
   compliance_rate = len(patched_aircraft) / total_fleet * 100
   
   if compliance_rate < 100:
       # Non-compliance: FAA enforcement action
       report_violation_to_regulator()
   
   # Submit to FAA: Compliance report + audit logs

---

**Question 4: Supply Chain Attack (8 points)**

Attacker compromises OEM's build server, injects malware into LSAP.

a) How does ARINC 835 chain of trust detect this? (4 pts)
b) What additional protections does ARINC 827 provide? (2 pts)
c) How does ARINC 842 audit trail help post-incident? (2 pts)

**Answer:**

a) **Chain of Trust Detection:**

.. code-block:: text

   Level 1: Developer Signature (git commit GPG)
   - Malware injected AFTER developer commit
   - Developer signature valid, but code modified
   
   Level 2: Build System Signature
   - Compromised build server signs malicious binary
   - Build signature VALID (attacker has build server private key)
   
   Level 3: OEM Release Signature (ARINC 835)
   - OEM security team reviews build before signing
   - Code review, malware scan (SAST/DAST tools)
   - If detected: REJECT signature, investigate breach
   - If missed: Malicious LSAP signed (worst case)
   
   Aircraft Verification:
   - Aircraft verifies OEM signature (valid if signed)
   - Cannot detect malware if OEM signature applied
   
   Mitigation:
   - Separate signing server (air-gapped, hardware HSM)
   - Multi-person authorization (2-of-3 keys required)
   - Code review + malware scan before signing

b) **ARINC 827 Protections:**
   - **Encryption:** Prevents attacker from modifying LSAP during distribution
   - **Integrity:** GCM authentication tag detects tampering
   - **Limitation:** Only protects distribution, not build process

c) **ARINC 842 Audit Trail:**

.. code-block:: text

   Post-Incident Investigation:
   
   1. Query audit log: Which aircraft received malicious LSAP?
   2. Identify affected tail numbers
   3. Emergency AD (Airworthiness Directive): Ground fleet
   4. Distribute clean LSAP, rollback malicious version
   5. Root cause: Build server compromise timestamp
   6. Forensics: How attacker gained access (phishing, insider?)
   
   Audit log provides:
   - Complete traceability (every LSAP installation)
   - Rapid response (identify affected aircraft in minutes)
   - Regulatory evidence (FAA investigation)

---

**Question 5: Integration Example (10 points)**

Airline loads FMS navigation database (AIRAC cycle 2602).

a) List all ARINC security standards involved. (3 pts)
b) Trace the LSP from OEM to aircraft activation. (5 pts)
c) What security checks occur at each step? (2 pts)

**Answer:**

a) **ARINC Standards:**
   - **ARINC 827:** Encrypt navigation database (EDS crate)
   - **ARINC 835:** Sign database (OEM digital signature)
   - **ARINC 842:** Audit trail (log distribution, installation)
   - **ARINC 615A:** Upload to aircraft (Ethernet)
   - **ARINC 665:** LSP metadata, version compatibility

b) **End-to-End Trace:**

.. code-block:: text

   Step 1: OEM (Jeppesen) Creates Database
   - Compile AIRAC 2602 (waypoints, airways, procedures)
   - Format: ARINC 424-22
   - Sign with Jeppesen private key (ARINC 835 - ECDSA P-384)
   
   Step 2: Encrypt for Distribution (ARINC 827)
   - Generate AES-256 session key
   - Encrypt database → EDS crate (1.2 GB)
   - Encrypt AES key with airline's RSA public key
   
   Step 3: Distribution
   - Upload to Jeppesen server (TLS 1.3)
   - Airline downloads via secure link
   - Decrypt EDS crate with airline private key
   
   Step 4: Upload to Aircraft (ARINC 615A)
   - Technician connects to aircraft WiFi
   - FTP transfer to FMS: 192.168.10.100
   - Verify SHA-256 checksum
   
   Step 5: Aircraft Validation
   - Verify Jeppesen signature (ARINC 835)
   - Check AIRAC effective dates (2026-02-22 to 2026-03-21)
   - Check part number compatibility (ARINC 665)
   
   Step 6: Activation (ARINC 667)
   - Install to inactive partition
   - Reboot FMS (30 seconds)
   - BIT verifies database loads correctly
   - If pass: Activate (switch active partition)
   
   Step 7: Audit (ARINC 842)
   - Log: Tail number, timestamp, database version
   - Compliance tracking: Fleet coverage

c) **Security Checks:**

.. code-block:: text

   OEM Side:
   - Code review before signing
   - Digital signature (ARINC 835)
   - Encryption (ARINC 827)
   
   Distribution:
   - TLS 1.3 (encrypted channel)
   - Certificate validation (airline authentic?)
   
   Aircraft Side:
   - Signature verification (OEM authentic?)
   - Checksum (integrity)
   - Compatibility (version, dependencies)
   - BIT (functionality)
   
   Post-Installation:
   - Audit log (traceability)
   - Compliance reporting (regulatory)

================================================================================
5. Completion Checklist
================================================================================

□ Understand ARINC 827 EDS architecture (PKI, encryption, EDS crate)
□ Implement AES-256-GCM encryption for LSP distribution
□ Implement RSA-4096 key exchange (hybrid encryption)
□ Manage X.509 certificates (issuance, renewal, revocation)
□ Understand ARINC 835 digital signatures (ECDSA P-384, RSA-PSS)
□ Implement chain of trust (developer → build → OEM signatures)
□ Know ARINC 842 vulnerability management (CVE tracking, CVSS scoring)
□ Implement patch distribution workflow (7-day deadline for critical)
□ Generate audit logs (ARINC 842 compliance)
□ Integrate with ARINC 615A (secure Ethernet loading)
□ Comply with DO-326A/DO-356A (airworthiness security)

================================================================================
6. Key Takeaways
================================================================================

1. **ARINC 827 = Secure Distribution:** PKI + AES-256 encryption for LSP delivery

2. **EDS Crate = Encrypted Container:** Hybrid encryption (RSA for key, AES for data)

3. **ARINC 835 = Code Signing:** Digital signatures (ECDSA P-384 preferred)

4. **Chain of Trust = Multi-Level:** Developer → Build → OEM signatures

5. **ARINC 842 = Lifecycle Security:** Vulnerability management, patch distribution, audit

6. **Critical Patches = 7 Days:** CVSS ≥9.0 requires fleet-wide patching within 1 week

7. **Audit Trail = Mandatory:** 10-year retention for regulatory compliance

8. **DO-326A Integration:** Security standards aligned with FAA/EASA requirements

9. **Certificate Management:** 2-5 year validity, CRL/OCSP for revocation

10. **Zero Trust:** Verify every LSP signature, even from trusted OEM

================================================================================
References & Further Reading
================================================================================

**Standards:**
- ARINC 827 — Electronic Distribution System (EDS)
- ARINC 835 — Software Upload and Retrieval with Digital Signature
- ARINC 842 — Design Guidance for Continued Airworthiness Security

**Regulatory:**
- DO-326A — Airworthiness Security Process Specification
- DO-356A — Airworthiness Security Methods and Considerations
- FAA AC 119-1A — Software Distribution Control

**Cryptography:**
- NIST FIPS 186-5 — Digital Signature Standard (DSS)
- NIST SP 800-57 — Key Management Recommendations
- RFC 5280 — X.509 Certificate and CRL Profile

**Cybersecurity:**
- CVSS v3.1 — Common Vulnerability Scoring System
- CWE — Common Weakness Enumeration
- MITRE ATT&CK — Adversarial Tactics, Techniques, and Common Knowledge

================================================================================

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Standards:** ARINC 827/835/842, DO-326A/356A

================================================================================
