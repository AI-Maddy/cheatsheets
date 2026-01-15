🔐 **ED-203A / DO-356A — Airworthiness Security Cheatsheet**
═════════════════════════════════════════════════════════════

**Standard:** Airworthiness Security Process Specification (ED-203A) / Methods (DO-356A)  
**Authority:** EUROCAE/RTCA  
**Version:** ED-203A (2018), DO-356A (2018)  
**Application:** Cybersecurity assurance for aircraft systems

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **WHAT IS ED-203A/DO-356A?**
────────────────────────────────

ED-203A defines the **security assurance process** for aircraft systems, while 
DO-356A provides **methods and tools** for implementing security. Together they 
form the aviation cybersecurity standard complementing DO-178C (safety) with 
security requirements.

**Key Differences from DO-178C:**

| Aspect | DO-178C (Safety) | ED-203A (Security) |
|:-------|:-----------------|:-------------------|
| **Focus** | Unintentional failures | Intentional attacks |
| **Threat** | Random faults | Malicious actors |
| **Approach** | Fault tolerance | Attack resistance |
| **Metric** | Failure probability | Attack difficulty |
| **Levels** | DAL (A-E) | SAL (1-3) |

════════════════════════════════════════════════════════════════════

🏅 **SECURITY ASSURANCE LEVELS (SAL)**
──────────────────────────────────────

**Criticality Classification:**

| SAL | Threat Model | Attacker Profile | Resources | Verification Rigor |
|:----|:-------------|:-----------------|:----------|:-------------------|
| **SAL 1** | 🟢 Casual/Coincidental | Untrained, opportunistic | Minimal | Basic security testing |
| **SAL 2** | 🟡 Intentional/Simple | Trained, limited expertise | Moderate | Security analysis required |
| **SAL 3** | 🔴 Sophisticated/Determined | Expert, organized | Significant | Independent security review |

**SAL 1 — Protection Against Casual Violations:**

✅ Passenger attempting unauthorized network access  
✅ Accidental misconfiguration exposing services  
✅ Basic input validation failures  
✅ Default credentials not changed  
✅ Unintentional protocol violations

**Example Mitigations:**
- Input validation
- Access control (basic authentication)
- Error handling
- Logging and monitoring

**SAL 2 — Protection Against Intentional, Simple Attacks:**

⚠️ Insider threat with limited expertise  
⚠️ Off-the-shelf hacking tools (Metasploit, nmap)  
⚠️ Social engineering attacks  
⚠️ Network sniffing/eavesdropping  
⚠️ Known vulnerability exploitation (CVEs)

**Example Mitigations:**
- Encryption (TLS/SSL)
- Strong authentication (multi-factor)
- Intrusion detection systems
- Regular security updates
- Security testing (penetration testing)

**SAL 3 — Protection Against Sophisticated Attacks:**

🔴 Nation-state actors or organized crime  
🔴 Custom exploit development (zero-days)  
🔴 Advanced persistent threats (APTs)  
🔴 Hardware tampering/side-channel attacks  
🔴 Supply chain compromises

**Example Mitigations:**
- Hardware security modules (HSM)
- Secure boot with TPM
- Runtime integrity verification
- Formal security analysis
- Independent security assessment
- Red team exercises

════════════════════════════════════════════════════════════════════

🔑 **KEY SECURITY CONCEPTS**
────────────────────────────

**CIA Triad:**

🔹 **Confidentiality:** Data accessible only to authorized parties  
🔹 **Integrity:** Data cannot be modified without detection  
🔹 **Availability:** System remains accessible when needed

**Additional Security Properties:**

🔹 **Authentication:** Verifying identity of users/systems  
🔹 **Authorization:** Granting appropriate access rights  
🔹 **Non-repudiation:** Proof of action (cannot deny)  
🔹 **Accountability:** Auditing who did what, when

════════════════════════════════════════════════════════════════════

🛡️ **SECURITY DEVELOPMENT PROCESS**
────────────────────────────────────

**1. Security Risk Assessment:**

```
Step 1: Identify Assets
  ├─ Flight-critical data
  ├─ Passenger PII
  ├─ Aircraft configuration
  └─ Maintenance data

Step 2: Identify Threats
  ├─ External attackers
  ├─ Malicious insiders
  ├─ Supply chain
  └─ Physical access

Step 3: Vulnerability Analysis
  ├─ Network exposure
  ├─ Software flaws
  ├─ Weak authentication
  └─ Missing encryption

Step 4: Impact Assessment
  ├─ Safety impact
  ├─ Operational impact
  ├─ Financial impact
  └─ Reputation impact

Step 5: Determine SAL
  └─ Based on threat sophistication
```

**2. Security Requirements:**

✅ **Functional Security Requirements:**
- Authentication mechanisms
- Encryption algorithms
- Access control rules
- Audit logging

✅ **Assurance Requirements:**
- Code reviews for security flaws
- Penetration testing
- Vulnerability scanning
- Security regression testing

**3. Security Architecture:**

🏗️ **Defense in Depth:**

```
Layer 1: Perimeter Security (Firewall, IDS/IPS)
  ↓
Layer 2: Network Security (VLANs, encryption)
  ↓
Layer 3: Host Security (OS hardening, EDR)
  ↓
Layer 4: Application Security (Input validation, auth)
  ↓
Layer 5: Data Security (Encryption at rest, access control)
```

**4. Security Implementation:**

✅ Secure coding practices (CERT C, MISRA)  
✅ Cryptographic libraries (FIPS 140-2 validated)  
✅ Security frameworks (OAuth, SAML)  
✅ Hardware security (TPM, secure enclaves)

**5. Security Verification:**

✅ **Static Analysis:** Code scanning for vulnerabilities  
✅ **Dynamic Analysis:** Runtime security testing  
✅ **Penetration Testing:** Ethical hacking  
✅ **Fuzz Testing:** Malformed input testing  
✅ **Threat Modeling:** STRIDE, attack trees

**6. Security Validation:**

✅ Red team exercises  
✅ Security audits  
✅ Independent security assessment (SAL 3)  
✅ Operational security monitoring

════════════════════════════════════════════════════════════════════

🎯 **THREAT MODELING**
──────────────────────

**STRIDE Methodology:**

| Threat | Description | Example in Aircraft | Mitigation |
|:-------|:------------|:--------------------|:-----------|
| **S**poofing | Impersonating another entity | Fake ground station | Mutual authentication |
| **T**ampering | Modifying data/code | Malicious firmware update | Digital signatures |
| **R**epudiation | Denying action | Pilot denies command | Audit logs, non-repudiation |
| **I**nfo Disclosure | Exposing sensitive data | Passenger data leak | Encryption, access control |
| **D**enial of Service | Preventing system use | Network flooding | Rate limiting, redundancy |
| **E**levation of Privilege | Gaining unauthorized access | Privilege escalation bug | Principle of least privilege |

**Attack Tree Example — Unauthorized IFE Access:**

```
Goal: Gain access to IFE backend
  ├─ AND
  │   ├─ Bypass authentication
  │   │   ├─ Brute force password
  │   │   ├─ Exploit auth bypass bug
  │   │   └─ Social engineering
  │   └─ Reach IFE network
  │       ├─ Passenger Wi-Fi access
  │       └─ Physical USB access
  └─ OR
      ├─ Exploit zero-day vulnerability
      └─ Supply chain compromise
```

════════════════════════════════════════════════════════════════════

🔒 **CRYPTOGRAPHIC REQUIREMENTS**
──────────────────────────────────

**Minimum Standards (2026):**

| Purpose | Algorithm | Key Size | Notes |
|:--------|:----------|:---------|:------|
| **Symmetric Encryption** | AES | 256-bit | Use GCM mode for AEAD |
| **Asymmetric Encryption** | RSA | 4096-bit | Or ECDSA P-384 |
| **Digital Signatures** | RSA | 4096-bit | Or ECDSA P-384 |
| **Hashing** | SHA-2/3 | SHA-256+ | Never MD5/SHA-1 |
| **Key Exchange** | ECDH | P-384 | Or DH 3072-bit |
| **Random Numbers** | DRBG | N/A | NIST SP 800-90A |

**Key Management:**

✅ **Generation:** Use FIPS 140-2 validated RNG  
✅ **Storage:** Hardware security module (HSM)  
✅ **Distribution:** Secure key exchange (TLS, IKE)  
✅ **Rotation:** Regular key updates (annually minimum)  
✅ **Revocation:** Certificate revocation lists (CRL)

════════════════════════════════════════════════════════════════════

📂 **REQUIRED DELIVERABLES**
────────────────────────────

**Security Planning:**

📄 **PSSS** — Plan for Security in Software Systems  
📄 **SRMP** — Security Risk Management Plan  
📄 **STR** — Security Threat Report

**Security Development:**

📄 **SSecRS** — System Security Requirements Specification  
📄 **SSA** — System Security Architecture  
📄 **SSCI** — Security-Critical Components Identification

**Security Verification:**

📄 **SVD** — Security Verification Data  
📄 **STAR** — Security Test and Analysis Report  
📄 **SVCR** — Security Verification Completion Report

**Security Assurance:**

📄 **SSecS** — System Security Summary (key deliverable!)  
📄 **SISAE** — Security Independent Security Assessment Evidence (SAL 3)

════════════════════════════════════════════════════════════════════

⚠️ **COMMON PITFALLS**
──────────────────────

**❌ Security as Afterthought:**
- Problem: Adding security late in development
- Solution: Security by design from requirements phase

**❌ Overreliance on Perimeter Security:**
- Problem: "Hard shell, soft center" architecture
- Solution: Defense in depth, zero trust

**❌ Weak Authentication:**
- Problem: Default passwords, single-factor auth
- Solution: Strong passwords + MFA for SAL 2+

**❌ Insufficient Security Testing:**
- Problem: Only functional testing, no penetration testing
- Solution: Regular pen tests, vulnerability scanning

**❌ Ignoring Supply Chain:**
- Problem: Trusting all vendors/components
- Solution: Vendor security assessment, code audits

════════════════════════════════════════════════════════════════════

✨ **QUICK REFERENCE CARD**
───────────────────────────

**ED-203A in 10 Points:**

1. 🔐 **3 SAL levels:** 1 (casual) to 3 (sophisticated)
2. 🎯 **Threat-driven:** Based on attacker capability
3. 🛡️ **Complements DO-178C:** Security + Safety
4. 📊 **Risk assessment required:** Before SAL assignment
5. 🔍 **Independent review for SAL 3:** Third-party assessment
6. 🔑 **Cryptography mandatory:** AES-256, RSA-4096 minimum
7. 🔒 **Defense in depth:** Multiple security layers
8. ✅ **Security testing:** Pen tests, fuzz tests, static analysis
9. 📝 **SSecS is key deliverable:** Security accomplishment summary
10. 🎓 **STRIDE methodology:** Common threat modeling approach

**SAL Decision Tree:**

```
What is the attacker sophistication?
  ├─ Casual/Accidental → SAL 1
  │     └─ Mitigations: Basic auth, input validation
  ├─ Intentional/Simple Tools → SAL 2
  │     └─ Mitigations: Encryption, IDS, regular updates
  └─ Sophisticated/Determined → SAL 3
        └─ Mitigations: HSM, formal analysis, red team
```

════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────

**Q1: What's the difference between SAL 1 and SAL 3?**
→ SAL 1 = casual attacker, basic mitigations  
→ SAL 3 = sophisticated attacker, independent review required

**Q2: How does ED-203A differ from DO-178C?**
→ DO-178C = safety (unintentional failures)  
→ ED-203A = security (intentional attacks)

**Q3: What are the 6 STRIDE threats?**
→ Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege

**Q4: What cryptographic minimums for 2026?**
→ AES-256, RSA-4096 (or ECDSA P-384), SHA-256+

**Q5: When is independent security assessment required?**
→ SAL 3 systems require independent review

════════════════════════════════════════════════════════════════════

📚 **FURTHER READING**
──────────────────────

📖 ED-203A (EUROCAE) / DO-356A (RTCA)  
📖 DO-326A (Airworthiness Security Process Specification)  
📖 "Threat Modeling: Designing for Security" — Adam Shostack  
📖 NIST Cybersecurity Framework  
📖 ISO/IEC 27001/27002 (Information Security)  
📖 ARINC 664 Part 8 (Network Security)

════════════════════════════════════════════════════════════════════

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Target Audience:** Aircraft Services Architects, Security Engineers, Certification Specialists
