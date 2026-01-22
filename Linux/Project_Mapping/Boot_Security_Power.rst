===============================================
Boot, Security & Power Management Portfolio
===============================================

:Author: Madhavan Vivekanandan
:Date: January 22, 2026
:Purpose: Document boot optimization, secure boot, and power management across projects
:Scope: U-Boot, UEFI, HAB, SELinux, Power states, Hibernation

.. contents:: Quick Navigation
   :depth: 3
   :local:

Overview
=========

**Core Competencies**:

==========================  ==========  =======================================
Domain                      Projects    Key Achievements
==========================  ==========  =======================================
**Boot Optimization**       #1, #7      15s → 3s (5x), 15s → 6s (2.5x)
**Secure Boot**             #1, #2, #7  UEFI, HAB, Custom verified boot
**Security (SELinux)**      #2          Enforcing mode for avionics
**Power Management**        #1, #7      < 8mW hibernation, 3x battery life
**OTA Updates**             #1, #4      SWUpdate, encrypted updates
==========================  ==========  =======================================

Section 1: Boot Systems & Optimization
========================================

1.1 Boot Time Optimization Results
------------------------------------

Boot Time Achievements Across Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------+---------------------+---------------------+------------------+
| Project  | Original Boot Time  | Optimized Boot Time | Improvement      |
+==========+=====================+=====================+==================+
| #1 IoT   | ~15 seconds         | **< 3 seconds**     | **5x faster**    |
+----------+---------------------+---------------------+------------------+
| #7       | ~15 seconds         | **< 6 seconds**     | **2.5x faster**  |
| Thermal  | (cold boot)         | (cold boot)         |                  |
+----------+---------------------+---------------------+------------------+
| #7       | ~5 seconds          | **< 2 seconds**     | **2.5x faster**  |
| Thermal  | (hibernate wake)    | (wake from sleep)   |                  |
+----------+---------------------+---------------------+------------------+

1.2 U-Boot Customization
--------------------------

U-Boot Experience by Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Projects**: #1 (IoT i.MX93), #2 (Avionics Atom), #7 (Thermal DaVinci)

U-Boot Customizations
~~~~~~~~~~~~~~~~~~~~~~

**1. Manufacturing Test Commands** (Thermal Imaging)::

    /* DFM (Design For Manufacturing) test commands */
    int do_mfg_test(cmd_tbl_t *cmdtp, int flag, int argc, char * const argv[])
    {
        int ret = 0;
        
        printf("=== Manufacturing Test Suite ===\n\n");
        
        /* 1. NAND Flash Test */
        printf("Testing NAND Flash...\n");
        if (nand_test_all_blocks() != 0) {
            printf("NAND Test FAILED\n");
            ret = 1;
        } else {
            printf("NAND Test PASSED\n");
        }
        
        /* 2. DDR Memory Test */
        printf("\nTesting DDR Memory...\n");
        if (ddr_mem_test(0x80000000, 0x8000000) != 0) {  /* Test 128MB */
            printf("DDR Test FAILED\n");
            ret = 1;
        } else {
            printf("DDR Test PASSED\n");
        }
        
        /* 3. I2C Bus Test */
        printf("\nTesting I2C Bus...\n");
        if (i2c_probe_devices() != 0) {
            printf("I2C Test FAILED\n");
            ret = 1;
        } else {
            printf("I2C Test PASSED\n");
        }
        
        /* 4. SPI Bus Test */
        printf("\nTesting SPI Bus...\n");
        if (spi_probe_devices() != 0) {
            printf("SPI Test FAILED\n");
            ret = 1;
        } else {
            printf("SPI Test PASSED\n");
        }
        
        /* 5. USB Host Test */
        printf("\nTesting USB Host...\n");
        if (usb_test() != 0) {
            printf("USB Test FAILED\n");
            ret = 1;
        } else {
            printf("USB Test PASSED\n");
        }
        
        /* 6. Ethernet Test */
        printf("\nTesting Ethernet...\n");
        if (eth_loopback_test() != 0) {
            printf("Ethernet Test FAILED\n");
            ret = 1;
        } else {
            printf("Ethernet Test PASSED\n");
        }
        
        if (ret == 0) {
            printf("\n*** ALL TESTS PASSED ***\n");
            setenv("mfg_status", "PASS");
        } else {
            printf("\n*** SOME TESTS FAILED ***\n");
            setenv("mfg_status", "FAIL");
        }
        
        return ret;
    }
    
    U_BOOT_CMD(
        mfgtest, 1, 0, do_mfg_test,
        "run manufacturing test suite",
        "\n"
        "    - Tests NAND, DDR, I2C, SPI, USB, Ethernet\n"
        "    - Sets mfg_status environment variable"
    );

**2. NAND BBT Support** (Thermal Imaging)::

    /* U-Boot NAND configuration matching kernel BBT */
    #define CONFIG_SYS_NAND_USE_BBT
    #define CONFIG_SYS_NAND_BAD_BLOCK_POS    0
    
    /* Custom BBT descriptor (must match kernel) */
    static struct nand_bbt_descr uboot_bbt_main = {
        .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | 
                   NAND_BBT_WRITE | NAND_BBT_2BIT | 
                   NAND_BBT_VERSION,
        .offs = 8,
        .len = 4,
        .veroffs = 12,
        .maxblocks = 4,
        .pattern = bbt_pattern
    };
    
    /* NAND initialization with BBT */
    int board_nand_init(struct nand_chip *nand)
    {
        /* Configure NAND controller */
        davinci_nand_init(nand);
        
        /* Setup BBT descriptors */
        nand->bbt_td = &uboot_bbt_main;
        nand->bbt_md = &uboot_bbt_mirror;
        
        /* Hardware BCH ECC */
        nand->ecc.mode = NAND_ECC_HW;
        nand->ecc.size = 512;
        nand->ecc.bytes = 10;  /* BCH-8 */
        nand->ecc.strength = 8;
        
        return 0;
    }

**3. Boot Time Optimization** (IoT i.MX93)::

    /* Minimal U-Boot configuration for fast boot */
    #define CONFIG_BOOTDELAY        0  /* No delay */
    #define CONFIG_SILENT_CONSOLE   /* Suppress boot messages */
    
    /* Remove unused commands */
    #undef CONFIG_CMD_EDITENV
    #undef CONFIG_CMD_SAVEENV
    #undef CONFIG_CMD_BDI
    #undef CONFIG_CMD_CONSOLE
    #undef CONFIG_CMD_ECHO
    #undef CONFIG_CMD_FPGA
    #undef CONFIG_CMD_ITEST
    #undef CONFIG_CMD_LOADB
    #undef CONFIG_CMD_LOADS
    #undef CONFIG_CMD_MISC
    #undef CONFIG_CMD_NFS
    #undef CONFIG_CMD_SETGETDCR
    #undef CONFIG_CMD_SOURCE
    #undef CONFIG_CMD_XIMG
    
    /* Fast environment loading (raw MMC) */
    #define CONFIG_ENV_IS_IN_MMC
    #define CONFIG_ENV_OFFSET       0x400000
    #define CONFIG_ENV_SIZE         0x2000
    
    /* Optimized boot command */
    #define CONFIG_BOOTCOMMAND \
        "mmc dev 0; " \
        "mmc read 0x40480000 0x800 0x4000; " \  /* Read kernel (8MB) */
        "mmc read 0x43000000 0x4800 0x100; " \   /* Read DTB (512KB) */
        "bootz 0x40480000 - 0x43000000"          /* Boot directly */
    
    /* Skip memory test for faster boot */
    #define CONFIG_SKIP_LOWLEVEL_INIT

**4. Secure Boot U-Boot** (i.MX93 HAB)::

    /* HAB (High Assurance Boot) configuration */
    #define CONFIG_SECURE_BOOT
    #define CONFIG_FSL_CAAM            /* Cryptographic Accelerator */
    #define CONFIG_CMD_DEKBLOB         /* Data Encryption Key blob */
    #define CONFIG_IMX_HAB             /* HAB support */
    
    /* Verify signed images before loading */
    int board_late_init(void)
    {
        /* Check HAB status */
        if (!imx_hab_is_enabled()) {
            printf("WARNING: HAB not enabled\n");
        }
        
        /* Authenticate images */
        uint32_t load_addr = CONFIG_LOADADDR;
        uint32_t ivt_offset = 0;
        size_t bytes = 0;
        
        if (authenticate_image(load_addr, ivt_offset, &bytes) != 0) {
            printf("Image authentication FAILED\n");
            hang();  /* Stop boot if authentication fails */
        }
        
        return 0;
    }

Boot Process Timeline (i.MX93 Optimized)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Time (ms)    Stage                   Details
    ─────────────────────────────────────────────────────────────────
    0            Power-On Reset          Hardware initialization
    100          Boot ROM                Load U-Boot SPL from eMMC
    300          U-Boot SPL              DDR init, load main U-Boot
    600          U-Boot Main             HAB verification, load kernel
    1200         Kernel Decompression    Decompress and relocate kernel
    1500         Kernel Init             Early init, device probing
    2000         Init (systemd)          Parallel service startup
    2800         User Space Ready        System fully booted
    
    Total: < 3 seconds

**Optimization Techniques**:

================================  ==========================================
Technique                         Impact
================================  ==========================================
Remove unused U-Boot commands     -200ms (faster compilation, smaller)
Optimize environment loading      -150ms (raw MMC vs filesystem)
Silent console (no messages)      -100ms (no UART delays)
Parallel kernel init              -500ms (async device probing)
Systemd parallel startup          -1000ms (services start concurrently)
Minimal rootfs (SquashFS)         -300ms (less I/O)
Built-in kernel drivers           -200ms (no module loading)
================================  ==========================================

**Interview Talking Point**:
*"I optimized boot time on 3 platforms: i.MX93 IoT from 15s → 3s (removed unused U-Boot commands, silent console, parallel systemd init, SquashFS rootfs); ARM9 thermal from 15s → 6s (U-Boot optimization, kernel config, initscript tuning); hibernate wake 5s → 2s (minimal image, optimized resume path). Techniques: U-Boot stripping, kernel built-ins vs modules, parallel init, filesystem optimization."*

Section 2: Secure Boot Implementations
========================================

2.1 Three Secure Boot Architectures
-------------------------------------

Secure Boot Comparison
~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+-------------------+---------------------+------------------+
| Secure Boot Type | Project           | Platform            | Security Level   |
+==================+===================+=====================+==================+
| **UEFI Secure**  | #2 (Avionics)     | Intel Atom C3xxx    | Very High        |
+------------------+-------------------+---------------------+------------------+
| **HAB (NXP)**    | #1 (IoT)          | i.MX93 (ARM)        | Very High        |
+------------------+-------------------+---------------------+------------------+
| **Custom**       | #7 (Thermal)      | ARM9 DaVinci        | High             |
+------------------+-------------------+---------------------+------------------+

2.2 UEFI Secure Boot (Avionics)
---------------------------------

**Project**: #2 (Intel Atom C3xxx Avionics Platform)

UEFI Secure Boot Chain
~~~~~~~~~~~~~~~~~~~~~~~~

::

    [Power-On]
         ↓
    [UEFI Firmware (Platform Key PK)]
         ↓ Verifies
    [Bootloader/Shim (Key Exchange Key KEK)]
         ↓ Verifies
    [Kernel (Database Key db)]
         ↓ Verifies
    [Kernel Modules (db or custom key)]
         ↓
    [User Space (signed binaries)]

**Key Hierarchy**:

====================  ====================================================
Key Type              Purpose
====================  ====================================================
**PK** (Platform Key) Root of trust, signs KEK
**KEK** (Key Exch)    Signs db and dbx (revocation)
**db** (Database)     Signs bootloaders, kernels, drivers
**dbx** (Blacklist)   Revoked signatures
====================  ====================================================

Generating UEFI Keys
~~~~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    # Generate UEFI Secure Boot keys
    
    # 1. Platform Key (PK) - Root of trust
    openssl req -new -x509 -newkey rsa:2048 -subj "/CN=Avionics PK/" \
        -keyout PK.key -out PK.crt -days 3650 -nodes -sha256
    cert-to-efi-sig-list -g "$(uuidgen)" PK.crt PK.esl
    sign-efi-sig-list -k PK.key -c PK.crt PK PK.esl PK.auth
    
    # 2. Key Exchange Key (KEK)
    openssl req -new -x509 -newkey rsa:2048 -subj "/CN=Avionics KEK/" \
        -keyout KEK.key -out KEK.crt -days 3650 -nodes -sha256
    cert-to-efi-sig-list -g "$(uuidgen)" KEK.crt KEK.esl
    sign-efi-sig-list -k PK.key -c PK.crt KEK KEK.esl KEK.auth
    
    # 3. Database Key (db) - Signs bootloader, kernel, modules
    openssl req -new -x509 -newkey rsa:2048 -subj "/CN=Avionics db/" \
        -keyout db.key -out db.crt -days 3650 -nodes -sha256
    cert-to-efi-sig-list -g "$(uuidgen)" db.crt db.esl
    sign-efi-sig-list -k KEK.key -c KEK.crt db db.esl db.auth
    
    # Store securely (Hardware Security Module in production)
    chmod 600 *.key

Signing Binaries
~~~~~~~~~~~~~~~~~

**Sign Kernel**::

    # Sign bzImage with db key
    sbsign --key db.key --cert db.crt --output bzImage.signed bzImage
    
    # Verify signature
    sbverify --cert db.crt bzImage.signed

**Sign All Kernel Modules**::

    #!/bin/bash
    # Sign all .ko modules
    
    MODULES_DIR="/lib/modules/5.10.100/kernel"
    
    find $MODULES_DIR -name '*.ko' | while read module; do
        echo "Signing $module..."
        
        # Extract module name
        modname=$(basename $module)
        
        # Sign with kernel module signing tool
        scripts/sign-file sha256 db.key db.crt $module
        
        # Verify
        if modinfo $module | grep -q "sig_id"; then
            echo "  $modname: Signed OK"
        else
            echo "  $modname: Signing FAILED"
            exit 1
        fi
    done
    
    echo "All modules signed successfully"

**Kernel Configuration for Module Signing**::

    CONFIG_MODULE_SIG=y
    CONFIG_MODULE_SIG_FORCE=y          # Refuse unsigned modules
    CONFIG_MODULE_SIG_ALL=y            # Sign all modules automatically
    CONFIG_MODULE_SIG_SHA256=y         # Use SHA256
    CONFIG_MODULE_SIG_HASH="sha256"
    CONFIG_MODULE_SIG_KEY="certs/db.key"  # Key for signing

UEFI Firmware Setup
~~~~~~~~~~~~~~~~~~~~

::

    # Install keys to UEFI firmware (via efitools or mokutil)
    
    # 1. Boot to UEFI Shell
    # 2. Enroll PK (takes ownership)
    KeyTool.efi
    # Select "Edit Keys"
    # Platform Key (PK) → Replace → PK.auth
    
    # 3. Enroll KEK
    # Key Exchange Keys → Add → KEK.auth
    
    # 4. Enroll db
    # Authorized Signatures → Add → db.auth
    
    # 5. Enable Secure Boot
    # Secure Boot Configuration → Attempt Secure Boot: [Enabled]
    
    # 6. Verify
    # Boot Linux and check
    mokutil --sb-state
    # Output: SecureBoot enabled

**Interview Talking Point**:
*"Implemented UEFI Secure Boot for Intel Atom avionics platform: generated PKI hierarchy (PK → KEK → db), signed all binaries (bootloader, kernel, 200+ modules) using sbsign/sign-file, configured kernel with MODULE_SIG_FORCE to reject unsigned modules, and enrolled keys in UEFI firmware. Result: complete boot chain verification from UEFI firmware through kernel and all modules."*

2.3 HAB Secure Boot (i.MX93 IoT)
----------------------------------

**Project**: #1 (Smart Home IoT Platform)

NXP HAB (High Assurance Boot) Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    [Boot ROM (Immutable)]
         ↓ Verifies with SRK (Super Root Key)
    [U-Boot SPL] (Signed)
         ↓ Verifies
    [U-Boot] (Signed)
         ↓ Verifies
    [Kernel + DTB] (Signed)
         ↓
    [Rootfs with dm-verity] (Integrity protected)

**HAB Features**:

==========================  ==================================================
Feature                     Description
==========================  ==================================================
SRK (Super Root Key)        Root of trust (4 keys, 2048-bit RSA)
CSF (Command Sequence File) Signature data for images
IVT (Image Vector Table)    Points to CSF for verification
eFuses                      Store SRK hash, enable closed mode
HAB Events                  Log of authentication events
==========================  ==================================================

Generating HAB Keys
~~~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    # Generate HAB key pair (using NXP CST tool)
    
    cd cst-3.3.1/keys/
    
    # Generate 4 SRK key pairs (production uses HSM)
    ./hab4_pki_tree.sh
    
    # Output:
    # SRK1_sha256_2048_65537_v3_ca_key.pem  (private)
    # SRK1_sha256_2048_65537_v3_ca_crt.pem  (public certificate)
    # SRK2_sha256_2048_65537_v3_ca_key.pem
    # SRK2_sha256_2048_65537_v3_ca_crt.pem
    # SRK3_sha256_2048_65537_v3_ca_key.pem
    # SRK3_sha256_2048_65537_v3_ca_crt.pem
    # SRK4_sha256_2048_65537_v3_ca_key.pem
    # SRK4_sha256_2048_65537_v3_ca_crt.pem
    
    # Generate SRK table and hash
    ../linux64/bin/srktool -h 4 -t SRK_1_2_3_4_table.bin -e SRK_1_2_3_4_fuse.bin \
        -d sha256 -c \
        SRK1_sha256_2048_65537_v3_ca_crt.pem,\
        SRK2_sha256_2048_65537_v3_ca_crt.pem,\
        SRK3_sha256_2048_65537_v3_ca_crt.pem,\
        SRK4_sha256_2048_65537_v3_ca_crt.pem
    
    # SRK_1_2_3_4_fuse.bin contains hash to burn to eFuses

Signing U-Boot with HAB
~~~~~~~~~~~~~~~~~~~~~~~~~

**CSF (Command Sequence File) for U-Boot**::

    [Header]
    Version = 4.3
    Hash Algorithm = sha256
    Engine = CAAM
    Engine Configuration = 0
    Certificate Format = X509
    Signature Format = CMS
    
    [Install SRK]
    File = "../crts/SRK_1_2_3_4_table.bin"
    Source index = 0  # Use SRK1
    
    [Install CSFK]
    File = "../crts/CSF1_1_sha256_2048_65537_v3_usr_crt.pem"
    
    [Authenticate CSF]
    
    [Install Key]
    Verification index = 0
    Target index = 2
    File = "../crts/IMG1_1_sha256_2048_65537_v3_usr_crt.pem"
    
    [Authenticate Data]
    Verification index = 2
    Blocks = 0x40480000 0x0 0x80000 "u-boot.imx"  # Start, offset, size, file

**Signing Process**::

    # Generate CSF binary
    cst -i csf_uboot.txt -o csf_uboot.bin
    
    # Append CSF to U-Boot image
    cat u-boot.imx csf_uboot.bin > u-boot-signed.imx
    
    # Flash to eMMC
    dd if=u-boot-signed.imx of=/dev/mmcblk0 bs=1k seek=33

**Signing Kernel + DTB**::

    # Kernel IVT
    [Authenticate Data]
    Blocks = 0x40480000 0x0 0x800000 "zImage"  # Kernel
    Blocks = 0x43000000 0x0 0x20000 "imx93-smarthome.dtb"  # DTB

Enabling HAB Closed Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # In U-Boot, burn SRK hash to eFuses (IRREVERSIBLE!)
    
    # 1. Read SRK hash
    hexdump -e '/4 "0x"' -e '/4 "%X""\n"' SRK_1_2_3_4_fuse.bin
    # Output: 0xABCD1234 0x5678EFAB ...
    
    # 2. Burn to eFuses (DANGER: One-time operation!)
    => fuse prog 6 0 0xABCD1234  # SRK_HASH[255:224]
    => fuse prog 6 1 0x5678EFAB  # SRK_HASH[223:192]
    => fuse prog 6 2 0x...       # SRK_HASH[191:160]
    => fuse prog 6 3 0x...       # SRK_HASH[159:128]
    => fuse prog 7 0 0x...       # SRK_HASH[127:96]
    => fuse prog 7 1 0x...       # SRK_HASH[95:64]
    => fuse prog 7 2 0x...       # SRK_HASH[63:32]
    => fuse prog 7 3 0x...       # SRK_HASH[31:0]
    
    # 3. Enable HAB closed mode (device will only boot signed images)
    => fuse prog 0 6 0x00000010  # SEC_CONFIG[HAB_CLOSED]=1
    
    # 4. Reboot - HAB will verify all images

**Verifying HAB Status**::

    # In U-Boot
    => hab_status
    
    # Expected output (closed mode, no events):
    Secure boot enabled
    
    HAB Configuration: 0xcc, HAB State: 0x99
    No HAB Events Found!

**Interview Talking Point**:
*"Implemented NXP HAB secure boot for i.MX93 IoT: generated 4 SRK key pairs using CST tool, created CSF (Command Sequence Files) to sign U-Boot/kernel/DTB, burned SRK hash to eFuses, and enabled HAB closed mode. Device now only boots signed images verified by boot ROM using hardware root of trust. All images authenticated before execution, with HAB events logged for audit."*

2.4 Custom Verified Boot (Thermal)
------------------------------------

**Project**: #7 (ARM9 DaVinci Thermal Imaging)

**Simpler than UEFI/HAB but effective for product security**

Custom Boot Verification
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    [U-Boot]
         ↓
    Verify Kernel SHA256
         ↓ (Hash stored in U-Boot env)
    Verify Rootfs SHA256
         ↓ (Hash stored in NAND spare area)
    Boot if verified

**U-Boot Verification Code**::

    int verify_and_boot(void)
    {
        unsigned char kernel_sha256[32];
        unsigned char rootfs_sha256[32];
        unsigned char computed_hash[32];
        
        /* Read expected hashes from environment */
        char *kernel_hash_str = getenv("kernel_hash");
        char *rootfs_hash_str = getenv("rootfs_hash");
        
        /* Convert hex strings to binary */
        hex_to_bin(kernel_hash_str, kernel_sha256, 32);
        hex_to_bin(rootfs_hash_str, rootfs_sha256, 32);
        
        /* Load kernel to RAM */
        nand_read_skip_bad(0x80700000, 0x400000, 0x400000);  /* 4MB kernel */
        
        /* Compute SHA256 of kernel */
        sha256_csum_wd((unsigned char *)0x80700000, 0x400000, 
                       computed_hash, CHUNKSZ_SHA256);
        
        /* Verify kernel */
        if (memcmp(kernel_sha256, computed_hash, 32) != 0) {
            printf("Kernel verification FAILED!\n");
            return -1;
        }
        printf("Kernel verification PASSED\n");
        
        /* Similar verification for rootfs */
        
        /* Boot verified kernel */
        do_bootm(NULL, 0, 3, bootm_argv);
        
        return 0;
    }

Section 3: Security Implementations
=====================================

3.1 SELinux Integration (Avionics)
------------------------------------

**Project**: #2 (Intel Atom C3xxx Avionics)

**Why SELinux for Avionics**:

- **Mandatory Access Control (MAC)**: Beyond traditional Unix permissions
- **Least Privilege**: Services run with minimal permissions
- **Audit Trail**: All access attempts logged
- **DO-178C Compliance**: Security policy documentation

SELinux Configuration
~~~~~~~~~~~~~~~~~~~~~~

**Buildroot Configuration**::

    BR2_PACKAGE_SELINUX=y
    BR2_PACKAGE_LIBSELINUX=y
    BR2_PACKAGE_LIBSEMANAGE=y
    BR2_PACKAGE_LIBSEPOL=y
    BR2_PACKAGE_POLICYCOREUTILS=y
    BR2_PACKAGE_SELINUX_PYTHON=y

**Kernel Configuration**::

    CONFIG_SECURITY_SELINUX=y
    CONFIG_SECURITY_SELINUX_BOOTPARAM=y
    CONFIG_SECURITY_SELINUX_DISABLE=n  # Cannot disable at runtime
    CONFIG_SECURITY_SELINUX_DEVELOP=n  # Production mode
    CONFIG_SECURITY_SELINUX_AVC_STATS=y
    CONFIG_SECURITY_SELINUX_CHECKREQPROT_VALUE=0
    CONFIG_DEFAULT_SECURITY_SELINUX=y

**Boot Parameters**::

    # In /boot/grub/grub.cfg
    linux /bzImage.signed root=/dev/sda2 ro selinux=1 security=selinux

Custom SELinux Policy
~~~~~~~~~~~~~~~~~~~~~~

**avionics.te** (Type Enforcement)::

    policy_module(avionics, 1.0.0)
    
    # Avionics control service domain
    type avionics_t;
    type avionics_exec_t;
    init_daemon_domain(avionics_t, avionics_exec_t)
    
    # CAN device access
    type avionics_can_device_t;
    dev_node(avionics_can_device_t)
    allow avionics_t avionics_can_device_t:chr_file rw_chr_file_perms;
    
    # FPGA device access
    type avionics_fpga_device_t;
    dev_node(avionics_fpga_device_t)
    allow avionics_t avionics_fpga_device_t:chr_file rw_chr_file_perms;
    
    # Network (AFDX) access
    allow avionics_t self:tcp_socket create_stream_socket_perms;
    allow avionics_t self:udp_socket create_socket_perms;
    corenet_tcp_bind_generic_node(avionics_t)
    corenet_udp_bind_generic_node(avionics_t)
    
    # Logging
    logging_send_syslog_msg(avionics_t)
    
    # File access (config, logs)
    type avionics_config_t;
    files_type(avionics_config_t)
    allow avionics_t avionics_config_t:file read_file_perms;
    
    type avionics_log_t;
    logging_log_file(avionics_log_t)
    allow avionics_t avionics_log_t:file append_file_perms;

**avionics.fc** (File Contexts)::

    # Executable
    /usr/bin/avionics-control    -- gen_context(system_u:object_r:avionics_exec_t,s0)
    
    # Devices
    /dev/can[0-9]+               -c gen_context(system_u:object_r:avionics_can_device_t,s0)
    /dev/fpga0                   -c gen_context(system_u:object_r:avionics_fpga_device_t,s0)
    
    # Configuration
    /etc/avionics(/.*)?             gen_context(system_u:object_r:avionics_config_t,s0)
    
    # Logs
    /var/log/avionics(/.*)?         gen_context(system_u:object_r:avionics_log_t,s0)

**Compiling and Loading Policy**::

    # Compile policy module
    checkmodule -M -m -o avionics.mod avionics.te
    semodule_package -o avionics.pp -m avionics.mod -fc avionics.fc
    
    # Load policy
    semodule -i avionics.pp
    
    # Verify
    semodule -l | grep avionics

**Relabeling Filesystem**::

    # After policy changes, relabel
    setfiles -r /mnt/rootfs \
        /etc/selinux/avionics/contexts/files/file_contexts \
        /mnt/rootfs

SELinux Audit
~~~~~~~~~~~~~~

**Monitoring Denials**::

    # View SELinux denials
    ausearch -m avc -ts recent
    
    # Example denial:
    type=AVC msg=audit(1674389234.123:456): avc: denied { read } for \
        pid=1234 comm="avionics-control" name="config.dat" dev="sda2" \
        ino=12345 scontext=system_u:system_r:avionics_t:s0 \
        tcontext=system_u:object_r:unlabeled_t:s0 tclass=file permissive=0
    
    # Fix: Add policy or relabel file
    chcon -t avionics_config_t /etc/avionics/config.dat

**Interview Talking Point**:
*"Implemented SELinux enforcing mode for avionics platform: created custom policy module (avionics.te) defining domains for avionics-control service, allowed minimal permissions (CAN/FPGA devices, AFDX network, config files), compiled with checkmodule/semodule_package, and loaded into kernel. Configured file contexts, relabeled filesystem with setfiles, and monitored denials with ausearch. Result: MAC preventing privilege escalation even if service compromised."*

3.2 OTA (Over-The-Air) Updates
--------------------------------

**Projects**: #1 (IoT), #4 (AFIRS SDU)

SWUpdate Integration (IoT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**sw-description** (Update manifest)::

    software =
    {
        version = "1.2.3";
        
        smarthome-board = {
            hardware-compatibility: [ "1.0" ];
            
            images: (
                {
                    filename = "rootfs.squashfs";
                    type = "raw";
                    device = "/dev/mmcblk0p2";
                    sha256 = "abc123def456...";
                    encrypted = true;
                    ivt = "ivt.bin";
                }
            );
            
            scripts: (
                {
                    filename = "post_update.sh";
                    type = "shellscript";
                }
            );
        };
    }

**Encrypted OTA** (AES-256-CBC)::

    # Encrypt update package
    openssl enc -aes-256-cbc -in rootfs.squashfs -out rootfs.squashfs.enc \
        -pass file:aes.key -pbkdf2
    
    # Generate IVT for HAB
    gen_ivt rootfs.squashfs.enc ivt.bin
    
    # Create SWUpdate package
    sw-update-sign -s sw-description -k priv.pem rootfs.squashfs.enc post_update.sh

Section 4: Power Management
=============================

4.1 Hibernation Implementation (Thermal)
------------------------------------------

**Project**: #7 (ARM9 DaVinci Thermal Imaging)

**Achievement**: < 8mW power consumption, < 2s wake-up

Hibernation Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    [Running State]
         ↓ User triggers hibernate (button/timeout)
    [Pre-Hibernation Script]
         ├─ Stop non-critical services
         ├─ Flush all filesystems
         └─ Create minimal hibernation image
         ↓
    [Kernel Hibernation]
         ├─ Save RAM to NAND
         ├─ Power down peripherals
         └─ Enter deep sleep (< 8mW)
         ↓
    [Wake Event] (button press, RTC alarm)
         ↓
    [U-Boot]
         ├─ Detect hibernation image
         ├─ Load image to RAM (< 2s)
         └─ Jump to kernel resume
         ↓
    [Kernel Resume]
         ├─ Restore devices
         └─ Resume processes
         ↓
    [Post-Resume Script]
         └─ Restart services
         ↓
    [Running State Restored]

Hibernation Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Kernel Configuration**::

    CONFIG_HIBERNATION=y
    CONFIG_PM_STD_PARTITION="/dev/mmcblk0p3"  # Swap partition for hibernation
    CONFIG_PM_SLEEP=y
    CONFIG_SUSPEND=y
    CONFIG_PM_AUTOSLEEP=n  # Manual hibernation only
    CONFIG_TOI=y  # TuxOnIce for faster hibernation (optional)

**Hibernation Script** (/usr/sbin/thermal-hibernate)::

    #!/bin/sh
    # Thermal imaging hibernation script
    
    echo "Preparing for hibernation..."
    
    # 1. Stop non-critical services
    systemctl stop thermal-processing.service
    systemctl stop networking.service
    systemctl stop bluetooth.service
    
    # 2. Flush filesystem caches
    sync
    echo 3 > /proc/sys/vm/drop_caches
    
    # 3. Minimize hibernation image
    echo 0 > /sys/power/image_size  # Minimal image for fast resume
    
    # 4. Configure wake sources
    echo enabled > /sys/devices/platform/gpio-keys/power/wakeup  # Power button
    echo enabled > /sys/class/rtc/rtc0/device/power/wakeup       # RTC alarm
    
    # 5. Enter hibernation
    echo disk > /sys/power/state
    
    # --- System hibernates here ---
    
    # --- Resume continues here ---
    echo "Resuming from hibernation..."
    
    # 6. Restart services
    systemctl start thermal-processing.service
    systemctl start networking.service
    systemctl start bluetooth.service
    
    echo "Hibernation resume complete"

**Resume Script** (U-Boot)::

    # U-Boot checks for hibernation image
    if test -e mmc 0:3 /hibernation_image; then
        echo "Hibernation image found, resuming..."
        
        # Load hibernation image to RAM
        load mmc 0:3 0x80000000 /hibernation_image
        
        # Calculate resume address
        setexpr resume_addr 0x80000000 + 0x1000
        
        # Jump to kernel resume
        go 0x80000000
    else
        # Normal boot
        boot
    fi

Ultra-Low Power State
~~~~~~~~~~~~~~~~~~~~~~

**Custom Deep Sleep** (< 50 µA)::

    /* Platform-specific deep sleep */
    void enter_ultra_low_power_state(void)
    {
        /* 1. Disable all non-essential peripherals */
        disable_video_processing();
        disable_dsp();
        disable_usb_controller();
        disable_ethernet();
        disable_mmc();
        
        /* 2. Keep only wake sources and minimal RAM refresh */
        /* - GPIO for power button */
        /* - RTC for alarms */
        /* - Minimal SDRAM self-refresh */
        
        /* 3. Configure SDRAM self-refresh */
        writel(SDRAM_SELF_REFRESH_ENABLE, SDRAM_CTRL_REG);
        
        /* 4. Gate all unnecessary clocks */
        clk_disable(CLK_VIDEO);
        clk_disable(CLK_DSP);
        clk_disable(CLK_USB);
        clk_disable(CLK_EMAC);
        
        /* 5. Enter ARM9 standby (WFI) */
        cpu_do_idle();
        
        /* Power consumption: < 50 µA */
        /* Wake latency: ~100 ms */
    }

**Interview Talking Point**:
*"Implemented 3-tier power management for thermal imaging: (1) Runtime PM for device-level power with 100ms autosuspend; (2) Hibernation to NAND with < 8mW power consumption and < 2s resume (minimal image, optimized U-Boot resume path, SDRAM self-refresh); (3) Ultra-low-power state < 50 µA (disabled all peripherals except GPIO wake button and RTC, SDRAM self-refresh, ARM9 WFI). Achieved 72-hour battery life from 24-hour baseline."*

Summary: Boot, Security & Power Management
===========================================

**Boot Optimization**:
- 3 projects with significant boot time improvements (5x, 2.5x, 2.5x)
- U-Boot customization (manufacturing tests, NAND BBT, silent console)
- Techniques: Minimal U-Boot, parallel init, SquashFS, built-in drivers

**Secure Boot**:
- 3 implementations: UEFI (avionics), HAB (IoT), Custom (thermal)
- UEFI: PKI hierarchy (PK/KEK/db), sbsign, module signing, 200+ signed binaries
- HAB: SRK keys, CSF signing, eFuse programming, closed mode
- SELinux: Custom policy, enforcing mode, MAC for avionics

**Power Management**:
- Hibernation: < 8mW, < 2s wake (minimal image, SDRAM self-refresh)
- Ultra-low-power: < 50 µA (all peripherals off, GPIO + RTC only)
- Battery life: 3x improvement (24h → 72h)

**OTA Updates**:
- SWUpdate integration with encrypted packages (AES-256)
- Atomic updates with rollback capability
- HAB-verified update images

**Interview Summary**:
*"I have deep expertise in boot optimization (15s → 3s, 5x improvement through U-Boot stripping, parallel init, minimal rootfs), secure boot (3 implementations: UEFI with full PKI for avionics, NXP HAB with eFuse-backed root of trust for IoT, custom verified boot for thermal), security hardening (SELinux enforcing with custom policies), and power management (< 8mW hibernation with < 2s resume, < 50 µA ultra-low-power mode, 3x battery life improvement). All implementations production-deployed and field-proven."*

End of Document
================

**Last Updated**: January 22, 2026
**Expertise Areas**: Boot optimization, Secure boot (UEFI/HAB), SELinux, Power management, OTA

© 2026 Madhavan Vivekanandan - All Rights Reserved
