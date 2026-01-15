🔒 **Secure Boot & PKI — Aircraft Systems Cheatsheet**
══════════════════════════════════════════════════════

**Technology:** Secure Boot with Public Key Infrastructure  
**Standards:** UEFI Secure Boot, NIST SP 800-147, DO-326A  
**Application:** Aircraft embedded systems, IFE platforms, avionics computers  
**⚠️ Critical:** 2026 Secure Boot Certificate Expiration Crisis

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **WHAT IS SECURE BOOT?**
───────────────────────────

Secure Boot ensures only **trusted, cryptographically signed** software can execute 
during system startup. It prevents bootkit and rootkit attacks by verifying each 
component in the boot chain.

**Why Secure Boot in Aircraft?**

✅ **Prevents unauthorized firmware:** Blocks malicious boot-time code  
✅ **Supply chain protection:** Ensures authentic OEM software  
✅ **Regulatory compliance:** Required for ED-203A SAL 2/3  
✅ **Tamper detection:** Identifies compromised systems  
✅ **Recovery assurance:** Rolls back to known-good state

**Boot Chain Without Secure Boot:**

```
Power On → BIOS/UEFI → Bootloader → OS Kernel → Applications
          (No verification, any code can run)
```

**Boot Chain With Secure Boot:**

```
Power On → UEFI Firmware
              ↓ [Verify Signature]
           Bootloader (Signed by KEK)
              ↓ [Verify Signature]
           OS Kernel (Signed by DB)
              ↓ [Verify Signature]
           Drivers & Modules (Signed)
              ↓ [Verify Signature]
           Applications (Signed)
```

════════════════════════════════════════════════════════════════════

🔑 **SECURE BOOT KEY HIERARCHY**
────────────────────────────────

**Four Key Databases:**

```
┌────────────────────────────────────────────────────────────┐
│ Platform Key (PK) — Root of Trust                          │
│ Owner: OEM (Boeing, Airbus, Panasonic Avionics)            │
│ Purpose: Controls KEK updates                              │
│ Quantity: 1 key only                                       │
└────────────────────────────────────────────────────────────┘
            ↓ Signs
┌────────────────────────────────────────────────────────────┐
│ Key Exchange Key (KEK) — Intermediate Authority            │
│ Owner: OEM + Operating System Vendor (Microsoft, Linux)    │
│ Purpose: Controls DB and DBX updates                       │
│ Quantity: Multiple keys (1-5 typical)                      │
└────────────────────────────────────────────────────────────┘
            ↓ Signs
┌────────────────────────────────────────────────────────────┐
│ Signature Database (DB) — Authorized Signers               │
│ Owner: Software vendors (bootloader, kernel, drivers)      │
│ Purpose: Whitelist of allowed software signatures          │
│ Quantity: 10-100 certificates                              │
└────────────────────────────────────────────────────────────┘
            ↓ Blocks
┌────────────────────────────────────────────────────────────┐
│ Forbidden Signature Database (DBX) — Revoked Keys          │
│ Purpose: Blacklist compromised keys/software               │
│ Quantity: Growing list (100+ entries by 2026)              │
└────────────────────────────────────────────────────────────┘
```

**Key Relationships:**

🔹 **PK** controls **KEK** (can add/remove KEK entries)  
🔹 **KEK** controls **DB & DBX** (can add/remove signatures)  
🔹 **DB** allows software to boot (whitelist)  
🔹 **DBX** blocks software from booting (blacklist)

**Certificate Format:**

- **Type:** X.509 certificates
- **Algorithm:** RSA-2048 minimum (RSA-4096 recommended for 2026+)
- **Hash:** SHA-256 (SHA-1 deprecated)
- **Validity:** 5-10 years typical

════════════════════════════════════════════════════════════════════

⚠️ **2026 SECURE BOOT CERTIFICATE CRISIS**
───────────────────────────────────────────

**The Problem:**

Many Secure Boot certificates issued in 2016-2018 have **10-year validity** 
and will **expire in June 2026**. After expiration:

❌ Systems will **refuse to boot**  
❌ Firmware updates will be **rejected**  
❌ Recovery partitions may be **inaccessible**  
❌ Grounded aircraft if not addressed

**Affected Systems:**

🔴 **High Risk:**
- IFE systems installed 2016-2019
- Avionics computers with UEFI firmware
- Ground support equipment
- Maintenance laptops

🟡 **Medium Risk:**
- Recently updated systems (certs may be refreshed)
- Systems with HSM-based key storage

🟢 **Low Risk:**
- Legacy BIOS systems (no Secure Boot)
- Systems with automated cert renewal

**Mitigation Strategy:**

**Phase 1: Assessment (Q1 2026)**

✅ Inventory all aircraft systems with Secure Boot  
✅ Extract certificate expiration dates  
✅ Prioritize by expiration timeline  
✅ Identify affected aircraft tail numbers

**Phase 2: Certificate Renewal (Q2 2026)**

✅ Obtain new certificates from OEMs  
✅ Test certificate update process  
✅ Develop rollback procedures  
✅ Train maintenance personnel

**Phase 3: Deployment (Q2-Q3 2026)**

✅ OTA updates for internet-connected systems  
✅ USB-based updates for isolated systems  
✅ Phased rollout (10 aircraft → 100 → fleet)  
✅ Verify boot success on each system

**Phase 4: Verification (Q4 2026)**

✅ Audit all systems for updated certificates  
✅ Monitor boot failures  
✅ Document lessons learned  
✅ Plan for next renewal cycle (2031-2036)

**Emergency Recovery Plan:**

If system fails to boot due to expired certificate:

1. **Enter UEFI Setup** (usually F2, Delete, or ESC during boot)
2. **Disable Secure Boot** (temporary workaround)
3. **Boot to recovery partition**
4. **Install updated certificates**
5. **Re-enable Secure Boot**
6. **Verify successful boot**

════════════════════════════════════════════════════════════════════

🏗️ **PKI ARCHITECTURE FOR AIRCRAFT**
──────────────────────────────────────

**Certificate Authority (CA) Hierarchy:**

```
┌────────────────────────────────────────────────┐
│ Root CA (Offline, HSM-protected)               │
│ Example: "Boeing Aircraft Root CA"             │
│ Validity: 20 years                             │
└────────────────────────────────────────────────┘
            ↓ Issues
┌────────────────────────────────────────────────┐
│ Intermediate CA (Online, HSM-protected)        │
│ Example: "Boeing IFE Signing CA"               │
│ Validity: 10 years                             │
└────────────────────────────────────────────────┘
            ↓ Issues
┌────────────────────────────────────────────────┐
│ End-Entity Certificates                        │
│ - Firmware signing certificates                │
│ - Code signing certificates                    │
│ - Device authentication certificates           │
│ Validity: 1-5 years                            │
└────────────────────────────────────────────────┘
```

**Certificate Types:**

🔹 **Root CA:** Long-lived, offline, rarely used  
🔹 **Intermediate CA:** Operational signing, regularly used  
🔹 **Code Signing:** For signing firmware, software updates  
🔹 **Device Certificates:** For mutual TLS, device authentication  
🔹 **TLS/SSL Certificates:** For encrypted communications

**HSM (Hardware Security Module) Integration:**

```
┌─────────────────────────────────────────┐
│ HSM (FIPS 140-2 Level 3)                │
│ ├─ Private Key Storage                  │
│ ├─ Signing Operations                   │
│ ├─ Key Generation                       │
│ └─ Tamper Detection                     │
└─────────────────────────────────────────┘
         ↑
         │ Protected Access
         ▼
┌─────────────────────────────────────────┐
│ Signing Server                          │
│ ├─ Firmware build pipeline              │
│ ├─ OTA update signing                   │
│ └─ Audit logging                        │
└─────────────────────────────────────────┘
```

**Key Ceremony:**

For high-security systems (SAL 3), key generation requires formal ceremony:

✅ **Multi-person authorization:** 3+ people required  
✅ **Physical security:** Secure facility, cameras, logs  
✅ **Witness:** Independent observer (auditor)  
✅ **Documentation:** Detailed procedure, signatures  
✅ **Backup:** Secure escrow for disaster recovery

════════════════════════════════════════════════════════════════════

🔐 **CERTIFICATE LIFECYCLE MANAGEMENT**
───────────────────────────────────────

**1. Certificate Issuance:**

```bash
# Generate private key (keep secure!)
openssl genrsa -out aircraft_signing.key 4096

# Generate Certificate Signing Request (CSR)
openssl req -new -key aircraft_signing.key \
  -out aircraft_signing.csr \
  -subj "/CN=Aircraft IFE Signing/O=Airline/C=US"

# CA signs CSR and issues certificate
# (Done by CA, not end user)
openssl x509 -req -in aircraft_signing.csr \
  -CA intermediate_ca.crt -CAkey intermediate_ca.key \
  -out aircraft_signing.crt -days 1825 -sha256
```

**2. Certificate Distribution:**

✅ **Secure channel:** HTTPS, SFTP, physical media  
✅ **Verification:** Check certificate fingerprint  
✅ **Installation:** Import into Secure Boot DB  
✅ **Testing:** Verify boot with new certificate

**3. Certificate Renewal:**

⏰ **When to renew:**
- 6 months before expiration (recommended)
- 3 months before expiration (minimum)
- Never wait until expiration!

**Renewal process:**
1. Generate new CSR with same CN (Common Name)
2. Submit to CA for signing
3. Receive new certificate
4. Test in staging environment
5. Deploy to production systems
6. Monitor for issues
7. Remove old certificate after grace period

**4. Certificate Revocation:**

**Reasons for revocation:**
- Private key compromised
- Certificate issued incorrectly
- Entity no longer authorized
- Cryptographic weakness discovered

**Revocation mechanisms:**

🔹 **CRL (Certificate Revocation List):**
- Periodically updated list of revoked certificates
- Downloaded and checked during verification
- Suitable for offline/air-gapped systems

🔹 **OCSP (Online Certificate Status Protocol):**
- Real-time revocation checking
- Requires internet connectivity
- Not suitable for isolated aircraft systems

**For aircraft, CRL is preferred** due to intermittent connectivity.

════════════════════════════════════════════════════════════════════

🔧 **IMPLEMENTATION EXAMPLE**
─────────────────────────────

**Signing Firmware for Secure Boot:**

```bash
#!/bin/bash
# Sign aircraft firmware for Secure Boot

FIRMWARE="ife_firmware_v2.5.bin"
SIGNING_KEY="aircraft_signing.key"
SIGNING_CERT="aircraft_signing.crt"
OUTPUT="ife_firmware_v2.5.signed.bin"

# Step 1: Generate hash of firmware
openssl dgst -sha256 -binary $FIRMWARE > firmware.hash

# Step 2: Sign hash with private key
openssl rsautl -sign -inkey $SIGNING_KEY \
  -in firmware.hash -out firmware.sig

# Step 3: Append signature to firmware
cat $FIRMWARE firmware.sig > $OUTPUT

# Step 4: Verify signature
openssl rsautl -verify -inkey $SIGNING_CERT -pubin \
  -in firmware.sig -out firmware.hash.verify

# Step 5: Compare hashes
if cmp -s firmware.hash firmware.hash.verify; then
  echo "✅ Firmware signed successfully"
else
  echo "❌ Signature verification failed"
  exit 1
fi

# Cleanup
rm firmware.hash firmware.sig firmware.hash.verify

echo "Signed firmware: $OUTPUT"
```

**Verifying Secure Boot Status:**

```bash
#!/bin/bash
# Check Secure Boot status on Linux system

# Method 1: Check UEFI variable
if [ -d /sys/firmware/efi ]; then
  SECUREBOOT=$(mokutil --sb-state 2>/dev/null)
  echo "Secure Boot Status: $SECUREBOOT"
else
  echo "System does not support UEFI Secure Boot"
fi

# Method 2: Check kernel log
dmesg | grep -i "secure boot"

# Method 3: Check certificates in DB
efi-readvar -v db -o db.bin
cert-to-efi-sig-list -g "" db.bin db.esl
sig-list-to-certs db.esl db
ls -l db/*.der

echo "Certificates extracted to db/ directory"
```

════════════════════════════════════════════════════════════════════

⚠️ **COMMON PITFALLS**
──────────────────────

**❌ Forgetting Certificate Expiration:**
- Problem: Certificates expire, systems won't boot
- Solution: Automated expiration monitoring, renewal 6 months early

**❌ Losing Private Keys:**
- Problem: Cannot sign new firmware without key
- Solution: Secure backup in HSM, escrow with trusted party

**❌ Single Point of Failure:**
- Problem: One compromised key affects entire fleet
- Solution: Key rotation, compartmentalization, rapid revocation

**❌ Insufficient Testing:**
- Problem: Signed firmware fails to boot in production
- Solution: Test on identical hardware before fleet deployment

**❌ No Rollback Plan:**
- Problem: Bad update bricks systems
- Solution: A/B partitions, recovery mode, known-good fallback

════════════════════════════════════════════════════════════════════

✨ **QUICK REFERENCE CARD**
───────────────────────────

**Secure Boot in 10 Points:**

1. 🔑 **4 key databases:** PK, KEK, DB, DBX
2. 🔒 **PK is root:** Controls everything else
3. ✅ **DB is whitelist:** Allows signed software to boot
4. ❌ **DBX is blacklist:** Blocks compromised software
5. 📅 **Expiration crisis:** June 2026 for 2016-era certs
6. 🔐 **HSM for keys:** FIPS 140-2 Level 3 minimum
7. 🔄 **Renew early:** 6 months before expiration
8. 🎯 **RSA-4096 minimum:** For new certificates in 2026+
9. 📜 **CRL for aircraft:** Revocation without internet
10. 🛡️ **Test before deploy:** Verify boot on identical hardware

**Certificate Lifecycle Checklist:**

✅ Generate key pair (private key in HSM)  
✅ Create CSR with correct CN  
✅ Submit CSR to CA for signing  
✅ Receive and verify certificate  
✅ Install certificate in Secure Boot DB  
✅ Test boot with new certificate  
✅ Deploy to fleet (phased rollout)  
✅ Monitor expiration (automated alerts)  
✅ Renew 6 months before expiration  
✅ Revoke if compromised (update DBX)

════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────

**Q1: What are the four Secure Boot key databases?**
→ PK (Platform Key), KEK (Key Exchange Key), DB (Signature Database), DBX (Forbidden Signature Database)

**Q2: Why is June 2026 critical for Secure Boot?**
→ Many certificates issued 2016-2018 expire (10-year validity), causing boot failures

**Q3: What is the minimum key size for new Secure Boot certificates?**
→ RSA-4096 (RSA-2048 is legacy minimum)

**Q4: How do you revoke a compromised Secure Boot certificate?**
→ Add certificate hash/signature to DBX (Forbidden Signature Database)

**Q5: What is an HSM and why is it used?**
→ Hardware Security Module — tamper-resistant device for secure key storage and signing operations

════════════════════════════════════════════════════════════════════

📚 **FURTHER READING**
──────────────────────

📖 UEFI Specification v2.10 (Secure Boot)  
📖 NIST SP 800-147 (BIOS Protection Guidelines)  
📖 NIST SP 800-147B (BIOS Protection for Servers)  
📖 DO-326A (Airworthiness Security Process Specification)  
📖 "Hacking the UEFI" — Rafal Wojtczuk & Corey Kallenberg  
📖 "UEFI Secure Boot in Modern Computer Security Solutions" — Microsoft

════════════════════════════════════════════════════════════════════

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Target Audience:** Aircraft Services Architects, Security Engineers, Firmware Developers
