==================================
Linux Boot Process - Complete Guide
==================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Experience: i.MX 93, Intel Atom C3xxx, TI DaVinci platforms

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========

Comprehensive guide covering embedded Linux boot process from power-on to userspace, including SOC-specific implementations, bootloader customization, secure boot mechanisms, and boot optimization techniques based on real-world project experience.

Boot Sequence Overview
=======================

Standard Boot Flow
------------------

.. code-block:: text

   Power-On → Boot ROM → Bootloader (U-Boot/UEFI) → Kernel → Init System → Userspace
      ↓          ↓            ↓                        ↓         ↓            ↓
   HW Init   Secure     Load Kernel              Mount FS   systemd      Applications
             Boot       Device Tree              Init RAM   sysvinit

Multi-Stage Boot Process
-------------------------

+---------+-------------------+------------------------+------------------+
| Stage   | Component         | Responsibility         | Project Example  |
+=========+===================+========================+==================+
| Stage 0 | Boot ROM          | Initial HW setup       | i.MX HAB ROM     |
|         | (immutable)       | Load bootloader        | Intel ME         |
+---------+-------------------+------------------------+------------------+
| Stage 1 | SPL/BL1           | DRAM init              | U-Boot SPL       |
|         | (limited SRAM)    | Load main bootloader   | UEFI PEI         |
+---------+-------------------+------------------------+------------------+
| Stage 2 | Main Bootloader   | Load kernel/DTB        | U-Boot proper    |
|         | (U-Boot/UEFI)     | Device init            | UEFI DXE         |
+---------+-------------------+------------------------+------------------+
| Stage 3 | Kernel            | Device drivers         | Linux 5.x/6.x    |
|         |                   | Filesystem mount       |                  |
+---------+-------------------+------------------------+------------------+
| Stage 4 | Init System       | Service startup        | systemd/busybox  |
+---------+-------------------+------------------------+------------------+

SOC-Specific Boot Implementations
==================================

NXP i.MX Series Boot
--------------------

i.MX 93 Boot Flow (Project Experience)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Boot ROM Configuration:**

.. code-block:: c

   // eFuse Configuration
   BOOT_CFG[3:0] = 0x2;  // Boot from SD/eMMC
   SECURE_BOOT_EN = 1;    // Enable HAB
   
   // Boot ROM searches for bootloader
   // Offset: 0x400 (SD), 0x1000 (eMMC)

**High Assurance Boot (HAB):**

.. code-block:: bash

   # Generate HAB signing keys
   ./cst --key SRK_1_sha256_4096_65537_v3_ca_crt.pem \
         --cert IMG1_1_sha256_4096_65537_v3_usr_crt.pem \
         --input csf_config.txt \
         --output csf.bin
   
   # Create signed U-Boot image
   cat u-boot-dtb.imx csf.bin > u-boot-signed.imx
   
   # Flash eFuse with SRK hash (one-time programmable)
   echo "SRK Hash: $(sha256sum srk_table.bin)"

**Heterogeneous Boot (Cortex-A55 + Cortex-M33):**

.. code-block:: c

   // Device Tree configuration
   reserved-memory {
       m33_reserved: m33@a4000000 {
           reg = <0xa4000000 0x1000000>;  // 16MB for M33
           no-map;
       };
   };
   
   remoteproc_m33: remoteproc@a4000000 {
       compatible = "fsl,imx93-cm33";
       clocks = <&clk IMX93_CLK_M33>;
       firmware-name = "rpmsg_lite_pingpong_rtos_linux_remote.elf";
   };

**Boot Optimization Results:**

- Cold boot: < 2 seconds (target < 6s for production)
- Secure boot overhead: ~200ms
- Parallel Cortex-A55 + M33 initialization

TI DaVinci (DM365/ARM9) Boot
----------------------------

**Boot ROM → UBL → U-Boot:**

.. code-block:: bash

   # NAND Flash Layout
   # 0x0000_0000 - 0x0002_0000: UBL (128KB)
   # 0x0002_0000 - 0x0010_0000: U-Boot (896KB)
   # 0x0010_0000 - 0x0050_0000: Kernel (4MB)
   # 0x0050_0000 - end: Rootfs
   
   # U-Boot NAND configuration
   nand write 0x82000000 0x20000 0xe0000  # Write U-Boot

**Custom Power States:**

.. code-block:: c

   // Hibernation with <8mW power consumption
   // Wake up in <2 seconds
   
   #include <mach/psc.h>
   
   void enter_hibernation(void) {
       // Save critical state to RTC RAM
       save_context_to_rtc();
       
       // Power down peripherals
       davinci_psc_config(DAVINCI_LPSC_USB, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_EMAC, 0, PSC_SWRSTDISABLE);
       
       // Enter deep sleep
       asm("wfi");  // Wait for interrupt
   }

**BBT (Bad Block Table) Support:**

.. code-block:: c

   // Custom NAND BBT implementation
   static struct nand_bbt_descr custom_bbt = {
       .options = NAND_BBT_LASTBLOCK | NAND_BBT_CREATE | NAND_BBT_WRITE,
       .offs = 8,
       .len = 4,
       .veroffs = 12,
       .maxblocks = 4,
       .pattern = bbt_pattern
   };

Intel Atom C3xxx Boot (Avionics Project)
-----------------------------------------

**UEFI Secure Boot Implementation:**

.. code-block:: bash

   # Generate platform keys
   openssl req -new -x509 -newkey rsa:2048 -keyout PK.key \
               -out PK.crt -days 3650 -nodes -subj "/CN=Platform Key/"
   
   openssl req -new -x509 -newkey rsa:2048 -keyout KEK.key \
               -out KEK.crt -days 3650 -nodes -subj "/CN=Key Exchange Key/"
   
   openssl req -new -x509 -newkey rsa:2048 -keyout db.key \
               -out db.crt -days 3650 -nodes -subj "/CN=Signature Database/"
   
   # Sign kernel and modules
   sbsign --key db.key --cert db.crt --output vmlinuz.signed vmlinuz
   
   # Enroll keys in UEFI
   efi-updatevar -f PK.auth PK
   efi-updatevar -f KEK.auth KEK
   efi-updatevar -f db.auth db

**Monolithic Operational Software Image:**

.. code-block:: bash

   # Buildroot configuration for monolithic image
   BR2_TARGET_ROOTFS_SQUASHFS=y
   BR2_TARGET_ROOTFS_SQUASHFS_COMPRESSION_XZ=y
   
   # Single signed image containing:
   # - Kernel
   # - Initramfs
   # - Rootfs (read-only squashfs)
   # - All drivers and applications
   
   # Update strategy: atomic full-image replacement
   dd if=system-image-v2.img of=/dev/sda1 bs=4M

Bootloader Development and Customization
=========================================

U-Boot Customization
--------------------

**Custom Commands (Project Examples):**

.. code-block:: c

   // Add custom manufacturing test commands
   int do_nand_test(cmd_tbl_t *cmdtp, int flag, int argc, char * const argv[])
   {
       if (argc < 2) {
           printf("Usage: nand_test <block_num>\n");
           return 1;
       }
       
       int block = simple_strtoul(argv[1], NULL, 10);
       
       // Erase block
       nand_erase_opts_t opts;
       memset(&opts, 0, sizeof(opts));
       opts.offset = block * nand_info->erasesize;
       opts.length = nand_info->erasesize;
       
       if (nand_erase_opts(nand_info, &opts)) {
           printf("Block %d: BAD\n", block);
           return 1;
       }
       
       printf("Block %d: GOOD\n", block);
       return 0;
   }
   
   U_BOOT_CMD(
       nand_test, 2, 0, do_nand_test,
       "Test NAND block",
       "<block_num> - Test specific NAND block"
   );

**NAND Flash BBT Support:**

.. code-block:: c

   // board/custom/board.c
   int board_nand_init(struct nand_chip *nand)
   {
       nand->ecc.mode = NAND_ECC_HW;
       nand->ecc.size = 512;
       nand->ecc.bytes = 10;
       nand->bbt_options = NAND_BBT_USE_FLASH | NAND_BBT_NO_OOB;
       nand->bbt_td = &custom_main_bbt_descr;
       nand->bbt_md = &custom_mirror_bbt_descr;
       
       return 0;
   }

**Environment Variables for DFM (Design For Manufacturing):**

.. code-block:: bash

   # U-Boot DFM test scripts
   setenv mfg_test 'run mem_test; run flash_test; run net_test'
   setenv mem_test 'mtest 0x80000000 0x90000000 1'
   setenv flash_test 'nand scrub -y; nand erase.chip; nand write.jffs2 0x82000000 0 0x1000000'
   setenv net_test 'dhcp; ping ${serverip}'
   saveenv

**Fast Boot Configuration:**

.. code-block:: c

   // include/configs/custom_board.h
   #define CONFIG_BOOTDELAY 0           // No delay
   #define CONFIG_SILENT_CONSOLE        // Suppress console output
   #define CONFIG_SYS_NO_FLASH          // Skip flash detection
   #define CONFIG_SKIP_LOWLEVEL_INIT    // Already done by SPL
   
   // Minimal device init
   #define CONFIG_SKIP_RELOCATION       // Don't relocate U-Boot
   
   // Direct boot command
   #define CONFIG_BOOTCOMMAND \
       "setenv bootargs console=ttyS0,115200 root=/dev/mmcblk0p2 ro;" \
       "ext4load mmc 0:1 0x82000000 uImage;" \
       "ext4load mmc 0:1 0x88000000 dtb;" \
       "bootm 0x82000000 - 0x88000000"

UEFI Development
----------------

**Custom DXE Driver:**

.. code-block:: c

   // Platform initialization driver
   EFI_STATUS
   EFIAPI
   PlatformInitDxeEntry (
       IN EFI_HANDLE        ImageHandle,
       IN EFI_SYSTEM_TABLE  *SystemTable
   )
   {
       EFI_STATUS Status;
       
       // Initialize platform-specific hardware
       Status = InitializePlatformGpio();
       if (EFI_ERROR(Status)) {
           return Status;
       }
       
       // Configure FPGA interfaces
       Status = ConfigureFpgaInterface();
       
       // Setup PCIe root complexes
       Status = InitializeRootComplexes();
       
       return EFI_SUCCESS;
   }

**Secure Boot Policy:**

.. code-block:: c

   // Enforce signature verification
   EFI_STATUS VerifyImageSignature(
       IN VOID   *ImageBuffer,
       IN UINTN  ImageSize
   )
   {
       EFI_STATUS Status;
       UINT8      *SignatureData;
       UINTN      SignatureSize;
       
       // Extract PE/COFF signature
       Status = GetPeCoffSignature(ImageBuffer, ImageSize,
                                   &SignatureData, &SignatureSize);
       
       // Verify against db (signature database)
       Status = VerifySignatureDatabase(SignatureData, SignatureSize);
       
       return Status;
   }

Device Tree Customization
==========================

Project-Specific Device Trees
------------------------------

**i.MX 93 Smart Home Device:**

.. code-block:: dts

   /dts-v1/;
   
   #include "imx93.dtsi"
   
   / {
       model = "Smart Home Hub i.MX93";
       compatible = "fsl,imx93-smart-home", "fsl,imx93";
       
       memory@80000000 {
           device_type = "memory";
           reg = <0x80000000 0x80000000>;  // 2GB LPDDR4
       };
       
       reserved-memory {
           #address-cells = <1>;
           #size-cells = <1>;
           ranges;
           
           // Cortex-M33 firmware
           m33_reserved: m33@a4000000 {
               reg = <0xa4000000 0x1000000>;
               no-map;
           };
           
           // Secure enclave
           optee_reserved: optee@be000000 {
               reg = <0xbe000000 0x02000000>;
               no-map;
           };
       };
       
       leds {
           compatible = "gpio-leds";
           
           status_led: led-status {
               gpios = <&gpio2 13 GPIO_ACTIVE_HIGH>;
               linux,default-trigger = "heartbeat";
           };
       };
       
       regulators {
           compatible = "simple-bus";
           
           reg_wifi_en: regulator-wifi {
               compatible = "regulator-fixed";
               regulator-name = "wifi-en";
               regulator-min-microvolt = <3300000>;
               regulator-max-microvolt = <3300000>;
               gpio = <&gpio1 9 GPIO_ACTIVE_HIGH>;
               enable-active-high;
           };
       };
   };
   
   &usdhc1 {
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_usdhc1>;
       bus-width = <4>;
       cd-gpios = <&gpio2 12 GPIO_ACTIVE_LOW>;
       status = "okay";
   };
   
   &eqos {  // Ethernet
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_eqos>;
       phy-mode = "rgmii";
       phy-handle = <&ethphy0>;
       status = "okay";
       
       mdio {
           #address-cells = <1>;
           #size-cells = <0>;
           
           ethphy0: ethernet-phy@0 {
               compatible = "ethernet-phy-ieee802.3-c22";
               reg = <0>;
           };
       };
   };
   
   &lpuart1 {  // Debug console
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_uart1>;
       status = "okay";
   };
   
   &flexcan1 {  // CAN for IoT gateway
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_flexcan1>;
       status = "okay";
   };

**Intel Atom Avionics Platform:**

.. code-block:: dts

   // ACPI-based system, custom ASL tables
   DefinitionBlock ("platform.aml", "SSDT", 2, "VENDOR", "AVIONIC", 1)
   {
       Scope (\_SB)
       {
           // FPGA device
           Device (FPGA)
           {
               Name (_HID, "ACPI0007")
               Name (_UID, 0)
               
               Method (_STA, 0, NotSerialized)
               {
                   Return (0x0F)  // Present and enabled
               }
               
               Name (_CRS, ResourceTemplate ()
               {
                   Memory32Fixed (ReadWrite, 0xFED00000, 0x00100000)
                   Interrupt (ResourceConsumer, Level, ActiveHigh, Exclusive) { 40 }
               })
           }
           
           // PCIe Root Complex 0
           Device (PCI0)
           {
               Name (_HID, EisaId ("PNP0A08"))
               Name (_CID, EisaId ("PNP0A03"))
               Name (_BBN, 0)
               
               Method (_CRS, 0, Serialized)
               {
                   Name (RBUF, ResourceTemplate ()
                   {
                       WordBusNumber (ResourceProducer, MinFixed, MaxFixed, PosDecode,
                           0x0000, 0x0000, 0x00FF, 0x0000, 0x0100)
                       DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed,
                           Cacheable, ReadWrite,
                           0x00000000, 0x80000000, 0xDFFFFFFF, 0x00000000, 0x60000000)
                   })
                   Return (RBUF)
               }
           }
       }
   }

**Runtime Device Tree Modification:**

.. code-block:: bash

   # U-Boot: Modify device tree before booting kernel
   fdt addr 0x88000000
   fdt resize 8192
   
   # Disable unused peripherals for fast boot
   fdt set /soc/usb@30b10000 status "disabled"
   fdt set /soc/usb@30b20000 status "disabled"
   
   # Set kernel command line
   fdt chosen /chosen
   fdt set /chosen bootargs "console=ttyLP0,115200 root=/dev/mmcblk0p2 ro quiet"
   
   # Boot modified tree
   bootm 0x82000000 - 0x88000000

Secure Boot Implementation
===========================

NXP i.MX HAB (High Assurance Boot)
-----------------------------------

**Complete Secure Boot Setup:**

.. code-block:: bash

   # 1. Generate HAB signing keys (one-time)
   cd cst-3.3.1/keys
   ./hab4_pki_tree.sh
   
   # 2. Create CSF (Command Sequence File) descriptor
   cat > csf_uboot.txt << EOF
   [Header]
   Version = 4.3
   Hash Algorithm = sha256
   Engine Configuration = 0
   Certificate Format = X509
   Signature Format = CMS
   Engine = CAAM
   
   [Install SRK]
   File = "../crts/SRK_1_2_3_4_table.bin"
   Source index = 0
   
   [Install CSFK]
   File = "../crts/CSF1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate CSF]
   
   [Install Key]
   Verification index = 0
   Target index = 2
   File = "../crts/IMG1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate Data]
   Verification index = 2
   Blocks = 0x877ff000 0x0 0x00090000 "u-boot-dtb.imx"
   EOF
   
   # 3. Generate CSF binary
   ./cst --input csf_uboot.txt --output csf_uboot.bin
   
   # 4. Append CSF to U-Boot image
   cat u-boot-dtb.imx csf_uboot.bin > u-boot-signed.imx
   
   # 5. Program SRK hash to eFuse (CAUTION: One-time operation!)
   # Extract SRK hash
   hexdump -e '/4 "0x"' -e '/4 "%08X""\n"' < SRK_1_2_3_4_fuse.bin
   
   # Using i.MX fuse programming tool
   echo "SRK_LOCK = 0x1" > fuse_config.txt
   echo "SRK_HASH[0] = 0xXXXXXXXX" >> fuse_config.txt
   echo "SRK_HASH[1] = 0xXXXXXXXX" >> fuse_config.txt
   # ... (8 words total)
   
   # 6. Enable secure boot (closes device - irreversible!)
   # SEC_CONFIG[1] = 1  (Closed configuration)

**Kernel Image Signing:**

.. code-block:: bash

   # CSF for kernel image
   cat > csf_kernel.txt << EOF
   [Header]
   Version = 4.3
   Hash Algorithm = sha256
   Engine Configuration = 0
   Certificate Format = X509
   Signature Format = CMS
   
   [Install SRK]
   File = "../crts/SRK_1_2_3_4_table.bin"
   Source index = 0
   
   [Install CSFK]
   File = "../crts/CSF1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate CSF]
   
   [Install Key]
   Verification index = 0
   Target index = 2
   File = "../crts/IMG1_1_sha256_4096_65537_v3_usr_crt.pem"
   
   [Authenticate Data]
   Verification index = 2
   Blocks = 0x80800000 0x0 0x00600000 "zImage"
   Blocks = 0x83000000 0x0 0x00010000 "imx93-custom.dtb"
   EOF
   
   # Generate and append CSF
   ./cst --input csf_kernel.txt --output csf_kernel.bin
   objcopy -I binary -O binary --pad-to 0x610000 --gap-fill=0x00 \
           zImage zImage_padded
   cat zImage_padded csf_kernel.bin > zImage_signed

UEFI Secure Boot (Intel Atom Project)
--------------------------------------

**Complete UEFI Secure Boot Chain:**

.. code-block:: bash

   # 1. Generate platform keys
   mkdir -p keys && cd keys
   
   # Platform Key (PK) - Root of trust
   openssl req -new -x509 -newkey rsa:2048 -keyout PK.key \
               -out PK.crt -days 3650 -nodes \
               -subj "/CN=Platform Key for Avionics Platform/"
   
   # Key Exchange Key (KEK) - Intermediary
   openssl req -new -x509 -newkey rsa:2048 -keyout KEK.key \
               -out KEK.crt -days 3650 -nodes \
               -subj "/CN=Key Exchange Key/"
   
   # Database key (db) - Sign binaries
   openssl req -new -x509 -newkey rsa:2048 -keyout db.key \
               -out db.crt -days 3650 -nodes \
               -subj "/CN=Signature Database Key/"
   
   # Convert to DER format
   openssl x509 -in PK.crt -outform DER -out PK.der
   openssl x509 -in KEK.crt -outform DER -out KEK.der
   openssl x509 -in db.crt -outform DER -out db.der
   
   # 2. Create authenticated variables
   cert-to-efi-sig-list -g "$(uuidgen)" PK.crt PK.esl
   sign-efi-sig-list -k PK.key -c PK.crt PK PK.esl PK.auth
   
   cert-to-efi-sig-list -g "$(uuidgen)" KEK.crt KEK.esl
   sign-efi-sig-list -a -k PK.key -c PK.crt KEK KEK.esl KEK.auth
   
   cert-to-efi-sig-list -g "$(uuidgen)" db.crt db.esl
   sign-efi-sig-list -a -k KEK.key -c KEK.crt db db.esl db.auth
   
   # 3. Sign bootloader and kernel
   sbsign --key db.key --cert db.crt --output bootx64.efi.signed bootx64.efi
   sbsign --key db.key --cert db.crt --output vmlinuz.signed vmlinuz
   
   # 4. Sign all kernel modules
   for module in $(find /lib/modules/$(uname -r) -name "*.ko"); do
       /usr/src/kernels/$(uname -r)/scripts/sign-file \
           sha256 db.key db.crt "$module"
   done
   
   # 5. Enroll keys (do this from UEFI shell or Linux with efi-updatevar)
   efi-updatevar -f PK.auth PK
   efi-updatevar -f KEK.auth KEK
   efi-updatevar -f db.auth db

**SELinux Integration (Avionics Project):**

.. code-block:: bash

   # Buildroot SELinux configuration
   BR2_PACKAGE_LIBSELINUX=y
   BR2_PACKAGE_LIBSEMANAGE=y
   BR2_PACKAGE_POLICYCOREUTILS=y
   BR2_PACKAGE_REFPOLICY=y
   
   # Custom SELinux policy for avionics
   policy_module(avionics_platform, 1.0.0)
   
   require {
       type init_t;
       type device_t;
       type kernel_t;
       class file { read write execute };
       class capability { sys_admin sys_rawio };
   }
   
   # Allow platform service to access hardware
   allow avionics_platform_t device_t:file { read write };
   allow avionics_platform_t self:capability { sys_admin sys_rawio };
   
   # Deny network access to safety-critical applications
   neverallow safety_critical_t port_t:tcp_socket name_connect;

SMP and AMP Boot
================

Symmetric Multi-Processing (SMP)
---------------------------------

**CPU Bringup Sequence:**

.. code-block:: c

   // arch/arm64/kernel/smp.c customization
   
   static int custom_boot_secondary(unsigned int cpu, struct task_struct *idle)
   {
       // Platform-specific secondary CPU initialization
       
       // 1. Prepare per-CPU stack
       void *stack = task_stack_page(idle) + THREAD_SIZE;
       
       // 2. Set secondary CPU entry point
       writel(virt_to_phys(secondary_entry), CPU_RELEASE_ADDR(cpu));
       
       // 3. Wake up CPU via IPI or SEV
       sev();  // Send event to wake WFE
       
       // 4. Wait for CPU to come online
       while (!cpu_online(cpu))
           cpu_relax();
       
       return 0;
   }
   
   // Secondary CPU entry
   asmlinkage void secondary_entry(void)
   {
       // Enable MMU
       cpu_switch_mm(mm->pgd, mm);
       
       // Initialize GIC CPU interface
       gic_cpu_init();
       
       // Enable interrupts
       local_irq_enable();
       
       // Signal completion
       set_cpu_online(smp_processor_id(), true);
       
       // Enter idle loop
       cpu_startup_entry(CPUHP_AP_ONLINE_IDLE);
   }

**Device Tree Configuration:**

.. code-block:: dts

   cpus {
       #address-cells = <1>;
       #size-cells = <0>;
       
       cpu0: cpu@0 {
           device_type = "cpu";
           compatible = "arm,cortex-a55";
           reg = <0x0>;
           enable-method = "psci";
           clocks = <&clk IMX93_CLK_A55>;
           operating-points-v2 = <&a55_opp_table>;
       };
       
       cpu1: cpu@100 {
           device_type = "cpu";
           compatible = "arm,cortex-a55";
           reg = <0x100>;
           enable-method = "psci";
           clocks = <&clk IMX93_CLK_A55>;
           operating-points-v2 = <&a55_opp_table>;
       };
   };
   
   psci {
       compatible = "arm,psci-1.0";
       method = "smc";
   };

Asymmetric Multi-Processing (AMP)
----------------------------------

**i.MX 93: Cortex-A55 + Cortex-M33 (Project Implementation):**

.. code-block:: c

   // Cortex-A55 (Linux) side - RemoteProc framework
   
   // drivers/remoteproc/imx_rproc.c
   static int imx_rproc_start(struct rproc *rproc)
   {
       struct imx_rproc *priv = rproc->priv;
       
       // 1. Load firmware to M33 TCM
       ret = imx_rproc_elf_load_segments(rproc, rproc->firmware);
       
       // 2. Configure M33 clock and power
       clk_prepare_enable(priv->clk);
       
       // 3. Release M33 from reset
       regmap_update_bits(priv->regmap, IMX93_SRC_M33_RCR,
                          SRC_M33_ENABLE, SRC_M33_ENABLE);
       
       // 4. Setup RPMsg virtio communication
       ret = rproc_boot(rproc);
       
       return ret;
   }
   
   // Device tree binding
   remoteproc_m33: remoteproc@a4000000 {
       compatible = "fsl,imx93-cm33";
       reg = <0xa4000000 0x40000>;  // TCM
       clocks = <&clk IMX93_CLK_M33>;
       mbox-names = "tx", "rx", "rxdb";
       mboxes = <&mu1 0 1
                 &mu1 1 1
                 &mu1 3 1>;
       memory-region = <&vdevbuffer>, <&vdev0vring0>, <&vdev0vring1>;
       firmware-name = "imx93_m33_sensor_fusion.elf";
   };
   
   // RPMsg communication channel
   reserved-memory {
       rpmsg_reserved: rpmsg@a4300000 {
           reg = <0xa4300000 0x10000>;
           no-map;
       };
       
       vdevbuffer: vdevbuffer@a4310000 {
           compatible = "shared-dma-pool";
           reg = <0xa4310000 0x10000>;
           no-map;
       };
   };

**Cortex-M33 Firmware (FreeRTOS):**

.. code-block:: c

   // M33 side - Real-time sensor processing
   #include "rpmsg_lite.h"
   #include "rpmsg_queue.h"
   #include "rpmsg_ns.h"
   
   #define RPMSG_LITE_LINK_ID    (0)
   #define RPMSG_LITE_SHMEM_BASE (0xA4300000)
   #define LOCAL_EPT_ADDR        (30)
   
   struct rpmsg_lite_instance *rpmsg_instance;
   struct rpmsg_lite_endpoint *ept;
   rpmsg_queue_handle queue;
   
   void rpmsg_init(void)
   {
       // Initialize RPMsg-Lite
       rpmsg_instance = rpmsg_lite_remote_init(
           (void *)RPMSG_LITE_SHMEM_BASE,
           RPMSG_LITE_LINK_ID,
           RL_NO_FLAGS
       );
       
       // Create endpoint
       queue = rpmsg_queue_create(rpmsg_instance);
       ept = rpmsg_lite_create_ept(rpmsg_instance, LOCAL_EPT_ADDR,
                                    rpmsg_queue_rx_cb, queue);
       
       // Announce service
       rpmsg_ns_announce(rpmsg_instance, ept, "sensor_fusion", 0);
   }
   
   void sensor_processing_task(void *param)
   {
       char buffer[512];
       uint32_t len;
       uint32_t src_addr;
       
       while (1) {
           // Receive data from Linux side
           rpmsg_queue_recv(rpmsg_instance, queue,
                           &src_addr, buffer, sizeof(buffer),
                           &len, RL_BLOCK);
           
           // Process sensor data (real-time critical)
           process_sensor_data(buffer, len);
           
           // Send results back to Linux
           rpmsg_lite_send(rpmsg_instance, ept, src_addr,
                          buffer, len, RL_BLOCK);
       }
   }

**Inter-Processor Communication Performance:**

.. code-block:: c

   // Measured latency on i.MX 93
   // A55 → M33: ~10μs
   // M33 → A55: ~8μs
   // Throughput: ~50 MB/s
   
   // Optimization: Zero-copy shared memory
   struct shared_buffer {
       volatile uint32_t write_idx;
       volatile uint32_t read_idx;
       uint8_t data[4096];
   } __attribute__((aligned(64)));  // Cache line aligned
   
   // Place in non-cached memory region
   struct shared_buffer *shm = (struct shared_buffer *)0xA4320000;

Boot Time Optimization
======================

Analysis and Measurement
-------------------------

**Bootchart Integration:**

.. code-block:: bash

   # Add to kernel command line
   initcall_debug printk.time=y quiet
   
   # Grab bootchart
   grabserial -d /dev/ttyUSB0 -b 115200 -e 30 -t -o boot.log
   
   # Alternative: systemd-analyze
   systemd-analyze
   systemd-analyze blame
   systemd-analyze critical-chain

**Kernel Boot Time Breakdown:**

.. code-block:: bash

   # Add timestamps to kernel
   CONFIG_PRINTK_TIME=y
   CONFIG_INITCALL_DEBUG=y
   
   # Parse dmesg for timing
   dmesg | grep "initcall" | awk '{print $2, $3, $5}' | sort -k3 -n

Optimization Techniques (Project Results)
-----------------------------------------

**1. Bootloader Optimization (U-Boot):**

.. code-block:: c

   // Parallel initialization
   #define CONFIG_BOOTDELAY 0
   #define CONFIG_ZERO_BOOTDELAY_CHECK
   #define CONFIG_SILENT_CONSOLE
   
   // Skip unnecessary hardware probing
   #define CONFIG_SYS_NO_FLASH
   #define CONFIG_ENV_IS_NOWHERE
   
   // Direct kernel boot
   #define CONFIG_BOOTCOMMAND \
       "ext4load mmc 0:1 $loadaddr uImage;" \
       "ext4load mmc 0:1 $fdtaddr dtb;" \
       "bootm $loadaddr - $fdtaddr"
   
   // Result: U-Boot time reduced from 3.2s → 0.8s

**2. Kernel Configuration:**

.. code-block:: bash

   # Minimize kernel size
   CONFIG_KERNEL_XZ=y                    # Best compression
   CONFIG_CC_OPTIMIZE_FOR_SIZE=y         # -Os optimization
   CONFIG_SLOB=y                         # Simple allocator
   
   # Disable debugging
   # CONFIG_DEBUG_KERNEL is not set
   # CONFIG_KALLSYMS is not set
   # CONFIG_PRINTK is not set              # Production only!
   
   # Async probing for slow devices
   CONFIG_USB_STORAGE_ASYNC_PROBE=y
   
   # Built-in drivers (no module loading)
   CONFIG_MMC=y                          # Not =m
   CONFIG_EXT4_FS=y
   
   # Result: Kernel boot time 2.8s → 1.4s

**3. Init System Optimization:**

.. code-block:: bash
   
   # BusyBox init (minimal)
   CONFIG_FEATURE_USE_INITTAB=y
   
   # /etc/inittab
   ::sysinit:/etc/init.d/rcS
   ::respawn:/sbin/getty 115200 console
   ::shutdown:/bin/umount -a -r
   
   # /etc/init.d/rcS - Parallel startup
   #!/bin/sh
   mount -t proc proc /proc &
   mount -t sysfs sysfs /sys &
   mount -t devtmpfs devtmpfs /dev &
   wait
   
   # Start only essential services
   /usr/sbin/telnetd -l /bin/sh &
   /usr/sbin/application &
   
   # Result: Init time 1.5s → 0.3s

**4. Filesystem Selection:**

+-------------+------------+-----------+-----------+
| Filesystem  | Boot Time  | Read Perf | Use Case  |
+=============+============+===========+===========+
| ext4        | Baseline   | Good      | Development |
| squashfs+xz | -30%       | Excellent | Production |
| initramfs   | -60%       | Best      | Embedded  |
+-------------+------------+-----------+-----------+

.. code-block:: bash

   # Initramfs (fastest boot)
   CONFIG_BLK_DEV_INITRD=y
   CONFIG_INITRAMFS_SOURCE="rootfs.cpio.xz"
   CONFIG_INITRAMFS_COMPRESSION_XZ=y
   
   # Result: Eliminates rootfs mount time (~0.5s saved)

**5. Deferred Initialization:**

.. code-block:: c

   // Mark non-critical drivers for deferred probe
   static struct platform_driver wifi_driver = {
       .probe = wifi_probe,
       .driver = {
           .name = "wifi-driver",
           .probe_type = PROBE_PREFER_ASYNCHRONOUS,
       },
   };
   
   // Or use late_initcall for non-essential drivers
   late_initcall(wifi_driver_init);

**Project Results Summary:**

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30
   
   * - Platform
     - Before
     - After
     - Key Optimizations
   * - i.MX 93 Smart Home
     - 6.2s
     - 1.8s
     - Parallel init, initramfs, async probe
   * - TI DaVinci DM365
     - 8.5s
     - 5.8s
     - U-Boot optimization, built-in drivers
   * - Intel Atom Avionics
     - 12.1s
     - 9.2s
     - UEFI optimization, systemd tuning

Hibernation and Fast Resume
----------------------------

**DaVinci Project: <2s Resume from <8mW Sleep:**

.. code-block:: c

   // Custom hibernation implementation
   #include <linux/suspend.h>
   #include <linux/rtc.h>
   
   // Save critical state to RTC SRAM (battery-backed)
   struct hibernate_context {
       uint32_t magic;
       void *resume_address;
       uint32_t saved_registers[32];
       uint32_t ddr_config[16];
   } __attribute__((packed));
   
   static int davinci_hibernate_enter(void)
   {
       struct hibernate_context *ctx = 
           (struct hibernate_context *)RTC_SRAM_BASE;
       
       // Save context
       ctx->magic = 0xDEADBEEF;
       ctx->resume_address = virt_to_phys(davinci_resume_entry);
       save_cpu_regs(ctx->saved_registers);
       save_ddr_config(ctx->ddr_config);
       
       // Power down peripherals
       davinci_psc_config(DAVINCI_LPSC_USB, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_EMAC, 0, PSC_SWRSTDISABLE);
       davinci_psc_config(DAVINCI_LPSC_VPSS, 0, PSC_SWRSTDISABLE);
       
       // Enter deep sleep (WFI)
       cpu_suspend(0, davinci_finish_suspend);
       
       // Execution resumes here after wakeup
       restore_peripherals();
       
       return 0;
   }
   
   // Boot ROM checks RTC SRAM for magic value
   // If found, jumps to resume_address instead of normal boot

Debug and Troubleshooting
==========================

Early Boot Debug
----------------

**JTAG/Serial Console:**

.. code-block:: bash

   # Kernel early printk
   CONFIG_EARLY_PRINTK=y
   CONFIG_EARLY_PRINTK_DBGP=y
   
   # Kernel command line
   earlycon=uart8250,mmio32,0x30860000 earlyprintk
   
   # U-Boot debug
   setenv bootargs "${bootargs} loglevel=8 debug"

**Common Boot Failures:**

.. code-block:: text

   Symptom: "Uncompressing Linux... done, booting the kernel"
   Cause: Wrong kernel load address or device tree
   Fix: Check U-Boot bootm addresses don't overlap
        Verify device tree compatible string
   
   Symptom: "Kernel panic - not syncing: VFS: Unable to mount root"
   Cause: Wrong root device or missing filesystem driver
   Fix: Check root= parameter
        Ensure filesystem compiled in (not module)
        Verify partition layout with printk in kernel
   
   Symptom: System hangs after "Starting kernel..."
   Cause: Device tree mismatch, missing console
   Fix: Add earlycon to cmdline
        Verify UART node in device tree
        Check pinmux configuration
   
   Symptom: Secure boot failure
   Cause: Signature mismatch, unsigned image
   Fix: Verify CSF appended correctly
        Check SRK hash matches eFuse
        Ensure keys not revoked

**Boot Trace Collection:**

.. code-block:: bash

   # ftrace for boot analysis
   trace_event=initcall:* tp_printk
   
   # After boot:
   cat /sys/kernel/debug/tracing/trace > boot_trace.txt

Best Practices
==============

General Guidelines
------------------

1. **Always maintain recovery mechanism**
   - Dual bank firmware
   - Serial console access
   - JTAG/SWD interface

2. **Document boot sequence**
   - Memory maps
   - Device tree bindings
   - Custom configurations

3. **Version control**
   - Track bootloader, kernel, device tree together
   - Tag stable configurations

4. **Testing**
   - Cold boot tests
   - Warm reboot tests
   - Power cycle stress tests
   - Secure boot verification

5. **Performance monitoring**
   - Measure each boot stage
   - Set targets for optimization
   - Track regression

Project-Specific Lessons
-------------------------

- **i.MX 93 Smart Home**: Prioritized security (HAB) while maintaining fast boot (<2s)
- **Intel Atom Avionics**: UEFI secure boot with monolithic image for field updates
- **TI DaVinci**: Power optimization critical; hibernation saves significant battery
- **Multiple platforms**: Device tree mastery essential for BSP portability

References
==========

- NXP i.MX 93 Reference Manual
- U-Boot Documentation: https://u-boot.readthedocs.io
- Linux Kernel Boot Process: Documentation/x86/boot.rst
- UEFI Specification 2.10
- Device Tree Specification v0.4
- HAB4 API Documentation (NXP Secure Boot)

