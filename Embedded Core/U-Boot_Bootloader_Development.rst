═══════════════════════════════════════════════════════════════════════
U-BOOT BOOTLOADER DEVELOPMENT FOR EMBEDDED SYSTEMS
═══════════════════════════════════════════════════════════════════════

**Comprehensive Guide to U-Boot Customization and Secure Boot**  
**Domain:** Embedded Linux 🐧 | Bootloaders 🚀 | Secure Boot 🔒  
**Purpose:** U-Boot architecture, NXP HAB, device trees, OTA updates, multi-stage boot

═══════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 3
   :local:

═══════════════════════════════════════════════════════════════════════

✨ **TL;DR — 30-Second Overview**
─────────────────────────────────────────────────────────────────────────

**U-Boot** (Universal Boot Loader) is the de-facto bootloader for embedded Linux systems.

**Key Features:**
- **Multi-architecture:** ARM, x86, PowerPC, MIPS, RISC-V
- **Flexible:** Boot from eMMC, SD, USB, TFTP, NFS
- **Interactive:** Command-line interface for debugging
- **Secure Boot:** HAB (NXP), UEFI Secure Boot, Verified Boot (Android)
- **Device Tree:** Dynamic hardware configuration
- **Falcon Mode:** Fast boot (skip U-Boot shell, direct to kernel)

**Boot Flow:**
ROM → SPL (2nd Program Loader) → U-Boot → Linux Kernel → Init System → User Space

**Your Experience (i.MX 93):**
- U-Boot customization for smart home automation
- HAB secure boot implementation
- Device tree modifications
- OTA update support

═══════════════════════════════════════════════════════════════════════

🏗️ **1. U-BOOT ARCHITECTURE**
─────────────────────────────────────────────────────────────────────────

**1.1 Boot Flow Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical ARM SoC Boot Sequence (NXP i.MX Family):**

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │                    POWER ON / RESET                         │
   └──────────────────────┬──────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────┐
   │  Stage 1: Boot ROM (Mask ROM in SoC)                        │
   │  - Size: 96 KB - 256 KB (built into silicon)                │
   │  - Functions:                                               │
   │    * Initialize minimal hardware (clocks, DDR controller)   │
   │    * Detect boot source (eMMC, SD, USB, UART)               │
   │    * Load SPL/U-Boot from boot device                       │
   │    * HAB authentication (if secure boot enabled)            │
   │  - Read-only (cannot be modified)                           │
   └──────────────────────┬──────────────────────────────────────┘
                          │ Load SPL into SRAM
   ┌──────────────────────▼──────────────────────────────────────┐
   │  Stage 2: SPL (Secondary Program Loader)                    │
   │  - Size: 64 KB - 256 KB (fits in SRAM)                      │
   │  - Functions:                                               │
   │    * Initialize DDR RAM (full DRAM controller setup)        │
   │    * Initialize additional peripherals (UART, I2C)          │
   │    * Load U-Boot proper from storage                        │
   │    * Optional: Load TF-A (Trusted Firmware-A)               │
   │  - Minimal functionality (size-constrained)                 │
   └──────────────────────┬──────────────────────────────────────┘
                          │ Load U-Boot into DDR RAM
   ┌──────────────────────▼──────────────────────────────────────┐
   │  Stage 3: U-Boot (Main Bootloader)                          │
   │  - Size: 500 KB - 2 MB                                      │
   │  - Functions:                                               │
   │    * Full hardware initialization (all peripherals)         │
   │    * Load device tree blob (DTB)                            │
   │    * Load kernel image (zImage, Image.gz)                   │
   │    * Load initramfs (optional)                              │
   │    * Set kernel command line (bootargs)                     │
   │    * Interactive shell (for debugging)                      │
   │    * Network boot (TFTP, NFS)                               │
   │    * Firmware updates (OTA)                                 │
   │  - Full-featured bootloader                                 │
   └──────────────────────┬──────────────────────────────────────┘
                          │ Boot kernel
   ┌──────────────────────▼──────────────────────────────────────┐
   │  Stage 4: Linux Kernel                                      │
   │  - Decompress kernel image                                  │
   │  - Parse device tree                                        │
   │  - Initialize memory management                             │
   │  - Mount root filesystem                                    │
   │  - Start init process (systemd, sysvinit)                   │
   └──────────────────────┬──────────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────────┐
   │  Stage 5: User Space                                        │
   │  - Init system (systemd)                                    │
   │  - Services and applications                                │
   └─────────────────────────────────────────────────────────────┘

**Timing (i.MX 93 Example):**

.. code-block:: text

   Boot ROM:        100 ms (minimal DDR init, load SPL)
   SPL:             200 ms (full DDR init, load U-Boot)
   U-Boot:          500 ms (peripheral init, load kernel)
   Kernel Init:     1-2 seconds (decompress, mount rootfs)
   Systemd:         2-3 seconds (start services)
   ─────────────────────────────────────────────────────
   Total Boot Time: 4-6 seconds (to user space)

**1.2 U-Boot Directory Structure**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   u-boot/
   ├── arch/                  # Architecture-specific code
   │   ├── arm/               # ARM architecture
   │   │   ├── cpu/           # CPU families (cortex-a53, cortex-m7)
   │   │   ├── dts/           # Device tree source files
   │   │   ├── mach-imx/      # NXP i.MX platform code
   │   │   └── lib/           # ARM-specific libraries
   │   ├── x86/
   │   └── powerpc/
   ├── board/                 # Board-specific code
   │   ├── freescale/         # NXP boards
   │   │   ├── imx93_evk/     # i.MX 93 EVK
   │   │   └── imx8mp/        # i.MX 8M Plus
   │   └── custom_vendor/     # Your custom board
   ├── cmd/                   # U-Boot commands (bootm, run, env, etc.)
   ├── common/                # Common bootloader code
   │   ├── board_r.c          # Board initialization (runtime)
   │   ├── board_f.c          # Board initialization (early)
   │   └── spl/               # SPL code
   ├── configs/               # Default configurations (defconfig)
   │   ├── imx93_11x11_evk_defconfig
   │   └── your_board_defconfig
   ├── drivers/               # Device drivers
   │   ├── mmc/               # MMC/SD/eMMC
   │   ├── net/               # Ethernet
   │   ├── usb/               # USB
   │   └── serial/            # UART
   ├── env/                   # Environment variable storage
   ├── include/               # Header files
   │   └── configs/           # Board-specific config headers
   ├── lib/                   # Libraries (CRC, compression, crypto)
   └── tools/                 # Build tools (mkimage, dumpimage)

**1.3 Configuration System**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Three-Level Configuration:**

1. **defconfig** (configs/imx93_11x11_evk_defconfig):
   - High-level features (enable/disable drivers)
   - Example: ``CONFIG_DM_MMC=y``, ``CONFIG_CMD_NET=y``

2. **Kconfig** (drivers/*/Kconfig):
   - Menu-driven configuration (like Linux kernel)
   - Run: ``make menuconfig``

3. **Board header** (include/configs/imx93_evk.h):
   - Low-level settings (memory layout, boot commands)
   - Legacy (being phased out in favor of device tree)

**Example defconfig:**

.. code-block:: kconfig

   # configs/imx93_custom_defconfig
   
   CONFIG_ARM=y
   CONFIG_ARCH_IMX93=y
   CONFIG_SYS_TEXT_BASE=0x80200000
   CONFIG_SYS_MALLOC_LEN=0x2000000
   CONFIG_NR_DRAM_BANKS=2
   
   # SPL
   CONFIG_SPL=y
   CONFIG_SPL_TEXT_BASE=0x2049A000
   CONFIG_SPL_STACK=0x20519dd0
   
   # Boot options
   CONFIG_BOOTDELAY=3
   CONFIG_USE_BOOTCOMMAND=y
   CONFIG_BOOTCOMMAND="run mmcboot"
   
   # Drivers
   CONFIG_DM_MMC=y
   CONFIG_FSL_ESDHC_IMX=y
   CONFIG_MMC_HS400_SUPPORT=y
   CONFIG_DM_ETH=y
   CONFIG_FEC_MXC=y
   CONFIG_DM_SERIAL=y
   CONFIG_USB=y
   CONFIG_USB_EHCI_HCD=y
   
   # Commands
   CONFIG_CMD_MMC=y
   CONFIG_CMD_EXT4=y
   CONFIG_CMD_FAT=y
   CONFIG_CMD_DHCP=y
   CONFIG_CMD_PING=y
   CONFIG_CMD_I2C=y
   CONFIG_CMD_GPIO=y
   
   # Security
   CONFIG_IMX_HAB=y
   CONFIG_SECURE_BOOT=y

═══════════════════════════════════════════════════════════════════════

🔧 **2. BUILDING U-BOOT**
─────────────────────────────────────────────────────────────────────────

**2.1 Build Environment Setup**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Install Dependencies (Ubuntu/Debian):**

.. code-block:: bash

   # Cross-compilation toolchain
   sudo apt-get update
   sudo apt-get install -y \
       gcc-arm-linux-gnueabihf \
       gcc-aarch64-linux-gnu \
       device-tree-compiler \
       bison flex \
       libssl-dev \
       bc \
       u-boot-tools
   
   # For ARM64 (i.MX 93 with Cortex-A55)
   export CROSS_COMPILE=aarch64-linux-gnu-
   export ARCH=arm64

**Download U-Boot:**

.. code-block:: bash

   # Official U-Boot (mainline)
   git clone https://github.com/u-boot/u-boot.git
   cd u-boot
   git checkout v2024.01  # Latest stable
   
   # NXP vendor tree (recommended for i.MX)
   git clone https://github.com/nxp-imx/uboot-imx.git -b lf-6.6.3_1.0.0
   cd uboot-imx

**2.2 Build for i.MX 93**
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # build_uboot_imx93.sh
   
   export CROSS_COMPILE=aarch64-linux-gnu-
   export ARCH=arm64
   
   # Clean previous build
   make mrproper
   
   # Load default configuration
   make imx93_11x11_evk_defconfig
   
   # Optional: Customize configuration
   make menuconfig
   
   # Build U-Boot
   make -j$(nproc)
   
   # Output files:
   # - u-boot.bin        : U-Boot binary (main bootloader)
   # - u-boot-nodtb.bin  : U-Boot without device tree
   # - spl/u-boot-spl.bin: SPL binary
   # - u-boot.dtb        : Device tree blob
   # - u-boot.imx        : Bootable image for i.MX (SPL + U-Boot + DTB)
   
   echo "✅ Build complete!"
   echo "Flash image: u-boot.imx"
   ls -lh u-boot.imx

**2.3 Flash to eMMC/SD Card**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Flash U-Boot to SD Card:**

.. code-block:: bash

   # WARNING: Replace /dev/sdX with your actual SD card device
   # Check with: lsblk
   
   SD_DEVICE=/dev/sdX
   
   # i.MX requires U-Boot at offset 32 KB (sector 64 with 512-byte sectors)
   # or offset 33 KB for some variants
   
   sudo dd if=u-boot.imx of=$SD_DEVICE bs=1k seek=32 conv=fsync
   
   # Verify
   sudo dd if=$SD_DEVICE of=/tmp/verify.bin bs=1k skip=32 count=1024
   cmp u-boot.imx /tmp/verify.bin

**Flash U-Boot to eMMC (from Linux running on target):**

.. code-block:: bash

   # Transfer u-boot.imx to target via SCP
   scp u-boot.imx root@192.168.1.100:/tmp/
   
   # On target:
   ssh root@192.168.1.100
   
   # Identify eMMC device (usually /dev/mmcblk0)
   lsblk
   
   # Flash U-Boot
   dd if=/tmp/u-boot.imx of=/dev/mmcblk0 bs=1k seek=32 conv=fsync
   
   # Reboot to test
   reboot

═══════════════════════════════════════════════════════════════════════

🖥️ **3. U-BOOT COMMANDS**
─────────────────────────────────────────────────────────────────────────

**3.1 Essential Commands**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Environment Variables:**

.. code-block:: bash

   # U-Boot shell (press any key during boot to interrupt)
   
   # Print all environment variables
   printenv
   
   # Print specific variable
   printenv bootcmd
   
   # Set variable
   setenv serverip 192.168.1.10
   setenv bootargs 'console=ttymxc0,115200 root=/dev/mmcblk0p2 rootwait rw'
   
   # Save environment to persistent storage (eMMC/SD)
   saveenv
   
   # Delete variable
   setenv bootargs
   saveenv

**Memory Operations:**

.. code-block:: bash

   # Memory display (hexdump)
   md 0x80000000 100    # Display 256 bytes from 0x80000000
   md.b 0x80000000 10   # Display 16 bytes
   md.w 0x80000000 10   # Display 32 bytes (word)
   md.l 0x80000000 10   # Display 40 bytes (long)
   
   # Memory write
   mw 0x80000000 0xdeadbeef   # Write 0xdeadbeef to address
   
   # Memory copy
   cp 0x80000000 0x90000000 1000   # Copy 4096 bytes
   
   # Memory compare
   cmp 0x80000000 0x90000000 1000

**Storage Commands:**

.. code-block:: bash

   # MMC/SD/eMMC
   mmc list                  # List MMC devices
   mmc dev 0                 # Select MMC device 0
   mmc info                  # Show MMC info
   mmc part                  # Show partitions
   
   # Read from MMC to RAM
   mmc read 0x80000000 0x800 0x2000   # Read 4 MB from sector 0x800 to RAM
   
   # Write from RAM to MMC
   mmc write 0x80000000 0x800 0x2000
   
   # Filesystem operations (FAT/ext4)
   fatls mmc 0:1           # List files on MMC 0, partition 1 (FAT)
   ext4ls mmc 0:2 /boot    # List files on MMC 0, partition 2 (ext4)
   
   # Load file from filesystem to RAM
   fatload mmc 0:1 0x80000000 zImage         # Load zImage to RAM
   ext4load mmc 0:2 0x83000000 /boot/imx93-11x11-evk.dtb  # Load DTB

**Network Commands:**

.. code-block:: bash

   # Set network parameters
   setenv ipaddr 192.168.1.100
   setenv serverip 192.168.1.10
   setenv netmask 255.255.255.0
   setenv ethaddr 00:11:22:33:44:55
   
   # Ping test
   ping 192.168.1.10
   
   # TFTP download
   tftp 0x80000000 zImage         # Download zImage from TFTP server
   tftp 0x83000000 imx93.dtb      # Download DTB
   
   # DHCP
   dhcp                           # Get IP via DHCP

**Boot Commands:**

.. code-block:: bash

   # Boot kernel from memory
   bootm 0x80000000               # Boot kernel at 0x80000000
   
   # Boot kernel with device tree
   bootm 0x80000000 - 0x83000000  # kernel at 0x80, DTB at 0x83000000
   
   # Boot using bootcmd (defined in environment)
   boot
   
   # Run script
   run mmcboot                    # Run mmcboot script from environment

**3.2 Boot Scripts**
~~~~~~~~~~~~~~~~~~~~~

**Define Boot Script in Environment:**

.. code-block:: bash

   # Set boot command for eMMC/SD boot
   setenv mmcboot ' \
       mmc dev 0; \
       ext4load mmc 0:2 0x80000000 /boot/Image; \
       ext4load mmc 0:2 0x83000000 /boot/imx93-11x11-evk.dtb; \
       setenv bootargs console=ttymxc0,115200 root=/dev/mmcblk0p2 rootwait rw; \
       booti 0x80000000 - 0x83000000'
   
   # Set as default boot command
   setenv bootcmd 'run mmcboot'
   saveenv

**Create U-Boot Script File:**

.. code-block:: bash

   # boot.txt (on host machine)
   cat > boot.txt << 'EOF'
   echo "Booting from eMMC..."
   mmc dev 0
   ext4load mmc 0:2 ${kernel_addr_r} /boot/Image
   ext4load mmc 0:2 ${fdt_addr_r} /boot/imx93-11x11-evk.dtb
   setenv bootargs console=ttymxc0,115200 root=/dev/mmcblk0p2 rootwait rw
   booti ${kernel_addr_r} - ${fdt_addr_r}
   EOF
   
   # Convert to U-Boot script image
   mkimage -T script -C none -n 'Boot Script' -d boot.txt boot.scr
   
   # Copy to SD card
   sudo cp boot.scr /media/boot/
   
   # In U-Boot, load and run script
   ext4load mmc 0:1 0x80000000 boot.scr
   source 0x80000000

═══════════════════════════════════════════════════════════════════════

🔒 **4. SECURE BOOT (NXP HAB)**
─────────────────────────────────────────────────────────────────────────

**4.1 HAB (High Assurance Boot) Overview**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is HAB:**
- NXP's secure boot mechanism for i.MX processors
- Authenticates bootloader and kernel using digital signatures
- Prevents unauthorized firmware from running
- Uses RSA-2048 or RSA-4096 public key cryptography

**HAB Boot Flow:**

.. code-block:: text

   ┌────────────────────────────────────────────────────┐
   │  Boot ROM (BootROM)                                │
   │  - Contains HAB library (built into silicon)       │
   │  - SRK (Super Root Key) hash fused in OTP          │
   └────────────┬───────────────────────────────────────┘
                │
                │ Load SPL
                │
   ┌────────────▼───────────────────────────────────────┐
   │  HAB Authentication (SPL)                          │
   │  1. Read SPL from storage                          │
   │  2. Parse IVT (Image Vector Table)                 │
   │  3. Parse CSF (Command Sequence File)              │
   │  4. Verify signature using SRK public key          │
   │  5. Compute hash of SPL image                      │
   │  6. Compare with signed hash                       │
   │     ✅ Match → Continue boot                       │
   │     ❌ Mismatch → HALT BOOT (secure mode)          │
   └────────────┬───────────────────────────────────────┘
                │
                │ SPL loads U-Boot
                │
   ┌────────────▼───────────────────────────────────────┐
   │  HAB Authentication (U-Boot)                       │
   │  - Same process as SPL                             │
   │  - U-Boot signature verified                       │
   └────────────┬───────────────────────────────────────┘
                │
                │ U-Boot loads kernel
                │
   ┌────────────▼───────────────────────────────────────┐
   │  Kernel Signature Verification (Optional)          │
   │  - Can use IMA (Integrity Measurement Arch)        │
   │  - Or U-Boot Verified Boot (FIT image signature)   │
   └────────────────────────────────────────────────────┘

**4.2 Generating HAB Keys**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Install NXP Code Signing Tool (CST):**

.. code-block:: bash

   # Download from NXP website (requires account)
   # https://www.nxp.com/webapp/sps/download/license.jsp?colCode=IMX_CST_TOOL
   
   # Extract
   tar xzf cst-3.3.1.tar.gz
   cd cst-3.3.1
   
   # Install dependencies
   sudo apt-get install -y libssl-dev

**Generate PKI Tree (Keys and Certificates):**

.. code-block:: bash

   cd cst-3.3.1/keys
   
   # Edit serial and key_length in serial and key_length files
   echo "12345678" > serial
   echo "4096" > key_length   # RSA-4096 (or 2048 for faster boot)
   
   # Generate keys
   ./hab4_pki_tree.sh
   
   # Generated files:
   # - SRK (Super Root Keys): SRK1-4 (4 keys, fuse hash of 1-4)
   # - CSF (Command Sequence File) keys: CSF1-4
   # - IMG (Image) keys: IMG1-4
   # - SRK_1_2_3_4_table.bin: Table of SRK public keys
   # - SRK_1_2_3_4_fuse.bin: SRK hash to fuse into OTP

**Key Hierarchy:**

.. code-block:: text

   SRK (Super Root Keys) - 4 keys
   ├── SRK1 ──┬── CSF1 (signs Command Sequence File)
   │          └── IMG1 (signs boot images)
   ├── SRK2 ──┬── CSF2
   │          └── IMG2
   ├── SRK3 ──┬── CSF3
   │          └── IMG3
   └── SRK4 ──┬── CSF4
              └── IMG4
   
   Only SRK hash is fused (not individual keys)
   → Can revoke individual SRKs without re-fusing

**4.3 Signing U-Boot with HAB**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Create CSF (Command Sequence File):**

.. code-block:: bash

   # csf_uboot.txt
   [Header]
   Version = 4.3
   Hash Algorithm = sha256
   Engine = CAAM
   Engine Configuration = 0
   Certificate Format = X509
   Signature Format = CMS
   
   [Install SRK]
   File = "../crts/SRK_1_2_3_4_table.bin"
   Source index = 0   # Use SRK1
   
   [Install CSFK]
   File = "../crts/CSF1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate CSF]
   
   [Install Key]
   Verification index = 0
   Target index = 2
   File = "../crts/IMG1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate Data]
   Verification index = 2
   Blocks = 0x80000000 0x0 0x80000 "u-boot.imx"
   
   # Blocks format: <RAM address> <offset in file> <size> <filename>
   # Adjust addresses based on your U-Boot link address

**Sign U-Boot:**

.. code-block:: bash

   # Generate CSF binary
   ../linux64/bin/cst --o csf_uboot.bin --i csf_uboot.txt
   
   # Append CSF to U-Boot image
   cat u-boot.imx csf_uboot.bin > u-boot-signed.imx
   
   # Pad to specific size if needed
   objcopy -I binary -O binary --pad-to 0x100000 --gap-fill=0x00 \
       u-boot-signed.imx u-boot-signed-padded.imx

**4.4 Fusing SRK Hash (ONE-TIME, IRREVERSIBLE)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # ⚠️  WARNING: Fusing is IRREVERSIBLE!
   # Test thoroughly before fusing production boards
   
   # 1. Boot into U-Boot (unsigned, open mode)
   
   # 2. Check current fuse values (should be all zeros for unfused board)
   fuse read 6 0   # Read SRK hash bank 6, word 0-7
   
   # 3. Display SRK hash to fuse
   hexdump -C SRK_1_2_3_4_fuse.bin
   
   # 4. Fuse SRK hash (example for i.MX 93)
   # Bank 6, words 0-7 contain the SRK hash
   fuse prog 6 0 0x12345678   # Word 0
   fuse prog 6 1 0x9ABCDEF0   # Word 1
   # ... continue for all 8 words (256-bit hash)
   
   # 5. Close the device (enable secure boot)
   fuse prog 1 3 0x00000001   # Set SRK_LOCK
   
   # 6. Reboot - device now requires signed images
   reset

**Test Secure Boot:**

.. code-block:: bash

   # Flash signed U-Boot
   dd if=u-boot-signed.imx of=/dev/mmcblk0 bs=1k seek=32
   
   # Reboot - should boot normally
   reboot
   
   # Flash unsigned U-Boot (should FAIL to boot in secure mode)
   dd if=u-boot.imx of=/dev/mmcblk0 bs=1k seek=32
   reboot   # Device will hang at BootROM (authentication failure)

**4.5 HAB Status Commands**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # In U-Boot shell:
   
   # Check HAB status
   hab_status
   
   # Example output (open mode, unsigned image):
   # Secure boot disabled
   # HAB Configuration: 0xf0, HAB State: 0x66
   # No HAB Events Found!
   
   # Example output (closed mode, authentication failure):
   # Secure boot enabled
   # HAB Configuration: 0xcc, HAB State: 0x99
   # 
   # --------- HAB Event 1 -----------------
   # event data:
   #     0xdb 0x00 0x24 0x42 0x33 0x22 0x0a 0x00
   # Status = HAB_FAILURE (0x33)
   # Reason = HAB_INV_SIGNATURE (0x22)
   # Context = HAB_CTX_AUTHENTICATE (0x0a)
   # Engine = HAB_ENG_ANY (0x00)

═══════════════════════════════════════════════════════════════════════

🌳 **5. DEVICE TREE IN U-BOOT**
─────────────────────────────────────────────────────────────────────────

**5.1 Device Tree Basics**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is Device Tree:**
- Hardware description in text format (`.dts`)
- Compiled to binary blob (`.dtb`)
- Passed from U-Boot to kernel
- Describes: memory, CPUs, peripherals, pin muxing

**Device Tree Structure:**

.. code-block:: dts

   /dts-v1/;
   
   / {
       model = "NXP i.MX93 11x11 EVK board";
       compatible = "fsl,imx93-11x11-evk", "fsl,imx93";
       
       #address-cells = <2>;
       #size-cells = <2>;
       
       chosen {
           bootargs = "console=ttymxc0,115200 earlycon";
           stdout-path = &lpuart1;
       };
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x0 0x80000000 0 0x80000000>;  /* 2 GB DDR */
       };
       
       cpus {
           #address-cells = <1>;
           #size-cells = <0>;
           
           cpu@0 {
               device_type = "cpu";
               compatible = "arm,cortex-a55";
               reg = <0x0>;
               enable-method = "psci";
           };
           
           cpu@100 {
               device_type = "cpu";
               compatible = "arm,cortex-a55";
               reg = <0x100>;
               enable-method = "psci";
           };
       };
       
       soc {
           compatible = "simple-bus";
           #address-cells = <1>;
           #size-cells = <1>;
           ranges = <0x0 0x0 0x0 0x40000000>;
           
           lpuart1: serial@44380000 {
               compatible = "fsl,imx93-lpuart", "fsl,imx7ulp-lpuart";
               reg = <0x44380000 0x1000>;
               interrupts = <GIC_SPI 19 IRQ_TYPE_LEVEL_HIGH>;
               clocks = <&clk IMX93_CLK_LPUART1>;
               clock-names = "ipg";
               status = "okay";
           };
           
           usdhc1: mmc@42850000 {
               compatible = "fsl,imx93-usdhc", "fsl,imx8mm-usdhc";
               reg = <0x42850000 0x10000>;
               interrupts = <GIC_SPI 86 IRQ_TYPE_LEVEL_HIGH>;
               clocks = <&clk IMX93_CLK_USDHC1>;
               clock-names = "per";
               bus-width = <4>;
               status = "okay";
           };
       };
   };

**5.2 Modifying Device Tree in U-Boot**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Runtime Device Tree Modification (fdt commands):**

.. code-block:: bash

   # Load device tree to memory
   ext4load mmc 0:2 0x83000000 /boot/imx93-11x11-evk.dtb
   
   # Set FDT address for manipulation
   fdt addr 0x83000000
   
   # Print device tree
   fdt print /
   fdt print /chosen
   
   # Modify bootargs
   fdt set /chosen bootargs "console=ttymxc0,115200 root=/dev/mmcblk0p2 rw"
   
   # Add property
   fdt set /soc/serial@44380000 status "okay"
   
   # Remove property
   fdt rm /soc/serial@44380000 status
   
   # Resize FDT (if adding many nodes)
   fdt resize 4096
   
   # Boot with modified DTB
   booti 0x80000000 - 0x83000000

**Overlay Support:**

.. code-block:: bash

   # Load base DTB
   ext4load mmc 0:2 0x83000000 /boot/imx93-11x11-evk.dtb
   
   # Load overlay
   ext4load mmc 0:2 0x83100000 /boot/overlays/custom-overlay.dtbo
   
   # Apply overlay
   fdt addr 0x83000000
   fdt resize 8192
   fdt apply 0x83100000
   
   # Boot with modified DTB
   booti 0x80000000 - 0x83000000

**5.3 Device Tree Overlay Example**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Enable Additional UART (overlay):**

.. code-block:: dts

   // custom-uart.dtso (device tree overlay source)
   /dts-v1/;
   /plugin/;
   
   &lpuart2 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_lpuart2>;
   };
   
   &iomuxc {
       pinctrl_lpuart2: lpuart2grp {
           fsl,pins = <
               MX93_PAD_UART2_TXD__LPUART2_TX  0x31e
               MX93_PAD_UART2_RXD__LPUART2_RX  0x31e
           >;
       };
   };

**Compile Overlay:**

.. code-block:: bash

   # Compile overlay
   dtc -@ -I dts -O dtb -o custom-uart.dtbo custom-uart.dtso
   
   # Copy to boot partition
   cp custom-uart.dtbo /boot/overlays/

═══════════════════════════════════════════════════════════════════════

🔄 **6. OTA (OVER-THE-AIR) UPDATES**
─────────────────────────────────────────────────────────────────────────

**6.1 Dual Boot Partition Strategy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Partition Layout:**

.. code-block:: text

   /dev/mmcblk0 (eMMC)
   ├── Boot Area (Hardware Boot Partition - 4 MB)
   │   └── U-Boot (u-boot.imx @ offset 32 KB)
   ├── p1: boot_a (FAT32, 128 MB)  - Active boot partition
   │   ├── Image_a
   │   └── imx93.dtb_a
   ├── p2: rootfs_a (ext4, 2 GB)   - Active root filesystem
   ├── p3: boot_b (FAT32, 128 MB)  - Backup boot partition
   │   ├── Image_b
   │   └── imx93.dtb_b
   ├── p4: rootfs_b (ext4, 2 GB)   - Backup root filesystem
   └── p5: data (ext4, remaining)  - User data (preserved across updates)

**Boot Logic (A/B Selection):**

.. code-block:: bash

   # U-Boot environment variables
   setenv boot_partition a           # Current active partition (a or b)
   setenv boot_count 0               # Boot attempt counter
   setenv boot_limit 3               # Max boot attempts before fallback
   
   # Boot script
   setenv do_boot ' \
       if test "${boot_partition}" = "a"; then \
           setenv bootpart 1; \
           setenv rootpart 2; \
       else \
           setenv bootpart 3; \
           setenv rootpart 4; \
       fi; \
       ext4load mmc 0:${bootpart} ${kernel_addr_r} Image_${boot_partition}; \
       ext4load mmc 0:${bootpart} ${fdt_addr_r} imx93.dtb_${boot_partition}; \
       setenv bootargs console=ttymxc0,115200 root=/dev/mmcblk0p${rootpart} rootwait rw; \
       booti ${kernel_addr_r} - ${fdt_addr_r}'
   
   # Boot with fallback
   setenv bootcmd ' \
       setexpr boot_count ${boot_count} + 1; \
       saveenv; \
       run do_boot; \
       if test ${boot_count} -ge ${boot_limit}; then \
           echo "Boot failed ${boot_limit} times, switching to backup partition"; \
           if test "${boot_partition}" = "a"; then \
               setenv boot_partition b; \
           else \
               setenv boot_partition a; \
           fi; \
           setenv boot_count 0; \
           saveenv; \
           reset; \
       fi'
   
   saveenv

**6.2 OTA Update Process**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Update Workflow:**

.. code-block:: text

   1. System running from partition A (boot_a + rootfs_a)
   2. Download new firmware to inactive partition B (boot_b + rootfs_b)
   3. Verify downloaded firmware (checksum, signature)
   4. Mark partition B as active (switch boot_partition variable)
   5. Reboot into partition B
   6. If boot successful (boot_count reset), mark update complete
   7. If boot fails 3 times, rollback to partition A

**Update Script (Linux):**

.. code-block:: bash

   #!/bin/bash
   # ota_update.sh - Perform OTA update
   
   set -e
   
   CURRENT_PART=$(fw_printenv -n boot_partition)
   
   if [ "$CURRENT_PART" = "a" ]; then
       NEW_PART="b"
       BOOT_DEV="/dev/mmcblk0p3"
       ROOTFS_DEV="/dev/mmcblk0p4"
   else
       NEW_PART="a"
       BOOT_DEV="/dev/mmcblk0p1"
       ROOTFS_DEV="/dev/mmcblk0p2"
   fi
   
   echo "Current partition: $CURRENT_PART"
   echo "Updating to partition: $NEW_PART"
   
   # Download firmware
   echo "Downloading firmware..."
   wget -O /tmp/Image https://update-server.com/firmware/Image
   wget -O /tmp/imx93.dtb https://update-server.com/firmware/imx93.dtb
   wget -O /tmp/rootfs.tar.gz https://update-server.com/firmware/rootfs.tar.gz
   
   # Verify checksums
   echo "Verifying checksums..."
   wget -O /tmp/checksums.txt https://update-server.com/firmware/checksums.txt
   cd /tmp
   sha256sum -c checksums.txt || { echo "Checksum verification failed!"; exit 1; }
   
   # Write boot files
   echo "Writing boot files..."
   mkdir -p /mnt/boot_new
   mount $BOOT_DEV /mnt/boot_new
   cp /tmp/Image /mnt/boot_new/Image_${NEW_PART}
   cp /tmp/imx93.dtb /mnt/boot_new/imx93.dtb_${NEW_PART}
   sync
   umount /mnt/boot_new
   
   # Write rootfs
   echo "Writing root filesystem..."
   mkfs.ext4 -F $ROOTFS_DEV
   mkdir -p /mnt/rootfs_new
   mount $ROOTFS_DEV /mnt/rootfs_new
   tar xzf /tmp/rootfs.tar.gz -C /mnt/rootfs_new
   sync
   umount /mnt/rootfs_new
   
   # Switch boot partition
   echo "Switching to new partition..."
   fw_setenv boot_partition $NEW_PART
   fw_setenv boot_count 0
   
   echo "✅ Update complete! Rebooting..."
   sleep 3
   reboot

**6.3 Rollback Mechanism**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Automatic Rollback (in U-Boot):**

Already implemented in bootcmd above - if boot fails 3 times, automatically switches partition.

**Manual Rollback (from Linux):**

.. code-block:: bash

   #!/bin/bash
   # rollback.sh - Manual rollback to previous partition
   
   CURRENT_PART=$(fw_printenv -n boot_partition)
   
   if [ "$CURRENT_PART" = "a" ]; then
       fw_setenv boot_partition b
       echo "Rolling back to partition B"
   else
       fw_setenv boot_partition a
       echo "Rolling back to partition A"
   fi
   
   fw_setenv boot_count 0
   
   echo "Rebooting to previous partition..."
   reboot

**Mark Boot Successful (from Linux init):**

.. code-block:: bash

   # /etc/init.d/boot-check (systemd service)
   #!/bin/bash
   
   # Reset boot counter on successful boot
   fw_setenv boot_count 0
   
   # Optional: Mark this partition as "verified good"
   CURRENT_PART=$(fw_printenv -n boot_partition)
   fw_setenv last_good_partition $CURRENT_PART

═══════════════════════════════════════════════════════════════════════

⚡ **7. PERFORMANCE OPTIMIZATION**
─────────────────────────────────────────────────────────────────────────

**7.1 Falcon Mode (Fast Boot)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is Falcon Mode:**
- Skip U-Boot interactive shell
- Jump directly from SPL to kernel
- Reduces boot time by 500-1000 ms

**Enable Falcon Mode:**

.. code-block:: bash

   # In U-Boot menuconfig:
   # CONFIG_SPL_OS_BOOT=y
   # CONFIG_SPL_FALCON_BOOT=y
   
   # Prepare Falcon mode (one-time setup)
   
   # 1. Load kernel and DTB to RAM
   ext4load mmc 0:2 0x80000000 /boot/Image
   ext4load mmc 0:2 0x83000000 /boot/imx93.dtb
   
   # 2. Prepare boot arguments
   setenv bootargs 'console=ttymxc0,115200 root=/dev/mmcblk0p2 rootwait rw'
   
   # 3. Save Falcon mode parameters
   spl export fdt 0x80000000 - 0x83000000
   
   # 4. Write kernel, DTB, and boot params to raw MMC sectors
   # (SPL will load from these fixed locations)
   mmc write 0x80000000 0x10000 0x8000    # Write kernel at sector 0x10000
   mmc write 0x83000000 0x18000 0x100     # Write DTB at sector 0x18000
   mmc write <args_addr> 0x19000 0x10     # Write boot args
   
   # 5. Enable Falcon mode
   setenv boot_os yes
   saveenv
   
   # Next boot: SPL directly boots kernel (bypasses U-Boot shell)

**Disable Falcon Mode (for debugging):**

.. code-block:: bash

   # Hold down a button during boot to interrupt
   # Or:
   setenv boot_os no
   saveenv

**7.2 Boot Time Optimization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Techniques:**

.. code-block:: bash

   # 1. Reduce bootdelay
   setenv bootdelay 0   # No delay (vs default 3 seconds)
   
   # 2. Disable unnecessary drivers in U-Boot
   # In menuconfig, disable: USB, PCI, SATA if not needed for boot
   
   # 3. Use compressed kernel (if not already)
   # Image.gz instead of Image (saves load time)
   
   # 4. Optimize DDR training
   # Use saved DDR training results (avoid re-training each boot)
   
   # 5. Parallel initialization
   # Enable CONFIG_SYS_INIT_SP_BSS_OFFSET for faster BSS clearing
   
   # 6. Skip unnecessary hardware init
   # Disable unused peripherals in device tree (status = "disabled")

**Measure Boot Time:**

.. code-block:: bash

   # Enable boot timing in U-Boot
   setenv bootchart yes
   
   # Or use Linux bootchart/systemd-analyze after boot
   systemd-analyze
   systemd-analyze blame

═══════════════════════════════════════════════════════════════════════

🐛 **8. DEBUGGING U-BOOT**
─────────────────────────────────────────────────────────────────────────

**8.1 Serial Console**
~~~~~~~~~~~~~~~~~~~~~~~

**Connect Serial Console:**

.. code-block:: bash

   # Hardware: USB-to-TTL adapter (FTDI, CP2102)
   # Connections:
   # - TX (board) → RX (adapter)
   # - RX (board) → TX (adapter)
   # - GND (board) → GND (adapter)
   
   # On host:
   sudo minicom -D /dev/ttyUSB0 -b 115200
   
   # Or:
   sudo screen /dev/ttyUSB0 115200
   
   # Or:
   sudo picocom -b 115200 /dev/ttyUSB0

**Enable Verbose Output:**

.. code-block:: bash

   # In U-Boot:
   setenv loglevel 7   # Maximum debug output
   
   # In Linux kernel boot:
   setenv bootargs '... loglevel=7 debug'

**8.2 JTAG Debugging**
~~~~~~~~~~~~~~~~~~~~~~

**JTAG Setup (Segger J-Link):**

.. code-block:: bash

   # Install J-Link software
   wget https://www.segger.com/downloads/jlink/JLink_Linux_x86_64.deb
   sudo dpkg -i JLink_Linux_x86_64.deb
   
   # Connect J-Link to board (20-pin JTAG header)
   # Start GDB server
   JLinkGDBServer -device MCIMX93_M33 -if JTAG -speed 4000
   
   # In another terminal, connect GDB
   aarch64-linux-gnu-gdb u-boot
   (gdb) target remote localhost:2331
   (gdb) load
   (gdb) break board_init_r
   (gdb) continue

**8.3 Common Issues**
~~~~~~~~~~~~~~~~~~~~~

**Issue 1: U-Boot Hangs at "Starting kernel..."**

.. code-block:: bash

   # Causes:
   # - Incorrect kernel load address
   # - DTB not loaded or wrong address
   # - Kernel expects different boot protocol
   
   # Solutions:
   # 1. Verify load addresses
   printenv kernel_addr_r fdt_addr_r
   
   # 2. Check kernel boot protocol
   file Image   # Should show "ARM64 executable"
   
   # 3. Use correct boot command
   booti ${kernel_addr_r} - ${fdt_addr_r}   # For ARM64 Image
   # Not: bootm (for uImage/zImage)

**Issue 2: "Bad Data CRC" when loading from MMC**

.. code-block:: bash

   # Causes:
   # - Corrupted filesystem
   # - Wrong partition number
   
   # Solutions:
   # 1. Verify partition
   mmc part
   
   # 2. Check filesystem
   ext4ls mmc 0:2 /boot
   
   # 3. Re-flash kernel
   # (from Linux:)
   dd if=Image of=/dev/mmcblk0p2 bs=1M

**Issue 3: Secure Boot Authentication Failure**

.. code-block:: bash

   # Check HAB status
   hab_status
   
   # If signature verification failed:
   # - Verify CSF addresses match U-Boot link address
   # - Check SRK hash fused correctly
   # - Ensure using correct signing keys
   
   # Test with unsigned image first (if not fused)

═══════════════════════════════════════════════════════════════════════

📚 **9. PRACTICAL EXAMPLES**
─────────────────────────────────────────────────────────────────────────

**9.1 Custom Board Porting**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Steps to Port U-Boot to Custom Board:**

.. code-block:: bash

   # 1. Copy reference board configuration
   cd u-boot
   cp -r board/freescale/imx93_evk board/mycompany/myboard
   cp configs/imx93_11x11_evk_defconfig configs/myboard_defconfig
   cp include/configs/imx93_evk.h include/configs/myboard.h
   
   # 2. Edit defconfig
   vim configs/myboard_defconfig
   # Change:
   # CONFIG_SYS_BOARD="myboard"
   # CONFIG_SYS_VENDOR="mycompany"
   
   # 3. Modify device tree
   cp arch/arm/dts/imx93-11x11-evk.dts arch/arm/dts/myboard.dts
   vim arch/arm/dts/myboard.dts
   # - Adjust memory size
   # - Configure pin muxing
   # - Enable/disable peripherals
   
   # 4. Update board-specific code
   vim board/mycompany/myboard/myboard.c
   # - board_init(): Hardware initialization
   # - board_late_init(): Late init (env setup)
   # - checkboard(): Display board info
   
   # 5. Build
   make CROSS_COMPILE=aarch64-linux-gnu- myboard_defconfig
   make CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

**9.2 Network Boot (TFTP)**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Setup TFTP Server (on development machine):**

.. code-block:: bash

   # Install TFTP server
   sudo apt-get install -y tftpd-hpa
   
   # Configure TFTP
   sudo vim /etc/default/tftpd-hpa
   # TFTP_USERNAME="tftp"
   # TFTP_DIRECTORY="/tftpboot"
   # TFTP_ADDRESS="0.0.0.0:69"
   # TFTP_OPTIONS="--secure"
   
   # Create TFTP directory
   sudo mkdir -p /tftpboot
   sudo chmod 777 /tftpboot
   
   # Copy kernel and DTB
   cp Image /tftpboot/
   cp imx93.dtb /tftpboot/
   
   # Restart TFTP server
   sudo systemctl restart tftpd-hpa

**Boot from TFTP (in U-Boot):**

.. code-block:: bash

   # Set network parameters
   setenv ipaddr 192.168.1.100
   setenv serverip 192.168.1.10
   setenv netmask 255.255.255.0
   
   # Download and boot
   tftp ${kernel_addr_r} Image
   tftp ${fdt_addr_r} imx93.dtb
   setenv bootargs 'console=ttymxc0,115200 root=/dev/nfs nfsroot=192.168.1.10:/nfs/rootfs,v3 ip=dhcp'
   booti ${kernel_addr_r} - ${fdt_addr_r}

**9.3 USB Recovery Mode**
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Force USB Boot (Rescue Mode):**

.. code-block:: bash

   # i.MX boards support USB Serial Download Protocol (SDP)
   
   # 1. Set boot mode DIP switches to USB boot
   #    (or short specific pads on board)
   
   # 2. Install imx_usb_loader tool
   git clone https://github.com/boundarydevices/imx_usb_loader.git
   cd imx_usb_loader
   make
   sudo make install
   
   # 3. Connect USB OTG cable
   
   # 4. Download U-Boot to RAM and execute
   sudo imx_usb u-boot.imx
   
   # 5. U-Boot runs from RAM (not persistent)
   # Can now flash new U-Boot to eMMC

═══════════════════════════════════════════════════════════════════════

📝 **QUICK REFERENCE**
─────────────────────────────────────────────────────────────────────────

**Essential U-Boot Commands**

.. code-block:: bash

   # Environment
   printenv            # Show all variables
   setenv var value    # Set variable
   saveenv             # Save to storage
   
   # Memory
   md 0x80000000      # Memory dump
   mw 0x80000000 0xff # Memory write
   
   # Storage
   mmc list           # List MMC devices
   mmc dev 0          # Select device
   mmc info           # Device info
   ext4load mmc 0:2 0x80000000 /boot/Image
   
   # Network
   ping 192.168.1.10
   tftp 0x80000000 Image
   
   # Boot
   booti 0x80000000 - 0x83000000  # Boot ARM64 kernel
   
   # Device Tree
   fdt addr 0x83000000
   fdt print /chosen
   
   # HAB
   hab_status         # Check secure boot status

**Build Commands**

.. code-block:: bash

   # Configure
   make CROSS_COMPILE=aarch64-linux-gnu- imx93_11x11_evk_defconfig
   make menuconfig
   
   # Build
   make CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
   
   # Flash
   dd if=u-boot.imx of=/dev/sdX bs=1k seek=32 conv=fsync

**Boot Time Breakdown (i.MX 93)**

.. code-block:: text

   ROM:         100 ms
   SPL:         200 ms
   U-Boot:      500 ms
   Kernel:      1-2 sec
   Systemd:     2-3 sec
   ────────────────────
   Total:       4-6 sec

═══════════════════════════════════════════════════════════════════════

✅ **KEY TAKEAWAYS**
─────────────────────────────────────────────────────────────────────────

**U-Boot Architecture:**
1. ✅ **Multi-stage boot:** ROM → SPL → U-Boot → Kernel
2. ✅ **Flexible:** Boot from eMMC, SD, USB, TFTP, NFS
3. ✅ **Interactive:** Command-line for debugging
4. ✅ **Configurable:** defconfig + Kconfig + device tree

**Secure Boot (HAB):**
1. ✅ **RSA-4096 signatures:** Authenticate bootloader and kernel
2. ✅ **SRK fusing:** One-time operation (irreversible)
3. ✅ **CST tool:** Generate keys, sign images
4. ✅ **Chain of trust:** ROM → SPL → U-Boot → Kernel

**Device Tree:**
1. ✅ **Hardware description:** Passed from U-Boot to kernel
2. ✅ **Runtime modification:** fdt commands
3. ✅ **Overlays:** Modular hardware configuration
4. ✅ **DTS → DTB:** Compile with dtc

**OTA Updates:**
1. ✅ **Dual partitions:** A/B boot + rootfs
2. ✅ **Automatic rollback:** If boot fails 3 times
3. ✅ **Safe updates:** Write to inactive partition
4. ✅ **Environment variables:** Switch boot_partition

**Performance:**
1. ✅ **Falcon Mode:** SPL → Kernel (skip U-Boot)
2. ✅ **Boot time:** 4-6 seconds typical
3. ✅ **Optimization:** Disable unused drivers, reduce delays

**Your Experience (i.MX 93):**
- ✅ U-Boot customization for smart home platform
- ✅ HAB secure boot implementation
- ✅ Device tree modifications
- ✅ OTA update support
- ✅ Bootloader debugging and optimization

═══════════════════════════════════════════════════════════════════════

**References:**

- U-Boot Documentation: https://u-boot.readthedocs.io/
- NXP i.MX Linux User Guide: https://www.nxp.com/imx-linux
- NXP HAB Security Reference Manual: AN4581
- Device Tree Specification: https://www.devicetree.org/
- Falcon Mode: doc/README.falcon (in U-Boot source)

**Last Updated:** January 2026 | **U-Boot Version:** 2024.01

═══════════════════════════════════════════════════════════════════════
