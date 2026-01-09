
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


Here is a concise **cheatsheet for OTA (Over-The-Air) in AUTOSAR** (both Classic and Adaptive platforms), reflecting the state of the industry in early 2026 (AUTOSAR R23-11 / R24-11 dominant).

📌 1. OTA Comparison: Classic vs Adaptive AUTOSAR

| Aspect                        | AUTOSAR Classic OTA (limited support)                  | AUTOSAR Adaptive OTA (ARA::UCM)                        | Main Driver / Difference |
|-------------------------------|--------------------------------------------------------|--------------------------------------------------------|--------------------------|
| **Native OTA support**        | No dedicated module – custom or external (e.g. Mender, RAUC) | Built-in Update & Configuration Management (UCM)       | Adaptive is designed for SDV |
| **Update granularity**        | Usually full image re-flash                            | Partial / delta / rolling updates                      | Adaptive allows selective ECU updates |
| **Update process**            | Monolithic (stop → flash → reboot)                     | Stateful (manifest → download → install → activate)    | Adaptive supports A/B partitions |
| **Rollback**                  | Difficult / custom                                     | Native rollback (via UCM state machine)                | Adaptive has built-in rollback |
| **Security**                  | External signature / encryption                        | Mandatory signed manifests + authentication            | Adaptive integrates crypto & verification |
| **Communication**             | Usually CAN / Ethernet (custom)                        | SOME/IP + Ethernet (standardized)                      | Adaptive uses service-oriented |
| **Typical release year**      | 2015–2025 (still dominant in legacy)                   | 2022–2026 (L2+/L3/L4 vehicles)                         | Adaptive for modern SDV |
| **Standards compliance**      | UNECE WP.29 R156 (custom implementation)               | Native support for R156 (S-SW & V-SW)                  | Adaptive simplifies compliance |

⭐ 📌 2. AUTOSAR Adaptive OTA – Key Components (ARA::UCM)

⭐ | Module / Component             | Abbreviation | Main Responsibility / Key APIs                              | Typical Flow / Phase |
|--------------------------------|--------------|-------------------------------------------------------------|----------------------|
| **Update & Configuration Management** | UCM          | Orchestrates entire OTA process                             | Central OTA manager |
| **Update Manager**             | —            | Processes update package (download → install → activation)  | ``ProcessUpdatePackage()`` |
| **Update Package**             | —            | Signed container (manifest + payloads + signatures)         | Signed by OEM / Tier-1 |
| **Manifest**                   | —            | Describes update (version, dependencies, actions)           | XML / ARXML-based |
| **State Machine**              | —            | Tracks update states (Idle → Downloading → Installing → Activating → Done) | UCM state transitions |
| **Transfer Service**           | —            | Handles download (HTTP/HTTPS, SOME/IP)                      | ara::ucm::Transfer |
| **Activation Service**         | —            | Executes activation (reboot, partition switch)              | ara::ucm::Activation |
| **Rollback Service**           | —            | Reverts to previous version on failure                      | ara::ucm::Rollback |
| **Backup & Restore**           | —            | Optional – saves current configuration before update        | ara::ucm::Backup |

📌 3. Typical OTA Flow in Adaptive AUTOSAR (2026)

1. **Initiate Update**  
   → Cloud / backend → UCM service discovery (SOME/IP)  
2. **Download Package**  
   → UCM downloads signed package (manifest + payloads)  
⭐    → Verifies signature (public key in fuses / secure storage)  
3. **Install Phase**  
   → UCM extracts & verifies payload integrity  
   → Applies delta / full update to target partition  
4. **Activation Phase**  
   → UCM switches active partition (A/B)  
   → Reboots ECU / triggers software reset  
5. **Post-Activation**  
   → UCM reports success/failure to backend  
   → Rollback if activation fails or post-check fails  
6. **Completion**  
   → UCM updates version info  
   → Sends final status via SOME/IP

🔐 4. Security & Compliance Requirements (UNECE WP.29 R156 / ISO/SAE 21434)

| Requirement                        | Adaptive AUTOSAR Support                               | Implementation Notes (2026)                          |
|------------------------------------|--------------------------------------------------------|------------------------------------------------------|
| Signed update package              | Mandatory (UCM verifies signature)                     | ECDSA-P384 / RSA-4096, SHA-384 digest                |
| Authenticated download             | HTTPS + client certificate or SOME/IP authentication   | Mutual TLS / token-based                             |
| Integrity check                    | Manifest + payload hash verification                   | SHA-256 / SHA-384                                    |
| Anti-rollback                      | Version check in manifest                              | Version counter / monotonic counter in secure storage |
⭐ | Secure storage of keys             | TPM 2.0 / Secure Element / DICE                        | HSM or PSA Certified RoT                             |
| Audit logging                      | UCM logs all OTA actions                               | Stored in persistency or TPM PCRs                    |
| Remote attestation                 | Optional – measured boot + PCR extension               | TPM 2.0 or DICE for proof of update                  |

⚙️ 5. Popular OTA Solutions Integrated with Adaptive AUTOSAR (2026)

| Solution / Stack               | AUTOSAR Adaptive Support | OTA Granularity | Typical OEM / Tier-1 Users | Notes |
|--------------------------------|---------------------------|------------------|----------------------------|-------|
| **EB corbos UCM**              | Native                    | Partial / delta  | Continental, Bosch         | Full AUTOSAR compliance |
| **Vector MICROSAR Adaptive UCM** | Native                  | Partial          | German OEMs                | Strong tool chain integration |
| **Mender**                     | Custom integration        | Full / delta     | Many Tier-1s               | Open-source, A/B partitions |
| **RAUC**                       | Custom integration        | Full / delta     | Automotive & industrial    | Squashfs + dm-verity focus |
| **SWUpdate**                   | Custom integration        | Full / delta     | Various                    | Flexible, Yocto-friendly |
| **HARMAN / Samsung OTA**       | Native in some stacks     | Partial          | Samsung Harman customers   | Cloud-integrated |

📌 6. Quick Mnemonics & Rules of Thumb (2026)

- **Adaptive = OTA-native** — UCM is mandatory for SDV compliance (R156)
- **Classic = OTA afterthought** — usually full re-flash via custom solution
- **Signed + authenticated** — minimum for R156 / ISO 21434
- **A/B partitions** — standard pattern for rollback & atomic update
- **dm-verity** — use for rootfs integrity (even in Adaptive)
- **Anti-rollback** — version counter in secure storage / fuses
- **SOME/IP + UCM** — standard communication for OTA in Adaptive
⭐ - **ASIL D OTA** → use secure element / HSM for key storage & signing

This cheatsheet reflects the current state of OTA in AUTOSAR platforms, with Adaptive clearly dominating for modern software-defined vehicles.

🟢 🟢 Good luck with your OTA implementation!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
