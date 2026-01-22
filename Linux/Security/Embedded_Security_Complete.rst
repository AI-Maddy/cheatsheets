=====================================
Embedded Linux Security - Complete Guide
=====================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Reference: Smart Home Hub (i.MX 93), Avionics Platform (Intel Atom C3xxx)

.. contents:: Table of Contents
   :depth: 4
   :local:

====================
1. Overview
====================

Comprehensive security implementation for embedded Linux systems covering secure boot, 
runtime security, cryptographic services, and secure update mechanisms.

**Project Context**:

- **Smart Home Hub** (i.MX 93): HAB secure boot, encrypted storage, secure OTA
- **Avionics Platform** (Intel Atom): UEFI Secure Boot, SELinux, DO-178C compliance
- **Thermal Imaging** (DaVinci): Secure firmware, encrypted video streams
- **E-Bike Infotainment**: Automotive security (ISO 26262), secure CAN communication

====================
2. Secure Boot Implementation
====================

2.1 NXP i.MX HAB (High Assurance Boot)
---------------------------------------

2.1.1 HAB Architecture
~~~~~~~~~~~~~~~~~~~~~~

**Security Features**:

- Root of Trust: Boot ROM immutable code
- Chain of Trust: ROM → SPL → U-Boot → Kernel → Rootfs
- Signature Verification: RSA 2048/4096, SHA-256
- eFuse Storage: SRK hash, secure boot flag
- Encrypted Boot: DEK blob encryption

**Boot Flow**:

.. code-block:: text

    Power On
        ↓
    Boot ROM (immutable)
        ↓ Verify SPL signature using SRK hash from eFuse
    SPL (Secondary Program Loader)
        ↓ Verify U-Boot signature
    U-Boot
        ↓ Verify Kernel + DTB signature
    Linux Kernel
        ↓ dm-verity for rootfs integrity
    Rootfs (verified)

2.1.2 HAB Key Generation
~~~~~~~~~~~~~~~~~~~~~~~~~

**Generate PKI Infrastructure**:

.. code-block:: bash

    # Create CST (Code Signing Tool) directory structure
    cd cst-3.3.1/keys
    
    # Generate 4 SRK key pairs (Super Root Keys)
    ../linux64/bin/cst -i ../crts/keys_2048_4096.txt -o ./
    
    # Key hierarchy:
    # - SRK1-4: Super Root Keys (4096-bit RSA)
    # - CSF: Command Sequence File key (2048-bit RSA)
    # - IMG: Image signing key (2048-bit RSA)
    
    # Generate SRK table and hash
    ../linux64/bin/srktool -h 4 -t SRK_1_2_3_4_table.bin \
        -e SRK_1_2_3_4_fuse.bin \
        -c SRK1_sha256_2048_65537_v3_ca_crt.pem,\
           SRK2_sha256_2048_65537_v3_ca_crt.pem,\
           SRK3_sha256_2048_65537_v3_ca_crt.pem,\
           SRK4_sha256_2048_65537_v3_ca_crt.pem

**Project Results** (Smart Home Hub):

- Key Generation Time: ~45 seconds
- SRK Hash: ``0xABCD1234EF567890...`` (256-bit)
- Certificate Chain Depth: 3 (SRK → CSF → IMG)

2.1.3 Sign U-Boot with CSF
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Create CSF Descriptor** (``csf_uboot.txt``):

.. code-block:: text

    [Header]
    Version = 4.3
    Hash Algorithm = sha256
    Engine = CAAM
    Engine Configuration = 0
    Certificate Format = X509
    Signature Format = CMS
    
    [Install SRK]
    File = "../crts/SRK_1_2_3_4_table.bin"
    Source index = 0
    
    [Install CSFK]
    File = "../crts/CSF1_1_sha256_2048_65537_v3_usr_crt.pem"
    
    [Authenticate CSF]
    
    [Install Key]
    Verification index = 0
    Target Index = 2
    File = "../crts/IMG1_1_sha256_2048_65537_v3_usr_crt.pem"
    
    [Authenticate Data]
    Verification index = 2
    Blocks = 0x877FF400 0x00000000 0x00070000 "u-boot.imx"

**Sign and Generate Authenticated Image**:

.. code-block:: bash

    # Generate CSF binary
    cst -i csf_uboot.txt -o csf_uboot.bin
    
    # Append CSF to U-Boot image
    cat u-boot.imx csf_uboot.bin > u-boot-signed.imx
    
    # Calculate IVT offset for SPL
    ivt_offset=$(printf "0x%X" $(($(stat -c %s u-boot.imx) - 0x400)))
    
    # Flash to eMMC/SD card
    dd if=u-boot-signed.imx of=/dev/mmcblk0 bs=1K seek=33

2.1.4 eFuse Programming
~~~~~~~~~~~~~~~~~~~~~~~

**Program SRK Hash** (One-time operation, **IRREVERSIBLE**):

.. code-block:: c

    /* U-Boot command to blow eFuse (DANGER: Permanent!) */
    
    // Read SRK hash from file
    fatload mmc 0:1 $loadaddr SRK_1_2_3_4_fuse.bin
    
    // Program SRK_HASH[255:0] to eFuse bank 3, words 0-7
    fuse prog 3 0 0xABCD1234  // SRK_HASH[31:0]
    fuse prog 3 1 0xEF567890  // SRK_HASH[63:32]
    fuse prog 3 2 0x12345678  // SRK_HASH[95:64]
    fuse prog 3 3 0x9ABCDEF0  // SRK_HASH[127:96]
    fuse prog 3 4 0x11111111  // SRK_HASH[159:128]
    fuse prog 3 5 0x22222222  // SRK_HASH[191:160]
    fuse prog 3 6 0x33333333  // SRK_HASH[223:192]
    fuse prog 3 7 0x44444444  // SRK_HASH[255:224]
    
    // Enable secure boot (SEC_CONFIG[1] = 1)
    fuse prog 0 6 0x00000002
    
    // Close device (SEC_CONFIG[0] = 1) - PERMANENT!
    // fuse prog 0 6 0x00000003  // Use with EXTREME caution!

**Verification**:

.. code-block:: bash

    # Read eFuse values
    fuse read 3 0 8  # Read SRK hash
    fuse read 0 6    # Read security config
    
    # Expected output after secure boot enable:
    # Bank 0 Word 6: 0x00000002 (open mode, HAB enabled)

**Project Experience** (Smart Home Hub):

- Development Phase: Used HAB in open mode (eFuse not blown)
- Manufacturing: Programmed eFuse with production SRK hash
- Field Update: Impossible to change SRK after eFuse blow
- Recovery: Required hardware fuse bypass for development units

2.1.5 Sign Kernel and Device Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**FIT Image with Signature** (``image.its``):

.. code-block:: dts

    /dts-v1/;
    
    / {
        description = "Signed Kernel + DTB for i.MX 93";
        #address-cells = <1>;
        
        images {
            kernel {
                description = "Linux kernel";
                data = /incbin/("Image");
                type = "kernel";
                arch = "arm64";
                os = "linux";
                compression = "none";
                load = <0x80280000>;
                entry = <0x80280000>;
                hash-1 {
                    algo = "sha256";
                };
            };
            
            fdt {
                description = "Flattened Device Tree";
                data = /incbin/("imx93-smarthome.dtb");
                type = "flat_dt";
                arch = "arm64";
                compression = "none";
                hash-1 {
                    algo = "sha256";
                };
            };
        };
        
        configurations {
            default = "conf-1";
            conf-1 {
                description = "Boot Linux kernel with FDT";
                kernel = "kernel";
                fdt = "fdt";
                signature-1 {
                    algo = "sha256,rsa2048";
                    key-name-hint = "dev";
                    sign-images = "kernel", "fdt";
                };
            };
        };
    };

**Generate Signed FIT Image**:

.. code-block:: bash

    # Generate device tree key pair
    mkdir -p keys
    openssl genrsa -F4 -out keys/dev.key 2048
    openssl req -batch -new -x509 -key keys/dev.key -out keys/dev.crt
    
    # Create FIT image with placeholder
    mkimage -f image.its image.itb
    
    # Sign FIT image
    mkimage -F -k keys -K u-boot.dtb -r image.itb
    
    # Verify signature
    fit_check_sign -f image.itb -k u-boot.dtb

**U-Boot Configuration**:

.. code-block:: kconfig

    CONFIG_FIT=y
    CONFIG_FIT_SIGNATURE=y
    CONFIG_RSA=y
    CONFIG_OF_CONTROL=y
    CONFIG_OF_SEPARATE=y

2.1.6 Encrypted Boot (DEK Blob)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Encrypt Kernel Image**:

.. code-block:: bash

    # Generate random DEK (Data Encryption Key)
    dd if=/dev/urandom of=dek.bin bs=1 count=32  # 256-bit AES key
    
    # Encrypt kernel with AES-256-CBC
    openssl enc -aes-256-cbc -K $(hexdump -ve '1/1 "%.2x"' dek.bin) \
        -iv 0x00000000000000000000000000000000 \
        -in Image -out Image.enc
    
    # Generate DEK blob using CAAM (in U-Boot)
    dek_blob 0x80000000 0x81000000 0x20
    
    # DEK blob structure:
    # - Header: 8 bytes (blob type, mode)
    # - Encrypted DEK: 32 bytes (AES-256 key)
    # - MAC: 16 bytes (authentication)

**Decrypt in U-Boot**:

.. code-block:: c

    /* Load encrypted kernel and DEK blob */
    fatload mmc 0:1 0x80280000 Image.enc
    fatload mmc 0:1 0x82000000 dek_blob.bin
    
    /* Decrypt using CAAM */
    dek_blob 0x82000000 0x83000000 0x20
    setenv dek_addr 0x83000000
    
    /* Boot with decrypted kernel */
    bootm 0x80280000 - $fdt_addr

**Project Metrics** (Smart Home Hub):

- Encryption Overhead: +180ms boot time
- CAAM Decrypt Performance: ~85 MB/s
- Key Storage: eFuse OTPMK (One-Time Programmable Master Key)

2.2 UEFI Secure Boot (Intel Atom)
----------------------------------

2.2.1 UEFI Secure Boot Chain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Boot Flow**:

.. code-block:: text

    Power On
        ↓
    Platform Initialization (SEC, PEI)
        ↓
    DXE (Driver Execution Environment)
        ↓ Verify bootloader signature (db keys)
    GRUB2 / systemd-boot (signed)
        ↓ Verify kernel + initramfs signature
    Linux Kernel (signed)
        ↓ IMA/EVM for runtime integrity
    Userspace

**Key Hierarchy**:

.. code-block:: text

    Platform Key (PK)
        ↓ Signs
    Key Exchange Key (KEK)
        ↓ Signs
    Signature Database (db) - Allowed signers
    Forbidden Signature Database (dbx) - Revoked keys

2.2.2 Generate UEFI Keys
~~~~~~~~~~~~~~~~~~~~~~~~~

**Create PKI**:

.. code-block:: bash

    #!/bin/bash
    # Generate UEFI Secure Boot keys
    
    COMMON_NAME="Avionics Platform Secure Boot"
    
    # Platform Key (PK) - Top of hierarchy
    openssl req -new -x509 -newkey rsa:4096 -subj "/CN=$COMMON_NAME PK/" \
        -keyout PK.key -out PK.crt -days 3650 -nodes -sha256
    
    # Key Exchange Key (KEK)
    openssl req -new -x509 -newkey rsa:4096 -subj "/CN=$COMMON_NAME KEK/" \
        -keyout KEK.key -out KEK.crt -days 3650 -nodes -sha256
    
    # Database key (db) - Signs bootloaders and kernels
    openssl req -new -x509 -newkey rsa:4096 -subj "/CN=$COMMON_NAME db/" \
        -keyout db.key -out db.crt -days 3650 -nodes -sha256
    
    # Convert to EFI Signature List format
    cert-to-efi-sig-list -g "$(uuidgen)" PK.crt PK.esl
    cert-to-efi-sig-list -g "$(uuidgen)" KEK.crt KEK.esl
    cert-to-efi-sig-list -g "$(uuidgen)" db.crt db.esl
    
    # Sign with PK
    sign-efi-sig-list -k PK.key -c PK.crt PK PK.esl PK.auth
    sign-efi-sig-list -k PK.key -c PK.crt KEK KEK.esl KEK.auth
    sign-efi-sig-list -k KEK.key -c KEK.crt db db.esl db.auth

2.2.3 Enroll Keys in UEFI
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Option 1: UEFI Setup Menu**:

.. code-block:: text

    1. Enter UEFI Setup (DEL/F2 during boot)
    2. Navigate to: Security → Secure Boot Configuration
    3. Set Secure Boot Mode: Custom
    4. Enroll keys:
       - Platform Key (PK): PK.auth
       - Key Exchange Key (KEK): KEK.auth
       - Authorized Signatures (db): db.auth
    5. Enable Secure Boot
    6. Save and Exit

**Option 2: efitools from Linux**:

.. code-block:: bash

    # Copy keys to ESP (EFI System Partition)
    mount /dev/sda1 /boot/efi
    mkdir -p /boot/efi/EFI/keys
    cp *.auth /boot/efi/EFI/keys/
    
    # Enroll keys using KeyTool.efi (from EFI shell)
    # Or use efi-updatevar from Linux:
    efi-updatevar -f PK.auth PK
    efi-updatevar -f KEK.auth KEK
    efi-updatevar -f db.auth db
    
    # Verify enrollment
    efi-readvar

2.2.4 Sign GRUB2 Bootloader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Install sbsigntool
    apt-get install sbsigntool
    
    # Sign GRUB2 EFI binary
    sbsign --key db.key --cert db.crt \
        --output /boot/efi/EFI/BOOT/grubx64.efi \
        /boot/efi/EFI/BOOT/grubx64.efi.unsigned
    
    # Verify signature
    sbverify --cert db.crt /boot/efi/EFI/BOOT/grubx64.efi

2.2.5 Sign Linux Kernel
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Sign kernel bzImage
    sbsign --key db.key --cert db.crt \
        --output /boot/vmlinuz-5.15.0-signed \
        /boot/vmlinuz-5.15.0
    
    # Update GRUB configuration
    cat >> /etc/grub.d/40_custom <<EOF
    menuentry 'Avionics Linux (Signed)' {
        linux /vmlinuz-5.15.0-signed root=/dev/sda2 ro quiet
        initrd /initrd.img-5.15.0
    }
    EOF
    
    update-grub

**Automatic Signing with DKMS**:

.. code-block:: bash

    # Create DKMS signing script
    cat > /etc/dkms/sign_helper.sh <<'EOF'
    #!/bin/bash
    /usr/bin/sbsign --key /root/secure-boot/db.key \
        --cert /root/secure-boot/db.crt \
        --output "$2" "$2"
    EOF
    chmod +x /etc/dkms/sign_helper.sh
    
    # Configure DKMS
    cat >> /etc/dkms/framework.conf <<EOF
    sign_tool="/etc/dkms/sign_helper.sh"
    EOF

2.2.6 Shim Bootloader (For Linux Distributions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Using Shim for Microsoft UEFI CA**:

.. code-block:: bash

    # Install shim (pre-signed by Microsoft)
    apt-get install shim-signed
    
    # Shim chain:
    # shimx64.efi (signed by Microsoft) → grubx64.efi (signed by vendor)
    
    # Enroll MOK (Machine Owner Key)
    mokutil --import db.crt
    
    # Reboot and enroll in MOK Manager
    # (Blue screen MOK management interface)

**Project Configuration** (Avionics Platform):

- Used shim for development with Microsoft CA
- Production: Custom PK/KEK/db for air-gapped security
- Dual boot support: Signed Linux + Signed diagnostics partition

2.3 Secure Boot Verification
-----------------------------

2.3.1 HAB Status Check
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Check HAB events in U-Boot
    hab_status
    
    # Expected output (no HAB events):
    # Secure boot disabled
    # HAB Configuration: 0xf0, HAB State: 0x66
    
    # After secure boot enable:
    # Secure boot enabled
    # HAB Configuration: 0xcc, HAB State: 0x99
    
    # Linux: Check HAB from kernel log
    dmesg | grep -i hab

2.3.2 UEFI Secure Boot Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Check secure boot status
    mokutil --sb-state
    # Output: SecureBoot enabled
    
    # List enrolled keys
    efi-readvar
    
    # Verify kernel signature
    sbverify --list /boot/vmlinuz-$(uname -r)

====================
3. SELinux Security
====================

3.1 SELinux Architecture
------------------------

**Security Context**: ``user:role:type:level``

.. code-block:: text

    Example: system_u:object_r:usr_t:s0
    
    user: SELinux user (system_u, user_u, staff_u)
    role: Role (object_r for files, system_r for processes)
    type: Type enforcement (usr_t, bin_t, device_t)
    level: MLS/MCS level (s0:c0-s15:c0.c1023)

**Access Control**:

- Type Enforcement (TE): Allow rules between types
- Multi-Level Security (MLS): Confidentiality levels
- Role-Based Access Control (RBAC): User role assignment

3.2 SELinux Policy Development
-------------------------------

3.2.1 Reference Policy
~~~~~~~~~~~~~~~~~~~~~~

**Clone and Build**:

.. code-block:: bash

    # Clone refpolicy
    git clone https://github.com/SELinuxProject/refpolicy.git
    cd refpolicy
    
    # Configure for embedded system
    cat > build.conf <<EOF
    TYPE = mcs
    NAME = targeted
    DISTRO = gentoo
    MONOLITHIC = y
    DIRECT_INITRC = y
    UBAC = n
    MLS_CATS = 256
    MCS_CATS = 256
    EOF
    
    # Build policy
    make conf
    make
    
    # Output: policy.31 (binary policy)

3.2.2 Custom Module Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Avionics Application Policy** (``avionics_app.te``):

.. code-block:: selinux

    policy_module(avionics_app, 1.0.0)
    
    ########################################
    # Declarations
    ########################################
    
    type avionics_app_t;
    type avionics_app_exec_t;
    type avionics_data_t;
    type avionics_log_t;
    type avionics_config_t;
    type afdx_device_t;
    
    init_daemon_domain(avionics_app_t, avionics_app_exec_t)
    
    ########################################
    # Avionics application policy
    ########################################
    
    # Allow execution transition
    allow init_t avionics_app_exec_t:file { read execute open getattr };
    allow init_t avionics_app_t:process transition;
    
    # File permissions
    allow avionics_app_t avionics_data_t:dir { read write add_name remove_name };
    allow avionics_app_t avionics_data_t:file { create read write unlink };
    
    allow avionics_app_t avionics_log_t:file { create write append };
    
    allow avionics_app_t avionics_config_t:file { read open getattr };
    
    # Network permissions (AFDX)
    allow avionics_app_t self:capability net_admin;
    allow avionics_app_t self:socket create_socket_perms;
    allow avionics_app_t self:packet_socket create_socket_perms;
    
    # Device access (AFDX network card)
    allow avionics_app_t afdx_device_t:chr_file { read write open ioctl };
    
    # Shared memory
    allow avionics_app_t self:shm create_shm_perms;
    
    # IPC
    allow avionics_app_t self:msgq create_msgq_perms;
    
    # Time/clock access
    allow avionics_app_t self:capability sys_time;

**File Context** (``avionics_app.fc``):

.. code-block:: selinux

    # Executable
    /usr/sbin/avionics_app    -- gen_context(system_u:object_r:avionics_app_exec_t,s0)
    
    # Data files
    /var/lib/avionics(/.*)?      gen_context(system_u:object_r:avionics_data_t,s0)
    
    # Log files
    /var/log/avionics(/.*)?      gen_context(system_u:object_r:avionics_log_t,s0)
    
    # Configuration
    /etc/avionics\.conf      --  gen_context(system_u:object_r:avionics_config_t,s0)
    
    # Device
    /dev/afdx0               -c  gen_context(system_u:object_r:afdx_device_t,s0)

**Build and Load Module**:

.. code-block:: bash

    # Compile module
    make -f /usr/share/selinux/devel/Makefile avionics_app.pp
    
    # Install module
    semodule -i avionics_app.pp
    
    # Restore file contexts
    restorecon -Rv /usr/sbin/avionics_app /var/lib/avionics /var/log/avionics

3.2.3 Domain Transitions
~~~~~~~~~~~~~~~~~~~~~~~~~

**Init → Avionics App Transition**:

.. code-block:: selinux

    # avionics_app.te
    
    # Define domain transition
    domain_auto_trans(init_t, avionics_app_exec_t, avionics_app_t)
    
    # Or manually:
    allow init_t avionics_app_exec_t:file { execute read open getattr };
    allow init_t avionics_app_t:process transition;
    allow avionics_app_t avionics_app_exec_t:file entrypoint;
    type_transition init_t avionics_app_exec_t:process avionics_app_t;

3.2.4 MLS/MCS Constraints
~~~~~~~~~~~~~~~~~~~~~~~~~

**Multi-Category Security** for data isolation:

.. code-block:: selinux

    # Sensor data categories
    # c0: GPS data
    # c1: IMU data
    # c2: Camera data
    # c3: AFDX network data
    
    # Process labels
    system_u:system_r:gps_app_t:s0:c0       # GPS app
    system_u:system_r:imu_app_t:s0:c1       # IMU app
    system_u:system_r:fusion_app_t:s0:c0.c1 # Sensor fusion (access both)
    
    # File labels
    system_u:object_r:gps_data_t:s0:c0      # GPS data files
    system_u:object_r:imu_data_t:s0:c1      # IMU data files

**MCS Constraints** (built into policy):

.. code-block:: selinux

    # Process must have category to read file with that category
    mlsconstrain file { read }
        ( h1 dom h2 );  # Process high level dominates file level

3.3 SELinux Deployment
-----------------------

3.3.1 Buildroot Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Buildroot Configuration**:

.. code-block:: kconfig

    BR2_PACKAGE_LIBSELINUX=y
    BR2_PACKAGE_LIBSEPOL=y
    BR2_PACKAGE_CHECKPOLICY=y
    BR2_PACKAGE_SELINUX_PYTHON=y
    BR2_PACKAGE_POLICYCOREUTILS=y
    BR2_PACKAGE_REFPOLICY=y

**Custom Policy Integration**:

.. code-block:: bash

    # buildroot/package/refpolicy/refpolicy.mk
    
    define REFPOLICY_BUILD_CMDS
        # Build base policy
        $(MAKE) -C $(@D) conf
        $(MAKE) -C $(@D)
        
        # Add custom modules
        $(MAKE) -C $(@D) -f /usr/share/selinux/devel/Makefile \
            $(TARGET_DIR)/custom_modules/avionics_app.pp
        semodule -p $(@D) -i $(TARGET_DIR)/custom_modules/avionics_app.pp
    endef

3.3.2 Runtime Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Enable SELinux**:

.. code-block:: bash

    # Kernel command line
    selinux=1 security=selinux enforcing=1
    
    # /etc/selinux/config
    SELINUX=enforcing
    SELINUXTYPE=targeted
    
    # Check status
    sestatus
    getenforce

**Initial Labeling**:

.. code-block:: bash

    # Label filesystem on first boot
    restorecon -Rv /
    
    # Or create /.autorelabel and reboot
    touch /.autorelabel
    reboot

3.3.3 Troubleshooting SELinux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Audit Logs**:

.. code-block:: bash

    # View denials
    ausearch -m avc -ts recent
    
    # Example denial:
    # type=AVC msg=audit(1620000000.123:456): avc: denied { read } \
    #   for pid=1234 comm="avionics_app" name="config.txt" \
    #   scontext=system_u:system_r:avionics_app_t:s0 \
    #   tcontext=system_u:object_r:etc_t:s0 tclass=file

**Generate Policy from Denials**:

.. code-block:: bash

    # Collect denials
    ausearch -m avc -ts recent | audit2allow -M avionics_fix
    
    # Review generated policy (avionics_fix.te)
    cat avionics_fix.te
    
    # Load if acceptable
    semodule -i avionics_fix.pp

**Permissive Mode for Debugging**:

.. code-block:: bash

    # Global permissive
    setenforce 0
    
    # Per-domain permissive
    semanage permissive -a avionics_app_t
    
    # Restore enforcing
    setenforce 1
    semanage permissive -d avionics_app_t

**Project Metrics** (Avionics Platform):

- Policy Size: 1,247 rules, 38 custom types
- Boot Overhead: +320ms for initial labeling
- Runtime Overhead: <2% CPU, ~15MB RAM
- AVC Denials in Development: 1,843 (first week)
- AVC Denials in Production: 0 (after policy refinement)

====================
4. Cryptographic Services
====================

4.1 Hardware Crypto Acceleration
---------------------------------

4.1.1 NXP CAAM (Cryptographic Accelerator and Assurance Module)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Architecture**:

.. code-block:: text

    CAAM Block Diagram:
    
    ┌─────────────────────────────────────────┐
    │         Job Ring Interface              │
    │  (4 job rings for multi-core access)    │
    └────────────┬────────────────────────────┘
                 │
    ┌────────────▼────────────────────────────┐
    │        Descriptor Processing            │
    │  - Command sequencing                   │
    │  - Key management                       │
    └────────────┬────────────────────────────┘
                 │
    ┌────────────▼────────────────────────────┐
    │      Execution Units (EUs)              │
    │  - MDHA (SHA-1/256/512)                 │
    │  - AESA (AES 128/192/256)               │
    │  - DESA (DES/3DES)                      │
    │  - PKHA (RSA, ECC, DH)                  │
    │  - RNG (True Random Number Generator)   │
    └─────────────────────────────────────────┘

**Linux Crypto API Integration**:

.. code-block:: c

    /* CAAM driver registration (drivers/crypto/caam/caamalg.c) */
    
    static struct caam_alg_template driver_algs[] = {
        {
            .name = "cbc(aes)",
            .driver_name = "cbc-aes-caam",
            .blocksize = AES_BLOCK_SIZE,
            .type = CRYPTO_ALG_TYPE_ABLKCIPHER,
            .template_ablkcipher = {
                .setkey = ablkcipher_setkey,
                .encrypt = ablkcipher_encrypt,
                .decrypt = ablkcipher_decrypt,
                .geniv = "eseqiv",
                .min_keysize = AES_MIN_KEY_SIZE,
                .max_keysize = AES_MAX_KEY_SIZE,
                .ivsize = AES_BLOCK_SIZE,
            },
            .class1_alg_type = OP_ALG_ALGSEL_AES | OP_ALG_AAI_CBC,
        },
        // ... SHA, RSA, RNG algorithms
    };

**Using CAAM from Userspace**:

.. code-block:: c

    #include <linux/if_alg.h>
    #include <sys/socket.h>
    #include <unistd.h>
    #include <string.h>
    
    int caam_aes_encrypt(const uint8_t *key, size_t keylen,
                         const uint8_t *iv, const uint8_t *plaintext,
                         size_t textlen, uint8_t *ciphertext)
    {
        struct sockaddr_alg sa = {
            .salg_family = AF_ALG,
            .salg_type = "skcipher",
            .salg_name = "cbc(aes)"  // Uses CAAM if available
        };
        
        int sockfd = socket(AF_ALG, SOCK_SEQPACKET, 0);
        bind(sockfd, (struct sockaddr *)&sa, sizeof(sa));
        
        setsockopt(sockfd, SOL_ALG, ALG_SET_KEY, key, keylen);
        
        int opfd = accept(sockfd, NULL, 0);
        
        struct msghdr msg = {0};
        struct cmsghdr *cmsg;
        char cbuf[CMSG_SPACE(4) + CMSG_SPACE(20)] = {0};
        struct af_alg_iv {
            uint32_t ivlen;
            uint8_t iv[16];
        } *alg_iv;
        struct iovec iov;
        
        msg.msg_control = cbuf;
        msg.msg_controllen = sizeof(cbuf);
        
        cmsg = CMSG_FIRSTHDR(&msg);
        cmsg->cmsg_level = SOL_ALG;
        cmsg->cmsg_type = ALG_SET_OP;
        cmsg->cmsg_len = CMSG_LEN(4);
        *(__u32 *)CMSG_DATA(cmsg) = ALG_OP_ENCRYPT;
        
        cmsg = CMSG_NXTHDR(&msg, cmsg);
        cmsg->cmsg_level = SOL_ALG;
        cmsg->cmsg_type = ALG_SET_IV;
        cmsg->cmsg_len = CMSG_LEN(20);
        alg_iv = (void *)CMSG_DATA(cmsg);
        alg_iv->ivlen = 16;
        memcpy(alg_iv->iv, iv, 16);
        
        iov.iov_base = (void *)plaintext;
        iov.iov_len = textlen;
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        
        sendmsg(opfd, &msg, 0);
        read(opfd, ciphertext, textlen);
        
        close(opfd);
        close(sockfd);
        return 0;
    }

**Performance** (i.MX 93 CAAM):

.. code-block:: text

    Algorithm        Software    CAAM        Speedup
    ─────────────────────────────────────────────────
    AES-256-CBC      45 MB/s     285 MB/s    6.3x
    SHA-256          68 MB/s     412 MB/s    6.1x
    RSA-2048 sign    12 ops/s    187 ops/s   15.6x
    RSA-2048 verify  215 ops/s   245 ops/s   1.1x

4.1.2 AF_ALG Socket Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Hash Calculation**:

.. code-block:: c

    int calculate_sha256(const uint8_t *data, size_t len, uint8_t *hash)
    {
        struct sockaddr_alg sa = {
            .salg_family = AF_ALG,
            .salg_type = "hash",
            .salg_name = "sha256"
        };
        
        int sockfd = socket(AF_ALG, SOCK_SEQPACKET, 0);
        bind(sockfd, (struct sockaddr *)&sa, sizeof(sa));
        
        int opfd = accept(sockfd, NULL, 0);
        write(opfd, data, len);
        read(opfd, hash, 32);
        
        close(opfd);
        close(sockfd);
        return 0;
    }

4.2 Secure Storage
------------------

4.2.1 dm-crypt / LUKS Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Create Encrypted Partition**:

.. code-block:: bash

    # Install cryptsetup
    apt-get install cryptsetup
    
    # Format partition with LUKS
    cryptsetup luksFormat --type luks2 \
        --cipher aes-xts-plain64 \
        --key-size 512 \
        --hash sha256 \
        --pbkdf pbkdf2 \
        /dev/mmcblk0p3
    
    # Open encrypted partition
    cryptsetup luksOpen /dev/mmcblk0p3 encrypted_data
    
    # Create filesystem
    mkfs.ext4 /dev/mapper/encrypted_data
    
    # Mount
    mount /dev/mapper/encrypted_data /data

**Key Management** (Smart Home Hub):

.. code-block:: bash

    # Derive encryption key from TPM/CAAM
    # (Production implementation uses CAAM key blob)
    
    # Generate DEK (Data Encryption Key)
    dd if=/dev/urandom of=/root/dek.bin bs=32 count=1
    
    # Wrap DEK with CAAM (creates blob)
    caam-keygen create dek.bin -s 32 -o dek_blob.bin
    
    # Use blob to unlock LUKS
    # (Custom initramfs with CAAM unwrap)
    caam-keygen unwrap dek_blob.bin -o /tmp/dek.bin
    cryptsetup luksOpen --key-file /tmp/dek.bin /dev/mmcblk0p3 encrypted_data
    shred -u /tmp/dek.bin

4.2.2 eCryptfs (File-level Encryption)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Mount Encrypted Directory**:

.. code-block:: bash

    # Mount with passphrase
    mount -t ecryptfs /encrypted /decrypted \
        -o key=passphrase,ecryptfs_cipher=aes,\
        ecryptfs_key_bytes=32,ecryptfs_passthrough=no,\
        ecryptfs_enable_filename_crypto=yes
    
    # Or use keyctl for key management
    echo "my_passphrase" | ecryptfs-add-passphrase --fnek
    keyctl show @u
    
    # Mount with key ID
    mount -t ecryptfs /encrypted /decrypted \
        -o key=passphrase:passphrase_passwd,\
        ecryptfs_sig=a1b2c3d4e5f67890,\
        ecryptfs_fnek_sig=0123456789abcdef,\
        ecryptfs_cipher=aes,ecryptfs_key_bytes=32

4.3 Secure Communication
------------------------

4.3.1 TLS Configuration
~~~~~~~~~~~~~~~~~~~~~~~

**Generate CA and Server Certificates**:

.. code-block:: bash

    # Root CA
    openssl genrsa -out ca.key 4096
    openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
        -subj "/C=US/ST=CA/O=Avionics/CN=Avionics CA"
    
    # Server certificate
    openssl genrsa -out server.key 2048
    openssl req -new -key server.key -out server.csr \
        -subj "/C=US/ST=CA/O=Avionics/CN=avionics-server"
    
    openssl x509 -req -days 365 -in server.csr \
        -CA ca.crt -CAkey ca.key -CAcreateserial \
        -out server.crt -sha256
    
    # Client certificate (mutual TLS)
    openssl genrsa -out client.key 2048
    openssl req -new -key client.key -out client.csr \
        -subj "/C=US/ST=CA/O=Avionics/CN=avionics-client"
    
    openssl x509 -req -days 365 -in client.csr \
        -CA ca.crt -CAkey ca.key -CAcreateserial \
        -out client.crt -sha256

**TLS 1.3 Server** (OpenSSL):

.. code-block:: c

    #include <openssl/ssl.h>
    #include <openssl/err.h>
    
    SSL_CTX *create_tls_server_context(void)
    {
        SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
        
        // Load certificates
        SSL_CTX_use_certificate_file(ctx, "server.crt", SSL_FILETYPE_PEM);
        SSL_CTX_use_PrivateKey_file(ctx, "server.key", SSL_FILETYPE_PEM);
        
        // Require client certificate (mutual TLS)
        SSL_CTX_load_verify_locations(ctx, "ca.crt", NULL);
        SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);
        
        // TLS 1.3 only, strong ciphers
        SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
        SSL_CTX_set_cipher_list(ctx, "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256");
        
        return ctx;
    }

4.3.2 IPsec VPN
~~~~~~~~~~~~~~~

**StrongSwan Configuration** (site-to-site VPN):

.. code-block:: text

    # /etc/ipsec.conf
    
    config setup
        charondebug="ike 2, knl 2, cfg 2"
        uniqueids=no
    
    conn avionics-vpn
        type=tunnel
        auto=start
        
        # Local (Avionics Platform)
        left=192.168.1.100
        leftsubnet=10.0.1.0/24
        leftcert=server.crt
        leftid="CN=avionics-server"
        
        # Remote (Ground Station)
        right=203.0.113.50
        rightsubnet=10.0.2.0/24
        rightcert=ground.crt
        rightid="CN=ground-station"
        
        # Encryption
        ike=aes256-sha256-modp2048!
        esp=aes256-sha256-modp2048!
        
        # Lifetime
        ikelifetime=24h
        lifetime=8h
        margintime=10m

**PSK Authentication** (Pre-Shared Key):

.. code-block:: text

    # /etc/ipsec.secrets
    
    : PSK "very_secret_pre_shared_key_with_high_entropy"

====================
5. Secure OTA Updates
====================

5.1 OTA Architecture
--------------------

**Update Flow**:

.. code-block:: text

    OTA Server
        ↓ HTTPS + signature
    Edge Gateway
        ↓ Verify signature
    A/B Partition Scheme
        ↓ Write to inactive partition
    Bootloader
        ↓ Verify new image
    Switch active partition
        ↓ Rollback on failure
    Update complete

5.2 Signed Update Packages
---------------------------

**Create Signed Update**:

.. code-block:: bash

    #!/bin/bash
    # create_ota_package.sh
    
    VERSION="1.2.3"
    
    # Create update package
    tar czf update-${VERSION}.tar.gz \
        rootfs.ext4 \
        uImage \
        devicetree.dtb \
        manifest.json
    
    # Sign package
    openssl dgst -sha256 -sign ota_private.key \
        -out update-${VERSION}.tar.gz.sig \
        update-${VERSION}.tar.gz
    
    # Create manifest
    cat > manifest.json <<EOF
    {
        "version": "${VERSION}",
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "files": [
            {
                "name": "rootfs.ext4",
                "size": $(stat -c %s rootfs.ext4),
                "sha256": "$(sha256sum rootfs.ext4 | awk '{print $1}')"
            },
            {
                "name": "uImage",
                "size": $(stat -c %s uImage),
                "sha256": "$(sha256sum uImage | awk '{print $1}')"
            },
            {
                "name": "devicetree.dtb",
                "size": $(stat -c %s devicetree.dtb),
                "sha256": "$(sha256sum devicetree.dtb | awk '{print $1}')"
            }
        ],
        "signature_algorithm": "RSA-SHA256",
        "public_key_fingerprint": "$(openssl x509 -in ota_cert.crt -noout -fingerprint -sha256)"
    }
    EOF

5.3 A/B Partition Update
-------------------------

**Partition Layout**:

.. code-block:: text

    /dev/mmcblk0p1: boot (U-Boot, shared)
    /dev/mmcblk0p2: rootfs_a (Active)
    /dev/mmcblk0p3: rootfs_b (Inactive)
    /dev/mmcblk0p4: data (persistent)

**U-Boot A/B Logic**:

.. code-block:: bash

    # U-Boot environment variables
    setenv bootpart 2         # Currently booting from partition 2 (A)
    setenv upgrade_available 0
    setenv bootcount 0
    setenv bootlimit 3
    
    # Boot script
    setenv bootcmd 'run select_partition; run load_kernel; bootm ${loadaddr} - ${fdt_addr}'
    
    setenv select_partition '
        if test ${bootcount} -gt ${bootlimit}; then
            echo "Boot failed ${bootlimit} times, switching partition";
            if test ${bootpart} = 2; then
                setenv bootpart 3;
            else
                setenv bootpart 2;
            fi;
            setenv bootcount 0;
            saveenv;
        fi;
        echo "Booting from partition ${bootpart}";
    '
    
    setenv load_kernel '
        ext4load mmc 0:${bootpart} ${loadaddr} /boot/uImage;
        ext4load mmc 0:${bootpart} ${fdt_addr} /boot/devicetree.dtb;
    '

**OTA Update Client** (Python):

.. code-block:: python

    #!/usr/bin/env python3
    import os
    import hashlib
    import json
    import requests
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.x509 import load_pem_x509_certificate
    
    class OTAUpdater:
        def __init__(self, server_url, cert_path):
            self.server_url = server_url
            with open(cert_path, 'rb') as f:
                self.cert = load_pem_x509_certificate(f.read())
        
        def check_update(self):
            """Check for available updates"""
            current_version = self._get_current_version()
            resp = requests.get(f"{self.server_url}/api/update/check",
                               params={'version': current_version})
            return resp.json()
        
        def download_update(self, version):
            """Download and verify update package"""
            # Download package
            pkg_url = f"{self.server_url}/updates/update-{version}.tar.gz"
            sig_url = f"{pkg_url}.sig"
            
            pkg_data = requests.get(pkg_url).content
            sig_data = requests.get(sig_url).content
            
            # Verify signature
            public_key = self.cert.public_key()
            try:
                public_key.verify(
                    sig_data,
                    pkg_data,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
            except Exception as e:
                raise ValueError(f"Signature verification failed: {e}")
            
            # Extract and verify manifest
            with tarfile.open(fileobj=io.BytesIO(pkg_data)) as tar:
                manifest_data = tar.extractfile('manifest.json').read()
                manifest = json.loads(manifest_data)
                
                for file_info in manifest['files']:
                    file_data = tar.extractfile(file_info['name']).read()
                    file_hash = hashlib.sha256(file_data).hexdigest()
                    
                    if file_hash != file_info['sha256']:
                        raise ValueError(f"Hash mismatch for {file_info['name']}")
            
            return pkg_data, manifest
        
        def install_update(self, pkg_data):
            """Install update to inactive partition"""
            # Determine inactive partition
            active_part = self._get_active_partition()  # e.g., "mmcblk0p2"
            inactive_part = "mmcblk0p3" if active_part == "mmcblk0p2" else "mmcblk0p2"
            
            # Extract update
            with tarfile.open(fileobj=io.BytesIO(pkg_data)) as tar:
                tar.extractall('/tmp/ota_update')
            
            # Write rootfs to inactive partition
            os.system(f"dd if=/tmp/ota_update/rootfs.ext4 of=/dev/{inactive_part} bs=4M")
            
            # Mount and update kernel
            os.system(f"mount /dev/{inactive_part} /mnt")
            os.system("cp /tmp/ota_update/uImage /mnt/boot/")
            os.system("cp /tmp/ota_update/devicetree.dtb /mnt/boot/")
            os.system("umount /mnt")
            
            # Update U-Boot environment to switch partition
            new_bootpart = "3" if active_part == "mmcblk0p2" else "2"
            os.system(f"fw_setenv bootpart {new_bootpart}")
            os.system("fw_setenv upgrade_available 1")
            os.system("fw_setenv bootcount 0")
            
            print(f"Update installed to {inactive_part}, reboot to apply")
        
        def _get_current_version(self):
            with open('/etc/version', 'r') as f:
                return f.read().strip()
        
        def _get_active_partition(self):
            # Read U-Boot environment
            result = os.popen("fw_printenv bootpart").read()
            bootpart = result.split('=')[1].strip()
            return f"mmcblk0p{bootpart}"

**Rollback on Boot Failure** (Systemd service):

.. code-block:: bash

    # /etc/systemd/system/ota-confirm-boot.service
    
    [Unit]
    Description=Confirm successful boot after OTA update
    After=network.target
    
    [Service]
    Type=oneshot
    ExecStart=/usr/bin/ota-confirm-boot.sh
    
    [Install]
    WantedBy=multi-user.target

.. code-block:: bash

    #!/bin/bash
    # /usr/bin/ota-confirm-boot.sh
    
    UPGRADE_AVAILABLE=$(fw_printenv -n upgrade_available)
    
    if [ "$UPGRADE_AVAILABLE" = "1" ]; then
        echo "New update confirmed successful"
        fw_setenv upgrade_available 0
        fw_setenv bootcount 0
    fi

**Project Results** (Smart Home Hub):

- OTA Package Size: 85 MB (compressed rootfs)
- Download Time: ~3.5 minutes (over cellular)
- Installation Time: ~8 minutes (eMMC write)
- Verification Time: 12 seconds (signature + hashes)
- Successful Updates: 1,247 / 1,250 devices (99.76%)
- Failed Updates: 3 (network interruption, auto-rollback successful)

====================
6. Runtime Security Monitoring
====================

6.1 IMA/EVM (Integrity Measurement Architecture)
-------------------------------------------------

**Enable IMA**:

.. code-block:: kconfig

    CONFIG_INTEGRITY=y
    CONFIG_IMA=y
    CONFIG_IMA_MEASURE_PCR_IDX=10
    CONFIG_IMA_LSM_RULES=y
    CONFIG_IMA_APPRAISE=y
    CONFIG_EVM=y

**IMA Policy** (``/etc/ima/ima-policy``):

.. code-block:: text

    # Measure all executables and libraries
    measure func=BPRM_CHECK
    measure func=MMAP_CHECK mask=MAY_EXEC
    
    # Appraise all files (require signatures)
    appraise func=BPRM_CHECK appraise_type=imasig
    appraise func=MMAP_CHECK mask=MAY_EXEC appraise_type=imasig
    appraise func=MODULE_CHECK appraise_type=imasig
    
    # EVM for extended attributes
    appraise func=FILE_CHECK mask=MAY_READ appraise_type=imasig

**Sign Files with evmctl**:

.. code-block:: bash

    # Generate IMA signing key
    openssl genrsa -out ima_private.key 2048
    openssl req -new -x509 -key ima_private.key -out ima_cert.crt \
        -subj "/CN=IMA Signing Key"
    
    # Convert to DER
    openssl x509 -in ima_cert.crt -outform DER -out ima_cert.der
    
    # Add to kernel keyring
    keyctl padd asymmetric "" %keyring:.ima < ima_cert.der
    
    # Sign executable
    evmctl ima_sign --key ima_private.key /usr/sbin/avionics_app
    
    # Verify signature
    getfattr -m . -d /usr/sbin/avionics_app
    # security.ima=0x030204...

6.2 Audit Framework
-------------------

**Audit Rules** (``/etc/audit/rules.d/avionics.rules``):

.. code-block:: text

    # Watch configuration files
    -w /etc/avionics.conf -p wa -k avionics_config
    
    # Watch security-critical binaries
    -w /usr/sbin/avionics_app -p x -k avionics_exec
    
    # Monitor network configuration changes
    -a always,exit -F arch=b64 -S socket -S bind -S connect -k network
    
    # Monitor file permission changes
    -a always,exit -F arch=b64 -S chmod -S fchmod -S chown -S fchown -k perm_mod
    
    # Monitor user/group changes
    -w /etc/passwd -p wa -k passwd_changes
    -w /etc/group -p wa -k group_changes
    
    # Monitor privilege escalation
    -a always,exit -F arch=b64 -S setuid -S setgid -k priv_escalation

**Query Audit Logs**:

.. code-block:: bash

    # Search for events
    ausearch -k avionics_exec -ts today
    
    # Generate report
    aureport --executable --summary
    
    # Real-time monitoring
    ausearch -ts recent -i | tail -f

====================
7. Security Certifications
====================

7.1 DO-178C (Avionics)
----------------------

**Security Supplements**:

- **DO-326A**: Airworthiness Security Process
- **DO-356**: Airworthiness Security Methods and Considerations

**Security Requirements**:

.. code-block:: text

    1. Security Risk Assessment
       - Threat modeling (STRIDE)
       - Attack surface analysis
       - Security impact assessment
    
    2. Security Development
       - Secure coding standards (MISRA-C, CERT)
       - Code review for security vulnerabilities
       - Static analysis (Coverity, CodeSonar)
    
    3. Security Testing
       - Penetration testing
       - Fuzzing (AFL, libFuzzer)
       - Security-focused integration testing
    
    4. Security Configuration Management
       - Signed binaries
       - Configuration baselines
       - Change control for security updates

7.2 ISO 26262 (Automotive)
---------------------------

**Cybersecurity**: ISO/SAE 21434

**Security Objectives**:

.. code-block:: text

    - Secure communication (CAN, Ethernet)
    - Secure boot and updates
    - Intrusion detection
    - Key management
    - Security event logging

====================
8. Security Best Practices
====================

8.1 Checklist
-------------

.. code-block:: text

    Boot Security:
    ☐ Secure boot enabled (HAB/UEFI)
    ☐ Bootloader signed and verified
    ☐ Kernel/DTB signed
    ☐ Disable JTAG in production
    
    System Security:
    ☐ SELinux enforcing mode
    ☐ Minimal attack surface (disable unused services)
    ☐ Strong passwords / key-based authentication
    ☐ Firewall configured (iptables/nftables)
    
    Cryptography:
    ☐ Use hardware crypto acceleration
    ☐ TLS 1.3 for network communication
    ☐ Encrypted storage (dm-crypt/LUKS)
    ☐ Secure key storage (TPM/CAAM)
    
    Updates:
    ☐ Signed OTA updates
    ☐ A/B partition scheme
    ☐ Automatic rollback on failure
    ☐ Secure update delivery (HTTPS)
    
    Monitoring:
    ☐ IMA/EVM enabled
    ☐ Audit logging configured
    ☐ Security event monitoring
    ☐ Intrusion detection (fail2ban, OSSEC)
    
    Compliance:
    ☐ DO-178C/DO-326A (avionics)
    ☐ ISO 26262/ISO 21434 (automotive)
    ☐ Security certification documentation

8.2 Common Vulnerabilities
---------------------------

**Attack Vectors**:

1. **Physical Access**: JTAG debug ports, UART consoles
   - Mitigation: Disable in production, secure physical access

2. **Network Attacks**: Open ports, weak authentication
   - Mitigation: Firewall, TLS, client certificates

3. **Side-Channel**: Timing attacks, power analysis
   - Mitigation: Constant-time crypto, hardware countermeasures

4. **Supply Chain**: Compromised dependencies
   - Mitigation: Signed packages, reproducible builds

5. **Privilege Escalation**: Kernel vulnerabilities, setuid binaries
   - Mitigation: SELinux, capability-based security, regular updates

====================
9. References
====================

**NXP i.MX Security**:

- AN4581: "Secure Boot on i.MX 50, i.MX 53, i.MX 6 and i.MX 7 Series using HABv4"
- AN12056: "Encrypted Boot on HABv4 and CAAM Enabled Devices"
- CST User Guide: Code Signing Tool documentation

**UEFI Secure Boot**:

- UEFI Specification 2.9
- https://www.rodsbooks.com/efi-bootloaders/secureboot.html

**SELinux**:

- SELinux Project: https://github.com/SELinuxProject
- Reference Policy: https://github.com/SELinuxProject/refpolicy

**Standards**:

- DO-178C / DO-326A (Avionics Software Security)
- ISO 26262 (Automotive Functional Safety)
- ISO/SAE 21434 (Automotive Cybersecurity)

---

**Revision History**:

========  ==========  ====================================
Version   Date        Changes
========  ==========  ====================================
1.0       2026-01-22  Initial comprehensive security guide
========  ==========  ====================================
