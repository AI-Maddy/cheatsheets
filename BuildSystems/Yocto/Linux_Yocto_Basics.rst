================================================================================
Yocto Project Basics for Embedded Linux
================================================================================

**TL;DR**: Yocto Project fundamentals - BitBake build system, Poky reference 
distribution, recipes, layers, and configuration for custom embedded Linux 
distributions. Focus on core concepts and practical usage.

**Related Cheatsheets**: 
:doc:`Buildroot </Linux/buildroot>`, 
:doc:`Linux Kernel </Linux/Linux Kernel>`,
:doc:`Linux Device Tree </Linux/Linux device tree>`,
:doc:`Embedded System Architecture </Embedded/Embedded_System_Architecture_Patterns>`

================================================================================
1. Yocto Project Overview
================================================================================

1.1 What is Yocto?
--------------------------------------------------------------------------------

**Key Concepts**:

- **Yocto Project**: Umbrella project providing tools for custom Linux distributions
- **Poky**: Reference distribution of Yocto Project
- **BitBake**: Task execution engine (similar to make)
- **OpenEmbedded**: Metadata and build framework
- **Metadata**: Recipes, configuration files, classes defining what to build

**Architecture**:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │         User Configuration (local.conf)         │
    │         bblayers.conf, site.conf                │
    └────────────────┬────────────────────────────────┘
                     │
    ┌────────────────▼────────────────────────────────┐
    │              BitBake Engine                     │
    │  (Parses recipes, resolves dependencies,        │
    │   schedules tasks, executes builds)             │
    └────────────────┬────────────────────────────────┘
                     │
    ┌────────────────▼────────────────────────────────┐
    │         Metadata (Recipes & Layers)             │
    │  meta/: Core OE layer                           │
    │  meta-poky/: Poky-specific metadata             │
    │  meta-yocto-bsp/: Reference BSPs                │
    │  meta-custom/: Your custom layers               │
    └────────────────┬────────────────────────────────┘
                     │
    ┌────────────────▼────────────────────────────────┐
    │            Build Output                         │
    │  tmp/deploy/images/: Bootloader, kernel, rootfs │
    │  tmp/deploy/rpm|deb|ipk/: Package feeds         │
    │  tmp/work/: Build artifacts for each recipe     │
    └─────────────────────────────────────────────────┘

**Advantages**:

- Highly customizable
- Supports multiple architectures
- Large community and BSP support
- Reproducible builds
- Package management (RPM, DEB, IPK)
- SDK generation for application development

**Compared to Buildroot**:

+---------------------+-------------------------+-------------------------+
| Feature             | Yocto                   | Buildroot               |
+=====================+=========================+=========================+
| Learning Curve      | Steep                   | Gentle                  |
| Build Time          | Slower (more features)  | Faster                  |
| Flexibility         | Very high               | Moderate                |
| Package Management  | Yes (RPM/DEB/IPK)       | Limited                 |
| Layered Approach    | Yes                     | No                      |
| SDK Generation      | Full SDK support        | Limited                 |
| Best For            | Complex products        | Simple, quick builds    |
+---------------------+-------------------------+-------------------------+

1.2 Directory Structure
--------------------------------------------------------------------------------

**Typical Yocto Build Directory**:

.. code-block:: text

    poky/
    ├── meta/                      # OpenEmbedded-Core layer
    │   ├── classes/               # Build system classes
    │   ├── conf/                  # Configuration files
    │   ├── recipes-*/             # Recipe directories
    │   └── ...
    ├── meta-poky/                 # Poky distribution layer
    ├── meta-yocto-bsp/            # Reference BSPs
    ├── meta-custom/               # Your custom layer (example)
    ├── scripts/                   # Utility scripts
    ├── oe-init-build-env          # Environment setup script
    └── build/                     # Build directory (created)
        ├── conf/
        │   ├── local.conf         # Local configuration
        │   └── bblayers.conf      # Layer configuration
        ├── tmp/                   # Temporary build files
        │   ├── work/              # Build work directories
        │   ├── deploy/            # Final outputs
        │   │   ├── images/        # Kernel, rootfs, etc.
        │   │   └── rpm/deb/ipk/   # Package feeds
        │   └── sysroots/          # Cross-compile sysroots
        ├── downloads/             # Downloaded sources
        └── sstate-cache/          # Shared state cache

================================================================================
2. Getting Started with Yocto
================================================================================

2.1 Initial Setup
--------------------------------------------------------------------------------

**Clone Poky**:

.. code-block:: bash

    # Clone the Yocto Project reference distribution
    git clone -b kirkstone git://git.yoctoproject.org/poky.git
    cd poky
    
    # Common release codenames:
    # - kirkstone (LTS - 4.0.x)
    # - dunfell (LTS - 3.1.x)
    # - honister (3.4.x)
    # - hardknott (3.3.x)

**Setup Build Environment**:

.. code-block:: bash

    # Source the environment setup script
    source oe-init-build-env
    
    # This creates 'build/' directory and sets up environment
    # You'll be in build/ directory after running this
    
    # To return to build later:
    cd poky
    source oe-init-build-env build

**Environment Variables Set**:

.. code-block:: bash

    echo $BUILDDIR    # Points to build directory
    echo $PATH        # Includes BitBake and scripts
    which bitbake     # Should show bitbake in PATH

2.2 Configuration Files
--------------------------------------------------------------------------------

**local.conf** (Build Configuration):

.. code-block:: bash

    # Location: build/conf/local.conf
    
    # Machine selection (target hardware)
    MACHINE ?= "qemux86-64"
    # Options: qemuarm, qemuarm64, qemux86, qemux86-64, qemuppc, qemumips, etc.
    # Or real hardware: beaglebone-yocto, raspberrypi4, etc.
    
    # Distribution (defaults to "poky")
    DISTRO ?= "poky"
    
    # Package management format
    PACKAGE_CLASSES ?= "package_rpm"
    # Options: package_rpm, package_deb, package_ipk
    
    # Number of parallel tasks (set to number of CPU cores)
    BB_NUMBER_THREADS ?= "${@oe.utils.cpu_count()}"
    PARALLEL_MAKE ?= "-j ${@oe.utils.cpu_count()}"
    
    # Disk space monitoring
    BB_DISKMON_DIRS = "\
        STOPTASKS,${TMPDIR},1G,100K \
        STOPTASKS,${DL_DIR},1G,100K \
        STOPTASKS,${SSTATE_DIR},1G,100K \
        ABORT,${TMPDIR},100M,1K \
        ABORT,${DL_DIR},100M,1K \
        ABORT,${SSTATE_DIR},100M,1K"
    
    # Download directory (shared across builds)
    DL_DIR ?= "${TOPDIR}/downloads"
    
    # Shared state cache (speeds up rebuilds)
    SSTATE_DIR ?= "${TOPDIR}/sstate-cache"
    
    # Additional image features
    EXTRA_IMAGE_FEATURES ?= "debug-tweaks tools-debug"
    # debug-tweaks: Allows root login without password
    # tools-debug: Includes debugging tools
    # dev-pkgs: Includes development packages
    # dbg-pkgs: Includes debug symbol packages
    
    # Root password (for non-debug builds)
    # EXTRA_USERS_PARAMS = "usermod -P mypassword root;"

**bblayers.conf** (Layer Configuration):

.. code-block:: bash

    # Location: build/conf/bblayers.conf
    
    BBPATH = "${TOPDIR}"
    BBFILES ?= ""
    
    BBLAYERS ?= " \
      /path/to/poky/meta \
      /path/to/poky/meta-poky \
      /path/to/poky/meta-yocto-bsp \
      "
    
    # To add your custom layer:
    # BBLAYERS += "/path/to/meta-custom"

2.3 Basic Build Commands
--------------------------------------------------------------------------------

**BitBake Commands**:

.. code-block:: bash

    # Build a minimal image
    bitbake core-image-minimal
    
    # Build a full SATO desktop image
    bitbake core-image-sato
    
    # Build only the Linux kernel
    bitbake virtual/kernel
    
    # Build a specific recipe
    bitbake <recipe-name>
    
    # Clean a recipe (remove build artifacts)
    bitbake -c clean <recipe-name>
    
    # Clean and remove downloaded source
    bitbake -c cleanall <recipe-name>
    
    # Force rebuild
    bitbake -c cleansstate <recipe-name>
    bitbake <recipe-name>
    
    # Show recipe dependencies
    bitbake -g <recipe-name>
    bitbake -g core-image-minimal
    # Creates task-depends.dot, pn-depends.dot
    
    # List all available recipes
    bitbake-layers show-recipes
    
    # Search for a recipe
    bitbake-layers show-recipes | grep <pattern>
    
    # Show recipe information
    bitbake-layers show-recipes <recipe-name>

**Build Output**:

.. code-block:: bash

    # Images are located in:
    tmp/deploy/images/${MACHINE}/
    
    # Example for qemux86-64:
    ls tmp/deploy/images/qemux86-64/
    # core-image-minimal-qemux86-64.ext4        # Root filesystem
    # core-image-minimal-qemux86-64.tar.bz2     # Tarball
    # bzImage                                    # Kernel
    # bzImage-qemux86-64.bin                    # Kernel with machine name

================================================================================
3. Running QEMU Images
================================================================================

3.1 Quick QEMU Launch
--------------------------------------------------------------------------------

**Run QEMU Image**:

.. code-block:: bash

    # Run the built image in QEMU
    runqemu qemux86-64
    
    # Or specify image explicitly
    runqemu qemux86-64 core-image-minimal
    
    # With graphics
    runqemu qemux86-64 core-image-sato
    
    # Serial console only (no graphics)
    runqemu qemux86-64 nographic
    
    # With KVM acceleration (much faster)
    runqemu qemux86-64 kvm
    
    # Custom kernel command line
    runqemu qemux86-64 bootparams="console=ttyS0"

**Login**:

.. code-block:: bash

    # Default login (with debug-tweaks enabled):
    # Username: root
    # Password: (none, just press Enter)

3.2 Network Configuration
--------------------------------------------------------------------------------

**Enable Networking in QEMU**:

.. code-block:: bash

    # Run with network enabled
    runqemu qemux86-64 slirp
    
    # Inside QEMU, configure network
    ifconfig eth0 up
    udhcpc -i eth0  # Get IP via DHCP
    
    # Test connectivity
    ping 8.8.8.8

================================================================================
4. BitBake Fundamentals
================================================================================

4.1 Recipe Syntax Basics
--------------------------------------------------------------------------------

**Simple Recipe Structure** (.bb file):

.. code-block:: bash

    # Recipe metadata
    SUMMARY = "Short description"
    DESCRIPTION = "Longer description of the package"
    HOMEPAGE = "http://example.com"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=abc123..."
    
    # Source location
    SRC_URI = "http://example.com/myapp-${PV}.tar.gz"
    SRC_URI[md5sum] = "abc123..."
    SRC_URI[sha256sum] = "def456..."
    
    # Version
    PV = "1.0"
    
    # Dependencies
    DEPENDS = "library1 library2"
    RDEPENDS:${PN} = "runtime-package1 runtime-package2"
    
    # Inherit classes
    inherit autotools
    
    # Installation
    do_install() {
        install -d ${D}${bindir}
        install -m 0755 myapp ${D}${bindir}/
    }

**Common Variables**:

.. code-block:: bash

    ${PN}          # Package name
    ${PV}          # Package version
    ${PR}          # Package revision
    ${P}           # ${PN}-${PV}
    ${S}           # Source directory
    ${B}           # Build directory
    ${D}           # Destination directory (install root)
    ${WORKDIR}     # Working directory
    
    ${bindir}      # /usr/bin
    ${sbindir}     # /usr/sbin
    ${libdir}      # /usr/lib
    ${includedir}  # /usr/include
    ${sysconfdir}  # /etc
    ${datadir}     # /usr/share

4.2 Task Execution
--------------------------------------------------------------------------------

**Common Tasks**:

.. code-block:: bash

    do_fetch      # Download sources
    do_unpack     # Extract sources
    do_patch      # Apply patches
    do_configure  # Configure (e.g., ./configure)
    do_compile    # Build (e.g., make)
    do_install    # Install to ${D}
    do_package    # Create packages
    do_deploy     # Deploy to deploy directory

**Task Dependencies**:

.. code-block:: bash

    # Tasks run in order: fetch → unpack → patch → configure → compile → install
    
    # Add dependency
    do_compile[depends] += "library:do_populate_sysroot"
    
    # Add task after another
    addtask mytask after do_compile before do_install

**Run Specific Task**:

.. code-block:: bash

    # Run only the compile task
    bitbake -c compile <recipe>
    
    # Run fetch task
    bitbake -c fetch <recipe>
    
    # List all tasks for a recipe
    bitbake -c listtasks <recipe>

================================================================================
5. Working with Layers
================================================================================

5.1 Creating a Custom Layer
--------------------------------------------------------------------------------

**Create Layer**:

.. code-block:: bash

    # Use bitbake-layers to create a new layer
    cd poky
    bitbake-layers create-layer meta-custom
    
    # This creates:
    # meta-custom/
    # ├── conf/
    # │   └── layer.conf
    # ├── COPYING.MIT
    # ├── README
    # └── recipes-example/
    #     └── example/
    #         └── example_0.1.bb

**Layer Structure**:

.. code-block:: bash

    meta-custom/
    ├── conf/
    │   └── layer.conf          # Layer configuration
    ├── recipes-core/           # Core recipes (overrides/extensions)
    ├── recipes-kernel/         # Kernel recipes
    ├── recipes-bsp/            # BSP recipes
    ├── recipes-myapp/          # Your application recipes
    │   └── myapp/
    │       ├── myapp_1.0.bb
    │       └── files/
    │           ├── myapp.c
    │           └── myapp.service
    ├── classes/                # Custom classes
    └── COPYING.MIT

**layer.conf**:

.. code-block:: bash

    # Location: meta-custom/conf/layer.conf
    
    # We have a conf and classes directory, add to BBPATH
    BBPATH .= ":${LAYERDIR}"
    
    # We have recipes-* directories, add to BBFILES
    BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
                ${LAYERDIR}/recipes-*/*/*.bbappend"
    
    BBFILE_COLLECTIONS += "meta-custom"
    BBFILE_PATTERN_meta-custom = "^${LAYERDIR}/"
    BBFILE_PRIORITY_meta-custom = "6"
    
    LAYERSERIES_COMPAT_meta-custom = "kirkstone"
    LAYERDEPENDS_meta-custom = "core"

5.2 Adding Layer to Build
--------------------------------------------------------------------------------

**Add to bblayers.conf**:

.. code-block:: bash

    # Manual method - edit build/conf/bblayers.conf
    BBLAYERS += "/path/to/poky/meta-custom"
    
    # Or use bitbake-layers command
    bitbake-layers add-layer ../meta-custom
    
    # Show all layers
    bitbake-layers show-layers
    
    # Remove a layer
    bitbake-layers remove-layer meta-custom

5.3 Layer Priority
--------------------------------------------------------------------------------

**Understanding Priority**:

.. code-block:: bash

    # Higher BBFILE_PRIORITY means higher precedence
    # In layer.conf:
    BBFILE_PRIORITY_meta-custom = "10"
    
    # meta-custom (priority 10) will override:
    # - meta (priority 5)
    # - meta-poky (priority 5)
    # - meta-yocto-bsp (priority 5)

================================================================================
6. Common Images
================================================================================

6.1 Standard Images
--------------------------------------------------------------------------------

**Image Types**:

.. code-block:: bash

    # Minimal console-only image
    core-image-minimal
    # Size: ~10-20 MB
    # Use: Minimal footprint, no package manager
    
    # Minimal with package management
    core-image-base
    # Size: ~30-50 MB
    # Use: Basic system with package manager
    
    # Full-featured image with GUI (SATO desktop)
    core-image-sato
    # Size: ~300+ MB
    # Use: Development, testing with GUI
    
    # Minimal image with SSH server
    core-image-minimal-dev
    # Size: ~20-30 MB
    # Use: Remote development
    
    # Full SDK image
    core-image-full-cmdline
    # Size: ~100+ MB
    # Use: Command-line development tools

**Building**:

.. code-block:: bash

    bitbake core-image-minimal
    bitbake core-image-base
    bitbake core-image-sato

6.2 Image Features
--------------------------------------------------------------------------------

**Adding Features to Images**:

.. code-block:: bash

    # In local.conf:
    
    EXTRA_IMAGE_FEATURES += "debug-tweaks"
    # Allows root login without password, enables serial console
    
    EXTRA_IMAGE_FEATURES += "tools-debug"
    # Adds gdb, strace, tcf-agent, etc.
    
    EXTRA_IMAGE_FEATURES += "package-management"
    # Includes package manager (rpm, opkg, apt)
    
    EXTRA_IMAGE_FEATURES += "ssh-server-openssh"
    # Includes OpenSSH server
    
    EXTRA_IMAGE_FEATURES += "dev-pkgs"
    # Includes development packages (headers, libraries)
    
    IMAGE_FEATURES += "splash"
    # Boot splash screen

================================================================================
7. Common Configuration Patterns
================================================================================

7.1 Customizing Kernel
--------------------------------------------------------------------------------

**Kernel Configuration**:

.. code-block:: bash

    # In local.conf:
    
    # Use a specific kernel version
    PREFERRED_VERSION_linux-yocto = "5.15%"
    
    # Add kernel modules to image
    IMAGE_INSTALL:append = " kernel-modules"
    
    # Or specific modules
    IMAGE_INSTALL:append = " kernel-module-usbserial"

**Kernel Config Fragment**:

.. code-block:: bash

    # Create a bbappend file:
    # meta-custom/recipes-kernel/linux/linux-yocto_%.bbappend
    
    FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
    
    SRC_URI += "file://custom.cfg"
    
    # custom.cfg contains kernel config options:
    # CONFIG_USB_SERIAL=m
    # CONFIG_USB_SERIAL_FTDI_SIO=m

7.2 Adding Packages to Image
--------------------------------------------------------------------------------

**Install Packages**:

.. code-block:: bash

    # In local.conf:
    
    # Add specific packages
    IMAGE_INSTALL:append = " vim git python3"
    
    # Add package groups
    IMAGE_INSTALL:append = " packagegroup-core-buildessential"
    
    # Remove packages
    IMAGE_INSTALL:remove = "busybox"

7.3 Root Filesystem Type
--------------------------------------------------------------------------------

**Filesystem Formats**:

.. code-block:: bash

    # In local.conf:
    
    # Generate multiple formats
    IMAGE_FSTYPES = "ext4 tar.bz2 wic"
    
    # Common formats:
    # ext4       - Standard Linux filesystem
    # tar.bz2    - Compressed tarball
    # cpio.gz    - Initramfs
    # wic        - Disk image with partitions
    # jffs2      - Flash filesystem
    # ubifs      - Flash filesystem
    # squashfs   - Read-only compressed filesystem

================================================================================
8. Troubleshooting
================================================================================

8.1 Common Issues
--------------------------------------------------------------------------------

**Build Failures**:

.. code-block:: bash

    # Check build log
    less tmp/work/<arch>/<recipe>/<version>/temp/log.do_<task>
    
    # Example:
    less tmp/work/core2-64-poky-linux/bash/5.1-r0/temp/log.do_compile
    
    # Increase verbosity
    bitbake -v <recipe>
    
    # Debug mode
    bitbake -D <recipe>

**Fetch Failures**:

.. code-block:: bash

    # Manually download to DL_DIR
    wget -P downloads/ <source-url>
    
    # Check network connectivity
    ping github.com
    
    # Use mirror
    # In local.conf:
    SOURCE_MIRROR_URL = "http://example.com/sources"
    INHERIT += "own-mirrors"

**Disk Space**:

.. code-block:: bash

    # Clean temporary files
    bitbake -c cleanall <recipe>
    
    # Remove old build artifacts
    rm -rf tmp/
    
    # Clean sstate cache
    rm -rf sstate-cache/

8.2 Debugging Tips
--------------------------------------------------------------------------------

**Recipe Debugging**:

.. code-block:: bash

    # Drop into devshell (interactive shell in build environment)
    bitbake -c devshell <recipe>
    
    # This opens shell where you can manually run commands
    
    # Show recipe variables
    bitbake -e <recipe> | grep ^VARIABLE_NAME=
    
    # Example: show source directory
    bitbake -e bash | grep ^S=

**Dependency Issues**:

.. code-block:: bash

    # Show why a package is being built
    bitbake -g <image-name> -u taskexp
    
    # Find which recipe provides a file
    oe-pkgdata-util find-path /usr/bin/bash
    
    # List files in a package
    oe-pkgdata-util list-pkg-files bash

================================================================================
9. Best Practices
================================================================================

9.1 Development Workflow
--------------------------------------------------------------------------------

**DO**:

- Use layers for customization (don't modify meta/)
- Use ``:append`` and ``:prepend`` instead of ``+=`` when possible
- Keep download and sstate-cache outside build directory
- Use shared state cache across builds
- Version control your custom layers
- Document layer dependencies
- Use PREFERRED_VERSION for reproducible builds

**DON'T**:

- Modify files in meta/ directly
- Keep old build artifacts (clean when needed)
- Ignore license compliance
- Use hardcoded paths
- Forget to update layer compatibility

9.2 Performance Optimization
--------------------------------------------------------------------------------

**Speed Up Builds**:

.. code-block:: bash

    # In local.conf:
    
    # Use all CPU cores
    BB_NUMBER_THREADS = "${@oe.utils.cpu_count()}"
    PARALLEL_MAKE = "-j ${@oe.utils.cpu_count()}"
    
    # Shared state mirror
    SSTATE_MIRRORS = "\
        file://.* http://sstate.yoctoproject.org/all/PATH;downloadfilename=PATH \n \
    "
    
    # Premirror (check before fetching)
    PREMIRRORS:prepend = "\
        git://.*/.* http://downloads.yoctoproject.org/mirror/sources/ \n \
    "
    
    # Use RAM disk for tmp (if you have enough RAM)
    # Mount tmpfs to tmp/

================================================================================
See Also
================================================================================

- :doc:`Buildroot </Linux/buildroot>`
- :doc:`Linux Kernel </Linux/Linux Kernel>`
- :doc:`Linux Device Tree </Linux/Linux device tree>`
- :doc:`Yocto Recipes and Layers </Linux/Linux_Yocto_Recipes_Layers>`
