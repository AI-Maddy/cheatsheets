================================================================================
Linux Build Systems (Yocto & Buildroot) – Comprehensive Reference
================================================================================

:Author: Embedded Linux Build Systems Expert
:Date: January 2026
:Version: 1.0
:Target: Production embedded Linux developers, build engineers, system architects
:Scope: Complete reference for Yocto Project (BitBake, layers, recipes) and Buildroot (menuconfig, packages, defconfigs)

.. contents:: **Table of Contents**
   :depth: 3
   :local:

================================================================================
TL;DR – Quick Reference
================================================================================

**Yocto vs Buildroot Decision Matrix**

+------------------------+---------------------------+---------------------------+
| Feature                | **Yocto Project**         | **Buildroot**             |
+========================+===========================+===========================+
| **Learning curve**     | Steep (weeks-months)      | Gentle (hours-days)       |
+------------------------+---------------------------+---------------------------+
| **Build time**         | Slower (hours first time) | Fast (30-60 min)          |
+------------------------+---------------------------+---------------------------+
| **Flexibility**        | Extreme (layers, recipes) | Good (Kconfig + makefiles)|
+------------------------+---------------------------+---------------------------+
| **Rebuilds**           | Incremental (sstate)      | Slower (less caching)     |
+------------------------+---------------------------+---------------------------+
| **Package management** | Yes (RPM, DEB, IPK)       | No (statically built)     |
+------------------------+---------------------------+---------------------------+
| **Best for**           | Commercial products, BSPs | Prototypes, small systems |
+------------------------+---------------------------+---------------------------+
| **Industry adoption**  | Automotive, aerospace     | IoT, consumer electronics |
+------------------------+---------------------------+---------------------------+

**Essential Yocto Commands**

.. code-block:: bash

    # Environment setup (every session)
    source oe-init-build-env
    
    # Main configuration
    bitbake-layers add-layer ../meta-mylayer
    bitbake core-image-minimal
    
    # Development workflow
    devtool modify busybox              # Edit sources
    devtool build busybox               # Rebuild
    devtool finish busybox meta-custom  # Save patches
    
    # Debugging
    bitbake busybox -c devshell         # Shell in build environment
    bitbake -e busybox | grep ^SRC_URI  # Show final variable values
    bitbake-layers show-appends         # Which .bbappends are active

**Essential Buildroot Commands**

.. code-block:: bash

    # Configuration
    make list-defconfigs                    # Show available boards
    make raspberrypi5_defconfig             # Load board config
    make menuconfig                         # Customize
    
    # Build
    make -j$(nproc)                         # Parallel build
    make sdk                                # Build SDK for app developers
    
    # Package-level iteration
    make busybox-menuconfig                 # Configure busybox
    make linux-menuconfig                   # Configure kernel
    make busybox-rebuild                    # Rebuild one package
    
    # Debugging
    make show-info | jq .                   # Package list (JSON)
    make graph-depends                      # Dependency graph
    make pkg-stats                          # CVE status

**Yocto Layer Structure**

.. code-block:: text

    meta-mylayer/
    ├── conf/
    │   ├── layer.conf                      # Layer metadata
    │   ├── machine/myboard.conf            # Machine definition
    │   └── distro/mydistro.conf            # Distro policy
    ├── recipes-kernel/linux/
    │   ├── linux-yocto_%.bbappend          # Kernel modifications
    │   └── linux-yocto/my.cfg              # Kernel config fragment
    ├── recipes-bsp/u-boot/
    │   └── u-boot_%.bbappend               # Bootloader patches
    ├── recipes-core/images/
    │   └── my-image.bb                     # Custom image recipe
    └── recipes-support/myapp/
        ├── myapp_1.0.bb                    # Application recipe
        └── files/
            ├── myapp.service               # Systemd unit
            └── 0001-fix.patch              # Patches

**Buildroot Package Structure**

.. code-block:: text

    package/myapp/
    ├── Config.in                           # Kconfig menu entry
    ├── myapp.mk                            # Makefile (infrastr. + hooks)
    └── myapp.hash                          # SHA256 checksums
    
    # Global patches directory
    BR2_GLOBAL_PATCH_DIR=board/myboard/patches/

**Key Configuration Files**

*Yocto (build/conf/)*:

- ``local.conf``: MACHINE, DISTRO, IMAGE_FEATURES, parallel build settings
- ``bblayers.conf``: Active layers (BBLAYERS variable)

*Buildroot*:

- ``.config``: Main configuration (generated by menuconfig)
- ``configs/myboard_defconfig``: Minimal saved configuration
- ``BR2_EXTERNAL`` trees: External package/board definitions

================================================================================
Section 1: Yocto Project Architecture
================================================================================

1.1 Overview
------------

**What is Yocto?**

The Yocto Project is a comprehensive Linux distribution build framework comprising:

- **Poky**: Reference distribution (minimal bootable image)
- **OpenEmbedded Core**: Core metadata (recipes, classes, configuration)
- **BitBake**: Task execution engine (Python-based, like make on steroids)

**Architecture Diagram**::

    ┌───────────────────────────────────────────────────────────┐
    │                   Yocto Project                           │
    │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
    │  │   Poky      │  │ meta-oe      │  │  meta-custom    │  │
    │  │ (reference) │  │ (extensions) │  │  (your layers)  │  │
    │  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │
    │         │                │                    │           │
    │         └────────────────┴────────────────────┘           │
    │                          │                                │
    │                   ┌──────▼──────┐                         │
    │                   │  BitBake    │  ← Task executor        │
    │                   └──────┬──────┘                         │
    │                          │                                │
    │         ┌────────────────┼────────────────┐               │
    │         │                │                │               │
    │    ┌────▼────┐    ┌──────▼──────┐  ┌─────▼─────┐         │
    │    │ Recipes │    │  Classes    │  │   Config  │         │
    │    │ (.bb)   │    │ (.bbclass)  │  │  (.conf)  │         │
    │    └─────────┘    └─────────────┘  └───────────┘         │
    └───────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Build Output         │
              │  - Toolchain          │
              │  - Kernel             │
              │  - Root filesystem    │
              │  - Bootloader         │
              │  - SDK                │
              └───────────────────────┘

1.2 Layer System
----------------

**Layer Concept**: Layers are collections of related metadata (recipes, configuration, classes).

**Standard Layer Naming**:

+---------------------+------------------------------------------+---------------------------+
| **Prefix**          | **Purpose**                              | **Example**               |
+=====================+==========================================+===========================+
| ``meta-``           | General layer                            | ``meta-custom``           |
+---------------------+------------------------------------------+---------------------------+
| ``meta-bsp-``       | Board Support Package                    | ``meta-ti``, ``meta-rpi`` |
+---------------------+------------------------------------------+---------------------------+
| ``meta-oe-``        | OpenEmbedded extensions                  | ``meta-python``           |
+---------------------+------------------------------------------+---------------------------+

**Layer Priority**: Higher priority layers override lower priority layers.

.. code-block:: bitbake

    # In conf/layer.conf
    BBFILE_PRIORITY_mylayer = "10"          # Higher = wins

**Layer Dependencies**:

.. code-block:: bitbake

    LAYERDEPENDS_mylayer = "core openembedded-layer"

**Creating a Layer**:

.. code-block:: bash

    # Quick creation (recommended)
    bitbake-layers create-layer ../meta-mylayer
    
    # Generated structure:
    # meta-mylayer/
    # ├── conf/layer.conf
    # ├── recipes-example/example/example.bb
    # └── COPYING.MIT
    
    # Add to build
    bitbake-layers add-layer ../meta-mylayer
    
    # Verify
    bitbake-layers show-layers

**Layer Configuration (conf/layer.conf)**:

.. code-block:: bitbake

    # Add to BBPATH (for conf and classes directories)
    BBPATH .= ":${LAYERDIR}"
    
    # Add recipes
    BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
                ${LAYERDIR}/recipes-*/*/*.bbappend"
    
    # Layer collection (unique identifier)
    BBFILE_COLLECTIONS += "mylayer"
    BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
    BBFILE_PRIORITY_mylayer = "10"
    
    # Layer compatibility (Yocto release codenames)
    LAYERSERIES_COMPAT_mylayer = "nanbield scarthgap"
    
    # Dependencies
    LAYERDEPENDS_mylayer = "core"

1.3 BitBake Fundamentals
-------------------------

**BitBake**: Task-based build system executing recipes.

**Key Concepts**:

- **Recipe (.bb)**: Instructions to build a package
- **Append (.bbappend)**: Modifications to existing recipes
- **Class (.bbclass)**: Reusable functionality
- **Configuration (.conf)**: Global settings

**BitBake Task Execution**::

    do_fetch → do_unpack → do_patch → do_configure → 
    do_compile → do_install → do_package → do_package_write_*

**Common BitBake Commands**:

.. code-block:: bash

    # Build image
    bitbake core-image-minimal
    
    # Build single recipe
    bitbake busybox
    
    # Execute specific task
    bitbake busybox -c configure
    
    # Force task execution
    bitbake busybox -c compile -f
    
    # Clean build artifacts
    bitbake busybox -c cleanall              # Nuclear (work + sstate + downloads)
    bitbake busybox -c cleansstate           # Remove sstate cache only
    
    # Development shell (in build environment)
    bitbake busybox -c devshell
    
    # Show final variable value
    bitbake -e busybox | grep ^SRC_URI=
    
    # Dependency graph
    bitbake -g core-image-minimal            # Generates .dot files
    bitbake -g -u depexp core-image-minimal  # GUI dependency explorer

**BitBake Variables**:

.. code-block:: bitbake

    # Assignment operators
    VAR = "value"                    # Simple assignment
    VAR ?= "default"                 # Set if not already set
    VAR ??= "weak default"           # Weaker default (2026 style)
    VAR += "append"                  # Append with space
    VAR =+ "prepend"                 # Prepend with space
    VAR .= "append-no-space"         # Append without space
    VAR =. "prepend-no-space"        # Prepend without space
    
    # Override syntax (modern 2026 style)
    SRC_URI:append = " file://patch.patch"
    SRC_URI:prepend = "file://first.patch "
    SRC_URI:remove = "file://unwanted.patch"
    
    # Conditional overrides
    SRC_URI:append:raspberrypi5 = " file://rpi5.cfg"
    RDEPENDS:${PN}:append:class-target = " util-linux"

**Variable Expansion**:

.. code-block:: bitbake

    ${VAR}                           # Immediate expansion
    $${VAR}                          # Delayed expansion
    ${@python_expression}            # Python inline code
    
    # Common uses
    S = "${WORKDIR}/git"
    D = "${WORKDIR}/image"           # Destination directory (rootfs staging)
    PN = "package-name"              # Package name
    PV = "1.2.3"                     # Package version
    PR = "r0"                        # Package revision

1.4 devtool Workflow (Modern Recommended Approach)
---------------------------------------------------

**devtool**: High-level tool for recipe development (2026 best practice).

**Common Workflows**:

**A. Modify Existing Recipe**:

.. code-block:: bash

    # 1. Create workspace copy with git repo
    devtool modify busybox
    
    # Sources extracted to: workspace/sources/busybox/
    # Git repo initialized for tracking changes
    
    # 2. Edit sources
    cd workspace/sources/busybox/
    vi networking/httpd.c
    git commit -a -m "Fix buffer overflow"
    
    # 3. Build modified version
    devtool build busybox
    
    # 4. Deploy to running target device
    devtool deploy-target busybox root@192.168.1.100
    
    # 5. Test on target, then finalize
    devtool finish busybox meta-custom
    
    # Result: Creates .bbappend with patches in meta-custom layer
    # meta-custom/recipes-core/busybox/
    # ├── busybox_%.bbappend
    # └── busybox/
    #     └── 0001-Fix-buffer-overflow.patch
    
    # 6. Clean workspace
    devtool reset busybox

**B. Add New Recipe from External Source**:

.. code-block:: bash

    # Add from git
    devtool add myapp https://github.com/vendor/myapp.git
    
    # Add from local directory
    devtool add myapp /path/to/myapp/
    
    # devtool generates initial recipe:
    # workspace/recipes/myapp/myapp_git.bb
    
    # Build and test
    devtool build myapp
    
    # Finalize to custom layer
    devtool finish myapp meta-custom

**C. Upgrade Package Version**:

.. code-block:: bash

    # Attempt automated version upgrade
    devtool upgrade openssl
    
    # devtool:
    # 1. Downloads new version
    # 2. Attempts to apply existing patches
    # 3. Creates new recipe with updated SRCREV/PV
    
    # Review changes, rebuild, test
    devtool build openssl
    
    # Finish upgrade
    devtool finish openssl meta-openembedded

**devtool Status**:

.. code-block:: bash

    devtool status                   # Show active workspace recipes

================================================================================
Section 2: Yocto Recipes
================================================================================

2.1 Recipe Structure
--------------------

**Minimal Recipe Template (myapp_1.0.bb)**:

.. code-block:: bitbake

    SUMMARY = "Short one-line description"
    DESCRIPTION = "Longer multi-line description (optional)"
    AUTHOR = "Your Name <you@example.com>"
    HOMEPAGE = "https://example.com/myapp"
    BUGTRACKER = "https://github.com/vendor/myapp/issues"
    SECTION = "applications"
    
    # License (SPDX identifiers preferred)
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."
    
    # Source location
    SRC_URI = "git://github.com/vendor/myapp.git;protocol=https;branch=main \
               file://0001-fix-build.patch \
               file://myapp.service \
               file://myapp.conf"
    
    # For git sources
    SRCREV = "abcdef1234567890abcdef1234567890abcdef12"
    PV = "1.0+git${SRCPV}"
    
    # Source directory (where unpacked code lives)
    S = "${WORKDIR}/git"
    
    # Inherit build system helpers
    inherit meson pkgconfig systemd
    
    # Build-time dependencies
    DEPENDS = "openssl zlib libcurl"
    
    # Runtime dependencies
    RDEPENDS:${PN} = "bash ca-certificates"
    
    # Systemd integration
    SYSTEMD_SERVICE:${PN} = "myapp.service"
    SYSTEMD_AUTO_ENABLE = "enable"
    
    # Extra meson/cmake/autotools flags
    EXTRA_OEMESON = "-Dfeature-x=enabled -Dfeature-y=disabled"
    
    # Custom install steps (if needed)
    do_install:append() {
        install -d ${D}${sysconfdir}
        install -m 0644 ${WORKDIR}/myapp.conf ${D}${sysconfdir}/
    }
    
    # Package files
    FILES:${PN} += "${bindir}/myapp \
                    ${systemd_system_unitdir}/myapp.service \
                    ${sysconfdir}/myapp.conf"
    
    FILES:${PN}-dev += "${includedir}/myapp/*.h"

**Recipe Variables Reference**:

+---------------------------+-------------------------------------------------------+
| **Variable**              | **Purpose**                                           |
+===========================+=======================================================+
| ``SUMMARY``               | One-line description                                  |
+---------------------------+-------------------------------------------------------+
| ``LICENSE``               | SPDX license identifier                               |
+---------------------------+-------------------------------------------------------+
| ``LIC_FILES_CHKSUM``      | License file + md5/sha256 checksum                    |
+---------------------------+-------------------------------------------------------+
| ``SRC_URI``               | Source locations (tarballs, git, local files)         |
+---------------------------+-------------------------------------------------------+
| ``SRCREV``                | Git commit hash (or tag)                              |
+---------------------------+-------------------------------------------------------+
| ``PV``                    | Package version (usually auto-derived from filename)  |
+---------------------------+-------------------------------------------------------+
| ``PR``                    | Package revision (default: r0)                        |
+---------------------------+-------------------------------------------------------+
| ``S``                     | Source directory (${WORKDIR}/git for git sources)     |
+---------------------------+-------------------------------------------------------+
| ``B``                     | Build directory (default: ${S})                       |
+---------------------------+-------------------------------------------------------+
| ``D``                     | Destination directory (rootfs staging area)           |
+---------------------------+-------------------------------------------------------+
| ``DEPENDS``               | Build-time dependencies                               |
+---------------------------+-------------------------------------------------------+
| ``RDEPENDS:${PN}``        | Runtime dependencies                                  |
+---------------------------+-------------------------------------------------------+
| ``RRECOMMENDS:${PN}``     | Optional runtime recommendations                      |
+---------------------------+-------------------------------------------------------+
| ``FILES:${PN}``           | Files included in main package                        |
+---------------------------+-------------------------------------------------------+
| ``FILES:${PN}-dev``       | Files for development package                         |
+---------------------------+-------------------------------------------------------+
| ``PACKAGES``              | Package split (default: ${PN}-dbg ${PN}-dev ${PN})   |
+---------------------------+-------------------------------------------------------+

2.2 Recipe Appends (.bbappend)
------------------------------

**Purpose**: Modify existing recipes without copying entire .bb file.

**Location**: Must match recipe path structure.

Example: To modify ``meta-oe/recipes-support/openssl/openssl_3.2.bb``:

.. code-block:: text

    meta-custom/recipes-support/openssl/openssl_%.bbappend
    meta-custom/recipes-support/openssl/openssl/my-patch.patch

**Common .bbappend Patterns**:

.. code-block:: bitbake

    # 1. Tell BitBake where to find extra files
    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"
    
    # 2. Add patch
    SRC_URI:append = " file://0001-custom-fix.patch"
    
    # 3. Machine-specific additions
    SRC_URI:append:raspberrypi5 = " file://rpi5-tuning.cfg"
    
    # 4. Modify configure flags
    EXTRA_OECONF:append = " --enable-custom-feature"
    EXTRA_OEMESON:append = " -Dcustom=true"
    
    # 5. Add runtime dependency
    RDEPENDS:${PN}:append = " util-linux"
    
    # 6. Custom install additions
    do_install:append() {
        rm -f ${D}${bindir}/unwanted-tool
        install -d ${D}${sysconfdir}/custom
        install -m 0644 ${WORKDIR}/custom.conf ${D}${sysconfdir}/custom/
    }
    
    # 7. Add subpackage
    PACKAGES += "${PN}-tools"
    FILES:${PN}-tools = "${bindir}/custom-tool*"
    RDEPENDS:${PN}-tools = "${PN}"

2.3 Build System Inheritance
-----------------------------

**Common Classes to Inherit**:

+-------------------------+-------------------------------------------------------+
| **Class**               | **Purpose**                                           |
+=========================+=======================================================+
| ``autotools``           | GNU autotools (./configure, make, make install)       |
+-------------------------+-------------------------------------------------------+
| ``cmake``               | CMake build system                                    |
+-------------------------+-------------------------------------------------------+
| ``meson``               | Meson build system (fast, Python-based)               |
+-------------------------+-------------------------------------------------------+
| ``cargo``               | Rust cargo build                                      |
+-------------------------+-------------------------------------------------------+
| ``qmake5``              | Qt5 qmake                                             |
+-------------------------+-------------------------------------------------------+
| ``python3native``       | Python3 host-side build                               |
+-------------------------+-------------------------------------------------------+
| ``systemd``             | Systemd unit integration                              |
+-------------------------+-------------------------------------------------------+
| ``update-rc.d``         | SysV init script integration                          |
+-------------------------+-------------------------------------------------------+
| ``pkgconfig``           | pkg-config support                                    |
+-------------------------+-------------------------------------------------------+
| ``update-alternatives`` | Manage alternative implementations                    |
+-------------------------+-------------------------------------------------------+
| ``useradd``             | Create users/groups at build time                     |
+-------------------------+-------------------------------------------------------+

**Autotools Example**:

.. code-block:: bitbake

    inherit autotools pkgconfig
    
    EXTRA_OECONF = "--enable-ssl \
                    --disable-static \
                    --with-zlib=${STAGING_LIBDIR}/.."

**Meson Example** (2026 preferred for new projects):

.. code-block:: bitbake

    inherit meson pkgconfig
    
    EXTRA_OEMESON = "-Dfeature-x=enabled \
                     -Dtests=disabled \
                     -Ddocs=false"

**Custom Class Example** (classes/myclass.bbclass):

.. code-block:: bitbake

    # Custom class for company-specific packaging
    
    COMPANY_PREFIX ?= "/opt/company"
    
    do_install:prepend() {
        install -d ${D}${COMPANY_PREFIX}
    }
    
    FILES:${PN} += "${COMPANY_PREFIX}/*"

2.4 Recipe Tasks
----------------

**Standard Task Sequence**:

.. code-block:: text

    do_fetch          → Download sources
    do_unpack         → Extract tarballs / checkout git
    do_patch          → Apply patches
    do_configure      → Run ./configure or equivalent
    do_compile        → Run make or equivalent
    do_install        → Install to ${D} (staging directory)
    do_package        → Split into packages
    do_package_write_* → Create RPM/DEB/IPK packages

**Custom Task Overrides**:

.. code-block:: bitbake

    # Override entire task
    do_compile() {
        ${CC} ${CFLAGS} ${LDFLAGS} main.c -o myapp
    }
    
    # Prepend to existing task
    do_configure:prepend() {
        # Run before standard configure
        sed -i 's/foo/bar/g' ${S}/configure.ac
    }
    
    # Append to existing task
    do_install:append() {
        # Run after standard install
        install -d ${D}${sysconfdir}/init.d
        install -m 0755 ${WORKDIR}/initscript ${D}${sysconfdir}/init.d/myapp
    }
    
    # Task dependencies
    do_compile[depends] += "openssl-native:do_populate_sysroot"

**Common Install Patterns**:

.. code-block:: bitbake

    do_install() {
        # Install binary
        install -d ${D}${bindir}
        install -m 0755 myapp ${D}${bindir}/
        
        # Install library
        install -d ${D}${libdir}
        install -m 0644 libmyapp.so.1.0 ${D}${libdir}/
        ln -sf libmyapp.so.1.0 ${D}${libdir}/libmyapp.so.1
        ln -sf libmyapp.so.1 ${D}${libdir}/libmyapp.so
        
        # Install header
        install -d ${D}${includedir}/myapp
        install -m 0644 ${S}/include/*.h ${D}${includedir}/myapp/
        
        # Install systemd unit
        install -d ${D}${systemd_system_unitdir}
        install -m 0644 ${WORKDIR}/myapp.service ${D}${systemd_system_unitdir}/
        
        # Install configuration
        install -d ${D}${sysconfdir}
        install -m 0644 ${WORKDIR}/myapp.conf ${D}${sysconfdir}/
    }

2.5 Package Splitting
---------------------

**Default Package Split**:

.. code-block:: bitbake

    PACKAGES = "${PN}-dbg ${PN}-staticdev ${PN}-dev ${PN}-doc ${PN}-locale ${PN}"

**Custom Subpackages**:

.. code-block:: bitbake

    # Add custom subpackages BEFORE defaults
    PACKAGES =+ "${PN}-tools ${PN}-examples ${PN}-firmware"
    
    # Define what goes in each
    FILES:${PN} = "${bindir}/myapp \
                   ${libdir}/libmyapp.so.*"
    
    FILES:${PN}-dev = "${includedir}/myapp/*.h \
                       ${libdir}/libmyapp.so \
                       ${libdir}/pkgconfig/myapp.pc"
    
    FILES:${PN}-tools = "${bindir}/myapp-tool* \
                         ${sbindir}/myapp-admin"
    
    FILES:${PN}-examples = "${datadir}/myapp/examples/*"
    
    FILES:${PN}-firmware = "${nonarch_base_libdir}/firmware/myapp/*"
    
    # Define dependencies between subpackages
    RDEPENDS:${PN}-tools = "${PN}"
    RDEPENDS:${PN}-examples = "${PN} python3"

================================================================================
Section 3: Buildroot Architecture
================================================================================

3.1 Overview
------------

**Buildroot Philosophy**: Simple, fast, minimal embedded Linux system generator.

**Key Characteristics**:

- **Kconfig**: Same configuration system as Linux kernel
- **Makefile-based**: GNU Make orchestrates entire build
- **Static linking**: No package manager, everything built into filesystem
- **Fast**: Typically 30-60 minutes for complete system
- **Self-contained**: Generates own toolchain

**Build Flow**::

    make defconfig → make menuconfig → make
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
              Toolchain Build    Packages Build     Rootfs Assembly
              ┌────────────┐     ┌────────────┐     ┌──────────────┐
              │ gcc        │     │ busybox    │     │ ext4         │
              │ binutils   │     │ kernel     │     │ squashfs     │
              │ glibc/musl │     │ libraries  │     │ tar.gz       │
              └────────────┘     │ apps       │     │ initramfs    │
                                 └────────────┘     └──────────────┘
                                        │
                                        ▼
                              output/images/
                              ├── zImage
                              ├── rootfs.ext4
                              ├── rootfs.tar
                              └── sdcard.img

3.2 Directory Structure
-----------------------

**Top-level Directories**:

.. code-block:: text

    buildroot/
    ├── arch/                    # Architecture-specific config
    ├── board/                   # Board-specific files
    │   ├── raspberrypi/
    │   │   ├── post-build.sh    # Post-build hooks
    │   │   ├── post-image.sh    # Post-image generation
    │   │   └── genimage.cfg     # SD card image layout
    ├── boot/                    # Bootloader packages
    ├── configs/                 # Board defconfigs
    │   ├── raspberrypi5_defconfig
    │   └── qemu_aarch64_virt_defconfig
    ├── fs/                      # Filesystem generation
    ├── linux/                   # Kernel build infrastructure
    ├── package/                 # All package definitions
    │   ├── busybox/
    │   ├── dropbear/
    │   └── myapp/
    ├── system/                  # System skeleton, init scripts
    ├── toolchain/               # Toolchain build/external config
    ├── support/                 # Helper scripts
    ├── output/                  # Build output (auto-generated)
    │   ├── build/               # Package build directories
    │   ├── host/                # Host tools
    │   ├── images/              # Final images ★
    │   ├── staging/             # Sysroot (headers + libs)
    │   └── target/              # Populated rootfs
    └── Makefile                 # Main orchestration

**Output Directory Details**:

.. code-block:: text

    output/
    ├── build/                   # Per-package build dirs
    │   ├── busybox-1.36.1/
    │   ├── linux-6.6.12/
    │   └── dropbear-2024.85/
    ├── host/                    # Cross-compilation tools
    │   ├── bin/
    │   │   ├── aarch64-buildroot-linux-gnu-gcc
    │   │   └── aarch64-buildroot-linux-gnu-pkg-config
    │   └── usr/
    ├── images/                  # ★ Final deliverables
    │   ├── Image                # Kernel (ARM64)
    │   ├── rootfs.ext4          # Root filesystem (ext4)
    │   ├── rootfs.tar           # Root filesystem (tarball)
    │   ├── sdcard.img           # Bootable SD card image
    │   └── boot.vfat            # Boot partition (if separate)
    ├── staging/                 # Sysroot for cross-compilation
    │   ├── usr/include/
    │   └── usr/lib/
    └── target/                  # Unpacked rootfs (stripped)
        ├── bin/
        ├── etc/
        ├── lib/
        └── usr/

3.3 Configuration System
-------------------------

**Kconfig Hierarchy**:

.. code-block:: text

    Config.in (top-level)
    ├── Target options
    ├── Build options
    ├── Toolchain
    ├── System configuration
    ├── Kernel
    ├── Target packages
    │   ├── Compressors
    │   ├── Networking applications
    │   ├── Libraries
    │   └── ...
    └── Filesystem images

**Main Configuration Sections**:

**A. Target Options**:

.. code-block:: text

    Architecture: ARM, x86_64, MIPS, etc.
    Architecture variant: Cortex-A53, x86-64, etc.
    Target binary format: ELF
    Target architecture: arm64, x86_64, etc.

**B. Toolchain**:

.. code-block:: text

    Toolchain type:
    - Buildroot toolchain (build from source)
    - External toolchain (Bootlin, Linaro, vendor)
    
    C library:
    - glibc (full-featured, larger)
    - musl (small, modern, recommended 2026)
    - uClibc-ng (very small, embedded)
    
    Kernel headers: Match target kernel version

**C. System Configuration**:

.. code-block:: text

    Root filesystem skeleton: BusyBox default / custom
    System hostname: buildroot
    System banner: Custom message
    Init system:
    - BusyBox init
    - systemd
    - OpenRC
    - None
    /dev management:
    - Static using device table
    - Dynamic using devtmpfs only
    - Dynamic using devtmpfs + mdev
    - Dynamic using devtmpfs + eudev
    Root password: (can be hashed)
    Run a getty after boot: ttyAMA0, ttyS0, etc.

**D. Kernel**:

.. code-block:: text

    Kernel version: Latest, custom tarball, custom git
    Defconfig name: defconfig, vendor_defconfig
    Custom config file: /path/to/.config
    Kernel config fragment files: additional .cfg files
    Device tree source: myboard.dts

**E. Filesystem Images**:

.. code-block:: text

    ext2/3/4 root filesystem
    tar the root filesystem
    cpio the root filesystem (for initramfs)
    squashfs root filesystem
    ubifs root filesystem (for NAND flash)
    iso image (for CD/DVD/USB)

3.4 Package Infrastructure
---------------------------

**Package Anatomy**:

.. code-block:: text

    package/myapp/
    ├── Config.in                # Kconfig menu entry
    ├── myapp.mk                 # Build instructions
    └── myapp.hash               # SHA256 checksums

**Config.in Example**:

.. code-block:: kconfig

    config BR2_PACKAGE_MYAPP
        bool "myapp"
        depends on BR2_PACKAGE_OPENSSL
        select BR2_PACKAGE_ZLIB
        help
          My application does something useful.
          
          https://github.com/vendor/myapp

**myapp.mk Example (generic infrastructure)**:

.. code-block:: makefile

    ################################################################################
    #
    # myapp
    #
    ################################################################################
    
    MYAPP_VERSION = 1.2.3
    MYAPP_SITE = https://github.com/vendor/myapp/archive
    MYAPP_SOURCE = v$(MYAPP_VERSION).tar.gz
    MYAPP_LICENSE = MIT
    MYAPP_LICENSE_FILES = LICENSE
    
    # Dependencies
    MYAPP_DEPENDENCIES = openssl zlib
    
    # Build commands (for non-autotools/cmake/meson)
    define MYAPP_BUILD_CMDS
        $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
    endef
    
    define MYAPP_INSTALL_TARGET_CMDS
        $(INSTALL) -D -m 0755 $(@D)/myapp $(TARGET_DIR)/usr/bin/myapp
        $(INSTALL) -D -m 0644 $(@D)/myapp.conf $(TARGET_DIR)/etc/myapp.conf
    endef
    
    $(eval $(generic-package))

**Package Infrastructures**:

+---------------------------+---------------------------------------------------+
| **Infrastructure**        | **Use Case**                                      |
+===========================+===================================================+
| ``generic-package``       | Manual build commands                             |
+---------------------------+---------------------------------------------------+
| ``autotools-package``     | GNU autotools (./configure, make)                 |
+---------------------------+---------------------------------------------------+
| ``cmake-package``         | CMake build system                                |
+---------------------------+---------------------------------------------------+
| ``meson-package``         | Meson build system                                |
+---------------------------+---------------------------------------------------+
| ``python-package``        | Python setuptools/pip                             |
+---------------------------+---------------------------------------------------+
| ``cargo-package``         | Rust cargo                                        |
+---------------------------+---------------------------------------------------+
| ``kernel-module``         | Out-of-tree kernel modules                        |
+---------------------------+---------------------------------------------------+

**Autotools Package Example**:

.. code-block:: makefile

    MYAPP_VERSION = 2.0
    MYAPP_SITE = https://myapp.org/releases
    MYAPP_SOURCE = myapp-$(MYAPP_VERSION).tar.xz
    MYAPP_LICENSE = GPL-2.0+
    MYAPP_LICENSE_FILES = COPYING
    MYAPP_DEPENDENCIES = openssl
    
    # Configure flags
    MYAPP_CONF_OPTS = --enable-ssl --disable-static
    
    $(eval $(autotools-package))

**CMake Package Example**:

.. code-block:: makefile

    MYAPP_VERSION = 3.1
    MYAPP_SITE = $(call github,vendor,myapp,v$(MYAPP_VERSION))
    MYAPP_LICENSE = BSD-3-Clause
    MYAPP_LICENSE_FILES = LICENSE
    MYAPP_DEPENDENCIES = zlib libcurl
    
    # CMake options
    MYAPP_CONF_OPTS = -DENABLE_TESTS=OFF -DBUILD_SHARED_LIBS=ON
    
    $(eval $(cmake-package))

3.5 Build Phases and Hooks
---------------------------

**Standard Build Phases**:

.. code-block:: text

    download → extract → patch → configure → build → install

**Phase-specific Hooks**:

.. code-block:: makefile

    # PRE hooks (run before phase)
    MYAPP_PRE_DOWNLOAD_HOOKS
    MYAPP_PRE_EXTRACT_HOOKS
    MYAPP_PRE_PATCH_HOOKS
    MYAPP_PRE_CONFIGURE_HOOKS
    MYAPP_PRE_BUILD_HOOKS
    MYAPP_PRE_INSTALL_TARGET_HOOKS
    
    # POST hooks (run after phase)
    MYAPP_POST_DOWNLOAD_HOOKS
    MYAPP_POST_EXTRACT_HOOKS
    MYAPP_POST_PATCH_HOOKS
    MYAPP_POST_CONFIGURE_HOOKS
    MYAPP_POST_BUILD_HOOKS
    MYAPP_POST_INSTALL_TARGET_HOOKS

**Hook Example**:

.. code-block:: makefile

    define MYAPP_FIX_PERMISSIONS
        chmod +x $(@D)/scripts/*.sh
    endef
    MYAPP_POST_EXTRACT_HOOKS += MYAPP_FIX_PERMISSIONS
    
    define MYAPP_INSTALL_INIT_SCRIPT
        $(INSTALL) -D -m 0755 package/myapp/S99myapp \
            $(TARGET_DIR)/etc/init.d/S99myapp
    endef
    MYAPP_POST_INSTALL_TARGET_HOOKS += MYAPP_INSTALL_INIT_SCRIPT

================================================================================
Section 4: Buildroot Workflows
================================================================================

4.1 Common Build Commands
--------------------------

**Configuration**:

.. code-block:: bash

    # List available defconfigs
    make list-defconfigs
    
    # Load board defconfig
    make raspberrypi5_defconfig
    make qemu_aarch64_virt_defconfig
    
    # Customize configuration
    make menuconfig                      # Ncurses UI
    make nconfig                         # Alternative UI
    make xconfig                         # Qt5 GUI (if available)
    
    # Save current config as defconfig
    make savedefconfig
    # Result: defconfig file in current directory
    
    # Apply custom defconfig
    make defconfig BR2_DEFCONFIG=/path/to/my_defconfig

**Building**:

.. code-block:: bash

    # Full build
    make                                 # or: make all
    make -j$(nproc)                      # Parallel build (recommended)
    
    # Download sources only (for offline build)
    make source
    
    # Generate SDK
    make sdk                             # Relocatable SDK for app developers
    
    # Generate documentation
    make manual                          # HTML manual
    make manual-pdf                      # PDF manual

**Package-level Operations**:

.. code-block:: bash

    # Build single package
    make busybox
    make linux
    make dropbear
    
    # Rebuild package
    make busybox-rebuild                 # Re-run build + install
    
    # Reconfigure package
    make linux-menuconfig                # Kernel config
    make busybox-menuconfig              # BusyBox config
    make linux-update-defconfig          # Save kernel config fragment
    
    # Clean package
    make busybox-dirclean                # Remove build directory
    make busybox-clean                   # Clean build artifacts
    
    # Show package dependencies
    make busybox-show-depends
    
    # Show package info
    make show-info | jq '.busybox'

**Cleaning**:

.. code-block:: bash

    # Clean output (keep downloads + .config)
    make clean
    
    # Nuclear clean (remove everything)
    make distclean
    
    # Clean specific package
    make <package>-dirclean

**Debugging and Analysis**:

.. code-block:: bash

    # Package information (JSON)
    make show-info                       # All packages
    make show-info | jq .                # Pretty print
    
    # Dependency graphs (requires graphviz)
    make graph-depends                   # Package dependencies
    make graph-build                     # Build time analysis
    make graph-size                      # Size contribution per package
    
    # CVE and package statistics
    make pkg-stats                       # HTML report in output/
    
    # License compliance
    make legal-info                      # Generate license report
    
    # Print variables
    make printvars                       # All variables
    make printvars VARS=BR2_             # Variables matching pattern
    make printvars PKG=LINUX             # Variables for specific package

4.2 Custom Board Support
-------------------------

**Creating Custom Board Configuration**:

.. code-block:: bash

    # 1. Start from similar board
    make qemu_aarch64_virt_defconfig
    
    # 2. Customize
    make menuconfig
    
    # 3. Save as new defconfig
    make savedefconfig
    mv defconfig configs/myboard_defconfig
    
    # 4. Create board-specific directory
    mkdir -p board/mycompany/myboard
    
    # 5. Add post-build script
    cat > board/mycompany/myboard/post-build.sh << 'EOF'
    #!/bin/bash
    # Custom post-build actions
    echo "Custom build for MyBoard" > ${TARGET_DIR}/etc/board-info
    EOF
    chmod +x board/mycompany/myboard/post-build.sh
    
    # 6. Reference in menuconfig
    # System configuration → Custom scripts to run after creating root fs
    # → board/mycompany/myboard/post-build.sh

**Custom Package Creation**:

.. code-block:: bash

    # 1. Create package directory
    mkdir -p package/myapp
    
    # 2. Create Config.in
    cat > package/myapp/Config.in << 'EOF'
    config BR2_PACKAGE_MYAPP
        bool "myapp"
        help
          My custom application
          https://github.com/mycompany/myapp
    EOF
    
    # 3. Add to parent Config.in
    echo 'source "package/myapp/Config.in"' >> package/Config.in
    
    # 4. Create myapp.mk
    cat > package/myapp/myapp.mk << 'EOF'
    MYAPP_VERSION = 1.0
    MYAPP_SITE = $(call github,mycompany,myapp,v$(MYAPP_VERSION))
    MYAPP_LICENSE = MIT
    MYAPP_LICENSE_FILES = LICENSE
    
    define MYAPP_BUILD_CMDS
        $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
    endef
    
    define MYAPP_INSTALL_TARGET_CMDS
        $(INSTALL) -D -m 0755 $(@D)/myapp $(TARGET_DIR)/usr/bin/myapp
    endef
    
    $(eval $(generic-package))
    EOF
    
    # 5. Create hash file
    cat > package/myapp/myapp.hash << 'EOF'
    # Locally computed
    sha256  abc123...  myapp-1.0.tar.gz
    sha256  def456...  LICENSE
    EOF
    
    # 6. Enable in menuconfig
    make menuconfig
    # Target packages → myapp → [*] myapp

**BR2_EXTERNAL Tree** (recommended for company-specific packages):

.. code-block:: bash

    # 1. Create external tree structure
    mkdir -p ~/mycompany-buildroot
    cd ~/mycompany-buildroot
    
    # 2. Create required files
    cat > external.desc << 'EOF'
    name: MYCOMPANY
    desc: MyCompany custom packages
    EOF
    
    cat > external.mk << 'EOF'
    include $(sort $(wildcard $(BR2_EXTERNAL_MYCOMPANY_PATH)/package/*/*.mk))
    EOF
    
    cat > Config.in << 'EOF'
    source "$BR2_EXTERNAL_MYCOMPANY_PATH/package/Config.in"
    EOF
    
    mkdir -p configs package
    
    # 3. Add packages (same structure as before)
    mkdir -p package/myapp
    # ... create Config.in, myapp.mk, myapp.hash
    
    # 4. Use external tree
    cd /path/to/buildroot
    make BR2_EXTERNAL=~/mycompany-buildroot qemu_aarch64_virt_defconfig
    make menuconfig

4.3 Optimization Techniques
----------------------------

**Build Speed Optimization**:

.. code-block:: bash

    # Enable ccache (compiler cache)
    # BR2_CCACHE=y in menuconfig or .config
    
    # Use parallel builds
    make -j$(nproc)
    
    # Download sources beforehand
    make source
    
    # Use per-package directories (safer parallel builds)
    # BR2_PER_PACKAGE_DIRECTORIES=y
    
    # Use external toolchain instead of building
    # Toolchain → Toolchain type → External toolchain
    # → Toolchain → Bootlin toolchains

**Size Optimization**:

.. code-block:: bash

    # Use musl instead of glibc
    # Toolchain → C library → musl
    
    # Disable unnecessary features
    # Target packages → Show packages that are also provided by busybox
    #                → Disable redundant packages
    
    # Use squashfs (compressed read-only filesystem)
    # Filesystem images → squashfs root filesystem
    
    # Strip binaries (default, but verify)
    # Build options → strip target binaries
    
    # Analyze size contributors
    make graph-size
    # Check output/graphs/graph-size.pdf

================================================================================
Section 5: Exam Question
================================================================================

**Question (18 points): Custom Automotive Gateway Build System**

You are building an automotive gateway device using both Yocto and Buildroot for different product variants:

- **Premium variant**: Yocto-based, full-featured (Ethernet, CAN, diagnostics, OTA updates)
- **Budget variant**: Buildroot-based, minimal (CAN, basic Ethernet)

**Requirements**:

**Part A (6 points)**: Yocto Premium Variant
Create a custom Yocto layer ``meta-autogate`` with:

1. Machine definition for ARM Cortex-A53 gateway controller
2. Custom image recipe with CAN utils, Ethernet tools, systemd
3. Custom application recipe ``autogate-service`` (git source)

Provide:
- Layer structure (directories + files)
- ``conf/layer.conf``
- ``conf/machine/autogate.conf``
- ``recipes-core/images/autogate-image.bb``
- ``recipes-apps/autogate-service/autogate-service_git.bb``

**Part B (5 points)**: Buildroot Budget Variant
Create Buildroot configuration for budget gateway:

1. Custom defconfig enabling CAN, dropbear SSH, basic networking
2. Custom package for CAN gateway application
3. Post-build script to configure CAN interfaces

Provide:
- ``configs/autogate_budget_defconfig`` content
- ``package/can-gateway/`` structure (Config.in, .mk, .hash)
- ``board/autogate/post-build.sh``

**Part C (4 points)**: Integration and CI/CD
Design build automation:

1. Bash script to build both variants
2. Size comparison report
3. Licensing compliance check

**Part D (3 points)**: Trade-offs Analysis
Compare Yocto vs Buildroot for this automotive gateway:

1. Build time (initial + incremental)
2. Package management needs
3. Long-term maintenance effort

--------------------------------------------------------------------------------
**Answer:**
--------------------------------------------------------------------------------

**Part A: Yocto Premium Variant (6 points)**

**Layer Structure**:

.. code-block:: text

    meta-autogate/
    ├── conf/
    │   ├── layer.conf
    │   └── machine/
    │       └── autogate.conf
    ├── recipes-core/
    │   └── images/
    │       └── autogate-image.bb
    └── recipes-apps/
        └── autogate-service/
            ├── autogate-service_git.bb
            └── files/
                └── autogate-service.service

**conf/layer.conf**:

.. code-block:: bitbake

    # Layer configuration for meta-autogate
    
    BBPATH .= ":${LAYERDIR}"
    
    BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
                ${LAYERDIR}/recipes-*/*/*.bbappend"
    
    BBFILE_COLLECTIONS += "autogate"
    BBFILE_PATTERN_autogate = "^${LAYERDIR}/"
    BBFILE_PRIORITY_autogate = "10"
    
    LAYERSERIES_COMPAT_autogate = "nanbield scarthgap"
    LAYERDEPENDS_autogate = "core openembedded-layer"

**conf/machine/autogate.conf**:

.. code-block:: bitbake

    #@TYPE: Machine
    #@NAME: Automotive Gateway Controller
    #@DESCRIPTION: ARM Cortex-A53 based CAN/Ethernet gateway
    
    DEFAULTTUNE = "cortexa53"
    require conf/machine/include/arm/armv8a/tune-cortexa53.inc
    
    MACHINE_FEATURES = "usbhost usbgadget ext2 vfat can ethernet"
    
    # Serial console
    SERIAL_CONSOLES = "115200;ttyS0"
    
    # Kernel
    PREFERRED_PROVIDER_virtual/kernel = "linux-yocto"
    PREFERRED_VERSION_linux-yocto = "6.6%"
    
    # Bootloader
    PREFERRED_PROVIDER_virtual/bootloader = "u-boot"
    
    # CAN support
    MACHINE_ESSENTIAL_EXTRA_RDEPENDS += "kernel-module-can \
                                          kernel-module-can-raw \
                                          kernel-module-can-dev \
                                          kernel-module-vcan"
    
    # Image format
    IMAGE_FSTYPES = "tar.bz2 ext4 wic.xz"
    
    # Extra firmware
    MACHINE_EXTRA_RDEPENDS += "linux-firmware-imx"

**recipes-core/images/autogate-image.bb**:

.. code-block:: bitbake

    SUMMARY = "Automotive Gateway Premium Image"
    DESCRIPTION = "Full-featured gateway image with CAN, Ethernet, OTA, diagnostics"
    LICENSE = "MIT"
    
    inherit core-image
    
    # Base system
    IMAGE_FEATURES += "ssh-server-dropbear \
                       tools-sdk \
                       tools-debug \
                       package-management"
    
    # Networking and CAN utilities
    IMAGE_INSTALL:append = " \
        can-utils \
        canutils \
        libsocketcan \
        ethtool \
        iperf3 \
        tcpdump \
        iproute2 \
        bridge-utils \
        iptables \
        nftables \
        dnsmasq \
        connman \
        curl \
        wget \
        ca-certificates \
        openssh-sftp-server \
        rsync \
        autogate-service \
    "
    
    # System management
    IMAGE_INSTALL:append = " \
        systemd-analyze \
        systemd-networkd \
        systemd-timesyncd \
        procps \
        htop \
        lsof \
        strace \
        gdb \
        vim \
    "
    
    # OTA update support
    IMAGE_INSTALL:append = " \
        swupdate \
        swupdate-www \
        libubootenv-bin \
    "
    
    # Diagnostics
    IMAGE_INSTALL:append = " \
        can-utils \
        i2c-tools \
        spi-tools \
        lmbench \
    "
    
    # Use systemd as init
    DISTRO_FEATURES:append = " systemd"
    DISTRO_FEATURES_BACKFILL_CONSIDERED:append = " sysvinit"
    VIRTUAL-RUNTIME_init_manager = "systemd"
    VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
    
    # Security hardening
    IMAGE_INSTALL:append = " \
        fail2ban \
        audit \
    "
    
    # Set root password (hashed: "gateway123")
    ROOT_PASSWORD_HASH = "$6$saltsaltsa$abc123..."  # Use openssl passwd -6
    
    EXTRA_IMAGE_FEATURES += "read-only-rootfs"

**recipes-apps/autogate-service/autogate-service_git.bb**:

.. code-block:: bitbake

    SUMMARY = "Automotive Gateway Service"
    DESCRIPTION = "Main application for CAN-Ethernet gateway functionality"
    AUTHOR = "Automotive Team <auto@example.com>"
    HOMEPAGE = "https://github.com/mycompany/autogate-service"
    SECTION = "applications"
    
    LICENSE = "Proprietary"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."
    
    # Git source
    SRC_URI = "git://github.com/mycompany/autogate-service.git;protocol=https;branch=main \
               file://autogate-service.service"
    
    SRCREV = "${AUTOREV}"  # Or specific commit hash for production
    PV = "1.0+git${SRCPV}"
    
    S = "${WORKDIR}/git"
    
    # Dependencies
    DEPENDS = "libsocketcan json-c openssl"
    RDEPENDS:${PN} = "can-utils libsocketcan bash"
    
    # Use meson build system
    inherit meson pkgconfig systemd
    
    # Systemd integration
    SYSTEMD_SERVICE:${PN} = "autogate-service.service"
    SYSTEMD_AUTO_ENABLE = "enable"
    
    # Meson options
    EXTRA_OEMESON = "-Dcan-support=true \
                     -Deth-support=true \
                     -Ddiagnostics=true \
                     -Dota-client=true"
    
    # Install systemd unit
    do_install:append() {
        install -d ${D}${systemd_system_unitdir}
        install -m 0644 ${WORKDIR}/autogate-service.service \
            ${D}${systemd_system_unitdir}/
        
        # Install configuration
        install -d ${D}${sysconfdir}/autogate
        install -m 0644 ${S}/config/gateway.conf \
            ${D}${sysconfdir}/autogate/
    }
    
    # Package files
    FILES:${PN} += "${bindir}/autogate-service \
                    ${systemd_system_unitdir}/autogate-service.service \
                    ${sysconfdir}/autogate/gateway.conf"

**recipes-apps/autogate-service/files/autogate-service.service**:

.. code-block:: ini

    [Unit]
    Description=Automotive Gateway Service
    After=network-online.target can.service
    Wants=network-online.target
    
    [Service]
    Type=notify
    ExecStart=/usr/bin/autogate-service --config /etc/autogate/gateway.conf
    Restart=always
    RestartSec=10
    
    # Security hardening
    PrivateTmp=yes
    ProtectSystem=strict
    ProtectHome=yes
    ReadWritePaths=/var/lib/autogate
    NoNewPrivileges=yes
    
    # CAN interface permissions
    AmbientCapabilities=CAP_NET_RAW CAP_NET_ADMIN
    
    [Install]
    WantedBy=multi-user.target

**Build Commands**:

.. code-block:: bash

    # Setup
    cd poky
    source oe-init-build-env build-premium
    
    # Add layers
    bitbake-layers add-layer ../meta-openembedded/meta-oe
    bitbake-layers add-layer ../meta-openembedded/meta-python
    bitbake-layers add-layer ../meta-openembedded/meta-networking
    bitbake-layers add-layer ../meta-autogate
    
    # Configure
    echo 'MACHINE = "autogate"' >> conf/local.conf
    
    # Build
    bitbake autogate-image

**Part B: Buildroot Budget Variant (5 points)**

**configs/autogate_budget_defconfig**:

.. code-block:: text

    BR2_arm=y
    BR2_cortex_a53=y
    BR2_ARM_FPU_VFPV4=y
    
    # Toolchain
    BR2_TOOLCHAIN_EXTERNAL=y
    BR2_TOOLCHAIN_EXTERNAL_BOOTLIN=y
    BR2_TOOLCHAIN_EXTERNAL_BOOTLIN_ARMV8_A_MUSL=y
    
    # System
    BR2_TARGET_GENERIC_HOSTNAME="autogate-budget"
    BR2_TARGET_GENERIC_ISSUE="Automotive Gateway Budget Edition"
    BR2_ROOTFS_OVERLAY="board/autogate/rootfs_overlay"
    BR2_ROOTFS_POST_BUILD_SCRIPT="board/autogate/post-build.sh"
    
    # Init
    BR2_INIT_BUSYBOX=y
    BR2_ROOTFS_DEVICE_CREATION_DYNAMIC_MDEV=y
    
    # Kernel
    BR2_LINUX_KERNEL=y
    BR2_LINUX_KERNEL_CUSTOM_VERSION=y
    BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE="6.6.12"
    BR2_LINUX_KERNEL_DEFCONFIG="defconfig"
    BR2_LINUX_KERNEL_CONFIG_FRAGMENT_FILES="board/autogate/linux-can.cfg"
    BR2_LINUX_KERNEL_DTS_SUPPORT=y
    BR2_LINUX_KERNEL_INTREE_DTS_NAME="autogate"
    
    # Networking
    BR2_PACKAGE_BUSYBOX_CONFIG="package/busybox/busybox-minimal.config"
    BR2_PACKAGE_DROPBEAR=y
    BR2_PACKAGE_ETHTOOL=y
    BR2_PACKAGE_IPROUTE2=y
    BR2_PACKAGE_IPTABLES=y
    
    # CAN support
    BR2_PACKAGE_LIBSOCKETCAN=y
    BR2_PACKAGE_CAN_UTILS=y
    BR2_PACKAGE_CAN_GATEWAY=y
    
    # Utilities
    BR2_PACKAGE_BUSYBOX_SHOW_OTHERS=y
    BR2_PACKAGE_PROCPS_NG=y
    BR2_PACKAGE_UTIL_LINUX=y
    BR2_PACKAGE_UTIL_LINUX_BINARIES=y
    
    # Filesystem
    BR2_TARGET_ROOTFS_EXT2=y
    BR2_TARGET_ROOTFS_EXT2_4=y
    BR2_TARGET_ROOTFS_EXT2_SIZE="64M"
    BR2_TARGET_ROOTFS_TAR=y

**package/can-gateway/Config.in**:

.. code-block:: kconfig

    config BR2_PACKAGE_CAN_GATEWAY
        bool "can-gateway"
        depends on BR2_PACKAGE_LIBSOCKETCAN
        select BR2_PACKAGE_JSON_C
        help
          Lightweight CAN-Ethernet gateway application
          for automotive budget variant.
          
          https://github.com/mycompany/can-gateway

**package/can-gateway/can-gateway.mk**:

.. code-block:: makefile

    ################################################################################
    #
    # can-gateway
    #
    ################################################################################
    
    CAN_GATEWAY_VERSION = 1.0.0
    CAN_GATEWAY_SITE = $(call github,mycompany,can-gateway,v$(CAN_GATEWAY_VERSION))
    CAN_GATEWAY_LICENSE = Proprietary
    CAN_GATEWAY_LICENSE_FILES = LICENSE
    CAN_GATEWAY_DEPENDENCIES = libsocketcan json-c
    
    define CAN_GATEWAY_BUILD_CMDS
        $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
    endef
    
    define CAN_GATEWAY_INSTALL_TARGET_CMDS
        $(INSTALL) -D -m 0755 $(@D)/can-gateway \
            $(TARGET_DIR)/usr/bin/can-gateway
        $(INSTALL) -D -m 0644 $(@D)/gateway.conf \
            $(TARGET_DIR)/etc/can-gateway.conf
    endef
    
    define CAN_GATEWAY_INSTALL_INIT_SYSV
        $(INSTALL) -D -m 0755 package/can-gateway/S99can-gateway \
            $(TARGET_DIR)/etc/init.d/S99can-gateway
    endef
    
    $(eval $(generic-package))

**package/can-gateway/can-gateway.hash**:

.. code-block:: text

    # Locally computed
    sha256  abc123def456...  can-gateway-1.0.0.tar.gz
    sha256  789ghi012jkl...  LICENSE

**package/can-gateway/S99can-gateway** (init script):

.. code-block:: bash

    #!/bin/sh
    
    DAEMON=/usr/bin/can-gateway
    PIDFILE=/var/run/can-gateway.pid
    
    start() {
        printf "Starting CAN gateway: "
        start-stop-daemon -S -q -b -m -p $PIDFILE -x $DAEMON -- \
            --config /etc/can-gateway.conf
        [ $? = 0 ] && echo "OK" || echo "FAIL"
    }
    
    stop() {
        printf "Stopping CAN gateway: "
        start-stop-daemon -K -q -p $PIDFILE
        [ $? = 0 ] && echo "OK" || echo "FAIL"
    }
    
    case "$1" in
        start) start ;;
        stop) stop ;;
        restart) stop; start ;;
        *) echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
    esac

**board/autogate/post-build.sh**:

.. code-block:: bash

    #!/bin/bash
    
    set -e
    
    TARGET_DIR=$1
    
    # Configure CAN interfaces
    cat > ${TARGET_DIR}/etc/network/interfaces.d/can0 << 'EOF'
    auto can0
    iface can0 can static
        bitrate 500000
        restart-ms 100
    EOF
    
    cat > ${TARGET_DIR}/etc/network/interfaces.d/can1 << 'EOF'
    auto can1
    iface can1 can static
        bitrate 250000
        restart-ms 100
    EOF
    
    # Set gateway configuration
    cat > ${TARGET_DIR}/etc/can-gateway.conf << 'EOF'
    {
        "can_interfaces": ["can0", "can1"],
        "eth_interface": "eth0",
        "gateway_mode": "bridge",
        "log_level": "info"
    }
    EOF
    
    # Add board info
    echo "Automotive Gateway Budget v1.0" > ${TARGET_DIR}/etc/board-info
    echo "Build date: $(date)" >> ${TARGET_DIR}/etc/board-info
    
    # Create required directories
    mkdir -p ${TARGET_DIR}/var/log/can-gateway
    
    echo "Post-build configuration complete"

**Part C: Integration and CI/CD (4 points)**

**build-both-variants.sh**:

.. code-block:: bash

    #!/bin/bash
    
    set -e
    
    BUILD_ROOT=$(pwd)
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    REPORT_DIR=${BUILD_ROOT}/build-reports/${TIMESTAMP}
    
    mkdir -p ${REPORT_DIR}
    
    # Build Yocto Premium Variant
    echo "=========================================="
    echo "Building Yocto Premium Variant"
    echo "=========================================="
    
    cd ${BUILD_ROOT}/poky
    source oe-init-build-env build-premium
    
    YOCTO_START=$(date +%s)
    bitbake autogate-image 2>&1 | tee ${REPORT_DIR}/yocto-build.log
    YOCTO_END=$(date +%s)
    YOCTO_TIME=$((YOCTO_END - YOCTO_START))
    
    # Copy artifacts
    cp -r tmp/deploy/images/autogate ${REPORT_DIR}/yocto-images/
    
    # Size analysis
    YOCTO_SIZE=$(du -sh tmp/deploy/images/autogate/autogate-image-autogate.ext4 | cut -f1)
    
    # License report
    bitbake autogate-image -c populate_lic
    cp -r tmp/deploy/licenses ${REPORT_DIR}/yocto-licenses/
    
    # Build Buildroot Budget Variant
    echo "=========================================="
    echo "Building Buildroot Budget Variant"
    echo "=========================================="
    
    cd ${BUILD_ROOT}/buildroot
    make autogate_budget_defconfig
    
    BUILDROOT_START=$(date +%s)
    make -j$(nproc) 2>&1 | tee ${REPORT_DIR}/buildroot-build.log
    BUILDROOT_END=$(date +%s)
    BUILDROOT_TIME=$((BUILDROOT_END - BUILDROOT_START))
    
    # Copy artifacts
    cp -r output/images ${REPORT_DIR}/buildroot-images/
    
    # Size analysis
    BUILDROOT_SIZE=$(du -sh output/images/rootfs.ext4 | cut -f1)
    
    # License report
    make legal-info
    cp -r output/legal-info ${REPORT_DIR}/buildroot-licenses/
    
    # Generate comparison report
    cat > ${REPORT_DIR}/comparison-report.txt << EOF
    ================================================================================
    Build Comparison Report - ${TIMESTAMP}
    ================================================================================
    
    YOCTO PREMIUM VARIANT:
    - Build time: ${YOCTO_TIME} seconds ($(($YOCTO_TIME / 60)) minutes)
    - Image size: ${YOCTO_SIZE}
    - Features: Full (CAN, Ethernet, OTA, diagnostics, systemd)
    - Package management: Yes (RPM)
    
    BUILDROOT BUDGET VARIANT:
    - Build time: ${BUILDROOT_TIME} seconds ($(($BUILDROOT_TIME / 60)) minutes)
    - Image size: ${BUILDROOT_SIZE}
    - Features: Minimal (CAN, basic Ethernet)
    - Package management: No
    
    BUILD TIME COMPARISON:
    - Yocto: ${YOCTO_TIME}s
    - Buildroot: ${BUILDROOT_TIME}s
    - Difference: $((YOCTO_TIME - BUILDROOT_TIME))s ($(((YOCTO_TIME - BUILDROOT_TIME) * 100 / BUILDROOT_TIME))% slower)
    
    SIZE COMPARISON:
    - Yocto: ${YOCTO_SIZE}
    - Buildroot: ${BUILDROOT_SIZE}
    
    LICENSE COMPLIANCE:
    - Yocto licenses: ${REPORT_DIR}/yocto-licenses/
    - Buildroot licenses: ${REPORT_DIR}/buildroot-licenses/
    
    ARTIFACTS:
    - Yocto images: ${REPORT_DIR}/yocto-images/
    - Buildroot images: ${REPORT_DIR}/buildroot-images/
    - Build logs: ${REPORT_DIR}/*.log
    EOF
    
    cat ${REPORT_DIR}/comparison-report.txt
    
    echo "Build complete. Report: ${REPORT_DIR}/comparison-report.txt"

**Part D: Trade-offs Analysis (3 points)**

**Comparison Table**:

+---------------------------+--------------------------------+---------------------------+
| **Aspect**                | **Yocto (Premium)**            | **Buildroot (Budget)**    |
+===========================+================================+===========================+
| **Initial build time**    | 2-4 hours (first build)        | 30-60 minutes             |
+---------------------------+--------------------------------+---------------------------+
| **Incremental build**     | 5-15 min (sstate cache)        | 10-30 min (less caching)  |
+---------------------------+--------------------------------+---------------------------+
| **Package management**    | Yes (RPM/DEB/IPK)              | No (static filesystem)    |
|                           | Field updates easier           | Requires full reflash     |
+---------------------------+--------------------------------+---------------------------+
| **Maintenance effort**    | Higher (complex layers)        | Lower (simple .mk files)  |
|                           | Requires BitBake expertise     | Easier to debug           |
+---------------------------+--------------------------------+---------------------------+
| **BSP integration**       | Excellent (vendor layers)      | Good (vendor defconfigs)  |
+---------------------------+--------------------------------+---------------------------+
| **Customization**         | Very flexible (layers stack)   | Moderate (BR2_EXTERNAL)   |
+---------------------------+--------------------------------+---------------------------+
| **Team learning curve**   | Steep (weeks-months)           | Gentle (days-weeks)       |
+---------------------------+--------------------------------+---------------------------+
| **Build reproducibility** | Good (sstate, downloads)       | Moderate (less caching)   |
+---------------------------+--------------------------------+---------------------------+
| **Industry support**      | Strong (automotive, aero)      | Growing (IoT, embedded)   |
+---------------------------+--------------------------------+---------------------------+
| **Image size**            | Larger (200-500 MB typical)    | Smaller (20-100 MB)       |
+---------------------------+--------------------------------+---------------------------+

**Recommendations for Automotive Gateway**:

**Premium Variant (Yocto)**:
- **Justification**: OTA updates require package management, complex BSP integration with multiple vendors (CAN controllers, Ethernet PHY, automotive MCUs), long product lifecycle (10+ years) benefits from layer-based maintenance
- **Trade-off accepted**: Longer build times acceptable for feature-rich product, team investment in Yocto training worthwhile for multi-product portfolio

**Budget Variant (Buildroot)**:
- **Justification**: Simpler feature set, cost-sensitive market requires smaller team, faster time-to-market critical
- **Trade-off accepted**: No field package updates (full reflash acceptable for budget market), smaller image size reduces flash costs

**Maintenance Strategy**:
- Yocto: Quarterly layer updates, dedicated build engineer
- Buildroot: Monthly package version bumps, any developer can maintain
- Common kernel/driver code shared between variants via git submodules

================================================================================
Section 6: Best Practices and Key Takeaways
================================================================================

6.1 Yocto Best Practices (2026)
--------------------------------

**Layer Management**:

✅ **DO**:
- Use ``devtool`` for all recipe modifications
- Keep layers focused (single responsibility)
- Version control layer dependencies
- Use ``LAYERSERIES_COMPAT`` for release tracking
- Prefer ``:append`` / ``:prepend`` over ``+=`` / ``=+``

❌ **DON'T**:
- Copy entire .bb files when .bbappend suffices
- Modify core layers directly
- Use ``${AUTOREV}`` in production
- Hardcode paths (use variables: ``${bindir}``, ``${sysconfdir}``)

**Recipe Development**:

✅ **DO**:
- Use modern override syntax: ``VAR:append:machine``
- Inherit appropriate classes (autotools, cmake, meson)
- Include accurate ``LIC_FILES_CHKSUM``
- Split packages logically (main, dev, doc)
- Use ``FILESEXTRAPATHS:prepend`` in .bbappend

❌ **DON'T**:
- Override ``do_install`` unnecessarily (use ``:append``)
- Forget ``DEPENDS`` vs ``RDEPENDS`` distinction
- Use ``rm -rf`` in recipes without safeguards

**Build Optimization**:

.. code-block:: bitbake

    # Parallel builds
    BB_NUMBER_THREADS = "16"
    PARALLEL_MAKE = "-j 16"
    
    # Shared state cache
    SSTATE_DIR = "/mnt/ssd/sstate-cache"
    
    # Download directory
    DL_DIR = "/mnt/ssd/downloads"
    
    # Remove unused DISTRO_FEATURES
    DISTRO_FEATURES:remove = "x11 wayland opengl vulkan"

6.2 Buildroot Best Practices (2026)
------------------------------------

**Configuration Management**:

✅ **DO**:
- Use BR2_EXTERNAL for company-specific packages
- Save defconfigs with ``make savedefconfig``
- Use config fragments for kernel/busybox
- Enable per-package directories (BR2_PER_PACKAGE_DIRECTORIES)
- Use external toolchains (Bootlin recommended)

❌ **DON'T**:
- Edit .config directly (use menuconfig)
- Commit full .config (use defconfig)
- Build toolchain when external available
- Forget to version control board/ directory

**Package Development**:

✅ **DO**:
- Use appropriate infrastructure (autotools-package, cmake-package)
- Include .hash file with SHA256
- Use hooks for custom build steps
- Test package in isolation: ``make <pkg>-dirclean && make <pkg>``

❌ **DON'T**:
- Download sources in build step (use SITE properly)
- Hardcode paths (use ``$(TARGET_DIR)``, ``$(STAGING_DIR)``)
- Forget to add package to parent Config.in

**Size Optimization**:

.. code-block:: bash

    # Use musl (smaller than glibc)
    BR2_TOOLCHAIN_BUILDROOT_MUSL=y
    
    # Strip binaries
    BR2_STRIP_strip=y
    
    # Minimize BusyBox
    BR2_PACKAGE_BUSYBOX_CONFIG="package/busybox/busybox-minimal.config"
    
    # Use squashfs
    BR2_TARGET_ROOTFS_SQUASHFS=y
    BR2_TARGET_ROOTFS_SQUASHFS4_XZ=y
    
    # Analyze size contributors
    make graph-size

6.3 Common Pitfalls
-------------------

**Yocto Pitfalls**:

1. **Shared State Cache Corruption**:
   - Symptom: Unexplained build failures, wrong package versions
   - Solution: ``bitbake <recipe> -c cleansstate && bitbake <recipe>``

2. **Layer Priority Conflicts**:
   - Symptom: Wrong recipe version selected
   - Solution: Check ``bitbake-layers show-layers``, adjust priorities

3. **FILESEXTRAPATHS Ordering**:
   - Wrong: ``FILESEXTRAPATHS:append := "${THISDIR}/${PN}:"``
   - Correct: ``FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"``

4. **AUTOREV in Production**:
   - Wrong: ``SRCREV = "${AUTOREV}"``
   - Correct: ``SRCREV = "abc123..."`  # Fixed commit hash

**Buildroot Pitfalls**:

1. **Parallel Build Races**:
   - Solution: Enable BR2_PER_PACKAGE_DIRECTORIES

2. **Config Fragment Ignored**:
   - Check: Fragment must end with ``.cfg``, listed in correct order

3. **Package Not Found**:
   - Verify: ``source "package/myapp/Config.in"`` added to parent Config.in

4. **Hash Mismatch**:
   - Solution: Regenerate with ``./utils/genhash <file>``

6.4 Debugging Techniques
------------------------

**Yocto Debugging**:

.. code-block:: bash

    # Environment variables
    bitbake -e busybox | grep ^SRC_URI=
    
    # Dependency chain
    bitbake -g core-image-minimal
    dot -Tpng task-depends.dot -o deps.png
    
    # Build directory inspection
    bitbake busybox -c devshell
    cd $S  # Source directory
    cd $B  # Build directory
    cd $D  # Destination (install staging)
    
    # Task re-execution
    bitbake busybox -c compile -f
    
    # Show recipe and dependencies
    bitbake-layers show-recipes busybox
    bitbake-layers show-appends busybox

**Buildroot Debugging**:

.. code-block:: bash

    # Package build directory
    cd output/build/<package>-<version>/
    
    # Manual build (after make <pkg>-configure)
    make $(cat ~/buildroot/output/build/<pkg>-<version>/.stamp_configured)
    
    # Check applied patches
    ls output/build/<pkg>/.applied_patches_list
    
    # Variable inspection
    make printvars VARS=BR2_PACKAGE_BUSYBOX
    make printvars PKG=LINUX
    
    # Dependency graph
    make show-depends | grep busybox

6.5 Key Takeaways
-----------------

**When to Choose Yocto**:
- ✅ Commercial products with long lifecycles (10+ years)
- ✅ Need for package management and OTA updates
- ✅ Complex BSP integration (multiple vendors)
- ✅ Automotive, aerospace, industrial applications
- ✅ Team size >5 developers, dedicated build engineer

**When to Choose Buildroot**:
- ✅ Prototypes and development boards
- ✅ Cost-sensitive products with simple requirements
- ✅ Fast time-to-market critical
- ✅ Small teams (<5 developers)
- ✅ IoT devices, consumer electronics
- ✅ Static filesystem acceptable (full reflash for updates)

**Modern Trends (2026)**:
- **musl libc**: Increasingly preferred over glibc (smaller, cleaner)
- **meson build system**: Faster than autotools, Yocto support excellent
- **Systemd dominance**: Most Yocto images, even some Buildroot configs
- **BR2_EXTERNAL**: Standard practice for Buildroot customization
- **devtool**: Yocto standard workflow (replacing manual recipe edits)
- **Container-based builds**: Yocto/Buildroot in Docker for reproducibility
- **SBOM generation**: Supply-chain security drives licensing tools

**Build System Decision Matrix**:

+-----------------------+------------------+------------------+
| **Factor**            | **Yocto**        | **Buildroot**    |
+=======================+==================+==================+
| Build time (initial)  | 2-4 hours        | 30-60 min        |
+-----------------------+------------------+------------------+
| Learning curve        | Steep            | Gentle           |
+-----------------------+------------------+------------------+
| Flexibility           | Extreme          | Good             |
+-----------------------+------------------+------------------+
| Package management    | Yes              | No               |
+-----------------------+------------------+------------------+
| BSP vendor support    | Excellent        | Good             |
+-----------------------+------------------+------------------+
| Image size            | Larger           | Smaller          |
+-----------------------+------------------+------------------+
| Maintenance           | Complex          | Simple           |
+-----------------------+------------------+------------------+

**Final Recommendations**:

1. **Start simple**: Buildroot for proof-of-concept, migrate to Yocto if product complexity grows
2. **Use external toolchains**: Saves hours on every clean build
3. **Automate everything**: CI/CD pipelines for both build systems
4. **Version control carefully**: Commit defconfigs, not full .config
5. **Document layers**: README.md in every custom layer/BR2_EXTERNAL tree
6. **Test incrementally**: ``make <pkg>-rebuild`` or ``bitbake -c compile -f`` for fast iteration
7. **Monitor licenses**: Use ``legal-info`` / ``populate_lic`` for compliance
8. **Cache aggressively**: Shared state cache (Yocto) and ccache (both) save significant time

**Common Commands Reference Card**:

*Yocto*:

.. code-block:: bash

    source oe-init-build-env                 # Setup
    bitbake core-image-minimal               # Build
    devtool modify busybox                   # Edit package
    bitbake busybox -c devshell              # Debug environment
    bitbake-layers show-layers               # List layers

*Buildroot*:

.. code-block:: bash

    make menuconfig                          # Configure
    make -j$(nproc)                          # Build
    make busybox-menuconfig                  # Configure package
    make busybox-rebuild                     # Rebuild package
    make show-info | jq .                    # Package list

================================================================================
End of Build Systems Comprehensive Reference
================================================================================

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Target Audience**: Embedded Linux engineers, BSP developers, build system architects  
**Coverage**: Yocto Project (Scarthgap 5.0, Nanbield 5.1), Buildroot 2025.11 LTS

