====================================
Bootloaders Complete Reference
====================================

:Author: Technical Documentation
:Date: January 2026
:Version: 3.0
:License: CC-BY-SA-4.0

.. contents:: 📑 Table of Contents
   :depth: 3
   :local:
   :backlinks: top

🎯 Overview
============

This is a comprehensive index of bootloader technologies. For detailed guides, see the dedicated cheatsheets:

* **U-Boot_Complete.rst** - Universal bootloader for embedded systems
* **GRUB_Complete.rst** - GNU bootloader for Linux/multi-OS
* **Secure_Boot_Complete.rst** - UEFI Secure Boot and verified boot
* **Coreboot_EDK2_Complete.rst** - Firmware development
* **SMP_AMP_Complete.rst** - Multicore processing

🔧 Popular Bootloaders
=======================

Embedded Systems
----------------

+-------------------+---------------------------+---------------------------------------+
| **Bootloader**    | **Architecture Support**  | **Key Features**                      |
+===================+===========================+=======================================+
| **U-Boot**        | ARM, x86, MIPS, PowerPC,  | Network boot (TFTP, HTTP, PXE),      |
|                   | RISC-V, ARC               | USB, eMMC, NAND, verified boot,       |
| **See:**          |                           | scripting, device trees               |
| U-Boot_Complete   |                           |                                       |
+-------------------+---------------------------+---------------------------------------+
| **Barebox**       | ARM, x86, MIPS, RISC-V    | U-Boot derivative, Linux-like         |
|                   |                           | drivers, smaller footprint,           |
|                   |                           | UEFI compatibility                    |
+-------------------+---------------------------+---------------------------------------+
| **wolfBoot**      | ARM, x86, RISC-V          | Secure boot, delta/OTA updates,       |
|                   |                           | TPM support, small footprint          |
+-------------------+---------------------------+---------------------------------------+
| **RedBoot**       | ARM, PowerPC, MIPS        | eCos RTOS-based, serial/Ethernet      |
|                   |                           | debugging                             |
+-------------------+---------------------------+---------------------------------------+
| **Arduino**       | AVR (ATmega)              | USB firmware updates, Optiboot,       |
| **Bootloader**    |                           | AVR109 protocol                       |
+-------------------+---------------------------+---------------------------------------+

Desktop/Server
--------------

+-------------------+---------------------------+---------------------------------------+
| **Bootloader**    | **Platform Support**      | **Key Features**                      |
+===================+===========================+=======================================+
| **GRUB2**         | x86 BIOS, UEFI, ARM,      | Multi-OS boot, scripting, themes,     |
|                   | PowerPC                   | encrypted partitions, network boot    |
| **See:**          |                           |                                       |
| GRUB_Complete     |                           |                                       |
+-------------------+---------------------------+---------------------------------------+
| **systemd-boot**  | UEFI (x86_64, ARM64)      | Simple UEFI loader, systemd           |
|                   |                           | integration, auto-discovery           |
+-------------------+---------------------------+---------------------------------------+
| **rEFInd**        | UEFI                      | Graphical boot manager, themes,       |
|                   |                           | auto-detection, Mac-style UI          |
+-------------------+---------------------------+---------------------------------------+
| **Clover**        | UEFI                      | Hackintosh support, macOS on          |
|                   |                           | non-Apple hardware, kext injection    |
+-------------------+---------------------------+---------------------------------------+
| **Windows**       | x86 BIOS, UEFI            | Windows boot manager, BCD,            |
| **Bootmgr**       |                           | multi-boot support                    |
+-------------------+---------------------------+---------------------------------------+
| **LILO**          | x86 BIOS                  | Legacy Linux loader, simple,          |
|                   |                           | sector-based                          |
+-------------------+---------------------------+---------------------------------------+
| **Syslinux**      | x86 BIOS, UEFI            | FAT/ext filesystem support,           |
|                   |                           | PXE boot, lightweight                 |
+-------------------+---------------------------+---------------------------------------+

Firmware
--------

+-------------------+---------------------------+---------------------------------------+
| **Firmware**      | **Architecture Support**  | **Key Features**                      |
+===================+===========================+=======================================+
| **Coreboot**      | x86, ARM, RISC-V,         | Fast boot (<1s), minimal firmware,    |
|                   | PowerPC                   | payload system (SeaBIOS, GRUB,        |
| **See:**          |                           | Linux, UEFI)                          |
| Coreboot_EDK2     |                           |                                       |
+-------------------+---------------------------+---------------------------------------+
| **Tianocore**     | x86, ARM, RISC-V          | Open-source UEFI implementation,      |
| **EDK2**          |                           | modular, standards-compliant          |
| **See:**          |                           |                                       |
| Coreboot_EDK2     |                           |                                       |
+-------------------+---------------------------+---------------------------------------+
| **OpenBIOS**      | PowerPC, SPARC            | Open Firmware implementation,         |
|                   |                           | device tree                           |
+-------------------+---------------------------+---------------------------------------+
| **DINK32**        | PowerPC                   | Diagnostic bootloader, debugging      |
+-------------------+---------------------------+---------------------------------------+
| **x86 BIOS**      | x86                       | Traditional PC firmware, legacy       |
|                   |                           | INT 13h, 16-bit real mode             |
+-------------------+---------------------------+---------------------------------------+

Specialized
-----------

+-------------------+---------------------------+---------------------------------------+
| **Bootloader**    | **Use Case**              | **Key Features**                      |
+===================+===========================+=======================================+
| **BURG**          | Linux desktops            | GRUB fork, graphical interface,       |
|                   |                           | themes                                |
+-------------------+---------------------------+---------------------------------------+
| **Yaboot**        | PowerPC Linux             | IBM PowerPC systems, OF               |
|                   |                           | compatibility                         |
+-------------------+---------------------------+---------------------------------------+
| **xOSL**          | Multi-boot                | Extended OS loader, legacy systems    |
+-------------------+---------------------------+---------------------------------------+
| **Smart Boot**    | Legacy x86                | Floppy-based, simple boot manager     |
| **Manager**       |                           |                                       |
+-------------------+---------------------------+---------------------------------------+

🔐 Secure Boot Technologies
============================

**For comprehensive secure boot implementation, see: Secure_Boot_Complete.rst**

Key Hierarchy
-------------

+---------------------------+----------------------------------------------------------+
| **Component**             | **Description**                                          |
+===========================+==========================================================+
| **Platform Key (PK)**     | Top-level trust, RSA-2048/X509, controls KEK            |
+---------------------------+----------------------------------------------------------+
| **Key Exchange Key**      | Intermediate trust layer, updates DB/DBX                 |
| **(KEK)**                 |                                                          |
+---------------------------+----------------------------------------------------------+
| **Signature Database**    | Whitelist of allowed signatures/certificates             |
| **(DB)**                  |                                                          |
+---------------------------+----------------------------------------------------------+
| **Forbidden Database**    | Blacklist of revoked/malicious signatures                |
| **(DBX)**                 |                                                          |
+---------------------------+----------------------------------------------------------+

Security Concepts
-----------------

+---------------------------+----------------------------------------------------------+
| **Concept**               | **Description**                                          |
+===========================+==========================================================+
| **Root of Trust (RoT)**   | Immutable hardware anchor, foundation of security        |
+---------------------------+----------------------------------------------------------+
| **Chain of Trust**        | Sequential verification: Firmware → Bootloader →         |
|                           | Kernel → Modules                                         |
+---------------------------+----------------------------------------------------------+
| **UEFI Secure Boot**      | Standard for verifying boot components via signatures    |
+---------------------------+----------------------------------------------------------+
| **Verified Boot**         | Cryptographic verification (FIT images in U-Boot)        |
+---------------------------+----------------------------------------------------------+
| **Measured Boot**         | TPM-based measurement and attestation                    |
+---------------------------+----------------------------------------------------------+
| **Digital Signature**     | RSA/ECDSA with SHA-256/384/512 hashing                   |
+---------------------------+----------------------------------------------------------+
| **Hardware Security**     | TPM, Secure Element, TrustZone, OTP/eFuse                |
+---------------------------+----------------------------------------------------------+

Update Mechanisms
-----------------

+---------------------------+----------------------------------------------------------+
| **Method**                | **Description**                                          |
+===========================+==========================================================+
| **OTA (Over-The-Air)**    | Remote firmware delivery with signature verification     |
+---------------------------+----------------------------------------------------------+
| **Delta Updates**         | Incremental patches, reduces download size               |
+---------------------------+----------------------------------------------------------+
| **A/B Partitioning**      | Dual boot slots for safe updates and rollback            |
+---------------------------+----------------------------------------------------------+
| **Anti-Rollback**         | Version tracking prevents downgrade attacks              |
+---------------------------+----------------------------------------------------------+

🛡️ Fail-Safe Boot Mechanisms
==============================

Recovery Modes
--------------

+---------------------------+----------------------------------------------------------+
| **Mode**                  | **Description**                                          |
+===========================+==========================================================+
| **Safe Mode**             | Minimal drivers/services, no third-party software,       |
|                           | troubleshooting mode                                     |
+---------------------------+----------------------------------------------------------+
| **Safe Mode with**        | Adds wired network drivers for internet access           |
| **Networking**            |                                                          |
+---------------------------+----------------------------------------------------------+
| **Safe Mode with**        | CLI interface for advanced recovery and scripting        |
| **Command Prompt**        |                                                          |
+---------------------------+----------------------------------------------------------+
| **Last Known Good**       | Revert to previous working configuration after           |
| **(LKG)**                 | failed boot                                              |
+---------------------------+----------------------------------------------------------+
| **Recovery Environment**  | Bootable recovery tools for repair/reset                 |
| **(WinRE, Recovery)**     | (Windows, Linux, OpenWrt)                                |
+---------------------------+----------------------------------------------------------+
| **Factory Reset**         | Restore device to original state, wipe user data         |
+---------------------------+----------------------------------------------------------+

Failsafe Triggers
-----------------

+---------------------------+----------------------------------------------------------+
| **Trigger Method**        | **Implementation**                                       |
+===========================+==========================================================+
| **Button Press**          | Physical button during boot window (3-5 seconds)         |
+---------------------------+----------------------------------------------------------+
| **Serial Console**        | Press specific key (e.g., 'f', ESC) on serial           |
+---------------------------+----------------------------------------------------------+
| **Boot Counter**          | Automatic failsafe after N failed boot attempts          |
+---------------------------+----------------------------------------------------------+
| **Broadcast Packet**      | UDP packet detection on network (OpenWrt)                |
+---------------------------+----------------------------------------------------------+
| **Watchdog Timeout**      | Hardware watchdog triggers recovery                      |
+---------------------------+----------------------------------------------------------+

Dual Boot Strategies
--------------------

+---------------------------+----------------------------------------------------------+
| **Strategy**              | **Description**                                          |
+===========================+==========================================================+
| **A/B Partitioning**      | Two complete system images, switch on failure            |
|                           | (Android, Chrome OS)                                     |
+---------------------------+----------------------------------------------------------+
| **Golden Image**          | Known-good firmware backup, restore on corruption        |
+---------------------------+----------------------------------------------------------+
| **Root Filesystem**       | Separate failsafe root filesystem for recovery           |
| **Fallback**              |                                                          |
+---------------------------+----------------------------------------------------------+
| **Disable Auto-Restart**  | Prevents boot loops, allows manual intervention          |
+---------------------------+----------------------------------------------------------+

⚙️ SMP and AMP Multicore Processing
=====================================

**For comprehensive multicore guide, see: SMP_AMP_Complete.rst**

Architecture Comparison
-----------------------

+---------------------------+----------------------------------+----------------------------------+
| **Aspect**                | **SMP (Symmetric)**              | **AMP (Asymmetric)**             |
+===========================+==================================+==================================+
| **OS Model**              | Single shared OS instance        | Multiple independent OS          |
+---------------------------+----------------------------------+----------------------------------+
| **Core Types**            | Homogeneous (identical ISA)      | Can be heterogeneous             |
+---------------------------+----------------------------------+----------------------------------+
| **Memory**                | Shared memory, cache coherent    | Shared or partitioned            |
+---------------------------+----------------------------------+----------------------------------+
| **Scheduling**            | OS kernel handles                | Manual assignment                |
+---------------------------+----------------------------------+----------------------------------+
| **IPC Mechanism**         | Kernel primitives (pipes, etc.)  | RPMsg, mailbox, shared memory    |
+---------------------------+----------------------------------+----------------------------------+
| **Example**               | Linux on 4x Cortex-A53           | Linux (A53) + FreeRTOS (M4)      |
+---------------------------+----------------------------------+----------------------------------+

SMP Concepts
------------

+---------------------------+----------------------------------------------------------+
| **Concept**               | **Description**                                          |
+===========================+==========================================================+
| **Homogeneous Cores**     | Identical processor cores (same ISA, features)           |
+---------------------------+----------------------------------------------------------+
| **Shared Memory**         | Common address space, cache coherency protocols          |
+---------------------------+----------------------------------------------------------+
| **Load Balancing**        | Dynamic task distribution across cores                   |
+---------------------------+----------------------------------------------------------+
| **NUMA**                  | Non-Uniform Memory Access, varying memory latencies      |
+---------------------------+----------------------------------------------------------+
| **HMP**                   | Heterogeneous Multi-Processing (big.LITTLE)              |
+---------------------------+----------------------------------------------------------+
| **CPU Affinity**          | Pin tasks/IRQs to specific cores                         |
+---------------------------+----------------------------------------------------------+

AMP Concepts
------------

+---------------------------+----------------------------------------------------------+
| **Concept**               | **Description**                                          |
+===========================+==========================================================+
| **Heterogeneous Cores**   | Different ISAs (e.g., ARM Cortex-A + Cortex-M)          |
+---------------------------+----------------------------------------------------------+
| **Multi-OS**              | Different OS per core (Linux + RTOS + bare-metal)       |
+---------------------------+----------------------------------------------------------+
| **Remoteproc**            | Linux framework for remote processor lifecycle           |
+---------------------------+----------------------------------------------------------+
| **RPMsg**                 | Message-based IPC for AMP systems                        |
+---------------------------+----------------------------------------------------------+
| **OpenAMP**               | Standard framework for AMP (Remoteproc + RPMsg)          |
+---------------------------+----------------------------------------------------------+
| **VirtIO**                | Virtual device abstraction for IPC                       |
+---------------------------+----------------------------------------------------------+
| **Resource Table**        | Firmware metadata for memory/resource allocation         |
+---------------------------+----------------------------------------------------------+
| **Lifecycle Management**  | Host controls remote core boot/shutdown                  |
+---------------------------+----------------------------------------------------------+

Common SoC Platforms
--------------------

+---------------------------+---------------------------+------------------------------+
| **SoC Family**            | **Cores**                 | **Typical Configuration**    |
+===========================+===========================+==============================+
| **NXP i.MX 8M**           | Cortex-A53 + Cortex-M4/M7 | Linux (A53) + RTOS (M4/M7)   |
+---------------------------+---------------------------+------------------------------+
| **TI AM64x/AM62x**        | Cortex-A53 + R5F + M4F    | Linux + RTOS + bare-metal    |
+---------------------------+---------------------------+------------------------------+
| **STM32MP1**              | Cortex-A7 + Cortex-M4     | Linux (A7) + RTOS (M4)       |
+---------------------------+---------------------------+------------------------------+
| **Xilinx Zynq**           | Cortex-A9/A53 + FPGA      | Linux + custom FPGA logic    |
+---------------------------+---------------------------+------------------------------+
| **Raspberry Pi**          | 4x Cortex-A53/A72         | Linux SMP                    |
+---------------------------+---------------------------+------------------------------+
| **Intel Xeon**            | Multi-socket x86          | Linux SMP with NUMA          |
+---------------------------+---------------------------+------------------------------+
| **Qualcomm Snapdragon**   | Kryo (big.LITTLE)         | Android HMP                  |
+---------------------------+----------------------------------------------------------+

Operating Systems
-----------------

**SMP Support:**

* Linux - Full SMP kernel
* Windows - SMP by default
* FreeBSD/NetBSD - SMP capable
* VxWorks - SMP mode
* QNX - SMP microkernel

**AMP/RTOS:**

* FreeRTOS - Popular for Cortex-M
* Zephyr - IoT RTOS
* eCos - Used in RedBoot
* RTEMS - Space/embedded RT OS
* VxWorks - Commercial RTOS
* Bare-metal - Custom firmware

**Hypervisors:**

* Xen - Type-1 hypervisor
* KVM - Linux-based virtualization
* Jailhouse - Partitioning hypervisor
* Type-1/2 - Hardware virtualization

📊 Use Case Matrix
===================

Bootloader Selection Guide
---------------------------

+------------------------+-------------------+----------------------------------------+
| **Use Case**           | **Recommended**   | **Rationale**                          |
+========================+===================+========================================+
| Embedded Linux         | U-Boot            | Industry standard, comprehensive       |
+------------------------+-------------------+----------------------------------------+
| x86 Linux Desktop      | GRUB2             | Multi-boot, UEFI support               |
+------------------------+-------------------+----------------------------------------+
| IoT/Constrained        | wolfBoot, Barebox | Small footprint, secure                |
+------------------------+-------------------+----------------------------------------+
| ChromeOS               | Coreboot          | Fast boot, verified boot               |
+------------------------+-------------------+----------------------------------------+
| UEFI Firmware          | Tianocore EDK2    | Standards-compliant UEFI               |
+------------------------+-------------------+----------------------------------------+
| Network Boot           | U-Boot, Syslinux  | PXE, TFTP support                      |
+------------------------+-------------------+----------------------------------------+
| Raspberry Pi           | U-Boot, start.elf | ARM boot, GPU firmware                 |
+------------------------+-------------------+----------------------------------------+
| Android Device         | U-Boot, fastboot  | Fastboot protocol, A/B updates         |
+------------------------+-------------------+----------------------------------------+

📚 Additional Resources
========================

Documentation Links
-------------------

* **U-Boot**: https://u-boot.readthedocs.io/
* **GRUB**: https://www.gnu.org/software/grub/manual/
* **Coreboot**: https://doc.coreboot.org/
* **EDK2**: https://github.com/tianocore/tianocore.github.io/wiki
* **OpenAMP**: https://github.com/OpenAMP/open-amp
* **UEFI**: https://uefi.org/specifications

Communities
-----------

* **U-Boot**: u-boot@lists.denx.de
* **GRUB**: bug-grub@gnu.org
* **Coreboot**: coreboot@coreboot.org, IRC #coreboot
* **EDK2**: devel@edk2.groups.io
* **Linux Boot**: linux-boot@vger.kernel.org

Tools & Utilities
-----------------

* **mkimage** - Create U-Boot images
* **grub-mkconfig** - Generate GRUB config
* **cbfstool** - Coreboot filesystem tool
* **flashrom** - Universal flash programmer
* **efibootmgr** - UEFI boot manager
* **sbsigntool** - Sign UEFI binaries
* **mokutil** - MOK management

================================
Last Updated: January 2026
Version: 3.0
================================