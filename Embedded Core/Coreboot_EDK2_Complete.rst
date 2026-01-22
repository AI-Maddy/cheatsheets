===============================================
Coreboot & UEFI EDK2 Firmware Development
===============================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 4
   :local:
   :backlinks: top

🎯 Overview
============

Comparison
----------

+------------------------+----------------------------------+----------------------------------+
| **Feature**            | **Coreboot**                     | **UEFI EDK2**                    |
+========================+==================================+==================================+
| Philosophy             | Minimal, fast, open firmware     | Full-featured UEFI implementation|
+------------------------+----------------------------------+----------------------------------+
| Boot Time              | Very fast (<1 second)            | Moderate (2-5 seconds)           |
+------------------------+----------------------------------+----------------------------------+
| Code Size              | Small (~100KB core)              | Large (several MB)               |
+------------------------+----------------------------------+----------------------------------+
| Architecture           | x86, ARM, RISC-V, PowerPC        | x86, ARM, RISC-V                 |
+------------------------+----------------------------------+----------------------------------+
| Payloads               | SeaBIOS, GRUB, Linux, UEFI       | Direct OS boot                   |
+------------------------+----------------------------------+----------------------------------+
| Development            | C, Assembly                      | C, Assembly                      |
+------------------------+----------------------------------+----------------------------------+
| Use Cases              | Embedded, IoT, ChromeOS          | Servers, desktops, UEFI standard |
+------------------------+----------------------------------+----------------------------------+

Boot Stages
-----------

**Coreboot:**

.. code-block:: text

   1. Bootblock       → Minimal CPU init
   2. Verstage        → Verified boot (optional)
   3. Romstage        → RAM initialization
   4. Ramstage        → Device initialization
   5. Payload         → OS bootloader or kernel

**UEFI EDK2:**

.. code-block:: text

   1. SEC (Security)  → CPU/platform init
   2. PEI (Pre-EFI)   → Memory init, early drivers
   3. DXE (Driver Execution) → Full driver model
   4. BDS (Boot Device Selection) → Boot manager
   5. RT (Runtime)    → OS runtime services

🔧 Coreboot Development
========================

Build Environment Setup
-----------------------

.. code-block:: bash

   # Install dependencies (Debian/Ubuntu)
   sudo apt install git build-essential gnat flex bison libncurses5-dev \
       libssl-dev libelf-dev zlib1g-dev python3 python3-distutils wget
   
   # Clone coreboot
   git clone https://review.coreboot.org/coreboot
   cd coreboot
   
   # Update submodules
   git submodule update --init --recursive
   
   # Build toolchain (ARM example)
   make crossgcc-arm
   
   # For x86
   make crossgcc-i386 CPUS=$(nproc)
   
   # For all architectures
   make crossgcc

Configuration
-------------

.. code-block:: bash

   # Interactive configuration
   make menuconfig
   
   # Select:
   # - Mainboard vendor and model
   # - Payload (SeaBIOS, GRUB2, Linux, Tianocore)
   # - Chipset options
   # - Console output (Serial, USB, etc.)
   
   # Save configuration (.config file)
   
   # Load existing config
   make defconfig
   
   # Specific board config
   make menuconfig BOARD=qemu-x86

Build Coreboot
--------------

.. code-block:: bash

   # Full build
   make -j$(nproc)
   
   # Output: build/coreboot.rom
   
   # Verbose build
   make V=1
   
   # Clean build
   make clean
   make distclean  # Including toolchain

Flash Coreboot
--------------

**Internal Flashing (from running system):**

.. code-block:: bash

   # Install flashrom
   sudo apt install flashrom
   
   # Read current ROM
   sudo flashrom -p internal -r backup.rom
   
   # Flash new ROM
   sudo flashrom -p internal -w build/coreboot.rom
   
   # Verify
   sudo flashrom -p internal -v build/coreboot.rom

**External Flashing (via programmer):**

.. code-block:: bash

   # Using CH341A programmer
   sudo flashrom -p ch341a_spi -r backup.rom
   sudo flashrom -p ch341a_spi -w coreboot.rom
   
   # Using Raspberry Pi
   sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=512 -w coreboot.rom

Testing with QEMU
-----------------

.. code-block:: bash

   # Build for QEMU
   make menuconfig
   # Select: Mainboard → Emulation → QEMU x86
   make -j$(nproc)
   
   # Run in QEMU
   qemu-system-x86_64 -bios build/coreboot.rom -serial stdio -m 1024
   
   # With network
   qemu-system-x86_64 -bios build/coreboot.rom -serial stdio \
       -netdev user,id=net0 -device e1000,netdev=net0

Coreboot Directory Structure
-----------------------------

.. code-block:: text

   coreboot/
   ├── src/
   │   ├── arch/          # Architecture-specific code
   │   ├── cpu/           # CPU support
   │   ├── device/        # Device framework
   │   ├── drivers/       # Device drivers
   │   ├── ec/            # Embedded Controller
   │   ├── mainboard/     # Board support
   │   ├── northbridge/   # Northbridge/memory controller
   │   ├── southbridge/   # Southbridge/PCH
   │   ├── security/      # Verified boot, TPM
   │   └── soc/           # System-on-Chip support
   ├── payloads/          # Payload options
   ├── util/              # Utilities
   │   ├── cbfstool/      # Firmware image tool
   │   ├── ifdtool/       # Intel Flash Descriptor tool
   │   └── nvramtool/     # CMOS/NVRAM tool
   └── Documentation/

Custom Board Support
--------------------

**Create New Board:**

.. code-block:: bash

   # Copy similar board as template
   cp -r src/mainboard/vendor/similar_board src/mainboard/myvendor/myboard
   
   # Edit files
   cd src/mainboard/myvendor/myboard

**mainboard/myvendor/myboard/Kconfig:**

.. code-block:: kconfig

   if BOARD_MYVENDOR_MYBOARD
   
   config BOARD_SPECIFIC_OPTIONS
       def_bool y
       select CPU_INTEL_HASWELL
       select NORTHBRIDGE_INTEL_HASWELL
       select SOUTHBRIDGE_INTEL_LYNXPOINT
       select BOARD_ROMSIZE_KB_8192
       select HAVE_ACPI_TABLES
       select HAVE_OPTION_TABLE
       select HAVE_SMI_HANDLER
       select SUPERIO_ITE_IT8728F
   
   config MAINBOARD_DIR
       string
       default "myvendor/myboard"
   
   config MAINBOARD_PART_NUMBER
       string
       default "My Board"
   
   config MAX_CPUS
       int
       default 8
   
   config DRAM_SIZE_MB
       int
       default 8192
   
   endif

**mainboard/myvendor/myboard/devicetree.cb:**

.. code-block:: text

   chip northbridge/intel/haswell
       device cpu_cluster 0 on
           chip cpu/intel/haswell
               device lapic 0 on end
           end
       end
       
       device domain 0 on
           device pci 00.0 on end  # Host bridge
           device pci 02.0 on end  # Graphics
           device pci 03.0 on end  # Mini-HD Audio
           
           chip southbridge/intel/lynxpoint
               device pci 14.0 on end  # USB 3.0
               device pci 16.0 on end  # MEI
               device pci 1a.0 on end  # USB 2.0
               device pci 1b.0 on end  # HD Audio
               device pci 1c.0 on end  # PCIe Port 1
               device pci 1f.0 on      # LPC bridge
                   chip superio/ite/it8728f
                       device pnp 2e.0 on end  # FDC
                       device pnp 2e.1 on      # Serial Port 1
                           io 0x60 = 0x3f8
                           irq 0x70 = 4
                       end
                   end
               end
               device pci 1f.2 on end  # SATA (AHCI)
               device pci 1f.3 on end  # SMBus
           end
       end
   end

**mainboard/myvendor/myboard/romstage.c:**

.. code-block:: c

   #include <stdint.h>
   #include <device/pci_def.h>
   #include <northbridge/intel/haswell/raminit.h>
   #include <southbridge/intel/lynxpoint/pch.h>
   
   void mainboard_romstage_entry(void)
   {
       /* Enable serial console */
       pch_enable_lpc();
       
       /* Initialize RAM */
       struct pei_data pei_data = {
           .pei_version = PEI_VERSION,
           .mchbar = DEFAULT_MCHBAR,
           .dmibar = DEFAULT_DMIBAR,
           .epbar = DEFAULT_EPBAR,
           .pciexbar = DEFAULT_PCIEXBAR,
           .smbusbar = SMBUS_IO_BASE,
           .wdbbar = 0x4000000,
           .wdbsize = 0x1000,
           .hpet_address = HPET_ADDR,
           .rcba = DEFAULT_RCBA,
           .pmbase = DEFAULT_PMBASE,
           .gpiobase = DEFAULT_GPIOBASE,
           .temp_mmio_base = 0xfed08000,
           .system_type = 0, /* Desktop */
           .tseg_size = CONFIG_SMM_TSEG_SIZE,
           .spd_addresses = { 0xa0, 0xa2, 0xa4, 0xa6 },
           .max_ddr3_freq = 1600,
           .usb_port_config = {
               /* USB port config here */
           },
       };
       
       /* Call MRC (Memory Reference Code) */
       sdram_initialize(&pei_data);
   }

Payloads
--------

**SeaBIOS (Legacy BIOS):**

.. code-block:: bash

   # In menuconfig:
   # Payload → Add a payload → SeaBIOS
   # Payload → SeaBIOS version → master
   
   # Build
   make -j$(nproc)

**GRUB2:**

.. code-block:: bash

   # Payload → Add a payload → GRUB2
   # Configure GRUB options
   
   # Custom GRUB config
   # Create: payloads/external/GRUB2/grub2/grub.cfg

**Linux Kernel as Payload:**

.. code-block:: bash

   # Build minimal kernel
   cd /path/to/linux
   make tinyconfig
   make menuconfig  # Enable required drivers
   make bzImage -j$(nproc)
   
   # In coreboot menuconfig:
   # Payload → Add a payload → Linux
   # Payload → Linux path and filename → /path/to/linux/arch/x86/boot/bzImage
   # Payload → Linux command line → "console=ttyS0,115200"

**Tianocore (UEFI):**

.. code-block:: bash

   # Payload → Add a payload → Tianocore
   # Select UEFI version
   
   # Build
   make -j$(nproc)

CBFS Tool
---------

.. code-block:: bash

   # List contents
   ./util/cbfstool/cbfstool build/coreboot.rom print
   
   # Add file
   ./util/cbfstool/cbfstool build/coreboot.rom add \
       -f myfile.bin -n myfile -t raw
   
   # Extract file
   ./util/cbfstool/cbfstool build/coreboot.rom extract \
       -n fallback/payload -f payload.elf
   
   # Remove file
   ./util/cbfstool/cbfstool build/coreboot.rom remove -n myfile
   
   # Add bootlogo
   ./util/cbfstool/cbfstool build/coreboot.rom add \
       -f logo.bmp -n bootsplash.bmp -t bootsplash

Debugging
---------

.. code-block:: bash

   # Enable debug output in menuconfig
   # Console → Enable "Serial console output"
   # Console → Console log level → Debug
   
   # View serial output
   screen /dev/ttyUSB0 115200
   
   # QEMU with debugging
   qemu-system-x86_64 -bios build/coreboot.rom -serial stdio -d int,cpu_reset
   
   # GDB debugging
   qemu-system-x86_64 -bios build/coreboot.rom -s -S &
   gdb build/cbfs/fallback/romstage.debug
   (gdb) target remote :1234
   (gdb) break bootblock_main
   (gdb) continue

🏗️ UEFI EDK2 Development
==========================

Build Environment Setup
-----------------------

.. code-block:: bash

   # Install dependencies (Ubuntu/Debian)
   sudo apt install build-essential uuid-dev iasl git nasm python3 python3-distutils
   
   # Clone EDK2
   git clone https://github.com/tianocore/edk2.git
   cd edk2
   git submodule update --init
   
   # Setup build environment
   make -C BaseTools
   source edksetup.sh
   
   # Or for BaseTools rebuild
   source edksetup.sh BaseTools

EDK2 Directory Structure
-------------------------

.. code-block:: text

   edk2/
   ├── BaseTools/         # Build tools
   ├── Conf/              # Build configuration
   ├── CryptoPkg/         # Cryptography services
   ├── MdePkg/            # Core UEFI definitions
   ├── MdeModulePkg/      # Core modules
   ├── NetworkPkg/        # Network stack
   ├── OvmfPkg/           # QEMU virtual platform
   ├── ShellPkg/          # UEFI Shell
   ├── SecurityPkg/       # Secure Boot, TPM
   ├── UefiCpuPkg/        # CPU-specific drivers
   └── EmulatorPkg/       # Software emulation

Build EDK2 for QEMU
-------------------

.. code-block:: bash

   # Set target architecture
   export ARCH=X64
   
   # Build OVMF (QEMU virtual firmware)
   build -a X64 -t GCC5 -p OvmfPkg/OvmfPkgX64.dsc
   
   # Output: Build/OvmfX64/DEBUG_GCC5/FV/OVMF.fd
   
   # Test with QEMU
   qemu-system-x86_64 -bios Build/OvmfX64/DEBUG_GCC5/FV/OVMF.fd \
       -drive file=disk.img,format=raw -m 2048

Build Configuration
-------------------

**Conf/target.txt:**

.. code-block:: ini

   # Active platform
   ACTIVE_PLATFORM       = OvmfPkg/OvmfPkgX64.dsc
   
   # Target architecture
   TARGET_ARCH           = X64
   
   # Build target
   TARGET                = DEBUG
   # Options: RELEASE, DEBUG, NOOPT
   
   # Toolchain
   TOOL_CHAIN_TAG        = GCC5
   
   # Number of threads
   MAX_CONCURRENT_THREAD_NUMBER = 8

Platform Description (.dsc)
----------------------------

**Example: MyPlatformPkg/MyPlatform.dsc**

.. code-block:: ini

   [Defines]
     PLATFORM_NAME           = MyPlatform
     PLATFORM_GUID           = 12345678-1234-1234-1234-123456789012
     PLATFORM_VERSION        = 0.1
     DSC_SPECIFICATION       = 0x00010005
     OUTPUT_DIRECTORY        = Build/MyPlatform
     SUPPORTED_ARCHITECTURES = X64
     BUILD_TARGETS           = DEBUG|RELEASE
     SKUID_IDENTIFIER        = DEFAULT
   
   [LibraryClasses]
     # Core libraries
     UefiApplicationEntryPoint|MdePkg/Library/UefiApplicationEntryPoint/UefiApplicationEntryPoint.inf
     UefiBootServicesTableLib|MdePkg/Library/UefiBootServicesTableLib/UefiBootServicesTableLib.inf
     UefiRuntimeServicesTableLib|MdePkg/Library/UefiRuntimeServicesTableLib/UefiRuntimeServicesTableLib.inf
     BaseLib|MdePkg/Library/BaseLib/BaseLib.inf
     BaseMemoryLib|MdePkg/Library/BaseMemoryLib/BaseMemoryLib.inf
     DebugLib|MdePkg/Library/BaseDebugLibSerialPort/BaseDebugLibSerialPort.inf
     PrintLib|MdePkg/Library/BasePrintLib/BasePrintLib.inf
   
   [Components]
     # SEC Phase
     UefiCpuPkg/SecCore/SecCore.inf
     
     # PEI Phase
     MdeModulePkg/Core/Pei/PeiMain.inf
     
     # DXE Phase
     MdeModulePkg/Core/Dxe/DxeMain.inf
     MdeModulePkg/Universal/PCD/Dxe/Pcd.inf
     
     # BDS
     MdeModulePkg/Universal/BdsDxe/BdsDxe.inf

Flash Description (.fdf)
-------------------------

**MyPlatformPkg/MyPlatform.fdf:**

.. code-block:: ini

   [FD.MyPlatform]
   BaseAddress   = 0xFFC00000
   Size          = 0x00400000
   ErasePolarity = 1
   
   # SEC
   0x00000000|0x00010000
   FILE = $(OUTPUT_DIRECTORY)/$(TARGET)_$(TOOL_CHAIN_TAG)/X64/SecCore.efi
   
   # PEI Core & Modules
   0x00010000|0x00050000
   INF MdeModulePkg/Core/Pei/PeiMain.inf
   
   # DXE Core & Drivers
   0x00060000|0x00200000
   INF MdeModulePkg/Core/Dxe/DxeMain.inf
   INF MdeModulePkg/Universal/PCD/Dxe/Pcd.inf
   
   # UEFI Shell
   0x00260000|0x00100000
   INF ShellPkg/Application/Shell/Shell.inf

Module Development (.inf)
--------------------------

**Create UEFI Application:**

.. code-block:: ini

   # MyPlatformPkg/Application/HelloWorld/HelloWorld.inf
   [Defines]
     INF_VERSION                    = 0x00010005
     BASE_NAME                      = HelloWorld
     FILE_GUID                      = 12345678-1234-1234-1234-123456789ABC
     MODULE_TYPE                    = UEFI_APPLICATION
     VERSION_STRING                 = 1.0
     ENTRY_POINT                    = UefiMain
   
   [Sources]
     HelloWorld.c
   
   [Packages]
     MdePkg/MdePkg.dec
   
   [LibraryClasses]
     UefiApplicationEntryPoint
     UefiLib
     DebugLib

**HelloWorld.c:**

.. code-block:: c

   #include <Uefi.h>
   #include <Library/UefiLib.h>
   #include <Library/UefiApplicationEntryPoint.h>
   
   EFI_STATUS
   EFIAPI
   UefiMain (
     IN EFI_HANDLE        ImageHandle,
     IN EFI_SYSTEM_TABLE  *SystemTable
     )
   {
     Print(L"Hello, UEFI World!\n");
     return EFI_SUCCESS;
   }

**Build and Run:**

.. code-block:: bash

   # Add to .dsc [Components] section:
   # MyPlatformPkg/Application/HelloWorld/HelloWorld.inf
   
   # Build
   build -a X64 -t GCC5 -p MyPlatformPkg/MyPlatform.dsc
   
   # Copy to EFI partition
   cp Build/MyPlatform/DEBUG_GCC5/X64/HelloWorld.efi /boot/efi/
   
   # Run from UEFI Shell
   fs0:
   HelloWorld.efi

UEFI Driver Development
------------------------

**Simple DXE Driver:**

.. code-block:: c

   #include <Uefi.h>
   #include <Library/UefiDriverEntryPoint.h>
   #include <Library/DebugLib.h>
   #include <Protocol/DriverBinding.h>
   
   EFI_STATUS
   EFIAPI
   MyDriverSupported (
     IN EFI_DRIVER_BINDING_PROTOCOL  *This,
     IN EFI_HANDLE                   ControllerHandle,
     IN EFI_DEVICE_PATH_PROTOCOL     *RemainingDevicePath OPTIONAL
     )
   {
     DEBUG ((DEBUG_INFO, "MyDriver: Supported check\n"));
     return EFI_SUCCESS;
   }
   
   EFI_STATUS
   EFIAPI
   MyDriverStart (
     IN EFI_DRIVER_BINDING_PROTOCOL  *This,
     IN EFI_HANDLE                   ControllerHandle,
     IN EFI_DEVICE_PATH_PROTOCOL     *RemainingDevicePath OPTIONAL
     )
   {
     DEBUG ((DEBUG_INFO, "MyDriver: Starting\n"));
     // Initialize hardware, install protocols
     return EFI_SUCCESS;
   }
   
   EFI_STATUS
   EFIAPI
   MyDriverStop (
     IN EFI_DRIVER_BINDING_PROTOCOL  *This,
     IN EFI_HANDLE                   ControllerHandle,
     IN UINTN                        NumberOfChildren,
     IN EFI_HANDLE                   *ChildHandleBuffer
     )
   {
     DEBUG ((DEBUG_INFO, "MyDriver: Stopping\n"));
     return EFI_SUCCESS;
   }
   
   EFI_DRIVER_BINDING_PROTOCOL gMyDriverBinding = {
     MyDriverSupported,
     MyDriverStart,
     MyDriverStop,
     0x10,  // Version
     NULL,  // ImageHandle (set in entry point)
     NULL   // DriverBindingHandle (set in entry point)
   };
   
   EFI_STATUS
   EFIAPI
   MyDriverEntry (
     IN EFI_HANDLE        ImageHandle,
     IN EFI_SYSTEM_TABLE  *SystemTable
     )
   {
     EFI_STATUS Status;
     
     gMyDriverBinding.ImageHandle = ImageHandle;
     gMyDriverBinding.DriverBindingHandle = ImageHandle;
     
     Status = gBS->InstallMultipleProtocolInterfaces (
                     &gMyDriverBinding.DriverBindingHandle,
                     &gEfiDriverBindingProtocolGuid,
                     &gMyDriverBinding,
                     NULL
                     );
     
     return Status;
   }

UEFI Protocols
--------------

**Common Protocols:**

.. code-block:: c

   // Simple Text Output
   EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL *ConOut = SystemTable->ConOut;
   ConOut->OutputString(ConOut, L"Hello!\n");
   
   // Block I/O (disk access)
   EFI_BLOCK_IO_PROTOCOL *BlockIo;
   Status = gBS->HandleProtocol(
       Handle,
       &gEfiBlockIoProtocolGuid,
       (VOID**)&BlockIo
   );
   
   // File System
   EFI_SIMPLE_FILE_SYSTEM_PROTOCOL *FileSystem;
   EFI_FILE_PROTOCOL *Root;
   Status = gBS->HandleProtocol(
       Handle,
       &gEfiSimpleFileSystemProtocolGuid,
       (VOID**)&FileSystem
   );
   FileSystem->OpenVolume(FileSystem, &Root);
   
   // Graphics Output
   EFI_GRAPHICS_OUTPUT_PROTOCOL *GraphicsOutput;
   Status = gBS->LocateProtocol(
       &gEfiGraphicsOutputProtocolGuid,
       NULL,
       (VOID**)&GraphicsOutput
   );

Debugging EDK2
--------------

.. code-block:: bash

   # Enable debug output
   # In .dsc file [PcdsFixedAtBuild]:
   gEfiMdePkgTokenSpaceGuid.PcdDebugPropertyMask|0xFF
   gEfiMdePkgTokenSpaceGuid.PcdDebugPrintErrorLevel|0x80000047
   
   # Use DEBUG macro in code
   DEBUG ((DEBUG_INFO, "Message: %d\n", value));
   
   # QEMU with debug console
   qemu-system-x86_64 -bios OVMF.fd -serial stdio -debugcon file:debug.log -global isa-debugcon.iobase=0x402
   
   # View debug output
   tail -f debug.log

🔬 Advanced Topics
===================

Coreboot Verified Boot (vboot)
-------------------------------

.. code-block:: bash

   # Enable in menuconfig
   # Security → Verified Boot (vboot)
   
   # Generate keys
   futility vbutil_key --pack keys/root_key.vbpubk \
       --key keys/root_key.pem --algorithm 11
   
   # Sign firmware
   futility vbutil_firmware --vblock vblock.bin \
       --keyblock keys/firmware.keyblock \
       --signprivate keys/firmware_data_key.vbprivk \
       --version 1 --kernelkey keys/kernel_subkey.vbpubk \
       --fv firmware.bin

EDK2 Secure Boot
----------------

.. code-block:: c

   // Enable in .dsc
   [PcdsFixedAtBuild]
     gEfiSecurityPkgTokenSpaceGuid.PcdUserPhysicalPresence|TRUE
   
   [Components]
     SecurityPkg/VariableAuthenticated/SecureBootConfigDxe/SecureBootConfigDxe.inf

Custom CPU Initialization
--------------------------

**Coreboot example:**

.. code-block:: c

   // src/cpu/myvendor/mycpu/mycpu_init.c
   static void model_XXXX_init(struct device *cpu)
   {
       /* Enable cache */
       x86_enable_cache();
       
       /* Setup MTRRs */
       x86_setup_mtrrs();
       x86_mtrr_check();
       
       /* Enable local APIC */
       setup_lapic();
       
       /* Set up ACPI */
       acpi_init(cpu);
   }
   
   static struct device_operations cpu_dev_ops = {
       .init = model_XXXX_init,
   };

ACPI Table Generation
---------------------

**Coreboot DSDT example:**

.. code-block:: asl

   /* src/mainboard/myvendor/myboard/acpi/platform.asl */
   DefinitionBlock (
       "platform.aml",
       "DSDT",
       2,
       "MYBRD",
       "MYBOARD",
       0x20160101
   )
   {
       Scope (\_SB)
       {
           Device (PCI0)
           {
               Name (_HID, EisaId ("PNP0A08"))
               Name (_CID, EisaId ("PNP0A03"))
               
               Device (LPCB)
               {
                   Name (_ADR, 0x001F0000)
                   
                   Device (COM1)
                   {
                       Name (_HID, EisaId ("PNP0501"))
                       Name (_UID, 1)
                       
                       Method (_STA, 0, NotSerialized)
                       {
                           Return (0x0F)
                       }
                   }
               }
           }
       }
   }

📚 Best Practices
==================

Coreboot
--------

1. **Use devicetree.cb**: Describe hardware declaratively
2. **Minimize bootblock**: Keep first stage small and fast
3. **Separate stages**: Clean separation between romstage/ramstage
4. **Test incrementally**: Verify each stage before proceeding
5. **Backup original firmware**: Always keep working backup

EDK2
----

1. **Follow coding style**: EDK II C Coding Standards Specification
2. **Use libraries**: Leverage existing library classes
3. **Protocol-oriented**: Design with UEFI protocol model
4. **Memory management**: Proper allocation/deallocation
5. **Error handling**: Check and handle all return values

🛠️ Useful Tools
=================

Coreboot Tools
--------------

.. code-block:: bash

   # cbmem - Read coreboot memory table
   sudo ./util/cbmem/cbmem -c  # Console log
   sudo ./util/cbmem/cbmem -t  # Timestamps
   
   # ectool - Embedded Controller tool
   sudo ./util/ectool/ectool -i
   
   # inteltool - Intel chipset info
   sudo ./util/inteltool/inteltool -a
   
   # superiotool - Super I/O detection
   sudo ./util/superiotool/superiotool -d

EDK2 Tools
----------

.. code-block:: bash

   # GenFw - Generate UEFI PE/COFF images
   GenFw -e UEFI_APPLICATION -o App.efi App.dll
   
   # VolInfo - Firmware volume info
   VolInfo OVMF.fd
   
   # EfiRom - Create PCI option ROM
   EfiRom -f 0x8086 -i 0x1234 -e MyDriver.efi -o MyDriver.rom

📖 Resources
=============

Documentation
-------------

**Coreboot:**

* Official Docs: https://doc.coreboot.org/
* Source: https://review.coreboot.org/coreboot
* Mailing List: coreboot@coreboot.org

**EDK2:**

* Getting Started: https://github.com/tianocore/tianocore.github.io/wiki/Getting-Started-with-EDK-II
* API Reference: https://github.com/tianocore-docs
* UEFI Specification: https://uefi.org/specifications

Community
---------

* **Coreboot IRC**: #coreboot on libera.chat
* **EDK2 Mailing List**: devel@edk2.groups.io
* **UEFI Forum**: https://uefi.org/forum

================================
Last Updated: January 2026
Version: 3.0
================================
