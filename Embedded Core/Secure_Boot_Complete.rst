=============================================
Secure Boot & Verified Boot Complete Guide
=============================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🔐 Overview
============

Secure Boot ensures only trusted software can execute during the boot process, protecting against rootkits, bootloaders malware, and unauthorized OS installations.

Key Concepts
------------

+---------------------------+----------------------------------------------------------+
| **Concept**               | **Description**                                          |
+===========================+==========================================================+
| Chain of Trust            | Each component verifies the next before execution        |
+---------------------------+----------------------------------------------------------+
| Root of Trust (RoT)       | Immutable hardware-anchored trust anchor                 |
+---------------------------+----------------------------------------------------------+
| Platform Key (PK)         | Top-level key establishing platform ownership            |
+---------------------------+----------------------------------------------------------+
| Key Exchange Key (KEK)    | Intermediate keys for OS-firmware trust                  |
+---------------------------+----------------------------------------------------------+
| Signature Database (DB)   | Whitelist of allowed signatures/hashes                   |
+---------------------------+----------------------------------------------------------+
| Forbidden DB (DBX)        | Blacklist of revoked/malicious signatures                |
+---------------------------+----------------------------------------------------------+
| Measured Boot             | TPM-based boot component measurements                    |
+---------------------------+----------------------------------------------------------+
| Verified Boot             | Cryptographic verification of boot components            |
+---------------------------+----------------------------------------------------------+

Boot Security Levels
--------------------

.. code-block:: text

   Level 0: No Security
   └─ Firmware → Bootloader → OS (no verification)
   
   Level 1: Basic Verification
   └─ Firmware → [Verify] Bootloader → OS
   
   Level 2: Full Chain of Trust
   └─ RoT → [Verify] Firmware → [Verify] Bootloader → [Verify] Kernel → [Verify] Modules
   
   Level 3: Measured Boot (TPM)
   └─ RoT → Measure & Verify each component → TPM sealing/attestation

🔑 UEFI Secure Boot
====================

Architecture
------------

.. code-block:: text

   Platform Key (PK)
        ├─ Controls KEK database
        └─ One key only
   
   Key Exchange Keys (KEK)
        ├─ Controls DB and DBX
        └─ Multiple keys allowed
   
   Signature Database (DB)
        ├─ Allowed signatures
        └─ Certificates and hashes
   
   Forbidden Signature Database (DBX)
        ├─ Revoked/malicious signatures
        └─ Blacklist

Key Management
--------------

**Check Secure Boot Status:**

.. code-block:: bash

   # Linux
   sudo mokutil --sb-state
   sudo dmesg | grep -i secure
   cat /sys/firmware/efi/efivars/SecureBoot-*
   
   # bootctl (systemd)
   bootctl status
   
   # UEFI Shell
   dmpstore SecureBoot
   dmpstore SetupMode

**List Enrolled Keys:**

.. code-block:: bash

   # List Platform Key
   sudo efi-readvar -v PK
   
   # List KEK
   sudo efi-readvar -v KEK
   
   # List DB
   sudo efi-readvar -v db
   
   # List DBX
   sudo efi-readvar -v dbx

Generate Keys
-------------

**Create Certificate Authority and Keys:**

.. code-block:: bash

   #!/bin/bash
   # generate-secure-boot-keys.sh
   
   OWNER="My Organization"
   CN_PK="Platform Key"
   CN_KEK="Key Exchange Key"
   CN_DB="Signature Database Key"
   
   # Create directory structure
   mkdir -p keys/{PK,KEK,db}
   cd keys
   
   # Generate UUID for key owner
   uuidgen > uuid.txt
   UUID=$(cat uuid.txt)
   
   # Platform Key (PK)
   openssl req -new -x509 -newkey rsa:2048 -subj "/CN=${CN_PK}/" \
       -keyout PK/PK.key -out PK/PK.crt -days 3650 -nodes -sha256
   
   # Key Exchange Key (KEK)
   openssl req -new -x509 -newkey rsa:2048 -subj "/CN=${CN_KEK}/" \
       -keyout KEK/KEK.key -out KEK/KEK.crt -days 3650 -nodes -sha256
   
   # Database Key (db)
   openssl req -new -x509 -newkey rsa:2048 -subj "/CN=${CN_DB}/" \
       -keyout db/db.key -out db/db.crt -days 3650 -nodes -sha256
   
   # Convert certificates to DER format
   openssl x509 -in PK/PK.crt -outform DER -out PK/PK.der
   openssl x509 -in KEK/KEK.crt -outform DER -out KEK/KEK.der
   openssl x509 -in db/db.crt -outform DER -out db/db.der
   
   # Create EFI signature lists
   cert-to-efi-sig-list -g "${UUID}" PK/PK.crt PK/PK.esl
   cert-to-efi-sig-list -g "${UUID}" KEK/KEK.crt KEK/KEK.esl
   cert-to-efi-sig-list -g "${UUID}" db/db.crt db/db.esl
   
   # Sign ESL files with keys
   sign-efi-sig-list -k PK/PK.key -c PK/PK.crt PK PK/PK.esl PK/PK.auth
   sign-efi-sig-list -k PK/PK.key -c PK/PK.crt KEK KEK/KEK.esl KEK/KEK.auth
   sign-efi-sig-list -k KEK/KEK.key -c KEK/KEK.crt db db/db.esl db/db.auth
   
   # Create empty key for Setup Mode (delete PK)
   sign-efi-sig-list -k PK/PK.key -c PK/PK.crt PK /dev/null PK/noPK.auth
   
   echo "Keys generated successfully!"
   echo "UUID: ${UUID}"
   ls -lR

Enroll Keys
-----------

**Method 1: Using efi-updatevar (Linux):**

.. code-block:: bash

   # IMPORTANT: System must be in Setup Mode
   # (Enter UEFI settings and clear all Secure Boot keys)
   
   # Enroll db key
   sudo efi-updatevar -e -f keys/db/db.esl db
   
   # Enroll KEK
   sudo efi-updatevar -e -f keys/KEK/KEK.esl KEK
   
   # Enroll PK (last step - locks Secure Boot)
   sudo efi-updatevar -f keys/PK/PK.auth PK
   
   # Verify
   sudo mokutil --sb-state

**Method 2: Using UEFI Setup:**

.. code-block:: text

   1. Copy .auth files to FAT32 USB drive
   2. Boot into UEFI Setup
   3. Navigate to Secure Boot settings
   4. Select "Enroll from file"
   5. Browse to USB and select:
      - db.auth for DB
      - KEK.auth for KEK
      - PK.auth for PK
   6. Reboot

**Method 3: Using KeyTool.efi:**

.. code-block:: bash

   # Download KeyTool
   wget https://github.com/jethrogb/KeyTool/releases/download/v1.0.1/KeyTool.efi
   
   # Copy to EFI partition
   sudo cp KeyTool.efi /boot/efi/EFI/tools/
   
   # Boot from GRUB
   menuentry 'KeyTool' {
       chainloader /EFI/tools/KeyTool.efi
   }

Sign Boot Components
--------------------

**Sign Bootloader (GRUB):**

.. code-block:: bash

   # Sign GRUB bootloader
   sudo sbsign --key keys/db/db.key --cert keys/db/db.crt \
       --output /boot/efi/EFI/ubuntu/grubx64.efi \
       /boot/efi/EFI/ubuntu/grubx64.efi
   
   # Verify signature
   sudo sbverify --cert keys/db/db.crt /boot/efi/EFI/ubuntu/grubx64.efi

**Sign Kernel:**

.. code-block:: bash

   # Sign Linux kernel
   sudo sbsign --key keys/db/db.key --cert keys/db/db.crt \
       --output /boot/vmlinuz-5.15.0-generic.signed \
       /boot/vmlinuz-5.15.0-generic
   
   # Update GRUB to use signed kernel
   # Edit /etc/grub.d/10_linux to use .signed kernels
   
   # Or use shim bootloader with MOK

**Automated Signing with DKMS:**

.. code-block:: bash

   # /etc/dkms/framework.conf
   mok_signing_key="/var/lib/shim-signed/mok/MOK.priv"
   mok_certificate="/var/lib/shim-signed/mok/MOK.der"
   sign_tool="/usr/lib/linux-kbuild-*/scripts/sign-file"

Shim Bootloader
---------------

**Using Shim for Easier Management:**

.. code-block:: bash

   # Install shim-signed
   sudo apt install shim-signed
   
   # Shim is pre-signed by Microsoft
   # Allows MOK (Machine Owner Keys) enrollment
   
   # Generate MOK keys
   sudo openssl req -new -x509 -newkey rsa:2048 \
       -keyout /var/lib/shim-signed/mok/MOK.priv \
       -out /var/lib/shim-signed/mok/MOK.pem \
       -outform PEM -subj "/CN=My MOK/" -nodes -days 3650
   
   sudo openssl x509 -in /var/lib/shim-signed/mok/MOK.pem \
       -outform DER -out /var/lib/shim-signed/mok/MOK.der
   
   # Import MOK
   sudo mokutil --import /var/lib/shim-signed/mok/MOK.der
   # Enter password when prompted
   
   # Reboot and complete enrollment in MOK Manager
   sudo reboot

**Sign with MOK:**

.. code-block:: bash

   # Sign kernel module
   sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file \
       sha256 \
       /var/lib/shim-signed/mok/MOK.priv \
       /var/lib/shim-signed/mok/MOK.der \
       /lib/modules/$(uname -r)/kernel/drivers/net/mymodule.ko
   
   # Verify
   sudo modinfo mymodule.ko | grep sig

🛡️ U-Boot Verified Boot
=========================

FIT Image Format
----------------

**Flattened Image Tree (FIT) Structure:**

.. code-block:: dts

   /dts-v1/;
   / {
       description = "Secure Boot Image";
       #address-cells = <1>;
       timestamp = <0x12345678>;
       
       images {
           kernel-1 {
               description = "Linux Kernel";
               data = /incbin/("./zImage");
               type = "kernel";
               arch = "arm";
               os = "linux";
               compression = "none";
               load = <0x80000000>;
               entry = <0x80000000>;
               hash-1 {
                   algo = "sha256";
               };
           };
           
           fdt-1 {
               description = "Device Tree Blob";
               data = /incbin/("./devicetree.dtb");
               type = "flat_dt";
               arch = "arm";
               compression = "none";
               hash-1 {
                   algo = "sha256";
               };
           };
           
           ramdisk-1 {
               description = "Initial Ram Disk";
               data = /incbin/("./initramfs.cpio.gz");
               type = "ramdisk";
               arch = "arm";
               os = "linux";
               compression = "gzip";
               hash-1 {
                   algo = "sha256";
               };
           };
       };
       
       configurations {
           default = "config-1";
           
           config-1 {
               description = "Boot Configuration";
               kernel = "kernel-1";
               fdt = "fdt-1";
               ramdisk = "ramdisk-1";
               
               signature-1 {
                   algo = "sha256,rsa2048";
                   key-name-hint = "dev";
                   sign-images = "fdt", "kernel", "ramdisk";
               };
           };
       };
   };

Generate Keys for U-Boot
-------------------------

.. code-block:: bash

   #!/bin/bash
   # Generate RSA keys for U-Boot verified boot
   
   mkdir -p keys
   
   # Generate 2048-bit RSA key
   openssl genrsa -F4 -out keys/dev.key 2048
   
   # Generate self-signed certificate
   openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt
   
   # Generate 4096-bit key (more secure)
   openssl genrsa -F4 -out keys/prod.key 4096
   openssl req -batch -new -x509 -key keys/prod.key -out keys/prod.crt
   
   # Set proper permissions
   chmod 600 keys/*.key
   chmod 644 keys/*.crt

Build Signed FIT Image
----------------------

.. code-block:: bash

   # Compile kernel ITS to FIT format
   mkimage -f kernel.its -K u-boot.dtb -k keys -r image.fit
   
   # Parameters:
   # -f: Input ITS file
   # -K: U-Boot DTB to embed public key
   # -k: Directory containing signing keys
   # -r: Perform signing
   
   # Verify signature
   fit_check_sign -f image.fit -k u-boot.dtb

U-Boot Configuration
--------------------

**Enable Verified Boot in U-Boot:**

.. code-block:: kconfig

   # configs/myboard_defconfig
   CONFIG_FIT=y
   CONFIG_FIT_SIGNATURE=y
   CONFIG_FIT_VERBOSE=y
   CONFIG_RSA=y
   CONFIG_RSA_VERIFY=y
   CONFIG_RSA_SOFTWARE_EXP=y
   CONFIG_SPL_FIT_SIGNATURE=y
   CONFIG_OF_CONTROL=y
   CONFIG_OF_SEPARATE=y
   CONFIG_DEFAULT_DEVICE_TREE="myboard"

**U-Boot Environment:**

.. code-block:: bash

   # Disable script execution without verification
   setenv verify yes
   
   # Boot only signed images
   setenv bootcmd 'fatload mmc 0:1 ${fit_addr} image.fit; bootm ${fit_addr}'

**Enforce Verification:**

.. code-block:: c

   // include/configs/myboard.h
   #define CONFIG_FIT_SIGNATURE_STRICT
   #define CONFIG_FIT_SIGNATURE_MAX_SIZE (256 * 1024)

Boot Signed FIT Image
---------------------

.. code-block:: bash

   # Load FIT image
   fatload mmc 0:1 0x80000000 image.fit
   
   # Verify and boot (automatic with CONFIG_FIT_SIGNATURE)
   bootm 0x80000000
   
   # Manual verification
   iminfo 0x80000000

SPL Verification
----------------

**Enable SPL Secure Boot:**

.. code-block:: kconfig

   CONFIG_SPL=y
   CONFIG_SPL_FIT=y
   CONFIG_SPL_FIT_SIGNATURE=y
   CONFIG_SPL_RSA=y
   CONFIG_SPL_CRYPTO_SUPPORT=y
   CONFIG_SPL_HASH_SUPPORT=y

**Boot Flow:**

.. code-block:: text

   ROM Code (Hardware RoT)
       ↓ [Verify Hash/Signature]
   SPL (u-boot-spl.bin)
       ↓ [Verify FIT Signature]
   U-Boot (u-boot.fit)
       ↓ [Verify FIT Signature]
   Linux Kernel + DTB (image.fit)

🔒 Embedded Linux Secure Boot
===============================

dm-verity (Read-Only Root)
---------------------------

**Create dm-verity Hash:**

.. code-block:: bash

   # Create hash tree for root filesystem
   sudo veritysetup format /dev/sda2 /dev/sda3 \
       --data-blocks $(blockdev --getsz /dev/sda2) \
       --hash-offset 0 > verity.log
   
   # Extract root hash
   ROOT_HASH=$(grep "Root hash" verity.log | awk '{print $3}')
   
   # Save hash to secure location (e.g., signed kernel cmdline)

**Kernel Command Line:**

.. code-block:: bash

   # Add to bootargs
   root=/dev/mapper/vroot ro \
   verity.data_device=/dev/sda2 \
   verity.hash_device=/dev/sda3 \
   verity.root_hash=${ROOT_HASH} \
   verity.hash_offset=0

**initramfs Setup:**

.. code-block:: bash

   # In initramfs init script
   veritysetup open /dev/sda2 vroot \
       /dev/sda3 ${ROOT_HASH} \
       --hash-offset=0
   
   mount -o ro /dev/mapper/vroot /mnt/root

IMA/EVM (Integrity Measurement Architecture)
---------------------------------------------

**Enable IMA in Kernel:**

.. code-block:: kconfig

   CONFIG_INTEGRITY=y
   CONFIG_IMA=y
   CONFIG_IMA_MEASURE_PCR_IDX=10
   CONFIG_IMA_APPRAISE=y
   CONFIG_IMA_TRUSTED_KEYRING=y
   CONFIG_EVM=y

**IMA Policy:**

.. code-block:: bash

   # /etc/ima/ima-policy
   
   # Measure all executables
   measure func=BPRM_CHECK
   
   # Measure all files opened for reading
   measure func=FILE_MMAP mask=MAY_EXEC
   
   # Appraise all files
   appraise func=BPRM_CHECK appraise_type=imasig
   appraise func=MODULE_CHECK appraise_type=imasig
   
   # Specific paths
   measure obj_type=usr_t func=FILE_CHECK mask=^MAY_READ
   appraise obj_type=usr_t func=FILE_CHECK mask=^MAY_READ appraise_type=imasig

**Sign Files:**

.. code-block:: bash

   # Load IMA signing key into kernel keyring
   sudo keyctl padd asymmetric "" %keyring:.ima < /path/to/key.der
   
   # Sign executable
   evmctl ima_sign --key /path/to/key.pem /usr/bin/myapp
   
   # Sign all files in directory
   find /usr/bin -type f -exec evmctl ima_sign --key /path/to/key.pem {} \;

**Boot with IMA:**

.. code-block:: bash

   # Kernel parameters
   ima_policy=tcb ima_appraise=enforce ima_appraise_tcb

TPM Integration
---------------

**Initialize TPM:**

.. code-block:: bash

   # Check TPM version
   cat /sys/class/tpm/tpm0/tpm_version_major
   
   # Take ownership (TPM 1.2)
   tpm_takeownership -z
   
   # Clear TPM (if needed)
   tpm_clear -z

**Measure Boot with TPM:**

.. code-block:: bash

   # Enable TPM in kernel
   CONFIG_TCG_TPM=y
   CONFIG_TCG_TIS=y
   CONFIG_TCG_CRB=y
   
   # Measure GRUB components
   # /etc/default/grub
   GRUB_ENABLE_CRYPTODISK=y
   
   # Measure kernel and initrd (automatically done by GRUB)

**Seal Secret with TPM:**

.. code-block:: bash

   # Seal data to specific PCR values
   tpm2_createpolicy --policy-pcr -l sha256:0,1,2,3,4,5,6,7 -f pcr.policy
   
   tpm2_create -C primary.ctx -g sha256 -G aes128 \
       -r seal.priv -u seal.pub -L pcr.policy -i secret.txt
   
   # Unseal (only works if PCRs match)
   tpm2_unseal -c seal.ctx -p pcr:sha256:0,1,2,3,4,5,6,7 -o unsealed.txt

**Remote Attestation:**

.. code-block:: bash

   # Generate quote (proof of PCR values)
   tpm2_quote -c ak.ctx -l sha256:0,1,2,3,4,5,6,7 -q 12345678 -m quote.msg -s quote.sig
   
   # Send quote.msg and quote.sig to verifier

🔐 Cryptographic Concepts
===========================

Signature Algorithms
--------------------

+-------------------+------------------+-----------------+----------------------+
| **Algorithm**     | **Key Size**     | **Security**    | **Use Case**         |
+===================+==================+=================+======================+
| RSA-2048          | 2048 bits        | Good            | Legacy compatibility |
+-------------------+------------------+-----------------+----------------------+
| RSA-4096          | 4096 bits        | Very Good       | High security        |
+-------------------+------------------+-----------------+----------------------+
| ECDSA P-256       | 256 bits         | Good            | Embedded systems     |
+-------------------+------------------+-----------------+----------------------+
| ECDSA P-384       | 384 bits         | Very Good       | Government           |
+-------------------+------------------+-----------------+----------------------+
| Ed25519           | 256 bits         | Excellent       | Modern choice        |
+-------------------+------------------+-----------------+----------------------+

Hash Functions
--------------

.. code-block:: bash

   # SHA-256 (most common)
   sha256sum file.bin
   openssl dgst -sha256 file.bin
   
   # SHA-384
   sha384sum file.bin
   
   # SHA-512
   sha512sum file.bin
   
   # In U-Boot FIT
   hash-1 {
       algo = "sha256";
   };

Key Storage
-----------

**Hardware Security Module (HSM):**

.. code-block:: text

   - Dedicated hardware for key storage
   - Keys never leave device
   - Examples: YubiKey HSM, nCipher, Thales Luna

**Trusted Platform Module (TPM):**

.. code-block:: text

   - Discrete chip on motherboard
   - Platform Configuration Registers (PCRs)
   - Secure key storage and generation
   - Versions: TPM 1.2, TPM 2.0

**Secure Element:**

.. code-block:: text

   - Embedded in SoC
   - Examples: ARM TrustZone, Intel SGX
   - Isolated execution environment

**OTP (One-Time Programmable) Memory:**

.. code-block:: text

   - eFuse, OTP-ROM
   - Permanently stores root keys
   - Cannot be modified after programming

🛠️ Toolchain & Utilities
==========================

Essential Tools
---------------

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install sbsigntool efitools mokutil \
       openssl u-boot-tools device-tree-compiler \
       tpm2-tools ima-evm-utils
   
   # RHEL/Fedora
   sudo dnf install sbsigntools efitools mokutil \
       openssl-devel uboot-tools dtc tpm2-tools ima-evm-utils

OpenSSL Commands
----------------

.. code-block:: bash

   # Generate RSA key
   openssl genrsa -out private.key 2048
   openssl genrsa -aes256 -out private_encrypted.key 4096  # Encrypted
   
   # Generate public key from private
   openssl rsa -in private.key -pubout -out public.key
   
   # Generate self-signed certificate
   openssl req -new -x509 -key private.key -out cert.crt -days 3650
   
   # Sign data
   openssl dgst -sha256 -sign private.key -out signature.sig data.bin
   
   # Verify signature
   openssl dgst -sha256 -verify public.key -signature signature.sig data.bin
   
   # View certificate
   openssl x509 -in cert.crt -text -noout
   
   # Convert formats
   openssl x509 -in cert.crt -outform DER -out cert.der
   openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem

sbsign/sbverify
---------------

.. code-block:: bash

   # Sign EFI binary
   sbsign --key db.key --cert db.crt --output signed.efi unsigned.efi
   
   # Verify signature
   sbverify --cert db.crt signed.efi
   
   # List signatures
   pesign -S -i signed.efi

mokutil
-------

.. code-block:: bash

   # Check Secure Boot state
   mokutil --sb-state
   
   # List enrolled keys
   mokutil --list-enrolled
   
   # Import MOK
   mokutil --import MOK.der
   
   # Delete MOK
   mokutil --delete MOK.der
   
   # Disable validation (requires reboot confirmation)
   mokutil --disable-validation
   
   # Test key
   mokutil --test-key MOK.der

🔧 Troubleshooting
===================

Common Issues
-------------

+----------------------------------+------------------------------------------------+
| **Issue**                        | **Solution**                                   |
+==================================+================================================+
| Secure Boot blocks Linux         | Use shim + MOK, or disable Secure Boot         |
+----------------------------------+------------------------------------------------+
| Custom kernel won't boot         | Sign kernel with enrolled key                  |
+----------------------------------+------------------------------------------------+
| Driver module load fails         | Sign module or disable Secure Boot             |
+----------------------------------+------------------------------------------------+
| U-Boot FIT verification fails    | Check key enrollment, rebuild U-Boot DTB       |
+----------------------------------+------------------------------------------------+
| TPM sealed data inaccessible     | PCRs changed, reboot to known-good state       |
+----------------------------------+------------------------------------------------+
| UEFI keys not enrolling          | Enter Setup Mode first (clear all keys)       |
+----------------------------------+------------------------------------------------+

Debug Secure Boot
-----------------

.. code-block:: bash

   # Check kernel log
   dmesg | grep -i "secure\|efi\|ima"
   
   # Verify UEFI variables
   ls -la /sys/firmware/efi/efivars/
   
   # Check module signature
   modinfo module.ko | grep sig
   
   # IMA logs
   cat /sys/kernel/security/ima/ascii_runtime_measurements
   
   # TPM PCR values
   tpm2_pcrread

Disable Secure Boot (Temporarily)
----------------------------------

.. code-block:: bash

   # From Linux (requires reboot confirmation)
   mokutil --disable-validation
   
   # From UEFI Setup
   # 1. Enter UEFI/BIOS Setup
   # 2. Navigate to Security → Secure Boot
   # 3. Set to "Disabled"
   # 4. Save and exit

Recovery Procedures
-------------------

**Lost Keys / Locked Out:**

.. code-block:: text

   1. Enter UEFI Setup
   2. Clear all Secure Boot keys (enter Setup Mode)
   3. Enroll new keys
   4. Re-sign all boot components

**Corrupted Signature:**

.. code-block:: bash

   # Boot from live USB (with Secure Boot disabled)
   # Chroot into system
   sudo mount /dev/sda2 /mnt
   sudo mount /dev/sda1 /mnt/boot/efi
   sudo mount --bind /dev /mnt/dev
   sudo mount --bind /proc /mnt/proc
   sudo mount --bind /sys /mnt/sys
   sudo chroot /mnt
   
   # Re-sign bootloader
   sbsign --key db.key --cert db.crt \
       --output /boot/efi/EFI/ubuntu/grubx64.efi \
       /boot/efi/EFI/ubuntu/grubx64.efi.original

📚 Best Practices
==================

Key Management
--------------

1. **Separate Keys by Purpose**: Different keys for PK, KEK, DB
2. **Backup Keys Securely**: Encrypted offline storage
3. **Key Rotation**: Plan for periodic key updates
4. **Access Control**: Limit who can access signing keys
5. **Hardware Storage**: Use HSM/TPM for production keys
6. **Audit Trail**: Log all signing operations

Development vs Production
--------------------------

.. code-block:: text

   Development:
   - Self-signed certificates OK
   - Shorter key lengths acceptable (2048-bit)
   - Keys can be stored on filesystem
   
   Production:
   - Certificate from trusted CA
   - Longer keys (4096-bit or ECDSA)
   - Keys in HSM/secure environment
   - Key ceremony for critical operations
   - Regular security audits

Secure Build Pipeline
---------------------

.. code-block:: yaml

   # CI/CD with secure signing
   stages:
     - build
     - sign
     - verify
     - deploy
   
   build_kernel:
     stage: build
     script:
       - make defconfig
       - make -j$(nproc)
     artifacts:
       paths:
         - vmlinuz
   
   sign_kernel:
     stage: sign
     script:
       - sbsign --key $SIGNING_KEY --cert $CERT vmlinuz
     artifacts:
       paths:
         - vmlinuz.signed
   
   verify_signature:
     stage: verify
     script:
       - sbverify --cert $CERT vmlinuz.signed

📖 Standards & Specifications
==============================

UEFI Specifications
-------------------

* **UEFI Specification 2.10**: https://uefi.org/specifications
* **UEFI Secure Boot**: Section 32
* **Platform Key Enrollment**: Section 32.3

Industry Standards
------------------

* **TPM 2.0**: ISO/IEC 11889
* **TCG PC Client Platform**: TPM 2.0 profile
* **FIPS 140-3**: Cryptographic module validation
* **Common Criteria**: Security evaluation standard

References
----------

* **Linux Kernel IMA**: Documentation/admin-guide/IMA.rst
* **U-Boot Verified Boot**: doc/uImage.FIT/verified-boot.txt
* **Shim Bootloader**: https://github.com/rhboot/shim
* **TPM2 Tools**: https://github.com/tpm2-software/tpm2-tools

================================
Last Updated: January 2026
Version: 3.0
================================
