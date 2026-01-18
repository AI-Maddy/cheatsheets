================================================================================
Embedded Linux: Yocto Project and BitBake - Complete Guide
================================================================================

:Author: Embedded Linux Documentation Project
:Date: January 18, 2026
:Reference: Linux Embedded Development (Module 1 Ch6-9, Module 2 Ch1-3)
:Target: Yocto Project 4.0+ (Kirkstone, Langdale, Mickledore)
:Version: 1.0

================================================================================
TL;DR - Quick Reference
================================================================================

**Essential Yocto Commands:**

.. code-block:: bash

   # Clone Poky (Yocto reference distribution)
   git clone -b kirkstone git://git.yoctoproject.org/poky.git
   cd poky
   
   # Setup environment
   source oe-init-build-env
   
   # Edit local.conf
   vim conf/local.conf
   # MACHINE = "beaglebone-yocto"
   # DL_DIR = "/path/to/downloads"
   # SSTATE_DIR = "/path/to/sstate-cache"
   
   # Build image
   bitbake core-image-minimal
   
   # Build SDK
   bitbake -c populate_sdk core-image-minimal
   
   # Clean
   bitbake -c cleanall <recipe>
   
   # Shell into build environment
   bitbake -c devshell <recipe>

**Yocto Directory Structure:**

.. code-block:: text

   poky/
   ├── meta/                    # OpenEmbedded-Core layer
   ├── meta-poky/               # Poky distribution layer
   ├── meta-yocto-bsp/          # BSP layer (reference boards)
   ├── meta-selftest/           # Testing layer
   ├── scripts/                 # Utility scripts
   └── bitbake/                 # BitBake build tool
   
   build/
   ├── conf/
   │   ├── local.conf           # Build configuration
   │   └── bblayers.conf        # Layer configuration
   ├── tmp/
   │   ├── deploy/images/       # Output images
   │   ├── work/                # Build artifacts
   │   └── sysroots/            # Cross-compile sysroots
   └── cache/                   # BitBake cache

**BitBake Recipe Basics:**

.. code-block:: bitbake

   # myapp_1.0.bb
   
   DESCRIPTION = "My Application"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
   
   SRC_URI = "git://github.com/user/myapp.git;protocol=https;branch=main"
   SRCREV = "${AUTOREV}"
   
   S = "${WORKDIR}/git"
   
   inherit autotools  # or cmake, meson
   
   do_install_append() {
       install -d ${D}${bindir}
       install -m 0755 myapp ${D}${bindir}
   }

**Common Yocto Tasks:**

.. code-block:: bash

   # List recipes
   bitbake-layers show-recipes
   
   # Search for recipe
   bitbake-layers show-recipes | grep kernel
   
   # Show recipe dependencies
   bitbake -g core-image-minimal
   
   # List layers
   bitbake-layers show-layers
   
   # Add layer
   bitbake-layers add-layer /path/to/meta-mylayer
   
   # Build specific package
   bitbake busybox
   
   # Get environment for recipe
   bitbake -e busybox | grep ^S=

================================================================================
1. Yocto Project Overview
================================================================================

1.1 What is Yocto Project?
---------------------------

**Definition:**

.. code-block:: text

   Yocto Project is a Linux Foundation project providing:
   - Framework for creating custom Linux distributions
   - Tools for building embedded Linux systems
   - Reference implementations and BSPs
   - Layer-based architecture for customization
   
   Key Components:
   ✓ BitBake - Build tool and task executor
   ✓ OpenEmbedded-Core (OE-Core) - Core recipes and classes
   ✓ Poky - Reference distribution
   ✓ Meta-layers - Extensible layer system
   ✓ Toaster - Web interface for builds
   
   Benefits:
   ✓ Reproducible builds
   ✓ Wide hardware support
   ✓ Package management
   ✓ Cross-compilation infrastructure
   ✓ SDK generation
   ✓ Quality assurance (testing framework)

**Yocto vs Other Build Systems:**

.. code-block:: text

   Yocto:
   ✓ Most flexible, enterprise-grade
   ✓ Steep learning curve
   ✓ Best for complex products, long-term support
   ✓ Used by: automotive, aerospace, industrial
   
   Buildroot:
   ✓ Simpler, easier to learn
   ✓ Less flexible
   ✓ Best for simple embedded systems
   ✓ Faster initial setup
   
   OpenWrt:
   ✓ Router/networking focused
   ✓ Package manager on target
   ✓ Best for network devices

1.2 Yocto Architecture
-----------------------

**Layer Architecture:**

.. code-block:: text

   Layers are collections of recipes organized by:
   - BSP (Board Support Package)
   - Distribution policy
   - Software features
   
   Layer Priority (low to high):
   meta                      # Base layer (OE-Core)
   meta-poky                 # Poky distribution
   meta-yocto-bsp            # Reference BSPs
   meta-<vendor>             # Vendor BSP (TI, NXP, etc.)
   meta-<distro>             # Custom distribution
   meta-<custom>             # Application layer
   
   Higher priority layers override lower layers

**BitBake Workflow:**

.. code-block:: text

   1. Parse recipes (.bb) and configuration files
   2. Resolve dependencies between tasks
   3. Build task dependency graph
   4. Execute tasks in dependency order:
      - do_fetch:     Download sources
      - do_unpack:    Extract sources
      - do_patch:     Apply patches
      - do_configure: Run configure (autotools/cmake)
      - do_compile:   Build source
      - do_install:   Install to ${D}
      - do_package:   Create packages (RPM/DEB/IPK)
      - do_rootfs:    Create root filesystem
      - do_image:     Generate final images
   5. Cache results (sstate)
   6. Deploy output to tmp/deploy/

**Recipe Inheritance:**

.. code-block:: text

   Recipe (.bb)
   ├── Inherits: base.bbclass (automatic)
   ├── Inherits: autotools.bbclass (explicit: inherit autotools)
   │   └── Provides: do_configure, do_compile, do_install
   ├── Inherits: pkgconfig.bbclass
   └── Appends: myapp_1.0.bbappend (from other layers)

================================================================================
2. Getting Started with Yocto
================================================================================

2.1 System Requirements
------------------------

**Host Dependencies:**

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install gawk wget git-core diffstat unzip texinfo \
       gcc-multilib build-essential chrpath socat cpio python3 \
       python3-pip python3-pexpect xz-utils debianutils iputils-ping \
       python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 \
       xterm python3-subunit mesa-common-dev zstd liblz4-tool
   
   # Fedora/RedHat
   sudo dnf install gawk make wget tar bzip2 gzip python3 unzip perl patch \
       diffutils diffstat git cpp gcc gcc-c++ glibc-devel texinfo chrpath \
       ccache perl-Data-Dumper perl-Text-ParseWords perl-Thread-Queue \
       python3-pip xz which SDL-devel xterm
   
   # Minimum requirements:
   # - 50 GB free disk space (100+ GB recommended)
   # - 8 GB RAM minimum (16+ GB recommended)
   # - Multi-core CPU (build time scales with cores)

**Download Poky:**

.. code-block:: bash

   # Clone Poky (Yocto reference distribution)
   git clone -b kirkstone git://git.yoctoproject.org/poky.git
   cd poky
   
   # Yocto releases (use LTS for production):
   # kirkstone (4.0 LTS) - Apr 2022, support until Apr 2026
   # langdale (4.1)      - Oct 2022
   # mickledore (4.2)    - Apr 2023
   # nanbield (4.3)      - Oct 2023
   
   # List available branches
   git branch -r | grep origin/

2.2 First Build
----------------

**Initialize Build Environment:**

.. code-block:: bash

   # Source environment setup script
   cd poky
   source oe-init-build-env
   
   # Creates build/ directory and sets environment:
   # - BUILDDIR: build/
   # - Adds bitbake to PATH
   # - Sets up conf/local.conf and conf/bblayers.conf
   
   # To use custom build directory:
   source oe-init-build-env mybuild

**Configure Build (conf/local.conf):**

.. code-block:: bash

   # Edit build/conf/local.conf
   vim conf/local.conf
   
   # Essential settings:
   
   # Machine (target hardware)
   MACHINE ?= "qemux86-64"
   # or: "beaglebone-yocto", "raspberrypi4-64", "qemuarm", etc.
   
   # Download directory (shared across builds)
   DL_DIR ?= "/opt/yocto/downloads"
   
   # Shared state cache (speeds up rebuilds)
   SSTATE_DIR ?= "/opt/yocto/sstate-cache"
   
   # Build parallelism
   BB_NUMBER_THREADS ?= "8"    # BitBake tasks in parallel
   PARALLEL_MAKE ?= "-j 8"     # Make jobs per task
   
   # Disk space monitoring
   BB_DISKMON_DIRS = "\
       STOPTASKS,${TMPDIR},1G,100K \
       STOPTASKS,${DL_DIR},1G,100K \
       STOPTASKS,${SSTATE_DIR},1G,100K"
   
   # Package management format
   PACKAGE_CLASSES ?= "package_rpm"  # or package_deb, package_ipk
   
   # Additional features
   EXTRA_IMAGE_FEATURES ?= "debug-tweaks tools-debug"
   # debug-tweaks: Enable root login without password, ssh server
   # tools-debug: Include gdb, strace
   # tools-sdk: Include development tools
   # package-management: Include package manager on target

**Build Image:**

.. code-block:: bash

   # Build minimal image
   bitbake core-image-minimal
   
   # Available images:
   # core-image-minimal        - Small image, BusyBox
   # core-image-base           - Console-only with package management
   # core-image-full-cmdline   - Full command-line tools
   # core-image-sato           - X11 with Sato desktop
   # core-image-weston         - Wayland with Weston compositor
   
   # Build time: 1-4 hours (first build), 5-30 min (incremental)
   
   # Output location:
   ls tmp/deploy/images/qemux86-64/
   # core-image-minimal-qemux86-64.ext4
   # core-image-minimal-qemux86-64.tar.bz2
   # core-image-minimal-qemux86-64.manifest
   # bzImage
   # modules-*-qemux86-64.tgz

**Test Image (QEMU):**

.. code-block:: bash

   # Run image in QEMU
   runqemu qemux86-64
   
   # Or specify image explicitly
   runqemu qemux86-64 core-image-minimal
   
   # With networking
   runqemu qemux86-64 nographic slirp
   
   # Login: root (no password with debug-tweaks)

2.3 Understanding Build Output
-------------------------------

**tmp/deploy/images/<machine>/:**

.. code-block:: bash

   # Kernel
   bzImage                  # x86/x86_64
   zImage                   # ARM 32-bit
   Image                    # ARM 64-bit
   
   # Root filesystem
   core-image-minimal-<machine>.ext4          # ext4 image
   core-image-minimal-<machine>.tar.bz2       # Tarball
   core-image-minimal-<machine>.wic           # Flashable SD image
   core-image-minimal-<machine>.squashfs      # Read-only compressed
   
   # Bootloader
   u-boot.bin               # U-Boot
   MLO                      # SPL (AM335x)
   
   # Device tree
   *.dtb                    # Device tree blobs
   
   # Modules
   modules-*.tgz            # Kernel modules
   
   # Manifest
   *.manifest               # List of packages in image

**tmp/work/:**

.. code-block:: bash

   # Build artifacts for each recipe
   tmp/work/<arch>/<recipe>/<version>/
   ├── temp/                # Build logs
   │   ├── log.do_compile
   │   ├── log.do_configure
   │   └── run.do_compile
   ├── <recipe>-<version>/  # Source directory
   ├── image/               # do_install output
   ├── packages-split/      # Package split output
   └── deploy-*/            # Deployed packages

================================================================================
3. BitBake Basics
================================================================================

3.1 BitBake Commands
--------------------

**Basic Commands:**

.. code-block:: bash

   # Build recipe
   bitbake <recipe>
   
   # Build specific task
   bitbake -c <task> <recipe>
   # Common tasks: fetch, compile, install, clean, cleanall
   
   # Example: Rebuild busybox
   bitbake -c cleanall busybox
   bitbake busybox
   
   # Force rebuild (ignore sstate cache)
   bitbake -f <recipe>
   
   # Continue build after failure
   bitbake -k <recipe>
   
   # Dry run (show what would be built)
   bitbake -n <recipe>
   
   # Show recipe information
   bitbake -e <recipe> | less
   # Shows all variables and their values
   
   # Interactive shell in build environment
   bitbake -c devshell <recipe>
   # Opens shell with all environment variables set
   
   # List tasks for recipe
   bitbake -c listtasks <recipe>

**Dependency Graphing:**

.. code-block:: bash

   # Generate dependency graph
   bitbake -g core-image-minimal
   # Creates:
   # task-depends.dot     - Task dependencies
   # recipe-depends.dot   - Recipe dependencies
   # package-depends.dot  - Package dependencies
   
   # View graph
   dot -Tpng task-depends.dot -o task-depends.png
   eog task-depends.png

**BitBake Layers:**

.. code-block:: bash

   # List layers
   bitbake-layers show-layers
   # layer                 path                                      priority
   # ==========================================================================
   # meta                  /path/to/poky/meta                        5
   # meta-poky             /path/to/poky/meta-poky                   5
   # meta-yocto-bsp        /path/to/poky/meta-yocto-bsp              5
   
   # Show recipes
   bitbake-layers show-recipes
   
   # Search recipes
   bitbake-layers show-recipes "*kernel*"
   
   # Show recipe file
   bitbake-layers show-recipes -f busybox
   # busybox:
   #   meta                 1.36.1  /path/to/poky/meta/recipes-core/busybox/busybox_1.36.1.bb
   
   # Add layer
   bitbake-layers add-layer /path/to/meta-mylayer
   # Updates conf/bblayers.conf
   
   # Remove layer
   bitbake-layers remove-layer meta-mylayer
   
   # Create layer
   bitbake-layers create-layer meta-mylayer

3.2 BitBake Variables
----------------------

**Common Variables:**

.. code-block:: bitbake

   # Machine and architecture
   MACHINE               # Target machine (beaglebone-yocto, qemux86-64)
   TARGET_ARCH           # Target architecture (arm, x86_64)
   TUNE_FEATURES         # CPU tuning (armv7a, cortexa8)
   
   # Source handling
   SRC_URI               # Source location(s)
   SRCREV                # Git revision/tag
   S                     # Source directory (${WORKDIR}/git)
   
   # Build directories
   WORKDIR               # Recipe work directory
   D                     # Destination (install) directory
   B                     # Build directory (${S} by default)
   
   # Installation paths
   bindir                # /usr/bin
   sbindir               # /usr/sbin
   libdir                # /usr/lib
   includedir            # /usr/include
   sysconfdir            # /etc
   datadir               # /usr/share
   
   # Version and naming
   PN                    # Package name
   PV                    # Package version
   PR                    # Package revision
   P                     # ${PN}-${PV}
   BPN                   # Base package name (without -native, etc.)
   
   # Dependencies
   DEPENDS               # Build-time dependencies (native tools, libraries)
   RDEPENDS_${PN}        # Runtime dependencies (on target)
   
   # License
   LICENSE               # License type (MIT, GPLv2, etc.)
   LIC_FILES_CHKSUM      # License file checksum

**Variable Operators:**

.. code-block:: bitbake

   # Assignment
   VAR = "value"              # Simple assignment
   VAR ?= "value"             # Assign if not already set
   VAR ??= "value"            # Weak default (lowest priority)
   VAR := "value"             # Immediate expansion
   
   # Append/Prepend
   VAR_append = " value"      # Append (note leading space)
   VAR_prepend = "value "     # Prepend (note trailing space)
   VAR += "value"             # Append with automatic space
   VAR =+ "value"             # Prepend with automatic space
   
   # Remove
   VAR_remove = "value"       # Remove specific value
   
   # Examples:
   SRC_URI = "git://github.com/example/app.git"
   SRC_URI_append = " file://mypatch.patch"
   # Result: SRC_URI = "git://... file://mypatch.patch"
   
   RDEPENDS_${PN} += "libssl"
   # Adds libssl to runtime dependencies

**Variable Expansion:**

.. code-block:: bitbake

   # Variable reference
   FOO = "bar"
   BAZ = "${FOO}"        # BAZ = "bar"
   
   # Path variables
   S = "${WORKDIR}/git"
   
   # Conditional assignment
   VAR = "${@'yes' if d.getVar('DEBUG') == '1' else 'no'}"
   
   # Get variable in Python
   debug = d.getVar('DEBUG')

3.3 BitBake Recipes
-------------------

**Recipe Structure:**

.. code-block:: bitbake

   # example_1.0.bb
   
   # Header: Description and license
   SUMMARY = "Example application"
   DESCRIPTION = "This is an example application for Yocto"
   HOMEPAGE = "https://example.com"
   SECTION = "applications"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."
   
   # Dependencies
   DEPENDS = "libpng zlib"
   RDEPENDS_${PN} = "bash libpng"
   
   # Source
   SRC_URI = "git://github.com/example/app.git;protocol=https;branch=master \
              file://0001-fix-build.patch \
              file://example.conf"
   SRCREV = "abc123def456..."
   
   # Source directory
   S = "${WORKDIR}/git"
   
   # Inherit classes
   inherit autotools pkgconfig
   
   # Configuration options
   EXTRA_OECONF = "--enable-feature-x --disable-feature-y"
   
   # Custom tasks
   do_install_append() {
       install -d ${D}${sysconfdir}
       install -m 0644 ${WORKDIR}/example.conf ${D}${sysconfdir}/
   }
   
   # Package splitting
   PACKAGES = "${PN} ${PN}-dev ${PN}-dbg"
   FILES_${PN} = "${bindir}/* ${sysconfdir}/*"
   FILES_${PN}-dev = "${includedir}/* ${libdir}/*.so"

**Recipe Naming:**

.. code-block:: text

   Recipe filename format:
   <package-name>_<version>.bb
   
   Examples:
   busybox_1.36.1.bb
   linux-yocto_6.1.bb
   python3-requests_2.28.1.bb
   
   Version special values:
   git         - Latest git HEAD
   svn         - Latest SVN revision
   ${PV}       - Use package version variable

**Recipe Inheritance (classes):**

.. code-block:: bitbake

   # inherit <class>
   
   # Common classes:
   inherit autotools          # Autotools (./configure, make, make install)
   inherit cmake              # CMake projects
   inherit meson              # Meson build system
   inherit pkgconfig          # pkg-config support
   inherit systemd            # systemd service integration
   inherit update-rc.d        # SysV init script integration
   inherit kernel             # Linux kernel recipes
   inherit module             # Kernel module recipes
   inherit native             # Build for build host
   inherit cross              # Cross-compile tool
   inherit allarch            # Architecture-independent (scripts, data)

**Recipe Examples:**

.. code-block:: bitbake

   # Simple autotools application
   # hello_1.0.bb
   SUMMARY = "Hello World"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://LICENSE;md5=..."
   
   SRC_URI = "file://hello.c \
              file://Makefile"
   
   S = "${WORKDIR}"
   
   do_compile() {
       ${CC} ${CFLAGS} ${LDFLAGS} hello.c -o hello
   }
   
   do_install() {
       install -d ${D}${bindir}
       install -m 0755 hello ${D}${bindir}/
   }

.. code-block:: bitbake

   # Git-based project with CMake
   # myapp_git.bb
   SUMMARY = "My Application"
   LICENSE = "GPLv2"
   LIC_FILES_CHKSUM = "file://COPYING;md5=..."
   
   DEPENDS = "libusb1 glib-2.0"
   RDEPENDS_${PN} = "libusb1 glib-2.0"
   
   SRC_URI = "git://github.com/user/myapp.git;protocol=https;branch=main \
              file://0001-fix-cross-compile.patch"
   SRCREV = "${AUTOREV}"
   
   S = "${WORKDIR}/git"
   
   inherit cmake pkgconfig
   
   EXTRA_OECMAKE = "-DENABLE_TESTS=OFF"
   
   do_install_append() {
       install -d ${D}${sysconfdir}/myapp
       install -m 0644 ${S}/config/default.conf ${D}${sysconfdir}/myapp/
   }

================================================================================
4. Layers and Configuration
================================================================================

4.1 Understanding Layers
-------------------------

**Layer Structure:**

.. code-block:: text

   meta-mylayer/
   ├── conf/
   │   └── layer.conf           # Layer configuration
   ├── recipes-kernel/
   │   └── linux/
   │       ├── linux-yocto_%.bbappend
   │       └── files/
   │           └── myconfig.cfg
   ├── recipes-core/
   │   └── images/
   │       └── my-custom-image.bb
   ├── recipes-myapp/
   │   └── myapp/
   │       ├── myapp_1.0.bb
   │       └── files/
   │           ├── myapp.c
   │           └── 0001-mypatch.patch
   ├── classes/
   │   └── myclass.bbclass
   └── README

**conf/layer.conf:**

.. code-block:: bitbake

   # Layer configuration
   BBPATH .= ":${LAYERDIR}"
   
   # Add recipes to bitbake search path
   BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
               ${LAYERDIR}/recipes-*/*/*.bbappend"
   
   BBFILE_COLLECTIONS += "mylayer"
   BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
   BBFILE_PRIORITY_mylayer = "6"
   
   # Layer dependencies
   LAYERDEPENDS_mylayer = "core"
   LAYERSERIES_COMPAT_mylayer = "kirkstone langdale"

**Creating a Layer:**

.. code-block:: bash

   # Auto-create layer structure
   bitbake-layers create-layer meta-mylayer
   
   # Manually create
   mkdir meta-mylayer
   cd meta-mylayer
   mkdir -p conf recipes-core/images
   
   # Create layer.conf
   cat > conf/layer.conf << 'EOF'
   BBPATH .= ":${LAYERDIR}"
   BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
               ${LAYERDIR}/recipes-*/*/*.bbappend"
   BBFILE_COLLECTIONS += "mylayer"
   BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
   BBFILE_PRIORITY_mylayer = "6"
   LAYERDEPENDS_mylayer = "core"
   LAYERSERIES_COMPAT_mylayer = "kirkstone"
   EOF
   
   # Add to build
   cd /path/to/build
   bitbake-layers add-layer /path/to/meta-mylayer

4.2 Recipe Appends (.bbappend)
-------------------------------

**Purpose:**

.. code-block:: text

   .bbappend files modify existing recipes without editing original:
   - Add patches
   - Modify configuration
   - Add files
   - Override variables
   - Extend tasks
   
   Naming: Must match recipe name with %:
   linux-yocto_%.bbappend   # Applies to all linux-yocto versions
   busybox_1.36.%.bbappend  # Applies to busybox 1.36.*

**Example .bbappend:**

.. code-block:: bitbake

   # meta-mylayer/recipes-kernel/linux/linux-yocto_%.bbappend
   
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   # Add kernel config fragment
   SRC_URI += "file://myconfig.cfg"
   
   # Add patch
   SRC_URI += "file://0001-add-my-driver.patch"
   
   # Modify kernel config
   do_configure_append() {
       # Enable specific config
       echo "CONFIG_MY_DRIVER=y" >> ${B}/.config
   }

**BusyBox Append Example:**

.. code-block:: bitbake

   # meta-mylayer/recipes-core/busybox/busybox_%.bbappend
   
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   # Add custom config
   SRC_URI += "file://defconfig"
   
   # The defconfig file contains BusyBox configuration

4.3 Configuration Files
------------------------

**conf/local.conf:**

.. code-block:: bash

   # Machine selection
   MACHINE ?= "beaglebone-yocto"
   
   # Distribution
   DISTRO ?= "poky"
   
   # Download and cache directories
   DL_DIR ?= "/opt/yocto/downloads"
   SSTATE_DIR ?= "/opt/yocto/sstate-cache"
   
   # Build parallelism
   BB_NUMBER_THREADS ?= "${@oe.utils.cpu_count()}"
   PARALLEL_MAKE ?= "-j ${@oe.utils.cpu_count()}"
   
   # Package format
   PACKAGE_CLASSES ?= "package_rpm"
   
   # Image features
   EXTRA_IMAGE_FEATURES ?= "debug-tweaks tools-debug ssh-server-openssh"
   
   # Root password (hashed)
   EXTRA_USERS_PARAMS = "usermod -P mypassword root;"
   
   # Additional packages in all images
   IMAGE_INSTALL_append = " myapp python3 vim"
   
   # SDK path
   SDKMACHINE ?= "x86_64"
   
   # Remove unused packages from sysroot
   INHERIT += "rm_work"
   
   # Use systemd instead of SysV init
   DISTRO_FEATURES_append = " systemd"
   VIRTUAL-RUNTIME_init_manager = "systemd"
   VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"

**conf/bblayers.conf:**

.. code-block:: python

   # POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
   # changes incompatibly
   POKY_BBLAYERS_CONF_VERSION = "2"
   
   BBPATH = "${TOPDIR}"
   BBFILES ?= ""
   
   BBLAYERS ?= " \
     /path/to/poky/meta \
     /path/to/poky/meta-poky \
     /path/to/poky/meta-yocto-bsp \
     /path/to/meta-openembedded/meta-oe \
     /path/to/meta-openembedded/meta-python \
     /path/to/meta-openembedded/meta-networking \
     /path/to/meta-mylayer \
     "

================================================================================
5. Custom Images
================================================================================

5.1 Creating Custom Image
--------------------------

**Basic Image Recipe:**

.. code-block:: bitbake

   # meta-mylayer/recipes-core/images/my-custom-image.bb
   
   SUMMARY = "My Custom Embedded Linux Image"
   LICENSE = "MIT"
   
   # Inherit core image class
   inherit core-image
   
   # Base image packages (from core-image-minimal)
   IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
   
   # Add custom packages
   IMAGE_INSTALL += " \
       busybox \
       util-linux \
       e2fsprogs \
       mtd-utils \
       i2c-tools \
       python3 \
       openssh \
       myapp \
       "
   
   # Image features
   IMAGE_FEATURES += "ssh-server-openssh splash package-management"
   
   # Root filesystem extra space (in KB)
   IMAGE_ROOTFS_EXTRA_SPACE = "512000"
   
   # Image format
   IMAGE_FSTYPES = "tar.bz2 ext4 wic"

**Image Based on Existing:**

.. code-block:: bitbake

   # my-custom-image.bb - Based on core-image-base
   
   require recipes-core/images/core-image-base.bb
   
   SUMMARY = "Custom image based on core-image-base"
   
   # Add additional packages
   IMAGE_INSTALL += " \
       kernel-modules \
       python3-numpy \
       opencv \
       gstreamer1.0 \
       myapplication \
       "
   
   # Additional features
   IMAGE_FEATURES += "tools-debug tools-sdk"

5.2 Package Groups
------------------

**Creating Package Group:**

.. code-block:: bitbake

   # meta-mylayer/recipes-core/packagegroups/packagegroup-myapps.bb
   
   SUMMARY = "My application package group"
   LICENSE = "MIT"
   
   inherit packagegroup
   
   RDEPENDS_${PN} = " \
       myapp1 \
       myapp2 \
       python3-requests \
       openssh-sftp-server \
       "

**Using Package Group in Image:**

.. code-block:: bitbake

   # my-custom-image.bb
   IMAGE_INSTALL += "packagegroup-myapps"

5.3 Image Features
------------------

**Common IMAGE_FEATURES:**

.. code-block:: text

   debug-tweaks           # Root login without password, other debug aids
   tools-debug            # gdb, strace, ltrace
   tools-sdk              # gcc, make, autotools (development on target)
   dev-pkgs               # Development packages (headers, .so files)
   dbg-pkgs               # Debug symbol packages
   staticdev-pkgs         # Static libraries
   doc-pkgs               # Documentation
   package-management     # Package manager (rpm, apt, opkg)
   splash                 # Boot splash screen
   ssh-server-dropbear    # Dropbear SSH server (lightweight)
   ssh-server-openssh     # OpenSSH server (full-featured)
   hwcodecs               # Hardware codec support
   read-only-rootfs       # Read-only root filesystem

**Custom IMAGE_FEATURES:**

.. code-block:: bitbake

   # In distro or layer conf
   IMAGE_FEATURES[validitems] += "myfeature"
   
   # Define feature
   FEATURE_PACKAGES_myfeature = "packagegroup-myfeature"

================================================================================
6. Working with Kernel
================================================================================

6.1 Kernel Recipe
-----------------

**linux-yocto:**

.. code-block:: bash

   # Yocto provides linux-yocto (mainline + Yocto patches)
   # Recipe: meta/recipes-kernel/linux/linux-yocto_*.bb
   
   # Configure kernel
   bitbake -c menuconfig virtual/kernel
   
   # Save config as fragment
   # 1. Make changes in menuconfig
   # 2. Save .config
   # 3. Create fragment:
   bitbake -c diffconfig virtual/kernel
   # Creates fragment-*.cfg in build directory

**Kernel Config Fragment:**

.. code-block:: bash

   # meta-mylayer/recipes-kernel/linux/files/myconfig.cfg
   CONFIG_CAN=m
   CONFIG_CAN_RAW=m
   CONFIG_CAN_BCM=m
   CONFIG_CAN_VCAN=m
   # CONFIG_USB_SERIAL_FTDI_SIO is not set
   
   # Apply fragment via append
   # meta-mylayer/recipes-kernel/linux/linux-yocto_%.bbappend
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   SRC_URI += "file://myconfig.cfg"

**Custom Kernel Patch:**

.. code-block:: bitbake

   # linux-yocto_%.bbappend
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   SRC_URI += " \
       file://0001-add-custom-driver.patch \
       file://0002-enable-feature.patch \
       "

6.2 Device Tree Customization
------------------------------

**Device Tree Append:**

.. code-block:: bitbake

   # linux-yocto_%.bbappend
   FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
   
   SRC_URI += "file://custom-board.dts"
   
   # Compile custom DTB
   KERNEL_DEVICETREE_append = " custom-board.dtb"

**Device Tree Overlay:**

.. code-block:: bitbake

   # For runtime overlay loading
   SRC_URI += "file://my-overlay.dts"
   
   do_compile_append() {
       dtc -@ -I dts -O dtb -o ${B}/my-overlay.dtbo ${WORKDIR}/my-overlay.dts
   }
   
   do_install_append() {
       install -d ${D}/boot/overlays
       install -m 0644 ${B}/my-overlay.dtbo ${D}/boot/overlays/
   }

6.3 Kernel Modules
------------------

**Out-of-Tree Kernel Module:**

.. code-block:: bitbake

   # mymodule_1.0.bb
   SUMMARY = "My custom kernel module"
   LICENSE = "GPLv2"
   LIC_FILES_CHKSUM = "file://COPYING;md5=..."
   
   inherit module
   
   SRC_URI = "file://mymodule.c \
              file://Makefile \
              file://COPYING"
   
   S = "${WORKDIR}"
   
   # Kernel module class handles:
   # - Cross-compilation setup
   # - Installation to /lib/modules/
   # - Dependency on kernel

**Makefile for Module:**

.. code-block:: make

   # Makefile
   obj-m := mymodule.o
   
   SRC := $(shell pwd)
   
   all:
   	$(MAKE) -C $(KERNEL_SRC) M=$(SRC)
   
   modules_install:
   	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install
   
   clean:
   	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c
   	rm -f Module.markers Module.symvers modules.order
   	rm -rf .tmp_versions Modules.symvers

================================================================================
7. SDK and Application Development
================================================================================

7.1 Building SDK
----------------

**Generate SDK:**

.. code-block:: bash

   # Build SDK for image
   bitbake -c populate_sdk core-image-minimal
   
   # Output:
   # tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-cortexa8hf-neon-beaglebone-yocto-toolchain-4.0.sh
   
   # Install SDK
   ./poky-glibc-x86_64-core-image-minimal-*.sh
   # Default install: /opt/poky/4.0
   
   # Setup environment
   source /opt/poky/4.0/environment-setup-cortexa8hf-neon-poky-linux-gnueabi
   
   # Cross-compile application
   $CC -o myapp myapp.c
   # Uses: arm-poky-linux-gnueabi-gcc

**Extensible SDK (eSDK):**

.. code-block:: bash

   # Build extensible SDK (includes bitbake)
   bitbake -c populate_sdk_ext core-image-minimal
   
   # Install
   ./poky-glibc-x86_64-core-image-minimal-*.sh
   
   # Setup
   source /path/to/esdk/environment-setup-cortexa8hf-neon-poky-linux-gnueabi
   
   # Can build recipes using devtool
   devtool add myapp https://github.com/user/myapp.git
   devtool build myapp
   devtool deploy-target myapp root@192.168.1.100

7.2 Using SDK
-------------

**Cross-Compiling with SDK:**

.. code-block:: bash

   # Source SDK environment
   source /opt/poky/4.0/environment-setup-*
   
   # Check environment
   echo $CC
   # arm-poky-linux-gnueabi-gcc -march=armv7-a -mfpu=neon ...
   
   # Compile C application
   $CC -o hello hello.c
   
   # Compile with library
   $CC -o myapp myapp.c $(pkg-config --cflags --libs libpng)
   
   # CMake project
   mkdir build && cd build
   cmake ..
   make
   
   # Autotools project
   ./configure $CONFIGURE_FLAGS
   make

================================================================================
8. Exam-Style Questions
================================================================================

**Q1:** What is the difference between DEPENDS and RDEPENDS?

**A:** DEPENDS: Build-time dependencies (tools, libraries needed to compile).
RDEPENDS_${PN}: Runtime dependencies (packages needed on target to run).

**Q2:** How do you add a custom layer to Yocto build?

**A:** `bitbake-layers add-layer /path/to/meta-mylayer`
Updates conf/bblayers.conf automatically.

**Q3:** What is a .bbappend file used for?

**A:** Modifies existing recipes without editing original. Used to add patches,
config files, or override variables. Must match recipe name (e.g., linux-yocto_%.bbappend).

**Q4:** How to build minimal image for QEMU ARM?

**A:**
.. code-block:: bash

   source oe-init-build-env
   # Edit conf/local.conf: MACHINE = "qemuarm"
   bitbake core-image-minimal
   runqemu qemuarm

**Q5:** What directory contains final build output images?

**A:** `tmp/deploy/images/<machine>/`
Contains kernel, rootfs, bootloader, device trees.

**Q6:** How to clean and rebuild a specific recipe?

**A:** `bitbake -c cleanall <recipe>` then `bitbake <recipe>`

**Q7:** What class is used for CMake-based recipes?

**A:** `inherit cmake`

**Q8:** How to add packages to all images?

**A:** In conf/local.conf: `IMAGE_INSTALL_append = " myapp python3"`

**Q9:** What is sstate cache?

**A:** Shared state cache stores prebuilt task outputs, enabling fast rebuilds
by reusing results when inputs haven't changed.

**Q10:** How to generate SDK for cross-compilation?

**A:** `bitbake -c populate_sdk core-image-minimal`
Install .sh script, source environment-setup script.

================================================================================
9. Key Takeaways
================================================================================

.. code-block:: text

   Yocto Workflow:
   ===============
   1. source oe-init-build-env
   2. Edit conf/local.conf (MACHINE, DL_DIR, SSTATE_DIR)
   3. Edit conf/bblayers.conf (add layers)
   4. bitbake <image>
   5. Deploy from tmp/deploy/images/<machine>/
   
   BitBake Basics:
   ===============
   bitbake <recipe>               # Build
   bitbake -c cleanall <recipe>   # Clean
   bitbake -c devshell <recipe>   # Interactive shell
   bitbake -e <recipe>            # Show variables
   bitbake -g <recipe>            # Dependency graph
   bitbake-layers show-layers     # List layers
   bitbake-layers add-layer       # Add layer
   
   Recipe Structure:
   =================
   LICENSE, LIC_FILES_CHKSUM     # Required
   SRC_URI, SRCREV               # Source location
   DEPENDS, RDEPENDS_${PN}       # Dependencies
   S, B, D                       # Directories
   inherit <class>               # autotools, cmake, systemd
   do_compile, do_install        # Custom tasks
   
   Layers:
   =======
   meta-mylayer/
   ├── conf/layer.conf
   ├── recipes-*/
   └── classes/
   
   .bbappend files modify recipes:
   linux-yocto_%.bbappend
   
   Configuration:
   ==============
   conf/local.conf      # Build config (MACHINE, features)
   conf/bblayers.conf   # Layer list
   
   Custom Image:
   =============
   inherit core-image
   IMAGE_INSTALL += "myapp python3"
   IMAGE_FEATURES += "ssh-server-openssh"
   IMAGE_FSTYPES = "tar.bz2 ext4 wic"
   
   SDK:
   ====
   bitbake -c populate_sdk <image>
   Install .sh script
   source environment-setup-*
   $CC -o myapp myapp.c
   
   Common Variables:
   =================
   MACHINE              # Target hardware
   DL_DIR               # Download cache
   SSTATE_DIR           # Shared state cache
   IMAGE_INSTALL        # Packages in image
   EXTRA_IMAGE_FEATURES # Image features
   BB_NUMBER_THREADS    # BitBake parallelism
   PARALLEL_MAKE        # Make jobs per recipe

================================================================================
END OF CHEATSHEET
================================================================================