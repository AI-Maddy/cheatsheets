
.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:


**cheatsheet for Secure Boot** in embedded Linux systems (2025–2026 perspective), focused on practical implementation, common chains, tools, and pitfalls in automotive, IoT, industrial, medical, and consumer devices.

📌 1. Secure Boot – Core Goals & Principles

| Goal                              | What it prevents / ensures                              | Typical Threat Mitigated                     |
|-----------------------------------|---------------------------------------------------------|----------------------------------------------|
| Authenticity                      | Only signed & trusted firmware runs                     | Malicious firmware injection                 |
| Integrity                         | No tampering with bootloader, kernel, rootfs            | Code modification / rootkits                 |
| Chain of Trust                    | Every stage verifies the next stage                     | Supply-chain attacks, persistent compromise  |
| Measured Boot                     | Cryptographic measurement (hash) of each stage          | Remote attestation (TPM / DICE)              |
| Verified Boot                     | Cryptographic verification (signature check)            | Boot-time integrity                          |

🐧 2. Typical Secure Boot Chains (Embedded Linux)

⭐ | Stage / Component          | Common Implementation (2026)                          | Verification Method                          | Typical Signer / Key Owner |
|----------------------------|-------------------------------------------------------|----------------------------------------------|----------------------------|
| **Boot ROM / Secure ROM**  | SoC fuses / immutable code                            | Hardware fuses / OTP                             | Silicon vendor             |
⭐ | **First Stage Bootloader** | U-Boot SPL / TF-A BL2 / proprietary PBL              | Public key hash in fuses / ROM                   | OEM / Silicon vendor       |
| **Second Stage Bootloader**| U-Boot proper / ATF BL31 / OP-TEE                      | RSA-2048/4096 / ECDSA-P256/P384 signature        | OEM                        |
⭐ | **Kernel (Image / FIT)**   | Linux kernel + initramfs (FIT image preferred)        | Same key or separate kernel key                  | OEM                        |
| **Device Tree / DTB**      | Appended or separate FIT component                    | Included in FIT signature                        | OEM                        |
| **Root Filesystem**        | Squashfs + dm-verity / dm-crypt + ext4/f2fs           | dm-verity (Merkle tree) or IMA/EVM               | OEM                        |
⭐ | **Root of Trust**          | Hardware (TPM 2.0, Secure Element, DICE, ARM TrustZone) | PCRs / attestation keys                          | OEM / Silicon vendor       |

💻 3. Common Secure Boot Implementations (Embedded Linux)

⭐ | Platform / Bootloader       | Secure Boot Mechanism                          | Key Features / Tools                         | Typical SoCs / Use Cases          |
|-----------------------------|------------------------------------------------|----------------------------------------------|-----------------------------------|
| **U-Boot + FIT**            | Signed FIT image (kernel + DTB + ramdisk)      | ``mkimage -f`` + ``bootm`` with signature check  | NXP i.MX, Rockchip, Allwinner, TI |
| **ARM Trusted Firmware (TF-A)** | BL2 (SPL) verifies BL31 + kernel               | Measured & verified boot, PSA Crypto         | Many ARMv8-A SoCs                 |
| **OP-TEE / TrustZone**      | Trusted OS verifies normal world               | Secure storage, RPMB, attestation            | Qualcomm, NXP, MediaTek           |
| **dm-verity**               | Integrity of rootfs (Merkle tree)              | ``veritysetup``, kernel dm-verity target       | Read-only Squashfs rootfs         |
| **TPM 2.0**                 | PCR extension + remote attestation             | tpm2-tools, tpm2-abrmd                       | Automotive, industrial            |
⭐ | **DICE (Device Identifier Composition Engine)** | Hardware-derived keys per boot stage       | TCG DICE spec, PSA Certified                 | Emerging in IoT / automotive      |

⭐ 🐧 4. Key Tools & Commands for Secure Boot (Linux Host / Target)

| Tool / Command                     | Purpose / Usage Example                                                                 | Typical Phase |
|------------------------------------|-----------------------------------------------------------------------------------------|---------------|
⭐ | ``openssl`` / ``sign-image``           | Generate RSA/ECDSA keys, sign FIT image                                                 | Development   |
⭐ | ``mkimage -f`` (U-Boot)              | Create signed FIT image: ``mkimage -f image.its -k keys/ -r image.itb``                   | Build         |
| ``fdt_add_signature``                | Add signature node to DTB (U-Boot FIT)                                                  | Build         |
| ``dm-veritysetup``                   | Create dm-verity table: ``veritysetup format rootfs.img rootfs.verity``                   | Build / OTA   |
| ``tpm2-tools``                       | PCR extend, quote, attestation: ``tpm2_pcrextend 0:sha256=...``                           | Runtime       |
| ``bootcount`` / ``bootlimit`` (U-Boot) | Rollback prevention (anti-rollback counter)                                             | Bootloader    |
| ``imx-boot`` / ``imx-sign`` (NXP)      | Sign i.MX boot images (habv4 / AHAB)                                                    | NXP-specific  |

⚙️ 5. Secure Boot Chain – Step-by-Step Verification Flow (Typical U-Boot + dm-verity)

1. **Boot ROM / Secure ROM**  
   → Verifies SPL / PBL (hash in fuses / OTP)  
2. **SPL / First Stage**  
   → Loads & verifies U-Boot proper (RSA/ECDSA signature)  
3. **U-Boot**  
   → Verifies FIT image (kernel + DTB + initramfs)  
   → Boots kernel  
4. **Kernel**  
   → Mounts dm-verity protected rootfs (Squashfs / ext4)  
   → Verifies Merkle tree root hash (in command line or initramfs)  
5. **Rootfs**  
   → Optional IMA/EVM for file-level integrity  
   → Secure OTA via RAUC / Mender / SWUpdate (signed updates)

💡 6. Common Pitfalls & Hardening Tips

| Issue / Pitfall                     | Consequence                              | Hardening / 🟢 🟢 Best Practice (2026)                          |
|-------------------------------------|------------------------------------------|------------------------------------------------------------|
⭐ | Unsigned / unverified FIT           | Easy firmware replacement                | Always use ``-k keys/`` + ``bootm`` with verification          |
⭐ | Weak keys (RSA-1024, no SHA-256)    | Forgery possible                         | RSA-4096 or ECDSA-P384 minimum, SHA-384 digest             |
| No rollback protection              | Downgrade attack                         | Use ``bootcount`` / anti-rollback fuses / version in manifest |
| Rootfs not integrity-protected      | Rootkit persistence                      | Always use dm-verity or fs-verity                          |
| Debug UART enabled in production    | Physical access → shell                  | Disable UART console (``console=``) or password protect      |
| No measured boot                    | Cannot attest boot integrity             | Extend PCRs (TPM / DICE) at each stage                     |
⭐ | OTA without authentication          | Malicious update                         | Signed packages + public key in fuses / secure storage     |

📌 7. Quick Mnemonics & Rules of Thumb

- **If you can JTAG or UART into production → Secure Boot is broken**  
- **FIT image is king** — sign everything in one blob (kernel + DTB + initramfs)  
- **dm-verity is cheap & powerful** — use it for read-only rootfs integrity  
- **Anti-rollback is mandatory** for OTA devices (fuses or persistent counter)  
- **Measured Boot** → use TPM 2.0 or DICE for remote attestation  
- **ECDSA-P384 > RSA-4096** for new designs (smaller signatures, same security)  
- **ASIL B+ / SIL 3+** → Secure Boot + dm-verity + rollback protection is baseline  

⭐ This cheatsheet covers the essentials for implementing, porting, or auditing Secure Boot on embedded Linux devices.

🟢 🟢 Good luck securing your bootloader and firmware!

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026

================================================================================

**Last updated:** January 2026
