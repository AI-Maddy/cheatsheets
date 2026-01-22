====================================
Buildroot Complete Development Guide
====================================

:Author: Madhavan Vivekanandan
:Date: January 2026
:Version: 1.0
:Project Experience: Intel Atom Avionics Platform, ARM platforms

.. contents:: Table of Contents
   :depth: 3
   :local:

Overview
========

Comprehensive guide to Buildroot for embedded Linux system development, covering monolithic image creation, package porting, dependency management, BSP customization, and security hardening based on real avionics and embedded project experience.

Introduction
============

What is Buildroot?
------------------

Buildroot is a simple, efficient, and easy-to-use tool to generate embedded Linux systems through cross-compilation.

**Key Features:**

.. code-block:: text

   ┌──────────────────────────────────────────┐
   │         Buildroot Architecture           │
   ├──────────────────────────────────────────┤
   │  Configuration (Kconfig)                 │
   │  ├── Target Architecture                 │
   │  ├── Toolchain                           │
   │  ├── Kernel/Bootloader                   │
   │  └── Root Filesystem Packages            │
   ├──────────────────────────────────────────┤
   │  Build System (Makefiles)                │
   │  ├── Download sources                    │
   │  ├── Extract and patch                   │
   │  ├── Configure and build                 │
   │  └── Install to target/staging           │
   ├──────────────────────────────────────────┤
   │  Output                                  │
   │  ├── Cross-compilation toolchain         │
   │  ├── Root filesystem images              │
   │  ├── Kernel image                        │
   │  └── Bootloader                          │
   └──────────────────────────────────────────┘

**When to Use Buildroot:**

- Small to medium-sized embedded systems
- Resource-constrained devices
- Need for reproducible builds
- Quick prototyping
- Security-focused systems (minimal attack surface)

**Project Example: Intel Atom Avionics Platform**

- Monolithic operational software image
- UEFI secure boot
- SELinux-hardened system
- Read-only squashfs root filesystem

Getting Started
===============

Installation and Setup
----------------------

.. code-block:: bash

   # Download Buildroot
   git clone https://git.buildroot.net/buildroot
   cd buildroot
   git checkout 2023.11  # LTS release
   
   # Or download tarball
   wget https://buildroot.org/downloads/buildroot-2023.11.tar.gz
   tar xzf buildroot-2023.11.tar.gz
   cd buildroot-2023.11
   
   # Check prerequisites
   which gcc make patch perl python3 wget git
   
   # For Intel Atom (64-bit)
   make pc_x86_64_efi_defconfig
   
   # For ARM (e.g., i.MX)
   make freescale_imx6qsabresd_defconfig
   
   # Customize configuration
   make menuconfig
   
   # Build (parallel build)
   make -j$(nproc)

Directory Structure
-------------------

.. code-block:: text

   buildroot/
   ├── arch/                   # Architecture-specific makefiles
   ├── board/                  # Board-specific files
   │   └── <vendor>/<board>/
   │       ├── linux.config    # Kernel configuration
   │       ├── rootfs-overlay/ # Additional root filesystem files
   │       └── post-build.sh   # Post-build customization scripts
   ├── boot/                   # Bootloader packages
   │   ├── grub2/
   │   ├── uboot/
   │   └── syslinux/
   ├── configs/                # Defconfig files
   ├── dl/                     # Downloaded source tarballs
   ├── fs/                     # Filesystem generation code
   ├── linux/                  # Linux kernel build infrastructure
   ├── output/                 # Build output directory
   │   ├── build/              # Build directories for each package
   │   ├── host/               # Host tools
   │   ├── images/             # Final images (kernel, rootfs, etc.)
   │   ├── staging/            # Sysroot for cross-compilation
   │   └── target/             # Target root filesystem (before finalization)
   ├── package/                # Package definitions
   ├── support/                # Support scripts
   └── toolchain/              # Toolchain infrastructure

Project-Specific Configuration
===============================

Avionics Platform (Intel Atom C3xxx)
-------------------------------------

**Requirements:**

- UEFI Secure Boot
- Monolithic squashfs image
- SELinux mandatory access control
- Minimal attack surface
- Deterministic builds

**Defconfig Creation:**

.. code-block:: bash

   # board/rockwell/atom-avionics/defconfig
   
   # Architecture
   BR2_x86_64=y
   BR2_x86_corei7=y
   
   # Toolchain
   BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
   BR2_TOOLCHAIN_BUILDROOT_CXX=y
   BR2_GCC_VERSION_11_X=y
   BR2_TOOLCHAIN_BUILDROOT_FORTRAN=y
   BR2_TOOLCHAIN_BUILDROOT_OPENMP=y
   
   # Kernel
   BR2_LINUX_KERNEL=y
   BR2_LINUX_KERNEL_CUSTOM_VERSION=y
   BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="5.15.120"
   BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
   BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="board/rockwell/atom-avionics/linux.config"
   BR2_LINUX_KERNEL_NEEDS_HOST_OPENSSL=y
   BR2_LINUX_KERNEL_NEEDS_HOST_LIBELF=y
   
   # Bootloader
   BR2_TARGET_GRUB2=y
   BR2_TARGET_GRUB2_X86_64_EFI=y
   BR2_TARGET_GRUB2_BUILTIN_MODULES="boot linux ext2 fat part_msdos part_gpt normal efi_gop efi_uga video_bochs video_cirrus"
   
   # System
   BR2_TARGET_GENERIC_HOSTNAME="avionics-platform"
   BR2_TARGET_GENERIC_ISSUE="Avionics Embedded Platform"
   BR2_ROOTFS_DEVICE_CREATION_DYNAMIC_EUDEV=y
   BR2_TARGET_GENERIC_ROOT_PASSWD="$1$encrypted$hash"
   BR2_SYSTEM_DHCP="eth0"
   
   # Init system
   BR2_INIT_SYSTEMD=y
   BR2_PACKAGE_SYSTEMD_NETWORKD=y
   BR2_PACKAGE_SYSTEMD_RESOLVED=y
   
   # Security: SELinux
   BR2_PACKAGE_LIBSELINUX=y
   BR2_PACKAGE_LIBSEMANAGE=y
   BR2_PACKAGE_LIBSEPOL=y
   BR2_PACKAGE_POLICYCOREUTILS=y
   BR2_PACKAGE_REFPOLICY=y
   BR2_PACKAGE_SELINUX_PYTHON=y
   BR2_PACKAGE_SETOOLS=y
   
   # Security: Cryptography
   BR2_PACKAGE_OPENSSL=y
   BR2_PACKAGE_LIBGCRYPT=y
   BR2_PACKAGE_CRYPTSETUP=y
   
   # Networking
   BR2_PACKAGE_IPTABLES=y
   BR2_PACKAGE_ETHTOOL=y
   BR2_PACKAGE_IPROUTE2=y
   BR2_PACKAGE_OPENSSH=y
   BR2_PACKAGE_OPENSSH_SERVER=y
   
   # Development tools (remove for production)
   BR2_PACKAGE_GDB=y
   BR2_PACKAGE_STRACE=y
   BR2_PACKAGE_LTRACE=y
   
   # Custom packages
   BR2_PACKAGE_AVIONICS_APP=y
   BR2_PACKAGE_FPGA_FIRMWARE=y
   
   # Filesystem
   BR2_TARGET_ROOTFS_SQUASHFS=y
   BR2_TARGET_ROOTFS_SQUASHFS_XZ=y
   
   # EFI image
   BR2_TARGET_ROOTFS_EXT2=y
   BR2_TARGET_ROOTFS_EXT2_4=y
   BR2_TARGET_ROOTFS_EXT2_SIZE="512M"

**Custom Linux Kernel Configuration:**

.. code-block:: bash

   # board/rockwell/atom-avionics/linux.config
   
   CONFIG_64BIT=y
   CONFIG_X86_64=y
   CONFIG_SMP=y
   CONFIG_NR_CPUS=16
   
   # UEFI support
   CONFIG_EFI=y
   CONFIG_EFI_STUB=y
   CONFIG_EFI_MIXED=y
   CONFIG_EFI_VARS=y
   
   # Security
   CONFIG_SECURITY=y
   CONFIG_SECURITY_SELINUX=y
   CONFIG_SECURITY_SELINUX_BOOTPARAM=y
   CONFIG_SECURITY_SELINUX_DEVELOP=y
   CONFIG_SECURITY_SELINUX_AVC_STATS=y
   CONFIG_DEFAULT_SECURITY_SELINUX=y
   
   CONFIG_SECCOMP=y
   CONFIG_SECCOMP_FILTER=y
   
   CONFIG_HARDENED_USERCOPY=y
   CONFIG_FORTIFY_SOURCE=y
   
   # Read-only rootfs
   CONFIG_OVERLAY_FS=y
   CONFIG_SQUASHFS=y
   CONFIG_SQUASHFS_XZ=y
   
   # Networking
   CONFIG_NETFILTER=y
   CONFIG_NETFILTER_XTABLES=y
   CONFIG_IP_NF_IPTABLES=y
   CONFIG_IP_NF_FILTER=y
   
   # PCIe
   CONFIG_PCI=y
   CONFIG_PCIEPORTBUS=y
   CONFIG_PCIEASPM=y
   
   # Custom drivers
   CONFIG_AVIONICS_FPGA=m
   CONFIG_ARINC_AFDX=m

Package Porting and Customization
==================================

Creating Custom Packages
-------------------------

**Project Example: Avionics Application Package**

.. code-block:: bash

   # package/avionics-app/Config.in
   
   config BR2_PACKAGE_AVIONICS_APP
       bool "avionics-app"
       depends on BR2_PACKAGE_OPENSSL
       depends on BR2_PACKAGE_LIBSELINUX
       select BR2_PACKAGE_BOOST
       select BR2_PACKAGE_BOOST_SYSTEM
       select BR2_PACKAGE_BOOST_THREAD
       help
         Avionics platform application.
         
         https://github.com/rockwell/avionics-app
   
   comment "avionics-app needs OpenSSL and SELinux"
       depends on !BR2_PACKAGE_OPENSSL || !BR2_PACKAGE_LIBSELINUX

**Package Makefile:**

.. code-block:: makefile

   # package/avionics-app/avionics-app.mk
   
   AVIONICS_APP_VERSION = 2.1.0
   AVIONICS_APP_SITE = $(call github,rockwell,avionics-app,v$(AVIONICS_APP_VERSION))
   AVIONICS_APP_LICENSE = Proprietary
   AVIONICS_APP_DEPENDENCIES = openssl boost libselinux
   AVIONICS_APP_INSTALL_STAGING = NO
   AVIONICS_APP_INSTALL_TARGET = YES
   
   # CMake-based build
   AVIONICS_APP_CONF_OPTS = \
       -DCMAKE_BUILD_TYPE=Release \
       -DENABLE_SELINUX=ON \
       -DENABLE_SECURE_BOOT=ON
   
   define AVIONICS_APP_INSTALL_INIT_SYSTEMD
       $(INSTALL) -D -m 0644 $(@D)/systemd/avionics-app.service \
           $(TARGET_DIR)/usr/lib/systemd/system/avionics-app.service
   endef
   
   define AVIONICS_APP_INSTALL_TARGET_CMDS
       $(INSTALL) -D -m 0755 $(@D)/build/avionics-app \
           $(TARGET_DIR)/usr/bin/avionics-app
       $(INSTALL) -D -m 0644 $(@D)/config/avionics.conf \
           $(TARGET_DIR)/etc/avionics/avionics.conf
       $(INSTALL) -D -m 0644 $(@D)/selinux/avionics_app.pp \
           $(TARGET_DIR)/usr/share/selinux/avionics_app.pp
   endef
   
   $(eval $(cmake-package))

**Register Package:**

.. code-block:: bash

   # package/Config.in
   
   menu "Custom packages"
       source "package/avionics-app/Config.in"
       source "package/fpga-firmware/Config.in"
   endmenu

Porting External Packages
--------------------------

**Example: Custom Communication Stack**

.. code-block:: bash

   # package/arinc-afdx/Config.in
   
   config BR2_PACKAGE_ARINC_AFDX
       bool "arinc-afdx"
       depends on BR2_LINUX_KERNEL
       help
         ARINC 664 (AFDX) communication stack.

.. code-block:: makefile

   # package/arinc-afdx/arinc-afdx.mk
   
   ARINC_AFDX_VERSION = 1.5.2
   ARINC_AFDX_SITE = /path/to/local/source
   ARINC_AFDX_SITE_METHOD = local
   ARINC_AFDX_LICENSE = Proprietary
   ARINC_AFDX_DEPENDENCIES = linux
   
   define ARINC_AFDX_BUILD_CMDS
       $(MAKE) $(LINUX_MAKE_FLAGS) -C $(LINUX_DIR) \
           M=$(@D) modules
   endef
   
   define ARINC_AFDX_INSTALL_TARGET_CMDS
       $(MAKE) $(LINUX_MAKE_FLAGS) -C $(LINUX_DIR) \
           M=$(@D) INSTALL_MOD_PATH=$(TARGET_DIR) modules_install
   endef
   
   $(eval $(generic-package))

Dependency Management
---------------------

**Automatic Dependency Resolution:**

.. code-block:: makefile

   # Package infrastructure handles dependencies
   
   PACKAGE_DEPENDENCIES = libfoo libbar
   
   # Buildroot ensures:
   # 1. Dependencies built before package
   # 2. Dependency headers available in staging
   # 3. Dependency libraries linked correctly

**Circular Dependency Handling:**

.. code-block:: bash

   # If package A needs B and B needs A (rare):
   
   # Option 1: Bootstrap build
   BR2_PACKAGE_A_BOOTSTRAP=y
   
   # Option 2: Split package
   # Create A-minimal without B dependency
   # Then full A with B

**Host vs Target Dependencies:**

.. code-block:: makefile

   # Host tools needed for build
   PACKAGE_DEPENDENCIES = host-pkgconf host-cmake
   
   # Target libraries
   PACKAGE_DEPENDENCIES += libssl zlib
   
   # Build-time only (not in target)
   PACKAGE_DEPENDENCIES += host-genimage

Monolithic Image Creation
==========================

Avionics Platform Approach
---------------------------

**Single Signed Image Strategy:**

.. code-block:: text

   Monolithic Image Structure:
   ┌─────────────────────────────────┐
   │     EFI System Partition        │
   │  ┌──────────────────────────┐   │
   │  │  Signed Bootloader       │   │
   │  │  (GRUB2 with sig)        │   │
   │  └──────────────────────────┘   │
   │  ┌──────────────────────────┐   │
   │  │  Signed Kernel           │   │
   │  │  (vmlinuz + signature)   │   │
   │  └──────────────────────────┘   │
   │  ┌──────────────────────────┐   │
   │  │  Signed Initramfs        │   │
   │  └──────────────────────────┘   │
   └─────────────────────────────────┘
   ┌─────────────────────────────────┐
   │     Root Partition               │
   │  ┌──────────────────────────┐   │
   │  │  Read-Only SquashFS      │   │
   │  │  - System binaries       │   │
   │  │  - Libraries             │   │
   │  │  - Configuration         │   │
   │  │  - Applications          │   │
   │  └──────────────────────────┘   │
   └─────────────────────────────────┘
   ┌─────────────────────────────────┐
   │     Data Partition (Optional)    │
   │  - Logs                          │
   │  - Runtime data                  │
   │  - Persistent configuration      │
   └─────────────────────────────────┘

**Image Generation Script:**

.. code-block:: bash

   # board/rockwell/atom-avionics/post-image.sh
   
   #!/bin/bash
   set -e
   
   BOARD_DIR="$(dirname $0)"
   IMAGES_DIR="${1}"
   
   # Sign kernel
   sbsign --key ${BOARD_DIR}/keys/db.key \
          --cert ${BOARD_DIR}/keys/db.crt \
          --output ${IMAGES_DIR}/bzImage.signed \
          ${IMAGES_DIR}/bzImage
   
   # Create EFI image
   genimage --rootpath "${TARGET_DIR}" \
            --tmppath "${BUILD_DIR}/genimage.tmp" \
            --inputpath "${IMAGES_DIR}" \
            --outputpath "${IMAGES_DIR}" \
            --config "${BOARD_DIR}/genimage-efi.cfg"
   
   # Calculate checksums
   cd ${IMAGES_DIR}
   sha256sum disk.img > disk.img.sha256
   
   # Create update package
   tar czf system-update-${BUILD_VERSION}.tar.gz \
       disk.img disk.img.sha256 update-metadata.json
   
   echo "Monolithic image created: ${IMAGES_DIR}/disk.img"
   echo "Update package: ${IMAGES_DIR}/system-update-${BUILD_VERSION}.tar.gz"

**Genimage Configuration:**

.. code-block:: cfg

   # board/rockwell/atom-avionics/genimage-efi.cfg
   
   image boot.vfat {
       vfat {
           files = {
               "EFI",
               "bzImage.signed",
               "rootfs.squashfs.signed"
           }
           file EFI/BOOT/bootx64.efi {
               image = "grub-efi/bootx64.efi"
           }
           file EFI/BOOT/grub.cfg {
               image = "grub.cfg"
           }
       }
       size = 256M
   }
   
   image disk.img {
       hdimage {
           gpt = true
       }
       
       partition boot {
           partition-type-uuid = c12a7328-f81f-11d2-ba4b-00a0c93ec93b
           image = "boot.vfat"
           bootable = true
       }
       
       partition rootfs {
           partition-type-uuid = 0fc63daf-8483-4772-8e79-3d69d8477de4
           image = "rootfs.squashfs"
       }
       
       partition data {
           partition-type-uuid = 0fc63daf-8483-4772-8e79-3d69d8477de4
           size = 1G
       }
   }

**GRUB Configuration:**

.. code-block:: cfg

   # board/rockwell/atom-avionics/grub.cfg
   
   set default=0
   set timeout=3
   
   # Secure boot entry
   menuentry "Avionics Platform" {
       insmod gzio
       insmod part_gpt
       insmod ext2
       insmod squash4
       
       set root=(hd0,gpt1)
       
       echo "Loading signed kernel..."
       linux /bzImage.signed root=/dev/sda2 ro \
           rootfstype=squashfs \
           security=selinux selinux=1 enforcing=1 \
           quiet console=ttyS0,115200
       
       echo "Booting..."
   }

BSP Customization
=================

Board-Specific Files
--------------------

**Directory Structure:**

.. code-block:: bash

   board/rockwell/atom-avionics/
   ├── defconfig                    # Buildroot configuration
   ├── linux.config                 # Kernel configuration
   ├── grub.cfg                     # Bootloader config
   ├── genimage-efi.cfg             # Image layout
   ├── post-build.sh                # Post-build customizations
   ├── post-image.sh                # Image generation
   ├── rootfs-overlay/              # Additional files
   │   ├── etc/
   │   │   ├── fstab
   │   │   ├── network/
   │   │   └── systemd/system/
   │   ├── usr/
   │   │   └── share/selinux/
   │   └── var/
   ├── patches/                     # Kernel/package patches
   │   └── linux/
   │       ├── 0001-Add-FPGA-driver.patch
   │       └── 0002-PCIe-multi-RC-support.patch
   └── keys/                        # Signing keys
       ├── PK.key
       ├── KEK.key
       └── db.key

**Post-Build Customization:**

.. code-block:: bash

   # board/rockwell/atom-avionics/post-build.sh
   
   #!/bin/bash
   set -e
   
   TARGET_DIR=$1
   
   # Remove unnecessary files for space/security
   rm -rf ${TARGET_DIR}/usr/share/man
   rm -rf ${TARGET_DIR}/usr/share/doc
   rm -rf ${TARGET_DIR}/usr/include
   rm -rf ${TARGET_DIR}/usr/share/gtk-doc
   
   # Remove development tools (production build)
   if [ "${BR2_ENABLE_DEBUG}" != "y" ]; then
       rm -f ${TARGET_DIR}/usr/bin/gdb
       rm -f ${TARGET_DIR}/usr/bin/strace
       rm -rf ${TARGET_DIR}/usr/lib/debug
   fi
   
   # Set correct permissions
   chmod 600 ${TARGET_DIR}/etc/shadow
   chmod 600 ${TARGET_DIR}/etc/ssh/sshd_config
   
   # Create required directories
   mkdir -p ${TARGET_DIR}/var/log/avionics
   mkdir -p ${TARGET_DIR}/opt/fpga/firmware
   
   # Install SELinux policy
   if [ -d ${TARGET_DIR}/usr/share/selinux ]; then
       echo "Installing SELinux policies..."
       # Policies installed by packages
   fi
   
   # Symlink timezone
   ln -sf /usr/share/zoneinfo/UTC ${TARGET_DIR}/etc/localtime
   
   # Configure systemd
   systemctl --root=${TARGET_DIR} enable avionics-app.service
   systemctl --root=${TARGET_DIR} enable sshd.service
   systemctl --root=${TARGET_DIR} disable NetworkManager.service
   
   echo "Post-build customization complete"

**Rootfs Overlay:**

.. code-block:: bash

   # board/rockwell/atom-avionics/rootfs-overlay/etc/fstab
   
   # <file system>  <mount point>  <type>  <options>         <dump> <pass>
   /dev/sda2        /              squashfs ro,noatime       0      0
   /dev/sda3        /var           ext4     rw,noatime       0      2
   tmpfs            /tmp           tmpfs    mode=1777,size=256M 0   0
   tmpfs            /run           tmpfs    mode=0755,nosuid,nodev 0 0

Kernel Customization
--------------------

**Applying Custom Patches:**

.. code-block:: bash

   # board/rockwell/atom-avionics/patches/linux/0001-Add-FPGA-driver.patch
   
   From: Madhavan Vivekanandan <madhavan@example.com>
   Date: Mon, 20 Jan 2025 10:00:00 +0000
   Subject: [PATCH] Add FPGA platform driver
   
   Add support for custom FPGA interfaceused in avionics platform.
   
   Signed-off-by: Madhavan Vivekanandan <madhavan@example.com>
   ---
    drivers/fpga/Kconfig           |  10 ++
    drivers/fpga/Makefile          |   1 +
    drivers/fpga/avionics_fpga.c   | 350 +++++++++++++++++++++++++++++
    3 files changed, 361 insertions(+)
    create mode 100644 drivers/fpga/avionics_fpga.c
   
   diff --git a/drivers/fpga/Kconfig b/drivers/fpga/Kconfig
   index 1234567..abcdefg 100644
   --- a/drivers/fpga/Kconfig
   +++ b/drivers/fpga/Kconfig
   @@ -100,6 +100,16 @@ config FPGA_MGR_XILINX_SPI
          FPGA manager driver support for Xilinx Spartan6 and 7 Series
          FPGA using slave serial configuration interface via SPI.
    
   +config FPGA_AVIONICS
   +    tristate "Avionics Platform FPGA"
   +    depends on PCI
   +    help
   +      FPGA driver for Avionics embedded platform.
   +      Provides interface for AFDX, discrete I/O, and other
   +      avionics-specific hardware.
   +
   +      If unsure, say N.
   +
    endif # FPGA
    
    endmenu

Security Hardening
==================

SELinux Integration
-------------------

**Enabling SELinux in Buildroot:**

.. code-block:: bash

   # In menuconfig:
   # System configuration
   #   -> Enable SELinux support
   
   BR2_PACKAGE_LIBSELINUX=y
   BR2_PACKAGE_LIBSEMANAGE=y
   BR2_PACKAGE_LIBSEPOL=y
   BR2_PACKAGE_POLICYCOREUTILS=y
   BR2_PACKAGE_REFPOLICY=y
   
   # Kernel config
   CONFIG_SECURITY_SELINUX=y
   CONFIG_SECURITY_SELINUX_BOOTPARAM=y
   CONFIG_DEFAULT_SECURITY_SELINUX=y

**Custom SELinux Policy:**

.. code-block:: bash

   # package/avionics-selinux-policy/avionics.te
   
   policy_module(avionics, 1.0.0)
   
   require {
       type init_t;
       type unconfined_t;
       type device_t;
       class file { read write open };
       class capability { sys_admin sys_rawio };
   }
   
   # Define avionics application domain
   type avionics_app_t;
   type avionics_app_exec_t;
   
   init_daemon_domain(avionics_app_t, avionics_app_exec_t)
   
   # Allow access to FPGA device
   allow avionics_app_t device_t:file { read write open };
   allow avionics_app_t self:capability { sys_admin sys_rawio };
   
   # Network access
   corenet_tcp_bind_generic_node(avionics_app_t)
   corenet_tcp_bind_http_port(avionics_app_t)
   
   # Logging
   logging_send_syslog_msg(avionics_app_t)
   
   # Deny dangerous capabilities
   neverallow avionics_app_t kernel_t:file { read write };
   neverallow avionics_app_t self:capability sys_module;

**Installing SELinux Policy:**

.. code-block:: bash

   # In post-build.sh
   
   if [ -f ${TARGET_DIR}/usr/share/selinux/avionics.pp ]; then
       mkdir -p ${TARGET_DIR}/etc/selinux/targeted/policy
       semodule -n -s targeted -i ${TARGET_DIR}/usr/share/selinux/avionics.pp \
                -p ${TARGET_DIR}/etc/selinux/targeted/policy
   fi
   
   # Label filesystem
   setfiles -F -r ${TARGET_DIR} \
       ${TARGET_DIR}/etc/selinux/targeted/contexts/files/file_contexts \
       ${TARGET_DIR}

Secure Boot
-----------

**UEFI Secure Boot Chain:**

.. code-block:: bash

   # Generate keys (one-time)
   board/rockwell/atom-avionics/generate-keys.sh
   
   #!/bin/bash
   
   KEYS_DIR=$(dirname $0)/keys
   mkdir -p ${KEYS_DIR}
   
   # Platform Key (PK)
   openssl req -new -x509 -newkey rsa:2048 \
       -keyout ${KEYS_DIR}/PK.key \
       -out ${KEYS_DIR}/PK.crt \
       -days 3650 -nodes \
       -subj "/CN=Platform Key/"
   
   # Key Exchange Key (KEK)
   openssl req -new -x509 -newkey rsa:2048 \
       -keyout ${KEYS_DIR}/KEK.key \
       -out ${KEYS_DIR}/KEK.crt \
       -days 3650 -nodes \
       -subj "/CN=Key Exchange Key/"
   
   # Signature Database (db)
   openssl req -new -x509 -newkey rsa:2048 \
       -keyout ${KEYS_DIR}/db.key \
       -out ${KEYS_DIR}/db.crt \
       -days 3650 -nodes \
       -subj "/CN=Signature Database/"
   
   echo "Keys generated in ${KEYS_DIR}"
   echo "IMPORTANT: Store private keys securely!"

**Signing Binaries:**

.. code-block:: bash

   # In post-image.sh
   
   sign_binary() {
       local INPUT=$1
       local OUTPUT=$2
       
       sbsign --key ${KEYS_DIR}/db.key \
              --cert ${KEYS_DIR}/db.crt \
              --output ${OUTPUT} ${INPUT}
       
       if [ $? -eq 0 ]; then
           echo "Signed: ${OUTPUT}"
       else
           echo "ERROR: Failed to sign ${INPUT}"
           exit 1
       fi
   }
   
   # Sign kernel
   sign_binary ${IMAGES_DIR}/bzImage ${IMAGES_DIR}/bzImage.signed
   
   # Sign modules
   for mod in $(find ${TARGET_DIR}/lib/modules -name "*.ko"); do
       ${LINUX_DIR}/scripts/sign-file sha256 \
           ${KEYS_DIR}/db.key ${KEYS_DIR}/db.crt ${mod}
   done

Read-Only Root Filesystem
--------------------------

**Overlay Configuration:**

.. code-block:: bash

   # In rootfs-overlay/etc/fstab
   
   # Read-only root
   /dev/sda2  /         squashfs  ro,noatime          0  0
   
   # Writable overlay for /var
   tmpfs      /var/tmp  tmpfs     mode=1777,size=64M  0  0
   
   # Persistent data
   /dev/sda3  /var      ext4      rw,noatime          0  2

**Systemd tmpfiles Configuration:**

.. code-block:: bash

   # rootfs-overlay/etc/tmpfiles.d/avionics.conf
   
   # Create runtime directories
   d /run/avionics 0755 avionics avionics -
   d /var/log/avionics 0755 avionics avionics -
   d /var/cache/avionics 0755 avionics avionics -
   
   # Clean temporary files on boot
   r /var/tmp/*
   r /tmp/*

Optimization and Size Reduction
================================

Minimizing Image Size
---------------------

**Buildroot Configuration:**

.. code-block:: bash

   # Optimize for size
   BR2_OPTIMIZE_S=y
   
   # Use musl instead of glibc (smaller)
   # BR2_TOOLCHAIN_BUILDROOT_MUSL=y  # If compatible
   
   # Strip binaries
   BR2_STRIP_strip=y
   
   # Don't install documentation
   # BR2_PACKAGE_*_INSTALL_DOC is not set

**Remove Unnecessary Packages:**

.. code-block:: bash
   
   # Audit package sizes
   cd output/target
   du -sh * | sort -h
   
   # Remove unused packages in menuconfig
   # Disable: python, perl, lua if not needed
   # Use busybox alternatives where possible

**Busybox Configuration:**

.. code-block:: bash

   # Minimal busybox for production
   CONFIG_FEATURE_PREFER_APPLETS=y
   CONFIG_FEATURE_SH_STANDALONE=y
   
   # Disable unnecessary applets
   # CONFIG_TELNETD is not set  # Use SSH only
   # CONFIG_FTPD is not set

Build Reproducibility
----------------------

**Deterministic Builds:**

.. code-block:: bash

   # Enable reproducible builds
   BR2_REPRODUCIBLE=y
   
   # This sets:
   # - SOURCE_DATE_EPOCH
   # - Strips timestamps
   # - Sorts file lists
   
   # Verify reproducibility
   make clean
   make -j$(nproc)
   sha256sum output/images/rootfs.squashfs > build1.sha256
   
   make clean
   make -j$(nproc)
   sha256sum output/images/rootfs.squashfs > build2.sha256
   
   diff build1.sha256 build2.sha256

**Version Tracking:**

.. code-block:: bash

   # Include build metadata
   BR2_VERSION_FULL="2.1.0-$(git rev-parse --short HEAD)-$(date +%Y%m%d)"
   
   # Store in image
   echo "${BR2_VERSION_FULL}" > output/target/etc/build-version
   
   # Include in update metadata
   cat > output/images/update-metadata.json <<EOF
   {
     "version": "${BR2_VERSION_FULL}",
     "build_date": "$(date -Iseconds)",
     "git_commit": "$(git rev-parse HEAD)",
     "kernel_version": "$(make -s kernelversion)"
   }
   EOF

Advanced Topics
===============

External Tree
-------------

**Organizing External Customizations:**

.. code-block:: bash

   # Create external tree
   mkdir -p ~/avionics-buildroot-external
   cd ~/avionics-buildroot-external
   
   # Structure
   external/
   ├── Config.in
   ├── external.desc
   ├── external.mk
   ├── board/
   │   └── atom-avionics/
   ├── configs/
   │   └── atom_avionics_defconfig
   └── package/
       ├── avionics-app/
       └── fpga-firmware/
   
   # external.desc
   name: AVIONICS
   desc: Avionics platform external tree
   
   # external.mk
   include $(sort $(wildcard $(BR2_EXTERNAL_AVIONICS_PATH)/package/*/*.mk))
   
   # Config.in
   source "$BR2_EXTERNAL_AVIONICS_PATH/package/avionics-app/Config.in"
   
   # Use external tree
   cd buildroot
   make BR2_EXTERNAL=~/avionics-buildroot-external atom_avionics_defconfig

Package Management
------------------

**Runtime Package Installation (Not typical for embedded):**

.. code-block:: bash

   # For development/testing only
   # Enable package management
   BR2_PACKAGE_OPKG=y
   
   # Or use static package list
   # Better for production

Debugging Builds
----------------

**Enable Debug Information:**

.. code-block:: bash

   # Kernel debug
   CONFIG_DEBUG_INFO=y
   CONFIG_DEBUG_INFO_DWARF4=y
   CONFIG_GDB_SCRIPTS=y
   
   # Buildroot debug
   BR2_ENABLE_DEBUG=y
   BR2_PACKAGE_GDB=y
   BR2_PACKAGE_GDB_SERVER=y

**Build System Debugging:**

.. code-block:: bash

   # Verbose build
   make V=1
   
   # Show commands
   make -n
   
   # Inspect package build
   make avionics-app-dirclean
   make avionics-app-rebuild V=1
   
   # Check dependencies
   make avionics-app-show-depends
   make avionics-app-graph-depends

Best Practices
==============

1. **Use defconfigs** - Don't commit .config files
2. **External trees** - Separate custom code from Buildroot
3. **Version control patches** - Track all customizations
4. **Reproducible builds** - Enable BR2_REPRODUCIBLE
5. **Minimal images** - Only include necessary packages
6. **Security hardening** - SELinux, read-only rootfs, secure boot
7. **Automated testing** - CI/CD for build verification
8. **Documentation** - README with build instructions

Comparison: Buildroot vs Yocto
==============================

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   
   * - Aspect
     - Buildroot
     - Yocto
   * - Learning Curve
     - Easy (Kconfig + Make)
     - Steep (BitBake DSL)
   * - Build Speed
     - Fast
     - Slower (more overhead)
   * - Flexibility
     - Good
     - Excellent
   * - Package Management
     - Limited
     - Advanced (recipes, layers)
   * - Use Case
     - Small/medium systems
     - Complex distributions
   * - Image Size
     - Smaller
     - Larger
   * - Rebuild Speed
     - Full rebuild
     - Incremental
   * - Community
     - Smaller
     - Larger

References
==========

- Buildroot User Manual: https://buildroot.org/docs.html
- Buildroot Training: https://bootlin.com/training/buildroot/
- Embedded Linux Development with Buildroot
- SELinux Project: https://selinuxproject.org/
- UEFI Secure Boot: https://wiki.ubuntu.com/UEFI/SecureBoot

