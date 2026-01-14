📡 **OTA Updates — Aircraft Systems Cheatsheet**
════════════════════════════════════════════════

**Technology:** Over-the-Air Firmware/Software Updates  
**Standards:** DO-326A, ARINC 615A, ISO 21434  
**Application:** IFE systems, avionics, EFB (Electronic Flight Bags)  
**Security:** Critical for preventing unauthorized modifications

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **WHAT ARE OTA UPDATES?**
────────────────────────────

Over-the-Air (OTA) updates enable **remote software/firmware updates** to aircraft 
systems without physical access. This reduces maintenance costs, enables rapid bug 
fixes, and accelerates feature deployment.

**Benefits:**

✅ **Cost savings:** No technician dispatch required  
✅ **Faster updates:** Minutes vs. hours/days  
✅ **Fleet-wide deployment:** 1000+ aircraft simultaneously  
✅ **Reduced downtime:** Update during turnaround  
✅ **Emergency patches:** Critical security fixes rapidly deployed

**Risks:**

⚠️ **Unauthorized updates:** Malicious firmware injection  
⚠️ **Update failures:** Bricked systems mid-flight  
⚠️ **Network attacks:** Man-in-the-middle, replay  
⚠️ **Partial updates:** Inconsistent system state  
⚠️ **Rollback issues:** Cannot revert to previous version

════════════════════════════════════════════════════════════════════

🏗️ **OTA UPDATE ARCHITECTURE**
───────────────────────────────

**End-to-End Update Flow:**

```
┌──────────────────────────────────────────────────────────────┐
│ GROUND INFRASTRUCTURE (Airline Data Center)                  │
│ ├─ OTA Update Server (package repository)                    │
│ ├─ Signing Server (HSM-protected keys)                       │
│ ├─ Metadata Database (versions, manifests)                   │
│ └─ Monitoring Dashboard (deployment status)                  │
└──────────────────────────────────────────────────────────────┘
            ↓
    Satellite Link (Inmarsat, Iridium)
    OR Cellular (5G, 4G LTE)
    OR Ground Wi-Fi (during turnaround)
            ↓
┌──────────────────────────────────────────────────────────────┐
│ AIRCRAFT GATEWAY (Firewall, Security Proxy)                  │
│ ├─ Certificate validation                                    │
│ ├─ Rate limiting                                             │
│ ├─ Connection logging                                        │
│ └─ Intrusion detection                                       │
└──────────────────────────────────────────────────────────────┘
            ↓
    Aircraft Internal Network (ARINC 664 / Ethernet)
            ↓
┌──────────────────────────────────────────────────────────────┐
│ ONBOARD UPDATE MANAGER (Orchestration Service)               │
│ ├─ Download update packages                                  │
│ ├─ Verify signatures (ECDSA/RSA)                             │
│ ├─ Check prerequisites (version, dependencies)               │
│ ├─ Coordinate with target systems                            │
│ └─ Rollback on failure                                       │
└──────────────────────────────────────────────────────────────┘
            ↓
    System-specific installation protocol
            ↓
┌──────────────────────────────────────────────────────────────┐
│ TARGET SYSTEMS                                                │
│ ├─ IFE Seat Controllers (100-400 units per aircraft)         │
│ ├─ IFE Server (centralized content/app server)               │
│ ├─ Cabin Management System                                   │
│ ├─ Connectivity Router (Wi-Fi, cellular modem)               │
│ └─ Electronic Flight Bag (Pilot tablets)                     │
└──────────────────────────────────────────────────────────────┘
```

════════════════════════════════════════════════════════════════════

🔐 **SECURITY REQUIREMENTS**
────────────────────────────

**1. Authenticity (Origin Verification):**

🔹 **Digital Signatures:**
- Algorithm: ECDSA-P384 or RSA-4096
- Hash: SHA-256 minimum
- Certificate: Signed by trusted CA

```bash
# Sign update package
openssl dgst -sha256 -sign private_key.pem \
  -out update.sig update.bin

# Verify signature
openssl dgst -sha256 -verify public_key.pem \
  -signature update.sig update.bin
```

**2. Integrity (Tamper Detection):**

🔹 **Hash Verification:**
- Algorithm: SHA-256 or SHA-3-256
- Manifest: Lists all files + hashes
- Check: Before and after transfer

```json
{
  "manifest_version": "1.0",
  "update_id": "IFE_v3.2.1",
  "files": [
    {
      "path": "/bin/ife_server",
      "size": 15728640,
      "sha256": "a3c5f8d2e9b1..."
    },
    {
      "path": "/lib/libmedia.so",
      "size": 2097152,
      "sha256": "b7d3e9f1a4c2..."
    }
  ]
}
```

**3. Confidentiality (Eavesdropping Protection):**

🔹 **Encryption:**
- Transport: TLS 1.3 (in-transit)
- Storage: AES-256-GCM (at-rest)
- Key Management: Ephemeral session keys

**4. Rollback Protection (Version Monotonicity):**

🔹 **Anti-Rollback Counter:**
- Stored in tamper-proof storage (e.g., TPM, secure flash)
- Increments with each update
- Prevents downgrade attacks

```
Current version: 3.2.0 (counter = 320)
New version: 3.2.1 (counter = 321) ✅ Allowed
Downgrade: 3.1.9 (counter = 319) ❌ Rejected
```

**5. Atomic Updates (All-or-Nothing):**

🔹 **A/B Partitioning:**

```
┌─────────────────────────────────────────────┐
│ Flash Storage (Dual Partition)              │
│                                             │
│ ┌──────────────┐  ┌──────────────┐         │
│ │ Partition A  │  │ Partition B  │         │
│ │ (Active)     │  │ (Inactive)   │         │
│ │ Version 3.2.0│  │ Version 3.1.9│         │
│ └──────────────┘  └──────────────┘         │
│        ↑                 ↑                  │
│        │                 │                  │
│  Boot from A       Fallback to B           │
│  (if boot fails, switch to B)              │
└─────────────────────────────────────────────┘

Update Process:
1. Download new version to Partition B
2. Verify signature & integrity
3. Set boot flag to Partition B
4. Reboot
5. If boot succeeds: Mark B as active
6. If boot fails: Revert to Partition A
```

════════════════════════════════════════════════════════════════════

🔄 **UPDATE PROCESS FLOW**
──────────────────────────

**Phase 1: Pre-Update Check**

```
1. ✅ Check aircraft state
   ├─ On ground (not in flight)
   ├─ Sufficient battery/power
   ├─ Network connectivity available
   └─ No critical operations in progress

2. ✅ Check system prerequisites
   ├─ Current version compatible
   ├─ Sufficient storage space
   ├─ Dependencies satisfied
   └─ No conflicting updates in progress

3. ✅ Download update manifest
   ├─ Retrieve from update server
   ├─ Verify manifest signature
   ├─ Check update applicability
   └─ Calculate download size
```

**Phase 2: Download**

```
1. 📥 Initiate download
   ├─ Establish TLS 1.3 connection
   ├─ Authenticate server certificate
   ├─ Request update package

2. 📦 Transfer update package
   ├─ Resume capability (if interrupted)
   ├─ Progress monitoring
   ├─ Bandwidth throttling (if needed)
   └─ Timeout handling

3. ✅ Verify downloaded package
   ├─ Check file size
   ├─ Compute SHA-256 hash
   ├─ Compare with manifest
   └─ Verify digital signature
```

**Phase 3: Installation**

```
1. 🔒 Prepare for installation
   ├─ Stop affected services gracefully
   ├─ Create backup of current version
   ├─ Lock system (prevent user access)
   └─ Log installation start

2. 📂 Install update
   ├─ Extract package to temporary directory
   ├─ Verify extracted files (hash check)
   ├─ Copy files to inactive partition (A/B)
   ├─ Update configuration files
   └─ Set boot flag to new partition

3. 🔄 Reboot system
   ├─ Flush caches
   ├─ Sync filesystems
   ├─ Initiate clean reboot
   └─ Boot from new partition
```

**Phase 4: Post-Update Verification**

```
1. ✅ Boot verification
   ├─ System boots successfully
   ├─ All services start
   ├─ No critical errors in logs
   └─ Connectivity restored

2. 🔍 Functional testing
   ├─ Smoke tests pass
   ├─ Critical features operational
   ├─ Performance within acceptable range
   └─ User acceptance (if applicable)

3. 📊 Report status
   ├─ Send success/failure to ground server
   ├─ Include version information
   ├─ Upload logs (if failure)
   └─ Mark update as complete
```

**Phase 5: Rollback (If Failure)**

```
If boot fails or tests fail:

1. ⏪ Automatic rollback
   ├─ Reboot (boot fails 3 times → fallback)
   ├─ Switch boot flag to previous partition
   ├─ Boot from known-good version
   └─ Mark new version as failed

2. 📝 Failure reporting
   ├─ Collect failure logs
   ├─ Capture diagnostic data
   ├─ Report to ground server
   └─ Alert maintenance team

3. 🔒 Prevent retry
   ├─ Blacklist failed update
   ├─ Wait for revised update
   └─ Do not auto-retry same version
```

════════════════════════════════════════════════════════════════════

🎯 **DEPLOYMENT STRATEGIES**
────────────────────────────

**1. Phased Rollout (Recommended for Aircraft):**

```
Stage 1: Pilot (10 aircraft, 1-2 days)
  ├─ Diverse fleet representation
  ├─ Intensive monitoring
  ├─ Immediate rollback capability
  └─ Go/No-Go decision

Stage 2: Limited (100 aircraft, 1 week)
  ├─ 10% of fleet
  ├─ Continued monitoring
  ├─ Issue tracking
  └─ Go/No-Go decision

Stage 3: Full Deployment (Remaining aircraft, 2-4 weeks)
  ├─ Automated rollout
  ├─ Staggered by region/aircraft type
  ├─ 24/7 monitoring
  └─ Rapid response team on standby
```

**2. Blue-Green Deployment:**

```
┌─────────────────────────────────────────────┐
│ Blue Environment (Current)                  │
│ All aircraft running version 3.2.0          │
└─────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────┐
│ Green Environment (New)                     │
│ Select aircraft updated to 3.2.1            │
│ Monitor for issues (24-48 hours)            │
└─────────────────────────────────────────────┘
            ↓
      If successful:
┌─────────────────────────────────────────────┐
│ Switch all to Green (3.2.1)                 │
│ Blue becomes fallback                       │
└─────────────────────────────────────────────┘
```

**3. Canary Deployment:**

```
1% of fleet → Monitor 24h → No issues?
   ↓ YES
10% of fleet → Monitor 24h → No issues?
   ↓ YES
50% of fleet → Monitor 24h → No issues?
   ↓ YES
100% of fleet (Full rollout)
```

════════════════════════════════════════════════════════════════════

⚠️ **COMMON PITFALLS**
──────────────────────

**❌ No A/B Partitioning:**
- Problem: Failed update bricks system
- Solution: Always use dual partitions with fallback

**❌ Insufficient Testing:**
- Problem: Update works in lab, fails on aircraft
- Solution: Test on actual aircraft hardware before rollout

**❌ No Rollback Plan:**
- Problem: Cannot recover from bad update
- Solution: Automated rollback + manual recovery procedure

**❌ Weak Signature Verification:**
- Problem: Unsigned/malicious updates accepted
- Solution: Mandatory ECDSA-P384/RSA-4096 signature checks

**❌ Ignoring Dependencies:**
- Problem: Update requires newer library not present
- Solution: Dependency checking before installation

════════════════════════════════════════════════════════════════════

✨ **QUICK REFERENCE CARD**
───────────────────────────

**OTA Security Checklist:**

✅ **Authenticity:** ECDSA-P384 or RSA-4096 signatures  
✅ **Integrity:** SHA-256 hash verification  
✅ **Confidentiality:** TLS 1.3 + AES-256-GCM  
✅ **Rollback protection:** Version monotonicity counter  
✅ **Atomic updates:** A/B partitions, fallback on failure  
✅ **Phased rollout:** 10 → 100 → all aircraft

**Update Package Structure:**

```
update_package_v3.2.1.zip
├── manifest.json (signed)
├── firmware.bin (signed)
├── signature.sig (detached signature)
├── dependencies.list
└── install_script.sh
```

════════════════════════════════════════════════════════════════════

🎓 **EXAM QUESTIONS**
─────────────────────

**Q1: What are the 5 security requirements for OTA updates?**
→ Authenticity, Integrity, Confidentiality, Rollback Protection, Atomic Updates

**Q2: What is A/B partitioning and why is it important?**
→ Dual partition system where updates go to inactive partition; enables automatic rollback if boot fails

**Q3: What is the recommended phased rollout strategy?**
→ 10 aircraft (pilot) → 100 aircraft (limited) → full fleet

**Q4: What signature algorithm is recommended for 2026?**
→ ECDSA-P384 or RSA-4096 with SHA-256

**Q5: How do you prevent rollback attacks?**
→ Anti-rollback counter in tamper-proof storage (TPM), increments with each update

════════════════════════════════════════════════════════════════════

📚 **FURTHER READING**
──────────────────────

📖 ARINC 615A (Portable Data Loader)  
📖 DO-326A (Airworthiness Security Process)  
📖 ISO/SAE 21434 (Automotive Cybersecurity, OTA chapter)  
📖 "The Update Framework (TUF)" — Kuppusamy et al.  
📖 NIST SP 800-147B (BIOS/Firmware Protection)

════════════════════════════════════════════════════════════════════

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Target Audience:** Aircraft Services Architects, Firmware Engineers, DevOps Teams
