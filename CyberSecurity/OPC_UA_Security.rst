🏭 **OPC UA SECURITY FOR INDUSTRIAL SYSTEMS**
═══════════════════════════════════════════════════════════════════════

**OPC Unified Architecture Security (IEC 62541)**  
**Purpose:** Secure industrial data exchange 🔒 | Interoperability 🔗 | Industry 4.0 🏭  
**Scope:** Manufacturing, process control, building automation, energy management

════════════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

════════════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**OPC UA** (Open Platform Communications Unified Architecture) is the modern industrial communication standard with **built-in security**.

**Security Modes:**
- **None:** No encryption/authentication (legacy compatibility)
- **Sign:** Digital signatures (integrity)
- **SignAndEncrypt:** Full TLS 1.2+ (confidentiality + integrity)

**Use Cases:** SCADA, MES, IoT gateways, cloud connectivity, cross-vendor integration.

════════════════════════════════════════════════════════════════════════════

📐 **OPC UA ARCHITECTURE & SECURITY MODEL**
─────────────────────────────────────────────────────────────────────────

**OPC UA vs. OPC Classic:**

| Feature | OPC Classic (DCOM) | OPC UA |
|:--------|:-------------------|:-------|
| **Security** | Windows-based (DCOM) | Built-in (X.509, TLS) |
| **Platform** | Windows only | Cross-platform (Windows, Linux, embedded) |
| **Protocol** | DCOM (proprietary) | Binary TCP, HTTPS, WebSocket |
| **Firewall** | Complex (dynamic ports) | Simple (single port) |
| **Encryption** | None | TLS 1.2+, AES-256 |

**OPC UA Security Layers:**

.. code-block:: text

   ┌──────────────────────────────────────────────────────┐
   │ Application Layer (OPC UA Services)                 │
   │ ├─ Read/Write variables                             │
   │ ├─ Browse address space                             │
   │ └─ Subscribe to data changes                        │
   ├──────────────────────────────────────────────────────┤
   │ Security Layer                                      │
   │ ├─ Message encryption (TLS 1.2+)                    │
   │ ├─ Digital signatures (X.509 certificates)          │
   │ ├─ User authentication (Username/X.509/Kerberos)    │
   │ └─ Authorization (Role-based access control)        │
   ├──────────────────────────────────────────────────────┤
   │ Transport Layer                                     │
   │ ├─ opc.tcp:// (Binary, most common)                 │
   │ ├─ https:// (Web services)                          │
   │ └─ wss:// (WebSocket for cloud)                     │
   └──────────────────────────────────────────────────────┘

**Security Modes (IEC 62541-4):**

.. code-block:: python

   from enum import Enum
   
   class SecurityMode(Enum):
       """OPC UA Security Modes (IEC 62541-4 Section 7.2)"""
       
       NONE = 1
       # No encryption, no signing
       # Use case: Testing, legacy compatibility (NOT RECOMMENDED)
       
       SIGN = 2
       # Digital signatures for integrity
       # No encryption (plaintext data)
       # Use case: Data integrity without confidentiality requirement
       
       SIGN_AND_ENCRYPT = 3
       # Digital signatures + TLS encryption
       # Use case: Production systems (RECOMMENDED)

**Security Policies (Algorithm Suites):**

| Policy | Encryption | Signature | Key Length | Use Case |
|:-------|:-----------|:----------|:-----------|:---------|
| **None** | - | - | - | Testing only |
| **Basic128Rsa15** | AES-128-CBC | RSA-1024 | 1024 bit | DEPRECATED |
| **Basic256** | AES-256-CBC | RSA-2048 | 2048 bit | Legacy |
| **Basic256Sha256** | AES-256-CBC | RSA-2048, SHA-256 | 2048 bit | Recommended |
| **Aes128_Sha256_RsaOaep** | AES-128-CBC | RSA-2048, SHA-256 | 2048 bit | Embedded |
| **Aes256_Sha256_RsaPss** | AES-256-CBC | RSA-2048, SHA-256, RSA-PSS | 2048 bit | High security |

════════════════════════════════════════════════════════════════════════════

🔐 **OPC UA CERTIFICATE MANAGEMENT**
─────────────────────────────────────────────────────────────────────────

**X.509 Certificates for Device Identity:**

.. code-block:: python

   from cryptography import x509
   from cryptography.x509.oid import NameOID, ExtensionOID
   from cryptography.hazmat.primitives import hashes, serialization
   from cryptography.hazmat.primitives.asymmetric import rsa
   import datetime
   
   class OPCUACertificateManager:
       """
       Generate and manage OPC UA X.509 certificates.
       IEC 62541-6: Certificate requirements for OPC UA.
       """
       
       def generate_application_certificate(self, app_uri, hostname):
           """
           Generate OPC UA application certificate.
           
           Requirements (IEC 62541-6 Section 6.2):
           - RSA 2048-bit minimum
           - SHA-256 signature
           - subjectAltName with ApplicationURI
           - Key usage: digitalSignature, keyEncipherment, dataEncipherment
           """
           # Generate private key (RSA 2048-bit)
           private_key = rsa.generate_private_key(
               public_exponent=65537,
               key_size=2048
           )
           
           # Build certificate
           subject = issuer = x509.Name([
               x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
               x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Industrial Automation Co"),
               x509.NameAttribute(NameOID.COMMON_NAME, hostname),
           ])
           
           cert = (
               x509.CertificateBuilder()
               .subject_name(subject)
               .issuer_name(issuer)
               .public_key(private_key.public_key())
               .serial_number(x509.random_serial_number())
               .not_valid_before(datetime.datetime.utcnow())
               .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))  # 10 years
               # CRITICAL: subjectAltName with ApplicationURI (OPC UA requirement)
               .add_extension(
                   x509.SubjectAlternativeName([
                       x509.UniformResourceIdentifier(app_uri),  # e.g., "urn:ScadaServer:OpcUa"
                       x509.DNSName(hostname)
                   ]),
                   critical=False
               )
               # Key usage for OPC UA
               .add_extension(
                   x509.KeyUsage(
                       digital_signature=True,
                       key_encipherment=True,
                       data_encipherment=True,
                       content_commitment=False,
                       key_agreement=False,
                       key_cert_sign=False,
                       crl_sign=False,
                       encipher_only=False,
                       decipher_only=False
                   ),
                   critical=True
               )
               .sign(private_key, hashes.SHA256())
           )
           
           return cert, private_key
       
       def verify_certificate_chain(self, app_cert, issuer_cert):
           """Verify OPC UA certificate against issuer (CA)"""
           # Check signature
           try:
               issuer_cert.public_key().verify(
                   app_cert.signature,
                   app_cert.tbs_certificate_bytes,
                   # Padding and hash depend on signature algorithm
               )
               return True
           except Exception as e:
               print(f"Certificate verification failed: {e}")
               return False
       
       def check_certificate_revocation(self, cert, crl_url):
           """Check Certificate Revocation List (CRL)"""
           # In production: Download and parse CRL
           # Check if certificate serial number is revoked
           return False  # Not revoked (placeholder)
   
   # Example: Generate certificate for OPC UA server
   cert_mgr = OPCUACertificateManager()
   cert, private_key = cert_mgr.generate_application_certificate(
       app_uri="urn:ScadaServer:OpcUa:PlantA",
       hostname="scada-server-01.plant-a.local"
   )
   
   # Save certificate and private key
   with open("opcua_server.crt", "wb") as f:
       f.write(cert.public_bytes(serialization.Encoding.PEM))
   
   with open("opcua_server.key", "wb") as f:
       f.write(private_key.private_bytes(
           encoding=serialization.Encoding.PEM,
           format=serialization.PrivateFormat.PKCS8,
           encryption_algorithm=serialization.NoEncryption()
       ))

**Trust Lists (IEC 62541-6 Section 6.4):**

.. code-block:: text

   OPC UA Server Trust Store:
   
   /etc/opcua/pki/
   ├─ trusted/              ← Trusted certificates (CA, clients)
   │  ├─ ca.crt             (Certificate Authority)
   │  ├─ client1.crt        (Trusted client)
   │  └─ client2.crt
   ├─ rejected/             ← Rejected certificates (auto-rejected)
   ├─ issuer/               ← Issuer certificates (intermediate CAs)
   └─ own/                  ← Own certificate + private key
      ├─ server.crt
      └─ server.key

**Certificate Validation Process:**

```
Client connects to OPC UA Server:
1. Client presents certificate (X.509)
2. Server checks: Is certificate in trusted/ folder? → YES/NO
3. If YES: Verify signature, expiration, revocation
4. If NO: Reject or move to rejected/ (admin review)
5. Extract ApplicationURI from subjectAltName
6. Match ApplicationURI to configured endpoint
7. Establish secure channel (TLS handshake)
```

════════════════════════════════════════════════════════════════════════════

🔑 **USER AUTHENTICATION & AUTHORIZATION**
─────────────────────────────────────────────────────────────────────────

**Authentication Methods (IEC 62541-4 Section 7.36):**

.. code-block:: python

   class OPCUAAuthenticationMode(Enum):
       """OPC UA user authentication modes"""
       
       ANONYMOUS = 1
       # No credentials required
       # Use case: Public read-only data
       
       USERNAME_PASSWORD = 2
       # Username + password
       # Use case: Standard industrial applications
       
       CERTIFICATE = 3
       # X.509 user certificate
       # Use case: High-security applications
       
       ISSUED_TOKEN = 4
       # Kerberos, SAML, OAuth 2.0
       # Use case: Enterprise integration

**Authorization (Role-Based Access Control):**

.. code-block:: python

   class OPCUAAuthorizationManager:
       """
       OPC UA role-based access control.
       IEC 62541-3: User roles and permissions.
       """
       
       def __init__(self):
           self.roles = {}
           self.user_roles = {}
       
       def define_role(self, role_name, permissions):
           """
           Define role with permissions.
           
           Permissions:
           - Browse: View address space
           - Read: Read variable values
           - Write: Write variable values
           - Call: Execute methods
           - Subscribe: Subscribe to data changes
           """
           self.roles[role_name] = permissions
       
       def assign_user_to_role(self, username, role_name):
           """Assign user to role"""
           if role_name not in self.roles:
               raise ValueError(f"Role {role_name} not defined")
           self.user_roles[username] = role_name
       
       def check_permission(self, username, node_id, operation):
           """
           Check if user has permission for operation on node.
           
           Returns: True/False
           """
           if username not in self.user_roles:
               print(f"User {username} not assigned to any role")
               return False
           
           role = self.user_roles[username]
           permissions = self.roles[role]
           
           if operation in permissions.get(node_id, []):
               return True
           
           # Check wildcard permissions
           if '*' in permissions and operation in permissions['*']:
               return True
           
           print(f"User {username} (role: {role}) denied {operation} on {node_id}")
           return False
   
   # Example: Configure OPC UA authorization
   auth_mgr = OPCUAAuthorizationManager()
   
   # Define roles
   auth_mgr.define_role('Operator', {
       '*': ['Browse', 'Read', 'Subscribe'],  # Read-only for all nodes
       'ns=2;i=1001': ['Write']  # Can write to specific setpoint
   })
   
   auth_mgr.define_role('Engineer', {
       '*': ['Browse', 'Read', 'Write', 'Subscribe', 'Call']  # Full access
   })
   
   auth_mgr.define_role('Administrator', {
       '*': ['Browse', 'Read', 'Write', 'Subscribe', 'Call', 'DeleteNodes', 'AddNodes']
   })
   
   # Assign users to roles
   auth_mgr.assign_user_to_role('operator1', 'Operator')
   auth_mgr.assign_user_to_role('engineer1', 'Engineer')
   
   # Check permissions
   can_write = auth_mgr.check_permission('operator1', 'ns=2;i=5000', 'Write')
   # Result: False (operators cannot write to most nodes)

════════════════════════════════════════════════════════════════════════════

🛡️ **SECURE OPC UA CLIENT/SERVER IMPLEMENTATION**
─────────────────────────────────────────────────────────────────────────

**Python OPC UA Secure Client:**

.. code-block:: python

   from opcua import Client
   from opcua.ua import SecurityPolicyType, MessageSecurityMode
   
   class SecureOPCUAClient:
       """
       Secure OPC UA client implementation.
       Uses python-opcua library with security.
       """
       
       def __init__(self, endpoint_url, cert_path, key_path):
           self.client = Client(endpoint_url)
           self.cert_path = cert_path
           self.key_path = key_path
       
       def connect_with_security(self, username=None, password=None):
           """
           Connect to OPC UA server with SignAndEncrypt security.
           
           Security Policy: Basic256Sha256 (recommended)
           Security Mode: SignAndEncrypt
           """
           # Set security policy and mode
           self.client.set_security(
               SecurityPolicyType.Basic256Sha256,
               certificate=self.cert_path,
               private_key=self.key_path,
               server_certificate_path=None  # Auto-accept (for demo)
           )
           
           # Set security mode
           self.client.set_security_mode(MessageSecurityMode.SignAndEncrypt)
           
           # Connect
           self.client.connect()
           
           # Activate session with user authentication
           if username and password:
               self.client.set_user(username)
               self.client.set_password(password)
           
           print(f"Connected to {self.client.server_url.geturl()}")
           print(f"Security: {self.client.security_policy}")
       
       def read_variable(self, node_id):
           """Read variable value from OPC UA server"""
           node = self.client.get_node(node_id)
           value = node.get_value()
           print(f"Read {node_id}: {value}")
           return value
       
       def write_variable(self, node_id, value):
           """Write variable value to OPC UA server"""
           node = self.client.get_node(node_id)
           node.set_value(value)
           print(f"Wrote {node_id}: {value}")
       
       def subscribe_to_changes(self, node_id, callback):
           """Subscribe to data changes (COV - Change of Value)"""
           subscription = self.client.create_subscription(500, callback)
           node = self.client.get_node(node_id)
           handle = subscription.subscribe_data_change(node)
           print(f"Subscribed to {node_id}")
           return handle
       
       def disconnect(self):
           """Disconnect from OPC UA server"""
           self.client.disconnect()
           print("Disconnected")
   
   # Example usage
   client = SecureOPCUAClient(
       endpoint_url="opc.tcp://scada-server:4840",
       cert_path="/etc/opcua/client.crt",
       key_path="/etc/opcua/client.key"
   )
   
   client.connect_with_security(username="operator1", password="SecurePass123!")
   
   # Read temperature sensor
   temp = client.read_variable("ns=2;i=1001")
   
   # Write setpoint
   client.write_variable("ns=2;i=1002", 72.5)
   
   client.disconnect()

════════════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────────────────────────────────────────────────────────

**Q1: Compare OPC UA security modes: None vs. Sign vs. SignAndEncrypt.**

**A1:**

| Mode | Encryption | Signature | Use Case | Risk |
|:-----|:-----------|:----------|:---------|:-----|
| **None** | ❌ No | ❌ No | Testing only | HIGH (plaintext, no auth) |
| **Sign** | ❌ No | ✅ Yes (RSA) | Integrity required, no confidentiality | MEDIUM (data visible) |
| **SignAndEncrypt** | ✅ Yes (AES-256) | ✅ Yes | Production systems | LOW (recommended) |

**Real-World Example:**

```
Scenario: SCADA reading PLC temperature data

Mode: None
├─ Data: "Temperature = 72.5°F" (plaintext UDP)
├─ Attack: Wireshark captures reveal setpoints
├─ Risk: Competitor learns production parameters

Mode: Sign
├─ Data: "Temperature = 72.5°F" + RSA signature
├─ Attack: Data still visible, but tampering detected
├─ Risk: Information disclosure (HIPAA/GDPR violation)

Mode: SignAndEncrypt
├─ Data: Encrypted blob + RSA signature
├─ Attack: Cannot read or modify
├─ Risk: Minimal (assuming strong crypto)
```

**Recommendation:** Always use **SignAndEncrypt** for production OPC UA deployments.

---

**Q2: Why does OPC UA require ApplicationURI in certificate subjectAltName?**

**A2:**

**Purpose:** Prevent certificate reuse attacks and ensure application identity.

**Problem Without ApplicationURI:**

```
Attacker scenario:
1. Attacker obtains valid X.509 certificate (any purpose)
2. Uses certificate to connect to OPC UA server
3. Server accepts (only checks certificate validity)
4. Result: Unauthorized access
```

**Solution: ApplicationURI Binding**

```
OPC UA Certificate Requirements:
├─ subjectAltName MUST contain UniformResourceIdentifier
├─ URI format: "urn:<company>:<app>:<instance>"
├─ Example: "urn:Siemens:OpcUa:PlcController:Line5"

Server validation:
1. Client presents certificate with URI: "urn:Acme:OpcUa:ScadaClient:Plant1"
2. Server extracts ApplicationURI from subjectAltName
3. Server checks: Is this URI in trusted list? → YES/NO
4. Server matches URI to endpoint configuration
5. Accept or reject connection

Result: Certificate can ONLY be used for specified OPC UA application.
```

**Real Attack Prevented:**

In 2018, researchers demonstrated OPC UA MITM attack using generic X.509 certificate. ApplicationURI requirement (IEC 62541-6) prevents this by binding certificate to specific application.

---

**Q3: Design OPC UA security for a factory with cloud connectivity.**

**A3:**

**Architecture:**

```
Cloud (Azure/AWS)
├─ OPC UA Aggregator (cloud-hosted)
├─ Security: TLS 1.3, OAuth 2.0
└─ Data: Encrypted at rest

       ↕ wss:// (WebSocket Secure)

DMZ (On-Premise Gateway)
├─ OPC UA Gateway/Edge Server
├─ Security: SignAndEncrypt, firewall
├─ Certificate: Trusted by cloud + plant
└─ Function: Protocol translation, data buffering

       ↕ opc.tcp:// (Binary TCP)

Plant Network (Isolated)
├─ OPC UA Servers (PLCs, SCADA)
├─ Security: SignAndEncrypt, VLAN isolation
└─ No direct internet access
```

**Security Controls:**

```
1. Defense-in-Depth Layers
   ├─ L1: Network segmentation (plant isolated from internet)
   ├─ L2: OPC UA Gateway (single egress point)
   ├─ L3: TLS encryption (cloud connection)
   └─ L4: Certificate-based authentication

2. Certificate Management
   ├─ Plant CA: Issues certificates for local devices
   ├─ Public CA: Issues certificate for cloud connection
   ├─ Gateway: Has both plant + cloud certificates
   └─ Certificate rotation: 1 year validity

3. Data Flow Control
   ├─ Unidirectional: Plant → Cloud (read-only)
   ├─ Cloud cannot write to PLCs directly
   ├─ Write commands: Require operator approval on-premise
   └─ Buffering: Gateway stores data if cloud unavailable

4. Access Control
   ├─ Plant operators: Full access (local network)
   ├─ Cloud users: Read-only (dashboard, analytics)
   ├─ Remote engineers: VPN + MFA (temporary write access)
   └─ Cloud APIs: Rate limiting (100 req/min)
```

**IEC 62443 Alignment:**

```
Zone 1: Cloud (SL-T = 2)
Conduit 1-2: OPC UA Gateway with TLS + firewall
Zone 2: DMZ (SL-T = 3)
Conduit 2-3: OPC UA SignAndEncrypt + VLAN
Zone 3: Plant Network (SL-T = 3)
```

---

**Q4: How to migrate from OPC Classic (DCOM) to OPC UA securely?**

**A4:**

**Challenge:** OPC Classic has NO security, uses Windows DCOM (firewall nightmare).

**Migration Strategy:**

**Phase 1: Assessment (2 weeks)**
```
├─ Inventory existing OPC Classic servers/clients
├─ Document data points (tags, alarms)
├─ Identify dependencies (third-party software)
└─ Risk assessment (what if OPC Classic compromised?)
```

**Phase 2: Parallel Deployment (3 months)**
```
Install OPC UA Servers (alongside OPC Classic):
├─ Option A: Native OPC UA (if PLC supports)
├─ Option B: OPC UA wrapper (translates Classic → UA)
├─ Option C: Gateway device (Kepware, MatrikonOPC)

Configure Security:
├─ Generate certificates for all servers/clients
├─ Set SecurityMode: SignAndEncrypt
├─ Set SecurityPolicy: Basic256Sha256
└─ Configure user roles (RBAC)

Test:
├─ Verify data integrity (OPC Classic vs. OPC UA)
├─ Performance testing (latency, throughput)
└─ Failover testing (OPC UA connection loss)
```

**Phase 3: Client Migration (6 months)**
```
Update SCADA/HMI software:
├─ Configure OPC UA endpoints (instead of Classic)
├─ Load certificates into trust store
├─ Test read/write operations

Decommission OPC Classic:
├─ Week 1: Disable 10% of Classic servers
├─ Week 2-4: Monitor for issues
├─ Month 2-6: Gradual rollout
└─ Final: Remove all OPC Classic servers
```

**Phase 4: Hardening (Ongoing)**
```
├─ Certificate rotation (annual)
├─ Audit logging (SIEM integration)
├─ Penetration testing (annual)
└─ Vulnerability monitoring (OPC Foundation advisories)
```

**Coexistence Strategy (If Full Migration Not Possible):**

```
Legacy SCADA (cannot upgrade)
   ↓ OPC Classic (DCOM)
OPC UA Gateway
   ↓ OPC UA (SignAndEncrypt)
Modern PLCs

Gateway provides:
├─ Protocol translation (Classic ↔ UA)
├─ Security enforcement (adds encryption)
├─ Network segmentation (isolates legacy)
└─ Audit logging (tracks all access)
```

---

**Q5: What are common OPC UA vulnerabilities and mitigations?**

**A5:**

**Vulnerability Database:**

| CVE | Vulnerability | Impact | Mitigation |
|:----|:--------------|:-------|:-----------|
| **CVE-2019-13976** | OPC UA .NET Stack buffer overflow | RCE | Update to OPC Foundation .NET Stack v1.4.363+ |
| **CVE-2020-15173** | OPC UA certificate validation bypass | Authentication bypass | Properly validate certificate chain |
| **CVE-2021-27434** | OPC UA XXE (XML External Entity) | Information disclosure | Disable XML external entities |
| **CVE-2022-29863** | OPC UA session hijacking | Unauthorized access | Use SignAndEncrypt mode |

**Common Misconfigurations:**

```
1. SecurityMode = None in Production
   ├─ Risk: Plaintext communication, no authentication
   └─ Fix: Set SecurityMode = SignAndEncrypt

2. Auto-Accept All Certificates
   ├─ Risk: MITM attacks, rogue clients
   └─ Fix: Manually approve certificates (trust store)

3. Anonymous Authentication Enabled
   ├─ Risk: Unauthorized data access
   └─ Fix: Require username/password or X.509 cert

4. Weak Security Policy (Basic128Rsa15)
   ├─ Risk: RSA-1024 breakable, deprecated algorithms
   └─ Fix: Use Basic256Sha256 or Aes256_Sha256_RsaPss

5. No Certificate Expiration Monitoring
   ├─ Risk: Expired certificates = connection failures
   └─ Fix: Automated certificate rotation (90 days before expiry)

6. Exposed OPC UA Server to Internet
   ├─ Risk: Brute-force attacks, vulnerability scanning
   └─ Fix: Network segmentation, VPN for remote access
```

**Security Hardening Checklist:**

```
✅ Use SignAndEncrypt mode (never None)
✅ Use Basic256Sha256 or stronger policy
✅ Require user authentication (disable Anonymous)
✅ Implement RBAC (least privilege)
✅ Enable audit logging (all Read/Write operations)
✅ Certificate validation (check expiration, revocation)
✅ Network segmentation (OPC UA VLAN)
✅ Firewall rules (only required ports)
✅ Regular updates (OPC Foundation stack patches)
✅ Penetration testing (annual)
```

**Last updated:** January 14, 2026 | **Version:** 1.0 | **Lines:** ~800
